// GET /api/passages/:id/translation — the publishable auditable translation object.
// Returns the translation as spans + alignments + decisions, so a reader can click a
// phrase and see WHY it was rendered that way. Accepts "kramasadbhava:1.8" or the full
// passage id.

import { NextRequest, NextResponse } from "next/server";
import { getPublishedTranslation } from "@/data/corpus/published";

export async function GET(
  _req: NextRequest,
  ctx: { params: Promise<{ id: string }> },
) {
  const { id: raw } = await ctx.params;
  const id = raw.startsWith("pt:") || raw.startsWith("tantra:")
    ? raw
    : `pt:passage:${raw}`;
  const pub = getPublishedTranslation(id);
  if (!pub) {
    return NextResponse.json({ error: "not_found", id, hint: "no published auditable translation yet for this passage" }, { status: 404 });
  }
  return NextResponse.json({
    passage_id: pub.passage_id,
    work_id: pub.work_id,
    text: pub.text,
    version_id: pub.version_id,
    version: pub.version,
    review_state: pub.review_state,
    provenance: pub.provenance,
    source_spans: pub.source_spans,
    target_spans: pub.target_spans,
    alignments: pub.alignments,
    decisions: pub.decisions,
    evidence: pub.evidence,
    c1: pub.c1,       // the commentary (when present), toggled on/off, verse-by-verse
    provenance_note: {
      note: "The published auditable translation: every phrase is addressable. Click a source or target span → its decision → evidence → review. Machine decisions are proposals until a review event promotes them.",
      api_version: "1.0",
    },
  });
}
