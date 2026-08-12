# ŚIVA CORPUS — ACQUISITION TARGETS & DOWNLOAD MANIFEST (the expansion plan)

*2026-08-12. Imported from R2 (`sanskritree/sivatargets`, renamed). The corpus-acquisition companion to
**Vision 11 — Śiva Before Abhinava** (`docs/vision/expansion/vision-11-siva-before-abhinava.md`). An
inventory of **open, legally-available** Śaiva primary Sanskrit + scholarly translations, separated from
piracy mirrors, prioritized by the same braided genealogy (early Mantramārga → Bhairava/Vidyāpīṭha →
Śākta/Kaula/Krama/Trika → Somānanda/Utpaladeva → Abhinavagupta). Ends with a request for a machine-readable
**download manifest** (one row per work: canonical_id, Sanskrit URL, translation URL, format, chapters,
edition, date, citations-in-Abhiava, TRANSLATE/INGEST/MANUSCRIPT status). See `docs/vision/expansion/README.md`
+ `docs/vision/INDEX.md`.*

---

I went back through the list and separated actual open primary material from things that merely circulate on piracy mirrors. The result is better than I expected: a large fraction of the Sanskrit substrate can already be assembled legally in machine-readable form, while the English-translated layer has very specific holes.

This follows the genealogy in your document: not “collect Tantra,” but reconstruct the braided route early Mantramārga → Bhairava/Vidyāpīṭha → Śākta/Kaula/Krama/Trika → Somānanda/Utpaladeva → Abhinavagupta.

One qualification: “all existing translations” can never be guaranteed literally exhaustive because translations hide in articles, dissertations and unpublished working editions. What follows is every substantial freely accessible scholarly translation/edition I could verify, plus important partial translations. I deliberately exclude unauthorized recent-book mirrors.

1. Siddhayogeśvarīmata

Date: approximately 7th century CE; relative dating is more secure than an exact year.
Author: anonymous scriptural redactors.
Tradition: Vidyāpīṭha; arguably our earliest substantial scriptural witness to what becomes Trika.

This is much more important than its fame suggests. Törzsök calls it the oldest scriptural source of the theological tradition subsequently known as Trika, while also making it an early source for mantra-goddess/Yoginī religion. Her thesis edits and translates 23 of the 32 chapters of the short recension.

Free Sanskrit + English

Judit Törzsök, 1999 Oxford DPhil — critical edition + annotated translation of 23 chapters

https://www.academia.edu/1013324/The_doctrine_of_magic_female_spirits_a_critical_edition_of_selected_chapters_of_the_Siddhayoge%C5%9Bvar%C4%ABmata_tantra_with_annotated_translation_and_analysis_INTRO

Translation component:

https://www.academia.edu/39478101/Siddhayoge%C5%9Bvar%C4%ABmata_translation_of_selected_chapters_Pt_2_of_the_thesis_Oxford_1999

_

The dissertation isn't merely a translation: it uses parallel passages from other edited and unedited tantras, identifies citations in Abhinavagupta's Tantrāloka, and compares alternative Svacchanda recensions.

Ingest immediately beside it

Mālinīvijayottara — claims descent from the Siddhayogeśvarīmata.
Tantrasadbhāva — later Trika development.
Svacchanda — extremely useful parallel source.
Brahmayāmala — to distinguish early Trika from the wider Vidyāpīṭha environment.

This should therefore become:

SYMT → MVT → Tantrasadbhāva → Abhinava

with actual passage-level dependency edges.

2. Mālinīvijayottaratantra

Date: pre-Abhinavagupta; probably formed in the early-medieval Trika environment before the 10th century. I would encode a range rather than a fake exact date.
Author: anonymous redactor(s).
Tradition: Trika, combining scriptural Trika with Siddhānta/Kaula yogic materials.

This is one of the most important texts in the entire corpus. Vasudeva shows that it synthesizes competing yogas and creates an extraordinarily elaborate system based around levels of apperception; Abhinavagupta subsequently makes it central to his synthesis.

