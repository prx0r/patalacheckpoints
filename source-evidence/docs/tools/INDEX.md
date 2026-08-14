# External Tools Index — Pāṭala integration docs (all 42 tools)

*2026-08-14. Per-tool docs for the mature open infrastructure Pāṭala **borrows** (reuse-first doctrine).
Every tool has a `.md` doc (this index) + a machine-readable entry in `MANIFEST.json` (+ the
status board in `docs/process/external-tools.md`). Each doc covers: what Pāṭala borrows · license · API ·
polite etiquette · how Pāṭala consumes it · **integration status**. Before building any scholarly infra,
check this list first.*

> **Offline docs registry (all 42 tools):**
> - **`MANIFEST.json`** — the machine-readable registry (category · borrow · license · docs_url · repo ·
>   **status** · used_in · notes). Validated by `MANIFEST.schema.json`.
> - **`INDEX.md`** — this file (human index grouped by category).
> - **`docs-cache/<slug>/`** — locally-downloaded canonical docs per tool.
> - **`docs/process/external-tools.md`** — the status board + 6 adapter contracts.
>
> **Status legend:** INTEGRATED (prod+tested) · WIRED (working adapter) · PARTIAL (stub) ·
> DOCS_ONLY (documented, no code) · PLANNED (adopt later) · WATCH (audited, not adopted) · NOT_USED.

## Parsing / extraction
| Tool | Borrows | License | Doc | Status |
|---|---|---|---|---|
| GROBID | PDF → structured scholarly text (TEI, refs, coordinates) | Apache-2.0 | `grobid.md` | PARTIAL |
| Docling | general docs (DOCX/EPUB/HTML/audio/…) → normalized witness | MIT | `docling.md` | DOCS_ONLY |
| AnyStyle | bibliography reference parser (GROBID fallback) | BSD | `anystyle.md` | DOCS_ONLY |

## Bibliography / identity / enrichment
| Tool | Borrows | License | Doc | Status |
|---|---|---|---|---|
| Zotero | bibliography CRUD, citations, `since=` sync | free client/API | `zotero.md` | DOCS_ONLY |
| Crossref | DOI/metadata resolution | CC0 | `crossref.md` | **WIRED** |
| OpenAlex | works/authors/venues/concepts enrichment | CC0/MIT | `openalex.md` | **WIRED** |
| OpenCitations | citation graph + disambiguation | CC0/ODC | `opencitations.md` | PARTIAL |
| Unpaywall | OA full-text discovery | CC0 | `unpaywall.md` | DOCS_ONLY |
| RAiD | research-activity identifier (binds ORCID/ROR/outputs) | open | `raid.md` | DOCS_ONLY |

## Retrieval / search
| Tool | Borrows | License | Doc | Status |
|---|---|---|---|---|
| Tantivy | local BM25 full-text (lexical baseline) | MIT | `tantivy.md` | NOT_USED |
| PaperQA2 | Scholar Assistant RAG + metadata clients | Apache-2.0 | `paperqa.md` | DOCS_ONLY |
| SciRAG | query decomposition / gap detection / outline synthesis | open | `scirrag.md` | DOCS_ONLY |
| S2ORC | modern-science structured corpus (later) | research | `s2orc.md` | NOT_USED |
| CRAG | corrective RAG (retriever + grader) pattern | open | `crag.md` | DOCS_ONLY |

## Annotation / review / UX
| Tool | Borrows | License | Doc | Status |
|---|---|---|---|---|
| INCEpTION | annotation/gold/adjudication workbench (the gold lab) | Apache-2.0 | `inception.md` | DOCS_ONLY |
| INCEpTION recommender | external recommender: AI → scholar accept/modify/reject → gold | Apache-2.0 | `inception-recommender.md` | PLANNED |
| Recogito | native Workbench/Review annotation UI (W3C Web Annotation) | BSD | `recogito.md` | DOCS_ONLY |
| Hypothesis | inline public annotation (→ ReviewProposal) | BSD client | `hypothesis.md` | DOCS_ONLY |
| OpenReview / Kotahi / Janeway / PubPub | peer-review / publishing workflow | MIT etc. | `openreview.md` | DOCS_ONLY |
| COAR Notify | peer-review federation protocol | open | `coar-notify.md` | DOCS_ONLY |
| Manubot | forkable Git-versioned scholarly essays | open | `manubot.md` | DOCS_ONLY |
| BDRC RDF editor | SHACL-driven scholar edit forms + deterministic serialization | varies | `buda-rdf-editor.md` | PLANNED |
| Sangrahaka | distributed KG annotation + querying (Sanskrit+CL+KG prior art) | varies | `sangrahaka.md` | WATCH |

