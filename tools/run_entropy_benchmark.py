#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="path to a log file")
    ap.add_argument("--level", type=int, default=19)
    args = ap.parse_args()

    engine = Path(__file__).resolve().parents[1] / "engines" / "null_entropy_max_v2.py"
    out = Path(args.input).with_suffix(".nmx")

    print("== Compress ==")
    subprocess.check_call([sys.executable, str(engine), "compress", args.input, str(out), "--level", str(args.level)])

    print("\n== Decompress ==")
    restored = Path(args.input).with_suffix(".restored")
    subprocess.check_call([sys.executable, str(engine), "decompress", str(out), str(restored), "--level", str(args.level)])

    # byte-proof
    a = Path(args.input).read_bytes()
    b = restored.read_bytes()
    print("\n== Proof ==")
    print("✅ BYTE-PERFECT MATCH" if a == b else "❌ MISMATCH")

if __name__ == "__main__":
    main()

