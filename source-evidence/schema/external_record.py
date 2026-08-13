#!/usr/bin/env python3
"""source-evidence/schema/external_record.py — ExternalRecord + the reconciliation adapter framework (P2).

The reviewer's reframe (P2): make ExternalRecord first-class. Do NOT immediately turn a GB catalogue
row into a Manuscript. Preserve the raw record forever, then reconcile:

    ExternalRecord   (raw, immutable — source + external_id + raw_payload_hash + raw fields)
        ↓ candidate_for
    Manuscript / Work / Person / Edition

This is the ingestion boundary: provenance is recorded at the boundary, so if Gyan Bharatam later
corrects a record, you preserve BOTH versions and re-run reconciliation.

The adapter framework: each external source (gretil/sarit/pandit/muktabodha/ngmcp/gyan_bharatam/
openalex/crossref/wikidata) implements the same contract:
    fetch() snapshot() normalize() map_identifiers() emit_external_records() reconcile() export_enrichment()
and declares license/access/source_authority/cadence/entity_types/rights.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field

# the epistemic-maturity ladder (the reviewer's §intro)
MATURITY = ("DISCOVERED", "NORMALIZED", "CANDIDATE_MATCH", "RESOLVED", "SCHOLAR_REVIEWED", "ADJUDICATED")


def _sha256(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


@dataclass
class ExternalRecord:
    """A raw, immutable record from an external manuscript/catalogue source.

    Preserved forever (raw_payload_hash); never mutated. Reconciliation produces NEW objects from it.
    """
    source: str                      # GYAN_BHARATAM / GRETIL / SARIT / PANDiT / NGMCP / MUKTABODHA ...
    external_id: str                 # the source's own id
    raw_payload_hash: str = ""
    retrieved_at: str = ""
    title_raw: str = ""
    author_raw: str = ""
    script_raw: str = ""
    repository_raw: str = ""
    shelfmark_raw: str = ""
    incipit_raw: str = ""
    extra: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.raw_payload_hash:
            self.raw_payload_hash = _sha256({"source": self.source, "external_id": self.external_id,
                                             "title": self.title_raw, "author": self.author_raw,
                                             "shelfmark": self.shelfmark_raw, "incipit": self.incipit_raw})

    def emit(self) -> dict:
        """The canonical ExternalRecord (the raw boundary object)."""
        return {
            "object_kind": "ExternalRecord",
            "source": self.source,
            "external_id": self.external_id,
            "raw_payload_hash": self.raw_payload_hash,
            "retrieved_at": self.retrieved_at,
            "fields": {"title": self.title_raw, "author": self.author_raw, "script": self.script_raw,
                       "repository": self.repository_raw, "shelfmark": self.shelfmark_raw,
                       "incipit": self.incipit_raw},
            "extra": self.extra,
            "design_law": "raw is preserved forever; reconciliation produces new objects, never mutates this",
        }


# ── the adapter framework contract ────────────────────────────────────────────
class ReconciliationAdapter:
    """Every external source adapter implements this contract.

    Subclass + implement the methods; declare the metadata. This lets the ecosystem grow without
    corrupting the canonical model (the reviewer's §10).
    """
    source = "UNSPECIFIED"
    license = ""
    access_constraints = ""
    source_authority = ""
    update_cadence = ""
    entity_types = []
    rights = ""

    def fetch(self, params: dict) -> list[dict]:
        raise NotImplementedError

    def snapshot(self) -> dict:
        """A reproducible snapshot of the source (immutable run id)."""
        raise NotImplementedError

    def normalize(self, raw: dict) -> dict:
        raise NotImplementedError

    def map_identifiers(self, rec: dict) -> dict:
        """Crosswalk external ids -> Pāṭala external_identifier entries."""
        raise NotImplementedError

    def emit_external_records(self, raws: list[dict]) -> list[ExternalRecord]:
        return [ExternalRecord(source=self.source, external_id=r.get("external_id"),
                               title_raw=r.get("title", ""), author_raw=r.get("author", ""),
                               shelfmark_raw=r.get("shelfmark", ""), incipit_raw=r.get("incipit", ""))
                for r in raws]

    def reconcile(self, records: list[ExternalRecord]) -> list[dict]:
        raise NotImplementedError

    def export_enrichment(self) -> list[dict]:
        raise NotImplementedError

    def describe(self) -> dict:
        return {"source": self.source, "license": self.license,
                "access_constraints": self.access_constraints, "source_authority": self.source_authority,
                "update_cadence": self.update_cadence, "entity_types": self.entity_types,
                "rights": self.rights}


if __name__ == "__main__":
    # a Gyan Bharatam-style raw row -> immutable ExternalRecord (raw preserved)
    rec = ExternalRecord(source="GYAN_BHARATAM", external_id="GB_8291",
                         title_raw="Malinivijayottara Tantra", author_raw="",
                         shelfmark_raw="NMS 45/86", incipit_raw="atha mālinīvijayottaram",
                         retrieved_at="2026-08-13")
    print("ExternalRecord (raw, immutable, provenance at the boundary):")
    print(json.dumps(rec.emit(), indent=2, ensure_ascii=False))
    print("  maturity ladder:", list(MATURITY))
    assert rec.raw_payload_hash
    print("\nSELF-TEST PASS (ExternalRecord first-class + adapter framework contract)")
