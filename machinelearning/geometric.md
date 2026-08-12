# GEOMETRIC — ideas borrowed from the HXRMXS/TPN engine (gamechangers for Pāṭala)

*2026-08-12. A deep read of the geometricengine (the UNO/TPN graph-native pedagogical engine) —
metaunoguide, TPN_FULL_SPEC, mechanisms, registers, devuno. The three real gamechangers for Pāṭala
are: (1) the **metacognitive `my_thoughts` layer**, (2) the **weighted transition graph as the move
selector** (no LLM in the decision path), and (3) the **hyperedge incidence graph**. Each is mapped
to what Pāṭala already has and what to build.*

---

## 1. THE THREE GAMECHANGERS

### 1.1 The metacognitive layer (`my_thoughts`) — the biggest borrow

The UNO data has a field `my_thoughts` — the teacher-model's **internal narrator** watching itself
teach. Most fields say *what happened*; `my_thoughts` says *why the system thinks it's happening*.
It parses into five sub-signals:

```txt
1. State inference   why do I think the learner is in this state?
2. Move rationale    why is this the right move now?
3. Trap model        what failure mode am I avoiding?
4. Prediction        what do I expect the learner to do next?
5. Watch signal      what will I look for in the next turn?
```

**The meta-point:** the visible fields train `input → label` (a classifier). `my_thoughts` trains
`input → reasoned policy update` (an internal analyst model) — not just what to do, but *why*, *what
to expect*, and *what to watch for next*. That is a metacognitive engine, not a classifier.

**Adapt to Pāṭala — the reading/watching analyst.** Before a journey/lesson/audio step, the system
produces a `my_thoughts`-style block:

```txt
Current hypothesis:  the reader came from the memory-theme (V2-A) and is comparing it to the
                     reflection-theme (V2-C) — they may conflate memory with the recognizer.
Best move:           route to the C1 that distinguishes them, not the passage that blends them.
Trap:                don't present the master-key (direction) yet — they haven't felt the split.
Predict:             they will ask how the "I" persists across time.
Watch:               do they move from "I remember" to "the remembering IS the Lord's power"?
```

Every educational stop carries this internal analyst — so the system reasons *about the reader's
state*, not just serves content. This is the "AI tutor with an epistemic gearbox" made concrete:
the graph selects the move; the metacognitive layer explains, predicts, and watches.

**Build:** a `data/corpus/analyst.ts` (or a `MetaThought` per journey stop) — the five-field block,
linked to the passage/theme. The LLM narrates; the analyst decides.

### 1.2 The weighted transition graph as the move selector (no LLM in the decision path)

The engine learns `P(B|A,U,C)` — the probability that intervention B works given prior A, user
profile U, and context C — as **weighted edges on a graph**. Inference queries the weights and
selects the move; no LLM in the cognition path. The LLM only composes the response after the graph
chose the move.

**Adapt to Pāṭala — the journey as a weighted graph, not a hand-authored course.**

The Pāṭala graph already has the *structure* (spines, themes, C1 see_also, relations, the recommend
rail, the journey selector built this session). The geometric step is to **weight the edges by
effectiveness**:

```txt
e = { weight: w(A→B | learner_profile, depth), observations: n, register, mechanism_shape }
```

- A = the current stop (passage/C1/theme)
- B = the next stop
- weight = learned "this next move helps this kind of learner at this depth"
- mechanism_shape = the teaching move (analogy/contrast/chain/reversal/zoom)

So "which passage next?" is answered by the **weighted graph**, and the LLM narrates the chosen
path. This is the "guided journey" made learnable: the graph owns the move; the LLM owns the voice.

**Build:** extend `data/corpus/journey.ts` + the recommend rail with a `weight`/`pathway_vector`
field per edge (one index per learner-profile / depth / register). The ML agent's Q1–Q3 (benchmark +
retrieval) can later *learn* these weights from the PUSHING sessions + the comparative matrix — the
transition data Pāṭala already has.

### 1.3 The hyperedge incidence graph (higher-order relations)

The engine builds `mythought_incidences` (3062 typed relationships) over `mythought_hyperedges`
(201 pedagogy blocks) — a **hyperedge incidence graph**, where each teaching block connects many
entities (state + function + mechanism + register + prediction + watch). This is the same higher-order
insight as the `TranslationDecision` n-ary object already in Pāṭala's graph.

