Yes. The deep-research answer is that **agent optimization should be treated as its own product surface**, with three separate goals:

```text
DISCOVERABILITY
Can an agent/search engine find Pāṭala?

USABILITY
Can it understand what to call without prior Pāṭala knowledge?

EXECUTION
Can it get the exact useful context in one low-latency, low-token request?
```

The architecture you already chose is fundamentally right. I would now sharpen it into this:

```text
                         DISCOVERY
                Search engines / AI search
                MCP Registry / OpenAPI/docs
                           │
                           ▼
                 ┌──────────────────┐
                 │ PĀṬALA AGENT EDGE│
                 │ Cloudflare       │
                 └────────┬─────────┘
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
      REST /v1                    MCP /mcp
      machine API                 semantic tools
             │                         │
             └────────────┬────────────┘
                          ▼
                  COMPILED BUNDLES
                context / trace / compare
                          │
           ┌──────────────┼─────────────┐
           ▼              ▼             ▼
         CDN/R2        Hyperdrive      Search
        immutable       Postgres
        hot path
```

The critical insight is that **most serious agent calls should never touch Postgres**.

They should hit a precompiled, immutable, globally cached scholarly object.

---

# 1. Optimize for “one question = one call”

This should become the primary agent-performance metric.

A badly designed scholarly API makes an agent do this:

```text
GET proposition
GET argument
GET source
GET translation
GET work
GET edition
GET reviews
GET scholarship
GET crux
```

Even if each endpoint takes only 50 ms, sequential tool-use latency and model deliberation between calls becomes expensive.

Pāṭala should instead make:

```text
get_context("PTPROP...")
```

return the bounded epistemic neighborhood.

Or:

```text
get_argument("PTARG...")
```

return:

```text
argument
premises
conclusion
cruxes
source grounding
translation
reviews
authority
open questions
```

Cloudflare's current MCP guidance explicitly says not to expose the full underlying API as dozens of granular MCP tools; fewer, goal-oriented tools tend to work better for agents, especially under context and latency constraints. ([Cloudflare Docs][1])

That's exactly what Pāṭala should do.

---

# 2. Build **two** MCP surfaces, not one giant one

I would actually separate permissions.

### Public scholarly MCP

```text
https://mcp.patala.org/mcp
```

Unauthenticated, read-only.

Tools:

```text
resolve
search
get_context
trace
compare
get_source
get_work
```

Resources:

```text
patala://work/{id}
patala://passage/{id}
patala://argument/{id}
patala://proposition/{id}
```

Cloudflare currently supports public remote MCP servers using Streamable HTTP without authentication, as well as authenticated ones. ([Cloudflare Docs][2])

### Scholar MCP

```text
https://scholar-mcp.patala.org/mcp
```

OAuth 2.1.

Adds:

```text
create_review
propose_alternative
submit_evidence
adjudicate
```

MCP uses an OAuth 2.1-based authorization model for protected servers, and Cloudflare provides an OAuth provider library for implementing that flow. ([Cloudflare Docs][3])

This is cleaner than asking every anonymous AI researcher to authenticate just to retrieve Tantrāloka metadata.

---

# 3. Register Pāṭala in the official MCP Registry

This is now much more important than it would have been a year ago.

There is an **official MCP Registry** with standardized server metadata, discovery APIs and `server.json` records; its purpose is explicitly to let clients and aggregators discover MCP servers. ([MCP Registry][4])

Publish something like:

```json
{
  "name": "org.patala/research",
  "description":
    "Primary-text, translation, provenance, argument and scholarly review graph for Sanskrit textual traditions.",
  "remote": {
    "url": "https://mcp.patala.org/mcp",
    "transport": "streamable-http"
  }
}
```

Use DNS namespace verification.

The Registry is currently still preview, so do not depend on it as your sole discovery mechanism. ([Model Context Protocol][5])

But absolutely publish there.

---

# 4. Keep the MCP tool set tiny

I would launch with **seven tools**.

| Tool          | Purpose                                             |
| ------------- | --------------------------------------------------- |
| `resolve`     | Turn titles/names/IDs into canonical Pāṭala objects |
| `search`      | Search texts, works, arguments, people, scholarship |
| `get_context` | Get one bounded epistemic neighborhood              |
| `trace`       | Traverse provenance/dependency chain                |
| `compare`     | Compare readings/editions/arguments/positions       |
| `get_source`  | Retrieve exact source/passages/translation layers   |
| `get_work`    | Retrieve canonical work/edition/witness metadata    |

