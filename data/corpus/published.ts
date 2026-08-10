// The published-translation registry — serves the phrase-click API.
// Milestone: the publishable translation object (see data/corpus/translation.ts).
import type { PublishedTranslation, TranslationDecision, EvidenceItem } from "./translation";
import { published18 } from "./units/kramasadbhava-1.8-published";

const PUBLISHED: Record<string, PublishedTranslation> = {
  "pt:passage:kramasadbhava:1.8": published18,
  "tantra:text:kramasadbhava:1.8": published18,
};

const DECISIONS: Record<string, TranslationDecision> = {};
const EVIDENCE: Record<string, EvidenceItem> = {};
for (const p of Object.values(PUBLISHED)) {
  for (const d of p.decisions) DECISIONS[d.id] = d;
  for (const e of p.evidence) EVIDENCE[e.id] = e;
}

export function getPublishedTranslation(passageId: string): PublishedTranslation | undefined {
  return PUBLISHED[passageId];
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
