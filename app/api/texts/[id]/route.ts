import { NextRequest, NextResponse } from "next/server";
import { audited, seed } from "@/data/atlas";
import { BibliographyRecord } from "@/data/atlas/bibliographyTypes";

type Record = BibliographyRecord & { urn: string };

const ALL: Record[] = [
  ...audited.map((r) => ({ ...r, urn: `tantra:text:${r.id}` })),
  ...seed.map((r) => ({ ...r, urn: `tantra:text:${r.id}` })),
];

export async function GET(
  _req: NextRequest,
  ctx: { params: Promise<{ id: string }> },
) {
  const { id: raw } = await ctx.params;
  // Accept either the stable id (kubjikamata) or the urn (tantra:text:kubjikamata).
  const id = raw.startsWith("tantra:text:") ? raw.slice("tantra:text:".length) : raw;
  const record = ALL.find((r) => r.id === id);
  if (!record) {
    const hint = ALL.find((r) => r.id.includes(id) || id.includes(r.id))?.id;
    return NextResponse.json({ error: "not_found", id, hint: hint ? `did you mean /api/texts/${hint}?` : undefined }, { status: 404 });
  }
  return NextResponse.json({
    data: record,
    provenance: {
      note: "Full bibliography record; every resource carries a provenance tier; statusChecked is the evidence-date.",
      api_version: "1.0",
    },
  });
}
