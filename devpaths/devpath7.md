# DEVPATH 7 — CANONICAL GRAPH CONTRACT (the Agent 1 × Atlas convergence point)

**Status: ✅ CLOSED (2026-08-13)**
**Commit:** `3a10ed1`
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

## Work completed

`source-evidence/schema/typed_scholarly_object.py` (new):
- **§27 fix** — content is a Pydantic **discriminated union** (`PropositionContent`, `CommitmentContent`,
  `GroundingLinkContent`, `InferenceApplicationContent`, `CruxContent`, `ReviewEventContent`,
  `ReviewProposalContent`, `AdjudicationContent`), not `dict[str, Any]`. Object union
  (`PropositionObject`/`CruxObject`/`ReviewEventObject`/`CommitmentObject`) discriminates by `layer`.
- **§28 fix** — `authority` is a VECTOR (generation/evidence/review/publication) with only derived
  `display_badge()` + eligibility predicates; no scalar ceiling.
- **§33** — `CruxContent` records PERTURBATION (what changed → which conclusion), not "LLM says important".
- **§34** — `ReviewEventContent` is a typed content record (evidence, never mutation).
- The **six-object convergence contract**: `CanonicalObjectRef`, `CanonicalVersionRef`,
  `BaseScholarlyObject` (envelope), `AuthorityVector`, `ObjectDependency`, `ObjectEvent` (hashed).

`machinelearning/research/patala_ml/proposition_layer.py` (reconciled):
- Added `Proposition.to_typed()` → typed `PropositionObject`/`PropositionContent` (Atlas field shape:
  formulation/subject/scope/modality/explicitness/speaker_ref/support_scope) with vector authority.
- Backward-compatible `to_dso()`/`emit()` kept.

`source-evidence/schema/test_typed_scholarly_object.py` (new): 26 checks, all pass.

## Acceptance / verification

| Check | Result |
|---|---|
| `test_typed_scholarly_object.py` | 26/26 PASS |
| `test_proposition_layer.py` (reconciled) | PASS |
| `test_crux_engine.py` (dependent) | PASS |
| full regression (6 suites) | all PASS |

## Honest note (git hygiene)

The devpath7 commit `3a10ed1` also swept in pre-existing `apps/web/*` (the frontend PoC) and
`docs/atlas-contracts/frontend-architecture.md` that were sitting untracked in the working tree. These are
now pushed; rewriting would need a force-push (avoided per discipline). They are valid tracked content
(the frontend law + a working PoC). A duplicate `docs/global/frontend-architecture.md` (my earlier draft)
was removed — the canonical frontend law lives in `docs/atlas-contracts/frontend-architecture.md`.

## Boundary

- This module defines the EPISTEMIC contracts (what a Proposition/Crux/ReviewEvent IS). The Atlas owns
  persistence (Postgres/R2/events). The typed content validates here; the Atlas stores
  `schema_name`/`schema_version`/validated payload.
- devpath7 is the last schema-unification task. **devpath8 (synthesis) can now build on a clean typed
  contract.**

## Exit → next

**devpath8 (SYNTHESIS CORE)**: `ResearchQuestion` / `DebateFrame` / `Position` / `ArgumentSynthesis` —
the convergence object. See `devpaths/devpath8.md`.
