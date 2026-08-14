# BUILD: THE FACTORY COORDINATION — the modern scheduler driving the full chain (T1→…→EDUCATION)

*2026-08-14 · status: WHAT TO BUILD · the coordination system that runs the whole chain constantly —
OG patala's factory DAG pass (fully spec'd in `docs/FACTORY.md`) + the modern deterministic scheduler
(ip-graph's `next_action.py`) + the gate infrastructure (Nyāya gate, Bayesian engine, ARG golds). The
answer to "do we have a modern alternative to the factory? YES — next_action."*

---

## 1. THE OG FACTORY COORDINATION (the formula system — fully spec'd)

**`/root/projects/patala/docs/FACTORY.md`** — the autonomous factory. The chain:
```
SOURCE → T1 → ARGMAP → L0 → L2 → L200 → C1 → THEME → ARGUMENT → SYNTHESIS → ESSAY → EDUCATION
```
**The DAG pass** (each scheduler iteration):
1. enumerate all eligible (object, layer) jobs from the registry
2. drain deterministic L0 (free)
3. rank model jobs by **translation-target priority** (Krama packet → tier-1 → tier-0/2 → flagships)
4. spend the model budget on T1/ARGMAP/L2/L200/C1 (batched, via the persistent Hermes session)
5. worker → validator → `registry.commit` (immutable, versioned)
6. record failures + audit events

**The files:** `factory_scheduler.py` (the DAG scheduler) · `factory_batch.py` (per-layer production +
retry + audit) · `factory_loop.sh` (the overnight driver) · `object_registry.py` (the immutable ledger) ·
`catalog.py` (per-work × per-layer tracking) · `contracts/CANONICAL-DAG.yaml` (the DAG truth).

**The Hermes skills that drive it:**
- `skills/assemble-stack/SKILL.md` — the per-work stack (00_source→07_c1 + AUDIT), CP1
- `skills/translate-passage/SKILL.md` — the T1→C1 passage flow
- `skills/validate-passage/SKILL.md` — the validation
- `skills/raw-l0/SKILL.md` — the L0 token floor

---

## 2. THE MODERN ALTERNATIVE — `next_action.py` (the deterministic scheduler)

**`/mnt/HC_Volume_106427611/ip-graph/lib/next_action.py`** — GEM 12.3:
```python
def priority(self, w=(2, 1, 3, 2, 2, 1)):
    # P(v) = w1·D + w2·B + w3·U + w4·Q + w5·R − w6·C
    # (downstream load, betweenness, uncertainty, question demand, review deficit, cost)
```
**This is the modern replacement for the factory's static-priority ranking step.** It factors in graph
centrality (betweenness), uncertainty (review deficit), learner question demand, and cost — not just the
static translation-target priority.

---

## 3. THE GATE INFRASTRUCTURE (all real, still there)

| Infra | File | What it is |
|---|---|---|
| **Nyāya gate** | `machinelearning/research/patala_ml/nyayagate.py` | `gate_claim()` + `check_viruddha_graph()` — bounded, never truth; the argument validity gate |
| **Bayesian engine** | `.../strength.py` | `ClaimStrength` (prior/posterior/log_bayes_factor) — the evidence-strength primitive |
| **ARG golds 002-005** | `gold002..005.py` | the 4 argument golds with scholarly_corroboration |
| **P0 graduation** | ip-graph `validate-graduation.py` | **DONE** — 14/14 on real data |
| **CP0-CP12** | `handover/CHECKPOINTS.md` | the checkpoint gates; CP4 (argument) is the frontier |

---

## 4. WHAT TO BUILD (the modern coordination)

### The build:
1. **Drive the factory DAG pass with `next_action`** — same chain (T1→ARGMAP→…→EDUCATION), but the ranking
   uses `next_action.priority()` (the weighted formula) instead of static translation-target priority.
   - The factory enumerates eligible jobs (upstream committed, layer not current) — unchanged.
   - The RANKING uses `next_action`: D (staleness blast-radius) + B (graph betweenness) + U (uncertainty)
     + Q (question demand) + R (review deficit) − C (cost).
   - So the organism "decides what to work on" by formula, not LLM-guess or static list.
2. **Wire the gates into the pass** — the Nyāya gate + Bayesian strength gate the ARGUMENT step; the
   ARG golds are the evidence. The factory commits only what passes.
3. **The Hermes skills drive it** — `translate-passage`/`assemble-stack`/`validate-passage` are the
   agentic hands that execute the worker steps (via `chat_agentic`, NOT `-z`).
4. **Run constantly** — `factory_loop.sh` + `start_overnight.sh` + the watchdog, driven by `next_action`.

### The WHY:
The OG factory is the coordination FORMULA; `next_action` is the modern SMART ranking. Combining them
makes the chain run constantly, deciding what to work on by the weighted formula, gated by the Nyāya +
Bayesian + ARG golds, executed by the Hermes skills. That's the "full factory autonomy" — the shared goal.

---

## THE TEST

```bash
# the modern scheduler ranks real tasks
python3 -c "
import sys; sys.path.insert(0,'/mnt/HC_Volume_106427611/ip-graph/lib')
from next_action import Task
t1=Task('translate-Stk','translate',downstream=8,uncertainty=0.5,cost=1.0)
t2=Task('verify-claim','verify',downstream=2,uncertainty=0.9,cost=0.5)
print('translate prio:', t1.priority(), '| verify prio:', t2.priority())
"
# the factory chain still enumerates the full DAG
python3 -c "
import sys; sys.path.insert(0,'/root/projects/patala/pipeline')
from factory_scheduler import LAYER_ORDER
print('chain:', LAYER_ORDER)
"
```

**Pass when:** the factory chain (T1→…→EDUCATION) runs constantly, driven by `next_action`'s weighted
formula for WHAT to work on, gated by the Nyāya gate + Bayesian strength + the ARG golds, executed by the
Hermes skills (via `chat_agentic`) — the full autonomous factory, modernized.
