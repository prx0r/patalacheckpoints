# Recipe — Build an AI research agent

This is the recipe that turns Pāṭala into an LLM's *scholarly evidence engine* — the thing FoJin-style MCP is built for. The rule that governs everything: **machines propose, humans review.** Never let a machine output masquerade as reviewed knowledge.

## The agent's constitution (rules to follow)

1. **Resolve identities before assuming aliases.** Don't guess that "Amṛteśatantram" is Netratantra — resolve it.
2. **Prefer accepted assertions over proposals.** `accepted` term senses > `machine_proposed` candidates.
3. **Never report `machine_proposed` as established fact.**
4. **Preserve uncertainty.** Don't launder `[X]` corrupt loci or `certainty: low` into confident prose.
5. **Cite the source/provenance the API returns.**
6. **Distinguish Pāṭala metadata from upstream source material** (OCHS, GRETIL, Muktabodha own their data).
7. **Do not infer permissions from public accessibility** (`rights: unknown` means unknown).

## The research workflow

```
question
   ↓
resolve_work          POST /api/resolve/work     → the work id
   ↓
get_work              GET  /api/works/{id}       → metadata + status
   ↓
get_passage_context   GET  /api/context/passages/{id}  → evidence bundle
   ↓
retrieve evidence     get_term_senses · get_manuscripts · search_passages · concordance
   ↓
answer with provenance
```

## Example: "How is kula used in Kramasadbhāva?"

```bash
# 1. the work
curl "http://localhost:3000/api/works/kramasadbhava"

# 2. an evidence bundle for a passage
curl "http://localhost:3000/api/context/passages/tantra:text:kramasadbhava:1.9"

# 3. the accepted senses
curl "http://localhost:3000/api/terms/kula/senses"

# 4. surface occurrences (substring, honest)
curl "http://localhost:3000/api/terms/kula/occurrences?work_id=kramasadbhava"
```

**How to answer correctly:** the context bundle gives you the passage's `tracked_terms` (accepted senses) and the neighboring context. The occurrence search gives you *surface* hits — say they are substring hits, not lemma evidence. Cite the work + passage + edition.

## What you must NEVER do

- Report a `machine_proposed` resolver candidate as a confirmed identity.
- Present a term proposal as an accepted sense.
- Treat `verified: false` (un-audited seed) as audited.
- Present our `T1` working translation as peer-reviewed.
- Infer "this is trainable / redistributable" from `rights: unknown`.

---

**MCP (agent convenience layer):** the same operations as HTTP — `get_work`, `get_source_passage`, `get_passage_context`, `get_term_senses`, `get_manuscripts`, `search_passages`, `find_term_occurrences`, `concordance`. The MCP mirrors the API one-to-one; it is not a separate universe.
