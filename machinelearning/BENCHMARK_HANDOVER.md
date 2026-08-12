# BENCHMARK HANDOVER — the Pāṭala Benchmark v0 seed

*2026-08-12. For the ML master. The seed fixtures already exist across the codebase; this
documents them so Benchmark v0 (MLUSEINPATALA.md Phase 1) is built from real data, not from
nothing. The seed is the *discipline*; formalizing it into the task-suite is the ML work.*

---

## 1. The seed assets (verified on disk)

| Asset | Where | What it provides |
|---|---|---|
| **gold.ts** | `/root/projects/patala/data/corpus/gold.ts` | 2 expert-checked gold decisions (Kramasadbhāva 1.8: nirānanda, devadeveśī) — `must_accept` / `must_not` / `required_uncertainty` |
| **QA v1 gold** | `/mnt/HC_Volume_106427611/sanskritree/qa_v1_gold.json` | 34 fixtures (17 positives / 17 clean controls) for reader-QA / claim-support tasks |
| **Stall log** | `/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/IPVV_STALL_LOG.md` | 60 human-logged stalls (argument/term/prose failures) — the negatives for depth-fidelity + claim-support |
| **IPVV passage corpus** | `/root/projects/patala/data/published/ipvv/` | 49 published passages with source + L2 + **C1 (verse_commentary[])** + c1_source — the retrieval/evidence substrate |
| **QA toolchain** | `/mnt/HC_Volume_106427611/sanskritree/translations/tools/qa_*.py` | the v0/v1/v2 evaluators (scaler, reader-QA, fidelity) — ready-made scorers |
| **Themes** | `/root/projects/patala/data/corpus/themes.ts` + `/api/themes` | deterministic theme proposals (shared lemmas) — the theme-discovery substrate |

## 2. What each benchmark task draws from (the mapping)

| Task (MLUSEINPATALA §3) | Seed source |
|---|---|
| passage retrieval | the 49-passage corpus (source + L2) |
| term-sense retrieval | `c1_source.key_terms` + term trajectories |
| claim → support | qa_v1_gold positives + C1 evidence |
| claim → counterevidence | stall-log negatives + `/api/verify/counterevidence` markers |
| C1 → source fidelity | c1_source (SUMMARY/EXPLANATION) + source text |
| theme relationship | `themes.ts` (deterministic proposals) + qa_v1_gold |
| translation-crux retrieval | gold.ts cruxes + the stall-log |

## 3. The discipline to carry forward (from the ML plan)

- **Benchmark before model** — no INFER adopted until it beats a baseline on the held-out set.
- **Small-but-hard** (50–100 fixtures) with deliberately difficult negatives (shared-vimarśa vocab,
  different doctrinal job).
- **Task-specific suite** — PATALA-RETRIEVAL / -EVIDENCE / -FIDELITY / -STRUCTURE, so a model can't
  game the aggregate.
- **Statistical rigor** — mean + bootstrap CI + delta vs baseline + paired test + error categories.
- **Leakage rules** — passage → chunk → vimarśa → work-held-out; the transfer result is
  train-on-IPVV-test-on-another-work.
- **EXPERIMENT ≠ PRODUCTION** — a meaningful experiment is legitimate even if it loses; adoption
  needs benchmark win + cost + interpretability.

## 4. The ground truth the ML master needs to know

The IPVV stack is now **fully wired into Pāṭala** (this session):
- 49 passages published as lazy JSON, each with source + L2 + **C1 verse_commentary[]** + c1_source.
- `/read` renders the Commentary toggle (multi-C1 for V1 passages).
- `/api/themes` + `get_themes` MCP tool expose deterministic theme proposals.
- `/api/verify/*` (quote, claim-structure, trace-dependency, counterevidence) expose the
  deterministic verification floor.

So the ML work can now **retrieve, cluster, and verify over the actual corpus** — not test fixtures.
The seed above is the starting point; formalize it into the task-suite, then run the baselines.
