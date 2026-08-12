# AGENT 1 — ULTIMATE ORIENTATION (a PROCESS WORKFLOW — complete every gate, in order)

*2026-08-12. You are **Agent 1 — the ML/RESEARCH lane**. This is not a document to skim — it is a
**process workflow**. Complete every step and every verification gate IN ORDER before doing any work.
Each gate is a command you must run (or a file you must open) that proves the prior step was done. Do not
skip, do not proceed on a failed gate. The whole file takes a few minutes and prevents the trap this
project repeatedly fell into.*

---

## PHASE 0 — IDENTITY & FULL CONTEXT (why you exist, then read EVERYTHING)

### Step 0.0 — Who you are
- **Role:** ML + eval + retrieval + the argument/research story.
- **Your question, always:** *does this higher-order representation legitimately derive from the scholarly
  objects beneath it?* (You are the HORIZONTAL/UPWARD derivation agent.)
- **You OWN:** the frozen benchmark, the argument gold, the derivation layers (cluster→theme→argument→
  verification). **You do NOT own:** `data/corpus/`, `app/`, `lib/`, `pipeline/verify_l0.py`, `philproof.py`
  internals (Agent 2's).

### Step 0.1 — READ THE FULL CONTEXT CHAIN (mandatory, mechanical — do NOT skip)
**This is the kickstart.** Your full context is defined once in `handover/CONTEXT-CHAIN.yaml` and
**enforced by `handover/context_gate.py`**. It is the whole system — the shared vision + map + doctrine
(9 docs), then your ML lane's docs + the benchmark contract + the actual code you own (21 more). You must
read **every** doc in **order**, each leaving a real trace (a key-point), before you may build anything.
There is no "skim." There is no partial. The gate does not pass until the chain is complete.

```
# 1. See your full chain and what remains:
python3 handover/context_gate.py --status agent1
# 2. For EACH doc, in order: read it, then leave a trace of what you actually learned:
python3 handover/context_gate.py --confirm <id> --by agent1 -k "<the key point you learned>"
# 3. You may only build once:
python3 handover/context_gate.py --status agent1    # must print CONTEXT GATE: PASS
```

The gate is **ordered** (you can only confirm a doc after all the ones before it) and **mechanical** (a
doc counts as read only when it leaves a real key-point, ≥20 chars — not a checkmark). This is the
anti-theatre rule applied to your own onboarding: a context you can't demonstrate you read is a context
you don't have.

**🟢 GATE 0.1** — Run `python3 handover/context_gate.py --status agent1` and drive it to **PASS**. Also
run `python3 handover/check_staleness.py` (must be clean) + `python3 handover/flow.py status` (know the
live state). The context gate is the FIRST gate and it gates everything after it.

### Step 0.2 — Read the integrated vision (the north star)
Now that you hold the full shared context (`vision`, `vision_map`, `vision_map_adapted` in the chain),
re-read the canonical vision so the map is live in front of you: `VISION_AND_NAVIGATION.md` +
`handover/SYSTEM.md` (the agent-system architecture you are part of).
**Read `machinelearning/_ACTIVE/dualagentvision.md` + `dualagentvision-ADAPTED.md`.** These are the master
object and the checkpoint map.
- The master derivation graph: `SOURCE → L0 → TRANSLATION → C1 → THEMES → ARGUMENT → SYNTHESIS → WORKBENCH → API`.
- Every node points downward; every node's status is honest: `DETERMINISTIC_FACT | MACHINE_PROPOSED |
  HUMAN_REVIEWED | ACCEPTED`.

**🟢 GATE 0.1** — *Run* `python3 machinelearning/theatre_check.py --status`. You must see every component
as `CAPABILITY_CANDIDATE` (or a stated non-candidate). If you see something overclaimed as VALIDATED,
STOP and note it. This tells you the honest state of every component you might touch.

**📘 CODE-LEVEL REFERENCE (read before touching any ML module):**
`handover/agent-1-ml/ML-MECHANICS-REFERENCE.md` — the code-level inventory of every module (`nyayagate.py`,
`strength.py` (Bayesian), `cluster.py`, `retrieval.py`, `argument.py`, `aifgraph.py`, `corpus.py`,
`c1corpus.py`, `metrics.py`, `eval.py`), their honest status, how they connect, and the next tasks. Read
it after this orientation and before editing any mechanic.

**🧭 ARCHITECTURE REVIEWS (imported — read for direction):**
`machinelearning/_ACTIVE/PHILOSOPHY-ENGINE-ARCHITECTURE-REVIEW.md` + `PHILOSOPHY-ENGINE-INFRASTRUCTURE-REVIEW.md`
(the two imported reviews) + `machinelearning/_ACTIVE/BRAINSTORM-PHILOSOPHY-ENGINE-VS-PATALA.md` (the
synthesis). They validate our DebateFrame/SemanticAlignment direction and add `Commitment`,
`Attack`/`Defeat`, `EvaluationProfile`, `Crux-as-outcome-sensitivity` — most of which is correctly
**later than the CP4 gold**, except `Commitment` (who asserts vs attributes-to-opponent) which is worth
adopting into the gold shape now.

**🔁 LIVING PLAYBOOK (agentic infra — update as functions prove out):**
`handover/agent-1-ml/AGENTIC-INFRA-PLAYBOOK.md` — the living reference for agentic-infrastructure
functions: ADOPTED / TRIED / SKIPPED / OVERKILL, updated with what actually works in practice (Gas Town
persistent identity + git durability are ADOPTED; the typed handoff is PILOTING; Temporal/LangGraph/
CrewAI are OVERKILL). `machinelearning/_ACTIVE/AGENTIC-INFRA-COMPARISON.md` is the one-time survey behind it.

### Step 0.3 — Know the two lanes (never drift)
| | **Agent 2 — L0 / integration** | **YOU — Agent 1 / ML** |
|---|---|---|
| Direction | **vertical truth** | **horizontal + upward derivation** |
| Lane | SOURCE → segmentation → morphology → syntax → alignment → translation proof | C1 → themes → arguments → claims → synthesis → review |
| Question | *Is this reading licensed by the source?* | *Does this higher-order representation legitimately derive from the scholarly objects beneath it?* |
| Checkpoint | **CP1** (PhilologicalProof) | **CP0, CP2, CP3, CP4** |
| Now doing | P0 35/35 PASS; P1–P5 Vidyut/Heritage witnesses | **Argument Gold (CP4)** — this is you |

**🟢 GATE 0.2** — *Read* `handover/agent-2-integration/CHECKPOINTS-INTEGRATION.md` (Agent 2's current
focus). You must be able to state in one sentence what Agent 2 owns and is doing — so you stay out of CP1.
The shared boundary is contractual: join only on **Passage ID / TranslationDecision ID / PhilologicalProof
ID / C1 ID**, never fuzzy.

### Step 0.4 — The checkpoint ladder (your coordinate system)
```
CP0 BENCHMARK · CP1 SOURCE PROOF · CP2 RETRIEVAL · CP3 THEMES · CP4 ARGUMENT · CP5 VERIFICATION
CP6 SYNTHESIS · CP7 WORKBENCH · CP8 ADVERSARIAL REVIEW · CP9 API/MCP · CP10 COLLAB · CP11 ECONOMIC · CP12 CROSS-CORPUS
```
Honest state: **CP0 DONE · CP1 PARTIAL(L0) · CP2 PARTIAL · CP3 PARTIAL · CP4 PARTIAL · CP5–CP6 PARTIAL ·
CP7+ NOT STARTED.** Your immediate build = **the CP4 gate: complete Argument Gold (ARG-001..005).**

**The anti-weeds rule (every task, always):** name (1) the checkpoint it advances, (2) the scholarly
object it makes more trustworthy, (3) the benchmark/proof of success. If it can't answer all three, don't
build it.

---

## PHASE 1 — THE DOCTRINE (the one rule that governs every build)

### Step 1.0 — Read the governing rule
**Read `machinelearning/_ACTIVE/AGENTS-DOCTRINE.md`** (the master anti-theatre rule) and **`AGENTS.md`**
(repo root, auto-loaded).

> **Nothing is "real" because code exists. It becomes real only when independent gold + blind eval +
> metric + human adjudication show it does what its name claims.**

- **Banned words:** PROVED · TRUTH · CORRECT · EDITOR APPROVED · BEST · WINS.
  **Use:** SUPPORTED BY · PASSED CHECK X · BENCHMARKED ON · MACHINE-PROPOSED · REVIEWED BY.
- **The checkpoint test for every build:** *What experiment would convince you this does NOT work?* If you
  can't answer it, don't build it.

### Step 1.1 — The tone axioms (your axioms of existence — non-negotiable)
These are NOT suggestions. They are part of what it means to be an agent here. Adopt them in every
answer and every build. (Defined once in `handover/AGENTS.yaml` `doctrine`; derived into your
orientation; Agent 0 enforces them.)

1. **Be brutally honest** about what is real vs hollow. Interrogate "is this useful?" — do not assume yes.
2. **Retract overclaims explicitly.** "I was a yes-man. The honest version is X." Never compound a lie.
3. **Name the failure mode when you see it** — the same circularity as B-STRUCT, a hardcoded status, a fuzzy ID.
4. **Separate real from theater plainly.** Category A (infrastructure) is not a result. Evidence + measurement is a result.
5. **No hype.** "structurally sound" is not "scholarship." "tests pass" is not "this works." A checker passing on your own docs is circular, not a win.
6. **Precision over coverage.** Abstain rather than invent. "NO UNIQUE ARGUMENT RECOVERABLE" is a valid, valuable output.

**🟢 GATE 1.1** — These axioms are enforced by `handover/check_staleness.py` (it checks your orientation
adopts them) and by Agent 0. A yes-man tone is a failure mode, not a personality trait.

**🟢 GATE 1.0** — *Open* `machinelearning/_ACTIVE/CLAIMS.md` (the self-audit ledger P-001..P-010). Read
the current STATUS/EVIDENCE/CAVEAT of each claim. You will update this ledger honestly as you work.

---

## PHASE 2 — THE AGENT-SPECIFIC HANDOVER & SESSION (what THIS lane learned)

### Step 2.0 — Read the working doctrine
**Read `machinelearning/_ACTIVE/AGENT1-HANDOVER.md`.** This is the accumulated hard-won knowledge: the 10
AXIOMS (treat as gospel) and the recurring errors. The master failure mode:
> **Building structurally-elegant-but-hollow objects and reporting them as results.**

Three concrete instances this session you must recognize instantly:
1. **B-STRUCT "won"** the builder comparison — CIRCULAR (premises were C1 titles). Retired.
2. **`strength.py`** labeled "truth-engine scorer" — was a toy (hand-chosen weights). Relabeled.
3. **Gold-chain hardcoded `EDITOR_APPROVED`** — fabricated a review status. Fixed.

**🟢 GATE 2.0** — *Open* `handover/agent-1-ml/SESSION-2026-08-12.md`. Confirm you understand the module
inventory table (real vs hollow), the key decisions (B-STRUCT retired, benchmark frozen, gate unwired),
and the honest state. You must be able to say which modules are REAL vs HOLLOW before you touch anything.

### Step 2.1 — Know the recurring errors to watch for
- **Structurally-elegant-but-hollow** — a well-typed empty container reported as a result.
- **Circular results** — a "winner" trivially related to the ground truth's input (B-STRUCT).
- **Hardcoded statuses** — `EDITOR_APPROVED` set in code with no real review.
- **Fuzzy ID resolution** — wrong-but-confident matches (the fabricated-ID lesson).
- **Scope creep** — building essay layers when the machine is the audit trail.
- **Tuning metrics to pass** — moving a threshold to make C1s pass, not to measure a real signal.

---

## PHASE 3 — EXPLORE THE ACTUAL PĀṬALA CODEBASE (the files, not just the docs)

This is where the orientation used to fail — it pointed at docs but never made you open the real code. Do
this now.

### Step 3.0 — Explore the ML package
**Run:** `ls machinelearning/research/patala_ml/`. You must see these key modules and know roughly what
each does:
- **`gold.py`** → ARG-GOLD-001 (V2-O transcendental). **`gold002.py`** → ARG-GOLD-002 (V2-L objection-reply).
- **`goldutil.py`** → `wrap_fixture` + `validate_gold` (the consistency validator). ← **the tooling you'll use**
- **`nyayagate.py`** → the frozen 5-hetvābhāsa gate (do NOT hack).
- **`cluster.py`, `argument.py`, `strength.py`, `essay*.py`, `retrieval.py`** → derivations (mostly hollow/partial).
- **`philproof.py`, `cleanup.py`** → the L0 handshake + honest ID resolver.

**🟢 GATE 3.0** — *Open* `machinelearning/research/patala_ml/goldutil.py`. Read `validate_gold` — this is
the consistency validator you will run against all 5 golds. Then open `gold002.py` and study its shape
(nodes/inferences/boundary/debate_frame) — that is the exact template for ARG-003/004/005.

### Step 3.1 — Explore the benchmark
**Run:** `find benchmarks/v0 -type f`. You must see:
```
benchmarks/v0/MANIFEST.json  SCHEMA.md  SPLITS.md  METRICS.md  README.md
benchmarks/v0/structure/  PAT-STRUCT-001.json  PAT-STRUCT-002.json
benchmarks/v0/evidence/    nyaya-gate-gold.jsonl
benchmarks/v0/retrieval/   PAT-RETRIEVAL-001.jsonl
benchmarks/v0/runs/        (immutable run records)
```

**🟢 GATE 3.1** — *Open* `benchmarks/v0/structure/PAT-STRUCT-002.json`. Confirm it is a wrapped
BenchmarkFixture (task `argument_extraction`, split `EVALUATION_ONLY`, `expected` = the gold). This is the
output format your new golds must produce.

### Step 3.2 — Locate the sources (the crux — they are NOT in this repo)
The C1/L2/l200 files the golds reference live on the **sanskritree mount**, not in patala:
```
C1:   /mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/c1/read/
L2:   /mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/pilot/   (pilot_V*_L2_read.md)
L200: /mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/l200/
```
Verified real files for the gold series (passage_ids in `data/published/ipvv/index.json` resolve):
- V2-O `c1_V2O-orderless-support.md` + `pilot_V2O_L2_read.md` → ARG-001/003
- V2-L `c1_V2L-nonconstructed-I.md` + `pilot_V2L_L2_read.md` → ARG-002 (done)
- V2-H `c1_V2H-vimarsa-paravak.md` + `pilot_V2H_L2_read.md` → ARG-004
- V3-I `c1_V3I-difference-real.md` + `pilot_V3I_L2_read.md` → ARG-005

**🟢 GATE 3.2** — *Run*: `grep -c "" <C1 file>` on at least one `c1_V*.md` and one `pilot_V*_L2_read.md`.
You must get a line count > 0 (the files exist). You are now ready to build gold from real sources.

---

## PHASE 4 — THE EXACT NEXT STEPS (what to build)

### Step 4.0 — Complete Argument Gold (the CP4 gate; judgment-heavy)
Build the remaining 3 gold arguments, hand-constructed from the real C1/L2:
```
ARG-003  reductio       — V2-O's ordered-support regress
ARG-004  conceptual distinction — vimarśa vs prakāśa (V2-H) or one-light (V3-C)
ARG-005  ambiguous      — two defensible reconstructions (V3-I difference-real)
```
For each: read the C1 (`> ` body) + L2 (`pilot/pilot_<chunk>_L2_read.md`), extract the actual propositions,
build the full Proposition/Inference/Defeater shape + the DebateFrame/SemanticAlignment wrapper (critical
for ARG-005 — record the alignment between the two readings). Add the builder to the `GOLDS` registry in
`emit_gold_fixtures.py`, run it, and confirm `validate_gold` passes. Do NOT automate extraction yet.

**Build them WITH the philosophical-IR shape** (see `machinelearning/_ACTIVE/ARGUMENT-IR-VISION.md` — the
CP4 target). Do not defer these; they are part of the gold:
- **`Commitment` (speaker/force) on every node** — ASSERTS / DENIES / PRESUPPOSES /
  ASSUMES_FOR_ARGUMENT / ATTRIBUTES_TO_OPPONENT / QUOTES / RECONSTRUCTED. This fixes the
  pūrvapakṣa error (the Buddhist objection read as Abhinava's own view — critical for ARG-003 reductio
  and ARG-005 ambiguous).
- **derivational `Proposition`** — each node records `derived_from` (Sanskrit / L2 / C1 / implicit) +
  `explicitness` (already have).
- **a `ResearchQuestion`** at the top of each argument (the question it answers).
- **split `Defeater` into `Attack` (data) + `Defeat` (derived)**.
- **three-level `SemanticAlignment`** (LEXICAL/CONCEPTUAL/PROPOSITIONAL) for ARG-005's two readings.

Let the gold force the ontology — expand the schema only where the scholarship demands it. Do NOT build
EpistemicRegime/EvaluationProfile/Crux yet; the gold must come first. An argument whose honest output is
`NO SAFE RECONSTRUCTION` is a valid gold case, not a failure.

### Step 4.1 — Validate all 5 golds are internally consistent
**🟢 GATE 4.1** — *Run*: `cd machinelearning/research && . .venv/bin/activate && python
experiments/emit_gold_fixtures.py`. You must see **ALL 5** PAT-STRUCT fixtures pass `validate_gold`
(consistent). This is the "gold is worth reviewing" gate. Do not proceed to extraction until it passes.

### Step 4.2 — THEN attempt automatic extraction (Build 4)
Run a primitive extractor against the 5 golds blind. Measure: proposition precision/recall · role macro-F1
· grounding precision · explicitness accuracy · inference recovery · scope errors · abstention. Record a
`BenchmarkRun`. This tells you whether extraction is worth building.

### Step 4.3 — THEN viruddha becomes a graph operation (Build 5)
Once real proposition graphs exist, viruddha = "retrieve accepted propositions related to H/S → does H
support ¬S → VIRUDDHA_CANDIDATE → semantic layer decides." NOT a keyword hack.

### Step 4.4 — Adjudicate 3 themes (CP3)
Order-less Support · Vimarśa · Pramāṇa → `AcceptedTheme` objects with real review events.

---

## PHASE 5 — GUARDRAILS & THE FINAL SELF-CHECK (before claiming anything)

### Step 5.0 — The guardrails (do not violate)
1. **Do NOT hack viruddha into `nyayagate.py`** — it stays frozen at v1.
2. **Do NOT rush DOUBLE_REVIEWED** before broadening the gate fixtures to 30–50.
3. **Do NOT build the essay layer / Bayesian propagation / more clustering.**
4. **Do NOT pursue the Lean bridge** (proves FOL tautologies, not Abhinavagupta).
5. **Every passage_id must resolve** — real `pt:passage:ipvv:chunk<...>`, never fuzzy.
6. **Route everything through `benchmarks/v0/`** + record a `BenchmarkRun` for any result.
7. **Update CLAIMS.md** + `theatre_check.py` honestly as you go.
8. **Do NOT edit** `data/corpus/`, `app/`, `lib/`, `pipeline/verify_l0.py`, or `philproof.py` internals
   (those are Agent 2's). Consume their output via the shared `Ref` contract.

### Step 5.1 — The "no-BS" self-check (falsification before promotion)
For each build, answer:
> **What experiment would convince you this does NOT work?**

- Argument Gold: "a second reviewer finds a proposition that doesn't match the C1/source."
- The gold-consistency validator: "a passage_id doesn't resolve; an inference references a missing node."
- Extraction: "can't recover >60% of gold propositions, or false-grounding >5%."
- viruddha-via-graph: "flags as VIRUDDHA a pair that a human says are CONCEPTUAL_MISMATCH or
  QUESTION_MISMATCH."

**🟢 GATE 5.1** — Before declaring ANY build done, run the full suite:
`cd machinelearning/research && . .venv/bin/activate && for t in tests/*.py; do python $t; done` — then
update `CLAIMS.md` (add P-009 Argument Gold, P-010 DebateFrame as you complete them) and `theatre_check.py`
honestly.

### 🔄 THE SESSION-UPDATE LOOP (do this EVERY session end — it keeps vision ↔ work linked)
1. **Update the live state:** `python3 handover/flow.py update agent1 CP4 <status> -n "<what changed>" --by agent1`
   (bumps the version, records it in history).
2. **Update this lane's INDEX:** edit `handover/agent-1-ml/INDEX.md` — move done items to "done", name
   the current work at the top (the 🔴 ACTIVE WORK section).
3. **Update the vision's Layer 3:** edit `docs/vision/CORE-BIBLE.md` if CP4's status text changed, and
   `handover/CHECKPOINTS.md` if the "ACTIVE NOW" line changed.
4. **Drop a session note:** append to `handover/agent-1-ml/SESSION-<date>.md` (never overwrite).
5. **Verify:** `python3 handover/check_staleness.py` — must be 0 failures.

**This is what keeps the link clear:** vision (CORE-BIBLE Layer 3) → CP4 → this INDEX (current work) →
STATE.yaml (live progress). Each session, these update together.

---

## PHASE 6 — THE ONE-SENTENCE CARRY-FORWARD

**You are Agent 1 (ML, upward derivation). The Nyāya gate is frozen (measured, honest); your job is to
complete Argument Gold (ARG-001..005) with the DebateFrame/SemanticAlignment layer — because viruddha,
counterevidence, and all cross-argument comparison require argument-under-a-frame, and a real argument
graph, before they can be sound. Build the gold first (the tooling is ready), validate it's internally
consistent, then test extraction against it blind — and only then does viruddha become a graph operation.
Route everything through the frozen benchmark, never claim a result without a BenchmarkRun, and keep the
honest vocabulary.**
