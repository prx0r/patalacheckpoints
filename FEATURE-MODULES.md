# FEATURE → MODULE LOCATION INDEX (resolve a feature directly to its code)

*2026-08-14. The map an agent needs to resolve ANY feature by NAME to its actual code locations. The
DIRECTORY-MANIFEST maps folders; this maps FEATURES. Hermes test (2026-08-14) showed an agent couldn't
find `education_compiler.py` by filename (it's buried in `machinelearning/` + `pipeline/`) and had to
content-search. This index fixes that: resolve "education" → its files directly.*

**Usage:** agent, given a feature name → look it up here → read the files. No content search needed.

---

## THE FEATURE → CODE MAP

| Feature | Code (implementation) | Surface (API/site) | Docs |
|---|---|---|---|
| **education** | `machinelearning/research/patala_ml/education_compiler.py` + `education_ir.py` (rule-based compiler) · `pipeline/education_worker.py` (LLM distiller) | `app/api/education/route.ts` · `app/learning/page.tsx` | `docs/vision/education/PATALA-EDUCATION-SYNTHESIS.md` |
| **essay** | `machinelearning/research/patala_ml/essay_compiler.py` · `essayplan.py` · `essay.py` · `essaysentence.py` · `essayverify.py` · `essaygen.py` | — | `docs/vision/essayguide.md` |
| **review** | `pipeline/review_engine.py` · `review_bundle.py` · `source-evidence/schema/contracts_human_authority.py` | `app/api/verify/*` | `docs/vision/vision-06-adversarial-review.md` |
| **argument** | `machinelearning/research/patala_ml/argument.py` · `builders.py` · `aspic_adapter.py` · `aifgraph.py` · `pipeline/argument_map_worker.py` | `app/api/themes/` | `docs/vision/INDEX.md` (CP4) |
| **synthesis** | `machinelearning/research/patala_ml/synthesis_core.py` · `theme_discovery.py` · `cluster.py` | — | `docs/global/globalgoal.md` + `agent1atlas.md` |
| **crux** | `machinelearning/research/patala_ml/crux_engine.py` | — | `docs/global/agent1atlas.md` |
| **proposition** | `machinelearning/research/patala_ml/proposition_layer.py` | — | `docs/global/globalgoal.md` |
| **atlas** | `python/patala_core/atlas/` (adapter/resolver/api) · `pipeline/atlas_backfill.py` · `atlas_persist_rich.py` · `atlas_scholarship_populate.py` | `app/api/works/` · `app/api/texts/` · `openpatala/` | `docs/process/02-atlas.md` |
| **factory** | `pipeline/factory_*.py` (scheduler/batch/certificate/rebuild/status/loop.sh) | `app/api/factory/*` | `docs/process/03-factory.md` |
| **ingestion** | `ingestion/` (asserter.py, r2.py, persistence.py, adapters/*) | — | `docs/process/01-ingestion.md` |
| **translation** | `pipeline/translation_targets.py` · `auto_translate*.py` · `l1_l2_translate.py` · `pipeline/*_worker.py` | `app/api/texts/[id]/translations/` | `docs/TRANSLATION_PROTOCOL.md` |
| **themes** | `machinelearning/research/patala_ml/theme_discovery.py` · `cluster.py` · `kcore.py` | `app/api/themes/route.ts` | `docs/vision/INDEX.md` (CP3) |
| **verification/evals** | `source-evidence/evals/` (Inspect tasks) | — | `docs/process/08-verification-plane.md` |
| **evidence** | `source-evidence/schema/` (contracts) · `source-evidence/production/adapters/` | — | `docs/process/external-tools.md` |
| **attestation** | `pipeline/review_engine.py` (ReviewEvent) · `source-evidence/schema/contracts_human_authority.py` | — | `docs/layers/08-human-authority.md` (the Scholar Attestation Vertical) |

---

## THE RESOLUTION RULE

```text
Agent asked about "education"
  → look up education in THIS index
  → read machinelearning/.../education_compiler.py + pipeline/education_worker.py
  → check app/api/education + app/learning
  → cross-check docs/process/docs_state.py for honest live state
```

This is the layer where feature-name → actual-code resolves. Combined with `DIRECTORY-MANIFEST.json`
(folder → role) and `NAVIGATION.md` (anything → layer), an agent has three resolvers covering every
level: feature → code, folder → role, resource → layer.
