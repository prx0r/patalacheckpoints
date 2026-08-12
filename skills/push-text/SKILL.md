---
name: push-text
description: "Run a Pushing enquiry (the Logicvid method) on a primary source: hound a text with 'why' to force its own reasoning out, find its tensions/paradoxes/hidden-premises, run the construct-destroy-provenance three passes, and emit strength-graded truth-packets anchored to passages. Use when asked to 'push a text', 'create a pushing file', find a text's cruxes or deepest questions, or turn a tension into a logical argument. The method is a SKILL (reasoning), not a script — the human stays the selection oracle."
version: 1.0.0
author: Pāṭala
metadata:
  hermes:
    tags: [pushing, logicvid, enquiry, argument, crux, tantra, scholarly, patala]
    related_skills: [write-commentary, translate-work, validate-passage, use-api]
    checkpoint: CP4 (pushing produces the argument material the gold + truth-packets consume)
---

# PUSH — run a Pushing enquiry (the Logicvid method)

## Purpose

Hound a text with "why" and **force its OWN reasoning out**. Our frameworks only supply the
questioning; the answers must come from the text. The output is a set of **penetrations** (where the
text asserts but does not prove) and **truth-packets** (arguments with a derived claim-strength),
each anchored to resolved passages.

This is a **skill**, not a script: it runs on reasoning and judgment, and the **human stays the
selection oracle** (which question is genuinely piercing — never automate that away).

## The one rule

> Hound the text with "why," and force its OWN reasoning out. Our frameworks enter only AFTER the
> text has spoken.

The extracted passages are the source of truth. Store **more passage than you need** — the text must
be re-readable and re-pushable.

## The two loops (what Pushing is)

```
SANSKRIOT → claims → definitions → dependencies → proof-or-boundary → GRAPH      (decomposition)
graph tension → paradox → hidden premises → branches → research → NEW GRAPH      (question-growth)
```

Pushing is the **question-growth** loop on top of the **decomposition** loop. It grows the graph the
formal engine then proves over.

## The question-asking DNA (from the real sessions)

Ask the same **question-shapes** the deep sessions use — not "what is X":

- **MECHANISM-GAP** — "why must prakāśa be accompanied by vimarśa?" (why is X necessarily Y?)
- **CRUX / theodicy** — "why does impurity arise? would Śiva choose suffering?"
- **SUBVERSION** — "does every cognition know itself?" (attack a relied-upon assumption)
- **QUANTIFIER** — "how does 'I am not any object' become 'I am the consciousness of every object'?"
- **REGISTER** — "a mother's grief IS suffering — is it really just a rasa?" (force the honest answer)
- **ROOT** — "what is time?" asked repeatedly until it becomes "is time itself a contraction?"

The 7-fold model is the **frame**; the Q1–Q25 are the **content** (the empirical questions the
Tantrāloka forced). The deepest questions are **grown by pushing, not pre-written** — record the NEW
questions each text forces.

## The round-structure of a session

```
ROUND N
  The question       (the sharp "why")
  The text's answer  (restated EXACTLY as it argues — no strawman)
  The new deeper question it forces
  > PENETRATION N:   (the exact spot where the text asserts but does not prove)
```

## The repeatable artifact (one enquiry = one folder)

```
inquiries/<slug>/
  root.json          question + source_scope + core_tension + hidden_premises + status
  source-spans.json  the quoted passages (the text speaks)
  reconstruction.md  Pass A: the strongest coherent reconstruction
  prosecution.md     Pass B: destroy it
  provenance.md      Pass C: every claim → a passage
  branches.md        the residual questions
  logicvid.md        the compiled enquiry (the output)
```

`root.json`:
```json
{
  "question": "If I must already be Śiva to recognize myself as Śiva, how can I recognize myself as not-Śiva?",
  "source_scope": ["Tantrāloka", "Tantrasāra", "Īśvarapratyabhijñā"],
  "core_tension": ["identity is invariant", "self-knowledge is presently limited"],
  "hidden_premises": [],
  "status": "seed"
}
```

## The three passes (the anti-cheat — do not skip)

- **Pass A — Construct.** Produce the strongest coherent reconstruction from the passages.
  Output: primitives · claims · dependency chain · hidden premises · chapter function · tensions · questions.
- **Pass B — Destroy.** A SEPARATE agent (do not reuse the construct agent) is FORBIDDEN from
  improving it; its only job is to find: unsupported entailments · conflated levels · translation
  dependence · missing intermediate claims · passages that resist · rival readings · false
  formalization · contradictions hidden by vague wording. The construct agent repairs only what survives.
- **Pass C — Provenance audit.** Every explicit claim has a passage · every derived claim lists
  premises · every cross-source claim preserves direction · every contradiction survives scope
  separation · every Sanskrit term keeps tradition-local meaning.

