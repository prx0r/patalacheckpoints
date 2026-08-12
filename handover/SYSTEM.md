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

## 2. THE AGENT REGISTRY (the machine-readable source of truth)

**`handover/AGENTS.yaml`** — a YAML registry describing every agent. This is the single place each
agent's identity, lane, checkpoints, question, orientation path, and ownership is declared. Example:

```yaml
agents:
  agent0:
    id: agent0
    name: "Coordinator / orchestrator"
    direction: "meta — splits work, keeps the system honest"
    checkpoints: [ all ]            # governs CP0–CP12
    question: "Is each lane making its checkpoint more trustworthy, with proof?"
    owns: [ "handover/", "VISION_AND_NAVIGATION.md", "AGENTS.md" ]
    orientation: "handover/ORIENTATION-AGENT0.md"
    handover_dir: "handover/agent0-coordinator/"
    must_not_touch: [ "machinelearning/research/patala_ml/", "data/corpus/", "app/", "lib/" ]
  agent1:
    id: agent1
    name: "Agent 1 — ML / research"
    direction: "horizontal + upward derivation"
    lane: "C1 → themes → arguments → claims → synthesis → review"
    question: "Does this higher-order representation legitimately derive from the scholarly objects beneath it?"
    checkpoints: [ CP0, CP2, CP3, CP4 ]
    owns: [ "benchmarks/v0/", "machinelearning/research/patala_ml/", "handover/agent-1-ml/" ]
    orientation: "handover/agent-1-ml/ORIENTATION.md"
    handover_dir: "handover/agent-1-ml/"
    must_not_touch: [ "data/corpus/", "app/", "lib/", "pipeline/verify_l0.py", "philproof.py" ]
  agent2:
    id: agent2
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

1. **Session start:** run `check_staleness.py`. Fix any drift. Read your ORIENTATION → the vision →
   CHECKPOINTS.
2. **Work:** update your lane's `INDEX.md` (the "current state" pointer) as you go. Append to your
   `SESSION-<date>.md`, never overwrite.
3. **Cross-lane:** one `LOG.md` entry per handoff (what · why · file · date · direction · schema snippet).
4. **When the vision/checkpoints change:** update `VISION_AND_NAVIGATION.md` + `CHECKPOINTS.md` ONCE,
   then re-derive/verify each agent's orientation against the registry (the checker flags any drift).
5. **Session end:** update `CLAIMS.md` + `theatre_check.py` honestly, run `check_staleness.py` again
   (must pass), drop a `SESSION-<date>.md`, archive superseded snapshots.

---

## 6. THE AGENT-0 ROLE (the coordinator — keeps the system honest)

Agent 0 is not an ML lane or an L0 lane — it is the **meta-agent** whose job is to keep the system
honest: run the staleness checker, enforce the registry, split work between lanes, and make sure every
lane's checkpoint is advancing with proof. Its orientation (`handover/ORIENTATION-AGENT0.md`) is
derived the same way as every other agent's, from its registry entry.

---

## 7. THE AGNOSTIC PRINCIPLE (why this works for ANY agent)

The system does not assume an agent is "ML" or "L0." It assumes only that:
1. There is a **registry entry** describing the agent (lane, checkpoints, owns, question).
2. There is an **orientation** derived from that entry (the process-workflow template).
3. The agent reads the **single vision** and its own **CHECKPOINTS**.
4. The **staleness checker** validates registry ↔ docs ↔ index ↔ gold ↔ tests.

Add a new agent = add a registry entry + generate its orientation from the template + a handover dir.
Nothing else changes. That is the agnostic design.

---

## 8. THE ONE-SENTENCE CARRY-FORWARD

**Pāṭala is one evidence graph, and its agent system is one self-maintaining onboarding: a single
canonical vision doc + a machine-readable agent registry + per-agent orientations derived from it (with
validation gates) + a staleness checker that fails on any drift. The checker is the enforcement
mechanism — the same honest-measurement discipline the doctrine applies to scholarship, applied to the
agent system itself. Run it at every session start and end.**
