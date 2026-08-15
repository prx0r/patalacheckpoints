Yes. There is substantially more free/near-free inference available than the usual OpenRouter + Workers AI list suggests.

I went looking specifically for **recurring free quotas, weird subsidized gateways, developer programs, anonymous endpoints, recurring GPU credits, decentralized inference, temporary promos, and machine-readable sources you can monitor**.

**Snapshot: August 16, 2026.** These offers change quickly, so I’d build a live registry rather than a static bookmarks file.

## The finds I would exploit first

### 1. Kilo Gateway / `kilo-auto/free` — possibly the best overlooked free router

This one is excellent.

Kilo currently offers:

* `kilo-auto/free`
* **$0**
* **200 requests/hour per IP**
* no credits required
* automatically rotates/routs between whatever good free models are currently available
* OpenAI-compatible gateway API

Kilo explicitly says the free pool is dynamically updated as providers change their promos. That means **they are already doing part of your scavenging for you**. ([Kilo][1])

The API pattern is:

```text
POST https://api.kilo.ai/api/gateway/chat/completions

model = kilo-auto/free
```

They also expose individual free models instead of forcing the router. Current examples have included Nemotron, StepFun, Laguna, Cohere North and OpenRouter free models. The catch is important: free upstreams may log/train on inputs, especially NVIDIA trial endpoints, so don't push confidential material through the free route. ([Kilo][2])

**Scavenger rating: 10/10.**

---

### 2. OpenCode Zen — temporary free frontier-ish endpoints

Your DeepSeek observation was correct.

OpenCode Zen currently has multiple **zero-price** promotional endpoints, including:

* DeepSeek V4 Flash
* MiMo-V2.5
* Hy3
* Laguna S 2.1
* Nemotron 3 Ultra
* Nemotron 3.5 Lightning
* Big Pickle

The promotions are explicitly temporary and exist partly to gather feedback/model-improvement data, so this should be treated as a rotating pool rather than infrastructure you depend on forever. ([OpenCode][3])

And importantly, they expose a model catalog:

```text
GET https://opencode.ai/zen/v1/models
```

That is exactly the kind of endpoint your deal hunter should poll.

**Scavenger rating: 10/10 while promos last.**

---

### 3. Z.AI / Zhipu — actual permanently free GLM APIs

This was one of the better niche finds.

Zhipu has an official **free-model family**, not just signup credits. Current offerings include:

* `GLM-4.7-Flash`
* `GLM-4.6V-Flash`
* `GLM-4.1V-Thinking-Flash`
* older GLM Flash models
* even some free image-generation/vision endpoints

GLM-4.7-Flash is explicitly described as the free version of GLM-4.7. ([BigModel Documentation][4])

Even more interesting: **GLM-4.6V-Flash is a free multimodal endpoint** accepting text, images, video and files with a 128K context window and function calling. ([BigModel Documentation][5])

OpenAI-ish endpoint:

```text
https://open.bigmodel.cn/api/paas/v4/chat/completions
```

**Scavenger rating: 10/10**, especially for multimodal jobs that would otherwise cost you money.

---

### 4. NVIDIA hosted NIM — enormous free prototyping catalog

NVIDIA Developer Program membership provides free access to hosted NIM endpoints for prototyping. NVIDIA also permits developers to self-host NIMs on up to 16 GPUs under its developer terms. ([NVIDIA Docs][6])

The current free catalog discovered by the community includes things as serious as:

* DeepSeek V4 Flash
* DeepSeek V4 Pro
* Nemotron 3 Ultra 550B
* Nemotron Super 120B
* GPT-OSS 120B
* MiniMax M3
* Mistral Medium 3.5
* Gemma 4 31B

The tracked rate is around **40 RPM**, although I would regard NVIDIA's official “free hosted prototyping” guarantee as authoritative and the precise RPM as something your canary tester should continually re-measure. ([GitHub][7])

API base:

```text
https://integrate.api.nvidia.com/v1
```

This is a particularly good target for bulk **non-sensitive experimentation**.

---

### 5. Groq free tier — probably the best predictable fixed quota

Groq remains ridiculously useful.

Current free limits include roughly:

* Llama 3.1 8B Instant: **14,400 requests/day**, 500K tokens/day
* Llama 3.3 70B: **1,000 requests/day**, 100K tokens/day
* GPT-OSS 120B: **1,000 requests/day**, 200K tokens/day
* GPT-OSS 20B: **1,000 requests/day**, 200K tokens/day
* Qwen 3.6 27B: **1,000 requests/day**, 200K tokens/day
* Groq Compound: 250 requests/day

Groq also exposes remaining/reset information through rate-limit response headers. ([GroqCloud][8])

For lots of small classification/extraction jobs, **14,400 8B calls/day is extremely useful**.

---

### 6. Cloudflare Workers AI

Still excellent:

**10,000 neurons/day free**, every day. Above that, Workers AI is currently $0.011/1,000 neurons. ([Cloudflare Docs][9])

Despite Cloudflare moving some models to paid-only access in July, the free plan still includes substantial models such as:

* GLM-4.7-Flash
* Gemma 4 26B
* Nemotron 3 120B

among others. ([Cloudflare Docs][10])

Cloudflare is particularly useful because you can put your entire router + state database + cron logic beside the inference layer.

---

### 7. OpenRouter free pool

Still worth maintaining as a fallback.

Current rule:

* without $10+ historical credit purchase: roughly **50 free-model requests/day**
* once you've purchased at least $10: **1,000 free-model requests/day**
* free model pool rotates

([OpenRouter][11])

And you can dynamically discover everything:

```text
GET https://openrouter.ai/api/v1/models
```

The official Models API returns normalized metadata, while the endpoint API can expose individual providers serving a given model. ([OpenRouter][12])

This means OpenRouter is as valuable as a **price-discovery database** as it is an inference endpoint.

---

### 8. OVHcloud anonymous inference — no account, no API key

This one is wonderfully scavenger-like.

OVHcloud AI Endpoints permits anonymous requests at:

**2 requests/minute, per IP, per model.**

No account/key required for that tier. Authenticated Public Cloud projects get much higher limits. ([OVHcloud Help][13])

The current catalog includes models such as Qwen 3.5 397B, GPT-OSS 120B/20B, Llama 3.3 70B and Qwen models. A community-maintained tracker lists this base:

```text
https://oai.endpoints.kepler.ai.cloud.ovh.net/v1
```

([GitHub][7])

At 2 RPM this isn't your primary chatbot backend, but it's **excellent for slow queues/background enrichment**.

Don't try to evade their quota with proxy/IP rotation—just treat the legitimate anonymous allowance as another worker lane.

---

### 9. ModelScope API-Inference

Another overlooked China-side source.

The current free API-Inference program is tracked at:

* **2,000 requests/day total**
* up to roughly **500/day per model**
* dynamic concurrency
* access to API-Inference-enabled Qwen and related models

It does require Alibaba Cloud binding and real-name verification. ([GitHub][7])

Base:

```text
https://api-inference.modelscope.cn/v1
```

For someone who can satisfy the normal account requirements, that's a substantial recurring quota.

---

### 10. SambaNova Cloud

Free tier is still useful, though request-count constrained.

Current free models include things like:

* DeepSeek V3.1
* DeepSeek V3.2 preview
* Llama 3.3 70B
* GPT-OSS 120B
* MiniMax M2.7

Typical free-model limit:

**20 RPM / 20 requests per day / ~200K tokens per day per model.** ([SambaNova Documentation][14])

So the trick here isn't lots of tiny requests—it's **20 chunky requests**.

---

### 11. Mistral Experiment / Free mode

Mistral still provides API access in its free/Experiment mode without needing a paid subscription. Limits are exposed through the account dashboard and can vary rather than being one simple universal number. ([Mistral AI Documentation][15])

This is particularly useful for **Codestral** and as BYOK for products such as Kilo. Kilo itself recommends Mistral's free tier for zero-cost autocomplete. ([Kilo][2])

---

### 12. Gemini Developer API

There are still free-tier Gemini models, particularly Flash-family models, but Google has made the quotas increasingly model/account/project-specific. RPD resets at midnight Pacific, and AI Studio is now the reliable place to see your active quota rather than assuming an old blog's numbers remain correct. ([Google AI for Developers][16])

One caveat: free-tier API data may be used by Google to improve products, whereas paid-tier handling differs. ([Google AI for Developers][17])

Also, Gemini API usage is no longer something I'd try to fund through the generic $300 Google Cloud trial; Google changed that situation in 2026. ([Google AI for Developers][18])

