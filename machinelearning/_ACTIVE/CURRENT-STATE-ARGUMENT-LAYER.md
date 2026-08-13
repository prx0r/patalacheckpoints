# CURRENT STATE — THE ARGUMENT LAYER (the architecture as it actually is)

*2026-08-12. THE authoritative current-state doc for Agent 1. If you read only one thing for orientation,
read this. It corrects a stale mental model that the handover docs (DEVPLAN / NEXT-STEPS / COMPONENT-CONTRACTS /
SESSION) no longer reflect. The code + CLAIMS P-020/P-021 are the truth; the older handover prose lagged them.
Read this FIRST, then `NEXT-STEPS.md` for the directive.*

---

## THE CORRECT ARCHITECTURE (top to bottom)

```
SOURCE / L0 / L2 / C1
        ↓
Propositions
        ↓
Local Arguments
        ↓
ArgumentAudits
        │
        ├──── Themes            (where in the conceptual landscape?)
        │
        ↓
ResearchPack                   [inquiry/material selection]
        ↓
ArgumentSynthesis              [higher-order reasoning]  ← THE MISSING LAYER, now being built
        ↓
SynthesisAudit
        ↓
 ┌──────┼────────────┐
 ↓      ↓            ↓
EO   EssayPlan   ArgumentMap
       ↓
     Essay
       ↓
SentenceEvidenceAudit
```

**Responsibilities:**
- **Themes** — where in the conceptual landscape?
- **Argument** — what does this local passage claim, and why?
- **ArgumentAudit** — what structural defects / tensions are present?
- **ResearchPack** — which objects are relevant to this inquiry? (composition/selection, NOT a cohesive argument)
- **ArgumentSynthesis** — what larger argument follows from those objects? (higher-order reasoning)
- **EssayObject** — one structured presentation/projection.
- **Essay** — prose communication.

---

## THE NYĀYA GATE IS ACTIVE (not parked, not unwired)

The argument IR prerequisite is already crossed: the 5 golds are IR-complete enough to support real
Proposition/Inference-shaped operations. The gate is no longer hypothetical infrastructure.

```
build_argument(...)                → construction-ONLY
    ↓
ArgumentProposal
    ↓
audit_argument(argument, comparison_graph)   → the ContextualArgumentAudit (the seam)
    ↓
structural Nyāya gate + graph-aware viruddha nomination
    ↓
ContextualArgumentAudit
    ↓
argument.audit_refs[]
```

**Deliberate, frozen design decision:** argument construction ≠ contextual argument validation.
`build_argument()` is construction-only; `audit_argument()` is where the graph-aware audit lives. Keep this
split frozen.

**What Nyāya currently means** (narrow, by design):
- A **bounded structural defect checker + contextual contradiction-candidate nominator**, over the
  Nyāya-inspired defect families: asiddha · viruddha · savyabhicara · satpratipaksa · badhita.
- It is **NOT** "this argument is philosophically proven valid."
- A clean gate can establish an **engineering/structural** result (`ENGINEERING_VALIDATED` in its dimension).
- It **cannot** establish: `SCHOLARLY_CORROBORATED`, `INDEPENDENT_REVIEWED`, or historically correct interpretation.

---

## VIRUDDHA — implemented, overclaimed, falsified, repaired

This is the project's epistemic discipline in action:
- **v1** compared candidate claims against committed propositions for content-overlap + opposite polarity. A
  first cross-gold scan surfaced 3 alleged disagreements, initially **overclaimed** as real findings.
