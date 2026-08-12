# Shared Reuse Matrix and Build Doctrine

## Own only what is uniquely Pāṭala

### Own
- stable IDs into premodern source traditions;
- exact provenance;
- ReviewEvent/correction history;
- Sanskrit-philosophy expert gold;
- historical SemanticAlignment;
- argument-under-interpretation IR;
- dependency/crux structure;
- expert adjudications.

### Reuse
- Sanskrit morphology;
- generic MT metric models;
- generic LLM eval execution;
- generic annotation engines/UX;
- generic peer-review workflow;
- generic argument interchange;
- global literature/citation discovery.

## Reuse map

| Need | Reuse | Pāṭala layer |
|---|---|---|
| morphology | Vidyut, Heritage, SanskritShala | selected analysis + disagreement + proof |
| corpora | Ambuda/DCS/GRETIL | historically ranked evidence |
| translation metric | xCOMET, MetricX | Sanskrit error ontology + expert gold |
| metric statistics | mt-metrics-eval | fixture provenance/tasks |
| eval runner | Inspect AI | BenchmarkFixture/Run |
| review workflow | OpenReview concepts | executable ReviewEvent/ImpactReport |
| argument exchange | xAIF/oAMF | Philosophy IR |
| annotation | INCEpTION/Hypothesis | stable refs + scholarly semantics |
| scholarly KG | ORKG | source-grounded historical argument graph |
| literature | Elicit/S2/ResearchRabbit | domain-specific source relations |

## Do not rebuild
1. Sanskrit morphology.
2. Generic LLM eval framework.
3. Generic MT metric statistics.
4. Conference peer-review infrastructure.
5. Web annotation infrastructure.
6. A global academic citation graph.
7. A generic argument ontology incompatible with established interchange.
8. A single translation score as truth.

## Build
1. RAW Sanskrit → auditable L0.
2. Sanskrit-philosophy error taxonomy.
3. T1–T4 benchmark family.
4. AuditFinding with deterministic/proposed/calibrated classes.
5. ReviewFinding tied to exact proposition/source refs.
6. ReviewEvent → DerivedState → ImpactReport.
7. Crux/counterfactual dependency analysis.
8. ResearchQuestion-centered Workbench.

## Recommended execution sequence
A. Factory: one-passage RAW-L0 → IPVV blind replay → human error review → Kramasadbhāva cross-work.
B. Benchmark+Audit: fixture schema + Inspect adapter → Audit v0 → feedback capture → v1 proposed → detector-specific calibration.
C. Review: native argument → generated essay → external thesis section → crux diagnostics.
D. Workbench: tiny review UI → ResearchQuestion workspace → collaboration.

## Shared model-run provenance
Every model-driven artifact/run stores:
- model/provider/version;
- prompt/skill version;
- git SHA;
- tools allowed;
- fixture/rubric version;
- runtime/cost;
- raw output;
- review outcome.

## Fail-closed policy
- unresolved canonical ref: no accepted output;
- P0 structural failure: no semantic promotion;
- analyzer disagreement: preserve CONFLICT;
- insufficient evidence: abstain;
- model timeout: bounded retry then explicit failure;
- review rejection/revision: preserve prior version/history.

## Licensing
Verify current licenses and model/data terms before vendoring or redistribution. Prefer adapters/dependencies to source copying. COMET code is Apache-2.0 but models can have separate terms; INCEpTION is Apache-2.0; Inspect AI is MIT; Hypothesis h is BSD-2-Clause. Check every data corpus separately.
