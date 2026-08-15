"""products/scholar_review/engine.py — Review #7 + Scholar Attestation #8 + Audit #14.

A standalone peer-review + attestation engine over REAL IPVV objects. Three products, one coherent
kernel (matches the Scholar family in v3 PRODUCTS.md):

  Review (#7)   : adversarial panel (anti-groupthink) + typed-dependency reducer + impact
  Attestation   : signed, content-addressed, tamper-detected ScholarAttestation
  Audit (#14)   : Pāṭala audits itself — every object/review/attestation resolves

Standalone: this module imports ONLY the shared IPVV loader + the deterministic review reducer. No
Next.js, no MCP, no network. Call it directly:

    from products.scholar_review.engine import ScholarProduct
    sp = ScholarProduct()
    sp.panel_review(ref, ["r1","r2","r3"], "j1", findings=[...])
    sp.attest(ref, "scholar-A", "ACCEPT_WITH_QUALIFICATIONS", "...")
    sp.audit()
"""
from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))
from review_engine import ReviewLedger  # noqa: E402
from products._shared import ipvv  # noqa: E402


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# --------------------------------------------------------------------------- #
# the adversarial panel (anti-groupthink) — inlined, no external kernel needed
# --------------------------------------------------------------------------- #
class _Panel:
    def __init__(self, reviewers, judge):
        self.reviewers = reviewers
        self.judge = judge
        self.opinions = {r: None for r in reviewers}
        self.blocking = 0

    def collect(self, reviewer, opinion, blocking=False):
        self.opinions[reviewer] = opinion
        if blocking:
            self.blocking += 1

    def verdict(self):
        votes = [v for v in self.opinions.values() if v is not None]
        agree = bool(votes) and all(v == votes[0] for v in votes)
        dissent = {r: o for r, o in self.opinions.items() if o is not None and o != (votes[0] if votes else None)}
        return {
            "consensus": agree, "n_reviewers": len(votes), "dissent": dissent,
            "blocking_findings": self.blocking,
            "verdict": "BLOCKED" if self.blocking > 0 else "REVISE_OR_ACCEPT",
        }


# --------------------------------------------------------------------------- #
# the signed attestation (content-addressed + deterministic signature)
# --------------------------------------------------------------------------- #
@dataclass
class ScholarAttestation:
    attestation_id: str
    target_ref: str
    target_version: str
    reviewer: str
    reviewer_kind: str
    scope: str
    verdict: str
    rationale: str
    content_hash: str
    signature: str
    created_at: str = field(default_factory=_now)

    def to_dict(self) -> dict:
        return asdict(self)


def _payload(a) -> str:
    return json.dumps({
        "attestation_id": a.attestation_id, "target_ref": a.target_ref,
        "target_version": a.target_version, "reviewer": a.reviewer,
        "reviewer_kind": a.reviewer_kind, "scope": a.scope,
        "verdict": a.verdict, "rationale": a.rationale,
    }, sort_keys=True, ensure_ascii=False)


def verify_attestation(att: dict, signing_key: str = "patala-demo-editorial-key") -> tuple[bool, str]:
    a = ScholarAttestation(**{k: att[k] for k in ScholarAttestation.__dataclass_fields__ if k in att})
    payload = _payload(a)
    if _sha(payload.encode()) != a.content_hash:
        return False, "content_hash_mismatch"
    if _sha((signing_key + ":" + payload).encode()) != a.signature:
        return False, "signature_invalid"
    return True, "VERIFIED"


