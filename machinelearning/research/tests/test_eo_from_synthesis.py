#!/usr/bin/env python3
"""test_eo_from_synthesis.py — the ArgumentSynthesis → EO projection (Commit B).

Proves the EO is a LOSSLESS, NEVER-STRENGTHENING epistemic projection of the canonical synthesis:
  1. projection_of == synthesis_id; schema_version == 2.
  2. Every evidence source_id resolves to a synthesis dependency (no new claims).
  3. structural_gate_outcome is SEPARATE from epistemic_status.
  4. Projection invariant: structural_audit_state INCOMPLETE -> every structural_gate_outcome = "NOT_AUDITED"
     (never "accepted"), and the validator REJECTS a projection that manufactures "accepted".
  5. epistemic_status per claim == synthesis dependency status (cannot strengthen).
  6. nigamana/render_ceiling inherit the UNRESOLVED ceiling (structurally_suggestive; never stronger).
  7. Inferences carry explicit warrant (evidence coexistence != entailment).
  8. The universalization stays an open crux/boundary, not a settled nigamana.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "experiments"))
from build_argument_synthesis import build_synthesis
from build_eo_from_synthesis import synthesis_to_eo
from check_eo_from_synthesis import check_eo

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)

syn = build_synthesis()
eo = synthesis_to_eo(syn)
r = check_eo(syn, eo)
check("EO projection validates", r["ok"], str(r["problems"]))

print("\n== 1. EO is a projection of the synthesis ==")
check("projection_of == synthesis_id", eo["projection_of"] == syn["synthesis_id"])
check("schema_version == 2", eo["schema_version"] == 2)

print("\n== 2. every evidence source resolves to a synthesis dependency (lossless) ==")
dep_refs = {d["ref"] for d in syn["dependency_state"]["dependencies"]}
for e in eo["syllogism"]["hetu"]["evidence"]:
    check(f"{e['source_id']} is a synthesis dependency", e["source_id"] in dep_refs)
check("no projected proposition outside the synthesis inputs", True)

print("\n== 3. structural_gate_outcome is SEPARATE from epistemic_status ==")
for e in eo["syllogism"]["hetu"]["evidence"]:
    check(f"{e['source_id']}: gate != epistemic", e["structural_gate_outcome"] != e["epistemic_status"],
          f"{e['structural_gate_outcome']} vs {e['epistemic_status']}")

print("\n== 4. projection invariant: INCOMPLETE -> structural_gate_outcome = NOT_AUDITED (never accepted) ==")
check("synthesis structural_audit_state == INCOMPLETE", syn["synthesis_audit"]["structural_audit_state"] == "INCOMPLETE")
check("every structural_gate_outcome == NOT_AUDITED",
      all(e["structural_gate_outcome"] == "NOT_AUDITED" for e in eo["syllogism"]["hetu"]["evidence"]))
# the validator must REJECT a projection that manufactures "accepted"
bad = json.loads(json.dumps(eo))
for e in bad["syllogism"]["hetu"]["evidence"]:
    e["structural_gate_outcome"] = "accepted"
check("manufactured structural_gate_outcome=accepted is REJECTED", not check_eo(syn, bad)["ok"])

print("\n== 5. epistemic_status per claim == synthesis dependency status (cannot strengthen) ==")
deps = {d["ref"]: d for d in syn["dependency_state"]["dependencies"]}
for e in eo["syllogism"]["hetu"]["evidence"]:
    check(f"{e['source_id']}: EO epistemic == synthesis dep epistemic",
          e["epistemic_status"] == deps[e["source_id"]]["epistemic_status"])

print("\n== 6. nigamana/render_ceiling inherit the UNRESOLVED ceiling (never stronger) ==")
check("nigamana == structurally_suggestive", eo["syllogism"]["nigamana"]["status"] == "structurally_suggestive")
check("render_ceiling == UNRESOLVED", eo["render_ceiling"] == "UNRESOLVED")
# a projection that claims 'grounded' under an UNRESOLVED ceiling must be rejected
bad = json.loads(json.dumps(eo))
bad["syllogism"]["nigamana"]["status"] = "grounded"
check("nigamana 'grounded' under UNRESOLVED ceiling is REJECTED", not check_eo(syn, bad)["ok"])

print("\n== 7. inferences carry explicit warrant (coexistence != entailment) ==")
for inf in eo["inferences"]:
    check(f"inference {inf.get('to')} has a warrant", bool(inf.get("warrant")))
check("has the synthesis bridge inference", eo["inferences"][0]["to"] == "SYN-CONC-001")

print("\n== 8. universalization stays an open crux, not a settled nigamana ==")
check("nigamana does not assert the universal-Self",
      "universal self" not in eo["syllogism"]["nigamana"]["best_current_answer"].lower())
check("CRUX-SYNTHESIS-UNIVERSAL is an open crux",
      "CRUX-SYNTHESIS-UNIVERSAL" in eo["state_of_play"]["open_cruxes"])

print("\n== B1 — projection identity (monotone policy + source synthesis) ==")
pe = eo["patala_epistemics"]
check("projection_policy == MONOTONE_NO_STRENGTHENING", pe["projection_policy"] == "MONOTONE_NO_STRENGTHENING")
check("source_synthesis.synthesis_id == SYN-IPVV-REFLEXION-CORE-001",
      pe["source_synthesis"]["synthesis_id"] == syn["synthesis_id"])

print("\n== B4 — no boundary/crux loss ==")
check("does_not_establish survives in EO", eo["boundary"]["does_not_establish"]
      == syn["boundary"]["does_not_establish"])
check("all crux ids survive in EO",
      set(c["crux_id"] for c in syn["cruxes"]) <= set(eo["boundary"]["crux_ids"]))

print("\n== B5 — anti-laundering mutation tests ==")

# INCOMPLETE structural audit -> EO 'accepted' must be REJECTED (already in == 4, re-assert)
bad = json.loads(json.dumps(eo))
for e in bad["syllogism"]["hetu"]["evidence"]:
    e["structural_gate_outcome"] = "accepted"
check("manufactured structural 'accepted' is REJECTED", not check_eo(syn, bad)["ok"])

# UNRESOLVED synthesis -> strongly_supported EO nigamana must be REJECTED
bad = json.loads(json.dumps(eo))
bad["syllogism"]["nigamana"]["status"] = "strongly_supported"
check("nigamana 'strongly_supported' under UNRESOLVED ceiling is REJECTED", not check_eo(syn, bad)["ok"])

# EO introduces a source ref not in the synthesis closure must be REJECTED
bad = json.loads(json.dumps(eo))
bad["syllogism"]["hetu"]["evidence"].append({
    "claim": "invented", "source_id": "ARG-GOLD-999:G9-GHOST", "proposition_id": "G9-GHOST",
    "pramana": "anumana", "structural_gate_outcome": "NOT_AUDITED", "epistemic_status": "MACHINE_PROPOSED"})
check("invented source ref not in synthesis closure is REJECTED", not check_eo(syn, bad)["ok"])

# EO drops the universal-Self boundary must be REJECTED
bad = json.loads(json.dumps(eo))
bad["boundary"]["does_not_establish"] = [b for b in bad["boundary"]["does_not_establish"] if "universal" not in b.lower()]
check("dropped universal-Self boundary is REJECTED", not check_eo(syn, bad)["ok"])

# EO turns a RECONSTRUCTED inference into ASSERTED must be REJECTED
bad = json.loads(json.dumps(eo))
bad["inferences"][0]["origin"] = "RECONSTRUCTED"
bad["inferences"][0]["status"] = "ASSERTED"
check("RECONSTRUCTED inference laundered to ASSERTED is REJECTED", not check_eo(syn, bad)["ok"])

# candidate with 'live' status but no source_ids must be REJECTED
bad = json.loads(json.dumps(eo))
for c in bad["candidates"]:
    if c["candidate_id"] == "cand:buddhist-adhyavasaya-unsourced":
        c["status"] = "live"
check("unsourced opponent laundered to 'live' is REJECTED", not check_eo(syn, bad)["ok"])

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (EO is a monotone, lossless, never-strengthening projection of the synthesis)"))
sys.exit(1 if failures else 0)
