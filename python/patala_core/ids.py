"""patala_core.ids — typed identity + version identity.

Implements technical-architecture-v1 §15–16:
  - object_id  = the stable identity across history (e.g. PTPROP_01J...)
  - version_id = one exact immutable formulation (e.g. PTPROPV_01J...)

UUIDv7 internally, encoded as opaque typed textual IDs. Never encode mutable metadata
inside the ID.
"""
from __future__ import annotations

import secrets
import time
from dataclasses import dataclass


def _uuid7_hex() -> str:
    """A minimal sortable (UUIDv7-ish) 32-hex id: unix_ms prefix + random tail."""
    ms = int(time.time() * 1000) & 0xFFFFFFFFFFFFFFFF
    return f"{ms:016x}{secrets.token_hex(8)}"


_TYPE_PREFIX = {
    "WORK": "PTW", "PERSON": "PTP", "INSTITUTION": "PTI",
    "EDITION": "PTE", "WITNESS": "PTM", "SURROGATE": "PTS",
    "TRANSCRIPTION": "PTT", "ETEXT": "PTX", "SOURCE": "PTSRC",
    "PASSAGE": "PTPASS", "PROPOSITION": "PTPROP", "VERSION": "PTPROPV",
    "ARGUMENT": "PTARG", "REVIEW": "PTREV", "ASSET": "PTASSET",
}


@dataclass(frozen=True)
class ObjectId:
    """Stable identity across a versioned object's history."""
    type: str
    value: str

    @classmethod
    def new(cls, type_: str) -> "ObjectId":
        return cls(type=type_, value=f"{_TYPE_PREFIX.get(type_, 'PT')}_{_uuid7_hex()}")

    def __str__(self) -> str:
        return f"{_TYPE_PREFIX.get(self.type, 'PT')}_{self.value}"


@dataclass(frozen=True)
class ObjectVersionId:
    """An exact immutable version of an object."""
    object_id: str
    version: int
    # content hash (the immutable formulation)
    payload_hash: str

    def __str__(self) -> str:
        return f"{self.object_id}@v{self.version}"
