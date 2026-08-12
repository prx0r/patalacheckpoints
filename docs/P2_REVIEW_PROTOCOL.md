# Corrected P2 blind-review protocol

## Generate

```bash
python3 pipeline/build_p2_review_blind_fixed.py \
  --ensemble /tmp/ens_s2/p2_disagreements.jsonl \
  --l0dir /mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/l0 \
  --out /tmp/p2review.jsonl \
  --key-out /tmp/p2review_key.jsonl
```

Give the reviewer **only**:
`/tmp/p2review_blind.csv`

Do not expose:
`/tmp/p2review_key.jsonl`
or the ensemble disagreement file.

## Reviewer labels

`SUPPORTED`
: L0 morphological analysis is the best/normal analysis in this context.

`PLAUSIBLE_ALTERNATIVE`
: L0 is linguistically licensed, but at least one competing analysis remains genuinely plausible.

`CONFLICT`
: L0 analysis is not supported by the reviewer’s reading.

`CANNOT_DECIDE`
: evidence/context is insufficient.

Also record:
- preferred lemma if different;
- whether the difference can materially change translation;
- short reason.

## Score

After the review is frozen:

```bash
python3 pipeline/score_p2_review_fixed.py \
  --review /tmp/p2review.jsonl \
  --key /tmp/p2review_key.jsonl \
  --out /tmp/p2_matrix.json
```

Do not tune Vidyut/Heritage normalization rules after inspecting the human labels without versioning a new evaluation round.
