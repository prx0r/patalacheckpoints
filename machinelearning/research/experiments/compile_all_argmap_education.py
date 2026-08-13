#!/usr/bin/env python3
"""experiments/compile_all_argmap_education.py — compile education packets from ALL real ARGMAPs.

The education vision (Pāṭala Education) requires education to be a PROJECTION of Pāṭala objects.
Now that 50 real ARGMAP objects exist (49 ingested IPVV golds + the factory object), compile a
LearningPacket for every real argument so the education layer is populated from real data, not just
the single hand-built VERTICAL-1 object.

Output: benchmarks/v0/review/ALL-ARGMAP-EDUCATION-PACKETS.json
        (packet per ARGMAP object + a summary of skills/misconceptions covered)
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "patala_ml"))
from education_ir import compile_interactions  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))
REG = os.path.join(ROOT, "data/corpus/registries/argmap-registry.jsonl")


def argmap_to_convergence_object(row: dict) -> dict:
    am = row["payload"].get("argument_map", {})
    oid = row["object_id"]
    steps = am.get("argument_steps", [])
    return {
        "object_id": oid,
        "research_question": am.get("what_is_at_issue", "")[:300],
        "propositions": [{"id": f"s{i}", "commitment": s[:200], "speaker": "author"}
                         for i, s in enumerate(steps[:4])],
        "arguments": [{"inferences": [{"inference_id": f"INF-{oid}", "premise_ids": [f"s{i}" for i in range(len(steps[:4]))],
                                       "conclusion_ids": [f"C-{oid}"]}]}] if steps else [],
        "cruxes": [{"crux_id": f"CRUX-{oid}",
                    "question": f"Decisive unresolved crux of {oid}: the load-bearing point the argument turns on"}],
        "boundary": {"does_not_establish": ["a universal Self (not established by a per-passage argument)"]},
        "source_refs": [f"pt:passage:ipvv:{oid.split(':')[-1]}"] if oid.startswith("ipvv:") else [],
        "epistemic_ceiling": "MACHINE_PROPOSED",
    }


def main() -> int:
    rows = [json.loads(l) for l in open(REG, encoding="utf-8") if l.strip()]
    packets = []
    skills = set()
    misconceptions = set()
    for r in rows:
        obj = argmap_to_convergence_object(r)
        pkt = compile_interactions(obj, ["CLASSIFY_SPEAKER", "ATTACH_PREMISE", "IDENTIFY_CRUX",
                                         "QUALIFY_SCOPE", "RECONSTRUCT_WARRANT"], "introductory")
        packets.append({"object_id": r["object_id"], "status": r.get("status"),
                        "interaction_count": pkt["interaction_count"],
                        "learning_skills": pkt["learning_skills"],
                        "misconceptions": [m["type"] for m in pkt["misconceptions"]]})
        skills.update(pkt["learning_skills"])
        for m in pkt["misconceptions"]:
            misconceptions.add(m["type"])

    summary = {
        "total_argmaps": len(packets),
        "total_interactions": sum(p["interaction_count"] for p in packets),
        "skills_covered": sorted(skills),
        "misconception_families_covered": sorted(misconceptions),
        "packets": packets,
    }
    out = os.path.join(ROOT, "benchmarks/v0/review/ALL-ARGMAP-EDUCATION-PACKETS.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"Education packets from {len(packets)} real ARGMAPs")
    print(f"  total interactions: {summary['total_interactions']}")
    print(f"  skills covered: {summary['skills_covered']}")
    print(f"  misconception families: {summary['misconception_families_covered']}")
    print(f"  wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
