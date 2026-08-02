import argparse
import copy
import hashlib
import json
import os
import re
import sys
import tempfile
import uuid
from pathlib import Path

if __package__:
    from .ium11_publication import (
        IUM11PublicationError,
        PUBLICATION_PATHS,
        compile_publication_contract,
        extract_publication_block,
        render_publication_contract_json,
        render_publication_markdown_block,
        validate_publication_text_boundary,
    )
    from .validate_ium10 import (
        IUM10ValidationError,
        PHASE_IDS,
        validate_ium10_repository,
    )
else:
    from ium11_publication import (
        IUM11PublicationError,
        PUBLICATION_PATHS,
        compile_publication_contract,
        extract_publication_block,
        render_publication_contract_json,
        render_publication_markdown_block,
        validate_publication_text_boundary,
    )
    from validate_ium10 import IUM10ValidationError, PHASE_IDS, validate_ium10_repository


TIME_MODEL_FINGERPRINT = "873774e52b6c9a20e08e5079c898a014493a39305be5efa35a601248ff36a2c1"
PROTOCOL_FIELDS = {
    "schemaVersion", "id", "status", "protocolVersion", "toolVersion",
    "timeModelFingerprintAlgorithm", "timeModelFingerprint", "variantId",
    "availabilityContractId", "allowedRecommendation",
    "forbiddenRecommendations", "minimumLearnerResponses",
    "learnerWarningRatio", "bands", "results", "prohibitedFieldNames",
    "evidenceTracks", "learnerPulseItems", "contextEnums", "clusters",
    "annualPilot",
}
CLUSTER_FIELDS = {
    "id", "order", "pilotAssignmentId", "integrationContractId", "moduleIds",
    "modulePilotAssignmentIds", "budgetUnits", "fallbackDeltaUnits",
    "handoffCriterionId",
}
ANNUAL_PILOT_FIELDS = {
    "id", "pilotAssignmentId", "variantId", "clusterIds", "budgetUnits",
}
CLUSTER_BINDINGS = [
    ("CLUSTER-7-DATA-CODING", "PILOT-INT-7-DATA-CODING", "INT-7-DATA-CODING", ["IUM-7-CORE-01", "IUM-7-CORE-02"], 8, 3),
    ("CLUSTER-7-PROGRAMMING", "PILOT-INT-7-PROGRAMMING", "INT-7-PROGRAMMING", ["IUM-7-CORE-03", "IUM-7-CORE-04"], 11, 2),
    ("CLUSTER-7-NET-SECURITY", "PILOT-INT-7-NET-SECURITY", "INT-7-NET-SECURITY", ["IUM-7-CORE-05", "IUM-7-CORE-06", "IUM-7-CORE-07"], 11, 3),
    ("CLUSTER-7-DATA-MEDIA-SOCIETY", "PILOT-INT-7-DATA-MEDIA-SOCIETY", "INT-7-DATA-MEDIA-SOCIETY", ["IUM-7-CORE-08", "IUM-7-CORE-09", "IUM-7-CORE-10"], 10, 6),
]
CORE_MODULE_IDS = [f"IUM-7-CORE-{number:02d}" for number in range(1, 11)]
PROHIBITED_FIELD_NAMES = [
    "studentName", "studentInitials", "schoolName", "teacherName", "className",
    "courseName", "email", "accountId", "learnerId", "lessonDate", "timetable",
    "freeText", "studentProduct", "studentProductUrl", "filePath", "screenshot",
    "photo", "audio", "video", "individualResponse", "responseSequence", "deviceId",
    "networkId", "browserId", "ipAddress", "telemetry", "privateReflection", "grade",
    "ranking", "competenceProfile", "automatedPersonalAssessment",
]
EVIDENCE_PACKAGE_FIELDS = {
    "schemaVersion", "packageType", "packageId", "protocolVersion",
    "protocolFingerprint", "toolVersion", "timeModelFingerprint", "scopeType",
    "scopeId", "context", "deliveryTimeEvidence", "learningQualityEvidence",
    "learnerPulseEvidence", "technicalPrivacyEvidence", "result",
    "developmentWarnings", "retentionClass",
}
CONTEXT_FIELDS = {
    "schoolYear", "term", "classSizeBand", "deviceClass", "browserFamily",
    "networkMode",
}
DELIVERY_FIELDS = {
    "plannedUnits", "actualUnits", "completedPhaseIds",
    "requiredLearningPhasesCompleted", "fallbackActivated",
    "technicalStartupMinutes", "supportDemandBand", "externalDisruptionCode",
}
ANNUAL_DELIVERY_FIELDS = DELIVERY_FIELDS | {"clusterOrder", "clusterActualUnits"}
LEARNING_QUALITY_FIELDS = {"moduleResults", "integrationResults"}
MODULE_RESULT_FIELDS = {"pilotAssignmentId", "moduleId", "criteria", "result"}
INTEGRATION_RESULT_FIELDS = {
    "pilotAssignmentId", "integrationContractId", "criteria",
    "handoffProductPresent", "handoffReused", "result",
}
CRITERION_FIELDS = {"criterionId", "band"}
PULSE_ITEM_FIELDS = {"itemId", "agree", "partly", "disagree", "noAnswer"}
TECHNICAL_PRIVACY_FIELDS = {
    "technicalFunction", "fallbackEquivalentLearningFunction", "problemCode",
    "severity", "privacyGate",
}
WARNING_FIELDS = {"id", "itemId", "status"}
PACKAGE_ID_PATTERN = re.compile(
    r"PKG-[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
)
FINGERPRINT_PATTERN = re.compile(r"[0-9a-f]{64}")
SCHOOL_YEAR_PATTERN = re.compile(r"[0-9]{4}-[0-9]{2}")
DECISION_PACKAGE_ID_PATTERN = re.compile(
    r"PKG-[0-9a-f]{8}-[0-9a-f]{4}-5[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
)
DECISION_PACKAGE_FIELDS = {
    "schemaVersion", "packageType", "packageId", "protocolVersion",
    "protocolFingerprint", "toolVersion", "timeModelFingerprint",
    "sourcePackageIds", "pilotResults", "moduleResults",
    "integrationResults", "availabilityGateResults",
    "timeAndFallbackSummary", "technicalPrivacySummary",
    "developmentWarnings", "statementBoundary", "recommendation",
    "reviewStatus", "retentionClass",
}
DECISION_PILOT_RESULT_FIELDS = {"scopeId", "packageId", "result"}
DECISION_MODULE_RESULT_FIELDS = {"moduleId", "pilotAssignmentId", "result"}
DECISION_INTEGRATION_RESULT_FIELDS = {
    "integrationContractId", "pilotAssignmentId", "result",
    "fallbackDeltaUnits",
}
AVAILABILITY_GATE_FIELDS = {
    "capacity", "integration", "technical", "privacy", "pilot",
}
TIME_FALLBACK_SUMMARY_FIELDS = {
    "plannedUnits", "actualUnits", "fallbackUnits", "requiredUnits",
}
TECHNICAL_PRIVACY_SUMMARY_FIELDS = {"technical", "privacy"}
REVIEW_STATUS_FIELDS = {"fach", "engineeringPrivacy", "commissioner"}
DECISION_NAMESPACE = uuid.UUID("32f31164-80d6-5ac9-851f-7579346166e5")
SYNTHETIC_EXAMPLE_NAMES = {
    "synthetic-cluster-pass.json",
    "synthetic-cluster-programming-pass.json",
    "synthetic-cluster-net-security-pass.json",
    "synthetic-cluster-data-media-society-pass.json",
    "synthetic-cluster-fail.json",
    "synthetic-annual-pass.json",
    "synthetic-decision-eligible.json",
}
SYNTHETIC_POSITIVE_EXAMPLE_NAMES = (
    "synthetic-cluster-pass.json",
    "synthetic-cluster-programming-pass.json",
    "synthetic-cluster-net-security-pass.json",
    "synthetic-cluster-data-media-society-pass.json",
    "synthetic-annual-pass.json",
)
SYNTHETIC_DECISION_NAME = "synthetic-decision-eligible.json"
PUBLICATION_PRODUCT_PATHS = (
    "README.md",
    "pilot/pilot-protocol.json",
    "pilot/docs/publication-contract.json",
    "pilot/schemas/evidence-package.schema.json",
    "pilot/schemas/decision-package.schema.json",
    "pilot/cockpit/index.html",
    "pilot/cockpit/assets/styles.css",
    "pilot/cockpit/assets/app.js",
    "pilot/cockpit/assets/protocol.js",
    "pilot/docs/teacher-guide.md",
    "pilot/docs/review-guide.md",
    *tuple(f"pilot/examples/{name}" for name in sorted(SYNTHETIC_EXAMPLE_NAMES)),
    "scripts/ium11_publication.py",
    "scripts/build_ium11_publication_contract.py",
    "scripts/validate_ium11.py",
    "scripts/build_ium11_cockpit.py",
    "scripts/validate_phase0.py",
    "tests/test_validate_ium11.py",
    "tests/test_ium11_publication_contract.py",
    "tests/test_ium11_cockpit_contract.py",
    "tests/test_validate_phase0.py",
)


class IUM11ValidationError(ValueError):
    pass


