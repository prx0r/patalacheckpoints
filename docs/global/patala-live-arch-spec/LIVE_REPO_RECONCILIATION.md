# LIVE REPOSITORY RECONCILIATION

This document records what the target architecture is being reconciled *from*. It deliberately distinguishes live-verified implementation facts from proposed target contracts.

## 1. Branch-aware source map

The repository is currently multi-branch. This audit treated the following as authoritative for the areas actually inspected:

| Area | Live source inspected | Role |
|---|---|---|
| generic corpus primitives | `main:data/corpus/primitives.ts` | legacy/shared TypeScript epistemic primitives |
| generic corpus graph | `main:data/corpus/graph.ts` | graph entities + generic annotation substrate |
| review/dependency reducer | `agent1-argument-layer-a1b:pipeline/review_engine.py` | current executable-corrections prototype |
| review vertical tests | `agent1-argument-layer-a1b:pipeline/test_review_engine.py` | executable behavioral contract |
| benchmark doctrine | `agent1-argument-layer-a1b:benchmarks/v0/MANIFEST.json` | evaluation-plane contract |
| project capability ledger | `agent1-argument-layer-a1b:machinelearning/_ACTIVE/CLAIMS.md` | anti-theatre status ledger |
| external integration map | `agent1-argument-layer-a1b:source-evidence/docs/INTEGRATION-SPEC.md` | reuse-first integration design |
| RAW-L0 builder | `agent2:pipeline/raw_l0.py` | current RAW Sanskrit → L0 implementation |
| unattended RAW-L0 | `agent2:pipeline/auto_raw_l0.py` | autonomous commit/advance path |
| corpus state machine | `agent2:pipeline/corpus_state.py` | workflow state/next-action |
| L0 validator | `agent2:pipeline/validate_l0_spec.py` | current structural gate |

**Important:** this spec does not infer that a file on one branch is merged into `main`. Cross-agent contracts below exist precisely because branch-local ownership is currently too strong.

## 2. What is already genuinely strong

### 2.1 Executable corrections

The live test gives a concrete behavioral contract:

```text
G2-TC2 v1
  │ scholar REVISE
  ▼
G2-TC2 v2 + immutable ReviewEvent
  │
  ├── G2-INF1 → NEED_REVIEW
  └── G2-CONC → NEED_REVIEW

ARG-004 → unchanged
G2-TC2 v1 → still resolvable
reducer(x) == reducer(x)
```

This is the right primitive. The final product is not “AI critiques text”; it is “review changes canonical scholarly state and every dependent result can say what changed and why.”

### 2.2 Anti-theatre claims ledger

`machinelearning/_ACTIVE/CLAIMS.md` is architecturally important, not just documentation. It explicitly separates:
- infrastructure from evidence;
- machine witness from human validation;
- model-independent review from specialist human review;
- local/source integrity from semantic correctness.

Examples in the live ledger include:
- P-001: IPVV P0 source anchoring supported, with cross-work caveat.
- P-002: benchmark supported as infrastructure, only partial as evidence.
- P-003: automatic argument reconstruction `NOT_ESTABLISHED`.
- P-004: Nyāya gate preliminary, explicitly not a semantic verifier.
- P-012: lexical ranker rejected as a witness on current gold.
- P-013: L0↔L2 alignment frozen as an adequate machine witness, not semantic validation.
- P-014: vertical serialization supported as infrastructure, not editorial validity.
- P-015: theme map supported as machine-proposed infrastructure, not adjudicated.

That discipline should become executable metadata, not remain only prose.

### 2.3 Evaluation plane separation

`benchmarks/v0/MANIFEST.json` and the claims ledger embody the correct rule:

> benchmark fixtures test machines; production objects publish scholarship.

A benchmark result must never update production authority state directly.

### 2.4 Reuse-first seam

The live integration spec already states the right replacement criterion:

> replacing any external tool later must not invalidate Pāṭala IDs or epistemic objects.

That should become an architectural test.

## 3. Semantic duplications that must be reconciled

### 3.1 Epistemic/review state

At least four distinct concerns are currently compressed into state values:

1. who/what originated an object;
2. whether software structurally checked it;
3. whether evidence supports it;
4. whether humans reviewed it;
5. whether it is publicly released/current.

A single enum cannot safely encode all five.

### 3.2 ReviewEvent duplication / ownership

The review prototype defines operational review semantics inside `pipeline/review_engine.py`, while generic corpus primitives also carry review concepts. Target:
- canonical **schema** belongs to shared kernel;
- reducer/execution belongs to pipeline;
- MCP/product calls use canonical command API;
- no agent/runtime privately defines authority semantics.

### 3.3 Generic Annotation vs typed scholarly objects

`graph.ts` has a generic annotation substrate. Keep it for truly open-ended annotations, but do not represent canonical:
- SourceAssertion
- TranslationDecision
- Proposition
- Commitment
- SemanticAlignment
- ReviewEvent
- DependencyEdge
as opaque annotation payloads.

If a field controls authority, dependency propagation, benchmark eligibility, or citation resolution, it deserves a typed object.

## 4. Live implementation risks

### R1 — authority bypass in review engine

The test correctly demonstrates that `submit_review(... actor_role="machine")` is forbidden. But the test itself uses lower-level `record_review(... actor_role="machine")` to create a review event.

**Implication:** authorization currently depends on choosing the correct method.

**Fix:** make low-level event append private/internal and require an unforgeable authorized command context. The storage layer validates the event envelope too. There must be one authority-changing command boundary.

### R2 — RAW-L0 surface fallback can masquerade as lemma

Current RAW-L0 can set:

```python
lemma_iast = lemma or token
```

That preserves a nonempty field but destroys the distinction between:
- analyzer-supported lemma;
- unchanged surface form because no lemma was obtained.

**Fix:** `surface_iast` is always present; `lemma_iast` is nullable; analyzer output is an `AnalysisWitness`. `PARSED` cannot be inferred from string non-emptiness.

### R3 — work-level VERIFIED after partial passage success

The unattended RAW-L0 runner can promote the work after `committed > 0`, even when other passages are blocked.

**Fix:** compute work completeness from per-passage states:

```text
COMPLETE   = every required passage committed and structurally valid
PARTIAL    = >=1 committed and >=1 unresolved/blocked
BLOCKED    = no progress possible under current source contract
EMPTY      = no committed passages
```

Only `COMPLETE` may trigger full-work advancement. `PARTIAL` may allow downstream *passage-scoped* work, never imply whole-work completion.

### R4 — overloaded VERIFIED

“source bytes/spans are lossless” is not “morphology correct” is not “translation reviewed” is not “scholarship verified”.

**Fix:** remove authority meaning from workflow labels. Use explicit validation/review axes.

### R5 — prototype review reducer lacks production authority machinery

Before production:
- persistent append-only event store;
- actor identity;
- reviewer credentials and scope;
- reviewer independence;
- version existence and hash binding;
- unique event IDs;
- optimistic concurrency;
- deterministic reducer version;
- reducer input snapshot/hash;
- impact report lineage;
- idempotent command handling;
- supersession semantics;
- audit export.

### R6 — branch-local schema ownership

Agent branches should produce implementations/proposals, not become the permanent namespace of canonical scholarly contracts.

**Fix:** introduce shared kernel schemas first; migrate agents through adapters; merge only once exact compatibility tests pass.

## 5. What not to “fix” by centralizing

Do not centralize everything. The target is **small canonical core + replaceable adapters**, not one giant package.

Keep external/generic concerns replaceable:
- GROBID/Docling extraction;
- Vidyut/Heritage analysis;
- PaperQA2/Tantivy retrieval;
- INCEpTION annotation/adjudication UI;
- OpenReview-like workflow;
- Inspect benchmark runtime;
- Zotero bibliography CRUD;
- Crossref/OpenAlex metadata;
- ORCID/ROR;
- CTS/DTS, IIIF, TEI, JATS, RO-Crate interoperability;
- Hermes/other agent runtimes.

Pāṭala centralizes only semantics that cannot change without changing the scholarly meaning of the graph.
