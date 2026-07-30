import copy
import json
import unittest
from pathlib import Path

from scripts.validate_ium09 import (
    BASELINE_MODULE_STRUCTURE_FINGERPRINT_SHA256,
    IUM09ValidationError,
    module_structure_fingerprint,
    validate_coverage_evidence,
)


PRIVATE_BOUNDARY_TEXT = (
    "Das private lokale Artefakt wird nicht erhoben, übertragen, "
    "eingesammelt, gespeichert oder bewertet."
)


def core_module(**overrides):
    module = {
        "id": "IUM-5-CORE-01",
        "grade": 5,
        "kind": "core",
        "competencyIds": ["BMB16-GYM-IK-GM-001"],
        "prerequisiteModuleIds": [],
        "lessonRange": {"min": 5, "max": 7},
    }
    module.update(overrides)
    return module


def module_payload(*modules):
    return {"modules": list(modules)}


def curriculum_contracts():
    return {
        "BMB16-GYM-IK-GM-001": {"text": "Konkrete Kompetenz."},
        "BMB16-GYM-IK-GM-002": {"text": "Zweite Kompetenz."},
        "BMB16-GYM-IK-GM-003": {"text": "Dritte Kompetenz."},
    }


def evidence_contract(**overrides):
    contract = {
        "id": "CE-IUM-5-CORE-01-BMB16-GYM-IK-GM-001",
        "competencyId": "BMB16-GYM-IK-GM-001",
        "mode": "module-detail",
        "learningAction": "Die Kompetenz fachlich ausführen.",
        "productEvidence": "Die fachliche Produktspur.",
        "productVisibility": "shared",
    }
    contract.update(overrides)
    return contract


def school_context_contract(**overrides):
    contract = evidence_contract(
        mode="school-context",
        executionType="actual-local-use",
        localConfigurationRequirement="Die lokale Schulumgebung wird verwendet.",
    )
    contract.update(overrides)
    return contract


def private_local_contract(**overrides):
    contract = evidence_contract(
        mode="private-local",
        productVisibility="private-local",
        privacyBoundary=PRIVATE_BOUNDARY_TEXT,
        nonPersonalFollowUp="Ein fiktiver Fall wird fachlich beurteilt.",
    )
    contract.update(overrides)
    return contract


class ValidateCoverageEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        cls.repository_payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(encoding="utf-8")
        )

    def validate(self, *contracts, module=None):
        payload = copy.deepcopy(self.repository_payload)
        module = payload["modules"][0] if module is None else module
        if module is not payload["modules"][0]:
            payload["modules"][0] = module
        module["coverageEvidence"] = list(contracts)
        return validate_coverage_evidence(
            payload, curriculum_contracts()
        )

    def test_accepts_all_valid_evidence_modes(self):
        second = school_context_contract(
            id="CE-IUM-5-CORE-01-BMB16-GYM-IK-GM-002",
            competencyId="BMB16-GYM-IK-GM-002",
        )
        private = private_local_contract(
            id="CE-IUM-5-CORE-01-BMB16-GYM-IK-GM-003",
            competencyId="BMB16-GYM-IK-GM-003",
        )
        result = self.validate(evidence_contract(), second, private)
        self.assertEqual(
            set(result),
            {
                "CE-IUM-5-CORE-01-BMB16-GYM-IK-GM-001",
                "CE-IUM-5-CORE-01-BMB16-GYM-IK-GM-002",
                "CE-IUM-5-CORE-01-BMB16-GYM-IK-GM-003",
            },
        )
        self.assertEqual(result[private["id"]]["mode"], "private-local")

    def test_rejects_unknown_competency(self):
        contract = evidence_contract(competencyId="UNKNOWN")
        contract["id"] = "CE-IUM-5-CORE-01-UNKNOWN"
        with self.assertRaisesRegex(IUM09ValidationError, "unknown competency"):
            self.validate(contract)

    def test_rejects_contract_for_flexible_module(self):
        module = core_module(kind="extension")
        with self.assertRaisesRegex(IUM09ValidationError, "core module"):
            self.validate(evidence_contract(), module=module)

    def test_rejects_duplicate_contract_id(self):
        with self.assertRaisesRegex(IUM09ValidationError, "unique"):
            self.validate(evidence_contract(), evidence_contract())

    def test_rejects_id_that_does_not_encode_module_and_competency(self):
        contract = evidence_contract(id="CE-IUM-5-CORE-01-WRONG")
        with self.assertRaisesRegex(IUM09ValidationError, "id"):
            self.validate(contract)

    def test_rejects_invalid_evidence_mode(self):
        with self.assertRaisesRegex(IUM09ValidationError, "mode"):
            self.validate(evidence_contract(mode="roadmap-level"))

    def test_rejects_invalid_product_visibility(self):
        with self.assertRaisesRegex(IUM09ValidationError, "visibility"):
            self.validate(evidence_contract(productVisibility="public"))

    def test_rejects_empty_coverage_evidence_when_field_is_present(self):
        payload = copy.deepcopy(self.repository_payload)
        payload["modules"][0]["coverageEvidence"] = []
        with self.assertRaisesRegex(IUM09ValidationError, "nonempty"):
            validate_coverage_evidence(payload, curriculum_contracts())

    def test_requires_actual_local_use_for_school_context(self):
        with self.assertRaisesRegex(IUM09ValidationError, "actual-local-use"):
            self.validate(school_context_contract(executionType="simulation"))

    def test_requires_local_configuration_for_school_context(self):
        contract = school_context_contract()
        del contract["localConfigurationRequirement"]
        with self.assertRaisesRegex(IUM09ValidationError, "localConfigurationRequirement"):
            self.validate(contract)

    def test_rejects_private_local_contract_with_nonprivate_visibility(self):
        with self.assertRaisesRegex(IUM09ValidationError, "private-local"):
            self.validate(private_local_contract(productVisibility="shared"))

    def test_requires_exact_private_boundary(self):
        with self.assertRaisesRegex(IUM09ValidationError, "privacyBoundary"):
            self.validate(private_local_contract(privacyBoundary="Nicht speichern."))

    def test_requires_nonpersonal_follow_up_for_private_local(self):
        contract = private_local_contract()
        del contract["nonPersonalFollowUp"]
        with self.assertRaisesRegex(IUM09ValidationError, "nonPersonalFollowUp"):
            self.validate(contract)


class ModuleStructureFingerprintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        cls.repository_payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(encoding="utf-8")
        )

    def test_repository_payload_matches_immutable_structure_baseline(self):
        self.assertEqual(
            module_structure_fingerprint(self.repository_payload),
            BASELINE_MODULE_STRUCTURE_FINGERPRINT_SHA256,
        )

    def test_rejects_changed_immutable_module_fields(self):
        mutations = {
            "id": lambda module: module.__setitem__("id", "IUM-5-CORE-99"),
            "grade": lambda module: module.__setitem__("grade", 6),
            "kind": lambda module: module.__setitem__("kind", "extension"),
            "prerequisiteModuleIds": lambda module: module.__setitem__(
                "prerequisiteModuleIds", ["IUM-5-CORE-01"]
            ),
            "lessonRange": lambda module: module.__setitem__(
                "lessonRange", {"min": 6, "max": 8}
            ),
        }
        for field, mutate in mutations.items():
            with self.subTest(field=field):
                payload = copy.deepcopy(self.repository_payload)
                mutate(payload["modules"][0])
                with self.assertRaisesRegex(
                    IUM09ValidationError, "module structure fingerprint"
                ):
                    validate_coverage_evidence(payload, curriculum_contracts())

    def test_json_key_order_does_not_change_fingerprint(self):
        reordered_payload = json.loads(
            json.dumps(self.repository_payload, sort_keys=True, ensure_ascii=False)
        )
        self.assertEqual(
            module_structure_fingerprint(self.repository_payload),
            module_structure_fingerprint(reordered_payload),
        )


if __name__ == "__main__":
    unittest.main()
