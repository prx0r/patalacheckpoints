# DEPRECATIONS, DUPLICATES, AND OWNERSHIP DECISIONS

| Current concern | Current location(s) | Decision |
|---|---|---|
| generic epistemic state | `data/corpus/primitives.ts`, `data/corpus/graph.ts` | deprecate as authority-bearing canonical enum; adapter to orthogonal axes |
| ReviewEvent schema | generic corpus concepts + Agent1 `pipeline/review_engine.py` | shared kernel owns schema; pipeline owns execution/reducer |
| generic Annotation payload | `data/corpus/graph.ts` | keep only for non-core/open-ended annotation; no core epistemic semantics in opaque payload |
| benchmark review status | `benchmarks/v0` | keep benchmark-local; do not merge with production review state |
| RAW-L0 VERIFIED | Agent2 corpus state/runner | replace with structural-validation + passage/work completeness |
| lemma fallback | Agent2 `raw_l0.py` | remove for new writes; nullable lemma + AnalysisWitness |
| work advancement on any commit | Agent2 `auto_raw_l0.py` | replace with passage aggregation |
| machine proposal | multiple layers | one ProposalEnvelope; authority NONE |
| DerivedState writes | review engine/runtime | reducer-only; agents/products cannot author |
| external standard schemas | source-evidence adapters | adapters only; never canonical owner |
| product finding review | future Audit | commands into canonical ReviewEvent, no parallel review table semantics |
| Argument interchange | xAIF/oAMF adapters | native IR remains canonical |
| scholar workflow | OpenReview/INCEpTION/Hypothesis integrations | reuse UX/workflow; canonical actions remain Pāṭala |

## Canonical owner test

A concept belongs in Pāṭala core iff changing/removing it would alter the meaning of scholarly state even after every external tool were swapped.

Examples:
- `ReviewEvent`: yes.
- `Commitment`: yes.
- `SemanticAlignment`: yes.
- `Inspect EvalLog`: no; linked external/run object.
- GROBID TEI node: no; extraction witness payload.
- Zotero item key: no; crosswalk.
- Hermes session ID: no; lineage metadata.
