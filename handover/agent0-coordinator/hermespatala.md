# HERMES × PĀṬALA — THE INTEGRATION (execution kernel + epistemic state)

*2026-08-12. The single canonical reference for how Hermes integrates with Pāṭala. Merges the
backend-infrastructure model (verified feature→vision mapping, 2026-08-12) with the advanced recipes
(`hermespatala2.md`) and the foundational correction (`hermespatala3.md`). **Thesis (SHARPENED): Hermes
is Pāṭala's replaceable execution kernel. Pāṭala itself is the durable epistemic protocol and scholarly
state. Hermes schedules and executes epistemically permitted transformations; it never determines what
Pāṭala knows.***

---

## THE FOUNDATIONAL THESIS (corrected)

> **Hermes is Pāṭala's execution kernel, NOT Pāṭala's epistemic backend.**

Hermes must be **replaceable**. If Hermes vanished in three years, Pāṭala must retain every source,
claim, review, disagreement, contributor identity, provenance chain, and scholarly status. Hermes gives
excellent *execution primitives* (kanban, worktrees, cron, hooks, profiles, delegation, MCP, checkpoints)
— but those are **workflow state, not scholarly truth**.

**External positioning (the bet):**
> Humans use Pāṭala Workbench. Agents use Pāṭala MCP/API. Pāṭala internally uses Hermes. Future external
> agent systems may invoke Pāṭala agents over A2A.

**The moat:** model/runtime independence. Models improve, agent runtimes come and go, chat interfaces
change — but outside scholars/AIs increasingly rely on **Pāṭala IDs, source spans, ReviewEvents,
alignments, argument objects, correction history**. Hermes does its job perfectly when it *disappears
underneath the institution*.

---

## THE MENTAL SEPARATION (the core principle)

```text
PĀṬALA
= epistemic state machine (the durable protocol + scholarly memory of record)
  objects / provenance / review / status /
  dependencies / claims / transitions / contributor IDs / rights / versions

HERMES
= cognitive execution fabric (replaceable)
  sessions / skills / delegation / tools /
  scheduling / hooks / messaging / trajectories
```

Pāṭala tells Hermes *what kinds of transformations are epistemically legal*. Hermes gives Pāṭala the
machinery to perform those transformations repeatedly, concurrently, persistently, and increasingly well.
**But Hermes never determines what Pāṭala knows.**

---

## THE FOUR CORRECTIONS (from hermespatala3.md — do not encode these as Hermes conventions)

1. **Kanban = scheduler, not constitution.** Hermes kanban handles task/ready/running/blocked/review/done/
   dependencies/attempt-history/worker-assignment. But Pāṭala owns the constitution: `MACHINE_PROPOSED ≠
   ACCEPTED automatically`, `source integrity ≠ interpretive grounding`, `review scope matters`,
   `reviewer identity matters`, `supersession is immutable`, `UNDERDETERMINED is permitted`. These live in
   Pāṭala schemas + write APIs, not kanban conventions.
   `Hermes: "should A4 run this review task?"` · `Pāṭala: "what constitutes a valid ReviewEvent?"`
2. **Hermes memory ≠ epistemic state.** Hermes MEMORY.md is tiny (~2,200 chars) + sessions (SQLite/FTS5).
   It holds *procedural/operator memory* (gold-first ontology, fail-closed, machine-proposed only) and
   *execution history* — NOT `ARG-002 is accepted`, `Ratié reviewed X`. Those resolve through Pāṭala.
   Triad: `Hermes MEMORY = operator memory` · `Hermes sessions = execution history` · `Pāṭala graph = scholarly memory of record`.
3. **Hermes checkpoints ≠ epistemic rollback.** Checkpoints = "undo a malformed file Agent 3 wrote"
   (filesystem). Pāṭala supersession = "preserve the history of changing scholarship" (`P:v1 ACCEPTED by A`
   → `P:v2 REVISED by B, supersedes P:v1`). Completely different.
4. **Hooks trigger integrity machinery; they don't determine integrity.** A source change fires a Hermes
   hook → Pāṭala's dependency engine calculates what's stale/affected/downstream. The dependency logic
   belongs in Pāṭala; Hermes just wakes it up.

---

## PART I — HERMES AS THE BACKEND (verified feature → vision mapping)

*Every feature below was verified against `hermes --help` / subcommand help on 2026-08-12. Hermes already
provides the A0 governance primitives the agent-architecture vision specced as bespoke build work.*

