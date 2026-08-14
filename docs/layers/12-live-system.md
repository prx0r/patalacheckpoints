# LAYER 12 — THE LIVE SYSTEM (agents · state · docs · staleness)

> **STATUS: PARTIAL — Tier-1 truth (registry/review/events) is REAL; projection/staleness/MCP/queue are pending** (derived live state — see `docs_state.py`)


*Part of the `NAVIGATION.md` layer map (the master tree / spine). THE complete live system: how Hermes agents, coding agents,
Pāṭala state, and the docs stay in sync so nothing goes stale. This is the CANONICAL spec for the
7 pieces that close the loop. Read this before building any orchestration or state-projection code.
Peer-reviewed against the Gas Town / Gas City / Beads / Beads-Rust / Beads-Viewer / Agetor / Mozzie /
Agent Mail / agtx / CAS stack (`docs-cache/coordinate-peer-review.md`); the 7-piece + 5-state model here
is the refined outcome.*

> **⚠ UPDATED by `docs-cache/agenticideas.md` (the most important correction):** the epistemic control
> plane (review gate, adjudication, epistemic ceilings) is ALREADY BUILT — don't re-build a Vouch-like
> substrate. The real missing piece is **operationalizing independent human scholarship** (the Scholar
> Attestation Vertical). So: **Piece 5 = the Scholar Attestation Vertical, not "the review gate." Piece 6
> (Task≠Run) = operations-only, outside the epistemic graph. Piece 7 = the Epistemic Work Queue v0
> (lexicographic policy + instrumentation, NOT ML).** Moat refined to `M = D×P×F×J×C×N×A` (transformation
> faithfulness × independent adjudication × correction propagation).

> **The one principle:** `Hermes owns the task lifecycle · Pāṭala owns the epistemic state · docs are a
> projection of Pāṭala state.` `Kanban = lifecycle truth · Worker = implementation · Reviewer = gates
> done · Pāṭala = epistemic truth.`

> **The governing boundary (sharpened):** **Pāṭala decides what matters; Hermes decides how work gets
> executed.** `patala_next_action()` answers "what is the highest-leverage unresolved object?" deterministically
> from the graph; Hermes finds a capable worker and completes it. This is the cleanest agentic boundary found
> across every stack reviewed.

---

## 1. THE PROBLEM (why docs go stale)

Docs are hand-written content about state. When an agent changes the factory code or a worker commits
an object, the docs describing that state become stale because nothing connects "the doc" to "the state
it describes."

The fix is **NOT** more hand-editing. It's: **separate docs into DERIVED-LIVE sections (rendered from
truth, never stale) and HAND-WRITTEN sections (agent-maintained, staleness-checked).**

## 2. THE THREE TIERS (one source of truth, two projections)

```text
TIER 1 — PĀṬALA STATE (the truth, machine-owned, append-only)
   object_registry.py  (versioned objects + hash-chained event ledger)   [built]
   corpus_state.py     (next_valid_action · ledger_json)                 [built]
   Postgres Atlas      (the canonical graph)                             [built]
   ReviewEvents        (human authority)                                 [built]
   git history         (code + docs changes)                             [built]
        ↓  derives
TIER 2 — PROJECTION (regenerated, NEVER hand-edited)
   docs_state()          → per-layer live-state JSON                     [TO BUILD]
   check_docs_stale.py   → code↔docs staleness flags                     [TO BUILD]
   STATE.yaml            → becomes a projection, not an orchestration DB [TO DEMOTE]
        ↓  renders
TIER 3 — PRESENTATION (the docs)
   docs/layers/NN-*.md   ·  NAVIGATION.md  ·  the canonical docs
```

## 2b. THE FIVE KINDS OF STATE (they must never substitute for each other)

The peer review's most important addition. `Markdown as task DB + memory + docs + state` is the disease;
these five states are the cure — each has ONE owner and must never silently substitute for another:

```text
DOMAIN STATE        "what is currently believed/accepted?"    Owner: Pāṭala (object_registry, ReviewEvents)
WORK STATE          "what is someone currently doing?"        Owner: Hermes Kanban
IMPLEMENTATION      "what code actually exists?"              Owner: Git / filesystem / tests
PROJECTION STATE    "what do humans currently see?"           Owner: projection engine
PROCEDURAL STATE    "how should this kind of work be done?"   Owner: versioned Hermes skills
```

