# hermespatalalayers.md

Yes. The right end-state is **skills per epistemic layer, one shared controller, and a scheduler that advances objects only when their prerequisites and gates are satisfied**.

I would **not** make each cron job directly trigger the next cron job. That becomes fragile very quickly. The cleaner architecture is:

```text
                     ┌─────────────────────┐
                     │  SCHEDULER / CRON   │
                     │  wakes controller   │
                     └──────────┬──────────┘
                                ↓
                     ┌─────────────────────┐
                     │ AUTONOMY CONTROLLER │
                     │ inspect registries  │
                     │ find eligible work  │
                     └──────────┬──────────┘
                                ↓
              ┌─────────────────────────────────┐
              │      CANONICAL STACK DAG        │
              │                                 │
SOURCE ──→ L0/L1 ──→ L2 ──→ L200 ──→ C1       │
                                  │      │       │
                                  │      ↓       │
                                  │    THEME     │
                                  │      ↓       │
                                  └──── ESSAY    │
                                         ↓       │
                                     EDUCATION   │
              └─────────────────────────────────┘
```

Cron should mean:

> “wake up, inspect canonical state, advance whatever is safely eligible.”

Not:

> “L0 cron finished, therefore shell-call L2 cron, therefore shell-call L200 cron…”

That distinction matters.

## The core architecture

There should be **one reusable autonomous runtime** and **one skill per layer**.

The reusable runtime owns only generic mechanics:

```text
locking
stable IDs
input hashes
eligibility
queues
batching
model calls
timeouts
retry/split
validation dispatch
immutable commit
supersession
failure state
run reports
cost accounting
```

The layer skill owns epistemology:

```text
what inputs are allowed?
what may the model infer?
what output schema is required?
what counts as an unsupported addition?
what validator runs?
what uncertainty must survive?
what blocks downstream release?
what certificate is required?
```

That division is the key.

---

# I would model each layer as a typed compiler pass

Think LLVM more than “agents chatting.”

Each stage consumes a defined IR and emits another.

### L0/L1 — philological compiler

```text
SOURCE
↓
exact spans
tokens
morphology witnesses
controlled translation
```

Skill:

```text
skills/patala-l0-l1/SKILL.md
```

Hard invariants:

* byte/span losslessness;
* exact source hash;
* stable passage ID;
* avagraha preserved;
* OCR corruption never guessed;
* morphological/model uncertainty explicit;
* no doctrinal supplementation.

This is where the factory is currently being hardened.

---

### L2 — reading compiler

Question:

> **What does the text say in readable English?**

Input should be L1 + source links.

Output:

```text
L2 paragraph/sentence
→ exact L1 refs
→ exact L0/source refs
```

The important invariant is:

[
content(L2) \subseteq content(L1) + declared_supplies
]

A readability model can restructure language aggressively, but every substantive clarification beyond the controlled layer becomes explicit.

The L2 skill therefore needs a **semantic-fidelity validator**, not merely English style checks.

---

# L200 is probably the most important autonomous skill

This is where the architecture gets distinctive.

L200 answers:

> **How exactly did we get from the source to this published reading?**

That should not just be another generative prompt.

It should be a partly deterministic **audit compiler**.

Given L2 + upstream objects, construct:

```text
0 Identification
1 Published Reading

2 Derivation Map
  L2 sentence
     ↓
  argument/read-map unit
     ↓
  L1
     ↓
  L0 span
     ↓
  Sanskrit source span

3 Material Translation Decisions
  SUPPLIED
  REFERENT_SUPPLY
  STRUCTURAL_CONNECTIVE
  LEXICAL
  GRAMMATICAL

4 Interpretive Assertions

5 Source Layer

6 Typed Cross-references

7 Open Items

8 Review State
```

The skill should generate only the parts that cannot be deterministically reconstructed.

For example:

```text
DERIVATION MAP
→ mostly deterministic

source hashes
→ deterministic

upstream IDs
→ deterministic

review history
→ deterministic

candidate MaterialTranslationDecision classification
→ model proposal

candidate InterpretiveAssertion
→ model proposal

open item detection
→ model proposal + validator
```

That is a big architectural principle:

> **Do not use the LLM to regenerate things the graph already knows.**

L200 should become the **proof object of the translation stack**.

---

# Then C1 becomes much cleaner

C1 answers:

> **What is being said here? What does this passage mean?**

It should consume:

```text
SOURCE
L0/L1
L2
L200
```

but crucially, it should probably reason **primarily through L200**, because L200 already distinguishes:

```text
translation decision
≠
interpretive assertion
≠
source-layer attribution
≠
cross-reference
≠
open question
```

That means C1 no longer has to reverse-engineer those distinctions from prose.

Architecture:

```text
                 L200
           ┌──────┼───────┐
           ↓      ↓       ↓
          MT      IA     OPEN
           \       |      /
            \      |     /
             ↓     ↓    ↓
                  C1
```

