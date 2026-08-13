# CLAIMS.md — Pāṭala's self-audit (the project auditable by its own philosophy)

*2026-08-12. The project's own claims ledger. Every significant capability claim has a STATUS, EVIDENCE,
CAVEAT, and what would promote it. This makes the project auditable using its own philosophy — no claim
is "real" because code exists; it's real only when independent gold + blind prediction + metric + human
adjudication show it.*

**The rule:** *Nothing is "real" because code exists. It becomes real only when an independently defined
task, human-grounded gold, and a reproducible evaluation show that it does what its name claims.*

---

## CLAIM P-001 — "Pāṭala has lossless source anchoring (L0)."
- **STATUS:** SUPPORTED (complete IPVV, 63/63) — the full flagship corpus
- **EVIDENCE:** `verify_l0.py` P0 harness — **the complete IPVV is now 63/63 P0 PASS**:
  - **V2/V3 (35 chunks): 35/35 PASS** — 0 unknown chars, 0 bad spans, 0 overlaps, 0 duplicates,
    monotonic ordering, full classification, deterministic.
  - **V1 legacy (28 chunks): 28/28 PASS** (NEW, 2026-08-12) — via the new V1 adapter
    (`pipeline/extract_l0_v1.py`, 91,714 tokens) producing canonical `l0_schema.json` records. The
    adapter covers the V1 prose format (inline `GLOSS (IAST)`, `[bracket]` connectives, line-wraps)
    such that the **existing `verify_l0.py` passes UNCHANGED** (byte-identical to git).
  - The 18 irregular V2/V3 regions are classified via `docs/l0_reviewed_exceptions.json`.
  - Reproduce: `python3 pipeline/extract_l0_v1.py <01_t1> <out> --all` then
    `python3 pipeline/verify_l0.py --t1 <01_t1> --l0 <out> --level p0`.
- **CAVEAT (cross-work, honest):** 63/63 proves the contract + verifier survive **two different IPVV
  source formats** (the `[and]-` gloss format and the legacy prose format) — strong evidence of format
  robustness. It does **NOT** yet prove generalization to IPK/Tantrāloka/Kubjikā without modification;
  the schema/tools are designed work-agnostically, but cross-work generalization remains to be
  demonstrated when the second real work is ingested. P2 (Vidyut morphology) is characterized (55%
  supported) but not yet the P2 ensemble-validated proof.
- **REQUIRED to promote (cross-work):** ingest a second real work's T1 and confirm no adapter change is
  needed; P2 ensemble validated against an independent witness; specialist review of a sample.
- **STATUS THIS SESSION (2026-08-12):** V2/V3 P0 **FROZEN** as the first completed CP1 sub-capability.
  Next (per the cross-layer review): Heritage as an independent P2 witness over all Vidyut CONFLICT +
  UNANALYZED records + a stratified control sample (~500 CONFIRMED, ~500 AMBIGUOUS_SUPPORTED) → an
  ensemble disagreement report. ranker.py is NOT promoted to P3; it is first audited + given a small
  human-reviewed lexical-sense gold + evaluated against baselines before being a non-authoritative
  lexical witness.

## CLAIM P-002 — "Pāṭala's benchmark is a real evaluation substrate."
- **STATUS:** SUPPORTED (as infrastructure) / PARTIAL (as evidence)
- **EVIDENCE:** `benchmarks/v0/` frozen (MANIFEST/SCHEMA/SPLITS/METRICS); retrieval fixture files;
  **5 structure golds** (ARG-GOLD-001..005, `validate_gold`-consistent, `review_state=CANDIDATE`);
  evidence = 12-fixture Nyāya-gate gold.
- **CAVEAT:** EVIDENCE and FIDELITY families still have **0 fixtures** in the frozen families (the
  12 gate fixtures are evidence-family, SINGLE_REVIEWED by one author). All fixtures are **CANDIDATE**,
  machine-authored, NOT independently DOUBLE_REVIEWED.
- **REQUIRED to promote:** targets (50 retrieval / 30 evidence / 10 structure / 30 fidelity); every
  fixture real-ID + review-status + provenance + no-leakage; independent reviewer sign-off.

