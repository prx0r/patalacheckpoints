Yes. After looking at Brilliant, Khan Academy/Khanmigo, current intelligent-tutoring research, knowledge tracing, argument/concept mapping, and the more interesting open-source systems, I think there is a **very strong model for Pāṭala Education**.

The important conclusion is:

> **Do not make “Brilliant for Tantra.” Build Brilliant’s learning loop on top of Pāṭala’s epistemic graph.**

That difference is enormous.

## Brilliant is the right product inspiration

Brilliant’s current philosophy is unusually aligned with what we want: one concept at a time, visual representations, active problem solving, instant feedback, pretesting before explanation, scaffolding that gradually disappears, targeted review, and personalized learning paths. Brilliant explicitly says it wants learners doing the thinking rather than consuming walls of text. ([Brilliant][1])

Their basic loop is approximately:

```text
CONFRONT PROBLEM
      ↓
MAKE A GUESS
      ↓
MANIPULATE / REASON
      ↓
GET SPECIFIC FEEDBACK
      ↓
SEE THE PRINCIPLE
      ↓
SOLVE A NEAR-NEIGHBOR
      ↓
REMOVE SCAFFOLDING
      ↓
RETRIEVE IT LATER
```

That is substantially better than:

```text
WATCH VIDEO
READ TEXT
ANSWER 5 MULTIPLE CHOICE QUESTIONS
```

And there is reasonable learning-science backing for the underlying pieces: worked examples can lower unnecessary cognitive burden for novices; support should fade as proficiency rises; retrieval practice improves later retention; and spaced/distributed practice generally outperforms massed study. ([PubMed][2])

### But Brilliant has a huge advantage: mathematics is manipulable

You can drag a triangle.

Change a probability.

Rotate a vector.

Move a point on a function.

The learner directly manipulates the structure being learned.

So the central design question for Pāṭala is:

> **What is the humanities/philosophy equivalent of dragging the triangle?**

I think we actually have the answer.

# You manipulate the argument

Not just read it.

Imagine learning Utpaladeva.

Instead of:

> “Utpaladeva argues that recognition requires a persistent subject…”

Pāṭala presents:

```text
A person recognizes:
"I saw this before."

Which must remain the same?

[A] the object
[B] the current cognition
[C] the previous cognition
[D] the recognizer
```

Pick one.

Then:

> Suppose the previous and present cognitions are numerically different.
> How does the present cognition know the earlier experience was **mine**?

You choose an answer.

Then the argument graph begins assembling visually:

```text
earlier cognition       current cognition
      │                       │
      └──── recognition ──────┘
                  │
                  ?
```

Drag:

```text
PERSISTING SUBJECT
```

into the missing position.

Then Pāṭala says:

> That's approximately Utpaladeva's move.

And now:

**Show me the Buddhist response.**

The structure transforms:

```text
persistent subject?
        ↓
NOT NECESSARY
        ↓
causal continuity of momentary cognitions
```

Now ask:

> Does this actually answer Utpaladeva?

And you have to identify the crux.

This is **Brilliant for philosophy** in a meaningful sense.

---

# The manipulable primitives already exist in Pāṭala

This is what makes the idea unusually coherent.

The education system doesn't need fake educational objects.

Its exercises manipulate the actual scholarly objects:

```text
Term
Sense
Passage
TranslationDecision
Proposition
Commitment
Evidence
Inference
Argument
DebateFrame
SemanticAlignment
Defeater
Crux
```

So interactive lesson types practically fall out of the ontology.

For example:

### `TERM_SENSE`

> What does `vimarśa` mean here?

Give three plausible readings.

Learner examines surrounding Sanskrit, period, author and parallels.

### `SPEAKER`

Display a passage:

> Who is committed to this proposition?

* Abhinavagupta
* the opponent
* commentator
* reconstructed premise

This directly teaches pūrvapakṣa/siddhānta discrimination.

### `GROUND_THE_CLAIM`

> Which source passage actually supports this claim?

Drag evidence to proposition.

### `SCOPE`

Compare:

> Consciousness is self-aware.

vs

> Cognition is self-aware insofar as...

Which overstates the source?

### `ARGUMENT`

Give premises.

Construct the missing inference.

### `DEFEATER`

> Which objection actually attacks the inference rather than changing the question?

### `SEMANTIC_ALIGNMENT`

> Do Dharmakīrti and Utpaladeva mean the same thing by cognition here?

