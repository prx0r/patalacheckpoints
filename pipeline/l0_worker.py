#!/usr/bin/env python3
"""pipeline/l0_worker.py — the L0 layer handler for the autonomy controller.

The real L0 production: deterministic RAW-L0 (Vidyut) + agentic batch gloss -> canonical records ->
validate_l0_spec (P0 + schema + abstraction + gloss) -> commit. This is what the controller's L0
eligibility feeds. Fail-closed: an unvalidated proposal is REJECTED, never committed.
"""
from __future__ import annotations

import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from raw_l0 import raw_l0_to_canonical, raw_l0, strip_verse_marker
from agentic_gloss import run_batch
from validate_l0_spec import validate
from agent3_batch import split_verses


def source_objects(work_id: str, source_text: str) -> list[dict]:
    """List a work's passages as SOURCE registry objects (stable object_id + input_hash)."""
    verses = split_verses(source_text)
    objs = []
    for i, v in enumerate(verses):
        stripped = strip_verse_marker(v)
        objs.append({"object_id": f"{work_id}:v{i+1}",
                     "input_hash": hashlib.sha256(stripped.encode("utf-8")).hexdigest(),
                     "verse": v})
    return objs


def l0_generator(layer: str, batch: list[dict]) -> list[dict]:
    """Real L0 for a bounded batch of source passages: deterministic + batch gloss -> proposals."""
    entries = []
    for i, b in enumerate(batch):
        records, _ = raw_l0_to_canonical(b["object_id"], b["verse"])
        tokens = [r["raw_fragment"] for r in records if r["raw_fragment"]]
        entries.append({"idx": i, "verse": b["verse"], "tokens": tokens, "records": records,
                        "passage_id": b["object_id"]})
    gloss_lookup = {}
    glossable = [e for e in entries if e["tokens"]]
    if glossable:
        # bound each model call: chunk the gloss into sub-batches (default 8) so one
        # giant batch does not overload/stall the model (the autonomous-run lesson)
        CHUNK = int(os.environ.get("PATALA_GLOSS_CHUNK", "8"))
        for start in range(0, len(glossable), CHUNK):
            for g in run_batch(glossable[start:start + CHUNK], layer):
                gloss_lookup[g["idx"]] = g["gloss_map"]
    proposals = []
    for i, e in enumerate(entries):
        gloss_map = gloss_lookup.get(i) or {t: {"literal": "", "compound": "", "supplied": False}
                                            for t in e["tokens"]}
        recs = raw_l0(e["passage_id"], e["passage_id"], e["verse"], gloss_map)["records"]
        proposals.append({"object_id": e["passage_id"], "input_hash": batch[i]["input_hash"],
                          "verse": e["verse"], "records": recs})
    return proposals


def l0_validator(layer: str, proposal: dict) -> tuple[bool, str]:
    """Un-cheatable gate: schema + P0 + abstraction-honesty + gloss (the model does not control it)."""
    v = validate(proposal["records"], chunk_text=strip_verse_marker(proposal["verse"]))
    return v["PASS"], ("" if v["PASS"] else "validate_l0_spec FAIL")


def make_l0_handlers() -> dict:
    return {"generator": l0_generator, "validator": l0_validator}
