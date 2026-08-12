# HERMES DEV PLAN — from foundation to the executable-corrections moat

*2026-08-12. The actionable build plan for operationalizing Hermes as Pāṭala's execution kernel, in service
of the corrected thesis (`hermespatala.md`): **Hermes = replaceable execution kernel; Pāṭala = durable
epistemic protocol + scholarly state.** The end-goal to obsess over is the **executable-corrections moat** —
a review is a *graph mutation with provenance*, not prose. This plan sequences the work so each step is a
real, verifiable capability (per the anti-theatre doctrine), not framework-building.

---

## THE FOUNDATION (already real — verified)

| Asset | Where | Status |
|---|---|---|
| Corpus state machine (Agent 2 core) | `pipeline/corpus_state.py` + `/api/corpus/state` | ✅ real — NEXT_VALID_ACTION control plane |
| IPVV source floor | 63/63 L0 lossless, frozen | ✅ real |
| Translation-state ledger | `data/corpus/downloads/translation-state-ledger.json` | ✅ real (45 works) |
| Model client | `pipeline/model.py` (shells to `hermes -z`) | ✅ real |
| Hermes runtime | kanban/cron/worktree/hooks/memory/checkpoints/mcp/skills/fallback/moa | ✅ available (verified) |
| **ReviewEvent + supersession primitives** | `data/corpus/primitives.ts`, `graph.ts`, `annotations.ts` | ✅ real — the seed of the corrections moat |
| MCP server | `mcp/index.mjs` (`tantrakosa`) | ⚠️ thin — one `patala` tool today |

---

## THE BUILD SEQUENCE (in dependency order)

### PHASE 1 — THE EXECUTION KERNEL (make Hermes operational for A3)

**1.1 Seed the Pāṭala profile + project** (per `HERMES-PATALA-SETUP.md`)
```
hermes profile create patala      # isolated config/memory/skills/sessions
hermes profile use patala
hermes project create patala      # anchor to /root/projects/patala
hermes project add-folder patala /root/projects/patala
```
Seed the profile's MEMORY.md with the **operator doctrine** (NOT epistemic state): fail-closed, machine-
proposed only, query via MCP, gold-first. Archive current skills first: `hermes skills snapshot export`.

**1.2 Point Hermes at the Pāṭala skill pack** (`skills.external_dirs` → `patala/skills/`)
Turn the existing repo skills (`translate-passage`, `translate-work`, `validate-passage`, `write-commentary`,
`assemble-stack`, `use-api`) into Hermes procedural memory via an external dir — repo stays the source of truth.

**1.3 Build the MCP capability layer** (the thin gap — highest value here)
Expose the graph as VERBS, not files. In `mcp/index.mjs`, add the `patala_*` tools the vision specced:
```
READ:   patala_resolve · patala_get_work_state · patala_get_passage · patala_get_grounding
        patala_get_dependencies · patala_next_action · patala_query_theme · patala_get_open_cruxes
WRITE:  patala_propose_translation · patala_propose_alignment · patala_propose_annotation
        patala_record_review · patala_mark_stale
NO:     patala_accept_claim / patala_set_truth  (never exist)
```
**"AI proposes ≠ Pāṭala asserts" is enforced at the tool boundary** — a confused prompt cannot call a
tool that doesn't exist. This is the single most important thing to build; it makes lane ownership into
permissions, not documentation.

**GATE 1:** an agent (via `hermes -z` in the patala profile) can query `patala_next_action`, `patala_get_work_state`,
and `patala_propose_translation` — and the write tool enforces MACHINE_PROPOSED (never ACCEPTED).

### PHASE 2 — THE TRANSLATION FACTORY (A3 prototype, the "translate while I sleep" loop)

**2.1 Kanban board + cron** — the supervisor, natively:
```
hermes kanban init        # the durable task board
hermes cron create "0 2 * * *" \
  "Run NEXT_VALID_ACTION for the top eligible work (query /api/corpus/state)" \
  --skill translate-passage --workdir /root/projects/patala
```
Each task: dependency = "L0 VERIFIED" (from Agent 2), claimed by the `patala` profile, run in `--worktree`,
executed via `pipeline/model.py` → T1→L2→C1, auto-validated, stamped MACHINE_PROPOSED, written back to the
ledger. **This is the A3 factory loop — Hermes IS the supervisor; no bespoke `auto_run.py` needed.**

**2.2 The validation gate in the loop** — after each translation, run `verify_l0`/`validate-passage`;
stop on failure (fail-closed). Provenance stamped at the tool boundary (Phase 1.3).

