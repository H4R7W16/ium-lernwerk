import copy
import json
import unittest
from pathlib import Path

from scripts.validate_ium10 import (
    BASELINE_COVERAGE_PROJECTION_SHA256,
    BASELINE_MODULE_STRUCTURE_SHA256,
    BASELINE_TIME_HANDOFF_SHA256,
    IUM10_BASELINE_COMMIT,
    IUM10ValidationError,
    coverage_projection_fingerprint,
    time_handoff_fingerprint,
    validate_capacity_model,
    validate_module_contracts,
    validate_time_model_draft,
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

    def test_repository_draft_has_the_capacity_contract_and_empty_future_contract_lists(self):
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
        self.assertEqual(
            {
                field: time_model[field]
                for field in (
                    "moduleContracts",
                    "integrationContracts",
                    "annualVariants",
                    "timeReviews",
                    "sequenceEvidence",
                    "gradeJudgements",
                    "risks",
                    "pilotAssignments",
                )
            },
            {
                "moduleContracts": [],
                "integrationContracts": [],
                "annualVariants": [],
                "timeReviews": [],
                "sequenceEvidence": [],
                "gradeJudgements": [],
                "risks": [],
                "pilotAssignments": [],
            },
        )
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
