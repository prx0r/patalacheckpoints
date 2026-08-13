// GET /api/education — the education projection surface (the Learn product).
//   ?id=learn-VERTICAL-1        → one learning packet (all interactions)
//   ?work=VERTICAL-1            → the packet for that argument/synthesis
//   (default)                   → the summary of all compiled packets
//
// Serves the compiled LearningPackets (InteractionDefinition JSON) produced by the education IR
// (education_ir.py) — framework-agnostic interactions derived from the scholarly graph. The packets
// are MACHINE_PROPOSED; epistemic + pedagogical validity is the eval plane's (EDU-BENCH) job, not
// this route.

import { NextRequest, NextResponse } from "next/server";
import { readFileSync } from "fs";
import path from "path";

const PACKETS_DIR = path.join(process.cwd(), "benchmarks", "v0", "review");
const ALL = path.join(PACKETS_DIR, "ALL-ARGMAP-EDUCATION-PACKETS.json");

function readJson(p: string) {
  try {
    return JSON.parse(readFileSync(p, "utf-8"));
  } catch {
    return null;
  }
}

export async function GET(req: NextRequest) {
  const id = req.nextUrl.searchParams.get("id");
  const work = req.nextUrl.searchParams.get("work");

  // one packet by id (e.g. learn-VERTICAL-1) or by work (e.g. VERTICAL-1)
  if (id || work) {
    const want = id ?? `learn-${work}`;
    // the VERTICAL-1 packet is stored separately; others are in the ALL index
    if (want === "learn-VERTICAL-1") {
      const pkt = readJson(path.join(PACKETS_DIR, "VERTICAL-1-EDUCATION-PACKET.json"));
      if (!pkt) return NextResponse.json({ error: "no_packet", id: want }, { status: 404 });
      return NextResponse.json({
        packet: pkt,
        status_note: "MACHINE_PROPOSED — compiled from the scholarly graph; EDU-BENCH evaluates epistemic + pedagogical validity.",
      });
    }
    const index = readJson(ALL);
    const entry = index?.packets?.find((p: any) => p.object_id === work || `learn-${p.object_id}` === want);
    if (entry) return NextResponse.json({ packet: entry, status_note: "MACHINE_PROPOSED" });
    return NextResponse.json({ error: "no_packet", id: want }, { status: 404 });
  }

  // summary of all compiled packets
  const index = readJson(ALL);
  if (!index) return NextResponse.json({ error: "no_packets" }, { status: 404 });
  return NextResponse.json({
    count: index.total_argmaps,
    total_interactions: index.total_interactions,
    skills: index.skills_covered,
    misconception_families: index.misconception_families_covered,
    status_note: "Education is a projection of the scholarly graph (LearningClaim/Skill/Interaction), MACHINE_PROPOSED.",
  });
}
