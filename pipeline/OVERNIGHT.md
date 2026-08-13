# PĀṬALA AUTONOMOUS FACTORY — OVERNIGHT RUNBOOK

*2026-08-13. How to leave the autonomous factory running overnight and wake up to maximum progress.
Everything is watchdog-protected, rate-limited, and idempotent — you do NOT need to watch it.
For the full code-level trace of every step, see `docs/SOURCE-PROCESS-OVERNIGHT.md`.*

---

## 1. ONE-COMMAND START

```bash
cd /root/projects/patala
bash pipeline/start_overnight.sh start
```

This launches BOTH autonomous systems + installs the cron watchdogs:

| System | What it does | Watchdog |
|---|---|---|
| **Live RAW→EN runner** | translates the RAW_SANSKRIT queue → English (`auto_translate_raw.py`) | `watchdog_auto_translate.sh` (cron 5min) |
| **Factory loop** | advances all works through canonical SOURCE→C1 (`factory_loop.sh` → DAG scheduler) | `factory_loop_watchdog.sh` (cron 5min) |

Both are **rate-limited** so they coexist without starving each other's model API.

## 2. MORNING CHECKLIST

```bash
bash pipeline/start_overnight.sh status     # are both systems still alive?
python3 pipeline/factory_status.py --all    # the corpus dashboard (what advanced)
python3 pipeline/factory_certificate.py     # the bulk-run certificate (integrity + resume)
tail /tmp/opencode/factory-loop.log         # the factory's overnight log
tail /tmp/opencode/auto-translate.log       # the live translation log
```

The dashboard shows per-work progress (SOURCE/T1/ARGMAP/L0/L2/L200/C1 + stale/retryable). The
certificate shows total commits + integrity (0 duplicates = healthy).

## 3. TUNING (optional, set env before `start`)

```bash
FACTORY_PER_LAYER=2     # passages per layer per work per pass
FACTORY_MODEL_CALLS=6   # model-call budget per pass (RAISE = faster factory, slower live runner)
FACTORY_THROTTLE=2      # seconds between model batches
FACTORY_SLEEP=30        # seconds between passes
FACTORY_MAX_PASSES=0    # 0 = run forever (set N for a bounded test run)
```

## 4. STOP / MANAGE

```bash
bash pipeline/start_overnight.sh stop     # stop the factory loop (leave live runner)
# to stop the live runner too:
setsid bash -c 'pkill -f "auto_translate_raw.py"'
```

---

## THE CANONICAL FILES (where everything lives)

| Concern | Path |
|---|---|
| **Canonical layer stack (LOCKED — the order + file types)** | `handover/agent-2-integration/CANONICAL-LAYER-STACK.md` |
| **Mission / CP ladder** | `handover/agent-2-integration/MISSION-AUTONOMOUS-FACTORY.md` |
| **Dev plan (Era A/B/C)** | `handover/agent-2-integration/DEV-PLAN.md` |
| **Checkpoints** | `handover/agent-2-integration/CHECKPOINTS-INTEGRATION.md` |
| **Current state (production reference)** | `handover/agent-2-integration/CURRENT-STATE.md` |
| **Agent 2 orientation (process workflow)** | `handover/agent-2-integration/ORIENTATION.md` |
| **Next-dev roadmap (Era A/B/C details)** | `docs/agent2nextdev.md` |
| **ML-verifiable layer contracts** | `docs/ML-VERIFIABLE-LAYER-CONTRACTS.md` |
| **Gold-standard mechanisms + data flow** | `docs/GOLD-STANDARD-MECHANISMS-AND-DATAFLOW.md` |
| **Live cross-agent status** | `live/agent2.md` · `live/agent1.md` |
| **Agent 2 handover (this session)** | `handover/agent-2-integration/BUILD-RECORD-2026-08-13-*.md` |

## THE FACTORY PIPELINE (what runs)

```
pipeline/start_overnight.sh          <- the ONE-COMMAND launcher (this runbook)
pipeline/factory_loop.sh             <- overnight repeat-loop driver
pipeline/factory_loop_watchdog.sh    <- cron watchdog (restart if dies)
pipeline/factory_scheduler.py        <- DAG scheduler (advances all works' eligible jobs)
pipeline/factory_batch.py            <- per-layer production + failure/retry queue
pipeline/factory_status.py           <- per-work progress dashboard
pipeline/factory_certificate.py      <- bulk-run certificate (integrity + resume)
pipeline/factory_rebuild.py          <- Era C: supersession propagation + targeted regeneration
pipeline/{t1,l0,l1_l2,l200,c1,theme,essay,education,argument_map}_worker.py  <- the layer producers
pipeline/object_registry.py          <- immutable per-layer registry (the authoritative state)
```

## HONEST EXPECTATIONS FOR OVERNIGHT

- **What advances**: T1 → ARGMAP → L0 → L2 → L200 → C1 objects across all registered works, steadily.
  The dashboard reflects real progress.
- **What's slow**: T1 is model-bound; with a small budget (to respect the live runner), the factory
  advances a few passages per pass. Raising `FACTORY_MODEL_CALLS` speeds it up at the live runner's
  expense.
- **Failures are SAFE**: a problematic verse (e.g. bhavopahara's long text) is recorded as retryable,
  never wedges the run, and is retried via the size-aware policy.
- **The certificate proves integrity**: 0 duplicate current versions + resume PASS = the run was clean.

*This is the Era B "run for 8 hours" deliverable — the autonomous corpus compiler left unattended.*
