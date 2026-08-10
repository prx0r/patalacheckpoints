// GET /api/passages/:id — one verse-anchored passage by stable ID.
// Accepts "tantra:text:kramasadbhava:1.2" or a bare "kramasadbhava:1.2".

import { NextRequest, NextResponse } from "next/server";
import { getPassage } from "@/data/corpus/passages";

export async function GET(
  _req: NextRequest,
  ctx: { params: Promise<{ id: string }> },
) {
  const { id: raw } = await ctx.params;
  const id = raw.startsWith("tantra:text:") ? raw : `tantra:text:${raw}`;
  const passage = getPassage(id);
  if (!passage) {
    return NextResponse.json({ error: "not_found", id }, { status: 404 });
  }
  return NextResponse.json({ data: passage, provenance: { api_version: "1.0" } });
}
