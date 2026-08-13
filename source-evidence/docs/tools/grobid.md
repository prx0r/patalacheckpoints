# GROBID — PDF → structured scholarly text

**What Pāṭala borrows:** turns messy PDFs into structured text (TEI) — bibliographic header, references, citation
contexts, sections/paragraphs, figures/tables, footnotes, PDF coordinates, DOI resolution, license. Used in
production by Semantic Scholar, ResearchGate, CERN, Internet Archive Scholar.

**License:** Apache-2.0 (code). Runs as a local Docker/HTTP service — no external dependency.

## API
Base URL (default) `http://localhost:8070` (dockerized).
- `POST /api/processFulltextDocument` — full document → TEI. Query: `input` (multipart PDF/TXT). Response: TEI XML.
- `POST /api/processHeaderDocument` — just the bibliographic header.
- `POST /api/processReferences` — bibliography/reference list.
- `POST /api/processCitation` — one citation string → structured reference.
- `POST /api/processCitationList` — a list.
- `POST /api/processNames` / `processAffiliations` — name/affiliation extraction.
- `POST /api/processFigures` — figure/table detection + captions + coordinates.
- `GET /api/isalive` — health.
- `GET /api/version` — version.
`POST /api/annotate` (W3C Web Annotation output) is also available.

## Rate limiting / etiquette
GROBID is **local** — no third-party rate limit. But it is CPU-heavy (ML models): run it as an async queue, one
document per process slot, avoid parallel bursts (it will slow/queue). Use `consolidateHeader`/`consolidateCitations`
with a Crossref `mailto` so GROBID can enrich. Retry with backoff on `504`.

## How Pāṭala consumes it
```
RAW PDF → GROBID /api/processFulltextDocument → TEI
   (coordinates + paragraphs) → Pāṭala SourceSpan (Web Annotation selectors + Pāṭala hash)
```
The GROBID TEI becomes the *extraction witness* (record `derivation_method: grobid@<version>`,
`text_sha256`), satisfying the PROV derivation + Web Annotation span layer.
