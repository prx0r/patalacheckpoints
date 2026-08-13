# CROSS-AGENT CONTRACT

Agents are replaceable producers. No agent owns canonical scholarly authority.

## 1. Proposal envelope

Every agent emits a proposal:

```json
{
  "proposal_id": "uuid-or-content-id",
  "created_at": "...",
  "producer": {
    "agent": "agent2",
    "code_ref": "git:<commit>",
    "runtime_ref": "hermes-or-other",
    "model_ref": "..."
  },
  "object_type": "AnalysisWitness|AuditFindingProposal|Proposition|...",
  "payload_schema": "pt://schema/.../v1",
  "payload": {},
  "input_refs": [
    {"object_id":"...", "version_id":"..."}
  ],
  "evidence_refs": [],
  "lineage": [],
  "structural_validation": [],
  "claimed_authority": "NONE"
}
```

The key field is `claimed_authority: NONE`.

## 2. Canonical ingress

```text
agent output
   ↓
schema validation
   ↓
reference resolution
   ↓
lineage verification
   ↓
proposal registry
   ↓
[human review or deterministic source-integrity policy where permitted]
   ↓
canonical command
   ↓
append ObjectVersion / ReviewEvent
   ↓
reducer
```

No agent may:
- set canonical `review_status`;
- write `DerivedState`;
- declare benchmark fixture adjudicated;
- overwrite an object version;
- bypass canonical review command;
- infer authority from model confidence.

## 3. Deterministic machine promotions are narrowly scoped

Some machine results can be accepted automatically **only for formally checkable properties**, e.g.:
- schema validity;
- hash equality;
- exact span bounds;
- source-byte roundtrip;
- object reference resolution.

They may never automatically promote:
- translation correctness;
- term sense;
- speaker attribution;
- proposition defensibility;
- argument soundness;
- corroboration meaning;
- contradiction;
- scholarly consensus.

## 4. Cross-agent version contract

Every producer records:
- git commit/ref;
- code package version;
- model ID/version;
- prompt/template hash where material;
- external tool/version;
- input object versions.

This makes an output reproducible even after branch merges.

## 5. Branch integration rule

Agent branches may define experimental schemas, but before merge:
1. map experimental object → canonical target object;
2. prove zero-loss or document loss explicitly;
3. add compatibility fixtures;
4. stop emitting new branch-local authority fields;
5. migrate execution to canonical command API;
6. retain historical branch artifact hashes.

## 6. Failure contract

Fail closed:
- unresolved canonical ref → no canonical promotion;
- source-integrity failure → no dependent semantic promotion;
- analyzer disagreement → preserve disagreement;
- insufficient evidence → abstain/open;
- model timeout → explicit failure, bounded retry;
- blocked passage → passage stays blocked;
- partial work → work stays partial;
- rejected/revised object → history remains resolvable.
