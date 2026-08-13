# AGENT 2 — DEV PLAN (canonical, honest state)

*2026-08-13. The single authoritative execution plan for the **corpus compiler + integrity lane**. Reflects
the honest state after the controller shells were built. Governed by `machinelearning/_ACTIVE/AGENTS-DOCTRINE.md` +
`CLAIMS.md` + `handover/CHECKPOINTS.md` + `handover/agent-2-integration/CHECKPOINTS-INTEGRATION.md`. Read
those first.*

> **THE NORTHSTAR (2026-08-13, two-plane):** Agent 1 solved the *algorithms* of the higher layers (theme
> clustering, argument, essay, semantic alignment). Agent 2 wraps each layer in the **autonomous controller
> flow** — producing deterministic, provenance-bound, layer-specific-validated objects — until the whole
> canonical stack is a **single autonomous compiler** with a **separate verification plane**:
> ```
> PRODUCTION COMPILER                          VERIFICATION PLANE
> SOURCE→T1→L0→ARGMAP→L2→L200→C1→              Inspect AI
>   THEME→ESSAY→EDUCATION                       ├─ LayerContract (deterministic+semantic+metamorphic)
>        │ every object                         ├─ external ML witnesses (RefChecker/AlignScore/GlossLM)
>        ▼                                      ├─ metamorphic tests (from our historical failures)
>   immutable registry                          └─ calibrated abstention + certificates
> ```
> **External ML methods TEST Pāṭala; they do not get to define Pāṭala truth.** The verification plane lives
> in `evals/` (research/eval env), NOT in the translation runtime. Full design:
> **`docs/ml/LAYER-TOOLS-INTEGRATION-NORTHSTAR.md`** (two-plane + LayerContract + PATALA-EVALS build order),
> grounded in `docs/ml/MACHINE-PROOF-CONTRACTS.md` (per-layer contracts + G0–G5 + the 5-gate checkpoint
> ladder) + `docs/ml/LAYER-TOOLS-SURVEY.md` (the tool survey: IGT/GlossLM, ByT5-Sanskrit, RefChecker,
> FActScore, AlignScore, metamorphic, conformal, Inspect).
> **ROLE DIVERGENCE (IMPORTANT): the verification plane is AGENT 1's lane.** Agent 1 has ALREADY built the
> Inspect evaluation plane in `source-evidence/evals/` (Inspect L200 + arg-laundry tasks + the frozen
> `EVAL-CONTRACT.md` + the `EVAL-CONTRACT-L200-EXPORT.md` lane-safe export contract; `inspect_ai` is
> installed in Agent 1's ML venv). **Agent 2 does NOT build a parallel `PATALA-EVALS` / Inspect plane.**
> Agent 2's job: build the production-compiler layers (T1/L0/L2/L200/C1/theme/essay/education workers +
> per-layer validators + the controller), then **EXPORT candidate bundles to Agent 1's evals plane** per the
> frozen export contract (Agent 1 consumes read-only; Agent 1 owns how Pāṭala is *tested*). This is the
> doctrine: external ML methods (Agent 1) test Pāṭala (Agent 2); they do not define Pāṭala truth. The
> LayerContract / G0–G5 / metamorphic / certificate schema from the northstar docs are the shared
> *methodology*; Agent 1's Inspect plane is where they run.
> **THE CANONICAL LAYER STACK IS LOCKED: see `handover/agent-2-integration/CANONICAL-LAYER-STACK.md`**
> (verified against the actual IPVV files — do not reorder/rename without updating that file). The order:
> ```
> SOURCE → T1 → L0 → [argument map] → L2 → L200 → C1 → THEME → ESSAY → EDUCATION
> ```
> **What each layer actually IS (verified):** `T1` = the **transliteral word-gloss** markdown (01_t1);
> `L0` = **structured token records extracted from T1** (`t1_extract.py → l0/*.l0.jsonl`, same content,
> machine form); the **argument map** (`pilot_*_ARGUMENT_MAP.md`) is a **lateral guide** that unlocks the
> readable layer; `L2` = the **readable whole-passage prose** (derived AFTER the transliteral layer, guided
> by the argument map); `L200` = the audit of how L2 was derived; `C1` = commentary.
> **Hard rule: work LAYER BY LAYER** — each layer according to its canonical spec + source files
> (`translations/_stack/ipvv/specs/*`, the L200 8-section spec, the C1-SPEC, the argument maps).
> **CP1 = SOURCE → T1** (the transliteral word-gloss producer + its semantic contract) — the first
> genuinely-difficult AI layer and the current frontier. Do NOT skip ahead; do NOT build a layer whose
> upstream is not committed.

