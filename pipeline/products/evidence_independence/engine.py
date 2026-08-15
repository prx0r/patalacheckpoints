#!/usr/bin/env python3
"""products/evidence_independence/engine.py — the evidence-independence product.

Upgrades the corroboration model with a REAL independence classification, closing the "3 papers say X
may be 1 origin" gap (SOURCE_ECHO). Uses:
  - the REAL corroboration registry (data/corpus/registries/corroboration-registry.jsonl)
  - the REAL source assertions (attributed_to authors + DOIs)
  - the finished OpenCitations adapter (classify_independence, now with live Crossref SAME_AUTHOR)

For each corroborated proposition, classify each corroborating source's INDEPENDENCE:
  INDEPENDENT_AUTHOR   the source does not cite / derive from the target
  DERIVED_CITATION     the source cites the target (may just repeat it)
  SAME_AUTHOR          same author as the target (likely not independent)
  ECHO                 multiple corroborators all deriving from ONE origin

Standalone + deterministic; the OpenCitations fetch is honest (UNAVAILABLE -> OPEN, never fabricated).
The output is MACHINE_PROPOSED evidence — it feeds the review gate, never claims truth itself.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT / "pipeline") not in sys.path:
    sys.path.insert(0, str(ROOT / "pipeline"))
if str(ROOT / "source-evidence/production/adapters") not in sys.path:
    sys.path.insert(0, str(ROOT / "source-evidence/production/adapters"))

from opencitations import fetch_citations, classify_independence  # noqa: E402

REG = ROOT / "data/corpus/registries"


def _load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def _assertions_by_ref() -> dict:
    out = {}
    for a in _load_jsonl(REG / "assertion-registry.jsonl"):
        out.setdefault(a.get("source_assertion_id"), a)
    return out


def corroborated_propositions() -> list[dict]:
    """Group the real corroboration registry by target proposition."""
    groups = {}
    for c in _load_jsonl(REG / "corroboration-registry.jsonl"):
        groups.setdefault(c["target_proposition_ref"], []).append(c)
    return [{"proposition": prop, "corroborations": corr} for prop, corr in groups.items()]


def _source_doi(a: dict) -> str | None:
    """Extract a real DOI from a source_assertion_id like pt:assertion:10.4324/..."""
    sid = a.get("source_assertion_id") or ""
    if ":" not in sid:
        return None
    # pt:assertion:10.4324/9781315400107-34  -> 10.4324/9781315400107-34
    rest = sid.split(":", 2)[-1]
    if rest.startswith("10.") and "/" in rest:
        return rest
    return None


def independence_report(live: bool = True) -> dict:
    """Classify the independence of every corroboration on the REAL proposition(s).

    live=True: hit OpenCitations/Crossref (honest UNAVAILABLE -> OPEN). live=False: offline,
    classify from author identity only (deterministic, no network).
    """
    assertions = _assertions_by_ref()
    propositions = corroborated_propositions()
    if not propositions:
        return {"status": "NO_CORROBORATIONS", "note": "the registry is empty; run scholarly_oracle first"}

    out = []
    for prop in propositions:
        corr = prop["corroborations"]
        # build corroborating sources {source_id, doi, author} from the assertions
        sources = []
        for c in corr:
            a = assertions.get(c["source_assertion_ref"], {})
            sources.append({
                "source_id": c["source_assertion_ref"],
                "doi": _source_doi(a),
                "author": a.get("attributed_to", ""),
                "relation": c.get("relation"),
                "independence_recorded": c.get("independence", "MACHINE_SEGREGATED"),
            })
        # DEDUPLICATE: the registry records the SAME source multiple times (real data has 5x
        # Sanderson). Counting them as 5 corroborations overstates independence. Collapse to
        # one entry per unique (source_id) and report the duplicates honestly.
        unique: dict[str, dict] = {}
        for s in sources:
            unique.setdefault(s["source_id"], {**s, "duplicate_count": 0})
            unique[s["source_id"]]["duplicate_count"] += 1
        unique_sources = list(unique.values())
        dupes = sum(1 for s in unique_sources if s["duplicate_count"] > 1)
        # the target DOI: take the first corroborator with a DOI as the anchor work
        target_doi = next((s["doi"] for s in unique_sources if s["doi"]), None)
        if live and target_doi:
            try:
                oc = fetch_citations(target_doi)
                cls = classify_independence(unique_sources, target_doi, opencitations=oc)
            except Exception:
                cls = {"status": "UNAVAILABLE", "note": "open-citations fetch failed (honest OPEN)"}
        else:
            # offline deterministic classification by author identity + relation
            per = [{"source": s["source_id"], "independence":
                    ("SAME_AUTHOR" if any(o["author"] and o["author"] == s["author"]
                                          for o in unique_sources if o is not s)
                     else "INDEPENDENT_AUTHOR")} for s in unique_sources]
            cls = {"status": "OFFLINE", "per_source": per, "echo_detected": False,
                   "note": "offline: author-identity only, no citation graph"}
        out.append({
            "proposition": prop["proposition"],
            "n_corroborations_recorded": len(corr),
            "n_unique_sources": len(unique_sources),
            "duplicate_sources": dupes,
            "target_doi": target_doi,
            "independence": cls,
            # Temporal validity (Graphiti genius process): this classification is a VALID-AT snapshot,
            # not an eternal truth. `valid_at` = when it was observed; the classification is
            # invalidatable (not deleted) when the source/evidence changes. This makes "what was the
            # independence at time T" queryable.
            "temporal": {
                "valid_at": _now(),
                "invalidated": False,
                "invalidated_at": None,
                "model": "validity-window: invalidate on source/evidence change, never delete",
            },
        })
    return {"status": "OK", "propositions": out, "live": live,
            "temporal_model": "Graphiti-style validity window: each independence is a valid-at snapshot, "
                              "invalidatable not deletable"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_demo() -> dict:
    """Controlled demo against the REAL corroboration registry (offline, deterministic)."""
    return independence_report(live=False)


if __name__ == "__main__":
    import sys as _s
    live = len(_s.argv) > 1 and _s.argv[1] == "live"
    res = independence_report(live=live)
    print(json.dumps(res, indent=2, ensure_ascii=False))
