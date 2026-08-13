# REVIEW ENGINE V2 HARDENING

## Preserve the existing semantic heart

The current Agent1 vertical has the right behavior:
- review is append-like;
- REVISE creates a new version;
- historical version survives;
- dependencies recompute;
- unrelated objects remain isolated;
- reducer is deterministic;
- proposal can be zero-authority;
- simulation can be zero-write.

Do not replace this with a generic workflow system.

## 1. One command boundary

Current prototype exposes both low-level recording and authorized submission. Target:

```text
ReviewService.submit(command, auth_context)
        │
        ├─ authenticate actor
        ├─ authorize object/scope/action
        ├─ resolve target version
        ├─ verify replacement version if REVISE
        ├─ validate decision
        ├─ enforce idempotency key
        ├─ append immutable event
        └─ trigger deterministic reducer
```

Only the event-store adapter can append, and it verifies the service-signed command envelope. `record_review` must not be a public authority-changing method.

## 2. ReviewCommand

```json
{
  "command_id":"...",
  "actor_ref":"pt:contributor:...",
  "credential_ref":"pt:credential:...",
  "target_ref":{"object_id":"...","version_id":"..."},
  "decision":"ACCEPT|REVISE|REJECT|ABSTAIN",
  "scope":"TRANSLATION|PROPOSITION|GROUNDING|ARGUMENT|...",
  "reason":{"text":"...","evidence_refs":[]},
  "replacement_ref":null,
  "expected_current_version":"...",
  "client_context":{"product":"translation-audit","finding_id":"..."}
}
```

## 3. ReviewEvent

Immutable result of accepted command:

```json
{
  "event_id":"pt:review:...",
  "event_version":"2",
  "command_id":"...",
  "actor_ref":"...",
  "credential_snapshot":{},
  "target_ref":{"object_id":"...","version_id":"..."},
  "decision":"REVISE",
  "scope":"PROPOSITION",
  "reason":{},
  "replacement_ref":{"object_id":"...","version_id":"..."},
  "created_at":"...",
  "event_hash":"..."
}
```

## 4. Reviewer independence

Store facts, then compute policies.

Facts:
- contributor identity;
- organization;
- authorship relation;
- prior contribution relation;
- declared conflict;
- credential/specialty.

Computed:
```text
SAME_AUTHOR
NON_INDEPENDENT
INDEPENDENT
SPECIALIST_INDEPENDENT
UNKNOWN
```

Never infer “independent” from two different display names alone.

## 5. Concurrency

`expected_current_version` provides optimistic concurrency.

If the object changed after reviewer loaded it:
- do not silently apply;
- return `VERSION_CONFLICT`;
- preserve submitted proposal;
- reviewer may rebase/reaffirm.

## 6. Reducer contract

Reducer output is a function of:

```text
(object versions, review events, dependency edges, policy version, reducer version)
```

Persist:
- input snapshot hash;
- reducer version;
- output hash;
- causal events;
- direct/transitive affected objects.

## 7. Impact semantics

Separate:
- `DIRECTLY_AFFECTED`
- `TRANSITIVELY_AFFECTED`
- `UNCHANGED`
- `BLOCKED`
- `NEEDS_RECOMPUTE`

Do not propagate indiscriminately. Edge type and review scope determine effect.

Example:
a proposition wording revision may stale premise-use/inference but need not stale exact source anchoring.

## 8. Production persistence

Recommended logical tables/collections:

```text
object_versions
review_commands
review_events
dependency_edges
derived_state_snapshots
impact_reports
contributors
credentials
```

Append-only for versions/events. Index latest projections separately.

## 9. Required tests beyond current vertical

- unauthorized low-level append impossible;
- machine cannot forge scholar context;
- nonexistent target version rejected;
- REVISE requires existing replacement version;
- duplicate command id idempotent;
- concurrent stale version rejected;
- two independent reviews counted correctly;
- same-author duplicate not counted independent;
- reducer output hash stable;
- reducer version change creates new snapshot, not rewrite;
- rejected historical version resolves;
- partial dependency graph does not imply global validity;
- one broken edge cannot stale unrelated subgraph;
- simulation zero-write including event store and projections.
