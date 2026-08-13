# L200 Candidate Export Contract — Agent 2 → Agent 1 (lane-safe, read-only)

*2026-08-12. Defines the immutable bundle Agent 2 writes ONCE for a live L200 candidate, and that Agent 1
consumes READ-ONLY as NAT evaluation material. No Agent 1 modification to the proposer or the candidate.
This is the clean lane boundary before NAT collection starts.*

## The bundle (Agent 2 writes exactly this, once)

```json
{
  "candidate_id": "pt:l200-run:...",
  "producer_lane": "agent2",
  "produced_at": "...",

  "inputs": {
    "source_ref": "...",
    "source_hash": "...",

    "l0_ref": "...",
    "l0_hash": "...",

    "l1_ref": "...",
    "l1_hash": "...",

    "l2_ref": "...",
    "l2_hash": "..."
  },

  "producer": {
    "model": "...",
    "prompt_hash": "...",
    "worker_sha": "...",
    "runtime": "...",
    "run_id": "..."
  },

  "proposal": { ... },

  "structural_validation": {
    "validator_sha": "...",
    "result": "PASS"
  },

  "hash_algorithm": "sha256",
  "canonicalization": "json-sort-keys-v1",
  "bundle_hash": "..."
}
```

## Bundle hash — canonicalization rule (NOT self-referential)

`bundle_hash` must **not** literally cover itself. Compute it over the canonical bundle **excluding** the
`bundle_hash` field:

```text
bundle_hash =
SHA256( canonical_json( bundle WITHOUT the bundle_hash field ) )
```

Freeze canonicalization exactly:

```text
encoding         : UTF-8
object keys      : sorted (byte-wise)
separators       : compact  {",", ":"}
unicode          : normalized consistently (NFKC) before hashing; preserved in the stored JSON
bundle_hash field: omitted from the hashed document
hash_algorithm   : sha256
canonicalization : json-sort-keys-v1
```

Agent 1 **independently recomputes** `bundle_hash` on ingest and must reject the bundle on mismatch.

## Guarantees

- **Immutable**: Agent 2 writes the bundle once. `bundle_hash` covers all fields except itself (inputs,
  producer, proposal, structural_validation, hash metadata). Any edit changes the hash → detectable.
- **Frozen inputs (all four derivational layers)**: the object proves exactly which versions of SOURCE, L0,
  L1 and L2 produced this candidate — each with its ref AND hash. This matters because Agent 2 is moving
  L200 onto `L0 + L1 + L2` inputs (not only L1 + L2).
- **Producer provenance**: model, prompt hash, worker SHA, runtime, run id — so a future change in the
  proposer is traceable.
- **Read-only boundary**: Agent 1 never modifies `candidate.json` (the bundle) or the proposer. Agent 1
  creates only NEW files: the independently adjudicated `adjudication.json` (and, for ARG, the authority
  snapshot).

## Agent 1 consumes read-only; Agent 1 separately creates

```text
nat/l200/<candidate_id>.candidate.json        (Agent 2's bundle, frozen, read-only)
nat/l200/<candidate_id>.adjudication.json     (Agent 1: independent adjudication = gold)
```

## What the adjudication contains (gold, separate from the candidate)

- verdict: PASS / FAIL
- violations: `[{family, sentence/span_ref, reason, expected_detector_rule, derivation_stage}]`
- `first_unsupported_layer` (epistemic axis) AND `derivation_stage` (factory axis) where applicable
- `uncertain: []`
- **adjudicator provenance** — who/what produced the adjudication (Agent 1 machine-assigned gold is NOT
  expert gold; label it exactly):

```json
{
  "adjudicator": {
    "type": "MACHINE",
    "agent": "agent1",
    "model": "...",
    "prompt_hash": "..."
  },
  "review_status": "NOT_HUMAN_REVIEWED"
}
```

`adjudicator.type`: `MACHINE | HUMAN | EXPERT | DUAL`. `review_status`: `NOT_HUMAN_REVIEWED |
HUMAN_REVIEWED | EXPERT_REVIEWED`. Later scholar-reviewed cases upgrade the `review_status` separately.

## Lane rule

> Agent 1 may consume Agent 2's frozen candidates as evaluation material, but must not tune or modify
> Agent 2's translation proposer. Agent 2 may later consume Agent 1's evaluation-runtime patterns.
> Agent 1 reports results; Agent 2 chooses what to change. Agent 1 never mutates the producer.
