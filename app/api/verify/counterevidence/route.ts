// GET /api/verify/counterevidence?ref=<passage-locator>
// Deterministic counterevidence: surfaces the curated contradicts/qualifies edges (the
// explicit qualification/contrast markers in the passage's C1). Honest about what is NOT
// yet recorded — never invents counterevidence. The ML master's discovery service will
// populate the frontier adversarial-retrieval set above this floor.

import { NextRequest, NextResponse } from "next/server";
import { findCounterevidence } from "@/lib/verify";

export async function GET(req: NextRequest) {
  const ref = req.nextUrl.searchParams.get("ref") ?? "";
  if (!ref) {
    return NextResponse.json({ error: "missing_ref", hint: "?ref=<locator|immutable-id>" }, { status: 400 });
  }
  return NextResponse.json(findCounterevidence(ref));
}
