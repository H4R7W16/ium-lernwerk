import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from scripts.validate_phase0 import (
    ValidationError,
    validate_claim_ledger,
    validate_crosswalk,
    validate_curriculum_dataset,
    validate_design_principles,
    validate_curriculum_integrations,
    validate_operators,
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
        "normativeStatus": "enacted",
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


def valid_curriculum_record(**overrides):
    record = {
        "id": "LH26-E-DP-001",
        "sourceId": "SRC-CUR-LESEHILFE-2026-27",
        "text": "Die Schülerinnen und Schüler können ein digitales Artefakt erstellen.",
        "grades": [5, 6],
        "level": "E",
        "area": "Digitalität und Partizipation",
        "recordType": "competency",
        "sourceLocator": {
            "page": 5,
            "section": "Klassen 5/6 – Digitalität und Partizipation",
        },
        "status": "verified",
    }
    record.update(overrides)
    return record


def valid_curriculum_payload(records=None, **overrides):
    payload = {
        "schemaVersion": 1,
        "sourceId": "SRC-CUR-LESEHILFE-2026-27",
        "records": records if records is not None else [valid_curriculum_record()],
    }
    payload.update(overrides)
    return payload


def valid_design_principle(**overrides):
    principle = {
        "id": "PRIN-001",
        "title": "Hilfen fachlich dosieren",
        "statement": "Hilfen adressieren konkrete Hürden und erhalten die zentrale Denkhandlung.",
        "claimIds": ["CLAIM-LP-006"],
        "appliesTo": ["Modulphase 4: angeleitet erproben"],
        "status": "working",
        "phase1Implications": [
            "Hilfestufen und ihre fachliche Funktion im Modulmanifest beschreibbar machen."
        ],
        "risks": ["Zu starke Hilfen können die zentrale Denkhandlung übernehmen."],
    }
    principle.update(overrides)
    return principle


def valid_design_principles_payload(principles=None, **overrides):
    payload = {
        "schemaVersion": 1,
        "principles": (
            principles
            if principles is not None
            else [valid_design_principle()]
        ),
    }
    payload.update(overrides)
    return payload


def valid_crosswalk_relation(**overrides):
    relation = {
        "id": "XW-001",
        "fromIds": ["LH26-E-ID-001"],
        "toIds": ["BMB16-GYM-IK-IW-001"],
        "relationship": "overlaps",
        "rationale": "Beide Records verlangen die Nutzung digitaler Angebote zur Recherche.",
        "status": "resolved",
        "followUp": "",
    }
    relation.update(overrides)
    return relation


def valid_crosswalk_payload(relations=None, unmapped_records=None, **overrides):
    relation_payloads = (
        relations
        if relations is not None
        else [valid_crosswalk_relation()]
    )
    unmapped_payloads = (
        unmapped_records
        if unmapped_records is not None
        else []
    )
    curriculum_record_ids = {
        record_id
        for relation in relation_payloads
        for record_id in relation.get("fromIds", [])
        + relation.get("toIds", [])
    } | {
        record.get("recordId")
        for record in unmapped_payloads
        if isinstance(record, dict) and record.get("recordId")
    }
    payload = {
        "schemaVersion": 1,
        "status": "working",
        "requiredSourceComparisons": [],
        "counts": {
            "curriculumRecords": len(curriculum_record_ids),
            "relations": len(relation_payloads),
            "unmappedRecords": len(unmapped_payloads),
            "relationshipCounts": dict(
                sorted(
                    Counter(
                        relation.get("relationship")
                        for relation in relation_payloads
                        if relation.get("relationship")
                    ).items()
                )
            ),
        },
        "relations": relation_payloads,
        "unmappedRecords": unmapped_payloads,
    }
    payload.update(overrides)
    return payload


def valid_operator_entry(**overrides):
    entry = {
        "id": "OPMAP-001",
        "kind": "operator",
        "exactOfficialTerm": "analysieren",
        "sourceRecordId": "BMB16-GYM-OP-002",
        "sourceDefinition": "Materialien oder Sachverhalte systematisch untersuchen.",
        "sourceAfb": "III",
        "expectedObservableAction": "Relevante Bestandteile nach Kriterien herausarbeiten und belegen.",
        "likelyComplexityBand": "independent-transfer-design-and-evaluation",
        "applicableGrades": [5],
        "notesOnAmbiguity": "Die Komplexität hängt von Material und Fragestellung ab.",
        "status": "working",
    }
    entry.update(overrides)
    return entry


def valid_operators_payload(entries=None, **overrides):
    payload = {
        "schemaVersion": 1,
        "status": "working",
        "entries": (
            entries
            if entries is not None
            else [valid_operator_entry()]
        ),
    }
    payload.update(overrides)
    return payload


class SourceRegisterTests(unittest.TestCase):
    def test_official_source_without_normative_status_is_rejected(self):
        source = valid_source()
        del source["normativeStatus"]

        with self.assertRaises(ValidationError):
            validate_source_register({"schemaVersion": 1, "sources": [source]})

    def test_non_official_source_requires_null_normative_status(self):
        with self.assertRaises(ValidationError):
            validate_source_register(
                {
                    "schemaVersion": 1,
                    "sources": [
                        valid_source(
                            sourceKind="secondary",
                            normativeStatus="enacted",
                        )
                    ],
                }
            )

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
                    "normativeStatus": "enacted",
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
                    "normativeStatus": "enacted",
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
            "normativeStatus",
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


class CurriculumDatasetTests(unittest.TestCase):
    def setUp(self):
        self.source_ids = {"SRC-CUR-LESEHILFE-2026-27"}

    def test_valid_dataset_returns_record_ids(self):
        record_ids = validate_curriculum_dataset(
            valid_curriculum_payload(),
            self.source_ids,
        )

        self.assertEqual(record_ids, {"LH26-E-DP-001"})

    def test_schema_version_one_is_required(self):
        with self.assertRaises(ValidationError):
            validate_curriculum_dataset(
                valid_curriculum_payload(schemaVersion=2),
                self.source_ids,
            )

    def test_registered_top_level_source_is_required(self):
        with self.assertRaises(ValidationError):
            validate_curriculum_dataset(
                valid_curriculum_payload(sourceId="SRC-NOT-REGISTERED"),
                self.source_ids,
            )

    def test_duplicate_record_ids_are_rejected(self):
        record = valid_curriculum_record()

        with self.assertRaises(ValidationError):
            validate_curriculum_dataset(
                valid_curriculum_payload(records=[record, dict(record)]),
                self.source_ids,
            )

    def test_empty_text_is_rejected(self):
        with self.assertRaises(ValidationError):
            validate_curriculum_dataset(
                valid_curriculum_payload(
                    records=[valid_curriculum_record(text="  ")]
                ),
                self.source_ids,
            )

    def test_missing_required_record_fields_are_rejected(self):
        required_fields = (
            "id",
            "sourceId",
            "text",
            "grades",
            "level",
            "area",
            "recordType",
            "sourceLocator",
            "status",
        )

        for field in required_fields:
            record = valid_curriculum_record()
            del record[field]

            with self.subTest(field=field):
                with self.assertRaises(ValidationError):
                    validate_curriculum_dataset(
                        valid_curriculum_payload(records=[record]),
                        self.source_ids,
                    )

    def test_invalid_grades_are_rejected(self):
        for grades in ([], "5/6", [0], [5, "6"], [True]):
            with self.subTest(grades=grades):
                with self.assertRaises(ValidationError):
                    validate_curriculum_dataset(
                        valid_curriculum_payload(
                            records=[valid_curriculum_record(grades=grades)]
                        ),
                        self.source_ids,
                    )

    def test_page_must_be_a_positive_integer(self):
        for page in (0, -1, 1.5, True):
            locator = {"page": page, "section": "Klassen 5/6"}

            with self.subTest(page=page):
                with self.assertRaises(ValidationError):
                    validate_curriculum_dataset(
                        valid_curriculum_payload(
                            records=[
                                valid_curriculum_record(sourceLocator=locator)
                            ]
                        ),
                        self.source_ids,
                    )

    def test_locator_section_must_be_nonempty(self):
        with self.assertRaises(ValidationError):
            validate_curriculum_dataset(
                valid_curriculum_payload(
                    records=[
                        valid_curriculum_record(
                            sourceLocator={"page": 5, "section": " "}
                        )
                    ]
                ),
                self.source_ids,
            )

    def test_status_must_be_allowed(self):
        with self.assertRaises(ValidationError):
            validate_curriculum_dataset(
                valid_curriculum_payload(
                    records=[valid_curriculum_record(status="draft")]
                ),
                self.source_ids,
            )

    def test_record_type_must_be_allowed(self):
        with self.assertRaises(ValidationError):
            validate_curriculum_dataset(
                valid_curriculum_payload(
                    records=[valid_curriculum_record(recordType="interpretation")]
                ),
                self.source_ids,
            )

    def test_record_id_must_be_nonempty_ascii(self):
        for record_id in ("", "LH26-Ä-001"):
            with self.subTest(record_id=record_id):
                with self.assertRaises(ValidationError):
                    validate_curriculum_dataset(
                        valid_curriculum_payload(
                            records=[valid_curriculum_record(id=record_id)]
                        ),
                        self.source_ids,
                    )

    def test_record_source_must_match_dataset_source(self):
        with self.assertRaises(ValidationError):
            validate_curriculum_dataset(
                valid_curriculum_payload(
                    records=[valid_curriculum_record(sourceId="SRC-OTHER")]
                ),
                self.source_ids,
            )


class DesignPrincipleTests(unittest.TestCase):
    def setUp(self):
        self.claim_ids = {"CLAIM-LP-006", "CLAIM-INF-004"}

    def test_non_object_payload_is_rejected_with_validation_error(self):
        for payload in ([], None):
            with self.subTest(payload=payload):
                with self.assertRaises(ValidationError):
                    validate_design_principles(payload, self.claim_ids)


class CrosswalkTests(unittest.TestCase):
    def setUp(self):
        self.curriculum_ids = {
            "LH26-E-ID-001",
            "BMB16-GYM-IK-IW-001",
        }

    def test_valid_crosswalk_returns_resolved_union(self):
        resolved_ids = validate_crosswalk(
            valid_crosswalk_payload(),
            self.curriculum_ids,
        )

        self.assertEqual(resolved_ids, self.curriculum_ids)

    def test_unknown_from_or_to_record_id_is_rejected(self):
        invalid_relations = (
            valid_crosswalk_relation(fromIds=["UNKNOWN"]),
            valid_crosswalk_relation(toIds=["UNKNOWN"]),
        )

        for relation in invalid_relations:
            with self.subTest(relation=relation):
                with self.assertRaises(ValidationError):
                    validate_crosswalk(
                        valid_crosswalk_payload(relations=[relation]),
                        self.curriculum_ids,
                    )

    def test_invalid_relationship_is_rejected(self):
        with self.assertRaises(ValidationError):
            validate_crosswalk(
                valid_crosswalk_payload(
                    relations=[
                        valid_crosswalk_relation(
                            relationship="similar"
                        )
                    ]
                ),
                self.curriculum_ids,
            )

    def test_missing_relation_field_is_rejected(self):
        required_fields = (
            "id",
            "fromIds",
            "toIds",
            "relationship",
            "rationale",
            "status",
            "followUp",
        )

        for field in required_fields:
            relation = valid_crosswalk_relation()
            del relation[field]

            with self.subTest(field=field):
                with self.assertRaises(ValidationError):
                    validate_crosswalk(
                        valid_crosswalk_payload(relations=[relation]),
                        self.curriculum_ids,
                    )

    def test_empty_rationale_is_rejected(self):
        with self.assertRaises(ValidationError):
            validate_crosswalk(
                valid_crosswalk_payload(
                    relations=[
                        valid_crosswalk_relation(rationale=" ")
                    ]
                ),
                self.curriculum_ids,
            )

    def test_open_relation_requires_explicit_follow_up(self):
        with self.assertRaises(ValidationError):
            validate_crosswalk(
                valid_crosswalk_payload(
                    relations=[
                        valid_crosswalk_relation(
                            status="open",
                            followUp="",
                        )
                    ]
                ),
                self.curriculum_ids,
            )

    def test_every_curriculum_record_must_be_accounted_for(self):
        with self.assertRaises(ValidationError):
            validate_crosswalk(
                valid_crosswalk_payload(
                    relations=[
                        valid_crosswalk_relation(toIds=[])
                    ]
                ),
                self.curriculum_ids,
            )

    def test_unmapped_record_requires_reason_and_follow_up(self):
        payloads = (
            valid_crosswalk_payload(
                relations=[],
                unmapped_records=[
                    {
                        "recordId": "LH26-E-ID-001",
                        "reason": "",
                        "followUp": "Im Modulreview prüfen.",
                    },
                    {
                        "recordId": "BMB16-GYM-IK-IW-001",
                        "reason": "Kein Gegenstück.",
                        "followUp": "Im Modulreview prüfen.",
                    },
                ],
            ),
            valid_crosswalk_payload(
                relations=[],
                unmapped_records=[
                    {
                        "recordId": "LH26-E-ID-001",
                        "reason": "Kein Gegenstück.",
                        "followUp": "",
                    },
                    {
                        "recordId": "BMB16-GYM-IK-IW-001",
                        "reason": "Kein Gegenstück.",
                        "followUp": "Im Modulreview prüfen.",
                    },
                ],
            ),
        )

        for payload in payloads:
            with self.subTest(payload=payload):
                with self.assertRaises(ValidationError):
                    validate_crosswalk(payload, self.curriculum_ids)

    def test_valid_unmapped_records_complete_the_union(self):
        payload = valid_crosswalk_payload(
            relations=[],
            unmapped_records=[
                {
                    "recordId": record_id,
                    "reason": "Kein quellentreues Gegenstück vorhanden.",
                    "followUp": "Bei der Modulzuordnung eigenständig berücksichtigen.",
                }
                for record_id in sorted(self.curriculum_ids)
            ],
        )

        self.assertEqual(
            validate_crosswalk(payload, self.curriculum_ids),
            self.curriculum_ids,
        )

    def test_unhashable_crosswalk_values_raise_validation_error(self):
        payloads = (
            valid_crosswalk_payload(status=[]),
            valid_crosswalk_payload(
                relations=[
                    valid_crosswalk_relation(relationship=[])
                ]
            ),
            valid_crosswalk_payload(
                relations=[valid_crosswalk_relation(status={})]
            ),
        )

        for payload in payloads:
            with self.subTest(payload=payload):
                with self.assertRaises(ValidationError):
                    validate_crosswalk(payload, self.curriculum_ids)

    def test_relation_ids_must_be_unique_ascii_xw_ids(self):
        duplicate = valid_crosswalk_relation()
        payloads = (
            valid_crosswalk_payload(
                relations=[duplicate, dict(duplicate)]
            ),
            valid_crosswalk_payload(
                relations=[
                    valid_crosswalk_relation(id="Beziehung-Ä")
                ]
            ),
        )

        for payload in payloads:
            with self.subTest(payload=payload):
                with self.assertRaises(ValidationError):
                    validate_crosswalk(payload, self.curriculum_ids)

    def test_relation_record_ids_must_be_unique_within_each_side(self):
        with self.assertRaises(ValidationError):
            validate_crosswalk(
                valid_crosswalk_payload(
                    relations=[
                        valid_crosswalk_relation(
                            fromIds=[
                                "LH26-E-ID-001",
                                "LH26-E-ID-001",
                            ]
                        )
                    ]
                ),
                self.curriculum_ids,
            )

    def test_mapped_record_cannot_also_be_unmapped(self):
        with self.assertRaises(ValidationError):
            validate_crosswalk(
                valid_crosswalk_payload(
                    unmapped_records=[
                        {
                            "recordId": "LH26-E-ID-001",
                            "reason": "Kein Gegenstück.",
                            "followUp": "Eigenständig berücksichtigen.",
                        }
                    ]
                ),
                self.curriculum_ids,
            )

    def test_comparative_relationship_requires_both_sides(self):
        with self.assertRaises(ValidationError):
            validate_crosswalk(
                valid_crosswalk_payload(
                    relations=[
                        valid_crosswalk_relation(toIds=[])
                    ],
                    unmapped_records=[
                        {
                            "recordId": "BMB16-GYM-IK-IW-001",
                            "reason": "Kein Gegenstück.",
                            "followUp": "Eigenständig berücksichtigen.",
                        }
                    ],
                ),
                self.curriculum_ids,
            )

    def test_new_relationship_requires_source_but_no_target(self):
        invalid_relations = (
            valid_crosswalk_relation(
                fromIds=[],
                toIds=[],
                relationship="new",
            ),
            valid_crosswalk_relation(relationship="new"),
        )

        for relation in invalid_relations:
            with self.subTest(relation=relation):
                with self.assertRaises(ValidationError):
                    validate_crosswalk(
                        valid_crosswalk_payload(relations=[relation]),
                        self.curriculum_ids,
                    )

    def test_relation_sides_must_be_disjoint(self):
        with self.assertRaises(ValidationError):
            validate_crosswalk(
                valid_crosswalk_payload(
                    relations=[
                        valid_crosswalk_relation(
                            toIds=[
                                "LH26-E-ID-001",
                                "BMB16-GYM-IK-IW-001",
                            ]
                        )
                    ]
                ),
                self.curriculum_ids,
            )

    def test_not_comparable_requires_source_but_no_target(self):
        with self.assertRaises(ValidationError):
            validate_crosswalk(
                valid_crosswalk_payload(
                    relations=[
                        valid_crosswalk_relation(
                            relationship="not-comparable"
                        )
                    ]
                ),
                self.curriculum_ids,
            )

    def test_declared_counts_must_match_payload(self):
        with self.assertRaises(ValidationError):
            validate_crosswalk(
                valid_crosswalk_payload(
                    counts={
                        "curriculumRecords": 99,
                        "relations": 1,
                        "unmappedRecords": 0,
                        "relationshipCounts": {"overlaps": 1},
                    }
                ),
                self.curriculum_ids,
            )

    def test_counts_and_source_comparisons_are_required(self):
        curriculum_records = {
            "LH26-E-ID-001": {
                "id": "LH26-E-ID-001",
                "sourceId": "SRC-CUR-LESEHILFE-2026-27",
            },
            "BMB16-GYM-IK-IW-001": {
                "id": "BMB16-GYM-IK-IW-001",
                "sourceId": "SRC-CUR-BMB-2016",
            },
        }
        for field in ("counts", "requiredSourceComparisons"):
            payload = valid_crosswalk_payload()
            del payload[field]

            with self.subTest(field=field):
                with self.assertRaises(ValidationError):
                    validate_crosswalk(payload, curriculum_records)

    def test_canonical_source_comparisons_must_be_complete(self):
        curriculum_records = {
            "LH26-E-ID-001": {
                "id": "LH26-E-ID-001",
                "sourceId": "SRC-CUR-LESEHILFE-2026-27",
            },
            "BMB16-GYM-IK-IW-001": {
                "id": "BMB16-GYM-IK-IW-001",
                "sourceId": "SRC-CUR-BMB-2016",
            },
            "INF7-16-GYM-PK-MI-001": {
                "id": "INF7-16-GYM-PK-MI-001",
                "sourceId": "SRC-CUR-INF7-2016",
            },
        }
        relations = [
            valid_crosswalk_relation(),
            valid_crosswalk_relation(
                id="XW-002",
                toIds=["INF7-16-GYM-PK-MI-001"],
            ),
        ]
        incomplete_comparisons = [
            {
                "fromSourceId": "SRC-CUR-LESEHILFE-2026-27",
                "toSourceId": "SRC-CUR-BMB-2016",
            },
            {
                "fromSourceId": "SRC-CUR-LESEHILFE-2026-27",
                "toSourceId": "SRC-CUR-INF7-2016",
            },
        ]

        with self.assertRaises(ValidationError):
            validate_crosswalk(
                valid_crosswalk_payload(
                    relations=relations,
                    requiredSourceComparisons=incomplete_comparisons,
                ),
                curriculum_records,
            )

    def test_required_source_comparisons_need_direct_relations(self):
        curriculum_records = {
            "LH26-E-ID-001": {
                "id": "LH26-E-ID-001",
                "sourceId": "SRC-CUR-LESEHILFE-2026-27",
            },
            "BMB16-GYM-IK-IW-001": {
                "id": "BMB16-GYM-IK-IW-001",
                "sourceId": "SRC-CUR-BMB-2016",
            },
            "INF7-16-GYM-PK-MI-001": {
                "id": "INF7-16-GYM-PK-MI-001",
                "sourceId": "SRC-CUR-INF7-2016",
            },
        }
        relations_without_bmb_inf = [
            valid_crosswalk_relation(),
            valid_crosswalk_relation(
                id="XW-002",
                toIds=["INF7-16-GYM-PK-MI-001"],
            ),
        ]
        required_comparisons = [
            {
                "fromSourceId": "SRC-CUR-LESEHILFE-2026-27",
                "toSourceId": "SRC-CUR-BMB-2016",
            },
            {
                "fromSourceId": "SRC-CUR-LESEHILFE-2026-27",
                "toSourceId": "SRC-CUR-INF7-2016",
            },
            {
                "fromSourceId": "SRC-CUR-BMB-2016",
                "toSourceId": "SRC-CUR-INF7-2016",
            },
        ]

        with self.assertRaises(ValidationError):
            validate_crosswalk(
                valid_crosswalk_payload(
                    relations=relations_without_bmb_inf,
                    requiredSourceComparisons=required_comparisons,
                ),
                curriculum_records,
            )

        relations_with_bmb_inf = relations_without_bmb_inf + [
            valid_crosswalk_relation(
                id="XW-003",
                fromIds=["BMB16-GYM-IK-IW-001"],
                toIds=["INF7-16-GYM-PK-MI-001"],
            )
        ]
        self.assertEqual(
            validate_crosswalk(
                valid_crosswalk_payload(
                    relations=relations_with_bmb_inf,
                    requiredSourceComparisons=required_comparisons,
                ),
                curriculum_records,
            ),
            set(curriculum_records),
        )


class OperatorMappingTests(unittest.TestCase):
    def setUp(self):
        self.curriculum_ids = {
            "BMB16-GYM-OP-002",
            "INF7-16-GYM-PK-MI-009",
        }

    def test_valid_operator_payload_returns_source_record_ids(self):
        source_record_ids = validate_operators(
            valid_operators_payload(
                entries=[
                    valid_operator_entry(),
                    valid_operator_entry(
                        id="OPMAP-002",
                        kind="process-competency",
                        exactOfficialTerm="Programme gezielt testen",
                        sourceRecordId="INF7-16-GYM-PK-MI-009",
                        sourceDefinition="Programme gezielt testen",
                        sourceAfb=None,
                        likelyComplexityBand="context-dependent",
                        applicableGrades=[7],
                    ),
                ]
            ),
            self.curriculum_ids,
        )

        self.assertEqual(source_record_ids, self.curriculum_ids)

    def test_unknown_source_record_is_rejected(self):
        with self.assertRaises(ValidationError):
            validate_operators(
                valid_operators_payload(
                    entries=[
                        valid_operator_entry(sourceRecordId="UNKNOWN")
                    ]
                ),
                self.curriculum_ids,
            )

    def test_duplicate_source_record_is_rejected(self):
        with self.assertRaises(ValidationError):
            validate_operators(
                valid_operators_payload(
                    entries=[
                        valid_operator_entry(),
                        valid_operator_entry(id="OPMAP-002"),
                    ]
                ),
                self.curriculum_ids,
            )

    def test_missing_operator_field_is_rejected(self):
        required_fields = (
            "id",
            "kind",
            "exactOfficialTerm",
            "sourceRecordId",
            "sourceDefinition",
            "sourceAfb",
            "expectedObservableAction",
            "likelyComplexityBand",
            "applicableGrades",
            "notesOnAmbiguity",
            "status",
        )

        for field in required_fields:
            entry = valid_operator_entry()
            del entry[field]

            with self.subTest(field=field):
                with self.assertRaises(ValidationError):
                    validate_operators(
                        valid_operators_payload(entries=[entry]),
                        self.curriculum_ids,
                    )

    def test_invalid_operator_classification_is_rejected(self):
        invalid_overrides = (
            {"kind": "derived-verb"},
            {"sourceAfb": "IV"},
            {"likelyComplexityBand": "universal-level-2"},
            {"applicableGrades": []},
            {"applicableGrades": [4]},
            {"status": "verified"},
        )

        for overrides in invalid_overrides:
            with self.subTest(overrides=overrides):
                with self.assertRaises(ValidationError):
                    validate_operators(
                        valid_operators_payload(
                            entries=[
                                valid_operator_entry(**overrides)
                            ]
                        ),
                        self.curriculum_ids,
                    )

    def test_unhashable_operator_values_raise_validation_error(self):
        payloads = (
            valid_operators_payload(status=[]),
            valid_operators_payload(
                entries=[valid_operator_entry(kind=[])]
            ),
            valid_operators_payload(
                entries=[
                    valid_operator_entry(
                        likelyComplexityBand={}
                    )
                ]
            ),
            valid_operators_payload(
                entries=[valid_operator_entry(status=[])]
            ),
        )

        for payload in payloads:
            with self.subTest(payload=payload):
                with self.assertRaises(ValidationError):
                    validate_operators(payload, self.curriculum_ids)

    def test_entry_ids_must_be_unique_ascii_opmap_ids(self):
        duplicate = valid_operator_entry()
        payloads = (
            valid_operators_payload(
                entries=[duplicate, dict(duplicate)]
            ),
            valid_operators_payload(
                entries=[
                    valid_operator_entry(id="Operator-Ä")
                ]
            ),
        )

        for payload in payloads:
            with self.subTest(payload=payload):
                with self.assertRaises(ValidationError):
                    validate_operators(payload, self.curriculum_ids)

    def test_kind_and_source_afb_must_agree(self):
        invalid_entries = (
            valid_operator_entry(sourceAfb=None),
            valid_operator_entry(
                kind="process-competency",
                sourceAfb="II",
            ),
        )

        for entry in invalid_entries:
            with self.subTest(entry=entry):
                with self.assertRaises(ValidationError):
                    validate_operators(
                        valid_operators_payload(entries=[entry]),
                        self.curriculum_ids,
                    )

    def test_every_requested_source_record_must_have_an_entry(self):
        with self.assertRaises(ValidationError):
            validate_operators(
                valid_operators_payload(),
                self.curriculum_ids,
            )

    def test_source_metadata_must_remain_exact_when_available(self):
        source_records = {
            "BMB16-GYM-OP-002": {
                "id": "BMB16-GYM-OP-002",
                "recordType": "operator",
                "operator": "analysieren",
                "text": "Materialien oder Sachverhalte systematisch untersuchen.",
                "afb": "III",
                "grades": [5],
            },
            "INF7-16-GYM-PK-MI-009": {
                "id": "INF7-16-GYM-PK-MI-009",
                "recordType": "process-competency",
                "text": "Programme gezielt testen",
                "grades": [7],
            },
        }
        process_entry = valid_operator_entry(
            id="OPMAP-002",
            kind="process-competency",
            exactOfficialTerm="Programme gezielt testen",
            sourceRecordId="INF7-16-GYM-PK-MI-009",
            sourceDefinition="Programme gezielt testen",
            sourceAfb=None,
            likelyComplexityBand="context-dependent",
            applicableGrades=[7],
        )
        invalid_operator_overrides = (
            {"exactOfficialTerm": "untersuchen"},
            {"sourceDefinition": "verkürzte Definition"},
            {"sourceAfb": "II"},
            {"applicableGrades": [6]},
        )

        for overrides in invalid_operator_overrides:
            with self.subTest(overrides=overrides):
                with self.assertRaises(ValidationError):
                    validate_operators(
                        valid_operators_payload(
                            entries=[
                                valid_operator_entry(**overrides),
                                process_entry,
                            ]
                        ),
                        source_records,
                    )

        with self.assertRaises(ValidationError):
            validate_operators(
                valid_operators_payload(
                    entries=[
                        valid_operator_entry(),
                        dict(process_entry, kind="operator"),
                    ]
                ),
                source_records,
            )


class CurriculumIntegrationFileTests(unittest.TestCase):
    def test_integration_files_are_loaded_and_validated_together(self):
        crosswalk_ids = {
            "LH26-E-ID-001",
            "BMB16-GYM-IK-IW-001",
        }
        operator_ids = {
            "BMB16-GYM-OP-002",
            "INF7-16-GYM-PK-MI-009",
        }
        operators = valid_operators_payload(
            entries=[
                valid_operator_entry(),
                valid_operator_entry(
                    id="OPMAP-002",
                    kind="process-competency",
                    exactOfficialTerm="Programme gezielt testen",
                    sourceRecordId="INF7-16-GYM-PK-MI-009",
                    sourceDefinition="Programme gezielt testen",
                    sourceAfb=None,
                    likelyComplexityBand="context-dependent",
                    applicableGrades=[7],
                ),
            ]
        )

        with tempfile.TemporaryDirectory() as directory:
            curriculum = Path(directory) / "curriculum"
            curriculum.mkdir()
            (curriculum / "operators.json").write_text(
                json.dumps(operators),
                encoding="utf-8",
            )
            (curriculum / "crosswalk.json").write_text(
                json.dumps(valid_crosswalk_payload()),
                encoding="utf-8",
            )

            result = validate_curriculum_integrations(
                Path(directory),
                crosswalk_ids,
                operator_ids,
            )

        self.assertEqual(
            result,
            {
                "curriculumIds": crosswalk_ids,
                "operatorRecordIds": operator_ids,
            },
        )

    def test_invalid_crosswalk_file_is_not_ignored(self):
        crosswalk_ids = {
            "LH26-E-ID-001",
            "BMB16-GYM-IK-IW-001",
        }
        operator_ids = {"BMB16-GYM-OP-002"}

        with tempfile.TemporaryDirectory() as directory:
            curriculum = Path(directory) / "curriculum"
            curriculum.mkdir()
            (curriculum / "operators.json").write_text(
                json.dumps(valid_operators_payload()),
                encoding="utf-8",
            )
            (curriculum / "crosswalk.json").write_text(
                json.dumps(
                    valid_crosswalk_payload(
                        relations=[
                            valid_crosswalk_relation(
                                relationship="similar"
                            )
                        ]
                    )
                ),
                encoding="utf-8",
            )

            with self.assertRaises(ValidationError):
                validate_curriculum_integrations(
                    Path(directory),
                    crosswalk_ids,
                    operator_ids,
                )


class DesignPrincipleFieldTests(unittest.TestCase):
    def setUp(self):
        self.claim_ids = {"CLAIM-LP-006", "CLAIM-INF-004"}

    def test_valid_payload_returns_principle_ids(self):
        principle_ids = validate_design_principles(
            valid_design_principles_payload(),
            self.claim_ids,
        )

        self.assertEqual(principle_ids, {"PRIN-001"})

    def test_unknown_claim_is_rejected(self):
        with self.assertRaises(ValidationError):
            validate_design_principles(
                valid_design_principles_payload(
                    principles=[
                        valid_design_principle(claimIds=["CLAIM-MISSING"])
                    ]
                ),
                self.claim_ids,
            )

    def test_duplicate_principle_id_is_rejected(self):
        principle = valid_design_principle()

        with self.assertRaises(ValidationError):
            validate_design_principles(
                valid_design_principles_payload(
                    principles=[principle, dict(principle)]
                ),
                self.claim_ids,
            )

    def test_principle_id_requires_ascii_prin_prefix(self):
        for principle_id in ("PRIN-", "PRIN-Ä", "X-001"):
            with self.subTest(principle_id=principle_id):
                with self.assertRaises(ValidationError):
                    validate_design_principles(
                        valid_design_principles_payload(
                            principles=[
                                valid_design_principle(id=principle_id)
                            ]
                        ),
                        self.claim_ids,
                    )

    def test_missing_required_field_is_rejected(self):
        required_fields = (
            "id",
            "title",
            "statement",
            "claimIds",
            "appliesTo",
            "status",
            "phase1Implications",
            "risks",
        )

        for field in required_fields:
            principle = valid_design_principle()
            del principle[field]

            with self.subTest(field=field):
                with self.assertRaises(ValidationError):
                    validate_design_principles(
                        valid_design_principles_payload(
                            principles=[principle]
                        ),
                        self.claim_ids,
                    )

    def test_invalid_required_field_type_is_rejected(self):
        invalid_values = {
            "id": 1,
            "title": 1,
            "statement": 1,
            "claimIds": "CLAIM-LP-006",
            "appliesTo": "Modulphase 4",
            "status": 1,
            "phase1Implications": "Manifest erweitern",
            "risks": "Übersteuerung",
        }

        for field, value in invalid_values.items():
            with self.subTest(field=field):
                with self.assertRaises(ValidationError):
                    validate_design_principles(
                        valid_design_principles_payload(
                            principles=[
                                valid_design_principle(**{field: value})
                            ]
                        ),
                        self.claim_ids,
                    )

    def test_required_strings_and_lists_must_be_nonempty(self):
        invalid_overrides = (
            {"title": " "},
            {"statement": ""},
            {"claimIds": []},
            {"claimIds": [""]},
            {"appliesTo": []},
            {"appliesTo": [" "]},
            {"phase1Implications": []},
            {"phase1Implications": [""]},
            {"risks": []},
            {"risks": [" "]},
        )

        for overrides in invalid_overrides:
            with self.subTest(overrides=overrides):
                with self.assertRaises(ValidationError):
                    validate_design_principles(
                        valid_design_principles_payload(
                            principles=[
                                valid_design_principle(**overrides)
                            ]
                        ),
                        self.claim_ids,
                    )

    def test_duplicate_claim_id_within_principle_is_rejected(self):
        with self.assertRaises(ValidationError):
            validate_design_principles(
                valid_design_principles_payload(
                    principles=[
                        valid_design_principle(
                            claimIds=["CLAIM-LP-006", "CLAIM-LP-006"]
                        )
                    ]
                ),
                self.claim_ids,
            )

    def test_invalid_status_is_rejected(self):
        with self.assertRaises(ValidationError):
            validate_design_principles(
                valid_design_principles_payload(
                    principles=[
                        valid_design_principle(status="verified")
                    ]
                ),
                self.claim_ids,
            )

    def test_unhashable_status_type_is_rejected_with_validation_error(self):
        for status in ([], {}):
            with self.subTest(status=status):
                with self.assertRaises(ValidationError):
                    validate_design_principles(
                        valid_design_principles_payload(
                            principles=[
                                valid_design_principle(status=status)
                            ]
                        ),
                        self.claim_ids,
                    )

    def test_schema_version_one_and_principles_array_are_required(self):
        invalid_payloads = (
            valid_design_principles_payload(schemaVersion=2),
            {"schemaVersion": 1, "principles": {}},
        )

        for payload in invalid_payloads:
            with self.subTest(payload=payload):
                with self.assertRaises(ValidationError):
                    validate_design_principles(payload, self.claim_ids)


if __name__ == "__main__":
    unittest.main()
