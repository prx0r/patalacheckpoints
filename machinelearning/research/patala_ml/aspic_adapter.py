"""patala_ml/aspic_adapter.py — project ARG-002 v2 into ASPIC+, with a minimal pilot evaluator.

The engineering question (the reviewer's falsification test):
  "Can Pāṭala's reconstructed argument be losslessly projected into ASPIC+, and does ASPIC behave
   as expected?"

Two parts:
  1. `project_arg002(gold)` — the ASPIC+ PROJECTION of ARG-002 v2's inferential core. This is the
     representational-fidelity artifact: can we encode the argument WITHOUT losing the distinction
     between an explicit proposition, a reconstructed warrant, and an objection?
  2. A MINIMAL abstract-acceptability evaluator (grounded semantics) as a PILOT FALLBACK.

⚠️ HONEST CAVEAT: the real py-aspic delegates evaluation to the external arg.tech web service
(`http://ws.arg.tech/e/dom`), which returned 503 (unavailable) at the time of this pilot. Rather than
fabricate a result, the pilot runs a minimal LOCAL grounded-semantics evaluator as a temporary fallback.
This is a pilot proxy, NOT the production delegation, and it must be re-run against the real ASPIC+
engine (or a local one) before the "delegate reasoning to ASPIC+" bet is accepted.

The projection keeps, as SEPARATE things (per IR-F-01 / IR-F-02):
  - EXPLICIT propositions / facts        (the shared ground + the textual distinction)
  - RECONSTRUCTED warrant                (a rule/preference, not a fact)
  - OBJECTION                           (dialectical context — NOT a premise; encoded as the defeasible
                                          move the reply undercuts)
"""
from __future__ import annotations

from patala_ml.gold002 import build_gold_002


# ── 1. THE PROJECTION ─────────────────────────────────────────────────────────
def project_arg002(gold: dict | None = None) -> dict:
    """Project ARG-002 v2's inferential core into an ASPIC+ theory (v1, converse fixed).

    Propositions (atoms): art, vikalpa, constructed, not_constructed, not_vikalpa.
      - art         = the 'I'-awareness is linguistically articulated (shared ground)
      - vikalpa     = the 'I'-awareness is a conceptual construction
      - constructed = the 'I'-awareness is produced by constructive/determinative operations
      - not_constructed / not_vikalpa = their negations
    Facts (strict premises):
      - art                         (shared ground: it IS linguistically expressed)
      - not_constructed             (G2-TC2: the 'I'-awareness is NOT one of those constructed relations)
    Rules:
      - r_opp  (DEFEASIBLE): art => vikalpa          (the OBJECTION collapsed: word-joined -> vikalpa)
      - r_tc1  (DEFEASIBLE): vikalpa => constructed  (G2-TC1 in the CORRECT direction: vikalpa works
                                                      through constructive operations -> if vikalpa then
                                                      constructed; NOT the converse)
      - r_reply (STRICT):   not_constructed -> not_vikalpa  (the reply's reconstructed modus tollens from
                                                      G2-TC1 + G2-TC2: if not constructed then not vikalpa)
    Contraries: constructed <-> not_constructed; vikalpa <-> not_vikalpa.

    The reconstructed warrant G2-IMPL is NOT a node/premise — it is carried by the reply rule (and belongs
    on the InferenceRule, not as an ordinary Proposition). The objection G2-OBJ is dialectical context; it
    enters ONLY as the defeasible rule r_opp it implies. G2-IC1 stays out of ASPIC (native grounding).
    """
    return {
        "gold_id": "ARG-GOLD-002",
        "version": "v2-aspic-v1",
        "propositions": ["art", "vikalpa", "constructed", "not_constructed", "not_vikalpa"],
        "facts": ["art", "not_constructed"],
        "rules": [
            {"label": "r_opp", "strict": False, "premises": ["art"], "conclusion": "vikalpa"},
            {"label": "r_tc1", "strict": False, "premises": ["vikalpa"], "conclusion": "constructed"},
            {"label": "r_reply", "strict": True, "premises": ["not_constructed"], "conclusion": "not_vikalpa"},
        ],
        "contraries": [("constructed", "not_constructed"), ("not_constructed", "constructed"),
                       ("vikalpa", "not_vikalpa"), ("not_vikalpa", "vikalpa")],
        "fidelity_notes": [
            "OBJECTION collapsed to one defeasible rule r_opp: art => vikalpa (the opponent's actual claim).",
            "G2-TC1 encoded in the CORRECT direction (vikalpa => constructed), NOT the converse.",
            "RECONSTRUCTED warrant (G2-IMPL) is NOT a node — carried by the reply rule r_reply "
            "(modus tollens: not_constructed -> not_vikalpa). Warrant belongs on the InferenceRule.",
            "INTERPRETIVE claim G2-IC1 is out of ASPIC scope (stays in Pāṭala as grounding).",
        ],
    }


