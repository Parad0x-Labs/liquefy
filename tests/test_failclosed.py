"""Fail-closed regression tests.

Pins two correctness/security contracts so they can't silently regress:

  1. A corrupt / bad-magic archive must RAISE (never return empty bytes), and the
     CLI must exit non-zero — never print a green "restored 0.00MB" on failure.
  2. Encryption must REFUSE to run without an explicit master secret (no fallback
     to a public constant key), and the orchestrator must not silently encrypt
     with a default key — while the non-encrypting paths still work with no secret.

Runs under pytest, or standalone: `PYTHONPATH=src python tests/test_failclosed.py`.
"""
import io
import json
import os
import sys
import tempfile

# Pin THIS repo first: src/ for `liquefy`, repo root for `engines` — so a stray
# pip -e install elsewhere can't shadow the code under test.
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(_ROOT, "src"))
sys.path.insert(0, _ROOT)

import liquefy  # noqa: E402
from liquefy.cli import main as cli_main  # noqa: E402
from security_compliance import NULL_Security_Layer  # noqa: E402
from orchestrator import NULL_Orchestrator  # noqa: E402


def _jsonl(n=20):
    recs = [{"a": i, "b": f"x{i % 3}"} for i in range(n)]
    raw = "\n".join(json.dumps(r) for r in recs).encode("utf-8")
    return recs, raw


def _rows(b):
    return [json.loads(line) for line in b.splitlines() if line.strip()]


# ── Bug 1: corrupt archive must not be silent data-loss ──────────────────────

def test_bad_magic_raises_not_empty():
    try:
        liquefy.decompress(b"TOTALLY-NOT-A-LIQUEFY-ARCHIVE" * 4)
        assert False, "bad magic must raise, not return empty bytes"
    except ValueError as e:
        assert "bad magic" in str(e).lower()


def test_truncated_blob_raises():
    _, raw = _jsonl()
    blob = liquefy.compress(raw)
    # Strip the magic so the header no longer matches — must fail loudly.
    try:
        liquefy.decompress(blob[2:])
        assert False, "truncated/de-magicked blob must raise"
    except ValueError:
        pass


def test_good_roundtrip_still_value_lossless():
    recs, raw = _jsonl()
    assert _rows(liquefy.decompress(liquefy.compress(raw))) == recs


def test_cli_decompress_fails_closed_on_corrupt():
    d = tempfile.mkdtemp()
    inp = os.path.join(d, "bad.null")
    out = os.path.join(d, "out.bin")
    with open(inp, "wb") as f:
        f.write(b"TOTALLY-NOT-A-LIQUEFY-ARCHIVE" * 4)

    err = io.StringIO()
    old_err, sys.stderr = sys.stderr, err
    old_argv, sys.argv = sys.argv, ["liquefy", "decompress", inp, out]
    code = "no-exit"
    try:
        cli_main()
    except SystemExit as e:
        code = e.code
    finally:
        sys.stderr, sys.argv = old_err, old_argv

    assert code == 1, f"CLI must exit 1 on corrupt input, got {code!r}"
    assert not os.path.exists(out), "no output file may be written on failure"
    msg = err.getvalue()
    assert "✓" not in msg, "must never print a green check on failure"
    assert "✗" in msg or "cannot decompress" in msg


# ── Bug 2: no default encryption key ─────────────────────────────────────────

def test_security_layer_refuses_default_key():
    try:
        NULL_Security_Layer()  # no secret
        assert False, "must refuse to encrypt without an explicit secret"
    except ValueError as e:
        assert "secret" in str(e).lower()


def test_security_layer_accepts_explicit_secret():
    # str and bytes both accepted; sealing round-trips.
    layer = NULL_Security_Layer(master_secret=b"\x01" * 32)
    sealed = layer.seal(b"hello", "acme")
    data, _ = layer.unseal(sealed, "acme")
    assert data == b"hello"
    assert NULL_Security_Layer(master_secret="KMS_KEY").master_secret == b"KMS_KEY"


def test_orchestrator_constructs_without_secret():
    # Constructing is allowed (e.g. to inspect engines) — the failure is deferred
    # to the moment an encrypting path is actually taken.
    o = NULL_Orchestrator(safety_enabled=True)
    assert o.detect_engine(b'{"a":1}\n') == "json_columnar"


def test_orchestrator_encrypt_path_raises_without_secret():
    _, raw = _jsonl()
    o = NULL_Orchestrator(safety_enabled=True)  # no security_secret
    try:
        o.compress(raw, engine_key="json_columnar")
        assert False, "orchestrator must not silently encrypt with a default key"
    except ValueError as e:
        assert "secret" in str(e).lower()


def test_orchestrator_full_pipeline_with_secret():
    recs, raw = _jsonl()
    o = NULL_Orchestrator(safety_enabled=True, security_secret="KMS")
    sealed = o.compress(raw, engine_key="json_columnar")
    assert _rows(o.decompress(sealed)) == recs


def _run_all():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for t in tests:
        t()
        print(f"  PASS  {t.__name__}")
    print(f"\n{len(tests)}/{len(tests)} fail-closed tests passed")
    return True


if __name__ == "__main__":
    sys.exit(0 if _run_all() else 1)
