# RAiD — the research-activity identifier (scholar identity/credit)

**What Pāṭala borrows:** RAiD (Research Activity Identifier) identifies the **research activity/project itself**
and binds contributors, organizations, outputs and other PIDs into a persistent project record with version
history. It completes the scholar-identity stack: Scholar → ORCID, Institution → ROR, Contribution role →
CRediT, Research project → RAiD, Published review/output → DOI.

**License:** open identifier system.

## Example
```
RAiD: Critical IPVV Reflexivity Project
 ├─ ORCID Tom / Scholar A
 ├─ ROR BHU
 ├─ DOI Dataset / Review Objects / Paper
```

## How Pāṭala consumes it
Pāṭala does NOT build its own global research-project identifier system — it uses RAiD for the project-level
identity and binds its `pt:*` objects under it.

**Priority: design the scholar-credit projection; runtime later.**
