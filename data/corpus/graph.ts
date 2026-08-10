// The Pāṭala Scholarly Graph — the canonical object/annotation model.
// See docs/SCHOLARLY_GRAPH.md. Everything Pāṭala serves is an OBJECT or an
// ANNOTATION/ASSERTION over objects. This is the durable model that must survive
// years, so it is deliberately small and conservative.
//
// Objects (identity, no mutable interpretation):
//   Work · Witness · DigitalRepresentation · CanonicalPassage · SourceSpan ·
//   Person · Organization · Term · Sense · Resource
// Annotations (the claims): translation, lexical_decision, grammar, ambiguity,
//   parallel, textual_variant, term_occurrence, sense_assignment, dating,
//   tradition, authorship, manuscript_identification, commentary,
//   term_history_assertion, bibliographic_claim.
// The three dimensions (never conflated): origin / status / certainty.

import type { Certainty, Origin, Evidence, ReviewEvent } from "./primitives";

export type GraphObjectType =
  | "work" | "witness" | "digital_representation" | "canonical_passage"
  | "source_span" | "person" | "organization" | "term" | "sense" | "resource";

export interface GraphObject {
  id: string;          // pt:work:kramasadbhava, pt:person:abhinavagupta, ...
  type: GraphObjectType;
  // durable identity facts only; contested claims live in annotations
  titles?: string[];   // canonical title + aliases
  external_ids?: { system: string; id: string }[];  // aliases, not replacements
  created_at?: string;
  [k: string]: unknown;
}

export type AnnotationType =
  | "translation" | "lexical_decision" | "grammar" | "ambiguity" | "parallel"
  | "textual_variant" | "term_occurrence" | "sense_assignment" | "dating"
  | "tradition" | "authorship" | "manuscript_identification" | "commentary"
  | "term_history_assertion" | "bibliographic_claim";

export type EpistemicState =
  | "machine_proposed" | "human_proposed" | "checked" | "expert_reviewed"
  | "editorially_accepted" | "disputed" | "rejected";

export interface Annotation {
  id: string;            // pt:annotation:{hash}
  target: string;        // any object or annotation id
  type: AnnotationType;
  payload: Record<string, unknown>;  // the specific claim's data
  origin: Origin;        // machine | editor | scholar | institution
  status: EpistemicState;
  certainty?: Certainty; // ≠ status
  evidence: Evidence[];
  review_events: string[];  // ReviewEvent ids
  created_at: string;
  created_by: string;
  supersedes?: string;   // id of the annotation this replaces
  superseded_by?: string;
}

export type ReviewScope =
  | "work_identity" | "date" | "translation" | "term_sense" | "parallel"
  | "manuscript_identification" | "tradition_classification" | "grammar"
  | "lexical" | "doctrinal" | "authorship";

// ── the graph container ────────────────────────────────────────────────────

export interface ScholarlyGraph {
  objects: GraphObject[];
  annotations: Annotation[];
  reviews: ReviewEvent[];
  crosswalks: { our_id: string; external_system: string; external_id: string; relationship: string; confidence: string; status: string }[];
  rights: Record<string, Record<string, string>>;  // object_id -> permission -> yes/no/unknown/conditional
}
