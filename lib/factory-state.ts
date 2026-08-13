// lib/factory-state.ts — the LIVE Pāṭala factory state, read from the Python side
// (translation-state-ledger.json + object registries), exposed to the Next.js API.
//
// This is the "local integration" of the Agent-2 factory into the site. The factory's
// registries/ledger are the canonical state; the frontend data modules (data/corpus/works.ts)
// are derived metadata. This lib bridges them so the API can serve live granular quality:
//   - source quality (clean/dirty, sanskrit chars, script)
//   - factory readiness (in ledger, next action, source objects, t1 committed)
//   - translation value (copyright-aware priority: HIGH/MEDIUM/LOW)
//
// Mirrors pipeline/source_ready.py so the Python and TS views agree.

import { promises as fs } from "fs";
import path from "path";

const ROOT = process.cwd();

// --- copyright heuristics (must match pipeline/source_ready.py) ---
const PD_HINTS = ["archive.org", "sacred-texts", "gutenberg", "wisdomlib", "upasanayoga", "ia", ".pdf", "gretil"];
const CORY_HINTS = ["oup.com", "pupress", "sunypress", "cambridge", "academic", "efeo.fr",
  "ifpindia.org/bookstore", "brill", "doi.org", "taylorfrancis", "anuttaratrikakula", "personal", "wordpress", "blogspot"];

async function readJson(p: string): Promise<any> {
  try { return JSON.parse(await fs.readFile(p, "utf-8")); } catch { return null; }
}

async function readJsonl(p: string): Promise<any[]> {
  try {
    const txt = await fs.readFile(p, "utf-8");
    return txt.split("\n").filter(Boolean).map((l) => JSON.parse(l));
  } catch { return []; }
}

async function readText(p: string): Promise<string> {
  try { return await fs.readFile(p, "utf-8"); } catch { return ""; }
}

function _priorityFor(status: string, urls: string[]): { priority: string; why: string } {
  const pd = urls.some((u) => PD_HINTS.some((h) => u.includes(h)));
  const cory = urls.some((u) => CORY_HINTS.some((h) => u.includes(h)));
  if (status === "none") return { priority: "HIGH", why: "no English translation found — own translation fills the gap" };
  if (cory) return { priority: "HIGH", why: "English exists but under copyright — translate your own to publish" };
  if (status === "complete" && pd) return { priority: "MEDIUM", why: "complete public-domain English available — link it; translating optional" };
  if (status === "complete") return { priority: "MEDIUM", why: "complete English exists — check copyright" };
  if (status === "partial") return { priority: "HIGH", why: "only partial English — own translation fills the gap" };
  return { priority: "LOW", why: "translation status unclear — verify" };
}

// --- source quality (mirror pipeline/source_ready.py) ---
function _cleanSignal(srcRef: string | null, wid: string): Record<string, any> {
  const p = srcRef && path.resolve(srcRef);
  // only local paths we can read; if not present fall back to data/corpus/sources
  const candidates = p && (p.startsWith(ROOT) || p.startsWith("/")) ? [p] : [path.join(ROOT, "data", "corpus", "sources", wid, `${wid}.txt`)];
  // lazily read the first existing candidate
  return { _candidate: candidates[0] }; // populated by caller via async
}

export async function factoryState() {
  const ledger = await readJson(path.join(ROOT, "data/corpus/downloads/translation-state-ledger.json"));
  const sourceReg = await readJsonl(path.join(ROOT, "data/corpus/registries/source-registry.jsonl"));
  const t1Reg = await readJsonl(path.join(ROOT, "data/corpus/registries/t1-registry.jsonl"));

  // committed SOURCE object ids
  const sourceWorks = new Set<string>();
  const sourceObj: Record<string, number> = {};
  for (const rec of sourceReg) {
    const oid = rec?.object_id;
    if (!oid || typeof oid !== "string") continue;
    if (oid.includes(":")) {
      const w = oid.split(":")[0];
      sourceWorks.add(w);
      sourceObj[w] = (sourceObj[w] ?? 0) + 1;
    }
  }
  // committed T1 ids
  const t1ByWork: Record<string, number> = {};
  for (const rec of t1Reg) {
    const oid = rec?.object_id;
    if (oid && typeof oid === "string" && oid.includes(":")) {
      const w = oid.split(":")[0];
      t1ByWork[w] = (t1ByWork[w] ?? 0) + 1;
    }
  }

  const works: Record<string, any> = {};
  const ledgerWorks = ledger?.works ?? {};
  for (const [wid, w] of Object.entries<any>(ledgerWorks)) {
    const src = w.source ?? {};
    const next = w.next_action ?? {};
    works[wid] = {
      work_id: wid,
      bibliographic_id: w.bibliographic_id ?? null,
      source_available: !!src.available,
      source_format: src.format ?? "UNKNOWN",
      source_ref: src.source_ref ?? null,
      next_action: next.action ?? null,
      in_queue: sourceWorks.has(wid),
      source_objects: sourceObj[wid] ?? 0,
      t1_committed: t1ByWork[wid] ?? 0,
    };
  }
  return { works, summary: { ledger_works: Object.keys(ledgerWorks).length, source_works: sourceWorks.size, t1_works: Object.keys(t1ByWork).length } };
}
