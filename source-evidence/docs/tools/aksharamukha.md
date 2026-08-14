# Aksharamukha — broad script / romanization interoperability

**What Pāṭala borrows:** transliteration across **120 scripts and 21 romanization systems** with
script-specific orthographic handling — Grantha, Śāradā, Newa, Bengali, Devanagari, Kannada, IAST,
ISO 15919, etc. The broad interoperability fallback once manuscripts (Grantha/Śāradā) appear.

**License:** MIT. Repo: `virtualvinodh/aksharamukha`.

## How Pāṭala consumes it
**PLANNED.** Vidyut `lipi` covers core IAST first; Aksharamukha is the broad fallback for manuscript
scripts.

## Doctrine
Reuse the ecosystem for script conversion; never reimplement. Core IAST via Vidyut; broad scripts via
Aksharamukha.
