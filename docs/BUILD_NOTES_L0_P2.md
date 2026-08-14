> **ARCHIVED / SUPERSEDED** — kept for history only. Do NOT follow as current. See `docs/INDEX.md` + `docs/DOCS-AUDIT.json` for the canonical doc for this concern.

# BUILD NOTES — L0 P2: Vidyut morphology witness + proof-semantics separation

*2026-08-12. Agent L0. This note records: (1) the standalone Vidyut P2 witness
(`pipeline/verify_l0_p2.py`), (2) the full-corpus P2 result, and (3) the `PhilologicalProof`
semantics correction (extraction_coverage ≠ lexical_sense). Aligned to `dualagentvision.md` CP1
(SOURCE PROOF).*

---

## 1. The P0 / P2 separation (frozen architecture)

Two independent problems, never conflated:

```
P0: Did we account for every T1 source region?     → verify_l0.py --level p0
P2: Is the extracted Sanskrit lemma licensed?      → verify_l0_p2.py (Vidyut)
```

P0 does NOT need Vidyut; Vidyut does NOT solve P0. If the hand parser silently misses a token,
Vidyut never sees it. The pipeline:

```
FREEFORM T1
  → tolerant editorial extractor (recognized / structural / UNKNOWN spans)
  → P0 coverage certificate ("every region classified?")
  → extracted Sanskrit spans → VIDYUT → P1/P2 linguistic witnesses
```

## 2. `pipeline/verify_l0_p2.py` — the Vidyut P2 witness

For every L0 record with a `lemma_iast` (surface), runs Vidyut (Chedaka + Kosha) and classifies:

| State | Meaning |
|---|---|
| `CONFIRMED` | Vidyut licenses our lemma/analysis |
| `AMBIGUOUS_SUPPORTED` | ours is one of several Vidyut analyses |
| `CONFLICT` | Vidyut analyses the surface, but as a different stem/segmentation |
| `UNANALYZED` | Vidyut cannot analyze the surface |
| `NO_SANSKRIT` | L0 record has no IAST lemma (the gloss-only AMBIGUOUS/FAILED set) |
| `TOOL_ERROR` | a transliteration/tool failure (kept separate from UNANALYZED) |

**Important matching rule (learned):** L0's `lemma_iast` stores the SURFACE (e.g. `saṃvedanasya`),
Vidyut returns the STEM (`saṃvid`). A naive exact match produces ~50% false `CONFLICT`. The fix:
match stem-as-prefix of surface + surface's own token text, giving derivationally-compatible
matches. Without this, the CONFLICT number is meaningless.

## 3. Full-corpus P2 result (V2/V3, 103,906 records, 35 chunks)

| State | Count | % |
|---|---|---|
| CONFIRMED | 29,284 | 28.2% |
| AMBIGUOUS_SUPPORTED | 27,967 | 26.9% |
| **supported (subtotal)** | **57,251** | **55.1%** |
| CONFLICT | 30,631 | 29.5% |
| UNANALYZED | 12,259 | 11.8% |
| NO_SANSKRIT | 3,758 | 3.6% |
| TOOL_ERROR | 7 | 0.0% |

**Interpretation (honest):**
- **55% of extracted Sanskrit lemmas are linguistically supported** by Vidyut.
- **29.5% CONFLICT** are largely **multi-member compounds** Vidyut segments into constituents
  (`svaprakāśatā → su+aprakāśatā`, `saṃśayānivṛtteḥ → saṃśayā+nivṛtteḥ`) while L0 treats them as one
  lemma. This is a REAL surface-vs-segmentation signal (P1/P2 intersection), not an error — a
  first-class disagreement-queue item.
- **11.8% UNANALYZED** + **3.6% NO_SANSKRIT** are genuinely without Vidyut support (sandhi forms
  Vidyut can't split, or gloss-only records).
- **7 TOOL_ERROR** — transliteration edge cases (e.g. `kārikās 4–5`), not linguistic.

Per-chunk results in `/tmp/l0p2full2/` (p2_summary.json + per-chunk `*.l0.p2.json`).

## 4. `PhilologicalProof` semantics correction (philproof.py)

**The bug fixed:** `proof_from_verify_l0` mapped `coverage.unknown → lexical_sense`. That conflates
two uncertainties:
- **extraction_coverage** = did the extractor classify every T1 region? (P0)
- **lexical_sense** = we identified the Sanskrit, but is its sense resolved? (P3)

A chunk with unclassified chars has `extraction_coverage: OPEN` — that is NOT an unresolved lexical
sense. Now:
- DIMENSIONS: `coverage` → **`extraction_coverage`**.
- `proof_from_verify_l0`: unknown chars → `extraction_coverage: OPEN` (+ `EXTRACTION_COVERAGE:n chars`
  in `open`); `lexical_sense` is left `UNCHECKED` (only P3 resolves it).

Verified: passing chunk → `extraction_coverage: PROVED, lexical_sense: UNCHECKED`; failing chunk →
`extraction_coverage: OPEN, open:['EXTRACTION_COVERAGE:639 chars...']`.

**Note:** the other agent owns `philproof.py` long-term; this correction is now in place and
contractually sound. The ML lane consumes `extraction_coverage` as the P0 signal and `lexical_sense`
only once P3 exists.

## 5. Reuse / not-rebuild
Vidyut (`vidyut 0.4.0`, MIT) is the P2 witness (already installed). Heritage (`heritage 1.1.0`) is the
independent second witness for P3 ensemble. `verify_l0_p2.py` emits witness states WITHOUT overwriting
L0 — Vidyut is a witness, not the editor.

## 6. Status vs the checkpoint gate (dualagentvision CP1)
- **P0 (source coverage):** V2/V3 15/35 chunks lossless; the rest honest `extraction_coverage: OPEN`.
- **P2 (morphology):** 55% supported; disagreement queue built from the 29.5% CONFLICT (compounds) +
  11.8% UNANALYZED.
- Remaining: run V2/V3 toward 63/63 P0, then Heritage as the P3 cross-check; V1 legacy format.
