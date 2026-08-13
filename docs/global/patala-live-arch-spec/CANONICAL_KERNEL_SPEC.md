# CANONICAL KERNEL SPEC

**Status:** proposed target contract.  
**Rule:** preserve existing identifiers and history through adapters; do not rewrite old records merely to make schemas look clean.

## 1. Package ownership

The exact directory name can change during implementation. The ownership boundary cannot.

```text
core/
  identity/
  authority/
  evidence/
  interpretation/
  argument/
  dependency/

pipeline/
  workers/
  reducers/
  commands/
  adapters/

benchmarks/
  fixtures/
  tasks/
  scorers/
  scanners/
  runs/

products/
  audit/
  review/
  workbench/

api/
  read/
  commands/
  mcp/
```

### `core/`
Contains canonical meanings. It must not import:
- Hermes;
- Inspect;
- GROBID;
- PaperQA;
- INCEpTION;
- product UI;
- agent code.

### `pipeline/`
Executes canonical commands and adapters. It may import core, never redefine core concepts.

### `benchmarks/`
Freezes evaluation fixtures/runs. It references source/canonical object IDs, but benchmark review/gold state is **evaluation authority**, not production scholarly authority.

### `products/`
Product-specific projections and proposed findings. Product events cross into core only via canonical commands.

## 2. Universal identity

Every authority-bearing or dependency-bearing object has stable object identity and immutable versions.

```json
{
  "object_id": "pt:proposition:G2-TC2",
  "object_type": "Proposition",
  "version_id": "sha256-or-stable-version-id"
}
```

### Invariants

- `object_id` identifies diachronic object identity.
- `version_id` pins exact content.
- review targets must pin a version.
- dependency edges that need reproducibility pin versions.
- “latest” is a view, never stored as a historical fact.
- an old version remains resolvable after revision.
- content-addressed hashes should be recorded even if human-friendly version labels also exist.

## 3. Canonical object families

### Identity
- `Work`
- `Witness`
- `DigitalRepresentation`
- `Passage`
- `StableSpan`
- `ObjectVersion`
- `ExternalCrosswalk`

### Evidence
- `SourceAssertion`
- `EvidenceUse`
- `CorroborationEvent`
- `CitationRelation`

### Philology / interpretation
- `AnalysisWitness`
- `PhilologicalProof`
- `TranslationDecision`
- `Term`
- `TermSense`
- `SemanticAlignment`
- `Proposition`
- `PropositionDerivation`
- `Commitment`

### Reasoning
- `ResearchQuestion`
- `DebateFrame`
- `Inference`
- `Argument`
- `Attack`
- `Defeater`
- `Crux`
- `ArgumentSynthesis`

### Authority
- `Contributor`
- `Credential`
- `ReviewEvent`
- `ReviewPolicy`
- `Adjudication`

### Temporal/dependency
- `DependencyEdge`
- `DerivedState`
- `ImpactReport`

## 4. Proposition must remember derivation

A proposition is not merely text.

```json
{
  "object_id": "pt:proposition:...",
  "version_id": "...",
  "text": "...",
  "derivation": {
    "kind": "EXPLICIT_SOURCE|RECONSTRUCTED|COMMENTARIAL|SYNTHETIC|ATTRIBUTED",
    "source_refs": [],
    "method_ref": null
  },
  "speaker_ref": "...",
  "commitment_ref": "...",
  "frame_refs": []
}
```

Critical distinction:
- explicit source statement;
- reconstructed proposition;
- author commitment;
- opponent commitment;
- quotation;
- assumption for argument.

Without this, a machine can create a structurally valid argument whose author attribution is false.

## 5. Commitment

Minimum vocabulary:

```text
ASSERTS
DENIES
PRESUPPOSES
ASSUMES_FOR_ARGUMENT
ATTRIBUTES_TO_OPPONENT
QUOTES
RECONSTRUCTED
OPEN
```

Commitment is independent from proposition truth/support.

## 6. Argument under a frame

Contradiction is never a raw edge between arbitrary proposition strings.

Before comparing:
1. same research/debate question?
2. same target?
3. compatible term senses?
4. compatible explanatory level?
5. compatible quantifier/scope?
6. compatible modality?
7. same or translatable frame?

`SemanticAlignment` records this comparison. Possible relation outputs include:

```text
COMMENSURABLE
PARTIALLY_COMMENSURABLE
QUESTION_MISMATCH
TARGET_MISMATCH
TERM_SENSE_MISMATCH
SCOPE_MISMATCH
MODALITY_MISMATCH
LEVEL_MISMATCH
NON_COMPARABLE
```

Only after adequate commensurability may a system propose:
`CONTRADICTS`, `SUPPORTS`, `ENTAILS`, etc.

## 7. Dependency edges

Minimum native relations:

```text
GROUNDS
USES_AS_PREMISE
USES_AS_WARRANT
CONCLUDES
DEPENDS_ON_READING
DEPENDS_ON_TERM_SENSE
DEPENDS_ON_ALIGNMENT
ORGANIZES
RESPONDS_TO
ATTACKS
DEFEATS
SUPERSEDES
```

Edges may include:
- source object/version;
- target object/version or diachronic target;
- support scope;
- derivation origin;
- edge review state;
- provenance.

## 8. Derived state is computed, not authored

A reducer derives effective state from:
- immutable object versions;
- immutable review events;
- dependency edges;
- policy/reducer version.

Never let an agent directly write `DerivedState`.

Every derived result includes:

```json
{
  "object_ref": {"object_id":"...", "version_id":"..."},
  "state": "NEED_REVIEW",
  "reducer": {"name":"dependency-reducer", "version":"..."},
  "input_snapshot_hash":"...",
  "causes":["pt:review:..."],
  "computed_at":"..."
}
```

## 9. Crux

A crux is a counterfactual dependency result, not a rhetorical label.

For target conclusion `C` and disputed input `P`:

1. compute support state for `C`;
2. retract/disable `P` in simulation only;
3. recompute;
4. if `C` materially changes, `P` is decision-relevant;
5. minimal sets whose removal changes target outcome are candidate crux sets.

`simulate_review` is therefore not just a UI convenience. It is the beginning of the crux engine.

## 10. No generic confidence field

Do not introduce a universal 0–1 “truth/confidence” number. Scores can exist only with:
- named task;
- metric semantics;
- calibration population;
- model/evaluator version;
- evidence;
- known limitations.

An uncalibrated heuristic must remain explicitly unvalidated.
