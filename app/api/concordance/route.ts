// GET /api/concordance — raw-corpus word tracking via scripts/concordance.py.
// Searches the RAW tantric e-text corpus (Muktabodha + local GRETIL, ~500 texts),
// NOT our translations (anti-echo guard built into concordance.py). This is the
// surface-level occurrence layer (normalized substring); a full lemma index is later.
// Runs concordance.py as a subprocess (cached index makes it fast after first build).

import { NextRequest, NextResponse } from "next/server";
import { execFile } from "child_process";
import { promisify } from "util";

const execFileP = promisify(execFile);

const SANSKRITREE = process.env.TANTRA_CORPUS_ROOT ?? "/mnt/HC_Volume_106427611/sanskritree";
const CONCORDANCE = `${SANSKRITREE}/scripts/concordance.py`;

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const q = searchParams.get("q") ?? "";
  const texts = searchParams.get("texts") ?? undefined;
  const context = Math.min(8, parseInt(searchParams.get("context") ?? "1", 10));
  const max = Math.min(50, parseInt(searchParams.get("max") ?? "10", 10));

  if (!q.trim()) {
    return NextResponse.json({ error: "missing_query", hint: "?q=khecarī" }, { status: 400 });
  }
  const terms = q.trim().split(/\s+/);

  const args = [...terms, "--json", "--context", String(context), "--max", String(max)];
  if (texts) args.push("--texts", texts);

  try {
    const { stdout } = await execFileP("python3", [CONCORDANCE, ...args], { timeout: 60000 });
    const data = JSON.parse(stdout);
    return NextResponse.json({
      query: { terms, texts: texts ?? null, context, max },
      ...data,
      provenance: {
        note: "Raw-corpus surface occurrences (concordance.py). Normalized substring, not lemmatized; never our translations. Read-only, no interpretation.",
        api_version: "1.0",
      },
    });
  } catch (e: any) {
    return NextResponse.json({ error: "concordance_failed", detail: String(e?.message ?? e) }, { status: 500 });
  }
}
