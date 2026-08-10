// GET /api/relations/:work_id — typed + confidence + evidence edges touching a work.
// Lets the passage/MCP layer rank context: direct textual relative > same tradition.

import { NextRequest, NextResponse } from "next/server";
import { relationsFor } from "@/data/corpus/relations";

export async function GET(
  _req: NextRequest,
  ctx: { params: Promise<{ work_id: string }> },
) {
  const { work_id } = await ctx.params;
  const id = work_id.startsWith("tantra:text:") ? work_id.slice("tantra:text:".length) : work_id;
  const rels = relationsFor(id);
  return NextResponse.json({ work_id: id, count: rels.length, relations: rels });
}