C1 then produces passage-local hermeneutics and **machine proposals only**.

It can also emit:

```text
TranslationChallenge
InterpretiveAssertionChallenge
ResearchQuestion
ParallelCandidate
TermSenseProposal
```

But it should never rewrite upstream objects itself.

---

# Theme should not just be “run clustering after C1”

This is where the Agent 1 work becomes useful.

Theme should consume a graph of accepted/proposed C1 assertions, not merely text embeddings.

Something like:

```text
C1 assertions
+
term senses
+
cross-references
+
local arguments
+
speaker/position
+
L200 provenance
        ↓
candidate thematic structure
```

There should probably be several proposal engines:

```text
deterministic:
- k-core
- explicit cross-ref connectivity
- recurring term/sense
- argument dependency

heuristic:
- Louvain/community
- semantic similarity
- PPR neighborhoods

neural:
- BGE/ColBERT eventually
```

and then a `THEME` skill synthesizes those signals into:

```json
{
  "theme_id": "...",
  "label": "...",
  "member_claims": [],
  "development": [],
  "counterexamples": [],
  "edge_evidence": [],
  "status": "MACHINE_PROPOSED"
}
```

Not:

> cluster = theme.

That distinction remains essential.

---

# ESSAY should consume arguments, not C1 prose

This is another place I'd be strict.

Bad architecture:

```text
all C1 commentary
↓
LLM
↓
essay
```

Better:

```text
THEME
↓
ResearchQuestion
↓
candidate relevant propositions
↓
local Arguments
↓
ArgumentSynthesis
↓
SynthesisAudit
↓
EssayPlan
↓
Essay
↓
SentenceEvidenceAudit
```

So the Agent 1 stack becomes the **ESSAY compiler**.

That means Agent 1's work was not a separate side project. It belongs here:

```text
L200
↓
C1
↓
THEME
↓
ARGUMENT
↓
ARGUMENT SYNTHESIS
↓
ESSAY
```

The essay skill itself should not do philosophical reasoning from scratch.

It should render an already structured synthesis.

---

# EDUCATION is another projection

Education should come **after** the scholarly object.

Not:

```text
source → AI lesson
```

but:

```text
reviewed/qualified claims
↓
lesson plan
↓
explanation
↓
quiz
↓
visualization
```

The authority of the educational rendering cannot exceed its source object.

So:

[
authority(Education(x)) \le authority(x)
]

Same invariant all the way up.

---

# I would give every layer three distinct states

This is important.

Do not just use:

```text
DONE / NOT DONE
```

Use:

```text
GENERATED
VALIDATED
REVIEWED
```

For example:

```text
L200_GENERATED
L200_ENGINEERING_VALIDATED
L200_SPECIALIST_REVIEWED
```

because downstream eligibility depends on the use case.

An experimental C1 might be allowed to consume:

```text
L200_ENGINEERING_VALIDATED
```

while public publication might require:

```text
L200_SPECIALIST_REVIEWED
```

That lets the same graph serve research, staging and publication without lying about authority.

---

# Cron architecture

I would use cron only as the **heartbeat**.

Something like:

```text
*/15 * * * * patala-autonomy tick
```

or hourly initially.

`tick` does:

```text
1. acquire global/controller lock
2. inspect registries
3. calculate eligible jobs
4. score priority
5. claim bounded jobs
6. dispatch appropriate skill
7. validate
8. commit
9. record failures/review-needed
10. stop
```

Then next tick continues.

No endless loop required.

No agent needs to “remember where it was.”

The registries remember.

---

# Eligibility is the real engine

Each stage gets a deterministic predicate.

Example:

```python
eligible_for_l2(passage):
    return (
        l1_committed(passage)
        and not l2_current_for(l1_version)
        and not source_blocked(passage)
    )
```

L200:

```python
eligible_for_l200(passage):
    return (
        l2_committed(passage)
        and upstream_refs_complete(passage)
        and not l200_current_for(l2_version)
    )
```

C1:

```python
eligible_for_c1(passage):
    return (
        l200_engineering_validated(passage)
        and not c1_current_for(l200_version)
    )
```

Theme:

```python
eligible_for_theme(work):
    return enough_c1_coverage(work) and theme_inputs_changed(work)
```

Essay:

```python
eligible_for_essay(question):
    return (
        research_pack_complete(question)
        and argument_synthesis_exists(question)
        and synthesis_audit_exists(question)
    )
```

This is far safer than agents triggering agents.

---

# Use queues, but don't make the queue authoritative

A queue is useful for scheduling.

But canonical truth remains registries/object versions.

Architecture:

```text
REGISTRY = truth
QUEUE    = work request/cache
RUN LOG  = execution history
```

A queue item can disappear and be rebuilt.

A committed scholarly object cannot.

---

# Each layer should have its own registry

