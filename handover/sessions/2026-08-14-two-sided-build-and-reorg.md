# SESSION — 2026-08-14: the two-sided build + the doc reorg (agentpatala)

*The session that (1) organized the migration/ docs into a clean 3-part structure, (2) set up the
two-sided collaboration with agentgraph, and (3) built + verified the OG patala pipeline end-to-end.
Read `HANDOVER.md` (the stable state) + `migration/shared/README.md` (the coordination) first; this is
the timestamped record of what happened.*

---

## 1. WHAT THIS SESSION DID

### 1.1 Organized the migration/ docs (the reorg)
The `migration/` folder had sprawled to 75 files (v2 + v3 + shared) with overlap. Cleaned it:
- **`migration/v3/`** = the CURRENT blueprint (the organism, 16 products, verified proofs, live tests)
- **`migration/shared/`** = the LIVE coordination with agentgraph (the two-sided build)
- **`migration/v2/`** = ARCHIVED (superseded by v3)
- Wired into the root: `docs/INDEX.md` + `AGENTS.md` read-order now reference v3 + shared.

### 1.2 Set up the two-sided collaboration (agentgraph + agentpatala)
- `migration/shared/ROLE-SEPARATION.md` — agentgraph (frontier kernels) vs agentpatala (production/tester)
- `migration/shared/HANDOFF-QUEUE.md` — the live integration status (agentgraph's 37 → agentpatala's 10)
- `migration/shared/AGENTS-AGENTPATALA.md` — my role contract
- `migration/shared/SHARED-GOAL.md` — the north star: priority-queue Sanskrit → full spine → products
- `migration/shared/BUILD-*.md` (14 files) — the build-directive set for agentgraph, each with real file refs
- `migration/shared/CRITICAL-AUDIT-IPGRAPH.md` + `PEER-REVIEW-IPGRAPH-NAV.md` — the honest audits

### 1.3 Built + verified the OG patala pipeline (the real data, not the lab demo)
- **The full-system test** (`migration/v3/full_system_test.py`) — the Sārdhatriśatikālottarāgama (a real
  untranslated Śaiva Āgama, 309 verses): 11/11 on source→tokenize→translate (Hermes)→proof→argument→
  crux→review→education→autonomous loop
- **The multi-subject test** (`test_multisubject.py`) — 20/20 across IPVV + Doyle + Ratié (generality)
- **The product proofs** (`build_products.py`) — 18/18 products on the real V2-A claim
- **The autonomous pipeline** (`autonomous_pipeline.py`) — the priority-queue ingestion wired to 48 real
  works from the sivaqueue
- **The OG static site** (`web/`) — Astro 0-JS site over the real data (254 works, 9 clusters, 49 passages)

### 1.4 Found the critical issues (the honest audit)
- **The `chat` vs `-z` fix**: `hermes -z` is blind (~3.8% yield); `chat_agentic()` (agentic `hermes chat`)
  is correct. ip-graph's `hermes_exec.py` uses `-z` (wrong + orphaned).
- **The 6 divergent ReviewEvent/Authority contracts** — must converge before building more.
- **The OG site's API reads static `@/data` (33/43), not the live registry** — the four-truths gap.

---

## 2. THE KEY FILES (what a next agent should read)

### The stable entry
- `HANDOVER.md` — the current state
- `AGENTS.md` — the governing rules + read-order
- `NAVIGATION.md` — the master index

### The current blueprint + coordination
- `migration/v3/README.md` — the organism + proofs
- `migration/shared/README.md` — the two-sided build (the coordination)
- `migration/shared/BUILD-INDEX.md` — the build-directive map

### The verified proofs (the evidence)
- `migration/v3/full_system_test.py` (11/11) · `test_multisubject.py` (20/20) · `build_products.py` (18/18)
- `migration/v3/translate_passage.py` (the real Hermes generation)

---

## 3. THE PRIORITIES FOR THE NEXT AGENT

1. **Wire the OG site/API/MCP to the LIVE data** (`BUILD-SITE-LIVE-DATA.md`) — 33/43 routes read static
   `@/data`, 0 hit the registry. This closes the four-truths gap.
2. **Converge the 6 divergent contracts** (`BUILD-CONTRACTS-CONVERGENCE.md`) — the #1 build.
3. **Fix the Hermes invocation** (`BUILD-WIRE-HERMES-GENERATION.md`) — adopt `chat_agentic`, not `-z`.
4. **Build the CP4 argument frontier** (`BUILD-CP4-ARGUMENT.md`) — the moat.
5. **Wire the factory to run constantly** (`BUILD-FACTORY-COORDINATION.md`) — `next_action` + the chain.

---

## 4. THE HONEST STATE

- **The root is clean and organized** (AGENTS read-order, VISION-CHUNKS, 13 layer pages, docs_state).
- **The migration/ folder is now clean** (v3 current, shared coordination, v2 archived).
- **The OG site/MCP/examples are real + useful** (43 routes, 29 MCP tools, 7 examples, timeline, lemma).
- **The factory + the two-sided build work** (full-system test 11/11 on a real untranslated work).
- **The known gaps**: the static-vs-live read surface, the 6 divergent contracts, the `-z` misuse, the
  CP4 argument frontier, the corpus-wide graduation (only one work run end-to-end, not the full queue).

---

## 5. THE AUTONOMOUS FACTORY — IT'S REAL, IT RAN, HERE'S HOW TO RESTART

**The autonomous factory EXISTS and WORKS** (verified):
- **The machinery**: `pipeline/start_overnight.sh` (one-command launcher) · `factory_loop.sh` (the
  repeat-loop driver) · `factory_loop_watchdog.sh` (cron restart) · `factory_scheduler.py` (the DAG
  pass) · `factory_batch.py` (per-layer + audit) · `object_registry.py` (the ledger).
- **It RAN today** (last run 10:47-10:56, audit ledger has 6,577 entries). It registered the
  Sārdhatriśatikālottarāgama as SOURCE, ran the Hermes T1 worker, and **committed 8 real Stk T1 objects**
  to the registry (T1 went 306→314). The audit shows the commits at 19:28-19:30.
- **It is NOT currently running** (cron watchdogs = 0, no live process).

### The real registry state (verified)
```
SOURCE: 32039 · T1: 314 (incl. 8 Stk) · L0: 791 · ARGMAP: 50 · L2: 3 · L200: 5 · C1: 3 · THEME: 1
```

### How to restart it (for the next agent)
```bash
bash pipeline/start_overnight.sh start      # starts the factory loop + live RAW→EN runner + installs cron watchdogs
bash pipeline/start_overnight.sh status     # are they alive?
tail -f /tmp/opencode/factory-loop.log      # the live factory log
python3 pipeline/factory_certificate.py     # the integrity cert (PASS = clean)
```

### The honest caveat
The factory ran T1 on 8 Stk verses and committed them — but it has NOT advanced Stk through L0/L2/L200/C1
yet (those are 0 for Stk). The full chain on one work is the corpus-wide graduation. The factory is real;
the continuous full-chain run is the next build (`BUILD-FACTORY-COORDINATION.md` — drive it with
`next_action`).
