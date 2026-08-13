# L0 DECOMPOSITION — definitive classification (A1-P12)

*786 objects, 402 roundtrip-pass, 384 fail*

## Failure class tally (objects with at least one instance)

| class | objects | example |
|---|---|---|
| TOKEN_LOSS | 361 | [('brahmayamala:v2', ['kāraṇam']), ('brahmayamala:v4', ['brahmāṇi']), ('brahmayamala:v5', ['indrāṇi'])] |
| CANONICALIZATION | 40 | [('brahmayamala:v6', ['mātṝṇāṃ']), ('brahmayamala:v10', ['śṛṇu'])] |
| FORMAT_ONLY | 0 | — |
| GLOSS_LOSS (unglossed token) | 384 | [('brahmayamala:v2', ['kāra', 'dārukāhvaya', 'devāssañcintitassarve', 'am']), ('brahmayamala:v4', ['māheśvarī', 'maheśvarāt', 'brahmā', 'i', 'brahmasaṃbhūtā'])] |

## The architectural answer

The dominant class determines the contract. If TOKEN_LOSS is dominant and real content is absent, L0 is a **lossy projection** OR the worker drops tokens (a production defect). If FORMAT_ONLY/CANONICALIZATION dominate, the roundtrip test encodes obsolete expectations and the contract should be corrected to preserve-invariants rather than exact roundtrip.

### Raw counts

- TOKEN_LOSS objects: 361
- CANONICALIZATION objects: 40
- FORMAT_ONLY objects: 0
- GLOSS_LOSS objects: 384
- total failing objects: 384
