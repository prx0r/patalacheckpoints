// GET /api — the open API index (discoverability). Lists the surface + the northstar
// framing, so any agent/consumer can see what Pāṭala serves without digging.

import { NextRequest, NextResponse } from "next/server";

export async function GET(_req: NextRequest) {
  return NextResponse.json({
    name: "Pāṭala",
    tagline: "The authority, provenance, relationship, expert-validation and workflow layer for tantric textual heritage.",
    api_version: "1.0",
    endpoints: {
      texts: ["GET /api/texts", "GET /api/texts/:id", "GET /api/texts/:id/translations"],
      works: ["GET /api/works", "GET /api/works/:id", "GET /api/works/:id/manuscripts"],
      relations: ["GET /api/relations/:work_id"],
      passages: ["GET /api/passages/:id", "GET /api/search/passages", "GET /api/context/passages/:id", "GET /api/passages/:id/translation"],
      decisions: ["GET /api/decisions/:id"],
      terms: ["GET /api/terms", "GET /api/terms/:lemma/senses", "GET /api/terms/:lemma/occurrences", "GET /api/terms/:lemma/history", "GET /api/term-proposals"],
      manuscripts: ["GET /api/manuscripts", "GET /api/works/:id/manuscripts"],
      resolve: ["POST /api/resolve/work"],
      stats: ["GET /api/stats"],
    },
    principles: {
      provenance: "every record carries a tier / statusChecked / custodian",
      resolve_dont_duplicate: "we connect sources and preserve their custodianship",
      machine_proposal_neq_assertion: "only human review creates assertions",
      open_commons: "open scholarly infrastructure where rights permit",
    },
  });
}
