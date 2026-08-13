# Tantivy — local BM25 full-text search (the lexical baseline)

**What Pāṭala borrows:** a mature MIT-licensed, Lucene-inspired full-text search engine in Rust with Python
bindings — BM25, phrase search, facets, incremental indexing, JSON fields, compressed doc storage. Pāṭala does NOT
need Elasticsearch/OpenSearch/a vector cluster for the (non-internet-scale) scholar corpus.

**License:** MIT.

## API / usage
- Python bindings: `pip install tantivy`. Build an `Index` with a schema, add docs, commit, then query with BM25
  / phrase / term queries; support field-level filters (author/year/scholar/work).
- Incremental indexing; `Index::reload` / `Searcher`.

## Rate limiting / etiquette
Local library — no server/rate limits. Etiquette = index determinism + reproducibility: keep a frozen corpus
snapshot so a benchmark's lexical baseline doesn't drift.

## How Pāṭala consumes it
```
SourceSpan corpus → Tantivy (BM25 / phrase / author-year / scholar / work filters) → independent lexical baseline
   for every retrieval benchmark (CorroborationBench: BM25 vs dense vs hybrid vs PaperQA2 vs Pāṭala graph)
```
Prefer reuse **through PaperQA2** (which bundles Tantivy) first; stand it up directly only if needed.

**Priority: HIGH (via PaperQA).**
