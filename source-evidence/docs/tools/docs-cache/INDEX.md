# External Tools Docs — offline registry + docs cache

*2026-08-12. Machine-readable source: `MANIFEST.json`. For each tool: what Pāṭala borrows, license, canonical docs URL, repository, and the locally-downloaded docs. This is the **organized reference** for the S0.1 reuse-first stack; every tool is borrowed, none is built.*

> **Usage:** `python3 source-evidence/evals/download_tool_docs.py` re-downloads/caches any tool's docs (polite single GET). Cached docs are offline snapshots for reference only — never canonical state.

## Parsing

| Tool | Borrows | License | Docs (local) | Cached (offline) | Canonical URL | Repo |
|---|---|---|---|---|---|---|
| **anystyle** | bibliography reference parser (GROBID fallback) | BSD | `anystyle.md` | `docs-cache/anystyle/` | [site](https://anystyle.io) | [repo](https://github.com/inukshuk/anystyle) |
| **docling** | general docs (DOCX/EPUB/HTML/audio/…) → normalized witness | MIT | `docling.md` | `docs-cache/docling/` | [site](https://github.com/docling-project/docling) | [repo](https://github.com/docling-project/docling) |
| **grobid** | PDF → structured scholarly text (TEI, references, citation contexts, sections, coordinates) | Apache-2.0 | `grobid.md` | `docs-cache/grobid/` | [site](https://grobid.readthedocs.io) | [repo](https://github.com/kermitt2/grobid) |

## Bibliography

| Tool | Borrows | License | Docs (local) | Cached (offline) | Canonical URL | Repo |
|---|---|---|---|---|---|---|
| **crossref** | DOI/metadata resolution + review DOI registration (isReviewOf) | CC0 | `crossref.md` | `docs-cache/crossref/` | [site](https://api.crossref.org) | [repo](https://gitlab.com/crossref) |
| **openalex** | works/authors/venues/concepts enrichment | CC0/MIT | `openalex.md` | `docs-cache/openalex/` | [site](https://docs.openalex.org) | [repo](https://github.com/ourresearch/openalex) |
| **opencitations** | citation graph + disambiguation | CC0/ODC | `opencitations.md` | `docs-cache/opencitations/` | [site](https://opencitations.net) | [repo](https://github.com/opencitations) |
| **raid** | research-activity identifier (binds contributors/orgs/outputs/PIDs) | open | `raid.md` | `docs-cache/raid/` | [site](https://www.raid.org) | [repo](https://github.com/au-research/raid-metadata) |
| **unpaywall** | OA full-text discovery | CC0 | `unpaywall.md` | `docs-cache/unpaywall/` | [site](https://unpaywall.org) | [repo](https://github.com/ourresearch/unpaywall) |
| **zotero** | bibliography CRUD, citations, `since=` sync, CSL/BibTeX/TEI export | free client/API | `zotero.md` | `docs-cache/zotero/` | [site](https://www.zotero.org/support/dev/web_api/v3/basics) | [repo](https://github.com/zotero) |

## Retrieval

| Tool | Borrows | License | Docs (local) | Cached (offline) | Canonical URL | Repo |
|---|---|---|---|---|---|---|
| **crag** | corrective RAG (retriever + grader) pattern | MIT | `crag.md` | `docs-cache/crag/` | [site](https://github.com/langchain-ai/langgraph) | [repo](https://github.com/langchain-ai/langgraph) |
| **paperqa** | Scholar Assistant RAG + metadata clients (Crossref/OpenAlex/Unpaywall) | Apache-2.0 | `paperqa.md` | `docs-cache/paperqa/` | [site](https://github.com/future-house/paper-qa) | [repo](https://github.com/future-house/paper-qa) |
| **s2orc** | full-text corpus of 100M+ OA papers (source of GROBID XML) | CC0 (corpus) | `s2orc.md` | `docs-cache/s2orc/` | [site](https://github.com/allenai/s2orc) | [repo](https://github.com/allenai/s2orc) |
| **scirrag** | query decomposition, citation-graph expansion, gap detection | open | `scirrag.md` | `docs-cache/scirrag/` | [site](https://github.com/yale-nlp/SciRAG) | [repo](https://github.com/yale-nlp/SciRAG) |
| **tantivy** | local BM25 full-text (lexical baseline) | MIT | `tantivy.md` | `docs-cache/tantivy/` | [site](https://docs.rs/tantivy) | [repo](https://github.com/quickwit-oss/tantivy) |

## Annotation

| Tool | Borrows | License | Docs (local) | Cached (offline) | Canonical URL | Repo |
|---|---|---|---|---|---|---|
| **hypothesis** | inline public annotation (→ ReviewProposal) | BSD client | `hypothesis.md` | `docs-cache/hypothesis/` | [site](https://h.readthedocs.io) | [repo](https://github.com/hypothesis/client) |
| **inception** | annotation/gold/adjudication workbench (the gold lab) | Apache-2.0 | `inception.md` | `docs-cache/inception/` | [site](https://inception-project.github.io) | [repo](https://github.com/inception-project/inception) |
| **orkg** | scholarly KG patterns (precedent/interop, NOT backend) | open | `orkg.md` | `docs-cache/orkg/` | [site](https://orkg.org) | [repo](https://gitlab.com/TIBHannover/orkg) |
| **recogito** | native Workbench/Review annotation UI (W3C Web Annotation) | BSD | `recogito.md` | `docs-cache/recogito/` | [site](https://recogito.github.io) | [repo](https://github.com/recogito/text-annotator-js) |

## Evaluation

| Tool | Borrows | License | Docs (local) | Cached (offline) | Canonical URL | Repo |
|---|---|---|---|---|---|---|
| **inspect** | THE benchmark runtime (datasets/agents/scorers/scanners/EvalLog/viewer) | MIT | `inspect.md` | `docs-cache/inspect/` | [site](https://inspect.aisi.org.uk) | [repo](https://github.com/UKGovernmentBEIS/inspect_ai) |

## Workflow

| Tool | Borrows | License | Docs (local) | Cached (offline) | Canonical URL | Repo |
|---|---|---|---|---|---|---|
| **coar-notify** | peer-review federation protocol (Pāṭala as a review service) | open | `coar-notify.md` | `docs-cache/coar-notify/` | [site](https://github.com/coar-notify/coarnotifypy) | [repo](https://github.com/COAR-Notify/notify) |
| **manubot** | forkable Git-versioned scholarly essays (Vision 07) | open | `manubot.md` | `docs-cache/manubot/` | [site](https://manubot.org) | [repo](https://github.com/manubot/manubot) |
| **openreview** | review/submission workflow (with Kotahi/Janeway/PubPub) | MIT | `openreview.md` | `docs-cache/openreview/` | [site](https://docs.openreview.net) | [repo](https://github.com/openreview/openreview-api) |

## Packaging

| Tool | Borrows | License | Docs (local) | Cached (offline) | Canonical URL | Repo |
|---|---|---|---|---|---|---|
| **ro-crate** | portable corpus/benchmark packaging | Apache-2.0 | `ro-crate.md` | `docs-cache/ro-crate/` | [site](https://www.researchobject.org/ro-crate/) | [repo](https://github.com/ResearchObject/ro-crate-py) |

## Assistant

| Tool | Borrows | License | Docs (local) | Cached (offline) | Canonical URL | Repo |
|---|---|---|---|---|---|---|
| **storm** | perspective-guided exploration / Co-STORM mind-map (Vision 07) | MIT | `storm.md` | `docs-cache/storm/` | [site](https://github.com/stanford-oval/storm) | [repo](https://github.com/stanford-oval/storm) |

## Watch

| Tool | Borrows | License | Docs (local) | Cached (offline) | Canonical URL | Repo |
|---|---|---|---|---|---|---|
| **citevqa** | citation-verification / visual QA research precedent | open | `citevqa.md` | `docs-cache/citevqa/` | [site](https://github.com/opendatalab/CiteVQA) | [repo](https://github.com/princeton-nlp/ScienceQA) |
| **valsci-sciatlas** | concepts/claims over scholarly corpora (watch/steal-ideas) | open | `valsci-sciatlas.md` | `docs-cache/valsci-sciatlas/` | [site](https://github.com/p-v-o-s/pioneer-valley-open-science.github.com) | [repo](https://github.com/Value-of-science/val-sci) |

---

## How to add a tool
1. Add an entry to `MANIFEST.json` (category, borrow, license, docs_url, repo, local_doc, docs_cache).
2. Add the per-tool integration doc in `source-evidence/docs/tools/<slug>.md`.
3. Run `python3 source-evidence/evals/download_tool_docs.py <slug>` to cache the canonical docs.
4. Re-run this generator to refresh this index.