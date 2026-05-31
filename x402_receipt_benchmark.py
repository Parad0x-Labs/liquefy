#!/usr/bin/env python3
"""
x402 Receipt Batch Compression Benchmark
=========================================
Tests Liquefy columnar compression vs zstd on 10,000 realistic x402 payment receipts.
Run from: F:\\Enterprise  tests\\liquefy\\
"""

import sys
import os
import time
import random
import string
import json
import struct

# Wire up liquefy from repo root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'engines', 'json_codec'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'engines'))

import zstandard as zstd

from NULL_Json_Columnar_Gun_v1 import NULL_Json_Columnar_Gun_v1

# ─── Constants ────────────────────────────────────────────────────────────────

N_RECEIPTS    = 10_000
N_SENDERS     = 50
RECEIVER      = "https://api.claude.x402.xyz/v1/inference"
PROGRAM_ID    = "x4o2RcptAnCHoRPaYmEnTsXXXXXXXXXXXXXXXXXXXX"
MODEL         = "claude-3-5-sonnet-20241022"
BASE_TS       = 1_748_000_000_000   # ms — late May 2026
BASE58_CHARS  = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

# S3 Standard pricing (us-east-1, 2026)
S3_PRICE_PER_GB_MONTH = 0.023

# ─── Helpers ──────────────────────────────────────────────────────────────────

rng = random.Random(42)   # deterministic seed for reproducibility

def rand_base58(length: int) -> str:
    return ''.join(rng.choices(BASE58_CHARS, k=length))

def rand_hex(length: int) -> str:
    return ''.join(rng.choices('0123456789abcdef', k=length))

def generate_receipts(n: int) -> list[dict]:
    """Generate n realistic x402 receipts."""
    senders = [rand_base58(44) for _ in range(N_SENDERS)]
    receipts = []
    for i in range(n):
        amount = round(0.001 + (i % 91) * 0.0001, 6)   # 0.001 – 0.01 USDC, low-cardinality feel
        receipts.append({
            "txSignature":  rand_base58(88),
            "amount":       amount,
            "sender":       senders[i % N_SENDERS],
            "receiver":     RECEIVER,
            "timestamp":    BASE_TS + i * 100,           # 100 ms apart
            "receiptId":    i,
            "programId":    PROGRAM_ID,
            "model":        MODEL,
            "tokens_used":  rng.randint(100, 4096),
            "prompt_hash":  rand_hex(64),
        })
    return receipts

def to_jsonl(receipts: list[dict]) -> bytes:
    return b'\n'.join(json.dumps(r, separators=(',', ':')).encode() for r in receipts)

def stripped(receipts: list[dict]) -> list[dict]:
    """Remove high-entropy fields: txSignature, prompt_hash."""
    return [{k: v for k, v in r.items() if k not in ('txSignature', 'prompt_hash')}
            for r in receipts]

def fmt_bytes(b: int) -> str:
    if b < 1024:         return f"{b} B"
    if b < 1024**2:     return f"{b/1024:.1f} KB"
    return               f"{b/1024**2:.2f} MB"

def ratio(original: int, compressed: int) -> str:
    r = original / compressed if compressed else 0
    return f"{r:.2f}x"

def s3_cost_1m_per_day(compressed_bytes_per_10k: int) -> str:
    """Monthly S3 cost for 1M receipts/day (30 days)."""
    receipts_per_day   = 1_000_000
    scale              = receipts_per_day / N_RECEIPTS
    bytes_per_day      = compressed_bytes_per_10k * scale
    bytes_per_month    = bytes_per_day * 30
    gb_per_month       = bytes_per_month / 1024**3
    cost               = gb_per_month * S3_PRICE_PER_GB_MONTH
    return f"${cost:.2f}/mo  ({gb_per_month:.2f} GB/mo)"

