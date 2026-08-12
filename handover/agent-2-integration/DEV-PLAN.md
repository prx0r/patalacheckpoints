# AGENT 2 — DEV PLAN (canonical, honest state)

*2026-08-12. The single authoritative execution plan for the **corpus compiler + integrity lane**. Reflects
the honest state after the RAW-L0 factory build. Governed by `machinelearning/_ACTIVE/AGENTS-DOCTRINE.md` +
`CLAIMS.md` + `handover/CHECKPOINTS.md` + `handover/agent-2-integration/CHECKPOINTS-INTEGRATION.md`. Read
those first.*

> **The governing rule:** *Nothing is "real" because code exists. It becomes real only when independent gold
> + blind prediction + metric + human adjudication show it does what its name claims.* A tested schema ≠ a
> result. The checkpoint-test applies to every build: **name the checkpoint it advances · the scholarly
> object it makes more trustworthy · the benchmark/proof of success. If it can't answer all three, don't
> build it.**

---

## 0. THE HONEST STATE (what's real vs. hollow — from CLAIMS.md)

> **Where we are (2026-08-12):** the CP1 source→L0 floor is **63/63 lossless and frozen**, and the
> **RAW-L0 factory core** (raw Sanskrit → canonical L0, P0-validated) is built and proven deterministic —
> no Hermes required. The blocker is now **the gloss/generative layer + a reliable model transport** (the
> remaining gap before L0 is complete), then the **Sanskrit-only replay benchmark**.

| Asset | Status | Real? |
|---|---|---|
| **P0 source floor** (`verify_l0.py`) | **63/63 LOSSLESS** (V2/V3 35/35 + V1 legacy 28/28), frozen | ✅ REAL (P-001 SUPPORTED) |
| **P2 morphology witness** (`verify_l0_p2.py` + ensemble) | Vidyut×Heritage calibrated: control 84–85%, CONFLICT-resolve 72%, double-conflict ~9% | ✅ REAL (P-011 SUPPORTED, frozen witness; human blind review pending) |
| **P3 lexical ranker** (`ranker.py`) | **REJECTED** — 0.76 < embedding baseline 0.81, 100% false-certainty | ❌ NOT_ESTABLISHED (P-012); the 0.81 embedding is the floor to beat |
| **P4 alignment** (`l0_align.py`) | L0↔L2 term-anchor: recall 0.93 / prec 0.89 / abstain 1.0 + Vidyut witness 0.81 | ✅ REAL (P-013 SUPPORTED_MACHINE_WITNESS, FROZEN per adequacy doctrine) |
| **Corpus state machine** (`corpus_state.py`) | per-work state from disk truth + `NEXT_VALID_ACTION` + ledger (45 works) | ✅ REAL (the Agent 3 control plane) |
| **RAW-L0 factory core** (`raw_l0.py`) | raw Sanskrit → canonical L0 (IPVV schema), Vidyut + P0; lemma=null → AMBIGUOUS | ✅ REAL (deterministic; **gloss layer gap**) |
| **Agent 3 batch + queue** (`agent3_batch.py`, `agent3_queue.py`) | 21 prioritized targets (Krama first) + 39 leads; processes next passage, resume-after-failure | ✅ REAL (mechanics) |
| **Versioned L0 registry** (`l0_registry.py`) | immutable versions, commit, mark_reviewed | ✅ REAL (Kramasadbhāva v1–v4) |
| **Executable-corrections review engine** (`review_engine.py`) | append-only ReviewEvent → reducer → ImpactReport; PROPOSE not ACCEPT; Phase 3A+3D | ✅ REAL (15/15 tests — the moat) |

**The single highest-value real build (now):** wire a reliable **gloss/model transport** for `literal_gloss`
(the top gap), then run the **Sanskrit-only replay benchmark** against IPVV gold (the Pāṭala-Evals embryo).

---

## 1. THE PRIORITY SEQUENCE (the RAW-L0 factory, per `handover/hermes/AUTOTRANSLATE-NORTHSTAR.md`)

The autonomous factory is the headline; validation is the substrate. In order:

```
1. ✅ GLOSS/MODEL TRANSPORT   DONE (2026-08-12) — Hermes (-z) is functional; the gloss is generated per
                           token through pipeline/model.py, anchored to the deterministic RAW-L0
                           segmentation, and populated into literal_gloss. Verified on a real
                           Kramasadbhāva verse (P0 PASS, 0 unknown, 4/4 non-empty glosses). Also fixed
                           the gloss-map shape inconsistency (flat vs nested both accepted).
2. ▶ SANSKRIT-ONLY REPLAY   hide IPVV gold English, run RAW-L0, compare vs gold → measures segmentation/
                           lemma/morphology/gloss/abstention/false-certainty (the Pāṭala-Evals embryo)
3. INGEST PRIMARY TEXTS    the not-yet-ingested texts from docs/corpus/SANSKRITREE-IMPORT-MANIFEST.md
                           → data/corpus/passages/
4. CROSS-WORK L0           Kramasadbhāva first (RAW_SANSKRIT, priority #1 in the queue) → GENERATE_L0 →
                           VERIFIED P0 → MACHINE_PROPOSED → GENERATE_TRANSLATION (unblocks the raw works)
```

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
