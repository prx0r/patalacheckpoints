# DEVPATH 11 — EDUCATION COMPILER (Synthesis → LearningClaim → ...)

**Status: ✅ CLOSED (2026-08-13) — infra built + tested; production data empty (see honest gaps)**
**Route recorded 2026-08-13** (this file was absent while the README marked the route CLOSED; recorded for verifiability)
**Source of truth:** `docs/vision/education/EDUCATION_VISION.md` + `PATALA-EDUCATION-SYNTHESIS.md`

---

## Objective

Project the synthesis graph into a teaching surface: turn an `ArgumentSynthesis` (devpath8) into
structured learning interactions (interaction-definition JSON), gated by epistemic humility
(MACHINE_PROPOSED, never "consensus"), so the education layer is a *projection of the graph*, not a
new LLM re-argument.

## What was built

Two implementations exist (see honest gaps — this is a real structural concern):

1. **ML research compiler** — `machinelearning/research/patala_ml/education_compiler.py`
   - `ArgumentSynthesis → learning_interactions_from_synthesis → LearningInteraction[]` → `LearningBundle`.
   - Emits InteractionDefinition JSON (`interaction_type/prompt/options/feedback_rules/derived_from/target`).
   - Rule-based projection: SPEAKER_CLASSIFY, CRUX_IDENTIFY, COUNTEREVIDENCE_SELECT, SOURCE_GROUND.
   - Pure, no model calls; deterministic bundle_hash.
   - Test: `machinelearning/research/tests/test_education_compiler.py` (structural verification of the
     InteractionDefinition schema + no manufactured-consensus / no RESOLVED targets).

2. **Production pipeline worker** — `pipeline/education_worker.py`
   - Consumes a committed **ESSAY**, LLM-distills to `{title, summary, key_points}` (a "3-min explainer").
   - Deterministic gate: `education_validator` requires MACHINE_PROPOSED, committed source essay,
     non-empty summary, ≤1500 chars (distill-not-re-run), and absence of the `_OVERREACH` lexicon.
   - Wired into the autonomy controller: `autonomy.py` `LAYER_HANDLERS["EDUCATION"]`.
   - Test: `pipeline/test_theme_essay_education.py` (seeds 3 fake C1s → THEME → ESSAY → EDUCATION,
     verifies generator/validator incl. overreach rejection).

## Canonical placement

`contracts/CANONICAL-DAG.yaml`: `EDUCATION: requires: [ESSAY]` (and `ESSAY: requires: [SYNTHESIS]`).
So the canonical chain is `... → C1 → THEME/ARGUMENT → SYNTHESIS → ESSAY → EDUCATION`.

## Honest gaps (per AGENTS.md — "a tested schema is not a result")

- The two implementations are **not connected**: the ML compiler (the vision's path) is orphaned
  (imported only by its test); the production worker is an LLM essay-distillation and never touches
  `ArgumentSynthesis`. The graph-native `Synthesis → LearningClaim` pipeline the vision promises does
  not yet exist in the running system.
- Vision-only (no code): `LearningClaim` object, `LearningSkill`, `MasteryEvidence`, curricula,
  lesson plans, registers/mechanism-shapes, journeys, misconception maps. The production worker is
  LLM-driven (the opposite of the vision's "no LLM in the cognition path" principle).
- Declared-but-unimplemented skills: `PREMISE_ATTACH`, `WARRANT_RECONSTRUCT` (in `SKILLS` constant but
  never emitted).
- **Production data empty:** no committed EDUCATION objects above L0 in the registry
  (`education-registry.jsonl`, `synthesis-registry.jsonl` absent). All output is
  `status: MACHINE_PROPOSED`, no gold/blind-eval/human-adjudication.

## Acceptance (route criteria)

- Education is a canonical layer with a deterministic gate. ✅ (DAG + validator)
- ML compiler produces InteractionDefinition JSON from an ArgumentSynthesis. ✅ (tested)
- The synthesis→LearningClaim graph-native pipeline in production. ❌ NOT YET — next work.

## References

- `machinelearning/research/patala_ml/education_compiler.py` (ML compiler)
- `pipeline/education_worker.py` (production worker + validator)
- `docs/vision/education/EDUCATION_VISION.md`, `PATALA-EDUCATION-SYNTHESIS.md`
- `translations/_stack/ipvv/specs/SPEC_EDUCATION.md`
- `contracts/CANONICAL-DAG.yaml` (EDUCATION ← ESSAY)
