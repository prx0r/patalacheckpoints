#!/usr/bin/env python3
"""pipeline/eval_sanskrit.py — the Sanskrit model-eval harness (replicates IndicParam, arXiv 2512.00333).

Answers "which model is actually good at Sanskrit" by running any model against the IndicParam Sanskrit
subset (1,315 Sanskrit + 971 Sanskrit-English = 2,286 questions, real UGC-NET gold). Same methodology as
the paper: zero-shot MCQ, deterministic (temperature 0), regex letter extraction.

Run via the model router / adapter so a model can come from ANY provider (free Cloudflare, discounted
opencode-go, market OpenRouter). The measured Sanskrit accuracy feeds model-quality.json — so the router
uses OUR measured scores, not just the paper's.

Usage:
  eval_sanskrit.py --model @cf/meta/llama-4-scout-17b-16e-instruct --provider cloudflare --limit 50
  eval_sanskrit.py --model deepseek-v4-flash --provider opencode-go --limit 20
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(str(Path(__file__).resolve().parents[1]))
DATA = ROOT / "data" / "benchmarks" / "indicparam" / "data.csv"
if str(ROOT / "pipeline") not in sys.path:
    sys.path.insert(0, str(ROOT / "pipeline"))


def load_sanskrit(limit: int | None = None) -> list[dict]:
    """The Sanskrit + Sanskrit-Mix questions (with the gold answer)."""
    rows = []
    with open(DATA, encoding="utf-8", errors="ignore") as f:
        for r in csv.DictReader(f):
            if r.get("subject", "").lower() in ("sanskrit", "sanskrit mix"):
                rows.append(r)
    if limit:
        rows = rows[:limit]
    return rows


def make_prompt(row: dict) -> str:
    """The exact IndicParam MCQ prompt (verified from their eval script)."""
    lang = row.get("subject", "Sanskrit")
    return (f"{row.get('question_text','')}\n\n"
            f"A) {row.get('option_a','')}\nB) {row.get('option_b','')}\n"
            f"C) {row.get('option_c','')}\nD) {row.get('option_d','')}\n\n"
            f"The above question is written in {lang} language. Please analyze the question and "
            f"options carefully, and select the correct answer. Respond ONLY with one letter "
            f"(A, B, C, or D) corresponding to the correct option. Do not provide any explanation "
            f"or additional text.")


def extract_answer(response: str) -> str:
    """Regex letter extraction (mirrors their extract_answer)."""
    if not response:
        return ""
    m = re.search(r"(?:^|answer[:\s]*|choice[:\s]*|option[:\s]*)([ABCD])(?:\)|\.|\s|$)", response, re.I)
    return (m.group(1).upper() if m else "")


def _run_via_router(rows: list[dict], model: str, provider: str | None,
                    quality_required: float | None = None) -> list[dict]:
    """Run the questions through the model router (so free/discounted providers are used)."""
    import model_router as MR
    from model_adapter import get_adapter

    router = MR.Router()
    pid, mdl = (provider, model) if provider else router.pick(quality_required)
    if pid is None or mdl is None:
        raise RuntimeError("no provider/model available in the router")
    adapter = get_adapter("direct")  # OpenAI-compatible completion
    # load provider creds (cloudflare token etc.)
    prov = MR.PROVIDERS.get(pid, {})
    env = prov.get("env_key")
    results = []
    for row in rows:
        prompt = make_prompt(row)
        if pid == "cloudflare":
            res = _cf_complete(prov, mdl, prompt)
        else:
            res = adapter.complete_json("You are answering a Sanskrit multiple-choice exam question.",
                                        prompt, mdl, timeout=60)
        if not res.ok:
            # quota/error → swap provider via router
            router.exhaust(pid, f"error: {res.error}")
            pid2, mdl2 = router.pick(quality_required)
            if pid2 and mdl2:
                pid, mdl = pid2, mdl2
                res = adapter.complete_json("You are answering a Sanskrit exam.", prompt, mdl2, timeout=60)
        pred = extract_answer(res.content)
        results.append({"question_id": row.get("unique_question_id") or row.get("id"),
                        "question_type": row.get("question_type"),
                        "correct": (row.get("correct_answer") or "").strip().lower(),
                        "pred": pred.lower(), "ok": res.ok})
    return results


def _cf_complete(prov: dict, model: str, prompt: str, timeout: int = 60) -> object:
    """Cloudflare Workers AI completion (REST). Returns a ModelResult-like object."""
    import os, urllib.request, json as _j
    from model_adapter import ModelResult
    token = os.environ.get(prov["env_key"], "")
    account = os.environ.get(prov.get("env_account", ""), "")
    url = f"https://api.cloudflare.com/client/v4/accounts/{account}/ai/run/{model}"
    body = _j.dumps({"messages": [{"role": "user", "content": prompt}], "max_tokens": 50}).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = _j.loads(r.read())
            return ModelResult(content=(d.get("result") or {}).get("response", ""), model=model, ok=True)
    except Exception as e:
        return ModelResult(content="", ok=False, error=str(e)[:200], model=model)


def score(results: list[dict]) -> dict:
    total = len(results)
    correct = sum(1 for r in results if r["pred"] == r["correct"])
    by_type = {}
    for r in results:
        t = r["question_type"] or "?"
        by_type.setdefault(t, [0, 0])
        by_type[t][1] += 1
        if r["pred"] == r["correct"]:
            by_type[t][0] += 1
    return {"total": total, "correct": correct,
            "accuracy": round(correct / total * 100, 1) if total else 0.0,
            "by_type": {t: {"correct": c, "total": n, "acc": round(c / n * 100, 1) if n else 0}
                        for t, (c, n) in by_type.items()}}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", required=True, help="the model id to evaluate")
    ap.add_argument("--provider", default=None, help="provider (cloudflare/opencode-go/openrouter) or auto-router")
    ap.add_argument("--limit", type=int, default=None, help="limit questions (quick smoke test)")
    ap.add_argument("--save", action="store_true", help="write the measured score to model-quality.json")
    a = ap.parse_args()

    rows = load_sanskrit(a.limit)
    print(f"=== SANSKRIT EVAL: {a.model} (provider={a.provider or 'auto-router'}, n={len(rows)}) ===")
    results = _run_via_router(rows, a.model, a.provider)
    s = score(results)
    print(f"  accuracy: {s['correct']}/{s['total']} = {s['accuracy']}%")
    for t, v in s["by_type"].items():
        print(f"    {t}: {v['correct']}/{v['total']} = {v['acc']}%")
    if a.save:
        _save_quality(a.model, s["accuracy"])
    return 0


def _save_quality(model_id: str, acc: float):
    import json
    qf = ROOT / "data" / "model-quality.json"
    d = json.loads(qf.read_text(encoding="utf-8"))
    base = model_id.split("/")[-1]
    d["models"][base] = {**d["models"].get(base, {}), "sanskrit": acc, "measured_by": "eval_sanskrit"}
    qf.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  ✓ saved measured score for {base} → model-quality.json")


if __name__ == "__main__":
    sys.exit(main())
