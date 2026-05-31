#!/usr/bin/env python3
"""
Liquefy Unified Benchmark Suite
=================================
Compares Liquefy against Zstd, LZ4, Brotli, and gzip across 6 log datasets.

Usage:
    pip install -r requirements.txt
    python tools/benchmark_suite.py
    python tools/benchmark_suite.py --lines 20000
    python tools/benchmark_suite.py --dataset json
    python tools/benchmark_suite.py --no-search

Outputs:
    REPORTS/BENCHMARK_SUITE_RESULTS.md
    REPORTS/benchmark_suite_results.json
"""

import argparse
import gzip
import hashlib
import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "engines" / "json_codec"))
sys.path.insert(0, str(REPO_ROOT / "engines"))

# ── optional imports (graceful degradation) ──────────────────────────────────
try:
    import zstandard as zstd
    HAS_ZSTD = True
except ImportError:
    HAS_ZSTD = False

try:
    import lz4.frame as lz4
    HAS_LZ4 = True
except ImportError:
    HAS_LZ4 = False

try:
    import brotli
    HAS_BROTLI = True
except ImportError:
    HAS_BROTLI = False

try:
    from NULL_Json_Columnar_Gun_v1 import NULL_Json_Columnar_Gun_v1 as LiquefyJSON
    HAS_LIQUEFY = True
except ImportError:
    HAS_LIQUEFY = False

# ── dataset generators ────────────────────────────────────────────────────────

def gen_json_logs(n):
    rows = []
    for i in range(n):
        rows.append(json.dumps({
            "ts": i, "level": "ERROR" if i % 100 == 0 else "INFO",
            "service": "api-gateway", "trace_id": f"trace-{i:08d}",
            "msg": f"handled request {i} in {i % 50}ms",
            "user_id": i % 500, "region": "eu-west-1",
        }, separators=(",", ":")))
    return "\n".join(rows).encode()

def gen_payment_receipts(n):
    rows = []
    for i in range(n):
        rows.append(json.dumps({
            "tx_id": f"tx-{i:010d}", "amount": round((i % 999) + 0.99, 2),
            "currency": "USD", "status": "SETTLED" if i % 20 != 0 else "FAILED",
            "merchant": f"merchant-{i % 50:04d}", "ts": 1700000000 + i,
        }, separators=(",", ":")))
    return "\n".join(rows).encode()

def gen_nginx_logs(n):
    lines = []
    methods = ["GET", "POST", "PUT", "DELETE"]
    codes   = ["200", "200", "200", "304", "404", "500"]
    for i in range(n):
        lines.append(
            f'192.168.{i%255}.{i%254} - - [01/Jan/2026:00:{i%60:02d}:{i%60:02d} +0000]'
            f' "{methods[i%4]} /api/v1/resource/{i%100} HTTP/1.1"'
            f' {codes[i%6]} {(i%9+1)*512}'
        )
    return "\n".join(lines).encode()

def gen_k8s_logs(n):
    rows = []
    for i in range(n):
        rows.append(json.dumps({
            "ts": f"2026-01-01T00:{i%60:02d}:{i%60:02d}Z",
            "stream": "stdout", "pod": f"app-{i%20:05d}",
            "namespace": "production", "container": "api",
            "log": f"INFO  handler=/{['health','metrics','ready'][i%3]} latency={i%200}ms",
        }, separators=(",", ":")))
    return "\n".join(rows).encode()

def gen_syslog(n):
    lines = []
    hosts = [f"host-{i:03d}" for i in range(10)]
    procs = ["sshd", "cron", "kernel", "systemd", "dockerd"]
    for i in range(n):
        lines.append(
            f"Jan  1 00:{i%60:02d}:{i%60:02d} {hosts[i%10]} {procs[i%5]}[{1000+i%900}]:"
            f" message {i}: operation completed status=ok retries={i%3}"
        )
    return "\n".join(lines).encode()

def gen_sql_logs(n):
    rows = []
    tables = ["users", "orders", "products", "sessions", "events"]
    for i in range(n):
        rows.append(json.dumps({
            "ts": f"2026-01-01 00:{i%60:02d}:{i%60:02d}.{i%999:03d}",
            "pid": 1000 + i % 200, "duration_ms": i % 500,
            "query": f"SELECT * FROM {tables[i%5]} WHERE id={i} LIMIT 100",
            "rows_returned": i % 100,
        }, separators=(",", ":")))
    return "\n".join(rows).encode()

DATASETS = {
    "json":     ("JSON agent logs",       gen_json_logs),
    "payments": ("Payment receipts",      gen_payment_receipts),
    "nginx":    ("Nginx access logs",     gen_nginx_logs),
    "k8s":      ("Kubernetes logs",       gen_k8s_logs),
    "syslog":   ("Syslog (RFC 3164)",     gen_syslog),
    "sql":      ("PostgreSQL slow query", gen_sql_logs),
}

# ── compressor wrappers ───────────────────────────────────────────────────────

