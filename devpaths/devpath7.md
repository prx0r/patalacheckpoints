# DEVPATH 7 — CANONICAL GRAPH CONTRACT (the Agent 1 × Atlas convergence point)

**Status: ⏳ READY** (next unblocked after devpath1/4/5/6)
**Source of truth:** `docs/global/agent1atlas.md` + `docs/vision/atlas/technical-architecture-v1.md`
**My analysis:** `devpaths/agent1atlas-reaction.md`

---

## Objective

Freeze the canonical scholarly-object contract so Agent 1 (epistemic contracts) and Atlas (identity +
persistence) snap together. Fix the current DSO debt AND reconcile my devpath4 proposition layer with the
Atlas `PropositionContent`.

## The real scope (not "small")

The directive calls devpath7 "very small," but the actual substance is:

1. **Implement tech-arch-v1 §27** — replace `DerivedScholarlyObject.content: dict[str, Any]` with a
   **Pydantic discriminated union** (typed `PropositionContent`, `ReviewEventContent`, `CruxContent`, …).
2. **Implement tech-arch-v1 §28** — remove the scalar `epistemic_ceiling` as canonical; keep the 4-axis
   `authority` vector, derive only display badges / eligibility gates.
3. **Reconcile my `proposition_layer.py` → Atlas `PropositionContent`** — this is the real work.
   My Proposition has `proposition_text`/`commitment`/`explicitness`/`derived_from`/`grounding`/
   `scholarly_corroboration`; Atlas `PropositionContent` has `formulation`/`subject`/`scope`/`modality`/
   `explicitness`/`speaker_ref`/`assumptions`/`support_scope`. **Pick ONE field shape.**
4. **Freeze the six-object convergence contract** (the directive §14):
   `CanonicalObjectRef · CanonicalVersionRef · ScholarlyObjectEnvelope · AuthorityVector ·
   ObjectDependency · ObjectEvent`.
5. **Reconcile the commitment vocabulary** (exists in 2 places: my COMMITMENTS tuple + tech-arch §30
   `CommitmentContent.force`) — one source of truth (the Atlas contract, since it goes to Postgres).

## The six-object contract (freeze these)

```text
CanonicalObjectRef    object_id + object_type
CanonicalVersionRef   object_id + version_id + schema_name + schema_version + payload_hash
ScholarlyObjectEnvelope  the DSO envelope (id/layer/derived_from/source_refs/authority)
AuthorityVector       generation/evidence/review/publication (never one scalar)
ObjectDependency      consumer_version_id/dependency_version_id/relation/load_bearing/epistemic_role
ObjectEvent           the append-only event (the ledger)
```

## Acceptance

- `DerivedScholarlyObject` uses a Pydantic discriminated union for `content` (no `dict[str, Any]`).
- `authority` is a vector; no scalar `epistemic_ceiling` is canonical (only derived display).
- My `proposition_layer.py` and the Atlas `PropositionContent` use the SAME field shape.
- The six-object contract is frozen and referenced by both lanes.

## Boundary

- devpath7 is the joint Agent-1/Agent-2 convergence point. Atlas owns identity+persistence (Postgres,
  R2, hashes, rights); Agent 1 owns the epistemic content contracts.
- Do NOT broaden the ontology; freeze the minimum and let both lanes proceed.

## References

- `docs/vision/atlas/technical-architecture-v1.md` §17, §27–31 (the already-written spec)
- `docs/global/agent1atlas.md` §11–15 (the boundary + six-object contract)
- `source-evidence/schema/derived_scholarly_object.py` (current, to fix)
- `machinelearning/research/patala_ml/proposition_layer.py` (my devpath4, to reconcile)
