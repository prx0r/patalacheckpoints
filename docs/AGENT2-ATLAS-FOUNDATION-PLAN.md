# AGENT 2 — ATLAS FOUNDATION PLAN (do B properly first, then one vertical)

*2026-08-13. The corrected build plan: build the **foundation** (B) completely and properly first —
DB, R2, bibliography-as-Atlas, API — while the running factory stays untouched behind a compatibility
adapter. Only when the foundation is real do we run one end-to-end vertical. This supersedes
`docs/AGENT2-NEXT-DEVPLAN.md` (the sivaqueue intake plan) as the next-cycle plan.*

---

## 0. THE PRINCIPLE

> **Build a new source substrate under the factory without stopping the machine that already works.**

- The current factory (61 works, live loop) is **production**. Treat it as such.
- The Atlas is **upstream of** the factory — identity/provenance — never a replacement for it.
- Do **not** destabilize SOURCE/T1/L0 behavior while the substrate is being built.

The factory keeps running in the background through all of this. We are not choosing between B and C —
we are doing **B (foundation) first, then C (one vertical)** once the substrate is real.

---

## 1. THE DB DECISION (locked)

**Use PostgreSQL.** Grounded in your actual setup:

| Choice | Verdict |
|---|---|
| **Postgres** | ✅ **Already running** in Docker (postgres:16 + postgres:17). ACID, JSONB for authority metadata, `pg_trgm` for Sanskrit fuzzy-title reconciliation, FTS. Mature MCP server. |
| D1 (Cloudflare) | ❌ Wrong runtime — you're self-hosted (Next.js + Python factory), not Workers. |
| SQLite/JSON | 🡒 that's the **current** state (export format, not canonical). |
| Neo4j / graph DB | 🡒 later. Postgres entity+relationship + NetworkX in-memory is enough. |
| Timescale | 🡒 later (only if time-series analytics needed). |

**Practical:** spin up a **dedicated `patala-atlas` Postgres** container (do NOT reuse temporal-postgresql
or postiz-postgres — those belong to other apps). Postgres has a first-class **MCP server**, so the Atlas
becomes MCP-queryable natively (`resolve_work`, `find_editions` …).

### The Atlas schema contract
Use typed **Pydantic** models as the single schema source of truth:

```text
Python model → JSON Schema → DB validation/serialization → API model
```
Never hand-maintain parallel schema definitions.

### Base entities (start small — no giant normalized schema yet)

```text
Work · Person · Institution
Edition · Witness · Surrogate · EText
ExternalIdentifier · Relationship
Asset · Rights · AuthorityEvidence
Source          (the factory needs it)
```

---

## 2. THE STORAGE ARCHITECTURE (locked)

> **Postgres stores what things ARE and how they relate. R2 stores the bytes. Search stores disposable
> indexes.** Never let Elasticsearch, R2 filenames, or the filesystem become canonical truth.

```text
PostgreSQL  = ENTITY TRUTH   (works, editions, relationships, authority, rights)
R2          = ARTIFACT TRUTH (the exact bytes, content-addressed by SHA-256)
EVENT LOG   = HISTORY TRUTH  (what changed / who / why)
```

### R2 bucket layout (four buckets, clear permissions)

| Bucket | Contents | Visibility |
|---|---|---|
| `patala-public` | rights-cleared texts, public TEI, snapshots, released translations | public |
| `patala-source` | factory source files, e-texts, OCR, transcriptions, source PDFs | private |
| `patala-manuscripts` | user uploads, scans, TIFF/JPEG, HTR inputs | very controlled |
| `patala-artifacts` | T1/L0/ARGMAP/L2/L200/C1, proof, benchmark outputs | private until promoted |

**Content-address by SHA-256** — key R2 objects by `objects/sha256/xx/xxxx…/blob`, never
`tantraloka-final-final2.txt`. Logical identity (`pt:etext:tantraloka:gretil`) moves between hashes
via explicit versioning; old bytes stay addressable. Immutable artifact history without a blockchain.

