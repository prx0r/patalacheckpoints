# DEVPATH 13 · P1 — CROSS-LANE ATLAS SEMANTIC AUDIT

**Status: ✅ CLOSED (2026-08-13)**
**Directive:** A1-CONTINUE-v2 P1 — "Agent 1 should inspect Agent 2's actual resolver output, not merely its schema."

---

## What was audited

`python/patala_core/atlas/resolver.py` — the Agent 2 producer that emits `SourceResolutionCandidate`
with per-dimension authority evidence + convenience gates.

Audited surface (per the directive):
```
authority vocabulary · evidence provenance · source independence · gate predicates ·
factory_eligible · publication_eligible · scholar_review_eligible · rights handling · exact IDs
```

## Findings (producer-side semantic inflation)

### P1-F1 — `publication_eligible` was NOT rights-aware (SEVERE)
The `_gate(evidence, "publication")` predicate returned `True` whenever `EDITION_IDENTITY` was
`MULTI_SOURCE_MATCHED / COPY_INSPECTED / EDITION_VERIFIED` — it **never consulted `RIGHTS`**.
Reproduced:
```
EDITION_IDENTITY=EDITION_VERIFIED + RIGHTS=UNKNOWN      -> publication=True  (WRONG)
EDITION_IDENTITY=EDITION_VERIFIED + RIGHTS=DISCOVERABLE  -> publication=True  (WRONG)
```
This contradicts the natural-benchmark expectation (nat-022/nat-023/nat-038) and the authority-
inflation law: a searchable-only or rights-unknown source must NEVER open publication.

### P1-F2 — `factory_eligible` keyed on WORK_IDENTITY, not a usable edition
`factory` returned `True` for `WORK_IDENTITY in (CATALOG_MATCHED, MULTI_SOURCE_MATCHED)` even when the
edition was only a weak candidate and rights were unknown. The factory consumes an EDITION for
translation; a high work identity alone is not a usable translation source.

### P1-F3 — single-ladder vocabulary across heterogeneous dimensions (structural)
One `LADDER` (UNKNOWN…SCHOLAR_CONFIRMED) is shared by WORK_IDENTITY, EDITION_IDENTITY, RIGHTS, etc.
This permits nonsense relations (e.g. `SCHOLAR_CONFIRMED` on RIGHTS, `EDITION_VERIFIED` on
WORK_IDENTITY) that the honest per-dimension ladders in `source_authority.py` would reject. The
natural benchmark already uses per-dimension ladders; the resolver should too.

## Fix applied

`_gate` rewritten to be **rights-aware and dimension-consistent**:
- `publication`: requires `RIGHTS in (REDISTRIBUTABLE, OPEN_LICENSE)` **AND** a copy-inspected/verified edition.
- `factory`: requires a usable edition (COPY_INSPECTED/EDITION_VERIFIED) **AND** processing rights
  (never rights-UNKNOWN/DISCOVERABLE).
- `scholar`: requires a positively identified work (review does not require publication rights).

Verified: `RIGHTS=UNKNOWN → publication=False, factory=False`; `REDISTRIBUTABLE/OPEN_LICENSE + verified
edition → publication=True`; `PROCESSING_ALLOWED + verified edition → factory=True`.

Regression tests added to `python/patala_core/atlas/test_resolver.py` (P1 audit block) — all pass.
The natural-benchmark expectations (nat-022/023/038/039/045/046) are now consistent with the producer.

## Deliverables
- Resolver gate fix: `python/patala_core/atlas/resolver.py` (`_gate`)
- Regression tests: `python/patala_core/atlas/test_resolver.py` (P1 audit block)

**Hand-off to Agent 2:** adopt the rights-aware `_gate` semantics + per-dimension ladders so producer
and evaluator agree. Re-run the resolver test suite before any further authority promotion.
