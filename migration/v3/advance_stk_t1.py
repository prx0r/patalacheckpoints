#!/usr/bin/env python3
"""advance_stk_t1.py — run the REAL factory batch on Stk, committing T1 to the REAL object_registry.

The actual pipeline (factory_batch._produce_layer → worker → R.commit), not the lab demo. The Stk
work is committed as SOURCE (184 objects). This advances SOURCE→T1 via the real Hermes t1_worker,
committing MACHINE_PROPOSED T1 objects to the real registry.

Run: nohup python3 migration/v3/advance_stk_t1.py > /tmp/opencode/stk_t1.log 2>&1 &
"""
import sys, json, time
sys.path.insert(0, "/root/projects/patala/pipeline")
import object_registry as R
import factory_batch as FB

WORK = "sardhatrisatikalottara"

def main():
    # load the real Stk SOURCE objects from the REGISTRY PAYLOAD (the real Sanskrit), not the jsonl
    src = R._load("SOURCE")["objects"]
    inputs = []
    for oid in sorted(src):
        if not oid.startswith(WORK):
            continue
        v = src[oid][-1]
        verse = (v.get("payload", {}).get("verse") or "").strip()
        # skip the header rows (title / 'Based on the edition')
        if verse and not verse.startswith(("Sārdhatriś", "Sardhatri")) and "Based on" not in verse:
            inputs.append({"object_id": oid, "input_hash": v.get("input_hash", ""), "verse": verse})
        if len(inputs) >= 8:
            break
    print(f"Loaded {len(inputs)} real Stk SOURCE objects from the registry payloads")
    if not inputs:
        print("NO verses — check registry payloads")
        return
    print("First input:", inputs[0]["verse"][:50])

    # run the REAL factory T1 layer (Hermes worker + validator + R.commit)
    print("\nRunning the REAL factory batch T1 layer (Hermes)...")
    res = FB._produce_layer("T1", inputs, batch_size=4)
    print("factory result:", json.dumps(res, default=str)[:400])

    # verify the real registry
    t1_objs = R._load("T1")["objects"]
    stk_t1 = [k for k in t1_objs if k.startswith(WORK)]
    print(f"\n=== REGISTRY AFTER T1 ===")
    print(f"  Stk T1 objects committed: {len(stk_t1)}")
    print(f"  SOURCE total: {len(R._load('SOURCE')['objects'])}")

if __name__ == "__main__":
    main()