### `CRUX`

> Flip exactly one assumption. Which destroys the conclusion?

**That last one could be unbelievably good.**

---

# There is actual evidence for the graph/argument side too

Concept mapping has been repeatedly studied as an educational technique, including systematic reviews and meta-analyses finding positive effects on academic achievement and critical-thinking outcomes, although strength and context vary by study. ([PubMed][3])

There is also work specifically using argument-map-supported debate to encourage deeper critical-thinking activity. ([PubMed][4])

And computational argumentation research has explicitly identified **richness, visualization, interactivity, and personalization** as important dimensions for educational argument feedback. ([arXiv][5])

So we're not inventing the premise that manipulating conceptual/argument structure can teach reasoning.

What Pāṭala adds is that the graph isn't an educational approximation.

**It is the same graph the scholarship lives in.**

---

# Then steal Intelligent Tutoring Systems rather than rebuilding adaptive learning

There is decades of ITS work underneath products like this.

The useful conceptual decomposition is approximately:

```text
DOMAIN MODEL
what can be known

STUDENT MODEL
what this learner probably knows

PEDAGOGICAL MODEL
what should happen next

INTERFACE
how the learner interacts
```

Knowledge Tracing is the field concerned with inferring a learner's evolving knowledge state from interactions. ([arXiv][6])

Pāṭala already gives us an unusually strong **domain model**.

That's normally one of the hard parts.

So add:

```text
PĀṬALA GRAPH
      +
LEARNER GRAPH
```

For every learner:

```text
concept: recognition
mastery: 0.82

concept: momentariness
mastery: 0.63

skill: distinguish attribution
mastery: 0.91

skill: identify scope inflation
mastery: 0.47

skill: reconstruct warrant
mastery: 0.34
```

Then choose the next activity accordingly.

---

# OATutor is probably the most directly reusable GitHub project

OATutor is an open-source intelligent tutoring system built specifically for research. It already implements Bayesian Knowledge Tracing, skill models, adaptive problem selection, hints/scaffolding, logging, content pools and A/B testing. ([GitHub][7])

Its content model is basically:

```text
problem
 ├ skill(s)
 ├ steps
 ├ hints
 └ tutoring pathway
```

And its mastery engine selects activities partly according to which associated knowledge components are weakest. ([GitHub][7])

That maps remarkably well:

```text
OATutor                  Pāṭala

KnowledgeComponent   →   Concept / reasoning skill
Problem              →   LearningInteraction
Hint                  →   Evidence/scaffold
SkillModel            →   educational graph projection
BKT mastery           →   LearnerState
Problem selection     →   NextLearningAction
```

I would **mine this heavily** rather than inventing adaptive mastery machinery from nothing.

Not necessarily fork the whole UI.

Reuse the ideas/code where appropriate.

---

# OpenTutor is almost eerily close to part of our desired stack

A newer open-source project, OpenTutor, combines an adaptive workspace, AI tutoring with source citations, quizzes, FSRS spaced repetition, a knowledge graph, learner-state adaptation and multiple LLM providers. It labels some of its knowledge-graph-aware adaptation features experimental, which is exactly how we should treat similar machinery initially. ([GitHub][8])

Its loop is basically:

```text
material
→ teach
→ practice
→ remember learner state
→ schedule review
```

Useful.

But Pāṭala's huge difference is:

```text
OpenTutor:
PDF → generated knowledge structure

Pāṭala:
reviewed scholarly graph
→ educational projection
```

That is a completely different quality of substrate.

OpenTutor's graph is there to tutor.

**Pāṭala's graph exists independently as scholarship.**

That's the moat.

---

# There are also KG-RAG tutoring systems

Recent work on knowledge-graph-enhanced RAG tutoring argues that semantic-vector retrieval alone misses important conceptual relationships, and instead expands retrieval through knowledge-graph relations. A published KG-RAG tutor study reported improved assessment outcomes over its comparison setup, though it's one study and should not be treated as universal proof of the architecture. ([arXiv][9])

There is a corresponding open implementation that combines vector retrieval and graph traversal for tutoring. ([GitHub][10])

Again, Pāṭala already has the better graph.

So:

```text
DON'T:

student asks question
→ embed question
→ top 5 chunks
→ LLM
```

Do:

```text
student question
      ↓
resolve ResearchQuestion
      ↓
identify concepts / prerequisite graph
      ↓
inspect learner state
      ↓
retrieve relevant:
  propositions
  arguments
  evidence
  translations
  passages
      ↓
choose pedagogical move
      ↓
generate response
```

That's much closer to an intelligent tutor.

---

# I think `ResearchQuestion` should become the curriculum primitive

This connects directly with the recursive-prerequisite work.

A recent RPKT proposal identifies an interesting problem: learners often don't know what prerequisite they are missing. It recursively discovers prerequisite concepts until it reaches the learner's knowledge boundary rather than requiring a completely fixed curriculum. ([arXiv][11])

Pāṭala can do an unusually disciplined form of this because our prerequisites aren't merely LLM hallucinations.

Imagine:

```text
QUESTION:
Why does recognition imply continuity?

needs:
├── recognition
├── memory
├── numerical identity
├── cognition
└── momentariness
```

Learner understands:

```text
recognition       ✓
memory            ✓
numerical identity ?
momentariness     ✗
```

So Pāṭala dynamically sends them:

```text
"What does Buddhist momentariness claim?"
```

Then comes back.

That is much better than a rigid module sequence.

---

# So the learner graph has two different kinds of mastery

This is important.

Most systems track **content knowledge**.

Pāṭala should track:

```text
CONTENT
───────
recognition
vimarśa
apoha
momentariness
śakti
spanda
36 tattvas

REASONING
─────────
identify proposition
distinguish speaker
recognize scope
find evidence
reconstruct warrant
distinguish support/attack
compare senses
identify crux
detect overstatement
```

Then somebody might be:

```text
Pratyabhijñā content       84%
argument reconstruction   39%
source criticism           61%
Buddhist background        42%
```

That's vastly more informative than:

> Lesson 17 complete.

---

# And don't use BKT blindly

Bayesian Knowledge Tracing is attractive because it's interpretable and battle-tested in intelligent tutors. OATutor uses it. ([GitHub][7])

But humanities knowledge is not always binary.

"Does learner know `vimarśa`?" is too crude.

I'd have learner state include at least:

```text
exposure
retrieval_strength
application
discrimination
explanation
transfer
```

For example:

```json
{
  "concept": "vimarsa",
  "recognition": 0.95,
  "recall": 0.82,
  "application": 0.61,
  "sense_discrimination": 0.43
}
```

You can start simple and empirically discover which dimensions predict later success.

Knowledge-tracing research itself still has unresolved tradeoffs between predictive performance and interpretability, so there is no reason to prematurely adopt the fanciest deep model. ([arXiv][12])

Start interpretable.

---

# Retrieval practice should be everywhere

This is one area where the evidence is strong enough to make it a default design principle.

Reviews find retrieval practice improves long-term retention compared with simple restudy, and applied reviews also support distributed/spaced practice. ([PubMed Central (PMC)][13])

Therefore after learning:

> What is a Commitment?

Don't show another explanation tomorrow.

Ask:

> In this passage, is Abhinavagupta asserting the claim or reporting an opponent?

And a week later:

> Why can't textual occurrence alone establish authorial commitment?

And later:

> Here's an unseen passage. Classify it.

That's progression:

```text
RECALL
↓
RECOGNITION IN CONTEXT
↓
APPLICATION
↓
TRANSFER
```

Much better.

---

# We should use scaffold fading too

For novices:

```text
Claim
↓
[choose evidence from 3 options]
```

Then:

```text
Claim
↓
highlight relevant sentence yourself
```

Then:

```text
Claim
↓
find supporting passage in document
```

Then:

```text
Claim
↓
search entire corpus
```

Same skill.

Decreasing scaffolding.

Worked-example and cognitive-load research supports giving novices substantial structure and progressively reducing support as competence develops. ([PubMed][2])

That is exactly Brilliant's interaction philosophy too. ([Brilliant][1])

---

# Another great Brilliant concept: pretest before explanation

Brilliant says its lessons often let the learner attempt something before being shown the procedure. ([Brilliant][1])

For Pāṭala this could be incredible.

Do not begin:

> “Here are the Buddhist and Śaiva positions on recognition.”

Begin:

## A thought experiment

> Yesterday you saw a blue vase.
> Today you see it again and think:
>
> **“That's the same vase I saw yesterday.”**
>
> Yesterday's cognition no longer exists.
>
> What makes today's recognition possible?

Options:

```text
A. the object
B. memory trace
C. causal continuity
D. a persisting recognizer
E. nothing needs to persist
```

Now you've got the student philosophizing **before they know which historical school says what**.

Then reveal:

```text
Interesting.

You have just entered a debate
Utpaladeva cares deeply about.
```

That can be unbelievably compelling.

---

# This is where humanities can actually beat Brilliant

STEM has manipulable systems.

But philosophy has something arguably richer:

**You can manipulate commitments.**

Change:

```text
P: cognitions are momentary
```

to:

```text
¬P
```

and let the graph update.

The learner can literally see:

```text
IF cognition persists
    ↓
argument A survives
argument B becomes unnecessary

IF cognition is momentary
    ↓
recognition problem appears
    ↓
possible solutions:
       causal continuity
       memory disposition
       persistent subject
```

This is Pāṭala's dependency engine repurposed as an **interactive philosophical simulator**.

That is the feature I would put money behind.

---

# Call it “counterfactual learning”

Instead of only asking:

> Which answer is correct?

Ask:

> **What changes if this assumption is false?**

That's precisely what our Crux machinery does.

A lesson could show:

```text
CONCLUSION
Recognition requires a persisting knower.

supporting graph:
P1 ─┐
P2 ─┼→ I1 → C
P3 ─┘
```

Learner clicks P2:

**RETRACT**

Graph recomputes.

```text
C loses support.
```

Then:

> P2 is therefore load-bearing.

They have just *experienced* what a crux is.

No lecture needed.

That's the Pāṭala equivalent of Brilliant changing a variable in a physics simulation.

---

# Socratic AI is useful, but chat should not be the product

There is active research on constraining LLMs to behave more like Socratic tutors rather than answer machines. Recent systems use structured questioning, reflection prompts and course grounding, and some report encouraging early results. ([arXiv][14])

Khan Academy is similarly treating AI tutoring as something that requires continuous empirical testing rather than assuming a capable LLM is automatically a capable tutor; in May 2026 it described iterative evaluation work yielding a six-percentage-point improvement in one tutoring outcome. ([Khan Academy Blog][15])

This matters because **LLM ≠ pedagogy**.

There is also evidence that even strong models still struggle to predict good tutor strategy and student outcomes in tutoring dialogues. ([ACL Anthology][16])

Therefore:

```text
BAD
AI decides what to teach
AI decides whether learner understands
AI decides what is true
AI decides next step
```

versus:

```text
GOOD

Pāṭala graph → what is true/evidenced
Learner model → current state
Pedagogical policy → allowed next moves
LLM → language + questioning + explanation
```

Again: **LLM should be the renderer, not the system.**

---

# The architecture I would build

```text
                    PĀṬALA SCHOLARLY GRAPH
                              │
       ┌──────────────────────┼───────────────────────┐
       │                      │                       │
       ▼                      ▼                       ▼
  concepts/terms         arguments/cruxes        source evidence
       │                      │                       │
       └──────────────────────┼───────────────────────┘
                              ↓
                   EDUCATIONAL COMPILER
                              │
             ┌────────────────┼────────────────┐
             ▼                ▼                ▼
       KnowledgePacket    Interactions    Assessments
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                         LEARNER MODEL
                    knowledge + reasoning skills
                              │
                              ▼
                    PEDAGOGICAL POLICY
                  "what should happen next?"
                              │
           ┌──────────────────┼───────────────────┐
           ▼                  ▼                   ▼
      INTERACTIVE          AI TUTOR           REVIEW
       PROBLEM            dialogue          spaced retrieval
           │                  │                   │
           └──────────────────┼───────────────────┘
                              ↓
                       LEARNER EVENTS
                              ↓
                         update model
```

---

# I would reuse this tech stack

### OATutor

Steal/reuse:

* skill ↔ problem mappings;
* BKT learner state;
* adaptive activity selection;
* hints;
* A/B experimentation;
* learning-event logging. ([GitHub][7])

### FSRS or equivalent scheduler

For memory review.

We don't need to invent spaced repetition.

### Inspect / Pāṭala Benchmark

Interestingly, the education system should have evaluation exactly like the scholarship machine.

Test:

```text
Does lesson improve:
immediate understanding?
24h retention?
7d retention?
far transfer?
source discrimination?
argument reconstruction?
```

**Never optimize only engagement.**

### Pāṭala graph

Own.

### LLM

Replaceable tutor/rendering component.

