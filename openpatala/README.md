# OPENPĀṬALA — the open Sanskrit research graph ("OpenAlex for Sanskrit")

*2026-08-13. The home of the **Pāṭala Atlas** — the open, authoritative identity/provenance layer for
the Sanskrit textual tradition (then Vedic, then Pāli/Tibetan/Greek/Latin/Arabic). This folder holds
the reference material for building it the OpenAlex way — **copy their product architecture, not
their scale architecture.***

**Vision 15** (`docs/vision/vision-15-patala-atlas-sanskrit-research-graph.md`) is the strategy.
**This folder is the build.** It imports the real OpenAlex docs so we build against a proven pattern,
not from scratch.

---

## 1. What this is

Pāṭala is becoming an **open research graph for the Sanskrit tradition** — the thing OpenAlex is for
modern scholarship, but built for **textual transmission**:

```text
OpenAlex models:            Pāṭala models:
  Paper                      Work
  Author                     Edition
  Institution                Witness
  Citation                   Surrogate
                             Transcription
                             E-text
                             Translation
                             Scholarship
                                  ↓
                             Proposition / Argument / Review
```

OpenAlex is the right **product-architecture template**: stable IDs, heterogeneous entity graph,
external-ID crosswalks, API-first, simple REST grammar, search as a disposable projection,
metadata-first ingestion, bulk snapshots, open downloadable dataset. Its scale architecture
(Elasticsearch cluster, huge ETL, hundreds-of-millions assumptions) is explicitly **not** what we copy.

> **Access caveat (see `docs/atlas-contracts/access-policy.md`):** "open data infrastructure" applies to the
> **discovery/index layer** (metadata, identifiers, previews, documentation, snapshots of metadata). The
> **high-value derived substrate** (full translations, argument graph, bundles, bulk corpus) is a
> **controlled asset** served through tiered, authenticated access — not indiscriminately crawlable.
> **Public discovery ≠ public corpus.**

---

## 2. The three-layer position

```text
ATLAS     what exists + where + which version/witness?     (identity / provenance)  ← THIS FOLDER
    ↓
FACTORY   what can we derive from it?                      (transformation)
    ↓
EPISTEMIC CORE   what is actually supported?               (trust / reasoning)
```

---

## 3. The storage architecture (locked)

> **Postgres stores what things ARE and how they relate. R2 stores the bytes. Search engines store
> disposable indexes.** Never let Elasticsearch, R2 filenames, or the filesystem become canonical truth.

```text
PostgreSQL  = ENTITY TRUTH   (what exists / relationships / authority)
R2          = ARTIFACT TRUTH (the exact bytes, content-addressed by SHA-256)
EVENT LOG   = HISTORY TRUTH  (what changed / who / why)
```
Everything else (Elasticsearch, catalog pages, Next.js caches, Parquet snapshots) is a **disposable
projection**, rebuildable from Postgres + R2.

---

## 4. What we copy from OpenAlex (see `reference/openalex/`)

| OpenAlex feature | We copy | Notes |
|---|---|---|
| **Stable typed IDs** | ✅ | `PTW…` Work · `PTE…` Edition · `PTM…` Witness · `PTS…` Surrogate · `PTT…` Transcription · `PTX…` EText · `PTP…` Person · `PTI…` Institution · `PTR…` ReviewEvent; permanent HTTP URLs |
| **Heterogeneous entity graph** | ✅ | entity + relationship tables in Postgres (no graph DB yet) |
| **External-ID crosswalks** | ✅ | `external_identifier` table: NCC/NGMCP/NMM/GRETIL/SARIT/Muktabodha/OCLC/DOI/OpenAlex/ORCID/ROR/IIIF/CTS/ISBN |
| **API-first, simple REST grammar** | ✅ | `filter=` `search=` `sort=` `cursor=` `select=` `group_by=` (OpenAlex grammar) |
| **Search as disposable projection** | ✅ | rebuildable from Postgres; add Elasticsearch only for serious corpus search |
| **Metadata-first ingestion** | ✅ | resolve identity + rights BEFORE fetching expensive bytes |
| **Bulk snapshots** | ✅ | JSONL + Parquet to R2, from day one |
| **Open downloadable dataset** | ✅ | researchers consume Pāṭala without the API |
| **OpenAPI spec from day one** | ✅ | TS + Python SDK + MCP adapter + docs all derive from it |
| **The LLM guide** | ✅ | `api-guide-for-llms.md` — model the Atlas API guide on it |

