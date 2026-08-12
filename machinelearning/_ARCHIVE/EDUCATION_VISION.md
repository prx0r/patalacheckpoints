# EDUCATION LAYER — the graph-native teaching engine (vision)

*2026-08-12. The educational layer, built on what we have (the learning strategy + concept modules +
the graph) and borrowing the strongest mechanisms from the HXRMXS UNO engine (a graph-native
pedagogical policy engine). The thesis: **the graph doesn't just store scholarship — it selects the
teaching move, and every lesson is a path through the graph, not a paragraph.**

---

## 1. What we already have

- **`docs/LEARNING_STRATEGY.md`** — "research once, distill repeatedly": primary text → essay →
  concept explainer → video → short. The knowledge packet is the durable unit.
- **`docs/content/modules/`** — school modules (trika, spanda, pratyabhijñā, krama, recognition).
- **`app/learning/`** — the Learn layer (foundations, timeline, geography, school index).
- **The graph** — passages + C1 + themes + hub + the source spines. This is the substrate the
  education must derive from (never free-floating).

The gap: education is currently **content modules** (written explainers), not a **graph-native
teaching system** that selects paths through the scholarship.

---

## 2. The borrowed mechanisms (from the geometricengine — transferable)

The HXRMXS engine treats pedagogy as a **graph-owned pathway selection**: learn weights from real
transitions, then infer the next move from the graph — no LLM in the cognition path. The transferable
mechanisms:

### 2.1 Mechanism-shapes (the teaching MOVE, agnostic to content)
A "move" is a structural pattern, not a topic. These are lineage-agnostic — "structural_analogy" is
the same in Epictetus, Abhinava, or a science lesson. The Pāṭala set:
```
structural_analogy   map unknown → familiar, preserving relations (the mirror, the crystal)
contrast             show A vs B to isolate the difference (IPVV vs Tantrāloka)
chain                follow a dependency sequence (the kārikā → Vṛtti → Vivṛti → IPV)
collapse             reduce to the single load-bearing move (the master-key: direction)
threshold            the point where a claim stops being supported (the boundary)
reversal             the turn (recognition-not-attainment; upāya as reversal)
zoom                 resolution change (passage → C1 → theme → work → cross-work)
```
**Borrow:** every educational step is tagged with a mechanism-shape, so the system can *vary the
move* (not just the content) — a lesson re-taught with analogy vs contrast vs chain.

### 2.2 Registers (the depth/intensity dial)
The engine's 24 registers along 6 dimensions (intensity, intimacy, style…) parallel Pāṭala's depth:
```
DEPTH        original → read → guide → study → critical  (the choose-your-depth ladder)
FELT         doctrine → example → felt-experience (camatkāra, the why-it-matters)
SCOPE        single passage → vimarśa → work → tradition
REGISTER     scholarly → beginner → GEN-Z (the projection)
```
**Borrow:** every lesson is parameterized by depth/felt/scope/register, so the SAME knowledge packet
renders at any level — the L2→C1→theme→essay projection made navigable.

### 2.3 The pathway-vector (graph-owned selection)
The engine stores, per learning option, a vector of effectiveness per user cluster. For Pāṭala:
```
each lesson has a pathway_vector[]  (one index per learner-profile / entry-point)
  "start here if you come from vimarśa"   ← the concept you already know
  "start here if you want the felt"        ← the felt register
  "start here if you're a scholar"         ← the depth
```
**Borrow:** the graph *selects the next move* from the learner's entry-point + the relation edges —
not a static course. This is the "guided journey": the graph picks the path (passage → C1 → theme →
parallel → essay) from where you are.

---

## 3. The visionary features (how an AI uses our graph)

