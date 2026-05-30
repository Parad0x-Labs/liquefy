#!/usr/bin/env bash
# Liquefy — one-command install
# Linux / macOS / WSL / Git Bash
set -e

echo ""
echo "  Liquefy — columnar compression that beats Zstd"
echo "  github.com/Parad0x-Labs/liquefy"
echo ""

# Python SDK
if command -v pip &>/dev/null; then
  echo "  [1/2] installing Python SDK..."
  pip install -q -r requirements.txt
  pip install -q -e .
  echo "  ✓  Python SDK ready"
  echo "       from liquefy import compress, decompress, search"
else
  echo "  [1/2] pip not found — skipping Python SDK"
  echo "        install Python 3.9+ then rerun this script"
fi

# CLI wrapper
chmod +x ./liquefy 2>/dev/null || true
echo "  ✓  CLI ready: ./liquefy compress / decompress / verify / search"

echo ""
echo "  Quick test:"
echo "    python -c \"from liquefy import compress,decompress; d=b'{\"x\":1}\\n'*1000; assert decompress(compress(d))==d; print('✓ works')\""
echo ""
echo "  Benchmark vs Zstd:"
echo "    python tools/benchmark.py"
echo ""
echo "  Docs:  github.com/Parad0x-Labs/liquefy"
echo "  x402:  github.com/Parad0x-Labs/dna-x402"
echo ""
