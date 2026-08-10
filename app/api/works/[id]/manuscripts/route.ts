// GET /api/works/:id/manuscripts — the OCHS manuscript witnesses of one work.

import { NextRequest, NextResponse } from "next/server";
import { manuscriptsForWork } from "@/data/corpus/manuscripts";

export async function GET(
  _req: NextRequest,
  ctx: { params: Promise<{ id: string }> },
) {
  const { id } = await ctx.params;
  const workId = id.startsWith("tantra:text:") ? id.slice("tantra:text:".length) : id;
  const ms = manuscriptsForWork(workId);
  return NextResponse.json({
    work_id: workId,
    count: ms.length,
    provenance: {
      note: "OCHS manuscript witnesses (custodian OCHS, CC BY-NC-SA 4.0). These are physical witnesses of the work; link out to OCHS for images and the authoritative record.",
    },
    manuscripts: ms,
  });
}
