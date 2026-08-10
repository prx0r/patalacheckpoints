// The atlas data model — chaining.dev's project model reinterpreted as
// an entity-relation graph for the Śaiva-Śākta ecosystem.
//
// The crucial design point (from the reference map): relations are NOT
// encoded as `parent:` fields on entities. History is not a family tree.
// Relations live separately, typed, with a confidence level — so the
// canonical research we're building can populate the edges.

export type EntityType = "tradition" | "text" | "person" | "concept";

export interface AtlasEntity {
  id: string;
  type: EntityType;
  title: string;
  sanskrit?: string;
  period?: {
    start?: number;
    end?: number;
    approximate?: boolean;
  };
  summary: string;
  concepts?: string[];
  resources?: {
    title: string;
    href: string;
    type: "translation" | "explainer" | "scholarship";
  }[];
  // dossier — the deep content shown when clicked (the Tantrāloka-workbook pattern)
  dossier?: {
    systemicFunction?: string;
    problems?: string[];
    doctrinalCore?: string[];
    dependencies?: string[];
    outputs?: string[];
  };
  // bibliography — the spec-2 "WHAT EXISTS?" record (the atlas/bibliography spine).
  // Every translation-status assertion carries its evidence (statusChecked + statusEvidence),
  // and the public phrase is deliberately "No complete English translation located", not
  // "Untranslated", unless scholarship explicitly establishes otherwise.
  bibliography?: {
    status?: {
      sanskritEtext?: boolean;
      criticalEdition?: boolean;
      completeEnglish?: boolean;
      partialEnglish?: boolean;
      siteWorkingTranslation?: boolean;
      communityReviewed?: boolean;
      statusChecked?: string;
      statusEvidence?: string;
      statusPhrase?: string;
    };
    manuscripts?: {
      siglum?: string;
      note?: string;
    }[];
    scholarship?: string[];
    related?: string[];
  };
}

export type RelationType =
  | "develops-from"
  | "textual-borrowing"
  | "influence"
  | "synthesis"
  | "commentary"
  | "contains"
  | "conceptual-parallel";

export type Confidence = "established" | "strong" | "possible";

export interface AtlasRelation {
  source: string;
  target: string;
  type: RelationType;
  confidence: Confidence;
  evidence?: string[];
}
