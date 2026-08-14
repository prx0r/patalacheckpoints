Yes. After looking across the formal adaptive-learning literature and current open-source systems, I think there is a **much sharper architecture than GeometricEngine**.

GeometricEngine had the correct intuition:

> state → intervention → outcome → update

But that problem has several mature research traditions already. Pāṭala should compose them rather than inventing its own monolithic “learning AI.”

The stack I would use is:

```text
                    PĀṬALA TRUTH GRAPH
             concepts / claims / arguments / sources
                           │
                           ▼
                   DOMAIN STRUCTURE
               prerequisites / alternatives
                           │
           ┌───────────────┴────────────────┐
           ▼                                ▼
    LEARNER STATE                       USER MEMORY
 what do they know?              what has happened over time?
           │                                │
           └───────────────┬────────────────┘
                           ▼
                    POLICY ENGINE
              what should happen next?
                           │
                           ▼
             lesson / question / video /
             argument / source / discussion
                           │
                           ▼
                   OBSERVED OUTCOME
                           │
                           ▼
                  LEARNING UPDATE
```

And there are existing technologies for almost every box.

## 1. Knowledge Space Theory is probably the formal foundation we're missing

This was the biggest find.

**Knowledge Space Theory / Learning Spaces** formalizes a domain not merely as a prerequisite DAG, but as the set of feasible **knowledge states** a learner can occupy. It underlies ALEKS and introduces the idea of the learner's **outer fringe**: things they are currently ready to learn next. ([Springer Nature Link][1])

Suppose Pāṭala has:

```text
A = recognition
B = prakāśa
C = vimarśa
D = svātantrya
E = contraction
```

Instead of merely saying:

```text
A → B → C → D → E
```

we represent valid knowledge states:

```text
{}
{A}
{A,B}
{A,B,C}
{A,B,D}
{A,B,C,D}
...
```

Given:

```text
user knowledge = {A,B}
```

the system computes:

```text
INNER FRINGE:
things worth reviewing

OUTER FRINGE:
things they can meaningfully learn next
```

This gives us a principled distinction between:

**what is interesting**

and

**what this person is ready for**.

ALEKS has used this sort of state-space approach at large scale; the formal literature specifically treats personalized progression as movement through enormous spaces of feasible knowledge states rather than a single fixed sequence. ([Springer Nature Link][2])

### For Pāṭala

I would distinguish:

```text
LOGICAL GRAPH
what propositions depend upon what

SCHOLARLY GRAPH
what interpretations/evidence support what

PEDAGOGICAL GRAPH
what understanding tends to require what

KNOWLEDGE SPACE
which combinations of understanding are coherent learner states
```

That is considerably sharper than GeometricEngine's free-form `student_state` strings.

---

# 2. Bayesian Knowledge Tracing should probably be our v1 learner model

Do **not** begin by training a huge neural model.

Bayesian Knowledge Tracing already gives us the basic hidden-state model:

```text
P(user understands concept)
```

updated after evidence.

The open-source `pyBKT` implementation is mature and explicitly models cognitive mastery from sequences of learner interactions. ([GitHub][3])

For each Pāṭala concept:

```text
vimarśa mastery = .42
recognition mastery = .91
svātantrya mastery = .56
```

After an assessment:

```text
P(vimarśa) .42 → .67
```

After later failure:

```text
.67 → .54
```

Much better than:

```text
completed = true
```

And it's interpretable.

### Importantly

Mastery probability shouldn't only come from MCQs.

Pāṭala has much richer observations:

```text
answered MCQ
completed argument
identified invalid inference
asked follow-up
corrected misconception
explained concept
transferred concept to novel example
selected textual evidence
```

Those can become observation types with different diagnostic strengths.

---

# 3. Then benchmark BKT against modern Knowledge Tracing

Once usage grows, use **pyKT** rather than arbitrarily choosing a fashionable model.

pyKT is a maintained research toolkit that benchmarks a broad family including DKT, DKVMN, SAKT, AKT, GKT, DTransformer, uncertainty-aware KT and others. ([GitHub][4])

That's ideal because Pāṭala can eventually run:

```text
BKT
vs
AKT
vs
GKT
vs
DTransformer
vs
our model
```

against our own longitudinal dataset.