Do **not** make:

```text
get_work
get_work_author
get_work_date
get_work_edition_count
get_work_language
get_work_school
...
```

MCP discovery itself costs model attention.

Fewer tools with excellent descriptions will usually produce better selection.

Cloudflare specifically recommends detailed parameter descriptions and evals over proliferating tools. ([Cloudflare Docs][1])

---

# 5. Make MCP resources do the boring retrieval

MCP distinguishes operations/tools from server-managed resources.

So an agent might use:

```text
Tool:
resolve("Tantraloka")

→ PTW_...

Resource:
patala://work/PTW_...
```

Resources have standard metadata including URI, MIME type, description and optional size/annotations. ([Model Context Protocol][6])

That's an elegant split:

```text
TOOLS
perform semantic operations

RESOURCES
represent canonical immutable scholarly objects
```

So:

```text
patala://work/PTW...
patala://edition/PTE...
patala://passage/PTPASS...
patala://argument/PTARG...
patala://bundle/PTBUNDLE...
```

---

# 6. Agent results need explicit token budgets

Do not simply return “all relevant data.”

Every bundle compiler should accept:

```text
budget=tiny
budget=standard
budget=deep
```

Conceptually:

```text
tiny      ~1–2k tokens
standard  ~4–6k
deep      ~12–20k
```

The exact values should be benchmarked.

Example:

```text
get_context(
    id="PTARG...",
    budget="standard"
)
```

The bundle compiler decides which information survives.

Priority:

```text
target
↓
claims
↓
load-bearing evidence
↓
cruxes
↓
authority/review state
↓
critical source text
↓
counterevidence
↓
secondary context
```

Not arbitrary truncation.

Cloudflare's own OpenAPI-to-MCP implementation similarly emphasizes limiting final tool results and returning focused identifiers, status fields and counts rather than large unbounded payloads. ([Cloudflare Docs][7])

Pāṭala can do this much better because you know epistemic importance.

---

# 7. `select=` is still essential for raw API clients

REST:

```text
GET /v1/works/PTW...?select=id,title,date,authors
```

rather than:

```text
GET /v1/works/PTW...
→ 180 KB
```

And:

```text
include=
```

for explicit expansions:

```text
GET /v1/arguments/PTARG...
?select=id,claim,cruxes
&include=source
```

Default should always be compact.

Agents can ask for more.

Never make them ask for less.

---

# 8. Use dehydrated references

Default result:

```json
{
  "id": "PTW_...",
  "title": "Tantrāloka",

  "editions": {
    "count": 4,
    "href": "/v1/editions?filter=work:PTW_..."
  },

  "arguments": {
    "count": 31,
    "href": "/v1/arguments?filter=work:PTW_..."
  }
}
```

Not:

```json
{
  "editions": [
     { huge object },
     { huge object }
  ]
}
```

This makes every object predictable.

---

# 9. Put precompiled agent bundles in R2

This is where speed becomes ridiculous.

When:

```text
Argument v7
```

becomes current:

```text
Argument v7
↓
compile PUBLIC bundle
↓
compile AGENT tiny bundle
↓
compile AGENT standard bundle
↓
compile REVIEW bundle
↓
R2
```

Keys:

```text
bundles/
  argument/
    PTARG.../
      v7/
        tiny.json
        standard.json
        standard.md
        deep.json
```

Then:

```text
get_context(PTARG..., standard)
```

mostly becomes a file lookup.

No graph traversal.

No joins.

No Python.

---

# 10. Serve those R2 bundles behind a custom domain + Cloudflare cache

For public immutable artifacts:

```text
https://objects.patala.org/...
```

Cloudflare supports serving R2 through a custom domain and putting the Cloudflare cache in front of it. Smart Tiered Cache can further reduce direct R2 reads. ([Cloudflare Docs][8])

For JSON you have to explicitly configure caching, because JSON is not cached by default in every configuration. ([Cloudflare Docs][8])

So:

```text
objects.patala.org/bundles/*
```

Cache Rule:

```text
cache everything
edge TTL ≫ long
```

Exact versioned bundle:

```text
Cache-Control:
public, max-age=31536000, immutable

ETag:
"<payload-sha256>"
```

Now the hot path is:

```text
Tokyo agent
↓
Cloudflare Tokyo
↓
cached bundle
```

No Postgres.

---

