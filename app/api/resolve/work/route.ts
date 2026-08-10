// POST /api/resolve/work — candidate work identity for a manuscript record.
// Input: { title?, incipit?, alternateTitles?, script?, language? }
// Returns RANKED CANDIDATES with confidence + matching evidence. This is a machine
// proposal only — per NORTHSTAR: "AI proposes identity ≠ Pāṭala asserts identity."
// Only a review event creates an assertion.

import { NextRequest, NextResponse } from "next/server";
import { works } from "@/data/corpus/works";
import { manuscriptsForWork } from "@/data/corpus/manuscripts";

function norm(s: string): string {
  return (s || "").toLowerCase().replace(/[^a-z0-9]+/g, "").trim();
}

function coreTokens(s: string): string[] {
  return (s || "").toLowerCase().split(/[^a-zāīūṛḷṅñṭḍṇśṣḥ]+/).filter((t) => t.length >= 4);
}

export async function POST(req: NextRequest) {
  let body: any = {};
  try {
    body = await req.json();
  } catch {}

  const title = String(body.title ?? "").trim();
  const incipit = String(body.incipit ?? "").trim();
  if (!title && !incipit) {
    return NextResponse.json({ error: "missing_input", hint: "provide title and/or incipit" }, { status: 400 });
  }

  const candidates = [];
  for (const w of works) {
    let score = 0;
    const evidence: string[] = [];

    // alias surface: work title + any resolved OCHS manuscript titles
    const aliases = [w.title, ...(w.alternateTitles ?? [])];
    for (const m of manuscriptsForWork(w.id)) {
      if (m.title) aliases.push(m.title);
    }

    if (title) {
      const tNorm = norm(title);
      const tTokens = coreTokens(title);
      let bestAlias = 0;
      for (const a of aliases) {
        const aNorm = norm(a);
        if (aNorm === tNorm) bestAlias = Math.max(bestAlias, 1);
        else if (aNorm && tNorm && (aNorm.includes(tNorm) || tNorm.includes(aNorm))) bestAlias = Math.max(bestAlias, 0.8);
        else {
          const aTokens = coreTokens(a);
          const hits = tTokens.filter((tk) => aTokens.some((ak) => ak === tk)).length;
          bestAlias = Math.max(bestAlias, tTokens.length ? hits / tTokens.length : 0);
        }
      }
      if (bestAlias > 0) {
        score += bestAlias * 0.8;
        evidence.push(`title match (${bestAlias.toFixed(2)})`);
      }
    }

    if (incipit) {
      const iNorm = norm(incipit);
      // match against the work's manuscript incipits where available
      for (const m of manuscriptsForWork(w.id)) {
        if (m.incipit) {
          const mNorm = norm(m.incipit);
          if (iNorm.length > 20 && (mNorm.includes(iNorm.slice(0, 24)) || iNorm.slice(0, 24).includes(mNorm.slice(0, 24)))) {
            score += 0.6;
            evidence.push(`incipit match (${m.ochs_slug})`);
            break;
          }
        }
      }
    }

    if (score > 0) {
      candidates.push({ work_id: w.id, title: w.title, urn: w.urn, traditions: w.traditions, confidence: Math.min(1, score), evidence });
    }
  }

  candidates.sort((a: any, b: any) => b.confidence - a.confidence);

  return NextResponse.json({
    query: { title, incipit: incipit ? `${incipit.slice(0, 40)}…` : null },
    status: "machine_proposed",
    count: candidates.length,
    candidates: candidates.slice(0, 8),
    provenance: {
      note: "Machine proposal only. Identity is NOT asserted until a human review event accepts a candidate (northstar: AI proposes ≠ Pāṭala asserts).",
      api_version: "1.0",
    },
  });
}
