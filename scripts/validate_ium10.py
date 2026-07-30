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
            expected_path_ids = set(CORE_PATH_IDS[contract["grade"]])
            if module_id == "IUM-6-CORE-04":
                expected_path_ids.add("targeted-extension")
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
            expected_path_ids = {"standalone"}

        path_budgets = contract["pathBudgets"]
        _require(isinstance(path_budgets, list), f"path budgets must be a list: {module_id}")
        path_ids = []
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
        _require(
            len(path_ids) == len(set(path_ids)) and set(path_ids) == expected_path_ids,
            f"time contract paths differ from the IUM10 contract: {module_id}",
        )
        contracts_by_module_id[module_id] = contract

    _require(
        set(contracts_by_module_id) == set(modules_by_id),
        "every module needs exactly one time contract",
    )
    return contracts_by_module_id


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
