# PĀṬALA V2 — THE REUSABLE MODULE INVENTORY (tagged · lifecycle · gold standard · scholar products)

*2026-08-14 · status: PROPOSAL · companion to `LAYER-MAPPING.md` + `LAYERS.yaml`. This is the complete
inventory of EVERY reusable module in Pāṭala, tagged by what it does and how it maps to v2. It answers
three questions an agent or builder actually asks: (1) what modules can I REUSE? (2) how do they form
the Sanskrit→Education lifecycle? (3) what are the scholar products?*
*The gold standard throughout is the **IPVV** (Īśvarapratyabhijñāvivṛtivimarśinī) vertical — the one
corpus where every layer has real, human-authored gold.*

---

## 0. Tag legend

Every module is tagged `[L<layer>]` (which v2 layer it serves), `[REUSE]` (proven, safe to reuse),
`[PARTIAL]` (works but needs attention), `[GOLD-IPVV]` (the gold standard reference), and a one-line
"what it does."

- `[REUSE]` = built + tested, do not rebuild
- `[PARTIAL]` = exists but has a known gap (called out)
- `[GOLD-IPVV]` = the module is validated against the IPVV gold vertical
- `[NEW]` = needed but does not exist yet

---

## 1. THE KERNEL (identity · authority · objects) — the v2 spine

| Module | Tags | What it does | v2 name |
|---|---|---|---|
| `python/patala_core/authority.py` | `[REUSE]` | AuthorityVector — 4 axes (generation/evidence/review/publication), gate predicates, display badge, **NO scalar rank** | **kernel/authority** |
| `python/patala_core/objects.py` | `[REUSE]` | typed scholarly objects: Proposition, Commitment, GroundingLink, InferenceApplication, Crux, ReviewEvent, ReviewProposal, Adjudication | **kernel/objects** |
| `python/patala_core/ids.py` | `[REUSE]` | canonical `pt:` URN ids | **kernel/identity** |
| `docs/atlas-contracts/*` (10 docs) | `[REUSE]` | the contract specs for the above + read-api, source-resolver, access-policy | kernel contracts |
| *(missing)* | `[NEW]` | `derivation.py` — explicit parents+transformation edges; `events.py`+`reducers.py`; `gates.py`; `staleness.py` | kernel |

**⚠️ Divergence (verified):** 4 distinct ReviewEvent/Authority definitions exist. v2 promotes
`patala_core` to canonical and retires `pipeline/object_registry.py`, `pipeline/review_engine.py`, and
`source-evidence/schema/`'s copies. **The kernel is half-built — the authority model already exists.**

---

## 2. THE FACTORY / COMPILER (advances every layer)

| Module | Tags | What it does |
|---|---|---|
| `pipeline/object_registry.py` | `[REUSE]` | versioned registry + event ledger + atomic writes + `summary()` (the live counts) |
| `pipeline/factory_scheduler.py` | `[REUSE]` | eligibility → schedule → run (per-layer, per-work) |
| `pipeline/factory_batch.py` | `[REUSE]` | failure/retry queue |
| `pipeline/factory_rebuild.py` | `[REUSE]` | A2-18 DependencyImpactReport |
| `pipeline/factory_certificate.py` | `[REUSE]` | live-registry integrity cert (789 bad hashes — live-data debt) |
| `pipeline/factory_status.py` · `catalog.py` | `[REUSE]` | status + catalog views |
| `contracts/CANONICAL-DAG.yaml` | `[REUSE]` | the ONE dependency manifest every consumer derives from |
| `pipeline/autonomy.py` | `[REUSE]` | wires `LAYER_HANDLERS` incl. real ARGUMENT/SYNTHESIS workers |

---

## 3. THE SCHOLARLY SPINE WORKERS (Source → Lesson) — each maps to its v2 layer

### 3.1 Source (position 0)
| Module | Tags | What it does |
|---|---|---|
| `ingestion/asserter.py` | `[REUSE]` | SourceAsserter: external → canonical objects |
| `ingestion/r2.py` | `[REUSE]` | SnapshotStore — R2 Bronze, content-addressed |
| `ingestion/adapters/*` | `[REUSE]` | PANDiT/SARIT/etc per-source adapters |
| `pipeline/register_sources.py` | `[REUSE]` | commits RAW-EN works as SOURCE |

