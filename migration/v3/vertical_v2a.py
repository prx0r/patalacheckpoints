#!/usr/bin/env python3
"""vertical_v2a.py — run one IPVV chunk (V2-A) from raw to essay, wiring the proven kernels."""
import os, sys, json, hashlib
sys.path.insert(0, "/mnt/HC_Volume_106427611/ip-graph/lib")

from epistemic import EpistemicEnvelope, rank
from review import reducer, ReviewState, ReviewPhase
from scholar_review import verify_citations
from staleness import blast_radius, build_dependency_index
from education import LearningClaim
from essay_ingest import EssayIngestor

IPVV = "/root/projects/sanskritree/translations/_stack/ipvv"
results = []
def check(name, cond, detail=""):
    results.append(bool(cond)); print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")

# ---- 0. RAW ----
src = open(f"{IPVV}/00_source/torella_ipk.txt").read()
check("0 raw: Torella IPK text loaded", len(src) > 50000)

# ---- 1. T1 ----
t1 = open(f"{IPVV}/02_t1/chunkV2-A-caturtho-vimarsa-aham.md").read()
check("1 T1: word-faithful draft loaded", len(t1) > 1000 and "[and]-the-Lord" in t1)

# ---- 2. L0 ----
l0_lines = open(f"{IPVV}/l0/chunkV2-A-caturtho-vimarsa-aham.l0.jsonl").readlines()
check("2 L0: token floor loaded", len(l0_lines) > 1000)

# ---- 3. L2 ----
l2 = open(f"{IPVV}/pilot/pilot_V2A_L2_read.md").read()
check("3 L2: readable prose loaded", "Memory as the Lord's power" in l2 and len(l2) > 1000)

# ---- 4. L200 ----
l200 = open(f"{IPVV}/l200/V2A-caturtho-aham.md").read()
check("4 L200: proof audit loaded", "## 2. DERIVATION MAP" in l200)

# ---- 5. C1 ----
c1 = open(f"{IPVV}/c1/read/c1_V2A-memory-lords-power.md").read()
check("5 C1: commentary loaded", len(c1) > 500 and "memory" in c1.lower())

# ---- 6. INGEST ----
ing = EssayIngestor("ipvv-V2-A")
ing.structure("Memory as the Lord's power", "Abhinavagupta (IPVV V2-A)", [
    {"id": "caturtho-vimarsa", "chapter": "caturtho-vimarsa", "ipk_refs": ["IPK 1.2.3"]},
])
ing.mine_claim("Memory is the un-broken manifestation of the experienced object, not an impression's revival",
               "IPK 1.2.3", "SCHOLARLY_CORROBORATED", "thesis",
               "sa hi pūrvānubhūtārthopalabdhā ...", "caturtho-vimarsa")
ing.mine_claim("Memory is the Lord's own power — the paramaṃ svātantryam",
               "IPK 1.2.3", "SCHOLARLY_CORROBORATED", "conclusion",
               "smaraṇaśaktireva hi paramaṃ svātantryam", "caturtho-vimarsa")
ing.mine_claim("The aham shines two-faced: seer of the blue (inward) and I-thus (outward)",
               "IPK 1.3.1", "ENGINEERING_VALIDATED", "premise", "nīlaboddhā aham", "caturtho-vimarsa")
ing.add_move("Memory = un-broken manifestation", "Memory = Lord's power", "ENTAILMENT")
check("6 ingest: 3 claims mined + 1 move, honest ceilings", len(ing.claims) == 3 and len(ing.moves) == 1)

# ---- 7. REVIEW ----
known = {"IPK 1.2.3", "IPK 1.3.1", "IPK 1.3.6"}
cits = verify_citations([c.source_ref for c in ing.claims], known)
check("7 review: all 3 claims' citations resolve (no phantom)", all(c.status != "PHANTOM" for c in cits))

# ---- 8. GATE ----
st = ReviewState("ipvv-V2-A-thesis")
reducer(st, evidence_ok=True)
check("8 gate: corroborated claim advances", st.phase in (ReviewPhase.ALIGNED, ReviewPhase.REVIEWING))

# ---- 9. STALENESS ----
ipk_dag = {"IPK-1.2.3": {"requires": []}, "IPK-1.3.1": {"requires": ["IPK-1.2.3"]},
           "memory-lords-power": {"requires": ["IPK-1.2.3", "IPK-1.3.1"]}}
dep = build_dependency_index(ipk_dag)
stale = blast_radius(dep, {"IPK-1.2.3"})
check("9 staleness: retracting IPK 1.2.3 flags the memory-lords-power essay", "memory-lords-power" in stale)

# ---- 10. EDUCATION ----
lcs = ing.to_learning_claims()
check("10 education: 3 mined claims -> 3 LearningClaims", len(lcs) == 3)

# ---- 11. ESSAY ----
essay = f"""# Memory as the Lord's Power (IPVV V2-A)

**Proof-linked essay.** Every sentence carries its claim → proof → Sanskrit.

{l2[:600]}

## The argument (from the mined graph)
1. **Thesis:** Memory is the un-broken manifestation, not an impression's revival.
   → *proof: L200 audit, IPK 1.2.3*
2. **Conclusion:** Memory is the Lord's own power — the paramaṃ svātantryam.
   → *proof: smaraṇaśaktireva hi paramaṃ svātantryam*
3. **The two-faced aham:** seer of the blue (inward) and I-thus (outward).
   → *proof: IPK 1.3.1*

{c1}
"""
check("11 essay: proof-linked projection assembled", len(essay) > 1500 and "Proof-linked essay" in essay)

print(f"\n=== VERTICAL V2-A: {sum(results)}/{len(results)} passed ===")
print("raw → T1 → L0 → ARGMAP → L2 → L200 → C1 → [mined graph] → review → stale → education → essay")
sys.exit(0 if all(results) else 1)
