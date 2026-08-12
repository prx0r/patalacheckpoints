# BUILD NOTES — the generic autonomy controller (2026-08-12)

Per `hermespatalalayers.md` + `hermespatala-architecture-review.md`. The autonomous factory is now a
**generic controller over the canonical L0→L2→L200→C1→THEME→ESSAY DAG**, not a T-flow or an LLM
orchestrator. This is the first vertical: the controller + per-layer registries + re-mapped skills.

## What was built

### `pipeline/object_registry.py` — generic per-layer immutable registry
- Append-only JSONL per layer: `data/corpus/registries/<layer>-registry.jsonl`.
- Canonical layers + prerequisites (`PREREQS`): SOURCE, L0, L1, L2, L200, C1, THEME, ARGUMENT, SYNTHESIS,
  ESSAY, EDUCATION.
- **Three-state ladder** per object: `GENERATED → ENGINEERING_VALIDATED → SPECIALIST_REVIEWED`.
- `commit` (immutable, supersedes prior, old versions stay citable) · `current` · `versions` ·
  `is_committed` (**idempotency by input_hash, never byte-identical output**) · `set_status` ·
  `supersede` (cascading stale) · `objects_at_status`.

### `pipeline/autonomy.py` — the deterministic controller (the cron heartbeat)
- `eligible_for(layer, object_id, input_hash)` — ordinary code (prereqs committed, this layer not current).
- `find_eligible` · `tick` (lock → inspect registries → compute eligible → bounded batch → dispatch layer
  handler → validate → COMMIT/REJECT → detect stale/supersede → run report) · `acquire_lock` (flock).
- Layer-agnostic: `LAYER_HANDLERS` maps each layer to `{skill, generator, validator}`; L0 wires the built
  factory, others use the layer-skill prompt + deterministic validator hook.
- Run reports to `data/corpus/downloads/autonomy-reports/`.

### Canonical layer skills (re-mapped to the real stack)
`skills/autonomous-layer/patala-autonomous-layer-skills/skills/`:
- **controller** + **L0** (existing) + **L1** · **L2** (semantic-fidelity: `content(L2) ⊆ content(L1)+supplies`)
  · **L200** (the audit: 8-section, MT/IA split, Task-2 fidelity — the highest-value certificate) ·
  **C1** · **THEME** (evidence-backed, not cluster=theme) · **ESSAY** (proof-carrying prose) ·
  **EDUCATION** (authority ≤ source).
- Removed the retired **T1/R1/T2/R2/T3/T3.1** skills. `LAYER_MATRIX.md` + `manifest.json` updated to the
  canonical stack.

## Verified
- `object_registry.py` + `autonomy.py` compile; `autonomy.py --dry-run` runs and emits a report.
- DAG test: L0 commit → L1 eligible; L1 commit → L2 eligible; idempotency (already-committed skipped);
  supersession (L1 stale → downstream eligible); three-state ladder.

## Honest state
- The **generic skeleton + L0 wiring + registries + skills** are built and tested in the deterministic
  core. The per-layer **generative generators** (L2/L200/C1/THEME/ESSAY model calls) and their real
  validators are **hooked but not yet exercised** — they're wired to `generic_generator`/
  `generic_validator` stubs. Real L200/C1 generation + their validators are the next layer work.
- Open gates unchanged: **L0 canary** and the **factory certificate** before any unattended scale.

## Next (per the build order)
L0 controller canary → L0 certificate → L2 generator+validator → **L200** (generator + Task-2 validator) →
C1 → supersession propagation → THEME → connect Argument/Synthesis → ESSAY → EDUCATION.

---

## TEST RESULTS (2026-08-12, fail-fast)

`pipeline/test_autonomy.py` — **16/16 PASS** (registry commit/current/idempotency/three-state · eligibility
DAG · controller find_eligible + tick + run report · supersession/cascading-stale). `pipeline/test_autonomous.py`
(F1/F4/F6) — **7/7 PASS**.