I would do roughly:

```text
registries/
  source-registry.jsonl
  l0-registry.jsonl
  l1-registry.jsonl
  l2-registry.jsonl
  l200-registry.jsonl
  c1-registry.jsonl
  theme-registry.jsonl
  argument-registry.jsonl
  synthesis-registry.jsonl
  essay-registry.jsonl
  education-registry.jsonl
```

Eventually SQLite is probably better operationally, but the conceptual model should stay immutable/versioned.

Each record:

```json
{
  "object_id": "...",
  "layer": "L200",
  "input_refs": ["..."],
  "input_hash": "...",
  "version": 3,
  "status": "ENGINEERING_VALIDATED",
  "created_by": "...",
  "created_at": "...",
  "supersedes": "...",
  "review_events": []
}
```

---

# One particularly powerful idea: cascading invalidation without destructive mutation

Suppose a Sanskritist changes L1.

You should not manually repair every layer.

Instead:

```text
L1 v4 supersedes L1 v3
↓
L2 v2 depends on L1 v3 → STALE
↓
L200 v1 depends on L2 v2 → STALE
↓
C1 v3 → STALE
↓
theme proposal → STALE
↓
essay synthesis → potentially STALE
```

Then cron naturally rebuilds downstream proposals.

This is the killer feature of the architecture.

But importantly:

> old objects remain historically available.

So you get a full scholarly correction history.

---

# The highest-level architecture I'd aim for

```text
                 ┌──────────────────────────┐
                 │      SOURCE CORPUS       │
                 └────────────┬─────────────┘
                              ↓
                 ┌──────────────────────────┐
                 │       L0 / L1            │
                 │ philological substrate   │
                 └────────────┬─────────────┘
                              ↓
                 ┌──────────────────────────┐
                 │         L2 READ          │
                 │ publishable reading      │
                 └────────────┬─────────────┘
                              ↓
                 ┌──────────────────────────┐
                 │       L200 AUDIT         │
                 │ derivational proof       │
                 └────────────┬─────────────┘
                              ↓
                 ┌──────────────────────────┐
                 │           C1             │
                 │ passage interpretation   │
                 └────────────┬─────────────┘
                              ↓
              ┌───────────────┴────────────────┐
              ↓                                ↓
       ┌──────────────┐                 ┌──────────────┐
       │    THEMES    │                 │  ARGUMENTS   │
       │ development  │                 │ local logic  │
       └──────┬───────┘                 └──────┬───────┘
              └───────────────┬────────────────┘
                              ↓
                 ┌──────────────────────────┐
                 │   ARGUMENT SYNTHESIS     │
                 │ cruxes + epistemic ceil  │
                 └────────────┬─────────────┘
                              ↓
                 ┌──────────────────────────┐
                 │          ESSAY           │
                 │ proof-carrying prose     │
                 └────────────┬─────────────┘
                              ↓
                 ┌──────────────────────────┐
                 │       EDUCATION          │
                 │ lesson/video/explainer   │
                 └──────────────────────────┘
```

Underneath **every box**:

```text
SKILL
SCHEMA
REGISTRY
VALIDATOR
CERTIFICATE
RUN LOG
REVIEW EVENTS
```

Above every box:

```text
ONE CONTROLLER
ONE SCHEDULER
```

That is the architecture.

---

# The bit I think becomes the actual moat

Not any individual model.

Not even the translation.

It's this:

```text
scholar changes one judgment
        ↓
exact object superseded
        ↓
dependency graph knows what changed
        ↓
affected interpretations become stale
        ↓
themes/arguments/syntheses re-evaluate
        ↓
essay wording changes automatically
        ↓
education output updates
        ↓
full history remains citable
```

That's the thing Academia, generic RAG systems, and normal translation projects do not naturally give you.

It makes the **scholarly judgment itself executable**.

---

# Practical build order

I would not build all skills at once.

Do:

```text
1. finish generic controller at L0
2. prove crash/idempotency/certificate
3. L2 skill
4. L200 skill — spend serious effort here
5. C1 skill
6. correction/supersession propagation
7. THEME skill
8. connect existing Argument/ArgumentSynthesis
9. ESSAY skill
10. EDUCATION projections
11. only then optimize throughput/models
```

And I would make one **single passage** go all the way:

```text
SOURCE
→ L0
→ L1
→ L2
→ L200
→ C1
→ Theme
→ Argument
→ Synthesis
→ Essay
→ Lesson
```

Then mutate one upstream translation decision and prove the change propagates correctly.

That is probably the next truly killer vertical after the Agent 1 demo.

The end-state is therefore less “a bunch of cron agents” and more:

> **a continuously running scholarly build system, where skills are compiler passes, registries are canonical state, validators are type/epistemic checks, cron merely wakes the scheduler, and human judgments create versioned events that automatically invalidate and regenerate downstream knowledge.**
