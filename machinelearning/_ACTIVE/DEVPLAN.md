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

> **Where we are (2026-08-12):** CP4 (Phase 3 — machine-readable philosophy) has entered empirical
> development. The 5 Argument Gold fixtures exist and are internally consistent; a blind primitive baseline
> is recorded; and a vertical object resolves one proposition all the way down. The blocker is now
> **independent review of the gold** — the argument layer is structurally real but scholarly CANDIDATE.

| Asset | Status | Real? |
|---|---|---|
| **`benchmarks/v0/`** | frozen (MANIFEST/SCHEMA/SPLITS/METRICS) + **ARG-GOLD-001..005** | ✅ REAL (the measurement substrate) |
| **Argument Gold** | ARG-001..005, `validate_gold`-consistent, **task_level A/B/C + commitment + support_scope** | 🔶 **CANDIDATE** — machine-authored, **NOT independently reviewed** (the current gate) |
| **Baseline extractor** | run BLIND vs the 5 golds; **lexical-overlap F1 0.36, inference recovery 0.0** | 🔶 baseline (the floor to beat); P-003 NOT_ESTABLISHED |
| **Vertical object** | one proposition resolves downward (exact refs, typed `GroundingLink`s, honest proof status) | ✅ infrastructure/serialization (v0 frozen); P-014 |
| **Review packet (v2, primary-Sanskrit)** | `benchmarks/v0/ARG-GOLD-REVIEW-PACKET-v2.md` + machine-checkable `benchmarks/v0/review/ARG-GOLD-REVIEW-PACKET-v2.json` — self-contained, reviewer-facing, grounded directly to primary Sanskrit (L2 never required) | ✅ the tool to get independent review |
| **The Nyāya gate** (truth-engine, 680 LOC) | `NYAYA_GATE_CANDIDATE_v1`, deterministic | ✅ REAL, **UNWIRED — deferred until gold reviewed + real `Inference` objects exist** |
| **L0 proofs** (`verify_l0.py`) | P0 harness, **V2/V3 35/35 PASS** (lossless, frozen), + Vidyut P2 witness + Heritage ensemble | ✅ REAL |
| **`cluster.py`** | real graph topology | 🔶 machine proposals, not accepted themes |
| **`strength.py`** | BayesianEvidencePrimitive | 🔶 math; uncalibrated (no epistemic role yet) |
| **`argument.py`** | schema; `gate` slot empty | 🔶 container, not argument |
| **essay/AIF/c1metrics** | representations/diagnostics | 🔶 infrastructure, no validated content |

**The single highest-value real build (now): REVIEW the Argument Gold first (via the review packet), then
build a real extractor, then wire the Nyāya gate over real `Inference` objects.** The gate is real but
unwired; it must NOT be wired onto arbitrary claims — it plugs in at CP4 once real `Proposition`/`Inference`
objects exist (per `handover/CHECKPOINTS.md`). Sequence: independent review of ARG-001..005 → (one clean
reviewed argument enables the py-aspic pilot) → a real extractor (blind, beats baseline) → argument graph →
then the gate as an audit of the `Inference`.

---

## 1. PHASE A — WIRE THE NYĀYA GATE — CP4/CP6 semantic verification (DEFERRED, not immediate)

> **Order correction (2026-08-12):** this is NOT the immediate build. The gate must wait for a
> *reviewed* argument with real `Proposition`/`Inference` objects (per `handover/CHECKPOINTS.md` +
> `CLAIMS.md` P-003/P-004). Immediate = independent gold review, then a real extractor, then the gate.
> This section is the gate's *eventual* wiring, kept for when the argument graph is real.

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

> **Order corrected (2026-08-12, revision 2).** The bottleneck is **epistemic, not engineering** — more
> machine evaluation against machine-created gold (`M1 → G_machine → M2 → metric`) does not advance the
> epistemic state. The governing doctrine (see `handover/agent-1-ml/NEXT-STEPS.md`): *when the missing
> oracle is human scholarly judgment, do not substitute another model — either obtain the judgment, or
> work only on claims verifiable mechanically.* So the extractor, gate wiring, and neural retrieval are
> **PARKED** until the human review crosses the gate. What advances now is either **human-reviewed**
> progress or **construction-verifiable** progress.

