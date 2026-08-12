# HANDOFF-LOG — the coordination record between Agent 1 (ML) and Agent 2 (integration)

*One entry per handoff: what · why · file · date · direction (A1→A2 or A2→A1). Per the
`DUAL_AGENT_TRACK.md` protocol, every data-carrying handoff includes a schema snippet.*

---

## E1 — Agent 1 → Agent 2: E1-fidelity baseline done (2026-08-12)

**What:** Agent 1 completed the first real retrieval baseline — BM25 vs dense vs hybrid on the
C1→L2 fidelity task (query = C1 commentary, index = L2 only, 49 items, 300-bootstrap CI).

**Why it matters to Agent 2:** plain dense embeddings did NOT beat BM25 (MRR delta −0.035, p=0.083;
hybrid tie). This is an honest negative — it argues the discriminating signal is **structured/graph**
(see_also, key terms, relations), not a fancier text encoder. Agent 1 will need Agent 2's
themes-with-evidence / structured edges to test the flagship question.

**Files:**
- `machinelearning/research/experiments/E1-fidelity-REPORT.md`
- `machinelearning/research/experiments/fidelity_bm25_dense_hybrid.json`
- `machinelearning/research/tasks/PATALA-FIDELITY.jsonl`

**Schema of what Agent 1 consumes (the current substrate snapshot):**
```json
{ "id": "pt:passage:...", "locator": "chunkV2-O-...md", "l2_text": "string",
  "c1": { "verse_commentary": [{ "locator": "string", "commentary": "string" }] },
  "c1_source": { "summary": "string", "key_terms": "string", "related_passages": "string" } }
```

**Requested from Agent 2 (when ready):** themes-with-evidence — the deterministic theme proposals with
their member C1s + edge reasons, exposed with a schema snippet (see step 5 of the Agent 1 queue). Not
blocking anything Agent 1 does next (tokenizer + benchmark + full retrieval baselines are independent).
