# PĀṬALA — THE MASTER NAVIGATION (resolve anything)

*2026-08-14. THE canonical index for navigating the whole project — for a human, a coding agent, or
Hermes. Every resource (layer, site surface, data file, script, doc) resolves to: **what it is · its
layer · canonical ref · implementation · key docs · how to run · how to use with Hermes.** If you can
name it, find it here and trace it to its layer.*

**How to use this:** pick a column (Surface / Layer / Data / Script) → read its row → the row gives you
the canonical ref + implementation path + docs + run command + Hermes usage. Everything points back to a
layer in `docs/global/globalglobal.md`.

---

## 0. THE LAYER MAP (the spine everything hangs on)

`docs/global/globalglobal.md` is the tree. `docs/layers/` has one deep page per layer (what/purpose/
tools/data/processes/impls/docs). The layers:

```
00 Governance · 01 Ingestion · 02 Atlas · 03 Factory · 04 Evidence · 05 Research (MOAT)
06 Commentarial · 07 Verification · 08 Human Authority · 09 Organism · 10 Surfaces · 11 Org/Economics
**12 LIVE SYSTEM** (the meta-layer that orchestrates all the others — agents · state · docs · staleness)
```

**Full data flow:** `sources → R2 → reconcile → ATLAS → FACTORY(SOURCE→C1) → RESEARCH(props→args→cruxes→
synthesis) → COMMENTARIAL → VERIFICATION → REVIEW → ORGANISM(Q) → SURFACES → ECONOMICS`

---

## 0b. THE CODE MAP (every dir in plain words)

> The physical folder names are historical; this is the translation layer. The clean concept name is in
> the "=" column. Never rename the physical dirs (breaks ~20k imports). **The machine-verifiable version
> is `DIRECTORY-MANIFEST.json` + `check_directory_manifest.py` (every top-level folder → role/layer/class).**
> **To resolve a FEATURE (education, essay, argument...) directly to its code, see `FEATURE-MODULES.md`.**
> **⚠ Code-schema divergences (ReviewEvent/Authority/Proposition defined in 3-4 places) are flagged in
> `SCHEMA-AUDIT.json` — an agent should read that before trusting any single definition.**

| Physical dir | What it actually is | = clean name | Layer |
|---|---|---|---|
| `ingestion/` | the intake engine: SourceAsserter, R2 snapshot store, per-source adapters | = **ingestion** | 01 |
| `python/patala_core/atlas/` | the Atlas: Postgres (22 tables), resolver, FastAPI API | = **atlas** | 02 |
| `migrations/` | the Alembic Postgres migrations (schema `0001`) | = **db-migrations** | 02 |
| `contracts/` | `CANONICAL-DAG.yaml` — the layer dependency graph | = **dag** | 00,03 |
| `pipeline/` | the factory: workers, scheduler, object_registry + event ledger | = **factory** | 03 |
| `machinelearning/research/patala_ml/` | the research engines: propositions, arguments, cruxes, synthesis, essay, education | = **research** | 05 |
| `source-evidence/` | the scholarly-evidence substrate: contracts, adapters, evals | = **evidence** | 04,07 |
| `source-evidence/evals/` | the benchmark/eval plane (Inspect, NAT, golds) | = **evals** | 07 |
| `source-evidence/production/adapters/` + `ingestion/adapters/` | the external connectors + borrowed-tool adapters | = **adapters** | 01,04 |
| `infra/` | the R2 content-addressed asset store | = **storage** | 02 |
| `app/` | the Next.js site (reader, bibliography, learning) | = **web** | 10 |
| `apps/web/` | the Astro static reader shell | = **astro-web** | 10 |
| `mcp/` | the MCP server (20 tools) | = **mcp** | 10 |
| `openpatala/` | the Atlas build reference ("OpenAlex for Sanskrit") | = **atlas-build** | 02 |
| `lib/` | TS helpers (atlas.ts, verify.ts, factory-state.ts, citation.ts) | = **web-lib** | 10 |
| `data/` | the corpus + atlas data (bibliography, passages, published) | = **data** | content |
| `docs/` | documentation | = **docs** | knowledge |
| `endgamebuild/` | the audit + health + inventory + progress | = **audit** | — |
| `handover/` | cross-agent coordination + build records | = **handover** | history |
| `skills/` | the Hermes skill pack source of truth (synced 1:1 to the `patala` profile) | = **skill-pack** | 12 |
| `examples/` | executable API examples ("executable truth"), 01-07 + run_all.sh | = **examples** | 10 |
| `live/` | fast live agent session state (delegates authority to handover/) | = **live** | — |
| `devpaths/` | the Agent-1 devpath execution log (completed = archive, blocked = roadmap) | = **devpaths** | 05 |
| `ai/` | one-off deep-research essays (argumentation-IR survey, AI-vision) — NOT wired into the docs spine; reference only | = **ai-research** | 05 |
| `onboarding/` | the single on-ramp | = **onboarding** | 00 |
| `components/` | ReactFlow atlas graph components | = **web-components** | 10 |
| `factory-certificates/` | L0/L200 certificates | = **certificates** | 07 |
| `docs-site/` | the docs.patala.org site generator | = **docs-site** | 10 |
| `tmp_t1/` | temporary scratch (gitignored; tests recreate fixtures) | = **tmp-scratch** | — |

