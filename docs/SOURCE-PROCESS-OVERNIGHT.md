> **ARCHIVED / SUPERSEDED** — kept for history only. Do NOT follow as current. See `docs/INDEX.md` + `docs/DOCS-AUDIT.json` for the canonical doc for this concern.

# PĀṬALA AUTONOMOUS FACTORY — FULL SOURCE PROCESS (what happens when you run overnight)

*2026-08-13. This is the complete, code-accurate trace of what the system does when you run
`bash pipeline/start_overnight.sh start` and leave it overnight. Every step below is a real code path
(not a description of intent). It is the "how it actually works" companion to `OVERNIGHT.md` (the
runbook).*

---

## 0. THE ONE COMMAND

```bash
bash pipeline/start_overnight.sh start
```

This launches TWO independent autonomous systems, each watchdog-protected, sharing one rate-limited
model API:

```
SYSTEM 1:  live RAW→EN runner     (auto_translate_raw.py)   → English translations
SYSTEM 2:  factory loop           (factory_loop.sh)         → canonical SOURCE→C1 objects
```

---

## 1. WHAT `start_overnight.sh start` DOES (in order)

`pipeline/start_overnight.sh` runs these exact steps:

1. **Installs cron watchdogs** (idempotent, removes old then re-adds):
   ```
   */5 * * * * pipeline/watchdog_auto_translate.sh     → restart live runner if dead
   */5 * * * * pipeline/factory_loop_watchdog.sh       → restart factory loop if dead
   ```
2. **Starts the live RAW→EN runner** (if not already running):
   - `setsid nohup python3 -u pipeline/auto_translate_raw.py >> /tmp/opencode/auto-translate.log &`
   - `setsid` = detached process group (survives your shell/session ending).
3. **Starts the factory loop** (if not already running):
   - `setsid nohup bash pipeline/factory_loop.sh >> /tmp/opencode/factory-loop.log &`

Both are **idempotent** — if already running (checked by `pgrep`), it does nothing.

---

## 2. THE WATCHDOG LOOP (every 5 minutes, forever)

`watchdog_auto_translate.sh` / `factory_loop_watchdog.sh` (run by cron every 5 min):

```
IF the target process is alive   → exit 0 (do nothing)
ELSE                             → setsid nohup ... &  (restart it)
```

So if anything crashes overnight, cron restarts it within 5 minutes. Because every process is
**registry-driven + idempotent** (dedup by `object_id + input_hash`), a restart **resumes from the
correct frontier with zero duplicate commits** — it never redoes completed work.

---

## 3. WHAT THE LIVE RAW→EN RUNNER DOES (System 1)

`pipeline/auto_translate_raw.py` (detached, watchdog-protected):

```
for each work in the RAW_SANSKRIT queue (the ledger):
    load_raw_source(work)            # read the on-disk Sanskrit
    split_verses() / prose-chunks    # split into passages
    for each context-full batch:     # bounded by PATALA_CONTEXT (default 1M tokens)
        batch_translate.py → model.chat → hermes -z   # ONE model call per full context
    write data/corpus/downloads/translations/<work>.jsonl   # MACHINE_PROPOSED English
    advance_ledger(work)             # t1=MODERN_PRESENT (the readable English layer)
```

- **Idempotent**: skips passages whose `source_sha256` already has a non-empty translation.
- **Crash-safe**: per-work checkpoint; resumes where it left off.
- This produces the **readable English substrate** (the L2-style output) for the whole corpus.

---

## 4. WHAT THE FACTORY LOOP DOES (System 2) — the full trace

`factory_loop.sh` runs an infinite repeat loop:

```
while true:
    PASS n:
        factory_scheduler.py --retry --per-layer N --max-model-calls B --throttle T
            → retry durable failures first (A2-11)
            → run ONE DAG pass (see §5)
    sleep FACTORY_SLEEP (30s)
    next pass
```

Each pass calls `pipeline/factory_scheduler.py`, which is the **DAG scheduler** (§5). It logs to
`/tmp/opencode/factory-loop.log`. When `FACTORY_MAX_PASSES` is set, it emits the bulk certificate at
the end.

---

## 5. ONE DAG PASS (the core of the factory loop)

`pipeline/factory_scheduler.py::scheduler_pass()` runs these exact steps:

### 5a. Enumerate ALL eligible jobs (DAG scheduling)
`_eligible_jobs(works, layers)` walks every registered work × every layer and finds every
`(object_id, layer)` pair where:
- the layer's **upstream** (from `object_registry.PREREQS`) has a **committed** object for that passage
- the layer itself does **not** yet have a committed current object for it

