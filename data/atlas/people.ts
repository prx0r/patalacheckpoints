import { AtlasEntity } from "@/lib/atlas";

export const people: AtlasEntity[] = [
  {
    id: "abhinavagupta",
    type: "person",
    title: "Abhinavagupta",
    sanskrit: "अभिनवगुप्त",
    period: { start: 975, end: 1025, approximate: true },
    summary:
      "The great synthesis-node of the Trika (c. 975–1025). His Tantrāloka integrates the three goddesses' cult, the Kālī systems, Kaula practice, Pratyabhijñā metaphysics, and Spanda language into one system. He must be read as a synthesis-node, not a transparent witness to all earlier Tantra.",
    concepts: ["anuttara", "prakāśa", "vimarśa", "upāya"],
    dossier: {
      systemicFunction:
        "Abhinavagupta is the major synthesis-node: every earlier scripture and current converges on his Tantrāloka. The commentary-rule: 'This is an earlier scriptural use. Abhinava later interprets a related expression as X' — never the reverse.",
      doctrinalCore: [
        "The concentrated worship of Parā as the solitary heroine (Ekavīrā)",
        "The four upāyas as differently actualized under contraction",
        "The kula/akula metaphysical polarity",
      ],
      outputs: ["the Tantrāloka's 37 āhnikas", "the four-upāyas dossier", "the synthesis-map"],
    },
  },
  {
    id: "utpaladeva",
    type: "person",
    title: "Utpaladeva",
    sanskrit: "उत्पलदेव",
    period: { start: 925, end: 975, approximate: true },
    summary:
      "The developer of the classical Pratyabhijñā system (c. 925–975). His Īśvarapratyabhijñā and the Siddhitrayī (including the Ajaḍapramātṛsiddhi) establish recognition as reidentification of an already-existing identity.",
    concepts: ["recognition", "vimarśa", "svātantrya"],
    dossier: {
      systemicFunction:
        "Utpaladeva founds the philosophical core the report stratifies into A (reflexive presence), B (ownership), C (universalization). The Ajaḍapramātṛsiddhi's anti-inert-light argument is the A-thesis's sharpest statement.",
      doctrinalCore: [
        "Existence as manifestation (prakhyā-upākhyā)",
        "The 'I am this' — the segmented this grounded in the I",
        "The non-reflexive light is crystal-like, hence inert",
      ],
      outputs: ["the A/B/C stratification", "the Siddhitrayī", "the recognition-frame"],
    },
  },
  {
    id: "somananda",
    type: "person",
    title: "Somānanda",
    sanskrit: "सोमानन्द",
    period: { start: 900, end: 950, approximate: true },
    summary:
      "The opener of the Pratyabhijñā trajectory (c. 900–950), author of the Śivadṛṣṭi. Stronger on divine identity than on the later phenomenology of recognition; his work's full passage-extraction requires the Nemec edition (ACQ).",
    concepts: ["recognition", "prakāśa"],
    dossier: {
      systemicFunction:
        "Somānanda initiates the philosophical stage; the report flags that he is stronger on divine identity than the later recognition-phenomenology.",
      doctrinalCore: ["the Śivadṛṣṭi's divine-identity framing"],
      outputs: ["the Śivadṛṣṭi passage-work (pending Nemec)"],
    },
  },
  {
    id: "jnananetra",
    type: "person",
    title: "Jñānanetra / Śivānanda",
    sanskrit: "ज्ञाननेत्र",
    period: { start: 800, end: 850, approximate: true },
    summary:
      "The chartable origin of the Krama's history (first half of the 9th century). His lineage-traditions connect with Oḍḍiyāna; the Devīpañcaśataka and Kramasadbhāva are the Krama's scriptural prototypes.",
    concepts: ["krama", "kālī"],
    dossier: {
      systemicFunction:
        "Jñānanetra marks the beginning of the Krama's chartable history — the report's earliest datable Krama node.",
      doctrinalCore: ["the Krama's Oḍḍiyāna-origin memory", "the scriptural prototypes"],
      outputs: ["the Krama-timeline's origin-node"],
    },
  },
  {
    id: "jayaratha",
    type: "person",
    title: "Jayaratha",
    sanskrit: "जयरथ",
    period: { start: 1225, end: 1275, approximate: true },
    summary:
      "The 13th-century author of the Tantrāloka's great commentary, the Viveka — the exegetical culmination of the Trika. His commentary accompanies the GRETIL Tantrāloka and is the doctrinal referee for reading Abhinavagupta.",
    concepts: ["prakāśa", "upāya"],
    dossier: {
      systemicFunction:
        "Jayaratha's Viveka is the late exegetical layer — the KSTS edition's commentary that glosses the Tantrāloka verse-by-verse.",
      doctrinalCore: ["the Tantrāloka's verse-by-verse gloss"],
      outputs: ["the commentary-map", "the doctrinal referee"],
    },
  },
  {
    id: "dyczkowski",
    type: "person",
    title: "Mark Dyczkowski",
    sanskrit: "मार्क ड्यचकोवस्की",
    period: { start: 1952, end: 2025, approximate: false },
    summary:
      "The modern curatorial force behind our corpus. His research collection and Muktabodha's e-text selection (2004–2018) curated the 'ever expanding circles' of tantric literature; his translations (Tantrāloka 11 vols, Aphorisms of Śiva, Stanzas on Vibration, Manthānabhairavatantram) are our anchors.",
    concepts: ["kula", "krama", "mālinī"],
    dossier: {
      systemicFunction:
        "Dyczkowski belongs in the modern reception/curation graph, separate from historical influence. The selection-effect caveat: our corpus counts measure curation, not historical influence.",
      doctrinalCore: ["the 500-text curated corpus", "the tantric anchors"],
      outputs: ["the anchors registry", "the selection-effect caveat"],
    },
  },
  {
    id: "maheshvarananda",
    type: "person",
    title: "Maheśvarānanda",
    sanskrit: "महेश्वरानन्द",
    period: { start: 1000, end: 1200, approximate: true },
    summary:
      "The author of the Mahārthamañjarī with its own Parimala commentary — the Krama's theology at its peak. He explicitly yokes the Krama-path to the Śivadṛṣṭi and the Pratyabhijñā, making the report's 'Pratyabhijñā running sideways' the text's own self-positioning.",
    concepts: ["krama", "spanda", "vimarśa"],
    dossier: {
      systemicFunction:
        "Maheśvarānanda is the Krama's self-commentator — his Parimala is the referee that lets us read the Krama from within, not through imported Trika assumptions.",
      doctrinalCore: [
        "The heart's pulse (hṛdaya-parispanda) as the only śāstra",
        "The guru-as-krama (the cognition-sequence's living reflexion)",
      ],
      outputs: ["the 70-gāthā tantra", "the Parimala anchor", "the Krama-perspective cycle"],
    },
  },
];
