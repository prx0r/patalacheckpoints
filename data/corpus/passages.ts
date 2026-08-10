// The passage corpus index — loads the segmented *.jsonl files under
// data/corpus/passages at request time (lazy, cached). Server-only.
// Each passage may carry a working translation (close_translation) derived from
// our T1 files, plus flags and provenance.

import { readFileSync, readdirSync } from "fs";
import path from "path";

export interface Passage {
  id: string;
  work_id: string;
  location: { chapter: number; verse: number };
  sanskrit: string;
  source_edition: string;
  close_translation?: string;
  flags?: string[];
  provenance?: string;
}

const dir = path.join(process.cwd(), "data", "corpus", "passages");

let _index: Passage[] | null = null;

function load(): Passage[] {
  if (_index) return _index;
  const all: Passage[] = [];
  try {
    for (const f of readdirSync(dir)) {
      if (!f.endsWith(".jsonl")) continue;
      for (const line of readFileSync(path.join(dir, f), "utf8").split("\n")) {
        if (line.trim()) all.push(JSON.parse(line) as Passage);
      }
    }
  } catch {
    // corpus dir absent — return empty rather than crash
  }
  _index = all;
  return all;
}

export function getPassages(): Passage[] {
  return load();
}

export function getPassage(id: string): Passage | undefined {
  return load().find((p) => p.id === id);
}

export function searchPassages(q: string): Passage[] {
  const needle = q.toLowerCase();
  return load().filter(
    (p) =>
      p.sanskrit.toLowerCase().includes(needle) ||
      (p.close_translation ?? "").toLowerCase().includes(needle) ||
      p.id.toLowerCase().includes(needle),
  );
}

// Working translations for a work: every segmented passage that carries our T1 close_translation.
export function workingTranslations(workId: string): Passage[] {
  return load().filter((p) => p.work_id === workId && p.close_translation);
}

export function workingTranslationCounts(): Record<string, number> {
  const counts: Record<string, number> = {};
  for (const p of load()) {
    if (p.close_translation) counts[p.work_id] = (counts[p.work_id] ?? 0) + 1;
  }
  return counts;
}
