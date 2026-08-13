# PĀṬALA — CANONICAL INFRASTRUCTURE INVENTORY ("WHAT EXISTS, WHERE, DON'T REBUILD")

*2026-08-13. The consolidated inventory of EVERYTHING already built. Read this before building
anything. It maps the existing infra, the canonical navigation, the engines, the schemas, the
external-tool integrations, and the REAL gaps. **If it's listed here, do not rebuild it — extend it.***

> **Compass + map (read FIRST, in order):**
> 1. `VISION_AND_NAVIGATION.md` — the compass (vision, 8-step progression, where everything lives).
> 2. `docs/INDEX.md` — the flat canonical map (single source of truth per concern).
> 3. `docs/vision/CORE-BIBLE.md` — the whole vision as one zoomable map.
> 4. `handover/CHECKPOINTS.md` — the shared execution map (CP0–CP4 gates).
> 5. `handover/agent0-coordinator/INDEX.md` — the agent-system map (A0–A8 architecture).
> 6. `docs/global/patala-full-audit-bundle/FULL_AUDIT.md` — the existing full audit + `AUDITED_FILES.md` + `REUSE_VS_BUILD.json`.
> 7. `docs/vision/essayguide.md` — the essay/education/review research-program guide.

---

## 1. THE CORE (do not rebuild)

