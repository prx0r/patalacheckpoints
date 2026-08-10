# Pāṭala Translation Schema

*2026-08-10. The data shape for a translation record. Machine schema (JSON); the house T1 markdown maps 1:1. Policy (what/how to translate) is in `STYLE_GUIDE.md` + `EVIDENCE_POLICY.md`; workflow in `REVIEW_PROTOCOL.md`. Versioned `1.0.0`.*

## Core object

```json
{
  "translation_id": "pt:translation:kubjikamata:1.1:v1",
  "passage_id": "tantra:text:kubjikamata:1.1",
  "work_id": "kubjikamata",
  "location": { "chapter": 1, "verse": 1 },
  "version": 1,
  "supersedes": null,
  "derived_from": null,
  "created_by": { "kind": "model", "identifier": "deepseek-v4-flash" },

  "base": {
    "source_edition": "GRETIL (Goudriaan-Schoterman ed.)",
    "source_text": "saṃvartāmaṇḍalānte ..."
  },

  "close_translation": "At the end of the saṃvarta-maṇḍala ...",
  "reader_draft": "At the turning of the great wheel ...",

  "lexical_decisions": [
    {
      "id": "pt:decision:kubjikamata:1.1:lex:01",
      "surface": "kula",
      "lemma": "kula",
      "sense_id": "kula.body.power",
      "translation_here": "kula (retained)",
      "certainty": "medium",
      "proposal": true
    }
  ],

  "grammatical_notes": [],

  "alignments": [
    { "source_span": "saṃvartāmaṇḍalānte", "target_span": "at the end of the saṃvarta-maṇḍala", "type": "direct" },
    { "source_span": null, "target_span": "therefore", "type": "supplied" }
  ],

  "ambiguities": [
    { "id": "pt:decision:kubjikamata:1.1:amb:01", "issue": "...", "reading_preferred": "...", "reading_alternative": "...", "evidence": ["..."], "status": "open", "flag": "LEX" }
  ],

  "assessment": {
    "textual": "secure",
    "grammatical": "secure",
    "lexical": "uncertain",
    "interpretive": "moderate"
  },

  "evidence_used": [
    {
      "resource_id": "pt:resource:gretil-kubjikamata",
      "passage_id": "tantra:text:kubjikamata:1.1",
      "role": "lexical_parallel",
      "relationship": "same_work",
      "supports": "lex:kubjikamata:1.1:lex:01",
      "source_class": "critical_edition",
      "note": "Same construction with ..."
    }
  ],

  "parallels": [
    { "passage": "tantra:text:kubjikamata:1.1", "kind": "conceptual_parallel", "note": "..." }
  ],

  "existing_translation_comparisons": [
    { "translator": "X", "coverage": "1.1", "access": "external", "note": "divergence + reason" }
  ],

  "unresolved": [],
  "editorial_notes": [],
  "policy": {
    "translation_contract": "1.0.0",
    "style_guide": "1.0.0",
    "term_ledger_revision": "abc123"
  },
  "pipeline_stage": "T1",
  "review_status": "eligible_for_review"
}
```

## Field notes (the review-driven changes)

### flags — typed, not one `[X]`
```text
[TXT] textual uncertainty     [GRAM] grammatical ambiguity
[LEX] lexical/sense uncertainty  [DOCT] doctrinal interpretive uncertainty
[WIT] witness disagreement    [SUP] supplied wording (NOT necessarily unresolved)
```
`unresolved[]` contains only genuinely-unresolved flags (TXT/GRAM/LEX/DOCT/WIT). `SUP` goes into `editorial_notes[]` or `alignments` (`type:"supplied"`) — supplied wording is often defensible, not a research problem.

### assessment — not a scalar confidence
Replace `"confidence":"medium"` with per-dimension states derived from flags:
```text
textual / grammatical / lexical / interpretive : secure | ambiguous | uncertain | moderate
```
A UI badge (e.g. `needs_review`) is *derived* from these, never asked from the model.

### decision ids
Every interpretive decision carries `id: "pt:decision:{work}:{loc}:{type}:{n}"` (lex/amb/align/gram...), so review can target `decision lex:01` rather than the whole verse.

### version lineage
`translation_id`, `version`, `supersedes`, `derived_from`, `created_by`. Review is append-only.

### policy version
Every record records which `translation_contract`, `style_guide`, and `term_ledger_revision` it was produced under — so later it is knowable which passages were generated under policy 1.2 vs 2.0.

### parallels taxonomy
```text
exact_quote · probable_quote · adaptation · formulaic_parallel · lexical_parallel · syntactic_parallel · conceptual_parallel
```
(`close` is retired as too ambiguous; the parallel detector will need these.)

### evidence objects
A resource's **quality tier** and its **role in the argument** are separate dimensions. Use `resource_id` + `role` + `source_class` (the resource object carries publisher/author/licence/peer-review/critical-edition flags — don't repeat crude A/B/C tiers inline).

### alignments
```text
alignments[] { source_span, target_span, type: "direct" | "supplied" | "merged" | "split" }
```
Supports later audits ("which English words have no Sanskrit support?"). Word-level alignment is optional per sentence; the structure is present now.

### separation of layers
```text
LemmaOccurrence (factual-ish: surface, lemma candidate, location)
  ↓
LexicalDecision (interpretive: sense, translation, evidence)
  ↓
TermSense (site-wide accepted sense, review-promoted only)
```
Source morphology ≠ translator interpretation ≠ accepted sense.
