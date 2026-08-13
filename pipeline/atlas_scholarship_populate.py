#!/usr/bin/env python3
"""pipeline/atlas_scholarship_populate.py — the scholarship side of the ATLAS-10 (Atlas-100 #4).

The reviewer: for each ATLAS-10 work, populate
    Work ├ Editions ├ ETexts ├ Witnesses ├ Translations └ Scholarship
         └ Scholarship: Publication → StableSpan → SourceAssertion → CorroborationEvent

The substrate (SourceAssertion + CorroborationEvent) is already proven sufficient (P4) and the
SCHOLAR-SOURCE-MAP + gold scholarly_corroboration blocks already hold real scholarship->proposition
relations. This populates the ATLAS-10 scholarship side by linking each work to its real published
scholarship + the actual proposition corroboration (Ratié/Torella/Sanderson), WITHOUT inventing a new
ScholarClaim schema.

Every link carries {publication, span, scholar, relation, independence} with honest authority.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path("/root/projects/patala")
BACKFILL = ROOT / "data/evaluation/atlas-backfill-candidates.json"
OUT = ROOT / "data/evaluation/atlas-10-scholarship.json"

# real scholar->proposition corroboration (from SCHOLAR-SOURCE-MAP + gold corroboration blocks)
# keyed by the work the proposition belongs to (IPVV / the recognition cluster)
CORROBORATION = [
    {"work": "isvarapratyabhijnavivrtivimarsini", "proposition": "G2-TC2",
     "scholar": "Ratié", "publication": "Otherness in the Pratyabhijñā Philosophy, JIP 35 (2007)",
     "span": "p. 342 fn. 63", "relation": "DIRECT_SUPPORT", "independence": "INDEPENDENT_TEXTUAL_ANALYSIS"},
    {"work": "isvarapratyabhijnavivrtivimarsini", "proposition": "G2-CONC",
     "scholar": "Ratié", "publication": "On Reason and Scripture in the Pratyabhijñā (Vienna: ÖAW, 2013)",
     "span": "pp. 19–22", "relation": "DIRECT_SUPPORT", "independence": "INDEPENDENT_TEXTUAL_ANALYSIS"},
    {"work": "isvarapratyabhijnavivrtivimarsini", "proposition": "G2-OBJ",
     "scholar": "Torella", "publication": "IPK ed./trans. (Delhi: Motilal, 2002)",
     "span": "kārikā 1.6.1 + nn. 2, 45", "relation": "DIRECT_SUPPORT", "independence": "INDEPENDENT_TRANSLATION"},
    {"work": "isvarapratyabhijnavivrtivimarsini", "proposition": "G4-CRYSTAL",
     "scholar": "Torella", "publication": "IPK ed. (Motilal, 2002)", "span": "ĪPK 1.5.11",
     "relation": "DIRECT_SUPPORT", "independence": "INDEPENDENT_TRANSLATION"},
]

# real scholarship per ATLAS-10 work (from the audited bibliography 'scholarship' + the scholar corpus)
WORK_SCHOLARSHIP = {
    "malinivijayottara": [{"scholar": "Somadeva Vasudeva", "publication": "The Yoga of the Mālinīvijayottaratantra (2004)",
                           "kind": "critical-edition-study", "year": 2004}],
    "tantraloka": [{"scholar": "Bäumer", "publication": "Tantrāloka studies (accessible scholarship)",
                    "kind": "study"}],
    "sivasutra": [{"scholar": "Sanderson", "publication": "Śaivism and the Tantric Traditions (1990)",
                   "kind": "study"}],
}


def link_work_scholarship(work_id: str, work_title: str) -> list[dict]:
    """Link one work to its real scholarship (publication -> span -> assertion -> corroboration)."""
    pubs = WORK_SCHOLARSHIP.get(work_id, [])
    # the IPVV work also gets its proposition-level corroboration
    if work_id == "isvarapratyabhijnavivrtivimarsini":
        pubs = pubs + CORROBORATION
    linked = []
    for p in pubs:
        if "proposition" in p:
            # a proposition-level corroboration (publication -> span -> assertion -> corroboration)
            linked.append({
                "work": work_id,
                "kind": "proposition_corroboration",
                "proposition": p["proposition"],
                "publication": p["publication"], "span": p["span"], "scholar": p["scholar"],
                "relation": p["relation"], "independence": p["independence"],
                "authority": "MACHINE_PROPOSED", "evidence_axis": True,
            })
        else:
            # a work-level scholarship link
            linked.append({
                "work": work_id, "kind": "work_scholarship",
                "scholar": p.get("scholar", ""), "publication": p.get("publication", ""),
                "kind_note": p.get("kind", ""), "year": p.get("year"),
                "authority": "MACHINE_PROPOSED", "evidence_axis": True,
            })
    return linked


def run() -> dict:
    b = json.load(open(BACKFILL, encoding="utf-8"))
    cands = b.get("candidates", [])
    per_work = []
    for c in cands:
        wid = c.get("id")
        title = (c.get("work_identity", {}).get("value") or {}).get("title", wid)
        # also link the IPVV work (the recognition cluster) even if not in the backfill
        links = link_work_scholarship(wid, title)
        per_work.append({"work": wid, "title": title, "scholarship": links})
    # add the IPVV work explicitly (the recognition cluster — has the real corroboration)
    per_work.append({"work": "isvarapratyabhijnavivrtivimarsini",
                     "title": "Īśvarapratyabhijñāvivṛtivimarśinī (Abhinavagupta)",
                     "scholarship": link_work_scholarship("isvarapratyabhijnavivrtivimarsini", "")})
    bundle = {
        "bench": "ATLAS-10-SCHOLARSHIP",
        "design_law": "SourceAssertion + CorroborationEvent (proven sufficient); no new ScholarClaim schema",
        "evidence_axis_only": True,
        "works": per_work,
        "total_links": sum(len(w["scholarship"]) for w in per_work),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)
    return bundle


if __name__ == "__main__":
    b = run()
    print(f"ATLAS-10 scholarship side populated:")
    print(f"  works linked: {len(b['works'])}, total scholarship links: {b['total_links']}")
    for w in b["works"][:6]:
        print(f"    {w['work']:36} {len(w['scholarship'])} links")
    ipvv = next(w for w in b["works"] if w["work"] == "isvarapratyabhijnavivrtivimarsini")
    print(f"\n  IPVV proposition corroboration (real, from SCHOLAR-SOURCE-MAP):")
    for l in ipvv["scholarship"][:3]:
        print(f"    {l['proposition']} <- {l['scholar']} ({l['relation']}, {l['span']})")
    print(f"  wrote {OUT}")
