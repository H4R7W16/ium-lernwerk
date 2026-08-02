import hashlib
import json
import re


PUBLICATION_CONTRACT_ID = "IUM11-PUBLICATION-CONTRACT"
PUBLICATION_CONTRACT_VERSION = "1.0.0"
PUBLICATION_START_MARKER = "<!-- IUM11-PUBLICATION-CONTRACT:START -->"
PUBLICATION_END_MARKER = "<!-- IUM11-PUBLICATION-CONTRACT:END -->"
PUBLICATION_PATHS = (
    "README.md",
    "pilot/docs/teacher-guide.md",
    "pilot/docs/review-guide.md",
)
STATEMENT_BOUNDARY = "documented-conditions-only"
FUTURE_ALLOWED_CHANGES = [
    {"field": "availabilityStatus", "value": "available"},
    {"field": "timeFeasibilityStatus", "value": "green"},
    {"field": "pilotStatus", "value": "completed"},
]
UNCHANGED_AXES = [
    {"field": "status", "value": "working"},
    {"field": "semanticCoverageStatus", "value": "partial"},
]

_TIME_MODEL_FINGERPRINT = (
    "873774e52b6c9a20e08e5079c898a014493a39305be5efa35a601248ff36a2c1"
)
_VARIANT_ID = "GRADE-7-WORKING-40"
_AVAILABILITY_CONTRACT_ID = "AVAIL-GRADE-7-WORKING-40"
_CURRENT_AXES = {
    "status": "working",
    "availabilityStatus": "conditional",
    "timeFeasibilityStatus": "amber",
    "sequenceEvidenceStatus": "covered",
    "pilotStatus": "not-started",
    "semanticCoverageStatus": "partial",
}
_CLUSTER_IDS = (
    "CLUSTER-7-DATA-CODING",
    "CLUSTER-7-PROGRAMMING",
    "CLUSTER-7-NET-SECURITY",
    "CLUSTER-7-DATA-MEDIA-SOCIETY",
)


class IUM11PublicationError(ValueError):
    pass


def _require(condition, message):
    if not condition:
        raise IUM11PublicationError(message)


def _canonical_sha256(payload):
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _single_raw_variant(time_model):
    _require(isinstance(time_model, dict), "time model must be an object")
    variants = time_model.get("annualVariants")
    _require(isinstance(variants, list), "raw variant boundary requires annual variants")
    matches = [
        variant
        for variant in variants
        if isinstance(variant, dict) and variant.get("id") == _VARIANT_ID
    ]
    _require(len(matches) == 1, "raw variant boundary requires one working variant")
    return matches[0]


def _single_raw_availability(time_model):
    contracts = time_model.get("availabilityContracts")
    _require(isinstance(contracts, list), "availability boundary requires contracts")
    matches = [
        contract
        for contract in contracts
        if isinstance(contract, dict)
        and contract.get("id") == _AVAILABILITY_CONTRACT_ID
        and contract.get("variantId") == _VARIANT_ID
    ]
    _require(len(matches) == 1, "availability boundary requires one matching contract")
    return matches[0]


def _grade_7_judgement(ium10_result):
    judgements = ium10_result.get("gradeJudgements") if isinstance(ium10_result, dict) else None
    _require(isinstance(judgements, dict) and 7 in judgements, "judgement boundary requires Grade 7")
    judgement = judgements[7]
    _require(isinstance(judgement, dict), "judgement boundary requires Grade 7 object")
    return judgement


