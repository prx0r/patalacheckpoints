#!/usr/bin/env python3
"""python/patala_core/atlas/test_resolver.py — I3 source-resolver tests.

Proves the I3 resolver produces the Agent 1 Atlas NAT candidate shape:
  - multidimensional authority (NOT a single verified=true / lone EDITION_VERIFIED string)
  - per-dimension relation vocabulary
  - honest OPEN/UNSUPPORTED for unresolved dimensions
  - explicit gate predicates (factory/publication/scholar_review), never a scalar rank
Run: python3 python/patala_core/atlas/test_resolver.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from patala_core.atlas.resolver import DIMENSIONS, resolve_work  # noqa: E402


def t(name, cond, detail=""):
    print(("PASS" if cond else "FAIL"), "-", name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def main() -> int:
    ok = True
    print("=== I3: source resolver slice ===")

    cand = resolve_work("matangaparamesvara", net=False)

    ok &= t("candidate type is SOURCE_RESOLUTION_CANDIDATE", cand.get("type") == "SOURCE_RESOLUTION_CANDIDATE")
    ok &= t("authority is per-dimension, not a single scalar", isinstance(cand.get("authority"), dict))
    ok &= t("has all 7 authority dimensions", set(cand["authority"].keys()) == set(DIMENSIONS),
            f"got {sorted(cand['authority'])}")
    ok &= t("no 'verified' scalar in authority", "verified" not in cand["authority"])
    ok &= t("no single authority_state scalar", "authority_state" not in cand)

    # each dimension has a relation from the ladder vocabulary (or honest OPEN/UNSUPPORTED)
    vocab = {"DISCOVERED", "INTERNAL_IDENTITY_BOUND", "EXTERNAL_CANDIDATE_FOUND",
             "CATALOG_MATCHED", "MULTI_SOURCE_MATCHED", "COPY_INSPECTED",
             "EDITION_VERIFIED", "TEXT_DERIVATION_VERIFIED", "SCHOLAR_CONFIRMED", "OPEN", "UNSUPPORTED"}
    bad = [d for d, ev in cand["authority"].items() if ev.get("relation") not in vocab]
    ok &= t("all dimension relations use the authority vocabulary", not bad, f"bad={bad}")

    # open dimensions are explicit
    ok &= t("open_dimensions listed explicitly", isinstance(cand.get("open_dimensions"), list))

    # gates are predicates
    gates = cand.get("gates", {})
    ok &= t("gates are explicit predicates", set(gates) == {"factory_eligible", "publication_eligible", "scholar_review_eligible"},
            f"gates={list(gates)}")
    ok &= t("all gate values are bools", all(isinstance(v, bool) for v in gates.values()))

    # Authority-inflation fix: an internal crosswalk mapping is INTERNAL_IDENTITY_BOUND, NOT
    # MULTI_SOURCE_MATCHED (a crosswalk is not external corroboration). If the DB crosswalk is
    # unreachable the relation stays DISCOVERED (honest). It must NEVER be promoted to
    # MULTI_SOURCE_MATCHED or CATALOG_MATCHED by an internal mapping alone.
    wid_rel = cand["authority"]["WORK_IDENTITY"]["relation"]
    ok &= t("WORK_IDENTITY is NOT inflated to MULTI_SOURCE/CATALOG by an internal mapping",
            wid_rel in ("INTERNAL_IDENTITY_BOUND", "DISCOVERED"), wid_rel)
    ok &= t("publication gate NOT opened by an internal mapping",
            gates["publication_eligible"] is False, f"publication={gates['publication_eligible']}")

    # honesty: etext/witness/date/rights stay OPEN (we don't claim what we can't resolve)
    for dim in ("ETEXT_DERIVATION", "WITNESS_LINKAGE", "DATE_PRECISION", "RIGHTS"):
        rel = cand["authority"][dim]["relation"]
        if rel not in ("OPEN", "DISCOVERED"):
            ok &= t(f"{dim} honest (not inflated)", False, f"relation={rel}")
    ok &= t("unresolved dimensions stay OPEN (no provenance theatre)",
            all(cand["authority"][d]["relation"] in ("OPEN", "DISCOVERED") for d in ("ETEXT_DERIVATION", "WITNESS_LINKAGE", "DATE_PRECISION", "RIGHTS")))

    print("")
    print("RESULT: " + ("ALL PASS" if ok else "FAILURES"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