Eligibility map (the canonical dependency DAG):
```
T1      eligible when SOURCE committed
ARGMAP  eligible when T1 committed
L0      eligible when T1 committed        (deterministic — free)
L2      eligible when ARGMAP committed
L200    eligible when L2 committed
C1      eligible when L200 committed
```

So after T1 commits for a passage, the NEXT pass sees L0 and ARGMAP become eligible → downstream
advances automatically (§7).

### 5b. Rank jobs
- **Deterministic jobs** (L0) run FIRST, free (never consume the model budget).
- **Model-bound jobs** (T1/ARGMAP/L2/L200/C1) are ranked **round-robin across works** so one work
  cannot monopolize the model.

### 5c. Drain deterministic jobs (free)
`_produce_layer("L0", ...)` runs immediately for eligible L0, no budget cost.

### 5d. Spend the model budget
The scheduler spends at most `FACTORY_MODEL_CALLS` model-bound jobs per pass (default 6), sleeping
`FACTORY_THROTTLE` seconds between them. This is the **rate limiter** that keeps the factory from
starving the live runner.

---

## 6. WHAT A SINGLE LAYER JOB DOES (`factory_batch._produce_layer`)

For one `(object_id, layer)` job:

```
1. handler = autonomy.LAYER_HANDLERS[layer]     # the real worker (t1_worker, l0_worker, ...)
2. proposals = handler["generator"](layer, batch)   # the model (or deterministic) produces the object
3. ok, why = handler["validator"](layer, proposal)  # the layer-specific deterministic validator
4. if ok:   registry.commit(layer, object_id, input_hash, payload)   # immutable, versioned
   else:    record failure (validator rejection = permanent, model-fail = retryable)
```

**Each layer's worker + validator:**
| Layer | Worker | Validator (deterministic gate) |
|---|---|---|
| T1 | `t1_worker.py` | canonical `[and]-GLOSS (IAST)` shape + source binding + fail-closed |
| L0 | `raw_l0.py` | `validate_l0_spec` (P0 lossless + schema) |
| ARGMAP | `argument_map_worker.py` | 4-section shape + provenance |
| L2 | `l1_l2_translate.py` | semantic-fidelity (content ⊆ L1+supplies) + provenance |
| L200 | `l200_worker.py` | Task-2 fidelity (8-section, MT/IA split) |
| C1 | `c1_worker.py` | C1-SPEC §17 (passage-local) |

**The registry (`object_registry.py`) is the authoritative state.** Every commit is immutable +
versioned; a correction creates a new version that supersedes the old (old kept for history).

---

## 7. HOW DOWNSTREAM ADVANCES AUTOMATICALLY (the DAG cascade)

Because eligibility is derived from the registry each pass, the system is self-advancing:

```
PASS 1:  SOURCE exists → T1 eligible → T1 committed for some passages
PASS 2:  T1 exists → L0 + ARGMAP eligible → L0 (free) + ARGMAP committed
PASS 3:  ARGMAP exists → L2 eligible → L2 committed
PASS 4:  L2 exists → L200 eligible → L200 committed
PASS 5:  L200 exists → C1 eligible → C1 committed
```

So over successive passes, a passage naturally travels SOURCE → T1 → ARGMAP → L0 → L2 → L200 → C1,
with the scheduler spending its model budget across the **whole graph** (not just the lowest layer).

---

## 8. FAILURES ARE SAFE (the A2-11 contract)

- A passage whose model call **times out or returns bad JSON** → `GENERATION_FAILED` → recorded as
  **RETRYABLE** in `factory-failure-queue.jsonl` (append-only audit). The neighbor passages **still
  commit** (isolation).
- On a later pass, `--retry` re-attempts it. On success it's marked **RESOLVED** (history preserved,
  never deleted). On failure it stays OPEN, bounded by the **size-aware timeout** (T1 scales timeout
  with token count, so long verses get more time instead of failing).
- A **validator rejection** (permanent) is recorded, not retried forever.
- **Zero duplicate commits** — `is_committed(object_id, input_hash)` in the registry prevents any
  re-commit of already-current work.

---

## 9. THE BULK CERTIFICATE (proves the run was clean)

At the end of a bounded run (`FACTORY_MAX_PASSES=N`), `factory_loop.sh` runs:

```bash
python3 pipeline/factory_certificate.py --passes N --model-calls TOTAL
```

