# AGENT 1 × ATLAS CONVERGENCE — the canonical scholarly graph, not a canonical packet

*Peer-review directive for Agent 1 (epistemic core) + Agent 2 (Atlas). 2026-08-13.*

---

## 1. THE CONVERGENCE POINT

**Stop thinking in terms of one final packet as canonical.**

The canonical thing is the **versioned scholarly graph**. Packets are compiled read-models over it.

That distinction resolves the duplication that is surfacing across the lanes.

### What Agent 1 has genuinely built

```text
ARGMAP
  ↓
Proposition
  ↓
Argument
  ↓
Crux
  ↓
ReviewEvent / Adjudication
```

- Proposition layer is real — 34 current proposition objects (real-corpus ARGMAP NAT gate pending).
- Crux layer is real — 15 perturbation-derived cruxes over four gold arguments; Nyāya profile
  explicitly bounded, not treated as truth.
- G4 has the exact human path + `ReviewBundle` — reviews attached to exact versions, zero-write
  impact simulation.

---

## 2. FREEZE THE ARCHITECTURE: one canonical graph, not one canonical packet

```text
PĀṬALA CANONICAL SCHOLARLY GRAPH

LAYER A — AUTHORITY / TEXTUAL IDENTITY
Work
Edition
Witness
Surrogate
EText
Source
ScholarlyWork
Person
Institution

          ↓

LAYER B — TEXT COMPILATION
Passage
T1
L0
ARGMAP
L2
L200
C1
TranslationDecision

          ↓

LAYER C — EPISTEMIC CORE
SourceAssertion
Proposition
Commitment
GroundingLink
InferenceApplication
Argument
Attack
Crux

          ↓

LAYER D — SYNTHESIS
ResearchQuestion
DebateFrame
Position
Theme
ArgumentSynthesis
CruxSet

          ↓

LAYER E — HUMAN AUTHORITY
ReviewEvent
ReviewProposal
Adjudication
PromotionEvent
ImpactReport

          ↓

LAYER F — PROJECTIONS
Essay
Lesson
LearningClaim
VideoScript
Guide
FAQ
AgentAnswer
```

**That graph is the product.**

Everything else:

```text
ReviewBundle
ArgumentBundle
EducationBundle
EssayBundle
AgentContextBundle
```

is a **materialized projection**.

---

## 3. THE MISSING LAYER IS NOW SYNTHESIS

Do **not** jump directly `Argument → essay prose` and independently `Argument → education`,
because that creates two competing interpretation layers.

You need:

```text
Arguments
      ↓
ARGUMENT SYNTHESIS
      ↓
 ┌────┼────────┐
 ▼    ▼        ▼
Essay Lesson  Review
```

That is the convergence object.

### Next milestone: G5 — SYNTHESIS CORE

Minimum objects:

```text
ResearchQuestion
DebateFrame
Position
ArgumentSynthesis
```

with `Theme` as a curated/derived grouping rather than the central object.

---

## 4. WHY `ArgumentSynthesis` IS THE CRUCIAL PARENT OBJECT

Question: *Is recognition fundamentally a recollection of an already-existing self?*

Arguments:

```text
ARG-1 Utpaladeva argument
ARG-2 Abhinavagupta elaboration
ARG-3 Buddhist objection
ARG-4 reply
ARG-5 modern reconstruction
```

Don't let the essay author or lesson compiler independently figure out how those relate.

```json
{
  "type": "ARGUMENT_SYNTHESIS",

  "research_question": "RQ-17",

  "debate_frame": "DF-4",

  "positions": [
    "POS-ŚAIVA",
    "POS-BUDDHIST"
  ],

  "arguments": [
    "ARG-1",
    "ARG-2",
    "ARG-3",
    "ARG-4"
  ],

  "relations": [
    {
      "from": "ARG-3",
      "to": "ARG-1",
      "relation": "ATTACKS"
    }
  ],

  "cruxes": [
    "CRUX-7",
    "CRUX-12"
  ],

  "supported_conclusions": [],
  "open_questions": [],
  "scope_boundaries": [],
  "unresolved_disagreement": []
}
```

This captures: **What is the current best structured understanding of this debate?**

---

## 5. IT IS NOT A "FINAL TRUTH OBJECT"

`ArgumentSynthesis` should NOT say `CONCLUSION = TRUE`.

It says:

```text
under DebateFrame DF4:

Position A has: arguments X/Y
Position B has: objection Z
decisive unresolved crux: CRUX-12
current evidence status: ...
review state: ...
```

That is exactly the philosophy-engine discipline.

---

## 6. THEMES SIT AROUND SYNTHESIS, NOT ABOVE TRUTH

Clustering is not a Theme.

```text
Theme =
a versioned scholarly grouping of propositions/arguments/passages
under an explicit conceptual criterion
```

```json
{
  "theme_id": "THEME-REFLEXIVITY",
  "label": "Reflexive consciousness",

  "selection_rule": {
    "type": "SCHOLARLY_CURATED"
  },

  "members": [
    "PROP-4",
    "PROP-17",
    "ARG-2"
  ],

  "scope": {
    "works": ["IPK", "IPVV"]
  }
}
```

