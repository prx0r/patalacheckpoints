> **ARCHIVED / SUPERSEDED** — kept for history only. Do NOT follow as current. See `docs/INDEX.md` + `docs/DOCS-AUDIT.json` for the canonical doc for this concern.

# P4 ALIGNMENT — task definition (the meaningful L0↔L2 benchmark)

*2026-08-12. Defines what P4 (CP1, Agent 2 / L0 lane) actually measures, BEFORE building. Written because the
prior P4 artifact (`benchmark_p4_alignment.py`, commit `7c28065`, `docs/p4_alignment_eval_report.json`) measured
the **trivial by-construction** gloss↔iast pairs, which is NOT the meaningful task. Per
`docs/L0_PROGRESS_AND_PLAN.md` §next: "the L0 gloss↔iast pairs are aligned *by construction*, so the real P4
question is L0↔L2 (published prose) alignment."*

---

## 1. Why the prior baseline was the wrong task

The committed baseline samples 66,077 clean L0 token pairs (`literal_gloss` EN ↔ `lemma_iast` SKT). But those
pairs come from the **same** `[and]-gloss (iast)` fragment — they are aligned **by construction**. Measuring an
aligner's ability to reproduce them is circular/self-validating; it does not test whether alignment is recoverable
from the actual source + prose.

## 2. The real substrate (verified)

- **L0** (`l0/*.l0.jsonl`, 35 chunks, 103,917 records): word-level gloss. Each record carries
  `lemma_iast` (Sanskrit) + `literal_gloss` (English) + exact source spans + `quoted` + `status`.
  This is the **source side**, aligned by construction.
- **L2** (`l2_text` in `data/published/ipvv/pt-passage-*.json`, 49 passages): **freestyle interpretive prose**
  (Dyczkowski-mode), NOT a word-for-word translation. **43 of 49 passages embed Sanskrit anchors inline in
  parentheses**, e.g. `reflexive-awareness (vimarśa)`, `re-reflection (parāmarśa)`, `the first "tuṭi" (the
  bursting)`. The surrounding prose is interpretation (SUPPLIED), not token-for-token.
- **No L0↔L2 gold exists.** `l2_text` is a separately-compiled rendering (does not byte-match the L2 pilot body).

## 3. What "correct alignment" means (the scoped, defensible definition)

The L2 prose is paraphrase, so free-form bitext alignment (e.g. awesome-align AER) is ill-defined. The
**recoverable, token-grounded** unit is the **inline Sanskrit anchor** the prose itself marks in parentheses.
So:

> **P4 task = term-anchor alignment.** For each L2 sentence, recover the inline IAST anchor(s); link each anchor
> to the matching L0 lemma record within the same passage (exact lemma match; else `UNALIGNED`). Prose with no
> recoverable anchor must be **abstained on**, not force-aligned.

This aligns with the abstention principle (the L0/L2 Fidelity notes already mark SUPPLIED additions as non-grounded).

## 4. Metrics

- **Anchor-recovery recall** — fraction of true inline IAST anchors the system finds in the L2 prose.
- **Anchor-resolution precision** — of the anchors found, fraction correctly linked to a same-passage L0 lemma.
- **Abstention quality** — prose clauses with no recoverable anchor are correctly left `UNALIGNED` (no invented mapping).
- Report precision / recall / abstention **per-passage**, no single aggregate (per `benchmarks/v0/METRICS.md`).

## 5. Baselines + the independent witness

1. **regex paren-extraction** — naive floor: finds parentheticals (high anchor recall, 0 resolution).
2. **token-overlap vs L0 lemmas** — links anchors by surface overlap to L0 `lemma_iast`, with the
   established matching rule (diacritic-insensitive stem-as-prefix; per the P2 lesson). Current floor:
   **resolution recall 0.93 / precision 0.89 / abstain 1.0** over 35 passages / 105 anchors.
3. **Independent morphological witness (Vidyut)** — since awesome-align is a *sentence-level bilingual
   aligner* (fits MT bitext, not our anchor↔lemma L0↔L2 task), we use Vidyut (already our P2 engine,
   CPU) as the independent second method: it confirms an anchor↔L0-lemma link by assigning both forms a
   common stem. This is the non-human "two reviewers" step (per the P2 Vidyut×Heritage precedent).

**Ensemble result (2026-08-12, `--witness`):** over 99 resolved links, Vidyut confirms **38 AGREE / 9
DISAGREE / 52 UNABLE** → **agree_rate_analyzed_only 0.81** (81% of links Vidyut could analyze), with
UNABLE mostly inflected/compound L0 surfaces Vidyut cannot parse (honest abstention, not fabricated
agreement). The 9 DISAGREE are largely Vidyut compound-analysis errors on the L0 surface side, not
genuine anchor mismatches — recorded as a Vidyut limitation, not as a P4 failure.

## 6. Gold-first discipline

- **No fresh human gold is available.** Independence is instead established via (a) the deterministic
  baselines, (b) the independent Vidyut morphological witness (ensemble agreement), and (c) hard
  invariants (anchor verbatim in the L2 prose; resolved lemma's Sanskrit actually occurs in the source).
- The token-overlap floor + Vidyut agreement together constitute a multi-witness result, mirroring how P2
  was frozen as a calibrated witness without a fresh human pass.
- No claim of "alignment solved"; only "aligned on this data, confirmed by an independent morphological
  witness, beating the trivial floor".

## 7. Status

**FROZEN — SUPPORTED_MACHINE_WITNESS (2026-08-12).** Per the adequacy doctrine, P4 has done its job:
- deterministic aligner: **recall 0.93 / precision 0.89 / abstention 1.0** (35 passages / 105 anchors)
- independent Vidyut morphological witness: **0.81 analyzed-only agreement** (38 AGREE / 9 DISAGREE /
  52 UNABLE, analyzed_share 0.47)
- **What it does:** proposes/resolves likely anchor↔lemma links.
- **What it does NOT do:** prove semantic equivalence · prove translation correctness · replace human
  philology.
- **Freeze:** do NOT hunt a third analyzer / tune compound handling / squeeze 0.81→0.88.
- **Next review:** ONLY when a real downstream consumer fails. P4's uncertainty is metadata carried
  into the proposition certificate, not a blocker.

Report: `docs/p4_alignment_eval_report.json`. Code: `pipeline/l0_align.py` + `pipeline/test_l0_align.py`
(26/26 pass). Claim: CLAIMS.md P-013.