We don't need to speculate which wins.

Measure it.

---

# 4. Graph Knowledge Tracing is particularly relevant to us

Normal KT often treats skills too independently.

But Pāṭala already owns a concept graph.

Graph-based Knowledge Tracing was designed specifically to model how mastery of related knowledge components interacts rather than treating each component as isolated. ([GitHub][5])

More recent **GRKT** explicitly argues that learner knowledge should evolve through graph-structured relations between concepts and models retrieval, strengthening, learning and forgetting over that graph. ([arXiv][6])

That's almost made for Pāṭala.

Example:

```text
User correctly understands:

prakāśa
   │
   └─ influences probability of understanding →
                                      vimarśa
```

An observation about `vimarśa` can therefore update neighboring concepts somewhat rather than only one scalar.

---

# 5. PSI-KT may be even closer to the thing we actually want

One paper I'd put near the top of our reading list is **PSI-KT**.

It explicitly tries to jointly model:

* learner progress;
* learner-specific traits;
* prerequisite structure;
* learning dynamics;

while remaining interpretable and scalable. ([arXiv][7])

That matters because our prerequisite graph isn't completely known in advance.

We have:

```text
authored prerequisite edge
```

but user data might discover:

```text
learned prerequisite edge
```

PSI-KT is much closer conceptually to:

> **infer both the learner and parts of the map they're learning on.**

That's precisely the long-term Pāṭala feedback loop.

---

# 6. Cognitive Diagnosis is another important layer

Knowledge tracing asks:

> How is mastery changing through time?

**Cognitive Diagnosis** asks:

> What combination of latent competencies explains this learner's responses?

The open-source **InsCD** toolkit combines classical psychometric approaches such as IRT with modern graph-based cognitive-diagnosis models. ([GitHub][8])

This could be very useful for Pāṭala because our “skills” aren't merely topics.

Example:

User keeps failing several completely different questions.

Underlying diagnosis may be:

```text
not:
"doesn't understand Abhinavagupta"

but:

difficulty with
  ├─ scope
  ├─ necessary vs sufficient
  ├─ reflexivity
  └─ identity through time
```

Then their profile becomes multidimensional:

```text
CONCEPTUAL
recognition          .83
vimarśa              .61

REASONING
scope                .47
counterexample       .80
modal reasoning      .55

PHILOLOGICAL
term consistency     .34

COMPARATIVE
position alignment   .71
```

That's hugely useful.

A recent cognitive-diagnosis direction goes even further and models not only which concepts are mastered but whether the learner understands **relations between concepts**. ([arXiv][9])

That's basically:

> Do you know A and B?

versus:

> Do you understand **why A relates to B?**

For philosophy, the second one matters much more.

---

# 7. Contextual bandits are the sharper version of GeometricEngine's policy weights

GeometricEngine currently does roughly:

```text
state S
→ intervention X worked previously
→ increase W[S,X]
```

That's crude reinforcement learning.

A contextual bandit formalizes:

```text
context = learner state

actions =
  lesson A
  lesson B
  argument exercise
  video
  analogy
  primary source

reward =
  observed learning gain
```

Then choose the action predicted to work best while still sometimes exploring alternatives.

A real educational deployment using contextual bandits on learner trajectories reported improved completion/engagement relative to its comparison approaches. ([arXiv][10])

A 2026 paper applies **contextual Thompson sampling** specifically to selecting exercises according to estimated learner skill gain. ([arXiv][11])

That is what I'd use instead of GeometricEngine's handmade additive weights.

### Pāṭala version

```text
CONTEXT

mastery:
  vimarśa=.42
  prakāśa=.83

confusion:
  vimarśa=attention

interest:
  consciousness=.91

previous intervention:
  prose explainer failed

AVAILABLE ACTIONS

A argument diagram
B Buddhist contrast
C primary passage
D analogy
E 3-minute video

POLICY:
choose B
```

Observe learning outcome.

Update.

That's a proper adaptive system.

---

# 8. We should NOT jump immediately to full RL

This matters.

Contextual bandits are good when we're mainly choosing the **next action**.

Full reinforcement learning becomes appropriate when:

```text
action now
       ↓
changes state
       ↓
affects what becomes learnable
       ↓
changes long-term outcome
```

