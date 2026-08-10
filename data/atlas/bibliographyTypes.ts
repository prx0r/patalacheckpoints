// The Tantra Hub bibliography — the shared types.
// The schema is LLM-readable AND scholar-friendly: root-vs-commentary are separate
// records; translations[] carry language/coverage/style; textSources[] carry
// type+coverage+editor+year; every resource carries a provenance tier.
// Tier = provenance class, NOT intellectual quality (Dyczkowski's own site is D).

export type ResourceTier = "A" | "B" | "C" | "D" | "E";

export interface BibTranslation {
  language: string;
  translator?: string;
  work?: string;
  coverage?: string; // e.g. "1.1–1.399", "complete", "chs. 1–4, 7, 12–17"
  complete: boolean;
  type: "scholarly" | "traditional" | "independent" | "working";
  year?: number;
  url?: string;
  tier?: ResourceTier;
  note?: string;
}

export interface BibSource {
  id?: string; // stable addressable id, e.g. "pt:src:kramasadbhava:dyczkowski-ed"
  type: "critical_edition" | "edition" | "etext" | "scan";
  coverage?: string;
  editor?: string;
  year?: number;
  url?: string;
  provider?: string;
  tier?: ResourceTier;
  rights?: { status: "open" | "public_domain" | "permission" | "restricted" | "unknown" };
  note?: string;
}

export interface BibScholarship {
  author?: string;
  work: string;
  year?: number;
  url?: string;
  tier?: ResourceTier;
  kind?: "study" | "lecture" | "course" | "commentary" | "explainer";
}

export interface BibliographyRecord {
  id: string;
  work: string;
  traditions: string[];
  period?: { start?: number; end?: number; approximate?: boolean };
  verified: boolean; // false = seed, not yet audited (legacy)
  // The bibliography gate (the reviewer's contract): how far this record has been
  // brought toward translation-readiness. unknown ≠ missing. Optional for backward
  // compat with existing records; derived as `seed` when absent.
  state?: "seed" | "translation_ready" | "audited";
  textSources: BibSource[];
  translations: BibTranslation[];
  translationStatus: "complete" | "partial" | "none";
  statusLabel: string;
  statusChecked: string;
  statusEvidence?: string;
  scholarship?: BibScholarship[];
  related?: string[];
  manuscripts?: { siglum?: string; note?: string }[];
  notes?: string[];
  // explicit unknowns (unknown ≠ missing — the contract)
  rights?: { status: "open" | "public_domain" | "permission" | "restricted" | "unknown" };
}
