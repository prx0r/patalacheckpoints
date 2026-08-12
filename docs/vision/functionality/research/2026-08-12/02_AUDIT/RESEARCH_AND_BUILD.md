# Project 02 — Pāṭala Audit

## Job to be done
“I translated this Sanskrit. Show me what is mechanically wrong, what is possibly wrong, and what has actually been calibrated against expert judgment.”

Three classes must remain distinct:
1. deterministic;
2. model-proposed (`MACHINE_PROPOSED`);
3. calibrated against held-out expert gold.

## Existing product signals

Paperpal manuscript checker:
https://paperpal.com/manuscript-check

Lesson: upload/check/fix is a clear academic workflow; users understand a battery of concrete checks better than an opaque score. Pāṭala differs by grounding findings into the historical-language source.

Elicit:
https://elicit.com/

Lesson: “reproducible, traceable, auditable” AI research and API/MCP access are now product expectations. Pāṭala should be domain-deep rather than broad paper search.

ResearchRabbit:
https://www.researchrabbit.ai/

Lesson: risk/trust signals should be integrated into a scholar’s existing exploration rather than hidden in separate reports.

## Core technical precedent: xCOMET

Repo:
https://github.com/Unbabel/COMET

Paper:
https://arxiv.org/abs/2310.10482
https://aclanthology.org/2024.tacl-1.54/

xCOMET demonstrates the right output shape:
`translation → error spans → severity → aggregate quality`.

Pāṭala adaptation:
`translation → Sanskrit/English spans → typed concern → severity → exact evidence → review state`.

Use xCOMET as a generic baseline/witness, not authority.

Other baselines:
https://github.com/google-research/metricx
https://github.com/google-research/mt-metrics-eval
https://aclanthology.org/2025.wmt-1.70/
https://arxiv.org/abs/2509.13980
https://arxiv.org/abs/2605.24904

2026 systematic review of automatic human translation evaluation:
https://www.sciencedirect.com/science/article/pii/S2772766126000066

Its warning that expert benchmark construction/explainability are often underdeveloped reinforces Pāṭala’s expert-gold + evidence-native design.

## Product modes

### Translation Audit
Outputs:
- source integrity;
- alignment;
- omission/addition;
- polarity/modality/agency;
- terminology;
- grammar/parse;
- attribution/scope;
- rival readings;
- provenance;
- unresolved/abstention.

### Compare Readings
Architecturally: two or more TranslationAudit objects + semantic diff.
Show:
- agreement;
- substantive divergence;
- asymmetric omission/addition;
- term-policy differences;
- scope differences;
- interpretive consequences;
- source support.

### Term Audit
Architecturally: aligned occurrences + TermSense evidence + translation decisions + consistency rules.
Show:
- every occurrence;
- local morphology/parse;
- renderings;
- candidate senses;
- drift;
- justified exceptions;
- unresolved cases.

## AuditFinding
Store:
- finding ID;
- detector class (`DETERMINISTIC`, `MODEL_PROPOSED`, `CALIBRATED`);
- type;
- severity;
- exact source/target spans;
- evidence refs;
- detector/version;
- review state;
- calibration stats where available.

A calibrated finding should link to suite/task/version and held-out precision/recall—not a generic “AI confidence.”

## Audit versions

### v0 deterministic
Build immediately:
- source normalization;
- span resolution;
- source coverage;
- alignment bookkeeping;
- omission candidates;
- addition candidates;
- terminology consistency;
- citation/provenance completeness.

### v1 proposed scholarly flags
Add:
- likely wrong lemma/sense;
- likely attachment;
- polarity/scope risk;
- attribution risk;
- rival parse;
- technical-term mismatch.

All visibly remain MACHINE_PROPOSED.

### v2 calibrated
Promote detector-by-detector after:
- expert fixtures;
- held-out evaluation;
- error analysis;
- false-positive measurement;
- version freeze.

## UI
Prefer a three-pane interaction:
`SANSKRIT | TRANSLATION | FINDINGS`

Tabs:
Overview / Alignment / Terms / Grammar / Rival Readings / Provenance.

High-value action: **Attack this reading**—but output is model-proposed until reviewed.

## Data flywheel
Every scholar response becomes a typed ReviewEvent:
- ACCEPT_FINDING
- REJECT_FINDING
- REVISE_FINDING
- MARK_OPEN
- ADD_RIVAL

This is how Audit manufactures benchmark candidates.

## Detector build order
1. span/coverage;
2. omission;
3. addition;
4. term consistency;
5. negation/polarity;
6. number/person/agency;
7. morphology;
8. compound/attachment;
9. speaker attribution;
10. scope;
11. technical sense;
12. rival reading.

Order from observable to interpretive.