Education obviously has this property.

But RL has severe delayed-credit and reward-design problems.

A 2025 Socratic tutoring paper formalizes adaptive tutoring as a **POMDP**, because the learner's true cognitive state is latent and only indirectly observed through responses. ([arXiv][12])

That's mathematically the eventual shape:

```text
hidden state:
true understanding

observations:
questions / answers / behavior

actions:
teaching interventions

transition:
learning / forgetting

reward:
long-term comprehension
```

But I'd make this **Pāṭala v4**, not v1.

---

# 9. So GeometricEngine should evolve like this

```text
CURRENT GEOMETRICENGINE

heuristic state
      ↓
counted weights
      ↓
intervention
      ↓
score
```

Replace with:

```text
PĀṬALA

Knowledge Space
      ↓
Bayesian / graph learner state
      ↓
Contextual Bandit
      ↓
Intervention
      ↓
Rich Outcome Measurement
      ↓
updated learner model
```

Eventually:

```text
POMDP / RL
```

That is the formalized version.

---

# 10. Add forgetting explicitly

A user understood something in January.

That does not mean they understand it in August.

Modern tutor research increasingly models temporal forgetting alongside mastery; recent personalized LLM-tutoring work explicitly combines learner memory, proficiency and forgetting rather than treating historical mastery as static. ([arXiv][13])

So:

```text
P(mastery | time)
```

should decay.

Then:

```text
vimarśa=.81

90 days no exposure

predicted retention=.58
```

Pāṭala surfaces:

> Quick refresh?

This is where FSRS-style scheduling can help for recall, but philosophical understanding needs more than flashcard scheduling.

---

# 11. Graphiti is directly useful for the **personal history graph**

This was another strong discovery.

Graphiti is an open-source temporal knowledge-graph system built specifically for continuously ingesting user interactions while keeping:

* entities;
* relationships;
* provenance;
* validity intervals;
* historical states;
* hybrid graph/semantic/keyword retrieval. ([GitHub][14])

It even uses **episodes** as the raw provenance objects from which derived graph facts are produced. ([GitHub][14])

This maps remarkably well to our conversation.

User says in January:

> I'm mostly interested in meditation.

April:

> I'm becoming much more interested in philosophical arguments.

August:

> I'm studying Buddhist epistemology.

Don't overwrite:

```text
interest=...
```

Store:

```text
INTEREST(user, meditation)
valid: Jan–Apr

INTEREST(user, arguments)
valid: Apr–

INTEREST(user, Buddhist epistemology)
valid: Aug–
```

Now you can query:

> How has this person's intellectual trajectory changed?

Graphiti is much closer to what we need for **user memory** than making our own temporal graph layer.

But I would **not** let it determine mastery.

Use:

```text
Graphiti:
biographical/interaction memory

KT system:
epistemic mastery
```

Different jobs.

---

# 12. Temporal data becomes crucial

Our learner shouldn't be one vector.

It should be:

```text
UserState(t)
```

Then:

```text
Jan
recognition=.20

Feb
recognition=.56

Mar
recognition=.81

May
recognition=.66    ← forgetting

Jun
recognition=.89    ← revisited through Buddhist objection
```

Now the model learns **learning curves**, not profiles.

---

# 13. Causal inference becomes important once we have a lot of data

This is a subtle but critical upgrade.

Suppose users who attend retreats later score higher on learning assessments.

You cannot conclude:

> retreats caused better learning.

Maybe highly motivated users attend retreats.

Similarly:

> people who watch primary-source videos improve more.

Maybe advanced learners self-select into them.

A 2026 study on tutoring interventions explicitly combines deep knowledge tracing with doubly robust causal estimation because tutoring usage is strongly self-selected and learner state changes over time. ([arXiv][15])

This should eventually become part of Pāṭala's research methodology.

So distinguish:

```text
CORRELATIONAL SIGNAL
people who did X tended to improve

from

CAUSAL ESTIMATE
X likely produced improvement
```

Very on-brand for Pāṭala.

---

# 14. Off-policy evaluation is also important

Once the recommender runs, you'll accumulate historical decisions:

```text
state S
→ system chose video A
→ outcome Y
```

Later you invent a better policy.

You don't necessarily want to expose everyone experimentally just to see whether it works.

