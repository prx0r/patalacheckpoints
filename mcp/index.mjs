// Pāṭala MCP — the scholarly evidence engine (v1).
// Read-only evidence retrieval over the corpus. The translator (ChatGPT/Claude/
// opencode) stays the translator; this server only supplies historically-grounded
// context and existing translations, per TRANSLATION_SKILL.md.
//
// It proxies the site's HTTP API (works/relations/passages) so there is ONE source
// of truth, and reads the term ledger (data/terms.json) + the on-disk T1/T2/T3 files.
//
// Usage: node index.mjs   (MCP stdio transport; connect via ChatGPT/Claude/opencode)
// Env:  TANTRA_API_BASE   default http://localhost:3000
//       TANTRA_CORPUS     default /mnt/HC_Volume_106427611/sanskritree/translations

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { readFileSync, readdirSync } from "fs";
import { spawnSync } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PATALA_ROOT = path.resolve(__dirname, "..");
const API_BASE = process.env.TANTRA_API_BASE ?? "http://localhost:3000";
const CORPUS = process.env.TANTRA_CORPUS ?? "/mnt/HC_Volume_106427611/sanskritree/translations";
const TERMS = path.resolve(__dirname, "../data/terms.json");

async function api(p, init) {
  const r = await fetch(`${API_BASE}${p}`, init);
  if (!r.ok) throw new Error(`API ${r.status} for ${p}`);
  return r.json();
}

let _terms = null;
function terms() {
  if (_terms) return _terms;
  try {
    _terms = JSON.parse(readFileSync(TERMS, "utf8")).terms;
  } catch {
    _terms = [];
  }
  return _terms;
}

const server = new McpServer({ name: "patala", version: "0.1.0" });

// ————————————————— get_work —————————————————
server.tool(
  "get_work",
  "Work registry entry: traditions (with certainty), date range, research_roles, translation status, source editions.",
  { id: z.string().describe("work id or urn") },
  async ({ id }) => {
    const d = await api(`/api/works/${encodeURIComponent(id)}`);
    return { content: [{ type: "text", text: JSON.stringify(d.data, null, 2) }] };
  },
);

// ————————————————— get_source_passage —————————————————
server.tool(
  "get_source_passage",
  "The Sanskrit of a single verse by stable passage id (e.g. 'tantra:text:kramasadbhava:1.2').",
  { passage_id: z.string() },
  async ({ passage_id }) => {
    const d = await api(`/api/passages/${encodeURIComponent(passage_id)}`);
    return { content: [{ type: "text", text: JSON.stringify(d.data, null, 2) }] };
  },
);

// ————————————————— resolve_ref —————————————————
server.tool(
  "resolve_ref",
  "The citation backbone. Resolve a reference (ipvv:V2-S:14, IPVV 1.5.11, a pt:pid immutable id, or a tantra:text urn) through the chain: work → passage → source spans → translations → decisions → evidence → C1 → related. Returns the immutable passage id.",
  { ref: z.string() },
  async ({ ref }) => {
    const d = await api(`/api/resolve?ref=${encodeURIComponent(ref)}`);
    return { content: [{ type: "text", text: JSON.stringify(d, null, 2) }] };
  },
);

// ————————————————— search_passages —————————————————
server.tool(
  "search_passages",
  "Substring search over the segmented Sanskrit corpus. Returns matching passages (sanskrit + id).",
  { q: z.string(), work_id: z.string().optional(), limit: z.number().optional() },
  async ({ q, work_id, limit }) => {
    const params = new URLSearchParams({ q, limit: String(limit ?? 30) });
    if (work_id) params.set("work_id", work_id);
    const d = await api(`/api/search/passages?${params}`);
    return { content: [{ type: "text", text: JSON.stringify(d, null, 2) }] };
  },
);

// ————————————————— verification floor (deterministic EXPOSE services) ———————
server.tool(
  "verify_quote",
  "Deterministic verbatim-quote verification: is this quote present in the passage's source (Sanskrit) or published L2? Never hallucinated.",
  { q: z.string(), ref: z.string() },
  async ({ q, ref }) => {
    const d = await api(`/api/verify/quote?q=${encodeURIComponent(q)}&ref=${encodeURIComponent(ref)}`);
    return { content: [{ type: "text", text: JSON.stringify(d, null, 2) }] };
  },
);
server.tool(
  "verify_claim_structure",
  "Deterministic claim-structure check: does the passage resolve and carry source + L2 + C1? The structural floor below any semantic verification.",
  { ref: z.string(), claim: z.string().optional() },
  async ({ ref, claim }) => {
    const p = new URLSearchParams({ ref });
    if (claim) p.set("claim", claim);
    const d = await api(`/api/verify/claim-structure?${p.toString()}`);
    return { content: [{ type: "text", text: JSON.stringify(d, null, 2) }] };
  },
);
server.tool(
  "trace_dependency",
  "Deterministic backward walk of the derivation DAG (source ← L2 ← C1): reports where support breaks. The provenance floor for any generated claim.",
  { ref: z.string() },
  async ({ ref }) => {
    const d = await api(`/api/verify/trace-dependency?ref=${encodeURIComponent(ref)}`);
    return { content: [{ type: "text", text: JSON.stringify(d, null, 2) }] };
  },
);
server.tool(
  "find_counterevidence",
  "Deterministic counterevidence: surfaces the curated contradicts/qualifies edges in the passage's C1. Honest about what is not yet recorded.",
  { ref: z.string() },
  async ({ ref }) => {
    const d = await api(`/api/verify/counterevidence?ref=${encodeURIComponent(ref)}`);
    return { content: [{ type: "text", text: JSON.stringify(d, null, 2) }] };
  },
);