- **Peer assessment** showed all 3 were **false positives** (e.g. "pratibhā is order-less" vs "pratibhā is not
  constituted by order" — the same position encoded differently; plus junk lexical overlap). **Retracted**
  explicitly; the fixtures were deleted/reclassified.
- **v2** now: removes function-word junk; preserves Sanskrit Unicode/diacritics; excludes RECONSTRUCTED and
  opponent-attributed propositions from the established pool; carries explicit defeater metadata; emits
  `VIRUDDHA_CANDIDATE` / `semantic_status: UNRESOLVED` — not contradiction. Defeaters: SCOPE_DIFFERENCE,
  MODALITY_DIFFERENCE, SPEAKER_DIFFERENCE, TEMPORAL_DIFFERENCE, QUALIFICATION, LEVEL_DIFFERENCE,
  NON_EQUIVALENT_PREDICATE. Detector version `PATALA.VIRUDDHA.GRAPH.v2`; candidates use `VIR-CAND-...`.
- **Rule: STOP improving viruddha.** It is good enough as a structural nominator with semantic defeaters. Do
  NOT turn it into a semantic-contradiction oracle.

**Cross-argument "disagreements" are now only tension candidates** (commitment-sensitive extractor):
- RECONSTRUCTED ↔ ASSERTS → `RECONSTRUCTION_TENSION_CANDIDATE`
- ASSERTS ↔ ASSERTS → textual/committed tension candidate
- DERIVES ↔ DERIVES → inference tension candidate
- **Rule: candidate ≠ fixture ≠ adjudicated disagreement.** No current cross-gold viruddha result is a
  settled disagreement in the IPVV.

---

## RESEARCHPACK IS REAL BUT NOT THE MISSING LAYER

Two concrete packs exist: `PACK-IPVV-NONCONSTRUCTED-I`, `PACK-IPVV-REFLEXION-CORE` — resolving against real
argument refs, proposition refs, themes, passages, evidence. **ResearchPack answers "which existing objects
belong together for this inquiry?"** — it is a composition/selection layer. **ResearchPack ≠ cohesive
argument.** It does not create the higher-order argument connecting those objects.

---

## THE MISSING LAYER = ARGUMENTSYNTHESIS (Pāṭala-native)

- **Argument** = local reasoning reconstructed from a textual unit.
- **ArgumentSynthesis** = higher-order reasoning constructed from multiple arguments/evidence objects.
- Named **ArgumentSynthesis**, NOT `CoherentArgument` ("coherent" prejudges success) and NOT `ArgumentPack`
  (sounds like another container).

Example: ARG-002 ("I-reflexive awareness is not merely conceptual construction") + ARG-004 ("manifestation
without vimarśa would be inert") may support the larger claim "reflexive self-awareness belongs intrinsically
to manifestation rather than being externally constructed" — but that larger conclusion is NEITHER ARG-002 NOR
ARG-004; it needs a **new bridge inference**, which must be **first-class**.

### EO is a projection, not the canonical reasoning layer
The EO was considered as the schema for the higher-order object and **rejected**: it inherits truth-engine
assumptions, is shaped around a 5-member Nyāya presentation, not every IPVV argument fits that form, and it
should not become the core Pāṭala ontology. EO is a **consumer/projection**: `ArgumentSynthesis → synthesis_to_eo()`
(also → `synthesis_to_essay_plan()`, → `synthesis_to_argument_map()`). **Do NOT make ArgumentSynthesis = EO.**

### Evidence-aware EssayObject (built + peer-reviewed, commit 57a9784)
The reflexion-core EO path was peer-reviewed hard; the fixes are in. The artifact is honestly **evidence-aware
EssayObject construction**, not an essay renderer. Each evidence claim separates `structural_gate_outcome`
from `epistemic_status` (e.g. `accepted` vs `MACHINE_PROPOSED`), encoding GATE_ACCEPTED ≠ EVIDENCE_ACCEPTED ≠
SCHOLARLY_SUPPORTED. Missing refs hard-fail; unsourced rivals become `UNSOURCED_RECONSTRUCTION`; explicit
`inferences[]`/`warrant`/`status: RECONSTRUCTED`; the negative render-rule test is real (mutate → set settled
nigamana → validator rejects).

---

## THE CORE MECHANISM OF THE SYNTHESIS: dependency propagation (weakest-governs)

**Wrong:** ARG-002 accepted + ARG-004 accepted = synthesis strongly supported.
**Correct:** the synthesis epistemic ceiling = the **minimum status of all load-bearing dependencies**
(ARG-002 dependency status · ARG-004 dependency status · SYN-INF-001 warrant status · open cruxes), with
explicit reasons.

A synthesis can be **STRUCTURALLY_COHERENT** yet **SEMANTICALLY_UNRESOLVED**. That distinction is essential.
Themes stay metadata (`theme_refs`) and **never** become inferential premises.

---

## STATE LADDER (unchanged, still honest)

```
MACHINE_PROPOSED
    ↓
ENGINEERING_VALIDATED     ← a clean Nyāya audit can justify this, in its dimension
    ↓
SCHOLARLY_CORROBORATED    ← NOT by the gate; opportunistic published scholarship, where load-bearing
    ↓
INDEPENDENT_REVIEWED      ← a human reviewing the exact object
```

A clean Nyāya audit can justify the ENGINEERING_VALIDATED transition. It cannot skip to the latter two.

---

## THE DIRECTIVE (what Agent 1 does next — see NEXT-STEPS.md)

**The one vertical path is DONE, VALIDATED, and PEER-REVIEW-CLEAN** (relative to the current proposition/synthesis
objects), pushed on `origin/agent1-argument-layer-a1b`: `0efc1df` (A.1) → `32083e6`+`d8b123b` (B) →
`a2c4591`+`398958f` (C) → `b1fb034`+`6b19f2b`+`cfcd1c5`+`aef17dd` (C.1 review passes) → `7ea182c`+`76263d8`
(k-core/Louvain). All test suites pass.

**The vertical is frozen and Agent 1 is on hold.** No C.2 / compositional-drift mechanism, no more clustering,
no xAIF, no TantraFact, no scholar-stamp/SEPIO runtime (deferred roadmap = record, not queue).

**Key boundary frozen:** Pāṭala distinguishes (a) metadata correctness, (b) semantic surface fidelity
(`PARAPHRASE_EXPANSION / CLAIM_SURFACE_INFLATION`), and (c) `reconstructable argument ≠ structurally validated
argument`. The semantic-relation labels are **reviewer-assigned assertions, not independently machine-proven
facts** — C.1 rejects declared unsupported expansion but does not yet auto-establish that a declared
`CONSERVATIVE_PARAPHRASE` is semantically correct.

**P-019 v2 (k-core/Louvain):** k-core = deterministic structural embeddedness; Louvain = heuristic modularity
community; `k_core != theme`. Empirical: on the 63-node IPVV C1 graph Louvain is STABLE (11 communities across
20 seeds, 0 unstable boundaries) — so k-core's rationale is deterministic embeddedness + reproducibility, not
that Louvain was unstable here.

**The next move is Agent 2 / the autonomous factory** (shared infra: registry idempotency → single-writer lock →
Hermes timeout/orphan cleanup → stable passage_id+hash binding → bounded batching → ASCII-avagraha → OCR→SOURCE_BLOCKED →
crash/resume + adversarial tests → Sanskrit-only replay certificate → a small Kramasadbhāva unattended canary; then
a generic L0 controller reused across the canonical production stack `L0/L1 → L2 READ → L200 AUDIT → C1 → THEMES →
ESSAYS → EDUCATION`, with L200 as the future derivational grounding seam for propositions/arguments). See
`NEXT-STEPS.md` revision 6.

## THE "DO NOT" LIST (Agent 1)
re-audit the 5 golds · restart systematic corroboration · improve viruddha · build more Nyāya heuristics ·
expand ResearchPack schema abstractly · generalize EO · bulk essay generation · semantic embedding/ranking ·
another evidence matrix · treat 26/26 tests as scholarly validation · treat `structural_gate_outcome=accepted`
as truth · promote any unresolved candidate to fixture · force every argument into the Nyāya EO form.

---

*This doc is the correction. If a handover doc (DEVPLAN / NEXT-STEPS / COMPONENT-CONTRACTS / SESSION /
CONTEXT-CHAIN) contradicts this, THIS is current and the other is stale — fix the other.*
