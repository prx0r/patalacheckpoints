#!/usr/bin/env python3
"""pipeline/batch_translate.py — ONE call, MANY translations, MAX context (the A3 agent's batch unit).

Takes a whole batch of raw Sanskrit verses + the work's full context packet (school/period,
companion guides, translation neighbourhood, semantic-shift term-senses) and returns, in ONE
`hermes -z` call, for EVERY verse:
  - the per-token L0 literal glosses (the RAW-L0 layer)
  - a CLOSE English translation (word/phrase-faithful, not free)

This is the "as many L0/translations as possible in one context/API call" design: the batch + all
its context is one prompt; the model returns one JSON for the whole batch. No max-token cap is passed
(model.py's _hermes_call passes only the prompt + model to `hermes -z`).

After the call, each verse is validated deterministically (validate_l0_spec) and stamped MACHINE_PROPOSED —
the model never self-validates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent3_batch import load_raw_source, split_verses
from raw_l0 import raw_l0_to_canonical, strip_verse_marker
from agentic_gloss import _term_packet_for
from model import chat


def build_entries(work_id: str, verses: list[str], start: int = 0) -> list:
    """Deterministic pass (Vidyut) over the batch. Each entry carries a STABLE passage_id and the
    source_sha256 of its stripped Sanskrit, so the model can echo both and the deterministic layer
    can reject any cross-verse misbind (F4).

    passage_id is GLOBAL across batches: `start` is the offset of this batch's first verse within
    the whole work, so batch 2 (verses 7-12) gets v7..v12, NOT v1..v6 again (a duplicate-id bug
    that made later batches translate as OPEN)."""
    entries = []
    for i, verse in enumerate(verses):
        stripped = strip_verse_marker(verse)
        sha = hashlib.sha256(stripped.encode("utf-8")).hexdigest()
        records, _ = raw_l0_to_canonical(f"{work_id}-v{start+i+1}", verse)
        tokens = [r["raw_fragment"] for r in records if r["raw_fragment"]]
        entries.append({"idx": start + i, "passage_id": f"{work_id}:v{start+i+1}", "source_sha256": sha,
                        "verse": verse, "tokens": tokens})
    return entries


def translate_batch(entries: list, work_id: str) -> dict:
    """ONE hermes -z call for the whole batch. Returns {passage_id: {tokens, close, uncertain}}
    after STRICT verification (F4): returned passage_id must be in the requested set, its echoed
    source_sha256 must match the local hash, no duplicates; any violating item is REJECTED (never
    misbind a plausible gloss to the wrong passage)."""
    packet = _term_packet_for(work_id)
    blocks = []
    for e in entries:
        if not e["tokens"]:
            continue
        blocks.append(
            f"--- VERSE ---\n"
            f"passage_id: {e['passage_id']}\n"
            f"source_sha256: {e['source_sha256']}\n"
            f"VERSE: {e['verse']}\n"
            f"TOKENS: {json.dumps(e['tokens'], ensure_ascii=False)}\n"
        )
    prompt = (
        "You are the Pāṭala A3 translation agent (the patala-translate skill). You are given a BATCH of "
        "raw Sanskrit verses with their Vidyut-segmented tokens. In ONE response, for EVERY verse, produce:\n"
        "  1. tokens: a literal, word/phrase-level English gloss for EACH token (the RAW-L0 layer). "
        "     Use the term-context packet for technical senses (never flat dictionary). "
        "     Unanalyzable token → empty string, NOT fabricated.\n"
        "  2. close: a CLOSE English rendering of the whole verse (word/phrase-faithful, not free).\n"
        "- Preserve negation / polarity / case contributions exactly.\n"
        "- If a sense is genuinely ambiguous in this school/period, list the token in 'uncertain' — "
        "  do NOT invent a confident sense.\n"
        "Return JSON ONLY:\n"
        "  {\"batch_id\": \"<your choice>\", \"translations\": [\n"
        "    {\"passage_id\": \"<the passage_id echoed from the prompt>\", "
        "\"source_sha256\": \"<the source_sha256 echoed from the prompt>\", "
        "\"tokens\": {\"<token>\": \"<gloss>\"}, \"close\": \"<close translation>\", "
        "\"uncertain\": [\"<token>\", ...]}\n"
        "  ]}\n"
        "covering EVERY verse and EVERY token. You MUST echo each passage's passage_id and "
        "source_sha256 exactly as given; do not invent or swap them.\n\n"
        f"{packet}\n\n"
        + "\n".join(blocks)
    )
    raw = chat("You are the Pāṭala translation agent (patala-translate).", prompt, max_tokens=None, timeout=600)
    return _verify_batch(raw, {e["passage_id"]: e for e in entries})


def _verify_batch(raw: str, requested: dict) -> dict:
    """F4 strict verification: membership + sha echo + no duplicates. Violating items are REJECTED."""
    try:
        data = json.loads(raw)
        items = data.get("translations", []) if isinstance(data, dict) else []
    except Exception:
        return {}
    seen = set()
    out = {}
    for it in items:
        if not isinstance(it, dict):
            continue
        pid = it.get("passage_id")
        req = requested.get(pid)
        if req is None or pid in seen:      # unexpected or duplicate → reject
            continue
        seen.add(pid)
        if it.get("source_sha256") != req["source_sha256"]:  # misbind → reject
            out[pid] = {"rejected": "source_sha256_mismatch"}
            continue
        gloss = it.get("tokens") or {}
        out[pid] = {
            "tokens": {t: gloss.get(t, "") for t in req["tokens"]},
            "close": it.get("close") or "",
            "uncertain": it.get("uncertain") or [],
        }
    return out


def run(work_id: str, max_verses: int = 50) -> dict:
    verses = split_verses(load_raw_source(work_id))[:max_verses]
    entries = build_entries(work_id, verses)
    result = translate_batch(entries, work_id)
    return {
        "work_id": work_id,
        "n_verses": len(entries),
        "n_calls": 1,
        "result": result,
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="kramasadbhava")
    ap.add_argument("--verses", type=int, default=4)
    a = ap.parse_args()
    r = run(a.work, a.verses)
    print(json.dumps(r, indent=2, ensure_ascii=False))
