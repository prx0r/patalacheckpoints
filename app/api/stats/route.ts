// GET /api/stats — corpus credibility signals (northstar: measure adoption by
// data depth, not page views). Works, passages, manuscript witnesses, terms,
// working translations, resolved works.

import { NextRequest, NextResponse } from "next/server";
import { works } from "@/data/corpus/works";
import { getPassages, workingTranslationCounts } from "@/data/corpus/passages";
import { getManuscripts, workManuscriptCounts } from "@/data/corpus/manuscripts";
import { getTerms, getProposals } from "@/data/corpus/terms";
import { getAssertions, getReviews, getCrosswalks } from "@/data/corpus/primitives";

export async function GET(_req: NextRequest) {
  const passages = getPassages();
  const passagesWithTranslation = passages.filter((p) => p.close_translation).length;
  const wtrans = workingTranslationCounts();
  const msCounts = workManuscriptCounts();
  const worksWithManuscripts = Object.keys(msCounts).length;
  const worksWithTranslations = Object.keys(wtrans).length;

  const assertions = getAssertions();
  const reviews = getReviews();

  return NextResponse.json({
    works: works.length,
    works_verified: works.filter((w) => w.verified).length,
    works_with_manuscripts: worksWithManuscripts,
    works_with_working_translations: worksWithTranslations,
    passages: passages.length,
    passages_with_working_translation: passagesWithTranslation,
    manuscript_witnesses: getManuscripts().length,
    accepted_terms: getTerms().length,
    term_proposals: getProposals().length,
    primitives: {
      assertions: assertions.length,
      assertions_with_evidence: assertions.filter((a) => a.evidence.length > 0).length,
      assertions_reviewed: assertions.filter((a) => a.review_events.length > 0).length,
      reviews: reviews.length,
      crosswalks: getCrosswalks().length,
    },
    provenance: { note: "Deterministic counts over the current dataset. Primitives = evidence-coverage & review-depth signals (nextdev: raw facts over synthetic scores).", api_version: "1.0" },
  });
}