Machine clustering proposes `ThemeCandidate`; human/editorial action promotes it into `Theme`.
Never: `Louvain cluster 6 = canonical doctrine`.

---

## 7. ESSAYS BECOME ALMOST TRIVIAL STRUCTURALLY

```text
ArgumentSynthesis
     ↓
EssayPlan
     ↓
EssayClaim[]
     ↓
SentenceEvidenceAudit
     ↓
Essay
```

An essay isn't allowed to invent its epistemic skeleton. It chooses a presentation over an existing
synthesis.

```json
{
  "essay_claim_id": "EC-7",

  "claim": "...",

  "derived_from": [
    "SYNTH-3",
    "PROP-17"
  ],

  "role": "MAIN_THESIS",

  "compression": "QUALIFIED",

  "source_refs": [],
  "counterevidence_refs": []
}
```

Then prose is generated around `EssayClaim`.

`scholarly graph → essay structure → prose` instead of `LLM writes nice essay → retrofit citations`.

---

## 8. EDUCATION CONSUMES THE SAME SYNTHESIS

```text
ArgumentSynthesis
       ↓
LearningClaim
       ↓
LearningSkill
       ↓
LearningInteraction
```

Same graph, different projection.

Example:
- Essay: explains the disagreement.
- Education: *Which proposition does the Buddhist objection attack? What changes if premise P3 is
  rejected? Which source supports the Śaiva reply?*
- Peer review: *Is the reconstructed reply fair? Is P3 genuinely load-bearing?*

---

## 9. PEER REVIEW CONSUMES THE SAME SYNTHESIS

Extend `ReviewBundle` generically. A scholar reviewing an `ArgumentSynthesis` gets:

```text
ReviewBundle<SYNTH-17>

Question
Positions
Arguments
Propositions
Cruxes
Primary evidence
Secondary scholarship
Machine evaluation
Known disagreement
Downstream: Essays 4, Lessons 3, Videos 1
```

They review the **structured scholarly object underneath all downstream outputs**, not an isolated
prose paragraph.

---

## 10. THE GENERIC MATERIALIZATION INTERFACE: `ScholarlyContextBundle<T>`

Not canonical. A compiled read model.

```json
{
  "schema": "patala.scholar-context.v1",

  "target": {
    "object_id": "...",
    "version_id": "...",
    "type": "ARGUMENT_SYNTHESIS"
  },

  "identity": {},
  "content": {},
  "upstream": {},
  "evidence": [],
  "arguments": [],
  "cruxes": [],
  "scholarship": [],
  "reviews": [],
  "authority": {},
  "dependencies": {},
  "downstream": {},
  "open_questions": []
}
```

Specialized views:

```text
ReviewBundle      = ScholarlyContextBundle + review_actions
EducationBundle   = ScholarlyContextBundle + learning skills/interactions
EssayBundle       = ScholarlyContextBundle + EssayPlan/EssayClaims
AgentContextBundle= ScholarlyContextBundle (token-budgeted)
```

Eventually precompiled + edge-cached for the Atlas API.

---

## 11. ATLAS AND AGENT 1 MUST NOT BOTH DEFINE THESE OBJECTS

Dangerous duplication. Agent 2's Atlas must NOT create argument/review/proposition schemas while
Agent 1 has another version.

### Split (hard boundary)

- **Atlas owns identity + persistence**: Object ID, Version ID, Object type, Payload schema/version,
  Dependencies, Source refs, Authority vector, Hashes, Events, External IDs, Rights.
- **Agent 1 owns epistemic contracts**: What is PropositionContent? CommitmentContent? A Crux? A
  ReviewEvent? An ArgumentSynthesis?
- **Agent 2 persists/materializes them**: Pydantic object → Atlas ScholarlyObjectVersion →
  dependency rows → R2 projection.

---

## 12. THE ATLAS SCHEMA: ONE GENERIC SCHOLARLY-OBJECT REGISTRY

Don't add `proposition/argument/crux/review/essay/lesson` as parallel Atlas schemas immediately.

```sql
scholarly_object (
    id UUID PRIMARY KEY,
    object_type TEXT NOT NULL,
    canonical_work_id UUID,
    created_at TIMESTAMPTZ
);

scholarly_object_version (
    id UUID PRIMARY KEY,
    object_id UUID NOT NULL,
    schema_name TEXT NOT NULL,
    schema_version TEXT NOT NULL,
    payload JSONB NOT NULL,
    payload_hash BYTEA NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    supersedes_version_id UUID
);

object_dependency (
    consumer_version_id UUID,
    dependency_version_id UUID,
    relation TEXT,
    load_bearing BOOLEAN,
    epistemic_role TEXT
);
```

That is where the two worlds meet.

---

## 13. TYPED PYDANTIC CONTRACTS REMAIN OUTSIDE POSTGRES

