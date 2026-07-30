import copy
import hashlib
import json
from collections import Counter

from scripts.validate_ium09 import module_structure_fingerprint


IUM10_BASELINE_COMMIT = "e53bad7cffe1541fc910db948235908bebe89caa"
BASELINE_MODULE_STRUCTURE_SHA256 = (
    "da02be74104d88dd9adb0d7927feeab4eea5f65dcc616c5645b0f2145ca4d4fc"
)
BASELINE_COVERAGE_PROJECTION_SHA256 = (
    "cb9e09fa755a15206054e87ad0d5a8784fead63ff59530da0088b34e11dd2974"
)
BASELINE_TIME_HANDOFF_SHA256 = (
    "423b94122b931f4585b75aa74074f71b2e80a2b8b02cc92b32bf74585128f9bd"
)
ROADMAP_DEPENDENT_IDS = frozenset(
    {
        "LH26-E-PROG-001",
        "LH26-E-PROG-002",
        "LH26-E-PROG-003",
        "LH26-E-PROG-004",
    }
)
PHASE_IDS = (
    "orientation-challenge",
    "activate-prior-knowledge",
    "build-concept",
    "guided-practice",
    "independent-action-product",
    "review-revise-transfer",
    "shared-consolidation",
)
CONTRACT_STATUSES = {"working", "reviewed"}
CORE_PATH_IDS = {
    5: {"baseline", "regular", "extended"},
    6: {"baseline", "regular"},
    7: {"optimized", "robust", "historical-minimum"},
}
CORE_PATH_ORDER = {
    5: ("baseline", "regular", "extended"),
    6: ("baseline", "regular", "targeted-extension"),
    7: ("optimized", "robust", "historical-minimum"),
}
ANNUAL_PATH_IDS_BY_KIND = {
    "planning-path": {"baseline", "regular", "extended"},
    "demand-scenario": {"optimized", "robust", "historical-minimum"},
}
GRADE_6_CORE_MODULE_IDS = frozenset(
    {
        "IUM-6-CORE-01",
        "IUM-6-CORE-02",
        "IUM-6-CORE-03",
        "IUM-6-CORE-04",
        "IUM-6-CORE-05",
        "IUM-6-CORE-06",
        "IUM-6-CORE-07",
    }
)
GRADE_6_INTEGRATION_IDS = frozenset(
    {
        "INT-6-ACTORS-SELECTION",
        "INT-6-CONFLICT-PRODUCTION",
        "INT-6-ALGORITHM-REVISIT",
    }
)
GRADE_6_VARIANT_TARGETS = {
    "GRADE-6-BASELINE": ("baseline", 30),
    "GRADE-6-REGULAR": ("regular", 34),
    "GRADE-6-EXTENDED-REFERENCE": ("extended", 38),
    "GRADE-6-EXTENDED-TRANSFER": ("extended", 38),
    "GRADE-6-EXTENDED-CODING": ("extended", 38),
}
_GRADE_6_REGULAR_CORE_OVERRIDES = {
    module_id: "regular" for module_id in GRADE_6_CORE_MODULE_IDS
}
ANNUAL_VARIANT_BUDGET_PATH_OVERRIDES = {
    "GRADE-6-EXTENDED-REFERENCE": {
        **_GRADE_6_REGULAR_CORE_OVERRIDES,
        "IUM-6-EXT-01": "standalone",
    },
    "GRADE-6-EXTENDED-TRANSFER": {
        **_GRADE_6_REGULAR_CORE_OVERRIDES,
        "IUM-6-TRANSFER-01": "standalone",
    },
    "GRADE-6-EXTENDED-CODING": {
        **_GRADE_6_REGULAR_CORE_OVERRIDES,
        "IUM-6-CORE-04": "targeted-extension",
        "IUM-6-EXT-02": "standalone",
    },
}


class IUM10ValidationError(ValueError):
    pass


def _require(condition, message):
    if not condition:
        raise IUM10ValidationError(message)


def _positive_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _nonnegative_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _nonempty_string_list(value):
    return (
        isinstance(value, list)
        and all(isinstance(item, str) and item.strip() for item in value)
        and len(value) == len(set(value))
    )


