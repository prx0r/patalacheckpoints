# 03 — FACTORY (the compiler / CI system)

*Part of `docs/process/README.md`. The factory is Pāṭala's **compiler** — it turns committed sources
into canonical scholarly objects (translations, arguments, synthesis) through a DAG of deterministic
workers. It is the "Agent 2" lane: the production machine that must never be destabilized.*

## 1. What the factory IS

The autonomous corpus compiler. Given a committed `SOURCE` object, it advances it through the layers,
committing each as an immutable, versioned object with a hash-chain event record.

```
SOURCE → T1 → L0 → [ARGMAP] → L2 → L200 → C1 → THEME → ARGUMENT → SYNTHESIS → ESSAY → EDUCATION
```

## 2. The canonical DAG (single source of truth)

`contracts/CANONICAL-DAG.yaml` declares layer→`requires[]`. It is compiled into
`object_registry.PREREQS`. **Every consumer (scheduler, rebuild engine, certificate, tests) MUST
derive from `PREREQS`, never hardcode the DAG.**

Key scholarly facts encoded:
- `T1` ← SOURCE (word-gloss)
- `L0` ← T1 (structured tokens)
- `ARGMAP` ← SOURCE + L0 (lateral guide)
- `L2` ← L0 + ARGMAP (readable prose)
- `L200` ← L2 (proof-carrying: MT/IA decisions)
- `C1` ← L200 (passage interpretation)
- `THEME`/`ARGUMENT` ← C1; `SYNTHESIS` ← ARGUMENT + THEME; `ESSAY` ← SYNTHESIS; `EDUCATION` ← ESSAY

## 3. The registry + event ledger (the crown jewel)

`pipeline/object_registry.py`:
- **Versioned JSONL registry** per layer (`data/corpus/registries/<layer>-registry.jsonl`). A fix emits a NEW version (`<layer>-<id>-v{n}`), never edits in place; `supersedes` chains; old versions stay citable.
- **Dedup** by `input_hash` + committed status.
- **Atomic + concurrency-safe:** single-writer `fcntl` lock + temp-write + `fsync` + atomic `os.replace`.
- **Append-only hash-chained ObjectEvent ledger** (`object-events.jsonl`): `append_event()` chains `prev_hash → event_hash`; `verify_event_chain()` re-derives it.

Reusable entry points: `commit()`, `commit_batch()`, `current()`, `versions()`, `is_committed()`,
`set_status()`, `supersede()`, `append_event()`, `verify_event_chain()`.

## 4. The state machine + queue + scheduler

| Concern | Module | Reusable entry point |
|---|---|---|
| Next valid action | `pipeline/corpus_state.py` | `next_valid_action()`, `detect_source_format()`, `discover_works()` |
| Translation queue | `pipeline/translation_targets.py` | `TARGETS`, `order_queue()`, `all_targets()` |
| Work queue consumer | `pipeline/agent3_queue.py` | `eligible_works()`, `process_next()` |
| Backlog scheduler | `pipeline/factory_scheduler.py` | `scheduler_pass()`, `queue_preview()` |
| Certificates | `pipeline/factory_certificate.py` | integrity + resume (PASS = clean) |
| Rebuild/impact | `pipeline/factory_rebuild.py` | dependency invalidation (A2-18) |

## 5. How a work enters the factory

```
sources/<wid>/<wid>.txt  (on disk)  →  corpus_state.discover_works (auto-registers)
   →  translation-state-ledger.json  →  agent3_queue.eligible_works
   →  factory_scheduler  →  worker produces layer  →  object_registry.commit
```
`register_sources.py` / `import_sanskritree.py` / `acquire_sivaqueue*.py` all commit `SOURCE` objects
so the scheduler picks the work up. The live loop is `bash pipeline/start_overnight.sh status`.

## 6. Workers (real generators + deterministic validators)

`t1_worker`, `l0_worker`, `argument_map_worker`, `l1_l2_worker`, `l200_worker`, `c1_worker`,
`theme_worker`, `essay_worker`, `education_worker` — all in `pipeline/`.

## 7. Known gaps (so nobody rediscovers them)

- **ARGUMENT / SYNTHESIS have NO real worker** — they're in `LAYERS` but unwired (DAG ends at C1; `autonomy` falls back to a stub).
- **THEME/ESSAY/EDUCATION not reachable via the live `factory_loop.sh`** (runs only T1..C1). Workers exist but nothing triggers them.
- **Live-registry integrity debt:** `factory_certificate` reports 789 bad hashes, 119 conflicts, 19 duplicates (live-data debt, not a cert-logic bug).
- **L1/L1L2 duplication:** two competing L1/L2 providers (`l1_l2_worker.py` vs `l1_l2_translate.py`); bare L1 legacy side-path not in the DAG.
- **Factory intake state fragmented:** 4 sivaqueue manifests at different completion, 3 sources of truth for "on disk" (audit §5.6).

## 8. Tests

```bash
python3 pipeline/test_object_events.py    # event ledger
python3 pipeline/test_factory_rebuild.py  # dependency invalidation
python3 pipeline/test_review_engine.py    # 23/23
python3 pipeline/test_review_bundle.py
python3 pipeline/test_scholarly_oracle.py # 13
python3 pipeline/factory_certificate.py   # integrity + resume
```
All PASS. `catalog.py --all` gives per-work bibliography + source + every layer + audit.