**The two substitutions that must never happen:**
```text
KANBAN "Translation 1.3.5 done"   ≠   PĀṬALA "Translation 1.3.5 accepted"
DOC "39/41 tests passing"         ≠   current state (must point to a TestRun → commit → results)
```

## 3. THE WORKER LANES (all feed one truth, all on one board)

The kanban contract (Hermes) defines a **worker lane**: an assignee string + a spawn mechanism + a
lifecycle terminator. Pāṭala has **4 lane types** — including the **coding agent**:

| Lane | Permissions | Writes to | Reviewer |
|---|---|---|---|
| **Agent 2 (producer)** | narrow, safe | `object_registry` (objects) | Agent 1 + scholar |
| **Agent 1 (verifier)** | narrow, safe | `ReviewEvents`, eval results | scholar |
| **Coding agent** | **broad** — code + docs + schema | **git commits + docs** | code review |
| **Scholar (human)** | sacred | `ReviewEvents` | human |

**The coding agent is a worker lane** — Hermes explicitly supports "external CLI worker lanes" (Codex,
Claude Code, OpenCode, etc.). A coding agent claims a task, does work, and its output (code commits +
doc updates) flows back through the board. It's just a broader-permission lane.

**Agent 3 (coordinator)** is the **orchestrator lane**: it has kanban tools but **NO** terminal/file/
code/web implementation tools (the anti-temptation rule from the Hermes orchestrator contract). It
decomposes goals → creates child tasks → routes to lanes → monitors → steps back.

## 4. THE 7 PIECES TO BUILD (once, formally — upgraded from 5 by the peer review)

### Piece 1 — Canonical State API (Tier 1, the truth)
Already built: `object_registry` (versioned + event ledger) · `corpus_state` (next_valid_action) ·
ReviewEvents. **No Markdown authority.** The peer review's first principle: domain state lives here,
append-only, never in docs.

### Piece 2 — Append-only Event Log (the missing first-class primitive)
Every meaningful mutation emits an event — **don't infer history from Git diffs**:
```json
{ "event_id": "...", "object_id": "...", "operation": "claim_qualified",
  "actor": "patala-verifier", "task_id": "...", "run_id": "...",
  "before_hash": "...", "after_hash": "...", "timestamp": "..." }
```
Current state = snapshot; history = events. (The `object-events.jsonl` ledger exists — extend it.)

### Piece 3 — Projection Engine (rename from `docs_state()`)
`docs` are only ONE consumer. The projection engine renders canonical state → docs + JSON + dashboard +
AGENTS context + API + scholar views:
```text
canonical state → projection engine → docs · JSON · dashboard · AGENTS ctx · API · scholar views
```
`docs_state()` is just one renderer of this.

### Piece 4 — Staleness/Provenance Engine (deterministic, from `check_docs_stale.py`)
Don't just do "file changed → doc stale." Track **provenance hashes** (from Repowise + the peer review):
```yaml
projection: docs/layers/03-factory.md#live-state
depends_on:  [registry:ObjectType, schema:Translation, file:pipeline/object_registry.py]
generated_from: { git_commit: abc123, state_hash: def456, renderer_version: 4 }
```
Then state is **CURRENT / STALE / UNKNOWN** deterministically — not by timestamp. For fully-derived
sections, drift is a **CI failure** (`generate-docs && git diff --exit-code`); for hand-written sections
it's a STALE/VERIFY flag.

### Piece 5 — the Scholar Attestation Vertical (redefined by agenticideas — the review gate is ALREADY BUILT)
**NOT "build the review gate"** — we have it (review_engine, adjudication, epistemic ceilings). The
missing piece is **operationalizing independent human scholarship over that machinery.** Prove a real
scholar can independently inspect + adjudicate ONE complete argument (a gold IPVV argument):
```text
ScholarlyAttestation: scholar_id · target_id/version/hash · expertise_scope · review_dimension
  · stance (ACCEPT / ACCEPT_WITH_QUALIFICATION / REJECT / CONTEST / UNDERDETERMINED)
  · rationale · cited_evidence[] · proposed_correction[] · confidence
  · disclosed_conflicts[] · compensation_context · timestamp
```
**The rule:** a scholar does NOT turn something into Truth by clicking approve — they ADD an attributable
epistemic event. Three specialists can disagree; all three are preserved; canonical status is a transparent
policy over evidence + attestations.

**The proof (the real moat):** after adjudication, **intentionally modify an upstream translation** and
verify which proposition/argument/synthesis/scholar-attestation becomes stale and propagates. That is
proof of **correction propagation through the intellectual dependency graph**, not a UI that collects a review.

