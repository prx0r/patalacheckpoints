Yes. The deeper search surfaced several things that could remove **major chunks of work**, especially on the three things you actually care about: **benchmarks, peer-review adversary, and scholar assistant/hub**.

The biggest new finding is that I would now add **Inspect AI, PaperQA2, INCEpTION, Docling and Hypothesis** to the reuse-first architecture. Those are not marginal conveniences; each can eliminate an entire Pāṭala subsystem.

## 1. Inspect AI — probably use this as the entire benchmark runtime

This is the strongest addition.

The UK AI Security Institute's **Inspect AI** is MIT-licensed and already provides datasets, agents/solvers, tools, model-provider abstraction, custom scorers, multiple scorers, model graders, sandboxing, reproducible evaluation logs, a log viewer, offline rescoring and transcript scanners. ([GitHub][1])

So I would **not build a Pāṭala benchmark framework**.

Make:

```text
TantraFact
ArgumentBench
CorroborationBench
CitationBench
PāṭalaQA
```

all **Inspect tasks**.

For example:

```text
TantraFact dataset
        ↓
Inspect Sample
        ↓
Pāṭala scholar-assistant solver
        ↓
custom scorers:
    verdict_accuracy
    span_precision
    attribution_accuracy
    scope_accuracy
    warrant_accuracy
    false_corroboration
        ↓
Inspect .eval log
        ↓
Inspect View
```

Inspect lets us have multiple custom scorers rather than crushing everything into one metric. ([Inspect][2])

That is almost perfect for the idea:

```text
SOURCE EXISTS           1
SPAN SUPPORTS           1
ATTRIBUTION             1
SCOPE                    0
WARRANT                  —
CONCLUSION               0
```

### Even better: Inspect Scanners

Inspect now has a distinct concept of **scanners** for examining transcripts for evaluation corruption such as shortcuts, errors, evaluation awareness or other behaviors that make a nominal score misleading. ([Inspect][3])

That maps beautifully onto Pāṭala's anti-cheating philosophy.

We can build:

```text
Pāṭala eval scanners

citation_laundering
scope_strengthening
unsupported_addition
source_misbinding
fake_abstention
benchmark_leak
gold_phrase_copying
unsupported_scholar_attribution
```

These don't even have to be main benchmark scores. They inspect the **reasoning/execution trace** for suspicious behavior.

Huge win.

### Inspect logs solve another problem

Every run records task/model/solver configuration and sample-level execution information, and the viewer exposes messages, scores and metadata. ([Inspect][4])

Therefore instead of inventing:

```text
benchmark_runs/
model_run_manifest.json
trace.jsonl
scores.json
viewer/
```

we can map:

```text
Pāṭala BenchmarkRun
↔
Inspect EvalLog
```

while Pāṭala retains only stable benchmark/gold IDs.

**Priority: IMMEDIATE.**

---

# 2. PaperQA2 — steal most of the Scholar Assistant retrieval engine

This is potentially the second-biggest saving.

FutureHouse's **PaperQA2** is Apache-2.0 and specifically built for high-accuracy scientific-paper RAG with citations. It already provides local full-text indexing, metadata-aware retrieval, LLM reranking/contextual summarization, iterative agentic search, document metadata resolution, caching, local/open models through LiteLLM, and citation-grounded answers. ([GitHub][5])

It even has research/evaluation around contradiction detection and scientific synthesis. ([GitHub][5])

This is close enough to our Scholar Assistant that I would **prototype Pāṭala on top of PaperQA2 before writing our own research retrieval system**.

We don't want:

```text
PaperQA answer
= Pāṭala answer
```

We want:

```text
                PaperQA2
                   │
          candidate retrieval
          contextual ranking
          evidence gathering
                   │
                   ▼
          Pāṭala SourceSpans
                   │
                   ▼
           SourceAssertions
                   │
                   ▼
           propositions / arguments
                   │
                   ▼
       epistemically constrained answer
```

PaperQA2 does:

> **find likely useful evidence.**

Pāṭala decides:

> **what that evidence actually licenses.**

That's ideal division of labor.

### Even its metadata clients may save code

PaperQA2 already has redundant metadata fetching and integrations around services such as Crossref, Semantic Scholar and Unpaywall, with metadata objects that include formatted citations, citation counts, licensing and PDF locations. ([GitHub][5])

So before writing:

