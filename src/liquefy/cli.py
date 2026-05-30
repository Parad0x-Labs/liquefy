"""
liquefy CLI — entry point for `pip install liquefy` users.
Mirrors the bash ./liquefy wrapper but works cross-platform.
"""
import sys
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        prog="liquefy",
        description="Columnar compression that beats Zstd on structured data.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("compress",   help="Compress a JSONL file")
    c.add_argument("input",  type=Path)
    c.add_argument("output", type=Path)

    d = sub.add_parser("decompress", help="Decompress a .null archive")
    d.add_argument("input",  type=Path)
    d.add_argument("output", type=Path)

    s = sub.add_parser("search",     help="Search without full decompress")
    s.add_argument("archive", type=Path)
    s.add_argument("query",   type=str)

    v = sub.add_parser("verify",     help="Verify bit-perfect round-trip")
    v.add_argument("input",   type=Path)

    b = sub.add_parser("benchmark",  help="Head-to-head vs Zstd")
    b.add_argument("--lines", type=int, default=50_000)

    args = parser.parse_args()

    from liquefy import compress, decompress, search as lsearch

    if args.cmd == "compress":
        data = args.input.read_bytes()
        blob = compress(data)
        args.output.write_bytes(blob)
        ratio = len(data) / len(blob)
        print(f"✓  {args.input.name}  {len(data)/1e6:.2f}MB → {len(blob)/1e6:.2f}MB  ({ratio:.1f}×)")

    elif args.cmd == "decompress":
        blob = args.input.read_bytes()
        data = decompress(blob)
        args.output.write_bytes(data)
        print(f"✓  restored {len(data)/1e6:.2f}MB → {args.output}")

    elif args.cmd == "search":
        blob = args.archive.read_bytes()
        result = lsearch(blob, args.query)
        status = "FOUND" if result["found"] else "NOT FOUND"
        print(f"{status}  query={args.query!r}  latency={result['latency_ms']}ms  method={result['method']}")

    elif args.cmd == "verify":
        data = args.input.read_bytes()
        blob = compress(data)
        restored = decompress(blob)
        if restored == data:
            ratio = len(data) / len(blob)
            print(f"✓  bit-perfect  ratio={ratio:.1f}×  {len(data)/1e6:.2f}MB → {len(blob)/1e6:.2f}MB")
        else:
            print("✗  MISMATCH — restoration not bit-perfect", file=sys.stderr)
            sys.exit(1)

    elif args.cmd == "benchmark":
        import subprocess, sys
        root = Path(__file__).resolve().parent.parent.parent
        subprocess.run([sys.executable, str(root / "tools" / "benchmark.py"),
                       "--lines", str(args.lines)], check=True)
