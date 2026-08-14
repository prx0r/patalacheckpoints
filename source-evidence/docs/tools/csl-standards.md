# CSL-standards — dictionary lineage & standards crosswalks

**What Pāṭala borrows:** the Cologne Sanskrit Lexicon's experiments in TEI / OntoLex / FrAC / RDF /
JSON-LD / SHACL for dictionary lineage, source records, attestations, evidence classes, stable IDs,
recovery status, and machine-reviewed mappings.

**License:** varies. Repo: `sanskrit-lexicon/csl-standards`.

## Why it matters (alignment, NOT adoption)
Their vocabulary (`SourceRecord`, `sourceDictionary`, `citedWork`, `citedRange`, `evidenceClass`,
`LineageRelation`, `recoveryStatus`, `modelingNote`) maps closely onto Pāṭala concepts (`EvidenceUse`,
`SourceSpan`, `Assertion`, `Derivation`, `ReviewStatus`, `Provenance`).

**Do NOT copy their ontology wholesale.** Create `patala ↔ CSL/OntoLex/FrAC` crosswalks.

## How Pāṭala consumes it
**PLANNED.** Reference for standards adapters outward. Their own findings (TEI and OntoLex lose
different information) validate our **rich-native-first, standards-adapters-outward** architecture.

## Doctrine
Rich native canonical representation first; standards adapters outward.
