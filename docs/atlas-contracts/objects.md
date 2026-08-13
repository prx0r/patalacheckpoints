# Epistemic objects

*Field reference for the typed scholarly objects (`python/patala_core/objects.py`). These are the
Epistemic Core's outputs — Proposition, Commitment, GroundingLink, InferenceApplication, Crux,
ReviewEvent, ReviewProposal, Adjudication.*

## Base scholarly object

Every object carries the universal envelope:

```python
class BaseScholarlyObject(BaseModel):
    object_id: str
    version_id: str
    layer: str
    derived_from: list[str]     # upstream version_ids this was derived from
    source_refs: list[str]      # source version_ids grounding it
    authority: AuthorityVector
    schema_version: str
    # + layer-specific `content` (typed discriminated union)
```

`content` is a **typed discriminated union** — never `dict[str, Any]` (P0 correction #1).

## The objects

### Proposition
```python
class PropositionContent(BaseModel):
    formulation: str
    subject: str | None
    scope: Scope                      # LOCAL_PASSAGE … SYSTEMATIC_RECONSTRUCTION
    modality: Modality                # ASSERTED / POSSIBLE / NECESSARY / …
    temporal_scope: str | None
    explicitness: EXPLICIT | IMPLIED | RECONSTRUCTED
    speaker_ref: str | None
    assumptions: list[str]
    support_scope: Scope
    proposition_review_state: UNREVIEWED | SINGLE_REVIEWED | ADJUDICATED
```
> `proposition_review_state` is a **strict Literal** — education states (`PEDAGOGICALLY_REVIEWED`)
> are rejected (P0 correction #3).

### Commitment
```python
class CommitmentContent(BaseModel):
    proposition_ref: str
    actor_ref: str
    force: ASSERTS | DENIES | PRESUPPOSES | ASSUMES_FOR_ARGUMENT |
           ATTRIBUTES_TO_OPPONENT | QUOTES | RECONSTRUCTED
```
> `ATTRIBUTES_TO_OPPONENT` prevents opponent material being silently laundered into author belief.

### GroundingLink
```python
class GroundingLinkContent(BaseModel):
    from_ref: str; to_ref: str
    relation: TEXTUAL_GROUNDING | LEXICAL_GROUNDING |
              TRANSLATION_DEPENDENCY | SCHOLARLY_SUPPORT
    scope: str
```
> Textual grounding is NOT logical inference. That distinction is absolute.

### InferenceApplication
```python
class InferenceApplicationContent(BaseModel):
    premises: list[str]; conclusion: str
    rule_ref: str | None
    reconstruction_status: EXPLICIT | IMPLICIT | EDITORIAL_RECONSTRUCTION
    evaluator_results: list[str]
```
> Nyāya evaluation is a **result over** this object, not baked into truth.

### Crux
```python
class CruxContent(BaseModel):
    argument_ref: str
    proposition_refs: list[str]
    perturbation: CruxPerturbation
    outcome_before: str; outcome_after: str
```
> A Crux records *what changed → which conclusion changed* (deterministic), not "LLM says this premise
> looks important."

### ReviewEvent
```python
class ReviewEventContent(BaseModel):
    target_version: str
    reviewer: ReviewerIdentity
    decision: ACCEPT | ACCEPT_WITH_QUALIFICATION | DISPUTE |
              PROPOSE_ALTERNATIVE | ABSTAIN | OUT_OF_SCOPE
    scope: str; reasoning: str
    evidence_refs: list[str]
    alternative_ref: str | None
    conflict_of_interest: str | None
```
> **ReviewEvent cannot mutate target.** That is constitutional.

### ReviewProposal
```python
class ReviewProposalContent(BaseModel):
    review_event_ref: str
    target_version: str
    proposed_successor: str
    change_summary: str; evidence_refs: list[str]
```

### Adjudication
```python
class AdjudicationContent(BaseModel):
    target_version: str
    considered_reviews: list[str]
    adjudicator_refs: list[str]
    outcome: ACCEPT_CURRENT | ACCEPT_PROPOSED_SUCCESSOR | REVISE | REMAIN_DISPUTED
    reasoning: str; dissent_refs: list[str]
```
> Keeps disagreement alive — `REMAIN_DISPUTED` is a valid terminal state.

## Example (full object)

```python
from patala_core.objects import PropositionObject
from patala_core.authority import AuthorityVector, GenerationStatus

p = PropositionObject(
    object_id="PTPROP_01J...", version_id="PTPROPV_01J...",
    layer="PROPOSITION",
    content={
        "formulation": "recognition requires a persistent subject",
        "explicitness": "RECONSTRUCTED",
        "support_scope": "SAME_WORK",
    },
    authority=AuthorityVector(generation=GenerationStatus.ENGINEERING_VALIDATED),
)
```
