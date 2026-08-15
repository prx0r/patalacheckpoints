# EDUCATION_ORGANISM — the audited education-serving organism

*One product folder, mirroring the Pāṭala products layout. This is the **education-serving organism**:
the derivational audit trail (any claim → source), the learning-compiler (LearningPackets), the AI
tutor (blind-graded), the learner store, and the OG endgame learning surface — all wired into the
Astro site + API. Deterministic engines, real data, audited.*

## Layout
```
education_organism/
  engines/
    education.py         LearningClaim · MasteryEvidence · compile_interactions · wrong_answer_to_neighbor
    organism.py          UserKnowledgeState · MisconceptionGraph (consumers as sensors)
    organism_loop.py     the 10-stage consumer→research machine
    misconception.py     the repair cascade (flag→RKA-propagate→dissolve)
    pedagogy.py          BKT mastery · next_interaction (targets the weakest skill)
    memory.py            procedural memory (dream-cycle consolidation)
    segment_key.py       GEM-A: segmentId:field provenance keying (from Bilara)
    reconciliation.py    GEM-C: the source-preservation gate (from Ambuda)
  README.md              (this index)
  AGENT-GUIDE.md         how to use the organism end-to-end
  VISION.md              the cohesive endgame (one organism: site + products + chain)
```

## Status (all verified on REAL data, CPU-only)
| Engine | Proof | What it does |
|---|---|---|
| `education.py` | 9/9 | interaction compiler → LearningPacket; wrong-answer→known-neighbor moat |
| `organism_loop.py` | 8/8 | consumer→research machine (probe→gap→proposal→human gate) |
| `misconception.py` | 9/9 | the repair cascade (closes the flywheel) |
| `pedagogy.py` | 7/7 | BKT mastery + next_interaction |
| `memory.py` | ✓ | procedural memory (dream-cycle) |
| `segment_key.py` | ✓ | GEM-A provenance spine |
| `reconciliation.py` | ✓ | GEM-C source-preservation gate |

**End-to-end audit trail (verified 5/5):** an education claim resolves to source:
```
EDUCATION → ESSAY → SYNTHESIS → ARGUMENT → C1 → L200 → L2 → L1 → L0 → T1 → SOURCE
```

## Serving (the live product surface)
- **Static Astro site** (10 pages, 0-JS): `/education/`, `/learning/` (schools·timeline·foundations),
  `/bibliography/`, `/themes/`, `/scholars/` — compute-on-write, immutable bytes.
- **API** (stdlib, :8787): `/education`, `/resolve` (audit trail), `/answer` (tutor grading).
- **Learner store**: SQLite (append-only events, mastery, misconceptions).

## Why it matters
This is the **endgame surface** — the OG patala learning site (schools, timeline, foundations,
tantraloka resources) made **audited through the organism**: every claim carries an epistemic ceiling
and resolves to its source, not free-floating prose. Scholars work it via the workbench; the public
reads it on the site; the organism keeps it honest.
