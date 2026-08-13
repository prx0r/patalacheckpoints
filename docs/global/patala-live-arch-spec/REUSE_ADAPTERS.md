# REUSE ADAPTERS

## Rule

> Borrow mature infrastructure; own only the epistemic seam.

Adapters are outbound/inbound compatibility layers. Canonical Pāṭala objects must never be redesigned merely to mirror an external schema.

| External system/standard | Use it for | Pāṭala must own |
|---|---|---|
| Vidyut | Sanskrit morphological witness | AnalysisWitness, disagreement state, canonical refs |
| Heritage | independent Sanskrit witness | same |
| GROBID | PDF→TEI extraction witness | Witness/representation/span identity + derivation |
| Docling | other document extraction | same |
| Zotero | bibliography CRUD/citation/sync | canonical scholarly identity/crosswalk/authority |
| Crossref/DataCite | metadata/PIDs | crosswalk + accepted canonical metadata |
| OpenAlex | discovery/metadata/citation context | source/evidence interpretation |
| OpenCitations | citation lineage | independence/corroboration classification |
| PaperQA2/Tantivy | candidate retrieval | SourceAssertion/EvidenceUse licensing |
| INCEpTION | annotation/adjudication UI | canonical reviewed gold objects |
| Hypothesis | annotation/review proposal UX | validated ReviewEvent |
| OpenReview/Kotahi/Janeway/OJS | workflow concepts/integration | scholarly object/review semantics |
| Inspect AI | benchmark execution | fixtures, scorers, scanners, run registry |
| Hermes | replaceable agent runtime | proposal envelope, lineage, authority boundary |
| CTS | primary-text identity compatibility | canonical Pāṭala IDs + crosswalk |
| DTS | text API interoperability | Pāṭala read model/API |
| IIIF | images/manuscripts | asset/witness identity |
| TEI | critical-edition interchange | canonical edition semantics/crosswalk |
| JATS | article ingestion/export | claim/evidence graph |
| PROV-O | provenance interchange | native provenance-required objects |
| W3C Web Annotation | resilient target/span interoperability | StableSpan identity/semantics |
| CiTO | citation relation interchange | evidence-use semantics |
| FaBiO/BIBFRAME | bibliography interchange | Pāṭala work/witness identity |
| ORCID | person identity | contributor roles/credentials/history |
| ROR | organization identity | institution relation/history |
| RO-Crate | corpus/benchmark packaging | canonical bundle contents/meaning |
| xAIF/oAMF | argument interchange | native Sanskrit-philosophy IR |

## Adapter acceptance test

For every external adapter:

1. Export canonical object A.
2. Replace adapter implementation/tool with a mock B.
3. Re-import equivalent external data.
4. Confirm canonical IDs do not change.
5. Confirm authority/review state does not change without a canonical event.
6. Confirm unsupported external fields remain external metadata.
7. Confirm tool outage cannot erase canonical state.

If these fail, the integration owns too much of Pāṭala.
