> **ARCHIVED / SUPERSEDED** — kept for history only. Do NOT follow as current. See `docs/INDEX.md` + `docs/DOCS-AUDIT.json` for the canonical doc for this concern.

# nextdev2 — Pāṭala Development Plan (forward)

*2026-08-10. The forward-looking plan consolidating everything this session established.
Companion to `nextdev.md` (the six primitives), `PROCESS_NOTES.md` (the strategic reset),
`HANDOVER.md`/`HANDOVER_NEXT.md` (the handover), and `STATE_OF_PLAY.md`. This doc is the
*what-to-do-next*, grounded in what now actually exists.*

---

## 1. Where we are (the ground truth)

### The product is built and proven
- **The publishable auditable translation object** — the thing Pāṭala publishes. `source
  span → decision → target span`, with first-class evidence, review, and version lineage.
  Proven on Kramasadbhāva 1.8 (`/read/kramasadbhava/1.8`).
- **The auditable reader** — phrase-clickable: hover-aligns Sanskrit/English, click a
  decision phrase → side panel (status, alternatives, why, evidence cards, review),
  READ/AUDIT toggle.
- **The API** — 19 routes incl. `/api/passages/:id/translation` + `/api/decisions/:id`.
  101/101 tests.
- **The pipeline** — T1→T3 via Hermes works (Milestone A1 proven); C1 is done by the
  editorial model (you), NOT machine-generated.
- **The six primitives + scholarly graph** — Identity/Assertion/Evidence/Provenance/
  Review/Rights + objects/annotations, with a lint and gold-fixture regression.

### The core loop (the product)
```
PUBLISHED TRANSLATION
  → TARGET SPAN
  → ALIGNMENT
  → TRANSLATION DECISION
  → EVIDENCE
  → REVIEW EVENTS
  → VERSION LINEAGE
```

### The strategic reset (locked)
Pāṭala = **provenance + adjudication infrastructure**, not a translation factory.
The moat = evidence-backed scholarly judgments (the "Sense"/"Synthesis" layers). Hermes
owns model plumbing; C1s are written by the editorial model with anchored context.

---

## 2. The direction (what we're building toward)

### The reader is the product; the site is built around it
The website is NOT the graph. It is a **pleasant reading experience** where every
interpretive decision is inspectable. Landing → texts → reader; plus traditions,
concepts, learning, about/method.

### Content is the high-signal move (we are bored of infra — rightly)
We already hold real content we haven't surfaced:
- **Per-school dirs** `sanskritree/saivamap/{trika,krama_kalikula,kubjika,kaula,spanda_pratyabhijna,sarvamnyaya}` (core texts + anchors per tradition)
- **11 dossiers** (kula, krama, śakti, vimarśa, spanda, mātṛkā-khecarī, ...)
- **6 real C1s** already written (Śivasūtra, Akulavīra, Kubjikā, KJN, ...)
- **A 1540-line Tantrāloka workbook** (`corpus/learning/REFERENCE_TANTRALOKA_WORKBOOK.txt`)
- **The thesis** (`sanskritree/THESIS.md`) — a separate proof-engine thread

---

## 3. The concrete next moves (priority order)

### A. Per-school learning pages (the endgame3 "Learn X" pathway) — HIGHEST
*Architecture: see `docs/vision/education/LEARNING_STRATEGY.md` — research once, structure once, distill
repeatedly. The durable unit is the ConceptLesson (knowledge packet); video/shorts/quizzes
are renderings of it, never separately-researched formats.*
For each school, build `/traditions/{krama,trika,kubjika,kaula,...}` pulling from
`saivamap/` + dossiers + C1s + links to the reader:
```
/traditions/krama
  What is Krama?            (plain-language, from dossiers + C1s)
  Core texts                (Kramasadbhāva, Mahānayaprakāśa, Mahārthamañjarī)
    → each links to its reader
  Key concepts              (krama, saṃvit, Kālīs) → concept pages
  The workbook              (if one exists for that school)
```
This makes the textual landscape navigable — the mission, for real.

### B. C1 commentaries, school by school — the content engine
Write C1s for high-value passages with the editorial model + anchored context (per
`skills/write-commentary`). Follow the map's order (Trika → Krama → Kubjikā). Each C1
becomes the reader's Commentary block + feeds concept pages. Start with the 5 strongest
passages, then scale. The Śivasūtra C1s prove the format.

