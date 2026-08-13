# BENCHMARK + INSPECT ADAPTER SPEC

## Architectural rule

The benchmark plane is downstream of frozen/reviewed data and upstream of model development.

```text
PRODUCTION SCHOLARLY GRAPH
     │ one-way snapshot/export
     ▼
BENCHMARK CANDIDATE
     │ independent review/adjudication
     ▼
FROZEN BENCHMARK FIXTURE
     │
     ▼
INSPECT TASK/RUN
     │
     ▼
METRICS / FAILURE CASES
```

There is **no arrow from an Inspect score directly into production authority**.

## 1. Preserve current benchmark gold ladder

The existing benchmark review vocabulary is valid *inside evaluation*:
- CANDIDATE
- SINGLE_EDITOR_GOLD
- DOUBLE_REVIEWED_GOLD
- ADJUDICATED_GOLD

Do not merge it with production `review_status`.

## 2. Fixture contract

```json
{
  "fixture_id":"PAT-T2-...",
  "fixture_version":"1",
  "family":"T1_SOURCE|T2_TRANSLATION|T3_INTERPRETATION|T4_ARGUMENT",
  "task":"...",
  "input_snapshot":{},
  "source_refs":[{"object_id":"...","version_id":"..."}],
  "expected":{},
  "acceptable_alternatives":[],
  "forbidden_inferences":[],
  "abstention_expected":false,
  "error_taxonomy":[],
  "gold_state":"CANDIDATE",
  "review_event_refs":[],
  "provenance":{},
  "freeze_hash":"..."
}
```

## 3. Error taxonomy

Keep the high-value taxonomy:

```text
OMISSION
UNSUPPORTED_ADDITION
POLARITY_NEGATION
MODALITY
AGENCY
SYNTACTIC_ATTACHMENT
COMPOUND_PARSE
TECHNICAL_TERM_SENSE
SPEAKER_ATTRIBUTION
PURVAPAKSA_SIDDHANTA
SCOPE
CONCEPTUAL_DISTINCTION
RIVAL_READING_IGNORED
UNSAFE_CERTAINTY
```

## 4. Inspect adapter boundary

Pāṭala owns:
- fixtures;
- task definitions;
- domain scorers;
- scanners;
- split policy;
- gold review metadata;
- run registry link.

Inspect owns:
- eval execution;
- model adapter orchestration;
- log/runtime mechanics.

Persist mapping:

```json
{
  "benchmark_run_id":"pt:benchmark-run:...",
  "suite_version":"...",
  "fixture_snapshot_hash":"...",
  "inspect_eval_log_ref":"...",
  "model_ref":"...",
  "scorer_versions":{},
  "scanner_versions":{},
  "started_at":"...",
  "completed_at":"...",
  "environment":{}
}
```

## 5. Required scanners

- benchmark leakage;
- gold phrase copying;
- unsupported addition;
- attribution laundering;
- citation laundering;
- scope strengthening;
- false corroboration;
- unsafe certainty.

## 6. Dataset policy

At maturity:
- public development set;
- reproducible public test slice;
- private locked evaluation;
- fresh continuously produced cases.

Hard cases are more valuable than thousands of trivial examples.

## 7. Audit flywheel

A reviewed Audit finding may yield a benchmark candidate only if:
- exact source/input versions pinned;
- before/after decision preserved;
- reviewer identity policy satisfied;
- no private/confidential data leakage;
- fixture task is independently defined;
- benchmark exporter records derivation.

A product acceptance click alone is not gold.
