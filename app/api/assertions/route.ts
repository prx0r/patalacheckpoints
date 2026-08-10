// GET /api/assertions — contested scholarly claims as first-class objects
// (subject/predicate/value + status + certainty + evidence + review events).
// Filter by ?subject=pt:work:kubjikamata. Per nextdev: a scholar could say
// "I disagree" → model it as an assertion, not a bare field.

import { NextRequest, NextResponse } from "next/server";
import { getAssertions, getReviews } from "@/data/corpus/primitives";

export async function GET(req: NextRequest) {
  const subject = req.nextUrl.searchParams.get("subject");
  const list = getAssertions(subject ?? undefined);
  const withReviews = list.map((a) => ({ ...a, reviews: getReviews(a.id) }));
  return NextResponse.json({
    count: withReviews.length,
    assertions: withReviews,
    provenance: {
      note: "Assertions are reviewable claims, not bare fields. status + certainty + origin + evidence + review_events make disagreement representable without corrupting the graph.",
      api_version: "1.0",
    },
  });
}
