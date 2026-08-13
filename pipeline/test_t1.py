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
    # Agent 1's export contract: tokens carry sanskrit/iast/gloss/status (layer_contract.py)
    ok &= t("T1 tokens carry Agent-1 contract keys (sanskrit/iast/gloss/status)",
            all(all(k in tk for k in ("sanskrit", "iast", "gloss", "status")) for tk in tokens))
    ok &= t("T1 token status enum valid", all(tk["status"] in ("GLOSSED", "ABSTAIN") for tk in tokens))
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

    # G2 root-cause regression: retroflex ṇ must NOT split a lexical unit (gaṇeśaḥ, kāraṇam, śaktijanmā).
    # The old IAST_TOKEN char class omitted 'ṇ' (0x1e47), over-splitting gaṇeśaḥ -> ga + eśaḥ.
    buggy = "dantyāsyo'yaṃ haṭhādyaḥ śamayatu duritaṃ śaktijanmā gaṇeśaḥ || 1 ||"
    segs = TW._segment(buggy)
    surfaces = [s["surface"] for s in segs]
    ok &= t("gaṇeśaḥ stays one lexical unit (G2 EF-T1-0003 fix)",
            "gaṇeśaḥ" in surfaces and "ga" not in surfaces,
            f"{[s for s in surfaces if 'ga' in s or 'eśa' in s]}")
    ok &= t("śaktijanmā stays whole (G2 EF-T1-0003)",
            "śaktijanmā" in surfaces, surfaces)
    kara = "kāraṇam bhavati"  # kāra+am over-split (EF-T1-0002)
    ok &= t("kāraṇam stays whole (G2 EF-T1-0002)",
            "kāraṇam" in [s["surface"] for s in TW._segment(kara)])

    # G2 root-cause regression: vṛttimīśaḥ compound mis-gloss (EF-T1-2026-0004). The model strung
    # vṛtti+īśa literally as "the-mental-modification-the-Lord"; the worker fix parses it as a
    # sensible tatpuruṣa compound gloss.
    mangled = {"tokens": {"vṛttimīśaḥ": {"gloss": "the-mental-modification-the-Lord", "quoted": False}}}
    vseg = TW._segment("sanmārgālokanāya vyapanayatu sa vastāmasīṃ vṛttimīśaḥ || 2 ||")
    vout = TW._assemble_t1("sanmārgālokanāya vyapanayatu sa vastāmasīṃ vṛttimīśaḥ || 2 ||",
                           vseg, mangled["tokens"])
    vtok = next((tk for tk in vout if tk["surface"] == "vṛttimīśaḥ"), None)
    ok &= t("vṛttimīśaḥ compound gloss corrected (G2 EF-T1-0004)",
            vtok is not None and vtok["gloss"] == "the Lord who is the mental modification",
            vtok["gloss"] if vtok else "no token")
    ok &= t("vṛttimīśaḥ correction keeps canonical [and]- form",
            vtok is not None and "[and]-the Lord who is the mental modification (vṛttimīśaḥ)" in vtok["form"])

    print("\n" + ("T1 ALL PASS" if ok else "T1 SOME FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
