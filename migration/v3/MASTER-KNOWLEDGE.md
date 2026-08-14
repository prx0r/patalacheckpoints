# MASTER-KNOWLEDGE.md — the fast context file for any new agent (read after HANDOVER + AGENTS)

*2026-08-14 · status: THE ONE-STOP REFERENCE · consolidates the two-sided build (agentpatala ↔
agentgraph), the confirmed OpenPāṭala proposal, the verified reality of v3, and the peer-review
findings. Designed so a new agent gets the whole picture in minutes, then goes deep only where it
needs to. This is a projection; the truth is `object_registry` + git + the tests.*

---

## 1. THE TWO-SIDED BUILD (the single most important thing to understand)

**Two repos, one Pāṭala, working at the seam defined in `migration/shared/ROLE-SEPARATION.md`:**

```text
AGENTGRAPH (ip-graph / fuck-off) = THE FRONTIER      AGENTPATALA (this repo) = PRODUCTION / TESTER
  /mnt/HC_Volume_106427611/ip-graph/              /root/projects/patala/
  builds NOVEL kernels + proves mechanisms        wires PROVEN kernels into the REAL pipeline,
  (validate-*.py on stand-in data)                 tests on REAL Sanskrit/Hermes, ships products
```

**The promotion gate (the ONE rule of the seam):** a kernel crosses from FRONTIER (theirs, proven on
stand-in data) to INTEGRATED (ours, production) ONLY when agentpatala runs it on REAL Pāṭala data. Nothing
is production until it passes real-evidence tests. **This is what makes the collaboration non-theatre.**

**The clean test of who does what:**
- NEW kernel or novel integration → **AGENTGRAPH**
- wiring a kernel into Pāṭala / testing on real IPVV+gold / shipping a product → **AGENTPATALA**

**The hard process boundary:** `schema.py` COLLIDES between the two repos (different APIs). The two
systems MUST run in **separate processes**. Never import both in one process.

---

## 2. THE SHARED GOAL (what both sides build toward)

`migration/shared/SHARED-GOAL.md`: the **autonomous organism** — ingest a batch of untranslated Sanskrit
docs in a priority-based queue → full spine `SOURCE→T1→L0→L2→L200→C1→ARGUMENT→CRUX→ESSAY→EDUCATION` →
epistemic gate → products → self-improving loop. `next_action` (weighted formula, not LLM-guess) decides
WHAT to work on next.

**The two active lanes (AGENTS.md §3):**
- **Agent 1 (ML/philosophy)** — upward: C1→themes→arguments→claims→synthesis. *Does this higher rep legitimately derive from what's beneath it?*
- **Agent 2 (corpus compiler + integrity)** — vertical: SOURCE→T1→L0→…→C1. *Is this reading licensed by the source?*
- Join on Passage ID / TranslationDecision ID / C1 ID — NEVER fuzzy.

---

## 3. THE CONFIRMED PROPOSAL — OPENPĀṬALA SUBPROJECT (what to build next)

**File:** `migration/shared/PROPOSAL-OPENPATALA-SUBPROJECT.md` — **CONFIRMED by agentgraph** (§7: yes,
consume our provenance kernels at the seam; + §8: the performance contract).

### The goal
Make `openpatala/` the working **OpenAlex-grammar service over the real Sanskrit record** (the "OpenAlex
for Sanskrit"). Copy OpenAlex's **product architecture** (stable IDs, entity graph, external-ID crosswalks,
API-first, metadata-first ingestion, bulk snapshots), NOT its scale architecture (no Elasticsearch cluster).

### The minimal product loop (v1 = done)
```text
real bibliography work (atlas-bibliography.json, 254 works)
  → resolves to a canonical work (stable ID + rights + provenance)
  → served by the atlas OpenAlex-grammar API (works/search/filter from the LIVE registry, not static)
  → crosswalked to external IDs (VIAF/ORCID/ROR where real)
  → visible on the site
```

### The deliverables (all WIRING, no new frontiers)
1. **Atlas API reads the LIVE registry** — replace the static `_load()` in
   `python/patala_core/atlas/api.py` with the real `object_registry` (SOURCE works) + bibliography link.
