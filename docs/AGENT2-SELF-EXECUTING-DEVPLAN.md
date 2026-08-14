> **ARCHIVED / SUPERSEDED** — kept for history only. Do NOT follow as current. See `docs/INDEX.md` + `docs/DOCS-AUDIT.json` for the canonical doc for this concern.

# AGENT 2 — SELF-EXECUTING DEV PLAN (ordered by fragility: least fragile first)

*2026-08-13. The dev plan for Agent 2 to build the Pāṭala Atlas foundation, ordered so that **every
step is additive, isolated, and revertible** — least fragile (most reversible) first. The hard rule:
**nothing in this plan rewrites or destabilizes the running factory** (61 works, live loop). Each step has
an exit gate; a step is only "done" when its gate passes.*

*Source docs (read in order): `docs/vision/atlas/technical-architecture-v1.md` (the authoritative schema/
stack), `docs/AGENT2-ATLAS-FOUNDATION-PLAN.md` (the I1–I6 sequence), `openpatala/README.md`, the 3 atlas
blueprints (`engineering`, `cloudflare-edge-layer`, `performance`).*

---

## The fragility principle

Least fragile = most reversible = do first. Each tier is **independent and shippable alone**:

```text
TIER 0  [DONE]  Cloud/R2 infra — additive, no factory touch, fully reversible
TIER 1  Pydantic schema models — pure Python, no DB, no factory
TIER 2  Dedicated Postgres Atlas — isolated container, no factory dependency
TIER 3  Compatibility adapter + 254-record migration — additive, reversible, factory keeps reading
TIER 4  Read API — read-only, additive, no factory writes
TIER 5  One vertical (Brahmayāmala / Dviśatikālottara) — the first end-to-end proof
TIER 6  [DEFERRED] resolver adapters, ingest, snapshots, observability
```

---

## TIER 0 — Cloud/R2 infra [DONE this session]

- Created `patala` R2 bucket with prefix-folders (`public/ source/ manuscripts/ artifacts/ releases/ objects/`).
- `infra/r2_assets.py`: content-addressed put/get/verify/head/migrate + `presign_upload()` (SHA-256 keyed).
- Migrated **86 on-disk Sanskrit sources** → `patala/source/` (content-addressed, immutable).

**Exit gate (passing):** 86/86 in R2, verify PASS, immutable by construction. ✅

---

## TIER 1 — Pydantic schema models (pure Python, zero risk)

The user is finishing schemas; Agent 2 supports with the **contract package** the architecture specifies.
This is pure Python — no DB, no factory, no side effects. Fully reversible (just delete the package).

**What:** create `python/patala_core/` (or `schemas/`) with the Pydantic discriminated models from
`technical-architecture-v1.md` §27–36:

```text
BaseScholarlyObject        (id, object_id, layer, derived_from, source_refs, authority, schema_version)
  ├ PropositionObject        content: PropositionContent
  ├ CommitmentObject         content: CommitmentContent
  ├ GroundingLinkObject      content: GroundingLinkContent
  ├ InferenceApplicationObject content: InferenceApplicationContent
  ├ CruxObject               content: CruxContent
  ├ ReviewEventObject        content: ReviewEventContent   (ReviewEvent cannot mutate target)
  ├ ReviewProposalObject     content: ReviewProposalContent
  └ AdjudicationObject       content: AdjudicationContent
AuthorityVector             (4 independent axes — NOT one rank)
```

**The 3 P0 corrections (from the doc) — implement these, do NOT repeat them:**
1. `content` is **typed discriminated content**, never `dict[str, Any]`.
2. **`AuthorityVector`** = {generation, evidence, review, publication} as 4 independent axes; gates are
   explicit predicates (`eligible_for_publication()`, `eligible_for_scholar_review()`), never `ceiling >= 3`.
3. **No universal review ladder** — education states (e.g. `PEDAGOGICALLY_REVIEWED`) never apply to a
   Proposition; each object type has its own state machine.

**Schema source of truth:** Pydantic → JSON Schema → TypeScript. DB stays Alembic SQL migrations. Do NOT
make Drizzle/TS the universal ontology.

**Exit gate:** `pydantic` models import cleanly; a discriminated-union test proves `PropositionObject`
rejects `PEDAGOGICALLY_REVIEWED` and that `AuthorityVector` has no total-order rank; models generate JSON
Schema. Tests green.

---

## TIER 2 — Dedicated Postgres Atlas (isolated container)

Spin up a **dedicated `patala-atlas`** Postgres container (do NOT reuse temporal/postiz — those belong to
other apps). Isolated; the factory never reads it until the adapter exists. Fully revertible (drop the
container).

**What:**
1. `docker run` a `patala-atlas` Postgres (image `postgres:17`), separate port, separate volume.
2. **Alembic** migrations with the schema from `technical-architecture-v1.md` §17–26, §44–46:
   `work, person, institution, edition, witness, surrogate, transcription, etext, source, scholarly_work,
   external_identifier, name_variant, relationship, asset, asset_version, rights, authority_evidence,
   passage, passage_version, scholarly_object, scholarly_object_version, object_dependency`.
