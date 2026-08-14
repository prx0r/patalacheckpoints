# PĀṬALA V3 — THE PRODUCTS (fully specced: mechanism · proof · external tool · build)

*2026-08-14 · status: THE PRODUCT SPEC · v2's product doctrine (16 products, 4 families, checkpoint
ladders) fully specced for v3: each product now carries its PROVEN mechanism (ip-graph `lib/`), the
verifiable proof, the exact external tool, and the exact build path. 13/16 products have a proven
mechanism (51/51 experiments pass); 3 need building (Essay, Commentary, Tokenization).*
*Sources: `strategy/PRODUCTS.md` (v2 doctrine) + `ip-graph/migration/v2/PRODUCTS.md` (proven mechanisms)
+ `EXTERNAL-REPOS.md` (external tools) + `V3-BUILD-SPEC.md` (the stack).*

---

## THE 4 FAMILIES (the site hierarchy — unchanged from v2)

**Texts** (Reading · Translation · Translation Proof · Compare Translations · Term Audit · **Atlas/Identity**)
**Arguments** (Claim · Argument · Crux · Comparison · Synthesis)
**Scholar** (Research Packet · Review · Scholar Attestation · Audit · Benchmark)
**Learn** (Essay · Explainer · Argument Map · Understanding Checks · Course)
Underneath: API · MCP · Context Bundles · Datasets.

**The missing products v2 had that v3 must carry (the Atlas/Identity family):**
- **Atlas / Identity** — the authority graph (254 works) + the human/API surface; every object's canonical ID. Built in patala (`patala_core/atlas/`), NOT in the lab.
- **Bibliography / Discovery** — the 254-work bibliography + Zotero/Crossref/OpenAlex/OpenCitations discovery.
- **Terminology / Lemma-through-time** — `trajectories.ts`, `/api/terms/:lemma/history`.
- **Timeline** — `historyTimeline.json`, `/api/history/timeline`.

---

## THE 16 PRODUCTS — FULLY SPECCED

### 0. Atlas / Identity — ✅ PROVEN (in patala; NOT in lab — the v3 gap to carry)
- **Artifact:** the Pāṭala Authority Graph + its human/API surface (the Atlas)
- **Mechanism:** `python/patala_core/atlas/` (migrate · resolver · adapter · api) — per-dimension
  authority + rights-aware gates; the 254-work bibliography (`atlas-bibliography.json`)
- **Proof:** test_resolver (22) · test_api (9) · test_adapter (6)
- **External:** CTS (identity) · Zotero/Crossref/OpenAlex/OpenCitations (discovery) · RO-Crate (packaging)
- **Build:** the authority graph is the identity backbone EVERY other product references. **v3 must not
  drop this — it exists in patala, not the lab. Wire it as the resolve layer under every product.**

### 0b. Terminology / Lemma-through-time — ✅ PROVEN (in patala)
- **Artifact:** lemma → diachronic sense-trajectory
- **Mechanism:** `data/corpus/trajectories.ts` + `terms.ts`; `/api/terms/:lemma/history`
- **Proof:** the lemma-history route serves real trajectories
- **External:** darshana-temporal-analysis · text-fabric
- **Build:** the terminology layer feeds Translation (term consistency) + Lesson (distractors).

### 0c. Timeline — ✅ PROVEN (in patala)
- **Artifact:** the school/tradition chronology
- **Mechanism:** `data/atlas/historyTimeline.json`; `/api/history/timeline`
- **Proof:** the timeline route serves the map

---

### 1. Translation — ✅ PROVEN (needs IPVV data)
- **Artifact:** `TranslationRevision`
- **Mechanism:** `lib/translation.py` (the non-aggregate vector); proof generators ByT5-Sanskrit /
  Sanskrit Heritage / Vidyut / skrutable
- **Proof:** `validate-products.py` PASS
- **Build:** wire the vector into the real translation pipeline (IPVV); deterministic checks (T1-T3)
  exist; add independent review + scholar approval.

