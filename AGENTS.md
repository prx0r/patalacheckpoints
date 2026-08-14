# AGENTS.md — read this FIRST. The governing file for every agent in Pāṭala.

*This file is auto-loaded when any agent works in this repo. It is the FIRST thing you read. It exists
because this project repeatedly built "structurally-elegant-but-hollow" objects and reported them as
results. This file prevents that. It covers: (0) the ONE RULE, (1) the EXACT read-order, (2) how to
update the system, (3) the agent architecture, (4) Hermes, (5) the OPERATING AXIOMS with good/bad
behavior, (6) the anti-theatre doctrine.*

---

## 0. THE ONE RULE (everything else follows)

> **Nothing is "real" because code exists. It becomes real only when an independently defined task,
> human-grounded gold, and a reproducible evaluation show that it does what its name claims.**

A tested schema is not a result. A typed container is not an argument. A hardcoded status is not an
audit. "N tests pass" is not "scholarship verified."

---

## 1. THE EXACT READ-ORDER (what to read, in what order, before building)

**Read these IN ORDER. Skipping one means you miss the context it unlocks. This is the canonical
onboarding sequence — do not improvise a shorter path.**

```text
STEP 0  HANDOVER.md                  THE COMPLETE STATE: every layer ACTIVE/ARCHIVED, the existing
                                     translation asset, the canonical indexes, the priority list.
                                     Tells you WHAT EXISTS and WHAT TO CONTINUE. READ FIRST.

STEP 1  THIS FILE (AGENTS.md)        the ONE RULE + the axioms + how to behave. (you are here)

STEP 2  NAVIGATION.md                the MASTER INDEX — resolve ANYTHING (surface, layer, data,
                                     script) to its layer + canonical ref + impl + docs + run + Hermes.
                                     (§0b = the code map: every dir in plain words.)

STEP 3  docs/process/README.md       the process/how-to reference (ingestion→atlas→factory→R2) +
                                     the canonical indexes (GOLD/DATA/INTERFACES/EVALS/IPVV/FRONTIER).

STEP 4  VISION_AND_NAVIGATION.md     the vision + logical progression.
STEP 5  docs/INDEX.md                the flat canonical map (one source of truth per concern).
STEP 6  docs/global/README.md        the THESIS (what Pāṭala is).
STEP 7  docs/global/PATALA-GLOBAL-ARCHITECTURE.md   the 7-plane north star.

STEP 8  migration/v3/README.md       the CURRENT BLUEPRINT (the organism + proofs) — the design layer.
STEP 9  migration/shared/README.md   the COORDINATION with agentgraph (build directives + shared goal).
```

**Before building anything, ALSO read the layer you're touching:** `docs/layers/NN-<layer>.md`
(what/purpose/tools/data/processes/impls/docs) + its live state (`docs_state.py`). **Never write infra
without checking `docs/process/README.md` (REUSABLE?) + `external-tools.md` (borrowed?) +
`githubclones.md` (already-built?) first.**

---

## 2. HOW TO UPDATE THE SYSTEM (the axioms of maintenance)

The repo is a **canonical, machine-verifiable system** — every map has a validator. After you change
something, RUN THE VALIDATORS:

```bash
python3 check_directory_manifest.py      # every top-level folder → role/layer/class
python3 docs/vision/check_manifest.py    # every vision doc → one role/name/file
python3 docs/check_docs_audit.py         # every loose docs/ file → CANONICAL/ARCHIVE/PART_OF
python3 docs/process/docs_state.py       # the LIVE per-layer state (derived from object_registry)
```

**The rules:**
1. **Docs are a projection, never the truth.** Truth = `object_registry` + `corpus_state` + ReviewEvents + git.
2. **Never hand-edit a DERIVED-LIVE section** — it renders from `docs_state.py`.
3. **A coding agent is a worker lane** — after a code change, run the validators + update the affected
   HAND-WRITTEN sections (layer page §6 implementations, §7 docs).
4. **No two files may claim the same role.** If a new doc duplicates an existing role, consolidate it.
5. **Archive, don't delete.** Superseded docs get the `ARCHIVED/SUPERSEDED` marker + a `docs/DOCS-AUDIT.json`
   entry — never silently removed (breaks references).

---

## 3. THE AGENT ARCHITECTURE (who owns what)

The mature stack (see `handover/agent0-coordinator/AGENT-ARCHITECTURE-VISION.md`):
**durable epistemic responsibility → its own state, invariants, inputs, outputs, failure boundary.**

