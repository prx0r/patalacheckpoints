"""ingestion/adapters/iiif.py — the generic IIIF ReconciliationAdapter.

IIIF (International Image Interoperability Framework) is a strategic decision (globalpartnerships.md
§3): ONE adapter connects many libraries (Bodleian, IFP, Cambridge, NGMCP scans...). Pāṭala does NOT
host images; it publishes a JSON-LD manifest referencing an institution's canvases. A Witness/Surrogate
references an external IIIF manifest.

This adapter ingests a IIIF Presentation-API v2/v3 manifest (by manifest URL or local JSON) into an
ExternalRecord (a Surrogate/Witness with an iiif_manifest link). It is GENERIC — the same code serves
every IIIF library.
"""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path
from typing import Optional

_ROOT = Path(__file__).resolve().parent.parent.parent
for _p in (_ROOT / "source-evidence" / "schema",):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from external_record import ExternalRecord, ReconciliationAdapter  # noqa: E402

UA = "patala-scholar-resolver/0.1 (mailto:dev@patala.local)"


class IiifAdapter(ReconciliationAdapter):
    source = "IIIF"
    license = "see institution manifest"
    access_constraints = "public IIIF Presentation API v2/v3"
    source_authority = "institutional IIIF providers (Bodleian, IFP, ...)"
    update_cadence = "per institution"
    entity_types = ["SURROGATE", "WITNESS"]
    rights = "reference institution manifests; do not rehost without permission"

    def __init__(self, manifests: Optional[list[str]] = None):
        """manifests: optional list of IIIF manifest URLs to ingest (else supply params['manifest'])."""
        self.manifests = manifests or []

    def snapshot(self) -> dict:
        return {"source": self.source, "snapshot_id": "iiif-live", "license": self.license,
                "n_manifests": len(self.manifests)}

    def _fetch_manifest(self, url: str) -> Optional[dict]:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/ld+json, application/json"})
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:  # noqa: BLE001
            return None

    def fetch(self, params: dict) -> list[dict]:
        urls = self.manifests + ([params["manifest"]] if params.get("manifest") else [])
        out = []
        for u in urls:
            m = self._fetch_manifest(u)
            if not m:
                continue
            label = m.get("label", {})
            label_txt = ""
            if isinstance(label, dict):  # v3
                for lang, vals in label.items():
                    label_txt = vals[0] if isinstance(vals, list) and vals else str(vals)
                    break
            elif isinstance(label, str):  # v2
                label_txt = label
            manifest_id = m.get("id") or m.get("@id") or u
            out.append({"external_id": f"iiif:{manifest_id.rstrip('/').rsplit('/',1)[-1]}",
                        "title": str(label_txt), "url": u, "manifest": m})
        return out

    def normalize(self, raw: dict) -> dict:
        return {"external_id": raw.get("external_id"), "title": raw.get("title", ""),
                "extra": {"manifest_url": raw.get("url"),
                          "canvas_count": len(raw.get("manifest", {}).get("items", [])
                                            or raw.get("manifest", {}).get("sequences", [{}])[0].get("canvases", []))}}

    def emit_external_records(self, raws: list[dict]) -> list[ExternalRecord]:
        return [ExternalRecord(source=self.source, external_id=r["external_id"],
                               title_raw=r.get("title", ""),
                               retrieved_at="iiif-live",
                               extra=r.get("extra", {}))
                for r in raws]

    def map_identifiers(self, rec: dict) -> dict:
        return {"scheme": "IIIF", "value": rec.get("extra", {}).get("manifest_url", ""),
                "url": rec.get("extra", {}).get("manifest_url", "")}

    def export_enrichment(self) -> list[dict]:
        return [{"type": "surrogate_link",
                 "note": "one IIIF adapter connects many libraries; Pāṭala references manifests, never rehosts"}]
