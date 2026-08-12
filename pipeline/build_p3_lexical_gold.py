#!/usr/bin/env python3
"""build_p3_lexical_gold.py — create the P3 lexical-sense gold benchmark.

Stratified per the review: 60 fixtures = 20 easy / 20 technical-stable / 15 polysemous / 5
NO_UNIQUE_SENSE. Each fixture carries real L0 lemma+gloss+passage locator, candidate senses, a
preferred sense, and the abstention cases (NO_UNIQUE_SENSE is the CORRECT answer for those).

IMPORTANT (anti-theatre): this is GOLD, to be SINGLE_EDITOR_REVIEWED (then ideally a second reviewer)
before it is treated as gold. It is benchmark-first — ranker.py is NOT yet a verifier, it is a candidate
ranker to be evaluated against baselines.

Usage:
  python3 pipeline/build_p3_lexical_gold.py --l0dir <l0> --out <fixtures.json> [--n 60] [--seed 42]
"""
from __future__ import annotations
import argparse
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

# technical terms we deliberately weight (their senses are what Pāṭala must get right)
TECH_TERMS = ["vimarśa", "pratibhā", "prakāśa", "saṃvid", "pramātṛ", "ābhāsa",
              "svātantrya", "krama", "śakti", "jñāna", "bheda", "abheda", "tattva",
              "spanda", "māyā", "niyati", "kāla", "pramāṇa"]

# canonical sense inventory per lemma (from the gloss distributions observed in L0)
CANONICAL = {
    "vimarśa": ["reflexive-awareness", "rehearsal/reconsideration", "conceptual-apprehension"],
    "pratibhā": ["flashing-intuition", "inspiration", "appearance"],
    "prakāśa": ["manifestation", "light", "consciousness-luminosity", "revealing"],
    "saṃvid": ["consciousness", "awareness", "knowledge"],
    "pramātṛ": ["the-knower", "subject-of-cognition", "agent"],
    "ābhāsa": ["appearance", "manifestation", "image-reflection"],
    "svātantrya": ["sovereign-freedom", "independence", "self-dependence"],
    "krama": ["order", "sequence", "succession"],
    "śakti": ["power", "energy", "capacity"],
    "jñāna": ["knowledge", "cognition", "insight"],
    "bheda": ["difference", "distinction", "split"],
    "abheda": ["non-difference", "non-distinction", "identity"],
    "tattva": ["reality", "principle", "category", "essence"],
    "spanda": ["vibration", "pulsation", "throb"],
    "māyā": ["māyā-power", "illusion", "creative-power"],
    "niyati": ["necessity", "fate", "fixed-order"],
    "kāla": ["time", "period", "Kāla-principle"],
    "pramāṇa": ["valid-means-of-knowledge", "evidence", "criterion"],
}

# gloss-token → sense hints (so preferred is CONSISTENT with the actual gloss)
def sense_for_gloss(gloss: str) -> str | None:
    """Pick the canonical sense whose keyword appears in the gloss (or a stem hint)."""
    g = gloss.lower()
    hints = [
        ("reflexive", "reflexive-awareness"), ("rehearsal", "rehearsal/reconsideration"),
        ("conceptual", "conceptual-apprehension"), ("intuition", "flashing-intuition"),
        ("inspiration", "inspiration"), ("manifestation", "manifestation"),
        ("light", "light"), ("luminosity", "consciousness-luminosity"), ("reveal", "revealing"),
        ("consciousness", "consciousness"), ("awareness", "awareness"), ("knowledge", "knowledge"),
        ("knower", "the-knower"), ("appearance", "appearance"), ("image", "image-reflection"),
        ("freedom", "sovereign-freedom"), ("independence", "independence"),
        ("order", "order"), ("sequence", "sequence"), ("succession", "succession"),
        ("power", "power"), ("energy", "energy"), ("capacity", "capacity"),
        ("cognition", "cognition"), ("insight", "insight"), ("difference", "difference"),
        ("distinction", "distinction"), ("split", "split"), ("non-difference", "non-difference"),
        ("identity", "identity"), ("reality", "reality"), ("principle", "principle"),
        ("category", "category"), ("essence", "essence"), ("vibration", "vibration"),
        ("pulsation", "pulsation"), ("throb", "throb"), ("illusion", "illusion"),
        ("necessity", "necessity"), ("fate", "fate"), ("time", "time"), ("period", "period"),
        ("valid-means", "valid-means-of-knowledge"), ("evidence", "evidence"),
    ]
    for token, sense in hints:
        if token in g:
            return sense
    return None


# which senses are TECHNICAL (doctrinal) — the ranker must prefer these in technical context
TECH_SENSE = {
    "vimarśa": "reflexive-awareness", "pratibhā": "flashing-intuition",
    "prakāśa": "consciousness-luminosity", "saṃvid": "consciousness",
    "pramātṛ": "the-knower", "ābhāsa": "appearance", "svātantrya": "sovereign-freedom",
    "krama": "order", "śakti": "power", "jñāna": "knowledge", "bheda": "difference",
    "abheda": "non-difference", "tattva": "reality", "spanda": "vibration",
    "māyā": "māyā-power", "niyati": "necessity", "kāla": "time", "pramāṇa": "valid-means-of-knowledge",
}