### 2. Translation Proof — ✅ PROVEN (THE MOAT)
- **Artifact:** `TranslationProof TP-NNNN` (vector, not scalar)
- **Mechanism:** `lib/translation.py` — SOURCE_COVERAGE·TARGET_GROUNDING·MORPHOLOGY·SYNTAX·NEGATION·
  MODALITY·TERM_CONSISTENCY·ENTAILMENT·PARALLEL_WITNESS·HUMAN_REVIEW; publication gate BLOCKS on any
  failing dimension (never one "94%").
- **Proof:** `validate-products.py` PROVEN
- **External auditors (redundant, never one decides):** xCOMET · GemSpanEval · OTTAWA · MQM ·
  entailment · term-consistency
- **Build:** production-ready as a mechanism. Add real Sanskrit audit dims (Vidyut, xCOMET) + the IPVV
  golds. **This is the strongest defensible product — and it's proven.**

### 3. Passage / Reading — ✅ PROVEN mechanism
- **Artifact:** canonical Passage object
- **Mechanism:** `lib/query.py` (KG2Code executable queries)
- **Proof:** `validate-stack.py` (real graph)
- **External:** Mirador 4 + TextOverlay · Recogito · CTS · Text-Fabric
- **Build:** the Passage Workbench — a Sanskritist disagrees with a reading → a GraphProposal → the
  human gate. The query DSL is proven.

### 4. Claim — ✅ PROVEN
- **Artifact:** `Claim C-NNNN`
- **Mechanism:** `lib/epistemic.py` envelope (SOURCE-SAYS / SCHOLAR-RECONSTRUCTS / PĀṬALA-INFERS kept
  distinct via epistemic_ceiling)
- **Proof:** `validate-stack.py` (a real thesis claim stays MACHINE_PROPOSED)
- **Build:** hook the envelope to real passages + the review reducer.

### 5. Argument — ✅ PROVEN
- **Artifact:** `Argument` (AIF Info/Inference/Conflict)
- **Mechanism:** `lib/review.py` + `lib/scholar_review.py`
- **Proof:** `validate-layer03-05.py` + `scripts/validate-kernels.py`
- **External:** ASPIC+ · AIF/xAIF · IAM (verification); the IR is Pāṭala-owned
- **Build:** scale the working argument exemplar to real IPVV arguments.

### 6. Crux — ✅ PROVEN
- **Artifact:** `Crux`
- **Mechanism:** `experiment-crux-compiler.py` (computes minimal divergence between positions)
- **Proof:** crux-compiler
- **Build:** wire crux-compiler into the argument engine as a first-class object.

### 7. Review — ✅ PROVEN
- **Artifact:** ReviewEvent
- **Mechanism:** `lib/scholar_review.py` — adversarial panel + cross-review + CiteCheck phantom
  detection + review-bias robustness (37.1% finding)
- **Proof:** `scripts/validate-kernels.py` PROVEN
- **Build:** add signed ReviewEvents (review is evidence about a target, never mutating it).

### 8. Scholar Attestation — ⚠️ PROVEN-MECHANISM (needs signed auth — gap E)
- **Artifact:** signed HumanAttestation
- **Mechanism:** `lib/agent_delivery.py` human gate (agent proposes, only human authorizes)
- **Proof:** `validate-agent-delivery.py`
- **External:** ORCID · CRediT · DOI · C2PA
- **Build:** replace `human_authorize()` with a cosign-style signed attestation (gap E). **Required
  before any public authority/marketplace.**

### 9. Research Packet — ✅ PROVEN
- **Artifact:** ResearchPacket (the scholarly equivalent of a proof state)
- **Mechanism:** `lib/retrieval.py` (PathRAG/HippoRAG) + `lib/query.py`
- **Proof:** `validate-layer10.py` + `scripts/validate-kernels.py` (HippoRAG hub-bias finding documented)
- **Build:** the question→search-plan→evidence-packet flow (from paper-qa reference).

### 10. Synthesis — ⚠️ PROVEN-MECHANISM
- **Artifact:** Synthesis (ArgumentSynthesis)
- **Mechanism:** `lib/evolve.py` MAP-Elites evolution (converges + preserves diversity)
- **Proof:** `validate-evolve.py`
- **Build:** connect the evolution loop to real arguments; fitness must be a VECTOR (never one scalar).