## CLAIM P-003 — "Pāṭala can automatically reconstruct IPVV arguments."
- **STATUS:** NOT_ESTABLISHED
- **EVIDENCE (2026-08-12):** 5 real hand-gold arguments exist (ARG-GOLD-001..005, `benchmarks/v0/structure/`,
  `validate_gold`-consistent, `review_state=CANDIDATE`). **An independent MODEL review
  (`REVIEW-2026-08-12-MODEL-1`) returned: ARG-001/002/004/005 REVISE, ARG-003 REJECT_AS_TEXTUAL_GOLD**
  (demoted to ALT_RATIONAL_RECONSTRUCTION — the regress was not licensed). Corrections applied: the
  regress/transcendental layer removed (ARG-001); knower/Lord + parā-vāk identifications are GROUNDING,
  not inferences; ARG-005 objection is a dialectical RESPONDS_TO; ARG-002 v2 is the clean py-aspic target.
  Status is **MODEL_INDEPENDENT_REVIEWED** — NOT INDEPENDENT_REVIEWED/SPECIALIST_REVIEWED (a human
  Sanskritist against the primary text is required for those). A primitive baseline extractor was run
  BLIND (the CP4 Build-4 gate); metric bounded as `baseline-v0-lexical-proposition-overlap` (F1 ~0.36,
  inference recovery 0.0).
- **CAVEAT:** a sentence-level baseline cannot recover abstract/reconstructed propositions. The golds are
  `CANDIDATE`; ARG-003 is not a task-A extraction target (its regress must not be trained/recovered).
  IR findings captured in `machinelearning/_ACTIVE/IR-REVIEW-FINDINGS.md` (inference-vs-dialectical,
  grounding-vs-inference, support_scope, commitment reconstruction force) — must inform IR v1.
- **REQUIRED to promote:** (a) a human Sanskrit-specialist review against the PRIMARY TEXT (the packet now
  carries the primary-text requirement); (b) a real extractor that beats the baseline; (c) abstention on a
  NO-SAFE-RECONSTRUCTION case.

## CLAIM P-004 — "The Nyāya gate validates claims."
- **STATUS:** FROZEN — `NYAYA_GATE_CANDIDATE_v1` (BENCHMARKED_PRELIMINARY, NOT independently validated,
  NOT a semantic verifier)
- **EVIDENCE (2026-08-12):** 12 author-made gold fixtures; the Pāṭala-adapted gate run BLIND: **defect
  recall 4/5 (0.80) · clean FP 0/5 (0.00) · abstention 1/2 (0.50)**. Full record + the pre-fix
  savyabhicara bug/fix: `NYAYA-GATE-CANDIDATE-V1.md`.
- **CAVEAT:** the 1 miss is **viruddha**, which requires a real argument graph (knowing the IPVV argues
  memory proves a persistent self). Structural/local defects (asiddha/savyabhicara/satpratipaksa/badhita)
  are partially detected; viruddha is context-dependent and NOT hackable as a keyword.
- **REQUIRED to promote to `verify-claim-semantic`:** real Argument Gold (ARG-001..010) + argument graph;
  viruddha as a graph operation over DebateFrames; independently reviewed gold (30–50 fixtures, ≥2
  reviewers); abstention gap closed.

## CLAIM P-005 — "The Bayesian primitive (strength.py) scores claim support."
- **STATUS:** UNVALIDATED_HEURISTIC (BayesianEvidencePrimitive)
- **EVIDENCE:** math correct (24 tests); weights HAND-CHOSEN, not calibrated.
- **CAVEAT:** no epistemic role until calibrated against adjudicated outcomes.
- **REQUIRED:** calibration on reviewed decisions; Brier/log-loss/calibration vs simpler baselines.

## CLAIM P-006 — "The gold-chain certificate audits cross-layer derivation."
- **STATUS:** INFRASTRUCTURE (renderer) — honest statuses now
- **EVIDENCE:** L0 layer REAL (source_integrity PROVED, morphology SUPPORTED, OPEN cruxes propagate).
  INTERPRETATION/INFERENCE/ESSAY_CLAIM = MACHINE_PROPOSED (fixed; no fabricated EDITOR_APPROVED).
- **CAVEAT:** the L0 floor is real; everything above is machine-proposed until reviewed.
- **REQUIRED to promote:** accepted themes/arguments with real review events enter the chain.