| Hermes feature (verified) | Realizes the vision's... |
|---|---|
| **`kanban`** | **Agent 0's scheduler/constitution** — durable SQLite board, atomic task claims, dependencies, named-profile execution in isolated workspaces. Replaces bespoke typed-handoff + lane-ownership + gating. |
| **`--worktree`** | **The git-isolation fix for INCIDENT-2026-08-12-01** — "run in an isolated git worktree (for parallel agents)." Built-in; Agent 1 can never stage Agent 2's files. |
| **`cron`** | The "translate while I sleep" factory loop (scheduled A3 jobs, with `--skill --workdir --deliver`). |
| **`hooks` + `webhook`** | Dependency/staleness propagation (source change → invalidate L0 proof). Scholarly CI. |
| **`memory` + `memory-graph`** | Durable epistemic state (the Pāṭala soul in MEMORY.md; memory-graph = timeline of learned skills/memories). |
| **`checkpoints`** | Rollback — the mechanical guard behind "mistakes don't compound." |
| **`mcp` (tantrakosa server)** | The corpus as a native tool surface (21 tools: resolve, verify, themes, recommend, ...). |
| **`fallback` + `moa`** | Model resilience (no single point of failure; mixture-of-agents). |
| **`skills`** | The doctrine as executable procedure. |
| **`sessions`** | Persistent, searchable work (SQLite + FTS5; list/export/archive). |

**The corrected thesis:** Hermes is Pāṭala's **replaceable execution kernel** — it provides the runtime
primitives (kanban scheduler, worktrees, cron, hooks, skills, sessions, resilience). Pāṭala layers its
epistemic state (the corpus ledger + gold) and doctrine-carrying skills on top. Hermes does NOT rebuild
the agent runtime, and it is NOT the epistemic authority. If Hermes vanished, Pāṭala retains all scholarly truth.

---

## PART II — THE REALIZED ARCHITECTURE

**The sober architecture (from hermespatala3.md) — Pāṭala's epistemic core sits ABOVE the Hermes kernel:**
```
PĀṬALA
  EPISTEMIC CORE (Works · Passages · Assertions · Propositions · Arguments ·
                  Alignments · Reviews · Provenance · Versions · Rights ·
                  Contributor IDs · Dependency graph · Corpus state)
        │  event/jobs
        ▼
  HERMES (execution kernel)
  Kanban · Profiles · Worktrees · Cron · Delegation · Skills · Hooks ·
  Checkpoints · Models/fallback
        │
  A1 / A2 / A3 / A4 ...
```

```
                HERMES (the replaceable execution kernel)
   kanban(scheduler, NOT constitution) · cron · hooks/webhook
   worktree(isolation) · skills · sessions · mcp · fallback/moa
                         │
   ┌─────────────────────┼─────────────────────┐
   ▼                     ▼                     ▼
 A2 patala profile    A3 patala profile    A1 patala profile
 (corpus compiler)   (translation factory) (philosophy)
   │                     │                     │
   └─────────┬───────────┴──────────┬──────────┘
             ▼                      ▼
         A4 review             A5 synthesis
             └────────┬────────────┘
                      ▼
                  A6 projection · A7 scholar network (later)
```

**End-state:** humans use the **Pāṭala Scholar Workbench**; agents use **Pāṭala MCP/API**; Pāṭala
internally uses **Hermes**; future external agents invoke Pāṭala over **A2A**. Hermes is invisible
infrastructure — it disappears underneath the institution.

---

## PART III — THE ADVANCED RECIPES (from hermespatala2.md)

### 1. Pāṭala agents = persistent Hermes identities, state OUT of Hermes memory
Keep authoritative state (ARG-002 status, CP3 status, source hashes, accepted claims, review decisions)
in **Pāṭala**. Hermes memory holds only **operating doctrine** (the soul). Use `session_search` (FTS5)
for historical recall.
```
Hermes memory  = operating doctrine
Hermes session = experiential history
Pāṭala git/graph = truth
```

### 2. Every Pāṭala transformation = a Hermes Skill, with skill evolution under review
Formalize `/patala-source-ingest`, `/patala-build-l0`, `/patala-translation-pass`, `/patala-c1`,
`/patala-theme-discovery`, `/patala-argument-extract`, `/patala-argument-review`, `/patala-semantic-align`,
`/patala-evaluate-argument`, `/patala-crux`, `/patala-session-close`. **Skill evolution** = Hermes
self-improvement proposes a skill patch → Pāṭala review gate → frozen benchmark → only promote if the
benchmark improves. Institutional learning at the process level, not model fine-tuning.

