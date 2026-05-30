#!/usr/bin/env python3
"""
NULL_Sql_Native_Velocity - [NULL VELOCITY v1]
==============================================
TARGET: Enterprise SQL Dumps @ Native Speeds.
TECH:   Direct C-Transform + Smart Column Buffers + Zstd.
"""

import time
import ctypes
import os
import zstandard as zstd
import xxhash

PROTOCOL_ID = b'SQC\x01'

try:
    # Try local path first
    base_path = os.path.dirname(os.path.abspath(__file__))
    lib = ctypes.CDLL(os.path.join(base_path, "sql_scanner.so"))
except:
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        lib = ctypes.CDLL(os.path.join(base_path, "sql_scanner.dll"))
    except:
        lib = None

lib.transform_sql.argtypes = [
    ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32, # In
    ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_uint32), # Tpl Out
    ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_uint32), # Var Out
    ctypes.POINTER(ctypes.c_uint32) # Var Count
]
lib.transform_sql.restype = ctypes.c_int32

class NULL_Sql_Native_Velocity:
    def __init__(self, level=3):
        self.cctx = zstd.ZstdCompressor(level=level)
        self.dctx = zstd.ZstdDecompressor()

    def compress(self, raw: bytes) -> bytes:
        # Buffers
        raw_ptr = (ctypes.c_uint8 * len(raw)).from_buffer_copy(raw)
        tpl_out = (ctypes.c_uint8 * (len(raw) * 2))()
        var_out = (ctypes.c_uint8 * (len(raw) * 2))()
        
        tpl_len = ctypes.c_uint32(0)
        var_len = ctypes.c_uint32(0)
        var_count = ctypes.c_uint32(0)
        
        # ONE NATIVE CALL
        lib.transform_sql(raw_ptr, len(raw), 
                          tpl_out, ctypes.byref(tpl_len), 
                          var_out, ctypes.byref(var_len), 
                          ctypes.byref(var_count))
        
        # 3. Final Compression (Combined bytes)
        # Layout: [TplLen][Tpl][VCount][VarStream]
        # We use a simple separator for Zstd to find
        combined = bytes(tpl_out[:tpl_len.value]) + b'TITAN' + bytes(var_out[:var_len.value])
        
        payload = self.cctx.compress(combined)
        return PROTOCOL_ID + payload

    def decompress(self, blob: bytes) -> bytes:
        if not blob.startswith(PROTOCOL_ID): return b""
        stream = self.dctx.decompress(blob[4:])
        
        tpl_part, var_part = stream.split(b'TITAN', 1)
        
        # Reconstruct (Still in Python, but very fast)
        out = bytearray()
        parts = tpl_part.split(b"\x00")
        
        v_ptr = 0
        def unpack_varint():
            nonlocal v_ptr
            res = 0; shift = 0
            while True:
                b = var_part[v_ptr]; v_ptr += 1
                res |= (b & 0x7F) << shift
                if not (b & 0x80): break
                shift += 7
            return res

        for i in range(len(parts)-1):
            out.extend(parts[i])
            v_l = unpack_varint()
            out.extend(var_part[v_ptr:v_ptr+v_l])
            v_ptr += v_l
        out.extend(parts[-1])
        return bytes(out)

if __name__ == "__main__":
    codec = NULL_Sql_Native_Velocity()
    if len(os.sys.argv) > 2:
        with open(os.sys.argv[2], "rb") as f: d = f.read()
        if os.sys.argv[1] == "compress":
            with open(os.sys.argv[3], "wb") as f: f.write(codec.compress(d))
        else:
            with open(os.sys.argv[3], "wb") as f: f.write(codec.decompress(d))
