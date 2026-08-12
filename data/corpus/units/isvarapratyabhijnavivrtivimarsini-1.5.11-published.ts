// IPVV 1.5.11 — the published auditable translation object (the recognition-thesis unit).
//
// The single most important passage for the recognition thesis: IPK 1.5.11, as expanded by the
// IPVV. "The essential nature of light is reflective awareness (vimarśa); otherwise light, though
// 'coloured' by objects, would be similar to an insentient reality, such as crystal."
//
// Sanskrit (Torella ed., IPK 1.5.11 + Vṛtti):
//   prakāśo vimarśo 'tha vā prakāśātmā prakāśo hi vimarśaḥ svabhāvaḥ |
//   anyathā 'rthagrāhako prakāśo hi rūpasthito 'pi sphāṭikādivad acetanatāṃ prāpnuyāt
//
// This unit is the "toggleable source" for the recognition thesis: the reader renders the
// Sanskrit, the translation, and the C1 commentary (the deep IPVV expansion), each independently
// toggled.

import type { PublishedTranslation, TranslationDecision, SourceSpan, TargetSpan, Alignment, EvidenceItem, ReviewState } from "../translation";
import { deriveReviewState } from "../translation";

const PID = "pt:passage:isvarapratyabhijnavivrtivimarsini:1.5.11";
const VERSION = "pt:translation:isvarapratyabhijnavivrtivimarsini:1.5.11:v1";

// ── source spans ────────────────────────────────────────────────────────────
export const sourceSpans: SourceSpan[] = [
  { id: "pt:srcspan:ipvv:1.5.11:1", passage_id: PID, text: "prakāśasya", start: 0, end: 9 },
  { id: "pt:srcspan:ipvv:1.5.11:2", passage_id: PID, text: "vimarśo", start: 10, end: 17 },
  { id: "pt:srcspan:ipvv:1.5.11:3", passage_id: PID, text: "vā", start: 18, end: 20 },
  { id: "pt:srcspan:ipvv:1.5.11:4", passage_id: PID, text: "mukhya ātmā", start: 21, end: 31 },
  { id: "pt:srcspan:ipvv:1.5.11:5", passage_id: PID, text: "anyathā", start: 32, end: 39 },
  { id: "pt:srcspan:ipvv:1.5.11:6", passage_id: PID, text: "arthagrāhako", start: 40, end: 52 },
  { id: "pt:srcspan:ipvv:1.5.11:7", passage_id: PID, text: "prakāśo", start: 53, end: 61 },
  { id: "pt:srcspan:ipvv:1.5.11:8", passage_id: PID, text: "rūpasthito 'pi", start: 62, end: 76 },
  { id: "pt:srcspan:ipvv:1.5.11:9", passage_id: PID, text: "sphāṭikādivad", start: 77, end: 89 },
  { id: "pt:srcspan:ipvv:1.5.11:10", passage_id: PID, text: "acetanatāṃ", start: 90, end: 100 },
  { id: "pt:srcspan:ipvv:1.5.11:11", passage_id: PID, text: "prāpnuyāt", start: 101, end: 109 },
];

// ── target spans ────────────────────────────────────────────────────────────
export const targetSpans: TargetSpan[] = [
  { id: "pt:tgtspan:ipvv:1.5.11:1", translation_version_id: VERSION, text: "of light" },
  { id: "pt:tgtspan:ipvv:1.5.11:2", translation_version_id: VERSION, text: "reflective awareness (vimarśa)" },
  { id: "pt:tgtspan:ipvv:1.5.11:3", translation_version_id: VERSION, text: "indeed" },
  { id: "pt:tgtspan:ipvv:1.5.11:4", translation_version_id: VERSION, text: "is the primary essence (mukhya ātman)" },
  { id: "pt:tgtspan:ipvv:1.5.11:5", translation_version_id: VERSION, text: "otherwise" },
  { id: "pt:tgtspan:ipvv:1.5.11:6", translation_version_id: VERSION, text: "the object-apprehending" },
  { id: "pt:tgtspan:ipvv:1.5.11:7", translation_version_id: VERSION, text: "light" },
  { id: "pt:tgtspan:ipvv:1.5.11:8", translation_version_id: VERSION, text: "though 'coloured' by its form" },
  { id: "pt:tgtspan:ipvv:1.5.11:9", translation_version_id: VERSION, text: "like crystal and the like" },
  { id: "pt:tgtspan:ipvv:1.5.11:10", translation_version_id: VERSION, text: "insentience" },
  { id: "pt:tgtspan:ipvv:1.5.11:11", translation_version_id: VERSION, text: "would attain" },
];

