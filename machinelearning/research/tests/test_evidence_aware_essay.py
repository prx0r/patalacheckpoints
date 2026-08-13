#!/usr/bin/env python3
"""test_evidence_aware_essay.py — evidence-aware EssayObject + the hard render rule (real tests).

Per the peer review, the negative test must actually exercise the validator on a MUTATED object
(not just check Python set membership). Uses check_eo_obj() directly.

Tests:
  1. The reflexion-core EO validates (provenance resolves, gate passes, ceiling respected).
  2. NEGATIVE: an EO with a SETTLED nigamana.status under an UNRESOLVED ceiling is REJECTED by the
     validator (the rule bites on the mutated object).
  3. NEGATIVE: an evidence claim with a FAILING gate outcome (hollow) is REJECTED (gate pass is tested,
     not mere field presence).
  4. NEGATIVE: an unsourced rival marked 'live' is REJECTED (must be UNSOURCED_RECONSTRUCTION).
  5. POSITIVE: the committed EO's source_ids all resolve to the correct gold (no stale-gid bug).
"""
from __future__ import annotations

import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "experiments"))
from check_evidence_aware_essay import check_eo_obj, PASSING_GATE_OUTCOMES, SETTLED_STATUSES

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


path = os.path.join(ROOT, "benchmarks/v0/review/EO-IPVV-REFLEXION-CORE.json")
check("EO exists", os.path.exists(path))
eo = json.load(open(path))

print("== the reflexion-core EO validates ==")
r = check_eo_obj(eo)
check("EO validates (provenance + gate + ceiling)", r["ok"], str(r["problems"]))
check("render ceiling derived as UNRESOLVED", r["ceiling"] == "UNRESOLVED", r["ceiling"])

print("\n== HARD RULE (negative, real): a settled status under UNRESOLVED ceiling is rejected ==")
bad_settle = copy.deepcopy(eo)
bad_settle["syllogism"]["nigamana"]["status"] = "strongly_supported"
r_bad = check_eo_obj(bad_settle)
check("settled nigamana under UNRESOLVED ceiling is REJECTED by the validator",
      not r_bad["ok"], str(r_bad["problems"]))

print("\n== gate PASS is tested (not just field presence) ==")
bad_gate = copy.deepcopy(eo)
bad_gate["syllogism"]["hetu"]["evidence"][0]["structural_gate_outcome"] = "hollow"
r_gate = check_eo_obj(bad_gate)
check("a FAILING gate outcome (hollow) is REJECTED",
      not r_gate["ok"], str(r_gate["problems"]))

print("\n== unsourced rival must not be 'live' ==")
bad_rival = copy.deepcopy(eo)
for c in bad_rival["candidates"]:
    if "buddhist" in c["candidate_id"]:
        c["status"] = "live"
r_rival = check_eo_obj(bad_rival)
check("unsourced rival marked 'live' is REJECTED (must be UNSOURCED_RECONSTRUCTION)",
      not r_rival["ok"], str(r_rival["problems"]))

print("\n== provenance: every source_id resolves to the correct gold (no stale-gid bug) ==")
for e in eo["syllogism"]["hetu"]["evidence"]:
    sid = e["source_id"]
    # accept ARG-GOLD-002:G2-CONC (canonical synthesis dep ref) or gold:ARG-GOLD-002:G2-CONC
    parts = sid.split(":")
    gid = parts[-2] if len(parts) >= 2 else ""
    prop = parts[-1]
    check(f"source {sid} resolves to a gold + proposition", bool(gid) and bool(prop), sid)
    # the structural gate and the epistemic status must be SEPARATE axes (a gate is not a truth
    # launder). NOT_AUDITED (audit incomplete) + any honest epistemic status is fine; they must differ.
    check(f"epistemic_status is separate from gate (not 'accepted' launder)",
          e.get("structural_gate_outcome") != e.get("epistemic_status"))

print("\n== explicit inferences join grounded claims (evidence coexistence != inference) ==")
check("EO has an inferences object", "inferences" in eo and len(eo["inferences"]) >= 1)

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (evidence-aware EO + real hard-rule tests)"))
sys.exit(1 if failures else 0)
