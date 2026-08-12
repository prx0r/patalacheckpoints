#!/usr/bin/env python3
"""check_review_packet.py — the hard acceptance gate for the rebuilt ARG-GOLD review packet.

Enforces that every proposed proposition points DOWNWARD to primary Sanskrit evidence, NOT through L2:

    Proposition  --GROUNDED_IN-->  L0/SourceSpan  -->  Sanskrit

The L2 must never be an intermediate authority for a review decision. The gate is mechanical:

    for every proposed proposition:   >=1 primary Sanskrit SourceSpan resolves
    for every inference:              all premise proposition refs resolve
    for every Sanskrit citation:      exact span resolves to L0/P0-backed source
    L2 dependence required for judgment: ZERO
"""
from __future__ import annotations

import json
import os
import sys

IPVV = "/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv"
L0_DIR = os.path.join(IPVV, "l0")

# passage_id -> the L0 chunk file that carries its primary Sanskrit analysis floor
CHUNK_BY_PASSAGE = {
    "pt:passage:ipvv:chunkV2-O-saptamo-vimarsa.md": "chunkV2-O-saptamo-vimarsa",
    "pt:passage:ipvv:chunkV2-L-sastho-vimarsa-smrti-apohana.md": "chunkV2-L-sastho-vimarsa-smrti-apohana",
    "pt:passage:ipvv:chunkV2-H-pancamo-vimarsa-k11-13.md": "chunkV2-H-pancamo-vimarsa-k11-13",
    "pt:passage:ipvv:chunkV3-I-kriya-caturtho-close-k20-21.md": "chunkV3-I-kriya-caturtho-close-k20-21",
}


def load_l0(chunk: str) -> dict[str, dict]:
    p = os.path.join(L0_DIR, f"{chunk}.l0.jsonl")
    if not os.path.exists(p):
        return {}
    out = {}
    for line in open(p, encoding="utf-8"):
        if line.strip():
            r = json.loads(line)
            out[r["id"]] = r
    return out


def check_packet(packet_path: str) -> dict:
    problems = []
    with open(packet_path, encoding="utf-8") as f:
        packet = json.load(f)

    l0_cache = {}
    def chunk_for(passage_id):
        chunk = CHUNK_BY_PASSAGE.get(passage_id, "")
        if chunk and chunk not in l0_cache:
            l0_cache[chunk] = load_l0(chunk)
        return chunk

    for arg in packet.get("arguments", []):
        gid = arg.get("gold_id", "?")
        propositions = arg.get("propositions", [])
        prop_ids = {p.get("proposition_id") for p in propositions}

        # (1) every proposition has >=1 resolving primary Sanskrit span
        for p in propositions:
            spans = p.get("primary_evidence", [])
            if not spans:
                problems.append(f"{gid}/{p.get('proposition_id')}: no primary_evidence spans")
                continue
            resolved = 0
            for span in spans:
                chunk = chunk_for(span.get("passage_id", ""))
                if chunk and span.get("span_id") in l0_cache[chunk]:
                    resolved += 1
            if resolved == 0:
                problems.append(f"{gid}/{p.get('proposition_id')}: no primary span resolves "
                                f"(spans: {[s.get('span_id') for s in spans]})")

        # (2) every inference's premise refs resolve
        for inf in arg.get("inferences", []):
            for pid in inf.get("premise_ids", []) + inf.get("conclusion_ids", []):
                if pid not in prop_ids:
                    problems.append(f"{gid}/{inf.get('inference_id')}: premise/conclusion {pid} missing")

        # (3) every Sanskrit citation's exact span resolves to L0/P0-backed source
        for cite in arg.get("sanskrit_citations", []):
            chunk = chunk_for(cite.get("passage_id", ""))
            if chunk and cite.get("span_id") not in l0_cache[chunk]:
                problems.append(f"{gid}: citation span {cite.get('span_id')} does not resolve")

        # (4) L2 must not be required for judgment
        if arg.get("l2_required_for_judgment"):
            problems.append(f"{gid}: L2 marked as required for judgment (must be ZERO)")

    return {"ok": len(problems) == 0, "problems": problems}


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_review_packet.py <packet.json>")
        return 1
    r = check_packet(sys.argv[1])
    if r["ok"]:
        print("REVIEW PACKET GATE: PASS — every proposition grounds to primary Sanskrit; L2 not required.")
        return 0
    print("REVIEW PACKET GATE: FAIL")
    for p in r["problems"]:
        print(f"  ✗ {p}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
