# PĀṬALA EDUCATION — Cross-Lane Synthesis (imported 2026-08-13)

*This is the consolidated, canonical statement of Pāṭala Education, synthesized from five imported
design documents (the education dialogue series + the GlossLM expansion doc). It is a **product/vision
lens** — it points DOWN to the architecture (`PATALA-GLOBAL-ARCHITECTURE.md`) and the scholarly kernel,
and does not independently describe implementation.*

*Sources imported (from R2 `sanskritree/`): `educationn`, `education2`, `educationmain`,
`educationglobal`, `greeek`.*

---

## 1. THE ONE-LINE DEFINITION

> **Pāṭala Education is an intelligent tutoring system over the epistemic graph, where the learner
> learns by manipulating the same propositions, evidence, interpretations, and dependencies that
> scholars use to represent the tradition.**

**Not** "Brilliant for Tantra." **Not** "courses about Tantra." Education is a **projection** of the
scholarly graph, not a separate knowledge base.

The defining concept:

> **Progressive epistemic zoom — any explanation can be expanded downward through its reasoning and
> evidence until the learner reaches the primary source.**

---

## 2. THE ARCHITECTURE (education as a compiled projection)

```text
                         SCHOLARLY CORE
                    SOURCE → T1 → L0 → ARGMAP → L2 → L200 → C1
                                      │
                               Proposition / Argument
                                      │
                              LearningClaim IR
                                      │
                            Interaction Compiler
                                      │
                     LearnerResponse / MasteryEvidence
                                      │
                               LearnerState
                                  ↙       ↘
                                BKT       FSRS
                                  \       /
                             Pedagogical Policy
                                      │
                               next interaction
```

The **design law** (must be enforced technically):

> **Education is a projection of Pāṭala objects, not a separate knowledge base.**

Every educational object resolves DOWNWARD to canonical scholarly objects. Nothing is invented for
education that doesn't already exist (or isn't derived from) the graph.

---

## 3. THE CANONICAL EDUCATION OBJECTS (the "native layer")

These are the four objects that define the layer. FSRS/BKT/PostHog consume them — they do NOT define them.

### `LearningClaim`
```json
{
  "learning_claim_id": "",
  "derived_from": [],
  "content": "",
  "claim_type": "",
  "difficulty": "",
  "prerequisites": [],
  "source_refs": [],
  "epistemic_ceiling": ""
}
```
*Example: "The learner can distinguish an author's own commitment from an objection the author is
reporting."*

### `LearningSkill`
```json
{
  "skill_id": "",
  "type": "TERM_DISCRIMINATION | SPEAKER_ATTRIBUTION | COMMITMENT_ATTRIBUTION |
           SCOPE_DISCRIMINATION | WARRANT_RECONSTRUCTION | DEFEATER_RECOGNITION |
           CRUX_IDENTIFICATION | SOURCE_GROUNDING"
}
```

### `LearningInteraction`
```json
{
  "interaction_id": "",
  "targets": [],
  "derived_from": [],
  "interaction_type": "",
  "prompt_state": "",
  "response_space": "",
  "diagnostic_map": "",
  "correct_state": "",
  "hints": [],
  "source_refs": [],
  "review_state": ""
}
```

### `MasteryEvidence`
```json
{
  "learner": "",
  "skill_ref": "",
  "learning_claim_ref": "",
  "interaction_ref": "",
  "difficulty": "",
  "response": "",
  "correctness": "",
  "hint_level": "",
  "transfer_status": "",
  "timestamp": ""
}
```

---

## 4. THE INTERACTION VOCABULARY (start small)

The document proposes a large primitive vocabulary. **Start with six:**

```text
Choice
SpanSelect
SpeakerClassify
PremiseAttach
ArgumentAssemble
PremiseRetract
```

Those prove Pāṭala teaches **structure** (not quizzes). Then add:

```text
TermSenseChoose
SourceGround
CruxFind
TranslationRepair
```

---

## 5. THE THREE (FOUR) EDUCATIONAL MODES

