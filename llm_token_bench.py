#!/usr/bin/env python3
"""
LLM Token Sequence Compression Benchmark
=========================================
Tests 4 compression strategies on realistic LLM output token sequences:
  a. Raw int32 -> zstd
  b. Delta int32 -> zstd
  c. Columnar by semantic position (col_k = token[k] of each line) -> Liquefy JSON columnar
  d. Liquefy JSON columnar treating each row as {"t0":tok0, "t1":tok1, ...}

Also tests: grep for a specific token ID at a specific position (column) without full decompress.

Sequences generated using tiktoken cl100k_base vocab (0-100256).
"""

import sys
import os
import struct
import time
import random
import json

import numpy as np
import zstandard as zstd

# Add liquefy engine to path
LIQUEFY_DIR = r"F:\Enterprise  tests\liquefy"
CODEC_DIR   = os.path.join(LIQUEFY_DIR, "engines", "json_codec")
sys.path.insert(0, CODEC_DIR)
sys.path.insert(0, LIQUEFY_DIR)

from NULL_Json_Columnar_Gun_v1 import NULL_Json_Columnar_Gun_v1

# ─── PARAMETERS ─────────────────────────────────────────────────────────────
N_ROWS      = 10_000   # number of "lines" (each line = one token sequence / row)
ROW_WIDTH   = 16       # tokens per line
VOCAB_SIZE  = 100_256  # tiktoken cl100k_base range

# Realistic token pools (simulate common patterns)
COMMON_TOKENS_JSON  = [257, 1, 284, 25, 198, 366, 2, 3, 4, 13, 91, 220, 50256, 338, 523]
COMMON_TOKENS_CODE  = [4299, 220, 25, 198, 1330, 422, 50256, 357, 46256, 2488, 4738, 2163, 28231, 9516, 8162]
KEYWORDS_CODE       = [4738, 4299, 1330, 2163, 611, 2073, 329, 981, 1441, 3601, 2488, 1303, 6407, 10352, 6045]

random.seed(42)
np.random.seed(42)

cctx = zstd.ZstdCompressor(level=6)
dctx = zstd.ZstdDecompressor()

# ─── DATA GENERATORS ─────────────────────────────────────────────────────────

def gen_json_output(n_rows, row_width):
    """Structured JSON output: tokens cluster around common values."""
    rows = []
    # Keys like "ts", "level", "msg" map to short token clusters
    key_clusters = [
        list(range(1, 50)),           # ts-like: small tokens
        [1, 2, 3, 4, 5, 6],           # level: very few options
        COMMON_TOKENS_JSON[:8],       # msg start: common structural tokens
    ]
    for _ in range(n_rows):
        row = []
        for pos in range(row_width):
            cluster = key_clusters[pos % len(key_clusters)]
            if random.random() < 0.75:
                row.append(random.choice(cluster))
            else:
                row.append(random.randint(0, 5000))  # occasional rare token
        rows.append(row)
    return rows

def gen_freetext_output(n_rows, row_width):
    """Free text output: more random token distribution."""
    rows = []
    for _ in range(n_rows):
        row = [random.randint(0, VOCAB_SIZE - 1) for _ in range(row_width)]
        rows.append(row)
    return rows

def gen_code_output(n_rows, row_width):
    """Code output: keywords repeat heavily."""
    rows = []
    for _ in range(n_rows):
        row = []
        for pos in range(row_width):
            if pos == 0:
                row.append(random.choice(KEYWORDS_CODE))
            elif pos < 4:
                # indent/syntax tokens — very repetitive
                row.append(random.choice([220, 220, 220, 198, 25, 357, 46256, 4738]))
            else:
                if random.random() < 0.60:
                    row.append(random.choice(COMMON_TOKENS_CODE))
                else:
                    row.append(random.randint(0, 20000))
        rows.append(row)
    return rows

# ─── ENCODING HELPERS ─────────────────────────────────────────────────────────

