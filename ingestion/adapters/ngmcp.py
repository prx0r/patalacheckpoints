"""ingestion/adapters/ngmcp.py — the NGMCP ReconciliationAdapter.

NGMCP (National Archives of Nepal / Nepal-German Manuscript Cataloguing Project) documents 180,000+
manuscripts (globalpartnerships.md §1). Like PANDiT, NGMCP has no public bulk API — data comes via
catalogue exports/spreadsheets. This adapter consumes a CSV/spreadsheet export (Bronze snapshot).

Design law: NGMCP records are ExternalRecords (raw, immutable). Reconciliation produces Witness/Work
objects; a scholar adjudicates identity. Never auto-merge manuscripts (FALSE_MERGE_RATE = 0).
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Optional

_ROOT = Path(__file__).resolve().parent.parent.parent
for _p in (_ROOT / "source-evidence" / "schema",):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from external_record import ExternalRecord, ReconciliationAdapter  # noqa: E402

COL_ID = ("id", "shelfmark", "accession", "record_id")
COL_TITLE = ("title", "work", "work_title")
COL_REPO = ("repository", "institution", "archive")


class NgmcpAdapter(ReconciliationAdapter):
    source = "NGMCP"
    license = "catalogue data; check per-export terms"
    access_constraints = "catalogue CSV export (no public bulk API)"
    source_authority = "National Archives of Nepal / NGMCP"
    update_cadence = "manual snapshot"
    entity_types = ["MANUSCRIPT", "WITNESS"]
    rights = "catalogue metadata; link + attribute, do not relicense"

    def __init__(self, csv_path: Optional[str] = None, snapshot_id: str = "ngmcp-snapshot"):
        self.csv_path = csv_path
        self.snapshot_id = snapshot_id

    def snapshot(self) -> dict:
        return {"source": self.source, "snapshot_id": self.snapshot_id, "license": self.license,
                "path": self.csv_path}

    def fetch(self, params: dict) -> list[dict]:
        path = self.csv_path or params.get("csv")
        if not path:
            raise ValueError("NgmcpAdapter needs a catalogue CSV export path")
        with open(path, encoding="utf-8-sig", newline="") as fh:
            return list(csv.DictReader(fh))

    def normalize(self, raw: dict) -> dict:
        def pick(*names):
            for n in names:
                v = raw.get(n)
                if v not in (None, ""):
                    return str(v).strip()
            return ""
        return {"external_id": pick(*COL_ID), "title": pick(*COL_TITLE),
                "shelfmark": pick(*COL_ID), "repository_raw": pick(*COL_REPO),
                "extra": {"raw_row": raw}}

    def emit_external_records(self, raws: list[dict]) -> list[ExternalRecord]:
        out = []
        for r in raws:
            n = self.normalize(r)
            out.append(ExternalRecord(
                source=self.source,
                external_id=n["external_id"],
                title_raw=n["title"],
                shelfmark_raw=n["shelfmark"],
                repository_raw=n["repository_raw"],
                retrieved_at=self.snapshot_id,
                extra=n["extra"],
            ))
        return out

    def map_identifiers(self, rec: dict) -> dict:
        return {"scheme": "NGMCP", "value": rec.get("external_id", "")}

    def export_enrichment(self) -> list[dict]:
        return [{"type": "manuscript_resolution",
                 "note": "NGMCP records resolve to Witness/Work via the entity resolver; never auto-merge"}]
