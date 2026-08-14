# 07 — ML EPISTEMIC CORE (propositions → arguments → synthesis → essay/education)

*Part of `docs/process/README.md`. This is the **epistemic upper layer** (Agent 1): the Pāṭala-native
machinery that turns the canonical passages/translations (from the factory) into propositions,
arguments, cruxes, synthesis, and downstream essays/education/review. This is the **moat** — the layer
nobody else has.*

> Previously this lane was deliberately excluded from the process guides. This guide covers it so the
> full repo has a complete layer map. The code lives in `machinelearning/research/patala_ml/`.

---

## 1. The layer stack (what the factory's output feeds)

```text
FACTORY OUTPUT (C1 interpretations, passages)   ← 03-factory.md
   ↓
PROPOSITIONS   (proposition_layer.py)
   ↓
ARGUMENTS      (argument.py, aspic_adapter.py, aifgraph.py)
   ↓
CRUXES         (crux_engine.py)  — the minimal load-bearing disagreement
   ↓
SYNTHESIS      (synthesis_core.py, theme_discovery.py)  ← the convergence object
   ↓
ESSAY / EDUCATION / REVIEW   (projections over the same synthesis)
   ↓
COMMENTARIAL GRAPH (scholars over the same synthesis)    ← 06-commentarial-graph.md
```

## 2. The reusable engines (machinelearning/research/patala_ml/)

| Concern | Module | Role |
|---|---|---|
| Propositions | `proposition_layer.py` | extract/type propositions from passages |
| Arguments | `argument.py`, `builders.py`, `aspic_adapter.py`, `aifgraph.py` | argument reconstruction + ASPIC/AIF interop |
| Nyāya gate | `nyayagate.py` | bounded domain gate — NEVER truth |
| Cruxes | `crux_engine.py` | perturbation-derived cruxes (the load-bearing disagreement) |
| Synthesis | `synthesis_core.py`, `theme_discovery.py`, `cluster.py`, `kcore.py` | the ArgumentSynthesis / Theme objects |
| Strength | `strength.py` | honest Bayesian claim strength |
| Scholarship | `layered_scholarship.py` | INTERPRETATION ≠ EVIDENCE |
| Semantic | `semantic_alignment.py`, `retrieval.py`, `pushing.py` | term sense + retrieval |
| Essay | `essay_compiler.py`, `essayplan.py`, `essayverify.py`, `essaysentence.py`, `essaygen.py`, `essay.py` | ArgumentSynthesis → EssayPlan → EssayClaim → prose |
| Education | `education_compiler.py`, `education_ir.py` | ArgumentSynthesis → LearningClaim → interactions |
| Gold | `gold002.py`…`gold005.py`, `gold.py`, `goldchain.py` | the argument golds |

## 3. The core objects (Pāṭala-native)

- **`Proposition`** — a claim extracted from a passage (the atom below arguments).
- **`Argument`** — premises → conclusion with support/attack.
- **`Crux`** — the minimal load-bearing disagreement whose resolution changes conclusion status.
- **`ArgumentSynthesis`** — the convergence object (question/frame/positions/arguments/cruxes).
- **`Theme`** — a versioned scholarly grouping (machine proposes, human promotes).
- **`DerivedScholarlyObject`** — the universal envelope with the 4-axis `Authority` vector
  (generation/evidence/review/publication) + `derive_ceiling()` (R3: ceiling is DERIVED).

## 4. The doctrine (anti-theatre, from AGENTS.md + AGENTS-DOCTRINE.md)

1. **No "final truth object."** `ArgumentSynthesis` says "under frame DF4, Position A has args X/Y,
   Position B has objection Z, decisive crux is CRUX-12" — NOT "conclusion = true."
2. **Clustering ≠ Theme.** A Louvain cluster is a `ThemeCandidate`; human promotion makes a `Theme`.
3. **Essay/education/review are loss-constrained renderers** over one synthesis — never separate truths.
4. **MACHINE_PROPOSED ≠ ACCEPTED.** Extraction/reconstruction is reviewable, never model-truth.
5. **The ceiling law:** `authority(projection) ≤ authority(parent)`.

## 5. Current gaps (from PROJECT-AUDIT — do not reintroduce)

- **ARGUMENT / SYNTHESIS have NO real worker** — DAG ends at C1; `autonomy` falls back to a stub.
- **THEME/ESSAY/EDUCATION not reachable via the live `factory_loop.sh`** — workers exist, nothing triggers them.
- 2 stale-test failures (`test_evidence_aware_essay`, `test_vertical`) — data-drift, not code bugs.

---

## 6. The full-repo layer map (the complete picture)

```text
INGESTION (01)        sources → ExternalRecords → reconcile → canonical objects
   ↓
ATLAS (02)            the canonical graph (Postgres + R2 + ledger) — the immutable reference
   ↓
FACTORY (03)          SOURCE→T1→L0→ARGMAP→L2→L200→C1 (the compiler)
   ↓
EPISTEMIC CORE (07)   propositions → arguments → cruxes → synthesis   [MOAT]
   ↓
COMMENTARIAL GRAPH (06)  scholar positions/questions over the primary graph
   ↓
ESSAY / EDUCATION / REVIEW / MEDIA   (projections over one synthesis)
   ↓
SITES / APIs (05)     both sites + MCP read the SAME canonical truth
```
Beneath it all: R2 (04, immutable bytes) + external tools (borrowed) + repos-to-raid (githubclones).
