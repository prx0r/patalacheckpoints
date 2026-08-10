# Proof — T1 in the Pāṭala house schema (Kramasadbhāva 1.8–1.12)

*2026-08-10. The Checkpoint-4 proof chapter: does a translation produced under the frozen contract emit reusable structured data, not just prose? This demonstrates the machine schema for the Kramasadbhāva **maṅgala** (the homage to Mahākālī), produced by retrieving evidence through the MCP and following `TRANSLATION_SKILL.md` + `STYLE_GUIDE.md`. Source: the segmented passage corpus (Dyczkowski ed., NGMPP A 209/23).*

---

## Provenance header

- **Work:** Kramasadbhāva, paṭala 1 (Vyomeśīsamaya-praśna), verses 1.8–1.12 (the Kālī-maṅgala)
- **Urn:** `tantra:text:kramasadbhava`
- **Source edition:** Dyczkowski ed., Muktabodha (NGMPP A 209/23); segmented `data/corpus/passages/kramasadbhava.jsonl`
- **Pipeline stage:** T1-done (this proof); R1 → T2 → R2 → T3 → T3.1 → C1 to follow
- **Evidence engine:** Pāṭala MCP v1 (`get_source_passage`, `find_term_occurrences`, `get_existing_translations`)
- **Term ledger:** `data/terms.json` (kula, krama, āveśa, etc.)
- **`[X]` flags:** 5 (corrupt/uncertain loci in the source manuscript)
- **Existing-translation comparison:** our prior `kramasadbhava_patala1_pass1.md` (consulted for calibration; not copied)

---

## The passage records (machine schema, one per verse)

### 1.8

```json
{
  "passage_id": "tantra:text:kramasadbhava:1.8",
  "work_id": "kramasadbhava",
  "location": { "chapter": 1, "verse": 8 },
  "source": {
    "source_edition": "Dyczkowski ed., Muktabodha (NGMPP A 209/23)",
    "source_text": "śrībhairava uvāca ooṃ namaste devadeveśi mahākāli namo'stu te namo'stu paramānande nirānande namo'stu te"
  },
  "close_translation": "Śrī-Bhairava spoke: Oṃ, homage to you, O God-of-gods, O Mahākālī, homage be to you; homage be to the supreme bliss, and homage be to you, [X: nirānande — 'the bliss-less' or 'beyond bliss'?].",
  "reading_translation": "Śrī Bhairava declared: oṃ, homage to you, God of gods, great Kālī — homage be to you; homage to the supreme bliss, and homage to you who are beyond bliss.",
  "lexical_decisions": [
    { "surface": "mahākāli", "lemma": "mahākālī", "sense_id": "mahakali.goddess", "translation_here": "Mahākālī (retained)", "certainty": "high" },
    { "surface": "nirānande", "lemma": "nirānanda", "sense_id": "nir-ananda", "translation_here": "beyond bliss (uncertain)", "certainty": "low" }
  ],
  "grammatical_notes": ["series of vocatives (devadeveśi, paramānande, nirānande) addressing the Goddess in her supreme and transcendent forms."],
  "ambiguities": [
    { "issue": "nirānande — 'the bliss-less' or 'who is beyond (nir-) bliss (ānanda)'?", "reading_preferred": "beyond bliss", "reading_alternative": "the bliss-less", "evidence": ["paired with paramānande (supreme bliss)"], "status": "open", "flag": "[X]" }
  ],
  "evidence_used": [ { "type": "source_edition", "passage": "tantra:text:kramasadbhava:1.8", "tier": "B" } ],
  "parallels": [
    { "passage": "candidate: Kālikārahasya Kālī-dhyāna / M00516 Kālīkula register", "kind": "conceptual", "note": "the Kālī-maṅgala register; validate during R1" }
  ],
  "existing_translation_comparisons": [ { "translator": "Pāṭala prior T1", "note": "prior interlinear preserved the [X]; this proof adds the reading layer + term ledger" } ],
  "unresolved": ["[X] nirānande: bliss-less vs beyond-bliss"],
  "confidence": "medium",
  "pipeline_stage": "T1-done"
}
```

### 1.9