// ── alignments ──────────────────────────────────────────────────────────────
export const alignments: Alignment[] = [
  { id: "pt:align:ipvv:1.5.11:1", source_span_ids: ["pt:srcspan:ipvv:1.5.11:1"], target_span_ids: ["pt:tgtspan:ipvv:1.5.11:1"], type: "direct", decision_ids: [], method: "human" },
  { id: "pt:align:ipvv:1.5.11:2", source_span_ids: ["pt:srcspan:ipvv:1.5.11:2"], target_span_ids: ["pt:tgtspan:ipvv:1.5.11:2"], type: "direct", decision_ids: ["pt:decision:ipvv:1.5.11:LEX:1"], method: "pipeline_adjudication" },
  { id: "pt:align:ipvv:1.5.11:3", source_span_ids: ["pt:srcspan:ipvv:1.5.11:3"], target_span_ids: ["pt:tgtspan:ipvv:1.5.11:3"], type: "direct", decision_ids: [], method: "human" },
  { id: "pt:align:ipvv:1.5.11:4", source_span_ids: ["pt:srcspan:ipvv:1.5.11:4"], target_span_ids: ["pt:tgtspan:ipvv:1.5.11:4"], type: "direct", decision_ids: [], method: "human" },
  { id: "pt:align:ipvv:1.5.11:5", source_span_ids: ["pt:srcspan:ipvv:1.5.11:5"], target_span_ids: ["pt:tgtspan:ipvv:1.5.11:5"], type: "direct", decision_ids: [], method: "human" },
  { id: "pt:align:ipvv:1.5.11:6", source_span_ids: ["pt:srcspan:ipvv:1.5.11:6"], target_span_ids: ["pt:tgtspan:ipvv:1.5.11:6"], type: "direct", decision_ids: [], method: "human" },
  { id: "pt:align:ipvv:1.5.11:7", source_span_ids: ["pt:srcspan:ipvv:1.5.11:7"], target_span_ids: ["pt:tgtspan:ipvv:1.5.11:7"], type: "direct", decision_ids: [], method: "human" },
  { id: "pt:align:ipvv:1.5.11:8", source_span_ids: ["pt:srcspan:ipvv:1.5.11:8"], target_span_ids: ["pt:tgtspan:ipvv:1.5.11:8"], type: "direct", decision_ids: [], method: "human" },
  { id: "pt:align:ipvv:1.5.11:9", source_span_ids: ["pt:srcspan:ipvv:1.5.11:9"], target_span_ids: ["pt:tgtspan:ipvv:1.5.11:9"], type: "direct", decision_ids: [], method: "human" },
  { id: "pt:align:ipvv:1.5.11:10", source_span_ids: ["pt:srcspan:ipvv:1.5.11:10"], target_span_ids: ["pt:tgtspan:ipvv:1.5.11:10"], type: "direct", decision_ids: [], method: "human" },
  { id: "pt:align:ipvv:1.5.11:11", source_span_ids: ["pt:srcspan:ipvv:1.5.11:11"], target_span_ids: ["pt:tgtspan:ipvv:1.5.11:11"], type: "direct", decision_ids: [], method: "human" },
];

// ── evidence pool ───────────────────────────────────────────────────────────
export const evidence: EvidenceItem[] = [
  { id: "pt:evidence:ipvv:1.5.11:1", resource_id: PID, locator: "1.5.11", excerpt: "prakāśasya vimarśo vā mukhya ātmā", verification: "verified" },
  { id: "pt:evidence:ipvv:1.5.11:2", resource_id: "pt:res:torella-ipk", locator: "1.5.11 + Vṛtti", excerpt: "Reflective awareness (pratyavamarsa) constitutes the primary essence (mukhya atma) of light... since there is no 'savouring' (camatkrteh)", verification: "verified" },
  { id: "pt:evidence:ipvv:1.5.11:3", resource_id: "pt:passage:isvarapratyabhijnavivrtivimarsini:2.5.11", locator: "V2H", excerpt: "The manifestation is not a passive, inert light. Its very nature is the reflexive-awareness — the light's own grasp of itself", verification: "verified" },
  { id: "pt:evidence:ipvv:1.5.11:4", resource_id: "pt:res:ratie-le-soi", locator: "Ch. 7", excerpt: "camatkara... the satisfaction one discovers oneself feeling", verification: "locator_unverified" },
];

