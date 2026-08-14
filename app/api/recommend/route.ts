// GET /api/recommend?work=<id>  or  ?passage=<id>&see_also=<C1 see-also>
// The deterministic related-text rail ("similar sources"). Given a work or passage, returns
// the recommended related texts ranked by relation type × confidence, assembled from the
// existing spines + relations + hub + the passage's C1 see_also.
//
// Deterministic first (data already exists); ML-similarity refines it later.

import { NextRequest, NextResponse } from "next/server";
import { recommendForWork, recommendForPassage } from "@/data/corpus/recommend";

export async function GET(req: NextRequest) {
  const work = req.nextUrl.searchParams.get("work");
  const passage = req.nextUrl.searchParams.get("passage");
  const seeAlso = req.nextUrl.searchParams.get("see_also") ?? "";

  if (passage) {
    return NextResponse.json({ passage, recommendations: recommendForPassage(passage, seeAlso) });
  }
  if (work) {
    return NextResponse.json({ work, recommendations: recommendForWork(work) });
  }
  return NextResponse.json({ error: "missing_param", hint: "?work=<id> or ?passage=<id>&see_also=<...>" }, { status: 400 });
}
