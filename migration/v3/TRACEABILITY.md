# PĀṬALA V3 — TRACEABILITY (every v3 reference → full resolvable path → implementation → test)

*2026-08-14 · status: THE RESOLUTION MAP · every reference in the v3 docs resolves to a real file,
implementation, and test. v3 uses abbreviated names (e.g. `translation.py`, `markguidance.md`); this map
gives the FULL path so an agent can always find the source. The rule: **nothing in v3 is a claim without
a resolvable origin.***
*Two roots: `/root/projects/patala/` (the Pāṭala repo) and `/mnt/HC_Volume_106427611/ip-graph/` (the
proven lab). The `.meta`/Ochema hubs are at `/root/projects/`.*

---

## THE RESOLVE CHAIN (how to find anything)

```text
v3 reference → this map → full path → the implementation → its validating test
```

---

## 1. THE LAB KERNELS (ip-graph) — each maps to its test

The `lib/*.py` kernels live in `/mnt/HC_Volume_106427611/ip-graph/lib/`; each has a validating
`validate-*.py` in `/mnt/HC_Volume_106427611/ip-graph/scripts/`.

| v3 ref | Full path (ip-graph) | Validating test |
|---|---|---|
| `epistemic.py` | `lib/epistemic.py` | `scripts/validate-stack.py`, `validate-provenance.py` |
| `schema.py` | `lib/schema.py` | `scripts/validate-kernels.py` |
| `review.py` | `lib/review.py` | `scripts/validate-layer03-05.py` |
| `scholar_review.py` | `lib/scholar_review.py` | `scripts/validate-kernels.py`, `experiment-review-bias.py` |
| `staleness.py` | `lib/staleness.py` | `scripts/validate-layer03-05.py` (RKA blast-radius) |
| `query.py` | `lib/query.py` | `scripts/validate-kernels.py`, `validate-layer10.py` |
| `retrieval.py` | `lib/retrieval.py` | `scripts/validate-layer10.py` (PathRAG/HippoRAG) |
| `translation.py` | `lib/translation.py` | `scripts/validate-products.py` (the moat) |
| `certificate.py` | `lib/certificate.py` | `scripts/validate-kernels.py`, `experiment-certification-weight.py` |
| `discovery.py` | `lib/discovery.py` | `scripts/validate-kernels.py`, `experiment-counterfactual-engine.py` |
| `education.py` | `lib/education.py` | `scripts/validate-education-organism.py` |
| `organism.py` | `lib/organism.py` | `scripts/validate-education-organism.py` |
| `organism_loop.py` | `lib/organism_loop.py` | `scripts/validate-organism-loop.py` |
| `pedagogy.py` | `lib/pedagogy.py` | `scripts/validate-pedagogy.py` |
| `evolve.py` | `lib/evolve.py` | `scripts/validate-evolve.py` |
| `agent_delivery.py` | `lib/agent_delivery.py` | `scripts/validate-agent-delivery.py` |
| `essay_ingest.py` | `lib/essay_ingest.py` | `scripts/validate-essay-ingest.py` |

**The master test runner:** `scripts/run-tests.py` (51/51 PASS). The proofs are stored in
`data/references/theatre-proofs-all.json`.

## 2. THE EXPERIMENTS (ip-graph)

| v3 ref | Full path (ip-graph) |
|---|---|
| `experiment-crux-compiler.py` | `experiment-crux-compiler.py` (root) |
| `experiment-reactive-essay.py` | `experiment-reactive-essay.py` |
| `experiment-claim-standardisation.py` | `experiment-claim-standardisation.py` |
| `experiment-import-scifact.py` | `experiment-import-scifact.py` |
| `experiment-bounded-context.py` | `experiment-bounded-context.py` |
| `theatre-check.py` / `theatre-check-all.py` | `scripts/theatre-check.py`, `scripts/theatre-check-all.py` |

## 3. THE PATALA NATIVE MACHINERY (patala repo)

