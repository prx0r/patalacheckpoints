import { traditions } from "./traditions";
import { texts } from "./texts";
import { textsAdditional } from "./texts";
import { people } from "./people";
import { concepts } from "./concepts";
import { relations } from "./relations";
import { audited } from "./audited";
import { seed } from "./bibliographySeed";
import { sivaqueueSeed } from "./sivaqueueSeed";
import { sivaqueue34Seed } from "./sivaqueue34Seed";
import { sivaqueueGapSeed } from "./sivaqueueGapSeed";
import { sanskritreeImportSeed } from "./sanskritreeImportSeed";
import { BibliographyRecord } from "./bibliographyTypes";
import { resources } from "./resources";
import type { Resource, ResourceType, Tradition } from "./resourcesTypes";
import { TYPE_LABEL } from "./resourcesTypes";
import { AtlasEntity, AtlasRelation } from "@/lib/atlas";

export const atlasEntities: AtlasEntity[] = [
  ...traditions,
  ...texts,
  ...textsAdditional,
  ...people,
  ...concepts,
];

export { relations };
export { audited };
export { seed };
export { sivaqueueSeed };
export { sivaqueue34Seed };
export { sivaqueueGapSeed };
export { sanskritreeImportSeed };
export { concepts };
export { traditions };
export type { BibliographyRecord, BibTranslation, BibSource, BibScholarship, ResourceTier } from "./bibliographyTypes";
export { resources };
export type { Resource, ResourceType, Tradition };
export { TYPE_LABEL };

export const relationTypes = relations as AtlasRelation[];

export function getEntity(id: string): AtlasEntity | undefined {
  return atlasEntities.find((e) => e.id === id);
}

export function getRelationsFor(id: string): AtlasRelation[] {
  return relations.filter((r) => r.source === id || r.target === id);
}

// The relation-type → label/colour mapping for the edge rendering.
export const relationMeta: Record<
  string,
  { label: string; color: string; dash?: string }
> = {
  "develops-from": { label: "DEVELOPS", color: "#8b3528" }, // vermilion
  "textual-borrowing": { label: "BORROWS", color: "#c99545" }, // saffron
  influence: { label: "INFLUENCES", color: "#75552b", dash: "6 3" }, // saffron-dim
  synthesis: { label: "SYNTHESIZES", color: "#8b3528" },
  commentary: { label: "COMMENTS", color: "#928873" }, // ash
  contains: { label: "CONTAINS", color: "#5a5145" },
  "conceptual-parallel": { label: "PARALLEL", color: "#75552b", dash: "2 3" },
};

export const typeColor: Record<string, string> = {
  tradition: "#c99545", // saffron
  text: "#8b3528", // vermilion
  person: "#928873", // ash
  concept: "#75552b", // saffron-dim
};