def _canonical_sha256(value):
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _validate_grade_6_judgement(time_model):
    module_contracts = time_model.get("moduleContracts")
    integration_contracts = time_model.get("integrationContracts")
    annual_variants = time_model.get("annualVariants")
    grade_judgements = time_model.get("gradeJudgements")
    _require(
        isinstance(module_contracts, list)
        and isinstance(integration_contracts, list)
        and isinstance(annual_variants, list)
        and isinstance(grade_judgements, list),
        "grade 6 orchestration collections must be lists",
    )

    grade_6_module_contract_records = [
        contract
        for contract in module_contracts
        if isinstance(contract, dict) and contract.get("grade") == 6
    ]
    grade_6_module_contracts = {
        contract.get("moduleId"): contract
        for contract in grade_6_module_contract_records
    }
    grade_6_integration_records = [
        contract
        for contract in integration_contracts
        if isinstance(contract, dict)
        and (
            contract.get("id") in GRADE_6_INTEGRATION_IDS
            or any(
                module_id in GRADE_6_CORE_MODULE_IDS
                for module_id in contract.get("moduleIds", [])
                if isinstance(module_id, str)
            )
        )
    ]
    grade_6_integrations = {
        contract.get("id"): contract
        for contract in grade_6_integration_records
    }
    grade_6_variant_records = [
        variant
        for variant in annual_variants
        if isinstance(variant, dict) and variant.get("grade") == 6
    ]
    grade_6_variants = {
        variant.get("id"): variant
        for variant in grade_6_variant_records
    }
    grade_6_judgements = [
        judgement
        for judgement in grade_judgements
        if isinstance(judgement, dict) and judgement.get("grade") == 6
    ]
    orchestration_present = bool(
        grade_6_integrations or grade_6_variants or grade_6_judgements
    )
    if not orchestration_present:
        return

    _require(
        len(grade_6_judgements) == 1,
        "grade 6 orchestration needs exactly one judgement",
    )
    judgement = grade_6_judgements[0]
    judgement_fields = {
        "grade",
        "semanticCoverageStatus",
        "timeFeasibilityStatus",
        "sequenceEvidenceStatus",
        "pilotStatus",
        "annualVariantIds",
        "rationale",
        "risk",
        "decisionOptions",
    }
    _require(
        set(judgement) == judgement_fields,
        "grade 6 judgement fields differ from the IUM10 contract",
    )
    _require(
        judgement["semanticCoverageStatus"] in {"covered", "partial"}
        and judgement["sequenceEvidenceStatus"] in {"covered", "partial"}
        and judgement["pilotStatus"]
        in {"not-started", "in-progress", "completed"},
        "grade 6 semantic, sequence, or pilot status is invalid",
    )
    _require(
        judgement["timeFeasibilityStatus"] in {"green", "amber"},
        "grade 6 time feasibility must be green or amber",
    )
    _require(
        _nonempty_string_list(judgement["annualVariantIds"])
        and set(judgement["annualVariantIds"]) == set(GRADE_6_VARIANT_TARGETS),
        "grade 6 judgement must reference the exact annual variants",
    )
    for field in ("rationale", "risk"):
        _require(
            isinstance(judgement[field], str) and judgement[field].strip(),
            f"grade 6 judgement {field} must be a nonempty string",
        )
    _require(
        _nonempty_string_list(judgement["decisionOptions"])
        and judgement["decisionOptions"],
        "grade 6 judgement decision options must be nonempty and unique",
    )

    residual_markers = []
    if (
        not GRADE_6_CORE_MODULE_IDS <= set(grade_6_module_contracts)
        or len(grade_6_module_contracts) != 11
        or len(grade_6_module_contract_records)
        != len(grade_6_module_contracts)
    ):
        residual_markers.append("module contracts")
    for module_id, module_contract in grade_6_module_contracts.items():
        if module_contract.get("status") not in {"working", "reviewed"}:
            residual_markers.append(module_id)
    if (
        set(grade_6_integrations) != set(GRADE_6_INTEGRATION_IDS)
        or len(grade_6_integration_records) != len(grade_6_integrations)
    ):
        residual_markers.append("integration")
    for integration_id in GRADE_6_INTEGRATION_IDS:
        integration = grade_6_integrations.get(integration_id)
        if not isinstance(integration, dict) or integration.get("status") not in {
            "working",
            "reviewed",
        }:
            residual_markers.append(integration_id)

    if (
        set(grade_6_variants) != set(GRADE_6_VARIANT_TARGETS)
        or len(grade_6_variant_records) != len(grade_6_variants)
    ):
        residual_markers.append("30/34/38")
    for variant_id, (path_id, target_units) in GRADE_6_VARIANT_TARGETS.items():
        variant = grade_6_variants.get(variant_id)
        if (
            not isinstance(variant, dict)
            or variant.get("pathId") != path_id
            or variant.get("targetUnits") != target_units
            or variant.get("available") is not True
            or variant.get("status") not in {"working", "reviewed"}
        ):
            residual_markers.append(variant_id)

    ready_for_green = not residual_markers
    _require(
        (judgement["timeFeasibilityStatus"] == "green") == ready_for_green,
        "grade 6 green judgement requires exact 30/34/38 variants and passing integrations",
    )
    if not ready_for_green:
        residual_text = f"{judgement['rationale']} {judgement['risk']}"
        _require(
            any(marker in residual_text for marker in residual_markers),
            "grade 6 amber judgement must name a concrete residual finding",
        )


def coverage_projection_fingerprint(coverage_payload, remediation_payload):
    remediation_by_id = {
        entry["competencyId"]: entry
        for entry in remediation_payload["entries"]
    }
    projection = []
    for entry in coverage_payload["entries"]:
        remediation = remediation_by_id.get(entry["competencyId"])
        after = remediation["after"] if remediation else entry
        projection.append(
            {
                "competencyId": entry["competencyId"],
                "moduleIds": sorted(entry["moduleIds"]),
                "coverageStatus": after["coverageStatus"],
                "semanticAudit": after["semanticAudit"],
                "evidenceModuleId": entry["evidenceModuleId"],
            }
        )
    return _canonical_sha256(
        sorted(projection, key=lambda record: record["competencyId"])
    )


def time_handoff_fingerprint(remediation_payload):
    handoffs = [
        {
            "competencyId": entry["competencyId"],
            "moduleId": entry["before"]["evidenceModuleId"],
            "sourceTimeImpactLevel": entry["timeImpact"]["level"],
            "sourceTimeImpactRationale": entry["timeImpact"]["rationale"],
        }
        for entry in remediation_payload["entries"]
    ]
    return _canonical_sha256(
        sorted(handoffs, key=lambda record: record["competencyId"])
    )


def validate_time_model_draft(time_model):
    """Validate the top-level schema version required by the IUM10 draft."""
    _require(isinstance(time_model, dict), "time model draft must be an object")
    schema_version = time_model.get("schemaVersion")
    _require(
        isinstance(schema_version, int)
        and not isinstance(schema_version, bool)
        and schema_version == 1,
        "schema version must be the integer 1",
    )
    _validate_grade_6_judgement(time_model)
    return time_model


