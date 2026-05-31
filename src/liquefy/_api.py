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
    # Installed: engines is a top-level package alongside liquefy
    try:
        import engines as _e
        _ep = Path(_e.__file__).resolve().parent
        for _d in _ep.iterdir():
            if _d.is_dir() and str(_d) not in sys.path:
                sys.path.insert(0, str(_d))
        if str(_ep) not in sys.path:
            sys.path.insert(0, str(_ep))
        return
    except ImportError:
        pass
    # Dev / editable: engines/ at repo root (3 levels up from src/liquefy/_api.py)
    _ep = Path(__file__).resolve().parent.parent.parent / "engines"
    if _ep.exists():
        for _d in _ep.iterdir():
            if _d.is_dir() and str(_d) not in sys.path:
                sys.path.insert(0, str(_d))
        if str(_ep) not in sys.path:
            sys.path.insert(0, str(_ep))

_wire_engines()

from NULL_Json_Columnar_Gun_v1 import NULL_Json_Columnar_Gun_v1 as _ColGun  # type: ignore
from security_compliance import NULL_Security_Layer  # type: ignore

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
    Decompress a Liquefy-compressed blob back to the original bytes.
    Bit-perfect: output is byte-for-byte identical to the original input.

    Args:
        blob: Compressed bytes from compress().

    Returns:
        Original bytes.
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


def compress_encrypted(data: bytes | str, key: bytes) -> bytes:
    """
    Compress then encrypt with AES-256-GCM.

    Only the key-holder can decompress. Used for private agent payment
    receipt batches — parties share the key, chain sees only the ciphertext.

    Args:
        data: Raw JSONL bytes or str.
        key:  32-byte AES-256 key.

    Returns:
        Encrypted+compressed bytes.
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    compressed = compress(data)
    layer = NULL_Security_Layer(encryption_key=key)
    return layer.encrypt(compressed)


def decompress_encrypted(blob: bytes, key: bytes) -> bytes:
    """
    Decrypt then decompress an encrypted Liquefy blob.

    Args:
        blob: Encrypted+compressed bytes from compress_encrypted().
        key:  Same 32-byte AES-256 key used to encrypt.

    Returns:
        Original bytes.
    """
    layer = NULL_Security_Layer(encryption_key=key)
    compressed = layer.decrypt(blob)
    return decompress(compressed)
