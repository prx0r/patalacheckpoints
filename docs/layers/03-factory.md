# LAYER 03 — FACTORY (the compiler)

> **STATUS: PARTIAL — SOURCE→C1→THEME→ARGUMENT is REAL (32k source objects); SYNTHESIS/ESSAY/EDUCATION are 0 (not built)** (derived live state — see `docs_state.py`)


*Part of the `NAVIGATION.md` layer map (the master tree / spine). The compiler that turns committed sources into canonical objects.*

## 1. What it is
The autonomous corpus compiler: advances a committed SOURCE through a DAG of deterministic workers to
produce canonical scholarly objects. The "Agent 2" lane — production machinery that must never be
destabilized.

## 2. Purpose
Compile translations + scholarly objects with exact-version provenance and reproducibility. Every
object is an immutable, versioned, hash-chained record.

## 3. External tools used
Vidyut (Sanskrit linguistic engine — the deterministic tokenizer) via `pipeline/agentic_gloss.py`.
Hermes (execution kernel) via `pipeline/model.py` (agentic `hermes chat`). See `external-tools.md`.

**Translation substrate (from the `patalatranslate` review — §K):** the frontier is **proof-carrying
translation**, not a score. The `TranslationProof` object carries `source_identity · source_analysis ·
alignment · semantic_obligations [negation/modality/scope] · unverified · alternatives · checks`. Sanskrit
proof generators: Vidyut + ByT5-Sanskrit + Sanskrit Heritage. Benchmarks: **Mitrasamgraha** (391k pairs →
error families → validators), **MITRA** (1.74M cross-source S↔T↔C pairs → cross-source verification),
OTTAWA (omission/addition). Alignment: awesome-align + bertalign. MQM as the error vocabulary.
**Never a single aggregate score — redundant independent auditors + bi-directional entailment.**

## 4. Data
- **Registries:** `data/corpus/registries/<layer>-registry.jsonl` (versioned objects per layer).
- **Event ledger:** `data/corpus/registries/object-events.jsonl` (append-only, hash-chained).
- **Translation queue:** `data/corpus/downloads/translation-state-ledger.json`.

## 5. Processes

**TARGET DAG (the design):**
```
SOURCE → T1 → L0 → [ARGMAP] → L2 → L200 → C1 → THEME → ARGUMENT → SYNTHESIS → ESSAY → EDUCATION
```
The canonical DAG (`contracts/CANONICAL-DAG.yaml`) → `object_registry.PREREQS`. Scheduler ranks
eligible jobs by translation-target priority; every worker output is validated before commit.

**CURRENT LIVE STATE (derived from object_registry — NOT the target):**
```
SOURCE(32k) → T1(306) → L0(791) → ARGMAP(50) → L2(3) → L200(5) → C1(3) → THEME(1) → ARGUMENT(10)
SYNTHESIS=0 · ESSAY=0 · EDUCATION=0   ← the upper layers are DESIGN, not built
```
> This layer page's live state renders from `python3 docs/process/docs_state.py` — never hand-edit the
> counts. It is NOT the full pipeline; only SOURCE→ARGUMENT is real today.

## 6. Implementations
- `contracts/CANONICAL-DAG.yaml` — the layer graph (single source of truth).
- `pipeline/object_registry.py` — versioned registry + event ledger + `commit_batch`.
- `pipeline/factory_scheduler.py` — DAG backlog scheduler.
- `pipeline/corpus_state.py` — state machine + `next_valid_action`.
- `pipeline/translation_targets.py` — the prioritized queue.
- `pipeline/*_worker.py` — t1/l0/argmap/l2/l200/c1/theme/essay/education workers.
- `pipeline/agentic_gloss.py` — Vidyut-anchored T1 glossing.
- Tests: `test_object_events`, `test_factory_rebuild`, `test_review_engine`, `factory_certificate`.

## 7. Docs
- `docs/process/03-factory.md` — the detailed layer guide.
- `docs/FACTORY.md` — the factory reference.
- `docs/global/globalplan.md` — the dev plan (Phase 0–8).
- `endgamebuild/INFRA-INVENTORY.md` §2 — the factory inventory.
