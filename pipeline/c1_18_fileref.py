#!/usr/bin/env python3
"""Run C1 on kramasadbhāva 1.8 via Hermes — file-referencing, not prompt-dumping.

Hermes has full access to the codebase. So instead of inlining the whole stack into
the prompt, we point it at the persisted files and let it read them. The prompt is
small; hermes does the reading, research, and writing.
"""
import os, sys, json
sys.path.insert(0, "/root/projects/patala")
import pipeline.model as model_mod

REC = "/root/projects/sanskritree/translations/_stack/kramasadbhava/passages/1.8.json"
SKILL = "/root/projects/patala/skills/write-commentary/SKILL.md"
DOSSIERS = "/root/projects/sanskritree/saivamap/dossiers/"

PROMPT = f"""You are producing C1, a capstone scholarly commentary, for Kramasadbhāva 1.8
(the Krama tradition). Follow the write-commentary skill and READ THE FILES on disk —
do not rely on model memory.

READ THESE FIRST:
1. The persisted translation stack: {REC}
   (JSON: stages T1/R1/T2/R2/T3 — read the actual R1 cruxes, R2 decisions, T3 resolved)
2. The write-commentary skill: {SKILL}
3. The lemma dossiers (for nirānanda / ānanda / related technical terms): {DOSSIERS}
4. If useful, the canonical reference map and corpus: search the corpus for
   nirānanda / paramānanda / Mahākālī invocations / Krama maṅgalas.

THE KEY SCHOLARLY QUESTION — nirānande:
- R2 classified nirānande as CONSTRAINED = "O bliss-less one" (plain privative nir-+ānanda).
- But external evidence suggests it may be a TECHNICAL Krama/Kubjikā term:
  * the Mahānaya online edition of Kramasadbhāva 1.8 renders nirānande as "the Bliss of
    Stillness", not merely "bliss-less"
  * Dyczkowski-related Kubjikā material connects nirānanda with nirācārānanda,
    "bliss of stillness"
  * other tantric sources use nirānanda for a transcendental/void-related state of bliss
    beyond the bliss/absence opposition
- Is "CONSTRAINED" (source forces the literal privative) too strong? Should it be
  PREFERRED or OPEN given the historical technical usage? Use the local dossiers/corpus
  to check what nirānanda means in this tradition.

WRITE the C1 commentary (200-450 words), structured as:
A. Core sense — what the verse is doing (the vocative-chain stuti / maṅgala opening).
B. devadeveśi — most likely meaning and why.
C. nirānande — the paradox: what the grammar alone permits vs what historical tantric
   usage suggests. State clearly whether R2's CONSTRAINED was overconfident.
D. Larger significance — what this opening tells us about the Krama maṅgala.

Be concise, source-aware, explicit about uncertainty. Reference stable IDs where you can.
Then, on a final line starting with CHALLENGE:, state in one sentence whether T3 should
be revised on nirānande (yes/no) and to what reading. Write the full commentary to
standard output.
"""

def main():
    print("=== launching file-referencing C1 via hermes ===", flush=True)
    out = model_mod._hermes_call(PROMPT, model="deepseek-v4-flash")
    print("=== C1 OUTPUT ===", flush=True)
    print(out, flush=True)
    os.makedirs("/root/projects/sanskritree/translations/_stack/kramasadbhava/c1", exist_ok=True)
    with open("/root/projects/sanskritree/translations/_stack/kramasadbhava/c1/1.8.md", "w", encoding="utf-8") as f:
        f.write("# C1 — Kramasadbhāva 1.8\n\n" + out)
    print("\n=== saved to c1/1.8.md ===", flush=True)

if __name__ == "__main__":
    main()
