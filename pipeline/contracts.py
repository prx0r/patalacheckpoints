"""Stage-contract validation.

Separates THREE different questions (per the 1.8 peer review):
  FORMAT   — is it parseable JSON?            (model.parse_json)
  CONTRACT — did the model produce the REQUIRED data?  (this module)
  AUDIT    — is that data structurally/epistemically acceptable? (audit.py)

A stage may return VALID JSON that is NOT a valid stage output. E.g. `{}` or
`{"cruxes":[]}` parse fine but may not satisfy the R1 contract.

Required fields are SUBSTANTIVE: present, right type, and not empty where an empty
value would mean "the model produced nothing."

Returns a list of {field, reason} problems. Empty list = contract satisfied.
"""
from __future__ import annotations
from typing import Any

# required: field -> a predicate that returns True if the value is "substantive"
def _non_empty_str(v):
    return isinstance(v, str) and v.strip() != ""

def _list(v):
    return isinstance(v, list)

def _any(v):
    return v is not None

# T1 close/reader must be non-empty; flags optional
T1 = {"close_translation": _non_empty_str, "reader_draft": _non_empty_str}
# R1 assessment non-empty; cruxes a list (may be [])
R1 = {"assessment": _non_empty_str, "cruxes": _list}
# T2 translation non-empty; decisions list; constrained list
T2 = {"translation": _non_empty_str, "decisions": _list, "constrained": _list}
# R2 translation non-empty; decisions list; hard_core non-empty
R2 = {"translation": _non_empty_str, "decisions": _list, "hard_core": _non_empty_str}
# T3 resolved non-empty
T3 = {"resolved": _non_empty_str}

CONTRACTS = {
    "T1": T1, "R1": R1, "T2": T2, "R2": R2, "T3": T3,
    # T3.1 is prose; C1 handled specially (prose + separate metadata extraction)
}

# the lean model contract field -> canonical schema field
LEAN_TO_CANONICAL = {
    "T1": {"translation": "close_translation", "reader": "reader_draft", "flags": "flags"},
    "R1": {"assessment": "detail", "cruxes": "cruxes"},
    "T2": {"translation": "close_translation", "decisions": "rival_decisions", "constrained": "constrained"},
    "R2": {"translation": "chosen", "decisions": "decisions", "hard_core": "hard_core"},
    "T3": {"resolved": "resolved"},
}


def validate_stage_contract(stage: str, obj: dict) -> list[str]:
    """Return a list of contract problems (empty = satisfied)."""
    contract = CONTRACTS.get(stage)
    if contract is None:
        return []  # no contract (T3.1 prose, C1 handled separately)
    problems = []
    for field, pred in contract.items():
        if field not in obj:
            problems.append(f"{stage}.{field}: missing")
        elif not pred(obj[field]):
            problems.append(f"{stage}.{field}: empty or wrong type")
    return problems


def normalize_lean(stage: str, obj: dict) -> dict:
    """Map a LEAN model object to the RICH canonical schema, using the lean→canonical
    field map. Keeps any canonical-named keys already present (backward compat)."""
    mapping = LEAN_TO_CANONICAL.get(stage, {})
    out = dict(obj)
    for lean_key, canonical_key in mapping.items():
        if lean_key in obj:
            out[canonical_key] = obj[lean_key]
    return out
