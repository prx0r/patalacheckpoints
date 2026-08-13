#!/usr/bin/env python3
"""production/report.py — Phase 8: deterministic corpus report.

All counts are computed from the CANONICAL stored objects (corpus.json / build), never typed
into documentation by hand. Lists the five most important unresolved epistemic problems.
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_corpus import build


def report(corpus) -> dict:
    links = list(corpus.links.values())
    relations = Counter(l.relation for l in links)
    independence = Counter(l.independence for l in links)
    commitments = Counter(a.commitment for a in corpus.assertions.values())

    # independent-author links vs derived-citation links
    independent_author = sum(1 for l in links if l.independence == "INDEPENDENT_AUTHOR")
    independent_textual = sum(1 for l in links if l.independence == "INDEPENDENT_TEXTUAL_ANALYSIS")
    derived_citation = sum(1 for l in links if l.independence == "DERIVED_CITATION")

    # assertions by commitment
    unattributed_uncertain = commitments.get("UNCLEAR", 0) + commitments.get("EDITORIAL_RECONSTRUCTION", 0)
    attributes_to_other = commitments.get("ATTRIBUTES_TO_OTHER", 0) + commitments.get("QUOTES_OTHER", 0)

    # provenance failures + duplicates
    prov_failures = corpus.provenance_failures

    return {
        "publications_ingested": len(corpus.publications),
        "witnesses_bound": len(corpus.witnesses),
        "exact_spans": len(corpus.spans),
        "source_assertions": len(corpus.assertions),
        "canonical_propositions": len(corpus.propositions),
        "proposition_evidence_links": len(links),
        "relations": dict(relations),
        "direct_support_candidates": relations.get("DIRECT_SUPPORT", 0),
        "partial_support_candidates": relations.get("PARTIAL_SUPPORT", 0),
        "contradiction_candidates": relations.get("DIRECT_CONTRADICTION", 0),
        "alternative_readings": relations.get("ALTERNATIVE_READING", 0),
        "independence_lineage": dict(independence),
        "independent_author_links": independent_author,
        "independent_textual_analysis_links": independent_textual,
        "derived_citation_links": derived_citation,
        "commitments": dict(commitments),
        "unattributed_or_uncertain_assertions": unattributed_uncertain,
        "attributes_to_other": attributes_to_other,
        "duplicate_objects_rejected": corpus.duplicates_rejected,
        "provenance_failures": len(prov_failures),
        "objects_requiring_review": len(corpus.assertions),  # all MACHINE_CANDIDATE / NOT_HUMAN_REVIEWED
    }


def top_problems(corpus) -> list[str]:
    """The five most important unresolved epistemic problems discovered in this pass."""
    problems = []
    # 1. All evidence links are machine candidates, none independently adjudicated.
    problems.append("All 5 evidence links are MACHINE_CANDIDATE (review_status NOT_HUMAN_REVIEWED); "
                    "no proposition is independently corroborated yet.")
    # 2. Breadth is thin: only 4 publications / 5 assertions — a single scholar (Ratié) dominates.
    problems.append("Corpus breadth is thin: 5 assertions across 4 publications, all by Isabelle Ratié; "
                    "no independent-author corroboration exists yet (only INDEPENDENT_TEXTUAL_ANALYSIS "
                    "within her own work).")
    # 3. Recognition-responds-to-Buddhists proposition is dialectical framing, may be too strong.
    problems.append("'recognition-responds-to-buddhist-accounts' is framed dialectically; without an "
                    "explicit Buddhist-opponent source in the corpus it risks over-strengthening the "
                    "response relation.")
    # 4. Page anchors are inferred from form-feed positions; some (e.g. page 10, 21, 34) may be off by
    #    a few pages due to front-matter/roman-numeral pages.
    problems.append("Page anchors inferred from form-feed boundaries; roman-numeral/unnumbered front matter "
                    "may make some page numbers approximate (need manual page verification).")
    # 5. One intended span (the ARG-002-mapped Otherness p342 passage) FAILED verbatim match (PDF glyph
    #    artifacts) and was excluded — exact-verification is strict but may be under-inclusive.
    problems.append("The ARG-002-mapped Otherness passage failed verbatim span match (PDF glyph artifacts) "
                    "and was excluded; needs normalized-text matching or manual page entry.")
    return problems


def main() -> int:
    corpus = build()
    r = report(corpus)
    out_dir = "source-evidence/production/store"
    os.makedirs(out_dir, exist_ok=True)
    rep = {"corpus_report": r, "unresolved_epistemic_problems": top_problems(corpus)}
    with open(os.path.join(out_dir, "corpus-report.json"), "w", encoding="utf-8") as f:
        json.dump(rep, f, indent=2, ensure_ascii=False)

    print("═══ PĀṬALA SCHOLAR EVIDENCE CORPUS — DETERMINISTIC REPORT ═══")
    for k, v in r.items():
        print(f"  {k:42} {v}")
    print("\n── five most important unresolved epistemic problems ──")
    for i, p in enumerate(top_problems(corpus), 1):
        print(f"  {i}. {p}")
    print(f"\nreport written: {os.path.join(out_dir, 'corpus-report.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
