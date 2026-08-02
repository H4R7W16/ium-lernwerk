import copy
import json
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest import mock

import scripts.validate_phase0 as validate_phase0_script
from scripts.validate_phase0 import (
    ValidationError,
    validate_claim_ledger,
    validate_crosswalk,
    validate_curriculum_dataset,
    validate_design_principles,
    validate_curriculum_integrations,
    validate_coverage,
    validate_module_candidates,
    validate_operators,
    validate_source_register,
)


def markdown_section(markdown, heading):
    lines = markdown.splitlines()
    if heading not in lines:
        raise AssertionError(f"Markdown section missing: {heading}")
    start = lines.index(heading)
    level = len(heading) - len(heading.lstrip("#"))
    end = len(lines)
    for index in range(start + 1, len(lines)):
        candidate = lines[index]
        if candidate.startswith("#"):
            candidate_level = len(candidate) - len(candidate.lstrip("#"))
            if candidate_level <= level:
                end = index
                break
    return "\n".join(lines[start + 1:end]).strip()


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


MODULE_GRAMMAR_PHASES = [
    "orientation-challenge",
    "activate-prior-knowledge",
    "build-concept",
    "guided-practice",
    "independent-action-product",
    "review-revise-transfer",
    "shared-consolidation",
]


def valid_module_candidate(**overrides):
    module = {
        "id": "IUM-5-CORE-01",
        "title": "Recherche mit prüfbaren Belegen",
        "grade": 5,
        "kind": "core",
        "strandIds": ["STRAND-B"],
        "competencyIds": [
            "LH26-E-ID-001",
            "BMB16-GYM-IK-IW-001",
        ],
        "prerequisiteModuleIds": [],
        "lessonRange": {"min": 4, "max": 6},
        "centralQuestion": "Wie wird aus einer Suchfrage ein belastbarer Befund?",
        "centralLearningAction": (
            "Suchergebnisse auswählen, Quellen anhand von Kriterien "
            "vergleichen und eine begründete Auswahl revidieren."
        ),
        "centralLearningProduct": (
            "Quellendossier mit Suchweg, Kriterienprüfung, Belegen und Revision."
        ),
        "moduleGrammar": list(MODULE_GRAMMAR_PHASES),
        "mediumRationale": (
            "Die digitale Rechercheumgebung ist selbst Gegenstand der "
            "Analyse und macht Suchweg, Quellenwechsel und Belegprüfung "
            "direkt ausführbar."
        ),
        "analogMaterials": [],
        "assessmentWorkingNotes": (
            "Optional prüfbar sind Kriterienanwendung, Belegqualität und "
            "begründete Revision; es entsteht kein Personenprofil."
        ),
        "status": "working",
    }
    module.update(overrides)
    return module


def valid_module_candidates_payload(modules=None, **overrides):
    core = valid_module_candidate()
    extension = valid_module_candidate(
        id="IUM-5-EXT-01",
        title="Recherchewerkzeuge vergleichen",
        kind="extension",
        competencyIds=["LH26-E-ID-001"],
        prerequisiteModuleIds=["IUM-5-CORE-01"],
        lessonRange={"min": 2, "max": 3},
        moduleGrammar=[
            "orientation-challenge",
            "guided-practice",
            "independent-action-product",
            "review-revise-transfer",
            "shared-consolidation",
        ],
    )
    transfer = valid_module_candidate(
        id="IUM-6-TRANSFER-01",
        title="Belege in einem neuen Kontext prüfen",
        grade=6,
        kind="transfer",
        competencyIds=["BMB16-GYM-IK-IW-001"],
        prerequisiteModuleIds=["IUM-5-CORE-01"],
        lessonRange={"min": 2, "max": 4},
        moduleGrammar=[
            "orientation-challenge",
            "activate-prior-knowledge",
            "independent-action-product",
            "review-revise-transfer",
            "shared-consolidation",
        ],
    )
    project = valid_module_candidate(
        id="IUM-7-PROJECT-01",
        title="Offenes Evidenzprojekt",
        grade=7,
        kind="project",
        prerequisiteModuleIds=["IUM-5-CORE-01"],
        lessonRange={"min": 6, "max": 10},
        moduleGrammar=[
            "orientation-challenge",
            "activate-prior-knowledge",
            "build-concept",
            "independent-action-product",
            "review-revise-transfer",
            "shared-consolidation",
        ],
    )
    payload = {
        "schemaVersion": 1,
        "status": "working",
        "modules": (
            modules
            if modules is not None
            else [core, extension, transfer, project]
        ),
    }
    payload.update(overrides)
    return payload


