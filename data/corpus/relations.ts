// The corpus manifest — relationship edges. Derived from the atlas relations
// (already typed + confidence + evidence). These let the passage/MCP layer rank
// context: same work > direct textual relative > same tradition > adjacent.

import { relations as atlasRelations } from "../atlas";

export interface CorpusRelation {
  source: string;
  target: string;
  relation: string;
  certainty: "established" | "strong" | "possible";
  evidence: string[];
}

export const relations: CorpusRelation[] = atlasRelations.map((r) => ({
  source: r.source,
  target: r.target,
  relation: r.type,
  certainty: r.confidence,
  evidence: r.evidence ?? [],
}));

export function relationsFor(workId: string): CorpusRelation[] {
  return relations.filter((r) => r.source === workId || r.target === workId);
}
