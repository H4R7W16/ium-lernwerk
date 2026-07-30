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

EXPECTED_GRADE_6_CORE_UNITS = {
    "IUM-6-CORE-01": {"baseline": 5, "regular": 6},
    "IUM-6-CORE-02": {"baseline": 4, "regular": 5},
    "IUM-6-CORE-03": {"baseline": 4, "regular": 4},
    "IUM-6-CORE-04": {
        "baseline": 4,
        "regular": 5,
        "targeted-extension": 6,
    },
    "IUM-6-CORE-05": {"baseline": 4, "regular": 4},
    "IUM-6-CORE-06": {"baseline": 4, "regular": 4},
    "IUM-6-CORE-07": {"baseline": 5, "regular": 6},
}

EXPECTED_GRADE_6_FLEX_CONTRACTS = {
    "IUM-6-EXT-01": {
        "standaloneUnitRange": {"min": 3, "recommended": 4, "max": 4},
        "prerequisiteModuleIds": ["IUM-6-CORE-01"],
    },
    "IUM-6-EXT-02": {
        "standaloneUnitRange": {"min": 2, "recommended": 3, "max": 3},
        "prerequisiteModuleIds": ["IUM-6-CORE-05"],
    },
    "IUM-6-TRANSFER-01": {
        "standaloneUnitRange": {"min": 2, "recommended": 4, "max": 4},
        "prerequisiteModuleIds": ["IUM-5-CORE-01", "IUM-6-CORE-05"],
    },
    "IUM-6-PROJECT-01": {
        "standaloneUnitRange": {"min": 8, "recommended": 10, "max": 12},
        "prerequisiteModuleIds": ["IUM-6-CORE-01", "IUM-6-CORE-07"],
    },
}

EXPECTED_GRADE_6_INTEGRATIONS = {
    "INT-6-ACTORS-SELECTION": {
        "moduleIds": ["IUM-6-CORE-01", "IUM-6-CORE-02"],
        "countedInModuleId": "IUM-6-CORE-01",
        "sharedMinutes": 90,
        "savingsMinutesByPath": {"baseline": 90, "regular": 45},
    },
    "INT-6-CONFLICT-PRODUCTION": {
        "moduleIds": ["IUM-6-CORE-06", "IUM-6-CORE-07"],
        "countedInModuleId": "IUM-6-CORE-07",
        "sharedMinutes": 90,
        "savingsMinutesByPath": {"baseline": 90, "regular": 0},
    },
    "INT-6-ALGORITHM-REVISIT": {
        "moduleIds": ["IUM-5-CORE-05", "IUM-6-CORE-04"],
        "countedInModuleId": "IUM-6-CORE-04",
        "sharedMinutes": 45,
        "savingsMinutesByPath": {"baseline": 45, "regular": 0},
    },
}

EXPECTED_GRADE_6_VARIANTS = {
    "GRADE-6-BASELINE": {
        "pathId": "baseline",
        "targetUnits": 30,
        "coreUnits": 30,
        "flexModuleId": None,
        "flexUnits": 0,
    },
    "GRADE-6-REGULAR": {
        "pathId": "regular",
        "targetUnits": 34,
        "coreUnits": 34,
        "flexModuleId": None,
        "flexUnits": 0,
    },
    "GRADE-6-EXTENDED-REFERENCE": {
        "pathId": "extended",
        "targetUnits": 38,
        "coreUnits": 34,
        "flexModuleId": "IUM-6-EXT-01",
        "flexUnits": 4,
    },
    "GRADE-6-EXTENDED-TRANSFER": {
        "pathId": "extended",
        "targetUnits": 38,
        "coreUnits": 34,
        "flexModuleId": "IUM-6-TRANSFER-01",
        "flexUnits": 4,
    },
    "GRADE-6-EXTENDED-CODING": {
        "pathId": "extended",
        "targetUnits": 38,
        "coreUnits": 35,
        "flexModuleId": "IUM-6-EXT-02",
        "flexUnits": 3,
    },
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
        module_payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(encoding="utf-8")
        )

        validate_time_model_draft(time_model, module_payload)

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
        cls.grade_5_and_6_payload = {
            "modules": [
                module
                for module in module_payload["modules"]
                if module["grade"] in {5, 6}
            ]
        }
        cls.grade_5_payload = {
            "modules": [
                module for module in module_payload["modules"] if module["grade"] == 5
            ]
        }
        cls.grade_5_and_6_contracts = [
            contract
            for contract in cls.time_model["moduleContracts"]
            if contract["grade"] in {5, 6}
        ]
        cls.grade_5_contracts = [
            contract
            for contract in cls.time_model["moduleContracts"]
            if contract["grade"] == 5
        ]

    def test_repository_has_seven_complete_grade_5_time_contracts(self):
        contracts = validate_module_contracts(
            self.grade_5_contracts,
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
        all_contracts = validate_module_contracts(
            self.grade_5_and_6_contracts,
            self.grade_5_and_6_payload,
        )
        integrations = validate_integration_contracts(
            self.time_model["integrationContracts"],
            all_contracts,
        )
        contracts = {
            module_id: contract
            for module_id, contract in all_contracts.items()
            if contract["grade"] == 5
        }

        self.assertEqual(
            set(integrations),
            {"INT-5-RESEARCH-PRODUCTION"} | set(EXPECTED_GRADE_6_INTEGRATIONS),
        )
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
                    else ["INT-6-ALGORITHM-REVISIT"]
                    if module_id == "IUM-5-CORE-05"
                    else []
                )
                for module_id in EXPECTED_GRADE_5_UNITS
            },
        )

    def test_repository_has_available_core_only_30_34_38_variants(self):
        all_contracts = validate_module_contracts(
            self.grade_5_and_6_contracts,
            self.grade_5_and_6_payload,
        )
        integrations = validate_integration_contracts(
            self.time_model["integrationContracts"],
            all_contracts,
        )
        all_variants = validate_annual_variants(
            self.time_model["annualVariants"],
            all_contracts,
            integrations,
        )
        contracts = {
            module_id: contract
            for module_id, contract in all_contracts.items()
            if contract["grade"] == 5
        }
        variants = {
            variant_id: variant
            for variant_id, variant in all_variants.items()
            if variant["grade"] == 5
        }

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


