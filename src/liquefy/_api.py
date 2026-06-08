"""
Clean public API — thin wrapper over the engine internals.
Agents and SDKs import from here. All heavy lifting is in engines/.
"""

from __future__ import annotations
import sys
import os
from pathlib import Path

# Wire up engine paths — works in dev (repo clone) and installed (pip)
def _wire_engines() -> None:
    # Prefer the engines/ that ships with THIS package (dev/src layout: 3 levels up
    # from src/liquefy/_api.py) so a stray editable install of liquefy elsewhere
    # cannot shadow it via the meta-path finder. In a wheel install there is no
    # repo-relative engines/, so fall back to importing the top-level `engines`.
    _repo_engines = Path(__file__).resolve().parent.parent.parent / "engines"
    if (_repo_engines / "__init__.py").exists():
        _ep = _repo_engines
    else:
        try:
            import engines as _e
            _ep = Path(_e.__file__).resolve().parent
        except ImportError:
            return
    for _d in _ep.iterdir():
        if _d.is_dir() and str(_d) not in sys.path:
            sys.path.insert(0, str(_d))
    if str(_ep) not in sys.path:
        sys.path.insert(0, str(_ep))

_wire_engines()

from NULL_Json_Columnar_Gun_v1 import NULL_Json_Columnar_Gun_v1 as _ColGun  # type: ignore
from security_compliance import NULL_Security_Layer, AuditChain, secure_audit_log  # type: ignore

_ENGINE = _ColGun(level=22)


def compress_records(records: list) -> bytes:
    """
    Compress a list of dicts (agent logs, receipts, tool calls, etc).
    This is the primary handoff point — pass any structured records,
    get back compressed bytes ready for encryption / Arweave / anchoring.

    Args:
        records: List of dicts. All dicts should share the same schema
                 for best compression (agent logs, receipts, spans, etc).

    Returns:
        Compressed bytes. Pass directly to encrypt(), upload to Arweave,
        or anchor the sha256() as a Solana commitment.

    Example:
        from liquefy import compress_records
        blob = compress_records(receipts)          # receipts: list[dict]
        commitment = hashlib.sha256(blob).digest() # 32-byte anchor
    """
    import json as _json
    lines = "\n".join(_json.dumps(r, separators=(",", ":")) for r in records)
    return _ENGINE.compress(lines.encode("utf-8"))


def compress(data: bytes | str) -> bytes:
    """
    Compress structured JSON/JSONL bytes using Liquefy Columnar Gun v1.

    Args:
        data: Raw JSONL bytes (or str — will be UTF-8 encoded).
              Each line should be a JSON object for best compression.

    Returns:
        Compressed bytes. 33–61× smaller than input on structured data.

    Example:
        blob = compress(open("receipts.jsonl", "rb").read())
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    return _ENGINE.compress(data)


def decompress(blob: bytes) -> bytes:
    """
    Decompress a Liquefy-compressed blob back to the recovered records.

    Value-lossless: the recovered records are equal to the originals and the
    recovery is SHA-256-verified, but textual formatting (whitespace, JSON
    key-order) is normalized — the output is not guaranteed byte-identical to
    the original input.

    Args:
        blob: Compressed bytes from compress().

    Returns:
        Recovered bytes.

    Raises:
        ValueError: if the blob is not a recognized Liquefy archive (bad magic
            / corrupt / truncated). The error propagates to the caller — we
            never silently return empty bytes on a bad archive.
    """
    return _ENGINE.decompress(blob)


def search(blob: bytes, query: str) -> dict:
    """
    Search a compressed blob WITHOUT full decompression.

    Liquefy's columnar layout means it only decompresses the relevant column,
    making search 5–61× faster than decompressing first and then searching.

    Args:
        blob:  Compressed bytes from compress().
        query: String to search for.

    Returns:
        Dict with keys:
            found       (bool)   — whether the query was found
            matches     (list)   — matching row indices
            latency_ms  (float)  — search time in milliseconds
            method      (str)    — "columnar_grep" (partial decompress)
                                   or "fallback_full" (full decompress)

    Example:
        result = search(blob, "trace-00049999")
        if result["found"]:
            print(f"Found in {result['latency_ms']:.1f}ms")
    """
    import time
    t = time.perf_counter()
    raw = _ENGINE.grep(blob, query)
    elapsed = (time.perf_counter() - t) * 1000
    return {
        "found":      bool(raw.get("matches")),
        "matches":    raw.get("matches", []),
        "latency_ms": round(elapsed, 2),
        "method":     raw.get("method", "columnar_grep"),
    }


def compress_encrypted(data: bytes | str, key: bytes, *, commitment=None,
                       tenant_id: str = "liquefy") -> bytes:
    """
    Compress then encrypt with AES-256-GCM (tenant-isolated key derivation).

    Only the key-holder can decompress. Used for private agent payment receipt
    batches — parties share the key, the chain sees only the ciphertext.

    Args:
        data:       Raw JSONL bytes or str.
        key:        Shared secret (e.g. os.urandom(32)). The AES key is derived
                    from (key, tenant_id) via PBKDF2 with a per-blob salt.
        commitment: Optional PCC Commitment (or 32-byte root). When supplied, the
                    root is bound into the AES-GCM AAD, cryptographically tying
                    the ciphertext to the column commitment.
        tenant_id:  Multi-tenant isolation label (default "liquefy").

    Returns:
        Sealed bytes — decrypt with decompress_encrypted(..., key, tenant_id=).
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    compressed = compress(data)
    metadata: dict = {}
    if commitment is not None:
        root = getattr(commitment, "root", commitment)
        metadata["pcc_root"] = root.hex() if isinstance(root, (bytes, bytearray)) else str(root)
    layer = NULL_Security_Layer(master_secret=key)
    return layer.seal(compressed, tenant_id, metadata)


def decompress_encrypted(blob: bytes, key: bytes, *, tenant_id: str = "liquefy",
                         return_meta: bool = False):
    """
    Decrypt then decompress a sealed Liquefy blob.

    Args:
        blob:        Sealed bytes from compress_encrypted().
        key:         Same shared secret used to seal.
        tenant_id:   Same tenant label used to seal (default "liquefy").
        return_meta: If True, return (data, metadata); metadata carries the bound
                     pcc_root when one was supplied. Default False returns data.

    Raises:
        PermissionError on wrong key/tenant or any tampering.
    """
    layer = NULL_Security_Layer(master_secret=key)
    compressed, metadata = layer.unseal(blob, tenant_id)
    data = decompress(compressed)
    return (data, metadata) if return_meta else data
