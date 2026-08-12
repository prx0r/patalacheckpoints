# AGENT 1 (ML) — NEXT STEPS (current execution, 2026-08-12)

*The exact how-to for the next session. Read `AGENTS.md`, `AGENT1-HANDOVER.md`, `INDEX.md`,
`SESSION-2026-08-12.md`, `_ACTIVE/IR-REVIEW-FINDINGS.md` first. This is the execution layer on top of
those. A new agent should be able to continue from here without re-deriving the session.*

---

## 0. WHERE YOU ARE (one honest paragraph)

Pāṭala's substrate + provenance + representation layers are real. Agent 1 has: 5 model-critiqued
argument golds (CANDIDATE), a fully-resolving vertical object, a recall-first theme map over the IPVV/C1
(100% coverage), model theme reviews (the three are different kinds), an ASPIC adapter + pilot
(proxy-supported; real engine is an open external dependency), and a primitive extraction baseline
(NOT_ESTABLISHED). The frontier is the **symbolic layer**: semantic alignment + theme acceptance + the
first auditable argument. Do NOT build more internal machinery for its own sake — the next work is
making the existing objects externally valuable (see the "brutal question" below).

---

## 1. THE NEXT BUILD, IN ORDER

### Build 1 — CP3 theme acceptance (the highest-leverage, least-gated)
You already have the model reviews (`benchmarks/v0/review/THEME-REVIEW-001..003.json`):
- Order-less Support → `LOCAL_THEME` (REVISE — tighten membership, add V2A)
- Vimarśa → `CONCEPT_TERM_FAMILY` (RETYPE — a success)
- Pramāṇa → `DOCTRINAL_PROBLEM_DOMAIN` (RETYPE — a success)

**Do:** confirm these (a second model or a human), promote the three to `ACCEPTED_THEME` (or
`MODEL_REVIEWED`), and record them in the theme map. This crosses CP3's gate ("3 themes adjudicated").

### Build 2 — SemanticAlignment v0 (the foundational symbolic layer)
Freeze `SemanticAlignment` v0 FROM the actual annotations the theme reviews require — do NOT design an
alignment engine against synthetic assumptions. The reviews surfaced concrete relations to model:
- `vimarśa` NEAR_SAME across V2H/V2J/V2O (but the term family spans sphurattā/samskāra/vākāsphoṭa)
- `sphurattā` AMBIGUOUS, `parā-vāk` NOT_ENOUGH_CONTEXT
- `pramāṇa` NEAR_SAME as a doctrinal target, `anumāna` AMBIGUOUS across sub-domains

**Use what we already have:** `sentence_transformers` (installed) → build occurrence-pair candidates,
score dense + sparse lexical + a cross-encoder reranker, benchmark the coarse SAME/NEAR/PARTIAL/DIFFERENT
judgment against the review seeds. Then build the `CAN_CONFLICT(A,B)` gate (same target/sense/scope/level/
modality before contradiction). This is the symbolic layer behind the "semantic microscope" vision
(`machinelearning/_ACTIVE/RETRIEVAL-NEUROSYNTHETIC-VISION.md`, Stage A).

**Stage A result (2026-08-12):** the harness is built and the generic English/multilingual encoder is
falsified (0/8). The ablation isolates the failure to the **encoder/representation space**, NOT context
windows. **Next:** a cross-encoder pair classifier (sees A+B jointly) or a Sanskrit-aware embedding,
beating the frozen baseline; keep the three-space disagreement as a SEMANTIC_TENSION signal. Then expand
the gold to ~40-100 heterogeneous pairs before touching PPR/CatRAG.

### Build 3 — The first AUDITABLE argument (ARG-002 v2)
Do NOT wait for a human Sanskritist to build things experimentally. But the *scholarly validation* of an
argument is the human gate. The milestone: get ARG-002 v2 through an **independent review** → the first
`INDEPENDENT_REVIEWED` / `ACCEPTED` argument → then real py-aspic (the 503 dependency) becomes meaningful.
Mark progress as `ENGINEERING_VALIDATED`, never `SCHOLARLY_VALIDATED`, until that review happens.

### Build 4 — CP2 retrieval over Pāṭala objects (the "neural layer")
Index **Sanskrit lemmas + translations + C1 + argument objects** (not English chunks) with
BM25 / dense / late-interaction baselines, evaluated against `benchmarks/v0/retrieval/`. This is the
neural layer of the "semantic microscope" vision (`RETRIEVAL-NEUROSYNTHETIC-VISION.md`): it PROPOSES
candidates + why; the symbolic layer (alignment) says the relation; the scholar adjudicates.

Also fold in the Phase-D concrete builds (DEVPLAN §5): **D2** replace `cluster.py`'s Louvain with k-core
(deterministic, reproducible themes); **D3** multi-hop Personalized-PageRank traversal over Pāṭala's
curated graph (NOT an OpenIE graph). Avoid Kùzu (ARCHIVED); treat GraphRAG/LightRAG as pattern libraries only.

---

## 2. THE BRUTAL QUESTION (ask every few weeks)

> **What new scholarly task can Pāṭala perform today that would have been materially harder without
> this infrastructure?**

Progress so far: trace one proposition to Sanskrit (done) → turn a machine-discovered theme into an
auditable reviewed object (in progress) → extract one defensible argument automatically (next) →
identify a real crux between two interpretations → route only that crux to a specialist.

---

## 3. THE WARNING LABELS (never overclaim)

- `reference_resolution: EXACT` = the **proof reference** resolves exactly — NOT semantic entailment.
  Always carry `semantic_support: MACHINE_PROPOSED`.
- `AUDITABLE ARGUMENT REPRESENTATION` ✅ ≠ `SCHOLARLY VALIDATED ARGUMENT` ⏳.
- `ENGINEERING_VALIDATED` ≠ `SCHOLARLY_VALIDATED`.
- L0: source span = deterministic floor; lemma/morphology = machine witness, reviewed per its own status.
- Extraction/crux built against MODEL_CRITIQUED_CANDIDATE_GOLD = ENGINEERING_VALIDATED, not validated.

---

## 4. GUARDRAILS

1. Route everything through `benchmarks/v0/` + record a `BenchmarkRun`.
2. Join on `Ref` IDs (passage / proof / C1) — never fuzzy.
3. Do NOT hack viruddha into the frozen `nyayagate.py`.
4. Do NOT build the essay layer / Bayesian propagation / more clustering.
5. **Git discipline:** you are agent1; work only in the agent1 worktree on branch `agent1`; stage only
   your explicit paths + commit immediately; never force-push / rewrite another lane's commit (see
   `GIT-INCIDENTS.md` INCIDENT-2026-08-12-01).
6. Update `CLAIMS.md` + `theatre_check.py` honestly as you go; drop a `SESSION-<date>.md` at session end.

---

## 5. THE ONE-SENTENCE CARRY-FORWARD

**The substrate, provenance, argument representation, and a recall-first theme map are real; the next
work is the symbolic layer — accept the three themes (CP3), freeze SemanticAlignment v0 from the actual
annotations, and cross the first argument (ARG-002 v2) through independent review to unlock real
py-aspic and crux — while keeping the neural retrieval layer (CP2) as the buildable "proposes candidates"
half and never conflating reference-resolution with semantic truth.**