### 3. Hermes subagents as EPISTEMIC ADVERSARIES, not workers
Blind, isolated contexts. For argument reconstruction:
```
SUBAGENT A (minimalist)  recover only what the text licenses
SUBAGENT B (strong)      strongest coherent reconstruction
SUBAGENT C (adversary)   falsify A and B (reversed entailments, imported doctrine, scope jumps)
A cannot see B. Parent derives: agreement · disagreement · crux.
```
Generic recipe: `BLIND GENERATE → BLIND COUNTERGENERATE → ADVERSARIAL AUDIT → SYNTHESIZE DIFFERENCE → STORE DISAGREEMENT, NOT JUST WINNER`.

### 4. Blind adjudication tournaments
5 reconstruction agents → 3 critic agents (anonymized candidates) → 2 judge agents (no candidate
provenance) → parent records consensus/minority/exact-disputed-premises. **Don't average scores** — derive
stable claims, unstable claims, interpretive forks, load-bearing disagreements. A machine pre-review
dossier that compresses human attention.

### 5. `execute_code` as the deterministic tissue between reasoning steps
The model writes Python calling Hermes tools; only final output returns. For Agent 2: enumerate manifests,
query bibliography, hash sources, resolve IDs, compute missing transitions → print only anomalies
("17 stale source deps, 8 missing L0 artifacts..."). `LLM = judgment · execute_code = computation · Pāṭala = state`.

### 6. A Pāṭala Hermes plugin exposing the graph as VERBS, not files
Tools like `patala_resolve`, `patala_get_work_state`, `patala_next_action`, `patala_get_passage`,
`patala_propose_annotation`, `patala_record_review`, `patala_get_dependencies`, `patala_mark_stale`,
`patala_query_theme`, `patala_get_open_cruxes`. **Write verbs are PROPOSE / RECORD_REVIEW — never
SET_TRUTH / ACCEPT.** "AI proposes ≠ Pāṭala asserts" enforced at the tool boundary: a confused prompt
cannot call `patala_accept_claim` because it doesn't exist.

### 7. MCP/tool filtering = capability security per agent
Lane ownership becomes **permissions**, not documentation. Agent 1: read corpus, propose argument/theme,
run evaluator (NO source mutation, NO accepted-status). Agent 2: read/write corpus state, run source
verification, mark stale (NO philosophical acceptance). Agent 3: read eligible jobs, write machine-proposed
translation + C1 proposal (NO accept, NO bibliography mutation). Agent 4 (later): read proposals, create
review event, promote only under policy.

### 8. Hermes hooks = database triggers for epistemic invariants
- `pre_tool_call`: verify source ref resolves / work eligible / correct lane / correct worktree / deps current.
- `post_tool_call`: hash artifact, attach provenance, emit state-transition event, queue validation.
- `subagent_stop`: persist agent-role/model/source-hash/output-hash/result.
- `on_session_end`: run staleness check, theatre check, uncommitted-artifact check, skill-learning proposal, handoff summary.

### 9. Agent 4 = a review scheduler driven by graph conditions (not a to-do list)
Nightly NO-AGENT cron script queries Pāṭala (new proposals, stale artifacts, failed factory jobs,
unreviewed high-centrality claims, new cruxes) → only if meaningful, launch a review session ranked by
downstream impact / uncertainty / centrality / source quality. Graph-aware review allocation.

### 10. Webhook-driven scholarly CI ("GitHub CI for epistemology")
On a push to translations/ c1/ argument-gold/ theme-gold/ bibliography → Hermes determines affected
objects → runs the right audit (source change → A2 dependency audit; C1 change → A1 theme impact;
argument change → evaluator rerun; review event → projection regeneration) → posts a PR comment
(SCHOLARLY IMPACT: 2 source proofs stale, 4 propositions downstream, ...).

### 11. Hermes trajectories = a dataset of scholarly cognition (a moat)
Save source → machine reconstruction → tools consulted → alternative → criticism → revision → review →
human correction → final accepted object. 10,000 passages of "how difficult Sanskrit/philosophical
judgments get corrected" = training/eval data for translation, extraction, alignment, uncertainty
calibration, review prioritization. Hermes already has session/trajectory export — don't invent capture.

