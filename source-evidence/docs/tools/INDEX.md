# External Tools Index — Pāṭala integration docs (S0.1, expanded)

*2026-08-13. Per-tool docs for the mature open infrastructure Pāṭala **borrows** (the reuse-first doctrine from
`tool-integration.md` + `tool-integration2.md`). Each covers: what Pāṭala borrows · license · API · polite
rate-limiting etiquette · how Pāṭala consumes it. Before building any scholarly infra, check this list first.*

> **Offline docs registry (all 26 tools):**
> - **`MANIFEST.json`** — the machine-readable registry (category · borrow · license · docs_url · repo · cache path).
> - **`docs-cache/INDEX.md`** — the organized, cross-referenced table (local doc ↔ cached offline docs ↔ canonical URL ↔ repo).
> - **`docs-cache/<slug>/index.md` + `SOURCE.txt`** — locally-downloaded canonical docs per tool.
> - Re-fetch any/all docs with `python3 source-evidence/evals/download_tool_docs.py [slug...]` (polite single GET).

## Parsing / extraction
| Tool | Borrows | License | Doc |
|---|---|---|---|
| GROBID | PDF → structured scholarly text (TEI, refs, coordinates) | Apache-2.0 | `tools/grobid.md` |
| Docling | general docs (DOCX/EPUB/HTML/audio/…) → normalized witness | MIT | `tools/docling.md` |
| AnyStyle | bibliography reference parser (GROBID fallback) | BSD | `tools/anystyle.md` |

## Bibliography / identity / enrichment
| Tool | Borrows | License | Doc |
|---|---|---|---|
| Zotero | bibliography CRUD, citations, `since=` sync | free client/API | `tools/zotero.md` |
| Crossref | DOI/metadata resolution | CC0 | `tools/crossref.md` |
| OpenAlex | works/authors/venues/concepts enrichment | CC0/MIT | `tools/openalex.md` |
| OpenCitations | citation graph + disambiguation | CC0/ODC | `tools/opencitations.md` |
| Unpaywall | OA full-text discovery (via PaperQA) | CC0 | `tools/unpaywall.md` |

## Retrieval / search
| Tool | Borrows | License | Doc |
|---|---|---|---|
| Tantivy | local BM25 full-text (lexical baseline) | MIT | `tools/tantivy.md` |
| PaperQA2 | Scholar Assistant RAG + metadata clients | Apache-2.0 | `tools/paperqa.md` |

## Annotation / review / UX
| Tool | Borrows | License | Doc |
|---|---|---|---|
| INCEpTION | annotation/gold/adjudication workbench (the gold lab) | Apache-2.0 | `tools/inception.md` |
| Recogito | native Workbench/Review annotation UI (W3C Web Annotation) | BSD | `tools/recogito.md` |
| Hypothesis | inline public annotation (→ ReviewProposal) | BSD client | `tools/hypothesis.md` |
| OpenReview / Kotahi / Janeway / PubPub | peer-review / publishing workflow (don't pick one yet) | MIT etc. | `tools/openreview.md` |
| COAR Notify | peer-review federation protocol (Pāṭala as a review service) | open | `tools/coar-notify.md` |
| Manubot | forkable Git-versioned scholarly essays (Vision 07) | open | `tools/manubot.md` |

## Scholar Assistant / Workbench
| Tool | Borrows | License | Doc |
|---|---|---|---|
| PaperQA2 | Scholar Assistant RAG + metadata clients | Apache-2.0 | `tools/paperqa.md` |
| SciRAG | query decomposition / gap detection / outline synthesis | open | `tools/scirrag.md` |
| STORM / Co-STORM | the "Perspective Collector" precursor (Vision 07) | Apache-2.0 | `tools/storm.md` |

## Identity / credit
| Tool | Borrows | License | Doc |
|---|---|---|---|
| RAiD | research-activity identifier (binds ORCID/ROR/outputs) | open | `tools/raid.md` |
| ORCID / ROR / CRediT | person / institution / contribution-role identity | open | (see reconciliation + scholar docs) |
| Crossref peer-review DOI | citable review objects (`isReviewOf`) | CC0 | `tools/crossref.md` |

## Packaging / benchmark
| Tool | Borrows | License | Doc |
|---|---|---|---|
| RO-Crate | portable corpus/benchmark packaging | Apache-2.0 | `tools/ro-crate.md` |
| Inspect AI | the ENTIRE benchmark runtime + scorers + scanners | MIT | `tools/inspect.md` |
| CRAG (mock-API) | reproducible frozen-snapshot benchmark env | open | `tools/crag.md` |

## Patterns / baselines / later
| Tool | Borrows | License | Doc |
|---|---|---|---|
| ORKG | structured-claims patterns (borrow, NOT backend) | MIT | `tools/orkg.md` |
| CiteVQA | Strict Epistemic Accuracy metric | open | `tools/citevqa.md` |
| S2ORC | modern-science structured corpus (later) | research | `tools/s2orc.md` |
| Valsci / SciAtlas | external baselines / retrieval providers (later) | open | `tools/valsci-sciatlas.md` |

**Pāṭala's only custom layer is the thin resolver + SourceAssertion + CorroborationEvent + the epistemic objects.**
Everything below is borrowed. **Polite usage is mandatory**: `mailto:` (OpenAlex/Crossref/Unpaywall), back off on
`429`, Zotero `since=`/batching, cursor pagination, cache aggressively, never hammer public APIs, and tests run
offline by default (`-m integration` opt-in).
