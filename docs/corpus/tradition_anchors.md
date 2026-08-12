# Tradition Anchors & The Semantic Frame — the guiding layer

*Built from the canonical reference map (`corpus/targets/canonical_reference_map.md`). This is how we stop translating randomly: every batch is placed in a tradition, every tradition has anchors (published translations + digital texts we hold), and every term's likely sense is framed by its tradition before we translate. The reference map is the guiding light; this doc is its operational arm.*

---

## 1. The frame: translate by tradition, not by corpus-order alone

The reference map's core claim: these are not six schools but **one network with transfer-nodes** (the Kaula reformulation, Abhinava's Trika synthesis). Consequences for translation:

1. **A term's likely sense is tradition-conditional.** `kula` in a Kubjikā text ≠ `kula` in Abhinava ≠ `kula` in a Yoginī-cult text. Before translating any occurrence, check the dossier for the *tradition you're in* (the reference map's glossary + our `period_glossary_pass1.md`).
2. **Abhinava is a synthesis-node, not a transparent witness.** Earlier scriptures must not be read "because Abhinavagupta says so." When an earlier text uses a term, say: "this is an earlier scriptural use; Abhinava later interprets a related expression as X."
3. **The Dyczkowski-effect caveat:** our corpus is a curated selection. Occurrence-counts measure corpus-representation, not historical influence. Never cite a count as influence.
4. **The ingestion waves** (from the report): Semantic anchors → Krama core → Kubjikā root → Kubjikā expansion → bridges → large syntheses → Sarvāmnāya. The leapfrog map's hops map onto these waves.

---

## 2. The anchor table — what we hold, per tradition

**Anchor = a text with enough control** (published translation, commentary, or stable edition) **to interpret its neighbors.** ✓ = on disk/local · [R2] = in the R2 bucket · [ACQ] = to acquire · — = not available.

### TRIKA (the calibration layer — the Rosetta corpus)
| Text | Sanskrit e-text | English anchor | Notes |
|---|---|---|---|
| Tantrāloka + Jayaratha | ✓ GRETIL (gretil_tantraloka.txt) | ✓ **Dyczkowski 11 vols** [R2] + Tantrasāra GRETIL | the doctrinal oracle |
| Spandakārikā | ✓ (via the bundle) | ✓ **Dyczkowski, Stanzas on Vibration** [R2] | 4 commentaries on disk |
| Vijñānabhairava | ✓ (muktabodha + CP2 work) | ✓ Lakshmanjoo-aligned (our CP2) | 162 vv, done |
| Mālinīvijayottaratantra | ✓ M00160 | — [ACQ: no published full transl.] | the report's A+ Trika scripture |
| Parātriṃśikā + Abhinava | ✓ M00042–44, M00154, M00215 | — [ACQ: Jaideva Singh's transl.] | the phonemic bridge |
| Īśvarapratyabhijñā + Vimarśinī (3 vols) | ✓ M00019–22 | — [ACQ: Torella] | the pramāṇa-language |
| Śivadṛṣṭi (Somānanda) | ✓ (library) | — [ACQ: Nemec] | proto-Pratyabhijñā |
| Tantrasadbhāva / Siddhayogeśvarīmata | [verify library] | — | the early Trika strata |
| Śivasūtra complex | ✓ | ✓ Dyczkowski's Aphorisms [R2] | anchored, T3'd |

### KRAMA / KĀLĪKULA (the first leap — the cognition-sequence tradition)
| Text | Sanskrit e-text | English anchor | Notes |
|---|---|---|---|
| Mahānayaprakāśa | ✓ M00033/M00034 | — [ACQ] | the crown, Hop 3 |
| Mahārthamañjarī | ✓ M00035 | — | Krama theology |
| Devīpañcaśataka / Kālīkulapañcaśatikā | [verify — not found in local list] | — [ACQ] | one of Sanderson's 2 Krama prototypes |
| Kramasadbhāva | [verify — not on GRETIL/local] | — [ACQ] | the other Krama prototype |
| Kālīkulakramārcana | — [R2?] | — | Vimalaprabodha, 1002 CE |
| Mahāguhyakālīvidhāna | ✓ M00516/M04003 | — | the Guhyakālī practical layer |
| Nityākaulatantra | ✓ M00316 | — | Dyczkowski-documented fragment (done) |

### KUBJIKĀ / PAŚCIMĀMNĀYA (the specialist corpus — Western Transmission)
| Text | Sanskrit e-text | English anchor | Notes |
|---|---|---|---|
| **Kubjikāmata (KMT)** | ✓ **GRETIL (Goudriaan–Schoterman) — saved `gretil2/raw_kubjikamata.txt`** | — [ACQ: Dyczkowski's study] | the A+ root text, 25 paṭalas, verse-stable |
| Kubjikātantra | ✓ M00030 | — | 17 paṭalas T1'd (ours) |
| Kubjikā liturgy (pūjā, dīkṣā, gurumaṇḍala) | ✓ M00547–51 | — | the ritual layer |
| Ṣaṭsāhasrasaṃhitā | [verify] | — | the expansion |
| Śrīmatottara | — [ACQ] | — | the KMT expansion |
| Ciñciṇīmatasārasamuccaya | — [ACQ] | — | the A+ bridge text |
| Manthānabhairavatantra | ✓ (library) + ✓ **Dyczkowski Kumārikākhaṇḍa** [R2] | ✓ Dyczkowski's edition [R2] | 22k ślokas — B (huge) |

### KAULA (the bundle — what we've been translating)
| Text | Sanskrit e-text | English anchor | Notes |
|---|---|---|---|
| Kaulajñānanirṇaya | ✓ M00027 | ✓ Bagchi 1934 print (round2) | T3'd, the bundle's anchor |
| Akulavīratantra | ✓ M00003 | ✓ archive.org translation | T3'd (1–18) |
| Kulānanda + Chandrikā | ✓ M00513 + print | the Chandrikā (OCR-pending) | T1'd |
| Kulārṇavatantra | ✓ M00031 | — [ACQ: published transl. exists] | the kula-manual's intertext |
| Kaularahasya / Kulapradīpa / Kulālaśāstra / Kaulārcanadīpikā / Kuladīpikā | ✓ all | — | our Hop-1 openings |

### SPANDA / PRATYABHIJÑĀ (the philosophical control corpus — runs alongside)
| Text | Sanskrit e-text | English anchor | Notes |
|---|---|---|---|
| Spandakārikā + 4 commentaries | ✓ | ✓ Dyczkowski (Stanzas) [R2] | the control |
| Ajaḍapramātṛsiddhi / Īśvarasiddhi | ✓ M00502/M00658, M00023/M00660 | — | the Siddhitrayī, pre-pipeline translated |
| Vākyapadīya (Bhartṛhari) | ✓ GRETIL | ✓ (translation in library) | the synthesis-antecedent |
| Nyāyasūtra / Tattvacintāmaṇi | ✓ GRETIL (gretil2) | ✓ Jhā (round2) | Hop 10's Nyāya layer |

### SARVĀMNĀYA / NEWAR (the endgame synthesis)
| Text | Sanskrit e-text | English anchor | Notes |
|---|---|---|---|
| Newar paddhatis (Siddhalakṣmī, Guhyakālī, Kālīkrama...) | [R2: mbt + the manuscript reservoir] | — | the C→A layer, later |

---

## 3. The GitHub/digital resources per tradition (the refs to use)

| Resource | What it gives | Use for |
|---|---|---|
| GRETIL (`gretil.sub.uni-goettingen.de`) | machine-readable editions: KMT, TĀ, Tantrasāra, Vākyapadīya | the verse-stable Sanskrit anchors (KMT now saved) |
| Muktabodha (local `sources/muktabodha-lib/`) | 500 e-texts, Dyczkowski-curated | the corpus; most traditions covered |
| **Ambuda / Vidyut** (`github.com/ambuda-org`) | Pāṇinian morphology, TEI ingestion | the future `[G]`-referee + the reader UI |
| **DCS / Oliver Hellwig** (`github.com/OliverHellwig/sanskrit`) | lemmatized GRETIL, sandhi-split | lemma-level search when we need it |
| **Cologne Sanskrit Lexicon** (`github.com/sanskrit-lexicon`) | MW/Apte machine-readable | the dictionary baseline (not the tantric senses) |
| **SARIT** (`sarit.github.io`) | TEI critical-edition schema | the edition layer later |
| **FoJin** (`github.com/xr843/fojin`) | deterministic citation-guards, trust-states, URN model | the audit-layer design (our `audit_t1.py`'s model) |
| **Bilara** (`github.com/suttacentral/bilara`) | the segment-ID translation model | the reader's data model |
| **Mitrasaṃgraha** (arXiv 2601.07314) | 391k Skt→Eng bitext | potential MT baseline, later |
| archive.org | the Bagchi 1934, the Akulavīra translation, the prints | the [X]-collation referee |

**The rule for these links:** use them as *referees*, not builders. Vidyut checks our grammar; Cologne gives the dictionary baseline; GRETIL gives independent editions; FoJin gives the trust-guard design. **None of them provides the tantric technical-semantic layer** — that's ours (the concordance + the dossiers).

---

## 4. What the anchor-map changes in the leapfrog

1. **The batch order becomes tradition-aware.** When a hop's batch begins, consult this table first: what anchors does this tradition have? If it has an anchor (the bundle's Bagchi, the KMT's GRETIL, the TĀ's Dyczkowski), the R2 can run the three-way check. If not, the [X]-rate rises honestly.
2. **The Kubjikā hop (Hop 2) is now unblocked.** The KMT GRETIL anchor is saved — the report's A+ root text. The next Kubjikā work (the KMT itself, or the Kubjikātantra's T2/T3) can cite it.
3. **The acquisition list is now tradition-ordered** (from the report + this table): Trika → Torella (ĪPK), Jaideva Singh (Parātriṃśikā), Nemec (Śivadṛṣṭi); Krama → Devīpañcaśataka/Kramasadbhāva texts; Kubjikā → Dyczkowski's KMT study, Śrīmatottara, Ciñciṇīmata; Kaula → the Kulārṇava translation.
4. **The dossiers drive the sense-choices.** The 24-lemma list from the report is the dossier backlog; each batch dossiers the lemmas it touches, with both our corpus attestations AND the report's scholarly senses.

---

## 5. The immediate next batch (tradition-aware)

Given the anchors now held, the highest-value tradition-aware next moves:

| Option | Tradition | Anchor available? | Why |
|---|---|---|---|
| **Kubjikāmata opening T1** (the KMT's paṭala 1) | Kubjikā | ✓ GRETIL (verse-stable) | the report's A+ root; the Kubjikā-hop's on-ramp; the new GRETIL anchor makes it the ideal next T1 |
| **Kaularahasya 4–24 continuation** | Kaula | — (bundle-internal) | continues the open Hop-1 batch, no new anchor |
| **Kubjikātantra T2/R2/T3** | Kubjikā | ✓ the KMT-adjacent (our own T1 + the GRETIL KMT) | completes the flow for our 17-paṭala text |
| **Kulapradīpa prakāśas 2–7** | Kaula | the Kulārṇava-intertext ✓ | continues the kula-manual batch |
| **Mahānayaprakāśa opening** | Krama | — [ACQ] | the crown (Hop 3), highest value, hardest |

**Recommendation:** start the **Kubjikāmata paṭala 1 T1** — it's the report's #1 A+ text, the GRETIL anchor is freshly saved, and it makes the Kubjikā-hop real instead of speculative. Its term-frames (kula, akula, śakti, mālinī, khecarī) are all in the report's dossiers, so the translation is tradition-guided from the first verse.