def sep_compress(receipts: list[dict]) -> tuple[int, int]:
    """
    Separated approach:
      - Low-entropy fields  → Liquefy columnar
      - High-entropy fields (txSignature, prompt_hash) → separate zstd L22

    Returns (liquefy_bytes, zstd_bytes).
    """
    low_entropy  = stripped(receipts)
    high_entropy = [{"txSignature": r["txSignature"], "prompt_hash": r["prompt_hash"]}
                    for r in receipts]

    low_jsonl    = to_jsonl(low_entropy)
    high_jsonl   = to_jsonl(high_entropy)

    engine       = NULL_Json_Columnar_Gun_v1(level=22)
    cctx_l22     = zstd.ZstdCompressor(level=22)

    liq_blob     = engine.compress(low_jsonl)
    zstd_blob    = cctx_l22.compress(high_jsonl)
    return len(liq_blob), len(zstd_blob)

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("  x402 Receipt Batch Compression Benchmark")
    print(f"  {N_RECEIPTS:,} receipts  |  {N_SENDERS} agent wallets  |  Liquefy + zstd L22")
    print("=" * 70)

    # 1. Generate receipts
    t0 = time.perf_counter()
    receipts = generate_receipts(N_RECEIPTS)
    gen_ms = (time.perf_counter() - t0) * 1000
    print(f"\n[gen]  Generated {N_RECEIPTS:,} receipts in {gen_ms:.0f} ms")

    # ── Raw sizes ────────────────────────────────────────────────────────
    full_jsonl     = to_jsonl(receipts)
    stripped_jsonl = to_jsonl(stripped(receipts))

    raw_full    = len(full_jsonl)
    raw_strip   = len(stripped_jsonl)

    print(f"\n--- Raw input sizes ---")
    print(f"  Full JSONL:     {fmt_bytes(raw_full)}")
    print(f"  Stripped JSONL: {fmt_bytes(raw_strip)}")

    # Entropy analysis: how many bytes are in high-entropy fields?
    # txSignature ≈ 88 chars, prompt_hash ≈ 64 chars, plus JSON overhead (~18 chars)
    rand_bytes_per_receipt  = 88 + 64   # raw random characters
    total_rand_bytes        = rand_bytes_per_receipt * N_RECEIPTS
    rand_fraction           = total_rand_bytes / raw_full
    print(f"\n--- Entropy analysis ---")
    print(f"  Random bytes (txSig+hash per receipt): {rand_bytes_per_receipt} chars")
    print(f"  Total random payload:  {fmt_bytes(total_rand_bytes)}")
    print(f"  Fraction of raw bytes that are random: {rand_fraction*100:.1f}%")
    print(f"  Structured/compressible fraction:      {(1-rand_fraction)*100:.1f}%")

    engine_l22 = NULL_Json_Columnar_Gun_v1(level=22)
    cctx_l22   = zstd.ZstdCompressor(level=22)

    print("\n" + "=" * 70)
    print("  Approach A -- Full JSONL -> Liquefy columnar (level 22)")
    print("=" * 70)
    t0 = time.perf_counter()
    blob_a = engine_l22.compress(full_jsonl)
    ms_a   = (time.perf_counter() - t0) * 1000
    sz_a   = len(blob_a)
    print(f"  Compressed:      {fmt_bytes(sz_a)}")
    print(f"  Ratio:           {ratio(raw_full, sz_a)} ({raw_full/sz_a:.1f}x)")
    print(f"  Time:            {ms_a:.0f} ms")
    print(f"  S3 1M/day est:   {s3_cost_1m_per_day(sz_a)}")

    print("\n" + "=" * 70)
    print("  Approach B -- Stripped JSONL (no txSig/hash) -> Liquefy columnar")
    print("=" * 70)
    t0 = time.perf_counter()
    blob_b = engine_l22.compress(stripped_jsonl)
    ms_b   = (time.perf_counter() - t0) * 1000
    sz_b   = len(blob_b)
    print(f"  Compressed:      {fmt_bytes(sz_b)}")
    print(f"  Ratio:           {ratio(raw_strip, sz_b)} (vs stripped raw)")
    print(f"  Ratio vs full:   {ratio(raw_full, sz_b)} (vs full raw)")
    print(f"  Time:            {ms_b:.0f} ms")
    print(f"  S3 1M/day est:   {s3_cost_1m_per_day(sz_b)}")

    print("\n" + "=" * 70)
    print("  Approach C -- Full JSONL -> zstd L22 (baseline)")
    print("=" * 70)
    t0 = time.perf_counter()
    blob_c = cctx_l22.compress(full_jsonl)
    ms_c   = (time.perf_counter() - t0) * 1000
    sz_c   = len(blob_c)
    print(f"  Compressed:      {fmt_bytes(sz_c)}")
    print(f"  Ratio:           {ratio(raw_full, sz_c)}")
    print(f"  Time:            {ms_c:.0f} ms")
    print(f"  S3 1M/day est:   {s3_cost_1m_per_day(sz_c)}")

    print("\n" + "=" * 70)
    print("  Approach D -- Separated: low-entropy->Liquefy, high-entropy->zstd L22")
    print("=" * 70)
    t0 = time.perf_counter()
    sz_d_liq, sz_d_zstd = sep_compress(receipts)
    ms_d = (time.perf_counter() - t0) * 1000
    sz_d_total = sz_d_liq + sz_d_zstd
    print(f"  Liquefy (structured fields): {fmt_bytes(sz_d_liq)}")
    print(f"  zstd L22 (sigs + hashes):    {fmt_bytes(sz_d_zstd)}")
    print(f"  Combined total:              {fmt_bytes(sz_d_total)}")
    print(f"  Ratio vs full raw:           {ratio(raw_full, sz_d_total)}")
    print(f"  Time:                        {ms_d:.0f} ms")
    print(f"  S3 1M/day est:               {s3_cost_1m_per_day(sz_d_total)}")

    # ── Summary table ────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("  SUMMARY")
    print("=" * 70)
    print(f"  {'Approach':<42} {'Size':>9}  {'Ratio':>7}  {'S3/mo':>12}")
    print(f"  {'-'*42} {'-'*9}  {'-'*7}  {'-'*12}")

    rows = [
        ("A  Full JSONL → Liquefy",         sz_a,       raw_full),
        ("B  Stripped JSONL → Liquefy",      sz_b,       raw_full),
        ("C  Full JSONL → zstd L22",         sz_c,       raw_full),
        ("D  Separated (Liquefy + zstd)",    sz_d_total, raw_full),
    ]
    for label, sz, raw in rows:
        r   = raw / sz if sz else 0
        s3  = s3_cost_1m_per_day(sz)
        print(f"  {label:<42} {fmt_bytes(sz):>9}  {r:>6.1f}x  {s3:>12}")

    print()
    print(f"  Raw JSONL (baseline): {fmt_bytes(raw_full)}")
    print()

    # ── Insight: what's driving size ─────────────────────────────────────
    print("--- Key insight ---")
    rand_pct = rand_fraction * 100
    struct_pct = (1 - rand_fraction) * 100
    print(f"  {rand_pct:.0f}% of raw bytes are cryptographically random (incompressible).")
    print(f"  {struct_pct:.0f}% are structured/low-cardinality and compress well.")
    best_structured = raw_strip / sz_b if sz_b else 0
    print(f"  Liquefy achieves {best_structured:.1f}x on the structured subset alone.")

    overhead_random = (sz_a - sz_b) / total_rand_bytes
    print(f"  Adding random fields: zstd overhead on incompressible data ≈ "
          f"{overhead_random*100:.0f}% expansion of the raw random payload.")

    winner_ratio = raw_full / min(sz_a, sz_b, sz_c, sz_d_total)
    winner_name  = {sz_a: 'A', sz_b: 'B', sz_c: 'C', sz_d_total: 'D'}[
        min(sz_a, sz_b, sz_c, sz_d_total)]
    print(f"\n  Best overall: Approach {winner_name} at {winner_ratio:.1f}x compression.")
    print()

if __name__ == "__main__":
    main()
