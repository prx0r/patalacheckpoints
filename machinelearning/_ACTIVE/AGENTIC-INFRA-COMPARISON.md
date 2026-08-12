# AGENTIC-INFRA COMPARISON — Gastown, LangGraph, Temporal, CrewAI, Mastra vs. Pāṭala's agent system

*2026-08-12. A grounded survey (READMEs fetched) of existing agentic infrastructure, compared to the
Pāṭala agent system (template `agent0` → live `instances`, `STATE.yaml`, `flow.py`, `check_staleness.py`).
The question: what FUNCTIONS are worth borrowing, and what is overengineering for Pāṭala? Honest
position up front: **Pāṭala's agent system is small and purpose-built; the value of these frameworks is
as a menu of functions, not as dependencies.**

---

## 1. WHAT WE COMPARED (grounded — READMEs read)

| System | What it is | The function most relevant to us |
|---|---|---|
| **Gas Town** (Steve Yegge) | Multi-agent **workspace manager** for Claude/Copilot/Codex | git-backed **persistent work state** (Beads ledger) + **identities** (persist across restarts) + **mailboxes/handoffs** + a coordinator ("the Mayor") |
| **LangGraph** (LangChain) | Low-level **stateful agent orchestration** | **durable execution** (resume from where it left off), checkpoints, memory, human-in-the-loop |
| **Temporal** | **Durable execution** engine | durable workflows — retries, state survival, versioning |
| **CrewAI** | Role-playing **autonomous agent** framework | role-based agents, task orchestration |
| **Mastra** | TS framework for AI agents | agent workflows, tooling |
| **OpenAI Agents SDK** | Agent building kit | handoffs, guardrails, tool calling |
| **OpenClaw** | "always-on agent OS" | persistent agent that acts across sessions |

---

## 2. THE DIRECT ANALOG (Gas Town is our closest cousin)

Gas Town's model maps almost 1:1 onto what we built:

| Gas Town | Pāṭala ours |
|---|---|
| **Town** (workspace) | `handover/` |
| **Rigs** (per-project containers) | per-lane handover dirs (`agent-1-ml/`, `agent-2-integration/`) |
| **The Mayor** (coordinator) | the **agent0 template's governance function** |
| **Polecats** (ephemeral workers, persistent identity) | live agent instances (`instance_of: agent0`) with persistent identity + ephemeral sessions |
| **Hooks** (git-worktree persistent state) | `STATE.yaml` + `history.log` (persistent, versioned) |
| **Beads ledger** (git-backed issue/state store) | `STATE.yaml` + `check_staleness.py` |
| **Mailboxes / handoffs** | `handover/LOG.md` cross-lane entries |

**The key insight we share with Gastown:** the hard problem is **context persistence across agent
restarts** — exactly what our `STATE.yaml` + per-instance `history.log` solve. Gastown persists work in
**git-backed hooks** (survives crashes); we persist in **versioned YAML + logs** (survives session ends).
Conceptually identical, ours is lighter.

---

## 3. FUNCTIONS WORTH BORROWING (genuinely useful to Pāṭala)

Ranked by real leverage for Pāṭala, not by framework popularity:

### 3a. **Git-backed durability (Gas Town)** — the highest-value borrow
Gas Town's core trick: work state lives in **git**, so an agent crash/restart loses nothing. **We already
have git.** The upgrade: make `STATE.yaml` + `history.log` + `INDEX.md` **a first-class git-tracked
"ledger"** so a restarting agent *git-reverts/reads* its own last state rather than trusting memory.
This is a **policy + one command**, not a dependency.

### 3b. **Identity that persists across sessions (Gas Town Polecats)** — we already have this
"persistent identity, ephemeral session." Our instances have persistent `id` + `history.log`. **We have
it; formalize it** (each `SESSION-<date>.md` links to the instance's persistent identity).

### 3c. **Mailboxes / typed handoffs (Gas Town)** — a real gap, cheap to add
Gas Town routes work between agents via mailboxes. We use `LOG.md` but it's a flat log, not routed.
**Borrow:** a lightweight `handover/inbox/<from>→<to>/` convention OR a `handoff` subcommand in
`flow.py` (`flow.py handoff <from> <to> "<what> <file> <schema>"`). **Small, high-value.**

### 3d. **Durable "resume from where you left off" (LangGraph/Temporal)** — conceptually already ours
Our `flow.py status` + `STATE.yaml` IS "resume from where you left off" at the checkpoint level. We do
NOT need Temporal's full durable-workflow engine (that's for long-running compute workflows, not a
research agent system). **Skip the dependency; keep the concept.**

