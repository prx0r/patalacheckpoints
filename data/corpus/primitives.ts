// The six formal primitives (per nextdev.md): Identity, Assertion, Evidence,
// Provenance, Review, Rights. Lean — enough structure that every contested claim
// is traceable, reviewable, reversible. Seed data lives in data/primitives.json.

import { readFileSync } from "fs";
import path from "path";

export type EpistemicState = "machine_proposed" | "human_proposed" | "checked" | "expert_reviewed" | "editorially_accepted" | "disputed" | "rejected";
export type Certainty = "certain" | "probable" | "possible" | "uncertain";
export type Origin = "machine" | "editor" | "scholar" | "institution";

export interface Evidence {
  resource: string;
  locator?: string;
  role: "supports" | "contradicts" | "defines" | "dates" | "identifies" | "quotes" | "parallel" | "commentary";
  note?: string;
}

export interface Assertion {
  id: string;
  subject: string;
  predicate: string;
  value: string;
  certainty?: Certainty;
  status: EpistemicState;
  origin: Origin;
  evidence: Evidence[];
  review_events: string[];
  created_at?: string;
}

export interface ReviewEvent {
  id: string;
  target: string;
  scope: "work_identity" | "date" | "translation" | "term_sense" | "parallel" | "manuscript_identification" | "tradition_classification";
  reviewer: { kind: string; id: string };
  decision: "accept" | "reject" | "revise" | "needs_specialist" | "abstain";
  reason?: string;
  created_at?: string;
}

export interface Crosswalk {
  our_id: string;
  external_system: string;
  external_id: string;
  relationship: "same" | "likely_same" | "derived_from" | "version_of" | "witness_of" | "references";
  confidence: "established" | "strong" | "possible";
  status: "unresolved" | "candidate_match" | "confirmed_match" | "rejected_match";
}

// Rights: operational permissions, each yes/no/unknown/conditional. Unknown is valid.
export type Permission = "yes" | "no" | "unknown" | "conditional";
export interface Rights {
  public_display: Permission;
  download: Permission;
  redistribution: Permission;
  api_fulltext: Permission;
  index_search: Permission;
  embed: Permission;
  rag: Permission;
  embeddings: Permission;
  model_training: Permission;
  evaluation: Permission;
  commercial_feed: Permission;
}

const FILE = path.join(process.cwd(), "data", "primitives.json");
let _data: any = null;
function load(): any {
  if (_data) return _data;
  try {
    _data = JSON.parse(readFileSync(FILE, "utf8"));
  } catch {
    _data = { assertions: [], reviews: [], crosswalks: [], epistemic_states: [], certainty_levels: [], origins: [] };
  }
  return _data;
}

export function getAssertions(subject?: string): Assertion[] {
  const a = load().assertions as Assertion[];
  return subject ? a.filter((x) => x.subject === subject) : a;
}
export function getReviews(target?: string): ReviewEvent[] {
  const r = load().reviews as ReviewEvent[];
  return target ? r.filter((x) => x.target === target) : r;
}
export function getCrosswalks(ourId?: string): Crosswalk[] {
  const c = load().crosswalks as Crosswalk[];
  return ourId ? c.filter((x) => x.our_id === ourId) : c;
}
export function DEFAULT_RIGHTS(): Rights {
  return {
    public_display: "unknown",
    download: "unknown",
    redistribution: "unknown",
    api_fulltext: "unknown",
    index_search: "unknown",
    embed: "unknown",
    rag: "unknown",
    embeddings: "unknown",
    model_training: "unknown",
    evaluation: "unknown",
    commercial_feed: "unknown",
  };
}
