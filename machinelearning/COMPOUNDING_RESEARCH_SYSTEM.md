# PĀṬALA — THE COMPOUNDING RESEARCH SYSTEM (organization + vision)

*2026-08-12. How every primary source becomes a tracked hub of ALL its derived outputs — essays,
pushing-enquiries, logical arguments, learning — so the project compounds instead of scattering.
Three ideas unify: (1) the **source-centric hub** model, (2) the **PUSHING method** (mechanical
deep-dive), (3) **logical arguments as the gold** that ties the truth engine to the corpus.*

---

## 1. The core organizing idea — every source is a HUB, not a file

Today the outputs of a text are scattered: essays in `research-library/`, translations in
`sanskritree/`, the truth-engine formalizations in `truth/`, learning in `patala/`. The organizing
fix: **every primary source is a tracked hub of all its derived outputs**, and the hub is tied to the
bibliography + API.

```
PRIMARY SOURCE  (the canonical text, e.g. IPVV / Tantrāloka / IPK)
  ├─ translation stack   (T1/L0/L2/L200/C1)   — the reading
  ├─ PUSHING enquiry     (the deep-dive Q&A)   — the hard questions
  ├─ ESSAYS             (interpretive, comparative)
  ├─ LOGICAL ARGUMENTS  (formal, the gold)     — proofs / decomposition
  ├─ LEARNING           (lessons, guides)
  └─ all tied by the passage IDs + the source registry
```

This is **agnostic** — the same hub shape works for IPVV, Tantrāloka, IPK, Kubjikā, a Buddhist text,
a ritual manual. The hub is what "for each text" means: one place to see, track, and generate every
kind of output that text has spawned.

### The hub is a graph object (already in the model)
The pāṭala `data/corpus/graph.ts` + `canonical-spines.ts` already give the spine (root → commentary →
synthesis). Extend the model so every derived artifact is an **annotation/object on the hub**:
```
pt:work:ipvv
  ├─ pt:passage:...       (the 49 published passages)
  ├─ pt:essay:...         (each essay → its passages)
  ├─ pt:pushing:...       (the enquiry → its quoted passages)
  ├─ pt:argument:...      (the formal argument → its premises/conclusion → passages)
  └─ pt:learning:...      (each lesson → its passages)
```
The bibliography already lists the work; the hub makes its *outputs* first-class and queryable via
the API (`/api/works/:id` → returns translations, essays, arguments, learning).

---

## 2. The PUSHING method — the mechanical deep-dive (a reusable formula)

The `PUSHING-TANTRALOKA` / `PUSHING-IPVV` resources are the exemplar of a **mechanical formula** that
"hounds the text with why" and asks the hard questions scholars usually don't. Formalize it as a
reusable method, not a one-off:

```
PUSHING — the deep-dive formula (per source, per region)
1. Take the text's asserted claims.
2. Turn each into a "why?" question.
3. Hound the TEXT ITSELF (its own reasoning, its commentaries) for the answer — NOT our frameworks.
4. Store the FULL quoted passage for each question (the text speaks before we interpret).
5. Keep asking "why" until the text's deepest reasoning is exposed.
6. Our frameworks (aperture, MEPIT, pure-thesis) enter ONLY AFTER the text has spoken.
```

**The value:** this is the *discovery* step. It finds tensions, implicit commitments, and the
deepest arguments — which are exactly what the formal logical-argument layer then makes precise.

---

## 3. LOGICAL ARGUMENTS ARE THE GOLD — the compounding pipeline

The vision: **PUSHING finds tensions → formal logical arguments resolve/analyze them → essays get
written from the arguments.** It all compounds and tracks.

```
PUSHING enquiry (finds a tension, quotes the passages)
   ↓
FORMAL LOGICAL ARGUMENT (the gold)
   • premises extracted from the quoted passages
   • inference typed (reductio / analogy / identity / entailment)
   • conclusion
   • tied to the truth engine (NYĀYA→LEAN decomposition)
   ↓
ESSAY (written from the argument — every claim cites the argument + its passages)
   ↓
LEARNING (taught from the essay)
```

