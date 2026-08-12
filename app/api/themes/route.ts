// GET /api/themes — deterministic theme structure over the IPVV C1s (Phase 0c).
//   ?work=isvarapratyabhijnavivrtivimarsini  → all themes (default)
//   ?passage=pt:passage:ipvv:...             → themes containing that passage
//   ?id=pt:theme:vimarśa                     → one theme
//
// Themes are MACHINE_PROPOSED (shared technical lemmas across C1s). They are the substrate
// the theme-clustering builds on; human adjudication promotes them to established.

import { NextRequest, NextResponse } from "next/server";
import { deriveThemes, themesFor, themeById } from "@/data/corpus/themes";

export async function GET(req: NextRequest) {
  const passage = req.nextUrl.searchParams.get("passage");
  const id = req.nextUrl.searchParams.get("id");

  if (id) {
    const theme = themeById(id);
    if (!theme) return NextResponse.json({ error: "no_theme", id }, { status: 404 });
    return NextResponse.json({ theme });
  }
  if (passage) {
    return NextResponse.json({ passage, themes: themesFor(passage) });
  }
  const themes = deriveThemes();
  return NextResponse.json({
    count: themes.length,
    status_note: "MACHINE_PROPOSED — shared technical lemmas across C1s; human adjudication required before treating as established.",
    themes,
  });
}
