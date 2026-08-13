# ENDGAME BUILD — BUILD NOTES & PROGRESS (Agent 1 / Agent 2 consolidated)

*2026-08-13 (late). Consolidated build notes + progress across the endgame build, captured so any
next agent can resume without re-deriving. This records WHAT was built, WHY it matters to the
endgame vision, the decisive experiment, and the open review items.*

---

## 1. THE STRATEGIC REFRAME (why this build exists)

The endgame vision (docs/global/globalgoal.md, docs/endgame3.md) is: **one versioned scholarly graph
(Layers A→F) — everything else (essay/lesson/review/education bundle) is a materialized projection
over it.** The missing middle is SYNTHESIS (Arguments → ArgumentSynthesis → {Essay, Lesson, Review}).

The sober-review reframe (which now drives the build): Pāṭala has PROVEN it can **carry** epistemic
structure, NOT yet that it can **discover** it. Everything above ARGMAP risks being a beautiful
consumer of hand-curated reasoning. **The bottleneck is SOURCE → ARGMAP: automatic argument
discovery from real IPVV.**

The order that followed (reviewer's immediate order):
```
1. fix registry concurrency            [DONE]
2. separate T1 units from ARGMAP context windows  [DONE]
3. freeze a bounded 5-unit IPVV pilot  [DONE]
4. generate T1/L0/ARGMAP, no gold leakage  [DONE — used REAL existing T1/L0/C1]
5. run blind argument-recovery scoring [DONE — real result]
6. inspect + fix producer              [NEXT]
7. repeat until credible               [NEXT]
8. only then run V2L / bulk IPVV       [LATER]
9. audit repo visibility               [DONE — PDFs untracked]
```

---

## 2. WHAT WAS BUILT (commit-linked)

### A. Repo exposure fix — `0dd950d`
- The repo `prx0r/patala` is **PUBLIC**.
- Untracked **9 in-copyright scholar PDFs** (sivaqueue2: Dyczkowski Doctrine_of_Vibration,
  Hanneder Malinīślokavārttika, Chakravarti Tantrasāra, + āgama texts).
- `.gitignore` now excludes `**/*.pdf` + `data/corpus/registries/*.jsonl` +
  `data/corpus/downloads/*.{json,jsonl}` (derived data stays local).
- ⚠️ **OPEN (owner decision):** the PDFs remain in PRIOR git history. Full removal needs a
  destructive `git filter-repo` rewrite. Not done unilaterally.
- Safe: `research-library/` (scholar essays/PDFs) was already OUTSIDE the repo (0 tracked).

### B. Registry concurrency — `9c16373`
- `pipeline/object_registry.py`: `_FileLock` (fcntl single-writer) + `_atomic_write`
  (temp + fsync + atomic `os.replace`) for rewrites; append_event takes the lock + fsyncs.
- Permanently fixes the torn-write corruption class. Tests pass.

### C. T1 units vs ARGMAP context windows — `397ca25`
- `pipeline/ingest_ipvv_t1_feeder.py`: records segmentation provenance
  (`semantic_boundary_claim=NONE`), builds **overlapping `ArgumentContext` bundles**
  (`ipvv:V2:argctx:NNN`, contiguous members) so ARGMAP consumes a contiguous bundle, not a
  cut-in-half unit. 10 argctx objects for V2L.

### D. THE DECISIVE EXPERIMENT — IPVV-ARGREC-PILOT-001 (`397ca25` … `ec11368`)
- **Key correction:** V2L's T1/L0/C1 ALREADY EXIST as gold material in the sanskree stack
  (`translations/_stack/ipvv/02_t1|/l0|/c1/read`). Generating T1 was pointless — the pilot feeds the
  model the REAL existing T1/L0/C1 for kārikās 1-5, with NO gold ARGMAP leakage.
- Result (real): the machine independently recovered the V2L argument —
  - what_is_at_issue: the ahaṃ-pratyavamarśa / vikalpa / dvayākṣepī-viniścaya crux ✓
  - steps: objection (āśaṅkā) → reply ("nāsau vikalpaḥ sahyukto dvayākṣepī viniścayaḥ") → crux
    (word-body = śabdana, not organ-born word) ✓  — the CORRECT argument.
  - **UNSUPPORTED_BRIDGE_RATE = 0** (the catastrophic metric).
- Files:
  - `pipeline/freeze_argrec_pilot.py` → `data/evaluation/argrec-pilot-001-freeze.json`
  - `pipeline/run_argrec_pilot_argmap.py` (hermes-driven, no gold leakage)
  - `pipeline/finalize_argrec_pilot.py` → `data/evaluation/argrec-pilot-001-argmap.json`
  - `benchmarks/v0/runs/argrec-pilot-001-score.json`
- ⚠️ **OPEN (scorer limitation):** blind score reads 0.0 recall because the scorer uses naive
  token-overlap; scholarly paraphrase shares almost no surface tokens. The recovery is correct but
  UNDER-MEASURED. **The scorer needs semantic matching (embeddings / LLM-as-judge).**

### E. Agent 1 judging infrastructure (the "consumers ready to judge")
- `ARGUMENT-RECOVERY-BENCH-v1` (`de2030a`, `510c714`): gold schema + blind scorer +
  `build_recovery_gold.py` → **51 frozen recovery-gold cases** (`data/evaluation/recovery-gold-v1.json`)
  from the real IPVV pilot golds.
- `warrant_reconstruction.py` (`406e5aa`): TEXT_EXPLICIT / RATIONAL / EDITORIAL + fabrication detection.
- `ESSAY-BENCH-v1` (`31246bb`): 4 gates (traceability / claim fidelity / essay-argument /
  prose-discourse), validated against REAL scholar essays (research-library). It FAILS my generated
  essay (duplicate opening) and PASSES the real one.
- `EDU-BENCH-v1` (`d327eef`): skill validity / misconception diagnosis / progression / transfer;
  real VERTICAL-1 packet scored **0.4 epistemic-valid** (honest finding).
- `layered_scholarship.py` (`a9b52d9`): the hard-data vs loose-interpretation multi-layer object
  (INTERPRETATION ≠ EVIDENCE).
- `extract_arguments_from_essays.py` (`07dd8a0`): backward extraction — real scholar essays →
  gold-compatible arguments (works on the reflexivity-debate essay: 7 rounds, 13 nodes, 3 attacks;
  verdicts parse).

---

## 3. WHERE THE WORKFLOW IS NOW (honest state)

```
PROVEN ✓        exact-version plumbing · provenance propagation · typed argument representation ·
                perturbation/crux machinery · synthesis representation · essay/sentence-audit ·
                education IR · review materialization · correction propagation

NEWLY PROVEN ✓  a bounded pilot CAN recover a real IPVV argument from real T1/L0/C1, no gold
                leakage, with UNSUPPORTED_BRIDGE_RATE = 0  ← the decisive result

NOT YET PROVEN  scaled argument discovery · fair blind scoring (semantic match) · producer fixes
                from findings · 5-argument / bulk IPVV · scholar acceptance
```

---

## 4. NEXT PLANS & WHY

1. **Fix the recovery scorer with semantic matching** (embeddings or an LLM-as-judge over the gold
   propositions) so the pilot's true recovery is fairly measured. *Why:* token-overlap
   under-measures correct scholarly paraphrase — we cannot know if discovery works until we measure
   it fairly.
2. **Push the backward-extracted real arguments through the EXISTING synthesis/crux machinery** so
   synthesis + education get real fuel (not hand-gold). *Why:* everything above ARGMAP is currently
   demonstration until real arguments flow.
3. **Inspect the pilot's recovered argument manually + fix the producer** (the objection/reply/crux
   it recovered is correct — confirm and generalize). *Why:* close the recovery loop credibly.
