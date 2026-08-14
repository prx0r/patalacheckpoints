# 05 — APP / API / MCP / SITES (the read surfaces)

*Part of `docs/process/README.md`. The app, APIs, and MCP are **projections over the one canonical
graph** — never separate databases. Both sites (the current Next.js app + the Atlas) and every API
read the SAME canonical truth. This is what makes the "immutable reference across the site" work.*

## 1. The principle

> One canonical graph (Postgres + R2 + ledger). Everything below is a disposable projection.

```
Postgres Atlas  ──►  patala_core/atlas/api.py (FastAPI, OpenAlex grammar)
                     ├── the Next.js site (data/atlas/*, /bibliography, /)
                     └── MCP server (mcp/index.mjs, 20 tools proxying the HTTP API + review engine)
```

## 2. Reusable surfaces

| Surface | Reusable entry point | Purpose |
|---|---|---|
| Atlas read API | `python/patala_core/atlas/api.py` — FastAPI `app`, 5 endpoints | works/editions/search, OpenAlex grammar |
| App routes | `app/api/` — 42+ routes | works, texts, passages, manuscripts, search, resolve, themes, education, stats, crosswalks |
| MCP server | `mcp/index.mjs` — 20 tools | HTTP API proxy + review-engine tools |

## 3. Known issues (audit §5 — do not reintroduce)

1. **IPVV passage-ID mismatch (top priority):** published IPVV store uses `pt:passage:ipvv:chunkA-…md`;
   the segmented jsonl corpus uses `tantra:text:…:V2-A:<slug>`. So `/resolve`, `/context/passages/:id`,
   `/passages/:id` **404** against the richest IPVV data.
2. **`translation_status` vs `translationStatus`** casing inconsistency across works/texts routes.
3. **1 dangling atlas relation** (`nitya_shodasikarnava → yoginīhṛdaya`) + `passages: null` dead key
   in recovery-gold.
4. **Factory intake state fragmented** across 4 sivaqueue manifests / 3 sources of truth for "on disk".
5. Hard-coded machine paths: `concordance/route.ts` → `/mnt/HC_Volume_106427611/sanskritree`; MCP
   TANTRA_CORPUS/TANTRA_API_BASE defaults.

## 4. Build / run

```bash
npm run dev      # local dev (localhost:3000)
npm run build    # the verification (must be clean)
```
Data lives in `data/atlas/*` (traditions.ts, texts.ts, people.ts, concepts.ts, relations.ts,
audited.ts, bibliographySeed.ts). Edit `data/atlas/*` to grow the site.
