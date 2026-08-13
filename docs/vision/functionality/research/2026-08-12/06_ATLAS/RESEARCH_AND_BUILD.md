# Project 06 — Pāṭala Atlas (the Sanskrit Research Graph)

## Objective
Turn the current bibliography from "supporting metadata for the factory" into **the authoritative
identity/provenance layer the factory is downstream of** — an "OpenAlex for Sanskrit" that models
**textual transmission** (Work → Edition → Witness → Surrogate → Transcription → E-text → Source),
not just modern scholarship. Mostly **formalizes the substrate already built** (bibliography,
`source_ready`, catalog, registries, `verify_editions.py`, factory hooks) — this is not a new
project from scratch.

References:
- Vision 15 (the Atlas framing): `docs/vision/vision-15-patala-atlas-sanskrit-research-graph.md`
- Engineering blueprint: `docs/vision/atlas/atlas-engineering-blueprint.md`
- Source-resolver design: `docs/vision/source-resolution/source-resolver-design.md`

## The three-layer position

```text
ATLAS     what exists + where + which version/witness?     (identity / provenance)
    ↓
FACTORY   what can we derive from it?                      (transformation)
    ↓
EPISTEMIC CORE   what is actually supported?               (trust / reasoning)
```

## Reuse, do not rebuild

Copy **OpenAlex's product architecture, not its scale architecture**. Pāṭala is orders of magnitude
smaller than OpenAlex for years, so reproducing their Elasticsearch/ETL/cluster stack would be pure
operational burden with no scholarly value.

**Copy (product architecture):**
```text
stable first-class IDs
heterogeneous entity graph
external-ID crosswalks
API-first product
simple REST grammar (filter/search/select/sort/cursor/group_by)
search as a disposable projection
metadata-first ingestion
bulk snapshots (JSONL + Parquet)
open downloadable dataset
incremental update model
```

**Do NOT copy yet (scale architecture):**
```text
massive Elasticsearch deployment
their huge ETL architecture
hundreds-of-millions scale assumptions
their entity ontology
their compute infrastructure
```

**Sanskrit-specific sources (reuse as adapters, not replace):**
```text
WORK IDENTITY        NCC (New Catalogus Catalogorum)
MANUSCRIPT WITNESSES NMM / Pandulipi Patala (India) · NGMCP (Nepal)
E-TEXTS              GRETIL · SARIT · Muktabodha
SURROGATES / IIIF    Bodleian · OCHS
PRINTED EDITIONS     Google Books · HathiTrust · LoC · WorldCat
MODERN SCHOLARSHIP   Crossref · OpenAlex  (used ONLY for the scholarship layer)
AUTHORS              ORCID
INSTITUTIONS         ROR
```

**Manuscript infrastructure:**
```text
HTR / OCR:     Transkribus (institutional collaboration) · Kraken (open/self-hosted, trainable)
               Do NOT build recognition from scratch.
IMAGE LAYER:   IIIF Presentation 3 (Manifest → Canvas → annotations) as the canonical external image layer.
TEI:           use for critical editions / transcription / apparatus / manuscript description.
               Factory consumes normalized JSON internally:  TEI → CanonicalText JSON → factory.
```

## The storage architecture (locked)

The clean rule:
> **Postgres stores what things ARE and how they relate. R2 stores the bytes. Search engines store
> disposable indexes.** Never let Elasticsearch, R2 filenames, or the filesystem become canonical truth.

```text
              PostgreSQL          R2                 Search index
              canonical graph     bytes/blobs        disposable projection
                  │                   │
                  └────────┬──────────┘
                           ▼
                     PĀṬALA FACTORY
                           │
                           ▼
                     EPISTEMIC CORE
                           │
                           ▼
                    PUBLIC SNAPSHOTS (JSONL + Parquet + RO-Crate)
```

**Three sources of truth, not one:**
```text
POSTGRES ATLAS  = ENTITY TRUTH   (what exists / relationships / authority)
R2              = ARTIFACT TRUTH (the exact bytes, content-addressed by SHA-256)
EVENT LOG       = HISTORY TRUTH  (what changed / who / why)
```
Everything else (Elasticsearch, Marquez, catalog pages, Next.js caches, Parquet snapshots) is a
**disposable projection**, rebuildable from Postgres + R2.

## The entity/asset distinction (critical)

Never collapse these. A manuscript (Bodleian MS Sansk. X) is an **entity**; its JPEG scans, TIFF
masters, PDF, IIIF manifest, OCR, transcription are **assets** under it.