The `patala_*` capability verbs (below) are the write boundary for this:
```text
patala_propose_translation · patala_propose_claim · patala_attach_evidence ·
patala_request_review · patala_record_review · patala_qualify_claim ·
patala_supersede_interpretation · patala_get_allowed_actions · patala_next_action
```
**Never `patala_set_status`** — expose `patala_get_allowed_actions(object_id)` → the state machine returns
the legal transitions. Write = PROPOSE/RECORD_REVIEW, never SET_TRUTH/ACCEPT.

### Piece 6 — Operational Task/Run Provenance (operations-only, OUTSIDE the epistemic graph)
Agetor-inspired, **no epistemic ontology changes**:
```text
Task (id, kind, target_ids[], objective, dependencies[], policy)
Run (id, task_id, agent, model, input_snapshot, started_at, ended_at, outcome)
RunEvent (run_id, sequence, event_type, artifact_ref, timestamp)
→ Run generated→ C1:… / ArgumentProposal:…
```
**`execution success ≠ epistemic success`** — a task can have ten successful runs and zero accepted
results. The `InputSnapshot` (git_commit, schema_version, corpus_version, source hashes, translation
versions, prompt/model/tool versions, policy version) makes every object's provenance resolvable years
later — **proof of derivation**. This is operations, not a second epistemic universe.

### Piece 7 — the Epistemic Work Queue v0 (redefined by agenticideas — lexicographic policy, NOT ML)
`patala_next_action()` is a **graph-aware triage engine**, but start with **lexicographic policy**, not a
weighted score (no outcome data yet + Goodhart risk):
```text
1 correctness blockers → 2 source/provenance blockers → 3 stale descendants from corrections →
4 high-propagation unresolved cruxes → 5 specialist-review bottlenecks → 6 gold-set expansion →
7 breadth/coverage → 8 speculative enrichment
```
Inside a bucket: `downstream exposure / expected scarce-resource cost`. Core quantity:
```text
epistemic exposure  E(v) = U(v) × I(v) × P(v)     (unresolved uncertainty × importance × propagation)
review leverage     L(v) = Δtrusted-graph / expected-cost
```
**A 5-minute scholar decision on one reading that controls 8 propositions / 3 arguments / 2 syntheses can
outrank translating 50 easy passages.** Every recommendation explains itself:
```text
NEXT ACTION: Review C1-IPVV-X · WHY: unresolved translation qualification · supports 4 argument nodes ·
appears in 2 syntheses · no independent specialist review · upstream evidence complete ·
estimated scholar time: low · EXPECTED EFFECT: resolve/invalidate 11 downstream objects
```
**Piece 7 v0 is an INSTRUMENTATION project, not optimization.** Collect predicted-vs-actual
cost/uncertainty/descendants/reviewer-requirement per resolved task; only after hundreds of events decide
policy vs heuristic vs bandit vs learned.

**The Goodhart warning:** `next_action()` can affect the graph it later measures. Score from quantities
agents can't cheaply manipulate: source-dependency structure, existing downstream published use,
independent review disagreement, staleness propagation, external demand, manually-designated priority.
**Deterministic policy before learned optimization.** Plus the `patala-observer` (read-only): how much
work was rejected, which workflow is reliable, where human reviews overturn agents.

### Pieces 8 & 9 — the Hermes profiles + the coding-agent lane contract

**The 3 Hermes profiles + one kanban board** (the orchestrator fabric):
```bash
hermes profile create patala-producer     # Agent 2 — objects, no adjudication
hermes profile create patala-verifier     # Agent 1 — evaluate, no production mutation
hermes profile create patala-coordinator  # Agent 3 — kanban only, NO impl tools
hermes kanban create patala               # ONE board (don't split — dependency graph stays visible)
```
Capabilities are enforced in **profile config, not prompts**:
```yaml
profile: patala-verifier
capabilities: [patala_read_source, patala_read_claim, patala_propose_review, patala_request_revision]
denied: [patala_accept_claim, patala_adjudicate, git_push_main]
```
The permission architecture **enforces epistemology**. Plus the skill pack (procedural layer):
`skills/ { verify-sanskrit-reading, create-evidence-object, assess-paraphrase-expansion,
review-argument, ingest-pandit-work, reconcile-person-identities, run-scholar-adjudication }`.

