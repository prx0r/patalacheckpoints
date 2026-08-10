import { AtlasEntity } from "@/lib/atlas";

export const texts: AtlasEntity[] = [
  {
    id: "tantraloka",
    type: "text",
    title: "Tantrāloka",
    sanskrit: "तन्त्रालोक",
    period: { start: 975, end: 1025, approximate: true },
    summary:
      "Abhinavagupta's great synthesis — the 'Light on the Tantras', 37 āhnikas, with Jayaratha's 13th-century Viveka commentary. Four books at once: a theory of liberating knowledge, a total map of manifestation, a ritual technology of subject reconstruction, and a politics of scriptural authority.",
    concepts: ["anuttara", "kula", "visarga", "svātantrya", "upāya"],
    resources: [
      { title: "Tantrāloka āhnika 1 (our T1)", href: "/texts/tantraloka", type: "translation" },
      { title: "Dyczkowski 11 vols", href: "/texts/tantraloka", type: "scholarship" },
    ],
    dossier: {
      systemicFunction:
        "The whole work in seed form is āhnika 1: it establishes the problem, goal, terminology, authority, chapter sequence, and the relation between liberating knowledge and the ritual system.",
      doctrinalCore: [
        "The Unsurpassed (anuttara) as the ground",
        "The four upāyas (anupāya, śāmbhava, śākta, āṇava)",
        "The Mālinīvijayottara as the source-scripture",
      ],
      outputs: ["the 37-āhnika map", "the four-upāyas dossier", "the recognition-dependency tree"],
    },
  },
  {
    id: "mahanayaprakasha",
    type: "text",
    title: "Mahānayaprakāśa",
    sanskrit: "महानयप्रकाश",
    period: { start: 900, end: 1100, approximate: true },
    summary:
      "The Krama crown — the single highest-value untranslated text in the corpus. Rājānaka Śitikaṇṭhācārya's illumination of the Great Way, with the author's own commentary interleaved. The daśākhaṇḍa (ten Kālīs of cognition) and the four-egg cosmology.",
    concepts: ["saṃvit", "krama", "kālī", "daśākhaṇḍa"],
    dossier: {
      systemicFunction:
        "The Mahānayaprakāśa is the Krama's philosophical synthesis — the process-based reading of liberation as cognition-sequence. Its opening (our T1) establishes the goddess-energies and the cosmology.",
      doctrinalCore: [
        "The ten divisions (daśākhaṇḍa) of cognition's illumination",
        "The four-egg (caturaṇḍā) cosmology with the six courses",
        "The Uḍḍiyāna-seat and the akula/kula pair",
      ],
      outputs: ["the opening T1", "the daśākhaṇḍa dossier", "the Krama-cosmology map"],
    },
  },
  {
    id: "maharthamanjari",
    type: "text",
    title: "Mahārthamañjarī",
    sanskrit: "महार्थमञ्जरी",
    period: { start: 1000, end: 1200, approximate: true },
    summary:
      "Maheśvarānanda's 70-gāthā Krama tantra with his own Parimala commentary. The Krama's theology at its peak — the spanda-principle, the cognition-sequence, and the explicit yoking of the Krama-path to the Śivadṛṣṭi and the Pratyabhijñā.",
    concepts: ["spanda", "saṃvit", "krama", "vimarśa"],
    resources: [
      { title: "The maṅgala T3 (our work)", href: "/texts/maharthamanjari", type: "translation" },
      { title: "The Parimala (Trivandrum Series)", href: "/texts/maharthamanjari", type: "scholarship" },
    ],
    dossier: {
      systemicFunction:
        "The Mahārthamañjarī is the first Krama text fully anchor-backed in our corpus — its own Parimala is the referee. The maṅgala establishes the pulse-register (spanda as cognition's rhythm) and the guru-as-krama.",
      doctrinalCore: [
        "The pulse, the pulse's rest, the pulse's outpouring",
        "The prakāśa suffused-with-reflexion as the engine",
        "The heart's pulse (hṛdaya-parispanda) as the only śāstra",
      ],
      outputs: ["the maṅgala T3", "the spanda-dossier", "the Krama-perspective cycle"],
    },
  },
  {
    id: "kubjikamata",
    type: "text",
    title: "Kubjikāmata",
    sanskrit: "कुब्जिकामत",
    period: { start: 950, end: 1100, approximate: true },
    summary:
      "The principal scripture of the Kubjikā tradition (Paścimāmnāya), ~3,000 verses in the Kulālikāmnāya version. Its maṅgala juxtaposes akula and kula in a compressed cosmology; its paṭala 1 culminates in the phonemic Rudraśakti's emergence (Mālinī).",
    concepts: ["mālinī", "kula", "akula", "mātṛkā"],
    resources: [
      { title: "Paṭala 1 (our T1)", href: "/texts/kubjikamata", type: "translation" },
      { title: "GRETIL (Goudriaan–Schoterman)", href: "/texts/kubjikamata", type: "scholarship" },
    ],
    dossier: {
      systemicFunction:
        "The Kubjikāmata is the report's A+ text for the whole Kubjikā tradition — the root scripture that reworks Trika material into the Kubjikā's own system. The phonemic Mālinī and the mantra-body are its distinctive contribution.",
      doctrinalCore: [
        "The akula/kula cosmology in the maṅgala",
        "The phonemic Rudraśakti: the goddess of all syllables",
        "The siddha-krama as the secret order",
      ],
      outputs: ["paṭala 1 T1", "the phonemic dossiers", "the Kulālikāmnāya map"],
    },
  },
  {
    id: "kaulajnananirnaya",
    type: "text",
    title: "Kaulajñānanirṇaya",
    sanskrit: "कौलज्ञाननिर्णय",
    period: { start: 950, end: 1100, approximate: true },
    summary:
      "The Matsyendra-bundle's core text — the 'Determination of the Kaula Knowledge', 24 paṭalas. Its doctrines (the jñāna/kriyā/icchā descent-chain, the kula-terminology, the body-geography) anchor the whole Kaula layer, with the Bagchi 1934 print as the collation-referee.",
    concepts: ["kula", "yoginī", "dīkṣā", "jñāna"],
    dossier: {
      systemicFunction:
        "The KJN is the bundle's anchor — its vocabulary is the Kaula register's entry-ticket, and its Bagchi-print collation resolves the bundle's [X]-flags.",
      doctrinalCore: [
        "The descent-chain jñāna ⊃ kriyā ⊃ icchā ⊃ tejas",
        "The kula as the transmission's body",
        "The 'by mere knowledge' thesis (the vidyā-śravaṇa)",
      ],
      outputs: ["the 24-paṭala T1", "the Bagchi collation", "the kula-dossier"],
    },
  },
  {
    id: "spandakarika",
    type: "text",
    title: "Spandakārikā",
    sanskrit: "स्पन्दकारिका",
    period: { start: 850, end: 950, approximate: true },
    summary:
      "The 53 verses of the Spanda, traditionally attributed to Vasugupta, with four commentaries (the anchor is Dyczkowski's Stanzas on Vibration). The pulse-theology: Śiva as the source of the wheel of powers, the perceiver's unswerving nature.",
    concepts: ["spanda", "śakti", "cakra"],
    dossier: {
      systemicFunction:
        "The Spandakārikā is the Spanda current's root — the wheel-of-energies cosmology and the pulse-language that the Krama and Trika both draw on.",
      doctrinalCore: [
        "The wheel of powers whose source is Śaṅkara",
        "The unobstructed nature → no obstruction anywhere",
        "The perceiver never deviates from his own nature",
      ],
      outputs: ["the 53-verse translation", "the spanda-dossier", "the four-commentary anchor-check"],
    },
  },
];
// The T3'd / T1'd additions from the translation project (2026-08-09)
export const textsAdditional: import("@/lib/atlas").AtlasEntity[] = [
  {
    id: "jnanakarika",
    type: "text",
    title: "Jñānakārikā",
    sanskrit: "ज्ञानकारिका",
    period: { start: 950, end: 1100, approximate: true },
    summary:
      "The Verses of Knowledge — the Matsyendra-bundle's third text, fully T3'd. The kārikā-register: the dvandva-doctrine, the dharmādharma-discrimination, and the caryā's interiorized body-geography (the body as śmaśāna, liṅga, vṛkṣa-mūla).",
    concepts: ["kula", "śūnya", "krama"],
    resources: [
      { title: "The full T3 (paṭalas 1–3)", href: "/texts/jnanakarika", type: "translation" },
    ],
    dossier: {
      systemicFunction: "The bundle's knowledge-path: 'by mere knowledge alone, liberation arises for the yogins' (1/11).",
      doctrinalCore: [
        "The both/neither apophasis — neither the mind nor its absence",
        "The dharmādharma-pair as the two bonds, cut by the sword of knowledge",
        "The interiorized geography: the body as the rite's locus",
      ],
      outputs: ["the T3-FINAL (3 paṭalas)", "the dvandva-dossier"],
    },
  },
  {
    id: "ajadapramatrsiddhi",
    type: "text",
    title: "Ajaḍapramātṛsiddhi",
    sanskrit: "अजडप्रमातृसिद्धि",
    period: { start: 925, end: 975, approximate: true },
    summary:
      "Utpaladeva's 'Establishment of the Non-Inert Knower' — the Siddhitrayī's core, key-verses T3'd. The anti-inert-light argument: the non-reflexive consciousness is crystal-like, hence inert.",
    concepts: ["recognition", "vimarśa", "prakāśa"],
    resources: [
      { title: "The key-verses T3", href: "/texts/ajadapramatrsiddhi", type: "translation" },
      { title: "The 1921 Kashmir Series", href: "/texts/ajadapramatrsiddhi", type: "scholarship" },
    ],
    dossier: {
      systemicFunction: "The report's A+ Pratyabhijñā control — the A-thesis (reflexive presence) established, the universalization (C) honestly OPEN.",
      doctrinalCore: [
        "Existence as manifestation (prakhyā-upākhyā)",
        "The 'I am this' — the segmented this grounded in the I",
        "The non-reflexive light is like a sky-flower: unable to establish anything",
      ],
      outputs: ["the key-verses T3", "the A/B/C stratification"],
    },
  },
  {
    id: "kaularahasya",
    type: "text",
    title: "Kaularahasya",
    sanskrit: "कौलरहस्य",
    period: { start: 1000, end: 1300, approximate: true },
    summary:
      "The Secret of the Kaula [path] — the vāma-mārga's self-defense and the dīkṣā-theology. Paṭalas 1–5 T1'd: the makāra-rites, the āmnāya-geography, the sāmrājya-dīkṣā's culmination.",
    concepts: ["kula", "cakra", "mantra", "vāma"],
    resources: [
      { title: "Paṭalas 1–5 (T1)", href: "/texts/kaularahasya", type: "translation" },
    ],
    dossier: {
      systemicFunction: "The rahasya-genre's defense of the left-hand path — the dīkṣā as absolutely required, the paśu's exclusion.",
      doctrinalCore: [
        "The vāma/dakṣiṇa path-discrimination across the āmnāyas",
        "The dīkṣā's ten saṃskāras and the sāmrājya-hierarchy",
        "The eclipse-dīkṣā (the sun = Śiva, the moon = śakti)",
      ],
      outputs: ["the paṭalas 1–5 T1", "the dīkṣā-theology map"],
    },
  },
  {
    id: "kulapradipa",
    type: "text",
    title: "Kulapradīpa",
    sanskrit: "कुलप्रदीप",
    period: { start: 1500, end: 1800, approximate: true },
    summary:
      "Śivānandācārya's Lamp of the Kula — the consolidated kula-orthodoxy's self-praise, 7 prakāśas. Prakāśas 1–2 T1'd: the path-hierarchy, the Kaulika's encomium, the bhoga-yoga.",
    concepts: ["kula", "krama", "cakra"],
    resources: [
      { title: "Prakāśas 1–2 (T1)", href: "/texts/kulapradipa", type: "translation" },
    ],
    dossier: {
      systemicFunction: "The kula-dharma's encomium — the Kaulika as the vessel, the Kulārṇava-quoted authority.",
      doctrinalCore: [
        "The path-hierarchy ending in the Kaula",
        "The bhoga-yoga: enjoyment becomes yoga directly",
        "The Kaulika's presence purifies the land",
      ],
      outputs: ["the prakāśas 1–2 T1", "the kula-dharma dossier"],
    },
  },
  {
    id: "kubjikatantra",
    type: "text",
    title: "Kubjikātantra",
    sanskrit: "कुब्जिकातन्त्र",
    period: { start: 950, end: 1200, approximate: true },
    summary:
      "The Kubjikā tradition's own tantra (17 paṭalas, T1'd) — distinct from the Kubjikāmata. The vidyā-śravaṇa (liberation by hearing), the Daśamahāvidyā-list, the yonimudrā.",
    concepts: ["mālinī", "kula", "yoginī"],
    dossier: {
      systemicFunction: "The Kubjikā's independent tantra — the hearing-liberation and the goddess-lists.",
      doctrinalCore: ["the vidyā-śravaṇa: liberation by hearing alone", "the yonimudrā", "the Daśamahāvidyā"],
      outputs: ["the 17-paṭala T1"],
    },
  },
  {
    id: "sivasutra",
    type: "text",
    title: "Śivasūtra",
    sanskrit: "शिवसूत्र",
    period: { start: 850, end: 950, approximate: true },
    summary:
      "The 78 sūtras of the Trika's foundation with Bhāskara's Vārttika — T3'd (the anchored text). The ŚS 1.3's yoni-varga, the mātṛkā-cakra, the icchā-as-Umā. Anchored by Dyczkowski's Aphorisms of Śiva.",
    concepts: ["mātṛkā", "śakti", "kula"],
    resources: [
      { title: "The ŚS + Vārttika T3", href: "/texts/sivasutra", type: "translation" },
      { title: "Dyczkowski's Aphorisms", href: "/texts/sivasutra", type: "scholarship" },
    ],
    dossier: {
      systemicFunction: "The Trika's foundational scripture — the error-measurement's anchored test-case (0% error vs Dyczkowski).",
      doctrinalCore: [
        "The yoni-varga as the body of the kalās (1.3)",
        "Mātṛkā as the ground of knowledge (1.4)",
        "The perceiver's unswerving nature",
      ],
      outputs: ["the T3 (78 sūtras)", "the error-measurement", "the anchored R2"],
    },
  },
  {
    id: "cidgaganacandrika",
    type: "text",
    title: "Cidgaganacandrikā",
    sanskrit: "चिद्गगनचन्द्रिका",
    period: { start: 1100, end: 1300, approximate: true },
    summary:
      "The 'Moonbeam of the Sky of Consciousness' — the Krama's cosmology-stotra in 312 verses, attributed to Kālidāsa (the 'Śrīvatsa' of the closing), a eulogy of Parāśakti that is also a commentary on Siddhanātha's Kramastuti. Our T1-FULL is a likely first English verse-translation (the Trivikrama 1937 volume is an edition + study, not a translation).",
    concepts: ["prakāśa", "vimarśa", "khecarī", "śūnya", "krama"],
    resources: [
      { title: "Cidgaganacandrikā (our T1-FULL, 312 vv)", href: "/texts/cidgaganacandrika", type: "translation" },
      { title: "Trivikrama Tirtha 1937 (edition + study)", href: "/texts/cidgaganacandrika", type: "scholarship" },
    ],
    dossier: {
      systemicFunction:
        "The Cidgaganacandrikā is the Krama's cosmology in praise-form: the four goers (khecarī, bhūcarī, dikcarī, gocarī), the Kālasaṃkarṣiṇī, and the whole manifestation-order (dhāma/varṇa/saṃvit) sung as the Goddess.",
      doctrinalCore: [
        "The consciousness-sky (cidgagana) and its moonbeam (the Goddess)",
        "The four goers as the senses' powers",
        "The Kālasaṃkarṣiṇī (the time-drawer) as the devouring terminus",
        "The attribution: Kālidāsa/Śrīvatsa, a Kramastuti-commentary",
      ],
      outputs: ["the T1-FULL (312 vv)", "the four-goers dossier", "the khecaratā-verse's cross-text"],
    },
  },
  {
    id: "kakacandeshvarimata",
    type: "text",
    title: "Kākacaṇḍeśvarīmata",
    sanskrit: "काकचण्डेश्वरीमत",
    period: { start: 1000, end: 1200, approximate: true },
    summary:
      "The 'Doctrine of Kākacaṇḍeśvarī' (the Crow-goddess) — the Krama's practical/alchemical layer in 57 paṭalas: the jīva-doctrine opening, then the rasa-śāstra (the mercury's eighteen operations, the guṭikās, the amaratva-kalpas, the kāyacikitsā). Diglossic — Sanskrit doctrine + Hindavi recipes. A genuine first-translation.",
    concepts: ["krama", "śakti", "cakra", "khecarī", "mantra"],
    resources: [
      { title: "Kākacaṇḍeśvarīmata (our T1-FULL, 57 paṭalas)", href: "/texts/kakacandeshvarimata", type: "translation" },
    ],
    dossier: {
      systemicFunction:
        "The Kākacaṇḍeśvarīmata is the Krama's practical pole: where the MNP gives the philosophy, this gives the sādhana — the substance-means (dravya-upāya) to the immortal body, from the jīva's bondage to the siddha's vajra-body.",
      doctrinalCore: [
        "The jīva's bondage and the dravya-upāya (the substance-means)",
        "The aṣṭādaśa-karma (the mercury's eighteen operations)",
        "The khecaratva and the amaratva (the sky-going, the deathlessness)",
        "The diglossia: Sanskrit doctrine + Hindavi recipes",
      ],
      outputs: ["the T1-FULL (57 paṭalas)", "the alchemical operations", "the Hindavi-recipe register"],
    },
  },
  {
    id: "nitya_shodasikarnava",
    type: "text",
    title: "Nityāṣoḍaśikārṇava",
    sanskrit: "नित्याषोडशिकार्णव",
    period: { start: 900, end: 1100, approximate: true },
    summary:
      "The 'Ocean of the Sixteen Nityās' — the Śrīvidyā's first part (the Yoginīhṛdaya the second, per the Cambridge MS-OR-00156, Kathmandu 1346 CE). The cakra-worship of Tripurasundarī, with Bhāskararāya's Setubandha commentary. Our T1-FULL covers the pūrva's 8 paṭalas (212 vv) — a genuine first English translation.",
    concepts: ["cakra", "krama", "mantra", "śakti"],
    resources: [
      { title: "Nityāṣoḍaśikārṇava pūrva (our T1-FULL, 212 vv)", href: "/texts/nitya_shodasikarnava", type: "translation" },
    ],
    dossier: {
      systemicFunction:
        "The Nityāṣoḍaśikārṇava is the Śrīvidyā's ritual-theology: the śrīcakra's geometric construction (the 43 triangles), the vāgdevatā-octad, the pañcadaśī's kūṭas, and the āvaraṇas' worship — the text the Yoginīhṛdaya presupposes.",
      doctrinalCore: [
        "The śrīcakra's construction (the five-śakti × four-fire)",
        "The vāgdevatā-octad and the pañcadaśī's kūṭas",
        "The dhyāna of the red Tripurasundarī",
        "The commentary-dependency: the Setubandha's numbers are required",
      ],
      outputs: ["the T1-FULL (212 vv)", "the cakra-arithmetic", "the vāgdevatā-octad dossier"],
    },
  },
  {
    id: "yoginihrdaya",
    type: "text",
    title: "Yoginīhṛdaya",
    sanskrit: "योगिनीहृदय",
    period: { start: 1100, end: 1200, approximate: true },
    summary:
      "The 'Heart of the Yoginī' — the Śrīvidyā's second part (the Nityāṣoḍaśikārṇava the first, per the Cambridge MS-OR-00156). The Vāmakeśvara's inner text, with Amṛtānanda's Dīpikā. Anchored, not translated by us: Padoux's *The Heart of the Yoginī* (OUP 2013) is the full translation.",
    concepts: ["cakra", "kula", "prakāśa", "vimarśa"],
    resources: [
      { title: "Padoux, The Heart of the Yoginī (OUP 2013)", href: "/texts/yoginihrdaya", type: "translation" },
    ],
    dossier: {
      systemicFunction:
        "The Yoginīhṛdaya is the Śrīvidyā's heart-text — the cakra-saṃketa, mantra-saṃketa, and pūjā-saṃketa of Tripurasundarī. Its Dīpikā (Amṛtānanda) cites the Cidgaganacandrikā by name, linking the Krama and the Śrīvidyā.",
      doctrinalCore: [
        "The three saṃketas (cakra, mantra, pūjā)",
        "The kāmakalā and the baindava-cakra",
        "The Dīpikā's Cidgaganacandrikā-citations",
      ],
      outputs: ["the anchored reference (Padoux)", "the three-saṃketa map"],
    },
  },
];
