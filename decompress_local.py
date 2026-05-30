#!/usr/bin/env python3
"""
Liquefy Local Decompressor (Public Reference Path)
=================================================
Provides SHA-256 integrity verification against proof-pack/hashes.txt,
and directs users to the appropriate engine or sealed decoder for actual
decompression.

For enterprise-grade, hardened restoration, use the sealed decoder appliance.
Visit: https://github.com/Parad0x-Labs/liquefy/blob/master/docs/enterprise-evaluation.md
"""

import argparse
import sys
import os
import hashlib


def calculate_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def load_hashes(hashes_file):
    """Parse proof-pack/hashes.txt into a dict of {path: hash}."""
    entries = {}
    with open(hashes_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(None, 1)
            if len(parts) == 2:
                digest, path = parts
                entries[path] = digest
    return entries


def verify_archive(archive_path, hashes_file):
    if not os.path.exists(hashes_file):
        print(f"Error: hashes file not found: {hashes_file}")
        sys.exit(1)

    actual_hash = calculate_sha256(archive_path)

    try:
        hashes = load_hashes(hashes_file)
    except Exception as e:
        print(f"Error reading hashes file: {e}")
        sys.exit(1)

    # Match by filename or full path stored in hashes.txt
    archive_name = os.path.basename(archive_path)
    expected_hash = None
    for path, digest in hashes.items():
        if path == archive_path or os.path.basename(path) == archive_name:
            expected_hash = digest
            break

    print(f"Archive : {archive_path}")
    print(f"SHA-256 : {actual_hash}")

    if expected_hash is None:
        print(f"FAIL  - no entry found for '{archive_name}' in {hashes_file}")
        sys.exit(1)

    if actual_hash == expected_hash:
        print(f"PASS  - hash matches proof-pack record")
        sys.exit(0)
    else:
        print(f"FAIL  - expected {expected_hash}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Liquefy Local Reference Decompressor")
    parser.add_argument("archive", help="Path to the .liq / .null archive")
    parser.add_argument("-o", "--output", help="Output path for restored data")
    parser.add_argument("--verify-only", action="store_true",
                        help="Only verify SHA-256 integrity against proof-pack/hashes.txt")

    args = parser.parse_args()

    if not os.path.exists(args.archive):
        print(f"Error: Archive not found: {args.archive}")
        sys.exit(1)

    print("--- Liquefy Local Reference Tool ---")
    print(f"Archive: {args.archive}")

    if args.verify_only:
        hashes_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "proof-pack", "hashes.txt")
        verify_archive(args.archive, hashes_file)
        # verify_archive exits; no fall-through

    # Decompression path — no sealed engine bundled in this public reference script
    print()
    print("The Python engines are in engines/ — use them directly for decompression.")
    print("Example:")
    print("  python engines/json_codec/NULL_Json_Columnar_Gun_v1.py")
    print()
    print("For bit-perfect, enterprise-grade restoration use the sealed decoder appliance:")
    print("  docker run --rm -v \"$(pwd)\":/data parad0xlabs/liquefy-decoder:latest /data/<archive>")
    sys.exit(0)


if __name__ == "__main__":
    main()
