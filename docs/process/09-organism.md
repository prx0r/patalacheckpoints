# PĀṬALA AS ORGANISM — the Human Understanding Graph + consumer-as-probe

*2026-08-14. The organism vision: Pāṭala as a living system that not only represents what the texts
say (epistemic graph) but continuously observes what humans struggle to understand (human understanding
graph), and uses that gap to decide what scholarship, explanation, education and media happen next.
Raw research: `docs/vision/organism/` (consumerorganism, consumerorganismtech, organism_meh,
patalaorganism, patalaorganismvisions). This is the **Q variable in the moat**: the question/understanding
graph competitors cannot reproduce.*

---

## 1. The core idea: two first-class graphs, not one

```text
EPISTEMIC GRAPH            HUMAN UNDERSTANDING GRAPH
source · translation       user · question · confusion · belief
claim · argument           misconception · learning state
evidence · concept         follow-up · resolution · interest
scholar · review
        │                        │
        └───────── MAGIC EDGES ──┘
   Question ──about──> Concept
   Confusion ──misreads──> Claim
   Objection ──attacks──> Premise
   Lesson ──resolves──> Confusion
   ScholarDecision ──changes──> Answer
   Answer ──generates──> Followup
```

**The second graph may be as important as the Sanskrit graph itself.** Pāṭala becomes:
```
What do the texts say? → What arguments do they make? → What do humans struggle to understand? →
What is the best evidence-grounded route for THIS human? → observe the knowledge gap → decide what's next.
```

## 2. The engineering architecture (consumerorganismtech)

**Don't have one giant AI graph.** Use an **immutable interaction/event stream** feeding several graph/
model projections, each optimized for a different question.

```text
RAW EVENTS (immutable + consent-scoped)
   ↓
temporal user graph (Graphiti — episodes as provenance, validity periods, MCP-ready)
   ↓
learner state model (pyBKT v1 — Knowledge-Space Theory / outer fringe)
   ↓
truth graph (Pāṭala's own epistemic graph — never let projections decide truth)
```

- **Graphiti** (`getzep/graphiti`): incremental temporal graph, preserves episodes as provenance,
  validity periods (not overwrites), semantic+keyword+graph retrieval, MCP tooling.
- **pyBKT**: first formal learner-state model (Bayesian Knowledge Tracing). **pyKT**: benchmark modern
  KT models later. **Knowledge Space Theory**: feasible knowledge states + the learner's outer fringe
  (the things they're ready to learn next).

## 3. Every user has a knowledge state, not a profile

```text
UserKnowledgeState: interests, concept mastery, arguments understood, known confusions,
questions asked, positions explored, primary texts encountered, preferred depth, open learning cruxes
```
→ the AI teacher knows *"Tom understands prakāśa but not yet why vimarśa is required"* and routes
through the graph accordingly. **Personalization changes the path, not the truth.**

## 4. Consumers are probes into the graph

- **Question clusters** — "If consciousness is Śiva, why recognize?" clusters under a canonical
  Question with frequency/followup/resolution rate → a map of unresolved human understanding.
- **Explanation gaps** — if 31% of readers ask the same follow-up, the explanation isn't working →
  auto-open an improvement task → better explainer.
- **Missing graph parts** — an unanswered question becomes an OPEN QUESTION → research agent searches →
  new relations/arguments → consumers become discovery probes for scholarship.
- **Scholar bounties** — a frequent, important, unresolved question enters the scholar review queue;
  when adjudicated, *"a new scholarly review changed Pāṭala's answer to a question you asked 6 months
  ago"* → incredible retention.
- **Epistemic friction map** — high user-misunderstanding + high scholarly-disagreement + weak evidence
  = priority research zones.

## 5. The demand-driven autonomous chain

```text
100k interactions → question graph → cluster+rank → gaps → research agent →
source/evidence graph → argument reconstruction → verification → canonical answer →
lesson/essay/video → understanding telemetry → next iteration
```
Multi-objective (NOT clicks): `demand × epistemic importance × unresolvedness × source support ×
learning value × media potential` — resistant to clickbait collapse.

## 6. The moat update

```
M = D × P × V × N × A × Q        (Q = question/understanding graph)
```
Competitors can scrape the corpus, clone the UI, use the same models — they cannot reproduce years of
"what people ask, where they misunderstand, which explanations work, which interventions changed
understanding."

## 7. Privacy

Structured extraction from raw chat (Question/Confusion/Objection/ConceptMention/...); personal history
separate from aggregate/anonymized learning signals; explicit opt-in; delete/export; never silently
treat private chats as research material.

---

## 8. How it links to the rest of Pāṭala

```
EPISTEMIC CORE (07) + COMMENTARIAL GRAPH (06)   → the truth graph
VERIFICATION PLANE (08)                          → tests the truth graph
EDUCATION VISION (LearningClaim/Skill/Interaction/MasteryEvidence) → the learner objects
ORGANISM (this)                                  → the user side: questions/confusions feed back
   → demand graph → content market → scholar bounties → the compounding consumer loop
```
The education vision's `MasteryEvidence` + the organism's `UserKnowledgeState` are the two halves of the
same adaptive-learning story. Repos to raid: **Graphiti** (temporal user graph), **pyBKT/pyKT**
(learner models), **Knowledge Space Theory / ALEKS** (prerequisite/fringe), **OATutor/OpenTutor**
(adaptive tutoring).
