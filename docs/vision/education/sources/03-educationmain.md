Exactly. The deep version is stronger than “interactive education.”

> **Pāṭala can compile scholarly structure into diagnostic interactions where each possible response corresponds to a specific interpretation of the underlying argument.**

So answering correctly is **evidence that the learner has recovered the relevant distinction, dependency, scope, attribution, or crux**.

Not mathematical proof that they “understand” in some absolute sense. But something much better than normal quiz correctness: a **typed demonstration of understanding against a known epistemic object**.

That gives us a direct extension of the whole architecture.

# 1. The complete Pāṭala stack now becomes

```text
SOURCE
│
│  "What does the text actually contain?"
▼
PhilologicalProof
TranslationDecision
TermSense
│
│  "What does it mean?"
▼
Proposition
Commitment
SemanticAlignment
│
│  "What follows from what?"
▼
Inference
Argument
Defeater
Crux
DebateFrame
│
│  "What do scholars warrant?"
▼
EvidenceUse
CorroborationEvent
ReviewEvent
DerivedState
│
│  "How do we communicate it?"
▼
Synthesis
KnowledgePacket
│
│  "Can someone reconstruct it?"
▼
LearningInteraction
LearnerResponse
DiagnosticResult
MasteryEvidence
│
│  "What should they encounter next?"
▼
LearnerState
PrerequisiteGraph
PedagogicalPolicy
```

That bottom layer isn't disconnected from scholarship.

It's **compiled out of scholarship**.

And this means our earlier architecture has accidentally given us the ingredients for a very sophisticated educational engine.

---

# 2. The fundamental object should be `LearningClaim`

Not merely:

```text
lesson: "Recognition"
```

Instead:

```yaml
LearningClaim:
  id: LC-PRAT-001

  learner_should_understand:
    "Utpaladeva's recognition argument requires explaining
     how temporally distinct cognitions can participate in
     recognition of something as previously experienced."

  derived_from:
    propositions:
      - P-001
      - P-002
    inferences:
      - INF-003
    cruxes:
      - CRUX-001
    passages:
      - IPK-1.x.x
    debate_frame:
      - DF-RECOGNITION

  required_discriminations:
    - memory != recognition
    - causal continuity != numerical identity
    - current cognition != previous cognition
    - author commitment != opponent commitment

  mastery_conditions:
    - identify_dependency
    - survive_distractor
    - explain_choice
    - transfer_to_new_case
```

Notice what's happened.

The learning objective is now **machine-linked to the exact philosophical structure we're asking the human to recover**.

---

# 3. Then multiple choice becomes surprisingly serious

Normal multiple choice:

> What does vimarśa mean?

A. awareness
B. reflection
C. self-awareness
D. energy

Mostly tests terminology recall.

Pāṭala multiple choice should instead ask a **discriminating question**.

Suppose the underlying scholarly structure is:

```text
P1 Cognition C₁ occurred previously.
P2 Cognition C₂ occurs now.
P3 C₁ ≠ C₂.
P4 Recognition nevertheless relates the present
   experience to the previous experience as "mine".
────────────────────────────────────────────────
C  Some account of diachronic continuity is required.
```

Now ask:

> Which fact creates the problem that the recognition argument is trying to solve?

A. The perceived object exists at two times.
B. The two cognitions are numerically distinct.
C. Recognition necessarily involves language.
D. Memory reproduces the original cognition exactly.

Correct answer:

```text
B
```

But importantly:

```text
B → recognizes the target dependency.

A → object/subject confusion.
C → imports an irrelevant condition.
D → collapses recognition into memory/reproduction.
```

Therefore we don't store:

```text
answer = wrong
```

We store:

```yaml
LearnerResponse:
  selected: D

DiagnosticResult:
  misconception:
    type: CONCEPT_COLLAPSE
    objects:
      - memory
      - recognition

  failed_discrimination:
    - memory != recognition

  affected_learning_claim:
    - LC-PRAT-001
```

