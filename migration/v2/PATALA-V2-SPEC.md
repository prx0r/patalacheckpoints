# PĀṬALA V2 — THE COHERENT SYSTEM SPEC (draft for review)

*2026-08-14 · status: PROPOSAL (not yet implemented) · owner: all lanes · location: migration/v2/*
*This is the v2 target. It renames the cryptic layer codes, codifies every layer with clear docs and
transformation rules, and unifies the ledger / Postgres / site / published corpus onto ONE event-sourced
kernel. It does NOT throw away the working machinery — it re-wires and renames it.*

---

## 0. Why v2

The current system works but is incoherent to read. Three separate problems:

1. **Cryptic, overlapping names.** `T1` means both a DAG layer AND a translation micro-stage. `L0`,
   `L2`, `L200` are archaeology. `C1` means two things. `ARGMAP` is an outline, not a "map."
2. **Four disconnected stores.** The site reads hand-written `data/atlas/*.ts`; Postgres is filled
   separately by `migrate.py`; the ledger is JSONL files; the published corpus is separate JSON. None
   are linked by derivation, so counts and truth drift (verified: site reads `.ts`, zero API routes
   hit Postgres).
3. **No single codified spec.** 19 docs each claim "Layer 3 is PARTIAL" independently. The DAG
   (`contracts/CANONICAL-DAG.yaml`) is the only machine spec, and it's layer-dependency-only — it
   carries no transformation, authority, or verifier per layer.

**v2 principle:** *one kernel, one derivation graph, clear names, compiled projections.* Docs and the
site become projections of state, not separate truths.

---

## 1. The rename map (code → clear name)

### 1.1 The DAG layers (the vertical spine)

| v1 code | v2 name | What it is | Produced by | Requires | Verifier |
|---|---|---|---|---|---|
| `SOURCE` | **Source** | raw text as ingested, Bronze on R2 | `ingestion` | — | source fingerprint (incipit/explicit/hash) |
| `T1` | **DraftTranslation** | working draft translation | `t1_worker` | Source | gloss precision, losslessness |
| `L0` | **Tokenization** | structured token records derived from the draft | `l0_worker` | DraftTranslation | token↔verse binding, no dupes |
| `ARGMAP` | **ArgumentOutline** | lateral argument guide over source+tokenization | `argument_map_worker` | Source, Tokenization | outline covers the passage's moves |
| `L2` | **Translation** | readable prose translation, guided by the outline | `l1_l2_worker` | Tokenization, ArgumentOutline | prose fidelity to token floor |
| `L200` | **TranslationProof** | proof of HOW each reading was derived | `l200_worker` | Translation | 8-section audit (see §5) |
| `C1` | **Commentary** | compact passage-local commentary | `c1_worker` | TranslationProof | 100–450 words, no essays-as-evidence |
| `THEME` | **Theme** | theme/cluster discovery across commentaries | `theme_worker` | Commentary | cluster coherence |
| `ARGUMENT` | **Argument** | propositions → argument → cruxes | `epistemic_worker` | Commentary | structural validity, scope, modality |
| `SYNTHESIS` | **Synthesis** | converged synthesis over arguments+themes | `epistemic_worker` | Argument, Theme | derivation-complete, adjudicated inputs |
| `ESSAY` | **Essay** | essay, sentence-sourced | `essay_worker` | Synthesis | every sentence has a dependency link |
| `EDUCATION` | **Lesson** | questions + distractors with proof paths | `education_worker` | Essay | each answer/distractor derivable |

### 1.2 The translation micro-stages (inside one passage)

| v1 code | v2 name | What it is |
|---|---|---|
| `T1` | `DraftTranslation` | working draft (same object as the DAG layer) |
| `R1` | `DraftReview` | peer review of the draft against Sanskrit |
| `T2` | `AlternativeTranslation` | a genuinely alternative reading |
| `R2` | `Adjudication` | adjudication between draft / alternative |
| `T3` | `FinalTranslation` | the settled reading |
| `T3.1` | `FinalProof` | proof layer on the final reading |
| `C1` | `Commentary` | the commentary |

**Key unification:** the micro-stages and the DAG layers now share one vocabulary. `DraftTranslation`,
`Commentary` mean the same thing whether you are inside a passage or up the spine.

### 1.3 Worker file rename map

| v1 file | v2 package/module |
|---|---|
| `t1_worker.py` | `layers/draft_translation.py` |
| `l0_worker.py` | `layers/tokenization.py` |
| `argument_map_worker.py` | `layers/argument_outline.py` |
| `l1_l2_worker.py` | `layers/translation.py` |
| `l200_worker.py` | `layers/translation_proof.py` |
| `c1_worker.py` | `layers/commentary.py` |
| `theme_worker.py` | `layers/theme.py` |
| `epistemic_worker.py` | `layers/argument.py` + `layers/synthesis.py` |
| `essay_worker.py` | `layers/essay.py` |
| `education_worker.py` | `layers/lesson.py` |

---

## 2. The kernel (one event-sourced core)

The review (`migration/mixxii`) and this session's findings agree: **the kernel is the system.** Every
layer, every store, every surface is an application of it.

```
patala_kernel/
    identity.py        ObjectRef, Revision, content-addressed (SHA-256)
    derivation.py      parents + transformation + authority-preservation policy
    authority.py       AuthorityVector (partial-order, NOT max-of-axes)
    events.py          typed events (EvidenceAttached, TranslationAuditCompleted, ...)
    reducers.py        deterministic current-state from events
    gates.py           predicates permitting next transition
    staleness.py       dependency-driven invalidation + rebuild scheduling
    projection.py      compile canonical state → immutable artifacts
```

### 2.1 The canonical object model

```
CanonicalObject
    immutable revision
        ↓
    Derivation          parents + transformation + params + tool/model/version
        ↓
    EvidenceUses
        ↓
    AuthorityVector     generation / evidence / review / publication  (partial order)
        ↓
    append-only ObjectEvents
        ↓
    deterministic reducer
        ↓
    ProjectionState     (the current readable state)
        ↓
    gate                permits the next derivation
```

### 2.2 Authority semantics (the anti-theatre core)

Authority is a **vector with partial-order comparison**, never a scalar `max`:

```
A ⪯ B  ⟺  ∀i. A_i ≤ B_i
authority(X) ≠ max_i X_i
```

- `object TYPE ≠ epistemic STATE`. A `Source` is not automatically `SCHOLARLY_CORROBORATED` because of
  its type. A `DraftTranslation` of a scholar-reviewed source does **not** inherit scholarly review.
- Defaults are honest: new derived objects start `MACHINE_PROPOSED`; review advances independently.
- Every transformation declares its own authority-preservation policy `P_T`:

```
A(O_{n+1}) ⪯ P_T(A(O_n))
```

e.g. `scholar-reviewed Source --machine-translate--> DraftTranslation` must NOT preserve the review
axis; `adjudicated Translation --comment--> Commentary` preserves evidence but not pedagogy.

---

## 3. The transformation registry (the real unlock)

Rather than scattered `build_essay.py` / `build_questions.py` scripts, represent the transformations
once. The same registry then drives scheduling, staleness, validation, MCP, docs, and UI provenance.

```python
@transformation("reconstruct_proposition")
class ReconstructProposition:
    input       = Tokenization          # or Translation
    output      = Proposition
    invalidates = [Argument, Synthesis, Essay, Lesson]
    preserves   = [evidence, generation]       # authority axes preserved
    requires    = ["review:independent_advanceable"]
    verifier    = [proposition_schema, scope_check, modality_check]
```

### 3.1 The projection DAG (the single most important abstraction)

```
Source
  └─extract→ Tokenization
                ├─translate→ Translation ──audit→ TranslationProof
                └─reconstruct→ Proposition ──infer→ Argument
                                                       ├─synthesize→ Synthesis ──render→ Essay
                                                       │                        └─compile→ Lesson
                                                       ├─review→ ReviewState
                                                       └─crux→ Crux
```

Every projection records `input_hashes + transformation_version + config_version + output_hash`.
`hash(inputs + transformation + config)` is the cache key. If unchanged → **DO NOTHING**.

This ONE graph is simultaneously: correctness graph, staleness propagator, incremental rebuild
scheduler, and part of retrieval. That convergence is v2's biggest lever.

---

## 4. The codified layer spec (single source of truth)

This is the `LAYERS.yaml` that replaces the 19 hand-maintained status docs. Generated docs
(`CURRENT_STATE.md`, `NAVIGATION.md`, layer pages) render from it. **Status is a projection, not a
hand-written claim.**

```yaml
# migration/v2/LAYERS.yaml (conceptual shape — to be generated as machine truth)
layers:
  - name: Source
    id: source
    position: 0
    status: BUILT            # derived from object_registry, never hand-set
    requires: []
    produces: [draft_translation]
    doc: |
      Raw text as ingested. Bronze snapshot on R2 (source/ingestion/<SRC>/snapshots/).
    verifier: source_fingerprint
  - name: DraftTranslation
    id: draft_translation
    position: 1
    requires: [source]
    produces: [tokenization, argument_outline]
    doc: |
      Working draft translation of one passage. The first machine-readable scholarly object.
    verifier: gloss_precision, losslessness
  # ... every layer, same shape ...
```

**Rule:** an agent or doc that wants to know a layer's state reads `LAYERS.yaml` (+ the live registry
counts), never a prose paragraph that could be stale. `docs_state.py` already does the live-count half;
v2 extends it to carry the full per-layer contract.

---

## 5. `TranslationProof` (the moat) — codified

`TranslationProof` is a **vector of independently inspectable obligations**, not a scalar score:

```
TranslationQuality ≠ Σ_i w_i · q_i
TranslationProof = vector of obligations
```

Obligations (each independently inspectable): source coverage · grounding · morphology · syntax ·
negation · modality · terminology · semantic entailment · XCOMET · parallel witness · human review.

**Separate proof from policy:**

```
proof  = facts          (the vector)
policy = requirements   (per surface)
gate   = evaluate(proof, policy)
```

Example policies:
- private experiment: human review not required
- machine draft: `coverage ≥ 0.98`
- public machine translation: `negation PASS` + `source coverage`
- scholar edition: requires independent reviewer
- canonical edition: requires adjudication

---

## 6. The stores — how they unify (no more four truths)

| Store | v2 role | Written by | Read by |
|---|---|---|---|
| **Postgres** | canonical transactional state (the materialized projection) | reducer (from events) | factory, MCP, cold/dynamic queries |
| **R2** | immutable compiled artifacts (SHA-256 addressed) | projection compiler | CDN / static assets |
| **Ledger** (event log) | append-only truth (the source of events) | agents/workers | reducer |
| **TS seeds / published JSON** | **removed** as sources; become compiled exports | projection compiler | — |

**The site stops reading `data/atlas/*.ts`.** It reads compiled HTML/JSON from R2 (human pages) and a
thin Worker API (dynamic). The 254 works, the passages, the proofs, the lessons all come from the same
graph.

---

## 7. Execution model (Hermes = executor, never truth)

```
Pāṭala decides → Hermes executes → Pāṭala reduces
```

```
Task { transformation, inputs, policy, required_capabilities, acceptance_tests }
        ↓
RuntimeRouter → deterministic | Hermes | human
        ↓
RunResult { events[], artifacts[] }
        ↓
Pāṭala reducer decides what happened (never Hermes)
        ↓
new state → staleness → next tasks
```

- **Hermes is a replaceable runtime** behind one tiny interface: `run(task) -> RunResult`.
- Hermes memory = ergonomic operational memory. Pāṭala graph = canonical epistemic memory. Never blur.
- Hermes cron emits `ExternalChangeDetected` events; cron does not mutate truth.
- MCP is a **thin adapter** over the same query layer (not 100 tools; ~8 verbs:
  `resolve search get context trace compare query submit`).

---

## 8. The agent-facing surface (skills renamed to match)

| v1 skill | v2 name |
|---|---|
| `raw-l0` | `tokenize` |
| `translate-passage` | `draft-passage` (DraftTranslation→…→Commentary) |
| `translate-work` | `draft-work` |
| `patala-translate` | `draft-translation-loop` |
| `write-commentary` | `commentate` |
| `patala-l0` | `patala-tokenization` |
| `patala-l1` | `patala-translation` |
| `patala-l2` | `patala-translation` |
| `patala-l200` | `patala-translation-proof` |
| `patala-c1` | `patala-commentary` |
| `patala-theme` | `patala-theme` |
| `patala-essay` | `patala-essay` |
| `patala-education` | `patala-lesson` |

---

## 9. The v2 repo layout (target)

```
patala/
  kernel/            identity · derivation · authority · events · reducers · gates · staleness · projection
  schemas/           source · translation · proposition · argument · review · education · generated
  factory/           dag · compiler · projections · invalidation · queue · publish
  pipelines/         ingest · extract · sanskrit · translation · arguments · research · synthesis · education
  agents/            runtime · hermes · profiles · skills
  retrieval/         search · graph · bundles · query
  apps/              web (Astro) · api (Worker) · mcp (thin) · review
  storage/           postgres · r2 · migrations
  analytics/         duckdb · parquet · benchmarks
  interoperability/  tei · cts · aif · nanopub · prov
  experiments/       frontier (PROBE / PROVEN / archived)   ← production never imports this
  docs/              architecture · contracts · domains · operations · decisions
  tests/             schema · epistemic · provenance · compiler · integration · performance
```

**Production code never imports from `experiments/`.** An experiment is promoted by rewriting it
against stable kernel contracts.

---

## 10. The three planes (governing law per plane)

```
TRUTH PLANE      Nothing becomes true because an agent says so.
COMPILE PLANE    Nothing recomputes unless its dependencies changed.
READ PLANE       Nothing computes at request time if bytes could already exist.
```

- Truth: Postgres + Pāṭala kernel (objects/evidence/events/authority)
- Compile: Python + Hermes + DuckDB (dependencies/hashes/staleness/tasks)
- Read: immutable HTML/JSON/bundles/Parquet on R2 + CDN + thin Workers/MCP

---

## 11. Proposed build sequence (phased, low-risk first)

Phase 0 — **Rename + codify** (does NOT change behavior, only names + docs)
  1. Freeze the rename map (§1). Add a `LAYERS.yaml` (§4) as machine truth; generate `CURRENT_STATE.md`
     + layer pages from it; retire the 19 hand-maintained status docs.
  2. Rename workers/skills to match (§1.3, §8). Keep old names as aliases/redirects during transition.

Phase 1 — **Close the seams** (make counts true)
  3. Wire the ledger → Postgres projection (reducer writes Postgres from events).
  4. Make the site read the compiled bibliography/objects, not the `.ts` seeds.
  5. L200/C1 bulk-ingest: register the 63 real golds as canonical objects with `Derivation` edges.

Phase 2 — **Kernel + transformation registry**
  6. Extract `patala_kernel` (identity/derivation/authority/events/reducers/gates/staleness).
  7. Build the transformation registry (§3) and the projection DAG.
  8. Implement staleness over object-level dependencies.

Phase 3 — **Projection compiler + reactive factory**
  9. Compile canonical state → immutable R2 bundles/pages/API objects.
  10. Wire THEME→ESSAY→LESSON into the live factory loop as compiled projections.

Phase 4 — **Scholar attestation + products**
  11. Scholar attests to granular objects/findings/transformations (not "the project").
  12. Expose `patala_*` MCP verbs (explain/why/dependencies/cruxes/stale/review/attest/compile).

Phase 5 — **Measure, then optimize**
  13. Only where profiling shows a hot deterministic kernel, consider Rust.

---

## 12. What does NOT change

- The scholarly pipeline mechanics (translation flow, commentary, argument, essay) stay.
- The anti-theatre doctrine stays — it's the reason v2 exists.
- R2 ingestion → bibliography → atlas pipeline stays.
- The corpus assets (IPVV golds, 71 RAW-EN works, 141 T1, 11 T3) stay.

**v2 is not a rewrite of the scholarship. It is a rewrite of the plumbing around it, so the names are
clear, the layers are codified, and every store derives from one graph.**

---

*This is a PROPOSAL for review. Next concrete step: generate the machine-readable `LAYERS.yaml`
(§4) with the full per-layer contract (id/name/position/requires/produces/doc/verifier/authority/
transformation), then wire `docs_state.py` to render `CURRENT_STATE.md` from it. That single artifact
is the spine of v2 and the natural first build whether the team pursues rename-only or the full kernel.*
