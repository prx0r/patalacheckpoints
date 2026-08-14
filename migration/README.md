# migration/ — high-level migration plans & scripts

*Holding area for cross-cutting migration work: data/byte migrations between the R2 data lake,
`sanskritree`, `research-library`, and the Pāṭala factory registry; schema/migration scripts; and
one-shot transformations that don't belong in `pipeline/` or `ingestion/`.*

## What's here

| Path | What it is |
|---|---|
| `v2/` | **the Pāṭala v2 blueprint** — the coherent-system spec (strategy, architecture, layer/mapping, modules, current→vision, ground-up plan, goated docs). This is where the future lives. |
| `mixxii` | the systems review (imported from R2) — the epistemic-wind-tunnel analysis that shaped v2 |

**If you are a new agent, go to `v2/README.md` and follow its reading hierarchy** (strategy WHY → architecture WHAT → ground-truth maps → current→vision → build plan).

## Purpose

Anything that **moves, transforms, or reconciles existing state** (rather than building new
machinery) lives here. Think: R2 Bronze snapshots → factory registry, sibling-repo gold → canonical
objects, Postgres atlas backfills, registry integrity repair.

## Layout conventions

- One subfolder (or file) per migration, self-contained.
- Every migration carries a `README.md` stating: source → target, idempotency, dry-run flag,
  rollback, and how to verify the result.
- Prefer `--dry-run` by default; only write state when told.
- Reference the R2 credentials in the gitignored `.r2-env` (never commit secrets).