# --------------------------------------------------------------------------- #
# the product
# --------------------------------------------------------------------------- #
class ScholarProduct:
    def __init__(self, seed: bool = True, readonly: bool = False):
        self.ledger = ReviewLedger()
        self.objects: dict[str, dict] = {}
        self.attestations: list[dict] = []
        self._readonly = readonly
        if seed:
            self._hydrate()

    def _hydrate(self):
        for n in ipvv.goldchain():
            ref = n["id"]
            self.objects.setdefault(ref, n)
            self.ledger.add_version(ref, json.dumps(n, ensure_ascii=False)[:500])
            for dep in n.get("depends_on", []):
                self.ledger.edges.append(type("E", (), {"source": dep, "target": ref, "type": "GROUNDS"})())
        for c in ipvv.passages():
            ref = ipvv.passage_id(c)
            if ref and ref not in self.objects:
                self.objects[ref] = c
                self.ledger.add_version(ref, ipvv.c1_body(c)[:500])
        for a in ipvv.assertions():
            ref = a.get("id")
            if ref and ref not in self.objects:
                self.objects[ref] = a
                self.ledger.add_version(ref, json.dumps(a, ensure_ascii=False)[:500])

    def _require(self, ref: str) -> dict:
        if ref not in self.objects:
            raise KeyError(f"unknown object {ref}")
        return self.objects[ref]

    # read surfaces
    def list_objects(self, layer: str | None = None) -> list[dict]:
        objs = [{"id": k, "layer": (v.get("layer") or "passage"), "status": v.get("status"),
                 "review_state": v.get("review_state")} for k, v in self.objects.items()]
        if layer:
            objs = [o for o in objs if o["layer"] == layer]
        objs.sort(key=lambda o: o["id"])
        return objs

    def object_state(self, ref: str, version: str | None = None) -> dict:
        self._require(ref)
        return self.ledger.get_state(ref, version)

    def impact(self, ref: str) -> dict:
        self._require(ref)
        return self.ledger.impact_report(ref)

    # review
    def propose_review(self, target_ref: str, proposed_decision: str, rationale: str,
                       scope: str = "passage", evidence_refs: list[str] | None = None) -> dict:
        self._require(target_ref)
        return self.ledger.propose_review(target_ref, "v1", proposed_decision, rationale, scope, evidence_refs)

    def submit_review(self, actor_id: str, actor_kind: str, authorization_scope: str,
                      target_ref: str, decision: str, rationale: str, scope: str = "passage",
                      evidence_refs: list[str] | None = None) -> dict:
        self._require(target_ref)
        ev = self.ledger.submit_review(actor_id, actor_kind, authorization_scope,
                                       target_ref, "v1", decision, scope, rationale, evidence_refs)
        rec = ev.to_dict()
        # persist to the contribution ledger (so the scholar profile accumulates across sessions)
        if not self._readonly:
            p = ROOT / "data/scholar/reviews.jsonl"
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        return {"review": rec, "derived_state": self.ledger.reduce().states}

    def simulate_review(self, target_ref: str, decision: str) -> dict:
        self._require(target_ref)
        return self.ledger.simulate_review(target_ref, decision)

    def panel_review(self, target_ref: str, reviewers: list[str], judge: str,
                     findings: list[dict] | None = None) -> dict:
        self._require(target_ref)
        panel = _Panel(reviewers, judge)
        for f in (findings or []):
            panel.collect(f.get("reviewer"), f.get("opinion"),
                          blocking=f.get("severity") == "BLOCKING")
        return {"target_ref": target_ref, "reviewers": reviewers, "judge": judge,
                "verdict": panel.verdict()}

    # attestation
    def attest(self, target_ref: str, reviewer: str, verdict: str, rationale: str,
               scope: str = "passage", signing_key: str = "patala-demo-editorial-key",
               private_pem: bytes | None = None) -> dict:
        """Attest to a precise object. Default: demo HMAC signature. If `private_pem` (an Ed25519
        private key) is given, uses PRODUCTION asymmetric signing (cosign-style, verify with public
        key only)."""
        self._require(target_ref)
        vs = self.ledger.versions.get(target_ref, [])
        version = vs[-1].version if vs else "v1"
        att = {"attestation_id": f"SA-{target_ref}:{version}:{reviewer}",
               "target_ref": target_ref, "target_version": version, "reviewer": reviewer,
               "reviewer_kind": "scholar", "scope": scope, "verdict": verdict, "rationale": rationale}
        if private_pem is not None:
            from products.scholar_review.signing import make_signed_attestation
            rec = make_signed_attestation(att, private_pem)
            self.attestations.append(rec)
            return {"attestation": rec, "verified": True, "algorithm": "Ed25519"}
        # demo HMAC path (kept for backward-compat / offline)
        a = ScholarAttestation(**att, content_hash="", signature="")
        payload = _payload(a)
        a.content_hash = _sha(payload.encode())
        a.signature = _sha((signing_key + ":" + payload).encode())
        rec = a.to_dict()
        self.attestations.append(rec)
        return {"attestation": rec, "verified": verify_attestation(rec, signing_key)}

    # audit
    def audit(self) -> dict:
        ds = self.ledger.reduce()
        states = ds.states
        unreviewed = [o for o in self.objects if states.get(o, "CANDIDATE") == "CANDIDATE"]
        from collections import Counter
        layers = Counter(v.get("layer", "passage") for v in self.objects.values())
        verified = sum(1 for a in self.attestations if verify_attestation(a)[0])
        return {
            "objects": len(self.objects),
            "layers": dict(sorted(layers.items())),
            "reviews_in_ledger": len(self.ledger.events),
            "attestations_signed": len(self.attestations),
            "attestations_verified": verified,
            "unreviewed_objects": len(unreviewed),
        }


