Yes. The platform we are converging on is not “Brilliant, but for Sanskrit.” It is closer to:

> **Brilliant interaction design × intelligent tutoring × Sanskrit language laboratory × Pāṭala epistemic graph × scholarly provenance.**

The web research makes the build much clearer. Most of the generic platform already exists in reusable pieces. The thing worth inventing is the **education compiler that turns Pāṭala’s scholarly objects into manipulations that diagnose understanding**.

## The full stack I would build

| Layer                    | Use                                       | Build vs reuse                          |
| ------------------------ | ----------------------------------------- | --------------------------------------- |
| Scholarly truth/evidence | Pāṭala canonical graph                    | **OWN**                                 |
| Education compiler       | argument → diagnostic interaction         | **OWN**                                 |
| Interaction runtime      | MCQ, graph manipulation, source exercises | mostly own UX, reuse rendering libs     |
| Learner model            | skill/mastery estimates                   | reuse BKT ideas initially               |
| Memory scheduler         | long-term retrieval                       | **reuse FSRS**                          |
| AI tutor                 | Socratic guidance/explanation             | model-agnostic wrapper                  |
| Sanskrit NLP             | morphology, segmentation, transliteration | **reuse ensemble**                      |
| Sanskrit speech          | pronunciation, listening, speaking        | hybrid; likely **Pāṭala-specific work** |
| Search/RAG               | source retrieval                          | reuse generic engine                    |
| Authoring                | scholar/pedagogy editors                  | reuse editor/collaboration              |
| Analytics                | learning-event telemetry                  | reuse                                   |
| Experimentation          | compare pedagogical strategies            | reuse                                   |
| LMS standards            | external schools/universities             | adapters only                           |
| Media                    | diagrams, audio, animations               | compiled projection                     |
| Mobile/offline           | learner app                               | later projection of same runtime        |

The important point is that **none of these should create another source of scholarly truth**.

---

# 1. The learning runtime: steal Brilliant's principles, not its structure

Brilliant currently emphasizes single-concept interactive lessons, pretesting before instruction, hands-on manipulation, progressively harder problems, instant custom feedback, visual representations, personalized next steps, and restrained gamification. Its tutor Koji can also see the current interactive state rather than operating as an isolated chatbot. ([Brilliant][1])

That maps almost perfectly onto Pāṭala:

```text
BRILLIANT

mathematical structure
      ↓
interactive manipulation
      ↓
learner response
      ↓
diagnosis
      ↓
next manipulation


PĀṬALA

epistemic structure
      ↓
interactive manipulation
      ↓
learner response
      ↓
epistemic diagnosis
      ↓
next manipulation
```

The killer difference remains:

> Brilliant lets you manipulate **mathematical relationships**.
> Pāṭala lets you manipulate **commitments, evidence and arguments**.

So don't build an H5P-style “quiz platform” as the product.

Build an **Epistemic Interaction Runtime**.

---

# 2. The interaction primitives

I would make this an actual reusable frontend package:

```text
@patala/interactions
```

with approximately:

```text
ChoiceInteraction
MultiChoiceInteraction
OrderingInteraction
MatchingInteraction

PropositionSelect
EvidenceAttach
EvidenceReject

CommitmentClassify
SpeakerClassify

TermSenseChoose
TranslationCompare
SpanSelect

PremiseAttach
WarrantComplete
ArgumentAssemble

DefeaterChoose
AttackEdgeDraw

ScopeCompare
ModalityCompare

SemanticAlignment
DebateFrameMatch

PremiseRetract
ImpactPredict
CruxFind

SourceGround
SanskritAlign
TranslationRepair
```

The generic interactions already have precedent in H5P, which supports multiple choice, drag-and-drop, fill-in-the-blank, flash cards, timelines, interactive video, audio recording and other reusable interactive content types. H5P is therefore worth mining for interaction/content packaging ideas, but I would **not** make H5P the Pāṭala canonical runtime because its objects do not understand propositions, commitments, evidence or cruxes. ([GitHub][2])

---

# 3. Use Cytoscape.js for the argument simulator

This one is an unusually good fit.

Cytoscape.js gives us an actively maintained graph-theory model plus interactive web renderer; its current GitHub release stream is still active in 2026. ([GitHub][3])

For something like:

```text
P1 ──┐
P2 ──┼── INF1 ─── C
P3 ──┘
```

the student can:

* drag premises;
* connect edges;
* remove propositions;
* inspect dependencies;
* reveal evidence;
* collapse/expand argument subgraphs;
* compare two DebateFrames;
* watch conclusion states change.

The huge architectural win is:

```text
backend dependency graph
        ↓
same graph semantics
        ↓
Cytoscape presentation
```

rather than constructing fake educational diagrams.

---

# 4. Make every interaction compile from a scholarly object

This remains the heart.

```text
Proposition
     ↓
LearningClaim

Inference
     ↓
CompleteWarrant interaction

Commitment
     ↓
Who-is-asserting-this interaction

TermSense
     ↓
ChooseSense interaction

SemanticAlignment
     ↓
Same-question-or-not interaction

Defeater
     ↓
Which-objection-works interaction

Crux
     ↓
Retract-and-predict interaction

SourceAssertion
     ↓
Which-passage-supports-this interaction
```

And critically:

```text
wrong scholarly neighbor
      ↓
diagnostic distractor
```

The system should almost never ask an LLM:

> invent three plausible wrong answers.

It should ask:

```text
find:
nearest rival proposition
common scope inflation
known attribution inversion
alternative term sense
defeated inference
question mismatch
known misconception
```

That is a much more defensible multiple-choice generator.

---