> **The governing rule:** *Nothing is "real" because code exists. It becomes real only when independent gold
> + blind prediction + metric + human adjudication show it does what its name claims.* A tested schema ≠ a
> result. The checkpoint-test applies to every build: **name the checkpoint it advances · the scholarly
> object it makes more trustworthy · the benchmark/proof of success. If it can't answer all three, don't
> build it.**

---

## 0. THE HONEST STATE (what's real vs. hollow — from CLAIMS.md)

> **Where we are (2026-08-13):** the **controller shells exist for several downstream layers**, but the
> canonical T1 worker is the current **first unsatisfied layer contract** (per `docs/ml/MACHINE-PROOF-CONTRACTS.md`
> §20). L0/L1/L2/L200/C1 have controller handlers + layer-specific validators (L0→…→C1 mechanical vertical
> PASS). THEME/ESSAY/EDUCATION are wired (structural validators). **T1 (the transliteral word-gloss producer)
> is NOT built** — and T1 is where the semantic/ML work belongs (the gloss, false-certainty, technical
> senses, abstention). The frontier is **CP1 = SOURCE → T1**: build the T1 producer, then its semantic
> contract (IGT/GlossLM + ByT5-Sanskrit + metamorphic mutations + Inspect, per `docs/ml/LAYER-TOOLS-SURVEY.md`).

| Asset | Status | Real? |
|---|---|---|
| **Controller shells** (`autonomy.py`) | L0/L1/L2/L200/C1 have real handlers + layer-specific validators; THEME/ESSAY/EDUCATION wired (structural); deterministic vertical proof L0→…→C1 PASS | ✅ REAL (build 2026-08-13) |
| **T1 worker (transliteral word-gloss)** | **NOT BUILT** — the first unsatisfied layer contract. This is CP1. | ❌ TO BUILD |
| **L0 worker** (`l0_worker.py` + `raw_l0.py`) | deterministic RAW-L0 (MODE_B) schema-conformant + P0-lossless; validator accepts real IPVV exemplars | ✅ REAL (but see note: L0 = deterministic round-trip of T1 per canonical stack, not the ML layer) |
| **L1/L2 workers** (`l1_l2_worker.py`, `l1_l2_translate.py`) | provenance continuity + semantic-fidelity validators; model path produces fluent prose | ✅ REAL |
| **L200 worker** (`l200_worker.py`) | constrained compiler (candidate→classifier, IGNORE default); 8-section audit; derivation map binds argmap+L0+source | ✅ REAL |
| **C1 worker** (`c1_worker.py`) | passage-local commentary per C1-SPEC; C1-SPEC §17 validator | ✅ REAL |
| **THEME worker** (`theme_worker.py`) | evidence-backed synthesis via Agent 1's hybrid clustering; members resolve, boundary, MACHINE_PROPOSED | ✅ REAL |
| **ESSAY worker** (`essay_worker.py`) | proof-carrying prose from THEME+C1; SentenceEvidenceAudit gate (fail-closed) | ✅ REAL |
| **EDUCATION worker** (`education_worker.py`) | distills essay; no overreach, derived-from-essay | ✅ REAL |
| **P0 source floor** (`verify_l0.py`) | **63/63 LOSSLESS** (V2/V3 35/35 + V1 legacy 28/28), frozen | ✅ REAL (P-001 SUPPORTED) |
| **P2 morphology witness** (`verify_l0_p2.py` + ensemble) | Vidyut×Heritage calibrated: control 84–85%, CONFLICT-resolve 72%, double-conflict ~9% | ✅ REAL (P-011 SUPPORTED, frozen witness) |
| **P4 alignment** (`l0_align.py`) | L0↔L2 term-anchor: recall 0.93 / prec 0.89 / abstain 1.0 | ✅ REAL (P-013 SUPPORTED_MACHINE_WITNESS, FROZEN) |
| **Executable-corrections review engine** (`review_engine.py`) | append-only ReviewEvent → reducer → ImpactReport | ✅ REAL (15/15 tests — the moat) |

