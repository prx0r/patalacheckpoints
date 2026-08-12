#!/usr/bin/env python3
"""pipeline/night_review.py — review the unattended night run's outputs.

Reads the per-verse verdicts (agent3-autonomous-log.jsonl) + the per-work records
(night-review.jsonl) and prints a reviewable summary: per work, committed/failed/
abstained, the validation verdicts, and sampled glosses + close translations so a
human can judge output quality. Judge on: sense-correctness (school/period), gloss
fidelity, abstention quality, false-certainty, and validation honesty.

Usage:
  python3 pipeline/night_review.py [--n 10]
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUTO = ROOT / "data/corpus/downloads/agent3-autonomous-log.jsonl"
NIGHT = ROOT / "data/corpus/downloads/night-review.jsonl"


def load(path: Path) -> list[dict]:
    recs = []
    if not path.exists():
        return recs
    for line in path.open(encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            recs.append(json.loads(line))
        except Exception:
            continue
    return recs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=6, help="sample verses per work")
    a = ap.parse_args()

    auto = load(AUTO)
    night = load(NIGHT)

    print("=" * 70)
    print("NIGHT RUN REVIEW")
    print("=" * 70)
    for r in night:
        if r.get("event") == "NIGHT_START":
            print(f"\nstarted: {r['ts']} | config: {r['config']}")
        elif r.get("event") == "WORK_SUMMARY":
            s = r["summary"]
            print(f"\n## WORK {r['work_id']} @ {r['ts']}")
            print(f"   attempted={s.get('verses_attempted')} committed={s.get('verses_committed')} "
                  f"failed={s.get('verses_failed')} abstained={s.get('abstentions')}")
            for f in s.get("failures", [])[:5]:
                print(f"   FAIL {f.get('passage_id')}: {f.get('why')}")
        elif r.get("event") == "WORK_ERROR":
            print(f"\n## WORK {r['work_id']} ERROR: {r.get('error')}")
        elif r.get("event") == "HALT_TOO_MANY_FAILURES":
            print(f"\n## HALT (too many failures) at {r['work_id']}")
        elif r.get("event") == "NIGHT_END":
            print(f"\nEND: {r['ts']} rounds={r.get('rounds_done')}")

    # per-verse verdicts (sample)
    verdicts = [r for r in auto if "passage_id" in r and "decisions" in r]
    print("\n" + "=" * 70)
    print(f"PER-VERSE VERDICTS ({len(verdicts)} in log) — sample {a.n} most recent")
    print("=" * 70)
    for v in verdicts[-a.n:]:
        val = v.get("validation") or {}
        commits = [d for d in v.get("decisions", []) if d.get("action") == "COMMIT_L0"]
        fails = [d for d in v.get("decisions", []) if d.get("action") == "FAIL_VALIDATION"]
        tag = f"COMMIT v{commits[0]['version']}" if commits else ("FAIL" if fails else "?")
        print(f"\n  {v.get('passage_id')} [{tag}] n={v.get('n_records')} p0_pass={val.get('p0_pass')} "
              f"unknown={val.get('unknown')} PASS={val.get('PASS')}")
        print(f"    verse: {v.get('verse','')[:70]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
