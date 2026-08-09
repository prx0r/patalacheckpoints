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
