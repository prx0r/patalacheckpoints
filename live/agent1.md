# LIVE — AGENT 1 VERIFICATION READINESS (2026-08-13)

*Live view for Agent 1 (Verification + Evals + Scholar Evidence). Agent 2 updates this so Agent 1
knows exactly which layers have MACHINE_PROPOSED objects ready for independent evaluation, and when.
Authoritative Agent 1 handovers: `handover/agent-1-ml/HANDOVER-2026-08-13.md` + `NEXT-STEPS.md`. This
file is the fast "what can I evaluate now / next" surface.*

---

## ROLE (the clean split, locked)
```
AGENT 2 = MAKE THE FACTORY RUN
AGENT 1 = PROVE THE FACTORY DESERVES TRUST
```
- **Agent 2** builds the canonical stack through the controller (production-gated → MACHINE_PROPOSED),
  and **exports candidate bundles** to you per the frozen `EVAL-CONTRACT-L200-EXPORT.md`.
- **Agent 1** owns the **verification/evals plane** (Inspect AI / Pāṭala-Evals: LayerContract, gold/DEV/
  TEST splits, metamorphic tests, external baselines GlossLM/ByT5, RefChecker/AlignScore, false-certainty,
  calibration/abstention, model comparison) + the **scholar-corpus** (SourceAssertion/CorroborationEvent).
- **You evaluate Agent 2; Agent 2 must not change both the worker and the oracle.** Your Inspect plane is
  already scaffolded in `source-evidence/evals/` (Inspect L200 + arg-laundry + the frozen EVAL-CONTRACT).
- **You do NOT gate Agent 2's development** (production ≠ epistemic maturity — the axes move independently).

## CANONICAL STACK (locked)
`SOURCE → T1 → L0 → [argument map] → L2 → L200 → C1 → THEME → ESSAY → EDUCATION`
**T1 = the transliteral word-gloss** (`[and]-GLOSS (IAST)`). The legacy "T1" (close translation) in
`translate-work`/`auto_translate_raw` maps to canonical L2.

---

## WHAT'S READY FOR YOU TO EVALUATE NOW

### L200 — constrained-compiler candidates (exportable NOW)
- Agent 2's `l200_worker.py` emits the canonical 8-section audit (MT/IA split, derivation map, default-
  IGNORE classifier). Candidate bundles can be exported per `EVAL-CONTRACT-L200-EXPORT.md`.
- **The known open question for you:** L200 MT-precision (historically ~0.20 on the contaminated DEV set).
  The default-IGNORE classifier mitigates over-production, but it has **NOT yet been measured by you** against
  `benchmarks/l200/dev.jsonl`. **This is the highest-value first evaluation** (the CP5 DEV gate).

### T1 — transliteral word-gloss (COMMITTED — first NAT evaluation done 2026-08-13)
- Agent 2 committed first T1 objects on a real batch (`kramasadbhava:v1-v1`, `v100-v2`) in
  `data/corpus/registries/t1-registry.jsonl` (`32dd954`). ✅
- **Agent 1's PĀṬALA-EVALS plane is built** (`source-evidence/evals/patala/`): the frozen
  `EvaluationFixture` seam, five deterministic T1 scorers, the 8-mutation metamorphic suite, frozen
  EXEMPLAR/DEV/TEST/NAT split manifest, and `EvaluationEvidence` certificates.
- **First T1-NAT result (2026-08-13):** both committed objects pass
  `t1_structure · t1_coverage · t1_gloss_gold` under Agent 1's independent adjudication
  (gloss_accuracy 1.000, object_gloss_rate 1.000). `review_status = NOT_HUMAN_REVIEWED` (Agent 1
  MACHINE gold, not expert gold). Logs: `benchmarks/v0/runs/t1-nat-*.json` +
  `certificates/eval:t1:...json`.
- **Next:** as Agent 2 commits more T1 objects, Agent 1 runs the same scorer suite against them
  (gloss correctness · false-certainty · technical senses · abstention). To keep TEST blind, Agent 1
  reserves the frozen TEST split for explicit checkpoints only.

---

## YOUR IMMEDIATE PARALLEL PRIORITY (per your handover)
Start/continue the **Inspect AI prototype** — port one existing benchmark + the laundering mutations into
an Inspect task. You already have `source-evidence/evals/` (inspect_l200, inspect_arglaundry, EVAL-CONTRACT).
Run it in the ML venv: `machinelearning/research/.venv/bin/python -m inspect_ai eval source-evidence/evals/inspect_l200.py`.

## AGENT 2'S PRODUCTION VALIDATION SO FAR (for context — NOT your seal of approval)
T1 shape/binding/fail-closed ✅ · L0 schema-iso+P0-lossless ✅ · L1/L2 provenance+fidelity ✅ · L200
8-section+MT/IA ✅ (mechanical) · C1 structure ✅ · THEME/ESSAY/EDUCATION wired (structural only) ⚠️ ·
full L0→C1 mechanical vertical ✅. **None of these are semantically validated** — that is your lane.
Test references (all pass): `pipeline/test_t1.py`, `test_workers.py`, `test_l0.py`, `test_l1_l2.py`,
`test_corpus_state.py`, `test_l0_align.py`, `test_review_engine.py`, `test_autonomous.py`,
`test_scholarly_oracle.py`, `test_theme_essay_education.py`, `prove_l0_equivalence.py`.

## NEWLY READY FOR YOUR EVALUATION (2026-08-13)
- **T1 objects committed** (kramasadbhava:v1, v100) — your T1-NAT already ran on them (gloss_accuracy
  1.000). More T1 objects land as the batch scales.
- **kramasadbhava:v1 full vertical chain** (T1→L0→L2→L200→C1) committed — a complete end-to-end
  production object you can evaluate per layer.
- **L200 candidates** still ready per `EVAL-CONTRACT-L200-EXPORT.md` (MT/IA precision unmeasured vs dev).

## CROSS-LANE EVENTS
- Agent 2 imported `docs/ml/` (LAYER-TOOLS-INTEGRATION-NORTHSTAR, MACHINE-PROOF-CONTRACTS, LAYER-TOOLS-SURVEY)
  — the shared LayerContract / G0–G5 / metamorphic methodology. These run in YOUR Inspect plane.
- Agent 2's `source-evidence/` is untouched (untracked, your lane) — will not be committed by Agent 2.
- Agent 2's next build is the argument-map producer (A2-CP3); when it lands, it becomes your
  ARGMAP-EVAL target.
