#!/usr/bin/env python3
"""products/claim/test.py — Claim (#4) proof on REAL IPVV.
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/products/claim/test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))

from products.claim.engine import claims, gate_scope, make_claim  # noqa: E402
from products._shared import ipvv  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("CLAIM (#4) — proof on REAL IPVV\n")
    all_claims = claims()
    gate("claims from real passages", len(all_claims) >= 40, f"{len(all_claims)} claims")
    c = all_claims[0]
    gate("has text", bool(c["text"]), f"text={c['text'][:40]}...")
    gate("source-backed", len(c["source_refs"]) >= 1, f"source_ref={c['source_refs']}")
    gate("honest ceiling", c["epistemic_ceiling"] == "MACHINE_PROPOSED",
         f"PĀṬALA-INFERS stays MACHINE_PROPOSED (never inflated)")

    # source-says path raises ceiling only with a real source
    src = make_claim(ipvv.passages()[0], "SOURCE-SAYS")
    gate("SOURCE-SAYS raises to SCHOLARLY_CORROBORATED",
         src["epistemic_ceiling"] == "SCHOLARLY_CORROBORATED",
         f"ceiling={src['epistemic_ceiling']}")

    # gate: all pass (no false flags on the full body)
    gated = [gate_scope(c) for c in all_claims]
    gate("all claims pass the honesty gate", all(g["gated_ok"] for g in gated),
         f"{sum(1 for g in gated if g['gated_ok'])}/{len(gated)} gated_ok")

    # a manually-inflated claim must be flagged (the gate catches real inflation)
    fake = dict(c); fake["modality"] = "NECESSITY"; fake["_body"] = "a simple statement without modal force"
    g = gate_scope(fake)
    gate("gate flags genuine inflation", not g["gated_ok"], f"flags={g['gate_flags']}")

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