**GATE 2:** one eligible work (e.g. kramasadbhava's next passage) runs through the cron/kanban loop end-to-end
and the ledger reflects the new state (MACHINE_PROPOSED translation, no ACCEPTED).

### PHASE 3 — THE EPISTEMIC CORE + POLICY (make corrections executable — the moat)

**3.1 Make ReviewEvent a graph mutation** (the thing to obsess over)
The primitives exist (`ReviewEvent`, `supersedes`, epistemic states). Wire them into a mutation API:
```
POST /api/objects/{id}/review
  { decision: REJECT|REVISE|ACCEPT|ABSTAIN
    reason, replacement_ref, evidence_refs, reviewer_id, scope, object_version }
→ creates an immutable ReviewEvent
→ if REJECT/REVISE: marks the target superseded + returns the affected downstream objects
```
**3.2 Dependency recomputation** — the hook that makes corrections ripple:
A review → Pāṭala's dependency engine computes what changes:
```
INF-182 rejected (P71 doesn't support W14, replacement W19)
  → argument state changes
  → crux changes
  → downstream claims/synthesis flagged
  → future agents inherit the correction
```
This is the bridge from "AI peer-review tool" to "scholarly operating system." Hermes hooks trigger the
recomputation; **Pāṭala's dependency engine determines it** (per correction #4).

**GATE 3:** a REJECT ReviewEvent on an inference object creates the mutation, marks it superseded, and the
dependency engine returns the affected downstream objects — all with provenance.

### PHASE 4 — THE SCHOLAR SURFACE (the product)

**4.1 The Scholar Workbench review UI** — the primary surface (browser):
Given a REVIEW TASK (evidence + impact), the scholar can `ACCEPT/REVISE/REJECT/ABSTAIN/PROPOSE ALTERNATIVE`.
Submission → immutable ReviewEvent → Hermes wakes Agent 1 to recompute. **The scholar never sees Hermes.**

**4.2 The AI copilot inside the Workbench** — a constrained patala profile that queries the MCP, compares
readings, launches blind critics, but **cannot accept/promote**. The scholar signs the judgment.

**GATE 4:** a scholar can review one argument in the workbench; the submission mutates the graph and the
impact report updates.

### PHASE 5 — THE MOAT (hardened, external)

**5.1 Bring Your Own Agent** — `mcp.patala.org` with OAuth scopes (corpus:read, proposal:write, review:submit).
External agents (Claude/ChatGPT/their own) connect to Pāṭala without Pāṭala running their model.

**5.2 The executable-corrections dataset** — from Hermes trajectories + ReviewEvents, build the dataset:
`source → machine reconstruction → tools → alternatives → criticism → revision → review → human correction →
final object`. The moat: a dataset of *how difficult Sanskrit/philosophical judgments get corrected.*

**GATE 5:** an external agent resolves a Pāṭala ID over MCP; and the correction-history dataset exists and
is queryable.

---

## THE GUARDRAILS (from the corrected thesis — non-negotiable)

1. **Hermes never determines what Pāṭala knows.** All epistemic state, review decisions, provenance, and
   status live in Pāṭala (epistemic core + ledger + API). Hermes holds operator doctrine + execution history only.
2. **No tool can set truth/accept.** Only PROPOSE/RECORD verbs exist; promotion is a scoped policy action.
3. **Kanban is a scheduler, not the constitution.** The state machine lives in Pāṭala schemas/write APIs.
4. **Checkpoints ≠ epistemic rollback.** Hermes checkpoints undo files; Pāṭala supersession preserves history.
5. **Hooks trigger; Pāṭala determines.** Dependency/staleness logic is Pāṭala's; Hermes wakes it.
6. **Do NOT build** Temporal/LangGraph/CrewAI/a custom scheduler/a proprietary multi-agent protocol/a vector-
   memory universe/a bespoke workflow engine. Hermes runs the jobs.
7. **Don't require scholars to install Hermes.** They use the Workbench / MCP.

---

## THE ONE-SENTENCE CARRY-FORWARD

**Hermes is Pāṭala's replaceable execution kernel; the moat is that Pāṭala makes a scholar's correction an
executable graph mutation with provenance. Build in order: (1) the execution kernel — seed the patala
profile + MCP capability layer (graph-as-verbs, PROPOSE-not-ACCEPT at the tool boundary), (2) the A3
translation factory on kanban+cron, (3) the ReviewEvent-as-graph-mutation + dependency recomputation (the
thing to obsess over), (4) the Scholar Workbench + copilot, (5) BYOA over MCP + the executable-corrections
dataset. Each phase has a gate; keep authoritative state in Pāṭala, doctrine in Hermes memory, history in
Hermes sessions, and let Hermes disappear underneath the institution.**
