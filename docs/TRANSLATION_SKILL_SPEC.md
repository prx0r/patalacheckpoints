# Translation Skill + MCP — spec (un-overengineered)

*2026-08-10. The goal: formalise the translation process we already run (T1 → R1 → T2 → R2 → T3 → C1) into a repeatable **skill**, add the **T3.1 readable layer**, and ship a **minimal MCP** that ChatGPT/Claude can call to translate in our house style. We deliberately do NOT build the full concordance/parallel/audit engine first. The deliverable is one working "translate" command + the research context it needs. Everything heavier is a later checkpoint.*
Companion to `TRANSLATION_PROTOCOL.md` (the fuller data-model vision — this doc is the *buildable* slice).

---

## 0. The governing rule

**The translations ARE the substrate** (concordance, term history, commentary, audits, TTS, MCP all derive from them). So the skill's job is to make each translation produce **versioned, passage-level, evidence-carrying** output — not a loose blob. But we keep the *output format* close to what we already write, so nothing is thrown away and the skill ships fast.

---

## 1. The pipeline we already have → the formal skill

We formalise exactly what we run today, plus one new layer (T3.1):

```
T1  working translation (pass-1 files, [X]-flags, provenance header)
 → R1  review of T1 (crux-verses; [G]/[P]/[A] evidence)
 → T2  fresh translation, DIFFERENT strategy (blind of T1's sentences)
 → R2  T1-vs-T2 comparison + adjudication + growing commentary (converges)
 → T3  final synthesis (the resolved text; OPEN flags carried inline)
 → T3.1  READABLE layer (NEW) — natural-English reading translation of T3,
        always linked to T3 (updates in lock-step with it)
 → C1  commentary pass (independent research, may overturn T3)
```

**Key additions from the protocol:**
- **T3.1** = the *reading translation* (protocol §2B), derived from T3 but written as clean natural English. It is **derived, not independent** — it lives inside the same record as `translation.reading`, so when T3 changes, T3.1 is regenerated. This is the "site reader" voice; T3 stays the close/scholarly voice.
- **Term ledger** (protocol §3–4): during T1/T2 each crux term records `surface → lemma → translation_here → sense → certainty`. Minimal: a `terms:` list per passage. This is the seed of the concordance.
- **Version + provenance header** stays (as we already do). Nothing is overwritten; every phase appends.

**Status labels (unchanged, extended):** `T1-done → R1-done → T2-done → R2-done → T3-FINAL → T3.1-done → C1-done`.

---

## 2. The one "translate" command (the skill's core)

The skill is a **single orchestrated command**, not a monolith. It runs the pipeline per passage and writes versioned files. For MCP it is the *orchestrator*, not the only tool.

```text
translate <work> <chapter/range>
```

What it does, per passage:
1. **SOURCE** — pick edition/witness (from `bibliographySeed`/`audited` textSources, or explicit).
2. **SEGMENT** — assign stable IDs `tantra:text:{work}:{chapter}.{verse}`.
3. **DRAFT (T1)** — close translation, [X]-flags, provenance header, term ledger.
4. **CONTEXT** — call MCP tools for same-text / same-school / same-period usage + existing translations + term policy.
5. **READING (T3.1 seed)** — natural-English rendering of the T1 draft.
6. **AUDIT** — self-check (negation, numbers, omission, addition, term drift, grammar, parallel conflict).
7. **WRITE** — append a versioned record to the work's translation file.

It writes exactly the artifacts we already use (`{text}_pass1.md` etc.), extended with the `terms:` + `reading:` fields. The human (you) still runs R1/T2/R2/T3; the skill makes each phase a *repeatable, versioned, evidence-carrying* step.

---

## 3. The MCP deliverable (v1 — small, real)

One MCP server, read-only over the corpus, with a handful of tools. **No vector DB, no full-text search engine yet.** Tools read files we already have.