## What we DON'T copy yet

```text
massive Elasticsearch deployment
their huge ETL architecture
hundreds-of-millions scale assumptions
their entity ontology  (we have our own: textual transmission)
their compute infrastructure
```

---

## 5. What's UNIQUE to us (OpenAlex can't do this)

OpenAlex models citation networks of modern papers. We model **textual transmission**:

```text
WORK → has edition → EDITION → constituted from → MANUSCRIPT WITNESSES
     → represented by → DIGITAL SURROGATES → transcribed as → TRANSCRIPTIONS
     → normalized as → E-TEXTS → selected as → PĀṬALA SOURCE → factory
```

And the entity/asset distinction (a manuscript is an entity; its scans/OCR/transcription are assets).
That is the moat — OpenAlex has no analogue for it.

---

## 6. Layout

```text
openpatala/
  README.md                     ← this synthesis
  reference/
    openalex/                   ← imported OpenAlex docs (the product-architecture template)
      api-guide/                ← how to use the API (filter/search/sort/select/cursor/group)
      entities/                 ← works/authors/sources/institutions/topics/publishers/funders/geo
      snapshots/                ← the complete-snapshot + data-format + download model
      api-guide-for-llms.md     ← condensed reference for AI agents
      known-issues.md
      SUMMARY.md
```

Related (not copied here, linked):
- `docs/vision/vision-15-patala-atlas-sanskrit-research-graph.md` — the strategy
- `docs/vision/atlas/atlas-engineering-blueprint.md` — the build blueprint
- `docs/vision/source-resolution/source-resolver-design.md` — the reconciliation authority stack
- `docs/vision/functionality/research/2026-08-12/06_ATLAS/RESEARCH_AND_BUILD.md` — the endgame-build project

---

## 7. Current state (2026-08-13)

Already built (the accidental Atlas):
- Bibliography: `data/atlas/` (254 records, school/period/translations)
- Quality signal: `source_ready.py` (CLEAN/READY/PRIORITY, copyright-aware)
- Catalog + API: `pipeline/catalog.py` + `/api/factory/quality`
- Versioned registries + hash-chained event ledger
- Verification v1: `verify_editions.py` (attestations vs archive.org + GRETIL; authority ladder)
- Factory hooks: factory loop + auto-intake

Next (per the blueprint's I1–I6):
```text
I1  Atlas DB      Postgres + Pydantic (Work/Person/Institution/Edition/Witness/Surrogate/EText/
                  ExternalIdentifier/Relationship/Asset/Rights/AuthorityEvidence); migrate 254 records.
I2  R2 asset store  four buckets; put/get/verify/presign; SHA-256 keyed.
I3  Source resolver  resolve_work/edition/witness via Sanskrit authority adapters.
I4  API v1        /works /people /editions /witnesses /etexts /search + filter/search/select/sort/cursor.
I5  Ingestion     URL / upload / IIIF → asset → reconcile → source candidate → factory.
I6  Snapshot exporter  nightly JSONL + Parquet to R2.
```

---

## 8. The carry-forward

> **OPENPĀṬALA = the open Sanskrit research graph.** Copy OpenAlex's *product* architecture (stable
> IDs, entity graph, crosswalks, API grammar, snapshots) — never its *scale* architecture. Model
> **textual transmission** (Work→Edition→Witness→Surrogate→Transcription→E-text→Source), not citation
> networks. Postgres (entity truth) + R2 (artifact truth) + event log (history truth). Mostly built
> already as the bibliography + quality signal + catalog + registries; next is I1 (Postgres Atlas) +
> I2 (R2 store) + I4 (OpenAlex-grammar API).
