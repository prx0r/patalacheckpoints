# SYSTEM GROWTH + THE HERMES INFRA DECISION (synthesis)

*2026-08-12. Two things: (A) how the geometricengine's learning loop shows Pāṭala growing over time,
and (B) whether Hermes should be Pāṭala's infra. Both grounded in the actual code.*

---

## A. THE GEOMETRICENGINE LEARNING LOOP (what Pāṭala should copy)

The engine's real mechanism (from `train.py`, `graph.py`, `pathway.py`):

```
UNO episodes (annotated pedagogy)
  → parse each turn into a full record (state, function, mechanism, register, my_thoughts)
  → build transitions (from_state → move → predicted_impact → next_state)
  → TRAIN: for each from_state, increment W[state][move] and W[move][next_state]
  → store in policy_weights
Inference:
  user_text → retrieve similar hyperedges → infer state
  → query trained W[state] for the top move
  → graph composes the response (no LLM in the decision path)
  → user rates it → feedback updates W
```

**The growth loop (the gamechanger):** the system gets *better* because every real interaction
updates the transition weights. It's not "AI + a database"; it's a **weighted pedagogical graph that
learns from its own use**.

### How Pāṭala grows over time (the adaptation)

Pāṭala already has the *structure* (passages + C1 + themes + hub + journey + recommend + analyst).
The geometric lesson is the **feedback-weighted growth**:

```
A NEW TEXT is added
  → PUSHING enquiry (discovery)         → grows the passages + penetrations
  → argument truth-packets (formal)      → the logical-arguments gold
  → comparative matrix (across texts)    → the cross-text data
  → lessons/journeys (the graph selects) → the education layer
  → learners/readers interact            → feedback updates the edge weights
  → the journey/recommend/analyst get BETTER (the weights learn)
  → new essays/lessons derived from the improved graph
```

So the compounding isn't just "more content" — it's that **each layer feeds the next, and real use
improves the selection weights**, exactly like the geometricengine but over scholarly evidence
instead of therapy.

The three Pāṭala-specific growth engines (already built or spec'd):
1. **PUSHING → argument → essay** (`SPEC_LOGICAL_ARGUMENTS_GOLD`): discovery compounds into formal
   arguments.
2. **Comparative matrix** (`SPEC_COMPARATIVE_PUSHING`): every text fills a column; the matrix grows
   without re-asking.
3. **The education graph** (journey + recommend + analyst): real reader interaction learns which
   paths work — the geometric feedback loop.

---

## B. THE HERMES INFRA DECISION

### Current state (verified)

- **Pāṭala already uses Hermes** as its model client: `pipeline/model.py` shells out to `hermes -z`
  for every stage. The epistemic logic (schemas, contracts, audit) stays in Pāṭala; only the "call
  the model" step is delegated.
- **There's a rich `.hermes/skills/` library** (~40+ skills: data-science, autonomous-agents,
  factory-pipeline, deep-analysis, etc.) and Pāṭala's own `skills/` (translate-passage,
  write-commentary, use-api, assemble-stack, validate-passage).
- The geometricengine uses a similar pattern (delegates to DeepSeek via `deepseek_client.py`, but
  the graph owns the cognition).

### Recommendation: YES, Hermes is the right infra — but with the geometric boundary

**Use Hermes as the model/infra layer** (it already is, and it's the right call — it isolates the
model calls, gives skills, retries, JSON handling). **BUT apply the geometric principle: Hermes
(LLM) should narrate the graph-selected path; it should NOT decide the scholarly move.** The move
(journey, recommendation, argument verdict) comes from the graph + the deterministic floor.

Concretely, Pāṭala's infra stack:

```
HERMES (the agent/infra layer)
  → model calls, skills, retries, JSON, the narrator
PĀṬALA GRAPH (the scholarly authority)
  → the deterministic floor: resolve, verify, journey, recommend, analyst, themes
  → selects the move; Hermes narrates it with source anchors
```

This is the "no LLM in the cognition path" principle: **the graph owns the scholarship; Hermes owns
the voice.** They never collapse.

### What to adopt from the geometricengine's stack

| Engine tool | Pāṭala equivalent | Verdict |
|---|---|---|
| LangGraph (stateful talk loop) | `pipeline/model.py` + hermes | already have the loop; LangGraph optional later |
| SQLite graph/hypergraph | `data/corpus/` TS modules + the lazy JSON store | TS data is fine; SQLite only if queries get heavy |
| vector retrieval (Qdrant) | the ML agent's benchmark Q2/Q3 | build it (Agent 1's lane) |
| `my_thoughts` metacognitive | `analyst.ts` + `/api/analyst` (built) | done |
| weighted transition graph | journey + recommend + the future edge-weights | build the weights (geometric.md §1.2) |
| feedback → weight update | the ML benchmark + the review loop | the ML agent's Q1 + the human-review gate |

---

## C. WHAT THIS MEANS FOR THE NEXT BUILD

1. **Pāṭala should keep Hermes as its infra** — it's already wired, it's the right isolation, and it
   gives the skills/retries/JSON layer. No need to swap it.
2. **The growth loop is the prize** — the system compounds because each layer feeds the next and
   real use improves selection. The concrete next steps (all spec'd):
   - the **edge weights / pathway-vectors** on journey+recommend (so the graph learns the move),
   - the **comparative matrix seed** (so cross-text data exists to learn from),
   - the **feedback loop** (readers/learners rate → weights update).
3. **The division stays clean** — Hermes narrates; the graph decides. Both agents build on this
   (Agent 1: the learnable weights + benchmark; Agent 2: the structure + the analyst/journey).

---

## D. BOTTOM LINE

The geometricengine's deepest lesson is not its stack — it's that **a scholarly/pedagogical system
grows by a weighted graph that learns from its own use, while the LLM stays a narrator**. Pāṭala
already has the substrate and the deterministic floor; Hermes is (and should stay) the infra layer.
The growth is: add texts → push them → formalize arguments → compare → teach → learn from use → the
weights improve → more essays/lessons. That is the compounding loop, and it's all now spec'd across
`geometric.md`, `EDUCATION_VISION.md`, `WHAT_NEXT_PATALA.md`, and the ML consolidated build.
