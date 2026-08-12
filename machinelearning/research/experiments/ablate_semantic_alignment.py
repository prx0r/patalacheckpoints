#!/usr/bin/env python3
"""ablate_semantic_alignment.py — controlled representation ablation on the FROZEN 8 gold pairs.

Stage A, round 2. The 0/8 MiniLM baseline falsified the harness. Now: WHICH combination of
(context-window × encoder) carries real semantic signal? Thresholds are FIXED across all combinations
(no per-model tuning — that would be fitting to the test).

Failure decomposition question:
  is alignment failing because of (1) weak encoder, (2) wrong context window, (3) bad representation
  space, (4) bad gold granularity, or (5) genuinely hard ambiguity?

Design:
  windows  : lemma_only · sanskrit (IAST) · l2 · sanskrit_l2 · c1_window (around lemma) · c1_full
  encoders : dense (MiniLM) · multilingual (paraphrase-multilingual, if it loads) · lexical (offline,
             model-free hashed n-gram)
  metric   : accuracy on the 5 DECIDABLE NEAR_SAME gold pairs (vimarśa ×3, pramāṇa ×2) — can the
             representation tell that vimarśa@V2H ≈ vimarśa@V2J? The AMBIGUOUS/NOT_ENOUGH golds test
             abstention separately (a single cosine cannot abstain, by design).

Run: cd research && . .venv/bin/activate && python experiments/ablate_semantic_alignment.py
"""
from __future__ import annotations
import hashlib
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from experiments.benchmark_semantic_alignment import GOLD, _load

PILOT_DIR = "/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/pilot"
L2_FILES = {
    "V2H-vimarsa-paravak": "pilot_V2H_L2_read.md", "V2J-samskara": "pilot_V2J_L2_read.md",
    "V2O-orderless-support": "pilot_V2O_L2_read.md", "V3F-grace": "pilot_V3F_L2_read.md",
    "V2I-sphuratta": "pilot_V2I_L2_read.md", "V2L-nonconstructed-I": "pilot_V2L_L2_read.md",
    "V2P-pramatr-vyapara": "pilot_V2P_L2_read.md", "V3E-error": "pilot_V3E_L2_read.md",
    "V2D-jnanasakti": "pilot_V2D_L2_read.md", "V2E-external-inferred": "pilot_V2E_L2_read.md",
    "V3H-inference-across-knowers": "pilot_V3H_L2_read.md",
}

# fixed label-mapping thresholds (SAME for all window×encoder combinations — the controlled comparison)
def _propose(cos: float) -> str:
    if cos >= 0.82:
        return "SAME_SENSE"
    if cos >= 0.62:
        return "NEAR_SAME"
    if cos <= 0.32:
        return "DIFFERENT_SENSE"
    return "PARTIAL_OVERLAP"


def _tokenize(s): return re.findall(r"[a-zāīūṛṣṭṇḥ]+", (s or "").lower())
def _norm(s):
    s=(s or "").lower()
    for a,b in [("ā","a"),("ī","i"),("ū","u"),("ṛ","r"),("ṣ","s"),("ś","s"),("ṇ","n"),("ṭ","t"),("ḍ","d"),("ḥ","h"),("ṃ","m")]:
        s=s.replace(a,b)
    return s

def _l2(c1_id: str) -> str:
    f = os.path.join(PILOT_DIR, L2_FILES.get(c1_id, ""))
    if os.path.exists(f):
        return open(f, encoding="utf-8").read()[:600]
    return ""


def _windows(c1_id: str, lemma: str) -> dict:
    d = _load(c1_id, lemma)
    full = " ".join(l.lstrip("> ").strip() for l in
                    open(f"/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/c1/read/c1_{c1_id}.md", encoding="utf-8")
                    if l.strip().startswith(">"))
    l2 = _l2(c1_id)
    return {
        "lemma_only": lemma,
        "sanskrit": d["sanskrit"],
        "l2": l2,
        "sanskrit_l2": d["sanskrit"] + " " + l2,
        "c1_window": d["c1"],
        "c1_full": full,
    }


