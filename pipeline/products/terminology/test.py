#!/usr/bin/env python3
"""products/terminology/test.py — Terminology / Lemma-through-time proof on REAL data.
Run: cd patala && python3 pipeline/products/terminology/test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))

from products.terminology.engine import lemma_history, sense_trajectory, evidence_for, lemmas  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("TERMINOLOGY / LEMMA-THROUGH-TIME — proof on REAL data\n")
    ls = lemmas()
    gate("real lemmas loaded", len(ls) >= 5, f"{len(ls)} lemmas")

    h = lemma_history("kula")
    gate("kula history found", h["found"], f"{len(h['nodes'])} nodes")
    gate("nodes carry sense_id + status", all(n.get("sense_id") and n.get("status") for n in h["nodes"]),
         "each node is a reviewable sense assertion")

    tr = sense_trajectory("kula")
    gate("trajectory ordered", len(tr["trajectory"]) >= 2, f"{len(tr['trajectory'])} periods")

    ev = evidence_for("kula")
    gate("evidence links present", len(ev["evidence"]) >= 1, f"{len(ev['evidence'])} evidence links")

    # a specific node's evidence (the Kubjikā mantra-body, with a real passage locator)
    ev2 = evidence_for("kula", "kula.kubjika.mantra-body")
    gate("node evidence resolves", len(ev2["evidence"]) >= 1,
         f"passage={ev2['evidence'][0]['target_id']} locator={ev2['evidence'][0]['locator']}")

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
