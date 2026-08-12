# THE AGENT SYSTEM — a self-maintaining onboarding & coordination architecture

*2026-08-12. The meta-layer above the agents. This is NOT one agent's onboarding — it is the
**agent-agnostic system** that onboards ANY agent (Agent 0 coordinator, Agent 1 ML, Agent 2 L0,
future agents) consistently, keeps the vision doc live, derives each agent's flow from a single
source of truth, and **detects stale docs automatically**. If you are an agent reading this: it tells
you where your orientation comes from and how to keep the system honest.*

---

## 0. WHY THIS EXISTS (the failure it fixes)

The project kept drifting because each agent's onboarding was hand-written, duplicated the vision, and
rotted: the vision doc, the handover, the session notes, and the checkpoints could disagree, and nothing
detected it. This system makes the onboarding **derived, not hand-copied**, so:
1. The **vision lives once** (the canonical vision doc is the single source of truth).
2. Each agent's **orientation is derived** from the vision + a machine-readable registry — not a stale copy.
3. A **staleness checker** runs and fails when any doc drifts from the registry/vision/index.

---

## 1. THE SINGLE SOURCE OF TRUTH (the vision doc)

**`VISION_AND_NAVIGATION.md`** (repo root) is the canonical vision. It is the only place the global
"what and why" lives. It states: the computable scholarly tradition, the logical progression, and the
navigation map.

**Everything an agent needs to know is DERIVED from this + `handover/CHECKPOINTS.md`** (the shared
execution map: CP0–CP4, the contracts, the gate definitions).

> Rule: **never copy the vision into an agent doc.** An agent doc *links* to the vision and *derives*
> its lane. If an agent doc contains a stale copy of the vision, the checker flags it.

---

## 2. THE AGENT REGISTRY — ONE TEMPLATE (agent0), N LIVE INSTANCES

**`handover/AGENTS.yaml`** — the single source of truth. The model is:

> **agent0 is the AGNOSTIC TEMPLATE / archetype — the abstract structure every live agent is an
> instantiation of.** agent1, agent2, ... are `instance_of: agent0`: live agents with concrete file
> references (`owns`, `orientation`, `history`) and tracked progress (`STATE.yaml` + a per-instance
> `history.log`). Add a new agent = instantiate the template (a new `instances` entry + an orientation
> generated from `ORIENTATION-TEMPLATE.md` + a handover dir + a history log). Nothing else changes.

```yaml
version: "2.0"
template:                    # agent0 — the archetype (NOT a live lane)
  id: agent0
  name: "The Agent Archetype (agnostic template)"
  schema: [ id, name, direction, lane, question, checkpoints, owns, orientation, handover_dir, must_not_touch ]
  lifecycle_phases: [ PHASE 0..6 ]       # the process-workflow orientation template
  orientation_template: "handover/ORIENTATION-TEMPLATE.md"
  live_flow: { status, update, history, add_instance }   # flow.py
doctrine:                    # adopted by EVERY live instance
  one_rule: "..."
  tone_axioms: [ ...6... ]
instances:                   # agent1, agent2 = 'agent0' applied to a lane
  agent1: { instance_of: agent0, lane: "C1→themes→arguments→claims→synthesis→review",
            checkpoints: [CP0,CP2,CP3,CP4], owns: [...], history: "handover/agent-1-ml/history.log" }
  agent2: { instance_of: agent0, lane: "SOURCE→segmentation→morphology→syntax→alignment→proof",
            checkpoints: [CP1], owns: [...], history: "handover/agent-2-integration/history.log" }
```

