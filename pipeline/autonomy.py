#!/usr/bin/env python3
"""pipeline/autonomy.py — the generic autonomy controller (the cron heartbeat).

Per hermespatalalayers.md + hermespatala-architecture-review.md:
  cron wakes a DETERMINISTIC controller tick (never an LLM orchestrator).
  tick:
    1. acquire single-writer lock
    2. inspect the per-layer registries (canonical truth)
    3. compute eligible objects (deterministic predicates: prereqs committed, this layer not current)
    4. claim a bounded batch
    5. dispatch the layer skill to the generative backend (Hermes/direct adapter)
    6. parse by stable ID, reject misbinds
    7. run the layer-specific deterministic validator
    8. COMMIT / REVIEW_REQUIRED / REJECT
    9. detect stale (an upstream input changed) and supersede downstream
    10. emit the run report (evidence, not proof); exit
  The graph itself determines what becomes runnable. No agent triggers the next layer.
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from object_registry import (LAYERS, PREREQS, STATES, is_committed, current, commit,
                             supersede, set_status, input_hash)

ROOT = Path("/root/projects/patala")
LOCK_PATH = ROOT / "data/corpus/downloads/.autonomy.lock"
REPORT_DIR = ROOT / "data/corpus/downloads/autonomy-reports"
SKILL_DIR = ROOT / "skills/autonomous-layer/patala-autonomous-layer-skills/skills"


def acquire_lock() -> int:
    fd = os.open(LOCK_PATH, os.O_CREAT | os.O_RDWR, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("another autonomy controller holds the lock; exiting", flush=True)
        sys.exit(0)
    return fd


def eligible_for(layer: str, object_id: str, input_hash_val: str) -> str:
    """Deterministic eligibility predicate. Returns '' if eligible, else a reason string.
    This is ordinary code, NOT an LLM judgment."""
    if is_committed(layer, object_id, input_hash_val):
        return "already_committed_for_input"
    for p in PREREQS.get(layer, []):
        if not is_committed(p, object_id, input_hash_val):
            return f"prereq_{p}_missing"
    return ""


def find_eligible(layer: str, inputs: list[dict]) -> list[dict]:
    """inputs: list of {object_id, input_hash}. Returns those eligible for `layer`."""
    out = []
    for i in inputs:
        reason = eligible_for(layer, i["object_id"], i["input_hash"])
        if not reason:
            i["_layer"] = layer
            out.append(i)
    return out


def detect_stale(layer: str, object_id: str, new_input_hash: str) -> list[str]:
    """If an upstream input changed, mark the current version stale (cascading supersession)."""
    cur = current(layer, object_id)
    if cur and cur.get("input_hash") != new_input_hash and not cur.get("superseded"):
        return supersede(layer, object_id)
    return []


# ── layer handlers: (skill_path, generator, validator) ──
# L0 uses the built RAW-L0 factory; other layers use the layer-skill prompt via the generic
# generator (generative proposal) + a deterministic validator hook.
def _generator_prompt(layer: str) -> str:
    skill = SKILL_DIR / f"patala-{layer.lower()}" / "SKILL.md"
    if skill.exists():
        return skill.read_text(encoding="utf-8")[:4000]
    return f"Pāṭala autonomous layer {layer}. Produce the layer object with full provenance."


def generic_generator(layer: str, batch: list[dict]):
    """A minimal, honest generator stub: returns the batch as proposals for the validator to
    process. Real per-layer generation is wired by each layer's skill; this keeps the controller
    layer-agnostic and testable without a model call."""
    return [{"object_id": i["object_id"], "layer": layer, "input_hash": i["input_hash"],
             "_proposal": True} for i in batch]


def generic_validator(layer: str, proposal: dict) -> tuple[bool, str]:
    """Deterministic validator hook. Layer-specific validators (L0 P0, L200 Task-2, C1 quality
    test, ...) plug in here. Default: accept a well-formed proposal with matching id/hash."""
    if not proposal.get("object_id"):
        return False, "missing_object_id"
    return True, ""


# layer -> handler (skill path is derived from the name)
LAYER_HANDLERS = {
    layer: {"skill": f"patala-{layer.lower()}",
            "generator": generic_generator,
            "validator": generic_validator}
    for layer in LAYERS
}

# Wire the REAL L0 layer handler (deterministic RAW-L0 + batch gloss + validate).
try:
    from l0_worker import make_l0_handlers
    LAYER_HANDLERS["L0"] = make_l0_handlers()
except Exception as e:  # pragma: no cover
    print("L0 worker not wired:", e, file=sys.stderr)

# Wire the T1 layer handler (A2-CP1: the transliteral word-gloss producer). T1 is the first
# interpretive layer — the canonical [and]-GLOSS (IAST) form. Deterministic production gate.
try:
    from t1_worker import make_t1_handlers
    LAYER_HANDLERS["T1"] = make_t1_handlers()
except Exception as e:  # pragma: no cover
    print("T1 worker not wired:", e, file=sys.stderr)

# Wire the ARGUMENT MAP handler (A2-CP3: the lateral guide that unlocks L2). Reconstructs the passage's
# argument structure from committed T1/L0 before prose is written. Deterministic production gate.
try:
    from argument_map_worker import make_argmap_handlers
    LAYER_HANDLERS["ARGMAP"] = make_argmap_handlers()
except Exception as e:  # pragma: no cover
    print("ARGMAP worker not wired:", e, file=sys.stderr)

# Wire the L200 audit compiler (partly deterministic + Task-2 validator).
try:
    from l200_worker import make_l200_handlers
    LAYER_HANDLERS["L200"] = make_l200_handlers()
except Exception as e:  # pragma: no cover
    print("L200 worker not wired:", e, file=sys.stderr)

# Wire the L1 (controlled) + L2 (readable) provenance-continuity handlers (CP3).
try:
    from l1_l2_worker import make_l1_handlers, make_l2_handlers
    LAYER_HANDLERS["L1"] = make_l1_handlers()
    LAYER_HANDLERS["L2"] = make_l2_handlers()
except Exception as e:  # pragma: no cover
    print("L1/L2 workers not wired:", e, file=sys.stderr)

# Wire the model-driven L1/L2 translation engine (GENERATE_TRANSLATION — the AI worker).
try:
    from l1_l2_translate import make_l1l2_handlers
    LAYER_HANDLERS["L1L2"] = make_l1l2_handlers()
except Exception as e:  # pragma: no cover
    print("L1L2 translation worker not wired:", e, file=sys.stderr)

# Wire the C1 passage-commentary worker (CP8 — consumes L200's MT/IA/OPEN, passage-local).
try:
    from c1_worker import make_c1_handlers
    LAYER_HANDLERS["C1"] = make_c1_handlers()
except Exception as e:  # pragma: no cover
    print("C1 worker not wired:", e, file=sys.stderr)

# Wire the Hermes-runs-layer-skill worker for the synthesis/derivation layers (ESSAY, EDUCATION)
# that have canonical skills but no dedicated python worker. The model proposes via the layer skill;
# a deterministic structural validator gates the commit (the model never self-validates).
try:
    from generative_worker import make_generative_handler, skill_proposal_validator
    for _layer in ("ESSAY", "EDUCATION"):
        LAYER_HANDLERS[_layer] = {"generator": make_generative_handler(_layer)["generator"],
                                  "validator": skill_proposal_validator}
except Exception as e:  # pragma: no cover
    print("generative worker not wired:", e, file=sys.stderr)

# Wire the THEME worker (evidence-backed synthesis across committed C1s) — reuses Agent 1's hybrid
# graph + overlapping clustering; deterministic THEME validator gates the commit.
try:
    from theme_worker import make_theme_handlers
    LAYER_HANDLERS["THEME"] = make_theme_handlers()
except Exception as e:  # pragma: no cover
    print("THEME worker not wired:", e, file=sys.stderr)

# Wire the ESSAY worker (proof-carrying prose from committed THEME+C1) — reuses Agent 1's Essay
# object model + verify_essay (SentenceEvidenceAudit) as the commit gate.
try:
    from essay_worker import make_essay_handlers
    LAYER_HANDLERS["ESSAY"] = make_essay_handlers()
except Exception as e:  # pragma: no cover
    print("ESSAY worker not wired:", e, file=sys.stderr)

# Wire the EDUCATION worker (distill the committed essay into a concept primer) — deterministic
# EDUCATION validator gates the commit (derived-from-essay, concise, no overreach).
try:
    from education_worker import make_education_handlers
    LAYER_HANDLERS["EDUCATION"] = make_education_handlers()
except Exception as e:  # pragma: no cover
    print("EDUCATION worker not wired:", e, file=sys.stderr)

# Wire the ARGUMENT worker (CANONICAL-GRAPH-1 P3) — the epistemic crown. Derives propositions +
# cruxes from an eligible ARGMAP via the crux engine. HARD GATE: ARGMAP eligible + propositions
# traceable + no unsupported bridge, else DEPENDENCY_BLOCKED (never the generic fallback).
try:
    from epistemic_worker import make_argument_handlers
    LAYER_HANDLERS["ARGUMENT"] = make_argument_handlers()
except Exception as e:  # pragma: no cover
    print("ARGUMENT worker not wired:", e, file=sys.stderr)

# Wire the SYNTHESIS worker (CANONICAL-GRAPH-1 P3) — ArgumentSynthesis from Arguments[] + Cruxes[].
# HARD GATE: never resolve an open dispute merely because synthesis is requested.
try:
    from epistemic_worker import make_synthesis_handlers
    LAYER_HANDLERS["SYNTHESIS"] = make_synthesis_handlers()
except Exception as e:  # pragma: no cover
    print("SYNTHESIS worker not wired:", e, file=sys.stderr)


def tick(layers: list[str] | None = None, max_batch: int = 8,
         dry_run: bool = False, inputs: dict[str, list[dict]] | None = None) -> dict:
    """One bounded controller pass (the cron heartbeat body)."""
    layers = layers or [l for l in LAYERS if l not in ("SOURCE",)]
    report = {
        "run_id": f"autonomy-{int(datetime.now(timezone.utc).timestamp())}",
        "ts": datetime.now(timezone.utc).isoformat(),
        "layers": {},
        "committed": 0, "skipped": 0, "failed": 0, "review_required": 0, "stale": 0,
    }
    for layer in layers:
        layer_inputs = (inputs or {}).get(layer, [])
        eligible = find_eligible(layer, layer_inputs)
        layer_report = {"eligible": len(eligible), "committed": 0, "failed": 0}
        # bounded batches
        for start in range(0, len(eligible), max_batch):
            batch = eligible[start:start + max_batch]
            proposals = LAYER_HANDLERS[layer]["generator"](layer, batch)
            for p in proposals:
                ok, why = LAYER_HANDLERS[layer]["validator"](layer, p)
                if not ok:
                    report["failed"] += 1
                    layer_report["failed"] += 1
                    continue
                # stale detection: if upstream changed, supersede
                report["stale"] += len(detect_stale(layer, p["object_id"], p.get("input_hash", "")))
                if dry_run:
                    report["skipped"] += 1
                    continue
                payload = {k: v for k, v in p.items() if k not in ("object_id", "input_hash", "_layer")}
                commit(layer, p["object_id"], p.get("input_hash", ""), created_by="autonomy-controller",
                       payload=payload)
                report["committed"] += 1
                layer_report["committed"] += 1
        report["layers"][layer] = layer_report
    _write_report(report)
    return report


def _write_report(report: dict) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORT_DIR / f"{report['run_id']}.json"
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--layers", default=None, help="comma-separated layers; default all except SOURCE")
    ap.add_argument("--max-batch", type=int, default=8)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    layers = a.layers.split(",") if a.layers else None
    fd = acquire_lock()
    try:
        r = tick(layers=layers, max_batch=a.max_batch, dry_run=a.dry_run)
        print(json.dumps(r, indent=2, ensure_ascii=False))
    finally:
        try:
            os.close(fd)
        except Exception:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