Complete free Sanskrit e-text

GRETIL

https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/html/sa_mAlinIvijayottaratantra.htm

This is especially useful computationally. Chapters 1–4, 7 and 11–17 derive from Vasudeva's critical work; the remaining chapters are supplied from Madhusudan Kaul's 1922 KSTS edition.
Best free scholarly translation/edition

Somadeva Vasudeva, The Yoga of the Mālinīvijayottaratantra

https://www.academia.edu/3203294/The_Yoga_of_the_M%C4%81lin%C4%ABvijayottaratantra_Collection_Indologie_97_Institut_fran%C3%A7ais_de_Pondich%C3%A9ry_Ecole_fran%C3%A7aise_dExtr%C3%AAme_Orient_Pondich%C3%A9ry_2004

It contains Sanskrit editions of major chapters and extensive translations/analysis, especially the yoga material.

There is also a complete online independent translation project:

https://www.sanskrit-trikashaivism.com/en/malinivijayottaratantra-chapter-1-trika-scriptures-non-dual-shaivism-of-kashmir/829

Treat that as secondary/reference, not as your gold scholarly translation.
Adjacent ingestion

Absolute priority:

Siddhayogeśvarīmata
Tantrasadbhāva
Mālinīvijayavārttika
Tantrāloka
Svacchanda
relevant Siddhānta yoga: Mṛgendra, Mataṅga, Kiraṇa

Vasudeva's research is particularly valuable because the MVT itself explicitly incorporates Siddhānta and Kula systems.

3. Tantrasadbhāva

Date: difficult. Certainly considerably earlier than its surviving late-11th-century Nepalese manuscript and already authoritative enough to be quoted by Kashmirian authors. I'd provisionally encode c. 8th–10th century, low/medium confidence.
Author: anonymous.
Tradition: non-Siddhāntika Śaiva/Trika environment.

This may be the highest-return untranslated scripture in the whole corpus.

Bang confirms that the extant recension survives through Nepalese witnesses, that it is heavily cited by Kashmirian authors, and that it has significant relations with both the Svacchanda and Kubjikāmata.

Best free edition + English translation

Junglan Bang, 2022 PhD, Hamburg

https://ediss.sub.uni-hamburg.de/handle/ediss/9642?mode=full

This is essential.

It critically edits and translates selected material including:

chapter 1;
part of chapter 3;
chapter 9;
chapter 18;
chapter 28;

plus parallel passages from the Nepalese Svacchandalalitabhairava recension and material from Bhojadeva's Siddhāntasārapaddhati.

Sanskrit e-text situation

There has long been an electronic Tantrasadbhāva associated with the tantric e-text ecosystem; scholarship explicitly lists it among electronic texts used in research.

Start from the INDOLOGY tantric-resource hub:

https://indology.info/virtual-e-text-archive-of-indic-texts/

That page links the Hamburg tantric e-text collections and other relevant repositories.
Adjacent texts

This is one of those cases where adjacency is more important than chronology:

Svacchanda ↔ Tantrasadbhāva ↔ Kubjikāmata

Bang finds exactly these relations.

Also ingest:

Siddhayogeśvarīmata
Mālinīvijayottara
Brahmayāmala
Tantrāloka/Jayaratha citations

This could produce an exceptional textual borrowing graph.

4. Svacchandatantra + Kṣemarāja's Uddyota

Date: probably around the 7th–8th century in its earlier strata; definitely early enough to borrow from older Niśvāsa material.


Author: anonymous scripture; commentary by Kṣemarāja, c. 11th century.
Tradition: Bhairava/Mantramārga, enormously influential in Kashmir.

Free Sanskrit

Muktabodha has a searchable electronic Svacchandatantra with Kṣemarāja's complete commentary. INDOLOGY's archive explicitly inventories it.

Main resource directory:

https://indology.info/virtual-e-text-archive-of-indic-texts/

Muktabodha:

https://muktabodha.org/

Muktabodha announced that both the Netra + Kṣemarāja and Svacchanda + Kṣemarāja e-texts were generated largely from the KSTS editions.
Public-domain Sanskrit scan

