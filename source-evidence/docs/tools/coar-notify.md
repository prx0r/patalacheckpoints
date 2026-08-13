# COAR Notify — interoperable peer-review federation (Pāṭala as scholarly protocol)

**What Pāṭala borrows:** the protocol connecting repositories with peer-review services and overlay journals
using Linked Data Notifications + ActivityStreams. Supported by DSpace, OPS, Kotahi, PREreview, PCI. **Pāṭala does
not need to become a journal** — it can be a review service in the Publish–Review–Curate ecosystem, where multiple
review communities independently review/endorse the same work (no one truth authority).

**License:** protocol/open (an interoperability standard).

## Usage (protocol, not a service you run immediately)
```
repository/paper elsewhere → COAR Notify → Pāṭala Review → structured adversarial review → COAR Notify →
repository/publisher/overlay journal
```
Document the adapter contract now; run infrastructure later.

## How Pāṭala consumes it
Maps to the "Pāṭala as scholarly protocol" vision — federated review, not a single venue. Add COAR Notify to the
high-priority interoperability list (alongside OpenReview/Kotahi/Janeway/PubPub).

**Priority: document the adapter contract; no infrastructure yet.**
