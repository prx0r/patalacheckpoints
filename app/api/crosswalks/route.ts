// GET /api/crosswalks — our object ↔ external object mappings (first-class).
// Generalizes the OCHS resolution: relationship (same_as / witness_of / ...),
// confidence, status (unresolved / candidate / confirmed / rejected). Filter by ?our_id=.

import { NextRequest, NextResponse } from "next/server";
import { getCrosswalks } from "@/data/corpus/primitives";

export async function GET(req: NextRequest) {
  const ourId = req.nextUrl.searchParams.get("our_id");
  const list = getCrosswalks(ourId ?? undefined);
  return NextResponse.json({
    count: list.length,
    crosswalks: list,
    provenance: {
      note: "Crosswalks link our objects to external records (OCHS, NGMPP, Gyan Bharatam...) while preserving both identifiers — the federation layer. Resolve, don't duplicate.",
      api_version: "1.0",
    },
  });
}
