# Inspect AI — PĀṬALA-ARG-LAUNDRY-SYN v0.1

*2026-08-12. The **Track C** evaluation-plane benchmark (Global Architecture v0.1), running on the
**Inspect AI** runtime. This is a **synthetic-sensitivity** benchmark, NOT real-world detection.*

## What this proves (and doesn't)

**PĀṬALA-ARG-LAUNDRY-SYN v0.1 is a valid synthetic-contract benchmark.** It tests the detector's correctness
against an **independently specified** synthetic contract — gold is specified independently, never derived from
the detector. For the controlled transformations in `GOLD`, the detector's sensitivity and specificity are
measured directly. The architectural proof is also real: a frozen deterministic Pāṭala audit was moved into a
real Inspect task (Dataset → Solver → custom Scorers → EvalLog), no model calls needed. **Inspect can be the
evaluation runtime instead of us building one.**

What this does **not** establish is **NAT/GEN real-world performance** (real laundering produced by models in
the wild, or whole-pipeline output). Those are separate claims, not built yet.

The benchmark claims are **SYN only**:

| Claim | Covers | Status |
|---|---|---|
| **PĀṬALA-ARG-LAUNDRY-SYN** | known-good audit + controlled mutations → does the checker detect known corruption? | **this file (v0.1)** |
| PĀṬALA-ARG-LAUNDRY-NAT | naturally occurring model outputs + independent adjudication | not built |
| PĀṬALA-ARG-LAUNDRY-GEN | model asked to produce prose/audit → checker runs downstream → whole pipeline | not built |

> A perfect SYN score establishes **synthetic sensitivity of the detector to injected corruption**, NOT
> that the detector finds real laundering in the wild. Don't let "Inspect benchmark passes" become evidence
> of real-world semantic detection.

## The critical fix from v0 (circular gold → independent gold)

v0 (99dec61) derived every target from `check_audit()` itself:

```text
gold(x)     = detector(x)
prediction(x) = detector(x)
```

so `gold == prediction` by construction — the benchmark could **not** falsify the detector, and a missed
mutation was silently labelled PASS. That is the exact class of mistake the anti-theatre doctrine forbids.

**v0.1 fixes it:** the `GOLD` table is hardcoded from the mutation *semantics* (`{fixture_id → expected}`),
never by running the detector. Now:

```text
detector output  vs  independently specified expected behavior
```

A missed mutation is now a **real benchmark failure**. Proof of the fix: when a control fixture was
mis-specified (`C03_BOUNDARY_QUALIFIED` labelled PASS), the detector correctly FAILed it and 17/18 exposed a
genuine gold error — exactly the kind of catch circular gold would have hidden.

## Fixture design

Every sample carries a **FROZEN candidate object** — the (possibly mutated) audit JSON + the authority
context — as its solver-visible `input`. The solver consumes **only that object**; it does not receive the
mutation-family recipe and cannot know which mutation was injected. Any future solver (LLM reviewer, hybrid,
external baseline) can run the same frozen sample.

Gold (`GOLD`) — **5 must-PASS controls + 14 must-FAIL laundering mutations** across Commit-C rules C01–C07:

- **Controls (must PASS):** CLEAN · C06_EXPLANATORY/TRANSITION (exempt prose) · C07_EXPANSIVE_WITH_SUPPORT ·
  C05_RIVAL_SOURCED_QUALIFIED
- **Laundering (must FAIL):** C01_MISSING_{CLAIM,SOURCE}_REFS, _AUDIT_BLOCK · C02_BYPASS_WARRANT ·
  C03_{INFLATE_STRENGTH,AUTHORS_LAUNDER,DIRECT_RENDER,ATTRIBUTION_AUTHOR} · C03B_DIRECT_UNDER_SUPPORTED ·
  C03_BOUNDARY_QUALIFIED · C04_DROP_BOUNDARY · C05_RIVAL_ASSERT ·
  C07_{INVALID_SEMANTIC_RELATION,EXPANSIVE_NO_SUPPORT}

Controls are essential: they prevent the detector from "winning" by rejecting everything.

## Metrics

Three aggregate statistics (NA-safe):

```text
verdict_accuracy       = correct / total
clean_specificity      = clean correctly accepted / all clean   (1 - FPR)
mutation_sensitivity   = mutations correctly rejected / all mutations   (1 - FNR)
```

Current result (v0.1, pinned runtime): **1.000 / 1.000 / 1.000** (19/19).
`clean_specificity` and `mutation_sensitivity` are NA-safe: with zero fixtures of a class they return `NaN`
rather than inflating an aggregate.

## Run (deterministic — no model calls)

