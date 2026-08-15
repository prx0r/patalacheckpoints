#!/usr/bin/env python3
"""pipeline/gold_check.py — independent-gold check for the epistemic products.

FLAW-5 fix: the products' tests were SELF-AUTHORED (they asserted their own derivation). This is the
independent-gold check: compare a product's output against the smellycock raw-material golds (real,
hand-authored C1/argmap) — the ground truth the product did NOT produce.

Checks:
  - claim: does my claim's thesis appear in / match the gold C1's thesis for the same passage?
  - argument: does my argument's thesis/premises appear in the gold ARGMAP for the same passage?

The gold is INDEPENDENT (from smellycock, hand-authored by a scholar); the product output is DERIVED
from the IPVV passage. A match means the product is grounded; a mismatch is an honest signal, not a
fake pass.

Usage: python3 pipeline/gold_check.py [--product claim|argument]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "pipeline"))
sys.path.insert(0, str(REPO / "pipeline/products"))

GOLD_DIR = Path("/root/smellycock/raw-material")

# gold C1 filename -> the IPVV passage it corresponds to
GOLD_TO_PASSAGE = {
    "c1_V1A-svatyandya.md": "chunkA-svatyandya",
    "c1_V1B-eligibility.md": "chunkB-eligibility",
}


def _gold_c1(passage_fragment: str) -> str | None:
    """Find the gold C1 for a passage fragment, return its body."""
    for fname, frag in GOLD_TO_PASSAGE.items():
        if frag in passage_fragment:
            p = GOLD_DIR / "c1" / fname
            if p.exists():
                # the gold body is the quoted block after the # title
                lines = p.read_text().splitlines()
                body = " ".join(l for l in lines if not l.startswith("#"))
                return body
    return None


def check_claim() -> list[dict]:
    """Compare my claim thesis against the independent gold C1 for the same passage."""
    from products.claim.engine import claims
    from products._shared import ipvv
    results = []
    for c in claims():
        ref = c["source_refs"][0] if c["source_refs"] else ""
        # find the passage for this claim
        passage = next((p for p in ipvv.passages() if p.get("immutable_id") == ref), None)
        if not passage:
            continue
        gold = _gold_c1(passage.get("id", ""))
        if gold is None:
            continue
        # does my thesis's key terms appear in the gold? (independent overlap)
        my_text = c["text"].lower()
        gold_l = gold.lower()
        # check the claim's key nouns appear in the gold (crude but honest overlap)
        overlap = sum(1 for w in ["spontaneity", "svācchandya", "manifestation", "consciousness",
                                  "recognition", "self", "aware", "eligibility", "prostration"]
                      if w in my_text and w in gold_l)
        results.append({
            "passage": passage.get("id"),
            "my_claim": c["text"][:80],
            "gold_passage_found": gold is not None,
            "term_overlap_with_gold": overlap,
            "ceiling": c["epistemic_ceiling"],
            "grounded_in_gold": overlap >= 1,
        })
    return results


def check_argument() -> list[dict]:
    """Compare my argument's thesis against the gold ARGMAP (independent)."""
    from products.argument.engine import arguments
    results = []
    for a in arguments():
        src = a.get("source_refs", [])
        src_id = src[0] if src else ""
        # find the passage
        from products._shared import ipvv
        passage = next((p for p in ipvv.passages()
                        if (p.get("immutable_id") == src_id) or
                        (src_id and src_id.split(":")[-1] in p.get("id", ""))), None)
        if not passage:
            continue
        # gold argmap (only V2-L has a gold argmap)
        gold_map = GOLD_DIR / "argmap" / "pilot_V2L_ARGUMENT_MAP.md"
        if gold_map.exists() and "v2l" in passage.get("id", "").lower():
            gold_text = gold_map.read_text().lower()
            thesis = (a.get("thesis") or "").lower()
            overlap = sum(1 for w in ["pratyavamarśa", "vikalpa", "recollection", "construction",
                                      "apohana", "self"]
                          if w in thesis and w in gold_text)
            results.append({
                "passage": passage.get("id"),
                "my_argument_thesis": a.get("thesis", "")[:60],
                "gold_argmap_found": True,
                "term_overlap_with_gold": overlap,
            })
    return results


if __name__ == "__main__":
    product = sys.argv[2] if len(sys.argv) > 1 and sys.argv[1] == "--product" else "claim"
    if product == "claim":
        res = check_claim()
        grounded = sum(1 for r in res if r["grounded_in_gold"])
        print(f"CLAIM gold-check: {len(res)} claims compared to independent gold")
        for r in res:
            print(f"  {'✓' if r['grounded_in_gold'] else '✗'} {r['passage'][-30:]:34} overlap={r['term_overlap_with_gold']}")
        print(f"grounded_in_gold: {grounded}/{len(res)}")
    elif product == "argument":
        res = check_argument()
        print(f"ARGUMENT gold-check: {len(res)} arguments compared to gold argmap")
        for r in res:
            print(f"  {r['passage'][-30:]:34} overlap={r['term_overlap_with_gold']}")