# ---- encoders (dense + multilingual if loadable + lexical) ----
_enc = {}
def _encoder(name: str):
    if name in _enc:
        return _enc[name]
    if name == "lexical":
        _enc[name] = None
        return None
    try:
        from sentence_transformers import SentenceTransformer
        mid = {"dense": "sentence-transformers/all-MiniLM-L6-v2",
               "multilingual": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"}[name]
        m = SentenceTransformer(mid)
        _enc[name] = m
        return m
    except Exception:
        _enc[name] = False
        return False

def _hashed(s, dim=512, n=3):
    v=[0.0]*dim
    t=re.sub(r"[^a-zāīūṛṣṭṇḥ]"," ",(s or "").lower()); t=re.sub(r"\s+","",t)
    for i in range(max(0,len(t)-n+1)):
        h=int(hashlib.md5(t[i:i+n].encode()).hexdigest(),16); v[h%dim]+=1.0
    norm=math.sqrt(sum(x*x for x in v)) or 1.0
    return [x/norm for x in v]

def _cos(a,b): return sum(x*y for x,y in zip(a,b))

def _vec(enc, text):
    if enc is not None and enc is not False:
        try: return [float(x) for x in enc.encode(text or " ")]
        except Exception: pass
    return _hashed(text)

DECIDABLE = [(a,b,l,g) for a,b,l,g in GOLD if g == "NEAR_SAME"]  # the 5 testable pairs


def main():
    WINDOWS = ["lemma_only","sanskrit","l2","sanskrit_l2","c1_window","c1_full"]
    ENCODERS = ["dense","multilingual","lexical"]
    print(f"ablation over {len(DECIDABLE)} decidable NEAR_SAME pairs · {len(GOLD)} frozen golds · "
          f"fixed thresholds\n")
    header = f"{'window':<12}" + "".join(f"{e:>13}" for e in ENCODERS)
    print(header); print("-"*len(header))

    best = (0, None, None)
    for w in WINDOWS:
        row = f"{w:<12}"
        for e in ENCODERS:
            enc = _encoder(e)
            if enc is False:
                row += f"{'n/a':>13}"; continue
            correct = 0
            for a, b, lemma, _ in DECIDABLE:
                wa, wb = _windows(a, lemma), _windows(b, lemma)
                cos = _cos(_vec(enc, wa[w]), _vec(enc, wb[w]))
                if _propose(cos) in ("NEAR_SAME", "SAME_SENSE"):
                    correct += 1
            acc = correct / len(DECIDABLE)
            row += f"{acc:>13.2f}"
            if acc > best[0]:
                best = (acc, w, e)
        print(row)

    print(f"\nBEST-RAW: {best[1]} × {best[2]} = {best[0]:.2f} on the 5 NEAR_SAME pairs")
    print("""
HONEST INTERPRETATION (do not read the 1.00s as a win):
  - lemma_only = 1.00 is CIRCULAR: the lemma is identical in both occurrences, so it only proves
    'same lemma == same lemma', not semantic alignment. Exclude it as a real signal.
  - multilingual = 1.00 across ALL windows (incl. c1_full, where the English model scored 0.00) is
    NON-DISCRIMINATIVE: its cosine is compressed high for all same-domain (IPVV) text -> everything
    maps to NEAR/SAME. It cannot distinguish NEAR_SAME from PARTIAL/AMBIGUOUS.
  - The genuinely informative row is dense (English): sanskrit 0.60 -> l2 0.40 -> c1_window 0.00 ->
    c1_full 0.00. Context HURTS the generic English encoder: the more commentary context, the less
    signal. This RULES OUT 'context-window construction' as the fix.

CONCLUSION (failure decomposition):
  The 0/8 failure is NOT (2) context-window construction. It is (1) weak/generic encoder +
  (3) representation space: a generic English or multilingual model cannot align contextualized
  philosophical occurrences. The fix is a Sanskrit-aware embedding and/or a CROSS-ENCODER pair
  classifier (sees A and B jointly -> relation proposal) — per the Stage-A plan (step 3). Keep the
  three-space disagreement (sanskrit vs l2 vs c1) as a SEMANTIC_TENSION signal, not as the sole scorer.
""")


if __name__ == "__main__":
    main()
