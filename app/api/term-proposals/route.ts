// GET /api/term-proposals — the machine/human term-sense proposals (never auto-accepted).
// Filter by ?lemma= or ?status=proposed|reviewed|accepted.
import { NextRequest, NextResponse } from "next/server";
import { getProposals } from "@/data/corpus/terms";

export async function GET(req: NextRequest) {
  const lemma = req.nextUrl.searchParams.get("lemma");
  const status = req.nextUrl.searchParams.get("status");
  let list = getProposals(lemma ?? undefined);
  if (status) list = list.filter((p) => (p.status ?? "") === status);
  return NextResponse.json({
    count: list.length,
    proposals: list,
    provenance: { note: "Term-sense proposals. Only a human review event promotes proposed → reviewed → accepted into terms.json.", api_version: "1.0" },
  });
}