**Every wrong answer is epistemically meaningful.**

That is radically more useful.

---

# 4. Distractors should come from the argument graph

This may be one of the strongest pieces of the whole design.

We should rarely invent plausible-looking wrong answers.

Generate distractors from actual structured alternatives:

```text
correct answer
     │
     ├── rival proposition
     ├── rejected interpretation
     ├── defeated inference
     ├── scope inflation
     ├── modality change
     ├── wrong speaker
     ├── related-but-non-equivalent term
     ├── known scholarly disagreement
     └── common model/human error
```

So if Pāṭala knows:

```text
P1: awareness manifests an object

P2: awareness apprehends itself

P3: P1 alone is insufficient for reflexive awareness
```

then a question can distinguish:

```text
prakāśa
vimarśa
prakāśa + vimarśa
object manifestation
self-apprehension
```

The distractors are generated from **real neighboring commitments**.

That makes the question diagnostic instead of merely difficult.

---

# 5. The Argument IR becomes an Exercise IR

This is the piece I would formally add to Pāṭala.

We already have approximately:

```text
Proposition
Inference
Grounding
Defeater
Commitment
DebateFrame
SemanticAlignment
Crux
```

Create a compiler:

```text
ARGUMENT IR
    ↓
EDUCATION COMPILER
    ↓
INTERACTION IR
```

Something like:

```yaml
LearningInteraction:
  id: LI-0092

  target:
    object_type: Inference
    object_id: INF-003

  operation:
    IDENTIFY_MISSING_PREMISE

  presentation:
    difficulty: 2
    scaffold_level: 3

  prompt:
    ...

  response_space:
    type: SINGLE_CHOICE

  options:
    - proposition: P-018
      role: CORRECT

    - proposition: P-021
      role: RIVAL_READING

    - proposition: P-032
      role: SCOPE_ERROR

    - generated_from: attribution_flip
      role: ATTRIBUTION_ERROR

  mastery_signal:
    skill: WARRANT_RECONSTRUCTION

  provenance:
    generated_from_argument: ARG-002
    compiler_version: ...
```

That becomes canonical.

---

# 6. And there are a finite number of powerful interaction operators

This is where it becomes buildable.

The education compiler doesn't need to "invent lessons."

It applies operations to scholarly structures.

```text
SOURCE OPERATORS
─────────────────────────────────
LOCATE_SOURCE
MATCH_QUOTATION
IDENTIFY_VARIANT
MATCH_TRANSLATION
DETECT_OMISSION
DETECT_ADDITION


PHILOLOGY OPERATORS
─────────────────────────────────
CHOOSE_TERM_SENSE
COMPARE_TRANSLATIONS
RESOLVE_ALIGNMENT
IDENTIFY_NEGATION
IDENTIFY_SCOPE
IDENTIFY_AGENT
CHOOSE_PARSE
RANK_RIVAL_READING


INTERPRETATION OPERATORS
─────────────────────────────────
IDENTIFY_PROPOSITION
IDENTIFY_COMMITMENT
IDENTIFY_SPEAKER
DISTINGUISH_ASSERTION_FROM_ATTRIBUTION
DETECT_PARAPHRASE_EXPANSION
DETECT_CLAIM_SURFACE_INFLATION


ARGUMENT OPERATORS
─────────────────────────────────
CONNECT_PREMISE
IDENTIFY_WARRANT
COMPLETE_INFERENCE
ORDER_ARGUMENT
CLASSIFY_SUPPORT_ATTACK
IDENTIFY_DEFEATER
FIND_MISSING_PREMISE


COMPARISON OPERATORS
─────────────────────────────────
ALIGN_TERM_SENSE
ALIGN_DEBATE_FRAME
DETECT_SCOPE_MISMATCH
DETECT_QUESTION_MISMATCH
GENUINE_CONTRADICTION_OR_NOT


CRUX OPERATORS
─────────────────────────────────
RETRACT_PREMISE
PREDICT_IMPACT
IDENTIFY_LOAD_BEARING_PREMISE
MINIMAL_CRUX
COMPARE_RIVAL_CRUXES


SYNTHESIS OPERATORS
─────────────────────────────────
CHOOSE_BEST_SUMMARY
DETECT_OVERSTATEMENT
MATCH_CONCLUSION_TO_EVIDENCE
IDENTIFY_UNCERTAINTY
DISTINGUISH_FACT_FROM_RECONSTRUCTION
```

