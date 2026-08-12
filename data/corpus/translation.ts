// The publishable translation object — the canonical product.
//
// The thing Pāṭala publishes is NOT "an English string." It is a translation where
// every phrase is addressable: source span → decision → target span, with evidence,
// review, and version history. T1–T3 are workflow stages that GENERATE candidate
// decisions; this is the object that renders.
//
// See docs/SCHOLARLY_GRAPH.md + NORTHSTAR's LEXICAL_DECISION entity.

import type { Origin } from "./primitives";

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
  method?: DerivationMethod;   // how this alignment was derived
}

// ── evidence (FIRST-CLASS) ──────────────────────────────────────────────────

export type EvidenceVerification =
  | "verified" | "locator_unverified" | "quote_unverified" | "resource_missing";

// A stable, addressable evidence item — the thing a decision's reasoning bottoms out on.
export interface EvidenceItem {
  id: string;            // pt:evidence:{n}
  resource_id: string;   // a Resource or passage id (resolvable)
  locator?: string;      // page / verse / folio
  excerpt?: string;      // the retrieved quote / text
  verification: EvidenceVerification;
}

export type EvidenceRole =
  | "supports" | "contradicts" | "defines" | "dates" | "identifies"
  | "quotes" | "parallel" | "commentary";

// Links a decision to an EvidenceItem, with its role in the argument.
export interface EvidenceUse {
  evidence_id: string;
  role: EvidenceRole;
  note?: string;
}

// ── decisions ───────────────────────────────────────────────────────────────

export type DecisionType =
  | "LEXICAL" | "GRAMMATICAL" | "TEXTUAL" | "REFERENTIAL" | "SUPPLIED" | "ALIGNMENT";

export type DecisionStatus =
  | "CONSTRAINED" | "PREFERRED" | "OPEN" | "RECONSTRUCTED";

// How a claim/alignment was derived (provenance at the assertion level).
export type DerivationMethod =
  | "human" | "llm" | "embedding" | "exact_match" | "lexical_rule"
  | "imported_scholarship" | "commentary_gloss" | "pipeline_adjudication" | "pipeline";

// What the EVIDENCE says (≠ what adjudication was reached ≠ what was reviewed).
export type EvidenceState =
  | "grounded" | "partially_grounded" | "source_only" | "evidence_missing" | "evidence_conflict";

// The editorial/review state of a decision (derived from ReviewEvents, never manual).
export type EditorialStatus = "proposed" | "reviewed" | "accepted" | "disputed";

// The central object: one materially interpretive choice, fully auditable.
export interface TranslationDecision {
  id: string;            // pt:decision:{passage}:{type}:{n}
  passage_id: string;
  translation_version_id: string;

  source_span_ids: string[];
  target_span_ids: string[];

  type: DecisionType;
  claim: string;

  // For OPEN: surface_rendering is the current editorial surface text, NOT a resolution.
  surface_rendering: string;
  adjudicated_reading?: string;      // set only when the crux is resolved
  alternatives: string[];

  status: DecisionStatus;            // CONSTRAINED / PREFERRED / OPEN / RECONSTRUCTED
  evidence_state: EvidenceState;     // grounded / partially_grounded / ...
  editorial_status: EditorialStatus; // DERIVED from review events
  reason: string;

  method: DerivationMethod;          // how this claim was derived
  evidence: EvidenceUse[];           // → EvidenceItem ids
  review_events: string[];           // ReviewEvent ids

  origin: Origin;                    // machine | editor | scholar | institution
  created_at: string;
  created_by: string;
  supersedes?: string;               // decision id this replaces
}

// ── the assembled object ────────────────────────────────────────────────────

export type ReviewState = "proposed" | "reviewed" | "accepted" | "mixed" | "disputed";

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
  evidence: EvidenceItem[];         // the resolved evidence pool
  review_state: ReviewState;        // DERIVED from decision review events
  // C1 — the commentary, toggled on/off on the reader. Verse-by-verse, razor-sharp
  // (Dyczkowski-like), extracting the doctrinal depth beneath the audited T3.
  // Optional (not all passages have a C1 yet).
  c1?: {
    body: string;
    // verse_commentary: one entry per verse/locator, in order — each a sharp
    // verse-by-verse analysis that breathes, tied to the T3 verse it comments on.
    verse_commentary?: { locator: string; commentary: string }[];
    claim_links: { claim: string; target_span_id: string }[];
    // from the IPVV c1/read renderings (terms / see-also), optional
    terms?: string;
    see_also?: string;
  };
  // the structured c1/source record (SUMMARY/FUNCTION/KEY TERMS/...) when present
  c1_source?: Record<string, string>;
  provenance: {
    base_source: string;
    edition: string;
    translation_version_id: string;
  };
}

// ── review-state derivation ─────────────────────────────────────────────────

export function deriveReviewState(decisions: TranslationDecision[]): ReviewState {
  const states = new Set(decisions.map((d) => d.editorial_status));
  if (!states.size) return "proposed";
  if (states.has("disputed")) return "disputed";
  if (states.size === 1) {
    const s = [...states][0];
    return s === "accepted" ? "accepted" : s === "reviewed" ? "reviewed" : "proposed";
  }
  // mixed: some accepted/reviewed, some not
  if (states.has("accepted") || states.has("reviewed")) return "mixed";
  return "proposed";
}
