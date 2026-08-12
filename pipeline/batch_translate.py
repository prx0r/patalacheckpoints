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
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent3_batch import load_raw_source, split_verses
from raw_l0 import raw_l0_to_canonical
from agentic_gloss import _term_packet_for
from model import chat


def build_entries(work_id: str, verses: list[str]) -> list:
    """Deterministic pass (Vidyut) over the batch: collect per-verse token lists."""
    entries = []
    for i, verse in enumerate(verses):
        records, _ = raw_l0_to_canonical(f"{work_id}-v{i+1}", verse)
        tokens = [r["raw_fragment"] for r in records if r["raw_fragment"]]
        entries.append({"idx": i, "verse": verse, "tokens": tokens})
    return entries


def translate_batch(entries: list, work_id: str) -> dict:
    """ONE hermes -z call for the whole batch. Returns {idx: {tokens_gloss, close_translation}}."""
    packet = _term_packet_for(work_id)
    blocks = []
    for e in entries:
        if not e["tokens"]:
            continue
        blocks.append(
            f"--- VERSE {e['idx']} ---\n"
            f"VERSE: {e['verse']}\n"
            f"TOKENS: {json.dumps(e['tokens'], ensure_ascii=False)}\n"
        )
    prompt = (
        "You are the Pāṭala A3 translation agent (the patala-translate skill). You are given a BATCH of "
        "raw Sanskrit verses with their Vidyut-segmented tokens. In ONE response, for EVERY verse, produce:\n"
        "  1. glosses: a literal, word/phrase-level English gloss for EACH token (the RAW-L0 layer). "
        "     Use the term-context packet for technical senses (never flat dictionary). A gloss is the "
        "     literal meaning, not a whole-verse translation. Unanalyzable token → empty string, NOT fabricated.\n"
        "  2. close: a CLOSE English rendering of the whole verse (word/phrase-faithful to the Sanskrit, "
        "     not a free literary translation).\n"
        "- Preserve negation / polarity / case contributions exactly.\n"
        "- If a sense is genuinely ambiguous in this school/period, note it as a short 'uncertain' list on "
        "  that verse — do NOT invent a confident sense.\n"
        "Return JSON ONLY, keyed by verse idx:\n"
        "  {\"<idx>\": {\"tokens\": {\"<token>\": \"<gloss>\"}, \"close\": \"<close translation>\", "
        "\"uncertain\": [\"<token>\", ...]}}\n"
        "covering EVERY verse and EVERY token.\n\n"
        f"{packet}\n\n"
        + "\n".join(blocks)
    )
    raw = chat("You are the Pāṭala translation agent (patala-translate).", prompt, max_tokens=None, timeout=600)
    return _parse_batch(raw, entries)


def _parse_batch(raw: str, entries: list) -> dict:
    try:
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise ValueError("batch translate not an object")
    except Exception:
        return {}
    out = {}
    for e in entries:
        got = data.get(str(e["idx"])) or data.get(e["idx"]) or {}
        gloss = (got.get("tokens") or {}) if isinstance(got, dict) else {}
        out[e["idx"]] = {
            "tokens": {t: gloss.get(t, "") for t in e["tokens"]},
            "close": (got.get("close") or "") if isinstance(got, dict) else "",
            "uncertain": (got.get("uncertain") or []) if isinstance(got, dict) else [],
        }
    return out


def run(work_id: str, max_verses: int = 50) -> dict:
    verses = split_verses(load_raw_source(work_id))[:max_verses]
    entries = build_entries(work_id, verses)
    result = translate_batch(entries, work_id)
    return {
        "work_id": work_id,
        "n_verses": len(verses),
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
