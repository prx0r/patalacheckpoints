# VISION — the one audited epistemic organism (the cohesive endgame)

*2026-08-15 · the complete endgame: how the OG patala learning surface, the product engines, and the
derivational chain form ONE organism — not two sites. Everything audited, everything resolving to
source.*

---

## THE ONE PICTURE (one organism, layered)

```
┌─────────────────────────────────────────────────────────────────────┐
│ THE SITE (serving surface — what users + agents see)                │
│   /              atlas graph                                        │
│   /bibliography  the works (254)                                    │
│   /themes        the theme clusters                                 │
│   /learning      schools · timeline · shared foundations (audited)  │
│   /education     the lessons (LearningPackets, audited to source)   │
│   /concepts      the 25 concepts                                    │
│   /scholars      the scholar contribution ledger (JSON-LD)          │
│   + /resolve     the audit trail (any claim → source)               │
│   + API :8787    education index · resolve · answer (tutor)         │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ serves immutable bytes (compute-on-write, 0-JS)
┌───────────────────────────────▼─────────────────────────────────────┐
│ THE PRODUCTS (the engine layer — deterministic, real data)          │
│   education_organism/: education · organism · organism_loop ·       │
│     misconception · pedagogy · memory · segment_key · reconciliation│
│   (+ agent3's passage/claim/argument/crux/scholar_*/review_* engines)│
│   → generate + validate the content the site serves                 │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ feeds
┌───────────────────────────────▼─────────────────────────────────────┐
│ THE ORGANISM (the derivational chain + audit)                       │
│   SOURCE → T1 → L0 → L2 → L200 → C1 → THEME → ARG → SYNTH →         │
│   ESSAY → EDUCATION, audited via /resolve to source                  │
└─────────────────────────────────────────────────────────────────────┘
```

## The one law

> **One audited epistemic organism.** Scholars work it via the workbench (review, adjudicate, attest);
> the public reads it on the site (0-JS, audited); every claim resolves to its source through the
> derivational chain. The organism keeps it honest (ceilings, gates, reconciliation, the audit trail).

## The layered access (NOT two sites)

| Layer | Who | Tools |
|---|---|---|
| **Public site** | everyone | read bibliography/themes/learning/education/scholars — 0-JS, audited |
| **Scholar workbench** | scholars (login) | agent3's `scholar_*`, `review_*`, `passage_workbench` — adjudicate/attest/publish |
| **The bridge** | `scholar_publication` | compiles reviews + attestations → JSON-LD the site serves |

So a scholar logs in → uses the workbench tools → their adjudication promotes the organism's
MACHINE_PROPOSED → ADJUDICATED → `scholar_publication` compiles it → the public site serves it as
citable records. **That is the human gate of the organism, made public.**

## The endgame surfaces (the OG site, organism-grounded)

The OG patala learning page (schools, timeline, shared foundations, geography, tantraloka resources)
is now compiled into an **audited projection**: each foundation carries an honest epistemic_ceiling +
provenance and resolves via `/resolve` to source — **not free-floating prose**.

## What makes it trustworthy (the axioms)

1. **Audit trail** — every claim resolves to source (SOURCE→…→EDUCATION).
2. **Honest ceilings** — MACHINE_PROPOSED / ENGINEERING_VALIDATED; nothing inflated.
3. **Deterministic gates** — Nyāya, cite-contract, quality, blind-assessor, reconciliation; no LLM in
   the cognition path.
4. **The flywheel** — learners-as-sensors → misconceptions → source-repair → dissolve → better teaching.
5. **Compute-on-write** — the site serves static bytes, 0-JS, ETag/304, under the perf budgets.

## The state (all real + verified)

- **Live site**: 10 pages, all HTTP 200, 0-JS (bibliography, themes, learning, education ×4, scholars).
- **API**: :8787 education index / resolve / answer.
- **Learner store**: SQLite.
- **Audit**: e2e 5/5 (claim → source), test suite 22/22.
- **Scholar surface**: a real scholar (26 contributions, 26 attestations) served on `/scholars/`.

*This is the endgame: the OG learning surface, made audited + live through the organism.*
