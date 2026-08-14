# THE EVALS & BENCHMARKS INDEX — the real evaluation plane

*2026-08-14. The catalog of Pāṭala's **real benchmarks and evaluations** — the frozen golds, the NAT
(Need-A-Test) adversarial suites, the benchmark fixtures, and the eval runners. This is the "how is
Pāṭala tested?" reference — complementing `GOLD-EVIDENCE-INDEX.md` (the results) with the *testing
infrastructure and frozen benchmark data*.*

> **The principle:** per the anti-theatre doctrine, a claim is only real if it's benchmarked against
> frozen gold with a reproducible eval. THIS is that plane — the frozen benchmarks and the NAT tests.

---

## 1. THE BENCHMARK SUITE — `benchmarks/v0/`

| Asset | What |
|---|---|
| `MANIFEST.json` / `SCHEMA.md` / `SPLITS.md` / `METRICS.md` / `FIDELITY-v0-SPEC.md` | the benchmark contracts |
| `ARG-GOLD-REVIEW-PACKET(-v2).md` + `.json` | the primary-Sanskrit-grounded argument review gold |
| `semantic-shift-atlas.json` | **16 lemmas × 25 senses** (the lemma→sense evidence graph) |
| `theme-map-ipvv-v0.json` + `theme-discovery-ipvv-v0.json` | the IPVV theme discovery results |
| `semantic-alignment-bench-v0.json` | the semantic-alignment benchmark |
| `THEME-ADJUDICATION-PACKET.md` + `THEME-MAP-IPVV-REPORT.md` | the theme adjudication packets |
| `corroboration/` `disagreements/` `evidence/` `retrieval/` `structural/` `vertical/` `review/` `runs/` `packs/` | the per-domain benchmark dirs |

## 2. THE REVIEW PACKETS — `benchmarks/v0/review/`

The real argument/essay/education review evidence:
| Asset | What |
|---|---|
| `ARG-GOLD-REVIEW-PACKET-v2.json` | the frozen argument review |
| `ARG-EVIDENCE-MATRIX.json` · `ARG-IR-AUDIT.json` | the argument-evidence matrix + IR audit |
| `EO-IPVV-REFLEXION-CORE.json` | the education object (reflexion core) |
| `ESSAY-IPVV-REFLEXION-CORE-001{.md,.v2.md,.audit.json,.SUPERSEDE.json}` | the IPVV essay + audit + supersede (the honest essay-review trail) |
| `ALL-ARGMAP-EDUCATION-PACKETS.json` | 250 education interaction packets compiled from 50 real ARGMAPs |
| `REVIEW-2026-08-12-MODEL-1.json` | the first model review |
| `PATALA-VERTICAL-1-CERTIFICATE.json` | the gold review vertical certificate |

## 3. THE NAT TESTS (adversarial, frozen-gold) — `source-evidence/evals/patala/tasks/`

The Need-A-Test / adversarial evaluation suites (each measures whether the system fails an obvious trap):
| NAT / bench | What it tests |
|---|---|
| `atlas_nat.py` + `atlas_nat_natural.py` (51 frozen natural cases) | the Atlas authority gate |
| `argmap_ipvv_eval.py` + `argmap_eval.py` | the IPVV ARGMAP reconstruction |
| `argument_recovery_bench.py` | argument recovery (the judge) |
| `manuscript_resolution_gold.py` + `run_reconciliation_eval.py` | reconciliation (FALSE_MERGE_RATE) |
| `essay_bench.py` · `edu_bench.py` · `warrant_reconstruction.py` | essay/education/warrant |
| `source_authority.py` · `atlas_qa_audit.py` | source authority + the authority-inflation audit |
| `evaluation_candidate.py` + `evaluation_finding.py` | the cross-lane eval contract |
| Gold: `data/evaluation/recovery-gold-v1.json` (51 cases) | the recovery gold |

## 4. THE EVAL LOGS — `logs/*.eval` + `source-evidence/evals/logs/`

The actual Inspect eval runs (frozen, reproducible):
`l0-proof-*.eval` · `tantra-gold-*.eval` · `atlas-nat-natural-*.eval` — the recorded runs with results.

---

## 5. HOW AN AGENT USES THIS

```text
"how is Pāṭala tested?"  →  this index
  → the benchmark contracts (MANIFEST/SCHEMA/SPLITS/METRICS)  →  the frozen eval gold
  → the NAT tests (atlas/argmap/manuscript/essay/edu)          →  the adversarial suites
  → the review packets (argument/essay/education)              →  the per-object review evidence
  → the eval logs                                            →  the recorded runs
```

**The anti-theatre note:** the eval plane is REAL and tested — the 10 eval self-tests pass, the NAT
suites are frozen against gold, and the runs are recorded. This is where Pāṭala's claims are made
falsifiable.

---

*This is the evals & benchmarks index. It completes the "what actually exists" documentation:
`GOLD-EVIDENCE-INDEX.md` (results) · `DATA-ASSETS-INDEX.md` (data) · `INTERFACES-INDEX.md` (callable) ·
`EVALS-BENCHMARKS-INDEX.md` (how it's tested).*
