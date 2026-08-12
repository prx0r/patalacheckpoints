# L200 LIVE CANARY (2026-08-12) — experiment, non-blocking

Ran the REAL comparative MT/IA proposer (un-stubbed) on 5 IPVV-derived passages through the certified
validator. This is an EXPERIMENT ("does the live proposer survive the certified gate?"), not a blocker.

| fixture | phenomenon | status | validator | MT | IA | runtime |
|---|---|---|---|---|---|---|
| F1 | SUPPLIED | **GENERATION_FAILED** | blocked | 0 | 0 | 26s |
| F2 | REFERENT_SUPPLY | COMPLETE | ✅ | 3 | 1 | 48s |
| F4 | LEXICAL | COMPLETE | ✅ | 1 | 1 | 26s |
| F6 | IA-not-MT | COMPLETE | ✅ | 5 | 3 | 40s |
| F10 | zero-MT/IA | COMPLETE | ✅ | 0 | 0 | 8s |

## Findings
- **Fail-closed works live**: F1's model failure → GENERATION_FAILED → validator blocked it (never commits).
- **Empty-success works live**: F10 → COMPLETE with MT=0/IA=0 → commits (model successfully found nothing).
- The model finds real MT/IA on most passages (referential supply, lexical, connective).
- **Watch-item**: F6 (an IA-not-MT fixture) produced 5 MT — possible over-production/laundering that the
  structural validator cannot judge semantically. The typed-reference check (forbidden_mt) is what catches
  this at benchmark time; the live canary only reports validator pass.
- Runtime 8–48s/passage — hermes is slow but functional.

## Conclusion
The live proposer **survives the certified gate** (no GENERATION_FAILED commits, empty-success correct).
Model over/under-production of MT/IA is the real L200 quality question — to be measured by the typed
reference benchmark later, not by this canary. Do NOT scale L200 until that benchmark.
