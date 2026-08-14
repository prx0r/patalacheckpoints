# LAYER 02 — ATLAS (the canonical graph + storage)

> **STATUS: PARTIAL — the 22-table Postgres + resolver + API are REAL; the read API + reconciliation adapters are pending** (derived live state — see `docs_state.py`)


*Part of the `globalglobal.md` spine. The canonical scholarly graph — the immutable reference.*

## 1. What it is
The canonical authority graph: what exists and how it relates. The single source of truth both sites +
all APIs read. Postgres = entity truth · R2 = byte truth · event log = history truth.

## 2. Purpose
Be the durable, provenance-carrying reference everything else projects over. Enforce the identity rule
(external IDs are crosswalks, never canonical) and per-dimension authority (never one scalar).

## 3. External tools used
OpenAlex, Crossref (metadata resolution), VIAF/ROR/ORCID (identity crosswalks) via
`source-evidence/production/adapters/` (see `external-tools.md`). Storage: R2 content-addressed.

**Identity / manuscript / provenance substrate (from the `patalagithubs` review — §J):**
- **Citable passage identity** → CTS / CapiTainS (`capitains.org`) — adopt the citation semantics (CTS URN
  as `external_ids.cts_urn`), not the server stack.
- **Critical-edition / collation** → Saktumiva (witness→variant→editorial-decision) — reverse-engineer its
  object model before building; and **SARIT** as the Indic TEI compatibility target.
- **Provenance** → knowledgeProvenance (`mntlra/knowledgeProvenance`, multi-source assertions +
  supports/refutes/trust) + nanopub (outward standard) + Eigenius (epistemic-status distinction).
- **Schema drift** → **Stencila** (one canonical YAML schema → compiled TS/Python/Rust/JSON-Schema) — the
  answer to the `SCHEMA-AUDIT` divergence (ReviewEvent/Authority/Proposition in 3-4 places).

## 4. Data (the 22-table Postgres schema)
Entities: `work · person · institution · edition · witness · surrogate · etext · source · scholarly_work`
Rights: `rights · asset · asset_version`
Identity: `external_identifier · name_variant · relationship · authority_evidence`
Scholarly: `passage · passage_version · scholarly_object · scholarly_object_version · object_dependency`
Verified 2026-08-14: work=254, external_identifier=254, authority_evidence=268, edition=3, etext=8,
scholarly_work=6, relationship=9.

## 5. Processes
```
Postgres = what exists · R2 = the bytes · event log = history
everything else (search/catalog/API) = disposable projection
```
Identity rule: deterministic UUID = `md5(legacy_id)[:16]`; never an external DB as primary key.

## 6. Implementations
- `migrations/versions/0001_authority_graph_schema.py` — the DDL (22 tables).
- `python/patala_core/atlas/adapter.py` — `AtlasAdapter`, `PostgresBackend.legacy_id_map()` (crosswalk).
- `python/patala_core/atlas/resolver.py` — `resolve_work`, `persist_evidence` (per-dimension authority).
- `python/patala_core/atlas/api.py` — the FastAPI read API (OpenAlex grammar).
- `python/patala_core/atlas/migrate.py` — the legacy→Postgres migration.
- `pipeline/atlas_persist_rich.py` — rich scholarship → Postgres.
- `infra/r2_assets.py` — content-addressed R2 store.
- `openpatala/` — the Atlas build reference.
- Tests: `test_adapter`, `test_api`, `test_resolver`.

## 7. Docs
- `docs/process/02-atlas.md` — the detailed layer guide.
- `docs/atlas-contracts/atlas-database.md` — the full schema.
- `docs/global/agent1atlas.md` — the Atlas convergence directive.
- `docs/vision/vision-15-patala-atlas-sanskrit-research-graph.md` — the Atlas strategy.
