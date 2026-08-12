# SPEC — ALTERNATIVE ARGUMENT-BUILDERS + COMPARISON HARNESS

*2026-08-12. The user's directive: build ALTERNATIVE theme→argument paths, so we can COMPARE which
system produces better arguments and validate which metrics are meaningful (vs. which are "bs"). This is
the scientific-discipline layer — we don't trust one builder; we build several and measure.*

---

## 1. The goal

Given the 6 real IPVV theme-clusters (CL-0..7), build an `ArgumentProposal` for each via **multiple
strategies**, then compare the strategies to find:
1. which builder produces the most **defensible** argument (best premises, best strength),
2. which **metrics** actually discriminate quality (vs. which are noise),
3. how each compares to the **human ground-truth** argument (the reflexivity-debate).

**We don't adopt one path; we measure all and let the evidence decide.**

---

## 2. The alternative builders (the strategies)

Each builder takes a theme (cluster of C1s) and produces an `ArgumentProposal`. They differ in HOW they
derive premises + weights + scheme:

| Builder | Strategy | How it derives | Strength basis |
|---|---|---|---|
| **B-STRUCT** | curated-structure-driven | premises = the member C1s' KEY TERMS + see-also; scheme from cluster content | the C1s' internal relations |
| **B-LEXICAL** | shared-term-driven | premises = C1s sharing the most technical lemmas; scheme = the dominant lemma family | shared-term Jaccard |
| **B-GRAPH** | graph-centrality-driven | premises = the highest-centrality member C1s (the hub of the cluster); scheme = the cluster's connective move | edge weight |
| **B-PUSHING** | question-driven | premises = the PUSHING-record questions that the theme's C1s answer; scheme = the question type | the question-shape DNA |

All four use the SAME `ArgumentProposal`/`build_argument` + Bayesian `strength.py`, so they're
**directly comparable** — only the *premise-derivation* differs. That isolates the variable: which way of
finding premises produces better arguments.

---

## 3. The comparison harness (what we measure)

For each builder × theme, produce an `ArgumentProposal` and score it on TWO kinds of metric:

### 3a. Structural metrics (machine-checkable)
| Metric | What it tests | Meaningful? |
|---|---|---|
| **resolvability** | every premise's passage_id resolves | ✅ always meaningful (audit floor) |
| **premise-diversity** | premises come from ≥2 distinct sub-areas (not all same passage) | likely meaningful |
| **strength-certainty** | the derived Bayesian certainty (WELL_SUPPORTED vs SPECULATIVE) | ⚠️ need to validate — is a "certain" auto-arg actually better? |
| **coverage** | % of the theme's member C1s represented in the premises | test whether more = better |
| **no-anachronism** | premises avoid modern-comparison terms (reuse C1 metric) | ✅ meaningful |

### 3b. Ground-truth comparison (the real test)
For the ONE theme that has a human argument (reflexivity, = CL-3 order-less-support family), compare each
builder's output to the human `LOGICAL-ARGUMENT-1-reflexivity-debate.md`:
- **claim-overlap** — do the builder's premises mention the same load-bearing concepts (reflexivity,
  self-awareness, universalization)?
- **scheme-match** — does the builder's inferred scheme match the human's (reductio/debate)?

This is the **"which metrics are bs"** test: if a metric (e.g. strength-certainty) ranks builder X highest
but the ground-truth says builder X is wrong, that metric is misleading.

---

## 4. The output — a comparison report

For each builder, a per-theme `ArgumentProposal` + the metric scores + (for the ground-truth theme) the
human-comparison. Then a verdict:
```
BUILDER        avg_resolv  avg_div  avg_cov  gt_overlap  verdict
B-STRUCT       1.0         0.8      0.9      0.7         BEST
B-LEXICAL      1.0         0.6      0.7      0.5         (mid)
B-GRAPH        1.0         0.7      0.6      0.6         (mid)
B-PUSHING      0.9         0.9      0.5      0.8         (best gt overlap, lower coverage)
```
The verdict tells us which builder to trust AND whether e.g. "coverage" or "strength-certainty" actually
correlates with ground-truth quality.

---

## 5. What this enables (the payoffs)

1. **Which builder is better** — evidence-based, not preference.
2. **Which metrics are real** — if ground-truth-overlap correlates with builder A, and strength-certainty
   also ranks A high, then strength is meaningful; if they disagree, strength is bs.
3. **The premise→passage gold** — the winning builder's premises ARE the auditable argument roots.
4. **A benchmark** — the ground-truth arguments + these builder outputs form the PATALA-STRUCTURE / argument
   task the strategy requires.

---

## 6. The build queue

| # | Build | Effort |
|---|---|---|
| 1 | **`builders.py`** — the 4 alternative builders (B-STRUCT/LEXICAL/GRAPH/PUSHING) | medium |
| 2 | **`compare_arguments.py`** — the harness scoring each builder×theme + ground-truth comparison | medium |
| 3 | **the comparison report** — the per-builder verdict + which-metrics-are-real | low |
| 4 | **tests** — each builder produces a valid ArgumentProposal; the harness runs | medium |

This is the "compare alternative systems and see what works" layer — and it turns the argument-building
into a measured, falsifiable process instead of one hand-picked path.
