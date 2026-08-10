#!/usr/bin/env python3
"""Run C1 on kramasadbhāva 1.8 via Hermes — LEAN, focused prompt (fits the timeout).

C1 is the first external-evidence challenge to the machine adjudication. The single
giant-JSON call timed out, so we do the two-artifact approach the reviewer advised:
  CALL 1: write the C1 commentary as prose (focused, small prompt).
  CALL 2: extract the structured metadata (challenge/evidence/proposals) separately.

This call is CALL 1 — produce the commentary prose + a clear challenge verdict on
nirānande (is R2's CONSTRAINED too strong? PREFERRED/OPEN?).
"""
import sys, os, json
sys.path.insert(0, "/root/projects/patala")
import pipeline.model as model_mod

# A LEAN, focused C1 prompt — just the crux + T3 + the nirānanda direction.
PROMPT = """You are producing C1, a capstone scholarly commentary for one verse of the Kramasadbhāva (Krama tradition).

VERSE (1.8): ooṃ namaste devadeveśi mahākāli namo'stu te | namo'stu paramānande nirānande namo'stu te
CURRENT T3: "Oṃ — homage to you, O mistress of the god of gods; Mahākālī, homage be to you. Homage be to you, O supreme bliss; to you, O bliss-less one, homage be to you."

CONTEXT: This is a vocative-chain stuti (homage-hymn) to the goddess Mahākālī. It opens the Kramasadbhāva's maṅgala. The R1 found two cruxes: devadeveśi (compound parse: 'queen of the gods' vs 'mistress of the god of gods') and nirānande (privative 'O bliss-less one' vs a technical transcendental sense).

THE KEY QUESTION — nirānande:
- R2 classified nirānande as CONSTRAINED = "O bliss-less one" (plain privative nir-+ānanda).
- BUT external evidence suggests it may be a TECHNICAL Krama/Kubjikā term:
  * the Mahānaya online edition of Kramasadbhāva 1.8 renders nirānande as "the Bliss of Stillness", not merely "bliss-less"
  * Dyczkowski-related Kubjikā material connects nirānanda with nirācārānanda, "bliss of stillness"
  * other tantric sources use nirānanda for a transcendental/void-related state of bliss beyond the bliss/absence opposition
- So: is "CONSTRAINED" (source forces the literal privative) too strong? Should it be PREFERRED or OPEN given the historical technical usage?

WRITE the C1 commentary (200-450 words), structured as:
A. Core sense — what the verse is doing (the vocative-chain stuti).
B. devadeveśi — most likely meaning and why.
C. nirānande — the paradox: what the grammar alone permits vs what historical tantric usage suggests. State clearly whether R2's CONSTRAINED was overconfident.
D. Larger significance — what this opening tells us about the Krama maṅgala.

Be concise, source-aware, explicit about uncertainty. Do NOT pad. Then, on a new line starting with CHALLENGE:, state in one sentence whether T3 should be revised on nirānande (yes/no) and to what reading.
"""

def main():
    print("=== launching lean C1 via hermes ===", flush=True)
    out = model_mod._hermes_call(PROMPT, model="deepseek-v4-flash")
    print("=== C1 OUTPUT ===", flush=True)
    print(out, flush=True)
    # save it
    os.makedirs("/root/projects/sanskritree/translations/_stack/kramasadbhava/c1", exist_ok=True)
    with open("/root/projects/sanskritree/translations/_stack/kramasadbhava/c1/1.8.md", "w", encoding="utf-8") as f:
        f.write("# C1 — Kramasadbhāva 1.8\n\n" + out)
    print("\n=== saved to c1/1.8.md ===", flush=True)

if __name__ == "__main__":
    main()