```text
DISCOVER  5–10 min, no prereqs, one amazing question, aha-driven    (Brilliant-like)
LEARN     adaptive, learner-state driven, FSRS, prerequisite paths  (ITS)
PRACTICE  learner-model driven demonstration                        (separate from LEARN)
STUDY     primary text, Sanskrit, apparatus, arguments, scholarship (source-grounding)
```

**They are NOT three content libraries.** Same graph, different depth. (The document elevates PRACTICE
to a fourth mode.)

---

## 6. THE INTERACTION COMPILER + THE GOLD DOCTRINE

```python
compile_interactions(
    scholarly_object=ARG_002,
    targets=["premise_identification", "warrant_reconstruction", "crux_detection"],
    learner_level="novice",
)
```

Returns an ordered `LearningPacket` (LearningClaims, prerequisite skills, misconception candidates,
6–10 interaction specs, correct interpretations, diagnostic distractors, source refs, progression
order, epistemic ceiling).

**The anti-theatre ladder applies to education content too:**
```text
GENERATED → STRUCTURALLY_VALID → SUBJECT_REVIEWED → PEDAGOGICALLY_REVIEWED
→ PILOTED → MEASURED → VALIDATED
```
**Do NOT autogenerate 10,000 lessons.** Build **20 gold learning experiences** first; then build the
compiler machinery from what the golds force. Same doctrine as Argument IR: **gold forces ontology.**

---

## 7. THE KEY INSIGHT — "wrong answer → known epistemic neighbor"

The education moat is NOT adaptive scheduling. It's this:

```text
wrong answer
    ↓
known epistemic neighbor
```
instead of:
```text
LLM invents distractor
```

A wrong answer maps back into Pāṭala's own failure taxonomy:
- rival proposition · wrong speaker · scope inflation · wrong technical sense · defeated inference ·
  false contradiction · omitted qualifier · alternative DebateFrame

**Learner mistakes become meaningful because they resolve back into the scholarly graph.**

---

## 8. THE FLYWHEEL + MULTI-LAYER MOATS

```text
SCHOLARSHIP → epistemic graph → learning claims → interactions → learners
→ response evidence → misconception data → better pedagogy → hard distinctions
→ machine benchmarks → scholar questions → corrections → better epistemic graph
```

Then MEDIA renders from the same graph + interactions, and Sanskrit speech/pronunciation data becomes
another unique asset.

**Four compounding moats:**
1. **Scholarly** — sources + provenance + expert correction
2. **Machine** — benchmarks + adversarial fixtures
3. **Pedagogical** — diagnostic interactions + misconception graph
4. **Language** — Sanskrit alignment + pronunciation + speech + historical term-sense

---

## 9. SCHOLAR CORRECTIONS IMPROVE EDUCATION AUTOMATICALLY (the killer property)

```text
Scholar reviews Proposition P → ReviewEvent fires → "too strong, narrower condition"
→ Argument changes → Synthesis changes → KnowledgePacket stale → beginner explanation flagged
→ quiz depending on old claim flagged
```

Education is a **compiled projection of current scholarly state** — when scholarship changes, you know
exactly which educational explanations need reconsideration. (This is the executable-corrections
engine repurposed for education.)

---

## 10. THE "COUNTERFACTUAL / CRUX" PRIMITIVE — the one feature to fund

Instead of "which answer is correct," ask: **"what changes if this assumption is false?"**

```text
Learner clicks premise P2: RETRACT
→ graph recomputes → C loses support
→ "P2 is therefore load-bearing."
```

The learner **experiences** what a crux is. This is Pāṭala's dependency engine as an **interactive
philosophical simulator** — the humanities' answer to "dragging the triangle."

---

## 11. THE FIRST PROTOTYPE (do NOT build the platform yet)

Build **ONE argument** (ARG-GOLD-002, or whichever Agent-1 gold is currently strongest) into a
10–15 minute Brilliant-quality interactive:

```text
1  strange opening puzzle           7  classify whether rival answers same question
2  choose what recognition requires 8  retract premise → watch argument change
3  expose temporal problem          9  identify crux
4  drag missing premise             10 descend into translation
5  reveal historical position       11 descend into Sanskrit
6  introduce rival Buddhist solution 12 source-level challenge
13 unseen transfer problem          14 "what you demonstrated" summary screen
```

If this is excellent → the educational thesis is proven. If boring → building an LMS would've been
wasted. **Prove manipulating the epistemic structures is compelling BEFORE building the platform.**

---

## 12. MULTILINGUAL EXPANSION (GlossLM) — the language-agnostic kernel

Separate concern (`greeek`): GlossLM validates that **T1 can be a language-agnostic intermediate
layer** rather than a Sanskrit-only hack. The portable boundary:

> **Every language-specific compiler must emit a standardized semantic/philological intermediate
> representation.**

```text
                UNIVERSAL PĀṬALA CORE
       ┌───────────────┼───────────────┐
  SanskritCompiler  GreekCompiler  PaliCompiler
       │               │               │
       ▼               ▼               ▼
      T1              T1              T1
       └───────────────┼───────────────┘
                        ▼
                       L0 → ARGMAP → L2 → L200 → C1 → epistemic graph
```

L0 is the portable layer. Do NOT overgeneralize T1 (don't make `vibhakti`/`karaka` mandatory universal
fields; use `morph_features`). **Sanskrit/Tantra stays the proving ground**; add Pāli or Greek as the
ONE second compiler only after the Sanskrit kernel is proven.

---

## 13. THE TECH STACK (reuse-first)

| Concern | Choice |
|---|---|
| Web | Next.js / React / TypeScript |
| Interactive graph | Cytoscape.js |
| Editor | Tiptap (headless ProseMirror) |
| Collaboration | Yjs + Hocuspocus |
| Learner model | simple BKT (inspired by OATutor) |
| Memory | FSRS-6 |
| AI tutor | provider-independent LLM adapter + typed tutor actions |
| Sanskrit morphology | Vidyut + Heritage witnesses (ensemble, disagreement = feature) |
| Sanskrit ASR | IndicConformer (baseline) |
| Sanskrit TTS | research/fine-tune track (do NOT pretend generic Hindi TTS solves it) |
| Analytics | PostHog |
| Experimentation | PostHog → GrowthBook later |
| Benchmarks | Inspect AI |
| Export | xAPI/LTI/QTI adapters later (never canonical) |
| Provenance | existing Pāṭala graph |

**What NOT to build:** no custom rich-text editor, no custom spaced-repetition, no custom analytics, no
generic RAG, no LMS, no 100k-lesson content farm. Put engineering into: Epistemic Interaction IR,
LearningClaim, diagnostic distractors, misconception graph, MasteryEvidence, argument simulator,
progressive epistemic zoom, education compiler, Sanskrit interactive reader, pronunciation layer,
scholar→education correction propagation.

---

## 14. AGENT RESPONSIBILITY (keep the lanes clean)

- **Agent 2** = produce + maintain canonical scholarly objects (NOT education).
- **Agent 1** = prove/evaluate scholarly AND educational correctness.
- **Agent 3** (Hermes) = route work, not build pedagogy.
- **Agent 4 (future)** = Education Compiler, ONLY after a manual prototype proves useful.
  Authority: Agent4 proposes → Agent1 verifies epistemic fidelity → pedagogy reviewer validates teaching
  quality.

---

## 15. THE CARRY-FORWARD

**Education is a first-class projection of the scholarly factory, defined by four native objects
(LearningClaim, LearningSkill, LearningInteraction, MasteryEvidence) + the interaction compiler + the
progressive-epistemic-zoom law; the correct next move is NOT a platform but ONE gold argument
(ARG-GOLD-002) compiled into a Brilliant-quality interactive to prove the educational thesis, with the
Sanskrit interactive reader before Sanskrit speech, and the multilingual/GlossLM expansion deferred
until the Sanskrit kernel is proven.**