```text
Entity
   │
   └── Asset
         │
         ├── AssetVersion 1
         └── AssetVersion 2
```

Likewise: Tantrāloka = Work · Kaul 1918 = Edition · GRETIL transcription = EText ·
`tantraloka.txt` = Asset.

**Content-addressed storage:** key R2 objects by SHA-256, not `tantraloka-final-final2.txt`.
This gives genuine immutable artifact history without a blockchain — the logical identity
(`pt:etext:tantraloka:gretil`) can move between asset hashes via explicit versioning while old
bytes stay addressable.

## Storage policy (Atlas completeness ≠ file ownership)

```text
RIGHTS-CLEARED / OWNED     → R2 full copy
OPEN INSTITUTIONAL IIIF    → preserve URI + metadata + checksum; optional permitted cache
COPYRIGHTED / RESTRICTED   → metadata + external locator only
USER / SCHOLAR UPLOAD      → R2 private until rights resolved
```
Do NOT mirror every manuscript. If Bodleian/OCHS exposes a stable IIIF resource, an external IIIF
manifest reference can be enough. This makes institutional partnership easy.

## R2 buckets (keep it to four)

```text
patala-public      rights-cleared texts, public TEI, snapshots, review bundles, released translations
patala-source      factory source files, e-texts, OCR, transcriptions, source PDFs  (private by default)
patala-manuscripts user uploads, scans, TIFF/JPEG, HTR inputs  (very controlled)
patala-artifacts   T1/L0/ARGMAP/L2/L200/C1, proof, benchmark outputs  (private until promoted)
```

## Reconciliation (lazy, never bulk)

Do NOT ingest every Sanskrit record on earth. When a text enters the genealogy/factory/research path:

```text
touch work
→ resolve aliases
→ query Sanskrit authorities (NCC / NMM / NGMCP)
→ query manuscript catalogs
→ query editions (Google Books / HathiTrust / LoC / WorldCat)
→ query digital repositories (SARIT / GRETIL / Muktabodha / IIIF)
→ cache candidate graph
→ human confirm ambiguous matches
→ promote
```

**No automatic authority promotion from fuzzy matching.** Use the authority ladder
(`DISCOVERED → CATALOG_MATCHED → MULTI_SOURCE_MATCHED → COPY_INSPECTED → EDITION_VERIFIED →
TEXT_DERIVATION_VERIFIED → SCHOLAR_CONFIRMED`). `source_ready` should eventually depend on this,
not merely "clean Sanskrit on disk."

## API (copy OpenAlex grammar)

```text
GET /works  GET /works/{id}
GET /editions  GET /editions/{id}
GET /witnesses  GET /witnesses/{id}
GET /people  GET /institutions
GET /etexts  GET /translations  GET /scholarship
GET /search
```
with `filter=`, `search=`, `sort=`, `cursor=`, `select=`, `group_by=`. Publish an OpenAPI spec from
day one (TypeScript + Python SDK + MCP adapter + docs all derive from it). Return **dehydrated
references** (count + api_url), not nested universes.

Typed IDs are first-class: `PTW…` Work · `PTE…` Edition · `PTM…` Manuscript · `PTS…` Surrogate ·
`PTT…` Transcription · `PTX…` EText · `PTP…` Person · `PTI…` Institution · `PTR…` ReviewEvent —
with permanent HTTP identifiers (`https://patala.org/W/PTW0000129`) that resolve forever. Separate
stable identity (`PTW…` = "Tantrāloka generally") from version identity (`pt:source:tantraloka:v17`
sha256:… = "the exact frozen textual state").

## Ingestion pipeline (sits BEFORE the factory)

```text
UPLOAD / URL / IIIF / GRETIL / SARIT
            ↓
       IngestionJob → FETCH → HASH → MIME + metadata → RIGHTS → IDENTIFY
            ↓
       RECONCILE → Work / Edition / Witness
            ↓
       EXTRACT → TEI / OCR / transcription / text → SourceCandidate
            ↓
       SOURCE AUTHORITY GATE
            ↓
       factory_ready
```
Route uploads **directly to R2 via presigned URLs** (never pipe bytes through the Next.js server).

## Infrastructure commits (implement in order, depth before width)

