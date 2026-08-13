# AGENT 2 — DEV PLAN (canonical, honest state)

*2026-08-13. The single authoritative execution plan for the **corpus compiler + integrity lane**. Reflects
the honest state after the full autonomous stack was wired. Governed by `machinelearning/_ACTIVE/AGENTS-DOCTRINE.md` +
`CLAIMS.md` + `handover/CHECKPOINTS.md` + `handover/agent-2-integration/CHECKPOINTS-INTEGRATION.md`. Read
those first.*

> **THE NEW NORTHSTAR (2026-08-13):** Agent 1 solved the *algorithms* of the higher layers (theme
> clustering, argument, essay, semantic alignment). Agent 2's job is now to wrap each layer in the
> **autonomous controller flow** — producing deterministic, provenance-bound, layer-specific-validated
> objects through the registry — until the whole canonical stack is a **single autonomous pipeline**:
> ```
> SOURCE → L0/L1 → L2 → L200 → C1 → THEME → ESSAY → EDUCATION
> ```
> **Hard rule: work LAYER BY LAYER** — each layer according to its canonical spec + source files
> (`translations/_stack/ipvv/specs/*`, the L200 8-section spec, the C1-SPEC, the argument maps
> `pilot_*_ARGUMENT_MAP.md`). Perfect L0 → commit → L1/L2 → commit → L200 → commit → C1 → commit →
> THEME → ESSAY → EDUCATION. Do NOT skip ahead; do NOT build a layer whose upstream is not committed.
> **CP1 = a machine-learning-verified L0 (or T1/L1/R1 reading)** — the foundation everything below builds on.

> **The governing rule:** *Nothing is "real" because code exists. It becomes real only when independent gold
> + blind prediction + metric + human adjudication show it does what its name claims.* A tested schema ≠ a
> result. The checkpoint-test applies to every build: **name the checkpoint it advances · the scholarly
> object it makes more trustworthy · the benchmark/proof of success. If it can't answer all three, don't
> build it.**

---

## 0. THE HONEST STATE (what's real vs. hollow — from CLAIMS.md)

> **Where we are (2026-08-13):** the **full autonomous stack is WIRED** — every layer
> (L0/L1/L2/L200/C1/THEME/ESSAY/EDUCATION) has a controller handler producing its canonical file shape +
> a layer-specific deterministic validator. The frontier is **CP1 = a machine-learning-verified L0/T1/L1/R1
> reading** — proving semantic equivalence against the IPVV exemplar gold (the ML harness), which then
> becomes the reusable substrate for every downstream layer's own proof.

| Asset | Status | Real? |
|---|---|---|
| **Full autonomous stack wired** (`autonomy.py`) | L0/L1/L2/L200/C1/THEME/ESSAY/EDUCATION all have controller handlers + layer-specific validators; deterministic vertical proof L0→…→C1 PASS | ✅ REAL (build 2026-08-13) |
| **L0 worker** (`l0_worker.py` + `raw_l0.py`) | deterministic RAW-L0 (MODE_B) schema-conformant + P0-lossless; validator accepts real IPVV exemplars | ✅ REAL |
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

**The single highest-value real build (now):** **CP1 = the machine-learning-verified L0/T1/L1/R1 reading**
— run the semantic-equivalence harness (`docs/ML-L0-SEMANTIC-EQUIVALENCE-PROPOSAL.md`) against the IPVV
exemplar gold, iterate our RAW-L0 toward it, and emit the mechanical proof. This is the foundation-proof
for the whole stack.

---

## 1. THE PRIORITY SEQUENCE (the singular autonomous stack, layer by layer)

**THE NORTHSTAR — work layer by layer, each layer's worker + validator against its canonical spec + source
files.** The algorithms of the higher layers already exist (Agent 1); we wrap each in the autonomous flow.

```
0. ✅ STACK WIRED (2026-08-13): L0/L1/L2/L200/C1/THEME/ESSAY/EDUCATION all have controller handlers
   + layer-specific validators; test_theme_essay_education.py + test_workers.py ALL PASS.
1. ▶ CP1 = ML-VERIFIED L0/T1/L1/R1 READING  (the foundation proof)
   run the semantic-equivalence harness vs the IPVV exemplar gold:
   prove our RAW-L0 is (a) schema-isomorphic, (b) validator-equivalent, (c) P0-lossless, (d) semantically
   equivalent to the exemplar gloss (the ML part). Emit the mechanical proof. This becomes the reusable
   eval substrate for every downstream layer's proof.
2. L1/L2 verified against a real passage (provenance + semantic-fidelity + live model path).
3. L200 constrained compiler measured against benchmarks/l200/dev.jsonl (CP5 DEV gate).
4. C1 live-model comparison vs the c1/read exemplars.
5. THEME/ESSAY/EDUCATION produced autonomously on a real corpus subset; each layer's validator gates.
6. FULL END-TO-END autonomous vertical proof: raw Sanskrit → SOURCE → L0 → L1 → L2 → L200 → C1 →
   THEME → ESSAY → EDUCATION, all through the controller, fail-closed, idempotent, provenance-bound.
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