**The single highest-value real build (now):** **A2-CP1 = SOURCE → T1** — the transliteral word-gloss
producer (the first unsatisfied layer). This is the factory's job. Note: the ML/semantic-equivalence
*evaluation* of T1 is **Agent 1's lane** (the Inspect/Pāṭala-Evals plane + `docs/ml/MACHINE-PROOF-CONTRACTS.md`
contracts) — Agent 2 builds the producer + deterministic validation, Agent 1 evaluates it. Agent 2 does
NOT need a passed gold benchmark to move to the next layer (production ≠ epistemic maturity).

---

## 1. THE PRIORITY SEQUENCE — AGENT 2'S AUTONOMOUS FACTORY (A2-CP1..A2-CP7)

**THE ROLE SPLIT (2026-08-13):** `AGENT 2 = MAKE THE FACTORY RUN` · `AGENT 1 = PROVE THE FACTORY DESERVES
TRUST`. Agent 2 builds the shortest working autonomous factory through **C1**; Agent 1 (parallel, one layer
behind) builds the evals. **Agent 2's gate per layer is PRODUCTION only** — canonical shape + provenance/
integrity + safe unattended production → `MACHINE_PROPOSED`, move on. Do NOT gate on Agent-1's benchmark.

```
A2-CP1  SOURCE → T1      the transliteral word-gloss producer  (CURRENT FRONTIER)
A2-CP2  T1 → L0          deterministic structured encode of T1 (round-trip/isomorphism)
A2-CP3  → argument map   the passage's argument structure
A2-CP4  → L2             readable translation
A2-CP5  → L200           constrained audit (MT/IA split)
A2-CP6  → C1             passage-local commentary
A2-CP7  whole-work unattended run through C1   ← FIRST FACTORY MILESTONE (stop here)
```

**Do NOT start THEME/ESSAY/EDUCATION yet** — they wait until the factory through C1 is proven. Each
layer's worker + deterministic validator against its canonical spec + source files
(`translations/_stack/ipvv/specs/*`, the L200 8-section spec, the C1-SPEC, the argument maps). Do NOT do
ML research, benchmark architecture, scholar-corpus integration, model comparison, or external-tool
experiments — that is Agent 1's verification/evidence lane.

**Agent 1's parallel track (for reference — NOT Agent 2's work):**
```
A1:  T1-EVAL ── ARGMAP-EVAL ── L2-EVAL ── ...  (Inspect AI / Pāṭala-Evals, one layer behind A2)
     + scholar-evidence corpus continuously (SourceAssertion/CorroborationEvent)
```
Agent 2 exports MACHINE_PROPOSED candidate bundles to Agent 1 per the frozen export contract; Agent 1
returns failure taxonomies + improvement recommendations.

### The factory certificate (the threshold before "set it loose")
```
P0 coverage              100%      · bad source spans     0      · unknown chars    0
segmentation             measured  · lemma selection      measured  · morphology     measured
literal gloss            human-rated  · false certainty   below threshold (the killer metric)
abstention precision     measured  · cost / 1k tokens     known  · review minutes / 1k tokens  known
hard failure rate        known
```

**The unit economics Agent 3 optimizes is review burden, not just token cost.**

---

## 2. THE BUILD ORDER (Builds 1–6, from the northstar)