**The template vs. the instances:**
- **agent0 (template)** — the shape every agent fills: the schema, the doctrine + tone axioms, the
  lifecycle (the ORIENTATION-TEMPLATE's 6 phases), and the live flow. It owns `SYSTEM.md`, `AGENTS.yaml`,
  `STATE.yaml`, `flow.py`, `check_staleness.py`. It has **no lane progress of its own** — it is what the
  lanes are made of.
- **agent1 / agent2 (instances)** — the template applied to a concrete lane, with real `owns` /
  `must_not_touch` / `orientation` / `history`, and tracked checkpoint progress in `STATE.yaml`.

**The coordinator function is NOT a competing "agent0 lane."** It is the template's own governance
function — any instance acting as coordinator runs the staleness checker + flow, enforces the registry
and the tone axioms, and gates checkpoints. (See `handover/ORIENTATION-AGENT0.md`.)
    name: "Agent 2 — L0 / integration"
    direction: "vertical truth"
    lane: "SOURCE → segmentation → morphology → syntax → alignment → translation proof"
    question: "Is this reading licensed by the source?"
    checkpoints: [ CP1 ]
    owns: [ "data/corpus/", "app/", "lib/", "pipeline/verify_l0.py", "philproof.py", "handover/agent-2-integration/" ]
    orientation: "handover/agent-2-integration/ORIENTATION.md"
    handover_dir: "handover/agent-2-integration/"
    must_not_touch: [ "benchmarks/v0/", "machinelearning/research/patala_ml/" ]
```

**The registry is the contract.** The orientation of every agent is derived from its registry entry.
The checker validates that each agent's actual files match its registry entry.

---

## 3. THE PER-AGENT FLOW (the template every ORIENTATION follows)

Every agent's `ORIENTATION.md` is a **process workflow** with mandatory gates — NOT a passive document.
The template (already implemented for Agent 1):

```
PHASE 0 — IDENTITY & VISION   (who you are, the integrated vision, the two-lane awareness, your checkpoints)
PHASE 1 — THE DOCTRINE        (the one rule, CLAIMS.md ledger)
PHASE 2 — AGENT-SPECIFIC      (your handover + session notes — validated reads)
PHASE 3 — EXPLORE THE CODEBASE (open the actual files you own — validated)
PHASE 4 — THE EXACT NEXT STEPS (your build, with a gate that must pass)
PHASE 5 — GUARDRAILS & SELF-CHECK (the falsification test before claiming)
PHASE 6 — CARRY-FORWARD
```

**Every gate is a command the agent must run** (`theatre_check.py`, `emit_gold_fixtures.py`, a `wc -l`,
a test suite). A failed gate STOPS the agent. This is how the system ensures steps are actually done,
not just listed.

---

## 4. THE STALENESS CHECKER (how the system stays honest)

**`handover/check_staleness.py`** — run this to detect when docs have drifted. It checks, across the
whole system:

| Check | Detects |
|---|---|
| **Registry ↔ files** | every `orientation`/`handover_dir`/`owns` path in `AGENTS.yaml` exists |
| **Registry ↔ vision** | `VISION_AND_NAVIGATION.md` + `handover/CHECKPOINTS.md` exist and are referenced |
| **Orientation ← registry** | each agent's ORIENTATION mentions its own `question` + `checkpoints` (from the registry) — catches a stale orientation that drifted from its own definition |
| **Vision-not-copied** | no agent doc contains a verbatim block from the vision (they must link, not copy) |
| **INDEX freshness** | each lane's `INDEX.md` exists (the "current state" pointer) |
| **Passage resolution** | every `pt:passage:ipvv:chunk...` id in `benchmarks/v0/structure/` resolves against `data/published/ipvv/index.json` |
| **GOLD consistency** | every PAT-STRUCT fixture passes the gold-consistency validator |
| **Test health** | the test suite still runs green |

**A FAILING CHECK MEANS THE SYSTEM IS STALE — FIX THE DOC, NOT THE CHECKER.**

**🟢 GATE 4.0 (run on every session start AND end):**
`python3 handover/check_staleness.py` — must report 0 failures before work begins and after it ends.

---

## 5. HOW AGENTS KEEP THE VISION LIVE (the workflow)

**The versioned live flow (the orchestration layer):**
```
VISION (VISION_AND_NAVIGATION.md)             the canonical north star
   ↓
CHECKPOINTS (handover/CHECKPOINTS.md)         the shared execution map (CP0–CP12)
   ↓
STATE (handover/STATE.yaml)                   the LIVE per-agent + shared checkpoint statuses
   ↓
flow.py (handover/flow.py)                    the single interface agents use to update state
   ↓
history.log                                   the immutable versioned change log (who/what/when)
```
**`flow.py` is the ONLY way to change live state.** Every `flow update` bumps `state_version` and appends
an attributed, timestamped entry to `history.log`. New agents slot in via `flow add-agent` (scaffolds a
state block) + an `AGENTS.yaml` entry + a generated orientation.

1. **Session start:** run `python3 handover/check_staleness.py` (must be clean). Run
   `python3 handover/flow.py status` (know the live state). Read your ORIENTATION → the vision →
   CHECKPOINTS.
2. **Work:** update your lane's `INDEX.md` as you go. Append to your `SESSION-<date>.md`, never overwrite.
3. **Progress:** when a checkpoint changes status, run
   `python3 handover/flow.py update <agent> <cp> <status> -n "<note>" --by <agent>` — this versions the
   change. Keep `CHECKPOINTS.md` + your `INDEX.md` consistent with it.
4. **Cross-lane:** one `LOG.md` entry per handoff (what · why · file · date · direction · schema snippet).
5. **When the vision/checkpoints change:** update `VISION_AND_NAVIGATION.md` + `CHECKPOINTS.md` ONCE,
   then re-derive/verify each agent's orientation against the registry.
6. **Session end:** update `CLAIMS.md` + `theatre_check.py` honestly, run `check_staleness.py` again
   (must pass), drop a `SESSION-<date>.md`, archive superseded snapshots.

---

## 6. THE GIT LAYER — PER-AGENT BRANCHES, ONE SHARED TRUNK

Each live agent commits its **own deliverables to its own branch**; the shared trunk carries what is
canonical and the coordination state. This prevents the failure this project hit: two agents working in
one working tree, so one lane's uncommitted work is invisible and unpushed.

```
main     shared trunk   — the vision, the doctrine, canonical checkpoint-crossing objects,
                          and the shared coordination state (handover/LOG.md, STATE.yaml,
                          flow.py, check_staleness.py, AGENTS.yaml, SYSTEM.md)
agent1   working branch — Agent 1's deliverables (benchmarks/v0/, machinelearning/research/patala_ml/)
agent2   working branch — Agent 2's deliverables (pipeline/, data/, lib/, docs/)
```

**Rules (agnostic, apply to every agent):**
1. **Commit your own lane's files to your own branch** (`agent1` / `agent2` / ...). Never sweep
   another agent's uncommitted work or the pre-existing build into a commit you claim.
2. **The shared coordination state lives on `main`** — `handover/LOG.md`, `handover/STATE.yaml`,
   `flow.py`, `check_staleness.py`, `AGENTS.yaml`, `SYSTEM.md`. Both agents write it, so a coordinator
   (agent0) merges it onto `main` to avoid conflicts; do not fight over it on your branch.
3. **Merge to `main` when a checkpoint crosses its gate** (or a canonical object is frozen) — not on
   every commit. A checkpoint crossing is a `flow.py update <agent> <cp> <status>` + the agent's
   branch merged to `main`.
4. **Push your branch** at session end so your work is durable and attributable (`git push -u origin
   <your-branch>`).
5. **Never force-push, never rewrite shared history.** Append-only on `main`.

**The per-agent convention is recorded in `AGENTS.yaml` (`git.branch` per instance) and enforced by
Agent 0 (see `ORIENTATION-AGENT0.md` § git).**

---

## 7. THE AGENT-0 ROLE — THE ARCHETYPE + ITS GOVERNANCE FUNCTION

Agent 0 is **not a lane and not a competing coordinator.** It is the **agnostic template** every live
agent (`instance_of: agent0`) instantiates — the schema, the doctrine + tone axioms, the lifecycle, and
the live flow (see §2). The **governance function** (running the staleness checker, enforcing the
registry + tone axioms, gating each checkpoint's proof) is part of the template and can be performed by
any instance acting as coordinator — see `handover/ORIENTATION-AGENT0.md`. Its orientation
(`ORIENTATION-TEMPLATE.md`) is the generic shape; each live instance's `ORIENTATION.md` is that template
applied to its lane.

---

## 8. THE AGNOSTIC PRINCIPLE (why this works for ANY agent)

The system does not assume an agent is "ML" or "L0." It assumes only that:
1. There is a **registry entry** describing the agent (lane, checkpoints, owns, question).
2. There is an **orientation** derived from that entry (the process-workflow template).
3. The agent reads the **single vision** and its own **CHECKPOINTS**.
4. The **staleness checker** validates registry ↔ docs ↔ index ↔ gold ↔ tests.

Add a new agent = add a registry entry + generate its orientation from the template + a handover dir.
Nothing else changes. That is the agnostic design.

---

## 9. THE ONE-SENTENCE CARRY-FORWARD

**Pāṭala is one evidence graph, and its agent system is one self-maintaining onboarding: a single
canonical vision doc + a machine-readable agent registry + per-agent orientations derived from it (with
validation gates) + a staleness checker that fails on any drift. The checker is the enforcement
mechanism — the same honest-measurement discipline the doctrine applies to scholarship, applied to the
agent system itself. Run it at every session start and end.**