Internet Archive has downloadable Sanskrit volumes:

https://archive.org/details/SriSvacchandaTantraIParamhansaMishra

English

I do not find a complete, modern, scholarly English translation openly and lawfully downloadable.

There are scholarly studies/translations of portions. A good free one for your corpus is the ritual/body study:

https://www.researchgate.net/publication/278152455_The_Body_Divine_Tantric_Saivite_Ritual_Practices_in_the_Svacchandatantra_and_Its_Commentary

Adjacent

Mandatory:

Niśvāsa
Tantrasadbhāva
Netra
Mālinīvijayottara
Kṣemarāja's later exegesis

Pāṭala priority: extremely high because here you have complete Sanskrit + commentary but no equivalent complete English layer.

5. Brahmayāmala / Picumata

Date: core probably late 7th / early 8th century.
Author: anonymous/redactional.
Tradition: early Bhairava/Vidyāpīṭha Śākta Śaivism.

This is one of the earliest surviving goddess-oriented Śaiva tantras. The corpus is more than 12,000 verses, with roughly a hundred chapters.

Free critical edition + translation: Hatley

Volume I — chapters 1–2, 39–40, 83

https://www.academia.edu/37169073/The_Brahmay%C4%81mala_or_Picumata_Volume_I_Chapters_1_2_39_40_and_83_Revelation_Ritual_and_Material_Culture_in_an_Early_%C5%9Aaiva_Tantra

Author-uploaded/free scholarly PDF.

HAL record:

https://hal.science/hal-02126896

Free critical edition + translation: Kiss

Volume II — chapters 3, 21, 45

https://www.academia.edu/127174520/Brahmaya_malatantra_or_Picumata_vol_II_The_Religious_Observances_and_Sexual_Rituals_of_the_Tantric_Practitioner_Chapters_3_21_and_45_A_Critical_Edition_and_Annotated_Translation_By_Csaba_Kiss

Hatley's dissertation

Earlier versions also edit/translate chapters 55, 73, 99, in addition to material subsequently revised for publication. Scholarship explicitly records this online dissertation layer.

Chapter 46

Hatley's 2025 paper provides another critical edition/translation of chapter 46.

So do not translate the already-covered chapters from scratch.

Build:

BraYā 1–3
21
39–40
45–46
55
73
83
99
      = existing human gold

everything else
      = translation frontier
Adjacent

Mandatory:

Siddhayogeśvarīmata
Tantrasadbhāva
Svacchanda
Jayadrathayāmala
Kubjikāmata

There are actual structural parallels: for example, scholarship notes continuities between Brahmayāmala goddess structures and later Kubjikāmata material.

6. Jayadrathayāmala / Śiraścheda

Date: layered compilation; much of the material relevant to the emergence of Krama belongs to the early-medieval period, probably broadly 9th–10th century, but I would encode individual layers separately rather than assign the whole 24,000-verse complex one date.
Author: anonymous/redactional; the title does not mean King Jayadratha wrote it.
Tradition: Kālīkula / Krama / Vidyāpīṭha.

This remains one of the biggest holes.

Excellent discovery: complete public-domain manuscript of Ṣaṭka III

Staatsbibliothek Berlin has digitized Jayadrathayāmala Ṣaṭka 3, MS Hs. or. 8535, 216 folios, copied in 1667.

Catalogue + download:

https://www.deutsche-digitale-bibliothek.de/item/F724ZGSKVCKQTWQL5JLBKRSIXXBPVPV7

Permanent resolver:

http://resolver.staatsbibliothek-berlin.de/SBB00020C5200000000

It is explicitly marked Public Domain.

That's a significant ingestion opportunity.

Electronic transcription

Olga Serbaeva produced working electronic transcriptions based on the Kathmandu manuscripts; scholarship cites:

NAK 5-4650 — ṣaṭkas I–II
NAK 5-722 — ṣaṭka III
NAK 1-1468 — ṣaṭka IV

