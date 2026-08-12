# EXPERIMENT — E1-fidelity (C1→L2 fidelity baselines)

*2026-08-12. The first real baseline run in the Pāṭala ML research lane.*

## Research question
For the C1→source fidelity task, does dense retrieval beat lexical BM25 overlap?

## Method
- **Task:** `tasks/PATALA-FIDELITY.jsonl` — query = the passage's C1 commentary, relevant = its own
  passage, index = **L2 only** (non-leaky: query and indexed field are different representations).
- **Corpus:** the 49 published IPVV passages (read-only from the store).
- **Retrievers:** BM25 · dense (sentence-transformers `all-MiniLM-L6-v2`) · hybrid (0.5/0.5).
- **Metrics:** Recall@5, MRR@10, with 300-iteration bootstrap CI + paired delta vs BM25.

## Result (see experiments/fidelity_bm25_dense_hybrid.json)
| retriever | R@5 (CI) | MRR@10 | delta MRR vs BM25 | p |
|---|---|---|---|---|
| BM25-l2 | 0.837 [0.73,0.94] | 0.802 | — | — |
| dense-l2 | 0.837 [0.73,0.94] | 0.768 | −0.035 | 0.083 |
| hybrid-l2 | 0.837 [0.71,0.92] | 0.800 | −0.002 | 0.740 |

## Interpretation
**Plain dense embeddings do not beat BM25 for C1→source fidelity.** The difference is not significant
and numerically favors BM25. This is an honest negative: for this task, lexical overlap is the stronger
signal. It argues the discriminating signal for Pāṭala is **structured/graph** (see_also, key terms,
relations) — not a fancier text encoder. This directly supports the frozen strategy's focus on the
**hybrid scholarly graph** over generic embeddings.

## Reproducibility
- dataset version: patala store @ git HEAD of this session (49 passages)
- split: N/A (fidelity, per-passage; no train/test yet)
- embedding model: `sentence-transformers/all-MiniLM-L6-v2`
- random seed: patala_ml.metrics.RNG = 20260812
- hardware: CPU (no CUDA)
- metrics: experiments/fidelity_bm25_dense_hybrid.json

## Decision
- ADOPT BM25 as the retrieval baseline (it is the thing to beat).
- DO NOT adopt generic dense embeddings for this task without graph/structured signal.
- NEXT: run the STRUCTURE task (see_also-pair classification) + add a graph/relational feature arm to
  test whether scholarly relations improve over text — the flagship question.

## Error categories (to add next)
- cases where the C1 does NOT retrieve its own passage (BM25 failures) — inspect whether they share
  few surface terms (the target for structured signal).
