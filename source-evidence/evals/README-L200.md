# Inspect AI — PĀṬALA-L200-SYN v0.1

*2026-08-12. The **second** Inspect evaluation (Track C, Global Architecture v0.1). Ports the L200
typed-reference semantic layer — the layer that catches the exact failure the structural validator cannot:
**IA→MT laundering** (the F6 live canary produced 5 MTs on an IA-not-MT fixture; see
`factory-certificates/L200-v1/live-canary.md`).*

## Why this benchmark exists

The L200-v1 structural validator passed the F6 case **semantically wrong**: it cannot judge whether a
proposed MT is really a translation choice or an interpretive assertion laundered as one. The **typed
reference checker** (`certificate_l200.check_dim`) is the semantic gate that catches this, by checking each
proposal against typed reference conditions (`expected_mt` / `forbidden_mt` / `expected_ia` /
`required_open_items`). This task measures the checker's sensitivity to controlled mutations — the same
contract-first discipline used to fix ARG-LAUNDRY.

## Design (independent gold, frozen objects)

- **SUT:** `check_dim(proposal, fixture)` — the deterministic typed-reference checker.
- **GOLD is independent of the SUT** — verdicts come from the `FIXTURE_SPEC` (mutation semantics), never
  from running `check_dim`. A missed laundering is now a real failure.
- **Solver consumes only the FROZEN object** — each sample carries the proposal + fixture reference JSON as
  its input; the solver never sees which mutation was injected.
- **5 must-PASS controls + 6 must-FAIL mutations:**

| Fixture | Type | Verdict | Detects |
|---|---|---|---|
| F1/F2/F4/F5/F10 CLEAN | control | PASS | correct-by-fixture proposal |
| **F6_IA_AS_MT** | launder | **FAIL** | IA→MT laundering (`forbidden_MT_present:SUPPLIED`) |
| F1_FORBIDDEN_LEXICAL | launder | FAIL | MT precision (forbidden type present) |
| F1_MISSING_REQUIRED_MT | mutation | FAIL | MT recall (required MT missing) |
| F6_MISSING_IA | mutation | FAIL | IA recall (expected IA missing) |
| F3_MISSING_SOURCE_LAYER | mutation | FAIL | source-layer attribution |
| F9_MISSING_OPEN_ITEM | mutation | FAIL | open-item honesty |

The **F6_IA_AS_MT** case is the point: it mirrors the real F6 live failure and proves the typed-reference
checker catches what the structural validator cannot.

## Metrics

```text
verdict_accuracy       (correct / total)
clean_specificity      (1 - FPR)
mutation_sensitivity   (1 - FNR)
```

Result (v0.1, pinned runtime): **1.000 / 1.000 / 1.000 (11/11)**.

## Claim class

**PĀṬALA-L200-SYN** — synthetic sensitivity of the typed-reference checker to controlled mutations.
This does **not** establish L200-NAT (real live-model proposals independently typed) or whole-pipeline
behavior. The live proposer's MT/IA over/under-production is measured separately by `benchmark_l200_live.py`;
the Inspect task is the *contract* the live output is judged against.

## Run

```bash
machinelearning/research/.venv/bin/python source-evidence/evals/inspect_l200.py          # show fixtures
machinelearning/research/.venv/bin/python -m inspect_ai eval source-evidence/evals/inspect_l200.py
```

## Versioning

EvalLog metadata records `pinned_inspect=inspect-ai==0.3.258`, `dataset_hash`, and `sut_sha` (fingerprint of
`certificate_l200.py`, the SUT). Bumping any of these is an explicit re-record, never silent drift.