def valid_coverage_entry(**overrides):
    requirement_text = (
        "einen aktuellen Internetbrowser und Suchmaschinen zu "
        "Recherchezwecken einsetzen"
    )
    action = "Eine Recherche mit Browser und Suchmaschine durchführen."
    product = "Ein sichtbares Suchprotokoll."
    entry = {
        "competencyId": "BMB16-GYM-IK-IW-001",
        "normativeWeight": "enacted",
        "moduleIds": ["IUM-5-CORE-01"],
        "coverageStatus": "covered",
        "semanticAudit": "operator-product-match",
        "requirementText": requirement_text,
        "evidenceModuleId": "IUM-5-CORE-01",
        "evidence": (
            f"Kernmodul IUM-5-CORE-01: {action} "
            f"Sichtbarer Nachweis: {product}"
        ),
        "matchRationale": (
            f"Die Anforderung „{requirement_text}“ wird durch die zentrale "
            f"Lernhandlung „{action}“ ausgeführt; das Produkt „{product}“ "
            "dokumentiert das Ergebnis."
        ),
        "risk": (
            "Kandidatenabdeckung ersetzt noch keine Zeit- und "
            "Implementierungsprüfung."
        ),
        "followUp": (
            "Operator, Lernhandlung und Produkt im Modulreview erneut prüfen."
        ),
    }
    entry.update(overrides)
    return entry


