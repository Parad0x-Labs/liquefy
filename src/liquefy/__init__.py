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

from liquefy._api import compress, compress_records, decompress, search, compress_encrypted, decompress_encrypted

# Per-Column Commitment — keystone of the Verifiable Evidence Layer.
# Pin every column under one 32-byte root; prove/disclose a single column
# without revealing the rest. Pure stdlib, no agent/Solana deps.
from liquefy.pcc import (
    commit_records,
    commit_jsonl,
    inclusion_proof,
    verify_inclusion,
    verify_disclosure,
    Commitment,
    InclusionProof,
)

__version__ = "0.2.2"
__all__ = [
    "compress", "compress_records", "decompress", "search",
    "compress_encrypted", "decompress_encrypted",
    "commit_records", "commit_jsonl", "inclusion_proof",
    "verify_inclusion", "verify_disclosure", "Commitment", "InclusionProof",
]
