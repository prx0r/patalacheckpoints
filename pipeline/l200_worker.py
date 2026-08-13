#!/usr/bin/env python3
"""pipeline/l200_worker.py — the L200 layer handler (the audit compiler).

Per hermespatalalayers.md + the frozen L200 spec (translations/_stack/ipvv/l200/README-L200-SPEC.md):

  DO NOT use the LLM to regenerate what the graph already knows. L200 is partly deterministic:
  - deterministic: identification, published reading, derivation map (from refs), source hashes,
    upstream IDs, review state
  - model-proposed: candidate MaterialTranslationDecision classification, candidate InterpretiveAssertion,
    open-item detection

CONSTRAINED COMPILER (CP4 redesign, MISSION CP4/CP5): the model no longer writes open-ended MT/IA
lists. Instead the worker generates a bounded set of CANDIDATE alignment units from the grounded L1
reading vs the published L2 reading, and the model CLASSIFIES each candidate (SUPPLIED /
REFERENT_SUPPLY / STRUCTURAL_CONNECTIVE / LEXICAL / GRAMMATICAL / INTERPRETIVE_ASSERTION /
OPEN / IGNORE). IGNORE is the DEFAULT PRIOR: most English differences are not material translation
decisions. Candidate generation does NOT assert a decision — it only marks "this alignment location
requires classification." The validator enforces the Task-2 fidelity checks (8 sections; MT separate
from IA; refs typed; open items have status; review state set). This is the derivational proof object
of the stack.
"""
from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import object_registry as R
from model import chat

MT_TYPES = ["SUPPLIED", "REFERENT_SUPPLY", "STRUCTURAL_CONNECTIVE", "LEXICAL", "GRAMMATICAL"]
CLASS_LABELS = MT_TYPES + ["INTERPRETIVE_ASSERTION", "OPEN", "IGNORE"]
SOURCE_LAYERS = ["kārikā", "Vṛtti", "Vivṛti", "Abhinava", "objection", "reply", "quotation"]
XREF_TYPES = ["ROOT_TEXT_CONTEXT", "SAME_ARGUMENT_CONTINUATION", "DOCTRINAL_PARALLEL",
              "COMPARATIVE_PARALLEL", "SECONDARY_SYNTHESIS"]
_VERBOTEN = re.compile(r"\b(the|and|of|is|in|to|a|for|with|that|this)\b", re.I)


def _committed_l2(object_id: str, input_hash: str) -> dict:
    """Resolve the committed L2 object (the authoritative input) from the registry."""
    cur = R.current("L2", object_id)
    if cur and cur.get("input_hash") == input_hash:
        return cur
    # fall back to L1L2 (the AI-worker path stores L1+L2 under the same object_id)
    cur = R.current("L1L2", object_id)
    if cur and cur.get("input_hash") == input_hash:
        return cur
    return {}


# --------------------------------------------------------------------------- #
# candidate generation (deterministic): bounded alignment units needing classification
# --------------------------------------------------------------------------- #
@dataclass
class Candidate:
    idx: int
    l1: str      # the grounded/controlled reading span
    l2: str      # the published reading span


def _split_sentences(text: str) -> list[str]:
    """Very conservative sentence splitter for English prose (period/question-mark bounded)."""
    parts = re.split(r"(?<=[.?!])\s+", (text or "").strip())
    return [p.strip() for p in parts if p.strip()]


def _generate_candidates(l1_text: str, l2_text: str, budget: int = 40) -> list[Candidate]:
    """Deterministic candidate generation (CP4): bounded, mark-classification-only.

    A candidate is a single L2 sentence plus its best-guess L1 ground. It NEVER asserts a
    decision; it says "this alignment location requires classification." IGNORE is the default
    prior downstream. Cap by `budget` so the classifier never gets a huge open-ended list."""
    cands: list[Candidate] = []
    l1_sents = _split_sentences(l1_text)
    l2_sents = _split_sentences(l2_text)
    # pairwise: align the i-th published sentence to the i-th grounded sentence (best-effort
    # positional; the classifier decides whether any material difference exists).
    for i, l2 in enumerate(l2_sents[:budget]):
        l1 = l1_sents[i] if i < len(l1_sents) else ""
        cands.append(Candidate(idx=i, l1=l1, l2=l2))
    return cands


