# PĀṬALA GOLD-STANDARD MECHANISMS + FULL DATA FLOW (HIGH-LEVEL SPEC)

*2026-08-13 · The high-scale view of what we already have: the gold-standard mechanisms (proven,
frozen, or witness-level) and the complete data flow as implemented. This is a TRACKING doc — it tells
an agent "what exists, where it lives, what it proves, and how the data flows" so no work is duplicated
and no capability is lost. It complements `handover/agent-2-integration/CANONICAL-LAYER-STACK.md`
(the layer *order* + file types) and `docs/ML-VERIFIABLE-LAYER-CONTRACTS.md` (the per-layer
*done-correct* contracts). Read those three together.*

---

## 0. THE ONE-LINE PICTURE

We have a **two-agent, single-graph architecture** over the canonical stack, already implemented
through the controller:

```
Agent 2 (infrastructure + substrate + autonomous factory)
   └─ deterministic controller (autonomy.py) drives every layer via a per-layer worker + validator
Agent 1 (algorithms + scholarship)
   └─ the higher-layer algorithms (theme/argument/essay/semantic-alignment) that Agent 2 REUSES
```

**Layers live in the registry** (`data/corpus/registries/<layer>-registry.jsonl`, immutable/versioned);
**the controller advances them** by deterministic eligibility; **each layer has a layer-specific
validator**; **Agent 1's algorithms are the proposal engines Agent 2 wraps.**

---

## 1. THE GOLD-STANDARD MECHANISMS (verified, frozen, or witness — what we can trust)

### 1a. The proof ladder (L0 substrate floor) — Agent 2

| Mechanism | File | What it proves | Status |
|---|---|---|---|
| **P0 source proof** | `pipeline/verify_l0.py` | every source char accounted for, lossless, 0 unknown, spans exact | **63/63 FROZEN** (V2/V3 35/35 + V1 28/28), P-001 SUPPORTED |
| **P2 morphology witness** | `pipeline/verify_l0_p2.py` | Vidyut×Heritage: is our lemma licensed? | **frozen witness** (P-011): control 84–85%, CONFLICT-resolve 72%, real dispute ~9% |
| **P4 alignment witness** | `pipeline/l0_align.py` | L0↔L2 term-anchor alignment | **frozen witness** (P-013): recall .93 / prec .89 / abstain 1.0 |
| **RAW-L0 (MODE_B)** | `pipeline/raw_l0.py` | raw Sanskrit → canonical L0, deterministic, P0-lossless | ✅ real (Vidyut + P0, no model for the floor) |
| **L0 validator** | `pipeline/validate_l0_spec.py` | schema + P0 + abstraction-honesty; gloss NOT a commit gate | ✅ real (accepts the real IPVV exemplars, 100%) |

### 1b. The autonomous controller + registry (the state machine) — Agent 2

| Mechanism | File | What it does |
|---|---|---|
| **Autonomy controller** | `pipeline/autonomy.py` | ONE deterministic controller: flock, eligibility DAG, bounded batches, dispatch layer handler, validate, COMMIT/REJECT, run reports, idempotency, supersession. `LAYER_HANDLERS` = L0/L1L2/L1/L2/L200/C1/THEME/ESSAY/EDUCATION. |
| **Object registry** | `pipeline/object_registry.py` | immutable per-layer registry; three-state ladder (GENERATED/ENGINEERING_VALIDATED/SPECIALIST_REVIEWED); input-hash idempotency; supersession + cascading stale |
| **Model adapters** | `pipeline/model_adapter.py`, `pipeline/model.py` | Direct (~2s) + Hermes (`hermes -z`) backends; strict batch binding, fail-closed, process-group kill |

### 1c. The per-layer workers + validators (the factory) — Agent 2, wrapping Agent 1 where applicable

| Layer | Worker (pipeline/) | Validator (layer-specific) | Reuses Agent 1? |
|---|---|---|---|
| L0 | `l0_worker.py` + `raw_l0.py` | `validate_l0_spec` (P0 + schema + abstention) | — |
| L1/L2 | `l1_l2_worker.py` + `l1_l2_translate.py` | L1/L2 semantic-fidelity (content ⊆ upstream + supplies; provenance) | — |
| L200 | `l200_worker.py` | Task-2 fidelity (8 sections, MT/IA split, derivation map) | — |
| C1 | `c1_worker.py` | C1-SPEC §17 (passage-local, concise, no essay lexicon) | — |
| THEME | `theme_worker.py` | members resolve, strength+role, boundary, MACHINE_PROPOSED | **yes** — `patala_ml.cluster` |
| ESSAY | `essay_worker.py` | SentenceEvidenceAudit (every sentence licensed) | **yes** — `patala_ml.essay`/`essayverify` |
| EDUCATION | `education_worker.py` | derived-from-essay, concise, no overreach | — |

