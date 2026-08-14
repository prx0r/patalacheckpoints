# BUILD: WIRE THE OG SITE + MCP TO THE LIVE DATA (kill the static-vs-live gap)

*2026-08-14 · status: WHAT TO BUILD · the OG Next.js site + MCP server are real and rich, but they read
STATIC `@/data` files, not the LIVE factory registry/DB. This is the "four-truths" problem at the read
surface — the site serves curated data while the factory writes the registry, and they're disconnected.
Reference the ACTUAL files.*

---

## THE REAL OG SITE (what exists — not orphaned)

### The Next.js app (`/root/projects/patala/app/`)
- **12 pages**: concepts, resources, traditions, texts (kramasadbhava, isvarapratyabhijnavivrtivimarsini),
  read/[work]/[locator], learning, history, bibliography
- **43 API routes** (`app/api/*/route.ts`): works, texts, passages, manuscripts, search, resolve, themes,
  education, stats, crosswalks, decisions, context, journey, recommend, concordance, relations, verify/*,
  history/timeline, terms/[lemma]/history
- **The "other stuff"** (timeline + lemma):
  - `app/api/history/timeline/route.ts` → reads `data/atlas/historyTimeline.json` (23 schools)
  - `app/api/terms/[lemma]/history/route.ts` → the diachronic sense-trajectory (curated, NOT mechanical)

### The MCP server (`/root/projects/patala/mcp/index.mjs`)
- **29 tools**: get_work, get_source_passage, resolve_ref, search_passages, verify_*, get_themes,
  get_related_works, concordance, get_manuscripts, get_history_timeline, patala_* review tools
- Proxies the `/api/*` routes (22 `api(` calls)

### The real data it reads (the static layer)
- `data/atlas/*.ts` (audited, bibliographySeed, concepts, people, relations, traditions, texts, resources,
  sivaqueueSeeds) + `data/corpus/*.ts` (analyst, annotations, canonical-spines, gold, graph)
- `data/atlas/historyTimeline.json` (timeline) · `data/corpus/atlas-bibliography.json` (254 works) ·
  `data/published/ipvv/*.json` (55 passages)

---

## THE GAP (verified)

**33 of the 43 API routes read `@/data` (static TS/JSON files); 0 hit Postgres or the live
`object_registry`.**

```bash
grep -rl "from \"@/data" app/api/ | wc -l   # 33 static
grep -rl "postgres\|Pool\|object_registry" app/api/ | wc -l   # 0 live
```

So the site serves CURATED data while the factory writes the REGISTRY — they're disconnected. A new
translation committed to the registry does NOT appear on the site until someone manually updates the
`@/data` files. This is the four-truths problem at the read surface.

---

## WHAT TO BUILD (wire the site + MCP to the live data)

1. **The read-path bridge**: make the API routes read from the LIVE source of truth (Postgres per
   SPEC-00, or the compiled projections), not the hand-edited `@/data` TS files.
   - `docs/process/05-app-api-sites.md` says the design: *"One canonical graph (Postgres + R2 + ledger).
     Everything below is a disposable projection."* The site should READ the projection, not be the source.
2. **The compile bridge**: the factory's committed objects → the projections the site serves (via
   ip-graph's `context_compiler` / `bundle_router`, or the `web/` Astro static site). So a new
   translation → registry → projection → site, automatically.
3. **The MCP proxy**: the 29 MCP tools should proxy the LIVE data (or the compiled projections), not the
   static TS.

### The design target (SPEC-00)
```text
factory (object_registry, the live truth)
   → compile (context_compiler / bundle_router)
   → projections (JSON/HTML/bundles on R2+CDN)
   → the site + MCP read the projections (0 request-time reconstruction)
```
The site becomes a read plane over the LIVE factory, not a parallel curated store.

---

## THE TEST

```bash
# verify the current gap (33 static, 0 live)
cd /root/projects/patala
grep -rl "from \"@/data" app/api/ | wc -l   # 33
grep -rl "object_registry\|Pool" app/api/ | wc -l   # 0

# after the build: a new committed translation appears on the site without editing @/data
python3 -c "import sys; sys.path.insert(0,'pipeline'); import object_registry as R; print('SOURCE:', len(R._load('SOURCE')['objects']))"
```

**Pass when:** the 43 API routes + 29 MCP tools serve the LIVE factory data (via compiled projections),
and a new translation committed to the registry automatically reaches the site — no hand-edited `@/data`.
That closes the four-truths gap at the read surface.
