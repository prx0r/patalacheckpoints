# HERMES AS PĀṬALA'S BACKEND INFRASTRUCTURE — the full model

> **⚠ SUPERSEDED THESIS — see the CANONICAL doc `hermespatala.md`.** This file's feature map (verified
> 2026-08-12) is retained as reference, but its original thesis ("Hermes IS the kernel/A0 runtime") was
> **corrected** by `hermespatala3.md`: **Hermes is Pāṭala's REPLACEABLE execution kernel, NOT its epistemic
> backend.** The feature inventory below (kanban/worktree/cron/hooks/memory/checkpoints/mcp/fallback/
> skills/sessions) is accurate; the epistemic-authority framing is not. Read `hermespatala.md` for the
> corrected, canonical architecture.

*2026-08-12. How Hermes (the agentic framework already configured on this machine) realizes the ENTIRE
Pāṭala vision — not just the translation factory, but the Agent 0 governance layer, the git/worktree
discipline, the corpus state machine, the review loop, and the multi-agent architecture. Every feature
named below was verified against `hermes --help` / subcommand help on 2026-08-12. This is the model; it
tells us what Hermes already provides so we DON'T re-build it.*

---

## THE THESIS

> **Hermes is not "a model wrapper we shell out to." It is Pāṭala's agentic backend. It already implements
> the A0 governance primitives (durable task board, isolated worktrees, scheduled jobs, event hooks,
> memory, rollback) that the agent-architecture vision specced as bespoke build work. Pāṭala's job is to
> layer its EPISTEMIC STATE (the doctrine, the corpus ledger, the gold) on top, not to rebuild the agent
> runtime.**

The mapping: **Hermes = the kernel/scheduler/constitution runtime** · **Agent 2's `corpus_state.py` =
the epistemic state** · **Pāṭala's skills = the doctrine encoded as executable procedure.**

---

## FEATURE → VISION REALIZATION (verified, feature by feature)

### 1. `hermes kanban` — the AGENT 0 ORCHESTRATION LAYER (the single most important)
*Verified: durable SQLite task board, shared across profiles; tasks claimed atomically, can depend on
other tasks, executed by a NAMED PROFILE in an ISOLATED workspace.*

This is **Agent 0's scheduler/constitution made real**:
```
Board per project (one for Patala)
  ├── tasks with dependencies (kanban create / link / block)
  ├── atomic claim (no two agents grab the same work)
  ├── executed by a named profile (kanban assign → profile) in an isolated workspace (--worktree)
  └── durable + auditable (SQLite, log/runs/heartbeat)
```
**This replaces bespoke "typed handoff" + "lane ownership" + "priority/gating"** we specced in the agent
vision. A3 translation job = a kanban task claimed by the `patala` profile; its dependency = "L0 VERIFIED"
(from Agent 2's ledger); its executor runs in an isolated worktree.

### 2. `hermes --worktree` — THE GIT-ISOLATION FIX (root cause of INCIDENT-2026-08-12-01)
*Verified: `--worktree, -w` = "Run in an isolated git worktree (for parallel agents)."*

**This is the per-agent worktree we documented in GIT-INCIDENTS.md — built-in.** Each agent/profile runs
in its own git worktree, so Agent 1 can never stage Agent 2's files (they're not in its worktree). The
`agent identity ↔ worktree path ↔ branch` invariant is enforced by Hermes itself. We don't need to hand-run
`git worktree add` — Hermes does it per invocation.

### 3. `hermes cron` — THE "TRANSLATE WHILE I SLEEP" SCHEDULER
*Verified: `cron create <schedule> <prompt> --skill --workdir --deliver`.*

```
cron create "0 2 * * *" "Run NEXT_VALID_ACTION for the top eligible work" \
  --skill patala-translate --workdir /root/projects/patala-agent2
```
Scheduled jobs that: read Agent 2's ledger (`/api/corpus/state`), execute the eligible translation work,
and deliver the report (origin/local/telegram/discord/signal). **This is the A3 factory loop, natively
scheduled.**

### 4. `hermes hooks` + `hermes webhook` — EVENT-DRIVEN GOVERNANCE
*Verified: shell hooks in config fired on events (with allowlist/consent); webhook subscriptions for
event-driven agent activation.*

