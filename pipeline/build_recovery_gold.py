#!/usr/bin/env python3
"""pipeline/build_recovery_gold.py — freeze ARGUMENT-RECOVERY-BENCH-v1 gold from the real IPVV golds.

Turns the hand-authored IPVV pilot argument-maps (the gold standard) into the FROZEN recovery-gold
schema. These are hidden from the generator: Agent 2 produces an ARGMAP for the same passage blind,
Agent 1 scores it against this gold.

Frozen gold per case (argument_recovery_bench.GOLD_SCHEMA):
    case_id, passage_ref, research_question
    propositions[]   {pid, text, speaker, commitment, explicitness, source_span}
    inferences[]     {iid, premises, conclusion, warrant, warrant_status, warrant_constraints}
    attacks[]        {attacker, target_premise, type}
    open_questions[] {text, status}
    cruxes[]         {crux_id, decisive_premises, question}

Source: /mnt/.../ipvv/pilot/pilot_V*_ARGUMENT_MAP.md (the 51 real golds).

The propositions/inferences are DERIVED from the gold's kārikā-by-kārikā argument reconstruction
(the 'what is at issue' -> the thesis; the argument steps -> premises; the unresolved -> open;
the decision -> the boundary). Each proposition's speaker is inferred from the gold's structure
(author claim vs reported objection).

Design: this gold is the independent reference. It is written once, frozen (hash), and never edited
to make a candidate pass.
"""
from __future__ import annotations

import glob
import hashlib
import json
import os
import re
import sys

GOLD_DIR = "/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/pilot"
OUT = "/root/projects/patala/data/evaluation/recovery-gold-v1.json"


