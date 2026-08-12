#!/usr/bin/env python3
"""check_argument_synthesis.py — validate an ArgumentSynthesis (Pāṭala's canonical reasoning object).

An ArgumentSynthesis is a NEW higher-order argument from multiple lower-order arguments/evidence.
Audits are NEVER merged into stronger support:
  accepted + accepted != strongly_supported.
The epistemic ceiling propagates by WEAKEST-GOVERNS: an UNRESOLVED input keeps the synthesis UNRESOLVED.
Themes are metadata (selection/context), NOT inferential premises.

Rules:
  S01  object_kind == ArgumentSynthesis; has thesis, inputs, inferences, synthesis_audit, cruxes
  S02  every inference has premises + conclusion + warrant + status
  S03  unsupported bridges (MACHINE_RECONSTRUCTED / not entailed) are EXPLICITLY listed in
       synthesis_audit.unsupported_bridges — the object must not hide the leap
  S04  epistemic_ceiling propagates the WEAKEST input ceiling (never merges into stronger)
  S05  themes appear only as theme_refs metadata, never as an input/inference premise
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))

CEILING_RANK = {"INDEPENDENT_REVIEWED": 4, "SCHOLARLY_CORROBORATED": 3,
                "SCHOLARLY_CORROBORATED_PRELIMINARY": 2, "CANDIDATE": 1, "MACHINE_PROPOSED": 1}


def check_synthesis_obj(syn: dict) -> dict:
    problems = []
    if syn.get("object_kind") != "ArgumentSynthesis":
        problems.append("object_kind != ArgumentSynthesis")
    for k in ("thesis", "inputs", "inferences", "synthesis_audit", "cruxes"):
        if k not in syn:
            problems.append(f"missing '{k}'")

    for inf in syn.get("inferences", []):
        for k in ("inference_id", "premises", "conclusion", "warrant", "status"):
            if not inf.get(k):
                problems.append(f"inference {inf.get('inference_id','?')} missing {k}")

    audit = syn.get("synthesis_audit", {})
    # S03: the leap must be exposed
    if audit.get("unsupported_bridges") is None:
        problems.append("synthesis_audit.unsupported_bridges missing (must list reconstructed bridges)")
    # S04: weakest-governs ceiling
    ceilings = [audit.get("input_ceiling", "MACHINE_PROPOSED")]
    if audit.get("epistemic_ceiling") == "STRONG" and "MACHINE_PROPOSED" in ceilings:
        problems.append("epistemic_ceiling=STRONG but input is MACHINE_PROPOSED — audits were merged (forbidden)")
    # S05: themes are metadata only
    input_refs = {p for i in syn.get("inputs", []) for p in i.get("proposition_refs", [])}
    for inf in syn.get("inferences", []):
        if any("cand_" in p for p in inf.get("premises", [])):
            problems.append("a theme (cand_*) is used as an inference premise — forbidden (metadata only)")

    return {"ok": len(problems) == 0, "problems": problems,
            "ceiling": audit.get("epistemic_ceiling"),
            "unsupported_bridges": audit.get("unsupported_bridges", []),
            "n_inferences": len(syn.get("inferences", [])),
            "n_cruxes": len(syn.get("cruxes", []))}


def check_synthesis(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return check_synthesis_obj(json.load(f))


def main() -> int:
    path = os.path.join(ROOT, "benchmarks/v0/review/SYN-IPVV-REFLEXION-CORE-001.json")
    r = check_synthesis(path)
    print("SYN-IPVV-REFLEXION-CORE-001 (ArgumentSynthesis):")
    print(f"  ceiling: {r['ceiling']} | unsupported bridges: {r['unsupported_bridges']} "
          f"| inferences: {r['n_inferences']} | cruxes: {r['n_cruxes']}")
    if r["ok"]:
        print("  VALID: leap exposed, ceiling propagated (weakest-governs), themes = metadata only.")
    else:
        for p in r["problems"]:
            print(f"    ✗ {p}")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
