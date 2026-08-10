// Kramasadbhāva 1.8 — the published auditable translation object (the product).
//
// The first real instance: source spans, target spans, alignments, decisions, and
// FIRST-CLASS evidence (EvidenceItem pool + EvidenceUse links). All evidence IDs are
// resolvable — nothing dangles.
//
// Sanskrit (Dyczkowski ed.):
//   ooṃ namaste devadeveśi mahākāli namo'stu te | namo'stu paramānande nirānande namo'stu te

import type { PublishedTranslation, TranslationDecision, SourceSpan, TargetSpan, Alignment, EvidenceItem, ReviewState } from "../translation";
import { deriveReviewState } from "../translation";

const PID = "pt:passage:kramasadbhava:1.8";
const VERSION = "pt:translation:kramasadbhava:1.8:v2";

// ── source spans ────────────────────────────────────────────────────────────
export const sourceSpans: SourceSpan[] = [
  { id: "pt:srcspan:krs:1.8:1", passage_id: PID, text: "ooṃ", start: 0, end: 3 },
  { id: "pt:srcspan:krs:1.8:2", passage_id: PID, text: "namaste", start: 4, end: 11 },
  { id: "pt:srcspan:krs:1.8:3", passage_id: PID, text: "devadeveśi", start: 12, end: 22 },
  { id: "pt:srcspan:krs:1.8:4", passage_id: PID, text: "mahākāli", start: 23, end: 31 },
  { id: "pt:srcspan:krs:1.8:5", passage_id: PID, text: "namo'stu te", start: 32, end: 43 },
  { id: "pt:srcspan:krs:1.8:6", passage_id: PID, text: "namo'stu", start: 45, end: 52 },
  { id: "pt:srcspan:krs:1.8:7", passage_id: PID, text: "paramānande", start: 53, end: 64 },
  { id: "pt:srcspan:krs:1.8:8", passage_id: PID, text: "nirānande", start: 65, end: 74 },
  { id: "pt:srcspan:krs:1.8:9", passage_id: PID, text: "namo'stu te", start: 75, end: 86 },
];

// ── target spans ────────────────────────────────────────────────────────────
export const targetSpans: TargetSpan[] = [
  { id: "pt:tgtspan:krs:1.8:1", translation_version_id: VERSION, text: "Oṃ" },
  { id: "pt:tgtspan:krs:1.8:2", translation_version_id: VERSION, text: "homage to you" },
  { id: "pt:tgtspan:krs:1.8:3", translation_version_id: VERSION, text: "O mistress of the god of gods" },
  { id: "pt:tgtspan:krs:1.8:4", translation_version_id: VERSION, text: "Mahākālī" },
  { id: "pt:tgtspan:krs:1.8:5", translation_version_id: VERSION, text: "homage be to you" },
  { id: "pt:tgtspan:krs:1.8:6", translation_version_id: VERSION, text: "homage be to you" },
  { id: "pt:tgtspan:krs:1.8:7", translation_version_id: VERSION, text: "O supreme bliss" },
  { id: "pt:tgtspan:krs:1.8:8", translation_version_id: VERSION, text: "O bliss-less one" },
  { id: "pt:tgtspan:krs:1.8:9", translation_version_id: VERSION, text: "homage be to you" },
];