def rows_to_raw_int32(rows):
    """Flatten all rows into a single int32 array (natural order)."""
    flat = []
    for row in rows:
        flat.extend(row)
    return np.array(flat, dtype=np.int32).tobytes()

def rows_to_delta_int32(rows):
    """Delta encode across the entire flattened sequence, store as int32."""
    flat = []
    for row in rows:
        flat.extend(row)
    arr = np.array(flat, dtype=np.int64)
    delta = np.empty_like(arr)
    delta[0] = arr[0]
    delta[1:] = np.diff(arr)
    # clamp to int32 range (deltas in vocab-range should fit)
    return delta.astype(np.int32).tobytes()

def rows_to_columnar_ndjson(rows, row_width):
    """Convert rows to NDJSON where each record is {t0:v, t1:v, ..., tN:v}."""
    lines = []
    for row in rows:
        record = {f"t{i}": int(row[i]) for i in range(min(row_width, len(row)))}
        lines.append(json.dumps(record, separators=(',', ':')).encode())
    return b'\n'.join(lines) + b'\n'

# ─── BENCHMARK CORE ──────────────────────────────────────────────────────────

def bench_compress(name, data_bytes, compress_fn, decompress_fn, repeat=3):
    """Run compress + decompress, return dict with ratio and speeds."""
    orig_size = len(data_bytes)

    # Warmup
    compressed = compress_fn(data_bytes)
    comp_size = len(compressed)
    _ = decompress_fn(compressed)

    # Timed compress
    t0 = time.perf_counter()
    for _ in range(repeat):
        compressed = compress_fn(data_bytes)
    compress_ms = (time.perf_counter() - t0) / repeat * 1000

    # Timed decompress
    t0 = time.perf_counter()
    for _ in range(repeat):
        decompressed = decompress_fn(compressed)
    decompress_ms = (time.perf_counter() - t0) / repeat * 1000

    ratio = orig_size / comp_size if comp_size > 0 else 0

    compress_mb_s   = (orig_size / 1024 / 1024) / (compress_ms / 1000) if compress_ms > 0 else 0
    decompress_mb_s = (orig_size / 1024 / 1024) / (decompress_ms / 1000) if decompress_ms > 0 else 0

    return {
        "name":          name,
        "orig_kb":       round(orig_size / 1024, 1),
        "comp_kb":       round(comp_size / 1024, 1),
        "ratio":         round(ratio, 2),
        "compress_ms":   round(compress_ms, 2),
        "decompress_ms": round(decompress_ms, 2),
        "compress_MB/s":   round(compress_mb_s, 1),
        "decompress_MB/s": round(decompress_mb_s, 1),
    }

# ─── GREP BENCHMARK ──────────────────────────────────────────────────────────

