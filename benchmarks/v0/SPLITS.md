# PATALA BENCHMARK v0 — SPLITS (leakage policy)

*2026-08-12. The most important design decision. Do NOT use random passage splitting as the main
evaluation — tightly-related material leaks vocabulary, argument sequence, commentary phrasing, and
adjacent passages. Use progressively harder split classes.*

---

## 1. The split classes

| Class | Meaning | Use |
|---|---|---|
| **S0 — SAME-PASSAGE** | train and test on the same passage | development / debug only |
| **S1 — PASSAGE HELD-OUT** | different passage, same local argument family | weak generalization |
| **S2 — ARGUMENT-FAMILY HELD-OUT** | entire dialectical sequence withheld | **the meaningful v0 test** |
| **S3 — SECTION/VIMARŚA HELD-OUT** | whole vimarśa/adhikāra withheld | stronger |
| **S4 — WORK HELD-OUT** | train IPVV → test another text | eventual transfer |

**For v0, S2 is the meaningful test wherever enough data exists.** Random splits are S0/S1-grade and
leak — do not use them as the headline result.

---

## 2. How to assign a split class

A fixture's `split_class` is decided by WHICH scholarly units are withheld, not by a random seed:

```
S1: withhold the specific passage (its chunk)
S2: withhold the whole argument family (the vimarśa / dialectical sequence the passage belongs to)
S3: withhold the whole section
S4: withhold the whole work
```

The grouping is **scholarly** (by vimarśa/argument-family), not random.

---

## 3. ARG-GOLD-001 special case

There is ONE gold argument. Do NOT pretend there is a train/test split yet. Mark it:

```
split_class: EVALUATION_ONLY
allowed_training_use: false
```

Use it to test the HARNESS, not to select a model. Only after ~5 hand-built arguments exist can we draw
conclusions about extraction quality.

---

## 4. Leakage inspection

Every candidate fixture, before BENCHMARK_ACCEPTED, must answer:
- Is this source already used to GENERATE the method being evaluated? (→ exclude / DERIVED_FROM_PRODUCT)
- Does its training set contain the same argument family as its test? (→ S2 leakage → fix split)

---

## 5. The split manifest (per run)

Every run records its actual split in `runs/<ts>/split_manifest.json`, so a claim like
"late interaction beat BM25" is answerable as:
> on benchmark v0, split S2, Recall@5 improved X→Y, using this commit + config.
