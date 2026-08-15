# PĀṬALA PRODUCTS — standalone core engines

*One folder per product. Each product is a **standalone module** (stdlib + shared IPVV loader + the
deterministic `review_engine` reducer where relevant). No Next.js, no MCP, no network in the engine —
wire those up later. All engines hydrate from **real IPVV data**, so they are source-backed and
comparable.*

## Layout
```
pipeline/products/
  _shared/            ipvv.py · closed_vocabulary.py · canonical_id.py
  scholar_review/     Review #7 · Scholar Attestation #8 · Audit #14 (+ gate.py, signing.py)
  translation_proof/  Translation Proof #2 (the moat)
  argument/           Argument #5
  crux/               Crux #6
  research_packet/    Research Packet #9 (PathRAG flow + relevance_score)
  comparison/         Comparison #13
  evidence_independence/  evidence-independence (SOURCE_ECHO)
  claim/              Claim #4
  context_bundle/     Agent Context Bundle #16
  passage/            Passage / Reading #3
  benchmark/          Dataset / Benchmark #15 (inspect_ai)
  passage_workbench/  Passage Workbench (disagreement recording)
  terminology/        Terminology / Lemma-through-time
  timeline/           Timeline
```

## Status (all verified on REAL data, CPU-only)
| Product | Folder | Proof | Substrate |
|---|---|---|---|
| Review + Attestation + Audit | `scholar_review/` | 11/11 | IPVV goldchain+C1+assertions |
| Translation Proof | `translation_proof/` | 6/6 | IPVV passages |
| Argument | `argument/` | 6/6 | IPVV C1 |
| Crux | `crux/` | 4/4 | IPVV arguments |
| Research Packet | `research_packet/` | 5/5 | IPVV passages + PathRAG |
| Comparison | `comparison/` | 3/3 | IPVV arguments |
| Evidence Independence | `evidence_independence/` | 5/5 | corroboration registry + live OpenCitations |
| Claim | `claim/` | 7/7 | IPVV C1 → proposition |
| Context Bundle | `context_bundle/` | 6/6 | composes argument/crux/claim/packet |
| Passage / Reading | `passage/` | 6/6 | IPVV passages + KG2Code query |
| Benchmark | `benchmark/` | 5/5 (+ inspect_ai 1.000) | real samples → inspect_ai |
| Passage Workbench | `passage_workbench/` | 5/5 | disagreements → durable review gate |
| Terminology | `terminology/` | 6/6 | trajectories.json + terms.json |
| Timeline | `timeline/` | 5/5 | historyTimeline.json |
| **Total** | | **80/80** | |

## Run everything
```bash
cd /root/patalacheckpoints
for p in scholar_review translation_proof argument crux research_packet comparison evidence_independence claim context_bundle passage benchmark passage_workbench terminology timeline; do
  echo "--- $p ---"; PYTHONPATH=pipeline python3 pipeline/products/$p/test.py | grep SUMMARY
done
```

## The dependency chain (kept minimal + acyclic)
```
_shared/ipvv.py ──► translation_proof   (reads passages)
                ──► argument           (reads C1 passages)
argument ──► crux ──► comparison
argument ──► research_packet (via shared ipvv)
scholar_review (reads goldchain + passages + assertions; uses review_engine reducer)
```

## Product ↔ v3 catalog
- **#2** Translation Proof → `translation_proof/`
- **#5** Argument → `argument/`
- **#6** Crux → `crux/`
- **#7** Review → `scholar_review/`
- **#8** Scholar Attestation → `scholar_review/`
- **#9** Research Packet → `research_packet/`
- **#13** Comparison → `comparison/`
- **#14** Audit → `scholar_review/`

## Wiring later (NOT done in the engines)
- **API**: a thin `app/api/<product>?verb=...` route per product (spawnSync → `<product>/engine.py`)
- **MCP**: `patala_<product>_*` verbs (spawnSync → `<product>/engine.py`)
- These are deliberately absent from the engines so they stay portable; wire them when the repos are
  aligned.

## Honest limits (shared)
- All engines are deterministic + stdlib; no live LLM/auditor calls. Live auditors (xCOMET/MQM),
  formal validity checking (ASPIC+/AIF), production signed-auth, and durable ledger persistence are
  later integrations — documented per product.