# 5. Learner modelling: OATutor is the codebase to mine first

OATutor is the best immediately reusable intelligent-tutoring reference I found. It is open-source, uses Bayesian Knowledge Tracing, has configurable problem selection, problem→skill mappings, hints/scaffolding, A/B testing support and optional logging; its content model also explicitly separates problems, steps and tutoring pathways. ([GitHub][4])

Their architecture:

```text
Knowledge Component
      ↕
Problem
      ↕
Response
      ↓
BKT
      ↓
estimated mastery
      ↓
next problem
```

Pāṭala:

```text
LearningSkill
      ↕
LearningInteraction
      ↕
MasteryEvidence
      ↓
mastery reducer
      ↓
LearnerState
      ↓
next interaction
```

I would **copy the conceptual architecture, not their domain ontology**.

Start BKT-simple.

Do not start with giant deep knowledge-tracing models.

A 2026 experiment comparing adaptive strategies in a logic ITS found BKT-based and deep-RL adaptive policies both improved test performance over its non-adaptive condition, with different benefits by prior-knowledge group. It is promising evidence for adaptivity, not a reason to assume one algorithm universally wins. ([arXiv][5])

Our own data should eventually decide.

---

# 6. But Pāṭala mastery should be richer than “knows concept”

We need two dimensions.

```text
KNOWLEDGE

recognition
prakāśa
vimarśa
momentariness
apoha
spanda
śakti
memory
numerical identity


EPISTEMIC SKILLS

source locating
term discrimination
speaker attribution
commitment attribution
scope discrimination
warrant reconstruction
defeater recognition
semantic alignment
crux identification
source grounding
```

So the learner model becomes a sparse matrix:

```text
                           SKILL
                    TERM  SCOPE  CRUX  WARRANT
recognition          .91   .61   .42    .55
momentariness        .82   .73   .31    .48
vimarśa              .88   .40   —      .59
```

This is far more interesting than XP.

---

# 7. FSRS should own the memory scheduling problem

There is no reason for Pāṭala to invent another spaced repetition scheduler.

The Open Spaced Repetition project maintains FSRS implementations in Rust, Python, TypeScript, Go, Swift and other languages. Current FSRS-6 models learner memory using difficulty, stability and retrievability, and the project provides schedulers plus parameter optimization. ([GitHub][6])

Use it for things that genuinely depend on retention:

```text
technical terms
Sanskrit vocabulary
school/text chronology
definitions
important passages
argument components
distinctions
```

But don't reduce everything to flashcards.

For Pāṭala:

```text
FSRS says:
"this distinction is due for retrieval"

Education Engine says:
"what interaction best retrieves it?"
```

So instead of:

> What is pūrvapakṣa?

you can schedule:

> Here is an unseen paragraph. Which proposition is the author's commitment?

Same memory target.

Far stronger retrieval task.

---

# 8. Build a hierarchy of mastery evidence

This should become fundamental:

```text
E0  exposed
E1  recognized
E2  discriminated
E3  reconstructed
E4  explained
E5  applied
E6  transferred
E7  defended
E8  source-grounded
```

Then FSRS should schedule **an appropriate retrieval interaction**, not blindly repeat the original problem.

Example:

```text
Day 0
MCQ discrimination

Day 2
argument reconstruction

Day 8
new-context transfer

Day 25
source-grounding challenge
```

Now spaced repetition becomes spaced **epistemic performance**.

That feels much more Pāṭala.

---

# 9. AI tutor: take the Koji architecture lesson very seriously

Brilliant says Koji sees the actual learning environment and what the learner has done so far; its behavior/actions are custom to Brilliant rather than simply exposing a raw third-party model. ([Brilliant][7])

That is exactly what we need.

Not:

```text
chat(question)
```

but:

```text
TutorContext:
  learner_state
  current_interaction
  attempted_answers
  target_learning_claim
  misconception_candidates
  permitted_hints
  proposition_graph
  relevant_sources
  current_depth
```

Then the model chooses only from typed pedagogical actions:

```text
ASK_DISCRIMINATING_QUESTION
HIGHLIGHT_RELATION
REVEAL_HINT
SHOW_COUNTEREXAMPLE
REQUEST_JUSTIFICATION
SHOW_RIVAL_READING
DESCEND_TO_SOURCE
RECAP
GIVE_EXPLANATION
ABSTAIN
```

The LLM should not decide scholarly truth.

It uses Pāṭala's current state.

---

# 10. OpenTutor is worth stealing implementation patterns from

OpenTutor already combines local/self-hosted AI tutoring, quizzes, FSRS, learner adaptation and an experimental knowledge graph. It also supports multiple LLM providers instead of hard-binding itself to one model. ([GitHub][8])

Useful patterns to steal:

```text
provider abstraction
quiz/interaction routing
FSRS integration
knowledge graph ↔ learner state
Socratic tutor mode
source-cited answers
adaptive sequencing
```

Do **not** inherit:

```text
PDF → LLM-generated truth graph
```

because Pāṭala has a vastly stronger substrate.

Our flow is:

```text
adjudicated scholarly graph
        ↓
learning compiler
```

not:

```text
upload PDF
↓
hope model extracted concepts properly
```

---

# 11. Sanskrit should become an entire interactive language laboratory

This is where Pāṭala can get absurdly strong.

A source passage can expose layers:

```text
Sanskrit
  │
  ├ orthography
  ├ transliteration
  ├ audio
  ├ tokenization
  ├ sandhi
  ├ morphology
  ├ compound analysis
  ├ lemma
  ├ dictionary senses
  ├ term history
  ├ literal gloss
  ├ translation
  ├ alternate reading
  └ philosophical role
```