def _referenced_pilot_ids(compiled_protocol):
    clusters = compiled_protocol.get("clusters") if isinstance(compiled_protocol, dict) else None
    _require(isinstance(clusters, list) and len(clusters) == 4, "cluster boundary requires four clusters")
    pilot_ids = []
    module_ids = []
    cluster_rows = []
    for order, cluster in enumerate(clusters, start=1):
        _require(isinstance(cluster, dict) and cluster.get("order") == order, "cluster order boundary differs")
        _require(
            cluster.get("id") == _CLUSTER_IDS[order - 1],
            "cluster identity boundary differs",
        )
        modules = cluster.get("modules")
        declared_module_ids = cluster.get("moduleIds")
        _require(
            isinstance(modules, list)
            and isinstance(declared_module_ids, list)
            and len(modules) == len(declared_module_ids),
            "module boundary differs from compiled cluster",
        )
        compiled_module_ids = [
            module.get("moduleId") if isinstance(module, dict) else None
            for module in modules
        ]
        _require(compiled_module_ids == declared_module_ids, "module boundary differs from cluster binding")
        _require(
            isinstance(cluster.get("pilotAssignmentId"), str)
            and isinstance(cluster.get("integrationContractId"), str)
            and type(cluster.get("budgetUnits")) is int
            and type(cluster.get("fallbackDeltaUnits")) is int,
            "cluster boundary has invalid values",
        )
        pilot_ids.append(cluster["pilotAssignmentId"])
        pilot_ids.extend(
            module.get("pilotAssignmentId") if isinstance(module, dict) else None
            for module in modules
        )
        module_ids.extend(compiled_module_ids)
        cluster_rows.append({
            "id": cluster.get("id"),
            "order": cluster["order"],
            "budgetUnits": cluster["budgetUnits"],
            "fallbackDeltaUnits": cluster["fallbackDeltaUnits"],
        })
    _require(
        all(isinstance(value, str) and value for value in module_ids)
        and len(module_ids) == 10
        and len(set(module_ids)) == 10,
        "module boundary requires ten unique cluster modules",
    )
    annual_pilot = compiled_protocol.get("annualPilot")
    _require(isinstance(annual_pilot, dict), "pilot boundary requires annual pilot")
    annual_pilot_id = annual_pilot.get("pilotAssignmentId")
    _require(isinstance(annual_pilot_id, str), "pilot boundary requires annual assignment")
    pilot_ids.append(annual_pilot_id)
    _require(len(pilot_ids) == 15 and len(set(pilot_ids)) == 15, "pilot boundary requires fifteen assignments")
    return pilot_ids, module_ids, cluster_rows