def canonical_sha256(payload: object) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise IUM11ValidationError(message)


def _require_exact_fields(payload: dict, fields: set[str], label: str) -> None:
    _require(isinstance(payload, dict), f"{label} must be an object")
    _require(set(payload) == fields, f"{label} fields differ from contract")


def _load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _index_by_id(records: object, label: str) -> dict:
    _require(isinstance(records, list), f"{label} must be a list")
    indexed = {record.get("id"): record for record in records if isinstance(record, dict)}
    _require(len(indexed) == len(records) and None not in indexed, f"{label} IDs must be unique")
    return indexed


def _working_40_phase_ids(module_contract: dict) -> list[str]:
    paths = module_contract.get("pathBudgets")
    _require(isinstance(paths, list), "module contract pathBudgets must be a list")
    matches = [path for path in paths if isinstance(path, dict) and path.get("pathId") == "working-40"]
    _require(len(matches) == 1, "module contract must contain one working-40 budget")
    phase_budgets = matches[0].get("phaseBudgets")
    _require(isinstance(phase_budgets, list), "working-40 phaseBudgets must be a list")
    phase_ids = [phase.get("phaseId") for phase in phase_budgets if isinstance(phase, dict)]
    _require(len(phase_ids) == len(phase_budgets), "working-40 phases must be objects")
    _require(phase_ids == list(PHASE_IDS), "working-40 phases differ from contract")
    return phase_ids


def _validate_protocol_constants(protocol: dict, time_model: dict) -> None:
    _require(protocol["schemaVersion"] == 1, "protocol schemaVersion must be 1")
    _require(protocol["id"] == "IUM11-GRADE-7-WORKING-40-PILOT", "protocol ID differs from contract")
    _require(protocol["status"] == "working", "protocol status must remain working")
    _require(protocol["protocolVersion"] == "1.0.0", "protocolVersion differs from contract")
    _require(protocol["toolVersion"] == "1.0.0", "toolVersion differs from contract")
    _require(protocol["timeModelFingerprintAlgorithm"] == "sha256-canonical-json-v1", "unsupported time-model fingerprint algorithm")
    _require(canonical_sha256(time_model) == TIME_MODEL_FINGERPRINT, "time model fingerprint differs from pinned contract")
    _require(protocol["timeModelFingerprint"] == TIME_MODEL_FINGERPRINT, "protocol time model fingerprint differs from contract")
    _require(protocol["variantId"] == "GRADE-7-WORKING-40", "protocol variant differs from contract")
    _require(protocol["availabilityContractId"] == "AVAIL-GRADE-7-WORKING-40", "protocol availability contract differs from contract")
    _require(protocol["allowedRecommendation"] == "eligible-for-working-availability-review", "allowed recommendation differs from contract")
    _require(protocol["forbiddenRecommendations"] == ["reviewed", "standard"], "forbidden recommendations differ from contract")
    _require(protocol["minimumLearnerResponses"] == 10, "minimum learner responses differs from contract")
    _require(protocol["learnerWarningRatio"] == {"numerator": 1, "denominator": 3}, "learner warning ratio differs from contract")
    _require(protocol["bands"] == ["strong", "mixed", "weak"], "bands differ from contract")
    _require(protocol["results"] == ["pass", "fail", "not-evaluable"], "results differ from contract")
    _require(protocol["prohibitedFieldNames"] == PROHIBITED_FIELD_NAMES, "prohibited field names differ from contract")
    _require(protocol["evidenceTracks"] == ["deliveryTimeEvidence", "learningQualityEvidence", "learnerPulseEvidence", "technicalPrivacyEvidence"], "evidence tracks differ from contract")
    _require(protocol["learnerPulseItems"] == [
        {"id": "clarity", "prompt": "Ich wusste, was ich fachlich bearbeiten sollte."},
        {"id": "cognitiveEngagement", "prompt": "Ich musste erklären, prüfen, testen oder begründen – nicht nur klicken oder abschreiben."},
        {"id": "supportUsefulness", "prompt": "Die Hilfen halfen mir weiter, ohne die Lösung vorzugeben."},
    ], "learner pulse items differ from contract")
    _require(protocol["contextEnums"] == {
        "term": ["first-half", "second-half", "full-year"],
        "classSizeBand": ["under-10", "10-19", "20-29", "30-plus"],
        "deviceClass": ["desktop", "laptop", "tablet", "mixed"],
        "browserFamily": ["chromium", "firefox", "safari", "mixed"],
        "networkMode": ["offline", "school-network", "local-fallback"],
    }, "context enums differ from contract")


def validate_pilot_protocol(protocol: dict, time_model: dict) -> dict:
    _require_exact_fields(protocol, PROTOCOL_FIELDS, "pilot protocol")
    _require(isinstance(time_model, dict), "time model must be an object")
    _validate_protocol_constants(protocol, time_model)

    modules_by_id = {
        contract.get("moduleId"): contract
        for contract in time_model.get("moduleContracts", [])
        if isinstance(contract, dict)
    }
    integrations_by_id = _index_by_id(time_model.get("integrationContracts"), "integration contracts")
    pilots_by_id = _index_by_id(time_model.get("pilotAssignments"), "pilot assignments")
    variants_by_id = _index_by_id(time_model.get("annualVariants"), "annual variants")
    availability_by_id = _index_by_id(time_model.get("availabilityContracts"), "availability contracts")

    clusters = protocol["clusters"]
    _require(isinstance(clusters, list) and len(clusters) == 4, "protocol requires four clusters")
    compiled_clusters = []
    seen_modules = []
    expected_pilot_ids = set()
    for order, (cluster, binding) in enumerate(zip(clusters, CLUSTER_BINDINGS), start=1):
        _require_exact_fields(cluster, CLUSTER_FIELDS, f"cluster {order}")
        cluster_id, pilot_id, integration_id, module_ids, budget_units, fallback_units = binding
        _require(cluster["id"] == cluster_id and cluster["order"] == order, "cluster sequence differs from contract")
        _require(cluster["pilotAssignmentId"] == pilot_id, "cluster pilot assignment differs from contract")
        _require(cluster["integrationContractId"] == integration_id, "cluster integration differs from contract")
        _require(cluster["moduleIds"] == module_ids, "cluster module IDs differ from contract")
        _require(cluster["modulePilotAssignmentIds"] == [f"PILOT-{module_id}" for module_id in module_ids], "cluster module pilot assignments differ from contract")
        _require(cluster["budgetUnits"] == budget_units, "cluster budget differs from contract")
        _require(cluster["fallbackDeltaUnits"] == fallback_units, "cluster fallback differs from contract")
        _require(cluster["handoffCriterionId"] == "handoffProductPresent", "cluster handoff criterion differs from contract")

        integration = integrations_by_id.get(integration_id)
        _require(isinstance(integration, dict) and integration.get("moduleIds") == module_ids, "integration contract differs from cluster binding")
        _require(integration.get("pathIds") == ["working-40", "robust"], "integration paths differ from contract")
        _require(all(isinstance(integration.get(field), list) and integration[field] for field in ("preservedLearningActions", "preservedProductAndCurriculumEvidence")), "integration handoff evidence is incomplete")
        pilot = pilots_by_id.get(pilot_id)
        _require(isinstance(pilot, dict) and pilot.get("scopeType") == "integration" and pilot.get("scopeIds") == [integration_id] and pilot.get("contractIds") == [integration_id], "integration pilot assignment differs from contract")
        _require(cluster["handoffCriterionId"] in pilot.get("measures", []), "integration pilot lacks handoff measure")
        expected_pilot_ids.add(pilot_id)

        compiled_modules = []
        for module_id, module_pilot_id in zip(module_ids, cluster["modulePilotAssignmentIds"]):
            module = modules_by_id.get(module_id)
            _require(isinstance(module, dict) and module.get("grade") == 7 and module.get("kind") == "core", "cluster module differs from Grade 7 core contract")
            _require(all(isinstance(module.get(field), str) and module[field] for field in ("centralLearningAction", "centralLearningProduct")), "module learning references are incomplete")
            required_phase_ids = _working_40_phase_ids(module)
            module_pilot = pilots_by_id.get(module_pilot_id)
            _require(isinstance(module_pilot, dict) and module_pilot.get("scopeType") == "module" and module_pilot.get("scopeIds") == [module_id] and module_pilot.get("contractIds") == [module.get("id")], "module pilot assignment differs from contract")
            expected_pilot_ids.add(module_pilot_id)
            seen_modules.append(module_id)
            compiled_modules.append({
                "moduleId": module_id,
                "pilotAssignmentId": module_pilot_id,
                "requiredPhaseIds": required_phase_ids,
                "criteria": [
                    {"criterionId": f"CRIT-{module_id}-ACTION", "sourceField": "centralLearningAction", "kind": "must"},
                    {"criterionId": f"CRIT-{module_id}-PRODUCT", "sourceField": "centralLearningProduct", "kind": "must"},
                ],
            })
        compiled_cluster = copy.deepcopy(cluster)
        compiled_cluster["modules"] = compiled_modules
        compiled_cluster["integration"] = {
            "integrationContractId": integration_id,
            "pilotAssignmentId": pilot_id,
            "criteria": [
                {"criterionId": f"CRIT-{integration_id}-HANDOFF-ACTIONS", "sourceField": "preservedLearningActions", "kind": "must"},
                {"criterionId": f"CRIT-{integration_id}-HANDOFF-EVIDENCE", "sourceField": "preservedProductAndCurriculumEvidence", "kind": "must"},
            ],
        }
        compiled_clusters.append(compiled_cluster)

    _require(seen_modules == CORE_MODULE_IDS, "protocol must bind each Grade 7 core module exactly once")
    annual_pilot = protocol["annualPilot"]
    _require_exact_fields(annual_pilot, ANNUAL_PILOT_FIELDS, "annual pilot")
    _require(annual_pilot == {
        "id": "ANNUAL-7-WORKING-40",
        "pilotAssignmentId": "PILOT-GRADE-7-WORKING-40",
        "variantId": "GRADE-7-WORKING-40",
        "clusterIds": [binding[0] for binding in CLUSTER_BINDINGS],
        "budgetUnits": 40,
    }, "annual pilot differs from contract")
    annual_assignment = pilots_by_id.get(annual_pilot["pilotAssignmentId"])
    _require(isinstance(annual_assignment, dict) and annual_assignment.get("scopeType") == "annual-variant" and annual_assignment.get("scopeIds") == [annual_pilot["variantId"]] and annual_assignment.get("contractIds") == [protocol["availabilityContractId"]], "annual pilot assignment differs from contract")
    expected_pilot_ids.add(annual_pilot["pilotAssignmentId"])
    _require(len(expected_pilot_ids) == 15, "protocol requires fifteen distinct pilot assignments")
    _require(all(pilot_id in pilots_by_id for pilot_id in expected_pilot_ids), "protocol references a missing pilot assignment")

    variant = variants_by_id.get(protocol["variantId"])
    _require(isinstance(variant, dict) and variant.get("targetUnits") == annual_pilot["budgetUnits"] and variant.get("integrationContractIds") == [binding[2] for binding in CLUSTER_BINDINGS], "annual variant differs from protocol binding")
    availability = availability_by_id.get(protocol["availabilityContractId"])
    _require(isinstance(availability, dict) and availability.get("variantId") == protocol["variantId"] and availability.get("requiredCapacityUnits") == annual_pilot["budgetUnits"], "availability contract differs from protocol binding")
    _require(availability.get("fallbackDeltaUnitsByIntegrationContractId") == {binding[2]: binding[5] for binding in CLUSTER_BINDINGS}, "availability fallback deltas differ from protocol")

    compiled = copy.deepcopy(protocol)
    compiled["clusters"] = compiled_clusters
    compiled["clustersById"] = {cluster["id"]: cluster for cluster in compiled_clusters}
    compiled["protocolFingerprint"] = canonical_sha256(protocol)
    return compiled


