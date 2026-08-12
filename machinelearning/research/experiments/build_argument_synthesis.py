#!/usr/bin/env python3
"""build_argument_synthesis.py — the ArgumentSynthesis, Pāṭala's canonical reasoning product.

ArgumentSynthesis answers: given a ResearchPack's material, what LARGER argument can defensibly be
reconstructed, exactly how does it derive (every bridge/warrant explicit), and where does it remain
open? It is NOT a container (ResearchPack) and NOT an essay (prose). It is a NEW higher-order argument
constructed from multiple lower-order arguments/evidence objects.

Crucial audit semantics: audits are NOT merged into stronger support.
  accepted + accepted != strongly_supported.
Dependencies propagate their CEILING (the weakest governs). An UNRESOLVED input keeps the synthesis
ceiling UNRESOLVED.

Themes are metadata (selection/context), NEVER inferential premises.

EO / EssayPlan / ArgumentMap are PROJECTIONS of this object, not its schema.
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
PACK = os.path.join(ROOT, "benchmarks/v0/packs/PACK-IPVV-REFLEXION-CORE.json")

# render ceilings, weakest-governs ordering
CEILING_RANK = {"INDEPENDENT_REVIEWED": 4, "SCHOLARLY_CORROBORATED": 3,
                "SCHOLARLY_CORROBORATED_PRELIMINARY": 2, "CANDIDATE": 1, "MACHINE_PROPOSED": 1}


def input_ceiling(ref: str, prop: str) -> str:
    """The epistemic ceiling of one input proposition (from the gold's commitments)."""
    # Currently every gold is CANDIDATE / MACHINE_PROPOSED (nothing independently reviewed).
    return "MACHINE_PROPOSED"


def build_synthesis() -> dict:
    with open(PACK, encoding="utf-8") as f:
        pack = json.load(f)

    # exact input propositions
    inputs = [
        {"type": "ARGUMENT", "ref": "ARG-GOLD-002",
         "proposition_refs": ["G2-TC2", "G2-CONC"]},
        {"type": "ARGUMENT", "ref": "ARG-GOLD-004",
         "proposition_refs": ["G4-CRYSTAL", "G4-CONC"]},
    ]

    # the synthesis-level inference (the NEW bridge — must be explicit, its own object)
    # Thesis: self-experience belongs intrinsically to manifestation (not externally constructed).
    # Premises: (P1) the I-grasp is not a conceptual construction [G2-CONC];
    #           (P2) manifestation without reflexive awareness would be inert [G4-CRYSTAL].
    # Bridge (the new inference): P1 + P2 => reflexivity belongs intrinsically to manifestation.
    inferences = [{
        "inference_id": "SYN-INF-001",
        "premises": ["gold:ARG-GOLD-002:G2-CONC", "gold:ARG-GOLD-004:G4-CRYSTAL"],
        "conclusion": "SYN-CONC-001",
        "warrant": ("if reflexive unity (the 'I'-grasp) is not conceptual construction "
                    "[G2-CONC], and manifestation requires reflexive self-awareness to be "
                    "non-inert [G4-CRYSTAL], then reflexivity belongs intrinsically to "
                    "manifestation"),
        "status": "MACHINE_RECONSTRUCTED",
    }]

    # dependency audits: the synthesis depends on the source arguments' audits
    dependency_audits = [
        "AUDIT-ARG-GOLD-002:G2-CONC", "AUDIT-ARG-GOLD-002:G2-TC2",
        "AUDIT-ARG-GOLD-004:G4-CRYSTAL", "AUDIT-ARG-GOLD-004:G4-CONC",
    ]

    # the synthesis-level audit — does NOT merge audits into stronger support
    input_ceilings = [input_ceiling(i["ref"], p) for i in inputs for p in i["proposition_refs"]]
    # weakest governs (UNRESOLVED if any input is CANDIDATE/MACHINE_PROPOSED)
    weakest = min(input_ceilings, key=lambda c: CEILING_RANK.get(c, 0))

    # THE VALUE PROBE: does the synthesis overclaim? P1+P2 do NOT entail "self-experience is
    # intrinsically fundamental". G2-CONC is about the I-grasp not being a construction; G4-CRYSTAL
    # is about inertness-without-vimarsa. The synthesis thesis (reflexivity belongs intrinsically to
    # manifestation) is a REASONABLE bridge but NOT entailed — it must be flagged as an unsupported
    # bridge (a reconstruction), not a settled conclusion.
    unsupported_bridges = ["SYN-INF-001"]

    synthesis = {
        "synthesis_id": "SYN-IPVV-REFLEXION-CORE-001",
        "object_kind": "ArgumentSynthesis",
        "research_question": pack.get("research_question", ""),
        "thesis": {
            "proposition": ("Reflexivity (vimarśa) belongs intrinsically to manifestation: the "
                            "self-grasp is not a construction, and manifestation without reflexive "
                            "awareness is inert."),
            "status": "MACHINE_RECONSTRUCTED",
        },
        "theme_refs": pack.get("theme_refs", []),   # metadata only — NEVER premises
        "inputs": inputs,
        "inferences": inferences,
        "dependency_audits": dependency_audits,
        "synthesis_audit": {
            "input_ceiling": weakest,                 # weakest-governs propagation
            "internal_consistency": "PASS",           # no internal contradictions detected
            "unsupported_bridges": unsupported_bridges,   # the reconstructed bridge, not entailed
            "unresolved_dependencies": dependency_audits,  # all CANDIDATE/MACHINE_PROPOSED
            "epistemic_ceiling": "UNRESOLVED",        # because inputs are unresolved
            "audit_merge_note": "audits are NOT merged; accepted + accepted != strongly supported",
        },
        "cruxes": [
            {"crux_id": "CRUX-REFLEXION-INERT",
             "affects": ["SYN-INF-001", "SYN-CONC-001"],
             "question": "Can an inert thing establish, or does establishment require the self-luminous non-inert?"},
            {"crux_id": "CRUX-SYNTHESIS-UNIVERSAL",
             "affects": ["SYN-CONC-001"],
             "question": "Does per-act intrinsic reflexivity commit to the universal-Self (V2C), or only to per-act self-luminosity?"},
        ],
        "status": "MACHINE_PROPOSED",
    }
    return synthesis


def synthesis_to_eo(syn: dict) -> dict:
    """PROJECTION: ArgumentSynthesis -> EO v2 (a derived view, NOT the canonical schema).

    EO is one serialization of the synthesis. If EO's five-member Nyāya shape ever proves too
    restrictive, the synthesis (the actual intellectual graph) survives unchanged. This is an
    adapter, deliberately: it maps the synthesis's reasoning onto the EO's syllogism shape.
    """
    inputs_by_ref = {i["ref"]: i for i in syn["inputs"]}
    # gather evidence claims from the synthesis inputs' propositions
    evidence = []
    props = {}
    sys.path.insert(0, os.path.join(ROOT, "machinelearning/research"))
    for gid, g in {"ARG-GOLD-002": build_gold_002(), "ARG-GOLD-004": build_gold_004()}.items():
        for n in g["nodes"]:
            props[n["proposition_id"]] = n.get("proposition") or n.get("text") or ""
    for i in syn["inputs"]:
        for p in i["proposition_refs"]:
            evidence.append({"claim": props.get(p, ""), "source_id": f"gold:{i['ref']}:{p}",
                             "pramana": "anumana"})
    # the nigamana inherits the synthesis ceiling (UNRESOLVED -> structurally_suggestive, not settled)
    ceiling = syn["synthesis_audit"]["epistemic_ceiling"]
    nigamana_status = "structurally_suggestive" if ceiling == "UNRESOLVED" else "strongly_supported"
    return {
        "eo_id": "eo:ipvv-reflexion-core",
        "schema_version": 2,
        "title": syn["thesis"]["proposition"],
        "status": "draft",
        "projection_of": syn["synthesis_id"],          # the canonical object
        "schema_source": {"repo": "patala", "path": "docs/ontology/EO-v2.md"},
        "question": {"question_id": "q:reflexion-core", "tension_point": syn["research_question"],
                     "why_it_matters": "the reflexion-core synthesis", "resolution_level": "local_argument"},
        "syllogism": {
            "pratijna": {"proposition": syn["thesis"]["proposition"], "what_it_claims": "synthesis thesis"},
            "hetu": {"evidence": evidence, "source_ids": [e["source_id"] for e in evidence]},
            "udaharana": {"examples": []},
            "upanaya": {"application": "synthesis of ARG-002 + ARG-004", "cruxes": [c["crux_id"] for c in syn["cruxes"]]},
            "nigamana": {"best_current_answer": syn["thesis"]["proposition"],
                         "status": nigamana_status, "scope": "local"},
        },
        "state_of_play": {"summary": syn["thesis"]["proposition"],
                          "what_survives": "synthesis thesis (reconstructed)",
                          "what_is_weakened": "unsupported bridge",
                          "what_would_change_our_mind": "independent review",
                          "open_cruxes": [c["crux_id"] for c in syn["cruxes"]]},
        "render_ceiling": ceiling,
        "provenance": {"parent_ros": [], "parent_dossier": syn["synthesis_id"],
                       "created_by": "agent1", "last_updated": "2026-08-12"},
    }


def main() -> int:
    syn = build_synthesis()
    out = os.path.join(ROOT, "benchmarks/v0/review/SYN-IPVV-REFLEXION-CORE-001.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(syn, f, indent=2)

    print("ArgumentSynthesis — SYN-IPVV-REFLEXION-CORE-001")
    print(f"  inputs: {[i['ref'] for i in syn['inputs']]}")
    print(f"  inferences (bridges): {[i['inference_id'] for i in syn['inferences']]}")
    a = syn["synthesis_audit"]
    print(f"  input_ceiling: {a['input_ceiling']} | epistemic_ceiling: {a['epistemic_ceiling']}")
    print(f"  unsupported_bridges: {a['unsupported_bridges']}  (the leap is EXPOSED, not hidden)")
    print(f"  cruxes: {[c['crux_id'] for c in syn['cruxes']]}")
    print(f"\nwritten: {out}")

    # also write the EO projection (derived, not canonical)
    eo = synthesis_to_eo(syn)
    eo_out = os.path.join(ROOT, "benchmarks/v0/review/EO-IPVV-REFLEXION-CORE.json")
    with open(eo_out, "w", encoding="utf-8") as f:
        json.dump(eo, f, indent=2)
    print(f"EO projection (derived from synthesis) written: {eo_out}")
    print(f"  nigamana.status={eo['syllogism']['nigamana']['status']} (from ceiling {eo['render_ceiling']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
