#!/usr/bin/env python3
"""eval_p3_lexical.py — evaluate P3 lexical-sense methods against the gold benchmark.

Methods (benchmark-first — ranker.py is a CANDIDATE, not a verifier):
  baseline_most_common  always the corpus-dominant gloss for the lemma
  baseline_local_l0     the fixture's own L0 gloss (identity — measures how much gold
                        already encodes the answer)
  baseline_embedding    simple lexical-overlap / normalized-token match (no model yet)
  ranker_candidate      the old engine's rank_senses() (reused, audited)

Metrics (per the review):
  top1_accuracy    accepted sense ranked first
  top3_recall      accepted sense in top-3
  mrr
  abstention_quality   did it abstain (no unique sense) when the gold says OPEN?
  technical_term_accuracy  correct only on the technical-stable fixtures
  false_certainty_rate     how often it committed to a sense when gold is OPEN

Usage:
  python3 pipeline/eval_p3_lexical.py --gold docs/p3_lexical_gold_v0.json [--ranker]
"""
from __future__ import annotations
import argparse
import json
import sys
from collections import Counter


def norm(s: str) -> str:
    return s.lower().strip().replace("-", " ")


def score_topk(predicted: list[str], preferred: str) -> tuple[bool, bool, float]:
    """Returns (top1_ok, top3_ok, reciprocal_rank)."""
    if not preferred or not predicted:
        return False, False, 0.0
    r = norm(preferred)
    for i, p in enumerate(predicted):
        if norm(p) == r or r in norm(p) or norm(p) in r:
            return (i == 0, i < 3, 1.0 / (i + 1))
    return False, False, 0.0


# --------------------------------------------------------------------------- #
# baselines
# --------------------------------------------------------------------------- #
def baseline_most_common(fixture, corpus_gloss):
    """Always predict the most frequent sense for the lemma (no context)."""
    lemma = fixture["lemma"]
    top = corpus_gloss.get(lemma)
    if not top:
        return [fixture["candidate_senses"][0] if fixture["candidate_senses"] else "?"]
    # map dominant L0 gloss to a candidate sense by token overlap
    best = None
    for c in fixture["candidate_senses"]:
        if norm(top) == norm(c) or norm(top) in norm(c) or norm(c) in norm(top):
            best = c
            break
    if best is None:
        best = fixture["candidate_senses"][0] if fixture["candidate_senses"] else "?"
    return [best]


def baseline_local_l0(fixture, corpus_gloss):
    """Predict from the fixture's own L0 gloss (the identity leak measure)."""
    surface = fixture["surface"]
    for c in fixture["candidate_senses"]:
        if norm(c) in norm(surface) or norm(surface) in norm(c):
            return [c]
    return [fixture["candidate_senses"][0] if fixture["candidate_senses"] else "?"]


def baseline_embedding(fixture, corpus_gloss, **kw):
    """Simple lexical-overlap ranking (no model — a placeholder for real embeddings later)."""
    surface = norm(fixture["surface"])
    scored = []
    for c in fixture["candidate_senses"]:
        nc = norm(c)
        # overlap of significant tokens
        toks = set(nc.split()) & set(surface.split())
        score = len(toks) + (0.5 if nc in surface else 0.0)
        scored.append((c, score))
    scored.sort(key=lambda x: -x[1])
    return [c for c, _ in scored]


