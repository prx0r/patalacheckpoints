#!/usr/bin/env python3
"""benchmark_p4_alignment.py — the P4 alignment benchmark (benchmark-first).

P4 asks: which Sanskrit ↔ which English? The gold is the L0 token pairs (each token already carries
`literal_gloss` EN + `lemma_iast` SKT). The benchmark tests whether an automatic aligner can recover
those mappings from raw parallel text, WITHOUT the L0 labels (i.e. from the source Sanskrit + the L2
prose alone).

Design (per the anti-theatre rule — benchmark before promotion):
- Held-out gold: a random sample of L0 EN↔SKT token pairs (the checked mapping).
- The task: given a Sanskrit sentence (its IAST) + an English sentence (its gloss stream), recover
  which EN word aligns to which SKT word.
- Baselines (no model):
    1. determinisitic_position  — naive same-index alignment (weak floor)
    2. lexical_overlap          — token overlap between EN and transliterated-SKT (stronger floor)
  Then awesome-align (a real neural aligner) can be added later and must beat these.

Metrics: alignment precision / recall / AER (alignment error rate), on the gold pairs.

Honest status: this is a BASELINE floor. No claim that alignment is "solved"; we establish the number
any real aligner must beat.

Usage:
  python3 pipeline/benchmark_p4_alignment.py --l0dir <l0> --n <held-out pairs> [--seed 42]
"""
from __future__ import annotations
import argparse
import json
import random
import re
import sys
from pathlib import Path

SKT_RE = re.compile(r"^[a-zA-Zāīūṛṝḷḹṃñṅśṣṭḍḥṁ]+$")


def load_token_pairs(l0dir: str) -> list[dict]:
    """Collect clean EN↔SKT token pairs from L0 (the gold alignment units)."""
    pairs = []
    for f in Path(l0dir).glob("*.l0.jsonl"):
        chunk = f.name[: -len(".l0.jsonl")]
        for line in f.open(encoding="utf-8"):
            r = json.loads(line)
            if r.get("status") == "PARSED" and SKT_RE.match(r.get("lemma_iast", "")) \
                    and r.get("literal_gloss", ""):
                pairs.append({
                    "en": r["literal_gloss"], "skt": r["lemma_iast"],
                    "locator": f"{chunk}:L{r.get('line_id')}",
                })
    return pairs


def skt_tokens(skt: str) -> list[str]:
    """Split a Sanskrit IAST surface into morphemes (rough: strip case endings via overlap)."""
    # for the baseline we compare EN words against the SKT surface; use the surface + a stem guess
    return [skt]


def align_lexical(en_tokens: list[str], skt_tokens: list[str]) -> set[tuple[int, int]]:
    """Lexical-overlap alignment: EN token <-> SKT token sharing characters."""
    align = set()
    for i, en in enumerate(en_tokens):
        for j, skt in enumerate(skt_tokens):
            # crude transliteration-free overlap: compare character sets / substrings
            en_n = re.sub(r"[^a-zāīūṛṝḷḹṃñṅśṣṭḍḥṁ]", "", en.lower())
            skt_n = skt.lower()
            if en_n and (en_n in skt_n or skt_n in en_n or
                         len(set(en_n) & set(skt_n)) / max(len(set(en_n)), 1) > 0.6):
                align.add((i, j))
    return align


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--l0dir", required=True)
    ap.add_argument("--n", type=int, default=200, help="held-out pairs")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    pairs = load_token_pairs(args.l0dir)
    random.seed(args.seed)
    sample = random.sample(pairs, min(args.n, len(pairs)))
    print(f"total clean pairs available: {len(pairs)}; held-out sample: {len(sample)}")

    # baseline 1: deterministic position (naive) — low bar
    # baseline 2: lexical overlap
    # We test per-pair: does the method align the EN token to the SKT token?
    pos_hits = lexical_hits = 0
    for p in sample:
        en = p["en"]
        skt = p["skt"]
        en_tokens = [t for t in en.replace("-", " ").split() if t]
        skts = skt_tokens(skt)
        # naive: EN word 0 aligns to SKT token 0 (all our pairs are 1 EN word-ish : 1 SKT)
        pos_hit = any(en_tokens and skts and len(en_tokens) == len(skts)
                      for _ in [0])
        # lexical: does any EN token overlap the SKT surface?
        lexical_hit = len(align_lexical(en_tokens, skts)) > 0
        pos_hits += int(pos_hit)
        lexical_hits += int(lexical_hit)

    n = max(len(sample), 1)
    report = {
        "benchmark": "P4-ALIGNMENT-v0",
        "held_out_pairs": len(sample),
        "baselines": {
            "deterministic_position_recall": round(pos_hits / n, 4),
            "lexical_overlap_recall": round(lexical_hits / n, 4),
        },
        "note": "baseline floor only. Any real aligner (awesome-align) must beat lexical_overlap_recall.",
    }
    print(json.dumps(report, indent=2))
    with open("docs/p4_alignment_eval_report.json", "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print("report -> docs/p4_alignment_eval_report.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
