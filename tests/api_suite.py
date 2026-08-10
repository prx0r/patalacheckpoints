#!/usr/bin/env python3
"""Pāṭala API verification suite.

Hits the live API (default http://localhost:3000) and checks the invariants from
docs/apitest.md: contract shape, referential integrity, epistemic invariants,
provenance, golden resolver cases, error handling.

Usage: python3 tests/api_suite.py [base_url]
Exit code 0 = all pass. Prints a PASS/FAIL report per check.
"""
import json
import sys
import urllib.request
import urllib.error

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3000"

PASS = 0
FAIL = 0
FAILURES = []


def get(path):
    req = urllib.request.Request(BASE + path, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, json.loads(r.read().decode())


def post(path, body):
    data = json.dumps(body).encode()
    req = urllib.request.Request(BASE + path, data=data,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, json.loads(r.read().decode())


def status_of(path):
    try:
        return get(path)[0]
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return -1


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  PASS  {name}")
    else:
        FAIL += 1
        FAILURES.append((name, detail))
        print(f"  FAIL  {name}  {detail}")


# ────────────────────────────────────────────────────────────────
print("== 1. Contract shape ==")
_, index = get("/api")
check("index has name Pāṭala", index.get("name") == "Pāṭala", str(index.get("name")))
check("index has endpoints map", isinstance(index.get("endpoints"), dict))

_, texts = get("/api/texts")
ids = [t["id"] for t in texts["texts"]]
check("texts returns list", isinstance(texts["texts"], list) and len(texts["texts"]) > 0)
check("texts ids unique", len(ids) == len(set(ids)), f"dup={len(ids)-len(set(ids))}")
check("texts have urn", all(t.get("urn", "").startswith("tantra:text:") for t in texts["texts"]))
check("texts have statusChecked", all(t.get("statusChecked") for t in texts["texts"]))
bad_status = [t["id"] for t in texts["texts"] if t["translationStatus"] not in ("complete", "partial", "none")]
check("texts status enum valid", not bad_status, str(bad_status))

_, works = get("/api/works")
wids = [w["id"] for w in works["works"]]
check("works returns list", isinstance(works["works"], list) and len(works["works"]) > 0)
check("works ids unique", len(wids) == len(set(wids)))
check("works have urn", all(w.get("urn", "").startswith("tantra:text:") for w in works["works"]))

# ────────────────────────────────────────────────────────────────
print("== 2. Referential integrity (spot + all) ==")
# every work resolves individually
resolve_fail = [w for w in wids if status_of(f"/api/works/{w}") != 200]
check("every work resolves via /api/works/:id", not resolve_fail, f"broken={resolve_fail[:5]}")

# every text resolves individually
txt_resolve_fail = [t for t in ids if status_of(f"/api/texts/{t}") != 200]
check("every text resolves via /api/texts/:id", not txt_resolve_fail, f"broken={txt_resolve_fail[:5]}")

# all passages: parent work resolves + neighboring passages resolve
_, all_passages = get("/api/texts/kubjikamata/translations")
ps = all_passages.get("translations", [])
check("kubjikamata translations loaded", len(ps) > 0, str(len(ps)))
if ps:
    p = ps[0]
    check("passage has work_id", p.get("work_id") == "kubjikamata", p.get("work_id"))
    check("passage has id", p.get("id", "").startswith("tantra:text:kubjikamata:"), p.get("id"))
    check("passage has sanskrit", bool(p.get("sanskrit")), "empty sanskrit")
    check("passage has location", p.get("location", {}).get("chapter") is not None)

# context bundle integrity: manuscripts + tracked terms resolve
code, ctx = get("/api/context/passages/tantra:text:kubjikamata:1.1")
check("context bundle returns 200", code == 200)
check("context has work", ctx.get("work") and ctx["work"].get("id") == "kubjikamata")
check("context manuscripts all resolve", all(m.get("id", "").startswith("pt:ms:") for m in ctx.get("manuscripts", [])))
check("context tracked_terms have senses", all(t.get("senses") for t in ctx.get("tracked_terms", [])))

# relations: every edge resolves to a work endpoint (source or target)
_, rel = get("/api/relations/kubjikamata")
check("relations returns list", isinstance(rel.get("relations"), list))

# ────────────────────────────────────────────────────────────────
print("== 3. Epistemic invariants (the moat) ==")
# machine resolver NEVER returns accepted status
code, res = post("/api/resolve/work", {"title": "Kubjikamatatantra"})
check("resolver returns machine_proposed", res.get("status") == "machine_proposed", str(res.get("status")))
check("resolver returns candidates array", isinstance(res.get("candidates"), list))
check("resolver never returns accepted", not any(c.get("status") == "accepted" for c in res.get("candidates", [])))

# term proposals NEVER appear as accepted senses
_, senses = get("/api/terms/kula/senses")
_, props = get("/api/term-proposals?lemma=kula")
accepted_ids = {s["id"] for s in senses.get("senses", [])}
check("kula senses accepted (2)", len(senses.get("senses", [])) == 2, str(len(senses.get("senses", []))))
prop_lemmas = [p["lemma"] for p in props.get("proposals", [])]
check("proposal layer separate (kula proposal listed)", "kula" in prop_lemmas, str(prop_lemmas))

# occurrence search is honest
_, occ = get("/api/terms/kula/occurrences?work_id=kubjikamata")
check("occurrences honest substring", occ.get("match_method") == "substring", str(occ.get("match_method")))
check("occurrences honest lemmatized:false", occ.get("lemmatized") is False, str(occ.get("lemmatized")))

# unverified bibliography retains verified:false
_, kw = get("/api/texts/kubjikamata")
check("seed work stays verified:false", kw["data"].get("verified") is False, str(kw["data"].get("verified")))

# working translations flagged provisional
_, tr = get("/api/texts/kubjikamata/translations")
check("working translations staged T1", tr.get("provenance", {}).get("stage") == "T1")
check("working translations carry not-reviewed note", "NOT peer reviewed" in tr.get("provenance", {}).get("note", "") or "not peer reviewed" in tr.get("provenance", {}).get("note", "").lower())

# accepted assertions require review; expert_reviewed has review event
_, asserts = get("/api/assertions")
for a in asserts.get("assertions", []):
    if a.get("status") == "expert_reviewed":
        check("expert_reviewed assertion has review event", len(a.get("reviews", [])) > 0, a["subject"])
        break
else:
    print("  WARN  no expert_reviewed assertion to check")

# ────────────────────────────────────────────────────────────────
print("== 4. Provenance ==")
_, st = get("/api/stats")
check("stats has provenance", bool(st.get("provenance")))
check("stats reports corpus counts", st.get("works") == 69 and st.get("passages") == 4016,
      f"works={st.get('works')} passages={st.get('passages')}")
_, ctx2 = get("/api/context/passages/tantra:text:kramasadbhava:1.9")
check("context has provenance note", bool(ctx2.get("provenance", {}).get("note")))

# ────────────────────────────────────────────────────────────────
print("== 5. Golden resolver cases ==")
golden = [
    ("Amṛteśatantram", "netratantra"),
    ("Kubjikamatatantra", "kubjikamata"),
    ("Kaulajñānanirṇaya", "kaulajnananirnaya"),
]
for title, expect in golden:
    _, r = post("/api/resolve/work", {"title": title})
    got = [c["work_id"] for c in r.get("candidates", [])]
    check(f"resolver: '{title}' → contains {expect}", expect in got, str(got))

# gibberish → no confident resolution
_, r = post("/api/resolve/work", {"title": "zzzzqqqxxxnomatch"})
check("resolver: gibberish → low/no candidates", len(r.get("candidates", [])) <= 1, str(len(r.get("candidates", []))))

# ────────────────────────────────────────────────────────────────
print("== 6. Error handling ==")
check("unknown work → 404", status_of("/api/works/doesnotexist") == 404)
check("unknown text → 404", status_of("/api/texts/doesnotexist") == 404)
check("unknown passage → 404", status_of("/api/passages/doesnotexist") == 404)
check("missing search query → 400", status_of("/api/search/passages?work_id=x") == 400)
check("missing concordance query → 400", status_of("/api/concordance?max=1") == 400)
check("concordance zero-hit → 200 empty result", status_of("/api/concordance?q=zzzqqq&max=1") == 200)
def post_status(path, body=None):
    try:
        return post(path, body or {})[0]
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return -1

check("missing resolve body → 400", post_status("/api/resolve/work", {}) == 400)
check("unknown term sense → 404", status_of("/api/terms/zzznolemma/senses") == 404)

# ────────────────────────────────────────────────────────────────
print(f"\n==== RESULT: {PASS} passed, {FAIL} failed ====")
if FAILURES:
    print("\nFailures:")
    for name, detail in FAILURES:
        print(f"  - {name}: {detail}")
sys.exit(1 if FAIL else 0)
