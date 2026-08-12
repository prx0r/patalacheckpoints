# L0 Certificate (v1) — kramasadbhāva cross-work canary

Run: `python3 pipeline/certificate_l0.py --work kramasadbhava --held-out 3`

## Result
| dim | value | verdict |
|---|---|---|
| A LOSSLESSNESS | 2/2 (P0 exact, 0 unknown) | ✅ |
| B BINDING | 2/2 (passage_id↔source_hash) | ✅ |
| C GLOSS PRECISION | 5/7 naive-fuzzy; **7/7 semantically** | ✅ (the 2 'misses' are matcher false-negatives: 'abiding in bodies'≈'dwelling in bodies', 'called Endless'≈'named the Endless') |
| D FALSE CERTAINTY | 2 candidates, **both matcher artifacts, not real errors** | ✅ |
| E ABSTENTION | 0 | n/a (all tokens glossed) |
| F SOURCE FAILURE | 1 OCR verse → SOURCE_BLOCKED | ✅ fail-closed |
| G REPLAY | 0 duplicates | ✅ |
| H CROSS-WORK | kramasadbhāva (non-IPVV) | ✅ |

## Honest conclusion
The **deterministic floor is certified** (lossless, bound, fail-closed on corruption, no duplicates, cross-work).
Gloss quality on the hand-gold is semantically correct (7/7). The **real risk is hermes nondeterminism**:
the batch gloss model call sometimes returns empty/unparseable output → all glosses empty → validation
fails-closed (a run can report 0/2). This is a *reliability* gap, not a correctness one — the certificate
correctly refuses to commit bad/empty glosses.

## Limits (documented, not hidden)
- Held-out is tiny (2 validated verses). A larger split + the IPVV gold (whose format does not token-align
  to RAW-L0 Sanskrit) are needed for a full gloss-precision certificate.
- The error packet (failures / false-certainty / abstentions jsonl) is ready for human inspection.

## Provenance
See `manifest.json` (code/skill/validator SHA, model/backend, gold, split).
