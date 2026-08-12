# TRANSLATION APPROACH & VALIDATION — the doctrine for large-text autonomous translation

*2026-08-12. The production-critical notes on how to translate HUGE texts (Tantrāloka, Svacchanda,
Kubjikāmata...) with the autonomous Agent 3 factory — grounded in how we already did the IPVV. The single
most important principle:

> **A translation is genuinely useless if it is wrong.** An agent can translate entire works that then
> become unusable. Validation is therefore the most important thing — more important than raw production
> speed. Never let the factory outrun the validator.

---

## 0. THE GOLD STANDARD (reference every time)

**Mark Dyczkowski's Tantrāloka is the gold standard** for how a scholarly Śaiva translation should read.
Volume 1 is on disk:

```
/mnt/HC_Volume_106427611/sanskritree/sources/muktabodha-lib/
  tantrAloka chapters 1 thru 14-M00092-IAST.txt   (vol 1, 54,497 lines, M00092, BY-NC 4.0)
  tantrAloka chapters 15 thru 38-M00093-IAST.txt  (vol 2)
/mnt/HC_Volume_106427611/sanskritree/sources/gretil_tantraloka.txt
```

**A NEW AGENT working on any Śaiva translation must first review the Dyczkowski Tantrāloka** — the
transcription under Dyczkowski's direction, the Jayaratha commentary, and the house style it models. It is
the calibration for register, terminology, and how the Sanskrit is carried into English.

**For a specific work, ALSO web-search the actual scholarship on that text.** The same Sanskrit term can be
used differently across works and traditions. This is hard and must be planned for:
- `śakti` in the Krama packet ≠ `śakti` in the Śaiva Siddhānta
- `vimarśa` in the IPVV (Pratyabhijñā) ≠ how it functions in a Kaula ritual text
- a term's *technical sense* is set by the tradition + the commentary, not by the dictionary

**Rule:** before translating a work, build its **term/context packet** — how the key terms are used in THAT
work (same-work usage, same-author, same-school, commentary) — so the translator doesn't import the wrong
sense from another tradition.

---

## 1. HOW WE DID THE IPVV (the proven method)

The IPVV was not translated in one pass. The method, which scales to any huge text:

```
SOURCE (the raw edition / manuscript)
   ↓  CHUNK   split into bounded, addressable chunks (the IPVV's 49-63 chunks)
   ↓  CONTEXT  build the context packet for the chunk (same-work, same-school, commentary)
   ↓  L0       lossless token/gloss substrate (PROVED source spans)
   ↓  L1       CONTROLLED translation (Sanskrit-close, proposition-faithful)
   ↓  L2       readable prose
   ↓  L200     the audit (derivation map, MT/IA split)
   ↓  C1       commentary
```

**The two things that made IPVV work (and must not be skipped for any large text):**

1. **Chunking.** Do not translate "a whole book." Split into bounded chunks (a few hundred lines / a
   paṭala / a vimarśa) so: each chunk is independently verifiable, a bad chunk fails without corrupting the
   whole, and the queue processes chunk-by-chunk. This is why `agent3_queue.py` processes *passages*, not
   entire works.

2. **Context engineering on a TOP-TIER translation FIRST, then review.** Before the bulk pass, produce a
   small exemplar (a few chunks) at the highest quality, review it hard, and freeze it as the house standard
   for the rest. You do NOT start mass-producing until the exemplar is right. This is the
   "before attempting it we did some context engineering on top tier translation to ensure it was how we
   wanted and then reviewed" — it's the calibration gate.

---

## 2. WHY VALIDATION IS THE MOST IMPORTANT THING

A wrong translation is worse than no translation — it silently poisons everything downstream (L2, C1,
arguments, the benchmark). So the factory is built **fail-closed, validate-first**:

```
RAW SANSKRIT
   ↓  L0  [PROVED source spans — lossless, immutable versioned]
   ↓  L1  [CONTROLLED — proposition-faithful, auditable]
   ↓  AUDIT [structural + semantic checks; FAIL → review queue, never a silent pass]
   ↓  REVIEW [human/expert adjudication at the exemplar + crux level]
```

**The validation gates (from the northstar + our P3 lesson):**
- **P0 source-span** — PROVED (mechanical, lossless). Already done.
- **False-certainty** — the killer metric. A translator that invents a lemma/sense it doesn't actually
  know = unusable output. Abstain (AMBIGUOUS/OPEN) is the correct, valuable behavior.
- **Chunk-level review** — the exemplar is reviewed before mass production; crux passages are human-checked.

**The economic threshold** (the question that decides if Agent 3 is worth using):
> **Is this output worth reviewing rather than redoing from scratch?**
If the factory's error rate makes review-as-hard-as-redo, the factory is not yet viable. The metric is
**review burden**, not token cost.

---

## 3. THE SPECIFIC RISK: SANSKRIT TERMS USED DIFFERENTLY ACROSS WORKS

This is genuinely hard and must be planned for:

| Risk | Example | Mitigation |
|---|---|---|
| Same term, different tradition | `śakti` (Krama power vs Siddhānta) | per-work term packet, not a global glossary |
| Technical sense set by commentary | a term's meaning fixed by Jayaratha/Abhinava | consult the work's own commentary |
| False friend across works | a word that looks like a known term but isn't | verify against the specific work's usage |
| Pūrvapakṣa vs siddhānta | who is speaking (opponent vs author) | source-layer tagging (the IPVV's L200) |

**The plan:** each work gets a **term-context packet** (from the northstar's agentic loop — RETRIEVE
same-work / same-author / same-school usage) built BEFORE the gloss pass, so the translator never imports a
sense from the wrong tradition.

---

## 4. THE AGENT 3 SEQUENCE FOR A HUGE TEXT (the safe way)

```
1. SOURCE      register the work's source (Tantrāloka M00092, Svacchanda, etc.)
2. TERM PACKET build the per-work term/context packet (Dyczkowski review + web search + commentary)
3. EXEMPLAR    translate + review a few chunks to TOP quality; FREEZE as the standard
4. QUEUE       the prioritized queue processes remaining chunks (agent3_queue.py)
5. VALIDATE    each chunk: P0 lossless + L1 controlled + audit; FAIL → review queue
6. VERSION     each successful chunk commits an immutable L0 version (l0_registry.py)
7. REVIEW      crux + exemplar-level human adjudication before anything is trusted
```

**The guardrail:** the factory never outruns the validator. A chunk that fails structural or semantic
audit goes to the review queue and HALTS its branch — it does not get silently marked complete and it does
not block the rest of the work.

---

## 5. THE ONE-SENTENCE CARRY-FORWARD

**Translate huge texts the way we did the IPVV — chunk, context-engineer a top-tier exemplar and review it
first, then run the prioritized queue with validation as the hard gate (P0 lossless + false-certainty +
abstention + chunk review), using Dyczkowski's Tantrāloka as the calibration gold standard and a per-work
term-context packet to stop the same Sanskrit term from being misread across traditions — because a wrong
translation is worse than no translation, and the factory is only worth running if its output is cheaper
to review than to redo.**