def _sha256(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _object_id(path: str) -> str:
    base = os.path.basename(path)
    m = re.match(r"pilot_(V\d+[A-Z]+(?:_[A-Za-z0-9]+)?)_ARGUMENT_MAP", base)
    tag = m.group(1) if m else base.replace("_ARGUMENT_MAP.md", "")
    passage = re.match(r"(V\d+[A-Z]+)", tag)
    return f"ipvv:{passage.group(1) if passage else tag}"


def _section(lines: list[str], heading_re) -> str:
    out, on = [], False
    for ln in lines:
        if re.match(heading_re, ln):
            on = True
            continue
        if on:
            if re.match(r"^#+ ", ln):
                break
            s = ln.strip()
            if s:
                out.append(s)
    return "\n".join(out).strip()


def _detect_speaker(text: str) -> str:
    low = text.lower()
    if any(k in low for k in ("objection", "opponent", "buddhist", "the rival", "one might say",
                              "nanu", "āśaṅkya", "it could be said")):
        return "opponent"
    if any(k in low for k in ("the reply", "abhinavagupta", "the siddhānta", "we hold", "our view",
                              "the lord", "he shows", "the author")):
        return "author"
    return "author"


def _detect_explicitness(text: str) -> str:
    low = text.lower()
    if any(k in low for k in ("can be reconstructed", "it can be", "one can", "plausibly",
                              "the reconstruction", "we can infer")):
        return "RECONSTRUCTED"
    return "EXPLICIT"


def convert_gold(path: str) -> dict:
    lines = open(path, encoding="utf-8").read().splitlines()
    what = _section(lines, r"^##\s*1\.\s*What is at issue")
    arg = _section(lines, r"^##\s*2\.\s*The argument")
    opensec = _section(lines, r"^##\s*3\.\s*(Unresolved|Open|Uncertain)")
    decision = _section(lines, r"^##\s*4\.\s*Decision for L2")

    # propositions = the kārikā-by-kārikā argument chunks
    chunks = [c for c in re.split(r"\n\s*\*{0,2}Kārikā\s*\d+", "\n" + arg) if " ".join(c.split()).strip()]
    propositions = []
    for i, c in enumerate(chunks[:6]):
        text = " ".join(c.split())[:220]
        if not text:
            continue
        propositions.append({
            "pid": f"{_object_id(path)}:P{i+1}",
            "text": text,
            "speaker": _detect_speaker(text),
            "commitment": "RECONSTRUCTS" if _detect_explicitness(text) == "RECONSTRUCTED" else "ASSERTS",
            "explicitness": _detect_explicitness(text),
            "source_span": "",
        })
    # the thesis (what is at issue) as a reconstructed proposition
    if what and len(propositions) < 6:
        propositions.insert(0, {
            "pid": f"{_object_id(path)}:THESIS",
            "text": " ".join(what.split())[:220],
            "speaker": "author", "commitment": "ASSERTS", "explicitness": "RECONSTRUCTED",
            "source_span": "",
        })
    # the decision as the boundary
    if decision and len(propositions) < 6:
        propositions.append({
            "pid": f"{_object_id(path)}:BOUNDARY",
            "text": " ".join(decision.split())[:220],
            "speaker": "author", "commitment": "RECONSTRUCTS", "explicitness": "RECONSTRUCTED",
            "source_span": "",
        })

    # inference: thesis <- (the chunks) as one reconstructed bridge
    premises = [p["pid"] for p in propositions if p["explicitness"] == "EXPLICIT"][:4]
    inferences = [{
        "iid": f"{_object_id(path)}:I1",
        "premises": premises,
        "conclusion": propositions[0]["pid"] if propositions else "",
        "warrant": ("the argument reconstructs the passage's reasoning step by step; the bridge is "
                    "rational reconstruction, not a textually-explicit inference"),
        "warrant_status": "RATIONAL_RECONSTRUCTION",
        "warrant_constraints": [],  # spans not carried in the gold md; the human would cite them
    }]

    # open questions
    open_questions = []
    for ln in opensec.splitlines() if opensec else []:
        s = ln.strip().lstrip("0123456789.·- \t")
        if s and len(s) > 20:
            open_questions.append({"text": s[:220], "status": "OPEN"})
    if not open_questions and opensec:
        open_questions.append({"text": opensec[:220], "status": "OPEN"})

    # crux: the core unresolved dispute (from what is at issue / open questions)
    crux_q = open_questions[0]["text"] if open_questions else what
    cruxes = [{"crux_id": f"{_object_id(path)}:CRUX", "decisive_premises": premises[:2],
               "question": crux_q[:220]}]

    return {
        "case_id": _object_id(path),
        "passage_ref": f"pt:passage:ipvv:{_object_id(path).split(':')[1]}",
        "research_question": what[:300],
        "propositions": propositions,
        "inferences": inferences,
        "attacks": [],   # the gold md doesn't isolate attack edges cleanly; left empty (filled by review)
        "open_questions": open_questions,
        "cruxes": cruxes,
    }


def main() -> int:
    golds = sorted(glob.glob(os.path.join(GOLD_DIR, "*_ARGUMENT_MAP.md")))
    cases = []
    skipped = []
    for path in golds:
        c = convert_gold(path)
        if not c["propositions"]:
            skipped.append(path)
            continue
        cases.append(c)
    bundle = {
        "bench": "ARGUMENT-RECOVERY-BENCH-v1",
        "frozen": True,
        "cases": cases,
        "case_count": len(cases),
        "gold_hash": _sha256(cases),
        "frozen_at": "2026-08-13",
        "design_note": ("Independent frozen gold derived from the hand-authored IPVV pilot argument-maps. "
                        "Hidden from the ARGMAP generator. Never edited to make a candidate pass."),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)
    n_prop = sum(len(c["propositions"]) for c in cases)
    n_open = sum(len(c["open_questions"]) for c in cases)
    print(f"ARGUMENT-RECOVERY-BENCH-v1 gold frozen: {len(cases)} cases ({len(golds)} golds, {len(skipped)} skipped)")
    print(f"  propositions={n_prop}, inferences={len(cases)}, open_questions={n_open}, cruxes={len(cases)}")
    print(f"  gold_hash={bundle['gold_hash'][:16]}...")
    print(f"  wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
