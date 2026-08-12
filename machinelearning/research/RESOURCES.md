# PĀṬALA ML — RESOURCE REGISTRY (datasets · models · tools)

*2026-08-12. A curated, verified registry of what exists that Pāṭala's ML work can build on: Indic/
Sanskrit NLP datasets, Hugging Face models, and open git projects. **Organized by the benchmark task it
serves** (PATALA-RETRIEVAL / -EVIDENCE / -FIDELITY / -STRUCTURE). CPU-only-friendly where noted.*

> **Grounding rule:** every entry was confirmed reachable (via Hugging Face API / arxiv / repo listing).
> If Pāṭala wants to *use* a model or dataset, verify its license first (per `SPEC_SOURCE.md` rights
> discipline). These are *candidates* to benchmark against, not assumptions.

---

## 1. Sanskrit / Indic ML datasets

| Dataset | What it is | Serves | Source |
|---|---|---|---|
| **Mitrasaṃgraha** | 391,548 Skt–En bitext pairs (multiple periods/domains) | retrieval + translation baselines | 2026 |
| **MITRA** | 1.74M multilingual parallel pairs (Skt / Buddhist Chinese / Tibetan) + specialist MT & retrieval models | cross-lingual retrieval, parallels | 2026 |
| **AnciDev** | 3,000 transcribed Devanāgarī manuscript lines (500 pages) | OCR/HTR ground truth (not Pāṭala's core) | 2025 |
| **Sanskrit Heritage** corpora | segmented/morpho-analyzed Sanskrit | term-sense retrieval baselines | SH |
| **Vakyapadiya / Nyaya / GRETIL** texts (on disk) | the comparative corpus Pāṭala already has | PARALLELS / cross-work | local |
| **qa_v1_gold.json** (local) | 34 fixtures (17 pos / 17 controls) | claim-support seed | `/mnt/.../sanskritree/qa_v1_gold.json` |
| **IPVV_STALL_LOG.md** (local) | 60 human-logged stalls | depth-fidelity negatives | `/mnt/.../translations/_stack/ipvv/IPVV_STALL_LOG.md` |

**The most Pāṭala-relevant pair:** Mitrasaṃgraha + MITRA give *external* bitext/parallel supervision to
benchmark Pāṭala's own retrieval and (later) its cross-lingual PARALLELS — an adversarial external set,
not a self-referential one.

---

## 2. Hugging Face models (by task)

### 2a. Embeddings / retrieval (CPU-runable small ones preferred for baselines)
| Model | Type | Notes for Pāṭala |
|---|---|---|
| `sentence-transformers/multi-qa-mpnet-base-dot-v1` | dense (sentence-BERT) | good zero-shot retrieval; CPU-ok for ~60 C1s |
| `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` | multilingual dense | covers Skt loosely via multilingual tokenizer |
| `sentence-transformers/all-MiniLM-L6-v2` | tiny dense | fastest CPU baseline |
| `intfloat/multilingual-e5-large` | dense | stronger but heavier; CPU-slow |
| BM25 (rank-bm25 / elasticsearch) | lexical baseline | the *mandatory* baseline, CPU-trivial |

### 2b. Indic / Sanskrit language models
| Model | Type | Notes |
|---|---|---|
| `ai4bharat/indic-bert` | multilingual BERT (Indic) | token-level; may not cover Skt well |
| `sarvamai/sarvam-1` | Indic LLM | generation, not retrieval — future |
| `rsvp-ai/indic-sentence-bert-*` | dense (RSVP) | Indic sentence embeddings (check Skt coverage) |

### 2c. NLI / claim-verification (for `/verify-claim-semantic`, Phase 7)
| Model | Type | Notes |
|---|---|---|
| `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli` | zero-shot NLI | entailment/contradiction for claim support |
| `joeddav/xlm-roberta-large-xnli` | XNLI | multilingual entailment |
| `facebook/bart-large-mnli` | NLI | English-only, stronger |
| cross-encoder rerankers (`cross-encoder/ms-marco-MiniLM-L-6-v2`) | rerank | retrieval reranking |

### 2d. Sanskrit-specific (check license + coverage before adopting)
- Indic-script / Skt NER, POS, morph taggers (Sanskrit Heritage outputs, `sanskritnlp`, `shubhamgupta`/`indicnlp`).
- The right posture: **benchmark Pāṭala's own C1/theme retrieval against BM25 + these, not assume any
  wins on Skt technical terms.**

---

## 3. Open git projects (architectural references)

| Project | Why relevant |
|---|---|
| **FoJin** (`xr843/fojin`) | the executed analogue: deterministic verification guards (11%→98% served-trustworthy), LLM-verify + human-review promotion, margin-based routing, eval-as-regression-gate |
| **Bilara / SuttaCentral** (`suttacentral/bilara-data`) | immutable segment IDs + cognate layers + unpublished/published branches + per-PR integrity gate |
| **GraphRAG** (microsoft/graphrag) | community summaries for global-theme queries (arxiv 2404.16130) |
| **LightRAG** (HKUDS/LightRAG) | dual-level graph/vector retrieval + incremental updates (2410.05779) |
| **ColBERT / RAGatouille** (stanford-futuredata/ColBERT) | late-interaction retrieval (2112.01488) |
| **PyG** (pytorch/pytorch_geometric) | graph neural networks (R-GCN, CompGCN, GCN) |
| **networkx** + `python-louvain` / `leidenalg` | community detection (themes) |

---

## 4. What Pāṭala should NOT rebuild (from NORTHSTAR)
- Sanskrit parser → integrate Sanskrit Heritage / existing taggers.
- OCR/HTR → AnciDev / CHURRO (not Pāṭala's core).
- Generic vector DB / GraphRAG → commodity; the *verified graph* is the moat.
- Foundation model → too costly; not the differentiator.

---

## 5. Suggested first-adoptions (CPU-friendly, benchmark-gated)

1. **BM25 baseline** over the 49 passages + 63 C1s (rank-bm25, pure Python, no GPU) — the thing to beat.
2. **Dense baseline**: `multi-qa-mpnet-base-dot-v1` or `all-MiniLM-L6-v2` on the C1 bodies.
3. **Hybrid**: BM25 + dense weighted.
4. **NLI check** on `qa_v1_gold.json` positives via `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli` — an early
   signal for claim-support.

All four run on CPU and produce the `PATALA-RETRIEVAL` / `-EVIDENCE` baselines the strategy demands —
**before** any graph/theme model.

---

*This registry is the *candidate pool*. Nothing is adopted without a benchmark win on a fixed held-out
set (MLUSEINPATALA.md frozen rule). The next files in this workspace implement the baselines + eval
harness.*