**Entity vs Asset** — never collapse: Tantrāloka = Work · Kaul 1918 = Edition · GRETIL file = EText ·
`tantraloka.txt` = Asset. A manuscript is an entity; its scans/OCR/transcription are assets under it.

---

## 3. THE BIBLIOGRAPHY → ATLAS MIGRATION (the data foundation)

The 254 existing bibliography records become the Atlas's first population. This is the real "data
sources organised" work.

### Migration rules
- **Preserve current IDs** — explicit mapping `legacy_work_id → Atlas PTW id`. Never silently regenerate.
- **0 lost fields, 0 duplicate canonical works.**
- **JSON export reproduces current bibliography semantics** (so nothing downstream breaks).
- **Compatibility adapter**: existing bibliography JSON → Atlas interface, so the running factory's
  catalog can read through the Atlas without a rewrite.

### Exit conditions
```text
254/254 records migrated
0 lost fields
0 duplicates
JSON export matches current semantics
factory catalog reads through Atlas adapter
```
At that point **Postgres is canonical; the JSON is an export.**

---

## 4. THE FULL SEQUENCE (adjusted — foundation first, then vertical)

```text
A2-0   Freeze + adapter          tag current factory; no SOURCE/T1/L0 behavior change;
                                 bibliography JSON → Atlas compatibility adapter; loop keeps running.

[ FOUNDATION — do B completely first ]

A2-1   I1 Atlas DB               dedicated patala-atlas Postgres; Pydantic contracts;
                                 schema; migrate 254 records preserving IDs; JSON compat export.

A2-2   I2 R2 asset store         four buckets; put_asset/get_asset/verify_asset/presign_upload;
                                 SHA-256 addressing; migrate the 78 CLEAN Sanskrit sources;
                                 local-cache fallback; factory can fetch same object either way.

A2-3   I4 read API v1            /works /editions /people /etexts /witnesses + /search;
                                 filter/search/select/sort/cursor (NOT group_by yet);
                                 Postgres FTS + pg_trgm (no Elasticsearch); OpenAPI spec.

[ VERTICAL — one complete object through the whole stack ]

A2-4   Pick the vertical         prefer on-disk CLEAN + HIGH + has SOURCE objects + Atlas record.
                                 Engineering: Brahmayāmala (already touched, frozen T1 defects exist).
                                 Flagship untranslated: Dviśatikālottara (English=none). Not necessarily same.

A2-5   I3 resolver slice         resolve_work/edition/etext for ONE vertical;
                                 Work→Edition→EText→Asset SHA→Source; AuthorityEvidence + explicit OPENs;
                                 no auto-promotion; statuses DISCOVERED→…→SCHOLAR_CONFIRMED.

A2-6   Authority-aware source_ready   source_ready = clean AND work_identity AND edition_identity
                                       AND rights AND asset_integrity; split factory/publication/review eligibility.

A2-7   Vertical translation      one bounded unit (paṭala/chapter/20–50 passages);
                                 SOURCE→T1→L0→ARGMAP→L2→L200→C1; every output carries Atlas source ID +
                                 asset hash + edition ref + source version + worker provenance.

A2-8   ARGMAP → Agent 1         Agent 2 emits ARGMAP EvaluationCandidates; Agent 1 does NAT;
                                 Agent 2 consumes EvaluationFindings → only clean ARGMAP → proposition candidates.

A2-9   Proposition substrate    materialize Proposition/Commitment/GroundingLink/InferenceApplication/
                                 Argument/Attack/Crux as versioned factory objects; NetworkX for ancestors/
                                 descendants/paths/topological order/cuts. Agent 2 = graph mechanics,
                                 Agent 1 = epistemic semantics. (Shared canonical schema.)

A2-10  ReviewBundle-v1          read-only composition: Work + Edition + Source asset + Sanskrit + T1 +
                                 L0 + L2 + L200 + C1 + ARGMAP + Proposition + MachineTranslationProof +
                                 Agent1 findings + SourceAssertions + alternatives + ImpactReport.
                                 "Everything a human needs to adjudicate one exact object."

[ SCALE ]

A2-11  I5 ingestion             URL / IIIF / file / GRETIL/SARIT → IngestionJob → asset → reconcile →
                                 SourceCandidate → authority gate → factory. (Institutional integration.)

A2-12  I6 snapshots             works/editions/witnesses/relationships/etexts .jsonl + .parquet to R2;
                                 atlas-release-2026-08-v1 + schema version + counts + hash manifest.

[ HARDENING — only after the vertical works ]

A2-13  Observability            OpenLineage/Marquez/OpenTelemetry around the factory.
A2-14  Release provenance       PatalaAttestation (subject hash/inputs/worker SHA/skill/model/run/proof);
                                 later anchor release roots via Sigstore/Rekor.
```

