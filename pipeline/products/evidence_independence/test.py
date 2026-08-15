#!/usr/bin/env python3
"""products/evidence_independence/test.py — evidence-independence proof on REAL corroboration data.
Run: cd patala && python3 pipeline/products/evidence_independence/test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))
sys.path.insert(0, str(ROOT))

from products.evidence_independence.engine import independence_report, corroborated_propositions  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("EVIDENCE INDEPENDENCE — proof on REAL corroboration registry\n")
    props = corroborated_propositions()
    gate("real corroborations found", len(props) >= 1, f"{len(props)} corroborated proposition(s)")

    r = independence_report(live=False)
    gate("offline report OK", r["status"] == "OK", f"status={r['status']}")
    p = r["propositions"][0]
    gate("duplicates detected", p["duplicate_sources"] >= 1,
         f"recorded={p['n_corroborations_recorded']}, unique={p['n_unique_sources']}, dupes={p['duplicate_sources']}")
    gate("unique sources classified", p["n_unique_sources"] == len(p["independence"]["per_source"]),
         f"{p['n_unique_sources']} sources, {len(p['independence']['per_source'])} classified")
    gate("independence values valid", all(s["independence"] in
         ("INDEPENDENT_AUTHOR", "DERIVED_CITATION", "SAME_AUTHOR", "UNKNOWN")
         for s in p["independence"]["per_source"]),
         "each source classified honestly")

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
