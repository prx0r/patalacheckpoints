# RED-TEAM REPORT ROUND 2 — sneaky / real-world (live)

*2026-08-15 · second adversarial pass. Actively tried to break the pipeline with REAL messy OCR from
archive.org + sneaky edge cases (mojibake, noise-dilution, garbage-Devanagari). Full logs in
`research/redteam-logs/round2-real-ocr.log`.*

---

## What I did
1. **Pulled real messy OCR** from archive.org (Gautamiya Tantra, 515KB scanned Devanagari OCR — genuine
   mess: `श @&क्टडपणो`, `2523 795`, half-recognized chars).
2. **Tried to break with:** GBK/latin-1 mojibake, noise-diluted Devanagari (77% ASCII noise), pure
   garbage-Devanagari (random Devanagari-range chars), and the full assess on all of them.

---

## FINDINGS

### Finding A — REAL OCR is correctly accepted (NOT a vuln, good news)
The real Gautamiya OCR (515KB, density 0.84, 6616 danda markers) → `clean=True, RAW_SANSKRIT`. Analysis:
**it hits 17/17 valid Sanskrit words** (न, च, देव, सर्व, शिव...) + real verse markers. It's *genuinely
usable* Sanskrit (messy margins, real body). **The pipeline correctly accepts it.** ✅

### Finding B — mojibake test was FLAWED (invalid test, not a vuln)
My latin-1→utf-8 round-trip recovered the original Devanagari (160811 chars). The "mojibake" wasn't
real mojibake. No vuln. ✅ (Honest: my test was wrong, not the pipeline.)

### Finding C — noise-diluted text passes clean (LOW-MED, mitigated)
A 72KB file (77% ASCII page noise + 23% Devanagari, density 0.231) → `clean=True`. The density check
catches *pure* garbage but not *noise-diluted* text. **Mitigation: the assess identity gate routes it to
SCHOLAR_QUEUE** (identity=UNRESOLVED → never auto-route to translate).

### Finding D — garbage-Devanagari (HIGH, now FIXED)
Random Devanagari-range chars (density 0.85, no real words) → `clean=True`. The density check can't
distinguish garbage-Devanagari from real. **This was the sneakiest break.**

---

## THE KEY INSIGHT — DEFENSE IN DEPTH (the pipeline is actually safe)

Even where the clean-check is imperfect (Findings C/D), the **identity gate is the real protector**:
- Every adversarial input assessed as `identity=UNRESOLVED` → routed to **SCHOLAR_QUEUE** (manual
  review), NEVER auto-routed to TRANSLATE.
- **The route to TRANSLATE requires `identity ∈ {EXACT, PROBABLE}`** — which requires a real atlas
  match. Garbage can't reach translation without a genuine identity.
- **No crash on any input** (fail-closed held).

So: the clean-check weakness is contained by the identity gate. This is good architecture.

---

## THE FIX (round 2, committed)
**`_clean_signal` now has a word-validity signal** (multi-char Sanskrit words: नाम, शिव, देव, सर्व,
यथा, भवति...). If a Devanagari file has high density but ZERO common words → `clean=False` (OCR-mess).

**Verified:**
| Input | Before | After |
|---|---|---|
| Garbage-Devanagari (random) | clean=True (vuln) | **clean=False** ✅ |
| Real messy OCR (Gautamiya) | clean=True | clean=True (correct) ✅ |
| Real IAST files | clean=True | clean=True (no regression) ✅ |

---

## REMAINING GAP (documented, LOW priority)
Noise-DILUTED real text (Finding C) still passes clean — but it's harmless because the identity gate
sends it to scholar-queue anyway. A full fix would require a word-coverage ratio, which is heavier.
Deferred; the defense-in-depth already protects the translation lane.

---

*Round 2 verdict: 1 real vuln found (garbage-Devanagari) + 1 documented low-priority gap (noise-dilution).
The pipeline did NOT crash on anything; the identity gate held the translation lane safe. Fix committed.*