---

### 13. Cohere trial API

Cohere remains useful for free experimentation. Trial API keys have their own limits, and its current Command family—including Command A+—can be accessed without normal production billing until the applicable trial limits are hit. ([Cohere Documentation][19])

A current community tracker records roughly **1,000 API calls/month** for the non-commercial trial tier. ([GitHub][7])

I'd use it for semantic/RAG experiments rather than build a commercial workload around the trial.

---

### 14. Ollama Cloud free tier

Ollama Cloud now has a free “light usage” tier, including cloud models rather than requiring your own machine. It measures usage more qualitatively/by compute/session limits rather than publishing a nice token/day number. Current tracked cloud models include DeepSeek V4, MiniMax, Kimi, GPT-OSS, Nemotron and Qwen. ([GitHub][7])

Worth probing. Don't build assumptions around an unpublished quota.

---

### 15. LLM7.io — bizarre no-registration gateway

A current open-source free-API registry has LLM7 at:

* no registration for basic access
* around 30 models
* approximately **30 RPM anonymous**
* approximately 120 RPM with a token

and models including DeepSeek, Gemini Flash Lite, GPT-4o-mini, Mistral and Qwen. ([GitHub][7])

Base:

```text
https://api.llm7.io/v1
```

This is one I would classify as **“probe it and never send secrets”**, rather than entrusting production infrastructure to it.

---

### 16. Aion Labs

Another small provider that doesn't appear in most lists.

Its current free tier is tracked as:

* no card
* **15 RPM**
* **20K tokens/day**
* Aion 2.5 / 3.0 family

([GitHub][7])

More specialized toward storytelling/roleplay, so less interesting for your coding/research agents, but free compute is free compute.

---

### 17. Hugging Face

The ordinary free Inference Providers allowance has become tiny:

**$0.10/month** for Free accounts. ([Hugging Face][20])

But the hidden better deal is **ZeroGPU**. Qualifying free HF accounts can currently host up to **two ZeroGPU Spaces**. ([Hugging Face][21])

For bursty demos or your own Gradio-powered inference tools, this is much more interesting than the $0.10 router allowance.

---

### 18. Together's literally $0 model

Together added:

**Prism-ML/Ternary-Bonsai-27B — $0 inference**

to serverless in August 2026. It has a 262K context window. ([Together AI docs][22])

Catch: Together's current serverless account flow may require an initial **$5 credit purchase** even where the model itself costs $0.

Still worth putting in the registry.

---

### 19. SiliconFlow

SiliconFlow's Chinese platform has a set of genuinely free models after the required identity/account setup. Their documentation distinguishes free model IDs from paid `Pro/` variants. ([SiliconFlow][23])

International SiliconFlow is less exciting: more of a starter-credit proposition; current international signup messaging has advertised roughly $1 starting credit. ([SiliconFlow][24])

---

## The recurring-GPU-credit loophole

This is arguably **more valuable than hunting token quotas** because you can run whatever open model you want.

### Modal: $30 every month

Starter is $0 and gives **$30/month of free compute**, including GPU workloads, 10 GPU concurrency and serverless web functions. ([Modal][25])

That means you could deploy a quantized model behind your own API and let scale-to-zero make the $30 stretch.

### Beam: another $30 every month

Beam independently gives **$30 free credit every month**. It has serverless GPUs and on-demand hardware; current advertised H100 on-demand pricing starts around $1.74/hour. ([Beam Cloud][26])

So:

> Modal $30/month + Beam $30/month = **$60 recurring compute/month** before touching token APIs.

That's one of the biggest discoveries in this whole search.

### Lightning

Lightning currently has a smaller recurring free-credit allocation and free CPU resources, with additional academic programs available in some cases. ([Lightning AI][27])

I'd rank it below Modal/Beam, but monitor it.

---

# The “developer pays $0 forever” category

These aren't normal free APIs, but economically they're even better.

### Puter.js

Puter uses a **User-Pays** model.

You embed AI into your web app; your developer account does **not** pay the inference bill. Each user's own Puter allowance/account bears their usage. ([Puter Developer][28])

For a public research/product site this can turn:

> 10,000 users × inference usage = horrifying API bill

into:

> developer inference expense ≈ $0.

