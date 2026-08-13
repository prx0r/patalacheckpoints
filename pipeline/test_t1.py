#!/usr/bin/env python3
"""pipeline/test_t1.py — deterministic T1 layer tests (A2-CP1, transliteral word-gloss).

Covers the canonical T1 producer + its deterministic production gate, with the model stubbed:
  - canonical shape: `[and]-GLOSS (IAST)` form
  - source binding: every token's IAST surface appears in the source verse
  - coverage: every Vidyut/IAST token is represented
  - provenance: input_hash bound; status MACHINE_PROPOSED
  - fail-closed: model failure / bad JSON -> GENERATION_FAILED (never a partial commit)

This is the PRODUCTION gate (Agent 2's lane). Semantic quality evaluation is Agent 1's evals lane.
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, "/root/projects/patala/pipeline")

import t1_worker as TW


def t(name, cond, detail=""):
    print(("PASS" if bool(cond) else "FAIL"), "-", name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def main() -> int:
    ok = True
    verse = "śivo bhūtvā śivaṃ yajet"
    good = {"tokens": {"śivo": {"gloss": "the auspicious one", "quoted": False},
                       "bhūtvā": {"gloss": "having become", "quoted": False},
                       "śivaṃ": {"gloss": "the auspicious one (acc)", "quoted": False},
                       "yajet": {"gloss": "should worship", "quoted": False}}}

    print("=== T1 canonical shape + source binding (model stubbed) ===")
    TW.chat = lambda s, p, **kw: json.dumps(good)
    props = TW.t1_generator("T1", [{"object_id": "kramasadbhava:v1", "verse": verse}])
    ok &= t("T1 generator produced a proposal", len(props) == 1)
    p = props[0]
    ok &= t("T1 status MACHINE_PROPOSED", p["t1_status"] == "MACHINE_PROPOSED")
    tokens = p["t1"].get("tokens", [])
    ok &= t("T1 produces one token per source surface", len(tokens) == 4, f"{len(tokens)}")
    ok &= t("T1 forms are canonical [and]-GLOSS (IAST)",
            all("[and]-" in tk["form"] and f"({tk['surface']})" in tk["form"] for tk in tokens),
            [tk["form"] for tk in tokens])
    ok &= t("T1 surfaces all appear in source",
            all(tk["surface"].lower() in verse.lower() for tk in tokens))
    ok &= t("T1 input_hash bound", bool(p["input_hash"]))
    vok, why = TW.t1_validator("T1", p)
    ok &= t("T1 validator passes", vok, why)

    print()
    print("=== T1 fail-closed (model failure never commits) ===")
    TW.chat = lambda s, p, **kw: "not json {"
    bad = TW.t1_generator("T1", [{"object_id": "kramasadbhava:v1", "verse": verse}])[0]
    ok &= t("bad model output -> GENERATION_FAILED", bad["t1_status"] == "GENERATION_FAILED")
    ok &= t("GENERATION_FAILED blocked by validator", TW.t1_validator("T1", bad)[0] is False)

    print()
    print("=== T1 abstention (honest empty gloss is valid, not a fabrication) ===")
    abstain = {"tokens": {"śivo": {"gloss": "", "quoted": False},
                          "bhūtvā": {"gloss": "", "quoted": False},
                          "śivaṃ": {"gloss": "", "quoted": False},
                          "yajet": {"gloss": "", "quoted": False}}}
    TW.chat = lambda s, p, **kw: json.dumps(abstain)
    aprop = TW.t1_generator("T1", [{"object_id": "kramasadbhava:v1", "verse": verse}])[0]
    ok &= t("abstention (empty gloss) is valid canonical T1 (not fabricated)",
            TW.t1_validator("T1", aprop)[0] is True)

    print("\n" + ("T1 ALL PASS" if ok else "T1 SOME FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
