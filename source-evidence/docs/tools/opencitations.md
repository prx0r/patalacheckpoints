# OpenCitations Meta + Index — citation graph + bibliographic disambiguation

**What Pāṭala borrows:** the citation graph (which work cites which) + bibliographic disambiguation of the same
work across identifiers (DOI / Academia PDF / Crossref record / local PDF / a citation in another article). Use
as a **metadata witness**; never own the global citation DB.

**License:** OpenCitations data is CC0; software is open-source (e.g. `oc_meta`).

## API
- **OpenCitations Index** (citation graph): `https://opencitations.net/index/api/v1/citations/<work_id>` and
  `/references/<work_id>` — citations to/from a work by DOI/OpenAlex/ORCID/etc.
- **OpenCitations Meta** (`oc_meta`): bibliographic records + their disambiguation and provenance.
  `https://opencitations.net/meta/api/v1/metadata/<id>` — metadata for an id.
- Work IDs accepted across DOI, OpenAlex, PMID, arXiv, etc. (the cross-identifier disambiguation is the value).

## Rate limiting / etiquette
- Public endpoints are free; be conservative. Use **paged responses** (do not fetch an entire citation set at
  once for a huge work), cache citation subgraphs locally, and back off on `429` (`Retry-After`).
- Respect the service's terms; this is community infrastructure. Batch by work, not by single citation.

## How Pāṭala consumes it
```
pt:source_id + DOI/OpenAlex id → OpenCitations citations/references → the "3 independent scholars vs 3
papers repeating one scholar" distinction (via the citation/derivation graph), feeding CorroborationEvent
independence/lineage classification.
```
Do NOT build a global citation database — import links.