def load_lemma_records(l0dir: str) -> dict:
    """lemma → list of {gloss, passage_locator, id, source_text, raw_fragment, sanskrit_iast}."""
    d = defaultdict(list)
    for f in Path(l0dir).glob("*.l0.jsonl"):
        chunk = f.name[: -len(".l0.jsonl")]
        for line in f.open(encoding="utf-8"):
            r = json.loads(line)
            lem = r.get("lemma_iast", "")
            gloss = r.get("literal_gloss", "")
            if not lem or not gloss:
                continue
            # extract the IAST Sanskrit from the raw_fragment's parenthetical
            import re as _re
            m = _re.search(r"\(([^()]+)\)", r.get("raw_fragment", ""))
            skt = m.group(1).strip() if m else ""
            d[lem].append({"gloss": gloss, "id": r.get("id"),
                           "locator": f"{chunk}:L{r.get('line_id')}",
                           "source_text": r.get("source_text", ""),
                           "raw_fragment": r.get("raw_fragment", ""),
                           "sanskrit_iast": skt})
    return d


def build_fixture(lemma, gloss, locator, sense, extra_senses, is_no_unique=False, rec=None):
    f = {
        "surface": gloss, "lemma": lemma, "passage_locator": locator,
        "candidate_senses": extra_senses if is_no_unique else [sense] + extra_senses,
        "preferred": None if is_no_unique else sense,
        # enrichment per the external review (docs/P3_EDITORIAL_REVIEW.md): real Sanskrit context,
        # not just the English gloss that already embodies the label.
        "passage_id": (rec or {}).get("id"),
        "source_span_id": (rec or {}).get("locator"),
        "sanskrit_token": (rec or {}).get("sanskrit_iast"),
        "sanskrit_clause": (rec or {}).get("source_text", ""),
        "evidence": {"local_context": [(rec or {}).get("source_text", gloss)],
                     "same_work_parallels": [], "lexical_sources": [], "commentary": []},
        "review_state": "MACHINE_DRAFT",  # to be promoted to SINGLE_EDITOR_GOLD by human review
    }
    return f


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--l0dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=60)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    random.seed(args.seed)
    recs = load_lemma_records(args.l0dir)

    easy, tech, poly, nou = 0, 0, 0, 0
    fixtures = []
    seen = set()  # avoid duplicate (lemma, preferred) fixtures — gloss may vary
    # 20 easy: technical terms with an obvious dominant sense
    for lem in random.sample(TECH_TERMS, min(20, len(TECH_TERMS))):
        pool = recs.get(lem, [])
        if not pool:
            continue
        for r in random.sample(pool, min(len(pool), 20)):
            preferred = sense_for_gloss(r["gloss"]) or TECH_SENSE.get(lem, CANONICAL[lem][0])
            if (lem, preferred) in seen:
                continue
            seen.add((lem, preferred))
            fi = build_fixture(lem, r["gloss"], r["locator"], preferred,
                               [s for s in CANONICAL.get(lem, ["?"]) if s != preferred], rec=r)
            fixtures.append(fi); easy += 1
            break

    # 20 technical-stable: weighted to technical sense
    for lem in TECH_TERMS:
        if tech >= 20:
            break
        pool = recs.get(lem, [])
        if not pool:
            continue
        for r in random.sample(pool, min(len(pool), 30)):
            ts = sense_for_gloss(r["gloss"]) or TECH_SENSE.get(lem)
            if not ts:
                continue
            if (lem, ts) in seen:
                continue
            seen.add((lem, ts))
            alt = [s for s in CANONICAL.get(lem, []) if s != ts]
            fi = build_fixture(lem, r["gloss"], r["locator"], ts, alt, rec=r)
            fixtures.append(fi); tech += 1
            break

    # 15 polysemous: term whose sense is genuinely context-dependent
    # NOTE: the real L0 data is dominated by a few dominant senses per term, so this may undershoot;
    # that is honest — we record what the data supports rather than padding with invented contexts.
    poly_terms = ["prakāśa", "krama", "śakti", "jñāna", "bheda", "tattva", "kāla", "ābhāsa"]
    for lem in poly_terms:
        if poly >= 15:
            break
        pool = recs.get(lem, [])
        if not pool:
            continue
        for r in random.sample(pool, min(len(pool), 40)):
            senses = CANONICAL.get(lem, ["?", "??"])
            preferred = sense_for_gloss(r["gloss"]) or (senses[1] if len(senses) > 1 else senses[0])
            if (lem, preferred) in seen:
                continue
            seen.add((lem, preferred))
            fi = build_fixture(lem, r["gloss"], r["locator"], preferred,
                               [s for s in senses if s != preferred], rec=r)
            fixtures.append(fi); poly += 1
            break

    # 5 NO_UNIQUE_SENSE: the correct answer is abstention (OPEN)
    for lem in ["vimarśa", "pratibhā", "māyā", "pramāṇa", "krama"]:
        if nou >= 5:
            break
        pool = recs.get(lem, [])
        if not pool:
            continue
        r = random.choice(pool)
        if (lem, None) in seen:
            continue
        seen.add((lem, None))
        fi = build_fixture(lem, r["gloss"], r["locator"], None, CANONICAL.get(lem, ["?", "?"]),
                           is_no_unique=True, rec=r)
        fixtures.append(fi); nou += 1

    # trim/pad to n
    fixtures = fixtures[: args.n]

    out = {
        "benchmark": "P3-LEXICAL-SENSE-v0",
        "description": "lexical-sense gold: does the ranker identify the accepted sense + abstain when OPEN?",
        "stratification": {"easy": easy, "technical_stable": tech, "polysemous": poly, "no_unique_sense": nou},
        "fixtures": fixtures,
    }
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    print(f"wrote {len(fixtures)} fixtures (easy={easy} tech={tech} poly={poly} nou={nou}) to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