| Tool | Reads | Purpose |
|---|---|---|
| `get_skill_protocol` | the protocol + style guide | tells the model our house style + pipeline (injects the "instructions") |
| `get_source_passage` | `sanskritree/sources/**` (Sanskrit e-texts) | fetch the Sanskrit for `work:chapter.verse` |
| `get_existing_translation` | `sanskritree/translations/01_t1_working|05_t3_final/**` | fetch our existing T1/T2/T3 for a passage |
| `get_term_policy` | a small `data/terms.json` (curated senses) | the glossary / sense policy for a lemma |
| `find_lemma_occurrences` | a simple precomputed `data/occurrences.json` | same lemma across our corpus (start coarse: per-text counts) |
| `get_anchor` | the on-disk anchor texts (Dyczkowski stack, GRETIL) | quote the published translation/commentary for a passage |
| `translate` | the pipeline | orchestrate T1→...→T3.1 per the protocol, write versioned files |

**Design choice (protocol §10 honoured):** `translate` is the orchestrator; the *research primitives* (`get_source_passage`, `find_lemma_occurrences`, `get_anchor`, `get_term_policy`, `get_existing_translation`) are what the model calls to ground each step. The MCP returns **evidence**, not a magic answer.

**Minimal data files to build for v1 (all small, hand/semi-curated):**
- `data/terms.json` — the tracked technical lemmas + senses + policy (start ~15 terms: śakti, kula, krama, vimarśa, prakāśa, visarga, khecarī, āveśa, uccāra, śūnya, mātṛkā, spanda, saṃvit, parāmarśa, svātantrya).
- `data/occurrences.json` — per lemma, a coarse list of `{work, range}` (generated by a grep over the corpus once; not a live search).
- `data/anchors.ts` — the on-disk anchor paths (Dyczkowski stack, GRETIL) per work, from `bibliographySeed`/`audited`.

---

## 4. Anchor metadata by school + period (the missing piece, scoped small)

The protocol's §11 is right: "same school/period" needs each work tagged. We already have this in the bibliography (`traditions`, `period`). **v1 reuses `BibliographyRecord.period` + `traditions`** rather than building a new table. Only when the concordance gets real do we add a dedicated `works-meta` table with scholarly evidence per date/tradition.

---

## 5. What this does NOT build yet (explicit deferrals)

- Full-text / vector concordance — deferred (start with grep-based `occurrences.json`).
- Automatic parallel detection — deferred; parallels are captured manually in `terms:`/`parallels:` as we translate (protocol §13), then validated.
- `audit_translation` as a real endpoint — deferred; v1 audit is the model following the audit checklist in the skill, not a separate engine.
- TEI export, scholar-review UI, versioning DB — all later checkpoints.

This is deliberately a **1–2 session build**: the skill doc + the MCP server + the three small data files. It gets us a ChatGPT-usable translation assistant now.

---

## 6. Validation (how we know it works)

1. Point ChatGPT (or a CLI) at the MCP and run `translate` on **one chapter** of a genuinely-untranslated, clean-Sanskrit text (candidates: Timirodghāṭana, or a Kulasāra paṭala — both already in our working corpus).
2. Confirm the output has: stable passage IDs, `terms:` ledger, `reading:` (T3.1) alongside the close draft, [X]-flags, version + provenance header.
3. Confirm a human can run R1 → T2 → R2 → T3 → T3.1 → C1 on top of it without reformatting.
4. Confirm `find_lemma_occurrences` + `get_anchor` return useful context (not a search engine, just our indexed data).

---

## 7. Immediate next actions (in order)

- [ ] **Write the skill doc** (`docs/TRANSLATION_SKILL.md`) — the exact prompt/protocol the MCP injects: pipeline, style-guide rules (§8 of the protocol), audit checklist, output format (passage object with `terms:` + `reading:`).
- [ ] **Write the style guide** (`docs/STYLE_GUIDE.md`) — Sanskrit retention list, capitalisation policy, compound policy, ambiguity policy, no-anachronism rule.
- [ ] **Build `data/terms.json`** (curated senses for ~15 lemmas) + **`data/occurrences.json`** (grep-generated coarse index).
- [ ] **Build the MCP server** (TypeScript/Next or a small standalone server) exposing the v1 tools above.
- [ ] **Run the proof chapter** end-to-end; record it as Checkpoint 3.
