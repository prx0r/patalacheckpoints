"""ingestion/adapters/wikidata.py — the Wikidata ReconciliationAdapter.

The universal entity cross-ID adapter (globalpartnerships.md integration-first #1). Wikidata is the
cheapest, highest-value identity backbone: it cross-walks PANDiT/GRETIL/OpenAlex/VIAF/authorities onto
one graph. It has NO auth and a public SPARQL + WB API.

IMPORTANT design law (from external_record.py + globalpartnerships.md §identity):
  Wikidata IDs are crosswalk identifiers (external_identifier rows), NEVER canonical identity.
  A Wikidata Q-id may change/merge; PATA-W-xxx must survive independently.

This is a ReconciliationAdapter subclass. Register + feed it through SourceAsserter.
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

WIKIDATA_SPARQL = "https://query.wikidata.org/sparql"
WIKIDATA_WB = "https://www.wikidata.org/w/api.php"
UA = "patala-scholar-resolver/0.1 (mailto:dev@patala.local)"


def _get_json(url: str, params: dict, accept: str = "application/json") -> Optional[dict]:
    import json
    import urllib.parse
    import urllib.request

    url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception:  # noqa: BLE001
        return None


class WikidataAdapter(ReconciliationAdapter):
    source = "WIKIDATA"
    license = "CC0"
    access_constraints = "public SPARQL + WB API, no auth"
    source_authority = "Wikimedia Foundation"
    update_cadence = "continuous"
    entity_types = ["WORK", "PERSON", "INSTITUTION", "WORK_CROSSWALK"]
    rights = "CC0 (public domain)"

    def __init__(self, query: Optional[str] = None):
        self.query = query or self.DEFAULT_QUERY

    # match by label to a Q-id (crosswalk: works, people, etc.)
    DEFAULT_QUERY = """
SELECT ?item ?itemLabel WHERE {
  ?item rdfs:label ?itemLabel .
  FILTER(CONTAINS(LCASE(?itemLabel), LCASE("$label")))
} LIMIT 10
"""

    def snapshot(self) -> dict:
        return {"source": self.source, "snapshot_id": "wikidata-live", "license": self.license,
                "note": "live cross-ID lookup (no static snapshot)"}

    def fetch(self, params: dict) -> list[dict]:
        """Search Wikidata entities by label. params['label'] (e.g. 'Tantrāloka')."""
        label = params.get("label") or params.get("title")
        if not label:
            return []
        q = self.DEFAULT_QUERY.replace("$label", label.replace('"', ""))
        data = _get_json(WIKIDATA_SPARQL, {"query": q, "format": "json"}, accept="application/sparql-results+json")
        if not data:
            return []
        out = []
        for b in data.get("results", {}).get("bindings", []):
            qid = b.get("item", {}).get("value", "").rsplit("/", 1)[-1]
            label = b.get("itemLabel", {}).get("value", "")
            out.append({"external_id": qid, "title": label, "url": f"https://www.wikidata.org/wiki/{qid}"})
        return out

    def normalize(self, raw: dict) -> dict:
        return {"external_id": raw.get("external_id"), "title": raw.get("title", ""),
                "extra": {"url": raw.get("url")}}

    def emit_external_records(self, raws: list[dict]) -> list[ExternalRecord]:
        return [ExternalRecord(source=self.source, external_id=r["external_id"],
                               title_raw=r.get("title", ""),
                               retrieved_at="wikidata-live",
                               extra={"url": r.get("url")})
                for r in raws]

    def map_identifiers(self, rec: dict) -> dict:
        return {"scheme": "WIKIDATA", "value": rec.get("external_id", "").replace("Q", "Q"),
                "url": f"https://www.wikidata.org/wiki/{rec.get('external_id', '')}"}

    def export_enrichment(self) -> list[dict]:
        return [{"type": "identity_crosswalk",
                 "note": "Wikidata is a universal cross-ID; connect Q-ids to PATA-W-… via external_identifier"}]
