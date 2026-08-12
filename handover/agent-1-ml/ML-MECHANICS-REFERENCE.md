# ML MECHANICS — the code-level reference (what each module ACTUALLY does)

*2026-08-12. The ground-truth inventory of the ML workspace, read directly from the code (not the
handover's descriptions). Every module in `machinelearning/research/patala_ml/` — what it computes,
its honest status, and how it connects. Use this to know the mechanics before touching them.
Re-verify against the code if you change anything.*

---

## The data loaders (the input floor)

### `corpus.py` — the passage store loader
- **Reads** `data/published/ipvv/pt-passage-*.json` (the lazy-JSON store, 49 passages).
- **Produces** `PassageDoc`: id (pt:passage) · locator (chunk) · l2_text · c1_body · source_sanskrit ·
  key_terms · see_also. `full_text()` = L2 + C1 concatenated.
- **Used by** `retrieval.py` (the indexable units) and `eval.py` (via `load_passages`).
- **Honest status:** infrastructure — real corpus, real IDs.

### `c1corpus.py` — the C1-node loader (for clustering)
- **Reads** the 63 `c1/read/c1_*.md` files directly (NOT the JSON store).
- **Produces** `C1Node`: c1_id (e.g. `V2O-orderless-support`) · passage_id · body (the `> ` quote lines) ·
  terms (parsed `**Terms:**`) · see_also (parsed `**See also:**`).
- **Why C1 granularity (63) not passage (49):** the V1 passage's 14 fine-grained C1s participate individually.
- **Used by** `cluster.py`.

---

## The clustering (CP3 — the intellectual-structure proposals)

### `cluster.py` — Stage-2 hybrid-graph clustering of the 63 C1s
- **Mechanism:** hybrid graph (curated `See also` edges, weight 1.0 + shared-KEY-TERM Jaccard edges,
  weight 0.5 × jaccard, min jaccard 0.3) → **Louvain** community detection (python-louvain, `community`)
  → multi-assign borderline nodes (a node whose neighbor-weight to a 2nd community ≥ 0.85× its best
  community gets both).
- **Key design decision (from the themes pilot):** shared **body-words are noise** (over-connect);
  the discriminating signal is curated `See also` edges + shared **KEY TERMS**. Do NOT switch to body-word similarity.
- **Deterministic** (fixed seed 42), CPU-only.
- **Produces** `ClusterProposal`: cluster_id · members · strengths (within-community degree) ·
  edge_evidence (the `{a,b,type,weight}` pairs = why these C1s are together, answerable).
- **Honest status:** real graph topology; **machine proposals, NOT accepted themes** (CP3 gate not crossed).

---

## The retrieval (CP2 — the evidence-finding baselines)

### `retrieval.py` — the baselines to beat
- **BM25** (`rank_bm25`), **dense** (sentence-transformers MiniLM, cosine), **hybrid** (weighted sum of
  min-max-normalized BM25 + cosine dense, default 0.5/0.5).
- All build an index over `PassageDoc` by a chosen field: `full` | `l2` | `c1`.
- **These are the THINGS TO BEAT** — no learned model is adopted until it beats them on a fixed held-out set.

### `eval.py` + `metrics.py` — the frozen statistical discipline
- **`metrics.py`:** `recall@k`, `mrr@k`, `ndcg@k` (binary gains) · `classification_metrics` ·
  `bootstrap_ci` (percentile CI, fixed seed `RNG`) · `paired_bootstrap_delta` (paired bootstrap CI +
  sign-flip **permutation p-value**, H0 delta=0) · `theme_discovery_metrics`.
- **`eval.py`:** `evaluate_retrieval` runs each retriever per-query, reports mean + bootstrap CI per
  metric + **paired delta vs the BM25 baseline** with the permutation p-value.
- **The unit of analysis is the query/claim, NOT the token** — this is explicit in `bootstrap_ci`.
- **Honest status:** real harness. The E1-fidelity run showed **dense did NOT beat BM25** (MRR delta
  −0.035, p=0.083) — an honest negative arguing the signal is structured/graph, not a fancier encoder.

---

## The argument layer (CP4 — built; golds CANDIDATE; the frontier is semantic alignment + gold review)

### `argument.py` — the Claim-v3-shaped ArgumentProposal
- **Adopts truth-engine Claim v3:** `posterior_targets` (move Bayesian state AFTER gate approval) vs
  `argument_targets` (graph nodes/edges + state-of-play pressure, never touch the posterior).
- **`NyayaMember`** = one of the 5-member syllogism: PRATIJNĀ · HETU · UDAHARANA · UPANAYA · NIGAMANA.
- **`ClaimV3`** = one atomic claim: claim_text · tradition_scope · pramana · hetu · sadhya ·
  vyapti_statement · falsifier · posterior_targets · argument_targets · weights (log_bayes_factor,
  w_rel, w_map, w_aux) · **gate** (must exist to update posterior) · status · strength.
- **`build_argument`** assembles the proposal + derives aggregate strength via `strength.score_argument_premises`.
- **`from_logical_argument_file`** parses a `LOGICAL-ARGUMENT-*.md` (the 5-member shape) into an ArgumentProposal.
- **Honest status:** schema + assembly real; **the `gate` slot is empty** (needs the gate wired); the
  actual propositions must come from the gold.

### `aifgraph.py` — the AIF-informed argument graph (3 node types)
- **INFORMATION** node (a proposition) · **INFERENCE** node (why A licenses B, the scheme) ·
  **CONFLICT** node (why X challenges Y: OBJECTION/REBUTTAL/QUALIFICATION).
- **`check()`** returns REAL invariants (not invented scores): inference premises/conclusion exist ·
  conflict source/target exist · premise nodes have resolvable passage_ids · implicit premises flagged.
- **Honest status:** representation + structural soundness checks; **no real content yet** (that's the gold work).

### The gold (the hand-built ground truth the extractor is tested against)
- **`gold.py`** → ARG-GOLD-001 (V2-O transcendental) · **`gold002.py`** → ARG-GOLD-002 (V2-L objection-reply).
- **`goldutil.py`** → `wrap_fixture` (the CP0 BenchmarkFixture envelope) + `validate_gold` (the
  consistency validator: passage resolves · inference integrity · no unused textual claims · boundary).
- **`emit_gold_fixtures.py`** → the `GOLDS` registry (add a builder → auto wrap+validate+write).

---

## The Nyāya gate (CP4 audit — the frozen external asset)

### `nyayagate.py` — the Pāṭala-adapted 5-hetvābhāsa gate
- **Reuses the truth-engine's MECHANISM (the 5 fallacies), rejects its ontology.** The truth-engine's
  680-LOC gate is metaphysics-specific; this is the Pāṭala version with philological/argument rules.
- **The 5 hetvābhāsas:**
  - **asiddha** — the hetu is not itself established (markers: "subtle body", "past lives", ...; or
    strong-conclusion-from-sabda/upamana with high |lbf|).
  - **viruddha** — evidence supports the OPPOSITE (markers: "therefore the opposite", "proves it is not"...).
  - **savyabhicara** — universal claim without strong vyāpti (vc≥0.8 + no violations); or vc<0.6; or listed violations.
  - **satpratipaksa** — an equally-strong counter-inference (opposite sign + overlapping target).
  - **badhita** — contradicted by stronger evidence (markers: "no neural correlate"...).
- **Outcome ladder:** accepted → accepted_with_penalty → needs_review → hollow(abstain). A missing
  falsifier always downgrades a would-be-accepted claim.
- **`can_update_posterior`:** accepted→True, accepted_with_penalty→True(cap), needs_review/hollow/refuted→False.
- **Measured state:** `NYAYA_GATE_CANDIDATE_v1` — defect recall 4/5 (0.80), clean FP 0/5 (0.00),
  abstain 1/2 (0.50). **The 1 miss is viruddha** — it needs a real argument graph, NOT a keyword hack.
- **⚠️ FROZEN. Do NOT hack viruddha into this file.** It stays v1 until Argument Gold + a real argument
  graph exist (then viruddha = graph operation → `VIRUDDHA_CANDIDATE` → semantic/human layer decides).

---

## The Bayesian engine (the strength primitive)

### `strength.py` — `BayesianEvidencePrimitive` (a claim-evidence accumulator)
- **HONEST SCOPE (read this):** a *mathematical primitive*, NOT a truth engine, NOT an argument scorer,
  NOT calibrated. Weights are hand-chosen. It does NOT establish truth/validity/correctness/acceptance.
- **Mechanism:** `weighted_lbf = w_rel × w_map × w_dep × w_aux × log_bayes_factor`; then
  `posterior = sigmoid(log_odds(prior) + weighted_lbf)`.
- **Paradigm crowding:** `w_dep = 1/(1 + alpha·n_prior)` — repeated same-paradigm premises get down-weighted.
- **Maps to ordinal labels:** posterior → `certainty` (certain/probable/possible/uncertain) → `strength`
  (WELL_SUPPORTED/PLAUSIBLE/SPECULATIVE). **Ordinal, NOT calibrated probability.**
- **`audit_trace()`** records the full derivation (the "why this strength").
- **`score_argument_premises`** aggregates premises → an argument-level posterior.
- **Honest status:** math correct (24 tests); **UNVALIDATED_HEURISTIC** — no epistemic role until
  calibrated against adjudicated outcomes. Do NOT call its outputs "probabilities."

---

## The verification floor

### `philproof.py` + `goldchain.py` — the L0 handshake + cross-layer certificate
- **`philproof.py`** consumes the `pp:` proof IDs (from Agent 2's `verify_l0.py`) — the L0 floor.
- **`goldchain.py`** renders the cross-layer certificate. **Honest statuses now:** L0 = REAL
  (source_integrity PROVED, morphology SUPPORTED, OPEN cruxes propagate); INTERPRETATION/INFERENCE/
  ESSAY_CLAIM = MACHINE_PROPOSED (fixed — no fabricated `EDITOR_APPROVED`).

### `cleanup.py` — the honest ID resolver
- Exact-match resolution, no fuzzy. The fabricated-ID failure (V2L → wrong passage) is why this is strict.

---

## HOW IT ALL CONNECTS (the data flow)

```
corpus.py / c1corpus.py   (real passages + C1 nodes)
   ↓
cluster.py  →  ClusterProposal (CP3, machine proposals)
retrieval.py + eval.py + metrics.py  →  benchmarked retrieval (CP2)
   ↓
gold.py / gold002.py  →  Argument Gold  (CP4 ground truth, the active build)
   ↓
argument.py + aifgraph.py  →  ArgumentProposal / ArgumentGraph (built FROM the gold, gate slot empty)
   ↓
strength.py  →  Bayesian strength (ordinal, uncalibrated)
nyayagate.py  →  the 5-hetvābhāsa audit of the Inference (frozen at v1; viruddha awaits the graph)
   ↓
philproof.py + goldchain.py  →  the verification floor (L0 real, upper MACHINE_PROPOSED)
```

## THE NEXT TASKS (the current frontier — what the mechanics are FOR)

1. **CP3 theme acceptance** — promote `THEME-REVIEW-001..003` (Order-less=LOCAL_THEME, Vimarśa=CONCEPT_TERM_FAMILY,
   Pramāṇa=DOCTRINAL_PROBLEM_DOMAIN) → `ACCEPTED_THEME`.
2. **Semantic Alignment competence** — the Stage-A harness (`semantic_alignment.py`) is built and the
   generic encoder is falsified (0/8). Beat it with a cross-encoder pair classifier / Sanskrit-aware
   embedding; keep the three-space disagreement as a SEMANTIC_TENSION signal. See
   `RETRIEVAL-NEUROSYNTHETIC-VISION.md`.
3. **Independent gold review → the first AUDITABLE argument** (ARG-002 v2) → real py-aspic + crux.
4. **Retrieval layer (CP2)** — BM25/dense/late-interaction over Pāṭala objects + k-core determinism +
   multi-hop PPR over the curated graph.

## THE HONEST POSITION

The mechanics are real and tested, but they are **A (infrastructure) + B (the gold/theme layer is
evidence)** — not **C (results)**. No claim is a result until it's measured against frozen gold and
recorded as a `BenchmarkRun`. The golds are `CANDIDATE` (model-critiqued, NOT independently reviewed);
extraction is `NOT_ESTABLISHED`; the semantic-alignment baseline is falsified (0/8). **The next thing
that makes any of it a result is (a) the themes accepted, (b) a semantic-alignment system that beats the
baseline, and (c) the first argument through independent review — then everything above becomes
measurable.**
