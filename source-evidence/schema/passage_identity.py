#!/usr/bin/env python3
"""source-evidence/schema/passage_identity.py — the PassageIdentity crosswalk (CANONICAL-GRAPH-1 P0).

The audit's #1 finding: two passage-ID systems coexist and don't resolve:
    published:  pt:passage:ipvv:chunkV2-A-<slug>.md        (49 passages)
    segmented:  tantra:text:...:V2-A:<slug>                (231 jsonl passages, 35 V-tags)

This is an explicit identity/crosswalk, NOT a rename. It maps every alias to ONE canonical Passage:

    PassageIdentity
        canonical_passage_id
        aliases[]
        source_segmentation_refs[]
        published_projection_refs[]

Invariant:
    resolve(any historical/current passage id) -> exactly one canonical Passage (unless genuinely
    ambiguous).

The V-tag (e.g. V2-A) is the shared key: published chunkV2-A-*.md and jsonl ...:V2-A:<slug> both carry it.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

ROOT = Path("/root/projects/patala")
PUBLISHED = ROOT / "data/published/ipvv/index.json"
JSONL = ROOT / "data/corpus/passages/isvarapratyabhijnavivrtivimarsini.jsonl"


def _vtags():
    """All distinct V-tags (V2-A..V3-P) from the segmented corpus."""
    if not JSONL.exists():
        return set()
    v = set()
    for line in open(JSONL, encoding="utf-8"):
        try:
            d = json.loads(line)
            m = re.search(r":(V\d+-?[A-Z]):", d.get("id", ""))
            if m:
                v.add(m.group(1))
        except Exception:
            continue
    return v


def build_crosswalk() -> dict:
    """Build the PassageIdentity map: V-tag -> {canonical, published_ids[], jsonl_ids[]}."""
    xw = {}
    # published store: pt:passage:ipvv:chunk<VTAG>-<slug>.md
    if PUBLISHED.exists():
        idx = json.load(open(PUBLISHED, encoding="utf-8"))
        for p in idx.get("passages", []):
            loc = p.get("locator", "")           # chunkV2-A-svatyandya.md
            m = re.match(r"chunk(V\d+-?[A-Z])", loc)
            if not m:
                continue
            tag = m.group(1)
            xw.setdefault(tag, {"canonical": f"pt:passage:ipvv:{tag}",
                                "published_ids": [], "jsonl_ids": []})
            xw[tag]["published_ids"].append(p.get("id", ""))
    # segmented corpus: tantra:text:...:<VTAG>:<slug>
    if JSONL.exists():
        for line in open(JSONL, encoding="utf-8"):
            try:
                d = json.loads(line)
            except Exception:
                continue
            mid = d.get("id", "")
            m = re.search(r":(V\d+-?[A-Z]):", mid)
            if not m:
                continue
            tag = m.group(1)
            xw.setdefault(tag, {"canonical": f"pt:passage:ipvv:{tag}",
                                "published_ids": [], "jsonl_ids": []})
            xw[tag]["jsonl_ids"].append(mid)
    # sort jsonl ids for determinism
    for v in xw.values():
        v["jsonl_ids"] = sorted(v["jsonl_ids"])
    return xw


def resolve(ref: str, crosswalk: dict | None = None) -> dict:
    """Resolve ANY passage reference to one canonical Passage. Returns {canonical, matched_on, ok}.

    Invariant: every id resolves. A published-only chunk (e.g. the V1/jñānādhikāra upoddhāta chunks
    chunkA..N with no jsonl segmentation) resolves to ITSELF as canonical, with jsonl_ids=[] — honest
    about coverage, never a failed resolution.
    """
    cw = crosswalk or build_crosswalk()
    # a published id like pt:passage:ipvv:chunkM-...md
    m = re.search(r"pt:passage:ipvv:(chunk[^-]+)", ref)
    if m:
        tag = m.group(1)  # e.g. 'chunkM'
        # if there's a V-tag variant, prefer the V-tag canonical
        vt = re.search(r"(V\d+-?[A-Z])", ref)
        if vt and vt.group(1) in cw:
            entry = cw[vt.group(1)]
            return {"ok": True, "canonical": entry["canonical"], "matched_on": vt.group(1),
                    "published_ids": len(entry["published_ids"]), "jsonl_ids": len(entry["jsonl_ids"])}
        # published-only chunk (V1 upoddhāta, no jsonl segmentation): canonical = itself
        return {"ok": True, "canonical": f"pt:passage:ipvv:{tag}",
                "matched_on": tag, "published_ids": 1, "jsonl_ids": 0,
                "note": "published-only projection (V1/jñānādhikāra); no segmented-corpus equivalent"}
    # a V-tag ref (jsonl or canonical)
    vt = re.search(r"(V\d+-?[A-Z])", ref)
    if vt:
        tag = vt.group(1)
        if tag in cw:
            entry = cw[tag]
            return {"ok": True, "canonical": entry["canonical"], "matched_on": tag,
                    "published_ids": len(entry["published_ids"]), "jsonl_ids": len(entry["jsonl_ids"])}
    return {"ok": False, "canonical": None, "matched_on": None, "reason": f"unresolvable ref {ref[:40]}"}


if __name__ == "__main__":
    cw = build_crosswalk()
    print(f"PassageIdentity crosswalk: {len(cw)} V-tags (V2-A..V3-P)")
    for tag in ["V2-A", "V2-L", "V3-M"]:
        e = cw.get(tag)
        if e:
            print(f"  {tag}: canonical={e['canonical']} published={len(e['published_ids'])} "
                  f"jsonl={len(e['jsonl_ids'])}")
    # test resolution of a published id + a jsonl id
    for ref in ["pt:passage:ipvv:chunkV2-L-sastho-vimarsa-smrti-apohana.md",
                "tantra:text:isvarapratyabhijnavivrtivimarsini:V2-A:The_fourth_vimar_a"]:
        r = resolve(ref, cw)
        print(f"  resolve({ref[:45]}...) -> {r['ok']} canonical={r['canonical']} on={r['matched_on']}")
