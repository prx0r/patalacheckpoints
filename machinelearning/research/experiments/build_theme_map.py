#!/usr/bin/env python3
"""build_theme_map.py — full theme organization over IPVV/C1: coverage, unassigned, C1 + argument
integration, and a machine-auditable ThemeMap.

Produces:
  - an enriched corpus-specific lexicon (curated from the C1 KEY TERMS + the IPVV vocabulary)
  - the recall-first ThemeDiscoveryResult with a full coverage/overlap/unassigned audit
  - integration with C1 commentary (each theme -> member C1s + snippets; concept -> C1 index)
  - integration with the argument golds (themes -> the ARG fixtures / passages they contain)
  - a machine-auditable ThemeMap JSON (every object tagged origin=MACHINE, status=MACHINE_PROPOSED,
    lexicon_version, signal) + a human-readable validation report (markdown)

Run: cd research && . .venv/bin/activate && python experiments/build_theme_map.py
"""
from __future__ import annotations
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.theme_discovery import discover_themes
from patala_ml.gold import build_gold_v0
from patala_ml.gold002 import build_gold_002
from patala_ml.gold003 import build_gold_003
from patala_ml.gold004 import build_gold_004
from patala_ml.gold005 import build_gold_005

C1_DIR = "/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/c1/read"
OUT_JSON = "/root/projects/patala/benchmarks/v0/theme-map-ipvv-v0.json"
OUT_MD = "/root/projects/patala/benchmarks/v0/THEME-MAP-IPVV-REPORT.md"
LEXICON_VERSION = "ipvv-c1-v0"

# curated corpus-specific lexicon: core IPVV concepts (IAST + English), mined from C1 KEY TERMS
IPVV_LEXICON = [    # reflexive awareness / recognition / the heart of the doctrine
    "vimarśa", "prakāśa", "pratibhā", "pratyabhijñā", "recognition", "reflexive", "self-grasp",
    "self-awareness", "sphurattā", "throbbing", "caitanya", "saṃvid", "awareness",
    # support / order
    "āśraya", "support", "akrama", "orderless", "order-less", "krama", "order",
    # epistemic means / inference
    "pramāṇa", "means of knowledge", "anumāna", "inference", "vyāpti", "pervasion", "hetu",
    "reason", "knowledge", "jñāna",
    # construction / language
    "vikalpa", "construction", "conceptual", "parā-vāk", "speech", "language", "vāk",
    "articulation", "linguistic", "śabda", "word",
    # powers / lord / freedom
    "śakti", "power", "svātantrya", "freedom", "māheśvarya", "lordship", "lord", "icchā",
    "will", "kriyā", "action", "agency", "agent",
    # memory / self / pastness
    "memory", "smṛti", "past", "pastness", "self", "aham", "i-awareness", "knower", "pramātṛ",
    # difference / unity / ignorance
    "bheda", "difference", "abheda", "unity", "one", "anirvācya", "ignorance", "bhedābheda",
    "monism", "consciousness", "manifestation", "light", "shines", "flashing",
    # causation / states
    "causality", "cause", "effect", "cikīrṣā", "states", "kancukas", "bond", "liberation",
    "grace", "dhyāna", "bhāvanā", "creation", "appearance", "crystal", "contraction",
    "continuity", "identity", "superimposition", "adhyāsa", "perception", "external",
]

# argument fixtures -> the passages they come from (for theme<->argument integration)
ARG_FIXTURES = [
    {"gold": "ARG-GOLD-001", "structure": "CONCEPTUAL_DISTINCTION", "passage": "chunkV2-O-saptamo-vimarsa",
     "c1": "V2O-orderless-support", "concepts": ["pratibhā", "orderless", "support", "akrama"]},
    {"gold": "ARG-GOLD-002", "structure": "CONCEPTUAL_DISTINCTION", "passage": "chunkV2-L-sastho-vimarsa-smrti-apohana",
     "c1": "V2L-nonconstructed-I", "concepts": ["vikalpa", "construction", "i-awareness", "reflexive"]},
    {"gold": "ARG-GOLD-003", "structure": "REDUCTIO", "passage": "chunkV2-O-saptamo-vimarsa",
     "c1": "V2O-orderless-support", "concepts": ["support", "orderless", "akrama", "regress"]},
    {"gold": "ARG-GOLD-004", "structure": "CONCEPTUAL_DISTINCTION", "passage": "chunkV2-H-pancamo-vimarsa-k11-13",
     "c1": "V2H-vimarsa-paravak", "concepts": ["vimarśa", "prakāśa", "reflexive", "parā-vāk"]},
    {"gold": "ARG-GOLD-005", "structure": "INTERPRETIVE_SCOPE", "passage": "chunkV3-I-kriya-caturtho-close-k20-21",
     "c1": "V3I-difference-real", "concepts": ["difference", "ignorance", "anirvācya", "will"]},
]


def load_c1s() -> list[dict]:
    out = []
    for p in sorted(glob.glob(os.path.join(C1_DIR, "c1_*.md"))):
        c1_id = os.path.basename(p)[3:-3]  # strip c1_ and .md
        body = " ".join(l.lstrip("> ").strip() for l in open(p, encoding="utf-8")
                        if l.strip().startswith(">"))
        out.append({"c1_id": c1_id, "text": body})
    return out


