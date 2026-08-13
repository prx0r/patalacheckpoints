# AGENT 2 — INTEGRATION LANE (handover index)

*The canonical documentation home for Agent 2 (the Autonomous Translation Factory / corpus compiler).
This README is the clean index — read the "READ FIRST" docs, then the deep references.*

**Role (the clean split):** `AGENT 2 = MAKE THE FACTORY RUN` · `AGENT 1 = PROVE THE FACTORY DESERVES
TRUST`. Agent 2 builds the canonical SOURCE→C1→(higher) factory; Agent 1 independently evaluates it.

---

## READ FIRST (the current state + how to operate)

| Doc | Why |
|---|---|
| **`HANDOVER-2026-08-13-LATE-SESSION.md`** | **the latest handover** — full current state + live systems + next work (READ THIS first) |
| **`CURRENT-STATE.md`** | the current operational state + honest limitations (Era A done, Era B done, Era C started) |
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

## The Atlas / foundation work (the current forward plan — READ THIS)

Agent 2's next cycle is **building the Pāṭala Atlas foundation properly first** (do B, then one vertical),
while the running factory stays untouched. Everything you need:

| Doc/File | What it is |
|---|---|
| **`docs/AGENT2-ATLAS-FOUNDATION-PLAN.md`** | **THE active next-cycle plan.** Do B (foundation) first: Postgres Atlas (I1) + R2 asset store (I2) + OpenAlex-grammar API (I4), then one vertical (Brahmayāmala / Dviśatikālottara). DB locked to Postgres. The old `AGENT2-NEXT-DEVPLAN.md` (sivaqueue intake) is superseded. |
| **`openpatala/README.md`** | **The "OpenAlex for Sanskrit" build folder.** Home of the Atlas; imported OpenAlex reference docs under `openpatala/reference/openalex/`. |
| **`docs/vision/vision-15-patala-atlas-sanskrit-research-graph.md`** | The Atlas **strategy** (Vision 15). |
| **`docs/vision/atlas/atlas-engineering-blueprint.md`** | The Atlas **build blueprint** (storage: Postgres=R2=event log; I1–I6). |
| **`docs/vision/atlas/atlas-cloudflare-edge-layer.md`** | The **Cloudflare edge layer** (Neon/Postgres canonical, Workers API + Hyperdrive + Cache + R2, factory stays self-hosted). |
| **`docs/vision/source-resolution/source-resolver-design.md`** | The **reconciliation authority stack** (NCC/NMM/NGMCP/GRETIL/SARIT/Muktabodha + catalogs + IIIF). |
| **`docs/vision/functionality/research/2026-08-12/06_ATLAS/RESEARCH_AND_BUILD.md`** | The **endgame-build** project doc for the Atlas. |

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
