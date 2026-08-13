# Crossref — DOI / metadata resolution

**What Pāṭala borrows:** DOI resolution + authoritative bibliographic metadata (title/authors/journal/year/license)
for works that have DOIs. Used by GROBID's `consolidateHeader`/`consolidateCitations`.

**License:** metadata is CC0; API is free, no key required.

## API
Base URL `https://api.crossref.org`.
- `GET /works/<doi>` — one work (title, author, container-title, year, license, reference, relation).
- `GET /works?query.bibliographic=<...>` — search by bibliographic string.
- `GET /works?filter=doi:...` — filter.
- `GET /prefixes/<prefix>/works` — all works by a publisher prefix.
- `GET /journals/<issn>/works` — works in a journal.
- Response is JSON; `message` holds the work; `reference` = its reference list (the citation graph from Crossref's
  perspective).

## Rate limiting / etiquette
- **Polite pool:** include `mailto` (e.g. `mailto:you@example.com`) to raise your limit and be treated politely.
- Recommended **best practice:** ~**1 request/second** sustained (bursts ok); do not exceed ~50/s (risks `429`).
- Back off on `429` with `Retry-After`; use the `Crossref-Plus`/`Crossref-Status` headers; cache resolved DOIs
  locally (never re-resolve the same DOI every run). Be kind — public free service.

## How Pāṭala consumes it
```
DOI (from GROBID/OpenAlex/Zotero) → GET /works/<doi> → authoritative metadata + license
   → crosswalk on pt:source_id (metadata witness)
```
Enrichment priority: **Crossref/DataCite → OpenAlex → OpenCitations → ORCID → ROR**.