This is our **interactive vocabulary**.

Comparable to Brilliant having things like:

```text
move point
change variable
order objects
estimate
construct
compare
predict
```

Except ours are epistemic operations.

---

# 7. There is a second dimension: response mechanics

The same intellectual operation can be presented through different mechanics.

For example `IDENTIFY_WARRANT`:

### Level 1 — Multiple choice

```text
Which missing premise connects these statements?
```

### Level 2 — Drag and drop

```text
P1 ──────┐
         ? → C
P2 ──────┘

[drag proposition here]
```

### Level 3 — Selection from corpus

Find the warrant among ten candidate propositions.

### Level 4 — Construct

Write it yourself.

### Level 5 — Source-ground

Find a passage that warrants your reconstruction.

### Level 6 — Defend

AI adversary gives strongest objection.

### Level 7 — Transfer

Do the same thing on a passage you've never encountered.

Same skill.

Increasing evidential strength.

---

# 8. This gives us an actual hierarchy of evidence for understanding

A correct multiple-choice answer is weak evidence because guessing is possible.

So don't claim:

> learner mastered concept.

We accumulate evidence.

```text
E0  EXPOSED
    learner saw explanation

E1  RECOGNIZED
    selected correct answer

E2  DISCRIMINATED
    selected correct answer against
    high-quality rival readings

E3  RECONSTRUCTED
    supplied/assembled missing structure

E4  EXPLAINED
    produced acceptable explanation

E5  APPLIED
    used principle on new example

E6  TRANSFERRED
    applied principle to materially
    different unseen context

E7  DEFENDED
    maintained interpretation under
    plausible counterargument

E8  SOURCE-GROUNDED
    connected reasoning back to
    appropriate primary evidence
```

Now **mastery is evidence-bearing too**.

This is incredibly aligned with Pāṭala.

We use the same anti-theatre doctrine on learners that we use on AI systems and scholarship:

> Don't call something understood merely because a field says `mastered=true`.

---

# 9. A learner answer becomes a tiny epistemic event

This suggests:

```yaml
MasteryEvidence:
  learner: USER-X

  target:
    learning_claim: LC-001

  demonstrated_operation:
    IDENTIFY_CRUX

  interaction:
    LI-083

  response:
    selected: P-003

  conditions:
    scaffold_level: 1
    unseen_material: true
    distractor_quality: adjudicated
    attempts: 1

  result:
    PASS

  evidence_strength:
    TRANSFER

  timestamp: ...
```

Then:

```text
LearnerState
```

is **derived** from these events.

Never directly mutated to:

```text
vimarsa_mastery = 91%
```

Instead:

```text
MasteryEvidence[]
      ↓
mastery reducer
      ↓
LearnerState
```

Sound familiar?

It's the same architecture as:

```text
ReviewEvent[]
      ↓
reducer
      ↓
DerivedState
```

That's beautiful because we're reusing the philosophical architecture all the way down.

---

# 10. Therefore: education itself becomes provenance-bearing

Suppose Tom's state says:

```text
UNDERSTANDS:
  recognition continuity argument
```

Click it.

Why does Pāṭala think so?

```text
✓ distinguished memory vs recognition
✓ reconstructed INF-003
✓ rejected causal-continuity distractor
✓ identified CRUX-001
✓ transferred argument to unseen example
? has not yet grounded it in Sanskrit
```

That's much cooler than:

> 87% mastery.

It gives the learner a **proof tree of their own learning**.

Again, not proof in the strict mathematical sense, but an inspectable evidential record.

---

