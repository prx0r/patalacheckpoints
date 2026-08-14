> **ARCHIVED / SUPERSEDED** — kept for history only. Do NOT follow as current. See `docs/INDEX.md` + `docs/DOCS-AUDIT.json` for the canonical doc for this concern.

# P2 ENSEMBLE — Vidyut × Heritage morphology validation (CP1)

*2026-08-12. Agent L0. An INDEPENDENT INSTRUMENT CALIBRATION experiment — NOT "another parser in the
stack." Question: **how trustworthy is the morphological witness, and what does disagreement mean?**

## Why this exists
P0 (source coverage) is PROVED for the V2/V3 flagship corpus (35/35 lossless). The next uncertainty is
not "did we lose source text?" but "is the morphology witness trustworthy, and which disagreements are
real L0 problems vs tool/representation artifacts?" The current Vidyut P2 result (55% supported, 29.5%
CONFLICT, 11.8% UNANALYZED) is polluted by representation differences (compounds, stems). This
experiment measures how much survives normalization by bringing in an independent witness.

## Honest status labels (never PROVED)
- `SUPPORTED_BY_ENSEMBLE` — both witnesses license the analysis
- `SUPPORTED_BY_SINGLE_WITNESS` — one witness licenses, other neutral/absent
- `CONFLICTING_WITNESSES` — witnesses disagree (genuine review candidate)
- `UNANALYZED` — no witness can analyze it (tooling gap, not necessarily L0 error)

## The experiment

### Input sets
| Set | Source | Purpose |
|---|---|---|
| A | all Vidyut CONFLICT | measure how much is representation-vs-real |
| B | all Vidyut UNANALYZED | measure tool coverage gap |
| C | ~N Vidyut CONFIRMED (control) | calibration: does agreement = correctness? |
| D | ~N Vidyut AMBIGUOUS_SUPPORTED (control) | calibration |

### Per-record capture
`l0_id · surface · lemma_iast · vidyut_state · vidyut_analyses[] · heritage_state · heritage_roots[] ·
agreement_class · relation_class`

### The disagreement taxonomy
```
V+ / H+  both support L0              → SUPPORTED_BY_ENSEMBLE
V- / H+  Vidyut conflict, Heritage ok → Vidyut-specific limitation / representation mismatch
V+ / H-  Vidyut ok, Heritage conflicts→ genuine review candidate
V- / H-  both conflict                → high-priority philological review
V? / H?  both unanalyzed              → tooling coverage gap
```
Normalized relation classes:
```
EXACT_LEMMA_AGREEMENT · STEM_EQUIVALENT · COMPOUND_SEGMENTATION_DIFFERENCE
· MORPHOLOGICAL_FEATURE_DIFFERENCE · NO_ANALYSIS · TOOL_ERROR
```

### Artifacts
```
p2_ensemble_report.json    summary + benchmark-style rates
p2_ensemble_confusion.csv  Vidyut×Heritage confusion matrix
p2_disagreements.jsonl     per-record (streamed)
p2_review_queue.jsonl      high-value cells for manual review
```

### Benchmark-style summary rates
```
CONTROL AGREEMENT RATE      (how often both witnesses agree on known-supported records)
CONFLICT RESOLUTION RATE    (how much Vidyut CONFLICT resolves to support via Heritage)
DOUBLE-CONFLICT RATE        (how much is genuinely contested)
DOUBLE-UNANALYZED RATE      (tool coverage gap)
TOOL ERROR RATE
```

## Reproduce
```
python3 pipeline/verify_l0_p2.py --l0 .../l0 --out /tmp/p2rec      # → p2_records.jsonl
python3 pipeline/verify_l0_ensemble.py --records /tmp/p2rec/p2_records.jsonl --out /tmp/ens \
    --control-n 500 --limit 2000 --seed 42
```

## Results

### Sampled run (500 records: 150 CONFLICT + 150 UNANALYZED + 100 CONFIRMED + 100 AMBIGUOUS_SUPPORTED)
Reproduce: `python3 pipeline/verify_l0_ensemble.py --records /tmp/p2rec/p2_records.jsonl --out /tmp/ens_s2 --control-n 100 --limit 150 --seed 42`

**Confusion matrix (Vidyut × Heritage sign):**
| Cell | Count | % | Meaning |
|---|---|---|---|
| V+/H+ | 170 | 34.0% | both support L0 |
| V?/H+ | 125 | 25.0% | Vidyut unanalyzed, Heritage supports → **VIDYUT_COVERAGE_GAP** |
| V-/H+ | 108 | 21.6% | Vidyut conflict, Heritage supports → **VIDYUT_REPRESENTATION_MISMATCH** |
| V-/H- | 42 | 8.4% | **DOUBLE_CONFLICT** (genuine review) |
| V+/H- | 30 | 6.0% | Heritage disagrees with L0 |
| V?/H- | 24 | 4.8% | Heritage conflicts on unanalyzed-by-Vidyut |
| V?/H? | 1 | 0.2% | both unanalyzed |

**Relation classes:** EXACT_LEMMA_AGREEMENT 19.8% · STEM_EQUIVALENT 14.2% · VIDYUT_COVERAGE_GAP 25.0% ·
VIDYUT_REPRESENTATION_MISMATCH 21.6% · DOUBLE_CONFLICT 8.4% · HERITAGE_DISAGREES_WITH_L0 6.0%.

**Benchmark rates:**
- **CONTROL AGREEMENT RATE: 85.0%** (170/200) — both witnesses agree on known-supported records. Validates the instruments.
- **CONFLICT RESOLUTION RATE: 72.0%** (108/150) — most Vidyut CONFLICT resolves to Heritage support → representation mismatch, NOT L0 error.
- **DOUBLE-CONFLICT RATE: 28.0%** — the genuinely contested remainder.
- **DOUBLE-UNANALYZED RATE: 0.2%** — nearly no tool coverage gap.
- **TOOL ERROR RATE: 0.2%**.

**Key conclusion:** the Vidyut 29.5% CONFLICT is **heavily inflated by representation mismatch (72% resolves)**. The real philological-dispute signal is ~8.4% (double-conflict). Vidyut's coverage gap is small (only 0.2% both-unanalyzed). **P2 (Vidyut morphology) is a useful witness** — its CONFLICT is mostly a representation artifact, and its UNANALYZED is largely recoverable by Heritage.

## Interpretation (how to read the numbers)
- A high **control agreement rate** (both witnesses agree on known-supported) validates the instruments.
- A high **conflict resolution rate** (Vidyut CONFLICT → Heritage supports) means most Vidyut
  "conflicts" are representation mismatches, NOT L0 errors — the 29.5% is inflated.
- A low **double-conflict rate** means few genuine philological disputes.
- High **double-unanalyzed** = tooling coverage gap, not L0 error.

## Blind manual review (required, in progress)
25–50 cases per major cell must be inspected by hand — otherwise "agreement" could be both tools making
the same mistake. This is the only way to know agreement ≈ correctness.

---
*Never promote MORPHOLOGY to PROVED. Use SUPPORTED_BY_ENSEMBLE / SUPPORTED_BY_SINGLE_WITNESS /
CONFLICTING_WITNESSES / UNANALYZED.*
