I researched this as an engineering problem rather than “find some graph libraries.” The cleanest conclusion is that Pāṭala should **not** have one giant AI graph. It should have an immutable interaction/event stream feeding several graph/model projections, each optimized for a different question.

The strongest reusable architecture I found is:

```text
                         RAW USER EVENTS
                chat / quiz / read / watch / search
                 save / objection / comparison / etc.
                              │
                              ▼
                     INTERACTION LEDGER
                  immutable + consent scoped
                              │
           ┌──────────────────┼──────────────────┐
           ▼                  ▼                  ▼
      USER TEMPORAL       LEARNER MODEL      QUESTION/GAP
          GRAPH               GRAPH             GRAPH
           │                  │                  │
           └──────────────┬───┴───────┬──────────┘
                          ▼           ▼
                   PEDAGOGY POLICY   DISCOVERY POLICY
                          │           │
                          ▼           ▼
                   next intervention research priority
                          │           │
                          ▼           ▼
                         USER      AI RESEARCH
                                      │
                                      ▼
                                REVIEW / VERIFY
                                      │
                                      ▼
                                  TRUTH GRAPH
                                      │
                    ┌─────────────────┼──────────────┐
                    ▼                 ▼              ▼
                  lesson             essay          video
                    │                 │              │
                    └─────────────────┼──────────────┘
                                      ▼
                                    USERS
```

The pieces for this already exist across several research communities. Here's what I would directly reuse.

---

# 1. Graphiti — use this for the **temporal user graph**

This is probably the single most immediately reusable graph project.

**GitHub**

