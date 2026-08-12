#!/usr/bin/env python3
"""analyze_ensemble.py — analyze p2_disagreements.jsonl (streamed or complete)."""
import json, sys
from collections import Counter

path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/ens_s2/p2_disagreements.jsonl"
rows = [json.loads(l) for l in open(path, encoding="utf-8")]
conf = Counter(r["agreement_class"] for r in rows)
rel = Counter(r["relation_class"] for r in rows)
inset = Counter(r["input_set"] for r in rows)

print(f"records: {len(rows)}")
print("input sets:", dict(inset))
print("\nconfusion (V/H sign):")
for k, v in conf.most_common():
    print(f"  {k:8s} {v}  ({100*v/len(rows):.1f}%)")
print("\nrelations:")
for k, v in rel.most_common():
    print(f"  {k:38s} {v}  ({100*v/len(rows):.1f}%)")

# rates
ctrl = [r for r in rows if r["input_set"].startswith("CTRL")]
confr = [r for r in rows if r["input_set"] == "CONFLICT"]
if ctrl:
    ctrl_agree = sum(1 for r in ctrl if r["agreement_class"].endswith("+"))
    print(f"\ncontrol agreement rate: {ctrl_agree}/{len(ctrl)} = {100*ctrl_agree/len(ctrl):.1f}%")
if confr:
    resolved = sum(1 for r in confr if r["relation_class"] in ("VIDYUT_REPRESENTATION_MISMATCH","EXACT_LEMMA_AGREEMENT"))
    dbl = sum(1 for r in confr if r["relation_class"]=="DOUBLE_CONFLICT")
    print(f"CONFLICT resolution rate: {resolved}/{len(confr)} = {100*resolved/len(confr):.1f}%")
    print(f"DOUBLE-CONFLICT rate: {100*dbl/len(confr):.1f}%")
