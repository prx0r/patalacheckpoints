import { AtlasEntity } from "@/lib/atlas";

export const concepts: AtlasEntity[] = [
  {
    id: "kula",
    type: "concept",
    title: "Kula",
    sanskrit: "कुल",
    period: { start: 800, end: 1300, approximate: true },
    summary:
      "Kula is the semantic chameleon of the whole corpus: Yoginī family/lineage → Kaula body/power-complex → totality of phenomena → Kubjikā's mantra-body → Abhinava's akula-pole. The translation-policy: retain 'Kula' in technical contexts, 'family/lineage' in the concrete Yoginī-classification, 'aggregate/body' only where the passage supports it.",
    concepts: ["akula", "yoginī", "krama"],
    resources: [
      { title: "The kula dossier", href: "/concepts/kula", type: "explainer" },
      { title: "Kaulajñānanirṇaya", href: "/texts/kaulajnananirnaya", type: "translation" },
    ],
    dossier: {
      systemicFunction:
        "Kula is the report's primary test-case for the lemma × tradition × period model — a single lemma whose senses branch by tradition, with the Kaula transition (lineage → body → totality) the clearest documented semantic shift in the ecosystem.",
      doctrinalCore: [
        "Early: Yoginī family/lineage (socio-mythic classification)",
        "Kaula: deliberate homonym-extension to body and totality",
        "Kubjikā: the mantra-body (kulātmaka deha)",
        "Abhinava: the manifest pole vs the transcendent akula",
      ],
      outputs: ["the semantic-shift trajectory", "the translation-policy", "the cross-tradition loci"],
    },
  },
  {
    id: "krama",
    type: "concept",
    title: "Krama",
    sanskrit: "क्रम",
    period: { start: 800, end: 1300, approximate: true },
    summary:
      "Krama spans ordinary 'sequence' to the Kālī-tradition's defining architecture: the perceptible order of worship reflects the imperceptible sequence of cognition (saṃvit-krama). Capitalize 'Krama' only when the lineage is demonstrable; otherwise render 'sequence/order'.",
    concepts: ["saṃvit", "kālī", "kula"],
    dossier: {
      systemicFunction:
        "Krama is the second semantic test-case: from ordinary succession → ritual order → the sequence of cognition → the named Krama/Mahānaya tradition. The critical transformation: ritual sequence becomes the enactment of the ever-present cognition-sequence.",
      doctrinalCore: [
        "Ordinary: sequence/order/procedure",
        "Ritual: the pūjā-krama",
        "Krama-school: saṃvit-krama (cognition as sequence)",
      ],
      outputs: ["the sequence-trajectory", "the 'no school-inference' rule", "the saṃvit dossier"],
    },
  },
  {
    id: "recognition",
    type: "concept",
    title: "Recognition",
    sanskrit: "प्रत्यभिज्ञा",
    period: { start: 900, end: 1025, approximate: true },
    summary:
      "The Pratyabhijñā thesis: liberation is recognition of an identity already obtaining. Recognition = transformation + reidentification + veridicality + stabilization. The report's A/B/C stratification governs it: A (reflexive presence) established, B (ownership) plausible, C (universalization) the live frontier.",
    concepts: ["vimarśa", "prakāśa", "svātantrya"],
    dossier: {
      systemicFunction:
        "Recognition is the semantic control thesis running sideways through the whole project — the philosophical core against which all the scriptural vocabularies are triangulated.",
      doctrinalCore: [
        "A nondual experience is evidence of a changed self-world organization, not proof of universal consciousness",
        "The three targets: process-internal, participatory, full Śaiva",
        "The universalization (C) is asserted, not demonstrated",
      ],
      outputs: ["the A/B/C dossier", "the recognition-frame", "the control-corpus design"],
    },
  },
  {
    id: "spanda",
    type: "concept",
    title: "Spanda",
    sanskrit: "स्पन्द",
    period: { start: 850, end: 1000, approximate: true },
    summary:
      "The dynamic pulse of the fundamental conscious reality — constitutive of manifestation and cognition, not a mechanically physical vibration. The pulse, the pulse's rest, and the pulse's outpouring are the cognition's own rhythm in the Krama's register.",
    concepts: ["śakti", "saṃvit", "svātantrya"],
    dossier: {
      systemicFunction:
        "Spanda supplies the dynamism-language the whole project draws on — the wheel-of-powers cosmology and the perceiver's unswerving nature.",
      doctrinalCore: [
        "Śiva as the source of the wheel of powers",
        "The pulse as constitutive, not mechanical",
        "The unobstructed nature → no obstruction",
      ],
      outputs: ["the spanda-dossier", "the pulse-register", "the wheel-of-powers map"],
    },
  },
  {
    id: "vimarśa",
    type: "concept",
    title: "Vimarśa",
    sanskrit: "विमर्श",
    period: { start: 900, end: 1025, approximate: true },
    summary:
      "Reflexive apprehension — the consciousness's capacity to apprehend itself and its content. Not mere 'reflection' (which falsely implies discursive thought). The report's A-thesis: manifestation without vimarśa would be crystal-like, hence inert.",
    concepts: ["prakāśa", "recognition", "svātantrya"],
    dossier: {
      systemicFunction:
        "Vimarśa is the reflexion-pole of the prakāśa/vimarśa pair — the engine of the Pratyabhijñā and the Krama's saṃvit-krama alike.",
      doctrinalCore: [
        "Reflexive apprehension, not discursive reflection",
        "The crystal-image: non-reflexive light is inert",
        "The 'I am this' as the reflexion's fulfillment",
      ],
      outputs: ["the vimarśa-dossier", "the A-thesis", "the engine-pair"],
    },
  },
  {
    id: "mālinī",
    type: "concept",
    title: "Mālinī",
    sanskrit: "मालिनी",
    period: { start: 950, end: 1100, approximate: true },
    summary:
      "The phonemic goddess of the Kubjikā — Rudraśakti, the mass of syllables, the origin of mantras, at once deity, alphabet, and mantra-ontology. She can simultaneously be Rudra's Śakti, the phonemes, a speaking goddess, and a knowledge-power.",
    concepts: ["mātṛkā", "khecarī", "kula"],
    dossier: {
      systemicFunction:
        "Mālinī is the Kubjikā's phonemic core — the demonstration that choosing one English equivalent for śakti fails when deity, alphabet and causal power overlap.",
      doctrinalCore: [
        "The self-born Rudraśakti from the phonemes",
        "The varṇa-rāśi: the mass of phonemes",
        "The mantra-deha: the phonemic body",
      ],
      outputs: ["the phonemic dossiers", "the Kubjikā-emergence", "the mātṛkā-map"],
    },
  },
];
