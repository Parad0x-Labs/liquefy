"""
Liquefy — columnar compression that beats Zstd on structured data.

Quick start:
    from liquefy import compress, decompress, search

    blob = compress(my_jsonl_bytes)        # 33-61× smaller than raw
    original = decompress(blob)            # bit-perfect restoration
    result = search(blob, "trace-00001")   # search WITHOUT full decompress

For AI agent payment receipt batching (Solana x402):
    See https://github.com/Parad0x-Labs/dna-x402 → packages/liquefy-receipts/
"""

from liquefy._api import compress, decompress, search, compress_encrypted, decompress_encrypted

__version__ = "0.1.0"
__all__ = ["compress", "decompress", "search", "compress_encrypted", "decompress_encrypted"]
