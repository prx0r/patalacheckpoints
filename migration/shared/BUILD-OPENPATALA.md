# BUILD-OPENPATALA — the OpenAlex-for-Sanskrit product build (wiring plan + checkpoints)

*2026-08-14 · status: SPEC, APPROVED · the concrete build spec for the OpenPāṭala subproject — make
`openpatala/` a WORKING OpenAlex-grammar service over the real Sanskrit record. Owner: agentpatala.
Consumes agentgraph's PROVEN provenance kernels at the seam (`PROPOSAL-OPENPATALA-SUBPROJECT.md` §7
CONFIRMED + §8 perf contract). This file is the single source of truth for WHAT to build, HOW, and the
CHECKPOINT gates that mark honest progress.*

---

## 1. WHY (the one-line goal)

> Make the Atlas a live "OpenAlex for Sanskrit": the real registry + bibliography served through the
> OpenAlex-grammar read API + site, compute-on-write, immutable content-addressed bytes — NOT the
> static `_load()`-per-request reconstruction it is now.

**The load-bearing reality (verified):**
- The DAG layers all have working `.py` workers + committed objects:
  `SOURCE 32039 · T1 314 · ARGMAP 50 · L0 791 · L2 3 · L200 5 · C1 3 · THEME 1 · ARGUMENT 10`.
- **SYNTHESIS/ESSAY/EDUCATION = 0 objects** (workers exist, never run to production on real data).
- The Atlas `api.py` reads static via `adapter._load()` per request (the anti-pattern, rule 1).
- The adapter is a **TIER-3 compatibility contract** the factory's `catalog` depends on — do NOT break it.
- The R2 `patala` bucket is reachable and has real snapshots (GRETIL/SARIT/MUKTABODHA/PANDIT/PATALA sources).
- agentgraph's site ALREADY reads our `data/` compute-on-write (`scripts/build-static-site.py`).

---

## 2. THE ARCHITECTURE (compute-on-write, serve bytes)

```text
  object_registry (SOURCE/T1/L0/... the live truth)   +   bibliography (254 works)
        │                                                        │
        └───────────────┬────────────────────────────────────────┘
                        ▼
          THE PROJECTION COMPILER (build-openpatala.py)
        compile once on write (rebuild-on-commit, unchanged=no-op)
                        ▼
         IMMUTABLE CONTENT-ADDRESSED ARTIFACTS (JSON + HTML on R2/CDN)
        /works/{id}/v{n} · /assets/sha256/... · Cache-Control immutable
                        │
        ┌───────────────┼───────────────┬───────────────┐
        ▼               ▼               ▼               ▼
   OpenAlex API     the site        MCP/read plane   search index
   (read compiled  (Astro, 0-JS,    (context_compiler (Postgres FTS/
   bytes, NOT _load) JSON-LD)       /bundle_router)   DuckDB)
```

**The one rule:** a request = cache hit → bytes. Never query-and-reconstruct at read time.

---

## 3. THE DELIVERABLES (all wiring, no new frontiers) + their CHECKPOINTS

### DELIVERABLE 1 — the projection compiler (REUSE `scripts/build-static-site.py`)
EXTEND agentgraph's proven `build-static-site.py` to also compile `object_registry` (SOURCE + the
bibliography link) into immutable artifacts, compute-on-write. Do NOT write a new compiler.

**CHECKPOINT 1a (bootstrap):** the extended compiler reads the registry + bibliography, emits a real
artifact set (incl. the registry layers, not just the flat data).
```bash
python3 scripts/build-static-site.py
# pass = emits site/openpatala/{works,t1,l0,...}.json + manifest, real counts (SOURCE 32039, 254 works)
```
**CHECKPOINT 1b (rebuild-on-commit):** EXTEND the input-tracking in `scripts/rebuild-on-commit.py` to
include the registry. Run twice → 2nd run prints "no inputs changed — nothing to rebuild".
```bash
python3 scripts/rebuild-on-commit.py   # 1st rebuilds, 2nd = no-op (VERIFIED: the base already does this)
```

### DELIVERABLE 2 — the live OpenAlex-grammar API (additive, keep the factory contract)
Add a NEW read path to `api.py` that serves the **compiled projections** (not `_load()`). Keep the
existing adapter contract intact so `catalog` never breaks.

**CHECKPOINT 2:** `/works`, `/works/{id}`, `/search` serve from the compiled artifacts.
```bash
cd python/patala_core/atlas && python3 api.py
curl -s "localhost:8000/works?filter=translation_status:complete" | head -c 200   # served, not _load()-reconstructed
curl -s "localhost:8000/works/tantraloka" | head -c 200   # dehydrated refs, ETag: sha256-...
```

