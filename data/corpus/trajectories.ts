// The term-trajectory dataset — the diachronic sense-history of each technical lemma.
// Seeded from the reference map (canonical_reference_map.md) + the dossiers
// (saivamap/dossiers/). This is the reference map's signature feature: a lemma
// does NOT have one meaning — it has a trajectory across traditions and periods.
//
// Each trajectory node: { period, tradition, sense, evidence[], translation_policy }.
// These are EVIDENCE-BACKED HYPOTHESES (the "Sense" level of authority), not
// settled facts. status reflects the source (reference map / dossier / verified).

export interface TrajectoryNode {
  period: string;
  tradition: string;
  sense: string;
  evidence?: string[];
  translation_policy?: string;
  status: "reference_map" | "dossier" | "verified";
}

export interface TermTrajectory {
  lemma: string;
  title: string;
  nodes: TrajectoryNode[];
  note?: string;
}

export const trajectories: TermTrajectory[] = [
  {
    lemma: "kula",
    title: "kula — the Kula / lineage / body / totality",
    nodes: [
      {
        period: "early Yoginī/Kaula",
        tradition: "Yoginī cult / Vidyāpīṭha",
        sense: "family / lineage of Yoginīs or Mothers",
        evidence: ["Sanderson's reconstruction from Vidyāpīṭha sources — the socio-mythic classification"],
        translation_policy: "translate 'family/lineage' when the concrete Yoginī-classification dominates",
        status: "reference_map",
      },
      {
        period: "developed Kaula",
        tradition: "Kaula",
        sense: "body; totality of power and phenomena",
        evidence: ["the Kaula homonym-extension: lineage → body → power → totality"],
        translation_policy: "retain 'Kula' or use 'body/totality' where the passage supports it",
        status: "reference_map",
      },
      {
        period: "Kubjikā (Western)",
        tradition: "Kubjikā",
        sense: "the mantra-body (mantradeha) / the structured Kula",
        evidence: ["KMT 17.80–82: the resulting body is kulātmaka"],
        translation_policy: "'aggregate/body/complex' only where the passage supports it",
        status: "dossier",
      },
      {
        period: "Abhinavagupta / Trika",
        tradition: "Trika",
        sense: "the manifest pole vs the transcendent akula",
        evidence: ["TĀ 3.143: the supreme anuttara-abode is akula; its visarga is the kaulikī śakti"],
        translation_policy: "retain 'Kula' when the whole technical system is activated; never auto-translate as 'family'",
        status: "verified",
      },
    ],
    note: "The clearest documented semantic shift in the ecosystem — the reference map's signature example.",
  },
  {
    lemma: "krama",
    title: "krama — sequence / ritual order / the Krama school",
    nodes: [
      {
        period: "general Sanskrit",
        tradition: "—",
        sense: "sequence / succession / order",
        evidence: ["the ordinary sense"],
        translation_policy: "translate 'sequence/succession'; do not infer the Krama school from the noun",
        status: "reference_map",
      },
      {
        period: "Krama / Kālīkula",
        tradition: "Krama",
        sense: "ordered unfolding of cognition reflected in ordered worship (saṃvit-krama)",
        evidence: ["Sanderson: the pūjā-krama reflects the saṃvit-krama"],
        translation_policy: "translate 'sequence' but flag the technical resonance; capitalise only where the school is demonstrable",
        status: "reference_map",
      },
      {
        period: "Abhinavagupta / Trika",
        tradition: "Trika",
        sense: "sequence, progressive manifestation, or graduated procedure",
        evidence: ["TĀ 1.5; numerous later chapters"],
        translation_policy: "often generic; sometimes carrying inherited Krama resonance — read the context",
        status: "reference_map",
      },
    ],
  },
  {
    lemma: "khecarī",
    title: "khecarī — sky-goer / goddess / mantra-body / mudrā",
    nodes: [
      {
        period: "early",
        tradition: "Krama / Kaula",
        sense: "a sky-going goddess / yoginī",
        evidence: [],
        translation_policy: "'sky-goer' / retain khecarī",
        status: "dossier",
      },
      {
        period: "Kubjikā (Western)",
        tradition: "Kubjikā",
        sense: "the mantra-body / a complex mantric goddess-body (Mālinī)",
        evidence: ["KMT 17.77–82: Khecarī as a sixteen-part goddess / mantradeha"],
        translation_policy: "retain khecarī; not reducible to the later haṭhayogic tongue-gesture",
        status: "dossier",
      },
      {
        period: "Abhinava's ritual synthesis",
        tradition: "Trika",
        sense: "mudrā, internal condition, movement through space, creation/retraction, possession",
        evidence: ["TĀ 32.31–65"],
        translation_policy: "read per context — an excellent polysemy test case",
        status: "reference_map",
      },
    ],
  },
  {
    lemma: "śakti",
    title: "śakti — power / the Goddess / mantric power",
    nodes: [
      {
        period: "Spanda",
        tradition: "Spanda",
        sense: "power/dynamism constitutive of manifestation and cognition",
        evidence: ["SPK 1, 18–19"],
        translation_policy: "not merely 'energy'",
        status: "reference_map",
      },
      {
        period: "Kubjikā",
        tradition: "Kubjikā",
        sense: "goddess / mantric power, with strong phonemic and triadic articulation",
        evidence: ["KMT 1.71–81; 2.1; 4.110"],
        translation_policy: "deity, language and causal power overlap — do not flatten into one gloss",
        status: "dossier",
      },
      {
        period: "Abhinava / Trika",
        tradition: "Trika",
        sense: "freedom/power of consciousness; specific powers differentiated from and reintegrated into supreme awareness",
        evidence: ["TĀ 1.5; 3.143–44; 33.20–29"],
        translation_policy: "translate by context; a single English 'energy' seriously impoverishes it",
        status: "reference_map",
      },
    ],
  },
  {
    lemma: "vimarśa",
    title: "vimarśa — reflection / reflexive awareness",
    nodes: [
      {
        period: "general Sanskrit",
        tradition: "—",
        sense: "consideration / reflection",
        evidence: ["the ordinary sense"],
        translation_policy: "translate normally",
        status: "reference_map",
      },
      {
        period: "Pratyabhijñā / Abhinava",
        tradition: "Pratyabhijñā",
        sense: "reflexive apprehension, self-awareness, the capacity of consciousness to apprehend itself",
        evidence: ["ĪPK 1.5.11–14; TĀ 3 and 33"],
        translation_policy: "'reflexive awareness' — 'reflection' alone can falsely imply discursive thought",
        status: "reference_map",
      },
    ],
  },
  {
    lemma: "visarga",
    title: "visarga — emission / release / the kaulikī śakti",
    nodes: [
      {
        period: "general",
        tradition: "—",
        sense: "emission / sending forth / the phoneme ḥ",
        evidence: ["the base semantic field"],
        translation_policy: "'emission' is the safest literal anchor; tag the register separately",
        status: "reference_map",
      },
      {
        period: "Abhinava / Trika",
        tradition: "Trika / Kaula",
        sense: "the supreme's kaulikī śakti; cosmogenic manifestation",
        evidence: ["TĀ 3.141–144"],
        translation_policy: "retain visarga in the technical context; tag grammatical/phonemic/cosmogenic/erotic registers separately",
        status: "reference_map",
      },
    ],
    note: "A lemma-level translation consistency is NOT desirable — semantic consistency is the goal, not lexical uniformity.",
  },
];

export function getTrajectory(lemma: string): TermTrajectory | undefined {
  const key = lemma.toLowerCase().replace(/[īūṛḷṅñṭḍṇśṣḥāēō]/g, (c) => c);
  return trajectories.find((t) => t.lemma.toLowerCase().replace(/[īūṛḷṅñṭḍṇśṣḥāēō]/g, (c) => c) === key);
}