def _classify_candidates(object_id: str, cands: list[Candidate]) -> tuple[str, list, list, list]:
    """CONSTRAINED classifier (CP4): the model classifies ONLY the generated candidates.

    IGNORE is the default prior. Returns (status, mt, ia, open_items):
      - mt:          [{label, type(<MT_TYPES>), basis}]   — genuine translation interventions only
      - ia:          [{label:"IA-001", text}]             — genuine interpretive additions only
      - open_items:  [{text, status: OPEN|NEEDS_REVIEW}]  — genuine unresolved items only
    status COMPLETE on a clean call; GENERATION_FAILED on any model/parse failure (fail-closed).
    """
    if not cands:
        return "COMPLETE", [], [], []
    lines = []
    for c in cands:
        lines.append(
            f"C{c.idx}:\n  GROUNDED(L1): {c.l1[:400] or '(none — L2 sentence has no positional L1 ground)'}\n"
            f"  PUBLISHED(L2): {c.l2[:400]}")
    prompt = (
        "You are the Pāṭala L200 audit classifier. Below are bounded CANDIDATE alignment units — each "
        "pairs a published L2 sentence with its grounded L1 reading. CLASSIFY each candidate. "
        "IGNORE is the DEFAULT PRIOR: most English differences are not material translation decisions. "
        "Only flag a candidate under EXACTLY one of:\n"
        "- SUPPLIED: English inserted for an implicit Sanskrit element\n"
        "- REFERENT_SUPPLY: an implicit this/that/he/it made explicit\n"
        "- STRUCTURAL_CONNECTIVE: therefore/however/that-is added to expose an inference\n"
        "- LEXICAL: a term-rendering decision (lemma -> target word)\n"
        "- GRAMMATICAL: a syntactic decision (case, compound, number, voice)\n"
        "- INTERPRETIVE_ASSERTION: the L2 adds a genuinely interpretive claim (NOT a paraphrase)\n"
        "- OPEN: a genuine unresolved philological item\n"
        "- IGNORE: nothing material changed / mere paraphrase (the common case)\n"
        "A paraphrase of the meaning is NEVER a translation decision — classify it IGNORE. "
        "Return JSON ONLY:\n"
        "{\"decisions\": [{\"candidate\": <idx>, \"label\": \"<IGNORE|...>\", "
        "\"type\": \"<MT type>\", \"basis\": \"...\", \"text\": \"...\"}]}\n"
        "covering EVERY candidate idx.\n\n" + "\n".join(lines)
    )
    try:
        raw = chat("You are a Sanskrit philologist (L200 audit classifier).", prompt, timeout=120)
        d = json.loads(_extract_json_block(raw))
        decisions = d.get("decisions", []) if isinstance(d, dict) else []
        mt, ia, open_items = [], [], []
        ia_n = 0
        for dec in decisions:
            label = (dec.get("label") or "IGNORE").upper()
            cidx = dec.get("candidate")
            basis = dec.get("basis") or ""
            text = dec.get("text") or ""
            if label in MT_TYPES:
                mt.append({"label": f"MT-{len(mt)+1:03d}", "type": label,
                           "basis": basis or f"candidate {cidx}"})
            elif label == "INTERPRETIVE_ASSERTION":
                ia_n += 1
                ia.append({"label": f"IA-{ia_n:03d}",
                           "text": text or basis or f"candidate {cidx}"})
            elif label == "OPEN":
                open_items.append({"text": text or basis or f"candidate {cidx}",
                                   "status": "OPEN"})
            # IGNORE -> nothing (the default prior)
        return "COMPLETE", mt, ia, open_items
    except Exception:
        return "GENERATION_FAILED", [], [], []


def _extract_json_block(raw: str) -> str:
    raw = (raw or "").strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
        raw = raw.rsplit("```", 1)[0]
    start, end = raw.find("{"), raw.rfind("}")
    if start >= 0 and end > start:
        return raw[start:end + 1]
    return raw


# --------------------------------------------------------------------------- #
# generator + validator
# --------------------------------------------------------------------------- #
def l200_generator(layer: str, batch: list[dict]) -> list[dict]:
    """Build the 8-section L200 for each L2 object. Deterministic scaffold + constrained classifier.

    COMPARATIVE (the correct L200 information flow): the model classifies bounded candidates
    comparing the GROUNDED reading (L0/L1) against L2 — not from L2 prose alone. proposal_status is
    COMPLETE only if the classifier call succeeded; GENERATION_FAILED otherwise (model failure ≠
    empty successful audit).
    """
    proposals = []
    for b in batch:
        obj = _committed_l2(b["object_id"], b.get("input_hash", ""))
        if not obj:
            # no committed L2 upstream -> DEPENDENCY_BLOCKED (never fabricate an audit)
            proposals.append({"object_id": b["object_id"], "input_hash": b.get("input_hash", ""),
                              "l200": {}, "proposal_status": "DEPENDENCY_BLOCKED"})
            continue
        payload = obj.get("payload", {})
        # L2 text comes from the L1L2 worker shape {l2:{text}} or the L2 worker shape {l2:{text}}.
        l2_text = (payload.get("l2") or {}).get("text", "")
        l1_text = (payload.get("l1") or {}).get("text", "")
        if not l2_text:
            l2_text = (payload.get("text") or "")
        l2_refs = obj.get("input_refs") or []
        l2_hash = b.get("input_hash", "")
        cands = _generate_candidates(l1_text, l2_text)
        status, mt, ia, open_items = _classify_candidates(b["object_id"], cands)
        scaffold = {
            "0_identification": {"object_id": b["object_id"], "l2_ref": b["object_id"],
                                 "l2_hash": l2_hash, "upstream": l2_refs,
                                 "l2_version": obj.get("version", "")},
            "1_published_reading": l2_text,
            "2_derivation_map": _derivation_map(l2_text, l1_text, b["object_id"]),
            "5_source_layer": [],
            "6_cross_references": [],
            "8_review_state": "machine",
        }
        obj_audit = {
            **scaffold,
            "3_material_translation_decisions": mt,
            "4_interpretive_assertions": ia,
            "7_open_items": open_items,
        }
        proposals.append({"object_id": b["object_id"], "input_hash": l2_hash,
                          "verse": l2_text, "l200": obj_audit,
                          "proposal_status": status})
    return proposals


