# READ-PLANE + ORGANISM INTEGRATION — my modern machinery as the serving substrate

*2026-08-14. The plan to make my read plane + organism the serving/autonomy layer over patala's factory.
Patala produces the canonical objects; my read plane (context_compiler → bundles → MCP → SEO → site) SERVES
them, and my organism (next_action + factory_pool + hermes) DRIVES the autonomous loop. This is the
integration seam the whole collaboration points to.*

---

## THE REALITY (verified)

**My read plane (REAL, validated):**
- `context_compiler.py` (12/12) — the projection compiler: canonical graph → immutable content-addressed
  context bundles (one agent question = one request).
- `fts_search.py` (9/9) — Postgres-FTS-equivalent baseline (p50 <10ms; Tantivy only if profiled hot).
- `bundle_router.py` (16/16) — the MCP 8-tool adapter + R2-style immutable emission.
- `seo.py` (13/13) — canonical URLs + JSON-LD + sitemap (unifies human/search/agent/API graphs).
- `build-static-site.py` — ALREADY compiles the real registry (SOURCE 32039, T1, L0, ... into site/).
- `rebuild-on-commit.py` — compute-on-write incremental (unchanged = no-op).
- `web/` Astro + `edge/worker.js` + `wrangler.toml` — built, NOT deployed.

**My organism (REAL, validated):**
- `ingestion_organism.py` (10/10) — the priority-driven refinery (SENSE→PRIORITIZE→INGEST→REFINE→VERIFY→
  COMMIT→SERVE→FEEDBACK).
- `next_action.py` (7/7) — the deterministic scheduler (decide WHAT by formula, not LLM-guess).
- `factory_pool.py` (10/10) — the DAG-gated parallel worker pool (many layers at once).
- `hermes_exec.py` (6/6) — real agentic generation (not blind -z).
- `self_healing.py` (8/8) — the typed repair cascade.

**The gap:** the read plane is a LOCAL simulation (bundles to disk, FTS in DuckDB, Astro un-deployed);
the organism isn't wired to patala's real factory loop.

---

## THE BUILD (in order)

### R1 — Deploy the read plane (SPEC-00 §9-20, the SPEC-49 premise)
- Push the compiled projections to R2 (content-addressed, immutable); serve via Cloudflare CDN.
- Stand up Neon Postgres + the `artifacts/aliases/relations/passages/works` canonical schema.
- Deploy the Astro site + Worker (`/api` + `/mcp`) + Hyperdrive (dynamic fallback only).
- Wire the projection DAG + incremental rebuild (add a doc → rebuild only affected, NOT the whole corpus).
- **Gate:** the site/API/MCP serve compiled bytes from R2/CDN (not _load()-reconstruction); a new doc does
  NOT rebuild the whole corpus.

### R2 — Wire the organism to the factory loop
- `next_action` (decide WHAT) → patala `corpus_state.next_valid_action` (decide the legal transition) →
  the factory workers (produce) → commit to registry → my read plane recompiles (rebuild-on-commit).
- `factory_pool` drives MANY works/layers in parallel, DAG-gated, each committing independently.
- **Gate:** the autonomous loop runs a real work through the full chain and the site updates (compute-on-write).

### R3 — The organism feedback (the flywheel)
- Learner probes → `ingestion_organism.learner_probe` → re-prioritize `next_action`.
- Misconceptions → cruxes → the pushing-miner feeds the argument layer.
- **Gate:** a learner probe raises a work's priority (Q) in the scheduler.

### R4 — The MCP + SEO surface over the live registry
- The `bundle_router` MCP 8-tools serve the real compiled works (resolve/search/get/context/trace/compare/
  neighbors/evidence).
- `seo` gives every work a canonical URL + JSON-LD (agent-SEO, unifies the graphs).
- **Gate:** a real work resolves via MCP + has a canonical URL + JSON-LD.

---

## THE INTEGRATION RULE

> patala produces (the factory + registry); my read plane SERVES (compiler → bundles → MCP → SEO → site);
> my organism DRIVES (next_action + factory_pool + hermes). One autonomous organism: produce → verify →
> serve → learn. Keep the two schema.py in separate processes.

## Proofs / resolution
- My read plane: `lib/{context_compiler,fts_search,bundle_router,seo}.py`, `scripts/build-static-site.py`,
  `scripts/rebuild-on-commit.py`, `web/`, `edge/`
- My organism: `lib/{ingestion_organism,next_action,factory_pool,hermes_exec,self_healing}.py`
- The specs: `specs/SPEC-00`, `specs/SPEC-49`
- The master: `devplans/MASTER-INTEGRATION-DEVPLAN.md`
