// GET /api/hub?work=<work_id> — the source-centric hub: every output a primary source has spawned.
//   ?work=isvarapratyabhijnavivrtivimarsini  → translations, essays, logical arguments, pushing, learning
//   ?work=...&kind=essay                     → only that kind
//
// The organizing primitive: a primary source is a HUB, not a file. This ties the bibliography
// (what exists) + the passages (the reading) to every derived output (PUSHING enquiry, essays,
// formal logical arguments, learning) — all on the same passage IDs, agnostic across works.

import { NextRequest, NextResponse } from "next/server";
import { hubFor, outputsFor, allHubs } from "@/data/corpus/hub";
import { works } from "@/data/corpus/works";

export async function GET(req: NextRequest) {
  const work = req.nextUrl.searchParams.get("work");
  const kind = req.nextUrl.searchParams.get("kind");

  if (work) {
    const hub = hubFor(work);
    const w = works.find((x) => x.id === work);
    if (!hub) {
      return NextResponse.json({ error: "no_hub", work, hint: "seed hubs: isvarapratyabhijnavivrtivimarsini, tantraloka" }, { status: 404 });
    }
    return NextResponse.json({
      work: w ? { id: w.id, title: w.title } : null,
      label: hub.label,
      outputs: kind ? outputsFor(work, kind as any) : hub.outputs,
      output_kinds: ["essay", "logical_argument", "pushing", "learning"],
    });
  }
  return NextResponse.json({ count: allHubs().length, hubs: allHubs() });
}
