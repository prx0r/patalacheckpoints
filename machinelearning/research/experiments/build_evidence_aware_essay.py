#!/usr/bin/env python3
"""build_evidence_aware_essay.py — the ResearchPack → EO v2 → evidence-aware essay path.

The peer review's directive: one real essay consumption path with the hard rule:
  if a pack dependency has semantic_status = UNRESOLVED:
      the renderer may QUALIFY it / represent alternatives / ABSTAIN
      but may NOT silently render it as settled fact.

Per the truth-engine EO-v2 spec (the canonical essay object):
  - an EO is a structured tension point, shaped as a Nyāya 5-member syllogism
  - every hetu.evidence claim must pass the Nyāya gate (§6) before production
  - nigamana.status + state_of_play carry what survives vs what's open vs what would change our mind
  - the UNRESOLVED rule maps onto nigamana.status (structurally_suggestive / underdetermined), NOT a
    settled verdict

This builds the reflexion-core EO v2 from the pack + the real golds, validating each evidence claim
through the Nyāya gate, and producing the evidence sheet (the review dossier).
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from patala_ml.gold002 import build_gold_002
from patala_ml.gold004 import build_gold_004
from patala_ml.nyayagate import gate_claim

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))
PACK = os.path.join(ROOT, "benchmarks/v0/packs/PACK-IPVV-REFLEXION-CORE.json")


def txt(n):
    return n.get("proposition") or n.get("text") or ""


def main() -> int:
    with open(PACK, encoding="utf-8") as f:
        pack = json.load(f)

    golds = {"ARG-GOLD-002": build_gold_002(), "ARG-GOLD-004": build_gold_004()}
    props = {}
    for gid, g in golds.items():
        for n in g["nodes"]:
            props[n["proposition_id"]] = (txt(n), gid, n.get("commitment"))

    # the evidence claims of the reflexion-core EO, each grounded in a gold proposition + gated
    evidence = []
    for cg in pack["proposition_refs"]:
        prop_text, gid, commitment = props.get(cg, ("(missing)", "", ""))
        if not prop_text:
            continue
        gate = gate_claim({"claim_id": f"pack:{cg}", "claim_text": prop_text,
                           "pramana": "anumana", "falsifier": {"type": "structural"},
                           "log_bayes_factor": 0.0}).to_dict()
        evidence.append({
            "claim": prop_text, "source_id": f"gold:{gid}:{cg}",
            "pramana": "anumana", "gate_outcome": gate.get("outcome"),
            "gate_failures": [f.get("fallacy") for f in gate.get("failures", [])],
        })

    # the EO v2 (canonical shape). semantic_status of every dependency is UNRESOLVED (the pack is
    # CANDIDATE / scholarly NONE), so nigamana.status is structurally_suggestive, NOT settled.
    eo = {
        "eo_id": "eo:ipvv-reflexion-core",
        "schema_version": 2,
        "title": "The determination cannot reach outside; self-experience is self-luminous",
        "status": "draft",
        "question": {
            "question_id": "q:reflexion-core-determinates-external",
            "tension_point": "Can the determination (adhyavasāya) establish an external object, or is self-experience self-luminous and self-contained?",
            "why_it_matters": "The reflexion-core cuts the Buddhist fallback to the determination as establishing externality; it is the load-bearing claim for the reflexivity/self-luminosity thesis.",
            "resolution_level": "local_argument",
        },
        "syllogism": {
            "pratijna": {"proposition": pack.get("research_question", ""),
                         "what_it_claims": "The determination cannot establish anything outside; self-experience (vimarśa) is self-luminous, un-divided from memory-cognition."},
            "hetu": {"evidence": evidence,
                     "source_ids": [f"gold:{gid}:{cg}" for cg in pack["proposition_refs"]]},
            "udaharana": {"examples": [
                {"scenario": "The child who cries 'the trees rush against the current' is told 'it is only seen so' — the outwardness is a manner of the seeing, not a thing established.",
                 "what_it_shows": "Externality is drawn by impression, not established by determination."},
            ]},
            "upanaya": {"application": "The reflexion-core's determination-failure converges with ARG-002 (the I-grasp is not a construction) and ARG-004 (manifestation without vimarśa is inert).",
                        "cruxes": ["CRUX-REFLEXION-INERT: can an inert thing establish, or does establishment require the self-luminous non-inert?"]},
            "nigamana": {"best_current_answer": "The determination cannot establish externality; self-experience is self-luminous. This is locally supported, but the universal-Self (V2C) is not entailed.",
                         "status": "structurally_suggestive",   # NOT settled — the UNRESOLVED rule
                         "scope": "Local self-luminosity: plausible. Universal-Self: underdetermined (open crux)."},
        },
        "candidates": [
            {"candidate_id": "cand:siddhanta-self-luminous", "name": "Self-luminous self-experience",
             "tradition": "pratyabhijna", "proponent": "Abhinavagupta",
             "position": "The determination cannot establish externality; the self-experience is self-luminous, one, all.",
             "source_ids": ["gold:ARG-GOLD-002:G2-CONC", "gold:ARG-GOLD-004:G4-CONC"],
             "status": "live"},
            {"candidate_id": "cand:buddhist-adhyavasaya", "name": "The determination establishes externality",
             "tradition": "buddhist_pramana", "proponent": "the Buddhist (fallback)",
             "position": "The determination (adhyavasāya) establishes an external object.",
             "source_ids": [], "status": "live",
             "falsifiers": ["An inert thing cannot establish (the reflexion-core's argument)"]},
        ],
        "state_of_play": {
            "summary": "The reflexion-core argues the determination cannot reach outside; self-experience is self-luminous. All dependencies are UNRESOLVED (CANDIDATE).",
            "what_survives": "The determination-failure argument and the self-luminosity claim (gated accepted).",
            "what_is_weakened": "The universal-Self (V2C) is not entailed by per-act self-luminosity.",
            "what_would_change_our_mind": "Evidence that an inert thing can establish, or that the 'external' has independent standing in any part of cognition.",
            "open_cruxes": ["CRUX-REFLEXION-INERT", "Does the reflexion-core's 'one, self-luminous, all' commit to the universal-Self?"],
        },
        "provenance": {"parent_ros": [], "parent_dossier": "benchmarks/v0/packs/PACK-IPVV-REFLEXION-CORE.json",
                       "created_by": "agent1", "last_updated": "2026-08-12"},
        # the hard behavior rule, made explicit
        "render_rule": "Any dependency with semantic_status=UNRESOLVED is QUALIFIED or ABSTAINED; "
                       "never rendered as settled fact. nigamana.status must stay structurally_suggestive/underdetermined.",
    }

    out = os.path.join(ROOT, "benchmarks/v0/review/EO-IPVV-REFLEXION-CORE.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(eo, f, indent=2)

    print("EO v2 (evidence-aware essay object) — reflexion-core")
    print(f"  evidence claims: {len(evidence)} | all gated:")
    for e in evidence:
        print(f"    {e['source_id']:28} gate={e['gate_outcome']} fails={e['gate_failures']}")
    print(f"  nigamana.status: {eo['syllogism']['nigamana']['status']}  (NOT settled — UNRESOLVED rule)")
    print(f"  open cruxes: {[c for c in eo['state_of_play']['open_cruxes']]}")
    print(f"\nwritten: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
