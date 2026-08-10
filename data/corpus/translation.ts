// The publishable translation object — the canonical product.
//
// The thing Pāṭala publishes is NOT "an English string." It is a translation where
// every phrase is addressable: source span → decision → target span, with evidence,
// review, and version history. T1–T3 are workflow stages that GENERATE candidate
// decisions; this is the object that object renders.
//
// See docs/SCHOLARLY_GRAPH.md + NORTHSTAR's LEXICAL_DECISION entity.

import type { Evidence, ReviewEvent } from "./primitives";

// ── spans ───────────────────────────────────────────────────────────────────

// A source span: a segment of the Sanskrit. Semantic IDs (tied to token/segment),
// NOT brittle character offsets.
export interface SourceSpan {
  id: string;            // pt:srcspan:{passage}:{n}
  passage_id: string;    // pt:passage:{work}:{loc}
  text: string;          // the Sanskrit surface
  start?: number;        // optional char offset (informational, not canonical identity)
  end?: number;
}

export interface TargetSpan {
  id: string;            // pt:tgtspan:{passage}:{n}
  translation_version_id: string;
  text: string;          // the English surface
}

// Many-to-many alignment between source and target spans.
export type AlignmentType = "direct" | "reordered" | "supplied" | "omitted" | "merged" | "split";

export interface Alignment {
  id: string;            // pt:align:{passage}:{n}
  source_span_ids: string[];
  target_span_ids: string[];
  type: AlignmentType;
  decision_ids: string[];
}

// ── decisions ───────────────────────────────────────────────────────────────

export type DecisionType =
  | "LEXICAL" | "GRAMMATICAL" | "TEXTUAL" | "REFERENTIAL" | "SUPPLIED" | "ALIGNMENT";

export type DecisionStatus =
  | "CONSTRAINED" | "PREFERRED" | "OPEN" | "RECONSTRUCTED";

// The central object: one materially interpretive choice, fully auditable.
export interface TranslationDecision {
  id: string;            // pt:decision:{passage}:{type}:{n}
  passage_id: string;
  translation_version_id: string;

  source_span_ids: string[];
  target_span_ids: string[];

  type: DecisionType;
  claim: string;
  preferred_reading: string;
  alternatives: string[];

  status: DecisionStatus;
  reason: string;

  evidence: Evidence[];
  review_events: string[];   // ReviewEvent ids

  origin: string;        // machine | editor | scholar
  created_at: string;
  created_by: string;
  supersedes?: string;   // decision id this replaces
}

// ── the assembled object ────────────────────────────────────────────────────

export interface PublishedTranslation {
  passage_id: string;
  work_id: string;
  text: string;                     // the current English
  version_id: string;
  version: number;
  source_spans: SourceSpan[];
  target_spans: TargetSpan[];
  alignments: Alignment[];
  decisions: TranslationDecision[];
  review_state: string;             // proposed | reviewed | accepted | mixed
  provenance: {
    base_source: string;
    edition: string;
    translation_version_id: string;
  };
}
