# SEMANTIC COMMENSURABILITY — DebateFrame + SemanticAlignment (the anti-fake-contradiction layer)

*2026-08-12. The deepest problem the viruddha case exposed: **semantic commensurability.** Before you
can say "Argument A defeats Argument B," you must know A and B are talking about the same proposition-
space. In Sanskrit philosophy that is often exactly what is contested. Two authors both use "cognition"
but mean: momentary representational event / self-manifesting awareness / epistemically valid awareness /
reflexive apprehension. Treating all four as one node manufactures contradictions that aren't real.*

---

## 0. The principle

> **The real primitive isn't argument. It's argument-under-a-frame. And the real primitive for comparison
> isn't contradiction — it's relation after semantic alignment.**

The first step in argument comparison is: **WHAT ARE THEY ARGUING ABOUT?** Not "detect the fallacy."

---

## 1. The three relation types (instead of one "contradiction")

Two claims may be:

1. **Genuine contradiction** — same subject, same predicate, same scope, same sense
   `CONTRADICTS` (A: cognition is momentary / B: cognition is not momentary)

2. **Apparent contradiction due to conceptual divergence** — A's "cognition" ≠ B's "cognition"
   `CONCEPTUAL_MISMATCH` or `DISPUTED_TERM_SENSE`

3. **Different questions** — A: what makes cognition epistemically valid? / B: what makes it manifest?
   `QUESTION_MISMATCH`

All three are useful scholarly outcomes. "They're talking past each other" is a first-class result, not
a failure.

---

## 2. The canonical objects

### DebateFrame (the contention)
```ts
interface DebateFrame {
  id: string;
  question: string;
  object_of_dispute: string;
  concept_refs: Ref[];
  participant_positions: { participant: string; proposition_ids: PropositionId[] }[];
  shared_ground: PropositionId[];
  disputed_ground: PropositionId[];
  semantic_alignments: SemanticAlignment[];
  status: "MACHINE_PROPOSED" | "EDITOR_REVIEWED" | "ACCEPTED";
}
```
Example:
```
QUESTION:            What accounts for continuity across cognitions?
SHARED TARGET:       continuity of experience / recognition
POSITION A:          requires a persisting knower
POSITION B:          can be explained through causal succession of momentary cognitions
CONTESTED ASSUMPTION: whether cognition is intrinsically self-revealing
TERM WARNING:        "cognition" is not yet assumed extensionally identical across positions
```

### SemanticAlignment (the term mapping)
```ts
interface SemanticAlignment {
  left_term: Ref; right_term: Ref;
  relation: "SAME_SENSE" | "OVERLAPPING" | "NARROWER" | "BROADER" |
            "ANALOGOUS" | "DISPUTED" | "DIFFERENT";
  context: Ref[]; rationale: string;
  status: "MACHINE_PROPOSED" | "EDITOR_REVIEWED" | "ACCEPTED";
}
```

### The explanatory level (a level mismatch is a warning before contradiction)
```
level: "PHENOMENOLOGICAL" | "EPISTEMIC" | "SEMANTIC" | "CAUSAL" | "METAPHYSICAL" | "METHODOLOGICAL"
```
Same term + different level → warning before contradiction inference.

---

## 3. The decision ladder (replaces naive contradiction)

```
not semantically commensurable         → NOT_COMPARABLE
different scope                        → QUALIFICATION_OR_SCOPE_MISMATCH
H supports ¬S (after alignment)        → VIRUDDHA_CANDIDATE
```
**viruddha requires the frame FIRST:** same DebateFrame? same target proposition? semantic alignment
adequate? scope compatible? Only then test "does H support ¬S?" This massively reduces fake contradictions.

---

## 4. The architecture (not "A vs B → contradiction classifier")

```
PASSAGES
  ↓
PROPOSITIONS
  ↓
DEBATE FRAME
  ↓
SEMANTIC ALIGNMENT
  ↓
POSITIONS
  ↓
INFERENCES
  ↓
CONFLICT / QUALIFICATION / NON-COMMENSURABILITY
```

---

## 5. The scholar payoff (this is a real feature, not just plumbing)

A scholar asks "where exactly do Utpaladeva and Dharmakīrti disagree?" Pāṭala returns:
```
SHARED QUESTION · SHARED ASSUMPTIONS · TERM ALIGNMENTS · POSITION A · POSITION B ·
TRUE POINT OF DIVERGENCE · APPARENT DISAGREEMENTS THAT DISAPPEAR once terminology is aligned
```
And adversarial review becomes genuinely useful: "Abhinavagupta rejects the Buddhist theory of
cognition" → *possible overstatement: the two use 'cognition' at different levels of analysis
(Buddhist: momentary cognitive events; Abhinava: the condition for their manifestation) — relation
PARTIAL OVERLAP / DISPUTED FRAME. Recommended narrower claim: ...*

---

## 6. Where it plugs in

- **viruddha** (the frozen-gate miss) becomes a graph operation over DebateFrames, not a keyword hack.
- **counterevidence** / **adversarial review** / **cross-tradition argument comparison** all require
  DebateFrame + SemanticAlignment when comparing distinct positions.
- It prevents the fake contradictions that would otherwise pollute the argument graph, theme clustering,
  and the comparative matrix.

**Status: MACHINE_PROPOSED design.** The objects are specified, not yet built. They become real at CP4
alongside Argument Gold — which is exactly the prerequisite viruddha exposed.

> **Vision link:** `ARGUMENT-GOLD-VISION.md` — the canonical framing of how Argument Gold + DebateFrame/SemanticAlignment unblock the gate (viruddha becomes a graph op). Execution: `handover/agent-1-ml/NEXT-STEPS.md`.
