#!/usr/bin/env python3
"""pipeline/l1_l2_translate.py — the AI translation worker (GENERATE_TRANSLATION stage).

The point of the factory: consume committed L0 objects and let the MODEL produce
provenance-bound L1 (controlled) + L2 (readable) translations. This is the generative
engine that runs unattended for hours.

Bounded, fail-closed, idempotent:
  - committed L0 (from registry) -> a bounded batch of passages
  - ONE model call per batch via the Direct adapter (fast, structured) — NOT slow hermes -z
  - strict F4 binding: model echoes passage_id + input_hash; wrong/missing/duplicate -> reject
  - output stamped MACHINE_PROPOSED (never ACCEPTED) + full provenance
  - validator: provenance resolves to committed L0; non-empty; no silent omission
  - empty/malformed/timeout -> the item FAILS, neighbors continue (never block the batch)

Semantic imperfection is allowed to commit (it is MACHINE_PROPOSED). Wrong passage / empty /
hash mismatch / malformed -> FAIL, never commit.
"""
from __future__ import annotations
import json, os, sys, hashlib, time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import object_registry as R
from model_adapter import get_adapter
from agentic_gloss import _term_packet_for


def _resolve_l0(batch: list[dict]) -> dict:
    """Map passage_id -> committed L0 object (the authoritative input for translation)."""
    out = {}
    for b in batch:
        l0 = R.current("L0", b["object_id"])
        if l0 and l0.get("input_hash") == b.get("input_hash"):
            out[b["object_id"]] = l0
    return out


def _l0_verse_text(l0: dict) -> str:
    return (l0.get("payload", {}) or {}).get("verse", "")


def _build_prompt(entries, work_id):
    packet = _term_packet_for(work_id)
    blocks = []
    for e in entries:
        verse = _l0_verse_text(e["l0"])
        tokens = [r["raw_fragment"] for r in e["l0"]["payload"].get("records", []) if r["raw_fragment"]]
        blocks.append(
            f"--- VERSE ---\n"
            f"passage_id: {e['passage_id']}\n"
            f"input_hash: {e['input_hash']}\n"
            f"VERSE: {verse}\n"
            f"TOKENS: {json.dumps(tokens, ensure_ascii=False)}\n"
        )
    return (
        "You are the Pāṭala AI translation worker. You are given a batch of raw Sanskrit verses with "
        "their Vidyut-segmented tokens and the work's term-context packet. For EVERY verse produce a "
        "careful scholarly translation in the Pāṭala house style:\n"
        "  1. close: a word/phrase-faithful CONTROLLED rendering (L1) — technical terms retained "
        "     (śakti, kula, krama, vimarśa, prakāśa, svātantrya, ...), structurally faithful.\n"
        "  2. readable: a flowing READABLE English rendering (L2) of the same sense.\n"
        "- Preserve negation / polarity / case contributions exactly.\n"
        "- If genuinely ambiguous in this school/period, list the token in 'uncertain' — do not invent a "
        "  confident sense; never fabricate.\n"
        "- Do NOT translate the passage_id or input_hash.\n"
        "Return JSON ONLY:\n"
        "  {\"translations\": [\n"
        "    {\"passage_id\": \"<echoed>\", \"input_hash\": \"<echoed>\", "
        "\"close\": \"<controlled L1>\", \"readable\": \"<readable L2>\", \"uncertain\": [\"<token>\",...]}\n"
        "  ]}\n"
        "covering EVERY verse. Echo each passage_id and input_hash exactly; never invent or swap them.\n\n"
        f"{packet}\n\n" + "\n".join(blocks)
    )


def _verify(raw: str, requested: dict) -> dict:
    """F4 strict: membership + input_hash echo + no duplicates. Violations rejected."""
    try:
        data = json.loads(raw)
        items = data.get("translations", []) if isinstance(data, dict) else []
    except Exception:
        return {"_error": "non_json", "_rejected_all": [p for p in requested]}
    seen = set()
    out = {}
    for it in items:
        if not isinstance(it, dict):
            continue
        pid = it.get("passage_id")
        req = requested.get(pid)
        if req is None or pid in seen:
            continue
        seen.add(pid)
        if it.get("input_hash") != req["input_hash"]:
            out[pid] = {"_rejected": "input_hash_mismatch"}
            continue
        out[pid] = {
            "close": (it.get("close") or "").strip(),
            "readable": (it.get("readable") or "").strip(),
            "uncertain": it.get("uncertain") or [],
        }
    missing = [p for p in requested if p not in out and p not in seen]
    if missing:
        out["_partial_missing"] = missing
    return out


