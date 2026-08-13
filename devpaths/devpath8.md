# DEVPATH 8 — SYNTHESIS CORE (the genuinely-new object)

**Status: ⏳ READY** (after devpath7)
**Source of truth:** `docs/global/agent1atlas.md` §3–6
**My analysis:** `devpaths/agent1atlas-reaction.md`

---

## Objective

Build the one object that exists NOWHERE in the Atlas docs or the technical architecture:
**`ArgumentSynthesis`** — the structured "current best understanding of this debate" that essays,
education, review, and agent answers all consume.

## The objects

```text
ResearchQuestion   what question does the debate answer?
DebateFrame        the positions + their relationship (the frame)
Position           a participant stance (ŚAIVA / BUDDHIST / ...)
ArgumentSynthesis  the parent object that ties question + frame + positions + arguments +
                   relations + cruxes + evidence + open disagreement together
```

`Theme` is a curated/derived grouping, NOT the central object.

## `ArgumentSynthesis` shape (from the directive)

```json
{
  "type": "ARGUMENT_SYNTHESIS",
  "research_question": "RQ-17",
  "debate_frame": "DF-4",
  "positions": ["POS-ŚAIVA", "POS-BUDDHIST"],
  "arguments": ["ARG-1", "ARG-2", "ARG-3", "ARG-4"],
  "relations": [{"from": "ARG-3", "to": "ARG-1", "relation": "ATTACKS"}],
  "cruxes": ["CRUX-7", "CRUX-12"],
  "supported_conclusions": [],
  "open_questions": [],
  "scope_boundaries": [],
  "unresolved_disagreement": []
}
```

## The relation vocabulary (MUST be frozen — my reaction note §4e)

The directive uses `relation: "ATTACKS"` but never defines the vocabulary. devpath8 must freeze:

```text
ATTACKS   SUPPORTS   UNDERPINS   UNDERMINES   REPLIES_TO   RESTRICTS   ...
```

## Non-negotiable discipline

- `ArgumentSynthesis` is NOT a final-truth object. It says "under DebateFrame DF4: Position A has X/Y,
  Position B has objection Z, decisive crux CRUX-12, evidence status ..., review state ..." — never
  `CONCLUSION = TRUE`.
- Build ONE on the strongest gold, not 100.
- `ThemeCandidate` (machine clustering) → human/editorial promotion → `Theme` (via the devpath6
  ReviewEvent/Adjudication path). Never `Louvain cluster 6 = canonical doctrine`.

## Input / Output

- Input: Propositions, Arguments, Attacks, Cruxes, SourceAssertions (my devpath4/5 layers).
- Output: one structured debate object.

## Acceptance

- `ArgumentSynthesis` is a first-class typed object (builds on the devpath7 typed content).
- One real synthesis on the strongest gold argument, with a frozen relation vocabulary.
- Honest: synthesis over GOLD is valid; real-corpus synthesis waits on the ARGMAP NAT gate (devpath3).

## References

- `docs/global/agent1atlas.md` §3–6, §8 (synthesis is the convergence object)
- `devpaths/agent1atlas-reaction.md` (my analysis + the relation-vocabulary gap)
- my devpath4 `proposition_layer.py`, devpath5 `crux_engine.py` (the inputs)