[https://github.com/getzep/graphiti](https://github.com/getzep/graphiti)

**Paper**

[https://arxiv.org/abs/2501.13956](https://arxiv.org/abs/2501.13956)

Graphiti incrementally converts episodes such as conversations and structured events into a temporal graph. Critically, it preserves the underlying episodes as provenance and gives relationships validity periods instead of overwriting history. It also combines semantic, keyword and graph retrieval. ([GitHub][1])

That maps almost perfectly to:

```text
Episode:
"user asked about vimarśa"

↓

Derived facts:

INTERESTED_IN(user, vimarśa)
ASKED(user, Q-991)
CONFUSED_ABOUT(user, C-112)
```

Then three months later:

```text
UNDERSTANDS(user, C-112)
```

You don't destroy the old state.

You know:

```text
valid_from
valid_until
source_episode
```

### What I would steal

Use its ideas/code for:

```text
Episode
Entity
TemporalFact
valid_at
invalid_at
source_episode_ids
hybrid retrieval
custom Pydantic entity types
```

Graphiti even exposes MCP tooling, so conceptually it fits Pāṭala's existing MCP architecture. ([GitHub][2])

### What I would NOT use it for

Don't let Graphiti decide:

```text
mastery(vimarśa)=0.82
```

That's a statistical educational state, not ordinary conversational memory.

Keep that separate.

---

# 2. pyBKT — use this as the first **formal learner state model**

**GitHub**

[https://github.com/CAHLR/pyBKT](https://github.com/CAHLR/pyBKT)

pyBKT estimates latent mastery from sequences of observed learner interactions and explicitly models learning, forgetting, guessing and mistakes. It also supports different learning rates for different resources/items. ([GitHub][3])

So Pāṭala starts with something interpretable:

```text
LearnerConceptState

concept_id: vimarsa

P_mastery: 0.61
P_learn:   0.17
P_forget:  0.03
P_guess:   0.08
P_slip:    0.11
```

Then evidence updates it.

But Pāṭala observations can be richer than normal educational questions:

```text
MCQ correct                  weak/medium evidence
argument reconstruction      strong evidence
source matching              strong evidence
teach-back                   strong evidence
follow-up confusion          negative evidence
novel transfer problem       very strong evidence
```

### Important Pāṭala adaptation

Don't have one hidden state called:

```text
knows vimarśa
```

Have components:

```text
definition
distinction_from_prakasa
role_in_argument
source_recognition
transfer
comparative_distinction
```

That becomes much more informative.

---

# 3. pyKT — eventually benchmark models rather than marrying BKT

**GitHub**

[https://github.com/pykt-team/pykt-toolkit](https://github.com/pykt-team/pykt-toolkit)

pyKT is a benchmarking toolkit containing many knowledge-tracing architectures, including DKT, DKVMN, GKT, SAKT, AKT and others. ([GitHub][4])

This matters because after Pāṭala accumulates actual longitudinal learning data, we can ask empirically:

```text
Which model predicts future understanding best?

BKT?
AKT?
GKT?
DKT?
our own model?
```

Don't decide this in 2026 based on aesthetics.

Build a standard event schema now so these models can later consume exactly the same traces.

---

# 4. GRKT/GKT — directly relevant because Pāṭala concepts already form a graph

### GRKT paper

[https://arxiv.org/abs/2406.12896](https://arxiv.org/abs/2406.12896)

### GRKT GitHub

[https://github.com/JJCui96/GRKT](https://github.com/JJCui96/GRKT)

### older GKT GitHub

[https://github.com/jhljx/GKT](https://github.com/jhljx/GKT)

GKT-style models propagate learner-state information over relationships between knowledge concepts rather than treating each knowledge component independently. GRKT goes further by explicitly modeling retrieval, strengthening, learning and forgetting over the knowledge graph. ([arXiv][5])

This is much closer to Pāṭala.

Suppose someone demonstrates mastery of:

```text
prakāśa
```

and then succeeds on:

```text
prakāśa → vimarśa distinction
```

The model can update related nodes differently:

```text
prakāśa               +small
vimarśa                +large
reflexivity             +medium
recognition             +small
```

Rather than assuming concepts are independent Bernoulli variables.

---

# 5. Dialogue-KT — extremely important because **our tutor is conversational**

**GitHub**

[https://github.com/umass-ml4ed/dialogue-kt](https://github.com/umass-ml4ed/dialogue-kt)

This project specifically studies knowledge tracing from tutor/student dialogue rather than merely answer sequences. It includes tooling to automatically annotate dialogue turns with knowledge components and correctness labels and benchmarks BKT/DKT-family models over those conversations. ([GitHub][6])

This is directly reusable for our chat ingestion pipeline.

Our transformation becomes:

```text
RAW CHAT TURN
    ↓
LLM annotation candidate
    ↓
{
  concepts: [vimarsa, prakasa],
  question_type: distinction,
  demonstrated_understanding: partial,
  misconception: vimarsa_is_attention
}
    ↓
structured LearningEvent
```

That gives us exactly the bridge from **unstructured chat → learner-state observations**.

I would inspect this repository closely before writing our own annotation system.

---

# 6. OATutor — steal the boring adaptive-tutor plumbing

**GitHub**

[https://github.com/CAHLR/OATutor](https://github.com/CAHLR/OATutor)

OATutor is an open-source intelligent tutor using BKT for mastery estimation and configurable problem selection; its design also supports experimental comparison of selection policies. ([GitHub][7])

We don't need its content or UI.

We should steal patterns for:

```text
content → knowledge components
interaction logging
mastery update
problem selection
A/B experiments
scaffolding/hints
```

Most importantly, it demonstrates how:

```text
content item
```

can map onto **multiple knowledge components**, which Pāṭala absolutely needs.

An argument challenge might test:

```text
recognition
continuity
scope
necessary_vs_sufficient
Buddhist_opponent
```

simultaneously.

---

# 7. OpenTutor — useful as a consumer product reference, less as science

**GitHub**

[https://github.com/zijinz456/OpenTutor](https://github.com/zijinz456/OpenTutor)

OpenTutor combines adaptive tutoring, concept graphs, mastery, quizzes, FSRS review, source-grounded chat and study planning in one local-first interface. Its own documentation marks some graph/adaptive components experimental, so I wouldn't use it as proof that the algorithms work. ([GitHub][8])

But product-wise it's useful.

Study:

```text
one workspace
+
source grounded tutor
+
concept map
+
review scheduler
+
mastery visualization
```

instead of separate `/courses`, `/chat`, `/quiz`, `/notes` silos.

---

# 8. Human-in-the-loop graph expansion — this is almost exactly the **Gap Engine**

This is one of the most important papers for the consumer-as-research-engine thesis.

**Paper**

[https://arxiv.org/abs/2212.05189](https://arxiv.org/abs/2212.05189)

The Pinterest work takes candidate new concepts, predicts where they belong in an existing knowledge graph, and sends those predicted graph placements to humans for verification. Their production deployment substantially reduced manual graph-expansion effort. ([arXiv][9])

We can directly adapt the mechanism.

Suppose questions reveal a recurring expression:

```text
"nondual perception"
```

Pipeline:

```text
new phrase / question cluster
          ↓
candidate Concept
          ↓
retrieve neighboring graph region
          ↓
predict parent(s)
          ↓
predict related concepts
          ↓
AI proposes:
   subtype_of perception?
   related_to recognition?
   modern_term_for X?
          ↓
review queue
          ↓
accept / merge / qualify / reject
```

This should be the **ontology-growth mechanism**.

Consumers find the candidate.

AI proposes placement.

Human authority decides.

---

# 9. Ontology Expansion research gives us the taxonomy for discovering new user needs

**Survey**

[https://arxiv.org/abs/2410.15019](https://arxiv.org/abs/2410.15019)

Conversational ontology expansion research distinguishes discovering new intents, new slot/value concepts, and joint expansion rather than assuming the ontology was correctly specified at launch. ([arXiv][10])

Translate that into Pāṭala:

```text
NEW CONCEPT
"I keep seeing people say nondual perception."

NEW RELATION
"Is recognition a kind of memory?"

NEW QUESTION TYPE
"Show where the Buddhist objection attacks this."

NEW USER INTENT
"Find a retreat where I can study this."
```

So raw user language becomes a detector for **schema inadequacy**.

---

# 10. ARIA — directly relevant to the AI asking humans only when uncertain

**GitHub**

[https://github.com/yf-he/aria](https://github.com/yf-he/aria)

ARIA is a self-improving agent architecture that detects uncertainty, requests targeted guidance from humans, stores timestamped learned knowledge, and manages conflicts/outdated knowledge. ([GitHub][11])

The mechanism is perfect for Pāṭala's research agents:

```text
Agent researches Q-811

confidence high:
→ continue automatically

confidence low because:
  two translations conflict
       ↓
formulate exact expert question
       ↓
"Does X govern Y or Z in this construction?"
       ↓
scholar answers
       ↓
store adjudication
       ↓
dependent graph updates
```

That's far better than:

> Scholar, please review this huge generated document.

Pāṭala already wants scoped adjudication; ARIA gives us another implementation reference for uncertainty-triggered human intervention.

---

# 11. Vouch — extremely aligned with Pāṭala's machine→proposal→human→canonical doctrine

**GitHub**

[https://github.com/vouchdev/vouch](https://github.com/vouchdev/vouch)

Vouch is a review-gated knowledge base where agents propose durable knowledge writes, claims retain citations, and human approval controls what enters the persistent KB. ([GitHub][12])

This is almost philosophically identical to Pāṭala's executable-corrections model.

Steal the workflow:

```text
AGENT GENERATED
      ↓
candidate diff
      ↓
sources machine checked
      ↓
review
      ↓
approved graph state
```

Particularly useful for the consumer Gap Engine:

```text
10,000 questions
      ↓
AI proposes 12 new canonical Question objects
      ↓
AI proposes 3 Concept edges
      ↓
human approves
```

Never let popularity write directly into canonical truth.

---

# 12. RefChecker — use the atomic **claim-triplet checking** idea

**GitHub**

[https://github.com/amazon-science/RefChecker](https://github.com/amazon-science/RefChecker)

RefChecker decomposes generated text into fine-grained claims represented as knowledge-style triplets and verifies them against references. ([GitHub][13])

This is directly useful for the autonomous:

```text
graph → essay
graph → lesson
graph → video script
```

compiler.

Generated explainer:

> Abhinavagupta argues that recognition requires an enduring subject.

Decompose:

```text
(Abhinavagupta,
 argues,
 recognition requires enduring subject)
```

Then check that against permitted graph/evidence objects.

That becomes a **rendering fidelity gate**.

---

# 13. RARR — steal its query→evidence→agreement→revision loop

**GitHub**

[https://github.com/anthonywchen/RARR](https://github.com/anthonywchen/RARR)

RARR takes generated claims, generates research questions about them, retrieves external evidence, checks whether the evidence agrees with the claim, and edits the claim if necessary. ([GitHub][14])

For Pāṭala:

```text
GENERATED EXPLAINER
       ↓
decompose claims
       ↓
generate evidence questions
       ↓
retrieve only Pāṭala-approved evidence
       ↓
agreement gate
       ↓
rewrite unsupported sentence
       ↓
recheck
```

This would be excellent inside autonomous essay/video generation.

Except unlike open-web RARR:

**our evidence universe is Pāṭala's provenance graph.**

Much stronger.

---

# 14. GraphCheck — very useful mechanism for checking long content against structured source graphs

**GitHub**

[https://github.com/Yingjian-Chen/GraphCheck](https://github.com/Yingjian-Chen/GraphCheck)

GraphCheck converts both claims and source documents into graph representations and performs graph-informed fact checking, motivated by the difficulty LLMs have catching relational errors across long documents. ([GitHub][15])

This is particularly relevant for:

```text
20 minute Pāṭala video script
```

because individual sentences can each look fine while the overall argument silently mangles relationships.

We could construct:

```text
SOURCE GRAPH
vs
SCRIPT CLAIM GRAPH
```

and detect:

```text
missing edge
reversed relation
wrong actor
wrong chronology
collapsed distinction
```

Very attractive for the media compiler.

---

# 15. CLAIMCHECK — probably the most important AI-review paper for our scholar layer

**Paper**

[https://arxiv.org/abs/2503.21717](https://arxiv.org/abs/2503.21717)

CLAIMCHECK links reviewer weaknesses to the paper claims they attack and evaluates whether critiques are valid, objective and properly grounded. Its experiments find current LLMs still behind human experts on several central claim-centric review tasks. ([arXiv][16])

That supports exactly our rule:

```text
AI CRITIQUE ≠ accepted criticism
```

Instead represent:

```text
Critique

attacks_claim_id
type
specificity
evidence
validity_candidate
review_state
```

Pāṭala's Reviewer-2 agent should produce **structured candidate objections**, not prose saying a paper is bad.

---

# 16. CLAIM-BENCH — steal the multi-pass claim/evidence extraction

**Paper**

[https://arxiv.org/abs/2506.08235](https://arxiv.org/abs/2506.08235)

CLAIM-BENCH evaluates LLM extraction and validation of claim–evidence relationships across full scientific papers and finds that carefully decomposed/multi-pass strategies improve linking over simpler processing, though at additional cost. ([arXiv][17])

For Pāṭala Review, don't:

```text
paper → one prompt → graph
```

Use:

```text
PASS 1
claims

PASS 2
candidate evidence

PASS 3
claim ↔ evidence linkage

PASS 4
argument relations

PASS 5
adversarial validation
```

This is slower but substantially more auditable.

---

# 17. CIBER — explicitly search for **refuting** evidence, not just support

**Paper**

[https://arxiv.org/abs/2503.07937](https://arxiv.org/abs/2503.07937)

CIBER separately searches for corroborating and refuting evidence and uses diverse interrogation probes to improve scientific claim investigation. ([arXiv][18])

This maps beautifully onto Pāṭala.

Every research claim should launch:

```text
SUPPORT SEARCH
+
QUALIFICATION SEARCH
+
COUNTEREVIDENCE SEARCH
```

rather than only retrieving nearest-semantic passages.

This prevents self-confirming research agents.

---

# 18. SCI-Verifier — useful as a model/verifier pattern

**GitHub**

[https://github.com/Zhengsh123/SCI-Verifier](https://github.com/Zhengsh123/SCI-Verifier)

SCI-Verifier is explicitly trained/evaluated as a reasoning verifier rather than a generator and accompanies a scientific verification benchmark. ([GitHub][19])

Long term we should probably have a **separate Pāṭala verifier model**.

Not:

```text
same model creates claim
and says claim is great
```

Architecture:

```text
Generator
    ↓
Verifier A: source fidelity
Verifier B: argument validity
Verifier C: scope/modality
Verifier D: translation fidelity
```

Eventually trained on our expert adjudications.

---

# 19. Argument-mining infrastructure — IAM gives us useful supervised task decomposition

**GitHub**

[https://github.com/LiyingCheng95/IAM](https://github.com/LiyingCheng95/IAM)

IAM decomposes argument mining into tasks such as claim extraction, stance classification and claim-evidence pair extraction. ([GitHub][20])

Pāṭala already has more sophisticated argument primitives than IAM, so don't adopt its ontology.

Reuse the **training task decomposition**:

```text
T1 proposition detection

T2 proposition type

T3 evidence span extraction

T4 evidence→claim relation

T5 claim→claim relation

T6 support / attack / qualify

T7 argument reconstruction
```

Train/evaluate each independently before pretending end-to-end argument extraction works.

---

# 20. Graph-R1 — technically fascinating for a later reasoning agent

**GitHub**

[https://github.com/LHRLAB/Graph-R1](https://github.com/LHRLAB/Graph-R1)

Graph-R1 constructs a knowledge hypergraph and trains an agent to repeatedly perform a cycle resembling think → issue graph query → retrieve subgraph → rethink, using RL. ([GitHub][21])

This is basically a future Pāṭala research agent:

```text
Question
   ↓
reason
   ↓
request specific graph neighborhood
   ↓
inspect
   ↓
identify missing fact
   ↓
query again
   ↓
answer
```

Rather than:

```text
retrieve top 20 chunks
→ dump into model
```

I would absolutely monitor/experiment with this once Pāṭala's graph has sufficient density.

---

# 21. Agent Lightning — potentially the eventual training infrastructure

**GitHub**

[https://github.com/microsoft/agent-lightning](https://github.com/microsoft/agent-lightning)

**Paper**

[https://arxiv.org/abs/2508.03680](https://arxiv.org/abs/2508.03680)

Agent Lightning decouples agent execution from training: agent trajectories/tool calls are recorded as structured traces, and optimization algorithms consume them later to improve policies/models. It explicitly tackles credit assignment across long agent trajectories. ([GitHub][22])

This is extremely relevant to the autonomous research engine.

Imagine recording:

```text
TASK:
answer research question Q

TRAJECTORY:
search graph
→ retrieve passage
→ propose hypothesis
→ inspect scholarship
→ revise
→ send crux to scholar
→ final answer

RESULT:
accepted / rejected
citations valid
argument score
scholar corrections
```

Now every Pāṭala research run becomes training data.

Later:

```text
Agent Lightning
        ↓
learn better research/search policies
```

This is closer to the “Karpathy/Eureka-style” self-improving system you're imagining.

---

# 22. DSPy — I would actually use this much sooner

**GitHub**

[https://github.com/stanfordnlp/dspy](https://github.com/stanfordnlp/dspy)

**Core paper**

[https://arxiv.org/abs/2310.03714](https://arxiv.org/abs/2310.03714)

**MIPRO**

[https://arxiv.org/abs/2406.11695](https://arxiv.org/abs/2406.11695)

**GEPA**

[https://arxiv.org/abs/2507.19457](https://arxiv.org/abs/2507.19457)

DSPy treats LM pipelines as programs with modules that can be optimized against explicit metrics rather than manually tuning prompts forever. ([GitHub][23])

This is perfect for:

```text
QuestionClusterExtractor
ConceptLinker
MisconceptionClassifier
ClaimExtractor
EvidenceLinker
GapClassifier
ReviewGenerator
ScriptVerifier
```

Define metrics from Pāṭala gold:

```text
exact concept IDs
correct EvidenceUse
valid support edge
no semantic inflation
correct gap type
```

Then optimize the LM program against those metrics.

That's far more appropriate to Pāṭala than a folder of gigantic hand-written prompts.

---

# 23. TextGrad — very useful for optimizing compound agents before actual model training

**Paper**

[https://arxiv.org/abs/2406.07496](https://arxiv.org/abs/2406.07496)

TextGrad treats components in compound AI systems as variables and propagates textual feedback through the pipeline to improve them. ([arXiv][24])

Possible Pāṭala loop:

```text
ResearchAgent output
        ↓
Verifier:
"Evidence linker repeatedly misses
qualifying passages because query is
too specific."
        ↓
textual feedback
        ↓
optimize EvidenceSearch module
```

This is a relatively cheap middle ground between:

```text
manually tweaking prompts
```

and:

```text
training an entire model
```

---

# 24. The self-improvement literature suggests one very clear architecture

A 2026 technical review organizes self-improving LLM systems around a loop of data acquisition, data selection, model optimization, inference refinement and continuous evaluation. ([arXiv][25])

Pāṭala gives that otherwise-generic loop actual semantic meaning:

```text
DATA ACQUISITION
user interactions

↓

DATA SELECTION
high-value Questions / Gaps

↓

RESEARCH
generate candidate knowledge

↓

EVALUATION
source + argument + scholar verification

↓

KNOWLEDGE UPDATE
Truth Graph

↓

POLICY OPTIMIZATION
better tutoring/research/content selection

↓

MORE INTERACTIONS
```

This is a proper self-improvement loop with **external grounding**, rather than models grading their own vibes.

---

# The graph schema I would actually implement

There should be a small shared event core.

```text
InteractionEvent
---------------
event_id
user_id
session_id
timestamp
event_type
object_ids[]
payload
consent_scope
```

Then specialized objects.

### Question

```text
Question
--------
question_id
raw_variants[]
canonical_text
concept_ids[]
claim_ids[]
argument_ids[]
question_type
frequency
growth
status
```

### Gap

```text
Gap
---
gap_id

type:
  EXPLANATION
  EVIDENCE
  ONTOLOGY
  ARGUMENT
  CORPUS
  DISAGREEMENT
  PEDAGOGICAL
  BENCHMARK
  CROSS_TRADITION
  OPEN_RESEARCH

trigger_question_ids[]
affected_objects[]
uncertainty
demand
centrality
downstream_impact
status
```

### Learner state

```text
LearnerState
------------
user_id
knowledge_component_id
mastery_probability
confidence
last_observed
model_version
evidence_event_ids[]
```

### Learning transition

```text
LearningTransition
------------------
from_state_id
intervention_id
predicted_outcome
observed_outcome
to_state_id
reward_components
```

### Research task

```text
ResearchTask
------------
gap_id
question_id
required_evidence[]
search_policy
candidate_findings[]
confidence
review_requirement
```

### Candidate graph mutation

```text
GraphProposal
-------------
proposal_id

operation:
  ADD_NODE
  ADD_EDGE
  MODIFY
  SUPERSEDE
  MERGE

source_events[]
evidence[]
agent_id
confidence
review_state
```

**Nothing generated goes straight into canonical truth.**

---

# Then build a five-gate AI review system

This is where I would sharpen Pāṭala considerably.

```text
PROPOSAL
   │
   ▼
G1 SCHEMA
Is it structurally valid?
   │
   ▼
G2 PROVENANCE
Does every assertion resolve to evidence?
   │
   ▼
G3 SEMANTIC FIDELITY
Does evidence actually support it?
   │
   ▼
G4 ADVERSARIAL
Can another agent find a better reading / contradiction?
   │
   ▼
G5 AUTHORITY
Does this require human expert judgment?
```

Possible statuses:

```text
REJECTED
MACHINE_PROPOSED
MACHINE_CORROBORATED
NEEDS_REVIEW
HUMAN_REVIEWED
ACCEPTED
CONTESTED
```

This is essentially combining Pāṭala's existing doctrine with mechanisms from Vouch, RARR, RefChecker, CLAIMCHECK and human-in-the-loop KG expansion. ([GitHub][12])

---

# The consumer→research chain then becomes technically precise

Consider a real interaction:

> “If consciousness is already Śiva, why does it have to recognize itself?”

### Stage 1 — interaction capture

```text
Episode E5811
```

Graphiti-style temporal memory.

### Stage 2 — question normalization

LLM proposes:

```text
Q184:
Why is recognition necessary if identity is already the case?
```

### Stage 3 — graph linking

```text
ABOUT → recognition
ABOUT → identity
TOUCHES → bondage
TOUCHES → contraction
```

### Stage 4 — cluster

Embedding + graph neighborhood + semantic model determines that 2,861 variants belong to Q184.

### Stage 5 — gap detection

Current answer exists.

But:

```text
follow-up confusion = 61%
```

Therefore:

```text
Gap:
PEDAGOGICAL_GAP
```

not necessarily:

```text
OPEN_RESEARCH
```

### Stage 6 — intervention experiment

Bandit/pedagogy system tests:

```text
A prose explanation
B argument graph
C Buddhist objection
D primary-source contrast
```

### Stage 7 — learning measurement

B resolves misconception much more often.

Update pedagogy graph.

### Stage 8 — content mutation

Agent proposes revised canonical explainer using B's mechanism.

### Stage 9 — verification

RARR/RefChecker-like claim checking.

### Stage 10 — dependency propagation

```text
explainer
lesson
essay
video script
AI teacher
```

all re-render.

That's the actual machine.

---

# And here's the part I think we should *not* do

Don't build:

```text
Neo4j
+
one huge universal graph
+
LLM queries it
```

and call it intelligence.

We need **separate semantics**.

I would maintain:

```text
1. Truth Graph
sources / claims / arguments / reviews

2. Temporal User Graph
interests / goals / history / preferences

3. Learner-State Model
probabilistic mastery; technically not merely graph facts

4. Question + Gap Graph
collective demand/discovery

5. Pedagogy Graph
state/intervention/outcome relationships

6. Event Ledger
immutable source behind all user-derived graphs
```

Some can share the same physical graph database later, but **they should remain logically separate models**.

That prevents:

```text
"asked about X"
```

becoming:

```text
"believes X"
```

or:

```text
"watched X"
```

becoming:

```text
"understands X"
```

which would poison everything.

---

# My actual reuse priority

| Tech/project                | Pāṭala use                                  |        Priority |
| --------------------------- | ------------------------------------------- | --------------: |
| **Graphiti**                | temporal user/context graph                 |       **10/10** |
| **Dialogue-KT**             | chat → knowledge observations               |       **10/10** |
| **pyBKT**                   | initial mastery model                       |       **10/10** |
| **Human-loop KG expansion** | consumer → ontology growth                  |       **10/10** |
| **DSPy**                    | optimize extraction/review programs         |       **10/10** |
| **RARR**                    | claim→retrieve→revise loop                  |        **9/10** |
| **RefChecker**              | atomic rendering verification               |        **9/10** |
| **CLAIMCHECK**              | grounded critique model/schema              |        **9/10** |
| **Vouch**                   | review-gated graph mutations                |        **9/10** |
| **GRKT**                    | graph-aware learner-state modeling          |  **8/10 later** |
| **CIBER**                   | support + refutation retrieval              |        **8/10** |
| **TextGrad**                | optimize compound AI pipelines              |        **8/10** |
| **Agent Lightning**         | train research/tutor agents on trajectories | **10/10 later** |
| **Graph-R1**                | learned graph-search/reasoning policy       |  **9/10 later** |
| **OpenTutor**               | consumer UX patterns                        |        **6/10** |
| full RL/POMDP               | long-term pedagogy                          |       **later** |

## The crucial architecture

If I were speccing the next version now, it would be:

```text
                PĀṬALA EVENT BUS
                       │
       ┌───────────────┼────────────────┐
       ▼               ▼                ▼
   Graphiti          Dialogue-KT     Question clusterer
  user memory          ↓                ↓
                  pyBKT state        Gap Engine
                       │                │
                       ▼                ▼
                 PEDAGOGY POLICY   RESEARCH POLICY
                       │                │
                       ▼                ▼
                     USER        Research Agents
                                        │
                               ┌────────┼────────┐
                               ▼        ▼        ▼
                             RARR   RefChecker CLAIMCHECK
                               │        │        │
                               └────────┼────────┘
                                        ▼
                                  GraphProposal
                                        │
                                     HUMAN
                                      GATE
                                        │
                                        ▼
                                   TRUTH GRAPH
                                        │
                    ┌───────────────────┼─────────────┐
                    ▼                   ▼             ▼
                 learning             media          scholar
```

Then later:

```text
all trajectories
     ↓
Agent Lightning / DSPy / KT experiments
     ↓
better tutor
better researcher
better content selector
better graph traversal
```

The thing I would **not** train first is a bespoke foundation model. The scarce asset is the structured trajectory dataset:

> **given user/research state S, intervention/action A, evidence context G, what happened next—and was it ultimately validated?**

Once Pāṭala owns millions of those transitions, training becomes much more interesting because we aren't teaching a model generic Sanskrit or generic pedagogy. We're training it on **how real humans move through a verified philosophical graph and how research agents successfully convert their questions into reviewed knowledge**.

That is the compounding technical engine.

[1]: https://github.com/getzep/graphiti?utm_source=chatgpt.com "GitHub - getzep/graphiti: Build Real-Time Knowledge Graphs for AI Agents · GitHub"
[2]: https://github.com/getzep/graphiti/blob/main/mcp_server/README.md?utm_source=chatgpt.com "graphiti/mcp_server/README.md at main · getzep/graphiti · GitHub"
[3]: https://github.com/CAHLR/pyBKT?utm_source=chatgpt.com "GitHub - CAHLR/pyBKT: Python implementation of Bayesian Knowledge Tracing and extensions · GitHub"
[4]: https://github.com/pykt-team/pykt-toolkit?utm_source=chatgpt.com "GitHub - pykt-team/pykt-toolkit: pyKT: A Python Library to Benchmark Deep Learning based Knowledge Tracing Models · GitHub"
[5]: https://arxiv.org/abs/2406.12896?utm_source=chatgpt.com "Leveraging Pedagogical Theories to Understand Student Learning Process with Graph-based Reasonable Knowledge Tracing"
[6]: https://github.com/umass-ml4ed/dialogue-kt?utm_source=chatgpt.com "GitHub - umass-ml4ed/dialogue-kt: Code for the paper \"Exploring Knowledge Tracing in Tutor-Student Dialogues using LLMs\" at LAK2025. · GitHub"
[7]: https://github.com/CAHLR/OATutor?utm_source=chatgpt.com "GitHub - CAHLR/OATutor: Open Source Intelligent Tutoring System w/ BKT (ReactJS and Firebase) · GitHub"
[8]: https://github.com/zijinz456/OpenTutor?utm_source=chatgpt.com "GitHub - zijinz456/OpenTutor: The first block-based adaptive learning workspace that runs locally. Upload any material → get AI-generated notes, quizzes, flashcards, and an adaptive tutor. Open source, self-hosted, 10+ LLM providers. · GitHub"
[9]: https://arxiv.org/abs/2212.05189?utm_source=chatgpt.com "Expanding Knowledge Graphs with Humans in the Loop"
[10]: https://arxiv.org/abs/2410.15019?utm_source=chatgpt.com "A Survey of Ontology Expansion for Conversational Understanding"
[11]: https://github.com/yf-he/aria?utm_source=chatgpt.com "GitHub - yf-he/aria: Enabling Self-Improving Agents to Learn at Test Time With Human-In-The-Loop Guidance (EMNLP'25) · GitHub"
[12]: https://github.com/vouchdev/vouch?utm_source=chatgpt.com "GitHub - vouchdev/vouch: A git-native, review-gated knowledge base for AI agents: they propose writes, you approve them. Every claim cites a source, every change is a diff in your repo. MCP + CLI. · GitHub"
[13]: https://github.com/amazon-science/RefChecker?utm_source=chatgpt.com "GitHub - amazon-science/RefChecker: RefChecker provides automatic checking pipeline and benchmark dataset for detecting fine-grained hallucinations generated by Large Language Models. · GitHub"
[14]: https://github.com/anthonywchen/RARR?utm_source=chatgpt.com "GitHub - anthonywchen/RARR: RARR: Researching and Revising What Language Models Say, Using Language Models · GitHub"
[15]: https://github.com/Yingjian-Chen/GraphCheck?utm_source=chatgpt.com "GitHub - Yingjian-Chen/GraphCheck: Official Implementation of ACL 2025 paper \"GraphCheck: Breaking Long-Term Text Barriers with Extracted Knowledge Graph-Powered Fact-Checking\" · GitHub"
[16]: https://arxiv.org/abs/2503.21717?utm_source=chatgpt.com "CLAIMCHECK: How Grounded are LLM Critiques of Scientific Papers?"
[17]: https://arxiv.org/abs/2506.08235?utm_source=chatgpt.com "Can AI Validate Science? Benchmarking LLMs for Accurate Scientific Claim $\rightarrow$ Evidence Reasoning"
[18]: https://arxiv.org/abs/2503.07937?utm_source=chatgpt.com "LLM-based Corroborating and Refuting Evidence Retrieval for Scientific Claim Verification"
[19]: https://github.com/Zhengsh123/SCI-Verifier?utm_source=chatgpt.com "GitHub - Zhengsh123/SCI-Verifier: Official GitHub repo for SCI-Verifier: Scientific Verifier with Thinking (ICLR2026). · GitHub"
[20]: https://github.com/LiyingCheng95/IAM?utm_source=chatgpt.com "GitHub - LiyingCheng95/IAM · GitHub"
[21]: https://github.com/LHRLAB/Graph-R1?utm_source=chatgpt.com "GitHub - LHRLAB/Graph-R1: [ICML 2026] Official resources of \"Graph-R1: Towards Agentic GraphRAG Framework via End-to-end Reinforcement Learning\". · GitHub"
[22]: https://github.com/microsoft/agent-lightning?utm_source=chatgpt.com "GitHub - microsoft/agent-lightning: The absolute trainer to light up AI agents. · GitHub"
[23]: https://github.com/stanfordnlp/dspy?utm_source=chatgpt.com "GitHub - stanfordnlp/dspy: DSPy: The framework for programming—not prompting—language models · GitHub"
[24]: https://arxiv.org/abs/2406.07496?utm_source=chatgpt.com "TextGrad: Automatic \"Differentiation\" via Text"
[25]: https://arxiv.org/abs/2603.25681?utm_source=chatgpt.com "Self-Improvement of Large Language Models: A Technical Overview and Future Outlook"