## Scholar Assistant / Workbench
| Tool | Borrows | License | Doc | Status |
|---|---|---|---|---|
| PaperQA2 | Scholar Assistant RAG + metadata clients | Apache-2.0 | `paperqa.md` | DOCS_ONLY |
| SciRAG | query decomposition / gap detection | open | `scirrag.md` | DOCS_ONLY |
| STORM / Co-STORM | perspective exploration / mind-map (Vision 07) | Apache-2.0 | `storm.md` | DOCS_ONLY |

## Evaluation / benchmark
| Tool | Borrows | License | Doc | Status |
|---|---|---|---|---|
| Inspect AI | the ENTIRE benchmark runtime + scorers + scanners | MIT | `inspect.md` | **INTEGRATED** |
| ORKG | structured-claims patterns (borrow, NOT backend) | MIT | `orkg.md` | DOCS_ONLY |
| CiteVQA | Strict Epistemic Accuracy metric | open | `citevqa.md` | DOCS_ONLY |
| Valsci / SciAtlas | concepts/claims over corpora (watch/steal-ideas) | open | `valsci-sciatlas.md` | DOCS_ONLY |

## Packaging / publishing
| Tool | Borrows | License | Doc | Status |
|---|---|---|---|---|
| RO-Crate | portable corpus/benchmark packaging | Apache-2.0 | `ro-crate.md` | DOCS_ONLY |
| TEI Publisher | TEI data → scholarly publication interface | GPL | `tei-publisher.md` | DOCS_ONLY |
| Nanopub | publish Assertions as machine-addressable, signed objects | protocol | `nanopub.md` | PLANNED |

## Linguistic (Sanskrit engine + corpus priors)
| Tool | Borrows | License | Doc | Status |
|---|---|---|---|---|
| **Vidyut** | Sanskrit linguistic engine: cheda (segmentation), prakriya (morphology), kosha (inflection), lipi (transliteration), sandhi, chandas (meter) | Apache-2.0 | `vidyut.md` | **INTEGRATED** |
| Ambuda DCS | 650k+ annotated Sanskrit sentences (~250 texts) → linguistic priors | varies | `ambuda-dcs.md` | PLANNED |
| DCS↔SH alignment | cross-parser disagreement dataset → consensus/uncertainty | GPL-3.0 | `dcs-sh-alignment.md` | PLANNED |
| Sanskrit-util | shared SLP1/IAST/Devanagari normalization | varies | `sanskrit-util.md` | PLANNED |
| Aksharamukha | 120 scripts + 21 romanization systems | MIT | `aksharamukha.md` | PLANNED |

## Lexical (dictionaries)
| Tool | Borrows | License | Doc | Status |
|---|---|---|---|---|
| C-SALT / CSL-orig | 45 dictionary collections (MW, PWG, PWK, Apte…) → lexical evidence graph | varies | `csl-orig.md` | PLANNED |
| CSL-standards | TEI/OntoLex/FrAC crosswalks for dictionary lineage + attestations | varies | `csl-standards.md` | PLANNED |

## Ontology (identity reference)
| Tool | Borrows | License | Doc | Status |
|---|---|---|---|---|
| BDRC owl-schema | Person/Work/Instance/Place/Role ontology (RDF, JSON-LD, SKOS) | CC0 | `buda-owl-schema.md` | PLANNED |

## Argument / education
| Tool | Borrows | License | Doc | Status |
|---|---|---|---|---|
| Argdown | human-readable argument syntax → visual maps | MIT | `argdown.md` | PLANNED |
| Pramana-NLP | Sanskrit pramāṇa corpus (Nyāya/Buddhist logic) + cleaning pipeline | varies | `pramana-nlp.md` | WATCH |

