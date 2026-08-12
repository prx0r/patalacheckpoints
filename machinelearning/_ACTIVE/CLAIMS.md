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
  `validate_gold`-consistent, `review_state=CANDIDATE`). A **primitive baseline extractor** was run BLIND
  against them (the CP4 Build-4 gate). Baseline metric (bounded, `baseline-v0-lexical-proposition-overlap`):
  **macro lexical-overlap F1 0.36 · role macro-F1 0.58 · explicitness 0.63 · grounding 1.0 · inference
  recovery 0.0**; on **Task A** (proposition extraction) nodes only, macro F1 ≈ 0.36. Immutable run:
  `benchmarks/v0/runs/2026-08-12T124709Z/`. This is the BASELINE, not a capability.
- **CAVEAT:** a sentence-level baseline cannot recover abstract/reconstructed gold propositions (ARG-001 F1 = 0.0)
  and produces NO inference graph. Golds are `CANDIDATE` — machine-authored, **not yet independently reviewed**.
  ARG-003's infinite-regress warrant is marked `candidate_reconstruction` pending specialist confirmation;
  ARG-005 is typed `INTERPRETIVE_SCOPE` (local vs systematic), not an ambiguity. Review protocol:
  `machinelearning/research/experiments/ARG-GOLD-REVIEW-PROTOCOL.md`.
- **REQUIRED to promote:** (a) independent editorial review of the 5 golds (the review protocol); (b) a real
  extractor that beats this baseline (lexical-overlap F1 + inference recovery > 0, low false-assertion) on a
  frozen held-out split, compared mainly to Task A; (c) abstention on a genuine NO-SAFE-RECONSTRUCTION case.

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

## CLAIM P-014 — "A proposition can be serialized as a VERTICAL OBJECT resolving to its source + proof."
- **STATUS:** SUPPORTED (as infrastructure/serialization) — NOT a validated scholarly result
- **EVIDENCE:** `patala_ml/vertical.py` resolves one proposition (ARG-001 G-TC2) all the way down:
  ResearchQuestion → Argument → Inference → Proposition → C1 → L2 → L0 anchor → SourceSpan → Sanskrit →
  PhilologicalProof, every arrow to real data. Artifact: `benchmarks/v0/vertical/vertical-v2o-g-tc2.json` +
  `tests/test_vertical.py` (0 fail).
- **CAVEAT:** the term→L0-anchor mapping is an explicit `key_terms` judgment (machine-proposed, NOT
  reviewed). The on-disk proof for this chunk predates the frozen 35/35 P0 (the authoritative `proof_id`
  is referenced, not substituted). ARG-001 lacks a first-class `research_question`/`commitment` (older
  schema). The vertical object is a consumer of Agent 2's L0 floor, not an independent result.
- **DOES NOT CLAIM:** that the proposition is editorially valid, or that the mapping is unique.
- **REQUIRED to promote (toward the convergence object):** the golds are independently reviewed; a
  reviewed term→anchor mapping; the frozen 35/35 P0 proof attached; a real evaluator (py-aspic/Nyāya)
  run over the object.

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
