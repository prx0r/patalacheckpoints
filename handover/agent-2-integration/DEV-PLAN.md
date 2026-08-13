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

> **Where we are (2026-08-13, end of session):** **Era A (Factory Completion) is DONE.** All six canonical
> layers (T1/L0/ARGMAP/L2/L200/C1) are AUTONOMOUSLY_PRODUCIBLE and **verified against the REAL IPVV
> exemplars** (the `test_*_ipvv.py` suite). **Era B (Corpus Compiler) is DONE** — the DAG scheduler
> (A2-8/9), rate limiting (A2-10), durable append-only failure/retry queue (A2-11), progress dashboard
> (A2-12), and bulk certificate (A2-13) are built + tested, and the overnight loop is live.
> **Era C (Rebuild Engine) is STARTED** — supersession propagation + targeted regeneration
> (`factory_rebuild.py`) + the critical `object_registry.current()` fix.

| Asset | Status | Real? |
|---|---|---|
| **Controller shells** (`autonomy.py`) | all layers have handlers + layer-specific validators; T1 + ARGMAP wired | ✅ REAL |
| **T1 worker** (`t1_worker.py`) | canonical `[and]-GLOSS (IAST)`, verified vs IPVV gold, Agent-1 evaluated (gloss_accuracy 1.000) | ✅ REAL (A2-CP1) |
| **L0 worker** (`raw_l0.py`) | deterministic floor, verified vs IPVV l0 exemplar | ✅ REAL (A2-CP2) |
| **ARGMAP worker** (`argument_map_worker.py`) | lateral guide, verified vs pilot_V2O_ARGUMENT_MAP | ✅ REAL (A2-CP3) |
| **L2 worker** (`l1_l2_translate.py`) | readable prose, verified vs pilot_V2O_L2_read | ✅ REAL (A2-CP4) |
| **L200 worker** (`l200_worker.py`) | constrained compiler, verified vs l200/V2O audit | ✅ REAL (A2-CP5) |
| **C1 worker** (`c1_worker.py`) | commentary, verified vs c1/read/V2O | ✅ REAL (A2-CP6) |
| **DAG scheduler** (`factory_scheduler.py`) | all eligible (object,layer) jobs; free-draining L0; rate-limited model budget | ✅ REAL (A2-8/9/10,13a/b) |
| **Failure/retry queue** (`factory_batch.py`) | durable, append-only history, isolation, size-aware retry | ✅ REAL (A2-11,11b) |
| **Progress dashboard** (`factory_status.py`) | per-work operational view | ✅ REAL (A2-12) |
| **Bulk certificate** (`factory_certificate.py`) | passes/jobs/integrity/resume | ✅ REAL (A2-13) |
| **Rebuild engine** (`factory_rebuild.py`) | supersession propagation + targeted regeneration | ✅ REAL (Era C, A2-14/15/16) |
| **Overnight pack** (`start_overnight.sh`, `OVERNIGHT.md`) | one-command launcher + runbook | ✅ REAL |
| **THEME/ESSAY/EDUCATION** | wired (structural) — wait for Agent 1 contracts | ⚠️ deferred |
| **P0/P2/P4 + review engine** | frozen proofs + the moat | ✅ REAL |

**The single highest-value real build (now):** **Era C continuation** — the DependencyImpactReport
(mechanical: changed object → descendants invalidated → rebuilt) + the ReviewBundle export
(SOURCE/T1/L0/ARGMAP/L2/L200/C1 + dependencies + versions + OPEN items) for Agent 1 / the scholar
review. **Overnight operation is ready:** `bash pipeline/start_overnight.sh start` (see
`pipeline/OVERNIGHT.md`).

---

## 1. THE PRIORITY SEQUENCE — AGENT 2'S AUTONOMOUS FACTORY (A2-CP1..A2-CP7)

**THE ROLE SPLIT (2026-08-13):** `AGENT 2 = MAKE THE FACTORY RUN` · `AGENT 1 = PROVE THE FACTORY DESERVES
TRUST`. Agent 2 builds the shortest working autonomous factory through **C1**; Agent 1 (parallel, one layer
behind) builds the evals. **Agent 2's gate per layer is PRODUCTION only** — canonical shape + provenance/
integrity + safe unattended production → `MACHINE_PROPOSED`, move on. Do NOT gate on Agent-1's benchmark.

```
A2-CP1  SOURCE → T1      ✅ DONE (v1, v100 committed; Agent 1 evaluated)
A2-CP2  T1 → L0          ✅ DONE (verified vs IPVV l0 exemplar)
A2-CP3  → argument map   ✅ DONE (verified vs pilot_V2O_ARGUMENT_MAP)
A2-CP4  → L2             ✅ DONE (verified vs pilot_V2O_L2_read)
A2-CP5  → L200           ✅ DONE (verified vs l200/V2O audit)
A2-CP6  → C1             ✅ DONE (verified vs c1/read/V2O)
A2-CP7  whole-work unattended run   🔶 Era A done; Era B scales to the whole corpus
```

**Era A (Factory Completion) is DONE.** All six layers AUTONOMOUSLY_PRODUCIBLE + IPVV-verified.

**Era B (Corpus Compiler) — DONE:**
```
A2-8   backlog scheduler       ✅ DONE (DAG scheduler, verified live)
A2-9   multi-work execution    ✅ DONE (all eligible jobs across the graph)
A2-10  resource/rate limiting  ✅ DONE (model-call budget + throttle + size-aware timeout)
A2-11  durable failure/retry queues   ✅ DONE (append-only history, isolation)
A2-12  corpus progress dashboard      ✅ DONE (factory_status)
A2-13  unattended bulk translation    ✅ DONE (factory_loop + certificate + overnight pack)
```
**Era C (Living rebuild engine) — STARTED:**
```
A2-14/15/16  supersession propagation + dependency invalidation + targeted regeneration  ✅ DONE (factory_rebuild)
A2-18  DependencyImpactReport   ▶ NEXT (mechanical: changed -> invalidated -> rebuilt)
A2-19  ReviewBundle export      ▶ NEXT (SOURCE/T1/L0/ARGMAP/L2/L200/C1 + deps + versions + OPEN)
```

**Overnight operation:** `bash pipeline/start_overnight.sh start` (see `pipeline/OVERNIGHT.md`).

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
