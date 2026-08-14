#!/usr/bin/env python3
"""Ask ChatGPT (via hermes -z) for the next-phase plan, grounded in the three
strategic docs. Hermes reads the files locally; we pass only the instruction."""
import sys, os
sys.path.insert(0, "/root/projects/patala")
import pipeline.model as model_mod

BASE = "/root/projects/patala"
PROMPT = f"""You are advising the Pāṭala project on its next phase. READ the following files
on disk (do not rely on memory), then propose a concrete, phased plan.

READ FIRST:
1. The advice request (my current state + the 5 questions):
   {BASE}/experiments/advice-request-next.md
2. The Tantra Hub spec (endgame2): {BASE}/docs/endgame2.md
3. The six-primitives spec (nextdev): {BASE}/docs/nextdev.md
4. The API-first build plan (DEV_PLAN): {BASE}/docs/DEV_PLAN.md
5. Optionally the current state: {BASE}/STATE_OF_PLAY.md and {BASE}/PROCESS_NOTES.md

CONTEXT: Pāṭala's automated translation pipeline works (T1→R1→T2→R2→T3 via a durable
state machine, model shelling to Hermes). C1/commentary is done by the user's main model,
NOT machine-generated. The six primitives + scholarly graph are built. 43 API routes, 29
MCP tools, 84 tests pass. 7 works segmented; 1 work (kramasadbhava) translation-ready.
Milestone A1 proven (Kramasadbhāva 1.8 full adjudication loop). The strategic reset:
Pāṭala = provenance + adjudication infrastructure, not a translation factory.

DELIVER:
- A clear #1 priority (single highest-leverage next action) with the first concrete step.
- A phased plan (phases with goals + a demonstrable artifact each).
- How to do the 25-verse research unit as a cohesive object (what Hermes accumulates vs.
  what the user's main model produces as C1s).
- How to make term-sense assignments first-class evidence-backed annotations (the
  nirānanda gap) so the term-history engine becomes an output of audited work.
- What NOT to do next.
- The smallest artifact I can show a Krama specialist this month.

Be concrete and specific. Reference file paths / code names where useful."""

def main():
    print("=== launching strategy request via hermes ===", flush=True)
    out = model_mod._hermes_call(PROMPT, model="deepseek-v4-flash", timeout=600)
    print(out, flush=True)
    with open("/root/projects/patala/experiments/advice-response.md", "w", encoding="utf-8") as f:
        f.write("# Advice Response — Pāṭala next phase\n\n" + out)
    print("\n=== saved to experiments/advice-response.md ===", flush=True)

if __name__ == "__main__":
    main()