def valid_coverage_payload(entries=None, **overrides):
    payload = {
        "schemaVersion": 1,
        "status": "working",
        "coverageBasis": "candidate-design",
        "entries": (
            entries
            if entries is not None
            else [
                valid_coverage_entry(),
                valid_coverage_entry(
                    competencyId="LH26-E-ID-001",
                    normativeWeight="orientation",
                    requirementText=(
                        "digitale Werkzeuge und Angebote zur "
                        "Informationsgewinnung nutzen"
                    ),
                    matchRationale=(
                        "Die Anforderung „digitale Werkzeuge und Angebote "
                        "zur Informationsgewinnung nutzen“ wird durch die "
                        "zentrale Lernhandlung „Eine Recherche mit Browser "
                        "und Suchmaschine durchführen.“ ausgeführt; das "
                        "Produkt „Ein sichtbares Suchprotokoll.“ "
                        "dokumentiert das Ergebnis."
                    ),
                ),
            ]
        ),
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

        for comparisons in ([], incomplete_comparisons):
            with self.subTest(comparisons=comparisons):
                with self.assertRaises(ValidationError):
                    validate_crosswalk(
                        valid_crosswalk_payload(
                            relations=relations,
                            requiredSourceComparisons=comparisons,
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


class ModuleCandidateTests(unittest.TestCase):
    def setUp(self):
        self.curriculum_ids = {
            "LH26-E-ID-001": {5, 6, 7},
            "BMB16-GYM-IK-IW-001": {5, 6, 7},
        }

    def test_valid_candidate_graph_returns_module_ids(self):
        module_ids = validate_module_candidates(
            valid_module_candidates_payload(),
            self.curriculum_ids,
        )

        self.assertEqual(
            module_ids,
            {
                "IUM-5-CORE-01",
                "IUM-5-EXT-01",
                "IUM-6-TRANSFER-01",
                "IUM-7-PROJECT-01",
            },
        )

    def test_duplicate_module_ids_are_rejected(self):
        modules = valid_module_candidates_payload()["modules"]
        modules.append(copy.deepcopy(modules[0]))

        with self.assertRaises(ValidationError):
            validate_module_candidates(
                valid_module_candidates_payload(modules=modules),
                self.curriculum_ids,
            )

    def test_missing_module_field_is_rejected(self):
        required_fields = (
            "id",
            "title",
            "grade",
            "kind",
            "strandIds",
            "competencyIds",
            "prerequisiteModuleIds",
            "lessonRange",
            "centralQuestion",
            "centralLearningAction",
            "centralLearningProduct",
            "moduleGrammar",
            "mediumRationale",
            "analogMaterials",
            "assessmentWorkingNotes",
            "status",
        )

        for field in required_fields:
            modules = valid_module_candidates_payload()["modules"]
            del modules[0][field]

            with self.subTest(field=field):
                with self.assertRaises(ValidationError):
                    validate_module_candidates(
                        valid_module_candidates_payload(modules=modules),
                        self.curriculum_ids,
                    )

    def test_unknown_competency_id_is_rejected(self):
        modules = valid_module_candidates_payload()["modules"]
        modules[0]["competencyIds"] = ["UNKNOWN"]

        with self.assertRaises(ValidationError):
            validate_module_candidates(
                valid_module_candidates_payload(modules=modules),
                self.curriculum_ids,
            )

    def test_unknown_prerequisite_module_id_is_rejected(self):
        modules = valid_module_candidates_payload()["modules"]
        modules[1]["prerequisiteModuleIds"] = ["IUM-5-CORE-99"]

        with self.assertRaises(ValidationError):
            validate_module_candidates(
                valid_module_candidates_payload(modules=modules),
                self.curriculum_ids,
            )

    def test_dependency_cycles_are_rejected(self):
        modules = valid_module_candidates_payload()["modules"]
        second_core = valid_module_candidate(
            id="IUM-5-CORE-02",
            title="Zweiter Kernkandidat",
            prerequisiteModuleIds=["IUM-5-CORE-01"],
        )
        modules[0]["prerequisiteModuleIds"] = ["IUM-5-CORE-02"]
        modules.append(second_core)

        with self.assertRaises(ValidationError):
            validate_module_candidates(
                valid_module_candidates_payload(modules=modules),
                self.curriculum_ids,
            )

    def test_invalid_or_missing_hybrid_module_kind_is_rejected(self):
        invalid_modules = valid_module_candidates_payload()["modules"]
        invalid_modules[1]["kind"] = "lab"
        missing_kind_modules = [
            module
            for module in valid_module_candidates_payload()["modules"]
            if module["kind"] != "project"
        ]

        for modules in (invalid_modules, missing_kind_modules):
            with self.subTest(modules=modules):
                with self.assertRaises(ValidationError):
                    validate_module_candidates(
                        valid_module_candidates_payload(modules=modules),
                        self.curriculum_ids,
                    )

    def test_missing_learning_product_or_medium_rationale_is_rejected(self):
        for field in ("centralLearningProduct", "mediumRationale"):
            modules = valid_module_candidates_payload()["modules"]
            modules[0][field] = " "

            with self.subTest(field=field):
                with self.assertRaises(ValidationError):
                    validate_module_candidates(
                        valid_module_candidates_payload(modules=modules),
                        self.curriculum_ids,
                    )

    def test_analog_material_needs_didactic_rationale_and_reconnection(self):
        invalid_analog_materials = (
            [
                {
                    "title": "Paketkarten",
                    "didacticRationale": "",
                    "digitalReconnection": "Netzmodell digital prüfen.",
                }
            ],
            [
                {
                    "title": "Paketkarten",
                    "didacticRationale": "Verteiltes Weiterleiten körperlich modellieren.",
                    "digitalReconnection": "",
                }
            ],
        )

        for analog_materials in invalid_analog_materials:
            modules = valid_module_candidates_payload()["modules"]
            modules[0]["analogMaterials"] = analog_materials

            with self.subTest(analog_materials=analog_materials):
                with self.assertRaises(ValidationError):
                    validate_module_candidates(
                        valid_module_candidates_payload(modules=modules),
                        self.curriculum_ids,
                    )

    def test_core_module_needs_grade_and_valid_lesson_range(self):
        invalid_overrides = (
            {"grade": None},
            {"lessonRange": None},
            {"lessonRange": {"min": 6, "max": 4}},
        )

        for overrides in invalid_overrides:
            modules = valid_module_candidates_payload()["modules"]
            modules[0].update(overrides)

            with self.subTest(overrides=overrides):
                with self.assertRaises(ValidationError):
                    validate_module_candidates(
                        valid_module_candidates_payload(modules=modules),
                        self.curriculum_ids,
                    )

    def test_core_modules_jointly_cover_all_required_curriculum_ids(self):
        modules = valid_module_candidates_payload()["modules"]
        modules[0]["competencyIds"] = ["LH26-E-ID-001"]

        with self.assertRaises(ValidationError):
            validate_module_candidates(
                valid_module_candidates_payload(modules=modules),
                self.curriculum_ids,
            )

    def test_core_module_requires_complete_seven_phase_grammar(self):
        modules = valid_module_candidates_payload()["modules"]
        modules[0]["moduleGrammar"] = MODULE_GRAMMAR_PHASES[:-1]

        with self.assertRaises(ValidationError):
            validate_module_candidates(
                valid_module_candidates_payload(modules=modules),
                self.curriculum_ids,
            )

    def test_core_path_cannot_depend_on_a_flexible_module(self):
        modules = valid_module_candidates_payload()["modules"]
        modules[0]["prerequisiteModuleIds"] = ["IUM-5-EXT-01"]
        modules[1]["prerequisiteModuleIds"] = []

        with self.assertRaises(ValidationError):
            validate_module_candidates(
                valid_module_candidates_payload(modules=modules),
                self.curriculum_ids,
            )

    def test_flexible_module_cannot_depend_on_another_flexible_module(self):
        modules = valid_module_candidates_payload()["modules"]
        modules[2]["prerequisiteModuleIds"] = ["IUM-5-EXT-01"]

        with self.assertRaises(ValidationError):
            validate_module_candidates(
                valid_module_candidates_payload(modules=modules),
                self.curriculum_ids,
            )

    def test_module_cannot_depend_on_a_later_grade(self):
        modules = valid_module_candidates_payload()["modules"]
        modules.append(
            valid_module_candidate(
                id="IUM-7-CORE-02",
                title="Späterer Kernkandidat",
                grade=7,
                competencyIds=["LH26-E-ID-001"],
            )
        )
        modules[1]["prerequisiteModuleIds"] = ["IUM-7-CORE-02"]

        with self.assertRaises(ValidationError):
            validate_module_candidates(
                valid_module_candidates_payload(modules=modules),
                self.curriculum_ids,
            )

    def test_module_grade_must_match_curriculum_grade_contract(self):
        curriculum_grade_contract = dict(self.curriculum_ids)
        curriculum_grade_contract["LH26-E-ID-001"] = {7}

        with self.assertRaises(ValidationError):
            validate_module_candidates(
                valid_module_candidates_payload(),
                curriculum_grade_contract,
            )


class ModuleCandidateFileTests(unittest.TestCase):
    def test_repository_candidates_cover_contract_and_preserve_hybrid_model(self):
        root = Path(__file__).resolve().parents[1]
        records = [
            record
            for path in sorted(
                (root / "curriculum").glob("**/competencies.json")
            )
            for record in json.loads(path.read_text(encoding="utf-8"))[
                "records"
            ]
        ]
        required_curriculum_grades = {
            record["id"]: set(record["grades"])
            for record in records
            if record["recordType"] not in {"example", "operator"}
        }
        payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(
                encoding="utf-8"
            )
        )
        module_ids = validate_module_candidates(
            payload,
            required_curriculum_grades,
        )
        modules_by_id = {
            module["id"]: module for module in payload["modules"]
        }
        specification = (
            root
            / "docs/superpowers/specs/"
            "2026-07-27-ium-lernwerk-gesamtdesign.md"
        ).read_text(encoding="utf-8")

        self.assertEqual(len(required_curriculum_grades), 171)
        self.assertEqual(len(module_ids), 31)
        self.assertEqual(
            {module["kind"] for module in payload["modules"]},
            {"core", "extension", "transfer", "project"},
        )
        self.assertEqual(
            {
                module["grade"]
                for module in payload["modules"]
                if module["kind"] == "core"
            },
            {5, 6, 7},
        )
        self.assertFalse(
            any(
                module["grade"] == 5
                and module["kind"] in {"transfer", "project"}
                for module in payload["modules"]
            )
        )
        for competency_id in (
            "LH26-E-KS-008",
            "LH26-E-KS-009",
            "LH26-E-KS-010",
        ):
            with self.subTest(competency_id=competency_id):
                self.assertFalse(
                    any(
                        competency_id in module["competencyIds"]
                        for module in payload["modules"]
                        if module["grade"] == 5
                    ),
                )
                self.assertIn(
                    competency_id,
                    modules_by_id["IUM-6-CORE-05"]["competencyIds"],
                )
        self.assertEqual(
            modules_by_id["IUM-6-EXT-02"]["prerequisiteModuleIds"],
            ["IUM-6-CORE-05"],
        )
        self.assertIn(
            "erarbeiten, erklären",
            modules_by_id["IUM-6-CORE-05"]["centralLearningAction"],
        )
        for module_id in ("IUM-5-CORE-07", "IUM-7-CORE-09"):
            with self.subTest(module_id=module_id):
                self.assertIn(
                    "private Selbstreflexion",
                    modules_by_id[module_id]["centralLearningAction"],
                )
                self.assertIn(
                    "nicht erhoben, gespeichert oder bewertet",
                    modules_by_id[module_id]["assessmentWorkingNotes"],
                )
        self.assertIn(
            "Gründe für und gegen die Nutzung Sozialer Medien",
            modules_by_id["IUM-6-CORE-06"]["centralLearningAction"],
        )
        self.assertIn(
            "Wirkung von Selbstdarstellung",
            modules_by_id["IUM-6-CORE-06"]["centralLearningAction"],
        )
        self.assertIn(
            "private Selbstreflexion",
            modules_by_id["IUM-6-CORE-06"]["centralLearningAction"],
        )
        self.assertEqual(
            specification.count(
                "Ein verbindlicher Kernlernweg sichert fachliche "
                "Progression und vollständige Curriculum-Abdeckung."
            ),
            1,
        )
        self.assertEqual(
            specification.count(
                "Vertiefungs-, Transfer- und Projektmodule können an "
                "definierte Voraussetzungen andocken und flexibel "
                "eingesetzt werden."
            ),
            1,
        )


class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.required_ids = {
            "BMB16-GYM-IK-IW-001": {
                "normativeWeight": "enacted",
                "text": (
                    "einen aktuellen Internetbrowser und Suchmaschinen zu "
                    "Recherchezwecken einsetzen"
                ),
            },
            "LH26-E-ID-001": {
                "normativeWeight": "orientation",
                "text": (
                    "digitale Werkzeuge und Angebote zur "
                    "Informationsgewinnung nutzen"
                ),
            },
        }
        self.module_ids = {
            "IUM-5-CORE-01": {
                "kind": "core",
                "competencyIds": [
                    "BMB16-GYM-IK-IW-001",
                    "LH26-E-ID-001",
                ],
                "centralLearningAction": (
                    "Eine Recherche mit Browser und Suchmaschine "
                    "durchführen."
                ),
                "centralLearningProduct": "Ein sichtbares Suchprotokoll.",
            },
            "IUM-5-CORE-02": {
                "kind": "core",
                "competencyIds": ["LH26-E-ID-001"],
                "centralLearningAction": "Eine Suchfrage prüfen.",
                "centralLearningProduct": "Ein Quellendossier.",
            },
            "IUM-5-EXT-01": {
                "kind": "extension",
                "competencyIds": ["BMB16-GYM-IK-IW-001"],
                "centralLearningAction": "Eine Recherche vertiefen.",
                "centralLearningProduct": "Ein Vertiefungsprotokoll.",
            },
        }

    def test_valid_coverage_returns_required_ids(self):
        self.assertEqual(
            validate_coverage(
                valid_coverage_payload(),
                self.required_ids,
                self.module_ids,
            ),
            set(self.required_ids),
        )

    def test_every_required_record_must_be_accounted_for(self):
        entries = valid_coverage_payload()["entries"][:-1]

        with self.assertRaises(ValidationError):
            validate_coverage(
                valid_coverage_payload(entries=entries),
                self.required_ids,
                self.module_ids,
            )

    def test_covered_record_needs_a_valid_core_module(self):
        invalid_module_lists = (
            ["UNKNOWN"],
            ["IUM-5-EXT-01"],
            [],
        )

        for module_ids in invalid_module_lists:
            entries = valid_coverage_payload()["entries"]
            entries[0]["moduleIds"] = module_ids

            with self.subTest(module_ids=module_ids):
                with self.assertRaises(ValidationError):
                    validate_coverage(
                        valid_coverage_payload(entries=entries),
                        self.required_ids,
                        self.module_ids,
                    )

    def test_referenced_core_must_contain_the_covered_competency(self):
        entries = valid_coverage_payload()["entries"]
        entries[0]["moduleIds"] = ["IUM-5-CORE-02"]

        with self.assertRaises(ValidationError):
            validate_coverage(
                valid_coverage_payload(entries=entries),
                self.required_ids,
                self.module_ids,
            )

    def test_partial_and_deferred_need_reason_risk_and_follow_up(self):
        for coverage_status in ("partial", "deferred"):
            for field in ("reason", "risk", "followUp"):
                entry = valid_coverage_entry(
                    coverageStatus=coverage_status,
                    semanticAudit="documented-gap",
                    reason="Nur ein Teil des Operators wird eingelöst.",
                )
                if field == "reason":
                    del entry[field]
                else:
                    entry[field] = " "
                entries = [
                    entry,
                    valid_coverage_entry(
                        competencyId="LH26-E-ID-001",
                        normativeWeight="orientation",
                    ),
                ]

                with self.subTest(
                    coverage_status=coverage_status,
                    field=field,
                ):
                    with self.assertRaises(ValidationError):
                        validate_coverage(
                            valid_coverage_payload(entries=entries),
                            self.required_ids,
                            self.module_ids,
                        )

    def test_semantic_audit_must_match_coverage_decision(self):
        invalid_pairs = (
            ("covered", "documented-gap"),
            ("partial", "operator-product-match"),
            ("deferred", "operator-product-match"),
        )

        for coverage_status, semantic_audit in invalid_pairs:
            entry = valid_coverage_entry(
                coverageStatus=coverage_status,
                semanticAudit=semantic_audit,
            )
            if coverage_status != "covered":
                entry["reason"] = "Der Produktnachweis ist unvollständig."
            entries = [
                entry,
                valid_coverage_entry(
                    competencyId="LH26-E-ID-001",
                    normativeWeight="orientation",
                ),
            ]

            with self.subTest(
                coverage_status=coverage_status,
                semantic_audit=semantic_audit,
            ):
                with self.assertRaises(ValidationError):
                    validate_coverage(
                        valid_coverage_payload(entries=entries),
                        self.required_ids,
                        self.module_ids,
                    )

    def test_semantic_traceability_must_match_source_and_module_contract(self):
        invalid_mutations = (
            ("requirementText", "Eine andere Anforderung."),
            ("evidenceModuleId", "IUM-5-CORE-02"),
            ("matchRationale", "Pauschale Matchbehauptung."),
            ("evidence", "Pauschale Evidenzbehauptung."),
        )

        for field, value in invalid_mutations:
            entries = valid_coverage_payload()["entries"]
            entries[0][field] = value

            with self.subTest(field=field):
                with self.assertRaises(ValidationError):
                    validate_coverage(
                        valid_coverage_payload(entries=entries),
                        self.required_ids,
                        self.module_ids,
                    )

    def test_normative_weight_must_match_curriculum_source_status(self):
        entries = valid_coverage_payload()["entries"]
        entries[1]["normativeWeight"] = "enacted"

        with self.assertRaises(ValidationError):
            validate_coverage(
                valid_coverage_payload(entries=entries),
                self.required_ids,
                self.module_ids,
            )

    def test_duplicate_or_unknown_competency_id_is_rejected(self):
        duplicate_entries = valid_coverage_payload()["entries"]
        duplicate_entries.append(copy.deepcopy(duplicate_entries[0]))
        unknown_entries = valid_coverage_payload()["entries"]
        unknown_entries[0]["competencyId"] = "UNKNOWN"

        for entries in (duplicate_entries, unknown_entries):
            with self.subTest(entries=entries):
                with self.assertRaises(ValidationError):
                    validate_coverage(
                        valid_coverage_payload(entries=entries),
                        self.required_ids,
                        self.module_ids,
                    )

    def test_required_strings_and_status_are_validated(self):
        invalid_mutations = (
            ("evidence", " "),
            ("risk", None),
            ("followUp", ""),
            ("coverageStatus", "open"),
            ("semanticAudit", "unreviewed"),
        )

        for field, value in invalid_mutations:
            entries = valid_coverage_payload()["entries"]
            entries[0][field] = value

            with self.subTest(field=field, value=value):
                with self.assertRaises(ValidationError):
                    validate_coverage(
                        valid_coverage_payload(entries=entries),
                        self.required_ids,
                        self.module_ids,
                    )


class CoverageRepositoryTests(unittest.TestCase):
    def test_phase0_file_entrypoint_runs_the_complete_chain(self):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, "-B", "scripts/validate_phase0.py"],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout,
            "phase 0, IUM09, IUM10 and IUM11 validation passed\n",
        )

    def test_phase0_entrypoint_runs_ium10_then_ium09_once_on_projection(self):
        call_order = []
        ium10_results = []
        ium11_results = []
        validate_ium10 = validate_phase0_script.validate_ium10
        validate_ium09 = validate_phase0_script.validate_ium09
        validate_ium11 = validate_phase0_script.validate_ium11

        def record_ium10(*args, **kwargs):
            call_order.append("ium10")
            result = validate_ium10(*args, **kwargs)
            ium10_results.append(result)
            return result

        def record_ium09(*args, **kwargs):
            call_order.append("ium09")
            return validate_ium09(*args, **kwargs)

        def record_ium11(*args, **kwargs):
            call_order.append("ium11")
            result = validate_ium11(*args, **kwargs)
            ium11_results.append(result)
            return result

        with mock.patch(
            "scripts.validate_phase0.validate_ium09",
            side_effect=record_ium09,
        ) as validate_ium09_mock, mock.patch(
            "scripts.validate_phase0.validate_ium10",
            side_effect=record_ium10,
        ) as validate_ium10_mock, mock.patch(
            "scripts.validate_phase0.validate_ium11",
            side_effect=record_ium11,
        ) as validate_ium11_mock, mock.patch("builtins.print") as print_mock:
            validate_phase0_script.main()

        self.assertEqual(call_order, ["ium10", "ium09", "ium11"])
        validate_ium10_mock.assert_called_once()
        validate_ium09_mock.assert_called_once()
        validate_ium11_mock.assert_called_once()
        self.assertEqual(len(ium11_results), 1)
        self.assertEqual(
            ium11_results[0]["publication"],
            {
                "productFiles": 27,
                "syntheticExamples": 7,
                "publications": 3,
                "publicationContracts": 1,
            },
        )
        (
            time_model,
            module_payload,
            current_coverage_payload,
            remediation_payload,
        ) = validate_ium10_mock.call_args.args
        projected_coverage_payload = validate_ium09_mock.call_args.args[1]
        module_payload_ium09, _, remediation_payload_ium09, contracts = (
            validate_ium09_mock.call_args.args
        )
        (
            time_model_ium11,
            ium10_result_ium11,
            protocol,
            evidence_schema,
            decision_schema,
            example_packages,
            cockpit_root,
        ) = validate_ium11_mock.call_args.args
        self.assertEqual(time_model["status"], "working")
        self.assertIs(time_model_ium11, time_model)
        self.assertIs(ium10_result_ium11, ium10_results[0])
        self.assertEqual(protocol["protocolVersion"], "1.0.0")
        self.assertEqual(
            evidence_schema["$schema"],
            "https://json-schema.org/draft/2020-12/schema",
        )
        self.assertEqual(
            decision_schema["$schema"],
            "https://json-schema.org/draft/2020-12/schema",
        )
        self.assertEqual(len(example_packages), 7)
        self.assertEqual(
            cockpit_root,
            Path(__file__).resolve().parents[1] / "pilot/cockpit",
        )
        self.assertIs(module_payload_ium09, module_payload)
        self.assertIs(remediation_payload_ium09, remediation_payload)
        self.assertEqual(len(module_payload["modules"]), 31)
        self.assertEqual(len(current_coverage_payload["entries"]), 171)
        self.assertEqual(len(projected_coverage_payload["entries"]), 171)
        self.assertEqual(len(remediation_payload["entries"]), 60)
        self.assertEqual(len(contracts), 171)
        self.assertEqual(
            Counter(
                entry["coverageStatus"]
                for entry in current_coverage_payload["entries"]
            ),
            Counter({"covered": 166, "partial": 5}),
        )
        self.assertEqual(
            Counter(
                entry["coverageStatus"]
                for entry in projected_coverage_payload["entries"]
            ),
            Counter({"covered": 164, "partial": 7}),
        )
        print_mock.assert_called_once_with(
            "phase 0, IUM09, IUM10 and IUM11 validation passed"
        )

    def test_repository_coverage_and_roadmap_are_complete_and_reviewable(self):
        root = Path(__file__).resolve().parents[1]
        curriculum_payloads = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted(
                (root / "curriculum").glob("**/competencies.json")
            )
        ]
        required_contracts = {}
        for payload in curriculum_payloads:
            normative_weight = (
                "orientation"
                if payload["metadata"]["normativeStatus"]
                == "orientation"
                else "enacted"
            )
            required_contracts.update(
                {
                    record["id"]: {
                        "normativeWeight": normative_weight,
                        "text": record["text"],
                    }
                    for record in payload["records"]
                    if record["recordType"] not in {"example", "operator"}
                }
            )
        module_payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(
                encoding="utf-8"
            )
        )
        module_contracts = {
            module["id"]: {
                "kind": module["kind"],
                "competencyIds": module["competencyIds"],
                "centralLearningAction": module["centralLearningAction"],
                "centralLearningProduct": module["centralLearningProduct"],
            }
            for module in module_payload["modules"]
        }
        module_competency_ids = {
            competency_id
            for module in module_payload["modules"]
            for competency_id in module["competencyIds"]
        }
        coverage_payload = json.loads(
            (root / "roadmap/coverage-plan.json").read_text(
                encoding="utf-8"
            )
        )
        remediation_payload = json.loads(
            (root / "roadmap/coverage-remediation.json").read_text(
                encoding="utf-8"
            )
        )

        coverage_ids = validate_coverage(
            coverage_payload,
            required_contracts,
            module_contracts,
        )
        self.assertEqual(len(coverage_ids), 171)
        self.assertEqual(module_competency_ids, coverage_ids)
        self.assertEqual(
            Counter(
                contract["normativeWeight"]
                for contract in required_contracts.values()
            ),
            Counter({"orientation": 95, "enacted": 76}),
        )
        remediation_entries = {
            entry["competencyId"]: entry
            for entry in remediation_payload["entries"]
        }
        entries_by_id = {
            entry["competencyId"]: entry
            for entry in coverage_payload["entries"]
        }
        legacy_covered_entries = [
            entry
            for entry in coverage_payload["entries"]
            if entry["competencyId"] not in remediation_entries
        ]
        self.assertEqual(len(legacy_covered_entries), 111)
        for entry in legacy_covered_entries:
            with self.subTest(legacy_covered_id=entry["competencyId"]):
                self.assertEqual(entry["coverageStatus"], "covered")
                self.assertEqual(entry["semanticAudit"], "operator-product-match")
                self.assertNotIn("evidenceContractId", entry)
        actual_status_counts = Counter(
            entry["coverageStatus"] for entry in coverage_payload["entries"]
        )
        self.assertEqual(
            actual_status_counts,
            Counter({"covered": 166, "partial": 5}),
        )
        self.assertEqual(
            Counter(
                (
                    entry["normativeWeight"],
                    entry["coverageStatus"],
                )
                for entry in coverage_payload["entries"]
            ),
            Counter(
                {
                    ("orientation", "covered"): 92,
                    ("orientation", "partial"): 3,
                    ("enacted", "covered"): 74,
                    ("enacted", "partial"): 2,
                }
            ),
        )
        self.assertEqual(
            len(
                {
                    entry["matchRationale"]
                    for entry in coverage_payload["entries"]
                }
            ),
            171,
        )
        expected_partial_ids = {
            competency_id
            for competency_id, entry in remediation_entries.items()
            if entry["decision"] == "remain-partial"
        } - {"LH26-E-PROG-001", "LH26-E-PROG-002"}
        for competency_id in expected_partial_ids:
            with self.subTest(competency_id=competency_id):
                entry = entries_by_id[competency_id]
                self.assertEqual(entry["coverageStatus"], "partial")
                self.assertEqual(
                    entry["semanticAudit"],
                    "documented-gap",
                )
                self.assertTrue(entry["reason"].strip())
                self.assertTrue(entry["risk"].strip())
                self.assertTrue(entry["followUp"].strip())
        for competency_id in {
            "LH26-E-PROG-001",
            "LH26-E-PROG-002",
            "LH26-E-PROG-003",
            "LH26-E-PROG-004",
        }:
            with self.subTest(progression_id=competency_id):
                entry = entries_by_id[competency_id]
                self.assertEqual(
                    entry["sequenceEvidenceId"], f"SE-{competency_id}"
                )
                self.assertEqual(
                    entry["timeReviewId"], f"TR-{competency_id}"
                )
        expected_covered_ids = {
            "BMB16-GYM-IK-PP-003",
            "INF7-16-GYM-PK-KK-003",
            "INF7-16-GYM-PK-KK-004",
            "LH26-E-DP-009",
        }
        for competency_id in expected_covered_ids:
            with self.subTest(competency_id=competency_id):
                entry = entries_by_id[competency_id]
                self.assertEqual(entry["coverageStatus"], "covered")
                self.assertEqual(
                    entry["semanticAudit"],
                    "operator-product-match",
                )

        roadmap = (root / "roadmap/module-roadmap.md").read_text(
            encoding="utf-8"
        )
        required_sections = (
            "## Planungsannahmen und Zeitmodell",
            "## Kernfolge Klasse 5",
            "## Kernfolge Klasse 6",
            "## Kernfolge Klasse 7",
            "## Flexible Kandidaten",
            "## Begründung der Abhängigkeiten",
            "## Curriculare Abdeckung",
            "## Jahreskorridore und Puffer",
            "## Analoge Materialien",
            "## Erhöhter Prüfbedarf",
            "## Empfehlung für den ersten Goldstandard-Pilot",
            "## Offene Entscheidungen und Risiken",
        )
        for section in required_sections:
            with self.subTest(section=section):
                self.assertIn(section, roadmap)
        modules_by_id = {
            module["id"]: module for module in module_payload["modules"]
        }
        semantic_contracts = {
            "IUM-5-CORE-06": (
                "vor einem Publikum vorstellen",
                "Kriterien",
            ),
            "IUM-6-CORE-02": (
                "private Selbstreflexion",
                "nicht erhoben, gespeichert oder bewertet",
            ),
            "IUM-7-CORE-04": (
                "arbeitsteilig als Team",
                "Teamreflexion und Präsentation",
            ),
            "IUM-7-CORE-08": (
                "vorhandenen Infrastruktur kommunizieren",
                "digitale Werkzeuge zum Teilen",
            ),
        }
        for module_id, required_phrases in semantic_contracts.items():
            module_text = " ".join(
                str(value)
                for value in modules_by_id[module_id].values()
                if isinstance(value, str)
            )
            for required_phrase in required_phrases:
                with self.subTest(
                    module_id=module_id,
                    required_phrase=required_phrase,
                ):
                    self.assertIn(
                        required_phrase.casefold(),
                        module_text.casefold(),
                    )
        for module_id in module_contracts:
            with self.subTest(module_id=module_id):
                self.assertIn(module_id, roadmap)
        coverage_section = markdown_section(
            roadmap, "## Curriculare Abdeckung"
        )
        baseline_section = markdown_section(
            coverage_section, "### Ausgangsbilanz vor IUM09"
        )
        final_section = markdown_section(
            coverage_section, "### Auditierte Endbilanz nach IUM09"
        )
        baseline_status_counts = Counter(
            entry["coverageStatus"]
            for entry in legacy_covered_entries
        )
        baseline_status_counts.update(
            entry["before"]["coverageStatus"]
            for entry in remediation_entries.values()
        )
        self.assertIn(
            (
                f"| Gesamt | {len(coverage_payload['entries'])} | "
                f"{baseline_status_counts['covered']} `covered`, "
                f"{baseline_status_counts['partial']} `partial`, "
                "0 `deferred` |"
            ),
            baseline_section,
        )
        historical_status_counts = Counter(
            entry["after"]["coverageStatus"]
            for entry in remediation_entries.values()
        )
        historical_status_counts.update(
            entry["coverageStatus"] for entry in legacy_covered_entries
        )
        self.assertIn(
            (
                f"| Gesamt | {len(coverage_payload['entries'])} | "
                f"{historical_status_counts['covered']} `covered`, "
                f"{historical_status_counts['partial']} `partial`, "
                "0 `deferred` |"
            ),
            final_section,
        )
        cause_section = markdown_section(
            coverage_section, "### Ergebnis nach Ursachenklasse"
        )
        for cause_class in sorted(
            {entry["causeClass"] for entry in remediation_entries.values()}
        ):
            cause_entries = [
                entry
                for entry in remediation_entries.values()
                if entry["causeClass"] == cause_class
            ]
            with self.subTest(cause_class=cause_class):
                self.assertIn(
                    (
                        f"| `{cause_class}` | {len(cause_entries)} | "
                        f"{sum(entry['decision'] == 'covered' for entry in cause_entries)} | "
                        f"{sum(entry['decision'] == 'remain-partial' for entry in cause_entries)} |"
                    ),
                    cause_section,
                )
        handoff_section = markdown_section(
            coverage_section, "### IUM10-Zeitübergabe"
        )
        published_handoffs = []
        for line in handoff_section.splitlines():
            if not line.startswith("| `IUM-"):
                continue
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            self.assertEqual(len(cells), 4)
            published_handoffs.append(
                (
                    cells[0].strip("`"),
                    cells[1].strip("`"),
                    cells[2].strip("`"),
                    cells[3],
                )
            )
        expected_handoffs = sorted(
            (
                entry["before"]["evidenceModuleId"],
                entry["competencyId"],
                entry["timeImpact"]["level"],
                entry["timeImpact"]["rationale"],
            )
            for entry in remediation_entries.values()
            if entry["timeImpact"]["level"]
            in {"review-required", "roadmap-dependent"}
        )
        self.assertEqual(published_handoffs, expected_handoffs)
        time_model = json.loads(
            (root / "roadmap/time-model.json").read_text(encoding="utf-8")
        )
        capacity_model = time_model["capacityModel"]
        self.assertIn("projectAssumption", capacity_model)
        project_assumption = capacity_model["projectAssumption"]
        self.assertEqual(
            project_assumption["nominalUnits"],
            project_assumption["coreUnits"]
            + project_assumption["bufferUnits"],
        )
        historical_core_ranges = {
            grade: (
                sum(
                    module["lessonRange"]["min"]
                    for module in module_payload["modules"]
                    if module["grade"] == grade and module["kind"] == "core"
                ),
                sum(
                    module["lessonRange"]["max"]
                    for module in module_payload["modules"]
                    if module["grade"] == grade and module["kind"] == "core"
                ),
            )
            for grade in (5, 6, 7)
        }
        for required_text in (
            f'{project_assumption["coreUnits"]} Unterrichtseinheiten Kern',
            f'{project_assumption["bufferUnits"]} Unterrichtseinheiten Puffer',
            *(
                f"{minimum}-{maximum}"
                for minimum, maximum in historical_core_ranges.values()
            ),
            "zeitlich nicht freigegeben",
            "Operator und Gegenstand",
            "IUM-5-CORE-05",
            "keine Phase-1-Implementierungsplanung",
        ):
            with self.subTest(required_text=required_text):
                self.assertIn(required_text, roadmap)
        self.assertNotIn("keine Phase-2-Implementierungsplanung", roadmap)


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
