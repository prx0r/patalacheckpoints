# PaperQA2 — the Scholar Assistant retrieval engine + metadata clients

**What Pāṭala borrows:** high-accuracy scientific-paper RAG with citations — local full-text indexing,
metadata-aware retrieval, LLM reranking/contextual summarization, iterative agentic search, document metadata
resolution, caching, local/open models (LiteLLM), citation-grounded answers. Plus redundant metadata clients
around **Crossref / Semantic Scholar / Unpaywall**. **Do not build our own scholarly RAG engine.**

**License:** Apache-2.0.

## API / usage
- Python library (`pip install paper-qa`), plus a Paper QA agent (RAG with citations) and Paper Search (semantic
  search over arXiv). Docs at paper-qa.readthedocs.io.
- `Settings()` for models (LiteLLM local/open), indexing, citations; `PaperQA`, `ask()` for grounded answers.
- It fetches metadata via its own clients (Crossref, Semantic Scholar, Unpaywall) — inspect these before writing
  `crossref_adapter.py` / `unpaywall_adapter.py` / `metadata_merge.py` ourselves.

## Rate limiting / etiquette
PaperQA2 respects the underlying providers' rate limits (Crossref/Semantic Scholar/Unpaywall — use their polite
pools, include contact identifiers where required). Cache indexed full text + metadata locally; don't re-fetch on
every run. Run retrieval offline against a local index once built.

## How Pāṭala consumes it
```
                PaperQA2 (finds likely-useful evidence)
                    │
           candidate retrieval · contextual ranking · evidence gathering
                    ▼
           Pāṭala SourceSpans  →  SourceAssertions  →  propositions/arguments
                    ▼
           epistemically constrained answer   (Pāṭala decides what the evidence licenses)
```
Also: PaperQA2's local **Tantivy BM25** = the independent lexical retrieval baseline for CorroborationBench
(BM25 vs dense vs hybrid vs PaperQA2 vs Pāṭala graph retrieval).

**Priority: IMMEDIATE prototype — point it at ~20 Ratié/Sanderson docs and compare its output to the current
`retrieval.py`.**