| Concern | Exists at | Status |
|---|---|---|
| Canonical object envelope | `source-evidence/schema/derived_scholarly_object.py` + `typed_scholarly_object.py` | built, tested |
| Scholar evidence profile | `source-evidence/schema/source_evidence_profile.py` (biblio_work/witness/span/source_assertion/corroboration_event) | built, tested |
| Human authority (review) | `source-evidence/schema/contracts_human_authority.py` (ReviewEvent/Proposal/Adjudication/Promotion) | built, tested |
| Epistemic evidence primitive | `machinelearning/research/patala_ml/strength.py` (Bayesian, honestly scoped) | built, tested |
| Truth-engine → Pāṭala mapping | `machinelearning/_ACTIVE/TRUTHENGINE_TO_PATALA_MAPPING.md` | documented (don't port full ontology) |

## 2. THE FACTORY (Agent 2 — do not rebuild)

- `pipeline/object_registry.py` — versioned registry + **atomic/single-writer** (concurrency-fixed)
- `pipeline/factory_scheduler.py` / `factory_batch.py` / `factory_certificate.py` / `factory_rebuild.py` / `factory_status.py` / `catalog.py`
- Workers: `t1_worker.py` · `l0_worker.py` · `argument_map_worker.py` · `l1_l2_worker.py` · `l200_worker.py` · `c1_worker.py` · `theme_worker.py` · `essay_worker.py` · `education_worker.py`
- Canonical DAG: `contracts/CANONICAL-DAG.yaml`
- Rebuild engine + impact: `factory_rebuild.py` (A2-18 DependencyImpactReport added)
- Review engine + ReviewBundle: `pipeline/review_engine.py` + `review_bundle.py`
- Scholar oracle: `pipeline/scholarly_oracle.py` (make_source_assertion / make_corroboration / run_vertical — tested)
- Live systems: `start_overnight.sh` (RAW→EN runner + factory loop, watchdog-protected)

## 3. THE ML / RESEARCH ENGINES (Agent 1 — do not rebuild)

`machinelearning/research/patala_ml/`:
- Argument: `argument.py` · `builders.py` · `aspic_adapter.py` · `aifgraph.py`
- Nyāya gate: `nyayagate.py` (bounded, never truth)
- Golds: `gold002.py` … `gold005.py` (ARG-GOLD-002..005 with scholarly_corroboration)
- Propositions: `proposition_layer.py` · Crux: `crux_engine.py` · Synthesis: `synthesis_core.py`
- Essay: `essay.py` · `essay_compiler.py` · `essayplan.py` · `essayverify.py` · `essaysentence.py`
- Education: `education_compiler.py` + `education_ir.py`
- Themes: `theme_discovery.py` · `kcore.py` · `cluster.py`
- Pushing/retrieval: `pushing.py` · `retrieval.py` · `semantic_alignment.py`
- Layered scholarship: `layered_scholarship.py` (INTERPRETATION ≠ EVIDENCE)

## 4. THE EVAL / BENCHMARK PLANE (do not rebuild)

`source-evidence/evals/patala/tasks/`:
- Atlas NAT: `atlas_nat.py` + `atlas_nat_natural.py` (51 frozen natural cases, non-circular)
- ARGMAP: `argmap_contract.py` · `argmap_eval.py` · `argmap_ipvv_eval.py`
- Argument recovery: `argument_recovery_bench.py` (P0, the judge)
- Warrant: `warrant_reconstruction.py` · Essay: `essay_bench.py` · Edu: `edu_bench.py`
- Source authority: `source_authority.py`
- Cross-lane contract: `evaluation_candidate.py` + `evaluation_finding.py`
- Gold: `data/evaluation/recovery-gold-v1.json` (51 cases)

## 5. EXTERNAL TOOLS — **all documented, few integrated** (the real gap)

26 tools documented in `source-evidence/docs/tools/` (+ `MANIFEST.json` + offline `docs-cache/`):

| State | Tools |
|---|---|
| **Integrated (real adapters)** | GROBID (`adapters/grobid_live.py`), Crossref, OpenAlex (`adapters/metadata_resolver.py`) |
| **Partial / reference** | Zotero, OpenCitations, Docling, Hypothesis |
| **Docs only (NOT built)** | AnyStyle, Unpaywall, Tantivy, PaperQA2, SciRAG, s2orc, CRAG, **INCEpTION**, **Recogito**, ORKG, RO-Crate, OpenReview, COAR Notify, Manubot, STORM, RAiD, citevqa, valsci-sciatlas |

**The real external-tools gap:** turn the documented plan into working adapters for INCEpTION
(annotation/gold lab), OpenCitations (citation graph), and the identity crosswalks (ORCID/ROR).

## 6. THE ATLAS (do not rebuild)

- `python/patala_core/atlas/` — `migrate.py` (Postgres schema: work/edition/witness/surrogate/etext/source/person/institution/external_identifier/authority_evidence/rights), `adapter.py`, `resolver.py` (per-dimension authority + rights-aware gates), `api.py` (OpenAlex-style /works//editions//search)
- Migration: `migrations/versions/0001_authority_graph_schema.py`
- **Real gap:** no `scholarly_claim`/`publication` table (the SCHOLARSHIP graph side) — but the substrate (`source_assertion`+`corroboration_event` in source_evidence_profile.py + scholarly_oracle.py) already covers this at the schema level.

## 7. THE APP / API / MCP

- `app/api/` — 50+ routes (works, texts, passages, manuscripts, search, verify/*, resolve, themes, education, journey, recommend, context, stats, term-proposals, crosswalks)
- `mcp/` — MCP server (`index.mjs`)
- `lib/`, `components/`, `docs-site/`, `openpatala/`

## 8. THE CANONICAL READ-ORDER (the compass — was here all along)

```
VISION_AND_NAVIGATION.md → docs/INDEX.md → docs/vision/CORE-BIBLE.md
→ THE_COMPANION.md (sanskritree) → handover/CHECKPOINTS.md
→ the audit bundle → docs/vision/essayguide.md
```

---

## 9. THE REAL GAPS — STATUS (updated 2026-08-13)

| Gap | Status |
|---|---|
| **Recovery scorer semantic matching** (P0) | ✅ DONE — `semantic_recovery_judge.py` (2-stage: embedding align + structured judge; offline fallback + LLM swap-in) |
| **INCEpTION annotation/gold bridge** (P1) | ✅ DONE — `annotation_bridge.py` (W3C-Web-Annotation export/import, round-trip verified) |
| **OpenCitations adapter** (P2) | ✅ DONE — `adapters/opencitations.py` (independence + SOURCE_ECHO detection) |
| **ORCID/ROR identity crosswalks** (P3) | ✅ DONE — `adapters/identity_crosswalk.py` (name-variant→Person, institution→ROR) |
| **Scholar-graph evaluation** (P4) | ✅ DONE — `scholar_graph_eval.py` (SourceAssertion+CorroborationEvent suffices; quality is measurable) |
| **Continuous semantic QA on Atlas** (P5) | ✅ DONE — `atlas_qa_audit.py` (authority-inflation/completeness/rights audit) |

**Flagged for review:**
- ⚠️ **Hermes model-config bug**: `model.py` sets `HERMES_MODEL` env (→ "Model not supported"); the
  config uses provider `opencode-go` (not `deepseek`). Blocks the LLM-judge path + any factory model
  call that overrides the model. The pilot's T1/ARGMAP worked via config default.
- ⚠️ **Atlas bibliography thin**: `atlas-bibliography.json` (254 recs) is 1/8 ATLAS-100 fields
  complete (all flagged by the P5 audit); the rich `audited.ts` (Trika-10) has full depth. ATLAS-100
  needs the rich fields backfilled from the TS bibliography.
- ⚠️ **Repo history rewrite** (owner decision): the in-copyright PDFs are untracked now but still in
  prior git history (destructive filter-repo, deferred).

## 10. RECONCILIATION-ENGINE LAYER (the ecosystem reframe, built 2026-08-13)

The partnership files (`docs/positioningpartners.md`, `docs/global/globalpartnerships.md`,
`docs/vision/vision-14-manuscript-to-scholarly-asset.md`) position Pāṭala as the reconciliation /
connective layer over Gyan Bharatam/OCHS/NGMPP/IFP/Muktabodha/GRETIL/SARIT. Built the concrete layer:

| Piece | Status | Where |
|---|---|---|
| **P4 MANUSCRIPT-RESOLUTION-GOLD** | ✅ | `evals/.../manuscript_resolution_gold.py` — 10 frozen cases, FALSE_MERGE_RATE primary |
| **P3 entity reconciliation engine** | ✅ | `evals/.../entity_reconciliation.py` — typed CandidateMatch (EXACT/PROBABLE/POSSIBLE/CONFLICT/UNRESOLVED) |
| **P3↔P4 loop** | ✅ | `evals/.../run_reconciliation_eval.py` — FALSE_MERGE_RATE=0, abstains 30% |
| **P2 ExternalRecord + adapter framework** | ✅ | `schema/external_record.py` — raw-immutable record + ReconciliationAdapter contract + maturity ladder |
| **Text fingerprints** | ✅ | `schema/text_fingerprint.py` — incipit/explicit/ngram/MinHash + candidate_rank |

The deep philosophy/argument stack (Track B) is unchanged and still the moat; this adds the
reconciliation layer (Track A) so the two meet on the same canonical IDs.

---

*If you're about to build something, check §1–§7 first. If it's listed, extend it. If it's not, it may be in the compass docs — read those before writing code.*
