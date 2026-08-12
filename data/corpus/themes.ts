// themes.ts — deterministic theme structure over the IPVV C1s (Phase 0c).
//
// Derivation: a theme is a group of passages that share a TECHNICAL LEMMA (from the
// c1 KEY TERMS) or a curated See-also edge. This is the STRUCTURED signal the ML pilot
// found to be the discriminating one (shared body-words are noise; shared key-terms +
// curated edges are the signal). It is deterministic — no model call — and is the
// substrate the ML master's theme-clustering will build on (SPEC_THEME_CLUSTERING).
//
// Each theme is a PROPOSAL (MACHINE_PROPOSED); human adjudication is required before it
// is treated as established (the "AI proposes ≠ Pāṭala asserts" rule).

import { readFileSync } from "fs";
import path from "path";

const IPVV_DIR = path.join(process.cwd(), "data", "published", "ipvv");

export interface ThemeMember {
  passage_id: string;
  role: "CORE" | "SUPPORTING";
}

export interface Theme {
  id: string;          // pt:theme:{slug}
  label: string;
  lemma: string;       // the technical term that defines the theme
  members: ThemeMember[];
  status: "MACHINE_PROPOSED";
  evidence: string[];  // the see-also edges / shared-term justification
}

let _index: { passages: { id: string; file: string }[] } | null = null;

function index(): { passages: { id: string; file: string }[] } | null {
  if (_index) return _index;
  try {
    _index = JSON.parse(readFileSync(path.join(IPVV_DIR, "index.json"), "utf8"));
  } catch {
    _index = null;
  }
  return _index;
}

function loadRec(file: string): Record<string, any> | null {
  try {
    return JSON.parse(readFileSync(path.join(IPVV_DIR, file), "utf8"));
  } catch {
    return null;
  }
}

// Parse the KEY TERMS into a set of normalized technical lemmas.
// Formats handled: "- **smṛti** — memory..." and "pramāṇa · prameya · ..."
// Keeps only genuine technical lemmas (has a diacritic, or is a known Sanskrit term) —
// filters English stop/filler words.
const STOP = new Set([
  "the","a","an","and","or","of","in","on","at","to","for","this","that","here",
  "there","not","no","is","are","be","it","as","by","with","from","its","his","her",
  "their","vs","versus","see","also","re","re-","one","two","self","now","then","which",
]);
const KNOWN_TERMS = new Set([
  "pramāṇa","prameya","pramātṛ","vimarśa","prakāśa","saṃvit","svātantrya","ābhāsa",
  "smṛti","anusandhāna","viśrānti","spanda","śakti","kriyā","jñāna","icchā","māyā",
  "apohana","adhyavasāya","pratyabhijñā","ahaṃ","idam","kañcuka","niyati","kāla","rāga",
  "avidyā","kalā","anuttara","kula","akula","upāya","mantra","bīja","śiva","īśvara",
  "pratibimba","ahampratyavamarśa","saṃskāra","tattva","vikalpa","sphurattā","parāvāk",
  "vyāhāra","samīhā","kārikā","sūtra","vimarśaśakti","kramārtha","akrama","bhedābheda",
]);

function isTechnicalTerm(s: string): boolean {
  if (STOP.has(s)) return false;
  if (KNOWN_TERMS.has(s)) return true;
  // has a Sanskrit diacritic → likely technical
  if (/[āīūṛṅñṭḍṇśṣḥĀĪŪṚṆÑṬḌṆŚṢḤ]/.test(s)) return true;
  return false;
}

function termsOf(rec: Record<string, any>): string[] {
  const terms = String(rec?.c1_source?.key_terms ?? rec?.c1?.terms ?? "");
  const out: string[] = [];
  for (const m of terms.matchAll(/\*\*([^*]+)\*\*/g)) {
    const t = m[1].trim().toLowerCase();
    if (isTechnicalTerm(t)) out.push(t);
  }
  for (const part of terms.split(/[·,;\n]/)) {
    const clean = part.replace(/\*\*/g, "").trim();
    if (clean && !clean.startsWith("-")) {
      const first = clean.split(/\s+/)[0].toLowerCase();
      if (isTechnicalTerm(first)) out.push(first);
    }
  }
  return [...new Set(out)];
}

function slug(s: string): string {
  return s.replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

// Build themes by grouping passages that share a technical lemma.
export function deriveThemes(): Theme[] {
  const idx = index();
  if (!idx) return [];
  // passage -> its lemmas
  const passageTerms = new Map<string, string[]>();
  const passageLabel = new Map<string, string>();
  for (const e of idx.passages) {
    const rec = loadRec(e.file);
    if (!rec) continue;
    passageTerms.set(e.id, termsOf(rec));
    passageLabel.set(e.id, e.id.split(":").pop() ?? e.id);
  }
  // lemma -> [passage ids]
  const lemmaMembers = new Map<string, string[]>();
  for (const [pid, terms] of passageTerms) {
    for (const t of terms) {
      if (t.length < 2) continue;
      if (!lemmaMembers.has(t)) lemmaMembers.set(t, []);
      lemmaMembers.get(t)!.push(pid);
    }
  }
  // a theme = a lemma with >=2 member passages (CORE = all)
  const themes: Theme[] = [];
  for (const [lemma, pids] of lemmaMembers) {
    if (pids.length < 2) continue;
    themes.push({
      id: `pt:theme:${slug(lemma)}`,
      label: lemma,
      lemma,
      members: pids.map((pid) => ({ passage_id: pid, role: "CORE" })),
      status: "MACHINE_PROPOSED",
      evidence: pids.map((pid) => `shared lemma "${lemma}" in ${pid}`),
    });
  }
  return themes.sort((a, b) => b.members.length - a.members.length);
}

export function themesFor(passageId: string): Theme[] {
  return deriveThemes().filter((t) => t.members.some((m) => m.passage_id === passageId));
}

export function themeById(id: string): Theme | undefined {
  return deriveThemes().find((t) => t.id === id);
}
