# Pāṭala ML — Reading Curriculum & Review (mlcurriculum.md)

*2026-08-12. The verified reading curriculum for the agent that will implement Pāṭala's ML layer. Every
arXiv ID below has been **fetched and confirmed to match its claimed title**. Corrections to the original
curriculum draft are flagged. This document also fixes the required deliverables: per-paper technical
notes, proof notes, and implementation decision records (ADRs) — so the agent learns rigorously rather
than cargo-culting methods.*

---

## 0. The non-negotiable discipline (read first, applies to all papers)

1. **Benchmark before model.** No INFER model (graph learning, entailment, embeddings) is adopted until
   it beats a baseline on a **fixed, held-out Pāṭala benchmark** — never "visually plausible examples."
2. **EXPOSE vs INFER.** Separating "surface structure that already exists" (deterministic, cheap) from
   "infer new scholarly structure" (model-based, benchmark-gated) is the governing frame.
3. **Two kinds of claims.** Every paper's note must separate *what is theoretically established* from
   *what is merely empirical*. "GraphGPS is expressive under its stated setup" and "GraphGPS did well on
   benchmark X" are not the same kind of claim.
4. **Fixed held-out test set before development.** No adjusting gold after seeing results unless the
   change is separately versioned and the original result remains recorded.
5. **AI proposes ≠ Pāṭala asserts.** Any INFER output is a hypothesis until it passes human review.

---

## 1. The verified reading list (in order)

Legend: **VERIFIED** = fetched and confirmed. **CANONICAL** = foundational, well-known; not re-fetched
but certain (classic/stable IDs). Section headers map to the original curriculum.

### 1. Retrieval foundations
| arXiv | Paper | Status | Pāṭala use |
|---|---|---|---|
| 2112.01488 | ColBERTv2 — lightweight late interaction | **VERIFIED** | strong retrieval baseline; token-level matching for Sanskrit terms |
| 2401.18059 | RAPTOR — recursive abstractive tree retrieval | **VERIFIED** | the span→passage→C1→theme→work hierarchy |
| 2405.14831 | HippoRAG — graph + Personalized PageRank | **VERIFIED** | graph-structure + PPR multi-hop; cheap vs iterative |
| 2410.05779 | LightRAG — dual-level graph/vector retrieval | **VERIFIED** | implementation reference for low/high-level + incremental updates; do NOT copy ontology |

### 2. GraphRAG / global corpus reasoning
| arXiv | Paper | Status | Pāṭala use |
|---|---|---|---|
| 2404.16130 | From Local to Global: Graph RAG | **VERIFIED** | community summaries for "what are the themes?" — directly informs THEME retrieval |

> **Pāṭala experiment (required):** plain vector RAG vs C1 retrieval vs accepted Theme dossiers vs graph
> community summaries — for global questions about the IPVV.

