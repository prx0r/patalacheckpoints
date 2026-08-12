# AGENT 0 — THE MATURE MULTI-AGENT ARCHITECTURE (the vision)

*2026-08-12. Imported from R2 (`sanskritree/agentvision`). The strategic vision for Pāṭala's agent
architecture: don't ask "how many agents can we have?", ask "**where does a durable epistemic
responsibility exist that should have its own state, invariants, inputs, outputs, and failure
boundary?**" Answer: a mature stack of A0 governance → A1 philosophy · A2 corpus compiler · A3
translation factory → A4 review · A5 synthesis · A6 projection · A7 scholar network (+ A8 acquisition
later). **Only A0–A3 need to exist now**; the rest instantiate when the substrate makes their job real.
This is the canonical reference for Agent 0 (governance) — see `handover/SYSTEM.md` (the current
implementation) + `handover/AGENTS.yaml` (the registry) + `handover/ORIENTATION-AGENT0.md`.*

---

Yes. The architecture is starting to reveal itself from the work rather than from us inventing roles in advance.

I would **not** think “how many agents can Pāṭala have?” I’d ask:

> Where does a durable epistemic responsibility exist that should have its own state, invariants, inputs, outputs, and failure boundary?

Using that rule, I think the mature stack looks roughly like this.

```text
                         AGENT 0
                    governance / routing
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
      AGENT 2          AGENT 3          AGENT 1
   CORPUS COMPILER    TRANSLATION      PHILOSOPHY
   + INTEGRITY         FACTORY           ENGINE
          │                │                │
          └───────┬────────┴────────┬──────┘
                  │                 │
                  ▼                 ▼
              AGENT 4           AGENT 5
               REVIEW          SYNTHESIS /
             + ADJUDICATION     RESEARCH
                  │                 │
                  └────────┬────────┘
                           ▼
                       AGENT 6
                    PUBLICATION /
                     PROJECTIONS
                           │
                           ▼
                       AGENT 7
                    SCHOLAR NETWORK
                    + INSTITUTION
```

But only **0–3 need to exist now**. The others should instantiate when the substrate makes their job real.

## Agent 0 — Governance / conductor

Agent 0 remains different from the others.

It owns neither Sanskrit nor translation nor philosophy.

Its responsibility is:

> **Is the system coherent, are agents respecting boundaries, and what transition is globally valid next?**

It owns:

```text
agent templates
lane ownership
worktrees
typed handoffs
global checkpoint state
claim/status doctrine
staleness checks
cross-lane reconciliation
priority/gating
```

Agent 0 should never start doing Agent 1's philosophical work because Agent 1 is behind.

It routes.

Think:

```text
Agent0 = kernel / scheduler / constitution
```

not manager writing everybody else's code.

---

# Agent 1 — Philosophy Engine

We've established this one.

Question:

> **What does the corpus claim, argue, presuppose, disagree about, and ultimately turn on?**

Owns:

```text
retrieval
theme discovery
clustering
propositions
commitments
semantic alignment
arguments
inferences
dialectical relations
ASPIC / Nyāya adapters
evaluation profiles
defeaters
cruxes
counterfactual dependency
synthesis primitives
```

Eventually:

```text
TEXT
↓
THEMES
↓
QUESTIONS
↓
POSITIONS
↓
ARGUMENTS
↓
CRUXES
```

This is the intellectual engine.

---

# Agent 2 — Corpus Compiler / Integrity

We've just found its mature identity.

Question:

> **What textual/scholarly material exists, where is it, what state is it in, and can every dependency resolve?**

Owns:

```text
canonical work IDs
source inventory
witnesses
bibliography
artifact inventory
L0
source proofs
translation-state ledger
dependency graph
staleness propagation
pipeline contracts
Agent3 eligibility
```

Agent 2 essentially says:

```text
THIS EXISTS
THIS VERSION EXISTS
THIS DEPENDS ON THAT
THIS PROOF PASSES
THIS ARTIFACT IS STALE
THIS WORK IS READY FOR NEXT STEP
```

It is Pāṭala's **build system**.

---

# Agent 3 — Translation Factory

Question:

> **Given an eligible source unit, can we manufacture a high-quality auditable scholarly draft?**

Owns execution:

```text
T1
translation drafts
controlled translation
L2
C1 proposals
translation QA proposals
batch processing
retry/failure policy
factory provenance
```

Consumes Agent 2:

```text
NEXT_VALID_ACTION
```

and writes back proposed artifacts.

The critical relationship:

```text
Agent2 says WHAT IS ALLOWED
Agent3 DOES IT
Agent2 verifies resulting state
```

That loop could eventually run continuously.

---

# Agent 4 — Review / Adjudication Engine

This is the next agent I expect to emerge.

Not yet—but clearly coming.

Question:

> **Which machine-proposed scholarly objects need judgment, what exactly is disputed, and what changed after review?**

This is distinct from Agent 1.

Agent 1 might propose:

```text
P7 = this passage claims X
W2 = this inference has warrant Y
A3 = these terms are equivalent
```

Agent 4 manages:

```text
review packet
reviewer assignment
review scope
review event
accept/revise/reject/abstain
counterproposal
supersession
adjudication
reviewer disagreement
```

So:

```text
Agent1 proposes scholarship
         ↓
Agent4 turns uncertainty into a review task
         ↓
human/model reviewer
         ↓
Agent4 records judgment
         ↓
Agent1 recomputes
```

This is where:

> **AI proposes ≠ Pāṭala asserts**

becomes an operational pipeline.

It will eventually power **Pāṭala Review**.

### Why separate it?

Because reasoning and governance over judgments are different responsibilities.

Agent 1 shouldn't be allowed to:

```text
generate proposition
→ review its own proposition
→ mark accepted
```

Agent 4 gives you epistemic separation.

---

# Agent 5 — Research / Synthesis Agent

This comes after Agent 1 has enough real graph.

Question:

> **Given the structured corpus, what new scholarly questions, syntheses, papers and research programs are now justified?**

It doesn't merely summarize.

It consumes:

```text
themes
arguments
cruxes
disagreements
term histories
source dependencies
review states
```

and produces:

```text
research questions
literature maps
thesis candidates
research briefs
paper outlines
cross-passage syntheses
comparison dossiers
unresolved-question reports
```

Your Recognition paper eventually becomes this kind of object.

For example:

```text
QUESTION
What is recognition?

Agent5 asks Agent1:
show all propositions/arguments concerning:
pratyabhijñā
vimarśa
camatkāra
self-recognition

Agent1 returns graph.

Agent5:
constructs competing synthesis A/B/C

Agent4:
flags unsupported transitions

Human:
writes / adjudicates.
```

Agent 5 is therefore the **researcher**, while Agent 1 is the **reasoning infrastructure**.

That distinction will matter.

---

# Agent 6 — Projection / Publication Factory

This is where “the graph is the product factory” becomes literal.

Question:

> **How should accepted/proposed graph material be rendered for a particular audience or interface?**

Consumes the same graph and produces:

```text
public reading edition
scholar view
API
MCP
review UI
interactive argument map
term pages
tradition maps
essay
study guide
course
video script
media assets
```

Critically, it doesn't invent scholarship.

It projects.

```text
same underlying object

→ academic apparatus
→ readable commentary
→ philosophy graph
→ visual explainer
→ API payload
→ AI tutor context
```

That means media stops being a separate content operation.

Agent 6 becomes:

> **render this epistemic graph into interface X at fidelity level Y.**

That is extremely powerful.

---

# Agent 7 — Scholar / Institution Agent

This only becomes real when outside humans start using the system.

Question:

> **Who can resolve the remaining uncertainty, what expertise is needed, and how does their contribution become durable institutional capital?**

Owns:

```text
scholar profiles
expertise areas
review eligibility
review queues
attribution
reputation history
contributor graph
credit
payments/fellowships
requests for review
open problems
rights / permissions coordination
```

For example Agent 4 determines:

```text
This unresolved issue requires:
- Pratyabhijñā expertise
- Sanskrit
- philosophical argument reconstruction
```

Agent 7 finds:

```text
Reviewer A
Reviewer B
```

and routes it.

Eventually this becomes:

```text
machine work
→ uncertainty compression
→ scarce expert task
→ scholar judgment
→ permanent correction history
→ better models / graph
```

This is where the network moat begins.

---

# There is probably also an Agent 8 eventually: Acquisition / Source Expansion