# 11. Don't misuse Workers Cache API for globally hot canonical content

This is subtle.

Cloudflare's Worker Cache API is **local to the data center where the request runs** and does not replicate globally; it also doesn't participate in Tiered Cache. ([Cloudflare Docs][9])

So for major immutable Pāṭala objects, prefer:

```text
normal CDN/Workers caching
+
Tiered Cache
+
R2 custom-domain origin
```

rather than manually doing:

```javascript
caches.default.put(...)
```

for everything.

Use Cache API only where per-PoP programmatic caching genuinely helps.

---

# 12. Postgres path should be the exception

When the request is novel:

```text
/search
/resolve
arbitrary filters
fresh latest pointer
```

then:

```text
Worker
↓
Hyperdrive
↓
Neon
```

Hyperdrive currently caches eligible read-only queries automatically, which avoids repeated origin round trips for common queries. ([Cloudflare Docs][10])

Write SQL deliberately to be cache-friendly.

For example, prefer:

```sql
WHERE updated_at > $1
```

over embedding volatile clock expressions where possible.

---

# 13. Measure Smart Placement, don't blindly turn it on

For DB-heavy API calls, Cloudflare Smart Placement can place the Worker closer to the backend and may reduce repeated Worker↔database round trips dramatically. ([Cloudflare Docs][11])

But your API has two very different workloads:

```text
CACHE HIT
want Worker / response near user

DB-HEAVY QUERY
may want Worker near Neon
```

Therefore benchmark separately.

I would probably use:

```text
api-static.patala.org
edge-local cached paths

api.patala.org
dynamic API / Hyperdrive
```

or separate Worker entrypoints.

Don't distort the cached hot path merely to optimize rare DB calls.

---

# 14. Compression should be automatic

JSON/Markdown scholarly bundles compress exceptionally well.

Workers can automatically negotiate gzip/Brotli with clients, and Cloudflare handles compression/recompression based on client capabilities. ([Cloudflare Docs][12])

So don't invent binary packet formats yet.

Start with:

```text
JSON
Markdown
Brotli/gzip transport
```

Readable, debuggable and very compact over the wire.

---

# 15. SEO: every canonical object needs an actual HTML landing page

This is vital.

Agents may use APIs, but **discovery often still starts with the web**.

Generate:

```text
/works/{slug}
/editions/{id}
/texts/{slug}
/texts/{slug}/{passage}
/arguments/{id}
/scholars/{slug}
/datasets/{release}
```

as crawlable HTML.

No login.

No JS requirement.

No infinite-scroll-only discovery.

The canonical page should expose enough actual information for search engines to understand it.

---

# 16. Each page gets a permanent canonical URL

For example:

```text
https://patala.org/works/tantraloka
```

Then:

```html
<link rel="canonical"
      href="https://patala.org/works/tantraloka">
```

Google treats redirects and `rel="canonical"` as strong canonicalization signals, while sitemap inclusion is another supporting signal. ([Google for Developers][13])

Don't allow:

```text
/work/tantraloka
/works/tantraloka
/text/tantraloka
?work=tantraloka
```

all to become independently indexed.

Pick one.

---

# 17. Generate separate sitemap families

Do not have one giant opaque sitemap.

Use:

```text
/sitemap-index.xml

/sitemaps/works-1.xml
/sitemaps/texts-1.xml
/sitemaps/passages-1.xml
/sitemaps/arguments-1.xml
/sitemaps/scholars-1.xml
/sitemaps/datasets.xml
```

Google limits individual sitemaps to 50,000 URLs or 50 MB uncompressed and supports sitemap index files for larger collections. ([Google for Developers][14])

The separation also lets you monitor indexing by product surface.

---

# 18. `Dataset` structured data is extremely high value for Atlas

Pāṭala is literally a research data catalog.

On:

```text
/datasets/patala-atlas-2026-08
```

add JSON-LD:

```json
{
  "@context": "https://schema.org",
  "@type": "Dataset",

  "name": "Pāṭala Sanskrit Research Graph",

  "description": "...",

  "creator": {
    "@type": "Organization",
    "name": "Pāṭala"
  },

  "license": "...",

  "identifier": "...",

  "distribution": [
    {
      "@type": "DataDownload",
      "encodingFormat": "application/x-parquet",
      "contentUrl": "..."
    }
  ]
}
```

