# Pāṭala Changelog

Separates **API changes** (software) from **data changes** (corpus) and **scholarly changes** (reclassifications after review). Data/scholarly changes are not software releases.

## 2026-08-10

### API changes
- Added `GET /api/health` — operational status + dataset revision, separate from `/api/stats`.
- Added `docs/openapi.yaml` — OpenAPI 3.0.3 spec for the full surface.
- Added `docs/api/` — 5-minute quickstart, 6 research recipes, 4 concepts, MCP mapping, and 7 executable examples (`examples/01..07`), runnable via `bash examples/run_all.sh`.
- Added `tests/api_suite.py` — 51-check verification suite (contract shape, referential integrity, epistemic invariants, provenance, golden resolver cases, error handling). `npm test`.
- **Fixed** MCP `concordance` tool: plain-object schema crashed the server; now uses Zod (all 12 MCP tools initialize).
- **Fixed** `sanskritree/scripts/concordance.py`: zero-hit is a valid 200 empty result in JSON mode (was exit 1 → API 500).

### Data changes
- Corpus: 69 works, 4,016 verse passages (5 works), 1,542 OCHS manuscript witnesses resolved to 18 works, 15 accepted terms + 1 proposal.
- OCHS manuscript layer (CC BY-NC-SA 4.0) ingested and crosswalked.

### Scholarly changes
- None this cycle.