but these are cited as working research e-texts, not a stable public critical edition.

Free translated portions

KramaNet gives an excellent bibliography of what has actually been translated:

https://www.kramanet.org/publications-1

Notably:

Ṣaṭka III, chapter 35 — Olga Serbaeva

listed there as “Avyapadeśyā: Indefinable Kālī.”

Also:

War-magic study with translated Jayadrathayāmala passages

https://www.mdpi.com/2077-1444/13/4/278

Bottom line

There is no complete open scholarly edition + English translation.

This remains a genuine flagship target.

7. Kālīkulapañcaśatikā / Devīpañcaśatikā

Date: early-medieval Krama, probably around the period in which the twelve-Kālī system is consolidating; treat approximately 9th–10th century pending section-level philological dating.
Author: anonymous scripture.
Tradition: Kālīkrama.

Free Sanskrit

This is one of Mark Dyczkowski's electronic editions preserved through the Muktabodha ecosystem.

INDOLOGY explicitly lists:

Kalikulapancasatika (also called Devipancasatika), edited by Mark S. G. Dyczkowski.

Resource gateway:

https://indology.info/virtual-e-text-archive-of-indic-texts/

Muktabodha:

https://muktabodha.org/

English

I found no complete scholarly English translation freely available.

There are translated passages embedded in Krama scholarship.

Adjacent — extremely important

Don't ingest this alone. Build the Kālīkrama packet:

Kālīkulapañcaśatikā
Kramasadbhāva
Devīdvyardhaśatikā
Jñānanetra's Śrīkhacakrapañcakastotra
Arṇasiṃha's Mahānayaprakāśa
Abhinavagupta's Kramastotra
Jayadrathayāmala

Crucially, the Sanskrit of almost this entire packet already exists electronically. INDOLOGY/Muktabodha lists the Devīdvyardhaśatikā, Kālīkulapañcaśatikā, Mahānayaprakāśa, Śrīkhacakrapañcakastotra and related works.

This changes my priority substantially.

We should ingest the whole Krama packet now.

8. Kramasadbhāva

Date: broadly early-medieval Krama, probably c. 9th–10th century; exact dating remains difficult.
Author: anonymous.
Tradition: Kālīkrama.

Sanskrit

Dyczkowski's electronic edition is explicitly documented in modern scholarship.

Again use:

https://indology.info/virtual-e-text-archive-of-indic-texts/

The INDOLOGY archive inventories it directly as:

Kramasadbhava, a Kalikrama text edited by Mark S.G. Dyczkowski.

English

No complete scholarly English translation located.

Adjacent

Same Krama packet as above.

For concept extraction I'd immediately make trajectories for:

krama
kālī
saṃhāra
kālasaṃkarṣiṇī
bhāsa
vikalpa
saṃvit
cakra
krama / akrama

and compare occurrences against Jayadrathayāmala and Abhinava.

9. Mālinīvijayavārttika / Mālinīślokavārttika — Abhinavagupta

Date: c. late 10th / early 11th century.
Author: Abhinavagupta.
Function: Abhinava's sustained interpretation of Mālinī revelation.

Free complete Sanskrit e-text

GRETIL contains both kāṇḍas, based on Jürgen Hanneder's input.

Main GRETIL:

https://gretil.sub.uni-goettingen.de/

Search title: Malinislokavarttika

Free scholarly edition + translation of the opening

Jürgen Hanneder, Abhinavagupta's Philosophy of Revelation

Direct Brill PDF:

https://brill.com/downloadpdf/display/title/24058.pdf

The study explicitly edits/translates the first part of the work dealing with Śaiva revelation.
Translation status

Complete Sanskrit: yes.
Complete English: no.

That makes it unusually attractive.

Unlike Jayadrathayāmala, the source text is already digitized and the author's terminology is massively cross-referenced through IPVV/Tantrāloka.

This is probably the easiest major Abhinava translation win after IPVV.

10. Śivadṛṣṭi — Somānanda + Utpaladeva's Padasaṃgati

