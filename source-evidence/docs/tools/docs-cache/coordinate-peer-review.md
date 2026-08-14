Yes. I went much deeper on the **state ↔ docs ↔ agents** problem rather than just looking for orchestration frameworks.

One limitation first: `~/projects/patala/handover/hermes/BACKEND-MODEL.md` is not mounted in my environment, so I could not actually read that local file. I did, however, work from the design you pasted and read the relevant current Hermes architecture/docs around Kanban, profiles, prompt assembly, skills, sessions/toolsets, and worker behavior. The important findings actually sharpen your proposed model quite a bit. ([GitHub][1])

# The strongest conclusion

Your sentence is almost right:

> Hermes owns the task lifecycle; Pāṭala owns epistemic state; docs are a projection of Pāṭala state.

I would make it slightly stricter:

```text
HERMES          = execution/lifecycle truth
PĀṬALA          = domain/epistemic truth
GIT             = implementation/history truth
DOCS            = human-readable projections
SKILLS          = procedural policy
SESSIONS        = historical observations
AGENT MEMORY    = convenience cache, never authority
```

That separation is the core.

The mistake I see repeatedly in other systems is making one storage mechanism do too much:

```text
Markdown as task DB
Markdown as memory
Markdown as documentation
Markdown as agent instructions
Markdown as system state
```

Eventually the same fact exists five times and diverges.

Hermes itself demonstrates both sides of this problem. Its Kanban uses durable SQLite specifically because cross-agent work should not depend on conversation context, while its skills are deliberately file-based procedural knowledge loaded on demand. Hermes profiles separately isolate config, sessions, memories, skills, cron state, etc. ([GitHub][2])

And amusingly, Hermes has already had a real `AGENTS.md is stale` issue because implementation evolved while manually maintained architecture documentation lagged behind. That is almost exactly the failure mode you're designing Pāṭala to prevent. ([GitHub][3])

---

# The architecture I would actually build

```text
                         USER / EXTERNAL EVENT
                                  │
                                  ▼
                        HERMES COORDINATOR
                           task decomposition
                                  │
                                  ▼
                    ┌──────────────────────────┐
                    │     HERMES KANBAN       │
                    │ lifecycle/control plane │
                    │                         │
                    │ todo/ready/running      │
                    │ blocked/review/done     │
                    │ dependencies/comments   │
                    │ leases/heartbeat/runs   │
                    └────────────┬─────────────┘
                                 │
                      dispatches │ work
                                 ▼
        ┌──────────────────────────────────────────────┐
        │                 WORKER LANES                 │
        │                                              │
        │ producer   verifier   coder   researcher     │
        │ scholar    ingestion  docs     synthesis     │
        └──────┬────────┬────────┬────────┬────────────┘
               │        │        │        │
               └──────────────┬─────────────────────────┘
                              │
                   ONLY VIA CAPABILITY APIs
                              │
                              ▼
              ┌──────────────────────────────┐
              │        PĀṬALA CORE           │
              │                              │
              │ Work / Passage / Claim       │
              │ Evidence / Argument          │
              │ ReviewEvent / Trajectory     │
              │ CorpusState / Registry       │
              └──────────────┬───────────────┘
                             │
                     canonical state
                             │
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
       EVENTS             PROJECTIONS          GIT
   append-only audit      docs/API/UI        implementation
          │                  │                  │
          │                  ▼                  │
          │          generated live docs       │
          │                  │                  │
          └──────────────┬───┴──────────────────┘
                         ▼
                 CONSISTENCY CHECKER
```

And there should be **no direct arrow**:

```text
agent → canonical Markdown doc
```

for facts that can be represented structurally.

That is the rule that saves you later.

---

# Hermes itself: what I would actually use

Hermes Kanban is stronger than I originally realized.

Every Kanban task is durable state in SQLite. Worker processes interact through the `kanban_*` tools rather than mutating some shared conversation. Dependencies are explicit; comments survive worker death; stale claims can be reclaimed; workers can be independent OS processes; multiple boards can exist. ([GitHub][1])

That means **don't rebuild lifecycle orchestration inside Pāṭala.**

Use Hermes for:

```text
task identity
assignment
dependency/blocking
worker spawning
heartbeat
retries
comments
blocked state
completion state
run history
```

But absolutely do **not** treat:

```text
kanban_complete(task)
```

as:

```text
patala_accept(result)
```

These need separate transitions:

```text
RUNNING
   │
   ▼
IMPLEMENTATION_COMPLETE
   │
   ▼
REVIEW
   │
   ├── reject ─────► READY
   │
   ▼
TECHNICALLY_ACCEPTED
   │
   ▼
DOMAIN/EPistemic REVIEW
   │
   ▼
PĀṬALA ACCEPTED
```

For coding tasks you may stop at technical acceptance.

For a Sanskrit interpretation, **only Pāṭala's review/event machinery controls epistemic acceptance.**

---

# Hermes profiles map very nicely onto your system

Hermes profiles are genuinely separate agent homes: each gets its own config, memory, sessions, skills, cron jobs and state. ([Hermes Agent][4])

So I would use profiles aggressively:

```text
patala-coordinator
patala-producer
patala-verifier
patala-coder
patala-ingestion
patala-research
```

But **roles should live in Pāṭala/Hermes config, not in prompts alone.**

For example:

```yaml
profile: patala-producer

capabilities:
  - patala_read_source
  - patala_propose_translation
  - patala_propose_claim

denied:
  - patala_accept_claim
  - patala_adjudicate
  - git_push_main
```

Versus:

```yaml
profile: patala-verifier

capabilities:
  - patala_read_source
  - patala_read_claim
  - patala_propose_review
  - patala_request_revision
```

Scholar:

```yaml
profile: scholar

capabilities:
  - patala_adjudicate
  - patala_supersede_interpretation
```

The permission architecture should enforce epistemology.

That's much stronger than:

> "Agent 1, remember you're a verifier."

---

# Hermes Skills should become Pāṭala's procedural layer

Hermes treats skills as **procedural knowledge**, separate from persistent factual memory. Skills are filesystem documents, progressively disclosed only when needed. ([GitHub][5])

This maps almost perfectly onto Pāṭala:

```text
FACT:
IPK 1.5.11 has reading X
        ↓
Pāṭala DB

PROCEDURE:
How to assess a Sanskrit negation scope dispute
        ↓
Hermes Skill
```

Examples:

```text
skills/
  verify-sanskrit-reading/
  create-evidence-object/
  assess-paraphrase-expansion/
  review-argument/
  ingest-pandit-work/
  reconcile-person-identities/
  run-scholar-adjudication/
```

Skills can include:

```text
SKILL.md
references/
templates/
scripts/
```

Hermes already supports exactly this layout. ([GitHub][5])

This gives you a beautifully clean division:

```text
Pāṭala DB     = WHAT we know
Skill         = HOW we operate
Kanban        = WHAT needs doing
Git           = WHAT changed in implementation
Docs          = WHAT humans should currently see
Session store = WHAT happened in agent conversations
```

That is the ontology for the infrastructure itself.

---

# Now the GitHub gold

I started with Gas Town because it's a useful reference architecture, but the smaller descendants/adjacent projects are more directly reusable.

## Tier 1: understand these, don't blindly adopt them

| Project       | What matters for Pāṭala                           |
| ------------- | ------------------------------------------------- |
| Gas Town      | persistent work identity + worktrees + roles      |
| Gas City      | decomposes orchestration into reusable primitives |
| Hermes Kanban | already your lifecycle control plane              |
| Beads         | durable dependency graph for agent work           |

### Gas Town

