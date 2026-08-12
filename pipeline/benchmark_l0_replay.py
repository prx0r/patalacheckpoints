#!/usr/bin/env python3
"""pipeline/benchmark_l0_replay.py — the Sanskrit-only replay benchmark (Pāṭala-Evals embryo).

Hides the gold English, runs the RAW-L0 factory (deterministic Vidyut core + agentic BATCH gloss)
on raw Sanskrit, then compares against a gold L0 layer. Measures, per token:
  - segmentation      (did the machine split the same tokens — token count / raw_fragment overlap)
  - lemma             (Vidyut lemma vs gold lemma, normalized match)
  - gloss             (machine literal_gloss vs gold literal_gloss, fuzzy agreement)
  - abstention        (machine left a token unglossed / AMBIGUOUS)
  - false-certainty   (machine confident where gold was AMBIGUOUS / empty)

HONESTY: the gold↔machine token alignment is approximate (the IPVV gold was built from the T1
gloss format; the machine reads raw Sanskrit, so tokenization differs). The benchmark reports
overlap metrics with that caveat, NOT a single inflated score. This is a scaffold: full IPVV
raw-chunk↔gold alignment is the formal-testing step (next round).

Usage:
  python3 pipeline/benchmark_l0_replay.py --work kramasadbhava [--verses 5]
  python3 pipeline/benchmark_l0_replay.py --source <raw.txt> --gold <gold.l0.jsonl>
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent3_batch import load_raw_source, split_verses
from raw_l0 import raw_l0_to_canonical
from agentic_gloss import run_batch


def norm(s: str) -> str:
    """Normalize a token for matching: lowercase, strip diacritics + non-alnum."""
    s = (s or "").lower()
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return "".join(c for c in s if c.isalnum())


def load_gold(path: str) -> list[dict]:
    recs = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            recs.append(json.loads(line))
        except Exception:
            continue
    return recs


def run_machine(work_id: str, verses: list[str]) -> list:
    """Deterministic RAW-L0 + BATCH gloss for the given verses. Returns per-verse records."""
    entries = []
    for i, verse in enumerate(verses):
        records, _ = raw_l0_to_canonical(f"{work_id}-v{i+1}", verse)
        entries.append({"idx": i, "verse": verse, "tokens": [r["raw_fragment"] for r in records if r["raw_fragment"]]})
    gloss_lookup = {}
    for g in run_batch([e for e in entries if e["tokens"]], work_id):
        gloss_lookup[g["idx"]] = g["gloss_map"]
    out = []
    for i, verse in enumerate(verses):
        records, _ = raw_l0_to_canonical(f"{work_id}-v{i+1}", verse)
        gm = gloss_lookup.get(i, {})
        for r in records:
            r["_machine_gloss"] = (gm.get(r["raw_fragment"]) or {}).get("literal", "")
        out.append(records)
    return out


def compare(machine_flat: list[dict], gold: list[dict]) -> dict:
    """Honest overlap between machine tokens and gold tokens (matched by normalized lemma)."""
    gold_by_lemma: dict[str, list[dict]] = {}
    for g in gold:
        gold_by_lemma.setdefault(norm(g.get("lemma_iast") or g.get("raw_fragment") or ""), []).append(g)

    n_machine = len(machine_flat)
    n_gold = len(gold)
    lemma_hit = gloss_hit = 0
    abstained = false_certain = 0
    matched = 0
    for m in machine_flat:
        lemma = norm(m.get("lemma_iast") or m.get("raw_fragment") or "")
        mgloss = norm(m.get("_machine_gloss") or "")
        gs = gold_by_lemma.get(lemma, [])
        if gs:
            matched += 1
            # lemma agreement: any gold record with the same normalized lemma
            lemma_hit += 1
            # gloss agreement: fuzzy (shared content) against any gold gloss in the group
            if mgloss and any(norm(g.get("literal_gloss") or "") and
                              (mgloss in norm(g["literal_gloss"]) or norm(g["literal_gloss"]) in mgloss)
                              for g in gs):
                gloss_hit += 1
        if not mgloss:
            abstained += 1
        # false-certainty: machine PARSED + gloss, but every matching gold was AMBIGUOUS/empty
        if mgloss and gs and all(g.get("status") == "AMBIGUOUS" or not (g.get("literal_gloss") or "") for g in gs):
            false_certain += 1

    return {
        "n_machine": n_machine,
        "n_gold": n_gold,
        "matched_by_lemma": matched,
        "lemma_agreement": round(matched / n_machine, 3) if n_machine else None,
        "gloss_agreement_of_matched": round(gloss_hit / matched, 3) if matched else None,
        "abstention_rate": round(abstained / n_machine, 3) if n_machine else None,
        "false_certainty": false_certain,
        "caveat": "gold↔machine token alignment is approximate (gold from T1-gloss format; machine from raw Sanskrit). Report is overlap, not a validated score.",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="kramasadbhava")
    ap.add_argument("--verses", type=int, default=3)
    ap.add_argument("--source", default=None, help="raw sanskrit file (else --work's ledger source)")
    ap.add_argument("--gold", default=None, help="gold L0 jsonl for comparison")
    a = ap.parse_args()

    if a.source:
        verses = split_verses(Path(a.source).read_text(encoding="utf-8"))[: a.verses]
    else:
        verses = split_verses(load_raw_source(a.work))[: a.verses]

    machine = run_machine(a.work, verses)
    machine_flat = [r for v in machine for r in v]

    print(f"work={a.work} verses={len(verses)} machine_tokens={len(machine_flat)}")
    # per-verse gloss coverage
    for i, v in enumerate(machine):
        glossed = sum(1 for r in v if r.get("_machine_gloss"))
        print(f"  v{i+1}: {len(v)} tokens, {glossed} glossed")

    if a.gold:
        gold = load_gold(a.gold)
        res = compare(machine_flat, gold)
        print("\nREPLAY METRICS:")
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print("\n(no gold given — machine metrics only; pass --gold <gold.l0.jsonl> for replay comparison)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
