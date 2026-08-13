# Pāṭala Access Policy — public discovery ≠ public corpus

*2026-08-13. The access-tiering + crawler policy. Complements `docs/api/concepts/rights.md` (the
per-resource permission matrix) with the **product-level access tiers** and the **AI-crawler policy**.*

## The correction

> **Pāṭala should be an open scholarly index and protocol, with selectively open content and controlled
> access to high-value derived data.**

This revises the earlier "entirely open data infrastructure" framing. Make the **ontology, catalog,
identifiers, discovery layer** public; make the **deep epistemic content** available through controlled
Pāṭala access. Discoverability without commoditizing the asset.

## Public vs controlled

```text
PUBLIC (discovery, indexable, crawlable)
├─ work / author / edition metadata
├─ identifiers + provenance summaries
├─ short preview passages
├─ dataset / schema documentation
├─ API / MCP documentation
├─ public essays / education you intentionally publish
└─ SEO landing pages

CONTROLLED (valuable substrate, authenticated/quota'd)
├─ full Sanskrit corpus
├─ full translations
├─ T1/L0/L200/C1
├─ full argument graph
├─ scholarly bundles
├─ bulk exports
└─ high-value agent context
```

## The tiered API design

```text
api.patala.org/v1/public/*      — NO key: resolve work, work/edition metadata, bibliographic search,
                                  authority summaries, small previews, public reviews
api.patala.org/v1/research/*    — API key / OAuth: full passages, translations, argument bundles,
                                  context bundles, trace, comparison, scholar evidence
api.patala.org/v1/bulk/*        — explicit agreement / paid / scholar: bulk corpus, snapshots,
                                  entire translations, large graph exports
```

MCP follows the same design:

```text
mcp.patala.org          → public discovery MCP (read-only)
research-mcp.patala.org → authenticated high-value scholarly MCP
```

## AI-crawler policy (Cloudflare fine-grained controls)

Cloudflare distinguishes **Search / Agent / Training** and the specific bots. Recommended Pāṭala policy:

```text
TRAINING CRAWLERS        GPTBot · ClaudeBot · CCBot · Bytespider · …      → BLOCK
SEARCH CRAWLERS          OAI-SearchBot · Claude-SearchBot · PerplexityBot ·
                         Googlebot · BingBot                              → ALLOW on public discovery pages
USER-INITIATED AGENTS    ChatGPT-User · Claude-User · Perplexity-User     → ALLOW public pages
                                                                          → authenticated API for valuable corpus
```

Blocking `ClaudeBot` signals exclusion from training datasets while user/search agents serve different
purposes — that separation is exactly what we want.

## CRITICAL: robots.txt is not a security boundary

Empirical research shows AI assistants vary in how reliably they respect `robots.txt`, especially for
inference-time retrieval. **If something is moat data, protect it with authentication / WAF / object
permissions — not `Disallow: /`.**

```text
R2 private
↓ Worker authentication
↓ entitlement / quota
↓ cache keyed appropriately
↓ bundle
```

Public **metadata** bundles can remain public + edge-cached. High-value **content** bundles must NOT be at
stable unauthenticated URLs.

## The product possibility

> Make Pāṭala **maximally indexable at the metadata level** while **forcing deep use through Pāṭala at
> inference time**.

```text
Google / ChatGPT Search sees:
  Tantrāloka · Abhinavagupta · ~10th/11th c.
  4 known editions · 31 structured arguments
  translation coverage 87% · 12 human-reviewed decisions
  "Access full scholarly context via Pāṭala"
```

That creates demand for the API instead of giving the dataset away.

## What stays open-source

```text
schemas · identifiers · API spec · evaluation methodology
client SDKs · selected benchmarks · public-domain source metadata
```

## What is a controlled asset

```text
large curated translation corpus · verified argument graph
expert corrections · full review bundles · premium bulk data
```

## Caveats

- Blocking crawlers doesn't prevent a model from learning facts that appear elsewhere.
- You can't retroactively control data already copied/published.
- But for **future Pāṭala-generated material**, this gives strong control over large-scale automated
  acquisition.

## Enforcement (Cloudflare)

- **AI Crawl Control** — allow/block by Search / Agent / Training class.
- **WAF rules** — path-specific exceptions: allow AI Search on `/works/*`, block training access to
  `/texts/full/*` or `/api/research/*`.

## Relation to the rights matrix

The per-resource `rights` matrix (`api/concepts/rights.md`: `api_fulltext`, `model_training`, `rag`, …)
decides **what may be done with a resource**. This policy decides **who can reach it and at what tier**.
The two work together: rights = the license/entitlement; access tiers = the delivery gate.