def grep_col_direct(gun, compressed_blob, target_token_id, position):
    """
    Direct column-aware grep: decompress ONLY the target column's payload,
    then scan it. This is the proper 'grep without full decompress' path.

    Liquefy COL2 format: iterate column blobs by name, stop when we find t{position}.
    Returns (matching_rows, elapsed_ms, bytes_read).
    """
    import struct as _struct

    blob = compressed_blob
    if not blob[:4] == b'COL2':
        return [], 0, 0

    ptr = 4
    row_count = _struct.unpack('<I', blob[ptr:ptr+4])[0]; ptr += 4
    num_cols  = _struct.unpack('<H', blob[ptr:ptr+2])[0]; ptr += 2
    ptr += 1  # trailing newline flag
    order_len = _struct.unpack('<I', blob[ptr:ptr+4])[0]; ptr += 4
    ptr += order_len
    p_len = _struct.unpack('<I', blob[ptr:ptr+4])[0]; ptr += 4
    ptr += p_len

    target_col_name = f"t{position}".encode()

    from NULL_Json_Columnar_Gun_v1 import unpack_delta_ints, unpack_varint_buf

    t0 = time.perf_counter()
    bytes_read = 0

    for _ in range(num_cols):
        name_len, ptr = unpack_varint_buf(blob, ptr)
        col_name = blob[ptr:ptr+name_len]; ptr += name_len
        payload_len = _struct.unpack('<I', blob[ptr:ptr+4])[0]; ptr += 4

        if col_name != target_col_name:
            ptr += payload_len  # skip: read header bytes only, not payload
            continue

        # Found target column — decompress only this chunk
        import zstandard as _zstd
        chunk = blob[ptr:ptr+payload_len]
        bytes_read += payload_len
        payload = _zstd.ZstdDecompressor().decompress(chunk)
        mode = payload[0]

        matches = []
        if mode == 0x05:  # integer delta column
            try:
                target = target_token_id
                mask = payload[1:1+row_count]
                present = sum(mask)
                vals = unpack_delta_ints(payload[1+row_count:], present)
                it = iter(vals)
                for i, m in enumerate(mask):
                    if m:
                        v = next(it)
                        if v == target:
                            matches.append(i)
            except Exception:
                pass
        break  # found our column, done

    elapsed_ms = (time.perf_counter() - t0) * 1000
    return matches, elapsed_ms, bytes_read


def grep_in_columnar(gun, compressed_blob, target_token_id, position, rows_with_match):
    """
    Test: find all rows where token at `position` == target_token_id
    WITHOUT decompressing the whole archive.

    In Liquefy columnar format, column "t{position}" holds exactly the token
    at that position for every row. We grep for the integer value.
    """
    query_str = str(target_token_id)
    t0 = time.perf_counter()
    result = gun.grep(compressed_blob, query_str)
    elapsed_ms = (time.perf_counter() - t0) * 1000

    found = set(result.get("matches", []))
    # Compute precision/recall relative to ground truth
    gt = set(rows_with_match)
    tp = len(found & gt)
    fp = len(found - gt)
    fn = len(gt - found)

    return {
        "target_token":   target_token_id,
        "position":       position,
        "ground_truth":   len(gt),
        "found":          len(found),
        "true_positive":  tp,
        "false_positive": fp,
        "false_negative": fn,
        "exact_match":    (fp == 0 and fn == 0),
        "grep_ms":        round(elapsed_ms, 2),
        "stats":          result.get("stats", {}),
    }

# ─── MAIN ────────────────────────────────────────────────────────────────────