### 3e. **Human-in-the-loop (LangGraph interrupts)** — we already have this
Our `review_state` ladder (SINGLE_REVIEWED → DOUBLE_REVIEWED → ADJUDICATED) + the gate's `needs_review`
IS human-in-the-loop. **Already there, more scholarly than LangGraph's.**

---

## 4. FUNCTIONS THAT ARE OVERENGINEERING FOR PĀṬALA (do NOT borrow)

| Function | Why it's overkill for us |
|---|---|
| **Temporal durable-workflow engine** | built for long-running distributed compute; our state is tiny and git-resident |
| **Full LangGraph graph executor + LangSmith tracing** | we don't need a runtime graph executor; our "graph" is the scholarly IR, not agent control flow |
| **CrewAI role-play + task delegation** | our agents are few (2 live + template), not a crew; role-play adds ceremony |
| **Mastra / OpenAI SDK agent tooling** | we don't build agents that call tools at runtime; we build *research* agents |
| **OpenClaw always-on agent** | Pāṭala agents work in sessions, not as a daemon |
| **Vector memory / long-term store** | our "memory" is the scholarly corpus + gold, already structured |
| **Multi-agent chat/debate (ACAL-style)** | we evaluate arguments, we don't run agent debates (yet — and that's a scholarly decision, not infra) |

**The principle (from our own doctrine):** Pāṭala's agent system is *infrastructure to keep scholarship
honest*, not a general agent platform. The frameworks are useful as a **menu of functions**, not as
dependencies.

---

## 5. HOW THIS BECOMES USEFUL TO PĀṬALA AS AN AUTONOMOUS SYSTEM

The honest path — what an autonomous Pāṭala needs vs. what the frameworks actually offer:

### What an autonomous Pāṭala actually needs
```
A controller that can:
  1. WAKE UP (session start) and know its full state  → flow.py status + STATE.yaml (HAVE)
  2. KNOW its lane + checkpoint + next step            → the instance orientation (HAVE)
  3. DO THE WORK (build gold, run extraction, gate)    → the lane's actual ML work (HAVE the machinery)
  4. RECORD progress durably (versioned, attributed)   → flow.py update + history.log (HAVE)
  5. HAND OFF to the other lane cleanly                → LOG.md + handoff (PARTIAL — add the handoff fn)
  6. SURVIVE a restart with no memory                  → git-backed state (HAVE, make it the discipline)
  7. NOT OVERCLAIM — every result is a BenchmarkRun    → the doctrine + CLAIMS.md (HAVE)
```

**Pāṭala is ALREADY 90% an autonomous agent system** — the missing 10% is the **typed handoff** and
making **git-backed durability** an explicit discipline. That's the difference between "docs we maintain"
and "a system that resumes itself."

### The one genuinely new function to add (cheap, no dependency)
**`flow.py handoff <from> <to> "<what> <file> <schema>"`** — a typed, logged, versioned handoff that:
1. appends to `LOG.md` (what · why · file · direction · schema),
2. appends to the receiving instance's inbox,
3. bumps the state version.

That's the single borrow that makes cross-lane autonomy real, and it's ~30 lines.

---

## 6. THE ONE-SENTENCE CARRY-FORWARD

**Gas Town is our closest cousin — it confirms our design (persistent identity + git-backed state +
a coordinator) is the right shape, and the one function worth borrowing is the typed handoff
(`flow.py handoff`) plus making git-backed durability explicit. LangGraph/Temporal/CrewAI solve problems
we don't have (durable compute, agent crews) and would be overengineering as dependencies. Pāṭala is
already ~90% an autonomous research agent system; the honest move is to add the handoff function and
stop there — not to import a platform.**