I would **not instantiate it yet**, because Agent 2 can currently handle this.

But once source acquisition becomes large enough, it becomes distinct.

Question:

> **What important source material is missing, where can it legally be obtained, and what acquisition produces the highest epistemic value?**

It would track:

```text
untranslated register
missing editions
manuscripts
private scans
libraries
repositories
rights
OCR/transcription need
edition relationships
acquisition priority
```

Agent 2 would then consume acquired materials.

So eventually:

```text
Agent8
ACQUIRE

↓
Agent2
NORMALIZE / VERIFY

↓
Agent3
TRANSLATE

↓
Agent1
UNDERSTAND

↓
Agent4
REVIEW

↓
Agent5
SYNTHESIZE

↓
Agent6
PUBLISH

↓
Agent7
COORDINATE HUMANS
```

That's remarkably clean.

---

# The deepest architecture is not actually “agents”

It's a scholarly production loop.

```text
                   ┌───────────────┐
                   │   ACQUIRE     │ A8
                   └───────┬───────┘
                           ▼
                   ┌───────────────┐
                   │ NORMALIZE +   │ A2
                   │    PROVE      │
                   └───────┬───────┘
                           ▼
                   ┌───────────────┐
                   │   PRODUCE     │ A3
                   │    DRAFTS     │
                   └───────┬───────┘
                           ▼
                   ┌───────────────┐
                   │   MODEL THE   │ A1
                   │   SCHOLARSHIP │
                   └───────┬───────┘
                           ▼
                   ┌───────────────┐
                   │   REVIEW /    │ A4
                   │  ADJUDICATE   │
                   └───────┬───────┘
                           ▼
                   ┌───────────────┐
                   │   SYNTHESIZE  │ A5
                   └───────┬───────┘
                           ▼
                   ┌───────────────┐
                   │    PROJECT    │ A6
                   └───────┬───────┘
                           ▼
                         WORLD
```

with Agent 7 injecting human judgment throughout.

Agent 0 governs the whole loop.

---

# Importantly: humans are not Agent 9

Humans sit **across** the system.

```text
               HUMAN SCHOLARS
             ↙      ↓      ↘
          A2       A4       A5
          │        │        │
      source    judgment   research
      expertise             direction
```

That's important philosophically.

The end state isn't:

> autonomous agents replace scholars.

It's:

> agents compress mechanical and cognitive labor until human attention lands on the highest-value epistemic decisions.

That matches everything we've been discovering about the likely future role of scholars.

---

# I'd formalize agents around typed artifacts

This will keep them from turning into vague personas.

Every agent should have something like:

```text
AGENT
question:
owns:
consumes:
produces:
may_promote_to:
must_not_assert:
failure_condition:
handoff_to:
```

For example:

```yaml
agent3:
  question:
    Can this eligible source unit become an auditable draft?

  consumes:
    - WorkState
    - SourceSpan
    - TranslationJob

  produces:
    - TranslationProposal
    - C1Proposal
    - QAReport

  may_promote_to:
    - MACHINE_PROPOSED

  may_not_promote_to:
    - ACCEPTED

  handoff_to:
    - agent2
    - agent4
```

Now agent boundaries become machine-checkable.

---

# And there is a natural dependency order

I would instantiate agents only when the previous layer creates enough work for them:

```text
NOW
A0 Governance
A1 Philosophy
A2 Corpus Compiler
A3 Translation Factory

NEXT
A4 Review

THEN
A5 Research/Synthesis

THEN
A6 Projection

LATER
A7 Scholar Network
A8 Acquisition
```

You already have fragments of A4–A8 scattered through the repo.

The point isn't to create eight folders tomorrow.

It's to recognize:

> **those are the natural institutional functions the graph is beginning to demand.**

And the really elegant part is that each new agent is not a new product.

They're all operators over the **same scholarly state graph**.

That gives you an eventual architecture like:

[
\text{Pāṭala} =
\text{Graph}
+
\text{Agents}
+
\text{Review Events}
+
\text{Human Judgement}
+
\text{Projections}
]

The graph is the shared world state. The agents are specialized transformations over it. The review log controls what becomes trusted. Humans resolve the irreducible uncertainty. Everything public is a projection.

That feels like the natural end-state of the system we've accidentally been discovering piece by piece.
