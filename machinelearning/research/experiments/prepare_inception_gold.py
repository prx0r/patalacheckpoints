#!/usr/bin/env python3
"""experiments/prepare_inception_gold.py — use INCEpTION for real gold (Atlas-100 #9).

The directive: the bridge exists — use it, don't build more. Prepare a REAL annotation project from
20 IPVV passages with the annotation layers (speaker / proposition span / commitment / premise /
conclusion / objection / reply / warrant), exported via the existing annotation_bridge (W3C-Web-
Annotation, INCEpTION-compatible), so humans can produce natural gold outside Agent-1's loop.

For each passage: the Sanskrit/L2 text + machine-proposed span labels (speaker, commitment) as the
pre-annotation; INCEpTION reviews; import returns ReviewEvents/gold.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))
sys.path.insert(0, os.path.join(ROOT, "source-evidence"))
from annotation_bridge import build_annotation_project  # noqa: E402
IPVV = os.path.join(ROOT, "data/published/ipvv")
OUT = os.path.join(ROOT, "data/evaluation/inception-gold-project.json")

# annotation layers (per the INCEpTION doc + the reviewer's P1)
LAYERS = ("speaker", "proposition", "commitment", "premise", "conclusion", "objection", "reply", "warrant")


def _passages(n=20):
    idx = json.load(open(os.path.join(IPVV, "index.json"), encoding="utf-8"))
    out = []
    for p in idx["passages"]:
        f = os.path.join(IPVV, p["file"])
        if not os.path.exists(f):
            continue
        d = json.load(open(f, encoding="utf-8"))
        text = (d.get("l2_text") or "").strip()
        if len(text) < 200:
            continue
        out.append({"id": p["id"], "chunk": p["locator"], "text": text[:2000]})
        if len(out) >= n:
            break
    return out


def prepare() -> dict:
    passages = _passages(20)
    projects = []
    for p in passages:
        text = p["text"]
        # machine pre-annotation: propose speaker/commitment spans from the passage's C1/l2 (best-effort
        # — the human corrects in INCEpTION). We mark a few candidate spans for review.
        spans = []
        for cue, label in (("Buddhist", "opponent"), ("Abhinavagupta", "author"),
                           ("the Lord", "author"), ("objection", "opponent")):
            i = text.find(cue)
            if i >= 0:
                spans.append({"span_id": f"{p['chunk']}:{label}:{i}", "char_start": i,
                              "char_end": min(i + len(cue), len(text)), "layer": "speaker",
                              "label": label, "label_type": "SPEAKER",
                              "machine_proposed": True, "uncertainty": "NEEDS_REVIEW",
                              "source_ref": p["id"]})
        if not spans:
            # no speaker cue found — propose a proposition-span task on the first sentence
            spans.append({"span_id": f"{p['chunk']}:prop:0", "char_start": 0,
                          "char_end": min(120, len(text)), "layer": "proposition",
                          "label": "proposition", "label_type": "PROPOSITION",
                          "machine_proposed": False, "uncertainty": "NEEDS_REVIEW", "source_ref": p["id"]})
        project = build_annotation_project(text, spans, f"IPVV-GOLD-{p['chunk'][:20]}", layers=LAYERS)
        projects.append({"passage": p["id"], "project": project})
    bundle = {
        "bench": "INCEPTION-GOLD-PREP",
        "passages": len(projects),
        "layers": list(LAYERS),
        "design": "machine pre-annotation -> INCEpTION review -> import as ReviewEvents/gold",
        "projects": projects,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)
    return bundle


if __name__ == "__main__":
    b = prepare()
    print(f"INCEpTION gold project prepared:")
    print(f"  passages: {b['passages']}, layers: {b['layers']}")
    for p in b["projects"][:3]:
        print(f"    {p['passage'][:40]:42} {p['project']['annotation_count']} pre-annotations")
    print(f"  wrote {OUT}")
    print("  next: import into INCEpTION (W3C-Web-Annotation), humans annotate, import as gold.")