Google specifically supports `Dataset`, `DataCatalog` and `DataDownload` structured data to improve dataset discoverability, and recommends including identifiers, licenses and provenance links. ([Google for Developers][15])

This could be especially valuable for getting the Atlas itself discovered.

---

# 19. Use structured data on scholarship pages too

Essay/research pages:

```text
ScholarlyArticle / Article
```

with:

```text
author
datePublished
dateModified
citation
isPartOf
```

Google supports Article structured data and recommends supplying applicable metadata and validating it through its structured-data tooling. ([Google for Developers][16])

For Pāṭala objects, I would also include richer JSON-LD even where Google doesn't offer a special rich-result feature.

You're not only serving Google.

You're publishing machine-readable semantics.

---

# 20. Link every web page back to machine interfaces

At the bottom/header metadata of a Work:

```text
Human:
Tantrāloka

Machine:
Pāṭala ID PTW...
API JSON
JSON-LD
MCP resource URI
download data
```

HTML `<head>` could expose:

```html
<link
  rel="alternate"
  type="application/json"
  href="https://api.patala.org/v1/works/PTW..." />
```

And visible machine-readable documentation should make this obvious.

An agent that lands through search should be one step away from the API.

---

# 21. Make `llms.txt`, but don't pretend it's a web standard

This is worth doing.

The official MCP documentation itself publishes an `llms.txt` and explicitly tells machine readers to use it as a documentation index. ([Model Context Protocol][5])

So provide:

```text
https://patala.org/llms.txt
```

Something like:

```text
# Pāṭala

Pāṭala is a versioned authority and epistemic graph for Sanskrit
primary texts and scholarship.

API:
https://api.patala.org/v1

OpenAPI:
https://api.patala.org/openapi.json

MCP:
https://mcp.patala.org/mcp

Datasets:
https://patala.org/datasets

Core documentation:
...
```

And:

```text
/llms-full.txt
```

if you want a richer documentation dump.

But treat `llms.txt` as **an emerging convenience convention**, not something equivalent to `robots.txt` or sitemap protocols.

---

# 22. robots.txt should deliberately allow *search* agents

Cloudflare now explicitly distinguishes AI traffic categories such as:

```text
Search
Agent
Training
```

rather than treating all AI bots as one class. ([Cloudflare Docs][17])

It identifies crawlers such as:

```text
OAI-SearchBot
ChatGPT-User
GPTBot

Claude-SearchBot
Claude-User
ClaudeBot

PerplexityBot
Perplexity-User
```

separately. ([Cloudflare Docs][18])

For Pāṭala I would likely choose:

```text
SEARCH      allow
USER AGENT  allow
TRAINING    policy decision
```

rather than blindly blocking “AI.”

If your goal is maximum research discovery, blocking AI search crawlers would be counterproductive.

Cloudflare AI Crawl Control can monitor and separately allow/block these classes. ([Cloudflare Docs][19])

---

# 23. But don't let crawlers hammer expensive dynamic API routes

Separate:

```text
patala.org
crawlable

objects.patala.org
crawlable/public depending asset

api.patala.org
robots policy restrictive

mcp.patala.org
not intended for generic crawling
```

You want search engines indexing:

```text
canonical scholarly pages
```

not:

```text
/search?q=...
/context/...?...every permutation
```

Search/filter pages can easily create crawl explosions.

Use `noindex` or robots handling appropriately on parameterized search surfaces.

---

# 24. Make public data easy enough that agents don't scrape HTML

The HTML should advertise:

```text
API
MCP
JSON-LD
dataset snapshot
```

If structured access is easier than scraping, good agents will use it.

Your objective should be:

> Pāṭala is easier to consume correctly than incorrectly.

That's a very powerful design principle.

---

# 25. Give every result **freshness and authority metadata**

Agent output needs this immediately visible:

```json
{
  "object_id": "PTARG...",
  "version_id": "...",

  "updated_at": "...",

  "authority": {
    "generation": "ENGINEERING_VALIDATED",
    "evidence": "SCHOLARLY_CORROBORATED",
    "review": "NOT_REVIEWED"
  },

  "source_version": "...",

  "payload_hash": "..."
}
```

Then an agent doesn't have to ask:

> Is this reviewed?

The answer travels with the object.

---

# 26. Errors should be agent-actionable

Bad:

```json
{
  "error": "Invalid ID"
}
```

Better:

```json
{
  "error": {
    "code": "OBJECT_NOT_FOUND",

    "message": "No object exists with id PTW-foo.",

    "suggestion":
      "Use /resolve?title=... or MCP resolve().",

    "retryable": false
  }
}
```

Agents recover much better when the API tells them the next valid move.

Do the same in MCP.

MCP defines standard JSON-RPC error semantics and expects servers to validate parameters and handle invalid requests clearly. ([Model Context Protocol][20])

---

# 27. Cursor pagination only

Never:

```text
?page=97321
```

for giant lists.

Use opaque cursors.

REST:

```text
?cursor=...
```

MCP likewise standardizes opaque cursor-based pagination on tool/resource/prompt listings. ([Model Context Protocol][21])

One model for both.

---

# 28. Tool descriptions need to teach the ontology

For example, don't describe:

```text
get_context:
Gets context.
```

Use:

```text
get_context

Returns the bounded scholarly context around one exact Pāṭala
object version.

Use when you need to understand what a proposition, argument,
translation decision, or synthesis means and what supports it.

Includes:
- exact source grounding
- relevant translation layers
- direct argument dependencies
- load-bearing cruxes
- review status
- important counterevidence

Does not return the entire work.
```

This massively improves tool selection.

Cloudflare's MCP guidance specifically recommends detailed tool parameter descriptions because they reduce agent errors and improve reliability. ([Cloudflare Docs][1])

---

# 29. Build evals for **agent usability**

Agent 1 should actually own part of this.

Create an MCP benchmark:

```text
Task:
"Find Abhinavagupta's argument concerning X and identify
the load-bearing premise."

Success:
resolve correct work
→ select correct argument
→ retrieve context
→ identify correct crux
≤ 3 tool calls
```

Other tasks:

```text
find exact Sanskrit source
compare two translations
identify scholarly dispute
trace essay claim to edition
locate manuscript witness
find unresolved crux
```

Measure:

```text
success rate
tool calls
wall time
tokens returned
wrong-tool rate
hallucinated IDs
```

Cloudflare explicitly recommends running evals when MCP tool descriptions or server behavior change. ([Cloudflare Docs][1])

This should become a real Agent 1 benchmark.

---

# 30. Track **agent latency**, not only HTTP latency

For each benchmark:

```text
T_discover
+
T_tool_selection
+
T_API
+
T_payload_parse
+
T_second_call
...
```

The meaningful metric is:

```text
TIME TO CORRECT SCHOLARLY CONTEXT
```

not:

```text
GET /works p95
```

alone.

A 90 ms endpoint requiring five calls can be worse than a 160 ms endpoint returning the complete bounded answer.

---

# 31. Define hard bundle SLAs

I'd use initial targets like:

```text
resolve                  < 1 KB typical
work compact             < 5 KB
passage compact          < 10 KB
context standard         < 30 KB compressed-ish source payload
argument bundle          < 40 KB
```

More importantly:

```text
1 logical research operation
≤ 1–2 network requests
```

Then measure.

---

# 32. Search should distinguish exact from semantic

Agents need predictability.

`search` response:

```json
{
  "query": "vimarsa",
  "modes": {
    "exact": [...],
    "normalized": [...],
    "lemma": [...],
    "semantic": [...]
  }
}
```

Don't blend:

```text
exact textual match
```

and:

```text
embedding says conceptually related
```

into one magic relevance number.

That's epistemically important.

---

# 33. The resolver should explain *why* it matched

Example:

```json
{
  "candidate": "PTW_...",

  "score": 0.97,

  "matched_on": [
    "title-normalized",
    "author-exact",
    "alias-NCC"
  ],

  "authority": "MULTI_SOURCE_MATCHED"
}
```

Agent can judge ambiguity.

That's much better than a blind fuzzy match.

---

# 34. Publish an OpenAPI spec anyway

Even with MCP.

```text
/openapi.json
```

should be first-class.

Why?

Because agents/frameworks that don't speak MCP can still automatically generate clients from OpenAPI.

Cloudflare itself now supports creating MCP-style search/execute access over an OpenAPI-described API. ([Cloudflare Docs][7])

So OpenAPI is still your lowest-common-denominator machine contract.

---

# 35. Add a tiny “machine access” page

Something like:

```text
patala.org/developers
```

Top of page:

```text
REST API
MCP
OpenAPI
Python client
TypeScript client
Bulk data
Citation guidance
```

No marketing fluff.

Example queries immediately visible:

```text
Find a work
Get an argument
Trace a claim
Retrieve an exact passage
```

