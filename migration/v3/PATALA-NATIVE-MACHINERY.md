# PĀṬALA V3 — THE PATALA-NATIVE MACHINERY (the actual Pāṭala-built code v3 must not lose)

*2026-08-14 · status: THE DOMAIN MACHINERY · the ACTUAL Pāṭala-built code (from `endgamebuild/`,
`source-evidence/`, `contracts/`, `pipeline/`, `data/`) that v3 was missing — it grounded the lab's
GENERIC kernels but dropped Pāṭala's DOMAIN machinery. This doc restores it: every piece is real, built,
and verified to exist. v3 = the lab's proven generic kernels + Pāṭala's actual domain machinery.*
*The split: **the ip-graph lab proved the GENERIC mechanisms** (epistemic envelope, reducers, staleness,
education). **Pāṭala built the DOMAIN machinery** (reconciliation, the golds, the translation flow, the
atlas, the eval plane). v3 needs both.*

---

## WHAT V3 WAS MISSING (validated — all present in Pāṭala, absent from v3)

### 1. THE RECONCILIATION ENGINE (Track A — the connective layer) — ✅ built, was missing
**What:** Pāṭala's position as the reconciliation/connective layer over Gyan Bharatam/OCHS/NGMPP/IFP/
Muktabodha/GRETIL/SARIT. The concrete machinery:
| Piece | File | Status |
|---|---|---|
| P4 manuscript-resolution gold | `evals/.../manuscript_resolution_gold.py` (10 frozen cases, FALSE_MERGE_RATE primary) | ✅ |
| P3 entity reconciliation engine | `evals/.../entity_reconciliation.py` (typed CandidateMatch: EXACT/PROBABLE/POSSIBLE/CONFLICT/UNRESOLVED) | ✅ |
| P3↔P4 loop | `evals/.../run_reconciliation_eval.py` (FALSE_MERGE_RATE=0, abstains 30%) | ✅ |
| P2 ExternalRecord + adapter framework | `schema/external_record.py` (raw-immutable + ReconciliationAdapter contract + maturity ladder) | ✅ |
| Text fingerprints | `schema/text_fingerprint.py` (incipit/explicit/ngram/MinHash + candidate_rank) | ✅ |

**Why v3 needs it:** this is the "OpenAlex for Sanskrit" connective layer — how Pāṭala resolves the
fragmented ecosystem onto one canonical ID. It's the identity layer's real machinery.

### 2. THE 5 GOLDS (the anti-theatre evidence) — ✅ built, was missing
| Gold | File | Count |
|---|---|---|
| Recovery gold | `data/evaluation/recovery-gold-v1.json` | 51 cases |
| Nyāya gate gold | `benchmarks/v0/evidence/nyaya-gate-gold.jsonl` | 12 |
| P3 lexical gold | `docs/p3_lexical_gold_v0.json` | — |
| P4 alignment eval | `docs/p4_alignment_eval_report.json` | — |
| Manuscript-resolution gold | `evals/.../manuscript_resolution_gold.py` | 10 |

**Why v3 needs it:** these are the *independent evidence* that make every `[PROVEN]` claim real. The
graduation test runs on them.

### 3. THE CANONICAL DAG (the dependency truth) — ✅ built, was missing
- **File:** `contracts/CANONICAL-DAG.yaml` — the ONE dependency manifest every consumer derives from.
- **Why v3 needs it:** v3's LAYERS.yaml lists layers; the canonical DAG is the *authoritative dependency
  order* (SOURCE→T1→L0→ARGMAP→L2→L200→C1→...). It's the machine truth behind staleness.

### 4. THE FACTORY LOOP (the live autonomous driver) — ✅ built, was missing
- **Files:** `pipeline/factory_loop.sh` (the overnight autonomous driver) + `register_sources.py` +
  `factory_scheduler.py` + `start_overnight.sh`
- **Why v3 needs it:** this is how the factory actually RUNS — the loop that advances layers. v3 names
  the reactive factory; this is its current running form.

