// analyst.ts — the metacognitive layer (borrowed from the HXRMXS `my_thoughts` field).
//
// Before the system narrates a journey/lesson step, it produces a MetaThought block — the
// internal analyst reasoning about the READER's state, not just serving content:
//   hypothesis (why I think the reader is here)
//   best_move  (why this is the right stop/move now)
//   trap       (what failure mode I'm avoiding)
//   predict    (what I expect the reader to ask/do next)
//   watch      (what I'll look for in the next step to confirm/correct)
//
// The graph selects the move; this layer explains/predicts/watches; the LLM only narrates.
// Deterministic over the existing structure (themes, C1, journey, recommend) — no LLM in the
// decision path.

import { journeyFromPassage, journeyFromTheme } from "./journey";
import { recommendForPassage } from "./recommend";
import { themesFor } from "./themes";

export interface MetaThought {
  stop_id: string;
  hypothesis: string;
  best_move: string;
  trap: string;
  predict: string;
  watch: string;
}

// Generate a MetaThought for a passage stop, using its themes + recommendations.
export function analystForPassage(passageId: string, label: string, seeAlso: string): MetaThought {
  const themes = themesFor(passageId);
  const recs = recommendForPassage(passageId, seeAlso);
  const themeLabel = themes.length ? themes[0].label : "the passage's own theme";
  const root = recs.find((r) => r.relation === "ROOT_TEXT");
  const parallel = recs.find((r) => r.relation === "PARALLEL");
  return {
    stop_id: passageId,
    hypothesis: `The reader arrived via ${themeLabel} — they are likely comparing this to nearby passages (${seeAlso || "the see-also"}) and may conflate the specific with the general.`,
    best_move: root
      ? `Anchor on the ROOT_TEXT (${root.title}) — this passage resolves against the root kārikā, so show that relation before the doctrine.`
      : `Anchor on the passage's own claim and its see-also, then the theme.`,
    trap: `Do NOT jump to the synthesis (the master-key / the essay) before the reader has felt the split this passage exposes.`,
    predict: `The reader will likely ask how this relates to ${parallel ? parallel.title : "the parallel commentary"} — the relation is where the tension lives.`,
    watch: `Watch whether they move from "this passage states X" to "this passage does the work of Y" — the step from content to mechanism.`,
  };
}

// Generate a MetaThought for a theme (concept-entry) journey.
export function analystForTheme(lemma: string): MetaThought {
  return {
    stop_id: `concept:${lemma}`,
    hypothesis: `The reader entered by the concept ${lemma} — they likely have a pre-existing (possibly wrong) intuition about it.`,
    best_move: `Show the occurrence map + the misconception→correction→evidence block first, then the passages.`,
    trap: `Do not let the reader's modern/intuitive sense of ${lemma} be silently confirmed; surface the textual register explicitly.`,
    predict: `They will test the concept against a specific passage they half-remember.`,
    watch: `Watch for the moment they stop using ${lemma} as a label and start using it as a structure.`,
  };
}

// The compiled analyst layer over a journey: one MetaThought per stop.
export function analystForJourney(entry: string, opts: { passage?: string; label?: string; seeAlso?: string; theme?: string }) {
  if (opts.passage) {
    const j = journeyFromPassage(opts.passage, opts.label ?? opts.passage, opts.seeAlso ?? "");
    return {
      entry,
      analyst: analystForPassage(opts.passage, opts.label ?? opts.passage, opts.seeAlso ?? ""),
      journey: j,
    };
  }
  if (opts.theme) {
    const j = journeyFromTheme(opts.theme);
    return { entry, analyst: analystForTheme(opts.theme), journey: j };
  }
  return null;
}
