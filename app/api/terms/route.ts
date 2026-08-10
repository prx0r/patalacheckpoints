// GET /api/terms — the full accepted term ledger (summary), each with proposal count.
import { NextRequest, NextResponse } from "next/server";
import { getTerms, getProposals } from "@/data/corpus/terms";

export async function GET() {
  const terms = getTerms();
  const proposals = getProposals();
  const out = terms.map((t) => ({
    lemma: t.lemma,
    sense_labels: t.senses.map((s) => s.label),
    preferred_renderings: t.preferred_renderings ?? [],
    proposals: proposals.filter((p) => p.lemma === t.lemma).length,
  }));
  return NextResponse.json({
    count: out.length,
    terms: out,
    proposal_count: proposals.length,
    provenance: { note: "Accepted term senses (review-promoted). Proposals are separate and never auto-accepted.", api_version: "1.0" },
  });
}
