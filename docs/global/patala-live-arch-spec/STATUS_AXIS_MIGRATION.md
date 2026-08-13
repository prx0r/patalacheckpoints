# STATUS AXIS MIGRATION

## Problem

Current files use state words for different questions:
- source/workflow completion;
- machine proposal;
- human checking;
- expert review;
- editorial acceptance;
- benchmark gold;
- derived dependency state.

A single `EpistemicState` cannot answer all of them without laundering one kind of assurance into another.

## Target: orthogonal axes

```json
{
  "origin": {
    "kind": "MACHINE|HUMAN|INSTITUTION",
    "actor_ref": "..."
  },
  "structural_validation": [
    {
      "kind": "SCHEMA|SOURCE_INTEGRITY|SPAN_RESOLUTION|HASH",
      "status": "PASS|FAIL|NOT_RUN|PARTIAL",
      "validator": "...",
      "validator_version": "...",
      "run_ref": "..."
    }
  ],
  "evidence_status": "UNSUPPORTED|SUPPORTED|CONFLICT|UNDERDETERMINED",
  "review_status": "UNREVIEWED|SINGLE_REVIEWED|DOUBLE_REVIEWED|ADJUDICATED|SPECIALIST_REVIEWED",
  "publication_status": "DRAFT|RELEASED|SUPERSEDED|WITHDRAWN"
}
```

`DerivedState` remains separate:
```text
CURRENT
NEED_REVIEW
SUPERSEDED
REJECTED
BLOCKED
```
because it is a reducer output, not an authority claim.

## Legacy mapping rules

Mappings are conservative. An adapter may map a legacy value only to the assurance actually established.

| Legacy term | Safe target mapping | Forbidden inference |
|---|---|---|
| `machine_proposed` | origin=MACHINE; review=UNREVIEWED | supported/reviewed |
| `human_proposed` | origin=HUMAN; review=UNREVIEWED | expert reviewed |
| `checked` | structural validation only if exact checker lineage known; otherwise legacy note | human/expert review |
| `expert_reviewed` | review=SPECIALIST_REVIEWED only if reviewer identity/scope resolvable | truth |
| `editorially_accepted` | publication/review policy event + reviewer lineage | truth |
| `CANDIDATE` benchmark | benchmark gold-state only | production authority |
| `SINGLE_EDITOR_GOLD` | benchmark review=SINGLE_REVIEWED | production scholarly review |
| `DOUBLE_REVIEWED_GOLD` | benchmark review=DOUBLE_REVIEWED | consensus/truth |
| `ADJUDICATED_GOLD` | benchmark review=ADJUDICATED | universal truth |
| RAW-L0 `VERIFIED` | inspect historical run; map source-integrity only where proven | morphology/translation correctness |
| `NEED_REVIEW` | DerivedState only | evidence unsupported |
| `REJECTED` | DerivedState resulting from review | deletion |

## Migration mechanism

Do not rewrite stored historical objects in-place.

1. Introduce `AuthorityEnvelopeV2`.
2. Add `legacy_state` to migration projection.
3. Implement deterministic adapters from each current module.
4. Store adapter version.
5. Emit “ambiguous legacy state” where semantics cannot be recovered.
6. New writes use V2 only.
7. Reads expose V2 + original legacy value during transition.
8. Remove legacy write paths after compatibility tests and one frozen release.
