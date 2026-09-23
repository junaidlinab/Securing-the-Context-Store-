# Use Case 2: Securing the Context Store on SAP HANA Cloud

## The scenario

Use case 1 built a governed context store and used it to ground answers. But that store holds the firm's most sensitive material. Names, account details, risk findings, numbers that are not meant for everyone. Before any of it is sent to an external LLM, it has to be protected.

A financial firm cannot just ship raw context to a model. Some columns identify people. Some rows belong to one department only. Some text has names buried inside it. If that leaves the building unprotected, it is a data problem and a compliance problem at the same time.

## What we are doing

We protect the context store inside SAP HANA Cloud, before anything leaves the SAP boundary. The financial data stays usable for grounding, but what a user can see is controlled, and personal data is taken out of the text.

Here is what we apply:

* Dynamic data masking. Identifying columns are hidden from users who do not have the right privilege.
* K-anonymity. Identifying attributes are generalized so a single row cannot be traced to one person or team.
* L-diversity. A sensitive attribute is protected so each group keeps enough variety to stay anonymous.
* Differential privacy. Calibrated noise is added to numeric signals so individual values cannot be read off.
* Row level security. A user only ever retrieves rows from their own department.
* Text body PII detection. Names and other personal data inside the free text are found and removed with Microsoft Presidio.

The database techniques run inside HANA. The text step runs outside it, because the free text is where HANA's own masking stops.

## Why this matters for the client

* The data is protected before it reaches the model. Sensitive columns, rows, and text are handled inside HANA, not after the fact.
* Access follows the person. A user sees only what their role allows, through the same retrieval query.
* Personal data does not leak into the prompt. The text is cleaned before it is ever sent to an LLM.
* It fits regulated work. Masking, anonymization, and row level access are the controls an auditor expects to see.
* Nothing leaves the SAP boundary unprotected. The protection sits on the same HANA Cloud platform the client already runs.

---

## What's in this pack

Two files.

## companion_script.sql

Run this file in the SAP HANA Database Explorer against your HANA Cloud instance. It creates a financial reporting context store (`FIN_REPORT_CONTEXT`), loads a small sample dataset with embeddings generated inside the database, and then demonstrates each protection technique in turn: dynamic data masking, k-anonymity, l-diversity, differential privacy, and row level security. A retrieval query using cosine similarity still returns grounded results through the protected views.

Run it top to bottom. To see masking take effect, run the check queries as a user who does not have the `UNMASKED` privilege. The table owner sees the unmasked values, so use a different user to see the masking work.

Prerequisites:

* SAP HANA Cloud instance with the Vector Engine enabled
* Data Privacy and anonymization features enabled
* Embedding model available: `SAP_NEB.20240715`
* Privilege to create tables, views, roles, and masks

## presidio_pii_detection.py

A standalone Python script that finds and removes personal data from the text of a retrieved chunk, using Microsoft Presidio. It runs on its own and does not need the HANA instance.

Install and run:

```
pip install presidio-analyzer presidio-anonymizer
python -m spacy download en_core_web_lg
python presidio_pii_detection.py
```
Author: Junaid Ahmed
 Contact: junaid.linab@gmail.com
