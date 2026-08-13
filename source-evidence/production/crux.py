#!/usr/bin/env python3
"""production/crux.py — A7: package the highest-value disputed claims as review-ready cruxes.

A crux = a proposition whose epistemic status is contested or underdetermined, packaged with:
  - the exact proposition + why it matters
  - evidence FOR (supporting assertions/spans)
  - evidence AGAINST / qualifying (partial/alternative/contradiction)
  - what would resolve it (the adjudication question)
  - review status (MACHINE_CANDIDATE / NOT_HUMAN_REVIEWED)

Cruxes are SMALL, scholar-reviewable units — not big essays. They exist to surface the
genuinely disputed points for human/expert adjudication.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_corpus import build


def build_cruxes(corpus) -> list[dict]:
    """Select propositions with contested/qualified/alternative evidence and package them."""
    # propositions that have non-DIRECT_SUPPORT evidence, OR 2+ authors, are crux candidates
    links_by_prop = {}
    for l in corpus.links.values():
        links_by_prop.setdefault(l.prop_ref, []).append(l)

    crux_candidates = []
    for prop_id, links in links_by_prop.items():
        relations = {l.relation for l in links}
        authors = {corpus.assertions[l.assertion_ref].attributed_to.split(":")[-1] for l in links}
        contested = len(authors) >= 2 or any(
            r in ("PARTIAL_SUPPORT", "ALTERNATIVE_READING", "DIRECT_CONTRADICTION", "UNDERDETERMINED")
            for r in relations)
        if contested:
            crux_candidates.append(prop_id)

    cruxes = []
    for prop_id in crux_candidates:
        prop = corpus.propositions[prop_id]
        links = links_by_prop[prop_id]
        supporting = []
        qualifying = []
        for l in links:
            a = corpus.assertions[l.assertion_ref]
            s = corpus.spans[a.span_ref]
            ev = {
                "author": a.attributed_to.split(":")[-1],
                "relation": l.relation,
                "claim": a.claim,
                "quote": (s.quote or "")[:160],
                "page": s.page,
                "independence": l.independence,
            }
            if l.relation == "DIRECT_SUPPORT":
                supporting.append(ev)
            else:
                qualifying.append(ev)
        cruxes.append({
            "crux_id": f"pt:crux:{prop_id.split(':')[-1]}",
            "proposition": prop_id,
            "formulation": prop.formulation,
            "why_it_matters": prop.scope,
            "evidence_for": supporting,
            "evidence_qualifying_or_against": qualifying,
            "review_status": "NOT_HUMAN_REVIEWED",
            "adjudication_question": (
                f"Does the supporting evidence license the formulation as stated, or does the "
                f"{'qualifying' if qualifying else 'multi-author'} evidence require a qualification?"
            ),
        })
    return cruxes


def main() -> int:
    corpus = build()
    cruxes = build_cruxes(corpus)
    out_dir = "source-evidence/production/store"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "cruxes.json"), "w", encoding="utf-8") as f:
        json.dump(cruxes, f, indent=2, ensure_ascii=False)
    print("═══ SCHOLAR-REVIEWABLE CRUXES (A7) ═══")
    print(f"{len(cruxes)} disputed propositions packaged for review:\n")
    for c in cruxes:
        print(f"  ◆ {c['crux_id'].split(':')[-1]}")
        print(f"    {c['formulation'][:90]}")
        for e in c['evidence_for']:
            print(f"      FOR   {e['author']:14} ({e['relation']:16}) p.{e['page']}")
        for e in c['evidence_qualifying_or_against']:
            print(f"      QUAL  {e['author']:14} ({e['relation']:16}) p.{e['page']}")
        print()
    print(f"cruxes written: {os.path.join(out_dir, 'cruxes.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