---

## 1. SITE SURFACES (what a visitor sees)

| Surface | What it is | Layer | Route / Data | Impl | Docs |
|---|---|---|---|---|---|
| **Home / Atlas graph** | the interactive tradition graph | 10 | `/` | `app/page.tsx` | `docs/vision/vision-15-...` |
| **Bibliography** | the living bibliography | 10 | `/bibliography` | `app/bibliography/page.tsx` + `data/atlas/bibliographySeed.ts` | `docs/process/02-atlas.md` |
| **Timeline / History** | the tradition timeline | 10 | `/history` | `app/history/page.tsx` + `data/atlas/historyTimeline.json` | `docs/vision/vision-11-...` |
| **Learning** | the education surface | 10 | `/learning` | `app/learning/page.tsx` | `docs/vision/education/...` |
| **Read** | the text reader | 10 | `/read/[work]/[locator]` | `app/read/[work]/[locator]/page.tsx` | `docs/endgame2.md` |
| **Concepts / Traditions / Resources** | the entity pages | 10 | `/concepts`, `/traditions`, `/resources` | `app/{concepts,traditions,resources}/` + `data/atlas/{concepts,traditions,resources}.ts` | `docs/vision/CORE-BIBLE.md` |

**Every surface reads the SAME canonical truth** (`docs/process/05-app-api-sites.md`) — never a separate DB.

---

## 2. THE API SURFACES (what an agent calls)

| API | What it is | Layer | Impl | Notes |
|---|---|---|---|---|
| Atlas read API | works/editions/search (OpenAlex grammar) | 2 | `python/patala_core/atlas/api.py` | FastAPI |
| `/api/works`, `/api/texts` | bibliography + texts | 10 | `app/api/texts/route.ts` | |
| `/api/resolve` | resolve a passage/claim to canonical | 2,5 | `app/api/resolve/route.ts` | |
| `/api/passages/[id]` | passage + translation | 2,3 | `app/api/passages/[id]/route.ts` | |
| `/api/history/timeline` | the timeline | 10 | `app/api/history/timeline/route.ts` | |
| `/api/terms/[lemma]/senses` | term senses | 5 | `app/api/terms/[lemma]/senses/route.ts` | |
| `/api/corpus/state` | the translation-state ledger | 3 | `app/api/corpus/state/route.ts` | |
| `/api/verify/*` | the verification floor | 7 | `app/api/verify/{claim-structure,counterevidence,quote,trace-dependency}/` | |
| `/api/context/passages/[id]` | the epistemic neighborhood | 2,5 | `app/api/context/passages/[id]/route.ts` | |
| MCP | 20 tools proxying the API + review engine | 10 | `mcp/index.mjs` | |

---

## 3. THE LAYERS (go deep per layer)

