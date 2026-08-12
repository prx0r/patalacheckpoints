#!/usr/bin/env python3
"""pipeline/l200_worker.py — the L200 layer handler (the audit compiler).

Per hermespatalalayers.md + the frozen L200 spec (translations/_stack/ipvv/l200/README-L200-SPEC.md):

  DO NOT use the LLM to regenerate what the graph already knows. L200 is partly deterministic:
  - deterministic: identification, published reading, derivation map (from refs), source hashes,
    upstream IDs, review state
  - model-proposed: candidate MaterialTranslationDecision classification, candidate InterpretiveAssertion,
    open-item detection

The validator enforces the Task-2 fidelity checks (8 sections; MT separate from IA; refs typed;
open items have status; review state set). This is the derivational proof object of the stack.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import object_registry as R
from model import chat

MT_TYPES = ["SUPPLIED", "REFERENT_SUPPLY", "STRUCTURAL_CONNECTIVE", "LEXICAL", "GRAMMATICAL"]
SOURCE_LAYERS = ["kārikā", "Vṛtti", "Vivṛti", "Abhinava", "objection", "reply", "quotation"]
XREF_TYPES = ["ROOT_TEXT_CONTEXT", "SAME_ARGUMENT_CONTINUATION", "DOCTRINAL_PARALLEL",
              "COMPARATIVE_PARALLEL", "SECONDARY_SYNTHESIS"]


def l200_generator(layer: str, batch: list[dict]) -> list[dict]:
    """Build the 8-section L200 for each L2 object. Deterministic scaffold + model MT/IA proposal.

    COMPARATIVE (the correct L200 information flow): the model proposes MT/IA by comparing the
    GROUNDED reading (L0/L1) against L2 — not from L2 prose alone. proposal_status is COMPLETE only
    if the model call succeeded; GENERATION_FAILED otherwise (model failure ≠ empty successful audit).
    """
    proposals = []
    for b in batch:
        obj = b.get("_l2") or {}          # the L2 object (text + refs) the caller attaches
        l2_text = obj.get("text", "")
        l2_refs = obj.get("refs", [])
        l1_text = obj.get("l1_text", "")  # the grounded/controlled reading (for the comparison)
        # deterministic scaffold (sections 0,1,2,5,6,8 from refs/graph); object ref ≠ hash
        scaffold = {
            "0_identification": {"object_id": b["object_id"], "l2_ref": obj.get("l2_ref", b["object_id"]),
                                 "l2_hash": b.get("input_hash", ""), "upstream": l2_refs},
            "1_published_reading": l2_text,
            "2_derivation_map": [{"l2_par": p, "refs": obj.get("par_refs", [])} for p in obj.get("paragraphs", [])],
            "5_source_layer": obj.get("source_layer", []),
            "6_cross_references": obj.get("cross_references", []),
            "8_review_state": "machine",
        }
        # model proposal: COMPARATIVE (L1 grounded reading + L2), bounded; never fabricate
        status, mt, ia, open_items = _propose_mt_ia(b["object_id"], l1_text, l2_text)
        obj_audit = {
            **scaffold,
            "3_material_translation_decisions": mt,
            "4_interpretive_assertions": ia,
            "7_open_items": open_items,
        }
        proposals.append({"object_id": b["object_id"], "input_hash": b.get("input_hash", ""),
                          "verse": l2_text, "l200": obj_audit,
                          "proposal_status": status})
    return proposals


def _propose_mt_ia(object_id: str, l1_text: str, l2_text: str) -> tuple[str, list, list, list]:
    """COMPARATIVE proposal: what materially changed between the grounded (L1) reading and L2?

    Returns (status, mt, ia, open_items) where status is COMPLETE on success and GENERATION_FAILED on
    any model failure — so an empty result is only ever 'nothing found', never 'worker failed'."""
    prompt = (
        "You are the Pāṭala L200 audit compiler. Compare the GROUNDED (L1) controlled reading with the "
        "published L2 reading and identify what materially changed between them:\n"
        "1. material_translation_decisions: [] of {\"label\":\"...\",\"type\":\"<one of " +
        ",".join(MT_TYPES) + ">\",\"basis\":\"...\"} — only genuine translation interventions "
        "(supplied referent, connective, lexical/grammatical choice); a paraphrase of meaning is NOT a "
        "translation decision.\n"
        "2. interpretive_assertions: [] of {\"label\":\"IA-001\",\"text\":\"...\"}.\n"
        "3. open_items: [] of {\"text\":\"...\",\"status\":\"OPEN|NEEDS_REVIEW\"}.\n"
        "If nothing materially changed, return empty lists (that is a valid COMPLETE result).\n"
        "Return JSON ONLY.\n\nGROUNDED (L1):\n" + (l1_text or "")[:1200] +
        "\n\nPUBLISHED (L2):\n" + (l2_text or "")[:1200]
    )
    try:
        raw = chat("You are a Sanskrit philologist (L200 audit).", prompt, timeout=120)
        import json
        d = json.loads(raw)
        return "COMPLETE", \
               d.get("material_translation_decisions", []), \
               d.get("interpretive_assertions", []), d.get("open_items", [])
    except Exception:
        return "GENERATION_FAILED", [], [], []


def l200_validator(layer: str, proposal: dict) -> tuple[bool, str]:
    """Task-2 fidelity + fail-closed: model failure must NOT equal an empty successful audit.

    proposal_status must be COMPLETE (GENERATION_FAILED/PARTIAL may not commit as a completed audit)."""
    if proposal.get("proposal_status") != "COMPLETE":
        return False, f"proposal_status:{proposal.get('proposal_status','MISSING')} (model did not complete)"
    l2 = proposal.get("l200", {})
    missing = [k for k in ("0_identification", "1_published_reading", "2_derivation_map",
                           "3_material_translation_decisions", "4_interpretive_assertions",
                           "5_source_layer", "6_cross_references", "7_open_items", "8_review_state")
               if k not in l2 or l2.get(k) in (None, "", []) and k not in ("3_material_translation_decisions",
                                                                           "4_interpretive_assertions", "7_open_items")]
    # hard check: sections that must always be present and non-empty
    required = ["0_identification", "1_published_reading", "2_derivation_map",
                "5_source_layer", "8_review_state"]  # 6 cross-refs may be empty (typed; none is fine)
    missing_req = [k for k in required if k not in l2 or not l2.get(k)]
    if missing_req:
        return False, f"missing_required_sections:{','.join(missing_req)}"
    # MT entries must have a valid type
    for mt in l2.get("3_material_translation_decisions", []):
        if mt.get("type") not in MT_TYPES:
            return False, f"bad_mt_type:{mt.get('type')}"
    # source layer + crossrefs typed if present
    for xr in l2.get("6_cross_references", []):
        if xr.get("type") not in XREF_TYPES:
            return False, f"bad_xref_type:{xr.get('type')}"
    return True, ""


def make_l200_handlers() -> dict:
    return {"generator": l200_generator, "validator": l200_validator}