```text
crossref_adapter.py
semantic_scholar_adapter.py
unpaywall_adapter.py
metadata_merge.py
```

we should inspect whether PaperQA's client layer can simply be reused.

**Priority: IMMEDIATE prototype.**

---

# 3. Tantivy — maybe don't build Elasticsearch/Qdrant-style infrastructure at all

PaperQA uses a local search stack, and the underlying **Tantivy** library is a mature MIT-licensed Lucene-inspired full-text search engine with BM25, phrase search, facets, incremental indexing, JSON fields, compressed document storage and Python bindings. ([GitHub][6])

This is appealing for Pāṭala because the scholar corpus isn't internet scale.

Potentially:

```text
SourceSpan corpus
      ↓
Tantivy:
  BM25
  phrase
  author/year filters
  scholar filters
  work filters
      ↓
dense reranker only when necessary
```

Meaning we probably don't need:

```text
Elasticsearch
OpenSearch
huge vector service
distributed search cluster
```

initially.

And importantly, BM25 gives us an **independent lexical baseline** for every retrieval benchmark.

So for CorroborationBench:

```text
BM25
vs
dense
vs
hybrid
vs
PaperQA2
vs
Pāṭala graph retrieval
```

becomes trivial.

**Priority: HIGH, but preferably reuse through PaperQA first.**

---

# 4. INCEpTION — this might eliminate most of our gold/adjudication UI work

This one is extremely relevant.

**INCEpTION** is an Apache-2.0 multi-user semantic annotation platform. It supports configurable text annotations, intelligent annotation recommendations, corpus management, knowledge bases/entity linking and programmatic workflows. It's actively maintained; its GitHub shows releases continuing into May 2026. ([GitHub][7])

Instead of immediately building Pāṭala UI for:

```text
highlight span
label speaker
label proposition
label support
correct attribution
choose argument relation
review machine annotation
```

we could adapt INCEpTION.

Imagine an **Argument Gold project**:

```text
SPAN:
Utpaladeva passage

ANNOTATION LAYERS:
speaker
commitment
proposition
premise/conclusion
inference
scope
uncertainty
source attribution
```

and a **Corroboration project**:

```text
Pāṭala proposition
+
Ratié paragraph

annotator chooses:
DIRECT_SUPPORT
PARTIAL_SUPPORT
CONTRADICTION
BACKGROUND
NON_EQUIVALENT
```

That is precisely annotation software territory.

### This could also solve benchmark creation

Instead of:

```text
researcher edits JSON manually
```

you get:

```text
machine pre-annotation
↓
INCEpTION review
↓
export
↓
Pāṭala reference object
↓
Inspect benchmark
```

That is a very mature workflow.

Pāṭala's eventual Scholar Hub UX may be much prettier, but **gold creation doesn't need the final product UI**.

This could save months.

**Priority: VERY HIGH for benchmark/gold authoring.**

---

# 5. Hypothesis — potentially borrow the actual scholar annotation UX

Hypothesis has an open-source browser annotation system: its `h` project serves the annotation API, while the BSD-licensed browser client can be embedded into webpages. ([GitHub][8])

This is different from INCEpTION.

I see:

```text
INCEpTION
= controlled benchmark / adjudication environment

Hypothesis
= lightweight public scholarly annotation
```

For the Scholar Hub, imagine scholars highlighting an IPVV or essay passage directly:

```text
highlight
↓
comment
↓
Pāṭala adapter
↓
ReviewEvent candidate
```

Or:

```text
"this citation doesn't support this claim"
```

attached directly to the rendered claim.

I would **not make Hypothesis annotations canonical ReviewEvents automatically**.

Instead:

```text
Hypothesis Annotation
↓
ReviewProposal
↓
Pāṭala ReviewEvent
```

after validation/identity resolution.

That potentially saves us from building a sophisticated text-selection/commenting UI.

**Priority: PILOT, not core yet.**

---

# 6. Docling — use beside GROBID, not instead of it

GROBID remains the better specialist for scholarly bibliographic extraction. It handles references, citation contexts, bibliographic consolidation, full text, figures/tables and PDF coordinates. ([GitHub][9])

But **Docling** is MIT-licensed and handles a much wider document world:

```text
PDF
DOCX
PPTX
XLSX
HTML
EPUB
audio
WebVTT
images
LaTeX
email
JATS
```

with layout, tables, formulas, reading order, images and a unified lossless document representation. ([GitHub][10])

