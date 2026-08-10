// GET /api/terms/:lemma/occurrences — coarse surface occurrences of a lemma in the
// segmented corpus. Honest about method: match_method substring, lemmatized false
// (Sanskrit inflection means this is NOT lemma retrieval). Use search_passages under
// the hood; real lemma indexing is a later capability.

import { NextRequest, NextResponse } from "next/server";
import { searchPassages } from "@/data/corpus/passages";

export async function GET(
  _req: NextRequest,
  ctx: { params: Promise<{ lemma: string }> },
) {
  const { lemma } = await ctx.params;
  const workId = _req.nextUrl.searchParams.get("work_id");
  const limit = parseInt(_req.nextUrl.searchParams.get("limit") ?? "50", 10);
  let hits = searchPassages(lemma);
  if (workId) hits = hits.filter((p) => p.work_id === workId);
  const truncated = hits.length > limit;
  return NextResponse.json({
    lemma,
    match_method: "substring",
    lemmatized: false,
    work_id: workId ?? null,
    count: hits.length,
    truncated,
    occurrences: hits.slice(0, limit),
    provenance: { note: "Substring surface occurrences only — NOT lemmatized. 'śakti / śaktiḥ / śaktim' are not interchangeable for a raw concordance.", api_version: "1.0" },
  });
}
