# THE SHARED BUILD-DIRECTIVE SET — what to build, with the real OG patala file references

*2026-08-14 · status: THE COMPLETE BUILD MAP for agentgraph · every piece ip-graph is missing, what to
build, why, and the REAL OG patala files to reference. Populated by agentpatala from a deep-dive of v2 +
OG patala. Each BUILD-* file is self-contained and points at actual files.*

---

## THE ONE-LINE

> **ip-graph has the modern kernels + read plane; OG patala has the REAL Sanskrit data pipeline (harvest,
> bibliography with editions, factory, state machine, translations). The build wires them into ONE
> autonomous organism.**

---

## THE BUILD-FILES (the complete set)

| Build file | What to build | The real OG patala files to reference |
|---|---|---|
| `BUILD-INGESTION-HARVEST.md` | wire the external harvest (R2 adapters → SOURCE) into `ingestion_organism` | `ingestion/adapters/{pandit,gretil,sarit,csalt,iiif,ngmcp,viaf,wikidata}.py` · `ingestion/r2.py` · `pipeline/{translation_targets,agent3_queue,acquire_sivaqueue_targets}.py` · `data/corpus/targets/sivaqueue.json` |
| `BUILD-BIBLIOGRAPHY-IDENTITY.md` | the bibliography ↔ identity ↔ factory link (with editions) | `data/corpus/atlas-bibliography.json` (254) · `data/atlas/{audited,bibliographySeed,sanskritreeImportSeed,sivaqueueSeed}.ts` · `data/atlas/bibliographyTypes.ts` · `python/patala_core/atlas/{migrate,resolver,api,adapter}.py` |
| `BUILD-FACTORY.md` | drive the organism with the real factory (workers + scheduler + batch + commit) | `pipeline/{factory_scheduler,factory_batch,factory_loop.sh,factory_loop_watchdog.sh,factory_certificate,factory_rebuild,factory_status,factory_run}.py` · `pipeline/{t1,l0,argument_map,l1_l2,l200,c1,theme,essay,education}_worker.py` · `pipeline/object_registry.py` · `pipeline/autonomy.py` · `contracts/CANONICAL-DAG.yaml` |
| `BUILD-HERMES-ORCHESTRATION.md` | wire Hermes as the execution kernel + the Agent-3 coordinator | `pipeline/model.py` · `handover/hermes/{HERMES-AGENT3-FACTORY-COORDINATOR,DEV-PLAN,CANONICAL,BACKEND-MODEL}.md` · `docs/{HERMES-ORCHESTRATION-REVIEW,agent3potential}.md` · `docs/global/HERMES-CALLING.md` · `mcp/index.mjs` (29 tools) |
| `BUILD-TRANSLATION-STATE.md` | the per-work FSM + the internal translation inventory | `pipeline/corpus_state.py` · `data/corpus/downloads/translation-state-ledger.json` · the 71 jsonl + 11 T3 + 28 T1 + 63 L200 + 63 C1 |
| `BUILD-CONTRACTS-CONVERGENCE.md` | **THE #1 BUILD** — converge the SIX divergent ReviewEvent/Authority defs into ONE canonical contract set (the CHECKPOINTS five contracts) | `source-evidence/schema/{contracts_human_authority,typed_scholarly_object}.py` · `python/patala_core/{objects,authority}.py` · `pipeline/review_engine.py` · ip-graph `lib/{review,epistemic}.py` |
| `BUILD-CP4-ARGUMENT.md` | the argument frontier (CP4, where lanes converge) — the philosophical IR + engines ip-graph lacks | `machinelearning/research/patala_ml/{argument,crux_engine,nyayagate,aspic_adapter,aifgraph,proposition_layer,builders,gold002..005}.py` · `machinelearning/_ACTIVE/ARGUMENT-IR-VISION.md` · `pipeline/ingest_ipvv_argmap_golds.py` |
| `BUILD-FACTORY-COORDINATION.md` | the modern scheduler (`next_action`) driving the full chain T1→…→EDUCATION, gated by Nyāya + Bayesian + ARG golds | `docs/FACTORY.md` · `pipeline/factory_scheduler.py` · ip-graph `lib/next_action.py` · `machinelearning/research/patala_ml/{nyayagate,strength,gold002..005}.py` |
| `BUILD-GATE-INFRA.md` | the gate infrastructure + the endgamebuild health survey (what's OPEN/FIXED, for agentgraph review) | `source-evidence/evals/patala/tasks/*` (NAT, argument_recovery, atlas_qa) · the 5 golds · `endgamebuild/{INFRA-INVENTORY,PROJECT-AUDIT}.md` · ip-graph `lib/{integrity_gate,evidence_ledger,verification_ensemble}.py` |
| **`BUILD-OPENPATALA.md`** | **the OpenAlex-for-Sanskrit product build (CONFIRMED) — wiring plan + checkpoints** | `openpatala/` · `python/patala_core/atlas/{api,adapter,migrate,resolver}.py` · `pipeline/object_registry.py` · `ingestion/adapters/{pandit,gretil,sarit}.py` · ip-graph `lib/{source_registry,evidence_ledger,context_compiler,bundle_router,seo}.py` |
| `WHAT-TO-BUILD.md` | the overall architecture + the 4 build links | (the master summary) |

---

## THE INVENTORY OG PATALA HAS THAT IP-GRAPH LACKS (the substance)

| Asset | Count | Real files |
|---|---|---|
| External harvest adapters | 9 | `ingestion/adapters/*.py` |
| R2 snapshot store | 1 | `ingestion/r2.py` |
| Bibliography (thin) | 254 works | `data/corpus/atlas-bibliography.json` |
| Bibliography (rich, editions) | 11 + 59 works | `data/atlas/audited.ts` + `bibliographySeed.ts` |
| Atlas identity machinery | 4 modules | `python/patala_core/atlas/*.py` |
| Per-work state machine | 111 works | `pipeline/corpus_state.py` + the ledger |
| Factory workers | 9 | `pipeline/*_worker.py` |
| Factory scheduler/loop/batch | 8 | `pipeline/factory_*.py/.sh` |
| Translated jsonl | 71 works | `data/corpus/downloads/translations/*.jsonl` |
| T3 finals | 11 | `sanskritree/translations/05_t3_final/` |
| T1 gold | 28 chunks | `sanskritree/.../ipvv/01_t1/`+`02_t1/` |
| L200 proof audits | 63 | `sanskritree/.../ipvv/l200/` |
| C1 commentaries | 63 | `sanskritree/.../ipvv/c1/read/` |
| Hermes model client | 1 | `pipeline/model.py` |
| MCP tools | 29 | `mcp/index.mjs` |
| The Stk work (untranslated test) | 1 (298 verses) | `data/corpus/sources/sardhatrisatikalottara/` |

---

## THE BUILD ORDER (why)

1. **Ingestion first** (`BUILD-INGESTION-HARVEST.md`) — no point compiling a graph without real Sanskrit.
2. **Identity second** (`BUILD-BIBLIOGRAPHY-IDENTITY.md`) — the bibliography (with editions) is the spine.
3. **Factory third** (`BUILD-FACTORY.md`) — the real workers produce + commit the objects.
4. **Hermes fourth** (`BUILD-HERMES-ORCHESTRATION.md`) — the execution kernel + Agent-3 profiles.
5. **State machine fifth** (`BUILD-TRANSLATION-STATE.md`) — the per-work FSM makes ALL works autonomous.

---

*This is the complete build-directive set. Every BUILD-* file names the real OG patala files agentgraph
should reference, so it can build without re-deriving. ip-graph brings the modern kernels + read plane;
OG patala brings the real Sanskrit data pipeline. The build wires them into ONE autonomous organism.*