- **Hooks** = "when an artifact lands / when a checkpoint crosses → fire a Pāṭala validation script."
- **Webhook** = "when the corpus source changes / when a review is due → activate the right agent."
This wires the **dependency/staleness propagation** (Agent 2's responsibility from the vision): a source
change triggers a hook that invalidates the L0 proof + downstream artifacts.

### 5. `hermes memory` + `memory-graph` — DURABLE EPISTEMIC MEMORY
*Verified: built-in MEMORY.md/USER.md always active; external providers (mem0, honcho, ...) optional;
memory-graph = timeline of learned skills/memories.*

- The **Pāṭala soul** = the profile's personality + MEMORY.md seeded with the doctrine.
- memory-graph = the project's "what we've learned / what state we're in" — replaces ad-hoc session notes.
- We use **built-in** memory (not an external provider) — no over-engineering.

### 6. `hermes checkpoints` — ROLLBACK / THEATER-GUARD
*Verified: shadow-git snapshots the working dir before write/patch/terminal calls.*

Every Pāṭala write is snapshotted → a bad translation/regeneration can be rolled back. This is the
mechanical guard behind "mistakes don't compound" — if Agent 3 produces garbage, `checkpoints` undoes it.

### 7. `hermes mcp` + the `tantrakosa` server — THE CORPUS AS TOOL SURFACE
*Verified: MCP config has a `tantrakosa` server → `patala/mcp/index.mjs` (21 tools).*

Hermes agents query the corpus (resolve, verify, themes, recommend, terms) as native tool calls. Agent 2's
`/api/corpus/state` adds the state machine. The corpus is a first-class tool surface for every agent.

### 8. `hermes fallback` + `moa` — RESILIENCE (no single-model point of failure)
*Verified: fallback providers tried when primary fails; MOA = mixture-of-agents model slots.*

Autonomous translation must not die on a model outage. Hermes fails over across providers/models.

### 9. `hermes skills` — THE DOCTRINE AS EXECUTABLE PROCEDURE
*Verified: skills (install/list/snapshot export/import); a skill = an executable procedure with its own
prompt + tools.*

Pāṭala's **skills = the doctrine encoded**: `patala-translate` (T1→L2→C1 per the protocol),
`patala-validate` (run verify_l0 + validate-passage), `patala-review` (A4 review packet), `patala-prove`
(A2 source-Sanskrit L0). Each skill carries the epistemic guardrails (stamp MACHINE_PROPOSED, never
ACCEPTED; abstain, don't invent). `skills snapshot` archives/reproduces them (fresh-state plan).

### 10. `hermes sessions` — PERSISTENT, SEARCHABLE WORK
*Verified: SQLite session store (list/export/archive/stats).*

The playbook's "searchable memory ([7])" — Hermes already persists + can export sessions. A restarting
agent resumes its own history.

---

## THE REALIZED ARCHITECTURE (the vision on Hermes)

```
                HERMES (the kernel / A0 runtime)
   kanban(board+atomic claims+dep) · cron · hooks/webhook
   worktree(isolation) · memory · checkpoints · mcp · fallback/moa
                        │
   ┌────────────────────┼────────────────────┐
   ▼                    ▼                    ▼
 A2 patala profile   A3 patala profile    A1 patala profile
 (corpus compiler)  (translation factory) (philosophy)
 owns corpus_state   consumes NEXT_       owns gold/ARG/
 ledger + /api/corpus VALID_ACTION from   vertical objects
 + skills: prove      A2; cron executes    + skills: analyze
   │                    the eligible work    │
   └─────────┬──────────┴─────────┬─────────┘
             ▼                    ▼
         A4 review          A5 synthesis
         (skills: review)   (skills: research)
             └────────┬────────┘
                      ▼
                 A6 projection (skills: publish)
                 A7 scholar network (later)
```

**The one real thing we build on top:** Pāṭala's *epistemic state* + *skills* + *MCP corpus tools* —
not the agent runtime. Hermes provides the runtime.

---

## THE CONCRETE PIPELINE (translation factory on Hermes)

```
[kanban] task: translate <work> (dependency: "L0 VERIFIED" from Agent 2)
   → claimed by patala/A3 profile, runs in --worktree
   → cron or kanban dispatches
   → skill: patala-translate runs T1→L2→C1 via pipeline/model.py (hermes -z)
   → skill: patala-validate runs verify_l0 + validate-passage
   → checkpoints snapshot every write (rollback if bad)
   → stamps MACHINE_PROPOSED provenance (never ACCEPTED)
   → writes back to Agent 2's ledger (state update)
   → [kanban] task complete → next eligible task
```

---

## WHAT THIS MEANS FOR THE EXISTING PLAN

- **The `auto_run.py` supervisor** shrinks to: a kanban task + a cron schedule + a `patala-translate`
  skill. Hermes IS the supervisor.
- **The per-agent worktree migration** (GIT-INCIDENTS.md) is `--worktree` per profile — no manual
  `git worktree add`.
- **Agent 0's bespoke governance** (typed handoff, lane ownership, gating) = kanban board + hooks.
- **The Pāṭala "soul"** = profile personality + MEMORY.md with the doctrine + the doctrine-carrying skills.

---

## RECOMMENDATION (minimal, non-over-engineered)

1. **Seed the `patala` profile + project** (per HERMES-PATALA-SETUP.md) with the doctrine soul.
2. **Build the doctrine-carrying skills**: `patala-translate`, `patala-validate`, `patala-prove`,
   `patala-review` — these encode the protocol + guardrails.
3. **Init the kanban board** + one cron job for the translation loop.
4. **Use `--worktree` per agent** — solves git isolation by construction.
5. **Do NOT build** a competing runtime (Temporal/LangGraph/CrewAI/Cloudflare orchestration). Hermes
   already is the kernel.

*Carry-forward: Hermes is the backend. Its kanban = Agent 0's scheduler, its --worktree = the git fix, its
cron = the sleep-time translator, its hooks = dependency propagation, its skills = the doctrine. Pāṭala
lays its epistemic state + skills on top. Build the skills and the board, seed the soul, and the vision's
A0–A3 run on infrastructure that already exists.*
