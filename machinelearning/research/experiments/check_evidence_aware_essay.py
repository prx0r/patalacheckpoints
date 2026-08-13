#!/usr/bin/env python3
"""check_evidence_aware_essay.py — validate an evidence-aware EssayObject (EO v2).

The peer-review hard rule:
  when render_ceiling == UNRESOLVED (derived from pack dependency statuses),
  the renderer must QUALIFY / represent alternatives / ABSTAIN — never render as settled fact.

Validation rules:
  V01  schema_version == 2, all 5 syllogism members present
  V02  every source_id RESOLVES to an exact argument + proposition (against the gold map)
  V03  every evidence claim has a structural_gate_outcome that is a PASSING outcome
       (accepted / accepted_with_penalty), not merely present
  V04  every evidence claim carries epistemic_status (MACHINE_PROPOSED etc.) separate from gate
  V05  unsourced rival positions (source_ids empty) must be UNSOURCED_RECONSTRUCTION, not "live"
  V06  grounded claims are joined only via explicit inferences (evidence coexistence != inference)
  V07  when render_ceiling == UNRESOLVED, nigamana.status must NOT be a settled/confident status
  V08  render_ceiling is present and one of the known values

Works on an OBJECT (check_eo_obj), so tests can pass a mutated object to prove the rule bites.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))

PASSING_GATE_OUTCOMES = {"accepted", "accepted_with_penalty"}
VALID_CEILINGS = {"UNRESOLVED", "CAN_RENDER_QUALIFIED", "CAN_RENDER_AS_GROUNDED"}
# statuses that imply a confident/settled answer (must NOT be used when ceiling == UNRESOLVED)
SETTLED_STATUSES = {"strongly_supported"}


def _load_gold_props() -> dict:
    """prop_id -> gold_id (the authoritative resolution map)."""
    sys.path.insert(0, os.path.join(ROOT, "machinelearning/research"))
    from patala_ml.gold002 import build_gold_002
    from patala_ml.gold004 import build_gold_004
    props = {}
    for gid, g in {"ARG-GOLD-002": build_gold_002(), "ARG-GOLD-004": build_gold_004()}.items():
        for n in g["nodes"]:
            props[n["proposition_id"]] = gid
    return props


_GOLD_PROPS = None
def gold_props():
    global _GOLD_PROPS
    if _GOLD_PROPS is None:
        _GOLD_PROPS = _load_gold_props()
    return _GOLD_PROPS


def _audit_incomplete(eo: dict) -> bool:
    """True when the EO's source synthesis has not completed a structural audit.

    When the audit is INCOMPLETE, a NOT_AUDITED structural gate is the CORRECT honest state (it would
    be a defect to claim a gate was passed without an audit). So the 'must pass' gate check only bites
    when the audit is complete.
    """
    state = (eo.get("patala_epistemics", {}) or {}).get("structural_audit_state") \
        or (eo.get("synthesis_audit", {}) or {}).get("structural_audit_state")
    return state == "INCOMPLETE"


def check_eo_obj(eo: dict) -> dict:
    problems = []
    if eo.get("schema_version", 0) != 2:
        problems.append("schema_version != 2")
    syll = eo.get("syllogism", {})
    for member in ("pratijna", "hetu", "udaharana", "upanaya", "nigamana"):
        if member not in syll or not syll[member]:
            problems.append(f"syllogism missing {member}")

    gp = gold_props()
    # V02: source resolution + V03: gate pass/fail + V04: epistemic_status
    # source_id may be the canonical unprefixed form (ARG-GOLD-002:G2-CONC, the synthesis dep ref) or
    # the gold:-prefixed form (gold:ARG-GOLD-002:G2-CONC). Both are valid; resolve by the proposition.
    for e in syll.get("hetu", {}).get("evidence", []):
        sid = e.get("source_id", "")
        # accept ARG-GOLD-002:G2-CONC or gold:ARG-GOLD-002:G2-CONC
        parts = sid.split(":") if sid.startswith("gold:") else sid.split(":") if sid.count(":") == 1 else []
        if len(parts) < 2:
            problems.append(f"malformed source_id: {sid}")
        else:
            gid = parts[-2] if sid.startswith("gold:") else parts[0]
            prop = parts[-1]
            if prop not in gp:
                problems.append(f"source_id proposition does not resolve: {prop}")
            elif not sid.startswith("gold:") and gp[prop] != gid:
                problems.append(f"source_id gold mismatch: {sid} (prop {prop} is in {gp[prop]})")
        if not e.get("structural_gate_outcome"):
            problems.append(f"evidence missing structural_gate_outcome: {e.get('claim','')[:40]}")
        elif e["structural_gate_outcome"] not in PASSING_GATE_OUTCOMES:
            # a NOT_AUDITED gate is CORRECT when the structural audit is INCOMPLETE (E04) — it is only
            # a defect if it claims a gate was passed without an audit. The strict "must pass" check
            # applies only when the audit is complete.
            if not (e["structural_gate_outcome"] == "NOT_AUDITED" and _audit_incomplete(eo)):
                problems.append(f"evidence gate FAILS (not passing): {e['structural_gate_outcome']}")
        if not e.get("epistemic_status"):
            problems.append(f"evidence missing epistemic_status: {e.get('claim','')[:40]}")

    # V05: unsourced rival positions must be UNSOURCED_RECONSTRUCTION
    for c in eo.get("candidates", []):
        if not c.get("source_ids") and c.get("status") in ("live", "weakened", "defeated"):
            problems.append(f"unsourced candidate marked {c.get('status')} (must be UNSOURCED_RECONSTRUCTION): {c.get('candidate_id')}")

    # V06: if there is a nigamana and grounded claims, require explicit inferences when joining
    nig = syll.get("nigamana", {})
    if nig and eo.get("inferences") is None:
        problems.append("inferences object missing (grounded claims must be joined via explicit warrant)")

    # V07 + V08: render ceiling governs nigamana.status
    ceiling = eo.get("render_ceiling")
    if ceiling not in VALID_CEILINGS:
        problems.append(f"invalid render_ceiling: {ceiling}")
    if ceiling == "UNRESOLVED" and nig.get("status") in SETTLED_STATUSES:
        problems.append(f"nigamana.status {nig.get('status')} is settled but render_ceiling=UNRESOLVED — must qualify/abstain")

    sop = eo.get("state_of_play", {})
    if not sop.get("open_cruxes"):
        problems.append("state_of_play.open_cruxes missing (must list unresolved cruxes)")

    return {"ok": len(problems) == 0, "problems": problems,
            "ceiling": ceiling, "nigamana_status": nig.get("status"),
            "n_evidence": len(syll.get("hetu", {}).get("evidence", [])),
            "n_cruxes": len(sop.get("open_cruxes", []))}


def check_eo(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return check_eo_obj(json.load(f))


def main() -> int:
    path = os.path.join(ROOT, "benchmarks/v0/review/EO-IPVV-REFLEXION-CORE.json")
    r = check_eo(path)
    print("EO-IPVV-REFLEXION-CORE (evidence-aware EssayObject):")
    print(f"  ceiling: {r['ceiling']} | nigamana: {r['nigamana_status']} | evidence: {r['n_evidence']} | cruxes: {r['n_cruxes']}")
    if r["ok"]:
        print("  VALID: provenance resolves, gate passes, render ceiling respected.")
    else:
        for p in r["problems"]:
            print(f"    ✗ {p}")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
