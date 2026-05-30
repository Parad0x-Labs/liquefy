#!/usr/bin/env python3
"""
NULL_K8s_Native_Velocity - [NULL VELOCITY v1]
==============================================
TARGET: High-Velocity K8s/Docker JSON Logs.
GOAL:   Maximum Speed + Structural Compression.
TECH:   Vectorized Regex + Block Columnar + Searchable Content Stream.
STATUS: 100% Lossless, Searchable.
"""

import time
import re
import zstandard as zstd
import struct
import xxhash
import sys
import io

PROTOCOL_ID = b'NIT\x01'

def pack_varint(val: int) -> bytes:
    if val < 0x80: return struct.pack("B", val)
    out = bytearray()
    while val >= 0x80:
        out.append((val & 0x7F) | 0x80); val >>= 7
    out.append(val & 0x7F)
    return bytes(out)

def unpack_varint_buf(data: bytes, pos: int) -> tuple:
    val = data[pos]; pos += 1
    if val < 0x80: return val, pos
    res = val & 0x7F; shift = 7
    while True:
        b = data[pos]; pos += 1
        res |= (b & 0x7F) << shift
        if not (b & 0x80): break
        shift += 7
    return res, pos

class BloomIndex:
    def __init__(self):
        self.ba = bytearray(4096)
    def add(self, token: bytes):
        h = xxhash.xxh64(token).intdigest()
        self.ba[(h & 0x7FFF) >> 3] |= (1 << (h & 7))
        self.ba[((h >> 16) & 0x7FFF) >> 3] |= (1 << ((h >> 16) & 7))
    def check(self, token: bytes) -> bool:
        h = xxhash.xxh64(token).intdigest()
        if not (self.ba[(h & 0x7FFF) >> 3] & (1 << (h & 7))): return False
        if not (self.ba[((h >> 16) & 0x7FFF) >> 3] & (1 << ((h >> 16) & 7))): return False
        return True

RE_K8S_FAST = re.compile(rb'^{"log":"((?:[^"\\]|\\.)*)","stream":"(stdout|stderr)","time":"([^"]+)"}\n$')

class NULL_K8s_Native_Velocity:
    def __init__(self, level=3): # Balanced for Nitro speed
        self.cctx = zstd.ZstdCompressor(level=level)
        self.dctx = zstd.ZstdDecompressor()

    def compress(self, raw: bytes) -> bytes:
        col_content, col_time, col_stream, col_raw = [], [], bytearray(), []
        bitmap = bytearray(); curr_byte = 0; bit_idx = 0; bloom = BloomIndex()
        total_lines = 0
        
        lines = raw.splitlines(keepends=True)
        for line in lines:
            total_lines += 1
            m = RE_K8S_FAST.match(line)
            if m:
                col_stream.append(0 if m.group(2) == b'stdout' else 1)
                content = m.group(1); col_content.append(content)
                if len(content) > 4:
                    for tok in content.split(b' '):
                        if len(tok) > 3: bloom.add(tok)
                col_time.append(m.group(3))
            else:
                curr_byte |= (1 << bit_idx); col_raw.append(line)
            bit_idx += 1
            if bit_idx == 8:
                bitmap.append(curr_byte); curr_byte = 0; bit_idx = 0
        if bit_idx > 0: bitmap.append(curr_byte)

        def pack_column(items):
            b = bytearray()
            for x in items: b.extend(pack_varint(len(x))); b.extend(x)
            return b

        rle_stream = bytearray()
        if col_stream:
            last = col_stream[0]; count = 0
            for s in col_stream:
                if s == last: count += 1
                else:
                    rle_stream.extend(pack_varint(count)); rle_stream.append(last)
                    last = s; count = 1
            rle_stream.extend(pack_varint(count)); rle_stream.append(last)
            
        payload = bytearray()
        payload.extend(pack_varint(total_lines))
        for chunk in [bitmap, rle_stream, pack_column(col_time), pack_column(col_raw), pack_column(col_content)]:
            payload.extend(pack_varint(len(chunk))); payload.extend(chunk)
        
        idx_bytes = bytes(bloom.ba)
        return PROTOCOL_ID + struct.pack('<I', len(idx_bytes)) + idx_bytes + self.cctx.compress(payload)

    def decompress(self, blob: bytes) -> bytes:
        if not blob.startswith(PROTOCOL_ID): raise ValueError("Invalid Magic")
        idx_len = struct.unpack('<I', blob[4:8])[0]
        data = self.dctx.decompress(blob[8+idx_len:]); p = 0
        
        total_lines, p = unpack_varint_buf(data, p)
        
        def read_chunk():
            nonlocal p; l, p = unpack_varint_buf(data, p); c = data[p:p+l]; p += l; return c
            
        bitmap, rle_stream, blob_time, blob_raw, blob_content = [read_chunk() for _ in range(5)]
        
        def unpack_col(b):
            res, ptr = [], 0
            while ptr < len(b):
                l, ptr = unpack_varint_buf(b, ptr); res.append(b[ptr:ptr+l]); ptr += l
            return iter(res)
            
        iter_time, iter_raw, iter_content = unpack_col(blob_time), unpack_col(blob_raw), unpack_col(blob_content)
        stream_vals = []; sr_ptr = 0
        while sr_ptr < len(rle_stream):
            count, sr_ptr = unpack_varint_buf(rle_stream, sr_ptr); val = rle_stream[sr_ptr]; sr_ptr += 1
            stream_vals.extend([val] * count)
        iter_stream = iter(stream_vals)
        
        out = io.BytesIO()
        P, M, MS, ME, S, E = b'{"log":"', b'","stream":"', b'stdout', b'stderr', b'","time":"', b'"}\n'
        
        for bm_idx in range(total_lines):
            byte_idx, bit_offset = bm_idx // 8, bm_idx % 8
            if (bitmap[byte_idx] >> bit_offset) & 1:
                out.write(next(iter_raw))
            else:
                out.write(P); out.write(next(iter_content)); out.write(M)
                out.write(MS if next(iter_stream) == 0 else ME)
                out.write(S); out.write(next(iter_time)); out.write(E)
                
        return out.getvalue()

    def grep(self, blob: bytes, query: str):
        idx_len = struct.unpack('<I', blob[4:8])[0]
        idx = BloomIndex(); idx.ba = bytearray(blob[8:8+idx_len])
        q = query.encode()
        if not idx.check(q): return
        data = self.dctx.decompress(blob[8+idx_len:]); p = 0
        _, p = unpack_varint_buf(data, p) # total_lines
        def skip(): nonlocal p; l, p = unpack_varint_buf(data, p); p += l
        for _ in range(4): skip()
        l, p = unpack_varint_buf(data, p); content_blob = data[p:p+l]
        print(f"Found {content_blob.count(q)} matches for '{query}'")

if __name__ == "__main__":
    if len(sys.argv) < 3: print("Usage: python NULL_K8s_Native_Velocity.py [compress|decompress|grep] <in> <out/query>"); sys.exit(1)
    codec = NULL_K8s_Native_Velocity()
    if sys.argv[1] == "compress":
        with open(sys.argv[2], "rb") as f: data = f.read()
        with open(sys.argv[3], "wb") as f: f.write(codec.compress(data))
    elif sys.argv[1] == "decompress":
        with open(sys.argv[2], "rb") as f: data = f.read()
        with open(sys.argv[3], "wb") as f: f.write(codec.decompress(data))
    elif sys.argv[1] == "grep":
        with open(sys.argv[2], "rb") as f: data = f.read()
        codec.grep(data, sys.argv[3])