// ————————————————— get_work_hub —————————————————
server.tool(
  "get_work_hub",
  "The source-centric hub: every output a primary source has spawned (translations, essays, logical arguments, pushing-enquiries, learning), all tied to the source's passages. Query by work.",
  { work: z.string() },
  async ({ work }) => {
    const d = await api(`/api/hub?work=${encodeURIComponent(work)}`);
    return { content: [{ type: "text", text: JSON.stringify(d, null, 2) }] };
  },
);

// ————————————————— get_themes —————————————————
server.tool(
  "get_themes",
  "Deterministic theme structure over the IPVV C1s (MACHINE_PROPOSED). Themes group passages sharing a technical lemma. Query by passage or list all.",
  { passage: z.string().optional() },
  async ({ passage }) => {
    const p = new URLSearchParams();
    if (passage) p.set("passage", passage);
    const d = await api(`/api/themes?${p.toString()}`);
    return { content: [{ type: "text", text: JSON.stringify(d, null, 2) }] };
  },
);

// ————————————————— get_related_works —————————————————
server.tool(
  "get_related_works",
  "Typed + confidence + evidence edges touching a work (direct textual relatives for retrieval ranking).",
  { work_id: z.string() },
  async ({ work_id }) => {
    const d = await api(`/api/relations/${encodeURIComponent(work_id)}`);
    return { content: [{ type: "text", text: JSON.stringify(d, null, 2) }] };
  },
);

// ————————————————— get_school_spine —————————————————
server.tool(
  "get_school_spine",
  "The canonical reading spine for a school, tied to the bibliography. Research the 'related N works' of a tradition as one ordered object (root scripture -> commentary -> synthesis -> our target).",
  { tradition: z.string().optional(), work: z.string().optional() },
  async ({ tradition, work }) => {
    const p = new URLSearchParams();
    if (tradition) p.set("tradition", tradition);
    if (work) p.set("work", work);
    const d = await api(`/api/spines?${p.toString()}`);
    return { content: [{ type: "text", text: JSON.stringify(d, null, 2) }] };
  },
);

// ————————————————— get_term_senses —————————————————
server.tool(
  "get_term_senses",
  "Accepted term senses from the ledger (data/terms.json). NOT evidence of occurrence — just the accepted sense policy. Machine/human term proposals live separately (term_proposals.jsonl) and only review promotes them.",
  { lemma: z.string() },
  async ({ lemma }) => {
    const entry = terms().find((t) => t.lemma === lemma) ?? null;
    return { content: [{ type: "text", text: JSON.stringify({ lemma, entry }, null, 2) }] };
  },
);

// ————————————————— search_surface_occurrences —————————————————
server.tool(
  "search_surface_occurrences",
  "Substring search over the segmented corpus (sanskrit + working translation + id). NOT morphological/lemma search — it returns match_method:'substring', lemmatized:false. Do not treat hits as lemma occurrences.",
  { q: z.string(), work_id: z.string().optional(), limit: z.number().optional() },
  async ({ q, work_id, limit }) => {
    const params = new URLSearchParams({ q, limit: String(limit ?? 20) });
    if (work_id) params.set("work_id", work_id);
    let hits = [];
    try {
      const d = await api(`/api/search/passages?${params}`);
      hits = d.passages ?? [];
    } catch {}
    return { content: [{ type: "text", text: JSON.stringify({ q, match_method: "substring", lemmatized: false, occurrences: hits }, null, 2) }] };
  },
);

// ————————————————— get_working_translations —————————————————
server.tool(
  "get_working_translations",
  "Our working (T1) translations for a work as verse-anchored passages (close translation + flags + source edition). Provisional, not peer reviewed. For comparison and calibration — never to be copied verbatim.",
  { work_id: z.string() },
  async ({ work_id }) => {
    const d = await api(`/api/texts/${encodeURIComponent(work_id)}/translations`);
    return { content: [{ type: "text", text: JSON.stringify(d, null, 2) }] };
  },
);

