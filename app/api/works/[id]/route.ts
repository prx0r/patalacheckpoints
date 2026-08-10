// GET /api/works/:id — one work's registry entry (accepts id or urn).

import { NextRequest, NextResponse } from "next/server";
import { works } from "@/data/corpus/works";

export async function GET(
  _req: NextRequest,
  ctx: { params: Promise<{ id: string }> },
) {
  const { id: raw } = await ctx.params;
  const id = raw.startsWith("tantra:text:") ? raw.slice("tantra:text:".length) : raw;
  const work = works.find((w) => w.id === id);
  if (!work) {
    return NextResponse.json({ error: "not_found", id }, { status: 404 });
  }
  return NextResponse.json({ data: work, provenance: { api_version: "1.0" } });
}