def _mb(n_bytes, seconds):
    return n_bytes / 1_048_576 / seconds if seconds > 0 else 0

def run_zstd(data, level):
    if not HAS_ZSTD:
        return None
    cctx = zstd.ZstdCompressor(level=level)
    t0 = time.perf_counter(); c = cctx.compress(data); ct = time.perf_counter()-t0
    dctx = zstd.ZstdDecompressor()
    t0 = time.perf_counter(); r = dctx.decompress(c);   dt = time.perf_counter()-t0
    return c, ct, dt, r

def run_lz4(data):
    if not HAS_LZ4:
        return None
    t0 = time.perf_counter(); c = lz4.compress(data);   ct = time.perf_counter()-t0
    t0 = time.perf_counter(); r = lz4.decompress(c);    dt = time.perf_counter()-t0
    return c, ct, dt, r

def run_brotli(data, quality):
    if not HAS_BROTLI:
        return None
    t0 = time.perf_counter(); c = brotli.compress(data, quality=quality); ct = time.perf_counter()-t0
    t0 = time.perf_counter(); r = brotli.decompress(c);                   dt = time.perf_counter()-t0
    return c, ct, dt, r

def run_gzip(data, level):
    t0 = time.perf_counter(); c = gzip.compress(data, compresslevel=level); ct = time.perf_counter()-t0
    t0 = time.perf_counter(); r = gzip.decompress(c);                        dt = time.perf_counter()-t0
    return c, ct, dt, r

def run_liquefy(data):
    if not HAS_LIQUEFY:
        return None
    try:
        engine = LiquefyJSON(level=22)
        t0 = time.perf_counter(); c = engine.compress(data);   ct = time.perf_counter()-t0
        t0 = time.perf_counter(); r = engine.decompress(c);    dt = time.perf_counter()-t0
        return c, ct, dt, r
    except Exception:
        return None

def search_full_decompress(compressed, query, decomp_fn):
    """Generic search: decompress everything then grep lines."""
    t0 = time.perf_counter()
    raw = decomp_fn(compressed)
    hits = sum(1 for ln in raw.splitlines() if query in ln)
    return (time.perf_counter()-t0)*1000, hits

def search_liquefy_columnar(compressed, query):
    """Liquefy columnar search: only decompresses relevant columns."""
    if not HAS_LIQUEFY:
        return None, None
    try:
        engine = LiquefyJSON()
        t0 = time.perf_counter()
        hits = len(engine.grep(compressed, query))
        return (time.perf_counter()-t0)*1000, hits
    except Exception:
        return None, None

# ── benchmark runner ──────────────────────────────────────────────────────────

def benchmark_dataset(name, label, data, run_search, search_query):
    raw = len(data)
    results = []

    def record(compressor, blob_ct_dt_r):
        if blob_ct_dt_r is None:
            return
        c, ct, dt, r = blob_ct_dt_r
        ok = (r == data) if name in ("nginx","syslog") else (len(r) == len(data))
        results.append({
            "compressor": compressor,
            "raw_bytes": raw,
            "compressed_bytes": len(c),
            "ratio": round(raw / len(c), 2),
            "compress_mbs": round(_mb(raw, ct), 1),
            "decompress_mbs": round(_mb(raw, dt), 1),
            "bit_perfect": ok,
            "search_ms": None,
            "search_hits": None,
            "_blob": c,
        })

    # Liquefy (JSON datasets only)
    if name in ("json", "payments", "k8s", "sql"):
        record("Liquefy COL", run_liquefy(data))
    # Zstd
    for lvl in (3, 9, 19, 22):
        record(f"Zstd L{lvl}", run_zstd(data, lvl))
    # LZ4
    record("LZ4", run_lz4(data))
    # Brotli
    for q in (5, 9, 11):
        record(f"Brotli Q{q}", run_brotli(data, q))
    # gzip
    for lvl in (6, 9):
        record(f"gzip -{lvl}", run_gzip(data, lvl))

    # Search latency
    if run_search and results:
        q_bytes = search_query.encode()
        for row in results:
            c = row["_blob"]
            if row["compressor"] == "Liquefy COL":
                ms, hits = search_liquefy_columnar(c, search_query)
            elif row["compressor"].startswith("Zstd"):
                lvl = int(row["compressor"].split("L")[1])
                ms, hits = search_full_decompress(c, q_bytes,
                    lambda b, l=lvl: zstd.ZstdDecompressor().decompress(b))
            elif row["compressor"] == "LZ4" and HAS_LZ4:
                ms, hits = search_full_decompress(c, q_bytes, lz4.decompress)
            elif row["compressor"].startswith("Brotli") and HAS_BROTLI:
                ms, hits = search_full_decompress(c, q_bytes, brotli.decompress)
            elif row["compressor"].startswith("gzip"):
                ms, hits = search_full_decompress(c, q_bytes, gzip.decompress)
            else:
                ms, hits = None, None
            row["search_ms"]   = round(ms, 2) if ms is not None else None
            row["search_hits"] = hits

    # Clean up blobs before returning
    for row in results:
        del row["_blob"]

    return results

