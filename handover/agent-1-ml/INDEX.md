# Agent 1 — ML/RESEARCH LANE INDEX

*The one living pointer for Agent 1's current state — done / in-progress / next. Update this as you work.
Append-only history lives under this folder; this file is the single "what is true right now" source for
the ML lane.*

> **LEADING CHECKPOINT DOC: `handover/CHECKPOINTS.md`** (the shared 5-checkpoint plan + 7 canonical
> contracts) + **`handover/agent-1-ml/CHECKPOINTS-ML.md`** (this lane's goals: CP0/CP2/CP3/CP4).
> Read those before the current-state below.

---

## Lane

- **Role:** ML + eval + retrieval + the research story.
- **Owns:** `machinelearning/` (doctrine, benchmark, DEVPLAN, experiments), the curriculum, statistical
  rigor, leakage rules.
- **THE GOVERNING RULE (read `AGENTS.md` + `machinelearning/AGENTS-DOCTRINE.md` FIRST):**
  *nothing is real because code exists; it's real only when independent gold + blind eval + metric +
  human adjudication show it.* A tested schema ≠ a result. Route everything through the frozen benchmark.
- **Rule (frozen):** no INFER model is adopted until it beats a baseline on a fixed held-out set.
- **Do NOT:** edit `data/corpus/`, `app/`, `lib/` (Agent 2's ontology); re-derive Agent 2's structures
  (philproof internals, verify_l0); port the F1–F8/D1–D5/B1–B6 ontology (rejected — doesn't fit Pāṭala).

---

## Current state (2026-08-12) — THE HONEST PICTURE

> **Read `handover/agent-1-ml/SESSION-2026-08-12.md` first** — the full session record. This INDEX is the
> living summary. **The vision this feeds:** `docs/vision/CORE-BIBLE.md` (Layer 3 = checkpoints) — my
> CP4 work is the ACTIVE item there; update it via `handover/flow.py` at session end.

### 🔴 THE ACTIVE WORK RIGHT NOW (this is the live task)
**CP4 — gold gate MET; vertical object resolves; next = independent review of the 5 golds.**
```
Built this session:
  ARG-003  reductio                (V2-O ordered-support regress, 8 nodes/4 infs)   ✅
  ARG-004  conceptual-distinction  (vimarśa vs prakāśa, V2-H, 6/4)                 ✅
  ARG-005  interpretive scope      (V3-I: local vs systematic, 5/3, 2 Positions,    ✅
            3-level SemanticAlignment; retyped from AMBIGUOUS after review)
  Build 4  primitive extractor run BLIND vs all 5 golds → BenchmarkRun             ✅
            (baseline lexical-overlap F1 0.36, inference recovery 0.0; Task-A bound,
             metric BOUNDED as baseline-v0)
  Gate #3  VERTICAL OBJECT v0 (HARDENED) — one proposition (ARG-001 G-TC2) with EVERY edge  ✅
            TYPED + honest resolution: exact L0 grounding_refs (no fuzzy search for gold),
            GroundingLink{relation,resolution,review_state} per edge, proof marked STALE (not
            resolved), C1/L2 at SPAN_LEVEL, missing IR fields surfaced (not retrofitted).
            patala_ml/vertical.py + benchmarks/v0/vertical/vertical-v2o-g-tc2.json. FROZEN v0.
            ✅ NOW FULLY RESOLVED: Agent 2 regenerated the authoritative P0 proof → proof edge
               STALE → EXACT / REFERENCE_RESOLVED (on_disk_PASS True, roundtrip PASS, 0 unresolved).
               The auditable Sanskrit→C1 chain closes end-to-end. Cross-lane handoff logged.
  Review-driven: golds now carry task_level A/B/C + candidate_reconstruction +
             support_scope; validator expanded (structural well-formedness only).
Honest status: golds are MACHINE_PROPOSED/CANDIDATE — NOT yet independently reviewed.
```
Next in order: (1) **independent review of the 5 golds** via `benchmarks/v0/ARG-GOLD-REVIEW-PACKET.md`
(a self-contained, human-readable packet — no Pāṭala/JSON knowledge needed; ACCEPT/REVISE/REJECT/ABSTAIN),
(2) **then** py-aspic over the CLEANEST reviewed argument (adapter/semantics test, provenance stays in
Pāṭala), (3) a real extractor that beats the baseline, (4) THEN viruddha as a graph op. See `NEXT-STEPS.md`.

**The source of this task:** `handover/agent-1-ml/ORIENTATION.md` Phase 4 + `NEXT-STEPS.md` + the vision
(`docs/vision/CORE-BIBLE.md` Layer 3 / `handover/CHECKPOINTS.md` CP4).

### The pivot this session: epistemic hardening (not building more)
We built a full ML spine (cluster→argument→essay→gold-chain), then an audit exposed it was mostly
structurally-elegant-but-hollow. We pivoted to: frozen benchmark + enforced doctrine + honest relabeling
+ one genuinely measured result (the Nyāya gate).

### What is REAL (the honest set)
- **`benchmarks/v0/`** — the frozen evaluation substrate (the most valuable thing we built).
- **The Nyāya gate** (`nyayagate.py`) — measured: detection 0.80, false-positive 0.00, abstain 0.50.
- **The L0 proofs** (Agent 2's `verify_l0.py`) — V2/V3 35/35 P0 PASS, verified. The gold chain now
  consumes these.
- **The clusterer** (`cluster.py`) — real graph topology; MACHINE_PROPOSED themes.

### What is HOLLOW (admitted, do not present as results)
- `strength.py` (BayesianEvidencePrimitive — uncalibrated, no epistemic role)
- `argument.py` (schema; `gate` slot empty)
- The essay layer (`essaygen/essayplan/...` — scope creep, the endpoint not the machine)
- `aifgraph.py` (no real propositions), `c1metrics.py` (unvalidated thresholds)
- `builders.py` comparison — **RETIRED as CIRCULAR**

### In progress / next (in order — the real work)
1. **🔴 Complete the Argument Gold (ARG-003/004/005)** — CP4, THE live task. All 5 golds consistent =
   the CP4 gate (see ORIENTATION Phase 4 + `emit_gold_fixtures.py`).
2. **Validate all 5 golds** pass `validate_gold` — the "gold is worth reviewing" gate.
3. **Test automatic extraction blind** against the 5 golds (Build 4) — measure proposition P/R, role
   macro-F1, grounding, explicitness, inference recovery, abstention. Record a `BenchmarkRun`.
4. **THEN viruddha becomes a graph operation** (Build 5) over DebateFrames → `VIRUDDHA_CANDIDATE`.
5. **Adjudicate 3 themes** (Order-less Support · Vimarśa · Pramāṇa) → `AcceptedTheme` (CP3).

**Do NOT:** build new layers, add graph abstractions, pursue the Lean bridge, or hack viruddha into the
frozen gate.

---

## Key files (the doctrine + the state)

### The governing doctrine (read first)
- `AGENTS.md` (repo root) — auto-loaded; the ONE RULE + read-order.
- `machinelearning/AGENTS-DOCTRINE.md` — the master anti-theatre rule.
- `machinelearning/CLAIMS.md` — the project's self-audit ledger (P-001..P-008).
- `machinelearning/COMPONENT-CONTRACTS.md` — the 9-field anti-theatre contracts.
- `machinelearning/AGENT1-HANDOVER.md` — the working doctrine (axioms, errors, tone).
- `machinelearning/theatre_check.py` — the mechanical gate (run before claiming "done").

### The vision + plan
- `machinelearning/dualagentvision.md` + `-ADAPTED.md` — the north star + checkpoint map (CP0–CP12).
- `machinelearning/DEVPLAN.md` — the consolidated execution plan (Nyāya gate is the #1 build).
- `machinelearning/MLUSEINPATALA.md` — the frozen strategy.

### The truth-engine goldmine (external)
- `machinelearning/TRUTHENGINE-FULL-AUDIT.md` — the 22-doc inventory (Nyāya gate = best asset, unwired).
- `machinelearning/TRUTHENGINE_TO_PATALA_MAPPING.md` — reuse mechanisms, reject the ontology.
- `machinelearning/SANSKRITREE-LEAN-REVIEW.md` — the honest verdict: don't build on Lean.
- Runtime: `/root/projects/.meta/misc/truth-engine/` (code + docs-active).

### The research lane
- `machinelearning/research/` — the 26-module package + 10 test files (339 passing).
- `machinelearning/mlcurriculum.md` — the verified 26-paper curriculum.
- `benchmarks/v0/` — the frozen substrate (MANIFEST/SCHEMA/SPLITS/METRICS + gold).

---

## Guardrails reminder
Never edit the deterministic substrate (`data/published/`, `lib/verify.ts`, `data/corpus/themes.ts`,
`lib/citation.ts`, `data/corpus/graph.ts`) — consume it through the shared contract. The philproof/verify_l0
internals are Agent 2's lane; my consumer (`philproof.py`, `build_goldchain.py`) reads their output. Join on
Passage ID / Proof ID / C1 ID — never fuzzy.

## THE ACTIVE NEXT-STEPS DOC (current execution)
- **`handover/agent-1-ml/NEXT-STEPS.md`** — the exact how-to for the next session: build ARG-GOLD-002..005
  (transcendental/objection-reply/reductio/conceptual-distinction/ambiguous) with the
  DebateFrame/SemanticAlignment layer, the per-build gates, the falsification self-check, and the guardrails.
