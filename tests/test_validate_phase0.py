import unittest

from scripts.validate_phase0 import (
    ValidationError,
    validate_claim_ledger,
    validate_source_register,
)


class SourceRegisterTests(unittest.TestCase):
    def test_duplicate_source_id_is_rejected(self):
        payload = {
            "schemaVersion": 1,
            "sources": [
                {
                    "id": "SRC-001",
                    "package": "official",
                    "sourceKind": "official",
                    "title": "Quelle A",
                    "authors": ["Institution A"],
                    "year": 2026,
                    "url": "https://example.org/a",
                    "doi": None,
                    "license": "unknown",
                    "accessed": "2026-07-28",
                    "verificationStatus": "primary-checked",
                    "relevance": ["curriculum"],
                },
                {
                    "id": "SRC-001",
                    "package": "official",
                    "sourceKind": "official",
                    "title": "Quelle B",
                    "authors": ["Institution B"],
                    "year": 2026,
                    "url": "https://example.org/b",
                    "doi": None,
                    "license": "unknown",
                    "accessed": "2026-07-28",
                    "verificationStatus": "primary-checked",
                    "relevance": ["curriculum"],
                },
            ],
        }

        with self.assertRaises(ValidationError):
            validate_source_register(payload)


class ClaimLedgerTests(unittest.TestCase):
    def test_reviewed_claim_requires_registered_source_and_limitations(self):
        payload = {
            "schemaVersion": 1,
            "claims": [
                {
                    "id": "CLAIM-INF-001",
                    "package": "informatikdidaktik",
                    "statement": "Codeverständnis braucht gezielte Aufgaben.",
                    "scope": "Sekundarstufe I",
                    "status": "reviewed",
                    "evidenceLevel": "medium",
                    "sourceIds": ["SRC-NOT-REGISTERED"],
                    "limitations": "",
                    "designImplications": ["Codeerklärung als Lernhandlung vorsehen."],
                }
            ],
        }

        with self.assertRaises(ValidationError):
            validate_claim_ledger(payload, {"SRC-001"})


if __name__ == "__main__":
    unittest.main()
