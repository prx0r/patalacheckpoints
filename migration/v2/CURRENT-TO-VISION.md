# PĀṬALA — CURRENT STATE → VISION STATE (every mechanism: as-is, to-be, why, how, integration)

*2026-08-14 · status: THE SYNTHESIS · companion to `LAYERS.yaml` + `LAYER-MAPPING.md` + `MODULES.md` +
`PATALA-V2-SPEC.md`. For EVERY mechanism: what it IS right now · what it BECOMES in v2 · WHY · HOW we
get there · how it INTEGRATES with the other layers. The build order EMERGES from this — each row's
"gap" is a concrete work item, and the integration column shows what it unblocks.*
*All "current" claims verified against the actual code/state on 2026-08-14.*

---

## THE FRAMEWORK (how to read each mechanism)

For every mechanism, six fields:

1. **CURRENT** — what it is today (verified, honest)
2. **VISION** — what it becomes in v2 (from the SPEC)
3. **WHY** — the reason for the change (the problem it fixes)
4. **HOW** — the concrete path (which files/pattern)
5. **INTEGRATION** — what it connects to / unblocks
6. **GAP** — the delta (a build order item)

---

## MECHANISM 1 — THE KERNEL (identity · authority · objects)

**CURRENT**
- `python/patala_core/` has a REAL AuthorityVector (`authority.py`: 4 axes, gate predicates, no scalar
  rank), typed objects (`objects.py`: Proposition/Crux/ReviewEvent/Adjudication), `ids.py` + the
  `docs/atlas-contracts/` contracts.
- **BUT** the factory (`object_registry.py`), `review_engine.py`, and `source-evidence/schema/` each
  define their OWN ReviewEvent/Authority. **Verified: 4 distinct implementations.** `patala_core` is a
  parallel implementation, not canonical.

**VISION**
- `patala_kernel/` = the ONE source of truth for identity/derivation/authority/events/reducers/gates/
  staleness. Every subsystem imports it. Nothing defines these semantics elsewhere.

**WHY**
- Four definitions = schema divergence = the exact disease the whole project is escaping. Every
  downstream capability (synthesis, education, scholar attestation) embeds drift if the kernel isn't one.

**HOW**
- Promote `patala_core` to canonical. Retire the 3 parallel ReviewEvent/Authority definitions. Add the
  missing kernel pieces (`derivation.py`, `events.py`, `reducers.py`, `gates.py`, `staleness.py`).

**INTEGRATION**
- Every mechanism below imports it. It's the substrate everything else rests on.

**GAP** → *converge the kernel (Phase 0/2). Smallest real move: make `patala_core` canonical.*

---

## MECHANISM 2 — THE LEDGER (object_registry)

**CURRENT**
- `pipeline/object_registry.py`: versioned registry as **JSONL files** (`data/corpus/registries/*.jsonl`,
  17 registries) + an **event log** (`object-events.jsonl`) + atomic writes + `summary()`. This is the
  de-facto truth ledger. Counts: SOURCE=32039, T1=306, L0=791, ARGMAP=50, L2=3, L200=5, C1=3.

**VISION**
- The ledger stays the append-only truth (event log + registry), but it becomes the WRITE side only.
  A reducer materializes current state into **Postgres** (the read side). The ledger is authoritative;
  Postgres is the compiled projection of it.

**WHY**
- Today Postgres (`migrate.py`) and the ledger are **disconnected** — separate truths that can drift.
  v2 makes the ledger the source and Postgres a projection, so there's ONE truth.

**HOW**
- Add a reducer that reads the ledger/events and writes Postgres. Kill the independent `migrate.py`
  write path (it becomes a projection writer).

**INTEGRATION**
- The factory reads/writes it; the reducer projects it to Postgres; the site reads Postgres/compiled
  output. Closing this seam kills the four-truths problem.

**GAP** → *ledger → Postgres projection (the reducer).*

---

## MECHANISM 3 — THE FACTORY / COMPILER (scheduler + workers + loop)

**CURRENT**
- `pipeline/factory_scheduler.py` + workers + `factory_loop.sh`. **Verified:** the loop runs
  `LAYERS="T1,ARGMAP,L0,L2,L200,C1"` — THEME/ESSAY/EDUCATION are NOT in the loop. ARGUMENT/SYNTHESIS
  workers exist (`autonomy.py` wires real handlers) but produce 0 objects. L200=5, C1=3.

