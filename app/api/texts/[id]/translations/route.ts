// GET /api/texts/:id/translations — our working (T1) translations for a work,
// as verse-anchored passages with the close translation + flags.
// Working translations are provisional (not peer reviewed); the provenance field
// says so. This is comparison/calibration material, never to be copied verbatim.

import { NextRequest, NextResponse } from "next/server";
import { workingTranslations } from "@/data/corpus/passages";

export async function GET(
  _req: NextRequest,
  ctx: { params: Promise<{ id: string }> },
) {
  const { id } = await ctx.params;
  const workId = id.startsWith("tantra:text:") ? id.slice("tantra:text:".length) : id;
  const passages = workingTranslations(workId);
  return NextResponse.json({
    work_id: workId,
    count: passages.length,
    provenance: {
      note: "Our working translations (T1), derived from the translation corpus markdown. NOT peer reviewed; provisional. Use for comparison and calibration, never to be copied verbatim.",
      stage: "T1",
    },
    translations: passages,
  });
}