**The coding-agent lane contract (in AGENTS.md)** — when a coding agent changes code:
1. Run the projection engine (Piece 3) — confirm DERIVED-LIVE sections still render.
2. Run the staleness engine (Piece 4) — find which HAND-WRITTEN sections drifted.
3. Update those sections (§6 implementations, §7 docs) as part of the change.
4. Commit code + docs together so the chain stays consistent.

## 5. THE COMPLETE LOOP

```text
HUMAN / USER intent
   →  AGENT 3 (coordinator, kanban orchestrator — kanban tools, NO impl tools)
        → decomposes → creates child tasks (kanban_create + kanban_link) → routes → steps back
   →  WORKER LANES claim tasks (Agent 2 / Agent 1 / CODING AGENT / scholar)
        → do work → terminate via kanban_complete / kanban_request_review / kanban_block
   →  PĀṬALA STATE updates (object_registry / ReviewEvents / git commits)
        →  docs_state() regenerates DERIVED-LIVE sections
        →  check_docs_stale.py flags HAND-WRITTEN sections that drifted
   →  REVIEWER gates "done" (sdlc-review skill / scholar) — KANBAN DONE ≠ PĀṬALA ACCEPTED
```

## 6. THE FORMAL RULES (so we can't fuck it up)

1. **Docs are a projection, never the truth.** Truth = `object_registry` + `corpus_state` + ReviewEvents + git.
2. **DERIVED-LIVE sections never get hand-edited** — they render from `docs_state()`.
3. **HAND-WRITTEN sections carry a staleness check** — `check_docs_stale.py` flags drift when code changes.
4. **Agents update state by DOING, not by editing docs.** The `patala_*` verbs are the boundary.
5. **Coding agents are a worker lane** — after a code change, run `docs_state()` + `check_docs_stale.py`
   and update affected HAND-WRITTEN sections. (In AGENTS.md.)
6. **Kanban task DONE ≠ Pāṭala object ACCEPTED.** Kanban = task lifecycle; Pāṭala = epistemic status.
   The reviewer gate is separate.
7. **Don't build a competing runtime** (Temporal/LangGraph/CrewAI/Cloudflare orchestration). Hermes is
   the kernel; Pāṭala layers epistemic state + skills on top.

---

## 6b. THE FULL HERMES TOOLKIT (beyond kanban — what else we can use)

These Hermes features are directly relevant to the live system (all verified against the docs/CLI):

