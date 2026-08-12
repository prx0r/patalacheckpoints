// GET /api/resolve?ref=ipvv:V2-S:14 — the citation backbone (FROZEN product model §2).
//
// Resolves a reference through the whole chain:
//   ref → immutable passage ID → work → passage → source spans → translations →
//   decisions → C1 → related claims/themes
//
// ID-based first, human-readable alias second. Never bakes a mutable locator into
// the system (see lib/citation.ts).

import { NextRequest, NextResponse } from "next/server";
import { resolve, canonicalize } from "@/lib/citation";
import { getPublishedTranslation, ipvvResolveImmutable } from "@/data/corpus/published";
import { getPassage } from "@/data/corpus/passages";
import { relationsFor } from "@/data/corpus/relations";
import { works } from "@/data/corpus/works";

export async function GET(req: NextRequest) {
  const ref = (new URL(req.url).searchParams.get("ref") ?? "").trim();
  if (!ref) {
    return NextResponse.json({ error: "missing_ref", hint: "?ref=ipvv:V2-S:14 or ?ref=pt:pid:..." }, { status: 400 });
  }

  const r = resolve(ref);
  // Prefer the lazy store's immutable id (single authority) over the kernel's hash,
  // so /read and /resolve agree on the exact immutable passage id.
  const storeImmutable = ipvvResolveImmutable(ref) ?? (r.ok ? ipvvResolveImmutable(r.immutable_id) : undefined);
  const immutable_id = storeImmutable ?? (r.ok ? r.immutable_id : undefined);
  const resolved_via = r.ok ? r.via : "store";

  if (!r.ok && !storeImmutable) {
    return NextResponse.json({ error: r.error, ref, hint: "try ipvv:1.5.11 or a tantra:text: urn" }, { status: 404 });
  }

  // resolve to passage by immutable id (registry) or canonical locator
  const c = canonicalize(ref);
  const workId = c.work ?? "isvarapratyabhijnavivrtivimarsini";
  const locator = c.locator ?? c.slug ?? ref;
  const passageId = `tantra:text:${workId}:${locator.split("§").pop()?.trim() ?? locator}`;

  // Try the canonical id, then the phase-1 chunk-locator form, then the immutable id.
  // The lazy loader (getPublishedTranslation) serves /read and /resolve the SAME object.
  let published = getPublishedTranslation(passageId)
    ?? getPublishedTranslation(storeImmutable ?? "")
    ?? getPublishedTranslation(locator);
  const passage = getPassage(passageId) ?? getPassage(locator);
  const work = works.find((w) => w.id === workId);

  // decisions + evidence from the published object (if any)
  const decisions = published?.decisions ?? [];
  const evidence = published?.evidence ?? [];
  const c1 = published?.c1 ?? null;

  const related = relationsFor(workId);

  return NextResponse.json({
    ref,
    immutable_id,
    resolved_via,
    chain: {
      work: work ? { id: work.id, title: work.title, urn: work.urn } : null,
      passage: passage ?? null,
      source_spans: passage ? [{ source_edition: passage.source_edition }] : [],
      translations: published
        ? [{ review_state: published.review_state, has_decisions: decisions.length > 0 }]
        : [],
      decisions: decisions.map((d) => ({ id: d.id, claim: d.claim, status: d.status, evidence_state: d.evidence_state })),
      evidence: evidence.map((e) => ({ id: e.id, resource_id: e.resource_id, verification: e.verification })),
      c1: c1 ? { present: true, blocks: c1.body.length } : null,
      related: related.map((x) => ({ source: x.source, target: x.target, relation: x.relation, certainty: x.certainty })),
    },
  });
}