3. Enable `pg_trgm`, `unaccent`, `pgcrypto`.

**Exit gate:** Alembic `upgrade head` runs clean on the isolated container; `pg_trgm`/`unaccent` available;
a trivial `INSERT/SELECT` round-trip on `work` + `authority_evidence` works. Factory untouched.

---

## TIER 3 — Compatibility adapter + 254-record migration (the "don't break the factory" gate)

The linchpin. Build an adapter so the existing bibliography JSON and the running factory catalog coexist
with the new Atlas — **without changing factory behavior**.

**What:**
1. `python/patala_core/atlas/adapter.py`: a read interface that serves a work's metadata either from the
   legacy JSON (today) or the Atlas Postgres (once migrated) — **same output contract**.
2. Write the **migration** script: 254 records → Postgres, **preserving legacy IDs** (explicit mapping
   `legacy_work_id → PTW_uuid`). 0 lost fields, 0 duplicate canonical works.
3. Keep JSON export reproducing current bibliography semantics.
4. The factory catalog reads **through the adapter** — behavior unchanged.

**Exit gate:** 254/254 migrated; 0 lost fields; 0 duplicates; JSON export matches; factory catalog reads
through the adapter with identical output to before. At this point **Postgres is canonical; JSON is an export.**

---

## TIER 4 — Read API (OpenAlex grammar, read-only)

Expose the graph the factory + atlas already have. Read-only, additive — no factory writes. Revertible
(route can be disabled).

**What:**
```text
GET /works  /works/{id}      GET /people  /people/{id}
GET /editions  /editions/{id}   GET /etexts/{id}   GET /witnesses/{id}
GET /passages/{id}  GET /propositions/{id}  GET /arguments/{id}
GET /search   GET /resolve   GET /context/{id}   GET /bundle/{type}/{id}
```
Query grammar: `filter= search= sort= select= cursor=` (NOT `group_by` yet). Agent-first endpoints
(`/context`, `/bundle`) return **dehydrated refs + bounded depth** (≤2, with node/byte/token budget).

**Stack:** Worker (TypeScript, Hono) + Hyperdrive → Postgres, R2 for blobs. In dev: Next.js route handlers
read the Atlas via the adapter (no infra leap yet).

**Exit gate:** a researcher with no repo access can `curl /works/PTW...` → discover work, resolve edition/
etext, see source status, retrieve metadata — via API alone. No N+1 (each endpoint ≤2 SQL queries).

---

## TIER 5 — One vertical (the real milestone)

Do **B**, then prove it with **one complete computable scholarly object**:
`Work → Edition/EText provenance → content-addressed source → translation → argument → Agent1 proof →
human-ready ReviewBundle → public API`.

**Pick:** **Brahmayāmala** (engineering — already touched, frozen T1 defects exist to exercise the
rebuild/eval loop) and/or **Dviśatikālottara** (flagship — English=none).

**What:** run one **bounded unit** (paṭala / 20–50 passages) through `SOURCE→T1→L0→ARGMAP→L2→L200→C1`,
every output carrying `Atlas source ID + asset hash + edition ref + source version + worker provenance`.
Build the **ReviewBundle-v1** (read-only composition of everything a human needs to adjudicate one object).

**Exit gate:** `GET /works/{id}` traverses `edition → source → translation objects` with no filesystem
access. The work exists as a complete computable scholarly object.

---

## TIER 6 — [DEFERRED] resolver, ingest, snapshots, hardening

Only after TIER 5. **Explicitly NOT this cycle** (from the plan): Elasticsearch, Neo4j, whole GRETIL/NMM
import, custom HTR, scholar UI, ORCID/nanopub/blockchain, OpenLineage, full-text cluster.

- **I3 resolver** — `resolve_work/edition/etext` for ONE work via the authority stack → `AuthorityEvidence`
  (statuses DISCOVERED→…→SCHOLAR_CONFIRMED), never one `verified=true`.
- **I5 ingest** — URL/IIIF/upload → asset → reconcile → SourceCandidate → authority gate → factory.
- **I6 snapshots** — JSONL + Parquet + release manifest to R2.
- **Observability/provenance** — OpenLineage/Marquez, PatalaAttestation, Rekor later.

---

## The do-not-do list (this cycle)

```text
NO Elasticsearch  NO Neo4j  NO GraphQL  NO Redis  NO Kafka  NO Kubernetes  NO microservices
NO whole GRETIL/NMM import  NO custom HTR/OCR  NO scholar UI  NO custom auth server
NO blockchain  NO ORCID/nanopub  NO Drizzle-as-ontology  NO rewriting the factory
```

---

## CARRY-FORWARD

**Do the foundation in fragility order: TIER 0 [done] → TIER 1 (Pydantic contract package, the 3 P0
corrections) → TIER 2 (dedicated Postgres Atlas + Alembic) → TIER 3 (compatibility adapter + 254-record
migration, preserving IDs, factory never breaks) → TIER 4 (OpenAlex-grammar read API) → TIER 5 (one
vertical: Brahmayāmala engineering / Dviśatikālottara flagship to a ReviewBundle). TIER 6 deferred. The
running factory stays production throughout.**
