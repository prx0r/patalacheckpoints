# FIRST GOLD VERTICAL — EXISTING ARG-002 REVIEW LOOP → AUDIT/BENCHMARK LOOP

This vertical deliberately begins from an existing live behavioral fixture rather than inventing a new Sanskrit example.

## Existing kernel fixture

The live review test uses:
- argument context `ARG-002`;
- proposition `G2-TC2`;
- versions v1 → v2;
- dependent inference `G2-INF1`;
- dependent conclusion `G2-CONC`;
- unrelated `ARG-004`.

Current expected behavior:
- v1 remains;
- review event resolves;
- v2 exists;
- inference and conclusion become `NEED_REVIEW`;
- impact report names exact affected objects;
- unrelated argument stays unchanged;
- reducer is idempotent.

## Extend it into the first whole-system vertical

### Step 1 — source/translation input
Choose one existing IPVV passage whose refs are already exact and whose translation relation is available. Do **not** manufacture a new passage for the demo.

### Step 2 — deterministic AuditFinding
Generate a finding whose class is mechanically testable, e.g. an exact source/target/provenance/alignment issue.

Required:
- exact source span;
- target span;
- run hash;
- detector/version;
- no truth language.

### Step 3 — review
A scholar opens the finding and chooses `REVISE_FINDING`.

The UI emits a `ReviewCommand`, not a direct database mutation.

### Step 4 — canonical mutation
The canonical service:
- validates actor/scope;
- pins reviewed version;
- appends ReviewEvent;
- creates/pins replacement version;
- runs reducer.

### Step 5 — impact
Verify:
- expected dependent object(s) become NEED_REVIEW;
- unrelated objects remain unchanged;
- old version and review event resolve;
- impact has cause chain.

### Step 6 — benchmark candidate exporter
A one-way exporter sees:
- reviewed before/after object;
- exact source;
- finding class;
- reviewer metadata;
and creates a `CANDIDATE` fixture in evaluation plane.

It does not mark it gold.

### Step 7 — independent review
A second reviewer/adjudicator upgrades the benchmark fixture according to benchmark policy. This is benchmark authority only.

### Step 8 — Inspect execution
Future Audit/model version runs blind on frozen fixture.

### Step 9 — development feedback
Benchmark results may change:
- detector code;
- prompt;
- model selection;
- abstention threshold.

They may not change production scholarly state.

## Acceptance criteria

### Identity
- every ref resolves;
- every review target pins exact version;
- historical v1 remains resolvable.

### Authority
- machine cannot submit canonical scholarly review;
- low-level append cannot bypass authorization;
- product action is not itself review authority.

### Dependency
- exact affected set reproducible;
- unrelated object unchanged;
- reducer idempotent;
- reducer/version lineage present.

### Evaluation
- benchmark fixture content frozen;
- fixture points to exact source versions;
- benchmark gold state distinct from production review state;
- run can reproduce scorer/scanner versions.

### Product honesty
- AuditFinding class visibly retained;
- unresolved uncertainty remains visible;
- no “verified/correct/proved” label derives from schema pass or model score.

## Why this is the first vertical

It closes all four loops simultaneously:
1. source/data;
2. scholar utility;
3. executable correction;
4. benchmark/data flywheel.

A prettier reader or larger corpus would not test the core moat this directly.
