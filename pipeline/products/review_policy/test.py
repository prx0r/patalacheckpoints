#!/usr/bin/env python3
"""products/review_policy/test.py — review-policy proof.
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/products/review_policy/test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))

from products.review_policy.engine import grants, can_promote, policy_summary  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("REVIEW POLICY — proof\n")
    g_scholar = grants("ACCEPT", "scholar")
    gate("scholar ACCEPT -> SINGLE_REVIEWED", g_scholar["resulting_state"] == "SINGLE_REVIEWED",
         g_scholar["grant"])
    g_machine = grants("ACCEPT", "machine")
    gate("machine ACCEPT -> no promotion (BLOCKED)", g_machine["grant"] == "CANDIDATE"
         or g_machine["grant"] == "BLOCKED", g_machine["grant"])
    g_reject = grants("REJECT", "scholar")
    gate("scholar REJECT -> REJECTED", g_reject["resulting_state"] == "REJECTED", g_reject["grant"])

    cp = can_promote("machine", "ADJUDICATED")
    gate("machine CANNOT adjudicate", not cp["allowed"], cp["note"])
    cp2 = can_promote("adjudicator", "ADJUDICATED")
    gate("adjudicator CAN adjudicate", cp2["allowed"], cp2["note"])

    s = policy_summary()
    gate("invariant declared", "authority(projection)" in s["invariant"], "policy preserves the invariant")
    gate("top rungs require human", s["top_rungs_require_human"], "ADJUDICATED needs a human")

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
