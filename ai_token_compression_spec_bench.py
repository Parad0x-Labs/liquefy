#!/usr/bin/env python3
"""
AI Token Compression — Liquefy Feature Spec Benchmark
======================================================
Spec: "AI Token Compression" as a new Liquefy column type.

Test data matches the exact user spec:
  - 1000 structured JSON LLM responses
  - Token IDs for JSON keys: drawn from 0-1000 range (low IDs = common tokens)
  - Token IDs for values:    drawn from 0-100k range
  - Ragged sequences (different lengths per row, 8-64 tokens)
  - Also tests fixed-width 16-token sequences for direct comparison

Four encoding strategies:
  a. raw int32 array -> zstd
  b. delta-encoded int32 -> zstd
  c. Liquefy columnar (transposed: column[i] = position-i across all rows)
  d. NDJSON row-per-sequence -> zstd baseline

Search capability:
  - Find all rows where token at position 3 == target (without full decompress)
  - Measure: bytes decompressed vs total archive size

Realistic models:
  1. "structured_json": JSON key tokens highly repetitive (0-1000), value tokens varied (0-100k)
  2. "chain_of_thought": Longer sequences, moderately repetitive
  3. "free_text":        Fully random 0-100k (worst case)
"""

import sys, os, json, time, random, struct
import numpy as np
import zstandard as zstd

LIQUEFY_DIR = r"F:\Enterprise  tests\liquefy"
CODEC_DIR   = os.path.join(LIQUEFY_DIR, "engines", "json_codec")
sys.path.insert(0, CODEC_DIR)
sys.path.insert(0, LIQUEFY_DIR)

from NULL_Json_Columnar_Gun_v1 import NULL_Json_Columnar_Gun_v1

random.seed(0xDEADBEEF)
np.random.seed(0xDEADBEEF)

cctx = zstd.ZstdCompressor(level=6)
dctx = zstd.ZstdDecompressor()

VOCAB_SIZE = 100_256   # tiktoken cl100k_base
N_ROWS     = 1_000

# ─── DATA GENERATORS ─────────────────────────────────────────────────────────

# Simulate common JSON-key tokens: "timestamp", "level", "message", "agent_id" etc.
# In tiktoken cl100k, short common English words cluster below ~5000.
# JSON structural tokens like `{`, `}`, `"`, `:` are often < 500.
JSON_KEY_TOKENS   = list(range(1, 800))        # 0-1000 as specified
JSON_VALUE_TOKENS = list(range(0, 100_000))    # 0-100k as specified

def gen_structured_json_fixed(n_rows, width=16):
    """
    Fixed-width token sequences simulating structured JSON LLM output.
    Positions 0,2,4 = JSON structural/key tokens (0-1000, highly repetitive)
    Positions 1,3,5+ = value tokens (0-100k, more varied)
    """
    # A few 'schema' key tokens that repeat across every row
    schema_keys = [random.randint(0, 999) for _ in range(6)]

    rows = []
    for _ in range(n_rows):
        row = []
        for pos in range(width):
            if pos % 2 == 0:
                # key/structural position: 85% schema token, 15% random low token
                if random.random() < 0.85:
                    row.append(schema_keys[pos % len(schema_keys)])
                else:
                    row.append(random.randint(0, 999))
            else:
                # value position: 20% common value tokens, 80% full vocab
                if random.random() < 0.20:
                    row.append(random.randint(0, 4999))
                else:
                    row.append(random.randint(0, 99_999))
        rows.append(row)
    return rows

def gen_structured_json_ragged(n_rows, min_len=8, max_len=64):
    """
    Ragged token sequences (different lengths per row) — realistic LLM output.
    Same token distribution as fixed, but varying length.
    """
    schema_keys = [random.randint(0, 999) for _ in range(8)]
    rows = []
    lengths = []
    for _ in range(n_rows):
        width = random.randint(min_len, max_len)
        lengths.append(width)
        row = []
        for pos in range(width):
            if pos % 2 == 0:
                if random.random() < 0.85:
                    row.append(schema_keys[pos % len(schema_keys)])
                else:
                    row.append(random.randint(0, 999))
            else:
                if random.random() < 0.20:
                    row.append(random.randint(0, 4999))
                else:
                    row.append(random.randint(0, 99_999))
        rows.append(row)
    return rows, lengths