This emits (to `data/corpus/downloads/factory-certificate.json`):
```
{ run_id, ts, scheduler_version, passes, works_touched,
  jobs: {attempted, committed, retryable, rejected, already_current},
  by_layer: {T1, L0, ARGMAP, L2, L200, C1},
  model_calls,
  integrity: {duplicates, bad_parent_hashes, registry_conflicts},   ← 0 = healthy
  resume_test: PASS }
```

`resume_test: PASS` + `integrity.duplicates == 0` = the run was idempotent and dependency-clean.

---

## 10. CHECKING PROGRESS OVERNIGHT (the morning view)

| Command | What it tells you |
|---|---|
| `bash pipeline/start_overnight.sh status` | are both systems alive? + corpus dashboard |
| `python3 pipeline/factory_status.py --all` | per-work progress (SOURCE/T1/.../C1 + stale/retryable) |
| `python3 pipeline/factory_certificate.py` | bulk certificate (integrity + resume) |
| `tail /tmp/opencode/factory-loop.log` | the factory's per-pass log |
| `tail /tmp/opencode/auto-translate.log` | the live translation log |

---

## 10.5 HOW STATE PERSISTS: the registry (canonical) vs the ledger (operational)

Two state systems, two writers. Do not conflate them:

| System | Files | Written by | Role |
|---|---|---|---|
| **REGISTRY (canonical)** | `data/corpus/registries/<layer>-registry.jsonl` | the factory workers (`object_registry.commit`) | the authoritative object state — immutable, versioned, provenance-bound |
| **LEDGER (operational)** | `data/corpus/downloads/translation-state-ledger.json` | the live RAW→EN runner (`advance_ledger`) + `corpus_state.py` | per-work operational view (translation/l0 status/next_action) |
| **QUEUE** | `agent3-queue-state.json` + `factory-failure-queue.jsonl` | live runner + factory | scheduling + durable failure/retry records |

**The factory is registry-driven.** The DAG scheduler (`factory_scheduler.py`) derives "what's next" by
scanning what is actually committed in the registries — it never walks the ledger. The live runner
advances the ledger. They stay consistent because both read/write the same passages; the **registry is
authoritative for the factory**, the **ledger is the operational view**.

**Transitions are derived, not hardcoded:** once T1 commits for a passage, the next pass sees L0 +
ARGMAP become eligible (from the registry), and so on down to C1. Every commit is immutable + versioned
(a correction creates a new version that supersedes the old). `is_committed(object_id, input_hash)`
makes everything idempotent + crash-resume-safe — a watchdog-restarted loop continues from the correct
frontier, never redoing completed work and never duplicating.

## 11. THE COMPLETE FILE → PROCESS MAP

```
START:  bash pipeline/start_overnight.sh start
          ├─ cron watchdog_auto_translate.sh ──────────────┐ (restarts)
          ├─ cron factory_loop_watchdog.sh ────────────────┤ (restarts)
          ├─ setsid nohup auto_translate_raw.py ───────────┼─ System 1 (English)
          └─ setsid nohup factory_loop.sh ─────────────────┘
                 └─ (loop) factory_scheduler.py --retry
                        ├─ retry failures (factory_batch._retry_failures)
                        └─ scheduler_pass()
                              ├─ _eligible_jobs() → the DAG
                              ├─ drain deterministic L0 (free)
                              └─ spend model budget on T1/ARGMAP/L2/L200/C1
                                     └─ factory_batch._produce_layer()
                                            ├─ worker (t1_worker, ...)
                                            ├─ validator (layer-specific)
                                            └─ registry.commit (immutable, versioned)
                              └─ record failures (retryable) / report
                        └─ sleep → next pass
                 └─ at end: factory_certificate.py → the bulk certificate
```

---

## 12. WHAT YOU CAN EXPECT OVERNIGHT (honest)

- **Progress**: a steady accumulation of canonical objects across works (T1 → ARGMAP → L0 → L2 →
  L200 → C1), advancing a few passages per pass (model-bound).
- **Rate**: bounded by the shared model API. Raise `FACTORY_MODEL_CALLS` for faster factory (at the
  live runner's expense). `FACTORY_PER_LAYER` controls passages/layer/pass.
- **Safety**: a problem verse is retryable (never a wedge); a crash is auto-restarted by cron;
  duplicates are impossible (registry idempotency); the certificate proves integrity.
- **Live runner**: continues translating the RAW→EN queue independently.