### 3.2 DraftTranslation (position 1)
| Module | Tags | What it does |
|---|---|---|
| `pipeline/t1_worker.py` | `[REUSE]` | working draft translation |
| `pipeline/import_sanskritree.py` | `[REUSE]` | old-batch (141 T1, 11 T3) conversion |
| `skills/translate-passage` | `[REUSE]` | the full draft→proof→commentary passage flow |

### 3.3 Tokenization (position 2)
| Module | Tags | What it does |
|---|---|---|
| `pipeline/l0_worker.py` | `[REUSE]` | token records from the draft |
| `pipeline/certificate_l0.py` | `[REUSE]` | deterministic floor cert (lossless/bound/fail-closed) |
| `pipeline/benchmark_l0_replay.py` | `[REUSE]` | L0 replay benchmark |

### 3.4 ArgumentOutline (position 3)
| Module | Tags | What it does |
|---|---|---|
| `pipeline/argument_map_worker.py` | `[REUSE]` | the lateral argument outline |
| `pipeline/ingest_ipvv_argmap_golds.py` | `[REUSE][GOLD-IPVV]` | ingests the 51 real IPVV ARGMAP golds (50/51 committed) |

### 3.5 Translation (position 4)
| Module | Tags | What it does |
|---|---|---|
| `pipeline/l1_l2_worker.py` | `[REUSE]` | readable prose translation guided by the outline |
| `pipeline/state_machine.py` | `[REUSE]` | the T1→R1→T2→R2→T3→T3.1→C1 micro-stage machine |

### 3.6 TranslationProof (position 5) — **THE MOAT**
| Module | Tags | What it does |
|---|---|---|
| `pipeline/l200_worker.py` | `[REUSE]` | the 8-section derivation proof |
| `pipeline/certificate_l200.py` | `[REUSE]` | proof-layer integrity cert |
| `source-evidence/evals/inspect_l200*.py` | `[REUSE][GOLD-IPVV]` | L200 NAT inspection on the IPVV gold |
| **sibling `sanskritree/.../ipvv/l200/` (63 audits)** | `[GOLD-IPVV]` | the 63 hand-authored proof audits |
| **`migration/v2/LAYERS.yaml` §5** | `[GOLD-IPVV]` | the TranslationProof vector-of-obligations spec |

### 3.7 Commentary (position 6)
| Module | Tags | What it does |
|---|---|---|
| `pipeline/c1_worker.py` | `[REUSE]` | compact passage-local commentary |
| **sibling `sanskritree/.../ipvv/c1/read+source/` (63 each)** | `[GOLD-IPVV]` | the 63 C1 gold records |

### 3.8 Theme (position 7)
| Module | Tags | What it does |
|---|---|---|
| `pipeline/theme_worker.py` | `[REUSE]` | theme/cluster discovery driver |
| `machinelearning/research/patala_ml/theme_discovery.py` | `[REUSE]` | theme discovery |
| `machinelearning/research/patala_ml/kcore.py` | `[REUSE]` | k-core decomposition |
| `machinelearning/research/patala_ml/cluster.py` | `[REUSE]` | clustering |
| `data/published/ipvv/clusters.json` | `[GOLD-IPVV]` | the IPVV theme clusters |

### 3.9 Argument (position 7) — the frontier
| Module | Tags | What it does |
|---|---|---|
| `machinelearning/research/patala_ml/argument.py` | `[REUSE]` | the argument model |
| `machinelearning/research/patala_ml/aspic_adapter.py` | `[REUSE]` | ASPIC+ argumentation adapter |
| `machinelearning/research/patala_ml/aifgraph.py` | `[REUSE]` | AIF argument-interchange graph |
| `machinelearning/research/patala_ml/crux_engine.py` | `[REUSE]` | the Crux primitive (minimum unresolved proposition) |
| `machinelearning/research/patala_ml/proposition_layer.py` | `[REUSE]` | the proposition layer |
| `machinelearning/research/patala_ml/nyayagate.py` | `[REUSE]` | the Nyāya gate (bounded, never truth) |
| `machinelearning/research/patala_ml/builders.py` | `[REUSE]` | argument builders |
| `pipeline/epistemic_worker.py` | `[REUSE]` | wires real ARGUMENT + SYNTHESIS handlers |

### 3.10 Review / Adjudication (cross-cutting)
| Module | Tags | What it does |
|---|---|---|
| `pipeline/review_engine.py` | `[REUSE]` | ReviewEvent ledger + impact_report (the reducer) |
| `pipeline/review_bundle.py` | `[REUSE]` | ReviewBundle |
| `pipeline/scholarly_oracle.py` | `[REUSE]` | make_source_assertion / corroboration / run_vertical |
| `source-evidence/schema/contracts_human_authority.py` | `[REUSE]` | Proposal/Adjudication/Promotion |
| `machinelearning/research/patala_ml/adjudicate.py` | `[REUSE]` | adjudication logic |

