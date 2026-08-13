# Pāṭala Contracts — Overview

*2026-08-13. OpenAlex-level reference for the Pāṭala epistemic object contracts
(`python/patala_core/`). These are the typed, Pydantic-validated scholarly objects that the Epistemic
Core produces and the Review/Education surfaces consume. They implement the three P0 schema corrections
from `docs/vision/atlas/technical-architecture-v1.md`: typed discriminated content, an AuthorityVector
(no scalar rank), and per-object-type state machines (no universal review ladder).*

> **Schema source of truth:** Pydantic → JSON Schema → TypeScript. The DB schema is Alembic SQL migrations
> (see `docs/atlas-contracts/atlas-database.md`). Do NOT make Drizzle/TypeScript the universal ontology.

---

## Contents

| Doc | What it is |
|---|---|
| **`ids.md`** | The identity model: stable `object_id` vs exact `version_id` |
| **`authority-vector.md`** | The 4-axis authority model + the gate predicates (the biggest P0 fix) |
| **`objects.md`** | The typed epistemic objects (Proposition, Commitment, Argument, Crux, Review, Adjudication…) |
| **`atlas-database.md`** | The Pāṭala Authority Graph Postgres schema (the 22 tables) |
| **`overview.md`** *(this file)* | The conceptual model + how the pieces fit |

---

## The conceptual model

```text
Atlas / Authority Graph      → what exists, which version/witness   (stable identity)
Factory / Compiler           → what can we derive from it?          (SOURCE→T1→L0→…→C1)
Epistemic Core               → what is actually supported?          (Proposition…Review)
```

The **object** is the thing with stable identity across history. The **version** is one exact immutable
formulation. Every review references a **version_id**, never just an object_id.

## The three P0 corrections (enforced here)

1. **Typed content.** Every scholarly object's `content` is a Pydantic discriminated union of typed
   content models — never `dict[str, Any]`.
2. **AuthorityVector, not a scalar rank.** Authority is 4 independent axes (generation / evidence /
   review / publication). There is NO `rank` or `ceiling`. Eligibility is decided by explicit predicates.
3. **Per-type state machines.** A Proposition has its own review state; education states
   (`PEDAGOGICALLY_REVIEWED`) can never apply to a Proposition. `ReviewEvent` cannot mutate its target.

## Quick reference

```python
from patala_core.objects import PropositionObject
from patala_core.authority import AuthorityVector, GenerationStatus

p = PropositionObject(
    object_id="PTPROP_01J...", version_id="PTPROPV_01J...",
    layer="PROPOSITION",
    content={"formulation": "recognition requires a persistent subject"},
    authority=AuthorityVector(generation=GenerationStatus.ENGINEERING_VALIDATED),
)
print(p.authority.eligible_for_publication())   # predicate, not a threshold
print(p.authority.display_badge())              # "machine-validated · not human-reviewed"
```

## Relation to the running factory

The running factory (61 works, live loop) writes versioned objects to the object registry
(`pipeline/object_registry.py`). These `patala_core` contracts are the **typed schema layer** for those
objects — the same objects, now with validated typed content and an honest AuthorityVector. The
compatibility adapter (TIER 3) bridges the legacy registry to these contracts without changing factory
behavior.