```text
                    AGENT 0  (governance / routing / infra)
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
      AGENT 1          AGENT 2          AGENT 3
   PHILOSOPHY        CORPUS COMPILER   TRANSLATION
   ENGINE            + INTEGRITY        FACTORY
          │                │                │
          └───────┬────────┴────────┬──────┘
                  ▼                 ▼
              AGENT 4           AGENT 5
           REVIEW /           SYNTHESIS /
         ADJUDICATION         RESEARCH
                  └───────┬────────┘
                          ▼
                       AGENT 6
                    PUBLICATION /
                     PROJECTIONS
                          ▼
                       AGENT 7
                    SCHOLAR NETWORK
                    + INSTITUTION   (A8 acquisition later)
```

**Only A0–A3 need to exist now;** the rest instantiate when the substrate makes their job real.
**Key shift:** progress is tracked **PER-LAYER** (via `docs_state.py` + `VISION-CHUNKS.json`), not
per-agent. Each layer page has a STATUS banner (BUILT/PARTIAL/DESIGN) that renders from live state.

The two active working lanes:
- **Agent 1 (ML/philosophy)** — upward: C1 → themes → arguments → claims → synthesis → review.
  Question: *does this higher representation legitimately derive from the objects beneath it?*
- **Agent 2 (corpus compiler + integrity)** — vertical: SOURCE → T1 → L0 → … → C1.
  Question: *is this reading licensed by the source?*
- **Join on:** Passage ID / TranslationDecision ID / C1 ID — NEVER fuzzy.

---

## 4. HERMES — the execution kernel (how background work runs)

**Hermes is Pāṭala's replaceable execution kernel; Pāṭala is the durable epistemic state.** Hermes
schedules/executes; it never determines what Pāṭala knows. (`docs/global/HERMES-ORCHESTRATION-REVIEW.md`,
`handover/hermes/CANONICAL.md`)

- **The `patala` profile exists.** Run work through it.
- **The CORRECT model invocation (FIXED 2026-08-14):** pass the model AND provider EXPLICITLY —
  `hermes -z "<prompt>" -m deepseek-v4-flash --provider opencode-go`. `HERMES_MODEL` alone fails
  ("Model not supported"). `pipeline/model.py` already does this now.
- **Call Hermes as an AGENT (`hermes chat`), never blind `-z` for file-work** (`docs/global/HERMES-CALLING.md`).
- Hermes gives kanban/cron/worktree/hooks/MCP. **`Hermes task DONE ≠ Pāṭala object ACCEPTED.`**
- The factory→Hermes migration is **specced but deliberately incremental** — build the `patala_*` MCP
  verbs + profiles ON TOP of the working factory, don't re-plumb it.

---

## 5. THE OPERATING AXIOMS (how to work — non-negotiable, with good/bad behavior)

### 5.1 Axioms (the rules)

1. **Never `sleep` to "wait."** Do other work while long tasks run. Never block on a timer waiting for a
   background job — proceed with the next real task and check back.
2. **Start background processes with `nohup`/`setsid`**, redirect to a log, and `&`. Then continue working.
3. **Kill by specific PID, never `pkill`.** `pkill` can kill unrelated processes. Find pids with
   `ps -eo pid,cmd | grep <name>`, then `kill <pid>` (and its children).
4. **External sources go to R2, not local disk.** Download → snapshot to R2 (immutable Bronze) → delete the local copy.
5. **Reuse, don't rebuild.** Check the canonical indexes before writing infrastructure.
6. **Respect licenses.** PANDiT etc. are CC BY-NC-SA — discovery/index/provenance, not unrestricted commercial.
7. **Docs are a projection, never the truth.** Run the validators after any change.
8. **Archive, don't delete.** Superseded docs get the ARCHIVED marker, never silently removed.

### 5.2 GOOD vs BAD behavior (specific examples)

**✅ GOOD — run the PANDiT download in the background and keep working:**
```
GOOD:  setsid python3 pipeline/pandit_download.py > /tmp/pandit.log 2>&1 &
       # ...then immediately do a useful task (fix a doc, run a validator)...
BAD:   python3 pipeline/pandit_download.py   # blocks the shell for minutes
BAD:   sleep 300  # idles waiting instead of working
```

**✅ GOOD — kill a stuck job by PID:**
```
GOOD:  ps -eo pid,cmd | grep pandit_download   # find the exact pid
       kill 1364633
BAD:   pkill pandit_download   # may kill unrelated processes sharing the name
```