# 11. This also fixes adaptive learning

We shouldn't ask:

> What lesson comes after lesson 7?

We ask:

```text
What cannot this learner currently do?
```

Suppose:

```text
TERM_SENSE                  strong
SPEAKER_ATTRIBUTION         strong
PROPOSITION_EXTRACTION      strong
WARRANT_RECONSTRUCTION      weak
CRUX_IDENTIFICATION         weak
SOURCE_GROUNDING            unknown
```

Then Pāṭala chooses an interaction that isolates warrant reconstruction.

Crucially, content and skill are separate axes.

```text
                   SKILL

             attribution
             warrant
             crux
             scope
             grounding
                ...
CONTENT ┌────────────────────────
        │
vimarśa │
apoha   │     mastery matrix
spanda  │
self    │
memory  │
...
```

So a learner might know a lot **about Abhinavagupta** but be bad at reconstructing arguments.

Another might be excellent at philosophy but know no Tantra.

Same system adapts differently.

---

# 12. This creates a very useful ontology separation

I'd formalize three graphs.

## A. Epistemic graph

What the scholarship says.

```text
Passage
→ Proposition
→ Inference
→ Argument
→ Crux
```

## B. Pedagogical graph

What depends pedagogically on what.

```text
numerical identity
      ↓
diachronic identity
      ↓
recognition problem
      ↓
Utpaladeva argument
```

This is not necessarily identical to logical dependency.

## C. Learner graph

What this particular learner has evidence of being able to do.

```text
Learner
 ├ concept state
 ├ skill state
 ├ misconception state
 └ learning history
```

Then:

```text
EpistemicGraph
     +
PedagogicalGraph
     +
LearnerGraph
     ↓
NEXT INTERACTION
```

That's the educational engine.

---

# 13. `Misconception` should become a first-class object

This is another major insight.

Because our wrong answers can correspond to structured intellectual mistakes:

```yaml
Misconception:
  id: MC-PRAT-007

  type: CONCEPT_COLLAPSE

  confuses:
    - recognition
    - memory

  associated_objects:
    - P-009
    - P-010

  detected_by:
    - LI-012
    - LI-087

  remediation:
    prerequisite:
      - KP-MEMORY-VS-RECOGNITION

  distinguishing_test:
    - LI-091
```

Other types:

```text
WRONG_SPEAKER
SCOPE_INFLATION
MODALITY_INFLATION
CONCEPT_COLLAPSE
TERM_SENSE_COLLAPSE
CAUSATION_IDENTITY_CONFUSION
EVIDENCE_WARRANT_CONFUSION
CORRELATION_GROUNDING_CONFUSION
QUESTION_MISMATCH
DEBATE_FRAME_MISMATCH
PURVAPAKSA_AS_AUTHOR
RIVAL_READING_IGNORED
```

Notice how many of these already exist in our **translation/argument error taxonomy**.

So the same failure taxonomy can diagnose:

```text
AI translation
AI argument reconstruction
student understanding
```

That's wild.

---

# 14. Benchmark ↔ Education becomes a dual system

This deserves explicit architecture.

For machines:

```text
PĀṬALA BENCHMARK
"What did the model understand?"
```

For humans:

```text
PĀṬALA LEARNING
"What did the learner understand?"
```

They may literally share fixtures.

Example:

```yaml
Fixture:
  source: IPVV passage

  target_distinction:
    author vs opponent commitment

  prompt_family:
    classify_commitment

  gold:
    ATTRIBUTES_TO_OPPONENT
```

Machine receives one rendering.

Human receives a more pedagogical rendering.

Same gold.

Same provenance.

Same scholarly adjudication.

Different evaluator.

This creates:

```text
                    SCHOLAR GOLD
                    /          \
                   /            \
          MACHINE EVAL       HUMAN LEARNING
```

That means the huge investment in gold doesn't only serve AI benchmarking.

It powers education.

And education interactions produce information about which distinctions are genuinely hard for humans—which can inform benchmark construction.

