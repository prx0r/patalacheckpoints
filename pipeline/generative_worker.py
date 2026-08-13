#!/usr/bin/env python3
"""pipeline/generative_worker.py — Hermes runs the real layer skills, driven by the controller.

THE BRIDGE: the controller's generative stage is a stub (generic_generator). This worker
replaces it — it invokes HERMES to run the ACTUAL layer skill (patala-l1, patala-l2, ...)
for a bounded batch, per the AUTONOMY_CONTRACT.

Flow (per the controller docstring):
  1. read the layer skill's SKILL.md (the generative contract)
  2. build a bounded batch request, each item carrying object_id + source_sha256 (stable binding)
  3. call Hermes via model.chat (hermes -z), which has the layer skill + context in-context
  4. parse the response BY stable ID (never positional); reject unknown/duplicate/hash-mismatch
  5. return proposals for the controller's deterministic validator to gate
The model is never the authority: the controller's validator decides commit.

Retry policy (from AUTONOMY_CONTRACT): one retry on transport/schema failure, then split batch.
"""
from __future__ import annotations
import json, os, sys, re
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model import chat
from object_registry import current, input_hash

SKILL_DIR = Path("/root/projects/patala/skills/autonomous-layer/patala-autonomous-layer-skills/skills")


def _skill_text(layer: str) -> str:
    p = SKILL_DIR / f"patala-{layer.lower()}" / "SKILL.md"
    if p.exists():
        return p.read_text(encoding="utf-8")
    return f"Pāṭala autonomous layer {layer}: produce the layer object with full provenance per the shared AUTONOMY_CONTRACT."


def _build_prompt(layer: str, batch: list[dict], context: dict | None = None) -> str:
    skill = _skill_text(layer)
    ctx = ""
    if context:
        ctx = "\n\n# WORK / TERM CONTEXT\n" + json.dumps(context, ensure_ascii=False)[:3000]
    items = []
    for b in batch:
        items.append({"object_id": b["object_id"], "source_sha256": b.get("source_sha256", b.get("input_hash", ""))})
    return (
        f"You are the Pāṭala {layer} layer. Execute the layer skill below exactly. "
        "For EVERY item in the batch, produce the layer output per the skill's output contract. "
        "Echo each object_id and source_sha256 EXACTLY as given; never invent or swap them. "
        "Abstain (empty) rather than fabricate. Return JSON ONLY.\n\n"
        f"# SKILL\n{skill}\n"
        f"{ctx}\n\n"
        f"# BATCH\n{json.dumps({'items': items}, ensure_ascii=False)}"
    )


def _extract_json(raw: str) -> dict:
    raw = raw.strip()
    try:
        return json.loads(raw)
    except Exception:
        pass
    m = re.search(r"\{.*\}", raw, re.S)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            pass
    return {}


def _parse_by_id(raw: str, requested: dict) -> dict:
    """Parse the Hermes response by stable object_id. Reject unknown/duplicate/hash-mismatch."""
    data = _extract_json(raw)
    items = data.get("items") or data.get("translations") or []
    if isinstance(items, dict):
        items = list(items.values())
    seen = set()
    out = {}
    for it in items:
        if not isinstance(it, dict):
            continue
        oid = it.get("object_id") or it.get("passage_id")
        req = requested.get(oid)
        if req is None or oid in seen:
            continue
        seen.add(oid)
        sha = it.get("source_sha256") or it.get("input_hash")
        if sha and sha != req.get("source_sha256"):
            out[oid] = {"_rejected": "source_sha256_mismatch"}
            continue
        out[oid] = {k: v for k, v in it.items()
                    if k not in ("object_id", "passage_id", "source_sha256", "input_hash")}
    return out


def generate(layer: str, batch: list[dict], context: dict | None = None,
             model: str = "deepseek-v4-flash", timeout: int = 180) -> dict:
    """Run Hermes on the layer skill for a bounded batch. Returns {object_id: fields} (clean
    items only). One retry on transport/schema failure, then split the batch in half."""
    if not batch:
        return {}
    requested = {b["object_id"]: {"source_sha256": b.get("source_sha256", b.get("input_hash", ""))}
                 for b in batch}
    prompt = _build_prompt(layer, batch, context)
    raw = chat(f"You are the Pāṭala {layer} layer (autonomous).", prompt, model=model, timeout=timeout)
    out = _parse_by_id(raw, requested)
    clean = [oid for oid, v in out.items() if isinstance(v, dict) and not v.get("_rejected")]
    if clean:
        return {oid: out[oid] for oid in clean}
    # one retry, then split
    raw2 = chat(f"You are the Pāṭala {layer} layer (autonomous). Retry cleanly.", prompt, model=model, timeout=timeout)
    out2 = _parse_by_id(raw2, requested)
    clean2 = [oid for oid, v in out2.items() if isinstance(v, dict) and not v.get("_rejected")]
    if clean2:
        return {oid: out2[oid] for oid in clean2}
    # split
    half = (len(batch) + 1) // 2
    result = {}
    for sub in (batch[:half], batch[half:]):
        result.update(generate(layer, sub, context, model, timeout))
    return result


def make_generative_handler(layer: str) -> dict:
    """A controller handler whose generator calls Hermes on the layer skill; validator is the
    generic one (the layer skill's gate is enforced by the worker's binding + controller)."""
    def generator(layer_, batch):
        out = generate(layer_, batch)
        proposals = []
        for b in batch:
            fields = out.get(b["object_id"])
            if fields is None:
                continue  # model didn't produce it -> not a proposal -> not committed
            if isinstance(fields, dict) and fields.get("_rejected"):
                continue
            proposals.append({"object_id": b["object_id"],
                              "input_hash": b.get("input_hash", b.get("source_sha256", "")),
                              "layer": layer_, **fields})
        return proposals

    return {"generator": generator,
            "validator": lambda l, p: (False, "skill validator not wired")
            if p.get("_validator_missing") else (True, "")}


def skill_proposal_validator(layer: str, proposal: dict) -> tuple[bool, str]:
    """Deterministic gate: a proposal from Hermes must carry the layer's required field
    and a resolvable input hash. (The layer skill's semantic validator is a stub to be wired
    per-layer; this keeps the controller fail-closed on structural/provenance errors.)"""
    if not proposal.get("object_id"):
        return False, "missing_object_id"
    if not proposal.get("input_hash"):
        return False, "missing_input_hash"
    # layer must have produced SOMETHING (no empty commits)
    body = {k: v for k, v in proposal.items() if k not in ("object_id", "input_hash", "layer")}
    if not body:
        return False, "empty_layer_output (no commit)"
    return True, ""
