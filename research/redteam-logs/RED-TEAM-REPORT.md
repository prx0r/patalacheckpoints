# RED-TEAM REPORT — pipeline + API (live adversarial testing)

*2026-08-15 · live red-team against the ingestion → assess → queue → openpatala → site pipeline.
Goal: BREAK it with adversarial input (shitty OCR, garbage Sanskrit, malformed files, variant identity,
API fuzz) and record real results. No help given — raw, honest findings. Raw logs in
`research/redteam-logs/`.*

---

## FINDING 1 (HIGH) — `_clean_signal` mislabels low-density garbage as CLEAN

**Vulnerability:** a 1120-byte file with only 3 IAST chars (pure English/OCR noise) is flagged `clean=True`.

**Repro:**
```python
# 1120 bytes of English/headers + 3 IAST chars
sig = source_ready._clean_signal("redteam_garbage")
# → clean=True, reason="looks like clean Sanskrit"
```

**Root cause** (`pipeline/source_ready.py:71-81`):
```python
if sanskrit_chars == 0: clean = False           # catches no-Sanskrit
elif sanskrit_chars < 50 and size > 2000: clean = False   # catches large low-density
elif size < 1000: clean = False                 # catches tiny
else: clean = True                               # ← GAP: 1000<=size<=2000 + low density falls here
```

**Impact:** garbage OCR → `CLEAN_ETEXT` → routed to TRANSLATE. Would waste translation work on noise.

**Fix:** add a density-ratio check (`sanskrit_chars / size < threshold → not clean`), independent of
absolute size.

---

## FINDING 2 (MEDIUM-HIGH) — format detection false-positive on low-density text

**Vulnerability:** the scheme detector calls anything with ANY IAST diacritic char `iast`, so the same
garbage (3 diacritics in 1120 bytes) → `format=RAW_SANSKRIT`.

**Root cause** (`pipeline/assess.py` `_scheme`): `if re.search(r"[āīūṛ...]", text): return "iast"` — no
density threshold.

**Impact:** compounds Finding 1 — garbage becomes `CLEAN_ETEXT/RAW_SANSKRIT`, fully routed to translate.

**Fix:** require a minimum IAST/Devanagari density before declaring RAW_SANSKRIT.

---

## FINDING 3 (LOW) — reconciliation under-promotes identical-title + empty-author

**Vulnerability:** `Śiva Sūtra` vs `Siva Sutra` (title_sim=1.0, both authors empty) → **POSSIBLE**, not
PROBABLE. The `author_sim ≥ 0.7` clause can't pass with empty authors even at title_sim=1.0.

**Impact:** safe direction (under-promotes, never over-merges) but noisy — certain matches stay POSSIBLE.

**Fix:** if `title_sim == 1.0` and both authors empty → PROBABLE.

---

## MINOR — API silently returns `{}` for an unknown `select` field

`/works?select=nonexistent_field` → `200, {}` (silent empty). A validation warning would be clearer.

---

## WHAT PASSED (handled correctly)

| Test | Result |
|---|---|
| **Malformed files** (empty, binary 5KB, UTF-8 BOM) | ✅ all handled (empty/binary rejected, BOM parsed) |
| **Reconciliation:** empty titles, garbage titles, same-title-diff-author trap | ✅ UNRESOLVED / UNRESOLVED / CONFLICT (never over-merges) |
| **API fuzz:** bad cursor, no-q search, huge per_page, nonexistent work, SQL-injection filter | ✅ all fail-closed (400/404/422, no 500, no crash) |
| **SQL injection** | ✅ inert — the read path has no SQL/DB (string-compared), safe by design |

---

## THE FIXED THINGS (for the next build pass)

1. **`_clean_signal`**: add density ratio (`sanskrit_chars/size`) — kills Finding 1.
2. **`_scheme`**: add density threshold before declaring `iast`/RAW_SANSKRIT — kills Finding 2.
3. **`reconcile`**: `title_sim==1.0` + empty authors → PROBABLE — kills Finding 3.
4. **`_select`**: warn/400 on an unknown select field (minor).

## STATUS (2026-08-15 — ALL FIXED + VERIFIED)

| Finding | Fix | Verified |
|---|---|---|
| **1** clean-signal gap | density-ratio 0.05 in `source_ready._clean_signal` (calibrated: real 0.13-0.15, garbage 0.003) | ✅ garbage → clean=False "low Sanskrit density ratio"; real files still pass |
| **2** format false-positive | density gate in `assess._detect_format` | ✅ garbage → UNKNOWN "likely OCR-mess"; real → RAW_SANSKRIT |
| **3** reconciliation POSSIBLE-vs-PROBABLE | identical title + empty authors → PROBABLE | ✅ Śiva Sūtra/Siva Sutra → PROBABLE |
| **minor** silent `{}` on bad select | `_select` surfaces `warnings[]` in provenance | ✅ /works?select=bad → warnings field |

Regression: translation_availability 11/11 PASS; all real files still CLEAN/RAW_SANSKRIT.

---

*This is the raw red-team result. 2 real vulnerabilities (clean-signal gap + format false-positive) and
1 minor. The malformed-file + identity + API robustness all passed. Nothing crashed the process; the
fail-closed design held.*
