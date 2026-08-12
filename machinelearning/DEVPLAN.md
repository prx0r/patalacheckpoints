# PĀṬALA — DEV PLAN (CONSOLIDATED, honest state)

*2026-08-12. The single authoritative execution plan. **Consolidates** DEVPLAN.md, LOGICAL-ORDER.md,
DEVPLAN_AGNOSTIC_CONTRACT.md, SPEC_CONSOLIDATED_BUILD.md, WIRE-NYAYA-GATE.md into one doc that reflects
the honest state after the anti-theatre cleanup. Governed by `AGENTS-DOCTRINE.md` + `CLAIMS.md` +
`COMPONENT-CONTRACTS.md`. **Read those first.***

> **The governing rule:** *Nothing is "real" because code exists. It becomes real only when independent
> gold + blind prediction + metric + human adjudication show it does what its name claims.* A tested
> schema ≠ a result. The checkpoint-test applies to every build.

---

## 0. THE HONEST STATE (what's real vs. hollow — from CLAIMS.md)

| Asset | Status | Real? |
|---|---|---|
| **`benchmarks/v0/`** | frozen (MANIFEST/SCHEMA/SPLITS/METRICS) + ARG-GOLD-001 | ✅ REAL (the measurement substrate) |
| **The Nyāya gate** (truth-engine, 680 LOC) | `NYAYA_GATE_CANDIDATE_v1`, deterministic | ✅ REAL, **UNWIRED** — the next build |
| **L0 proofs** (`verify_l0.py`) | P0 harness, 11/35 pass, honest | ✅ REAL (surfaces real bugs) |
| **L0 floor in gold-chain** | SOURCE_INTEGRITY PROVED, OPEN cruxes propagate | ✅ REAL |
| **`cluster.py`** | real graph topology | 🔶 machine proposals, not accepted themes |
| **`strength.py`** | BayesianEvidencePrimitive | 🔶 math; uncalibrated (no epistemic role yet) |
| **`argument.py`** | schema; `gate` slot empty | 🔶 container, not argument |
| **essay/AIF/c1metrics** | representations/diagnostics | 🔶 infrastructure, no validated content |

**The single highest-value real build: wire the Nyāya gate.** Everything else is either done (benchmark)
or infrastructure awaiting validated content.

---

## 1. PHASE A — WIRE THE NYĀYA GATE (the immediate build) — CP6 semantic verification

**The best use of the truth-engine's gate:** implement `verify-claim-semantic` — the deterministic gate
deciding whether a claim is *logically admissible* (pramāṇa + hetvābhāsa + falsifier) and whether it may
move evidence (`can_update_posterior`). It fills `argument.py`'s empty `gate` slot. Full justification:
`WIRE-NYAYA-GATE.md`.

### A1 — Gold for the gate (the CRITICAL prerequisite)
The gate is currently `NYAYA_GATE_CANDIDATE_v1` — deterministic but untested. **Before promoting it, it
needs hand-adjudicated gold fixtures** for each of the 5 hetvābhāsas:
```
asiddha      → positive (is one), negative, borderline
viruddha     → positive, negative, borderline
savyabhicara → positive, negative, borderline
satpratipaksa→ positive, negative, borderline
badhita      → positive, negative, borderline
```
- **GOLD:** `benchmarks/v0/evidence/` — positive/negative/borderline per fallacy, hand-adjudicated.
- **METRIC:** false-positive fallacy rate · detects each defect · no confusion of absence-of-evidence
  with asiddha · abstention.
- **ADOPTION GATE:** run blind → measure → compare vs regex + LLM + hybrid baselines → only then
  promote to `verify-claim-semantic`.

### A2 — The implementation
```
benchmarks/v0/evidence/   the gold fixtures (per fallacy, hand-adjudicated)
pipeline/                 port the gate's validate()/gate_claim() logic
lib/verify.ts             add verifyClaimSemantic(claim, ref)
app/api/verify/claim-semantic/route.ts
mcp/index.mjs             verify_claim_semantic tool
```
- The gate needs a **pramāṇa field** on claims (currently absent) — the first concrete data change.

### A3 — The bonus (free)
`satpratipaksa` (counter-balanced claim) **is** `discover_counterevidence` — the Phase-6
counterevidence tool, from the same gate.

---

## 2. PHASE B — GROW THE ARGUMENT GOLD (CP4) — build gold, not models

The scarce artifact is gold, not another extractor.

### B1 — The gold set (ARG-GOLD-001..010)
Target 10 hand-reconstructed arguments, each with:
```
exact Sanskrit source · real passage ID · textual propositions · interpretive propositions ·
implicit premises · objection/reply · inference relation · boundary · alternative reconstruction ·
why this reconstruction was chosen · review history
```
Make them DIFFICULT (the reviewer's mix):
- 2 clear · 2 implicit · 2 objection/reply · 1 reductio · 1 ambiguous reconstruction ·
  1 where two readings are defensible · **1 where extraction should return "cannot confidently reconstruct"**
The last one matters — a good system abstains.

### B2 — The abstraction benchmark
Add abstention metrics: **precision at accepted claims · coverage · abstention accuracy ·
false-assertion rate.** For scholarship: **precision over coverage** (40% coverage / 98% grounded >
95% / 75%). Each gold fixture is `SINGLE_REVIEWED` → `DOUBLE_REVIEWED` → `ADJUDICATED` via independent
reviewers (no closed-loop self-confirmation).

---

## 3. PHASE C — EVALUATE (only after A + B)

- **Retrieval re-baseline** (CP2): BM25/dense/hybrid on the frozen `benchmarks/v0/retrieval/`, split S2.
  Already partially done (S1-nonleak); refine to S2.
- **Argument extractor** (CP4): evaluate blind against ARG-GOLD-001..010. Metrics: proposition F1,
  grounding precision, relation F1, inference-scheme macro-F1, scope-fidelity error, abstention.
- **Semantic verification** (CP6): the Nyāya gate vs regex vs LLM vs hybrid on the adversarial
  benchmark (negation/scope/attribution/counterevidence/fallacies/boundary).

---

## 4. THE PRIORITY ORDER (what to do, and why)

| # | Build | CP | Why |
|---|---|---|---|
| **1** | **Gate gold fixtures** (evidence/ family) | CP6 | the gate is real but untested; gold makes it promotable |
| **2** | **Wire `verify-claim-semantic`** | CP6 | the best real asset, currently unused |
| **3** | **Argument gold 001–010** | CP4 | the scarce artifact; makes extraction scientific |
| **4** | **Retrieval re-baseline on S2** | CP2 | convert S1-nonleak to the honest split |

**Do NOT:** build more essay layers, add graph abstractions, or port the Bayesian ontology (rejected in
`TRUTHENGINE_TO_PATALA_MAPPING.md`).

---

## 5. THE CHECKPOINT-TEST (applies to every build)

> **What experiment would convince you this does NOT work?**

If you can't answer it, the capability isn't ready for evaluation. And every result must carry lineage
(benchmark_version · gold_version · commit · split · seed · config · date) or it doesn't exist.

---

## 6. The sequence

```
A (gate gold + wire gate)  →  B (argument gold)  →  C (evaluate against frozen benchmark)
```
Each gated on the checkpoint-test + the anti-theatre protocol. Nothing promotes to `VALIDATED` without
independent gold + blind eval + metric + human adjudication.
