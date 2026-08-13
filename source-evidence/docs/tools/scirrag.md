# SciRAG — Scholar Assistant expansion / gap critic

**What Pāṭala borrows:** an open-source system adding to the Scholar Assistant: **query decomposition**,
**parallel/sequential retrieval**, **citation-graph expansion**, **gap detection**, **symbolic reranking**, and
**outline-guided synthesis** — evaluated on ScholarQA/QASA/SciFact-style tasks.

**License:** open (Yale NLP).

## How Pāṭala consumes it
```
question → PaperQA2 retrieval → SciRAG expansion / gap critic → candidate evidence →
PĀṬALA EPISTEMIC CHECKING → answer + evidence + rival reading + boundary + crux
```
SciRAG does the retrieval/expansion/gap work; Pāṭala decides what the retrieved literature licenses. **Do not
build a research search engine.**

**Priority: prototype alongside PaperQA2 for the Scholar Assistant.**
