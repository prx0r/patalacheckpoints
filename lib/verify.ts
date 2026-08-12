// lib/verify.ts — the deterministic verification floor (Phase 2 EXPOSE services).
//
// These implement "AI proposes ≠ Pāṭala asserts" as machine access, over data that
// already exists. They are DETERMINISTIC — they return explicit structural verdicts,
// not model judgment. The ML master's INFER services (semantic entailment, discovery)
// operate ABOVE these.
//
//   verifyQuote(quote, ref)           — is this quote present in the passage's source/L2?
//   verifyClaimStructure(claim, ref)  — does the passage resolve? does it have source + L2 + C1?
//   traceDependency(ref, from)        — the derivation DAG backward walk (source←L2←C1)
//   findCounterevidence(claim, ref)   — the curated contradicts/qualifies evidence (explicit edges)

import { getPublishedTranslation, ipvvResolveImmutable } from "@/data/corpus/published";

function norm(s: string): string {
  return (s || "").toLowerCase().replace(/[^\p{L}\p{N}]+/gu, "").trim();
}

export interface VerifyResult {
  ref: string;
  passage_id?: string;
  immutable_id?: string;
  verdict: boolean;
  detail: string;
}

// 1. VERIFY QUOTE — is a verbatim quote present in the passage's source (Sanskrit) or L2?
// Deterministic substring test after NFKC-ish normalization. Distinguishes source-quote
// (Sanskrit) from translation-quote (L2). Returns explicit verdict + where it matched.
export function verifyQuote(quote: string, ref: string): VerifyResult {
  const nq = norm(quote);
  if (!nq) return { ref, verdict: false, detail: "empty quote" };
  const imm = ipvvResolveImmutable(ref);
  const pub = imm ? getPublishedTranslation(imm) : undefined;
  if (!pub) return { ref, verdict: false, detail: "passage not found; quote unverifiable" };
  const sourceText = pub.source_spans.map((s) => s.text).join(" ") || "";
  const l2Text = pub.text || "";
  const inSource = norm(sourceText).includes(nq);
  const inL2 = norm(l2Text).includes(nq);
  let detail = "quote not found";
  if (inSource) detail = "quote matched in the SOURCE (Sanskrit)";
  else if (inL2) detail = "quote matched in the published L2 translation";
  return {
    ref, passage_id: pub.passage_id, immutable_id: imm,
    verdict: inSource || inL2, detail,
  };
}

// 2. VERIFY CLAIM STRUCTURE — does a claim resolve to a passage with the required structure?
// Deterministic: passage must resolve to an immutable id AND carry source + L2 + C1.
export function verifyClaimStructure(claim: string, ref: string): VerifyResult {
  const imm = ipvvResolveImmutable(ref);
  const pub = imm ? getPublishedTranslation(imm) : undefined;
  if (!pub) return { ref, verdict: false, detail: "passage not found; claim has no structural support" };
  const hasSource = (pub.source_spans?.length ?? 0) > 0;
  const hasL2 = Boolean(pub.text);
  const hasC1 = Boolean(pub.c1?.body);
  const ok = hasSource && hasL2 && hasC1;
  return {
    ref, passage_id: pub.passage_id, immutable_id: imm,
    verdict: ok,
    detail: ok
      ? "claim resolves: passage has source + L2 + C1"
      : `claim partially supported (source=${hasSource}, l2=${hasL2}, c1=${hasC1})`,
  };
}

// 3. TRACE DEPENDENCY — walk the derivation DAG backward: claim ← C1 ← L2 ← source.
// Returns the chain of what each layer provides, and where (if anywhere) support breaks.
export function traceDependency(ref: string, from: "essay" | "theme" | "c1" | "l2" = "c1"): VerifyResult {
  const imm = ipvvResolveImmutable(ref);
  const pub = imm ? getPublishedTranslation(imm) : undefined;
  if (!pub) return { ref, verdict: false, detail: "passage not found; dependency chain empty" };
  const chain = [
    { layer: "source", present: (pub.source_spans?.length ?? 0) > 0, note: `${pub.source_spans?.length ?? 0} source span(s)` },
    { layer: "l2", present: Boolean(pub.text), note: pub.text ? `${pub.text.length} chars of L2` : "missing" },
    { layer: "c1", present: Boolean(pub.c1?.body), note: pub.c1?.body ? `${pub.c1.body.length} chars of C1` : "missing" },
  ];
  // find the first break
  const broken = chain.find((c) => !c.present);
  const ok = !broken;
  return {
    ref, passage_id: pub.passage_id, immutable_id: imm,
    verdict: ok,
    detail: ok
      ? "dependency chain intact: source → L2 → C1"
      : `dependency chain breaks at ${broken?.layer}: ${broken?.note}`,
  };
}

// 4. FIND COUNTEREVIDENCE — the curated contradicts/qualifies edges.
// Deterministic: any passage whose C1 explicitly qualifies/contrasts is flagged; in the
// absence of explicit curated edges it returns an honest "no curated counterevidence yet"
// rather than inventing any. (The ML master's discovery service will populate these.)
export function findCounterevidence(ref: string): VerifyResult {
  const imm = ipvvResolveImmutable(ref);
  const pub = imm ? getPublishedTranslation(imm) : undefined;
  if (!pub) return { ref, verdict: false, detail: "passage not found; no counterevidence" };
  const c1 = pub.c1?.body || "";
  // look for explicit qualification/contrast markers in the C1 (deterministic, conservative)
  const markers = ["does not establish", "does not by itself", "not alone", "contrast", "qualified", "tension"];
  const found = markers.filter((m) => c1.includes(m));
  const detail = found.length
    ? `counterevidence/qualification present in C1: ${found.join("; ")}`
    : "no curated counterevidence recorded (C1 does not mark a qualification/contrast)";
  return { ref, passage_id: pub.passage_id, immutable_id: imm, verdict: found.length > 0, detail };
}

export const verifyApi = { verifyQuote, verifyClaimStructure, traceDependency, findCounterevidence };