| Feature | What it does | How Pāṭala uses it |
|---|---|---|
| **`/goal` (Ralph loop)** | auto-continuation across turns until a judge says done; **completion contracts** (outcome/verification/constraints/boundaries/stop-when) + **quality gates** (deterministic shell commands that must pass before done) + `/subgoal` + `/goal wait` (park on a background PID) | Agent 2 "translate kramasadbhava to L2 with `factory_certificate` passing as the gate" — the gate makes "done" mechanically checkable, not vibe. Perfect for the factory loop. |
| **Event hooks (plugin)** | `pre_tool_call` / `post_tool_call` / `pre_llm_call` / `on_session_end` / kanban hooks (`kanban_task_claimed/completed/blocked`) — fire custom code at lifecycle points | **Wire the staleness projection**: on `kanban_task_completed` → run `docs_state()` + `check_docs_stale.py`. On `post_tool_call` of a `patala_*` write verb → refresh affected layer pages. This is the anti-staleness mechanism made automatic. |
| **Gateway hooks** | `HOOK.yaml` + `handler.py` in `~/.hermes/hooks/` — logging/alerts/webhooks on `agent:start/end`, `session:*`, `command:*` | Alert on long-running factory tasks, log agent activity, notify on overnight failures. |
| **Outbound webhooks** | push signed lifecycle events to external HTTP endpoints | scholarly CI ("GitHub CI for epistemology" — CANONICAL #10): a C1 change → webhook → Pāṭala dependency audit → PR comment. |
| **`cron`** | scheduled jobs (`--skill --workdir --deliver`) | the "translate while I sleep" loop (Agent 3 scheduled tasks). |
| **`--worktree`** | isolated git worktree per agent | git isolation so Agent 1 can never stage Agent 2's files. |
| **`checkpoints`** | shadow-git snapshots before writes | rollback a bad regeneration ("mistakes don't compound"). |
| **`memory` + `memory-graph`** | built-in MEMORY.md + timeline of learned skills/memories | the `patala` profile soul + the "what we've learned" timeline. |
| **`sessions` (FTS5)** | persistent searchable work | Agent 3 recalls "why was bhavopahara blocked last time?" |
| **`insights`** | token/cost/tool-pattern analytics | operational reporting ("what did we spend? what tools are hot?"). |
| **`dashboard` / `serve`** | web UI / headless backend | the Agent-3 control panel ("what changed overnight?"). |
| **`skills` + `bundles`** | procedural memory (executable doctrine) + multi-skill aliases | `patala-translate`, `patala-validate`, `patala-review`, `patala-adversarial-review` as skills; `bundles` = a pipeline alias. |
| **`moa` / `fallback`** | mixture-of-agents + model failover | resilience (no single-model point of failure). |
| **`mcp`** | run Hermes as MCP server + manage MCP servers | the `patala_*` verb layer (Piece 3). |

**The key additions this gives us beyond the original 5 pieces:**
- **`/goal` + quality gates** = deterministic "done" for factory tasks (ties directly to the reviewer-gate rule).
- **Hooks** = make `docs_state()` + `check_docs_stale.py` run AUTOMATICALLY on task completion, not manually. This is the single biggest improvement — the projection updates itself.
- **`checkpoints`** = the rollback guard so a bad agent run can't corrupt state.

---

## 6c. THE ECOSYSTEM OF ORGANS (the 15-plane review)

A second peer review (`docs-cache/ecosystem-15planes.md`) reframed the endgame: **not one giant agent
framework, but a stack of narrow systems around a small Pāṭala kernel, with Hermes as the execution
plane.** The golden rule is unchanged: **Pāṭala decides what is true and what matters; Hermes decides
who does the work and how.**

**The kernel + organs model:** Pāṭala owns a brutally-good small kernel (identity, provenance, passages,
claims, arguments, reviews, trajectories, events, permissions, the capability API, the epistemic
review-gate, the learner semantics, the projection engine, `patala_next_action()` triage). Everything
else is an ORGAN — pinched/adapted/replaced from the ecosystem:

| Plane | Pinch from |
|---|---|
| Agent control | Hermes (primary) · Gas Town/City (workflows) · **Agetor** (Task≠Run) · Overstory (mail/watchdog) · agtx (allowed_actions) · mcp_agent_mail (leases) |
| Graph triage | **Beads Viewer** (PageRank/betweenness/critical-path → structured output) → `patala_next_action()` |
| Review gating | **Vouch** (proposal→validation→review→accept, cited evidence, append-only) · Sage Wiki · llm-wiki-newsroom (reground) |
| Document ingestion | **Docling (+MCP)** · GROBID · S2ORC doc2json · **Zotero Translation Server** |
| Bibliography | Zotero MCP Plus · Cita (adapters) |
| Manuscripts | **Mirador 4** (+TextOverlay) · Recogito · INCEpTION (adjudication concepts) |
| Argument interop | AIF/xAIF adapters (ARG Tech) |
| Claim checking | RARR · RefChecker · GraphCheck · DSPy (optimize vs gold) · IAM |
| Consumer temporal | **Graphiti** (as a projection, NOT canonical) · CoWork OS · DeepTutor (L1/L2/L3 memory) |
| Learner model | pyBKT · Dialogue-KT · OATutor · OpenTutor (UX) · **adaptive-knowledge-graph** (interfaces gold) |
| KG→docs | Epicenter (DB canonical, Markdown a view) · SQLite Sync (offline scholars, later) |
| Observability | **Phoenix** / Langfuse (external trace plane; Pāṭala review stays internal) |
| Media | **Remotion** · **OpenMontage** (research→script→assets→edit) · remotion-superpowers · frankxai/remotion-video |
| Distribution | **Postiz** (+ Postiz Agent) — the Hermes publishing lane calls it |
| Feedback organism | the closing loop: ledger → agents → gated truth → products → interactions → new gaps |

**Immediate clone set (harvest, don't vendor):** Hermes · Gas Town · Gas City · Overstory · agtx ·
mcp_agent_mail · Agetor · Beads · Beads Viewer · Vouch · Sage Wiki · llm-wiki-newsroom · Docling (+MCP) ·
GROBID · Zotero Translation Server · Zotero MCP Plus · Cita · Mirador 4 · Mirador TextOverlay · Recogito ·
AIF arg-datasets/oAMF · RARR · RefChecker · GraphCheck · DSPy · Graphiti · CoWork OS · DeepTutor · pyBKT ·
Dialogue-KT · OATutor · OpenTutor · adaptive-knowledge-graph · Epicenter · Phoenix · Langfuse · Remotion ·
OpenMontage · remotion-superpowers · frankxai/remotion-video · Postiz · Postiz Agent.

**The "don't build" boundary (confirmed):** PDF parsing · manuscript rendering · generic agent
scheduling · generic trace observability · social upload adapters · BKT itself · basic annotation
widgets · generic citation scraping. **The moat = the kernel + the review-gated promotion + the
capability API + the projection engine.**

## 7. CURRENT STATE (honest, 2026-08-14)

| Piece | Status |
|---|---|
| Tier 1 — Canonical State API (object_registry, corpus_state, Atlas, ReviewEvents) | ✅ built |
| Append-only Event Log (`object-events.jsonl`) | ✅ exists — extend to first-class events |
| Projection Engine (`docs_state` → docs/JSON/dashboard/AGENTS/API) | ❌ to build |
| Staleness/Provenance Engine (`check_docs_stale.py`) | ❌ to build |
| Capability MCP (`patala_*` verbs) | ❌ to build (DEV-PLAN Gate 1) |
| Task≠Run≠Attempt + Leases | ❌ to build (run/attempt model + resource leases) |
| Observer/Triage (`patala_next_action`, `patala-observer`) | ❌ to build |
| 3 Hermes profiles (producer/verifier/coordinator) | ❌ only `patala` profile exists |
| One kanban board | ❌ no board yet |
| STATE.yaml as projection | ⚠️ currently hand-maintained (to demote) |
| Coding-agent lane contract | ⚠️ needs the rule added to AGENTS.md |

**Peer-reviewed stack (cloned + studied 2026-08-14):** agetor (Task≠Run, base-commit pinning),
beads_rust (append-only audit, SQLite↔JSONL projection), beads_viewer (graph triage, PageRank/
betweenness), mcp_agent_mail (leases, identities, Git+SQLite). These confirm the 7-piece model; we adapt
their patterns, never ship their code wholesale.

## 8. BUILD ORDER (dependency-ordered — the 7 pieces + fabric)

1. **Canonical State API** (Tier 1) — confirm object_registry + corpus_state + ReviewEvents expose reads.
2. **Append-only Event Log** (Piece 2) — extend `object-events.jsonl` to a first-class event primitive.
3. **Projection Engine** (Piece 3) — canonical state → docs/JSON/dashboard/AGENTS/API/scholar views.
4. **Staleness/Provenance Engine** (Piece 4) — provenance-hash staleness + CI drift check.
5. Wire DERIVED-LIVE sections into the layer pages + NAVIGATION (render from the projection engine).
6. **Capability MCP** (Piece 5 verbs) — the `patala_*` verbs + `patala_get_allowed_actions`.
7. **Scholar Attestation Vertical** (Piece 5) — one gold argument, real scholar adjudicates, correction
   propagates (the review gate itself is already built — this is the human layer over it).
8. **Operational Task/Run Provenance** (Piece 6) — Task≠Run + InputSnapshot, operations-only, outside the epistemic graph.
9. **Epistemic Work Queue v0** (Piece 7) — lexicographic policy + instrumentation, NOT ML.
10. The 3 Hermes profiles + kanban board + Agent-3 orchestrator + the skill pack.
11. Add the coding-agent lane contract to AGENTS.md.
12. Demote STATE.yaml to a projection (regenerated, not hand-edited).

> **The immediate frontier (agenticideas):** NOT making Pāṭala more agentic — it's proving a serious
> scholar can enter, disagree at the right epistemic level, and make the whole graph more correct without
> destroying provenance. The Scholar Attestation Vertical (Piece 5) is the priority.

---

## 9. HOW IT LINKS

- **Layers 00 (governance)** — the rules above are the governance.
- **Layers 03/05 (factory/research)** — Tier 1 state they produce.
- **Layer 07 (verification)** — the reviewer gate.
- **Layer 10 (this)** — the orchestration + projection.
- **Hermes** — the execution kernel (`handover/hermes/CANONICAL.md`, `BACKEND-MODEL.md`,
  `HERMES-AGENT3-FACTORY-COORDINATOR.md`, `DEV-PLAN.md`).
- **Our agent0/AGENTS.yaml/STATE.yaml** — becomes a projection, not a second orchestration DB.
- **NAVIGATION.md** — the presentation layer renders live state.

*This is the canonical spec. Build the 5 pieces in order; the live system is complete when `docs_state()`
+ `check_docs_stale.py` + the `patala_*` verbs + the 3 profiles + the coding-agent contract are all in
place and wired into NAVIGATION + the layer pages.*
