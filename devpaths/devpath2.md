# DEVPATH 2 — G2: close the T1/L0 correction loop

**Status: ⛔ BLOCKED (needs Agent 2 `factory_rebuild(cidgagana:v1)`)**

---

## Objective

Prove the Pāṭala thesis on one real passage: production defect → independently frozen finding →
targeted repair → dependency rebuild → blind retest → proof refresh. This closes the 6-finding bundle.

## Already built (Agent 1 side)

- `EvaluationFinding` + `EvaluationCandidate` contracts (both directions, exact-version) — see
  `devpaths/devpath1.md` (E2-01 delivered the cross-lane objects).
- The 6-finding bundle: `data/evaluation/findings/` — EF-T1-2026-0001..0004 (T1) + EF-L0-2026-0001/0002.
- Regression fixtures (T1-REG-001..004) + `t1_regression.py`.
- Per-passage proof envelope (`proof_envelope.py`).

## The G2 exit test (cidgagana:v1 first — its T1 error propagates to L0)

1. **Agent 2** consumes the bundle → fixes the segmentation root class →
   `factory_rebuild(cidgagana:v1)` → emits an `EvaluationCandidate` (new exact version) +
   `ImpactReport` (trigger=`EF-T1-2026-0003`).
2. **Agent 1** blind-retests on the NEW exact version:
   - T1-REG-003 (gaṇeśaḥ) → expect FAIL→PASS
   - L0 losslessness for cidgagana:v1 → expect FAIL→PASS
   - proof envelope → expect FAIL→PASS
   - old versions still citable; an unrelated control passage unchanged.
3. **Agent 1** marks the findings RESOLVED (only Agent 1 can close).

## Acceptance

- One passage completes the full cycle with exact versions + immutable findings + targeted
  regeneration + independent re-verification.
- `ImpactReport` records the consequence; the retest IDs attach to it.

## Gate

⛔ **Blocked on Agent 2** running `factory_rebuild(cidgagana:v1)`. Do not chase until that output
lands. Once the new `EvaluationCandidate` is emitted, use the `EvaluationFinding.retest()` lifecycle
(from devpath1) to close findings.

## References

- `endgamebuild/SPEC-CLOSE-G2.md` (a1b) · `docs/global/PATALA-GLOBAL-ARCHITECTURE.md` (dependency
  propagation) · `docs/global/GLOBAL-NEXT.md`.