```text
I1  Atlas DB      Postgres + Pydantic schema (Work/Person/Institution/Edition/Witness/Surrogate/
                  EText/ExternalIdentifier/Relationship/Asset/Rights/AuthorityEvidence); migrate the
                  existing 254 bibliography records; keep JSON export compatibility.
I2  R2 asset store   patala-public / patala-source / patala-manuscripts / patala-artifacts;
                  put_asset() / get_asset() / verify_asset() / presign_upload(); SHA-256 keyed.
I3  Source resolver   resolve_work() / resolve_edition() / resolve_witness() via Sanskrit authority
                  adapters; results become AuthorityEvidence, never automatic truth.
I4  API v1        /works /people /editions /witnesses /etexts /search with filter/search/select/sort/cursor.
I5  Ingestion     external URL / upload / IIIF → asset → reconcile → source candidate → factory.
                  (This is when institutional integration becomes real.)
I6  Snapshot exporter   nightly/weekly JSONL + Parquet to R2. Now Pāṭala is a real open-data project.
```

## Current state (2026-08-13)

Already built and live:
- Bibliography: `data/atlas/` (254 records, school/period/translations)
- Quality signal: `source_ready.py` (CLEAN / READY / PRIORITY, copyright-aware)
- Catalog + API: `pipeline/catalog.py` + `/api/factory/quality`
- Versioned registries + hash-chained event ledger
- Verification v1: `pipeline/verify_editions.py` (attestations vs archive.org + GRETIL; authority ladder)
- Factory hooks: factory loop + auto-intake

Next step (per the commits): **I1 + I2 + I4** — stand up the Postgres Atlas, migrate the 254 records,
create the R2 asset store, and expose the OpenAlex-grammar read API. Prove the model on the existing
corpus before adding the reconciliation adapters (I3) and ingestion (I5).

## Notes on the two Atlas manuscripts

### `atlas-engineering-blueprint.md` (the "how to build it" doc)
- Copy OpenAlex's **product** architecture, not its **scale** architecture.
- Postgres = canonical entity truth; R2 = content-addressed artifact truth; event log = history truth.
- Entity vs Asset distinction is critical; content-address by SHA-256.
- Keep it to four R2 buckets; route uploads via presigned URLs.
- Postgres (with pg_trgm trigram fuzzy search + FTS) is plenty for up to ~100k entities — no
  Elasticsearch yet; add it only for serious corpus search (vimarśa NEAR svātantrya), as a rebuildable
  projection. Index multiple Sanskrit representations (devanāgarī, IAST, SLP1, normalized, lemma,
  sandhi-split, english).
- Don't use a graph database (Neo4j) yet — Postgres `entity`/`relationship` + NetworkX is enough.
- Add a simple data lake (Parquet snapshots in R2) from day one; Iceberg/R2 Data Catalog later (beta).
- API: copy OpenAlex grammar; publish OpenAPI; dehydrate references; typed IDs; stable vs version identity.
- Rights metadata lives in Postgres, bytes in R2; the API answers "can user download? can factory
  process?" deterministically.
- Storage policy: Atlas completeness ≠ file ownership (IIIF external refs are fine).
- Lock the mundane storage architecture; everything interesting lives above it.

### `source-resolver-design.md` (the "what to reconcile against" doc)
- There is **no one Sanskrit API** — build a federated reconciliation engine (OpenRefine model).
- Authority stack: NCC (work identity) · NMM/Pandulipi (4M manuscripts) · NGMCP (Nepal tantra) ·
  SARIT (verified TEI e-texts) · GRETIL (machine-readable register) · Muktabodha (3k texts, 570
  e-texts, Dyczkowski-edited) · library catalogs (Google Books/HathiTrust/LoC/WorldCat) · IIIF.
- Distinguish Work / Edition / Witness / Surrogate / Transcription / E-text / Source — never collapse.
- Authority ladder with explicit semantics: `SCHOLARLY_CORROBORATED ≠ TRUE ≠ ACCEPTED ≠ HUMAN_REVIEWED`.
- OpenRefine-style reconciliation: candidate → authority → confidence → AUTO / HUMAN REVIEW / UNRESOLVED.
- Pipeline: `pipeline/source_resolver.py` (title/author/local_file → work/edition/witness/digital
  surrogates + resolution + evidence); no auto-promotion from fuzzy matching.
- Human reconciliation queue for ambiguous matches; `0.99` exact → auto-bind, `0.78` → review, homonym → scholar.
- Institutional pitch: "Keep ownership + canonical manuscript identity; Pāṭala consumes stable images/
  transcriptions and adds downstream value." (OCHS/Bodleian own images + HTR ground truth; Pāṭala adds
  reconciliation/audit/argument/review/education.)
- The manuscript is the **root of the dependency graph** — a YouTube claim can descend to `MS Bodl.
  Sanskrit xxx → folio 41r → IIIF pixels`.
