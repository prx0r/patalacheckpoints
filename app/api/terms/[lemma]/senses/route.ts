// GET /api/terms/:lemma/senses — the accepted term senses from the ledger.
// This is accepted corpus knowledge (review-promoted), NOT a dictionary and NOT
// evidence of occurrence. Proposals live separately (see /api/terms/:lemma/proposals).

import { NextRequest, NextResponse } from "next/server";
import { getTerm, getProposals } from "@/data/corpus/terms";

export async function GET(
  _req: NextRequest,
  ctx: { params: Promise<{ lemma: string }> },
) {
  const { lemma } = await ctx.params;
  const term = getTerm(lemma);
  if (!term) {
    return NextResponse.json({ error: "not_found", lemma }, { status: 404 });
  }
  return NextResponse.json({
    lemma,
    senses: term.senses,
    preferred_renderings: term.preferred_renderings ?? [],
    avoid: term.avoid ?? [],
    notes: term.notes ?? [],
    proposals: getProposals(lemma).length,
    provenance: { note: "Accepted term senses, review-promoted. Machine proposals live separately and are never auto-accepted.", api_version: "1.0" },
  });
}
