"""ingestion/adapters/viaf.py — the VIAF ReconciliationAdapter.

VIAF (Virtual International Authority File) gives persistent authority IDs for historical authors —
the identity layer for People (globalpartnerships.md integration-first #4). Public SRU/API, no auth.

Design law: VIAF ids are crosswalk identifiers (external_identifier), NEVER canonical person identity.
A VIAF cluster may merge/split; PATA-P-xxx survives independently.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

_ROOT = Path(__file__).resolve().parent.parent.parent
for _p in (_ROOT / "source-evidence" / "schema",):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from external_record import ExternalRecord, ReconciliationAdapter  # noqa: E402

VIAF_SRU = "https://viaf.org/viaf/search"
UA = "patala-scholar-resolver/0.1 (mailto:dev@patala.local)"


def _get_json(url: str, params: dict) -> Optional[dict]:
    import json
    import urllib.parse
    import urllib.request

    url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception:  # noqa: BLE001
        return None


class ViafAdapter(ReconciliationAdapter):
    source = "VIAF"
    license = "ODC-BY / public authority data"
    access_constraints = "public SRU API, no auth"
    source_authority = "OCLC / national libraries"
    update_cadence = "continuous"
    entity_types = ["PERSON"]
    rights = "authority data; link + attribute, do not relicense"

    def __init__(self):
        pass

    def snapshot(self) -> dict:
        return {"source": self.source, "snapshot_id": "viaf-live", "license": self.license,
                "note": "live authority lookup (no static snapshot)"}

    def fetch(self, params: dict) -> list[dict]:
        """Search VIAF by author name. params['author'] (e.g. 'Abhinavagupta')."""
        author = params.get("author") or params.get("name")
        if not author:
            return []
        query = f'local.personalNames all "{author}"'
        data = _get_json(VIAF_SRU, {
            "query": query, "httpAccept": "application/json", "maximumRecords": "10",
        })
        if not data:
            return []
        out = []
        recs = data.get("searchRetrieveResponse", {}).get("records", []) or []
        for r in recs:
            rec = r.get("record", {}).get("recordData", {})
            vc = rec.get("viaf", {}) or {}
            main = rec.get("mainHeadings", {}).get("data", [])
            label = ""
            if isinstance(main, list) and main:
                label = main[0].get("text", "")
            viaf_id = str(vc.get("viafID", "") or rec.get("viafID", ""))
            if not viaf_id:
                continue
            out.append({"external_id": viaf_id, "title": label,
                        "url": f"https://viaf.org/viaf/{viaf_id}"})
        return out

    def normalize(self, raw: dict) -> dict:
        return {"external_id": raw.get("external_id"), "title": raw.get("title", ""),
                "extra": {"url": raw.get("url")}}

    def emit_external_records(self, raws: list[dict]) -> list[ExternalRecord]:
        return [ExternalRecord(source=self.source, external_id=r["external_id"],
                               title_raw=r.get("title", ""),
                               retrieved_at="viaf-live",
                               extra={"url": r.get("url")})
                for r in raws]

    def map_identifiers(self, rec: dict) -> dict:
        return {"scheme": "VIAF", "value": rec.get("external_id", ""),
                "url": f"https://viaf.org/viaf/{rec.get('external_id', '')}"}

    def export_enrichment(self) -> list[dict]:
        return [{"type": "identity_crosswalk",
                 "note": "VIAF links historical-author clusters to PATA-P-… via external_identifier"}]
