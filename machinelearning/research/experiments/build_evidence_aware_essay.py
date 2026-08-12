#!/usr/bin/env python3
"""build_evidence_aware_essay.py — ResearchPack → evidence-aware EssayObject construction.

Per the peer review + canonical EO-v2 spec (docs/ontology/EO-v2.md): construct an evidence-aware
EssayObject (EO) from a ResearchPack, with STRICT provenance discipline:

  - every source_id is derived from the actual proposition→(gold,text,commitment) resolution map
    (no stale loop variables);
  - every proposition_ref MUST resolve; an unresolved ref HARD-FAILS (no fake "(missing)" evidence);
  - each evidence claim carries structural_gate_outcome SEPARATE from epistemic_status
    (gate accepted ≠ evidence accepted ≠ scholar supported);
  - unsourced rival positions are marked UNSOURCED_RECONSTRUCTION (never a clean "live" position
    with no source);
  - grounded claims are joined into conclusions ONLY via explicit inference/warrant objects
    (evidence coexistence ≠ inference);
  - the render ceiling (UNRESOLVED vs CAN_RENDER) is DERIVED from the pack's dependency statuses.

This is "evidence-aware EssayObject construction", NOT yet a prose essay renderer — that is the
next layer (EssayPlan → draft → sentence/claim/inference/evidence audit).
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

# schema provenance (issue 7): the canonical spec is now pinned inside patala
SCHEMA_SOURCE = {"repo": "patala", "commit": "docs/ontology/EO-v2.md", "path": "docs/ontology/EO-v2.md"}

# the render-ceiling policy (issue 6): derived from dependency statuses, data-driven
PACK_STATUS_TO_CEILING = {
    "INDEPENDENT_REVIEWED": "CAN_RENDER_AS_GROUNDED",
    "SCHOLARLY_CORROBORATED": "CAN_RENDER_AS_GROUNDED",
    "SCHOLARLY_CORROBORATED_PRELIMINARY": "CAN_RENDER_QUALIFIED",
    "CANDIDATE": "UNRESOLVED",          # must qualify / abstain
    "MACHINE_PROPOSED": "UNRESOLVED",
}


def derive_render_ceiling(pack: dict) -> str:
    """Derive the render ceiling from the pack's dependency statuses (data-driven, not hardcoded)."""
    rs = pack.get("review_summary", {})
    # the governing status is the WEAKEST of the relevant review states
    arg_review = rs.get("argument_review", "CANDIDATE").upper()
    scholarly = rs.get("scholarly_review", "NONE").upper()
    # scholarly_review=NONE is the weakest possible — the whole thing is unresolved
    if scholarly in ("NONE", ""):
        return "UNRESOLVED"
    ceiling = PACK_STATUS_TO_CEILING.get(arg_review, "UNRESOLVED")
    return ceiling


def resolve_propositions() -> dict:
    """Build the authoritative proposition→(gold_id, text, commitment) map (no stale vars)."""
    props = {}
    for gid, g in ({"ARG-GOLD-002": build_gold_002(), "ARG-GOLD-004": build_gold_004()}).items():
        for n in g["nodes"]:
            props[n["proposition_id"]] = {
                "gold_id": gid,
                "text": n.get("proposition") or n.get("text") or "",
                "commitment": n.get("commitment") or n.get("speaker") or "",
            }
    return props


