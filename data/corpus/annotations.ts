// First real scholarly-graph annotation instances — the nirānanda case (Milestone A2).
//
// The concrete "one reviewed instance beats a schema with no data" move. This wires
// the six-primitives model to an actual scholarly question: what does nirānande mean
// at Kramasadbhāva 1.8?
//
// Two RIVAL sense assignments (annotations on the same occurrence — disagreement is
// native, nothing overwritten). One is machine-proposed (from the 1.8 run's R1/R2),
// one is editor-proposed (the technical Krama reading). Both carry evidence. Review
// is NOT yet done — that is the next step (Milestone C / a real specialist).
import type { Annotation } from "./graph";

// The occurrence itself: nirānande at 1.8.
export const nirAnandeOccurrence: Annotation = {
  id: "pt:annotation:krs:1.8:niranande:occurrence",
  target: "pt:passage:kramasadbhava:1.8",
  type: "term_occurrence",
  payload: { lemma: "nirānanda", surface: "nirānande", chapter: 1, verse: 8 },
  origin: "machine",
  status: "machine_proposed",
  certainty: "certain",
  evidence: [
    { resource: "pt:passage:kramasadbhava:1.8", role: "identifies" },
  ],
  review_events: [],
  created_at: "2026-08-10",
  created_by: "patala-pipeline",
};

// RIVAL A — the literal privative (from the machine run's R1/R2; CONSTRAINED in R2).
export const nirAnandePrivative: Annotation = {
  id: "pt:annotation:krs:1.8:nirananda:privative",
  target: nirAnandeOccurrence.id,   // annotation-on-annotation
  type: "sense_assignment",
  payload: { sense_id: "nirānanda.privative", claim: "O bliss-less one (privative nir-+ānanda)" },
  origin: "machine",
  status: "machine_proposed",
  certainty: "possible",
  evidence: [
    { resource: "pt:passage:kramasadbhava:1.8", role: "defines" },
    { resource: "pt:passage:kramasadbhava:1.6", locator: "nirāmayaḥ (same privative nir-)", role: "parallel" },
    { resource: "pt:annotation:krs:1.8:nirananda:occurrence", role: "supports" },
  ],
  review_events: [],
  created_at: "2026-08-10",
  created_by: "patala-pipeline",
};

// RIVAL B — the technical Krama reading (the external-evidence correction).
export const nirAnandeTechnical: Annotation = {
  id: "pt:annotation:krs:1.8:nirananda:technical",
  target: nirAnandeOccurrence.id,   // same occurrence — disagreement is native
  type: "sense_assignment",
  payload: {
    proposed_sense_id: "nirānanda.krama.technical",
    claim: "a technical state beyond the bliss/absence pair — 'the bliss of stillness' (cf. nirācārānanda)",
  },
  origin: "editor",
  status: "human_proposed",
  certainty: "probable",
  evidence: [
    { resource: "pt:res:mahanaya-kramasadbhava", locator: "1.8", role: "parallel", note: "Mahānaya online edition renders nirānande as 'the Bliss of Stillness'" },
    { resource: "pt:res:kubjika-niracarananda", locator: "nirācārānanda", role: "defines", note: "Dyczkowski-related Kubjikā material: nirānanda as technical, connected with nirācārānanda 'bliss of stillness'" },
    { resource: "pt:res:dyczkowski-ed", role: "supports" },
  ],
  review_events: [],
  created_at: "2026-08-10",
  created_by: "editor",   // your main model, not machine
};

// The research question this unresolved disagreement raises.
export const nirAnandeResearchQuestion: Annotation = {
  id: "pt:annotation:krs:1.8:nirananda:research-question",
  target: nirAnandeOccurrence.id,
  type: "research_question",
  payload: {
    question: "Does the pairing with paramānande (1.8) force the literal privative 'bliss-less', or does the technical 'bliss of stillness' sense better fit the stuti's emission hierarchy? Requires a Krama specialist verdict.",
  },
  origin: "editor",
  status: "human_proposed",
  certainty: "uncertain",
  evidence: [
    { resource: "pt:annotation:krs:1.8:nirananda:privative", role: "parallel" },
    { resource: "pt:annotation:krs:1.8:nirananda:technical", role: "parallel" },
  ],
  review_events: [],
  created_at: "2026-08-10",
  created_by: "editor",
};

export const nirAnandeInstances = [
  nirAnandeOccurrence,
  nirAnandePrivative,
  nirAnandeTechnical,
  nirAnandeResearchQuestion,
];
