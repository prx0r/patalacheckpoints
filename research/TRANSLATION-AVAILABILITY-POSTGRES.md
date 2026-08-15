# TRANSLATION-AVAILABILITY → POSTGRES (the future canonical step)

*2026-08-15. The perf stack says CANONICAL DB = Neon PostgreSQL. Right now the translation-availability
index is served as a **compiled JSON artifact** (compute-on-write, read-from-bytes, ETag→304) — the
correct read layer, but the structured entity data (works, translations, authorships) has no Postgres
home yet. This is the documented path to make Postgres the canonical store when the data volume or
query needs demand it.*

---

## Why it's deferred (perf rule 6: measure before adding infra)
- The read layer is already fast: compiled JSON + ETag/304 + Astro 0-JS. No latency problem measured.
- Postgres isn't running on this box (8GB, no swap, 2 agents); the existing atlas Postgres backend is
  specced but down. Standing it up is a real infra cost that isn't yet justified by measured need.
- The `authority_evidence` / `work` schema (`migrations/versions/0001_authority_graph_schema.py`)
  already exists for the identity layer.

---

## The migration path (when to do it)

### Trigger (any of these)
1. Query volume/latency on `/translations` + `/works/{id}/translations` becomes a measured bottleneck.
2. We need SQL filters the compiled JSON can't do (e.g. `tradition=Krama AND coverage=partial AND
   has_english=false` across 50k+ works).
3. The translation records grow to the point where JSON rewrite-per-compile is slower than a DB query.

### The schema (additive, mirrors the compiled shape)
```sql
CREATE TABLE IF NOT EXISTS translation_record (
  work_id        TEXT PRIMARY KEY,        -- canonical atlas id
  coverage       TEXT,                    -- full | partial | none
  has_english    BOOLEAN,
  missing        BOOLEAN,
  languages      JSONB,                   -- ["en","it",...]
  translations   JSONB,                   -- [{language,url,translator,coverage,complete,type,tier}]
  copyright_hint TEXT,                    -- PUBLIC_DOMAIN | UNDETERMINED | IN_COPYRIGHT
  factory_state  JSONB,                   -- {t1,l2,c1,next_action}
  live_locations JSONB,                   -- [{provider,url,is_oa,kind}] (from the build-time locator)
  compiled_at    TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS idx_tr_coverage ON translation_record (coverage);
CREATE INDEX IF NOT EXISTS idx_tr_missing   ON translation_record (missing);
```

### The flow (same compute-on-write discipline)
1. `build_translation_index.py` writes the compiled JSON **and** upserts `translation_record` rows
   (still compute-on-write — the live APIs only run at build time).
2. `PostgresBackend` (in `atlas/adapter.py`) reads from `translation_record` instead of the JSON when
   Postgres is up; falls back to the compiled JSON otherwise (the existing dual-backend pattern).
3. `/works/{id}/translations` + `/translations` serve from the same read-model, unchanged contract.

### The non-negotiables (unchanged)
- Live external APIs (OpenAlex/Unpaywall/Crossref) NEVER run per-request — only at build time.
- ETag/304 + immutable cache stay (Postgres is canonical, but the CDN/compiled layer is the read path).
- External IDs remain crosswalks, never canonical identity (AXIOMS).

---

*This is the documented future step, not a build now. The current infra is correct and aligned: compiled
JSON + ETag/304 + Astro 0-JS, Postgres as the canonical target when measured need arrives.*