def ranker_candidate(fixture, corpus_gloss, **kw):
    """Run the old engine's rank_senses (audited candidate). May be None if ranker not available."""
    try:
        sys.path.insert(0, "/mnt/HC_Volume_106427611/sanskritree/src")
        from sanskritree.evidence.ranker import rank_senses
        ranked = rank_senses(fixture["lemma"], [fixture["lemma"]], "ipvv")
        # map RankedSense.gloss to candidate senses
        out = []
        for rs in ranked:
            for c in fixture["candidate_senses"]:
                if norm(rs.gloss) == norm(c) or norm(rs.gloss) in norm(c) or norm(c) in norm(rs.gloss):
                    if c not in out:
                        out.append(c)
            if len(out) >= 3:
                break
        # ensure non-empty
        if not out and fixture["candidate_senses"]:
            out = [fixture["candidate_senses"][0]]
        return out
    except Exception as e:
        return [f"RANKER_ERR:{e}"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", required=True)
    ap.add_argument("--ranker", action="store_true", help="include ranker_candidate (may be slow)")
    ap.add_argument("--corpus", default="/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/l0",
                    help="l0 dir to compute corpus-dominant gloss per lemma")
    args = ap.parse_args()

    gold = json.load(open(args.gold))
    fixtures = gold["fixtures"]

    # corpus-dominant gloss per lemma (for the most-common baseline)
    corpus_gloss = Counter()
    import glob
    for f in glob.glob(args.corpus + "/*.l0.jsonl"):
        for line in open(f, encoding="utf-8"):
            r = json.loads(line)
            lem = r.get("lemma_iast", ""); g = r.get("literal_gloss", "")
            if lem and g:
                corpus_gloss[(lem, g)] += 1
    dom = {}
    lemma_gloss = {}
    for (lem, g), n in corpus_gloss.items():
        if lem not in lemma_gloss or n > corpus_gloss.get((lem, lemma_gloss[lem]), 0):
            lemma_gloss[lem] = g
            dom[lem] = g

    methods = {
        "baseline_most_common": baseline_most_common,
        "baseline_local_l0": baseline_local_l0,
        "baseline_embedding": baseline_embedding,
    }
    if args.ranker:
        methods["ranker_candidate"] = ranker_candidate

    report = {}
    for mname, fn in methods.items():
        top1 = top3 = mrr_sum = 0
        abstain_ok = abstain_total = 0
        tech_ok = tech_total = 0
        false_cert = 0
        n = 0
        for fi in fixtures:
            n += 1
            predicted = fn(fi, dom) if mname != "ranker_candidate" else fn(fi, dom)
            if isinstance(predicted[0], str) and predicted[0].startswith("RANKER_ERR"):
                continue
            t1, t3, rr = score_topk(predicted, fi["preferred"])
            top1 += int(t1); top3 += int(t3); mrr_sum += rr
            # abstention: gold is OPEN (preferred None) — correct = predict nothing / abstain
            if fi["preferred"] is None:
                abstain_total += 1
                # a correct abstention = the method returned no confident single sense
                if len(predicted) == 0 or (len(predicted) >= 2 and len(set(predicted)) >= 2):
                    abstain_ok += 1
                else:
                    false_cert += 1
            # technical-term accuracy: any fixture whose lemma is in the technical set
            if fi["lemma"] in ("vimarśa", "pratibhā", "prakāśa", "saṃvid", "pramātṛ",
                               "ābhāsa", "svātantrya", "krama", "śakti", "jñāna"):
                tech_total += 1
                tech_ok += int(t1)
        denom = max(n, 1)
        report[mname] = {
            "n": n,
            "top1_accuracy": round(top1 / denom, 4),
            "top3_recall": round(top3 / denom, 4),
            "mrr": round(mrr_sum / denom, 4),
            "abstention_quality": round(abstain_ok / max(abstain_total, 1), 4),
            "abstain_cases": abstain_total,
            "technical_term_accuracy": round(tech_ok / max(tech_total, 1), 4),
            "tech_cases": tech_total,
            "false_certainty_rate": round(false_cert / max(abstain_total, 1), 4),
        }
        print(f"\n=== {mname} ===")
        for k, v in report[mname].items():
            print(f"  {k:28s} {v}")

    print("\n=== comparison (top1 / mrr / abstain) ===")
    for mname in methods:
        r = report.get(mname, {})
        print(f"  {mname:22s} top1={r.get('top1_accuracy'):<6} mrr={r.get('mrr'):<6} "
              f"abstain={r.get('abstention_quality')} false_cert={r.get('false_certainty_rate')}")

    with open("docs/p3_lexical_eval_report.json", "w", encoding="utf-8") as fh:
        json.dump({"benchmark": "P3-LEXICAL-SENSE-v0", "methods": report}, fh, indent=2)
    print("\nreport -> docs/p3_lexical_eval_report.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
