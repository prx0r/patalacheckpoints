# PĀṬALA BENCHMARK v0

*2026-08-12. The frozen evaluation substrate. **Tests machines that propose scholarship.**
Pāṭala PRODUCT publishes scholarship; PĀṬALA BENCHMARK tests machines — they do not collapse.*

## The four task families
- **PATALA-RETRIEVAL** — passage / term-sense / related-passage / translation-crux retrieval
- **PATALA-EVIDENCE** — claim→support / claim→counterevidence / quote-source verification
- **PATALA-STRUCTURE** — proposition extraction, role, explicitness, support/attack/qualify, inference recovery, grounding, scope fidelity
- **PATALA-FIDELITY** — L2→C1 / C1→Theme / Theme→Guide / boundary preservation

## The contracts (frozen)
| File | What it freezes |
|---|---|
| `MANIFEST.json` | version, task families, review states, honesty rules, size targets |
| `SCHEMA.md` | the fixture envelope + acceptance gate + anti-circularity |
| `SPLITS.md` | the leakage policy (S0–S4; S2 is the v0 test; ARG-GOLD-001 = EVALUATION_ONLY) |
| `METRICS.md` | per-metric semantics; NO aggregate score; the 4-layer epistemic declaration |

## Current seed
- `structure/PAT-STRUCT-001.json` — **ARG-GOLD-001** (the first hand-built gold argument, V2-O).
  `SINGLE_EDITOR_GOLD`, `EVALUATION_ONLY`, `allowed_training_use: false`.

## Rules
1. A fixture produced by method X cannot gold-evaluate X (anti-circularity).
2. Every run is immutable (`runs/<ts>/` with version, split, config, predictions, metrics, commit).
3. No magical aggregate score; report per-metric.
4. Ad-hoc results not rerun on this frozen suite are `PRE-BENCHMARK` (retired).

## Next (per the plan)
- Hand-build ~4 more gold arguments → structure family grows past the seed.
- Rerun BM25/dense/hybrid against this frozen suite (split S2) → re-baseline or retire.
- Evaluate the first automatic argument extractor against ARG-GOLD-001 (harness test, no model selection).
