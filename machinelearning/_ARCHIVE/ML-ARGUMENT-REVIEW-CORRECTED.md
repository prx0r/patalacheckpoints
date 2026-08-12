# ML — CORRECTED ARCHITECTURE (external review incorporated)

*2026-08-12. The corrected Pāṭala ML architecture after an external review against digital philology
(Perseus/ATLAS, CITE/CTS), computational argumentation (AIF/Argument Web), scholarly knowledge graphs
(ORKG), claim verification (SciFact), provenance-aware generation (GenProve/TRACER/PaperTrail), and
formalization (Lean Copilot, Mathesis). **Three of my earlier claims were wrong/overclaiming; this doc
corrects them. The project is approved, the "60% solved" framing is rejected, and Lean is demoted.***

---

## 0. The corrected thesis

> **Pāṭala: Provenance-Preserving Scholarly Derivation from Primary Text to Argument and Synthesis.**

Sanskrit is the flagship domain, NOT the scientific problem. The real question is:

> Can a system preserve epistemic provenance while progressively transforming a primary historical
> source into translation, commentary, structured argument, and higher-order scholarly synthesis?

Nobody needs to "believe the model's essay" if the system exposes:
```
WHAT WAS SAID · WHAT WAS TRANSLATED · WHAT WAS INTERPRETED
WHAT WAS INFERRED · WHO ASSERTED IT · WHAT SUPPORTS IT
WHAT CHALLENGES IT · WHERE HUMAN JUDGMENT ENTERED
```

---

## 1. The corrected architecture (from the review)

```
PRIMARY TEXT (Sanskrit / witnesses)
  → L0 → L2 → L200 → C1
  → ARGUMENT PROPOSALS      (source-linked at every node; C1 only DISCOVERS, never proves)
  → human adjudication
  → ARGUMENT GRAPH          (supports / attacks / qualifies)
  → THEMES
  → ESSAY PLAN              (thesis · claims · objections · evidence · inference deps)
  → human approval
  → ESSAY RENDER            (sentence-level provenance: Quotation/Compression/Inference)
  → quote/claim/counterevidence verifiers
  → PUBLICATION
```
And Lean is a **separate, optional analytical instrument** on selected strictly-formalizable subgraphs.

---

## 2. Correction #1 — C1 → Argument is NOT low-effort (and not the ultimate evidence)

**The overclaim:** "Argument Mining over the pre-segmented C1s/IAs is low-effort."
**The correction:** pre-segmentation helps, but extracting *implicit premise, speaker, scope, reductio
structure, suppressed premise, target opponent, inference rule, qualification* from Abhinavagupta is
genuinely hard. And there's a **circularity risk**: formalizing our C1 and having the graph "confirm"
our interpretation just formalizes the commentary.

**The fix — an `ArgumentProposal` points DOWNWARD:**
```
ARG-031
  claim:      ...
  source:     Sanskrit span          ← the ultimate evidence
  L1 support: ...
  L2 rendering: ...
  C1 explanation: ...                ← DISCOVERS the argument, never proves it
  speaker:    ABHINAVAGUPTA
  role:       CONCLUSION
  explicitness: EXPLICIT | IMPLICIT
  inference:  ARG-INF-044
  status:     MACHINE_PROPOSED
```
C1 helps discover the argument; it must never be the ultimate evidence for it.

---

## 3. Correction #2 — Lean is not the general truth engine

**The overclaim:** "wire Lean Copilot for the PROVED verdict."
**The correction:** IPVV is transcendental reasoning, conceptual analysis, analogies, phenomenological
premises, defeasible inference — not a math textbook. Lean can prove "C follows formally from A, B, R"
but NOT "A faithfully represents what Abhinavagupta meant."

**The honest status:** `FORMALLY_VALID_GIVEN_ENCODING`, not `PROVED`. The chain:
```
Sanskrit → scholarly interpretation → formalization proposal
  → HUMAN FORMALIZATION REVIEW → Lean → FORMALLY_VALID_GIVEN_ENCODING
```
Lean is an **optional analytical instrument** for strictly-formalizable subarguments, not the spine.

---

## 4. Correction #3 — provenance ≠ support (four levels)

**RESOLVES** (the source exists — deterministic) ·
**AUTHENTIC** (the quotation really occurs there — deterministic) ·
**RELEVANT** (the evidence concerns the claim — semantic, model-proposed) ·
**SUPPORTS** (the evidence actually licenses the claim — semantic, human-reviewable).

