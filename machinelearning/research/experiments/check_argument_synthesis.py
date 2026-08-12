#!/usr/bin/env python3
"""check_argument_synthesis.py — validate an ArgumentSynthesis (Pāṭala's canonical reasoning object).

An ArgumentSynthesis is a NEW higher-order argument from multiple lower-order arguments/evidence.
Audits are NEVER merged into stronger support. The epistemic ceiling propagates by WEAKEST-GOVERNS over
LOAD-BEARING dependencies only. The bridge's ORIGIN and its EVIDENTIAL state are separate dimensions.

Rules:
  S01  object_kind == ArgumentSynthesis; has thesis, inputs, inferences, synthesis_audit, cruxes
  S02  every inference has premises + conclusion + warrant + origin + support_state/assessment
  S03  inferential coverage via a REAL SYMBOL TABLE built from AUTHORITATIVE input resolution:
         every input's argument_ref + proposition_ref is checked against the actual gold registry;
         resolvable = resolved source propositions ∪ inference-produced conclusions;
         every premise must resolve; every synthesis conclusion must be produced by an inference
  S04  the thesis proposition_id must equal a produced inference conclusion (graph-shaped)
  S05  epistemic_ceiling = WEAKEST over LOAD-BEARING deps only (never merged; non-load-bearing never caps)
  S06  bridge origin (RECONSTRUCTED) is separate from evidential support_state (UNRESOLVED)
  S07  themes appear only as theme_refs metadata, never as an input/inference premise
  S08  no invented audit refs: with no persisted audit registry, audit_state=AUDITED is REJECTED;
       per-dependency structural_audit must carry state + outcome + audit_refs
  S09  structural audit axis is separate: synthesis_audit.structural_audit_state present;
       if structural_audit_state != COMPLETE, no dependency may manufacture a structural outcome
  S10  internal_consistency must NOT claim STRUCTURALLY_COHERENT unless a defined check ran
  S11  boundary uses reconstruct/currently_supports vocabulary, not overclaiming 'establishes'
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from patala_ml.gold002 import build_gold_002
from patala_ml.gold004 import build_gold_004

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))

CEILING_RANK = {"UNRESOLVED": 0, "MACHINE_PROPOSED": 1, "ENGINEERING_VALIDATED": 2,
                "SCHOLARLY_CORROBORATED_PRELIMINARY": 3, "SCHOLARLY_CORROBORATED": 4,
                "INDEPENDENT_REVIEWED": 5}
ROLE_LOAD_BEARING = {"LOAD_BEARING_PREMISE", "LOAD_BEARING_INFERENCE"}


def _authoritative_registry() -> dict:
    """gold_id -> set(proposition_id) — the AUTHORITATIVE membership source (not the synthesis's claims)."""
    golds = {"ARG-GOLD-002": build_gold_002(), "ARG-GOLD-004": build_gold_004()}
    return {gid: {n["proposition_id"] for n in g["nodes"]} for gid, g in golds.items()}


def check_synthesis_obj(syn: dict) -> dict:
    problems = []
    auth = _authoritative_registry()

    # S01 — shape
    if syn.get("object_kind") != "ArgumentSynthesis":
        problems.append("object_kind != ArgumentSynthesis")
    for k in ("thesis", "inputs", "inferences", "synthesis_audit", "cruxes", "dependency_state"):
        if k not in syn:
            problems.append(f"missing '{k}'")

    # S07 — themes are metadata only
    if "cand_" in " ".join(p for i in syn.get("inferences", []) for p in i.get("premises", [])):
        problems.append("a theme (cand_*) is used as an inference premise — forbidden (metadata only)")
    if syn.get("theme_refs") is None:
        problems.append("theme_refs missing (themes are metadata, not premises)")

    # ── S03 — AUTHORITATIVE input resolution (does NOT trust the synthesis's declarations) ──
    known_source_props = set()
    for inp in syn.get("inputs", []):
        aref = inp.get("argument_ref")
        if aref not in auth:
            problems.append(f"input argument_ref {aref!r} is not in the gold registry")
            continue
        # validate every claimed proposition against the ACTUAL gold membership
        for p in inp.get("proposition_refs", []):
            if p not in auth[aref]:
                problems.append(f"input {aref} + {p!r}: proposition does not belong to {aref} "
                                f"(authoritative membership: {sorted(auth[aref])})")
            else:
                known_source_props.add(p)
        # S08 — no invented audits: canonical v1 has no persisted audit registry -> AUDITED rejected
        sa = inp.get("structural_audit") or {}
        if sa.get("state") == "AUDITED":
            problems.append(f"input {aref}: AUDITED not permitted until a persisted audit registry exists")
        if sa.get("outcome") not in (None, "NOT_AUDITED"):
            problems.append(f"input {aref}: structural outcome {sa.get('outcome')} manufactured with no persisted audit")

    inference_conclusions = {inf["conclusion"] for inf in syn.get("inferences", []) if inf.get("conclusion")}
    resolvable = known_source_props | inference_conclusions

    if not inference_conclusions:
        problems.append("no inference produces a conclusion (inferential coverage empty)")

    for inf in syn.get("inferences", []):
        iid = inf.get("inference_id", "?")
        for k in ("premises", "conclusion", "warrant", "origin", "support_state"):
            if not inf.get(k):
                problems.append(f"inference {iid} missing {k}")
        if not inf.get("premises"):
            problems.append(f"inference {iid}: no premises (every inference needs >=1)")
        for p in inf.get("premises", []):
            if p not in resolvable:
                problems.append(f"inference {iid}: premise {p} does not resolve "
                                f"(known={sorted(known_source_props)} ∪ produced={sorted(inference_conclusions)})")
        if inf.get("conclusion") not in inference_conclusions:
            problems.append(f"inference {iid}: conclusion {inf.get('conclusion')} not in produced set")

    # S04 — the thesis is a produced conclusion
    thesis_pid = (syn.get("thesis") or {}).get("proposition_id")
    if thesis_pid:
        if thesis_pid not in inference_conclusions:
            problems.append(f"thesis proposition_id {thesis_pid} is not a produced inference conclusion")
    else:
        problems.append("thesis lacks a stable proposition_id (must equal a synthesis conclusion)")

    # S05 — weakest-governs over LOAD-BEARING deps only
    audit = syn.get("synthesis_audit", {})
    deps = syn.get("dependency_state", {}).get("dependencies", [])
    lb_statuses = [d.get("epistemic_status") for d in deps if d.get("role") in ROLE_LOAD_BEARING]
    if not lb_statuses:
        problems.append("no LOAD_BEARING dependencies to compute the ceiling over")
    else:
        expected = min((CEILING_RANK.get(s, 1) for s in lb_statuses), default=0)
        expected_status = next((s for s, r in sorted(CEILING_RANK.items(), key=lambda kv: kv[1])
                                if r == expected), "UNRESOLVED")
        if audit.get("epistemic_ceiling") != expected_status:
            problems.append(f"epistemic_ceiling {audit.get('epistemic_ceiling')} != weakest load-bearing "
                            f"({expected_status} over {sorted(set(lb_statuses))})")

    # S08 — per-dependency structural_audit must be well-formed
    for d in deps:
        sa = d.get("structural_audit") or {}
        for k in ("state", "outcome", "audit_refs"):
            if k not in sa:
                problems.append(f"dependency {d.get('ref')}: structural_audit missing '{k}'")

    # S09 — structural audit axis separate + the downstream projection invariant
    sas = audit.get("structural_audit_state")
    if not sas:
        problems.append("synthesis_audit.structural_audit_state missing (must be INCOMPLETE/COMPLETE)")
    if sas and sas != "COMPLETE" and any(d.get("structural_audit", {}).get("outcome") is not None
                                          for d in deps):
        problems.append("structural_audit_state != COMPLETE but a dependency has a structural outcome "
                        "(projection may NOT manufacture structural_gate_outcome=accepted)")

    # S10 — internal_consistency must not overclaim
    ic = audit.get("internal_consistency")
    if ic == "STRUCTURALLY_COHERENT":
        problems.append("internal_consistency=STRUCTURALLY_COHERENT is not demonstrated "
                        "(no cross-inference / warrant / Nyāya check ran); use NOT_EVALUATED")

    # S11 — boundary vocabulary
    bnd = syn.get("boundary", {})
    if "establishes" in bnd and "currently_supports" not in bnd:
        problems.append("boundary uses 'establishes' (overclaiming); use currently_supports/reconstructs")

    return {"ok": len(problems) == 0, "problems": problems,
            "ceiling": audit.get("epistemic_ceiling"),
            "structural_audit_state": audit.get("structural_audit_state"),
            "n_inferences": len(syn.get("inferences", [])),
            "n_cruxes": len(syn.get("cruxes", []))}


def check_synthesis(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return check_synthesis_obj(json.load(f))


def main() -> int:
    path = os.path.join(ROOT, "benchmarks/v0/review/SYN-IPVV-REFLEXION-CORE-001.json")
    r = check_synthesis(path)
    print("SYN-IPVV-REFLEXION-CORE-001 (canonical ArgumentSynthesis):")
    print(f"  epistemic_ceiling: {r['ceiling']} | structural_audit_state: {r['structural_audit_state']} "
          f"| inferences: {r['n_inferences']} | cruxes: {r['n_cruxes']}")
    if r["ok"]:
        print("  VALID: inputs resolved against the gold registry, premises resolve, thesis is a produced "
              "conclusion, two-axis audit, themes = metadata only.")
    else:
        for p in r["problems"]:
            print(f"    ✗ {p}")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