### 1d. Agent 1's algorithm gold (the proposal engines Agent 2 reuses / aligns with)

| Mechanism | File | Status |
|---|---|---|
| **Semantic alignment** | `machinelearning/research/patala_ml/semantic_alignment.py` | align(A,B) in 3 spaces (sanskrit/l2/c1), 6 labels + abstention. **Baseline falsified 0/8** (generic encoder fails on Sanskrit) — needs a Sanskrit-aware encoder. **SHARED with Agent 2's L0-semantic-equivalence proposal — the one duplication hotspot.** |
| **Theme clustering** | `patala_ml/cluster.py`, `kcore.py`, `theme_discovery.py` | hybrid graph + Louvain/k-core; 63/63 coverage; MACHINE_PROPOSED, no ACCEPTED theme yet |
| **Argument gold** | `patala_ml/gold*.py`, `goldchain.py`, `vertical.py` | ARG-GOLD-001..005 (CANDIDATE); vertical object (ARG-001 G-TC2) frozen, reference-resolution EXACT |
| **Essay/SentenceEvidenceAudit** | `patala_ml/essayverify.py` | independent adversarial verifier; 6 laundering/paraphrase mutation classes caught |
| **Nyāya gate** | `patala_ml/nyayagate.py` | 5-hetvābhāsa gate: detection 0.80 / FP 0.00 / abstain 0.50. FROZEN. |

---

## 2. THE FULL DATA FLOW (as implemented)

### 2a. The canonical layer pipeline (through the controller)

```
                      ┌──────────────────────────────────────────────┐
                      │  autonomy.py  (ONE deterministic controller)   │
                      │  flock · eligibility · batch · validate · commit│
                      └───────┬──────────────────────────────┬────────┘
                              │ advances, in order          │ layer-specific
                              ▼                             ▼
   SOURCE ──► T1 ──► L0 ──► [argument map] ──► L2 ──► L200 ──► C1 ──► THEME ──► ESSAY ──► EDUCATION
     │          │      │         │             │       │        │        │          │          │
     │          │      │         │             │       │        │        │          │          │
     │          │   raw_l0.py    │          l1_l2   l200_    c1_      theme_    essay_    education_
     │          │   l0_worker    │          _worker  worker  worker   worker    worker    worker
     │          │                │          (L1L2)                       (wraps    (wraps
     │          │                │                                     Agent1)   Agent1)
     ▼          ▼                ▼
  registry  registry          registry      ── each layer commits an immutable, versioned,
  SOURCE     T1                L0→L2→L200→C1    provenance-bound object to its registry
```

### 2b. What actually lives in the registry (committed objects, verified 2026-08-13)

```
SOURCE   981 · L0   790 · L1   5 · L2   3 · L200   9 · C1   3 · THEME   1 · ESSAY   0 · EDUCATION   0
```
So the pipeline is **populated and committed through THEME**; ESSAY/EDUCATION workers exist + test but
have not yet committed real objects on the current corpus subset.

### 2c. The two sides of the graph (Agent 1's architecture)

```
PRIMARY-TEXT SIDE                     SCHOLARSHIP SIDE
SOURCE → L0/L1 → L2                   Publication → Witness → Span
       → L200 → C1                        → SourceAssertion
                \                     /
              Proposition ↔ CorroborationEvent ↔ SourceAssertion
```
The generic source substrate sits under/alongside the Sanskrit L0/L200 stack. Modern English scholarship
is NOT forced through L0/L1/L2/L200.

### 2d. The live production run (separate from the validated vertical)

```
auto_translate_raw.py (detached, watchdog-cron)  →  batch_translate.py  →  model.chat → hermes -z
   → data/corpus/downloads/translations/<work>.jsonl   (MACHINE_PROPOSED English, 73 works, idempotent)
```
This is the **live RAW→English translation runner** (currently translating the RAW_SANSKRIT queue). It is
a *different deliverable* from the canonical validated vertical — it produces MACHINE_PROPOSED English
only, NOT the validated L0→…→C1 objects.

---

## 3. THE HONEST BOUNDARY (what is PROVEN vs NOT)

**PROVEN / FROZEN (gold-standard, trustworthy):**
- P0 lossless L0 floor (63/63) · P2 morphology witness · P4 alignment witness · RAW-L0 determinism +
  losslessness · the controller/registry mechanics (idempotency, supersession, fail-closed)
- The vertical provenance chain L0→L1→L2→L200→C1 (mechanical proof PASS)

**WIRED but NOT semantically proven:**
- L200 (MT-precision ~0.20 known, now mitigated by default-IGNORE classifier but unmeasured vs DEV)
- C1 (live comparison vs exemplar pending)
- THEME / ESSAY / EDUCATION (structural validators only; real semantic gates = the ML contracts)