And learners can interact with every level.

Example:

```text
तदेतत् ...
```

Tap word:

```text
surface
↓
sandhi expansion
↓
lemma
↓
morphological possibilities
↓
historical senses
↓
occurrences in corpus
↓
translation choice here
↓
why that choice matters to argument
```

This is where Ambuda is extremely worth studying. Ambuda is actively building a digital Sanskrit library and maintains Vidyut, its Sanskrit software infrastructure; its repositories also expose cleaned DCS/GRETIL-derived resources. ([GitHub][9])

---

# 12. Sanskrit analysis stack: keep the ensemble philosophy

For production Sanskrit analysis, I would continue the existing Pāṭala approach rather than betting everything on one parser.

```text
Vidyut
   │
   ├── compare
   │
Heritage
   │
   └── disagreement
          ↓
     AnalysisWitness[]
```

The Sanskrit Heritage system still exposes its Sanskrit dictionary/reader/grammar tooling and remains a useful independent analysis witness. ([Sanskrit][10])

AI4Bharat also maintains Indic transliteration tooling supporting Sanskrit and multilingual translation tooling that includes Sanskrit; those are useful auxiliary adapters, particularly for script handling and multilingual educational projection, but neither should override Pāṭala's philological decisions. ([GitHub][11])

For students, analyzer disagreement becomes an educational feature:

> Vidyut and Heritage disagree here. Why?

That is actually advanced Sanskrit pedagogy.

---

# 13. Sanskrit speech is currently a real opportunity

This was one of the most interesting findings.

There is **not yet an obvious polished open-source Sanskrit equivalent of modern IndicF5**.

AI4Bharat's current IndicF5 model advertises 11 languages—Assamese, Bengali, Gujarati, Hindi, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil and Telugu—and does not list Sanskrit. Its earlier Indic-TTS release lists 13 languages and likewise does not list Sanskrit. ([GitHub][12])

Azure likewise does not currently expose a dedicated Sanskrit neural TTS voice according to Microsoft's own support response and current language tables. ([Microsoft Learn][13])

Meanwhile, Sanskrit-specific research exists. A 2022 low-resource Sanskrit Tacotron2/WaveGlow transfer-learning system trained from only 2.5 hours of Sanskrit speech reported a mean opinion score of 3.38 from 37 evaluators with Sanskrit knowledge. ([arXiv][14])

More interestingly, 2025 work on linguistically related zero-shot Indian-language TTS reported intelligible/natural Sanskrit generation by leveraging related-language synthesis and shared phone representations. ([arXiv][15])

So I would **not** consider Sanskrit TTS solved.

I would make it a Pāṭala subproject.

---

# 14. The Sanskrit TTS system we actually want

Not merely:

```text
Devanagari → pleasant voice
```

We need:

```text
Sanskrit text
   ↓
normalized canonical reading
   ↓
sandhi-aware phonological representation
   ↓
pronunciation units
   ↓
prosodic mode
   ├ prose
   ├ verse
   ├ slow pedagogical
   └ possibly recitation tradition
   ↓
speech synthesizer
   ↓
word/phoneme timestamps
```

And importantly store:

```text
AudioWitness:
  source_text_version
  pronunciation_policy
  voice
  model
  model_version
  phonological_input
  prosody_mode
  generated_audio_hash
```

Eventually have **scholars/Sanskrit speakers adjudicate pronunciation**.

That creates a novel dataset too.

---

# 15. Separate ordinary Sanskrit pronunciation from Vedic recitation

Very important architecturally.

Classical Sanskrit reading:

```text
phonemes
sandhi
vowel length
aspiration
retroflexion
accent-neutral prose prosody
```

Vedic recitation can involve accentual and recitational traditions that are not equivalent to generic Sanskrit TTS.

Therefore:

```text
PronunciationPolicy:
  CLASSICAL_PROSE
  CLASSICAL_VERSE
  PEDAGOGICAL_SLOW
  VEDIC_[specific tradition]
```

Never let a generic TTS model silently fabricate Vedic correctness.

This fits Pāṭala's provenance discipline perfectly.

---

# 16. Sanskrit ASR is in a better position than TTS

AI4Bharat's IndicConformer currently lists a Sanskrit (`sa`) monolingual ASR checkpoint among models for the 22 scheduled Indian languages, under an MIT-licensed repository. ([GitHub][16])

There is also 2025 Sanskrit-specific Whisper transfer-learning research reporting a 15.42% WER on the Vāksañcaya dataset. ([arXiv][17])

So pronunciation exercises can eventually become:

```text
learner reads Sanskrit
       ↓
ASR / phoneme alignment
       ↓
compare expected phonology
       ↓
feedback
```

But I would avoid generic:

> pronunciation = 83%

Instead:

```text
vowel length       ✓
retroflexion        ?
aspiration          ✗
word segmentation  ✓
```

and preserve uncertainty.

---

# 17. The Sanskrit listening interaction could be excellent

Example:

Audio plays:

> Sanskrit phrase

Student sees:

```text
A ...
B ...
C ...
D ...
```

where options differ only in:

```text
short/long vowel
retroflex/dental
aspirated/unaspirated
sandhi boundary
```

Correct discrimination becomes evidence of phonological understanding.

Same educational philosophy again.

---

# 18. Authoring: use Tiptap rather than building an editor

Tiptap is currently an actively maintained headless ProseMirror-based editor framework with extensive extension support, and its open-source collaboration backend Hocuspocus uses Yjs. ([GitHub][18])

Perfect for:

```text
KnowledgePacket editor
scholar commentary editor
lesson framing
video script
explanatory prose
```

