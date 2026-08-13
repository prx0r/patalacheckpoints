# TRANSLATION AUDIT — FIRST SCHOLAR PRODUCT API

## Product contract

Input:
- Sanskrit source/witness/passage or resolvable Pāṭala passage ref;
- a translation;
- optional alignment/translation-decision data.

Output:
1. what is **mechanically demonstrable**;
2. what is **machine-proposed for review**;
3. what has been **calibrated against reviewed gold**.

The UI and API must never collapse these classes.

## 1. Audit run

`POST /v1/audits`

```json
{
  "source_ref":{"object_id":"pt:passage:...","version_id":"..."},
  "translation":{
    "text":"...",
    "language":"en",
    "external_id":null
  },
  "requested_detectors":["*"],
  "mode":"DETERMINISTIC_ONLY|PROPOSED|CALIBRATED"
}
```

Returns immutable run ID and source/input hashes.

## 2. AuditFinding

```json
{
  "finding_id":"pt:audit-finding:...",
  "audit_run_ref":"...",
  "class":"DETERMINISTIC|MODEL_PROPOSED|CALIBRATED",
  "type":"OMISSION|UNSUPPORTED_ADDITION|POLARITY_NEGATION|MODALITY|AGENCY|SYNTACTIC_ATTACHMENT|COMPOUND_PARSE|TECHNICAL_TERM_SENSE|SPEAKER_ATTRIBUTION|PURVAPAKSA_SIDDHANTA|SCOPE|CONCEPTUAL_DISTINCTION|RIVAL_READING_IGNORED|UNSAFE_CERTAINTY|PROVENANCE",
  "severity":"INFO|LOW|MEDIUM|HIGH|CRITICAL",
  "source_spans":[{"ref":"..."}],
  "target_spans":[{"start":0,"end":12}],
  "claim":{
    "text":"...",
    "modality":"DEMONSTRATED|POSSIBLE|CALIBRATED_RISK"
  },
  "evidence_refs":[],
  "detector":{
    "id":"...",
    "version":"...",
    "code_ref":"...",
    "model_ref":null
  },
  "calibration":null,
  "review_projection":{
    "status":"UNREVIEWED"
  }
}
```

For `CALIBRATED`, calibration must name dataset/split/metric/version, not just a confidence score.

## 3. Finding actions

Product actions:
```text
ACCEPT_FINDING
REJECT_FINDING
REVISE_FINDING
MARK_OPEN
ADD_RIVAL_READING
```

They are **not** themselves canonical scholarly decisions.

Mapping:
- product sends a `ReviewCommand`;
- canonical review engine appends `ReviewEvent`;
- product reads updated projection.

This prevents Audit from inventing a parallel review system.

## 4. v0 detector set

Start with observable/deterministic properties:

- source ref resolves;
- source hash/version pinned;
- Sanskrit coverage accounting;
- target coverage/alignment bookkeeping;
- missing aligned source segment candidates;
- target material with no aligned source candidate;
- terminology consistency across same declared sense;
- explicit negation/polarity token mismatch candidate where mechanically licensed;
- provenance/lineage completeness;
- duplicate/malformed spans;
- unresolved references.

Do not advertise “translation correctness”.

## 5. v1 model-proposed set

Only after v0 workflow is real:
- technical term sense;
- syntactic attachment;
- scope/modality;
- speaker/commitment attribution;
- rival compound parse;
- rival reading;
- pūrvapakṣa/siddhānta attribution.

Every finding says “model-proposed”, cites evidence, and allows abstention.

## 6. v2 calibrated

Calibrate detector by detector.

Required metrics depend on detector, but generally:
- precision/recall by error class;
- false-certainty rate;
- abstention coverage/risk;
- calibration error where probabilistic;
- reviewer acceptance/rejection;
- expert review minutes saved;
- subgroup by text/tradition/period/genre.

A high aggregate score cannot hide a catastrophic polarity or attribution failure.

## 7. Views

One product, multiple modes:

```text
Overview
Sanskrit ↔ Translation
Findings
Terms
Grammar / Analysis Witnesses
Rival Readings
Provenance
Review History
Impact
```

Compare, Term Audit, and Attack This Reading are modes over the same canonical objects, not separate data models.

## 8. Export

Export a proof/audit bundle containing:
- input refs/hashes;
- findings;
- detector lineage;
- review history;
- unresolved/open findings;
- versions;
- RO-Crate or equivalent packaging adapter later.

The bundle demonstrates inspectability, not truth.
