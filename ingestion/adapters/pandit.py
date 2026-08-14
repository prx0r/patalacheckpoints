"""ingestion/adapters/pandit.py — the PANDiT ReconciliationAdapter.

ALIGNED with ingestion-refinery.md §3-§6: PANDiT has NO documented public REST API to architect
around. Its data is downloadable (the search UI exposes "Download CSV"); the current general search
holds ~69,580 entities. The adapter therefore consumes PANDiT CSV exports (a Bronze snapshot on disk
or R2), not a live API.

Key doctrine:
  - PANDiT is licensed CC BY-NC-SA 4.0 -> enforce a license firewall (never auto-merge into a
    commercial corpus; partner instead).
  - PANDiT relationships (Person AUTHORED Work) become ExternalRecords / assertions, never canonical
    fields (assertion-as-Evidence, §5).
  - Raw is preserved forever; reconciliation produces NEW canonical objects (maturity ladder).

This is a ReconciliationAdapter subclass (source-evidence/schema/external_record.py) — the contract is
reused, not redefined. Register it via the ingestion.run_ingestion() runner.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import sys
from pathlib import Path
from typing import Optional

_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_ROOT / "source-evidence" / "schema"))
sys.path.insert(0, str(_ROOT / "source-evidence" / "evals" / "patala" / "tasks"))

from external_record import ExternalRecord, ReconciliationAdapter

# PANDiT CSV columns observed in the public search export (defensive; missing cols tolerated).
COL_TITLE = ("title", "work_title", "Title")
COL_AUTHOR = ("author", "creator", "Author")
COL_ID = ("id", "record_id", "URL")
COL_SHELFMARK = ("shelfmark", "location", "repository")
COL_INCIPIT = ("incipit", "text_start")


class PanditAdapter(ReconciliationAdapter):
    source = "PANDIT"
    license = "CC-BY-NC-SA-4.0"
    access_constraints = "CSV export; no public REST API (as of 2026-08)"
    source_authority = "PANDiT Project (https://panditproject.org)"
    update_cadence = "manual snapshot"
    entity_types = ["WORK", "PERSON", "MANUSCRIPT", "PUBLICATION", "INSTITUTION"]
    rights = "CC-BY-NC-SA-4.0 (non-commercial, share-alike); partner, do not relicense"

    def __init__(self, csv_path: Optional[str] = None, snapshot_id: str = "pandit-2026-08-14"):
        self.csv_path = csv_path
        self.snapshot_id = snapshot_id
        self._rows: list[dict] = []

    # ---- ReconciliationAdapter contract ----

    def snapshot(self) -> dict:
        sha = "unknown"
        if self.csv_path and Path(self.csv_path).exists():
            sha = hashlib.sha256(Path(self.csv_path).read_bytes()).hexdigest()
        return {"source": self.source, "snapshot_id": self.snapshot_id,
                "license": self.license, "raw_sha256": sha, "path": self.csv_path}

    def fetch(self, params: dict) -> list[dict]:
        """Load the PANDiT CSV export rows. If csv_path is unset, read from params['csv']."""
        path = self.csv_path or params.get("csv")
        if not path:
            raise ValueError("PanditAdapter needs a CSV export path (no live PANDiT API)")
        with open(path, encoding="utf-8-sig", newline="") as fh:
            self._rows = list(csv.DictReader(fh))
        return self._rows

    def normalize(self, raw: dict) -> dict:
        """Normalize one raw CSV row into the ExternalRecord fields (Silver, source-bound)."""
        def pick(*names):
            for n in names:
                v = raw.get(n)
                if v not in (None, ""):
                    return str(v).strip()
            return ""

        return {
            "external_id": pick(*COL_ID),
            "title": pick(*COL_TITLE),
            "author": pick(*COL_AUTHOR),
            "shelfmark": pick(*COL_SHELFMARK),
            "incipit": pick(*COL_INCIPIT),
            "extra": {"raw_row": raw},
        }

    def emit_external_records(self, raws: list[dict]) -> list[ExternalRecord]:
        out = []
        for r in raws:
            n = self.normalize(r)
            out.append(ExternalRecord(
                source=self.source,
                external_id=n["external_id"],
                title_raw=n["title"],
                author_raw=n["author"],
                shelfmark_raw=n["shelfmark"],
                incipit_raw=n["incipit"],
                retrieved_at=self.snapshot_id,
                extra=n["extra"],
            ))
        return out

    def map_identifiers(self, rec: dict) -> dict:
        """Crosswalk the PANDiT id -> external_identifier entry (PANDIT scheme)."""
        return {"scheme": "PANDIT", "value": rec.get("external_id"),
                "url": f"https://panditproject.org/search?q={rec.get('external_id')}"}

    def reconcile(self, records: list[ExternalRecord]) -> list[dict]:
        from entity_reconciliation import reconcile
        return [reconcile({"rid": r.external_id, "title": r.title_raw, "author": r.author_raw},
                          {"rid": r.external_id, "title": r.title_raw, "author": r.author_raw})
                for r in records]

    def export_enrichment(self) -> list[dict]:
        # corrections/duplicates discovered -> contribute back upstream (ingestion-refinery §23)
        return [{"type": "license_firewall", "source": self.source,
                 "license": self.license,
                 "policy": "CC-BY-NC-SA: non-commercial, share-alike; partner, do not relicense"}]

    def describe(self) -> dict:
        d = super().describe()
        d["snapshot_id"] = self.snapshot_id
        return d
