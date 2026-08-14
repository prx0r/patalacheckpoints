"""ingestion/persistence.py — reusable Postgres writer for the SourceAsserter.

ALIGNED with the existing Atlas persistence (do not reinvent):
  - identity crosswalk  : python/patala_core/atlas/adapter.py (PostgresBackend.legacy_id_map)
  - deterministic UUID  : md5(legacy_id)[:16] -> uuid (migrate.py / atlas_persist_rich.py / resolver.py)
  - authority_evidence  : python/patala_core/atlas/resolver.py::persist_evidence (per-dimension rows)
  - DB url / connection : patala_core.atlas.adapter.DEFAULT_DB_URL

This module provides typed, reusable write functions (upsert-ish, idempotent) so ANY adapter's intake
(SourceSnapshot -> ExternalRecord) can land in the Atlas Postgres as canonical objects + per-dimension
authority evidence — without duplicating the crosswalk or UUID rule. Every write is idempotent: the
same source record (scheme+value) never creates a duplicate.

Design laws (from ingestion-refinery.md):
  - external IDs are external_identifier rows, NEVER canonical identity
  - imported relationships are authority_evidence (per-dimension), never canonical fields
  - raw is preserved forever; reconciliation produces new objects
"""
from __future__ import annotations

import hashlib
import json
import sys
import uuid
from pathlib import Path
from typing import Optional

_ROOT = Path(__file__).resolve().parent.parent
for _p in (_ROOT, _ROOT / "python", _ROOT / "pipeline"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from patala_core.atlas.adapter import DEFAULT_DB_URL  # noqa: E402


def _conn():
    import psycopg2
    url = DEFAULT_DB_URL.replace("postgresql+psycopg2://", "postgresql://", 1)
    return psycopg2.connect(url)


def deterministic_uuid(legacy_id: str) -> str:
    """The canonical identity rule: md5(legacy_id)[:16] -> uuid (must match migrate/resolver/persist)."""
    return str(uuid.UUID(bytes=hashlib.md5(legacy_id.encode()).digest()[:16]))


class AtlasWriter:
    """Reusable, idempotent writer over the Atlas Postgres 22-table schema.

    Uses the existing crosswalk + UUID rule; writes authority evidence per-dimension (never a single
    'verified' boolean). All methods are safe to call repeatedly.
    """

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self._conn = None
        self._cur = None

    def _open(self):
        if self._conn is None:
            self._conn = _conn()
            self._cur = self._conn.cursor()
        return self._cur

    def close(self):
        if self._conn is not None:
            if not self.dry_run:
                self._conn.commit()
            else:
                self._conn.rollback()
            self._cur.close()
            self._conn.close()
            self._conn = None

    def work_exists(self, legacy_id: str) -> Optional[str]:
        cur = self._open()
        wid = deterministic_uuid(legacy_id)
        cur.execute("SELECT id FROM work WHERE id = %s", (wid,))
        row = cur.fetchone()
        return row[0] if row else None

    def ensure_work(self, legacy_id: str, title: str, *, source: str = "external") -> str:
        """Upsert a work (deterministic UUID). Returns the work uuid."""
        cur = self._open()
        wid = deterministic_uuid(legacy_id)
        cur.execute("SELECT id FROM work WHERE id = %s", (wid,))
        row = cur.fetchone()
        if row:
            return row[0]
        if self.dry_run:
            return wid
        cur.execute(
            """INSERT INTO work (id, canonical_title, title_normalized, work_type, created_at, updated_at)
               VALUES (%s,%s,%s,%s, now(), now())""",
            (wid, title, title.lower(), "work"))
        return wid

    def ensure_external_identifier(self, entity_type: str, entity_id: str,
                                   scheme: str, value: str, url: Optional[str] = None,
                                   raw_metadata: Optional[dict] = None) -> None:
        """Idempotent insert into external_identifier (UNIQUE(scheme,value) guards dups)."""
        cur = self._open()
        if self.dry_run:
            return
        cur.execute(
            """INSERT INTO external_identifier (id, entity_type, entity_id, scheme, value, url, retrieved_at, raw_metadata)
               VALUES (gen_random_uuid(),%s,%s,%s,%s,%s, now(), %s)
               ON CONFLICT (scheme, value) DO NOTHING""",
            (entity_type, entity_id, scheme, value, url, json.dumps(raw_metadata or {}, default=str)))

    def add_authority_evidence(self, subject_id: str, dimension: str, source_scheme: str,
                               relation: str, evidence_payload: Optional[dict] = None,
                               subject_type: str = "work") -> None:
        """Write one per-dimension authority_evidence row (resolver.py pattern)."""
        cur = self._open()
        if self.dry_run:
            return
        cur.execute(
            """INSERT INTO authority_evidence (id, subject_type, subject_id, dimension, source_scheme,
               relation, evidence_payload, asserted_at)
               VALUES (gen_random_uuid(),%s,%s,%s,%s,%s,%s, now())""",
            (subject_type, subject_id, dimension, source_scheme, relation,
             json.dumps(evidence_payload or {}, default=str)))

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False
