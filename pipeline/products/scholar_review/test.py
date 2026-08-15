#!/usr/bin/env python3
"""products/scholar_review/test.py — the Review + Attestation + Audit proof on REAL IPVV.

Run: cd patala && python3 -m products.scholar_review.test   (or PYTHONPATH=pipeline python3 products/scholar_review/test.py)
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "pipeline"))

from products.scholar_review.engine import ScholarProduct, verify_attestation  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("SCHOLAR REVIEW + ATTESTATION + AUDIT — proof on REAL IPVV\n")
    sp = ScholarProduct(readonly=True)

    print("1. HYDRATION")
    objs = sp.list_objects()
    gate("real objects hydrated", len(objs) >= 80, f"{len(objs)} reviewable objects")
    layers = sp.audit()["layers"]
    gate("real derivation spine", "ARGUMENT" in layers and "L200" in layers, f"layers={list(layers)}")

    print("\n2. ADVERSARIAL PANEL")
    ref = [o for o in objs if o["layer"] == "C1"][0]["id"]
    p = sp.panel_review(ref, ["r1", "r2", "r3"], "j1", findings=[
        {"reviewer": "r1", "opinion": "SUPPORT"},
        {"reviewer": "r2", "opinion": "SUPPORT"},
        {"reviewer": "r3", "opinion": "CONCERN", "severity": "BLOCKING"}])
    gate("blocking -> BLOCKED", p["verdict"]["verdict"] == "BLOCKED", f"verdict={p['verdict']['verdict']}")
    gate("dissent surfaced", len(p["verdict"]["dissent"]) == 1, "minority dissent not forced")

    print("\n3. AUTHORIZATION")
    try:
        sp.submit_review("agent", "machine", "*", ref, "ACCEPT", "x")
        gate("machine cannot promote", False, "FORBIDDEN should raise")
    except PermissionError:
        gate("machine cannot promote", True, "machine actor forbidden")
    sub = sp.submit_review("scholar-A", "scholar", "*", ref, "ACCEPT", "sound")
    gate("scholar can submit", sub["review"]["reviewer_kind"] == "scholar", "scoped review accepted")

    print("\n4. SIGNED ATTESTATION")
    att = sp.attest(ref, "scholar-A", "ACCEPT_WITH_QUALIFICATIONS", "reviewed")
    ok, why = att["verified"]
    gate("attestation signed + verified", ok, f"{att['attestation']['attestation_id']} ({why})")
    tampered = dict(att["attestation"]); tampered["rationale"] = "tampered"
    gate("tamper detected", verify_attestation(tampered)[0] is False, "content change breaks hash")

    print("\n5. SIMULATION (zero-write)")
    fresh = [o for o in objs if o["layer"] == "L2"][0]["id"]
    sp.simulate_review(fresh, "REJECT")
    gate("simulation does not mutate", sp.object_state(fresh)["effective_state"] == "CANDIDATE",
         f"state={sp.object_state(fresh)['effective_state']}")

    print("\n6. AUDIT")
    audit = sp.audit()
    gate("audit resolves all", audit["objects"] >= 80, f"{audit['objects']} objects")
    gate("attestations verifiable", audit["attestations_verified"] >= 1,
         f"{audit['attestations_verified']} verified")

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
