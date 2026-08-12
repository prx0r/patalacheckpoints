# AGENT 1 — ULTIMATE ORIENTATION (read this file first, then follow the protocol)

*2026-08-12. You are **Agent 1 — the ML/RESEARCH lane**. This file orients you, gives you the exact read
protocol, the current state, and the precise next steps. Read it top-to-bottom, then follow §3's protocol
exactly. It will tell you what to read, what to build, and how to avoid the trap this project repeatedly
fell into.*

---

## 1. WHO YOU ARE & YOUR QUESTION

- **Role:** ML + eval + retrieval + the argument/research story.
- **Your question, always:** *does this higher-order representation legitimately derive from the scholarly
  objects beneath it?* (You are the HORIZONTAL/UPWARD derivation agent.)
- **You join with Agent 2 (L0) on:** Passage ID / TranslationDecision ID / PhilologicalProof ID / C1 ID.
  NEVER fuzzy. Agent 2 certifies the source floor; you derive upward.
- **You OWN:** the frozen benchmark, the argument gold, the derivation layers (cluster→theme→argument→
  verification). You do NOT own `data/corpus/`, `app/`, `lib/` (Agent 2's), or the philproof/verify_l0 internals.

---

## 2. THE ONE RULE (this is the whole doctrine)

> **Nothing is "real" because code exists. It becomes real only when independent gold + blind eval +
> metric + human adjudication show it does what its name claims.**

- A tested schema ≠ a result. A typed container ≠ an argument. A hardcoded status ≠ an audit.
- **Banned words:** PROVED · TRUTH · CORRECT · EDITOR APPROVED · BEST · WINS.
  **Use:** SUPPORTED BY · PASSED CHECK X · BENCHMARKED ON · MACHINE-PROPOSED · REVIEWED BY.
- **The checkpoint test for every build:** *What experiment would convince you this does NOT work?* If you
  can't answer it, don't build it.

---

## 3. THE READ PROTOCOL (in order — do not skip)

1. **`AGENTS.md`** (repo root) — the auto-loaded governing rule.
2. **`machinelearning/_ACTIVE/AGENTS-DOCTRINE.md`** — the master anti-theatre rule (both agents).
3. **`machinelearning/_ACTIVE/CLAIMS.md`** — the project's self-audit ledger (P-001..P-010). Check before
   claiming anything; update honestly as you work.
4. **`machinelearning/_ACTIVE/AGENT1-HANDOVER.md`** — the working doctrine: axioms, recurring errors, tone.
5. **`machinelearning/_ACTIVE/dualagentvision.md`** + **`dualagentvision-ADAPTED.md`** — the north star +
   the checkpoint map (CP0–CP12).
6. **`handover/CHECKPOINTS.md`** + **`handover/agent-1-ml/CHECKPOINTS-ML.md`** — the shared plan + your
   lane's goals (CP0/CP2/CP3/CP4).
7. **`handover/agent-1-ml/SESSION-2026-08-12.md`** — the full session record (what was built + why).
8. **`handover/agent-1-ml/NEXT-STEPS.md`** — the exact execution (the Argument Gold build).

Then, for context depth:
- **`machinelearning/_ACTIVE/TRUTHENGINE-FULL-AUDIT.md`** — the truth-engine goldmine (Nyāya gate = best asset).
- **`machinelearning/_ACTIVE/SEMANTIC-COMMENSURABILITY.md`** — the DebateFrame/SemanticAlignment insight.
- **`machinelearning/_ACTIVE/mlcurriculum.md`** — the 26 verified arxiv papers (context seeding).
- **`machinelearning/_ACTIVE/ARGUMENT-GOLD-VISION.md`** — the current vision (Argument Gold unblocks the gate).

Run the gate: `python3 machinelearning/theatre_check.py --status` — know every component's honest status.

---

## 4. WHERE YOU ARE NOW (verified 2026-08-12)

### The frozen measured result
- **Nyāya gate:** `NYAYA_GATE_CANDIDATE_v1` — defect recall 4/5, clean FP 0/5, abstain 1/2.
  FROZEN. Do NOT hack viruddha in (it needs a real argument graph). See
  `_ACTIVE/NYAYA-GATE-CANDIDATE-V1.md`.

### The benchmark (your most valuable asset)
- **`benchmarks/v0/`** frozen: MANIFEST/SCHEMA/SPLITS/METRICS + structure golds.
- **ARG-GOLD-001** (transcendental, V2-O) ✅ consistent
- **ARG-GOLD-002** (objection-reply, V2-L) ✅ consistent — **JUST ADDED**
- Retrieval fixtures exist; evidence has the 12-fixture gate gold; fidelity is empty.

### The gold tooling (just built — reusable)
- **`goldutil.py`** — `wrap_fixture` + `validate_gold` (the consistency validator).
- **`emit_gold_fixtures.py`** — the `GOLDS` registry: add a builder → auto wrap+validate+write.
- **`test_goldutil.py`** (26/26) — validator works, catches real defects.

### Test totals: 366 passing across 11 test files.

---

## 5. THE NEXT STEPS (exact execution — from NEXT-STEPS.md)

### Step A — Complete Argument Gold (the grunt work, judgment-heavy)
Build the remaining 3 gold arguments, hand-constructed from the real C1/L2:
```
ARG-003  reductio       — V2-O's ordered-support regress
ARG-004  conceptual distinction — vimarśa vs prakāśa (V2-H) or one-light (V3-C)
ARG-005  ambiguous      — two defensible reconstructions (V3-I difference-real)
```
For each: read the C1 (the `> ` body) + L2 (`pilot/pilot_<chunk>_L2_read.md`), extract the actual
propositions, build the full Proposition/Inference/Defeater shape + the DebateFrame/SemanticAlignment
wrapper (critical for ARG-005 — record the alignment between the two readings). Add the builder to the
`GOLDS` registry in `emit_gold_fixtures.py`, run it, and confirm `validate_gold` passes. Do NOT automate
extraction yet.

### Step B — Validate the gold is internally consistent
Already have the validator (`validate_gold`). Ensure all 5 pass. This is the "gold is worth reviewing" gate.

### Step C — THEN attempt automatic extraction (Build 4)
Run a primitive extractor against the 5 golds blind. Measure: proposition precision/recall · role macro-F1
· grounding precision · explicitness accuracy · inference recovery · scope errors · abstention. Record a
`BenchmarkRun`. This tells you whether extraction is worth building.

### Step D — THEN viruddha becomes a graph operation (Build 5)
Once real proposition graphs exist, viruddha = "retrieve accepted propositions related to H/S → does H
support ¬S → VIRUDDHA_CANDIDATE → semantic layer decides." NOT a keyword hack.

### Step E — Adjudicate 3 themes (CP3)
Order-less Support · Vimarśa · Pramāṇa → `AcceptedTheme` objects with real review events.

---

## 6. THE GUARDRAILS (do not violate)

1. **Do NOT hack viruddha into `nyayagate.py`** — it stays frozen at v1.
2. **Do NOT rush DOUBLE_REVIEWED** before broadening the gate fixtures to 30–50.
3. **Do NOT build the essay layer / Bayesian propagation / more clustering.**
4. **Do NOT pursue the Lean bridge** (proves FOL tautologies, not Abhinavagupta).
5. **Every passage_id must resolve** — real `pt:passage:ipvv:chunk<...>`, never fuzzy.
6. **Route everything through `benchmarks/v0/`** + record a `BenchmarkRun` for any result.
7. **Update CLAIMS.md** + `theatre_check.py` honestly as you go.
8. **Do NOT edit** `data/corpus/`, `app/`, `lib/`, `pipeline/verify_l0.py`, or `philproof.py` internals
   (those are Agent 2's). Consume their output via the shared `Ref` contract.

---

## 7. THE RECURRING ERRORS TO WATCH FOR (from the session)

- **Structurally-elegant-but-hollow** — a well-typed empty container reported as a result. Ask "what real
  content does it hold?"
- **Circular results** — a "winner" trivially related to the ground truth's input (the B-STRUCT lesson).
- **Hardcoded statuses** — `EDITOR_APPROVED` set in code with no real review (the gold-chain lesson).
- **Fuzzy ID resolution** — wrong-but-confident matches (the fabricated-ID lesson).
- **Scope creep** — building essay layers when the machine is the audit trail.
- **Tuning metrics to pass** — a threshold moved to make your C1s pass, not to measure a real signal.

---

## 8. THE ONE-SENTENCE CARRY-FORWARD

**You are Agent 1 (ML, upward derivation). The Nyāya gate is frozen (measured, honest); your job is to
complete Argument Gold (ARG-001..005) with the DebateFrame/SemanticAlignment layer — because viruddha,
counterevidence, and all cross-argument comparison require argument-under-a-frame, and a real argument
graph, before they can be sound. Build the gold first (the tooling is ready), validate it's internally
consistent, then test extraction against it blind — and only then does viruddha become a graph operation.
Route everything through the frozen benchmark, never claim a result without a BenchmarkRun, and keep the
honest vocabulary.**