// ————————————————— get_passage_context —————————————————
server.tool(
  "get_passage_context",
  "The deterministic evidence bundle for a passage: Sanskrit + work metadata + manuscript witnesses + neighboring passages + tracked term senses + related works + rights. No generated interpretation.",
  { passage_id: z.string() },
  async ({ passage_id }) => {
    const d = await api(`/api/context/passages/${encodeURIComponent(passage_id)}`);
    return { content: [{ type: "text", text: JSON.stringify(d, null, 2) }] };
  },
);

// ————————————————— find_term_occurrences —————————————————
server.tool(
  "find_term_occurrences",
  "Surface occurrences of a lemma in the segmented corpus. HONEST: match_method substring, lemmatized false (not morphological).",
  { lemma: z.string(), work_id: z.string().optional(), limit: z.number().optional() },
  async ({ lemma, work_id, limit }) => {
    const params = new URLSearchParams({ limit: String(limit ?? 50) });
    if (work_id) params.set("work_id", work_id);
    const d = await api(`/api/terms/${encodeURIComponent(lemma)}/occurrences?${params}`);
    return { content: [{ type: "text", text: JSON.stringify(d, null, 2) }] };
  },
);

// ————————————————— get_term_history —————————————————
server.tool(
  "get_term_history",
  "The diachronic sense-trajectory of a lemma: how its meaning shifts across traditions and periods (the reference map's signature feature). Evidence-backed hypotheses, not settled facts.",
  { lemma: z.string() },
  async ({ lemma }) => {
    const d = await api(`/api/terms/${encodeURIComponent(lemma)}/history`);
    return { content: [{ type: "text", text: JSON.stringify(d, null, 2) }] };
  },
);

// ————————————————— concordance —————————————————
server.tool(
  "concordance",
  "Raw-corpus word tracking across ~500 Sanskrit e-texts (Muktabodha + GRETIL), NOT our translations (anti-echo). Normalized-substring; context lines per hit. Heavier than search_surface_occurrences — use for term usage across the whole tantric corpus.",
  { q: z.string(), texts: z.string().optional(), context: z.number().optional(), max: z.number().optional() },
  async ({ q, texts, context, max }) => {
    const params = new URLSearchParams();
    params.set("q", q);
    if (texts) params.set("texts", texts);
    if (context) params.set("context", String(context));
    if (max) params.set("max", String(max));
    const d = await api(`/api/concordance?${params}`);
    return { content: [{ type: "text", text: JSON.stringify(d, null, 2) }] };
  },
);

// ————————————————— get_manuscripts —————————————————
server.tool(
  "get_manuscripts",
  "The OCHS manuscript witnesses of a work (NAK/NGMPP IDs, script, provenance, date, folios, incipit/colophon). Custodian OCHS, CC BY-NC-SA 4.0; link out for images. No work_id lists all.",
  { work_id: z.string().optional(), q: z.string().optional() },
  async ({ work_id, q }) => {
    const params = new URLSearchParams();
    if (work_id) params.set("work_id", work_id);
    if (q) params.set("q", q);
    const d = await api(`/api/manuscripts${params.toString() ? `?${params}` : ""}`);
    return { content: [{ type: "text", text: JSON.stringify(d, null, 2) }] };
  },
);

// ————————————————— get_existing_translations —————————————————
server.tool(
  "get_existing_translations",
  "Our existing T1/T2/T3 translation files for a work (for comparison and calibration — never to be copied). Returns file paths + a matching excerpt.",
  { work_id: z.string(), needle: z.string().optional() },
  async ({ work_id, needle }) => {
    const dirs = ["01_t1_working", "03_t2_alternate", "05_t3_final", "06_c1_interpretation"];
    const files = [];
    for (const dir of dirs) {
      const p = path.join(CORPUS, dir);
      try {
        for (const f of readdirSync(p)) {
          if (f.toLowerCase().includes(work_id.toLowerCase())) files.push({ stage: dir, file: path.join(dir, f) });
        }
      } catch {}
    }
    let excerpt = null;
    if (needle && files.length) {
      const fp = path.join(CORPUS, files[0].file);
      try {
        const text = readFileSync(fp, "utf8");
        const i = text.toLowerCase().indexOf(needle.toLowerCase());
        if (i >= 0) excerpt = text.slice(Math.max(0, i - 400), i + 600);
      } catch {}
    }
    return { content: [{ type: "text", text: JSON.stringify({ work_id, files, excerpt }, null, 2) }] };
  },
);

// ————————————————— Phase 3D: executable-corrections review tools —————————————————
// Thin layer over pipeline/review_engine.py (the ONLY place review-state logic lives).
// Object-centric: agents speak Pāṭala object language, never read/write review files.
// Boundary: agents PROPOSE; authorized reviewers SUBMIT; Pāṭala ALONE computes consequences.
const REVIEW_ENGINE = path.resolve(__dirname, "../pipeline/review_engine.py");

