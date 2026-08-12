# BUILD NOTES — ML lane progress log

*2026-08-12. A running log of what's been built in the ML research lane, in order, so nothing is lost
and the next session knows exactly where things stand.*

---

## 1. The working ML package (`machinelearning/research/patala_ml/`)

| Module | What it does | Tests |
|---|---|---|
| `corpus.py` | loads the 49 published IPVV passages (L2 + C1 + terms + see_also) | — |
| `c1corpus.py` | loads the 63 C1 read/ files as clustering nodes (V1 fine-grained preserved) | via cluster |
| `cluster.py` | hybrid-graph clustering (See-also + shared KEY TERMS, Louvain + overlap) | test_cluster 14 |
| `strength.py` | Bayesian claim-strength scorer (weighted_lbf → Certainty) — truth-engine port | test_strength 24 |
| `argument.py` | Claim-v3 ArgumentProposal (5-member Nyāya, conclusion, tension_id, gate, Bayesian strength) | test_argument 29 |
| `builders.py` | 4 ALTERNATIVE argument-builders (STRUCT/LEXICAL/GRAPH/PUSHING) for comparison | via compare |
| `c1metrics.py` | C1 machine metrics (novelty, boundary, hedge, anachronism, terms, localness) | — |
| `pushing.py` | parse PUSHING sessions into PushingRecords (question → gem → passages) | — |
| `retrieval.py` | BM25 / dense / hybrid retrievers (field-aware) | — |
| `eval.py` | benchmark runner (mean + CI + paired delta) | — |
| `metrics.py` | retrieval + classification + bootstrap CI + paired test | — |

**Test totals: 67/67 passing** (cluster 14 + strength 24 + argument 29).

## 2. Experiments (the results)

| Experiment | Result | File |
|---|---|---|
| **E1 fidelity** | BM25 ≥ dense for C1→L2 (dense delta −0.035, p=0.08) | `E1-fidelity-REPORT.md` |
| **E2 retrieval** | hybrid best R@5 (0.735) on hard retrieval | `retrieval_bm25_dense_hybrid.json` |
| **Cluster** | 9 clean V2/V3 themes + V1 dialectic flagged editorially | `clusters.json` + report |
| **C1 metrics** | calibrated on the IPVV gold standard (novelty 0.15, hedge/boundary read c1_source) | `run_c1metrics.py` |
| **Argument comparison** | **B-STRUCT wins gt-overlap (0.417); coverage is a REAL metric (Spearman +0.94 vs gt)** | `compare_arguments.py` |

## 3. Key findings (the science)

1. **B-STRUCT is the best argument-builder** — curated see-also + key-terms premises capture the human
   argument's concepts; lexical/centrality/question approaches don't.
2. **`coverage` is a real quality metric** (Spearman +0.94 vs ground-truth overlap); **resolvability and
   diversity are noise** (no variance). This is the "which metrics are bs" answer.
3. **BM25 ≥ dense for fidelity** — lexical overlap is the stronger signal for C1→source; dense helps on
   paraphrased retrieval (hybrid best).
4. **The V1 block doesn't cluster usefully** — it's a dense dialectic; handle editorially.

## 4. The alignment (ML-ALIGNMENT.md)

Every ML artifact maps onto existing Pāṭala types (EvidenceVerification/EvidenceRole/Certainty/
EpistemicState/EvidenceUse) + the truth-engine weighted_lbf. Nothing parallel.

## 5. Next (in logical order)

1. **AIF-informed ArgumentGraph** — propositions ≠ inference ≠ conflict nodes (external review §6).
2. **EssayPlan** — the essay as a scholarly-decision object (thesis/claims/objections/evidence), then
   prose as a rendering (external review §7).
3. **Build the winning builder's argument → EssayPlan → essay** on one theme (the end-to-end proof).
4. **Validate each transformation** (the gold-chain methodology, external review §10) — not the final essay.

## 6. The data foundation status (what's "for any text")

- Schemas: L0 rigid, T1→C1 rigid (schema.py), argument = Claim-v3 (built), provenance 4-level (designed).
- The IPVV is the gold standard / calibration corpus; the agnostic contract freezes what works.
- `contracts/` directory (the reusable validator set) = the remaining consolidation task.

## 7. AIF graph + EssayPlan (built 2026-08-12)

- **`aifgraph.py`** — the AIF-informed argument graph: `InfoNode` (proposition) ≠ `InferenceNode`
  (scheme/move) ≠ `ConflictNode` (objection/rebuttal). `check()` validates REAL invariants:
  inference/conflict node integrity, **premises resolve to passages** (conclusions are derived), implicit
  premises flagged for review. No invented numeric scores.
- **`essayplan.py`** — the EssayPlan: the essay as a scholarly DECISION (thesis/claims/objections/
  evidence sets), reviewed BEFORE prose. `plan_from_argument()` derives it from an ArgumentProposal
  (conclusion → thesis, premises → claims, each tracing to passages).
- **test_essayplan.py 17/17** — B-STRUCT on CL-3 → AIF graph → EssayPlan, validated for structural
  soundness + resolvability.
- **Total ML suite: 84/84 passing.**
- **Discipline kept** (per the user's warning): judged on structural soundness + auditable grounding,
  NOT quantitative metrics that are likely bs. (The comparison experiment already proved coverage is
  real and resolvability/diversity are noise — I did not bolt fake scores onto the AIF graph or EssayPlan.)
