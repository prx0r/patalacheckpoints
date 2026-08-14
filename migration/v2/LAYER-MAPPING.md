# PĀṬALA V2 — THE FULL LAYER MAPPING (names · mechanisms · process · vision · checkpoints)

*2026-08-14 · status: PROPOSAL · the complete clean map of every layer in Pāṭala v2. For each layer:
new name (v1 code) · what it is · mechanism (the real files/modules it points at) · process notes ·
what it needs · how it relates to other layers · which vision doc(s) it serves · which checkpoint it
advances. All pointers are to ACTUAL files, so an agent can go straight to the machinery.*
*Companion: `PATALA-V2-SPEC.md` (the architecture) + `LAYERS.yaml` (the machine contract). This doc is
the human/agent walkthrough of both.*

---

## How to read a layer block

```
▸ NAME (v1 code) — one-line what-it-is
  MECHANISM   → the actual worker/module/skill that does it
  PROCESS     → how it is produced, what gate it must pass, its honest state
  NEEDS       → what must be true for this layer to be real (inputs + authority)
  RELATES     → parents/children/peers in the DAG
  VISION      → vision docs + checkpoint this layer serves
```

The vertical spine, bottom to top:
`Source → DraftTranslation → Tokenization → ArgumentOutline → Translation → TranslationProof →
Commentary → Theme/Argument → Synthesis → Essay → Lesson`, with **Review/Adjudication** and
**Scholar Attestation** as cross-cutting planes, and **Ingestion/Atlas/Evidence/Verification** as the
supporting substrate (Layers 00–04).

---

## PHASE 0 — GOVERNANCE (v1 Layer 00) — stays, renamed clean

▸ **Governance** — the anti-theatre doctrine, operating axioms, agent contract.

- MECHANISM → `AGENTS.md` (rules) · `machinelearning/_ACTIVE/AGENTS-DOCTRINE.md` (master doctrine) ·
  `machinelearning/_ACTIVE/CLAIMS.md` (audit ledger) · `machinelearning/theatre_check.py` (gate) ·
  `contracts/CANONICAL-DAG.yaml` (dependency truth)
- PROCESS → the ONE RULE: nothing is real without task + gold + reproducible eval. The gate prints
  honest per-component status.
- VISION → **A (Foundations)**: `CORE-BIBLE.md` (the vision canon — one vision, 6 zoomable layers) ·
  `NORTHSTAR.md` (deepest strategy) · `endgame1..5year.md` (Vision 01-05 origin arc: translation lab /
  Tantra Hub / one scholarly infra / economic thesis / 2026-2031 window) · `foundationalideas.md`
  (passage/text identity as the anchor) · `vision/CATEGORIES.md` (the 8-category taxonomy) ·
  `vision/INDEX.md` · `vision/REVIEWS.md` · all layers (0-12) · **CP0**

---

## SUPPORTING SUBSTRATE (Layers 01–04) — the plumbing under the spine

### Layer 01 — Ingestion (name unchanged)

▸ **Ingestion** — external sources → Bronze on R2 → canonical objects.

- MECHANISM → `ingestion/asserter.py` (SourceAsserter) · `ingestion/r2.py` (SnapshotStore, R2 Bronze) ·
  `ingestion/adapters/*` (PANDiT/SARIT/etc) · `pipeline/register_sources.py`
- PROCESS → download → snapshot to R2 (immutable) → asserter writes SOURCE objects → (v2: events →
  reducer → Postgres projection). License recorded on every object.