def run_dataset(label, rows):
    print(f"\n{'='*70}")
    print(f"  DATASET: {label}  ({len(rows)} rows x {ROW_WIDTH} tokens)")
    print(f"{'='*70}")

    gun = NULL_Json_Columnar_Gun_v1(level=6, fast=True)

    # Build inputs
    raw_int32   = rows_to_raw_int32(rows)
    delta_int32 = rows_to_delta_int32(rows)
    ndjson      = rows_to_columnar_ndjson(rows, ROW_WIDTH)

    results = []

    # (a) Raw int32 -> zstd
    r = bench_compress(
        "a. raw-int32 -> zstd",
        raw_int32,
        lambda d: cctx.compress(d),
        lambda d: dctx.decompress(d),
    )
    results.append(r)

    # (b) Delta int32 -> zstd
    r = bench_compress(
        "b. delta-int32 -> zstd",
        delta_int32,
        lambda d: cctx.compress(d),
        lambda d: dctx.decompress(d),
    )
    results.append(r)

    # (c) Columnar by semantic position -> Liquefy JSON columnar
    # Each "row" in the NDJSON is {t0:.., t1:.., ..} — Liquefy column t{k}
    # contains all token-at-position-k values across rows = same as "semantic position" split.
    r = bench_compress(
        "c. columnar-pos -> Liquefy",
        ndjson,
        lambda d: gun.compress(d),
        lambda d: gun.decompress(d),
    )
    results.append(r)

    # (d) Same as (c) but labeled explicitly as "JSON columnar row per token-sequence"
    # This IS (c) — Liquefy takes the NDJSON and stores each key as a column.
    # For clarity we also test with raw NDJSON -> zstd as baseline.
    r = bench_compress(
        "d. NDJSON row -> zstd (baseline)",
        ndjson,
        lambda d: cctx.compress(d),
        lambda d: dctx.decompress(d),
    )
    results.append(r)

    print(f"\n{'Method':<30} {'Orig KB':>8} {'Comp KB':>8} {'Ratio':>7} {'Cmp ms':>8} {'Dcp ms':>8} {'Cmp MB/s':>10} {'Dcp MB/s':>10}")
    print("-" * 95)
    for r in results:
        print(f"{r['name']:<30} {r['orig_kb']:>8} {r['comp_kb']:>8} {r['ratio']:>7.2f}x {r['compress_ms']:>8.1f} {r['decompress_ms']:>8.1f} {r['compress_MB/s']:>10.1f} {r['decompress_MB/s']:>10.1f}")

    # ─── GREP TEST ───────────────────────────────────────────────────────────
    print(f"\n  GREP TEST: find rows where token at position 3 == 1234")
    print(f"  (WITHOUT decompressing the whole archive)")

    TARGET_TOKEN = 1234
    TARGET_POS   = 3

    # Plant TARGET_TOKEN at TARGET_POS in 50 known rows so we have ground truth
    PLANTED_ROWS = list(range(100, 150))  # rows 100-149
    rows_mod = [list(r) for r in rows]
    for i in PLANTED_ROWS:
        rows_mod[i][TARGET_POS] = TARGET_TOKEN

    # Ground truth: which rows have token 1234 at position 3?
    gt_rows = [i for i, row in enumerate(rows_mod) if len(row) > TARGET_POS and row[TARGET_POS] == TARGET_TOKEN]

    # Rebuild NDJSON with planted rows and compress
    ndjson_mod = rows_to_columnar_ndjson(rows_mod, ROW_WIDTH)
    compressed_blob = gun.compress(ndjson_mod)
    grep_result = grep_in_columnar(gun, compressed_blob, TARGET_TOKEN, TARGET_POS, gt_rows)

    # Also: correctness check — the grep queries column "t3" which is the integer column
    # for position 3. Liquefy grep searches ALL columns for the value, so it may find
    # rows where other columns also contain 1234. Record what grep actually does.
    all_rows_with_1234_anywhere = set(
        i for i, row in enumerate(rows_mod) if TARGET_TOKEN in row
    )
    rows_with_1234_at_pos3_only = set(gt_rows)
    cross_col_matches = all_rows_with_1234_anywhere - rows_with_1234_at_pos3_only
    print(f"  [Note] rows with 1234 anywhere in row: {len(all_rows_with_1234_anywhere)}")
    print(f"  [Note] rows with 1234 ONLY at pos 3:   {len(rows_with_1234_at_pos3_only)}")
    print(f"  [Note] rows with 1234 in OTHER cols:   {len(cross_col_matches)} (expect FP in full-scan grep)")

    print(f"  Target token={TARGET_TOKEN} at position t{TARGET_POS}")
    print(f"  Ground truth rows: {grep_result['ground_truth']}")
    print(f"  Liquefy grep found: {grep_result['found']}")
    print(f"  True positives: {grep_result['true_positive']}  False pos: {grep_result['false_positive']}  False neg: {grep_result['false_negative']}")
    print(f"  Exact match: {grep_result['exact_match']}")
    print(f"  Grep time: {grep_result['grep_ms']} ms")
    stats = grep_result.get("stats", {})
    if stats:
        tot_bytes   = stats.get("total_archive_bytes", 0)
        dec_bytes   = stats.get("bytes_decoded", 0)
        cand_cols   = stats.get("candidate_cols", 0)
        total_cols  = stats.get("total_cols", 0)
        pct         = (dec_bytes / tot_bytes * 100) if tot_bytes else 0
        print(f"  Archive: {tot_bytes/1024:.1f} KB  |  Decoded: {dec_bytes/1024:.1f} KB ({pct:.1f}% of archive)")
        print(f"  Columns scanned: {cand_cols}/{total_cols}")

    # ─── DIRECT COLUMN GREP (single-column, true skip) ───────────────────────
    print(f"\n  DIRECT COLUMN GREP: decompress ONLY column t{TARGET_POS}")
    direct_matches, direct_ms, direct_bytes = grep_col_direct(
        gun, compressed_blob, TARGET_TOKEN, TARGET_POS
    )
    direct_gt = set(gt_rows)
    direct_found = set(direct_matches)
    d_tp = len(direct_found & direct_gt)
    d_fp = len(direct_found - direct_gt)
    d_fn = len(direct_gt - direct_found)
    total_comp = len(compressed_blob)
    pct_direct = direct_bytes / total_comp * 100 if total_comp else 0
    print(f"  Ground truth: {len(direct_gt)}  Found: {len(direct_found)}")
    print(f"  TP={d_tp} FP={d_fp} FN={d_fn}  Exact={d_fp==0 and d_fn==0}")
    print(f"  Time: {direct_ms:.2f} ms  |  Bytes decompressed: {direct_bytes} ({pct_direct:.1f}% of {total_comp/1024:.1f} KB archive)")

    return results, grep_result


