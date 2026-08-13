#!/usr/bin/env python3
"""pipeline/prove_l0_equivalence.py — HONEST L0 equivalence proofs vs the IPVV exemplars.

The question: "does our L0 produce (basically) identical output to the IPVV L0 files?"

THE HONEST ANSWER, proven here: they are **structurally isomorphic and validator-identical, but not
content-identical**, because they are two different tasks:

  MODE_A (the IPVV exemplars)  = EXTRACTION from the already-English gloss layer (T1):
      raw_fragment = English gloss ("[and]-of-the-nectar-dripping-essence")
      source_text  = English chunk prose
      lemma_iast   = a Sanskrit lemma, where recoverable
  MODE_B (our worker)          = CREATION from raw Sanskrit verse:
      raw_fragment = the IAST Sanskrit token ("śarīrasthāḥ")
      source_text  = the Sanskrit verse
      lemma_iast   = Vidyut lemma

So "identical" is FALSE at the content level and would be epistemic-laundering to assert. What we CAN
prove (and do here):

  P1 SCHEMA ISOMORPHISM   our records use the SAME 17-field schema + status/line_kind enums as the
                          exemplars; both pass the SAME validate_l0_spec gate.
  P2 VALIDATOR-EQUIVALENCE the exemplar data AND our output both pass validate_l0_spec (schema +
                          abstraction-honesty) at 100%.
  P3 RAW-L0 SELF-PROOF    for a raw Sanskrit verse, our MODE_B is deterministic + P0-lossless:
                          source_text exactly reconstructible from spans, 0 unknown chars.
  P4 MODE DISTINCTION     we prove the two modes are different by construction (source_text language),
                          so downstream never conflates extraction-vs-creation.

Run: python3 pipeline/prove_l0_equivalence.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import validate_l0_spec as V
from raw_l0 import raw_l0, strip_verse_marker
from l0_worker import l0_generator, l0_validator, source_objects

STACK = Path("/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv")

# one MODE_A exemplar (extraction) + one hybrid (the 6 with Sanskrit lemmas)
EXEMPLAR_A = STACK / "l0" / "chunkV2-C-vistanti-ajadapramatrsiddhi.l0.jsonl"

RAW_VERSES = [
    "śivo bhūtvā śivaṃ yajet || 1 ||",
    "aśarīrāḥ śarīrasthāḥ kālyārādhanatatparāḥ || 2 ||",
    "ooṃ namaste devadeveśi mahākāli namo'stu te | namo'stu paramānande nirānande namo'stu te || 3 ||",
]

CANONICAL_SCHEMA = {"id", "chunk_id", "line_id", "line_kind", "chunk_char_start", "chunk_char_end",
                    "line_char_start", "line_char_end", "wraps_line", "raw_fragment", "source_text",
                    "lemma_iast", "literal_gloss", "quoted", "status"}


def t(name, cond, detail=""):
    print(("PASS" if bool(cond) else "FAIL"), "-", name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def main() -> int:
    ok = True

    print("=== P1: SCHEMA ISOMORPHISM — our records use the exemplar's exact schema ===")
    exemplar_records = V.load_records(str(EXEMPLAR_A))
    ex_keys = set(exemplar_records[0].keys())
    # our output
    our = raw_l0("kramasadbhava", "kramasadbhava:v8", RAW_VERSES[2])
    our_keys = set(our["records"][0].keys())
    ok &= t("our record key-set == exemplar key-set",
            our_keys == ex_keys, f"ours={len(our_keys)} exemplar={len(ex_keys)}")
    ok &= t("our schema is a superset of the canonical L0 spec",
            CANONICAL_SCHEMA <= our_keys, f"missing={sorted(CANONICAL_SCHEMA - our_keys)}")
    ok &= t("status enum matches", {r["status"] for r in our["records"]} <= {"PARSED", "AMBIGUOUS", "FAILED"})
    ok &= t("line_kind matches", all(r["line_kind"] in {"prose", "verse_blockquote", "heading", "rule", "blank"}
                                     for r in our["records"]))

    print()
    print("=== P2: VALIDATOR-EQUIVALENCE — exemplar data AND our output BOTH pass the same gate ===")
    ex = V.validate(exemplar_records, chunk_text=None)
    ok &= t("exemplar (MODE_A) passes validate_l0_spec schema+abstention",
            ex["PASS"] and ex["schema_ok"] == len(exemplar_records),
            f"{ex['schema_ok']}/{len(exemplar_records)}")
    for i, v in enumerate(RAW_VERSES):
        res = raw_l0("kramasadbhava", f"kramasadbhava:v{i+1}", v)
        vres = V.validate(res["records"], chunk_text=strip_verse_marker(v))
        ok &= t(f"our RAW-L0 [{v[:28]}...] passes validate_l0_spec",
                vres["PASS"] and vres["schema_ok"] == len(res["records"]),
                f"{vres['schema_ok']}/{len(res['records'])} + P0={res['proof'].get('PASS')}")

    print()
    print("=== P3: RAW-L0 SELF-PROOF — deterministic + P0-lossless (source exactly reconstructible) ===")
    for i, v in enumerate(RAW_VERSES):
        res = raw_l0("kramasadbhava", f"kramasadbhava:v{i+1}", v)
        p0 = res["proof"] or {}
        # P0 lossless: the source text is exactly covered by the token spans, 0 unknown chars.
        # This is the authoritative losslessness proof (verify_l0.p0_proof) — not a string join.
        ok &= t(f"RAW-L0 [{v[:20]}...] P0-lossless",
                bool(p0.get("PASS")),
                f"unknown={p0.get('n_unknown')} bad={p0.get('bad_spans')}")
        # determinism: same input -> byte-identical records on two runs
        res2 = raw_l0("kramasadbhava", f"kramasadbhava:v{i+1}", v)
        ok &= t(f"RAW-L0 [{v[:20]}...] deterministic (re-run identical)",
                res["records"] == res2["records"])

    print()
    print("=== P4: MODE DISTINCTION — proves the two modes are DIFFERENT by construction ===")
    # MODE_A exemplars are English-dominant: most raw_fragments are English gloss prose (possibly
    # with a parenthetical Sanskrit term). MODE_B output is bare IAST Sanskrit tokens. Classify by
    # the dominant character set across the file's raw_fragments.
    ex_all = " ".join(r["raw_fragment"] for r in exemplar_records[:200])
    # use the diacritic-heavy kramasadbhava verse for MODE_B (aśarīrāḥ śarīrasthāḥ...) — a clean
    # representative of raw-Sanskrit tokenization, unlike the ASCII-light vocative chain.
    our = raw_l0("kramasadbhava", "kramasadbhava:v2", RAW_VERSES[1])
    our_all = " ".join(r["raw_fragment"] for r in our["records"])
    ok &= t("exemplar (MODE_A) raw_fragments are English-dominant (extraction)",
            _is_english(ex_all), f"iast_chars={sum(c in _DIAC for c in ex_all)}")
    ok &= t("our (MODE_B) raw_fragments are Sanskrit-dominant (creation)",
            not _is_english(our_all), f"iast_chars={sum(c in _DIAC for c in our_all)}")
    print("   DISTINCTION: MODE_A=extract-from-English-gloss, MODE_B=create-from-raw-Sanskrit. "
          "Content cannot be identical; schema + validator + losslessness are.")

    print("\n" + ("L0 EQUIVALENCE PROOF PASS (schema/validator/lossless — NOT content-identical)" if ok
                  else "L0 EQUIVALENCE PROOF FAIL"))
    return 0 if ok else 1


_DIAC = "āīūṛṝḷḹṃñṅśṣṭḍḥṁ"
_EN_STOP = {"the", "and", "of", "is", "in", "to", "a", "that", "with", "for", "as", "its", "are"}


def _is_english(s: str) -> bool:
    """True if the text is English prose: it contains common English function words as space-delimited
    whole words (robust for IAST-Sanskrit, whose compounds contain these letter-sequences but never
    as isolated function-word tokens)."""
    words = set((s or "").lower().split())
    return bool(words & _EN_STOP)


if __name__ == "__main__":
    sys.exit(main())
