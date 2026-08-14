#!/usr/bin/env python3
"""pipeline/register_harvest_sources.py — batch-register the extracted harvest verses as SOURCE objects.

Efficient batched intake (the factory's per-work _register_source is O(registry-size) per work, which
does not scale to ~1.7M verses). This builds all entries in memory and commits in ONE commit_batch pass.

It registers SOURCE objects named <work_id>:v<i> for every verse in the extracted <work>.jsonl files
(GRETIL/SARIT/MUKTABODHA), with input_hash = sha256(verse) == the jsonl source_sha256 (the factory
contract). Idempotent: skips object_ids already in the registry.

Usage:
  python3 pipeline/register_harvest_sources.py          # register all extracted works
  python3 pipeline/register_harvest_sources.py --limit 50000   # cap (test)
  python3 pipeline/register_harvest_sources.py --dry-run        # report only
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "pipeline"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

TRANS_DIR = ROOT / "data" / "corpus" / "downloads" / "translations"

# the extracted harvest jsonl files (the factory-runnable sources)
HARVEST_PREFIXES = ("sa_", "astaprakarana", "astavakragita", "asvaghosa")


def collect_entries(limit: int = 0, dry_run: bool = False):
    import object_registry as R
    existing = set(R._load("SOURCE")["objects"].keys())
    entries = []
    seen_oids = set(existing)
    for f in sorted(TRANS_DIR.glob("*.jsonl")):
        wid = f.name.replace(".jsonl", "")
        if not wid.startswith(HARVEST_PREFIXES):
            continue
        for line in f.open(encoding="utf-8"):
            try:
                r = json.loads(line)
            except Exception:  # noqa: BLE001
                continue
            verse = (r.get("sanskrit") or "").strip()
            if not verse:
                continue
            oid = f"{wid}:v{r.get('verse_idx', 0)}"
            if oid in seen_oids:
                continue
            h = hashlib.sha256(verse.encode("utf-8")).hexdigest()
            entries.append({"object_id": oid, "input_hash": h,
                            "payload": {"verse": verse, "source_text": verse,
                                        "source": r.get("_source", ""),
                                        "provenance": {"status": "MACHINE_PROPOSED",
                                                       "source": r.get("_source", ""),
                                                       "work_id": wid}}})
            seen_oids.add(oid)
            if limit and len(entries) >= limit:
                return entries
    return entries


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--chunk", type=int, default=20000, help="entries per commit_batch call (bounded memory)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    entries = collect_entries(a.limit, a.dry_run)
    print(f"collected {len(entries)} new SOURCE entries (not already in the registry)")
    if a.dry_run or not entries:
        print("DRY-RUN (or none to add) — no writes")
        return 0
    import object_registry as R
    total = 0
    for i in range(0, len(entries), a.chunk):
        R.commit_batch("SOURCE", entries[i:i + a.chunk], "harvest-verse-intake")
        total += a.chunk if i + a.chunk <= len(entries) else len(entries) - i
        s = R.summary()
        print(f"  chunk {i//a.chunk + 1}: committed {total} so far; SOURCE now {s['SOURCE']['objects']}", flush=True)
    s = R.summary()
    print(f"committed {total}; SOURCE registry now: {s['SOURCE']['objects']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