```bash
# 1. build + inspect the 19 fixtures
machinelearning/research/.venv/bin/python source-evidence/evals/inspect_arglaundry.py

# 2. run the eval (writes an Inspect EvalLog)
cd /root/projects/patala
machinelearning/research/.venv/bin/python -m inspect_ai eval source-evidence/evals/inspect_arglaundry.py
# → log: logs/<ts>_arglaundry_<id>.eval
```

## Benchmarks in this package

| Benchmark | File | SUT | Claim class | Fixtures |
|---|---|---|---|---|
| **PĀṬALA-ARG-LAUNDRY-SYN** | `inspect_arglaundry.py` | Commit-C essay-audit detector (`check_sentence_evidence_audit.check_audit`) | SYN | 19 (5 PASS + 14 FAIL), C01–C07 |
| **PĀṬALA-L200-SYN** | `inspect_l200.py` | L200 typed-reference checker (`certificate_l200.check_dim`) | SYN | 11 (5 PASS + 6 FAIL), incl. the F6 IA→MT laundering case |
| **PĀṬALA-ARG-LAUNDRY-NAT** | `inspect_arglaundry_nat.py` | Commit-C detector on natural outputs (frozen authority snapshot) | NAT | harness; corpus in `nat/arg-laundry/` |
| **PĀṬALA-L200-CHECKER-NAT** | `inspect_l200_nat.py` | `check_dim` given proposal + adjudicated reference | NAT | harness; corpus in `nat/l200/` |
| **PĀṬALA-L200-DETECTOR-NAT** | `inspect_l200_detector_nat.py` | independent semantic detector (future) | NAT | harness only — no SUT yet |
| **EVAL-CONTRACT** | `EVAL-CONTRACT.md` | the 12-field contract every eval MUST satisfy | — | all |
| **L200 export contract** | `EVAL-CONTRACT-L200-EXPORT.md` | Agent2→Agent1 immutable candidate bundle | — | lane-safe NAT |

All share the same Inspect contract: **independent gold** (never derived from the SUT), solver-visible
frozen objects (never the mutation recipe or hidden gold), hidden fixture metadata, real split metrics, and
full versioning (inspect version + complete dataset hash + SUT-only hash) in the EvalLog.

## NAT status (honest — see `nat/README.md`)

The NAT **harnesses ship**; the NAT **corpora are not yet collected.** The historical natural corpus is
sparse (the only ARG audit on disk is the object used to build SYN; Agent 2's live L200 proposals are not
yet exported as frozen objects). Per the anti-theatre doctrine, natural samples must be frozen prior
outputs + independent adjudication, sampled across clean/problematic/borderline — not fabricated. An empty
NAT run is NOT a result and fails loudly.

## Run

```bash
# any single benchmark
machinelearning/research/.venv/bin/python -m inspect_ai eval source-evidence/evals/inspect_arglaundry.py
machinelearning/research/.venv/bin/python -m inspect_ai eval source-evidence/evals/inspect_l200.py
```

## Claim classes (SYN / NAT / GEN — keep distinct)

- **SYN** — known-good object + controlled mutation → does the checker detect known corruption? *(these two)*
- **NAT** — naturally occurring model outputs + independent adjudication → does the checker detect real
  laundering? *(next; the F6 live canary is a candidate NAT failure)*
- **GEN** — model asked to produce output → checker runs downstream → whole pipeline evaluated.

A perfect SYN score establishes synthetic sensitivity to injected corruption, **not** real-world detection.
Do not let "Inspect benchmark passes" become evidence of NAT/GEN performance.

## Versioning (the evaluation substrate is pinned, not drifting)

The EvalLog metadata records, for reproducibility:
- `bench=PĀṬALA-ARG-LAUNDRY-SYN`, task version
- `pinned_inspect=inspect-ai==0.3.258` (also in `requirements.txt`)
- `dataset_hash` (SHA of all sample metadata)
- `detector_sha` (SHA of the frozen detector source = SUT fingerprint)

Changes to the substrate (bumping `inspect-ai`, changing the detector, expanding the suite) must be explicit
and re-recorded as a fresh BenchmarkRun — never silent drift.

## Honest status & next steps

- **Verified:** Inspect loads the task, runs all 19 samples through the deterministic detector, computes the
  split metrics, and writes a `status=success` EvalLog with full versioning metadata.
- **The Inspect `scanner` API** is version-specific (installed `0.3.258` lacks `inspect_ai.scan`); the task
  does not fake scanner support. Add laundering scanners once the installed version exposes them.
- **Next:** (1) port a second existing benchmark (e.g. the fidelity suite or L200) to prove the Inspect
  abstraction generalizes; (2) wire a model solver so the detector becomes a *checker on model output* rather
  than the solver; (3) only then start CorroborationBench / TantraFact. Do not conflate SYN with NAT/GEN.
