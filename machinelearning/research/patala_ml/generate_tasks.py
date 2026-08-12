"""patala_ml/generate_tasks.py — derive benchmark fixtures from REAL scholarly structure.

Uses the actual C1 `see_also` / related-passage edges as the relational gold (they encode real
doctrinal links), to seed PATALA-RETRIEVAL + PATALA-STRUCTURE without inventing labels.

For each passage with see_also links, we produce:
  retrieval task:  query = a sentence of the passage's L2; relevant = {this passage}
                   (retrieval should pull the passage itself back)
  structure task:  pair (passage, its see_also target) with relation POSITIVE
                   hard negative = a passage sharing key-terms but NOT in see_also
"""
from __future__ import annotations

import json
import random

from .corpus import PassageDoc, load_passages


def _sample_sentence(text: str) -> str:
    """A short query sentence from the prose."""
    sentences = [s.strip() for s in text.replace("\n", " ").split(". ") if len(s.strip()) > 40]
    return random.choice(sentences) if sentences else text[:120]


def generate_retrieval_tasks(docs: list[PassageDoc], n_per_doc: int = 1, seed: int = 0) -> list[dict]:
    rng = random.Random(seed)
    tasks = []
    for d in docs:
        if not d.l2_text:
            continue
        for _ in range(n_per_doc):
            q = _sample_sentence(d.l2_text)
            # hard negative: a doc sharing >=1 key term but a different chunk
            hard = []
            for o in docs:
                if o.id == d.id:
                    continue
                shared = set(d.key_terms) & set(o.key_terms)
                if shared and not (o.locator in d.see_also or d.locator in o.see_also):
                    hard.append(o.id)
                    break
            tasks.append({
                "query": q,
                "relevant": [d.id],
                "hard_negatives": hard[:1],
                "item_key": d.id,
            })
    return tasks


def generate_structure_tasks(docs: list[PassageDoc], seed: int = 0) -> list[dict]:
    """POSITIVE pairs from real see_also edges; hard-negative = shared-term non-linked pair."""
    rng = random.Random(seed)
    by_loc = {d.locator: d for d in docs}
    tasks = []
    seen = set()
    for d in docs:
        for target in d.see_also:
            # target is like "V2-S" or "IPK 1.5.11" — resolve to a doc
            t = next((o for o in docs if target in o.locator), None)
            if not t:
                continue
            pair = tuple(sorted([d.id, t.id]))
            if pair in seen:
                continue
            seen.add(pair)
            tasks.append({
                "a": d.id, "b": t.id, "relation_type": "POSITIVE",
                "evidence": f"see_also in {d.locator} → {t.locator}",
                "item_key": pair[0] + "::" + pair[1],
            })
    return tasks


def generate_fidelity_tasks(docs: list[PassageDoc]) -> list[dict]:
    """C1→L2 fidelity (NON-LEAKY): query = the C1 commentary, relevant = its own passage.

    The retriever indexes L2 only, so this tests whether the commentary reliably points back
    to its source passage — the C1→source fidelity task. The query is a different
    representation than the indexed field, so it cannot trivially match itself.
    """
    tasks = []
    for d in docs:
        if not d.c1_body or not d.l2_text:
            continue
        tasks.append({
            "query": d.c1_body[:800],
            "relevant": [d.id],
            "hard_negatives": [],
            "item_key": d.id,
        })
    return tasks


def write_tasks(tasks: list[dict], path: str):
    with open(path, "w", encoding="utf-8") as f:
        for t in tasks:
            f.write(json.dumps(t, ensure_ascii=False) + "\n")
    print(f"wrote {len(tasks)} tasks → {path}")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="tasks")
    ap.add_argument("--store", default=None)
    args = ap.parse_args()
    docs = load_passages(args.store)
    ret = generate_retrieval_tasks(docs, seed=1)
    write_tasks(ret, f"{args.out}/PATALA-RETRIEVAL.jsonl")
    struct = generate_structure_tasks(docs, seed=1)
    write_tasks(struct, f"{args.out}/PATALA-STRUCTURE.jsonl")
    fid = generate_fidelity_tasks(docs)
    write_tasks(fid, f"{args.out}/PATALA-FIDELITY.jsonl")
    print(f"retrieval={len(ret)} structure={len(struct)} fidelity={len(fid)}")
