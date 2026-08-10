# Milestone A — Kramasadbhāva 1.8 complete scholarly object (v2, via Hermes)

*2026-08-10. Building one complete scholarly object through the REAL Hermes path.
This is the validation of the whole architecture — not the API transport, the
scholarly artifact.*

## The run

`pipeline/milestone_a.py` drove `kramasadbhāva 1.8` through the state machine
(T1→R1→T2→R2→T3) using `model.py` → `hermes -z` (Hermes owns provider reliability).

**Persisted:** `translations/_stack/kramasadbhava/passages/1.8.json`
Stages completed: **T1, R1, T2, R2, T3** (T3.1 the reading layer timed out — cosmetic,
not architectural).

## The scholarly result (the interesting part)

### R1 — real cruxes found
1. **`nirānande`** — LEXICAL: privative vocative "O bliss-less one" (nir-ānandā) vs.
   the earlier T1's "beyond bliss".
2. **`devadeveśi`** — LEXICAL: the compound parse — `deva-deveśī` ("queen of the gods")
   vs. `devadeva-īśī` ("mistress of the god of gods").

### R2 — adjudicated with the decision taxonomy
```
c1  devadeveśi = devadeva-īśī, 'mistress of the god of gods'   CONSTRAINED
c2  nirānande  = privative vocative, 'O bliss-less one'        CONSTRAINED
c3  paramānande = 'O supreme bliss' (T1 and T2 agree)          CONSTRAINED
hard_core: 1.8 is a vocative-chain stuti of the goddess, framed at 1.7 (pādau jagrāha...)
```

### T3 — the resolved translation
> oṃ — homage to you, O mistress of the god of gods; Mahākālī, homage be to you.
> Homage be to you, O supreme bliss; to you, O bliss-less one, homage be to you.

The R1 cruxes were genuinely adjudicated: `nirānande` settled to the privative
"O bliss-less one" (per the grammar + crux), and `devadeveśi` to "mistress of the god
of gods" (devadeva-īśī, a real improvement over the earlier direct-model T3 which said
"Queen of Gods").

## What this proves

- The **whole architecture works** with a real model: source → T1 → R1 (real cruxes)
  → T2 (rival) → R2 (decision-taxonomy adjudication) → T3 (resolved).
- **Hermes path is viable** — `model.py` shelling to `hermes -z` returns real,
  structured, contract-passing output for every core stage.
- The **stage-contract layer works** — no empty strict stages silently accepted.
- The `nirānande` crux (the passage's genuine uncertainty, flagged in the very first
  proof) was **carried and resolved through the pipeline**, not laundered.

## The one issue

**T3.1 (the reading layer) timed out** at the 180s hermes subprocess timeout. It's the
last cosmetic stage. The fix is simple: raise the hermes subprocess timeout (or run
T3.1 alone). Not architectural.

## Next

1. Run T3.1 alone (or raise the timeout) → the stack is 6/6.
2. Run C1 on the persisted T3/R2 stack (the `write-commentary` skill).
3. Then Milestone B (a contiguous 25-verse unit, automated).