But the structured epistemic objects should **not live inside rich-text JSON**.

Instead:

```text
Tiptap document
   │
   ├ text nodes
   └ embedded references
        ↓
pt:proposition:...
pt:passage:...
pt:argument:...
pt:interaction:...
```

Rich text is the projection.

Graph remains canonical.

---

# 19. Collaboration: Yjs

Yjs provides CRDT shared data structures, offline/local persistence options, multiple editor bindings and network-independent synchronization. ([GitHub][19])

Use that for:

```text
collaborative lesson drafting
scholar commentary
review annotations
Workbench notes
```

Again:

> collaborative text changes are drafts/proposals.

They don't mutate scholarly authority.

---

# 20. Analytics: PostHog initially

PostHog currently bundles product analytics, session replay, feature flags, experiments, surveys, data pipelines, error tracking and LLM observability. ([GitHub][20])

That removes an absurd amount of platform work.

Track:

```text
interaction_started
interaction_answered

distractor_selected
hint_requested

explanation_opened
source_zoomed

argument_node_moved
premise_retracted

answer_revised

transfer_passed

review_due
review_completed

lesson_abandoned
lesson_resumed
```

But there is a Pāṭala-specific event we should own:

```text
MasteryEvidence
```

PostHog analytics event ≠ mastery evidence.

Mastery evidence has semantic meaning.

---

# 21. Experimentation: GrowthBook becomes interesting later

GrowthBook currently supports feature flags, A/B experimentation, Bayesian/sequential methods, CUPED and other experiment tooling, with SDKs across major platforms. ([GitHub][21])

This eventually lets us experimentally test:

```text
Explain then problem
       vs
Problem then explain

MCQ
       vs
construction

argument visualization
       vs
prose

Socratic hint
       vs
worked example

immediate correction
       vs
delayed self-correction
```

Measure:

```text
not clicks
not completion

but:

24h transfer
7d retention
misconception correction
source-grounding performance
```

This could become a serious research platform.

---

# 22. Learning events should eventually expose xAPI compatibility

ADL's current xAPI architecture defines learner activity/performance statements communicated to a Learner Record Store. ([ADLNet][22])

Don't make xAPI canonical.

Instead:

```text
Pāṭala MasteryEvidence
       ↓ adapter
xAPI statement
```

Why?

Because:

```text
xAPI:
Tom answered interaction 17

Pāṭala:
Tom demonstrated
SCOPE_DISCRIMINATION
against two adjudicated rival readings
on unseen source material
with no hint
```

Our semantics are much richer.

But interoperability is valuable later.

---

# 23. The content compiler becomes enormous leverage

Once we have:

```text
ResearchQuestion
LearningClaim
Argument
SourceEvidence
PrerequisiteGraph
MisconceptionGraph
```

we can render:

```text
DISCOVERY CARD
5 minute puzzle

LESSON
15 minute interaction sequence

DEEP DIVE
45 minute guided study

QUIZ
diagnostic fixture set

FLASHCARD
FSRS retrieval object

TUTOR SESSION
Socratic pathway

ARTICLE
progressive explanation

VIDEO
script + visual sequence

SHORT
one conceptual hook

SOURCE STUDY
advanced Sanskrit

TEACHER PACK
discussion + exercises
```

**One knowledge substrate.**

---

# 24. Media should be generated from interaction states

This is especially exciting given the wider Pāṭala/media work.

Imagine video:

```text
"What has to persist for recognition?"

P1 appears.
P2 appears.
Student-style options appear.

Cognition node disappears.

Argument collapses.

Buddhist alternative appears.

New edge grows.

CRUX highlights.
```

That visual already exists because we built it as an educational interaction.

So:

```text
interactive scene
      ↓
animation timeline
      ↓
video visual
```

The media engine can reuse the same state transitions.

That creates consistent visual grammar.

---

# 25. The three modes should remain

### DISCOVER

```text
5–10 min
no prerequisites
one amazing question
visual
interactive
aha-driven
```

Closest to Brilliant.

### LEARN

```text
adaptive
learner-state driven
FSRS
prerequisite paths
diagnostic interactions
```

Closest to intelligent tutoring.

### STUDY

```text
primary text
Sanskrit
apparatus
arguments
scholarship
source grounding
```

Closer to actual scholarship.

But they are **not three content libraries**.

```text
same graph
different depth
```

---

# 26. Add a fourth mode: PRACTICE

I now think this deserves separation:

```text
DISCOVER
"show me why this is fascinating"

LEARN
"teach this systematically"

PRACTICE
"make me demonstrate it"

STUDY
"take me to the evidence"
```

Practice becomes entirely learner-model driven.

---

# 27. Progressive epistemic zoom becomes the UI law

At any moment:

```text
simple claim
    ↓
technical statement
    ↓
proposition
    ↓
argument
    ↓
rival reading
    ↓
scholarship
    ↓
translation
    ↓
Sanskrit
    ↓
witness
```

The learner never hits:

> trust the lesson writer.

They can descend.

That is the philosophical equivalent of seeing your work in maths.

---

# 28. The AI teacher should also zoom *up* and *down*

Student:

> I don't understand this.

Tutor doesn't just generate more prose.

It chooses:

```text
ZOOM_UP
give intuitive example

ZOOM_SIDEWAYS
show analogy

ZOOM_DOWN
show exact argument

ZOOM_DOWN_MORE
show source

COMPARE
show rival answer

MANIPULATE
launch interaction
```

This gives us a **typed pedagogical action space**.

I would explicitly expose that to Hermes/agents.

---

# 29. The interaction compiler could become a genuine engine

Something like:

```python
compile_interactions(
    scholarly_object=ARG_002,
    targets=[
        "premise_identification",
        "warrant_reconstruction",
        "crux_detection"
    ],
    learner_level="novice",
)
```

returns:

```text
LI-001 pretest

LI-002 drag missing premise

LI-003 discriminate rival reading

LI-004 retract premise

LI-005 predict effect

LI-006 identify crux

LI-007 unseen transfer
```

Then **humans author/review the gold interactions**.

AI can propose.

Never publish huge automatic lesson dumps.

---

# 30. Use the same anti-theatre ladder for educational content

```text
GENERATED
↓
STRUCTURALLY_VALID
↓
SUBJECT_REVIEWED
↓
PEDAGOGICALLY_REVIEWED
↓
PILOTED
↓
MEASURED
↓
VALIDATED
```

Don't call:

```text
LLM generated quiz
```

“effective learning content.”

Exactly same principle as Pāṭala scholarship.

---

# 31. Gold learning fixtures become another moat

For every strong learning interaction:

```text
LearningFixture:
  target_learning_claim
  target_skill
  target_argument
  prerequisites

  prompt_state

  response_space

  correct_interpretation

  diagnostic_distractors

  misconception_mapping

  acceptable_reasoning

  mastery_evidence_level

  source_refs

  scholar_review
  pedagogy_review

  measured_outcomes
```

Over time:

```text
10,000 gold interactions
+
millions of responses
+
diagnostic misconception mappings
```

becomes a very valuable dataset.

---

# 32. Machine benchmark and human education should share the same deep fixtures

Still one of the best insights.

```text
             GOLD DISTINCTION
                 │
       ┌─────────┴─────────┐
       ↓                   ↓
 MODEL BENCHMARK       HUMAN EXERCISE
       │                   │
 model response        learner response
       ↓                   ↓
failure taxonomy     misconception taxonomy
```

Then compare.

Maybe models and humans systematically fail on different aspects.

That itself could become excellent research.

---

# 33. Architecture I would now settle on

```text
                        PĀṬALA
                           │
                   SCHOLARLY KERNEL
                           │
        ┌──────────────────┼────────────────────┐
        │                  │                    │
      SOURCE           ARGUMENT              REVIEW
        │                  │                    │
        └──────────────────┼────────────────────┘
                           ↓
                    EDUCATION COMPILER
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
     LearningClaim   Misconception       Prerequisites
         │             Graph                 │
         └─────────────────┼─────────────────┘
                           ↓
                  INTERACTION COMPILER
                           │
         ┌─────────┬───────┼────────┬─────────┐
         ↓         ↓       ↓        ↓         ↓
       MCQ       SOURCE   GRAPH    AUDIO      TUTOR
                STUDY     SIM
         │         │       │        │         │
         └─────────┴───────┼────────┴─────────┘
                           ↓
                     LearnerResponse
                           ↓
                     MasteryEvidence
                           ↓
                       LearnerState
                           │
                    ┌──────┴───────┐
                    ↓              ↓
                   BKT            FSRS
                    │              │
                    └──────┬───────┘
                           ↓
                  PEDAGOGICAL POLICY
                           ↓
                    NEXT INTERACTION
```

---

# 34. Recommended actual technology stack

For a low-cost build, I would currently choose:

```text
WEB
Next.js / React / TypeScript

INTERACTIVE GRAPH
Cytoscape.js

EDITOR
Tiptap

COLLABORATION
Yjs + Hocuspocus

INTERACTION ENGINE
Pāṭala custom React components
with H5P mined for patterns

LEARNER MODEL
simple BKT implementation
inspired by OATutor

MEMORY
FSRS-6

AI TUTOR
provider-independent LLM adapter
+ Pāṭala typed tutor actions

SANSKRIT MORPHOLOGY
Vidyut + Heritage witnesses

TRANSLITERATION
existing Indic/Sanskrit tooling

SANSKRIT ASR
IndicConformer as first baseline

SANSKRIT TTS
initial research/fine-tune track;
do not pretend generic Hindi TTS solves it

SEARCH
existing Pāṭala retrieval
→ later PaperQA/Tantivy candidate retrieval

ANALYTICS
PostHog

EXPERIMENTATION
PostHog initially
GrowthBook later if experiments become sophisticated

BENCHMARKS
Inspect AI

AUTHORING
Tiptap
+ canonical structured-object embeds

EXPORT
xAPI/LTI/QTI adapters later
never canonical

PROVENANCE
existing Pāṭala graph
```

Many of these components are explicitly designed to be embedded or swapped: Cytoscape provides a graph model/renderer, Tiptap is headless/extensible, Yjs is network-agnostic, OATutor cleanly separates skill models from content, FSRS has several language implementations, and PostHog/GrowthBook expose APIs/SDKs for instrumentation and experimentation. ([GitHub][3])

---

# 35. What I would **not** build

This is almost as important.

```text
NO custom rich-text editor

NO custom spaced repetition algorithm

NO custom generic analytics

NO generic A/B testing engine

NO LMS

NO conference peer-review platform

NO generic RAG framework

NO generic graph renderer

NO general Sanskrit dictionary database
when good source data exists

NO proprietary closed lesson format
that can't resolve to graph objects

NO giant bespoke model runtime

NO auto-generated 100,000-lesson content farm
```

Put engineering effort into:

```text
Epistemic Interaction IR

LearningClaim

Diagnostic distractors

Misconception graph

MasteryEvidence

Argument simulator

Progressive epistemic zoom

Education compiler

Sanskrit interactive reader

Sanskrit pronunciation layer

scholar → education correction propagation
```