### 3.1 Guided journeys (the conceptual-path)
The user enters with a *question* or *known concept*; the graph composes a path:
```
"I want to understand what Abhinavagupta thinks I am"
  → CORE-Q  (what is the subject?)   → passages
  → vimarśa (the felt)               → C1s + themes
  → the master-key (direction)       → the essay
  → the practical (what to do)       → learning
```
This is the "journey" vision — the graph's edges (spines, themes, C1 see_also) ARE the path. The
engine selects it from the learner's entry, not a hand-authored course.

### 3.2 Audio / podcast generation (from the graph, not a transcript)
The learning strategy says derive everything from the knowledge packet. Audio:
```
5-min explainer   ← the passage note
20-min overview   ← the C1 + theme dossier
90-min deep-dive  ← the essay + the argument truth-packets
```
Each is a *narration of the graph path* with the source anchors embedded (citation-preserving
audio: "as the Tantrāloka 1/52 says, [quote]"). Because the path has sequence + terms + passages,
the audio is generated from the structure, not improvised.

### 3.3 Concept journeys + misconception maps (the entry-point dial)
- Enter by concept → the graph shows where it develops (occurrence map, 5 kinds).
- Each concept carries a **misconception → correction → textual evidence** block (the "why people
  get it wrong" layer, from the real-DNA questions).
- The learner's wrong intuition becomes the entry-point; the graph corrects via the text.

### 3.4 The "choose your depth" + media projection (the renderer)
One knowledge packet → any output, via the register dial:
```
ORIGINAL   the Sanskrit
READ       the L2
GUIDE      the plain rendering (GEN-Z-register, but licensed)
STUDY      the C1
CRITICAL   the apparatus
AUDIO      the 5/20/90-min narrations
VIDEO      the argument diagram (the mechanism-shape rendered)
QUIZ       the misconception-test (from the misconception maps)
```
All resolve to the same passages. This is the "one graph, many projections" endgame.

---

## 4. How it links to the system

| Layer | Feeds it |
|---|---|
| passages + C1 | the READ/STUDY + the journey steps |
| themes + hub | the guided-journey paths + the essay library |
| canonical-spines + relations | the related-text rail (already built: `/api/recommend`) |
| argument truth-packets | the deep-dive audio/essay (the PROVED/PLAUSIBLE strength) |
| the questionnaire (real-DNA) | the misconception maps + the felt register |
| `/api/recommend` | the "because you read X, try Y" path-continuation |

---

## 5. The build order (what to add next)

1. **Mechanism-shapes + registers** — tag lessons with a move + a depth register (a `data/corpus/
   pedagogy.ts`): the teaching-move vocabulary over the knowledge packets.
2. **The pathway-vector / journey selector** — `/api/journey?from=<concept-or-question>`: the graph
   composes a path (using spines + themes + C1 see_also + recommend). This is the highest-value
   new feature — it makes the graph *select teaching*.
3. **Audio generator** — a script that narrates a passage/C1/theme path with source anchors
   embedded (the citation-preserving audio). Uses the existing structure; no new research.
4. **Concept journey pages** — extend the concept pages with the occurrence map + the
   misconception→correction→evidence block.
5. **The renderer** — one knowledge packet → READ/GUIDE/STUDY/AUDIO/VIDEO via the register dial.

---

## 6. The bottom line

The education layer should stop being "written explainer modules" and become a **graph-native
teaching engine**: the graph selects the move (mechanism-shape), the level (register), and the path
(journey) from the learner's entry — and every lesson, audio, and video is a *projection of the
evidence graph*, never free-floating. We have the substrate (passages + C1 + themes + hub + the
recommend rail); the missing piece is the **pedagogy layer that rides on it** — the mechanism-shapes,
registers, and the graph-owned journey selector.

The strongest single borrow from the geometricengine is the principle: **no LLM in the cognition
path — the graph owns the move.** For Pāṭala that means: the journey, the mechanism-shape, and the
depth are selected from the graph's structure (spines + themes + relations + C1 see_also), and the
LLM only narrates the already-chosen path with the source anchors embedded.