So modify the source layer to:

```text
                    INPUT
                      │
       ┌──────────────┴──────────────┐
       ▼                             ▼
 scholarly PDF                    everything else
       │                             │
    GROBID                        Docling
       │                             │
       └──────────────┬──────────────┘
                      ▼
               normalized witness
```

For future Pāṭala this matters enormously because you'll have:

* journal articles;
* books/EPUBs;
* lecture transcripts;
* scholar presentations;
* interview audio;
* manuscript images;
* education content.

Don't write format-specific loaders.

**Priority: HIGH as fallback/general adapter.**

---

# 7. AnyStyle — tiny useful fallback for horrible bibliographies

**AnyStyle** is a BSD-style licensed bibliographic reference parser with CLI/API support and trainable models. It handles raw citation strings and can export structured formats including CSL-style data. ([GitHub][11])

GROBID already handles references well, so don't make this primary.

Use:

```text
GROBID reference parser
        ↓ failed/low confidence?
AnyStyle
        ↓
Crossref/OpenAlex resolve
```

Particularly valuable for:

* old humanities bibliographies;
* pasted bibliography files;
* weird footnote-style references;
* bibliographies outside PDFs.

Very little integration effort.

**Priority: CHEAP WIN.**

---

# 8. S2ORC — don't ingest it, but exploit it later for the science side

AllenAI's **S2ORC** is a large general-purpose structured scientific literature corpus, and its current distribution is available through the Semantic Scholar API/bulk data system. ([GitHub][12])

It won't solve Sanskrit humanities scholarship.

But when Pāṭala expands into:

```text
Friston
Seth
Solms
Levin
consciousness science
neuroscience
```

there is no reason to PDF-ingest that literature manually at the same scale.

Keep:

```text
Sanskrit/humanities:
our curated corpus

modern science:
S2ORC / Semantic Scholar substrate
```

then normalize both into `SourceAssertion`.

**Priority: LATER.**

---

# 9. CiteVQA has a metric we should steal conceptually

A newer benchmark, **CiteVQA**, explicitly separates:

```text
answer correctness
```

from:

```text
citation/evidence correctness
```

and defines a strict attributed-accuracy measure requiring both to be valid. ([GitHub][13])

That is extremely Pāṭala-like.

For PāṭalaQA I'd define:

[
PAA = AnswerCorrect \land AttributionCorrect
]

and potentially:

[
PEA =
AnswerCorrect
\land EvidenceCorrect
\land AttributionCorrect
\land ScopePreserved
]

Call it something like:

```text
Strict Epistemic Accuracy
```

A model shouldn't get full credit because the answer happens to be correct while citing the wrong evidence.

That principle should run through **all** our benchmarks.

**Priority: BENCHMARK DESIGN.**

---

# 10. CRAG's mock-API pattern is worth stealing

Meta's open CRAG benchmark includes mock APIs so retrieval/knowledge access can be evaluated in a reproducible controlled environment rather than against a changing live web. ([GitHub][14])

We could do the same for Pāṭala benchmarks.

Instead of giving benchmark agents unrestricted access to our live corpus:

```text
TantraFact benchmark container
│
├── mock_source_api
├── mock_bibliography_api
├── resolve_span()
└── search_sources()
```

Each model gets **exactly the same corpus snapshot**.

That's very useful for:

* preventing retrieval drift;
* preventing benchmark contamination from current product state;
* reproducible papers;
* externally releasing benchmarks without releasing restricted source PDFs.

Very strong pattern.

**Priority: WHEN TANTRAFACT v0 BEGINS.**

---

# 11. Inspect + CRAG together give us the benchmark infrastructure almost for free

This is the architecture I now want:

```text
                    TANTRAFACT DATA
                           │
                    frozen RO-Crate
                           │
                           ▼
                  Mock Pāṭala Source API
                           │
                           ▼
                    Inspect AI Task
                     /            \
                 model            tools
                   │                │
                   └──── answer ────┘
                           │
                     custom scorers
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
     verdict           evidence          process
     accuracy           accuracy          failures
                           │
                        scanners
                           │
                       EvalLog
                           │
                     Inspect View
```

We would be insane to build all of that ourselves when the pieces already exist.

---

# 12. PaperQA2 itself gives us a baseline adversary

Don't only reuse PaperQA2 in production.

Make it a benchmark baseline.

For every:

