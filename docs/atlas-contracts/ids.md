# IDs — stable identity vs exact version

*Field reference for the Pāṭala identity model (`python/patala_core/ids.py`).*

Two distinct identities — never conflate them:

| Identity | Meaning | Example | Never changes? |
|---|---|---|---|
| **`object_id`** | the thing across its entire history | `PTPROP_01J...` | yes |
| **`version_id`** | one exact immutable formulation | `PTPROPV_01J...` | yes (immutable) |

External users can cite either:
- the **work**: "Tantrāloka generally" → `PTW_01J...`
- the **version**: "the exact source Pāṭala used in analysis X" → `PTSRC_...@v17` + payload hash

## Design rules

- **UUIDv7 internally**, encoded as sortable opaque textual IDs (collision-resistant for distributed
  creation, offline imports, external contributions — NOT sequential integers).
- **Never encode mutable metadata inside the ID.** A work's date/edition live in columns, not in the ID.
- **Typed prefix** on the public ID so the type is self-describing:

| Type | Prefix | Type | Prefix |
|---|---|---|---|
| WORK | `PTW` | PASSAGE | `PTPASS` |
| PERSON | `PTP` | PROPOSITION | `PTPROP` |
| INSTITUTION | `PTI` | PROPOSITION VERSION | `PTPROPV` |
| EDITION | `PTE` | ARGUMENT | `PTARG` |
| WITNESS | `PTM` | REVIEW | `PTREV` |
| SURROGATE | `PTS` | ASSET | `PTASSET` |
| TRANSCRIPTION | `PTT` | SOURCE | `PTSRC` |
| ETEXT | `PTX` | | |

Permanent resolver: `https://patala.org/id/PTW_...` (redirects/render forever).

## Python

```python
from patala_core.ids import ObjectId, ObjectVersionId

oid = ObjectId.new("WORK")            # PTW_<uuid7>
vid = ObjectVersionId(object_id=str(oid), version=4, payload_hash="sha256:...")
print(vid)                            # PTW_...@v4
```

## Data model

```
object_id   → the stable identity (one row, many versions)
version_id  → an exact immutable formulation (payload_hash = its content)
```
