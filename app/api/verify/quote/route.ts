// GET /api/verify/quote?q=<quote>&ref=<passage-locator>
// Deterministic verbatim-quote verification against the passage's source (Sanskrit) or L2.
// Returns an explicit verdict — never silent fallback.

import { NextRequest, NextResponse } from "next/server";
import { verifyQuote } from "@/lib/verify";

export async function GET(req: NextRequest) {
  const q = req.nextUrl.searchParams.get("q") ?? "";
  const ref = req.nextUrl.searchParams.get("ref") ?? "";
  if (!q || !ref) {
    return NextResponse.json({ error: "missing_params", hint: "?q=<quote>&ref=<locator|immutable-id>" }, { status: 400 });
  }
  return NextResponse.json(verifyQuote(q, ref));
}
