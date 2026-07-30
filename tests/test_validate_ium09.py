import copy
import json
import unittest
from pathlib import Path

from scripts.validate_ium09 import (
    BASELINE_PARTIAL_IDS,
    BASELINE_MODULE_STRUCTURE_FINGERPRINT_SHA256,
    IUM09ValidationError,
    coverage_baseline_fingerprint,
    module_structure_fingerprint,
    validate_coverage_evidence,
    validate_ium09,
    validate_remediation_ledger,
    validate_remediated_coverage,
)


PRIVATE_BOUNDARY_TEXT = (
    "Das private lokale Artefakt wird nicht erhoben, übertragen, "
    "eingesammelt, gespeichert oder bewertet."
)


EXPECTED_CAUSE_CLASS_BY_ID = {
    **dict.fromkeys(
        {
            "BMB16-GYM-IK-GM-001", "BMB16-GYM-IK-GM-003",
            "BMB16-GYM-IK-MG-002", "BMB16-GYM-IK-PP-002",
            "BMB16-GYM-PK-RK-004", "INF7-16-GYM-IK-ALG-003",
            "INF7-16-GYM-IK-DC-001", "INF7-16-GYM-IK-DC-004",
            "INF7-16-GYM-IK-DC-005", "INF7-16-GYM-IK-IGD-004",
            "INF7-16-GYM-IK-IGD-006", "INF7-16-GYM-PK-AB-002",
            "INF7-16-GYM-PK-AB-005", "INF7-16-GYM-PK-AB-006",
            "INF7-16-GYM-PK-KK-002", "INF7-16-GYM-PK-KK-006",
            "INF7-16-GYM-PK-MI-003", "INF7-16-GYM-PK-MI-005",
            "INF7-16-GYM-PK-SV-002", "INF7-16-GYM-PK-SV-003",
            "LH26-E-ALG-001", "LH26-E-ALG-007", "LH26-E-ALG-008",
            "LH26-E-ALG-009", "LH26-E-DA-004", "LH26-E-DA-005",
            "LH26-E-DA-006", "LH26-E-DA-008", "LH26-E-DA-009",
            "LH26-E-DA-010", "LH26-E-DA-012", "LH26-E-DP-004",
            "LH26-E-DP-006", "LH26-E-ID-009", "LH26-E-ID-020",
            "LH26-E-ID-021", "LH26-E-KS-002", "LH26-E-KS-014",
            "LH26-E-KS-015",
        },
        "module-detail",
    ),
    **dict.fromkeys(
        {
            "BMB16-GYM-IK-GM-002", "BMB16-GYM-IK-KK-002",
            "BMB16-GYM-IK-KK-003", "BMB16-GYM-PK-HK-003",
            "BMB16-GYM-PK-SK-003", "INF7-16-GYM-PK-SV-001",
            "LH26-E-DA-015", "LH26-E-DP-001", "LH26-E-KS-001",
        },
        "school-context",
    ),
    **dict.fromkeys(
        {
            "BMB16-GYM-IK-MG-001", "BMB16-GYM-IK-MG-003",
            "BMB16-GYM-PK-RK-001", "BMB16-GYM-PK-RK-002",
            "BMB16-GYM-PK-RK-003", "LH26-E-DP-003", "LH26-E-DP-013",
            "LH26-E-DP-014",
        },
        "private-local",
    ),
    **dict.fromkeys(
        {
            "LH26-E-PROG-001", "LH26-E-PROG-002",
            "LH26-E-PROG-003", "LH26-E-PROG-004",
        },
        "roadmap-level",
    ),
}

