# LAYER 10 — SURFACES (sites + APIs + products)

> **STATUS: PARTIAL — app/ + mcp/ + openpatala are REAL; the Scholar/Contributor/Reviewer surfaces are pending** (derived live state — see `docs_state.py`)


*Part of the `NAVIGATION.md` layer map (the master tree / spine). The renderings of the one canonical graph.*

## 1. What it is
The product surfaces: the sites, APIs, MCP, and products that render the one canonical graph for
different audiences. Everything here is a **projection** — it reads the same truth, never a separate
database.

## 2. Purpose
Let consumers, scholars, contributors, developers, and reviewers each enter at their depth — all over
the same graph. The 5 product surfaces (Consumer · Scholar · Contributor · Developer · Reviewer).

## 3. External tools used
See `external-tools.md` — retrieval (Tantivy/Postgres FTS), annotation (INCEpTION/Recogito), publishing
(RO-Crate/nanopub), IIIF (manuscript images).

## 4. Data
- `data/atlas/*` — the site data (traditions.ts, texts.ts, people.ts, concepts.ts, relations.ts,
  audited.ts, bibliographySeed.ts).
- The FastAPI read model (`atlas/api.py`) + the compiled `atlas-bibliography.json`.
- The Next.js app routes (`app/`) + MCP (`mcp/index.mjs`).

## 5. Processes
```
one canonical graph → AtlasAdapter (compiled read-model) → all surfaces read the same truth
```
Both the Tantra Hub + the Atlas read the same canonical layer — never two databases (Vision 12: one
core, five permission-scoped surfaces).

## 6. Implementations
- `python/patala_core/atlas/api.py` — the FastAPI read API (OpenAlex grammar).
- `app/` — the Next.js site (reader, bibliography, learning).
- `apps/web/` — the Astro static reader shell.
- `mcp/index.mjs` — the MCP server (20 tools).
- `openpatala/` — the Atlas build ("OpenAlex for Sanskrit").
- `docs-site/` — the docs site (docs.patala.org).
- Tests: `test_api` (9), the app route imports.

## 7. Docs
- `docs/process/05-app-api-sites.md` — the detailed layer guide.
- `docs/process/SITE-WIDE-ORGANIZATION.md` — the sites/surfaces map.
- `docs/vision/vision-12-multi-surface-platform.md` — one core, five surfaces.
- `docs/vision/vision-13-product-portfolio-by-user-base.md` — the product catalog.
- `docs/vision/vision-15-patala-atlas-sanskrit-research-graph.md` — the Atlas.
