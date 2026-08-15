# PĀṬALA TESTING & VALIDATION — the consolidated reference

*2026-08-15 · the single organized entry point to ALL testing, red-team, and validation work on the
pipeline. Everything is logged, reproducible, and honest (the ONE RULE: nothing is real without a gate).
This is the master index — every artifact below is linked + summarized.*

---

## 1. THE TEST HIERARCHY (how it's organized)

```
testing/
├── TEST-INDEX.md              ← this file (the master map)
├── unit/                       ← reproducible gates per component
│   ├── translation_availability  11/11 PASS
│   ├── translation_locator       10/10 PASS (live multi-API)
│   ├── atlas-api                 ALL PASS (OpenAlex grammar)
│   └── assess                    16/16 PASS (decision engine)
├── integration/               ← the full E2E pipeline trace
│   └── E2E-INGEST-TO-SITE.md     ingest→harvest→assess→queue→openpatala→site
└── redteam/                   ← adversarial (tried to break it)
    ├── ROUND1/                  clean-signal gap + format false-positive + reconciliation
    ├── ROUND2/                  garbage-Devanagari + real OCR + mojibake + noise-dilution
    └── index
```

---

## 2. RED-TEAM RESULTS (the security posture)

### Round 1 (adversarial input: garbage, malformed, identity, API fuzz)
| # | Finding | Severity | Fixed |
|---|---|---|---|
| 1 | `_clean_signal` mislabels low-density IAST garbage as CLEAN (size 1000-2000 gap) | HIGH | ✅ density-ratio (0.05, calibrated) |
| 2 | `_scheme`/format calls garbage RAW_SANSKRIT (any diacritic = iast) | MED-HIGH | ✅ density gate |
| 3 | identical-title + empty-author → POSSIBLE not PROBABLE | LOW | ✅ title_sim==1.0 + no authors → PROBABLE |
| minor | API silently `{}` on unknown select field | — | ✅ `warnings[]` in provenance |

**Held (passed):** malformed files (empty/binary/BOM), identity traps (CONFLICT never over-merged),
API fuzz (400/404/422, no 500/crash), SQL-injection inert (no DB in read path).

### Round 2 (sneaky + real-world)
| Finding | Result |
|---|---|
| **garbage-Devanagari** (random deva chars, high density, no words) | 🔴 vuln → **FIXED** (word-validity signal) |
| Real messy OCR (Gautamiya 515KB) | ✅ correctly accepted (real words, usable) |
| mojibake attempt | ✅ my test was flawed (round-tripped), not a vuln |
| noise-diluted (77% ASCII + 23% deva) | 🟡 passes clean, but identity gate → scholar-queue |

**KEY INSIGHT — defense in depth:** the clean/density check is imperfect, but the **identity gate is the
real protector** — garbage is always `UNRESOLVED` → SCHOLAR_QUEUE, never auto-routed to TRANSLATE
(which requires EXACT/PROBABLE identity). **The translation lane is safe.**

---

## 3. THE E2E PIPELINE (verified live, full trace)

Traced `kiranatantra` end-to-end: **ingest (784+499 SOURCE) → harvest (318k verses) → assess
(CLEAN_ETEXT→TRANSLATE) → queue (81 works, pos 9) → openpatala (partial EN/IT) → site (215 pages)**.
Full log: `integration/E2E-INGEST-TO-SITE.md`.

---

## 4. THE API (final surface, OpenAlex grammar)

| Endpoint | What | Grammar |
|---|---|---|
| `/health` | backend + counts | — |
| `/works` | list works | filter/search/sort/select/cursor |
| `/works/{id}` | one work | select |
| `/works/{id}/translations` | translation-availability (the product) | ETag→304 |
| `/translations` | translation list | search/filter/cursor/ETag |
| `/editions` | editions | filter |
| `/search` | search alias | — |
| `/openpatala` + `/{layer}` | live registry | select/ETag |
| `/resolve` | identity crosswalk | OpenAlex/Crossref/Unpaywall |

Full spec: `api/API-REFERENCE.md`.

---

## 5. THE RESEARCH (the translation-availability product)

Compiled in `research/`: the repo survey (REPORT-15), the adapter/crawl roadmap (REPORT-16), the
translation-availability thesis, the Postgres migration path, the API polite-usage reference, and the
38-source register.

---

## 6. THE GATES (run to verify nothing regressed)

```bash
cd /root/patalacheckpoints
PYTHONPATH=pipeline python3 pipeline/translation_availability_test.py   # 11/11
PYTHONPATH=python   python3 pipeline/translation_locator_test.py        # 10/10
PYTHONPATH=pipeline python3 pipeline/assess_test.py                     # 16/16
(cd python && /root/patalacheckpoints/.venv-atlas/bin/python3 patala_core/atlas/test_api.py)  # ALL PASS
```

---

*This is the master index. Every artifact below it is reproducible + logged. The pipeline is tested,
red-teamed twice, and hardened; the API is documented and live.*
