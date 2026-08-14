# LAYER 09 — ORGANISM (the human understanding graph)

*Part of the `globalglobal.md` spine. The second first-class graph — user questions/confusions/beliefs.*

## 1. What it is
The human-understanding graph: treats user interaction as structured epistemic data (not chat logs).
The consumer app becomes a sensor for what humans fail to understand, care about, confuse, contest, and
want next.

## 2. Purpose
Add the **Q variable to the moat**: `M = D×P×V×N×A×Q`. Competitors can scrape the corpus and clone the
UI, but cannot reproduce years of "what people ask, where they misunderstand, which explanations work."

## 3. External tools used (planned)
**Graphiti** (temporal user graph — episodes as provenance, validity periods, MCP) · **pyBKT** (learner
state model) · **pyKT** (modern KT benchmarks) · Knowledge Space Theory / ALEKS (prerequisite + outer
fringe) · OATutor/OpenTutor (adaptive tutoring). See `external-tools.md`.

## 4. Data
- `UserKnowledgeState` — interests, concept mastery, arguments understood, known confusions, questions.
- Question clusters — canonical Question with frequency/followup/resolution rate.
- The second graph: user · question · confusion · belief · misconception · learning state · follow-up.
- Magic edges: Question──about──>Concept · Confusion──misreads──>Claim · Objection──attacks──>Premise.

## 5. Processes
```
100k interactions → question graph → cluster+rank → gaps → research agent → evidence graph →
argument reconstruction → verification → canonical answer → lesson/essay/video → telemetry → iterate
```
Explanation gaps (31% ask the same follow-up) → auto-open improvement task. Unanswered question → OPEN
QUESTION → scholar bounty → adjudication → "a new review changed the answer to your 6-month-old question."

## 6. Implementations
**STATUS: design only — not yet built.** Raw research: `docs/vision/organism/` (5 docs). The temporal
graph + learner model will be built here. See `docs/process/09-organism.md`.

**Substrate now identified (from the `patalagithubs` ecosystem review — `docs/process/githubclones.md` §J):**
- **Learner-state / education runtime** → **Engram** (`nagisanzenin/engram`) — knowledge-dependency graph,
  predict→act→explain, blind grading, FSRS, receipts-not-enthusiasm. *"Red-circle this — clone before
  writing more education infra."* Also `ktaletsk/learn-codebase` (Socratic + mastery), `lfnovo/open-cognition`
  (MCP + learning-graph), `SYuan03/Skill-Anything` (the compiler mentality), `studyield/studyield` (teach-back UX),
  `arturseo-geo/llm-knowledge-base` (gap tracker — UNKNOWN as a first-class object).
- **Temporal user graph** → Graphiti · **learner model** → pyBKT/pyKT (from `consumerorganismtech`).
- **Learning scheduler** → FSRS (don't build).

**These make the education half of Layer 09 no longer "no substrate" — it has a concrete reuse-first build path.**
## 7. Docs
- `docs/process/09-organism.md` — the detailed layer guide.
- `docs/vision/organism/` — the 5 raw organism vision docs.
- `docs/vision/education/PATALA-EDUCATION-SYNTHESIS.md` — the learner objects (MasteryEvidence).
- `docs/vision/vision-09-media-and-cross-tradition.md` — the media layer.
