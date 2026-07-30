import hashlib
import json
from collections import Counter


BASELINE_COVERAGE_COMMIT = "69c9d4f5504a297289615b4169fc4a9ea6d9b253"
BASELINE_PARTIAL_COUNT = 60
BASELINE_RECORD_FINGERPRINT_SHA256 = (
    "b7602352c67f61cdf075a65df167e12f7283b8f62867386545fea758b6e08892"
)
BASELINE_MODULE_STRUCTURE_FINGERPRINT_SHA256 = (
    "da02be74104d88dd9adb0d7927feeab4eea5f65dcc616c5645b0f2145ca4d4fc"
)
CAUSE_CLASS_COUNTS = Counter(
    {
        "module-detail": 39,
        "school-context": 9,
        "private-local": 8,
        "roadmap-level": 4,
    }
)
EVIDENCE_MODES = {"module-detail", "school-context", "private-local"}
PRODUCT_VISIBILITIES = {"shared", "teacher-observable", "private-local"}
TIME_IMPACT_LEVELS = {
    "none-detected",
    "review-required",
    "roadmap-dependent",
}
GRAPH_IMPACT_LEVELS = {"none", "review-required"}
PRIVATE_BOUNDARY_TEXT = (
    "Das private lokale Artefakt wird nicht erhoben, übertragen, "
    "eingesammelt, gespeichert oder bewertet."
)


class IUM09ValidationError(ValueError):
    pass


def _require(condition, message):
    if not condition:
        raise IUM09ValidationError(message)


def _require_nonempty_string(value, field, contract_id):
    _require(
        isinstance(value, str) and value.strip(),
        f"{field} missing or invalid: {contract_id}",
    )


def _canonical_sha256(value):
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def module_structure_fingerprint(module_payload):
    structure = sorted(
        (
            {
                "id": module["id"],
                "grade": module["grade"],
                "kind": module["kind"],
                "prerequisiteModuleIds": sorted(
                    module["prerequisiteModuleIds"]
                ),
                "lessonRange": module["lessonRange"],
            }
            for module in module_payload["modules"]
        ),
        key=lambda record: record["id"],
    )
    return _canonical_sha256(structure)


def _validate_evidence_contract(contract, module):
    _require(isinstance(contract, dict), "evidence contract must be an object")
    required_fields = (
        "id",
        "competencyId",
        "mode",
        "learningAction",
        "productEvidence",
        "productVisibility",
    )
    missing_fields = [field for field in required_fields if field not in contract]
    _require(
        not missing_fields,
        f"evidence contract missing fields: {', '.join(missing_fields)}",
    )
    contract_id = contract["id"]
    for field in required_fields:
        _require_nonempty_string(contract[field], field, contract_id)

    module_id = module["id"]
    competency_id = contract["competencyId"]
    _require(
        contract_id == f"CE-{module_id}-{competency_id}",
        f"invalid evidence contract id: {contract_id}",
    )
    _require(
        contract["mode"] in EVIDENCE_MODES,
        f"invalid evidence mode: {contract_id}",
    )
    _require(
        contract["productVisibility"] in PRODUCT_VISIBILITIES,
        f"invalid product visibility: {contract_id}",
    )

    mode = contract["mode"]
    visibility = contract["productVisibility"]
    if mode == "module-detail":
        _require(
            visibility in {"shared", "teacher-observable"},
            f"module-detail needs shared or teacher-observable visibility: {contract_id}",
        )
    elif mode == "school-context":
        _require(
            visibility in {"shared", "teacher-observable"},
            f"school-context needs shared or teacher-observable visibility: {contract_id}",
        )
        _require(
            contract.get("executionType") == "actual-local-use",
            f"school-context needs actual-local-use: {contract_id}",
        )
        _require_nonempty_string(
            contract.get("localConfigurationRequirement"),
            "localConfigurationRequirement",
            contract_id,
        )
    else:
        _require(
            visibility == "private-local",
            f"private-local needs private-local visibility: {contract_id}",
        )
        _require(
            contract.get("privacyBoundary") == PRIVATE_BOUNDARY_TEXT,
            f"private-local privacyBoundary must match exactly: {contract_id}",
        )
        _require_nonempty_string(
            contract.get("nonPersonalFollowUp"),
            "nonPersonalFollowUp",
            contract_id,
        )


def validate_coverage_evidence(module_payload, curriculum_contracts):
    _require(isinstance(module_payload, dict), "module payload must be an object")
    modules = module_payload.get("modules")
    _require(isinstance(modules, list), "modules must be a list")
    _require(
        isinstance(curriculum_contracts, dict),
        "curriculum contracts must be a mapping",
    )

    evidence_contracts = {}
    for module in modules:
        _require(isinstance(module, dict), "module must be an object")
        module_id = module.get("id")
        _require_nonempty_string(module_id, "module id", "unknown module")
        if "coverageEvidence" not in module:
            continue
        evidence = module["coverageEvidence"]
        _require(
            isinstance(evidence, list) and bool(evidence),
            f"coverageEvidence must be a nonempty list: {module_id}",
        )
        _require(
            module.get("kind") == "core",
            f"coverage evidence requires a core module: {module_id}",
        )
        competency_ids = module.get("competencyIds")
        _require(
            isinstance(competency_ids, list),
            f"module competencyIds must be a list: {module_id}",
        )
        for contract in evidence:
            _validate_evidence_contract(contract, module)
            contract_id = contract["id"]
            competency_id = contract["competencyId"]
            _require(
                competency_id in curriculum_contracts,
                f"unknown competency: {competency_id}",
            )
            _require(
                competency_id in competency_ids,
                f"competency is not registered in module: {competency_id}",
            )
            _require(
                contract_id not in evidence_contracts,
                f"evidence contract ids must be unique: {contract_id}",
            )
            evidence_contracts[contract_id] = contract

    _require(
        module_structure_fingerprint(module_payload)
        == BASELINE_MODULE_STRUCTURE_FINGERPRINT_SHA256,
        "module structure fingerprint differs from immutable baseline",
    )
    return evidence_contracts
