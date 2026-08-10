// The published-translation registry — serves the phrase-click API.
// Milestone: the publishable translation object (see data/corpus/translation.ts).
import type { PublishedTranslation, TranslationDecision, EvidenceItem } from "./translation";
import { published18 } from "./units/kramasadbhava-1.8-published";
import { kramasadbhava_1_25 } from "./units/kramasadbhava-1-25-generated";

const PUBLISHED: Record<string, PublishedTranslation> = {
  "pt:passage:kramasadbhava:1.8": published18,
  "tantra:text:kramasadbhava:1.8": published18,
  // generated 1.1–1.25 — but the hand-authored 1.8 is richer, so keep it.
  ...Object.fromEntries(
    Object.entries(kramasadbhava_1_25).filter(([pid]) => !pid.endsWith(":1.8"))
  ),
};
// also index by the tantra:text: urn form (skip 1.8, already hand-authored)
for (const [pid, p] of Object.entries(kramasadbhava_1_25)) {
  if (pid.endsWith(":1.8")) continue;
  PUBLISHED[pid.replace("pt:passage:", "tantra:text:")] = p;
}

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

export function listUnitPassages(workSlug: string): { passage_id: string; locator: string; has_translation: boolean; open_decisions: number; decisions: number }[] {
  const out: { passage_id: string; locator: string; has_translation: boolean; open_decisions: number; decisions: number }[] = [];
  const prefix = `pt:passage:${workSlug}:`;
  for (const [pid, p] of Object.entries(PUBLISHED)) {
    if (!pid.startsWith(prefix)) continue;
    const verse = pid.split(":").pop() ?? "";
    out.push({
      passage_id: pid,
      locator: verse,
      has_translation: p.text.length > 0,
      open_decisions: p.decisions.filter((d) => d.status === "OPEN").length,
      decisions: p.decisions.length,
    });
  }
  return out.sort((a, b) => a.locator.localeCompare(b.locator, undefined, { numeric: true }));
}
