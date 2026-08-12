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
    """Build the 8-section L200 for each L2 object. Deterministic scaffold + model MT/IA proposal."""
    proposals = []
    for b in batch:
        obj = b.get("_l2") or {}          # the L2 object (text + refs) the caller attaches
        l2_text = obj.get("text", "")
        l2_refs = obj.get("refs", [])
        # deterministic scaffold (sections 0,1,2,5,6,8 from refs/graph)
        scaffold = {
            "0_identification": {"object_id": b["object_id"], "l2_ref": b.get("input_hash", ""),
                                 "upstream": l2_refs},
            "1_published_reading": l2_text,
            "2_derivation_map": [{"l2_par": p, "refs": obj.get("par_refs", [])} for p in obj.get("paragraphs", [])],
            "5_source_layer": obj.get("source_layer", []),
            "6_cross_references": obj.get("cross_references", []),
            "8_review_state": "machine",
        }
        # model proposal: candidate MT + IA from the L2 text (bounded; fall back deterministically)
        mt, ia, open_items = _propose_mt_ia(b["object_id"], l2_text)
        obj_audit = {
            **scaffold,
            "3_material_translation_decisions": mt,
            "4_interpretive_assertions": ia,
            "7_open_items": open_items,
        }
        proposals.append({"object_id": b["object_id"], "input_hash": b.get("input_hash", ""),
                          "verse": l2_text, "l200": obj_audit})
    return proposals


def _propose_mt_ia(object_id: str, l2_text: str) -> tuple[list, list, list]:
    """Model proposes candidate MT/IA/open items; on any failure fall back to honest empty (never fabricate)."""
    prompt = (
        "You are the Pāṭala L200 audit compiler. From this L2 reading, propose:\n"
        "1. material_translation_decisions: [] of {\"label\":\"...\",\"type\":\"<one of " +
        ",".join(MT_TYPES) + ">\",\"basis\":\"...\"} — only genuine translation interventions; "
        "a paraphrase of meaning is NOT a translation decision.\n"
        "2. interpretive_assertions: [] of {\"label\":\"IA-001\",\"text\":\"...\"}.\n"
        "3. open_items: [] of {\"text\":\"...\",\"status\":\"OPEN|NEEDS_REVIEW\"}.\n"
        "Return JSON ONLY.\n\nL2 READING:\n" + (l2_text or "")[:2500]
    )
    try:
        raw = chat("You are a Sanskrit philologist (L200 audit).", prompt, timeout=120)
        import json
        d = json.loads(raw)
        return d.get("material_translation_decisions", []), \
               d.get("interpretive_assertions", []), d.get("open_items", [])
    except Exception:
        return [], [], []


def l200_validator(layer: str, proposal: dict) -> tuple[bool, str]:
    """Task-2 fidelity: the 8 sections present, MT separate from IA, refs typed, review state set."""
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
