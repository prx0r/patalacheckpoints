#!/usr/bin/env python3
"""run_c1metrics.py — score all 63 IPVV C1s against the machine metrics (Phase A1).

Proves the C1 contract on the gold standard: do the IPVV C1s pass the novelty / localness /
no-anachronism / boundary / hedge / term-quality thresholds? Where they fail, that's the
evidence for tuning the thresholds (the calibration corpus is the IPVV).

Run: cd research && . .venv/bin/activate && python experiments/run_c1metrics.py
"""
from __future__ import annotations
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.c1metrics import score_c1


def load_ipvv_c1s():
    """Load the 63 IPVV C1s: body (from read/), terms/related (from read/ header)."""
    c1dir = "/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/c1/read"
    out = []
    for f in sorted(glob.glob(os.path.join(c1dir, "c1_*.md"))):
        text = open(f, encoding="utf-8").read()
        body = " ".join(re.findall(r"\n> ?(.*)", text))
        terms_m = re.search(r"\*\*Terms:\*\*\s*(.*?)(?=\n\*\*|\Z)", text, re.S)
        see_m = re.search(r"\*\*See also:\*\*\s*(.+)", text)
        terms = [t.strip() for t in (terms_m.group(1) if terms_m else "").replace("·", "\n").split("\n") if t.strip()]
        see = [s.strip() for s in (see_m.group(1) if see_m else "").split("·") if s.strip()]
        # L2 for novelty: match the passage's L2 text via the store
        out.append({"id": os.path.basename(f).replace("c1_", "").replace(".md", ""),
                    "body": body, "terms": terms, "related": see,
                    "boundary": text})  # whole file as boundary context
    return out


def main():
    c1s = load_ipvv_c1s()
    print(f"scoring {len(c1s)} IPVV C1s\n")

    # load the passage L2 texts for novelty comparison
    store = "/root/projects/patala/data/published/ipvv"
    l2_by_id = {}
    for f in glob.glob(os.path.join(store, "pt-passage-*.json")):
        r = json.load(open(f))
        l2_by_id[r.get("chunk", "")] = r.get("l2_text", "") or ""

    results = []
    for c in c1s:
        # C1 id like 'V3M-states' or 'V2O-orderless' -> section 'V3M'/'V2O'; match the chunk
        # (chunkV3-M-... or chunkV2-O-...) by normalizing V3M <-> V3-M.
        short = c["id"].split("-")[0].upper()          # e.g. V3M, V2O, V1K
        norm_short = short.replace("V", "V").replace("V", "")  # -> 3M, 2O (strip leading V)
        l2, boundary_structured = "", ""
        for chunk, txt in l2_by_id.items():
            # normalize chunkV3-M-... -> 3M (remove 'chunk', 'V', '-')
            norm_chunk = re.sub(r"[^0-9A-Z]", "", chunk.upper())  # CHUNKV3MAGAMA... -> 3MAGAMA...
            if norm_chunk.startswith(norm_short) or norm_short in norm_chunk:
                l2 = txt
                break
        # find the structured boundary from the store (same match)
        for f in glob.glob(os.path.join(store, "pt-passage-*.json")):
            r = json.load(open(f))
            chunk = r.get("chunk", "")
            norm_chunk = re.sub(r"[^0-9A-Z]", "", chunk.upper())
            if norm_chunk.startswith(norm_short) or norm_short in norm_chunk:
                cs = r.get("c1_source") or {}
                boundary_structured = cs.get("boundary_/_open", "") or ""
                break
        boundary_text = boundary_structured or c["boundary"]
        s = score_c1(c["body"], l2, terms=c["terms"], related=c["related"], boundary_text=boundary_text)
        s["id"] = c["id"]
        results.append(s)

    # summary
    import statistics
    metrics = ["novelty", "no_anachronism", "boundary", "hedge", "term_quality", "localness"]
    print(f"{'C1':42} {'overall':>7}  passes")
    fails = []
    for r in results:
        mark = "✓" if r["passes"] else "✗"
        if not r["passes"]:
            fails.append(r)
        print(f"{r['id']:42} {r['overall']:7.2f}  {mark}")
        if not r["passes"]:
            bad = [k for k, v in r.items() if isinstance(v, dict) and not v.get("pass")]
            print(f"    fails: {bad}")

    print(f"\n=== {len(results) - len(fails)}/{len(results)} C1s pass the contract ===")
    if fails:
        print(f"{len(fails)} fail — the evidence for tuning thresholds:")
        from collections import Counter
        cnt = Counter()
        for r in fails:
            for k, v in r.items():
                if isinstance(v, dict) and not v.get("pass"):
                    cnt[k] += 1
        print("  failure counts by metric:", dict(cnt))


if __name__ == "__main__":
    main()
