---
name: Pāṭala Theme Synthesis Producer
version: 1.0.0
project: patala
kind: autonomous-layer-skill
layer: THEME
status: canonical-proposal
inherits: ../../AUTONOMY_CONTRACT.md
---

# Purpose

Produce THEME dossiers: evidence-backed synthesis of how an idea develops across the work, from a graph
of accepted/proposed C1 assertions (NOT bare text clustering). Cluster ≠ theme.

## Authority boundary
Every member claim must have C1 evidence; a theme never exceeds the authority of its member C1s.
Synthesis is now expected (unlike C1) but must be edge-evidenced.

## Required inputs
- accepted/proposed C1 assertions (with `object_id` + status)
- term senses · cross-references · local arguments · speaker/position · L200 provenance

## Proposal engines (signals, then the skill synthesizes)
```
deterministic: k-core · explicit cross-ref connectivity · recurring term/sense · argument dependency
heuristic:     Louvain/community · semantic similarity · PPR neighborhoods
neural:        BGE/ColBERT (later)
```

## Output contract
```json
{
  "theme_id": "...", "label": "...", "member_claims": [],
  "development": [], "counterexamples": [], "edge_evidence": [],
  "status": "MACHINE_PROPOSED"
}
```

## Hard commit gate
- every member_claim has a resolvable C1 `object_id` with evidence
- development spans the work, not a single passage
- counterexamples / tensions recorded, not flattened
- status is MACHINE_PROPOSED (never ACCEPTED)

## Validator
Deterministic: all member C1 ids resolve; no member without C1 evidence; theme id stable.

## Certificate
replay/gold hidden · false-certainty (claim without evidence) · abstention · human review of failure clusters ·
cross-work · misbinding adversarial test.
