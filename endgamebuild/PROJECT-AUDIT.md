# PĀṬALA — FULL PROJECT AUDIT (2026-08-13)

*Parallel read-only audit of every subsystem (factory, ML/research, source-evidence/external-tools,
Atlas, app/API/MCP/data). Run by 5 independent audit agents; consolidated here. This is the honest
state of the whole project — what works, what's broken, what's dead, and the priority fixes. Read
`INFRA-INVENTORY.md` for what exists; this is the HEALTH check.*

---

## AUDIT SUMMARY

| Subsystem | Health | Test status |
|---|---|---|
| Factory/pipeline | ✅ SOLID (machinery green; live-data integrity debt) | 5/5 suites PASS + 5 more |
| ML/research engines | ✅ SOLID (all import; 39/41 tests pass) | 2 stale-test failures |
| Source-evidence/external-tools | ✅ SOLID (schema+adapters+evals) | 10/10 eval self-tests PASS |
| Atlas | ✅ FUNCTIONAL (thin contract green; Postgres reachable) | 3/3 suites PASS |
| App/API/MCP/data | ✅ RICH (42 routes, 20 MCP tools) | static, no dev-server run |

**Overall: the project is healthy and green at its core.** The failures found are stale-data/test-drift
and live-data-integrity debt, not broken architecture. The real gaps are: unwired high layers,
IPVV-passage id mismatch in the API, an unpopulated rich scholarship graph in Postgres, and scattered
hard-coded machine paths.

---

## 1. FACTORY / PIPELINE AUDIT

### Works (all green)
- Workers: t1/l0/l1_l2/l200/c1/theme/essay/education + argument_map — real generators + deterministic validators.
- Machinery: object_registry (concurrency-safe, atomic), factory_scheduler, factory_batch (failure/retry queue), factory_rebuild (A2-18), factory_certificate, factory_status, catalog.
- Review: review_engine (23/23), review_bundle, scholarly_oracle (13). Canonical DAG = single source of truth.
- **Tests: test_object_events, test_factory_rebuild, test_review_engine, test_review_bundle, test_scholarly_oracle ALL PASS** + test_workers/catalog/scheduler/certificate/status PASS.

### Broken / incomplete
1. **`ARGUMENT` and `SYNTHESIS` layers have NO real worker** — `autonomy.LAYER_HANDLERS` falls back to a stub `generic_generator`; the DAG ends at C1. They're in `LAYERS` but unwired dead-ends.
2. **High layers (THEME→ESSAY→EDUCATION) not reachable via the production factory** — `factory_loop.sh` only runs T1/ARGMAP/L0/L2/L200/C1. Workers exist but nothing triggers them (ESSAY=0, EDUCATION=0 in live data).
3. **`factory_certificate` reports the live registry NON-clean**: duplicates=19, bad_parent_hashes=789, registry_conflicts=119, resume="49 would-recommit". This is live-data integrity debt (the cert logic is correct).
4. **`L1`/`L1L2` duplicated + not in the canonical DAG** — two competing L1/L2 providers (l1_l2_worker.py vs l1_l2_translate.py), no dependency constraints.

### Dead / duplicate
- `factory_run.py` — self-marked OBSOLETE/SUPERSEDED.
- `c1_18.py`, `c1_18_lean.py`, `c1_18_fileref.py` — three legacy variants of one C1-1.8 run.
- `autonomy.py:169-175` generative ESSAY/EDUCATION wiring overwritten by the real workers (dead code).

## 2. ML / RESEARCH AUDIT

### Works
- All 43 `patala_ml/` modules import cleanly. argument/nyayagate/crux/synthesis/proposition/education_ir/theme/strength/layered_scholarship/semantic_alignment/retrieval + 5 gold engines all complete and distinct (not duplicates).
- **Tests: 39/41 PASS.** test_nyaya_gate_wiring, test_crux_engine, test_education_ir, test_layered_scholarship, test_argument_synthesis, test_proposition_layer, test_education_compiler ALL PASS.

### Broken (stale-test drift, not code bugs)
1. **`test_evidence_aware_essay.py` FAIL** — the benchmark artifact uses an old source_id format + NOT_AUDITED gate; the validator is newer than the artifact.
2. **`test_vertical.py` FAIL (5 checks)** — depends on a `/tmp/l0proof/...json` file that doesn't exist (ephemeral) + stale "null field" assertions.

