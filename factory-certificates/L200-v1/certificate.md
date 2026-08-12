# L200 Certificate (v1) — validator torture test + derivational proof

Run: `python3 pipeline/certificate_l200.py`

## Result: PASS
- **10/10 phenomenon fixtures** pass the structural validator AND the typed reference checks
  (SUPPLIED · REFERENT_SUPPLY · STRUCTURAL_CONNECTIVE · LEXICAL · GRAMMATICAL · IA-not-MT ·
  speaker-boundary · quotation · unresolved · zero-MT/IA).
- **14/14 dimensions** (A–L):
  - A derivation binding (canonical l2_ref + l2_hash + upstream) · A wrong-l2_ref flagged
  - B eight-section completeness
  - C/D/E MT recall + precision via typed reference conditions (not lexical matching)
  - F MT/IA laundering flagged (IA-as-MT caught by forbidden_mt)
  - G source-layer required + wrong-attribution caught
  - H open-item honesty (unresolved fixture must surface its OPEN item)
  - I failure semantics (GENERATION_FAILED never commits)
  - **J empty-success** — zero-MT/IA with COMPLETE status commits ([] = successfully found nothing)
  - CD invalid MT type rejected
  - K replay (no duplicate on identical input)
  - **L mutation/invalidation** — change upstream L2 hash → prior L200 superseded, cannot masquerade

## The key asymmetry (proven)
`[] because the model successfully found nothing` (J, commits) ≠ `[] because generation failed` (I, blocks).
And L proves L200 behaves as a real derivational proof object (upstream change invalidates downstream).

## Honest scope
This certificate proves the **deterministic validator + typed-reference semantics + adversarial
rejection + invalidation** are correct (all mutations fail; all correct fixtures pass). The **live model
MT/IA proposal is the generative layer** — here stubbed with the fixture's reference (deterministic,
reproducible). Real model MT/IA on actual IPVV chunks at scale remains the pending generative work,
gated by the same validator. Per the review, L200 is NOT scaled across IPVV yet.
