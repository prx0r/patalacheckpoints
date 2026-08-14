# BUILD: THE HERMES ORCHESTRATION (the execution kernel + Agent-3 coordinator)

*2026-08-14 · status: WHAT TO BUILD (for agentgraph) · the precise build spec for Hermes as the execution
kernel — the REAL model client + the Agent-3 factory-coordinator design, referencing the ACTUAL files.*

---

## THE GAP

ip-graph's `hermes_exec.py` shells to `hermes -z`, but it's a thin wrapper. OG patala has the FULL Hermes
orchestration: the model client, the Agent-3 coordinator design, the MCP bridge, and the `patala_*` verbs.
This is the nervous system ip-graph's organism should be wired into.

---

## THE REAL HERMES FILES (reference these)

### 1. The model client (the real Hermes execution path)
**`/root/projects/patala/pipeline/model.py`**
- Drives the translator model VIA the Hermes agent (`hermes -z`), NOT a direct API call
- `DEFAULT_MODEL = "deepseek-v4-flash"`, `HERMES_BIN = "hermes"`
- `_hermes_call(prompt, model, timeout, retries)` — shells to `hermes -z` with model + provider, kills the
  process group on timeout (no orphaned hermes)
- `chat(system, user)` / `chat_agentic(system, user)` — the two real call paths
- **This is the same path ip-graph's `hermes_exec.py` mirrors** — the two should be unified

### 2. The Agent-3 factory-coordinator design (the orchestration)
**`/root/projects/patala/handover/hermes/HERMES-AGENT3-FACTORY-COORDINATOR.md`**
- Hermes **profiles** = the Agent 1/2/3 abstraction:
  ```bash
  hermes profile create patala-producer \
  hermes profile create patala-verifier \
  hermes profile create patala-coordinator \
  ```
- Hermes has a dedicated **orchestrator profile lane** (assigns profiles, schedules)
- The kanban orchestrator knows what each profile is good at

### 3. The other Hermes specs (the full orchestration picture)
| File | What it is |
|---|---|
| `handover/hermes/DEV-PLAN.md` | the Hermes build plan (execution kernel → the executable-corrections moat) |
| `handover/hermes/CANONICAL.md` | Hermes = replaceable execution kernel; Pāṭala = durable epistemic protocol |
| `docs/HERMES-ORCHESTRATION-REVIEW.md` | moving the built factory to Hermes |
| `docs/global/HERMES-CALLING.md` | how Pāṭala calls Hermes (the invocation) |
| `docs/agent3potential.md` | the Agent-3 case |
| `handover/hermes/BACKEND-MODEL.md` | the backend model |
| `handover/hermes/hermespatala-architecture-review.md` | the honest Hermes↔Pāṭala review |

### 4. The MCP bridge (the Hermes↔Pāṭala verbs)
**`/root/projects/patala/mcp/index.mjs`** — 29 tools, incl. the `patala_*` review verbs:
- `patala_get_review_state` · `patala_propose_review` · `patala_submit_review` · `patala_get_impact` ·
  `patala_simulate_review` · `patala_get_factory_status` · `patala_get_certificate`
- Plus the domain tools: `get_work`, `get_source_passage`, `resolve_ref`, `search_passages`, `verify_*`,
  `get_themes`, `get_related_works`, `concordance`, `get_manuscripts`, `get_history_timeline`

---

## WHAT TO BUILD (wire Hermes into the organism)

### The build:
1. **Unify `model.py` + `hermes_exec.py`** — one Hermes execution client both sides use. ip-graph's
   `hermes_exec.prompt()` already mirrors `model.py`'s `_hermes_call`; make them one.
2. **Wire the Agent-3 profiles** — the producer/verifier/coordinator profiles (from
   `HERMES-AGENT3-FACTORY-COORDINATOR.md`) drive the organism's refine/verify steps.
3. **The MCP bridge** — the organism's commit/serve calls the `patala_*` MCP verbs + the read-plane tools.
4. **The execution doctrine** — Hermes executes; Pāṭala decides. The organism's workers call Hermes via
   `model.py`; the reducers/gates decide what's canonical.

### The WHY:
Hermes is the execution kernel. The real model client + the Agent-3 coordinator + the MCP bridge ARE the
nervous system. Wiring the organism to them makes it actually GENERATE (Hermes) + coordinate (profiles) +
serve (MCP) — the full autonomous loop.

---

## THE TEST

```bash
# verify the real model client works (Hermes executes)
python3 -c "
import sys; sys.path.insert(0,'/root/projects/patala/pipeline')
from model import chat
print(chat('Reply with exactly: HERMES-OK', 'confirm')[:40])
"
# verify the MCP server loads (29 tools)
node -e "const m=require('/root/projects/patala/mcp/index.mjs'); console.log('MCP loaded')"
```

**Pass when:** the organism's refine() calls the real Hermes client (`model.py`/`hermes_exec.py`), the
Agent-3 profiles (producer/verifier/coordinator) drive the steps, and the `patala_*` MCP verbs expose the
result. Hermes executes; Pāṭala decides.
