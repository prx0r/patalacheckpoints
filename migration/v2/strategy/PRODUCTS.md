# PĀṬALA — THE PRODUCTS (the canonical user-facing product doctrine)

*2026-08-14 · status: FORMALIZED · source: R2 `blog-video-assets/uploads/patalaproducts` (imported),
formalized against the v2 layers, the existing vision docs, and the reusable module inventory.*
*This is the **external product surface** — deliberately SMALLER and more productized than the internal
architecture. Internally there can be dozens of object types; externally, users see a handful of focused
scholarly products, each with a clear artifact, proof object, checkpoint, and use case.*

---

## THE 16 PRODUCTS (the clean canonical list)

```text
 1. Translation           7. Review                13. Comparison
 2. Translation Proof     8. Scholar Attestation   14. Audit
 3. Passage / Reading     9. Research Packet       15. Dataset / Benchmark
 4. Claim                10. Synthesis             16. Agent Context Bundle
 5. Argument             11. Essay / Explainer
 6. Crux                 12. Education / Understanding Check
```

Each is detailed below with: what it is · the canonical artifact · the checkpoint ladder · the
product URL/name · which v2 layer(s) it maps to · which existing modules/vision support it.

---

## 1. Translation — *the simplest product, what readers consume*

- **What:** SOURCE PASSAGE → TRANSLATION. Exposes Sanskrit, word segmentation, literal translation,
  readable translation, notes, uncertainties, alternate readings.
- **Artifact:** `TranslationRevision`
- **Checkpoint:** T0 machine draft → T1 source-complete → T2 morphology/syntax → T3 terminology →
  T4 independent review → T5 scholar approved
- **Product page:** `patala.org/translation/IPVV-1.5.11`
- **v2 layer:** DraftTranslation + Translation (positions 1, 4)
- **Supports:** `t1_worker.py`, `l1_l2_worker.py`, `state_machine.py` (T1→R1→T2→R2→T3→T3.1→C1)

## 2. Translation Proof — *a flagship product*

- **What:** NOT "AI says this translation is good" — a structured **non-aggregate vector** of audit
  dimensions. Expose per-dimension PASS/WARN/pending, never a single "94% score."
- **Dimensions:** SOURCE_COVERAGE · TARGET_GROUNDING · MORPHOLOGY · SYNTAX · NEGATION · MODALITY ·
  TERM_CONSISTENCY · SEMANTIC_ENTAILMENT · PARALLEL_WITNESS · HUMAN_REVIEW
- **Artifact:** `TranslationProof TP-NNNN` (vector, not scalar)
- **Checkpoint:** TP0 generated → TP1 deterministic checks → TP2 adversarial audit → TP3 independent
  review → TP4 scholar adjudicated
- **v2 layer:** TranslationProof (position 5) — **the moat**
- **Supports:** `l200_worker.py`, `certificate_l200.py`, `inspect_l200*`, the 63 sibling golds
- **Vision:** `PATALA-V2-SPEC.md` §5 · `docs/process/INDUSTRY-ALIGNMENT.md` (TranslationProof novel)

## 3. Passage / Reading — *the philology-facing primitive*

- **What:** the canonical passage page: SOURCE → witnesses, editions, variants, segmentation,
  morphology, readings, translation revisions. Product = **Passage Workbench** where a Sanskritist says
  "I disagree with this sandhi resolution / I prefer reading X / this edition has Y."
- **Artifact:** canonical Passage object
- **Checkpoint:** P0 ingested → P1 normalized → P2 witness-aligned → P3 readings encoded → P4 reviewed
- **v2 layer:** Source + Tokenization (positions 0, 2) — the foundation under Translation Proof
- **Supports:** `l0_worker.py`, `certificate_l0.py`, `app/read`, `app/api/passages/*`, lemma-through-time
  (`trajectories.ts`), the timeline (`historyTimeline.json`)

## 4. Claim — *the first serious scholarly abstraction*

- **What:** PASSAGES → CLAIM. Example: "Abhinavagupta treats recognition as re-identification rather
  than acquisition of genuinely new knowledge." Exposes: claim, scope, modality, source passages,
  supporting evidence, counterevidence, interpretive status, authority.
- **Crucially:** SOURCE-SAYS / SCHOLAR-RECONSTRUCTS / PĀṬALA-INFERS must remain visibly distinct.
- **Artifact:** `Claim C-NNNN`
- **Checkpoint:** C0 proposed → C1 evidence attached → C2 scope/modality audit → C3 contradiction search
  → C4 independent review → C5 adjudicated
