// GET /api/verify/trace-dependency?ref=<passage-locator>&from=c1
// Deterministic backward walk of the derivation DAG (source ← L2 ← C1) — reports where
// (if anywhere) the chain breaks. The provenance floor for any generated claim.

import { NextRequest, NextResponse } from "next/server";
import { traceDependency } from "@/lib/verify";

export async function GET(req: NextRequest) {
  const ref = req.nextUrl.searchParams.get("ref") ?? "";
  const from = req.nextUrl.searchParams.get("from") ?? "c1";
  if (!ref) {
    return NextResponse.json({ error: "missing_ref", hint: "?ref=<locator|immutable-id>" }, { status: 400 });
  }
  return NextResponse.json(traceDependency(ref, from as any));
}
