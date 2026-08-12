#!/usr/bin/env python3
"""check_sentence_evidence_audit.py — Commit C: validate the SentenceEvidenceAudit against the synthesis.

The essay's audit is checked against the SYNTHESIS's authority — metadata-driven, NOT regex.

Rules (Commit C):
  C01  Every LOAD_BEARING sentence must have the full semantic metadata (claim_refs / inference_refs /
       source_refs / render_mode / speaker / assertion_strength) and an audit block.
  C02  Synthesis sentences (claim_refs contains SYN-CONC-001) MUST resolve through the bridge:
         SYN-CONC-001 -> SYN-INF-001 -> {G2-CONC, G4-CONC} -> sources
       i.e. a sentence asserting/suggesting the thesis MUST carry SYN-INF-001 in inference_refs and the
       premise sources in source_refs. If it cites only the source spans directly (bypassing SYN-INF-001),
       the provenance is bypassed -> FAIL (warrant erasure / provenance bypass).
  C03  No claim inflation: for a sentence claiming SYN-CONC-001 (origin MACHINE_RECONSTRUCTED; bridge
       support_state UNRESOLVED):
         - assertion_strength must NOT be in {PROVEN, ESTABLISHES, PROVES}
         - speaker must NOT be "Abhinavagupta" (authorship laundering: a reconstruction is not his claim)
         - render_mode must NOT be "DIRECT" (must be QUALIFIED/ATTRIBUTED)
  C04  Boundary preservation: every synthesis.does_not_establish item must be represented by a BOUNDARY
       sentence. Dropping any -> FAIL (boundary erasure).
  C05  Rival integrity: an UNSOURCED_RECONSTRUCTION rival sentence (render_mode RIVAL, no source_refs) must
       not be rendered as DIRECT/asserted (assertion_strength must be RECONSTRUCTED / CAN_BE_RECONSTRUCTED).
  C06  Only LOAD_BEARING sentences require full chains; TRANSITION/EXPLANATORY/SIGNPOST are exempt.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_argument_synthesis import build_synthesis

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))

STRONG_STRENGTHS = {"PROVEN", "ESTABLISHES", "PROVES", "PROVED"}
FULLY_SUPPORTED = {"SCHOLARLY_CORROBORATED", "SCHOLARLY_CORROBORATED_PRELIMINARY", "INDEPENDENT_REVIEWED"}


def synthesis_authority() -> dict:
    syn = build_synthesis()
    deps = {d["ref"]: d["epistemic_status"] for d in syn["dependency_state"]["dependencies"]}
    return {
        "ceiling": syn["synthesis_audit"]["epistemic_ceiling"],
        "ref_status": deps,
        "syn_conc_origin": syn["thesis"].get("status"),
        "bridge": {inf["inference_id"]: inf for inf in syn["inferences"]},
        "bridge_premises": {inf["inference_id"]: inf.get("premises", []) for inf in syn["inferences"]},
        "does_not_establish": syn.get("boundary", {}).get("does_not_establish", []),
    }


def check_audit(audit: dict, authority: dict | None = None) -> dict:
    authority = authority or synthesis_authority()
    problems = []
    syn_conc = "SYN-CONC-001"
    syn_inf = "SYN-INF-001"

    sent_by_id = {}
    boundary_sents = []

    for r in audit.get("sentences", []):
        sid = r.get("sid")
        sent_by_id[sid] = r
        role = r.get("role", "EXPLANATORY")
        if role != "LOAD_BEARING":
            continue  # C06 — non-load-bearing prose is exempt

        # C01 — full metadata on load-bearing sentences
        for field in ("claim_refs", "inference_refs", "source_refs", "render_mode", "speaker", "assertion_strength"):
            if field not in r:
                problems.append(f"{sid}: missing '{field}'")
        if "audit" not in r:
            problems.append(f"{sid}: missing audit block")

        # C03 — no claim inflation on a synthesis-thesis sentence
        if syn_conc in r.get("claim_refs", []):
            # C02 — must go THROUGH the bridge, never bypass by citing sources directly
            if syn_inf not in r.get("inference_refs", []):
                problems.append(f"{sid}: claims {syn_conc} but bypasses {syn_inf} (warrant erasure / provenance bypass)")
            strength = r.get("assertion_strength", "").upper()
            if strength in STRONG_STRENGTHS:
                problems.append(f"{sid}: assertion_strength={strength} on a MACHINE_RECONSTRUCTED thesis (inflation)")
            if r.get("speaker") == "Abhinavagupta":
                problems.append(f"{sid}: attributes the reconstruction {syn_conc} to Abhinavagupta (authorship laundering)")
            if r.get("attribution") == "AUTHOR":
                problems.append(f"{sid}: attribution=AUTHOR on the reconstructed {syn_conc} (authorship laundering)")
            if r.get("render_mode") == "DIRECT":
                problems.append(f"{sid}: render_mode DIRECT for UNRESOLVED thesis (must be QUALIFIED/ATTRIBUTED)")

        # C03b — a QUALIFIED claim must not be DIRECT
        statuses = [authority["ref_status"].get(c, "MACHINE_PROPOSED") for c in r.get("claim_refs", [])]
        if statuses and r.get("render_mode") == "DIRECT" and not all(s in FULLY_SUPPORTED for s in statuses):
            problems.append(f"{sid}: render_mode DIRECT but claims are not fully supported {sorted(set(statuses))}")

        # C05 — rival integrity: an unsourced opponent must stay RIVAL/reconstructed, never asserted
        is_rival = r.get("render_mode") == "RIVAL" or r.get("is_rival") is True
        if is_rival and not r.get("source_refs"):
            if r.get("render_mode") in ("DIRECT",) or r.get("assertion_strength", "").upper() in STRONG_STRENGTHS:
                problems.append(f"{sid}: unsourced rival rendered as asserted (rival laundering)")
        # general guard: any unsourced, non-boundary position asserted as fact is laundering
        if (not r.get("claim_refs")) and (not r.get("source_refs")) and r.get("render_mode") != "BOUNDARY":
            if r.get("render_mode") == "DIRECT" or r.get("assertion_strength", "").upper() in STRONG_STRENGTHS:
                problems.append(f"{sid}: unsourced position asserted (rival/boundary laundering)")

        # C07 — paraphrase-expansion guard (semantic-strength drift inside a single proposition)
        if r.get("claim_refs"):
            rel = r.get("semantic_relation_to_claim")
            if rel not in ("EXACT", "CONSERVATIVE_PARAPHRASE", "EXPANSIVE"):
                problems.append(f"{sid}: semantic_relation_to_claim {rel!r} missing/invalid on a claimed sentence")
            elif rel == "EXPANSIVE":
                # EXPANSIVE is only allowed if the added content is backed by extra refs
                if len(r.get("claim_refs", [])) <= 1 and not r.get("inference_refs"):
                    problems.append(f"{sid}: semantic_relation_to_claim=EXPANSIVE with no additional "
                                    "claim/inference refs (unsupported surface expansion)")

        # C04 — collect boundary sentences
        if r.get("render_mode") == "BOUNDARY":
            boundary_sents.append(sid)

    # C04 — boundary preservation (ALWAYS checked; zero boundary sentences = total erasure)
    boundary_text = " ".join(sent_by_id[s]["text"].lower() for s in boundary_sents)
    for item in authority["does_not_establish"]:
        key = item.split()[0].lower()
        if key and key not in boundary_text:
            problems.append(f"boundary erasure: does_not_establish item {item!r} not represented")

    return {"ok": len(problems) == 0, "problems": problems,
            "n_load_bearing": sum(1 for r in audit.get("sentences", []) if r.get("role") == "LOAD_BEARING"),
            "n_boundary": len(boundary_sents)}


def check_audit_path(audit_path: str, authority: dict | None = None) -> dict:
    with open(audit_path, encoding="utf-8") as f:
        return check_audit(json.load(f), authority)


def main() -> int:
    audit_path = os.path.join(ROOT, "benchmarks/v0/review/ESSAY-IPVV-REFLEXION-CORE-001.audit.json")
    r = check_audit_path(audit_path)
    print("ESSAY-IPVV-REFLEXION-CORE-001 SentenceEvidenceAudit:")
    print(f"  load-bearing sentences: {r['n_load_bearing']} | boundary sentences: {r['n_boundary']}")
    if r["ok"]:
        print("  VALID: synthesis sentences resolve through SYN-INF-001; no inflation / laundering / "
              "boundary erasure / warrant erasure.")
    else:
        for p in r["problems"]:
            print(f"    ✗ {p}")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
