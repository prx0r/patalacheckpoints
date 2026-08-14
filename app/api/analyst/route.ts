// GET /api/analyst?passage=<id>&label=<...>&see_also=<...>  or  ?theme=<lemma>
// The metacognitive layer (borrowed from the HXRMXS `my_thoughts`): before narrating a journey
// step, produce a MetaThought block (hypothesis / best_move / trap / predict / watch) reasoning
// about the READER's state. The graph selects the move; the analyst explains/predicts/watches;
// the LLM narrates.

import { NextRequest, NextResponse } from "next/server";
import { analystForJourney } from "@/data/corpus/analyst";

export async function GET(req: NextRequest) {
  const passage = req.nextUrl.searchParams.get("passage");
  const theme = req.nextUrl.searchParams.get("theme");
  const label = req.nextUrl.searchParams.get("label") ?? "";
  const seeAlso = req.nextUrl.searchParams.get("see_also") ?? "";

  const result = analystForJourney(passage ?? theme ?? "", { passage: passage ?? undefined, theme: theme ?? undefined, label, seeAlso });
  if (!result) return NextResponse.json({ error: "missing_param", hint: "?passage=<id>&see_also=<...> or ?theme=<lemma>" }, { status: 400 });
  return NextResponse.json(result);
}
