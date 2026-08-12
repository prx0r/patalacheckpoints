# ML PUSHING — turning the PUSHING/DNA method into a learnable pipeline

*2026-08-12. **Agent 1's (ML) read of the PUSHING work** — the QUESTIONNAIRE_REAL_DNA, the PUSHING
sessions, and the comparative spec. The central realization: **the PUSHING sessions are ALREADY a
supervised reasoning dataset** — `question → distinctions → theorem → boundary → next-pressure-point`,
each anchored to passages. This doc makes that structure formally learnable. Companion to
`SPEC_COMPARATIVE_PUSHING.md` (the method) and `SPEC_ARGUMENT_TRUTH_PACKET.md` (the argument object).*

---

## 0. The insight: pushing is already ML-shaped

Reading the raw sessions (logic5, the PUSHING-IPVV scaffold), every session has the same latent
structure:

```
QUESTION        the pressure point (mechanism-gap, crux, subversion, quantifier, register, root)
DISTINCTIONS    the text's terms separated (e.g. manifestation ≠ presence ≠ experience ≠ consciousness)
THEOREM         the boxed result ("Reality is manifest before it is interpreted as belonging to a subject")
BOUNDARY        "what has actually been established" — the honest limit ("he has NOT proved one Self")
NEXT_PRESSURE   the new question the text forces ("why is prakāśa always accompanied by vimarśa?")
PASSAGES        the passages the session cites (V2L, V2O, V2P...)
```

This is **exactly** the supervision the whole project wants — but it's in prose. Turning it into typed
records makes it:
- **retrievable** (question → passages, the same premise→support shape as the argument pipeline),
- **classifiable** (which question-shape? which kind of boundary?),
- **trainable** (can a model predict the next pressure-point from a text + a question?).

So the PUSHING work is not a side-doc — it is **the richest existing source of supervised scholarly
reasoning** in the corpus. This is the "the best questions are grown, not pre-written" insight made
learnable: **if we record how questions grow, we can learn the growth.**

---

## 1. The four things to formalize (in order of value)

### 1.1 The pushing-record data type (the core object)

```ts
interface PushingRecord {
  id: string;                    // pt:pushing:<work>:<session>:<n>
  work_id: string;
  question: string;              // the pressure point, verbatim
  question_shape: "MECHANISM_GAP" | "CRUX" | "SUBVERSION" | "QUANTIFIER" | "REGISTER" | "ROOT";
  stage?: string;                // the 7-fold stage it belongs to (Being/Power/…/Liberation)
  distinctions?: string[];       // the terms separated
  theorem: string;               // the boxed result (the gem)
  boundary: string;              // what has NOT been established (the honest limit)
  next_pressure: string;         // the question the text now forces
  passage_ids: string[];         // resolved passages
  strength: "PROVED" | "REVIEWED" | "WELL_SUPPORTED" | "PLAUSIBLE" | "PARTIAL" | "SILENT";
  source_file: string;           // the session file
}
```

This is the **machine shape of the DNA**. It is the logical layer's `PushingRecord`, and it produces the
argument truth-packets (§1.2).

### 1.2 The mapping to the existing pipeline

```
PushingRecord.theorem  →  the ArgumentTruthPacket.conclusion  (SPEC_ARGUMENT_TRUTH_PACKET.md)
PushingRecord.passage_ids → the premises' passage_ids
PushingRecord.boundary  →  the honest verdict (PROVED vs PLAUSIBLE vs SPECULATIVE)
PushingRecord.next_pressure → the tension_id of the NEXT argument
```

So a pushing session is **not parallel to the argument pipeline — it FEEDS it.** Each session's
theorem is a candidate argument conclusion; its boundary sets the strength; its next_pressure seeds the
next argument. The compounding loop is: PUSHING → ARGUMENT → (boundary as verdict) → ESSAY → next
PUSHING. This is the other agent's loop, but now each step is a **typed record** instead of a prose file.

### 1.3 The comparative matrix (from SPEC_COMPARATIVE_PUSHING §3)

The matrix `question × text → answer-cell` is already specced. For ML it's a **multi-text supervision
table**: the same question-shape across texts gives *contrast* labels (a question one text answers
WELL_SUPPORTED and another is SILENT on is exactly the "unanswered-is-data" signal). This becomes the
PATALA-STRUCTURE / comparative task substrate.

---

## 2. The ML tasks (what becomes learnable, once §1.1 exists)