---

# One crucial thing Brilliant understands: learning content needs obsessive hand-design

This is where AI enthusiasm can kill us.

Brilliant describes its lessons as heavily designed around interaction, visual intuition and carefully chosen problems; its content has been built over years, while AI tutoring is layered into that curriculum rather than replacing it. ([Brilliant][1])

Likewise, recent research into automatically generating interactive lessons finds LLMs can help, but task-decomposed generation plus human evaluation still reveals weaknesses such as generic feedback and unclear instructional segments. ([arXiv][17])

So **do not autogenerate 10,000 lessons**.

That would repeat exactly the Pāṭala anti-theatre lesson.

Do:

```text
20 GOLD LEARNING EXPERIENCES
```

Measure them.

Then build compiler machinery from what those golds force.

Exact same doctrine as Argument IR:

> **Gold forces ontology.**

---

# I'd create an Education Gold set

This might actually be important.

For every canonical lesson:

```text
LEARN-GOLD-001
Question:
What makes recognition possible?

Learning objectives:
- distinguish memory from recognition
- identify continuity issue
- reconstruct Utpaladeva's move

Prerequisites:
- cognition
- memory
- numerical identity

Misconceptions:
- recognition = simple remembering
- author/opponent attribution collapse

Interactions:
1 pretest
2 manipulate argument
3 source challenge
4 rival position
5 crux challenge

Transfer:
new unseen passage

Evidence:
links to Pāṭala objects

Review:
scholar
pedagogy reviewer

Metrics:
immediate
24h
7d
transfer
```

Then the educational compiler is evaluated against those.

This becomes another serious Pāṭala research contribution.

---

# And I wouldn't structure the public app primarily as courses

I'd give people **journeys** and **questions**.

Home:

> What do you want to understand?

```text
CONSCIOUSNESS
What does it mean to say consciousness is fundamental?

SELF
Does anything persist through time?

PERCEPTION
Are we seeing the world as it is?

MANTRA
What does a mantra actually do?

LIBERATION
What is recognition supposed to change?

TANTRA
What even is Tantra?

DEBATES
Can momentary consciousness explain memory?
```

Click one.

Five-minute interactive.

Then:

```text
Continue deeper →
```

You progressively enter the tradition.

This is much more compelling to a general audience than:

> Course 1: Introduction to Kashmir Śaivism

---

# Then courses emerge automatically above it

Eventually:

```text
Journey: Recognition
12 packets

Journey: Abhinavagupta
28 packets

Journey: Buddhist–Śaiva Debate
37 packets

Journey: Krama
19 packets

Journey: History of Tantra
45 packets

Course: Pratyabhijñā
= selected ordered traversal across packets
```

So:

> **Packets are canonical. Courses are playlists.**

Very important architectural distinction.

Same as:

> scholarly objects canonical; essays projections.

---

# I think there are actually three educational modes

## 1. DISCOVER

Brilliant-like.

Interactive, beautiful, curiosity-led.

Target: general users.

```text
5–15 minutes
one striking question
one insight
minimal prerequisites
```

## 2. LEARN

Mastery/adaptive.

Knowledge graph + retrieval practice + progression.

Target: serious learner.

```text
learner state
prerequisite graph
practice
spaced review
mastery
```

## 3. STUDY

Primary-source environment.

Target: advanced users/student scholars.

```text
Sanskrit
translation
commentary
argument
scholarship
source exercises
```

Same graph.

Different depth.

---

# And this gives us the cleanest version of progressive epistemic zoom

Imagine every explanation contains:

**Go deeper ↓**

Level 0:

> Consciousness knows itself.

Level 1:

> Abhinavagupta argues that awareness must involve both manifestation and reflexive self-apprehension.

Level 2:

```text
prakāśa
+
vimarśa
```

Level 3:

argument map.

Level 4:

rival interpretation.

Level 5:

scholarly citations.

Level 6:

translation.

Level 7:

Sanskrit.

Level 8:

witness / philological apparatus.

That is not something I found another education product doing end-to-end.

That is **extremely Pāṭala**.

---

# The biggest insight from this search

I previously framed Pāṭala Education as:

> educational projection of the graph.

After looking at the field, I'd strengthen it:

> **Pāṭala Education should be an intelligent tutoring system over an epistemic graph, where the learner learns by manipulating the same propositions, evidence, interpretations and dependencies scholars use to represent the tradition.**