### The truth engine is the formalization machine
- `nyayaengine.py` (NYĀYA → LEAN decomposition, the "truth compressor") already exists as a scaffold.
- `ground_truth/nyaya_claims.json` holds formal claim data.
- `apoha-partition-formal.md`, `LOGICAL-ARGUMENT-1-reflexivity-debate.md`,
  `LOGICAL-ARGUMENT-NANAVIRA.md` are the exemplars — formal arguments built from the texts.
- The `LOGICAL-ARGUMENT-PAPER-FRAME.md` is the essay-writing-from-argument pattern.

**The compounding step:** once the corpus is machine-readable (passages + C1s + themes + resolve),
a PUSHING-found tension can be:
1. **Extracted** — its passages resolved (via `/api/resolve` + the published store).
2. **Formalized** — premises/conclusion into an argument object tied to those passages.
3. **Proved/analyzed** — run through the truth engine (Lean/Nyāya) where it's formalizable.
4. **Narrated** — an essay written from the argument, every claim pointing back to the evidence
   (the SHOW EVIDENCE / claim-level discipline).
5. **Taught** — a lesson derived from the essay.

This is the "compounds and tracks" engine: PUSHING → argument → essay → learning, all on the same
passage IDs, all queryable from the source hub.

---

## 4. The IPVV essays as the seed + future inspiration

The `research-library/recognition/` essays are the current examples of how Pāṭala expands once it
has a corpus. Save them as **hub outputs tied to the IPVV**, so they become:
- resources on `pt:work:ipvv` (via the bibliography + `/api/resources`),
- inspirational templates for the PUSHING→argument→essay pipeline (the reflexive-debate and
  logical-argument essays are the models).

---

## 5. What this enables (the vision, concretely)

| Capability | Today | With the hub + argument pipeline |
|---|---|---|
| "What does this text say?" | translations | translations + C1 + themes |
| "What are the hard questions?" | PUSHING-IPVV/Tantrāloka | a per-source PUSHING enquiry |
| "What are the tensions?" | manual discovery | PUSHING surfaces them; formal args make them precise |
| "What is the argument?" | LOGICAL-ARGUMENT essays | formal argument objects + truth-engine proofs |
| "Teach me" | lessons | essays → lessons, all sourced |
| "Where do I start?" | — | epistemic PageRank over the source hub |

---

## 6. The dual-agent split for this

- **Agent 2 (integration/content):** build the **source-hub model** (extend the graph + API so every
  source lists its essays/arguments/learning), save the PUSHING + IPVV essays as hub outputs, write
  the PUSHING-formula spec.
- **Agent 1 (ML/research):** build the **logical-argument layer** (the argument object schema + the
  truth-engine/nyāya link + the "extract tension → formalize → prove" pipeline + the benchmark for
  it).

They meet at the source hub: Agent 2 exposes the passages + essays; Agent 1 formalizes over them.

---

## 7. Immediate next steps (todos)

- [ ] **Hub model** — extend `canonical-spines.ts`/graph so a work lists its outputs (essays,
      arguments, learning, pushing) with passage links; expose via `/api/works/:id`.
- [ ] **Save the PUSHING + IPVV essays** as hub resources (register in the bibliography + resources
      so they're tracked against the source).
- [ ] **PUSHING-formula spec** — formalize the method (§2) as a reusable per-source template.
- [ ] **Argument object schema** — `pt:argument:` with premises/conclusion/inference/evidence →
      passages (Agent 1).
- [ ] **Truth-engine link** — tie the argument objects to `nyayaengine.py`/Lean (Agent 1).
- [ ] **The compounding pipeline** — a documented run: pick an IPVV tension → resolve passages →
      formalize → (prove) → essay → lesson.
