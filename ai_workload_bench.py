#!/usr/bin/env python3
"""
AI Workload Benchmarks for Liquefy Columnar Engine.
Measures actual compression ratios for 5 AI-specific workload types.
"""
import sys
import os
import json
import random
import struct
import time
import zstandard as zstd

# Wire the engine path
sys.path.insert(0, r"F:\Enterprise  tests\liquefy\engines\json_codec")
sys.path.insert(0, r"F:\Enterprise  tests\liquefy\engines")
sys.path.insert(0, r"F:\Enterprise  tests\liquefy\src\liquefy")

from NULL_Json_Columnar_Gun_v1 import NULL_Json_Columnar_Gun_v1

# -----------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------

def make_jsonl(rows: list) -> bytes:
    lines = [json.dumps(r, separators=(',', ':')) for r in rows]
    return ('\n'.join(lines) + '\n').encode('utf-8')

def zstd_compress(data: bytes, level: int = 3) -> bytes:
    cctx = zstd.ZstdCompressor(level=level)
    return cctx.compress(data)

def ratio(original: bytes, compressed: bytes) -> float:
    return len(original) / len(compressed)

def bench(name: str, data: bytes, engine: NULL_Json_Columnar_Gun_v1) -> dict:
    t0 = time.perf_counter()
    liq = engine.compress(data)
    liq_ms = (time.perf_counter() - t0) * 1000

    zstd3 = zstd_compress(data, level=3)
    zstd22 = zstd_compress(data, level=22)

    r_liq   = ratio(data, liq)
    r_z3    = ratio(data, zstd3)
    r_z22   = ratio(data, zstd22)
    r_vs_z3 = r_liq / r_z3

    return {
        "workload": name,
        "rows": data.count(b'\n'),
        "raw_bytes": len(data),
        "liquefy_bytes": len(liq),
        "zstd3_bytes": len(zstd3),
        "zstd22_bytes": len(zstd22),
        "ratio_liquefy": round(r_liq, 1),
        "ratio_zstd3": round(r_z3, 1),
        "ratio_zstd22": round(r_z22, 1),
        "liquefy_vs_zstd3": round(r_vs_z3, 2),
        "liquefy_ms": round(liq_ms, 1),
    }

def print_result(r: dict):
    print(f"\n{'='*60}")
    print(f"  {r['workload']}")
    print(f"{'='*60}")
    print(f"  Rows             : {r['rows']:,}")
    print(f"  Raw bytes        : {r['raw_bytes']:,}")
    print(f"  Liquefy bytes    : {r['liquefy_bytes']:,}")
    print(f"  zstd-3 bytes     : {r['zstd3_bytes']:,}")
    print(f"  zstd-22 bytes    : {r['zstd22_bytes']:,}")
    print(f"  --- Ratios ---")
    print(f"  Liquefy          : {r['ratio_liquefy']}x")
    print(f"  zstd-3           : {r['ratio_zstd3']}x")
    print(f"  zstd-22          : {r['ratio_zstd22']}x")
    print(f"  Liquefy / zstd-3 : {r['liquefy_vs_zstd3']}x better")
    print(f"  Compress ms      : {r['liquefy_ms']} ms")

# -----------------------------------------------------------------------
# WORKLOAD 1: LLM API Response Logs
# -----------------------------------------------------------------------
def workload_llm_logs(n=50_000):
    models = ["claude-3-5", "claude-3-opus", "gpt-4o", "gpt-4-turbo", "gemini-1.5-pro"]
    tools  = ["web_search", "code_exec", "file_read", "calculator", "browser"]
    sessions = [f"sess-{random.randint(100000,999999):06x}" for _ in range(200)]
    base_ts = 1748000000

    rows = []
    for i in range(n):
        rows.append({
            "model":      random.choice(models),
            "tokens_in":  random.randint(100, 4000),
            "tokens_out": random.randint(50, 2000),
            "cost":       round(random.uniform(0.0001, 0.05), 6),
            "ts":         base_ts + i * 3,
            "session":    random.choice(sessions),
            "tool":       random.choice(tools),
        })
    return make_jsonl(rows)

