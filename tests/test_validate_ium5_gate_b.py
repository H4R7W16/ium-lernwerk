import json
from pathlib import Path
import unittest


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


if __name__ == "__main__":
    unittest.main()
