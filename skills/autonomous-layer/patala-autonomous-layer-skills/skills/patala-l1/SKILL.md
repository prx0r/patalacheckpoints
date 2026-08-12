---
name: Pāṭala L1 Controlled Translation Producer
version: 1.0.0
project: patala
kind: autonomous-layer-skill
layer: L1
status: canonical-proposal
inherits: ../../AUTONOMY_CONTRACT.md
---

# Purpose

Produce the controlled (word/phrase-faithful) L1 translation from committed L0 token analysis.

## Authority boundary
- L0 spans/hashes are deterministic proof; L1 is a MACHINE_PROPOSED close translation.
- Avagraha preserved; source span lossless; no doctrinal supplementation.

## Required inputs per item
- `object_id` · `source_sha256` · L0 committed refs
- token/span/morphology witnesses

## Generative task
Word/phrase-faithful close translation, preserving negation/polarity/case. No reading beyond the
controlled layer; interpretive moves go to L200 IA, not L1.

## Output contract (keyed by object_id, not position)
```json
{"batch_id":"...","items":[{"object_id":"...","source_sha256":"...","close":"...","uncertain":[]}]}
```

## Hard commit gate
- every requested item echoed with matching `object_id` + `source_sha256`
- no misbind (sha mismatch rejects the item)
- no silent repair of source corruption

## Validator
L1 semantic-fidelity validator: content(L1) ⊆ content(L0/L1-witnesses) + declared supplies.

## Certificate (before unattended scale)
replay/gold hidden · hard-failure rate · false-certainty · abstention · human review of failure clusters ·
cross-work · misbinding adversarial test · crash/idempotency.
