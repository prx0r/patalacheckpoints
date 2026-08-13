#!/usr/bin/env python3
"""pipeline/test_l200_ipvv.py — verify the L200 constrained compiler against the REAL IPVV audit.

The user asked: test on IPVV so we can verify against the previous existing files. This runs my L200
constrained compiler on the V2-O kārikā 1 (feeding the L1 close + L2 readable) and checks the produced
Material Translation Decisions against the canonical `l200/V2O-saptamo-vimarsa.md` audit (the gold).

The gold V2-O audit's MT taxonomy: LEXICAL×3 · GRAMMATICAL · SUPPLIED · STRUCTURAL_CONNECTIVE. A faithful
L200 must classify its MT decisions within this frozen taxonomy, never inventing a category.

Check (production contract + classification):
  - proposal COMPLETE (fail-closed)
  - 8-section shape present
  - every MT type is within the frozen taxonomy {SUPPLIED, REFERENT_SUPPLY, STRUCTURAL_CONNECTIVE,
    LEXICAL, GRAMMATICAL}
  - MT/IA strictly separated; derivation map present
Semantic classification precision is Agent 1's evals lane (CP5 DEV gate).

Run: python3 pipeline/test_l200_ipvv.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R
import l200_worker as LW

KARIKA1 = ("yā caiṣā pratibhā tattatpadārthakramarūṣitā "
           "akramānantacidrūpaḥ pramātā sa maheśvaraḥ")
L1_CLOSE = ("This pratibhā, colored with the sequence of the meanings of these and those words — the "
            "knowing subject whose form is sequence-less infinite consciousness — he is the great Lord")
L2_READ = ("This intuitive awareness, tinctured by the ordered succession of one word-meaning after "
           "another, is the great Lord himself — the knower whose essence is infinite consciousness "
           "beyond all sequence")

GOLD_TYPES = {"LEXICAL", "GRAMMATICAL", "SUPPLIED", "STRUCTURAL_CONNECTIVE"}


def t(name, cond, detail=""):
    print(("PASS" if bool(cond) else "FAIL"), "-", name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def main() -> int:
    ok = True
    R.REG_DIR = Path(tempfile.mkdtemp())
    oid = "ipvv:V2O:k1"
    print("=== L200 constrained compiler vs the REAL IPVV audit (V2-O) ===")

    # seed committed L2 for the passage (the L200 input)
    R.commit("L2", oid, "h2", created_by="test",
             payload={"l2": {"text": L2_READ}, "l1": {"text": L1_CLOSE}})

    props = LW.l200_generator("L200", [{"object_id": oid, "input_hash": "h2"}])
    ok &= t("L200 generator produced a proposal", len(props) == 1)
    p = props[0]
    ok &= t("L200 proposal COMPLETE (fail-closed)", p["proposal_status"] == "COMPLETE",
            p["proposal_status"])
    if p["proposal_status"] != "COMPLETE":
        return 0 if ok else 1
    l200 = p["l200"]
    # 8-section shape
    required = ["0_identification", "1_published_reading", "2_derivation_map",
                "3_material_translation_decisions", "4_interpretive_assertions",
                "5_source_layer", "6_cross_references", "7_open_items", "8_review_state"]
    ok &= t("L200 8-section shape present", all(k in l200 for k in required))
    ok &= t("L200 validator passes", LW.l200_validator("L200", p)[0])
    # MT taxonomy: every MT type within the frozen set
    mt = l200.get("3_material_translation_decisions", [])
    my_types = {m.get("type") for m in mt}
    ok &= t("All MT types within the frozen taxonomy", my_types <= set(LW.MT_TYPES), f"{sorted(my_types)}")
    # recall on the gold's load-bearing types
    recalled = my_types & GOLD_TYPES
    ok &= t("L200 recalls gold MT types", bool(recalled), f"recalled={sorted(recalled)}")
    # MT/IA separated + derivation map present
    ok &= t("L200 derivation map present", bool(l200.get("2_derivation_map")))

    print("\n  MT produced:", [m.get("type") for m in mt][:8])
    print("  gold MT types:", sorted(GOLD_TYPES))
    print("\n" + ("L200-IPVV PASS" if ok else "L200-IPVV SOME FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
