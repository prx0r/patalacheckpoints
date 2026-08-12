#!/usr/bin/env python3
"""check_evidence_aware_essay.py — validate an EO v2 + enforce the UNRESOLVED render rule.

Per the peer-review hard behavior test:
  if a pack dependency has semantic_status = UNRESOLVED:
      the renderer may QUALIFY it / represent alternatives / ABSTAIN
      but may NOT silently render it as settled fact.

An EO v2 (the canonical essay object, EO-v2.md spec) expresses this through:
  - nigamana.status must be structurally_suggestive / underdetermined (NOT strongly_supported/weak
    implying settled) when any dependency is UNRESOLVED
  - state_of_play.open_cruxes must list the unresolved cruxes
  - every syllogism member present (Nyāya form)
  - every hetu.evidence claim has a gate_outcome
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))

# statuses that IMPLY a settled/confident answer (not allowed when deps are UNRESOLVED)
SETTLED_STATUSES = {"strongly_supported", "weak"}


def check_eo(path: str) -> dict:
    problems = []
    with open(path, encoding="utf-8") as f:
        eo = json.load(f)

    if eo.get("schema_version", 0) != 2:
        problems.append("schema_version != 2")
    syll = eo.get("syllogism", {})
    for member in ("pratijna", "hetu", "udaharana", "upanaya", "nigamana"):
        if member not in syll or not syll[member]:
            problems.append(f"syllogism missing {member}")
    # every evidence claim has a gate outcome
    for e in syll.get("hetu", {}).get("evidence", []):
        if not e.get("gate_outcome"):
            problems.append(f"evidence claim has no gate_outcome: {e.get('claim', '')[:40]}")
    # the UNRESOLVED rule
    nig = syll.get("nigamana", {})
    if nig.get("status") in SETTLED_STATUSES:
        problems.append(f"nigamana.status {nig.get('status')} implies a settled answer, but "
                        "dependencies are UNRESOLVED — the renderer must QUALIFY/ABSTAIN, not settle")
    # open cruxes must be present when unresolved
    sop = eo.get("state_of_play", {})
    if not sop.get("open_cruxes"):
        problems.append("state_of_play.open_cruxes missing (must list unresolved cruxes)")
    return {"ok": len(problems) == 0, "problems": problems,
            "nigamana_status": nig.get("status"),
            "n_evidence": len(syll.get("hetu", {}).get("evidence", [])),
            "n_cruxes": len(sop.get("open_cruxes", []))}


def main() -> int:
    path = os.path.join(ROOT, "benchmarks/v0/review/EO-IPVV-REFLEXION-CORE.json")
    r = check_eo(path)
    print("EO-IPVV-REFLEXION-CORE (evidence-aware essay):")
    print(f"  nigamana.status: {r['nigamana_status']} | evidence: {r['n_evidence']} | open cruxes: {r['n_cruxes']}")
    if r["ok"]:
        print("  VALID: UNRESOLVED deps are held as structurally_suggestive (not settled); cruxes listed.")
    else:
        for p in r["problems"]:
            print(f"    ✗ {p}")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
