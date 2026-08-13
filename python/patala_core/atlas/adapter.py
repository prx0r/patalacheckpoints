"""patala_core.atlas.adapter — the compatibility adapter (TIER 3).

The "don't break the factory" gate. Serves bibliography/work metadata from EITHER the legacy
TypeScript seed files (today) OR the Atlas Postgres (once migrated) — with the SAME output contract,
so the factory catalog + corpus_state behave identically either way.

Contract (must match pipeline/catalog._load_atlas exactly):
    { id, title, translation_status, verified }

Two backends:
    LegacyBackend  — parses data/atlas/*.ts (current behavior)
    PostgresBackend — reads the Atlas `work` table (+ relations)
    AtlasAdapter   — picks Postgres when available, else falls back to legacy. No factory behavior change.

Env:
    PATALA_DB_URL  (default the local dev patala-atlas Postgres)
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Protocol

import os
ROOT = Path(os.environ.get("PATALA_ROOT", "/root/projects/patala"))
DEFAULT_DB_URL = os.environ.get("PATALA_DB_URL",
                               "postgresql+psycopg2://patala:patala_atlas_pw@localhost:5433/patala_atlas")
ATLAS_FILES = ("audited.ts", "bibliographySeed.ts", "sivaqueueSeed.ts", "sivaqueue34Seed.ts", "sivaqueueGapSeed.ts")


# ── the shared contract ──────────────────────────────────────────────────────────
class BibliographyRecord(Protocol):
    id: str
    title: str
    translation_status: str
    verified: str | None


# ── legacy backend (current behavior) ────────────────────────────────────────────
class LegacyBackend:
    """Parse data/atlas/*.ts BibliographyRecord entries -> {id: record}. Mirrors catalog._load_atlas."""

    def __init__(self, atlas_dir: Path | None = None):
        self.atlas_dir = atlas_dir or (ROOT / "data" / "atlas")

    def load(self) -> dict[str, dict]:
        records: dict[str, dict] = {}
        for fn in ATLAS_FILES:
            p = self.atlas_dir / fn
            if not p.exists():
                continue
            text = p.read_text(encoding="utf-8")
            for m in re.finditer(r'\{\s*"?id"?\s*:\s*"([A-Za-z0-9_-]+)"', text):
                oid = m.group(1)
                block = text[m.start():m.start() + 1600]
                title = re.search(r'work:\s*"([^"]+)"', block) or re.search(r'"work":\s*"([^"]+)"', block)
                status = re.search(r'translationStatus:\s*"([^"]+)"', block) or re.search(r'"translationStatus":\s*"([^"]+)"', block)
                verified = re.search(r'verified:\s*(true|false)', block) or re.search(r'"verified":\s*(true|false)', block)
                records[oid] = {
                    "id": oid,
                    "title": title.group(1) if title else oid,
                    "translation_status": status.group(1) if status else "unknown",
                    "verified": verified.group(1) if verified else None,
                }
        return records


# ── postgres backend ──────────────────────────────────────────────────────────────
class PostgresBackend:
    """Read the Atlas `work` table (+ authority_evidence for the verified/authority signal)."""

    def __init__(self, url: str | None = None):
        self.url = url or os.environ.get("PATALA_DB_URL", DEFAULT_DB_URL)
        self._conn = None

    def _connect(self):
        if self._conn is None:
            import psycopg2
            url = self.url.replace("postgresql+psycopg2://", "postgresql://", 1) if "+psycopg2" in self.url else self.url
            self._conn = psycopg2.connect(url)
        return self._conn

    def available(self) -> bool:
        """Is the Atlas Postgres reachable?"""
        try:
            self._connect()
            return True
        except Exception:
            return False

    def load(self) -> dict[str, dict]:
        """Return records keyed by LEGACY id (the shared contract key), via the crosswalk.

        legacy_id → {id: legacy_id, title, translation_status, verified} so the output matches
        the legacy TS backend exactly (same keys, same contract)."""
        conn = self._connect()
        cur = conn.cursor()
        # legacy id crosswalk: legacy_id -> atlas uuid
        cur.execute("SELECT value, entity_id FROM external_identifier WHERE scheme='LEGACY_ATLAS_ID'")
        legacy_map = {v: str(eid) for v, eid in cur.fetchall()}
        if not legacy_map:
            cur.close()
            return {}
        # fetch all works + their translation_status/verified from authority_evidence payload (ONE query, no N+1).
        # Prefer the row that carries the contract payload (translation_status) so resolver-added evidence
        # (which may not set the contract fields) doesn't clobber the bibliography contract.
        cur.execute("""
            SELECT w.id, w.canonical_title,
                   ae.evidence_payload, ae.relation
            FROM work w
            LEFT JOIN LATERAL (
                SELECT evidence_payload, relation FROM authority_evidence ae
                WHERE ae.subject_type='work' AND ae.subject_id=w.id
                  AND ae.dimension='WORK_IDENTITY'
                  AND (ae.evidence_payload ? 'translation_status')
                ORDER BY ae.asserted_at DESC LIMIT 1
            ) ae ON true
        """)
        by_uuid: dict[str, tuple] = {}
        for wid, title, payload, relation in cur.fetchall():
            payload = payload if isinstance(payload, dict) else (payload or {})
            status = (payload or {}).get("translation_status", "unknown")
            verified = (payload or {}).get("verified")
            by_uuid[str(wid)] = (title, status, verified, relation)
        cur.close()
        # invert: for each legacy id, resolve its work via the crosswalk
        records: dict[str, dict] = {}
        for legacy_id, uuid_ in legacy_map.items():
            row = by_uuid.get(uuid_)
            if row is None:
                continue
            title, status, verified, _relation = row
            records[legacy_id] = {
                "id": legacy_id,
                "title": title,
                "translation_status": status if status != "unknown" else "unknown",
                "verified": verified,
            }
        return records

    def legacy_id_map(self) -> dict[str, str]:
        """legacy_work_id -> atlas uuid. The migration stores legacy id in external_identifier (scheme=LEGACY_ATLAS_ID)."""
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT ei.value, ei.entity_id FROM external_identifier ei
            WHERE ei.scheme='LEGACY_ATLAS_ID'
        """)
        out = {v: str(eid) for v, eid in cur.fetchall()}
        cur.close()
        return out


def _status_from_authority(authority: str | None) -> str:
    """Map the authority_evidence relation to a translation_status-ish signal (best effort)."""
    if not authority or authority == "seed":
        return "unknown"
    a = authority.upper()
    if "SCHOLAR" in a or "VERIFIED" in a or "MATCHED" in a:
        return "complete"
    return "unknown"


# ── the adapter (chooses backend) ─────────────────────────────────────────────────
class AtlasAdapter:
    """Serves bibliography metadata from Postgres when available, else legacy TS. Same contract.

    Speed doctrine (performance.md + agent-optimization.md): MATERIALIZE once, cache it, one-call
    retrieval. The compiled read-model is computed on write (migration/refresh), not on every read,
    so hot reads are a plain dict lookup — no joins, no N+1, no live connection check per call.
    """

    def __init__(self, legacy: LegacyBackend | None = None, pg: PostgresBackend | None = None,
                 cache_path: Path | None = None):
        self.legacy = legacy or LegacyBackend()
        self.pg = pg or PostgresBackend()
        self.cache_path = cache_path or (ROOT / "data" / "corpus" / "atlas-bibliography.json")
        self._compiled: dict[str, dict] | None = None
        self._backend: str | None = None

    # ── compiled read-model (materialize once; hot path = dict lookup) ───────
    def _backend_is_postgres(self) -> bool:
        if self._backend is None:
            # cached decision: Postgres only once migrated (has legacy_id_map rows)
            self._backend = "postgres" if (self.pg.available() and self.pg.legacy_id_map()) else "legacy"
        return self._backend == "postgres"

    def refresh(self, use_postgres: bool | None = None) -> dict[str, dict]:
        """Materialize the compiled read-model (call on write/migration, not per read)."""
        if use_postgres is True:
            data, backend = self.pg.load(), "postgres"
        elif use_postgres is False:
            data, backend = self.legacy.load(), "legacy"
        else:
            if self._backend_is_postgres():
                data, backend = self.pg.load(), "postgres"
            else:
                data, backend = self.legacy.load(), "legacy"
        self._compiled = data
        self._backend = backend
        # persist so cold starts load from disk, not a re-parse
        try:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            self.cache_path.write_text(json.dumps({"backend": backend, "records": data}, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass
        return data

    def load(self) -> dict[str, dict]:
        """Hot path: return the compiled model without touching the DB or re-parsing TS."""
        if self._compiled is None:
            # try disk cache first (fastest), else materialize
            if self.cache_path.exists():
                try:
                    c = json.loads(self.cache_path.read_text(encoding="utf-8"))
                    self._backend = c.get("backend", "legacy")
                    self._compiled = c.get("records", {})
                    return self._compiled
                except Exception:
                    pass
            self.refresh()
        return self._compiled or {}

    def ids(self) -> set[str]:
        return set(self.load().keys())

    def get(self, wid: str) -> dict | None:
        return self.load().get(wid)

    def using_postgres(self) -> bool:
        return self._backend == "postgres" if self._backend else self._backend_is_postgres()


def load_bibliography(use_postgres: bool | None = None) -> dict[str, dict]:
    """Convenience: load with explicit override (None=auto, True=force pg, False=force legacy)."""
    adapter = AtlasAdapter()
    if use_postgres is True:
        return adapter.pg.load()
    if use_postgres is False:
        return adapter.legacy.load()
    return adapter.load()