// ── alignments ──────────────────────────────────────────────────────────────
export const alignments: Alignment[] = [
  { id: "pt:align:krs:1.8:1", source_span_ids: ["pt:srcspan:krs:1.8:1"], target_span_ids: ["pt:tgtspan:krs:1.8:1"], type: "direct", decision_ids: [], method: "human" },
  { id: "pt:align:krs:1.8:2", source_span_ids: ["pt:srcspan:krs:1.8:2"], target_span_ids: ["pt:tgtspan:krs:1.8:2"], type: "direct", decision_ids: [], method: "human" },
  { id: "pt:align:krs:1.8:3", source_span_ids: ["pt:srcspan:krs:1.8:3"], target_span_ids: ["pt:tgtspan:krs:1.8:3"], type: "direct", decision_ids: ["pt:decision:krs:1.8:LEX:1"], method: "pipeline_adjudication" },
  { id: "pt:align:krs:1.8:4", source_span_ids: ["pt:srcspan:krs:1.8:4"], target_span_ids: ["pt:tgtspan:krs:1.8:4"], type: "direct", decision_ids: [], method: "human" },
  { id: "pt:align:krs:1.8:5", source_span_ids: ["pt:srcspan:krs:1.8:5"], target_span_ids: ["pt:tgtspan:krs:1.8:5"], type: "direct", decision_ids: [], method: "human" },
  { id: "pt:align:krs:1.8:6", source_span_ids: ["pt:srcspan:krs:1.8:6"], target_span_ids: ["pt:tgtspan:krs:1.8:6"], type: "direct", decision_ids: [], method: "human" },
  { id: "pt:align:krs:1.8:7", source_span_ids: ["pt:srcspan:krs:1.8:7"], target_span_ids: ["pt:tgtspan:krs:1.8:7"], type: "direct", decision_ids: ["pt:decision:krs:1.8:LEX:3"], method: "pipeline_adjudication" },
  { id: "pt:align:krs:1.8:8", source_span_ids: ["pt:srcspan:krs:1.8:8"], target_span_ids: ["pt:tgtspan:krs:1.8:8"], type: "direct", decision_ids: ["pt:decision:krs:1.8:LEX:2"], method: "pipeline_adjudication" },
  { id: "pt:align:krs:1.8:9", source_span_ids: ["pt:srcspan:krs:1.8:9"], target_span_ids: ["pt:tgtspan:krs:1.8:9"], type: "direct", decision_ids: [], method: "human" },
];

// ── evidence pool (FIRST-CLASS, all resolvable) ─────────────────────────────
export const evidence: EvidenceItem[] = [
  { id: "pt:evidence:krs:1.8:1", resource_id: PID, locator: "1.8", excerpt: "ooṃ namaste devadeveśi mahākāli namo'stu te", verification: "verified" },
  { id: "pt:evidence:krs:1.8:2", resource_id: "pt:passage:kramasadbhava:1.9", locator: "1.9 (kuleśi)", excerpt: "namo nitye tvanitye ca ... kuleśi kauleśi", verification: "verified" },
  { id: "pt:evidence:krs:1.8:3", resource_id: "pt:passage:kramasadbhava:1.6", locator: "1.6 (nirāmayaḥ)", excerpt: "mahābhīmo bhairavo vai nirāmayaḥ", verification: "verified" },
  { id: "pt:evidence:krs:1.8:4", resource_id: "pt:res:mahanaya-kramasadbhava", locator: "1.8", excerpt: "Mahānaya renders nirānande as 'the Bliss of Stillness'", verification: "locator_unverified" },
  { id: "pt:evidence:krs:1.8:5", resource_id: "pt:res:kubjika-niracarananda", locator: "nirācārānanda", excerpt: "nirānanda connected with nirācārānanda 'bliss of stillness' (Dyczkowski-related Kubjikā material)", verification: "quote_unverified" },
  { id: "pt:evidence:krs:1.8:6", resource_id: "pt:res:dyczkowski-ed", locator: "1.8", excerpt: "Dyczkowski edition of the Kramasadbhāva", verification: "verified" },
];