function review(verb, args = {}) {
  const r = spawnSync("python3", [REVIEW_ENGINE, verb, JSON.stringify(args)], {
    encoding: "utf8", timeout: 30000,
  });
  if (r.status !== 0) throw new Error((r.stderr || r.stdout || "review engine error").slice(0, 500));
  return JSON.parse(r.stdout);
}

// ————————————————— the Hermes reducer bridge (pipeline/product_reducer.py) ———————
// The deterministic .py REDUCTION layer the agentic OS gates product derivations through.
// Hermes/PRODUCT for GENERATION; this .py for REDUCTION (validator + canonical hash + commit).
const REDUCER_ENGINE = path.resolve(__dirname, "../pipeline/product_reducer.py");
function reducer(verb, args = {}) {
  const argv = [REDUCER_ENGINE, verb, args.product ?? "claim"];
  if (verb === "validate" || verb === "commit") argv.push(JSON.stringify(args.proposal ?? {}));
  if (verb === "commit") argv.push(args.actor ?? "hermes-worker", args.layer ?? "CLAIM");
  const r = spawnSync("python3", argv, {
    encoding: "utf8", timeout: 30000, cwd: PATALA_ROOT, env: { ...process.env, PYTHONPATH: PATALA_ROOT },
  });
  if (r.status !== 0) throw new Error((r.stderr || r.stdout || "reducer error").slice(0, 500));
  return JSON.parse(r.stdout);
}

