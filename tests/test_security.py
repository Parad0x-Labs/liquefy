"""Tests for the fixed encryption path + tamper-evident audit chain.

Runs under pytest, or standalone: `PYTHONPATH=src python tests/test_security.py`.
"""
import json
import os
import sys

# Pin THIS repo first: src/ for `liquefy`, repo root for `engines` — so a stray
# pip -e install elsewhere can't shadow the code under test.
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(_ROOT, "src"))
sys.path.insert(0, _ROOT)

from liquefy import (  # noqa: E402
    compress_encrypted,
    decompress_encrypted,
    commit_records,
    AuditChain,
    secure_audit_log,
)


def _data(n=40):
    return ("\n".join(
        json.dumps({"ts": 1700000000 + i, "src": f"agent-{i % 3}", "amount": 1000 + i})
        for i in range(n)
    )).encode("utf-8")


def _rows(b):
    return [json.loads(line) for line in b.splitlines() if line.strip()]


def test_encrypt_roundtrip():
    raw, key = _data(), os.urandom(32)
    blob = compress_encrypted(raw, key)
    assert blob != raw and len(blob) < len(raw)          # encrypted + compressed
    back = decompress_encrypted(blob, key)
    assert _rows(back) == _rows(raw)                      # value-lossless


def test_wrong_key_rejected():
    raw, key = _data(), os.urandom(32)
    blob = compress_encrypted(raw, key)
    try:
        decompress_encrypted(blob, os.urandom(32))
        assert False, "wrong key must not decrypt"
    except PermissionError:
        pass


def test_tenant_isolation():
    raw, key = _data(), os.urandom(32)
    blob = compress_encrypted(raw, key, tenant_id="acme")
    try:
        decompress_encrypted(blob, key, tenant_id="globex")
        assert False, "wrong tenant must not decrypt"
    except PermissionError:
        pass
    assert _rows(decompress_encrypted(blob, key, tenant_id="acme")) == _rows(raw)


def test_pcc_root_bound_into_aad():
    raw, key = _data(), os.urandom(32)
    c = commit_records(_rows(raw))
    blob = compress_encrypted(raw, key, commitment=c)
    data, meta = decompress_encrypted(blob, key, return_meta=True)
    assert _rows(data) == _rows(raw)
    # The PCC root is carried (and authenticated) in the sealed metadata.
    assert meta["meta"]["pcc_root"] == c.root_hex()
    # Flipping any byte breaks AEAD/HMAC -> hard failure, never silent.
    bad = bytearray(blob)
    bad[-1] ^= 0x01
    try:
        decompress_encrypted(bytes(bad), key)
        assert False, "tampered blob must not decrypt"
    except PermissionError:
        pass


def test_audit_chain_tamper_evident():
    ch = AuditChain()
    h0 = ch.append("seal", {"tenant": "acme"})
    h1 = ch.append("anchor", {"tx": "abc123"})
    assert ch.verify()
    assert h0 != h1 and ch.head == bytes.fromhex(h1)
    assert len(ch.entries) == 2
    # Altering any past entry breaks every subsequent link.
    ch._entries[0]["meta"]["tenant"] = "globex"
    assert not ch.verify()


def test_secure_audit_log_returns_head():
    h = secure_audit_log("unit-test-event", {"x": 1})
    assert isinstance(h, str) and len(h) == 64  # sha256 hex


def _run_all():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for t in tests:
        t()
        print(f"  PASS  {t.__name__}")
    print(f"\n{len(tests)}/{len(tests)} security tests passed")
    return True


if __name__ == "__main__":
    sys.exit(0 if _run_all() else 1)
