"""Tests for liquefy.pcc — Per-Column Commitment.

Runs under pytest, or standalone: `PYTHONPATH=src python tests/test_pcc.py`.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from liquefy.pcc import (  # noqa: E402
    commit_records,
    commit_jsonl,
    inclusion_proof,
    verify_inclusion,
    verify_disclosure,
    leaf_hash,
)


def _sample(n=60):
    return [
        {
            "ts": 1700000000 + i,
            "src": f"agent-{i % 3}",
            "amount": 1000 + i * 1.5,
            "ok": (i % 2 == 0),
            "note": (None if i % 7 == 0 else f"note-{i}"),
        }
        for i in range(n)
    ]


def _values(records, col):
    return [r.get(col) for r in records]


def _zone(commitment, col):
    return next(lf.zone for lf in commitment.leaves if lf.name == col)


def test_roundtrip_all_columns():
    recs = _sample()
    c = commit_records(recs)
    assert len(c.root) == 32
    for name in c.column_names():
        proof = inclusion_proof(c, name)
        assert verify_disclosure(c.root, name, _zone(c, name), _values(recs, name), proof), name


def test_determinism_and_order_independence():
    recs = _sample()
    # Same data, different key insertion order per row -> identical root.
    shuffled = [{k: r[k] for k in reversed(list(r.keys()))} for r in recs]
    assert commit_records(recs).root == commit_records(shuffled).root
    # Re-committing is stable.
    assert commit_records(recs).root == commit_records(recs).root


def test_root_changes_on_any_value_change():
    recs = _sample()
    base = commit_records(recs).root
    tampered = [dict(r) for r in recs]
    tampered[17]["amount"] = tampered[17]["amount"] + 0.001
    assert commit_records(tampered).root != base


def test_disclosure_tamper_detected():
    recs = _sample()
    c = commit_records(recs)
    proof = inclusion_proof(c, "amount")
    good = _values(recs, "amount")
    assert verify_disclosure(c.root, "amount", _zone(c, "amount"), good, proof)
    # Flip one disclosed value -> leaf no longer matches the committed root.
    bad = list(good)
    bad[0] = bad[0] + 1
    assert not verify_disclosure(c.root, "amount", _zone(c, "amount"), bad, proof)
    # Lie about the zone map -> also rejected.
    bad_zone = dict(_zone(c, "amount"))
    bad_zone["max"] = 10 ** 9
    assert not verify_disclosure(c.root, "amount", bad_zone, good, proof)


def test_wrong_column_and_proof_fail():
    recs = _sample()
    c = commit_records(recs)
    amount_proof = inclusion_proof(c, "amount")
    # Proof name guards against substitution.
    assert not verify_disclosure(c.root, "src", _zone(c, "src"), _values(recs, "src"), amount_proof)
    # A valid 'src' leaf under the 'amount' proof path must not verify.
    src_leaf = leaf_hash("src", _zone(c, "src"), _values(recs, "src"))
    assert not verify_inclusion(c.root, src_leaf, amount_proof)


def test_jsonl_matches_records():
    import json

    recs = _sample()
    jsonl = "\n".join(json.dumps(r) for r in recs).encode("utf-8")
    assert commit_jsonl(jsonl).root == commit_records(recs).root
    # Trailing newline / blank lines tolerated.
    assert commit_jsonl(jsonl + b"\n\n").root == commit_records(recs).root


def test_single_column_and_empty():
    one = commit_records([{"x": 1}, {"x": 2}])
    assert len(one.leaves) == 1
    p = inclusion_proof(one, "x")
    assert p.siblings == []  # single leaf -> root is the leaf
    assert verify_disclosure(one.root, "x", _zone(one, "x"), [1, 2], p)
    # Empty dataset has a well-defined sentinel root, distinct from a 1-col root.
    empty = commit_records([])
    assert len(empty.root) == 32
    assert empty.root != one.root


def test_zone_exact():
    recs = _sample(10)
    c = commit_records(recs)
    z = _zone(c, "amount")
    amounts = _values(recs, "amount")
    assert z["type"] == "float"
    assert z["min"] == min(amounts) and z["max"] == max(amounts)
    assert z["count"] == 10 and z["nulls"] == 0
    # 'note' has a null every 7th row (indices 0,7 within 10 -> 2 nulls).
    zn = _zone(c, "note")
    assert zn["nulls"] == sum(1 for v in _values(recs, "note") if v is None)


def _run_all():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    passed = 0
    for t in tests:
        t()
        print(f"  PASS  {t.__name__}")
        passed += 1
    print(f"\n{passed}/{len(tests)} PCC tests passed")
    return passed == len(tests)


if __name__ == "__main__":
    sys.exit(0 if _run_all() else 1)