def main():
    print("LLM TOKEN COMPRESSION BENCHMARK")
    print(f"Rows: {N_ROWS}  |  Width: {ROW_WIDTH}  |  Vocab: 0-{VOCAB_SIZE}")
    print("Python / zstd L6 / Liquefy NULL_Json_Columnar_Gun_v1 (fast=True)")

    datasets = [
        ("JSON output (clustered)",  gen_json_output(N_ROWS, ROW_WIDTH)),
        ("Free text (random)",       gen_freetext_output(N_ROWS, ROW_WIDTH)),
        ("Code output (repetitive)", gen_code_output(N_ROWS, ROW_WIDTH)),
    ]

    all_results = {}
    for label, rows in datasets:
        res, grep_r = run_dataset(label, rows)
        all_results[label] = {"compression": res, "grep": grep_r}

    # ─── SUMMARY TABLE ───────────────────────────────────────────────────────
    print(f"\n\n{'='*70}")
    print("  SUMMARY — Compression Ratios by Dataset")
    print(f"{'='*70}")
    header = f"{'Dataset':<28} {'a. raw->zstd':>13} {'b. delta->zstd':>15} {'c. Liquefy-col':>15} {'d. NDJSON->zstd':>16}"
    print(header)
    print("-" * 90)
    for label, data in all_results.items():
        ratios = [r["ratio"] for r in data["compression"]]
        print(f"{label:<28} {ratios[0]:>13.2f}x {ratios[1]:>15.2f}x {ratios[2]:>15.2f}x {ratios[3]:>16.2f}x")

    print(f"\n{'='*70}")
    print("  GREP RESULTS (columnar search without full decompress)")
    print(f"{'='*70}")
    print(f"{'Dataset':<28} {'GT rows':>8} {'Found':>7} {'Exact?':>8} {'ms':>8} {'%decoded':>10}")
    print("-" * 75)
    for label, data in all_results.items():
        g = data["grep"]
        stats = g.get("stats", {})
        tot = stats.get("total_archive_bytes", 1)
        dec = stats.get("bytes_decoded", 0)
        pct = dec / tot * 100 if tot else 0
        print(f"{label:<28} {g['ground_truth']:>8} {g['found']:>7} {str(g['exact_match']):>8} {g['grep_ms']:>8.1f} {pct:>10.1f}%")

    # Save JSON results
    out_path = os.path.join(LIQUEFY_DIR, "llm_token_bench_results.json")
    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nFull results saved to: {out_path}")


if __name__ == "__main__":
    main()