That's the novel material.

---

# 36. The particularly insane Sanskrit reader interaction

I think this could itself be a flagship.

Student reads IPVV:

```text
[SANSKRIT]
      ↓ click
[TOKEN]

surface
lemma
morphology
sandhi
compound
dictionary
historical sense
      ↓
[TRANSLATION OPTIONS]
      ↓
why this reading?
      ↓
[TRANSLATION DECISION]
      ↓
what claim depends on it?
      ↓
[PROPOSITION]
      ↓
what argument depends on it?
      ↓
[ARGUMENT]
      ↓
what changes if translated differently?
      ↓
[IMPACT SIMULATION]
```

**That is Sanskrit learning + philosophy learning + textual criticism in one interaction.**

I don't know another mainstream learning platform built around that depth of reversible evidential structure.

---

# 37. The theory beneath it is actually coherent

You end up combining several established educational ideas:

```text
PRETESTING
try before being told

ACTIVE LEARNING
manipulate rather than consume

SCAFFOLDING
give support

FADING
remove that support

RETRIEVAL PRACTICE
reconstruct later

SPACING
schedule later retrieval

DISCRIMINATION
separate close alternatives

TRANSFER
perform on unseen material

ADAPTIVITY
target learner weakness

SOCRATIC GUIDANCE
questions rather than answer dumps

METACOGNITION
show why Pāṭala thinks you know something
```

Brilliant itself explicitly describes pretesting, hands-on manipulation, minimizing cognitive load initially, instant feedback and progressive difficulty; modern ITS research continues to explore adaptive scaffolding strategies. ([Brilliant][1])

Our novelty is **binding those operations to an inspectable scholarly argument/evidence graph**.

---

# 38. The actual flywheel becomes ridiculous

```text
SCHOLARSHIP
    ↓
epistemic graph
    ↓
learning claims
    ↓
interactions
    ↓
learners
    ↓
response evidence
    ↓
misconception data
    ↓
better pedagogy
    ↓
hard distinctions
    ├──────────────→ machine benchmarks
    │
    ↓
scholar questions
    ↓
corrections
    ↓
better epistemic graph
```

Then:

```text
MEDIA
```

comes out of the same graph and interactions.

And:

```text
Sanskrit TTS / pronunciation data
```

becomes another unique asset.

---

# 39. There are arguably four distinct moats now

```text
1. SCHOLARLY MOAT
sources + provenance + expert correction

2. MACHINE MOAT
benchmarks + difficult adversarial fixtures

3. PEDAGOGICAL MOAT
diagnostic interactions + misconception graph

4. LANGUAGE MOAT
Sanskrit alignment + pronunciation + speech +
historical term-sense data
```

And all four compound.

This is much harder to copy than “we translated a lot of Sanskrit.”

---

# 40. The best first education prototype is still tiny

Don't build the platform yet.

Build:

```text
ONE ARGUMENT

ARG-002 or whichever Agent1 gold
is currently strongest
```

Then make a **10–15 minute Brilliant-quality interactive**:

```text
1  strange opening puzzle

2  choose what recognition requires

3  expose temporal problem

4  drag missing premise

5  reveal historical position

6  introduce rival Buddhist solution

7  classify whether it actually answers same question

8  retract premise

9  watch argument change

10 identify crux

11 descend into translation

12 descend into Sanskrit

13 answer source-level challenge

14 unseen transfer problem

15 show "what you demonstrated"
```

At the end:

```text
YOU DEMONSTRATED

✓ distinction: recognition ≠ memory
✓ reconstruction: INF-X
✓ crux identification
✓ rival-position discrimination
✓ unseen transfer

NOT YET DEMONSTRATED

○ source grounding
○ Sanskrit term discrimination
```

That screen alone could feel completely unlike normal educational software.

---

## The highest-value new technical project

After this search, I'd move **Sanskrit speech** much higher than I had it.

There is strong Sanskrit ASR infrastructure to try immediately, but the modern open-source TTS projects I found do **not** give us an obvious high-quality Sanskrit production voice; Sanskrit-specific research instead suggests low-resource fine-tuning and cross-lingual phonological transfer are feasible. ([GitHub][16])

That means Pāṭala could plausibly build a unique:

> **scholar-reviewed Sanskrit speech corpus + pronunciation engine + pedagogical TTS/ASR layer**

and use it across every text.

That becomes useful for:

```text
reader audio
word pronunciation
chant/prose distinction
listening tests
pronunciation practice
video narration
accessibility
Sanskrit learning
alignment research
```

So my final architecture would now treat **Education + Sanskrit Speech** as first-class projections of the scholarly factory—not side features.

And the strongest product principle remains:

> **Every abstraction should be reversible, and every assessment should force the learner to demonstrate some structure already represented in the scholarly graph.**

That is how Pāṭala can become genuinely Brilliant-like without becoming a Brilliant clone.

This education architecture is strong, and it fits Pāṭala unusually well. The main thing I would change now is **sequence**. The document is broad enough that it could easily become another huge parallel build. The right move is to compile education **from the verified scholarly stack**, not build an education platform alongside it. 

The core architecture I would lock is:

```text
SCHOLARLY CORE
SOURCE → T1 → L0 → ARGMAP → L2 → L200 → C1
                         ↓
                  Proposition / Argument
                         ↓
                  LearningClaim IR
                         ↓
                Interaction Compiler
                         ↓
             LearnerResponse / MasteryEvidence
                         ↓
                  LearnerState
                    ↙       ↘
                  BKT       FSRS
                    \       /
                Pedagogical Policy
                         ↓
                 next interaction
```

The key design law from the document is exactly right:

> **Education is a projection of Pāṭala objects, not a separate knowledge base.** 

That should be enforced technically.

## The highest-value thing to build first

Do **not** start with Sanskrit TTS, analytics, FSRS, BKT, Tiptap, collaboration, mobile, or a course builder.

Build this:

```text
EducationCompiler v0
```

Input:

```json
{
  "argument_ref": "ARG-GOLD-002",
  "learner_level": "introductory",
  "targets": [
    "commitment_attribution",
    "premise_identification",
    "warrant_reconstruction",
    "crux_detection"
  ]
}
```

Output:

```text
LearningPacket
├── LearningClaims
├── prerequisite skills
├── misconception candidates
├── 6–10 interaction specs
├── correct interpretations
├── diagnostic distractors
├── source refs
├── progression order
└── epistemic ceiling
```

That gives you the actual novel compiler.

Everything else can attach later.

## The object model is the important part

I would define four canonical education objects first.

### `LearningClaim`

```text
learning_claim_id
derived_from[]
content
claim_type
difficulty
prerequisites[]
source_refs[]
epistemic_ceiling
```

Example:

```text
"The learner can distinguish an author's own commitment
from an objection the author is reporting."
```

### `LearningSkill`

```text
skill_id
type:
  TERM_DISCRIMINATION
  SPEAKER_ATTRIBUTION
  COMMITMENT_ATTRIBUTION
  SCOPE_DISCRIMINATION
  WARRANT_RECONSTRUCTION
  DEFEATER_RECOGNITION
  CRUX_IDENTIFICATION
  SOURCE_GROUNDING
```

### `LearningInteraction`

```text
interaction_id
targets[]
derived_from[]
interaction_type
prompt_state
response_space
diagnostic_map
correct_state
hints[]
source_refs[]
review_state
```

### `MasteryEvidence`

```text
learner
skill_ref
learning_claim_ref
interaction_ref
difficulty
response
correctness
hint_level
transfer_status
timestamp
```

This is the native layer. FSRS/BKT/PostHog should consume it, not define it.

## The interaction runtime should start tiny

The file proposes a big primitive vocabulary.  I would start with six:

```text
Choice
SpanSelect
SpeakerClassify
PremiseAttach
ArgumentAssemble
PremiseRetract
```

Those are enough to demonstrate that Pāṭala can teach **structure**, rather than simply generating quizzes.

Then add:

```text
TermSenseChoose
SourceGround
CruxFind
TranslationRepair
```

after the first prototype works.

## ARG-GOLD-002 is probably the correct first demo

The document's proposed 10–15 minute interactive is basically the right prototype. 

I would make it deliberately small:

```text
1. puzzle:
   Which claim is actually being defended?

2. speaker attribution:
   author / opponent / reconstructed?

3. premise select:
   which statement does the response depend on?

4. missing warrant:
   connect premise → conclusion

5. rival position:
   is it answering the same question?

6. retract one premise:
   what downstream claim changes?

7. crux:
   which commitment controls the disagreement?

8. source zoom:
   show L2 → T1/L0 → Sanskrit

9. unseen transfer:
   same skill, different passage
```

If this is excellent, you've proven the educational thesis.

If it's boring, building a whole LMS would have been wasted effort.

## The most important moat in the education layer is not adaptive scheduling

It's this:

```text
wrong answer
    ↓
known epistemic neighbor
```

instead of:

```text
LLM invents distractor
```

For example, a wrong answer can be sourced from:

* rival proposition;
* wrong speaker;
* known scope inflation;
* wrong technical sense;
* defeated inference;
* false contradiction;
* omitted qualifier;
* alternative DebateFrame.

That means learner mistakes become meaningful because they map back into Pāṭala's own failure taxonomy.

This is very distinctive.

## Agent responsibilities

I would **not put education under Agent 2**.

Agent 2 should remain:

```text
produce + maintain canonical scholarly objects
```

Agent 1:

```text
prove/evaluate scholarly and educational correctness
```

Agent 3, the Hermes coordinator we just discussed:

```text
route work, not build pedagogy
```

I would eventually create an **Agent 4: Education Compiler** once the first manual prototype proves useful.

Its responsibility:

```text
PĀṬALA objects
↓
LearningClaim
↓
LearningInteraction proposal
↓
pedagogy fixtures
```

But authority remains:

```text
Agent4 proposes
Agent1 verifies epistemic fidelity
pedagogy reviewer validates teaching quality
```

That keeps the architecture clean.

## Sanskrit reader comes before Sanskrit speech

The Sanskrit-language-lab section in the document is excellent, but I would reorder it.

Build:

```text
Sanskrit source
↓
token click
↓
lemma
↓
morphology
↓
sense
↓
translation decision
↓
proposition
↓
argument
```

first. 

That leverages assets Pāṭala already possesses.

Then add audio:

```text
token → pronunciation
passage → slow reading
learner speech → ASR feedback
```

TTS/ASR becomes much more valuable once the interactive reader already exists.

## BKT + FSRS should remain replaceable adapters

The document gets this right. 

I'd structure:

```text
MasteryReducer interface
├ BKT-v1
├ simple empirical mastery
└ later IRT / DKT / RL

MemoryScheduler interface
└ FSRS
```

Never put BKT fields directly into canonical learner objects.

Then you can compare models later.

## The strongest educational research experiment

Once you have ~100 good interactions, test:

```text
A: explanation → question

B: question → explanation

C: manipulation → explanation

D: source-grounding manipulation → explanation
```

Measure:

```text
immediate accuracy
24h transfer
7d retention
new-passage performance
source-grounding ability
```

Not engagement.

