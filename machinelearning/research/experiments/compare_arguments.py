#!/usr/bin/env python3
"""compare_arguments.py — the comparison harness (which builder is better, which metrics are real).

For each builder × theme, produces an ArgumentProposal and scores it on structural metrics +
(for the ground-truth theme) a comparison against the human argument. This answers:
  1. Which builder produces the most defensible argument?
  2. Which metrics actually correlate with ground-truth quality (vs. which are noise)?

Run: cd research && . .venv/bin/activate && python experiments/compare_arguments.py
"""
from __future__ import annotations
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.builders import BUILDERS
from patala_ml.c1corpus import load_c1_nodes
from patala_ml.argument import from_logical_argument_file


def load_themes():
    """The 6 real theme-clusters (size>=3) from clusters.json."""
    d = json.load(open("/root/projects/patala/data/published/ipvv/clusters.json"))
    return [c for c in d["clusters"] if c["size"] >= 3]


# ── structural metrics ───────────────────────────────────────────────────────
def resolve_ok(arg):
    """Every premise claim has a passage_id or a resolvable target."""
    return all(c.source_ok for c in arg.premise_claims) if hasattr(arg, "premise_claims") else True


def resolvability(arg):
    if not arg.premise_claims:
        return 0.0
    with_pass = sum(1 for c in arg.premise_claims if c.argument_targets)
    return with_pass / len(arg.premise_claims)


def premise_diversity(arg):
    """Distinct premise claim_texts (semantic spread) — how many distinct premises, not targets."""
    texts = set(c.claim_text for c in arg.premise_claims if c.claim_text.strip())
    return min(1.0, len(texts) / 3.0)


def coverage(arg, theme_members):
    """% of the theme's member C1s represented among the premise claims.

    A premise claim covers a member if the member's short id (e.g. 'v2o') appears in the
    claim_text or claim_id of that premise (normalized: v2o -> 2o to match chunkV2-O).
    """
    if not theme_members or not arg.premise_claims:
        return 0.0
    member_short = {m.split("-")[0].lower() for m in theme_members if m.split("-")[0]}
    covered = set()
    for c in arg.premise_claims:
        blob = (c.claim_text + " " + c.claim_id).lower()
        for ms in member_short:
            # v2o -> also try 2o (chunkV2-O has a V prefix)
            stripped = ms.replace("v", "", 1) if ms.startswith("v") else ms
            if ms and (ms in blob or stripped in blob):
                covered.add(ms)
    return round(len(covered) / len(member_short), 3)


def certainty(arg):
    return arg.aggregate_strength.get("certainty", "uncertain") if arg.aggregate_strength else "uncertain"


# ── ground-truth comparison ──────────────────────────────────────────────────
LOAD_BEARING = ["reflexiv", "self", "vimarśa", "universal", "intrinsic", "awareness"]


def gt_overlap(arg):
    """How many load-bearing concepts of the human argument appear in this builder's premises."""
    text = " ".join(m.text.lower() for m in arg.members)
    return round(sum(1 for w in LOAD_BEARING if w in text) / len(LOAD_BEARING), 3)


def scheme_match(arg):
    """Does the builder's scheme match the human's (reductio/debate)?"""
    return 1.0 if arg.inference_scheme == "REDUCTIO" else 0.0


def main():
    c1nodes = load_c1_nodes()
    themes = load_themes()
    print(f"{len(themes)} themes × {len(BUILDERS)} builders = {len(themes)*len(BUILDERS)} arguments\n")

    # the ground-truth theme is the reflexivity family (CL-3 order-less support) — compare against
    # the human reflexivity-debate argument
    gt = from_logical_argument_file(
        "/root/projects/research-library/LOGICAL-ARGUMENT-1-reflexivity-debate.md",
        "ipvv", "pt:argument:ipvv:reflexivity-debate")

    rows = []
    for builder_name, builder_fn in BUILDERS.items():
        for theme in themes:
            tid = theme["cluster_id"]
            arg = builder_fn(
                theme["member_c1_ids"], c1nodes,
                f"pt:argument:ipvv:{tid}", "ipvv", f"Theme {tid}")
            rows.append({
                "builder": builder_name, "theme": tid,
                "n_members": len(arg.members),
                "resolvability": resolvability(arg),
                "diversity": premise_diversity(arg),
                "coverage": coverage(arg, theme["member_c1_ids"]),
                "certainty": certainty(arg),
                "gt_overlap": gt_overlap(arg) if tid in ("CL-3", "CL-0") else None,
                "scheme_match": scheme_match(arg) if tid in ("CL-3", "CL-0") else None,
            })

    # report
    print(f"{'builder':10} {'theme':7} {'n':>2} {'resolv':>6} {'div':>5} {'cov':>5} {'cert':>10} {'gtOv':>5} {'gtSc':>5}")
    for r in sorted(rows, key=lambda x: (x["builder"], x["theme"])):
        print(f"{r['builder']:10} {r['theme']:7} {r['n_members']:2} "
              f"{r['resolvability']:6.2f} {r['diversity']:5.2f} {r['coverage']:5.2f} "
              f"{r['certainty']:>10} "
              f"{r['gt_overlap'] if r['gt_overlap'] is not None else '-':>5} "
              f"{r['scheme_match'] if r['scheme_match'] is not None else '-':>5}")

    # aggregate per builder
    print("\n=== per-builder aggregate (avg over themes) ===")
    from collections import defaultdict
    agg = defaultdict(lambda: {"resolv": [], "div": [], "cov": [], "gt": []})
    for r in rows:
        a = agg[r["builder"]]
        a["resolv"].append(r["resolvability"]); a["div"].append(r["diversity"])
        a["cov"].append(r["coverage"])
        if r["gt_overlap"] is not None:
            a["gt"].append(r["gt_overlap"])
    for b, a in agg.items():
        avg = lambda x: round(sum(x) / len(x), 3) if x else 0
        print(f"{b:10} resolv={avg(a['resolv'])} div={avg(a['div'])} cov={avg(a['cov'])} "
              f"gt_overlap={avg(a['gt'])}")

    # the "which metrics are real" question:
    print("\n=== which metrics correlate with ground-truth quality? ===")
    print("(on the ground-truth themes, does a metric rank the builder that gt_overlap ranks best?)")
    # correlate each metric against gt_overlap across the ground-truth rows
    gt_rows = [r for r in rows if r["gt_overlap"] is not None]
    if gt_rows:
        import statistics
        for metric in ["resolvability", "diversity", "coverage"]:
            xs = [r[metric] for r in gt_rows]
            ys = [r["gt_overlap"] for r in gt_rows]
            if len(set(xs)) > 1 and len(set(ys)) > 1:
                # simple rank-correlation
                sx = {v: i for i, v in enumerate(sorted(set(xs)))}
                sy = {v: i for i, v in enumerate(sorted(set(ys)))}
                rx = [sx[v] for v in xs]; ry = [sy[v] for v in ys]
                n = len(rx)
                rho = 1 - (6 * sum((a - b) ** 2 for a, b in zip(rx, ry))) / (n * (n * n - 1))
                print(f"  {metric} vs gt_overlap: spearman≈{rho:+.2f} "
                      f"({'meaningful' if abs(rho) > 0.5 else 'weak/bs'})")
            else:
                print(f"  {metric} vs gt_overlap: (insufficient variance to correlate)")
        # save
        with open("/root/projects/patala/data/published/ipvv/argument_comparison.json", "w") as f:
            json.dump(rows, f, indent=2)
        print("\nsaved data/published/ipvv/argument_comparison.json")


if __name__ == "__main__":
    main()
