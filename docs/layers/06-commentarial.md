# LAYER 06 — COMMENTARIAL GRAPH (secondary scholarship)

*Part of the `globalglobal.md` spine. Turns papers into a computable commentary layer.*

## 1. What it is
The secondary-scholarship layer: turns thousands of papers (Ratié, Torella, Dyczkowski, Sanderson) into
a **computable commentary layer** over the primary-source graph — not a pile of PDFs, not just RAG
embeddings.

## 2. Purpose
Preserve the full scholarly debate: PRIMARY SAYS X ≠ RATIÉ INTERPRETS X ≠ PĀṬALA ACCEPTS X. Enable
"research once; render repeatedly" into Ask/Learn/Essays/Video/Scholar pages without intellectual drift.

## 3. External tools used (planned)
Docling/GROBID (document substrate) · SocraticKG (QA-intermediate) · ORKG (contribution abstraction) ·
DSPy (measurable extraction) · RefChecker/CIBER/GraphCheck/CLAIMCHECK/RARR (verifier ensemble) ·
geometricengine hyperedge pattern. See `external-tools.md` + `githubclones.md`.

## 4. Data
- `ScholarContributionPacket` — Questions/Positions/Interpretations/Arguments/EvidenceUses/Definitions/
  Distinctions/Objections/Agreements/Disagreements/ResearchGaps/Quotes.
- `ScholarPosition` — one scholar's scoped claim (proposition, modality, source_span, evidence_used).
- `AttributionEvent` — scholar credit (DIRECT_QUOTE / PARAPHRASED_POSITION / EVIDENCE_SOURCE / ...).
- `Quote`/`Paraphrase` — exact-vs-paraphrased separation. `RightsState` — copyright/quote/derivative.

## 5. Processes
```
paper → 0 rights/identity → 1 structure → 2 scholarly interrogation (QA) → 3 atomic extraction →
4 argument reconstruction → 5 primary-source alignment → 6 scholar alignment → 7 canonicalization →
8 adversarial pass → 9 ScholarContributionPacket → 10 graph proposal (MACHINE_PROPOSED) → 11 surfaces
```
Verifier ensemble checks evidence, not just extraction. Essay = a `Synthesis` graph projection, not
saved prose.

## 6. Implementations
**STATUS: design only — not yet built.** Raw research: `docs-cache/commentarialgraph-research.md`,
`externalpaper-research.md`. The engines will be built under this layer; see `docs/process/06-commentarial-graph.md`.

## 7. Docs
- `docs/process/06-commentarial-graph.md` — the detailed layer guide.
- `docs/global/globalglobal.md` — the spine.
- `docs/process/githubclones.md` — SocraticKG, ORKG, blogengine (Research Object), geometricengine.
