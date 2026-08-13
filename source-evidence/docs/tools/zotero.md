# Zotero — bibliography / library management backend

**What Pāṭala borrows:** the entire bibliographic CRUD + citation layer — items/collections, attachments,
creators, versioning, file upload, full-text access, incremental `since=` sync, BibTeX/BibLaTeX/CSL JSON/RIS/MODS/
TEI export, formatted citations/bibliographies. Pāṭala does NOT maintain its own bibliography subsystem.

**License:** client + Web API are free/open-source (server AGPL; the public API is free to use with an account).

## API (Web API v3)
Base URL `https://api.zotero.org`.
- `GET /users/<id>/items` — items, paged. Params: `start`, `limit` (max 100), `format` (json/bibtex/csljson/rdf),
  `q`, `qmode`, `tag`, `since` (incremental sync), `sort`/`direction`.
- `POST /users/<id>/items` — create (needs API key). Bulk create is fine (array).
- `PATCH /users/<id>/items` — partial update (version-concurrency: include current `version` to avoid clobber).
- `GET /users/<id>/collections`, `/collections/<key>/items`.
- `GET /users/<id>/items/<key>/file` — attachment file; `/items/<key>/file/view`.
- `GET /users/<id>/settings/keys/current` — verify key.
- Header `Zotero-API-Key: <key>` for auth; `Zotero-Write-Token` for multi-item writes.
- **Versioning:** every object has a `version`; use `since=` for incremental changes — Pāṭala doesn't build sync.

## Rate limiting / etiquette
- Unauthenticated/anonymous requests are heavily throttled. **Always use an API key.**
- Default rate limits are generous but enforce **polite polling**: use `since=` + `limit=100` + pagination rather
  than re-fetching everything; back off on `429 Too Many Requests` (respect the `Retry-After` header).
- Batch writes (array) instead of many single POSTs. Avoid polling the API on a tight loop — cache locally.

## How Pāṭala consumes it
```
Zotero item = bibliographic identity (crosswalk) — store:
  zotero_library_id · zotero_item_key · DOI · OpenAlex ID · OpenCitations ID
on the stable pt:source_id (never let Zotero own the identity).
```
Cite using **CSL/citeproc** via Zotero's `csljson`/`citeproc-js` — formatted citations for the site/education
without custom citation code.
