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

const transport = new StdioServerTransport();
await server.connect(transport);
