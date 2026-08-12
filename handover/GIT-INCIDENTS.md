# GIT INCIDENT LOG — provenance errors are recorded, not erased

*2026-08-12. Pāṭala's doctrine applies to its own Git history: a provenance error is a finding, not
something to hide. This log records cross-lane Git incidents so they become agent-infrastructure
fixtures (CAUSE / TRIGGER / RECOVERY / PREVENTION) rather than repeated mistakes.*

---

## INCIDENT-2026-08-12-01 — CROSS_LANE_INDEX_CONTAMINATION (`4cc78d1`)

- **commit:** `4cc78d1` "Agent 2 (L0): śiva-corpus download manifest + cross-work L0 audit finding"
- **commit_author_lane:** agent2
- **contains (both lanes):**
  - agent2 L0 work (śiva-corpus manifest, GRETIL e-texts, cross-work L0 audit)
  - **agent1 ML work accidentally co-committed** (ASPIC adapter + pilot + run `133850Z`, CP4 state update,
    agent1 session/handoff content)
- **CAUSE:** one shared working tree + one shared index across all agents. Branches do not isolate the
  index or working tree.
- **TRIGGER:** Agent 1 `git add`-ed files; Agent 2 committed while those files remained staged, sweeping
  them into its own commit.
- **BAD RECOVERY (do not repeat):** subsequent branch surgery (stash / cherry-pick / reset / branch -D)
  on the dirty shared tree increased entanglement and crossed lanes further.
- **CORRECT RECOVERY:** stop mutation → record this incident → Agent 0 reconciles attribution → migrate
  live agents to dedicated worktrees.
- **PREVENTION (root cause):** give each live agent its own **Git worktree**
  (`/root/projects/patala-agent1` on `agent1`, `/root/projects/patala-agent2` on `agent2`, ...) with a
  separate working tree + index + branch checkout, sharing only the object DB. Then
  `git branch --show-current` alone is insufficient; the invariant is
  `agent identity ↔ worktree path ↔ checked-out branch` — all three must agree, and session start fails
  hard unless they do.

---

## AGENT0 ACTION — migrate live agents to dedicated worktrees (root-cause fix)

**Why:** branches do not isolate the index/working tree. Only a per-agent worktree makes it *impossible
by construction* for one agent to mutate another's pending state.

**Migration (once):**
```bash
# from the canonical repo root (coordinator), AFTER reconciling INCIDENT-2026-08-12-01 attribution:
git worktree add /root/projects/patala-agent1 agent1
git worktree add /root/projects/patala-agent2 agent2
# register each worktree path in AGENTS.yaml (agent1.worktree, agent2.worktree)
```

**Per-agent operating rule afterward:**
- Agent 1's shell is rooted at `/root/projects/patala-agent1`; its index/working tree are its own.
- Agent 1 can never stage Agent 2's files, because Agent 2's modified files aren't in Agent 1's worktree.
- Typed handoffs (LOG.md) still carry data/schema coordination; Git is no longer a shared mutable workspace.

**Session-start gate (each agent):**
```bash
[ "$(git -C "$PWD" branch --show-current)" = "agent1" ] \
  && [ "$(realpath .)" = "$(realpath /root/projects/patala-agent1)" ] \
  || { echo "FAIL: agent identity / worktree path / branch disagree"; exit 1; }
```

**Attribution rule for the past commit:** `4cc78d1` is recorded (INCIDENT-2026-08-12-01), NOT rewritten.
Subsequent clean commits on the correct worktrees establish ownership.
