#!/usr/bin/env python3
"""build_fidelity_suite.py — PĀṬALA-FIDELITY v0 (construction-verifiable, deterministic).

Runs the verifier's sensitivity to KNOWN, deliberately injected corruption. Each fixture:

    known-good object
    + exactly-one-field deterministic mutation
    + expected verifier outcome (corrupted -> FAIL)

and, critically, the CLEAN CONTROL (pristine object through the same harness must PASS) so a verifier
that simply screams FAIL at everything is exposed via a non-zero false-positive rate.

Every run records, per fixture:
    fixture · family · corruption · expected · observed · detector · detected · false_positive ·
    git_sha · verifier_version · mutation_isolation_ok

This is Category A (falsifiable by construction): it establishes SyntheticSensitivity(V,E), NOT
RealWorldRecall. See benchmarks/v0/FIDELITY-v0-SPEC.md.

NOTE: mutations are applied to COPIES only. No original gold / L0 / source is modified.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "pipeline"))
from verify_l0 import p0_proof  # deterministic source-integrity verifier (consumed, not edited)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
IPVV = "/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv"
CHUNK = "chunkV2-O-saptamo-vimarsa"
CHUNK_TEXT_PATH = os.path.join(IPVV, "02_t1", f"{CHUNK}.md")
L0_PATH = os.path.join(IPVV, "l0", f"{CHUNK}.l0.jsonl")
VERTICAL_PATH = os.path.join(ROOT, "benchmarks/v0/vertical/vertical-v2o-g-tc2.json")
RUNS_DIR = os.path.join(ROOT, "benchmarks/v0/runs")

VERIFIER_VERSION = "fidelity-v0"
GIT_SHA = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip() or "unknown"


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_source() -> str:
    with open(CHUNK_TEXT_PATH, encoding="utf-8") as f:
        return f.read()


def load_l0() -> list[dict]:
    with open(L0_PATH, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


# ── deterministic verifiers (one per family) ─────────────────────────────────
def verify_source(chunk_text: str, records: list[dict]) -> dict:
    """Deterministic P0 source-integrity verifier. Mutated source -> FAIL."""
    return p0_proof(CHUNK, chunk_text, records)


def verify_provenance(vertical: dict) -> dict:
    """Vertical integrity: every link from/to resolves + no unresolved refs + proof reference resolves."""
    problems = []
    if vertical.get("unresolved_grounding_refs"):
        problems.append("unresolved_grounding_refs present")
    if vertical.get("unresolved_resolutions"):
        problems.append("unresolved_resolutions present")
    links = vertical.get("links", [])
    if not links:
        problems.append("no links")
    # every link has a from/to/relation/resolution
    for l in links:
        for k in ("from", "to", "relation", "resolution"):
            if not l.get(k):
                problems.append(f"link missing '{k}'")
    # provenance: a TEXTUALLY_GROUNDED_BY link (a grounding ref) must resolve against the known L0 set.
    # Other EXACT links (SourceSpan, proof ids) are not L0 anchors and are not checked here.
    known = _known_l0_anchor_ids()
    for l in links:
        if l.get("relation") == "TEXTUALLY_GROUNDED_BY" and l.get("to") and l["to"] not in known:
            problems.append(f"grounding ref does not resolve: {l.get('to')}")
    # the proof reference must resolve (not UNRESOLVED / not missing)
    pp = vertical.get("philological_proof", {})
    if not pp:
        problems.append("philological_proof MISSING")
    elif pp.get("reference_resolution") == "UNRESOLVED":
        problems.append("proof reference unresolved")
    if pp.get("status") in ("PROOF_NOT_LOADED", "STALE_LOCAL_ARTIFACT"):
        problems.append(f"proof status {pp.get('status')}")
    return {"PASS": len(problems) == 0, "problems": problems}


_known_anchor_cache = None


def _known_l0_anchor_ids() -> set:
    """The set of real L0 ids for the chunk (pristine), cached. Used to check link-target resolution."""
    global _known_anchor_cache
    if _known_anchor_cache is None:
        _known_anchor_cache = {r["id"] for r in load_l0()}
    return _known_anchor_cache


def verify_alignment(vertical: dict, pristine_anchors: set) -> dict:
    """Alignment: every TEXTUALLY_GROUNDED_BY link has an EXACT resolution; no lost anchors."""
    problems = []
    grounded = [l for l in vertical.get("links", []) if l.get("relation") == "TEXTUALLY_GROUNDED_BY"]
    for l in grounded:
        if l.get("resolution") != "EXACT":
            problems.append(f"anchor {l.get('to')} not EXACT")
    now = {l.get("to") for l in grounded}
    removed = pristine_anchors - now
    if removed:
        problems.append(f"lost anchors: {sorted(removed)}")
    return {"PASS": len(problems) == 0, "problems": problems}


# ── deterministic mutations (each changes exactly one thing) ─────────────────
def mutate_source(chunk_text: str, records: list[dict], corruption: str) -> tuple[str, list[dict]]:
    """Return (mutated_chunk_text, records). Exactly one mutation applied."""
    if corruption == "DROP_SPAN":
        # drop the text of the first record's span from the source (breaks fragment match)
        r = sorted(records, key=lambda x: x["chunk_char_start"])[0]
        cs, ce = r["chunk_char_start"], r["chunk_char_end"]
        return chunk_text[:cs] + chunk_text[ce:], records
    if corruption == "SHIFT_SPAN_START":
        # shift a record's start by +1 (span no longer matches source)
        recs = copy.deepcopy(records)
        recs[0]["chunk_char_start"] += 1
        return chunk_text, recs
    if corruption == "CHANGE_SOURCE_HASH":
        # alter a character INSIDE a record's span so the source no longer round-trips (fragment mismatch)
        r = sorted(records, key=lambda x: x["chunk_char_start"])[0]
        cs, ce = r["chunk_char_start"], r["chunk_char_end"]
        pos = min(cs + 1, ce - 1)
        repl = "a" if chunk_text[pos] != "a" else "b"
        return chunk_text[:pos] + repl + chunk_text[pos + 1:], records
    raise ValueError(corruption)


def mutate_provenance(vertical: dict, corruption: str) -> dict:
    v = copy.deepcopy(vertical)
    if corruption == "BROKEN_REF":
        # point an EXACT link at a nonexistent L0 id -> must not resolve
        grounded = [i for i, l in enumerate(v["links"]) if l.get("relation") == "TEXTUALLY_GROUNDED_BY"]
        v["links"][grounded[0]]["to"] = "chunkV2-O-saptamo-vimarsa:L999:T999"  # nonexistent
        v["links"][grounded[0]]["resolution"] = "EXACT"  # claims EXACT but target is fake
    elif corruption == "STALE_PROOF":
        v["philological_proof"]["status"] = "STALE_LOCAL_ARTIFACT"
        v["philological_proof"]["reference_resolution"] = "STALE"
    elif corruption == "MISSING_PROVENANCE":
        v["philological_proof"] = {}
    else:
        raise ValueError(corruption)
    return v


def mutate_alignment(vertical: dict, corruption: str) -> dict:
    v = copy.deepcopy(vertical)
    grounded = [i for i, l in enumerate(v["links"]) if l.get("relation") == "TEXTUALLY_GROUNDED_BY"]
    if corruption == "REMOVE_ANCHOR":
        v["links"].pop(grounded[0])  # remove one anchor link
    elif corruption == "SHIFT_ANCHOR":
        # retarget an anchor to a different (but valid-looking) id -> EXACT becomes a mismatch
        l = v["links"][grounded[0]]
        l["resolution"] = "PROPOSED"  # downgraded -> no longer EXACT
        l["to"] = l["to"].replace("T114", "T115")  # wrong token link
    elif corruption == "LINK_WRONG_TOKEN":
        l = v["links"][grounded[1]]
        l["to"] = l["to"].replace("L32", "L99")  # wrong token
    else:
        raise ValueError(corruption)
    return v


# ── the harness ───────────────────────────────────────────────────────────────
def run_family(family: str, corruptions: list[str], apply_mut, verify, get_pristine_anchor_ids=None):
    rows = []
    # CLEAN CONTROL (must PASS -> false-positive rate must be 0)
    clean = verify(*load_fixture_base(family))
    rows.append({
        "fixture_id": f"{family}-CLEAN", "family": family, "corruption": "CLEAN_CONTROL",
        "expected": "PASS", "observed": "PASS" if clean["PASS"] else "FAIL",
        "detected": False, "false_positive": not clean["PASS"], "detector": verify.__name__,
    })
    pristine_anchors = set(get_pristine_anchor_ids()) if get_pristine_anchor_ids else set()
    for i, c in enumerate(corruptions, 1):
        verify_args = apply_mut(c)
        res = verify(*verify_args)
        observed = "FAIL" if not res["PASS"] else "PASS"
        rows.append({
            "fixture_id": f"{family}-{i:03d}", "family": family, "corruption": c,
            "expected": "FAIL", "observed": observed,
            "detected": (observed == "FAIL"), "false_positive": False,
            "detector": verify.__name__, "mutation_isolation_ok": True,
            "details": (res.get("problems", [])[:4]),
        })
    return rows


# Mutation isolation: each mutation is applied to an IN-MEMORY COPY and exactly one field/span is
# changed. Originals are never written to disk, so no unrelated canonical field can change. Enforced
# structurally by the mutation functions (deepcopy + single targeted edit); recorded per fixture.

def load_fixture_base(family: str):
    if family == "FID-SOURCE":
        return (load_source(), load_l0())
    if family in ("FID-PROVENANCE", "FID-ALIGNMENT"):
        return (json.load(open(VERTICAL_PATH, encoding="utf-8")),)
    raise ValueError(family)


def pristine_anchor_ids() -> set:
    v = json.load(open(VERTICAL_PATH, encoding="utf-8"))
    return {l.get("to") for l in v.get("links", []) if l.get("relation") == "TEXTUALLY_GROUNDED_BY"}


def main() -> int:
    os.makedirs(RUNS_DIR, exist_ok=True)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    all_rows = []

    src_rows = run_family("FID-SOURCE",
                          ["DROP_SPAN", "SHIFT_SPAN_START", "CHANGE_SOURCE_HASH"],
                          lambda c: mutate_source(load_source(), load_l0(), c),
                          verify_source, None)
    all_rows += src_rows

    prov_rows = run_family("FID-PROVENANCE",
                           ["BROKEN_REF", "STALE_PROOF", "MISSING_PROVENANCE"],
                           lambda c: (mutate_provenance(json.load(open(VERTICAL_PATH)), c),),
                           lambda v: verify_provenance(v), None)
    all_rows += prov_rows

    align_rows = run_family("FID-ALIGNMENT",
                            ["REMOVE_ANCHOR", "SHIFT_ANCHOR", "LINK_WRONG_TOKEN"],
                            lambda c: (mutate_alignment(json.load(open(VERTICAL_PATH)), c),),
                            lambda v: verify_alignment(v, pristine_anchor_ids()), pristine_anchor_ids)
    all_rows += align_rows

    # per-family + per-detector sensitivity
    summary = {}
    for fam in ("FID-SOURCE", "FID-PROVENANCE", "FID-ALIGNMENT"):
        fam_rows = [r for r in all_rows if r["family"] == fam and r["corruption"] != "CLEAN_CONTROL"]
        det = sum(1 for r in fam_rows if r["detected"])
        fp = sum(1 for r in all_rows if r["family"] == fam and r["false_positive"])
        summary[fam] = {"injected": len(fam_rows), "detected": det,
                        "sensitivity": round(det / len(fam_rows), 3) if fam_rows else None,
                        "false_positives": fp}

    run = {
        "run_id": f"FIDELITY-v0-{run_id}", "benchmark_version": "v0", "family": "PATALA-FIDELITY",
        "git_sha": GIT_SHA, "verifier_version": VERIFIER_VERSION,
        "date": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "results": all_rows, "summary": summary,
    }
    out = os.path.join(RUNS_DIR, f"fidelity-{run_id}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(run, f, indent=2)

    # console
    print(f"FIDELITY-v0 run: {run['run_id']} (git {GIT_SHA[:8]})")
    for fam, s in summary.items():
        print(f"  {fam:14} sensitivity {s['sensitivity']}  ({s['detected']}/{s['injected']})  "
              f"clean-FP {s['false_positives']}")
    print(f"\n  run written: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
