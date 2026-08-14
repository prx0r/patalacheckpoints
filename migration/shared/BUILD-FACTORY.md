# BUILD: THE FACTORY — the REAL implementations (what to wire into ip-graph's organism)

*2026-08-14 · status: WHAT TO BUILD (for agentgraph) · the precise build spec for the OG patala factory —
all the REAL worker + scheduler + batch implementations ip-graph's `ingestion_organism` should drive,
referencing the ACTUAL files.*

---

## THE GAP

ip-graph's `ingestion_organism` has the loop design but its `refine()` is abstract — it doesn't call the
REAL factory workers that produce and commit actual T1/L0/L2/L200/C1 objects. OG patala has all of them.

---

## THE REAL FACTORY FILES (reference these)

### 1. The scheduler + loop (the autonomous driver)
- **`/root/projects/patala/pipeline/factory_scheduler.py`** — the DAG scheduler:
  - `LAYER_ORDER = ["T1", "ARGMAP", "L0", "L2", "L200", "C1"]`
  - `MODEL_LAYERS = {"T1","ARGMAP","L2","L200","C1"}` (L0 is deterministic/free-draining)
  - eligibility: upstream committed + not already current; ranks by `work_priority` (the translation-target
    registry)
  - `scheduler_pass(works, layers, per_layer)` → executes within a budget
- **`/root/projects/patala/pipeline/factory_loop.sh`** — the overnight autonomous driver:
  - `LAYERS="T1,ARGMAP,L0,L2,L200,C1"`, watchdog-protected
- **`/root/projects/patala/pipeline/factory_loop_watchdog.sh`** — the watchdog

### 2. The batch + commit path (how proposals become real registry objects)
- **`/root/projects/patala/pipeline/factory_batch.py`**:
  - `_source_objects(work_id, count)` — loads committed SOURCE
  - `_produce_layer(layer, inputs, batch_size)` — runs the worker + validator + `R.commit`
  - `_commit_proposal(layer, p)` — via the handler validator → `R.commit(..., MACHINE_PROPOSED)`
  - `_audit(entry)` — the machine-readable audit ledger (`data/corpus/downloads/factory-audit.jsonl`)
- **`/root/projects/patala/pipeline/object_registry.py`** — the append-only versioned registry:
  - `commit(layer, object_id, input_hash, created_by, status, payload)` — the real commit
  - `_save`/`_load` + `append_event` (the hash-chained ObjectEvent ledger)

### 3. The 9 layer workers (each produces + validates one layer)
| Worker | Layer | Deterministic? |
|---|---|---|
| `t1_worker.py` | T1 (word gloss) | model (Hermes) |
| `l0_worker.py` | L0 (token floor) | deterministic |
| `argument_map_worker.py` | ARGMAP (outline) | model |
| `l1_l2_worker.py` | L2 (readable prose) | model (optional) |
| `l200_worker.py` | L200 (proof) | model |
| `c1_worker.py` | C1 (commentary) | model |
| `theme_worker.py` | THEME (clusters) | model |
| `essay_worker.py` | ESSAY | model |
| `education_worker.py` | EDUCATION | model |

### 4. The factory support (certificate, rebuild, status, run)
- `factory_certificate.py` — the live-registry integrity cert
- `factory_rebuild.py` — the A2-18 DependencyImpactReport (supersession propagation)
- `factory_status.py` / `factory_run.py` — status + run
- `contracts/CANONICAL-DAG.yaml` — the ONE dependency manifest (the DAG truth)

### 5. The autonomy wiring
- `autonomy.py` — `LAYER_HANDLERS` (wires the workers to the scheduler; real ARGUMENT/SYNTHESIS handlers)

---

## WHAT TO BUILD (drive the organism with the real factory)

### The build:
1. **`ingestion_organism.refine()` should call `factory_batch._produce_layer()`** — so the organism's
   refine step runs the REAL worker (e.g. `t1_worker` via Hermes) + validator + commits to the REAL
   `object_registry`, not an abstract `SanskritDoc.layers_done`.
2. **The organism's loop should use `factory_scheduler`** for eligibility + priority (not a flat queue).
3. **The organism's commit should call `object_registry.commit()`** — the REAL store the site reads.
4. **The DAG truth** is `contracts/CANONICAL-DAG.yaml` — the organism must derive eligibility from it.

### The WHY:
The organism is the loop DESIGN; the factory is the real EXECUTION. Wiring them makes the organism
actually produce + commit real T1/L0/L2/L200/C1 objects to the registry the site serves — not an abstract
status. This is the "full factory autonomy" — the shared goal.

---

## THE TEST

```bash
# run the real T1 worker on 4 real Stk verses (via the scheduler's batch)
python3 -c "
import sys; sys.path.insert(0,'/root/projects/patala/pipeline')
from factory_batch import _source_objects, _produce_layer
inputs=_source_objects('sardhatrisatikalottara', count=4)
print('inputs:', len(inputs), '| first:', inputs[0].get('verse','')[:40] if inputs else 'none')
"
```

**Pass when:** the organism's refine() runs the REAL factory workers, commits MACHINE_PROPOSED objects to
the real `object_registry` (verified in the T1/L0/L2/L200/C1 registries), gated by the handler validators.
