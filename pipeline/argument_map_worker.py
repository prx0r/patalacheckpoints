#!/usr/bin/env python3
"""pipeline/argument_map_worker.py — the ARGUMENT MAP layer handler (A2-CP3).

Per the locked canonical stack + `pilot_*_ARGUMENT_MAP.md` exemplars: the argument map reconstructs a
passage's ARGUMENT structure before prose is written — the lateral guide that unlocks L2. It is NOT a
translation and NOT a commentary. Canonical shape (from `pilot_V2O_ARGUMENT_MAP.md`):
  1. what_is_at_issue   the question / the passage's move (what is being established)
  2. argument_steps     the plan / kārikās / steps, reconstructed step by step
  3. open_items         genuinely unresolved / uncertain (never invented)
  4. decision_for_l2    the decision that guides the readable L2

ROLE SPLIT: Agent 2 = MAKE THE FACTORY RUN. This worker produces the canonical argument-map object with
deterministic validation (production gate -> MACHINE_PROPOSED). The *structural/semantic fidelity* of the
map is Agent 1's evals lane (ARGMAP-EVAL). Agent 2 does NOT need a passed gold benchmark to move on.

Production contract (deterministic):
  - canonical shape: the 4 sections present + well-formed
  - source binding: the map references the passage (object_id) + its source/T1
  - provenance: input_hash bound; status MACHINE_PROPOSED
  - fail-closed: model failure / bad JSON -> no partial commit
  - abstention-honest: open_items are genuine OPEN/uncertain, never fabricated conclusions
"""
from __future__ import annotations

import hashlib
import json
import sys

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R
from model import chat

REQUIRED_SECTIONS = ["what_is_at_issue", "argument_steps", "open_items", "decision_for_l2"]


def _context(object_id: str) -> dict:
    """Gather committed SOURCE + T1 + L0 for the passage as the map's grounding input."""
    ctx = {"object_id": object_id, "verse": "", "t1_gloss": "", "l0_tokens": []}
    # SOURCE verse (via T1's source_text, or the live-runner file)
    t1 = R.current("T1", object_id)
    if t1:
        ctx["t1_gloss"] = " ".join(t.get("form", "") for t in
                                   (t1.get("payload", {}).get("t1", {}) or {}).get("tokens", []))
        ctx["verse"] = (t1.get("payload", {}).get("t1", {}) or {}).get("source_text", "")
    l0 = R.current("L0", object_id)
    if l0:
        recs = (l0.get("payload", {}) or {}).get("records", [])
        ctx["l0_tokens"] = [r.get("raw_fragment", "") for r in recs if r.get("raw_fragment")]
    return ctx


def _build_prompt(object_id: str, ctx: dict) -> str:
    return (
        "You are the Pāṭala argument-map producer. Reconstruct the ARGUMENT structure of the passage "
        "below, BEFORE prose is written. This is the lateral guide that unlocks the readable L2.\n"
        "Produce EXACTLY these 4 sections (canonical shape):\n"
        "1. what_is_at_issue: the question the passage addresses / the move it makes — what it is "
        "   establishing, in 1-3 sentences.\n"
        "2. argument_steps: the argument reconstructed step by step — the plan / kārikā / verse-scheme "
        "   / the steps in order. Be faithful to the source; do not invent an argument the source "
        "   doesn't license.\n"
        "3. open_items: list of genuinely unresolved / uncertain items (each with a status OPEN | "
        "   NEEDS_REVIEW). Leave empty if none.\n"
        "4. decision_for_l2: the one-sentence decision that guides the readable L2 rendering.\n"
        "Return JSON ONLY:\n"
        "{\"what_is_at_issue\":\"...\",\"argument_steps\":[\"...\"],"
        "\"open_items\":[{\"text\":\"...\",\"status\":\"OPEN|NEEDS_REVIEW\"}],"
        "\"decision_for_l2\":\"...\"}\n\n"
        f"# PASSAGE\nobject_id: {object_id}\nverse: {ctx['verse']}\n"
        f"# T1 TRANSLITERAL GLOSS\n{ctx['t1_gloss'][:1500]}\n"
        f"# L0 TOKENS\n{', '.join(ctx['l0_tokens'][:60])}"
    )


def _parse(raw: str) -> dict:
    raw = (raw or "").strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
        raw = raw.rsplit("```", 1)[0]
    start, end = raw.find("{"), raw.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("no JSON object in argument-map model output")
    return json.loads(raw[start:end + 1])


def argmap_generator(layer: str, batch: list[dict]) -> list[dict]:
    proposals = []
    for b in batch:
        oid = b["object_id"]
        ctx = _context(oid)
        if not ctx["verse"] and not ctx["t1_gloss"]:
            # no committed T1 upstream -> dependency (never fabricate a map from nothing)
            proposals.append({"object_id": oid, "input_hash": b.get("input_hash", ""),
                              "argument_map": {}, "argmap_status": "DEPENDENCY_BLOCKED"})
            continue
        try:
            raw = chat("You are the Pāṭala argument-map producer (lateral guide for L2).",
                       _build_prompt(oid, ctx), timeout=180)
            data = _parse(raw)
            # deterministic coercion to the canonical 4-section shape
            body = {
                "what_is_at_issue": (data.get("what_is_at_issue") or "").strip(),
                "argument_steps": [s for s in (data.get("argument_steps") or []) if isinstance(s, str) and s.strip()],
                "open_items": data.get("open_items") or [],
                "decision_for_l2": (data.get("decision_for_l2") or "").strip(),
            }
            proposals.append({"object_id": oid, "input_hash": b.get("input_hash", "") or _hash(oid),
                              "argument_map": body, "argmap_status": "MACHINE_PROPOSED",
                              "source_object": oid})
        except Exception:
            proposals.append({"object_id": oid, "input_hash": b.get("input_hash", "") or _hash(oid),
                              "argument_map": {}, "argmap_status": "GENERATION_FAILED"})
    return proposals


def _hash(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def argmap_validator(layer: str, proposal: dict) -> tuple[bool, str]:
    """Deterministic argument-map production gate (canonical shape + provenance + fail-safe)."""
    if proposal.get("argmap_status") != "MACHINE_PROPOSED":
        return False, f"argmap_status:{proposal.get('argmap_status','MISSING')}"
    m = proposal.get("argument_map", {})
    # canonical shape: all 4 required sections present; at-issue + decision non-empty
    for s in REQUIRED_SECTIONS:
        if s not in m:
            return False, f"missing_section:{s}"
    if not (m.get("what_is_at_issue") or "").strip():
        return False, "missing what_is_at_issue"
    if not (m.get("decision_for_l2") or "").strip():
        return False, "missing decision_for_l2"
    # argument_steps: at least one step
    if not m.get("argument_steps"):
        return False, "missing argument_steps"
    # open_items well-formed (status enum)
    for oi in m.get("open_items", []):
        if oi.get("status") not in ("OPEN", "NEEDS_REVIEW"):
            return False, f"bad_open_item_status:{oi.get('status')}"
    # provenance: source_object + input_hash
    if not proposal.get("source_object"):
        return False, "missing source_object"
    if not proposal.get("input_hash"):
        return False, "missing input_hash"
    return True, ""


def make_argmap_handlers() -> dict:
    return {"generator": argmap_generator, "validator": argmap_validator}