**Fail-fast note:** the first run surfaced 2 failures — a **test-ordering bug, not a code bug**: the test
superseded L1 *before* asserting L2 eligibility, and the controller **correctly** blocked L2 (its prereq L1
was stale). Reordered the test to assert L2 eligibility/commit while L1 is valid, then assert the
supersession cascade afterward. This is exactly the behavior the architecture wants: a stale upstream blocks
downstream eligibility.

Run:
```bash
python3 pipeline/test_autonomy.py    # 16/16
python3 pipeline/test_autonomous.py  # 7/7
```

---

## L0 CANARY + L200 WORKER (2026-08-12) — proven

### L0 canary (controller drives real L0 production)
`pipeline/l0_worker.py` wires the controller's L0 handler to the real RAW-L0 factory (deterministic
Vidyut + agentic batch gloss → `validate_l0_spec` → commit). Ran the controller `tick` on 3
kramasadbhāva passages:
- **2 committed** (`v1`,`v3`) with real PARSED glossed records (e.g. aśarīrāḥ→"bodiless (ones)").
- **1 failed** (`v2`) — the OCR-noise verse (`* * * * * * * *`), correctly rejected by validation (fail-closed).
- Proof that the controller drives end-to-end L0 production via the layer handler.

### L200 worker (the audit compiler)
`pipeline/l200_worker.py` — partly deterministic (identification, published reading, derivation map
from refs, source-layer, cross-refs, review state) + model-proposed MT/IA/open-items. The **Task-2
validator** enforces: all required sections, MT classified (not IA), refs typed, source-layer tagged.
Ran through the controller: **L200 committed** with the full 8-section audit + derivation map; **idempotent**
(second tick skips).

### Worker tests
`pipeline/test_workers.py` — **8/8 PASS** (L0 validator fail-closed · L200 8-section generator · Task-2
validator pass/bad-MT/missing-source-layer · controller L200 commit · persistence · idempotency).

**Honest note:** the model-proposal layers (batch gloss for L0; MT/IA for L200) are stubbed in the tests
(hermes can hang — fail-fast). The deterministic scaffolds + validators are fully exercised; real model
calls are the generative layer, wired but exercised separately in the canary (L0 gloss) and pending for
L200 MT/IA at scale.

Run: `python3 pipeline/test_workers.py` · `test_autonomy.py` · `test_autonomous.py`.

---

## UPDATE (2026-08-12, later) — ModelAdapter + autonomous RAW-L0 re-anchor

**Re-anchor:** Agent 2 is back on autonomous RAW-L0 (the original goal). L200 is secondary until
autonomous RAW-L0 v1 is proven.

- **`pipeline/model_adapter.py`** — the ModelAdapter boundary: `DirectModelAdapter` (~1.4–2.1s, structured
  JSON via OPENCODE_GO_BASE_URL/API_KEY) + `HermesAdapter` (fallback) + `complete_batch_json` (strict
  object_id + input_hash binding, reject missing/wrong/duplicate/unknown, fail-closed partial).
- **Gloss wired to the adapter** — `agentic_gloss.py` batch gloss now routes through
  `get_adapter()` (Direct fast path). This attacks the RAW-L0 gloss nondeterminism + latency.
- **Autonomous RAW-L0 runs**: 11/12 kramasadbhāva passages committed through the controller (real glossed
  L0), 1 fail-closed. The Direct adapter should close the remaining reliability gap.

**Still needed (per PROGRESS-AUTONOMOUS-2026-08-12.md):** prove a real unattended batch on the Direct
adapter in the background; freeze autonomous RAW-L0 v1; then L200 candidate→classifier + TEST; then C1.

**File map + agent-1 handover + working-practice note:** `handover/agent-2-integration/PROGRESS-AUTONOMOUS-2026-08-12.md`
(single current-state map).