def _require_int(value: object, label: str, minimum: int = 0) -> None:
    _require(type(value) is int and value >= minimum, f"{label} must be an integer of at least {minimum}")


def _require_bool(value: object, label: str) -> None:
    _require(type(value) is bool, f"{label} must be a boolean")


def _require_enum(value: object, values: list[str], label: str) -> None:
    _require(isinstance(value, str) and value in values, f"{label} is invalid")


def _validate_criteria(criteria: object, expected: list[dict], label: str, protocol: dict) -> None:
    _require(isinstance(criteria, list) and len(criteria) == len(expected), f"{label} criteria differ from contract")
    for criterion, expected_criterion in zip(criteria, expected, strict=True):
        _require_exact_fields(criterion, CRITERION_FIELDS, f"{label} criterion")
        _require(criterion["criterionId"] == expected_criterion["criterionId"], f"{label} criterion IDs differ from contract")
        _require_enum(criterion["band"], protocol["bands"], f"{label} criterion band")


def evaluate_learner_pulse(payload: dict, protocol: dict) -> dict:
    if payload == {"status": "suppressed-small-group"}:
        return {"status": "suppressed-small-group", "warnings": []}
    _require_exact_fields(payload, {"status", "classResponseCount", "items"}, "learner pulse")
    _require(payload["status"] == "reported", "learner pulse status is invalid")
    _require_int(payload["classResponseCount"], "classResponseCount", protocol["minimumLearnerResponses"])
    items = payload["items"]
    expected_ids = [item["id"] for item in protocol["learnerPulseItems"]]
    _require(isinstance(items, list) and len(items) == len(expected_ids), "learner pulse items differ from contract")
    warnings = []
    for expected_id, item in zip(expected_ids, items, strict=True):
        _require_exact_fields(item, PULSE_ITEM_FIELDS, "learner pulse item")
        _require(item["itemId"] == expected_id, "learner pulse item order differs")
        for field in ("agree", "partly", "disagree", "noAnswer"):
            _require_int(item[field], f"learner pulse {field}")
        total = item["agree"] + item["partly"] + item["disagree"] + item["noAnswer"]
        valid = item["agree"] + item["partly"] + item["disagree"]
        _require(total == payload["classResponseCount"], "learner pulse sums differ")
        _require(valid >= protocol["minimumLearnerResponses"], "reported learner pulse item has fewer than 10 valid responses")
        ratio = protocol["learnerWarningRatio"]
        if item["disagree"] * ratio["denominator"] >= valid * ratio["numerator"]:
            warnings.append({"id": f"WARN-{expected_id}", "itemId": expected_id, "status": "open"})
    return {"status": "reported", "warnings": warnings}


def _derive_module_results_for_modules(payload: dict, modules: list[dict]) -> list[dict]:
    evidence_by_module_id = {
        item["moduleId"]
        for item in payload["learningQualityEvidence"]["moduleResults"]
    }
    _require(
        evidence_by_module_id == {module["moduleId"] for module in modules},
        "module results differ from contract",
    )
    results = []
    for module, evidence in zip(
        modules, payload["learningQualityEvidence"]["moduleResults"], strict=True
    ):
        _require(evidence["moduleId"] == module["moduleId"], "module result order differs from contract")
        results.append({
            "pilotAssignmentId": module["pilotAssignmentId"],
            "moduleId": module["moduleId"],
            "criteria": copy.deepcopy(evidence["criteria"]),
            "result": "pass" if all(
                criterion["band"] == "strong" for criterion in evidence["criteria"]
            ) else "fail",
        })
    return results


def _derive_module_results(payload: dict, cluster: dict) -> list[dict]:
    return _derive_module_results_for_modules(payload, cluster["modules"])


def _derive_integration_results_for_contracts(
    payload: dict,
    integrations: list[dict],
) -> list[dict]:
    evidence = payload["learningQualityEvidence"]["integrationResults"]
    _require(
        isinstance(evidence, list) and len(evidence) == len(integrations),
        "integration results differ from contract",
    )
    results = []
    for item, integration in zip(evidence, integrations, strict=True):
        _require(
            item["integrationContractId"] == integration["integrationContractId"],
            "integration result differs from contract",
        )
        passed = (
            all(criterion["band"] == "strong" for criterion in item["criteria"])
            and item["handoffProductPresent"]
            and item["handoffReused"]
        )
        results.append({
            "pilotAssignmentId": integration["pilotAssignmentId"],
            "integrationContractId": integration["integrationContractId"],
            "criteria": copy.deepcopy(item["criteria"]),
            "handoffProductPresent": item["handoffProductPresent"],
            "handoffReused": item["handoffReused"],
            "result": "pass" if passed else "fail",
        })
    return results


def _derive_integration_result(payload: dict, cluster: dict) -> dict:
    return _derive_integration_results_for_contracts(
        payload, [cluster["integration"]]
    )[0]


def _cluster_required_phases_completed(payload: dict, cluster: dict) -> bool:
    expected_phase_ids = sorted({
        phase_id
        for module in cluster["modules"]
        for phase_id in module["requiredPhaseIds"]
    })
    delivery = payload["deliveryTimeEvidence"]
    return (
        delivery["requiredLearningPhasesCompleted"] is True
        and delivery["completedPhaseIds"] == expected_phase_ids
    )


def derive_cluster_result(payload: dict, cluster: dict, protocol: dict) -> dict:
    delivery = payload["deliveryTimeEvidence"]
    technical_privacy = payload["technicalPrivacyEvidence"]
    not_evaluable = delivery["externalDisruptionCode"] == "interpretability-lost"
    module_results = _derive_module_results(payload, cluster)
    integration_result = _derive_integration_result(payload, cluster)
    pulse = evaluate_learner_pulse(payload["learnerPulseEvidence"], protocol)
    technical_path_passed = (
        technical_privacy["technicalFunction"] == "pass"
        or (
            delivery["fallbackActivated"]
            and technical_privacy["fallbackEquivalentLearningFunction"]
        )
    )
    failed = any([
        delivery["actualUnits"] > cluster["budgetUnits"],
        not _cluster_required_phases_completed(payload, cluster),
        any(item["result"] != "pass" for item in module_results),
        integration_result["result"] != "pass",
        not technical_path_passed,
        technical_privacy["privacyGate"] != "pass",
        bool(pulse["warnings"]),
    ])
    result = "not-evaluable" if not_evaluable else "fail" if failed else "pass"
    return {
        "result": result,
        "moduleResults": module_results,
        "integrationResult": integration_result,
        "developmentWarnings": pulse["warnings"],
        "fallbackDeltaUnits": cluster["fallbackDeltaUnits"] if result == "fail" else 0,
    }