def run_demo() -> dict:
    sp = ScholarProduct()
    ref = sp.list_objects(layer="C1")[0]["id"]
    panel = sp.panel_review(ref, ["r1", "r2", "r3"], "j1", findings=[
        {"reviewer": "r1", "opinion": "SUPPORT"},
        {"reviewer": "r2", "opinion": "SUPPORT"},
        {"reviewer": "r3", "opinion": "CONCERN", "severity": "BLOCKING", "text": "evidence gap"}])
    submit = sp.submit_review("scholar-A", "scholar", "*", ref, "ACCEPT", "sound")
    att = sp.attest(ref, "scholar-A", "ACCEPT_WITH_QUALIFICATIONS", "reviewed")
    return {"object": ref, "panel": panel, "submit": submit["review"], "attestation": att, "audit": sp.audit()}


if __name__ == "__main__":
    import sys as _sys
    verb = _sys.argv[1] if len(_sys.argv) > 1 else "demo"
    args = json.loads(_sys.argv[2]) if len(_sys.argv) > 2 else {}
    sp = ScholarProduct()
    try:
        if verb == "list_objects": res = {"objects": sp.list_objects(args.get("layer"))}
        elif verb == "object": res = sp.object_state(args["target_ref"])
        elif verb == "impact": res = sp.impact(args["target_ref"])
        elif verb == "panel": res = sp.panel_review(args["target_ref"], args.get("reviewers", ["r1", "r2", "r3"]), args.get("judge", "j1"), args.get("findings"))
        elif verb == "propose": res = sp.propose_review(args["target_ref"], args["proposed_decision"], args.get("rationale", ""), args.get("scope", "passage"), args.get("evidence_refs"))
        elif verb == "submit": res = sp.submit_review(args["actor_id"], args["actor_kind"], args.get("authorization_scope", "*"), args["target_ref"], args["decision"], args.get("rationale", ""), args.get("scope", "passage"), args.get("evidence_refs"))
        elif verb == "simulate": res = sp.simulate_review(args["target_ref"], args["decision"])
        elif verb == "attest": res = sp.attest(args["target_ref"], args["reviewer"], args["verdict"], args.get("rationale", ""), args.get("scope", "passage"))
        elif verb == "audit": res = sp.audit()
        elif verb == "demo": res = run_demo()
        else: res = {"error": f"unknown verb {verb}"}
        print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False)); _sys.exit(1)