Very different architecture, but extremely powerful.

### WebLLM

WebLLM runs open models **inside the user's browser via WebGPU** and provides an OpenAI-like API. The inference never needs your server. ([WebLLM][29])

So your marginal inference cost is literally $0.

Good for:

* classification
* local RAG
* small agents
* document extraction
* private transformations
* offline-ish functionality

depending on the user's hardware.

### Chrome Prompt API

Modern Chrome also exposes on-device generative APIs backed by its locally downloaded model on supported machines. The Prompt API reached a much more mature state in 2026. ([Chrome for Developers][30])

Again: **user hardware pays the compute cost.**

---

# Now the ridiculously cheap paid layer

Once the free queues are exhausted, don't fall directly back to OpenAI/Anthropic pricing.

## OpenCode Go is absurdly subsidized

Current price:

* $5 first month
* $10/month thereafter

but the plan provides usage buckets equivalent to:

* $12 / 5 hours
* $30 / week
* **$60 / month**

OpenCode estimates that $60 monthly allocation equates to roughly:

* **158,150 DeepSeek V4 Flash requests**
* 150,400 MiMo V2.5 requests
* 21,600 Qwen 3.7 Plus
* 17,150 DeepSeek V4 Pro
* 16,000 MiniMax M3
* 10,250 GPT-5.6 Luna

under its typical-request assumptions. ([OpenCode][31])

That is not ordinary API economics. It's a **subsidized subscription**.

For agentic coding/research workloads I would absolutely exploit it.

---

## DeepSeek direct — schedule jobs based on the clock

DeepSeek changes pricing at **16:00 UTC today, August 16**, which is **23:00 in Phnom Penh**. Their China announcement refers to August 17 because that's midnight Beijing time.

New V4 Flash rates:

**Off-peak**

* cached input: **$0.007/M**
* uncached input: **$0.22/M**
* output: **$0.66/M**

**Peak**

* cached: $0.014/M
* uncached: $0.44/M
* output: $1.32/M

Peak hours are 01:00–04:00 and 06:00–10:00 UTC; everything else gets the half-price off-peak rate. ([DeepSeek API Documentation][32])

In Cambodia that makes peak approximately:

```text
08:00–11:00
13:00–17:00
```

Queue bulk translation/indexing/research outside those windows.

That simple scheduler cuts direct DeepSeek inference cost **50%**.

---

# Decentralized/distributed gold

## AkashML

Akash's managed API is significantly easier than renting raw decentralized GPUs.

Current examples I found include approximately:

* DeepSeek V4 Flash: **$0.14 input / $0.28 output per M**
* Llama 3.3 70B: **$0.13 / $0.40**
* GPT-OSS 120B: approximately **$0.037 input / $0.49 output**

([AkashML][33])

The underlying Akash marketplace also uses decentralized capacity/reverse-auction economics, with substantially cheaper GPU capacity possible than hyperscaler list prices. ([Akash Network][34])

**Very worth benchmarking.**

---

## Chutes

Chutes is decentralized/serverless and currently offers, among others:

* DeepSeek V4 Flash: **$0.14 / $0.28**
* Gemma 4 31B Turbo: around **$0.12 / $0.37**
* Qwen / GLM / Kimi endpoints
* TEE variants for protected execution

([Chutes][35])

Private deployments start around $1.80 GPU-hour, with deployment fees, and public per-token endpoints have no general minimum. ([Chutes][36])

One important correction to old blog posts: **Chutes' old 200-free-requests/day scheme is gone.** Don't build on stale guides.

---

## io.net

io.net has its own inference layer over distributed GPUs.

Examples observed in current pricing include:

* Gemma 3n E4B around **$0.03/$0.03 per M**
* Llama 4 Maverick around **$0.27/$0.85**

([io.net][37])

Worth testing for tiny high-volume utility models.

---

## SaladCloud

This one is easy to overlook because it isn't primarily marketed as an LLM gateway.

Salad's distributed consumer-GPU cloud currently advertises:

* roughly **$0.12/M tokens average for TGI workloads**
* containers starting around **$0.04/hour**
* approximately $0.22/hour examples for 7B model serving

([Salad][38])

For a model you use constantly, this can be more interesting than serverless token APIs.

---

## Vast.ai Serverless

Vast now has a proper serverless inference product rather than merely renting random GPUs.