**Fantastic flywheel.**

---

# 15. Even Translation Audit becomes educational

Imagine a student working through Sanskrit.

Instead of Pāṭala simply saying:

> Your translation has the wrong agent.

It asks:

> Compare the Sanskrit and your translation.
> Who is the agent of `X`?

Then:

```text
A. cognition
B. subject
C. object
D. opponent
```

They answer.

Only if necessary does Pāṭala reveal the finding.

So Audit has modes:

```text
AUDIT MODE
tell me what is wrong

LEARN MODE
make me discover what is wrong
```

Same detector.

Same finding.

Different presentation.

That's brilliant for Sanskrit learning.

---

# 16. Review can also become education

Consider the scholar review interface:

```text
Claim
Evidence
Inference
Defeater
Crux
```

A student version can hide one component.

```text
Claim
Evidence
?
Conclusion
```

Fill it.

This means the eventual Scholar Workbench and advanced Study product can converge.

The difference between learner and scholar becomes progressively smaller.

At the deepest level:

> **Learning scholarship means progressively acquiring the ability to perform the actual typed actions scholars perform.**

That is a very strong educational philosophy.

---

# 17. Which means we can define levels by agency rather than content

Instead of:

```text
Beginner
Intermediate
Advanced
```

Use something closer to:

```text
LEVEL 0 — OBSERVE
read curated explanation

LEVEL 1 — RECOGNIZE
distinguish structures presented to you

LEVEL 2 — MANIPULATE
modify structured objects

LEVEL 3 — RECONSTRUCT
supply missing structures

LEVEL 4 — GROUND
connect structures to evidence

LEVEL 5 — CHALLENGE
find defeaters/rival readings

LEVEL 6 — ADJUDICATE
compare evidentially plausible alternatives

LEVEL 7 — CONTRIBUTE
submit structured scholarly proposal
```

Look at that final transition:

```text
learner
    ↓
advanced learner
    ↓
contributor
    ↓
scholar
```

There does not need to be a hard product boundary.

That could be profound for Pāṭala's contributor ecosystem.

---

# 18. The end-state product might feel like a game without becoming gamified nonsense

Imagine opening:

## Recognition

> Two cognitions occur at different times.

You see two nodes.

Then:

> Yet something is recognized as previously experienced.

A third node appears.

> What is missing?

You drag an answer.

The graph animates.

Correct.

Now Pāṭala introduces the Buddhist solution.

You manipulate that.

Then a competing Śaiva reconstruction.

You remove premises.

Watch conclusions collapse.

Then:

> **Which disagreement actually separates the two positions?**

You identify the crux.

Then:

> **Now show me the text.**

Sanskrit appears alongside the translation.

Then:

> **Does the Sanskrit warrant the stronger version of the claim?**

Now you're doing philology.

Twenty minutes ago you knew nothing about Pratyabhijñā.

You have now **reenacted the philosophical pressure that generated the doctrine**.

That is much better than learning:

> “Kashmir Shaivism believes in recognition.”

---

# 19. This suggests a core educational principle

I would put this in the Pāṭala constitution:

> **Do not tell the learner a distinction when the learner can be placed in a situation where the distinction becomes necessary.**

That's the Brilliant insight translated into philosophy.

For maths:

> Don't tell them the formula first. Let the structure force it.

For Pāṭala:

> Don't tell them Utpaladeva posits a persisting subject. Give them the recognition problem and make them discover what explanatory work persistence is doing.

Then reveal the historical tradition.

**The doctrine becomes an answer to a problem they now genuinely possess.**

That is how you make ancient philosophy feel alive.

---

# 20. The compiler architecture

I'd now add an entire Education Compiler layer to the repo vision:

```text
              CANONICAL SCHOLARLY STATE
                        │
                        ▼
              LEARNING CLAIM BUILDER
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
        skill extraction     prerequisites
              │                   │
              └─────────┬─────────┘
                        ▼
               INTERACTION COMPILER
                        │
       ┌────────────────┼────────────────┐
       ▼                ▼                ▼
   correct path     distractors      diagnostics
       │                │                │
       └────────────────┼────────────────┘
                        ▼
                INTERACTION FIXTURE
                        │
                        ▼
                    RENDERER
             ┌──────────┼──────────┐
             ▼          ▼          ▼
             MCQ       GRAPH      SOURCE
             DRAG      SIM        STUDY
             TEXT      CHAT       AUDIT
                        │
                        ▼
                 LEARNER RESPONSE
                        │
                        ▼
               RESPONSE EVALUATOR
                        │
              ┌─────────┴──────────┐
              ▼                    ▼
        MasteryEvidence        Misconception
              │                    │
              └──────────┬─────────┘
                         ▼
                   LearnerState
                         │
                         ▼
                PEDAGOGICAL POLICY
                         │
                         └──→ next interaction
```

---

# 21. The canonical education schemas I'd add

Not necessarily implementation tomorrow, but conceptually:

```text
LearningClaim
LearningSkill
PedagogicalDependency
Misconception
InteractionFixture
InteractionOption
DiagnosticMapping
LearnerResponse
MasteryEvidence
LearnerState
LearningPath
KnowledgePacket
```

And I'd be very strict about what belongs where.

`KnowledgePacket` is presentation/synthesis.

`LearningClaim` is what must be understood.

`InteractionFixture` is how we test it.

`MasteryEvidence` is what actually happened.

`LearnerState` is a derived estimate.

---

# 22. Every interaction should have explicit `what_it_tests`

This should be mandatory.

No:

```yaml
question:
  "What is spanda?"
```

without saying why we are asking it.

Instead:

```yaml
what_it_tests:
  target_object: Proposition/P-552

  discrimination:
    "spanda is not literal physical vibration"

  reasoning_skill:
    SENSE_DISCRIMINATION

  expected_evidence_level:
    E2_DISCRIMINATED

  known_misconceptions:
    - MC-SPANDA-PHYSICAL-VIBRATION
```

This prevents edtech theatre exactly as our other contracts prevent AI theatre.

---

# 23. And every answer option gets a provenance

Imagine:

```yaml
options:

  - text: "A physical vibration underlying matter"
    status: incorrect
    derives_from:
      misconception: MC-021

  - text: "The dynamic pulse or activity of consciousness"
    status: correct
    derives_from:
      proposition: P-992

  - text: "A synonym for śakti in every Śaiva text"
    status: incorrect
    derives_from:
      error: SCOPE_INFLATION

  - text: "The sequence of cognitions described by Krama"
    status: incorrect
    derives_from:
      concept: KRAMA_SEQUENCE
```

This is **proof-carrying multiple choice**, in our loose Pāṭala sense.

The question itself has an epistemic lineage.

---

# 24. Then questions can be regenerated safely after scholarly correction

This is crucial.

Suppose scholar review revises:

```text
P-992 v1
→
P-992 v2
```

Dependency propagation discovers:

```text
LearningClaim LC-22 depends on P-992
InteractionFixture LI-381 depends on LC-22
Option O-2 derives from P-992
KnowledgePacket KP-91 depends on P-992
VideoScript VS-12 depends on KP-91
```

All become:

```text
NEEDS_REVIEW
```

Education inherits **executable corrections**.

This is something almost no edtech system is built to do.

---

# 25. The really crazy long-term result: curricula can compile from scholarship

Given:

```text
target = "Understand the Pratyabhijñā response to Buddhist momentariness"
```

Compiler finds:

```text
target propositions
↓
required arguments
↓
required concepts
↓
required term senses
↓
required historical context
↓
prerequisite graph
```

Then intersects learner state:

```text
already mastered
vs
missing
```

and generates:

```text
your route
```

Something like:

```text
1. What is numerical identity?       4 min
2. Can cognition persist?            6 min
3. Momentariness simulator           7 min
4. Recognition puzzle                9 min
5. Reconstruct Utpaladeva            8 min
6. Buddhist counterargument          7 min
7. Find the real crux                6 min
8. Ground it in Sanskrit            12 min
```

