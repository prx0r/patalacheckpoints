// GET /api/works — the corpus manifest (work registry). Filter by tradition,
// translation status, verified. Returns the works at full metadata depth.

import { NextRequest, NextResponse } from "next/server";
import { works } from "@/data/corpus/works";
import { workingTranslationCounts } from "@/data/corpus/passages";
import { workManuscriptCounts } from "@/data/corpus/manuscripts";

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const tradition = searchParams.get("tradition");
  const status = searchParams.get("status");
  const verified = searchParams.get("verified");

  const counts = workingTranslationCounts();
  const msCounts = workManuscriptCounts();

  const filtered = works.filter((w) => {
    if (tradition && !w.traditions.some((t) => t.label === tradition || t.id === tradition)) return false;
    if (status && w.translation_status !== status) return false;
    if (verified && String(w.verified) !== verified) return false;
    return true;
  }).map((w) => ({ ...w, working_translations: counts[w.id] ?? 0, manuscripts: msCounts[w.id] ?? 0 }));

  return NextResponse.json({
    count: filtered.length,
    query: { tradition: tradition ?? null, status: status ?? null, verified: verified ?? null },
    works: filtered,
    provenance: {
      note: "The work registry. traditions carry explicit certainty; date ranges carry certainty; nothing is forced into a rigid taxonomy. working_translations = count of our T1 passages served.",
      api_version: "1.0",
    },
  });
}
