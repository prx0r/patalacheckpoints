"""ingestion/adapters/csalt.py — the C-SALT ReconciliationAdapter.

C-SALT (Cologne Sanskrit Lexicon) provides Sanskrit dictionary lookup via public REST + GraphQL APIs
(globalpartnerships.md §2). Pāṭala uses it for LEXICAL LINKS while dictionary definitions stay
EXTERNAL evidence — our contextual Sanskrit sense objects remain ours (never copy their definitions
as canonical).

Design law: a dictionary hit is EVIDENCE for a LexicalSense candidate, never the canonical sense.
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

CSALT_REST = "https://www.sanskrit-lexicon.uni-koeln.de/"
UA = "patala-scholar-resolver/0.1 (mailto:dev@patala.local)"


class CSaltAdapter(ReconciliationAdapter):
    source = "C-SALT"
    license = "CC-BY / CC-BY-SA (see per-lexicon)"
    access_constraints = "public REST + GraphQL, no auth"
    source_authority = "Cologne Sanskrit Lexicon (Köln)"
    update_cadence = "per lexicon release"
    entity_types = ["LEXICAL_SENSE", "TERM"]
    rights = "link + attribute; definitions stay external evidence"

    def __init__(self, base_url: str = CSALT_REST):
        self.base_url = base_url

    def snapshot(self) -> dict:
        return {"source": self.source, "snapshot_id": "csalt-live", "license": self.license,
                "note": "live lexicon lookup (no static snapshot)"}

    def fetch(self, params: dict) -> list[dict]:
        """Look up a Sanskrit term. params['term'] (e.g. 'vimarśa'). Returns candidate senses."""
        term = params.get("term")
        if not term:
            return []
        # C-SALT exposes a JSON lookup; this is the standard endpoint shape.
        import json
        import urllib.parse
        import urllib.request

        url = f"{self.base_url.rstrip('/')}/scansrvpy/scansrvpyjson?dict=apte&key={urllib.parse.quote(term)}"
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                data = json.loads(r.read().decode("utf-8"))
        except Exception:  # noqa: BLE001
            return []
        # response shapes vary by lexicon; handle both a list and a dict payload defensively
        rows = data if isinstance(data, list) else data.get("result", data.get("data", []))
        if isinstance(rows, dict):
            rows = [rows]
        out = []
        for r in rows[:20]:
            headword = r.get("headword") or r.get("key") or r.get("word") or term
            sense = r.get("meaning") or r.get("sense") or r.get("translation") or ""
            out.append({"external_id": f"csalt:{urllib.parse.quote(headword)}", "title": headword,
                        "author_raw": sense, "extra": {"headword": headword, "sense": sense}})
        return out

    def normalize(self, raw: dict) -> dict:
        return {"external_id": raw.get("external_id"), "title": raw.get("title", ""),
                "author_raw": raw.get("author_raw", ""), "extra": raw.get("extra", {})}

    def emit_external_records(self, raws: list[dict]) -> list[ExternalRecord]:
        return [ExternalRecord(source=self.source, external_id=r["external_id"],
                               title_raw=r.get("title", ""), author_raw=r.get("author_raw", ""),
                               retrieved_at="csalt-live", extra=r.get("extra", {}))
                for r in raws]

    def map_identifiers(self, rec: dict) -> dict:
        return {"scheme": "CSALT", "value": rec.get("external_id", "").replace("csalt:", ""),
                "url": f"{self.base_url.rstrip('/')}/mwquery"}

    def export_enrichment(self) -> list[dict]:
        return [{"type": "lexical_link",
                 "note": "dictionary definitions remain external evidence; sense objects are ours"}]