Date: late 9th / early 10th century.
Author: Somānanda.
Commentator: Utpaladeva.
Tradition: immediate philosophical precursor to Pratyabhijñā.

This is non-negotiable for Pāṭala.

Torella describes it as the first philosophical presentation of nondual Śaivism and a foundation stone of Pratyabhijñā.

Sanskrit

Muktabodha has the Śivadṛṣṭi electronically. INDOLOGY explicitly lists:

Sivadrsti of Somananda

among Muktabodha's searchable corpus.

https://muktabodha.org/
Old Sanskrit edition

The historical KSTS edition is:

Madhusudan Kaul, KSTS 54, Srinagar 1934

with Somānanda and Utpaladeva's commentary; Torella identifies this edition precisely.

English translation

John Nemec's The Ubiquitous Śiva critically edits/translates the first three āhnikas together with Utpaladeva's commentary.

It is a commercial OUP book rather than a legitimately free open edition; don't pirate it.

Bibliographic record:

https://www.finna.fi/Record/kamk.99553259306247

Free scholarly corrections / translated passages

Raffaele Torella's substantial article:

https://www.researchgate.net/publication/272018703_Notes_on_the_Sivadrsti_by_Somananda_and_its_Commentary

This is extremely useful because Torella identifies textual problems in the existing editions/translations and discusses both Śivadṛṣṭi and Utpaladeva's commentary.
Critical correction to our earlier plan

Utpaladeva's surviving commentary does not cover the entire Śivadṛṣṭi. Torella reports that the Padasaṃgati survives through the first three āhnikas and part of the fourth.

So the project should be:

Śivadṛṣṭi 1–3
existing gold: Nemec + Utpaladeva

Śivadṛṣṭi 4
fragmentary Utpaladeva commentary

Śivadṛṣṭi remainder
Somānanda alone
      ↓
compare proposition-by-proposition with ĪPK

That would be exceptionally valuable.

11. Kiraṇatantra + Rāmakaṇṭha

Date: early Śaiva Siddhānta, probably broadly 7th–8th-century scripture; Rāmakaṇṭha is much later, around the 10th century.
Scripture: anonymous.
Commentary: Bhaṭṭa Rāmakaṇṭha II.

Free machine-readable Sanskrit

Chapters 1–6 + Rāmakaṇṭha commentary

https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/4_rellit/saiva/kirtc_pu.htm

This is derived from Dominic Goodall's critical edition and contains both scripture and commentary.
English

Goodall's edition provides annotated English for chapters 1–6, but I did not locate a legitimate complete freely downloadable edition of the published book.

So:

Sanskrit gold: readily ingestible.
English gold: chapters 1–6 exists academically, but access/licensing requires care.
Remaining material: major opportunity.

Adjacent

For the philosophical engine ingest:

Sadyojyotis
Mṛgendratantra
Mataṅgaparameśvara
Parākhyatantra
Rāmakaṇṭha's other works
Utpaladeva/IPK/IPVV

This provides your strongest internal Śaiva control group:

Rāmakaṇṭha
pati ≠ paśu
         vs
Utpaladeva
everything manifests within unitary consciousness
12. Netratantra + Kṣemarāja

Date: probably early 9th century; scholarship treats it as later than Svacchanda and centuries earlier than Kṣemarāja.


Author: anonymous.
Commentary: Kṣemarāja, c. 11th century.

Sanskrit

Muktabodha has a searchable Netra Tantra + Kṣemarāja commentary, based largely on the KSTS edition.

https://muktabodha.org/The original KSTS edition was published in volumes 46 and 61, edited by Madhusudan Kaul; surviving manuscripts have also been digitized.
English

There is now substantial modern scholarship on Netra, but I do not find a complete free scholarly English translation of the entire tantra + Kṣemarāja.

Useful contextual study/preview:

https://api.pageplace.de/preview/DT0400.9780197553275_A42843176/preview-9780197553275_A42843176.pdf

Adjacent

Especially:

Svacchandatantra
Mṛtyuñjaya traditions
Kṣemarāja
Tantrāloka
IPVV

