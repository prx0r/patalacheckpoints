# Agent 1 — ML/RESEARCH LANE INDEX

*The one living pointer for Agent 1's current state — done / in-progress / next. Update this as you work.
Append-only history lives under this folder; this file is the single "what is true right now" source for
the ML lane.*

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
> living summary.

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
1. **Nyāya gate → viruddha-via-graph** — the hard remaining part. Detecting "memory proves the self is
   constructed" is a defect needs the argument graph (IPVV argues the opposite, V2-P). Keyword rules can't.
   This is where the gate + Pāṭala's C1/argument layer connect for real.
2. **Wire `verify-claim-semantic`** — fill `argument.py`'s empty `gate` slot + `lib/verify.ts` + the API.
3. **Grow the argument gold** (ARG-GOLD-001..010, independently reviewed) — CP4.
4. **Retrieval re-baseline on split S2** — CP2 (currently S1-nonleak).

**Do NOT:** build new layers, add graph abstractions, or pursue the Lean bridge (proves FOL tautologies,
not Abhinavagupta).

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
