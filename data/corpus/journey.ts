// journey.ts — the graph-owned teaching-path selector.
//
// Given a learner's entry (a concept, a question, a passage), the graph composes a guided
// journey: a sequence of stops (passage → C1 → theme → parallel → essay) selected from the
// graph's OWN structure (themes, spines, C1 see_also, the recommend rail) — not a
// hand-authored course. The LLM only narrates the chosen path; the graph owns the move.
//
// This is the education layer's core primitive: the "guided journey" / choose-your-path.

import { deriveThemes, themesFor } from "./themes";
import { recommendForPassage } from "./recommend";
import { spineFor } from "./canonical-spines";

export interface JourneyStop {
  kind: "passage" | "theme" | "c1" | "parallel" | "essay" | "concept";
  id: string;
  label: string;
  note?: string;
}

export interface Journey {
  entry: string;
  stops: JourneyStop[];
  rationale: string;
}

// Build a journey from a starting passage (chunk id) + its C1 see_also.
export function journeyFromPassage(passageId: string, label: string, seeAlso: string): Journey {
  const stops: JourneyStop[] = [];
  // 1. the passage itself
  stops.push({ kind: "passage", id: passageId, label });
  // 2. its C1 see_also -> related passages
  if (seeAlso) {
    for (const ref of seeAlso.split(/[·,;]/)) {
      const clean = ref.trim();
      if (clean) stops.push({ kind: "c1", id: clean, label: `see-also: ${clean}` });
    }
  }
  // 3. the themes it belongs to
  for (const t of themesFor(passageId)) {
    stops.push({ kind: "theme", id: t.id, label: `theme: ${t.label}` });
  }
  // 4. the related works (root/parallel/scholarship)
  for (const r of recommendForPassage(passageId, seeAlso).slice(0, 4)) {
    stops.push({ kind: "parallel", id: r.work_id, label: `${r.relation}: ${r.title}` });
  }
  return { entry: passageId, stops, rationale: "path composed from the passage's C1 see-also + its themes + the related-text rail" };
}

// Build a journey from a concept (a theme label) — the learner enters by idea.
export function journeyFromTheme(lemma: string): Journey {
  const stops: JourneyStop[] = [{ kind: "concept", id: `concept:${lemma}`, label: lemma }];
  const themes = deriveThemes();
  const t = themes.find((x) => x.label === lemma) ?? themes[0];
  if (t) {
    stops.push({ kind: "theme", id: t.id, label: `theme: ${t.label}` });
    for (const m of t.members.slice(0, 5)) {
      stops.push({ kind: "passage", id: m.passage_id, label: m.passage_id });
    }
  }
  return { entry: lemma, stops, rationale: "path composed from the theme's member passages" };
}