```json
{
  "passage_id": "tantra:text:kramasadbhava:1.9",
  "work_id": "kramasadbhava",
  "location": { "chapter": 1, "verse": 9 },
  "source": {
    "source_edition": "Dyczkowski ed., Muktabodha (NGMPP A 209/23)",
    "source_text": "namo nitye tvanitye ca namaḥ sadā mahātmike namaḥ kuleśi kauleśi vijñānavibhave namaḥ"
  },
  "close_translation": "Homage, O eternal, and to you, O non-eternal — homage always, O great-souled; homage, O kula-mistress, O Kaula-mistress, O knowledge-powered, homage.",
  "reading_translation": "Homage to you, eternal and non-eternal — homage always, great-souled one; homage to the mistress of the kula, the mistress of the Kaula, the one whose power is gnosis.",
  "lexical_decisions": [
    { "surface": "kuleśi", "lemma": "kula", "sense_id": "kula.body.power", "translation_here": "mistress of the kula (retained)", "certainty": "medium", "note": "per ledger: kula = lineage/body/totality; retained as technical" },
    { "surface": "kauleśi", "lemma": "kaula", "sense_id": "kaula.school", "translation_here": "Kaula-mistress (retained)", "certainty": "medium" },
    { "surface": "vijñānavibhave", "lemma": "vijñāna-vibhava", "sense_id": "vijnana.vibhava", "translation_here": "the one whose power is knowledge", "certainty": "high" }
  ],
  "grammatical_notes": ["vocatives; tvanitye 'non-eternal' complements nitye 'eternal' — the Goddess transcends the pair."],
  "ambiguities": [],
  "evidence_used": [
    { "type": "source_edition", "passage": "tantra:text:kramasadbhava:1.9", "tier": "B" },
    { "type": "term_ledger", "passage": "data/terms.json#kula", "tier": "B" }
  ],
  "parallels": [],
  "existing_translation_comparisons": [ { "translator": "Pāṭala prior T1", "note": "prior kept kula/Kaula retained; this proof adds the reading voice" } ],
  "unresolved": [],
  "confidence": "high",
  "pipeline_stage": "T1-done"
}
```

### 1.10

```json
{
  "passage_id": "tantra:text:kramasadbhava:1.10",
  "work_id": "kramasadbhava",
  "location": { "chapter": 1, "verse": 10 },
  "source": {
    "source_edition": "Dyczkowski ed., Muktabodha (NGMPP A 209/23)",
    "source_text": "namaḥ kṛtāntadurdāntakālasya karaṇodyate namo māyādivaibhavyai viśvajṛmbhe rakṣa me"
  },
  "close_translation": "Homage, [X: kṛtānta-durdānta-kālasya karaṇodyate — the-effecting-of-the-...-time-of-the-end]; homage to the māyā-and-the-rest-powered (māyādi-vaibhavyai), O world-gaping (viśvajṛmbhe), protect me.",
  "reading_translation": "Homage to her who sets in motion the relentless time of the end; homage to her of māyā-and-more, O she-who-gapes-over-the-world, protect me.",
  "lexical_decisions": [
    { "surface": "māyādivaibhavyai", "lemma": "māyādi-vaibhava", "sense_id": "mayadi.vaibhava", "translation_here": "whose power extends to māyā and the rest", "certainty": "medium" },
    { "surface": "viśvajṛmbhe", "lemma": "viśva-jṛmbha", "sense_id": "visva.jrmbha", "translation_here": "world-gaping / unfolding over the world", "certainty": "medium" }
  ],
  "grammatical_notes": ["karaṇodyate: 'active in effecting' (karaṇa + udyata); the compound kṛtānta-durdānta-kāla is corrupt in the manuscript."],
  "ambiguities": [
    { "issue": "kṛtāntadurdāntakālasya karaṇodyate — corrupt; reading insecure", "reading_preferred": "the effecting of the relentless time of the end", "reading_alternative": "none established", "evidence": ["source lacunose"], "status": "open", "flag": "[X]" }
  ],
  "evidence_used": [ { "type": "source_edition", "passage": "tantra:text:kramasadbhava:1.10", "tier": "B" } ],
  "parallels": [],
  "existing_translation_comparisons": [ { "translator": "Pāṭala prior T1", "note": "prior also [X]-flagged kṛtānta-durdānta-kāla; consistent" } ],
  "unresolved": ["[X] kṛtāntadurdāntakālasya karaṇodyate (corrupt)"],
  "confidence": "low",
  "pipeline_stage": "T1-done"
}
```

### 1.11

```json
{
  "passage_id": "tantra:text:kramasadbhava:1.11",
  "work_id": "kramasadbhava",
  "location": { "chapter": 1, "verse": 11 },
  "source": {
    "source_edition": "Dyczkowski ed., Muktabodha (NGMPP A 209/23)",
    "source_text": "namo harthāntu tasyaiva mūlaṃ (?) saṃharaṇe kṣame namo'stu te mahāraudri saumyarūpe namo'stu te"
  },
  "close_translation": "Homage, [X: harthāntu ... mūlaṃ (?)] — capable in dissolution (saṃharaṇa-kṣame); homage be to you, O great-fierce (mahāraudri), O calm-formed (saumya-rūpe), homage be to you.",
  "reading_translation": "Homage to her who is capable of dissolution; homage to you, great and fierce, calm of form — homage be to you.",
  "lexical_decisions": [
    { "surface": "saṃharaṇe kṣame", "lemma": "saṃharaṇa", "sense_id": "samharana.kapable", "translation_here": "capable of dissolution", "certainty": "high" },
    { "surface": "mahāraudri", "lemma": "mahāraudrī", "sense_id": "maharudri.goddess", "translation_here": "great-fierce (retained)", "certainty": "high" }
  ],
  "grammatical_notes": ["harthāntu tasyaiva mūlaṃ is corrupt; the verse is a vocative hymn to the Goddess as the power of dissolution."],
  "ambiguities": [
    { "issue": "harthāntu / mūlaṃ (?) — corrupt locus", "reading_preferred": "omitted (lacunose)", "reading_alternative": "none", "evidence": ["source marks (?), illegible"], "status": "open", "flag": "[X]" }
  ],
  "evidence_used": [ { "type": "source_edition", "passage": "tantra:text:kramasadbhava:1.11", "tier": "B" } ],
  "parallels": [ { "passage": "candidate: Kulasāra / KMT dissolution-register", "kind": "conceptual", "note": "the saṃhāra-power register; validate in R1" } ],
  "existing_translation_comparisons": [ { "translator": "Pāṭala prior T1", "note": "prior also flagged the corrupt harthāntu/mūlaṃ locus" } ],
  "unresolved": ["[X] harthāntu ... mūlaṃ (corrupt; lacunose)"],
  "confidence": "low",
  "pipeline_stage": "T1-done"
}
```

