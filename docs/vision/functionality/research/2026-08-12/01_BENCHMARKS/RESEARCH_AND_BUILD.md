# Project 01 — Pāṭala Benchmarks

## Positioning
Do not build “another Sanskrit MT benchmark.” Build the measurement layer for difficult premodern Sanskrit scholarship.

One family should mirror the evidence graph:
- T1 SOURCE: segmentation, morphology, syntax, alignment.
- T2 TRANSLATION: omission, unsupported addition, polarity, modality, agency, terminology.
- T3 INTERPRETATION: speaker attribution, scope, rival reading, conceptual distinction, abstention.
- T4 ARGUMENT: proposition, commitment, inference, support/attack, semantic alignment, crux.

## External benchmarks/datasets

Mitrasamgraha:
https://arxiv.org/abs/2601.07314

IndicGenBench:
https://aclanthology.org/2024.acl-long.595/
https://github.com/google-research-datasets/indic-gen-bench

SanskritShala:
https://arxiv.org/abs/2302.09527

MITRA:
https://arxiv.org/abs/2601.06400

These provide external baselines and task/data patterns. Pāṭala differentiates through expert philosophical adjudication, fine-grained errors, provenance, attribution/scope/argument tasks and private locked cases.

## Eval infrastructure

### Inspect AI — recommended primary runner
https://github.com/UKGovernmentBEIS/inspect_ai
https://inspect.aisi.org.uk/
https://github.com/UKGovernmentBEIS/inspect_evals

Why: model-neutral, composable datasets/tools/scorers, agent/tool evals, logs, parallel execution, mature view tooling.

Recommendation: keep Pāṭala `BenchmarkFixture/BenchmarkRun` canonical and write an Inspect adapter. Do not move Pāṭala epistemic state into the eval framework.

Other useful harnesses:
https://github.com/openai/evals
https://github.com/EleutherAI/lm-evaluation-harness

## Translation metric baselines

COMET/xCOMET:
https://github.com/Unbabel/COMET
https://arxiv.org/abs/2310.10482
https://aclanthology.org/2024.tacl-1.54/

MetricX:
https://github.com/google-research/metricx

MT Metrics Eval:
https://github.com/google-research/mt-metrics-eval

xCOMET's valuable design is span-level error detection + severity rather than only one score. Copy the shape; do not assume its pretrained metric is reliable on philosophical Sanskrit. `mt-metrics-eval` is especially useful for correlations, significance tests and MQM-style human-rating handling.

## Pāṭala error taxonomy
Use MQM-inspired severity but Sanskrit-specific categories:
- OMISSION
- UNSUPPORTED_ADDITION
- POLARITY_NEGATION
- MODALITY
- AGENCY
- SYNTACTIC_ATTACHMENT
- COMPOUND_PARSE
- TECHNICAL_TERM_SENSE
- SPEAKER_ATTRIBUTION
- PURVAPAKSA_SIDDHANTA
- SCOPE
- CONCEPTUAL_DISTINCTION
- RIVAL_READING_IGNORED
- UNSAFE_CERTAINTY

Each annotation stores exact source/target spans, severity, evidence refs, reviewer and review state.

## Argument/review benchmark precedents

CLAIM-BENCH:
https://arxiv.org/abs/2506.08235
https://aclanthology.org/2025.ijcnlp-long.127/

CLAIMCHECK:
https://aclanthology.org/2025.findings-emnlp.1185/

CLAIM-BENCH shows value from staged/multi-pass claim↔evidence reasoning. CLAIMCHECK evaluates whether critiques actually target paper claims and whether weaknesses are valid/objective. Both map well to Pāṭala T4 and Review.

## Contamination strategy
Private benchmarking:
https://arxiv.org/abs/2403.00393

Publishing benchmarks without fully giving answers:
https://arxiv.org/abs/2505.18102

Contamination-resistant benchmark argument:
https://arxiv.org/abs/2605.19999

Mitigation assessment:
https://arxiv.org/abs/2503.16402

Recommended split:
- PUBLIC DEV: schema, examples, development fixtures.
- PUBLIC EVAL: reproducibility subset, rotatable.
- PRIVATE LOCKED: scholar-reviewed official evaluation.
- FRESH: newly adjudicated cases continuously added.

## Scoring
Primary output is a profile, not a mystical scalar:
SOURCE / MORPHOLOGY / TRANSLATION / POLARITY / TERMINOLOGY / ATTRIBUTION / RIVAL READING / ARGUMENT / ABSTENTION.

A leaderboard aggregate can exist for ordering but must not erase dimensions.

## Run metadata
Every run freezes:
- Pāṭala git SHA;
- exact model/provider;
- prompt/agent version;
- tools allowed;
- fixture/rubric version;
- split;
- cost/latency;
- raw predictions;
- scorer version.

## Immediate build
1. freeze initial T1/T2 fixture schema;
2. implement Inspect adapter;
3. export current deterministic P0/P4 checks as scorers;
4. create Sanskrit-only IPVV RAW-L0 task;
5. add expert-reviewed T2 error-span fixtures;
6. keep first private locked split from day one.
