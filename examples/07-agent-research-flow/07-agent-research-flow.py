#!/usr/bin/env python3
"""Example 07 — AI research agent flow.

Docs: docs/api/recipes/ai-research-agent.md
Usage: python3 07-agent-research-flow.py [base_url]
The canonical agent loop: resolve → get work → evidence bundle → terms → occurrences.
Checks the epistemic-invariant guarantees an agent must respect.
"""
import json, sys, urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3000"


def get(p):
    with urllib.request.urlopen(BASE + p, timeout=30) as r:
        return json.loads(r.read())


def post(p, body):
    req = urllib.request.Request(BASE + p, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def main():
    # 1. resolve identity
    r = post("/api/resolve/work", {"title": "Kubjikamatatantra"})
    assert r["status"] == "machine_proposed"
    work_id = r["candidates"][0]["work_id"]
    print("1. resolved →", work_id, "(machine_proposed)")

    # 2. get the work
    w = get(f"/api/works/{work_id}")["data"]
    assert w["id"] == work_id
    print("2. work:", w["title"], "| status:", w["translation_status"], "| verified:", w["verified"])

    # 3. evidence bundle for a passage
    pid = f"tantra:text:{work_id}:1.1"
    c = get(f"/api/context/passages/{pid}")
    assert c["passage"]["id"] == pid
    print("3. evidence bundle:", pid)

    # 4. accepted term senses
    senses = get("/api/terms/kula/senses")
    print("4. kula senses:", [s["label"] for s in senses["senses"]])

    # 5. occurrences (honest substring)
    occ = get(f"/api/terms/kula/occurrences?work_id={work_id}")
    print(f"5. kula surface occurrences in {work_id}: {occ['count']} (lemmatized={occ['lemmatized']})")

    # Epistemic guards the agent MUST respect:
    assert r["status"] == "machine_proposed", "must not report resolver as fact"
    assert occ["lemmatized"] is False, "must not claim lemma evidence from substring search"
    assert w["verified"] is False, "seed record must stay verified:false"
    print("  epistemic guards hold: proposal ≠ fact, substring ≠ lemma, seed ≠ audited")
    print("OK")


if __name__ == "__main__":
    main()
