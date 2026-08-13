#!/usr/bin/env python3
"""pipeline/run_argrec_pilot_argmap.py — generate ARGMAP for IPVV-ARGREC-PILOT-001 (gate #4).

Consumes the frozen context bundle (ipvv:V2L:argctx:001 = k1..k5) — the T1/L0 of the CONTIGUOUS
window, NOT a single cut-in-half unit — and produces an ARGMAP candidate for the known hard argument
(V2L apohana / 'I'-recollection is not a construction).

NO-GOLD-LEAKAGE (the reviewer's rule): the prompt may include Sanskrit / T1 gloss / L0 tokens / C1 and
generic argument instructions, but MUST NOT retrieve or reference the gold ARGMAP for ipvv:V2L.

Usage (after T1 for the window exists):
    python3 pipeline/run_argrec_pilot_argmap.py  [--emit json]
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

sys.path.insert(0, "/root/projects/patala/pipeline")
import object_registry as R  # noqa: E402
from model import chat  # noqa: E402

PILOT = json.load(open("/root/projects/patala/data/evaluation/argrec-pilot-001-freeze.json", encoding="utf-8"))
WINDOW = PILOT["context_window"]["members"]
OUT = "/root/projects/patala/data/evaluation/argrec-pilot-001-argmap.json"


def _gather_context() -> dict:
    """Gather the frozen window's T1 gloss + source + (optionally L0) as the model's grounding input."""
    t1_gloss = {}
    source = {}
    for unit in WINDOW:
        cur = R.current("SOURCE", unit)
        if cur:
            source[unit] = cur["payload"].get("verse", "")[:400]
        t1 = R.current("T1", unit)
        if t1:
            toks = (t1.get("payload", {}).get("t1", {}) or {}).get("tokens", [])
            t1_gloss[unit] = " ".join((t.get("gloss") or t.get("form") or "") for t in toks)[:600]
    return {"source": source, "t1_gloss": t1_gloss}


def _build_prompt(ctx: dict) -> str:
    src = "\n".join(f"## {u}\n{s}" for u, s in ctx["source"].items())
    gloss = "\n".join(f"## {u} T1\n{g}" for u, g in ctx["t1_gloss"].items())
    return (
        "You are the Pāṭala argument-map producer. Reconstruct the ARGUMENT of the following IPVV "
        "passage (the apohana / ahaṃ-pratyavamarśa discussion: is the 'I'-recollection a construction?)\n"
        "This is a CONTIGUOUS WINDOW (kārikās 1-5) — the objection, reply and crux may span several units; "
        "do NOT cut the argument short at a unit boundary.\n"
        "Produce EXACTLY 4 sections:\n"
        "1. what_is_at_issue: the question + the move, 1-3 sentences.\n"
        "2. argument_steps: the argument step by step (the objection -> reply -> the crux).\n"
        "3. open_items: genuinely unresolved items (status OPEN|NEEDS_REVIEW).\n"
        "4. decision_for_l2: one sentence guiding the readable L2.\n"
        "Return JSON ONLY: {\"what_is_at_issue\":\"...\",\"argument_steps\":[\"...\"],"
        "\"open_items\":[{\"text\":\"...\",\"status\":\"OPEN|NEEDS_REVIEW\"}],\"decision_for_l2\":\"...\"}\n\n"
        f"# SOURCE (Sanskrit, the window)\n{src}\n"
        f"# T1 GLOSS (per unit)\n{gloss}\n"
        "GROUNDING RULE: every argument step must cite a line/unit/kārikā; do not invent a premise the "
        "text doesn't license."
    )


def _parse(raw: str) -> dict:
    raw = (raw or "").strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0]
    s, e = raw.find("{"), raw.rfind("}")
    return json.loads(raw[s:e + 1])


def generate() -> dict:
    ctx = _gather_context()
    # the gold MUST NOT be retrieved (no-leakage); only source/T1/instructions
    prompt = _build_prompt(ctx)
    raw = chat("You are the Pāṭala argument-map producer (no gold retrieval; only the given source).",
               prompt, timeout=240)
    body = _parse(raw)
    cand = {
        "pilot_id": PILOT["pilot_id"],
        "window": WINDOW,
        "argument_map": {
            "what_is_at_issue": (body.get("what_is_at_issue") or "").strip(),
            "argument_steps": [s for s in (body.get("argument_steps") or []) if isinstance(s, str) and s.strip()],
            "open_items": body.get("open_items") or [],
            "decision_for_l2": (body.get("decision_for_l2") or "").strip(),
        },
        "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest(),
        "model": "deepseek-v4-flash",
        "no_gold_leakage": True,
        "status": "MACHINE_PROPOSED",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(cand, f, indent=2, ensure_ascii=False)
    return cand


if __name__ == "__main__":
    c = generate()
    am = c["argument_map"]
    print(f"ARGMAP candidate for {c['pilot_id']} (no gold leakage):")
    print(f"  what_is_at_issue: {am['what_is_at_issue'][:90]}")
    print(f"  steps: {len(am['argument_steps'])}, open: {len(am['open_items'])}")
    for s in am["argument_steps"]:
        print(f"    - {s[:90]}")
    print(f"  wrote {OUT}")
