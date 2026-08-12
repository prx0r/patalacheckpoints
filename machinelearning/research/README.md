# PĀṬALA ML RESEARCH WORKSPACE

*2026-08-12. The **separate ML research lane** — completely independent of the Pāṭala app
(`app/`, `data/corpus/`, the other agent's integration). This tree does CPU-only ML baselines,
benchmarks, and experiments over the *published* corpus. It reads the store read-only; it never writes
to it.*

## Layout
```
patala_ml/            the package
  corpus.py           load the published IPVV passages (L2 + C1 + terms + see_also)
  retrieval.py        BM25 / dense / hybrid retrievers (CPU)
  eval.py             benchmark runner (mean + bootstrap CI + paired delta)
  metrics.py          retrieval + classification + theme metrics, bootstrap CI, paired test
  generate_tasks.py   derive benchmark fixtures from REAL see_also edges (no invented labels)
tasks/                generated task files (PATALA-RETRIEVAL/-STRUCTURE/-FIDELITY)
experiments/          per-experiment outputs (metrics.json etc.)
RESOURCES.md          the curated dataset/model/tool registry
```

## Setup
```bash
cd research
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt          # core (BM25 + clustering) — ~200M, CPU
# ONLY for the dense/hybrid arms (heavier, ~1G): install CPU-only torch + sentence-transformers
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install sentence-transformers
# optional: export HF_TOKEN=...  (stored in gitignored .env, never committed)
```

## The venv is disposable — don't protect it
The 5.1G GPU-build venv was rebuilt **CPU-only → 1.4G** (the 2.7G NVIDIA CUDA libs were pure waste on
a GPU-less box). If storage is tight, **delete `.venv` and re-create with `requirements.txt` on demand** —
the committed code + requirements fully reproduce it. The models here are tiny baseline probes
(MiniLM ~90MB), NOT the product.

## What this lane actually does (honest scope)
Only **retrieval baselines**: does lexical (BM25) or semantic (dense) retrieval find the right passage
for a query? The results (BM25 ≥ dense for C1→fidelity; hybrid best R@5 on hard retrieval) are the
*evidence* that no model gets adopted until it beats these. This feeds the truth-engine's
**premise→passage** step. The truth engine (argument verification: Nyāya gate, Bayesian scorer, Lean)
is a different, more valuable system in `/root/projects/.meta/misc/truth-engine/` + `sanskritree/proof_engine/`.

## Run the first baseline
```bash
. .venv/bin/activate
python -m patala_ml.generate_tasks --out tasks      # derive fixtures from real see_also
python experiments/run_fidelity.py                   # BM25 vs dense vs hybrid on C1→L2 fidelity
```

## The first result (2026-08-12, honest + statistically-gated)
On `PATALA-FIDELITY` (query = C1 commentary, index = L2 only; 49 items, 300 bootstrap iters):
```
BM25-l2   R@5=0.837  MRR@10=0.802
dense-l2  R@5=0.837  MRR@10=0.768  delta=-0.035 p=0.083   (NOT better)
hybrid-l2 R@5=0.837  MRR@10=0.800  delta=-0.002 p=0.740   (tie)
```
**Interpretation:** for C1→source fidelity, plain dense embeddings do NOT beat lexical BM25 overlap.
This is a real, publishable-in-principle negative — it justifies *not* chasing generic embeddings for
this task and points the need toward **structured/graph** signal (the whole POINT of Pāṭala) rather than
a fancier text encoder.

## Discipline (frozen, from MLUSEINPATALA.md)
- benchmark before model · fixed held-out · expose before infer · human-review gate
- no learned model adopted until it beats a baseline on a fixed held-out set
- statistical rigor (mean + CI + paired test), leakage-safe splits, reproducibility
- The app integration (C1 wiring, themes, verify floor) is the OTHER agent's lane — this tree reads the
  store only.
