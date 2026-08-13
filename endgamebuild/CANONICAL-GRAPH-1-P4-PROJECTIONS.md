# CANONICAL-GRAPH-1 P4 — ON-DEMAND PROJECTIONS (THEME/ESSAY/EDUCATION)

*2026-08-13. The reviewer's P4: do NOT wire Essay/Education into the automatic production loop. The
workers exist but should be ON-DEMAND projections, not automatic consequences of every C1 object.*

---

## THE DISTINCTION

```
FACTORY CORE (automatic, canonical):
    SOURCE → T1 → L0 → ARGMAP → L2 → L200 → C1 → ARGUMENT → SYNTHESIS

PROJECTION JOBS (on-demand, not automatic):
    SYNTHESIS → THEME candidate
    SYNTHESIS → ESSAY
    SYNTHESIS → EDUCATION
```

## WHY

- The essay layer can produce structurally-traceable-but-intellectually-thin prose.
- Education has no meaningful learner validation yet.
- Overnight automatic generation of THEME/ESSAY/EDUCATION would create enormous volumes of mediocre
  downstream objects + more invalidation debt (the audit's concern).

## THEME IS A LATERAL INDEX, NOT A LINEAR DEPENDENCY

The reviewer's correction: Theme is conceptual grouping/indexing, not a required parent in the
epistemic dependency spine. Arguments can span themes; themes can cluster arguments.

```
                  ┌→ ThemeCandidate
C1 / Proposition ─┤
                  └→ Argument
```

Therefore **THEME was REMOVED from the scheduler `LAYER_ORDER`** (it was added earlier in the audit-fix
pass; the reviewer correctly flagged this). It remains a lateral derived index, not a canonical parent.

## ENFORCED

- `LAYER_ORDER = [T1, ARGMAP, L0, L2, L200, C1]` (reverted — THEME not a mandatory layer).
- THEME/ESSAY/EDUCATION workers exist and are wired in `LAYER_HANDLERS` but are invoked on-demand,
  not by the production loop.
- The epistemic crown is `C1 → ARGUMENT → SYNTHESIS` (see P3), then projections on top.