// ── the decisions ───────────────────────────────────────────────────────────
export const decisions: TranslationDecision[] = [
  {
    id: "pt:decision:krs:1.8:LEX:1",
    passage_id: PID,
    translation_version_id: VERSION,
    source_span_ids: ["pt:srcspan:krs:1.8:3"],
    target_span_ids: ["pt:tgtspan:krs:1.8:3"],
    type: "LEXICAL",
    claim: "devadeveśi — the compound parse",
    surface_rendering: "O mistress of the god of gods (devadeva-īśī)",
    adjudicated_reading: "O mistress of the god of gods",
    alternatives: ["queen of the gods (deva-deveśī)"],
    status: "PREFERRED",
    evidence_state: "grounded",
    editorial_status: "proposed",
    reason: "The doubled deva forms the superlative 'god of gods'; īśī 'mistress' matches the kuleśī pattern at 1.9.",
    method: "pipeline_adjudication",
    evidence: [
      { evidence_id: "pt:evidence:krs:1.8:1", role: "defines" },
      { evidence_id: "pt:evidence:krs:1.8:2", role: "parallel" },
    ],
    review_events: [],
    origin: "machine",
    created_at: "2026-08-10",
    created_by: "patala-pipeline",
  },
  {
    id: "pt:decision:krs:1.8:LEX:2",
    passage_id: PID,
    translation_version_id: VERSION,
    source_span_ids: ["pt:srcspan:krs:1.8:8"],
    target_span_ids: ["pt:tgtspan:krs:1.8:8"],
    type: "LEXICAL",
    claim: "nirānande — privative vs technical sense",
    surface_rendering: "O bliss-less one (privative nir-+ānanda)",   // current surface, NOT a resolution
    alternatives: ["O bliss at rest / stillness (technical Krama sense)"],
    status: "OPEN",
    evidence_state: "partially_grounded",
    editorial_status: "proposed",
    reason: "Morphology supports the privative; but Krama/Kubjikā material (Mahānaya's 'Bliss of Stillness'; nirācārānanda) suggests a technical transcendent sense. R2's CONSTRAINED was overconfident.",
    method: "pipeline_adjudication",
    evidence: [
      { evidence_id: "pt:evidence:krs:1.8:1", role: "defines" },
      { evidence_id: "pt:evidence:krs:1.8:3", role: "parallel" },
      { evidence_id: "pt:evidence:krs:1.8:4", role: "parallel" },
      { evidence_id: "pt:evidence:krs:1.8:5", role: "defines" },
      { evidence_id: "pt:evidence:krs:1.8:6", role: "supports" },
    ],
    review_events: [],
    origin: "machine",
    created_at: "2026-08-10",
    created_by: "patala-pipeline",
  },
  {
    id: "pt:decision:krs:1.8:LEX:3",
    passage_id: PID,
    translation_version_id: VERSION,
    source_span_ids: ["pt:srcspan:krs:1.8:7"],
    target_span_ids: ["pt:tgtspan:krs:1.8:7"],
    type: "LEXICAL",
    claim: "paramānande — uncontested vocative",
    surface_rendering: "O supreme bliss",
    adjudicated_reading: "O supreme bliss",
    alternatives: [],
    status: "CONSTRAINED",
    evidence_state: "grounded",
    editorial_status: "proposed",
    reason: "Uncontested vocative; forms the polar pair with nirānande.",
    method: "pipeline_adjudication",
    evidence: [{ evidence_id: "pt:evidence:krs:1.8:1", role: "defines" }],
    review_events: [],
    origin: "machine",
    created_at: "2026-08-10",
    created_by: "patala-pipeline",
  },
];

export const published18: PublishedTranslation = {
  passage_id: PID,
  work_id: "pt:work:kramasadbhava",
  text: "Oṃ, homage to you, O mistress of the god of gods, Mahākālī; homage be to you. Homage be to you, O supreme bliss; to you, O bliss-less one, homage be to you.",
  version_id: VERSION,
  version: 2,
  source_spans: sourceSpans,
  target_spans: targetSpans,
  alignments,
  decisions,
  evidence,
  review_state: deriveReviewState(decisions) as ReviewState,   // DERIVED, not manual
  c1: {
    body: "Kramasadbhāva 1.8 — the maṅgala's vocative-chain crux.",
    verse_commentary: [
      {
        locator: "1.8",
        commentary: `The verse opens the homage with four vocatives, each naming the goddess in a different register. "Mistress of the god of gods" (devadeveśī): the doubled deva makes the superlative — she governs the source of the gods, the power of the Lord, not a deity among deities. "Great Kālī": the all-devouring, not a destroyer but the power of consciousness that absorbs the world back into the light that witnesses it.

The centre is the pair paramānande / nirānande — "O supreme bliss" and "O bliss-less." The privative (nir-) most directly gives "the bliss-less one," and R2's LEX:2 marked that CONSTRAINED. But the hymn's logic points elsewhere: everywhere it addresses the goddess across a pair (eternal/non-eternal at 1.9, being/non-being at 1.14) to say she is beyond both, not one pole. On that reading nirānande is the "bliss at rest" — the stillness beyond joy and its loss, the anākhya of the Krama's own cycle. The morphology and the doctrine pull apart; LEX:2 is genuinely OPEN. This commentary does not resolve it — it preserves the contest and lets the reader weigh the two.`,
      },
    ],
    claim_links: [
      { claim: "mistress of the god of gods", target_span_id: "pt:tgtspan:krs:1.8:3" },
      { claim: "O supreme bliss", target_span_id: "pt:tgtspan:krs:1.8:7" },
      { claim: "O bliss-less one / O bliss at rest", target_span_id: "pt:tgtspan:krs:1.8:8" },
    ],
  },
  provenance: {
    base_source: "pt:src:kramasadbhava:dyczkowski-ed",
    edition: "Dyczkowski ed., Muktabodha (NGMPP A 209/23)",
    translation_version_id: VERSION,
  },
};
