#!/usr/bin/env python3
"""pipeline/test_argmap_ipvv.py — verify the ARGUMENT MAP against the REAL IPVV exemplar.

The user asked: test on IPVV so we can verify against the previous existing files. This runs my
argument-map producer on the V2-O kārikā 1 verse and checks the produced map against the hand-authored
`pilot_V2O_ARGUMENT_MAP.md` exemplar (the gold).

The gold's core content (what a correct map of V2-O must address):
  - the QUESTION / what is at issue (the support of the powers, āśraya)
  - the maheśvara (the great Lord) as the free support
  - the pratibhā (the flashing) with its order-less knower
  - the freedom / anvaya-vyatireka argument

Check: the produced map's what_is_at_issue + argument_steps must address the same load-bearing claims
the gold addresses. This is a QUALITATIVE structural check (Agent 1 owns exact semantic adjudication).

Run: python3 pipeline/test_argmap_ipvv.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R
import argument_map_worker as AM

KARIKA1 = ("yā caiṣā pratibhā tattatpadārthakramarūṣitā "
           "akramānantacidrūpaḥ pramātā sa maheśvaraḥ")

# load-bearing claims the gold argument map (V2-O) addresses
GOLD_CLAIMS = ["support", "āśraya", "maheśvara", "pratibhā", "flashing", "order-less", "freedom", "powers"]
GOLD_TEXT = open("/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/pilot/pilot_V2O_ARGUMENT_MAP.md").read()


def t(name, cond, detail=""):
    print(("PASS" if bool(cond) else "FAIL"), "-", name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def main() -> int:
    ok = True
    oid = "ipvv:V2O:k1"
    print("=== ARGUMENT MAP vs the REAL IPVV exemplar (pilot_V2O_ARGUMENT_MAP.md) ===")

    # seed a committed T1 so the map has upstream (deterministic)
    R.commit("T1", oid, "hash1", created_by="test",
             payload={"t1": {"tokens": [{"sanskrit": t, "iast": t, "gloss": "x", "status": "GLOSSED",
                                          "form": f"[and]-x ({t})"} for t in
                                          ["yā", "caiṣā", "pratibhā", "tattatpadārthakramarūṣitā",
                                           "akramānantacidrūpaḥ", "pramātā", "sa", "maheśvaraḥ"]],
                             "source_text": KARIKA1, "status": "MACHINE_PROPOSED"},
                      "t1_status": "MACHINE_PROPOSED"})

    # run the producer (real model — the map's content is generated)
    props = AM.argmap_generator("ARGMAP", [{"object_id": oid, "input_hash": "hash1"}])
    p = props[0]
    ok &= t("ARGMAP production gate", p["argmap_status"] == "MACHINE_PROPOSED", p["argmap_status"])
    if p["argmap_status"] != "MACHINE_PROPOSED":
        print("\n" + ("ARGMAP-IPVV FAIL" if not ok else "PASS"))
        return 0 if ok else 1

    m = p["argument_map"]
    text = " ".join([m.get("what_is_at_issue", ""), m.get("decision_for_l2", ""),
                     " ".join(m.get("argument_steps", []))]).lower()
    ok &= t("ARGMAP validator passes", AM.argmap_validator("ARGMAP", p)[0])

    # coverage of the gold's load-bearing claims
    covered = [c for c in GOLD_CLAIMS if c.lower() in text]
    missing = [c for c in GOLD_CLAIMS if c.lower() not in text]
    ok &= t("ARGMAP addresses the gold's load-bearing claims", len(covered) >= 5,
            f"covered={covered} missing={missing}")

    print("\n  gold claims addressed:", covered)
    print("  what_is_at_issue:", m.get("what_is_at_issue", "")[:120])
    print("  decision_for_l2:", m.get("decision_for_l2", "")[:120])

    print("\n" + ("ARGMAP-IPVV PASS" if ok else "ARGMAP-IPVV SOME FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