def gen_chain_of_thought(n_rows, width=32):
    """
    Chain-of-thought traces: moderate repetition, wider sequences.
    Certain reasoning tokens repeat (e.g. "because", "therefore", "so").
    """
    cot_tokens = [random.randint(100, 3000) for _ in range(20)]  # reasoning vocab
    rows = []
    for _ in range(n_rows):
        row = []
        for pos in range(width):
            if pos < 3:
                # prefix tokens almost always the same
                row.append(cot_tokens[pos % 3])
            elif random.random() < 0.35:
                row.append(random.choice(cot_tokens))
            else:
                row.append(random.randint(0, 50_000))
        rows.append(row)
    return rows

def gen_free_text(n_rows, width=16):
    """Fully random tokens 0-100k (worst case for compression)."""
    rows = []
    for _ in range(n_rows):
        rows.append([random.randint(0, VOCAB_SIZE - 1) for _ in range(width)])
    return rows

# ─── ENCODING ────────────────────────────────────────────────────────────────

def encode_raw_int32(rows):
    """Flatten all rows to int32 bytes (natural order)."""
    flat = [t for row in rows for t in row]
    return np.array(flat, dtype=np.int32).tobytes()

def encode_raw_with_lengths(rows):
    """Ragged-aware: prefix each row with uint16 length, then int32 tokens."""
    buf = bytearray()
    for row in rows:
        buf += struct.pack('<H', len(row))
        buf += np.array(row, dtype=np.int32).tobytes()
    return bytes(buf)

def encode_delta_int32(rows):
    """Delta-encode across entire flattened sequence."""
    flat = [t for row in rows for t in row]
    arr = np.array(flat, dtype=np.int64)
    delta = np.empty_like(arr)
    delta[0] = arr[0]
    delta[1:] = np.diff(arr)
    return delta.astype(np.int32).tobytes()

def encode_ndjson(rows, pad_width=None):
    """
    NDJSON: one JSON object per row, keys t0..tN.
    If pad_width given, pad shorter rows with -1 (null sentinel).
    """
    lines = []
    for row in rows:
        w = pad_width if pad_width else len(row)
        record = {}
        for i in range(w):
            record[f"t{i}"] = int(row[i]) if i < len(row) else -1
        lines.append(json.dumps(record, separators=(',', ':')).encode())
    return b'\n'.join(lines) + b'\n'

def encode_columnar_transposed(rows, pad_width):
    """
    Manual columnar transposition: for each position k, emit all row[k] values.
    Store as NDJSON so Liquefy can ingest it.
    """
    # This IS what Liquefy does internally — the NDJSON columnar encoding.
    # We show it explicitly for clarity.
    return encode_ndjson(rows, pad_width=pad_width)

# ─── BENCHMARK ───────────────────────────────────────────────────────────────

def bench(name, data_bytes, compress_fn, decompress_fn, repeat=5):
    orig = len(data_bytes)
    comp = compress_fn(data_bytes)
    comp_size = len(comp)
    _ = decompress_fn(comp)

    t0 = time.perf_counter()
    for _ in range(repeat):
        comp = compress_fn(data_bytes)
    cmp_ms = (time.perf_counter() - t0) / repeat * 1000

    t0 = time.perf_counter()
    for _ in range(repeat):
        decompress_fn(comp)
    dcp_ms = (time.perf_counter() - t0) / repeat * 1000

    ratio = orig / comp_size if comp_size else 0
    cmp_mbs = (orig / 1048576) / (cmp_ms / 1000) if cmp_ms else 0
    dcp_mbs = (orig / 1048576) / (dcp_ms / 1000) if dcp_ms else 0

    return {
        "name": name,
        "orig_kb": round(orig / 1024, 1),
        "comp_kb": round(comp_size / 1024, 1),
        "ratio": round(ratio, 2),
        "cmp_ms": round(cmp_ms, 2),
        "dcp_ms": round(dcp_ms, 2),
        "cmp_mbs": round(cmp_mbs, 1),
        "dcp_mbs": round(dcp_mbs, 1),
    }

# ─── COLUMN GREP ─────────────────────────────────────────────────────────────

