import copy
import json
import unittest
from pathlib import Path

from scripts.validate_ium10 import (
    BASELINE_COVERAGE_PROJECTION_SHA256,
    BASELINE_TIME_HANDOFF_SHA256,
    IUM10ValidationError,
    coverage_projection_fingerprint,
    time_handoff_fingerprint,
    validate_ium10_baseline,
)


class IUM10BaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        cls.module_payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(encoding="utf-8")
        )
        cls.coverage_payload = json.loads(
            (root / "roadmap/coverage-plan.json").read_text(encoding="utf-8")
        )
        cls.remediation_payload = json.loads(
            (root / "roadmap/coverage-remediation.json").read_text(encoding="utf-8")
        )

    def validate_baseline(self, module_payload=None, coverage_payload=None, remediation_payload=None):
        return validate_ium10_baseline(
            self.module_payload if module_payload is None else module_payload,
            self.coverage_payload if coverage_payload is None else coverage_payload,
            self.remediation_payload if remediation_payload is None else remediation_payload,
        )

    def test_repository_baseline_has_immutable_module_coverage_and_handoff_contracts(self):
        result = self.validate_baseline()

        self.assertEqual(len(result["moduleIds"]), 31)
        self.assertEqual(len(result["coverageIds"]), 171)
        self.assertEqual(len(result["handoffIds"]), 60)
        self.assertEqual(
            coverage_projection_fingerprint(
                self.coverage_payload,
                self.remediation_payload,
            ),
            BASELINE_COVERAGE_PROJECTION_SHA256,
        )
        self.assertEqual(
            time_handoff_fingerprint(self.remediation_payload),
            BASELINE_TIME_HANDOFF_SHA256,
        )

    def test_rejects_mutated_module_id_grade_kind_prerequisite_or_lesson_range(self):
        mutations = (
            ("id", "IUM-5-CORE-01-MUTATED"),
            ("grade", 8),
            ("kind", "extension"),
            ("prerequisiteModuleIds", ["IUM-5-CORE-99"]),
            ("lessonRange", {"min": 99, "max": 100}),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                module_payload = copy.deepcopy(self.module_payload)
                module_payload["modules"][0][field] = value

                with self.assertRaises(IUM10ValidationError):
                    self.validate_baseline(module_payload=module_payload)

    def test_rejects_mutated_coverage_id_module_assignment_or_ium09_status(self):
        mutations = (
            ("competencyId", "MUTATED-COVERAGE-ID"),
            ("moduleIds", ["IUM-5-CORE-02"]),
            ("coverageStatus", "partial"),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                coverage_payload = copy.deepcopy(self.coverage_payload)
                coverage_payload["entries"][0][field] = value

                with self.assertRaises(IUM10ValidationError):
                    self.validate_baseline(coverage_payload=coverage_payload)

    def test_rejects_mutated_handoff_id_module_level_or_rationale(self):
        mutations = (
            ("competencyId", "MUTATED-HANDOFF-ID"),
            ("before.evidenceModuleId", "IUM-5-CORE-02"),
            ("timeImpact.level", "none-detected"),
            ("timeImpact.rationale", "Mutierte Übergabebegründung."),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                remediation_payload = copy.deepcopy(self.remediation_payload)
                target = remediation_payload["entries"][0]
                container, _, key = field.rpartition(".")
                if container:
                    target[container][key] = value
                else:
                    target[key] = value

                with self.assertRaises(IUM10ValidationError):
                    self.validate_baseline(remediation_payload=remediation_payload)
