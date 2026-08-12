---
name: Pāṭala Education Projection Producer
version: 1.0.0
project: patala
kind: autonomous-layer-skill
layer: EDUCATION
status: canonical-proposal
inherits: ../../AUTONOMY_CONTRACT.md
---

# Purpose

Project reviewed/qualified scholarly objects into lessons, explainers, quizzes, visualizations. Education
comes AFTER the scholarly object; it is a derived rendering, not a source of claims.

## Authority boundary
authority(Education(x)) ≤ authority(x). A lesson may simplify for teaching but must never assert more
than its source object licenses. Never derive a lesson directly from the source text.

## Input chain
```
reviewed/qualified claims → lesson plan → explanation → quiz → visualization
```

## Output contract
```json
{"lesson_id": "...", "source_object_refs": [], "audience": "...", "plan": [], "quizzes": [], "status": "MACHINE_PROPOSED"}
```

## Hard commit gate
- every claim traces to a reviewed/qualified source object (status ≥ ENGINEERING_VALIDATED)
- no claim exceeds the source object's authority
- source_object_refs resolve

## Validator
Authority-fidelity: each lesson claim maps to a source claim with equal-or-higher authority; no new claims.

## Certificate
replay/gold · false-certainty · abstention · human review of failure clusters · cross-work.