### 12. Counterfactual research swarms
Given a crux (e.g. vimarśa = SAME_SENSE vs NEAR_SAME vs DIFFERENT_SENSE), spawn isolated subagents each
on a graph snapshot with one variable changed; ask what arguments/themes/contradictions/claims change.
Parent compares worlds → CRUX IMPACT. Structured Monte Carlo over interpretation space.

### 13. Scholar simulation before scholar review
Skills = review methodologies, not fake personalities: `/textual-philologist`,
`/historian-of-philosophy`, `/formal-argument-reviewer`, `/translation-auditor`,
`/tradition-comparison-reviewer`. Apply several methodological lenses to every object. Human then sees
a machine pre-review (2 scope issues, 1 unsupported inference, ...) + remaining questions. Expert
attention compression.

### 14. Separate discovery models from adjudication models
Cheap/high-recall model for discovery (many themes/alignments/alternatives) → strong reasoning model for
critique → separate model to compress disagreement → human final. `cheap recall → expensive precision →
scarce human judgment`. Economic scaling.

### 15. Model disagreement itself as evidence
Run the same structured task with models A/B/C; store disagreement as a feature
(MODEL_CONSENSUS_HIGH / MODEL_DISAGREEMENT_HIGH). Correlate later with human corrections → an empirical
review-prioritization signal, better than raw LLM confidence.

### 16. Self-improving procedures from correction history (gated)
ReviewEvents → analyze recurring correction patterns → propose changes to `/patala-translation` /
`/patala-commitment-extraction` → run frozen benchmark before/after → **only promote if the benchmark
improves**. Never let Hermes self-improvement directly rewrite production procedures. Controlled drift.

---

## PART IV — THE THREE INTEGRATIONS TO BUILD FIRST

### A. Pāṭala skill pack (external skill dir)
Hermes supports `skills.external_dirs` — so `patala/skills/` (translate-passage, build-l0, write-c1,
theme-discovery, argument-review, session-close) stays the repo source of truth and becomes native Hermes
procedural memory without copying into Hermes.

### B. Pāṭala MCP/plugin capability layer
Expose structured graph verbs (`patala_*`) and whitelist them differently per agent. Gets agents away from
arbitrary filesystem reasoning.

### C. Blind adversarial delegation recipe
One canonical `/patala-adversarial-review` skill that auto-launches minimal reconstruction + strong
reconstruction + adversarial critic + synthesis, returning a structured disagreement object. Immediately
improves theme/argument/translation/semantic-alignment review.

---

## PART V — THE SCHOLAR & API SURFACE (the product vision, from hermespatala3.md)

**The guiding rule: scholars should almost never know Hermes exists.** Don't ask a Sanskritist to
"install Hermes, configure a profile, connect MCP, select a model" — that kills adoption. A scholar
experiences **Pāṭala**, not its runtime. Three ways to interact, in priority order:

### 1. The primary surface: Pāṭala Scholar Workbench (browser)
Agent 1 creates a `REVIEW TASK` (e.g. ARG-002: does V2-L license this reconstruction?) with exact
Sanskrit, source/literal layer, translation, C1, proposed propositions + warrant, competing
reconstruction, machine critique, and **impact** (this judgment affects 2 arguments / 1 theme / 4 claims).
The scholar sees the evidence and can `ACCEPT / REVISE / REJECT / ABSTAIN / PROPOSE ALTERNATIVE / COMMENT`.
Underneath, submission creates an immutable `ReviewEvent` (reviewer_id, object_version, scope, decision,
rationale, evidence_refs, timestamp). Then Hermes wakes Agent 1 to recompute affected objects.

**The AI copilot inside the Workbench:** a constrained "Scholar Copilot" Hermes profile that queries the
Pāṭala MCP, retrieves passages, compares alignments, searches bibliography, launches blind-critic
subagents, constructs alternatives — but **cannot ACCEPT/REJECT/PROMOTE**. The scholar signs the judgment.
```
Scholar → Pāṭala Workbench → Hermes Research Copilot → Pāṭala read/propose tools
```

### 2. The strategic surface: Bring Your Own Agent (MCP) — `mcp.patala.org`
MCP is a tool-access protocol that doesn't dictate a UI. Advanced scholars could connect Claude, ChatGPT,
Hermes, a university agent, or their own Python agent to `mcp.patala.org` and call
`patala.search_passages · resolve · get_source · get_translation · trace_claim · get_argument ·
compare_readings · list_open_questions · propose_translation · propose_alignment · propose_review`,
with OAuth scopes (corpus:read, bibliography:read, review:read, proposal:write, review:submit).
**Do not make Pāṭala dependent on the winning chat interface** — this is where adoption-of-identifiers
becomes the moat.

