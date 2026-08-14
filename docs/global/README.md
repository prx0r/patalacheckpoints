# PĀṬALA — THE THESIS

*The canonical one-page statement of what Pāṭala is, what it is not, what it contributes, and where it
sits in the ecosystem. This is the README of the global docs — the answer to "what are we actually
building?" Read this first; everything else is detail.*

---

## WHAT PĀṬALA IS

> **Pāṭala is an authority graph for historical Sanskrit knowledge — a reconciliation engine that
> turns uncertain, fragmented, external manuscript and scholarship records into increasingly resolved,
> provenance-carrying scholarly objects, with machines proposing structure and scholars able to
> inspect, correct and certify it.**

The core chain — the thing that makes Pāṭala hard to replace:

```
MANUSCRIPT / EXTERNAL RECORD
      ↓  (reconciliation)
WORK
      ↓
EDITION → WITNESS → SURROGATE → ETEXT → SOURCE
      ↓
PASSAGE → TRANSLATION DECISION
      ↓
PROPOSITION
      ↓
ARGUMENT → CRUX
      ↓
ARGUMENT SYNTHESIS
      ↓
{ REVIEW · ESSAY · EDUCATION · AGENTS }
```

Everything below `WORK` is the **deep scholarly vertical**; everything above `MANUSCRIPT` is the
**ingestion/reconciliation surface**. Both meet on the same canonical IDs. That is the two-speed
architecture: most records are weak/sparse/uncertain (handled by reconciliation), a few are
gold-grade arguments (handled by the deep vertical).

## WHAT PĀṬALA IS NOT

- **Not** another manuscript archive (Gyan Bharatam, OCHS, NGMPP already do that).
- **Not** another Sanskrit e-text library (GRETIL, SARIT, Ambuda, Muktabodha already do that).
- **Not** another OCR/HTR project (Kraken, Transkribus, eScriptorium exist).
- **Not** another translation publisher (84000, SuttaCentral exist).
- **Not** another generic AI essay generator (that gets commoditized).

Pāṭala is **between** those layers: it resolves, connects, contextualizes and certifies.

## THE ONE CONTRIBUTION

> **Pāṭala owns the epistemic dependency graph — the answer to "what exactly exists, what is this
> edition/witness/text, where did this reading come from, who supports it, who disputes it, and what
> downstream knowledge depends on it?" — with every answer carrying exact provenance and an honest
> authority state.**

The moat is not the corpus (copyable) nor the translations (increasingly copyable). It is the
**versioned, provenance-carrying, expert-correctable authority graph**:

```
M ≈ D × P × V × N × A
  D = curated data · P = provenance depth · V = verified judgments
  N = contributor network · A = adoption of identifiers/interfaces
```

## THE INTEGRATION POSTURE

Pāṭala **borrows mature open infrastructure** (reuse-first) and integrates it as a permanent
subsystem — it never rebuilds what exists, and every external tool has one bounded job:

| Class | Tools (documented + adapted) | Pāṭala owns |
|---|---|---|
| **Parsing** | GROBID, Docling, AnyStyle | the stable span, not the parse |
| **Bibliography/identity** | Crossref, OpenAlex, OpenCitations, Zotero, ORCID, ROR | identity resolution + provenance, not the global DB |
| **Retrieval** | Tantivy, PaperQA2, SciRAG | the candidate→judge loop, not the search engine |
| **Annotation/gold** | INCEpTION, Recogito | the gold labels + ReviewEvents, not the UI |
| **Review/publishing** | OpenReview, COAR Notify, Manubot | the epistemic impact, not the workflow |
| **Evaluation** | Inspect AI | the epistemic contracts + benchmarks, not the runtime |
| **Manuscript** | IIIF, Kraken, TEI | the witness→edition decision, not the imaging |

**The invariant:** none of those tools decides "does this evidence support this proposition?" — Pāṭala
owns that seam, and records every imported assertion with `source · version · transform · provenance`.

## THE AUTHORITY LADDER (honest, never inflated)

Every object carries a multidimensional authority vector (never one scalar "trusted"):

```
DISCOVERED → NORMALIZED → CANDIDATE_MATCH → RESOLVED → SCHOLAR_REVIEWED → ADJUDICATED
```

and per-dimension evidence. The doctrine:

```
UNKNOWN → OPEN          is cheap (always allowed)
UNKNOWN → VERIFIED       is dangerous (a false promotion — never silently resolved)
INTERPRETATION ≠ EVIDENCE
SCHOLARLY_CLAIM ≠ PĀṬALA_REVIEW    (a scholar published X ≠ a scholar reviewed our object)
```

## THE PRODUCTS (projections over the one graph)

Everything below is a **materialized projection**, not a separate system:

```
PĀṬALA RESEARCH    discover / reconstruct / synthesize       (the deep vertical)
PĀṬALA REVIEW       verify / dispute / adjudicate             (the scholar product)
PĀṬALA LEARN        understand / manipulate / prove mastery   (the education product)
PĀṬALA ATLAS        resolve / connect / certify               (the reconciliation surface)
```

## WHY PĀṬALA MATTERS NOW

The manuscript-supply problem is being solved (Gyan Bharatam: 11.9M manuscripts surveyed, 800k+
digitized). The bottleneck moves **up**: from digitization to *"what is this object, what work is it,
which recension, what scholarship exists, what can I trust?"* That is the gap Pāṭala fills — and it is
the same engine whether the source is Gyan Bharatam, GRETIL, SARIT, PANDiT, NGMCP, Muktabodha, or
future Greek/Pāli material.

## THE HONEST STATE (what has been proven)

```
PROVEN ✓      exact-version plumbing · provenance propagation · typed argument representation ·
              perturbation/crux machinery · synthesis · essay/education/review evaluators ·
              correction propagation · a bounded pilot recovering a real IPVV argument from real
              T1/L0/C1 with no gold leakage (UNSUPPORTED_BRIDGE_RATE = 0)

IN PROGRESS    filling the Atlas (ATLAS-10 → ATLAS-100) · real ARGMAP at scale · scholar network ·
              human gold via INCEpTION · external-adapter live coverage

NOT YET       scaled argument discovery · scholar acceptance · pedagogical effectiveness ·
              reconciliation at the millions-of-records scale
```

---

*This thesis is the fixed point. `docs/global/globalpartnerships.md` (integration/identity),
`globalaccess.md` (open-reference / controlled-corpus), `PATALA-GLOBAL-ARCHITECTURE.md` (the seven
planes), and `docs/vision/essayguide.md` (the essay/education/review programs) are the detail layers.
Read those next; all point down to this.*

> **The master navigation** — resolve anything (layer, surface, data, script) to its canonical ref,
> implementation, docs, and Hermes usage — is `NAVIGATION.md` (repo root). The deep per-layer pages are
> `docs/layers/`. This file is the thesis they hang on.