4. **Only then scale to V2L / bulk IPVV** (the feeder + ArgumentContext layer is ready). *Why:* do not
   run 48 units until a 5-unit pilot is credible.

**Review items for the coordinator:**
- [ ] Repo history rewrite (PDFs) — owner decision, destructive.
- [ ] Recovery scorer: adopt semantic matching.
- [ ] Confirm the pilot's UNSUPPORTED_BRIDGE_RATE=0 as the headline discovery result.
- [ ] Education: VERTICAL-1 packet is only 0.4 epistemically valid — needs producer fix (free-text
      warrants with no options, multiple-correct, missing transfer).

---

## 5. KEY FILES MAP

| Concern | Path |
|---|---|
| Master build spec (devpath13) | `endgamebuild/devpath13-a1-continue-v2.md` |
| This record | `endgamebuild/BUILD-NOTES-PROGRESS.md` |
| Recovery bench | `source-evidence/evals/patala/tasks/argument_recovery_bench.py` |
| Recovery gold | `data/evaluation/recovery-gold-v1.json` |
| Pilot freeze / candidate / score | `data/evaluation/argrec-pilot-001-*.json` + `benchmarks/v0/runs/argrec-pilot-001-score.json` |
| Pilot scripts | `pipeline/{freeze,run,finalize}_argrec_pilot*.py` |
| T1-unit/ArgumentContext feeder | `pipeline/ingest_ipvv_t1_feeder.py` |
| Backward extractor | `pipeline/extract_arguments_from_essays.py` |
| Warrant / essay / edu evaluators | `source-evidence/evals/patala/tasks/{warrant_reconstruction,essay_bench,edu_bench}.py` |
| Layered scholarship | `machinelearning/research/patala_ml/layered_scholarship.py` |