## The honesty rules (the discipline that makes it trustworthy)

1. **Licensed vs not.** Always split what the text *licenses* from what it *does not* (logicdog: a
   dog enacts contracted aham-vimarśa → "ontological recognition" licensed; a dog attaining
   liberating recognition → unsupported). State the unsupported as unsupported.
2. **Face the relabelling accusation head-on.** The naturalist's strongest objection: "vimarśa is a
   metaphysical relabelling of multiscale self-organization." Meet it: Abhinavagupta can accept every
   empirical mechanism and still hold it does not explain why manifestation is self-apprehending.
3. **Refuse three errors:** compression (forcing distinct claims into one clean system) · attribution
   (giving Abhinavagupta a later commentator's repair) · bridge (treating similar terms as identical —
   prakāśa = phenomenal consciousness is a *probe, not an identity*).
4. **Never collapse levels.** Use the 6-level frame (M→D→B→N→W→R: manifestation → differentiation →
   bounded embodiment → normative agency → world-model → recognition). Never write "consciousness =
   integration."

## Turn arguments into truth-packets

Treat each penetration's argument like a translation: an auditable object with a resolvable path and a
**derived claim-strength**:

```
pt:argument:<work>:<slug> {
  work_id, title, kind (reductio|analogy|identity|entailment|decomposition),
  premises [ {text, passage_ids} ], inference, conclusion {text, passage_ids},
  tension_id, provenance, proof?, status (MACHINE_DRAFT → REVIEWED|PROVED|OUTSIDE_FORMAL|HOLLOW)
}
```

Claim strength is **derived**, never hand-waved:
```
PROVED           formal proof exists (truth engine / Lean)
REVIEWED         human review accepted reconstruction + provenance
WELL_SUPPORTED   premises resolve, inference sound, no surviving prosecution
PLAUSIBLE        coherent reconstruction with a live objection (the tension stands)
SPECULATIVE      a probe — explicitly NOT asserted as the text's claim
```

An essay then says "the text's position (WELL_SUPPORTED, prem. A, B, C)" vs "a possible reading
(SPECULATIVE)" — never overclaiming. The auditable path: conclusion → inference → premises → each
premise resolves to its passage (via `/api/resolve`).

## The compounding pipeline

```
PUSHING (finds tension, quotes passages)
  → resolve passages (/api/resolve + published store)
  → FORMAL LOGICAL ARGUMENT (the truth-packet)
  → TRUTH ENGINE (PROVED / OUTSIDE_FORMAL / HOLLOW — honest)
  → ESSAY (cites the argument at its claim-strength)
  → LEARNING
  → back to PUSHING the next tension
```
All tracked on the source hub (`/api/hub`): `pt:hub:<work>:<kind>:<slug>` with `passage_ids`.

## Working procedure (when invoked)

1. **Assemble the source.** Gather T1/L2/L200/C1 + the spine + the hub for the work.
2. **Engineer the question-asking context first** (the key). Read the session so you ask the DNA
   shapes, not generic "what is X" questions.
3. **Run the loop** to natural endpoints. Question → text's answer → deeper question → penetration.
   Pivot until the questions repeat (you've found the bottom).
4. **Run the three passes** (construct / destroy / provenance). Pass B is a separate destructive agent.
5. **Extract truth-packets** from the penetrations with derived claim-strength.
6. **Compile the pushing file** into `inquiries/<slug>/` + the `logicvid.md` deliverable.
7. **Record the NEW questions the text forced** (the grown layer) — these are where the text is most
   itself.

**Do NOT commit to git** (the sessions are working artifacts, not the canonical corpus).

## The seed (what's on disk, for reference)

- **Method source:** `research-library/pushing/_source/` — logicvidsmethod (the two loops + three
  reliability levels + three passes), logicframework (the 6-level frame), logicframework2,
  logicdog (licensed-vs-not, the relabelling accusation), logic5/6/7 + logicvid3 (worked penetrations),
  PUSHING-TANTRALOKA, PUSHING-IPVV.
- **Formal guide:** `research-library/pushing/PUSHING_GUIDE.md` — the full how-to.
- **The DNA questionnaire:** `research-library/pushing/QUESTIONNAIRE_REAL_DNA.md` — the CORE shapes +
  the empirical Śaiva Q1–Q25.
- **Worked sessions:** `research-library/recognition/pushing-tantraloka/LOGICVID-session-*.md` (30+) +
  `recognition/pushing-ipvv/`.
- **The hub:** `data/corpus/hub.ts` tracks `pt:hub:ipvv:pushing:main` and `pt:hub:tantraloka:pushing:main`.

Read the relevant source files before pushing — the method is in them; this skill encodes it.