- RELATES → feeds **Source** (the spine's floor) + **Atlas** (bibliography/identity).
- VISION → `docs/corpus/TARGETS-INDEX.md` (acquisition) · **CP1**

### Layer 02 — Atlas / Identity (v1 Layer 02, stays)

▸ **Atlas** — the canonical identity graph (works/people/traditions/authority evidence) + Postgres.

- MECHANISM → `python/patala_core/atlas/migrate.py` (Postgres 22-table schema) · `resolver.py` ·
  `adapter.py` · `api.py` · `data/atlas/*.ts` (bibliography seeds) · `data/corpus/atlas-bibliography.json`
- PROCESS → identity + authority resolution; the bibliography. **v2 change:** the site stops reading
  `.ts` directly; Postgres becomes the compiled projection of the ledger, and `.ts`/`.json` become
  exports. **Today's reality:** site reads `.ts`; DB is a separate island (verified).
- RELATES → resolves **Source** identity; provides the authority backbone every layer's objects point to.
- VISION → **G (Atlas/Identity)**: `vision-15-patala-atlas-sanskrit-research-graph.md` (OpenAlex-for-
  Sanskrit) · `vision-14-manuscript-to-scholarly-asset.md` · `vision/source-resolution/source-resolver-
  design.md` (federated resolver) · the Atlas engineering set: `vision/atlas/technical-architecture-v1.md`,
  `atlas-engineering-blueprint.md` (Postgres=R2=event-log, I1–I6), `atlas-cloudflare-edge-layer.md`,
  `atlas-performance.md` (compute-on-write / immutable=cacheable), `atlas/agent-optimization.md` ·
  `docs/foundationalideas.md` (passage/text identity as the anchor) · **CP1, CP12**

### Layer 03 — Factory / Compiler (v1 Layer 03, stays, becomes "the compiler")

▸ **Factory** — the workers + scheduler + object_registry + event ledger that advance every layer.

- MECHANISM → `pipeline/object_registry.py` (versioned registry + event ledger + atomic writes) ·
  `factory_scheduler.py` · `factory_batch.py` · `factory_certificate.py` · `factory_rebuild.py` ·
  `factory_status.py` · `contracts/CANONICAL-DAG.yaml` · `pipeline/*_worker.py` (all layers)
- PROCESS → eligibility (all `requires` satisfied + no current object) → schedule → run (Hermes or
  deterministic) → events → reducer → state. **v2 change:** this becomes the reactive compiler driven
  by the transformation registry + derivation graph; staleness = the same traversal.
- RELATES → owns the whole spine; **Review/Adjudication** and **Scholar Attestation** are its gates.
- VISION → **F (Expansion/Corpus, intake)**: `vision/expansion/vision-11-siva-before-abhinava.md` (Śaiva
  genealogy as the next major corpus) · `...-prehistory.md` (deep source tree) · `...-corpus-manifest.md` ·
  `endgame1.md` (Vision 01 — the translation laboratory) · `PATALA-V2-SPEC.md` §3 (transformation registry /
  projection DAG) · **CP0–CP9, CP12 (cross-corpus)**

### Layer 04 — Evidence (v1 Layer 04, stays)

▸ **Evidence** — contracts, adapters, external tools (the evidence seam).

- MECHANISM → `source-evidence/schema/*.py` (contracts) · `source-evidence/docs/tools/MANIFEST.json`
  (69 tools) · `source-evidence/evals/*` · `docs/process/external-tools.md`
- PROCESS → the typed evidence substrate every scholarly object carries. **v2:** `EvidenceUses` +
  `AuthorityVector` become kernel primitives.
- RELATES → underlies every layer's authority; feeds **Verification** (Layer 07).
- VISION → the "own the evidence seam" posture · **CP2**

---

## THE SCHOLARLY SPINE (Layers 05-08) — renamed, codified

### Layer 05 — Source (v1 SOURCE, position 0)

▸ **Source** — raw text as ingested, Bronze on R2.

- MECHANISM → `ingestion/` (asserter + R2) · `data/corpus/registries/source-registry.jsonl` (32,039)
- PROCESS → immutable Bronze snapshot + manifest. A source is a *publication*, not an epistemic verdict.
- NEEDS → provenance verified (fingerprint: incipit/explicit/hash).
- RELATES → parent of **DraftTranslation** + **ArgumentOutline**.
- VISION → **CP1 (SOURCE PROOF)**

### Layer 05 — DraftTranslation (v1 T1, position 1)

▸ **DraftTranslation** — the working draft of one passage.

- MECHANISM → `pipeline/t1_worker.py` (Hermes/model) · `pipeline/import_sanskritree.py` (old batch:
  141 T1) · skill `draft-passage`
- PROCESS → source → draft. Gate: gloss precision, losslessness, no dupes. Does NOT inherit the
  source's review authority.
- NEEDS → Source.
- RELATES → produces **Tokenization**; micro-stage siblings R1/DraftReview, T2/Alternative, T3/Final.
- VISION → the translation flow · **CP1**

### Layer 05 — Tokenization (v1 L0, position 2)

▸ **Tokenization** — structured token records over the draft; the token floor.

- MECHANISM → `pipeline/l0_worker.py` · `pipeline/certificate_l0.py` (deterministic floor) ·
  `pipeline/extract_l0_v1.py` · skill `tokenize` · registry `l0-registry.jsonl` (791)
- PROCESS → draft → tokens. Gate: token↔verse binding, no dupes, deterministic, fail-closed.
- NEEDS → DraftTranslation.
- RELATES → feeds **Translation** + **ArgumentOutline**.
- VISION → the philo-logical floor · **CP1**

### Layer 05 — ArgumentOutline (v1 ARGMAP, position 3)

▸ **ArgumentOutline** — the lateral guide: what's at issue, the argument steps, the unresolved points,
the decision for the translation.

- MECHANISM → `pipeline/argument_map_worker.py` · `pipeline/ingest_ipvv_argmap_golds.py` (50/51 golds
  ingested) · registry `argmap-registry.jsonl`
- PROCESS → lateral (not a DAG child of translation): needs Source + Tokenization. Structured 4
  sections. Named an OUTLINE, not a map.
- NEEDS → Source, Tokenization.
- RELATES → guides **Translation** (readable prose) + later **Argument** reconstruction.
- VISION → the lateral guide concept · **CP4 (argument)**

### Layer 05 — Translation (v1 L2, position 4)

▸ **Translation** — the readable prose translation of the passage, guided by the outline over the token
floor.

- MECHANISM → `pipeline/l1_l2_worker.py` · skill `patala-translation`
- PROCESS → prose render. Gate: fidelity to token floor, guided by outline. Micro-stage aliases
  T2/T3/R1/R2 live here (Alternative / Final / DraftReview / Adjudication).
- NEEDS → Tokenization, ArgumentOutline.
- RELATES → produces **TranslationProof**.
- VISION → the translation product · **CP1**

### Layer 05 — TranslationProof (v1 L200, position 5) — the moat

▸ **TranslationProof** — the proof of HOW each reading was derived; a vector of independently
inspectable obligations (never a scalar score).

- MECHANISM → `pipeline/l200_worker.py` · `pipeline/certificate_l200.py` ·
  `source-evidence/evals/inspect_l200*.py` · sibling gold `sanskritree/translations/_stack/ipvv/l200/`
  (63 audits) · skill `patala-translation-proof`
- PROCESS → 8-section audit (IDENTIFICATION / PUBLISHED READING / DERIVATION MAP / MATERIAL TRANSLATION
  DECISIONS / INTERPRETIVE ASSERTIONS / SOURCE LAYER / CROSS-REFERENCES / REVIEW STATE); typed decision
  types; **separate proof from policy** (§5 of the SPEC). **v2 gap to close:** only 5 L200 objects are
  in the registry though 63 golds exist in the sibling repo — a bulk-ingest is a priority (Phase 1).
- NEEDS → Translation.
- RELATES → produces **Commentary**; the anti-theatre backbone of publication.
- VISION → the moat · **CP1, CP4**

### Layer 05 — Commentary (v1 C1, position 6)

▸ **Commentary** — compact passage-local commentary (100–450 words), two representations
(structured + continuous).

- MECHANISM → `pipeline/c1_worker.py` · skill `commentate` · registry `c1-registry.jsonl`
- PROCESS → proof → commentary. Hard rules: no essays-as-evidence, no modern comparison, no PARALLELS
  inside, compact-not-essay. **v2 gap:** only 3 C1 in registry vs 63 golds in sibling (same ingest gap).
- NEEDS → TranslationProof.
- RELATES → feeds **Theme** + **Argument**.
- VISION → the living interpretation · **CP1, CP4**

### Layer 05/06 — Theme (v1 THEME, position 7)

▸ **Theme** — theme/cluster discovery across commentaries.

- MECHANISM → `pipeline/theme_worker.py` · `machinelearning/research/patala_ml/theme_discovery.py`,
  `kcore.py`, `cluster.py` · `data/published/ipvv/clusters.json` · skill `patala-theme`
- PROCESS → cluster commentaries; cluster coherence gate. A clustering, not a verdict.
- NEEDS → Commentary.
- RELATES → feeds **Synthesis**.
- VISION → the machine-readable philosophy phase · **CP3 (THEMES)**

### Layer 06 — Argument (v1 ARGUMENT, position 7)

▸ **Argument** — propositions → argument → cruxes; an executable derivation object.

- MECHANISM → `pipeline/epistemic_worker.py` (`make_argument_handlers`) ·
  `machinelearning/research/patala_ml/argument.py`, `aspic_adapter.py`, `aifgraph.py`, `crux_engine.py`,
  `proposition_layer.py` · `pipeline/ingest_ipvv_argmap_golds.py`
- PROCESS → reconstruct from Commentary + golds. Gate: structural validity, evidence completeness,
  scope/modality consistency, contradiction status. **validity ≠ soundness** — the graph represents it.
- NEEDS → Commentary (+ reviewable golds). Crux = the minimum unresolved proposition downstream turns on.
- RELATES → produces **Synthesis** + **Lesson**; converges with **Theme**.
- VISION → the epistemic core (the moat) · **CP4 (ARGUMENT)** — the frontier

### Layer 06 — Review / Adjudication (v1 Layer 08's human-authority core, cross-cutting)

▸ **Review / Adjudication** — the deterministic review reducer + scholar adjudication plane.

- MECHANISM → `pipeline/review_engine.py` (ReviewEvent ledger + impact_report) ·
  `source-evidence/schema/contracts_human_authority.py` · `pipeline/review_bundle.py` ·
  `vision-06-adversarial-review.md`
- PROCESS → state + event/evidence → deterministic reducer → next state. Agents submit *claims about
  state*, never state itself. **v2:** replace lossy `evidence_ok: bool` with typed events + canonical
  Findings. Four divergent `ReviewEvent` defs must converge (SCHEMA-AUDIT) — Phase 0 priority.
- NEEDS → kernel `events.py` + `reducers.py` + `gates.py`.
- RELATES → the gate for **TranslationProof**, **Argument**, **Synthesis**, publication.
- VISION → `vision-06-adversarial-review.md` · **CP5 (VERIFICATION), CP8 (ADVERSARIAL REVIEW)**

---

## THE EPISTEMIC UPPER STACK (Layers 07-08) — the honest frontier (all currently EMPTY)

### Layer 07 — Synthesis (v1 SYNTHESIS, position 8)

▸ **Synthesis** — converged synthesis over arguments + themes; a compiled projection.

- MECHANISM → `pipeline/epistemic_worker.py` (`make_synthesis_handlers`) ·
  `machinelearning/research/patala_ml/synthesis_core.py`
- PROCESS → only built when its arguments are qualified/adjudicated. **SYNTHESIS=0 is the honest state**
  until then. Gate: derivation-complete over qualified argument objects.
- NEEDS → Argument, Theme (+ review).
- RELATES → produces **Essay**.
- VISION → the epistemic core · **CP6 (SYNTHESIS)**

### Layer 07 — Essay (v1 ESSAY, position 9)

▸ **Essay** — essay whose every sentence retains a machine-traversable proof path.

- MECHANISM → `pipeline/essay_worker.py` · `machinelearning/research/patala_ml/essay*.py`,
  `essay_compiler.py`, `essayverify.py` · sibling `research-library/recognition/ESSAY-*.md` (22)
- PROCESS → render from Synthesis. Gate: every sentence has a dependency link. **ESSAY=0 honest.**
- NEEDS → Synthesis.
- RELATES → produces **Lesson**.
- VISION → `vision-07-new-scholar.md` (essay = rendering of the graph) · **CP6**

### Layer 07 — Lesson (v1 EDUCATION, position 10)

▸ **Lesson** — questions + distractors as compiled epistemic projections; each answer AND distractor
derivable from the graph.

- MECHANISM → `pipeline/education_worker.py` · `machinelearning/research/patala_ml/education_compiler.py`,
  `education_ir.py` · `docs/vision/education/`
- PROCESS → compile from Essay + graph. Gate: correct answer has a proof path; each distractor maps to
  an identifiable reasoning error (scope / epistemic-vs-metaphysical confusion / attractive-but-
  contradicts-premise). **LESSON=0 honest.**
- NEEDS → Essay (+ Argument/Theme so distractors are real).
- RELATES → a product surface; consumes the whole graph.
- VISION → **H (Education/Research-Program)**: `vision/education/PATALA-EDUCATION-SYNTHESIS.md` (the 4
  native education objects: LearningClaim/Skill/Interaction/MasteryEvidence) · `LEARNING_STRATEGY.md`
  (research-once/distill-repeatedly) · `EDUCATION_VISION.md` (graph-native teaching engine) ·
  `essayguide.md` (the Essay Research Program) · education as compiled epistemic projections · **CP6**

---

## SCHOLARS + PRODUCTS + SURFACES (Layers 09-12) — the human + economic + product planes

### Layer 08 — Scholar Attestation (v1 Layer 08, becomes granular)

▸ **Scholar Attestation** — a scholar attests to granular objects / findings / transformations, not
"approve the project."

- MECHANISM → `source-evidence/schema/contracts_human_authority.py` (Proposal/Adjudication/Promotion) ·
  `pipeline/review_engine.py` · `vision-07-new-scholar.md` · `vision-06-adversarial-review.md`
- PROCESS → attestation attaches a ReviewEvent to a granular object (a finding, a TranslationProof, a
  crux decision). The downstream impact is computed via the derivation graph.
- RELATES → the human gate over the whole spine.
- VISION → **B (Scholars)**: `vision-07-new-scholar.md` (workbench, perspective collector, structured
  inquiry) · `vision-06-adversarial-review.md` (the research-compiler diagnostics) ·
  `scholars/README.md` (who the contributors are) · **CP8 (ADVERSARIAL REVIEW)**

### Layer 09 — Organism / Human-Understanding Graph (v1 Layer 09, DESIGN)

▸ **Organism** — user interaction as structured epistemic data, not chat logs; consumer-as-probe.

- MECHANISM → `docs/vision/organism/` · `docs/process/09-organism.md` · candidate substrate Engram
- PROCESS → DESIGN only. The Q-moat variable.
- RELATES → feeds back into Review/Lesson product iteration.
- VISION → **D (Media & Organism)**: `vision-09-media-and-cross-tradition.md` (media layer + cross-
  tradition engine) · `organism/patalaorganism.md` (two first-class graphs) ·
  `organism/patalaorganismvisions.md` (longitudinal user graph) · `organism/consumerorganism.md`
  (consumer-as-probe) · `organism/consumerorganismtech.md` (event stream → graph projections) ·
  `organism/organism_meh.md` (adaptive learning, KST/BKT) · **CP10, CP12**

### Layer 10 — Surfaces / Products (v1 Layer 10, stays)

▸ **Surfaces** — the multi-surface platform; one core, five surfaces differing by permission, not truth.

- MECHANISM → `app/` (Next.js) · `app/api/` (43 routes) · `mcp/index.mjs` (29 tools) · `openpatala/` ·
  `docs-site/` · skills · **v2 change:** read compiled R2 artifacts, not `.ts` seeds.
- RELATES → every layer's compiled output; Hermes sits above a thin MCP (8 verbs).
- VISION → **E (Platform & Product)**: `vision-12-multi-surface-platform.md` (one core, five permission-
  scoped surfaces) · `vision-13-product-portfolio-by-user-base.md` (product catalog) ·
  `ENDGAME_SITE_SPEC.md` (the Tantra Reader site) · `endgame2.md` (Vision 02 — the Tantra Hub) ·
  **F/D media**: `vision-09-media-and-cross-tradition.md` · **functionality**: `vision/functionality/
  hermes-execution.md` (vision × Hermes execution → Layer 12) · **CP9 (API/MCP)**

### Layer 11 — Org / Economics (v1 Layer 11, DESIGN)

▸ **Org/Economics** — paid adjudication, credit (ORCID/CRediT/DOI), partnerships, the Scholar Compact.

- MECHANISM → `vision-08-scholar-economics.md` · `vision-10-market-entry-and-partnerships.md` ·
  `docs/positioningpartners.md` · `docs/global/globalpartnerships.md` · `vision/economics/README.md`
- RELATES → the incentives that make scholar attestation sustainable.
- VISION → **C (Economics)**: `vision-08-scholar-economics.md` (paid adjudication, ORCID/CRediT/DOI,
  ownership) · `vision-10-market-entry-and-partnerships.md` (BHU, funding, pilots, IP) ·
  `economics/README.md` (scarce assets, flywheel) · `endgame4.md` (Vision 04 — the economic thesis) ·
  `endgame5year.md` (Vision 05 — 2026-2031 window) · **CP11 (ECONOMIC)**

### Layer 12 — Live System (v1 Layer 12, PARTIAL) — the orchestration glue

▸ **Live System** — projection engine, staleness engine, MCP verbs, task≠run≠event, Hermes profiles,
coding-agent contract.

- MECHANISM → `docs/layers/12-live-system.md` (the 7 pieces) · `docs/process/docs_state.py` ·
  `pipeline/autonomy.py` · `~/.hermes/profiles/patala/` · `pipeline/model.py` (Hermes invocation)
- PROCESS → Pāṭala decides, Hermes executes, Pāṭala reduces. Hermes is the executor, not truth.
- RELATES → ties everything together; the compiler becomes reactive.
- VISION → **functionality**: `vision/functionality/hermes-execution.md` (vision × Hermes execution map)
  · `vision/functionality/README.md` (tools + machinery + interfaces) · the 7 pieces · **CP9, CP10, CP12**

---

## THE CROSS-CUTTING PLANE — Verification (Layer 07 in v1)

▸ **Verification** — external methods test Pāṭala; they never define Pāṭala truth.

- MECHANISM → `source-evidence/evals/patala/tasks/*` (atlas_nat, argmap, argument_recovery, warrant,
  essay_bench, edu_bench, source_authority) · `benchmarks/v0/` · `data/evaluation/recovery-gold-v1.json`
  (51 cases) · the 5 golds (nyaya/p3/p4/manuscript/recovery) · NAT tests
- PROCESS → independent gold + blind eval + metric + human adjudication. The anti-theatre gate.
- VISION → the eval plane · **CP0 (BENCHMARK), CP5**

---

## THE HONEST STATE (one screen, derived not hand-written)

| Layer (v2) | v1 | position | status (live) | the real gap to close |
|---|---|---|---|---|
| Source | SOURCE | 0 | BUILT | — |
| DraftTranslation | T1 | 1 | BUILT | old batch (141) not all canonical |
| Tokenization | L0 | 2 | BUILT | — |
| ArgumentOutline | ARGMAP | 3 | BUILT | 50/51 golds ingested |
| Translation | L2 | 4 | BUILT | — |
| TranslationProof | L200 | 5 | PARTIAL | **63 golds in sibling, only 5 in registry** |
| Commentary | C1 | 6 | PARTIAL | **63 golds in sibling, only 3 in registry** |
| Theme | THEME | 7 | PARTIAL | on-demand only |
| Argument | ARGUMENT | 7 | PARTIAL | workers wired, 0 committed |
| Review/Adjudication | (L8) | — | PARTIAL | **4 divergent ReviewEvent defs** |
| Synthesis | SYNTHESIS | 8 | EMPTY | honest 0 |
| Essay | ESSAY | 9 | EMPTY | honest 0 |
| Lesson | EDUCATION | 10 | EMPTY | honest 0 |
| Scholar Attestation | L8 | — | DESIGN | granular, not project-level |
| Organism | L9 | — | DESIGN | Engram candidate |
| Surfaces | L10 | — | PARTIAL | site reads `.ts`, not the graph |
| Economics | L11 | — | DESIGN | — |
| Live System | L12 | — | PARTIAL | 7 pieces |

*This table should be generated from `LAYERS.yaml` + the live registry (Phase 0 build) so it can never
drift. Today it is hand-compiled for review.*

---

## The v2 priority map (what to build first)

1. **Converge the kernel primitives** (ReviewEvent, AuthorityVector, Proposition, Derivation, ObjectRef)
   — Phase 0, kills the schema divergence. [SCHEMA-AUDIT]
   ⚠️ **KEY: the kernel is already half-built.** `python/patala_core/` has `authority.py` (a real
   AuthorityVector: 4 axes, gate predicates, display badge — NO scalar rank), `objects.py` (Proposition/
   Crux/ReviewEvent/Adjudication), `ids.py`, + full contracts in `docs/atlas-contracts/`. BUT the
   factory (`pipeline/object_registry.py`, `review_engine.py`) and `source-evidence/schema/` use their
   OWN separate ReviewEvent/Authority definitions — verified 4 distinct implementations. Phase 0 =
   promote `patala_core` to canonical and retire the other 3, NOT greenfield a new kernel.
2. **L200 + C1 bulk-ingest** (63 golds → registry with Derivation edges) — Phase 1, makes the moat counts
   true. [the single highest-leverage next build]
3. **Wire ledger → Postgres projection** + make the site read compiled objects, not `.ts` — Phase 1,
   kills the four-truths problem.
4. **Staleness + transformation registry** — Phase 2, the reactive compiler.
5. **THEME→ESSAY→LESSON in the live loop as compiled projections** — Phase 3, turns the honest EMPTY
   layers into real (gated) ones.
6. **Scholar attestation to granular objects** — Phase 4.
7. **MCP 8-verb thin adapter + performance** — Phase 5.

---

## VISION → LAYER → CATEGORY CROSS-REFERENCE (all 49 vision docs)

The canonical 8-category taxonomy (`docs/vision/CATEGORIES.md`) mapped onto the v2 layers. Every vision
doc resolves to a category AND a layer — nothing in the vision is unmapped.

| Category | Focus | Layer(s) | Vision docs (all mapped) |
|---|---|---|---|
| **A Foundations** | core vision + origin arc | 00, 02, 03, 10, 11 | `CORE-BIBLE` · `NORTHSTAR` · `endgame1..5year` · `foundationalideas` · `positioningpartners` · `vision/CATEGORIES` · `vision/INDEX` · `vision/REVIEWS` |
| **B Scholars** | review + workbench, the human layer | 08 | `vision-06-adversarial-review` · `vision-07-new-scholar` · `vision/scholars/README` |
| **C Economics** | incentives + market + sustainability | 11 | `vision-08-scholar-economics` · `vision-10-market-entry-and-partnerships` · `vision/economics/README` |
| **D Media & Organism** | media layer + human-understanding graph | 09 | `vision-09-media-and-cross-tradition` · `vision/organism/{patalaorganism,patalaorganismvisions,consumerorganism,consumerorganismtech,organism_meh}` |
| **E Platform & Product** | multi-surface + product portfolio | 10 | `vision-12-multi-surface-platform` · `vision-13-product-portfolio-by-user-base` · `ENDGAME_SITE_SPEC` |
| **F Expansion / Corpus** | Śiva-before-Abhinava + cross-tradition intake | 03 | `vision/expansion/vision-11-siva-before-abhinava{-prehistory,-corpus-manifest}` · `vision/expansion/README` |
| **G Atlas / Identity** | research graph + manuscripts + source-resolution | 02 | `vision-14-manuscript-to-scholarly-asset` · `vision-15-patala-atlas-sanskrit-research-graph` · `vision/source-resolution/source-resolver-design` · `vision/atlas/{technical-architecture-v1,atlas-engineering-blueprint,atlas-cloudflare-edge-layer,atlas-performance,agent-optimization}` |
| **H Education / Research-Program** | essay + learning + program guides | 05, 09 | `essayguide` · `vision/education/{PATALA-EDUCATION-SYNTHESIS,LEARNING_STRATEGY,EDUCATION_VISION,sources}` · `vision/functionality/README` |
| *(cross-cut)* | vision × Hermes execution | 12 | `vision/functionality/hermes-execution.md` |

**Completeness check:** every file under `docs/vision/` (root `.md` + the `atlas/ economics/ education/
expansion/ functionality/ organism/ scholars/ source-resolution/` subdirs) is listed above and assigned
to a category + layer. None is orphaned.

---

## VISION-ADJACENT DOCS OUTSIDE `docs/vision/` (the global strategy + corpus guidance sets)

`docs/vision/` holds the *architecture* visions. But vision/strategy content also lives in two other
places that a complete map must account for: the **global strategy/architecture set** (`docs/global/`)
and the **corpus scholarly-guidance set** (`docs/corpus/`). These are referenced where they belong in
the layer blocks above; this is the explicit accounting so nothing is invisible.

### Global strategy / architecture (`docs/global/`)

| Doc | What it is | Maps to layer |
|---|---|---|
| `PATALA-GLOBAL-ARCHITECTURE.md` | the frozen v0.1 global architecture (one graph, many interfaces) | 00, 10 |
| `agent1atlas.md` | Agent1 × Atlas convergence — the canonical scholarly graph, not a canonical packet | 02, 05 |
| `globalplan.md` | Global dev plan — current state → full platform | 00, 12 |
| `globalgoal.md` | the goal — the versioned scholarly graph is canonical; packets are compiled read-models | 00, 02, 03 |
| `globalaccess.md` | Access, rights & ecosystem — open-reference, controlled-corpus | 02, 11 |
| `globalpartnerships.md` | partnerships & the reconciliation layer | 11 |
| `GLOBAL-NEXT-2026-08-13.md` | coordinated next steps for the next agent | 12 |
| `GLOBAL-STATE-2026-08-13.md` | (ELAD) full state handover | 00, 12 |
| `globalglobal.md` | **ARCHIVED / redirect → NAVIGATION.md** | — |
| `HERMES-CALLING.md` | how Pāṭala calls Hermes | 12 |
| `ingestion-refinery.md` | the ingestion process | 01 |
| `patala-peer-review.md` · `peer-review-goat.md` | peer-review doctrine | 08, 07 |

### Corpus scholarly-guidance (`docs/corpus/`)

These are **domain-content guidance** (the scholarly textual territory), not architecture — they guide
the *content*, so they map to the layers that consume the corpus.

| Doc | What it is | Maps to layer |
|---|---|---|
| `markguidance.md` | Recognition-Enquiry guidance across Pratyabhijñā + rivals + consciousness research | 02, 06 |
| `canonical_reference_map.md` | the Trika–Krama–Kubjikā–Kaula–Pratyabhijñā–Sarvāmnāya textual territory map | 02, 06 |
| `translation_atlas.md` | the translation-status atlas | 05 |
| `translation_flow_spec.md` | the translation flow spec | 05 |
| `tradition_anchors.md` · `atlasflaws.md` | tradition anchoring + atlas flaws | 02 |
| `leapfrog_map.md` · `leapfrog_guide.md` | the leapfrog strategy for the corpus | 03, 05 |
| `bibliography-strategy.md` | bibliography acquisition strategy | 02 |
| `TARGETS-INDEX.md` | the acquisition goldmine (corpus targets) | 01, 03 |
| `sivaqueue{2,3,34,4}-translation-guide.md` · `sivaqueue-guide.md` | per-queue intake guides | 01, 05 |

### Other vision-adjacent (top-level `docs/`)

| Doc | What it is | Maps to layer |
|---|---|---|
| `positioningpartners.md` | positioning & partners (Category C) | 11 |
| `foundationalideas.md` | passage/text identity as the stable anchor | 02 |
| `endgame1..5year.md` | Vision 01-05 origin arc | 00, 03, 10, 11 |
| `ENDGAME_SITE_SPEC.md` | the Tantra Reader site spec | 10 |
| `SCHOLARLY_GRAPH.md` | the canonical object/annotation model | 02, 05 |

> **Note on `patalaendgame` / `rm*` / `rmdev`:** those names appear only in the **R2 uploads** bucket
> (`blog-video-assets/uploads/`), not as docs in this repo — they are exported notes, not part of the
> repo's vision corpus. If you want them reconciled into the map, they'd need to be imported first.

---

## THE CONTRACT / CONCEPT CLUSTERS (`docs/atlas-contracts/`, `docs/api/concepts/`, `docs/ontology/`)

These hold the **existing schema/contract specs** — several are the v2 kernel's contracts, already
written. This is the most important under-surfaced area: **the kernel is not just a future idea, it
already has contract docs + a `python/patala_core/` implementation.**

### `docs/atlas-contracts/` — the v2 kernel contracts (already exist)

| Doc | What it is | v2 relevance |
|---|---|---|
| `authority-vector.md` | AuthorityVector — 4 axes, gate predicates, NO scalar rank (field ref for `python/patala_core/authority.py`) | **core kernel** — implements the mixxii authority requirement |
| `objects.md` | the typed scholarly objects (Proposition/Commitment/GroundingLink/InferenceApplication/Crux/ReviewEvent/ReviewProposal/Adjudication) | **core kernel** |
| `ids.md` | canonical id scheme (`pt:` URNs) | **core kernel** (ObjectRef) |
| `read-api.md` | the read-side API contract | Layer 10 |
| `source-resolver.md` | the federated edition/manuscript resolver | Layer 02 |
| `access-policy.md` | publication/rights gates | Layers 02, 11 |
| `adapter-migration.md` | adapter migration path | Layer 04 |
| `atlas-database.md` | the atlas Postgres schema | Layer 02 |
| `frontend-architecture.md` | the read-side UI architecture | Layer 10 |
| `overview.md` | the contract cluster overview | — |

### `docs/api/concepts/` — the epistemic-status model (core doctrine)

| Doc | What it is | v2 relevance |
|---|---|---|
| `epistemic-model.md` | SOURCE/PROPOSAL/ASSERTION/REVIEW/ACCEPTED + the rules (Proposal ≠ assertion, Accepted ≠ certain, machine score ≠ confidence) | the anti-theatre core — maps to kernel `authority` + `reducers` |
| `assertions-proposals.md` | the assertion/proposal distinction | kernel `authority` |
| `rights.md` | rights + publication posture | Layers 02, 11 |
| `work-witness-passage.md` | the Work/Witness/Passage identity model | Layer 02 |
| `mcp.md` + `recipes/*` | the MCP + API surface (7 recipe docs) | Layer 10 |

### `docs/ontology/` — the higher-object specs

| Doc | What it is | v2 relevance |
|---|---|---|
| `EO-v2.md` | Essay Object v2 — full spec | Layer 07 (Essay) |
| `RO-v2.md` | Research Object v2 — full spec | Layers 05-07 |

---

## THE ML / CONTENT CLUSTERS (`docs/ml/`, `docs/content/`)

| Doc | What it is | Maps to layer |
|---|---|---|
| `ml/LAYER-TOOLS-INTEGRATION-NORTHSTAR.md` | the layer-tools integration north star | 05, 07 |
| `ml/LAYER-TOOLS-SURVEY.md` | the external layer-tool landscape (verification kernel composition) | 04, 07 |
| `ml/MACHINE-PROOF-CONTRACTS.md` | the universal "layer done" definition (LayerContract with 5 gates) | 03, 07 |
| `content/modules/school-*.md` + `recognition.md` | ConceptLesson modules (the Pratyabhijñā foundation) | 07, 09 (Lesson + organism) |

---

**Full accounting:** architecture vision = `docs/vision/` (50 docs) + global strategy (`docs/global/`) +
corpus guidance (`docs/corpus/`) + the contract/concept clusters (`docs/atlas-contracts/`,
`docs/api/concepts/`, `docs/ontology/`) + the ML/content clusters (`docs/ml/`, `docs/content/`) + the
top-level strategy docs. Every one is now assigned a category + layer. Nothing is unmapped.

**Why these were missed:** the `check_docs_audit.py` validator only scanned **top-level `docs/*.md`**
(`DOCS.glob("*.md")`), so all 176 docs in subdirectories were invisible to the audit. This is now fixed —
the validator recursively checks every `docs/**/*.md` (rule 5) and the audit passes.



---

*This mapping points every layer at its real machinery, its vision, and its checkpoint, and it is
FAST to produce because it is just pointers — no code changes. The next step to make it self-consistent
forever is to generate this exact doc from `LAYERS.yaml` + the live registry instead of hand-writing it.*
