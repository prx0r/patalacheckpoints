# Bibliography strategy — curated, tiered expansion (not "everything")

*2026-08-13. A working decision on **how far the Pāṭala bibliography goes** — how much of GRETIL /
Muktabodha / the wider tradition to register. The short answer: **curated + tiered + slowly expanding**,
with the factory's own quality signal deciding what earns a record.*

---

## The tension

- **Too narrow** (only IPVV + core) → the atlas can't support the Śaiva→Vedic→Greek genealogy vision;
  every expansion needs new bibliography.
- **Too broad** (every GRETIL/Muktabodha e-text) → thousands of low-value seed records, most with no
  English, no clear school/period, unverified; the atlas becomes noise and the factory spends budget
  on texts nobody needs.

The middle path: **register what the factory + the genealogy actually touch, at increasing depth,
and let the quality signal (source_ready) drive the priority.**

---

## The tiered model

### Tier 0 — Actively worked (curated, audited)
Everything the factory is **processing now**: on-disk Sanskrit, in the queue, CLEAN+HIGH priority.
These get **full** records — school, śākhā, period, author, register, sources, translations, verdict.
**≈ the 52 CLEAN+HIGH works today.** This is the gold standard; these become `state: audited`.

### Tier 1 — In the queue / on-disk (seed records)
Any work with an **on-disk Sanskrit source** (`data/corpus/sources/`, currently 73) gets at least a
**seed** record (tradition + period + source + translation status) so the catalog/API can show it and
the factory can route it. This is the **"ensure it's all in the bibliography"** bar we just met.
`state: seed`.

### Tier 2 — Documented but not acquired (registry-only)
Works in the **sivaqueue guides / access-manifest** that are scholarly targets but have no on-disk
source yet (scans needing OCR, paywalled editions). Record the **metadata + links** so they're
discoverable and the OCR/manuscript pipeline knows they're wanted — but don't register them as
factory-ready. `state: seed`, `translationStatus` honest.

### Tier 3 — The wider tradition (on demand, never bulk)
GRETIL's full ~490-work corpus, Muktabodha's full library, etc. are **NOT** bulk-registered. They are
registered **when the genealogy / a manuscript / a request actually touches them** — i.e. lazily,
one work at a time, with the same quality gate. This keeps the atlas curated and trustworthy while
still being able to grow toward the full tradition over time.

---

## The rule in one line

> **Register breadth at Tier 2 (metadata) automatically, but only promote a work to factory-ready
> (Tier 0/1) when it has an on-disk source + a real reason (genealogy value, manuscript, request).**
> The bibliography grows **curated + tiered + slowly**, never "dump everything."

---

## What this means operationally

- **Today (done this session):** 254 records — 73 on-disk works all have seed records (Tier 1 closed),
  plus the sivaqueue3/4 census works (Tier 2), plus the audited core (Tier 0).
- **The factory's `source_ready` priority** decides which seeds get promoted toward audited — a
  HIGH+CLEAN+READY work is where the factory spends budget, and that's the signal for "deepen this
  record."
- **Do NOT** write a bulk GRETIL/Muktabodha importer for thousands of records. Write a **lazy lookup**
  that registers a work on demand (when a manuscript, a request, or the genealogy touches it).

---

## The carry-forward

The bibliography is the **source of truth**; it grows **curated, tiered, and on-demand** — Tier 0
(audited, what the factory works) → Tier 1 (seed, on-disk, in the queue) → Tier 2 (metadata, not yet
acquired) → Tier 3 (lazy, only when touched). The factory's quality signal decides promotion. This
keeps the atlas a high-signal, trustworthy scholarly asset instead of a dump, while still scaling
toward the full Śaiva→Vedic→Greek tradition.