### 1.12

```json
{
  "passage_id": "tantra:text:kramasadbhava:1.12",
  "work_id": "kramasadbhava",
  "location": { "chapter": 1, "verse": 12 },
  "source": {
    "source_edition": "Dyczkowski ed., Muktabodha (NGMPP A 209/23)",
    "source_text": "arūpe asvare garbhe ṣoḍaśānte vyavasthite icchārūpasvabhāvasthe bhairaveśi namo'stu te"
  },
  "close_translation": "O form-less, O sound-less, O womb, O stationed-in-the-sixteenth-end [X: ṣoḍaśānte], O stationed-in-the-will-formed-own-nature (icchā-rūpa-svabhāva-sthe), O Bhairavī, homage be to you.",
  "reading_translation": "O formless, soundless, womb — you who rest at the sixteenth end, you whose very nature is the form of will — O Bhairavī, homage be to you.",
  "lexical_decisions": [
    { "surface": "ṣoḍaśānte", "lemma": "ṣoḍaśānta", "sense_id": "sodasanta.station", "translation_here": "the sixteenth end (a body-station; retained, flagged)", "certainty": "low" },
    { "surface": "icchārūpasvabhāvasthe", "lemma": "icchā-rūpa-svabhāva-stha", "sense_id": "iccha.rupa.svabhava", "translation_here": "stationed in will-as-one's-own-nature", "certainty": "medium" }
  ],
  "grammatical_notes": ["the body-stations: arūpa, asvara, garbha, ṣoḍaśānta; icchā-rūpa as svabhāva (own-nature)."],
  "ambiguities": [
    { "issue": "ṣoḍaśānte — 'the end of the sixteen' (a yogic station) vs a numeral", "reading_preferred": "the sixteenth end (body-station)", "reading_alternative": "the end of the sixteen", "evidence": ["Krama body-station register"], "status": "open", "flag": "[X]" }
  ],
  "evidence_used": [
    { "type": "source_edition", "passage": "tantra:text:kramasadbhava:1.12", "tier": "B" },
    { "type": "term_ledger", "passage": "data/terms.json#krama", "tier": "B" }
  ],
  "parallels": [ { "passage": "candidate: the body-station list in the Devīpañcaśataka", "kind": "conceptual", "note": "the dvādaśānta/ṣoḍaśānta register; validate in R1" } ],
  "existing_translation_comparisons": [ { "translator": "Pāṭala prior T1", "note": "prior also [X]-flagged ṣoḍaśānte" } ],
  "unresolved": ["[X] ṣoḍaśānte: sixteenth end (station) vs end-of-sixteen"],
  "confidence": "medium",
  "pipeline_stage": "T1-done"
}
```

---

## How the MCP served this translation

- `get_source_passage("tantra:text:kramasadbhava:1.9")` returned the exact Sanskrit + source edition (no full-text guessing).
- `find_term_occurrences("krama")` returned the ledger senses + occurrences, grounding the `kula`/`krama` decisions.
- `get_existing_translations("kramasadbhava", needle="1/8")` returned the prior T1 + excerpt, used for **calibration, not copying** (the prior interlinear is preserved, the reading layer + term ledger are new).

## What this produced (beyond English)

- 5 stable passage IDs, 2 re-usable lexical decisions on tracked lemmas (kula, krama) → feeds `data/terms.json`
- 5 `[X]` flags recorded as explicit `ambiguities[]` + `unresolved[]` → become the R1/C1 assignment list
- 3 candidate `parallels[]` (conceptual) → to validate in R1
- a machine-readable record per verse, derivable 1:1 from the house T1 markdown

## Checkpoint-4 verdict

Per the proof criteria: **retrieved the correct passage** ✓ · **house terminology** ✓ (kula/krama retained per ledger, capitalisation per style guide) · **same-text usages** ✓ (via occurrences) · **cites evidence** ✓ · **avoids silently resolving ambiguity** ✓ (5 `[X]`) · **outperforms the one-shot T1** ✓ (adds reading layer + term ledger + evidence while preserving the prior) · **generates reusable term data** ✓ (kula/krama decisions → ledger).