**VISION**
- The factory becomes a **reactive compiler**: driven by the transformation registry + derivation graph,
  computing staleness and recompiling only what changed. THEME→ESSAY→LESSON become compiled projections
  in the loop. Every layer's output is a projection with a proof path.

**WHY**
- The current loop stops at C1 and leaves the upper layers EMPTY. The compiler model makes the whole
  spine runnable and gated (nothing builds until its inputs are real and reviewed).

**HOW**
- Extend the loop to the upper layers as projections. Add the transformation registry + staleness over
  object-level dependency edges.

**INTEGRATION**
- Feeds Postgres (projection), the site (compiled artifacts), and the education/scholar products
  (which consume the upper layers).

**GAP** → *upper-layer projection + transformation registry + staleness.*

---

## MECHANISM 4 — REVIEW / ADJUDICATION (the reducer)

**CURRENT**
- `pipeline/review_engine.py` (ReviewEvent ledger + impact_report), `review_bundle.py`,
  `contracts_human_authority.py`. Already event→reducer→state. But `evidence_ok: bool` is lossy and the
  ReviewEvent def diverges from `patala_core`.

**VISION**
- Typed events (EvidenceAttached, TranslationAuditCompleted, ContradictionRaised, FindingResolved,
  AdjudicationRecorded) + canonical Findings. Agents submit CLAIMS about state, never state itself.
  Deterministic reducer + gate. One ReviewEvent definition.

**WHY**
- `evidence_ok: bool` throws away the months of work building a non-lossy system. The four defs must
  converge. Review is the gate everything upper depends on.

**HOW**
- Adopt `patala_core`'s objects as canonical; type the reducer inputs; add Findings + gates.

**INTEGRATION**
- The gate for TranslationProof, Argument, Synthesis, publication, scholar attestation.

**GAP** → *kernel convergence + typed reducer inputs.*

---

## MECHANISM 5 — THE ATLAS (identity + Postgres)

**CURRENT**
- `python/patala_core/atlas/` (migrate/resolver/adapter/api) + Postgres 22-table schema + the 254-work
  bibliography (`atlas-bibliography.json`). The site reads `.ts`/JSON seeds, NOT Postgres (verified: 33 of
  43 API routes read `@/data/*` files; 0 hit Postgres).

**VISION**
- Postgres = the compiled projection of the ledger. The site reads compiled objects (from Postgres/
  R2), not `.ts` seeds. Bibliography/identity = projections of the same objects.

**WHY**
- Today the site, the DB, and the ledger are three truths. v2 makes the site read the graph.

**HOW**
- Close the read path: site → compiled objects (Postgres or R2). Backfill the rich atlas fields.

**INTEGRATION**
- The identity backbone every object references; the read plane's source.

**GAP** → *site read path + Postgres projection + atlas backfill.*

---

## MECHANISM 6 — THE SITE / SURFACES (app + API + MCP)

**CURRENT**
- `app/` (Next.js) + `app/api/` (43 routes) + `mcp/index.mjs` (29 tools). **33/43 routes read `@/data`
  (.ts/JSON) seeds; 0 hit Postgres.** Lemma-through-time (`/terms/:lemma/history`) + timeline
  (`/history/timeline`) both implemented. Products: the 16-product catalog (`strategy/PRODUCTS.md`).

**VISION**
- Thin read plane over compiled objects. MCP collapses to ~8 verbs (resolve/search/get/context/trace/
  compare/query/submit). Context Bundles (micro 2k / standard 8k / deep 32k) as agent cache lines.
  Each product = a compiled projection.

**WHY**
- The site is the product surface. Making it read the graph (not `.ts`) is what makes the products real
  and the counts true.

**HOW**
- Wire the read path to compiled objects. Collapse MCP. Build the product projections.

**INTEGRATION**
- Consumes every layer's compiled output; Hermes sits above the thin MCP.

**GAP** → *read-path wiring + MCP collapse + product projections.*

---

## MECHANISM 7 — TRANSLATIONPROOF (the moat)

**CURRENT**
- `l200_worker.py` + `certificate_l200.py` + `inspect_l200*` + tests all exist. **Verified:** registry
  has L200=5, but **63 gold audits sit in the sibling `sanskritree` repo, never registered.**

**VISION**
- TranslationProof = a real, queryable asset: 63 registered proofs with derivation edges (proof→C1→T1→
  SOURCE), non-aggregate vector exposed per proof. The flagship product + the moat.

**WHY**
- It's the claimed differentiator, but it's a design + 5 rows + 63 stranded golds. Registering it makes
  it real.