### 3. Later: A2A (agent-to-agent)
```
Pāṭala HTTP API = stable primitive data interface
Pāṭala MCP      = agent-friendly tool/resource interface
A2A (later)     = Pāṭala exposes long-running agent capabilities to other agents
                  (e.g. publish an Agent Card advertising translation_audit,
                   argument_audit, source_trace, semantic_comparison, literature_dossier)
```
A2A v1.0 is for opaque agent systems to discover one another + collaborate without exposing internal
memory/tools. Don't build it today — MCP solves today's integration problem.

### 4. Peer review becomes bigger than "review this translation"
A scholar uploads a paper → Pāṭala Review runs: claim extraction → citation resolution → corpus retrieval
→ argument extraction → terminology audit → counterevidence search → alternative reconstruction →
source-grounding audit → Reviewer-2 attack → impact/crux analysis. Result: "17 claims extracted; 11
strongly grounded, 3 need qualification, 2 unsupported, 1 underdetermined; LOAD-BEARING ISSUE C7 depends
on treating vimarśa in V2L/V2O as SAME_SENSE..." Every criticism bottoms out in corpus objects and
survives as an auditable artifact.

**Human peer review, restructured:** author uploads → machine pre-review → structured open questions →
A7 routes remaining questions to scholars → human ReviewEvents → machine recomputation → adjudicated
review dossier. The machine doesn't replace peer review; it compresses it to "the 7 claims where expert
judgment has maximum value."

### 5. The executable-corrections moat (obsess over this)
Normal review = prose ("I don't think this works"). Pāṭala = a graph mutation with provenance:
```
ReviewEvent: target=INF-182 · decision=REJECT · reason="premise P71 doesn't support rule W14"
            · replacement=W19 · evidence=SourceSpan...
→ graph recomputes → argument state changes → crux changes → synthesis changes → future agents inherit
```
A review becomes a **graph mutation with provenance** — the bridge from "AI peer-review tool" to
"scholarly operating system."

### 6. The ultimate minimal architecture (don't build a framework)
Build only what belongs uniquely to Pāṭala:
```
1. EPISTEMIC GRAPH / LEDGER   IDs, sources, assertions, arguments, reviews, dependencies, versions
2. POLICY / STATE TRANSITIONS what MACHINE_PROPOSED means, who may promote what, staleness/supersession
3. PĀṬALA API                 stable primitives
4. PĀṬALA MCP                 AI-native access to those primitives
5. SCHOLAR WORKBENCH          excellent human review UX
6. PĀṬALA SKILLS              domain procedures executed by Hermes
7. HERMES                     run the damn jobs
```
No Temporal, LangGraph, custom scheduler, proprietary multi-agent protocol, vector-memory universe,
bespoke workflow engine, or requirement for scholars to install Hermes.

**Agents as roles/capability profiles, not immortal processes:** don't map "A1 = one Hermes process
forever." Pāṭala agents are roles; kanban creates executions of those capabilities (a task claims a
worker = patala-philosophy profile + skill + isolated workspace, produces Proposal objects + EvaluationRun
+ evidence refs, then the worker dies). Persistent identity belongs to the role + execution record.

**And don't use MoA as "truth by committee":** 5 models agreeing ≠ scholarly truth. Record
MODEL_AGREEMENT / MODEL_DISAGREEMENT and test whether disagreement predicts human revision.

---

## THE CARRY-FORWARD

> **Hermes is Pāṭala's replaceable execution kernel; Pāṭala itself is the durable epistemic protocol and
> scholarly state. Hermes schedules and executes epistemically permitted transformations; it never
> determines what Pāṭala knows.** Humans use the Pāṭala Workbench; agents use Pāṭala MCP/API; Pāṭala
> internally uses Hermes; future external agents invoke Pāṭala over A2A. Build the three integrations
> first (skill pack, MCP capability layer, blind adversarial review); keep authoritative state in Pāṭala
> (epistemic core), doctrine in Hermes memory, history in Hermes sessions; use `--worktree`, `kanban`,
> `cron`, and `hooks` as the execution layer only. Hermes succeeds when it disappears underneath the
> institution — when outside scholars and AIs rely on Pāṭala IDs, source spans, ReviewEvents, alignments,
> argument objects, and correction history.
