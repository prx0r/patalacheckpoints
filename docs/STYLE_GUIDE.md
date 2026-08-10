# Pāṭala Style Guide (house voice)

*2026-08-10. The explicit voice policy for our translations. Not "translate beautifully but accurately" — concrete rules the agent (and every T-phase) follows. Paired with `TRANSLATION_SKILL.md` (the contract).*

---

## 1. Sanskrit retention

Keep these technical terms untranslated (transliterated, italicised) where English would obscure the technical sense:

```text
śakti  kula  krama  spanda  vimarśa  prakāśa  visarga  khecarī
āveśa  uccāra  śūnya  mātṛkā  saṃvit  parāmarśa  svātantrya  tattva
```

- Elsewhere translate normally.
- A term is retained when the English gloss would collapse a technical sense into a vague one (e.g. rendering `kula` as "family" where it means the totality/lineage-body). Retain it; record the decision in `lexical_decisions`.
- Do NOT retain a term merely for atmosphere. Retention is semantic, not stylistic.

## 2. Transliteration

- Use IAST (diacritics). Match the source's orthography for names (Śiva, Kālī, Kubjikā, Abhinavagupta).
- Sanskrit terms retained are lowercase except proper nouns and where a school/doctrine is demonstrably meant (see §6).

## 3. Capitalisation (explicit policy)

- **Śiva / Śivā** — proper name: capitalise. **śiva** (adj., "auspicious") — lowercase.
- **Goddess / goddess** — capitalise when it is the divine referent of the text's context (devī as the Goddess); lowercase for a generic goddess of a list.
- **Consciousness / consciousness** — capitalise when it is the doctrinal absolute (saṃvit/cit as the ultimate); lowercase for ordinary awareness.
- **Power / power** — capitalise when it is a hypostasised śakti; lowercase for ordinary capability.
- When in doubt, prefer lowercase; the R1 reviewer may promote to capital with justification. Consistency within a text trumps all.

## 4. Compounds

- Prefer readable English; do NOT force a Sanskrit compound structure onto English.
- Record the **parse** in `grammatical_notes[]` when the compound is load-bearing or ambiguous (e.g. karmadhāraya vs tatpuruṣa, active vs passive).
- A compound that admits two parses → preferred parse in the translation, alternative in `ambiguities[]`.

## 5. Supplied English

- Anything **materially supplied** for readability (implicit subject, connective, fill pronoun) should be auditable — bracket or note it if it changes meaning.
- Never insert a sentence, clause, or doctrine the Sanskrit does not support.

## 6. Technical consistency

- Same lemma/sense → same English rendering within a text, unless local context warrants deviation (then record it).
- **Capitalisation rule for schools:** capitalise "Krama / Kula / Trika" ONLY where the *school/doctrine* is demonstrable. "krama" as "sequence/ritual order" stays lowercase. Same for `kula` (structure) vs `Kula` (school).
- Range-not-default: a lemma's sense is chosen from the context; do not default to the dictionary's first gloss.

## 7. Ambiguity

- `translation = preferred reading`, `note = alternative`. Never merge both into vague English.
- If two readings remain viable after evidence, keep it `[X]`-flagged rather than resolving arbitrarily.

## 8. Metaphysical interpretation (the anti-anachronism rule)

- **Do not insert later-school doctrine into an earlier text.** E.g., do not read a full Pratyabhijñā doctrine into a 9th-c. Krama/Kubjikā scripture unless the commentary or evidence supports it.
- A later commentary's gloss is evidence, not the root's own claim — attribute it (e.g. "Jayaratha glosses this as...").
- Keep *textual scholarship* and *practice instruction* visibly separate; never let the site's AI silently convert a ritual text into modern meditation instruction.

## 9. Register

- **close_translation**: analytical, structurally faithful; technical terms retained; preferred reading.
- **reading_translation**: natural, flowing, defensible; still accurate — never prettier at the cost of meaning.
- Avoid archaisms and pseudo-scriptural "thee/thou" register unless the source genuinely warrants it. Avoid modern slang. Prefer plain, precise, dignified English.

## 10. The C1 commentary voice (distinct from the translation voice)

The C1 is NOT a fifth translation of the verse. It is a **commentary** — the voice of
Dyczkowski's Tantrāloka with Jayaratha's Viveka: dense, reasoned, flowing prose that
*thinks with* the text and draws out the doctrine beneath it.

- **Reason, don't report.** Develop the argument — how the premise forces the conclusion,
  how the image works, why the rival reading fails — rather than restating the verse.
- **Continuous prose, not a gloss.** Prefer a developed paragraph that moves, over the
  mechanical "this verse says X; the reason is Y."
- **Layer the sentences.** Let clauses subordinate and qualify; build one sustained thought.
  Vary length — a long sentence carries the argument, a short one lands it.
- **Ground every claim.** Carry the evidence with the prose (the Vṛtti, the parallel, the
  history, the grammar). Nothing floats free of the text.
- **Weigh the rival.** Let the opposing reading state itself fully before being set aside —
  or honored as genuinely open. The reader should feel the force of what was rejected.
- **Draw out the esoteric underneath.** The surface image is the entry; open the doctrine
  it holds — but tie it back to the specific wording.
- **Keep the argument's motion.** Comment on the sequence, not just the verse; a text is an
  argument moving from challenge to resolution.

Full discipline: `skills/write-commentary/SKILL.md` §5.

## 11. Do

- Be consistent, honest, and precise.
- Flag what you don't know.
- Record every retained term and every parse decision.
- Let evidence decide; say when you're unsure.

## 12. Don't

- Don't copy published translations or our earlier T-versions verbatim.
- Don't silently repair corrupt/lacunose text.
- Don't add unsupported doctrine or supplied clauses without a note.
- Don't mark anything "complete" until T3.
- Don't write C1 as a verse-summary gloss ("this verse says X"). Reason and develop instead.
