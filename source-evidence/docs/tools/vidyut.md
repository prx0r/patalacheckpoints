# Vidyut — the Sanskrit linguistic engine (S-tier)

**What Pāṭala borrows:** the deterministic Sanskrit linguistic stack — segmentation, morphology,
inflection, transliteration, sandhi, meter. This is the canonical `SanskritLinguisticAdapter`: every
passage acquires linguistic annotations (segments, lemmas, morphology, sandhi, meter) as **derived
annotations, never edits to L0**.

**License:** Apache-2.0. Repo: `ambuda-org/vidyut`.

## Components
- `vidyut-cheda` — segmentation + morphological annotation (interactive, low-memory, real-time).
- `vidyut-prakriya` — Pāṇinian derivation.
- `vidyut-kosha` — compact inflection lookup.
- `vidyut-lipi` — transliteration (IAST/SLP1/Devanagari).
- `vidyut-sandhi` — sandhi splitting.
- `vidyut-chandas` — meter.

## How Pāṭala consumes it
**INTEGRATED** — used in `pipeline/agentic_gloss.py` as the deterministic tokenizer/segmenter/
lemmatizer that anchors the per-token gloss work.

```
passage (L0 source text)
   → Vidyut (cheda + lipi + sandhi + kosha)
   → { surface, segments[], lemmas[], morphology[], sandhi_analysis[], derivations[], meter }
   → stored as DERIVED linguistic annotations (never modify L0)
```

## Doctrine
Linguistic analysis is **derived annotation + evidence**, never the L0 truth. Vidyut is one analyzer;
cross-analyzer agreement (DCS/Heritage/VedaWeb) is used for confidence, not Vidyut alone.