Agent 1 defines:

```python
PropositionContent
ArgumentContent
CruxContent
ArgumentSynthesisContent
ReviewEventContent
LearningClaimContent
EssayClaimContent
```

Pydantic validates them. Atlas stores `schema_name`, `schema_version`, validated payload.
The DB does not reimplement every philosophical invariant.

---

## 14. WHICH COMES FIRST: ATLAS SCHEMA OR SYNTHESIS?

Tiny convergence contract first, then both proceed independently. Do not block Atlas for two weeks.

Freeze only these six:

```text
CanonicalObjectRef
CanonicalVersionRef
ScholarlyObjectEnvelope
AuthorityVector
ObjectDependency
ObjectEvent
```

Then:
- Agent 2 → implements storage/API
- Agent 1 → implements new semantic types

Every new Agent 1 object automatically fits the same Atlas registry.

---

## 15. WHAT AGENT 1 SHOULD DO NEXT (the devpath sequence)

### devpath7 — CANONICAL GRAPH CONTRACT (very small)
Agent 1 + Atlas agree on: ObjectId, VersionId, object_type, schema_name, schema_version,
payload_hash, derived_from, source_refs, authority, dependency.
Fix the current DSO issue: `content: dict[str, Any]` → typed Pydantic discriminated union.
Remove scalar authority as canonical. **The last schema-unification task.**

### devpath8 — SYNTHESIS CORE
Build `ResearchQuestion`, `DebateFrame`, `Position`, `ArgumentSynthesis`.
Input: Propositions, Arguments, Attacks, Cruxes, SourceAssertions.
Output: one structured debate object. Start with the strongest gold. One, not 100 themes.

### devpath9 — SYNTHESIS NAT / adversarial tests
Mutation suite: POSITION_COLLAPSE, RIVAL_AS_CONSENSUS, CRUX_OMISSION, SCOPE_INFLATION,
ARGUMENT_DIRECTION_REVERSAL, UNRESOLVED_AS_RESOLVED, COUNTEREVIDENCE_DROP,
SCHOLAR_ATTRIBUTION_COLLAPSE. Proof that synthesis hasn't destroyed the lower argument graph.

### devpath10 — ESSAY COMPILER
`ArgumentSynthesis → EssayPlan → EssayClaim`. Reuse SentenceEvidenceAudit, EO-v2, prose-faithfulness.
Prose generation only after EssayClaim is structurally grounded.

### devpath11 — EDUCATION COMPILER
`ArgumentSynthesis → LearningClaim → LearningSkill → LearningInteraction`.
First interaction set: speaker attribution, premise attach, warrant reconstruction, crux
identification, counterevidence.

### devpath12 — UNIVERSAL BUNDLE COMPILER
`materialize_context(target_version, profile)`.
Profiles: REVIEW, ESSAY, EDUCATION, AGENT, PUBLIC.
`ReviewBundle` becomes `profile=REVIEW`.

---

## 16. WHEN AGENT 2 FINALLY UNBLOCKS devpath2/3

No redesign. Replace the synthetic/gold corpus underneath:

```text
real Agent2 ARGMAP
↓ ARGMAP NAT
↓ real propositions
↓ real arguments
↓ real cruxes
↓ real synthesis
↓ real essays/education/reviews
```

---

## 17. THE EXACT FINAL COMPILER ARCHITECTURE

```text
                              ATLAS
                    identity / provenance / bytes
                                │
                                ▼
SOURCE → T1 → L0 → ARGMAP → L2 → L200 → C1
                                │
                                ▼
                         PROPOSITIONS
                                │
                 ┌──────────────┼────────────┐
                 ▼              ▼            ▼
            Commitments     Grounding     SourceAssertions
                 │              │            │
                 └──────────────┼────────────┘
                                ▼
                           ARGUMENTS
                                │
                      attacks / replies
                                │
                                ▼
                             CRUXES
                                │
                                ▼
                       ARGUMENT SYNTHESIS
                 question / frame / positions
                 evidence / dispute / cruxes
                                │
              ┌─────────────────┼──────────────────┐
              ▼                 ▼                  ▼
          EssayPlan        LearningClaim       ReviewBundle
              │                 │                  │
          EssayClaim       Interactions          Scholar
              │                 │                  │
            Essay             Course          Adjudication
              │                 │                  │
              └─────────────────┼──────────────────┘
                                ▼
                         downstream graph
```

---

## 18. THE DEEPEST RULE

There is **no separate essay truth**, **no separate education truth**, **no separate reviewer
truth**.

There is one canonical scholarly graph, then different projections with different purposes and
permissions.

The single most important new object between the current argument work and all of those products is:

# `ArgumentSynthesis`

not a mega-packet.

Then the generic `ScholarlyContextBundle` makes that graph fast and usable by humans, agents, essays,
education, and review.

**Devpath7 = canonical object convergence contract; devpath8 = ArgumentSynthesis.** Agent 2 can
implement Atlas storage against that contract in parallel. That is where the two lanes finally snap
together.