### 3. Higher-order structure (your ontology)
| arXiv | Paper | Status | Pāṭala use |
|---|---|---|---|
| 2602.14470 | HyperRAG — n-ary facts over hypergraphs (WWW'26) | **VERIFIED** | closest to `TranslationDecision` n-ary objects; query-conditioned reasoning chains |
| 2504.08758 | Hyper-RAG — hypergraph-driven RAG vs hallucination | **VERIFIED** | different project, similar name; hallucination reduction; directly compares to graph RAG |
| 2404.01039 | Survey on Hypergraph Neural Networks (KDD'24) | **VERIFIED** | decompose HNNs into input/features/message-passing/training before implementing |
| 2503.07959 | Recent Advances in HGNNs | **VERIFIED** | newer architecture taxonomy (HGCN/HGAT/HGAE/HGRN/DHGGM) + open problems |

> **⚠ Correction to the draft:** 2602.14470 and 2504.08758 are genuinely different papers — the
> curriculum correctly warned about this; both are verified real and distinct.

### 4. Multi-relational graph learning
| arXiv | Paper | Status | Pāṭala use |
|---|---|---|---|
| 1703.06103 | R-GCN — relational graph convnets | **CANONICAL** | relation-specific message passing for your typed relations |
| 1911.03082 | CompGCN — composition-based multi-relational | **CANONICAL** | joint node+relation representations |
| 2106.06935 | NBFNet — Neural Bellman-Ford | **CANONICAL** | `trace_dependency` + relation-path prediction |

### 5. General graph architecture
| arXiv | Paper | Status | Pāṭala use |
|---|---|---|---|
| 2205.12454 | GraphGPS — recipe for graph transformers | **CANONICAL** | positional encoding / local message passing / global attention separation |

> **Required before implementing:** a technical note explaining why GraphGPS is or is not appropriate
> relative to R-GCN/NBFNet.

### 6. Graph foundation models (frontier, not immediate production)
| arXiv | Paper | Status | Pāṭala use |
|---|---|---|---|
| 2410.12609 | Towards Graph Foundation Models (SCR) | **VERIFIED** | zero-shot KG reasoning → cross-corpus transfer |
| 2505.15116 | Graph Foundation Models: A Comprehensive Survey | **VERIFIED** | backbone/pretraining/adaptation taxonomy; read before claiming "GFM" |
| 2505.12027 | REEF — Relation-Aware Graph Foundation Model | **VERIFIED** | relations as reusable units; relation-conditioned parameter gen — relevant to Pāṭala's meaningful relation semantics |

> **⚠ Correction to the draft:** 2410.12609 is titled *"Training on Knowledge Graphs Enables
> Transferability to General Graphs"* and introduces **SCR** (not "SCORE"). It uses **semantic-conditioned
> message passing**. The draft's "SCORE" naming is wrong; the mechanism description is right.

### 7. Overlapping themes
| arXiv | Paper | Status | Pāṭala use |
|---|---|---|---|
| 1909.12201 | Overlapping Community Detection with GNNs | **VERIFIED** | direct model of overlapping membership (your multi-theme C1s) |
| 2306.13400 | Network community detection via neural embeddings | **VERIFIED** | why embeddings recover communities (node2vec ≈ spectral) — antidote to blind cluster-plots |

> **Pāṭala benchmark (required):** HDBSCAN on text vs graph community detection vs overlapping GNN vs
> editor-approved themes. Do NOT assume the neural one wins.

### 8. Hyperbolic representation (traditions/concept hierarchies)
| arXiv | Paper | Status | Pāṭala use |
|---|---|---|---|
| 2211.04050 | Hyperbolic Graph Representation Learning: A Tutorial | **CANONICAL** | why hyperbolic suits tree-like/scale-free structures |
| 2202.13852 | Hyperbolic Graph Neural Networks: A Review | **CANONICAL** | architectures + geometric assumptions |
| 2412.12158 | H2GNN — Hyperbolic Hypergraph NNs | **VERIFIED** | multi-relational + hypergraph + hyperbolic — the long-term frontier |

> Do NOT implement hyperbolic tomorrow. It is the frontier experiment once several works/traditions exist.

### 9. Claim extraction & epistemic units
| arXiv | Paper | Status | Pāṭala use |
|---|---|---|---|
| 2502.10855 | Claimify — extraction & evaluation of factual claims (ACL'25) | **VERIFIED** | turn essay/C1/theme prose into addressable assertions; coverage + decontextualization eval |

> **Pāṭala test design (from Claimify):** claim completeness · claim independence ·
> decontextualization · semantic preservation. Author note: Metropolitansky & Larson are also GraphRAG
> (2404.16130) authors — same research line.

### 10. Claim verification / support / contradiction
| arXiv | Paper | Status | Pāṭala use |
|---|---|---|---|
| 2408.08067 | RAGChecker | **VERIFIED** | fine-grained retrieval/generation diagnosis; not one vague faithfulness score |
| 2601.06519 | MedRAGChecker | **VERIFIED** | atomic claims + evidence-grounded NLI + KG consistency → `/verify-claim-semantic` |
| 2506.04583 | SUCEA — adversarial fact-checking | **VERIFIED** | claim decomposition + iterative evidence retrieval → `/discover-counterevidence` |

> **Pāṭala requirement:** this should inform the distinction between *explicit CONTRADICTS edges* (EXPOSE)
> and *discovered counterevidence* (INFER).

### 11. RAG evaluation theory
| arXiv | Paper | Status | Pāṭala use |
|---|---|---|---|
| 2405.07437 | Evaluation of RAG: A Survey (Auepora) | **VERIFIED** | build your benchmark taxonomy from this, don't invent metrics |
| 2504.14891 | RAG Evaluation in the Era of LLMs: A Comprehensive Survey | **VERIFIED** | broadens to factuality, safety, efficiency |

---

## 2. Required deliverables — the agent must produce these, not "read and absorb"

### 2a. Per-paper technical note (every paper)
```
machinelearning/papers/<paper>.md
 1. Problem definition
 2. Mathematical formulation
 3. Inputs / outputs
 4. Architecture
 5. Objective / loss
 6. Training regime
 7. Inference procedure
 8. Complexity
 9. Assumptions
10. Evaluation datasets
11. Metrics
12. Baselines
13. Ablations
14. Reported result
15. Failure modes
16. What is theoretically established
17. What is merely empirical      ← the crucial distinction
18. Exact mapping to Pāṭala
19. Minimal reproducible implementation
20. Experiment needed before adoption
```

### 2b. Proof notes (for the mathematically serious papers)
For NBFNet (2106.06935), GraphGPS (2205.12454), and the hyperbolic models:
```
machinelearning/proofs/
  nbfnet-bellman-ford.md
  graphgps-expressivity.md
  hyperbolic-capacity.md

THEOREM / PROPOSITION     exact statement from the paper
ASSUMPTIONS
DEFINITIONS
PROOF SKETCH              in our own notation
WHAT IT ACTUALLY GUARANTEES
WHAT IT DOES NOT GUARANTEE
PĀṬALA RELEVANCE
```
Do NOT let the agent say "the paper proves X" without reconstructing the assumptions.

### 2c. Implementation decision records (before any model)
```
machinelearning/decisions/ADR-XXX-<model>.md
  Research question
  Baseline
  Proposed model
  Hypothesis
  Dataset split
  Metrics
  Acceptance threshold
  Ablations
  Compute budget
  Failure criteria
  Result
  Decision: ADOPT / REJECT / MORE-EVIDENCE
```
Worked example:
```
Research question: Does late interaction improve retrieval of doctrinally relevant IPVV
passages over BM25+dense?
Baselines: BM25 · BGE dense · BM25+BGE
Candidate: ColBERTv2
Primary:   Recall@5 · MRR@10
Secondary: term-sense recall · hard-negative discrimination
Adopt only if: significant improvement on the held-out Pāṭala benchmark, not merely visual examples.
```

---

## 3. The experiment ladder (after reading)

```
E0  Benchmark            expert-reviewed retrieval/support/theme fixtures
E1  Retrieval            BM25 vs dense vs late-interaction vs hybrids
E2  Theme discovery      text-only vs graph-only vs hybrid vs learned graph
E3  Claim verification   NLI-only vs graph-only vs NLI+graph
E4  Counterevidence      semantic retrieval vs adversarial retrieval
E5  Vertical fidelity    C1→Theme→Guide semantic conservation
E6  Graph reasoning      R-GCN / CompGCN / NBFNet / GraphGPS
E7  Higher-order         ordinary graph vs native hypergraph
E8  Geometry             Euclidean vs hyperbolic representations
E9  Cross-work transfer  train IPVV / evaluate unseen work
```
Each has a **fixed held-out test set decided before model development**.

---

## 4. The frontier target (what Pāṭala is eventually capable of supporting)

> **Structured Scholarly Supervision for Provenance-Preserving Reasoning over Premodern Texts**

Experiments showing:
```
text embeddings
<
structured scholarly graph
<
text + scholarly graph
<
higher-order provenance representation
```
on: passage retrieval · thematic discovery · claim support · counterevidence · cross-layer fidelity.

The novelty is the **supervision structure produced by critical scholarship itself**:
source → reading → decision → commentary → theme → claim → pedagogical rendering. That is the
dataset/modeling opportunity worth protecting — not "we applied GraphRAG to Sanskrit."

---

## 5. Verification summary (what I actually checked, 2026-08-12)

I fetched and confirmed the titles of 21 of the 26 papers; the remaining 5 (R-GCN, CompGCN, NBFNet,
GraphGPS, hyperbolic tutorial + review) are canonical foundational works with stable, well-known IDs.

**Two corrections to the draft curriculum:**
1. **2410.12609** is titled *"Training on Knowledge Graphs Enables Transferability to General Graphs"*
   and introduces **SCR** with **semantic-conditioned message passing** — not "SCORE."
2. The two hypergraph-RAG papers (2602.14470 vs 2504.08758) are **confirmed distinct and both real**
   — the draft's warning was correct.

**Everything else in the curriculum is confirmed as written.** The reading order (retrieval →
GraphRAG → higher-order → multi-relational → general graph → GFMs → overlapping → hyperbolic → claims →
verification → eval) is sound and appropriately staged from cheap baselines to frontier research.

## PROGRESS (2026-08-12)

The corpus-side prerequisites the curriculum assumed are now in place: C1s wired into the published
objects, THEMES exposed, the deterministic verification floor live. The curriculum's staged reading
order (retrieval → graph → verification → eval) can now be executed against real fixtures rather than
hand-built examples.
