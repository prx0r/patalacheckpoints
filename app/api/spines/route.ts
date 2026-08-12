// GET /api/spines — the canonical reading spine per school, tied to the bibliography.
//   ?tradition=pratyabhijna  → the recognition spine (IPK → Vivṛti → IPV → IPVV → Hṛdaya ...)
//   ?work=isvarapratyabhijnavivrtivimarsini → the spine containing that work + its bibliography
//
// Lets an agent research the "related N works" of a school as ONE navigable object,
// each step pointing to its bibliography record (sources, translations, scholarship).

import { NextRequest, NextResponse } from "next/server";
import { allSpines, spineFor, spineForWork } from "@/data/corpus/canonical-spines";
import { works } from "@/data/corpus/works";

export async function GET(req: NextRequest) {
  const tradition = req.nextUrl.searchParams.get("tradition");
  const work = req.nextUrl.searchParams.get("work");

  const withBib = (spine: { tradition: string; label: string; summary: string; steps: any[] }) => ({
    ...spine,
    steps: spine.steps.map((st) => {
      const w = works.find((x) => x.id === st.work_id);
      return { ...st, work: w ? { id: w.id, title: w.title, traditions: w.traditions, research_roles: w.research_roles, translation_status: w.translation_status } : null };
    }),
  });

  if (work) {
    const spine = spineForWork(work);
    if (!spine) return NextResponse.json({ error: "no_spine", work, hint: "try isvarapratyabhijnavivrtivimarsini" }, { status: 404 });
    return NextResponse.json({ work, spine: withBib(spine) });
  }

  if (tradition) {
    const spine = spineFor(tradition);
    if (!spine) return NextResponse.json({ error: "no_spine", tradition, available: allSpines().map((s) => s.tradition) }, { status: 404 });
    return NextResponse.json({ spine: withBib(spine) });
  }

  return NextResponse.json({ count: allSpines().length, spines: allSpines().map(withBib) });
}
