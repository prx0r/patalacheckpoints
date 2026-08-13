# OpenAlex — scholarly metadata / enrichment

**What Pāṭala borrows:** a large open scholarly graph (works/authors/venues/institutions/concepts/citation
counts) to *propose* title/author/year/venue/DOI/related-works for an ingested PDF — as a **metadata witness,
never canonical identity**. Canonical = stable `pt:*` + external IDs attached.

**License:** data CC0, code MIT. No API key required for basic use.

## API
Base URL `https://api.openalex.org`.
- `GET /works` — search works. Params: `search`, `filter=doi:...|openalex:W...|title.search:...`,
  `per-page` (max 200), `cursor` (pagination), `select` (fields), `mailto`.
- `GET /works/W<id>` — one work (authorships, referenced_works, cited_by_count, locations, concepts).
- `GET /authors`, `/venues`, `/sources`, `/institutions`, `/concepts`, `/topics` — same pattern.
- `GET /works?filter=cites:W<id>` — works citing a given work (the citation graph from OpenAlex's perspective).
- `select=` to request only needed fields (less load).

## Rate limiting / etiquette
- **Use the polite pool:** include `mailto` on every request (or an `X-OpenAlex` header) → raises your limit and
  puts you in the polite queue.
- Polite pool ≈ **10 requests/second**; without `mailto` it's much lower and you risk `429`.
- Back off on `429` (respect `Retry-After`), use `cursor` pagination (not `page`), cache aggressively, batch by
  DOI rather than one query per title. Be kind — this is a public free service.

## How Pāṭala consumes it
```
ingested PDF → GROBID header → OpenAlex search by title/DOI → propose {title, author, year, venue, DOI,
OpenAlex W-id, cited_by, referenced_works}
   → store as crosswalk on pt:source_id (metadata witness, not identity)
```
Later, the citation graph helps distinguish "3 independent scholars" from "3 papers repeating one scholar" (via
`referenced_works` + `cites`).
