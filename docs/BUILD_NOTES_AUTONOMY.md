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