## CLAIM P-007 — "Vidyut improves L0 morphological validation."
- **STATUS:** NOT_RUN (Vidyut P2 not wired)
- **EVIDENCE:** none yet.
- **REQUIRED:** Vidyut over the 3,656 AMBIGUOUS + 2 FAILED records; measure how many ambiguities it
  constrains; characterize CONFIRMED/AMBIGUOUS_SUPPORTED/CONFLICT/UNANALYZED/TOOL_ERROR.

## CLAIM P-008 — "The C1 corpus is a genuine scholarly resource."
- **STATUS:** SUPPORTED (as content)
- **EVIDENCE:** 49 passages, 63 C1s, real content, resolvable.
- **CAVEAT:** C1 quality metrics are unvalidated heuristics (thresholds tuned, not benchmarked).

---

## CLAIM P-011 — "Pāṭala can use two independent Sanskrit analyzers to identify high-risk morphological L0 records."
- **STATUS:** SUPPORTED (calibrated machine witness) — NOT VALIDATED_AGAINST_HUMAN_GOLD (blind review pending)
- **EVIDENCE:** 500/4600-record stratified ensemble (Vidyut × Heritage): **control agreement 84–85%**,
  Vidyut CONFLICT resolution 72% (most conflict is representation mismatch, not L0 error), double-conflict
  ~9% (the genuinely-review-worthy set), double-unanalyzed 0.2%, tool-error 0.2%.
  Reproducible: `verify_l0_p2.py` → `verify_l0_ensemble.py` → `build_p2_review.py`.
- **CAVEAT:** "double-conflict" means both tools fail to support L0 — it does NOT mean the L0 analysis is
  wrong. The blind human review (160 cases, built) will disaggregate REAL_L0_ERROR / GENUINE_AMBIGUITY /
  COMPOUND_ISSUE / BOTH_TOOLS_LIMITED / EDITORIAL_ARTIFACT. That review is logged as non-blocking follow-up.
- **DOES NOT CLAIM:** morphological correctness is proven; double-conflict implies L0 error.
- **ADOPTION GATE:** frozen as a calibrated witness; the blind review (when a reviewer is available) is
  the path to VALIDATED_AGAINST_HUMAN_GOLD.

---

## CLAIM P-012 — "The old lexical ranker (ranker.py) improves P3 lexical-sense selection."
- **STATUS:** NOT_ESTABLISHED (rejected as a witness on the current gold)
- **EVIDENCE:** 21-fixture P3 gold eval: ranker.py top1=0.76, abstention=0.0, false-certainty=1.0. It
  does NOT beat the embedding/lexical-overlap baseline (top1=0.81, abstention=1.0, false-certainty=0.0),
  and it never abstains on NO_UNIQUE_SENSE fixtures. See `docs/p3_lexical_eval_report.json`.
- **CAVEAT:** the gold is v0 (21 fixtures, SINGLE_EDITOR review pending). The embedding baseline (0.81)
  is the current floor any real method must beat; the abstention dimension is decisive.
- **DOES NOT CLAIM:** lexical-sense selection is solved by ranker.py.

---

## CLAIM P-013 — "Pāṭala can propose/resolve L0↔L2 term-anchor alignments as an independently witnessed aid."
- **STATUS:** SUPPORTED_MACHINE_WITNESS (FROZEN — adequate for its consumer, not a semantic validator)
- **EVIDENCE:** `pipeline/l0_align.py` over the 35 V2/V3 passages / 105 inline IAST anchors:
  deterministic aligner resolution recall **0.93**, precision **0.89**, abstention **1.0**; plus an
  independent Vidyut morphological witness (assigns anchor + L0 lemma a common stem):
  **0.81 analyzed-only agreement** (38 AGREE / 9 DISAGREE / 52 UNABLE, analyzed_share 0.47).
  Tests: `pipeline/test_l0_align.py` 26/26. Report: `docs/p4_alignment_eval_report.json`,
  spec: `docs/P4_ALIGNMENT_SPEC.md`.
