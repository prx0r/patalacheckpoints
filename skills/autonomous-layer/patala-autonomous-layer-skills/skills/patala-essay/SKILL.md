---
name: Pāṭala Essay Producer
version: 1.0.0
project: patala
kind: autonomous-layer-skill
layer: ESSAY
status: canonical-proposal
inherits: ../../AUTONOMY_CONTRACT.md
---

# Purpose

Render a structured synthesis into proof-carrying prose. The essay skill does NOT do philosophical
reasoning from scratch — it renders the ArgumentSynthesis (cruxes + epistemic ceiling) into prose with
every sentence evidence-audited.

## Authority boundary
The essay must not exceed its source synthesis. authority(ESSAY(x)) ≤ authority(SYNTHESIS(x)).
Internal essays are INTERNAL_SYNTHESIS, never PRIMARY_EVIDENCE for upstream layers.

## Input chain (do not skip)
```
THEME → ResearchQuestion → candidate relevant propositions → local Arguments →
ArgumentSynthesis → SynthesisAudit → EssayPlan → Essay → SentenceEvidenceAudit
```

## Output contract
```json
{
  "essay_id": "...", "question": "...", "propositions": [],
  "argument_synthesis_ref": "...", "sections": [],
  "sentence_evidence": [{"sentence": "...", "refs": ["pt:..."]}],
  "status": "MACHINE_PROPOSED"
}
```

## Hard commit gate
- every sentence carries a resolvable evidence ref (no orphan claims)
- every claim maps to the ArgumentSynthesis (no new philosophy invented in the essay)
- comparison / modern application / broader synthesis permitted ONLY here (not C1)

## Validator
SentenceEvidenceAudit: every sentence's refs resolve; no sentence asserting more than its refs license.

## Certificate
replay/gold · false-certainty (unsupported sentence) · abstention · human review of failure clusters ·
cross-work · misbinding adversarial test.
