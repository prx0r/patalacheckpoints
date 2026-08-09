import { AtlasEntity } from "@/lib/atlas";

export const traditions: AtlasEntity[] = [
  {
    id: "trika",
    type: "tradition",
    title: "Trika",
    sanskrit: "त्रिक",
    period: { start: 850, end: 1050, approximate: true },
    summary:
      "The Trika is the 'triad' tradition of Kashmir — the three goddesses (Parā, Parāparā, Aparā) assimilated to Kālī systems and philosophically reconstructed on Pratyabhijñā foundations by Abhinavagupta. The calibration layer of the whole corpus.",
    concepts: ["prakāśa", "vimarśa", "anuttara", "kula"],
    resources: [
      { title: "Tantrāloka (Dyczkowski)", href: "/texts/tantraloka", type: "translation" },
      { title: "The recognition enquiry", href: "/concepts/recognition", type: "explainer" },
    ],
    dossier: {
      systemicFunction:
        "The Trika is the calibration layer — its Tantrāloka supplies the doctrinal oracle for the whole corpus, and its technical vocabulary (prakāśa, vimarśa, svātantrya, kula) is the Rosetta layer for the other traditions.",
      doctrinalCore: [
        "Consciousness is intrinsically reflexive (prakāśa-vimarśa)",
        "The Unsurpassed (anuttara) is the ground of the powers",
        "The kula/akula polarity: the manifest pole and the transcendent pole",
      ],
      outputs: ["the Tantrāloka's 37 āhnikas mapped", "the glossary dossiers", "the recognition thesis"],
    },
  },
  {
    id: "krama",
    type: "tradition",
    title: "Krama",
    sanskrit: "क्रम",
    period: { start: 800, end: 1200, approximate: true },
    summary:
      "The Krama ('sequence') tradition is a highly internalized Kālī-oriented system: the perceptible order of worship corresponds to the imperceptible sequence of cognition. Sequence IS cognition — the Kālīs are moments of cognition, not merely goddesses.",
    concepts: ["saṃvit", "krama", "kālī", "spanda"],
    resources: [
      { title: "Mahānayaprakāśa", href: "/texts/mahanayaprakasha", type: "translation" },
      { title: "Mahārthamañjarī", href: "/texts/maharthamanjari", type: "translation" },
    ],
    dossier: {
      systemicFunction:
        "The Krama is the process-based corrective to a 'single static witness' metaphysics. Its core move: the pūjā-krama (ritual order) reflects the saṃvit-krama (cognition-sequence).",
      doctrinalCore: [
        "The ten Kālīs as ten moments of cognition (daśākhaṇḍa)",
        "The saṃvit-krama: cognition as sequence",
        "The Mahānaya/Mahārtha path as the crown",
      ],
      outputs: ["the daśākhaṇḍa mapped", "the cognition-sequence dossiers", "the process-based reading of liberation"],
    },
  },
  {
    id: "kubjika",
    type: "tradition",
    title: "Kubjikā",
    sanskrit: "कुब्जिका",
    period: { start: 950, end: 1300, approximate: true },
    summary:
      "The Kubjikā tradition belongs to the Western Transmission (Paścimāmnāya). It reworks Trika material into a newly constituted deity-mantra-yoga-ritual system, with the goddess Kubjikā and the phonemic Mālinī at its center. Preserved overwhelmingly in Nepal.",
    concepts: ["mālinī", "mātṛkā", "khecarī", "mantra"],
    resources: [
      { title: "Kubjikāmata paṭala 1", href: "/texts/kubjikamata", type: "translation" },
    ],
    dossier: {
      systemicFunction:
        "The Kubjikā is the specialist corpus — the Western Transmission's own system, closely connected to the Trika but independently elaborated. Its phonemic goddess (Mālinī) and mantra-body doctrine are the report's flagged A+ material.",
      doctrinalCore: [
        "The phonemic Rudraśakti: the goddess of the syllables",
        "The mantra-body (mantradeha) as the kula-formed body",
        "The akula/kula cosmology in the maṅgala",
      ],
      outputs: ["the Kubjikāmata's 25 paṭalas", "the phonemic dossiers", "the Nepalese-transmission map"],
    },
  },
  {
    id: "kaula",
    type: "tradition",
    title: "Kaula",
    sanskrit: "कौल",
    period: { start: 900, end: 1200, approximate: true },
    summary:
      "The Kaula is the reformulation of the Yoginī-cult traditions into a domesticated path for householders. It preserves the lineage-family sense of kula while deliberately extending it toward the body, power, and the totality of phenomena.",
    concepts: ["kula", "yoginī", "dīkṣā", "vāma"],
    resources: [
      { title: "Kaulajñānanirṇaya", href: "/texts/kaulajnananirnaya", type: "translation" },
      { title: "Kaularahasya", href: "/texts/kaularahasya", type: "translation" },
    ],
    dossier: {
      systemicFunction:
        "The Kaula is the reformulation-node: the Yoginī-cult's kaula-path made accessible, the vāma-mārga defended, the dīkṣā-theology built. The Matsyendra-bundle (KJN, Akulavīra, Jñānakārikā) is its scripture.",
      doctrinalCore: [
        "The kula as lineage AND body AND totality",
        "The vāma/dakṣiṇa path-discrimination",
        "The dīkṣā as absolutely required",
      ],
      outputs: ["the bundle's T3s", "the kula-dossier", "the dīkṣā-theology map"],
    },
  },
  {
    id: "spanda",
    type: "tradition",
    title: "Spanda",
    sanskrit: "स्पन्द",
    period: { start: 850, end: 1000, approximate: true },
    summary:
      "The Spanda ('pulse') current around the Śivasūtra and Spandakārikā: the dynamic pulse of the fundamental conscious reality. A post-scriptural doctrinal development, not a revealed sect — it supplies the language of dynamism that the Krama and Trika both draw on.",
    concepts: ["spanda", "śakti", "svātantrya"],
    dossier: {
      systemicFunction:
        "Spanda is the control corpus's dynamism-pole: consciousness as the pulse (spanda), not a static witness. The Spandakārikā with four commentaries is the anchor.",
      doctrinalCore: [
        "The wheel of powers (śakticakra) whose source is Śiva",
        "The pulse (spanda) as constitutive of manifestation and cognition",
        "The perceiver never deviates from his own nature",
      ],
      outputs: ["the Spandakārikā's 53 verses", "the spanda-dossier", "the four-commentary map"],
    },
  },
  {
    id: "pratyabhijna",
    type: "tradition",
    title: "Pratyabhijñā",
    sanskrit: "प्रत्यभिज्ञा",
    period: { start: 900, end: 1025, approximate: true },
    summary:
      "The Pratyabhijñā ('Recognition') philosophical system of Somānanda → Utpaladeva → Abhinavagupta: liberation is recognition of an identity already obtaining. It runs sideways through the entire project as the semantic control corpus.",
    concepts: ["recognition", "vimarśa", "prakāśa", "svātantrya"],
    dossier: {
      systemicFunction:
        "Pratyabhijñā is best modeled as a philosophical/exegetical current intersecting Trika, not another directional Kaula āmnāya. It gives unusually precise philosophical definitions that anchor the technical vocabulary.",
      doctrinalCore: [
        "Recognition = transformation + reidentification + veridicality + stabilization",
        "The A/B/C stratification: reflexive presence, ownership, universalization",
        "Existence as manifestation (prakhyā-upākhyā)",
      ],
      outputs: ["the ĪPK + the Siddhitrayī", "the A/B/C dossier", "the recognition-frame"],
    },
  },
  {
    id: "sarvamnyaya",
    type: "tradition",
    title: "Sarvāmnāya / Newar",
    sanskrit: "सर्वाम्नाय",
    period: { start: 1200, end: 1700, approximate: true },
    summary:
      "The Nepalese multi-āmnāya syntheses: traditions that deliberately combine Kubjikā, Kālī, Tripurā, Siddhalakṣmī and others into integrated systems. The endgame of the corpus — where incompatible systems were made mutually translatable by practitioners themselves.",
    concepts: ["kula", "yoginī", "pīṭha"],
    dossier: {
      systemicFunction:
        "The Sarvāmnāya tests whether the semantic model can recognise several traditions being deliberately combined — the crosswalk layer.",
      doctrinalCore: ["the multi-āmnāya ritual systems", "the preservation of the lost material"],
      outputs: ["the Newar paddhatis map", "the cross-āmnāya synthesis dossier"],
    },
  },
];
