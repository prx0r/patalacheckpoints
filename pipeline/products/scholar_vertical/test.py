#!/usr/bin/env python3
"""products/scholar_vertical/test.py — the Scholar Attestation Vertical proof.
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/products/scholar_vertical/test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))

from products.scholar_vertical.engine import run_vertical  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("SCHOLAR ATTESTATION VERTICAL — proof\n")
    r = run_vertical(decision="ACCEPT", rationale="reviewed; sound")
    gate("real target reviewed", r["target"].startswith("V2-") or ":" in r["target"], r["target"])
    gate("decision submitted + attested", r["decision"]["submitted"] and r["decision"]["attested"],
         r["decision"]["review_id"] or "attested")
    gate("correction propagates", r["propagation"]["impact_potential"] >= 1,
         f"potential={r['propagation']['impact_potential']}, unaffected={r['propagation']['unaffected']}")
    gate("profile records the review", r["profile"]["n_reviews"] >= 1, f"{r['profile']['n_reviews']} reviews")
    gate("published record emitted", r["published"], "JSON-LD record published")

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