// ── the decisions ───────────────────────────────────────────────────────────
export const decisions: TranslationDecision[] = [
  {
    id: "pt:decision:ipvv:1.5.11:LEX:1",
    passage_id: PID,
    translation_version_id: VERSION,
    source_span_ids: ["pt:srcspan:ipvv:1.5.11:2"],
    target_span_ids: ["pt:tgtspan:ipvv:1.5.11:2"],
    type: "LEXICAL",
    claim: "vimarśa — reflective awareness as the essence",
    surface_rendering: "reflective awareness (vimarśa)",
    adjudicated_reading: "reflective awareness (vimarśa), the self-grasp that is the felt essence of light",
    alternatives: ["reflexive determination", "the light's own grasp of itself"],
    status: "PREFERRED",
    evidence_state: "grounded",
    editorial_status: "proposed",
    reason: "The Vṛtti glosses vimarśa as pratyavamarsa and ties it to camatkṛti (savouring) — the felt register. The IPVV expands it as 'the light's own grasp of itself' and identifies it with the parā-vāk and the māheśvarya.",
    method: "pipeline_adjudication",
    evidence: [
      { evidence_id: "pt:evidence:ipvv:1.5.11:1", role: "defines" },
      { evidence_id: "pt:evidence:ipvv:1.5.11:2", role: "defines" },
      { evidence_id: "pt:evidence:ipvv:1.5.11:3", role: "supports" },
      { evidence_id: "pt:evidence:ipvv:1.5.11:4", role: "parallel" },
    ],
    review_events: [],
    origin: "machine",
    created_at: "2026-08-11",
    created_by: "patala-pipeline",
  },
];

export const published1511: PublishedTranslation = {
  passage_id: PID,
  work_id: "pt:work:isvarapratyabhijnavivrtivimarsini",
  text: "Of light, reflective awareness (vimarśa) is indeed the primary essence; otherwise, though coloured by its form, the object-apprehending light would be like crystal — it would attain insentience.",
  version_id: VERSION,
  version: 1,
  source_spans: sourceSpans,
  target_spans: targetSpans,
  alignments,
  decisions,
  evidence,
  review_state: deriveReviewState(decisions) as ReviewState,
  c1: {
    body: "IPK 1.5.11 — the reflexivity claim at the root of the recognition thesis, expanded by the IPVV.",
    verse_commentary: [
      {
        locator: "1.5.11",
        commentary: `This kārikā is the seed of the whole recognition philosophy. It states the reflexivity claim: the essence of light — of consciousness — is not the passive showing of objects but the reflective awareness (vimarśa) that the light is present to itself in the act of showing. The Vṛtti adds the decisive gloss: reflective awareness (pratyavamarsa) is the primary essence (mukhya atman) of light, "since there is no savouring (camatkrteh)."

The point is precise. A light that merely reflected the blue, the yellow, the jar — without knowing that it reflected — would be no different from a crystal. It would show the world, but it would not be aware of showing it; it would be inert. What makes the light conscious, what makes it not a thing, is that it is present to itself in the act of manifesting. And that self-presence is a savouring, a camatkrti — a felt, not merely formal, reflexivity.

The IPVV (V2H) expands this into the heart of the whole teaching: "The manifestation is not a passive, inert light. Its very nature is the reflexive-awareness — the light's own grasp of itself." And it identifies this reflexive-awareness with the supreme Word (parā-vāk), with the Lord's freedom (svātantrya), and with his lordship (aiśvarya). The reflexivity claim of 1.5.11 is the root of the recognition-thesis: because the essence of light is the felt self-awareness, recognition is the felt re-cognition of the self — the removal of a false self-positioning, and nothing added.

The honest boundary: the IPK asserts that vimarśa is the essence; the IPVV proves it (the swift-action argument, V2H) and expands it (the parā-vāk, the māheśvarya). But the universalization — that all such self-aware light is one — is the further commitment the tradition makes, argued via the order-less support (V2O) but not forced.`,
      },
    ],
    claim_links: [
      { claim: "reflective awareness (vimarśa)", target_span_id: "pt:tgtspan:ipvv:1.5.11:2" },
      { claim: "the felt essence (camatkṛti)", target_span_id: "pt:tgtspan:ipvv:1.5.11:4" },
      { claim: "like crystal / insentient", target_span_id: "pt:tgtspan:ipvv:1.5.11:9" },
    ],
  },
  provenance: {
    base_source: "pt:src:isvarapratyabhijnakarika:torella-ed",
    edition: "Torella critical ed., IPK 1.5.11 + Vṛtti; IPVV expansion",
    translation_version_id: VERSION,
  },
};
