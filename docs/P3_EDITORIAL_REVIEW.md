# P3 lexical-gold editorial review

## Status

**0/21 fixtures promoted to `SINGLE_EDITOR_GOLD`.**

This is intentional. The current file is a good machine-draft *candidate set*, but it does not contain enough independent evidence to support editorial adjudication.

## Why

Most `local_context` fields are merely the pre-existing English literal gloss. That makes promotion circular: the proposed lexical sense is being judged from the translation that already embodies it.

For a real lexical-sense gold fixture, add at minimum:

- immutable `passage_id`;
- exact `source_span_id`;
- Sanskrit token and full Sanskrit clause;
- 1–3 surrounding Sanskrit clauses where needed;
- L2 translation context;
- candidate senses generated independently of the gold label;
- same-work parallels;
- dictionary / lexical source refs where relevant;
- optional commentary/scholarship refs;
- reviewer rationale;
- explicit `NO_UNIQUE_SENSE` when context underdetermines the choice.

## Specific red flags in v0

- `tattva` at `chunkV2-A-caturtho-vimarsa-aham:L568` is duplicated with incompatible preferred senses (`reality` and `principle`) while the visible context is only `that`.
- `vimarśa` at `chunkV2-A...:L878` appears once with preferred `rehearsal/reconsideration` and once as NO_UNIQUE, again without enough source context to adjudicate the difference.
- `māyā` at the same V3-K occurrence appears both preferred (`māyā-power`) and NO_UNIQUE.
- `krama` at the same V2-M occurrence appears both preferred (`order`) and NO_UNIQUE.
- Several technical terms (`saṃvid`, `prakāśa`, `pratibhā`, `svātantrya`) cannot be responsibly gold-labelled from a one-token English gloss.

These duplicate pairs are potentially valuable **adversarial/abstention tests** after human review. They should not be hidden or deleted; they should be re-authored with adequate context.

## Proposed review states

Keep all current entries:
`MACHINE_DRAFT`

After context enrichment:
`SINGLE_EDITOR_GOLD`

After independent second review:
`DOUBLE_REVIEWED_GOLD`

After disagreement resolution:
`ADJUDICATED_GOLD`
