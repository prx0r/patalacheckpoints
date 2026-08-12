# Project 03 — Pāṭala Review

## Product
Pāṭala Review is the scholar-facing surface for the research compiler:

`scholarship → claims → sources → dependencies → counterevidence → scope/attribution checks → cruxes → evidence-backed diagnostics`.

The compiler is the engine; Review is the product.

## Market references
Paperpal:
https://paperpal.com/manuscript-check

Elicit:
https://elicit.com/

These prove preflight/research-check workflows. Pāṭala should differentiate through primary-source grounding, historical interpretation and explicit dependency graphs.

## Review workflow infrastructure

OpenReview docs:
https://docs.openreview.net/

Python client:
https://github.com/openreview/openreview-py

Web:
https://github.com/openreview/openreview-web

Reuse concepts for submissions/reviews/assignments/identity/decisions where needed. Do not rebuild conference management. Pāṭala’s unique layer is executable correction + dependency impact.

## Critical research precedents

### CLAIMCHECK
https://aclanthology.org/2025.findings-emnlp.1185/

It links review weaknesses to the claims they dispute and labels validity/objectivity/type. This is a direct precedent for testing whether Pāṭala critiques are grounded.

Adapt:
`critique → target proposition → evidence → critique type → reviewer validity judgment`.

### CLAIM-BENCH
https://arxiv.org/abs/2506.08235
https://aclanthology.org/2025.ijcnlp-long.127/

It shows staged/multi-pass claim↔evidence reasoning can outperform monolithic prompting, at greater cost.

Pāṭala Review should therefore compile in passes:
1. extract claims;
2. resolve evidence;
3. reconstruct dependencies;
4. generate challenges;
5. verify each challenge is grounded.

### AI as scientific quality checker
https://arxiv.org/abs/2505.23824

Strong framing for Pāṭala: quality checker, not fake authoritative peer reviewer.

### 2026 peer-review survey
https://arxiv.org/abs/2606.25057

Risks to build around:
- reliability;
- disagreement;
- domain transfer;
- prompt injection;
- retrieval vulnerabilities;
- reward hacking.

Treat uploaded papers as untrusted data.

### PeerArg
https://arxiv.org/abs/2409.16813

Supports Pāṭala’s decision to combine LLM extraction with explicit argument structures rather than end-to-end black-box reviewing.

## Argument interoperability

AIF datasets:
https://github.com/arg-tech/aif-arg-datasets

oAMF:
https://github.com/arg-tech/oAMF

Inter-document scientific argument web:
https://doi.org/10.4230/TGDK.3.3.4

Use xAIF/oAMF as import/export/evaluation adapters. Keep Pāṭala’s canonical Philosophy IR because it adds Commitment, DebateFrame, SemanticAlignment, derivational propositions and cruxes that matter historically.

## Output should look like compiler diagnostics

Examples:
- ERROR: cited quote is not present in resolved passage.
- WARNING: claim attributes an opponent’s objection to the author.
- WARNING: conclusion depends on an OPEN reading.
- INFO: rival reading preserves source but changes proposition scope.
- CRUX: removing disputed premise P collapses the only support chain to conclusion C.

Do not make “72/100 paper quality” the canonical output.

## Review pipeline

R0 ingest: preserve page/line/span coordinates.
R1 claims: extract claims/citations.
R2 grounding: resolve citations/quotes/source passages.
R3 argument: reconstruct propositions/inferences/commitments with abstention.
R4 attack: retrieve counterevidence/rival readings/scope conflicts.
R5 dependency: trace load-bearing readings/evidence.
R6 crux: counterfactual removal/recomputation.
R7 critique validator: every warning must name exact target + evidence + epistemic class.

## Security
Because documents may contain hostile or accidental instructions:
- document content is data, never system instruction;
- quarantine hidden/meta text;
- allowlist tools;
- preserve source text for audit;
- flag prompt-like embedded text;
- no document may grant itself permissions.

## Build sequence
Review v0: one native Pāṭala Argument object.
Review v1: short essay generated from Pāṭala objects.
Review v2: external thesis/paper section whose citations resolve into Pāṭala.
Only later attempt generic humanities PDFs.

This sequence lets correctness be measured before generalization.