def _validate_context(context: object, protocol: dict) -> None:
    _require_exact_fields(context, CONTEXT_FIELDS, "context")
    _require(isinstance(context["schoolYear"], str) and SCHOOL_YEAR_PATTERN.fullmatch(context["schoolYear"]), "schoolYear is invalid")
    for field, values in protocol["contextEnums"].items():
        _require_enum(context[field], values, f"context {field}")


def _validate_delivery_time(payload: object, scope: dict, is_annual: bool) -> None:
    expected_fields = ANNUAL_DELIVERY_FIELDS if is_annual else DELIVERY_FIELDS
    _require_exact_fields(payload, expected_fields, "delivery time evidence")
    for field in ("plannedUnits", "actualUnits", "technicalStartupMinutes"):
        _require_int(payload[field], field)
    _require(payload["plannedUnits"] == scope["budgetUnits"], "plannedUnits differs from scope budget")
    _require(isinstance(payload["completedPhaseIds"], list), "completedPhaseIds must be a list")
    _require(all(isinstance(phase_id, str) for phase_id in payload["completedPhaseIds"]), "completedPhaseIds must contain strings")
    _require(payload["completedPhaseIds"] == sorted(set(payload["completedPhaseIds"])), "completedPhaseIds must be sorted and unique")
    _require_bool(payload["requiredLearningPhasesCompleted"], "requiredLearningPhasesCompleted")
    _require_bool(payload["fallbackActivated"], "fallbackActivated")
    _require_enum(payload["supportDemandBand"], ["low", "medium", "high"], "supportDemandBand")
    _require_enum(payload["externalDisruptionCode"], ["none", "interpretability-lost"], "externalDisruptionCode")
    if is_annual:
        cluster_ids = scope["clusterIds"]
        _require(payload["clusterOrder"] == cluster_ids, "annual cluster order differs from contract")
        cluster_actual_units = payload["clusterActualUnits"]
        _require(isinstance(cluster_actual_units, list) and len(cluster_actual_units) == len(cluster_ids), "annual cluster actual units differ from contract")
        for cluster_id, record in zip(cluster_ids, cluster_actual_units, strict=True):
            _require_exact_fields(record, {"clusterId", "actualUnits"}, "annual cluster actual units")
            _require(record["clusterId"] == cluster_id, "annual cluster actual unit order differs")
            _require_int(record["actualUnits"], "annual cluster actualUnits")
        _require(payload["actualUnits"] == sum(record["actualUnits"] for record in cluster_actual_units), "annual actualUnits sum differs")


def _validate_learning_quality(payload: object, modules: list[dict], integrations: list[dict], protocol: dict) -> None:
    _require_exact_fields(payload, LEARNING_QUALITY_FIELDS, "learning quality evidence")
    module_results = payload["moduleResults"]
    _require(isinstance(module_results, list) and len(module_results) == len(modules), "module results differ from contract")
    for result, expected in zip(module_results, modules, strict=True):
        _require_exact_fields(result, MODULE_RESULT_FIELDS, "module result")
        _require(result["pilotAssignmentId"] == expected["pilotAssignmentId"], "module pilot assignment differs from contract")
        _require(result["moduleId"] == expected["moduleId"], "module ID differs from contract")
        _validate_criteria(result["criteria"], expected["criteria"], "module", protocol)
        _require_enum(result["result"], protocol["results"], "module result")
    integration_results = payload["integrationResults"]
    _require(isinstance(integration_results, list) and len(integration_results) == len(integrations), "integration results differ from contract")
    for result, expected in zip(integration_results, integrations, strict=True):
        _require_exact_fields(result, INTEGRATION_RESULT_FIELDS, "integration result")
        _require(result["pilotAssignmentId"] == expected["pilotAssignmentId"], "integration pilot assignment differs from contract")
        _require(result["integrationContractId"] == expected["integrationContractId"], "integration contract differs from contract")
        _validate_criteria(result["criteria"], expected["criteria"], "integration", protocol)
        _require_bool(result["handoffProductPresent"], "handoffProductPresent")
        _require_bool(result["handoffReused"], "handoffReused")
        _require_enum(result["result"], protocol["results"], "integration result")


def _validate_technical_privacy(payload: object) -> None:
    _require_exact_fields(payload, TECHNICAL_PRIVACY_FIELDS, "technical privacy evidence")
    _require_enum(payload["technicalFunction"], ["pass", "fail"], "technicalFunction")
    _require_bool(payload["fallbackEquivalentLearningFunction"], "fallbackEquivalentLearningFunction")
    _require_enum(payload["problemCode"], ["none", "startup", "execution", "import", "export"], "problemCode")
    _require_enum(payload["severity"], ["none", "minor", "major", "blocking"], "severity")
    _require(payload["privacyGate"] == "pass", "privacyGate fail cannot be exported")


def _validate_development_warnings(payload: object, warnings: list[dict]) -> None:
    _require(isinstance(payload, list), "developmentWarnings must be a list")
    for warning in payload:
        _require_exact_fields(warning, WARNING_FIELDS, "development warning")
        _require(warning["id"] == f"WARN-{warning['itemId']}", "development warning ID is invalid")
        _require(warning["status"] == "open", "development warning status is invalid")
    _require(payload == warnings, "developmentWarnings differ from learner pulse warnings")


def _validate_evidence_package_contract(payload: dict, protocol: dict) -> dict:
    _require_exact_fields(payload, EVIDENCE_PACKAGE_FIELDS, "evidence package")
    _require(type(payload["schemaVersion"]) is int and payload["schemaVersion"] == 1, "package schemaVersion must be 1")
    _require(isinstance(payload["packageId"], str) and PACKAGE_ID_PATTERN.fullmatch(payload["packageId"]), "packageId is invalid")
    _require(isinstance(payload["packageType"], str), "packageType must be a string")
    _require(isinstance(payload["scopeType"], str), "scopeType must be a string")
    _require(isinstance(payload["scopeId"], str), "scopeId must be a string")
    for field in ("protocolFingerprint", "timeModelFingerprint"):
        _require(isinstance(payload[field], str) and FINGERPRINT_PATTERN.fullmatch(payload[field]), f"{field} is invalid")
    _require(payload["protocolVersion"] == protocol["protocolVersion"] == "1.0.0", "protocolVersion differs from contract")
    _require(payload["toolVersion"] == protocol["toolVersion"] == "1.0.0", "toolVersion differs from contract")
    _require(payload["protocolFingerprint"] == protocol["protocolFingerprint"], "protocolFingerprint differs from contract")
    _require(payload["timeModelFingerprint"] == protocol["timeModelFingerprint"], "timeModelFingerprint differs from contract")
    _require(payload["retentionClass"] == "until-decision", "retentionClass differs from contract")
    _require_enum(payload["result"], protocol["results"], "package result")
    _validate_context(payload["context"], protocol)

    is_cluster = payload["packageType"] == "cluster-evidence" and payload["scopeType"] == "cluster"
    is_annual = payload["packageType"] == "annual-evidence" and payload["scopeType"] == "annual"
    _require(is_cluster or is_annual, "package type and scope type differ")
    if is_cluster:
        _require(payload["scopeId"] in protocol["clustersById"], "cluster scopeId differs from contract")
        scope = protocol["clustersById"][payload["scopeId"]]
        modules = scope["modules"]
        integrations = [scope["integration"]]
        expected_phase_ids = sorted({phase_id for module in modules for phase_id in module["requiredPhaseIds"]})
    else:
        scope = protocol["annualPilot"]
        _require(payload["scopeId"] == scope["id"], "annual scopeId differs from contract")
        clusters = [protocol["clustersById"][cluster_id] for cluster_id in scope["clusterIds"]]
        modules = [module for cluster in clusters for module in cluster["modules"]]
        integrations = [cluster["integration"] for cluster in clusters]
        expected_phase_ids = sorted({phase_id for module in modules for phase_id in module["requiredPhaseIds"]})

    _validate_delivery_time(payload["deliveryTimeEvidence"], scope, is_annual)
    delivery = payload["deliveryTimeEvidence"]
    _require(delivery["completedPhaseIds"] == expected_phase_ids, "completedPhaseIds differ from required learning phases")
    _require(delivery["requiredLearningPhasesCompleted"] is True, "required learning phases must be complete")
    _validate_learning_quality(payload["learningQualityEvidence"], modules, integrations, protocol)
    learner_pulse = evaluate_learner_pulse(payload["learnerPulseEvidence"], protocol)
    _validate_technical_privacy(payload["technicalPrivacyEvidence"])
    _validate_development_warnings(payload["developmentWarnings"], learner_pulse["warnings"])
    if is_cluster:
        derived = derive_cluster_result(payload, scope, protocol)
        _require(
            payload["learningQualityEvidence"]["moduleResults"] == derived["moduleResults"],
            "module results differ from derived evidence",
        )
        _require(
            payload["learningQualityEvidence"]["integrationResults"]
            == [derived["integrationResult"]],
            "integration results differ from derived evidence",
        )
        _require(
            payload["result"] == derived["result"],
            "cluster budget or result differs from derived evidence",
        )
    else:
        derived = _derive_annual_evidence_result(payload, protocol)
        _require(
            payload["learningQualityEvidence"]["moduleResults"] == derived["moduleResults"],
            "annual module results differ from derived evidence",
        )
        _require(
            payload["learningQualityEvidence"]["integrationResults"]
            == derived["integrationResults"],
            "annual integration results differ from derived evidence",
        )
        _require(payload["result"] == derived["result"], "annual result differs from derived evidence")
    return copy.deepcopy(payload)


