#!/usr/bin/env python3
"""pipeline/run_argrec_pilot_argmap.py — generate the pilot ARGMAP candidate (gate #4).

The V2L T1/L0/C1 ALREADY EXIST as the real gold material (sanskritree stack) — NO T1 generation needed.
This feeds the model the REAL existing factory-style inputs for the frozen window (kārikās 1-5) and
asks it to recover the argument, WITHOUT the gold ARGMAP.

INPUT (real, existing):
    - T1  : translations/_stack/ipvv/02_t1/chunkV2-L-sastho-vimarsa-smrti-apohana.md
    - L0  : translations/_stack/ipvv/l0/chunkV2-L....l0.jsonl (token glosses)
    - C1  : translations/_stack/ipvv/c1/read/c1_V2L-nonconstructed-I.md

NO-GOLD-LEAKAGE: the gold ARGMAP (pilot_V2L_ARGUMENT_MAP.md) is NEVER read or passed.

Usage:
    python3 pipeline/run_argrec_pilot_argmap.py
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

sys.path.insert(0, "/root/projects/patala/pipeline")
from model import chat  # noqa: E402

BASE = "/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv"
T1 = os.path.join(BASE, "02_t1/chunkV2-L-sastho-vimarsa-smrti-apohana.md")
L0 = os.path.join(BASE, "l0/chunkV2-L-sastho-vimarsa-smrti-apohana.l0.jsonl")
C1 = os.path.join(BASE, "c1/read/c1_V2L-nonconstructed-I.md")
GOLD_ARGMAP = os.path.join(BASE, "pilot/pilot_V2L_ARGUMENT_MAP.md")  # NEVER READ
OUT = "/root/projects/patala/data/evaluation/argrec-pilot-001-argmap.json"

# the frozen window (kārikās 1-5) — we slice the T1/L0 to these units where possible
WINDOW = ["k1", "k2", "k3", "k4", "k5"]


def _read(p):
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def _l0_first_n(n=400):
    """The first n L0 token-gloss records (the window's tokens)."""
    out = []
    for i, line in enumerate(open(L0, encoding="utf-8")):
        if i >= n:
            break
        try:
            r = json.loads(line)
            out.append(f"{r.get('raw_fragment')} = {r.get('literal_gloss')}")
        except Exception:
            continue
    return "\n".join(out)


def build_prompt() -> str:
    t1 = _read(T1)
    c1 = _read(C1)
    l0 = _l0_first_n(350)
    return (
        "You are the Pāṭala argument-map producer. Reconstruct the ARGUMENT structure of the IPVV "
        "passage below (the ṣaṣṭho vimarśa: is the 'I'-recollection / ahaṃ-pratyavamarśa a conceptual "
        "construction (vikalpa), or the two-invoking determination (dvayākṣepī viniścaya)?).\n"
        "This is kārikās 1-5 of V2-L (the apohana / smṛti discussion). The objection, reply, and crux "
        "may span the whole window — do not cut the argument short.\n"
        "Produce EXACTLY 4 sections:\n"
        "1. what_is_at_issue: the question + the move, 1-3 sentences.\n"
        "2. argument_steps: the argument step by step (objection -> reply -> the crux), each step "
        "   citing a kārikā/line.\n"
        "3. open_items: genuinely unresolved items (status OPEN|NEEDS_REVIEW).\n"
        "4. decision_for_l2: one sentence guiding the readable L2.\n"
        "Return JSON ONLY: {\"what_is_at_issue\":\"...\",\"argument_steps\":[\"...\"],"
        "\"open_items\":[{\"text\":\"...\",\"status\":\"OPEN|NEEDS_REVIEW\"}],\"decision_for_l2\":\"...\"}\n\n"
        f"# T1 (transliteral gloss, the window)\n{t1[:6000]}\n\n"
        f"# L0 TOKEN GLOSSES (first 350)\n{l0}\n\n"
        f"# C1 (the passage interpretation)\n{c1}\n\n"
        "GROUNDING RULE: every argument step must be anchored to a kārikā/line in the T1. Do NOT "
        "invent a premise the text does not license. If something is unresolved, say so."
    )


def generate() -> dict:
    prompt = build_prompt()
    raw = chat("You are the Pāṭala argument-map producer (no gold retrieval; only the given source).",
               prompt, timeout=300)
    raw = (raw or "").strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0]
    s, e = raw.find("{"), raw.rfind("}")
    body = json.loads(raw[s:e + 1]) if s >= 0 and e > s else {}
    cand = {
        "pilot_id": "IPVV-ARGREC-PILOT-001",
        "window": WINDOW,
        "argument_map": {
            "what_is_at_issue": (body.get("what_is_at_issue") or "").strip(),
            "argument_steps": [s for s in (body.get("argument_steps") or []) if isinstance(s, str) and s.strip()],
            "open_items": body.get("open_items") or [],
            "decision_for_l2": (body.get("decision_for_l2") or "").strip(),
        },
        "inputs": {"T1": os.path.basename(T1), "L0": os.path.basename(L0), "C1": os.path.basename(C1)},
        "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest(),
        "model": "deepseek-v4-flash",
        "no_gold_leakage": True,
        "gold_never_read": True,
        "status": "MACHINE_PROPOSED",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(cand, f, indent=2, ensure_ascii=False)
    return cand


if __name__ == "__main__":
    c = generate()
    am = c["argument_map"]
    print(f"ARGMAP candidate (from REAL T1/L0/C1, no gold leakage):")
    print(f"  what_is_at_issue: {am['what_is_at_issue'][:100]}")
    print(f"  steps: {len(am['argument_steps'])}, open: {len(am['open_items'])}")
    for s in am["argument_steps"]:
        print(f"    - {s[:100]}")
    print(f"  wrote {OUT}")