def validate_capacity_model(capacity_model, unit_contract):
    """Validate IUM10's dated capacity assumptions and return planning paths."""
    _require(isinstance(unit_contract, dict), "unit contract must be an object")
    _require(
        set(unit_contract) == {"label", "minutes"},
        "unit contract fields differ from the IUM10 contract",
    )
    _require(
        unit_contract["label"] == "Unterrichtseinheit",
        "unit label must be Unterrichtseinheit",
    )
    _require(
        isinstance(unit_contract["minutes"], int)
        and not isinstance(unit_contract["minutes"], bool)
        and unit_contract["minutes"] == 45,
        "unit minutes must be exactly 45",
    )

    _require(isinstance(capacity_model, dict), "capacity model must be an object")
    _require(
        set(capacity_model)
        == {
            "officialWeeklyUnits",
            "officialStatus",
            "calendarEstimate",
            "capacityLevels",
            "planningPaths",
            "bufferRule",
            "status",
        },
        "capacity model fields differ from the IUM10 contract",
    )
    _require(
        isinstance(capacity_model["officialWeeklyUnits"], int)
        and not isinstance(capacity_model["officialWeeklyUnits"], bool)
        and capacity_model["officialWeeklyUnits"] == 1,
        "official weekly units must be exactly 1",
    )
    _require(
        capacity_model["officialStatus"] == "administrative-context",
        "official status must be administrative-context; 30+6 is only an explanatory risk text",
    )

    calendar_estimate = capacity_model["calendarEstimate"]
    _require(isinstance(calendar_estimate, dict), "calendar estimate must be an object")
    _require(
        set(calendar_estimate) == {"schoolYear", "status", "weekdayUnits"},
        "calendar estimate fields differ from the IUM10 contract",
    )
    _require(
        calendar_estimate["schoolYear"] == "2026/2027",
        "calendar school year must be 2026/2027",
    )
    _require(
        calendar_estimate["status"] == "dated-project-calculation",
        "calendar estimate must be a dated project calculation",
    )
    weekday_units = calendar_estimate["weekdayUnits"]
    expected_weekday_units = {
        "monday": 40,
        "tuesday": 40,
        "wednesday": 39,
        "thursday": 36,
        "friday": 37,
    }
    _require(isinstance(weekday_units, dict), "weekday units must be an object")
    _require(
        set(weekday_units) == set(expected_weekday_units),
        "weekday unit fields differ from the IUM10 contract",
    )
    for weekday, expected_units in expected_weekday_units.items():
        _require(
            isinstance(weekday_units[weekday], int)
            and not isinstance(weekday_units[weekday], bool)
            and weekday_units[weekday] == expected_units,
            f"weekday units for {weekday} differ from the IUM10 contract",
        )

    _require(
        capacity_model["capacityLevels"]
        == ["calendar-capacity", "local-capacity", "planning-capacity"],
        "capacity levels differ from the IUM10 contract",
    )

    planning_paths = capacity_model["planningPaths"]
    _require(isinstance(planning_paths, list), "planning paths must be a list")
    _require(len(planning_paths) == 3, "planning paths must contain exactly three paths")
    paths_by_id = {}
    for path in planning_paths:
        _require(isinstance(path, dict), "planning path must be an object")
        _require(
            set(path) == {"id", "units", "status"},
            "planning path fields differ from the IUM10 contract",
        )
        _require(isinstance(path["id"], str), "planning path id must be a string")
        _require(path["id"] not in paths_by_id, "planning path ids must be unique")
        _require(
            isinstance(path["units"], int) and not isinstance(path["units"], bool),
            "planning path units must be an integer",
        )
        _require(path["status"] == "working", "planning path status must be working")
        paths_by_id[path["id"]] = path
    expected_path_units = {"baseline": 30, "regular": 34, "extended": 38}
    _require(
        set(paths_by_id) == set(expected_path_units),
        "planning path ids differ from the IUM10 contract",
    )
    for path_id, expected_units in expected_path_units.items():
        _require(
            paths_by_id[path_id]["units"] == expected_units,
            f"planning path {path_id} units differ from the IUM10 contract",
        )

    buffer_rule = capacity_model["bufferRule"]
    _require(isinstance(buffer_rule, dict), "buffer rule must be an object")
    _require(
        set(buffer_rule)
        == {"formula", "minimumBufferUnits", "protectedLearningFunctions"},
        "buffer rule fields differ from the IUM10 contract",
    )
    _require(
        buffer_rule["formula"] == "localCapacityUnits - selectedPathUnits",
        "buffer formula must subtract the selected path from local capacity",
    )
    _require(
        isinstance(buffer_rule["minimumBufferUnits"], int)
        and not isinstance(buffer_rule["minimumBufferUnits"], bool)
        and buffer_rule["minimumBufferUnits"] == 0,
        "minimum buffer units must be the non-negative value 0",
    )
    _require(
        buffer_rule["protectedLearningFunctions"]
        == [
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
        "baseline path must retain all protected learning functions outside the buffer",
    )
    _require(capacity_model["status"] == "working", "capacity model status must be working")

    return paths_by_id


def validate_module_contracts(module_contracts, module_payload):
    """Validate time contracts against the immutable IUM09 module graph."""
    modules = module_payload.get("modules") if isinstance(module_payload, dict) else None
    _require(isinstance(modules, list), "module payload must contain modules")
    modules_by_id = {}
    for module in modules:
        _require(isinstance(module, dict), "module must be an object")
        module_id = module.get("id")
        _require(
            isinstance(module_id, str) and module_id,
            "module id must be a nonempty string",
        )
        _require(module_id not in modules_by_id, "module ids must be unique")
        modules_by_id[module_id] = module

    _require(isinstance(module_contracts, list), "module contracts must be a list")
    contract_fields = {
        "id",
        "moduleId",
        "grade",
        "kind",
        "historicalLessonRange",
        "competencyIds",
        "centralLearningAction",
        "centralLearningProduct",
        "prerequisiteModuleIds",
        "revisitModuleIds",
        "pathBudgets",
        "standaloneUnitRange",
        "timeReviewIds",
        "integrationContractIds",
        "schoolDependentSteps",
        "risk",
        "pilotRequired",
        "status",
    }
    contracts_by_module_id = {}
    contract_ids = set()
    for contract in module_contracts:
        _require(isinstance(contract, dict), "module contract must be an object")
        _require(
            set(contract) == contract_fields,
            "module contract fields differ from the IUM10 contract",
        )
        module_id = contract["moduleId"]
        _require(
            isinstance(module_id, str) and module_id in modules_by_id,
            f"unknown module for time contract: {module_id}",
        )
        _require(
            module_id not in contracts_by_module_id,
            f"module needs exactly one time contract: {module_id}",
        )
        contract_id = contract["id"]
        _require(
            isinstance(contract_id, str) and contract_id == f"TC-{module_id}",
            f"invalid time contract id: {module_id}",
        )
        _require(contract_id not in contract_ids, "time contract ids must be unique")
        contract_ids.add(contract_id)
        module = modules_by_id[module_id]
        for field, source_field in (
            ("grade", "grade"),
            ("kind", "kind"),
            ("historicalLessonRange", "lessonRange"),
            ("competencyIds", "competencyIds"),
            ("centralLearningAction", "centralLearningAction"),
            ("centralLearningProduct", "centralLearningProduct"),
            ("prerequisiteModuleIds", "prerequisiteModuleIds"),
        ):
            _require(
                contract[field] == module.get(source_field),
                f"time contract {field} differs from module: {module_id}",
            )
        _require(
            _nonempty_string_list(contract["revisitModuleIds"]),
            f"invalid revisit module ids: {module_id}",
        )
        _require(
            _nonempty_string_list(contract["timeReviewIds"]),
            f"invalid time review ids: {module_id}",
        )
        _require(
            _nonempty_string_list(contract["integrationContractIds"]),
            f"invalid integration contract ids: {module_id}",
        )
        _require(
            _nonempty_string_list(contract["schoolDependentSteps"]),
            f"invalid school-dependent steps: {module_id}",
        )
        _require(
            isinstance(contract["risk"], str) and contract["risk"].strip(),
            f"time contract risk must be a nonempty string: {module_id}",
        )
        _require(
            contract["pilotRequired"] is True,
            f"time contract must require a pilot: {module_id}",
        )
        _require(
            isinstance(contract["status"], str)
            and contract["status"] in CONTRACT_STATUSES,
            f"invalid time contract status: {module_id}",
        )

        is_core = contract["kind"] == "core"
        standalone_range = contract["standaloneUnitRange"]
        if is_core:
            _require(
                contract["grade"] in CORE_PATH_IDS,
                f"invalid core module grade: {module_id}",
            )
            _require(
                standalone_range is None,
                f"core module cannot have a standalone unit range: {module_id}",
            )
            expected_path_id_sets = {frozenset(CORE_PATH_IDS[contract["grade"]])}
            if module_id == "IUM-6-CORE-04":
                expected_path_id_sets.add(
                    frozenset(CORE_PATH_IDS[contract["grade"]] | {"targeted-extension"})
                )
        else:
            _require(
                isinstance(standalone_range, dict)
                and set(standalone_range) == {"min", "recommended", "max"}
                and all(_positive_int(value) for value in standalone_range.values())
                and standalone_range["min"]
                <= standalone_range["recommended"]
                <= standalone_range["max"],
                f"invalid standalone unit range: {module_id}",
            )
            expected_path_id_sets = {frozenset({"standalone"})}

        path_budgets = contract["pathBudgets"]
        _require(isinstance(path_budgets, list), f"path budgets must be a list: {module_id}")
        path_ids = []
        validated_budgets = []
        for budget in path_budgets:
            _require(isinstance(budget, dict), f"path budget must be an object: {module_id}")
            _require(
                set(budget)
                == {
                    "pathId",
                    "units",
                    "minutes",
                    "directMinutes",
                    "countedSharedMinutes",
                    "phaseBudgets",
                    "sharedAllocations",
                },
                f"path budget fields differ from the IUM10 contract: {module_id}",
            )
            path_id = budget["pathId"]
            _require(
                isinstance(path_id, str) and path_id,
                f"path budget id must be a nonempty string: {module_id}",
            )
            path_ids.append(path_id)
            _require(
                _positive_int(budget["units"]),
                f"path budget units must be a positive integer: {module_id}",
            )
            _require(
                _positive_int(budget["minutes"]),
                f"path budget minutes must be a positive integer: {module_id}",
            )
            _require(
                _nonnegative_int(budget["directMinutes"])
                and _nonnegative_int(budget["countedSharedMinutes"]),
                f"direct and shared minutes must be non-negative integers: {module_id}",
            )
            _require(
                budget["minutes"] == budget["units"] * 45,
                f"path budget minutes must equal units times 45: {module_id}",
            )
            _require(
                budget["minutes"]
                == budget["directMinutes"] + budget["countedSharedMinutes"],
                f"direct and shared minutes must equal total minutes: {module_id}",
            )

            phase_budgets = budget["phaseBudgets"]
            _require(
                isinstance(phase_budgets, list),
                f"phase budgets must be a list: {module_id}",
            )
            phase_ids = []
            phase_minutes = 0
            for phase_budget in phase_budgets:
                _require(
                    isinstance(phase_budget, dict)
                    and set(phase_budget)
                    == {"phaseId", "minutes", "learningFunction"},
                    f"phase budget fields differ from the IUM10 contract: {module_id}",
                )
                phase_id = phase_budget["phaseId"]
                _require(
                    isinstance(phase_id, str) and phase_id in PHASE_IDS,
                    f"invalid phase id: {module_id}",
                )
                _require(
                    _positive_int(phase_budget["minutes"]),
                    f"phase minutes must be a positive integer: {module_id}",
                )
                _require(
                    isinstance(phase_budget["learningFunction"], str)
                    and phase_budget["learningFunction"].strip(),
                    f"learning function must be a nonempty string: {module_id}",
                )
                phase_ids.append(phase_id)
                phase_minutes += phase_budget["minutes"]
            expected_phase_ids = set(PHASE_IDS) if is_core else set(module["moduleGrammar"])
            _require(
                len(phase_ids) == len(set(phase_ids))
                and set(phase_ids) == expected_phase_ids,
                f"phase budgets differ from module grammar: {module_id}",
            )
            _require(
                phase_minutes == budget["minutes"],
                f"phase budget minutes must equal total minutes: {module_id}",
            )

            shared_allocations = budget["sharedAllocations"]
            _require(
                isinstance(shared_allocations, list),
                f"shared allocations must be a list: {module_id}",
            )
            allocation_ids = set()
            shared_minutes = 0
            for allocation in shared_allocations:
                _require(
                    isinstance(allocation, dict)
                    and set(allocation) == {"integrationContractId", "minutes"},
                    f"shared allocation fields differ from the IUM10 contract: {module_id}",
                )
                allocation_id = allocation["integrationContractId"]
                _require(
                    isinstance(allocation_id, str) and allocation_id,
                    f"invalid shared allocation id: {module_id}",
                )
                _require(
                    allocation_id not in allocation_ids,
                    f"shared allocation ids must be unique: {module_id}",
                )
                _require(
                    _positive_int(allocation["minutes"]),
                    f"shared allocation minutes must be a positive integer: {module_id}",
                )
                allocation_ids.add(allocation_id)
                shared_minutes += allocation["minutes"]
            _require(
                shared_minutes == budget["countedSharedMinutes"],
                f"shared allocation minutes must equal counted shared minutes: {module_id}",
            )
            validated_budgets.append(budget)
        _require(
            len(path_ids) == len(set(path_ids))
            and frozenset(path_ids) in expected_path_id_sets,
            f"time contract paths differ from the IUM10 contract: {module_id}",
        )
        if is_core:
            protected_growth_phases = {
                "guided-practice",
                "independent-action-product",
                "review-revise-transfer",
            }
            budgets_by_path_id = {
                budget["pathId"]: budget for budget in validated_budgets
            }
            ordered_budgets = [
                budgets_by_path_id[path_id]
                for path_id in CORE_PATH_ORDER[contract["grade"]]
                if path_id in budgets_by_path_id
            ]
            for previous_budget, budget in zip(
                ordered_budgets,
                ordered_budgets[1:],
            ):
                if budget["units"] <= previous_budget["units"]:
                    continue
                previous_phase_minutes = {
                    phase["phaseId"]: phase["minutes"]
                    for phase in previous_budget["phaseBudgets"]
                }
                phase_minutes = {
                    phase["phaseId"]: phase["minutes"]
                    for phase in budget["phaseBudgets"]
                }
                _require(
                    any(
                        phase_minutes[phase_id] > previous_phase_minutes[phase_id]
                        for phase_id in protected_growth_phases
                    ),
                    "additional path time must increase practice, product, or revision "
                    "over its immediate predecessor: "
                    f"{module_id}/{budget['pathId']}",
                )
        contracts_by_module_id[module_id] = contract

    _require(
        set(contracts_by_module_id) == set(modules_by_id),
        "every module needs exactly one time contract",
    )
    return contracts_by_module_id


def validate_integration_contracts(integration_contracts, module_contracts):
    """Validate shared-time contracts and enforce single counting."""
    _require(
        isinstance(module_contracts, dict),
        "validated module contracts must be keyed by module id",
    )
    for module_id, module_contract in module_contracts.items():
        _require(
            isinstance(module_id, str)
            and isinstance(module_contract, dict)
            and module_contract.get("moduleId") == module_id,
            "module contract index differs from module ids",
        )

    _require(
        isinstance(integration_contracts, list),
        "integration contracts must be a list",
    )
    contract_fields = {
        "id",
        "moduleIds",
        "pathIds",
        "sharedPhaseOrProduct",
        "countedInModuleId",
        "sharedMinutes",
        "savingsMinutesByPath",
        "preservedLearningActions",
        "preservedProductAndCurriculumEvidence",
        "prerequisites",
        "risk",
        "fallback",
        "status",
    }
    contracts_by_id = {}
    for contract in integration_contracts:
        _require(
            isinstance(contract, dict),
            "integration contract must be an object",
        )
        _require(
            set(contract) == contract_fields,
            "integration contract fields differ from the IUM10 contract",
        )
        contract_id = contract["id"]
        _require(
            isinstance(contract_id, str) and contract_id.strip(),
            "integration contract id must be a nonempty string",
        )
        _require(
            contract_id not in contracts_by_id,
            "integration contract ids must be unique",
        )

        module_ids = contract["moduleIds"]
        _require(
            _nonempty_string_list(module_ids) and len(module_ids) >= 2,
            f"integration needs at least two unique modules: {contract_id}",
        )
        _require(
            all(module_id in module_contracts for module_id in module_ids),
            f"integration references unknown module: {contract_id}",
        )
        counted_module_id = contract["countedInModuleId"]
        _require(
            isinstance(counted_module_id, str)
            and counted_module_id in module_ids,
            f"integration counted module must be a participant: {contract_id}",
        )
        participant_grades = {
            module_id: module_contracts[module_id].get("grade")
            for module_id in module_ids
        }
        if len(set(participant_grades.values())) > 1:
            _require(
                len(module_ids) == 2
                and all(_positive_int(grade) for grade in participant_grades.values()),
                f"cross-grade integration must connect exactly two dated modules: {contract_id}",
            )
            earlier_module_id, later_module_id = sorted(
                module_ids,
                key=lambda module_id: participant_grades[module_id],
            )
            earlier_contract = module_contracts[earlier_module_id]
            later_contract = module_contracts[later_module_id]
            _require(
                participant_grades[earlier_module_id]
                < participant_grades[later_module_id]
                and earlier_module_id
                in later_contract.get("prerequisiteModuleIds", [])
                and later_module_id
                in earlier_contract.get("revisitModuleIds", [])
                and counted_module_id == later_module_id,
                "cross-grade integration must follow prerequisite and revisit "
                f"semantics and be counted in the later grade: {contract_id}",
            )

        path_ids = contract["pathIds"]
        _require(
            _nonempty_string_list(path_ids) and path_ids,
            f"integration paths must be nonempty and unique: {contract_id}",
        )
        for module_id in module_ids:
            available_path_ids = {
                budget.get("pathId")
                for budget in module_contracts[module_id].get("pathBudgets", [])
                if isinstance(budget, dict)
            }
            _require(
                set(path_ids) <= available_path_ids,
                f"integration references unknown path for module {module_id}: {contract_id}",
            )

        shared_minutes = contract["sharedMinutes"]
        _require(
            _positive_int(shared_minutes),
            f"integration shared minutes must be a positive integer: {contract_id}",
        )
        savings = contract["savingsMinutesByPath"]
        _require(
            isinstance(savings, dict) and set(savings) == set(path_ids),
            f"integration savings paths differ from its paths: {contract_id}",
        )
        _require(
            all(
                _nonnegative_int(minutes) and minutes <= shared_minutes
                for minutes in savings.values()
            ),
            f"integration savings must be non-negative integer minutes: {contract_id}",
        )

        for field in (
            "sharedPhaseOrProduct",
            "risk",
            "fallback",
        ):
            _require(
                isinstance(contract[field], str) and contract[field].strip(),
                f"integration {field} must be a nonempty string: {contract_id}",
            )
        for field in (
            "preservedLearningActions",
            "preservedProductAndCurriculumEvidence",
            "prerequisites",
        ):
            _require(
                _nonempty_string_list(contract[field]) and contract[field],
                f"integration {field} must be nonempty and unique: {contract_id}",
            )
        _require(
            contract["status"] in {"working", "reviewed", "failed"},
            f"invalid integration status: {contract_id}",
        )

        allocation_locations = []
        for module_id, module_contract in module_contracts.items():
            references_contract = contract_id in module_contract.get(
                "integrationContractIds",
                [],
            )
            _require(
                references_contract == (module_id in module_ids),
                f"integration references differ from participants: {contract_id}",
            )
            for budget in module_contract.get("pathBudgets", []):
                path_id = budget.get("pathId")
                allocations = budget.get("sharedAllocations")
                _require(
                    isinstance(allocations, list),
                    f"shared allocations must be a list: {module_id}/{path_id}",
                )
                matching_allocations = [
                    allocation
                    for allocation in allocations
                    if isinstance(allocation, dict)
                    and allocation.get("integrationContractId") == contract_id
                ]
                for allocation in matching_allocations:
                    _require(
                        set(allocation) == {"integrationContractId", "minutes"}
                        and _positive_int(allocation["minutes"])
                        and allocation["minutes"] == shared_minutes,
                        f"invalid shared allocation: {module_id}/{path_id}/{contract_id}",
                    )
                    allocation_locations.append((module_id, path_id))

        expected_locations = {
            (counted_module_id, path_id) for path_id in path_ids
        }
        _require(
            len(allocation_locations) == len(expected_locations)
            and set(allocation_locations) == expected_locations,
            f"shared minutes must be counted exactly once per path: {contract_id}",
        )
        contracts_by_id[contract_id] = contract

    known_integration_ids = set(contracts_by_id)
    for module_id, module_contract in module_contracts.items():
        integration_ids = module_contract.get("integrationContractIds")
        _require(
            _nonempty_string_list(integration_ids),
            f"module integration references must be unique strings: {module_id}",
        )
        _require(
            set(integration_ids) <= known_integration_ids,
            f"module has an unknown integration reference: {module_id}",
        )
        for budget in module_contract.get("pathBudgets", []):
            path_id = budget.get("pathId")
            allocations = budget.get("sharedAllocations")
            _require(
                isinstance(allocations, list),
                f"shared allocations must be a list: {module_id}/{path_id}",
            )
            for allocation in allocations:
                _require(
                    isinstance(allocation, dict)
                    and set(allocation) == {"integrationContractId", "minutes"},
                    f"invalid shared allocation: {module_id}/{path_id}",
                )
                _require(
                    allocation["integrationContractId"] in known_integration_ids,
                    f"unknown shared allocation integration id: {module_id}/{path_id}",
                )

    return contracts_by_id


def validate_annual_variants(
    annual_variants,
    module_contracts,
    integration_contracts,
):
    """Validate annual allocations against module and integration contracts."""
    _require(
        isinstance(module_contracts, dict),
        "validated module contracts must be keyed by module id",
    )
    _require(
        isinstance(integration_contracts, dict),
        "validated integration contracts must be keyed by contract id",
    )
    _require(isinstance(annual_variants, list), "annual variants must be a list")
    variant_fields = {
        "id",
        "grade",
        "kind",
        "pathId",
        "targetUnits",
        "allocations",
        "integrationContractIds",
        "available",
        "status",
        "rationale",
        "risk",
    }
    allocation_fields = {"moduleId", "budgetPathId", "units"}
    variants_by_id = {}
    for variant in annual_variants:
        _require(isinstance(variant, dict), "annual variant must be an object")
        _require(
            set(variant) == variant_fields,
            "annual variant fields differ from the IUM10 contract",
        )
        variant_id = variant["id"]
        _require(
            isinstance(variant_id, str) and variant_id.strip(),
            "annual variant id must be a nonempty string",
        )
        _require(
            variant_id not in variants_by_id,
            "annual variant ids must be unique",
        )
        _require(
            _positive_int(variant["grade"]),
            f"annual variant grade must be a positive integer: {variant_id}",
        )
        _require(
            variant["kind"] in {"planning-path", "demand-scenario"},
            f"invalid annual variant kind: {variant_id}",
        )
        _require(
            isinstance(variant["pathId"], str) and variant["pathId"].strip(),
            f"annual variant path id must be a nonempty string: {variant_id}",
        )
        _require(
            variant["pathId"] in ANNUAL_PATH_IDS_BY_KIND[variant["kind"]],
            f"annual variant uses an unknown {variant['kind']} planning path: {variant_id}",
        )
        _require(
            _positive_int(variant["targetUnits"]),
            f"annual variant target units must be a positive integer: {variant_id}",
        )
        _require(
            isinstance(variant["available"], bool),
            f"annual variant availability must be boolean: {variant_id}",
        )
        _require(
            variant["status"] in {"working", "reviewed"},
            f"invalid annual variant status: {variant_id}",
        )
        for field in ("rationale", "risk"):
            _require(
                isinstance(variant[field], str) and variant[field].strip(),
                f"annual variant {field} must be a nonempty string: {variant_id}",
            )

        integration_ids = variant["integrationContractIds"]
        _require(
            _nonempty_string_list(integration_ids),
            f"annual variant integration ids must be unique strings: {variant_id}",
        )
        _require(
            all(
                integration_id in integration_contracts
                for integration_id in integration_ids
            ),
            f"annual variant references unknown integration: {variant_id}",
        )

        allocations = variant["allocations"]
        _require(
            isinstance(allocations, list) and allocations,
            f"annual variant allocations must be nonempty: {variant_id}",
        )
        allocation_module_ids = set()
        allocated_units = 0
        required_integration_ids = set()
        selected_budget_path_ids = {}
        for allocation in allocations:
            _require(
                isinstance(allocation, dict)
                and set(allocation) == allocation_fields,
                f"annual allocation fields differ from the IUM10 contract: {variant_id}",
            )
            module_id = allocation["moduleId"]
            _require(
                isinstance(module_id, str) and module_id in module_contracts,
                f"annual variant references unknown module: {variant_id}/{module_id}",
            )
            _require(
                module_id not in allocation_module_ids,
                f"annual variant module allocations must be unique: {variant_id}",
            )
            module_contract = module_contracts[module_id]
            _require(
                module_contract.get("grade") == variant["grade"],
                f"annual variant module grade differs: {variant_id}/{module_id}",
            )
            budget_path_id = allocation["budgetPathId"]
            expected_budget_path_id = ANNUAL_VARIANT_BUDGET_PATH_OVERRIDES.get(
                variant_id,
                {},
            ).get(module_id, variant["pathId"])
            _require(
                budget_path_id == expected_budget_path_id,
                "annual allocation budget path differs from variant path: "
                f"{variant_id}/{module_id}",
            )
            matching_budgets = [
                budget
                for budget in module_contract.get("pathBudgets", [])
                if isinstance(budget, dict)
                and budget.get("pathId") == budget_path_id
            ]
            _require(
                len(matching_budgets) == 1,
                f"annual variant references unknown budget path: {variant_id}/{module_id}",
            )
            units = allocation["units"]
            _require(
                _positive_int(units),
                f"annual allocation units must be a positive integer: {variant_id}",
            )
            _require(
                units == matching_budgets[0].get("units"),
                f"annual allocation differs from module budget: {variant_id}/{module_id}",
            )
            selected_budget = matching_budgets[0]
            shared_allocations = selected_budget.get("sharedAllocations", [])
            _require(
                isinstance(shared_allocations, list),
                f"annual allocation shared allocations must be a list: {variant_id}/{module_id}",
            )
            for shared_allocation in shared_allocations:
                _require(
                    isinstance(shared_allocation, dict)
                    and set(shared_allocation)
                    == {"integrationContractId", "minutes"},
                    f"invalid annual shared allocation: {variant_id}/{module_id}",
                )
                integration_id = shared_allocation["integrationContractId"]
                _require(
                    integration_id in integration_contracts,
                    f"annual variant uses unknown shared integration: {variant_id}",
                )
                integration = integration_contracts[integration_id]
                _require(
                    integration.get("countedInModuleId") == module_id
                    and budget_path_id in integration.get("pathIds", []),
                    f"annual shared integration is not applicable: {variant_id}/{integration_id}",
                )
                required_integration_ids.add(integration_id)
            allocation_module_ids.add(module_id)
            selected_budget_path_ids[module_id] = budget_path_id
            allocated_units += units
        _require(
            allocated_units == variant["targetUnits"],
            f"annual allocation sum differs from target units: {variant_id}",
        )
        if variant["kind"] == "planning-path":
            expected_core_module_ids = {
                module_id
                for module_id, module_contract in module_contracts.items()
                if module_contract.get("grade") == variant["grade"]
                and module_contract.get("kind") == "core"
            }
            allocated_core_module_ids = {
                module_id
                for module_id in allocation_module_ids
                if module_contracts[module_id].get("kind") == "core"
            }
            _require(
                allocated_core_module_ids == expected_core_module_ids,
                f"planning variant must retain all core modules: {variant_id}",
            )
            _require(
                all(
                    module_contracts[module_id].get("kind") != "project"
                    for module_id in allocation_module_ids
                ),
                f"normal planning variants must exclude project modules: {variant_id}",
            )
            for module_id in allocation_module_ids:
                module_contract = module_contracts[module_id]
                if module_contract.get("kind") == "core":
                    continue
                same_grade_prerequisites = {
                    prerequisite_id
                    for prerequisite_id in module_contract.get(
                        "prerequisiteModuleIds",
                        [],
                    )
                    if prerequisite_id in module_contracts
                    and module_contracts[prerequisite_id].get("grade")
                    == variant["grade"]
                }
                _require(
                    same_grade_prerequisites <= allocation_module_ids,
                    f"flex allocation omits same-grade prerequisites: {variant_id}/{module_id}",
                )
        for integration_id in required_integration_ids:
            integration = integration_contracts[integration_id]
            participant_grades = {
                module_id: module_contracts[module_id].get("grade")
                for module_id in integration.get("moduleIds", [])
                if module_id in module_contracts
            }
            _require(
                participant_grades
                and max(participant_grades.values()) == variant["grade"]
                and participant_grades.get(integration.get("countedInModuleId"))
                == variant["grade"],
                "annual cross-grade integration must be counted in the "
                f"variant grade: {variant_id}/{integration_id}",
            )
            same_grade_participants = {
                module_id
                for module_id in integration.get("moduleIds", [])
                if module_id in module_contracts
                and module_contracts[module_id].get("grade") == variant["grade"]
            }
            _require(
                same_grade_participants <= allocation_module_ids,
                f"annual variant omits integration participants: {variant_id}/{integration_id}",
            )
            selected_participants = (
                set(integration.get("moduleIds", [])) & allocation_module_ids
            )
            _require(
                all(
                    selected_budget_path_ids[module_id]
                    in integration.get("pathIds", [])
                    for module_id in selected_participants
                ),
                "annual integration participant budget path is unsupported: "
                f"{variant_id}/{integration_id}",
            )
        _require(
            set(integration_ids) == required_integration_ids,
            f"annual variant references differ from required integrations: {variant_id}",
        )
        _require(
            not variant["available"]
            or all(
                integration_contracts[integration_id].get("status") != "failed"
                for integration_id in required_integration_ids
            ),
            f"available annual variant uses a failed integration: {variant_id}",
        )
        variants_by_id[variant_id] = variant

    return variants_by_id


def validate_ium10_baseline(module_payload, coverage_payload, remediation_payload):
    """Validate the immutable IUM09 baseline consumed by IUM10."""
    modules = module_payload.get("modules") if isinstance(module_payload, dict) else None
    _require(isinstance(modules, list), "module payload must contain modules")
    module_ids = {module["id"] for module in modules}
    _require(len(module_ids) == len(modules) == 31, "module ids must be exactly 31 and unique")
    _require(
        module_structure_fingerprint(module_payload) == BASELINE_MODULE_STRUCTURE_SHA256,
        "module structure fingerprint differs from immutable IUM09 baseline",
    )
    _require(
        Counter(module["kind"] for module in modules) == Counter({"core": 24, "extension": 3, "transfer": 2, "project": 2}),
        "module kind counts differ from immutable IUM09 baseline",
    )

    coverage_entries = (
        coverage_payload.get("entries") if isinstance(coverage_payload, dict) else None
    )
    _require(isinstance(coverage_entries, list), "coverage payload must contain entries")
    coverage_ids = {entry["competencyId"] for entry in coverage_entries}
    _require(len(coverage_ids) == len(coverage_entries) == 171, "coverage ids must be exactly 171 and unique")
    _require(
        Counter(entry["coverageStatus"] for entry in coverage_entries)
        == Counter({"covered": 164, "partial": 7}),
        "coverage status counts differ from immutable IUM09 baseline",
    )
    _require(
        coverage_projection_fingerprint(coverage_payload, remediation_payload)
        == BASELINE_COVERAGE_PROJECTION_SHA256,
        "coverage projection fingerprint differs from immutable IUM09 baseline",
    )

    handoff_entries = (
        remediation_payload.get("entries")
        if isinstance(remediation_payload, dict)
        else None
    )
    _require(isinstance(handoff_entries, list), "remediation payload must contain entries")
    handoff_ids = {entry["competencyId"] for entry in handoff_entries}
    _require(len(handoff_ids) == len(handoff_entries) == 60, "handoff ids must be exactly 60 and unique")
    _require(
        Counter(entry["timeImpact"]["level"] for entry in handoff_entries)
        == Counter({"review-required": 56, "roadmap-dependent": 4}),
        "time handoff level counts differ from immutable IUM09 baseline",
    )
    _require(
        {
            entry["competencyId"]
            for entry in handoff_entries
            if entry["timeImpact"]["level"] == "roadmap-dependent"
        }
        == ROADMAP_DEPENDENT_IDS,
        "roadmap-dependent handoff ids differ from immutable IUM09 baseline",
    )
    _require(
        time_handoff_fingerprint(remediation_payload)
        == BASELINE_TIME_HANDOFF_SHA256,
        "time handoff fingerprint differs from immutable IUM09 baseline",
    )

    return {
        "moduleIds": module_ids,
        "coverageIds": coverage_ids,
        "handoffIds": handoff_ids,
    }
