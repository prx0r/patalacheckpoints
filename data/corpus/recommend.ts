// recommend.ts — the deterministic related-text rail ("similar sources").
//
// Given a work or passage, recommend the related texts ranked by
//   relation type × confidence × shared terms
// using data that ALREADY exists:
//   - canonical-spines.ts  (the root/commentary/synthesis path per school)
//   - relations.ts         (typed edges)
//   - hub.ts               (a work's essays/arguments/pushing)
//   - the passage C1's see_also (the local "read this too")
//
// Deterministic first; ML-similarity refines it later (after the embedding index).
// This is the "Netflix for related texts" rail.

import { spineForWork, spineFor } from "./canonical-spines";
import { relationsFor } from "./relations";
import { outputsFor } from "./hub";
import { works } from "./works";

export type RecommendRelation =
  | "ROOT_TEXT"        // the kārikā/root this comments on
  | "PARALLEL"         // a parallel commentary (e.g. IPV to IPVV)
  | "CONTINUES_ARGUMENT" // next step in the same argument
  | "OPPOSING_POSITION"  // the opponent (Buddhist, Vaiśeṣika)
  | "DOCTRINAL_PARALLEL" // same doctrine elsewhere (Tantrāloka)
  | "SCHOLARSHIP"      // the adjudicating scholarship (Ratié)
  | "SEE_ALSO"         // the C1's own cross-references

export interface RecommendItem {
  work_id: string;
  title: string;
  relation: RecommendRelation;
  certainty: "established" | "strong" | "possible";
  note?: string;
}

const STEP_ROLE_TO_RELATION: Record<string, RecommendRelation> = {
  root_scripture: "ROOT_TEXT",
  commentary: "PARALLEL",
  synthesis: "DOCTRINAL_PARALLEL",
  anchor: "SCHOLARSHIP",
};

// For a work: recommend from its school spine (root/commentary/synthesis) + its relations.
export function recommendForWork(workId: string): RecommendItem[] {
  const items: RecommendItem[] = [];
  const spine = spineForWork(workId);
  const w = works.find((x) => x.id === workId);
  if (spine) {
    for (const step of spine.steps) {
      if (step.work_id === workId) continue;
      const sw = works.find((x) => x.id === step.work_id);
      items.push({
        work_id: step.work_id,
        title: sw?.title ?? step.work_id,
        relation: STEP_ROLE_TO_RELATION[step.role] ?? "DOCTRINAL_PARALLEL",
        certainty: "strong",
        note: step.note,
      });
    }
  }
  // relations graph edges (the direct textual relatives)
  for (const r of relationsFor(workId)) {
    const other = r.source === workId ? r.target : r.source;
    if (other === workId) continue;
    const ow = works.find((x) => x.id === other);
    items.push({
      work_id: other,
      title: ow?.title ?? other,
      relation: "DOCTRINAL_PARALLEL",
      certainty: r.certainty,
      note: `relations: ${r.relation}`,
    });
  }
  return dedupe(items);
}

// For a passage: recommend from its C1 see_also (the local "read this too") + the work rail.
export function recommendForPassage(passageId: string, seeAlso: string): RecommendItem[] {
  const items: RecommendItem[] = [];
  // the work rail (root/parallel/synthesis)
  const workId = passageId.includes(":ipvv:") ? "isvarapratyabhijnavivrtivimarsini" : passageId.split(":")[2] ?? "";
  items.push(...recommendForWork(workId));
  // the C1's own see_also (e.g. "V2-B · V2-P · IPK 1.3")
  if (seeAlso) {
    for (const ref of seeAlso.split(/[·,;]/)) {
      const clean = ref.trim();
      if (clean) items.push({ work_id: workId, title: clean, relation: "SEE_ALSO", certainty: "strong" });
    }
  }
  return dedupe(items);
}

function dedupe(items: RecommendItem[]): RecommendItem[] {
  const seen = new Set<string>();
  const out: RecommendItem[] = [];
  for (const it of items) {
    const key = `${it.work_id}:${it.title}:${it.relation}`;
    if (seen.has(key)) continue;
    seen.add(key);
    out.push(it);
  }
  // order: root > parallel > continue > opposing > doctrinal > scholarship > see-also
  const order: Record<RecommendRelation, number> = {
    ROOT_TEXT: 0, PARALLEL: 1, CONTINUES_ARGUMENT: 2, OPPOSING_POSITION: 3,
    DOCTRINAL_PARALLEL: 4, SCHOLARSHIP: 5, SEE_ALSO: 6,
  };
  return out.sort((a, b) => order[a.relation] - order[b.relation]);
}
