---
name: Pāṭala Autonomous Layer Auditor
version: 1.0.0
project: patala
kind: autonomous-layer-skill
layer: AUDIT
status: canonical-proposal
inherits: ../../AUTONOMY_CONTRACT.md
---

# Purpose

Apply common adversarial checks to outputs before commit and generate explicit failure classes. This is a validator interface, not a generic LLM judge.

# Checks common to every layer

- identifier/hash binding
- prerequisite/version closure
- provenance closure
- source/speaker attribution
- negation/modality/quantifier preservation
- unsupported addition
- omitted open boundary/crux
- semantic-strength inflation
- machine-as-human-review laundering
- duplicate/supersession correctness

# Translation-specific categories

`NEGATION | NUMBERS | OMISSION | UNSUPPORTED_ADDITION | TERM_DRIFT | GRAMMATICAL_UNCERTAINTY | PARALLEL_CONFLICT`

# Result

```json
{"object_id":"...","layer":"...","verdict":"PASS|REJECT|REVIEW_REQUIRED",
 "findings":[{"severity":"ERROR|WARN","class":"...","detail":"...","refs":[]}]}
```

A warning never silently becomes acceptance. An audit surfaces evidence; it does not claim scholarly correctness beyond its configured scope.
