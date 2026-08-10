// The term-trajectory dataset — the diachronic sense-history of each technical lemma.
//
// IMPORTANT (per the term-trajectory red-team review): a trajectory node is NOT
// loose "term metadata". It is a scholarly ASSERTION that a particular sense is
// operative within a particular historical/traditional scope. Therefore:
//
//   - every node has a stable id (targetable, reviewable — invariant 3)
//   - every node references an accepted `sense_id` (from data/terms.json) or a
//     `proposed_sense_id` (from data/term_proposals.jsonl) — it does NOT create a
//     parallel sense ontology
//   - every node carries addressable `evidence_links` (passage ids / resource ids),
//     not just display labels
//   - origin (where the claim came from) and status (epistemic maturity) and
//     certainty are SEPARATE dimensions (status ≠ certainty)
//   - period/tradition are structured where possible (ids), labels kept for display
//
// This is curated interpretation (the "Sense"/"Synthesis" authority level), seeded
// from the reference map + dossiers. It is NOT mechanically derived from corpus
// occurrences.

export interface TrajectoryEvidenceLink {
  target_id: string;        // a passage id (tantra:text:...) or resource id
  type: "passage" | "resource" | "work";
  role: "supports" | "defines" | "illustrates" | "contradicts" | "historical_argument";
  locator?: string;         // e.g. "17.80–82" or "p. 143" for external resources
}

export interface TrajectoryNode {
  id: string;                                  // stable, opaque semantic id, e.g. "kula.kubjika.mantra-body"
  lemma: string;                               // canonical lemma
  period_label: string;                        // display, e.g. "Abhinavagupta / Trika"
  date_range?: { not_before?: number; not_after?: number; certainty?: string } | null;
  tradition_ids: string[];                     // canonical tradition ids (resolve against data/atlas)
  tradition_label: string;                     // display
  sense_id?: string;                           // an ACCEPTED sense (must exist in terms.json)
  proposed_sense_id?: string;                  // a PROPOSED sense (must exist in term_proposals.jsonl)
  claim: string;                               // the historical-scope assertion
  evidence_links: TrajectoryEvidenceLink[];
  origin: "reference_map" | "dossier" | "external_scholarship" | "manual";
  status: "proposed" | "reviewed" | "accepted" | "disputed";
  certainty?: "secure" | "probable" | "possible" | "uncertain";
  translation_policy?: {                        // a SEPARATE house-recommendation assertion
    guidance: string;
    policy_version?: string;
  };
}

export interface TermTrajectory {
  lemma: string;
  title: string;
  nodes: TrajectoryNode[];
  note?: string;
}

// Canonical tradition ids (resolve against data/atlas/traditions.ts)
const TRAD = {
  TRIKA: "trika",
  KRAMA: "krama",
  KUBJIKA: "kubjika",
  KAULA: "kaula",
  SPANDA: "spanda",
  PRATYABHIJNA: "pratyabhijna",
} as const;

