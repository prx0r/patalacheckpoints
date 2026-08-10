// GET /api/manuscripts — the manuscript witness layer (OCHS metadata, resolved).
// Filter by ?work_id= to get the witnesses of one of our works, or ?q= to search
// title/NAK/NGMPP. Provenance: custodian OCHS, CC BY-NC-SA 4.0, source_url per record.

import { NextRequest, NextResponse } from "next/server";
import { getManuscripts, manuscriptsForWork, workForManuscript } from "@/data/corpus/manuscripts";

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const workId = searchParams.get("work_id");
  const q = searchParams.get("q");

  let list = getManuscripts();
  if (workId) {
    list = manuscriptsForWork(workId);
  } else if (q) {
    const needle = q.toLowerCase();
    list = list.filter(
      (m) =>
        (m.title ?? "").toLowerCase().includes(needle) ||
        (m.catalogueIds ?? "").toLowerCase().includes(needle) ||
        (m.script ?? "").toLowerCase().includes(needle),
    );
  }

  const out = list.map((m) => ({ ...m, works: workForManuscript(m.ochs_slug), raw: undefined }));
  return NextResponse.json({
    count: out.length,
    query: { work_id: workId ?? null, q: q ?? null },
    manuscripts: out,
    provenance: {
      note: "Manuscript witness metadata from OCHS (custodian), CC BY-NC-SA 4.0; each record links to its authoritative source. Resolved to our works where curated.",
      api_version: "1.0",
    },
  });
}
