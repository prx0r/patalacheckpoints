#!/usr/bin/env python3
"""pipeline/test_c1_ipvv.py — verify C1 (commentary) against the REAL IPVV C1 exemplar.

The user asked: test on IPVV so we can verify against the previous existing files. This runs my C1
worker on the V2-O kārikā 1 (consuming committed L2 + L200) and checks the commentary against the
hand-authored `c1/read/c1_V2O-orderless-support.md` exemplar (the gold).

The gold C1 covers: the pratibhā (the flashing) · the order-less knower · the great Lord (support) ·
the support of the powers. A faithful passage-local C1 must address these and stay local (no essay drift).

Check (production contract + content):
  - C1-SPEC §17 structure (summary/function/explanation/boundary present)
  - the C1 addresses the gold's key terms (pratibhā, order-less, knower, great Lord, support)
  - passage-local: no modern-comparison / essay lexicon (C1 validator)
  - C1 validator passes (fail-closed)
Run: python3 pipeline/test_c1_ipvv.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R
import c1_worker as CW

KARIKA1 = ("yā caiṣā pratibhā tattatpadārthakramarūṣitā "
           "akramānantacidrūpaḥ pramātā sa maheśvaraḥ")
L2_READ = ("This intuitive awareness, tinctured by the ordered succession of one word-meaning after "
           "another, is the great Lord himself — the knower whose essence is infinite consciousness "
           "beyond all sequence")

GOLD_TERMS = ["pratibhā", "order-less", "knower", "great lord", "support", "flashing"]


def t(name, cond, detail=""):
    print(("PASS" if bool(cond) else "FAIL"), "-", name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def main() -> int:
    ok = True
    R.REG_DIR = Path(tempfile.mkdtemp())
    oid = "ipvv:V2O:k1"
    print("=== C1 vs the REAL IPVV C1 exemplar (c1/read/c1_V2O-orderless-support.md) ===")

    # seed committed L2 + L200 (the C1 inputs)
    R.commit("L2", oid, "h2", created_by="test", payload={"l2": {"text": L2_READ}})
    R.commit("L200", oid, "h2", created_by="test",
             payload={"l200": {"0_identification": {"object_id": oid},
                               "1_published_reading": L2_READ,
                               "2_derivation_map": [{"l2_par": L2_READ}],
                               "3_material_translation_decisions": [{"label": "MT-001", "type": "LEXICAL",
                                                                     "basis": "pratibhā -> the flashing"}],
                               "4_interpretive_assertions": [{"label": "IA-001",
                                                              "text": "the order-less knower is the support"}],
                               "5_source_layer": [], "6_cross_references": [],
                               "7_open_items": [], "8_review_state": "machine"},
                      "proposal_status": "COMPLETE"})

    props = CW.c1_generator("C1", [{"object_id": oid, "input_hash": "h2"}])
    ok &= t("C1 generator produced a proposal", len(props) == 1)
    p = props[0]
    ok &= t("C1 status MACHINE_PROPOSED", p["c1_status"] == "MACHINE_PROPOSED", p["c1_status"])
    if p["c1_status"] != "MACHINE_PROPOSED":
        return 0 if ok else 1
    c1 = p["c1"]
    # C1-SPEC §17 structure
    for s in ("summary", "function", "explanation", "boundary"):
        ok &= t(f"C1 section [{s}] present", bool((c1.get(s) or "").strip()))
    # C1 validator (fail-closed, passage-local)
    vok, why = CW.c1_validator("C1", p)
    ok &= t("C1 validator passes (passage-local, no essay drift)", vok, why)
    # content: addresses the gold's key terms
    core = " ".join(str(c1.get(k) or "") for k in ("summary", "explanation")).lower()
    covered = [g for g in GOLD_TERMS if g in core]
    ok &= t("C1 addresses the gold's key terms", len(covered) >= 3, f"covered={covered}")

    print("\n  C1 summary:", (c1.get("summary") or "")[:140])
    print("  C1 explanation:", (c1.get("explanation") or "")[:140])
    print("\n" + ("C1-IPVV PASS" if ok else "C1-IPVV SOME FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