### C. Surface existing content
- The **Tantrāloka workbook** → `/learning/tantraloka-workbook` (the "Learn Trika" pathway)
- The **dossiers** → `/concepts/{lemma}` interactive pages
- **The external resources** — DONE: `data/atlas/resources.ts` (29 typed + tradition-tagged
  sources) surfaced on `/resources` + `GET /api/resources`. Next: the contextual join layer
  (resource blocks on text pages via each resource's `works?` field) + an MCP `get_resources` tool.

### D. Scale the reader to the 25-verse unit
Generate `PublishedTranslation` candidates for Kramasadbhāva 1.1–1.28 (Hermes emits
spans/alignments/decisions; the pattern is proven on 1.8). The reader component is
data-agnostic — no redesign.

---

## 4. The reader interactions (the target UX)

### Default: clean prose
- Sanskrit line, English line, commentary below.
- Most spans just align; only materially interpretive choices have a decision.

### Hover
- Hovering `nirānande` (Sanskrit) highlights `O bliss-less one` (English), and vice-versa
  (via the Alignment object).

### Click a decision phrase → right-hand panel
```
nirānande
Current rendering   O bliss-less one
Status              OPEN  (plain-language: "More than one serious reading remains.")
Alternative         bliss at rest / stillness
Why                 the published rationale artifact
Evidence            [cards: role + resource + locator + excerpt + verification]
Review              Machine proposal · not yet reviewed by a specialist
History             v1 "beyond bliss" → v2 "O bliss-less one"
```

### READ / AUDIT toggle
- **READ**: clean Sanskrit + English.
- **AUDIT**: decision phrases visibly marked (OPEN red, CONSTRAINED green, PREFERRED
  saffron); decision list shown.

---

## 5. The scholarly loop to complete (after reading works)

```
PUBLISH → READ → INSPECT DECISION → PROPOSE/REVIEW → VERSION → REPUBLISH
```
- **Suggest correction** inside the decision panel (structured form → ReviewEvent / human
  proposal; never mutates the accepted translation directly).

---

## 6. The semantic flywheel (later, not now)

Once ~20 grounded sense assignments exist:
- Reviewed SenseAssignments seed candidate discovery for nearby passages → term-history
  becomes an *output* of audited work, not hand-authored.
- `/concepts/nirānanda` becomes automatically useful (occurrences + sense assignments +
  evidence + trajectory).

Do NOT build this before the reader + C1s + school pages exist.

---

## 7. What NOT to do next

- No more model-interface rabbit holes (Hermes owns plumbing; C1s are editorial).
- No broad 58-record bibliography sweep (just-in-time only).
- No giant graph migration / bulk-encoding (the unit grows by use).
- No RAG / embeddings / lemmatizer (the reset explicitly deferred these).
- No consumer app / payments / marketplace / courses-platform / retreats yet.
- No new backend entity types until the reader shows a real gap.

---

## 8. The immediate plan (first actions)

1. **Build `/traditions/krama`** as the first real school page (wired to reader + dossiers
   + C1s + the workbook). Prove the school-page pattern.
2. **Write 5 C1s** (Śivasūtra-style) for the strongest Krama passages, with the editorial
   model + anchored evidence.
3. **Surface the Tantrāloka workbook** as a learning pathway.
4. **Scale the reader** to the 1.1–1.28 unit (generate published objects; the component
   is data-agnostic).

Everything else follows from the reader + content being genuinely useful.

---

## 9. Files to read for the next agent

| File | What it is |
|---|---|
| `HANDOVER_NEXT.md` | the handover (current state + next build) |
| `PROCESS_NOTES.md` | the strategy + reset |
| `STATE_OF_PLAY.md` | the honest state |
| `docs/SCHOLARLY_GRAPH.md` | the canonical data model |
| `docs/endgame2.md` + `endgame3.md` | the hub + learning vision |
| `skills/write-commentary/SKILL.md` | how to write a C1 |
| `../sanskritree/saivamap/` | the per-school working tree (content) |
| `../sanskritree/corpus/learning/REFERENCE_TANTRALOKA_WORKBOOK.txt` | the Learn-Trika pathway |
| `experiments/advice-response.md` | the full strategic advisory |