## Watch / later
| Tool | Borrows | License | Doc | Status |
|---|---|---|---|---|
| VedaWeb / Tekst | info architecture: text/token/annotation/lexical-link/metrical | varies | `vedaweb-tekst.md` | WATCH |
| Pramana-NLP (Vātāyana) | intertextuality search interface | varies | `pramana-nlp.md` | WATCH |

## Paper → commentarial graph (the scholarly compiler, see 06-commentarial-graph.md)
| Tool | Borrows | License | Doc | Status |
|---|---|---|---|---|
| Marker | documents → Markdown/JSON (difficult PDFs) | GPL-3.0/model | `marker.md` | PLANNED |
| Nougat | academic-document OCR (equations/tables) | CC-BY-NC | `nougat.md` | PLANNED |
| S2ORC-doc2json | PDF→GROBID→TEI→structured scholarly JSON (schema ref) | Apache-2.0 | `s2orc-doc2json.md` | PLANNED |
| SocraticKG | QA-mediated KG construction | Apache-2.0 | `socratickg.md` | PLANNED |
| DSPy | typed extraction programs with measurable outputs | MIT | `dspy.md` | PLANNED |
| RefChecker | atomic claim decomposition + fidelity | Apache-2.0 | `refchecker.md` | PLANNED |
| CIBER | deliberate refutation retrieval | research | `ciber.md` | PLANNED |
| GraphCheck | graph-vs-graph relational drift | research | `graphcheck.md` | PLANNED |
| CLAIMCHECK | claim-targeted critique (scholar objections) | research | `claimcheck.md` | PLANNED |
| RARR | retrieve → assess → revise unsupported output | Apache-2.0 | `rarr.md` | PLANNED |

## Verification plane (external methods test Pāṭala — see 08-verification-plane.md)
| Tool | Borrows | License | Doc | Status |
|---|---|---|---|---|
| AlignScore | cheap semantic entailment/consistency witness | MIT | `alignscore.md` | PLANNED |
| FActScore | atomic factual precision | MIT | `factscore.md` | PLANNED |
| GlossLM | 450k IGT glossing corpus (T1 benchmark paradigm) | Apache-2.0 | `glosslm.md` | PLANNED |
| ByT5-Sanskrit | Sanskrit segmentation/lemmatization/tagging + OCR post-corr | unclear | `byt5-sanskrit.md` | PLANNED |
| StructEval | structured-output eval methodology (borrow only) | Apache-2.0 | `structeval.md` | PLANNED |
| conformal prediction | calibrated abstention / risk control | method | `conformal-prediction.md` | PLANNED |
| metamorphic testing | invariant-preserving perturbation tests | method | `metamorphic-testing.md` | PLANNED |

**Note:** these compose into the verification plane — Inspect (runtime) + RefChecker/FActScore (atomic
decomposition) + AlignScore (cheap entailment) + conformal (abstention) + metamorphic (mutation). They
TEST Pāṭala; they never define Pāṭala truth.

**Note:** the verifier ensemble (RefChecker/CIBER/GraphCheck/CLAIMCHECK/RARR) forms the evidence-check
layer over the commentarial graph; DSPy makes extraction measurable; SocraticKG provides the QA-intermediate
representation. Ecosystem repos (blogengine/geometricengine/Ochema) live in `docs/process/githubclones.md`.

---

**Pāṭala's only custom layer is the thin resolver + SourceAssertion + CorroborationEvent + the epistemic
objects.** Everything below is borrowed. **Polite usage is mandatory:** `mailto:` (OpenAlex/Crossref/
Unpaywall), back off on `429`, Zotero `since=`/batching, cursor pagination, cache aggressively, never
hammer public APIs, tests run offline by default (`-m integration` opt-in).

> **Also see:** `docs/process/external-tools.md` (status board + 6 adapter contracts) ·
> `docs/process/githubclones.md` (researcher-built repos to raid) · `MANIFEST.json` (machine-readable).
