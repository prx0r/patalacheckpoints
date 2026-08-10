# Pāṭala Learning Strategy — research once, distill repeatedly

*2026-08-10. The content architecture. The educational layer must be **derived from**
the scholarly infrastructure, never free-floating explainers. The durable unit is the
**knowledge packet**; everything else — videos, shorts, quizzes, courses — is a rendering
of it. This keeps the learning content correct (it bottoms out in passages + evidence +
review) and maximally reusable.*

---

## 1. The principle

> **Research once. Structure once. Distill repeatedly.**

The transformation chain:

```text
PRIMARY TEXT + SCHOLARSHIP
        ↓
RESEARCH NOTE / ESSAY        ← the canonical scholarly object
        ↓
CONCEPT EXPLAINER            ← the teaching distillation
        ↓
3–4 MIN VIDEO SCRIPT
        ↓
SHORT / QUIZ / FLASHCARD
```

Do **not** create each format separately. Create one strong source object, then derive
everything else from it. Videos age; scripts get rewritten; UIs change. The knowledge
packet is the durable object.

---

## 2. The canonical object: the knowledge packet

```text
ConceptLesson
- title
- question
- core_claim (2–4 sentences)
- prerequisites[] (concept ids)
- primary_passages[]       (stable passage ids)
- claims[]                (each an auditable assertion)
- evidence[]              (passages, scholarship, dossiers)
- scholarly_support[]     (Ratié, Torella, Bäumer, Dyczkowski, ...)
- key_distinctions[]      (what this does NOT mean)
- open_or_contested[]     (honest uncertainty)
- full_explanation        (1000–2500 words — the research-grade essay)
- short_explanation       (400–600 words — the 3-min explainer)
- memory[]                (3–5 recall questions)
- review_state            (proposed / reviewed / accepted)
```

Every claim in the packet can link straight to a primary passage, scholarship, or the
terminology dossier — so even beginner material has a hidden academic spine.

---

## 3. Three depths, one source

Expose each packet at three depths:

```text
QUICK   3–4 minute explanation   (the short_explanation)
DEEP    full essay / research note (the full_explanation)
SOURCE  primary passages + citations + audit trail   (links to the reader)
```

This matches Pāṭala: the educational layer always bottoms out in actual passages.

---

## 4. One research session → four assets

For each concept, one research session (20–40 min) produces:

```text
MASTER NOTE   "What is vimarśa?"      ~2,000 words
    ↓
EXPLAINER     "What does it mean for  ~500 words
               consciousness to know itself?"
    ↓
SHORT         "Why awareness isn't    ~100 words
               just a light"
    ↓
QUIZ          "Why isn't prakāśa alone sufficient?"
```

No format is researched independently — each is a distillation of the master note.

---

## 5. Learning around questions, not chapter order

Structure learning by **questions in prerequisite order**, not by "Tantrāloka chapter 1,
then chapter 2." Example (Trika):

```text
Why don't I experience myself as Śiva?
What is recognition?
What is prakāśa-vimarśa?
What is śakti?
Why does consciousness appear limited?
What are the kañcukas?
What are the 36 tattvas actually doing?
What is mala?
What is śaktipāta?
Why are there different upāyas?
What does initiation change?
What is mantra?
What is kula?
What is Krama?
What is liberation according to Abhinavagupta?
```

---

## 6. The per-tradition pathway (10–20 questions each)

For Trika, a simple 20-question curriculum:

```text
FOUNDATIONS      1. What is consciousness?  2. What is recognition?
                 3. Why don't we recognize ourselves?  4. Prakāśa & vimarśa
                 5. Śakti & svātantrya
MANIFESTATION    6. How does the One appear as many?  7. The 36 tattvas
                 8. Māyā & the kañcukas  9. Mala  10. Spanda
PRACTICE        11. Śaktipāta  12. The upāyas  13. Mantra
                14. Initiation  15. Vijñānabhairava-style practice
SYNTHESIS       16. Kula  17. Krama  18. Bhairava  19. Liberation
                20. What Abhinavagupta is actually claiming
```

Each node = one 3–4 min lesson with a **Deep dive** below it. That's a real curriculum
without a course platform.

---

## 7. Videos come last in the chain

```text
research → accurate written explanation → teaching explanation → script → video
```

One pathway of 20 lessons can produce, from the SAME research:

```text
20 site explainers
20 × 3–4 min videos
20 deeper essays/notes
~40–60 shorts
3–5 long YouTube videos
1 coherent beginner course
```

YouTube and the website reuse the same material: site "What is vimarśa?", 3-min video of
the same lesson, long-form combining 6 related lessons, shorts from individual hooks.

---

## 8. The immediate move (do NOT build a platform yet)

1. Take the existing Tantrāloka workbook (`corpus/learning/REFERENCE_TANTRALOKA_WORKBOOK.txt`)
   and turn it into **20–30 questions in prerequisite order**.
2. Pick the first five and make each one:
   - 1 research-grade master note
   - 1 excellent 3–4 minute explainer
   - 3–5 recall questions
3. Put those on simple pages.

If that feels good, you have the learning system. Video generation, progress tracking,
spaced repetition, and courses can all be added later as *renderings of packets*.

---

## 9. How this fits the auditable architecture

When the explainer says "Vimarśa is consciousness's reflexive self-apprehension," that
claim links straight to:

```text
Tantrāloka passage   → /read/...
Pratyabhijñā passage → /read/...
scholarship          → the decision/evidence trail
terminology dossier  → /concepts/vimarśa
```

So the ConceptLesson is really a **view over the scholarly graph** — the knowledge packet
is assembled from, and bottoms out in, the same infrastructure as the reader. This is the
"research-grade essays, not academic-paper ceremony" middle ground: 1,500–3,000 sharp
words establish the problem, the answer, the Sanskrit vocabulary, the primary passages,
the major scholarly interpretations, and where simplification becomes misleading.

---

## 10. File map

| Artifact | Where |
|---|---|
| This strategy | `docs/LEARNING_STRATEGY.md` |
| Tantrāloka workbook (the seed content) | `sanskritree/corpus/learning/REFERENCE_TANTRALOKA_WORKBOOK.txt` |
| The master map | `sanskritree/corpus/learning/REFERENCE_TANTRALOKA_MASTER_MAP.md` |
| C1s (the scholarly material to draw from) | `sanskritree/translations/06_c1_interpretation/` |
| Dossiers | `sanskritree/saivamap/dossiers/` |
| The reader (the SOURCE depth) | `app/read/[work]/[locator]/` |