| Task | Suite | Input → output | Baseline | Why it matters |
|---|---|---|---|---|
| **Question-shape classification** | PATALA-STRUCTURE | session question → MECHANISM_GAP/CRUX/SUBVERSION/… | majority-class | learns *how* Pāṭala pushes (the DNA) |
| **Theorem → passage retrieval** | PATALA-EVIDENCE | a theorem/gem → the passages that license it | BM25 | the premise→support task, from real pushing |
| **Boundary detection** | PATALA-EVIDENCE | session prose → the honest-boundary sentence | — | learns to *not* overclaim (the "AI proposes ≠ asserts" rule, machine-learned) |
| **Next-pressure prediction** | PATALA-STRUCTURE | text + question + boundary → next_pressure | — | the deepest: learns the *growth* of questions — the "grown, not pre-written" insight made predictive |
| **Cross-text answer retrieval** | PATALA-RETRIEVAL | question-shape → the passages across texts that answer it | BM25 | the comparative matrix as retrieval |

**The two highest-value, most-honest tasks:**
1. **Theorem → passage retrieval** — gold derived from *real* sessions (the sessions already cite
   passages); no invented labels. Same principle as my see_also tasks.
2. **Boundary detection** — this is the *unique* Pāṭala signal. Most corpora teach a model what a text
   says; Pāṭala can teach a model **what a text does NOT establish**. That's the "honest boundary" made
   learnable, and it's the machine version of the epistemic-compiler rule.

---

## 3. The immediate build (my lane, grounded in real data)

The pushing sessions are on disk (`research-library/pushing/_source/` + `recognition/pushing-*/`). The
first build is a **pushing-parser + record extractor**:

1. **`patala_ml/pushing.py`** — parse the session files into `PushingRecord`s. The session structure
   is regular enough (Question / Distinct / Theorem / Boundary / Next) that a deterministic parser +
   a small model-assisted extraction can bootstrap ~50–100 records from the existing sessions (PUSHING-
   IPVV Q1–Q10 + their gems; the LOGICVID sessions; the Tantrāloka Q1–Q25).
2. **Map each record's `passage_ids`** via `/api/resolve` (the deterministic floor — if a session cites
   V2L, resolve it to the real passage id).
3. **Generate the PATALA-EVIDENCE tasks** (theorem→passage) + PATALA-STRUCTURE tasks (question-shape,
   boundary) from the records.
4. **Run the BM25 baseline** on theorem→passage retrieval.
5. **Log the handoff**: "pushing records extracted; here's the schema; Agent 2, confirm the comparative
   matrix + hub wiring."

**Honesty guardrails (same as always):**
- The parser is *assisted* by a model but every record is human-reviewable; `status: MACHINE_DRAFT`
  until reviewed.
- `passage_ids` must resolve (the deterministic floor) — no guessing.
- The boundary is extracted verbatim (it's the session's own honesty), not rewritten.

---

## 4. How this fits the vision

The PUSHING→ML pipeline is the **discovery engine of the computable scholarly tradition**:
- PUSHING finds the tensions (the "why" questions) — the discovery step.
- Formal arguments + boundary detection make them precise and honest — the analysis step.
- The question-growth (next-pressure) is learnable — so the system can *propose* new penetrations the
  same way the human grows them ("grown, not pre-written" becomes a learned capability).
- The comparative matrix makes every text answer the same shapes — the cross-tradition spine.

This is the **fifth research question in the frozen strategy** — *"Can models discover relationships
experts accept without erasing disagreement?"* — operationalized. And it's the one lane where Pāṭala's
*philosophical* DNA (mechanism-gap, crux, honest boundary) becomes *ML* DNA.

---

## 5. What I need from Agent 2 (the handoff request)

For the pushing records to resolve cleanly, I need the comparative/matrix + hub wiring confirmed, and
specifically:
- The `questionnaires.ts` data (CORE shapes + Śaiva Q1–Q25) versioned, so records can be tagged by
  question-id.
- Confirmation that `pt:pushing:` is a hub kind (or my records just live in `research/pushing/` until
  then — not blocking).
- A schema handshake if the pushing-record shape should be a shared type.

Nothing blocks the parser itself — it reads the session files on disk and produces records I own.

---

## 6. Bottom line

The PUSHING work is the **most ML-ready scholarly asset nobody has yet treated as data**. Its sessions
already contain `question → distinctions → theorem → boundary → next-pressure → passages` — the exact
supervision the project wants, including the rare "what the text does NOT establish" signal. Formalizing
it as typed `PushingRecord`s:

1. feeds the argument-truth-packet pipeline (theorem → conclusion, boundary → verdict),
2. yields honest, non-invented gold for theorem→passage retrieval,
3. makes the **boundary** — Pāṭala's unique honesty — a *learnable* classification,
4. and (the deepest) makes **question-growth** predictive: the "best questions are grown, not
   pre-written" insight becomes a model capable of proposing the next pressure-point.

The immediate build — a pushing-record parser over the real sessions — is 100% in my lane, reads only
what's on disk, and produces the first supervised-reasoning records from genuine Pāṭala scholarship.
