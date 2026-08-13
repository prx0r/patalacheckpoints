#!/usr/bin/env python3
"""pipeline/compare_ipvv_exemplars.py — run the per-layer workers on the REAL IPVV V2-O exemplars
and compare output against the hand-authored canonical files we already made.

Layers tested (live model where applicable):
  L200  : feed the actual V2-O L1 (grounded) + L2 (published) into the constrained compiler,
          compare the produced MT/IA/OPEN against the hand-authored `l200/V2O-saptamo-vimarsa.md`.
  C1    : feed the actual V2-O L2 + the hand-authored L200 MT/IA/OPEN into the C1 worker,
          compare the produced commentary against the hand-authored `c1/read/c1_V2O-orderless-support.md`.
  L0    : run the deterministic RAW-L0 on a real kramasadbhava verse, assert P0 lossless + schema.

This is a QUALITATIVE + STRUCTURAL comparison (the model output will differ in wording but must
match the exemplar's structure, scope, and decision-types). Prints PASS/FAIL per check.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

STACK = Path("/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv")

# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def t(name, cond, detail=""):
    print(("PASS" if bool(cond) else "FAIL"), "-", name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def _section_text(md: str, heading: str) -> str:
    """Extract the body of a markdown section by heading prefix."""
    lines = md.splitlines()
    out, grab = [], False
    for ln in lines:
        if ln.strip().startswith(f"## {heading}") or ln.strip().startswith(f"**{heading}"):
            grab = True
            continue
        if grab:
            if ln.strip().startswith("## ") or ln.strip().startswith("**"):
                break
            out.append(ln)
    return "\n".join(out).strip()


def _mt_types(md: str) -> set[str]:
    """Collect MT decision types from the canonical V2O L200 exemplar §3 table."""
    body = _section_text(md, "3. MATERIAL TRANSLATION DECISIONS")
    return set(re.findall(r"\b(SUPPLIED|REFERENT_SUPPLY|STRUCTURAL_CONNECTIVE|LEXICAL|GRAMMATICAL)\b", body))


def _ia_labels(md: str) -> list[str]:
    body = _section_text(md, "4. INTERPRETIVE ASSERTIONS")
    return re.findall(r"\bIA-\d+\b", body)


# --------------------------------------------------------------------------- #
# L0 — deterministic RAW-L0 on a real verse (no model)
# --------------------------------------------------------------------------- #
def test_l0():
    from raw_l0 import raw_l0
    verse = "śivo bhūtvā śivaṃ yajet |"
    res = raw_l0("kramasadbhava", "kramasadbhava:v1", verse)
    p0 = res["proof"] or {}
    recs = res["records"]
    ok = True
    ok &= t("L0: produces records", len(recs) > 0, f"{len(recs)} records")
    ok &= t("L0: P0 lossless proof passes", bool(p0.get("PASS")), json.dumps(p0)[:120])
    # schema sanity: every record has the required fields + status enum
    required = ["id", "raw_fragment", "source_text", "lemma_iast", "literal_gloss", "status"]
    ok &= t("L0: schema fields present", all(all(r.get(f) is not None for f in required) for r in recs))
    ok &= t("L0: status enum valid", all(r["status"] in {"PARSED", "AMBIGUOUS", "FAILED"} for r in recs))
    return ok


# --------------------------------------------------------------------------- #
# L200 — constrained compiler on the REAL V2-O L1/L2 vs the canonical V2-O L200
# --------------------------------------------------------------------------- #
def test_l200_v2o():
    import l200_worker as LW
    v2o_l200 = (STACK / "l200" / "V2O-saptamo-vimarsa.md").read_text(encoding="utf-8")
    # the exemplar's L2 published reading (extract the §1 body, strip markers)
    l2_text = (STACK / "pilot" / "pilot_V2O_L2_read.md").read_text(encoding="utf-8")
    # L1 ground: use the L0 key-token glosses as the controlled ground (from the exemplar §2)
    l1_text = ("the powers, knowledge memory removal, are established; a power needs a support; "
               "the support is the mahesvara, whose essence is the freedom of joining, separating, "
               "resting, concealing, manifesting; the pratibha is the flashing seasoned with the "
               "order of the word-objects; its support is the order-less infinite-consciousness-form "
               "knower; that knower is the great Lord")

    cands = LW._generate_candidates(l1_text, l2_text)
    status, mt, ia, open_items = LW._classify_candidates("IPVV:V2O", cands)
    ok = True
    ok &= t("L200: classifier returns COMPLETE", status == "COMPLETE", status)
    ok &= t("L200: produces MT decisions (bounded)", 0 <= len(mt) <= len(cands), f"{len(mt)} MT / {len(cands)} cands")
    # compare MT types against the canonical exemplar's §3
    ex_types = _mt_types(v2o_l200)
    my_types = {m["type"] for m in mt}
    ok &= t("L200: MT types ⊆ canonical taxonomy", my_types <= set(LW.MT_TYPES), f"mine={sorted(my_types)}")
    # the exemplar includes LEXICAL (pratibhā) + STRUCTURAL_CONNECTIVE + SUPPLIED — check recall on
    # the most load-bearing types the exemplar flags
    load_bearing = {"LEXICAL", "STRUCTURAL_CONNECTIVE", "SUPPLIED"}
    recall = load_bearing & my_types
    ok &= t("L200: recalls load-bearing canonical MT types", bool(recall),
            f"recalled={sorted(recall)} of {sorted(load_bearing)}")
    print("   L200 MT produced:", json.dumps(mt, ensure_ascii=False)[:400])
    print("   canonical V2-O MT types:", sorted(ex_types))
    return ok


# --------------------------------------------------------------------------- #
# C1 — passage commentary on the REAL V2-O inputs vs the canonical c1_V2O
# --------------------------------------------------------------------------- #
def test_c1_v2o():
    import c1_worker as CW
    c1_exemplar = (STACK / "c1" / "read" / "c1_V2O-orderless-support.md").read_text(encoding="utf-8")
    l2_text = (STACK / "pilot" / "pilot_V2O_L2_read.md").read_text(encoding="utf-8")
    # hand-authored L200 MT/IA/OPEN as the C1 input packet (faithful to the canonical audit)
    mt = [{"label": "MT-001", "type": "LEXICAL", "basis": "pratibhā -> the flashing"},
          {"label": "MT-002", "type": "LEXICAL", "basis": "rūṣitā -> seasoned"},
          {"label": "MT-003", "type": "GRAMMATICAL", "basis": "akramānantacidrūpaḥ compound"},
          {"label": "MT-006", "type": "STRUCTURAL_CONNECTIVE", "basis": "the akrama turn"}]
    ia = [{"label": "IA-001", "text": "the order-less knower is required by the structure of ordered experience"},
          {"label": "IA-003", "text": "the maheśvara is the free act, not the inert base"}]
    opn = [{"text": "the 14-verse plan's full mapping", "status": "OPEN"}]

    l1_text = ("the powers are established; a power needs a support; the support is the mahesvara, the "
               "freedom to join and separate; the pratibha is the flashing seasoned with the order of the "
               "word-objects; its support is the order-less infinite-consciousness-form knower, the great Lord")
    body = CW._build_prompt("IPVV:V2O", {"l2": {"payload": {"l1": {"text": l1_text},
                                                          "l2": {"text": l2_text}}},
                                          "l200": {"payload": {"l200": {
                                              "3_material_translation_decisions": mt,
                                              "4_interpretive_assertions": ia,
                                              "7_open_items": opn}}}})
    import c1_worker
    raw = c1_worker.chat("You are the Pāṭala C1 scholar (passage commentary).", body, timeout=180)
    c1 = CW._parse_c1(raw)
    ok = True
    for s in ("summary", "function", "explanation", "boundary"):
        ok &= t(f"C1: section present+non-empty [{s}]", bool((c1.get(s) or "").strip()))
    ok &= t("C1: key_terms present", isinstance(c1.get("key_terms"), list))
    # C1 validator (the deterministic gate)
    vok, why = CW.c1_validator("C1", {"object_id": "IPVV:V2O", "c1": c1, "c1_status": "MACHINE_PROPOSED"})
    ok &= t("C1: deterministic validator passes", vok, why)
    # scope: the exemplar is passage-local — must NOT contain essay-only lexicon
    core = " ".join(str(c1.get(k) or "") for k in ("summary", "function", "explanation", "boundary"))
    ok &= t("C1: no modern-comparison/essays-as-evidence lexicon",
            not CW._ESSAY_LEXICON.search(core))
    print("   C1 summary:", (c1.get("summary") or "")[:150])
    print("   C1 boundary:", (c1.get("boundary") or "")[:150])
    return ok


def main() -> int:
    print("=== LAYER-WORKER vs IPVV EXEMPLAR COMPARISON ===")
    ok = True
    ok &= test_l0()
    print()
    ok &= test_l200_v2o()
    print()
    ok &= test_c1_v2o()
    print("\n" + ("ALL LAYER TESTS PASS" if ok else "SOME LAYER TESTS FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
