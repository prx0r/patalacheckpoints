# AGENTIC INFRA — LIVING PLAYBOOK (what we borrow, what works in practice)

*2026-08-12. The **living reference** for agentic infrastructure as it applies to Pāṭala. Unlike the
one-time survey (`AGENTIC-INFRA-COMPARISON.md`), this file is **updated continuously with what actually
works in practice** — functions we adopt, tried-and-abandoned ideas, and observed results. It is the
practical layer over the survey's findings. **Keep this honest: if a borrow doesn't help, record that and
drop it. Category A (infra) that doesn't earn its keep is theater.**

---

## HOW TO USE THIS FILE
- This is a **living ledger**, not a spec. Update it as you actually adopt (or abandon) a function.
- Every entry has: **FUNCTION · STATUS (ADOPTED / TRIED / SKIPPED / OVERKILL) · WHY / RESULT**.
- The rule from our doctrine applies: *a function is real only if it earns its keep in practice, not
  because a framework ships it.*

---

## BORROWED / ADOPTED (working in practice)

### [1] Persistent identity across sessions — ADOPTED
**Source:** Gas Town (Polecats — persistent identity, ephemeral session).
**In Pāṭala:** live instances (`instance_of: agent0`) keep a stable `id` + `handover/<id>/history.log`.
**Result (practical):** a restarting agent reads its own history; identity survives session ends. Already
working — just needs to stay the discipline. **Keep.**

### [2] Git-backed durable state — ADOPTED
**Source:** Gas Town (Hooks — git-worktree persistence).
**In Pāṭala:** `STATE.yaml` + `history.log` + per-lane `INDEX.md` are git-tracked.
**Result (practical):** an agent that loses all memory on restart can `git log` / read `STATE.yaml` and
resume from where it left off. **This is the single most valuable property and we already have it** — the
discipline is: ALWAYS update state via `flow.py` (never let progress live only in session memory).

### [3] Versioned, attributed progress — ADOPTED
**Source:** Gas Town (Beads ledger) / Temporal (versioning).
**In Pāṭala:** `flow.py update` bumps `state_version` + appends `who/what/when` to `history.log`.
**Result (practical):** every change is auditable. **Keep.**

### [4] Human-in-the-loop / review states — ADOPTED (native)
**Source:** LangGraph (interrupts).
**In Pāṭala:** the `review_state` ladder (SINGLE_REVIEWED → DOUBLE_REVIEWED → ADJUDICATED) + the gate's
`needs_review` — already more scholarly than LangGraph's interrupts. **Keep, it's native.**

### [5] Template → instances (agnostic agent shape) — ADOPTED
**Source:** our own design (confirmed by Gas Town's Town/Mayor/Polecats).
**In Pāṭala:** `AGENTS.yaml` has `template: agent0` + `instances: agent1/agent2` (`instance_of: agent0`).
**Result (practical):** adding an agent = instantiating the template (entry + orientation + history log).
**Keep.**

---

## PARTIALLY ADOPTED / PILOTING

### [6] Typed handoff (mailbox routing) — TRIED, PILOTING
**Source:** Gas Town (mailboxes).
**What:** `flow.py handoff <from> <to> "<what> <file> <schema>"` — a typed, logged, versioned handoff.
**Status:** NOT yet implemented. The comparison flagged it as the single highest-value borrow.
**Decision pending:** add if cross-lane handoffs (Agent 1 → Agent 2 at CP4) become frequent enough to
justify it. *Update here once tried.*

### [7] Searchable session memory — ADOPTED (concept), IMPLEMENTATION PENDING
**Source:** Loom (ghuntley/loom) — thread/conversation persistence with FTS5 search.
**What:** make agent memory **searchable, not just persisted** — `flow.py search <term>` over
`history.log` + `SESSION-*.md` (a small FTS index or a grep-based search command).
**Status:** the concept is ADOPTED (persistence-without-search = storage, not memory); the command is
not yet implemented. ~40 lines.
**Decision pending:** add `flow.py search` so a restarting agent genuinely *remembers* ("when did we
last touch CP4 / the Commitment decision?") instead of re-reading files. *Update once implemented.*

---

## TRIED & ABANDONED / SKIPPED (honest)

_(Reserved for things we try and drop. Per the doctrine: recording a failure is more valuable than a
hollow success. Add entries here as you actually try and reject functions.)_

---

## OVERKILL (do NOT adopt — recorded so we don't revisit)

| Function | Why overkill for Pāṭala | Source |
|---|---|---|
| **Temporal durable-workflow engine** | for long-running distributed compute; our state is tiny + git-resident | Temporal |
| **Full LangGraph graph executor + LangSmith** | we need no runtime graph executor; our "graph" is the scholarly IR | LangGraph |
| **CrewAI role-play + task delegation** | 2 live agents + a template, not a crew | CrewAI |
| **Mastra / OpenAI SDK runtime tooling** | we don't run tool-calling agents; we run research agents | Mastra / OpenAI |
| **OpenClaw always-on daemon** | Pāṭala agents work in sessions | OpenClaw |
| **Loom coding-agent REPL + tool execution** | Pāṭala agents do research, not code editing | Loom |
| **Loom enterprise infra (K8s Weaver, auth/ABAC, analytics, feature flags)** | overkill for a 2-agent scholarly system | Loom |
| **Vector memory / long-term store** | our "memory" is the structured corpus + gold | various |
| **Multi-agent debate (ACAL-style)** | a scholarly decision, not infra; not now | ACAL |

---

## THE PRACTICAL PRINCIPLE (the one to keep)

> **Pāṭala's agent system is infrastructure to keep scholarship honest — not a general agent platform.
> Borrow functions as a menu, adopt only what earns its keep in practice, and record what actually works
> in THIS file. A function that doesn't help Pāṭala's real work (gold, extraction, verification) is
> theater regardless of which framework ships it.**

---

*Update this file whenever you: adopt a function (moves it to ADOPTED with a result), try and drop one
(moves it to TRIED & ABANDONED), or confirm a borrow is working. Keep it honest — that's its whole value.*