### 3.11 Synthesis (position 8)
| Module | Tags | What it does |
|---|---|---|
| `machinelearning/research/patala_ml/synthesis_core.py` | `[REUSE]` | ArgumentSynthesis (the convergence object) |
| `pipeline/epistemic_worker.py` (`make_synthesis_handlers`) | `[REUSE]` | the synthesis worker (0 objects — honest) |

### 3.12 Essay (position 9)
| Module | Tags | What it does |
|---|---|---|
| `machinelearning/research/patala_ml/essay.py` | `[REUSE]` | the essay model |
| `machinelearning/research/patala_ml/essay_compiler.py` | `[REUSE]` | essay compiler |
| `machinelearning/research/patala_ml/essayverify.py` | `[REUSE]` | essay verification (sentence dependency) |
| `machinelearning/research/patala_ml/essayplan.py` · `essaysentence.py` · `essaygen.py` | `[REUSE]` | essay planning/sentencing/generation |
| `pipeline/essay_worker.py` | `[REUSE]` | the essay worker (0 objects — honest) |
| **sibling `research-library/recognition/ESSAY-*.md` (22)** | `[GOLD-IPVV]` | the 22 gold essays |

### 3.13 Lesson / Education (position 10)
| Module | Tags | What it does |
|---|---|---|
| `machinelearning/research/patala_ml/education_compiler.py` | `[REUSE]` | education compiler |
| `machinelearning/research/patala_ml/education_ir.py` | `[REUSE]` | education IR (the 4 native objects: LearningClaim/Skill/Interaction/MasteryEvidence) |
| `pipeline/education_worker.py` | `[REUSE]` | the lesson worker (0 objects — honest) |
| `docs/vision/education/PATALA-EDUCATION-SYNTHESIS.md` | `[GOLD-IPVV]` | the education cross-lane synthesis |
| `source-evidence/evals/patala/tasks/edu_bench.py` | `[REUSE]` | the education benchmark (measured 0.4 epistemic-valid) |

---

## 4. THE FULL LIFECYCLE — Sanskrit → Education (one line each hop)

```
Sanskrit source (R2 Bronze)
   └─ Source ────────────────[ingestion/asserter + r2.py]──────────────▶ SOURCE
      └─ DraftTranslation ───[t1_worker]──────────────────────────────▶ T1 draft
         └─ Tokenization ────[l0_worker + certificate_l0]─────────────▶ token floor
            ├─ ArgumentOutline ─[argument_map_worker + 51 IPVV golds]──▶ the guide
            └─ Translation ────[l1_l2_worker]──────────────────────────▶ prose
               └─ TranslationProof ─[l200_worker + 63 IPVV audits]─────▶ the moat
                  └─ Commentary ───[c1_worker + 63 IPVV golds]─────────▶ living interpretation
                     ├─ Theme ─────[theme_worker + kcore/cluster]──────▶ clusters
                     └─ Argument ──[argument.py + crux_engine + nyayagate]▶ propositions→cruxes
                        └─ Review/Adjudication ─[review_engine]────────▶ reviewed state
                           └─ Synthesis ───[synthesis_core]────────────▶ convergence
                              └─ Essay ────[essay_compiler + 22 golds]──▶ proof-linked prose
                                 └─ Lesson ─[education_compiler]───────▶ questions+distractors
                                    └─ Scholar Attestation ─[contracts_human_authority]▶ human gate
```

**The honest truth:** the lifecycle is REAL and TESTED from Source → Commentary (positions 0-6),
with **Review/Adjudication** operating throughout. Everything from **Synthesis (7) up is EMPTY**
(0 objects) — the workers exist but nothing triggers them until their inputs are real and gated.

---

## 5. ORIGINAL CONCEPTS & INFRA — ALL RELEVANT FILES REFERENCED

The "original" Pāṭala ideas (lemma-through-time, the timeline, external tools, translation proofs)
are not aspirational — they have a real start. This is the complete file reference for each, so an
agent can go straight to the code/data.

### 5.1 Lemma-through-time (diachronic sense-trajectories) — IMPLEMENTED

