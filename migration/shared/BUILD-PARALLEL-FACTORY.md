# THE FULL AUTONOMOUS FACTORY — from sequential loop to parallel multi-layer (the exact path)

*2026-08-14 · status: THE DESIGN · how the current factory (sequential batch loop) becomes a FULL
autonomous factory running MANY layers at once. The honest gap: it's autonomous + constant now, but
SINGLE-THREADED. This is the design for parallelism, grounded in the real files.*

---

## 1. THE CURRENT STATE (verified — what it is now)

**The factory is autonomous + constant, but SEQUENTIAL:**
- `pipeline/factory_loop.sh` — a `while true` loop: each pass runs the scheduler → sleeps → repeats
- `pipeline/factory_scheduler.py` — one pass: enumerate eligible jobs → drain L0 → rank by priority →
  spend the model budget on T1/ARGMAP/L2/L200/C1 → commit
- `pipeline/factory_batch.py` — "deliberately SIMPLE and batch-oriented" — one work, one layer batch at a time
- `contracts/CANONICAL-DAG.yaml` + `object_registry.PREREQS` — the eligibility (a layer is eligible only
  when its upstream is committed)

```text
while true:
  pass: enumerate eligible → drain L0 → rank → budget on T1/ARGMAP/L2/L200/C1 → commit
  sleep
```

**It runs constantly (the loop never stops) but it does NOT parallelize.** One layer advances at a time.

---

## 2. THE THREE THINGS "FULL AUTONOMOUS" NEEDS (and what's already there)

| Needed | Current | Status |
|---|---|---|
| **Constant running** | `factory_loop.sh` (while true) + watchdog + cron | ✅ HAVE |
| **The DAG ordering** | `CANONICAL-DAG.yaml` + `PREREQS` (eligible only when upstream committed) | ✅ HAVE |
| **Parallel layer workers** (many layers at once) | single-threaded batch | ❌ MISSING |
| **Which work/layer next** | `work_priority` (static translation-target priority) | ⚠️ needs `next_action` |

**So the gap is ONE thing: parallelism.** The factory is autonomous + DAG-respecting, but not parallel.

---

## 3. THE PARALLEL DESIGN (the full autonomous factory)

```text
                  THE DAG (CANONICAL-DAG.yaml)
   SOURCE → T1 → ARGMAP → L0 → L2 → L200 → C1 → THEME → ARGUMENT → ...
                     │
   next_action() decides WHICH work + layer to do next (weighted formula)
                     │
        ┌────────────┼────────────┬────────────┬────────────┐
        ▼            ▼            ▼            ▼            ▼
   T1-worker    L0-worker    L2-worker    L200-worker   C1-worker
   (Hermes)    (determin)    (Hermes)     (Hermes)     (Hermes)
        │            │            │            │            │
        └────────────┴────────────┴────────────┴────────────┘
                     │  each commits MACHINE_PROPOSED to the registry
                     ▼
              object_registry (the ledger)
                     │  DAG eligibility (upstream committed = this layer can run)
                     ▼
              the next eligible layer for the next pass
```

### The key rules:
1. **One worker per layer** (a thread/process pool) — each drains ITS layer's eligible jobs.
2. **The DAG gates them** — a worker only processes jobs whose upstream is committed (PREREQS).
3. **`next_action` picks what's next** — which work + layer, by the weighted formula (not static priority).
4. **Each worker commits independently** — immutable, versioned, audited.
5. **The loop drives it** — `factory_loop.sh` spawns the pool each pass.

---

## 4. WHAT TO BUILD (the exact path, with the real files)

### Step 1 — the worker pool (parallelism)
Wrap each layer's `factory_batch._produce_layer` in a worker that can run concurrently:
```python
# a pool: one worker per layer, each drains its eligible jobs
from concurrent.futures import ThreadPoolExecutor
from factory_batch import _produce_layer
from factory_scheduler import _eligible_jobs, LAYER_ORDER
# for each layer in DAG order, run its eligible jobs in a worker
```
- The pool respects the DAG: a layer's jobs are only eligible when upstream committed.
- `ThreadPoolExecutor` gives parallelism; each worker commits to the registry independently.

### Step 2 — `next_action` as the scheduler (which work/layer next)
Replace `work_priority` (static translation-target priority) with ip-graph's `next_action.priority()`:
```python
# P(v) = w1·D + w2·B + w3·U + w4·Q + w5·R − w6·C
# (downstream, betweenness, uncertainty, question demand, review deficit, cost)
```
So the pool decides what to work on by formula, not static list.

### Step 3 — the Agent-3 worker profiles (the execution lanes)
`hermes profile create patala-producer/verifier/coordinator` — the producer/verifier/coordinator lanes
(from `BUILD-AGENT-SYSTEM-RECOVERY.md`) execute the parallel workers via Hermes.

---

## 5. THE RESULT (the full autonomous factory)

```text
while true:
  next_action() → pick the highest-priority work+layer for each worker
  spawn the worker pool (T1/L0/L2/L200/C1 ...) → each drains its eligible jobs
  each commits MACHINE_PROPOSED to the registry (immutable, versioned, audited)
  the DAG + staleness decide what's eligible next
  sleep → repeat
```

Many layers run at once, each respecting the DAG, each committing real objects, driven by `next_action`
+ the Hermes worker profiles, running constantly. THAT is the full autonomous factory.

---

## 6. THE TEST

```bash
# 1. the DAG eligibility already works (verify Stk is eligible for L0 after T1)
python3 -c "
import sys; sys.path.insert(0,'/root/projects/patala/pipeline')
import object_registry as R
print('Stk T1:', sum(1 for k in R._load('T1')['objects'] if k.startswith('sardhatrisatikalottara')))
"
# 2. next_action ranks (the scheduler formula)
python3 -c "
import sys; sys.path.insert(0,'/mnt/HC_Volume_106427611/ip-graph/lib')
from next_action import Task
print('translate:', Task('t','translate',downstream=8,uncertainty=0.5).priority())
print('verify:', Task('v','verify',downstream=2,uncertainty=0.9).priority())
"
```

**Pass when:** the worker pool runs T1/L0/L2/L200/C1 CONCURRENTLY (many layers at once), each respecting
the DAG + `next_action`, committing real objects to the registry, running constantly — the full
autonomous factory.
