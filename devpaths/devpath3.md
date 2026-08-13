# DEVPATH 3 — G3A: ARGMAP NAT on real Agent 2 output

**Status: ⛔ BLOCKED (needs a real ARGMAP batch)**

---

## Objective

Run the ARGMAP NAT harness (built in devpath1, E2-01) on Agent 2's real ARGMAP objects. This is the
moment the harness stops being "waiting-time" and starts producing real findings.

## The route

- For each real ARGMAP map Agent 2 commits:
  - wrap it in the shared `EvaluationCandidate` (`from_registry_row`);
  - run `verify_argmap()` (the bounded verifier from devpath1);
  - measure the 8 contract dimensions (NODE/ROLE/EDGE/SPEAKER/SCOPE/OPEN/INFERENCE/SUPPORT);
  - freeze naturally-occurring failures as `EvaluationFinding`s (the G3 loop).
- Do NOT invent an ARGMAP-specific handoff — reuse the cross-lane EvaluationCandidate/EvaluationFinding.

## Acceptance

- The ARGMAP NAT task (`argmap_eval.py`) reports all dimensions on a real batch.
- Naturally-occurring failures are frozen as `EvaluationFinding`s; `mutation_sensitivity` becomes
  well-defined (non-NaN) once real defects exist.
- `SPEAKER_COLLAPSE` and `SCOPE_INFLATION` families are exercised on real output.

## Gate

⛔ **Blocked on Agent 2** emitting a real ARGMAP batch (the worker is done; the corpus is pending).
The harness is ready — this is the first thing to run when the batch lands.

## References

- `source-evidence/evals/patala/tasks/{argmap_eval,argmap_ipvv_eval,argmap_contract,evaluation_finding,evaluation_candidate}.py` (devpath1)
- `endgamebuild/SPEC-EPISTEMIC-CORE.md` (A3) · `handover/agent-2-integration/`.
