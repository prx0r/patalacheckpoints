# Pāṭala Review Protocol

*2026-08-10. The workflow: pipeline stages, the independent-first-pass rule, review events, and how term proposals are promoted. Policy in `STYLE_GUIDE.md` + `EVIDENCE_POLICY.md`; data shape in `TRANSLATION_SCHEMA.md`.*

## 1. The pipeline (semantically distinct stages)

```text
T0   machine draft — disposable, never published
T1   evidence-bearing working translation — eligible_for_review
R1   human editorial pass (first review of T1)
T2   human-corrected scholarly working translation
R2   specialist / domain review
T3   stable scholarly release
T3.1 public reader edition (derived from T3; updates in lock-step)
C1   commentary / public explanation (independent research; may overturn)
```

- **T1 is NOT called "publishable."** Use `eligible_for_review`. If shown publicly at all, it carries a large **WORKING / AI-ASSISTED** banner.
- **T3.1 is derived from T3**, never independent — a change to T3 regenerates T3.1.

## 2. The independent-first-pass rule (anti-anchoring)

Do NOT consult published/other translations during the initial pass:

### Pass A — independent draft
The translator has: base text, grammar, same-work usage, the term ledger, related primary texts, commentaries. It produces and **freezes** `draft_A` (close + reader_draft).

### Pass B — translation comparison
*Only then* retrieve Dyczkowski / Singh / Vasudeva / etc. and record:

```text
Our initial reading:    X
Published translator:   Y
After comparison:       retained X  /  changed to Z
Reason:                 ...
```

### Corroboration, not independence
> Agreement with a published translation is **corroborative** evidence, but does **not independently establish** the reading.

The old line "independent coincidence is hard-core evidence" is retired: if you've looked at the translation, agreement is not independent.

## 3. Requirement wording (where no translation exists)

Not "existing translations consulted" as a hard requirement. Instead:

> All known accessible relevant translations were **checked for availability**; those actually consulted are recorded.

Some works genuinely have none, and copyright/access may prevent consultation.

## 4. Review events (append-only, decision-addressed)

```json
{
  "id": "pt:review:kubjikamata:1.1:lex:01:v2",
  "passage_id": "tantra:text:kubjikamata:1.1",
  "decision_id": "pt:decision:kubjikamata:1.1:lex:01",
  "reviewer": { "kind": "human", "identifier": "scholar-x" },
  "finding": "kula should not be rendered 'family' here",
  "type": "terminology",
  "suggested": "kula (retained)",
  "evidence": ["Tantrasadbhāva 4.7", "Tantrāloka 29.23"],
  "status": "accepted",
  "created_at": "..."
}
```

Badges derived from review history: `WORKING (AI-assisted)` → `HUMAN REVIEWED (1 reviewer)` → `SCHOLAR REVIEWED (2 domain specialists)` → `EDITORIALLY STABLE`.

## 5. Term proposal promotion

`terms.json` is **accepted** data; `term_proposals.jsonl` is proposals. Only a human review event promotes:

```text
proposed → reviewed → accepted
```

A translation that uses an accepted sense links `sense_id`. A translation that needs a new sense emits a `term_sense_proposal` (never writes to `terms.json` directly).

## 6. The publishable gate (renamed: eligible_for_review)

A T1 is `eligible_for_review` when ALL hold:
- [ ] base source identified; provenance header present
- [ ] close_translation + reader_draft present
- [ ] technical/ambiguous items resolved with evidence OR typed-flagged
- [ ] audit checklist run; no silent omissions/additions
- [ ] Pass A done before Pass B; comparisons recorded (not copied)
- [ ] term decisions either link an accepted sense or emit a proposal
- [ ] assessment recorded per dimension

## 7. Audit checklist (per translation)

- **Negation** — no omitted/added `na`/`mā`
- **Numbers** — counts/arithmetic preserved
- **Omission** — nothing silently dropped
- **Addition** — no English concept without Sanskrit support (→ `SUP`/`editorial_notes`)
- **Term drift** — same sense rendered consistently; deviations recorded
- **Grammar** — parse defensible; alternatives flagged
- **Parallel conflict** — a rendering contradicting a cited parallel is flagged for review
