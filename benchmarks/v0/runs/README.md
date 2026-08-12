# BenchmarkRun policy — runs/ vs scratch/

Per METRICS.md §4, every `BenchmarkRun` is one immutable directory. This file fixes the **lifecycle**
so scientific mistakes are recorded honestly rather than hidden.

## The two places

| Location | Kind | Lifecycle |
|---|---|---|
| `runs/<ts>/` | **official BenchmarkRun** | **append-only once written with `status: COMPLETED`**. Never delete or edit. |
| `scratch/` | disposable development output | may be overwritten/deleted freely (debugging noise, pre-fix iterations). |

## When an official run turns out wrong

You may NOT delete a completed run because you dislike it. Instead mark it invalid:

```json
{
  "status": "INVALIDATED",
  "superseded_by": "<new run dir name>",
  "reason": "metric implementation bug: <short description>"
}
```

Keep it. It is more scientifically useful to show a mistake and its correction than to pretend it
never happened. Deleting a run that was never registered / was a scratch iteration is fine.

## How to register

The runner writes `benchmark_version.json` with `"status": "COMPLETED"` only when the run is final.
A run directory without `status: COMPLETED` is a draft and may be cleaned up before designation.

## Current runs

| Dir | Task | Status |
|---|---|---|
| `2026-08-12T124709Z` | ARGUMENT_EXTRACTION (primitive baseline, Task A) | COMPLETED |
