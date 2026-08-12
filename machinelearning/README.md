# machinelearning/ — Pāṭala's ML workspace (organized)

*2026-08-12. The ML workspace, organized into **ACTIVE** (the living doctrine + current work) and
**ARCHIVE** (superseded / historical / no-longer-actionable — kept, never deleted). **Start with
`_ACTIVE/AGENTS-DOCTRINE.md`.** The enforcement gate `theatre_check.py` lives in the root.*

> **Nothing is "real" because code exists.** It becomes real only when independent gold + blind eval +
> metric + human adjudication show it does what its name claims. See `_ACTIVE/AGENTS-DOCTRINE.md`.

---

## 1. READ FIRST — the ACTIVE doctrine (in order)

| File | What it is |
|---|---|
| `_ACTIVE/AGENTS-DOCTRINE.md` | **the master anti-theatre rule** (both agents). The 3 categories, 9-field contract, epistemic labels, banned words, abstention, lineage, falsification |
| `_ACTIVE/CLAIMS.md` | the project's self-audit ledger (P-001..P-010) — update honestly as you work |
| `_ACTIVE/COMPONENT-CONTRACTS.md` | the 9-field anti-theatre contract per component |
| `_ACTIVE/AGENT1-HANDOVER.md` | the working doctrine (axioms, recurring errors, tone) |
| `_ACTIVE/MLUSEINPATALA.md` | the frozen ML strategy + the north-star rule |

## 2. The vision (the north star)

| File | What it is |
|---|---|
| `_ACTIVE/dualagentvision.md` | the full vision: one scholarly derivation graph, 13 phases, CP0–CP12 |
| `_ACTIVE/dualagentvision-ADAPTED.md` | the checkpoint map (what our infra covers) |
| `_ACTIVE/ARGUMENT-GOLD-VISION.md` | **the current vision**: Argument Gold + DebateFrame/SemanticAlignment unblock the gate |

## 3. The current work (the active build)

| File | What it is |
|---|---|
| `_ACTIVE/NYAYA-GATE-CANDIDATE-V1.md` | the frozen, measured Nyāya gate result (defect 4/5, FP 0/5, abstain 1/2) |
| `_ACTIVE/SEMANTIC-COMMENSURABILITY.md` | the anti-fake-contradiction layer (DebateFrame / SemanticAlignment) |
| `_ACTIVE/DEVPLAN.md` | the consolidated execution plan (Argument Gold = the next build) |
| `_ACTIVE/SPEC_EPISTEMIC_PROPAGATION.md` | the epistemic-evidence-propagation contract |
| `_ACTIVE/ML-ALIGNMENT.md` | every ML artifact maps onto Pāṭala types |
| `_ACTIVE/BUILD-NOTES.md` | the running progress log |
| `_ACTIVE/HONEST-AUDIT-OWN-STRUCTURES.md` | the no-BS inventory of what we built (real vs hollow) |

## 4. The reference material (active, but reference-only)

| File | What it is |
|---|---|
| `_ACTIVE/TRUTHENGINE-FULL-AUDIT.md` | the 22-doc truth-engine inventory (Nyāya gate = best asset) |
| `_ACTIVE/TRUTHENGINE_TO_PATALA_MAPPING.md` | reuse mechanisms, reject the ontology |
| `_ACTIVE/SANSKRITREE-LEAN-REVIEW.md` | the honest Lean verdict (don't build on it) |
| `_ACTIVE/mlcurriculum.md` | the verified 26-paper arxiv curriculum (context seeding) |
| `_ACTIVE/ml-truthmap.md` | the truth-engine review |
| `_ACTIVE/PLATFORM_PROVENANCE_PRESERVING_GENERATION.md` | the provenance principle |

## 5. ARCHIVED (superseded / historical — kept, never deleted)

| File | Why archived |
|---|---|
| `_ARCHIVE/LOGICAL-ORDER.md` · `DEVPLAN_AGNOSTIC_CONTRACT.md` · `SPEC_CONSOLIDATED_BUILD.md` | superseded by `DEVPLAN.md` |
| `_ARCHIVE/WIRE-NYAYA-GATE.md` | superseded by the gate-freeze + ARGUMENT-GOLD-VISION |
| `_ARCHIVE/SPEC_ALTERNATIVE_ARGUMENT_BUILDERS.md` | the builder comparison was RETIRED as circular |
| `_ARCHIVE/HONESTY-CLEANUP.md` · `ZOOMOUT-REVIEW.md` | historical records of the cleanup |
| `_ARCHIVE/MLVISION.md` · `VISION-COMPUTABLE-TRADITION.md` · `HOW-IT-FITS.md` · `GAPS.md` · `PATALA_AS_LIBRARY_ENGINE.md` | superseded by `dualagentvision-ADAPTED.md` + the doctrine |
| `_ARCHIVE/PATALAML.md` · `REVIEW_PATALAML_VS_CODEBASE.md` · `mlreview.md` · `mlpipeline.md` · `mllogical.md` · `mlpushing.md` | the original exploration (historical) |
| `_ARCHIVE/SPEC_THEME_CLUSTERING.md` · `SPEC_THEME.md` · `THEMES_PILOT_REPORT.md` · `themes_pilot.py` · `SPEC_STAGE2_CLUSTER.md` | themes piloted; CP3 not done — kept for when themes resume |
| `_ARCHIVE/SPEC_PUSHING_METHOD.md` · `SPEC_LOGICAL_ARGUMENTS_GOLD.md` · `SPEC_ARGUMENT_TRUTH_PACKET.md` · `COMPOUNDING_RESEARCH_SYSTEM.md` · `CONTEXT_ENGINEERING.md` | the PUSHING/compounding thread (historical) |
| `_ARCHIVE/EDUCATION_VISION.md` · `geometric.md` · `SYSTEM_GROWTH_AND_HERMES.md` | vision/other-lane |
| `_ARCHIVE/SPEC_L0_PROOF.md` · `SPEC_L0_STANDARDIZATION.md` · `IPVV-STACK-INTEGRATION.md` | L0/other-lane (Agent 2's) |
| `_ARCHIVE/DUAL_AGENT_TRACK.md` | superseded by `AGENTS-DOCTRINE.md` + the checkpoint docs |
| `_ARCHIVE/SPEC_RIGID_DATA_CONTRACT.md` | superseded by `SPEC_EPISTEMIC_PROPAGATION.md` |
| `_ARCHIVE/ML-ARGUMENT-REVIEW-CORRECTED.md` | the external review (historical; distilled into the doctrine) |

---

## The enforcement tool

- **`theatre_check.py`** (root) — the mechanical anti-theatre gate. Run
  `python3 machinelearning/theatre_check.py --status` before claiming any component is "done."

## The handovers (in `handover/agent-1-ml/`)
- `CHECKPOINTS-ML.md` — this lane's goals (CP0/CP2/CP3/CP4)
- `SESSION-2026-08-12.md` — the full session record
- `NEXT-STEPS.md` — the exact execution (Argument Gold build)

## Sources / sync
The `SPEC_THEME_*`, `PATALAML`, `PLATFORM_PROVENANCE_PRESERVING_GENERATION` docs were mirrored from
`sanskritree/translations/_stack/ipvv/specs/`. The originals live there too (now archived here). Keep
in sync if edited.
