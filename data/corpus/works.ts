// The corpus manifest — the work registry. Derived from the bibliography
// (audited + seed), shaped for the passage/MCP layer: stable work_id, traditions
// with confidence, date range with certainty, translation status, source editions.
// Uncertain metadata is given explicit confidence, not forced perfect.

import { audited, seed } from "../atlas";
import { BibliographyRecord } from "../atlas/bibliographyTypes";

export interface CorpusWork {
  id: string;
  title: string;
  alternateTitles?: string[];
  authors?: string[];
  traditions: { id: string; label: string; certainty: "high" | "medium" | "low" }[];
  date?: { not_before?: number; not_after?: number; certainty: "approximate" | "medium" | "low" };
  region?: string[];
  genres?: string[];
  languages: string[];
  source_editions: string[];
  translation_status: "complete" | "partial" | "none";
  bibliography_state: "seed" | "translation_ready" | "audited"; // the gate
  research_roles?: string[];
  rights?: {
    status: "open" | "public_domain" | "permission" | "restricted" | "unknown";
    license?: string;
    redistribution?: boolean;
    api_fulltext?: boolean;
    model_training?: boolean;
    notes?: string;
    // operational permissions matrix (nextdev): each yes/no/unknown/conditional
    may_embed?: "yes" | "no" | "unknown" | "conditional";
    may_rag?: "yes" | "no" | "unknown" | "conditional";
    may_evaluation?: "yes" | "no" | "unknown" | "conditional";
    may_commercial_feed?: "yes" | "no" | "unknown" | "conditional";
  };
  related: string[];
  verified: boolean;
  urn: string;
}

function slug(t: string): string {
  return t.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || t;
}

// Anchor role vs tradition membership. "Same tradition" is too crude for
// retrieval — a later commentary, root Tantra, anthology and philosophical
// synthesis should not be weighted equally. research_roles captures function.
const RESEARCH_ROLES: Record<string, string[]> = {
  tantraloka: ["synthesis", "citation_source", "commentarial_bridge"],
  tantrasadbhava: ["primary_scripture", "terminology_anchor"],
  malinivijayottara: ["primary_scripture", "terminology_anchor"],
  spandakarika: ["primary_scripture", "synthesis"],
  sivasutra: ["primary_scripture", "terminology_anchor"],
  kramasadbhava: ["primary_scripture", "translation_target", "terminology_anchor"],
  mahanayaprakasha: ["primary_scripture", "translation_target"],
  kramastotra: ["primary_scripture", "translation_target"],
  devipancasataka: ["primary_scripture", "translation_target", "terminology_anchor"],
  kubjikamata: ["primary_scripture", "translation_target", "terminology_anchor"],
  satsahasrasamhita: ["primary_scripture", "translation_target"],
  shrimatottara: ["primary_scripture"],
  kularatnoddyota: ["primary_scripture"],
  timirodghatana: ["primary_scripture", "translation_target"],
  kulasara: ["primary_scripture", "translation_target"],
  vijnanabhairava: ["primary_scripture", "translation_target", "terminology_anchor"],
};

function toWork(b: BibliographyRecord): CorpusWork {
  return {
    id: b.id,
    urn: `tantra:text:${b.id}`,
    title: b.work,
    traditions: b.traditions.map((t) => ({ id: slug(t), label: t, certainty: "medium" as const })),
    date: b.period
      ? { not_before: b.period.start, not_after: b.period.end, certainty: b.period.approximate ? ("approximate" as const) : ("medium" as const) }
      : undefined,
    languages: ["sa"],
    source_editions: [...new Set(b.textSources.map((s) => s.provider ?? s.url).filter((x): x is string => Boolean(x)))],
    translation_status: b.translationStatus,
    bibliography_state: b.state ?? (b.verified ? ("audited" as const) : ("seed" as const)),
    research_roles: RESEARCH_ROLES[b.id],
    rights: { status: "unknown", notes: "Source-specific rights must be resolved before full-text redistribution/API/training. Our own working translations are ours." },
    related: b.related ?? [],
    verified: b.verified,
  };
}

export const works: CorpusWork[] = [...audited, ...seed].map(toWork);
