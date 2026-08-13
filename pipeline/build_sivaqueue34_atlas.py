#!/usr/bin/env python3
"""pipeline/build_sivaqueue34_atlas.py — generate data/atlas/sivaqueue34Seed.ts.

One-time generator: converts the sivaqueue3/4 census + translation-guide data into
BibliographyRecord entries (TypeScript), so the bibliography atlas is the canonical source
for every work's tradition/sub-school, working period, author/attribution, parsing register,
Sanskrit sources, and available English translations + verdict.

The data below is transcribed from:
  - docs/corpus/sivaqueue3-translation-guide.md
  - docs/corpus/sivaqueue4-translation-guide.md
  - docs/corpus/sivaqueue34-companion.md   (tradition / period / author / register)

Run: python3 pipeline/build_sivaqueue34_atlas.py   (writes data/atlas/sivaqueue34Seed.ts)
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("/root/projects/patala")
OUT = ROOT / "data/atlas" / "sivaqueue34Seed.ts"

# Each record: id, work, traditions[], subschool, period{start,end,approximate},
# author, register, sources[], translations[], verdict.
# sources/translations: dict(provider, url, note, type, tier).
RECORDS = [
    # ---------------- sivaqueue4: Vedic Saṃhitās ----------------
    dict(
        id="maitrayanisamhita", work="Maitrāyaṇī Saṃhitā (Kṛṣṇa Yajurveda)",
        traditions=["Vedic"], subschool="Kṛṣṇa Yajurveda, Maitrāyaṇīya",
        period=dict(start=-1200, end=-900, approximate=True), author="Anonymous priestly transmission",
        register="Old Yajurvedic prose/mantra",
        sources=[
            dict(type="etext", provider="GRETIL", url="https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/1_veda/1_sam/maitrs_pu.htm", note="von Schroeder edition", tier="C"),
            dict(type="scan", provider="Internet Archive", url="https://archive.org/details/maitrayanisamhit015004mbp", note="Satavalekar edition", tier="C"),
        ],
        translations=[], verdict="TRANSLATE / HIGH-VALUE VEDIC CONTROL",
    ),
    dict(
        id="kathakasamhita", work="Kāṭhaka Saṃhitā (Kṛṣṇa Yajurveda)",
        traditions=["Vedic"], subschool="Kṛṣṇa Yajurveda, Kaṭha",
        period=dict(start=-1200, end=-900, approximate=True), author="Anonymous priestly transmission",
        register="Old Yajurvedic",
        sources=[
            dict(type="index", provider="GRETIL", url="https://gretil.sub.uni-goettingen.de/gretil.html", tier="D"),
            dict(type="index", provider="TITUS", url="https://titus.uni-frankfurt.de/texte/texte2.htm", tier="D"),
            dict(type="index", provider="Vedic Heritage", url="https://vedicheritage.gov.in/samhitas/yajurveda/", tier="D"),
        ],
        translations=[], verdict="TRANSLATE (Rudra-relevant sections first)",
    ),
    dict(
        id="kapisthalakathasamhita", work="Kapiṣṭhala-Kaṭha Saṃhitā (Kṛṣṇa Yajurveda)",
        traditions=["Vedic"], subschool="Kṛṣṇa Yajurveda, Kapiṣṭhala",
        period=dict(end=-1000, approximate=True), author="Anonymous",
        register="Old Yajurvedic",
        sources=[
            dict(type="edition", provider="SOAS Repository", url="https://soas-repository.worktribe.com/output/383107/kapisthala-katha-samhita", note="Raghu Vira edition", tier="C"),
            dict(type="edition", provider="DOI", url="https://doi.org/10.25501/SOAS.00034009", tier="C"),
        ],
        translations=[], verdict="TRANSLATE-HOLES / VERY INTERESTING",
    ),
    dict(
        id="taittiriyabrahmana", work="Taittirīya Brāhmaṇa (Kṛṣṇa Yajurveda)",
        traditions=["Vedic"], subschool="Kṛṣṇa Yajurveda, Taittirīya",
        period=dict(start=-900, end=-700, approximate=True), author="Anonymous",
        register="Late Vedic prose/mantra",
        sources=[
            dict(type="scan", provider="Internet Archive", url="https://archive.org/download/dli.granth.71695/71695.pdf", note="Vol. II, Rajendralal Mitra edition", tier="C"),
            dict(type="scan", provider="Internet Archive", url="https://archive.org/download/dli.granth.71696/71696.pdf", note="Vol. III", tier="C"),
        ],
        translations=[], verdict="TRANSLATE SELECTED PASSAGES (Rudra/theology)",
    ),
    dict(
        id="kausitakibrahmana", work="Kauṣītaki / Śāṅkhāyana Brāhmaṇa (Ṛgveda)",
        traditions=["Vedic"], subschool="Ṛgvedic Kauṣītaki/Śāṅkhāyana",
        period=dict(start=-900, end=-700, approximate=True), author="Anonymous",
        register="Brāhmaṇa prose",
        sources=[
            dict(type="etext", provider="GRETIL", url="https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/html/sa_kauSItakibrAhmaNa.htm", note="Sreekrishna Sarma edition", tier="C"),
            dict(type="etext", provider="GRETIL", url="https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/1_veda/2_bra/kausibru.htm", tier="C"),
        ],
        translations=[
            dict(language="en", translator="A. B. Keith", work="Rigveda Brahmanas", coverage="complete (Aitareya + Kauṣītaki)", complete=True, type="scholarly", url="https://archive.org/details/rigvedabrahmana00keitgoog", tier="C"),
        ],
        verdict="INGEST-GOLD",
    ),
    dict(
        id="gopathabrahmana", work="Gopatha Brāhmaṇa (Atharvaveda)",
        traditions=["Vedic"], subschool="Atharvaveda",
        period=dict(approximate=True), author="Anonymous",
        register="Late Vedic/Brāhmaṇa",
        sources=[
            dict(type="etext", provider="GRETIL", url="https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/1_veda/2_bra/gopthbru.htm", tier="C"),
            dict(type="scan", provider="Internet Archive", url="https://archive.org/details/gopathabrahmanao00gopauoft", note="Mitra/Vidyābhūṣaṇa 1872", tier="C"),
            dict(type="index", provider="Vedic Heritage", url="https://vedicheritage.gov.in/brahmanas/gopatha-brhamana/", tier="D"),
        ],
        translations=[
            dict(language="en", translator="Hukam Chand Patyal", coverage="complete", complete=True, type="scholarly", note="commercial edition", tier="D"),
        ],
        verdict="SANSKRIT INGEST + TRANSLATION ACQUISITION/NEW TRANSLATION",
    ),
    dict(
        id="pancavimsabrahmana", work="Pañcaviṃśa / Tāṇḍya Mahābrāhmaṇa (Sāmaveda)",
        traditions=["Vedic"], subschool="Sāmaveda, Kauthuma",
        period=dict(start=-900, end=-700, approximate=True), author="Anonymous",
        register="Technical ritual prose",
        sources=[
            dict(type="etext", provider="GRETIL", url="https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/html/sa_paJcaviMzabrAhmaNa.htm", tier="C"),
        ],
        translations=[
            dict(language="en", translator="Willem Caland", coverage="complete", complete=True, type="scholarly", url="https://archive.org/details/pancavimsabrahma032052mbp", tier="C"),
            dict(language="en", translator="Willem Caland", coverage="complete", complete=True, type="scholarly", url="https://www.wisdomlib.org/hinduism/book/panchavimsha-brahmana-english-translation", tier="C"),
        ],
        verdict="INGEST-GOLD / CONTROL CORPUS",
    ),
    dict(
        id="jaiminiyabrahmana", work="Jaiminīya Brāhmaṇa (Sāmaveda)",
        traditions=["Vedic"], subschool="Sāmaveda, Jaiminīya",
        period=dict(end=-900, approximate=True), author="Anonymous",
        register="Archaic/irregular Brāhmaṇa prose",
        sources=[
            dict(type="scan", provider="Internet Archive", url="https://archive.org/details/jaiminiyabrahman014906mbp", note="Raghu Vira edition", tier="C"),
            dict(type="etext", provider="sa.wikisource", url="https://sa.wikisource.org/wiki/सामवेदः/जैमिनीयाः/जैमिनीयं_ब्राह्मणम्", tier="C"),
            dict(type="index", provider="Vedic Heritage", url="https://vedicheritage.gov.in/brahmanas/jaiminiya-brhamana/", tier="D"),
        ],
        translations=[], verdict="TRANSLATE-HOLES",
    ),
    dict(
        id="jaiminiyaupanisadbrahmana", work="Jaiminīya-Upaniṣad-Brāhmaṇa (Sāmaveda)",
        traditions=["Vedic"], subschool="Sāmaveda, Jaiminīya",
        period=dict(start=-800, end=-600, approximate=True), author="Anonymous",
        register="Transitional Brāhmaṇa/Upaniṣadic",
        sources=[
            dict(type="etext", provider="Sanskrit Library", url="https://sanskritlibrary.org/catalogsText/titus/vedic/jub.html", note="TITUS/Oertel tradition, XML", tier="C"),
        ],
        translations=[
            dict(language="en", translator="Hanns Oertel", coverage="complete", complete=True, type="scholarly", note="text + translation + notes basis", tier="C"),
        ],
        verdict="INGEST-GOLD",
    ),
    dict(
        id="sankhayanaaranyaka", work="Śāṅkhāyana Āraṇyaka (Ṛgveda)",
        traditions=["Vedic"], subschool="Ṛgvedic Śāṅkhāyana",
        period=dict(start=-800, end=-600, approximate=True), author="composite",
        register="Late Vedic prose",
        sources=[
            dict(type="etext", provider="GRETIL", url="https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/html/sa_zaGkhAyana-AraNyaka.htm", note="Bhim Dev + Keith material", tier="C"),
        ],
        translations=[], verdict="INGEST / TRANSLATE-HOLES",
    ),
    dict(
        id="aitareyaaranyaka", work="Aitareya Āraṇyaka (Ṛgveda)",
        traditions=["Vedic"], subschool="Ṛgveda",
        period=dict(start=-800, end=-600, approximate=True), author="composite; traditional ṛṣi associations",
        register="Late Vedic prose",
        sources=[
            dict(type="scan", provider="Internet Archive", url="https://archive.org/search?query=%22Aitareya+Aranyaka%22+Keith", note="A. B. Keith edition/translation", tier="C"),
            dict(type="index", provider="TITUS", url="https://titus.uni-frankfurt.de/texte/texte2.htm", tier="D"),
        ],
        translations=[
            dict(language="en", translator="A. B. Keith", coverage="complete", complete=True, type="scholarly", note="classic edition/translation", tier="C"),
        ],
        verdict="INGEST-GOLD",
    ),
    # ---------------- sivaqueue4: Upaniṣads ----------------
    dict(
        id="maitriupanisad", work="Maitrī / Maitrāyaṇīya Upaniṣad",
        traditions=["Upaniṣadic"], subschool="Maitrāyaṇīya/Yajurvedic",
        period=dict(end=-300, approximate=True), author="composite/anonymous",
        register="Late Upaniṣadic Sanskrit",
        sources=[
            dict(type="scan", provider="Internet Archive", url="https://archive.org/details/p2upanishads00mluoft", tier="C"),
            dict(type="index", provider="GRETIL", url="https://gretil.sub.uni-goettingen.de/gretil.html", tier="D"),
        ],
        translations=[
            dict(language="en", translator="Max Müller", coverage="complete", complete=True, type="scholarly", url="https://archive.sacred-texts.com/hin/sbe15/sbe15113.htm", tier="C"),
        ],
        verdict="INGEST-GOLD",
    ),
    dict(
        id="kathaupanisad", work="Kaṭha Upaniṣad",
        traditions=["early Upaniṣadic"], subschool="Kṛṣṇa Yajurveda/Kaṭha association",
        period=dict(start=-500, end=-300, approximate=True), author="Anonymous",
        register="Late Vedic → early Classical transition",
        sources=[
            dict(type="etext", provider="Wisdom Library", url="https://www.wisdomlib.org/hinduism/book/katha-upanishad-shankara-bhashya", note="Sanskrit + Śaṅkara + S. Sitarama Sastri English", tier="C"),
            dict(type="scan", provider="Internet Archive", url="https://archive.org/details/p2upanishads00mluoft", tier="C"),
        ],
        translations=[
            dict(language="en", translator="Max Müller", coverage="complete", complete=True, type="scholarly", url="https://archive.org/details/p2upanishads00mluoft", tier="C"),
        ],
        verdict="INGEST-GOLD (control for self/yoga/liberation)",
    ),
    dict(
        id="mahanarayanaupanisad", work="Mahānārāyaṇa Upaniṣad",
        traditions=["late Vedic/Upaniṣadic"], subschool="Taittirīya/Yajurveda traditions",
        period=dict(end=-400, approximate=True), author="Anonymous compilation",
        register="Late Vedic + liturgical Sanskrit",
        sources=[
            dict(type="index", provider="GRETIL", url="https://gretil.sub.uni-goettingen.de/gretil.html", tier="D"),
            dict(type="index", provider="Vedic Heritage", url="https://vedicheritage.gov.in/", tier="D"),
        ],
        translations=[], verdict="INGEST + ALIGN RECENSIONS",
    ),
    dict(
        id="atharvasiraupanisad", work="Atharvaśiras / Atharvaśira Upaniṣad",
        traditions=["early explicitly Rudra-Śaiva Upaniṣadic"], subschool="Atharvavedic affiliation",
        period=dict(start=-100, end=100, approximate=True), author="Anonymous",
        register="Late Upaniṣadic/sectarian Sanskrit",
        sources=[
            dict(type="etext", provider="GRETIL", url="https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/html/sa_zira-upaniSad.htm", tier="C"),
            dict(type="etext", provider="GRETIL", url="https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/1_veda/4_upa/sirup_u.htm", note="Ramamaya Tarkaratna, Atharvana-Upanishads 1872", tier="C"),
        ],
        translations=[], verdict="A-TIER TRANSLATE (high signal: gods ask Rudra who he is)",
    ),
    dict(
        id="kaivalyaupanisad", work="Kaivalya Upaniṣad",
        traditions=["Śaiva/Vedāntic Upaniṣadic"], subschool="Atharvavedic classification",
        period=dict(start=0, end=300, approximate=True), author="Anonymous; dialogue Aśvalāyana/Brahmā",
        register="Classicalizing Upaniṣadic Sanskrit",
        sources=[
            dict(type="etext", provider="GRETIL", url="https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/1_veda/4_upa/kaivup_u.htm", tier="C"),
            dict(type="etext", provider="GRETIL", url="https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/html/sa_kaivalyopaniSad.htm", tier="C"),
        ],
        translations=[
            dict(language="en", translator="Alladi Mahadeva Sastri", coverage="complete", complete=True, type="scholarly", url="https://archive.org/details/amritabindukaiva00mahauoft", year=1898, tier="C"),
            dict(language="en", coverage="complete", complete=True, type="independent", url="https://upasanayoga.org/KaivU.htm", note="CC BY-NC-SA", tier="C"),
        ],
        verdict="INGEST-MULTI-GOLD (Śiva identified with brahman/ātman)",
    ),
    dict(
        id="sivaupanisad", work="Śiva Upaniṣad",
        traditions=["sectarian Śaiva Upaniṣadic"], subschool="later Śaiva minor-Upaniṣad corpus",
        period=dict(start=0, end=1000, approximate=True), author="Anonymous; Mahākāla discourse",
        register="Classical/Purāṇic-style Sanskrit",
        sources=[
            dict(type="etext", provider="GRETIL", url="https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/4_rellit/saiva/sivup_pu.htm", note="Adyar Library Unpublished Upaniṣads; references śivadharmāḥ", tier="C"),
        ],
        translations=[], verdict="TRANSLATE (chronologically tagged conservatively)",
    ),
    dict(
        id="svetasvataraupanisad", work="Śvetāśvatara Upaniṣad",
        traditions=["theistic Upaniṣadic"], subschool="Kṛṣṇa Yajurveda",
        period=dict(end=-300, approximate=True), author="traditionally Śvetāśvatara; historically anonymous",
        register="Late Upaniṣadic verse/prose",
        sources=[], translations=[], verdict="INGEST-GOLD (control; Sāṃkhya-Yoga + theism)",
    ),
    # ---------------- sivaqueue3: epics + Purāṇas ----------------
    dict(
        id="mahabharata", work="Mahābhārata (Śiva strata)",
        traditions=["Epic Brahmanical"], subschool="pan-Indian epic; numerous Śaiva strata",
        period=dict(start=-400, end=400, approximate=True), author="traditionally Vyāsa; historically composite",
        register="Epic Sanskrit",
        sources=[
            dict(type="etext", provider="GRETIL", url="https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/2_epic/mbh/sas/b05/b05c100.htm", note="BORI critical-edition basis", tier="C"),
        ],
        translations=[
            dict(language="en", translator="K. M. Ganguli", coverage="complete", complete=True, type="scholarly", url="https://archive.org/details/mahabharataofkri04calcuoft", note="public-domain", tier="C"),
        ],
        verdict="INGEST-GOLD (Śiva strata; Droṇa/Sānti/Anuśāsana parvans)",
    ),
    dict(
        id="vayupurana", work="Vāyu Purāṇa",
        traditions=["Purāṇic, strongly Śaiva-inflected"], subschool="early Purāṇic cosmology/genealogy",
        period=dict(start=0, end=1000, approximate=True), author="traditionally Vyāsa; anonymous redactors",
        register="Purāṇic Sanskrit",
        sources=[
            dict(type="scan", provider="Internet Archive", url="https://ia801406.us.archive.org/25/items/in.ernet.dli.2015.322328/2015.322328.The-Vayu_text.pdf", note="Rajendralal Mitra Sanskrit", tier="C"),
        ],
        translations=[
            dict(language="en", coverage="complete (2 vols)", complete=True, type="scholarly", url="https://archive.org/download/in.ernet.dli.2015.110236/2015.110236.The-Vayu-Purana-Part-2_text.pdf", tier="C"),
        ],
        verdict="INGEST-GOLD (date individual textual layers)",
    ),
    dict(
        id="lingapurana", work="Liṅga Purāṇa",
        traditions=["explicitly Śaiva Purāṇic"], subschool="Liṅga/Śiva theology",
        period=dict(start=0, end=1000, approximate=True), author="traditionally Vyāsa; composite",
        register="Purāṇic Sanskrit",
        sources=[
            dict(type="etext", provider="GRETIL", url="https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/3_purana/lip_2__u.htm", note="Part II, Venkatesvara Press 1906", tier="C"),
            dict(type="scan", provider="Internet Archive", url="https://archive.org/download/lingapurana/linga_purana.pdf", tier="C"),
        ],
        translations=[
            dict(language="en", translator="J. L. Shastri", coverage="complete (2 parts)", complete=True, type="scholarly", url="https://archive.org/details/LingaPuranaJ.L.ShastriPart1", tier="C"),
        ],
        verdict="INGEST-GOLD",
    ),
    dict(
        id="kurmapurana", work="Kūrma Purāṇa",
        traditions=["Purāṇic, sectarian synthesis"], subschool="Vaiṣṇava frame with substantial Īśvara/Śaiva material",
        period=dict(start=0, end=1000, approximate=True), author="traditionally Vyāsa; composite",
        register="Purāṇic Sanskrit",
        sources=[
            dict(type="etext", provider="GRETIL", url="https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/3_purana/kurmp2_u.htm", note="Part II", tier="C"),
            dict(type="etext", provider="GRETIL", url="https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/3_purana/kurmp1_u.htm", note="Part I", tier="C"),
        ],
        translations=[
            dict(language="en", translator="Anand Swarup Gupta", coverage="complete", complete=True, type="scholarly", url="https://archive.org/details/kurmapuranaTRkashirajtrust1972", note="Varanasi Kashiraj Trust 1972", tier="C"),
        ],
        verdict="INGEST-GOLD",
    ),
    dict(
        id="skandapurana", work="Early Skandapurāṇa",
        traditions=["early Śaiva Purāṇic"], subschool="early SkP recension (≠ later printed Skandapurāṇa)",
        period=dict(start=500, end=700, approximate=True), author="anonymous/redactional",
        register="Purāṇic Sanskrit",
        sources=[
            dict(type="etext", provider="SARIT", url="https://sarit.indologie.uni-goettingen.de/", note="Sanskrit", tier="C"),
            dict(type="scan", provider="OAPEN", url="https://library.oapen.org/bitstream/20.500.12657/25710/1/9789004383517%20-%20The%20Skandapur%C4%81%E1%B9%87a%20Volume%20IV.pdf", note="Critical edition vol. IV, chs. 70–95", tier="C"),
        ],
        translations=[], verdict="INGEST (early Śaiva sacred geography/cosmos)",
    ),
    # ---------------- sivaqueue3: Pāśupata + Śivadharma + Niśvāsa ----------------
    dict(
        id="pasupatasutra", work="Pāśupatasūtra",
        traditions=["Atimārga Śaivism"], subschool="Pāñcārthika Pāśupata",
        period=dict(start=300, end=500, approximate=True), author="traditionally revelation with Lakulīśa; historical author unknown",
        register="Sūtra Sanskrit",
        sources=[], translations=[], verdict="INGEST (root text of Pāśupata)",
    ),
    dict(
        id="sivadharma", work="Śivadharmaśāstra",
        traditions=["lay/devotional Śaivism"], subschool="Śivadharma corpus",
        period=dict(start=500, end=900, approximate=True), author="anonymous/redactional",
        register="Epic-Purāṇic/Classical mixture",
        sources=[], translations=[
            dict(language="en", translator="Peter Bisschop", coverage="chapter 6", complete=False, type="scholarly", work="Universal Śaivism", tier="C"),
            dict(language="en", coverage="chapters 10–11", complete=False, type="scholarly", note="Śaiva Utopia; Śaiva Rites of Fasting and Gift of Cattle", tier="C"),
        ], verdict="INGEST (lay/devotional Śaiva dharma corpus)",
    ),
    dict(
        id="sivadharmottara", work="Śivadharmottara",
        traditions=["lay/devotional + doctrinal Śaivism"], subschool="Śivadharma corpus",
        period=dict(start=500, end=900, approximate=True), author="anonymous; dialogue framing",
        register="Classical/Purāṇic",
        sources=[
            dict(type="scan", provider="IFP", url="https://www.ifpindia.org/transcripts/pdf/T0075.pdf", tier="C"),
        ],
        translations=[], verdict="TRANSLATE / INGEST (Śivadharma corpus companion)",
    ),
    dict(
        id="nisvasatattvasamhita", work="Niśvāsatattvasaṃhitā (Mūlasūtra, Uttarasūtra, Nayasūtra)",
        traditions=["Mantramārga"], subschool="early Śaiva tantra; proto-/early Siddhānta environment",
        period=dict(start=400, end=700, approximate=True), author="revealed scripture; historical redactors anonymous",
        register="early tantric, significantly non-Pāṇinian",
        sources=[
            dict(type="edition", provider="EFEO", url="https://publications.efeo.fr/en/livres/828_the-ni-v-satattvasa-hit--the-earliest-surviving-aiva-tantra", note="critical edition + annotated translation", tier="C"),
        ],
        translations=[
            dict(language="en", coverage="critical ed. with annotated translation", complete=False, type="scholarly", url="https://publications.efeo.fr/en/livres/828_the-ni-v-satattvasa-hit--the-earliest-surviving-aiva-tantra", tier="C"),
        ],
        verdict="INGEST-GOLD (earliest surviving Śaiva tantra)",
    ),
    dict(
        id="nisvasamukhatattvasamhita", work="Niśvāsamukhatattvasaṃhitā",
        traditions=["early Śaivism"], subschool="interface: Pāśupata/Lākula → Mantramārga",
        period=dict(start=600, end=700, approximate=True), author="scripture; anonymous redactors",
        register="early tantric Sanskrit, irregular",
        sources=[
            dict(type="edition", provider="IFP", url="https://ifpindia.org/bookstore/ci145/", note="critical edition + translation, appendix Śivadharmasaṅgraha 5–9", tier="C"),
        ],
        translations=[
            dict(language="en", coverage="critical ed. with annotated translation", complete=False, type="scholarly", url="https://ifpindia.org/bookstore/ci145/", tier="C"),
        ],
        verdict="INGEST-GOLD (maps Pāśupata/Lākula/Mantramārga against one another)",
    ),
    dict(
        id="atharvavedasaunaka", work="Atharvaveda (Śaunaka recension)",
        traditions=["Vedic"], subschool="Atharvaveda, Śaunaka recension",
        period=dict(start=-1200, end=-900, approximate=True), author="many anonymous ritual-poetic strata",
        register="Vedic Sanskrit, often lexically unusual",
        sources=[
            dict(type="etext", provider="TITUS", url="https://titus.uni-frankfurt.de/texte/etcd/ind/aind/ved/av/avs/avst.htm", tier="C"),
            dict(type="scan", provider="Internet Archive", url="https://archive.org/download/dli.granth.70884/70884.pdf", note="Roth & Whitney edition", tier="C"),
        ],
        translations=[
            dict(language="en", translator="Whitney & Lanman", coverage="complete (2 vols)", complete=True, type="scholarly", url="https://archive.org/details/atharvavedasamhi01whituoft", tier="C"),
            dict(language="en", translator="Ralph T. H. Griffith", coverage="complete", complete=True, type="scholarly", url="https://sacred-texts.com/hin/av/", tier="C"),
        ],
        verdict="INGEST-GOLD (keep Śaunaka + Paippalāda as separate witnesses)",
    ),
    dict(
        id="atharvavedapaippalada", work="Atharvaveda (Paippalāda recension)",
        traditions=["Vedic"], subschool="Atharvaveda, Paippalāda",
        period=dict(end=-1000, approximate=True), author="Anonymous; recension-specific material",
        register="Vedic Sanskrit; recension-specific",
        sources=[
            dict(type="index", provider="UZH", url="https://www.atharvavedapaippalada.uzh.ch/en.html", note="ongoing critical-edition project", tier="C"),
        ],
        translations=[], verdict="INGEST (not a copy of Śaunaka; separate witness)",
    ),
    dict(
        id="satapathabrahmana", work="Śatapatha Brāhmaṇa",
        traditions=["Vedic"], subschool="Śukla Yajurveda; Mādhyaṃdina/Kāṇva recensions",
        period=dict(start=-900, end=-600, approximate=True), author="Anonymous Yājñavalkya-associated tradition",
        register="Developed Brāhmaṇa prose",
        sources=[
            dict(type="etext", provider="GRETIL", url="https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/1_veda/2_bra/satapath/sb_08_u.htm", note="book 8", tier="C"),
            dict(type="etext", provider="GRETIL", url="https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/1_veda/2_bra/satapath/sb_14_u.htm", note="book 14", tier="C"),
        ],
        translations=[
            dict(language="en", translator="Julius Eggeling", coverage="complete", complete=True, type="scholarly", note="SBE series", tier="C"),
        ],
        verdict="INGEST-GOLD (Rudra dossier across Brāhmaṇas)",
    ),
    dict(
        id="satarudriya", work="Śatarudrīya / Śrī Rudram",
        traditions=["Vedic Rudra cult"], subschool="Taittirīya (TS 4.5) + Vājasaneyi (ch. 16)",
        period=dict(approximate=True), author="Anonymous",
        register="Vedic mantra; formula-heavy",
        sources=[
            dict(type="etext", provider="Vignanam", url="https://vignanam.org/media/samskritam/kyts-4.5-namaste-rudra-manyava-krishna-yajurveda-taittiriya-samhita-patha.html", note="TS 4.5 namaste rudra", tier="C"),
            dict(type="index", provider="Vedic Heritage", url="https://vedicheritage.gov.in/samhitas/yajurveda/vajasneyi-madhyandina-samhita/", note="Vājasaneyi ch. 16", tier="D"),
        ],
        translations=[], verdict="INGEST-GOLD (align Śatarudrīya recensions verse-by-verse)",
    ),
]


def _period_json(p) -> str:
    parts = []
    if p.get("start") is not None:
        parts.append(f'"start": {p["start"]}')
    if p.get("end") is not None:
        parts.append(f'"end": {p["end"]}')
    if p.get("approximate"):
        parts.append('"approximate": true')
    return "{" + ", ".join(parts) + "}"


def _sources_js(sources) -> str:
    items = []
    for s in sources:
        parts = [f'"type": "{s["type"]}"', f'"provider": "{s["provider"]}"',
                 f'"url": "{s["url"]}"']
        if s.get("note"):
            parts.append(f'"note": "{s["note"]}"')
        if s.get("tier"):
            parts.append(f'"tier": "{s["tier"]}"')
        items.append("{" + ", ".join(parts) + "}")
    return "[" + ", ".join(items) + "]"


def _translations_js(ts) -> str:
    items = []
    for t in ts:
        parts = [f'"language": "{t["language"]}"']
        if t.get("translator"):
            parts.append(f'"translator": "{t["translator"]}"')
        if t.get("work"):
            parts.append(f'"work": "{t["work"]}"')
        if t.get("coverage"):
            parts.append(f'"coverage": "{t["coverage"]}"')
        parts.append(f'"complete": {str(t.get("complete", False)).lower()}')
        parts.append(f'"type": "{t.get("type", "scholarly")}"')
        if t.get("year"):
            parts.append(f'"year": {t["year"]}')
        if t.get("url"):
            parts.append(f'"url": "{t["url"]}"')
        if t.get("tier"):
            parts.append(f'"tier": "{t["tier"]}"')
        if t.get("note"):
            parts.append(f'"note": "{t["note"]}"')
        items.append("{" + ", ".join(parts) + "}")
    return "[" + ", ".join(items) + "]"


def _record_js(r) -> str:
    lines = [
        '{', f'  "id": "{r["id"]}",',
        f'  "work": "{r["work"]}",',
        f'  "traditions": {json.dumps(r["traditions"], ensure_ascii=False)},',
    ]
    if r.get("subschool"):
        lines.append(f'  "subschool": "{r["subschool"]}",')
    if r.get("period"):
        lines.append(f'  "period": {_period_json(r["period"])},')
    lines.append(f'  "verified": false,')
    lines.append(f'  "state": "seed",')
    lines.append(f'  "author": "{r.get("author", "")}",')
    lines.append(f'  "register": "{r.get("register", "")}",')
    lines.append(f'  "textSources": {_sources_js(r.get("sources", []))},')
    lines.append(f'  "translations": {_translations_js(r.get("translations", []))},')
    has_tr = bool(r.get("translations"))
    status = "complete" if (has_tr and all(t.get("complete") for t in r["translations"])) else ("partial" if has_tr else "none")
    label = ("Complete scholarly English translation located" if status == "complete"
             else ("Partial scholarly English translation located" if status == "partial"
                   else "No complete scholarly English translation located"))
    lines.append(f'  "translationStatus": "{status}",')
    lines.append(f'  "statusLabel": "{label} as of 2026-08-13",')
    lines.append(f'  "statusChecked": "2026-08-13",')
    lines.append(f'  "verdict": "{r.get("verdict", "")}",')
    lines.append('}')
    return "\n".join(lines)


def main() -> int:
    body = ",\n".join("  " + _record_js(r) for r in RECORDS)
    header = (
        "// Auto-generated 2026-08-13: sivaqueue3 (#0–10) + sivaqueue4 (#1–20) census works,\n"
        "// mapped to BibliographyRecord from the sivaqueue3/4 translation guides + companion\n"
        "// (tradition/sub-school, working period, author, parsing register, Sanskrit sources,\n"
        "// English translations + verdict). verified:false = seed.\n"
        "// Generated by pipeline/build_sivaqueue34_atlas.py — do not hand-edit.\n\n"
        'import { BibliographyRecord } from "./bibliographyTypes";\n\n'
        "export const sivaqueue34Seed: BibliographyRecord[] = [\n"
    )
    footer = "\n];\n"
    OUT.write_text(header + body + footer, encoding="utf-8")
    print(f"wrote {OUT} with {len(RECORDS)} records")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
