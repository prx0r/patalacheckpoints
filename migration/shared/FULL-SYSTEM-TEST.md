# THE FULL-SYSTEM TEST — the Sārdhatriśatikālottarāgama (the IPVV-equivalent autonomous test)

*2026-08-14 · status: THE TEST WORK · the chosen work to test the FULL autonomous organism, exactly as
we tested IPVV. Both agentgraph and agentpatala build against this single test target.*

---

## THE TEST WORK: Sārdhatriśatikālottarāgama (Stk)

- **What:** a real early-Śaiva-Siddhānta Āgama (the "Three-and-a-half-hundred" Kālottara)
- **Source:** GRETIL, **Dominic Goodall's critical edition** (Pondicherry, IFP 1979) + Rāmakaṇṭha's commentary
- **Size:** 1035 lines, **309 verses** (clean transliterated Sanskrit with `// Stk_1.1` pada markers)
- **Status:** untranslated (`U`), **NO gold built** — a genuinely untranslated work, the IPVV-equivalent test
- **Location:** `data/corpus/sources/sardhatrisatikalottara/sardhatrisatikalottara.txt`
- **Queue:** sivaqueue #31, early Siddhānta, companion guides G2/G5

**Why this work:** it's the ideal full-system test —
- Genuinely untranslated (not pre-golded) → tests the real forward-generation, not reading gold
- Substantive but manageable (309 verses) → a real corpus, not a toy
- Real critical edition (Goodall) → the scholarly standard
- A Śaiva Āgama (different from IPVV's Pratyabhijñā) → tests the organism's portability

---

## THE FULL-SYSTEM TEST PLAN (the autonomous run)

The complete organism, run autonomously on this work's opening verses:

```
SOURCE   the real Stk Sanskrit (Goodall ed.)
  → TOKENIZE   vidyut segments the verses
  → TRANSLATE  real Hermes, complete 3-layer (T1 gloss + close + reading + commentary)
  → PROOF      the non-aggregate 11-dim TranslationProof vector
  → ARGUMENT   mine the claim + entailment move (essay_ingest)
  → CRUX       detect the distillation crux
  → REVIEW     the human gate (evidence advances, machine can't promote)
  → EDUCATION  compile a LearningClaim
  → AUTONOMOUS the priority-queue ingestion loop commits the work (agentgraph's organism)
  → PRODUCTS   the 4-family stack assembles
```

**The runner:** `migration/v3/full_system_test.py` (Hermes for translation, isolated lab kernels for the
rest — the schema.py collision constraint).

---

## THE PASS CRITERIA (each step must pass)

| Step | Pass when |
|---|---|
| SOURCE | the real Stk loads, `// Stk_1.1` + Goodall present |
| TOKENIZE | vidyut segments ≥ 8 tokens of the opening verses |
| TRANSLATE | T1 gloss ≥ 8 terms + close + reading + commentary produced (real Hermes) |
| PROOF | 11-dim vector, honest gate |
| ARGUMENT/CRUX | claim + move + crux mined |
| REVIEW | evidence advances, NOT auto-promoted (human gate) |
| EDUCATION | LearningClaim compiled |
| AUTONOMOUS | the priority-queue loop commits the work (version recorded) |
| PRODUCTS | the 4-family stack assembles (18 products) |

---

## THE SCALED-UP TEST (the corpus-wide graduation)

After the opening-verses test passes, the full autonomous graduation:
1. Run **all 309 verses** through the translation spine (real Hermes, batched per the t1_worker flow).
2. Commit the real L0/T1/L2/L200/C1 objects to the registry (the real data structures).
3. Generate the themes/clusters over the resulting commentaries (the theme worker).
4. Verify a **source mutation propagates** (staleness: change one verse → downstream flags).
5. Serve the compiled projections (bibliography/themes/passages pages).

**This is the shared goal's test:** the whole priority queue (or this one work, full) fed through the
organism as ONE coherent system — populating every data structure and transformation.

---

## THE DIVISION (who does what on this test)

| Task | Owner |
|---|---|
| The translation spine (Hermes) + proof on Stk verses | AGENTPATALA |
| The argument/crux/review/education kernels | AGENTGRAPH (built) + AGENTPATALA (wired) |
| The autonomous ingestion loop | AGENTGRAPH (built `ingestion_organism`) + AGENTPATALA (wired to Stk) |
| The full 309-verse run + registry commit | AGENTPATALA |
| Themes/clusters over Stk commentaries | AGENTPATALA (theme worker) + AGENTGRAPH (cluster kernel) |
| `misconception.py` repair cascade (the loop's closing edge) | AGENTGRAPH |

---

## STATUS

- ✅ Test work chosen + verified (real Stk, 309 verses, untranslated, no gold)
- 🔄 The opening-verses full-system test is running (`full_system_test.py`)
- ⏳ The full 309-verse corpus-wide run is the next milestone

---

*The Sārdhatriśatikālottarāgama is the IPVV-equivalent test: a genuinely untranslated Śaiva Āgama run
through the complete autonomous organism. This is what proves the shared goal works — one real work,
fully ingested and transformed as one coherent system.*