That's considerably more ambitious.

And importantly, technically plausible.

The components mostly exist:

```text
interaction design       ← Brilliant inspiration
learner modeling         ← OATutor / BKT / KT
spaced practice          ← mature research/tools
AI dialogue              ← Khanmigo / Socratic tutors
KG retrieval             ← existing KG-RAG research
concept maps             ← existing education research
argument feedback        ← computational argumentation
domain graph             ← PĀṬALA
epistemic provenance     ← PĀṬALA
dependency simulation    ← PĀṬALA
primary source zoom      ← PĀṬALA
```

So once again, **we should not build 80% of the generic education engine.**

Build the weird 20% nobody else has:

> **interactive epistemic objects + source descent + argument simulation + scholarly uncertainty + correction propagation.**

That is the education moat.

[1]: https://brilliant.org/about/?utm_source=chatgpt.com "About | Brilliant"
[2]: https://pubmed.ncbi.nlm.nih.gov/31465546/?utm_source=chatgpt.com "Element interactivity as a factor influencing the effectiveness of worked example-problem solving and problem solving-worked example sequences - PubMed"
[3]: https://pubmed.ncbi.nlm.nih.gov/28273528/?utm_source=chatgpt.com "The effectiveness of concept mapping on development of critical thinking in nursing education: A systematic review and meta-analysis - PubMed"
[4]: https://pubmed.ncbi.nlm.nih.gov/35664173/?utm_source=chatgpt.com "Exploring the Effects of Argument Map-Supported Online Group Debate Activities on College Students' Critical Thinking - PubMed"
[5]: https://arxiv.org/abs/2307.15341?utm_source=chatgpt.com "Teach Me How to Improve My Argumentation Skills: A Survey on Feedback in Argumentation"
[6]: https://arxiv.org/abs/2201.06953?utm_source=chatgpt.com "Knowledge Tracing: A Survey"
[7]: https://github.com/CAHLR/OATutor?utm_source=chatgpt.com "GitHub - CAHLR/OATutor: Open Source Intelligent Tutoring System w/ BKT (ReactJS and Firebase) · GitHub"
[8]: https://github.com/zijinz456/OpenTutor?utm_source=chatgpt.com "GitHub - zijinz456/OpenTutor: The first block-based adaptive learning workspace that runs locally. Upload any material → get AI-generated notes, quizzes, flashcards, and an adaptive tutor. Open source, self-hosted, 10+ LLM providers. · GitHub"
[9]: https://arxiv.org/abs/2311.17696?utm_source=chatgpt.com "How to Build an Adaptive AI Tutor for Any Course Using Knowledge Graph-Enhanced Retrieval-Augmented Generation (KG-RAG)"
[10]: https://github.com/098765d/AI_Tutor?utm_source=chatgpt.com "GitHub - 098765d/AI_Tutor: AI-Tutor: LLM and RAG-Enhanced AI Tutoring for Various Courses · GitHub"
[11]: https://arxiv.org/abs/2508.11892?utm_source=chatgpt.com "RPKT: Learning What You Don't -- Know Recursive Prerequisite Knowledge Tracing in Conversational AI Tutors for Personalized Learning"
[12]: https://arxiv.org/abs/2412.09248?utm_source=chatgpt.com "A Systematic Review of Knowledge Tracing and Large Language Models in Education: Opportunities, Issues, and Future Research"
[13]: https://pmc.ncbi.nlm.nih.gov/articles/PMC3983480/?utm_source=chatgpt.com "Retrieval practice enhances new learning: the forward effect of testing - PMC"
[14]: https://arxiv.org/abs/2512.03501?utm_source=chatgpt.com "SocraticAI: Transforming LLMs into Guided CS Tutors Through Scaffolded Interaction"
[15]: https://blog.khanacademy.org/how-khan-academy-is-building-a-better-ai-tutor-our-most-recent-learnings/?utm_source=chatgpt.com "How Khan Academy Is Building a Better AI Tutor: Our Most Recent Learnings  - Khan Academy Blog"
[16]: https://aclanthology.org/2025.bea-1.55/?utm_source=chatgpt.com "Exploring LLMs for Predicting Tutor Strategy and Student Outcomes in Dialogues - ACL Anthology"
[17]: https://arxiv.org/abs/2506.17356?utm_source=chatgpt.com "Automatic Large Language Models Creation of Interactive Learning Lessons"
