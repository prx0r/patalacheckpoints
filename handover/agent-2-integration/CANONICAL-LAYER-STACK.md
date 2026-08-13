# PĀṬALA CANONICAL LAYER STACK — the authoritative reference (LOCKED 2026-08-13)

*This is the single source of truth for the canonical layer order, the file type each layer produces,
and the dependency between layers. It is **verified against the actual IPVV stack on the mount**
(`/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/`) — every claim below is grounded in a
real file, not recalled. The autonomous factory workers and all plans must follow this order exactly.
Do NOT rename layers, reorder the stack, or invent file types without updating THIS file.*

---

## 0. THE CANONICAL ORDER (one line)

```
SOURCE → T1 → L0 → [argument map] → L2 → L200 → C1 → THEME → ESSAY → EDUCATION
```

**Two key truths (verified):**
1. **T1 and L0 are the SAME transliteral content in two encodings.** T1 = word-by-word gloss as
   *markdown prose* (`01_t1/`, `02_t1/`); L0 = the same transliteral gloss as *structured token
   records* (`l0/`, `l0_v1/`), produced by `t1_extract.py`. **L0 is derived FROM T1.**
2. **L2 (readable whole-passage prose) is the OUTPUT, not the input.** It is derived AFTER the
   transliteral layer, **guided by the argument map** (`pilot_*_ARGUMENT_MAP.md`).

> **⚠️ NAMING DISAMBIGUATION (critical, do not confuse):** there are TWO different things historically
> called "T1".
> - **CANONICAL T1 (this stack, the IPVV definition) = the transliteral word-gloss** — the
>   `[and]-GLOSS (IAST)` word/phrase-faithful gloss (e.g. `[and]-thus (evam)`). This is the floor, and
>   L0 is its structured encoding. **THIS is the T1 in this stack.**
> - **LEGACY "T1" (the retired `translate-work` skill + `auto_translate_raw.py` state machine
>   `T1→R1→T2→R2→T3→C1`) = a "best constructive reading" / close translation.** That is a *different,
>   earlier pipeline*; its "close translation" is the readable-English stage, which in THIS canonical
>   stack corresponds to **L2** (the readable layer), not the canonical T1.
> When reading any file, treat **T1 = transliteral word-gloss** (canonical). The legacy
> `translate-work`/`auto_translate_raw` "close translation" is the L2-style readable layer, not this
> stack's T1.

---

## 1. THE LAYERS — file type, source dir, dependency (verified)

| # | Layer | What the file IS | Source dir (IPVV) | Depends on |
|---|---|---|---|---|
| 1 | **SOURCE** | raw Sanskrit base text | `00_source/` | — |
| 2 | **T1** | **transliteral word-gloss markdown** — each Sanskrit token + literal English in-line, e.g. `[and]-thus (evam), [and]-with-this-vimarśa-three (amunā...)` | `01_t1/` (Vol 1), `02_t1/` (Vol 2/3) | SOURCE |
| 3 | **L0** | **structured token records** — `raw_fragment` + `lemma_iast` + `literal_gloss` (same content as T1, machine form) | `l0/` (extraction), `l0_v1/` (legacy) | **T1** (`t1_extract.py → l0/*.l0.jsonl`) |
| — | **argument map** | the passage's argument structure: the plan, kārikās, the verse-scheme, OPEN items | `pilot/*_ARGUMENT_MAP.md` | SOURCE + L0 (a **lateral guide**) |
| 4 | **L2** | **readable whole-passage prose** — "The powers — knowledge, memory, removal — have been established..." | `pilot/*_L2_read.md` | L0/T1 + **argument map** |
| 5 | **L200** | the **audit** of how L2 was derived (8 sections: identification, published reading, derivation map, MT decisions, IA, source layer, crossrefs, open, review state) | `l200/` (canonical), `l200_legacy/` (preserved) | L2 + L0 + argument map + source |
| 6 | **C1** | passage-local commentary (SUMMARY/FUNCTION/KEY TERMS/EXPLANATION/BOUNDARY/RELATED) | `c1/read/` + `c1/source/` | L200 |
| 7 | **THEME** | evidence-backed synthesis across C1s (not a keyword/cluster) | — | C1 |
| 8 | **ESSAY** | proof-carrying prose from themes (+ comparison/modern application) | — | THEME |
| 9 | **EDUCATION** | pedagogic distillation of the essay | — | ESSAY |