There is a direct reason: Abhinavagupta cites the text in both the Tantrāloka and IPVV.

So it belongs in the IPVV evidence graph, not merely the ritual corpus.

13. Kubjikāmatatantra

Date: early Western Kaula/Kubjikā tradition; I'd encode approximately 9th–10th-century formation with later transmission history rather than confidently attach a single date.
Author: anonymous.
Tradition: Paścimāmnāya / Kubjikā Kaula.

Complete free Sanskrit e-text

Excellent quality for ingestion:

https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/4_rellit/saiva/kubjt_pu.htm

It is based on the Goudriaan/Schoterman 1988 edition and was input by Somadeva Vasudeva.

This is 6,000+ lines of directly machine-readable Sanskrit.

English

There is no equivalent complete, freely available scholarly English translation that I could verify.

Adjacent

Extremely high signal:

Tantrasadbhāva
Brahmayāmala
Siddhayogeśvarīmata
Manthānabhairavatantra
Kularatnoddyota
Śrīmatottara

In fact scholarship explicitly records the Kularatnoddyota as an unpublished/digital electronic text, while Kubjikāmata is already on GRETIL.

14. Manthānabhairavatantra

Here's a major correction to my earlier suggestion.

Do not make this a translation target yet.

Mark Dyczkowski already spent decades on it.

Existing work

The work is approximately 24,000 verses. Dyczkowski produced a 14-volume scholarly project, including critical Sanskrit, translation, extensive notes and historical study of the Kumārikākhaṇḍa.

Bibliographic record:

https://hermetism.org/catalogue/kashmir-shaivism/dyczkowski-manthanabhairavatantra/

The publisher edition is copyrighted, and I did not locate an authorized free full digital edition.

So do not use the PDFCoffee/etc. mirrors.

What to ingest instead

Acquire/licence Dyczkowski eventually, but prioritize free primary infrastructure first:

Kubjikāmata
Kularatnoddyota
Tantrasadbhāva
Brahmayāmala
MVT

Then use Manthānabhairava as a giant comparison corpus.

15. Devyāmala

This is the messiest one.

Date: early-medieval Śākta/Kaula material, but the textual identity and layers need much more care than the comparatively stable MVT or Kubjikāmata.
Author: anonymous.
State: fragmented/manuscript-heavy tradition rather than a clean modern canonical edition.

I did not find a complete freely available critical edition or translation that I would trust enough to recommend as Pāṭala's base text.

However, the Devyāmala is genuinely important enough to keep on the watch list: modern work on early Śaiva temple architecture, for example, critically edits and translates Devyāmala material alongside other early Śaiva scriptures.

So I'd classify:

High historical value, bad immediate translation economics.

Don't start here while Tantrasadbhāva/Krama/MVV have clean electronic witnesses.

The adjacent corpus I now think we should ingest

This deep dive changes the answer substantially.

There is a ready-made electronic Krama corpus hiding in Muktabodha that should go into Pāṭala essentially immediately. INDOLOGY verifies all of these electronic texts.

Text	Why
Devīdvyardhaśatikā — Prabodhanātha	major Kālīkrama witness
Kālīkulapañcaśatikā	core early Kālī scripture
Kramasadbhāva	core Krama scripture
Mahānayaprakāśa — Arṇasiṃha	systematic Krama
Śrīkhacakrapañcakastotra — Jñānanetra	exceptionally important early master/text
Kularatnoddyota	Kaula/Kubjikā bridge
Spandakārikā + Kallaṭa + Rāmakaṇṭha	early nondual Kashmir bridge
Spandapradīpikā — Bhagavadutpala	alternative Spanda interpretation
Śivadṛṣṭi — Somānanda	immediate Pratyabhijñā ancestor
Śivastotrāvalī — Utpaladeva	doctrinal + experiential Utpaladeva
Īśvarasiddhi — Utpaladeva	crucial philosophical fragment/work
Sambandhasiddhi — Utpaladeva	important philosophical context
Netra + Kṣemarāja	Kashmirian Bhairava substrate
Svacchanda + Kṣemarāja	huge Bhairava substrate
Tantrāloka + Jayaratha	canonical synthesis + source identification