def validate_evidence_package(payload: dict, protocol: dict, time_model: dict) -> dict:
    _require(
        canonical_sha256(time_model) == protocol["timeModelFingerprint"],
        "time model differs from compiled protocol",
    )
    return _validate_evidence_package_contract(payload, protocol)


def _technical_path_passed(payload: dict) -> bool:
    delivery = payload["deliveryTimeEvidence"]
    technical_privacy = payload["technicalPrivacyEvidence"]
    return (
        technical_privacy["technicalFunction"] == "pass"
        or (
            delivery["fallbackActivated"]
            and technical_privacy["fallbackEquivalentLearningFunction"]
        )
    )


def _derive_annual_evidence_result(annual_payload: dict, protocol: dict) -> dict:
    clusters = [
        protocol["clustersById"][cluster_id]
        for cluster_id in protocol["annualPilot"]["clusterIds"]
    ]
    modules = [module for cluster in clusters for module in cluster["modules"]]
    integrations = [cluster["integration"] for cluster in clusters]
    module_results = _derive_module_results_for_modules(annual_payload, modules)
    integration_results = _derive_integration_results_for_contracts(
        annual_payload, integrations
    )
    delivery = annual_payload["deliveryTimeEvidence"]
    _require(delivery["actualUnits"] <= 40, "annual budget exceeded")
    _require(
        delivery["clusterOrder"] == protocol["annualPilot"]["clusterIds"],
        "annual sequence differs",
    )
    annual_cluster_units = delivery["clusterActualUnits"]
    for record, cluster_id in zip(
        annual_cluster_units,
        protocol["annualPilot"]["clusterIds"],
        strict=True,
    ):
        _require(
            record["clusterId"] == cluster_id
            and record["actualUnits"] <= protocol["clustersById"][cluster_id]["budgetUnits"],
            f"annual cluster budget exceeded: {cluster_id}",
        )

    integrations_passed = all(item["result"] == "pass" for item in integration_results)
    modules_passed = all(item["result"] == "pass" for item in module_results)
    pulse = evaluate_learner_pulse(annual_payload["learnerPulseEvidence"], protocol)
    availability_conditions = {
        "capacity": delivery["actualUnits"] == 40,
        "integration": "passed" if integrations_passed else "failed",
        "technical": "passed" if _technical_path_passed(annual_payload) else "failed",
        "privacy": "passed" if annual_payload["technicalPrivacyEvidence"]["privacyGate"] == "pass" else "failed",
    }
    annual_not_evaluable = delivery["externalDisruptionCode"] == "interpretability-lost"
    annual_failed = any([
        not availability_conditions["capacity"],
        availability_conditions["integration"] == "failed",
        availability_conditions["technical"] == "failed",
        availability_conditions["privacy"] == "failed",
        not modules_passed,
        bool(pulse["warnings"]),
    ])
    annual_result = (
        "not-evaluable"
        if annual_not_evaluable
        else "fail"
        if annual_failed
        else "pass"
    )
    gates = {
        "capacity": "passed" if availability_conditions["capacity"] else "failed",
        "integration": availability_conditions["integration"],
        "technical": availability_conditions["technical"],
        "privacy": availability_conditions["privacy"],
        "pilot": "passed" if annual_result == "pass" else "failed",
    }
    return {
        "result": annual_result,
        "actualUnits": delivery["actualUnits"],
        "availabilityGateResults": gates,
        "moduleResults": module_results,
        "integrationResults": integration_results,
        "developmentWarnings": pulse["warnings"],
    }


def derive_annual_result(
    annual_payload: dict,
    cluster_packages: list[dict],
    protocol: dict,
) -> dict:
    _require(isinstance(cluster_packages, list), "annual result requires cluster packages")
    _require(
        all(
            isinstance(item, dict) and item.get("scopeId") in protocol["clustersById"]
            for item in cluster_packages
        ),
        "annual result requires known cluster packages",
    )
    ordered = sorted(
        cluster_packages,
        key=lambda item: protocol["clustersById"][item["scopeId"]]["order"],
    )
    _require(len(ordered) == 4, "annual result requires four cluster packages")
    _require(
        len({item["scopeId"] for item in ordered}) == 4,
        "annual result requires distinct cluster packages",
    )
    annual_sources = [*ordered, annual_payload]
    _require(
        len({item["packageId"] for item in annual_sources}) == 5,
        "annual result requires distinct source package IDs",
    )
    for field in (
        "protocolVersion", "protocolFingerprint", "toolVersion",
        "timeModelFingerprint",
    ):
        _require(
            len({item[field] for item in annual_sources}) == 1,
            f"annual source {field} values differ",
        )
    _require(annual_payload["protocolVersion"] == protocol["protocolVersion"], "annual protocolVersion differs")
    _require(annual_payload["protocolFingerprint"] == protocol["protocolFingerprint"], "annual protocolFingerprint differs")
    _require(annual_payload["toolVersion"] == protocol["toolVersion"], "annual toolVersion differs")
    _require(annual_payload["timeModelFingerprint"] == protocol["timeModelFingerprint"], "annual timeModelFingerprint differs")
    _require(
        [item["scopeId"] for item in ordered] == protocol["annualPilot"]["clusterIds"],
        "annual cluster sequence differs",
    )
    for item in ordered:
        cluster = protocol["clustersById"][item["scopeId"]]
        _require(
            item["deliveryTimeEvidence"]["actualUnits"] <= cluster["budgetUnits"],
            f"cluster budget exceeded: {item['scopeId']}",
        )
    for item in ordered:
        _validate_evidence_package_contract(item, protocol)
    _require(
        all(item["result"] == "pass" for item in ordered),
        "annual result requires positive clusters",
    )

    derived = _derive_annual_evidence_result(annual_payload, protocol)
    return {
        "result": derived["result"],
        "actualUnits": derived["actualUnits"],
        "availabilityGateResults": derived["availabilityGateResults"],
    }


def _decision_package_id(source_package_ids: list[str]) -> str:
    name = "|".join(sorted(source_package_ids))
    return f"PKG-{uuid.uuid5(DECISION_NAMESPACE, name)}"


def _expected_decision_scopes(protocol: dict) -> list[str]:
    return [*protocol["annualPilot"]["clusterIds"], protocol["annualPilot"]["id"]]


def _validate_decision_results(payload: dict, protocol: dict) -> None:
    pilot_results = payload["pilotResults"]
    expected_scopes = _expected_decision_scopes(protocol)
    _require(isinstance(pilot_results, list) and len(pilot_results) == 5, "pilotResults must contain five records")
    for result, scope_id in zip(pilot_results, expected_scopes, strict=True):
        _require_exact_fields(result, DECISION_PILOT_RESULT_FIELDS, "pilot result")
        _require(result["scopeId"] == scope_id, "pilot result sequence differs")
        _require(isinstance(result["packageId"], str) and PACKAGE_ID_PATTERN.fullmatch(result["packageId"]), "pilot source packageId is invalid")
        _require_enum(result["result"], protocol["results"], "pilot result")
    _require(
        [item["packageId"] for item in pilot_results] == payload["sourcePackageIds"],
        "pilot result sources differ",
    )
    _require(
        all(item["result"] == "pass" for item in pilot_results[:4]),
        "first four cluster pilot results must pass",
    )

    expected_modules = [
        module
        for cluster in protocol["clusters"]
        for module in cluster["modules"]
    ]
    module_results = payload["moduleResults"]
    _require(isinstance(module_results, list) and len(module_results) == 10, "moduleResults must contain ten records")
    for result, module in zip(module_results, expected_modules, strict=True):
        _require_exact_fields(result, DECISION_MODULE_RESULT_FIELDS, "decision module result")
        _require(result["moduleId"] == module["moduleId"], "decision module sequence differs")
        _require(result["pilotAssignmentId"] == module["pilotAssignmentId"], "decision module pilot assignment differs")
        _require_enum(result["result"], protocol["results"], "decision module result")
    _require(
        all(item["result"] == "pass" for item in module_results),
        "cluster module results must pass",
    )

    integration_results = payload["integrationResults"]
    _require(isinstance(integration_results, list) and len(integration_results) == 4, "integrationResults must contain four records")
    for result, cluster in zip(integration_results, protocol["clusters"], strict=True):
        _require_exact_fields(result, DECISION_INTEGRATION_RESULT_FIELDS, "decision integration result")
        integration = cluster["integration"]
        _require(result["integrationContractId"] == integration["integrationContractId"], "decision integration sequence differs")
        _require(result["pilotAssignmentId"] == integration["pilotAssignmentId"], "decision integration pilot assignment differs")
        _require_enum(result["result"], protocol["results"], "decision integration result")
        _require_int(result["fallbackDeltaUnits"], "fallbackDeltaUnits")
        expected_fallback = cluster["fallbackDeltaUnits"] if result["result"] == "fail" else 0
        _require(result["fallbackDeltaUnits"] == expected_fallback, "integration fallback delta differs")
    _require(
        all(item["result"] == "pass" for item in integration_results),
        "cluster integration results must pass",
    )


