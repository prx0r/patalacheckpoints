# PĀṬALA — THE PRODUCTS ↔ VISIONS MAP (implemented vs visionary · use case · why · how they link)

*2026-08-14 · status: THE PRODUCT-VISION MAP · companion to `strategy/PRODUCTS.md` (the 16-product
catalog) + `GOATED-TO-VISION.md` + `LAYER-MAPPING.md`. For EVERY product: what is IMPLEMENTED today
(verified) vs what is VISIONARY, the exact USE CASE, WHY it exists, and HOW it links to the vision docs
it emerges from. This answers: **do products emerge from visions, or the other way around — and how do
we get there.***
*All "implemented" claims verified against the actual routes, MCP tools, and published data on
2026-08-14.*

---

## THE KEY QUESTION FIRST: do products emerge from visions, or visions from products?

**The honest answer: it's a loop, but the *grounding* is bottom-up.** The vision docs (endgame,
vision-06/07/08...) describe where Pāṭala is going; but a product is only REAL when it's implemented and
a user can touch it. So:

```text
VISION (where we're going) ──► PRODUCT CONCEPT (a use case) ──► IMPLEMENTATION (real + tested)
                                                                      │
                                                              (a user can use it)
                                                                      │
                                                              a product EMERGES
                                                                      │
                                                              (grounds the vision — it's now true)
```

**The rule that decides "implemented vs visionary":** a product is IMPLEMENTED only when a user can
actually get its value today (a route serves it, a tool exposes it, data carries it). Otherwise it is
VISIONARY — a real use case with a clear why, but not yet built. Pāṭala's anti-theatre doctrine demands
we never call a visionary product implemented.

