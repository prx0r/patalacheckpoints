# AGENT 1 — REACTION NOTES on the Atlas convergence plan

*2026-08-13. My working notes after saving `docs/global/agent1atlas.md` and reviewing the Atlas vision
files. Honest reaction: what is correct, what I noticed, what is missing, what needs correcting before
devpath7–12 begin.*

---

## 1. WHAT I REVIEWED

- `docs/global/agent1atlas.md` (the convergence directive, just saved)
- `docs/vision/vision-15-patala-atlas-sanskrit-research-graph.md` (the Atlas product framing)
- `docs/AGENT2-ATLAS-FOUNDATION-PLAN.md` (Agent 2's build plan: A2-0..A2-14)
- `docs/vision/atlas/technical-architecture-v1.md` (the frozen technical architecture, 2337 lines)
- `docs/vision/atlas/atlas-engineering-blueprint.md` (the Postgres/R2/API design)
- `docs/vision/atlas/atlas-performance.md`, `atlas-cloudflare-edge-layer.md`
- `docs/corpus/atlasflaws.md` (the honest self-critique of corpus verification)

---

## 2. THE DIRECTIVE IS MOSTLY CORRECT — but it's not new, it's a rediscovery

**The single most important thing I noticed:** `docs/vision/atlas/technical-architecture-v1.md` **already
contains almost the entire "convergence contract"** the directive proposes as devpath7–12. Specifically:

- §27 already says: fix `DerivedScholarlyObject` — replace `content: dict[str, Any]` with **Pydantic
  discriminated unions** (the exact devpath7 ask).
- §28 already says: **do not derive one misleading scalar authority** — keep the 4-axis vector, derive
  only display badges / eligibility gates (the exact devpath7 "remove scalar authority" ask).
- §29–31 already define typed `PropositionContent`, `CommitmentContent`, `GroundingLinkContent` with the
  exact same commitment vocabulary (ASSERTS/DENIES/PRESUPPOSES/ASSUMES_FOR_ARGUMENT/ATTRIBUTES_TO_OPPONENT/
  QUOTES/RECONSTRUCTED) as my devpath4 `proposition_layer.py`.
- §17 already has the typed-table SQL model (work/person/edition/witness/source + asset + authority_evidence).
- `AgentContextBundle` is already named.

**So the directive is not discovering a gap — it is formalizing a convergence that the Atlas docs
already agreed on.** The real work is that these are **specs, not code** — none of this is implemented yet
in the Agent-1 side or the Atlas side. That is the actual gap.

### The genuinely missing piece (the directive is right about this)
`ArgumentSynthesis` — the synthesis object — is **defined NOWHERE** in the Atlas docs or the technical
architecture. `PropositionContent`/`CommitmentContent`/`GroundingLinkContent` are there; `ArgumentSynthesis`
is not. devpath8 (synthesis core) is genuinely new and is the correct next Agent-1 milestone.

---

## 3. WHERE THE DIRECTIVE IS CORRECT

1. **One graph, not one packet.** Correct. The graph is the product; bundles are compiled read-models. This
   matches what I built: `ReviewBundle` (devpath6) is a materialization, not a new canonical type.
2. **Synthesis is the missing layer.** Correct and the single best point. `Argument → essay` and
   `Argument → education` independently WOULD create two competing interpretation layers. The
   `ArgumentSynthesis` parent is the right convergence object.
3. **Synthesis ≠ final truth.** Correct — matches the philosophy-engine discipline I've been holding
   (`verify_claim_semantic` is bounded, crux is perturbation). An `ArgumentSynthesis` that says
   "Position A has X/Y, Position B has objection Z, crux CRUX-12" is exactly the right non-asserting shape.
4. **Atlas/Agent-1 boundary.** Correct and necessary. Atlas owns identity+persistence; Agent 1 owns
   epistemic contracts. This is the one thing that must NOT be duplicated. My `proposition_layer.py` and the
   Atlas's `PropositionContent` must be the SAME contract.
5. **Tiny convergence contract first (the six: ObjectRef, VersionRef, Envelope, AuthorityVector,
   ObjectDependency, ObjectEvent).** Correct sequencing. Do not block Atlas on essays.

---

## 4. WHAT I NOTICE / POTENTIAL PROBLEMS

### 4a. My devpath4 `proposition_layer.py` is NOT the Atlas's `PropositionContent` shape
My devpath4 Proposition carries `commitment`, `explicitness`, `derived_from`, `grounding`,
`scholarly_corroboration`, wrapped in the existing `DerivedScholarlyObject` (which still has
`content: dict[str, Any]`). The Atlas's `PropositionContent` (tech-arch §29) has `formulation`, `subject`,
`scope`, `modality`, `explicitness`, `speaker_ref`, `assumptions`, `support_scope`.

**These two do NOT currently agree.** This is exactly the duplication the directive warns about. Before
devpath7, I must reconcile my `Proposition` against the Atlas `PropositionContent` — pick ONE field shape.
My current `proposition_text`/`commitment` maps to Atlas `formulation`/`force` (via Commitment), but the
rest differ. **devpath7 is not just "fix the DSO" — it's "align my proposition layer with the Atlas
PropositionContent."**

### 4b. `technical-architecture-v1.md` itself flags the SAME P0 schema issues
It already calls `content: dict[str, Any]` and the scalar `epistemic_ceiling` "P0 schema issues." So the
directive's devpath7 is not a new instruction — it's an already-flagged debt that neither lane has closed.
I should reference §27/§28 of tech-arch-v1 as the authoritative fix spec, not reinvent it.

### 4c. The commitment vocabulary already exists in TWO places
- My `proposition_layer.py` COMMITMENTS tuple
- Atlas tech-arch §30 `CommitmentContent.force`

They match (good) but are two definitions. One should be the source of truth (the Atlas contract, since it
goes to Postgres).

### 4d. The directive's devpath order has a dependency problem
The directive says devpath7 (schema contract) → devpath8 (synthesis). But devpath8's `ArgumentSynthesis`
consumes `PropositionContent`/`CommitmentContent` which are the tech-arch §29-30 shapes — which depend on
the devpath7 fix. So devpath7 is a hard prerequisite, correctly. But devpath7 is "very small" only if we
treat tech-arch-v1 §27-31 as the already-written spec and just implement it. If we re-derive it, it's big.

### 4e. What the directive does NOT mention (gaps)
- **The NAT gate is still pending.** devpath8 synthesis over GOLD arguments is fine, but the directive's
  "real ARGMAP → real propositions → real synthesis" (its §16) still waits on Agent 2. devpath8 can start on
  gold, but its acceptance must not claim real-corpus validity.
- **`ThemeCandidate` promotion** (§6) needs an adjudication path (devpath6's ReviewEvent/Adjudication) —
  the directive gestures at "human/editorial action" but doesn't wire it to the human-authority layer I built.
- **The `ScholarlyContextBundle<T>` profiles** (REVIEW/ESSAY/EDUCATION/AGENT/PUBLIC) — I already have
  `ReviewBundle`; devpath12 makes it `profile=REVIEW`. Good, but the PUBLIC profile needs a
  rights/permission story (Atlas owns rights; Agent 1 does not).
- **No `Attack`/`ArgumentSynthesis` relation vocabulary.** The directive's synthesis JSON uses `relation:
  "ATTACKS"` but doesn't define the relation vocabulary (ATTACKS/SUPPORTS/UNDERMINES/REPLIES_TO). My
  `crux_engine` and the tech-arch don't define it either. devpath8 needs this frozen.

---

## 5. MY VERDICT

**The directive is directionally correct and the `ArgumentSynthesis` focus is exactly right.** But it
understates that:

1. The convergence contract (devpath7) is **already spec'd** in `technical-architecture-v1.md` §27–31 and
   §17 — the work is implementation + **aligning my existing devpath4 proposition layer to it**, not design.
2. The genuinely new object is `ArgumentSynthesis` (devpath8) — it exists nowhere.
3. My devpath4 `proposition_layer.py` and the Atlas `PropositionContent` are currently **two different
   shapes** and must be reconciled FIRST — this is the real devpath7 scope, and it's not "very small."

### The ordering I would actually follow

```text
devpath7  CANONICAL GRAPH CONTRACT
          = implement tech-arch-v1 §27-31 (Pydantic discriminated DSO + vector authority)
          + reconcile my proposition_layer.py -> Atlas PropositionContent
          + freeze the six-object contract (Ref/VersionRef/Envelope/AuthorityVector/Dependency/Event)
          (NOT small, because of the reconciliation)

devpath8  SYNTHESIS CORE
          ResearchQuestion / DebateFrame / Position / ArgumentSynthesis
          + freeze the Attack/synthesis relation vocabulary (ATTACKS/SUPPORTS/UNDERMINES/REPLIES_TO)
          build ONE on the strongest gold (not 100)

devpath9  SYNTHESIS NAT (the mutation suite)  ← my ARGMAP-NAT pattern from devpath1

devpath10 ESSAY COMPILER   (Synthesis -> EssayPlan -> EssayClaim, reuse my EO/SentenceEvidenceAudit)
devpath11 EDUCATION COMPILER (Synthesis -> LearningClaim -> ...)
devpath12 UNIVERSAL BUNDLE  (materialize_context(target, profile); my ReviewBundle = profile=REVIEW)
```

devpath7 is the linchpin and the reconciliation with the existing Atlas spec is the real substance.

---

## 6. THE ONE-LINE CARRY-FORWARD

**The convergence is already designed in `technical-architecture-v1.md` §17/§27–31 — the real next move is
devpath7: implement that contract AND reconcile my devpath4 proposition layer to the Atlas `PropositionContent`,
then devpath8 builds the one object that genuinely doesn't exist yet: `ArgumentSynthesis`.**
