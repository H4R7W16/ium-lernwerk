import copy
import json
import unittest
from pathlib import Path

import scripts.validate_ium10 as ium10_validator
from scripts.validate_ium10 import (
    BASELINE_COVERAGE_PROJECTION_SHA256,
    BASELINE_MODULE_STRUCTURE_SHA256,
    BASELINE_TIME_HANDOFF_SHA256,
    IUM10_BASELINE_COMMIT,
    IUM10ValidationError,
    coverage_projection_fingerprint,
    time_handoff_fingerprint,
    validate_annual_variants,
    validate_capacity_model,
    validate_integration_contracts,
    validate_module_contracts,
    validate_time_model_draft,
    validate_ium10_baseline,
)


EXPECTED_GRADE_5_UNITS = {
    "IUM-5-CORE-01": {"baseline": 5, "regular": 6, "extended": 6},
    "IUM-5-CORE-02": {"baseline": 4, "regular": 5, "extended": 5},
    "IUM-5-CORE-03": {"baseline": 4, "regular": 5, "extended": 5},
    "IUM-5-CORE-04": {"baseline": 3, "regular": 3, "extended": 3},
    "IUM-5-CORE-05": {"baseline": 5, "regular": 5, "extended": 6},
    "IUM-5-CORE-06": {"baseline": 5, "regular": 5, "extended": 7},
    "IUM-5-CORE-07": {"baseline": 4, "regular": 5, "extended": 6},
}


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


class IUM10CapacityModelTests(unittest.TestCase):
    @staticmethod
    def unit_contract():
        return {"label": "Unterrichtseinheit", "minutes": 45}

    @staticmethod
    def capacity_model():
        return {
            "officialWeeklyUnits": 1,
            "officialStatus": "administrative-context",
            "calendarEstimate": {
                "schoolYear": "2026/2027",
                "status": "dated-project-calculation",
                "weekdayUnits": {
                    "monday": 40,
                    "tuesday": 40,
                    "wednesday": 39,
                    "thursday": 36,
                    "friday": 37,
                },
            },
            "capacityLevels": [
                "calendar-capacity",
                "local-capacity",
                "planning-capacity",
            ],
            "planningPaths": [
                {"id": "baseline", "units": 30, "status": "working"},
                {"id": "regular", "units": 34, "status": "working"},
                {"id": "extended", "units": 38, "status": "working"},
            ],
            "bufferRule": {
                "formula": "localCapacityUnits - selectedPathUnits",
                "minimumBufferUnits": 0,
                "protectedLearningFunctions": [
                    "activation",
                    "concept-building",
                    "guided-practice",
                    "independent-action",
                    "product-evidence",
                    "feedback-or-self-check",
                    "revision",
                    "consolidation",
                    "transfer-or-retrieval",
                ],
            },
            "status": "working",
        }

    def validate_capacity(self, capacity_model=None, unit_contract=None):
        return validate_capacity_model(
            self.capacity_model() if capacity_model is None else capacity_model,
            self.unit_contract() if unit_contract is None else unit_contract,
        )

    def test_returns_the_three_working_paths_for_the_45_minute_unit_and_dated_calendar(self):
        result = self.validate_capacity()

        self.assertEqual(
            result,
            {
                "baseline": {"id": "baseline", "units": 30, "status": "working"},
                "regular": {"id": "regular", "units": 34, "status": "working"},
                "extended": {"id": "extended", "units": 38, "status": "working"},
            },
        )

    def test_rejects_the_30_plus_6_heuristic_as_an_official_norm(self):
        capacity_model = self.capacity_model()
        capacity_model["officialStatus"] = "30+6 official norm"

        with self.assertRaisesRegex(IUM10ValidationError, "30\\+6"):
            self.validate_capacity(capacity_model=capacity_model)

    def test_rejects_a_negative_local_buffer(self):
        capacity_model = self.capacity_model()
        capacity_model["bufferRule"]["minimumBufferUnits"] = -1

        with self.assertRaisesRegex(IUM10ValidationError, "buffer"):
            self.validate_capacity(capacity_model=capacity_model)

    def test_rejects_a_missing_capacity_level(self):
        capacity_model = self.capacity_model()
        capacity_model["capacityLevels"].remove("local-capacity")

        with self.assertRaisesRegex(IUM10ValidationError, "capacity levels"):
            self.validate_capacity(capacity_model=capacity_model)

    def test_rejects_a_baseline_without_all_protected_learning_functions(self):
        capacity_model = self.capacity_model()
        capacity_model["bufferRule"]["protectedLearningFunctions"].remove("revision")

        with self.assertRaisesRegex(IUM10ValidationError, "protected learning functions"):
            self.validate_capacity(capacity_model=capacity_model)

    def test_rejects_boolean_values_where_integer_contract_values_are_required(self):
        mutations = (
            ("unit minutes", self.unit_contract(), ("minutes",), True),
            ("official units", self.capacity_model(), ("officialWeeklyUnits",), True),
            (
                "calendar weekday units",
                self.capacity_model(),
                ("calendarEstimate", "weekdayUnits", "monday"),
                True,
            ),
            ("path units", self.capacity_model(), ("planningPaths", 0, "units"), True),
            (
                "minimum buffer units",
                self.capacity_model(),
                ("bufferRule", "minimumBufferUnits"),
                True,
            ),
        )
        for label, payload, path, value in mutations:
            with self.subTest(label=label):
                target = payload
                for key in path[:-1]:
                    target = target[key]
                target[path[-1]] = value

                if label == "unit minutes":
                    with self.assertRaises(IUM10ValidationError):
                        self.validate_capacity(unit_contract=payload)
                else:
                    with self.assertRaises(IUM10ValidationError):
                        self.validate_capacity(capacity_model=payload)

    def test_rejects_boolean_schema_version_in_the_repository_draft(self):
        root = Path(__file__).resolve().parents[1]
        time_model = json.loads(
            (root / "roadmap/time-model.json").read_text(encoding="utf-8")
        )
        time_model["schemaVersion"] = True

        with self.assertRaisesRegex(IUM10ValidationError, "schema version"):
            validate_time_model_draft(time_model)

    def test_repository_draft_has_the_capacity_contract_and_only_later_task_lists_empty(self):
        root = Path(__file__).resolve().parents[1]
        time_model = json.loads(
            (root / "roadmap/time-model.json").read_text(encoding="utf-8")
        )

        validate_time_model_draft(time_model)

        self.assertEqual(
            set(time_model),
            {
                "schemaVersion",
                "status",
                "baseline",
                "unit",
                "capacityModel",
                "moduleContracts",
                "integrationContracts",
                "annualVariants",
                "timeReviews",
                "sequenceEvidence",
                "gradeJudgements",
                "risks",
                "pilotAssignments",
            },
        )
        self.assertEqual(time_model["schemaVersion"], 1)
        self.assertEqual(time_model["status"], "draft")
        self.assertEqual(
            time_model["baseline"],
            {
                "commit": IUM10_BASELINE_COMMIT,
                "moduleStructureSha256": BASELINE_MODULE_STRUCTURE_SHA256,
                "coverageProjectionSha256": BASELINE_COVERAGE_PROJECTION_SHA256,
                "timeHandoffSha256": BASELINE_TIME_HANDOFF_SHA256,
            },
        )
        self.assertEqual(time_model["timeReviews"], [])
        self.assertEqual(time_model["sequenceEvidence"], [])
        self.assertEqual(time_model["risks"], [])
        self.assertEqual(time_model["pilotAssignments"], [])
        self.assertEqual(
            validate_capacity_model(time_model["capacityModel"], time_model["unit"]),
            {
                "baseline": {"id": "baseline", "units": 30, "status": "working"},
                "regular": {"id": "regular", "units": 34, "status": "working"},
                "extended": {"id": "extended", "units": 38, "status": "working"},
            },
        )