- **CAVEAT:** P4 is **supporting infrastructure**, not a semantic validator. It proposes/re-solves
  likely anchor↔lemma links; it does **NOT** prove semantic equivalence, translation correctness, or
  replace human philology. The Vidyut witness covers only ~47% of links (UNABLE = inflected/compound
  L0 surfaces Vidyut can't parse — honest abstention, never fabricated). The 9 DISAGREE are mostly
  Vidyut compound-analysis errors, not genuine mismatches.
- **DOES NOT CLAIM:** perfect Sanskrit semantic alignment; that any link is editorially validated.
- **FROZEN (per the adequacy doctrine):** do NOT keep tuning for a third analyzer / compound handling /
  0.81→0.88. Revisit ONLY when a real downstream consumer fails. P4's uncertainty is metadata carried
  into the proposition certificate, not a blocker.

---

## CLAIM P-014 — "A proposition can be serialized as a VERTICAL OBJECT with typed, honestly-resolved evidence links."
- **STATUS:** SUPPORTED (as infrastructure/serialization, v0 FROZEN) — NOT a validated scholarly result
- **EVIDENCE:** `patala_ml/vertical.py` v0 serializes one proposition (ARG-001 G-TC2) with every edge
  TYPED as a `GroundingLink` (relation + resolution + review_state). GOLD grounding uses EXACT L0 refs
  (4 refs resolve; no fuzzy search). C1/L2 at SPAN_LEVEL with exact spans. Proof resolution is REAL:
  the on-disk artifact is marked **STALE** (predates the frozen 35/35 P0), not treated as resolved.
  Artifact: `benchmarks/v0/vertical/vertical-v2o-g-tc2.json` + `tests/test_vertical.py` (0 fail).
- **CAVEAT:** resolution/integrity only — the test does NOT establish that a span entails the
  proposition, that the reconstruction is defensible, or that the proof is authoritative. Missing IR
  fields (research_question, commitment, task_level on ARG-001) are surfaced, not retrofitted.
  **UPDATE (proof seam closed):** Agent 2 regenerated the authoritative V2-O P0 proof; the proof edge
  is now **EXACT / REFERENCE_RESOLVED** (on_disk_PASS True, roundtrip PASS, 0 unresolved) — the vertical
  object fully resolves end-to-end. The remaining gate is independent gold review.
- **DOES NOT CLAIM:** editorial validity; uniqueness of the grounding.
- **REQUIRED to promote (toward the convergence object):** the golds are independently reviewed; a
  reviewed term→anchor mapping; the frozen 35/35 P0 artifact attached; a real evaluator (py-aspic/Nyāya)
  run over the object.

---

## CLAIM P-015 — "Pāṭala can propose a reviewable map of a corpus's conceptual/theme structure (recall-first)."
- **STATUS:** SUPPORTED (as infrastructure / MACHINE_PROPOSED) — NOT adjudicated
- **EVIDENCE:** `patala_ml/theme_discovery.py` over the IPVV/C1 corpus: **100% segment coverage (63/63,
  0 unassigned)**, 83 candidate objects, overlap + unassigned + unstable-sense accounting, and
  C1 + argument integration. Artifacts: `benchmarks/v0/theme-map-ipvv-v0.json` +
  `THEME-MAP-IPVV-REPORT.md`. Recall-first: "complete" = maximise candidate coverage while exposing
  omissions/overlaps — NOT "found every true theme."
- **CAVEAT:** the "themes" are **candidate concept/key-term coverage**, not a mature thematic map.
  Many are generic tokens (`one`/`self`/`lord`); the HIGH-SIGNIFICANCE subset is the discriminative map.
  Kind + sense are MACHINE_PROPOSED pending adjudication.
- **REQUIRED to promote:** the kind/sense adjudication crosses to `ACCEPTED_THEME`.

## CLAIM P-016 — "The CP3 kind-taxonomy distinguishes Themes from Concepts/Domains/Motifs."
- **STATUS:** MODEL_REVIEWED (the kind taxonomy is validated by the three candidates being different kinds)
- **EVIDENCE:** `THEME-REVIEW-001..003` (model): Order-less Support = **LOCAL_THEME** (REVISE),
  Vimarśa = **CONCEPT_TERM_FAMILY** (RETYPE), Pramāṇa = **DOCTRINAL_PROBLEM_DOMAIN** (RETYPE). The three
  are NOT the same kind — so the taxonomy is necessary, not decorative.
- **CAVEAT:** a MODEL review (reconstruction-consistency), NOT specialist philological adjudication.
- **REQUIRED to promote:** a human/specialist confirmation; then `ACCEPTED_THEME` per candidate.

---

## The epistemic labels (the anti-conflation vocabulary)

| Label | Means | Not the same as |
|---|---|---|
| **BUILT** | code exists | TESTED |
| **TESTED** | software behavior tested | BENCHMARKED |
| **BENCHMARKED** | evaluated against independent fixtures | VALIDATED |
| **VALIDATED** | predefined threshold met | EDITOR_REVIEWED |
| **EDITOR_REVIEWED** | actual human review occurred | PRODUCTION |
| **PRODUCTION** | validated + monitored | — |

**The banned words (until independently justified):** PROVED · TRUTH · VERIFIED SEMANTICALLY · CORRECT ·
EDITOR APPROVED · BEST · WINS.
**The allowed words:** SUPPORTED BY · PASSED CHECK X · BENCHMARKED ON · MACHINE-PROPOSED · REVIEWED BY ·
NO CONFLICT DETECTED.

### The two validation labels (never blurred — applies project-wide)

```
ENGINEERING_VALIDATED  =  implementation / fixture behavior verified against a specified machine target
SCHOLARLY_VALIDATED    =  the substantive target itself crossed independent scholarly review
```

**Invariant:** `ENGINEERING_VALIDATED ≠ SCHOLARLY_VALIDATED`. A synthetic fidelity suite that detects
injected corruptions is `ENGINEERING_VALIDATED`; it does NOT make any argument `SCHOLARLY_VALIDATED`.
Thread this vocabulary into `theatre_check.py`, benchmark/run reporting, and any status surface that uses
ambiguous "validated" language. (Source: `handover/agent-1-ml/NEXT-STEPS.md`, `machinelearning/_ACTIVE/DEVPLAN.md` §4.)

### The evidence-hierarchy state machine (from MACHINE_PROPOSED to INDEPENDENT_REVIEWED)

Because live human review may be unavailable, the gate is NOT replaced by pretending it vanished — it is
given a hierarchy of weaker-but-still-useful evidence sources, each with a lower epistemic status. The
state machine:

```
MACHINE_PROPOSED          code / a machine authored it; nothing established
ENGINEERING_VALIDATED     behavior verified against a specified machine target (fidelity, determinism)
MULTI_MODEL_CORROBORATED  several independent machine reconstructions converge when denied the
                          circular derivation path (Sanskrit + L0 only). ≠ human validation.
SCHOLARLY_CORROBORATED    agrees with independent published scholarship (Ratié/Torella/etc. on the
                          exact passage). ≠ direct review of this exact Pāṭala object.
INDEPENDENT_REVIEWED      a qualified human actually reviewed the object. (the real gate)
```

**Distinctions that must never blur:**
```
MULTI_MODEL_CORROBORATED  = machines converge; ≠ human validation
SCHOLARLY_CORROBORATED    = agrees with independent published scholarship; ≠ direct review of this object
INDEPENDENT_REVIEWED      = a qualified human actually reviewed the object
HISTORICALLY_ATTESTED     = a later Sanskrit commentary recognized this reading; ≠ "correct"
STRUCTURALLY_COHERENT     = conclusion follows from encoded premises; ≠ "textually licensed"
```

### The evidence-vector model (instead of a fake binary gold label)

Do not force ACCEPT/REJECT when there is no human. Maintain an evidence vector per object:

```text
primary_text_grounding       strong / supported / weak / absent
morphology                   supported / unresolved
published_scholar_corrob     n/k with exact passages
model_reconstruction_agree   n/k
rival_reading                present / none
attribution_confidence       high / disputed / unknown
scope                        local / systematic / open
```

An object can remain `SCHOLARLY_UNREVIEWED` but be `HIGH_CORROBORATION`. This is more honest than
pretending the benchmark must be binary. (Source: Agent 1 review-packet rebuild, 2026-08-12.)

---

## The three kinds of validity (a permanent principle)

| Validity | Handled by |
|---|---|
| **SOFTWARE** — does the implementation behave per its spec? | tests |
| **EMPIRICAL** — does it perform on independent examples? | benchmarks |
| **SCHOLARLY** — are the examples and judgments intellectually defensible? | experts |

**Tests ≠ benchmarks ≠ expert review. Never report them as interchangeable.**

---

## The abstention principle (Pāṭala should know when NOT to assert)

- Precision over coverage for scholarship: **40% coverage / 98% grounded > 95% coverage / 75% grounded.**
- A good system must be able to abstain: "NO UNIQUE ARGUMENT RECOVERABLE" is a valid, valuable output.
- A model that confidently invents premises where none are recoverable = **severe failure**.
- Metrics include: precision at accepted claims · coverage · **abstention accuracy** · **false-assertion rate**.

---

## The anti-theatre protocol (the 9-field contract)

Every component must fill: **NAME · INPUT · OUTPUT · AUTHORITY · GOLD · BASELINE · METRIC · FAILURE MODE ·
ADOPTION GATE.** If any field is empty, the component is `EXPERIMENTAL_INFRASTRUCTURE`, not a scholarly
capability. See `AGENT1-HANDOVER.md` §4 + the component contracts below.

---

## CLAIM P-018 — "The Pāṭala verifier detects known, deliberately injected corruption (FIDELITY v0)."
- **STATUS:** SUPPORTED (as `ENGINEERING_VALIDATED`) — construction-verifiable, NOT scholarly
- **EVIDENCE:** `machinelearning/research/experiments/build_fidelity_suite.py` +
  `tests/test_fidelity.py`. First run `benchmarks/v0/runs/fidelity-20260812T154041Z.json`:
  **sensitivity 1.0 (9/9) + clean false-positive 0** across FID-SOURCE / FID-PROVENANCE / FID-ALIGNMENT
  (DROP_SPAN, SHIFT_SPAN_START, CHANGE_SOURCE_HASH, BROKEN_REF, STALE_PROOF, MISSING_PROVENANCE,
  REMOVE_ANCHOR, SHIFT_ANCHOR, LINK_WRONG_TOKEN). Clean control (pristine object) passes.
- **CAVEAT:** this is `SYNTHETIC_SENSITIVITY`, NOT `REAL_WORLD_RECALL` — it proves the verifier detects
  error types we inject, not all naturally occurring errors (the latter needs human gold). FID-L0 and
  FID-DEPENDENCY are not yet built.
- **DOES NOT CLAIM:** that any argument is validated, or that the verifier catches real-world errors.
- **REQUIRED to promote (to a broader engineering claim):** FID-L0 (deterministic L0 verifier),
  FID-DEPENDENCY (needs reviewed gold), and wider corruption coverage.

---

## CLAIM P-019 — "Pāṭala has a deterministic canonical structural graph baseline."
- **STATUS:** SUPPORTED (as `ENGINEERING_VALIDATED`) — construction-verifiable, NOT scholarly
- **EVIDENCE:** `machinelearning/research/experiments/benchmark_graph_determinism.py` +
  `tests/test_graph_determinism.py`. Deterministic k-core + connected-components decomposition over the
  theme-map co-occurrence graph (63 nodes / 1780 edges). Canonical hash (`bea595f4…`) is stable under:
  **D1** same-process repeat, **D2** cross-process (fresh subprocess), **D3** input-order permutation
  (node/edge insertion reorder), **D4** canonical serialization (endpoint-sorted undirected edges).
  Run: `benchmarks/v0/runs/determinism-DETERMINISM-20260812T154931Z.json`.
- **CAVEAT:** `DETERMINISM ≠ SEMANTIC_VALIDITY`. The hash being stable proves reproducibility, NOT that
  the clusters correspond to real scholarly themes. The canonical endpoint-sorting of undirected edges
  was required — without it the same graph hashed differently purely from insertion order.
- **DOES NOT CLAIM:** that clusters correspond to real themes; that the decomposition is superior to
  Louvain/Leiden; that graph topology captures philosophical similarity.
- **REQUIRED to promote:** nothing further (this is the reproducible-baseline claim). Louvain is retained
  separately as `EXPERIMENTAL_NONDETERMINISTIC_CLUSTERER`.

---

## CLAIM P-017 — "Pāṭala can propose coarse semantic alignment between contextualized occurrences (Stage A)."
- **STATUS:** INFRASTRUCTURE / harness built; **the generic English encoder baseline is 0/8 (falsified)**
- **EVIDENCE:** `patala_ml/semantic_alignment.py` (6-label vocabulary: SAME/NEAR/PARTIAL/DIFFERENT/AMBIGUOUS/
  NOT_ENOUGH_CONTEXT; 3 representation spaces) + `experiments/benchmark_semantic_alignment.py` + the
  controlled ablation. Gold = THEME-REVIEW-001..003 sense judgments.
- **CAVEAT:** the ablation shows the failure is the encoder/representation space (not context windows);
  a generic English/multilingual model cannot align contextualized Sanskrit philosophy. The harness +
  the falsification is the deliverable; a Sanskrit-aware embedding / cross-encoder is the baseline to beat.
- **DOES NOT CLAIM:** that alignment works, or that any neural score is a scholarly relation.

---

## CLAIM P-020 — "The graph-aware Nyāya audit is a real, separate operation on IR-complete arguments."
- **STATUS:** SUPPORTED (as `ENGINEERING_VALIDATED`) — construction and contextual validation are separate
- **EVIDENCE:** after the CP4 IR gate crossed (all 5 golds IR-complete), `argument.audit_argument(arg,
  comparison_graph)` is the graph-aware Nyāya audit: it runs the structural gate + `check_viruddha_graph`
  (graph viruddha) against a comparison graph, and records an `audit_ref` on the argument. Construction
  (`build_argument`) does NOT claim to do graph audit — it is construction-only. viruddha is a graph
  operation: it checks ESTABLISHED propositions (ASSERTS/DERIVES/SIDDHANTA; RECONSTRUCTED +
  ATTRIBUTES_TO_OPPONENT excluded) for opposite polarity → `VIRUDDHA` candidate with defeater metadata
  (NON_EQUIVALENT_PREDICATE, scope/modality/speaker/...), `semantic_status: UNRESOLVED` — it nominates,
  never settles. Detector is `graph-viruddha-v2` (Unicode-aware tokens, commitment-eligible pool).
- **CAVEAT (honest, learned by inspection + peer review):** the graph viruddha NOMINATES candidates; it
  does not adjudicate them. Manual inspection showed earlier cross-gold "findings" were artifacts
  (akrama polarity-encoding flip, function-word overlap). Fixed: function words dropped, privative terms
  (akrama) treated as absorbing negation (abstention on same-claim), Unicode tokenization. Remaining
  candidates carry NON_EQUIVALENT_PREDICATE + UNRESOLVED, never settled. Original gate benchmark unchanged.
- **DOES NOT CLAIM:** that the gate is a semantic verifier, that any viruddha finding is a settled
  contradiction, that cross-gold hits reflect IPVV disagreement (they may be only our reconstructions),
  or that build_argument performs graph audit.
- **REQUIRED to promote:** the T3/T4 eligibility gate + semantic review of candidates.
- **CAVEAT (honest, learned by inspection):** the graph viruddha NOMINATES candidates; it does not
  adjudicate them. Manual inspection of the 3 initial cross-gold hits showed **all 3 were artifacts**
  (an akrama/order-less polarity-encoding flip on the SAME claim, and a function-word-only overlap) —
  NOT real disagreements. The detector was fixed to (a) drop function words from overlap, (b) exclude
  RECONSTRUCTED and ATTRIBUTES_TO_OPPONENT from the established pool, and (c) carry defeater metadata
  (NON_EQUIVALENT_PREDICATE, scope/modality/speaker/...) so the semantic layer knows what to test.
  A genuine contradiction of the siddhānta (e.g. "the I IS a constructed relation") fires correctly.
- **DOES NOT CLAIM:** that the gate is a semantic verifier, that any viruddha finding is a settled
  contradiction, or that cross-gold hits reflect disagreement in the IPVV (they may reflect disagreement
  only in Pāṭala's own reconstructions).
- **REQUIRED to promote:** the T3/T4 eligibility gate (source spans resolve + commitment known +
  scope/modality/speaker compared + independent published evidence) + semantic review of candidates.

---

## CLAIM P-021 — "Pāṭala extracts commitment-sensitive cross-argument tension CANDIDATES."
- **STATUS:** SUPPORTED (as machine-discovered tension candidates) — NOT settled disagreements, NOT fixtures
- **EVIDENCE:** `experiments/build_disagreement_candidates.py` classifies graph-viruddha cross-gold
  hits by commitment type and writes `benchmarks/v0/disagreements/cross-gold-candidates.json`. All 3
  candidates are `RECONSTRUCTION_TENSION_CANDIDATE` (a RECONSTRUCTED conclusion vs a TEXTUALLY_COMMITTED
  proposition) — correctly reflecting that the tension is between Pāṭala's own reconstructions and the
  text's asserted propositions, NOT a settled disagreement in the IPVV. Candidate schema carries
  left/right commitments + pools + overlap basis + possible defeaters + `semantic_status: UNRESOLVED`.
- **CAVEAT (honest):** an earlier version wrongly emitted these as `RIVAL_READING` fixture disagreements;
  manual inspection showed all 3 initial hits were artifacts (akrama polarity-encoding flip, function-word
  overlap). Retracted. The candidate extractor now NEVER emits settled fact — only `_CANDIDATE` classes.
- **DOES NOT CLAIM:** that any candidate is a real philosophical disagreement, or that the detector has
  established precision.
- **REQUIRED to promote to T3/T4 fixture:** the eligibility gate (source spans resolve + commitment known
  + scope/modality/speaker compared + independent published evidence) + a surviving manual audit.

## CLAIM P-023 — "Pāṭala produced one end-to-end epistemically constrained prose vertical (peer-review-clean relative to the current objects)."
- **STATUS:** SUPPORTED (one synthesis; a DEMONSTRATION, NOT a validated capability)
- **EVIDENCE (2026-08-12):** `SYN-IPVV-REFLEXION-CORE-001` (canonical ArgumentSynthesis, bridge `SYN-INF-001`
  reconstructed + UNRESOLVED, weakest-governs ceiling) → monotone EO projection → one readable essay +
  `SentenceEvidenceAudit` (`ESSAY-IPVV-REFLEXION-CORE-001.{md,audit.json}` + EssayPlan), pushed on
  `origin/agent1-argument-layer-a1b`. The audit catches 6 corruption classes (strength inflation, authorship
  laundering, boundary erasure, rival laundering, warrant erasure, paraphrase expansion) via metadata-driven
  checks (not forbidden-word regex). All test suites pass.
- **CAVEAT (honest):** for ONE IPVV synthesis only. The semantic-relation labels (`EXACT /
  CONSERVATIVE_PARAPHRASE / EXPANSIVE`) are reviewer-assigned assertions, NOT independently machine-proven
  facts — C.1 rejects *declared* unsupported expansion but does not yet auto-establish that a declared
  `CONSERVATIVE_PARAPHRASE` is semantically correct. `reconstructable argument ≠ structurally validated
  argument` (S010 frozen). NOT "Pāṭala writes reliable scholarly essays."
- **REQUIRED to promote (→ a real essay capability):** many more syntheses + independent review.

## CLAIM P-024 — "Pāṭala has a deterministic structural k-core hierarchy over the C1 evidence graph, plus a real Louvain ablation (P-019 v2)."
- **STATUS:** SUPPORTED (as ENGINEERING_VALIDATED, structural — NOT a theme)
- **EVIDENCE (2026-08-12):** `patala_ml/kcore.py` + `build_kcore_structure.py` produce a
  `CoreStructureProposal` over the frozen C1 evidence graph (see_also w=1.0 + key-term w=0.5·Jaccard min0.3,
  body excluded, edge_evidence preserved): k-core number/shell/component/structural-role per C1 + a canonical
  graph_hash. Byte-identical across separate processes + insertion-order permutations
  (`test_kcore_reproducibility.py`, 3x stable). Artifact: `benchmarks/v0/structural/kcore-ipvv-c1-v0.json`
  (max_core=3; 17 C1s at top core = density, not centrality). `louvain_baseline` + a comparison/synthesis field
  populated from a REAL partition (regenerated with python-louvain, k-core hash unchanged `96f6623cd5963e98`).
- **EMPIRICAL FINDING:** on the actual 63-node IPVV C1 graph, Louvain is STABLE — 11 communities across 20
  seeds + insertion-order permutations, 0 unstable co-membership boundaries, 187 robust pairs
  (`louvain-stability-ipvv-c1-v0.json`). So k-core's rationale is **deterministic structural embeddedness +
  reproducible graph statistics, NOT because Louvain was empirically unstable here**.
- **CAVEAT:** `k_core != theme`. High core_number = density under representation R, NOT "philosophically
  central". Neither k-core nor Louvain is an AcceptedTheme; no claim of semantic/philosophical validity.
- **REQUIRED to promote (→ theme):** human adjudication of whether any structure deserves `AcceptedTheme`.
