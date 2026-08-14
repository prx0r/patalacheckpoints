# BUILD: WHAT WE DROPPED + THE CORRECT HERMES INVOCATION (rebuild the agent system right)

*2026-08-14 · status: THE COURSE-CORRECTION · what was dropped from the OG spec (agent 0, agent-3 kanban,
the A4-A8 architecture, the Hermes-executor moat) + the correct Hermes invocation. Read this before
building any agent/orchestration layer.*

---

## 1. THE CORRECT HERMES INVOCATION (`chat`, NOT `-z`)

**THE ONE RULE (from `docs/global/HERMES-CALLING.md`):**
> **`hermes -z "<prompt>"` is blind.** It is one-shot text completion with no file access, no tools, no
> skills (~3.8% yield on translation). **Use `hermes chat` (agentic)** — Hermes as an agent with file
> access + the Pāṭala skills.

**The correct invocation (agentic):**
```bash
hermes chat -Q -q "<ask>" --skills <skill> --yolo --max-turns 8
```
- `-Q` — quiet/programmatic mode (clean output for parsing)
- `--skills <skill>` — load a house skill (requires the `patala` profile)
- `--yolo` — unattended
- `--max-turns 8` — enough for the skill's inspection

**In code:** `pipeline/model.py`'s `chat_agentic()` does this correctly:
```python
cmd = [HERMES_BIN, "chat", "-Q", "-q", prompt, "--yolo",
       "--max-turns", str(max_turns), "-m", DEFAULT_MODEL, "--provider", provider]
```
`t1_worker.py` uses `chat_agentic` (line 41, 394). **This is the CORRECT path.**

### What's WRONG
- **ip-graph's `hermes_exec.py` uses `-z`** (`cmd = [HERMES_BIN, "-z", prompt, "-m", model, "--provider", provider]`) — blind, the old bug. It should use `chat` agentic.
- **agentpatala's `translate_passage.py` used `chat()`** (which shells to `-z`) — should use `chat_agentic()`.

---

## 2. WHAT WE DROPPED (from the OG spec)

### Agent 0 (the coordinator) — SPEC'D, NOT RUNNING
- `handover/agent0-coordinator/INDEX.md` + `AGENT-ARCHITECTURE-VISION.md` — the A0-A8 architecture.
- A0 governs the agent system (not a scholarly lane): the `AGENTS.yaml` registry, `check_staleness.py`,
  `CHECKPOINTS.md` (the CP0-CP4 gates).
- **Status:** documented as the coordinator, but no actual A0 agent operates it.

### Agent-3 kanban orchestration — SPEECCED, NOT BUILT
- `handover/hermes/HERMES-AGENT3-FACTORY-COORDINATOR.md` — fully specs:
  - The 3 profiles: `patala-producer`, `patala-verifier`, `patala-coordinator`
  - The **orchestrator profile lane** (kanban tools, but EXCLUDES implementation tools so it doesn't do
    the workers' jobs)
  - Kanban task-links/dependencies + the LLM decomposer (one task → child-task graph)
  - `orchestrator_profile` to own decomposition
- **Status:** only the `patala` profile exists (`hermes profile list` shows default + patala). The
  coordinator/producer/verifier profiles + the kanban orchestrator were NEVER created.

### The A4-A8 architecture — DEFERRED
- AGENTS.md: "Only A0-A3 need to exist now; the rest instantiate when the substrate makes their job real."
- A4 (review), A5 (synthesis), A6 (projection), A7 (scholar network), A8 (acquisition) — deferred.

### The Hermes-as-executor + scholar-peer-review moat — SPEC'D, NOT BUILT
- `handover/hermes/CANONICAL.md` — Hermes = REPLACEABLE execution kernel, NOT epistemic backend.
- `handover/hermes/DEV-PLAN.md` — the 5-phase build.
- `handover/hermes/PEER-REVIEW.md` — the executable-corrections system (review = a graph mutation with
  provenance).
- **Status:** specced; the peer-review moat (the product) is not built.

---

## 3. WHAT TO REBUILD (in the right order)

### Priority 1 — Fix the invocation (adopt `chat_agentic`)
- `hermes_exec.py` (ip-graph): change `-z` → `chat` agentic (`-Q -q --yolo --max-turns 8`).
- `translate_passage.py` (agentpatala): change `chat()` → `chat_agentic()`.
- **Why:** `-z` is the ~3.8% yield bug; `chat` agentic is the correct, working path (verified live).

### Priority 2 — Build the Agent-3 orchestration (the kanban build we specced)
- Create the 3 profiles: `hermes profile create patala-producer/verifier/coordinator`.
- Wire the **orchestrator profile lane** (kanban + decomposition, no implementation tools).
- **Why:** this is the autonomous factory coordination we specced but never built. The organism's
  producer/verifier/coordinator lanes should be Hermes profiles driving the real factory.

### Priority 3 — Activate Agent 0 as a running coordinator
- The A0 coordinator (AGENTS.yaml registry + staleness checker + checkpoint gates) should actually run
  and route the A1/A2/A3 lanes.

### Priority 4 — Build the scholar-peer-review moat (the product)
- `handover/hermes/PEER-REVIEW.md` — review = a provenance-carrying graph mutation. The Scholar API +
  adversarial review (which we verified works) wired to the live ledger.

---

## THE TEST (correct invocation)

```bash
# the CORRECT agentic call works (verified)
python3 -c "
import sys; sys.path.insert(0,'/root/projects/patala/pipeline')
from model import chat_agentic
print(chat_agentic('Reply with exactly: AGENTIC-WORKS', 'confirm')[:40])
"
# verify the 3 profiles exist
hermes profile list
# → should show patala-producer, patala-verifier, patala-coordinator
```

**Pass when:** the agent-3 profiles exist, the orchestrator lane runs the factory via kanban, the
coordinator (A0) routes the lanes, and all generation uses `chat_agentic` (NOT `-z`).
