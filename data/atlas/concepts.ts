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
  {
    id: "saṃvit",
    type: "concept",
    title: "Saṃvit",
    sanskrit: "सम्वित्",
    period: { start: 800, end: 1200, approximate: true },
    summary:
      "Conscious awareness considered in dynamic sequence — the Krama's saṃvit-krama. The perceptible order of worship reflects the imperceptible sequence of cognition. The engine of the Kālīs-as-moments.",
    concepts: ["krama", "spanda", "vimarśa"],
    dossier: {
      systemicFunction: "The Krama's engine — cognition as sequence, not a static witness.",
      doctrinalCore: [
        "The cognition's outflow (saṃvit-prasara) in the Mahānayaprakāśa",
        "The one-vs-many cognition question (MNP:598)",
        "The awareness-yoginīs (Mahārthamañjarī m.11)",
      ],
      outputs: ["the saṃvit dossier", "the Krama's engine-map"],
    },
  },
  {
    id: "akula",
    type: "concept",
    title: "Akula",
    sanskrit: "अकुल",
    period: { start: 900, end: 1100, approximate: true },
    summary:
      "The transcendent pole, explicitly identified with anuttara in Abhinava's synthesis. Best understood relationally with kula — the manifest pole is kula, its ground is akula.",
    concepts: ["kula", "anuttara"],
    dossier: {
      systemicFunction: "The akula/kula polarity — the compressed cosmology of the Kubjikāmata maṅgala, made metaphysical by Abhinava.",
      doctrinalCore: [
        "KMT 1.1: the five gone into akula-and-kula",
        "TĀ 3.143: the supreme abode is akula; its visarga is the kaulikī śakti",
      ],
      outputs: ["the akula dossier", "the polarity-map"],
    },
  },
  {
    id: "parāmarśa",
    type: "concept",
    title: "Parāmarśa",
    sanskrit: "परामर्श",
    period: { start: 900, end: 1025, approximate: true },
    summary:
      "Apprehension/self-apprehension — the act by which experience is gathered into unified awareness. Related to but not always interchangeable with vimarśa.",
    concepts: ["vimarśa", "recognition"],
    dossier: {
      systemicFunction: "The gathering-act of the Pratyabhijñā — distinct from vimarśa's self-grasping.",
      doctrinalCore: ["TĀ 33.20–29: the gathering into unified awareness"],
      outputs: ["the parāmarśa dossier"],
    },
  },
  {
    id: "prakāśa",
    type: "concept",
    title: "Prakāśa",
    sanskrit: "प्रकाश",
    period: { start: 900, end: 1025, approximate: true },
    summary:
      "Manifest luminosity — awareness as that in virtue of which things appear. 'Light' is suggestive but misleads if treated as physical luminosity.",
    concepts: ["vimarśa", "recognition"],
    dossier: {
      systemicFunction: "The luminosity-pole of the prakāśa/vimarśa pair — the A-thesis's engine.",
      doctrinalCore: [
        "Mahārthamañjarī g.2: the unmoving upsurge suffused with reflexion",
        "The heart as the unsurpassed-nectar-kula (TĀ 1.1)",
      ],
      outputs: ["the prakāśa dossier", "the engine-pair"],
    },
  },
  {
    id: "visarga",
    type: "concept",
    title: "Visarga",
    sanskrit: "विसर्ग",
    period: { start: 900, end: 1025, approximate: true },
    summary:
      "Emission, release, manifestation — the power by which the supreme projects itself. Carries phonemic, cosmological, and in some contexts erotic/ritual resonances.",
    concepts: ["kula", "prakāśa"],
    dossier: {
      systemicFunction: "The emission-pole of the cosmology — the world's seed (TĀ: visargaprasara).",
      doctrinalCore: [
        "TĀ 1.1: the heart made of the emission of the being",
        "The visarga's outflow as the world's variegation (M00092:76)",
      ],
      outputs: ["the visarga dossier", "the emission-map"],
    },
  },
  {
    id: "anuttara",
    type: "concept",
    title: "Anuttara",
    sanskrit: "अनुत्तर",
    period: { start: 975, end: 1025, approximate: true },
    summary:
      "The Unsurpassed — the concentrated Parā/Ekavīrā and the supreme state. Not merely the adjective 'highest' but a heavily loaded technical designation.",
    concepts: ["kula", "akula"],
    dossier: {
      systemicFunction: "The Trika's ground-term — the heart as the unsurpassed-nectar-kula (TĀ 1.1).",
      doctrinalCore: [
        "TĀ 1.5: the Unsurpassed as the ground of the three powers",
        "The anuttara/akula identification (TĀ 3.143)",
      ],
      outputs: ["the anuttara dossier", "the ground-map"],
    },
  },
  {
    id: "mātṛkā",
    type: "concept",
    title: "Mātṛkā",
    sanskrit: "मातृका",
    period: { start: 850, end: 1100, approximate: true },
    summary:
      "The Mother/phonemic matrix — the power embodied in the letters. Śakti is identified with Mātṛkā, Mātṛkā as Śiva-natured. Never 'alphabet' — the goddess-load is essential.",
    concepts: ["mālinī", "khecarī"],
    dossier: {
      systemicFunction: "The phonemic matrix — the alphabet as goddess.",
      doctrinalCore: [
        "ŚS 1.4: the ground of knowledge is Mātṛkā",
        "ŚS 2.7: the Mātṛkā-wheel's awakening",
      ],
      outputs: ["the mātṛkā dossier"],
    },
  },
  {
    id: "svātantrya",
    type: "concept",
    title: "Svātantrya",
    sanskrit: "स्वातन्त्र्य",
    period: { start: 900, end: 1025, approximate: true },
    summary:
      "The inherent freedom of conscious agency — ontological efficacy as well as volition. 'Free will' is too narrow.",
    concepts: ["spanda", "recognition", "śakti"],
    dossier: {
      systemicFunction: "The first power — the freedom that produces the world as mere appearance (TĀ 1.5).",
      doctrinalCore: [
        "TĀ 1.5: the power of freedom as the Lord's majesty",
        "The world as the essence of mere appearance by its freedom (M00092:59)",
      ],
      outputs: ["the svātantrya dossier"],
    },
  },
  {
    id: "āveśa",
    type: "concept",
    title: "Āveśa / Samāveśa",
    sanskrit: "आवेश",
    period: { start: 900, end: 1025, approximate: true },
    summary:
      "Entry / possession — the state of being entered by the divine. The practice's goal in the Trika's uccāra-complex.",
    concepts: ["spanda", "recognition"],
    dossier: {
      systemicFunction: "The possession-state — the entry into the supreme Lord.",
      doctrinalCore: [
        "The surge of the state of entry (TĀ M00092:32)",
        "The entry-into-Śiva-Śakti (TĀ M00092:172)",
      ],
      outputs: ["the āveśa dossier"],
    },
  },
  {
    id: "uccāra",
    type: "concept",
    title: "Uccāra",
    sanskrit: "उच्चार",
    period: { start: 900, end: 1025, approximate: true },
    summary:
      "The mantra's articulation/emission — the inner sound-rise, distinguished from the external rites (the kuṇḍa, the maṇḍala).",
    concepts: ["mantra", "āveśa"],
    dossier: {
      systemicFunction: "The inner articulation of the mantra — the Trika's uccāra-system.",
      doctrinalCore: ["The uccāra-and-the-rest as internal; the external rites (TĀ M00092:2611)"],
      outputs: ["the uccāra dossier"],
    },
  },
  {
    id: "vyāpti",
    type: "concept",
    title: "Vyāpti",
    sanskrit: "व्याप्ति",
    period: { start: 900, end: 1300, approximate: true },
    summary:
      "Pervasion — ontological in the Trika (the Lord's all-ness), logical in the Nyāya (the inference's pervasion-relation).",
    concepts: ["prakāśa"],
    dossier: {
      systemicFunction: "The cross-tradition fork: the Trika's ontological pervasion vs the Nyāya's logical relation.",
      doctrinalCore: ["the Lord's all-pervading nature", "the Tarkasaṃgraha's vyāpti (Hop 10)"],
      outputs: ["the vyāpti dossier", "the cross-tradition fork"],
    },
  },
  {
    id: "śūnya",
    type: "concept",
    title: "Śūnya",
    sanskrit: "शून्य",
    period: { start: 900, end: 1200, approximate: true },
    summary:
      "The void as the apophatic terminus — the pure consciousness-form, NOT mere absence. The Mahānayaprakāśa's śūnyāśūnya: 'the void-and-non-void.'",
    concepts: ["prakāśa", "kula"],
    dossier: {
      systemicFunction: "The apophatic terminus — the void that is the pure consciousness-form.",
      doctrinalCore: [
        "MNP: the void-and-non-void, the pure form not the absence",
        "JKK 3/13: knowing the void, the Stainless",
      ],
      outputs: ["the śūnya dossier", "the apophatic-map"],
    },
  },
  {
    id: "saṃhāra",
    type: "concept",
    title: "Saṃhāra / Sṛṣṭi",
    sanskrit: "संहार",
    period: { start: 850, end: 1100, approximate: true },
    summary:
      "Retraction / creation — the cosmic pair by whose opening and closing the universe is destroyed and created. The Lord's blink (SPK 1.1).",
    concepts: ["spanda", "prakāśa"],
    dossier: {
      systemicFunction: "The cosmic operations — creation, maintenance, withdrawal as the powers' rhythm.",
      doctrinalCore: [
        "SPK 1.1: by whose opening and closing the universe is destroyed and created",
        "SPK 1.6: the inner wheel drives the triad",
      ],
      outputs: ["the saṃhāra/sṛṣṭi dossier", "the cosmic-pair map"],
    },
  },
  {
    id: "cakra",
    type: "concept",
    title: "Cakra",
    sanskrit: "चक्र",
    period: { start: 850, end: 1200, approximate: true },
    summary:
      "The wheel — the power-aggregate in the Trika/Spanda (the Wheel of Energies), the ritual circle in the Kaula (the Bhairavī-cakra).",
    concepts: ["śakti", "kula"],
    dossier: {
      systemicFunction: "The wheel of powers vs the ritual circle — the register-fork.",
      doctrinalCore: [
        "SPK 1.1: the Wheel of Energies",
        "ŚS 2.7: the Mātṛkā-wheel",
        "KRH: the Bhairavī-cakra's equality",
      ],
      outputs: ["the cakra dossier", "the register-fork"],
    },
  },
  {
    id: "mantra",
    type: "concept",
    title: "Mantra",
    sanskrit: "मन्त्र",
    period: { start: 850, end: 1200, approximate: true },
    summary:
      "The corpus's most frequent technical term (58,842 occurrences — the Dyczkowski-selection caveat applies). The mantra as phonemic power, divine utterance, and the dīkṣā's vehicle.",
    concepts: ["mālinī", "uccāra", "kula"],
    dossier: {
      systemicFunction: "The mantra's phonemic origin and ritual vehicle.",
      doctrinalCore: [
        "KMT 1.75: the seed-letters born of the limbs",
        "KRH: the book-mantra's sin (the secrecy-discipline)",
      ],
      outputs: ["the mantra dossier", "the phonemic-map"],
    },
  },
  {
    id: "khecarī",
    type: "concept",
    title: "Khecarī",
    sanskrit: "खेचरी",
    period: { start: 800, end: 1300, approximate: true },
    summary:
      "The 'sky-going' power — in the Krama, the goddess/power of the sky and the siddhi-fruit of moving through it (khecaratva); not the later haṭhayogic tongue-gesture. One of the four goers (khecarī, bhūcarī, dikcarī, gocarī) — the senses' powers as the Goddess's modes.",
    concepts: ["śakti", "spanda", "saṃvit"],
    dossier: {
      systemicFunction:
        "Khecarī is the polysemy-test-case: the sky-goer goddess, the khecaratva-fruit (the siddha's sky-motion), and the phoneme-name (in the mantra-compositions) — the register must be tagged, never flattened to the haṭha-gesture.",
      doctrinalCore: [
        "The sky-goer as the power (never the tongue-gesture)",
        "The khecaratva-fruit: the siddha's sky-motion",
        "The four goers: khecarī, bhūcarī, dikcarī, gocarī",
        "The phoneme-name in the bīja-compositions",
      ],
      outputs: ["the khecarī dossier", "the four-goers map", "the khecaratva cross-text"],
    },
  },
];
