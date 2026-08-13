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

### T1 — transliteral word-gloss (NOT yet committed on a real batch — will announce)
- Worker built + production-validated, but T1 objects are not yet committed to the registry on a real
  batch. When Agent 2 commits them, they become your **CP1 T1 benchmark** target (gloss correctness,
  false-certainty, technical senses, abstention — the machineproof `T1` contract).

---

## YOUR IMMEDIATE PARALLEL PRIORITY (per your handover)
Start/continue the **Inspect AI prototype** — port one existing benchmark + the laundering mutations into
an Inspect task. You already have `source-evidence/evals/` (inspect_l200, inspect_arglaundry, EVAL-CONTRACT).
Run it in the ML venv: `machinelearning/research/.venv/bin/python -m inspect_ai eval source-evidence/evals/inspect_l200.py`.

## AGENT 2'S PRODUCTION VALIDATION SO FAR (for context — NOT your seal of approval)
T1 shape/binding/fail-closed ✅ · L0 schema-iso+P0-lossless ✅ · L1/L2 provenance+fidelity ✅ · L200
8-section+MT/IA ✅ (mechanical) · C1 structure ✅ · THEME/ESSAY/EDUCATION wired (structural only) ⚠️ ·
full L0→C1 mechanical vertical ✅. **None of these are semantically validated** — that is your lane.

## CROSS-LANE EVENTS
- Agent 2 imported `docs/ml/` (LAYER-TOOLS-INTEGRATION-NORTHSTAR, MACHINE-PROOF-CONTRACTS, LAYER-TOOLS-SURVEY)
  — the shared LayerContract / G0–G5 / metamorphic methodology. These run in YOUR Inspect plane.
- Agent 2's `source-evidence/` is untouched (untracked, your lane) — will not be committed by Agent 2.
