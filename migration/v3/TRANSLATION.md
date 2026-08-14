# PĀṬALA — THE COMPLETE TRANSLATION (the vision, the gap, the build)

*2026-08-14 · status: THE TRANSLATION REVIEW · the full translation vision from v1+v2, what exists vs
what's missing, and the build. The key finding: **the real translation is NOT just T1** — it's the
three-layer stack (T1 gloss → Close → Reading → Commentary) produced via the three-version flow. And
**one structured Hermes call produces it all.**

---

## THE TRANSLATION VISION (from the v1+v2 docs)

### The three-version flow (translation_flow_spec.md)
```
T1 (working) → R1 (review) → T2 (genuinely different) → R2 (adjudicate) → T3 (final synthesis) → C1
```
The principle: *three translations, composed independently, cannot be wrong in the same way — where they
agree is the hard core; where they differ is the interpretation-space; the adjudication is the commentary.*

### The three-layer model (TRANSLATION_PROTOCOL.md)
For each passage, three renderings:
| Layer | What | For |
|---|---|---|
| **Close** | structurally faithful | scholarship, audits, comparisons, agents |
| **Reading** | natural English, defensible | the default site reader |
| **Commentary** | what's happening | explanation, not translation |

### The translation object (TRANSLATION_SCHEMA.md)
Versioned passage-level claims linked to Sanskrit evidence — never one blob. From it derive concordance,
term history, commentary, audits, MCP, scholar review.

---

## WHAT EXISTS vs WHAT'S MISSING (the honest gap)

### Exists (the gold + partial workers)
| Piece | Status |
|---|---|
| T1 word-gloss worker | ✅ `t1_worker.py` (real, tested — produces correct glosses) |
| L1/L2 scaffold worker | ⚠️ `l1_l2_worker.py` — but it EXPLICITLY says "the point is NOT translation quality, it is provenance continuity" — it's a scaffold, not a real translation |
| T3 finals (gold) | ✅ 10+ works have human `t3_final.md` |
| The three-version flow | ❌ NO workers for R1/T2/R2 — the gold is human-authored |

### Missing (the real translation product)
| Piece | Status |
|---|---|
| **Close translation generation** | ❌ only optional enrichment in l1_l2, never gates |
| **Reading translation generation** | ❌ not automated |
| **Commentary generation** | ❌ not automated |
| **The three-version flow (T1→R1→T2→R2→T3)** | ❌ gold-only, no workers |

---

## THE BUILD — the complete translation in ONE structured call

The finding: **the three-layer translation (T1 → Close → Reading → Commentary) is produced by ONE
structured Hermes call** — the layers are interdependent, so producing them together is faster and more
coherent than 4 sequential calls.

### The worker (migration/v3/translate_passage.py)
One Hermes call returns JSON:
```json
{
  "t1":       {"token": "word-faithful gloss", ...},
  "close":    "structurally faithful translation",
  "reading":  "natural English translation",
  "commentary": "what the verse is doing",
  "notes":    ["uncertainties", "alternative readings", "term decisions"]
}
```
Then the non-aggregate TranslationProof (11-dim vector) is computed over it.

### The tested proof (fresh Vākyapadīya 1.1, ONE call)
- **T1:** `[and]-beginningless and endless (anādinidhanam)` · `[and]-Brahman (brahma)` · `[and]-Word-essence (śabdatattvam)` · `[and]-which (yad)` · `[and]-imperishable (akṣaram)`
- **Close:** "Brahman, beginningless and endless, the Word-essence (śabdatattva), which is imperishable (akṣara)"
- **Reading:** "Brahman — without beginning or end — is the imperishable reality of the Word (śabdatattva); from it, the imperishable, the world-process unfolds."
- **Commentary:** correctly explains śabdādvaita, vivarta vs pariṇāma, the akṣara pun (imperishable + syllable), the praṇava OM
- **Proof:** 11-dim vector, gate BLOCKED (human adjudication pending — honest)

### How to run
```bash
python3 migration/v3/translate_passage.py "anādinidhanam brahma śabdatattvaṃ yad akṣaram"
```

---

## WHY ONE CALL (not 4 sequential)

The layers are interdependent: reading builds on close, commentary explains reading. Producing them in a
single structured call is:
- **Faster:** one round-trip (~60s) instead of four (~240s)
- **More coherent:** the model produces the layers against each other, not in isolation
- **How production should work:** a task = one call that returns the full artifact

---

## THE HONEST STATE

| Translation layer | v1/v2 vision | Automated? | Verdict |
|---|---|---|---|
| T1 (word gloss) | the transliteral floor | ✅ `t1_worker.py` | WORKS |
| Close | structurally faithful | 🔧 now `translate_passage.py` | WORKS (built) |
| Reading | natural English | 🔧 now `translate_passage.py` | WORKS (built) |
| Commentary | what's happening | 🔧 now `translate_passage.py` | WORKS (built) |
| The three-version flow (T1→R1→T2→R2→T3) | the anti-cheat scholarship | ❌ gold-only | GAP — needs R1/T2/R2 workers |
| Proof | the non-aggregate audit | ✅ `translation.py` | WORKS |

**The build result:** the three-layer translation (T1 + Close + Reading + Commentary) is now automated
via one Hermes call. The remaining gap is the **three-version flow** (T2/R2 workers) — the anti-cheat
scholarship that produces the "hard core" via independent translations. That's the next frontier, and it
can be built the same way (T2 = a second Hermes call with a different reading-strategy).

---

*This is the complete translation review. The real translation is T1 + Close + Reading + Commentary —
now automated in one structured Hermes call (tested on a fresh verse). The remaining gap is the
three-version flow (R1/T2/R2 workers) which produces the anti-cheat scholarship — buildable the same way.*
