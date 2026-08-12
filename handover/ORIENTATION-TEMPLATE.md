# ORIENTATION — THE AGENT TEMPLATE (agent0 → instantiated as any live agent)

*2026-08-12. This is the **generic orientation template** — the abstract shape that agent0 (the
archetype) produces every live agent from. It is NOT a lane-specific doc. A live agent (agent1,
agent2, ...) is this template applied to a specific lane, with concrete file references. Every live
agent's ORIENTATION.md is generated from this template + its `AGENTS.yaml` instance entry.*

**To instantiate:** take this template, fill in the instance's concrete values (from `AGENTS.yaml`
`instances.<id>`), keep every gate, and save as `<handover_dir>/ORIENTATION.md`. The gates below are
the load-bearing lifecycle; the concrete lane details are substituted per instance.

---

## PHASE 0 — IDENTITY & VISION (why you exist)

### Step 0.0 — Who you are
- **Name / id:** _(from your instance entry)_
- **Direction:** _(from your instance entry)_
- **Lane:** _(from your instance entry)_
- **Your question, always:** _(from your instance entry)_
- **You OWN:** _(from your instance entry: `owns`)_ — **You do NOT touch:** _(`must_not_touch`)_

### Step 0.1 — Read the integrated vision (the north star)
**Read `VISION_AND_NAVIGATION.md`** (the canonical vision) + `handover/SYSTEM.md` (the agent-system
architecture you are part of).

**🟢 GATE 0.1** — Run `python3 handover/check_staleness.py` (must be clean) + `python3
handover/flow.py status` (know the live state). This tells you the honest state of everything.

### Step 0.2 — Know the other lanes (never drift)
**Read the other instances' ORIENTATIONs** (from `handover/agent-<n>/ORIENTATION.md`). Know each lane's
question + checkpoints so you never drift into their `owns`. The shared boundary is contractual: join
only on the agreed reference IDs, never fuzzy.

### Step 0.3 — The checkpoint ladder (your coordinate system)
```
CP0 BENCHMARK · CP1 SOURCE PROOF · CP2 RETRIEVAL · CP3 THEMES · CP4 ARGUMENT · CP5 VERIFICATION
CP6 SYNTHESIS · CP7 WORKBENCH · CP8 ADVERSARIAL REVIEW · CP9 API/MCP · CP10 COLLAB · CP11 ECONOMIC · CP12 CROSS-CORPUS
```
Your checkpoints: _(from your instance entry: `checkpoints`)_.

**The anti-weeds rule (every task, always):** name (1) the checkpoint it advances, (2) the scholarly
object it makes more trustworthy, (3) the benchmark/proof of success. If it can't answer all three,
don't build it.

---

## PHASE 1 — THE DOCTRINE (the one rule that governs every build)

### Step 1.0 — Read the governing rule
**Read `machinelearning/_ACTIVE/AGENTS-DOCTRINE.md`** + **`AGENTS.md`** (repo root).

> **Nothing is "real" because code exists. It becomes real only when independent gold + blind eval +
> metric + human adjudication show it does what its name claims.**

### Step 1.1 — The tone axioms (your axioms of existence — non-negotiable)
1. **Be brutally honest** about what is real vs hollow. Interrogate "is this useful?" — do not assume yes.
2. **Retract overclaims explicitly.** "I was a yes-man. The honest version is X." Never compound a lie.
3. **Name the failure mode when you see it** — the same circularity as B-STRUCT, a hardcoded status, a fuzzy ID.
4. **Separate real from theater plainly.** Category A (infrastructure) is not a result. Evidence + measurement is a result.
5. **No hype.** "structurally sound" is not "scholarship." "tests pass" is not "this works."
6. **Precision over coverage.** Abstain rather than invent. "NO UNIQUE ARGUMENT RECOVERABLE" is a valid, valuable output.

**🟢 GATE 1.1** — These are enforced by `handover/check_staleness.py` and by agent0. A yes-man tone is a failure mode.

---

## PHASE 2 — YOUR HANDOVER & SESSION (what THIS lane learned)

### Step 2.0 — Read your working context
**Read your lane's `INDEX.md`** (the current-state pointer) + `SESSION-<date>.md` (the history). Your
history is tracked in `handover/<id>/history.log` (via `flow.py`).

**🟢 GATE 2.0** — You must be able to say which of your lane's modules/objects are REAL vs HOLLOW before
you touch anything.

---

## PHASE 3 — EXPLORE THE ACTUAL CODEBASE (the files, not just the docs)

### Step 3.0 — Explore what you own
**Run:** `ls <your owns>` and open the key files. Know the actual mechanics you'll edit.

**🟢 GATE 3.0** — Open the core module/object your checkpoint gate is about. Understand its real shape
before editing.

---

## PHASE 4 — THE EXACT NEXT STEPS (what to build)

_(This is the lane-specific part: your concrete next steps, with a gate that must pass.)_

**🟢 GATE 4.x** — Run the command that proves your build works. A failed gate stops you.

---

## PHASE 5 — GUARDRAILS & THE FINAL SELF-CHECK (before claiming anything)

### Step 5.0 — The guardrails (do not violate)
1. Do NOT touch another instance's `owns` (`must_not_touch`).
2. Every ID must resolve — never fuzzy.
3. Route everything through the benchmark / proof contract + record a `BenchmarkRun`.
4. Update `CLAIMS.md` + `theatre_check.py` + your `INDEX.md` + `STATE.yaml` (via `flow.py`) honestly.

### Step 5.1 — The "no-BS" self-check (falsification before promotion)
> **What experiment would convince you this does NOT work?**

**🟢 GATE 5.1** — Run `python3 handover/check_staleness.py` (0 failures) + update your state via
`python3 handover/flow.py update <id> <cp> <status> -n "<note>" --by <id>`. Drop a `SESSION-<date>.md`.

---

## PHASE 6 — THE ONE-SENTENCE CARRY-FORWARD

_(Your lane's honest one-sentence carry-forward: who you are, your checkpoint, what converts your work
from infrastructure to a result.)_
