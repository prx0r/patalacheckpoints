import { NextRequest, NextResponse } from "next/server";
import { audited, seed } from "@/data/atlas";
import { BibliographyRecord } from "@/data/atlas/bibliographyTypes";

type Record = BibliographyRecord & { urn: string };

const ALL: Record[] = [
  ...audited.map((r) => ({ ...r, urn: `tantra:text:${r.id}` })),
  ...seed.map((r) => ({ ...r, urn: `tantra:text:${r.id}` })),
];

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const tradition = searchParams.get("tradition");
  const status = searchParams.get("status"); // complete | partial | none
  const verified = searchParams.get("verified"); // true | false
  const includeSeed = searchParams.get("includeSeed") !== "false"; // default true

  const filtered = ALL.filter((r) => {
    if (tradition && !r.traditions.includes(tradition)) return false;
    if (status && r.translationStatus !== status) return false;
    if (verified && String(r.verified) !== verified) return false;
    if (!includeSeed && !r.verified) return false;
    return true;
  });

  return NextResponse.json({
    count: filtered.length,
    query: { tradition: tradition ?? null, status: status ?? null, verified: verified ?? null, includeSeed },
    texts: filtered,
    provenance: {
      note: "Each record carries a stable urn + statusChecked (evidence-date); each resource carries a provenance tier (A critical · B text-repo · C scholarly-discovery · D niche · E mirror). 'No complete English translation located' is the public phrasing, not 'Untranslated'.",
      api_version: "1.0",
    },
  });
}