**Off-policy evaluation** estimates how a new policy might have performed using logged decisions from an old one, although the reliability depends heavily on coverage and assumptions. ([arXiv][16])

This becomes:

> Before deploying curriculum algorithm v17, replay it against historical trajectories.

That's proper ML-engine infrastructure.

---

# 15. The LLM should NOT be the learner model

This is an important finding.

A recent comparison found conventional deep knowledge tracing substantially more temporally coherent for learner-state estimation than using an LLM directly for that task, arguing for hybrid tutor architectures rather than “LLM remembers everything.” ([arXiv][17])

I agree strongly for Pāṭala.

Do this:

```text
structured learner model
        ↓
policy decides educational goal
        ↓
graph provides evidence/content
        ↓
LLM renders interaction
```

Not:

```text
dump chat history into LLM
→ "figure out what this person knows"
```

That would sacrifice the entire advantage of Pāṭala.

---

# 16. Karpathy's Eureka vision gets one thing exactly right

Eureka Labs' public vision is:

> domain expert designs high-quality course material; AI Teaching Assistant scales guidance through it. ([Eureka Labs][18])

That is already extremely close to Pāṭala's:

```text
SCHOLAR CREATES TRUTH

AI PERSONALIZES DELIVERY
```

But I think Pāṭala can eventually go **one level beyond the publicly described Eureka model**.

Eureka:

```text
expert curriculum
       ↓
AI tutor
       ↓
students
```

Pāṭala:

```text
expert graph
      ↓
AI tutor
      ↓
students
      ↓
learning trajectories
      ↓
empirical pedagogy graph
      ↓
curriculum improves
      ↓
questions reveal research gaps
      ↓
scholar graph improves
```

That's our distinctive loop.

The **truth graph** remains human-reviewed.

The **teaching graph** learns.

That separation is essential.

---

# 17. Existing product worth studying: OATutor

OATutor is open-source and already combines adaptive tutoring with Bayesian Knowledge Tracing. ([GitHub][19])

I wouldn't reuse its visual/product identity.

But inspect it for:

* skill-state handling;
* hint scaffolding;
* mastery transitions;
* event logging;
* content authoring;
* adaptive problem presentation.

This is mature intelligent-tutoring plumbing we shouldn't rediscover.

---

# 18. OpenTutor is worth stealing UI/product ideas from

OpenTutor is newer and interesting because it combines:

* adaptive tutoring;
* knowledge graph;
* concept mastery;
* quizzes;
* FSRS;
* adaptive depth;
* Socratic mode;
* planner;
* source-grounded tutor. ([GitHub][20])

Its graph/learner components are explicitly marked experimental, so I would not treat its learning algorithms as validated science. ([GitHub][20])

But as a **consumer product reference**, it's highly relevant.

Particularly:

```text
one adaptive workspace
rather than
course → quiz → chat as disconnected products
```

---

# 19. TutorLLM validates the hybrid pattern

TutorLLM explicitly combines:

```text
Knowledge Tracing
+
RAG
+
LLM
```

so the LLM receives both domain material and a predicted learner state rather than operating generically. ([arXiv][21])

That is approximately the architecture we want, except Pāṭala's RAG substrate is much richer:

```text
Source
Claim
Argument
Interpretation
Review
```

rather than generic scraped educational content.

---

# 20. The really interesting AI-training implication

Eventually **Pāṭala itself generates a unique training corpus for pedagogical AI**.

Every interaction can become:

```text
STATE S

QUESTION Q

AVAILABLE INTERVENTIONS
A B C D

SELECTED
B

TEACHING RESPONSE
R

PREDICTED EFFECT
E

ACTUAL OUTCOME
S'

DELAYED OUTCOME
S''

REWARD
learning gain
```

Now imagine tens of millions of these.

That's training data for a model whose job isn't:

> generate good prose.

It's:

> **select the pedagogical intervention that changes understanding from S to desirable S′.**

That's a much more interesting model.

---

# 21. This produces three potential models

### Model A — Knowledge Model

```text
input:
learner history

output:
P(mastery over graph)
```

Train from assessment/interaction traces.

### Model B — Pedagogical Policy

```text
input:
learner state + graph context

output:
next intervention
```