- **v2 layer:** Argument's proposition floor (position 7) + Review
- **Supports:** `proposition_layer.py`, `patala_core/objects.py` (PropositionObject),
  `docs/api/concepts/epistemic-model.md` (the status rules)

## 5. Argument — *a major product, a real Argument Proof*

- **What:** NOT mere argument visualization. A real **Argument Proof**: premises, inference, conclusion,
  evidence, defeaters, **validity** AND **soundness** as two independent judgements.
- **Artifact:** `Argument ARG-NNNN` (standalone, citable — "Pāṭala Argument")
- **Checkpoint:** A0 reconstructed → A1 premises grounded → A2 inference classified → A3 validity checked
  → A4 defeaters generated → A5 rival reconstruction tested → A6 reviewed
- **v2 layer:** Argument (position 7) — the frontier
- **Supports:** `argument.py`, `aspic_adapter.py`, `aifgraph.py`, `crux_engine.py`, `nyayagate.py`,
  `epistemic_worker.py` (`make_argument_handlers`), the 51 ARGMAP golds

## 6. Crux — *its own product, a major scholar-acquisition mechanism*

- **What:** the smallest unresolved proposition whose resolution would materially change the debate.
  Exposes: question, Position A/B, decisive evidence required, current best evidence, downstream
  consequences.
- **Artifact:** `Crux CRUX-NN`
- **Checkpoint:** CR0 candidate → CR1 downstream sensitivity confirmed → CR2 rivals represented →
  CR3 decisive-evidence conditions defined → CR4 reviewed
- **Product name:** **Open Crux**
- **v2 layer:** Argument's crux primitive (position 7)
- **Supports:** `crux_engine.py`, `patala_core/objects.py` (CruxObject)

## 7. Review — *itself a publishable object*

- **What:** `Review { target, reviewer, findings, severity, evidence, proposed corrections, disposition }`.
  Types: translation/argument/citation/source/essay/benchmark review. Statuses: OPEN · SUPPORTED ·
  REJECTED · RESOLVED · SUPERSEDED. Creates a visible scholarly **correction history**.
- **v2 layer:** Review/Adjudication (cross-cutting)
- **Supports:** `review_engine.py` (ReviewEvent ledger + impact), `review_bundle.py`,
  `contracts_human_authority.py`, `vision-06-adversarial-review.md`

## 8. Scholar Attestation — *highest-moat product after Translation Proof*

- **What:** a scholar attests to something **precise** (a TranslationRevision, a scope, a verdict like
  ACCEPT WITH QUALIFICATIONS) — never "approve all of Pāṭala." Attestation types: source authenticity,
  textual reading, translation fidelity, historical claim, argument reconstruction, bibliographic
  completeness.
- **Artifact:** signed `ScholarAttestation` (SA3 signed → SA4 public/citable)
- **Checkpoint:** SA0 invitation → SA1 review submitted → SA2 identity verified → SA3 attestation signed
  → SA4 public/citable
- **v2 layer:** Scholar Attestation (Layer 08) — the priority
- **Supports:** `contracts_human_authority.py` (Proposal/Adjudication), `review_engine.py`,
  `vision-07-new-scholar.md`; creates the **expert verification network**

## 9. Research Packet — *extremely practical, first monetizable scholar product*

- **What:** compile a question into: key claims, primary sources, strongest secondary literature,
  quotations/passages, disagreement map, cruxes, missing evidence, bibliography. Instead of searching
  twenty systems. Useful for scholars/students/writers/agents/YouTube/papers.
- **Artifact:** `ResearchPacket`
- **Checkpoint:** RP0 search → RP1 source gathering → RP2 evidence extraction → RP3 contradiction/rival
  search → RP4 bibliography audit → RP5 reviewed
- **v2 layer:** a projection over the whole spine
- **Supports:** `retrieval.py`, `pushing.py`, `semantic_alignment.py`, the atlas, `vision-07`

## 10. Synthesis — *not "AI summary"*

- **What:** multiple reviewed claims + arguments + cruxes + source constraints → a synthesis exposing
  what is **established / probable / disputed / unknown**. Very strict epistemic language.
