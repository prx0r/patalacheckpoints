// GET /api/texts/kramasadbhava/decisions — the unresolved/evidence-gap aggregation.
// Queries the unit's published decisions to pick C1 targets: which passages have OPEN
// cruxes, which have evidence gaps, which terms recur. This is the demand-driven queue.

import { NextRequest, NextResponse } from "next/server";
import { listUnitPassages, getPublishedTranslation } from "@/data/corpus/published";

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const onlyOpen = searchParams.get("open") === "true";
  const onlyGaps = searchParams.get("evidence_gap") === "true";

  const passages = listUnitPassages("kramasadbhava");
  const all: any[] = [];
  for (const p of passages) {
    const pub = getPublishedTranslation(p.passage_id);
    if (!pub) continue;
    for (const d of pub.decisions) {
      const gap = d.evidence_state === "evidence_missing" || d.evidence_state === "evidence_conflict";
      if (onlyOpen && d.status !== "OPEN") continue;
      if (onlyGaps && !gap) continue;
      all.push({
        decision_id: d.id,
        passage: p.passage_id,
        locator: p.locator,
        claim: d.claim,
        status: d.status,
        evidence_state: d.evidence_state,
        surface_rendering: d.surface_rendering,
      });
    }
  }
  return NextResponse.json({
    count: all.length,
    query: { open_only: onlyOpen, evidence_gap_only: onlyGaps },
    decisions: all,
    provenance: { note: "The C1-target queue: passages with OPEN cruxes or evidence gaps are where editorial/main-model effort should go first.", api_version: "1.0" },
  });
}