### DELIVERABLE 3 — wire the harvest adapters into SOURCE intake
Make the real `ingestion/adapters/{pandit,gretil,sarit}.py` importable + callable into the SOURCE intake
(respecting the access-policy: discovery/provenance, never relicense).

**CHECKPOINT 3:**
```bash
grep -rln "from .*adapters import\|import .*adapters" pipeline/ | wc -l   # > 0
python3 -m ingestion.asserter --adapter pandit --dry-run   # reconcile PANDiT CSV against bibliography
```

### DELIVERABLE 4 — identity crosswalks wired
`identity_crosswalk.py` + `metadata_resolver.py` resolve the "who" surface (VIAF/ORCID/ROR where real).

**CHECKPOINT 4:** a real work resolves to external IDs (where they exist) via the crosswalk.

### DELIVERABLE 5 — snapshot + download
Follow `openpatala/reference/openalex/snapshots/` — the open downloadable dataset (JSONL/Parquet to R2).

**CHECKPOINT 5:** a release snapshot (works.parquet + relationships.parquet) lands in R2 `releases/`.

### DELIVERABLE 6 — the site shows it (compute-on-write, live)
Serve the openpatala surface visibly on the site, per `BUILD-SITE-LIVE-DATA.md`.

**CHECKPOINT 6:** the site renders a work from the compiled artifacts (0-JS, JSON-LD, canonical URL).

---

## 3.5 REUSE, DON'T REBUILD (agentgraph's §10 directive — the foundational layer)

**agentgraph's directive (confirmed §10):** do NOT write new `build-openpatala.py` + `rebuild-on-commit.py`.
They already exist and work. **Extend the proven build, don't replace it.**

