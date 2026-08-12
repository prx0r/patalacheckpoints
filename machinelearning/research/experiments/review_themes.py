#!/usr/bin/env python3
"""review_themes.py — MODEL review of the three CP3 candidate themes (kind + coarse sense judgments).

Produces THEME-REVIEW-001..003: the same three-judgment output the packet asks of a human reviewer
(membership / kind / sense), rendered as an explicit ReviewEvent for a MODEL reviewer. It is a
RECONSTRUCTION-consistency review against the C1 material — NOT specialist philological adjudication.

Per the reviewer's framing: a RETYPE is a SUCCESS. This review tests whether the three candidates are
the same kind — they are suspected to differ (LOCAL_THEME / CONCEPT_TERM_FAMILY / DOCTRINAL_PROBLEM_DOMAIN).

Run: cd research && . .venv/bin/activate && python experiments/review_themes.py
"""
from __future__ import annotations
import json
import os

OUT_DIR = "/root/projects/patala/benchmarks/v0/review"

REVIEWER = {"kind": "AI_MODEL", "name": "GPT-5.6 Sol", "independence": "EXTERNAL_TO_BUILDER_AGENT",
            "scope": "THEME_KIND_AND_SENSE", "source_basis": "C1_L2_PACKET + theme-map-ipvv-v0"}

# the model review of each candidate: membership / kind / per-lemma sense / decision
REVIEWS = [
    {
        "review_id": "THEME-REVIEW-001", "target": "Order-less Support", "status": "MODEL_REVIEWED",
        "membership": {
            "confirm": ["V2L-nonconstructed-I", "V2N-inner-appearance", "V2O-orderless-support",
                        "V2P-pramatr-vyapara", "V2Q-omniscient", "V2R-mahesvarya", "V2S-unity-mahesvarya"],
            "questionable": ["V3F-grace (belongs to a grace/attainment strand)", "V3I-difference-real (action/unified-consciousness)"],
            "missing": ["V2A-memory-lords-power (the powers incl. memory)"],
        },
        "kind": {"narrowest_adequate": "LOCAL_THEME", "why": "one interpretive/doctrinal strand — the "
                 "one-support of the powers, order-less — instantiated across V2L..V2S; an argument "
                 "organizes it (ARG-001/003) but it is a theme, not a concept."},
        "sense": [
            {"lemma": "āśraya (support)", "judgment": "NEAR_SAME", "note": "the support of the powers is "
             "consistently the order-less knower across V2O..V2S"},
            {"lemma": "akrama / order-less", "judgment": "SAME_SENSE", "note": "the order-less character "
             "of the support is uniform in V2O"},
            {"lemma": "pratibhā (flashing)", "judgment": "NEAR_SAME", "note": "the flashing is the "
             "support's form; consistent"},
        ],
        "decision": "REVISE", "reason": "strong local theme; tighten membership (V3F/V3I likely belong "
        "elsewhere) + add V2A.",
    },
    {
        "review_id": "THEME-REVIEW-002", "target": "Vimarśa", "status": "MODEL_REVIEWED",
        "membership": {
            "confirm": ["V2H-vimarsa-paravak", "V2I-sphuratta", "V2J-samskara", "V2K-vacakasphota"],
            "questionable": ["V2J-samskara is memory-seeding, adjacent to vimarśa but a distinct function"],
            "missing": ["V2N-inner-appearance, V2L-nonconstructed-I (reflexive awareness appears there too)"],
        },
        "kind": {"narrowest_adequate": "CONCEPT_TERM_FAMILY", "why": "vimarśa / sphurattā / samskāra / "
                 "vākāsphoṭa are a technical term family around reflexive awareness (parā-vāk), not one "
                 "local argument or one coherent theme."},
        "sense": [
            {"lemma": "vimarśa (reflexive awareness)", "judgment": "NEAR_SAME", "note": "reflexive "
             "awareness is the constant; but it is used across different contexts"},
            {"lemma": "sphurattā (throbbing)", "judgment": "AMBIGUOUS", "note": "the throbbing is "
             "language/paśyantī in V2I vs the self-grasp elsewhere"},
            {"lemma": "parā-vāk (supreme speech)", "judgment": "NOT_ENOUGH_CONTEXT", "note": "appears in "
             "few members; needs more context to judge"},
        ],
        "decision": "RETYPE", "reason": "CONCEPT_TERM_FAMILY, not a local theme — a RETYPE is the success "
        "here.",
    },
    {
        "review_id": "THEME-REVIEW-003", "target": "Pramāṇa", "status": "MODEL_REVIEWED",
        "membership": {
            "confirm": ["V2D-jnanasakti", "V2E-external-inferred", "V2F-other-minds", "V3H-inference-across-knowers"],
            "questionable": ["V3H is a distinct vimarśa (inference-across-knowers), not a single pramāṇa "
                             "strand"],
            "missing": ["V1L-yogipratyaksa, V2P-pramatr-vyapara (pramāṇa as the knower's operation)"],
        },
        "kind": {"narrowest_adequate": "DOCTRINAL_PROBLEM_DOMAIN", "why": "pramāṇa as a doctrinal "
                 "problem-domain spans knowledge-power, inference of externals/other minds, and "
                 "inference-across-knowers — cross-cutting, not a local theme."},
        "sense": [
            {"lemma": "pramāṇa (means of knowledge)", "judgment": "NEAR_SAME", "note": "the means of "
             "knowledge is a stable doctrinal target"},
            {"lemma": "anumāna (inference)", "judgment": "AMBIGUOUS", "note": "inference appears in "
             "distinct sub-domains (externals, other minds, across knowers)"},
        ],
        "decision": "RETYPE", "reason": "DOCTRINAL_PROBLEM_DOMAIN, not a local theme — a RETYPE is the "
        "success here.",
    },
]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for r in REVIEWS:
        r["reviewer"] = REVIEWER
        r["status_note"] = "MODEL review of kind + coarse sense. NOT specialist philological adjudication."
        f = os.path.join(OUT_DIR, f"{r['review_id']}.json")
        json.dump(r, open(f, "w"), indent=2, ensure_ascii=False)
        print(f"wrote {f}")
        print(f"  {r['target']}: kind={r['kind']['narrowest_adequate']}  decision={r['decision']}")
        for s in r["sense"]:
            print(f"    sense[{s['lemma']}] = {s['judgment']}")


if __name__ == "__main__":
    main()
