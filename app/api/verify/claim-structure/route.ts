// GET /api/verify/claim-structure?ref=<passage-locator>&claim=<optional>
// Deterministic claim-structure verification: does the passage resolve and carry source + L2 + C1?
// The structural floor below any semantic claim verification.

import { NextRequest, NextResponse } from "next/server";
import { verifyClaimStructure } from "@/lib/verify";

export async function GET(req: NextRequest) {
  const ref = req.nextUrl.searchParams.get("ref") ?? "";
  const claim = req.nextUrl.searchParams.get("claim") ?? "";
  if (!ref) {
    return NextResponse.json({ error: "missing_ref", hint: "?ref=<locator|immutable-id>" }, { status: 400 });
  }
  return NextResponse.json(verifyClaimStructure(claim, ref));
}
