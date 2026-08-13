# PĀṬALA AUTONOMOUS FACTORY — canonical reference

*2026-08-13. The single authoritative reference for the **autonomous corpus compiler** (Agent 2's
core system). This doc ties together: the canonical stack, the factory pipeline (files + flow), the
state systems (registry/ledger/audit), the overnight operation, and the unified catalog. It is the
clean index — each section points to the deeper doc where needed.*

---

## 0. WHAT THIS IS

Agent 2 = **the operating system for the corpus**: schedule · execute · retry · resume · version ·
invalidate · rebuild · report. It turns registered Sanskrit works into canonical provenance-bound
objects through the stack, unattended, immutably tracked, and queryable.

The endgame loop:

```
INGEST → TRACK → LINK → AUTOMATE → VERIFY → TRACK
sanskrit    what's      to the     translate    immutable     every layer
works →     untrans-    downloaded    them       progress +     auditable
bibliography  lated     source docs  (factory)    audit log    (catalog)
```

---

## 1. THE CANONICAL STACK (locked)

`SOURCE → T1 → ARGMAP → L0 → L2 → L200 → C1 → THEME → ARGUMENT → SYNTHESIS → ESSAY → EDUCATION`

| Layer | What it is | Worker |
|---|---|---|
| SOURCE | raw Sanskrit base text | `factory_batch._register_source` |
| T1 | transliteral word-gloss (`[and]-GLOSS (IAST)`) | `t1_worker.py` |
| ARGMAP | the passage's argument structure (lateral guide) | `argument_map_worker.py` |
| L0 | structured token records from T1 (deterministic) | `raw_l0.py` |
| L2 | readable prose (guided by ARGMAP) | `l1_l2_translate.py` |
| L200 | the audit of how L2 was derived (8-section) | `l200_worker.py` |
| C1 | passage-local commentary | `c1_worker.py` |
| THEME/ARGUMENT/... | high scholarly layers | theme/essay/education workers |

Full spec: `handover/agent-2-integration/CANONICAL-LAYER-STACK.md`.

---

## 2. THE FACTORY PIPELINE (files + flow)

| File | Role |
|---|---|
| `start_overnight.sh` | ONE-COMMAND launcher (start/status/stop both systems + watchdogs) |
| `factory_loop.sh` | the overnight repeat-loop driver |
| `factory_loop_watchdog.sh` | cron watchdog (restart if the loop dies) |
| `factory_scheduler.py` | the DAG scheduler — enumerates ALL eligible (object,layer) jobs, ranks, executes within budget |
| `factory_batch.py` | per-layer production + durable failure/retry queue + audit ledger |
| `factory_status.py` | per-work progress dashboard |
| `factory_certificate.py` | the bulk-run certificate (integrity + resume) |
| `factory_rebuild.py` | Era C: supersession propagation + targeted regeneration |
| `catalog.py` | the unified per-work × per-layer tracking view |
| `object_registry.py` | the immutable per-layer artifact registry (authoritative state) |

**The DAG pass** (each scheduler iteration):
1. enumerate all eligible (object, layer) jobs from the registry (upstream committed + this layer not current)
2. drain deterministic L0 (free)
3. rank model jobs by **translation-target priority** (Krama packet → tier-1 → tier-0/2 → flagships/
   unknown), round-robin within each priority band so one work can't monopolize
4. spend the model budget on T1/ARGMAP/L2/L200/C1. T1 is produced in **batches** (one call glosses many
   verses — see §3a) — optionally via a **persistent Hermes session** (`PATALA_T1_SESSION=1`) that
   retains the work's context across calls
5. worker → validator → `registry.commit` (immutable, versioned)
6. record failures (upserted, capped) + audit events

**How a passage advances** (registry-derived, no manual calls):
`SOURCE → T1 → ARGMAP → L0 → L2 → L200 → C1 → ...` — each pass re-scans the registry and picks up
whatever became eligible.

