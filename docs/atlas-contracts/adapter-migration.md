# TIER 3 — the compatibility adapter + 254-record migration

*2026-08-13. The "don't break the factory" gate: make the Atlas Postgres canonical while the running
factory + existing API/MCP keep reading the same data through a compatibility adapter.*

## What was built

```text
python/patala_core/atlas/
  adapter.py   — the read interface (legacy TS OR Postgres, same contract)
  migrate.py   — 254 bibliography records → Postgres, preserving legacy IDs
  test_adapter.py — parity + compiled-read-model tests (ALL PASS)
```

## The contract (unchanged)

The adapter serves exactly what the factory catalog + corpus_state already consume:

```json
{ "id": "...", "title": "...", "translation_status": "complete|partial|none|unknown",
  "verified": "true|false|null" }
```

**254/254 records migrate with 0 contract mismatches** — the Postgres backend reproduces the legacy TS
output exactly.

## The speed doctrine (from performance.md / agent-optimization.md)

The adapter follows "materialize once, cache, one-call" — NOT per-request joins:

```text
refresh()   → materialize the compiled read-model (on migration/write)
load()      → hot path: return the cached dict (no DB, no re-parse)
disk cache  → cold starts read data/corpus/atlas-bibliography.json
```

No N+1. The Postgres `load()` does **one** query (works + crosswalk + authority via LATERAL), then a
dict inversion. Hot reads are plain dict lookups.

## Migration

```bash
python3 python/patala_core/atlas/migrate.py --dry-run   # report
python3 python/patala_core/atlas/migrate.py             # migrate + verify
```

Preserves legacy IDs via a **crosswalk** (`external_identifier` scheme=`LEGACY_ATLAS_ID` →
`legacy_id → PTW_uuid`), so nothing downstream loses the original identity. Deterministic UUIDs
(md5 of legacy id) make it idempotent. `authority_evidence` gets a seed `DISCOVERED` row with
`translation_status` + `verified` in the payload — honest, not a fake `verified=true`.

### Exit gate (met)

```text
254/254 migrated ✅       0 lost fields ✅       0 duplicates ✅
JSON/TS export matches ✅   factory catalog reads through adapter, unchanged ✅
```

## At this point

**Postgres is canonical for the bibliography; the TS files are an export/projection.** The adapter
bridges until the existing API/MCP are wired to read Postgres directly (TIER 4).

## Files

| File | Role |
|---|---|
| `adapter.py` | `LegacyBackend` (TS) · `PostgresBackend` (Postgres, one-query) · `AtlasAdapter` (compiled read-model) |
| `migrate.py` | migrate + verify (254/254) |
| `test_adapter.py` | parity + compiled-model tests |
