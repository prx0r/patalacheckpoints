// The published-translation registry — serves the phrase-click API.
//
// Lightweight by design: this file holds metadata/indexes only. The IPVV passages
// live as LAZY JSON assets in data/published/ipvv/ (index.json + one file per
// passage), loaded server-side on demand — NOT bundled into the client (~90MB).
//
// The invariant: the READER and the RESOLVER consume the SAME canonical published
// object. getPublishedTranslation(id) is the single loader for both.
//
// For the legacy hand-authored units (Kramasadbhāva 1.8, IPVV 1.5.11) the objects
// are imported directly (small). For the IPVV corpus we load lazily from disk.

import type { PublishedTranslation, TranslationDecision, EvidenceItem } from "./translation";
import { published18 } from "./units/kramasadbhava-1.8-published";
import { kramasadbhava_1_25 } from "./units/kramasadbhava-1-25-generated";
import { published1511 } from "./units/isvarapratyabhijnavivrtivimarsini-1.5.11-published";

// server-only lazy load of the IPVV corpus store
import { readFileSync, readdirSync, existsSync } from "fs";
import path from "path";

const IPVV_DIR = path.join(process.cwd(), "data", "published", "ipvv");

// ── in-memory: the small hand-authored units (bundled) ─────────────────────
const PUBLISHED: Record<string, PublishedTranslation> = {
  "pt:passage:isvarapratyabhijnavivrtivimarsini:1.5.11": published1511,
  "tantra:text:isvarapratyabhijnavivrtivimarsini:1.5.11": published1511,
  "pt:passage:kramasadbhava:1.8": published18,
  "tantra:text:kramasadbhava:1.8": published18,
  ...Object.fromEntries(
    Object.entries(kramasadbhava_1_25).filter(([pid]) => !pid.endsWith(":1.8"))
  ),
};
for (const [pid, p] of Object.entries(kramasadbhava_1_25)) {
  if (pid.endsWith(":1.8")) continue;
  PUBLISHED[pid.replace("pt:passage:", "tantra:text:")] = p;
}

// ── lazy IPVV store index (structural only) ────────────────────────────────
interface IndexEntry {
  id: string;
  immutable_id: string;
  locator: string;
  order: number;
  file: string;
  vol?: string;
}

let _ipvvIndex: { passages: IndexEntry[] } | null = null;

function ipvvIndex(): { passages: IndexEntry[] } | null {
  if (_ipvvIndex) return _ipvvIndex;
  try {
    _ipvvIndex = JSON.parse(readFileSync(path.join(IPVV_DIR, "index.json"), "utf8"));
  } catch {
    _ipvvIndex = null;
  }
  return _ipvvIndex;
}

// A canonical IPVV record from the lazy store (the phase-1 shape + immutable id).
export interface IpvvPassageRecord {
  id: string;
  immutable_id: string;
  work_id: string;
  chunk: string;
  vol?: string;
  source?: { start?: number; end?: number; text?: string };
  l0?: string | null;
  l2?: string | null;
  l2_text?: string;
  section?: string;
  status?: string;
  c1?: { body: string; terms?: string; see_also?: string; verse_commentary?: { locator: string; commentary: string }[] };
  c1_source?: Record<string, string>;
}

// Load a single IPVV passage record by its id, immutable id, or a locator alias.
function loadIpvvRecord(key: string): IpvvPassageRecord | null {
  const idx = ipvvIndex();
  if (!idx) return null;
  let entry: IndexEntry | undefined;
  for (const e of idx.passages) {
    if (e.id === key || e.immutable_id === key || e.locator === key) {
      entry = e;
      break;
    }
  }
  if (!entry) return null;
  const f = path.join(IPVV_DIR, entry.file);
  if (!existsSync(f)) return null;
  try {
    const rec = JSON.parse(readFileSync(f, "utf8"));
    rec.immutable_id = rec.immutable_id ?? entry.immutable_id;
    return rec;
  } catch {
    return null; // missing/invalid JSON → explicit null, never silent fallback
  }
}

