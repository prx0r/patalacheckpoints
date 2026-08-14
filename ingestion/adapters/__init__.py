"""ingestion/adapters/ — concrete external-source ReconciliationAdapters (the real gap).

ALIGNED: the adapter contract is `source-evidence/schema/external_record.py::ReconciliationAdapter`.
Each adapter below implements that contract for one external source. Add new sources by subclassing
the same contract (SARIT, OpenAlex, Crossref, Gyan Bharatam, ...) — never a parallel abstraction.
"""
