#!/usr/bin/env python3
"""test_annotation_bridge.py — the annotation bridge (devpath13 / reviewer priority #4).

Checks:
  1. export produces a W3C-Web-Annotation-compatible project with resilient selectors
  2. imported annotations become ReviewEvents (immutable, don't mutate source)
  3. a CORRECT becomes a gold-proposal (PENDING adjudication), never a source mutation
  4. a REJECT lists the span as rejected
  5. the round-trip: text hash + quote selectors let imports re-resolve the exact span
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from annotation_bridge import (
    build_annotation_project, import_annotations, build_vertical1_annotation_project,
    SPEAKER_LABELS, COMMITMENT_LABELS, SUPPORT_LABELS,
)

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


proj = build_vertical1_annotation_project()

print("== 1. export is W3C-Web-Annotation-compatible ==")
check("project has text + text_hash", proj["text"] and proj["text_hash"])
check("annotations carry oa:TextQuoteSelector + pt:HashSelector",
      all(any(s.get("@type") == "oa:TextQuoteSelector" for s in a["target"]["selectors"])
          and any(s.get("@type") == "pt:HashSelector" for s in a["target"]["selectors"])
          for a in proj["annotations"]))
check("labels come from Pāṭala vocabularies",
      all(a["body"]["label"] in SPEAKER_LABELS for a in proj["annotations"]))
check("layers include the gold layers",
      set(("speaker", "commitment", "proposition", "support", "scope", "uncertainty")).issubset(set(proj["layers"])))

print("\n== 2. import -> ReviewEvents (no source mutation) ==")
scholar = [
    {"span_id": "S-ADHY", "layer": "speaker", "label": "opponent", "label_type": "SPEAKER",
     "decision": "ACCEPT", "annotator": "scholar-A"},
    {"span_id": "S-ESTAB", "layer": "speaker", "label": "author", "label_type": "SPEAKER",
     "decision": "CORRECT", "note": "Abhinavagupta's own claim", "annotator": "scholar-A"},
    {"span_id": "S-ADHY", "layer": "speaker", "label": "opponent", "label_type": "SPEAKER",
     "decision": "REJECT", "annotator": "scholar-B"},
]
imp = import_annotations(proj, scholar)
check("each annotation -> a ReviewEvent", len(imp["review_events"]) == len(scholar))
check("ReviewEvents are pt:ReviewEvent", all(e["@type"] == "pt:ReviewEvent" for e in imp["review_events"]))
check("CORRECT -> a gold proposal (PENDING, not applied)", len(imp["gold_proposals"]) == 1
      and imp["gold_proposals"][0]["adjudication"] == "PENDING")
check("REJECT lists the span", "S-ADHY" in imp["rejected_span_ids"])
check("source untouched (no mutation field)", all("mutate" not in e for e in imp["review_events"]))

print("\n== 3. round-trip span resolution ==")
# a quote selector must exactly match the source text at those offsets
a0 = proj["annotations"][0]
quote = a0["target"]["selectors"][0]["exact"]
start, end = a0["target"]["selectors"][0]["start"], a0["target"]["selectors"][0]["end"]
check("quote selector re-resolves to the exact source span",
      proj["text"][start:end] == quote)

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (annotation bridge works)"))
sys.exit(1 if failures else 0)
