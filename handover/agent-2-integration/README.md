# AGENT 2 — INTEGRATION LANE (handover index)

*The canonical documentation home for Agent 2 (the Autonomous Translation Factory / corpus compiler).
This README is the clean index — read the "READ FIRST" docs, then the deep references.*

**Role (the clean split):** `AGENT 2 = MAKE THE FACTORY RUN` · `AGENT 1 = PROVE THE FACTORY DESERVES
TRUST`. Agent 2 builds the canonical SOURCE→C1→(higher) factory; Agent 1 independently evaluates it.

---

## READ FIRST (the current state + how to operate)

| Doc | Why |
|---|---|
| **`CURRENT-STATE.md`** | the current operational state + honest limitations (Era A done, Era B running, Era C started) |
| **`DEV-PLAN.md`** | the canonical execution plan (Era A/B/C + the checkpoint ladder) |
| **`CANONICAL-LAYER-STACK.md`** | the LOCKED layer order + file types + dependency (do not reorder/rename) |
| **`ORIENTATION.md`** | the process workflow (the full context chain + gates) |
| **`CHECKPOINTS-INTEGRATION.md`** | this lane's checkpoints + the concrete sequence |

## The overnight pack (how to run it)

| Doc/File | Why |
|---|---|
| **`docs/FACTORY.md`** | the canonical reference for the whole autonomous factory (READ THIS) |
| `pipeline/start_overnight.sh` | ONE-COMMAND launcher (start/status/stop both systems + watchdogs) |
| `pipeline/OVERNIGHT.md` | the overnight runbook + morning checklist |
| `docs/SOURCE-PROCESS-OVERNIGHT.md` | the full code-level trace of an overnight run |

## Session build records (what was built + how to continue)

| Record | What it covers |
|---|---|
| **`BUILD-RECORD-2026-08-13-ERA-BC-OVERNIGHT.md`** | Era B (corpus compiler) + Era C (rebuild engine) + the overnight pack |
| **`BUILD-RECORD-2026-08-13-LAYER-TESTS.md`** | per-layer workers verified against the IPVV exemplars |
| **`BUILD-RECORD-2026-08-13-VERTICAL-WORKERS.md`** | the L0→C1 vertical + layer-specific validators |
| **`BUILD-RECORD-2026-08-12-AUTONOMY.md`** | the original autonomous-factory build |

## Reference architecture docs (in `docs/`)

- **`GOLD-STANDARD-MECHANISMS-AND-DATAFLOW.md`** — the gold mechanisms + full data flow + the two
  state systems (registry vs ledger)
- **`ML-VERIFIABLE-LAYER-CONTRACTS.md`** — the per-layer done-correct contracts (Tier A deterministic +
  Tier B ML) — the shared methodology
- **`agent2nextdev.md`** — the Era A/B/C roadmap

## The live cross-agent surface

- `live/agent2.md` — Agent 2's live current state
- `live/agent1.md` — Agent 1's verification-readiness view (what's ready for evaluation)

---

## How to continue (Agent 2)

1. Read `docs/FACTORY.md` + `CURRENT-STATE.md` + `DEV-PLAN.md`.
2. The factory runs overnight via `bash pipeline/start_overnight.sh start`.
3. Track progress: `python3 pipeline/catalog.py` (unified view) · `factory_status.py` (dashboard) ·
   `factory_certificate.py` (integrity).
4. Next work (Era C): A2-18 DependencyImpactReport + A2-19 ReviewBundle export.
