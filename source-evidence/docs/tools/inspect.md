# Inspect AI — the benchmark runtime (Pāṭala's evaluation plane)

**What Pāṭala borrows:** the ENTIRE benchmark runtime — datasets, agents/solvers, tools, model-provider
abstraction, **custom scorers**, multiple scorers, model graders, sandboxing, reproducible eval logs, log viewer,
offline rescoring, and **scanners** (transcript inspection for evaluation corruption). Pāṭala does NOT build a
benchmark framework.

**License:** MIT.

## API / usage (Python framework, not a server)
- `pip install inspect_ai`; define a task with `@task`, `solver`, `scorer`, `scanner`.
- `inspect eval <task>` → produces an `.eval` log (JSONL) with task/model/solver config + per-sample execution,
  messages, scores, metadata.
- `inspect view` → the web log viewer.
- Custom scorers: `scorer()` returning per-sample scores (multiple scorers allowed — never crush into one metric).
- Scanners: `scanner()` examining reasoning/execution traces for shortcuts/errors/eval-awareness.
- Community registry: `inspect evals` — external eval implementations can be registered
  (`pip install patala-evals; inspect eval patala_evals/tantrafact`).

## Rate limiting / etiquette
Local, offline by default. Real model calls go through the model-provider abstraction (respect provider rate
limits). No public API to hammer — the etiquette is *reproducibility*: pin task/model/solver versions, keep the
corpus snapshot frozen (see CRAG mock-API), and never let benchmark runs depend on live external state.

## How Pāṭala consumes it
```
TantraFact / ArgumentBench / CorroborationBench / CitationBench / PāṭalaQA
   → Inspect tasks with custom scorers (verdict/span/attribution/scope/warrant/false-corroboration)
   + scanners (citation_laundering, scope_strengthening, unsupported_addition, benchmark_leak, gold_phrase_copying)
   → Pāṭala BenchmarkRun ↔ Inspect EvalLog
```
**Priority: IMMEDIATE — port the existing argument + corruption tests into one Inspect task.**