def validate_decision_package(payload: dict, protocol: dict, time_model: dict) -> dict:
    _require_exact_fields(payload, DECISION_PACKAGE_FIELDS, "decision package")
    _require(payload["schemaVersion"] == 1 and type(payload["schemaVersion"]) is int, "decision schemaVersion must be 1")
    _require(payload["packageType"] == "pilot-decision", "decision packageType differs")
    _require(isinstance(payload["packageId"], str) and DECISION_PACKAGE_ID_PATTERN.fullmatch(payload["packageId"]), "decision packageId is invalid")
    _require(payload["protocolVersion"] == protocol["protocolVersion"], "decision protocolVersion differs")
    _require(payload["protocolFingerprint"] == protocol["protocolFingerprint"], "decision protocolFingerprint differs")
    _require(payload["toolVersion"] == protocol["toolVersion"], "decision toolVersion differs")
    _require(canonical_sha256(time_model) == protocol["timeModelFingerprint"], "time model differs from compiled protocol")
    _require(payload["timeModelFingerprint"] == protocol["timeModelFingerprint"], "decision timeModelFingerprint differs")

    source_ids = payload["sourcePackageIds"]
    _require(isinstance(source_ids, list) and len(source_ids) == 5, "decision requires five source package IDs")
    _require(len(set(source_ids)) == 5, "decision source package IDs must be distinct")
    _require(all(isinstance(item, str) and PACKAGE_ID_PATTERN.fullmatch(item) for item in source_ids), "decision source package ID is invalid")
    _require(payload["packageId"] == _decision_package_id(source_ids), "decision packageId is not deterministic")
    _validate_decision_results(payload, protocol)

    gates = payload["availabilityGateResults"]
    _require_exact_fields(gates, AVAILABILITY_GATE_FIELDS, "availability gate results")
    for value in gates.values():
        _require_enum(value, ["passed", "failed"], "availability gate result")

    summary = payload["timeAndFallbackSummary"]
    _require_exact_fields(summary, TIME_FALLBACK_SUMMARY_FIELDS, "time and fallback summary")
    for field in TIME_FALLBACK_SUMMARY_FIELDS:
        _require_int(summary[field], f"time and fallback {field}")
    _require(summary["plannedUnits"] == 40, "decision plannedUnits must be 40")
    _require(summary["actualUnits"] <= 40, "decision actualUnits exceed 40 unit budget")
    fallback_units = sum(item["fallbackDeltaUnits"] for item in payload["integrationResults"] if item["result"] == "fail")
    _require(summary["fallbackUnits"] == fallback_units, "decision fallbackUnits differ from failed integrations")
    _require(summary["fallbackUnits"] <= 14, "decision fallbackUnits exceed contract")
    _require(summary["requiredUnits"] == 40 + summary["fallbackUnits"], "decision requiredUnits differ")

    technical_privacy = payload["technicalPrivacySummary"]
    _require_exact_fields(technical_privacy, TECHNICAL_PRIVACY_SUMMARY_FIELDS, "technical privacy summary")
    for value in technical_privacy.values():
        _require_enum(value, ["pass", "fail"], "technical privacy summary")

    warnings = payload["developmentWarnings"]
    _require(isinstance(warnings, list), "decision developmentWarnings must be a list")
    known_warning_item_ids = {item["id"] for item in protocol["learnerPulseItems"]}
    for warning in warnings:
        _require_exact_fields(warning, WARNING_FIELDS, "decision development warning")
        _require(warning["id"] == f"WARN-{warning['itemId']}" and warning["status"] == "open", "decision development warning is invalid")
        _require(warning["itemId"] in known_warning_item_ids, "decision development warning is unknown")
    _require(warnings == sorted(warnings, key=lambda item: item["id"]), "decision developmentWarnings must be sorted")
    _require(len({warning["id"] for warning in warnings}) == len(warnings), "decision developmentWarnings must be deduplicated")

    _require(payload["statementBoundary"] == "documented-conditions-only", "decision statement boundary differs")
    _require(payload["retentionClass"] == "until-decision", "decision retentionClass differs")
    review_status = payload["reviewStatus"]
    _require_exact_fields(review_status, REVIEW_STATUS_FIELDS, "review status")
    for value in review_status.values():
        _require_enum(value, ["not-started", "passed", "failed"], "review status")

    annual_result = payload["pilotResults"][-1]["result"]
    _require(
        gates["capacity"] == ("passed" if summary["actualUnits"] == 40 else "failed"),
        "capacity gate differs from exact annual units",
    )
    _require(
        gates["technical"] == ("passed" if technical_privacy["technical"] == "pass" else "failed"),
        "technical gate differs from annual summary",
    )
    _require(
        gates["privacy"] == ("passed" if technical_privacy["privacy"] == "pass" else "failed"),
        "privacy gate differs from annual summary",
    )
    _require(
        gates["pilot"] == ("passed" if annual_result == "pass" else "failed"),
        "pilot gate differs from annual result",
    )
    all_gates_passed = all(value == "passed" for value in gates.values())
    if annual_result == "pass":
        _require(all_gates_passed, "positive annual result requires five passed gates")
        _require(not warnings, "positive annual result conflicts with development warnings")
    expected_recommendation = (
        "eligible-for-working-availability-review"
        if annual_result == "pass" and all_gates_passed
        else "not-evaluable"
        if annual_result == "not-evaluable"
        else "repeat-required"
    )
    _require_enum(
        payload["recommendation"],
        ["eligible-for-working-availability-review", "repeat-required", "not-evaluable"],
        "decision recommendation",
    )
    _require(payload["recommendation"] == expected_recommendation, "decision recommendation differs from results")
    if any(value == "passed" for value in review_status.values()):
        _require(annual_result == "pass" and all_gates_passed, "reviews cannot pass without a positive minimal pilot")
    return copy.deepcopy(payload)


def build_decision_package(
    evidence_packages: list[dict],
    protocol: dict,
    time_model: dict,
) -> dict:
    time_model_before = canonical_sha256(time_model)
    _require(time_model_before == protocol["timeModelFingerprint"], "time model differs before decision build")
    _require(isinstance(evidence_packages, list) and len(evidence_packages) == 5, "decision requires exactly five evidence packages")
    validated = [
        validate_evidence_package(item, protocol, time_model)
        for item in evidence_packages
    ]
    package_ids = [item["packageId"] for item in validated]
    _require(len(set(package_ids)) == 5, "decision source package IDs must be distinct")
    expected_scopes = _expected_decision_scopes(protocol)
    packages_by_scope = {item["scopeId"]: item for item in validated}
    _require(len(packages_by_scope) == 5 and set(packages_by_scope) == set(expected_scopes), "decision evidence scopes differ from contract")
    ordered = [packages_by_scope[scope_id] for scope_id in expected_scopes]
    for field in (
        "protocolVersion", "protocolFingerprint", "toolVersion",
        "timeModelFingerprint",
    ):
        _require(len({item[field] for item in ordered}) == 1, f"decision source {field} values differ")

    cluster_packages = ordered[:4]
    annual_payload = ordered[4]
    annual_result = derive_annual_result(annual_payload, cluster_packages, protocol)
    cluster_results = []
    for source, cluster in zip(cluster_packages, protocol["clusters"], strict=True):
        result = derive_cluster_result(source, cluster, protocol)
        _require(source["result"] == result["result"], f"cluster result differs from evidence: {source['scopeId']}")
        cluster_results.append(result)
    _require(annual_payload["result"] == annual_result["result"], "annual result differs from evidence")

    module_results = [
        {
            "moduleId": item["moduleId"],
            "pilotAssignmentId": item["pilotAssignmentId"],
            "result": item["result"],
        }
        for result in cluster_results
        for item in result["moduleResults"]
    ]
    integration_results = []
    for result in cluster_results:
        item = result["integrationResult"]
        integration_results.append({
            "integrationContractId": item["integrationContractId"],
            "pilotAssignmentId": item["pilotAssignmentId"],
            "result": item["result"],
            "fallbackDeltaUnits": result["fallbackDeltaUnits"] if item["result"] == "fail" else 0,
        })
    fallback_units = sum(
        item["fallbackDeltaUnits"]
        for item in integration_results
        if item["result"] == "fail"
    )
    warning_by_id = {
        warning["id"]: copy.deepcopy(warning)
        for source in ordered
        for warning in source["developmentWarnings"]
    }
    source_ids = [item["packageId"] for item in ordered]
    pilot_results = [
        {"scopeId": item["scopeId"], "packageId": item["packageId"], "result": item["result"]}
        for item in ordered
    ]
    gates = annual_result["availabilityGateResults"]
    recommendation = (
        "eligible-for-working-availability-review"
        if all(item["result"] == "pass" for item in pilot_results)
        and all(value == "passed" for value in gates.values())
        else "not-evaluable"
        if any(item["result"] == "not-evaluable" for item in pilot_results)
        else "repeat-required"
    )
    package = {
        "schemaVersion": 1,
        "packageType": "pilot-decision",
        "packageId": _decision_package_id(source_ids),
        "protocolVersion": protocol["protocolVersion"],
        "protocolFingerprint": protocol["protocolFingerprint"],
        "toolVersion": protocol["toolVersion"],
        "timeModelFingerprint": protocol["timeModelFingerprint"],
        "sourcePackageIds": source_ids,
        "pilotResults": pilot_results,
        "moduleResults": module_results,
        "integrationResults": integration_results,
        "availabilityGateResults": copy.deepcopy(gates),
        "timeAndFallbackSummary": {
            "plannedUnits": 40,
            "actualUnits": annual_result["actualUnits"],
            "fallbackUnits": fallback_units,
            "requiredUnits": 40 + fallback_units,
        },
        "technicalPrivacySummary": {
            "technical": "pass" if gates["technical"] == "passed" else "fail",
            "privacy": "pass" if gates["privacy"] == "passed" else "fail",
        },
        "developmentWarnings": [warning_by_id[warning_id] for warning_id in sorted(warning_by_id)],
        "statementBoundary": "documented-conditions-only",
        "recommendation": recommendation,
        "reviewStatus": {
            "fach": "not-started",
            "engineeringPrivacy": "not-started",
            "commissioner": "not-started",
        },
        "retentionClass": "until-decision",
    }
    validated_package = validate_decision_package(package, protocol, time_model)
    _require(canonical_sha256(time_model) == time_model_before, "time model mutated during decision build")
    return validated_package