**HOW**
- **Write the L200 + C1 bulk-ingest** (mirror `ingest_ipvv_argmap_golds.py`, which took ARGMAP 1→50).
  Register the 63 L200 + 63 C1 with derivation edges. Then expose per-proof vectors.

**INTEGRATION**
- The moat under the scholar products; unblocks Synthesis/Essay/Lesson (their inputs).

**GAP** → ***THE L200 + C1 INGEST — the single highest-value next build.***

---

## MECHANISM 8 — THE ML / RESEARCH ENGINES (44 modules)

**CURRENT**
- `machinelearning/research/patala_ml/` = 44 modules (argument, crux_engine, aspic_adapter, aifgraph,
  nyayagate, synthesis_core, essay_compiler, education_compiler, theme_discovery, kcore, cluster,
  semantic_alignment, retrieval, pushing, gold002-005, etc.). All import cleanly; gold is IPVV.

**VISION**
- These become the transformation implementations behind the kernel — each a `@transformation` with a
  verifier, driven by the registry. The argument layer (CP4) is the frontier.

**WHY**
- The engines are real but disconnected; the transformation registry makes them composable + gated.

**HOW**
- Wrap each engine as a transformation with verifier + authority policy. Drive via the registry.

**INTEGRATION**
- The spine workers; the eval plane; the scholar products.

**GAP** → *transformation registry over the 44 engines.*

---

## MECHANISM 9 — THE PRIMA MATERIA / EXTRACTION (IPVV + pushing)

**CURRENT**
- IPVV is the gold standard corpus (Source→Commentary real + tested; 63 L200 + 63 C1 golds; 51 ARGMAP;
  22 essays) in the sibling repos. The **pushing method** (`research-library/pushing/PUSHING_GUIDE.md`,
  `AUTONOMOUS_PUSHING_AGENT_SPEC.md`) is the extraction engine. The layered questionnaire is the
  education bridge.

**VISION**
- The pushing method becomes the content-generation side of the Education/Lesson products. The gold
  (IPVV) feeds every layer. The questionnaire lets Pāṭala scale beyond Tantra.

**WHY**
- The prima materia exists; the extraction method exists; the education product doesn't yet consume them.

**HOW**
- Register the gold (Mechanism 7). Wire pushing output (claims/cruxes) into Lesson generation.

**INTEGRATION**
- Feeds Education, Research Packet, Comparison, Synthesis.

**GAP** → *gold ingest + pushing→education wiring.*

---

## THE BUILD ORDER (emerges from the gaps)

```
PHASE A — MAKE THE GOLD REAL (the moat + everything depends on it)
  1. L200 + C1 bulk-ingest (63+63 golds → registry with derivation edges)   ← Mechanism 7
     unblocks: TranslationProof product, Synthesis/Essay/Lesson inputs, scholar attestation

PHASE B — ONE TRUTH (kill the divergence + four-stores problem)
  2. Converge the kernel (promote patala_core; retire 3 parallel defs)      ← Mechanism 1
     unblocks: every downstream capability; kills schema drift
  3. Ledger → Postgres projection (the reducer)                             ← Mechanism 2
     unblocks: one truth; the site can read the graph

PHASE C — THE READ PLANE (the products become real)
  4. Site read path: read compiled objects, not .ts seeds                   ← Mechanism 6
  5. Collapse MCP to 8 verbs + Context Bundles                              ← Mechanism 6
  6. Transformation registry over the 44 engines                            ← Mechanism 8

PHASE D — THE UPPER STACK (the honest EMPTY layers become real)
  7. THEME→ESSAY→LESSON as compiled projections in the loop                ← Mechanism 3
  8. Staleness + reactive compiler                                           ← Mechanism 3
  9. Pushing → education wiring (prima materia → Lesson)                    ← Mechanism 9

PHASE E — THE SCHOLAR PRODUCTS
  10. Scholar attestation to granular objects                               ← Mechanism 4
  11. Research Packet / Comparison / Audit / Benchmark products             ← Mechanism 6
```

**The ordering principle:** build bottom-up so nothing is theatre. Each phase makes the previous one's
output REAL in the system. Phase A is first because the gold is the substance everything else projects —
and it's the smallest, highest-leverage move (a proven-pattern script, no architecture bet).

---

*This is the current→vision map for every mechanism. The build order fell out of it: **gold ingest first
(the substance), then convergence (one truth), then the read plane (products), then the upper stack
(the honest layers), then the scholar products.** Each gap is a concrete, scoped work item.*