def grep_single_column(compressed_blob, target_token, position):
    """
    Decompress ONLY column t{position} from a Liquefy COL2 archive.
    Return (matching_row_indices, elapsed_ms, bytes_decompressed, archive_bytes).
    """
    from NULL_Json_Columnar_Gun_v1 import unpack_delta_ints, unpack_varint_buf

    blob = compressed_blob
    archive_bytes = len(blob)

    if blob[:4] != b'COL2':
        return [], 0, 0, archive_bytes

    ptr = 4
    row_count = struct.unpack('<I', blob[ptr:ptr+4])[0]; ptr += 4
    num_cols  = struct.unpack('<H', blob[ptr:ptr+2])[0]; ptr += 2
    ptr += 1  # trailing_newline flag
    order_len = struct.unpack('<I', blob[ptr:ptr+4])[0]; ptr += 4
    ptr += order_len
    p_len = struct.unpack('<I', blob[ptr:ptr+4])[0]; ptr += 4
    ptr += p_len

    target_col = f"t{position}".encode()
    bytes_decomp = 0

    t0 = time.perf_counter()
    matches = []

    for _ in range(num_cols):
        name_len, ptr = unpack_varint_buf(blob, ptr)
        col_name = blob[ptr:ptr+name_len]; ptr += name_len
        payload_len = struct.unpack('<I', blob[ptr:ptr+4])[0]; ptr += 4

        if col_name != target_col:
            ptr += payload_len
            continue

        chunk = blob[ptr:ptr+payload_len]
        bytes_decomp += payload_len
        payload = zstd.ZstdDecompressor().decompress(chunk)
        mode = payload[0]

        if mode == 0x05:  # integer delta column
            try:
                mask = payload[1:1+row_count]
                present = sum(mask)
                vals = unpack_delta_ints(payload[1+row_count:], present)
                it = iter(vals)
                for i, m in enumerate(mask):
                    if m:
                        v = next(it)
                        if v == target_token:
                            matches.append(i)
            except Exception as e:
                print(f"    [warn] grep decode error: {e}")
        break

    elapsed_ms = (time.perf_counter() - t0) * 1000
    return matches, elapsed_ms, bytes_decomp, archive_bytes

# ─── DATASET RUNNER ──────────────────────────────────────────────────────────

def run_dataset(label, rows, pad_width=None):
    if pad_width is None:
        pad_width = max(len(r) for r in rows)

    gun = NULL_Json_Columnar_Gun_v1(level=6, fast=True)

    raw32         = encode_raw_int32(rows)
    delta32       = encode_delta_int32(rows)
    ndjson        = encode_ndjson(rows, pad_width=pad_width)

    results = []

    results.append(bench(
        "a. raw int32 -> zstd",
        raw32, cctx.compress, dctx.decompress
    ))
    results.append(bench(
        "b. delta int32 -> zstd",
        delta32, cctx.compress, dctx.decompress
    ))
    results.append(bench(
        "c. Liquefy columnar",
        ndjson,
        lambda d: gun.compress(d),
        lambda d: gun.decompress(d),
    ))
    results.append(bench(
        "d. NDJSON -> zstd (baseline)",
        ndjson, cctx.compress, dctx.decompress
    ))

    # ─── GREP TEST ───────────────────────────────────────────────────────────
    TARGET_TOKEN = 42
    TARGET_POS   = 2
    PLANT_ROWS   = list(range(200, 250))

    rows_g = [list(r) for r in rows]
    for i in PLANT_ROWS:
        if len(rows_g[i]) > TARGET_POS:
            rows_g[i][TARGET_POS] = TARGET_TOKEN

    gt = set(i for i, r in enumerate(rows_g) if len(r) > TARGET_POS and r[TARGET_POS] == TARGET_TOKEN)
    ndjson_g = encode_ndjson(rows_g, pad_width=pad_width)
    compressed_g = gun.compress(ndjson_g)

    matches, grep_ms, bytes_decomp, archive_bytes = grep_single_column(
        compressed_g, TARGET_TOKEN, TARGET_POS
    )
    found = set(matches)
    tp = len(found & gt)
    fp = len(found - gt)
    fn = len(gt - found)
    pct = bytes_decomp / archive_bytes * 100 if archive_bytes else 0

    grep_stats = {
        "ground_truth":    len(gt),
        "found":           len(found),
        "tp": tp, "fp": fp, "fn": fn,
        "exact": fp == 0 and fn == 0,
        "grep_ms":         round(grep_ms, 2),
        "bytes_decomp":    bytes_decomp,
        "archive_bytes":   archive_bytes,
        "pct_decoded":     round(pct, 2),
    }

    return results, grep_stats

# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 78)
    print("  AI TOKEN COMPRESSION — LIQUEFY FEATURE BENCHMARK")
    print(f"  N={N_ROWS} rows  |  Vocab 0-{VOCAB_SIZE}  |  zstd L6 + Liquefy COL2")
    print("=" * 78)

    datasets = {}

    # 1. Structured JSON fixed-width 16
    label = "structured_json (16 tok)"
    rows = gen_structured_json_fixed(N_ROWS, width=16)
    print(f"\n[1] {label}")
    res, grep = run_dataset(label, rows, pad_width=16)
    datasets[label] = {"compression": res, "grep": grep}
    for r in res:
        print(f"  {r['name']:<30}  orig={r['orig_kb']:>7.1f}KB  comp={r['comp_kb']:>7.1f}KB  ratio={r['ratio']:>6.2f}x  cmp={r['cmp_ms']:>6.1f}ms  dcp={r['dcp_ms']:>6.1f}ms")
    g = grep
    print(f"  GREP col[{2}]=42: GT={g['ground_truth']} found={g['found']} TP={g['tp']} FP={g['fp']} FN={g['fn']} exact={g['exact']} {g['grep_ms']}ms  decoded={g['pct_decoded']:.1f}% of archive")

    # 2. Structured JSON ragged (8-64 tokens)
    label = "structured_json (ragged)"
    rows_rag, lengths = gen_structured_json_ragged(N_ROWS, min_len=8, max_len=64)
    avg_len = sum(lengths) / len(lengths)
    pad_w   = max(lengths)
    print(f"\n[2] {label}  avg_len={avg_len:.1f}  max={pad_w}")
    res, grep = run_dataset(label, rows_rag, pad_width=pad_w)
    datasets[label] = {"compression": res, "grep": grep, "avg_len": avg_len, "pad_width": pad_w}
    for r in res:
        print(f"  {r['name']:<30}  orig={r['orig_kb']:>7.1f}KB  comp={r['comp_kb']:>7.1f}KB  ratio={r['ratio']:>6.2f}x  cmp={r['cmp_ms']:>6.1f}ms  dcp={r['dcp_ms']:>6.1f}ms")
    g = grep
    print(f"  GREP col[{2}]=42: GT={g['ground_truth']} found={g['found']} TP={g['tp']} FP={g['fp']} FN={g['fn']} exact={g['exact']} {g['grep_ms']}ms  decoded={g['pct_decoded']:.1f}% of archive")

    # 3. Chain-of-thought (width=32)
    label = "chain_of_thought (32 tok)"
    rows = gen_chain_of_thought(N_ROWS, width=32)
    print(f"\n[3] {label}")
    res, grep = run_dataset(label, rows, pad_width=32)
    datasets[label] = {"compression": res, "grep": grep}
    for r in res:
        print(f"  {r['name']:<30}  orig={r['orig_kb']:>7.1f}KB  comp={r['comp_kb']:>7.1f}KB  ratio={r['ratio']:>6.2f}x  cmp={r['cmp_ms']:>6.1f}ms  dcp={r['dcp_ms']:>6.1f}ms")
    g = grep
    print(f"  GREP col[{2}]=42: GT={g['ground_truth']} found={g['found']} TP={g['tp']} FP={g['fp']} FN={g['fn']} exact={g['exact']} {g['grep_ms']}ms  decoded={g['pct_decoded']:.1f}% of archive")

    # 4. Free text worst case
    label = "free_text (16 tok, random)"
    rows = gen_free_text(N_ROWS, width=16)
    print(f"\n[4] {label}")
    res, grep = run_dataset(label, rows, pad_width=16)
    datasets[label] = {"compression": res, "grep": grep}
    for r in res:
        print(f"  {r['name']:<30}  orig={r['orig_kb']:>7.1f}KB  comp={r['comp_kb']:>7.1f}KB  ratio={r['ratio']:>6.2f}x  cmp={r['cmp_ms']:>6.1f}ms  dcp={r['dcp_ms']:>6.1f}ms")
    g = grep
    print(f"  GREP col[{2}]=42: GT={g['ground_truth']} found={g['found']} TP={g['tp']} FP={g['fp']} FN={g['fn']} exact={g['exact']} {g['grep_ms']}ms  decoded={g['pct_decoded']:.1f}% of archive")

    # ─── SUMMARY ─────────────────────────────────────────────────────────────
    print(f"\n{'='*78}")
    print("  COMPRESSION RATIO SUMMARY  (higher = better)")
    print(f"{'='*78}")
    hdr = f"  {'Dataset':<26}  {'a.raw':>8}  {'b.delta':>8}  {'c.Liquefy':>10}  {'d.NDJSON':>9}  Liquefy/raw"
    print(hdr)
    print("  " + "-" * 74)
    for label, data in datasets.items():
        r = [x["ratio"] for x in data["compression"]]
        uplift = r[2] / r[0] if r[0] else 0
        print(f"  {label:<26}  {r[0]:>8.2f}x  {r[1]:>8.2f}x  {r[2]:>10.2f}x  {r[3]:>9.2f}x  {uplift:>9.2f}x")

    print(f"\n{'='*78}")
    print("  SEARCH CAPABILITY (single-column grep, no full decompress)")
    print(f"{'='*78}")
    print(f"  {'Dataset':<26}  {'GT':>5}  {'Found':>6}  {'Exact':>6}  {'ms':>7}  {'%decoded':>9}")
    print("  " + "-" * 65)
    for label, data in datasets.items():
        g = data["grep"]
        print(f"  {label:<26}  {g['ground_truth']:>5}  {g['found']:>6}  {str(g['exact']):>6}  {g['grep_ms']:>7.2f}  {g['pct_decoded']:>9.2f}%")

    # ─── TOKEN COLUMN TYPE SPEC NUMBERS ──────────────────────────────────────
    print(f"\n{'='*78}")
    print("  SPEC IMPLICATIONS — Token Column Type")
    print(f"{'='*78}")
    sj = datasets["structured_json (16 tok)"]["compression"]
    cot = datasets["chain_of_thought (32 tok)"]["compression"]
    ft = datasets["free_text (16 tok, random)"]["compression"]
    rag = datasets["structured_json (ragged)"]["compression"]

    print(f"  Structured JSON 16-tok:   raw->zstd={sj[0]['ratio']:.2f}x  Liquefy={sj[2]['ratio']:.2f}x  uplift={sj[2]['ratio']/sj[0]['ratio']:.2f}x")
    print(f"  Structured JSON ragged:   raw->zstd={rag[0]['ratio']:.2f}x  Liquefy={rag[2]['ratio']:.2f}x  uplift={rag[2]['ratio']/rag[0]['ratio']:.2f}x")
    print(f"  Chain-of-thought 32-tok:  raw->zstd={cot[0]['ratio']:.2f}x  Liquefy={cot[2]['ratio']:.2f}x  uplift={cot[2]['ratio']/cot[0]['ratio']:.2f}x")
    print(f"  Free text 16-tok:         raw->zstd={ft[0]['ratio']:.2f}x  Liquefy={ft[2]['ratio']:.2f}x  uplift={ft[2]['ratio']/ft[0]['ratio']:.2f}x")

    print(f"\n  NOTE: Liquefy input is NDJSON (~2.5-4x larger than raw int32),")
    print(f"  so the ratio is computed relative to NDJSON input size.")
    print(f"  For apples-to-apples vs raw int32 input, the effective ratio is:")
    for label, data in datasets.items():
        r = data["compression"]
        # c. Liquefy operates on NDJSON which is ~r[3]['orig_kb'] / r[0]['orig_kb'] * raw_size
        # but we want: how much space vs raw int32?
        raw_kb = r[0]["orig_kb"]
        liq_kb = r[2]["comp_kb"]
        eff = raw_kb / liq_kb if liq_kb else 0
        print(f"    {label:<26}  raw_int32={raw_kb:.0f}KB  liquefy_out={liq_kb:.0f}KB  eff_ratio={eff:.2f}x vs raw int32")

    out = os.path.join(LIQUEFY_DIR, "ai_token_compression_results.json")
    with open(out, "w") as f:
        json.dump(datasets, f, indent=2)
    print(f"\nFull results -> {out}")

if __name__ == "__main__":
    main()