def _load_synthetic_example_packages(
    root: Path,
    protocol: dict,
    time_model: dict,
    *,
    require_decision: bool,
) -> dict[str, dict]:
    examples_path = root / "pilot/examples"
    _require(examples_path.is_dir(), "synthetic examples directory is missing")
    paths = sorted(examples_path.glob("*.json"))
    names = {path.name for path in paths}
    expected_names = SYNTHETIC_EXAMPLE_NAMES - {SYNTHETIC_DECISION_NAME}
    _require(
        names == (SYNTHETIC_EXAMPLE_NAMES if require_decision else expected_names)
        or (not require_decision and names == SYNTHETIC_EXAMPLE_NAMES),
        "synthetic example filenames differ from contract",
    )
    _require(all(path.name.startswith("synthetic-") for path in paths), "examples must be explicitly synthetic")

    packages = {path.name: _load_json(path) for path in paths}
    for name, package in packages.items():
        if name != SYNTHETIC_DECISION_NAME:
            validate_evidence_package(package, protocol, time_model)
    return packages


def _reject_repository_evidence_outside_examples(root: Path) -> None:
    examples_path = (root / "pilot/examples").resolve(strict=True)
    for path in root.rglob("*.json"):
        resolved = path.resolve(strict=True)
        if resolved.is_relative_to(examples_path):
            continue
        payload = _load_json(resolved)
        if isinstance(payload, dict) and payload.get("packageType") in {
            "cluster-evidence", "annual-evidence", "pilot-decision",
        }:
            raise IUM11ValidationError(f"evidence package outside pilot/examples: {path}")


def _validate_synthetic_examples(
    root: Path,
    protocol: dict,
    time_model: dict,
    *,
    require_decision: bool,
) -> tuple[dict[str, dict], dict[str, int]]:
    evidence_schema = _load_json(root / "pilot/schemas/evidence-package.schema.json")
    decision_schema = _load_json(root / "pilot/schemas/decision-package.schema.json")
    _require(evidence_schema.get("additionalProperties") is False, "evidence schema must be closed")
    _require(decision_schema.get("additionalProperties") is False, "decision schema must be closed")
    _reject_repository_evidence_outside_examples(root)
    packages = _load_synthetic_example_packages(root, protocol, time_model, require_decision=require_decision)
    positive = [packages[name] for name in SYNTHETIC_POSITIVE_EXAMPLE_NAMES]
    positive_clusters = positive[:4]
    annual = positive[-1]
    _require([item["scopeId"] for item in positive_clusters] == protocol["annualPilot"]["clusterIds"], "positive cluster examples differ from contract")
    _require(all(item["result"] == "pass" for item in positive_clusters), "positive cluster examples must pass")
    _require(annual["scopeId"] == protocol["annualPilot"]["id"] and annual["result"] == "pass", "annual example must pass")
    _require(derive_annual_result(annual, positive_clusters, protocol)["result"] == "pass", "annual example is not derivable")

    negative = packages["synthetic-cluster-fail.json"]
    negative_result = derive_cluster_result(negative, protocol["clustersById"][negative["scopeId"]], protocol)
    _require(negative["scopeId"] == "CLUSTER-7-PROGRAMMING" and negative["result"] == "fail", "negative example differs from contract")
    _require(negative["deliveryTimeEvidence"]["actualUnits"] == 12, "negative example must demonstrate twelve units")
    _require(negative_result["result"] == "fail", "negative example must derive a failed result")
    _require(negative_result["developmentWarnings"] == [], "negative example must not add learner warnings")
    _require(negative_result["fallbackDeltaUnits"] == 2, "negative example must derive the programming fallback")

    counts = {"clusterPass": 4, "clusterFail": 1, "annualPass": 1, "decisionEligible": 0}
    if require_decision:
        decision = packages[SYNTHETIC_DECISION_NAME]
        _require(decision == build_decision_package(positive, protocol, time_model), "synthetic decision differs from positive examples")
        counts["decisionEligible"] = 1
    return packages, counts


def _validate_schema_is_closed(schema: dict, label: str) -> None:
    _require(isinstance(schema, dict), f"{label} schema must be an object")
    _require(
        schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema",
        f"{label} schema draft differs from contract",
    )

    def visit(node: object) -> None:
        if isinstance(node, dict):
            if node.get("type") == "object":
                _require(
                    node.get("additionalProperties") is False,
                    f"{label} schema object must be closed",
                )
            for value in node.values():
                visit(value)
        elif isinstance(node, list):
            for value in node:
                visit(value)

    visit(schema)


def _validate_in_memory_examples(
    example_packages: list[dict],
    protocol: dict,
    time_model: dict,
) -> dict[str, int]:
    _require(isinstance(example_packages, list), "example packages must be a list")
    _require(len(example_packages) == 7, "exactly seven synthetic example packages are required")
    _require(all(isinstance(package, dict) for package in example_packages), "example package must be an object")

    evidence_packages = [
        package for package in example_packages
        if package.get("packageType") != "pilot-decision"
    ]
    decision_packages = [
        package for package in example_packages
        if package.get("packageType") == "pilot-decision"
    ]
    _require(len(evidence_packages) == 6, "synthetic evidence example count differs from contract")
    _require(len(decision_packages) == 1, "synthetic decision example count differs from contract")
    for package in evidence_packages:
        validate_evidence_package(package, protocol, time_model)

    expected_cluster_ids = protocol["annualPilot"]["clusterIds"]
    positive_clusters = []
    for cluster_id in expected_cluster_ids:
        matches = [
            package for package in evidence_packages
            if package["scopeId"] == cluster_id and package["result"] == "pass"
        ]
        _require(len(matches) == 1, f"positive synthetic cluster differs from contract: {cluster_id}")
        positive_clusters.append(matches[0])
    annual_matches = [
        package for package in evidence_packages
        if package["scopeId"] == protocol["annualPilot"]["id"] and package["result"] == "pass"
    ]
    _require(len(annual_matches) == 1, "positive synthetic annual example differs from contract")
    annual = annual_matches[0]
    _require(
        derive_annual_result(annual, positive_clusters, protocol)["result"] == "pass",
        "annual example is not derivable",
    )

    negative_matches = [
        package for package in evidence_packages
        if package["scopeType"] == "cluster" and package["result"] == "fail"
    ]
    _require(len(negative_matches) == 1, "negative synthetic cluster count differs from contract")
    negative = negative_matches[0]
    negative_result = derive_cluster_result(
        negative,
        protocol["clustersById"][negative["scopeId"]],
        protocol,
    )
    _require(
        negative["scopeId"] == "CLUSTER-7-PROGRAMMING"
        and negative["deliveryTimeEvidence"]["actualUnits"] == 12,
        "negative synthetic cluster differs from contract",
    )
    _require(
        negative_result["result"] == "fail"
        and negative_result["fallbackDeltaUnits"] == 2
        and negative_result["developmentWarnings"] == [],
        "negative synthetic cluster is not derivable",
    )

    positive_packages = [*positive_clusters, annual]
    decision = decision_packages[0]
    validate_decision_package(decision, protocol, time_model)
    _require(
        decision == build_decision_package(positive_packages, protocol, time_model),
        "synthetic decision differs from positive examples",
    )
    return {
        "clusterPass": 4,
        "clusterFail": 1,
        "annualPass": 1,
        "decisionEligible": 1,
    }