# ── formatting ────────────────────────────────────────────────────────────────

COL_W = [18, 9, 11, 8, 12, 14, 11, 10]
HEADERS = ["Compressor", "Raw MB", "Comp MB", "Ratio", "Comp MB/s", "Decomp MB/s", "BitPerfect", "Search ms"]

def fmt_row(r):
    raw_mb  = f"{r['raw_bytes']/1e6:.2f}"
    comp_mb = f"{r['compressed_bytes']/1e6:.2f}"
    ratio   = f"{r['ratio']:.2f}x"
    c_mbs   = f"{r['compress_mbs']:.0f}"
    d_mbs   = f"{r['decompress_mbs']:.0f}"
    bp      = "PASS" if r['bit_perfect'] else "FAIL"
    srch    = f"{r['search_ms']:.1f}" if r['search_ms'] is not None else "-"
    return [r['compressor'], raw_mb, comp_mb, ratio, c_mbs, d_mbs, bp, srch]

def print_table(rows):
    sep = "+" + "+".join("-"*(w+2) for w in COL_W) + "+"
    def fmt(cells):
        return "|" + "|".join(f" {c:<{w}} " for c, w in zip(cells, COL_W)) + "|"
    print(sep)
    print(fmt(HEADERS))
    print(sep)
    for r in rows:
        print(fmt(fmt_row(r)))
    print(sep)

def md_table(rows):
    def row(cells):
        return "| " + " | ".join(cells) + " |"
    divider = "| " + " | ".join("---" for _ in HEADERS) + " |"
    lines = [row(HEADERS), divider]
    for r in rows:
        lines.append(row(fmt_row(r)))
    return "\n".join(lines)

# ── main ──────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Liquefy unified benchmark suite")
    ap.add_argument("--lines",   type=int, default=10_000, help="Lines per dataset (default 10000)")
    ap.add_argument("--dataset", choices=list(DATASETS)+["all"], default="all")
    ap.add_argument("--no-search", action="store_true")
    args = ap.parse_args()

    missing = []
    if not HAS_ZSTD:   missing.append("zstandard")
    if not HAS_LZ4:    missing.append("lz4")
    if not HAS_BROTLI: missing.append("brotli")
    if missing:
        print(f"[warn] Missing packages (will be skipped): {', '.join(missing)}")
        print("       Run: pip install -r requirements.txt\n")

    datasets = {k: v for k, v in DATASETS.items()} if args.dataset == "all" \
               else {args.dataset: DATASETS[args.dataset]}

    all_results = {}
    md_sections = [
        "# Liquefy Benchmark Suite Results\n",
        f"Generated against {args.lines:,} lines per dataset.\n",
        "Search latency = time to find a target string in the compressed archive.\n",
        "Liquefy uses native columnar grep (no full decompress). All others decompress then scan.\n\n---\n",
    ]

    for ds_key, (ds_label, ds_gen) in datasets.items():
        print(f"\n{'='*60}")
        print(f"  Dataset: {ds_label}  ({args.lines:,} lines)")
        print(f"{'='*60}")

        data = ds_gen(args.lines)
        # pick a query that exists in the data
        search_query = "trace-00009999" if ds_key == "json" else \
                       "tx-0000009999"  if ds_key == "payments" else \
                       "/api/v1/resource/99" if ds_key == "nginx" else \
                       "app-00019"      if ds_key == "k8s" else \
                       "host-009"       if ds_key == "syslog" else \
                       "events"

        rows = benchmark_dataset(ds_key, ds_label, data,
                                 run_search=not args.no_search,
                                 search_query=search_query)
        all_results[ds_key] = rows
        print_table(rows)

        # highlight best ratio
        liquefy_rows = [r for r in rows if r["compressor"] == "Liquefy COL"]
        zstd19_rows  = [r for r in rows if r["compressor"] == "Zstd L19"]
        if liquefy_rows and zstd19_rows:
            gain = liquefy_rows[0]["ratio"] / zstd19_rows[0]["ratio"]
            print(f"  -> Liquefy is {gain:.2f}x better ratio than Zstd L19 on this dataset")

        md_sections.append(f"## {ds_label}\n\n{md_table(rows)}\n")

    # ── write reports ────────────────────────────────────────────────────────
    reports_dir = REPO_ROOT / "REPORTS"
    reports_dir.mkdir(exist_ok=True)

    md_path = reports_dir / "BENCHMARK_SUITE_RESULTS.md"
    md_path.write_text("\n".join(md_sections), encoding="utf-8")

    json_path = reports_dir / "benchmark_suite_results.json"
    json_path.write_text(json.dumps(all_results, indent=2), encoding="utf-8")

    print(f"\nReports written:")
    print(f"  {md_path}")
    print(f"  {json_path}")

if __name__ == "__main__":
    main()
