#!/usr/bin/env python3
"""pipeline/agentic_translate.py — drive hermes as an AGENT (file access), not a blind -z model.

The core correction: the previous RAW->EN and factory paths called `hermes -z` (one-shot text mode,
NO file access, NO tools), so the model was blind to the repo and returned empty output for most
verses. Hermes is an agent with read/write file tools: it can read the source, the reference maps,
term packets, and the skills itself. This driver hands it a work, lets it pull its own context, and
the driver handles reliable per-verse file I/O + resumable progress (source_sha256 dedup).

Usage:
  python3 pipeline/agentic_translate.py --work kubjika [--batch 8] [--max N] [--detach]
  python3 pipeline/agentic_translate.py --all            # loop every registered work
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

TRANSLATIONS = Path("/root/projects/patala/data/corpus/downloads/translations")
REFERENCE = Path("/root/projects/patala/docs/corpus/canonical_reference_map.md")
HERMES_BIN = os.environ.get("HERMES_BIN", "hermes")
HERMES_PROFILE = os.environ.get("HERMES_PROFILE", "patala")
HERMES_SKILL = os.environ.get("HERMES_SKILL", "translate-passage")


def _source_sha256(verse: str) -> str:
    return hashlib.sha256(verse.strip().encode("utf-8")).hexdigest()


def load_source(work: str) -> list[dict]:
    """Load the raw Sanskrit verses for a work from the live-runner source file.

    The existing translations/<work>.jsonl holds {sanskrit, translation, status, source_sha256, ...}
    records written by the single-file runner; we reuse its 'sanskrit' field as the raw source and
    the whole record as the progress ledger (already-translated verses are skipped by source_sha256).
    """
    path = TRANSLATIONS / f"{work}.jsonl"
    if not path.exists():
        return []
    out = []
    for line in path.open(encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        verse = (r.get("sanskrit") or "").strip()
        if not verse:
            continue
        # reuse existing hash or compute it
        sha = r.get("source_sha256") or _source_sha256(verse)
        out.append({"sanskrit": verse, "source_sha256": sha})
    return out


def pending_verses(work: str) -> list[dict]:
    """Verses not yet translated (no non-empty translation on disk)."""
    src = load_source(work)
    have = set()
    path = TRANSLATIONS / f"{work}.jsonl"
    if path.exists():
        for line in path.open(encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            if (r.get("translation") or r.get("text") or "").strip():
                have.add(r.get("source_sha256") or _source_sha256((r.get("sanskrit") or "").strip()))
    return [s for s in src if s["source_sha256"] not in have]


def _read_output(work: str) -> dict[str, dict]:
    """Existing complete records keyed by source_sha256 (idempotent resume)."""
    out = {}
    path = TRANSLATIONS / f"{work}.jsonl"
    if path.exists():
        for line in path.open(encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            if (r.get("translation") or "").strip():
                out[r.get("source_sha256")] = r
    return out


def _append_records(work: str, records: list[dict]) -> None:
    path = TRANSLATIONS / f"{work}.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = _read_output(work)
    with path.open("a", encoding="utf-8") as fh:
        for r in records:
            sha = r.get("source_sha256")
            if sha and sha in existing:
                continue  # idempotent: never duplicate
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
            if sha:
                existing[sha] = r


def _hermes_translate(work: str, batch: list[dict]) -> list[dict]:
    """One agentic hermes call for a batch of verses. Hermes reads the repo itself for context.

    Returns [{'sanskrit','translation','source_sha256','status'}]. Uses `hermes chat -q` (agentic,
    file tools) NOT `-z` (blind). Fail-closed: on error returns empty -> caller retries, never writes
    a fabricated/partial record."""
    blocks = "\n".join(f"{i+1}. {v['sanskrit']}" for i, v in enumerate(batch))
    prompt = (
        "You are the Patala translation agent (translate-passage). Translate the following raw "
        "Sanskrit verse(s) into scholarly English prose in the Patala house style.\n"
        "RULES:\n"
        "- Follow the translate-passage skill (already loaded) for the audited per-passage flow.\n"
        "- Preserve technical terms (śakti, kula, krama, vimarśa, prakāśa, svātantrya, spanda, tattva) "
        "using the sense for this work.\n"
        "- Use your FILE TOOLS to read the canonical reference map at "
        f"{REFERENCE} and any term packets in the repo for the correct senses — do NOT guess from a "
        "flat dictionary.\n"
        "- If a verse is corrupt/unreadable, set translation to \"\" (empty) — never fabricate.\n"
        "Return JSON ONLY (no prose, no markdown fences):\n"
        "{\"translations\": [{\"idx\": <i>, \"text\": \"<english translation>\"}]}\n"
        "where idx is 1-based matching the list below. Cover EVERY verse.\n\n"
        "# VERSE LIST\n" + blocks
    )
    cmd = [HERMES_BIN, "chat", "-Q", "-q", prompt, "--yolo", "--max-turns", "8", "--skills", HERMES_SKILL]
    try:
        proc = subprocess.run(cmd, cwd="/root/projects/patala",
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              text=True, timeout=300)
    except subprocess.TimeoutExpired:
        print(f"  [agentic_translate] hermes timeout for {work} batch of {len(batch)}", flush=True)
        return []
    raw = (proc.stdout or "").strip()
    # strip fenced code block if present
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
        raw = raw.rsplit("```", 1)[0]
    data = _extract_json_object(raw)
    if data is None:
        print(f"  [agentic_translate] non-JSON reply for {work}: {raw[-300:]!r}", flush=True)
        return []
    by_idx = {}
    for t in (data.get("translations") or []):
        try:
            by_idx[int(t.get("idx"))] = (t.get("text") or "").strip()
        except Exception:
            continue
    out = []
    for i, v in enumerate(batch, start=1):
        text = by_idx.get(i, "")
        out.append({"sanskrit": v["sanskrit"], "translation": text,
                    "source_sha256": v["source_sha256"],
                    "status": "MACHINE_PROPOSED" if text else "OPEN",
                    "ts": time.strftime('%Y-%m-%dT%H:%M:%S')})
    return out


def _extract_json_object(raw: str):
    """Pull the JSON object containing 'translations' from hermes output (which may carry preamble).

    hermes -Q prints the requested JSON but sometimes with reasoning before/after it. Scan every '{'
    start, find its matching '}' with a depth counter, parse the span, and return the first object
    that actually has a 'translations' key. Tolerates nested braces and surrounding prose."""
    import json as _json
    i = 0
    while True:
        i = raw.find("{", i)
        if i < 0:
            return None
        depth = 0
        j = i
        while j < len(raw):
            c = raw[j]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    try:
                        obj = _json.loads(raw[i:j + 1])
                    except Exception:
                        break
                    if isinstance(obj, dict) and "translations" in obj:
                        return obj
                    break
            j += 1
        i = i + 1


def translate_work(work: str, batch_size: int = 8, max_verses: int = 0) -> dict:
    pending = pending_verses(work)
    if max_verses:
        pending = pending[:max_verses]
    total = len(pending)
    done = 0
    if total == 0:
        return {"work": work, "pending": 0, "translated": 0, "open": 0, "empty": "already done"}
    for start in range(0, total, batch_size):
        batch = pending[start:start + batch_size]
        records = _hermes_translate(work, batch)
        if not records:
            print(f"  {work}: batch {start}-{start+len(batch)} FAILED (no model output); backing off 20s", flush=True)
            time.sleep(20)
            continue
        _append_records(work, records)
        good = sum(1 for r in records if r["translation"])
        done += good
        print(f"  {work}: +{good}/{len(records)} non-empty (cumulative {done}/{total})", flush=True)
        time.sleep(2)  # gentle, coexist with anything else
    return {"work": work, "pending": total, "translated": done,
            "open": total - done, "empty": ""}


def translate_all(batch_size: int = 8, max_verses: int = 0, max_works: int = 0) -> None:
    works = sorted(p.name[:-6] for p in TRANSLATIONS.glob("*.jsonl") if p.name.endswith(".jsonl"))
    if max_works:
        works = works[:max_works]
    for w in works:
        try:
            r = translate_work(w, batch_size, max_verses)
            print(f"DONE {w}: {r}", flush=True)
        except Exception as e:
            print(f"ERROR {w}: {e}", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--work", help="single work id")
    g.add_argument("--all", action="store_true", help="loop all works")
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--max", type=int, default=0, help="max verses per work (0=all)")
    ap.add_argument("--max-works", type=int, default=0)
    a = ap.parse_args()
    if a.work:
        r = translate_work(a.work, a.batch, a.max)
        print(json.dumps(r, indent=2))
    else:
        translate_all(a.batch, a.max, a.max_works)
    return 0


if __name__ == "__main__":
    sys.exit(main())