```text
PāṭalaQA
CorroborationBench
CitationBench
```

run:

```text
BM25
PaperQA2
generic frontier model + RAG
Pāṭala
```

Then we can make legitimate empirical claims about what the epistemic graph adds.

For example:

```text
PaperQA2:
answer correct                 82%
citation correct               75%
scope preserved                61%

Pāṭala:
answer correct                 80%
citation correct               91%
scope preserved                89%
```

Hypothetical numbers obviously, but *that* is the research story.

Pāṭala may not initially win ordinary answer accuracy.

Its thesis is that it should win **epistemic fidelity**.

---

# 13. INCEpTION + Inspect creates a killer gold→eval pipeline

This may be the cleanest reuse architecture of all:

```text
                 MACHINE PROPOSAL
                        │
                        ▼
                    INCEpTION
              annotation/adjudication
                        │
                        ▼
                canonical gold JSON
                        │
                        ▼
                    Inspect AI
                  benchmark runtime
                        │
                        ▼
                models / Pāṭala
                        │
                        ▼
               scorer + scanners
```

Pāṭala only defines:

```text
annotation schema
benchmark task
epistemic scorers
```

not the UI or evaluation framework.

Fantastic division of labor.

---

# 14. Another thing: use existing eval registries to publish Pāṭala benchmarks

Inspect Evals now has a community eval registry where external evaluation implementations can be registered rather than merged directly into its core. ([GitHub][15])

That gives us a possible future distribution route:

```text
pip install patala-evals

inspect eval patala_evals/tantrafact
inspect eval patala_evals/argumentbench
```

and possibly list those in the wider Inspect ecosystem.

That is much better than:

```text
download our weird custom benchmark runner
```

for academic uptake.

---

# 15. Valsci is interesting specifically as an adversarial baseline

I found an open-source project called **Valsci** that performs automated scientific claim verification using literature retrieval and structured evidence reports. It supports OpenAI-compatible models and batch claim checking. ([GitHub][16])

I would **not build on it** because its epistemic assumptions—including bibliometric credibility scoring—don't align cleanly with Pāṭala.

But it's highly useful as:

```text
external competitor baseline
```

for CorroborationBench.

Run:

```text
Valsci
PaperQA2
generic RAG
Pāṭala
```

on the same claims.

If Pāṭala's more explicit attribution/scope/defeater machinery actually matters, it should show up.

---

# 16. SciAtlas is another useful comparator / retrieval provider

**SciAtlas** exposes graph-aware scholarly retrieval over papers, authors, institutions, venues, citations and research topics, and its client can emit reusable machine-readable research artifacts. ([GitHub][17])

Again:

```text
don't make backend
```

but potentially:

```text
external research retrieval provider
```

for the modern-science side.

It gives us another way of asking:

> does explicit Pāṭala epistemics improve on a good graph-aware research retrieval system?

---

# Updated ruthless reuse stack

I would now freeze this as the expanded doctrine:

| Pāṭala problem                           | Use this                               |
| ---------------------------------------- | -------------------------------------- |
| scholarly PDF parsing                    | **GROBID**                             |
| arbitrary documents                      | **Docling**                            |
| ugly bibliography fallback               | **AnyStyle**                           |
| bibliography management                  | **Zotero**                             |
| full-text BM25                           | **Tantivy / PaperQA2**                 |
| scientific-paper RAG                     | **PaperQA2**                           |
| publication metadata                     | **Crossref / OpenAlex**                |
| citation graph                           | **OpenCitations**                      |
| OA discovery                             | **PaperQA metadata stack / Unpaywall** |
| annotation/gold creation                 | **INCEpTION**                          |
| inline public annotation                 | **Hypothesis**                         |
| benchmark runtime                        | **Inspect AI**                         |
| benchmark trace analysis                 | **Inspect Scanners**                   |
| eval UI/logging                          | **Inspect View / EvalLog**             |
| reproducible retrieval env               | **CRAG mock-API pattern**              |
| corpus/benchmark export                  | **RO-Crate**                           |
| review workflow                          | **OpenReview**                         |
| scientific corpus later                  | **S2ORC**                              |
| research RAG baseline                    | **PaperQA2**                           |
| claim verifier baseline                  | **Valsci**                             |
| graph-retrieval baseline                 | **SciAtlas**                           |
| citation-faithfulness metric inspiration | **CiteVQA**                            |

And Pāṭala builds basically:

```text
SourceAssertion
CorroborationEvent
SemanticAlignment
Proposition
Commitment
Argument
ArgumentAudit
Crux
ArgumentSynthesis
ReviewEvent
epistemic dependency propagation

+

Pāṭala-specific benchmark datasets/scorers
Pāṭala-specific scholar UX
```

That is it.

## The next three integrations I'd actually prototype

Not 15 things at once.

**A. Inspect AI first.** Port the existing tiny Argument benchmark and corruption tests into one Inspect task. If it feels natural, freeze Inspect as the evaluation runtime.

**B. PaperQA2 second.** Point it at ~20 of your Ratié/Sanderson documents and compare its retrieval/evidence output to the current Pāṭala retrieval. Steal its metadata/evidence/search machinery wherever useful.

**C. INCEpTION third.** Load 5 Argument Gold objects or 20 SourceAssertion/Corroboration examples and see whether its annotation UI can become the gold-building/adjudication workbench.

If all three work, we eliminate three huge engineering categories:

```text
custom benchmark framework     ❌
custom scholarly RAG engine    ❌
custom annotation/gold UI      ❌
```

and can spend almost everything on the genuinely novel part:

> **Can a machine preserve warranted authority through source → interpretation → claim → argument → synthesis → review → explanation, and can we measure exactly where it fails?**

That's the part worth building.

[1]: https://github.com/UKGovernmentBEIS/inspect_ai?utm_source=chatgpt.com "GitHub - UKGovernmentBEIS/inspect_ai: Inspect: A framework for large language model evaluations · GitHub"
[2]: https://inspect.aisi.org.uk/scorers.html?utm_source=chatgpt.com "Scorers – Inspect"
[3]: https://inspect.aisi.org.uk/scanners.html?utm_source=chatgpt.com "Scanners – Inspect"
[4]: https://inspect.aisi.org.uk/eval-logs.html?utm_source=chatgpt.com "Log Files – Inspect"
[5]: https://github.com/future-house/paper-qa?utm_source=chatgpt.com "GitHub - Future-House/paper-qa: High accuracy RAG for answering questions from scientific documents with citations · GitHub"
[6]: https://github.com/quickwit-oss/tantivy?utm_source=chatgpt.com "GitHub - quickwit-oss/tantivy: Tantivy is a full-text search engine library inspired by Apache Lucene and written in Rust · GitHub"
[7]: https://github.com/inception-project/inception?utm_source=chatgpt.com "GitHub - inception-project/inception: INCEpTION provides a semantic annotation platform offering intelligent annotation assistance and knowledge management. · GitHub"
[8]: https://github.com/hypothesis/h?utm_source=chatgpt.com "GitHub - hypothesis/h: Annotate with anyone, anywhere. · GitHub"
[9]: https://github.com/grobidOrg/grobid?utm_source=chatgpt.com "GitHub - grobidOrg/grobid: A machine learning software for extracting information from scholarly documents · GitHub"
[10]: https://github.com/docling-project/docling?utm_source=chatgpt.com "GitHub - docling-project/docling: Get your documents ready for gen AI · GitHub"
[11]: https://github.com/inukshuk/anystyle?utm_source=chatgpt.com "GitHub - inukshuk/anystyle: Fast citation reference parsing · GitHub"
[12]: https://github.com/allenai/s2orc/blob/master/README.md?utm_source=chatgpt.com "s2orc/README.md at master · allenai/s2orc · GitHub"
[13]: https://github.com/opendatalab/CiteVQA?utm_source=chatgpt.com "GitHub - opendatalab/CiteVQA · GitHub"
[14]: https://github.com/facebookresearch/CRAG?utm_source=chatgpt.com "GitHub - facebookresearch/CRAG: Comprehensive benchmark for RAG · GitHub"
[15]: https://github.com/UKGovernmentBEIS/inspect_evals?utm_source=chatgpt.com "GitHub - UKGovernmentBEIS/inspect_evals: Collection of evals for Inspect AI · GitHub"
[16]: https://github.com/bricee98/Valsci?utm_source=chatgpt.com "GitHub - bricee98/Valsci: Validate scientific claims en masse. · GitHub"
[17]: https://github.com/zjunlp/SciAtlas?utm_source=chatgpt.com "GitHub - zjunlp/SciAtlas: A Large-Scale Knowledge Graph for Automated Scientific Research · GitHub"