---

## 5. THE COMPATIBILITY ADAPTER (the linchpin of "don't break the factory")

Before ANY Atlas change, build the adapter so both worlds coexist:

```text
existing bibliography JSON
        ↓ (adapter)
Atlas interface (Postgres)
        ↓
factory catalog  ← reads through Atlas, unchanged behavior
```

This is what lets us migrate to Postgres while the factory keeps running and reading the same data.

---

## 6. WHAT AGENT 2 EXPLICITLY MUST NOT DO THIS CYCLE

```text
NO Elasticsearch          NO Neo4j                 NO bulk Sanskrit authority importer
NO whole GRETIL import    NO whole NMM import      NO custom HTR
NO custom manuscript UI   NO scholar UI            NO ORCID / nanopub / blockchain
NO full OpenLineage now   NO full-text search cluster
```
All of that becomes attractive **after** the first vertical works. Now it is displacement activity.

---

## 7. THE REAL MILESTONE (success is NOT "API built")

> **ONE WORK EXISTS AS A COMPLETE COMPUTABLE SCHOLARLY OBJECT** —
> Work → verified Edition/EText provenance → content-addressed source → translation →
> argument reconstruction → Agent1 proof → human-ready ReviewBundle → public API → downloadable
> snapshot.

Once that works, breadth becomes mechanical, and the 61-work queue stops being "lots of jobs running"
and becomes **"61 works progressively entering a reusable scholarly knowledge infrastructure."**

---

## 8. CURRENT STATE / HEADROOM (what's already done)

Built and live:
- Bibliography: `data/atlas/` (254 records, school/period/translations)
- Quality signal: `source_ready.py` (CLEAN/READY/PRIORITY, copyright-aware)
- Catalog + API: `catalog.py` + `/api/factory/quality`
- Versioned registries + hash-chained event ledger
- Verification v1: `verify_editions.py` (attestations, authority ladder)
- Rebuild/ImpactReport machinery: `factory_rebuild.py`, `factory_batch.py`
- Factory: 61 works, live loop + auto-intake
- Reference base: `openpatala/reference/openalex/` (92 OpenAlex docs)
- Blueprints: Vision 15, `atlas-engineering-blueprint.md`, `source-resolver-design.md`

**Not yet started:** Postgres Atlas (I1), R2 asset store (I2), OpenAlex-grammar API (I4).

---

## 9. THE CARRY-FORWARD

> **Do B (the foundation) completely and properly first — a dedicated Postgres Atlas (I1), an R2
> asset store content-addressed by SHA-256 with the 78 CLEAN sources migrated (I2), an OpenAlex-grammar
> read API (I4), and the 254 bibliography records migrated behind a compatibility adapter so the running
> factory never breaks. Then run ONE vertical (Brahmayāmala for engineering / Dviśatikālottara for
> flagship) end-to-end to a ReviewBundle + public API. Postgres is the DB (already running in Docker);
> R2 is the bytes; the event log is history.**
