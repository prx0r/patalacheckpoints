#!/usr/bin/env python3
"""benchmark_contrast_sets.py — the contrast-set / falsification benchmark around the argument golds.

Instead of asking "is ARG-XXX correct?" (which needs a human), create NEARBY CORRUPTED versions of the
proposed argument and ask whether an evaluator reliably ranks the ORIGINAL above the corruption:

    P(original ranked above corruption)

The corruption types are philosophically important distinctions a serious system must be sensitive to:

    SWAP_SPEAKER            attribute a siddhānta proposition to the objector (pūrvapakṣa) or vice versa
    REVERSE_SUPPORT         turn a support edge into an attack (or the conclusion into a premise)
    NEGATE_PROPOSITION      flip the polarity of a proposition
    WIDEN_SCOPE             extend a local (V2-L) claim to a systematic/universal one
    NARROW_SCOPE            restrict a claim more than the text warrants
    DELETE_PREMISE          drop a necessary premise so the inference no longer follows
    REPLACE_TERM_SENSE      substitute a technical-term sense (e.g. vikalpa -> conceptual construction)
    PURVAPAKSA_AS_SIDDHANTA turn the pūrvapakṣa objection into the author's own commitment

This does NOT prove the original is correct. It tests whether the evaluator is sensitive to distinctions
that matter — an empirical capability claim needing no full semantic gold.

Each corruption is a small, explainable edit to the proposed argument JSON. The "evaluator" is a
comparator over structured properties (speaker, polarity, inference integrity, scope) that a model
judges against the original. The run reports a per-type sensitivity. Label: MULTI_MODEL / MACHINE
evidence — NOT validation.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PACKET = os.path.join(ROOT, "benchmarks/v0/review/ARG-GOLD-REVIEW-PACKET-v2.json")
RUNS_DIR = os.path.join(ROOT, "benchmarks/v0/runs")

DETECTOR_ID = "PATALA.ARGUMENT.CONTRAST_SET.v1"
VERIFIER_VERSION = "contrast-v0"


def git(args):
    return subprocess.run(["git", *args], capture_output=True, text=True, cwd=ROOT).stdout.strip()


# ── load the proposed argument from the packet ────────────────────────────────
def load_argument(gold_id: str) -> dict:
    with open(PACKET, encoding="utf-8") as f:
        packet = json.load(f)
    return next(a for a in packet["arguments"] if a["gold_id"] == gold_id)


def find_prop(arg, pid):
    return next(p for p in arg["propositions"] if p["proposition_id"] == pid)


# ── corruption generators (each edits exactly one dimension) ─────────────────
def corrupt(arg: dict, kind: str) -> dict:
    c = copy.deepcopy(arg)
    props = c["propositions"]

    if kind == "SWAP_SPEAKER":
        # find a siddhānta claim and attribute it to the objector
        p = next(p for p in props if p.get("speaker") == "siddhānta")
        p["speaker"] = "pūrvapakṣa (objector)"
    elif kind == "REVERSE_SUPPORT":
        # swap the conclusion into a premise and the premise into the conclusion
        conc = next(p for p in props if p.get("kind") == "CONCLUSION")
        prem = next(p for p in props if p.get("kind") == "TEXTUAL_CLAIM")
        conc["kind"], prem["kind"] = "TEXTUAL_CLAIM", "CONCLUSION"
    elif kind == "NEGATE_PROPOSITION":
        p = find_prop(c, "G2-TC2") if any(x["proposition_id"] == "G2-TC2" for x in props) else props[1]
        p["text"] = p["text"].replace("is not", "IS").replace("does not", "does")
        # force the negation marker
        p["text"] = "NOT(" + p["text"] + ")"
    elif kind == "WIDEN_SCOPE":
        for p in props:
            if p.get("proposition_id") == "G2-CONC":
                p["text"] = p["text"].replace("does not show", "shows that")
                p["scope"] = "SYSTEMATIC"  # a fabricated universal claim
    elif kind == "NARROW_SCOPE":
        for p in props:
            if p.get("proposition_id") == "G2-CONC":
                p["text"] = "Only in this single verse, " + p["text"]
    elif kind == "DELETE_PREMISE":
        # drop G2-TC1 (a premise of the inference) so the conclusion is unsupported
        c["propositions"] = [p for p in props if p.get("proposition_id") != "G2-TC1"]
    elif kind == "REPLACE_TERM_SENSE":
        for p in props:
            if p.get("proposition_id") == "G2-TC1":
                p["text"] = "vikalpa is EXACTLY the same as conceptual construction (identity, not distinction)"
    elif kind == "PURVAPAKSA_AS_SIDDHANTA":
        obj = next(p for p in props if p.get("kind") == "OBJECTION")
        obj["speaker"] = "siddhānta (author's own commitment)"  # the pūrvapakṣa leaks into author
    return c


# ── evaluator: rank original vs corruption on structured dimensions ──────────
def score_prop(p: dict) -> dict:
    """A structured signature of a proposition the comparator keys on (no prose parsing)."""
    return {
        "id": p.get("proposition_id"),
        "kind": p.get("kind"),
        "speaker": p.get("speaker"),
        "negated": p.get("text", "").startswith("NOT("),
        "scope": p.get("scope", ""),
        "prop_ids": set(x.get("proposition_id") for x in p.get("primary_evidence", [])),
    }


def signal_original_vs_corrupt(original: dict, corrupted: dict) -> dict:
    """Determine whether the corruption is DETECTABLE as a change on structured dimensions."""
    o = {score_prop(p)["id"]: score_prop(p) for p in original["propositions"]}
    c = {score_prop(p)["id"]: score_prop(p) for p in corrupted["propositions"]}
    flags = []
    for pid in o:
        if pid not in c:
            flags.append(f"proposition {pid} deleted")
            continue
        op, cp = o[pid], c[pid]
        if op["speaker"] != cp["speaker"]:
            flags.append(f"{pid}: speaker {op['speaker']} -> {cp['speaker']}")
        if op["kind"] != cp["kind"]:
            flags.append(f"{pid}: kind {op['kind']} -> {cp['kind']}")
        if op["negated"] != cp["negated"]:
            flags.append(f"{pid}: polarity changed")
        if op["scope"] != cp["scope"]:
            flags.append(f"{pid}: scope {op['scope']} -> {cp['scope']}")
        if op["prop_ids"] != cp["prop_ids"]:
            flags.append(f"{pid}: grounding refs changed")
    # inference integrity: every inference's premises must exist
    for inf in corrupted.get("inferences", []):
        for pid in inf.get("premise_ids", []) + inf.get("conclusion_ids", []):
            if pid not in c:
                flags.append(f"inference {inf.get('inference_id')} references missing {pid}")
    return {"detected": len(flags) > 0, "flags": flags[:6]}


def main() -> int:
    kinds = ["SWAP_SPEAKER", "REVERSE_SUPPORT", "NEGATE_PROPOSITION", "WIDEN_SCOPE",
             "NARROW_SCOPE", "DELETE_PREMISE", "REPLACE_TERM_SENSE", "PURVAPAKSA_AS_SIDDHANTA"]
    arg = load_argument("ARG-GOLD-002")

    rows = []
    for kind in kinds:
        corr = corrupt(arg, kind)
        sig = signal_original_vs_corrupt(arg, corr)
        rows.append({"corruption": kind, "detected": sig["detected"], "flags": sig["flags"]})

    detected = sum(1 for r in rows if r["detected"])
    # NOTE (interpretation): this comparator keys on STRUCTURED fields (speaker/kind/polarity/scope/
    # inference-integrity). So it is the DETERMINISTIC FLOOR, not a semantic measure. The corruptions it
    # MISSES (here NARROW_SCOPE and REPLACE_TERM_SENSE) are precisely the SEMANTIC ones — they change
    # meaning but not any structured field. That gap is the empirical argument for a separate
    # semantic-discrimination step (blind multi-model, step 3): structural sensitivity =/= semantic
    # sensitivity. Report the 6/8 as structural, and never as validation.

    run = {
        "run_id": f"CONTRAST-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        "benchmark_version": "v0", "family": "PATALA-CONTRAST-SET",
        "detector": DETECTOR_ID, "verifier_version": VERIFIER_VERSION,
        "execution_base_sha": git(["rev-parse", "HEAD"]), "artifact_commit_sha": None,
        "working_tree_dirty": bool(git(["status", "--porcelain"])),
        "target": "ARG-GOLD-002",
        "date": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "corruptions": kinds,
        "results": rows,
        "summary": {
            "n_types": len(kinds),
            "structurally_detected": detected,
            "structural_sensitivity": round(detected / len(kinds), 3),
            "note": "deterministic structural floor; semantic discrimination measured separately (blind multi-model)",
        },
    }
    os.makedirs(RUNS_DIR, exist_ok=True)
    out = os.path.join(RUNS_DIR, f"contrast-{run['run_id'].split('-',1)[1]}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(run, f, indent=2)
    run["artifact_commit_sha"] = git(["log", "-1", "--format=%H", "--", os.path.relpath(out, ROOT)]) or None
    with open(out, "w", encoding="utf-8") as f:
        json.dump(run, f, indent=2)

    print(f"CONTRAST-SET benchmark — target ARG-GOLD-002")
    print(f"  structural sensitivity: {run['summary']['structural_sensitivity']} "
          f"({detected}/{len(kinds)} corruption types detectable as a change)")
    for r in rows:
        print(f"    {r['corruption']:22} {'DETECTED' if r['detected'] else 'MISSED'} {r['flags'][:2]}")
    print(f"\n  run: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
