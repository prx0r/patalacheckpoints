# Pāṭala — Handover (2026-08-10)

*The single entry point for the next agent. Consolidates the whole project: what
Pāṭala is, the two codebases, what's built, how to run it, and what's next. See
`PROCESS_NOTES.md` for the strategic reorientations and `docs/PIPELINE_SOURCE_MANUAL.md`
for the code manual.*

---

## 1. What Pāṭala is

**Repo:** https://github.com/prx0r/patala (branch `main`), local `/root/projects/patala`.

Pāṭala is the **provenance + adjudication infrastructure for tantric textual knowledge**.
It sits *between* manuscript repositories (Muktabodha, OCHS, GRETIL) and the
people/AI that use them. It is NOT a translation-factory, NOT another archive, NOT an
OCR/lemmatisation/RAG project (those commoditize).

The real product is the scholarly loop:
```
SOURCE → PASSAGE → ASSERTIONS → EVIDENCE → REVIEW → ACCEPTED/DISPUTED → COMMENTARY → GRAPH
```
built on the **six primitives** (Identity, Assertion, Evidence, Provenance, Review, Rights).

**Core invariant:** *machines propose, humans review.* "AI proposes ≠ Pāṭala asserts."

---

## 2. The two codebases

| Codebase | Path | Role |
|---|---|---|
| **Pāṭala hub** | `/root/projects/patala` (git) | pipeline, API, passage corpus, bibliography, docs, skills |
| **Sanskrit corpus** | `/root/projects/sanskritree` (= `/mnt/HC_Volume_106427611/sanskritree`) | raw Sanskrit, flat translation files, dossiers, anchors, strategic docs |

The pipeline reads the corpus from `sanskritree/translations/`.

---

## 3. What's built (validated)

### The pipeline (`pipeline/`)
The durable state machine `T1 → R1 → T2 → R2 → T3 → T3.1 → [C1]`:
- `state_machine.py` — load/transition/run/audit/persist/reload; prerequisite-gated;
  versioned stages; stage-local audits; invalid-stage RETRY.
- `schema.py` — the record structure, stage constructors, versioning, review events.
- `contracts.py` — stage contracts (empty/`{}` strict output is INVALID).
- `audit.py` — structural + epistemic validation.
- `prompts.py` — the house prompts (lean model contracts per stage).
- `evidence.py` — the EvidencePacket (neighbors, terms, occurrences, crux surface terms).
- `validate.py` / `validate_readiness.py` / `validate_trajectories.py` — conformance,
  derived readiness, trajectory integrity.
- `model.py` — **shells out to `hermes -z`** (Hermes owns provider reliability/retries);
  we keep the schemas/contracts/parse logic.
- `milestone_a.py` — the Milestone-A runner (build one complete object for `1.8`).

### The API/MCP
19 API routes, 13 MCP tools, 83/83 test suite, OpenAPI spec, docs-site nav.

### The corpus
4,395 passages (7 works), 1,542 OCHS witnesses, 15 terms + trajectories,
**1/68 works translation-ready (derived)**.

### The skills (`skills/`)
`translate-work`, `translate-passage`, `write-commentary`, `validate-passage`,
`assemble-stack`, `use-api`.

---

## 4. The model-interface decision (critical)

We spent a long time trying to make `deepseek-v4-flash` return reliable JSON via the
raw API. The verdict: **stop**. `model.py` now delegates the model call to `hermes -z`
(which handles retries, backoff, provider switching). We keep our contracts/audit.
The success criterion is: give Hermes a work, walk away, come back to completed +
explicitly-failed records. **Do not reopen the model-interface rabbit hole unless
Hermes can't run batches at all.**

---

## 5. How to run

```bash
cd /root/projects/patala
npm run dev          # the API (localhost:3000)
npm test             # 83-check suite (needs the API up)

# build one scholarly object (Milestone A) via Hermes:
python3 pipeline/milestone_a.py     # kramasadbhāva 1.8 through T1..T3.1

# validate:
python3 pipeline/validate.py --report
python3 pipeline/validate_trajectories.py
python3 pipeline/validate_readiness.py
```

Hermes key: set `OPENCODE_GO_API_KEY` in `~/.hermes/.env` (opencode-go). Hermes
config: `~/.hermes/config.yaml` (`tantrakosa` MCP → `http://localhost:3000`).

---

## 6. The three milestones

- **A — one complete object:** `kramasadbhāva 1.8` source→C1→audit (in progress).
- **B — a coherent corpus:** `kramasadbhāva 1.1–25` automated by Hermes; inspect
  quality/consistency/failures.
- **C — external feedback:** 5 strong passages → one real Krama specialist.

---

## 7. What's next (priority)

1. Finish Milestone A → a real C1.
2. Milestone B (25-verse unit).
3. Write the **scholarly-graph schema** (Work/Witness/Passage/SourceSpan/Person/
   Term/Sense/Resource + annotations) — the canonical model that must survive years.
4. Milestone C (one scholar conversation).
5. Deepen the bibliography just-in-time.

**Deferred:** scholar dashboard, marketplace, payments, fancy RAG, custom OCR, all-69
bibliography completion, consumer UI.

---

## 8. Honest caveats

- **Milestone A is mid-flight** — the model path works (T1, R1 done via Hermes) but the
  stages take ~1min/call; a full 1.8 → C1 is minutes.
- The **corpus is small** (7 works segmented; 1 work translation-ready).
- **58 bibliography records are seed/verified:false** — readiness is derived, not asserted.
- The **docs are extensive but live in two repos** — `patala/docs/` and
  `sanskritree/corpus/targets/`; keep them in sync.
- `data/manuscripts.json` (5.5MB) and `kubjikamata.jsonl` (1.5MB) are gitignored
  (regenerate, don't commit).
