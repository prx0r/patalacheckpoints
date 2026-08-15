# research_packet — Research Packet (#9)

A **standalone** question → evidence-packet engine using **real graph retrieval (PathRAG flow)** over
real IPVV passages. A question returns exact lexical matches AND the graph-relevant neighborhood.

## Run
```bash
cd /root/patalacheckpoints
PYTHONPATH=pipeline python3 pipeline/products/research_packet/test.py   # 5/5 proof
PYTHONPATH=pipeline python3 pipeline/products/research_packet/engine.py "eternal self memory"
```

## Engine API
```python
from products.research_packet.engine import research_packet
pkt = research_packet("eternal self memory")
```

## Requires
`networkx` (PathRAG flow). Installed into system python; the product also runs under the `/root/venv`.

## Honest limits
- Retrieval = lexical seed + PathRAG flow (graph-structured, not semantic embedding). HippoRAG/ToG-2
  modes exist in `lib/retrieval.py` but are not all wired here yet.
- Graph is over passages (nodes) weighted by shared terms; a finer-grained concept graph is a later
  improvement.