That could turn the educational system into a genuine experimental platform.

## The real endgame

The most powerful concept in the attached document is not “Brilliant for Sanskrit.”

It is this:

```text
SCHOLAR CORRECTION
      ↓
canonical object changes
      ↓
argument changes
      ↓
LearningClaim becomes stale
      ↓
affected interactions become stale
      ↓
lesson regenerated/reviewed
      ↓
learner-facing explanation updates
```

That is extraordinary if you get it working.

A normal education platform has:

```text
lesson.docx
```

Pāṭala could have:

```text
lesson
→ learning claim
→ proposition
→ argument
→ translation decision
→ source span
→ Sanskrit
```

and every arrow remains inspectable.

So my execution order would be:

```text
E0  freeze Education IR
E1  ARG-GOLD-002 → LearningClaims
E2  compile 6–10 interactions
E3  build minimal React interaction runtime
E4  build progressive source zoom
E5  MasteryEvidence logging
E6  simple learner state
E7  FSRS
E8  BKT
E9  AI tutor typed actions
E10 Sanskrit interactive reader
E11 analytics/experiments
E12 speech
E13 authoring/collaboration
E14 full education platform
```

The crucial constraint is: **prove that manipulating Pāṭala's epistemic structures is actually a compelling learning experience before building the surrounding platform.**


[1]: https://brilliant.org/about/?utm_source=chatgpt.com "About | Brilliant"
[2]: https://github.com/h5p/h5p-wordpress-plugin?utm_source=chatgpt.com "GitHub - h5p/h5p-wordpress-plugin: Adds support for H5P Content in WordPress. · GitHub"
[3]: https://github.com/cytoscape/cytoscape.js/?utm_source=chatgpt.com "GitHub - cytoscape/cytoscape.js: Graph theory (network) library for visualisation and analysis · GitHub"
[4]: https://github.com/CAHLR/OATutor?utm_source=chatgpt.com "GitHub - CAHLR/OATutor: Open Source Intelligent Tutoring System w/ BKT (ReactJS and Firebase) · GitHub"
[5]: https://arxiv.org/abs/2602.07308?utm_source=chatgpt.com "Adaptive Scaffolding for Cognitive Engagement in an Intelligent Tutoring System"
[6]: https://github.com/open-spaced-repetition/fsrs-rs?utm_source=chatgpt.com "GitHub - open-spaced-repetition/fsrs-rs: FSRS for Rust, including Optimizer and Scheduler · GitHub"
[7]: https://brilliant.org/help/features/?utm_source=chatgpt.com "Product Features - Help Center | Brilliant"
[8]: https://github.com/zijinz456/OpenTutor?utm_source=chatgpt.com "GitHub - zijinz456/OpenTutor: The first block-based adaptive learning workspace that runs locally. Upload any material → get AI-generated notes, quizzes, flashcards, and an adaptive tutor. Open source, self-hosted, 10+ LLM providers. · GitHub"
[9]: https://github.com/ambuda-org?utm_source=chatgpt.com "Ambuda · GitHub"
[10]: https://sanskrit.inria.fr/cgi-bin/SKT/sktindex.cgi?utm_source=chatgpt.com "Sanskrit Heritage Dictionary"
[11]: https://github.com/ai4bharat/IndicTrans2?utm_source=chatgpt.com "GitHub - AI4Bharat/IndicTrans2: Translation models for 22 scheduled languages of India · GitHub"
[12]: https://github.com/AI4Bharat/IndicF5?utm_source=chatgpt.com "GitHub - AI4Bharat/IndicF5 · GitHub"
[13]: https://learn.microsoft.com/en-in/answers/questions/5614654/sanskrit-text-to-sanskrit-speech-coversion-using-a?utm_source=chatgpt.com "Sanskrit text to Sanskrit speech coversion using Azure text to speech services - Microsoft Q&A"
[14]: https://arxiv.org/abs/2212.03558?utm_source=chatgpt.com "Low-Resource End-to-end Sanskrit TTS using Tacotron2, WaveGlow and Transfer Learning"
[15]: https://arxiv.org/abs/2506.03884?utm_source=chatgpt.com "Kinship in Speech: Leveraging Linguistic Relatedness for Zero-Shot TTS in Indian Languages"
[16]: https://github.com/AI4Bharat/IndicConformerASR?utm_source=chatgpt.com "GitHub - AI4Bharat/IndicConformerASR · GitHub"
[17]: https://arxiv.org/abs/2501.10024?utm_source=chatgpt.com "Automatic Speech Recognition for Sanskrit with Transfer Learning"
[18]: https://github.com/ueberdosis/tiptap?utm_source=chatgpt.com "GitHub - ueberdosis/tiptap: The headless rich text editor framework for web artisans. · GitHub"
[19]: https://github.com/yjs/docs?utm_source=chatgpt.com "GitHub - yjs/docs · GitHub"
[20]: https://github.com/PostHog/posthog?utm_source=chatgpt.com "GitHub - PostHog/posthog: 🦔 PostHog is an all-in-one developer platform for building successful products. We offer product analytics, web analytics, session replay, error tracking, feature flags, experimentation, surveys, data warehouse, a CDP, and an AI product assistant to help debug your code, ship features faster, and keep all your usage and customer data in one stack. · GitHub"
[21]: https://github.com/growthbook/growthbook?utm_source=chatgpt.com "GitHub - growthbook/growthbook: Open Source Feature Flags, Experimentation, and Product Analytics · GitHub"
[22]: https://www.adlnet.gov/guides/tla/service-definitions/?utm_source=chatgpt.com "Introduction | Advanced Digital Learning Initiative"
