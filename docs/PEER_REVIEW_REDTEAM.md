# Pipeline Peer Review — Red-Team Response

*2026-08-10. The translation pipeline was red-teamed against FoJin, SuttaCentral/
Bilara, BDRC/BUDA, SARIT, OpenPecha and 84000. This records the verdict and the
decisions taken. Full original review preserved in context; this is the actionable
response.*

## The verdict

> The stack is directionally excellent. The biggest change recommended is to move
> from "one big per-passage translation blob" toward **independent, addressable
> annotations over addressable source objects**, with evidence links, review
> events and versions. The T1 JSON we designed becomes a *projection*, not the
> deepest source of truth.

Strong external validation: **OpenPecha is independently converging on almost
exactly our architecture** (base text + stand-off annotation layers, annotations
on annotations). Bilara validates stable segment IDs + independent cognate layers.
BDRC validates Work ≠ Instance. SARIT points to future TEI interop. 84000 validates
the translation-memory/glossary discipline and the "AI produces leverage, expert
adjudication produces authority" moat.

## The 4 data-model changes recommended

1. **Passage is doing too much.** Separate `CanonicalPassage` (abstract location,
   `tk:kramasadbhava:1.14`) from `SourceSpan[]` (how it appears in each edition/MS).
   Tantric manuscripts won't segment identically. → adopted as invariant 2.
2. **Don't anchor interpretive decisions to character offsets.** Anchor to a
   semantic id (`passage_id + token/lemma occurrence id`), not `chars 21–27`, so the
   sentence can be rewritten without losing the decision. → adopted into `lexical_decisions`
   (they already target a `surface`+`lemma`, not offsets — good).
3. **Translation version and decision version are independent.** `translation v7`
   can *use* stable decisions `D12, D19, D24` without re-creating them. The scholarly
   asset is `source passage + stable interpretive decisions`, not the prose sentence.
4. **Review needs scope + competence.** `review_type ∈ {TEXTUAL, GRAMMATICAL, LEXICAL,
   TRANSLATIONAL, HISTORICAL, DOCTRINAL, READABILITY, MANUSCRIPT}` + reviewer +
   scope + outcome. A Pratyabhijñā expert isn't a paleographer. → adopted.

## The 7 locked invariants

1. Stable IDs never depend on mutable wording.
2. Work ≠ witness ≠ digital representation ≠ canonical passage.
3. Annotations are independent from the base text and independently addressable.
4. Machine output always enters as a proposal, never authority.
5. Every meaningful scholarly judgment can carry evidence and review history.
6. Translation prose and interpretive decisions have independent version histories.
7. Convenient API bundles are projections over normalized scholarly data, not the
   canonical data model.

## Other adoptions

- **Everything important is an annotation/assertion targeting something addressable**
  (translation, lexical decision, grammar, variant, parallel, commentary, term
  occurrence, uncertainty — and annotations-on-annotations: review, correction,
  disagreement, evidence). This unifies what we'd called Assertion/Decision/Ambiguity/
  Review into one extensible pattern (matches `nextdev.md`).
- **Storage ≠ API.** Bundle on read, normalize on write.
- **AI provenance** on every machine object: model family/version, policy/skill
  version, input object ids, retrieval evidence ids, timestamp.
- **status ≠ certainty.** `accepted` + `probable` are separate dimensions. Don't turn
  accepted into fact.
- **Human review isn't inherently gold.** Use origin (machine/human) + status +
  review history, not a naive machine→human→scholar ladder. History beats ontology.
- **84000's outputs:** a serious translation derives glossary, translation memory,
  term concordance, bibliography, commentary candidates and topic dossiers — feeding
  the commentary/research pipeline.
- **Commentary layering** (Bilara's warning): `PASSAGE COMMENT` (short, local) →
  `TOPIC DOSSIER` (multi-passage) → `ESSAY` (full argument). Don't make C1 a 2,000-word
  blob on a verse.

## The one thing FoJin reveals NOT to overbuild

RAG, semantic search, MCP, stable IDs, knowledge graph, AI Q&A are becoming *expected
infrastructure* — FoJin already has them at scale. Our stronger layer is the messy-
historical-evidence one: resolve → structure → propose → expert adjudicate → preserve
judgment. Don't obsess over a fancy RAG stack.
