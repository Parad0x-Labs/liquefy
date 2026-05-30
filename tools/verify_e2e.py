#!/usr/bin/env python3
"""
Liquefy End-to-End Verification
================================
Generates synthetic JSON logs, compresses with the columnar engine,
restores, and confirms bit-perfect SHA-256 identity.

Usage:
    pip install -r requirements.txt
    python tools/verify_e2e.py
"""

import sys
import json
import hashlib
import time
from pathlib import Path

# Resolve repo root regardless of cwd
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "engines" / "json_codec"))
sys.path.insert(0, str(REPO_ROOT / "engines"))

try:
    from NULL_Json_Columnar_Gun_v1 import NULL_Json_Columnar_Gun_v1 as Engine
except ImportError as e:
    print(f"ERROR: Could not import engine: {e}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def generate_logs(n=10_000) -> bytes:
    """Generate compact JSON (no extra spaces) — matches engine output format."""
    lines = []
    for i in range(n):
        lines.append(json.dumps({
            "ts": i,
            "level": "ERROR" if i % 100 == 0 else "INFO",
            "service": "api-gateway",
            "trace_id": f"trace-{i:08d}",
            "msg": f"handled request {i} in {i % 50}ms",
        }, separators=(",", ":")))
    return "\n".join(lines).encode()


def main():
    print("=== Liquefy E2E Verification ===\n")

    # Step 1: generate
    print("[1/4] Generating 10,000 JSON log lines...")
    raw = generate_logs(10_000)
    raw_hash = sha256(raw)
    print(f"      {len(raw):,} bytes  sha256={raw_hash[:16]}...")

    # Step 2: compress
    print("[2/4] Compressing with JSON columnar engine...")
    engine = Engine(level=22)
    t0 = time.perf_counter()
    compressed = engine.compress(raw)
    c_ms = (time.perf_counter() - t0) * 1000
    ratio = len(raw) / len(compressed)
    print(f"      {len(compressed):,} bytes  ratio={ratio:.2f}x  ({c_ms:.1f} ms)")

    # Step 3: restore
    print("[3/4] Restoring...")
    t0 = time.perf_counter()
    restored = engine.decompress(compressed)
    d_ms = (time.perf_counter() - t0) * 1000
    print(f"      {len(restored):,} bytes  ({d_ms:.1f} ms)")

    # Step 4: verify
    print("[4/4] SHA-256 identity check...")
    restored_hash = sha256(restored)
    if raw == restored and raw_hash == restored_hash:
        print(f"\n  PASS  sha256={restored_hash}")
        print("  Bit-perfect restoration confirmed.\n")
    else:
        print("\n  FAIL  Data mismatch!")
        sys.exit(1)


if __name__ == "__main__":
    main()
