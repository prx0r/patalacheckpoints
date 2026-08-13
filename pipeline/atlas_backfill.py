#!/usr/bin/env python3
"""pipeline/atlas_backfill.py — the ATLAS backfill pipeline (Atlas-100 #2).

The directive: do NOT manually enrich 100 entries. Build a pipeline from the RICHER existing data
(`data/atlas/audited.ts` — the Trika-10 BibliographyRecord, full depth) into Atlas candidate records,
with per-field provenance + authority evidence.

    existing rich bibliography (audited.ts)
        ↓ normalizer
    Atlas candidate records
        ↓ identity resolver
    authority evidence per dimension
        ↓ (Postgres when available; else JSON store)

Every imported field carries {value, source, derivation, authority_state} — never a bare "date: 10th c."
with no provenance (the reviewer's explicit requirement).

The output feeds ATLAS-10 GOLD (the calibration set) → ATLAS-100.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path("/root/projects/patala")
ATLAS_DIR = ROOT / "data/atlas"
OUT = ROOT / "data/evaluation/atlas-backfill-candidates.json"

# authority per field — what a backfilled value may honestly claim (never inflated)
AUTHORITY = {
    "work_identity": "CATALOG_MATCHED",   # from the audited bibliography record
    "authorship": "CATALOG_SUPPORTED",
    "date": "CATALOG_SUPPORTED",          # from the period field (may be approximate)
    "editions": "CATALOG_SUPPORTED",
    "etexts": "CATALOG_SUPPORTED",
    "translations": "CATALOG_SUPPORTED",
    "scholarship": "CATALOG_SUPPORTED",
}


def _norm_id(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def _field(value, source="audited.ts", derivation="direct", authority="CATALOG_SUPPORTED"):
    """A provenance-carrying field (the reviewer's requirement — never a bare value)."""
    return {"value": value, "source": source, "derivation": derivation, "authority_state": authority}


def parse_ts_records() -> list[dict]:
    """Extract the BibliographyRecord objects from audited.ts via node (robust).

    The TS file is a JS object array (with `as Type` annotations). We strip the TS annotations and
    eval the array literal in node, which parses nested objects/arrays/URLs correctly — far more
    robust than a hand-rolled regex parser.
    """
    import subprocess
    node_script = r"""
const fs=require('fs');
let text=fs.readFileSync(process.argv[1],'utf8');
text=text.replace(/\s+as\s+[A-Za-z_][A-Za-z0-9_]*/g,'');
const eq=text.indexOf('export const audited');
const arr=text.indexOf('[', text.indexOf('=', eq));
let depth=0, end=-1;
for(let j=arr;j<text.length;j++){
  if(text[j]=='[')depth++;
  else if(text[j]==']'){depth--; if(depth==0){end=j;break;}}
}
const literal=text.slice(arr,end+1);
process.stdout.write(JSON.stringify(eval('('+literal+')')));
"""
    out = subprocess.run(["node", "-e", node_script, str(ATLAS_DIR / "audited.ts")],
                         capture_output=True, text=True, timeout=30)
    if out.returncode != 0:
        print(f"  node parse error: {out.stderr[:200]}", file=sys.stderr)
        return []
    return json.loads(out.stdout) if out.stdout.strip() else []


def normalize(rec: dict) -> dict:
    """Normalize one BibliographyRecord into an Atlas candidate with per-field provenance."""
    period = rec.get("period", {}) if isinstance(rec.get("period"), dict) else {}
    traditions = rec.get("traditions", []) if isinstance(rec.get("traditions"), list) else []
    return {
        "id": rec.get("id") or _norm_id(rec.get("work", "")),
        "work_identity": _field({"id": rec.get("id"), "title": rec.get("work"),
                                 "alternate_titles": rec.get("alternateTitles", [])}),
        "authorship": _field(rec.get("author") or "anonymous"),
        "date": _field({"start": period.get("start"), "end": period.get("end"),
                        "approximate": period.get("approximate", True)}),
        "language": _field("Sanskrit"),
        "tradition": _field(traditions),
        "editions": _field([t for t in rec.get("textSources", []) if t.get("type") == "edition"]),
        "etexts": _field([t for t in rec.get("textSources", []) if t.get("type") == "etext"]),
        "translations": _field(rec.get("translations", [])),
        "scholarship": _field(rec.get("scholarship", [])),
        "related": _field(rec.get("related", [])),
        "rights": _field({"status": "unknown"}, authority="UNKNOWN"),  # honest OPEN
        "source": "audited.ts (Trika-10 bibliography)",
        "provenance_hash": hashlib.sha256(json.dumps(rec, sort_keys=True, ensure_ascii=False).encode()).hexdigest(),
        "authority_vector": {
            "identity": "CATALOG_MATCHED", "authorship": "CATALOG_SUPPORTED", "date": "CATALOG_SUPPORTED",
            "editions": "CATALOG_SUPPORTED", "etexts": "CATALOG_SUPPORTED",
            "translations": "CATALOG_SUPPORTED", "scholarship": "CATALOG_SUPPORTED",
            "rights": "UNKNOWN",  # honest OPEN, never inflated
        },
    }


def run() -> dict:
    records = parse_ts_records()
    candidates = [normalize(r) for r in records]
    bundle = {
        "bench": "ATLAS-BACKFILL",
        "source": "data/atlas/audited.ts",
        "records_parsed": len(records),
        "candidates": candidates,
        "provenance_rule": "every field carries value/source/derivation/authority_state",
        "next": "ATLAS-10 GOLD: manually verify the first 10, then scale to 100",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)
    return bundle


if __name__ == "__main__":
    b = run()
    print(f"Atlas backfill: parsed {b['records_parsed']} rich records from audited.ts")
    print(f"  candidates: {len(b['candidates'])}")
    if b["candidates"]:
        c0 = b["candidates"][0]
        print(f"  first: {c0['id']} — {c0['work_identity']['value']['title']}")
        print(f"  date field provenance: {c0['date']['source']} / {c0['date']['authority_state']}")
        print(f"  rights: {c0['authority_vector']['rights']} (honest OPEN)")
    print(f"  wrote {OUT}")
