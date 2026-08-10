// GET /api/decisions/:id — the full audit trail for one translation decision.
// Resolves the decision's spans, evidence, review events, and version lineage.

import { NextRequest, NextResponse } from "next/server";
import { getDecision, getEvidence } from "@/data/corpus/published";
import { getReviews } from "@/data/corpus/primitives";

export async function GET(
  _req: NextRequest,
  ctx: { params: Promise<{ id: string }> },
) {
  const { id } = await ctx.params;
  const decision = getDecision(id);
  if (!decision) {
    return NextResponse.json({ error: "not_found", id }, { status: 404 });
  }
  const reviews = getReviews(decision.id);
  // resolve each EvidenceUse to its full EvidenceItem (the first-class evidence)
  const resolved_evidence = decision.evidence
    .map((use) => ({ use, item: getEvidence(use.evidence_id) }))
    .filter((x) => x.item !== undefined)
    .map(({ use, item }) => ({ ...use, item }));
  const unresolved = decision.evidence.filter((u) => !getEvidence(u.evidence_id));
  return NextResponse.json({
    id: decision.id,
    passage_id: decision.passage_id,
    translation_version_id: decision.translation_version_id,
    type: decision.type,
    claim: decision.claim,
    surface_rendering: decision.surface_rendering,
    adjudicated_reading: decision.adjudicated_reading ?? null,
    alternatives: decision.alternatives,
    status: decision.status,
    evidence_state: decision.evidence_state,
    editorial_status: decision.editorial_status,
    method: decision.method,
    reason: decision.reason,
    source_span_ids: decision.source_span_ids,
    target_span_ids: decision.target_span_ids,
    evidence: resolved_evidence,
    unresolved_evidence: unresolved.map((u) => u.evidence_id),
    origin: decision.origin,
    created_at: decision.created_at,
    created_by: decision.created_by,
    supersedes: decision.supersedes ?? null,
    reviews,
    audit_note: {
      note: "This decision is a proposal until a scoped ReviewEvent promotes it. status (CONSTRAINED/PREFERRED/OPEN) ≠ certainty ≠ review state.",
      api_version: "1.0",
    },
  });
}