**Adapt:** the journey/lesson is a hyperedge — `(passage, C1, theme, mechanism_shape, register,
prediction, watch)`. It's already partly true (the C1 + theme + passage are linked); the geometric
step is to make the *lesson* itself a first-class n-ary node on the hub (like the argument
truth-packet), so it resolves to all its evidence.

---

## 2. THE GEOMETRIC VOCABULARY (mechanism-shapes for teaching)

The engine's mechanism_shapes are content-agnostic teaching moves. The Pāṭala set, mapped to its
own doctrines:

```
structural_analogy   unknown → familiar, preserving relations (the mirror, the crystal, the seed)
contrast             IPVV vs Tantrāloka / memory vs recognition (isolate the difference)
chain                follow a dependency (kārikā → Vṛtti → Vivṛti → IPV → the essay)
collapse             reduce to one load-bearing move (the master-key: DIRECTION)
reversal             the turn (recognition-not-attainment; upāya as reversal; the yogin's I)
threshold            the boundary where a claim stops being supported (the honest limit)
zoom                 resolution change (passage → C1 → theme → work → cross-work)
reframe              the felt register (camatkāra — not just the doctrine, the why-it-matters)
```

Each lesson/journey-step carries a mechanism_shape + a register (depth/felt/scope). The graph
selects both. This is the "move, not just content" idea — a lesson re-taught with analogy vs
contrast vs chain is a different mechanism even if the content is identical.

---

## 3. THE REGISTER SET (the depth dial)

The engine's 24 registers along 6 dimensions. For Pāṭala, the registers ARE the choose-your-depth
ladder + the felt:

```
DIMENSION   DEPTH        original → read → guide → study → critical
DIMENSION   FELT         doctrine → example → felt (camatkāra — the savor)
DIMENSION   SCOPE        single passage → vimarśa → work → tradition → cross-tradition
DIMENSION   REGISTER     scholarly → beginner → GEN-Z (the projection register)
DIMENSION   MOVE         the mechanism_shape (analogy/contrast/chain/...)
DIMENSION   ENTRY        by concept / by question / by passage / by felt
```

Every knowledge packet renders at any register. This is the "one graph, many projections" made
parameterized — the renderer dial.

---

## 4. THE META-PRINCIPLE (the real gamechanger)

> **No LLM in the cognition path. The graph owns the move; the metacognitive layer explains it;
> the LLM only narrates the already-chosen path with the source anchors embedded.**

For Pāṭala this is the difference between "an AI that generates a lesson" and "a scholarly system
that selects the teaching move from its evidence graph, reasons about the reader's state, and then
speaks." The journey (built), the recommend rail (built), and the argument truth-packets (spec'd)
give the structure; the geometric additions are the **analyst layer** (§1.1) and the **edge weights**
(§1.2).

---

## 5. WHAT TO BUILD NEXT (in order)

1. **The analyst/metacognitive layer** (`data/corpus/analyst.ts` + a `MetaThought` on each journey
   stop): the five-field block (hypothesis / best-move / trap / predict / watch) that the system
   produces before narrating. The highest-value gamechanger — it turns the education layer from
   content-serving into reasoning.
2. **Edge weights / pathway-vectors** on the journey + recommend rail: `weight` per (learner-profile,
   depth, register), so the graph *selects* the move. The ML agent can learn these later from the
   PUSHING sessions + comparative matrix.
3. **Mechanism-shapes + registers** as a `data/corpus/pedagogy.ts`: the teaching-move vocabulary
   (analogy/contrast/chain/...) + the register dial, so lessons are tagged and re-renderable.
4. **The lesson as a hyperedge node** on the hub (like the argument truth-packet): a lesson resolves
   to its passage + C1 + theme + mechanism + register + watch-signal.

---

## 6. BOTTOM LINE

The geometricengine's gamechangers are not the tech stack (LangGraph/Qdrant) — they're three ideas:
**a metacognitive layer that reasons about the learner**, **a weighted graph that owns the move**,
and **the hyperedge view of a lesson**. Pāṭala already has the substrate (passages + C1 + themes +
hub + journey + recommend rail). The borrow is the *reasoning layer*: make the system watch itself
teach, select the move from the weighted graph, and explain why — so the education layer becomes a
genuine graph-native pedagogical engine, not a course renderer.
