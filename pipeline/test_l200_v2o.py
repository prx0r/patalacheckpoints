#!/usr/bin/env python3
"""pipeline/test_l200_v2o.py — L200 constrained compiler on the REAL IPVV V2-O exemplar.

Feeds the actual hand-authored V2-O L1 ground + L2 published reading into my constrained
classifier and compares the produced MT/IA against the canonical `l200/V2O-saptamo-vimarsa.md`
exemplar (the reference standard). Also checks the derivation map binds L0/source/argmap.

This is a live-model test (hermes). Run in the background, tail the log.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import l200_worker as LW

STACK = Path("/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv")
EXEMPLAR = STACK / "l200" / "V2O-saptamo-vimarsa.md"


def t(name, cond, detail=""):
    print(("PASS" if bool(cond) else "FAIL"), "-", name, (f" [{detail}]" if detail else ""), flush=True)
    return bool(cond)


def _mt_types(md: str) -> set:
    import re
    body = md.split("## 3. MATERIAL TRANSLATION DECISIONS")[-1].split("## 4.")[0]
    return set(re.findall(r"\b(SUPPLIED|REFERENT_SUPPLY|STRUCTURAL_CONNECTIVE|LEXICAL|GRAMMATICAL)\b", body))


def main() -> int:
    ok = True
    # the real V2-O L2 published reading (the freestyle read)
    l2_text = (STACK / "pilot" / "pilot_V2O_L2_read.md").read_text(encoding="utf-8")
    # the grounded L1 (controlled reading of kārikā 1 + the plan, from the arg map + L0)
    l1_text = ("the powers knowledge memory removal are established; a power needs a support; "
               "the support is the maheśvara whose essence is the freedom of joining separating "
               "resting concealing manifesting; not the inert fire-like; the pratibhā is the "
               "flashing seasoned with the order of the word-objects; its support is the order-less "
               "infinite-consciousness-form knower; that knower is the great Lord")

    print("=== L200 vs canonical V2-O exemplar (live constrained classifier) ===", flush=True)
    cands = LW._generate_candidates(l1_text, l2_text)
    print(f"candidates generated: {len(cands)}", flush=True)
    status, mt, ia, open_items = LW._classify_candidates("IPVV:V2O", cands)
    ok &= t("classifier COMPLETE", status == "COMPLETE", status)

    ex_types = _mt_types(EXEMPLAR.read_text(encoding="utf-8"))
    my_types = {m["type"] for m in mt}
    ok &= t("MT types valid taxonomy", my_types <= set(LW.MT_TYPES), f"mine={sorted(my_types)}")
    load_bearing = {"LEXICAL", "STRUCTURAL_CONNECTIVE", "SUPPLIED", "GRAMMATICAL", "REFERENT_SUPPLY"}
    recalled = load_bearing & my_types
    ok &= t("recalls canonical load-bearing MT types", len(recalled) >= 2,
            f"recalled={sorted(recalled)} canonical={sorted(ex_types)}")
    print("   MT produced:", json.dumps(mt, ensure_ascii=False)[:600], flush=True)
    print("   IA produced:", json.dumps(ia, ensure_ascii=False)[:400], flush=True)
    print("   OPEN:", json.dumps(open_items, ensure_ascii=False)[:200], flush=True)

    # derivation map binding (IPVV §2 shape)
    dm = LW._derivation_map(l2_text, l1_text, "IPVV:V2O")
    ok &= t("derivation map binds argmap+l0+source", bool(dm) and all(
        d.get("argument_map_segment") and d.get("source_range") for d in dm[:3]),
        f"{len(dm)} rows; first={dm[0] if dm else None}")

    print("\n" + ("L200 V2-O PASS" if ok else "L200 V2-O FAIL"), flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
