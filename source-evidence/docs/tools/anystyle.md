# AnyStyle — bibliography reference parser (fallback)

**What Pāṭala borrows:** a fast bibliographic reference parser (Ruby CLI/API, trainable models) handling raw
citation strings → structured references (CSL-style). Used as a **fallback** when GROBID's reference parser fails
or is low-confidence — especially old humanities bibliographies, pasted bibliography files, weird footnote
references, and bibliographies outside PDFs.

**License:** BSD-style.

## API / usage
- CLI: `anystyle parse <file>` / `anystyle find`; Ruby API; there is a Python wrapper (`anystyle-py`).
- Output: structured references (authors, title, year, venue) in CSL/JSON.

## Rate limiting / etiquette
Local tool — no rate limit. Etiquette = combine with Crossref/OpenAlex resolution; keep the raw string as
provenance.

## How Pāṭala consumes it
```
GROBID reference parser → failed/low confidence? → AnyStyle → Crossref/OpenAlex resolve
```
Feeds `BibliographyRecord` crosswalk + `BibliographyCrosswalks.witness[]`.

**Priority: CHEAP WIN.**