| Layer | Canonical ref | Deep page | Implementation | Key docs |
|---|---|---|---|---|
| **00 Governance** | `AGENTS.md` | `docs/layers/00-governance.md` | `machinelearning/theatre_check.py`, `contracts/CANONICAL-DAG.yaml` | `machinelearning/_ACTIVE/AGENTS-DOCTRINE.md` |
| **01 Ingestion** | `docs/process/01-ingestion.md` | `docs/layers/01-ingestion.md` | `ingestion/asserter.py`, `ingestion/r2.py`, `ingestion/adapters/*` | `docs/global/ingestion-refinery.md` |
| **02 Atlas** | `docs/process/02-atlas.md` | `docs/layers/02-atlas.md` | `python/patala_core/atlas/*`, `migrations/0001...` | `docs/atlas-contracts/atlas-database.md` |
| **03 Factory** | `docs/process/03-factory.md` | `docs/layers/03-factory.md` | `pipeline/object_registry.py`, `factory_scheduler.py`, `*_worker.py` | `docs/FACTORY.md` |
| **04 Evidence** | `docs/process/external-tools.md` | `docs/layers/04-evidence.md` | `source-evidence/schema/*`, `production/adapters/*` | `source-evidence/docs/tools/INDEX.md` |
| **05 Research** | `docs/process/07-ml-epistemic-core.md` | `docs/layers/05-research.md` | `machinelearning/research/patala_ml/*` | `docs/global/globalgoal.md` |
| **06 Commentarial** | `docs/process/06-commentarial-graph.md` | `docs/layers/06-commentarial.md` | (design) | `docs-cache/commentarialgraph-research.md` |
| **07 Verification** | `docs/process/08-verification-plane.md` | `docs/layers/07-verification.md` | `source-evidence/evals/*` | `docs/global/peer-review-goat.md` |
| **08 Human Authority** | `docs/process/README.md` (L8) | `docs/layers/08-human-authority.md` | `source-evidence/schema/contracts_human_authority.py`, `pipeline/review_engine.py` | `docs/global/patala-peer-review.md` |
| **09 Organism** | `docs/process/09-organism.md` | `docs/layers/09-organism.md` | (design) | `docs/vision/organism/*` |
| **10 Surfaces** | `docs/process/05-app-api-sites.md` | `docs/layers/10-surfaces.md` | `app/`, `mcp/`, `openpatala/` | `docs/vision/vision-12-...` |
| **11 Org/Economics** | `docs/global/globalpartnerships.md` | `docs/layers/11-org-economics.md` | `AGENTS.md`, `~/.hermes/profiles/patala/MEMORY.md` | `docs/endgame4.md` |
| **12 LIVE SYSTEM** | `docs/layers/12-live-system.md` | `docs/layers/12-live-system.md` | `docs_state()` · `check_docs_stale.py` · `patala_*` MCP verbs · 3 Hermes profiles + kanban | `handover/hermes/CANONICAL.md` + `DEV-PLAN.md` + `HERMES-AGENT3-FACTORY-COORDINATOR.md` |

---

## 4. THE DATA (where content lives)

| Data | What it is | Layer | Location |
|---|---|---|---|
| **Bibliography** | the canonical bibliography | 2 | `data/atlas/bibliographySeed.ts` + `data/corpus/atlas-bibliography.json` |
| **Audited bibliography** | the Trika-10 at full depth | 2 | `data/atlas/audited.ts` |
| **Tradition graph** | traditions + relations | 10 | `data/atlas/traditions.ts`, `relations.ts` |
| **Concepts / terms** | concept + term objects | 5 | `data/atlas/concepts.ts`, `data/terms.json` |
| **Timeline** | the history timeline | 10 | `data/atlas/historyTimeline.json` |
| **People** | scholars/person objects | 2,10 | `data/atlas/people.ts` |
| **Published corpus** | the published passages (IPVV, Kramasadbhāva) | 3 | `data/published/` |
| **Object registries** | versioned layer objects | 3 | `data/corpus/registries/*.jsonl` |
| **Event ledger** | append-only hash-chained history | 3 | `data/corpus/registries/object-events.jsonl` |
| **Postgres** | the canonical graph (22 tables) | 2 | `postgresql://patala:...@localhost:5433/patala_atlas` |
| **R2** | immutable bytes (Bronze/Silver snapshots) | 1,2 | `source/ingestion/<SOURCE>/snapshots/` |

