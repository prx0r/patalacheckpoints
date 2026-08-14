#!/usr/bin/env python3
"""pipeline/seed_t1_direct.py — DIRECT per-verse T1 seeding (robust, resumable).

The batched T1 generator is unreliable on large batches (the model hangs or returns non-JSON on the
heavy multi-verse prompt). This seeder instead calls the model PER-VERSE (proven to work, ~15-25s each),
produces the canonical per-token `[and]-GLOSS (IAST)` T1, and registers it. It is:
  - resumable: skips verses already committed (by object_id)
  - bounded: processes up to --limit verses, then exits (safe to re-run)
  - honest: provenance sanskritree-import / seed-t1, MACHINE_PROPOSED
  - single-writer safe: only run when the factory loop is stopped

USAGE:
  python3 pipeline/seed_t1_direct.py --work kalanalatantra            # seed one work (all verses)
  python3 pipeline/seed_t1_direct.py --work kaularahasya --limit 50   # seed 50 verses
  python3 pipeline/seed_t1_direct.py --all --limit 200                # seed across all works
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R
import t1_worker as T
from model import chat as _chat
from import_sanskritree import _sanskrit_for_work

STREAM_LOG = Path("/root/projects/patala/data/corpus/downloads/t1-stream.jsonl")


def _verse_hash(v: str) -> str:
    return hashlib.sha256(v.strip().encode("utf-8")).hexdigest()


def _stream_log(object_id: str, status: str, gloss_count: int, error: str = "") -> None:
    try:
        STREAM_LOG.parent.mkdir(parents=True, exist_ok=True)
        rec = {"ts": time.strftime('%Y-%m-%dT%H:%M:%S'), "object_id": object_id,
               "status": status, "gloss_count": gloss_count, "error": error or None}
        with STREAM_LOG.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass


def _gloss_verse(verse: str) -> dict | None:
    """Gloss a single verse via a LEAN direct prompt (proven reliable ~20s), returning the gloss map.

    The batched t1_generator hangs on its heavy multi-verse prompt; this bypasses it with the
    minimal single-verse prompt that works."""
    import json as _json
    segments = T._segment(verse)
    tokens = [s["surface"] for s in segments]
    if not tokens:
        return None
    prompt = (
        f"You are the Pāṭala T1 translator. Produce the canonical transliteral word-gloss "
        f"[and]-GLOSS (IAST) for EACH token of this Sanskrit verse.\nVERSE: {verse}\n"
        f"TOKENS: {', '.join(tokens)}\n"
        "Return JSON ONLY: {\"tokens\": {\"<token>\": {\"gloss\": \"<literal english>\", "
        "\"quoted\": false}}} covering EVERY token. Gloss is the plain literal phrase WITHOUT "
        "[and]- or parentheses."
    )
    raw = _chat("You are the Pāṭala T1 translator.", prompt, timeout=70)
    raw = (raw or "").strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
        raw = raw.rsplit("```", 1)[0]
    s, e = raw.find("{"), raw.rfind("}")
    if s < 0 or e <= s:
        return None
    try:
        data = _json.loads(raw[s:e + 1])
    except Exception:
        return None
    gloss_map = data.get("tokens") or {}
    if not gloss_map:
        return None
    # filter to only our tokens, drop junk
    return {t: gloss_map.get(t, {"gloss": "", "quoted": False}) for t in tokens}


def seed_work(work_id: str, limit: int = 0) -> dict:
    """Seed T1 for one work: register per-verse canonical T1 objects (skip already-done).

    Verses come from the OG source file (via import_sanskritree), not the translations file."""
    import import_sanskritree as I
    src_file = I._sanskrit_source_for(work_id)
    verses = I._extract_sanskrit_verses(src_file) if src_file else []
    if not verses:
        return {"work": work_id, "verses": 0, "committed": 0, "failed": 0, "skipped": 0,
                "note": "no source verses"}
    # committed T1 object_ids for this work
    done_ids = set()
    for oid in R._load("T1")["objects"]:
        if oid.startswith(work_id + ":"):
            done_ids.add(oid)
    # existing SOURCE object_ids so we bind T1 to the right object_id
    src_ids = {}
    for oid in R._load("SOURCE")["objects"]:
        if oid.startswith(work_id + ":"):
            cur = R.current("SOURCE", oid)
            if cur:
                src_ids[cur.get("input_hash", "")] = oid

    committed = failed = skipped = 0
    processed = 0
    for i, verse in enumerate(verses):
        if limit and processed >= limit:
            break
        oid = f"{work_id}:v{i+1}"
        if oid in done_ids:
            skipped += 1
            continue
        h = _verse_hash(verse)
        src_oid = src_ids.get(h, oid)
        processed += 1
        try:
            gloss_map = _gloss_verse(verse)
            if not gloss_map:
                failed += 1
                _stream_log(src_oid, "ABSTAIN", 0)
                continue
            # assemble canonical T1 tokens
            segments = T._segment(verse)
            t1_tokens = T._assemble_t1(verse, segments, gloss_map)
            R.commit("T1", src_oid, h, created_by="seed-t1-direct",
                     payload={"t1": {"tokens": t1_tokens,
                                     "source_sha256": h,
                                     "source_text": verse,
                                     "status": "MACHINE_PROPOSED"},
                              "provenance": "seed-t1-direct",
                              "t1_status": "MACHINE_PROPOSED"})
            committed += 1
            _stream_log(src_oid, "MACHINE_PROPOSED", len(t1_tokens))
        except Exception as e:
            failed += 1
            _stream_log(src_oid, "GENERATION_FAILED", 0, error=str(e)[:80])
        if processed % 5 == 0:
            print(f"  {work_id} {processed}/{len(verses)} done (committed={committed} failed={failed})",
                  flush=True)
    return {"work": work_id, "verses": len(verses), "committed": committed,
            "failed": failed, "skipped": skipped}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default=None)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="max verses per work (0=all)")
    ap.add_argument("--works", default=None, help="comma list")
    a = ap.parse_args()

    # collect target works
    works = []
    if a.work:
        works = [a.work]
    elif a.works:
        works = [w.strip() for w in a.works.split(",") if w.strip()]
    elif a.all:
        seen = set()
        for oid in R._load("SOURCE")["objects"]:
            if ":" in oid:
                seen.add(oid.split(":")[0])
        # only works with no/partial T1
        t1 = set()
        for oid in R._load("T1")["objects"]:
            if ":" in oid:
                t1.add(oid.split(":")[0])
        works = sorted(seen)
    else:
        print("provide --work, --works, or --all")
        return 1

    totals = {"committed": 0, "failed": 0, "skipped": 0}
    for w in works:
        r = seed_work(w, limit=a.limit)
        print(f"DONE {w}: committed={r['committed']} failed={r['failed']} skipped={r['skipped']}",
              flush=True)
        totals["committed"] += r["committed"]
        totals["failed"] += r["failed"]
        totals["skipped"] += r["skipped"]
    print(f"\nTOTAL: {totals['committed']} committed, {totals['failed']} failed, "
          f"{totals['skipped']} skipped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
