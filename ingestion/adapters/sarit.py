"""ingestion/adapters/sarit.py — the SARIT ReconciliationAdapter.

SARIT = Sanskrit Archive of Indic Texts, a clean TEI P5 corpus on GitHub (globalpartnerships.md §2).
The full corpus is already snapshotted to R2 (`sarit-tei-2026-08-14`, ~34 MB TEI). This adapter reads
SARIT TEI from R2 (or a local dir), extracts the work identity + text, and emits ExternalRecords.

GRETIL-file ≠ Work rule applies equally: a SARIT TEI file is a TextInstance (an electronic scholarly
edition), to be resolved to a canonical Work/Edition via the entity resolver.
"""
from __future__ import annotations

import re
import sys
import tarfile
import tempfile
from pathlib import Path
from typing import Optional

_ROOT = Path(__file__).resolve().parent.parent.parent
for _p in (_ROOT / "source-evidence" / "schema",):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from external_record import ExternalRecord, ReconciliationAdapter  # noqa: E402


def _tei_metadata(xml: str) -> dict:
    """Pull basic TEI header identity: titleStmt + sourceDesc (author/edition if present)."""
    out = {"title": "", "author": "", "editor": ""}
    m = re.search(r"<title[^>]*>(.*?)</title>", xml, re.S)
    if m:
        out["title"] = re.sub(r"<[^>]+>", "", m.group(1)).strip()
    # author in titleStmt <author>
    m = re.search(r"<author[^>]*>(.*?)</author>", xml, re.S)
    if m:
        out["author"] = re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return out


class SaritAdapter(ReconciliationAdapter):
    source = "SARIT"
    license = "per-file CC"
    access_constraints = "public TEI P5 on GitHub + R2 snapshot"
    source_authority = "SARIT (github.com/sarit/SARIT-corpus)"
    update_cadence = "per git commit"
    entity_types = ["TEXT_INSTANCE", "WORK"]
    rights = "per-file CC license; record each file's license"

    def __init__(self, r2_snapshot: Optional[str] = None,
                 snapshot_id: str = "sarit-tei-2026-08-14",
                 local_dir: Optional[str] = None):
        """r2_snapshot: optional snapshot_id to pull from R2 (via SnapshotStore).
        local_dir: alternative — a local SARIT clone/untarred dir."""
        self.r2_snapshot = r2_snapshot or snapshot_id
        self.local_dir = Path(local_dir) if local_dir else None

    def _read_files(self) -> dict[str, str]:
        """Return {filename: tei_xml} from local dir OR the R2 snapshot tarball."""
        files: dict[str, str] = {}
        if self.local_dir and self.local_dir.exists():
            for p in self.local_dir.rglob("*.xml"):
                files[p.name] = p.read_text(encoding="utf-8", errors="ignore")
            return files
        # pull the snapshot from R2
        try:
            import io
            import sys as _sys

            _sys.path.insert(0, str(_ROOT))
            from ingestion.r2 import SnapshotStore

            store = SnapshotStore(r2_bucket="patala")
            m = store.manifest("SARIT", self.r2_snapshot)
            if not m:
                return files
            prefix = m["prefix"]
            import boto3
            import os

            c = boto3.client("s3",
                             endpoint_url=os.environ.get("R2_ENDPOINT"),
                             aws_access_key_id=os.environ.get("R2_ACCESS_KEY_ID"),
                             aws_secret_access_key=os.environ.get("R2_SECRET_ACCESS_KEY"),
                             region_name="auto")
            for f in m["files"]:
                key = f"{prefix}/{f['path']}"
                data = c.get_object(Bucket="patala", Key=key)["Body"].read()
                with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
                    for mem in tf.getmembers():
                        if mem.name.endswith(".xml") and mem.isfile():
                            files[Path(mem.name).name] = tf.extractfile(mem).read().decode("utf-8", "ignore")
        except Exception as e:  # noqa: BLE001
            print(f"  [SaritAdapter] R2 read failed: {e}")
        return files

    def snapshot(self) -> dict:
        return {"source": self.source, "snapshot_id": self.r2_snapshot, "license": self.license,
                "r2_or_local": self.local_dir is not None}

    def fetch(self, params: dict) -> list[dict]:
        rows = []
        for name, xml in self._read_files().items():
            meta = _tei_metadata(xml)
            wid = name[:-4]  # strip .xml
            rows.append({"external_id": f"sarit:{wid}", "title": meta["title"] or wid,
                         "author": meta["author"], "filename": name, "text": xml})
        return rows

    def normalize(self, raw: dict) -> dict:
        return {"external_id": raw.get("external_id"), "title": raw.get("title", ""),
                "author_raw": raw.get("author", ""), "extra": {"filename": raw.get("filename"),
                                                               "text_chars": len(raw.get("text", ""))}}

    def emit_external_records(self, raws: list[dict]) -> list[ExternalRecord]:
        return [ExternalRecord(source=self.source, external_id=r["external_id"],
                               title_raw=r.get("title", ""), author_raw=r.get("author", ""),
                               retrieved_at=self.r2_snapshot,
                               extra=r.get("extra", {}))
                for r in raws]

    def map_identifiers(self, rec: dict) -> dict:
        return {"scheme": "SARIT", "value": rec.get("external_id", "").replace("sarit:", ""),
                "url": "https://github.com/sarit/SARIT-corpus"}

    def export_enrichment(self) -> list[dict]:
        return [{"type": "text_instance_resolution",
                 "note": "SARIT TEI files resolve to canonical Work/Edition via the entity resolver"}]