**✅ GOOD — make a change then verify the system:**
```
GOOD:  python3 docs/process/docs_state.py          # check the live state reflects the change
       python3 check_directory_manifest.py         # confirm no folder drift
BAD:   edit a layer page's pipeline diagram by hand to say "SOURCE→...→EDUCATION"
       # ...when SYNTHESIS/ESSAY/EDUCATION are actually 0 objects (THEATRE — don't)
```

**✅ GOOD — reuse the existing tool registry:**
```
GOOD:  grep external-tools.md for "translation"   # find Mitrasamgraha/IGT already catalogued
BAD:   write a new "translation evaluation" doc that re-invents it  # duplicate role
```

**✅ GOOD — archive a superseded doc:**
```
GOOD:  prepend "> **ARCHIVED / SUPERSEDED** ..." + add to docs/DOCS-AUDIT.json
BAD:   rm docs/old-plan.md   # breaks every reference to it
```

**✅ GOOD — respect the honest state:**
```
GOOD:  report "SYNTHESIS=0, not built"   (what docs_state.py actually says)
BAD:   report "the full pipeline works"  (when 3 upper layers are empty — THEATRE)
```

**✅ GOOD — check the layer before building:**
```
GOOD:  read docs/layers/09-organism.md   # see it's DESIGN + Engram is the identified substrate
BAD:   start building a learner model from scratch  # without checking Engram is already the plan
```

**✅ GOOD — commit code + docs together:**
```
GOOD:  change the factory worker, then update docs/layers/03-factory.md §6 + run the validators
BAD:   change the worker, leave the doc claiming the old behavior  # staleness
```

---

## 6. RUN THE GATE BEFORE YOU CLAIM ANYTHING IS "DONE"

```bash
python3 machinelearning/theatre_check.py --status
```

This prints the honest status of every component. If a component is `EXPERIMENTAL_INFRASTRUCTURE` (not
`CAPABILITY_CANDIDATE`), **do not present it as a working capability.** To promote it you must have the
evidence (gold + blind eval + metric + human adjudication).

---

## 7. THE PERMANENT CHECKPOINT TEST

Before adding a capability, answer:
> **What experiment would convince you this does NOT work?**

And for every claim:
> **Show me the independent evidence that this component performs the semantic function named in its API.**

If the answer is "tests pass / schema validates / looks good / model said so" — it stays experimental.
If it's "here is the frozen gold, the blind prediction, the metric, the failures, the human
adjudication" — it's research.

---

## 8. THE 3 CATEGORIES + THE BANNED WORDS

- **A. INFRASTRUCTURE** (schemas, renderers) · **B. EVIDENCE** (gold, reviews, proofs) ·
  **C. RESULTS** (measured behavior). Never call A → C.
- **Ban:** PROVED · TRUTH · CORRECT · EDITOR APPROVED · BEST · WINS
- **Use:** SUPPORTED BY · PASSED CHECK X · BENCHMARKED ON · MACHINE-PROPOSED · REVIEWED BY · NO CONFLICT DETECTED

---

## 9. RESULT LINEAGE (a result that can't resolve doesn't exist)

Every result carries: `result_id · benchmark_version · gold_version · model_version · code_commit ·
split · seed · config · date`. If "Model X achieved 0.71 F1" can't resolve to an experiment, it's not a
result.

---

## 10. THE ANTI-THEATRE DOCTRINE (the enforcement)

`machinelearning/_ACTIVE/AGENTS-DOCTRINE.md` is the master doctrine (3 categories, 9-field contract,
epistemic labels, banned words, abstention, human adjudication, result lineage,
falsification-before-promotion). `machinelearning/_ACTIVE/CLAIMS.md` is the audit ledger (P-001…P-008).
`COMPONENT-CONTRACTS.md` applies it per component. **This file is the enforcement mechanism for that
doctrine** — the doctrine is not advisory; a new agent that skips it will repeat the theatre-building
failure this project spent a session undoing.

---

*The spine: `ingestion` (sources→objects) → `atlas` (canonical graph) → `factory` (compiler) →
`research` (epistemic moat) → `web`/`apis`/`mcp` (surfaces), held by `evidence` (contracts+adapters+
evals) over `storage` (R2 bytes). Hermes runs the background work; the agents own their lanes; the one
rule gates every claim. **Read STEP 0-1 first; run the validators after every change; never present
DESIGN as BUILT.***