- **Artifact:** `Synthesis` (e.g. "State of the Question: Recognition in Utpaladeva and Abhinavagupta")
- **Checkpoint:** S0 candidate → S1 claims grounded → S2 contradictions reconciled/retained →
  S3 cruxes surfaced → S4 certainty calibrated → S5 reviewed
- **v2 layer:** Synthesis (position 8) — honest EMPTY today
- **Supports:** `synthesis_core.py`, `epistemic_worker.py` (`make_synthesis_handlers`)

## 11. Essay / Explainer — *a projection of the graph*

- **What:** SYNTHESIS → ESSAY. Every sentence retains `SentenceEvidence`; users click "Why does Pāṭala
  say this?" Formats: scholarly essay, popular explainer, video script, lecture, timeline, FAQ — SAME
  underlying proof graph.
- **Checkpoint:** E0 generated → E1 sentence evidence → E2 citation audit → E3 strength-drift audit →
  E4 editorial review
- **v2 layer:** Essay (position 9) + media projection
- **Supports:** `essay_compiler.py`, `essayverify.py`, `essayplan.py`, `essaysentence.py`, the 22 gold
  essays, `vision-07-new-scholar.md` (essay = rendering of the graph)

## 12. Education / Understanding Check — *one of the most distinctive products*

- **What:** compile arguments into questions where answering correctly demonstrates the conceptual
  distinction. Each distractor maps to a specific error (scope confusion, modal confusion, premise/
  conclusion reversal, rival-position confusion). Outputs: MCQ, argument completion, premise ranking,
  contradiction spotting, source attribution, counterfactual questions.
- **Checkpoint:** ED0 generated → ED1 answer proof → ED2 distractor proof → ED3 ambiguity test →
  ED4 learner calibration → ED5 reviewed
- **v2 layer:** Lesson (position 10) — honest EMPTY today
- **Supports:** `education_compiler.py`, `education_ir.py` (LearningClaim/Skill/Interaction/
  MasteryEvidence), `PATALA-EDUCATION-SYNTHESIS.md`, `edu_bench.py`

## 13. Comparison — *a really strong focused module*

- **What:** structured comparison (translation A vs B, scholar A vs B, text A vs B, argument A vs B,
  tradition A vs B) with output classified: AGREEMENT · DISAGREEMENT · APPARENT DISAGREEMENT ·
  TERMINOLOGICAL DIFFERENCE · SCOPE DIFFERENCE · REAL CRUX. E.g. "Torella vs Ratié on recognition."
- **Checkpoint:** CMP0 align claims → CMP1 normalize terminology → CMP2 scope/modality check →
  CMP3 actual contradictions → CMP4 crux extraction → CMP5 reviewed
- **v2 layer:** a projection over the spine
- **Supports:** the comparison machinery + the crux engine

## 14. Audit — *a generic product family, easiest standalone business product*

- **What:** input = someone else's artifact → output = `Findings[]` with severity, evidence, proposed
  correction, confidence. Families: Translation/Citation/Argument/Term/Bibliography/Source/Essay/
  AI Output Audit.
- **v2 layer:** Verification (Layer 07)
- **Supports:** `FIRST_PRODUCT_DECISION.md` (Translation Audit as the FIRST public product),
  `review_engine.py`, the eval plane

## 15. Dataset / Benchmark — *research credibility + infrastructure value*

- **What:** reviewed objects naturally generate benchmarks (Pāṭala Sanskrit Translation Benchmark,
  Negation Challenge, Compound Resolution, Argument Reconstruction, Citation Entailment, Scholar
  Review). Derived from **actual disagreements/failures**, not synthetic trivia.
- **Checkpoint:** B0 candidate cases → B1 decontamination → B2 gold creation → B3 independent
  adjudication → B4 blind eval → B5 public release
- **v2 layer:** Verification (Layer 07)
- **Supports:** the 5 golds, the eval plane, `FIRST_PRODUCT_DECISION.md` (IPVV Benchmark as the FIRST
  strategic asset)

## 16. Agent Context Bundle — *the machine-facing product*

- **What:** humans use Research Packet; agents use **Context Bundle** —
  `context(ARG-32, budget=8000)` returns object, premises, evidence, defeaters, cruxes, reviews,
  authority, dependencies — already ordered and token-budgeted. Variants: micro 2k / standard 8k / deep 32k.
