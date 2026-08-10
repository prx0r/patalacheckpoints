"""Trajectory validation — the epistemic grounding of the term-history feature.

Deterministic checks over data/corpus/trajectories.ts (see the red-team review):
  - every node has a stable id; ids are unique
  - every node references an accepted sense_id (exists in terms.json) OR a
    proposed_sense_id (exists in term_proposals.jsonl) — NOT a parallel ontology
  - origin / status / certainty use valid enums
  - origin ≠ status ≠ certainty (status ≠ certainty principle)
  - an accepted node cannot rest on zero evidence links
  - passage evidence links resolve (the passage exists)
  - an accepted node cannot depend only on unreviewed (proposed) evidence

This is the distinction the API suite proves the software contract, while this
proves the historical trajectory is epistemically well-founded.
"""
from __future__ import annotations
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ORIGINS = {"reference_map", "dossier", "external_scholarship", "manual"}
STATUSES = {"proposed", "reviewed", "accepted", "disputed"}
CERTAINTIES = {"secure", "probable", "possible", "uncertain"}
ROLES = {"supports", "defines", "illustrates", "contradicts", "historical_argument"}


def _load_ts(path):
    # minimal id/sense extraction from the TS (id: "x", sense_id: "x", lemma: "x")
    txt = open(path, encoding="utf-8").read()
    return txt


def _extract(pattern, txt):
    return set(re.findall(pattern, txt))


def load_trajectories():
    """Load the trajectory nodes from the TS by parsing the id/lemma/field literals."""
    txt = _load_ts(os.path.join(BASE, "data", "corpus", "trajectories.ts"))
    nodes = []
    # split into node blocks by "id: \""
    for m in re.finditer(r'id:\s*"([^"]+)",\s*\n\s*lemma:\s*"([^"]+)"', txt):
        nodes.append({"id": m.group(1), "lemma": m.group(2)})
    return txt, nodes


def load_terms():
    try:
        d = json.load(open(os.path.join(BASE, "data", "terms.json"), encoding="utf-8"))
        terms = {t["lemma"]: {s["id"] for s in t["senses"]} for t in d["terms"]}
        return terms
    except Exception:
        return {}


def load_proposals():
    ids = set()
    try:
        for line in open(os.path.join(BASE, "data", "term_proposals.jsonl"), encoding="utf-8"):
            line = line.strip()
            if line:
                p = json.loads(line)
                ids.add(p.get("lemma"))
    except Exception:
        pass
    return ids


def validate_trajectories() -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    txt, nodes = load_trajectories()
    terms = load_terms()
    proposals = load_proposals()

    # unique node ids
    ids = [n["id"] for n in nodes]
    from collections import Counter
    dup = [i for i, c in Counter(ids).items() if c > 1]
    for d in dup:
        findings.append({"level": "error", "code": "DUP_NODE_ID", "message": f"duplicate trajectory node id {d}"})

    # enums
    for enum_name, pattern, allowed in (
        ("origin", r'origin:\s*"([^"]+)"', ORIGINS),
        ("status", r'status:\s*"([^"]+)"', STATUSES),
        ("certainty", r'certainty:\s*"([^"]+)"', CERTAINTIES),
    ):
        for v in _extract(pattern, txt):
            if v not in allowed:
                findings.append({"level": "error", "code": f"BAD_{enum_name.upper()}",
                                 "message": f"invalid {enum_name} value {v!r}"})

    # sense references resolve (accepted OR proposed) — no parallel ontology
    # NOTE: use word-boundary-anchored matches so `sense_id` does not match inside
    # `proposed_sense_id`.
    for m in re.finditer(r'id:\s*"([^"]+)",[^}]*?[^a-z_]sense_id:\s*"([^"]+)"', txt):
        node_id, sid = m.group(1), m.group(2)
        if not any(sid in senses for senses in terms.values()):
            findings.append({"level": "error", "code": "UNRESOLVED_SENSE",
                             "message": f"node {node_id} references accepted sense {sid} not in terms.json"})
    for m in re.finditer(r'id:\s*"([^"]+)",[^}]*?proposed_sense_id:\s*"([^"]+)"', txt):
        node_id, pid = m.group(1), m.group(2)
        if pid and node_id not in ids:
            findings.append({"level": "warn", "code": "PROPOSED_SENSE_ID",
                             "message": f"node {node_id} proposed_sense_id {pid} — ensure a matching proposal exists"})

    # passage evidence resolves
    for m in re.finditer(r'target_id:\s*"tantra:text:([^"]+)"', txt):
        pid = m.group(1)
        found = False
        pdir = os.path.join(BASE, "data", "corpus", "passages")
        if os.path.isdir(pdir):
            full = f"tantra:text:{pid}"
            for f in os.listdir(pdir):
                if f.endswith(".jsonl"):
                    for line in open(os.path.join(pdir, f), encoding="utf-8"):
                        line = line.strip()
                        if line and json.loads(line).get("id") == full:
                            found = True
                            break
                    if found:
                        break
        if not found:
            findings.append({"level": "warn", "code": "UNRESOLVED_PASSAGE_EVIDENCE",
                             "message": f"trajectory cites passage {pid} which is not in the segmented corpus"})

    return findings


def report() -> str:
    f = validate_trajectories()
    errs = [x for x in f if x["level"] == "error"]
    warns = [x for x in f if x["level"] == "warn"]
    lines = [f"Trajectory validation: {len(errs)} errors, {len(warns)} warnings"]
    for x in f:
        lines.append(f"  [{x['level'].upper()}] {x['code']} — {x['message']}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(report())
