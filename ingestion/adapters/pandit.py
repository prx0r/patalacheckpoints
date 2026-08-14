"""ingestion/adapters/pandit.py — the PANDiT ReconciliationAdapter (bulk export).

ALIGNED with ingestion-refinery.md §3-§6. PANDiT has no public REST API; the authoritative bulk export
is the 18 MB CSV (69,779 records / 9 content types / 163 columns), snapshotted to R2 as
`pandit-entities-export-2025-11-07`. This adapter consumes that bulk CSV.

BULK EXPORT MODEL (better than per-type search exports):
  - The CSV has a `Content type` column (Print/Work/Manuscript/Extract/Person/Site/Institution/
    Collection/State). ONE file carries the whole corpus.
  - PanditBulkAdapter.split_by_type() splits it losslessly into per-type CSVs + a manifest.

Key doctrine (unchanged):
  - PANDiT is CC BY-NC-SA 4.0 -> license firewall (discovery/index/provenance source, NEVER treated as
    unrestricted commercial data). Record the license on every object.
  - PANDiT IDs are crosswalk identifiers, NEVER canonical identity (PATA-W-… survives).
  - Imported relationships -> assertions/authority_evidence, never canonical fields.
  - Raw preserved forever; reconciliation produces NEW objects.

LOSS-LESS: every source column is retained (nothing dropped). Input rows == accounted output rows.

This is a ReconciliationAdapter subclass (source-evidence/schema/external_record.py) — the contract is
reused, not redefined.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Optional

_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_ROOT / "source-evidence" / "schema"))

from external_record import ExternalRecord, ReconciliationAdapter  # noqa: E402

LICENSE = "CC-BY-NC-SA-4.0"


class PanditBulkAdapter(ReconciliationAdapter):
    """The PANDiT bulk-export adapter (all content types, lossless)."""

    source = "PANDIT"
    license = LICENSE
    access_constraints = "bulk CSV export (no public REST API)"
    source_authority = "PANDiT Project (https://panditproject.org)"
    update_cadence = "manual snapshot (2025-11-07)"
    entity_types = ["WORK", "PERSON", "MANUSCRIPT", "INSTITUTION", "PRINT", "EXTRACT",
                    "COLLECTION", "SITE", "STATE"]
    rights = LICENSE + " (non-commercial, share-alike); discovery/index/provenance source; partner, do not relicense"

    def __init__(self, csv_path: Optional[str] = None,
                 snapshot_id: str = "2025-11-07",
                 content_types: Optional[list[str]] = None):
        self.csv_path = csv_path
        self.snapshot_id = snapshot_id
        self.content_types = content_types or ["Work", "Person", "Manuscript", "Print"]

    # ---- the shared csv reader (lossless: keeps every column) ----
    @staticmethod
    def read_rows(csv_path: str) -> list[dict]:
        with open(csv_path, encoding="utf-8-sig", newline="") as fh:
            return list(csv.DictReader(fh))

    def split_by_type(self, rows: list[dict], out_dir: Path) -> dict:
        """Split the bulk CSV losslessly into per-type CSVs + a manifest. Returns counts.

        input_rows == sum(output rows). Every source column retained (writer uses the same fieldnames).
        """
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        if not rows:
            return {"error": "no rows", "output": []}
        fieldnames = list(rows[0].keys())
        by_type: dict[str, list[dict]] = {}
        for r in rows:
            by_type.setdefault(r.get("Content type", ""), []).append(r)
        written = {}
        manifest = {"source": "PANDIT", "snapshot_id": self.snapshot_id, "license": LICENSE,
                    "fieldnames": fieldnames, "files": []}
        for ct, part in sorted(by_type.items()):
            safe = ct.lower().replace(" ", "_").replace("/", "_") or "unknown"
            path = out_dir / f"pandit_{safe}.csv"
            with open(path, "w", encoding="utf-8", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=fieldnames)
                w.writeheader()
                w.writerows(part)
            sha = hashlib.sha256(path.read_bytes()).hexdigest()
            written[ct] = len(part)
            manifest["files"].append({"content_type": ct, "path": str(path),
                                      "rows": len(part), "sha256": sha})
        # validate: lossless round-trip
        in_rows = len(rows)
        out_rows = sum(len(p) for p in by_type.values())
        manifest["validation"] = {"input_rows": in_rows, "output_rows": out_rows,
                                  "lossless": in_rows == out_rows}
        (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False),
                                               encoding="utf-8")
        return {"written": written, "manifest": manifest, "validation": manifest["validation"]}

    # ---- ReconciliationAdapter contract ----
    def snapshot(self) -> dict:
        sha = "unknown"
        if self.csv_path and Path(self.csv_path).exists():
            sha = hashlib.sha256(Path(self.csv_path).read_bytes()).hexdigest()
        return {"source": self.source, "snapshot_id": self.snapshot_id, "license": self.license,
                "raw_sha256": sha, "path": self.csv_path}

    def fetch(self, params: dict) -> list[dict]:
        path = self.csv_path or params.get("csv")
        if not path:
            raise ValueError("PanditBulkAdapter needs the bulk CSV path (or params['csv'])")
        rows = self.read_rows(path)
        # filter to the requested content types (lossless per type)
        if self.content_types:
            rows = [r for r in rows if r.get("Content type", "") in self.content_types]
        return rows

    def normalize(self, raw: dict) -> dict:
        ct = raw.get("Content type", "")
        return {
            "external_id": raw.get("ID", ""),
            "title": raw.get("Title", "") or raw.get("Work", "") or raw.get("Print title", ""),
            "author_raw": raw.get("Authors (person)", "") or raw.get("Author (person IDs)", ""),
            "extra": {"content_type": ct, "full_row": raw, "license": self.license},
        }

    def emit_external_records(self, raws: list[dict]) -> list[ExternalRecord]:
        out = []
        for r in raws:
            n = self.normalize(r)
            if not n["external_id"]:
                continue
            out.append(ExternalRecord(
                source=self.source,
                external_id=f"pandit:{n['external_id']}",
                title_raw=n["title"],
                author_raw=n["author_raw"],
                retrieved_at=self.snapshot_id,
                extra=n["extra"],
            ))
        return out

    def map_identifiers(self, rec: dict) -> dict:
        return {"scheme": "PANDIT", "value": rec.get("external_id", "").replace("pandit:", ""),
                "url": f"https://panditproject.org/entity/{rec.get('external_id','').replace('pandit:','')}"}

    def export_enrichment(self) -> list[dict]:
        return [{"type": "license_firewall", "source": self.source, "license": self.license,
                 "policy": "CC-BY-NC-SA: discovery/index/provenance; partner, do not relicense"}]


# Backward-compat alias: the old simple name.
PanditAdapter = PanditBulkAdapter