**NOT STARTED / NOT ACHIEVED:**
- CP9 full unattended SOURCE→C1 vertical (terminal factory proof) — NOT achieved
- Semantic correctness vs human gold — NOT yet validated anywhere in the vertical

---

## 4. THE ONE DUPLICATION HOTSPOT (must keep aligned)

**Semantic equivalence / semantic alignment** is the only area where the two lanes genuinely overlap:
- Agent 1's `semantic_alignment.py` (already built, falsified baseline, needs Sanskrit-aware encoder)
- Agent 2's `docs/ML-L0-SEMANTIC-EQUIVALENCE-PROPOSAL.md` + `docs/ML-VERIFIABLE-LAYER-CONTRACTS.md`
  (the per-layer Tier-B semantic scorers)

**Rule: the CP1 L0/T1 contract and every per-layer Tier-B semantic scorer must be built ON TOP of
Agent 1's `semantic_alignment.py`** (extend/benchmark it), NOT as a parallel module. This is the shared
mechanism both lanes must treat as one.

**THE CLEAN ROLE SPLIT (2026-08-13):** `AGENT 2 = MAKE THE FACTORY RUN` · `AGENT 1 = PROVE THE FACTORY
DESERVES TRUST`.
- **Agent 2 = the Autonomous Translation Factory**: controller, registries, queues, workers, model
  adapters, batching, retries, crash/resume, idempotency, provenance, schemas, deterministic validation,
  staleness, pipeline certificates, running the corpus. Its gate per layer is **production only**
  (canonical shape + provenance + safe unattended run → MACHINE_PROPOSED). Sequence A2-CP1..A2-CP7,
  **stop at C1** for the first milestone. Does NOT do ML research / benchmark architecture / scholar
  corpus / model comparison / external-tool experiments.
- **Agent 1 = Verification + Evals + Scholar Evidence**: Inspect AI / Pāṭala-Evals (LayerContract,
  gold/DEV/TEST, metamorphic tests, external baselines, false-certainty, calibration) + the S0
  scholar-corpus (SourceAssertion/CorroborationEvent). **Evaluates Agent 2** independently, one layer
  behind. Owns `source-evidence/evals/` + `benchmarks/v0/` + the ML methodology.
- **The seam = the frozen export contract** (`EVAL-CONTRACT-L200-EXPORT.md`): Agent 2 writes an immutable
  MACHINE_PROPOSED candidate bundle; Agent 1 consumes read-only and returns failure taxonomies +
  improvement recommendations. Agent 1 does NOT gate Agent 2's development (production ≠ epistemic
  maturity — the two status axes move independently).
- **VERIFICATION-PLANE NOTE:** the Inspect evaluation plane is Agent 1's (already built in
  `source-evidence/evals/`). Agent 2 does NOT build a parallel Inspect/PATALA-EVALS plane. The two-plane
  northstar (`docs/ml/LAYER-TOOLS-INTEGRATION-NORTHSTAR.md`) is the shared *methodology*; it RUNS in
  Agent 1's Inspect plane.

---

## 5. KEY FILE MAP (for tracking)

| Concern | Files |
|---|---|
| Canonical layer order + file types | `handover/agent-2-integration/CANONICAL-LAYER-STACK.md` |
| Per-layer done-correct contracts (Tier A deterministic + Tier B ML) | `docs/ML-VERIFIABLE-LAYER-CONTRACTS.md` |
| L0 semantic-equivalence proposal (CP1) | `docs/ML-L0-SEMANTIC-EQUIVALENCE-PROPOSAL.md` |
| Controller + registry | `pipeline/autonomy.py`, `pipeline/object_registry.py` |
| L0 proof ladder | `pipeline/verify_l0.py`, `verify_l0_p2.py`, `l0_align.py`, `raw_l0.py`, `validate_l0_spec.py` |
| Layer workers | `pipeline/{l0,l1_l2,l200,c1,theme,essay,education}_worker.py`, `l1_l2_translate.py`, `generative_worker.py` |
| Agent 1 algorithms | `machinelearning/research/patala_ml/{semantic_alignment,cluster,kcore,theme_discovery,essay,essayverify,gold*}.py` |
| Live RAW→English runner | `pipeline/auto_translate_raw.py`, `watchdog_auto_translate.sh`, `batch_translate.py` |
| Mission ladder (CP0–CP10) | `handover/agent-2-integration/MISSION-AUTONOMOUS-FACTORY.md` |
| Agent 1 handover | `handover/agent-1-ml/HANDOVER-2026-08-13.md` + `NEXT-STEPS.md` |

---

*Keep this doc updated as capabilities cross gates. It is the tracking view — the canonical stack doc
holds the layer order, the contracts doc holds the done-correct checks, this doc holds the high-scale
"what exists + how it flows."*
