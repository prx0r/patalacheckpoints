---
name: Pāṭala Autonomous Layer Controller
version: 1.0.0
project: patala
kind: autonomous-layer-skill
layer: CONTROL
status: canonical-proposal
inherits: ../../AUTONOMY_CONTRACT.md
---

# Purpose

Run any Pāṭala layer as a resumable, idempotent, single-writer proposal factory. This skill does not generate scholarly content itself; it dispatches to exactly one layer skill and enforces the shared control-plane contract.

# Inputs

- target layer skill
- immutable registry/read view
- eligible work/object selector
- bounded batch configuration
- generative backend adapter (`HermesAdapter`, direct model adapter, etc.)
- deterministic validator(s)

# Procedure

1. Acquire the single-writer lock.
2. Recompute eligibility from immutable registry truth.
3. Select the next bounded set of stable IDs; never use a mutable cursor as authority.
4. Materialize each request with `object_id`, input/dependency hashes, layer, exact refs.
5. Call the layer skill through the backend adapter.
6. Parse by stable ID, never positional order.
7. Reject unknown/duplicate IDs and hash mismatches before semantic validation.
8. Run layer-specific deterministic validation.
9. Commit only passing objects as new immutable versions.
10. Emit failure records for rejected items without advancing them to committed.
11. Recompute progress from the registry and write the run report.
12. Release the lock.

# Retry policy

One retry for transport/schema failure. If the retry fails, split the batch once. Persistent failure becomes a durable failure record; do not loop indefinitely.

# Process ownership

Launch model CLIs in their own process group/session. On timeout: SIGTERM group -> short grace -> SIGKILL group. Verify no descendants remain.

# Cron/agent boundary

An agent may choose *what bounded run to request*. The deterministic controller decides what is already done, what is eligible, whether validation passed, and what may commit.

# Acceptance test

Crash the controller after generation but before commit; restart. No committed object is regenerated and no object is double-committed for the same input version.
