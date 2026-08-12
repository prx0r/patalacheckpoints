---
name: Pāṭala L2 Read Producer
version: 1.1.0
project: patala
kind: autonomous-layer-skill
layer: L2
status: canonical-proposal
inherits: ../../AUTONOMY_CONTRACT.md
---

# Purpose

Produce the L2 READ: readable English prose answering "what does the text say?" — the published reading
layer (see `pilot/pilot_*_L2_read.md`, `c1andmore.md`).

## Authority boundary
- Input: committed L1 + source links.
- The invariant: `content(L2) ⊆ content(L1) + declared_supplies`. A readability model may restructure
  language aggressively, but every substantive clarification beyond the controlled layer must become
  explicit (a declared supply or an L200 IA), never smuggled in as prose.
- L2 is a MACHINE_PROPOSED reading, not commentary (C1) and not justification (L200).

## Required inputs per item
- `object_id` · committed L1 refs · L0/source refs · argument/read-map

## Generative task
Readable, Dyczkowski-mode prose derived from the argument map + L1. Every sentence's substantive
content must be licensed by L1 (with declared supplies for anything added).

## Output contract
```json
{"batch_id":"...","items":[{"object_id":"...","paragraphs":[{"text":"...","refs":["pt:l1:...","pt:l0:..."]}]}]}
```

## Hard commit gate (semantic-fidelity validator, NOT English-style checks)
- each L2 ¶ maps to explicit L1 + L0/source refs
- any substantive clarification beyond L1 is flagged as a declared supply (→ L200 §3) or an IA (→ L200 §4)
- no unsupported conceptual expansion

## Validator
content(L2) ⊆ content(L1) + declared_supplies, checked per sentence against its refs.

## Certificate
replay/gold hidden · semantic-fidelity (unsupported addition) · abstention · human review of failure
clusters · cross-work · misbinding adversarial test.