It bills by the second and currently advertises an entry point of only **$5**, with on-demand, interruptible and reserved capacity. ([Vast AI][39])

Excellent for:

```text
cheap marketplace GPU
        ↓
vLLM / SGLang
        ↓
OpenAI-compatible endpoint
        ↓
your router
```

---

# Deals that LOOK good on old lists but are now dead

This section may save you more time than the live list.

**GitHub Models:** retired completely on **July 30, 2026**. Playground, model catalog, inference API and BYOK were removed. ([GitHub Docs][40])

**Lambda Inference API:** the famously cheap Lambda token API you're remembering is being **wound down**. Old `$0.02/M` references are historical; don't design around them. Lambda's GPU infrastructure remains relevant, but the old inference deal isn't your jackpot anymore. ([Lambda][41])

**Cerebras:** old articles still call it a permanent free tier. Current official terms instead give a **$5 trial credit**, expiring after 30 days, with payment-method verification. ([Cerebras Inference][42])

**Chutes:** old 200-RPD free program ended in 2026. Paid inference remains cheap. ([Chutes][43])

**Hyperbolic:** there were fantastic free-hosted-405B promotions historically; I couldn't verify an equivalent recurring current offer, so I would monitor rather than count it in your free capacity.

**Replicate:** useful product, but I found initial/promotional access rather than a dependable recurring-free LLM quota. ([Replicate][44])

This is why automated verification matters.

---

# Build `llm-scavenger`: your live pricing intelligence service

This is the part I think would be especially useful.

Don't maintain a Markdown list manually. Build a little database with these fields:

```sql
provider
model
api_base
model_id

deal_type
-- recurring_free
-- monthly_credit
-- temporary_promo
-- signup_credit
-- user_pays
-- paid
-- deprecated

input_usd_per_m
cached_input_usd_per_m
output_usd_per_m

rpm
rpd
tpm
tpd
monthly_credit_usd
reset_period

credit_card_required
identity_required
geo_restrictions
openai_compatible

training_on_free_data
sensitive_data_ok

source_url
source_hash
last_verified_at
expires_at

probe_status
probe_latency_ms
probe_effective_cost
```

Then treat **price claims and actual endpoint availability as separate facts**.

---

# Your best machine-readable upstream: Models.dev

This may be the single most useful data source for the whole project.

Models.dev is an open-source normalized database of:

* providers
* model IDs
* context lengths
* capabilities
* pricing
* provider availability

and exposes JSON directly:

```text
https://models.dev/api.json
https://models.dev/models.json
https://models.dev/catalog.json
```

([Models][45])

It currently knows about OpenCode Zen, OpenCode Go and dozens upon dozens of other providers. ([Models][46])

**Poll this first.**

---

# Second machine-readable upstream: OpenRouter

```text
GET https://openrouter.ai/api/v1/models
```

Extract:

```text
model
pricing.prompt
pricing.completion
pricing.cache_read
context_length
supported_parameters
```

Then, for models that interest you, query the actual endpoints/providers behind the model. OpenRouter documents both APIs officially. ([OpenRouter][12])

This lets you detect things like:

> Yesterday provider A served DeepSeek at $0.27/M; today provider B appeared at $0.14/M.

---

# Third: OpenCode

```text
GET https://opencode.ai/zen/v1/models
```

Take a snapshot every hour or two.

When:

```text
old.price > 0
new.price == 0
```

you've found a promo.

Or:

```text
new_model && new_price < threshold
```

send yourself an alert.

---

# Fourth: maintain the open-source free-API registry

I found a surprisingly useful project:

**`mnfst/awesome-free-llm-apis`**

It specifically attempts to list **permanent free tiers rather than signup-credit spam**, and currently includes obscure things such as Aion, Kilo, ModelScope, OVH, LLM7, Zhipu, SambaNova, Ollama Cloud, etc. It even keeps a machine-readable `data.json`. ([GitHub][7])

The important idea isn't blindly trusting it.

Watch its commits.

Someone else discovering:

> “Provider X quietly added 500 free calls/day”

can become an input into your system automatically.

---

# Fifth: scrape only the official pages that don't have APIs

Monitor hashes of:

```text
OpenCode Zen pricing
OpenCode Go
DeepSeek pricing
Groq rate limits
Cloudflare Workers AI pricing
Cloudflare Workers AI changelog
Gemini pricing + changelog
Mistral limits/changelog
Cerebras changelog
Together changelog
Beam pricing
Modal pricing
Chutes pricing
SambaNova rate limits
Kilo models
Z.AI free models
```

Don't alert on every HTML change.

Extract the relevant DOM/text, normalize whitespace, hash it:

```python
new_hash = sha256(normalized_pricing_text.encode()).hexdigest()

if new_hash != old_hash:
    run_llm_diff(old_text, new_text)
```

Then have a cheap/free model classify it into:

```json
{
  "new_free_tier": false,
  "price_drop_pct": 51,
  "new_model": "whatever",
  "quota_increase": null,
  "promo_expiry": null,
  "interesting": true
}
```

The scavenger can literally use free models to **hunt for more free models**.

---

# Sixth: use Hacker News as early-warning radar

HN's Algolia search API is public and supports programmatic search. ([HN Search][47])

Poll queries such as:

```text
"free inference"
"free LLM API"
"API credits"
"free GPU"
"inference pricing"
"price cut"
"free tier"
"OpenAI compatible"
"serverless GPU"
"DeepSeek pricing"
"Show HN inference"
```

Filter results newer than your previous poll.

Do the same with GitHub searches for README changes containing:

```text
"free tier"
"free credits"
"requests/day"
"tokens/day"
"no credit card"
"$0.00"
"inference API"
```

The goal isn't to trust social posts; they're **discovery signals** which your verifier then checks against official documentation.

---

# Your actual automatic routing stack

I would make it work like this:

```text
                      ┌─ Kilo Auto Free
                      ├─ OpenCode free promo
                      ├─ NVIDIA NIM
REQUEST → POLICY ────┼─ Groq
          ROUTER      ├─ Z.AI Flash
                      ├─ Workers AI quota
                      ├─ OpenRouter free
                      ├─ OVH background queue
                      ├─ SambaNova
                      │
                      └─ CHEAP FALLBACK
                            ↓
                      OpenCode Go
                      DeepSeek off-peak
                      AkashML
                      Chutes
                      Together
                      self-host Beam/Modal
```

Use LiteLLM as the compatibility layer if you don't want to implement 30 provider adapters. It already normalizes more than 100 providers behind OpenAI-style interfaces. ([GitHub][48])

But I'd keep **your own scheduler above LiteLLM**, because what you want isn't merely “pick cheapest advertised token price.”

It's:

```text
choose endpoint that minimizes:

actual $ / successful task
```

---

# This distinction is surprisingly important

A 2026 measurement study of hosted LLM APIs found that routing the **same model** to different inference providers could materially alter both throughput and price; one representative routing experiment cut Qwen3-32B cost by **37.8%**, while another nearly doubled DeepSeek throughput. ([arXiv][49])

And another study found that reasoning-token behavior can make the apparent per-token price misleading—the cheapest list price doesn't necessarily mean the cheapest completed task. ([arXiv][50])

So benchmark:

```text
provider
model
task_type
input_tokens
output_tokens
reasoning_tokens
cache_hits
latency
success
quality_score
actual_cost
```

Then compute:

```python
effective_cost = total_cost / successful_jobs
```

That should drive your router.

Not simply:

```python
min(input_token_price)
```

---

# An especially aggressive $0 strategy

If I were trying to squeeze the absolute maximum inference out of this ecosystem, I would allocate jobs approximately like:

```text
Frontend/simple private work
    → WebLLM / Chrome local model

Public web-app user features
    → Puter user-pays

Tiny repeated utilities
    → Groq 8B (14,400 RPD)

Coding
    → Kilo Auto Free
    → Laguna/Nemotron/etc
    → OpenCode promo

General reasoning
    → NVIDIA NIM
    → OpenCode DeepSeek V4 Flash
    → Z.AI GLM Flash

Vision/document work
    → Z.AI GLM-4.6V-Flash
    → Gemini free
    → Cloudflare free

Slow background jobs
    → OVH anonymous allowance
    → SambaNova quota
    → OpenRouter free

Custom/open model
    → Modal $30
    → Beam $30

Free exhausted
    → OpenCode Go

Bulk asynchronous paid
    → DeepSeek off-peak
    → AkashML / Chutes / Together

High sustained volume
    → Salad/Vast/Akash GPU + vLLM
```

