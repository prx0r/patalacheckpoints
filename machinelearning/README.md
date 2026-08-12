# machinelearning/ — Pāṭala's ML workspace

*2026-08-12. The consolidated home for all ML-related material that would otherwise be scattered across
`docs/` and the IPVV translation stack's `specs/`. The authoritative decision on what to build, and why,
is **`MLUSEINPATALA.md`** — read it first.*

---

## The canon (read in this order)

| File | What it is |
|---|---|
| **`MLUSEINPATALA.md`** | **THE canonical recommendation (FROZEN)** — what to do, in what order, with justifications. Start here. |
| **`DEVPLAN.md`** | the comprehensive execution plan — every phase broken into granular steps, each with the files to touch and the test that proves it (test-first, with run commands) |
| `MLVISION.md` | the big picture — how the ML strategy, the corpus, and the site vision compose; and how the whole becomes bigger than FoJin (self-improving scholarly intelligence, Vertical Fidelity, GEN-Z as the depth-conservation proof) |
| `VISION-COMPUTABLE-TRADITION.md` | the **grounded product vision** the ML serves — the multi-resolution knowledge system (epistemic gearbox, misconception maps, semantic-distance ladders, concept journeys, self-explaining corpus), each mapped to the ML primitive that enables it |
| `IPVV-STACK-INTEGRATION.md` | the ground-truth audit of the actual IPVV stack + the current Pāṭala wiring (verified numbers) — re-grounds the ML plan in the real data and exposes the C1-wiring gap |
| `GAPS.md` | implementation-vs-vision gap analysis (what exists vs what the vision wants) |
| `mlreview.md` | the ML review: the two difficulty classes (EXPOSE vs INFER), benchmark-first, FoJin/Bilara lessons |
| `mlcurriculum.md` | the verified 26-paper reading curriculum (every arXiv ID confirmed) + required deliverables |
| `REVIEW_PATALAML_VS_CODEBASE.md` | the honest review: ≥10 of the 20 PATALAML ideas are already built as data/ontology |
| `PATALAML.md` | the original 20-idea ML research roadmap |
| `PLATFORM_PROVENANCE_PRESERVING_GENERATION.md` | the verification floor: "AI proposes ≠ Pāṭala asserts" |
| `SPEC_THEME_CLUSTERING.md` | the theme-discovery mechanism (hybrid graph, 7 edges) |
| `SPEC_THEME.md` | the theme dossier structure |
| `THEMES_PILOT_REPORT.md` | the proven 25-C1 pilot (hybrid graph beats embeddings-only) |
| `themes_pilot.py` | the runnable pilot |
| **`COMPOUNDING_RESEARCH_SYSTEM.md`** | the source-centric HUB model + the PUSHING→argument→essay→learning compounding pipeline (how every text tracks all its outputs) |
| **`SPEC_PUSHING_METHOD.md`** | the mechanical deep-dive formula (the "Logicvid" method), reusable per source — the discovery step before formalization |
| **`DUAL_AGENT_TRACK.md`** | the two-lane split (Agent 1 = ML/research, Agent 2 = integration/content) with the shared contract + handoff protocol |
| **`BENCHMARK_HANDOVER.md`** | the benchmark v0 seed (gold.ts, qa_v1_gold, stall-log) the ML master builds from |
| **`SPEC_LOGICAL_ARGUMENTS_GOLD.md`** | the compounding loop: PUSHING → formal logical argument → truth-engine proof → essay → learning, all tracked on the hub (the highest-value output) |

## The work-directories

- `papers/` — per-paper technical notes (the 20-point template in `TEMPLATE.md`), one per curriculum paper
- `proofs/` — proof notes for NBFNet / GraphGPS / hyperbolic models (`TEMPLATE.md`)
- `decisions/` — implementation decision records (ADRs), `ADR-TEMPLATE.md`

## Sources of these documents

- `GAPS.md`, `mlreview.md`, `mlcurriculum.md` — produced 2026-08-12 from the patala codebase + vision docs
- `PATALAML.md`, `REVIEW_PATALAML_VS_CODEBASE.md`, `SPEC_THEME_*`, `THEMES_PILOT_*`, `themes_pilot.py`,
  `PLATFORM_PROVENANCE_PRESERVING_GENERATION.md` — canonical copies from
  `/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/specs/` (they live there too; this is
  the patala-side mirror so the ML workspace is self-contained).

> **Keep in sync:** if you edit a file in `sanskritree/translations/_stack/ipvv/specs/`, mirror it here,
> and vice-versa. The IPVV stack owns the canonical THEMES spec; this folder owns the ML decision-making.