Train from transitions/outcomes.

### Model C — Renderer

```text
input:
intervention + evidence + learner context

output:
actual conversational teaching
```

Train/preferences optimize clarity.

These should be independent.

That means if a better LLM arrives, swap Model C.

Your actual moat remains A + B + data.

---

# 22. Eventually a fourth model appears: the curriculum model

Given millions of trajectories:

```text
starting state
desired state
```

predict:

```text
best path
```

Almost:

```text
PATH(
    learner,
    current understanding,
    target understanding
)
```

Now Pāṭala can solve:

> I want to understand Abhinavagupta well enough to read the IPVV.

System computes a route.

Another user:

> I just want to understand what nonduality means.

Different route.

Same graph.

---

# 23. And a fifth model: question-value prediction

Because questions feed the autonomous research/media system:

```text
QuestionValue(Q) =
expected learning value
× population demand
× unresolvedness
× graph centrality
× research novelty
```

Then the system learns:

> Which unanswered question should we spend expensive scholar/agent time resolving?

That's effectively **active learning over the knowledge graph**.

The AI isn't only learning from users.

It's choosing **what data it needs next**.

---

# 24. This is where the engine becomes self-improving

The complete loop:

```text
              SCHOLARLY GRAPH
                    │
                    ▼
              learner model
                    │
                    ▼
               policy model
                    │
                    ▼
                teaching
                    │
                    ▼
              user response
                    │
              ┌─────┴─────┐
              ▼           ▼
        update learner   aggregate
            model         demand
                           │
                           ▼
                     missing knowledge
                           │
                           ▼
                       research
                           │
                           ▼
                    scholarly graph
```

Then simultaneously:

```text
interaction outcomes
        ↓
policy training
        ↓
better pedagogy
        ↓
better outcomes
        ↓
better training data
```

That's the compounding AI engine.

---

# My current recommended technical hierarchy

I would **not** build another big custom learner engine yet.

### Build now

**1. Pāṭala graph**

Already our strongest primitive.

**2. Knowledge-space layer**

Explicit prerequisites + feasible learner states + “ready next” fringe.

**3. BKT learner model**

Use an interpretable probabilistic baseline.

**4. LearningEvent / Transition schema**

Take this from GeometricEngine conceptually.

**5. Question clusters**

Every conversation feeds demand + learner state.

**6. Temporal user graph**

Graphiti-like episodes/facts for user history.

### Once meaningful usage exists

**7. pyKT experiments**

Compare learner models.

**8. contextual Thompson sampling**

Choose interventions.

**9. cognitive diagnosis**

Discover latent reasoning weaknesses.

**10. learned prerequisite graph**

Compare human-authored pedagogy against empirically inferred structure.

### Much later

**11. causal intervention estimation**

What actually helps whom?

**12. off-policy evaluation**

Safely evaluate replacement policies.

**13. POMDP/RL**

Optimize long intellectual trajectories.

**14. train Pāṭala pedagogical models**

On proprietary trajectory data.

---

# The conceptual stack is therefore sharper now

I'd define four graphs.

```text
1. TRUTH GRAPH
   what is justified?

2. DOMAIN GRAPH
   what conceptually depends on what?

3. LEARNER GRAPH
   what does this person understand?

4. PEDAGOGY GRAPH
   what tends to move learners between states?
```

Then:

```text
Truth Graph
    │
    ▼
Domain Graph
    │
    ├───────────────┐
    ▼               ▼
Learner Graph → Pedagogy Graph
    ▲               │
    └──── outcome ──┘
```

**GeometricEngine was basically an early hand-built Pedagogy Graph.**

What we've now found is that knowledge-space theory, knowledge tracing, cognitive diagnosis, contextual bandits and causal evaluation give us the formal machinery to make that graph significantly more rigorous.

And this creates what I think is the deepest moat in the entire consumer vision:

> **Pāṭala doesn't just learn what its users like. It learns what they know, what they misunderstand, what they are ready to understand next, and which evidence-grounded intervention actually helps people cross that gap.**

Then those same observations recursively determine what Pāṭala teaches, researches, writes and films next.