// Shape a lazy IPVV record into the PublishedTranslation the reader/API expect.
// One coarse source span (the Sanskrit range) + the L2 prose as the target, with
// provenance (l0/l2/source). Keeps reader + resolver on ONE canonical object.
function shapeIpvv(rec: IpvvPassageRecord): PublishedTranslation {
  const version = `${rec.id}:v1`;
  return {
    passage_id: rec.id,
    work_id: rec.work_id || "isvarapratyabhijnavivrtivimarsini",
    text: rec.l2_text || "",
    version_id: version,
    version: 1,
    review_state: "proposed",
    provenance: {
      base_source: rec.work_id || "isvarapratyabhijnavivrtivimarsini",
      edition: `our T1 (${rec.chunk || rec.id})`,
      translation_version_id: version,
    },
    source_spans: rec.source?.text
      ? [{ id: `${rec.id}:src`, passage_id: rec.id, text: rec.source.text }]
      : [],
    target_spans: rec.l2_text
      ? [{ id: `${rec.id}:tgt`, translation_version_id: version, text: rec.l2_text }]
      : [],
    alignments: rec.source?.text && rec.l2_text
      ? [{ id: `${rec.id}:align`, source_span_ids: [`${rec.id}:src`], target_span_ids: [`${rec.id}:tgt`], type: "merged", decision_ids: [], method: "pipeline" }]
      : [],
    decisions: [],
    evidence: [],
    // the C1 commentary (attached read/ rendering) — rendered by the Commentary toggle.
    // The reader renders pub.c1.verse_commentary[] (an array). The store may carry it
    // directly (from attach_c1.py) or we derive one entry from body.
    c1: rec.c1?.body || rec.c1?.verse_commentary?.length
      ? {
          body: rec.c1?.body || rec.c1?.verse_commentary?.[0]?.commentary || "",
          verse_commentary: rec.c1?.verse_commentary?.length
            ? rec.c1.verse_commentary
            : [{ locator: rec.chunk || rec.id, commentary: rec.c1?.body || "" }],
          claim_links: [],
          ...(rec.c1?.terms ? { terms: rec.c1.terms } : {}),
          ...(rec.c1?.see_also ? { see_also: rec.c1.see_also } : {}),
        }
      : undefined,
    // the structured c1/source record (for API/MCP + THEMES substrate)
    ...(rec.c1_source ? { c1_source: rec.c1_source } : {}),
  };
}

// The single loader used by BOTH /read and /api/resolve.
export function getPublishedTranslation(passageId: string): PublishedTranslation | undefined {
  // 1. in-memory hand-authored
  if (PUBLISHED[passageId]) return PUBLISHED[passageId];
  // 2. lazy IPVV store (by id, immutable id, or locator alias)
  const rec = loadIpvvRecord(passageId);
  if (rec) return shapeIpvv(rec);
  return undefined;
}

export function getDecision(decisionId: string): TranslationDecision | undefined {
  return DECISIONS[decisionId];
}

export function getEvidence(evidenceId: string): EvidenceItem | undefined {
  return EVIDENCE[evidenceId];
}

export function getDecisionIds(): string[] {
  return Object.keys(DECISIONS);
}

export function ipvvPassageCount(): number {
  return ipvvIndex()?.passages.length ?? 0;
}

// Resolve any key (passage id, immutable id, or locator alias) to the store's
// immutable passage id — the single authority. Used by /api/resolve so that a
// human locator (ipvv:V3-C, chunkV3-C-...) resolves to the SAME immutable id the
// store uses (and /read loads).
export function ipvvResolveImmutable(key: string): string | undefined {
  const idx = ipvvIndex();
  if (!idx) return undefined;
  for (const e of idx.passages) {
    if (e.id === key || e.immutable_id === key || e.locator === key) {
      return e.immutable_id;
    }
    // loose chunk-locator match: "V3-C" inside the chunk name
    if (key && e.locator && key.replace(/^ipvv[: ]+/, "").toLowerCase()
        && e.locator.toLowerCase().includes(key.replace(/^ipvv[: ]+/, "").toLowerCase())) {
      return e.immutable_id;
    }
  }
  return undefined;
}

// ── legacy decision/evidence pools (from the hand-authored units) ──────────
const DECISIONS: Record<string, TranslationDecision> = {};
const EVIDENCE: Record<string, EvidenceItem> = {};
for (const p of Object.values(PUBLISHED)) {
  for (const d of p.decisions) DECISIONS[d.id] = d;
  for (const e of p.evidence) EVIDENCE[e.id] = e;
}

// List the passages of a work (metadata only — from the lazy IPVV index or the
// in-memory registry). Kept for the text overview pages + kramasadbhava decisions.
export function listUnitPassages(workSlug: string): {
  passage_id: string; locator: string; has_translation: boolean; open_decisions: number; decisions: number;
}[] {
  const out: { passage_id: string; locator: string; has_translation: boolean; open_decisions: number; decisions: number }[] = [];
  if (workSlug === "isvarapratyabhijnavivrtivimarsini") {
    const idx = ipvvIndex();
    if (idx) {
      for (const e of idx.passages) {
        const rec = loadIpvvRecord(e.id);
        out.push({
          passage_id: e.id,
          locator: e.locator,
          has_translation: Boolean(rec?.l2_text),
          open_decisions: 0,
          decisions: 0,
        });
      }
    }
    return out.sort((a, b) => a.locator.localeCompare(b.locator));
  }
  for (const [pid, p] of Object.entries(PUBLISHED)) {
    if (!pid.startsWith(`pt:passage:${workSlug}:`)) continue;
    const open = p.decisions.filter((d) => d.status === "OPEN").length;
    out.push({
      passage_id: pid,
      locator: pid.split(":").pop() ?? pid,
      has_translation: Boolean(p.text),
      open_decisions: open,
      decisions: p.decisions.length,
    });
  }
  return out.sort((a, b) => a.locator.localeCompare(b.locator, undefined, { numeric: true }));
}
