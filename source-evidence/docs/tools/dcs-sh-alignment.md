# DCS↔SH alignment — cross-parser disagreement dataset

**What Pāṭala borrows:** the alignment between Digital Corpus of Sanskrit (DCS) annotations and Sanskrit
Heritage analyses — a **cross-parser disagreement dataset**. Also `svarupa_alignment` (VedaWeb/DCS/
Heritage/Samsaadhanii). This is the "no single analyzer is authoritative" foundation.

**License:** GPL-3.0. Repos: `SriramKrishnan8/dcs_sh_alignment`, `SriramKrishnan8/svarupa_alignment`.

## What it gives Pāṭala
```
PAT-LING-001
  surface Sanskrit
    ↓
  analysis[DCS]
  analysis[Heritage]
  analysis[VedaWeb]
  analysis[Samsaadhanii]
    ↓
  agreement matrix  (3/4 etc.)
    ↓
  Pāṭala candidate analysis + confidence
```

## How Pāṭala consumes it
**PLANNED / WATCH.** Data requires external Google Drive downloads (not self-contained). Usable as a
pattern/reference for the multi-analyzer agreement/uncertainty layer. Instead of "machine says X" →
"three independent Sanskrit systems support X; one proposes Y."

## Doctrine
Represent morphological/linguistic analysis as a **set of independent analyses with an agreement
matrix**, not one authoritative parse.