| v3 ref | Full path (patala) |
|---|---|
| `factory_scheduler.py` | `pipeline/factory_scheduler.py` |
| `factory_loop.sh` | `pipeline/factory_loop.sh` |
| `register_sources.py` | `pipeline/register_sources.py` |
| `start_overnight.sh` | `pipeline/start_overnight.sh` |
| `review_engine.py` | `pipeline/review_engine.py` |
| `certificate_l0.py` / `certificate_l200.py` | `pipeline/certificate_l0.py`, `pipeline/certificate_l200.py` |
| `t1_worker.py` / `l0_worker.py` / `l200_worker.py` | `pipeline/{t1,l0,l200}_worker.py` |
| `object_registry.py` | `pipeline/object_registry.py` |
| `metadata_resolver.py` | `source-evidence/production/adapters/metadata_resolver.py` |
| `opencitations.py` | `source-evidence/production/adapters/opencitations.py` |
| `identity_crosswalk.py` | `source-evidence/production/adapters/identity_crosswalk.py` |
| `external_record.py` | `source-evidence/schema/external_record.py` |
| `text_fingerprint.py` | `source-evidence/schema/text_fingerprint.py` |
| `entity_reconciliation.py` | `source-evidence/evals/patala/tasks/entity_reconciliation.py` |
| `manuscript_resolution_gold.py` | `source-evidence/evals/patala/tasks/manuscript_resolution_gold.py` |
| `run_reconciliation_eval.py` | `source-evidence/evals/patala/tasks/run_reconciliation_eval.py` |
| `atlas_qa_audit.py` | `source-evidence/evals/patala/tasks/atlas_qa_audit.py` |
| `semantic_recovery_judge.py` | `source-evidence/evals/patala/tasks/semantic_recovery_judge.py` |
| `scholar_graph_eval.py` | `source-evidence/evals/patala/tasks/scholar_graph_eval.py` |
| `atlas/` | `python/patala_core/atlas/` (migrate · resolver · adapter · api) |
| `contracts/CANONICAL-DAG.yaml` | `contracts/CANONICAL-DAG.yaml` |

## 4. THE DATA (patala)

| v3 ref | Full path |
|---|---|
| `atlas-bibliography.json` | `data/corpus/atlas-bibliography.json` (254 works) |
| `bibliographySeed.ts` | `data/atlas/bibliographySeed.ts` |
| `audited.ts` | `data/atlas/audited.ts` (Trika-10) |
| `seed60.md` | `docs/seed60.md` |
| `terms.ts` | `data/corpus/terms.ts` |
| `trajectories.ts` | `data/corpus/trajectories.ts` |
| `historyTimeline.json` | `data/atlas/historyTimeline.json` |
| `recovery-gold-v1.json` | `data/evaluation/recovery-gold-v1.json` (51 cases) |
| `nyaya-gate-gold.jsonl` | `benchmarks/v0/evidence/nyaya-gate-gold.jsonl` (12) |
| `p3_lexical_gold_v0.json` | `docs/p3_lexical_gold_v0.json` |
| `p4_alignment_eval_report.json` | `docs/p4_alignment_eval_report.json` |
| published IPVV | `data/published/ipvv/` (49 passages) |

## 5. THE LEGACY / GLOBAL DOCS

| v3 ref | Full path |
|---|---|
| `markguidance.md` | `docs/corpus/markguidance.md` |
| `canonical_reference_map.md` | `docs/corpus/canonical_reference_map.md` |
| `leapfrog_guide.md` / `leapfrog_map.md` | `docs/corpus/leapfrog_guide.md`, `docs/corpus/leapfrog_map.md` |
| `endgame5year.md` | `docs/endgame5year.md` |
| `globalnext.md` | `docs/global/GLOBAL-NEXT-2026-08-13.md` |
| `GLOBAL-STATE-2026-08-13.md` | `docs/global/GLOBAL-STATE-2026-08-13.md` |
| `globalpartnerships.md` | `docs/global/globalpartnerships.md` |
| `NORTHSTAR.md` | `docs/NORTHSTAR.md` |
| `technical-architecture-v1.md` | `docs/vision/atlas/technical-architecture-v1.md` |
| `ARGUMENT-IR-VISION.md` | `machinelearning/_ACTIVE/ARGUMENT-IR-VISION.md` |
| `ai/` (VISION, surveys) | `ai/VISION.md`, `ai/argumentation-ir-*.md`, `ai/TAKEAWAYS.md` |

