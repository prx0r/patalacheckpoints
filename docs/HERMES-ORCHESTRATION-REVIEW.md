# HERMES ORCHESTRATION REVIEW — moving the built factory to Hermes

*2026-08-13. Review of the previous Hermes×Pāṭala specs, and how the autonomous factory we just built
(Agent 2, the corpus OS) maps onto the Hermes orchestration plan. This is a REVIEW + MAPPING — no
implementation. It links the relevant docs so a future agent can execute the integration.*

---

## 0. THE SPECS WE ALREADY PLANNED (the docs)

| Doc | What it specifies | Location |
|---|---|---|
| **The integration (CANONICAL)** | Thesis: **Hermes = replaceable execution kernel; Pāṭala = durable epistemic state**. Hermes schedules/executes; never determines what Pāṭala knows. The 4 corrections (kanban≠constitution, memory≠epistemic state, checkpoints≠rollback, hooks-trigger-not-determine). The 3 integrations to build first. | `handover/hermes/CANONICAL.md` |
| **The build plan (DEV-PLAN)** | Phase 1 execution kernel (profile + MCP verbs) → Phase 2 A3 factory on kanban+cron → Phase 3 ReviewEvent-as-graph-mutation → Phase 4 Scholar Workbench → Phase 5 BYOA/corrections dataset. Each with a GATE. | `handover/hermes/DEV-PLAN.md` |
| **The thesis + README (index)** | Hermes = execution; Pāṭala = scholarly memory of record. The 3-way separation (Hermes memory = operator, sessions = history, Pāṭala graph = truth). | `handover/hermes/README.md` |
| **The northstar** | RAW-L0 (MODE_B) → blind IPVV replay → unleash on Kramasadbhāva → batch. (Now done.) | `handover/hermes/AUTOTRANSLATE-NORTHSTAR.md` |
| **Setup** | Fresh Hermes profile/project + the Pāṭala "soul" plan. | `handover/hermes/PATALA-SETUP.md` |
| **Architecture review + layers** | The canonical stack as compiler passes + the 3-states-per-layer doctrine. | `handover/hermes/hermespatala-architecture-review.md`, `hermespatalalayers.md` |

**The governing principle (from CANONICAL.md + DEV-PLAN):** Hermes must be **replaceable**. If it
vanished, Pāṭala retains every source, claim, review, provenance chain, and status. Hermes holds
execution/workflow state; Pāṭala holds scholarly truth. The `patala_*` tools enforce "AI proposes ≠
Pāṭala asserts" at the tool boundary.

---

## 1. WHAT WE BUILT (Agent 2, this session) THAT THE SPECS CALLED FOR

The factory we built **is** the A3 translation-factory loop the specs envisioned — but as a standalone
`factory_loop.sh` daemon, NOT yet driven by Hermes kanban/cron.

| Spec (DEV-PLAN Phase 2) | What we built | Status |
|---|---|---|
| "Kanban + cron supervisor — Hermes IS the supervisor, no bespoke auto_run.py" | `factory_loop.sh` (repeat-loop) + `factory_loop_watchdog.sh` (cron) + `factory_scheduler.py` (DAG) | **built, but as our own daemon, not Hermes kanban/cron** |
| "Run NEXT_VALID_ACTION for the top eligible work" | the DAG scheduler does exactly this (registry-derived eligibility) | ✅ built |
| "execute via model.py → T1→L2→C1, auto-validated, MACHINE_PROPOSED, written back to ledger" | the factory does exactly this (workers → validators → registry.commit) | ✅ built |
| "validation gate; stop on failure (fail-closed)" | the layer validators + failure/retry queue | ✅ built |
| "cron → scheduled A3 jobs" | our own `factory_loop_watchdog.sh` cron | built, but not `hermes cron` |

**So: the *execution* the specs wanted Hermes to run already exists as standalone Python.** The gap is
**the orchestration layer** — moving the factory from "a detached shell loop" to "Hermes kanban/cron
driving the `patala_*` MCP verbs."

---

## 2. WHAT'S MISSING to make it Hermes-orchestrated (the gap)

### 2.1 The `patala_*` MCP capability layer (spec'd, NOT built)
CANONICAL.md recipe #6 + DEV-PLAN Phase 1.3 specify graph-as-verbs:
```
READ:  patala_resolve · patala_get_work_state · patala_get_passage · patala_get_grounding
       patala_get_dependencies · patala_next_action · patala_query_theme · patala_get_open_cruxes
WRITE: patala_propose_translation · patala_propose_alignment · patala_propose_annotation
       patala_record_review · patala_mark_stale
NO:    patala_accept_claim / patala_set_truth (never exist)
```
**Current state:** the MCP server (`mcp/index.mjs`) has essentially **one `patala` tool**; there is no
`patala_next_action` / `patala_get_work_state` / `patala_propose_translation`. **This is the single
biggest gap** — it's what turns lane ownership into permissions and lets Hermes query/advance Pāṭala
without touching files.

### 2.2 Hermes kanban/cron as the supervisor (spec'd, not wired)
- `hermes kanban init` + `hermes cron create` (DEV-PLAN Phase 2.1) would drive the factory, replacing our
  bespoke `factory_loop.sh`. The specs are explicit: **"Hermes IS the supervisor; no bespoke
  auto_run.py needed."**