2. **Harvest adapters get imported + called** — `ingestion/adapters/{pandit,gretil,sarit}.py` into the
   SOURCE intake (respect access-policy: discovery/provenance for PANDiT, machine-readable for GRETIL/SARIT).
3. **Identity crosswalks get wired** — `identity_crosswalk.py` + `metadata_resolver.py` → the "who"
   surface; VIAF/ORCID/ROR where real.
4. **Snapshot + download** — follow `openpatala/reference/openalex/snapshots/`.
5. **Site shows it** — per `BUILD-SITE-LIVE-DATA.md`.

### The performance contract (agentgraph's §8 — MUST follow)
- **THE rule:** compute on write, read from bytes. `api.py` doing `_load()` per request = the anti-pattern
  (rule 1). Fix: compile once → immutable addressable artifacts → serve bytes (0 request-time reconstruction).
- **Immutable versioned URLs + content-addressing** — `/works/{id}/v{n}`, `/assets/sha256/...`,
  `Cache-Control: public, max-age=31536000, immutable`. Stable ID resolves to a sha256, not a mutable row.
- **One agent question = one request** — `?select=` + `?depth=` (bounded), compact bundles via `context_compiler`.
- **ETags from object hashes** — `ETag: "sha256-…"` + `If-None-Match` → 304.
- **Postgres FTS first** (`fts_search.py`, p50 <10ms over 425 docs) — NO Elasticsearch; Tantivy only if profiled hot.
- **CDN is the read layer**; measure before adding infra (no Neo4j/Kafka/ES for 10k-100k works).
- **Perf budget (SPEC-00 §23):** JS <10KB · compressed HTML <100KB · LCP <1s · agent lookup = 1 request ·
  bundle = 1 request · cached p95 <50ms · DB p95 <200ms · **a new doc must NOT rebuild the whole corpus**.
- **Seamless read-plane integration:** serve THROUGH agentgraph's `context_compiler.py` /
  `bundle_router.py` / `seo.py` / `rebuild-on-commit.py`. One read plane, two sides feeding it.

### The integration seam (how it works with agentgraph)
- openpatala CONSUMES their PROVEN provenance kernels (`source_registry` for rights+health,
  `evidence_ledger` for provenance, `next_action` for priority) at the promotion gate.
- openpatala HANDS them a live identity service (the OpenAlex-grammar surface) to test their mechanisms on
  REAL data.
- Boundary: does NOT touch their repo; does NOT invent new kernels; stays in a separate process; the Atlas
  is the product surface both feed, not a competition.

---

## 4. THE VERIFIED REALITY OF v3 (what actually works — I ran the tests)

**All in `migration/v3/`. These are REAL passing scripts (not docs-only), verified by execution:**

| Script | Result |
|---|---|
| `test_multisubject.py` | ✅ 20/20 (IPVV 9/9, Doyle 7/7, Ratié 4/4) |
| `build_products.py` | ✅ 18/18 |
| `vertical_v2a.py` | ✅ 12/12 |
| `test_products_integration.py` | ✅ 11 WORKS / 0 PARTIAL / 0 BROKEN (real Hermes) |
| `translate_passage.py` | ✅ real Hermes T1+close+reading+commentary+proof on a fresh verse |
| `full_system_test.py` | ✅ 11/11 on Sārdhatriśatikālottarāgama (untranslated, no gold) |

**The v3 blueprint** (`PATALA-V3-ORGANISM.md`, `PRODUCTS.md`, `V3-BUILD-SPEC.md`): one "Verified Epistemic
OS" with 5 organ-systems, a 17-kernel skeleton, 16 products + 6 expansions, 3 governing laws (TRUTH/COMPILE/
READ) + anti-theatre gate. Graduation test = one IPVV claim through the whole stack, then mutate the source.