### Dead / portability
- **Hard-coded machine paths**: `c1corpus.py:52`, `vertical.py:34,38` → `/mnt/HC_Volume_106427611/...` + `/tmp/l0proof`.
- `pushing.py` — real engine, no unit tests.
- `experiments/` has 57 scripts; ~12 are one-off dead-ends (adjudicate_cl3, build_goldchain, louvain_stability, etc.). ~8 are real validators (check_*). The `vertical1_*.py` + `run_*_batch.py` set is the active recent work.

## 3. SOURCE-EVIDENCE / EXTERNAL-TOOLS AUDIT

### Works
- Schemas complete + self-consistent (source_evidence_profile, contracts_human_authority, derived/typed_scholarly_object, external_record, text_fingerprint).
- All 5 adapters import cleanly; grobid_live/metadata_resolver/opencitations/identity_crosswalk each have working self-tests.
- **Tests: all 10 eval self-tests PASS** (argument_recovery, semantic_recovery, manuscript_resolution, atlas_nat_natural, essay_bench, entity_reconciliation, atlas_quality_scorecard, atlas_nat, synthesis_nat, warrant_reconstruction).

### Broken / incomplete
1. **`scholar_document.py:164` GrobidAdapter.parse() is a placeholder** — the real parse lives in the separate GrobidLiveAdapter (grobid_live.py). Two GROBID classes; the docstring path never parses.
2. **`argmap_eval.py` FAILs on `argmap-ipvv:V3M-v1`** — "unsupported inference at step 1" (a genuine eval defect on live IPVV).
3. **`opencitations.py` `_same_author()` always returns False** — SAME_AUTHOR classification hard-wired UNKNOWN.
4. **`scholar_document.py:220-227` self-imports** — odd/redundant.

### Dead / dangerous
- **`source-evidence/schema/schema/` — a stale nested duplicate dir** containing an IDENTICAL copy of source_evidence_profile.py and a DIVERGED derived_scholarly_object.py (old review-axis ranking). **Nothing imports it, but it's silent schema drift** — must be deleted.
- `source-evidence/docs/tools/inspect-api/` — empty dir.

### External-tools gap (confirmed)
- **26 tools documented** in MANIFEST.json + docs-cache, but **only 6 have code integration** (grobid, docling, crossref, openalex, opencitations, inspect). **20 are docs-only** (zotero, paperqa, inception, recogito, etc.).

## 4. ATLAS AUDIT

### Works
- resolver.py (per-dimension authority + gates, correct), api.py (OpenAlex-grammar), adapter.py (dual backend), migrate.py (idempotent). Postgres reachable (localhost:5433/patala_atlas, 22 tables).
- **Tests: test_resolver (22), test_api (9), test_adapter (6) ALL PASS.**

### Schema coverage
- 22 tables: BOTH graphs structurally present. Primary-text (work→edition/witness/surrogate/etext→source→passage) ✓. Scholarship graph structurally present via `scholarly_work`/`scholarly_object`/`relationship` ✓.
- **BUT: no `publication` or `scholarly_claim` table** (only the `scholarly_work` stub), and **only the primary-text path is populated** (work=254, authority_evidence=268, but edition=0, scholarly_work=0). The scholarship graph is EMPTY in Postgres.

### Thin-vs-rich mismatch (the key finding)
- `data/corpus/atlas-bibliography.json` (254 recs) = only 4 fields (id/title/translation_status/verified).
- `data/atlas/audited.ts` (Trika-10, 11 recs) = full depth (traditions/period/editions/translations/scholarship/related).
- **The rich data is staged in `atlas-backfill-candidates.json` but NEVER written to Postgres.** The Atlas read API serves only the thin contract.

### Issues
- Hard-coded DB creds (`adapter.py:27`, `resolver.py:212`) + hard-coded ROOT paths.
- Duplicate record `sivadharmottara` across two seed files.
- `verified` bool-in-TS vs string-in-JSON type drift; brittle regex TS parser.

## 5. APP / API / MCP / DATA AUDIT

### Works
- 42 API routes, all importable, 0 unresolved imports. Core read routes serve RICH data (not thin).
- MCP server: 20 tools proxying the HTTP API + review-engine tools. Functional.
- Published corpus: 49 IPVV passages + 25 Kramasadbhāva units.