- But: our `factory_loop.sh` already implements the DAG/retry/resume/watchdog subset. Per the A3 peer
  review, **don't migrate to Hermes kanban until the execution semantics are solid** — and even then,
  Hermes owns *who does what / workflow finish*, Pāṭala owns *validity*.

### 2.3 The `patala` Hermes profile + external skill dir (spec'd, not set up)
CANONICAL.md PART IV-A: point Hermes at `patala/skills/` as an external skill dir, and create a
`patala` profile. Not done.

---

## 3. THE MAPPING (how what we built slots in)

```
                HERMES (execution kernel — kanban/cron/hooks/mcp/skills)
                     │  drives via patala_* MCP verbs   (TO BUILD: the MCP capability layer)
                     ▼
        ┌────────────┴────────────┐
        ▼                         ▼
   patala_next_action       patala_propose_translation
   (read eligibility)       (write MACHINE_PROPOSED)
        │                         │
        ▼                         ▼
   OUR EXISTING FACTORY (the execution, already built):
   factory_scheduler.py (DAG) → factory_batch.py (workers+validators)
   → object_registry.commit → factory-audit.jsonl → catalog.py
        │
        ▼
   PĀṬALA EPISTEMIC CORE (registry + ledger + audit + catalog — the truth)
```

**The clean division (matches CANONICAL):**
- **Hermes** = kanban scheduler + cron + hooks + skills + sessions (workflow state). Replaceable.
- **Pāṭala** = registry + ledger + audit + catalog + validators (scholarly truth). Durable.
- **The bridge** = the `patala_*` MCP verbs (PROPOSE/RECORD, never ACCEPT).

**Our factory becomes the "A3 worker profile"** — a Hermes role whose jobs are "read `patala_next_action`,
propose translation, validated, MACHINE_PROPOSED, write back" — instead of a detached Python daemon.

---

## 4. RECOMMENDED INTEGRATION ORDER (execution-safe)

Per the peer-review (agent3potential.md) + these specs, the correct sequence:

1. **First: A2-ARCH-HARDEN** (reconcile the DAG + the registry immutability overclaim) — before wiring
   orchestration, the execution semantics must be correct. (Review: `docs/agent3potential.md`.)
2. **Build the `patala_*` MCP capability layer** — the highest-value, spec'd, NOT-built piece. Expose
   `patala_next_action`, `patala_get_work_state`, `patala_propose_translation` as verbs reading/writing
   our existing registry + ledger. This is what makes Hermes able to drive Pāṭala.
3. **Create the `patala` Hermes profile + external skill dir** (CANONICAL PART IV-A).
4. **Run the factory via `hermes kanban` + `hermes cron`** (DEV-PLAN Phase 2.1) — the supervisor becomes
   Hermes; our `factory_loop.sh` becomes the underlying A3 worker (or a `patala_run_factory` skill).
5. **Then Phase 3**: ReviewEvent-as-graph-mutation + dependency recomputation (the moat).
6. **Then Phase 4-5**: Scholar Workbench + BYOA/corrections dataset.

---

## 5. THE GUARDRAILS (from the specs — do not violate)

1. **Hermes never determines what Pāṭala knows.** All epistemic state lives in Pāṭala (registry/ledger/
   audit). Hermes holds operator doctrine + execution history only.
2. **No tool can set truth/accept.** Only PROPOSE/RECORD verbs; the `patala_accept_claim` tool must
   never exist.
3. **Kanban = scheduler, not constitution.** Pāṭala owns `MACHINE_PROPOSED ≠ ACCEPTED`, supersession,
   reviewer identity, scope.
4. **Hooks trigger integrity machinery; they don't determine it.** The dependency/staleness logic is
   Pāṭala's; Hermes wakes it.
5. **Do NOT build** Temporal/LangGraph/CrewAI/a custom scheduler/a bespoke workflow engine. Hermes runs
   the jobs; Pāṭala owns the state.
6. **Don't require scholars to install Hermes.** They use the Workbench / MCP.

---

## 6. VERDICT / CARRY-FORWARD

- **The specs exist and are comprehensive** — the Hermes orchestration plan was fully designed in
  `handover/hermes/CANONICAL.md` + `DEV-PLAN.md` (2026-08-12).
- **We built the execution** the specs wanted Hermes to run, but as a standalone Python daemon, not yet
  Hermes-orchestrated.
- **The bridge is the `patala_*` MCP capability layer** — currently almost absent (one tool). Building
  it + the `patala` profile + pointing Hermes kanban/cron at the factory is the concrete path to
  "Hermes orchestrates what Agent 2 built."
- **Do the A2-ARCH-HARDEN first** (the DAG + immutability fixes from the peer review), then the MCP
  layer, then the kanban/cron migration.

**Key docs to link:** `handover/hermes/CANONICAL.md` · `handover/hermes/DEV-PLAN.md` ·
`handover/hermes/README.md` · `handover/hermes/AUTOTRANSLATE-NORTHSTAR.md` ·
`docs/agent3potential.md` (peer review) · `docs/FACTORY.md` (what we built) ·
`docs/GOLD-STANDARD-MECHANISMS-AND-DATAFLOW.md` (the state systems).
