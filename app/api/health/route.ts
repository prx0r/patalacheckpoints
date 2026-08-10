// GET /api/health — operational health, separate from /api/stats (which is research
// metadata). Answers: is the service up, is the dataset loaded, what version.
// No internal secrets. Per docs/apitest.md §19.

import { NextRequest, NextResponse } from "next/server";
import { works } from "@/data/corpus/works";
import { getPassages } from "@/data/corpus/passages";

export async function GET(_req: NextRequest) {
  const passages = getPassages();
  return NextResponse.json({
    status: "ok",
    api_version: "1.0",
    dataset_revision: "2026-08-10",
    dataset: {
      works: works.length,
      passages: passages.length,
    },
    generated_at: new Date().toISOString(),
  });
}
