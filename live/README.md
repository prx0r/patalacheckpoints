# live/ — real-time cross-agent coordination

A root-level, easy-to-find shared surface for **live session state** between Agent 1 and Agent 2.

- `agent2.md` — Agent 2's current checkpoint, what it's building, validation status, and what's ready
  for Agent 1 to evaluate.
- `agent1.md` — Agent 1's verification readiness view: which layers have MACHINE_PROPOSED objects ready
  for independent evaluation, and when.

**Rules:**
- These are fast, update-in-place session records. Authoritative long-form handovers live in
  `handover/agent-1-ml/` and `handover/agent-2-integration/`.
- Agent 2 updates `agent2.md` and, when a layer's candidates are ready, notes it in `agent1.md`.
- Cross-lane events go in `handover/LOG.md`.
- The clean role split: **Agent 2 = MAKE THE FACTORY RUN · Agent 1 = PROVE THE FACTORY DESERVES TRUST.**
