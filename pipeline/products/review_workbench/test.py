#!/usr/bin/env python3
"""products/review_workbench/test.py — review-workbench proof on real objects.
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/products/review_workbench/test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))

from products.review_workbench.engine import open_workbench, decide  # noqa: E402
from products.scholar_identity.engine import register, verify_orcid, _new_ed25519_keypair  # noqa: E402
from products.scholar_review.engine import ScholarProduct  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("REVIEW WORKBENCH — proof on real objects\n")
    sp = ScholarProduct()
    ref = sp.list_objects(layer="C1")[0]["id"]
    priv, pub = _new_ed25519_keypair()
    ident = verify_orcid(register("0000-0000-0000-0000", "Scholar X", ["all"],
                                  public_key=pub.decode()))
    ident["_private_key"] = priv

    wb = open_workbench(ref, ident)
    gate("opens a real object", wb["target_ref"] == ref, ref)
    gate("shows downstream impact", "downstream" in wb and len(wb["downstream"]) >= 1,
         "impact present")
    gate("authorized scholar sees decisions", wb["decision_surface"]["decisions"] != [],
         f"{len(wb['decision_surface']['decisions'])} decisions")

    dec = decide(ref, ident, "ACCEPT", "sound", sign=True)
    gate("decision submitted through gate", dec["submitted"], dec["review"]["review_id"])
    gate("decision signed (attestation)", "attestation" in dec, "Ed25519 attestation")

    # a scholar out of scope cannot decide
    other = verify_orcid(register("0000-0003-0000-0001", "Scholar Y", ["timeline"]))
    dec2 = decide(ref, other, "ACCEPT", "x")
    gate("out-of-scope scholar blocked", not dec2["submitted"], dec2.get("error", ""))

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