| Build | What | Status |
|---|---|---|
| **1. `raw_l0.py`** | raw Sanskrit → canonical L0 JSONL (Vidyut + Heritage + Hermes/A3); no downstream translation | ✅ DONE (deterministic core + gloss transport) |
| **2. RAW-L0 audit** | extend `verify_l0.py`: P0 lossless + P1 segmentation + P2 morphology + P3 gloss + P4 alignment | 🔶 P0 done; P1–P5 extensions partial |
| **3. IPVV Sanskrit-only replay** | hide English, regenerate L0, compare vs gold → immutable `BenchmarkRun` | ▶ **NEXT** (gloss transport now DONE) |
| **4. human review 50–100 difficult cases** | sandhi / bahuvrīhi-tatpuruṣa / verbal morphology / technical terms; every correction = benchmark data | ⬜ (after 3) |
| **5. Kramasadbhāva first cross-work run** | `RAW_SANSKRIT → GENERATE_L0 → VERIFIED P0 → MACHINE_PROPOSED → GENERATE_TRANSLATION` | ⬜ (after 3–4) |
| **6. batch mode** | passages/chunks independently, bounded retries, halt-on-failure (never whole works) | ⬜ LAST |

---

## 3. THE QUEUE + VERSIONED L0 (already built — use it)

```
python3 pipeline/agent3_queue.py --registry   # 21 prioritized targets (Krama packet first)
python3 pipeline/agent3_queue.py --leads      # 39 tracked leads (registers I-III)
python3 pipeline/audit_translation_pipeline.py # 40 existing T1/R1/T2/R3/C1 works (the easy wins)
python3 pipeline/l0_registry.py               # versioned L0 (immutable, commit, mark_reviewed)
python3 pipeline/corpus_state.py              # regenerate the 45-work ledger
```

---

## 4. THE GOLDMINE (read before translating/acquiring)

- `docs/corpus/TARGETS-INDEX.md` — the master index (DB + the two goldmine docs).
- `docs/corpus/SANSKRITREE-IMPORT-MANIFEST.md` — the full sanskritree audit + where things import.
- `docs/corpus/canonical_reference_map.md` — taxonomy, ingestion waves, the **semantic-shift glossary**
  (the fix for cross-work term misreading).
- `docs/corpus/markguidance.md` — the Recognition Enquiry (for Agent 1).
- `data/corpus/targets/` — the compiled DB (sources/targets/leads/anchors/index).

---

## 5. GUARDRAILS (do not violate)

1. **Output `PhilologicalProof` objects + canonical L0 records, not logs.**
2. **Every proof dimension carries an honest status; no collapsed confidence number.**
3. **`extraction_coverage: OPEN` ≠ `lexical_sense: OPEN` — never conflate.**
4. **A wrong translation is worse than none.** Validation is the gate — never let the factory outrun the
   validator (P0 lossless + false-certainty + abstention + chunk review).
5. **L0 is immutable + versioned** — a fix emits a new version (`l0_registry`), never edit in place.
6. **Every ID must resolve** — real `pp:` / passage IDs, never fuzzy.
7. **Do NOT touch `benchmarks/v0/` or `machinelearning/research/patala_ml/`** (Agent 1's lane).
8. **Do NOT import the Lean/Pantograph code as a working capability** (aspirational) or the mystical
   `syntheses/*` / `truth/` dirs (noise).
9. **Do NOT build more review UX (3E/3F) until a real reviewer is ready.**
10. **Update `CLAIMS.md` + the handover honestly as each capability crosses its gate.**

---

## 6. THE ONE-SENTENCE CARRY-FORWARD

**Agent 2 owns the CP1 source→L0 floor (63/63 lossless, frozen) + the RAW-L0 factory core + the prioritized
21-target queue + the versioned L0 registry + the executable-corrections review engine; the next build is
(1) a reliable gloss/model transport, (2) the Sanskrit-only replay benchmark against IPVV gold (the
Pāṭala-Evals embryo), and (3) ingesting the not-yet-ingested primary texts — holding the hard line that a
wrong translation is worse than none, L0 is immutable/versioned, proof dimensions stay separate, and
validation is the gate.**