def _validate_publication_contract(
    root: Path,
    compiled_protocol: dict,
    time_model: dict,
    ium10_result: dict,
) -> dict[str, int]:
    root = Path(root)
    missing = [
        relative_path
        for relative_path in PUBLICATION_PRODUCT_PATHS
        if not (root / relative_path).is_file()
    ]
    _require(not missing, f"IUM11 product files are missing: {missing}")

    allowed_json_paths = {
        "pilot/docs/publication-contract.json",
        "pilot/pilot-protocol.json",
        "pilot/schemas/evidence-package.schema.json",
        "pilot/schemas/decision-package.schema.json",
        *{
            f"pilot/examples/{name}"
            for name in SYNTHETIC_EXAMPLE_NAMES
        },
    }
    actual_json_paths = {
        path.relative_to(root).as_posix()
        for path in (root / "pilot").rglob("*.json")
    }
    _require(
        actual_json_paths == allowed_json_paths,
        "pilot JSON files differ from the public synthetic-only contract",
    )
    example_names = {
        path.name for path in (root / "pilot/examples").glob("*.json")
    }
    _require(
        example_names == SYNTHETIC_EXAMPLE_NAMES
        and all(name.startswith("synthetic-") for name in example_names),
        "pilot examples must be exclusively and explicitly synthetic",
    )

    try:
        expected_contract = compile_publication_contract(
            compiled_protocol,
            time_model,
            ium10_result,
        )
        expected_json = render_publication_contract_json(expected_contract)
        expected_block = render_publication_markdown_block(expected_contract)
        _require(
            (root / "pilot/docs/publication-contract.json").read_bytes()
            == expected_json,
            "publication contract JSON differs from compiled contract",
        )

        publications = {
            relative_path: (root / relative_path).read_text(encoding="utf-8")
            for relative_path in PUBLICATION_PATHS
        }
        for relative_path, text in publications.items():
            actual_block = extract_publication_block(text)
            _require(
                actual_block == expected_block,
                f"publication contract block drift: {relative_path}",
            )
            validate_publication_text_boundary(relative_path, text)
    except IUM11PublicationError as error:
        raise IUM11ValidationError(str(error)) from error

    return {
        "productFiles": len(PUBLICATION_PRODUCT_PATHS),
        "syntheticExamples": len(SYNTHETIC_EXAMPLE_NAMES),
        "publications": len(PUBLICATION_PATHS),
        "publicationContracts": 1,
    }


def validate_ium11(
    time_model: dict,
    ium10_result: dict,
    protocol: dict,
    evidence_schema: dict,
    decision_schema: dict,
    example_packages: list[dict],
    cockpit_root: Path,
) -> dict:
    """Validate the complete in-memory IUM11 contract."""
    _require(isinstance(ium10_result, dict), "IUM10 result must be an object")
    _require("gradeJudgements" in ium10_result, "IUM10 result differs from contract")
    time_model_before = canonical_sha256(time_model)
    compiled = validate_pilot_protocol(protocol, time_model)
    _validate_schema_is_closed(evidence_schema, "evidence")
    _validate_schema_is_closed(decision_schema, "decision")
    example_counts = _validate_in_memory_examples(
        example_packages,
        compiled,
        time_model,
    )

    cockpit_root = Path(cockpit_root)
    for relative_path in (
        "index.html",
        "assets/styles.css",
        "assets/app.js",
        "assets/protocol.js",
    ):
        _require(
            (cockpit_root / relative_path).is_file(),
            f"cockpit product file is missing: {relative_path}",
        )
    if __package__:
        from .build_ium11_cockpit import compile_cockpit_contract, render_protocol_js
    else:
        from build_ium11_cockpit import compile_cockpit_contract, render_protocol_js
    repository_root = cockpit_root.parents[1]
    publication = _validate_publication_contract(
        repository_root,
        compiled,
        time_model,
        ium10_result,
    )
    expected_protocol_js = render_protocol_js(compile_cockpit_contract(repository_root))
    _require(
        (cockpit_root / "assets/protocol.js").read_bytes()
        == expected_protocol_js.encode("utf-8"),
        "cockpit protocol build differs from source contract",
    )
    _require(
        canonical_sha256(time_model) == time_model_before,
        "time model mutated during IUM11 validation",
    )
    return {
        "ium10": ium10_result,
        "protocol": compiled,
        "exampleCounts": example_counts,
        "publication": publication,
    }


def validate_ium11_repository(root: Path, *, require_decision: bool = True) -> dict:
    root = Path(root)
    time_model = _load_json(root / "roadmap/time-model.json")
    time_model_before = canonical_sha256(time_model)
    ium10_result = validate_ium10_repository(root)
    protocol = _load_json(root / "pilot/pilot-protocol.json")
    if require_decision:
        result = validate_ium11(
            time_model,
            ium10_result,
            protocol,
            _load_json(root / "pilot/schemas/evidence-package.schema.json"),
            _load_json(root / "pilot/schemas/decision-package.schema.json"),
            [
                _load_json(path)
                for path in sorted((root / "pilot/examples").glob("*.json"))
            ],
            root / "pilot/cockpit",
        )
        compiled = result["protocol"]
        example_counts = result["exampleCounts"]
    else:
        compiled = validate_pilot_protocol(protocol, time_model)
        _, example_counts = _validate_synthetic_examples(
            root, compiled, time_model, require_decision=False
        )
    _reject_repository_evidence_outside_examples(root)
    _require(canonical_sha256(time_model) == time_model_before, "time model mutated during repository validation")
    return {"ium10": ium10_result, "protocol": compiled, "exampleCounts": example_counts}


def _validate_private_decision_paths(
    evidence_paths: list[Path],
    output_path: Path,
    repository_root: Path,
) -> tuple[list[Path], Path]:
    _require(len(evidence_paths) == 5, "private decision build requires exactly five --evidence paths")
    repository_root = repository_root.resolve(strict=True)
    resolved_inputs = []
    for path in evidence_paths:
        resolved = path.resolve(strict=True)
        _require(resolved.is_file(), f"evidence path is not a file: {path}")
        _require(not resolved.is_relative_to(repository_root), f"private evidence path is inside repository: {path}")
        resolved_inputs.append(resolved)

    _require(not output_path.exists(), "decision output already exists")
    output_parent = output_path.parent.resolve(strict=True)
    _require(output_parent.is_dir(), "decision output parent is not a directory")
    resolved_output = output_parent / output_path.name
    _require(output_path.name not in {"", ".", ".."}, "decision output filename is invalid")
    _require(not resolved_output.is_relative_to(repository_root), "decision output path is inside repository")
    _require(resolved_output not in resolved_inputs, "decision output overlaps an evidence input")
    return resolved_inputs, resolved_output


def _write_json_exclusive_atomic(path: Path, payload: dict) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)


def _write_json_replace_atomic(path: Path, payload: dict) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Validate the IUM11 pilot protocol.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="Repository root containing roadmap and pilot JSON inputs.")
    parser.add_argument("--evidence", type=Path, action="append", default=[], help="Private evidence package path; repeat exactly five times.")
    parser.add_argument("--decision-output", type=Path, help="New private output path for the deterministic decision package.")
    parser.add_argument("--write-synthetic-decision", type=Path, help="Regenerate only pilot/examples/synthetic-decision-eligible.json from committed synthetic positive examples.")
    arguments = parser.parse_args(argv)
    try:
        _require(not (arguments.write_synthetic_decision and (arguments.evidence or arguments.decision_output)), "synthetic decision mode cannot be combined with private decision paths")
        result = validate_ium11_repository(arguments.root, require_decision=not arguments.write_synthetic_decision)
        if arguments.write_synthetic_decision:
            root = Path(arguments.root).resolve(strict=True)
            _require(
                arguments.write_synthetic_decision == Path("pilot/examples/synthetic-decision-eligible.json"),
                "synthetic decision output path differs from the committed example path",
            )
            examples, _ = _validate_synthetic_examples(root, result["protocol"], _load_json(root / "roadmap/time-model.json"), require_decision=False)
            decision = build_decision_package(
                [examples[name] for name in SYNTHETIC_POSITIVE_EXAMPLE_NAMES],
                result["protocol"],
                _load_json(root / "roadmap/time-model.json"),
            )
            _write_json_replace_atomic(root / "pilot/examples" / SYNTHETIC_DECISION_NAME, decision)
            print("IUM11 synthetic decision written: pilot/examples/synthetic-decision-eligible.json")
            return 0
        private_mode = bool(arguments.evidence) or arguments.decision_output is not None
        if private_mode:
            _require(arguments.decision_output is not None, "private decision build requires --decision-output")
            evidence_paths, output_path = _validate_private_decision_paths(
                arguments.evidence,
                arguments.decision_output,
                arguments.root,
            )
            evidence_packages = [_load_json(path) for path in evidence_paths]
            time_model = _load_json(Path(arguments.root) / "roadmap/time-model.json")
            decision = build_decision_package(
                evidence_packages,
                result["protocol"],
                time_model,
            )
            _write_json_exclusive_atomic(output_path, decision)
            print(
                "IUM11 private decision validation passed: "
                f"5 evidence packages, output {output_path}"
            )
            return 0
    except (IUM10ValidationError, IUM11ValidationError, OSError, json.JSONDecodeError) as error:
        print(f"IUM11 repository validation failed: {error}", file=sys.stderr)
        return 1
    protocol = result["protocol"]
    module_count = sum(len(cluster["modules"]) for cluster in protocol["clusters"])
    print(
        "IUM11 repository validation passed: "
        f"protocol {protocol['protocolVersion']}, {len(protocol['clusters'])} clusters, "
        f"{module_count} module bindings, and 1 annual pilot"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
