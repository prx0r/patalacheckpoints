// The audited Trika-10 — the first proper bibliography pass, at full depth.
// Root-vs-commentary are separate records; coverage/style/tier are explicit.
// status_checked: 2026-08-10.

import { BibliographyRecord } from "./bibliographyTypes";

export const audited: BibliographyRecord[] = [
  // ── 1. Mālinīvijayottaratantra ──
  {
    id: "malinivijayottara",
    work: "Mālinīvijayottaratantra",
    traditions: ["Bhairava/Vidyāpīṭha", "Trika"],
    period: { start: 800, end: 950, approximate: true },
    verified: true,
    textSources: [
      { type: "edition", coverage: "complete", provider: "Muktabodha M00160", tier: "B" },
      { type: "critical_edition", coverage: "chs. 1–4, 7, 12–17", editor: "Somadeva Vasudeva", year: 2004, tier: "A" },
    ],
    translations: [
      {
        language: "en",
        translator: "Somadeva Vasudeva",
        work: "The Yoga of the Mālinīvijayottaratantra",
        coverage: "chs. 1–4, 7, 12–17",
        complete: false,
        type: "scholarly",
        year: 2004,
        url: "http://www.ifpindia.org/bookstore/ci97/",
        tier: "A",
      },
    ],
    translationStatus: "partial",
    statusLabel: "Partial English (scholarly: chs. 1–4, 7, 12–17); no complete scholarly English located",
    statusChecked: "2026-08-10",
    statusEvidence: "Vasudeva's IFP/EFEO volume translates chs. 1–4, 7, 12–17, not the complete Tantra; other online renderings unverified.",
    scholarship: [
      { author: "Somadeva Vasudeva", work: "The Yoga of the Mālinīvijayottaratantra", year: 2004, url: "http://publications.efeo.fr/en/livres/618_the-yoga-of-the-malinivijayottaratantra-chapters-1-4-7-i2-17", tier: "A", kind: "study" },
      { work: "Wisdom Library references", url: "http://www.wisdomlib.org/definition/malinivijayottaratantra", tier: "C" },
    ],
    related: ["malinislokavarttika", "tantraloka"],
  },

  // ── 2. Vijñānabhairava ──
  {
    id: "vijnanabhairava",
    work: "Vijñānabhairava",
    traditions: ["Trika"],
    period: { start: 850, end: 950, approximate: true },
    verified: true,
    textSources: [
      { type: "etext", coverage: "complete", provider: "GRETIL (enc. Marino Faliero)", url: "http://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/html/sa_vijJAnabhairava.htm", tier: "B" },
    ],
    translations: [
      { language: "en", translator: "Jaideva Singh", work: "Vijñānabhairava or Divine Consciousness", coverage: "complete", complete: true, type: "traditional", year: 1979, url: "http://www.motilalbanarsidass.com/products/vijnanabhairava-or-divine-consciousness-a-treasury-of-112-types-of-yoga-1", tier: "A", note: "Sanskrit + English + notes" },
      { language: "en", translator: "Bettina Bäumer", work: "Vijñāna Bhairava: The Practice of Centring Awareness", coverage: "complete", complete: true, type: "traditional", year: 2002, url: "http://books.google.com/books?id=lqRGxgEACAAJ", tier: "A", note: "verses; with Swami Lakshman Joo's commentary" },
      { language: "fr", translator: "Lilian Silburn", work: "Le Vijñāna Bhairava", coverage: "complete", complete: true, type: "scholarly", year: 1961, tier: "A" },
    ],
    translationStatus: "complete",
    statusLabel: "Complete English translation, multiple (Singh; Bäumer); complete French (Silburn)",
    statusChecked: "2026-08-10",
    scholarship: [
      { work: "Wisdom Library references", url: "http://www.wisdomlib.org/definition/vijnanabhairava", tier: "C" },
    ],
    notes: ["Translation opportunity: low. Comparative/commentary opportunity: HIGH — do not create another basic translation without comparing against Singh/Bäumer."],
  },

  // ── 3. Parātriṃśikā (root) ──
  {
    id: "paratrisika",
    work: "Parātriṃśikā (root)",
    traditions: ["Trika"],
    period: { start: 800, end: 900, approximate: true },
    verified: true,
    textSources: [
      { type: "etext", coverage: "complete", provider: "Sanskrit Wikisource (export PDF/EPUB/MOBI)", url: "http://sa.wikisource.org/wiki/श्रीपरात्रिंशिका", tier: "B" },
    ],
    translations: [],
    translationStatus: "partial",
    statusLabel: "Root often studied via the Vivaraṇa; see the Vivaraṇa record for complete English",
    statusChecked: "2026-08-10",
    scholarship: [],
    related: ["paratrisikavivarana", "paratrisikalaghuvrtti"],
  },

  // ── 4. Parātriṃśikāvivaraṇa (Abhinavagupta) ──
  {
    id: "paratrisikavivarana",
    work: "Parātriṃśikāvivaraṇa (Abhinavagupta)",
    traditions: ["Trika"],
    period: { start: 975, end: 1025, approximate: true },
    verified: true,
    textSources: [
      { type: "edition", coverage: "complete", editor: "Muktabodha M00154 / KSTS vol. 18", year: 1918, provider: "Wikisource/Muktabodha", url: "http://sa.wikisource.org/wiki/परात्रिंशिका_(तत्त्वविवेकाख्यव्याख्योपेता)", tier: "B" },
    ],
    translations: [
      { language: "en", translator: "Jaideva Singh", work: "Parā-trīśikā-vivaraṇa: The Secret of Tantric Mysticism", coverage: "complete", complete: true, type: "traditional", url: "http://www.motilalbanarsidass.com/products/para-trisika-vivarana-of-abhinavagupta-the-secret-of-tantric-mysticism", tier: "A", note: "Motilal calls it the first English translation; Sanskrit + English" },
      { language: "it", translator: "Raniero Gnoli", coverage: "complete", complete: true, type: "scholarly" },
    ],
    translationStatus: "complete",
    statusLabel: "Complete English (Singh); Italian (Gnoli)",
    statusChecked: "2026-08-10",
    notes: ["Root and Vivaraṇa are separate records — do not collapse."],
    related: ["paratrisika", "paratrisikalaghuvrtti"],
  },

  // ── 5. Tantrāloka ──
  {
    id: "tantraloka",
    work: "Tantrāloka",
    traditions: ["Trika"],
    period: { start: 975, end: 1025, approximate: true },
    verified: true,
    textSources: [
      { type: "etext", coverage: "complete", provider: "GRETIL (Jun Takashima)", url: "http://gretil.sub.uni-goettingen.de/gretilbk.htm", tier: "B" },
      { type: "etext", coverage: "complete", provider: "Wisdom Library verse-reader", url: "http://www.wisdomlib.org/hinduism/book/tantraloka-sanskrit-text", tier: "C" },
    ],
    translations: [
      { language: "en", translator: "Mark Dyczkowski", work: "Tantrāloka, 11 vols (all 37 chapters + Jayaratha's commentary)", coverage: "complete", complete: true, type: "scholarly", url: "http://www.anuttaratrikakula.org/tantraloka-translation/", tier: "D", note: "translates both Abhinavagupta AND Jayaratha" },
      { language: "en", translator: "Satya Prakash Singh / Swami Maheshvarananda", work: "Sri Tantraloka (complete Sanskrit + English)", coverage: "complete", complete: true, type: "scholarly", url: "http://www.wisdomlib.org/hinduism/book/tantraloka-sanskrit-text", tier: "C" },
    ],
    translationStatus: "complete",
    statusLabel: "Complete English root × at least 2; complete English with Jayaratha (Dyczkowski)",
    statusChecked: "2026-08-10",
    statusEvidence: "Dyczkowski's 11 vols cover all 37 chapters and translate both Abhinavagupta and Jayaratha (volume mapping: 1=ch.1, 2=2–3, 3=4, 4=5–6, 5=7–8, 6=9–10, 7=11–14, 8=15, 9=16–27, 10=28–29, 11=30–37).",
    scholarship: [
      { work: "Dyczkowski's lecture/course material (per chapter, with Sanskrit + translation + audio/video)", url: "http://www.anuttaratrikakula.org/course-taa-ch6-overview/", tier: "D", kind: "lecture" },
    ],
    notes: ["Hindi editions exist (Paramahaṃsa Mishra 8 vols; Radheshyam Chaturvedi 5 vols)."],
  },

  // ── 6. Tantrasāra ──
  {
    id: "tantrasara",
    work: "Tantrasāra (Abhinavagupta)",
    traditions: ["Trika"],
    period: { start: 975, end: 1025, approximate: true },
    verified: true,
    textSources: [
      { type: "etext", coverage: "complete", provider: "GRETIL (enc. Oliver Hellwig)", url: "http://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/html/sa_abhinavagupta-tantrasAra.htm", tier: "B" },
    ],
    translations: [
      { language: "en", translator: "H. N. Chakravarty", work: "Tantrasāra of Abhinavagupta (ed. Boris Marjanovic)", coverage: "complete", complete: true, type: "scholarly", url: "http://www.indicabooks.com/product/tantrasara-of-abhinavagupta-copy/", tier: "A" },
    ],
    translationStatus: "complete",
    statusLabel: "Complete English (Chakravarty)",
    statusChecked: "2026-08-10",
    notes: ["Excellent alignment target — the GRETIL prose text is machine-readable."],
  },

  // ── 7. Mālinīślokavārttika ──
  {
    id: "malinislokavarttika",
    work: "Mālinīślokavārttika (Mālinīvijayavārttika)",
    traditions: ["Trika"],
    period: { start: 975, end: 1025, approximate: true },
    verified: true,
    textSources: [
      { type: "critical_edition", coverage: "1.1–1.399", editor: "Jürgen Hanneder", year: 1998, tier: "A", note: "GRETIL: verses 1.1–1.399 = Hanneder's improved critical text; remainder = Madhusudan Kaul Shastri's 1921 KSTS edition." },
      { type: "edition", coverage: "remainder", editor: "Madhusudan Kaul Shastri", year: 1921, tier: "B" },
      { type: "etext", coverage: "complete", provider: "GRETIL (both kāṇḍas)", url: "http://gretil.sub.uni-goettingen.de/gretil/1_sanskr/6_sastra/3_phil/saiva/abhmal1u.htm", tier: "B" },
    ],
    translations: [
      { language: "en", translator: "Jürgen Hanneder", work: "Abhinavagupta's Philosophy of Revelation", coverage: "1.1–1.399", complete: false, type: "scholarly", year: 1998, url: "http://philpapers.org/rec/HANAPO", tier: "A", note: "2023 Brill reissue" },
    ],
    translationStatus: "partial",
    statusLabel: "Partial English: 1.1–1.399 scholarly (Hanneder); remainder no complete English located",
    statusChecked: "2026-08-10",
    notes: ["Extremely good translation target for the remainder; the Sanskrit critical-quality differs by range."],
    related: ["malinivijayottara"],
  },

  // ── 8. Tantrasadbhāva ──
  {
    id: "tantrasadbhava",
    work: "Tantrasadbhāva",
    traditions: ["Bhairava/Vidyāpīṭha", "Trika"],
    period: { start: 800, end: 950, approximate: true },
    verified: true,
    textSources: [
      { type: "manuscript", coverage: "based on three Nepalese MSS", provider: "Hamburg Centre for Tantric Studies" } as any,
    ],
    translations: [
      { language: "en", translator: "Junglan Bang", work: "Selected Chapters from the Tantrasadbhāva (critical edition + translation)", coverage: "chs. 1, part of 3, 9, 18, 28", complete: false, type: "scholarly", url: "http://ediss.sub.uni-hamburg.de/handle/ediss/9642", tier: "A", note: "CC BY 4.0 open-access; with Svacchandalalitabhairava parallels" },
    ],
    translationStatus: "partial",
    statusLabel: "Partial English (open scholarly: selected chapters, CC BY); no complete English located",
    statusChecked: "2026-08-10",
    scholarship: [
      { work: "Hamburg project description", url: "http://www.tantric-studies.uni-hamburg.de/research/post-doc-and-doctoral-research/jung-lan-bang.html", tier: "A", kind: "study" },
      { work: "Wisdom Library references", url: "http://www.wisdomlib.org/definition/tantrasadbhava", tier: "C" },
    ],
    notes: ["Remaining translation opportunity: HUGE. The Bang material is reusable (CC BY) subject to attribution."],
  },

  // ── 9. Śivasūtra + Kṣemarāja's Vimarśinī ──
  {
    id: "sivasutra",
    work: "Śivasūtra + Kṣemarāja's Vimarśinī",
    traditions: ["Trika"],
    period: { start: 850, end: 950, approximate: true },
    verified: true,
    textSources: [
      { type: "etext", provider: "GRETIL / SanskritDocuments", tier: "B" },
    ],
    translations: [
      { language: "en", translator: "Jaideva Singh", work: "Śiva Sūtras: The Yoga of Supreme Identity", coverage: "complete (sūtras + Vimarśinī)", complete: true, type: "traditional", url: "http://www.motilalbanarsidass.com/products/siva-sutras-the-yoga-of-supreme-identity-jaideva-singh", tier: "A", note: "with Sanskrit, word meanings, exposition" },
      { language: "en", translator: "Swami Lakshman Joo", work: "Śiva Sūtras: The Supreme Awakening", coverage: "complete", complete: true, type: "traditional", year: 2007, url: "http://books.google.com/books?id=XIPXAAAAMAAJ", tier: "A", note: "based on oral lectures; prioritizes meaning over literal translation" },
      { language: "en", translator: "Subhash Kak", work: "independent online translation", coverage: "complete", complete: true, type: "independent", url: "http://sanskritdocuments.org/doc_shiva/shivasuutra.html", tier: "D", note: "the page itself distinguishes Kak's from Singh/Dyczkowski" },
    ],
    translationStatus: "complete",
    statusLabel: "Complete English, multiple (Singh; Lakshman Joo; Kak-independent)",
    statusChecked: "2026-08-10",
    notes: ["translation_style distinguishes philological vs traditional-expository vs independent — do not flatten."],
  },

  // ── 10. Spandakārikā + Spandanirṇaya ──
  {
    id: "spandakarika",
    work: "Spandakārikā (root) + Spandanirṇaya (Kṣemarāja commentary)",
    traditions: ["Trika", "Spanda"],
    period: { start: 850, end: 950, approximate: true },
    verified: true,
    textSources: [
      { type: "etext", coverage: "complete", provider: "GRETIL", tier: "B" },
    ],
    translations: [
      { language: "en", translator: "Jaideva Singh", work: "Spanda-kārikās: The Divine Creative Pulsation (kārikās + Spandanirṇaya)", coverage: "complete", complete: true, type: "traditional", url: "http://wellcomecollection.org/works/manv6j64", tier: "A" },
      { language: "en", translator: "Mark Dyczkowski", work: "The Doctrine of Vibration", coverage: "interpretive/translation", complete: true, type: "scholarly", tier: "A" },
    ],
    translationStatus: "complete",
    statusLabel: "Complete English, multiple (Singh; Dyczkowski), incl. the Kṣemarāja commentary",
    statusChecked: "2026-08-10",
    notes: ["Root and commentary are separate records. Comparative terminology value: very high."],
  },

  // ── 11. Parātriṃśikā Laghuvṛtti / Anuttaratattvavimarśinī ──
  {
    id: "paratrisikalaghuvrtti",
    work: "Parātriṃśikā Laghuvṛtti / Anuttaratattvavimarśinī (Abhinavagupta)",
    traditions: ["Trika"],
    period: { start: 975, end: 1025, approximate: true },
    verified: true,
    textSources: [],
    translations: [],
    translationStatus: "none",
    statusLabel: "Complete translation status not yet established — needs a dedicated bibliographic hunt",
    statusChecked: "2026-08-10",
    statusEvidence: "Abhinavagupta wrote TWO commentaries: the short Laghuvṛtti/Anuttaratattvavimarśinī and the large Parātriṃśikāvivaraṇa — keep them distinct.",
    related: ["paratrisika", "paratrisikavivarana"],
    notes: ["Dedicated bibliographic hunt required before marking complete-translation status."],
  },
];