Courses genuinely become **compiled paths through a dependency graph**.

Not manually fixed module trees.

---

# 26. And media can compile from the exact same object

The same LearningClaim:

```text
LC-PRAT-001
```

renders as:

```text
interactive puzzle
flashcard
multiple choice
Socratic tutor exchange
article section
animation
YouTube short
documentary beat
source-study exercise
argument map
```

So the media engine isn't creating another truth layer.

It's rendering epistemic objects under different constraints.

---

# 27. This changes what the educational moat actually is

It isn't:

* nice courses;
* an AI tutor;
* spaced repetition;
* multiple-choice generation;
* a knowledge graph.

Those are reproducible.

The moat becomes:

```text
EXPERT-ADJUDICATED SCHOLARLY GRAPH
            ×
TYPED LEARNING CLAIMS
            ×
DIAGNOSTIC DISTRACTORS
            ×
MISCONCEPTION GRAPH
            ×
LEARNER EVIDENCE HISTORY
            ×
CORRECTION PROPAGATION
```

And then network effects become serious.

After 100,000 learner interactions we start learning:

```text
Which distinction actually causes confusion?

Which distractor separates superficial from robust understanding?

Which premise is hardest to reconstruct?

Which explanation produces transfer?

Which prerequisite actually matters?

Which philosophical problems reliably produce the "aha" moment?
```

Now Pāṭala accumulates not just scholarly gold.

It accumulates **pedagogical gold about the structure of human understanding of that scholarship**.

That dataset would be genuinely unusual.

---

# 28. There is even a research program hiding here

Pāṭala could eventually publish results about:

```text
epistemic dependency
vs
pedagogical dependency

argument understanding
vs
fact recall

misconception topology

transfer across philosophical arguments

human vs model error overlap

which cruxes humans/models systematically miss

whether interactive counterfactual manipulation
improves argument comprehension
```

And because the scholarly objects are precisely identified, experiments are much cleaner than generic "AI tutor helps philosophy students" work.

---

# 29. The minimum build I would actually do

Do **not** build an education platform yet.

Take one fully worked argument—ideally the best IPVV/Pratyabhijñā argument vertical—and manually create:

```text
1 Argument
3–5 core propositions
2–3 real rival interpretations
1 genuine crux
2 source passages
3 known misconception types
```

Then produce perhaps **12 gold interactions** over that one graph:

```text
pretest
identify proposition
wrong speaker
term discrimination
missing premise
argument assembly
rival reading
support vs attack
retract premise
predict downstream impact
identify crux
unseen transfer case
```

And give every option a diagnostic mapping.

That's our educational equivalent of the five Argument Golds.

Then test:

```text
Can somebody who knows nothing
actually reconstruct the argument?
```

If they can, we've got something.

If not, the failures force the Education IR.

**Gold must force ontology again.**

---

# 30. The single cleanest statement of the whole thing

I think this is now the education north star:

> **Pāṭala does not test whether a learner remembers what a tradition says. It places the learner inside the evidential and argumentative structure that made the tradition's distinctions necessary, then records what they can actually reconstruct, discriminate, manipulate, transfer, and ground.**

And the architecture is almost absurdly coherent:

```text
SCHOLAR
constructs/reviews argument
        ↓
PĀṬALA
stores argument
        ↓
EDUCATION COMPILER
turns argument into manipulations
        ↓
LEARNER
reconstructs argument
        ↓
MASTERY EVIDENCE
records what was demonstrated
        ↓
PEDAGOGICAL ENGINE
finds missing structure
        ↓
NEXT MANIPULATION
```

The same graph becomes **scholarship, benchmark, education, assessment, tutoring and media**.

That is the first point in this project where I think the phrase **“one evidence graph from Sanskrit to scholarship to human understanding”** might actually be more accurate than the old Sanskrit→scholarship→media framing.
