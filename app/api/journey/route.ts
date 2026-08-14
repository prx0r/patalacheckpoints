// GET /api/journey?passage=<id>&label=<...>&see_also=<...>  or  ?theme=<lemma>
// The graph-owned guided journey: given an entry (passage or concept), compose a sequence of
// stops (passage → C1 see-also → themes → related works) from the graph's OWN structure.
// The LLM narrates the chosen path; the graph owns the move.

import { NextRequest, NextResponse } from "next/server";
import { journeyFromPassage, journeyFromTheme } from "@/data/corpus/journey";

export async function GET(req: NextRequest) {
  const passage = req.nextUrl.searchParams.get("passage");
  const label = req.nextUrl.searchParams.get("label") ?? passage ?? "";
  const seeAlso = req.nextUrl.searchParams.get("see_also") ?? "";
  const theme = req.nextUrl.searchParams.get("theme");

  if (theme) return NextResponse.json(journeyFromTheme(theme));
  if (passage) return NextResponse.json(journeyFromPassage(passage, label, seeAlso));
  return NextResponse.json({ error: "missing_param", hint: "?passage=<id>&see_also=<...> or ?theme=<lemma>" }, { status: 400 });
}
