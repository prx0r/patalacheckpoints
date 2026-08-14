# THE GATE INFRA + ENDGAMEBUILD SURVEY — the surrounding infrastructure (for agentgraph review)

*2026-08-14 · status: THE GATE + HEALTH INVENTORY · the complete gate infrastructure (Nyāya, Bayesian,
ARG golds, the eval/benchmark plane, integrity) + the endgamebuild health survey (what's OPEN, what's
FIXED). This is for agentgraph to REVIEW — the surrounding infra that makes the factory's output real,
and the honest gaps that need fixing. Reference the ACTUAL files.*

---

## PART 1 — THE GATE INFRASTRUCTURE (what makes a result real, not theater)

### 1. The ML gate engines (`/root/projects/patala/machinelearning/research/patala_ml/`)
| File | What it is |
|---|---|
| `nyayagate.py` | **the Nyāya gate** — `gate_claim()` + `check_viruddha_graph()`; bounded, NEVER truth (validity ≠ soundness) |
| `strength.py` | **the Bayesian engine** — `ClaimStrength` (prior/posterior/log_bayes_factor); the evidence-strength primitive under stated assumptions |
| `gold002.py` … `gold005.py` | **the ARG golds** — the 4 argument golds with `scholarly_corroboration` |
| `crux_engine.py` | the Crux primitive (minimal unresolved proposition) |
| `argument.py` | the argument model (premises/inference/conclusion/defeaters) |
| `aspic_adapter.py` · `aifgraph.py` · `proposition_layer.py` | the argumentation engines |

### 2. The eval/benchmark plane (the anti-theatre gates) — `source-evidence/evals/patala/tasks/`
| File | What it gates |
|---|---|
| `atlas_nat.py` + `atlas_nat_natural.py` | **51 frozen natural cases** (non-circular) — the atlas NAT |
| `argument_recovery_bench.py` | **P0, the judge** (the recovery benchmark) |
| `semantic_recovery_judge.py` | the 2-stage recovery scorer (embedding align + structured judge) |
| `argmap_contract.py` / `argmap_eval.py` / `argmap_ipvv_eval.py` | the ARGMAP eval |
| `warrant_reconstruction.py` · `essay_bench.py` · `edu_bench.py` | the per-layer NATs |
| `source_authority.py` | the source-authority gate |
| `evaluation_candidate.py` + `evaluation_finding.py` | the cross-lane contract |
| `atlas_qa_audit.py` | the continuous Atlas QA (authority-inflation/completeness/rights) |
| `atlas_quality_scorecard.py` | the Atlas quality scorecard |

### 3. The 5 golds (the frozen evidence) — all verified
- `data/evaluation/recovery-gold-v1.json` (51 cases)
- `benchmarks/v0/evidence/nyaya-gate-gold.jsonl` (12)
- `docs/p3_lexical_gold_v0.json`
- `docs/p4_alignment_eval_report.json`
- `source-evidence/evals/patala/tasks/manuscript_resolution_gold.py` (10)

### 4. The review/integrity gates (ip-graph's modern additions)
- `/mnt/HC_Volume_106427611/ip-graph/lib/integrity_gate.py` — the tri-state CLEAN/DEMOTED/EXCLUDED + primary-source gate
- `lib/evidence_ledger.py` — typed evidence events + confidence_kind
- `lib/verification_ensemble.py` — RefChecker + GraphCheck + RARR compose

---

## PART 2 — THE ENDGAMEBUILD SURVEY (the health check, for review)

**Read `endgamebuild/INFRA-INVENTORY.md` + `PROJECT-AUDIT.md`** — the honest project state.

### The DONE gaps (all in endgamebuild/INFRA-INVENTORY.md §9)
| Gap | Status | File |
|---|---|---|
| Recovery scorer semantic matching | ✅ DONE | `semantic_recovery_judge.py` |
| INCEpTION annotation/gold bridge | ✅ DONE | `annotation_bridge.py` |
| OpenCitations adapter | ✅ DONE | `adapters/opencitations.py` |
| ORCID/ROR identity crosswalks | ✅ DONE | `adapters/identity_crosswalk.py` |
| Scholar-graph evaluation | ✅ DONE | `scholar_graph_eval.py` |
| Continuous semantic QA on Atlas | ✅ DONE | `atlas_qa_audit.py` |
| Rich scholarship graph → Postgres | ✅ FIXED | `atlas_persist_rich.py` (3 editions, 8 etexts, 6 scholarly_work, 9 related) |
| Stale schema duplicate dir | ✅ FIXED | deleted |

### The OPEN gaps (the real work — in PROJECT-AUDIT.md §PRIORITY FIXES)
| Gap | Status | What it needs |
|---|---|---|
| **Reconcile IPVV passage ids** | 🔴 OPEN | the published store ↔ jsonl corpus mismatch (richest data 404s) |
| **Live-registry integrity debt** | 🔴 OPEN | `factory_certificate`: **789 bad hashes, 119 conflicts, 19 duplicates** |
| **L1/L1L2 duplication** | 🔴 OPEN | two competing L1/L2 providers (l1_l2_worker vs l1_l2_translate), bare L1 not in DAG |
| **THEME/ESSAY/EDUCATION in the loop** | ⚠️ PARTIAL | `factory_loop.sh` still runs only T1..C1; ARGUMENT/SYNTHESIS no worker |
| **Translation-status casing** | ⚠️ OPEN | `translation_status` vs `translationStatus` divergence |
| **IPVV passage-id / API** | ⚠️ OPEN | `/resolve` + `/context` should serve the richest IPVV data |

---

## WHAT TO BUILD / REVIEW (for agentgraph)

1. **Wire the gates into the factory pass** — the ARGUMENT step gated by `nyayagate` + `strength` +
   the ARG golds (002-005); the eval plane (NAT, argument_recovery) is the anti-theatre proof.
2. **Fix the OPEN endgamebuild gaps** — the IPVV passage-id mismatch (the richest data is 404ing), the
   789 bad hashes / 119 conflicts (registry integrity), the L1/L1L2 duplication.
3. **Review the whole health picture** — `PROJECT-AUDIT.md` is the honest "what works / what's broken".
   The factory_certificate numbers (789/119/19) are the live-data debt to repair.

---

## THE TEST (verify the gates are real)

```bash
# the Nyāya gate on a real claim
python3 -c "
import sys; sys.path.insert(0,'/root/projects/patala/machinelearning/research/patala_ml')
from nyayagate import gate_claim
print('nyaya gate imports:', gate_claim)
"
# the eval plane files exist
ls /root/projects/patala/source-evidence/evals/patala/tasks/atlas_nat.py
```

**Pass when:** the factory's ARGUMENT step is gated by the Nyāya + Bayesian + ARG golds, the eval plane
(51 NAT, argument_recovery) proves every result, and the endgamebuild OPEN gaps (IPVV ids, 789 hashes,
L1L2 dup) are on the review queue.