Then: `ENTAILS · SUPPORTS · QUALIFIES · CONTRADICTS · INSUFFICIENT`.
The deterministic `/verify/*` services establish the first two; the last two are model-proposed +
human-reviewable. **Scope-checking is first-class** (SciFact's lesson: a passage may support a restricted
claim; the essay must not silently universalize it — that's the BOUNDARY mechanism).

---

## 5. What to steal (the five concrete adoptions)

| Source | Steal | Why |
|---|---|---|
| **CITE/CTS** | permanent scholarly identifiers independent of UI/storage | matches Pāṭala's resolver; citation/retrieval services more durable than apps |
| **AIF / Argument Web** | propositions ≠ inference schemes ≠ conflict nodes (not flat `premise[]→conclusion`) | the mature ontology for philosophical/defeasible argument graphs |
| **Nanopublications** | atomic assertions packaged with their provenance | an essay = ordered citable Claim objects, prose as a rendering |
| **ORKG** | structured scholarly knowledge publishable/queryable/comparable | the document need not be the fundamental unit of scholarship |
| **GenProve/TRACER** | generation emits provenance SIMULTANEOUSLY, not citations bolted on after | the essay mechanism |

---

## 6. The AIF-informed ArgumentGraph (what to build, not premise[]→conclusion)

```
INFORMATION NODE   a proposition / textual assertion
INFERENCE NODE     why proposition A supposedly licenses B
CONFLICT NODE      why proposition X challenges Y
```
Then only **strictly-formalizable subgraphs** become Lean candidates. This sits BETWEEN Sanskrit and Lean:
philosophical/defeasible argumentation stays in the informal graph; a small formal core routes to Lean.

---

## 7. The EssayPlan (the essay is a scholarly decision, not prose)

Don't build `ArgumentPacket → generate essay.md`. Build:
```
THEME / QUESTION
  → ESSAY PLAN     (thesis · claims[] · objections[] · evidence sets[] · counterevidence[] · inference deps[])
  → human/editor approval
  → sentence generation
  → sentence provenance (Quotation / Compression / Inference)
  → verification
```
**The essay plan is itself an auditable object.** GenProve's finding (Inference provenance is the hard
case) means the essay's *inferences* are where the ML frontier lives.

---

## 8. Attributed contexts (disagreement is first-class, not error)

Don't put everything in one flat graph. Distinguish:
```
ABHINAVAGUPTA ASSERTS X
UTPALADEVA ASSERTS Y
RATIÉ INTERPRETS X AS Z
TORELLA RENDERS TERM AS Q
PĀṬALA EDITOR PREFERS R
ESSAY ARGUES S
```
Epistemic worlds / attributed contexts make disagreements data, not inconsistencies.

---

## 9. The PaperTrail UX warning (verification must be frictionless)

Fine-grained provenance made researchers LESS trusting but didn't change reliance (verification was
burdensome). So Pāṭala's answer to verification must be:
```
Essay sentence → click "WHY?" → "This is an inference."
  Premise 1 → IPVV V2-A · Premise 2 → IPVV V2-O
  Inference: continuity depends on the recognizer
  Potential qualification: V3-X
  [Sanskrit] [Translation] [C1] [Audit]
```
Verification must be **easier than blindly believing**.

---

## 10. The validation methodology (measure every transformation, not the final essay)

Build ONE end-to-end **gold chain manually first**:
```
10 difficult IPVV passages → 30–50 source-grounded propositions → 10–15 inference relations
  → 3–5 objections/replies → 2 themes → 1 EssayPlan → 1,500-word essay
```
Every object hand-adjudicated. Then make the machine reproduce each transformation independently, and
measure EACH:
```
C1 → proposition: precision/recall
proposition → argumentative role: macro F1
argument relation (support/attack/qualify): F1
implicit-premise proposals: human acceptance rate
essay claim → evidence: support precision
scope preservation: error rate
counterevidence retrieval: Recall@k
sentence provenance (Quotation/Compression/Inference): accuracy
```
**Do NOT evaluate the final essay first** — one fluent essay hides where the pipeline failed.

---

## 11. The re-scored feasibility (honest)

```
Sanskrit → L2/L200            mature
L200 → C1                     mature-ish
C1 → Argument                 plausible, but NOT low-effort
Argument representation       adopt AIF (proposition/inference/conflict nodes)
Argument → EssayPlan          very plausible
EssayPlan → prose             easy
Provenance → source           very plausible
Inference verification        frontier / hard
Lean validation               useful only for a strict subset
Fully autonomous scholarship  NO — and shouldn't be the goal
```

---

## 12. The point of the whole thing

The breakthrough is NOT automatically proving Abhinavagupta. It's building the first environment where a
scholarly interpretation can travel from a Sanskrit phrase into a modern essay **without ever losing the
record of where translation ended, interpretation began, synthesis entered, disagreement remained, and
evidence came from.** That is both more achievable and more interesting than "the auditable Sanskrit
pipeline," and it is what the docs from here forward should describe.