- **v2 layer:** the read-plane "agent cache line" (Layer 12)
- **Supports:** `PATALA-V2-SPEC.md` §10-11 (agent bundles), the MCP thin adapter (8 verbs)

---

## THE PRODUCT HIERARCHY (what the website shows — 4 families, not 16 items)

### **Texts** *(Sanskrit/philosophy entry point)*
Reading · Translation · Translation Proof · Compare Translations · Term Audit

### **Arguments** *(the philosophy/research engine)*
Claim · Argument · Crux · Comparison · Synthesis

### **Scholar** *(the scholarly infrastructure / business layer)*
Research Packet · Review · Scholar Attestation · Audit · Benchmark

### **Learn** *(the public/education layer)*
Essay · Explainer · Argument Map · Understanding Checks · Course

### Underneath all of them:
API · MCP · Context Bundles · Datasets

---

## THE CANONICAL PRODUCT GRAPH

```text
TEXT
 │
 ▼
PASSAGE
 │
 ▼
TRANSLATION
 │
 ▼
TRANSLATION PROOF
 │
 ▼
CLAIM
 │
 ▼
ARGUMENT
 │
 ├────► CRUX
 │
 ▼
REVIEW
 │
 ▼
SCHOLAR ATTESTATION
 │
 ▼
RESEARCH PACKET
 │
 ▼
SYNTHESIS
 │
 ├────► ESSAY
 ├────► EDUCATION
 ├────► VIDEO
 ├────► API
 └────► BENCHMARK
```

> The moat products: **Translation Proof, Argument Proof, Crux, Scholar Attestation, Research Packet.**
> Translation/essays/education are what people consume; those five are the infrastructure that makes the
> outputs difficult to copy convincingly.

---

## THE BUILD ORDER (the focused first-six vertical)

Don't attempt all products at once. Build **six canonical vertical products first**, because everything
after CP6 becomes a **projection** of the first six:

```text
CP1  PASSAGE             source + canonical IDs + morphology/readings
CP2  TRANSLATION PROOF   translation + multidimensional proof
CP3  CLAIM               passage → defensible proposition
CP4  ARGUMENT            claims → inference + validity + defeaters
CP5  SCHOLAR REVIEW      review + attestation + correction history
CP6  RESEARCH PACKET     compile all of the above into a deliverable
```
Then:
```text
CP7  SYNTHESIS
CP8  ESSAY
CP9  EDUCATION
CP10 BENCHMARK
```

---

## THE SOURCE MAP (products ↔ v2 ↔ vision ↔ modules)

| Product | v2 layer | Vision doc | Reuse modules |
|---|---|---|---|
| Translation | DraftTranslation, Translation | endgame1, vision-02 | `t1_worker`, `l1_l2_worker`, `state_machine` |
| Translation Proof | TranslationProof | INDUSTRY-ALIGNMENT | `l200_worker`, `certificate_l200`, `inspect_l200*` |
| Passage/Reading | Source, Tokenization | vision-15 (atlas) | `l0_worker`, `trajectories.ts`, `historyTimeline.json` |
| Claim | Argument floor | vision-06, epistemic-model | `proposition_layer`, `objects.py` |
| Argument | Argument | vision-06 | `argument`, `aspic_adapter`, `aifgraph`, `nyayagate` |
| Crux | Argument crux | vision-06 | `crux_engine` |
| Review | Review/Adjudication | vision-06, vision-07 | `review_engine`, `review_bundle` |
| Scholar Attestation | Scholar Attestation | vision-07 | `contracts_human_authority` |
| Research Packet | projection over spine | vision-07 | `retrieval`, `pushing`, `semantic_alignment` |
| Synthesis | Synthesis | — | `synthesis_core`, `epistemic_worker` |
| Essay/Explainer | Essay | vision-07, essayguide | `essay_compiler`, `essayverify` |
| Education | Lesson | education synthesis | `education_compiler`, `education_ir` |
| Comparison | projection over spine | vision-09 (cross-tradition) | crux engine |
| Audit | Verification | FIRST_PRODUCT_DECISION | `review_engine`, eval plane |
| Dataset/Benchmark | Verification | FIRST_PRODUCT_DECISION | the 5 golds, eval plane |
| Agent Context Bundle | read plane | SPEC §10-11 | MCP, projection compiler |

*This is the formalized product doctrine. The internal layer names (v2), the vision docs, and the reuse
modules all stay canonical — this file is the user-facing productization of them.*