[1]: https://link.springer.com/book/10.1007/978-3-642-01039-2?utm_source=chatgpt.com "Learning Spaces: Interdisciplinary Applied Mathematics | Springer Nature Link"
[2]: https://link.springer.com/article/10.1186/s40561-016-0038-y?utm_source=chatgpt.com "A possible future for next generation adaptive learning systems | Smart Learning Environments | Springer Nature Link"
[3]: https://github.com/CAHLR/pyBKT?utm_source=chatgpt.com "GitHub - CAHLR/pyBKT: Python implementation of Bayesian Knowledge Tracing and extensions · GitHub"
[4]: https://github.com/pykt-team/pykt-toolkit?utm_source=chatgpt.com "GitHub - pykt-team/pykt-toolkit: pyKT: A Python Library to Benchmark Deep Learning based Knowledge Tracing Models · GitHub"
[5]: https://github.com/jhljx/GKT?utm_source=chatgpt.com "GitHub - jhljx/GKT: Graph-based Knowledge Tracing: Modeling Student Proficiency Using Graph Neural Network · GitHub"
[6]: https://arxiv.org/abs/2406.12896?utm_source=chatgpt.com "Leveraging Pedagogical Theories to Understand Student Learning Process with Graph-based Reasonable Knowledge Tracing"
[7]: https://arxiv.org/abs/2403.13179?utm_source=chatgpt.com "Predictive, scalable and interpretable knowledge tracing on structured domains"
[8]: https://github.com/ECNU-ILOG/InsCD?utm_source=chatgpt.com "GitHub - ECNU-ILOG/InsCD: InsCD: A Modularized, Comprehensive and User-Friendly Toolkit for Machine Learning Empowered Cognitive Diagnosis · GitHub"
[9]: https://arxiv.org/abs/2412.19759?utm_source=chatgpt.com "Enhancing Cognitive Diagnosis by Modeling Learner Cognitive Structure State"
[10]: https://arxiv.org/abs/2207.14003?utm_source=chatgpt.com "Raising Student Completion Rates with Adaptive Curriculum and Contextual Bandits"
[11]: https://arxiv.org/abs/2602.04347?utm_source=chatgpt.com "A Bandit-Based Approach to Educational Recommender Systems: Contextual Thompson Sampling for Learner Skill Gain Optimization"
[12]: https://arxiv.org/abs/2512.11930?utm_source=chatgpt.com "Evolutionary Reinforcement Learning based AI tutor for Socratic Interdisciplinary Instruction"
[13]: https://arxiv.org/abs/2511.15163?utm_source=chatgpt.com "Teaching According to Students' Aptitude: Personalized Mathematics Tutoring via Persona-, Memory-, and Forgetting-Aware LLMs"
[14]: https://github.com/getzep/graphiti?utm_source=chatgpt.com "GitHub - getzep/graphiti: Build Real-Time Knowledge Graphs for AI Agents · GitHub"
[15]: https://arxiv.org/abs/2602.19296?utm_source=chatgpt.com "A Causal Framework for Estimating Heterogeneous Effects of On-Demand Tutoring"
[16]: https://arxiv.org/abs/2311.14110?utm_source=chatgpt.com "When is Off-Policy Evaluation (Reward Modeling) Useful in Contextual Bandits? A Data-Centric Perspective"
[17]: https://arxiv.org/abs/2512.23036?utm_source=chatgpt.com "Problems With Large Language Models for Learner Modelling: Why LLMs Alone Fall Short for Responsible Tutoring in K--12 Education"
[18]: https://eurekalabs.ai/?utm_source=chatgpt.com "Eureka Labs"
[19]: https://github.com/CAHLR/OATutor?utm_source=chatgpt.com "GitHub - CAHLR/OATutor: Open Source Intelligent Tutoring System w/ BKT (ReactJS and Firebase) · GitHub"
[20]: https://github.com/zijinz456/OpenTutor?utm_source=chatgpt.com "GitHub - zijinz456/OpenTutor: The first block-based adaptive learning workspace that runs locally. Upload any material → get AI-generated notes, quizzes, flashcards, and an adaptive tutor. Open source, self-hosted, 10+ LLM providers. · GitHub"
[21]: https://arxiv.org/abs/2502.15709?utm_source=chatgpt.com "TutorLLM: Customizing Learning Recommendations with Knowledge Tracing and Retrieval-Augmented Generation"