### 5. THE EVAL / VERIFICATION PLANE (the anti-theatre gate) — ⚠️ partial
- **Files:** `source-evidence/evals/patala/tasks/` — atlas_nat, argmap_eval, argument_recovery_bench,
  warrant_reconstruction, essay_bench, edu_bench, source_authority, evaluation_candidate/finding.
- **Why v3 needs it:** the eval plane is how anything is proven real. v3 mentions NAT/gold but not the
  actual task files.

### 6. THE IDENTITY CROSSWALKS (ORCID/ROR) — ✅ built, was missing
- **Files:** `source-evidence/production/adapters/identity_crosswalk.py` (name-variant→Person,
  institution→ROR) + `metadata_resolver.py` (Crossref/OpenAlex) + `opencitations.py` (SOURCE_ECHO detection)
- **Why v3 needs it:** the identity layer's external adapters — the "WIRED" tools v2 cataloged.

### 7. THE ATLAS QA + SEMANTIC RECOVERY — ✅ built, was missing
- `atlas_qa_audit.py` (authority-inflation/completeness/rights audit — the P5 continuous QA)
- `semantic_recovery_judge.py` (2-stage: embedding align + structured judge — the recovery scorer)
- `scholar_graph_eval.py` (SourceAssertion+CorroborationEvent suffices)

### 8. THE ARGUMENTATION IR (the frontier, the moat) — ⚠️ partial
- **Files:** `ai/` (VISION.md, argumentation-ir-frameworks-survey, argumentation-ir-exec-summary) +
  `machinelearning/_ACTIVE/ARGUMENT-IR-VISION.md` + `ai/TAKEAWAYS.md`
- **Why v3 needs it:** this is the *historically-grounded philosophical IR* that is the actual moat
  (per the mixxii + philosophy-engine reviews). v3's Argument layer borrows ASPIC/AIF but the IR itself
  is Pāṭala-native.

### 9. THE FACTORY CERTIFICATES — ✅ built, was missing
- **Files:** `factory-certificates/L0-v1/`, `L200-v1/` + `pipeline/certificate_l0.py`, `certificate_l200.py`
- **Why v3 needs it:** the deterministic floor certificates (lossless, bound, fail-closed) — the proof
  that the translation/proof floor is real.

### 10. THE BIBLIOGRAPHY SEEDS — ✅ built, was missing
- **Files:** `data/atlas/audited.ts` (Trika-10 full depth), `bibliographySeed.ts` (58), `seed60.md`,
  `atlas-bibliography.json` (254 compiled)
- **Why v3 needs it:** the identity layer's rich data (thin-vs-rich — the ATLAS-100 backfill gap).

---

## THE PATALA ↔ LAB SPLIT (what each side contributes to v3)

| Concern | Pāṭala (domain machinery) | ip-graph lab (generic kernels) |
|---|---|---|
| Identity | atlas, bibliography, crosswalks | — |
| Reconciliation | entity_reconciliation, fingerprints | — |
| The golds | the 5 golds + IPVV | validate-stack, scifact |
| Translation | the flow, certificates, TranslationProof gold | translation.py (the vector) |
| Argument | the IR (ai/, ARGUMENT-IR-VISION) | review.py, crux-compiler |
| Review | review_engine, contracts_human_authority | scholar_review.py (panel+citecheck) |
| Factory | factory_loop, canonical-DAG, scheduler | staleness.py, evolve.py |
| Eval | the eval plane, the 5 golds | theatre-check |
| Education | — | education.py, pedagogy.py, organism.py |
| Production | .meta (essay/render/publish) | agent_delivery.py |

**v3 = the lab's proven generic kernels + Pāṭala's actual domain machinery.** Dropping either makes it
incomplete: the lab without Pāṭala has no gold/domain; Pāṭala without the lab has no proven generic
machinery. Together they are the organism.

---

*This restores the Pāṭala-native machinery v3 had dropped. Every piece is real and verified (reconciliation
engine, 5 golds, canonical-DAG, factory loop, eval plane, crosswalks, atlas QA, argumentation IR, factory
certificates, bibliography seeds). v3 = lab's generic proven kernels + Pāṭala's domain machinery. See
`endgamebuild/INFRA-INVENTORY.md` for the authoritative "what exists" list.*
