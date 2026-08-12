# ARG-GOLD REVIEW PROTOCOL (the editorial pass)

*2026-08-12. The golds are `MACHINE_PROPOSED / CANDIDATE` — machine-reconstructed from the C1/L2 and
internally consistent, but **NOT yet independently reviewed**. Before any gold can be promoted to
`SINGLE_EDITOR_GOLD` / `ADJUDICATED_GOLD`, a human reviewer must rule on it. This is the review sheet.

**The governing principle (architectural doctrine):**
> **Validator establishes well-formedness; reviewers establish validity.**
> `validate_gold` proves a fixture is *well-formed* (IDs resolve, enums are valid, no dangling refs).
> It does NOT and cannot prove the propositions are *correct* — that is scholarly review.

## The four questions, per proposition AND per inference

For every node and every inference in a fixture, a reviewer answers:

1. **Is this actually present in the supplied source/context?** (i.e., the C1 + L2 named by the fixture)
2. **If not, is the reconstruction necessary for the argument?** (does the inference break without it?)
3. **Could another competent reader reconstruct it differently?**
4. **What is the narrowest conclusion the evidence licenses?**

Record: `SUPPORTED_BY_SOURCE` / `RECONSTRUCTED_NECESSARY` / `RIVAL_READING_POSSIBLE` /
`UNSUPPORTED` / `ABSTAIN`. A single `UNSUPPORTED` on a required (task_level A) node blocks promotion.

## Task-level reminder

The fixtures now tag each node `task_level`:
- **A_PROPOSITION_EXTRACTION** — explicitly/reconstructably present in the source; this is what an
  extractor must recover.
- **B_ARGUMENT_RECONSTRUCTION** — an implicit warrant that best explains the inference (may be
  `candidate_reconstruction`).
- **C_SYSTEMATIC_INTERPRETATION** — a stronger interpretation supportable only with wider corpus context.

An extractor should be compared mainly to **A**. Nodes tagged B/C are not "missing" if the source input
doesn't contain them.

## Specific rulings required (the open questions)

| Fixture | Ruling needed |
|---|---|
| **ARG-GOLD-003** (reductio, V2-O) | Is the infinite-regress warrant (G3-REG, G3-ABS, G3-INF-RED) genuinely the intended warrant, or our reconstruction? Until a specialist says yes, it stays `candidate_reconstruction` and is NOT a required extraction target. The SAFE GOLD (pratibhā bears order + pratibhā is akrama → support is orderless) is the task_level-A target. |
| **ARG-GOLD-004** (conceptual distinction, V2-H) | Is vimarśa-as-essence TEXTUALLY asserted by the C1 (as `G4-TC2` claims), or inferentially derived? If textual, the current graph (essence not inferred from bare-showing) stands; if not, demote G4-TC2 to task_level B and add an exhaustiveness premise. |
| **ARG-GOLD-005** (interpretive scope, V3-I) | Is this a genuine two-meaning AMBIGUITY, or (as now typed) `INTERPRETIVE_SCOPE` — Reading A locally entailed, Reading B a contextually-supported extension relying on same-work passages (V3-G/H, V2-S)? Ruling decides the fixture's `structure`. |

## After the review

- A reviewer who accepts a fixture's content signs it → `review_state: SINGLE_EDITOR_GOLD` and
  `authoring_method: FOUNDER_REVIEWED` (a founder's own scrutiny is still not *independent* gold).
- A second independent reviewer → `DOUBLE_REVIEWED_GOLD` / `ADJUDICATED_GOLD`.
- Statuses come from review **events**, never from code defaults.

## Status ladder (proposed, for the future)

```
MACHINE_PROPOSED
  → FOUNDER_REVIEWED      (the builder scrutinized it — still not independent)
  → DOMAIN_EDITOR_REVIEWED
  → DOUBLE_REVIEWED
  → ADJUDICATED
```
