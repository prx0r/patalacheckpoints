#!/usr/bin/env python3
"""pipeline/register_sources.py — one-time intake: register translated works into the SOURCE registry.

Bridges the RAW→EN runner to the factory:
  - the live runner writes data/corpus/downloads/translations/<work>.jsonl (raw EN step);
  - the factory consumes committed SOURCE objects (per verse) in the object registry.

Any work that has a translated <work>.jsonl but no committed SOURCE objects is not yet in the
factory queue. This intake registers those verses as SOURCE objects (dedup by verse content hash),
so the factory scheduler picks the work up and advances it SOURCE→T1→L0→ARGMAP→L2→L200→C1.

This runs as a standalone step (NOT inside the scheduler hot loop) because committing each verse
rewrites the registry file; it is fast enough per-work and intended to be run after the runner has
made progress (e.g. manually, or from a watchdog on a coarse interval).

Usage:
  python3 pipeline/register_sources.py                # register all translated-but-unregistered works
  python3 pipeline/register_sources.py --work <wid>   # register just one work
  python3 pipeline/register_sources.py --dry-run      # report what WOULD be registered (no writes)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")
import object_registry as R

TDIR = Path("/root/projects/patala/data/corpus/downloads/translations")


def _work_registered(wid: str) -> bool:
    return any(oid.startswith(wid) for oid in R._load("SOURCE")["objects"])


def _verses_of(wid: str) -> list[str]:
    verses = []
    tpath = TDIR / f"{wid}.jsonl"
    if not tpath.exists():
        return verses
    for line in tpath.open(encoding="utf-8"):
        try:
            r = json.loads(line)
            v = (r.get("sanskrit") or "").strip()
            if v:
                verses.append(v)
        except Exception:
            continue
    return verses


def register_work(wid: str, dry_run: bool = False) -> int:
    if _work_registered(wid):
        return 0
    verses = _verses_of(wid)
    if not verses:
        return 0
    if dry_run:
        return len(verses)
    # load existing committed SOURCE object_ids ONCE (avoid a full registry read per verse)
    existing = set(R._load("SOURCE")["objects"].keys())
    # content-hash index of ALL committed SOURCE input_hashes, so the same verse text is never
    # re-registered under a different (e.g. typo'd/underscore-vs-plain) work id (AGENTS.md: dedup by
    # content, not name). A verse whose content hash already exists is skipped regardless of name.
    all_source_hashes = set()
    for oid, vs in R._load("SOURCE")["objects"].items():
        for v in vs:
            all_source_hashes.add(v.get("input_hash", ""))
    entries = []
    for i, v in enumerate(verses):
        oid = f"{wid}:v{i+1}"
        if oid in existing:
            continue
        h = hashlib.sha256(v.encode("utf-8")).hexdigest()
        if h in all_source_hashes:
            continue  # content already committed under some work id — skip (prevents duplicate intake)
        entries.append({"object_id": oid, "input_hash": h,
                        "payload": {"verse": v, "source_text": v}})
    R.commit_batch("SOURCE", entries, created_by="register-sources-intake")
    return len(entries)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default=None, help="register just this work (else all translated works)")
    ap.add_argument("--dry-run", action="store_true", help="report what would be registered (no writes)")
    a = ap.parse_args()

    if a.work:
        ids = [a.work]
    else:
        ids = sorted(p.stem for p in TDIR.glob("*.jsonl"))
    ids = [w for w in ids if not _work_registered(w)]

    total_objs = 0
    for wid in ids:
        n = register_work(wid, dry_run=a.dry_run)
        total_objs += n
        if n or a.dry_run:
            tag = "WOULD register" if a.dry_run else "registered"
            print(f"{wid:45} {tag} {n} SOURCE objects", flush=True)

    print(f"\n{'[dry-run] would register ' if a.dry_run else 'registered '}{len(ids)} work(s), "
          f"{total_objs} SOURCE objects total", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
