// GET /api/terms/:lemma/history — the diachronic sense-trajectory of a lemma.
//
// A trajectory is a projection over CURATED historical-sense assertions (each a
// reviewable, addressable node referencing an accepted/proposed sense_id with
// evidence links). It is NOT mechanically derived from corpus occurrences.
//
// The endpoint returns per-node: id, sense_id/proposed_sense_id, scope, claim,
// evidence_links, origin, status, certainty — plus response-level warnings so an
// agent knows the epistemic state (e.g. proposed nodes, unresolved evidence).

import { NextRequest, NextResponse } from "next/server";
import { getTrajectory, TrajectoryNode } from "@/data/corpus/trajectories";
import { getTerm, getProposals } from "@/data/corpus/terms";
import { getPassage } from "@/data/corpus/passages";

export async function GET(
  _req: NextRequest,
  ctx: { params: Promise<{ lemma: string }> },
) {
  const { lemma } = await ctx.params;
  const traj = getTrajectory(lemma);
  if (!traj) {
    return NextResponse.json({ error: "not_found", lemma, hint: "trajectory not yet seeded for this lemma" }, { status: 404 });
  }

  // per-node checks
  const warnings: string[] = [];
  const nodes = traj.nodes.map((n: TrajectoryNode) => {
    const sense_ok = n.sense_id ? Boolean(getTerm(n.lemma)?.senses.find((s) => s.id === n.sense_id)) : false;
    const prop_ok = n.proposed_sense_id ? Boolean(getProposals(n.lemma)) : false;
    if (n.sense_id && !sense_ok) warnings.push(`${n.id}: sense_id ${n.sense_id} not found in the accepted ledger`);
    if (!n.sense_id && !n.proposed_sense_id) warnings.push(`${n.id}: has neither an accepted sense_id nor a proposed_sense_id`);
    if (!n.evidence_links.length && n.status !== "proposed") warnings.push(`${n.id}: no evidence links`);
    // resolve passage evidence where it is a passage id
    const resolved_evidence = n.evidence_links.map((e) => {
      if (e.type === "passage" && e.target_id.startsWith("tantra:text:")) {
        return { ...e, passage_exists: Boolean(getPassage(e.target_id)) };
      }
      return { ...e };
    });
    return {
      id: n.id,
      lemma: n.lemma,
      scope: {
        period: { label: n.period_label, date_range: n.date_range ?? null },
        traditions: n.tradition_ids,
        tradition_label: n.tradition_label,
      },
      sense_id: n.sense_id ?? null,
      proposed_sense_id: n.proposed_sense_id ?? null,
      claim: n.claim,
      evidence_links: resolved_evidence,
      origin: n.origin,
      status: n.status,
      certainty: n.certainty ?? null,
      translation_policy: n.translation_policy ?? null,
    };
  });

  const accepted = getTerm(lemma);
  return NextResponse.json({
    lemma,
    title: traj.title,
    trajectory: nodes,
    note: traj.note ?? null,
    accepted_senses: accepted ? accepted.senses : [],
    proposals: getProposals(lemma).length,
    warnings,
    provenance: {
      note: "The diachronic sense-trajectory: a projection over curated historical-sense assertions. Each node references an accepted/proposed sense with evidence links; origin/status/certainty are separate. NOT mechanically derived from corpus occurrences. Semantic consistency is the goal, not lexical uniformity.",
      api_version: "1.0",
    },
  });
}
