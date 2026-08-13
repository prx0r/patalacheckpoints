#!/usr/bin/env python3
"""pipeline/extract_arguments_from_essays.py — work BACKWARD: real scholar essays -> gold-compatible
logical arguments + synthesis, run through the EXISTING Pāṭala machinery.

The user's framing: "work backwards from existing essays ... we care more about the logical arguments
and synthesis and education." The research-library has 90+ real scholar essays that ALREADY carry the
logical-argument structure (pratijñā/hetu/udāharana/nigamana, SUPPORT/FALSIFIER/VERDICT, debate
ROUNDS). These are real hard-data arguments — far more real than forward-generating ARGMAP from
Sanskrit through the factory.

CRITICAL: this does NOT reinvent machinery. It emits gold-COMPATIBLE dicts (the same `nodes` +
`inferences` shape as gold002.py) so the output plugs straight into the EXISTING:
    - nyayagate.gate_claim / validate
    - crux_engine.build_crux_layer
    - synthesis_core.build_synthesis_from_gold
    - argument_recovery_bench.score_recovery (against frozen gold)

Usage:
    python3 pipeline/extract_arguments_from_essays.py --essay <path> [--emit gold|full]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

sys.path.insert(0, "/root/projects/patala/machinelearning/research")
from patala_ml.nyayagate import gate_claim  # noqa: E402
from patala_ml.crux_engine import build_crux_layer  # noqa: E402

# ── the essay's dialectical structure (the LOGICAL-ARGUMENT-1 format) ─────────
_ROUND_RE = re.compile(r"^## .*?(?:ROUND|round)\s*\d+", re.M)
_CLAIM_RE = re.compile(r"\*\*THE CLAIM[:\*]*\*\*?\s*(.+)", re.I)
_HETU_RE = re.compile(r"\*\*HETU[:\*]*\*\*?\s*(.+)", re.I)
_UDAHARA_RE = re.compile(r"\*\*UDAHARANA[:\*]*\*\*?\s*(.+)", re.I)
_UPANAYA_RE = re.compile(r"\*\*UPANAYA[:\*]*\*\*?\s*(.+)", re.I)
_NIGAMANA_RE = re.compile(r"\*\*NIGAMANA[:\*]*\*\*?\s*(.+)", re.I)
_SUPPORT_RE = re.compile(r"\*\*SUPPORT[:\*]*\*\*?\s*(.+)", re.I)
_FALSIFIER_RE = re.compile(r"\*\*FALSIFIER[:\*]*\*\*?\s*(.+)", re.I)
_VERDICT_RE = re.compile(r"\*\*VERDICT[:\*]*\*\*?\s*\[?(\w+)\]?\s*[—\-:]\s*(.+)", re.I)
_PRATIJNA_RE = re.compile(r"\*\*PRATIJÑA[:\*]*\*\*?\s*(.+)", re.I)


def _clean(s):
    return " ".join((s or "").split()).strip()


def _find_first(text, pattern):
    m = pattern.search(text)
    return m.group(1) if m else None


def _find_verdict(block):
    m = _VERDICT_RE.search(block)
    return {"status": m.group(1).lower(), "note": _clean(m.group(2))} if m else None


def _speaker_of(text):
    low = (text or "").lower()
    if any(k in low for k in ("buddhist", "opponent", "the rival", "dignāga", "dharmakīrti",
                              "nanu", "one might", "objection")):
        return "opponent"
    return "author"


def _explicitness_of(text):
    low = (text or "").lower()
    if any(k in low for k in ("the claim", "we hold", "our view", "abhinavagupta", "utpaladeva")):
        return "EXPLICIT"
    if any(k in low for k in ("reconstruct", "it can be", "one can", "plausibly", "we infer")):
        return "RECONSTRUCTED"
    return "EXPLICIT"


def extract_essay_to_gold(path: str, work_id: str = "scholar-essay") -> dict:
    """Extract a real essay into a gold-COMPATIBLE dict (nodes + inferences + boundary + debate_frame).

    Emits the SAME shape as gold002.py so the output feeds the existing synthesis/crux/gate machinery.
    """
    text = open(path, encoding="utf-8").read()
    pratijna = _clean(_find_first(text, _PRATIJNA_RE))
    nigamana = _clean(_find_first(text, _NIGAMANA_RE))
    research_question = pratijna or nigamana or _clean(_find_first(text, _CLAIM_RE))

    spans = list(_ROUND_RE.finditer(text))
    round_blocks = []
    for i, m in enumerate(spans):
        end = spans[i + 1].start() if i + 1 < len(spans) else len(text)
        round_blocks.append(text[m.start():end])

    nodes = []
    inferences = []
    attacks = []
    verdicts = []
    for i, block in enumerate(round_blocks):
        r = i + 1
        claim = _clean(_find_first(block, _CLAIM_RE))
        hetu = _clean(_find_first(block, _HETU_RE))
        udahara = _clean(_find_first(block, _UDAHARA_RE))
        falsifier = _clean(_find_first(block, _FALSIFIER_RE))
        verdict = _find_verdict(block)

        # CLAIM -> a thesis node
        if claim:
            nodes.append({"proposition_id": f"E{r}:CLAIM", "text": claim, "kind": "THESIS",
                          "explicitness": _explicitness_of(claim), "commitment": "ASSERTS",
                          "speaker": _speaker_of(claim), "derived_from": "ESSAY", "status": "MACHINE_PROPOSED"})
        # HETU -> a premise node (the reason)
        if hetu:
            nodes.append({"proposition_id": f"E{r}:HETU", "text": hetu, "kind": "PREMISE",
                          "explicitness": _explicitness_of(hetu), "commitment": "ASSERTS",
                          "speaker": _speaker_of(hetu), "derived_from": "ESSAY", "status": "MACHINE_PROPOSED"})
        # UDAHARANA -> an example node
        if udahara:
            nodes.append({"proposition_id": f"E{r}:UDAHARANA", "text": udahara, "kind": "EXAMPLE",
                          "explicitness": _explicitness_of(udahara), "commitment": "ASSERTS",
                          "speaker": _speaker_of(udahara), "derived_from": "ESSAY", "status": "MACHINE_PROPOSED"})
        # FALSIFIER -> an objection node (opponent)
        if falsifier:
            nodes.append({"proposition_id": f"E{r}:FALSIFIER", "text": falsifier, "kind": "OBJECTION",
                          "explicitness": "EXPLICIT", "commitment": "ATTRIBUTES_TO_OPPONENT",
                          "speaker": "opponent", "derived_from": "ESSAY", "status": "MACHINE_PROPOSED"})
        # the inference: claim + hetu -> verdict
        if claim and hetu and verdict:
            inferences.append({
                "inference_id": f"E{r}:INF",
                "premise_ids": [f"E{r}:CLAIM", f"E{r}:HETU"],
                "conclusion_ids": [f"E{r}:VERDICT"],
                "scheme": "SUPPORT",
                "warrant": "RECONSTRUCTED_WARRANT: the round supports its verdict by the claim+reason "
                           "(editorial reconstruction from the essay's own argument)",
                "warrant_status": "EDITORIAL_RECONSTRUCTION",
            })
            nodes.append({"proposition_id": f"E{r}:VERDICT", "text": verdict["note"], "kind": "CONCLUSION",
                          "explicitness": "EXPLICIT", "commitment": "ASSERTS",
                          "speaker": "author", "derived_from": "ESSAY", "status": "MACHINE_PROPOSED"})
            verdicts.append({"round": r, "verdict": verdict["status"]})
        if falsifier:
            attacks.append({"attacker": f"E{r}:FALSIFIER", "target_premise": f"E{r}:HETU",
                            "type": "UNDERMINE"})

    gold = {
        "gold_id": os.path.basename(path).replace(".md", ""),
        "work_id": work_id,
        "title": os.path.basename(path).replace(".md", ""),
        "passage": "scholar-essay (backward extraction)",
        "nodes": nodes,
        "inferences": inferences,
        "attacks": attacks,
        "boundary": {"does_not_establish": ["a universal Self (the debate leaves the ground open)"]},
        "debate_frame": {"question": research_question, "rounds": len(round_blocks),
                         "verdicts": verdicts},
        "status": "MACHINE_PROPOSED",
    }
    return gold


def run_existing_machinery(gold: dict) -> dict:
    """Push an extracted essay through the EXISTING nyaya-gate + crux machinery (no new ontology)."""
    # 1. nyaya gate on each claim (the existing bounded structural gate)
    gate = {}
    for n in gold["nodes"]:
        claim = {"text": n["text"], "commitment": n.get("commitment", "ASSERTS"),
                 "proposition_id": n["proposition_id"]}
        r = gate_claim(claim, [{"text": x["text"]} for x in gold["nodes"]])
        gate[n["proposition_id"]] = r.to_dict() if hasattr(r, "to_dict") else str(r)

    # 2. crux layer over the essay's arguments (the existing perturbation crux engine)
    arguments = [{"argument_id": gold["gold_id"], "inferences": gold["inferences"]}]
    # build_crux_layer expects Proposition objects; adapt minimally
    from patala_ml.proposition_layer import from_gold_node
    propositions = [from_gold_node(n, gold["gold_id"], "essay") for n in gold["nodes"]]
    try:
        cruxes = build_crux_layer(arguments, propositions, gold["nodes"])
    except Exception as e:
        cruxes = {"error": str(e)[:80]}

    return {"gate": gate, "crux_layer": cruxes,
            "n_nodes": len(gold["nodes"]), "n_inferences": len(gold["inferences"]),
            "n_attacks": len(gold.get("attacks", []))}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--essay", default="/root/projects/research-library/LOGICAL-ARGUMENT-1-reflexivity-debate.md")
    ap.add_argument("--emit", choices=["gold", "full"], default="gold")
    a = ap.parse_args()
    gold = extract_essay_to_gold(a.essay)
    mach = run_existing_machinery(gold)
    print(f"Extracted real essay -> gold-compatible argument:")
    print(f"  nodes={mach['n_nodes']} inferences={mach['n_inferences']} attacks={mach['n_attacks']}")
    print(f"  research_question: {gold['debate_frame']['question'][:80]}")
    print(f"  nyaya-gate: {len(mach['gate'])} claims gated")
    print(f"  crux-layer: {json.dumps(mach['crux_layer'], ensure_ascii=False)[:160]}")
    if a.emit == "gold":
        print("\n--- EMITTED GOLD (feeds build_synthesis_from_gold) ---")
        print(json.dumps(gold, indent=2, ensure_ascii=False)[:1500])
