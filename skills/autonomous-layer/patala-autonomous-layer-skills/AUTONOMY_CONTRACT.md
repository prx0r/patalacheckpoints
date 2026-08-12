# Pāṭala Autonomous Layer Contract v1.0

This contract is inherited by every autonomous layer skill in this bundle.

## Core invariant

Autonomy = deterministic state machine + bounded generative proposal calls + deterministic validators.

The model is never the authority for completion, provenance, state transitions, or acceptance.

## Canonical state machine

For a stable input object `x` and layer `L`:

```
UNSEEN
  -> GENERATING
  -> GENERATED
  -> VALIDATING
  -> COMMITTED

bounded failure exits:
  GENERATION_FAILED
  RESPONSE_SCHEMA_FAILED
  SOURCE_BLOCKED
  VALIDATION_FAILED
  DEPENDENCY_BLOCKED
  REVIEW_REQUIRED
```

Only COMMITTED objects count as durable progress. GENERATING/GENERATED/VALIDATING are ephemeral run state.

## Idempotency

Completion MUST be derived from immutable/versioned registry truth, never from a mutable cursor alone.

```
stable_object_id + layer + input_version_hash
        |
        +-- acceptable committed output exists -> SKIP
        +-- no acceptable committed output      -> ELIGIBLE
```

A ledger may cache/report progress, but it is not the source of truth.

Never use byte-identical model output as the dedup key. Generative output is nondeterministic.

## Stable binding contract

Every requested item must include:

- `object_id`
- `input_version_hash` or `source_sha256`
- `layer`
- exact dependency refs

Every model result must echo the same identifiers. Reject unknown IDs, duplicate IDs, missing hashes, or hash mismatches. Never bind outputs by array position alone.

## Batch policy

- bounded batches; default 8 items until a layer-specific certificate says otherwise
- a malformed item fails that item, not neighboring items
- JSON/schema failure => one bounded retry, then split batch
- timeout => kill the entire model process group, one bounded retry, then split/record failure
- never let one failed batch cause committed neighbors to be regenerated

Optimize validated committed objects per call, not raw tokens per call.

## Single-writer rule

Exactly one canonical writer may commit a given layer registry at a time. Acquire an OS-level lock (`flock` or equivalent) before eligibility selection and hold it through commit bookkeeping.

Agents/cron may request work; they do not own canonical state transitions.

## Immutability and supersession

Never edit a committed scholarly object in place. Corrections create a new version that supersedes the prior version while preserving history and review events.

## No-strengthening rule

For any transformation P from an upstream object x to a downstream object:

`authority(P(x)) <= authority(x)`

and natural-language content must not exceed licensed content except through explicitly referenced, separately grounded additions.

Missing review is `NOT_AUDITED`, never presumed accepted.

## Provenance closure

A committed output must retain enough machine-resolvable refs to walk back to every load-bearing dependency. A summary source list that omits a load-bearing dependency is incomplete.

## Fail-closed classes

Always fail/abstain rather than guess on:

- unresolved source corruption/OCR
- unknown input version
- missing prerequisite layer
- speaker/attribution ambiguity that changes meaning
- semantic expansion without backing refs
- source/result ID mismatch
- validator disagreement at a hard gate

## Proposal vs acceptance

Generative outputs are machine proposals unless a layer-specific rule explicitly permits deterministic derivation. A model may propose a correction/challenge; it must never silently mutate accepted upstream data.

## Layer certificate

No layer may be released for unattended high-throughput operation until it has:

1. replay/gold set hidden from generation
2. independently measured hard-failure rate
3. false-certainty/unsupported-assertion metric
4. abstention metric where applicable
5. human inspection of failure clusters
6. cross-work/domain test
7. known cost and review burden
8. crash/restart idempotency test
9. orphan-process cleanup test
10. wrong-ID/misbinding adversarial test

## Required run report

Every bounded run emits a machine-readable report containing:

- run_id
- layer
- model/backend + prompt/skill version
- input count / skipped count
- committed count
- validation failures by class
- source/dependency blocks
- retry/timeout counts
- per-item object_id + input hash + output version id + verdict
- wall-clock/cost if available

The report is evidence about a run, not proof of scholarly correctness.
