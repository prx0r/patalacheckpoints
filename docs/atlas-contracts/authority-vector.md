# AuthorityVector — authority without a scalar rank

*Field reference for `python/patala_core/authority.py` — the biggest P0 schema fix.*

**The problem it fixes:** the old shared schema assigned numerical ranks independently inside
`generation`, `evidence`, and `review`, then mapped those numbers back into **one global epistemic
ladder**. That made heterogeneous concepts accidentally equivalent — an engineering status could be
mislabeled as a scholarly status (e.g. `ceiling >= 3`).

**The fix:** authority is a **vector of four independent axes**. There is deliberately NO total order
across them. Eligibility is decided by explicit predicates, never a threshold.

## The four axes

| Axis | Meaning | Values |
|---|---|---|
| `generation` | how the object was produced | `MACHINE_PROPOSED` · `ENGINEERING_VALIDATED` · `EDITORIAL` |
| `evidence` | independent scholarly support | `NONE` · `SCHOLARLY_CORROBORATED` · `DISPUTED` · `CORROBORATION_OPEN` |
| `review` | human review state | `NOT_REVIEWED` · `SINGLE_REVIEWED` · `ADJUDICATED` |
| `publication` | publication / rights posture | `PRIVATE` · `INTERNAL` · `PUBLIC` |

## Canonical JSON

```json
{
  "authority": {
    "generation": "ENGINEERING_VALIDATED",
    "evidence": "SCHOLARLY_CORROBORATED",
    "review": "NOT_REVIEWED",
    "publication": "PUBLIC"
  }
}
```

## Gate predicates (explicit, never `ceiling >= 3`)

```python
vector.eligible_for_publication()   -> bool
vector.eligible_for_scholar_review() -> bool
vector.eligible_for_education()     -> bool
```

Rules of thumb:
- factory can process at `CATALOG_MATCHED`-ish / `MACHINE_PROPOSED`
- a public edition claim needs `EDITION_VERIFIED`
- a scholar-reviewed canonical reading needs `SCHOLAR_CONFIRMED`

## Display badge (a phrase, not a rank)

```python
vector.display_badge()
# "machine-validated · scholarly evidence available · not human-reviewed · public"
```

For UI, derive a human string like the above. Do **not** render "authority: 7/10".
