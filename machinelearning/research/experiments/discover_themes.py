#!/usr/bin/env python3
"""discover_themes.py — run theme discovery over the IPVV/C1 corpus (recall-first, v0).

Test bed is the IPVV/C1 material (not a generic essay yet): we have known key terms, existing clusters,
adjudication candidates, and source-linked C1s. The first benchmark question:
  "Given the known IPVV material, does the pipeline recover the three current candidates (Order-less
   Support / Vimarśa / Pramāṇa) PLUS plausible additional candidates, while exposing uncovered passages?"

Output is a ThemeDiscoveryResult + a coverage/overlap audit, saved as JSON.

Run: cd research && . .venv/bin/activate && python experiments/discover_themes.py
"""
from __future__ import annotations
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.theme_discovery import discover_themes, DEFAULT_LEXICON

C1_DIR = "/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/c1/read"
OUT = "/root/projects/patala/benchmarks/v0/theme-discovery-ipvv-v0.json"

# the three adjudication targets -> the key lemma that should surface them
TARGETS = {
    "Order-less Support": "order-less",
    "Vimarśa": "vimarśa",
    "Pramāṇa": "pramāṇa",
}


def load_c1_doc() -> str:
    parts = []
    for p in sorted(glob.glob(os.path.join(C1_DIR, "c1_*.md"))):
        name = os.path.basename(p)
        body = " ".join(l.lstrip("> ").strip() for l in open(p, encoding="utf-8")
                        if l.strip().startswith(">"))
        parts.append(f"{name}\n\n{body}")
    return "\n\n".join(parts)


def main():
    doc = load_c1_doc()
    res = discover_themes(doc, lexicon=DEFAULT_LEXICON)
    cov = res["coverage"]
    cands = res["candidate_objects"]

    print("THEME DISCOVERY v0 — IPVV/C1 (MACHINE_PROPOSED)\n")
    print(f"segments: {cov['n_segments']}  candidates: {len(cands)}")
    print(f"COVERAGE: {cov['assigned_pct']*100:.0f}% assigned ({cov['n_assigned']}/{cov['n_segments']}), "
          f"{cov['n_unassigned']} unassigned, {cov['n_multi_assigned']} multi-assigned, "
          f"{cov['n_unstable_sense_groups']} unstable-sense groups")

    print("\nTARGET RECOVERY (did the three candidates surface?):")
    for name, lemma in TARGETS.items():
        hit = [c for c in cands if lemma.lower() in c["label"].lower()]
        print(f"  {name:<20} key='{lemma}': {'FOUND -> ' + hit[0]['candidate_id'] if hit else 'NOT RECOVERED'}")

    print("\nTOP CANDIDATES (by member count):")
    for c in sorted(cands, key=lambda x: -len(x["member_segments"]))[:12]:
        print(f"  {c['candidate_id']:<18} n={len(c['member_segments']):<3} "
              f"kind={c['suspected_kind']:<24} sense={c['sense_stability']}")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(res, open(OUT, "w"), indent=2, ensure_ascii=False)
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
