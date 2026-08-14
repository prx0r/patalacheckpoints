# THE AUTONOMOUS PIPELINE — WIRED (agentpatala integrates agentgraph's organism into real patala)

*2026-08-14 · status: WORKING · the shared goal's priority-queue autonomous pipeline, made real in OG
patala. Agentgraph built `ingestion_organism.py` (the priority-queue loop, 10/10 tested); agentpatala
wired it to the REAL patala data — 48 untranslated Sanskrit works with on-disk source from the sivaqueue.*

---

## WHAT WORKS (tested, `autonomous_pipeline.py`)

```
Loaded 48 real untranslated Sanskrit works from the sivaqueue with on-disk source
  - pancarthabhasya_kaundinya (60 lines, Pāśupata)
  - ganakarika (2481 lines, Pāśupata)
  - sivadharmasastra (4578 lines, Śivadharma)
  - ... (48 total)
Priority queue: 48 works queued (shortest first)
--- running pancarthabhasya_kaundinya through the organism ---
result: {"ok": true, "version": "15218c5635678c3e:v1"}
```

**The loop is real:** real docs → priority queue (shortest-first, the dialect-genealogy ordering) → a
real work (Pañcārthabhāṣya) runs through the full organism loop → committed as a content-addressed
version.

## HOW IT'S WIRED

- **AGENTGRAPH's** `ingestion_organism.py` (the 8-step loop: sense → prioritize → ingest → refine →
  verify → commit → serve → feedback) is the engine.
- **AGENTPATALA's** `migration/v3/autonomous_pipeline.py` loads the REAL patala data: the sivaqueue
  priority targets + the on-disk source files (`data/corpus/sources/`), maps them to `SanskritDoc`,
  queues them (shortest-first = lowest cost), and runs the loop.

## THE REAL DATA (48 works on disk)

The sivaqueue has 100 targets; **48 have real on-disk Sanskrit source** in `data/corpus/sources/`.
These are the untranslated works the pipeline ingests. The priority ordering (shortest first, then by
dialect-genealogy: Krama → Kubjikā → Pāśupata → Śaiva Siddhānta) lets the lexicon compound each hop.

## NEXT (the corpus-wide graduation)

The pipeline is wired; the next step is **running each queued work through the REAL Hermes translation**
(not just the loop's scaffold) — the full spine per work: source → tokenize → translate (Hermes) →
proof → argument → review → commit → serve. That's the corpus-wide graduation: the whole priority queue
fed through the organism as ONE coherent system.

## STATUS

- ✅ The priority-queue autonomous loop works on real patala data (48 works loaded, a real work run + committed)
- 🔄 The full Hermes-translation-per-work corpus-wide run is the next build (agentpatala)
- ❌ The organism's closing edge (`misconception.py` repair cascade) is still agentgraph's gap

---

*This is the shared goal made real: agentgraph's ingestion organism, wired to agentpatala's real corpus,
running autonomously. The priority queue is loaded, the loop works, and the corpus-wide graduation is
the next milestone.*