def main():
    c1s = load_c1s()
    # each C1 body is joined prose (no internal blank lines) -> one segment per C1, aligned by index.
    # Do NOT prepend c1_id headers (that would split each C1 into header+body segments).
    doc = "\n\n".join(c["text"] for c in c1s)

    res = discover_themes(doc, lexicon=IPVV_LEXICON)
    cov = res["coverage"]
    cands = res["candidate_objects"]

    # ---- C1 integration: concept -> C1s, theme -> member C1s + snippets ----
    c1_by_id = {c["c1_id"]: c for c in c1s}
    # segment id in discover = "s{i}" aligned to c1 order; rebuild the c1 id per candidate member
    seg_to_c1 = [c["c1_id"] for c in c1s]
    for cand in cands:
        idxs = [int(s[1:]) for s in cand["member_segments"] if s[1:].isdigit()]
        member_c1 = [seg_to_c1[i] for i in idxs if i < len(seg_to_c1)]
        cand["member_c1_ids"] = member_c1
        cand["member_snippets"] = {cid: c1_by_id[cid]["text"][:160] for cid in member_c1}

    # concept -> C1 index
    concept_index = {}
    for i, c in enumerate(c1s):
        for t in IPVV_LEXICON:
            if _norm(t) in _norm(c["text"]):
                concept_index.setdefault(t, []).append(c["c1_id"])
    for t in list(concept_index):
        concept_index[t] = sorted(set(concept_index[t]))

    # ---- significance: discriminative technical theme vs generic-token noise ----
    # (100% coverage is inflated by ubiquitous generic tokens like 'one'/'self'; the useful map is the
    #  discriminative set. A theme is HIGH_SIGNIFICANCE if it is a technical lemma OR is bounded.)
    GENERIC = {"one", "self", "lord", "being", "awareness", "consciousness", "knowledge",
               "action", "power", "reason", "word", "light", "cause", "effect", "order", "past"}
    for cand in cands:
        cand["significance"] = ("LOW" if cand["label"] in GENERIC
                                else "HIGH" if cand["label"] in IPVV_LEXICON
                                else ("HIGH" if len(cand["member_c1_ids"]) <= 8 else "LOW"))

    # ---- argument integration: which themes contain the argument-fixture C1s ----
    for fix in ARG_FIXTURES:
        fix["matched_themes"] = [c["candidate_id"] for c in cands
                                 if fix["c1"] in c.get("member_c1_ids", [])]

    # ---- auditability ----
    tm = {
        "theme_map_version": "v0", "corpus": "IPVV", "lexicon_version": LEXICON_VERSION,
        "signal": "shared key technical terms (not body words)",
        "coverage": cov,
        "extracted_concepts": res["extracted_concepts"],
        "uncovered_segments": res["uncovered_segments"],
        "uncovered_c1_ids": [seg_to_c1[int(s[1:])] for s in res["uncovered_segments"]
                             if s[1:].isdigit() and int(s[1:]) < len(seg_to_c1)],
        "uncertain_assignments": res["uncertain_assignments"],
        "themes": cands,
        "concept_to_c1_index": concept_index,
        "argument_integration": ARG_FIXTURES,
        "provenance": {"origin": "MACHINE", "status": "MACHINE_PROPOSED",
                       "lexicon_version": LEXICON_VERSION, "decomposition": res["provenance"]["decomposition"]},
    }
    json.dump(tm, open(OUT_JSON, "w"), indent=2, ensure_ascii=False)

    # ---- human-readable report ----
    lines = [f"# THEME MAP — IPVV v0 (MACHINE_PROPOSED)\n",
             f"segments={cov['n_segments']} · candidates={len(cands)} · "
             f"coverage={cov['assigned_pct']*100:.0f}% ({cov['n_assigned']}/{cov['n_segments']}) · "
             f"unassigned={cov['n_unassigned']} · multi-assigned={cov['n_multi_assigned']} · "
             f"unstable-sense groups={cov['n_unstable_sense_groups']}\n",
             f"lexicon_version={LEXICON_VERSION} · {len(IPVV_LEXICON)} terms · signal: shared key terms\n",
             "\n## Themes (by member count)\n"]
    for c in sorted(cands, key=lambda x: -len(x["member_segments"])):
        lines.append(f"- **{c['label']}** [{c['suspected_kind']}, sense={c['sense_stability']}] "
                     f"n={len(c['member_segments'])}: {', '.join(c['member_c1_ids'])}")
    lines += ["\n## Unassigned C1s (not organized by any theme)\n"]
    lines += [f"- `{cid}`" for cid in tm["uncovered_c1_ids"]]
    lines += ["\n## HIGH-SIGNIFICANCE themes (the discriminative map)\n"]
    for c in sorted([x for x in cands if x["significance"] == "HIGH"], key=lambda x: -len(x["member_c1_ids"])):
        lines.append(f"- **{c['label']}** [{c['suspected_kind']}, sense={c['sense_stability']}] "
                     f"n={len(c['member_c1_ids'])}: {', '.join(c['member_c1_ids'])}")
    lines += ["\n## Argument integration\n"]
    for fix in ARG_FIXTURES:
        lines.append(f"- {fix['gold']} ({fix['structure']}) @ {fix['passage']} → "
                     f"themes: {', '.join(fix['matched_themes']) or '(none)'}")
    open(OUT_MD, "w", encoding="utf-8").write("\n".join(lines))
    print(f"wrote {OUT_JSON}\nwrote {OUT_MD}")


def _norm(s: str) -> str:
    s = (s or "").lower()
    for a, b in [("ā", "a"), ("ī", "i"), ("ū", "u"), ("ṛ", "r"), ("ṣ", "s"), ("ś", "s"),
                 ("ṇ", "n"), ("ṭ", "t"), ("ḍ", "d"), ("ḥ", "h"), ("ṃ", "m")]:
        s = s.replace(a, b)
    return s


if __name__ == "__main__":
    main()
