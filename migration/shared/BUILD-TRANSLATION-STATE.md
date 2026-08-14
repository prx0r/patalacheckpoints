# BUILD: THE TRANSLATION-STATE MACHINE + THE INTERNAL TRANSLATION INVENTORY

*2026-08-14 · status: WHAT TO BUILD (for agentgraph) · the precise build spec for the per-work
translation-state machine and the internal inventory — referencing the REAL OG patala files (corpus_state,
the ledger, the actual translations). This is the "full factorial state machine autonomously processing
all works".*

---

## THE REAL OG PATALA STATE MACHINE

### 1. `corpus_state.py` — the per-work FSM (the control plane)
**`/root/projects/patala/pipeline/corpus_state.py`**
```python
class WorkState:
    t1: str = "NOT_STARTED"   # NOT_STARTED | LEGACY_PRESENT | MODERN_PRESENT | PARTIAL
    l2: str = "NOT_STARTED"
    c1: str = "NOT_STARTED"
def next_valid_action(s: WorkState) -> dict:
    # LEGACY_T1_PRESENT -> MODERNIZE_L0
    # ... the legal next transition per work
def discover_works() -> list[WorkState]:   # scans the corpus, builds the 111-work state
def ledger_json() -> dict:                  # the machine-readable state ledger
```
- `NEXT_VALID_ACTION(work)` — the single legal next transition (the control plane for Agent 3)
- Tracks **111 works** through `t1`/`l2`/`c1` statuses

### 2. The state ledger (the honest per-work state)
**`/root/projects/patala/data/corpus/downloads/translation-state-ledger.json`**
- `works`: 111 entries, each with `work_id`, `bibliographic_id`, `source`, per-layer state
- `note`: "Agent 2 translation-state ledger. The control plane for Agent 3."

---

## THE REAL INTERNAL TRANSLATION INVENTORY (what exists internally)

| Inventory | Count | Where |
|---|---|---|
| Translated `<work>.jsonl` (raw-EN) | **71 works** | `/root/projects/patala/data/corpus/downloads/translations/*.jsonl` |
| T3 finals (completed translations) | **11 works** | `/root/projects/sanskritree/translations/05_t3_final/` |
| T1 gold (word-faithful glosses) | **28 chunks** | `/root/projects/sanskritree/translations/_stack/ipvv/01_t1/` + `02_t1/` |
| L200 proof audits | **63** | `/root/projects/sanskritree/translations/_stack/ipvv/l200/` |
| C1 commentaries | **63** | `/root/projects/sanskritree/translations/_stack/ipvv/c1/read/` |
| Old-batch T1 (sanskritree) | **141** | `/root/projects/sanskritree/translations/01_t1_working/` |
| The Stk work (new, untranslated) | **1 (298 verses)** | `/root/projects/patala/data/corpus/sources/sardhatrisatikalottara/` |

---

## THE FULL FACTORIAL STATE MACHINE (what to build)

### The per-work FSM (the full transitions)
```
SOURCE_PRESENT
  → T1:      NOT_STARTED → LEGACY_PRESENT → MODERN_PRESENT      (Hermes t1_worker)
  → L0:      MODERNIZE_L0 if legacy T1                           (deterministic l0_worker)
  → ARGMAP:  the lateral outline                                (model)
  → L2:      LEGACY_PRESENT → MODERN                             (l1_l2_worker)
  → L200:    the proof (only if L2 modern)                       (l200_worker)
  → C1:      the commentary                                      (c1_worker)
  → T3:      the final (only when C1 + proof done)               (the synthesis)
  → COMPLETE
```

### The build:
1. **Adopt `corpus_state.next_valid_action()` into `ingestion_organism`** — the organism's `refine()` step
   uses the per-work FSM to decide the legal next transition (not a flat `layers_done`).
2. **Build the internal translation inventory** as a machine-readable registry:
   ```
   work → t1 (gold/modern/none) → l2 → l200 (proof) → c1 → t3
   ```
   compiled from the REAL assets (71 jsonl, 11 T3, 28 T1, 63 L200, 63 C1).
3. **The full factorial FSM over all 111+ works** — each work advances through its legal transitions
   autonomously, gated by review + integrity + Hermes.
4. **The state → graph → site bridge** — the updated state flows into ip-graph's `works.jsonl` so the site
   shows each work's honest translation state.

---

## THE WHY

The thesis specced "a full factorial state machine autonomously processing all works." `corpus_state.py`
is that machine — but only in OG patala. ip-graph's organism has no per-work T1/L2/C1 state. Wiring the
state machine into the organism is what makes ALL works process autonomously, and the inventory is what
tells the organism what exists vs what needs building.

---

## THE TEST

```bash
# show the real per-work state + next action for the Stk work
python3 -c "
import sys; sys.path.insert(0,'/root/projects/patala/pipeline')
from corpus_state import discover_works, next_valid_action
works = discover_works()
stk = [w for w in works if w.work_id == 'sardhatrisatikalottara']
if stk:
    print('Stk state:', stk[0].t1, stk[0].l2, stk[0].c1)
    print('next action:', next_valid_action(stk[0]))
else:
    print('Stk not in discover_works (it is a new work)')
"
```

**Pass when:** the organism advances each of the 111+ works through its legal FSM transitions
(SOURCE→T1→L0→L2→L200→C1→T3→COMPLETE), gated by review + integrity + Hermes, with the internal inventory
(71/11/28/63/63) as the honest state the site serves.
