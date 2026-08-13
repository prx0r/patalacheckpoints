# RAW-L0 HARDENING SPEC

## Live issues addressed

The Agent2 path is valuable because it provides unattended RAW Sanskrit → L0 processing. It needs tighter semantic contracts before becoming the canonical factory floor.

### Issue A — surface fallback

Current behavior can populate lemma with the token when analysis supplies no lemma.

Target:

```json
{
  "token_id":"...",
  "surface_iast":"...",
  "surface_span":{"start":0,"end":4},
  "lemma_iast":null,
  "analysis_state":"UNANALYZED",
  "analysis_witness_refs":["pt:analysis-witness:..."]
}
```

Never manufacture a lemma merely to satisfy a schema.

### Issue B — analyzer result must be evidence

```json
{
  "object_type":"AnalysisWitness",
  "analyzer":"vidyut",
  "analyzer_version":"...",
  "input":{"surface":"...","context_span_ref":"..."},
  "candidates":[
    {
      "lemma_iast":"...",
      "morphology":{},
      "native_score":null
    }
  ],
  "outcome":"SUPPORTED|AMBIGUOUS|CONFLICT|UNANALYZED|TOOL_ERROR",
  "raw_output_hash":"..."
}
```

Heritage or another analyzer produces a second witness; disagreement is data, not an error to hide.

### Issue C — tokenization ≠ Sanskrit segmentation

If RAW-L0 currently uses regex/orthographic tokenization before per-token analysis, label it accurately:
- `ORTHOGRAPHIC_TOKENIZATION`
not
- `SANDHI_SEGMENTATION`.

Introduce an explicit segmentation layer only when a real segmenter is run and evaluated.

## Passage state

Each required passage has:

```text
REGISTERED
SOURCE_VALID
L0_PARTIAL
L0_COMPLETE
SOURCE_BLOCKED
L0_FAILED
```

A work aggregates these mechanically.

```text
EMPTY
PARTIAL
COMPLETE
BLOCKED
```

### Work aggregation

```python
if all(required passage == L0_COMPLETE):
    work = COMPLETE
elif any(complete) and any(not complete):
    work = PARTIAL
elif all(blocked_or_failed):
    work = BLOCKED
else:
    work = PARTIAL
```

`committed > 0` is never sufficient for `COMPLETE`.

## Advancement

- passage `L0_COMPLETE` may feed passage-scoped downstream work;
- work `COMPLETE` may feed whole-work operations;
- work `PARTIAL` must display exact missing/blocked set;
- a downstream aggregate must include corpus coverage denominator.

## Validation ladder

Keep separate:

```text
P0 SOURCE INTEGRITY
P1 SEGMENTATION
P2 MORPHOLOGY
P3 LEXICAL/SENSE
P4 ALIGNMENT
P5 SYNTAX (only if needed)
```

A P0 pass does not imply P2/P3.

## Factory objective

Primary operational metric:
> **expert review minutes per 1,000 Sanskrit tokens at a declared quality/abstention target**

Secondary:
- source coverage;
- failure/blocked rate;
- analyzer coverage;
- false-certainty rate;
- abstention usefulness;
- morphology error on reviewed sample;
- hard-case yield;
- cost.

Do not optimize API cost while increasing scholar review burden.