### The known v3 inconsistencies (do NOT propagate them; fix if you touch them)
- **Kernel count:** v3 says "17 kernels / 51 experiments"; shared says "37-42 kernels / 88 experiments".
  `ROLE-SEPARATION.md` explicitly flags this as unreconciled. **Treat shared's higher number as the truth**
  (agentgraph's peer-review says 42 kernels, 88 experiments, 82/82 tests).
- **Essay status:** ORGANISM/PRODUCTS still list Essay as "NEEDS-BUILD" but `PRODUCT-PROOFS.md` /
  `INTEGRATION-AUDIT.md` confirm Essay WORKS (real Hermes, verified). The correction exists but the older
  docs weren't updated. Use the WORKS status.
- **Products:** "13/16 PROVEN" (lab mechanism-proofs) vs "10 WORKS / 6 PARTIAL" (full-form testability).
  Different criteria; don't quote one without the other.
- **translation.py:** v3 marks it PROVEN; an older shared audit called it an empty container. Agentgraph's
  peer notes say it was since fixed (real Hermes). Use the fixed status.

---

## 5. THE PEER-REVIEW FINDING ON AGENTGRAPH'S `factory_pool.py` (the live review)

**Context:** agentgraph committed `5cf26937` "parallel factory worker pool (10/10)". I reviewed it and
found it does NOT actually advance work in the normal case.

**The critical bug:** `lib/factory_pool.py` **cannot bootstrap from an empty state.** The whole chain is
gated on SOURCE being committed (`LAYER_DAG`: T1←SOURCE, L0←T1, …), but `schedule()` only adds tasks for
the layers you pass in — SOURCE is never scheduled, so with `["T1","L0","L2","L200"]` there are **zero
eligible tasks** every pass → `rank()` returns `[]` → nothing runs → **commits 0 objects forever** unless
SOURCE is pre-seeded externally. I reproduced this exactly (mock producers, 5 iterations → n_committed=0).

**Why their "10/10" test passes anyway:** `scripts/validate-factory-pool.py` **manually pre-seeds**
`pool.committed[w]={"SOURCE":"committed"}` before running — it rigs the bootstrap and never exercises the
failure case.

**The "many layers at once" claim is largely false:** the DAG is a strict linear chain, so for any work
exactly ONE layer is eligible at a time. With `max_workers ≥ n_works` all works stay in lockstep → exactly
one layer advances per pass. It's parallel across WORKS within a layer, not across LAYERS (unless works
drift out of phase by accident).

**What IS real and correct in their pool:** the DAG gating (`eligible`), `next_action` formula scheduling,
concurrency across works, commit tracking, `report()`. The `rank()` return format `[(score, Task)]` is used
correctly. The `if ":" in t.id` filter is a no-op (every id has ":").

**The honest verdict:** the machinery is real but the pool is NOT the "many layers at once, autonomous,
self-driving factory" it claims. It needs an external SOURCE-commit/bootstrap step that is neither
documented nor built in. **This is the seam gap to coordinate on** — agentgraph's pool (lib/) and patala's
registry (object_registry) have no concrete interface between them yet.

**My recommendation:** when we wire the parallel factory (BUILD-PARALLEL-FACTORY), we (agentpatala) supply
the missing bootstrap + the real producers (our `factory_batch._produce_layer`) and the real
`object_registry.commit`, and test it on real data — that's the promotion gate. Do not accept their
"10/10" as proof of production readiness.

---

## 6. THE FOUR-TRUTHS + ANTI-THEATRE (the governing doctrine — never violate)

**The one rule (AGENTS.md §0):** Nothing is "real" because code exists. It becomes real only when an
independently defined task + human-grounded gold + a reproducible eval show it does what its name claims.

**The permanent checkpoint test (§7):** *What experiment would convince you this does NOT work?* If the
answer is "tests pass / schema validates / model said so" → EXPERIMENTAL. If it's "frozen gold, blind
prediction, metric, failures, human adjudication" → RESEARCH.

**The 3 categories + banned words (§8):** A. INFRASTRUCTURE (schemas) · B. EVIDENCE (gold/reviews/proofs) ·
C. RESULTS (measured behavior). Never call A→C. **Ban:** PROVED · TRUTH · CORRECT · BEST · WINS.
**Use:** SUPPORTED BY · PASSED CHECK X · BENCHMARKED ON · MACHINE-PROPOSED · REVIEWED BY · NO CONFLICT DETECTED.

