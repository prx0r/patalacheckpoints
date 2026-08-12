# Pāṭala Autonomous Layer Skills

Canonical skill bundle for repeating the crash-safe autonomous-factory pattern across the translation stack.

## Flow

`L0 → T1 → R1 → T2 → R2 → T3 → T3.1 → C1`

An additional `patala-l2` adapter is included because Pāṭala also has an existing L2 interpretive layer used by L0↔L2 alignment/argument work. It deliberately refuses to assume L2 == T3.1 or C1 unless the repository supplies an explicit mapping.

## Design

Every skill inherits `AUTONOMY_CONTRACT.md`:

- immutable-registry-derived idempotency
- stable ID + input-hash binding
- bounded batches/retries
- process-group cleanup
- single-writer locking
- fail-closed source/dependency handling
- immutable versioning/supersession
- provenance closure
- monotone no-strengthening
- proposal vs acceptance separation
- per-layer unattended-operation certificate

`patala-autonomy-controller` owns orchestration. Layer skills own generation contracts. `patala-layer-auditor` provides shared adversarial checks.

## Installation shape

Each skill is a directory containing `SKILL.md`, so the bundle can be copied into a Hermes/agent skill directory or adapted to another agent runtime without merging the layer instructions together.

## Critical boundary

These skills specify how autonomous proposal factories should behave. They do **not** assert that every stage currently has a completed empirical certificate. The L0 factory in particular must complete its Sanskrit-only replay/failure-rate/false-certainty certificate before unattended scale; downstream layers require their own replay/gold gates.

## Recommended next implementation order

1. wire `patala-autonomy-controller` into the existing Agent 2 registry/state machine
2. make L0 idempotent and process-safe
3. certify L0
4. reuse the controller unchanged for T1
5. then R1/T2/R2/T3/T3.1/C1 sequentially, each with its own registry key + validator + certificate
6. only then let a cron/Hermes agent request bounded runs

The key architecture is that **the controller repeats; the scholarly contract changes by layer**.
