# S2ORC-doc2json — the paper-normalization schema reference

**What Pāṭala borrows:** the S2ORC parser: PDF → GROBID → TEI XML → structured scholarly JSON, keeping
paper metadata, body sections, and citation links. The architectural distinction to steal:
`RawDocument / StructuredDocument / BibliographyEntry / CitationMention / BodySpan / Section`.

**License:** Apache-2.0. Repos: `allenai/s2orc-doc2json`, `allenai/s2orc`.

## How Pāṭala consumes it
**PLANNED.** The schema reference for the paper-normalization layer in `06-commentarial-graph.md`.
Pāṭala keeps its own `SourceSpanLedger`, not their ontology wholesale.

## Doctrine
Steal the Raw→Structured→Bibliography→CitationMention→Section distinction; keep Pāṭala-native spans.