[https://github.com/gastownhall/gastown](https://github.com/gastownhall/gastown)

Gas Town's particularly useful idea is the **hook**: a worker's persistent state is not synonymous with its live process. Work survives agent restart. Git worktrees provide durable implementation isolation. ([GitHub][6])

Its rough model:

```text
Mayor
  ↓
Convoy
  ↓
Beads
  ↓
Agents
  ↓
Hooks/worktrees
```

For Pāṭala:

**Do not clone Gas Town.**

Hermes already covers much of that control-plane territory.

Steal:

```text
persistent task identity
worker identity
resumable work attachment
worktree isolation
role-specific permissions
```

---

### Gas City

[https://github.com/gastownhall/gascity](https://github.com/gastownhall/gascity)

This may actually be more interesting architecturally than Gas Town because it extracts the reusable orchestration primitives:

```text
Agent
Bead
Formula
Rig
routing
health
orders
```

rather than hardcoding one mega workflow. ([GitHub][7])

The equivalent concept you want is:

```text
Pāṭala Workflow Formula

translate_passage
verify_passage
adjudicate_reading
ingest_work
reconcile_person
build_argument
publish_lesson
```

Each becomes a declarative workflow over Hermes tasks.

That's good.

---

# Tier 2: this is where it gets really useful

## Agetor

[https://github.com/alamops/agetor](https://github.com/alamops/agetor)

This is one of the best small builds I found for you.

Its state model is extremely clean:

```text
SQLite
  tasks
  runs
  events
  projects
  harnesses
  approvals

Git
  per-task worktrees

tmux
  persistent interactive sessions
```

Every task pins the base commit it started from, so reruns are reproducible. It keeps task execution history separate from task identity. It also explicitly differentiates an agent process exiting successfully from a human deciding the task is actually done. ([GitHub][8])

**Steal directly:**

```text
Task != Run
```

This matters enormously.

Pāṭala currently needs:

```text
WorkItem
  id

Run
  run_id
  work_item_id
  agent
  model
  prompt_hash
  started_at
  source_commit
  status
  outputs[]
```

Then:

```text
task P17
  run #1 failed
  run #2 produced candidate
  run #3 revised after review
```

Never overwrite the history.

That should go into your formal system design.

---

# Mozzie

[https://github.com/usemozzie/mozzie](https://github.com/usemozzie/mozzie)

Very underrated for your exact problem.

It has:

```text
work-item state machine
dependency management
sub-work items
attempt history
rejection feedback
worktrees
SQLite
orchestrator conversations
review workflow
```

Most interestingly, rejected work feeds the **attempt history back into the next run**. ([GitHub][9])

That gives us another Pāṭala primitive:

```text
Attempt
```

not merely `Run`.

A future agent should see:

```text
previous attempts:
1. proposed X
   rejected because Y

2. proposed Z
   rejected because Q
```

instead of rediscovering the same bad path.

That is enormously important for scholar review.

Imagine:

```text
InterpretationProposal I77
Attempt 1 → rejected: overreads ablative
Attempt 2 → rejected: ignores Jayaratha parallel
Attempt 3 → accepted
```

You're accumulating **negative epistemic knowledge**.

Very valuable.

---

# CAS

[https://github.com/codingagentsystem/cas](https://github.com/codingagentsystem/cas)

CAS combines:

```text
tasks
rules
skills
memory
SQLite
FTS
tree-sitter code understanding
worktree worker factory
```

and exposes the context layer via MCP. ([GitHub][10])

What I like for Pāṭala isn't its full factory.

It's its explicit separation:

```text
FACTORY
vs
CONTEXT SYSTEM
```

You've independently arrived at the same distinction:

```text
Hermes orchestration
vs
Pāṭala state/context
```

Good confirmation.

I wouldn't clone CAS.

Study its MCP context APIs.

---

# agtx

[https://github.com/fynnfluegge/agtx](https://github.com/fynnfluegge/agtx)

This one has a particularly strong idea:

> the orchestrator asks the state machine what transitions are allowed.

It exposes the board over MCP; the orchestrator retrieves `allowed_actions`, then asks the control plane to transition state. The TUI/server executes the side effects. ([GitHub][11])

That suggests Pāṭala should not expose:

```text
patala_set_status("accepted")
```

It should expose:

```text
patala_get_allowed_actions(object_id)
```

returning:

```json
{
  "allowed": [
    "request_review",
    "qualify_claim",
    "add_evidence"
  ]
}
```

Then explicit verbs perform the transitions.

That's much safer.

This is **one I would actually borrow structurally.**

---

# And now the really interesting ecosystem

## Beads

[https://github.com/gastownhall/beads](https://github.com/gastownhall/beads)

Beads has become a distributed dependency-aware task graph specifically for coding agents. Current versions use Dolt as canonical issue storage and treat JSONL as passive export/interchange rather than database truth. ([GitHub][12])

Its most important philosophical rule is:

> don't duplicate task state into Markdown TODOs.

Their `AGENTS.md` literally tells agents not to maintain Markdown task lists because Beads owns task truth. ([GitHub][13])

That supports your thesis strongly.

However, there is also a useful warning: users have hit synchronization complexity when multiple checkouts/worktrees have separate Dolt instances. ([GitHub][14])

So I would **not** introduce Dolt into Pāṭala just because Beads does.

You already have Hermes SQLite.

But steal:

```text
typed dependencies
deterministic ready-work calculation
discovered-from edges
structured JSON agent API
```

Especially:

```text
discovered_from
```

An agent working on X discovers Y:

```text
TASK Y
  discovered_from: TASK X
```

That lets you later analyze where work originated.

---

# Beads Rust — this is probably more aligned with you

[https://github.com/Dicklesworthstone/beads_rust](https://github.com/Dicklesworthstone/beads_rust)

This is a smaller reimplementation with a very interesting philosophy:

```text
SQLite = operational state
JSONL = git-readable projection
Git operations = external responsibility
append-only events = audit
```

It deliberately refuses to execute Git itself. ([GitHub][15])

That "non-invasive" design is very attractive for Pāṭala.

Rather than making every subsystem secretly mutate everything else:

```text
Pāṭala emits state
Git worker commits
Hermes dispatches
docs compiler projects
```

Each component does one thing.

### I would absolutely clone this to study it

```bash
git clone https://github.com/Dicklesworthstone/beads_rust
```

Not to ship it wholesale.

Study:

```text
storage/
events/
sync/
robot JSON interfaces
migration strategy
reconciliation behavior
```

---

# Beads Viewer: extremely relevant

[https://github.com/Dicklesworthstone/beads_viewer](https://github.com/Dicklesworthstone/beads_viewer)

This may contain something surprisingly valuable for Pāṭala.

It applies graph algorithms to the task dependency graph:

```text
PageRank
betweenness
critical path
HITS
eigenvector centrality
k-core
cycle detection
```

and gives agents deterministic robot-mode JSON rather than asking the LLM to reason over the raw graph. ([GitHub][16])

That maps beautifully to your argument/evidence graph.

You should **not ask an LLM**:

> which unresolved claim is most important?

when Pāṭala can calculate:

```text
downstream dependency count
betweenness
argument centrality
uncertainty
review deficit
citation importance
```

Then produce:

```text
patala_next_action()
```

from deterministic graph metrics.

This directly improves your proposed Gate 1 MCP tool.

Your `patala_next_action` should eventually be a **graph-aware triage engine**, not an LLM guess.

Something like:

[
priority(v)=
\alpha D(v)
+\beta B(v)
+\gamma U(v)
+\delta I(v)
-\lambda C(v)
]

where:

* (D) = downstream dependency impact
* (B) = betweenness/structural importance
* (U) = uncertainty
* (I) = user/research importance
* (C) = estimated cost

That is proper agentic scheduling.

---

# MCP Agent Mail — this is excellent

[https://github.com/Dicklesworthstone/mcp_agent_mail](https://github.com/Dicklesworthstone/mcp_agent_mail)

This one is seriously worth studying.

Architecture:

```text
Agents
   │
   ▼
FastMCP
   │
   ├────────► SQLite/FTS
   │
   └────────► Git-readable archive
```

It maintains agent identities, inboxes, threads and file reservation leases. Messages have durable thread identities. SQLite exists for query/search, while Git stores human-auditable artifacts. ([GitHub][17])

Most importantly, it has **advisory file leases**:

```text
Agent A reserves:
pipeline/object_registry.py

Agent B wants same file
      ↓
conflict surfaced
```

with TTLs and stale-owner recovery. ([GitHub][17])

Hermes gives you task ownership, but **task ownership is not necessarily resource ownership**.

These are different:

```text
Agent A owns TASK-77

TASK-77 may touch:
  schema.py
  registry.py

Agent B owns TASK-82

TASK-82 may also touch:
  registry.py
```

So I'd consider a lightweight:

```text
patala_resource_lease()
```

or reuse Agent Mail for coding lanes.

For epistemic objects this becomes even more interesting:

```text
lease:
  object = translation:IPVV:1.3.5
  purpose = adjudication
  mode = exclusive
```

although scholar review may want soft, rather than exclusive, concurrency.

---

# Thread

This is mentioned in the Beads community tooling list:

[https://github.com/jklenk/thread](https://github.com/jklenk/thread)

It is a read-only forensic/analytics layer over Beads history that computes things such as fidelity, rework cost and session compliance. ([GitHub][18])

This suggests a subsystem Pāṭala does **not** currently emphasize enough:

```text
OBSERVABILITY PLANE
```

Not:

```text
what is the state?
```

but:

```text
how did the system arrive here?
how much work was rejected?
which agent creates the most rework?
which workflow produces reliable outputs?
which tasks repeatedly reopen?
where do human reviews overturn agents?
```

That becomes incredibly valuable once you're running 20+ agents.

I'd call it:

```text
patala-observer
```

Read-only.

Never edits truth.

---

# EchoVault

[https://github.com/mraza007/echovault](https://github.com/mraza007/echovault)

This is a good little memory design.

It uses:

```text
Markdown vault = durable human-readable memories
SQLite FTS/vector index = retrieval layer
compact summaries = pointer layer
full documents = loaded on demand
```

rather than jamming everything into prompts. ([GitHub][19])

The exact implementation isn't needed, because Hermes already has session/memory/skills.

But steal the retrieval philosophy:

```text
IDENTIFIER
SUMMARY
RELEVANCE SIGNAL
      ↓
load full object only if needed
```

Pāṭala agents should see:

```text
Claim C491
"Recognition presupposes continuity..."
confidence=.72
```

not automatically the 12 KB provenance bundle.

Then:

```text
patala_get_claim(C491, depth="full")
```

Progressive disclosure should apply to your epistemic state exactly as Hermes applies it to Skills. ([GitHub][5])

---

# Repowise has a tiny feature I really want you to copy

[https://github.com/repowise-dev/repowise](https://github.com/repowise-dev/repowise)

Every response includes metadata about the index state such as which commit was indexed and warns when the indexed state no longer matches live HEAD. ([GitHub][20])

THIS directly improves your `check_docs_stale.py`.

Don't merely do:

```text
code file touched → docs possibly stale
```

Track provenance of the projection:

```yaml
generated_from:
  registry_commit: 51fab9
  corpus_state_hash: 4be02...
  schema_version: 17
  renderer_version: 9
generated_at: ...
```

Then a doc can prove:

```text
CURRENT
STALE
UNKNOWN
```

deterministically.

This is much better than timestamps.

---

# wshobson/agents has exactly the generated-artifact discipline

[https://github.com/wshobson/agents](https://github.com/wshobson/agents)

Their agent infrastructure has canonical source definitions and generated harness-specific outputs. Generated outputs are committed, but **never hand edited**; CI regenerates them and fails if generated files drift from canonical source. ([GitHub][21])

This is almost precisely how your docs should work.

Instead of:

```text
docs_state() modifies some Markdown
```

define:

```text
SOURCE
  docs/specs/
  registry/
  schema/
        │
        ▼
    generator
        │
        ├─ AGENTS.md fragments
        ├─ architecture status
        ├─ layer status
        ├─ MCP reference
        └─ object counts
```

Then CI:

```bash
generate-docs
git diff --exit-code
```

Failure means:

> generated projection does not match canonical state.

**This is stronger than staleness warnings.**

For fully-derived sections, drift should be a CI failure.

---

# Conductor OSS

[https://github.com/charannyk06/conductor-oss](https://github.com/charannyk06/conductor-oss)

Another nice hybrid:

```text
CONDUCTOR.md       human planning surface
SQLite             runtime sessions/attempts/coordination
worktrees          implementation isolation
```

It supports many CLI agents including Hermes, Codex, Claude, OpenCode, etc. ([GitHub][22])

It confirms a general pattern:

> Markdown works well as an operator interface, not as low-level runtime state.

This is how I'd treat Pāṭala docs.

---

# Kata

[https://github.com/gannonh/kata](https://github.com/gannonh/kata)

This is interesting because its orchestrator writes project state to disk as structured files, while Kata Context maintains a tree-sitter-derived dependency graph in SQLite. ([GitHub][23])

It supports explicit phases:

```text
discuss
plan
execute
verify
```

I wouldn't use Kata.

But its phase isolation is worth borrowing for coding work:

```text
SPEC
  ↓
PLAN
  ↓
IMPLEMENT
  ↓
VERIFY
  ↓
ACCEPT
```

Each phase emits an artifact.

That makes handoff/restart much cleaner.

---

# The coolest accidental discovery: Dicklesworthstone's whole ecosystem

[https://github.com/Dicklesworthstone](https://github.com/Dicklesworthstone)

This person has basically built a personal Unix-like agent infrastructure ecosystem.

Beyond Agent Mail and Beads Viewer, there are projects for:

```text
CASS           session history search
CASS Memory    memory layers
NTM            tmux multi-agent orchestration
UBS            precommit bug scanning
SLB            peer approval for dangerous operations
Eidetic Engine durable local-first memory
```

The GitHub profile currently describes these as complementary pieces rather than one giant framework. ([GitHub][24])

**This philosophy is exactly what I think Pāṭala should adopt.**

Don't create:

```text
patala-agent-framework.py
```

with 40 responsibilities.

Create small deterministic infrastructure components.

```text
patala-state
patala-events
patala-docs
patala-triage
patala-review
patala-observer
patala-mcp
```

Hermes composes them.

---

# So your five missing seams become seven

Your existing list was:

```text
docs_state()
check_docs_stale.py
patala_* MCP verbs
Hermes profiles
coding-agent lane
```

After this research I would change it to:

```text
1. CANONICAL STATE API
2. EVENT LOG
3. PROJECTION ENGINE
4. STALENESS/PROVENANCE ENGINE
5. CAPABILITY MCP
6. RESOURCE/OBJECT LEASES
7. OBSERVABILITY/TRIAGE ENGINE
```

### 1. Canonical state API

This is your existing:

```text
object_registry
corpus_state
ReviewEvents
```

No Markdown authority.

---

### 2. Append-only event log

This is missing from your description as a first-class primitive.

Every meaningful mutation should produce:

```json
{
  "event_id": "...",
  "object_id": "...",
  "operation": "claim_qualified",
  "actor": "patala-verifier",
  "task_id": "...",
  "run_id": "...",
  "before_hash": "...",
  "after_hash": "...",
  "timestamp": "..."
}
```

Then current state is:

```text
snapshot
```

while history is:

```text
events
```

Do not try to infer all domain history from Git diffs.

---

### 3. Projection engine

I'd rename:

```text
docs_state()
```

to something broader:

```text
project_state()
```

because Markdown isn't the only consumer.

```text
canonical state
      │
      ▼
projection engine
   ├─ docs
   ├─ JSON
   ├─ dashboard
   ├─ AGENTS context
   ├─ API
   └─ scholar views
```

Then:

```text
docs_state()
```

can just be one renderer.

---

### 4. Staleness/provenance engine

Not simply:

```text
file X changed therefore doc Y stale
```

Use explicit dependencies.

```yaml
projection: docs/layers/03-factory.md#live-state

depends_on:
  - registry:ObjectType
  - schema:Translation
  - file:pipeline/object_registry.py

generated_from:
  git_commit: abc123
  state_hash: def456
  renderer_version: 4
```

Then:

```text
state hash changed
        ↓
projection stale
```

And for hand-written claims:

```yaml
section: "Implementation notes"

depends_on:
  - pipeline/object_registry.py
  - pipeline/compile_published.py

verified_at_commit:
  object_registry.py: 98a2...
  compile_published.py: 12cd...
```

Now staleness is deterministic.

---

### 5. Capability MCP

This should become the **only supported agent-write boundary** for domain state.

Not CRUD.

Avoid:

```text
patala_update_object(...)
```

Prefer domain verbs:

```text
patala_propose_translation()
patala_propose_claim()
patala_attach_evidence()
patala_request_review()
patala_record_review()
patala_qualify_claim()
patala_supersede_interpretation()
patala_accept_candidate()
patala_get_allowed_actions()
patala_next_action()
```

The verbs carry your epistemology.

---

### 6. Leases

Borrow the Agent Mail idea.

```text
patala_claim_work()
```

for task ownership.

And perhaps:

```text
patala_reserve_object()
patala_reserve_surface()
```

for high-conflict resources.

Coding agents especially need filesystem-level leases if they're not isolated entirely by worktrees.

---

### 7. Observer/triage

Borrow Beads Viewer + Thread.

```text
patala_next_action()
```

should inspect:

```text
task dependency
epistemic dependency
uncertainty
centrality
human demand
review backlog
failure/rework history
agent competence
```

rather than simply asking Hermes' coordinator to invent the next task.

This is where Pāṭala eventually becomes **self-directing in a non-hand-wavy sense**.

---

# Most important distinction: four kinds of state

I would codify this in `10-live-system.md`.

```text
DOMAIN STATE
"What is currently believed/accepted?"
Owner: Pāṭala

WORK STATE
"What is someone currently doing?"
Owner: Hermes Kanban

IMPLEMENTATION STATE
"What code actually exists?"
Owner: Git/filesystem/tests

PROJECTION STATE
"What do humans currently see?"
Owner: projection engine
```

And then a fifth:

```text
PROCEDURAL STATE
"How should this kind of work be performed?"
Owner: versioned Hermes skills
```

These must never silently substitute for each other.

For example:

```text
KANBAN:
"Translation 1.3.5 done"

does NOT imply

PĀṬALA:
"Translation 1.3.5 accepted"
```

Similarly:

```text
DOC:
"39/41 tests passing"

does NOT establish that today.

It must point to:
TestRun → commit → results
```

That's the universal rule.

---

# Your docs should probably look like this

```markdown
# Factory Layer

## Contract
HAND-WRITTEN
What this layer means and its invariants.

## Architecture
HAND-WRITTEN
Stable design explanation.

## Live state
<!-- PATATA:BEGIN generated=factory-state -->
GENERATED.
DO NOT EDIT.
<!-- PATALA:END -->

## Known debt
GENERATED from structured issues / state.

## Implementation notes
HAND-WRITTEN.
Tracked against code dependencies.

## History
GENERATED from relevant events/releases.
```

Then:

```bash
patala docs generate
patala docs verify
```

`verify` regenerates into temp and diffs.

For fully derived sections:

```text
drift = FAIL
```

For hand-written sections:

```text
dependency changed = STALE/VERIFY
```

That's cleaner than trying to automatically rewrite prose whenever code changes.

---

# What I would actually clone tomorrow

If I were the coding agent implementing your infrastructure, I would clone **five**, not fifty:

```bash
git clone https://github.com/NousResearch/hermes-agent
git clone https://github.com/alamops/agetor
git clone https://github.com/Dicklesworthstone/beads_rust
git clone https://github.com/Dicklesworthstone/beads_viewer
git clone https://github.com/Dicklesworthstone/mcp_agent_mail
```

Then inspect these exact concerns:

```text
Hermes
  kanban schema
  dispatcher claim semantics
  profile isolation
  skill loading
  worker tools

Agetor
  Task vs Run
  base-ref pinning
  approval state
  event stream

beads_rust
  append-only audit
  SQLite ↔ JSONL projection
  deterministic ready-work
  reconcile logic

beads_viewer
  graph triage
  critical path
  PageRank/betweenness
  robot JSON outputs

mcp_agent_mail
  identities
  leases
  stale lease recovery
  Git + SQLite dual representation
  audit architecture
```

Everything else can be reference material.

---

# The resulting Pāṭala system

I think this is the system you're actually converging on:

```text
                             HERMES
                 coordination / scheduling
                             │
                 ┌───────────┴────────────┐
                 ▼                        ▼
             KANBAN                    SKILLS
          work lifecycle              procedures
                 │
                 ▼
             WORKER RUN
                 │
             task_id/run_id
                 │
                 ▼
            PĀṬALA MCP
         capability boundary
                 │
                 ▼
      ┌─────────────────────────┐
      │ CANONICAL DOMAIN STATE  │
      │                         │
      │ entities                │
      │ evidence                │
      │ interpretations         │
      │ arguments               │
      │ ReviewEvents            │
      │ trajectories            │
      └───────────┬─────────────┘
                  │
          append event
                  │
                  ▼
            EVENT HISTORY
                  │
        ┌─────────┼───────────┐
        ▼         ▼           ▼
      DOCS       API          UI
        │
        ▼
 provenance/staleness
        │
        ▼
       CI

           separate plane:

           GIT/WORKTREES
                │
                ▼
          CODE / SCHEMAS
                │
                ▼
              TESTS
                │
                ▼
        technical acceptance
```

And then sitting above everything:

```text
             PĀṬALA TRIAGE

epistemic graph + work graph + run history
                 │
                 ▼
          patala_next_action()
                 │
                 ▼
          Hermes coordinator
```

That last loop is the really exciting part.

Because eventually Hermes isn't being asked:

> "What should we work on?"

Pāṭala can answer deterministically:

> "C192 is currently the highest-leverage unresolved claim because it blocks 17 arguments, 4 synthesis objects, 3 lessons, has only reconstructed evidence, and received two contradictory reviewer judgments."

Then Hermes does what Hermes is actually good at:

> finding a capable worker and getting the task completed.

**Pāṭala decides what matters. Hermes decides how work gets executed.**

That is the cleanest boundary I've found across all these architectures, and I would now make that the governing rule of the entire agentic system. ([GitHub][1])

If you paste or upload `BACKEND-MODEL.md`, the next useful step is to do a **line-by-line architecture review against these repos** and turn it into the definitive `10-live-system.md` plus the actual schemas/interfaces for `Task`, `Run`, `Event`, `Projection`, `Lease`, and the `patala_*` MCP verbs.

[1]: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/kanban.md?utm_source=chatgpt.com "hermes-agent/website/docs/user-guide/features/kanban.md at main · NousResearch/hermes-agent · GitHub"
[2]: https://github.com/nousresearch/hermes-agent/blob/main/website/docs/user-guide/features/kanban.md?utm_source=chatgpt.com "hermes-agent/website/docs/user-guide/features/kanban.md at main · NousResearch/hermes-agent · GitHub"
[3]: https://github.com/NousResearch/hermes-agent/issues/19101?utm_source=chatgpt.com "AGENTS.md is stale: missing curator, incomplete cron/delegate docs, wrong test numbers, missing plugins · Issue #19101 · NousResearch/hermes-agent · GitHub"
[4]: https://hermes-agent.nousresearch.com/docs/user-guide/profiles/?utm_source=chatgpt.com "Profiles: Running Multiple Agents | Hermes Agent"
[5]: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md?utm_source=chatgpt.com "hermes-agent/website/docs/user-guide/features/skills.md at main · NousResearch/hermes-agent · GitHub"
[6]: https://github.com/gastownhall/gastown?utm_source=chatgpt.com "GitHub - gastownhall/gastown: Gas Town - multi-agent workspace manager · GitHub"
[7]: https://github.com/gastownhall/gascity?utm_source=chatgpt.com "GitHub - gastownhall/gascity: Orchestration-builder SDK for multi-agent coding workflows · GitHub"
[8]: https://github.com/alamops/agetor?utm_source=chatgpt.com "GitHub - alamops/agetor: The harness orchestrator — a local-first kanban for running Claude Code, Codex, and other CLI coding agents in parallel, each in its own git worktree. · GitHub"
[9]: https://github.com/usemozzie/mozzie?utm_source=chatgpt.com "GitHub - usemozzie/mozzie: Local-first desktop app that orchestrates AI coding agents in parallel — work items, git worktrees, dependency tracking, and review workflow in one window. · GitHub"
[10]: https://github.com/codingagentsystem/cas?utm_source=chatgpt.com "GitHub - codingagentsystem/cas: Multi-agent orchestration for Claude Code. Persistent memory, tasks, rules, and skills that make AI agents actually coordinate. · GitHub"
[11]: https://github.com/fynnfluegge/agtx?utm_source=chatgpt.com "GitHub - fynnfluegge/agtx: 🏄🏼‍♂️ The blackboard for coding agents - multi-session tool for claude code, cursor, codex, gemini · GitHub"
[12]: https://github.com/gastownhall/beads/wiki?utm_source=chatgpt.com "Home · gastownhall/beads Wiki · GitHub"
[13]: https://github.com/gastownhall/beads/blob/main/AGENTS.md?utm_source=chatgpt.com "beads/AGENTS.md at main · gastownhall/beads · GitHub"
[14]: https://github.com/gastownhall/beads/issues/3135?utm_source=chatgpt.com "Clarify git vs dolt as source of truth for issue data · Issue #3135 · gastownhall/beads · GitHub"
[15]: https://github.com/Dicklesworthstone/beads_rust/blob/main/AGENTS.md?utm_source=chatgpt.com "beads_rust/AGENTS.md at main · Dicklesworthstone/beads_rust · GitHub"
[16]: https://github.com/Dicklesworthstone/beads_viewer/blob/main/AGENTS.md?utm_source=chatgpt.com "beads_viewer/AGENTS.md at main · Dicklesworthstone/beads_viewer · GitHub"
[17]: https://github.com/dicklesworthstone/mcp_agent_mail?utm_source=chatgpt.com "GitHub - Dicklesworthstone/mcp_agent_mail: Asynchronous coordination layer for AI coding agents: identities, inboxes, searchable threads, and advisory file leases over FastMCP + Git + SQLite · GitHub"
[18]: https://github.com/gastownhall/beads/blob/main/docs/COMMUNITY_TOOLS.md?utm_source=chatgpt.com "beads/docs/COMMUNITY_TOOLS.md at main · gastownhall/beads · GitHub"
[19]: https://github.com/mraza007/echovault?utm_source=chatgpt.com "GitHub - mraza007/echovault: Local-first memory for coding agents. Decisions, bugs, and context stored as Markdown, indexed locally with FTS5 plus optional semantic search. No RAM overhead at idle, no external servers. · GitHub"
[20]: https://github.com/repowise-dev/repowise?utm_source=chatgpt.com "GitHub - repowise-dev/repowise: Codebase intelligence for AI-assisted engineering teams: code health scores, auto-generated docs, git analytics, dead code detection, and architectural decisions via MCP. · GitHub"
[21]: https://github.com/wshobson/agents/blob/main/AGENTS.md?utm_source=chatgpt.com "agents/AGENTS.md at main · wshobson/agents · GitHub"
[22]: https://github.com/charannyk06/conductor-oss?utm_source=chatgpt.com "GitHub - charannyk06/conductor-oss: Local-first control surface for AI coding agents, workspaces, worktrees, terminals, diffs, previews, and paired-device access. · GitHub"
[23]: https://github.com/gannonh/kata?utm_source=chatgpt.com "GitHub - gannonh/kata: Kata multi-agent orchestration monorepo: CLI, Symphony, Desktop, Context, Orchestrator · GitHub"
[24]: https://github.com/dicklesworthstone?utm_source=chatgpt.com "Dicklesworthstone (Jeff Emanuel) · GitHub"