class IUM10Grade6RepositoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        cls.time_model = json.loads(
            (root / "roadmap/time-model.json").read_text(encoding="utf-8")
        )
        module_payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(encoding="utf-8")
        )
        cls.grade_5_and_6_payload = {
            "modules": [
                module
                for module in module_payload["modules"]
                if module["grade"] in {5, 6}
            ]
        }
        cls.grade_6_payload = {
            "modules": [
                module for module in module_payload["modules"] if module["grade"] == 6
            ]
        }
        cls.grade_6_modules = {
            module["id"]: module for module in cls.grade_6_payload["modules"]
        }
        cls.grade_6_contracts = [
            contract
            for contract in cls.time_model["moduleContracts"]
            if contract["grade"] == 6
        ]
        cls.grade_5_and_6_contracts = [
            contract
            for contract in cls.time_model["moduleContracts"]
            if contract["grade"] in {5, 6}
        ]

    def validated_contracts(self):
        return validate_module_contracts(
            self.grade_6_contracts,
            self.grade_6_payload,
        )

    def validated_grade_5_and_6_contracts(self, contracts=None):
        return validate_module_contracts(
            (
                self.grade_5_and_6_contracts
                if contracts is None
                else contracts
            ),
            self.grade_5_and_6_payload,
        )

    def validated_orchestration(self, time_model=None):
        model = self.time_model if time_model is None else time_model
        contracts = validate_module_contracts(
            [
                contract
                for contract in model["moduleContracts"]
                if contract["grade"] in {5, 6}
            ],
            self.grade_5_and_6_payload,
        )
        integrations = validate_integration_contracts(
            model["integrationContracts"],
            contracts,
        )
        variants = validate_annual_variants(
            model["annualVariants"],
            contracts,
            integrations,
        )
        return contracts, integrations, variants

    def grade_6_orchestration_findings(self, time_model):
        grade_6_module_ids = set(self.grade_6_modules)
        grade_6_integration_ids = [
            integration["id"]
            for integration in time_model["integrationContracts"]
            if set(integration["moduleIds"]) & grade_6_module_ids
        ]
        grade_6_variant_ids = [
            variant["id"]
            for variant in time_model["annualVariants"]
            if variant["grade"] == 6
            or any(
                allocation["moduleId"] in grade_6_module_ids
                for allocation in variant["allocations"]
            )
        ]
        grade_6_judgement_indexes = [
            index
            for index, judgement in enumerate(time_model["gradeJudgements"])
            if judgement["grade"] == 6
            or set(judgement["annualVariantIds"]) & set(grade_6_variant_ids)
        ]
        return {
            "integrationContractIds": grade_6_integration_ids,
            "annualVariantIds": grade_6_variant_ids,
            "gradeJudgementIndexes": grade_6_judgement_indexes,
        }

    def assert_grade_6_scope_matches_task_6_exactly(self, time_model):
        findings = self.grade_6_orchestration_findings(time_model)
        self.assertEqual(
            set(findings["integrationContractIds"]),
            set(EXPECTED_GRADE_6_INTEGRATIONS),
        )
        self.assertEqual(
            set(findings["annualVariantIds"]),
            set(EXPECTED_GRADE_6_VARIANTS),
        )
        self.assertEqual(len(findings["gradeJudgementIndexes"]), 1)

    def test_repository_grade_6_scope_matches_task_6_exactly(self):
        self.assert_grade_6_scope_matches_task_6_exactly(self.time_model)

    def test_scope_links_spoofed_grade_judgement_to_grade_6_variant(self):
        adversarial_time_model = copy.deepcopy(self.time_model)
        repository_findings = self.grade_6_orchestration_findings(
            self.time_model
        )
        adversarial_time_model["annualVariants"].append(
            {
                "id": "SPOOFED-ALLOCATION-VARIANT",
                "grade": 5,
                "kind": "planning-path",
                "pathId": "baseline",
                "targetUnits": 30,
                "allocations": [
                    {
                        "moduleId": module_id,
                        "budgetPathId": "baseline",
                        "units": units["baseline"],
                    }
                    for module_id, units in EXPECTED_GRADE_6_CORE_UNITS.items()
                ],
                "integrationContractIds": [],
                "available": True,
                "status": "working",
                "rationale": "Über Klasse-6-Allokationen semantisch verknüpft.",
                "risk": "Das grade-Feld ist absichtlich falsch gesetzt.",
            }
        )
        spoofed_judgement_index = len(
            adversarial_time_model["gradeJudgements"]
        )
        adversarial_time_model["gradeJudgements"].append(
            {
                "grade": 5,
                "semanticCoverageStatus": "partial",
                "timeFeasibilityStatus": "green",
                "sequenceEvidenceStatus": "partial",
                "pilotStatus": "not-started",
                "annualVariantIds": ["SPOOFED-ALLOCATION-VARIANT"],
                "rationale": "Über die Jahresvariante semantisch Klasse 6.",
                "risk": "Das grade-Feld ist absichtlich falsch gesetzt.",
                "decisionOptions": ["defer-to-task-6"],
            }
        )

        findings = self.grade_6_orchestration_findings(
            adversarial_time_model
        )

        self.assertEqual(
            set(findings["annualVariantIds"]),
            set(EXPECTED_GRADE_6_VARIANTS)
            | {"SPOOFED-ALLOCATION-VARIANT"},
        )
        self.assertEqual(
            findings["gradeJudgementIndexes"],
            repository_findings["gradeJudgementIndexes"]
            + [spoofed_judgement_index],
        )
        with self.assertRaises(AssertionError):
            self.assert_grade_6_scope_matches_task_6_exactly(
                adversarial_time_model
            )

    def test_repository_has_exactly_three_grade_6_integrations_with_exact_boundaries(self):
        contracts, integrations, _ = self.validated_orchestration()
        grade_6_integrations = {
            integration_id: integration
            for integration_id, integration in integrations.items()
            if integration_id in EXPECTED_GRADE_6_INTEGRATIONS
        }

        self.assertEqual(
            set(grade_6_integrations),
            set(EXPECTED_GRADE_6_INTEGRATIONS),
        )
        for integration_id, expected in EXPECTED_GRADE_6_INTEGRATIONS.items():
            with self.subTest(integration_id=integration_id):
                integration = grade_6_integrations[integration_id]
                self.assertEqual(integration["pathIds"], ["baseline", "regular"])
                for field, value in expected.items():
                    self.assertEqual(integration[field], value)
                self.assertGreaterEqual(
                    len(integration["preservedLearningActions"]),
                    2,
                )
                self.assertGreaterEqual(
                    len(integration["preservedProductAndCurriculumEvidence"]),
                    2,
                )
                prerequisite_text = " ".join(integration["prerequisites"])
                for module_id in integration["moduleIds"]:
                    with self.subTest(
                        integration_id=integration_id,
                        module_id=module_id,
                    ):
                        learning_actions = [
                            action
                            for action in integration[
                                "preservedLearningActions"
                            ]
                            if action.startswith(f"{module_id} ")
                        ]
                        evidence_records = [
                            evidence
                            for evidence in integration[
                                "preservedProductAndCurriculumEvidence"
                            ]
                            if evidence.startswith(f"{module_id}: ")
                        ]
                        self.assertEqual(len(learning_actions), 1)
                        self.assertEqual(len(evidence_records), 1)
                        self.assertIn(
                            "Kompetenznachweis",
                            evidence_records[0],
                        )
                        self.assertIn(
                            "Produktnachweis",
                            evidence_records[0],
                        )
                        self.assertTrue(
                            any(
                                competency_id in evidence_records[0]
                                for competency_id in contracts[module_id][
                                    "competencyIds"
                                ]
                            )
                        )
                        self.assertIn(module_id, prerequisite_text)
                for path_id, saved_minutes in expected[
                    "savingsMinutesByPath"
                ].items():
                    self.assertIn(
                        f"{path_id}: +{saved_minutes} Minuten",
                        integration["fallback"],
                    )
                    self.assertIn(
                        f"{path_id}:",
                        integration["risk"],
                    )
                self.assertIn(
                    f"{integration['sharedMinutes']} Minuten",
                    integration["fallback"],
                )
                self.assertIn("eigenständig", integration["fallback"].lower())

    def test_rejects_grade_6_integration_when_participant_or_path_evidence_is_removed(self):
        def remove_learning_action(integration):
            del integration["preservedLearningActions"][0]

        def remove_product_evidence(integration):
            del integration["preservedProductAndCurriculumEvidence"][0]

        def remove_concrete_prerequisites(integration):
            integration["prerequisites"] = [
                "Die Voraussetzungen werden vor der Integration allgemein geprüft."
            ]

        def remove_path_specific_fallback(integration):
            integration["fallback"] = (
                "Bei Problemen werden eigenständige Sequenzen bereitgestellt."
            )

        def remove_path_specific_risk(integration):
            integration["risk"] = (
                "Ein allgemeines Integrationsrisiko bleibt zu beobachten."
            )

        mutations = (
            ("participant learning action", remove_learning_action),
            ("participant product evidence", remove_product_evidence),
            ("concrete prerequisites", remove_concrete_prerequisites),
            ("path-specific fallback", remove_path_specific_fallback),
            ("path-specific risk", remove_path_specific_risk),
        )
        for integration_id in EXPECTED_GRADE_6_INTEGRATIONS:
            for label, mutate in mutations:
                with self.subTest(
                    integration_id=integration_id,
                    removed=label,
                ):
                    adversarial_time_model = copy.deepcopy(self.time_model)
                    integration = next(
                        contract
                        for contract in adversarial_time_model[
                            "integrationContracts"
                        ]
                        if contract["id"] == integration_id
                    )
                    mutate(integration)

                    with self.assertRaises(IUM10ValidationError):
                        validate_time_model_draft(
                            adversarial_time_model,
                            self.grade_5_and_6_payload,
                        )

    def test_repository_counts_each_grade_6_shared_allocation_only_in_its_counted_module(self):
        contracts, integrations, _ = self.validated_orchestration()

        for integration_id, expected in EXPECTED_GRADE_6_INTEGRATIONS.items():
            locations = {
                (module_id, budget["pathId"], allocation["minutes"])
                for module_id, contract in contracts.items()
                for budget in contract["pathBudgets"]
                for allocation in budget["sharedAllocations"]
                if allocation["integrationContractId"] == integration_id
            }
            self.assertEqual(
                locations,
                {
                    (
                        expected["countedInModuleId"],
                        path_id,
                        expected["sharedMinutes"],
                    )
                    for path_id in ("baseline", "regular")
                },
            )

            adversarial_contracts = copy.deepcopy(contracts)
            uncounted_module_id = next(
                module_id
                for module_id in expected["moduleIds"]
                if module_id != expected["countedInModuleId"]
            )
            adversarial_contracts[uncounted_module_id]["pathBudgets"][0][
                "sharedAllocations"
            ].append(
                {
                    "integrationContractId": integration_id,
                    "minutes": expected["sharedMinutes"],
                }
            )
            with self.assertRaisesRegex(IUM10ValidationError, "exactly once"):
                validate_integration_contracts(
                    list(integrations.values()),
                    adversarial_contracts,
                )

    def test_rejects_cross_grade_integration_without_prerequisite_and_revisit_chain(self):
        contracts, integrations, _ = self.validated_orchestration()
        adversarial_contracts = copy.deepcopy(contracts)
        adversarial_contracts["IUM-5-CORE-05"]["revisitModuleIds"] = []

        with self.assertRaisesRegex(IUM10ValidationError, "cross-grade"):
            validate_integration_contracts(
                list(integrations.values()),
                adversarial_contracts,
            )

    def test_repository_has_exact_grade_6_30_34_and_three_38_variants(self):
        contracts, _, variants = self.validated_orchestration()
        grade_6_variants = {
            variant_id: variant
            for variant_id, variant in variants.items()
            if variant["grade"] == 6
        }
        core_module_ids = set(EXPECTED_GRADE_6_CORE_UNITS)

        self.assertEqual(set(grade_6_variants), set(EXPECTED_GRADE_6_VARIANTS))
        for variant_id, expected in EXPECTED_GRADE_6_VARIANTS.items():
            with self.subTest(variant_id=variant_id):
                variant = grade_6_variants[variant_id]
                allocations = {
                    allocation["moduleId"]: allocation
                    for allocation in variant["allocations"]
                }
                self.assertEqual(variant["pathId"], expected["pathId"])
                self.assertEqual(variant["targetUnits"], expected["targetUnits"])
                self.assertIs(variant["available"], True)
                self.assertEqual(variant["status"], "working")
                self.assertEqual(
                    core_module_ids & set(allocations),
                    core_module_ids,
                )
                self.assertEqual(
                    sum(
                        allocation["units"]
                        for module_id, allocation in allocations.items()
                        if module_id in core_module_ids
                    ),
                    expected["coreUnits"],
                )
                self.assertNotIn("IUM-6-PROJECT-01", allocations)

                flex_module_ids = {
                    module_id
                    for module_id in allocations
                    if contracts[module_id]["kind"] != "core"
                }
                expected_flex_ids = (
                    set()
                    if expected["flexModuleId"] is None
                    else {expected["flexModuleId"]}
                )
                self.assertEqual(flex_module_ids, expected_flex_ids)
                self.assertEqual(
                    sum(
                        allocations[module_id]["units"]
                        for module_id in flex_module_ids
                    ),
                    expected["flexUnits"],
                )

        coding_allocations = {
            allocation["moduleId"]: allocation
            for allocation in grade_6_variants[
                "GRADE-6-EXTENDED-CODING"
            ]["allocations"]
        }
        self.assertEqual(
            coding_allocations["IUM-6-CORE-04"],
            {
                "moduleId": "IUM-6-CORE-04",
                "budgetPathId": "targeted-extension",
                "units": 6,
            },
        )
        self.assertEqual(
            coding_allocations["IUM-6-EXT-02"],
            {
                "moduleId": "IUM-6-EXT-02",
                "budgetPathId": "standalone",
                "units": 3,
            },
        )

    def test_grade_6_extended_variants_use_explicit_budget_path_overrides(self):
        core_regular_overrides = {
            module_id: "regular" for module_id in EXPECTED_GRADE_6_CORE_UNITS
        }
        expected_overrides = {
            "GRADE-6-EXTENDED-REFERENCE": {
                **core_regular_overrides,
                "IUM-6-EXT-01": "standalone",
            },
            "GRADE-6-EXTENDED-TRANSFER": {
                **core_regular_overrides,
                "IUM-6-TRANSFER-01": "standalone",
            },
            "GRADE-6-EXTENDED-CODING": {
                **core_regular_overrides,
                "IUM-6-CORE-04": "targeted-extension",
                "IUM-6-EXT-02": "standalone",
            },
        }

        self.assertEqual(
            ium10_validator.ANNUAL_VARIANT_BUDGET_PATH_OVERRIDES,
            expected_overrides,
        )

    def test_rejects_stale_grade_6_variant_or_module_override_keys(self):
        contracts = self.validated_grade_5_and_6_contracts()
        integrations = validate_integration_contracts(
            self.time_model["integrationContracts"],
            contracts,
        )
        overrides = ium10_validator.ANNUAL_VARIANT_BUDGET_PATH_OVERRIDES
        original_overrides = copy.deepcopy(overrides)

        def add_stale_variant_override():
            overrides["STALE-GRADE-6-OVERRIDE"] = {
                "IUM-6-CORE-01": "regular",
            }

        def add_stale_module_override():
            overrides["GRADE-6-EXTENDED-REFERENCE"][
                "IUM-6-EXT-02"
            ] = "standalone"

        mutations = (
            ("stale variant override", add_stale_variant_override),
            ("stale module override", add_stale_module_override),
        )
        try:
            for label, mutate in mutations:
                with self.subTest(label=label):
                    overrides.clear()
                    overrides.update(copy.deepcopy(original_overrides))
                    mutate()

                    with self.assertRaisesRegex(
                        IUM10ValidationError,
                        "variant path override",
                    ):
                        validate_annual_variants(
                            self.time_model["annualVariants"],
                            contracts,
                            integrations,
                        )
        finally:
            overrides.clear()
            overrides.update(original_overrides)

    def test_rejects_grade_6_flex_replacement_and_project_in_normal_variants(self):
        contracts, integrations, variants = self.validated_orchestration()
        core_regular_overrides = {
            module_id: "regular" for module_id in EXPECTED_GRADE_6_CORE_UNITS
        }
        adversarial_variants = []

        flex_replacement = copy.deepcopy(variants["GRADE-6-BASELINE"])
        flex_replacement["id"] = "GRADE-6-FLEX-REPLACEMENT"
        flex_replacement["allocations"] = [
            (
                {
                    "moduleId": "IUM-6-EXT-01",
                    "budgetPathId": "standalone",
                    "units": 4,
                }
                if allocation["moduleId"] == "IUM-6-CORE-03"
                else allocation
            )
            for allocation in flex_replacement["allocations"]
        ]
        adversarial_variants.append(
            (
                flex_replacement,
                {"IUM-6-EXT-01": "standalone"},
                "all core modules",
            )
        )

        project_variant = copy.deepcopy(variants["GRADE-6-REGULAR"])
        project_variant.update(
            {
                "id": "GRADE-6-PROJECT-ADVERSARIAL",
                "pathId": "extended",
                "targetUnits": 44,
            }
        )
        project_variant["allocations"].append(
            {
                "moduleId": "IUM-6-PROJECT-01",
                "budgetPathId": "standalone",
                "units": 10,
            }
        )
        adversarial_variants.append(
            (
                project_variant,
                {
                    **core_regular_overrides,
                    "IUM-6-PROJECT-01": "standalone",
                },
                "project modules",
            )
        )

        for variant, overrides, message in adversarial_variants:
            with self.subTest(variant_id=variant["id"]):
                ium10_validator.ANNUAL_VARIANT_BUDGET_PATH_OVERRIDES[
                    variant["id"]
                ] = overrides
                try:
                    with self.assertRaisesRegex(IUM10ValidationError, message):
                        validate_annual_variants(
                            [variant],
                            contracts,
                            integrations,
                        )
                finally:
                    del ium10_validator.ANNUAL_VARIANT_BUDGET_PATH_OVERRIDES[
                        variant["id"]
                    ]

    def test_repository_grade_6_judgement_is_green_but_semantic_and_pilot_statuses_stay_separate(self):
        validate_time_model_draft(
            self.time_model,
            self.grade_5_and_6_payload,
        )
        judgements = [
            judgement
            for judgement in self.time_model["gradeJudgements"]
            if judgement["grade"] == 6
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
            set(judgement["annualVariantIds"]),
            set(EXPECTED_GRADE_6_VARIANTS),
        )
        self.assertIn("semant", judgement["rationale"].lower())
        self.assertIn("pilot", judgement["risk"].lower())

    def test_rejects_green_grade_6_judgement_when_variants_or_integrations_do_not_pass(self):
        mutations = (
            (
                "failed module contract",
                "moduleContracts",
                "TC-IUM-6-CORE-01",
                "status",
                "failed",
            ),
            (
                "wrong 30 path",
                "annualVariants",
                "GRADE-6-BASELINE",
                "targetUnits",
                31,
            ),
            (
                "failed integration",
                "integrationContracts",
                "INT-6-ACTORS-SELECTION",
                "status",
                "failed",
            ),
        )
        for label, collection, record_id, field, value in mutations:
            with self.subTest(label=label):
                adversarial_time_model = copy.deepcopy(self.time_model)
                records = adversarial_time_model[collection]
                record = next(record for record in records if record["id"] == record_id)
                record[field] = value
                with self.assertRaises(IUM10ValidationError):
                    validate_time_model_draft(
                        adversarial_time_model,
                        self.grade_5_and_6_payload,
                    )

        unjustified_amber = copy.deepcopy(self.time_model)
        next(
            judgement
            for judgement in unjustified_amber["gradeJudgements"]
            if judgement["grade"] == 6
        )["timeFeasibilityStatus"] = "amber"
        with self.assertRaisesRegex(
            IUM10ValidationError,
            "grade 6 green judgement",
        ):
            validate_time_model_draft(
                unjustified_amber,
                self.grade_5_and_6_payload,
            )

    def test_green_grade_6_judgement_runs_structural_and_exact_contract_validation(self):
        def mutate_counted_module(time_model):
            next(
                integration
                for integration in time_model["integrationContracts"]
                if integration["id"] == "INT-6-ACTORS-SELECTION"
            )["countedInModuleId"] = "IUM-6-CORE-03"

        def mutate_module_pair(time_model):
            next(
                integration
                for integration in time_model["integrationContracts"]
                if integration["id"] == "INT-6-CONFLICT-PRODUCTION"
            )["moduleIds"] = ["IUM-6-CORE-05", "IUM-6-CORE-07"]

        def mutate_savings(time_model):
            next(
                integration
                for integration in time_model["integrationContracts"]
                if integration["id"] == "INT-6-ALGORITHM-REVISIT"
            )["savingsMinutesByPath"]["baseline"] = 0

        def mutate_variant_budget_path(time_model):
            variant = next(
                variant
                for variant in time_model["annualVariants"]
                if variant["id"] == "GRADE-6-EXTENDED-REFERENCE"
            )
            allocation = next(
                allocation
                for allocation in variant["allocations"]
                if allocation["moduleId"] == "IUM-6-CORE-01"
            )
            allocation["budgetPathId"] = "baseline"

        mutations = (
            ("invalid counted module", mutate_counted_module),
            ("invalid module pair", mutate_module_pair),
            ("wrong exact savings", mutate_savings),
            ("invalid variant budget path", mutate_variant_budget_path),
        )
        for label, mutate in mutations:
            with self.subTest(label=label):
                adversarial_time_model = copy.deepcopy(self.time_model)
                mutate(adversarial_time_model)

                with self.assertRaises(IUM10ValidationError):
                    validate_time_model_draft(
                        adversarial_time_model,
                        self.grade_5_and_6_payload,
                    )

    def grade_6_amber_with_algorithm_bounds_residual(self, residual_evidence):
        time_model = copy.deepcopy(self.time_model)
        integration = next(
            integration
            for integration in time_model["integrationContracts"]
            if integration["id"] == "INT-6-ALGORITHM-REVISIT"
        )
        integration["savingsMinutesByPath"]["baseline"] = 0
        integration["fallback"] = integration["fallback"].replace(
            "baseline: +45 Minuten",
            "baseline: +0 Minuten",
        )
        judgement = next(
            judgement
            for judgement in time_model["gradeJudgements"]
            if judgement["grade"] == 6
        )
        judgement["timeFeasibilityStatus"] = "amber"
        judgement["rationale"] = "Das Zeiturteil ist wegen eines Restbefunds amber."
        judgement["risk"] = residual_evidence
        return time_model

    def test_amber_grade_6_judgement_rejects_generic_or_id_only_residual_text(self):
        invalid_residual_evidence = (
            "Eine Integration hat einen Restbefund.",
            "INT-6-ALGORITHM-REVISIT",
        )
        for residual_evidence in invalid_residual_evidence:
            with self.subTest(residual_evidence=residual_evidence):
                time_model = self.grade_6_amber_with_algorithm_bounds_residual(
                    residual_evidence
                )

                with self.assertRaises(IUM10ValidationError):
                    validate_time_model_draft(
                        time_model,
                        self.grade_5_and_6_payload,
                    )

    def test_amber_grade_6_judgement_accepts_exact_record_and_cause_evidence(self):
        time_model = self.grade_6_amber_with_algorithm_bounds_residual(
            "INT-6-ALGORITHM-REVISIT [contract-bounds-mismatch]"
        )

        result = validate_time_model_draft(
            time_model,
            self.grade_5_and_6_payload,
        )

        self.assertIs(result, time_model)

    def test_rejects_green_grade_6_judgement_with_duplicate_orchestration_records(self):
        duplicates = (
            ("moduleContracts", "TC-IUM-6-CORE-01"),
            ("integrationContracts", "INT-6-ACTORS-SELECTION"),
            ("annualVariants", "GRADE-6-BASELINE"),
        )
        for collection, record_id in duplicates:
            with self.subTest(collection=collection):
                adversarial_time_model = copy.deepcopy(self.time_model)
                record = next(
                    record
                    for record in adversarial_time_model[collection]
                    if record["id"] == record_id
                )
                adversarial_time_model[collection].append(copy.deepcopy(record))

                with self.assertRaises(IUM10ValidationError):
                    validate_time_model_draft(
                        adversarial_time_model,
                        self.grade_5_and_6_payload,
                    )

    def test_rejects_green_grade_6_judgement_with_extra_flex_project_integration(self):
        adversarial_time_model = copy.deepcopy(self.time_model)
        integration_id = "INT-6-EXTRA-FLEX-PROJECT"
        participant_ids = ("IUM-6-EXT-02", "IUM-6-PROJECT-01")
        contracts = {
            contract["moduleId"]: contract
            for contract in adversarial_time_model["moduleContracts"]
        }
        for module_id in participant_ids:
            contracts[module_id]["integrationContractIds"].append(
                integration_id
            )
        counted_budget = contracts["IUM-6-PROJECT-01"]["pathBudgets"][0]
        counted_budget["directMinutes"] -= 45
        counted_budget["countedSharedMinutes"] += 45
        counted_budget["sharedAllocations"].append(
            {
                "integrationContractId": integration_id,
                "minutes": 45,
            }
        )
        adversarial_time_model["integrationContracts"].append(
            {
                "id": integration_id,
                "moduleIds": list(participant_ids),
                "pathIds": ["standalone"],
                "sharedPhaseOrProduct": (
                    "Adversariale gemeinsame Flex-Projekt-Spur."
                ),
                "countedInModuleId": "IUM-6-PROJECT-01",
                "sharedMinutes": 45,
                "savingsMinutesByPath": {"standalone": 0},
                "preservedLearningActions": [
                    "Beide Module bearbeiten eine gemeinsame Spur."
                ],
                "preservedProductAndCurriculumEvidence": [
                    "Ein gemeinsames Produkt bleibt sichtbar."
                ],
                "prerequisites": [
                    "Beide Modulverträge liegen vor."
                ],
                "risk": "Die zusätzliche Integration ist nicht autorisiert.",
                "fallback": "Beide Module arbeiten eigenständig.",
                "status": "working",
            }
        )

        with self.assertRaisesRegex(
            IUM10ValidationError,
            "grade 6 green judgement",
        ):
            validate_time_model_draft(
                adversarial_time_model,
                self.grade_5_and_6_payload,
            )

    def test_repository_has_exactly_eleven_complete_grade_6_time_contracts(self):
        expected_module_ids = set(EXPECTED_GRADE_6_CORE_UNITS) | set(
            EXPECTED_GRADE_6_FLEX_CONTRACTS
        )
        self.assertEqual(
            {contract["moduleId"] for contract in self.grade_6_contracts},
            expected_module_ids,
        )
        contracts = self.validated_contracts()
        self.assertEqual(set(contracts), expected_module_ids)
        self.assertEqual(len(contracts), 11)

    def test_repository_grade_6_core_paths_match_the_approved_matrix(self):
        contracts = self.validated_contracts()

        for module_id, expected_paths in EXPECTED_GRADE_6_CORE_UNITS.items():
            with self.subTest(module_id=module_id):
                budgets = {
                    budget["pathId"]: budget
                    for budget in contracts[module_id]["pathBudgets"]
                }
                self.assertEqual(
                    {
                        path_id: budget["units"]
                        for path_id, budget in budgets.items()
                    },
                    expected_paths,
                )

    def test_repository_grade_6_flex_ranges_and_prerequisites_match_the_graph(self):
        contracts = self.validated_contracts()

        for module_id, expected in EXPECTED_GRADE_6_FLEX_CONTRACTS.items():
            with self.subTest(module_id=module_id):
                contract = contracts[module_id]
                self.assertEqual(
                    contract["standaloneUnitRange"],
                    expected["standaloneUnitRange"],
                )
                self.assertEqual(
                    contract["prerequisiteModuleIds"],
                    expected["prerequisiteModuleIds"],
                )
                self.assertEqual(
                    contract["prerequisiteModuleIds"],
                    self.grade_6_modules[module_id]["prerequisiteModuleIds"],
                )
                self.assertEqual(
                    contract["pathBudgets"][0]["units"],
                    expected["standaloneUnitRange"]["recommended"],
                )

    def test_repository_grade_6_phase_budgets_are_positive_and_grammar_complete(self):
        contracts = self.validated_contracts()

        for module_id, contract in contracts.items():
            expected_phase_ids = set(
                self.grade_6_modules[module_id]["moduleGrammar"]
            )
            for budget in contract["pathBudgets"]:
                with self.subTest(module_id=module_id, path_id=budget["pathId"]):
                    phase_budgets = budget["phaseBudgets"]
                    self.assertEqual(
                        {phase["phaseId"] for phase in phase_budgets},
                        expected_phase_ids,
                    )
                    self.assertTrue(
                        all(
                            phase["minutes"] > 0
                            and phase["learningFunction"].strip()
                            for phase in phase_budgets
                        )
                    )
                    self.assertEqual(
                        sum(phase["minutes"] for phase in phase_budgets),
                        budget["units"] * 45,
                    )

    def test_repository_extra_grade_6_core_time_only_expands_allowed_functions(self):
        contracts = self.validated_contracts()
        allowed_growth_phases = {
            "activate-prior-knowledge",
            "build-concept",
            "guided-practice",
            "independent-action-product",
            "review-revise-transfer",
            "shared-consolidation",
        }

        for module_id in EXPECTED_GRADE_6_CORE_UNITS:
            budgets = {
                budget["pathId"]: budget
                for budget in contracts[module_id]["pathBudgets"]
            }
            ordered_path_ids = [
                path_id
                for path_id in ("baseline", "regular", "targeted-extension")
                if path_id in budgets
            ]
            for earlier_path_id, later_path_id in zip(
                ordered_path_ids,
                ordered_path_ids[1:],
            ):
                earlier = {
                    phase["phaseId"]: phase["minutes"]
                    for phase in budgets[earlier_path_id]["phaseBudgets"]
                }
                later = {
                    phase["phaseId"]: phase["minutes"]
                    for phase in budgets[later_path_id]["phaseBudgets"]
                }
                growth_phases = {
                    phase_id
                    for phase_id in earlier
                    if later[phase_id] > earlier[phase_id]
                }
                with self.subTest(
                    module_id=module_id,
                    earlier_path_id=earlier_path_id,
                    later_path_id=later_path_id,
                ):
                    self.assertTrue(growth_phases <= allowed_growth_phases)
                    if budgets[later_path_id]["units"] > budgets[earlier_path_id]["units"]:
                        self.assertTrue(growth_phases)

    def test_repository_project_requires_focus_time_outside_normal_year_paths(self):
        contracts = self.validated_contracts()
        project = contracts["IUM-6-PROJECT-01"]

        self.assertIn("zusätzliche", project["risk"].lower())
        self.assertIn("schwerpunktzeit", project["risk"].lower())
        self.assertIn("30/34/38", project["risk"])
        self.assertFalse(
            any(
                allocation["moduleId"] == project["moduleId"]
                for variant in self.time_model["annualVariants"]
                for allocation in variant["allocations"]
            )
        )