**The link direction:** the VISION states the use case (why it should exist); the IMPLEMENTATION makes
it real; the product then *grounds* the vision (turns a doc's claim into observable fact). You need both
— but you can only call it a product once it's implemented.

---

## THE IMPLEMENTED SURFACE TODAY (what a user can actually touch — verified)

| Surface | Implemented | Evidence (verified) |
|---|---|---|
| **Reading / Translation** | ✅ | `app/read/[work]/[locator]`, `texts/*` pages; `/api/passages/:id/translation` |
| **Passage / Lemma data** | ✅ | `data/corpus/terms.ts`, `trajectories.ts`; `/api/terms/:lemma/history` (lemma-through-time) |
| **Timeline** | ✅ | `/api/history/timeline` → `historyTimeline.json` |
| **Search / Resolve** | ✅ | `/api/search`, `/api/resolve`, `get_source_passage`, `resolve_ref` (MCP) |
| **Review / Impact** | ✅ | `patala_get_review_state`/`propose_review`/`submit_review`/`get_impact`/`simulate_review` (MCP) |
| **Essay** | ✅ | `data/published/ipvv/essay-cl3.json` (11 claims, 11 sentences, **11/11 verified**) |
| **Clusters / Themes** | ✅ | `data/published/ipvv/clusters.json` (9 clusters) |
| **Factory status / cert** | ✅ | `patala_get_factory_status`, `patala_get_certificate` (MCP) |
| **Verify / Trace** | ✅ | `verify_quote`, `verify_claim_structure`, `trace_dependency`, `find_counterevidence` (MCP) |

**The IMPLEMENTED core:** reading, passage/lemma data, search/resolve, review/impact, essay, clusters,
factory status, verification — all live and touchable. This is the real product surface today.

---

## THE 16 PRODUCTS — IMPLEMENTED vs VISIONARY, use case, why, vision link

For each: **IMPLEMENTED?** (verified) · **USE CASE** (exactly who uses it, for what) · **WHY** (the
reason it exists) · **VISION** (the doc(s) it emerges from).

### 1. Reading / Translation — ✅ IMPLEMENTED
- **Use case:** a learner/reader opens a passage and reads a clean translation with notes.
- **Why:** the simplest product — what normal readers actually consume.
- **Vision:** `endgame1` (translation laboratory), `vision-02` (Tantra Hub reader).
- **Implemented via:** `app/read`, `texts/*`, `/api/passages/:id/translation`, `data/published/ipvv/*`.

### 2. TranslationProof — ⚠️ VISIONARY (machinery + gold exist, not yet a product)
- **Use case:** a scholar sees a non-aggregate proof vector per translation (coverage/morphology/negation/
  etc. PASS/WARN), not a "94% score."
- **Why:** the flagship + the moat — the thing that makes the translation defensible.
- **Vision:** `docs/process/INDUSTRY-ALIGNMENT.md` (TranslationProof novel) + `PATALA-V2-SPEC.md` §5.
- **Status:** `l200_worker.py` + 63 golds exist; registry has only 5. **Not yet a user-facing product.**
  → *this is THE gap.*

### 3. Passage / Reading workbench — ⚠️ PARTIAL
- **Use case:** a Sanskritist disagrees with a sandhi resolution or reading, and can record it.
- **Why:** the philology-facing primitive underneath everything.
- **Vision:** `vision-15` (atlas), `vision-14` (manuscript→scholarly asset).
- **Implemented:** passage data + terms exist; the *disagreement/editing* workbench is not built.

### 4. Claim — ⚠️ PARTIAL (data exists, product doesn't)
- **Use case:** "Abhinavagupta treats recognition as re-identification" as a reviewable object with
  SOURCE-SAYS / SCHOLAR-RECONSTRUCTS / PĀṬALA-INFERS kept distinct.
- **Why:** the first serious scholarly abstraction.
- **Vision:** `vision-06` (adversarial review), `docs/api/concepts/epistemic-model.md`.
- **Implemented:** propositions exist in the research engines; not a user-facing claim product.

### 5. Argument — ⚠️ VISIONARY (engines real, product not)
- **Use case:** a citable Argument Proof (premises/inference/conclusion/validity/soundness).
- **Why:** a major product; the reasoning discipline made visible.
- **Vision:** `vision-06`, `ARGUMENT-IR-VISION` (the CP4 target).
- **Status:** `argument.py`, `crux_engine`, `aspic_adapter`, `aifgraph`, `nyayagate` all exist;
  ARGUMENT=10 objects. The product (a scholar-citable proof) is not built.

### 6. Crux — ⚠️ VISIONARY (engine exists)
- **Use case:** "the smallest unresolved proposition whose resolution changes the debate" — a
  scholar-acquisition mechanism ("Open Crux").
- **Why:** vastly more useful than a literature review; where research concentrates.
- **Vision:** `vision-06`, `crux_engine.py`.
- **Status:** `crux_engine.py` exists; not a product.

### 7. Review — ✅ IMPLEMENTED (the reducer)
- **Use case:** a publishable Review object (target/reviewer/findings/severity/disposition) + a visible
  correction history.
- **Why:** review is the gate everything upper depends on; correction history = the trust surface.
- **Vision:** `vision-06` (adversarial review), `vision-07` (new scholar).
- **Implemented via:** `review_engine.py`, MCP `patala_get_review_state`/`propose_review`/`submit_review`.

### 8. Scholar Attestation — ⚠️ VISIONARY (contract exists)
- **Use case:** a scholar attests to a *precise* object ("reviewed verses 1.5.1-1.5.15 for semantic
  fidelity, ACCEPT WITH QUALIFICATIONS"), building the expert verification network.
- **Why:** the highest-moat product after Proof; makes scholar work durable + credited.
- **Vision:** `vision-07`, `vision-08` (ORCID/CRediT/DOI).
- **Status:** `contracts_human_authority.py` exists; the signed-attestation product is not built.

### 9. Research Packet — ⚠️ VISIONARY (first monetizable)
- **Use case:** a question → compiled claims/sources/quotations/disagreement-map/cruxes/bibliography.
- **Why:** stops scholars searching twenty systems; first monetizable scholar product.
- **Vision:** `vision-07`, `endgame3`.
- **Status:** the engines (`retrieval.py`, `pushing.py`) exist; the packet product is not built.

### 10. Synthesis — ⚠️ VISIONARY (engine exists, EMPTY)
- **Use case:** established / probable / disputed / unknown — the "state of the question."
- **Why:** convergence over reviewed claims + arguments + cruxes.
- **Vision:** `vision-06`; `synthesis_core.py`.
- **Status:** `synthesis_core.py` exists; SYNTHESIS=0 (honest — inputs not yet there).

### 11. Essay / Explainer — ✅ PARTIAL (one real essay)
- **Use case:** a projection of the graph where every sentence answers "why does Pāṭala say this."
- **Why:** the public/education layer; essay = a rendering of the graph.
- **Vision:** `vision-07`, `essayguide.md`.
- **Implemented:** `data/published/ipvv/essay-cl3.json` (11 claims, 11 sentences, **11/11 verified**) —
  the first real essay product. Format variety (video/lecture/FAQ) is visionary.

### 12. Education / Understanding Check — ⚠️ VISIONARY
- **Use case:** questions where a correct answer demonstrates the distinction; each distractor maps to a
  reasoning error.
- **Why:** one of the most distinctive products; "understanding as proof."
- **Vision:** `vision-education/*`, `PATALA-EDUCATION-SYNTHESIS.md`.
- **Status:** `education_compiler.py` + `education_ir.py` exist; LESSON=0; no product.

### 13. Comparison — ⚠️ VISIONARY (prior experiment RETIRED)
- **Use case:** structured disagreement (AGREEMENT/DISAGREEMENT/REAL CRUX) between translations/scholars/
  texts.
- **Why:** a really strong focused module; cross-tradition engine.
- **Vision:** `vision-09` (cross-tradition), `7-FOLD-COMPARATIVE-MODEL`.
- **Status:** `argument_comparison.json` exists but is **RETIRED** — "INVALID_EXPERIMENT / CIRCULAR_METRIC:
  B-STRUCT premises are C1 titles; gt_overlap measured passage-title overlap not reasoning." The real
  comparison product is NOT built. This is an honest prior failure to learn from.

### 14. Audit — ⚠️ VISIONARY (but the first-product doctrine says build it FIRST)
- **Use case:** input = someone's artifact → Findings[] (severity/evidence/correction/confidence).
- **Why:** the easiest standalone business product; creates structured correction data.
- **Vision:** `FIRST_PRODUCT_DECISION.md` (Translation Audit as the FIRST product).
- **Status:** the eval plane exists (verify_* MCP tools); the Audit product is not built.

### 15. Dataset / Benchmark — ⚠️ PARTIAL (golds exist)
- **Use case:** benchmarks derived from real failures (Translation, Negation, Argument Reconstruction...).
- **Why:** research credibility + infrastructure value.
- **Vision:** `FIRST_PRODUCT_DECISION.md` (IPVV Benchmark as the FIRST strategic asset).
- **Implemented:** the 5 golds + eval plane exist; a public benchmark product is not released.

### 16. Agent Context Bundle — ⚠️ VISIONARY
- **Use case:** `context(ARG-32, budget=8000)` → a token-budgeted packet (object/premises/evidence/
  cruxes/authority). The machine-facing product.
- **Why:** makes Pāṭala infrastructure for external agents.
- **Vision:** `PATALA-V2-SPEC.md` §10-11 (agent cache lines).
- **Status:** not built; the MCP (29 tools) is the current agent surface.

---

## HOW THE PRODUCTS LINK TOGETHER (the dependency web)

```text
        IMPLEMENTED CORE (today)
   Reading · Passage/Lemma · Search/Resolve · Review/Impact · Essay · Clusters · Verify
                    │
        (everything above is built; below needs it)
                    ▼
   THE MOAT LAYER (needs the proof)
   TranslationProof ◄──── the biggest gap (63 golds exist, not a product)
                    │
   THE UPPER STACK (needs the moat + arguments)
   Argument → Synthesis → Education → Comparison
                    │
   THE SCHOLAR / BUSINESS LAYER (needs the above)
   Research Packet · Scholar Attestation · Audit · Benchmark
                    │
   THE AGENT LAYER
   Context Bundle (needs everything, as token-budgeted packets)
```

**The linking principle:** every visionary product is a **projection of the layer below it**. You can't
build a real Comparison or Education product until the Arguments and Proofs they compare/teach exist.
That's why the implemented core (Reading→Review→Essay) is first, and the upper products follow.

---

## THE VISION ↔ PRODUCT LINK TABLE (which vision each product emerges from)

| Product | Emerges from vision(s) | Implemented? |
|---|---|---|
| Reading | endgame1, vision-02 | ✅ |
| TranslationProof | INDUSTRY-ALIGNMENT, SPEC §5 | ⚠️ gap |
| Passage workbench | vision-15, vision-14 | ⚠️ partial |
| Claim | vision-06, epistemic-model | ⚠️ partial |
| Argument | vision-06, ARGUMENT-IR-VISION | ⚠️ engines only |
| Crux | vision-06 | ⚠️ engine only |
| Review | vision-06, vision-07 | ✅ |
| Scholar Attestation | vision-07, vision-08 | ⚠️ contract only |
| Research Packet | vision-07, endgame3 | ⚠️ visionary |
| Synthesis | vision-06 | ⚠️ EMPTY |
| Essay | vision-07, essayguide | ✅ (1 real) |
| Education | education visions | ⚠️ EMPTY |
| Comparison | vision-09, comparative models | ⚠️ retired prior |
| Audit | FIRST_PRODUCT_DECISION | ⚠️ visionary (priority) |
| Benchmark | FIRST_PRODUCT_DECISION | ⚠️ partial (golds) |
| Context Bundle | SPEC §10-11 | ⚠️ visionary |

---

## THE HONEST SNAPSHOT (what's real vs promised)

**Implemented (a user can touch it today):** Reading · Passage/Lemma data · Search/Resolve · Timeline ·
Review/Impact · Essay (1 real) · Clusters · Factory status · Verification.

**Built machinery, not yet a product (the "almost" list):** TranslationProof (63 golds, 5 registered) ·
Argument (engines + 10 objects) · Crux (engine) · Synthesis (engine, 0 objects) · Essay (engine) ·
Education (engines) · Golds/benchmark.

**Purely visionary (use case defined, nothing user-facing):** Research Packet · Scholar Attestation ·
Comparison (prior attempt retired) · Audit · Context Bundle.

---

## THE HONEST BUILD DIRECTION (how products emerge from here)

The products are already emerging — they follow the implemented core. The direction:

1. **Reading → TranslationProof** (make the 63 golds a real product) — closes the moat gap, the biggest
   single step.
2. **Review → Scholar Attestation** (the signed, credited attestation) — the scholar layer becomes real.
3. **Essay → Education** (the 11-verified-essay as the seed of Understanding Checks) — content emerges
   from what's already proven.
4. **Verification → Audit** (the verify_* tools become the Audit product) — the first-business-product
   doctrine.
5. **The whole implemented core → Context Bundle** (packetize what already exists for agents).

**The through-line:** products emerge from what's IMPLEMENTED, not from the visions. The visions state
the use case and the why; the implementation makes it real; and each product once built grounds the
vision that named it. Start from the implemented core, extend it product by product, and let each new
product be a projection of what's already real — that's how "we get there."

---

*This is the products↔visions map. The key honest finding: **the implemented core is Reading→Review→Essay;
the moat (TranslationProof) is the single biggest gap; and every upper product (Education, Comparison,
Research Packet, Attestation, Audit, Context Bundle) is a projection of what must be built below it.** The
vision names the use case; the implementation makes it real; the product grounds the vision.*
