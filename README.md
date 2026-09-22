# Securing the Context Store — Anonymization, Masking, and PII Protection on SAP HANA Cloud

Companion code for the article on securing an enterprise RAG context store on SAP HANA Cloud.

## What This Covers

An enterprise RAG context store holds sensitive business content that is eventually sent to an external LLM. This companion shows how to protect that content **before it leaves the SAP boundary**, using SAP HANA Cloud's native security features plus a text-layer PII step:

1. **Dynamic data masking** — hide identifying columns based on privilege
2. **K-anonymity** — generalize quasi-identifiers so records aren't uniquely identifiable
3. **L-diversity** — protect a sensitive structured attribute within each group
4. **Differential privacy** — add calibrated noise to numeric signals
5. **Row-level security** — scope vector retrieval to a user's own rows
6. **Text-body PII detection** — anonymize the free-text chunk with Microsoft Presidio

All five database techniques run against the same financial-reporting context store, and a retrieval query using cosine similarity still returns grounded results through the protected views.

## Prerequisites

- SAP HANA Cloud instance with the Vector Engine enabled
- Data Privacy / anonymization features enabled
- Embedding model available: `SAP_NEB.20240715`
- Privilege to create tables, views, roles, and masks
- For the PII step only: Python 3.9+ with `presidio-analyzer`, `presidio-anonymizer`, and the spaCy `en_core_web_lg` model

## Files

- `companion_script.sql` — Self-contained SQL: creates the context store, loads a small sample dataset with in-database embeddings, and demonstrates masking, k-anonymity, l-diversity, differential privacy, and row-level security. Run top to bottom in the SAP HANA database explorer SQL console.
- `presidio_pii_detection.py` — Standalone Python script that detects and anonymizes PII in a retrieved context chunk. Runs independently of the HANA instance.

## How to Run

**SQL (HANA instance only):** open `companion_script.sql` in the SAP HANA database explorer SQL console (or hdbsql / DBeaver) connected to your instance and run it top to bottom. To see masking take effect, run the verification `SELECT`s as a user without the `UNMASKED` privilege.

**PII step (Python):**
```
pip install presidio-analyzer presidio-anonymizer
python -m spacy download en_core_web_lg
python presidio_pii_detection.py
```

## Author

Junaid Ahmed