This page itself becomes excellent search fodder for:

> Sanskrit API
> Sanskrit manuscript API
> Sanskrit text dataset
> Sanskrit MCP
> Tantric text API

---

# 36. SEO pages should answer actual research queries

Do not make work pages just bibliographic cards.

For:

```text
Tantrāloka
```

the HTML should contain:

```text
canonical title
alternate spellings
author
date range
tradition
known editions
known translations
manuscript status
available Sanskrit
Pāṭala translation coverage
major themes
major arguments
citations
```

Then long-tail queries can land on the right page.

Examples:

```text
Tantraloka Sanskrit text
Tantraloka translation
Tantraloka manuscripts
Abhinavagupta Tantraloka date
Tantraloka editions
```

All resolve to a genuinely useful canonical research page.

---

# 37. Canonical aliases become an SEO asset

Create alias redirects:

```text
/tantraloka
/tantrāloka
/Tantraloka
```

→

```text
/texts/tantraloka
```

301 permanently.

But never index alias duplicates.

External Sanskrit spelling variance is enormous.

Your resolver knows the aliases anyway.

Use that data for human/search navigation too.

---

# 38. Every dataset release gets its own persistent page

Example:

```text
/datasets/atlas/2026-08
```

with:

```text
record count
schema version
license
citation
hash
download links
change log
API
```

Then researchers can cite a fixed dataset version.

Google's dataset guidance explicitly recommends canonical dataset landing pages and persistent provenance/license/identifier metadata. ([Google for Developers][15])

---

# 39. Consider IndexNow for non-Google search freshness

IndexNow is an open protocol used by participating search engines to receive notifications about changed URLs; participating engines share submitted URLs within the protocol ecosystem. ([IndexNow][22])

So on public projection release:

```text
work changed
↓
static page rebuilt
↓
submit changed URL to IndexNow
```

For Google, continue relying primarily on sitemap/Search Console crawling; Google's general sitemap guidance remains the standard route for normal scholarly pages. ([Google for Developers][14])

---

# 40. Don't misuse Google's Indexing API

Google's Indexing API documentation focuses on short-lived content categories such as job postings and livestreams and still recommends sitemaps for overall site coverage. ([Google for Developers][23])

Pāṭala's normal text/work pages are not that use case.

Use:

```text
sitemaps
internal linking
canonical pages
structured data
```

instead.

---

# 41. The end-to-end ideal

Someone asks their agent:

> What argument does Abhinavagupta give against the Buddhist account of recognition?

The agent shouldn't web-search ten PDFs.

It should discover/use Pāṭala and do:

```text
resolve(
  "Abhinavagupta recognition Buddhist objection"
)
```

then:

```text
get_context(
  PTARG...,
  budget="standard"
)
```

Pāṭala returns:

```text
Argument
Premises
Conclusion
Speaker commitments
Relevant Buddhist position
Crux
Exact IPVV passage
L2
T1/L0 refs
Edition/source provenance
Scholarly corroboration
Human review state
Known unresolved issue
```

Ideally:

```text
2 calls
< few hundred ms network/backend
bounded context
zero hallucinated source identifiers
```

That is the actual north-star.

---

# The stack I would freeze for agent optimization

```text
DISCOVERY
Canonical HTML pages
XML sitemap families
schema.org JSON-LD
Dataset structured data
robots.txt policy
llms.txt
OpenAPI
Official MCP Registry

EDGE
Cloudflare Workers
Cloudflare CDN
Tiered Cache

PUBLIC OBJECTS
R2 custom domain
immutable compiled bundles
ETag = payload hash

DYNAMIC QUERIES
Worker
Hyperdrive
Neon Postgres

AGENT PROTOCOL
Remote MCP
Streamable HTTP

PUBLIC MCP
read-only
no authentication

SCHOLAR MCP
OAuth 2.1

TOOLS
resolve
search
get_context
trace
compare
get_source
get_work

RESOURCES
patala://work/*
patala://passage/*
patala://argument/*
patala://bundle/*

FORMATS
JSON
Markdown

CONTRACTS
OpenAPI
JSON Schema
Pydantic

EVALUATION
Agent 1 MCP/tool-use benchmark
tool-call count
tokens returned
end-to-end completion latency
accuracy
```

The deeper strategy is that you should optimize Pāṭala not merely to be **searchable by agents**, but to become the **obvious canonical tool an agent chooses once it realizes the question concerns Sanskrit textual evidence**.