| # | Build | CP | Kind | Why / status |
|---|---|---|---|---|
| **0** | **Fix worktrees + reconcile commits** | — | operational | Agent 0 action; hard precondition (Axiom 11). No experimental work, benchmark mutation, gold edit, or canonical model run until done. |
| **1** | **Independent review of ARG-GOLD-001..005** (target: ≥1 argument, ARG-002 v2) | CP4 | human-reviewed | the CP4 critical path. Success metric `count(INDEPENDENT_REVIEWED) > 0`. Packet: `benchmarks/v0/ARG-GOLD-REVIEW-PACKET-v2.md` (primary-Sanskrit grounded; gate: `check_review_packet.py`). Also instrument the review → first prototype of the Workbench/Review product. |
| **2** | **PĀṬALA-FIDELITY synthetic corruption suite** | CP4/CP0 | construction-verifiable | inject deterministic mutations (drop/duplicate/shift span, reorder, unknown-region; flip lemma/case/number/gender/replace surface; shift/remove/wrong/swapped anchor; delete grounding edge, nonexistent ref, stale proof, source-hash change) → assert the verifier fails. Metric `Sensitivity(V,E)`. **`SYNTHETIC_SENSITIVITY ≠ REAL_WORLD_RECALL`.** |
| **3** | **Deterministic graph baseline (k-core)** | CP3 | construction-verifiable | at least one deterministic canonical baseline (not "replace Louvain forever"). Test: `assert hash(run(graph)) == hash(run(graph))` across processes. |
| **4** | **Support / wait for human gold review** | CP4 | — | the gate that unlocks everything downstream. |

**PARKED until review (P4 of NEXT-STEPS):** the real extractor · gate gold fixtures + wiring
`verify-claim-semantic` · retrieval re-baseline on S2 · DSPy · HippoRAG/PPR · cross-encoder semantic
alignment · semantic microscope B–E · crux ML · argument ranking. Their evaluation reduces to the closed
machine loop and does not establish philosophical correctness.

**Do NOT:** build more essay layers, add graph abstractions, or port the Bayesian ontology (rejected in
`TRUTHENGINE_TO_PATALA_MAPPING.md`).

---

## 5. PHASE D — THE NEURAL / RETRIEVAL LAYER (the "semantic microscope" north-star)

> **Speculative vision + full review vs current state:** `machinelearning/_ACTIVE/RETRIEVAL-NEUROSYNTHETIC-VISION.md`
> (Stages A–E + the per-framework verdicts). The governing rule that keeps it non-theatre:
> **neural models discover neighbourhoods; Pāṭala turns them into typed, reviewable relations.**

The staged path (benchmark each layer before adding the next):
```
SEMANTIC ALIGNMENT v0 → HYBRID RETRIEVAL → SEMANTIC ATLAS → ARGUMENT-AWARE RETRIEVAL
→ GRAPH MEMORY / MULTI-HOP → COUNTERFACTUAL → SCHOLAR PRODUCT
```

**Current status (revision 2):** D1 (semantic alignment), D3 (multi-hop/PPR), and D4 (hybrid retrieval)
are **PARKED** until the human gold review crosses the gate — their evaluation is the closed machine
loop `M1 → G_machine → M2 → metric`, which does not establish philosophical correctness. Only **D2** is
now, reframed as a construction-verifiable baseline:

| # | Build | What | Why / status |
|---|---|---|---|
| D2 | **Deterministic graph baseline (k-core)** | at least one deterministic canonical baseline (rerun-today = rerun-tomorrow) — can be compared later against Louvain/Leiden/semantic clustering once real theme gold exists | fixes a real reproducibility risk (k-core paper, 2603.05207); do NOT assume determinism = better semantics. Test: `assert hash(run(graph)) == hash(run(graph))` across processes |

**PARKED until review:** D1 semantic alignment (Stage A harness already exists; baseline 0/8 falsified) ·
D3 multi-hop PPR over the curated graph (HippoRAG idea, NOT OpenIE) · D4 hybrid scholarly retrieval
(lemmas + C1 + arguments). **Pilot later (once gold matures):** DSPy for extraction/alignment
optimization.
**Avoid:** Kùzu (ARCHIVED), GraphRAG/LightRAG as dependencies (pattern libraries only). Benchmark each
neural layer on Pāṭala's own (reviewed) gold; never claim a neural output as validated.

---

## 6. THE CHECKPOINT-TEST (applies to every build)

> **What experiment would convince you this does NOT work?**

If you can't answer it, the capability isn't ready for evaluation. And every result must carry lineage
(benchmark_version · gold_version · commit · split · seed · config · date) or it doesn't exist.

---

## 7. The sequence

```
0 (fix worktrees) → 1 (independent gold review, CP4 critical path)
   → 2 (PĀṬALA-FIDELITY corruption suite, concurrent) → 3 (deterministic baseline, concurrent)
   → 4 (human gold review crosses the gate)
   → ONLY THEN: extractor → external evaluator → semantic alignment → neural retrieval
```
Each gated on the checkpoint-test + the anti-theatre protocol. Nothing promotes to `VALIDATED` without
independent gold + blind eval + metric + human adjudication.