**The argument map is the one non-sequential element** — it is a *lateral guide* (produced alongside
the transliteral work) that unlocks the readable L2 layer from the transliteral stack. It is not a
separate numbered stage; it is the semantic key to going word→passage.

---

## 2. THE CORRECT CREATION ORDER (what to build, in what sequence)

Work layer by layer, each layer's worker + validator against its canonical spec + source files. Do NOT
build a layer whose upstream is not committed.

```
1. SOURCE      acquire/verify the raw Sanskrit
2. T1          transliteral word-gloss (the FLOOR — the first interpretive layer)
3. L0          structured token records FROM T1 (same content, machine form)
4. argument map  the passage's argument structure (lateral guide)
5. L2          readable whole-passage prose, guided by the argument map
6. L200        the audit of how the L2 was derived
7. C1          passage commentary
8. THEME       evidence-backed synthesis across C1s
9. ESSAY       proof-carrying prose from themes
10. EDUCATION  pedagogic distillation of the essay
```

---

## 3. THE SPECS / SOURCE FILES EACH LAYER MUST FOLLOW

| Layer | Canonical spec / source file |
|---|---|
| T1 | `translations/_stack/ipvv/01_t1/` · `02_t1/` (the transliteral exemplars) |
| L0 | `translations/_stack/ipvv/l0/*.l0.jsonl` · `l0_v1/*.l0.jsonl` · `specs/l0_schema.json` |
| argument map | `translations/_stack/ipvv/pilot/*_ARGUMENT_MAP.md` |
| L2 | `translations/_stack/ipvv/pilot/*_L2_read.md` |
| L200 | `translations/_stack/ipvv/l200/README-L200-SPEC.md` (frozen 8-section) + the 3 canonical models (V2-O, V3-B, V3-C) |
| C1 | `translations/_stack/ipvv/c1/C1-SPEC.md` + `c1/read/*.md` |
| THEME | `translations/_stack/ipvv/specs/SPEC_THEME.md` + `SPEC_THEME_CLUSTERING.md` |
| ESSAY | `translations/_stack/ipvv/specs/SPEC_ESSAY.md` |
| EDUCATION | `translations/_stack/ipvv/specs/SPEC_EDUCATION.md` |

---

## 4. THE AUTONOMOUS WORKERS (what maps to what)

| Layer | Worker (pipeline/) | Validator (layer-specific, deterministic) |
|---|---|---|
| T1 | (to build — the transliteral gloss producer) | T1 fidelity: token↔gloss correspondence, provenance to source |
| L0 | `l0_worker.py` + `raw_l0.py` | `validate_l0_spec` (P0 lossless + schema + abstraction) |
| L2 | `l1_l2_translate.py` (L1L2 model path) + `l1_l2_worker.py` | L2 semantic-fidelity (content ⊆ L1+supplies) |
| L200 | `l200_worker.py` | Task-2 fidelity (8 sections, MT/IA split, derivation map) |
| C1 | `c1_worker.py` | C1-SPEC §17 (passage-local, concise, no modern-comparison) |
| THEME | `theme_worker.py` | members resolve, strength+role, boundary, MACHINE_PROPOSED |
| ESSAY | `essay_worker.py` | SentenceEvidenceAudit (every sentence licensed) |
| EDUCATION | `education_worker.py` | derived-from-essay, concise, no overreach |

**Every worker reuses the existing canonical machinery where it exists** (per the doctrine: reuse before
build). Agent 1's algorithms (theme clustering, argument, essay, semantic alignment) are the *proposal
engines*; Agent 2 wraps them in the autonomous controller flow + layer-specific validator.

---

## 5. CP1 = the machine-learning-verified L0 / T1 / L1 / R1 READING (the foundation proof)

CP1 is the foundation checkpoint: prove a machine-learning-verified L0 (or T1/L1/R1) reading. This is
what every downstream layer builds on. Concretely:
- Our L0 must be (a) schema-isomorphic to the IPVV exemplars, (b) validator-equivalent
  (`validate_l0_spec` passes on both), (c) P0-lossless (source exactly reconstructible), and (d)
  **semantically equivalent** to the exemplar gloss — the ML part.
- The semantic-equivalence harness lives at `docs/ML-L0-SEMANTIC-EQUIVALENCE-PROPOSAL.md`.

---

*LOCKED. Do not reorder, rename, or re-type the layers without updating THIS file. The autonomous
factory, the DEV-PLAN, and the CHECKPOINTS all reference this as the canonical layer contract.*