# -----------------------------------------------------------------------
# WORKLOAD 2: Agent Tool Call Traces (OpenTelemetry-style spans)
# -----------------------------------------------------------------------
def workload_agent_traces(n=50_000):
    services    = ["agent-core", "tool-dispatcher", "memory-store"]
    span_names  = ["web_search", "web_search", "web_search",  # heavily repeated
                   "code_exec", "file_read", "llm_call"]
    statuses    = ["OK", "OK", "OK", "ERROR"]  # mostly OK
    base_ts_us  = 1748000000_000_000  # microseconds

    rows = []
    ts = base_ts_us
    for i in range(n):
        rows.append({
            "trace_id":    f"trace-{i:010d}",
            "span_id":     f"span-{i:010d}",
            "parent_id":   f"span-{max(0,i-1):010d}",
            "service":     random.choice(services),
            "name":        random.choice(span_names),
            "start_us":    ts,
            "duration_ms": random.randint(1, 5000),
            "status":      random.choice(statuses),
        })
        ts += random.randint(100_000, 2_000_000)  # sequential with jitter
    return make_jsonl(rows)

# -----------------------------------------------------------------------
# WORKLOAD 3: Embedding Store Metadata
# -----------------------------------------------------------------------
def workload_embedding_meta(n=50_000):
    models = ["text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"]
    base_ts = 1748000000

    rows = []
    for i in range(n):
        doc_id   = (i // 100) + 1
        chunk_id = (i % 100) + 1
        rows.append({
            "id":         f"emb-{i:08d}",
            "model":      random.choice(models),
            "created_at": base_ts + i,
            "chunk_id":   f"doc-{doc_id:04d}-chunk-{chunk_id:03d}",
            "token_count": random.randint(128, 512),
        })
    return make_jsonl(rows)

# -----------------------------------------------------------------------
# WORKLOAD 4: x402 Receipts (stripped — no random hash fields)
# -----------------------------------------------------------------------
def workload_x402_stripped(n=50_000):
    import string
    _b58 = string.ascii_uppercase + string.ascii_lowercase + string.digits
    _b58 = [c for c in _b58 if c not in 'IOl0']  # base58 alphabet
    def rand_addr(length=44):
        return ''.join(random.choices(_b58, k=length))
    senders   = [rand_addr() for _ in range(50)]
    receivers = [rand_addr() for _ in range(10)]
    models    = ["claude-3-5", "claude-3-opus", "gpt-4o"]
    base_ts   = 1748000000

    rows = []
    for i in range(n):
        rows.append({
            "amount":      random.randint(1, 10000),
            "sender":      random.choice(senders),
            "receiver":    random.choice(receivers),
            "timestamp":   base_ts + i,
            "model":       random.choice(models),
            "tokens_used": random.randint(100, 4000),
        })
    return make_jsonl(rows)

# -----------------------------------------------------------------------
# WORKLOAD 5: Token ID Sequences (JSON array, integers 0-100k)
# -----------------------------------------------------------------------
def workload_token_ids(n=50_000):
    """Each row is {"seq": <int>, "token": <int 0-100k>}
    This lets us measure columnar integer encoding of token IDs.
    The token column is the interesting one — random 0-100k."""
    rows = []
    for i in range(n):
        rows.append({
            "seq":   i,
            "token": random.randint(0, 100_000),
        })
    return make_jsonl(rows)

def workload_token_ids_flat(n=50_000):
    """All tokens as one big JSON array (single row), to test raw int array behavior."""
    tokens = [random.randint(0, 100_000) for _ in range(n)]
    data   = json.dumps(tokens, separators=(',', ''))
    return data.encode('utf-8')

# -----------------------------------------------------------------------
# ANALYSIS: per-column encoding mode breakdown
# -----------------------------------------------------------------------
def analyze_encoding_modes(engine, data: bytes, label: str):
    """
    Decompose the compressed blob and report which encoding mode each column got,
    cardinality, and per-column size.
    """
    blob = engine.compress(data)
    if not blob.startswith(b'COL2'):
        print(f"  [{label}] Unexpected protocol")
        return

    MODES = {
        0x01: "dict-1B-idx (low-card)",
        0x02: "raw-join (high-card)",
        0x03: "float64 (raw)",
        0x04: "complex-json",
        0x05: "delta-int",
        0x06: "numeric-suffix-str",
        0x07: "dict-2B-idx (mid-card legacy)",
        0x08: "ISO-timestamp-delta",
        0x09: "dict+delta-idx (mid-card)",
        0x00: "empty",
    }

    ptr = 4
    row_count = struct.unpack('<I', blob[ptr:ptr+4])[0]; ptr += 4
    num_cols  = struct.unpack('<H', blob[ptr:ptr+2])[0]; ptr += 2
    ptr += 1
    order_len = struct.unpack('<I', blob[ptr:ptr+4])[0]; ptr += 4
    key_order = json.loads(blob[ptr:ptr+order_len]); ptr += order_len
    p_len     = struct.unpack('<I', blob[ptr:ptr+4])[0]; ptr += 4; ptr += p_len

    dctx = zstd.ZstdDecompressor()
    print(f"\n  [{label}] {row_count} rows, {num_cols} cols")

    def unpack_varint(buf, pos):
        res = 0; shift = 0
        while True:
            b = buf[pos]; pos += 1
            res |= (b & 0x7F) << shift
            if not (b & 0x80): break
            shift += 7
        return res, pos

    for _ in range(num_cols):
        name_len, ptr = unpack_varint(blob, ptr)
        col_name = blob[ptr:ptr+name_len].decode(); ptr += name_len
        pay_len  = struct.unpack('<I', blob[ptr:ptr+4])[0]; ptr += 4
        pay_blob = blob[ptr:ptr+pay_len]; ptr += pay_len
        payload  = dctx.decompress(pay_blob)
        mode     = payload[0] if payload != b'\x00' else 0x00
        mode_str = MODES.get(mode, f"0x{mode:02x}")
        print(f"    col={col_name:<20} mode={mode_str:<35} compressed={pay_len:>6} bytes")

# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------
def main():
    random.seed(42)  # reproducible
    engine = NULL_Json_Columnar_Gun_v1(level=22, fast=True)

    print("\n" + "="*60)
    print("  LIQUEFY AI WORKLOAD BENCHMARKS")
    print("  Each workload: 50,000 rows")
    print("="*60)

    results = []

    # W1: LLM logs
    print("\n[1/5] Generating LLM API response logs...")
    d1 = workload_llm_logs(50_000)
    r1 = bench("W1: LLM API Response Logs (50k rows)", d1, engine)
    print_result(r1)
    analyze_encoding_modes(engine, d1, "LLM logs")
    results.append(r1)

    # W2: Agent traces
    print("\n[2/5] Generating agent tool call traces...")
    d2 = workload_agent_traces(50_000)
    r2 = bench("W2: Agent Tool Call Traces / OTel Spans (50k rows)", d2, engine)
    print_result(r2)
    analyze_encoding_modes(engine, d2, "OTel spans")
    results.append(r2)

    # W3: Embedding metadata
    print("\n[3/5] Generating embedding store metadata...")
    d3 = workload_embedding_meta(50_000)
    r3 = bench("W3: Embedding Store Metadata (50k rows)", d3, engine)
    print_result(r3)
    analyze_encoding_modes(engine, d3, "Embedding meta")
    results.append(r3)

    # W4: x402 stripped receipts
    print("\n[4/5] Generating x402 receipts (stripped)...")
    d4 = workload_x402_stripped(50_000)
    r4 = bench("W4: x402 Receipts Stripped (50k rows)", d4, engine)
    print_result(r4)
    analyze_encoding_modes(engine, d4, "x402 stripped")
    results.append(r4)

    # W5: Token IDs (columnar rows)
    print("\n[5/5] Generating token ID sequences...")
    d5 = workload_token_ids(50_000)
    r5 = bench("W5: Token ID Sequences as Columnar Rows (50k rows)", d5, engine)
    print_result(r5)
    analyze_encoding_modes(engine, d5, "Token IDs")
    results.append(r5)

    # W5b: raw array baseline
    d5b = workload_token_ids_flat(50_000)
    z3_flat  = zstd_compress(d5b, 3)
    z22_flat = zstd_compress(d5b, 22)
    print(f"\n  [W5 flat-array baseline]")
    print(f"  Raw JSON array {len(d5b):,} bytes")
    print(f"  zstd-3 : {len(d5b)/len(z3_flat):.1f}x")
    print(f"  zstd-22: {len(d5b)/len(z22_flat):.1f}x")
    print(f"  (Liquefy only processes JSONL rows; flat array goes through zstd directly)")

    # Summary table
    print("\n\n" + "="*80)
    print(f"  {'WORKLOAD':<45} {'Liquefy':>8} {'zstd-3':>8} {'zstd-22':>9} {'vs zstd-3':>10}")
    print("="*80)
    for r in results:
        print(f"  {r['workload'][:45]:<45} {r['ratio_liquefy']:>7.0f}x {r['ratio_zstd3']:>7.0f}x {r['ratio_zstd22']:>8.0f}x {r['liquefy_vs_zstd3']:>9.1f}x")
    print("="*80)

if __name__ == "__main__":
    main()
