# AGENT 1 — BUILD RECORD 2026-08-12 (session index: everything built, its status, its purpose)

*A complete, honest index of what Agent 1 built this session. For a new agent: read this to see the whole
picture, `INDEX.md` for current state, `NEXT-STEPS.md` for what to do next. Every item is tagged with its
honest status — nothing here is "validated" unless it says so.*

---

## The session in one line

Pāṭala moved from "structural representation" to **auditable provenance + a real theme layer + a first
evaluator pilot**, while the doctrine forced the ontology corrections gold is supposed to force.

---

## 1. ARGUMENT GOLD (CP4) — the 5 golds + review

| Artifact | What | Status |
|---|---|---|
| `patala_ml/gold.py` (ARG-001) | transcendental (V2-O), regress layer removed after review | CANDIDATE |
| `patala_ml/gold002.py` (ARG-002 v2) | objection→reply, **the clean py-aspic target** | CANDIDATE (closest to clean) |
| `patala_ml/gold003.py` (ARG-003) | **demoted to `ALT_RATIONAL_RECONSTRUCTION`** (regress not licensed) | REJECT_AS_TEXTUAL_GOLD |
| `patala_ml/gold004.py` (ARG-004) | conceptual distinction (vimarśa vs prakāśa) | CANDIDATE |
| `patala_ml/gold005.py` (ARG-005) | `INTERPRETIVE_SCOPE` (local vs systematic) | CANDIDATE |
| `benchmarks/v0/structure/PAT-STRUCT-001..005.json` | emitted fixtures | validate_gold-consistent |
| `benchmarks/v0/review/REVIEW-2026-08-12-MODEL-1.json` | model review (REVISE ×4, REJECT ×1) | MODEL_INDEPENDENT_REVIEWED |
| `benchmarks/v0/ARG-GOLD-REVIEW-PACKET-v2.md` + `review/ARG-GOLD-REVIEW-PACKET-v2.json` | **rebuilt packet (primary-Sanskrit grounded)** — every proposition resolves to primary L0 spans; L2 never required (removes the circularity MODEL-1 flagged). Gate: `experiments/check_review_packet.py`. | ready for a human |
| `benchmarks/v0/ARG-GOLD-REVIEW-PACKET.md` | v1 packet (L2-based basis) — superseded by v2 | legacy |

**Ontology forced by gold (do not re-litigate):** inference-vs-dialectical, grounding-vs-inference,
`support_scope`, reconstruction commitment, warrant-on-InferenceRule → captured in
`machinelearning/_ACTIVE/IR-REVIEW-FINDINGS.md`.

## 2. VERTICAL OBJECT (the auditable provenance trail)

| Artifact | What | Status |
|---|---|---|
| `patala_ml/vertical.py` | one proposition → typed `GroundingLink`s down to exact L0 spans + proof | v0 FROZEN |
| `benchmarks/v0/vertical/vertical-v2o-g-tc2.json` | the object | `reference_resolution=EXACT`, `semantic_support=MACHINE_PROPOSED` |
| `experiments/build_vertical_object.py` | the runner | |

**Claim (P-014):** a proposition links through typed, resolvable objects to exact Sanskrit spans whose
proof resolves. **`EXACT` = reference resolution, NOT semantic entailment.**

## 3. THEME LAYER (CP3) — discovery + map + review

| Artifact | What | Status |
|---|---|---|
| `patala_ml/theme_discovery.py` | recall-first 8-step pipeline, coverage/overlap accounting | MACHINE_PROPOSED |
| `experiments/build_theme_map.py` | IPVV/C1 → 100% coverage (63/63, 0 unassigned) + C1 + argument integration | MACHINE_PROPOSED |
| `benchmarks/v0/theme-map-ipvv-v0.json` · `THEME-MAP-IPVV-REPORT.md` | the map + report | MACHINE_PROPOSED |
| `benchmarks/v0/THEME-ADJUDICATION-PACKET.md` | kind + coarse-sense review packet | ready |
| `benchmarks/v0/review/THEME-REVIEW-001..003.json` | model review: LOCAL_THEME / CONCEPT_TERM_FAMILY / DOCTRINAL_PROBLEM_DOMAIN | MODEL_REVIEWED |

**Claim (P-015/P-016):** candidate conceptual/thematic discovery covers the corpus; the kind-taxonomy is
validated (the three are different kinds). NOT yet accepted themes.

## 4. EVALUATION (CP4/CP5) — baseline + ASPIC pilot