| File | What it is |
|---|---|
| `data/corpus/trajectories.ts` (349 ln) | the curated historical-sense trajectories (the "lemma through time" data) |
| `data/corpus/terms.ts` (74 ln) | the term/lemma records |
| `data/corpus/passages.ts` | the passage records the terms reference |
| `data/terms.json` | the compiled terms data |
| `data/term_proposals.jsonl` | machine/curated term-sense proposals (the reviewable layer) |
| `app/api/terms/route.ts` | list terms |
| `app/api/terms/[lemma]/history/route.ts` | **the diachronic trajectory** (per-lemma sense-through-time) |
| `app/api/terms/[lemma]/senses/route.ts` | the senses of a lemma |
| `app/api/terms/[lemma]/occurrences/route.ts` | the occurrence counts |
| `docs/api/concepts/epistemic-model.md` | the status rules these assertions obey (proposed ≠ accepted) |

**Status:** built + serving. Trajectories are CURATED projections (not auto-derived from the graph) —
honest per the docstring. v2 direction: make them compiled projections once the graph is real.

### 5.2 The timeline (school/tradition chronology) — IMPLEMENTED

| File | What it is |
|---|---|
| `data/atlas/historyTimeline.json` (13KB) | the chronological school/tradition map (from the Śiva-before-Abhinava genealogy) |
| `app/api/history/timeline/route.ts` | serves the timeline |
| `docs/vision/expansion/vision-11-siva-before-abhinava-prehistory.md` | the source genealogy it's built from |

### 5.3 External tools & adapters — the honest split (6/69 wired)

| File | What it is | Status |
|---|---|---|
| `source-evidence/docs/tools/MANIFEST.json` | the 69-tool registry (INTEGRATED/WIRED/PARTIAL/DOCS_ONLY/PLANNED) | the source of truth |
| `source-evidence/docs/tools/INDEX.md` | the tool index | |
| `source-evidence/production/adapters/grobid_live.py` | GROBID (real) | PARTIAL |
| `source-evidence/production/adapters/metadata_resolver.py` | Crossref + OpenAlex (real) | WIRED |
| `source-evidence/production/adapters/opencitations.py` | OpenCitations (real) | PARTIAL |
| `source-evidence/production/adapters/identity_crosswalk.py` | ORCID/ROR name-variant crosswalks (real) | WIRED |
| `source-evidence/production/adapters/scholar_document.py` | scholar-doc parse (placeholder parse — see audit) | PARTIAL |
| `ingestion/adapters/{pandit,sarit,gretil,csalt,viaf,wikidata,ngmcp,iiif}.py` | the 8 real ingestion adapters | REUSE |
| `docs/process/external-tools.md` | the status board | |
| *(20 DOCS_ONLY: docling, anystyle, zotero, inception, recogito, hypothesis, ro-crate, ...)* | documentation only, no code | DOCS_ONLY |
| *(38 PLANNED)* | identified, not started | PLANNED |

**Honest reading:** the Sanskrit-relevant tooling (vidyut, the ingest adapters, crossref/openalex) is
REAL. Most borrowed tools are docs. The `vidyut` SanskritLinguisticAdapter is INTEGRATED.

### 5.4 TranslationProof (the moat) — machinery + gold exist; proofs not yet in the registry

| File | What it is |
|---|---|
| `pipeline/l200_worker.py` | the 8-section proof generator |
| `pipeline/certificate_l200.py` | the proof-layer integrity certificate |
| `pipeline/benchmark_l200_live.py` | live L200 benchmark |
| `source-evidence/evals/inspect_l200.py` | the L200 inspector |
| `source-evidence/evals/inspect_l200_nat.py` · `inspect_l200_detector_nat.py` | the L200 NAT evals |
| `pipeline/test_l200_ipvv.py` · `test_l200_v2o.py` | the L200 tests |
| **sibling `sanskritree/translations/_stack/ipvv/l200/` (66 files / 63 audits)** | the hand-authored gold proofs |
| **sibling `sanskritree/.../c1/read/` (63) + `c1/source/` (63)** | the C1 gold records |
| `pipeline/review_bundle.py` | the only current consumer of `TranslationProof` |
| `migration/v2/LAYERS.yaml` §5 + `PATALA-V2-SPEC.md` §5 | the vector-of-obligations spec |

**The gap (verified):** registry has L200=5, C1=3. The 63 golds live in the sibling repo, never
registered. The moat's machinery + gold are complete; the proofs just aren't IN Pāṭala yet. The
**L200+C1 bulk-ingest** closes this and is the single highest-leverage v2 move.

---

## 6. THE SCHOLAR PRODUCTS (the human-facing outputs)

