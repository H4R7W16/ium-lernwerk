import unittest

from scripts.validate_phase0 import (
    ValidationError,
    validate_claim_ledger,
    validate_source_register,
)


def valid_source(**overrides):
    source = {
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
    }
    source.update(overrides)
    return source


def valid_claim(**overrides):
    claim = {
        "id": "CLAIM-INF-001",
        "package": "informatikdidaktik",
        "statement": "Codeverständnis braucht gezielte Aufgaben.",
        "scope": "Sekundarstufe I",
        "status": "working",
        "evidenceLevel": "medium",
        "sourceIds": ["SRC-001"],
        "limitations": "Die Aussage gilt nicht automatisch für jede Lerngruppe.",
        "designImplications": ["Codeerklärung als Lernhandlung vorsehen."],
    }
    claim.update(overrides)
    return claim


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

    def test_source_with_any_missing_required_field_is_rejected(self):
        required_fields = (
            "id",
            "package",
            "sourceKind",
            "title",
            "authors",
            "year",
            "url",
            "doi",
            "license",
            "accessed",
            "verificationStatus",
            "relevance",
        )

        for field in required_fields:
            source = valid_source()
            del source[field]

            with self.subTest(field=field):
                with self.assertRaises(ValidationError):
                    validate_source_register({"schemaVersion": 1, "sources": [source]})

    def test_source_with_invalid_required_field_type_is_rejected(self):
        invalid_values = {
            "id": 1,
            "package": 1,
            "title": 1,
            "authors": "Institution A",
            "year": "2026",
            "url": 1,
            "doi": 1,
            "license": 1,
            "accessed": 20260728,
            "relevance": "curriculum",
        }

        for field, value in invalid_values.items():
            with self.subTest(field=field):
                with self.assertRaises(ValidationError):
                    validate_source_register(
                        {
                            "schemaVersion": 1,
                            "sources": [valid_source(**{field: value})],
                        }
                    )

    def test_source_id_requires_ascii_src_prefix(self):
        for source_id in ("Quelle-ä", "X1"):
            with self.subTest(source_id=source_id):
                with self.assertRaises(ValidationError):
                    validate_source_register(
                        {
                            "schemaVersion": 1,
                            "sources": [valid_source(id=source_id)],
                        }
                    )


class ClaimLedgerTests(unittest.TestCase):
    def test_reviewed_claim_requires_registered_source(self):
        payload = {"schemaVersion": 1, "claims": [valid_claim(
            status="reviewed",
            sourceIds=["SRC-NOT-REGISTERED"],
        )]}

        with self.assertRaises(ValidationError):
            validate_claim_ledger(payload, {"SRC-001"})

    def test_claim_with_any_missing_required_field_is_rejected(self):
        required_fields = (
            "id",
            "package",
            "statement",
            "scope",
            "status",
            "evidenceLevel",
            "sourceIds",
            "limitations",
            "designImplications",
        )

        for field in required_fields:
            claim = valid_claim()
            del claim[field]

            with self.subTest(field=field):
                with self.assertRaises(ValidationError):
                    validate_claim_ledger({"schemaVersion": 1, "claims": [claim]}, {"SRC-001"})

    def test_claim_with_invalid_required_field_type_is_rejected(self):
        invalid_values = {
            "id": 1,
            "package": 1,
            "statement": 1,
            "scope": 1,
            "sourceIds": "SRC-001",
            "limitations": 1,
            "designImplications": "Codeerklärung vorsehen.",
        }

        for field, value in invalid_values.items():
            with self.subTest(field=field):
                with self.assertRaises(ValidationError):
                    validate_claim_ledger(
                        {
                            "schemaVersion": 1,
                            "claims": [valid_claim(**{field: value})],
                        },
                        {"SRC-001"},
                    )

    def test_reviewed_claim_rejects_registered_source_without_primary_check(self):
        source_ids = validate_source_register(
            {
                "schemaVersion": 1,
                "sources": [valid_source(verificationStatus="metadata-checked")],
            }
        )

        with self.assertRaises(ValidationError):
            validate_claim_ledger(
                {"schemaVersion": 1, "claims": [valid_claim(status="reviewed")]},
                source_ids,
            )

    def test_reviewed_and_standard_claims_reject_plain_source_id_set(self):
        for status in ("reviewed", "standard"):
            with self.subTest(status=status):
                with self.assertRaises(ValidationError):
                    validate_claim_ledger(
                        {"schemaVersion": 1, "claims": [valid_claim(status=status)]},
                        {"SRC-001"},
                    )

    def test_working_claim_accepts_plain_source_id_set(self):
        claim_ids = validate_claim_ledger(
            {"schemaVersion": 1, "claims": [valid_claim()]},
            {"SRC-001"},
        )

        self.assertEqual(claim_ids, {"CLAIM-INF-001"})

    def test_claim_id_requires_ascii_documented_prefix(self):
        for claim_id in ("Claim-ä", "X1"):
            with self.subTest(claim_id=claim_id):
                with self.assertRaises(ValidationError):
                    validate_claim_ledger(
                        {
                            "schemaVersion": 1,
                            "claims": [valid_claim(id=claim_id)],
                        },
                        {"SRC-001"},
                    )

    def test_reviewed_claim_requires_limitations_after_source_registration(self):
        source_ids = validate_source_register(
            {"schemaVersion": 1, "sources": [valid_source()]}
        )

        with self.assertRaises(ValidationError):
            validate_claim_ledger(
                {
                    "schemaVersion": 1,
                    "claims": [valid_claim(status="reviewed", limitations="")],
                },
                source_ids,
            )

    def test_standard_claim_requires_limitations_after_source_registration(self):
        source_ids = validate_source_register(
            {"schemaVersion": 1, "sources": [valid_source()]}
        )

        with self.assertRaises(ValidationError):
            validate_claim_ledger(
                {
                    "schemaVersion": 1,
                    "claims": [valid_claim(status="standard", limitations="")],
                },
                source_ids,
            )


if __name__ == "__main__":
    unittest.main()