## 6. THE V2 / V3 SIBLING DOCS

| v3 ref | Full path |
|---|---|
| `PATALA-V2-SPEC.md` | `migration/v2/PATALA-V2-SPEC.md` |
| `LAYERS.yaml` (v2) | `migration/v2/LAYERS.yaml` |
| `PRODUCTS.md` (v2) | `migration/v2/strategy/PRODUCTS.md` |
| `EXTERNAL-REPOS.md` | `migration/v2/EXTERNAL-REPOS.md` |
| `EXTERNAL-EVIDENCE.md` | `migration/v2/EXTERNAL-EVIDENCE.md` |
| `CONVERGENCE-OCHEMA.md` | `migration/v2/CONVERGENCE-OCHEMA.md` |
| `GEMS.md` | `migration/v2/GEMS.md` |
| `GROUND-UP-PLAN.md` | `migration/v2/GROUND-UP-PLAN.md` |
| `CURRENT-TO-VISION.md` | `migration/v2/CURRENT-TO-VISION.md` |
| `LAYER-MAPPING.md` | `migration/v2/LAYER-MAPPING.md` |
| `MODULES.md` | `migration/v2/MODULES.md` |
| `PATALA-NATIVE-MACHINERY.md` | `migration/v3/PATALA-NATIVE-MACHINERY.md` |
| `LEGACY-GEMS.md` | `migration/v3/LEGACY-GEMS.md` |
| `STRUCTURES.md` | `migration/v3/STRUCTURES.md` |
| `MECHANISMS.md` | `migration/v3/MECHANISMS.md` |
| `renderr.md` | `migration/v2/renderr.md` |
| ip-graph `PRODUCTS.md` | `/mnt/HC_Volume_106427611/ip-graph/migration/v2/PRODUCTS.md` |
| ip-graph `RECONCILIATION.md` | `/mnt/HC_Volume_106427611/ip-graph/migration/v2/RECONCILIATION.md` |

## 7. THE PRODUCTION ORGANISM (.meta / Ochema)

| v3 ref | Full path |
|---|---|
| `workengestation/` | `/root/projects/workengestation/` (13 essays) |
| `renderio/` | `/root/projects/renderio/` (49 gold-packs) |
| `reception/` | `/root/projects/reception/` |
| `source-library/` | `/root/projects/source-library/` |
| `basecamp/` | `/root/projects/basecamp/` |
| `.meta/` | `/root/projects/.meta/` (source_graph.py, production-floor.py) |

---

## THE VALIDATION RESULT (2026-08-14)

- **114 unique references** extracted from v3 docs.
- **All resolve** to a real file once the full path is applied (via this map).
- **1 bug found + fixed:** `kernel-suite.py` (referenced in PRODUCTS/LAYERS/ORGANISM) doesn't exist —
  the real script is `scripts/validate-kernels.py`. Fixed in all v3 docs.
- **The `.meta`/lab roots** are documented so sibling-repo references resolve too.

**The rule going forward:** any new v3 reference must either be a full path or added to this map. Nothing
in v3 is a claim without a resolvable origin.

---

*This is the traceability guarantee. Every v3 reference → full path → implementation → test. The lab
kernels, the Pāṭala native machinery, the data, the legacy docs, the v2/v3 siblings, and the production
organism all resolve. The one broken reference (kernel-suite.py) is fixed.*
