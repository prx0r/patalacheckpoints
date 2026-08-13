# Unpaywall — open-access full-text discovery (via PaperQA)

**What Pāṭala borrows:** an open database of legal open-access full-text links for scholarly works (driven by
Crossref/DOI). For finding whether a work's full text is legally available (and under what license). **Prefer
reuse through PaperQA2's metadata client** rather than writing our own adapter.

**License:** Unpaywall data is CC0; the API is free with a polite email (`mailto`).

## API / usage
`https://api.unpaywall.org/v2/<doi>?email=<you>@<org>` → JSON with `is_oa`, `oa_locations[]` (url_for_pdf,
license, host_type), `best_oa_location`.

## Rate limiting / etiquette
Requires an email (politeness); keep to a modest request rate, cache results by DOI locally (never re-fetch the
same DOI each run). Back off on `429`.

## How Pāṭala consumes it
Feeds `BibliographyRecord.rights`/`textSources` (OA full-text discovery + license) — a metadata witness, never
the canonical identity.
