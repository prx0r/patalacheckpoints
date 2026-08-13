# CiteVQA — the Strict Epistemic Accuracy metric (benchmark design)

**What Pāṭala borrows:** the concept of separating **answer correctness** from **citation/evidence correctness**,
and requiring BOTH for an answer to be correct. Pāṭala's "strict epistemic accuracy" for PāṭalaQA.

**License:** open benchmark; we borrow the *metric concept*, not the dataset.

## The metric
```
PAA  = AnswerCorrect ∧ AttributionCorrect
PEA  = AnswerCorrect ∧ EvidenceCorrect ∧ AttributionCorrect ∧ ScopePreserved   ("Strict Epistemic Accuracy")
```
A model must NOT get full credit for a correct answer that cites the wrong evidence. This principle runs through
all Pāṭala benchmarks.

## How Pāṭala consumes it
Apply `PEA`-style scoring in TantraFact / CorroborationBench / CitationBench (via Inspect custom scorers): a
proposition is only "supported" if the evidence span is correct AND the attribution AND the scope are preserved —
not merely because the verdict happened to be right.

**Priority: benchmark design (fold into the Inspect scorers).**
