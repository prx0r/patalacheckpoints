#!/usr/bin/env python3
"""production/view.py — Phase 6: the scholarly evidence view (machine-readable first).

A proposition resolves to its real evidence:

    PROPOSITION
    ├── formulation / scope / modality / temporal_scope
    ├── Scholar A ── exact assertion/span
    ├── Scholar B ── exact assertion/span
    ├── alternative reading / contradiction / defeater
    ├── independence / lineage
    ├── scope notes / unresolved issues
    └── review status (MACHINE_CANDIDATE unless adjudicated)

Machine-readable (JSON) output; a thin renderable projection on top if cheap.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_corpus import build


def evidence_view(corpus) -> dict:
    """Build {prop_id: {evidence: [...]}} from the corpus."""
    view = {}
    # index spans/assertions by id for fast lookup
    spans = corpus.spans
    assertions = corpus.assertions
    witnesses = corpus.witnesses
    publications = corpus.publications

    for prop_id in corpus.propositions:
        prop = corpus.propositions[prop_id]
        entry = {
            "proposition_id": prop_id,
            "formulation": prop.formulation,
            "subject": prop.subject,
            "scope": prop.scope,
            "modality": prop.modality,
            "temporal_scope": prop.temporal_scope,
            "assumptions": prop.assumptions,
            "review_status": "MACHINE_CANDIDATE",
            "evidence": [],
            "alternative_readings": [],
            "contradictions": [],
            "defeaters": [],
            "unresolved": [],
        }
        for link in corpus.links.values():
            if link.prop_ref != prop_id:
                continue
            a = assertions.get(link.assertion_ref)
            if not a:
                entry["unresolved"].append(f"assertion_ref {link.assertion_ref} not in corpus")
                continue
            s = spans.get(a.span_ref)
            ev = {
                "relation": link.relation,
                "independence": link.independence,
                "review_state": link.review_state,
                "commitment": a.commitment,
                "attributed_to": a.attributed_to,
                "claim": a.claim,
                "span": {
                    "quote": s.quote if s else None,
                    "page": s.page if s else None,
                    "section": s.section if s else None,
                    "span_sha256": s.span_sha256 if s else None,
                    "witness_ref": s.witness_ref if s else None,
                },
            }
            # attach publication context from the witness
            if s and s.witness_ref in witnesses:
                wit = witnesses[s.witness_ref]
                pub = publications.get(wit.pub_ref)
                ev["publication"] = {"ref": wit.pub_ref,
                                     "title": pub.title if pub else None,
                                     "author": pub.author_name if pub else None,
                                     "year": pub.year if pub else None}
            if link.relation in ("ALTERNATIVE_READING",):
                entry["alternative_readings"].append(ev)
            elif link.relation in ("DIRECT_CONTRADICTION",):
                entry["contradictions"].append(ev)
            else:
                entry["evidence"].append(ev)
        view[prop_id] = entry
    return view


def render_view(corpus) -> str:
    """Human-readable text render of the evidence view (a thin projection)."""
    view = evidence_view(corpus)
    lines = []
    for prop_id, e in view.items():
        lines.append(f"\n══ PROPOSITION {prop_id.split(':')[-1]} ══")
        lines.append(f"  {e['formulation']}")
        if e.get("scope"):
            lines.append(f"  scope: {e['scope']}  |  modality: {e['modality']}")
        for ev in e["evidence"]:
            pub = ev.get("publication", {})
            lines.append(f"  • {ev['relation']} [{ev['independence']}] — {pub.get('author')} "
                         f"({pub.get('year')}) page {ev['span']['page']}")
            lines.append(f"      \"{ev['span']['quote']}\"")
            lines.append(f"      claim: {ev['claim']}")
        lines.append(f"  review_status: {e['review_status']}")
    return "\n".join(lines)


def main() -> int:
    corpus = build()
    import os
    out_dir = "source-evidence/production/store"
    view = evidence_view(corpus)
    with open(os.path.join(out_dir, "evidence-view.json"), "w", encoding="utf-8") as f:
        json.dump(view, f, indent=2, ensure_ascii=False)
    print(render_view(corpus))
    print(f"\nevidence view written: {os.path.join(out_dir, 'evidence-view.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