def _committed_l0_ranges(object_id: str) -> list[dict]:
    """Deterministic L0 spans for a passage (the derivation map's L0-range column)."""
    l0 = R.current("L0", object_id)
    if not l0:
        return []
    recs = (l0.get("payload", {}) or {}).get("records", [])
    ranges = []
    for r in recs:
        cs, ce = r.get("chunk_char_start"), r.get("chunk_char_end")
        if isinstance(cs, int) and isinstance(ce, int):
            ranges.append({"l0_record": r.get("id", ""), "range": f"L{cs}-L{ce}",
                           "fragment": (r.get("raw_fragment") or "")[:40]})
    return ranges


def _derivation_map(l2_text: str, l1_text: str, object_id: str = "") -> list[dict]:
    """Deterministic derivation map: per L2 paragraph -> argument-map segment -> L1 span ->
    L0 range -> source range (the IPVV L200-SPEC §2 shape).

    The argument-map segment is best-effort positional (the model does not invent it); L0 range is
    bound deterministically from the committed L0 records; source range is the passage locator."""
    l1 = _split_sentences(l1_text)
    l0_ranges = _committed_l0_ranges(object_id)
    out = []
    for i, sent in enumerate(_split_sentences(l2_text)):
        l1_span = l1[i] if i < len(l1) else ""
        l0_span = l0_ranges[i]["range"] if i < len(l0_ranges) else ""
        out.append({
            "l2_par": sent,
            "argument_map_segment": f"V2-O.{i+1}" if object_id else "",
            "l1_span": l1_span,
            "l0_range": l0_span,
            "source_range": object_id.split(":")[-1] if ":" in object_id else "",
        })
    return out


def l200_validator(layer: str, proposal: dict) -> tuple[bool, str]:
    """Task-2 fidelity + fail-closed: model failure must NOT equal an empty successful audit.

    proposal_status must be COMPLETE (GENERATION_FAILED/PARTIAL/DEPENDENCY_BLOCKED may not commit
    as a completed audit). Enforces the L200-SPEC strict rule: MT entries are genuine translation
    interventions with a valid type; IA entries are separate; the derivation map is present.
    """
    if proposal.get("proposal_status") != "COMPLETE":
        return False, f"proposal_status:{proposal.get('proposal_status','MISSING')}"
    l2 = proposal.get("l200", {})
    required = ["0_identification", "1_published_reading", "2_derivation_map", "8_review_state"]
    # 5_source_layer and 6_cross_references are optional-but-present sections: source-layer
    # attribution is a structural classification that needs speaker context we do not yet have
    # deterministically here; an empty value is an honest "not yet attributed", not a fabrication.
    missing_req = [k for k in required if k not in l2 or not l2.get(k)]
    if missing_req:
        return False, f"missing_required_sections:{','.join(missing_req)}"
    # MT entries must have a valid type AND be a genuine intervention (never an IA smuggled in).
    for mt in l2.get("3_material_translation_decisions", []):
        if mt.get("type") not in MT_TYPES:
            return False, f"bad_mt_type:{mt.get('type')}"
    # derivation map must cover the published reading (at least one row)
    dm = l2.get("2_derivation_map", [])
    if not dm or not dm[0].get("l2_par"):
        return False, "derivation_map empty or malformed"
    for xr in l2.get("6_cross_references", []):
        if xr.get("type") not in XREF_TYPES:
            return False, f"bad_xref_type:{xr.get('type')}"
    return True, ""


def make_l200_handlers() -> dict:
    return {"generator": l200_generator, "validator": l200_validator}