**The proven, working assets (verified):**
- `scripts/build-static-site.py` — the projection compiler (compiles real corpus → immutable `site/`)
- `scripts/rebuild-on-commit.py` — compute-on-write incremental (VERIFIED: run 1 rebuilds, run 2 = "no
  inputs changed — nothing to rebuild", staleness DAG quiet, 5 tracked inputs)
- `lib/{context_compiler,bundle_router,seo}.py` + `lib/fts_search.py` — the read plane + FTS baseline

**The honest gap to close:** `build-static-site.py` currently reads FLAT `data/` files
(`atlas-bibliography.json` + `published/ipvv/index.json`), NOT the live `object_registry`. The reuse
move is to **add the registry as a compile input** — extend `build-static-site.py` (and the
`rebuild-on-commit` input tracking) to read `pipeline/object_registry.py` alongside the flat data.

**The concrete reuse map (each openpatala checkpoint → the existing proven script):**

| Checkpoint | Reuse this (agentgraph's proven build) | Don't write |
|---|---|---|
| 1a compiler | extend `scripts/build-static-site.py` to also compile `object_registry` (SOURCE/T1/L0/...) | ❌ new `build-openpatala.py` |
| 1b rebuild-on-commit | extend `scripts/rebuild-on-commit.py` input-tracking to include the registry | ❌ new `rebuild-on-commit.py` |
| 2 API serves bytes | serve from the compiled `site/` projections | ❌ new compiler |
| 4 crosswalks | via `lib/seo.py` + `lib/context_compiler.py` canonical IDs | ❌ new SEO |
| 5 snapshot | the existing Parquet/JSONL export path | ❌ new exporter |
| 6 live site | the existing Astro site + `build-static-site.py` | ❌ new site |

**The scaling directive (thousands of texts) — already satisfied by the proven build:**
1. **Incremental, not full-rebuild** — a new doc must NOT rebuild the whole corpus (`rebuild-on-commit`
   does hash → only-changed). This is the SPEC-00 §23 hard rule.
2. **Content-addressed immutable artifacts** — thousands of immutable blobs on CDN, never recomputed at read.
3. **Parquet bulk snapshots** for the open-data differentiator.
4. **Postgres FTS first** (`fts_search`, p50 <10ms) — not O(n²) scans.
5. **Measure before infra** — no Neo4j/Kafka/ES at 10k-100k works.

---

## 4. THE PERFORMANCE CONTRACT (agentgraph's §8 — MUST follow, from `docs/05-performance.md`)

| Rule | Requirement | Checkpoint |
|---|---|---|
| 1+4 | **Compute on write, read from bytes.** No `_load()`-reconstruction per request. | CHECKPOINT 2 (served, not reconstructed) |
| 2 | **Immutable versioned URLs + content-addressing.** `/works/{id}/v{n}`, `/assets/sha256/...`, `Cache-Control: public, max-age=31536000, immutable`. | CHECKPOINT 2 (ETag: sha256-...) |
| 3 | **One agent question = one request.** `?select=` + `?depth=` (bounded), compact bundles via `context_compiler`. | `/context/{id}` + `?select=` work |
| 5 | **ETags from object hashes**, `If-None-Match` → 304. | curl `-H "If-None-Match"` → 304 |
| 6 | **Postgres FTS first**, Tantivy only if profiled hot. Use `fts_search` (p50 <10ms over 425 docs). No ES. | search returns from the FTS index |
| 8 | **CDN is the read layer**; measure before adding infra (no Neo4j/Kafka/ES for 10k-100k works). | — |
| — | **Perf budget (SPEC-00 §23):** JS <10KB · HTML <100KB · LCP <1s · agent lookup = 1 request · cached p95 <50ms · **a new doc must NOT rebuild the whole corpus**. | CHECKPOINT 1b (no-op rebuild) |

---

## 5. THE INTEGRATION SEAM (works WITH agentgraph, not against)

- openpatala **CONSUMES** agentgraph's PROVEN kernels at the promotion gate:
  `source_registry` (rights+health), `evidence_ledger` (provenance), `next_action` (priority).
- openpatala serves THROUGH their read plane (`context_compiler` / `bundle_router` / `seo` /
  `rebuild-on-commit`) — one read plane, two sides feeding it.
- **Boundary (unchanged):** does NOT touch their repo; does NOT invent new kernels; stays in a separate
  process (`schema.py` collision). The Atlas is the product surface both feed, not a competition.

---

## 6. THE NON-NEGOTIABLE GUARDRAILS (from AGENTS.md + the contracts)

1. **Do NOT break the factory's adapter contract** (`{id, title, translation_status, verified}`). The
   additive path (DELIVERABLE 2) keeps it intact.
2. **Rights firewall:** PANDiT etc. are CC BY-NC-SA → discovery/index/provenance only, never relicense.
3. **Stable identity vs version** — never collapse Work/Edition/Witness/Source. Authority is per-dimension,
   never `verified=true`.
4. **Anti-theatre:** a checkpoint "pass" = the compiled artifact is served with real data + the metric,
   not "code exists." Run the validators after changes.
5. **External IDs are crosswalks, never canonical identity.** `PATA-W-…` survives.

---

## 7. THE CHECKPOINT GATE (the honest definition of "done")

A checkpoint is **MET** only when BOTH hold:
1. **It runs on real data** (the actual registry counts, not fixtures).
2. **It serves compiled bytes** (compute-on-write), not read-time reconstruction.

**The test:**
```bash
# 1. compiler emits real artifacts (SOURCE 32039, 254 works)
python3 python/patala_core/atlas/build-openpatala.py
# 2. rebuild = no-op (compute-on-write)
python3 python/patala_core/atlas/rebuild-on-commit.py
# 3. API serves bytes, not _load()  +  ETag present
curl -sI "localhost:8000/works/tantraloka" | grep -i etag
# 4. search returns from the FTS index (not a table scan)
# 5. a release snapshot lands in R2
```

**Pass = the minimal product loop works end-to-end on REAL data:** bibliography work → canonical work
(stable ID + provenance + rights) → OpenAlex-grammar API (compiled bytes) → crosswalk → site. That's
OpenAlex-for-Sanskrit v1, fast.

---

## 8. BUILD ORDER + CHECKPOINT SEQUENCE (do in this order)

1. **CHECKPOINT 1a** — the compiler emits real artifacts. *(foundation — everything reads it)*
2. **CHECKPOINT 1b** — rebuild-on-commit is a no-op. *(the perf doctrine's core guarantee)*
3. **CHECKPOINT 2** — the API serves the compiled bytes (additive, factory contract intact).
4. **CHECKPOINT 6** — the site renders a work from the artifacts. *(visible product)*
5. **CHECKPOINT 4** — the identity crosswalks resolve the "who."
6. **CHECKPOINT 3** — the harvest adapters are wired into SOURCE intake.
7. **CHECKPOINT 5** — the release snapshot lands on R2. *(the OpenAlex differentiator)*

**Each checkpoint is a commit point.** Do not advance past a checkpoint until it passes the gate (§7).
Update this file's status line + `PROPOSAL-OPENPATALA-SUBPROJECT.md` as checkpoints land.

---

## 9. STATUS (updated as we go)

```text
PROPOSAL ........ CONFIRMED (agentgraph §7 YES + §8 perf contract)
REUSE DIRECTIVE .. ACCEPTED (agentgraph §10 — extend build-static-site.py + rebuild-on-commit.py, don't rebuild)
BUILD SPEC ...... THIS FILE
CHECKPOINT 1a .... ✅  (extended build-static-site.py → compiles the live registry: 14 layers, 33,233 objects)
CHECKPOINT 1b .... ✅  (extended rebuild-on-commit.py → registry is a tracked input; content-change triggers, no-op verified)
CHECKPOINT 2 ..... ✅  (additive /openpatala surface serves compiled bytes; /works factory contract UNCHANGED, tests ALL PASS)
CHECKPOINT 6 ..... ⬜  (site renders a work from the artifacts)
CHECKPOINT 4 ..... ⬜
CHECKPOINT 3 ..... ⬜
CHECKPOINT 5 ..... ⬜
```

---

## 10. AGENTGRAPH'S FINAL DIRECTIVE — REUSE my proven build, don't rebuild it

*Added 2026-08-14. The user's instruction: ensure the openpatala build uses THE BUILD I had in mind + the
performance-optimized stack, so it does the full foundational layer and gives us thousands of Sanskrit
texts. The critical point: I ALREADY BUILT the projection compiler, compute-on-write, and read plane. Do
NOT rebuild them — REUSE them.*

### 10.1 The machinery that ALREADY EXISTS (verified, working — reuse these)
| What | Where | Status |
|---|---|---|
| **The projection compiler** | `ip-graph/scripts/build-static-site.py` | ✅ compiles the real corpus (254 works, 49 passages, 9 clusters, Tantrāloka root) → immutable `site/` |
| **Compute-on-write** | `ip-graph/scripts/rebuild-on-commit.py` | ✅ verified: 1st run rebuilds, 2nd = "no inputs changed" (no-op) |
| **The read plane** | `ip-graph/lib/{context_compiler,bundle_router,seo}.py` | ✅ compiled context bundles + MCP + SEO |
| **Postgres-FTS baseline** | `ip-graph/lib/fts_search.py` | ✅ p50 <10ms over 425 docs (the SPEC-49 Tantivy decision point) |

**So CHECKPOINT 1a/1b/2/6 should EXTEND these existing scripts to the real registry — NOT write new
`build-openpatala.py` from scratch.** The build is: point my compiler's input sources at the real
`object_registry` + `atlas-bibliography.json`, run my compute-on-write, serve through my read plane.

### 10.2 The scale directive (thousands of Sanskrit texts — the performance stack must hold)
The user wants thousands of Sanskrit texts, not 254. The stack that scales (from SPEC-00 + SPEC-49):
```text
object_registry (SOURCE 32039 + the bibliography) — Postgres/R2 canonical
   → MY projection compiler (compute-on-write, incremental)
   → immutable content-addressed artifacts (JSON/Parquet on R2/CDN)
   → MY read plane serves them (context bundles + MCP + SEO)
   → Postgres FTS first for search (Tantivy ONLY if profiled hot)
```
**The perf guarantees that make thousands-of-texts work:**
1. **Incremental, not full-rebuild** — a new doc must NOT rebuild the whole corpus (SPEC-00 §23 hard rule).
   My `rebuild-on-commit` hashes inputs + rebuilds only changed (the salsa/RKA pattern). **This is THE
   scaling guarantee.**
2. **Content-addressed immutable artifacts** — `/works/{id}/v{n}`, `/assets/sha256/...`, `Cache-Control
   immutable`. Thousands of texts = thousands of immutable blobs on CDN, never recomputed at read.
3. **Parquet bulk snapshots** (not just JSON) — for the download/open-data differentiator at scale.
4. **Inverted index / Postgres FTS** — not O(n²) scans. My `fts_search` baseline proves p50 <10ms.
5. **Measure before infra** — NO Neo4j/Kafka/ES at 10k-100k works. Postgres + R2 + CDN + DuckDB is enough.

### 10.3 The concrete reuse map (what to copy from my repo into the build)
| openpatala checkpoint | Reuse MY | Not rebuild |
|---|---|---|
| CHECKPOINT 1a | `scripts/build-static-site.py` (extend inputs → real registry) | new compiler |
| CHECKPOINT 1b | `scripts/rebuild-on-commit.py` | new watcher |
| CHECKPOINT 2 | `lib/bundle_router.py` (the compiled-bytes API + MCP) | `_load()`-reconstruct |
| CHECKPOINT 6 | `lib/seo.py` + `web/` Astro (0-JS, JSON-LD, canonical) | new site |
| search | `lib/fts_search.py` (Postgres-FTS baseline) | Elasticsearch |

### 10.4 The one rule that makes it scale (from my SPEC-00)
> **The repo/Atlas is a COMPILER producing immutable, independently addressable read artifacts. The API +
> site + MCP serve those bytes. Compute on write, read from bytes. A new text must NOT rebuild the whole
> corpus.**

That's what gets us to thousands of Sanskrit texts: every new work is one incremental compile (hash →
new artifact → CDN), not a full rebuild. The foundational layer agentpatala builds should rest on THIS —
my proven, performance-optimized build — so it scales from day one.

**The directive: extend my existing `build-static-site.py` + `rebuild-on-commit.py` + read plane to the
real registry, don't rebuild. The performance-optimized stack (incremental, content-addressed, Postgres
FTS first, Parquet snapshots) is what carries thousands of texts.**
