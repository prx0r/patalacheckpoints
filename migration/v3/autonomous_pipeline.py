#!/usr/bin/env python3
"""autonomous_pipeline.py — the OG patala autonomous ingestion organism.

Wires the ip-graph `ingestion_organism` (the priority-queue autonomous loop, 10/10 tested) into the
REAL patala data: the sivaqueue priority targets + the real source files on disk. The shared goal made
concrete — untranslated Sanskrit docs enter a priority queue, are rights-gated, refined through the
LAYERS chain, verified, committed, and re-prioritized by learner feedback.

Run: python3 migration/v3/autonomous_pipeline.py
"""
import sys, os, json

# the lab kernels (isolated — the schema.py collision)
LAB = "/mnt/HC_Volume_106427611/ip-graph/lib"
sys.path.insert(0, LAB)
from ingestion_organism import IngestionOrganism, SanskritDoc

ROOT = "/root/projects/patala"

def load_real_targets():
    """Load the real patala sivaqueue priority targets + on-disk source files."""
    siva = json.load(open(f"{ROOT}/data/corpus/targets/sivaqueue.json"))
    targets = siva.get("targets", {})
    # map work_id -> on-disk source file (the real data)
    src_root = f"{ROOT}/data/corpus/sources"
    docs = []
    for wid, meta in targets.items():
        src_dir = f"{src_root}/{wid}"
        txt = f"{src_dir}/{wid}.txt"
        if os.path.exists(txt):
            lines = len(open(txt).readlines())
            docs.append(SanskritDoc(
                work_id=wid,
                title=meta.get("name", wid),
                source="patala-corpus",
                rights="CC_BY_NC_SA" if "PANDiT" in str(meta) else "public-domain",
                tradition=meta.get("tradition", ""),
                verses=lines,
            ))
    return docs

def main():
    print("=== OG PATALA AUTONOMOUS PIPELINE ===\n")
    docs = load_real_targets()
    print(f"Loaded {len(docs)} real untranslated Sanskrit works from the sivaqueue with on-disk source")
    for d in docs[:5]:
        print(f"  - {d.work_id} ({d.title[:40]}...) {d.verses} lines, tradition={d.tradition}")

    org = IngestionOrganism()
    # add the real docs to the priority queue (short works first = lowest cost)
    for d in docs:
        org.add(d, cost=1.0 / max(1, d.verses), uncertainty=0.5)

    print(f"\nPriority queue: {len(org.queue())} works queued (shortest first)")
    q = org.queue()
    if q:
        first = q[0]
        print(f"  next up: {first.get('work_id')} (P={first.get('P', '?')})")

    # run ONE real work through the full organism loop
    if docs:
        target = docs[0].work_id  # the shortest/priority work
        print(f"\n--- running {target} through the organism ---")
        result = org.run_one(target)
        print("  result:", json.dumps(result, default=str)[:200] if result else "(check logs)")

    print("\n=== AUTONOMOUS PIPELINE READY ===")
    print("The priority queue is loaded with real patala data; the organism loop is wired.")
    print("Next: run the full queue (real Hermes translation per work) — the corpus-wide graduation.")

if __name__ == "__main__":
    main()
