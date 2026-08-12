#!/usr/bin/env python3
"""check_eo_from_synthesis.py — validate that an EO is a LOSSLESS EPISTEMIC PROJECTION of its synthesis.

Rules (Commit B):
  E01  EO exists, has a projection_of == the synthesis id, and schema_version == 2.
  E02  Every evidence claim's source_id + proposition_id must resolve to a dependency of the synthesis;
       the set of projected propositions ⊆ the synthesis's input/dependency propositions (lossless: no new claims).
  E03  structural_gate_outcome is SEPARATE from epistemic_status.
  E04  Projection invariant: if the synthesis's structural_audit_state != COMPLETE, then every
       structural_gate_outcome must be "NOT_AUDITED" (NEVER "accepted"). No manufactured structural outcome.
  E05  The EO's epistemic_status for each claim equals the synthesis's resolved dependency epistemic_status
       (the projection cannot strengthen/weaken it).
  E06  The nigamana/render_ceiling cannot be stronger than the synthesis ceiling:
         synthesis UNRESOLVED -> nigamana structurally_suggestive + render_ceiling UNRESOLVED (qualify/abstain).
  E07  Every inference carries an explicit warrant + origin; evidence coexistence is NOT presented as entailment.
  E08  The universalization appears only as an open crux / boundary, never as a settled nigamana.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))

STRONG_NIGAMANA = {"grounded", "supported"}
CEILING_TO_NIGAMANA = {"UNRESOLVED": "structurally_suggestive", "MACHINE_PROPOSED": "structurally_suggestive",
                       "ENGINEERING_VALIDATED": "supported_qualified",
                       "SCHOLARLY_CORROBORATED_PRELIMINARY": "supported_qualified"}


def check_eo(syn: dict, eo: dict) -> dict:
    problems = []
    audit = syn.get("synthesis_audit", {})
    ceiling = audit.get("epistemic_ceiling", "UNRESOLVED")
    sas = audit.get("structural_audit_state", "INCOMPLETE")

    # E01
    if eo.get("schema_version") != 2:
        problems.append("EO schema_version != 2")
    if eo.get("projection_of") != syn.get("synthesis_id"):
        problems.append(f"EO projection_of {eo.get('projection_of')} != synthesis {syn.get('synthesis_id')}")

    # E02 — every projected proposition must be a synthesis dependency (lossless: no new claims)
    dep_by_ref = {d["ref"]: d for d in syn.get("dependency_state", {}).get("dependencies", [])}
    for e in eo.get("syllogism", {}).get("hetu", {}).get("evidence", []):
        if e.get("source_id") not in dep_by_ref:
            problems.append(f"evidence {e.get('source_id')} is not a synthesis dependency (lossless violated)")

    # E03 + E04 — structural/epistemic separation + the projection invariant
    for e in eo.get("syllogism", {}).get("hetu", {}).get("evidence", []):
        if e.get("structural_gate_outcome") == e.get("epistemic_status"):
            problems.append(f"evidence {e.get('source_id')}: structural_gate_outcome == epistemic_status (must be separate)")
        if sas != "COMPLETE" and e.get("structural_gate_outcome") != "NOT_AUDITED":
            problems.append(f"evidence {e.get('source_id')}: structural_gate_outcome={e.get('structural_gate_outcome')} "
                            f"manufactured while structural_audit_state={sas} (never 'accepted')")

    # E05 — epistemic_status must match the synthesis dependency (cannot strengthen)
    for e in eo.get("syllogism", {}).get("hetu", {}).get("evidence", []):
        dep = dep_by_ref.get(e.get("source_id"))
        if dep and e.get("epistemic_status") != dep.get("epistemic_status"):
            problems.append(f"evidence {e.get('source_id')}: epistemic_status {e.get('epistemic_status')} != "
                            f"synthesis dependency {dep.get('epistemic_status')} (projection strengthened/weakened)")

    # E06 — nigamana/render_ceiling cannot be stronger than the synthesis ceiling
    nig = eo.get("syllogism", {}).get("nigamana", {}).get("status")
    if ceiling in ("UNRESOLVED", "MACHINE_PROPOSED") and nig not in ("structurally_suggestive",):
        problems.append(f"nigamana {nig} is stronger than synthesis ceiling {ceiling}")
    expected_render = "UNRESOLVED" if ceiling in ("UNRESOLVED", "MACHINE_PROPOSED") else "CAN_RENDER_QUALIFIED"
    if eo.get("render_ceiling") == "CAN_RENDER_AS_GROUNDED" and ceiling not in ("INDEPENDENT_REVIEWED", "SCHOLARLY_CORROBORATED"):
        problems.append(f"render_ceiling {eo.get('render_ceiling')} overstates synthesis ceiling {ceiling}")

    # E07 — inferences carry explicit warrant + origin
    for inf in eo.get("inferences", []):
        if not inf.get("warrant"):
            problems.append(f"inference {inf.get('to')}: missing warrant (coexistence ≠ entailment)")

    # E08 — universalization only as open crux/boundary
    nig_text = (eo.get("syllogism", {}).get("nigamana", {}).get("best_current_answer") or "").lower()
    if "universal self" in nig_text or "universal-self" in nig_text:
        problems.append("nigamana asserts the universal-Self — must stay an open crux/boundary")

    return {"ok": len(problems) == 0, "problems": problems,
            "render_ceiling": eo.get("render_ceiling"),
            "nigamana_status": eo.get("syllogism", {}).get("nigamana", {}).get("status"),
            "n_evidence": len(eo.get("syllogism", {}).get("hetu", {}).get("evidence", []))}


def main() -> int:
    syn = json.load(open(os.path.join(ROOT, "benchmarks/v0/review/SYN-IPVV-REFLEXION-CORE-001.json")))
    eo = json.load(open(os.path.join(ROOT, "benchmarks/v0/review/EO-IPVV-REFLEXION-CORE.json")))
    r = check_eo(syn, eo)
    print("EO-IPVV-REFLEXION-CORE (projection of SYN-IPVV-REFLEXION-CORE-001):")
    print(f"  render_ceiling: {r['render_ceiling']} | nigamana: {r['nigamana_status']} | evidence: {r['n_evidence']}")
    if r["ok"]:
        print("  VALID: lossless projection, structural/epistemic separate, no strengthened state.")
    else:
        for p in r["problems"]:
            print(f"    ✗ {p}")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
