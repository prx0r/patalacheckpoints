# Pāṭala Product Research Pack — 2026-08-12

Anchor doctrine: `prx0r/patala` commit `619b7c8ff2a94e2d09b7cd0c63f24cce3230e950`

https://github.com/prx0r/patala/commit/619b7c8ff2a94e2d09b7cd0c63f24cce3230e950

Projects:
1. Factory — raw Sanskrit → audited MACHINE_PROPOSED L0.
2. Pāṭala Benchmarks — T1 SOURCE / T2 TRANSLATION / T3 INTERPRETATION / T4 ARGUMENT.
3. Pāṭala Audit — translation/comparison/terminology.
4. Pāṭala Review — argument/paper/thesis research compiler.
5. Pāṭala Workbench — research creation inside the evidence graph.
6. **Pāṭala Atlas — the Sanskrit Research Graph ("OpenAlex for Sanskrit")**: the authoritative
   identity/provenance layer the factory is downstream of. Models textual transmission
   (Work→Edition→Witness→Surrogate→Transcription→E-text→Source), reconciled lazily across
   NCC/NMM/NGMCP/GRETIL/SARIT/Muktabodha + library catalogs + IIIF. Storage: Postgres (entity truth)
   + R2 (content-addressed artifact truth) + event log (history truth); search is a disposable
   projection. Mostly formalizes the built bibliography + quality signal + catalog + registries.
   See `06_ATLAS/RESEARCH_AND_BUILD.md` + Vision 15 + `docs/vision/atlas/atlas-engineering-blueprint.md`
   + `docs/vision/source-resolution/source-resolver-design.md`.

Core conclusion: reuse mature infrastructure for morphology, MT evaluation, eval execution, annotation, review workflow and argument interchange. Pāṭala should own stable historical refs, provenance, expert corrections, Sanskrit-philosophy gold, argument-under-interpretation, semantic alignment and executable review history.

Doctrine:
- deterministic checks may make strong claims;
- model scholarly judgments remain MACHINE_PROPOSED;
- calibration requires held-out expert gold;
- Benchmark + Audit are one coupled program;
- every correction should be convertible into a benchmark candidate.
