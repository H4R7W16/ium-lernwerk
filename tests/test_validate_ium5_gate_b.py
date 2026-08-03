import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts import validate_ium5_gate_b


ROOT = Path(__file__).resolve().parents[1]
GATE_B_ROOT = ROOT / "pilot/ium5-gate-b"
SCHEMA_ROOT = GATE_B_ROOT / "schemas"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def iter_object_schemas(value, pointer="$"):
    if isinstance(value, dict):
        if value.get("type") == "object" or "properties" in value:
            yield pointer, value
        for key, item in value.items():
            yield from iter_object_schemas(item, f"{pointer}/{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from iter_object_schemas(item, f"{pointer}/{index}")


TECHNICAL_ROW_IDS = (
    "TECH-IPAD-TOUCH",
    "TECH-IPAD-VO",
    "TECH-DESKTOP-CHROMIUM",
    "TECH-DESKTOP-FIREFOX",
    "TECH-NET-OFFLINE-UPDATE",
    "TECH-LMS-ROUTE",
)


def valid_technical_evidence() -> dict:
    rows = []
    for row_id in TECHNICAL_ROW_IDS:
        rows.append(
            {
                "id": row_id,
                "operatingSystem": {"family": "linux", "version": "1"},
                "browser": {"family": "chromium", "version": "1"},
                "managedStatus": "not-managed",
                "policyStatus": "documented",
                "networkContext": "school-network",
                "checks": [{"id": "startup", "result": "pass"}],
                "result": "pass",
                "findings": [],
                "privateEvidenceRef": f"EVID-TECH-{row_id.removeprefix('TECH-')}",
            }
        )
    return {
        "documentType": "ium5-gate-b-technical-evidence",
        "schemaVersion": 1,
        "protocolId": "IUM5-GATE-B-1",
        "evidenceId": "GB-TECH-SYNTHETIC-01",
        "module": {
            "id": "IUM-5-CORE-05",
            "version": "0.1.0",
            "status": "working",
            "deviceVerified": "not-run",
        },
        "build": {
            "buildRevision": "1" * 40,
            "previewId": "ium5-gate-b-synthetic-001",
            "publicationMode": "gate-b-preview",
        },
        "policySummary": "documented",
        "rows": rows,
        "limitedException": None,
        "privacy": {
            "unexpectedThirdPartyRequests": False,
            "prohibitedDataObserved": False,
            "telemetryObserved": False,
        },
        "result": "pass",
        "retentionClass": "outside-repository-until-decision-plus-30-days",
    }


OBSERVATION_IDS = (
    "prediction-used",
    "trace-explained",
    "first-deviation-localized",
    "repair-hypothesis",
    "minimal-revision-retested",
    "loop-decision-justified",
    "systems-transfer",
    "support-preserves-thinking",
    "shared-consolidation",
)


def valid_pilot_evidence(run_kind: str) -> dict:
    confirmation = run_kind == "confirmation"
    phase_count = 6 if confirmation else 5
    return {
        "documentType": "ium5-gate-b-pilot-evidence",
        "schemaVersion": 1,
        "protocolId": "IUM5-GATE-B-1",
        "evidenceId": f"GB-PILOT-{'CONFIRM-01' if confirmation else 'EXPLORE-01'}",
        "module": {
            "id": "IUM-5-CORE-05",
            "version": "0.1.0",
            "status": "working",
            "deviceVerified": "not-run",
        },
        "build": {
            "buildRevision": "1" * 40,
            "previewId": "ium5-gate-b-synthetic-001",
            "publicationMode": "gate-b-preview",
        },
        "runKind": run_kind,
        "pathKind": "extended-270" if confirmation else "regular-225",
        "context": {
            "gradeBand": "grade-5",
            "groupSizeBand": "20-29",
            "seasonWindow": "autumn",
            "contextRelation": (
                "different-class-same-teacher" if confirmation else "first-class"
            ),
        },
        "phases": [
            {
                "id": f"LESSON-{index}",
                "enacted": True,
                "plannedMinutes": 45,
                "actualBand": "35-45",
                "deviationCode": "none",
            }
            for index in range(1, phase_count + 1)
        ],
        "observations": [
            {"id": observation_id, "band": "met"}
            for observation_id in OBSERVATION_IDS
        ],
        "timeFit": "pass",
        "sharedConsolidation": "completed",
        "fallback": {"used": False, "function": "not-needed"},
        "supportDemand": "low",
        "disruptions": [],
        "learnerPulse": {
            "status": "reported",
            "items": [
                {
                    "id": prompt_id,
                    "status": "reported",
                    "validResponses": 10,
                    "agree": 7,
                    "partly": 2,
                    "disagree": 1,
                    "noAnswer": 0,
                }
                for prompt_id in (
                    "clarity",
                    "cognitive-engagement",
                    "support-usefulness",
                )
            ],
        },
        "privacy": {
            "breachObserved": False,
            "prohibitedDataCollected": False,
            "paperSheetStatus": "destroyed",
            "digitalPackageStorage": "outside-repository",
        },
        "result": "pass",
        "retentionClass": "outside-repository-until-decision-plus-30-days",
    }


def valid_decision_package() -> dict:
    technical = valid_technical_evidence()
    exploratory = valid_pilot_evidence("exploratory")
    confirmation = valid_pilot_evidence("confirmation")
    return {
        "documentType": "ium5-gate-b-decision-package",
        "schemaVersion": 1,
        "protocolId": "IUM5-GATE-B-1",
        "decisionId": "GB-DECISION-SYNTHETIC-01",
        "module": copy.deepcopy(technical["module"]),
        "build": copy.deepcopy(technical["build"]),
        "technicalEvidence": technical,
        "exploratoryEvidence": exploratory,
        "confirmationEvidence": confirmation,
        "reviews": {
            "pilotTeacher": "approved",
            "fachDidaktik": "approved",
            "engineeringAccessibilityPrivacy": "approved",
            "coordination": "approved",
            "commissioner": "accepted",
        },
        "retention": {
            "paperAggregates": "destroyed",
            "digitalRealPackages": "deleted",
        },
        "derived": {
            "technicalEntry": "pass",
            "exploratoryResult": "pass",
            "confirmationResult": "pass",
            "recommendation": "eligible-for-working-release-review",
            "productStatus": "working",
            "deviceVerified": "not-run",
        },
    }


class ProtocolContractTests(unittest.TestCase):
    def test_protocol_defines_the_complete_nonrelease_contract(self):
        protocol = load_json(GATE_B_ROOT / "protocol.json")

        self.assertEqual(protocol["schemaVersion"], 1)
        self.assertEqual(protocol["protocolId"], "IUM5-GATE-B-1")
        self.assertEqual(
            protocol["module"],
            {
                "id": "IUM-5-CORE-05",
                "version": "0.1.0",
                "status": "working",
                "deviceVerified": "not-run",
            },
        )
        self.assertEqual(protocol["minimumLearnerResponses"], 10)
        self.assertEqual(
            protocol["allowedRecommendation"],
            "eligible-for-working-release-review",
        )

    def test_protocol_matrix_and_pilot_sequence_are_closed(self):
        protocol = load_json(GATE_B_ROOT / "protocol.json")

        self.assertEqual(
            [row["id"] for row in protocol["technicalMatrix"]],
            [
                "TECH-IPAD-TOUCH",
                "TECH-IPAD-VO",
                "TECH-DESKTOP-CHROMIUM",
                "TECH-DESKTOP-FIREFOX",
                "TECH-NET-OFFLINE-UPDATE",
                "TECH-LMS-ROUTE",
            ],
        )
        self.assertEqual(
            [(run["runKind"], run["pathKind"], run["minutes"]) for run in protocol["pilotRuns"]],
            [
                ("exploratory", "regular-225", 225),
                ("confirmation", "extended-270", 270),
            ],
        )
        self.assertEqual(len(protocol["observationCriteria"]), 9)
        self.assertEqual(len(protocol["learnerPulsePrompts"]), 3)

    def test_protocol_excludes_identity_and_automatic_release_fields(self):
        protocol = load_json(GATE_B_ROOT / "protocol.json")
        prohibited = set(protocol["prohibitedFieldNames"])

        self.assertTrue(
            {
                "name",
                "email",
                "school",
                "classCode",
                "exactDate",
                "ipAddress",
                "deviceId",
                "freeText",
                "score",
                "studentId",
                "learningProduct",
                "telemetry",
            }.issubset(prohibited)
        )
        self.assertEqual(protocol["statusMutation"], "forbidden")
        self.assertEqual(protocol["realEvidenceRepositoryPolicy"], "outside-repository")


class SchemaContractTests(unittest.TestCase):
    SCHEMA_NAMES = (
        "technical-evidence.schema.json",
        "pilot-evidence.schema.json",
        "decision-package.schema.json",
    )

    def test_all_schemas_are_draft_2020_12_and_recursively_closed(self):
        for name in self.SCHEMA_NAMES:
            with self.subTest(name=name):
                schema = load_json(SCHEMA_ROOT / name)
                self.assertEqual(
                    schema["$schema"],
                    "https://json-schema.org/draft/2020-12/schema",
                )
                object_schemas = list(iter_object_schemas(schema))
                self.assertGreater(len(object_schemas), 2)
                for pointer, object_schema in object_schemas:
                    self.assertIs(
                        object_schema.get("additionalProperties"),
                        False,
                        f"{name}{pointer} is not closed",
                    )
                    self.assertEqual(
                        set(object_schema.get("required", [])),
                        set(object_schema.get("properties", {})),
                        f"{name}{pointer} does not require every declared field",
                    )

    def test_schema_references_are_local_and_resolve(self):
        for name in self.SCHEMA_NAMES:
            schema = load_json(SCHEMA_ROOT / name)
            pending = [schema]
            while pending:
                value = pending.pop()
                if isinstance(value, dict):
                    reference = value.get("$ref")
                    if reference is not None:
                        self.assertFalse(reference.startswith(("http://", "https://")))
                        target_name = reference.split("#", 1)[0]
                        if target_name:
                            self.assertTrue((SCHEMA_ROOT / target_name).is_file())
                    pending.extend(value.values())
                elif isinstance(value, list):
                    pending.extend(value)

    def test_root_document_types_are_distinct_and_fixed(self):
        expected = {
            "technical-evidence.schema.json": "ium5-gate-b-technical-evidence",
            "pilot-evidence.schema.json": "ium5-gate-b-pilot-evidence",
            "decision-package.schema.json": "ium5-gate-b-decision-package",
        }
        for name, document_type in expected.items():
            with self.subTest(name=name):
                schema = load_json(SCHEMA_ROOT / name)
                self.assertEqual(
                    schema["properties"]["documentType"]["const"],
                    document_type,
                )


class ValidatorTests(unittest.TestCase):
    def assert_issue(self, document: dict, code: str):
        issues = validate_ium5_gate_b.validate_evidence(document)
        self.assertIn(code, {issue.code for issue in issues}, issues)

    def test_valid_technical_evidence_is_accepted(self):
        self.assertEqual(
            validate_ium5_gate_b.validate_evidence(valid_technical_evidence()),
            [],
        )

    def test_unknown_nested_field_is_rejected(self):
        document = valid_technical_evidence()
        document["rows"][0]["browser"]["engine"] = "Blink"
        self.assert_issue(document, "SCHEMA_ADDITIONAL_PROPERTY")

    def test_seventh_matrix_row_is_rejected(self):
        document = valid_technical_evidence()
        document["rows"].append(dict(document["rows"][0]))
        self.assert_issue(document, "SCHEMA_MAX_ITEMS")

    def test_missing_build_revision_is_rejected(self):
        document = valid_technical_evidence()
        del document["build"]["buildRevision"]
        self.assert_issue(document, "SCHEMA_REQUIRED")

    def test_serial_number_field_is_rejected_by_privacy_scan(self):
        document = valid_technical_evidence()
        document["rows"][0]["serialNumber"] = "device-17"
        self.assert_issue(document, "PRIVACY_FORBIDDEN_FIELD")

    def test_ip_address_in_a_string_is_rejected_by_privacy_scan(self):
        document = valid_technical_evidence()
        document["rows"][0]["findings"] = [
            {
                "code": "network-policy-blocker",
                "severity": "low",
                "status": "resolved",
                "reproductionSteps": ["Request observed at 192.0.2.17"],
            }
        ]
        self.assert_issue(document, "PRIVACY_IP_ADDRESS")

    def test_free_prose_field_is_rejected_by_privacy_scan(self):
        document = valid_technical_evidence()
        document["rows"][0]["freeText"] = "unstructured note"
        self.assert_issue(document, "PRIVACY_FORBIDDEN_FIELD")

    def test_matrix_ids_must_match_the_protocol_exactly(self):
        document = valid_technical_evidence()
        document["rows"][1]["id"] = TECHNICAL_ROW_IDS[0]
        self.assert_issue(document, "SEMANTIC_MATRIX_IDS")

    def test_lowercase_git_sha_is_not_treated_as_a_secret(self):
        document = valid_technical_evidence()
        document["build"]["buildRevision"] = "abcdef0123456789" * 2 + "abcdef01"
        self.assertEqual(validate_ium5_gate_b.validate_evidence(document), [])

    def test_sensitive_string_patterns_are_rejected(self):
        cases = (
            ("teacher@example.org", "PRIVACY_EMAIL_ADDRESS"),
            ("2001:db8::1", "PRIVACY_IP_ADDRESS"),
            ("Z" * 40, "PRIVACY_SECRET_40"),
        )
        for value, expected_code in cases:
            with self.subTest(expected_code=expected_code):
                issues = validate_ium5_gate_b.scan_forbidden_content(
                    {"reproductionSteps": [value]}
                )
                self.assertIn(expected_code, {issue.code for issue in issues})


class CliTests(unittest.TestCase):
    SCRIPT = ROOT / "scripts/validate_ium5_gate_b.py"

    def run_cli(self, *arguments):
        return subprocess.run(
            [sys.executable, "-B", str(self.SCRIPT), *map(str, arguments)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_protocol_command_succeeds(self):
        completed = self.run_cli("protocol")
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("PROTOCOL_VALID", completed.stdout)

    def test_invalid_evidence_command_fails_with_stable_error_code(self):
        document = valid_technical_evidence()
        document["rows"][0]["serialNumber"] = "device-17"
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "invalid.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            completed = self.run_cli("evidence", path)

        self.assertEqual(completed.returncode, 1)
        self.assertIn("PRIVACY_FORBIDDEN_FIELD", completed.stdout)

    def test_validation_does_not_modify_the_input_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            path = directory / "evidence.json"
            path.write_text(json.dumps(valid_technical_evidence()), encoding="utf-8")
            before = {item.name: item.read_bytes() for item in directory.iterdir()}

            completed = self.run_cli("evidence", path)

            after = {item.name: item.read_bytes() for item in directory.iterdir()}
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(after, before)

    def test_synthetic_command_checks_six_examples_and_three_outcomes(self):
        completed = self.run_cli("synthetic")
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(completed.stdout.count("SYNTHETIC_VALID\t"), 6)
        self.assertEqual(completed.stdout.count("SYNTHETIC_OUTCOME\t"), 3)
        for expected in (
            "eligible-for-working-release-review",
            "revise-required",
            "not-evaluable",
        ):
            self.assertIn(expected, completed.stdout)


class DecisionTests(unittest.TestCase):
    def test_positive_package_is_eligible_only_for_working_release_review(self):
        derived = validate_ium5_gate_b.evaluate_decision(valid_decision_package())
        self.assertEqual(
            derived,
            {
                "technicalEntry": "pass",
                "exploratoryResult": "pass",
                "confirmationResult": "pass",
                "recommendation": "eligible-for-working-release-review",
                "productStatus": "working",
                "deviceVerified": "not-run",
            },
        )

    def test_decision_table_has_stable_precedence(self):
        cases = (
            (
                "technical row blocked",
                lambda package: package["technicalEvidence"]["rows"][0].update(
                    result="blocked"
                ),
                "not-evaluable",
            ),
            (
                "privacy breach",
                lambda package: package["exploratoryEvidence"]["privacy"].update(
                    breachObserved=True
                ),
                "revise-required",
            ),
            (
                "same class",
                lambda package: package["confirmationEvidence"]["context"].update(
                    contextRelation="first-class"
                ),
                "not-evaluable",
            ),
            (
                "missing confirmation",
                lambda package: package.pop("confirmationEvidence"),
                "not-evaluable",
            ),
            (
                "criterion not met",
                lambda package: package["exploratoryEvidence"]["observations"][0].update(
                    band="not-met"
                ),
                "revise-required",
            ),
            (
                "two partly",
                lambda package: (
                    package["confirmationEvidence"]["observations"][0].update(
                        band="partly"
                    ),
                    package["confirmationEvidence"]["observations"][1].update(
                        band="partly"
                    ),
                ),
                "revise-required",
            ),
            (
                "review rejected",
                lambda package: package["reviews"].update(pilotTeacher="rejected"),
                "revise-required",
            ),
            (
                "limited technical entry",
                lambda package: package["technicalEvidence"].update(
                    policySummary="limited-accepted"
                ),
                "not-evaluable",
            ),
            (
                "build mismatch",
                lambda package: package["confirmationEvidence"]["build"].update(
                    buildRevision="2" * 40
                ),
                "not-evaluable",
            ),
            (
                "unresolved high technical finding",
                lambda package: package["technicalEvidence"]["rows"][0].update(
                    findings=[
                        {
                            "code": "interaction-loss",
                            "severity": "high",
                            "status": "unresolved",
                            "reproductionSteps": [],
                        }
                    ]
                ),
                "revise-required",
            ),
            (
                "deletion not confirmed",
                lambda package: package["retention"].update(
                    digitalRealPackages="scheduled-within-30-days"
                ),
                "not-evaluable",
            ),
        )
        for label, mutate, expected in cases:
            with self.subTest(label=label):
                package = valid_decision_package()
                mutate(package)
                derived = validate_ium5_gate_b.evaluate_decision(package)
                self.assertEqual(derived["recommendation"], expected)

    def test_privacy_breach_precedes_incomplete_evidence(self):
        package = valid_decision_package()
        package["technicalEvidence"]["privacy"]["telemetryObserved"] = True
        del package["confirmationEvidence"]
        derived = validate_ium5_gate_b.evaluate_decision(package)
        self.assertEqual(derived["recommendation"], "revise-required")

    def test_derived_values_are_checked_instead_of_trusted(self):
        package = valid_decision_package()
        package["derived"]["recommendation"] = "revise-required"
        issues, derived = validate_ium5_gate_b.validate_decision(package)
        self.assertIn("DECISION_DERIVED_MISMATCH", {issue.code for issue in issues})
        self.assertEqual(
            derived["recommendation"],
            "eligible-for-working-release-review",
        )


class PulseSuppressionTests(unittest.TestCase):
    def test_nine_valid_answers_are_suppressed_without_totals(self):
        self.assertEqual(
            validate_ium5_gate_b.normalize_pulse(
                {"agree": 4, "partly": 3, "disagree": 2, "noAnswer": 5}
            ),
            {"status": "suppressed"},
        )

    def test_ten_valid_answers_may_be_reported(self):
        self.assertEqual(
            validate_ium5_gate_b.normalize_pulse(
                {"agree": 7, "partly": 2, "disagree": 1, "noAnswer": 0}
            ),
            {
                "status": "reported",
                "validResponses": 10,
                "agree": 7,
                "partly": 2,
                "disagree": 1,
                "noAnswer": 0,
            },
        )

    def test_reported_item_below_threshold_is_rejected(self):
        document = valid_pilot_evidence("exploratory")
        document["learnerPulse"]["items"][0].update(
            validResponses=9,
            agree=6,
            partly=2,
            disagree=1,
        )
        issues = validate_ium5_gate_b.validate_evidence(document)
        self.assertIn("PULSE_MINIMUM_SUPPRESSION", {issue.code for issue in issues})

    def test_suppressed_item_cannot_carry_counts(self):
        document = valid_pilot_evidence("exploratory")
        document["learnerPulse"]["items"][0]["status"] = "suppressed"
        issues = validate_ium5_gate_b.validate_evidence(document)
        self.assertIn("PULSE_SUPPRESSED_VALUES", {issue.code for issue in issues})

    def test_suppressed_package_item_with_no_counts_is_valid(self):
        document = valid_pilot_evidence("exploratory")
        document["learnerPulse"] = {
            "status": "partly-suppressed",
            "items": [
                {"id": "clarity", "status": "suppressed"},
                document["learnerPulse"]["items"][1],
                document["learnerPulse"]["items"][2],
            ],
        }
        self.assertEqual(validate_ium5_gate_b.validate_evidence(document), [])


if __name__ == "__main__":
    unittest.main()