## 3a. T1 throughput (batched + optional session streaming)

- **Default (batched):** `t1_worker.t1_generator` packs a whole batch (all verses + Vidyut tokens)
  into ONE prompt, binds each verse's gloss to its `object_id`, and writes a per-verse stream log
  (`data/corpus/downloads/t1-stream.jsonl`) as each verse is produced.
- **Session streaming (`PATALA_T1_SESSION=1`):** `t1_session.py` opens ONE long-lived Hermes session per
  work seeded with the work's context packet, then feeds verse-chunks via `--resume <session>` — Hermes
  retains accumulated context across calls ("long context + document as it goes"), and each chunk is
  committed + stream-logged immediately (a failed chunk loses only that chunk, retryable).
  **EXPERIMENTAL — not yet proven live; batched is the proven default.**
- **Stream log schema:** `{ts, object_id, status: MACHINE_PROPOSED|ABSTAIN|GENERATION_FAILED,
  gloss_count, error}` — append-only, per-verse, consumable read-only by Agent 1.

Deep trace: `docs/SOURCE-PROCESS-OVERNIGHT.md`.

---

## 3. THE STATE SYSTEMS (3 tiers — do not conflate)

| Tier | Files | Written by | Role |
|---|---|---|---|
| **REGISTRY (canonical)** | `data/corpus/registries/<layer>-registry.jsonl` | the factory (`object_registry.commit`) | the authoritative per-layer object state — immutable, versioned, provenance-bound |
| **LEDGER (operational)** | `data/corpus/downloads/translation-state-ledger.json` | `auto_translate_raw.py` + `corpus_state.py` | per-work operational view (`bibliographic_id`, translation/l0 status, `next_action`) |
| **AUDIT (action trail)** | `data/corpus/downloads/factory-audit.jsonl` | the factory (`_audit`) | append-only, in-order record of every commit/reject/retryable |
| **T1 STREAM LOG** | `data/corpus/downloads/t1-stream.jsonl` | `t1_worker` / `t1_session` | append-only per-verse T1 output (MACHINE_PROPOSED/ABSTAIN/GENERATION_FAILED) |
| **QUEUE (resilience)** | `factory-failure-queue.jsonl` + `agent3-queue-state.json` | factory + live runner | durable failure/retry records + scheduling |

**The factory is registry-driven** — it scans committed registries, never walks the ledger. The live
runner advances the ledger. They stay consistent because both read/write the same passages.

**Idempotency / crash-resume:** `is_committed(object_id, input_hash)` prevents re-committing anything
already current; a watchdog-restarted loop continues from the correct frontier, never redoing completed
work, never duplicating.

---

## 4. OVERNIGHT OPERATION

```bash
bash pipeline/start_overnight.sh start     # launch both systems + install watchdogs
bash pipeline/start_overnight.sh status    # what's running + corpus dashboard
bash pipeline/start_overnight.sh stop      # stop the factory loop (leave live runner)
```

Tuning (env, before `start`): `FACTORY_MODEL_CALLS` (budget/pass, default 6) · `FACTORY_PER_LAYER` ·
`FACTORY_THROTTLE` · `FACTORY_SLEEP` · `FACTORY_MAX_PASSES`.

Two systems run overnight, both watchdog-protected + rate-limited:
- **live RAW→EN runner** (`auto_translate_raw.py`) → English substrate
- **factory loop** (`factory_loop.sh`) → canonical SOURCE→C1 objects

Runbook: `pipeline/OVERNIGHT.md` · deep trace: `docs/SOURCE-PROCESS-OVERNIGHT.md`.

---

## 5. THE UNIFIED CATALOG (audit + track every layer)

```bash
python3 pipeline/catalog.py                  # all works, human view
python3 pipeline/catalog.py --work <work>    # one work
python3 pipeline/catalog.py --json           # machine-readable
```