server.tool(
  "patala_reduce",
  "The Hermes-reducer bridge: derive + deterministically validate product proposals from real committed inputs, OR validate/commit a single proposal. This is the .py REDUCTION layer of the agentic OS (Hermes/PRODUCT generates, this gates + commits to object_registry at ENGINEERING_VALIDATED).",
  { verb: z.enum(["reduce", "validate", "commit"]).optional(), product: z.enum(["claim", "crux", "evidence", "tension"]).optional(), proposal: z.any().optional() },
  async ({ verb, product, proposal }) => {
    const r = reducer(verb ?? "reduce", { product, proposal });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_get_review_state",
  "What the scholarly graph currently says about an object: effective state, reviews, supersession, dependencies. Read-only, deterministic.",
  { target_ref: z.string().describe("object id, e.g. G2-TC2"), target_version: z.string().optional() },
  async ({ target_ref, target_version }) => {
    const s = review("get_state", { target_ref, target_version });
    return { content: [{ type: "text", text: JSON.stringify(s, null, 2) }] };
  },
);

server.tool(
  "patala_propose_review",
  "The machine-safe path: create a ReviewProposal that does NOT change scholarly state. Returns origin=MACHINE, status=PROPOSED. Hermes/copilots call THIS.",
  {
    target_ref: z.string(), target_version: z.string().optional(),
    proposed_decision: z.enum(["ACCEPT", "REVISE", "REJECT", "ABSTAIN"]),
    rationale: z.string().optional(), scope: z.string().optional(),
    evidence_refs: z.array(z.string()).optional(), replacement_proposal: z.string().optional(),
  },
  async (a) => {
    const p = review("propose", a);
    return { content: [{ type: "text", text: JSON.stringify(p, null, 2) }] };
  },
);

server.tool(
  "patala_submit_review",
  "The strongest boundary: creates a state-changing ReviewEvent ONLY if the actor is authorized. Requires actor_id + actor_kind + authorization_scope. Pāṭala policy decides legality — a machine actor is forbidden from promotion.",
  {
    actor_id: z.string(), actor_kind: z.string(), authorization_scope: z.string().optional(),
    target_ref: z.string(), target_version: z.string().optional(),
    decision: z.enum(["ACCEPT", "REVISE", "REJECT", "ABSTAIN"]),
    scope: z.string().optional(), rationale: z.string().optional(),
    evidence_refs: z.array(z.string()).optional(), replacement_ref: z.string().optional(),
  },
  async (a) => {
    const r = review("submit", a);
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_get_impact",
  "The product-facing tool: what a review/correction changes (directly + transitively affected, with the reason path). Also supports hypothetical simulation via patala_simulate_review.",
  { target_ref: z.string() },
  async ({ target_ref }) => {
    const r = review("impact", { target_ref });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_simulate_review",
  "ZERO-WRITE hypothetical: 'what happens if I reject G2-TC2?' Returns the hypothetical impact WITHOUT mutating any state. The precursor to the counterfactual scholar interface.",
  { target_ref: z.string(), decision: z.enum(["ACCEPT", "REVISE", "REJECT", "ABSTAIN"]), replacement_ref: z.string().optional() },
  async (a) => {
    const s = review("simulate", a);
    return { content: [{ type: "text", text: JSON.stringify(s, null, 2) }] };
  },
);
// ————————————————— Scholar Review + Attestation product (pipeline/products/scholar_review/engine.py) —————
// The Scholar family: Review #7, Scholar Attestation #8, Audit #14. Hydrates the ReviewLedger from
// REAL IPVV objects (goldchain + C1 + assertions), runs the adversarial panel, and signs attestations.
// Boundary preserved: agents PROPOSE; authorized scholars SUBMIT; Pāṭala alone computes consequences.
const SCHOLAR_ENGINE = path.resolve(__dirname, "../pipeline/products/scholar_review/engine.py");
function scholar(verb, args = {}) {
  const r = spawnSync("python3", [SCHOLAR_ENGINE, verb, JSON.stringify(args)], {
    encoding: "utf8", timeout: 30000,
    cwd: PATALA_ROOT,
    env: { ...process.env, PYTHONPATH: PATALA_ROOT },
  });
  if (r.status !== 0) throw new Error((r.stderr || r.stdout || "scholar engine error").slice(0, 500));
  return JSON.parse(r.stdout);
}

server.tool(
  "patala_scholar_list",
  "List the reviewable Scholar objects (goldchain nodes + C1 passages + assertions) hydrated from real IPVV data. Optional layer filter (L0/C1/ARGUMENT/...).",
  { layer: z.string().optional() },
  async ({ layer }) => {
    const r = scholar("list_objects", { layer });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_scholar_audit",
  "The Audit product: Pāṭala audits itself. Counts reviewable objects, derived review states, signed attestations, and unreviewed objects. Every object resolves.",
  {},
  async () => {
    const r = scholar("audit");
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_scholar_object",
  "What the Scholar graph currently says about one real object: effective review state, reviews, supersession, dependencies.",
  { target_ref: z.string().describe("object id, e.g. V2-L-sastho-vimarsa-smrti-apohana:c1"), target_version: z.string().optional() },
  async ({ target_ref, target_version }) => {
    const r = scholar("object", { target_ref, target_version });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_scholar_impact",
  "The product-facing correction tool: exactly what a review/change to an object affects (direct + transitive, typed).",
  { target_ref: z.string() },
  async ({ target_ref }) => {
    const r = scholar("impact", { target_ref });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_scholar_panel",
  "Run the adversarial scholar panel over a real object's reasoning: N independent reviewers + a judge, anti-groupthink (dissent reported, never forced). BLOCKED if any BLOCKING finding or phantom citation.",
  { target_ref: z.string(), reviewers: z.array(z.string()).optional(), judge: z.string().optional() },
  async (a) => {
    const r = scholar("panel", {
      target_ref: a.target_ref,
      reviewers: a.reviewers ?? ["r1", "r2", "r3"],
      judge: a.judge ?? "j1",
    });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_scholar_simulate",
  "ZERO-WRITE hypothetical correction: what happens if an object is rejected/accepted/revised. Returns hypothetical impact without mutating state.",
  { target_ref: z.string(), decision: z.enum(["ACCEPT", "REVISE", "REJECT", "ABSTAIN"]) },
  async (a) => {
    const r = scholar("simulate", a);
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_scholar_attest",
  "The highest-moat product: produce a SIGNED ScholarAttestation for a precise object (content-hash + deterministic signature). The reviewer attests to one scoped judgment, never 'all of Pāṭala'. Mechanism (signed, verifiable); production uses cosign/ORCID-backed keys.",
  { target_ref: z.string(), reviewer: z.string(), verdict: z.string(), rationale: z.string().optional(), scope: z.string().optional() },
  async (a) => {
    const r = scholar("attest", a);
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

// ————————————————— Moat products (pipeline/products/<product>/engine.py): #2 Proof #5 Argument #6 Crux #9 Packet #13 Comparison ———
// The 5 moat products, hydrated from REAL IPVV data. Deterministic, no model calls. Each verb
// dispatches to the corresponding standalone product engine with its positional args.
const MOAT_DIR = path.resolve(__dirname, "../pipeline/products");
function products(verb, args = {}) {
  // verb -> [engine path, [positional cli args built from `args`]]
  let engine, cliArgs = [];
  switch (verb) {
    case "summary":
    case "proof":
      engine = "translation_proof/engine.py";
      if (verb === "proof" && args.passage_id) cliArgs = [args.passage_id];
      break;
    case "argument":
      engine = "argument/engine.py";
      if (args.argument_id) cliArgs = [args.argument_id];
      break;
    case "crux":
      engine = "crux/engine.py";
      cliArgs = [args.a, args.b];
      break;
    case "packet":
      engine = "research_packet/engine.py";
      cliArgs = [args.question ?? "eternal self memory"];
      break;
    case "compare":
      engine = "comparison/engine.py";
      cliArgs = [args.a, args.b];
      break;
    case "claim":
      engine = "claim/engine.py";
      cliArgs = [];
      break;
    case "bundle":
      engine = "context_bundle/engine.py";
      cliArgs = [args.question ?? "eternal self memory", args.variant ?? "standard"];
      break;
    case "passage_get":
      engine = "passage/engine.py";
      cliArgs = [args.ref ?? "chunkD", "get"];
      break;
    case "passage_neighbors":
      engine = "passage/engine.py";
      cliArgs = [args.ref ?? "chunkD", "neighbors"];
      break;
    case "terminology":
      engine = "terminology/engine.py";
      cliArgs = [args.lemma ?? "kula", args.op ?? "trajectory"];
      break;
    case "timeline":
      engine = "timeline/engine.py";
      cliArgs = [args.op ?? "timeline", args.id ?? ""];
      break;
    case "review_queue":
      engine = "review_queue/engine.py";
      cliArgs = [args.scope ?? "", String(args.limit ?? 10)];
      break;
    case "scholar_identity":
      engine = "scholar_identity/engine.py";
      cliArgs = [args.op ?? "demo"];
      break;
    case "review_workbench":
      engine = "review_workbench/engine.py";
      cliArgs = [args.op ?? "demo"];
      break;
    case "scholar_profile":
      engine = "scholar_profile/engine.py";
      cliArgs = args.op === "profile"
        ? ["profile", args.scholar_id ?? "anonymous"]
        : ["leaderboard", String(args.limit ?? 10)];
      break;
    case "review_policy":
      engine = "review_policy/engine.py";
      cliArgs = args.op === "grants"
        ? ["grants", args.decision ?? "ACCEPT", args.actor_kind ?? "scholar"]
        : ["summary"];
      break;
    case "tension_finder":
      engine = "tension_finder/engine.py";
      cliArgs = [String(args.min_score ?? 0), String(args.limit ?? 20)];
      break;
    case "manuscript_routing":
      engine = "manuscript_routing/engine.py";
      cliArgs = [args.op ?? "demo"];
      break;
    case "manuscript_ingest":
      engine = "manuscript_ingest/engine.py";
      cliArgs = [args.op ?? "demo"];
      break;
    case "evidence":
      engine = "evidence_independence/engine.py";
      cliArgs = [args.mode ?? "offline"];
      break;
    case "passage_workbench":
      engine = "passage_workbench/engine.py";
      cliArgs = [args.op ?? "demo"];
      break;
    case "benchmark":
      engine = "benchmark/engine.py";
      cliArgs = [];
      break;
    case "scholar_publication":
      engine = "scholar_publication/engine.py";
      cliArgs = [args.op ?? "all"];
      break;
    case "scholar_vertical":
      engine = "scholar_vertical/engine.py";
      cliArgs = [args.decision ?? "ACCEPT"];
      break;
    case "collation":
      engine = "collation/engine.py";
      cliArgs = [args.op ?? "demo"];
      break;
    case "translation_studio":
      engine = "translation_studio/engine.py";
      cliArgs = [args.passage_id ?? "", args.register ?? ""];
      break;
    case "guard":
      engine = "guard/engine.py";
      cliArgs = [];
      break;
    default:
      throw new Error(`no engine for verb ${verb}`);
  }
  const script = path.resolve(MOAT_DIR, engine);
  const r = spawnSync("python3", [script, ...cliArgs], {
    encoding: "utf8", timeout: 30000,
    cwd: PATALA_ROOT,
    env: { ...process.env, PYTHONPATH: PATALA_ROOT },
  });
  if (r.status !== 0) throw new Error((r.stderr || r.stdout || "products engine error").slice(0, 500));
  return JSON.parse(r.stdout);
}

server.tool(
  "patala_products_summary",
  "Count the moat-product substrate: real IPVV passages, goldchain nodes, derived arguments, translation proofs.",
  {},
  async () => {
    const r = products("summary");
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_translation_proof",
  "The TranslationProof moat: a non-aggregate 10-dimension audit vector + a publication gate that BLOCKS on any failing dimension. No single 'quality %'. Built from a REAL IPVV passage (source Sanskrit + L2 + L200 proof).",
  { passage_id: z.string().optional().describe("optional; default returns all passages") },
  async ({ passage_id }) => {
    const r = products("proof", { passage_id });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_argument",
  "The Argument product: a real IPVV C1 passage -> thesis + premises + inference + defeaters (AIF-style). Source-backed, never hand-fed.",
  { argument_id: z.string().optional() },
  async ({ argument_id }) => {
    const r = products("argument", { argument_id });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_crux",
  "The Crux product: minimal divergence between two real IPVV arguments. The smallest load-bearing disagreement a targeted research task should attack.",
  { a: z.string().describe("argument_id A"), b: z.string().describe("argument_id B") },
  async ({ a, b }) => {
    const r = products("crux", { a, b });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_research_packet",
  "The Research Packet product: compile a question into a structured evidence packet (best-supported real passages + proof state). Deterministic lexical match over real source/L2/C1.",
  { question: z.string() },
  async ({ question }) => {
    const r = products("packet", { question });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_compare",
  "The Comparison product: structured comparison of two real IPVV arguments classified as AGREEMENT or REAL CRUX, with the shared + divergent premises.",
  { a: z.string().describe("argument_id A"), b: z.string().describe("argument_id B") },
  async ({ a, b }) => {
    const r = products("compare", { a, b });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

// ————————————————— New products: Claim #4 · Context Bundle #16 · Passage #3 · Terminology · Timeline ———————
server.tool(
  "patala_claim",
  "The Claim product: real IPVV passage -> a Proposition with an HONEST epistemic envelope (PĀṬALA-INFERS stays MACHINE_PROPOSED, never inflated) + scope/modality + gate flags.",
  {},
  async () => {
    const r = products("claim");
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_context_bundle",
  "The Agent Context Bundle product: one question -> ONE token-budgeted, ordered context bundle (micro 2k / standard 8k / deep 32k). Composes argument/crux/claim/research_packet on real IPVV.",
  { question: z.string().optional(), variant: z.enum(["micro", "standard", "deep"]).optional() },
  async ({ question, variant }) => {
    const r = products("bundle", { question, variant });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_passage",
  "The Passage/Reading product: canonical Passage + KG2Code query over real IPVV (get by fragment like 'chunkD', neighbors, evidence).",
  { ref: z.string().optional().describe("passage id or fragment, e.g. chunkD"), op: z.enum(["get", "neighbors", "evidence"]).optional() },
  async ({ ref, op }) => {
    const r = op === "neighbors" ? products("passage_neighbors", { ref }) : products("passage_get", { ref });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_terminology",
  "The Terminology / Lemma-through-time product: a lemma's diachronic sense-trajectory across traditions/periods (real trajectories.json).",
  { lemma: z.string().optional(), op: z.enum(["history", "trajectory", "evidence", "report"]).optional() },
  async ({ lemma, op }) => {
    const r = products("terminology", { lemma, op });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_timeline",
  "The Timeline product: the diachronic Śiva source-tree (schools, eras, lineage). E.g. op=lineage id=trika.",
  { op: z.enum(["timeline", "schools", "lineage", "eras", "chronological"]).optional(), id: z.string().optional() },
  async ({ op, id }) => {
    const r = products("timeline", { op, id });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

// ————————————————— Scholar workflow products (the peer-review surface) ———————
server.tool(
  "patala_review_queue",
  "The scholar's 'what do I review next': a PRIORITIZED queue (uncertainty x blast-radius x centrality / cost), not a flat list. Scope + limit optional.",
  { scope: z.string().optional(), limit: z.number().optional() },
  async ({ scope, limit }) => {
    const r = products("review_queue", { scope, limit });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_scholar_identity",
  "The scholar identity layer: ORCID-backed identity + domain scope + Ed25519 keypair (binds attestation signing).",
  { op: z.enum(["demo"]).optional() },
  async ({ op }) => {
    const r = products("scholar_identity", { op });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_review_workbench",
  "The peer-review surface: one object's full review context (state + downstream impact + decision surface). A scholar sees what changes if they reject it.",
  { op: z.enum(["demo"]).optional() },
  async ({ op }) => {
    const r = products("review_workbench", { op });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_scholar_profile",
  "The contribution ledger: a scholar's reviews + attestations (their track record). profile for one scholar, leaderboard for the overview.",
  { op: z.enum(["profile", "leaderboard"]).optional(), scholar_id: z.string().optional(), limit: z.number().optional() },
  async ({ op, scholar_id, limit }) => {
    const r = products("scholar_profile", { op, scholar_id, limit });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_review_policy",
  "The authority semantics: what each review decision (ACCEPT/REVISE/REJECT/ABSTAIN) by each actor kind GRANTS. The invariant authority(projection)<=authority(parent) is preserved.",
  { op: z.enum(["summary", "grants"]).optional(), decision: z.string().optional(), actor_kind: z.string().optional() },
  async ({ op, decision, actor_kind }) => {
    const r = products("review_policy", { op, decision, actor_kind });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_tension_finder",
  "The vision's /find-interesting-tension: surface WHERE interpretations diverge (contradictions, cruxes, distinction-forensics, doctrinal shifts, live-issues) on real IPVV. Papers come from here.",
  { min_score: z.number().optional(), limit: z.number().optional() },
  async ({ min_score, limit }) => {
    const r = products("tension_finder", { min_score, limit });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_manuscript_routing",
  "The manuscript-onboarding diagnostic (vision E3): label + route a manuscript (OCR_THEN_FACTORY / FACTORY_READY / NEEDS_TEXT / UNROUTEABLE) so getting manuscripts in is easy. Adopts kraken+eScriptorium, never rebuilds OCR.",
  { op: z.enum(["demo"]).optional() },
  async ({ op }) => {
    const r = products("manuscript_routing", { op });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_manuscript_ingest",
  "The manuscript->SOURCE adapter: turn a manuscript + OCR text into a labelled, quality-scored Pāṭala SOURCE (quality ladder: raw_scan -> ocr_done -> clean_etext -> factory_ready). OCR is the adopted GPU boundary (kraken/escriptorium), not rebuilt.",
  { op: z.enum(["demo"]).optional() },
  async ({ op }) => {
    const r = products("manuscript_ingest", { op });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_evidence",
  "The evidence-independence product: classify corroborating sources' independence (SOURCE_ECHO, dedup) on the real corroboration registry. mode=offline (deterministic) or live (OpenCitations).",
  { mode: z.enum(["offline", "live"]).optional() },
  async ({ mode }) => {
    const r = products("evidence", { mode });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_passage_workbench",
  "The passage disagreement workbench: a scholar records a disagreement with a passage (sandhi/reading/translation) through the durable review gate.",
  { op: z.enum(["demo"]).optional() },
  async ({ op }) => {
    const r = products("passage_workbench", { op });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_benchmark",
  "The benchmark product: compile real IPVV objects into an inspect_ai eval and report the honest-ceiling rate.",
  {},
  async () => {
    const r = products("benchmark");
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_scholar_publication",
  "The scholar publication surface: the Astro-servable JSON-LD scholar + attestation records (CV-legible output).",
  { op: z.enum(["all", "publish"]).optional() },
  async ({ op }) => {
    const r = products("scholar_publication", { op });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_scholar_vertical",
  "The Scholar Attestation Vertical: a scholar reviews + attests a real object and the correction propagates through the graph (the anti-theatre proof).",
  { decision: z.enum(["ACCEPT", "REVISE", "REJECT", "ABSTAIN"]).optional() },
  async ({ decision }) => {
    const r = products("scholar_vertical", { decision });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_collation",
  "The critical-edition collation (Saktumiva process): N witness texts -> a variant apparatus (which siglum reads what at each locus).",
  { op: z.enum(["demo"]).optional() },
  async ({ op }) => {
    const r = products("collation", { op });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_translation_studio",
  "The translation studio: render ONE passage in multiple registers (TECHNICAL/EXPANDED/CONDENSED/GEN_Z/ARGUMENT_DEPTH) from the same proof graph, with vertical fidelity. Controlled compression, never a new translation.",
  { passage_id: z.string().optional(), register: z.enum(["TECHNICAL", "EXPANDED", "CONDENSED", "GEN_Z", "ARGUMENT_DEPTH"]).optional() },
  async ({ passage_id, register }) => {
    const r = products("translation_studio", { passage_id, register });
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

server.tool(
  "patala_verify_quote",
  "The serve-time guard: verify quoted passages in an answer against retrieved sources (a fabricated quote is downgraded, never served verbatim) + whitelist every citation (a hallucinated work:locus is corrected/stripped). The enforcement of the UNANCHORED->reject rule at serve time.",
  {},
  async () => {
    const r = products("guard", {});
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  },
);

// ————————————————— get_history_timeline —————————————————
server.tool(
  "get_history_timeline",
  "The diachronic Śiva source tree: schools/traditions laid across time (genealogy + prehistory + philosophical interlocutors), each with period, epistemic era (textual/comparative/archaeological), influences, anchors, bibliography ids, hop; plus the diachronic transformation chains and the leapfrog translation-roadmap. Returns /api/history/timeline.",
  {},
  async () => {
    const d = await api(`/api/history/timeline`);
    return { content: [{ type: "text", text: JSON.stringify(d, null, 2) }] };
  },
);

// ————————————————— get_factory_status —————————————————
server.tool(
  "patala_get_factory_status",
  "The autonomous translation factory status: per-layer registry counts (source/l0/l1/l2/l200/c1/theme/essay/assertion/corroboration/witness/span) + the L0 and L200 certificate results. Registry = canonical state; certificates = the A-H / A-L gates. Backed by /api/factory/status.",
  {},
  async () => {
    const d = await api(`/api/factory/status`);
    return { content: [{ type: "text", text: JSON.stringify(d, null, 2) }] };
  },
);

// ————————————————— get_certificate —————————————————
server.tool(
  "patala_get_certificate",
  "Read a factory certificate result (e.g. 'L0-v1' or 'L200-v1'): the measured dimensions (lossless/binding/gloss/false-certainty/abstention/source-failure/replay/cross-work for L0; the A-L dims for L200).",
  { name: z.string().describe("certificate dir name, e.g. L0-v1 or L200-v1") },
  async ({ name }) => {
    const { readFile } = await import("fs/promises");
    const path = await import("path");
    const ROOT = path.dirname(path.dirname(new URL(import.meta.url).pathname));
    const p = path.join(ROOT, "factory-certificates", name, "results.json");
    try {
      const txt = await readFile(p, "utf-8");
      return { content: [{ type: "text", text: txt }] };
    } catch {
      return { content: [{ type: "text", text: `no certificate ${name}` }] };
    }
  },
);

const transport = new StdioServerTransport();
await server.connect(transport);