class IUM10ModuleContractTests(unittest.TestCase):
    @staticmethod
    def module_payload():
        return {
            "modules": [
                {
                    "id": "IUM-5-CORE-01",
                    "grade": 5,
                    "kind": "core",
                    "lessonRange": {"min": 5, "max": 7},
                    "competencyIds": ["COMP-CORE-01"],
                    "centralLearningAction": "Ein Modell fachlich anwenden.",
                    "centralLearningProduct": "Ein überprüfbares Modellprodukt.",
                    "prerequisiteModuleIds": [],
                    "moduleGrammar": [
                        "orientation-challenge",
                        "activate-prior-knowledge",
                        "build-concept",
                        "guided-practice",
                        "independent-action-product",
                        "review-revise-transfer",
                        "shared-consolidation",
                    ],
                },
                {
                    "id": "IUM-6-EXT-01",
                    "grade": 6,
                    "kind": "extension",
                    "lessonRange": {"min": 3, "max": 4},
                    "competencyIds": ["COMP-EXT-01"],
                    "centralLearningAction": "Eine Behauptung mit Belegen prüfen.",
                    "centralLearningProduct": "Eine begründete Prüfmatrix.",
                    "prerequisiteModuleIds": ["IUM-5-CORE-01"],
                    "moduleGrammar": [
                        "orientation-challenge",
                        "activate-prior-knowledge",
                        "guided-practice",
                        "independent-action-product",
                        "review-revise-transfer",
                        "shared-consolidation",
                    ],
                },
            ]
        }

    @staticmethod
    def phase_budgets(phase_ids):
        return [
            {
                "phaseId": phase_id,
                "minutes": 45,
                "learningFunction": f"{phase_id} fachlich durchführen.",
            }
            for phase_id in phase_ids
        ]

    @classmethod
    def core_contract(cls):
        phase_budgets = cls.phase_budgets(cls.module_payload()["modules"][0]["moduleGrammar"])
        minutes = sum(phase["minutes"] for phase in phase_budgets)
        return {
            "id": "TC-IUM-5-CORE-01",
            "moduleId": "IUM-5-CORE-01",
            "grade": 5,
            "kind": "core",
            "historicalLessonRange": {"min": 5, "max": 7},
            "competencyIds": ["COMP-CORE-01"],
            "centralLearningAction": "Ein Modell fachlich anwenden.",
            "centralLearningProduct": "Ein überprüfbares Modellprodukt.",
            "prerequisiteModuleIds": [],
            "revisitModuleIds": [],
            "pathBudgets": [
                {
                    "pathId": path_id,
                    "units": 7,
                    "minutes": minutes,
                    "directMinutes": minutes,
                    "countedSharedMinutes": 0,
                    "phaseBudgets": copy.deepcopy(phase_budgets),
                    "sharedAllocations": [],
                }
                for path_id in ("baseline", "regular", "extended")
            ],
            "standaloneUnitRange": None,
            "timeReviewIds": [],
            "integrationContractIds": [],
            "schoolDependentSteps": [],
            "risk": "Die verfügbare Schulzeit muss im Pilot geprüft werden.",
            "pilotRequired": True,
            "status": "working",
        }

    @classmethod
    def flexible_contract(cls):
        phase_budgets = cls.phase_budgets(cls.module_payload()["modules"][1]["moduleGrammar"])
        minutes = sum(phase["minutes"] for phase in phase_budgets)
        return {
            "id": "TC-IUM-6-EXT-01",
            "moduleId": "IUM-6-EXT-01",
            "grade": 6,
            "kind": "extension",
            "historicalLessonRange": {"min": 3, "max": 4},
            "competencyIds": ["COMP-EXT-01"],
            "centralLearningAction": "Eine Behauptung mit Belegen prüfen.",
            "centralLearningProduct": "Eine begründete Prüfmatrix.",
            "prerequisiteModuleIds": ["IUM-5-CORE-01"],
            "revisitModuleIds": ["IUM-5-CORE-01"],
            "pathBudgets": [
                {
                    "pathId": "standalone",
                    "units": 6,
                    "minutes": minutes,
                    "directMinutes": minutes,
                    "countedSharedMinutes": 0,
                    "phaseBudgets": phase_budgets,
                    "sharedAllocations": [],
                }
            ],
            "standaloneUnitRange": {"min": 3, "recommended": 4, "max": 6},
            "timeReviewIds": [],
            "integrationContractIds": [],
            "schoolDependentSteps": [],
            "risk": "Die zusätzliche Zeit wird nur bei lokaler Kapazität eingesetzt.",
            "pilotRequired": True,
            "status": "working",
        }

    @staticmethod
    def grade_six_core_04_module():
        return {
            "id": "IUM-6-CORE-04",
            "grade": 6,
            "kind": "core",
            "lessonRange": {"min": 5, "max": 7},
            "competencyIds": ["COMP-CORE-04"],
            "centralLearningAction": "Ein Programm schrittweise ausführen.",
            "centralLearningProduct": "Ein getestetes Programmprodukt.",
            "prerequisiteModuleIds": ["IUM-5-CORE-01"],
            "moduleGrammar": [
                "orientation-challenge",
                "activate-prior-knowledge",
                "build-concept",
                "guided-practice",
                "independent-action-product",
                "review-revise-transfer",
                "shared-consolidation",
            ],
        }

    @classmethod
    def grade_six_core_04_contract(cls, include_targeted_extension=False):
        contract = cls.core_contract()
        module = cls.grade_six_core_04_module()
        contract.update(
            {
                "id": "TC-IUM-6-CORE-04",
                "moduleId": module["id"],
                "grade": module["grade"],
                "kind": module["kind"],
                "historicalLessonRange": copy.deepcopy(module["lessonRange"]),
                "competencyIds": list(module["competencyIds"]),
                "centralLearningAction": module["centralLearningAction"],
                "centralLearningProduct": module["centralLearningProduct"],
                "prerequisiteModuleIds": list(module["prerequisiteModuleIds"]),
                "pathBudgets": contract["pathBudgets"][:2],
            }
        )
        if include_targeted_extension:
            targeted_extension = copy.deepcopy(contract["pathBudgets"][0])
            targeted_extension["pathId"] = "targeted-extension"
            contract["pathBudgets"].append(targeted_extension)
        return contract

    def contracts(self):
        return [self.core_contract(), self.flexible_contract()]

    def validate_contracts(self, contracts=None, module_payload=None):
        return validate_module_contracts(
            self.contracts() if contracts is None else contracts,
            self.module_payload() if module_payload is None else module_payload,
        )

    def test_returns_contracts_keyed_by_their_existing_module_ids(self):
        result = self.validate_contracts()

        self.assertEqual(set(result), {"IUM-5-CORE-01", "IUM-6-EXT-01"})
        self.assertEqual(result["IUM-5-CORE-01"]["id"], "TC-IUM-5-CORE-01")
        self.assertEqual(result["IUM-6-EXT-01"]["pathBudgets"][0]["pathId"], "standalone")

    def test_accepts_grade_six_core_04_with_standard_paths(self):
        contract = self.grade_six_core_04_contract()
        result = validate_module_contracts(
            [contract],
            {"modules": [self.grade_six_core_04_module()]},
        )

        self.assertEqual(result, {"IUM-6-CORE-04": contract})

    def test_accepts_grade_six_core_04_with_optional_targeted_extension(self):
        contract = self.grade_six_core_04_contract(include_targeted_extension=True)
        result = validate_module_contracts(
            [contract],
            {"modules": [self.grade_six_core_04_module()]},
        )

        self.assertEqual(
            {budget["pathId"] for budget in result["IUM-6-CORE-04"]["pathBudgets"]},
            {"baseline", "regular", "targeted-extension"},
        )

    def test_rejects_unknown_duplicate_or_malformed_contract_identity(self):
        mutations = (
            ("unknown module", "moduleId", "IUM-5-CORE-99"),
            ("wrong contract id", "id", "TC-IUM-5-CORE-99"),
        )
        for label, field, value in mutations:
            with self.subTest(label=label):
                contracts = self.contracts()
                contracts[0][field] = value
                with self.assertRaises(IUM10ValidationError):
                    self.validate_contracts(contracts=contracts)

        contracts = self.contracts()
        duplicate = copy.deepcopy(contracts[0])
        duplicate["moduleId"] = "IUM-6-EXT-01"
        duplicate["id"] = "TC-IUM-6-EXT-01"
        contracts.append(duplicate)
        with self.assertRaises(IUM10ValidationError):
            self.validate_contracts(contracts=contracts)

    def test_rejects_contract_metadata_that_diverges_from_its_module(self):
        mutations = (
            ("grade", 6),
            ("kind", "extension"),
            ("historicalLessonRange", {"min": 2, "max": 7}),
            ("competencyIds", ["COMP-OTHER"]),
            ("prerequisiteModuleIds", ["IUM-6-EXT-01"]),
            ("centralLearningAction", "Eine andere Lernhandlung."),
            ("centralLearningProduct", "Ein anderes Lernprodukt."),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                contracts = self.contracts()
                contracts[0][field] = value
                with self.assertRaises(IUM10ValidationError):
                    self.validate_contracts(contracts=contracts)

    def test_rejects_inconsistent_path_arithmetic(self):
        mutations = (
            ("unit minutes", "minutes", 314),
            ("phase total", "phaseBudgets.0.minutes", 44),
            ("direct and shared total", "directMinutes", 314),
        )
        for label, field, value in mutations:
            with self.subTest(label=label):
                contracts = self.contracts()
                budget = contracts[0]["pathBudgets"][0]
                target, _, key = field.rpartition(".")
                if target:
                    container, index = target.split(".")
                    budget[container][int(index)][key] = value
                else:
                    budget[key] = value
                with self.assertRaises(IUM10ValidationError):
                    self.validate_contracts(contracts=contracts)

        contracts = self.contracts()
        budget = contracts[0]["pathBudgets"][0]
        budget["directMinutes"] = 270
        budget["countedSharedMinutes"] = 45
        with self.assertRaises(IUM10ValidationError):
            self.validate_contracts(contracts=contracts)

    def test_rejects_missing_zero_or_unpermitted_phase_budgets(self):
        mutations = (
            ("missing core phase", "core", "phaseBudgets", lambda phases: phases[:-1]),
            ("zero core phase", "core", "phaseBudgets.0.minutes", 0),
            ("unpermitted flexible phase", "flexible", "phaseBudgets.0.phaseId", "build-concept"),
        )
        for label, contract_kind, field, value in mutations:
            with self.subTest(label=label):
                contracts = self.contracts()
                contract = contracts[0] if contract_kind == "core" else contracts[1]
                target, _, key = field.rpartition(".")
                if target == "":
                    budget = contract["pathBudgets"][0]
                    budget[key] = value(budget[key])
                else:
                    container, index = target.split(".")
                    contract["pathBudgets"][0][container][int(index)][key] = value
                with self.assertRaises(IUM10ValidationError):
                    self.validate_contracts(contracts=contracts)

    def test_rejects_missing_learning_function_non_core_paths_or_missing_pilot(self):
        mutations = (
            ("missing learning function", "learningFunction", ""),
            ("flexible core coverage", "pathId", "baseline"),
        )
        for label, field, value in mutations:
            with self.subTest(label=label):
                contracts = self.contracts()
                if field == "learningFunction":
                    contracts[0]["pathBudgets"][0]["phaseBudgets"][0][field] = value
                else:
                    contracts[1]["pathBudgets"][0][field] = value
                with self.assertRaises(IUM10ValidationError):
                    self.validate_contracts(contracts=contracts)

        contracts = self.contracts()
        contracts[0]["pilotRequired"] = False
        with self.assertRaises(IUM10ValidationError):
            self.validate_contracts(contracts=contracts)

    def test_rejects_boolean_values_in_integer_contract_fields(self):
        mutations = (
            ("standalone range minimum", "standaloneUnitRange.min", True),
            ("standalone range", "standaloneUnitRange.recommended", True),
            ("standalone range maximum", "standaloneUnitRange.max", True),
            ("path units", "pathBudgets.0.units", True),
            ("path minutes", "pathBudgets.0.minutes", True),
            ("direct minutes", "pathBudgets.0.directMinutes", True),
            ("shared minutes", "pathBudgets.0.countedSharedMinutes", True),
            ("phase minutes", "pathBudgets.0.phaseBudgets.0.minutes", True),
        )
        for label, field, value in mutations:
            with self.subTest(label=label):
                contracts = self.contracts()
                contract = contracts[1] if field.startswith("standalone") else contracts[0]
                current = contract
                for part in field.split(".")[:-1]:
                    current = current[int(part)] if part.isdigit() else current[part]
                current[field.split(".")[-1]] = value
                with self.assertRaises(IUM10ValidationError):
                    self.validate_contracts(contracts=contracts)

        contracts = self.contracts()
        budget = contracts[0]["pathBudgets"][0]
        budget["directMinutes"] = 270
        budget["countedSharedMinutes"] = 45
        budget["sharedAllocations"] = [
            {"integrationContractId": "INT-TEST", "minutes": True}
        ]
        with self.assertRaises(IUM10ValidationError):
            self.validate_contracts(contracts=contracts)

    def test_rejects_extra_path_time_without_more_practice_product_or_revision(self):
        contracts = self.contracts()
        regular = contracts[0]["pathBudgets"][1]
        regular["units"] += 1
        regular["minutes"] += 45
        regular["directMinutes"] += 45
        regular["phaseBudgets"][0]["minutes"] += 45

        with self.assertRaisesRegex(
            IUM10ValidationError,
            "practice, product, or revision",
        ):
            self.validate_contracts(contracts=contracts)

    def test_rejects_extended_focus_time_that_regresses_from_regular_path(self):
        contracts = self.contracts()
        regular = contracts[0]["pathBudgets"][1]
        regular["units"] = 8
        regular["minutes"] = 360
        regular["directMinutes"] = 360
        regular["phaseBudgets"][3]["minutes"] = 90

        extended = contracts[0]["pathBudgets"][2]
        extended["units"] = 9
        extended["minutes"] = 405
        extended["directMinutes"] = 405
        extended["phaseBudgets"][0]["minutes"] = 120
        extended["phaseBudgets"][3]["minutes"] = 60

        with self.assertRaisesRegex(
            IUM10ValidationError,
            "immediate predecessor",
        ):
            self.validate_contracts(contracts=contracts)

    def test_rejects_targeted_extension_focus_time_that_regresses_from_regular_path(self):
        contract = self.grade_six_core_04_contract(
            include_targeted_extension=True
        )
        regular = contract["pathBudgets"][1]
        regular["units"] = 8
        regular["minutes"] = 360
        regular["directMinutes"] = 360
        regular["phaseBudgets"][3]["minutes"] = 90

        targeted = contract["pathBudgets"][2]
        targeted["units"] = 9
        targeted["minutes"] = 405
        targeted["directMinutes"] = 405
        targeted["phaseBudgets"][0]["minutes"] = 120
        targeted["phaseBudgets"][3]["minutes"] = 60

        with self.assertRaisesRegex(
            IUM10ValidationError,
            "immediate predecessor",
        ):
            validate_module_contracts(
                [contract],
                {"modules": [self.grade_six_core_04_module()]},
            )


class IUM10IntegrationContractTests(unittest.TestCase):
    CONTRACT_ID = "INT-TEST-SHARED-EVIDENCE"

    @classmethod
    def module_contracts(cls):
        contracts = {}
        for module_id, counted in (("MODULE-A", False), ("MODULE-B", True)):
            path_budgets = []
            for path_id in ("baseline", "regular", "extended"):
                allocation = (
                    [{"integrationContractId": cls.CONTRACT_ID, "minutes": 45}]
                    if counted
                    else []
                )
                path_budgets.append(
                    {
                        "pathId": path_id,
                        "countedSharedMinutes": 45 if counted else 0,
                        "sharedAllocations": allocation,
                    }
                )
            contracts[module_id] = {
                "moduleId": module_id,
                "integrationContractIds": [cls.CONTRACT_ID],
                "pathBudgets": path_budgets,
            }
        return contracts

    @classmethod
    def integration_contract(cls):
        return {
            "id": cls.CONTRACT_ID,
            "moduleIds": ["MODULE-A", "MODULE-B"],
            "pathIds": ["baseline", "regular", "extended"],
            "sharedPhaseOrProduct": "Eine gemeinsame Quellen- und Belegspur.",
            "countedInModuleId": "MODULE-B",
            "sharedMinutes": 45,
            "savingsMinutesByPath": {
                "baseline": 45,
                "regular": 0,
                "extended": 0,
            },
            "preservedLearningActions": [
                "MODULE-A prüft Quellen.",
                "MODULE-B nutzt und belegt die Quellen.",
            ],
            "preservedProductAndCurriculumEvidence": [
                "Quellendossier und Produktquellenverzeichnis bleiben prüfbar.",
            ],
            "prerequisites": ["Die Produktspur nutzt dasselbe Rechercheergebnis."],
            "risk": "Getrennte Themen verhindern die gemeinsame Evidenzspur.",
            "fallback": "Beide Module erhalten eigenständige Recherche- und Produktionszeit.",
            "status": "working",
        }

    def validate_integrations(self, contracts=None, module_contracts=None):
        return validate_integration_contracts(
            [self.integration_contract()] if contracts is None else contracts,
            self.module_contracts() if module_contracts is None else module_contracts,
        )

    def test_returns_integration_contracts_keyed_by_unique_id(self):
        result = self.validate_integrations()

        self.assertEqual(result, {self.CONTRACT_ID: self.integration_contract()})

    def test_rejects_unknown_modules_paths_or_counted_module(self):
        mutations = (
            ("moduleIds", ["MODULE-A", "MODULE-MISSING"]),
            ("pathIds", ["baseline", "regular", "missing"]),
            ("countedInModuleId", "MODULE-MISSING"),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                contract = self.integration_contract()
                contract[field] = value
                with self.assertRaises(IUM10ValidationError):
                    self.validate_integrations(contracts=[contract])

    def test_rejects_missing_or_unexpected_fields_fail_closed(self):
        missing = self.integration_contract()
        missing.pop("countedInModuleId")
        unexpected = self.integration_contract()
        unexpected["note"] = "Nicht Teil des Vertrags."

        for contract in (missing, unexpected):
            with self.subTest(fields=set(contract)):
                with self.assertRaisesRegex(IUM10ValidationError, "fields"):
                    self.validate_integrations(contracts=[contract])

    def test_rejects_shared_minutes_counted_in_more_than_one_module(self):
        module_contracts = self.module_contracts()
        for budget in module_contracts["MODULE-A"]["pathBudgets"]:
            budget["countedSharedMinutes"] = 45
            budget["sharedAllocations"] = [
                {"integrationContractId": self.CONTRACT_ID, "minutes": 45}
            ]

        with self.assertRaisesRegex(IUM10ValidationError, "exactly once"):
            self.validate_integrations(module_contracts=module_contracts)

    def test_rejects_boolean_values_as_minutes(self):
        mutations = (
            ("sharedMinutes", True),
            ("savingsMinutesByPath.baseline", True),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                contract = self.integration_contract()
                current = contract
                parts = field.split(".")
                for part in parts[:-1]:
                    current = current[part]
                current[parts[-1]] = value
                with self.assertRaises(IUM10ValidationError):
                    self.validate_integrations(contracts=[contract])

        module_contracts = self.module_contracts()
        module_contracts["MODULE-B"]["pathBudgets"][0]["sharedAllocations"][0][
            "minutes"
        ] = True
        with self.assertRaises(IUM10ValidationError):
            self.validate_integrations(module_contracts=module_contracts)

    def test_rejects_unknown_module_integration_reference(self):
        module_contracts = self.module_contracts()
        module_contracts["MODULE-A"]["integrationContractIds"].append(
            "INT-UNKNOWN"
        )

        with self.assertRaisesRegex(IUM10ValidationError, "unknown integration reference"):
            self.validate_integrations(module_contracts=module_contracts)

    def test_rejects_unknown_shared_allocation_integration_id(self):
        module_contracts = self.module_contracts()
        budget = module_contracts["MODULE-A"]["pathBudgets"][0]
        budget["countedSharedMinutes"] = 45
        budget["sharedAllocations"].append(
            {"integrationContractId": "INT-UNKNOWN", "minutes": 45}
        )

        with self.assertRaisesRegex(IUM10ValidationError, "unknown shared allocation"):
            self.validate_integrations(module_contracts=module_contracts)


class IUM10AnnualVariantTests(unittest.TestCase):
    @staticmethod
    def module_contracts():
        return {
            "MODULE-A": {
                "moduleId": "MODULE-A",
                "grade": 5,
                "kind": "core",
                "pathBudgets": [
                    {"pathId": "baseline", "units": 2},
                    {"pathId": "regular", "units": 3},
                    {"pathId": "extended", "units": 3},
                ],
            },
            "MODULE-B": {
                "moduleId": "MODULE-B",
                "grade": 5,
                "kind": "core",
                "pathBudgets": [
                    {"pathId": "baseline", "units": 3},
                    {"pathId": "regular", "units": 3},
                    {"pathId": "extended", "units": 4},
                ],
            },
        }

    @staticmethod
    def annual_variant():
        return {
            "id": "GRADE-5-TEST",
            "grade": 5,
            "kind": "planning-path",
            "pathId": "baseline",
            "targetUnits": 5,
            "allocations": [
                {"moduleId": "MODULE-A", "budgetPathId": "baseline", "units": 2},
                {"moduleId": "MODULE-B", "budgetPathId": "baseline", "units": 3},
            ],
            "integrationContractIds": [],
            "available": True,
            "status": "working",
            "rationale": "Der Kernpfad passt rechnerisch in fünf Testeinheiten.",
            "risk": "Die Rechnung ist noch nicht pilotiert.",
        }

    def validate_variants(
        self,
        variants=None,
        module_contracts=None,
        integration_contracts=None,
    ):
        return validate_annual_variants(
            [self.annual_variant()] if variants is None else variants,
            self.module_contracts() if module_contracts is None else module_contracts,
            {} if integration_contracts is None else integration_contracts,
        )

    @staticmethod
    def integration_contract(status="working"):
        return {
            "id": "INT-TEST",
            "moduleIds": ["MODULE-A", "MODULE-B"],
            "pathIds": ["baseline"],
            "countedInModuleId": "MODULE-B",
            "status": status,
        }

    def integration_aware_inputs(self, *, integration_status="working"):
        module_contracts = self.module_contracts()
        module_contracts["MODULE-B"]["pathBudgets"][0]["sharedAllocations"] = [
            {"integrationContractId": "INT-TEST", "minutes": 45}
        ]
        integration = self.integration_contract(status=integration_status)
        return module_contracts, {"INT-TEST": integration}

    def override_variant(self):
        variant = self.annual_variant()
        variant.update(
            {
                "id": "GRADE-5-OVERRIDE-TEST",
                "pathId": "regular",
                "targetUnits": 6,
                "allocations": [
                    {
                        "moduleId": "MODULE-A",
                        "budgetPathId": "regular",
                        "units": 3,
                    },
                    {
                        "moduleId": "MODULE-B",
                        "budgetPathId": "baseline",
                        "units": 3,
                    },
                ],
                "integrationContractIds": ["INT-TEST"],
            }
        )
        return variant

    def validate_with_module_b_baseline_override(
        self,
        *,
        module_contracts,
        integration_contracts,
    ):
        variant = self.override_variant()
        overrides = ium10_validator.ANNUAL_VARIANT_BUDGET_PATH_OVERRIDES
        overrides[variant["id"]] = {"MODULE-B": "baseline"}
        try:
            return self.validate_variants(
                variants=[variant],
                module_contracts=module_contracts,
                integration_contracts=integration_contracts,
            )
        finally:
            del overrides[variant["id"]]

    def test_returns_annual_variants_keyed_by_unique_id(self):
        result = self.validate_variants()

        self.assertEqual(result, {"GRADE-5-TEST": self.annual_variant()})

    def test_rejects_unknown_modules_paths_allocation_units_or_target_sum(self):
        mutations = (
            ("allocations.0.moduleId", "MODULE-MISSING"),
            ("allocations.0.budgetPathId", "missing"),
            ("allocations.0.units", 3),
            ("targetUnits", 6),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                variant = self.annual_variant()
                current = variant
                for part in field.split(".")[:-1]:
                    current = current[int(part)] if part.isdigit() else current[part]
                current[field.split(".")[-1]] = value
                with self.assertRaises(IUM10ValidationError):
                    self.validate_variants(variants=[variant])

    def test_rejects_unknown_top_level_planning_path(self):
        variant = self.annual_variant()
        variant["pathId"] = "missing"

        with self.assertRaisesRegex(IUM10ValidationError, "planning path"):
            self.validate_variants(variants=[variant])

    def test_rejects_same_sized_foreign_budget_path_for_planning_variant(self):
        variant = self.annual_variant()
        variant["pathId"] = "regular"
        variant["targetUnits"] = 6
        variant["allocations"] = [
            {"moduleId": "MODULE-A", "budgetPathId": "extended", "units": 3},
            {"moduleId": "MODULE-B", "budgetPathId": "regular", "units": 3},
        ]

        with self.assertRaisesRegex(IUM10ValidationError, "variant path"):
            self.validate_variants(variants=[variant])

    def test_rejects_same_sized_optimized_budgets_for_robust_demand_scenario(self):
        module_contracts = {
            module_id: {
                "moduleId": module_id,
                "grade": 7,
                "kind": "core",
                "pathBudgets": [
                    {"pathId": "optimized", "units": units},
                    {"pathId": "robust", "units": units},
                ],
            }
            for module_id, units in (("MODULE-A", 2), ("MODULE-B", 3))
        }
        variant = {
            "id": "GRADE-7-ROBUST-TEST",
            "grade": 7,
            "kind": "demand-scenario",
            "pathId": "robust",
            "targetUnits": 5,
            "allocations": [
                {"moduleId": "MODULE-A", "budgetPathId": "optimized", "units": 2},
                {"moduleId": "MODULE-B", "budgetPathId": "optimized", "units": 3},
            ],
            "integrationContractIds": [],
            "available": False,
            "status": "working",
            "rationale": "Das robuste Testszenario weist fünf Einheiten aus.",
            "risk": "Das Testszenario ist kein verfügbarer Jahrespfad.",
        }

        with self.assertRaisesRegex(IUM10ValidationError, "variant path"):
            self.validate_variants(
                variants=[variant],
                module_contracts=module_contracts,
            )

    def test_rejects_missing_or_unexpected_fields_fail_closed(self):
        missing = self.annual_variant()
        missing.pop("available")
        unexpected = self.annual_variant()
        unexpected["note"] = "Nicht Teil des Vertrags."

        for variant in (missing, unexpected):
            with self.subTest(fields=set(variant)):
                with self.assertRaisesRegex(IUM10ValidationError, "fields"):
                    self.validate_variants(variants=[variant])

    def test_rejects_boolean_values_as_units_or_availability(self):
        mutations = (
            ("targetUnits", True),
            ("allocations.0.units", True),
            ("available", 1),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                variant = self.annual_variant()
                current = variant
                for part in field.split(".")[:-1]:
                    current = current[int(part)] if part.isdigit() else current[part]
                current[field.split(".")[-1]] = value
                with self.assertRaises(IUM10ValidationError):
                    self.validate_variants(variants=[variant])

    def test_rejects_omitted_integration_used_by_selected_budget(self):
        module_contracts, integrations = self.integration_aware_inputs()
        variant = self.annual_variant()

        with self.assertRaisesRegex(IUM10ValidationError, "required integrations"):
            self.validate_variants(
                variants=[variant],
                module_contracts=module_contracts,
                integration_contracts=integrations,
            )

    def test_rejects_failed_integration_while_variant_remains_available(self):
        module_contracts, integrations = self.integration_aware_inputs(
            integration_status="failed"
        )
        variant = self.annual_variant()
        variant["integrationContractIds"] = ["INT-TEST"]

        with self.assertRaisesRegex(IUM10ValidationError, "failed integration"):
            self.validate_variants(
                variants=[variant],
                module_contracts=module_contracts,
                integration_contracts=integrations,
            )

    def test_rejects_declared_integration_not_used_by_selected_budgets(self):
        integration = self.integration_contract()
        variant = self.annual_variant()
        variant["integrationContractIds"] = ["INT-TEST"]

        with self.assertRaisesRegex(IUM10ValidationError, "required integrations"):
            self.validate_variants(
                variants=[variant],
                integration_contracts={"INT-TEST": integration},
            )

    def test_rejects_override_when_participant_path_is_unsupported_by_integration(self):
        module_contracts, integrations = self.integration_aware_inputs()

        with self.assertRaisesRegex(
            IUM10ValidationError,
            "participant budget path",
        ):
            self.validate_with_module_b_baseline_override(
                module_contracts=module_contracts,
                integration_contracts=integrations,
            )

    def test_accepts_override_when_all_participant_paths_support_integration(self):
        module_contracts, integrations = self.integration_aware_inputs()
        integrations["INT-TEST"]["pathIds"] = ["baseline", "regular"]

        result = self.validate_with_module_b_baseline_override(
            module_contracts=module_contracts,
            integration_contracts=integrations,
        )

        self.assertEqual(set(result), {"GRADE-5-OVERRIDE-TEST"})


class IUM10Grade5RepositoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        cls.time_model = json.loads(
            (root / "roadmap/time-model.json").read_text(encoding="utf-8")
        )
        module_payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(encoding="utf-8")
        )
        cls.grade_5_payload = {
            "modules": [
                module for module in module_payload["modules"] if module["grade"] == 5
            ]
        }

    def test_repository_has_seven_complete_grade_5_time_contracts(self):
        contracts = validate_module_contracts(
            self.time_model["moduleContracts"],
            self.grade_5_payload,
        )

        self.assertEqual(set(contracts), set(EXPECTED_GRADE_5_UNITS))
        for module_id, expected_paths in EXPECTED_GRADE_5_UNITS.items():
            with self.subTest(module_id=module_id):
                contract = contracts[module_id]
                budgets = {
                    budget["pathId"]: budget for budget in contract["pathBudgets"]
                }
                self.assertEqual(
                    {path_id: budget["units"] for path_id, budget in budgets.items()},
                    expected_paths,
                )
                for budget in budgets.values():
                    phases = {
                        phase["phaseId"]: phase for phase in budget["phaseBudgets"]
                    }
                    self.assertEqual(len(phases), 7)
                    self.assertTrue(
                        phases["orientation-challenge"]["learningFunction"].endswith(
                            contract["centralLearningAction"]
                        )
                    )
                    self.assertTrue(
                        phases["independent-action-product"]["learningFunction"].endswith(
                            contract["centralLearningProduct"]
                        )
                    )

    def test_repository_integration_counts_shared_evidence_only_in_core_06(self):
        contracts = validate_module_contracts(
            self.time_model["moduleContracts"],
            self.grade_5_payload,
        )
        integrations = validate_integration_contracts(
            self.time_model["integrationContracts"],
            contracts,
        )

        self.assertEqual(set(integrations), {"INT-5-RESEARCH-PRODUCTION"})
        integration = integrations["INT-5-RESEARCH-PRODUCTION"]
        self.assertEqual(
            integration["moduleIds"],
            ["IUM-5-CORE-02", "IUM-5-CORE-06"],
        )
        self.assertEqual(integration["countedInModuleId"], "IUM-5-CORE-06")
        self.assertEqual(integration["sharedMinutes"], 45)
        self.assertEqual(
            integration["savingsMinutesByPath"],
            {"baseline": 45, "regular": 0, "extended": 0},
        )
        self.assertIn("Quellen", integration["sharedPhaseOrProduct"])
        self.assertIn("Beleg", integration["sharedPhaseOrProduct"])
        self.assertIn("eigenständig", integration["fallback"])
        self.assertEqual(
            {
                module_id: contract["integrationContractIds"]
                for module_id, contract in contracts.items()
            },
            {
                module_id: (
                    ["INT-5-RESEARCH-PRODUCTION"]
                    if module_id in {"IUM-5-CORE-02", "IUM-5-CORE-06"}
                    else []
                )
                for module_id in EXPECTED_GRADE_5_UNITS
            },
        )

    def test_repository_has_available_core_only_30_34_38_variants(self):
        contracts = validate_module_contracts(
            self.time_model["moduleContracts"],
            self.grade_5_payload,
        )
        integrations = validate_integration_contracts(
            self.time_model["integrationContracts"],
            contracts,
        )
        variants = validate_annual_variants(
            self.time_model["annualVariants"],
            contracts,
            integrations,
        )

        expected_variants = {
            "GRADE-5-BASELINE": ("baseline", 30),
            "GRADE-5-REGULAR": ("regular", 34),
            "GRADE-5-EXTENDED": ("extended", 38),
        }
        self.assertEqual(set(variants), set(expected_variants))
        for variant_id, (path_id, target_units) in expected_variants.items():
            with self.subTest(variant_id=variant_id):
                variant = variants[variant_id]
                self.assertEqual(variant["pathId"], path_id)
                self.assertEqual(variant["targetUnits"], target_units)
                self.assertIs(variant["available"], True)
                self.assertEqual(
                    variant["integrationContractIds"],
                    ["INT-5-RESEARCH-PRODUCTION"],
                )
                self.assertEqual(
                    {allocation["moduleId"] for allocation in variant["allocations"]},
                    set(EXPECTED_GRADE_5_UNITS),
                )
                self.assertTrue(
                    all(
                        contracts[allocation["moduleId"]]["kind"] == "core"
                        for allocation in variant["allocations"]
                    )
                )

    def test_repository_grade_5_judgement_separates_status_dimensions(self):
        judgements = [
            judgement
            for judgement in self.time_model["gradeJudgements"]
            if judgement["grade"] == 5
        ]

        self.assertEqual(len(judgements), 1)
        judgement = judgements[0]
        self.assertEqual(
            {
                "semanticCoverageStatus": judgement["semanticCoverageStatus"],
                "timeFeasibilityStatus": judgement["timeFeasibilityStatus"],
                "sequenceEvidenceStatus": judgement["sequenceEvidenceStatus"],
                "pilotStatus": judgement["pilotStatus"],
            },
            {
                "semanticCoverageStatus": "partial",
                "timeFeasibilityStatus": "green",
                "sequenceEvidenceStatus": "partial",
                "pilotStatus": "not-started",
            },
        )
        self.assertEqual(
            judgement["annualVariantIds"],
            ["GRADE-5-BASELINE", "GRADE-5-REGULAR", "GRADE-5-EXTENDED"],
        )
