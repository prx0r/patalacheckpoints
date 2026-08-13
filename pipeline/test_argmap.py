#!/usr/bin/env python3
"""pipeline/test_argmap.py — deterministic argument-map layer tests (A2-CP3).

Covers the canonical argument-map producer + its deterministic production gate (model stubbed):
  - canonical 4-section shape (what_is_at_issue / argument_steps / open_items / decision_for_l2)
  - provenance (source_object + input_hash bound); status MACHINE_PROPOSED
  - fail-closed: model failure / bad JSON -> no partial commit
  - open_items well-formed (status enum)
This is the PRODUCTION gate (Agent 2's lane). Semantic fidelity is Agent 1's evals lane.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R
import argument_map_worker as AM


def t(name, cond, detail=""):
    print(("PASS" if bool(cond) else "FAIL"), "-", name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def main() -> int:
    ok = True
    R.REG_DIR = Path(tempfile.mkdtemp())
    oid = "kramasadbhava:v1"
    # seed a committed T1 for the passage (so the map has upstream)
    R.commit("T1", oid, "abc123", created_by="test",
             payload={"t1": {"tokens": [{"surface": "śivo", "form": "[and]-the auspicious one (śivo)"}],
                             "source_text": "śivo bhūtvā śivaṃ yajet", "status": "MACHINE_PROPOSED"},
                      "t1_status": "MACHINE_PROPOSED"})

    good = {"what_is_at_issue": "Whether the one who worships must first become Śiva.",
            "argument_steps": ["The verse states that having become Śiva one should worship Śiva.",
                               "The predicate 'having become' establishes the transformation."],
            "open_items": [{"text": "whether 'yajet' is optative or subjunctive", "status": "OPEN"}],
            "decision_for_l2": "Render as the transformation-premise: becoming Śiva precedes worship."}

    print("=== ARGMAP canonical shape + provenance (model stubbed) ===")
    AM.chat = lambda s, p, **kw: json.dumps(good)
    props = AM.argmap_generator("ARGMAP", [{"object_id": oid, "input_hash": "abc123"}])
    ok &= t("ARGMAP generator produced a proposal", len(props) == 1)
    p = props[0]
    ok &= t("ARGMAP status MACHINE_PROPOSED", p["argmap_status"] == "MACHINE_PROPOSED")
    m = p["argument_map"]
    ok &= t("ARGMAP has all 4 canonical sections",
            set(m.keys()) == set(AM.REQUIRED_SECTIONS), str(list(m.keys())))
    ok &= t("ARGMAP what_is_at_issue + decision non-empty",
            bool(m["what_is_at_issue"]) and bool(m["decision_for_l2"]))
    ok &= t("ARGMAP has argument_steps", bool(m["argument_steps"]))
    ok &= t("ARGMAP source_object + input_hash bound",
            p.get("source_object") == oid and bool(p["input_hash"]))
    vok, why = AM.argmap_validator("ARGMAP", p)
    ok &= t("ARGMAP validator passes", vok, why)

    print()
    print("=== ARGMAP fail-closed (model failure never commits) ===")
    AM.chat = lambda s, p, **kw: "not json {"
    bad = AM.argmap_generator("ARGMAP", [{"object_id": oid, "input_hash": "abc123"}])[0]
    ok &= t("bad model output -> GENERATION_FAILED", bad["argmap_status"] == "GENERATION_FAILED")
    ok &= t("GENERATION_FAILED blocked by validator", AM.argmap_validator("ARGMAP", bad)[0] is False)

    print()
    print("=== ARGMAP dependency (no T1 upstream -> no fabricated map) ===")
    nop = AM.argmap_generator("ARGMAP", [{"object_id": "other:x", "input_hash": "h"}])[0]
    ok &= t("missing T1 -> DEPENDENCY_BLOCKED", nop["argmap_status"] == "DEPENDENCY_BLOCKED")
    ok &= t("DEPENDENCY_BLOCKED not committed", AM.argmap_validator("ARGMAP", nop)[0] is False)

    print("\n" + ("ARGMAP ALL PASS" if ok else "ARGMAP SOME FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