These are the products a scholar (and the public) actually consume. Each is a **compiled projection**
of the graph — not a separate system.

| Product | What it is | Built on | Status |
|---|---|---|---|
| **Adversarial Review** | `vision-06` — the research-compiler diagnostics (ERROR/WARNING/INFO), auditable criticism, dependency/impact | `review_engine.py` + `atlas-contracts` | ASPIRATIONAL |
| **Scholar Workbench** | `vision-07` — forkable scholarship, "AI proposes, scholar adjudicates" | `app/` + `review_engine` + `contracts_human_authority` | ASPIRATIONAL |
| **Scholar Attestation Vertical** | scholar attests to granular objects/findings/transformations | `contracts_human_authority.py` (Proposal/Adjudication) | the priority |
| **The Atlas / "OpenAlex for Sanskrit"** | `vision-15` — the research graph | `python/patala_core/atlas/*` + `app/` | PARTIAL |
| **Manuscript → Scholarly Asset** | `vision-14` — manuscript reconciliation | `manuscript_resolution_gold.py` + `entity_reconciliation.py` | PARTIAL |
| **Peer Review service** | `vision-06` + `patala-peer-review.md` | `review_engine` + `review_bundle` | PARTIAL |
| **Lesson / Course products** | the compiled educational projections | `education_compiler` + `essay` | EMPTY (honest) |
| **Media / Video projections** | `vision-09` — the media layer | (R2 render buckets exist: `essayviz-*`, `goldrender-*`) | DESIGN |

**The scholar product pipeline (how a scholar's work becomes canonical):**
```
Scholar reviews a granular object (a finding / a proof / a crux decision)
   → emits a ReviewEvent (Proposal / Adjudication)
   → reducer computes impact (what downstream becomes stale / changes)
   → object's AuthorityVector advances (review axis)
   → if ADJUDICATED + generation VALIDATED → eligible_for_publication
   → compiled out to the site / the bundle / the lesson
```

---

## 7. VERIFICATION / EVAL PLANE (how anything is proven real)

The anti-theatre gate. Every `[REUSE]` claim above must be backed by one of these.

| Eval | What it proves |
|---|---|
| `atlas_nat.py` + `atlas_nat_natural.py` | 51 frozen NAT cases on the atlas |
| `argument_recovery_bench.py` | P0 — the judge (recovery gold, 51 cases) |
| `semantic_recovery_judge.py` | 2-stage recovery scorer |
| `manuscript_resolution_gold.py` | FALSE_MERGE_RATE on 10 frozen cases |
| `entity_reconciliation.py` | typed CandidateMatch (EXACT/PROBABLE/CONFLICT/...) |
| `warrant_reconstruction.py` · `essay_bench.py` · `edu_bench.py` · `synthesis_nat.py` | the per-layer NATs |
| `atlas_quality_scorecard.py` · `atlas_qa_audit.py` | the atlas health scorecards |
| **the 5 golds** | `recovery-gold-v1.json` (51) · `nyaya-gate-gold.jsonl` (12) · `p3_lexical_gold_v0.json` · `p4_alignment_eval_report.json` · `manuscript_resolution_gold.py` |

---

## 8. WHAT DOES NOT EXIST YET (the v2 `[NEW]` list)

These are the genuine gaps — everything else is reusable.

1. **`derivation.py`** — explicit `parents + transformation + policy` edges (the linchpin)
2. **`events.py` + `reducers.py`** — canonical typed events + deterministic reducer (the kernel's missing half)
3. **`gates.py`** — the gate predicates (partially in `authority.py`, needs the general form)
4. **`staleness.py`** — dependency-driven invalidation over object-level edges
5. **`transformation registry`** — the `@transformation` decorator + registry driving scheduling/MCP/docs
6. **`projection compiler`** — canonical state → immutable R2 bundles/pages (the read plane)
7. **L200 + C1 bulk-ingest** — register the 63 golds + 63 C1 with Derivation edges (counts are false today)
8. **ledger → Postgres projection** — reducer writes Postgres from events (kill the four-truths problem)
9. **site read path** — stop reading `.ts` seeds; read compiled objects

---

*Every `[REUSE]` module is a real file you can import today. The gold standard is IPVV end-to-end
(Source→Commentary real + tested, with hand-authored golds at every layer; Synthesis→Lesson gated behind
real inputs). The v2 build is NOT greenfield — it is: converge the kernel (promote `patala_core`),
close the ingest + read-path seams, then add the 9 missing pieces above.*