That is enough separate capacity that a small project can do a **surprising amount of inference without paying conventional API rates**.

## My highest-signal discoveries from the hunt

If you only add ten new things to your arsenal, add:

1. **Kilo `kilo-auto/free` — 200 req/hour/IP**
2. **Z.AI free GLM-4.7 + free GLM-4.6V multimodal**
3. **NVIDIA NIM developer endpoints**
4. **Modal — $30 recurring/month**
5. **Beam — another $30 recurring/month**
6. **OVH — anonymous 2 RPM *per model***
7. **ModelScope — ~2,000 free RPD**
8. **OpenCode Zen's rotating free pool**
9. **OpenCode Go's $10 → $60-usage subsidy**
10. **Models.dev JSON + the awesome-free-llm-apis `data.json` as your discovery engine**

And the architecture I would actually build is a tiny open-source **`llm-scavenger` registry + canary tester + price/quota diff engine + LiteLLM router**. Once that exists, you stop asking “what's the cheapest API?” because your software continuously discovers the answer.

Because these deals change constantly, I can also monitor this exact ecosystem and alert you when a new recurring free API, major promotion, or unusually large price cut appears.

* [reuters.com](https://www.reuters.com/world/china/deepseek-raises-api-pricing-its-v4-models-2026-08-13/?utm_source=chatgpt.com)

[1]: https://kilo.ai/docs/code-with-ai/agents/auto-model?utm_source=chatgpt.com "Auto Model"
[2]: https://kilo.ai/docs/getting-started/using-kilo-for-free?utm_source=chatgpt.com "Using Kilo for Free"
[3]: https://opencode.ai/docs/zen/ "Zen | OpenCode"
[4]: https://docs.bigmodel.cn/cn/guide/models/free/glm-4.7-flash?utm_source=chatgpt.com "GLM-4.7-Flash - 智谱AI开放文档 - 平台介绍"
[5]: https://docs.bigmodel.cn/cn/guide/models/free/glm-4.6v-flash?utm_source=chatgpt.com "GLM-4.6V-Flash - 智谱AI开放文档 - 平台介绍"
[6]: https://docs.api.nvidia.com/nim/docs/product?utm_source=chatgpt.com "General NIM FAQ"
[7]: https://github.com/mnfst/awesome-free-llm-apis "GitHub - mnfst/awesome-free-llm-apis: List of Permanent Free LLM API (API Keys) · GitHub"
[8]: https://console.groq.com/docs/rate-limits "Rate Limits - GroqDocs"
[9]: https://developers.cloudflare.com/workers-ai/platform/pricing/?utm_source=chatgpt.com "Pricing · Cloudflare Workers AI docs"
[10]: https://developers.cloudflare.com/changelog/post/2026-07-28-models-require-workers-paid/?utm_source=chatgpt.com "Select models now require the Workers Paid plan"
[11]: https://openrouter.ai/docs/faq?utm_source=chatgpt.com "OpenRouter FAQ"
[12]: https://openrouter.ai/docs/api/api-reference/models/list-all-models-and-their-properties?utm_source=chatgpt.com "List all models and their properties"
[13]: https://help.ovhcloud.com/csm/en-au-public-cloud-ai-endpoints-getting-started?id=kb_article_view&sysparm_article=KB0065410&utm_source=chatgpt.com "AI Endpoints - Getting started"
[14]: https://docs.sambanova.ai/docs/en/models/rate-limits "Rate Limits Policy - SambaNova Documentation"
[15]: https://docs.mistral.ai/admin/billing-usage/usage-limits?utm_source=chatgpt.com "Usage and limits | Mistral Docs"
[16]: https://ai.google.dev/gemini-api/docs/rate-limits "Rate limits  |  Gemini API  |  Google AI for Developers"
[17]: https://ai.google.dev/gemini-api/docs/pricing?utm_source=chatgpt.com "Gemini Developer API pricing"
[18]: https://ai.google.dev/gemini-api/docs/billing?utm_source=chatgpt.com "Billing | Gemini API | Google AI for Developers"
[19]: https://docs.cohere.com/reference/errors?utm_source=chatgpt.com "Errors (status codes and description)"
[20]: https://huggingface.co/docs/inference-providers/pricing?utm_source=chatgpt.com "Pricing and Billing"
[21]: https://huggingface.co/docs/hub/spaces-zerogpu?utm_source=chatgpt.com "Spaces ZeroGPU: Dynamic GPU Allocation for Spaces"
[22]: https://docs.together.ai/docs/changelog?utm_source=chatgpt.com "Changelog - Together AI docs"
[23]: https://docs.siliconflow.cn/en/userguide/rate-limits/rate-limit-and-upgradation "Rate limits - SiliconFlow"
[24]: https://www.siliconflow.com/pricing?utm_source=chatgpt.com "Pricing Plans - SiliconFlow | Transparent Pay-as-You-Go"
[25]: https://modal.com/pricing?utm_source=chatgpt.com "Plan Pricing"
[26]: https://www.beam.cloud/pricing?utm_source=chatgpt.com "Pricing - Beam Cloud"
[27]: https://api.lightning.ai/notebooks?utm_source=chatgpt.com "Lightning | Deploy AI models"
[28]: https://developer.puter.com/pricing/?utm_source=chatgpt.com "Puter.js Pricing: The User-Pays Model - Puter Developer"
[29]: https://webllm.mlc.ai/?utm_source=chatgpt.com "WebLLM | Home"
[30]: https://developer.chrome.com/docs/ai/prompt-api?utm_source=chatgpt.com "The Prompt API | AI on Chrome - Chrome for Developers"
[31]: https://opencode.ai/docs/go/?utm_source=chatgpt.com "Go"
[32]: https://api-docs.deepseek.com/quick_start/pricing?utm_source=chatgpt.com "Models & Pricing | DeepSeek API Docs"
[33]: https://chatapi.akash.network/?utm_source=chatgpt.com "AkashML - Scale Your AI with High-Performance Inference"
[34]: https://akash.network/?utm_source=chatgpt.com "Akash Network - Decentralized Compute Marketplace"
[35]: https://chutes.ai/?utm_source=chatgpt.com "Chutes | Serverless AI Compute"
[36]: https://chutes.ai/pricing?utm_source=chatgpt.com "Per-token rates and TEE GPU deployments, priced in the ..."
[37]: https://io.net/p/best-cloud-gpu-providers-for-ai-ml-2026?utm_source=chatgpt.com "Best Cloud GPU Providers for AI/ML (2026)"
[38]: https://salad.com/?utm_source=chatgpt.com "Salad - Distributed GPU Cloud | 60,000+ daily active GPUs ..."
[39]: https://vast.ai/article/deploy-llm-inference-using-vast-ai-serverless?srsltid=AfmBOopZydiP3FtzH1DwO-bC0afiLIoLHRcLEp9leQJdqiQB-gPhFOMl&utm_source=chatgpt.com "Deploy LLM Inference Using Vast.ai Serverless"
[40]: https://docs.github.com/github-models?utm_source=chatgpt.com "GitHub Models"
[41]: https://lambda.ai/inference?utm_source=chatgpt.com "Inference"
[42]: https://inference-docs.cerebras.ai/support/rate-limits?utm_source=chatgpt.com "Rate Limits - Cerebras Inference"
[43]: https://chutes.ai/news/community-announcement-february?utm_source=chatgpt.com "Community Announcement - February 27th, 2026"
[44]: https://replicate.com/docs/guides/run/vinext?utm_source=chatgpt.com "Build a website with vinext"
[45]: https://models.dev/providers/freemodel "FreeModel models, pricing, and API docs | Models.dev"
[46]: https://models.dev/providers/opencode?utm_source=chatgpt.com "OpenCode Zen models, pricing, and API docs"
[47]: https://hn.algolia.com/api?utm_source=chatgpt.com "HN Search API | HN Search powered by Algolia"
[48]: https://github.com/BerriAI/litellm?utm_source=chatgpt.com "BerriAI/litellm: The fastest, litest AI Gateway. Rust core with ..."
[49]: https://arxiv.org/abs/2605.02821?utm_source=chatgpt.com "When Is the Same Model Not the Same Service? A Measurement Study of Hosted Open-Weight LLM APIs"
[50]: https://arxiv.org/abs/2603.23971?utm_source=chatgpt.com "The Price Reversal Phenomenon: When Cheaper Reasoning Models End Up Costing More"