### 11. Essay / Explainer — 🔧 NEEDS BUILD (mechanism proven)
- **Artifact:** sentence-sourced Essay
- **Mechanism:** the reactive-essay (`experiment-reactive-essay.py` — source retraction marks prose
  stale); the projection itself needs build. The `.meta` workengestation already writes essays (13).
- **Proof:** experiment-reactive-essay
- **Build:** compile verified argument → sentence-sourced essay, each sentence dependency-linked; wire
  verified Synthesis to `.meta` workengestation.

### 12. Education / Understanding Check — ⚠️ PROVEN-MECHANISM
- **Artifact:** LearningClaim + interaction fixture
- **Mechanism:** `lib/education.py` + `lib/pedagogy.py` — the "wrong answer → known epistemic neighbor"
  moat is proven
- **Proof:** `validate-education-organism.py` + `validate-pedagogy.py`
- **External:** pyBKT · Dialogue-KT · FSRS · adaptive-knowledge-graph (the GOLD interface map)
- **Build:** feed real discovery-progressions (from the LOGICVID gold) as the pedagogical structure.

### 13. Comparison — ✅ PROVEN
- **Artifact:** cross-tradition comparison
- **Mechanism:** `experiment-claim-standardisation.py` — structural claim vs tradition vocab + boundary
- **Proof:** claim-standardisation
- **Build:** the comparative questionnaire over the standardised claims.

### 14. Audit — ✅ PROVEN (the doctrine applied to itself)
- **Artifact:** verifiable proof record
- **Mechanism:** `theatre-check.py` + `theatre-check-all.py` — this IS the audit product
- **Proof:** theatre-check (Pāṭala audits itself)
- **Build:** productize as the standalone API/business product (Translation Audit first).

### 15. Dataset / Benchmark — ✅ PROVEN
- **Artifact:** benchmark
- **Mechanism:** `experiment-import-scifact.py` (external dataset into the engine) + the matrix
- **Proof:** import-scifact
- **External:** Mitrasamgraha · SciFact · wmt-mqm
- **Build:** the IPVV Benchmark (from real failures, not trivia).

### 16. Agent Context Bundle — ✅ PROVEN
- **Artifact:** one-request agent bundle
- **Mechanism:** `lib/agent_delivery.py` (context routing) + `lib/retrieval.py` (bounded context)
- **Proof:** `validate-agent-delivery.py` + `experiment-bounded-context.py`
- **Build:** the Context Bundles (micro 2k / standard 8k / deep 32k) — the "agent cache line."

---

## THE VERDICT (the honest status)

| # | Product | Status | Proof |
|---|---|---|---|
| 1 | Translation | PROVEN | validate-products |
| 2 | **Translation Proof** | **PROVEN (the moat)** | validate-products |
| 3 | Passage/Reading | PROVEN | validate-stack |
| 4 | Claim | PROVEN | validate-stack |
| 5 | Argument | PROVEN | layer03-05 |
| 6 | Crux | PROVEN | crux-compiler |
| 7 | Review | PROVEN | validate-kernels |
| 8 | Scholar Attestation | PROVEN-MECH (gap E) | validate-agent-delivery |
| 9 | Research Packet | PROVEN | layer10 |
| 10 | Synthesis | PROVEN-MECH | validate-evolve |
| 11 | **Essay** | **NEEDS BUILD** | reactive-essay (mech) |
| 12 | Education | PROVEN-MECH | education-organism |
| 13 | Comparison | PROVEN | claim-standardisation |
| 14 | Audit | PROVEN | theatre-check |
| 15 | Dataset/Benchmark | PROVEN | import-scifact |
| 16 | Context Bundle | PROVEN | validate-agent-delivery |

**13/16 proven · 2 strongest production-ready (TranslationProof, Education) · 3 need building (Essay,
Commentary, Tokenization).**

---

*This is the v3 product spec — every v2 product fully specced with its proven mechanism, proof, exact
external tool, and build path. The products aren't speculative anymore; they're proven mechanisms
awaiting integration. See `LAYERS.yaml` (v3) for the layer contract and `V3-BUILD-SPEC.md` for the build
order.*