| Artifact | What | Status |
|---|---|---|
| `patala_ml/extractor.py` + `eval_extraction.py` | primitive blind baseline | proposition F1 ~0.36, inference recovery 0 → **extraction NOT_ESTABLISHED (P-003)** |
| `patala_ml/aspic_adapter.py` + `experiments/eval_aspic_pilot.py` | ARG-002 v2 → ASPIC (minimal local fallback) | PROXY_SUPPORTED; real engine 503 = **open external dependency** |
| `benchmarks/v0/runs/2026-08-12T135103Z/` | the pilot EvaluationRun | REPRESENTATIONAL=PARTIAL, SEMANTIC=PROXY_SUPPORTED, BET=OPEN |

## 5. DOCTRINE / SYSTEM (the meta-layer)

| Artifact | What |
|---|---|
| `machinelearning/_ACTIVE/AGENT1-HANDOVER.md` | **Axiom 11 (git worktree discipline)** + the shared-index incident |
| `handover/GIT-INCIDENTS.md` | INCIDENT-2026-08-12-01 (4cc78d1 cross-lane) + Agent 0 worktree action |
| `handover/session_close.py` | the smooth session-end loop (gates + flow + SESSION + handoff) |
| `handover/CONTEXT-CHAIN.yaml` + `context_gate.py` | the full-context read gate (both agents complete) |
| `handover/CHECKPOINTS.md` | the Phase 1–7 ladder (checkpoints as children of phases) |
| `machinelearning/_ACTIVE/DEVPLAN.md` | priority corrected (gold review → extractor → gate) |
| `machinelearning/_ACTIVE/ML-ALIGNMENT.md` | IR→graph mapping (NOT FROZEN; Proposition identity/version open) |

## 6. THE HONEST STATE

```
SOURCE PROVENANCE / VERTICAL RESOLUTION       REAL
THEME DISCOVERY (candidate coverage)          REAL (MACHINE_PROPOSED)
THEME KIND-TAXONOMY                           MODEL_REVIEWED
ARGUMENT REPRESENTATION                       REAL
ARGUMENT SCHOLARLY VALIDATION                 ⏳ (needs independent human review)
AUTOMATIC EXTRACTION                          NOT_ESTABLISHED
SEMANTIC ALIGNMENT                            EARLY (reviews surfaced the relations to model)
ASPIC                                          PROXY_SUPPORTED (real engine = open dep)
CRUX / SYNTHESIS / WORKBENCH                  NOT YET
SCHOLAR REVIEW LOOP                           READY TO TEST
```

## 7. HOW A NEW AGENT CONTINUES

Read `NEXT-STEPS.md`. In order: **CP3 theme acceptance** (promote the 3 reviews) → **SemanticAlignment
v0** (freeze from the actual annotations) → **first auditable argument** (ARG-002 v2 through independent
review → real py-aspic) → **CP2 retrieval over Pāṭala objects** (the neural layer). Always: the warning
labels (§3 of NEXT-STEPS), the brutal question, and route everything through `benchmarks/v0/`.

## 8. STAGE A — SEMANTIC ALIGNMENT (the symbolic layer, built + falsified)

| Artifact | What | Status |
|---|---|---|
| `patala_ml/semantic_alignment.py` | `align(A,B)` → {relation_proposal, evidence, model_scores, abstain_reason}; 6-label vocabulary; 3 representation spaces (sanskrit/l2/c1) | MACHINE_PROPOSED |
| `experiments/benchmark_semantic_alignment.py` | 8 gold pairs from THEME-REVIEW; **baseline 0/8** (generic English encoder fails on Sanskrit/IPVV) | MACHINE_PROPOSED_BENCHMARK |
| `experiments/ablate_semantic_alignment.py` | controlled ablation (6 windows × 3 encoders, fixed thresholds) | finding below |
| `tests/test_semantic_alignment.py` | contract + vocabulary + abstention | 0 fail |

**The ablation finding (the real result):** the 0/8 failure is NOT context-window construction. It is the
**encoder + representation space**: a generic English or multilingual model cannot align contextualized
philosophical occurrences. `lemma_only` 1.00 = circular (same lemma); `multilingual` 1.00 =
non-discriminative (compressed cosine). The genuine signal: `dense` English **degrades with context**
(sanskrit 0.60 → l2 0.40 → c1 0.00 → c1_full 0.00). Keep the three-space disagreement as a
**SEMANTIC_TENSION** discovery signal. **Next baseline to beat: a Sanskrit-aware embedding and/or a
cross-encoder pair classifier.** (See `RETRIEVAL-NEUROSYNTHETIC-VISION.md`.)
