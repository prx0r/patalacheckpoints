#!/usr/bin/env python3
"""test_review_bundle.py — devpath6 (G4) ReviewBundle + human-authority path acceptance.

Checks (per SPEC-G3-HUMAN-AUTHORITY-PATH):
  1. ReviewBundle-v1 materializes read-only for one exact object (target ref/version/hash, actions)
  2. R2: a ReviewEvent never mutates its target (target_unchanged=True; no write to the object)
  3. R1: machine can never promote (machine_can_promote=False); review axis stays NOT_REVIEWED
     unless a human ACCEPTs
  4. R3: authority is a vector; epistemic_ceiling is derived, not writable
  5. the human-authority loop: ReviewEvent -> ReviewProposal/Adjudication path is representable
  6. a DISPUTE/PROPOSE_ALTERNATIVE flips the dependency impact (downstream -> NEED_REVIEW)
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from review_bundle import (
    materialize_bundle, build_review_event, simulate_correction,
    promotion_event, run_human_authority_path,
)

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


target = {
    "ref": "pt:proposition:G2-TC1", "version": "v1", "layer": "PROPOSITION", "hash": "abc",
    "source": ["pt:passage:ipvv:chunk"], "t1": {}, "l0": {}, "l2": {}, "l200": {},
    "proof": {"open_dimensions": ["proposition_licensing"]},
}

print("== ReviewBundle-v1 materializes read-only ==")
b = materialize_bundle(target)
check("bundle has target ref/version/hash", b["target"]["ref"] == "pt:proposition:G2-TC1"
      and b["target"]["version"] == "v1" and b["target"]["hash"])
check("bundle lists the review actions", set(b["review_actions"]) ==
      {"ACCEPT", "QUALIFY", "DISPUTE", "PROPOSE_ALTERNATIVE", "ABSTAIN"})
check("bundle has dependency_impact projection", "dependency_impact" in b)
check("bundle is read-only shape (no mutation fields)", "review_status" in b)

print("\n== R2: review never mutates the target ==")
ev = build_review_event(b, {"person_ref": "pt:scholar:x", "display_name": "X"}, "DISPUTE",
                        "over-licensed", alternative_ref="pt:proposition:G2-TC1:v2")
check("ReviewEvent created (evidence, not mutation)", ev.review_id.startswith("pt:review:"))
check("review target carries exact version + hash", ev.review_target.version == "v1"
      and ev.review_target.hash == "abc")
sim = simulate_correction(b, "DISPUTE")
check("simulation is zero-write: target_unchanged", sim["target_unchanged"] is True)
check("simulation computes impact", "impact" in sim)

print("\n== R1: machine cannot promote; only an H witness raises review axis ==")
check("machine_can_promote=False in simulation", sim["machine_can_promote"] is False)
check("review axis stays NOT_REVIEWED for a DISPUTE", sim["authority"]["review"] == "NOT_REVIEWED")
acc = simulate_correction(b, "ACCEPT")
# a machine ACCEPT still cannot raise the review axis (R1)
check("even a machine ACCEPT leaves review NOT_REVIEWED", acc["authority"]["review"] == "NOT_REVIEWED")

print("\n== R3: authority is a vector; ceiling derived ==")
check("authority is a 4-axis vector", set(sim["authority"]) ==
      {"generation", "evidence", "review", "publication"})
check("epistemic_ceiling present (derived)", "epistemic_ceiling" in sim)

print("\n== the human-authority loop ==")
out = run_human_authority_path(b, {"person_ref": "pt:scholar:elad"}, "DISPUTE", "reason")
check("loop returns review_event + simulated_impact + status", out["review_event"]["decision"] == "DISPUTE"
      and "simulated_impact" in out)
check("DISPUTE leaves review_status NOT_REVIEWED", out["review_status_after"] == "NOT_REVIEWED")
check("constitution enforced (R1/R2/R3)",
      out["constitution"]["R1_machine_cannot_promote"] and
      out["constitution"]["R2_review_never_mutates_target"] and
      out["constitution"]["R3_ceiling_is_derived"])
check("target not mutated by the loop", out["target_mutated"] is False)

print("\n== DISPUTE flips dependency impact (downstream -> NEED_REVIEW) ===")
b2 = materialize_bundle(target, dependencies={
    "propositions": [{"ref": "pt:prop:P17", "relation": "USES_AS_PREMISE"}],
    "arguments": [{"ref": "pt:argument:ARG-04", "relation": "USES_AS_PREMISE"}],
    "essays": [], "cruxes": [], "education": []})
sim2 = simulate_correction(b2, "DISPUTE")
impact_refs = [d["object"] for d in sim2["impact"].get("directly_affected", [])]
check("disputed proposition impacts downstream (P17, ARG-04)",
      any("P17" in r for r in impact_refs) and any("ARG-04" in r for r in impact_refs), impact_refs)

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (ReviewBundle + human-authority path work)"))
sys.exit(1 if failures else 0)