Per work it shows: **bibliography** (title/translation_status/verified, from the atlas) · **source**
linkage · **every layer's** current/stale/versions (SOURCE..EDUCATION) · **recent audit events**.

This is how the whole pipeline — bibliography → source → translation → high layers (themes, arguments,
essays, education) — becomes auditable and tracked. The registries are authoritative; the audit ledger
is the in-order action trail; the atlas is the bibliography; the catalog is the projection that ties
them together.

---

## 6. FAILURE RESILIENCE (the A2-11 contract)

- A passage whose model call fails → recorded (upserted) as RETRYABLE; neighbors still commit (isolation).
- Retried at the next pass, capped at `MAX_ATTEMPTS` (default 3) → then `BLOCKED_RETRY_EXHAUSTED`
  (stops consuming budget, can't wedge the run). Audit history preserved (never deleted).
- T1 timeout is size-aware (scales with verse length) so long verses get more time.
- `factory_certificate.py` proves integrity (0 duplicates, resume PASS) at the end of a run.

---

## 7. VALIDATION (all green, 2026-08-13)

- **18 deterministic test suites PASS**: test_workers · test_t1 · test_autonomy · test_l0 · test_l1_l2 ·
  test_corpus_state (11/0) · test_l0_align (26/0) · test_review_engine (23/0) · test_autonomous ·
  test_scholarly_oracle · test_argmap · test_failure_queue · test_factory_status · test_factory_scheduler ·
  test_rate_limit · test_factory_rebuild · test_factory_certificate · test_catalog.
- **IPVV-exemplar suite PASS** (T1/L0/ARGMAP/L2/L200/C1 verified against the real IPVV files) +
  `prove_l0_equivalence` (schema/validator/lossless).
- **Both systems running** (live runner + factory loop), watchdog-protected.

---

## 8. DOC MAP (the clean index)

| Concern | Doc |
|---|---|
| This factory reference | `docs/FACTORY.md` |
| Agent-2 handover index (READ FIRST) | `handover/agent-2-integration/README.md` |
| Canonical layer stack (locked) | `handover/agent-2-integration/CANONICAL-LAYER-STACK.md` |
| Overnight runbook (how to run) | `pipeline/OVERNIGHT.md` |
| Overnight source-process trace | `docs/SOURCE-PROCESS-OVERNIGHT.md` |
| Gold-standard mechanisms + data flow | `docs/GOLD-STANDARD-MECHANISMS-AND-DATAFLOW.md` |
| ML-verifiable layer contracts | `docs/ML-VERIFIABLE-LAYER-CONTRACTS.md` |
| Roadmap (Era A/B/C) | `docs/agent2nextdev.md` |
| Dev plan + checkpoints + current state | `handover/agent-2-integration/` (DEV-PLAN, CHECKPOINTS-INTEGRATION, CURRENT-STATE) |
| Live cross-agent status | `live/agent2.md` · `live/agent1.md` |

---

## 9. ORGANIZED FILES + OBSOLETE (cleanup)

**The current factory** is exactly these files — nothing else in `pipeline/factory_*` is part of it:
`start_overnight.sh` · `factory_loop.sh` · `factory_loop_watchdog.sh` · `factory_scheduler.py` ·
`factory_batch.py` · `factory_status.py` · `factory_certificate.py` · `factory_rebuild.py` ·
`t1_worker.py` · `t1_session.py` ·
`catalog.py` + `object_registry.py` (the state).

**Marked obsolete (superseded, kept for history only):**
- `pipeline/factory_run.py` — the original one-shot calibration driver → use `factory_scheduler.py`.
- Legacy L0 drivers (`auto_run.py`, `auto_raw_l0.py`, `prove_raw_l0.py`, `proof_autonomous_l0.py`) —
  the RAW-L0 v1 era; the factory now goes through the DAG scheduler + registry. Not referenced by any
  current test, doc, or the overnight system.

These are **marked, not deleted** — history is preserved. New work should not use them.