---

## 5. HOW TO RUN (the scripts)

| What | Command | Layer |
|---|---|---|
| Live systems status | `bash pipeline/start_overnight.sh status` | 3 |
| Factory catalog | `python3 pipeline/catalog.py --all` | 3 |
| Factory integrity | `python3 pipeline/factory_certificate.py` | 3 |
| Ingestion tests | `python3 ingestion/test_asserter.py` + `test_smoke.py` | 1 |
| R2 snapshot a source | `python3 -m ingestion.r2 --source X --snapshot-id Y --file Z` | 1 |
| Atlas read API | `uvicorn patala_core.atlas.api:app` | 2 |
| The anti-theatre gate | `python3 machinelearning/theatre_check.py --status` | 0 |
| Atlas migrations | `.venv-atlas/bin/alembic upgrade head` | 2 |
| The site (dev) | `npm run dev` | 10 |
| The site (verify) | `npm run build` | 10 |
| The eval plane | `python3 source-evidence/evals/...` | 7 |

---

## 6. HOW TO USE WITH HERMES

**Hermes = Pāṭala's replaceable execution kernel.** The `patala` profile (`~/.hermes/profiles/patala/`)
holds the operator memory + skills. Call it as an **agent, never blind `-z`** (`docs/global/HERMES-CALLING.md`).

```bash
# agentic call (the CORRECT way — has file access + skills)
hermes chat -Q -q "<ask>" --skills <skill> --yolo --max-turns 8

# run in the patala profile
hermes --profile patala -z "<prompt>"     # one-shot (blind — only for pure text)
```
- **Hermes task DONE ≠ Pāṭala object ACCEPTED** — proposals are MACHINE_PROPOSED until review.
- **Operating axioms (from AGENTS.md):** never sleep to wait · background via `nohup`/`setsid` ·
  kill by PID never `pkill` · external sources → R2 · reuse don't rebuild · respect licenses.
- The patala profile's `MEMORY.md` holds these axioms so Hermes follows them too.
- Model: the correct invocation is `hermes -z "<prompt>" -m deepseek-v4-flash --provider opencode-go`
  (pass BOTH model and provider explicitly — `HERMES_MODEL` alone fails). `pipeline/model.py` already does this.

---

## 7. THE DOCS TREE (where knowledge lives)

```
docs/global/globalglobal.md        ← THE SPINE (the tree) — start here
docs/vision/CATEGORIES.md          ← the 8 vision categories, each mapped to a Layer
docs/vision/REVIEWS.md             ← the canonical review index (every doc: name/contribution/layer/status)
docs/process/IPVV-BUILD.md         ← the complete IPVV build index (scholarly layers + factory + golds + tests)
docs/layers/                       ← one deep page per layer (what/purpose/tools/data/processes/impls/docs)
docs/process/README.md             ← the process index (01-09 + external-tools + githubclones + reconciliation)
docs/process/SITE-WIDE-ORGANIZATION.md  ← the full repo map
docs/global/                       ← thesis, architecture, partnerships, state
docs/vision/                       ← CORE-BIBLE + 13 visions + organism + scholars/education
endgamebuild/                      ← inventory + audit + progress (health)
SPINE.md                           ← every code dir in plain words
source-evidence/docs/tools/INDEX.md ← all 62 external tools + status
```

---

## 8. THE ONE-LINE CARRY-FORWARD

> Name anything in Pāṭala (a page, an API, a data file, a script, a doc) → find it in this index →
> it resolves to: its LAYER, its canonical ref, its implementation path, its key docs, how to run it,
> and how to drive it with Hermes. The spine is `docs/global/globalglobal.md`; the deep detail per layer
> is `docs/layers/`; this file is the resolver that connects everything.
