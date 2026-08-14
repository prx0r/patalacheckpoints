# LAYER 05 — RESEARCH / EPISTEMIC CORE (the moat)

> **STATUS: PARTIAL — argument/crux/synthesis compilers + golds EXIST; 0 essay/education objects (the upper projections are design)** (derived live state — see `docs_state.py`)


*Part of the `NAVIGATION.md` layer map (the master tree / spine). The Pāṭala-native epistemic engines — the moat nobody else has.*

## 1. What it is
The engines that turn canonical passages into propositions → arguments → cruxes → synthesis, then into
essays/education/review. The "Agent 1" lane (`machinelearning/research/patala_ml/`).

## 2. Purpose
Own the semantics of evidence, interpretation, argument, disagreement, and downstream consequence.
This is the layer competitors cannot copy — it combines primary passage → linguistic analysis →
translation decision → proposition → argument → objection → crux → scholarly adjudication →
machine-readable trust → educational proof.

## 3. External tools used
Vidyut (linguistic analysis) · the commentarial-graph extraction tools (SocraticKG, DSPy — planned) ·
the verifier ensemble (RefChecker, AlignScore — planned). See `external-tools.md`.

## 4. Data
- `machinelearning/research/patala_ml/` — the engines (argument, crux, synthesis, essay, education).
- Golds: `gold002.py`…`gold005.py`, `benchmarks/`.
- Evals: `source-evidence/evals/patala/tasks/` (ArgumentBench, Synthesis-NAT, etc.).

## 5. Processes

**TARGET:**
```
C1 interpretations → propositions → arguments → cruxes (load-bearing disagreement) → ArgumentSynthesis
→ EssayPlan/EssayClaim or LearningClaim/Skill/Interaction (projections of one synthesis)
```
The convergence object: **ArgumentSynthesis** (question/frame/positions/arguments/cruxes). Clustering ≠
Theme; machine proposes, human promotes. Essay/education/review are loss-constrained renderers.

**CURRENT LIVE STATE (from object_registry):**
```
ARGUMENT=10 objects real · SYNTHESIS=0 · ESSAY=0 · EDUCATION=0
```
> The compilers (essay_compiler, education_compiler) EXIST as code but have produced **0 objects**. The
> epistemic engines (argument, crux, synthesis) are real; the upper projections are DESIGN not built.
> Live state renders from `python3 docs/process/docs_state.py` — never hand-edit.

## 6. Implementations
- `proposition_layer.py` · `argument.py` · `aspic_adapter.py` · `crux_engine.py` · `nyayagate.py`.
- `synthesis_core.py` · `theme_discovery.py` · `cluster.py` · `strength.py`.
- `essay_compiler.py` · `essayplan.py` · `essayverify.py` · `essaysentence.py`.
- `education_compiler.py` · `education_ir.py`.
- `layered_scholarship.py` (INTERPRETATION ≠ EVIDENCE) · `semantic_alignment.py` · `retrieval.py`.
- Tests: 39/41 ML tests pass (2 stale-drift failures).

## 7. Docs
- `docs/process/07-ml-epistemic-core.md` — the detailed layer guide.
- `docs/global/globalgoal.md` + `agent1atlas.md` — the ArgumentSynthesis convergence doctrine.
- `docs/vision/essayguide.md` — the essay research program.
- `docs/vision/education/PATALA-EDUCATION-SYNTHESIS.md` — the education objects.
- `endgamebuild/INFRA-INVENTORY.md` §3 — the ML inventory.
