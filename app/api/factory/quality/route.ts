// GET /api/factory/quality — the live per-work translation-ready signal.
//   ?work=<work_id>   → one work's quality fingerprint
//   (no params)       → all works (reads the cached signal), optional ?priority=HIGH
//
// Bridges the Python factory (pipeline/source_ready.py — the tested CLEAN/READY/PRIORITY signal)
// into the site API. The full signal is computed by source_ready.py --write-cache into
// data/corpus/source-ready.json (refreshed when the factory/intake changes); this route reads
// that cache (fast). For a single unknown work it shells Python as a fallback.
//
// Returns per work:
//   clean     — on-disk Sanskrit usable (script density, size)
//   ready     — in ledger as RAW_SANSKRIT + has committed SOURCE objects
//   priority  — copyright-aware translation value (HIGH/MEDIUM/LOW)
//   english   — atlas translation coverage
//   next_action — ledger's next valid transition

import { promises as fs } from "fs";
import path from "path";
import { NextRequest, NextResponse } from "next/server";
import { execFile } from "child_process";
import { promisify } from "util";

const exec = promisify(execFile);
const ROOT = process.cwd();
const CACHE = path.join(ROOT, "data/corpus/source-ready.json");

async function readCache(): Promise<any[]> {
  try {
    return JSON.parse(await fs.readFile(CACHE, "utf-8"));
  } catch {
    return [];
  }
}

async function shellWork(work: string): Promise<any[]> {
  try {
    const { stdout } = await exec("python3", ["pipeline/source_ready.py", "--work", work, "--json"], { cwd: ROOT, timeout: 15000 });
    return JSON.parse(stdout);
  } catch {
    return [];
  }
}

export async function GET(req: NextRequest) {
  const work = req.nextUrl.searchParams.get("work");
  const priority = req.nextUrl.searchParams.get("priority");

  const cache = await readCache();
  let recs = cache;

  if (work) {
    let rec = recs.find((r) => r.work === work);
    if (!rec) {
      // not in cache — shell Python for the single work
      const live = await shellWork(work);
      rec = live[0] ?? null;
    }
    if (!rec) {
      return NextResponse.json({ error: "no_quality_signal", work }, { status: 404 });
    }
    return NextResponse.json({
      work: rec.work,
      quality: {
        clean: rec.clean,
        clean_reason: rec.reason ?? null,
        source: {
          on_disk: rec.on_disk,
          sanskrit_chars: rec.sanskrit_chars ?? 0,
          iast: rec.iast ?? 0,
          devanagari: rec.devanagari ?? 0,
          size: rec.size ?? 0,
          source_ref: rec.source_ref ?? null,
        },
        ready: {
          in_ledger: rec.in_ledger,
          in_queue: rec.has_source_objects,
          next_action: rec.next_action,
          t1_committed: rec.t1_committed ?? 0,
        },
        translation: {
          english: rec.english ?? "unknown",
          has_translation_urls: rec.has_translation_urls ?? false,
          pd_hint: rec.pd_hint ?? false,
          copyright_hint: rec.copyright_hint ?? false,
        },
        priority: rec.priority ?? "LOW",
        priority_reason: rec.why ?? null,
      },
      provenance: {
        note: "Live factory signal via pipeline/source_ready.py. clean = on-disk Sanskrit usable; ready = in ledger + source objects; priority = copyright-aware translation value.",
        api_version: "1.0",
      },
    });
  }

  let filtered = recs;
  if (priority) {
    const p = priority.toUpperCase();
    filtered = recs.filter((r) => (r.priority ?? "").toUpperCase() === p);
  }
  return NextResponse.json({
    count: filtered.length,
    total: recs.length,
    priority_filter: priority ?? null,
    summary: {
      clean: recs.filter((r) => r.clean).length,
      ready: recs.filter((r) => r.in_ledger && r.has_source_objects).length,
      high: recs.filter((r) => r.priority === "HIGH").length,
      medium: recs.filter((r) => r.priority === "MEDIUM").length,
      low: recs.filter((r) => r.priority === "LOW").length,
    },
    works: filtered.map((r) => ({
      work: r.work,
      clean: r.clean,
      ready: r.in_ledger && r.has_source_objects,
      in_queue: r.has_source_objects,
      sanskrit_chars: r.sanskrit_chars ?? 0,
      english: r.english ?? "unknown",
      priority: r.priority ?? "LOW",
      priority_reason: r.why ?? null,
    })),
  });
}