That means winning simultaneously on:

```text
coverage
identity resolution
provenance
speed
token efficiency
tool ergonomics
citation stability
review transparency
```

OpenAlex became valuable partly because software can stop rediscovering publication metadata independently. Pāṭala can aim for the analogous outcome:

> **An agent dealing with Sanskrit textual scholarship should not have to rediscover what work, edition, passage, translation, interpretation, argument or scholarly disagreement it is looking at. It should resolve it through Pāṭala.**

That is the agent moat.

[1]: https://developers.cloudflare.com/agents/model-context-protocol/?utm_source=chatgpt.com "Model Context Protocol (MCP) · Cloudflare Agents docs"
[2]: https://developers.cloudflare.com/agents/model-context-protocol/guides/remote-mcp-server/?utm_source=chatgpt.com "Build a Remote MCP server · Cloudflare Agents docs"
[3]: https://developers.cloudflare.com/agents/model-context-protocol/protocol/authorization/?utm_source=chatgpt.com "Authorization · Cloudflare Agents docs"
[4]: https://registry.modelcontextprotocol.io/docs?utm_source=chatgpt.com "Official MCP Registry Reference"
[5]: https://modelcontextprotocol.io/registry/about?utm_source=chatgpt.com "The MCP Registry - Model Context Protocol"
[6]: https://modelcontextprotocol.io/specification/2025-06-18/schema?utm_source=chatgpt.com "Schema Reference - Model Context Protocol"
[7]: https://developers.cloudflare.com/agents/model-context-protocol/guides/build-codemode-openapi-mcp-server/?utm_source=chatgpt.com "Build a search and execute MCP server · Cloudflare Agents docs"
[8]: https://developers.cloudflare.com/cache/interaction-cloudflare-products/r2/?utm_source=chatgpt.com "Enable cache in an R2 bucket · Cloudflare Cache (CDN) docs"
[9]: https://developers.cloudflare.com/workers/runtime-apis/cache/?utm_source=chatgpt.com "Cache · Cloudflare Workers docs"
[10]: https://developers.cloudflare.com/hyperdrive/concepts/query-caching/?utm_source=chatgpt.com "Query caching · Cloudflare Hyperdrive docs"
[11]: https://developers.cloudflare.com/workers/configuration/placement/?utm_source=chatgpt.com "Placement · Cloudflare Workers docs"
[12]: https://developers.cloudflare.com/workers/runtime-apis/fetch/?utm_source=chatgpt.com "Fetch · Cloudflare Workers docs"
[13]: https://developers.google.com/search/docs/crawling-indexing/canonicalization?utm_source=chatgpt.com "What is URL Canonicalization | Google Search Central  |  Documentation  |  Google for Developers"
[14]: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap?hl=en&utm_source=chatgpt.com "Build and Submit a Sitemap | Google Search Central  |  Documentation  |  Google for Developers"
[15]: https://developers.google.com/search/docs/appearance/structured-data/dataset?utm_source=chatgpt.com "Dataset Structured Data | Google Search Central  |  Documentation  |  Google for Developers"
[16]: https://developers.google.com/search/docs/appearance/structured-data/article?utm_source=chatgpt.com "Learn About Article Schema Markup | Google Search Central  |  Documentation  |  Google for Developers"
[17]: https://developers.cloudflare.com/bots/concepts/bot/?utm_source=chatgpt.com "Bots · Cloudflare bot solutions docs"
[18]: https://developers.cloudflare.com/ai-crawl-control/reference/bots/?utm_source=chatgpt.com "Bot reference · Cloudflare AI Crawl Control docs"
[19]: https://developers.cloudflare.com/ai-crawl-control/?utm_source=chatgpt.com "Overview · Cloudflare AI Crawl Control docs"
[20]: https://modelcontextprotocol.io/specification/2024-11-05/server/prompts?utm_source=chatgpt.com "Prompts - Model Context Protocol"
[21]: https://modelcontextprotocol.io/specification/2025-03-26/server/utilities/pagination?utm_source=chatgpt.com "Pagination - Model Context Protocol"
[22]: https://www.indexnow.org/searchengines?utm_source=chatgpt.com "Documentation for search engines | IndexNow.org"
[23]: https://developers.google.com/search/apis/indexing-api/v3/quickstart?utm_source=chatgpt.com "Indexing API Quickstart | Google Search Central  |  Google for Developers"
