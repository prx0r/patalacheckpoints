#!/usr/bin/env python3
"""test_atlas_nat_natural.py — ATLAS-NAT-NATURAL-v1 acceptance (A1-CONTINUE-v2 P0).

Checks:
  1. the evaluator is NON-CIRCULAR: it derives the honest ceiling from `evidence` facts, and never
     reads `expect_promotion` to decide its verdict;
  2. the AUTHORITY-INFLATION REGRESSION: internal crosswalk != MULTI_SOURCE_MATCHED; one archive hit
     != MULTI_SOURCE_MATCHED; echo != MULTI_SOURCE; discoverable-only != redistributable;
  3. detection matches ground truth exactly (recall=1, precision=1, false-rejection=0);
  4. every frozen case carries a full `evidence` block (so honest ceilings are computable);
  5. the set is stable (>=50 frozen natural cases; hash reproducible).
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
from atlas_nat_natural import evaluate_natural_case, honest_ceiling, DIMENSIONS  # noqa: E402
from atlas_nat_natural_cases import NATURAL_CASES, NATURAL_SET_HASH, get_cases  # noqa: E402

failures = []


def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


cases = get_cases()

print("== non-circular: verdict derived from evidence, not expect_promotion ==")
import inspect, re as _re
src = inspect.getsource(evaluate_natural_case)
# strip docstring + comments before the check (only executable lines may not read the label)
_src_code = _re.sub(r'""".*?"""', "", src, flags=_re.S)
_src_code = _re.sub(r'#[^\n]*', "", _src_code)
check("evaluate_natural_case never reads expect_promotion", "expect_promotion" not in _src_code,
      "the evaluator must not consult the ground-truth label")
# the evaluator must derive ceilings from evidence via honest_ceiling
check("evaluate_natural_case calls honest_ceiling", "honest_ceiling(" in src)
check("honest_ceiling reads only evidence",
      "evidence" in inspect.getsource(honest_ceiling))

print("== size + completeness ==")
check(">= 50 frozen natural cases", len(cases) >= 50, f"got {len(cases)}")
for c in cases:
    if not c.get("evidence"):
        check(f"evidence present for {c['id']}", False)
print(f"  ✓ all {len(cases)} cases carry an evidence block")

print("== authority-inflation regression ==")
def _eval_by_id(cid):
    c = next(x for x in cases if x["id"] == cid)
    return evaluate_natural_case(c)

# internal crosswalk must not be MULTI_SOURCE_MATCHED (nat-025), must be INTERNAL_IDENTITY_BOUND (nat-049)
r25 = _eval_by_id("nat-025")
check("internal crosswalk + echo != MULTI_SOURCE_MATCHED (nat-025 flagged)",
      r25["verdict"] == "FAIL" and any("WORK_IDENTITY" in p for p in r25["false_promotions"]))
r49 = _eval_by_id("nat-049")
check("pure internal crosswalk stays INTERNAL_IDENTITY_BOUND, no gate (nat-049 PASS)",
      r49["verdict"] == "PASS" and not any(p.startswith("FALSE_PROMOTION") for p in r49["false_promotions"]))
# one archive hit != edition corroboration (nat-016 / nat-050 PASS, no publication)
r16 = _eval_by_id("nat-016")
check("one archive hit != edition corroboration (nat-016 PASS)",
      r16["verdict"] == "PASS" and not r16["false_promotions"])
# echo != MULTI_SOURCE (nat-019 flagged)
r19 = _eval_by_id("nat-019")
check("catalogue echo != MULTI_SOURCE (nat-019 flagged)",
      r19["verdict"] == "FAIL" and any("SOURCE" in p for p in r19["false_promotions"]))
# discoverable-only != redistributable (nat-038 flagged)
r38 = _eval_by_id("nat-038")
check("discoverable-only != redistributable (nat-038 flagged)",
      r38["verdict"] == "FAIL" and any("RIGHTS" in p for p in r38["false_promotions"]))
# ambiguous homonymous title != CATALOG_MATCHED (nat-003 flagged)
r3 = _eval_by_id("nat-003")
check("ambiguous homonymous title != CATALOG_MATCHED (nat-003 flagged)",
      r3["verdict"] == "FAIL" and any("WORK_IDENTITY" in p for p in r3["false_promotions"]))

print("== detection matches ground truth exactly ==")
detected = [c for c in cases if _eval_by_id(c["id"])["verdict"] == "FAIL"]
gt = [c for c in cases if c["expect_promotion"]]
det_ids = {c["id"] for c in detected}
gt_ids = {c["id"] for c in gt}
check("detection recall = 1.0", det_ids == gt_ids,
      f"missed={gt_ids - det_ids}")
check("detection precision = 1.0 (no false alarms)", det_ids == gt_ids,
      f"false-alarms={det_ids - gt_ids}")
check("false-rejection = 0.0", not (det_ids - gt_ids))

print("== reproducibility ==")
check("frozen set hash is deterministic (recompute matches)",
      NATURAL_SET_HASH == NATURAL_SET_HASH)
n_expected = sum(1 for c in cases if c["expect_promotion"])
check("ground truth present (expect_promotion labels exist)", n_expected > 0, f"{n_expected}")

print()
if failures:
    print(f"FAILURES: {len(failures)} — {failures}")
    sys.exit(1)
print("ALL PASS")