export const trajectories: TermTrajectory[] = [
  {
    lemma: "kula",
    title: "kula — the Kula / lineage / body / totality",
    note: "The clearest documented semantic shift in the ecosystem — the reference map's signature example.",
    nodes: [
      {
        id: "kula.yogini.lineage",
        lemma: "kula",
        period_label: "early Yoginī/Kaula",
        date_range: { not_before: 750, not_after: 950, certainty: "uncertain" },
        tradition_ids: [TRAD.KAULA],
        tradition_label: "Yoginī cult / Vidyāpīṭha",
        sense_id: "kula.lineage",
        claim: "within early Yoginī/Vidyāpīṭha material, kula carries socio-mythic lineage classification",
        evidence_links: [
          { target_id: "resource:sanderson-vidyapitha", type: "resource",
            role: "historical_argument", locator: "the Vidyāpīṭha reconstruction" },
        ],
        origin: "reference_map",
        status: "accepted",
        certainty: "secure",
        translation_policy: { guidance: "translate 'family/lineage' when the concrete Yoginī-classification dominates" },
      },
      {
        id: "kula.kaula.body-power",
        lemma: "kula",
        period_label: "developed Kaula",
        tradition_ids: [TRAD.KAULA],
        tradition_label: "Kaula",
        sense_id: "kula.body.power",
        claim: "the Kaula homonym-extension: kula moves from lineage toward body, power, totality",
        evidence_links: [
          { target_id: "resource:sanderson-kaula", type: "resource",
            role: "historical_argument", locator: "the Kaula homonym-extension" },
        ],
        origin: "reference_map",
        status: "accepted",
        certainty: "probable",
        translation_policy: { guidance: "retain 'Kula' or use 'body/totality' where the passage supports it" },
      },
      {
        id: "kula.kubjika.mantra-body",
        lemma: "kula",
        period_label: "Kubjikā (Western)",
        tradition_ids: [TRAD.KUBJIKA],
        tradition_label: "Kubjikā",
        sense_id: "kula.body.power",
        claim: "in the Kubjikā corpus the body/power sense is specifically articulated through the mantra-body (mantradeha) — the structured Kula",
        evidence_links: [
          { target_id: "tantra:text:kubjikamata:17.80", type: "passage",
            role: "supports", locator: "17.80–82: the resulting body is kulātmaka" },
        ],
        origin: "dossier",
        status: "reviewed",
        certainty: "probable",
        translation_policy: { guidance: "'aggregate/body/complex' only where the passage supports it" },
      },
      {
        id: "kula.abhinava.akula-pole",
        lemma: "kula",
        period_label: "Abhinavagupta / Trika",
        date_range: { not_before: 975, not_after: 1025, certainty: "probable" },
        tradition_ids: [TRAD.TRIKA],
        tradition_label: "Trika",
        sense_id: "kula.body.power",
        claim: "in the Trika synthesis the kula-pole is set against the transcendent akula",
        evidence_links: [
          { target_id: "tantra:text:tantraloka:3.143", type: "passage",
            role: "supports", locator: "the anuttara-abode is akula; its visarga is the kaulikī śakti" },
        ],
        origin: "reference_map",
        status: "accepted",
        certainty: "secure",
        translation_policy: { guidance: "retain 'Kula' when the whole technical system is activated; never auto-translate as 'family'" },
      },
    ],
  },
  {
    lemma: "krama",
    title: "krama — sequence / ritual order / the Krama school",
    nodes: [
      {
        id: "krama.general.sequence",
        lemma: "krama",
        period_label: "general Sanskrit",
        tradition_ids: [],
        tradition_label: "—",
        sense_id: "krama.general.sequence",
        claim: "the ordinary sense of progression/order",
        evidence_links: [],
        origin: "manual",
        status: "accepted",
        certainty: "secure",
        translation_policy: { guidance: "translate 'sequence/succession'; do not infer the Krama school from the noun" },
      },
      {
        id: "krama.kalikula.cognition-sequence",
        lemma: "krama",
        period_label: "Krama / Kālīkula",
        tradition_ids: [TRAD.KRAMA],
        tradition_label: "Krama",
        sense_id: "krama.school.technical",
        claim: "the pūjā-krama (ritual order) reflects the saṃvit-krama (cognition-sequence) — sequence becomes the tradition's architecture",
        evidence_links: [
          { target_id: "resource:sanderson-krama", type: "resource",
            role: "historical_argument", locator: "the pūjā-krama / saṃvit-krama relation" },
        ],
        origin: "reference_map",
        status: "accepted",
        certainty: "probable",
        translation_policy: { guidance: "translate 'sequence' but flag the technical resonance; capitalise only where the school is demonstrable" },
      },
    ],
  },
  {
    lemma: "khecarī",
    title: "khecarī — sky-goer / goddess / mantra-body / mudrā",
    nodes: [
      {
        id: "khecari.kubjika.mantra-body",
        lemma: "khecarī",
        period_label: "Kubjikā (Western)",
        tradition_ids: [TRAD.KUBJIKA],
        tradition_label: "Kubjikā",
        sense_id: "khecari.mantra.body",
        claim: "Khecarī as a complex mantric goddess-body (Mālinī) — not reducible to the later haṭhayogic tongue-gesture",
        evidence_links: [
          { target_id: "tantra:text:kubjikamata:17.77", type: "passage",
            role: "supports", locator: "17.77–82: the sixteen-part goddess / mantradeha" },
        ],
        origin: "dossier",
        status: "reviewed",
        certainty: "probable",
      },
      {
        id: "khecari.trika.mudra-state",
        lemma: "khecarī",
        period_label: "Abhinava's ritual synthesis",
        tradition_ids: [TRAD.TRIKA],
        tradition_label: "Trika",
        proposed_sense_id: "khecari.trika.mudra-internal",
        claim: "in the Trika synthesis khecarī names mudrā, internal condition, movement through space, creation/retraction, possession — a polysemy within one chapter",
        evidence_links: [
          { target_id: "resource:tantraloka-vol", type: "resource",
            role: "supports", locator: "TĀ 32.31–65" },
        ],
        origin: "reference_map",
        status: "proposed",
        certainty: "possible",
        translation_policy: { guidance: "read per context — an excellent polysemy test case" },
      },
    ],
  },
  {
    lemma: "śakti",
    title: "śakti — power / the Goddess / mantric power",
    nodes: [
      {
        id: "sakti.spanda.dynamism",
        lemma: "śakti",
        period_label: "Spanda",
        tradition_ids: [TRAD.SPANDA],
        tradition_label: "Spanda",
        sense_id: "sakti.causal",
        claim: "power/dynamism constitutive of manifestation and cognition",
        evidence_links: [
          { target_id: "resource:spandakarika", type: "resource", role: "supports", locator: "SPK 1, 18–19" },
        ],
        origin: "reference_map",
        status: "accepted",
        certainty: "probable",
        translation_policy: { guidance: "not merely 'energy'" },
      },
      {
        id: "sakti.kubjika.mantric",
        lemma: "śakti",
        period_label: "Kubjikā",
        tradition_ids: [TRAD.KUBJIKA],
        tradition_label: "Kubjikā",
        sense_id: "sakti.mantric",
        claim: "goddess / mantric power with strong phonemic and triadic articulation",
        evidence_links: [
          { target_id: "resource:kubjikamata", type: "resource", role: "supports", locator: "KMT 1.71–81; 2.1; 4.110" },
        ],
        origin: "dossier",
        status: "reviewed",
        certainty: "probable",
      },
    ],
  },
  {
    lemma: "vimarśa",
    title: "vimarśa — reflection / reflexive awareness",
    nodes: [
      {
        id: "vimarsa.general.reflection",
        lemma: "vimarśa",
        period_label: "general Sanskrit",
        tradition_ids: [],
        tradition_label: "—",
        sense_id: "vimarsa.general",
        claim: "the ordinary sense of consideration/reflection",
        evidence_links: [],
        origin: "manual",
        status: "accepted",
        certainty: "secure",
      },
      {
        id: "vimarsa.pratyabhijna.reflexive",
        lemma: "vimarśa",
        period_label: "Pratyabhijñā / Abhinava",
        tradition_ids: [TRAD.PRATYABHIJNA, TRAD.TRIKA],
        tradition_label: "Pratyabhijñā",
        sense_id: "vimarsa.pratyabhijna.technical",
        claim: "reflexive apprehension / self-awareness — the capacity of consciousness to apprehend itself",
        evidence_links: [
          { target_id: "resource:ipk", type: "resource", role: "supports", locator: "ĪPK 1.5.11–14" },
          { target_id: "resource:tantraloka", type: "resource", role: "supports", locator: "TĀ 3 and 33" },
        ],
        origin: "reference_map",
        status: "accepted",
        certainty: "secure",
        translation_policy: { guidance: "'reflexive awareness' — 'reflection' alone can falsely imply discursive thought" },
      },
    ],
  },
  {
    lemma: "visarga",
    title: "visarga — emission / release / the kaulikī śakti",
    note: "A lemma-level translation consistency is NOT desirable — semantic consistency is the goal, not lexical uniformity.",
    nodes: [
      {
        id: "visarga.general.emission",
        lemma: "visarga",
        period_label: "general",
        tradition_ids: [],
        tradition_label: "—",
        sense_id: "visarga.general",
        claim: "emission / sending forth / the phoneme ḥ",
        evidence_links: [],
        origin: "manual",
        status: "accepted",
        certainty: "secure",
      },
      {
        id: "visarga.abhinava.kauliki-sakti",
        lemma: "visarga",
        period_label: "Abhinava / Trika",
        tradition_ids: [TRAD.TRIKA, TRAD.KAULA],
        tradition_label: "Trika / Kaula",
        sense_id: "visarga.kaula",
        claim: "the supreme's kaulikī śakti; cosmogenic manifestation",
        evidence_links: [
          { target_id: "resource:tantraloka", type: "resource", role: "supports", locator: "TĀ 3.141–144" },
        ],
        origin: "reference_map",
        status: "accepted",
        certainty: "probable",
        translation_policy: { guidance: "retain visarga in the technical context; tag grammatical/phonemic/cosmogenic registers separately" },
      },
    ],
  },
];

// ── the shared canonical lemma resolver ──────────────────────────────────────
// Strip diacritics + case so terms / history / occurrences / proposals / MCP all
// resolve the same way. This is the single place lemma identity is normalised.
const DIACRITICS: Record<string, string> = {
  ā: "a", ī: "i", ū: "u", ṛ: "r", ṝ: "r", ḷ: "l", ṅ: "n", ñ: "n",
  ṭ: "t", ḍ: "d", ṇ: "n", ś: "s", ṣ: "s", ḥ: "h", ē: "e", ō: "o",
  ǵ: "g", é: "e",
};

export function resolveLemma(input: string): string {
  return (input || "").toLowerCase()
    .split("")
    .map((c) => DIACRITICS[c] ?? c)
    .join("");
}

export function getTrajectory(lemma: string): TermTrajectory | undefined {
  const key = resolveLemma(lemma);
  return trajectories.find((t) => resolveLemma(t.lemma) === key);
}
