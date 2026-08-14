# 02 — ATLAS (the canonical graph + Postgres + read API)

*Part of `docs/process/README.md`. The Atlas is the **canonical scholarly graph** — the single source
of truth for what exists and how it relates. Everything upstream (ingestion) writes to it; everything
downstream (factory, sites, APIs) reads from it. **This is the "immutable reference" the two sites
share.***

## 1. The storage truth model

```
Postgres  = ENTITY/RELATIONSHIP truth  (what exists, how it relates, authority)
R2        = BYTE/ARTIFACT truth        (content-addressed by SHA-256)
Event log = HISTORY truth              (what changed, who, why)
Everything else (search, catalog pages, snapshots) = a DISPOSABLE projection
```

## 2. The Postgres schema (22 tables — `migrations/versions/0001_authority_graph_schema.py`)

**Entities:** `work`, `person`, `institution`, `edition`, `witness`, `surrogate`, `etext`,
`source`, `scholarly_work`.

**Rights & assets:** `rights`, `asset`, `asset_version` (content-addressed, `sha256`).

**Identity / relations / authority:** `external_identifier` (UNIQUE scheme+value),
`name_variant`, `relationship` (typed edges), `authority_evidence` (per-dimension, never one `verified`).

**Passages & scholarly objects:** `passage`, `passage_version`, `scholarly_object`,
`scholarly_object_version`, `object_dependency` (drives ImpactReport/staleness).

Connection (local): `postgresql+psycopg2://patala:patala_atlas_pw@localhost:5433/patala_atlas`
(pg_trgm for fuzzy-title reconciliation; Alembic for migrations; Neon + Hyperdrive in prod).

## 3. The reusable entry points (do NOT rebuild)

| File | Reusable entry point | Purpose |
|---|---|---|
| `python/patala_core/atlas/adapter.py` | `AtlasAdapter`, `load_bibliography`, `PostgresBackend.legacy_id_map()` | compiled read-model + **legacy↔Postgres crosswalk** |
| `python/patala_core/atlas/resolver.py` | `resolve_work`, `persist_evidence`, `LADDER`, `DIMENSIONS` | per-dimension authority + rights-aware gates |
| `python/patala_core/atlas/api.py` | FastAPI `app` (5 endpoints, OpenAlex grammar) | read API for sites/agents |
| `python/patala_core/atlas/migrate.py` | `migrate()`, `verify()` | one-off legacy→Postgres migration |
| `pipeline/atlas_persist_rich.py` | `persist(candidates)` | rich scholarship → Postgres |
| `pipeline/atlas_backfill.py` | `parse_ts_records()`, `normalize()` | `.ts` bibliography → backfill candidates |
| `migrations/versions/0001…py` | the DDL | canonical schema |

## 4. The canonical identity rule (must match everywhere)

**Deterministic UUID = `md5(legacy_id)[:16]` → uuid.** Replicated in `migrate.py`,
`atlas_persist_rich.py`, `resolver.py`, and `ingestion/persistence.py::deterministic_uuid`. Treat it
as the canonical identity rule — never invent a different derivation.

## 5. How data flows

```
legacy .ts seeds (bibliographySeed/audited/sivaqueue*) 
   → LegacyBackend.load() / atlas_backfill.parse_ts_records()
   → atlas-bibliography.json (thin, 254)   ← canonical READ contract
   → atlas-backfill-candidates.json (rich) → atlas_persist_rich.persist() → Postgres
ingestion/ (ExternalRecords)
   → SourceAsserter → AtlasWriter → work/external_identifier/authority_evidence (Postgres)
```

## 6. Current state + known gaps

- **Populated (verified 2026-08-14):** `work` (254), `external_identifier` (254), `authority_evidence`
  (268), `edition` (3), `etext` (8), `scholarly_work` (6), `relationship` (9).
- **Empty:** `source` (0), `scholarly_object` (0), `passage`/`passage_version` (0),
  `object_dependency` (0).
- **No write path for scholarship** — `source_assertion`/`corroboration_event` exist only as typed
  contracts (`source-evidence/schema/source_evidence_profile.py`), not persisted.

## 7. Tests

```bash
source .venv-atlas/bin/activate && alembic current   # 0001 (head)
python3 python/patala_core/atlas/test_adapter.py      # legacy/Postgres parity (254)
python3 python/patala_core/atlas/test_api.py           # 5 endpoints
python3 python/patala_core/atlas/test_resolver.py      # gates + dimensions
```
All pass. Postgres is reachable at localhost:5433.
