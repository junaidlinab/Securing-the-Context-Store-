# ============================================================
# Text-Body PII Detection and Anonymization — Microsoft Presidio
# Companion script — Securing the Context Store
# ============================================================
#
# WHAT THIS SCRIPT DOES
# ---------------------
# SAP HANA Cloud's native masking and anonymization protect structured
# columns, but the free-text body of a context chunk (stored as NCLOB)
# can still contain names and other identifiers. This script detects and
# anonymizes PII in that text with Microsoft Presidio, before the context
# package is sent to an external LLM.
#
# WHAT IS ACHIEVED
# ----------------
# Given a retrieved context chunk, the script reports the PII entities it
# finds (people, locations, etc.) and returns an anonymized version of the
# text with those entities replaced by a redaction token, while leaving
# domain terms such as "EBITDA" untouched via an allow list.
#
# HOW TO RUN
# ----------
# Runs standalone (e.g. Google Colab or any Python 3.9+ environment),
# independent of the HANA instance:
#     pip install presidio-analyzer presidio-anonymizer
#     python -m spacy download en_core_web_lg
#     python presidio_pii_detection.py
# ============================================================

from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# A context chunk retrieved from the store, before it reaches the LLM.
chunk_text = (
    "Revenue for Q4 2023 reached EUR 142.3 million, a 12% increase "
    "year-over-year. CFO Maria Steinberg noted that the EBITDA margin "
    "improved to 18.4%, driven by cost optimization in the EMEA region."
)

# Domain terms that must not be treated as PII. Some models flag
# financial acronyms such as EBITDA as organizations; the allow list
# keeps them in the text.
ALLOW_LIST = ["EBITDA", "EMEA"]

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# 1) Detect
results = analyzer.analyze(
    text=chunk_text,
    language="en",
    allow_list=ALLOW_LIST,
)

print("Detected entities:")
for r in results:
    print(
        f"  {r.entity_type:12} | pos {r.start:>3}-{r.end:<3} | "
        f"score {r.score:.2f} | '{chunk_text[r.start:r.end]}'"
    )

# 2) Anonymize — replace every detected entity with a single redaction token
operators = {"DEFAULT": OperatorConfig("replace", {"new_value": "[REDACTED]"})}
anonymized = anonymizer.anonymize(
    text=chunk_text,
    analyzer_results=results,
    operators=operators,
)

print("\nAnonymized text:")
print(anonymized.text)
