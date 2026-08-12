# HERMES — PĀṬALA-SCOPED SETUP (the execution-engine plan)

*2026-08-12. How Pāṭala integrates with Hermes, and how to give it a fresh, doctrine-scoped state with
its own "soul." This is the PLAN (do NOT run the mutation commands until the coordinator approves — they
touch the shared `~/.hermes` state). Companion to `AGENT-ARCHITECTURE-VISION.md` (A3 = translation factory
uses Hermes as its worker).*

---

## 1. HOW PĀṬALA INTEGRATES WITH HERMES TODAY (all live)

| Integration | What it does |
|---|---|
| **`pipeline/model.py`** | shells out to `hermes -z <prompt>` — Pāṭala keeps ALL the epistemic logic (lean JSON schemas, audit, contract-format repair); hermes handles model selection/retries/reliability. |
| **MCP server** | hermes config has a `tantrakosa` server → `patala/mcp/index.mjs` (21 tools: resolve, verify/quote, verify/claim-structure, trace-dependency, find-counterevidence, themes, hub, spines, recommend, terms, ...). Hermes agents can query the corpus as an agent. |
| **`~/.hermes/config.yaml`** | the shared hermes state (model: opencode-go/deepseek-v4-flash, MCP servers, personality registry). |

**Current role:** hermes is used as a *model-call wrapper* (`-z`), not yet as a full agent. But it IS a full
agentic framework (cron, sessions, memory, skills, mcp, fallback, moa, worktree, projects, profiles).

---

## 2. THE DESIGN: HERMES = A3's EXECUTION ENGINE (not the orchestrator)

```
Agent 2 (corpus_state.py) ──> says WHAT IS ALLOWED next (NEXT_VALID_ACTION, eligibility)
        │
        ▼
Hermes (cron job, patala profile) ──> executes the eligible work (T1→L2→C1)
        │
        ▼
Agent 2 (validates) ──> updates the ledger, stamps MACHINE_PROPOSED provenance
```

Hermes is the **worker** (A3's execution engine). Agent 2 owns state truth + `NEXT_VALID_ACTION`.
Hermes consumes that action, does the work, and writes back proposed artifacts for Agent 2 to verify.

---

## 3. THE PLAN: A FRESH, DOCTRINE-SCOPED HERMES STATE

### Step 1 — ARCHIVE the current skills (non-destructive)
```bash
hermes skills snapshot export /root/projects/patala/data/corpus/downloads/hermes-skills-archive.json
```
Preserves the accumulated project-specific skills (`acquire`, `cron-acquire`, `factory-pipeline`,
`source-to-essay`, `tantraloka-film`, ...) so nothing is lost. Skills live in `~/.hermes/skills` +
`~/.hermes/skill-bundles`.

### Step 2 — CREATE a Pāṭala profile (isolated identity + state)
```bash
hermes profile create patala
hermes profile use patala
```
A profile is an isolated identity/config/skills/session-store — separate from the `default` profile that
other projects (FableCut, blog, ...) have accumulated state in.

### Step 3 — CREATE the Pāṭala project (folder-scoped workspace)
```bash
hermes project create patala
hermes project add-folder patala /root/projects/patala
```
`No projects yet` currently — a `patala` project cleanly anchors to the repo.

### Step 4 — DEFINE THE PĀṬALA "SOUL" (the doctrine as identity)
Instead of hermes' default personalities (`catgirl`, `concise`, `hype`, ...), the patala profile should
carry a personality that encodes the **AGENTS-DOCTRINE**, so every hermes call operates under it:

```
PĀṬALA SOUL (the profile personality/system-prompt)
────────────────────────────────────────────
ONE RULE:  Nothing is "real" because code exists. It becomes real only when independent gold +
           blind eval + metric + human adjudication show it does what its name claims.
TONE:      brutally honest about what is real vs hollow; retract overclaims explicitly;
           name the failure mode; no hype; precision over coverage (abstain, don't invent).
BANNED:    PROVED · TRUTH · CORRECT · BEST · WINS
USE:       SUPPORTED BY · PASSED CHECK X · MACHINE-PROPOSED · REVIEWED BY
AI PROPOSES ≠ PĀṬALA ASSERTS:  machine output is always origin=machine; never self-promotes to accepted.
ABSTENTION: "NO UNIQUE ARGUMENT RECOVERABLE" is a valid, valuable output.
ROLES:     A2 corpus compiler (state truth) · A3 translation factory (execution) · A1 philosophy.
           Hermes is the A3 worker — it consumes NEXT_VALID_ACTION, never invents workflow.
```

### Step 5 — RE-ADD only the Pāṭala MCP + corpus-state tools
- keep the `tantrakosa` MCP server (the 21 corpus tools) in the patala profile
- the corpus-state endpoint `/api/corpus/state` is Agent 2's control plane (Hermes reads NEXT_VALID_ACTION from it)

---

## 4. WHAT THIS DOES / DOESN'T CHANGE

**Changes:** a clean, doctrine-scoped hermes identity + project for Pāṭala, isolated from other projects'
accumulated skills/state. Every hermes call (incl. the translation pipeline) runs under the Pāṭala soul.

**Does NOT change:** the existing `-z` translation path in `pipeline/model.py` (it keeps working — it just
now runs in the patala profile, under the doctrine soul). Agent 2's `corpus_state.py` + `/api/corpus/state`
are untouched. No migration of the corpus, bibliography, or gold.

**Not yet built (the remaining gap):** the `pipeline/auto_run.py` supervisor that ties hermes cron → Agent 2's
NEXT_VALID_ACTION into a safe "translate while I sleep" loop (auto-validate, stamp provenance, stop-on-failure,
batch report). This is the A3 worker loop; the hermes profile is its environment.

---

## 5. WHEN TO RUN THIS

At a coordinated session boundary (Agent 0 / the coordinator approves), because it mutates the shared
`~/.hermes` state. Step 1 (snapshot archive) is safe to run anytime — it's read-only-ish (writes a backup
file). Steps 2–5 should happen together so the patala profile is created, scoped, and doctrinally-seeded
in one coherent move, then the auto_run supervisor can be built on top.

---

*Carry-forward: Hermes is the right execution engine (already the model client, already has cron/sessions/
memory/mcp). Don't build a competing framework on Cloudflare — use R2 for storage only. Give Hermes a fresh
patala profile + project seeded with the Pāṭala doctrine as its "soul," then build the small auto_run
supervisor to connect hermes cron to Agent 2's NEXT_VALID_ACTION. That is the minimal, non-over-engineered
path to autonomous translation.*