# ── 2. MINIMAL ABSTRACT-ACCEPTABILITY (grounded semantics) — PILOT FALLBACK ───
def _build_af(proj: dict, include_defeater: bool) -> dict:
    """Build the abstract argumentation framework for the projection.

    Arguments are forward-chained from facts through rules. Attacks follow from contraries on
    conclusions, and an attack on a sub-argument attacks the parent (defeat by sub-argument).
    """
    facts = list(proj["facts"])
    if not include_defeater:
        facts = [f for f in facts if f != "not_constructed"]
    contr = {a: b for a, b in proj["contraries"]}  # a's contrary is b
    contr.update({b: a for a, b in proj["contraries"]})

    args = {}          # arg_id -> {conclusion, sub_args, strict}
    seen = set()       # (conclusion, tuple(sub_args)) dedup
    for f in facts:
        args[f"arg_{f}"] = {"conclusion": f, "sub_args": [], "strict": True}
        seen.add((f, ()))
    # forward-chain rules (bounded, deduped — avoids infinite regeneration)
    changed = True
    while changed:
        changed = False
        for rule in proj["rules"]:
            (prem,) = rule["premises"]
            for aid, a in list(args.items()):
                if a["conclusion"] == prem:
                    sig = (rule["conclusion"], tuple(sorted(a["sub_args"] + [aid])))
                    if sig in seen:
                        continue
                    cid = f"arg_{len(args)}"
                    # an argument is defeasible iff it uses a defeasible rule (or inherits from a sub-arg)
                    strict = rule["strict"] and all(args[s]["strict"] for s in a["sub_args"] + [aid])
                    args[cid] = {"conclusion": rule["conclusion"], "sub_args": [aid], "strict": strict}
                    seen.add(sig)
                    changed = True

    # attacks: attacker attacks target if the attacker's conclusion is a contrary of a conclusion
    # that appears in the target's support (including the target's own conclusion)
    def supports(target: dict) -> list[str]:
        out = [target["conclusion"]]
        for s in target["sub_args"]:
            out += supports(args[s])
        return out

    # DEFEAT = attack, with ASPIC+ preference: a strict argument defeats a defeasible one it attacks,
    # but a defeasible argument does NOT defeat a strict one it attacks.
    attacks = {aid: set() for aid in args}  # attacks[target] = attackers
    defeats = {aid: set() for aid in args}  # defeats[target] = effective attackers (after preference)
    ids = list(args)
    for t in ids:
        t_support = supports(args[t])
        for a in ids:
            a_conc = args[a]["conclusion"]
            if a_conc in {contr.get(s) for s in t_support}:
                attacks[t].add(a)
                # effective if not (attacker defeasible AND target strict)
                if not (not args[a]["strict"] and args[t]["strict"]):
                    defeats[t].add(a)
    return {"arguments": ids, "attacks": attacks, "defeats": defeats, "args": args}


def grounded_acceptable(af: dict) -> set[str]:
    """Grounded semantics over the DEFEAT relation (ASPIC+ preference applied).

    acceptable(a) iff every effective attacker (defeater) of a is defeated by some acceptable argument.
    """
    S: set[str] = set()
    while True:
        S2 = {a for a in af["arguments"]
              if all(any(d in S for d in af["defeats"][b]) for b in af["defeats"][a])}
        if S2 == S:
            break
        S = S2
    return S


def acceptable_conclusions(af: dict) -> set[str]:
    """Conclusions that have at least one acceptable argument."""
    acc = grounded_acceptable(af)
    return {af["args"][a]["conclusion"] for a in acc}


def run_arg002_aspic(with_defeater: bool) -> dict:
    """Run ARG-002 v2 under the minimal pilot evaluator. Returns the acceptability result."""
    proj = project_arg002()
    af = _build_af(proj, include_defeater=with_defeater)
    acc_concls = acceptable_conclusions(af)
    return {
        "with_defeater": with_defeater,
        "acceptable_conclusions": sorted(acc_concls),
        "vikalpa_acceptable": "vikalpa" in acc_concls,
        "n_arguments": len(af["arguments"]),
    }