**The real evidence (GOLD-EVIDENCE-INDEX.md):** SOURCE→T1→L0→L200, 5 golds, Nyāya gate, certificates, NAT
tests, 43 API routes, 19 skills. **DESIGN (not built):** Commentarial (06), Organism (09), Economics (11),
SYNTHESIS/ESSAY/EDUCATION were 0 — Essay now WORKS via real Hermes.

---

## 7. THE DATA + SURFACES (what's real and callable)

- **Real data:** 32k SOURCE objects, 254 bibliography works, 71 RAW-EN translated works (the live factory
  input), 71 translated works. Adapters exist (`ingestion/adapters/`) but are NOT imported by prod code.
- **The read surface (OG-READ-SURFACE.md):** 43 API routes (mostly static `@/data`), 19 Hermes skills,
  29 MCP tools, 7 runnable examples (`examples/run_all.sh`), timeline (23 schools via `historyTimeline.json`),
  lemma-through-time (`/api/terms/[lemma]/history`).
- **The site is static (Astro, 0 JS):** 254 works, 9 clusters, 49 passages — over `@/data`, NOT the live
  registry. The fix is `BUILD-SITE-LIVE-DATA.md` + §8 compute-on-write.

---

## 8. THE OPERATING AXIOMS (how to work — AGENTS.md §5)

1. Never `sleep` to "wait" — do other work; background long tasks with `nohup`/`setsid` + log + `&`.
2. Kill by specific PID, never `pkill`.
3. External sources go to R2 (immutable Bronze), not local disk.
4. Reuse, don't rebuild — check canonical indexes first.
5. Respect licenses (PANDiT etc. CC BY-NC-SA → discovery/provenance, not unrestricted commercial).
6. Docs are a projection, never the truth — run the validators after any change.
7. Archive, don't delete.
8. Run the validators after changes:
   ```bash
   python3 check_directory_manifest.py
   python3 docs/vision/check_manifest.py
   python3 docs/check_docs_audit.py
   python3 docs/process/docs_state.py
   python3 machinelearning/theatre_check.py --status   # the anti-theatre gate
   ```

---

## 9. THE PRIORITY ORDER (what to do next — reconciled)

1. **THE OPENPĀṬALA BUILD** — the confirmed proposal (§3): wire the minimal product loop, compute-on-write,
   consume agentgraph's provenance kernels at the seam. **This is the current task.**
2. **Wire the site/API/MCP to live data** (`BUILD-SITE-LIVE-DATA.md`) — currently static, needs the live
   registry + compute-on-write.
3. **Converge the 6 divergent contracts** (`BUILD-CONTRACTS-CONVERGENCE.md`) — agentgraph's peer-notes say
   done (10/10); verify against our side.
4. **The parallel factory** (`BUILD-PARALLEL-FACTORY.md`) — supply the bootstrap + real producers +
   real-data test for agentgraph's `factory_pool.py` (§5 finding).
5. **`misconception.py`** — the universally-named #1 organism gap (agentgraph's lane to build).
6. **Drive the factory with `next_action`** (`BUILD-FACTORY-COORDINATION.md`).

---

## 10. THE ENTRY PATH FOR A NEW AGENT (the designed read-order)

```text
STEP 0  HANDOVER.md                    ← you are here in spirit; the complete current state
STEP 1  AGENTS.md                      ← the ONE rule + axioms (read before building)
STEP 2  NAVIGATION.md                  ← the master index (resolve anything)
STEP 3  docs/process/README.md         ← the process + canonical indexes
...
STEP 8  migration/v3/README.md         ← the CURRENT blueprint + proofs
STEP 9  migration/shared/README.md     ← the COORDINATION with agentgraph
THIS FILE (MASTER-KNOWLEDGE.md)        ← the consolidated fast-reference for the two-sided build
```

---

*This file is the master knowledge reference. It consolidates the two-sided build, the confirmed
OpenPāṭala proposal, the verified v3 reality, and the peer-review findings. Read it after HANDOVER +
AGENTS, before going deep. The truth is the tests + `object_registry` + git — verify anything you build on.*