AUDITED_DECISIONS = {
    "BMB16-GYM-IK-GM-001": ("IUM-5-CORE-01", "module-detail", "covered"),
    "BMB16-GYM-IK-GM-002": ("IUM-5-CORE-01", "school-context", "covered"),
    "BMB16-GYM-IK-GM-003": (
        "IUM-5-CORE-01", "module-detail", "remain-partial"
    ),
    "BMB16-GYM-PK-SK-003": ("IUM-5-CORE-01", "school-context", "covered"),
    "LH26-E-DA-004": ("IUM-5-CORE-01", "module-detail", "covered"),
    "LH26-E-DP-001": ("IUM-5-CORE-01", "school-context", "covered"),
    "LH26-E-PROG-001": ("IUM-5-CORE-01", "roadmap-level", "remain-partial"),
    "LH26-E-PROG-002": ("IUM-5-CORE-05", "roadmap-level", "remain-partial"),
    "LH26-E-PROG-003": ("IUM-7-CORE-08", "roadmap-level", "remain-partial"),
    "LH26-E-PROG-004": ("IUM-7-CORE-08", "roadmap-level", "remain-partial"),
    "BMB16-GYM-IK-MG-001": ("IUM-5-CORE-07", "private-local", "covered"),
    "BMB16-GYM-IK-MG-002": ("IUM-5-CORE-07", "module-detail", "covered"),
    "BMB16-GYM-IK-MG-003": ("IUM-5-CORE-07", "private-local", "covered"),
    "BMB16-GYM-PK-RK-001": ("IUM-5-CORE-07", "private-local", "covered"),
    "BMB16-GYM-PK-RK-002": ("IUM-5-CORE-07", "private-local", "covered"),
    "BMB16-GYM-PK-RK-003": ("IUM-5-CORE-07", "private-local", "covered"),
    "LH26-E-DP-003": ("IUM-5-CORE-07", "private-local", "remain-partial"),
}


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
        "BMB16-GYM-IK-MG-001": {
            "text": (
                "die persönliche Motivation bezüglich des eigenen "
                "Medienverhaltens beschreiben und die eigene Nutzung ihrem "
                "Alter entsprechend bewerten"
            )
        },
        "BMB16-GYM-IK-MG-002": {
            "text": (
                "die positiven Aspekte der Mediennutzung, aber auch die "
                "Risiken und Gefahren des (übermäßigen) Mediengebrauchs "
                "erläutern, bewerten und präventive Maßnahmen benennen"
            )
        },
        "BMB16-GYM-IK-MG-003": {
            "text": (
                "die Wirkung von Medien an Beispielen untersuchen, ihre "
                "Empfindungen dazu äußern und erste Gesetzmäßigkeiten ableiten"
            )
        },
        "BMB16-GYM-PK-RK-001": {
            "text": (
                "anknüpfend an ihre eigenen Erfahrungen das Nutzungsverhalten "
                "beschreiben und vergleichen"
            )
        },
        "BMB16-GYM-PK-RK-002": {
            "text": (
                "den Einfluss der digitalen Medien auf ihre Lebenswelt "
                "darstellen und Wirklichkeit mit Medienwirklichkeit in "
                "Beziehung setzen"
            )
        },
        "BMB16-GYM-PK-RK-003": {
            "text": (
                "Auswirkungen der medialen Selbstdarstellung abschätzen und "
                "in Grundzügen bewerten"
            )
        },
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
                "CE-IUM-5-CORE-07-BMB16-GYM-IK-MG-001",
                "CE-IUM-5-CORE-07-BMB16-GYM-IK-MG-002",
                "CE-IUM-5-CORE-07-BMB16-GYM-IK-MG-003",
                "CE-IUM-5-CORE-07-BMB16-GYM-PK-RK-001",
                "CE-IUM-5-CORE-07-BMB16-GYM-PK-RK-002",
                "CE-IUM-5-CORE-07-BMB16-GYM-PK-RK-003",
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

    def test_rejects_private_local_visibility_for_module_detail(self):
        with self.assertRaisesRegex(IUM09ValidationError, "module-detail"):
            self.validate(evidence_contract(productVisibility="private-local"))

    def test_rejects_private_local_visibility_for_school_context(self):
        with self.assertRaisesRegex(IUM09ValidationError, "school-context"):
            self.validate(
                school_context_contract(productVisibility="private-local")
            )

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
                payload["modules"][0].pop("coverageEvidence", None)
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


class CoverageBaselineFingerprintTests(unittest.TestCase):
    def test_hashes_only_sorted_immutable_before_records(self):
        entries = [
            {
                "competencyId": "B",
                "requirementText": "B text",
                "before": {
                    "coverageStatus": "partial",
                    "semanticAudit": "documented-gap",
                    "evidenceModuleId": "IUM-5-CORE-02",
                    "reason": "B reason",
                },
                "decision": "remain-partial",
            },
            {
                "competencyId": "A",
                "requirementText": "A text",
                "before": {
                    "coverageStatus": "partial",
                    "semanticAudit": "documented-gap",
                    "evidenceModuleId": "IUM-5-CORE-01",
                    "reason": "A reason",
                },
                "decision": "covered",
            },
        ]

        self.assertEqual(
            coverage_baseline_fingerprint(entries),
            "51af7b42e2d84adf0a3b0cef4548e0f4adc2bd9f275f537f4fa3abc8c65be01c",
        )


class RemediationLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        cls.coverage_payload = json.loads(
            (root / "roadmap/coverage-plan.json").read_text(encoding="utf-8")
        )
        cls.ledger_payload = json.loads(
            (root / "roadmap/coverage-remediation.json").read_text(encoding="utf-8")
        )
        cls.curriculum_contracts = {
            entry["competencyId"]: {"text": entry["requirementText"]}
            for entry in cls.coverage_payload["entries"]
        }
        cls.coverage_entries = {
            entry["competencyId"]: entry
            for entry in cls.coverage_payload["entries"]
        }
        module_payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(encoding="utf-8")
        )
        cls.repository_evidence_contracts = validate_coverage_evidence(
            module_payload, cls.curriculum_contracts
        )

    def validate(self, payload, evidence_contracts=None):
        contracts = dict(self.repository_evidence_contracts)
        if evidence_contracts is not None:
            contracts.update(evidence_contracts)
        return validate_remediation_ledger(
            payload, self.curriculum_contracts, contracts
        )

    def test_repository_ledger_has_immutable_baseline_metadata(self):
        self.assertEqual(
            set(self.ledger_payload),
            {"schemaVersion", "status", "baseline", "entries"},
        )
        self.assertEqual(self.ledger_payload["schemaVersion"], 1)
        self.assertEqual(self.ledger_payload["status"], "working")
        self.assertEqual(
            self.ledger_payload["baseline"],
            {
                "coverageCommit": "69c9d4f5504a297289615b4169fc4a9ea6d9b253",
                "partialCount": 60,
                "recordFingerprintSha256": (
                    "b7602352c67f61cdf075a65df167e12f7283b8f62867386545fea758b6e08892"
                ),
            },
        )

    def test_repository_ledger_has_each_baseline_id_in_its_specified_class(self):
        actual = {
            entry["competencyId"]: entry["causeClass"]
            for entry in self.ledger_payload["entries"]
        }
        self.assertEqual(actual, EXPECTED_CAUSE_CLASS_BY_ID)
        self.assertEqual(len(self.ledger_payload["entries"]), 60)

    def test_repository_ledger_fingerprint_matches_approved_before_records(self):
        self.assertEqual(
            coverage_baseline_fingerprint(self.ledger_payload["entries"]),
            "b7602352c67f61cdf075a65df167e12f7283b8f62867386545fea758b6e08892",
        )

    def test_repository_ledger_preserves_before_records_and_matches_audits(self):
        for entry in self.ledger_payload["entries"]:
            with self.subTest(competency_id=entry["competencyId"]):
                source = self.coverage_entries[entry["competencyId"]]
                self.assertEqual(entry["requirementText"], source["requirementText"])
                audit = AUDITED_DECISIONS.get(entry["competencyId"])
                if audit is None:
                    expected_module = entry["before"]["evidenceModuleId"]
                    expected_cause = entry["causeClass"]
                    expected_decision = "remain-partial"
                    self.assertEqual(
                        entry["before"],
                        {
                            "coverageStatus": source["coverageStatus"],
                            "semanticAudit": source["semanticAudit"],
                            "evidenceModuleId": source["evidenceModuleId"],
                            "reason": source["reason"],
                        },
                    )
                else:
                    expected_module, expected_cause, expected_decision = audit
                self.assertEqual(
                    entry["before"]["evidenceModuleId"], expected_module
                )
                self.assertEqual(entry["causeClass"], expected_cause)
                self.assertEqual(entry["decision"], expected_decision)
                if expected_decision == "covered":
                    self.assertIsNotNone(entry["evidenceContractId"])
                    self.assertEqual(
                        entry["after"],
                        {
                            "coverageStatus": "covered",
                            "semanticAudit": "operator-product-match",
                        },
                    )
                    self.assertIsNone(entry["residualGap"])
                else:
                    self.assertIsNone(entry["evidenceContractId"])
                    self.assertEqual(
                        entry["after"],
                        {
                            "coverageStatus": "partial",
                            "semanticAudit": "documented-gap",
                        },
                    )
                    self.assertEqual(
                        entry["residualGap"],
                        {
                            "reason": source["reason"],
                            "risk": source["risk"],
                            "followUp": source["followUp"],
                        },
                    )
                expected_graph = (
                    "review-required"
                    if entry["competencyId"] == "BMB16-GYM-IK-GM-003"
                    else "none"
                )
                self.assertEqual(entry["graphImpact"]["level"], expected_graph)
                expected_time = (
                    "roadmap-dependent"
                    if entry["causeClass"] == "roadmap-level"
                    else "review-required"
                )
                self.assertEqual(entry["timeImpact"]["level"], expected_time)

    def test_validator_accepts_repository_baseline_ledger(self):
        entries = self.validate(self.ledger_payload)
        self.assertEqual(set(entries), set(EXPECTED_CAUSE_CLASS_BY_ID))

    def test_validator_rejects_changed_baseline_requirement_text(self):
        payload = copy.deepcopy(self.ledger_payload)
        payload["entries"][0]["requirementText"] = "Unzulässige Änderung."
        with self.assertRaisesRegex(IUM09ValidationError, "fingerprint"):
            self.validate(payload)

    def test_validator_rejects_incomplete_residual_gap(self):
        payload = copy.deepcopy(self.ledger_payload)
        entry = next(
            entry
            for entry in payload["entries"]
            if entry["decision"] == "remain-partial"
        )
        del entry["residualGap"]["followUp"]
        with self.assertRaisesRegex(IUM09ValidationError, "residualGap"):
            self.validate(payload)

    def test_validator_rejects_covered_contract_from_a_different_baseline_module(self):
        payload = copy.deepcopy(self.ledger_payload)
        entry = payload["entries"][0]
        contract_id = "CE-IUM-7-CORE-01-BMB16-GYM-IK-GM-001"
        entry.update(
            {
                "decision": "covered",
                "evidenceContractId": contract_id,
                "after": {
                    "coverageStatus": "covered",
                    "semanticAudit": "operator-product-match",
                },
                "residualGap": None,
            }
        )
        with self.assertRaisesRegex(IUM09ValidationError, "baseline module"):
            self.validate(
                payload,
                {contract_id: {"competencyId": entry["competencyId"]}},
            )

    def test_validator_rejects_roadmap_level_departures(self):
        index = next(
            index
            for index, entry in enumerate(self.ledger_payload["entries"])
            if entry["causeClass"] == "roadmap-level"
        )
        mutations = {
            "decision": (
                lambda entry: entry.update(
                    {
                        "decision": "covered",
                        "evidenceContractId": "CE-IUM-5-CORE-01-LH26-E-PROG-001",
                        "after": {
                            "coverageStatus": "covered",
                            "semanticAudit": "operator-product-match",
                        },
                        "residualGap": None,
                    }
                ),
                {"CE-IUM-5-CORE-01-LH26-E-PROG-001": {"competencyId": "LH26-E-PROG-001"}},
                "roadmap-level",
            ),
            "contract": (
                lambda entry: entry.__setitem__(
                    "evidenceContractId", "CE-IUM-5-CORE-01-LH26-E-PROG-001"
                ),
                {},
                "remain-partial",
            ),
            "time": (
                lambda entry: entry["timeImpact"].__setitem__(
                    "level", "review-required"
                ),
                {},
                "roadmap-level",
            ),
            "graph": (
                lambda entry: entry["graphImpact"].__setitem__(
                    "level", "review-required"
                ),
                {},
                "roadmap-level",
            ),
        }
        for departure, (mutate, evidence_contracts, message) in mutations.items():
            with self.subTest(departure=departure):
                payload = copy.deepcopy(self.ledger_payload)
                mutate(payload["entries"][index])
                with self.assertRaisesRegex(IUM09ValidationError, message):
                    self.validate(payload, evidence_contracts)