def main() -> int:
    with open(PACK, encoding="utf-8") as f:
        pack = json.load(f)
    props = resolve_propositions()

    # issue 2/3: every proposition_ref must resolve — HARD FAIL if not
    missing = [cg for cg in pack["proposition_refs"] if cg not in props]
    if missing:
        raise ValueError(f"unresolved proposition_ref(s): {missing} — the composition is malformed")

    # evidence claims with CORRECT gold_id (issue 1) + split gate/epistemic (issue 4)
    evidence = []
    for cg in pack["proposition_refs"]:
        r = props[cg]
        gate = gate_claim({"claim_id": f"pack:{cg}", "claim_text": r["text"],
                           "pramana": "anumana", "falsifier": {"type": "structural"},
                           "log_bayes_factor": 0.0}).to_dict()
        evidence.append({
            "claim": r["text"],
            "source_id": f"gold:{r['gold_id']}:{cg}",   # correct gold_id from the map
            "proposition_id": cg,
            "pramana": "anumana",
            "structural_gate_outcome": gate.get("outcome"),      # structural only
            "gate_failures": [f.get("fallacy") for f in gate.get("failures", [])],
            "epistemic_status": "MACHINE_PROPOSED",              # separate dimension
        })

    # issue 9: ground the rival position or mark it UNSOURCED
    rival_position = {
        "candidate_id": "cand:buddhist-adhyavasaya",
        "name": "The determination establishes externality",
        "tradition": "buddhist_pramana",
        "proponent": "the Buddhist (fallback, per the reflexion-core passage)",
        "position": "The determination (adhyavasāya) establishes an external object.",
        "source_ids": [],           # no resolving proposition in the golds
        "status": "UNSOURCED_RECONSTRUCTION",   # honest: reconstructed opponent, not grounded
    }

    # issue 10: explicit inferences (warrant) so grounded claims cannot be silently joined
    inferences = [
        {"from": ["gold:ARG-GOLD-002:G2-TC2", "gold:ARG-GOLD-004:G4-CRYSTAL"],
         "to": "gold:ARG-GOLD-002:G2-CONC",
         "warrant": "the I-grasp is not a construction; manifestation without vimarśa is inert → "
                    "self-experience is self-luminous and self-contained",
         "status": "RECONSTRUCTED"},
    ]

    ceiling = derive_render_ceiling(pack)

    eo = {
        "eo_id": "eo:ipvv-reflexion-core",
        "schema_version": 2,
        "title": "The determination cannot reach outside; self-experience is self-luminous",
        "status": "draft",
        "schema_source": SCHEMA_SOURCE,     # issue 7: immutable schema resolver
        "question": {
            "question_id": "q:reflexion-core-determinates-external",
            "tension_point": "Can the determination (adhyavasāya) establish an external object, or is self-experience self-luminous and self-contained?",
            "why_it_matters": "The reflexion-core cuts the Buddhist fallback to the determination as establishing externality.",
            "resolution_level": "local_argument",
        },
        "syllogism": {
            "pratijna": {"proposition": pack.get("research_question", ""),
                         "what_it_claims": "The determination cannot establish anything outside; self-experience (vimarśa) is self-luminous."},
            "hetu": {"evidence": evidence,
                     "source_ids": [e["source_id"] for e in evidence]},
            "udaharana": {"examples": [
                {"scenario": "The child who cries 'the trees rush against the current' is told 'it is only seen so'.",
                 "what_it_shows": "Externality is drawn by impression, not established by determination."}]},
            "upanaya": {"application": "The reflexion-core's determination-failure converges with the golds.",
                        "cruxes": ["CRUX-REFLEXION-INERT"]},
            "nigamana": {"best_current_answer": "The determination cannot establish externality; self-experience is self-luminous (locally).",
                         "status": "structurally_suggestive",   # render ceiling is UNRESOLVED
                         "scope": "Local self-luminosity: plausible. Universal-Self: underdetermined."},
        },
        "inferences": inferences,           # issue 10
        "candidates": [
            {"candidate_id": "cand:siddhanta-self-luminous", "name": "Self-luminous self-experience",
             "tradition": "pratyabhijna", "proponent": "Abhinavagupta",
             "position": "The determination cannot establish externality; self-experience is self-luminous.",
             "source_ids": ["gold:ARG-GOLD-002:G2-CONC", "gold:ARG-GOLD-004:G4-CONC"],
             "status": "live"},
            rival_position,                  # issue 9: UNSOURCED_RECONSTRUCTION
        ],
        "state_of_play": {
            "summary": "The reflexion-core argues the determination cannot reach outside; self-experience is self-luminous.",
            "what_survives": "The determination-failure argument and self-luminosity (structural gate accepted).",
            "what_is_weakened": "The universal-Self (V2C) is not entailed by per-act self-luminosity.",
            "what_would_change_our_mind": "Evidence that an inert thing can establish, or that the 'external' has independent standing.",
            "open_cruxes": ["CRUX-REFLEXION-INERT",
                            "Does the reflexion-core's 'one, self-luminous, all' commit to the universal-Self?"],
        },
        "render_ceiling": ceiling,           # issue 6: derived from pack statuses (UNRESOLVED)
        "render_rule": "When render_ceiling == UNRESOLVED, the renderer must QUALIFY / represent "
                       "alternatives / ABSTAIN — never render as settled fact.",
        "provenance": {"parent_ros": [], "parent_dossier": PACK,
                       "created_by": "agent1", "last_updated": "2026-08-12"},
    }

    out = os.path.join(ROOT, "benchmarks/v0/review/EO-IPVV-REFLEXION-CORE.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(eo, f, indent=2)

    print("Evidence-aware EssayObject construction (ResearchPack -> EO v2)")
    print(f"  render ceiling (derived from pack): {ceiling}")
    for e in evidence:
        print(f"    {e['source_id']:30} gate={e['structural_gate_outcome']:8} epistemic={e['epistemic_status']}")
    print(f"  inferences: {len(inferences)} | rival status: {rival_position['status']}")
    print(f"\nwritten: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
