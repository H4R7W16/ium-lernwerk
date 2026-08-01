import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path

if __package__:
    from .validate_ium10 import (
        IUM10ValidationError,
        PHASE_IDS,
        validate_ium10_repository,
    )
else:
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


def validate_ium11_repository(root: Path) -> dict:
    root = Path(root)
    time_model = _load_json(root / "roadmap/time-model.json")
    ium10_result = validate_ium10_repository(root)
    protocol = _load_json(root / "pilot/pilot-protocol.json")
    compiled = validate_pilot_protocol(protocol, time_model)
    return {"ium10": ium10_result, "protocol": compiled}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Validate the IUM11 pilot protocol.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="Repository root containing roadmap and pilot JSON inputs.")
    arguments = parser.parse_args(argv)
    try:
        result = validate_ium11_repository(arguments.root)
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
