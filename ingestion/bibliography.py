"""ingestion/bibliography.py — write ingested records into the existing Pāṭala bibliography.

ALIGNED: the canonical bibliography already lives at:
  data/corpus/atlas-bibliography.json   (thin: id/title/translation_status/verified)
  data/atlas/bibliographySeed.ts        (rich: traditions/period/editions/translations/scholarship)
  data/evaluation/atlas-backfill-candidates.json  (the rich backfill feed -> Postgres)

This module reads that bibliography as the canonical entity set and lets an adapter write new/updated
records into the thin JSON (never overwriting rich fields), so intake is discoverable up the chain
without destabilizing the factory or Postgres.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from .connector import IngestionResult

ROOT = Path(__file__).resolve().parent.parent
THIN = ROOT / "data/corpus/atlas-bibliography.json"


def load_thin() -> dict:
    return json.loads(THIN.read_text(encoding="utf-8"))


def existing_works() -> dict:
    """The canonical entity set {work_id: {...}} from the thin bibliography."""
    return load_thin().get("records", {})


def canonical_entities() -> list[dict]:
    """The canonical entities in the form the reconciliation engine expects ({rid,title,...})."""
    out = []
    for wid, rec in existing_works().items():
        out.append({"rid": rec.get("id", wid), "title": rec.get("title", wid)})
    return out


def merge_into_thin(result: IngestionResult, *, dry_run: bool = True,
                    write_path: Optional[Path] = None) -> dict:
    """Merge new/EXACT-matched records into the thin bibliography (dedup by id/title)."""
    path = write_path or THIN
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"records": {}}
    records = data.setdefault("records", {})
    added = updated = 0
    for rec in result.records:
        title = (rec.title_raw or "").strip()
        if not title:
            continue
        # key by normalized-ish id (external id) else by title; never clobber existing rich id
        key = rec.external_id or title.lower().replace(" ", "_")
        if key in records:
            updated += 1
            # never overwrite verified/rich fields; only fill missing title/translation_status
            records[key].setdefault("title", title)
            records[key].setdefault("translation_status", "pending")
            records[key].setdefault("verified", "false")
        else:
            records[key] = {"id": key, "title": title,
                            "translation_status": "pending", "verified": "false"}
            added += 1
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"added": added, "updated": updated, "total": len(records),
            "dry_run": dry_run, "path": str(path)}
