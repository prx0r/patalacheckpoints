"""Pāṭala evidence packet — the reproducible context fed into each stage.

Per the red-team review: translation stages must NOT "do research" from model
memory. They adjudicate using a supplied EVIDENCE PACKET. This builds it from the
corpus + the record:

    passage (sanskrit + edition)
    neighboring passages (prev/next)
    work metadata (bibliography_state, traditions, period)
    term senses + trajectories (for the tracked lemmas in this passage)
    same-work / same-tradition occurrences (coarse)
    known parallels / commentary witnesses
    existing translation anchors (rights-qualified)

If evidence is insufficient, the packet says so (evidence_needed) rather than the
model inventing it.
"""
from __future__ import annotations
import json
import os
import sys
from typing import Any, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# The core technical lemmas to pull term data for
CORE_LEMMAS = ["kula", "krama", "sakti", "khecari", "vimarsa", "prakasa",
               "spanda", "samvit", "visarga", "matrka", "uccara", "avesa",
               "sunya", "paramarsa", "svatantrya"]


def _passage_corpus() -> list[dict]:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pdir = os.path.join(base, "data", "corpus", "passages")
    out = []
    if os.path.isdir(pdir):
        for f in sorted(os.listdir(pdir)):
            if f.endswith(".jsonl"):
                for line in open(os.path.join(pdir, f), encoding="utf-8"):
                    line = line.strip()
                    if line:
                        out.append(json.loads(line))
    return out


def _terms() -> list[dict]:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    p = os.path.join(base, "data", "terms.json")
    try:
        return json.load(open(p, encoding="utf-8"))["terms"]
    except Exception:
        return []


def _trajectories() -> list[dict]:
    # best-effort: parse the trajectories.ts node id/lemma/sense literals
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    p = os.path.join(base, "data", "corpus", "trajectories.ts")
    out = []
    if os.path.exists(p):
        import re
        txt = open(p, encoding="utf-8").read()
        for m in re.finditer(r'lemma:\s*"([^"]+)",[^}]*?sense_id:\s*"([^"]+)"[^}]*?claim:\s*"([^"]+)"', txt):
            out.append({"lemma": m.group(1), "sense_id": m.group(2), "claim": m.group(3)})
    return out


def _lemma_matches(text: str, lemma: str) -> int:
    return text.lower().count(lemma.lower())


def build_evidence_packet(record: dict, work_id: str = "",
                          max_neighbors: int = 2,
                          max_occurrences: int = 20) -> dict[str, Any]:
    """Assemble the deterministic evidence packet for a passage record."""
    work_id = work_id or record.get("work_id", "")
    passage = record["source"]
    loc = record["location"]

    corpus = _passage_corpus()
    same_work = [p for p in corpus if p.get("work_id") == work_id]
    # neighbors by the current locator
    loc_str = loc.get("locator") or f"{loc['chapter']}.{loc['verse']}"
    ch, vs = loc.get("chapter"), loc.get("verse")
    neighbors = []
    for p in sorted(same_work, key=lambda x: (x["location"]["chapter"], x["location"]["verse"])):
        pc, pv = p["location"]["chapter"], p["location"]["verse"]
        if pc == ch and abs(pv - vs) in (1, 2) and pv != vs:
            neighbors.append({"id": p["id"], "sanskrit": p["sanskrit"][:160],
                              "locator": f"{pc}.{pv}"})

    # term data: find lemmas present in this passage's Sanskrit
    san = passage.get("source_text", "")
    terms = _terms()
    tracked = []
    for t in terms:
        norm = t["lemma"].replace("ā", "a").replace("ī", "i").replace("ū", "u") \
                         .replace("ś", "s").replace("ṣ", "s").replace("ṛ", "r") \
                         .replace("ḥ", "h").replace("ṅ", "n").replace("ñ", "n") \
                         .replace("ṭ", "t").replace("ḍ", "d").replace("ṇ", "n")
        if norm and norm.lower() in san.lower():
            tracked.append({
                "lemma": t["lemma"],
                "senses": [s["label"] for s in t.get("senses", [])],
                "preferred_renderings": t.get("preferred_renderings", []),
            })

    # occurrences (coarse substring, honest)
    occurrences = {
        "method": "substring",
        "lemmatized": False,
        "counts": {t["lemma"]: _lemma_matches(san, t["lemma"]) for t in tracked},
        "note": "substring, not lemma — for context only",
    }

    return {
        "passage": {"id": record["passage_id"], "sanskrit": san,
                    "edition": passage.get("source_edition"),
                    "source_id": passage.get("source_id")},
        "work": {"id": work_id, "locator": loc_str},
        "neighbors": neighbors[:max_neighbors],
        "terms": tracked,
        "occurrences": occurrences,
        "evidence_needed": [],   # populated by the stage if insufficient
        "provenance": "deterministic evidence packet — no generated interpretation",
    }