class RemediatedCoverageTests(unittest.TestCase):
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
            (root / "roadmap/coverage-remediation.json").read_text(
                encoding="utf-8"
            )
        )
        cls.curriculum_contracts = {
            entry["competencyId"]: {"text": entry["requirementText"]}
            for entry in cls.coverage_payload["entries"]
        }
        cls.repository_evidence_contracts = validate_coverage_evidence(
            cls.module_payload, cls.curriculum_contracts
        )

    def validated_ledger_entries(self):
        return validate_remediation_ledger(
            self.remediation_payload,
            self.curriculum_contracts,
            self.repository_evidence_contracts,
        )

    def covered_chain_payloads(self):
        module_payload = copy.deepcopy(self.module_payload)
        contract = evidence_contract()
        evidence = module_payload["modules"][0]["coverageEvidence"]
        evidence[:] = [
            contract
            if item["competencyId"] == contract["competencyId"]
            else item
            for item in evidence
        ]
        coverage_payload = copy.deepcopy(self.coverage_payload)
        coverage_entry = next(
            entry
            for entry in coverage_payload["entries"]
            if entry["competencyId"] == contract["competencyId"]
        )
        coverage_entry.update(
            {
                "coverageStatus": "covered",
                "semanticAudit": "operator-product-match",
                "evidenceContractId": contract["id"],
            }
        )
        for field in ("requirementText", "learningAction", "productEvidence"):
            value = (
                coverage_entry["requirementText"]
                if field == "requirementText"
                else contract[field]
            )
            coverage_entry["evidence"] += f" {value}"
            coverage_entry["matchRationale"] += f" {value}"
        remediation_payload = copy.deepcopy(self.remediation_payload)
        remediation_entry = next(
            entry
            for entry in remediation_payload["entries"]
            if entry["competencyId"] == contract["competencyId"]
        )
        remediation_entry.update(
            {
                "decision": "covered",
                "evidenceContractId": contract["id"],
                "after": {
                    "coverageStatus": "covered",
                    "semanticAudit": "operator-product-match",
                },
                "residualGap": None,
            }
        )
        return module_payload, coverage_payload, remediation_payload, contract

    def test_accepts_repository_remediation_chain(self):
        result = validate_remediated_coverage(
            self.coverage_payload,
            self.validated_ledger_entries(),
            self.repository_evidence_contracts,
            self.curriculum_contracts,
        )
        self.assertEqual(
            result,
            {entry["competencyId"] for entry in self.coverage_payload["entries"]},
        )

    def test_rejects_each_nonempty_residual_gap_mutation(self):
        for field in ("reason", "risk", "followUp"):
            with self.subTest(field=field):
                coverage_payload = copy.deepcopy(self.coverage_payload)
                partial_entry = next(
                    entry
                    for entry in coverage_payload["entries"]
                    if entry["coverageStatus"] == "partial"
                )
                partial_entry[field] += " Abweichung."
                with self.assertRaisesRegex(IUM09ValidationError, "residual"):
                    validate_remediated_coverage(
                        coverage_payload,
                        self.validated_ledger_entries(),
                        self.repository_evidence_contracts,
                        self.curriculum_contracts,
                    )

    def test_rejects_status_change_without_matching_ledger_decision(self):
        coverage_payload = copy.deepcopy(self.coverage_payload)
        partial_entry = next(
            entry
            for entry in coverage_payload["entries"]
            if entry["coverageStatus"] == "partial"
        )
        partial_entry.update(
            {
                "coverageStatus": "covered",
                "semanticAudit": "operator-product-match",
                "evidenceContractId": (
                    f"CE-{partial_entry['evidenceModuleId']}-"
                    f"{partial_entry['competencyId']}"
                ),
            }
        )
        with self.assertRaisesRegex(IUM09ValidationError, "coverage status"):
            validate_remediated_coverage(
                coverage_payload,
                self.validated_ledger_entries(),
                self.repository_evidence_contracts,
                self.curriculum_contracts,
            )

    def test_rejects_evidence_contract_id_on_legacy_covered_record(self):
        coverage_payload = copy.deepcopy(self.coverage_payload)
        legacy_covered = next(
            entry
            for entry in coverage_payload["entries"]
            if entry["competencyId"] not in EXPECTED_CAUSE_CLASS_BY_ID
        )
        legacy_covered["evidenceContractId"] = "CE-legacy-record"
        with self.assertRaisesRegex(IUM09ValidationError, "legacy covered"):
            validate_remediated_coverage(
                coverage_payload,
                self.validated_ledger_entries(),
                self.repository_evidence_contracts,
                self.curriculum_contracts,
            )

    def test_rejects_coverage_chain_truncated_to_baseline_partial_ids(self):
        coverage_payload = copy.deepcopy(self.coverage_payload)
        coverage_payload["entries"] = [
            entry
            for entry in coverage_payload["entries"]
            if entry["competencyId"] in BASELINE_PARTIAL_IDS
        ]
        curriculum_contracts = {
            competency_id: self.curriculum_contracts[competency_id]
            for competency_id in BASELINE_PARTIAL_IDS
        }
        with self.assertRaisesRegex(IUM09ValidationError, "exactly 171"):
            validate_remediated_coverage(
                coverage_payload,
                self.validated_ledger_entries(),
                self.repository_evidence_contracts,
                curriculum_contracts,
            )

    def test_rejects_remediation_mapping_with_legacy_covered_record(self):
        remediation_entries = dict(self.validated_ledger_entries())
        coverage_payload = copy.deepcopy(self.coverage_payload)
        legacy_covered = next(
            entry
            for entry in coverage_payload["entries"]
            if entry["competencyId"] not in BASELINE_PARTIAL_IDS
        )
        legacy_covered.update(
            {
                "coverageStatus": "partial",
                "semanticAudit": "documented-gap",
                "reason": "Unzulässige zusätzliche Restrisikoentscheidung.",
            }
        )
        remediation_entries[legacy_covered["competencyId"]] = {
            "competencyId": legacy_covered["competencyId"],
            "requirementText": legacy_covered["requirementText"],
            "decision": "remain-partial",
            "evidenceContractId": None,
            "after": {
                "coverageStatus": "partial",
                "semanticAudit": "documented-gap",
            },
            "residualGap": {
                "reason": legacy_covered["reason"],
                "risk": legacy_covered["risk"],
                "followUp": legacy_covered["followUp"],
            },
        }
        with self.assertRaisesRegex(IUM09ValidationError, "baseline partial ids"):
            validate_remediated_coverage(
                coverage_payload,
                remediation_entries,
                self.repository_evidence_contracts,
                self.curriculum_contracts,
            )

    def test_covered_record_requires_every_contract_text_in_evidence_and_rationale(self):
        for container in ("evidence", "matchRationale"):
            for field in ("requirementText", "learningAction", "productEvidence"):
                with self.subTest(container=container, field=field):
                    module_payload, coverage_payload, remediation_payload, contract = (
                        self.covered_chain_payloads()
                    )
                    coverage_entry = next(
                        entry
                        for entry in coverage_payload["entries"]
                        if entry["competencyId"] == contract["competencyId"]
                    )
                    value = (
                        coverage_entry["requirementText"]
                        if field == "requirementText"
                        else contract[field]
                    )
                    coverage_entry[container] = coverage_entry[container].replace(
                        value,
                        "",
                    )
                    evidence_contracts = validate_coverage_evidence(
                        module_payload,
                        self.curriculum_contracts,
                    )
                    remediation_entries = validate_remediation_ledger(
                        remediation_payload,
                        self.curriculum_contracts,
                        evidence_contracts,
                    )
                    message = "evidence" if container == "evidence" else "rationale"
                    with self.assertRaisesRegex(IUM09ValidationError, message):
                        validate_remediated_coverage(
                            coverage_payload,
                            remediation_entries,
                            evidence_contracts,
                            self.curriculum_contracts,
                        )

    def test_rejects_evidence_contract_without_a_covered_ledger_decision(self):
        evidence_contracts = dict(self.repository_evidence_contracts)
        evidence_contracts["CE-orphan"] = {
            "competencyId": "BMB16-GYM-IK-GM-001"
        }
        with self.assertRaisesRegex(IUM09ValidationError, "referenced"):
            validate_remediated_coverage(
                self.coverage_payload,
                self.validated_ledger_entries(),
                evidence_contracts,
                self.curriculum_contracts,
            )

    def test_orchestrator_rejects_module_structure_mutation(self):
        module_payload = copy.deepcopy(self.module_payload)
        module_payload["modules"][0]["grade"] = 6
        with self.assertRaisesRegex(IUM09ValidationError, "module structure fingerprint"):
            validate_ium09(
                module_payload,
                self.coverage_payload,
                self.remediation_payload,
                self.curriculum_contracts,
            )


if __name__ == "__main__":
    unittest.main()