def compile_publication_contract(compiled_protocol, time_model, ium10_result):
    """Compile the closed IUM11 publication contract from validated inputs."""
    _require(isinstance(compiled_protocol, dict), "protocol boundary requires an object")
    _require(isinstance(ium10_result, dict), "IUM10 boundary requires an object")

    raw_variant = _single_raw_variant(time_model)
    raw_availability = _single_raw_availability(time_model)
    _require(
        _canonical_sha256(time_model) == _TIME_MODEL_FINGERPRINT,
        "fingerprint boundary differs from approved time model",
    )
    _require(
        compiled_protocol.get("timeModelFingerprint") == _TIME_MODEL_FINGERPRINT,
        "protocol fingerprint boundary differs from approved time model",
    )
    _require(
        compiled_protocol.get("timeModelFingerprintAlgorithm")
        == "sha256-canonical-json-v1",
        "fingerprint algorithm boundary differs",
    )
    _require(
        compiled_protocol.get("protocolVersion") == "1.0.0"
        and compiled_protocol.get("toolVersion") == "1.0.0",
        "source version boundary differs",
    )

    variants = ium10_result.get("annualVariants")
    _require(isinstance(variants, dict), "IUM10 variant boundary requires index")
    indexed_variant = variants.get(_VARIANT_ID)
    _require(isinstance(indexed_variant, dict), "IUM10 variant boundary requires working variant")
    raw_variant_without_allocations = {
        key: value for key, value in raw_variant.items() if key != "allocations"
    }
    indexed_variant_without_allocations = {
        key: value for key, value in indexed_variant.items() if key != "allocations"
    }
    _require(
        raw_variant_without_allocations == indexed_variant_without_allocations,
        "variant boundary differs between raw and IUM10",
    )
    _require(
        raw_variant.get("availabilityContractId") == _AVAILABILITY_CONTRACT_ID,
        "availability boundary differs from variant",
    )
    availability = ium10_result.get("availabilityContracts")
    _require(isinstance(availability, dict), "availability boundary requires IUM10 index")
    indexed_availability = availability.get(_AVAILABILITY_CONTRACT_ID)
    _require(isinstance(indexed_availability, dict), "availability boundary requires indexed contract")
    _require(raw_availability == indexed_availability, "availability boundary differs between raw and IUM10")

    judgement = _grade_7_judgement(ium10_result)
    pilot_ids, module_ids, cluster_rows = _referenced_pilot_ids(compiled_protocol)
    allocations = raw_variant.get("allocations")
    _require(isinstance(allocations, list), "module boundary requires allocations")
    _require(
        allocations == indexed_variant.get("allocations"),
        "module allocation boundary differs between raw and IUM10",
    )
    allocation_module_ids = [
        allocation.get("moduleId") if isinstance(allocation, dict) else None
        for allocation in allocations
    ]
    _require(
        allocation_module_ids == module_ids
        and len(allocation_module_ids) == 10
        and len(set(allocation_module_ids)) == 10,
        "module boundary differs from variant allocations",
    )
    _require(
        sum(allocation.get("units", 0) for allocation in allocations) == 40,
        "module allocation boundary differs from target units",
    )
    _require(
        raw_variant.get("targetUnits") == 40
        and compiled_protocol.get("annualPilot", {}).get("budgetUnits") == 40
        and sum(row["budgetUnits"] for row in cluster_rows) == 40,
        "core path boundary differs from 40 units",
    )
    _require(
        raw_variant.get("integrationContractIds")
        == [cluster.get("integrationContractId") for cluster in compiled_protocol["clusters"]],
        "cluster integration boundary differs from variant",
    )
    _require(
        raw_availability.get("fallbackDeltaUnitsByIntegrationContractId")
        == {
            cluster["integrationContractId"]: cluster["fallbackDeltaUnits"]
            for cluster in compiled_protocol["clusters"]
        },
        "cluster fallback boundary differs from availability",
    )

    pilot_assignments = ium10_result.get("pilotAssignments")
    _require(isinstance(pilot_assignments, dict), "pilot boundary requires IUM10 index")
    _require(
        all(
            isinstance(pilot_assignments.get(pilot_id), dict)
            and pilot_assignments[pilot_id].get("personalData") == "prohibited"
            for pilot_id in pilot_ids
        ),
        "privacy boundary requires prohibited personal data",
    )
    _require(
        compiled_protocol.get("minimumLearnerResponses") == 10,
        "privacy boundary requires ten learner responses",
    )
    _require(
        compiled_protocol.get("allowedRecommendation")
        == "eligible-for-working-availability-review",
        "recommendation boundary differs",
    )
    _require(
        compiled_protocol.get("forbiddenRecommendations") == ["reviewed", "standard"],
        "maturity boundary differs",
    )
    _require(
        "flexible-module-substitution"
        in raw_availability.get("forbiddenCompensations", []),
        "preservation boundary requires flexible-module-substitution prohibition",
    )

    gates = raw_availability.get("gates")
    _require(
        isinstance(gates, dict)
        and gates
        and all(isinstance(gate, dict) and gate.get("status") == "not-started" for gate in gates.values()),
        "availability boundary requires not-started gates",
    )
    for axis, expected in _CURRENT_AXES.items():
        if axis in ("status", "availabilityStatus"):
            _require(raw_variant.get(axis) == expected, f"{axis} boundary differs from raw variant")
            _require(indexed_variant.get(axis) == expected, f"{axis} boundary differs from IUM10 variant")
        elif axis == "status":
            _require(compiled_protocol.get(axis) == expected, "status boundary differs from protocol")
        else:
            _require(judgement.get(axis) == expected, f"{axis} boundary differs from Grade 7 judgement")
    _require(compiled_protocol.get("status") == "working", "status boundary differs from protocol")

    return {
        "schemaVersion": 1,
        "id": PUBLICATION_CONTRACT_ID,
        "contractVersion": PUBLICATION_CONTRACT_VERSION,
        "sourceBindings": {
            "protocolPath": "pilot/pilot-protocol.json",
            "timeModelPath": "roadmap/time-model.json",
            "protocolVersion": compiled_protocol.get("protocolVersion"),
            "toolVersion": compiled_protocol.get("toolVersion"),
            "timeModelFingerprintAlgorithm": compiled_protocol.get("timeModelFingerprintAlgorithm"),
            "timeModelFingerprint": compiled_protocol.get("timeModelFingerprint"),
        },
        "corePath": {
            "variantId": _VARIANT_ID,
            "targetUnits": 40,
            "clusterCount": 4,
            "moduleCount": 10,
            "pilotStageCount": 5,
            "clusters": cluster_rows,
        },
        "privacyBoundary": {
            "minimumLearnerResponses": compiled_protocol["minimumLearnerResponses"],
            "personalDataAllowed": False,
            "realPackagesInRepositoryAllowed": False,
        },
        "currentAxes": dict(_CURRENT_AXES),
        "statementBoundary": STATEMENT_BOUNDARY,
        "allowedRecommendation": compiled_protocol["allowedRecommendation"],
        "forbiddenMaturityValues": list(compiled_protocol["forbiddenRecommendations"]),
        "futureDecisionBoundary": {
            "requiresCommissionerDecision": True,
            "allowedChanges": [dict(change) for change in FUTURE_ALLOWED_CHANGES],
            "unchangedAxes": [dict(axis) for axis in UNCHANGED_AXES],
            "secondIndependentAnnualRunRequiredForMaturity": True,
        },
        "preservationBoundary": {
            "flexibleModulesOutsideCorePreserved": True,
            "flexibleModuleSubstitution": "forbidden",
        },
        "realPilotCompleted": False,
        "syntheticValidationOnly": True,
    }
