# The Pāṭala Scholarly Graph — canonical schema

*2026-08-10. The durable data model. Everything Pāṭala serves is either an OBJECT or an
ANNOTATION/ASSERTION over objects. This schema must survive years, so it is deliberately
small and conservative. Built on the six primitives (`data/corpus/primitives.ts`) and
`nextdev.md`'s objects/claims/events distinction.*

---

## 1. Objects (the identities)

Objects are durable, addressable things. They do NOT contain mutable interpretation —
interpretation lives in assertions/annotations.

| Object | id pattern | What it is |
|---|---|---|
| **Work** | `pt:work:{slug}` | the abstract intellectual object (e.g. `Kramasadbhāva`) |
| **Witness** | `pt:wit:{slug}` | a concrete manifestation (a manuscript, an edition, a digital copy) |
| **DigitalRepresentation** | `pt:dr:{slug}` | a scan/image/transcription representation of a witness |
| **CanonicalPassage** | `pt:passage:{work}:{loc}` | one addressable unit of text |
| **SourceSpan** | `pt:span:{work}:{loc}` | how a passage appears in a specific witness/edition |
| **Person** | `pt:person:{slug}` | an author, translator, scholar, reviewer |
| **Organization** | `pt:org:{slug}` | an institution (Muktabodha, OCHS, IFP, BHU) |
| **Term** | `pt:term:{lemma}` | a technical term (kula, krama, śakti) |
| **Sense** | `pt:sense:{lemma}.{n}` | a meaning of a term in a scope |
| **Resource** | `pt:res:{slug}` | a bibliographic object (edition, article, lecture, manuscript record) |

**Rules:**
- IDs never change once public.
- Titles/names can change; IDs cannot.
- External IDs are aliases (crosswalks), not replacements.
- Objects carry only durable identity + facts (dates with certainty, traditions, coverage);
  contested claims live in assertions.

## 2. Annotations / Assertions (the claims)

Interpretation is an annotation targeting an object (or another annotation). This is the
OpenPecha-style "annotations on annotations" model, and the `nextdev.md` objects→claims→events
distinction.

```ts
interface Annotation {
  id: string;
  target: string;              // any object or annotation id
  type: AnnotationType;
  payload: any;                // the specific claim's data
  origin: Origin;              // machine | editor | scholar | institution
  status: EpistemicState;      // proposed | checked | expert_reviewed | accepted | disputed | rejected
  certainty?: Certainty;       // certain | probable | possible | uncertain  (≠ status)
  evidence: Evidence[];        // resource/passage links + role
  review_events: string[];     // ids of ReviewEvents
  created_at: string;
  created_by: string;
  superseded_by?: string;      // id of a later annotation that replaces this
}
```

Annotation types:
```
translation · lexical_decision · grammar · ambiguity · parallel · textual_variant ·
term_occurrence · sense_assignment · dating · tradition · authorship ·
manuscript_identification · commentary · term_history_assertion · bibliographic_claim
```

## 3. The three independent dimensions (never conflated)

On every version/annotation:

```
origin            who produced it (machine | human)
status            epistemic maturity (proposed → reviewed → accepted)
certainty         how sure (certain | probable | possible | uncertain)
```

- `status` ≠ `certainty`. `accepted` + `probable` is a valid state ("currently accepted,
  evidence incomplete").
- Machine output is always `origin=machine`; it NEVER sets `status=accepted` by itself.
  Only a scoped ReviewEvent promotes.

## 4. Review

A review is an event, scoped to a target/version:

```ts
interface ReviewEvent {
  id: string;
  target: string;            // the annotation/version reviewed
  scope: ReviewScope;        // grammar | lexical | translation | dating | term_sense | parallel | manuscript_identification | ...
  reviewer: { kind: string; id: string };
  review_type: string;       // TEXTUAL | GRAMMATICAL | LEXICAL | TRANSLATIONAL | HISTORICAL | DOCTRINAL | READABILITY | MANUSCRIPT
  outcome: "accept" | "reject" | "revise" | "needs_specialist" | "abstain";
  reason: string;
  evidence?: Evidence[];
  created_at: string;
}
```

- A review targets a specific version, not "the record".
- `accept` → the target becomes `reviewed`. Editorial promotion to `accepted` is a
  separate, explicit action that requires it to be `reviewed` first.

## 5. Evidence

Evidence links a claim to a source that supports/contradicts/defines it:

```ts
interface Evidence {
  resource: string;      // a Resource id (or passage id)
  locator?: string;      // page / verse / folio / section
  role: "supports" | "contradicts" | "defines" | "dates" | "identifies" | "quotes" | "parallel" | "commentary";
  note?: string;
}
```

Evidence does not make a claim true; it makes it traceable.

## 6. The unified graph

```
OBJECTS                    ANNOTATIONS                EVENTS
Work ─────────────────┐
Witness ──────────────┤      Annotation/Assertion    ReviewEvent
Passage ──────────────┼──►   (target, type, payload,  (who, what, scope,
SourceSpan ───────────┤        origin, status,        outcome, reason,
Person ───────────────┤        certainty, evidence)   evidence)
Term ─────────────────┤              │
Sense ────────────────┘              ▼
Resource                             supersedes / revision chain
```

Every object can be peeled back to a source; every claim carries evidence + review
history. This is the "bundle on read, normalize on write" model.

## 7. What maps onto the primitives

- A translation choice = an Annotation (type `translation`/`lexical_decision`) targeting
  a passage, with evidence + provenance + review.
- A term-history claim = an Annotation (type `term_history_assertion`) targeting a
  term/sense, with passage/scholarship evidence.
- A parallel = an Annotation (type `parallel`) relating passage A and passage B.
- A bibliography claim (edition X covers 1.1–4.55) = an Annotation (type
  `bibliographic_claim`).
- A C1 commentary = a set of Annotations + one commentary object.

## 8. Versioning

- Annotation versions are immutable; a change creates a new version with
  `supersedes`/`superseded_by`.
- The public API bundles these into convenient objects (a passage "context" bundle);
  the storage is normalized (see `docs/STACKED_ARTIFACT_SPEC.md`).