def _translate_batch_entries(entries, work_id, model="deepseek-v4-flash", attempts=3):
    requested = {e["passage_id"]: e for e in entries}
    prompt = _build_prompt(entries, work_id)
    adapter = get_adapter()
    last = None
    for a in range(attempts):
        res = adapter.complete_json(
            "You are the Pāṭala AI translation worker (GENERATE_TRANSLATION).",
            prompt, model=model, timeout=120)
        raw = res.content if res.ok else ""
        if not res.ok:
            last = res.error
            continue
        out = _verify(raw, requested)
        # accept if at least one clean item came back (partial allowed; neighbors proceed)
        clean = [p for p, v in out.items() if isinstance(v, dict) and not v.get("_rejected")]
        if clean:
            return out
        last = "no clean translations in response"
    return {"_error": last, "_rejected_all": list(requested)}


def l1l2_generator(layer: str, batch: list[dict]) -> list[dict]:
    """Model-driven L1/L2 for a bounded batch of committed-L0 passages.

    batch: [{object_id, input_hash, ...}]. Returns proposals (one per passage) that
    pass provenance/mechanical validation. A passage the model didn't return cleanly
    is simply ABSENT (the controller validator will not see it -> not committed)."""
    l0s = _resolve_l0(batch)
    entries = []
    for b in batch:
        l0 = l0s.get(b["object_id"])
        if not l0:
            continue   # no committed L0 -> cannot translate -> skip
        entries.append({"passage_id": b["object_id"], "input_hash": b["input_hash"],
                        "l0": l0})
    if not entries:
        return []

    # bounded sub-batches (default 6) so one big call does not stall; each call independent
    CHUNK = int(os.environ.get("PATALA_BC", "6"))
    proposals = []
    for start in range(0, len(entries), CHUNK):
        sub = entries[start:start + CHUNK]
        res = _translate_batch_entries(sub, _work_id(sub[0]["passage_id"]))
        if "_error" in res:
            continue   # whole sub-batch failed to generate; skip (neighbors in other chunks proceed)
        for e in sub:
            if e["passage_id"] in res and "_rejected" not in res[e["passage_id"]]:
                tr = res[e["passage_id"]]
                close = tr.get("close", "")
                readable = tr.get("readable", "")
                if not close and not readable:
                    continue   # empty -> honest no-commit
                l0 = e["l0"]
                l0_recs = l0["payload"].get("records", [])
                proposals.append({
                    "object_id": e["passage_id"],
                    "input_hash": e["input_hash"],
                    "layer": "L1L2",
                    "l1": {"text": close,
                           "provenance": {"passage_id": e["passage_id"],
                                          "l0_version": l0.get("version", ""),
                                          "l0_input_hash": l0.get("input_hash", ""),
                                          "input_hash": e["input_hash"]}},
                    "l2": {"text": readable,
                           "provenance": {"passage_id": e["passage_id"],
                                          "l0_version": l0.get("version", ""),
                                          "l0_input_hash": l0.get("input_hash", ""),
                                          "input_hash": e["input_hash"]}},
                    "_generation_status": "MACHINE_PROPOSED",
                })
    return proposals


def _work_id(passage_id: str) -> str:
    return passage_id.split(":")[0] if ":" in passage_id else ""


def l1l2_validator(layer: str, proposal: dict) -> tuple[bool, str]:
    # provenance must resolve to a committed L0
    l0 = R.current("L0", proposal["object_id"])
    if not l0:
        return False, "no committed L0 for translation"
    prov = proposal.get("l1", {}).get("provenance", {})
    if prov.get("l0_version") != l0.get("version"):
        return False, "L1 provenance does not resolve to committed L0"
    if not proposal.get("l1", {}).get("text") and not proposal.get("l2", {}).get("text"):
        return False, "empty translation (no commit)"
    return True, ""


def make_l1l2_handlers() -> dict:
    return {"generator": l1l2_generator, "validator": l1l2_validator}
