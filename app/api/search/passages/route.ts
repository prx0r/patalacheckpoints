// GET /api/search/passages?q=... — substring search over the passage corpus.
// Returns matching passages (sanskrit + id). Coarse; not a full-text engine yet.

import { NextRequest, NextResponse } from "next/server";
import { searchPassages } from "@/data/corpus/passages";

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const q = searchParams.get("q") ?? "";
  const work = searchParams.get("work_id");
  const limit = parseInt(searchParams.get("limit") ?? "50", 10);

  if (!q.trim()) {
    return NextResponse.json({ error: "missing_query", hint: "?q=śakti or ?q=kramasadbhava:1" }, { status: 400 });
  }
  let hits = searchPassages(q.trim());
  if (work) hits = hits.filter((p) => p.work_id === work);
  const truncated = hits.length > limit;
  return NextResponse.json({
    query: q,
    work_id: work ?? null,
    count: hits.length,
    truncated,
    passages: hits.slice(0, limit),
  });
}
