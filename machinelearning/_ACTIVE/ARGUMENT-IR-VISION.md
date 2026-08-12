# ARGUMENT-IR-VISION — the philosophical IR as the CP4 target (reconciled with the global vision)

*2026-08-12. Reconciles a third-party architecture review (the "argument-under-interpretation"
philosophy IR) with Pāṭala's existing global vision. **It does not rewrite the checkpoint ladder.** It
deepens what CP4 (Argument) IS and how it must be built — by making the philosophical intermediate
representation the target the hand-gold grows into. Read `VISION_AND_NAVIGATION.md` +
`dualagentvision.md` first; this is the refinement of STEP 6 / CP4 on top of them.*

---

## 0. THE HEADLINE (honest)

The review is **directionally excellent but it is a refinement, not a rewrite.** Its core claims already
exist in our project:

| Review claim | Where we already have it |
|---|---|
| "alignment before contradiction" | `SEMANTIC-COMMENSURABILITY.md` (the 3 relation types, the decision ladder) |
| "argument-under-a-frame" | `DebateFrame` (in `gold002.py`, `CHECKPOINTS.md` #8) |
| valid ≠ sound ≠ justified ≠ attributed ≠ true | the whole doctrine (`AGENTS-DOCTRINE.md`) |
| "don't reinvent the argumentation engines" | our guardrail (don't build the essay/Bayesian stack) |
| "UNDERDETERMINED is first-class" | the gate's abstain + `UNDERDETERMINED` outcome |
| **"let the gold force the ontology into existence"** | our own "one real gold > 1,000 shells" doctrine |

**What the review genuinely ADDS** (the real value):
1. `Commitment` (who asserts/denies/attributes/reconstructs) — fixes the pūrvapakṣa-as-Abhinava's-own error.
2. `ResearchQuestion` as a first-class object — the scholar's navigation unit.
3. `Position` as a bundle of commitments+arguments under a frame.
4. **Derivational `Proposition`** — every proposition remembers *how it came into existence*
   (explicit Skt / reconstructed L2 / derived C1 / implicit / attributed / editor-accepted).
5. Three-level `SemanticAlignment` (LEXICAL / CONCEPTUAL / PROPOSITIONAL).
6. `Attack` vs `Defeat` split; `EvaluationRun` as immutable (reproducible) evidence.
7. `Crux` as outcome-sensitivity (a computable graph problem, not an authored label).

---

## 1. HOW IT RECONCILES WITH THE CHECKPOINT LADDER

**The CP ladder is UNCHANGED.** The review operates entirely inside CP4 (Argument) and its downstream
(CP5 verification, CP6 synthesis):

```
CP0 BENCHMARK   (unchanged)
CP1 SOURCE PROOF (unchanged — Agent 2)
CP2 RETRIEVAL   (unchanged)
CP3 THEMES      (unchanged)
CP4 ARGUMENT    ← ENRICHED: the target is a philosophical IR (14 objects), built gold-first
CP5 VERIFICATION ← the multi-evaluator role (ASPIC / Nyāya / formal / semantic / philological)
CP6 SYNTHESIS   ← becomes trivial structurally (Question → Frame → Positions → Arguments → Crux → EssayPlan)
```

**The key reconciliation principle (from the review, matching our doctrine):**

> **Ontology may anticipate. Implementation must follow evidence.**

The 14-object IR is the **horizon schema** — a target that documents where CP4 is going. It is NOT to be
implemented empty. Only the objects the hand-gold actually requires get activated.

---

## 2. THE BUILD ORDER (inverted — gold first, ontology second)

The review correctly inverts the "design-then-encode" order. This is EXACTLY our CP4 gate:

```
ARG-GOLD-001  →  minimal objects (Proposition, Commitment, DebateFrame, InferenceRule, Argument)
ARG-GOLD-002  →  schema expands (objection→reply needs Attack)
ARG-GOLD-003  →  schema stabilizes (reductio needs Commitment: ASSUMES_FOR_ARGUMENT)
ARG-GOLD-004  →  conceptual distinction (needs three-level SemanticAlignment)
ARG-GOLD-005  →  ambiguous (needs ResearchQuestion + Position for two defensible reconstructions)
      ↓
  IR v1 FREEZE (only after 5 real arguments are represented without loss)
```

**The rule:** *if the gold can't force the ontology, the ontology isn't real.* Every new gold argument is
a probe that expands the schema only where the scholarship demands it.

---

## 3. THE MULTI-EVALUATOR ARCHITECTURE (CP5 — the destination)

The review's strongest structural contribution is making evaluation **profile-relative and multi-
evaluator** instead of one "truth" engine:

```
Pāṭala Argument (in the IR)
     │
     ├── ASPIC evaluator   → "what follows under a defeasible argumentation framework?"
     ├── Nyāya audit       → "does the inferential structure exhibit the 5 hetvābhāsas?"  (we HAVE this)
     ├── semantic verifier → "did we preserve scope, attribution, meaning?"  (we HAVE this, partially)
     ├── formal evaluator  → "is a selected encoding formally valid?"  (Lean/Z3, LATER)
     └── philological proof→ "does the source ground the proposition?"  (we HAVE this, L0)
```

**No single evaluator determines "truth."** Each asks a different question. The output is
dimensions-under-a-profile (`UNDERDETERMINED UNDER SHARED GROUND`), never "A wins 72%." This is our
gate's `tradition` field + `abstention` principle generalized into a first-class `EvaluationProfile`
+ immutable `EvaluationRun`.

**⚠️ The existing `nyayagate.py` becomes one evaluator in this architecture** — the Nyāya audit. It is
already measured and frozen. It does not need to become the whole answer.

---

## 4. THE 14 OBJECTS (the horizon — freeze the schema, activate only what gold needs)

```
 1. ResearchQuestion     8. InferenceApplication
 2. Proposition          9. Argument
 3. Commitment          10. Attack
 4. Position            11. Preference
 5. DebateFrame         12. Crux
 6. SemanticAlignment   13. (EpistemicRegime)
 7. InferenceRule       14. (ArgumentScheme)
+ EvaluationProfile + EvaluationRun  (non-primary: configuration / derived)
```

**For the next 5 gold arguments, activate only:** ResearchQuestion · Proposition · Commitment ·
DebateFrame · InferenceRule · InferenceApplication · Argument · Crux. Leave Preference, EpistemicRegime,
Attack, Position, ArgumentScheme **thin** until real examples demand them.

---

## 5. WHAT THIS MEANS FOR THE GOLD RIGHT NOW (the immediate, concrete change)

The single highest-value change to the existing gold shape, per the review:

1. **`Commitment` (or `speaker`/`force`) on every gold node** — ASSERTS / DENIES / PRESUPPOSES /
   ASSUMES_FOR_ARGUMENT / ATTRIBUTES_TO_OPPONENT / QUOTES / RECONSTRUCTED. This fixes the
   pūrvapakṣa-attribution error the whole corpus is vulnerable to (the Buddhist objection read as
   Abhinava's own view).
2. **Derivational `Proposition`** — each node records `derived_from` (Sanskrit / L2 / C1 / implicit /
   editor) + `explicitness` (EXPLICIT/RECONSTRUCTED/IMPLICIT). Our gold already has `explicitness`;
   add `derived_from`.
3. **A `ResearchQuestion`** at the top of each gold argument (what question does this argument answer?).
   Our `DebateFrame.question` already carries it — make it first-class.
4. **Split `Defeater` into `Attack` (data) + `Defeat` (derived)** — store the objection; whether it
   defeats is derived (and the Nyāya gate decides that, later).
5. **Three-level `SemanticAlignment`** (LEXICAL/CONCEPTUAL/PROPOSITIONAL) — needed by ARG-005.

**These are the changes ARG-003/004/005 should be BUILT with — not deferred.** The review says the
ontology is forced by the gold, so build the gold with the IR's richer shape from the start.

---

## 6. HOW IT BECOMES AGENT-BASED CHECKPOINTS & INSTRUCTIONS

### The shared vision (unchanged, refined)
- `VISION_AND_NAVIGATION.md` (root) — the compass. Add a pointer to this doc under STEP 6.
- `dualagentvision.md` + `dualagentvision-ADAPTED.md` — the CP ladder + state map. Unchanged.
- **`ARGUMENT-IR-VISION.md` (this doc)** — the CP4 target schema + build order.

### Agent 1 (ML) — owns CP4. Instructions become:
```
Build ARG-003/004/005 WITH the IR's shape:
  - Commitment (speaker/force) on every node
  - derivational Proposition (derived_from + explicitness)
  - a ResearchQuestion per argument
  - Attack vs Defeat split
  - three-level SemanticAlignment for ARG-005
Let the gold force the ontology — expand the schema only where scholarship demands.
Do NOT build EpistemicRegime/EvaluationProfile/Crux yet — the gold must come first.
```

### Agent 0 (coordinator) — gates CP4 by the IR test:
```
For each gold argument: can it be represented in the IR without loss?
  - every proposition has a commitment + derivation
  - the frame is mandatory for any cross-position claim
  - abstention is allowed (NO SAFE RECONSTRUCTION is a valid output)
If a gold argument forces the schema to grow, that's SUCCESS (the gold is working), not failure.
```

### Agent 2 (L0) — unchanged (CP1), but its `PhilologicalProof` becomes the `grounding`/`derived_from`
floor the IR's derivational propositions resolve to.

---

## 7. THE HONEST GAP (what this does NOT fix)

The IR is the **horizon**, not the current reality. We still have only 2 golds (ARG-001/002), no
extractor, no `Commitment` in the gold shape. The review itself warns against building the ontology
empty — so the honest position is:

> **This is the target schema for CP4, documented now so ARG-003/004/005 are built against it. But the
> only thing that makes it REAL is the gold. Until 5 real arguments are represented in the IR without
> loss, the 14-object ontology is a spec, not a result.**

---

## 8. THE ONE-SENTENCE CARRY-FORWARD

**The review validates our direction and deepens CP4: Pāṭala should not reinvent argumentation engines —
it should own the historically-grounded philosophical IR (Commitment, derivational Proposition,
ResearchQuestion, frame, alignment, regime) that existing engines cannot provide, built gold-first so the
ontology is forced by evidence, then evaluated multi-way (ASPIC / Nyāya / semantic / formal) under a
profile — never one "truth" number. The immediate action is to build ARG-003/004/005 with `Commitment`
and the derivational `Proposition` already in the shape; the 14-object IR is the horizon, not the now.**
