# DSPy — typed, measurable extraction programs

**What Pāṭala borrows:** programmatic optimization of AI pipelines — typed modules with measurable
outputs, optimized against a gold target (MIPRO, GEPA).

**License:** MIT. Repo: `stanfordnlp/dspy`.

## How Pāṭala consumes it
**PLANNED.** Replace hardcoded giant prompts with typed modules:
```text
QuestionExtractor   → canonical question accuracy
PositionExtractor   → attribution correctness
EvidenceLinker      → exact source-span F1
ArgumentExtractor   → edge precision
TermSenseExtractor  → semantic-inflation failures
```
Optimize against Pāṭala's gold review data.

## Doctrine
Path from prompt pipeline → measured program → optimized program. Pāṭala gold = the optimizer target.
