# Recipe — Explore terminology

The term ledger is Pāṭala's evidence-backed glossary: **accepted senses** are review-promoted; **proposals** are separate and never auto-accepted. A lemma has different senses in different texts/periods/traditions — there is no single global meaning.

## 1. The accepted ledger

```bash
curl "http://localhost:3000/api/terms"
```

Returns each lemma with its accepted sense labels and preferred renderings.

## 2. Accepted senses for one lemma

```bash
curl "http://localhost:3000/api/terms/kula/senses"
```

```json
{
  "lemma": "kula",
  "senses": [
    { "id": "kula.lineage", "label": "lineage / family" },
    { "id": "kula.body.power", "label": "body / power / totality" }
  ],
  "preferred_renderings": ["totality", "lineage", "body of powers", "the Kula (school)"],
  "proposals": 1
}
```

`accepted` = current editorial position, not universal consensus. These are **not** a dictionary and not evidence of occurrence.

## 3. Surface occurrences (honest about method)

```bash
curl "http://localhost:3000/api/terms/kula/occurrences?work_id=kubjikamata"
```

```json
{
  "lemma": "kula",
  "match_method": "substring",
  "lemmatized": false,
  "count": 207,
  "occurrences": [ ... ]
}
```

**This is substring matching, not lemma retrieval.** Sanskrit inflects — `śakti / śaktiḥ / śaktim` are different surface forms. The `lemmatized: false` field is Pāṭala being honest that this is a raw concordance, not a morphological search.

## 4. The diachronic sense-trajectory (the signature feature)

The reference map's killer feature: a lemma does NOT have one meaning — it has a
**trajectory** across traditions and periods.

```bash
curl "http://localhost:3000/api/terms/kula/history"
```

```json
{
  "lemma": "kula",
  "trajectory": [
    {
      "id": "kula.yogini.lineage",
      "scope": { "period": { "label": "early Yoginī/Kaula" }, "traditions": ["kaula"] },
      "sense_id": "kula.lineage",
      "claim": "within early Yoginī/Vidyāpīṭha material, kula carries socio-mythic lineage classification",
      "evidence_links": [ { "target_id": "resource:sanderson-vidyapitha", "type": "resource", "role": "historical_argument" } ],
      "origin": "reference_map",
      "status": "accepted",
      "certainty": "secure"
    },
    { "id": "kula.kaula.body-power", "sense_id": "kula.body.power", "claim": "the Kaula homonym-extension: lineage → body → power → totality", "status": "accepted" },
    { "id": "kula.kubjika.mantra-body", "sense_id": "kula.body.power", "claim": "the body/power sense articulated through the mantra-body (mantradeha)", "evidence_links": [{ "target_id": "tantra:text:kubjikamata:17.80", "type": "passage", "role": "supports" }], "status": "reviewed" },
    { "id": "kula.abhinava.akula-pole", "sense_id": "kula.body.power", "claim": "the kula-pole set against the transcendent akula", "evidence_links": [{ "target_id": "tantra:text:tantraloka:3.143", "type": "passage", "role": "supports" }], "status": "accepted", "certainty": "secure" }
  ],
  "warnings": [],
  "accepted_senses": [ ... ],
  "proposals": 1
}
```

These are **curated historical-sense assertions** — each node references an accepted
(`sense_id`) or proposed (`proposed_sense_id`) sense from the ledger (no parallel
sense ontology), carries stable IDs + addressable evidence links, and separates
`origin` (where the claim came from), `status` (epistemic maturity) and `certainty`.
The trajectory is a *projection over curated claims*, not mechanically derived from
corpus occurrences — the diachronic shift is scholarly synthesis, not raw data.
`warnings[]` surfaces unresolved evidence or proposed nodes.

## 5. Machine/human proposals (separate)

```bash
curl "http://localhost:3000/api/term-proposals?lemma=kula"
```

Proposals live here. A proposal **never** promotes itself into the accepted ledger — only a human review event does (`proposed → reviewed → accepted`).

---

**MCP:** `get_term_senses({ lemma })`, `get_term_history({ lemma })`, `find_term_occurrences({ lemma })`, `concordance({ q })`.
