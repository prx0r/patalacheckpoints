# Pāṭala Evidence Policy

*2026-08-10. How the translator reasons with evidence. Separate from the voice (`STYLE_GUIDE.md`), the data shape (`TRANSLATION_SCHEMA.md`), and the workflow (`REVIEW_PROTOCOL.md`). `TRANSLATION_SKILL.md` is the compiled instruction that references this.*

---

## 1. Base text vs textual evidence (the corrected hierarchy)

A critical edition and a manuscript are **different kinds of object, not quality levels**. Split them:

```text
BASE TEXT
  The explicitly chosen text from which this translation is made
  (a critical edition, or an e-text, or a manuscript — whatever is chosen).

TEXTUAL EVIDENCE
  1. the apparatus of the base edition
  2. manuscript witnesses
  3. other scholarly editions
  4. trustworthy transcriptions / e-texts
```

If the edition's reading at a locus is doubtful, an older manuscript is **evidence against it** — not automatically a lower-grade source. Record which you chose and why (`base` + `textual_variant_notes`).

## 2. Interpretive evidence (separate from textual)

```text
INTERPRETIVE EVIDENCE
  1. grammar of the present passage
  2. usage elsewhere in the same work
  3. explicit commentary on the passage
  4. direct textual parallels / quotations
  5. same author
  6. closely related textual tradition
  7. same historical milieu
  8. wider tantric Sanskrit
  9. general Sanskrit lexical evidence
```

## 3. The core rule (elevated)

> **Nothing overrides the grammar of the current passage merely because another text uses the word differently.**

A parallel, a commentary, or a school-usage can *constrain* or *suggest*, but the present passage's own syntax and morphology come first. If a parallel conflicts with the grammar of the locus, flag the conflict (`parallel_conflict`); do not bend the grammar.

## 4. Retrieval must not be over-claimed

The MCP exposes `search_surface_occurrences` — **substring search**, `lemmatized: false`. It does NOT do morphological or lemma retrieval. Never treat a substring hit as a lemma occurrence; Sanskrit inflects (`śakti / śaktiḥ / śaktim / śaktyā / śakteḥ` are not interchangeable for a raw concordance). Lemma retrieval (`find_lemma_occurrences`) is a later, distinct capability.

## 5. Term proposals vs accepted senses — no self-contamination

Machine-generated senses must never promote themselves into accepted corpus knowledge:

```text
data/terms.json           = ACCEPTED term data (only review promotes here)
data/term_proposals.jsonl = MACHINE/HUMAN proposals (proposed, never auto-accepted)
```

A translation emits:

```json
{
  "lemma": "krama",
  "proposed_sense": "ordered succession",
  "evidence": ["..."],
  "status": "proposed"
}
```

Only a human review event promotes: `proposed → reviewed → accepted`. This prevents the feedback loop where an LLM's guess becomes "established usage" by being retrieved as precedent.

## 6. Copyright boundaries on existing translations

The MCP must not silently dump copyrighted commercial translations into the model context. For a published (non-open) translation, return:

```json
{
  "translator": "X",
  "coverage": "3.1-3.20",
  "access": "external",
  "full_text_available_to_mcp": false,
  "resource_id": "..."
}
```

Only public-domain / openly-licensed translations may be fully retrieved, per their licence. **Our own working translations are fine** (they are ours). This is recorded in the `rights` field of the work/edition.

## 7. Retrieval ranking (for context selection)

```text
1. same work
2. direct textual relative   (from relations: quoted-by / borrows-from / commentary)
3. same author
4. same tradition
5. adjacent tradition
6. same date range
7. wider tantric corpus
```

`research_roles` (e.g. `synthesis`, `primary_scripture`, `translation_target`, `terminology_anchor`) further separates function from tradition membership — a later commentary and a root Tantra are not weighted equally just because they share a school tag.