### Broken / inconsistent (prioritized)
1. **IPVV passage-ID mismatch (the big one)**: published IPVV store uses `pt:passage:ipvv:chunkA-...md` ids, but the segmented jsonl corpus uses `tantra:text:...:V2-A:<slug>`. So `/resolve`, `/context/passages/:id`, `/passages/:id` **404 against the IPVV published layer** (the richest data is only reachable via `/passages/:id/translation`).
2. **No `/api/education` route** despite an `app/learning` UI page.
3. **Stale `/api` index** — doesn't list ~15 real endpoints.
4. **`translation_status` vs `translationStatus`** casing inconsistency across the works/texts routes.
5. **1 dangling atlas relation** (nitya_shodasikarnava → yoginīhṛdaya) + `passages: null` dead key in recovery-gold.
6. **Factory intake state fragmented** across 4 sivaqueue manifests at different completion + 3 sources of truth for "on disk".

### Hard-coded machine paths
- `concordance/route.ts` → `/mnt/HC_Volume_106427611/sanskritree`; MCP TANTRA_CORPUS/TANTRA_API_BASE defaults.

---

## PRIORITY FIXES (ranked)

1. **Reconcile IPVV passage ids** (published store ↔ jsonl corpus) so /resolve + /context serve the richest IPVV data.
2. **Write the rich scholarship graph to Postgres** (the ATLAS-10 backfill → the 22-table schema; add publication/scholarly_claim if needed) — ✅ **FIXED** (`atlas_persist_rich.py`: 3 editions, 8 etexts, 6 scholarly_work, 9 related persisted).
3. **Delete the stale `source-evidence/schema/schema/` duplicate dir** — ✅ **FIXED** (deleted; canonical `derived_scholarly_object` is the one imported).
4. **Wire the high layers (THEME/ESSAY/EDUCATION) into the production factory loop** + give ARGUMENT/SYNTHESIS real workers — ⚠️ **PARTIAL**: THEME added to the scheduler `LAYER_ORDER`; ARGUMENT/SYNTHESIS still no worker; the live `factory_loop.sh` still runs only T1..C1 (needs a deliberate production rewire).
5. **Repair the live-registry integrity debt** (factory_certificate: 789 bad hashes, 119 conflicts) — ⚠️ OPEN (live-data debt; the cert logic is correct).
6. **Refresh the /api index** + add the missing education route — ✅ **FIXED** (`/api/education` added; `/api` index expanded to ~15 more endpoints).
7. **Resolve the L1/L1L2 duplication** — ⚠️ OPEN (L2 canonical; L1L2 AI-worker fallback read by l200/c1; bare L1 legacy side-path not in DAG).
8. **Standardize the translation-status field** casing + unify the sivaqueue intake state model — ⚠️ OPEN.
9. **Portability**: move hard-coded `/mnt/...` + `/tmp` paths to env-config — ✅ **FIXED** for Atlas adapter/resolver + ML c1corpus/vertical (`PATALA_ROOT`/`PATALA_DB_URL`/`PATALA_C1_DIR`/`PATALA_IPVV_DIR`/`PATALA_PROOF_DIR`); still hard-coded in `extract.py`, `concordance/route.ts`, `reingest_grobid.py`.

## FIXED IN THIS AUDIT (commits)

- `source-evidence/schema/schema/` deleted (schema drift).
- `atlas_persist_rich.py` — rich scholarship graph → Postgres (thin-vs-rich gap closed).
- `/api/education` route + expanded `/api` index.
- Env-config machine paths (Atlas + c1corpus + vertical).
- THEME added to the scheduler LAYER_ORDER.

## OPEN / OWNER DECISIONS
- ARGUMENT/SYNTHESIS real workers + wiring THEME/ESSAY/EDUCATION into the live factory loop.
- Live-registry integrity debt (789 bad hashes).
- L1/L1L2 duplication.
- translation-status casing + sivaqueue intake-state unification.
- Remaining hard-coded paths (extract.py, concordance route, reingest_grobid).
- Repo history rewrite (in-copyright PDFs — destructive filter-repo).
- Modern-paper external adapters ~0% coverage for Sanskrit (don't invest further).

---

*The five subsystem audit passes were read-only. The consolidated audit then applied the explicitly
listed safe fixes (schema-drift deletion, rich-scholarship→Postgres, /api/education, env-config paths,
scheduler LAYER_ORDER). This supersedes the older `docs/global/patala-full-audit-bundle/FULL_AUDIT.md`
as the current full-project health check (that one audited an earlier snapshot).*