The source gateway for this entire collection is:

https://indology.info/virtual-e-text-archive-of-indic-texts/

and:

https://muktabodha.org/

So the actual Pāṭala corpus should now be built in this order

I would not translate in the same order as historical chronology.

Use existing human work to bootstrap an evidence graph first:

TIER 0 — INGEST EXISTING HUMAN GOLD
───────────────────────────────────
Siddhayogeśvarīmata — Törzsök
Mālinīvijayottara — Vasudeva
Tantrasadbhāva selections — Bang
Brahmayāmala translated chapters — Hatley/Kiss
Śivadṛṣṭi 1–3 — Nemec + Torella corrections
Kiraṇa 1–6 — Goodall
Niśvāsa — Goodall et al.

                 ↓

TIER 1 — INGEST COMPLETE SANSKRIT CORPORA
─────────────────────────────────────────
Svacchanda + Kṣemarāja
Netra + Kṣemarāja
Kubjikāmata
Kālīkulapañcaśatikā
Kramasadbhāva
Devīdvyardhaśatikā
Mahānayaprakāśa
Śrīkhacakrapañcakastotra
Śivadṛṣṭi
Mālinīvijayavārttika

                 ↓

TIER 2 — TRANSLATE THE HIGH-LEVERAGE HOLES
──────────────────────────────────────────
1. Kālīkulapañcaśatikā
2. Kramasadbhāva
3. remaining Mālinīvijayavārttika
4. remaining Śivadṛṣṭi
5. Tantrasadbhāva
6. Svacchanda
7. Netra
8. remaining Siddhayogeśvarīmata/MVT

                 ↓

TIER 3 — MANUSCRIPT-SCALE FLAGSHIPS
───────────────────────────────────
Jayadrathayāmala
remaining Brahmayāmala
Devyāmala

The key change is Krama.

We don't need to begin by wrestling blindly with the 24,000-verse Jayadrathayāmala. We already have a cluster of smaller, machine-readable Kālīkrama Sanskrit texts—Kālīkulapañcaśatikā + Kramasadbhāva + Devīdvyardhaśatikā + Mahānayaprakāśa + Jñānanetra—that can establish the terminology, ontology, deity graph and translation memory first.

Then when we hit Jayadrathayāmala, Pāṭala already knows the Krama language.

And the most exciting computational chain is now pretty clear:

BRAHMAYĀMALA
late 7th / early 8th c.
      │
      ├──── wider Vidyāpīṭha / Śākta substrate
      │
      ▼
SIDDHAYOGEŚVARĪMATA
      │
      ├─────────────────┐
      ▼                 ▼
MĀLINĪVIJAYOTTARA    KĀLĪ / KRAMA
      │                 │
      │          Kālīkulapañcaśatikā
      │          Kramasadbhāva
      │          Jayadrathayāmala
      │                 │
      └────────┬────────┘
               ▼
        ABHINAVAGUPTA
      MVV / TANTRĀLOKA
               │
               ├── Pratyabhijñā:
               │   Somānanda → Utpaladeva → IPVV
               │
               └── Bhairava:
                   Svacchanda / Netra

That's much closer to a recoverable dependency network than I thought when we started. We can already obtain machine-readable Sanskrit for a surprisingly large percentage of the nodes, and for several crucial nodes—SYMT, MVT, Tantrasadbhāva, Brahmayāmala—we have enough human scholarly translation to create a genuinely high-quality translation-memory/evidence layer rather than starting from LLM output.

The highest-value next action is therefore not another broad hunt: it is to make a download manifest for this exact corpus—one row per work with canonical_id, Sanskrit URL, translation URL, file format, chapters covered, edition basis, approximate date, author/redactor, citations in Abhinava, and TRANSLATE / INGEST / MANUSCRIPT status—so the repo can actually pull the corpus automatically.
