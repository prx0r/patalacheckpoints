#!/usr/bin/env python3
"""build_eo_from_synthesis.py — ArgumentSynthesis → EssayObject v2 (a LOSSLESS EPISTEMIC PROJECTION).

Commit B per the coordinator directive: the EO is a PROJECTION of the canonical ArgumentSynthesis
(`synthesis_to_eo(syn)`), NOT a loose independent build. It must:

  * derive evidence from the SYNTHESIS's dependency state (proposition refs + resolved epistemic_status
    + structural_audit), NOT from re-running gate_claim() on arbitrary claims — that disconnected path is gone;
  * preserve the EO-v2 distinction  structural_gate_outcome ≠ epistemic_status;
  * honor the projection invariant: if synthesis.structural_audit_state != COMPLETE, then
    structural_gate_outcome = "NOT_AUDITED" for every evidence claim (NEVER "accepted");
  * never strengthen any state — the EO's nigamana/render_ceiling inherit the synthesis's epistemic ceiling
    (UNRESOLVED → structurally_suggestive / must qualify / abstain);
  * carry the synthesis's explicit bridge inference + warrant (evidence coexistence ≠ inference);
  * keep the universalization as an open crux/boundary, never a settled claim.

This is "evidence-aware EssayObject construction from a validated synthesis" — NOT yet a prose renderer
(EssayPlan → draft → sentence/claim/inference/evidence audit is Commit C).
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patala_ml.gold002 import build_gold_002
from patala_ml.gold004 import build_gold_004
from build_argument_synthesis import build_synthesis

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))
OUT = os.path.join(ROOT, "benchmarks/v0/review/EO-IPVV-REFLEXION-CORE.json")

SCHEMA_SOURCE = {"repo": "patala", "commit": "docs/ontology/EO-v2.md", "path": "docs/ontology/EO-v2.md"}

# synthesis epistemic ceiling -> EO render posture (never strengthens)
CEILING_TO_RENDER = {
    "INDEPENDENT_REVIEWED": "CAN_RENDER_AS_GROUNDED",
    "SCHOLARLY_CORROBORATED": "CAN_RENDER_AS_GROUNDED",
    "SCHOLARLY_CORROBORATED_PRELIMINARY": "CAN_RENDER_QUALIFIED",
    "ENGINEERING_VALIDATED": "CAN_RENDER_QUALIFIED",
    "MACHINE_PROPOSED": "UNRESOLVED",
    "UNRESOLVED": "UNRESOLVED",
}
CEILING_TO_NIGAMANA = {
    "INDEPENDENT_REVIEWED": "grounded",
    "SCHOLARLY_CORROBORATED": "grounded",
    "SCHOLARLY_CORROBORATED_PRELIMINARY": "supported_qualified",
    "ENGINEERING_VALIDATED": "supported_qualified",
    "MACHINE_PROPOSED": "structurally_suggestive",
    "UNRESOLVED": "structurally_suggestive",
}


def _proposition_texts() -> dict:
    """gold:prop -> text (authoritative, from the actual gold nodes)."""
    texts = {}
    for gid, g in ({"ARG-GOLD-002": build_gold_002(), "ARG-GOLD-004": build_gold_004()}).items():
        for n in g["nodes"]:
            texts[f"{gid}:{n['proposition_id']}"] = n.get("proposition") or n.get("text") or ""
    return texts


def synthesis_to_eo(syn: dict) -> dict:
    """Project a canonical ArgumentSynthesis into an EO-v2 object (lossless, never strengthening)."""
    texts = _proposition_texts()
    audit = syn.get("synthesis_audit", {})
    ceiling = audit.get("epistemic_ceiling", "UNRESOLVED")
    sas = audit.get("structural_audit_state", "INCOMPLETE")
    deps = syn.get("dependency_state", {}).get("dependencies", [])

    # ── evidence derived from the SYNTHESIS's load-bearing proposition dependencies ──
    evidence = []
    for d in syn.get("dependency_state", {}).get("dependencies", []):
        pid = d.get("proposition_id")
        if not pid or d.get("gold_id") == "SYNTHESIS":
            continue  # the bridge is an inference, not a proposition
        sa = d.get("structural_audit") or {}
        # PROJECTION INVARIANT: structural_gate_outcome only from a REAL persisted audit.
        # With structural_audit_state INCOMPLETE, it is NOT_AUDITED — never "accepted".
        if sas == "COMPLETE" and sa.get("outcome"):
            gate_outcome = sa["outcome"]
        else:
            gate_outcome = "NOT_AUDITED"
        evidence.append({
            "claim": d.get("provenance", {}).get("text") or texts.get(d["ref"]) or "",
            "source_id": d["ref"],                      # e.g. ARG-GOLD-002:G2-CONC
            "proposition_id": pid,
            "pramana": "anumana",
            "structural_gate_outcome": gate_outcome,     # structural only (never "accepted" while INCOMPLETE)
            "gate_failures": [],
            "epistemic_status": d.get("epistemic_status"),   # separate dimension, from the synthesis
        })

    # ── the synthesis's bridge inference (explicit warrant; evidence coexistence ≠ inference) ──
    inferences = []
    for inf in syn.get("inferences", []):
        inferences.append({
            "from": [f"{p}" for p in inf.get("premises", [])],
            "to": inf.get("conclusion"),
            "warrant": inf.get("warrant", ""),
            "origin": inf.get("origin"),
            "support_state": inf.get("support_state"),
            "status": inf.get("origin"),
        })

    thesis = syn.get("thesis", {})
    boundary = syn.get("boundary", {})
    cruxes = syn.get("cruxes", [])

    eo = {
        "eo_id": "eo:ipvv-reflexion-core",
        "schema_version": 2,
        "title": thesis.get("text", ""),
        "status": "draft",
        "schema_source": SCHEMA_SOURCE,
        "projection_of": syn.get("synthesis_id"),   # EO is a PROJECTION of the canonical synthesis
        "question": {
            "question_id": "q:reflexion-core-intrinsic",
            "tension_point": syn.get("research_question", ""),
            "why_it_matters": "The reflexion-core: whether reflexivity belongs intrinsically to manifestation.",
            "resolution_level": "local_argument",
        },
        "syllogism": {
            "pratijna": {"proposition": thesis.get("text", ""),
                         "what_it_claims": "Reflexivity belongs intrinsically to manifestation (reconstructed)."},
            "hetu": {"evidence": evidence,
                     "source_ids": [e["source_id"] for e in evidence]},
            "udaharana": {"examples": [{"scenario": "a light that showed the world without knowing it showed it would be like inert crystal",
                                        "what_it_shows": "self-awareness in the act is what distinguishes the conscious from the inert"}]},
            "upanaya": {"application": "the synthesis of ARG-002 (I not a construction) + ARG-004 (manifestation without vimarśa inert)",
                        "cruxes": [c["crux_id"] for c in cruxes]},
            "nigamana": {"best_current_answer": thesis.get("text", ""),
                         "status": CEILING_TO_NIGAMANA.get(ceiling, "structurally_suggestive"),
                         "scope": "Local: reflexivity intrinsic per act. Universal-Self: open boundary."},
        },
        "inferences": inferences,
        "state_of_play": {
            "summary": thesis.get("text", ""),
            "what_survives": "the reconstructed bridge + the resolved load-bearing dependency statuses",
            "what_is_weakened": "the bridge support_state (UNRESOLVED) + the universalization boundary",
            "what_would_change_our_mind": "a real contextual audit (structural_audit_state -> COMPLETE) or an independent review",
            "open_cruxes": [c["crux_id"] for c in cruxes],
        },
        "render_ceiling": CEILING_TO_RENDER.get(ceiling, "UNRESOLVED"),   # derived from the synthesis ceiling
        "render_rule": ("When render_ceiling == UNRESOLVED, the renderer must QUALIFY / represent "
                        "alternatives / ABSTAIN — never render as settled fact. Structural outcomes are "
                        "NOT_AUDITED until a real contextual audit exists."),
        # ── Pāṭala epistemics extension to the legacy EO-v2 presentation schema ──
        # (the projection's organizing invariant: authority(P(x)) <= authority(x) for every projected claim)
        "patala_epistemics": {
            "render_ceiling": CEILING_TO_RENDER.get(ceiling, "UNRESOLVED"),
            "structural_audit_state": sas,
            "projection_policy": "MONOTONE_NO_STRENGTHENING",
            "source_synthesis": {
                "synthesis_id": syn.get("synthesis_id"),
                "synthesis_epistemic_ceiling": ceiling,
                "synthesis_structural_audit_state": sas,
            },
        },
        # B4 — no logical-boundary loss: every does_not_establish + crux survives machine-resolvably
        "boundary": {
            "does_not_establish": list(boundary.get("does_not_establish", [])),
            "crux_ids": [c["crux_id"] for c in cruxes],
        },
        # candidate handling: the sourced siddhanta candidate is live; the unsourced Buddhist rival stays
        # UNSOURCED_RECONSTRUCTION (recorded in the Pāṭala extension; never laundered to legacy 'live')
        "candidates": [
            {"candidate_id": "cand:siddhanta-reflexivity-intrinsic",
             "name": "Reflexivity belongs intrinsically to manifestation",
             "tradition": "pratyabhijna", "proponent": "Abhinavagupta",
             "position": thesis.get("text", ""),
             "source_ids": [d["ref"] for d in deps if d.get("gold_id") != "SYNTHESIS"],
             "status": "live",
             "patala_status": "RECONSTRUCTED_SUPPORTED"},
            {"candidate_id": "cand:buddhist-adhyavasaya-unsourced",
             "name": "The determination establishes externality (unsourced opponent)",
             "tradition": "buddhist_pramana", "proponent": "the Buddhist (fallback)",
             "position": "The determination (adhyavasāya) establishes an external object.",
             "source_ids": [],
             "status": "UNSOURCED_RECONSTRUCTION",   # honest: reconstructed opponent, not grounded
             "patala_status": "UNSOURCED_RECONSTRUCTION"},
        ],
        "provenance": {"parent_ros": [], "parent_synthesis": syn.get("synthesis_id"),
                       "projection_of": syn.get("synthesis_id"),
                       "created_by": "agent1", "last_updated": "2026-08-12"},
    }
    return eo


def main() -> int:
    syn = build_synthesis()
    eo = synthesis_to_eo(syn)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(eo, f, indent=2)

    print("ArgumentSynthesis -> EO v2 (lossless epistemic projection)")
    print(f"  projection_of: {eo['projection_of']}")
    print(f"  render_ceiling (from synthesis ceiling): {eo['render_ceiling']}")
    print(f"  nigamana.status: {eo['syllogism']['nigamana']['status']}")
    for e in eo["syllogism"]["hetu"]["evidence"]:
        print(f"    {e['source_id']:26} structural_gate_outcome={e['structural_gate_outcome']:11} "
              f"epistemic_status={e['epistemic_status']}")
    print(f"  inferences: {len(eo['inferences'])} | cruxes: {len(eo['state_of_play']['open_cruxes'])}")
    print(f"\nwritten: {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
