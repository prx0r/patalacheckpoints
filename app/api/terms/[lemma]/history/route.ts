// GET /api/terms/:lemma/history — the diachronic sense-trajectory of a lemma.
// The reference map's signature feature: a lemma does NOT have one meaning — it
// has a trajectory across traditions and periods. Seeded from the reference map
// + the dossiers. These are EVIDENCE-BACKED HYPOTHESES (the "Sense" level of
// authority), not settled facts — status reflects the source.

import { NextRequest, NextResponse } from "next/server";
import { getTrajectory } from "@/data/corpus/trajectories";
import { getTerm, getProposals } from "@/data/corpus/terms";

export async function GET(
  _req: NextRequest,
  ctx: { params: Promise<{ lemma: string }> },
) {
  const { lemma } = await ctx.params;
  const traj = getTrajectory(lemma);
  if (!traj) {
    return NextResponse.json({ error: "not_found", lemma, hint: "trajectory not yet seeded for this lemma" }, { status: 404 });
  }
  const accepted = getTerm(lemma);
  return NextResponse.json({
    lemma,
    title: traj.title,
    trajectory: traj.nodes,
    note: traj.note ?? null,
    accepted_senses: accepted ? accepted.senses : [],
    proposals: getProposals(lemma).length,
    provenance: {
      note: "The diachronic sense-trajectory: how the lemma's sense shifts across traditions/periods. Evidence-backed hypotheses (the reference map + dossiers), not settled facts. Semantic consistency is the goal, not lexical uniformity.",
      api_version: "1.0",
    },
  });
}
