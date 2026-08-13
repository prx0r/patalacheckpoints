# DEVPATH 1 — Wire the Nyāya gate + build the ARGMAP NAT harness

**Status: ✅ CLOSED (2026-08-13)**
**Commit:** `3df0955` (local, agent2 branch)

---

## Objective

Start here. Two unblocked items from `endgamebuild/HANDOVER-TO-NEW-AGENT.md`:
1. **E2-02** — wire the Nyāya gate into `argument.py` as a bounded structural/evaluative gate (NOT a
   truth oracle).
2. **E2-01** — build the ARGMAP NAT harness using the SAME cross-lane object as T1
   (`EvaluationCandidate → ARGMAP NAT → EvaluationFinding`), not an ARGMAP-specific handoff.

## Discipline (from the handover, non-negotiable)

- Do NOT broaden the ontology, build more synthetic eval infra, or disappear into the external-tool
  migration (Pydantic/NetworkX/OpenLineage wait until G2 closes + real ARGMAP flows).
- The gate is a **bounded evaluator**: PASS/PASS_WITH_OPEN/FAIL with dimensions
  (pratijna/hetu/scope/support_relation) — never `argument_valid=true`.
- Use the same cross-lane object as T1 for the ARGMAP NAT — do NOT invent an ARGMAP-specific handoff.

## Work completed

### P1 (E2-02) — bounded Nyāya gate

`machinelearning/research/patala_ml/nyayagate.py`:
- Added `verify_claim_semantic(claim, peer_claims, gold_propositions)` → dict:
  - maps the deterministic 5-hetvābhāsa gate + optional graph viruddha onto a bounded verdict
    (`PASS / PASS_WITH_OPEN / FAIL`);
  - reports the 4 dimensions (pratijna/hetu/scope/support_relation), each `CLEAN | OPEN | DEFECT`;
  - **never** emits `argument_valid=true` or "proven" — a clean result is engineering/structural
    (per GLOBAL-STATE §8 and NYAYA-GATE-CANDIDATE-V1);
  - a graph viruddha always → `FAIL` + `can_update_posterior=False`;
  - `validate()` / `gate_claim()` untouched (fully additive).
- `machinelearning/research/tests/test_verify_claim_semantic.py` — 12 checks, all pass.

Note: the gate slot in `argument.py` was already wired via `audit_argument()` → `validate()`
(construction vs contextual-audit separation by design). This route added the missing bounded
`verify_claim_semantic` evaluator the handover names as the target.

### P2 (E2-01) — ARGMAP NAT harness (cross-lane)

`source-evidence/evals/patala/tasks/`:
- **`evaluation_candidate.py`** — the shared `EvaluationCandidate` (frozen, exact-version, hashed),
  `from_registry_row()` wraps a layer-registry row. Same object for T1 and ARGMAP.
- **`evaluation_finding.py`** — the shared `EvaluationFinding` (schema `EvaluationFinding-v1`, same
  as the 6-finding bundle). Lifecycle `OPEN → retest(PASS)=RESOLVED / retest(FAIL)=STILL_FAILING`.
- **`argmap_contract.py`** — the 8 contract dimensions (NODE/ROLE/EDGE/SPEAKER/SCOPE/OPEN/INFERENCE/
  SUPPORT) + 6 core mutation families (OBJECTION_AS_AUTHOR_VIEW, GROUNDING_AS_INFERENCE,
  PREMISE_CONCLUSION_SWAP, RESPONSE_DIRECTION_FLIP, FALSE_CONTRADICTION, INVENTED_BRIDGE) +
  OPEN_AS_RESOLVED + SPEAKER_COLLAPSE + SCOPE_INFLATION. `check_shape()` checks the canonical
  4-section shape.
- **`argmap_eval.py`** — `PĀṬALA-ARGMAP-NAT` Inspect task over the committed ARGMAP registry.
  `verify_argmap()` is a bounded structural/evaluative verifier (critic, not generator).
- **`argmap_ipvv_eval.py`** — the IPVV-exemplar variant (`PĀṬALA-ARGMAP-NAT-IPVV`), adding a
  semantic-coverage dimension against the hand-authored `pilot_V2O_ARGUMENT_MAP.md` claims.
- **`test_argmap_nat.py`** — cross-lane contract + shape + mutation families + verifier behavior
  (clean→PASS; scope inflation→FAIL; silently-resolved open item→FAIL). All checks pass.

## Acceptance / verification

| Check | Result |
|---|---|
| `test_verify_claim_semantic.py` (P1) | 12/12 PASS |
| `test_nyaya_gate_wiring.py` (pre-existing, regression) | PASS |
| `test_argmap_nat.py` (P2 cross-lane) | PASS |
| `argmap_eval.py` (Inspect, `--model mockllm/mockllm`) | shape_pass_rate 1.000 (kramasadbhava:v1) |
| `argmap_ipvv_eval.py` (Inspect) | coverage_recall 1.000 |

## Honest boundary

- The ARGMAP verifier is an **engineering/structural critic** — NOT_HUMAN_REVIEWED. A clean map is
  engineering-valid, NOT scholar-correct.
- `mutation_sensitivity` is `NaN` until a real defect is frozen into the NAT corpus (the one committed
  map is clean).
- This route is the "waiting-time" work: the harness is ready the moment Agent 2 emits a real ARGMAP
  batch (that consumption is devpath3 / G3A).

## Exit → next

devpath1 is complete. Next: **devpath2 (G2)** — but it is blocked on Agent 2's
`factory_rebuild(cidgagana:v1)` consuming the 6-finding bundle. See `devpaths/devpath2.md`.

## Files

- `machinelearning/research/patala_ml/nyayagate.py` (modified)
- `machinelearning/research/tests/test_verify_claim_semantic.py` (new)
- `source-evidence/evals/patala/tasks/{evaluation_candidate,evaluation_finding,argmap_contract,argmap_eval,argmap_ipvv_eval,test_argmap_nat}.py` (new)
- `devpaths/README.md`, `devpaths/devpath1.md` (this file)
