# migration/ — the coordination + blueprint (organized)

*2026-08-14 · status: ORGANIZED · this folder holds (1) the **current blueprint** (v3), (2) the
**archived blueprint** (v2, superseded), and (3) the **shared coordination** with agentgraph (the
two-sided build). Read the READMEs in each. If you are a new agent: go to `v3/README.md` (the current
design + proofs) then `shared/README.md` (the live two-sided build directives).*

---

## THE CLEAN STRUCTURE

| Path | What it is | Status |
|---|---|---|
| **`v3/`** | the CURRENT blueprint — the organism (17→37 kernels, 16 products, the build spec, verified proofs, live tests) | ✅ CURRENT |
| **`shared/`** | the two-sided coordination with agentgraph — role separation, handoff queue, the build-directive set, the shared goal, the critical audits | 🟡 LIVE COORDINATION |
| **`v2/`** | the ORIGINAL blueprint (design/proposed) — superseded by v3 | 🔴 ARCHIVED |
| **`mixxii`** | the systems review (imported from R2) that shaped v2/v3 | reference |

---

## THE ONE-LINE (what each is for)

> **v3 = what Pāṭala is now (the proven organism + tests). shared = what we're building with agentgraph
> (the two-sided coordination + build directives). v2 = the earlier design it all grew from (archived).**

---

## READING ORDER (for a new agent)

1. **`v3/README.md`** — the current blueprint: the organism, the 16 products, the verified proofs (run the
   tests), the honest state.
2. **`shared/README.md`** — the coordination: who does what (agentgraph vs agentpatala), the handoff queue,
   the build-directive set (BUILD-*.md), the shared goal, the critical audits.
3. **`v2/README.md`** — (archived) the earlier design, for context only.

---

## WHAT THE MAIN DOCS TREE IS

The **canonical `docs/` tree** (process/, layers/, vision/, global/, corpus/, api/) is the operational
documentation. This `migration/` folder is the **design/coordination** layer — the blueprint (v3), the
archive (v2), and the shared build directives (shared/). They complement each other: `docs/` is the
running system; `migration/` is the plan + the coordination.
