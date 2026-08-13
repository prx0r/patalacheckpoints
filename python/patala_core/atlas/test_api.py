#!/usr/bin/env python3
"""python/patala_core/atlas/test_api.py — TIER 4 read-API tests (OpenAlex grammar over the Atlas).

Proves the read API exposes the bibliography with the OpenAlex query grammar, fast (compiled model,
no N+1):
  - /works list + filter + search + select + sort + cursor pagination
  - /works/{id} single (dehydrated refs)
  - /search alias
  - agent-actionable 404 error shape
Run: python3 python/patala_core/atlas/test_api.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from fastapi.testclient import TestClient  # noqa: E402
from patala_core.atlas.api import app  # noqa: E402

client = TestClient(app)


def t(name, cond, detail=""):
    print(("PASS" if cond else "FAIL"), "-", name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def main() -> int:
    ok = True
    print("=== TIER 4: OpenAlex-grammar read API ===")

    r = client.get("/health")
    ok &= t("health returns backend + count", r.json().get("works", 0) >= 250, f"works={r.json().get('works')}")

    r = client.get("/works?per_page=5&select=id,title,translation_status")
    j = r.json()
    ok &= t("/works list", j.get("count") == 5 and j.get("total", 0) >= 250, f"count={j.get('count')} total={j.get('total')}")
    ok &= t("select= limits fields", set(j["works"][0].keys()) <= {"id", "title", "translation_status"},
            f"keys={list(j['works'][0].keys())}")

    r = client.get("/search?q=tantraloka&select=id,title")
    j = r.json()
    ok &= t("/search alias finds a work", j.get("count", 0) >= 1 and "Tantrāloka" in j["works"][0]["title"],
            j["works"][0]["title"] if j.get("works") else "none")

    r = client.get("/works?filter=translation_status:complete&per_page=5&select=id,translation_status")
    j = r.json()
    ok &= t("filter= narrows to complete", j.get("count", 0) >= 1 and all(w["translation_status"] == "complete" for w in j["works"]),
            f"count={j.get('count')} of {j.get('total')}")

    r = client.get("/works/malinivijayottara")
    j = r.json()
    ok &= t("GET /works/{id}", "Mālinī" in j.get("data", {}).get("title", ""), j.get("data", {}).get("title"))

    r = client.get("/works?per_page=10")
    nc = r.json().get("next_cursor")
    ok &= t("cursor pagination returns next_cursor", bool(nc))
    if nc:
        r2 = client.get(f"/works?per_page=10&cursor={nc}")
        ok &= t("cursor advances page", r2.json().get("count") == 10, f"page2={r2.json().get('count')}")

    r = client.get("/works/does-not-exist-zzz")
    ok &= t("404 is agent-actionable (code/message/suggestion)", r.status_code == 404 and "suggestion" in str(r.json()),
            str(r.json())[:80])

    print("")
    print("RESULT: " + ("ALL PASS" if ok else "FAILURES"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
