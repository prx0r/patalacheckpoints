"""products/scholar_publication/engine.py — the scholar publication surface (the Astro-continuation).

The bridge from the interactive scholar layer to the PUBLIC site. Compiles a scholar's contributions
into a static, JSON-LD, Astro-servable record — the "CV-legible output" the vision (vision-08) wants:

  > Smith, Jane. "Philological review and adjudication of IPVV 1.5.1–20." Pāṭala Critical Edition, v1.3.

This is what the static Astro site serves as immutable bytes (compute on write, read from CDN). The
interactive reviewing happens in the workbench (Next/MCP); the PUBLISHED record of it lives here.

What it provides (CPU-only, deterministic):
  - profile_record(scholar_id)   -> the JSON-LD scholar-profile page record
  - attestation_record(id)       -> the JSON-LD attestation record
  - all_profiles()               -> the compiled index (for a /scholars page + sitemap)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT / "pipeline") not in sys.path:
    sys.path.insert(0, str(_ROOT / "pipeline"))

from products.scholar_profile.engine import profile  # noqa: E402


def _load_attestations() -> list[dict]:
    p = _ROOT / "data/scholar/attestations.jsonl"
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def profile_record(scholar_id: str, name: str = "Scholar") -> dict:
    """The JSON-LD scholar-profile record (Astro-servable)."""
    p = profile(scholar_id)
    return {
        "@context": "https://schema.org",
        "@type": "Person",
        "identifier": scholar_id,
        "name": name,
        "description": "Pāṭala scholar — contribution ledger of peer review + attestation.",
        "contributions": {
            "reviews": p["n_reviews"],
            "reviews_by_decision": p["reviews_by_decision"],
            "attestations": p["n_attestations"],
            "recent_activity": p["recent_activity"],
        },
        "citeAs": f"{name}. \"Pāṭala scholarly contributions.\" Pāṭala Critical Edition.",
        "url": f"https://patala.org/scholar/{scholar_id}",
    }


def attestation_record(attestation_id: str) -> dict | None:
    """The JSON-LD attestation record (the citable artifact)."""
    for a in _load_attestations():
        if a.get("attestation_id") == attestation_id or a.get("proposal") == attestation_id:
            return {
                "@context": "https://schema.org",
                "@type": "Review",
                "identifier": a.get("attestation_id") or a.get("proposal"),
                "itemReviewed": {"identifier": a.get("target_ref"), "type": "ScholarlyArticle"},
                "reviewer": {"identifier": a.get("reviewer"), "type": "Person"},
                "reviewRating": a.get("verdict"),
                "reviewBody": a.get("rationale"),
                "datePublished": a.get("created_at"),
                "author": {"type": "Person", "identifier": a.get("reviewer")},
            }
    return None


def all_profiles() -> dict:
    """The compiled scholar index (for a /scholars page + sitemap)."""
    from collections import Counter
    reviews = [json.loads(l) for l in
               (_ROOT / "data/scholar/reviews.jsonl").read_text().splitlines() if l.strip()] \
        if (_ROOT / "data/scholar/reviews.jsonl").exists() else []
    atts = _load_attestations()
    by_reviewer = Counter(r.get("reviewer") for r in reviews) | Counter(a.get("reviewer") for a in atts)
    return {
        "schema": "patala.scholar-publication.v1",
        "scholars": [{"id": s, "n_contributions": c,
                      "url": f"https://patala.org/scholar/{s}"}
                     for s, c in by_reviewer.most_common()],
        "n_scholars": len(by_reviewer),
        "n_attestations": len(atts),
        "note": "compiled public scholar records (JSON-LD, Astro-servable, immutable)",
    }


def publish_all(out_dir: Path | None = None) -> dict:
    """Emit all scholar + attestation records as immutable JSON files (compute on write)."""
    from collections import Counter
    reviews = [json.loads(l) for l in
               (_ROOT / "data/scholar/reviews.jsonl").read_text().splitlines() if l.strip()] \
        if (_ROOT / "data/scholar/reviews.jsonl").exists() else []
    atts = _load_attestations()
    by_reviewer = Counter(r.get("reviewer") for r in reviews) | Counter(a.get("reviewer") for a in atts)
    out = out_dir or (_ROOT / "data/scholar/published")
    out.mkdir(parents=True, exist_ok=True)
    emitted = 0
    for s in by_reviewer:
        rec = profile_record(s, name=s)
        (out / f"scholar-{s}.json").write_text(json.dumps(rec, indent=2, ensure_ascii=False))
        emitted += 1
    for a in atts:
        rec = attestation_record(a.get("attestation_id") or a.get("proposal"))
        if rec:
            (out / f"attestation-{(a.get('attestation_id') or a.get('proposal'))}.json").write_text(
                json.dumps(rec, indent=2, ensure_ascii=False))
            emitted += 1
    return {"emitted": emitted, "out_dir": str(out)}


if __name__ == "__main__":
    import sys as _s
    verb = _s.argv[1] if len(_s.argv) > 1 else "all"
    if verb == "all":
        print(json.dumps(all_profiles(), indent=2, ensure_ascii=False))
    elif verb == "publish":
        print(json.dumps(publish_all(), indent=2, ensure_ascii=False))
    elif verb == "profile":
        print(json.dumps(profile_record(_s.argv[2]), indent=2, ensure_ascii=False))
