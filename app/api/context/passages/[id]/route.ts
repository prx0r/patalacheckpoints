// GET /api/context/passages/:id — the deterministic evidence bundle (get_passage_context).
// Assembles: passage + work + manuscript witnesses + neighboring passages + tracked
// terms + related works + our translations + rights. NO generated interpretation —
// it is a transparent evidence packet (per NORTHSTAR.md).

import { NextRequest, NextResponse } from "next/server";
import { getPassage, getPassages } from "@/data/corpus/passages";
import { works } from "@/data/corpus/works";
import { manuscriptsForWork } from "@/data/corpus/manuscripts";
import { relationsFor } from "@/data/corpus/relations";
import { getTerm } from "@/data/corpus/terms";

export async function GET(
  _req: NextRequest,
  ctx: { params: Promise<{ id: string }> },
) {
  const { id: raw } = await ctx.params;
  const id = raw.startsWith("tantra:text:") ? raw : `tantra:text:${raw}`;
  const passage = getPassage(id);
  if (!passage) {
    return NextResponse.json({ error: "not_found", id }, { status: 404 });
  }

  const work = works.find((w) => w.id === passage.work_id);
  const all = getPassages();
  const idx = all.findIndex((p) => p.id === id);
  const neighbors = {
    previous: idx > 0 ? all[idx - 1] : null,
    next: idx >= 0 && idx < all.length - 1 ? all[idx + 1] : null,
  };

  // tracked terms: pull the ledger senses for a small set of core technical lemmas
  const CORE_LEMMAS = ["kula", "krama", "sakti", "khecari", "vimarsa", "prakasa", "spanda", "samvit", "visarga", "matrka", "uccara", "avesa", "sunya", "paramarsa", "svatantrya"];
  const tracked_terms = CORE_LEMMAS.map((l) => {
    const t = getTerm(l);
    return t ? { lemma: l, senses: t.senses, preferred_renderings: t.preferred_renderings } : null;
  }).filter(Boolean);

  return NextResponse.json({
    passage,
    work: work ? { id: work.id, urn: work.urn, title: work.title, traditions: work.traditions, date: work.date, translation_status: work.translation_status, research_roles: work.research_roles, rights: work.rights } : null,
    manuscripts: work ? manuscriptsForWork(work.id).map((m) => ({ id: m.id, title: m.title, catalogueIds: m.catalogueIds, script: m.script, provenanceCategory: m.provenanceCategory, dateOriginal: m.dateOriginal, folios: m.folios, source_url: m.source_url })) : [],
    neighboring: neighbors,
    tracked_terms,
    related_works: work ? relationsFor(work.id) : [],
    translations: {
      note: "Our working (T1) translations for the work; see /api/texts/:work_id/translations. Provisional, not peer reviewed.",
    },
    provenance: {
      note: "Deterministic evidence bundle. No generated interpretation; every element resolves to a source. Manuscripts are OCHS witnesses (custodian), CC BY-NC-SA 4.0.",
      api_version: "1.0",
    },
  });
}
