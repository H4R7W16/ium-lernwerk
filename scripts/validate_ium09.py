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
MODULE_DETAIL_IDS = frozenset(
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
    }
)
SCHOOL_CONTEXT_IDS = frozenset(
    {
        "BMB16-GYM-IK-GM-002", "BMB16-GYM-IK-KK-002",
        "BMB16-GYM-IK-KK-003", "BMB16-GYM-PK-HK-003",
        "BMB16-GYM-PK-SK-003", "INF7-16-GYM-PK-SV-001",
        "LH26-E-DA-015", "LH26-E-DP-001", "LH26-E-KS-001",
    }
)
PRIVATE_LOCAL_IDS = frozenset(
    {
        "BMB16-GYM-IK-MG-001", "BMB16-GYM-IK-MG-003",
        "BMB16-GYM-PK-RK-001", "BMB16-GYM-PK-RK-002",
        "BMB16-GYM-PK-RK-003", "LH26-E-DP-003", "LH26-E-DP-013",
        "LH26-E-DP-014",
    }
)
ROADMAP_LEVEL_IDS = frozenset(
    {
        "LH26-E-PROG-001", "LH26-E-PROG-002",
        "LH26-E-PROG-003", "LH26-E-PROG-004",
    }
)
BASELINE_PARTIAL_IDS = (
    MODULE_DETAIL_IDS
    | SCHOOL_CONTEXT_IDS
    | PRIVATE_LOCAL_IDS
    | ROADMAP_LEVEL_IDS
)
CAUSE_CLASS_BY_ID = {
    **dict.fromkeys(MODULE_DETAIL_IDS, "module-detail"),
    **dict.fromkeys(SCHOOL_CONTEXT_IDS, "school-context"),
    **dict.fromkeys(PRIVATE_LOCAL_IDS, "private-local"),
    **dict.fromkeys(ROADMAP_LEVEL_IDS, "roadmap-level"),
}
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


def coverage_baseline_fingerprint(entries):
    baseline_records = sorted(
        (
            {
                "competencyId": entry["competencyId"],
                "requirementText": entry["requirementText"],
                "before": {
                    "coverageStatus": entry["before"]["coverageStatus"],
                    "semanticAudit": entry["before"]["semanticAudit"],
                    "evidenceModuleId": entry["before"]["evidenceModuleId"],
                    "reason": entry["before"]["reason"],
                },
            }
            for entry in entries
        ),
        key=lambda record: record["competencyId"],
    )
    return _canonical_sha256(baseline_records)


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


def _require_exact_fields(payload, fields, context):
    _require(
        isinstance(payload, dict) and set(payload) == set(fields),
        f"invalid fields: {context}",
    )


def validate_remediation_ledger(
    remediation_payload,
    curriculum_contracts,
    evidence_contracts,
):
    _require_exact_fields(
        remediation_payload,
        {"schemaVersion", "status", "baseline", "entries"},
        "remediation ledger",
    )
    _require(remediation_payload["schemaVersion"] == 1, "invalid ledger schema")
    _require(remediation_payload["status"] == "working", "invalid ledger status")
    _require_exact_fields(
        remediation_payload["baseline"],
        {"coverageCommit", "partialCount", "recordFingerprintSha256"},
        "ledger baseline",
    )
    baseline = remediation_payload["baseline"]
    _require(
        baseline["coverageCommit"] == BASELINE_COVERAGE_COMMIT,
        "ledger coverage commit differs from immutable baseline",
    )
    _require(
        baseline["partialCount"] == BASELINE_PARTIAL_COUNT,
        "ledger partial count differs from immutable baseline",
    )
    _require(
        baseline["recordFingerprintSha256"]
        == BASELINE_RECORD_FINGERPRINT_SHA256,
        "ledger record fingerprint differs from immutable baseline",
    )
    entries = remediation_payload["entries"]
    _require(isinstance(entries, list), "ledger entries must be a list")
    _require(len(entries) == BASELINE_PARTIAL_COUNT, "ledger must contain 60 entries")
    _require(
        coverage_baseline_fingerprint(entries)
        == BASELINE_RECORD_FINGERPRINT_SHA256,
        "ledger before-record fingerprint differs from immutable baseline",
    )
    _require(isinstance(curriculum_contracts, dict), "curriculum contracts must be a mapping")
    _require(isinstance(evidence_contracts, dict), "evidence contracts must be a mapping")

    remediation_entries = {}
    for entry in entries:
        _require_exact_fields(
            entry,
            {
                "competencyId", "requirementText", "causeClass", "before",
                "decision", "evidenceContractId", "after", "changeRationale",
                "timeImpact", "graphImpact", "residualGap",
            },
            "remediation entry",
        )
        competency_id = entry["competencyId"]
        _require_nonempty_string(competency_id, "competencyId", "ledger entry")
        _require(
            competency_id not in remediation_entries,
            f"ledger competency ids must be unique: {competency_id}",
        )
        _require(
            competency_id in BASELINE_PARTIAL_IDS,
            f"unknown baseline competency: {competency_id}",
        )
        _require(
            entry["causeClass"] == CAUSE_CLASS_BY_ID[competency_id],
            f"invalid cause class: {competency_id}",
        )
        _require(
            competency_id in curriculum_contracts,
            f"unknown competency: {competency_id}",
        )
        curriculum_contract = curriculum_contracts[competency_id]
        _require(
            isinstance(curriculum_contract, dict)
            and curriculum_contract.get("text") == entry["requirementText"],
            f"requirement text differs from curriculum contract: {competency_id}",
        )
        _require_exact_fields(
            entry["before"],
            {"coverageStatus", "semanticAudit", "evidenceModuleId", "reason"},
            f"before record: {competency_id}",
        )
        _require(
            entry["before"]["coverageStatus"] == "partial"
            and entry["before"]["semanticAudit"] == "documented-gap",
            f"invalid before status: {competency_id}",
        )
        for field in ("evidenceModuleId", "reason", "requirementText", "changeRationale"):
            _require_nonempty_string(entry[field] if field in entry else entry["before"][field], field, competency_id)

        decision = entry["decision"]
        _require(decision in {"covered", "remain-partial"}, f"invalid decision: {competency_id}")
        _require_exact_fields(
            entry["after"],
            {"coverageStatus", "semanticAudit"},
            f"after record: {competency_id}",
        )
        _require_exact_fields(
            entry["timeImpact"], {"level", "rationale"}, f"time impact: {competency_id}"
        )
        _require_exact_fields(
            entry["graphImpact"], {"level", "rationale"}, f"graph impact: {competency_id}"
        )
        _require(
            entry["timeImpact"]["level"] in TIME_IMPACT_LEVELS,
            f"invalid time impact: {competency_id}",
        )
        _require(
            entry["graphImpact"]["level"] in GRAPH_IMPACT_LEVELS,
            f"invalid graph impact: {competency_id}",
        )
        _require_nonempty_string(entry["timeImpact"]["rationale"], "time rationale", competency_id)
        _require_nonempty_string(entry["graphImpact"]["rationale"], "graph rationale", competency_id)

        if decision == "covered":
            contract_id = entry["evidenceContractId"]
            _require_nonempty_string(contract_id, "evidenceContractId", competency_id)
            _require(contract_id in evidence_contracts, f"unknown evidence contract: {competency_id}")
            contract = evidence_contracts[contract_id]
            _require(
                contract["competencyId"] == competency_id,
                f"evidence contract has wrong competency: {competency_id}",
            )
            _require(
                contract_id
                == f"CE-{entry['before']['evidenceModuleId']}-{competency_id}",
                f"evidence contract differs from baseline module: {competency_id}",
            )
            _require(
                entry["after"] == {
                    "coverageStatus": "covered",
                    "semanticAudit": "operator-product-match",
                },
                f"invalid covered after status: {competency_id}",
            )
            _require(entry["residualGap"] is None, f"covered record has residual gap: {competency_id}")
        else:
            _require(entry["evidenceContractId"] is None, f"remain-partial has evidence contract: {competency_id}")
            _require(
                entry["after"] == {
                    "coverageStatus": "partial",
                    "semanticAudit": "documented-gap",
                },
                f"invalid remain-partial after status: {competency_id}",
            )
            _require_exact_fields(
                entry["residualGap"], {"reason", "risk", "followUp"}, f"residualGap: {competency_id}"
            )
            for field in ("reason", "risk", "followUp"):
                _require_nonempty_string(entry["residualGap"][field], f"residualGap.{field}", competency_id)

        if entry["graphImpact"]["level"] == "review-required":
            _require(decision == "remain-partial", f"graph review requires remain-partial: {competency_id}")
        if entry["causeClass"] == "roadmap-level":
            _require(decision == "remain-partial", f"roadmap-level must remain-partial: {competency_id}")
            _require(entry["evidenceContractId"] is None, f"roadmap-level has evidence contract: {competency_id}")
            _require(entry["timeImpact"]["level"] == "roadmap-dependent", f"roadmap-level must be roadmap-dependent: {competency_id}")
            _require(entry["graphImpact"]["level"] == "none", f"roadmap-level graph impact must be none: {competency_id}")
        remediation_entries[competency_id] = entry

    _require(
        set(remediation_entries) == BASELINE_PARTIAL_IDS,
        "ledger baseline competency ids differ from immutable baseline",
    )
    _require(
        Counter(entry["causeClass"] for entry in entries) == CAUSE_CLASS_COUNTS,
        "ledger cause class counts differ from immutable baseline",
    )
    return remediation_entries


def validate_remediated_coverage(
    coverage_payload,
    remediation_entries,
    evidence_contracts,
    curriculum_contracts,
):
    """Validate the fail-closed IUM09 coverage-plan projection."""
    _require(isinstance(coverage_payload, dict), "coverage payload must be an object")
    entries = coverage_payload.get("entries")
    _require(isinstance(entries, list) and bool(entries), "coverage entries must be a nonempty list")
    _require(isinstance(remediation_entries, dict), "remediation entries must be a mapping")
    _require(isinstance(evidence_contracts, dict), "evidence contracts must be a mapping")
    _require(isinstance(curriculum_contracts, dict), "curriculum contracts must be a mapping")

    coverage_entries = {}
    for entry in entries:
        _require(isinstance(entry, dict), "coverage entry must be an object")
        competency_id = entry.get("competencyId")
        _require_nonempty_string(competency_id, "competencyId", "coverage entry")
        _require(
            competency_id not in coverage_entries,
            f"coverage competency ids must be unique: {competency_id}",
        )
        coverage_entries[competency_id] = entry

    _require(
        set(coverage_entries) == set(curriculum_contracts),
        "coverage competency ids differ from curriculum contracts",
    )
    _require(
        set(remediation_entries) <= set(coverage_entries),
        "remediation competency ids are missing from coverage",
    )

    referenced_contract_ids = []
    for competency_id, entry in coverage_entries.items():
        if competency_id not in remediation_entries:
            _require(
                entry.get("coverageStatus") == "covered"
                and entry.get("semanticAudit") == "operator-product-match",
                f"legacy covered record changed status: {competency_id}",
            )
            _require(
                "evidenceContractId" not in entry,
                f"legacy covered record has evidenceContractId: {competency_id}",
            )
            continue

        remediation = remediation_entries[competency_id]
        _require(isinstance(remediation, dict), f"invalid remediation entry: {competency_id}")
        expected_after = remediation.get("after")
        _require(
            isinstance(expected_after, dict),
            f"invalid remediation after status: {competency_id}",
        )
        _require(
            entry.get("coverageStatus") == expected_after.get("coverageStatus")
            and entry.get("semanticAudit") == expected_after.get("semanticAudit"),
            f"coverage status differs from remediation ledger: {competency_id}",
        )
        _require(
            entry.get("requirementText") == remediation.get("requirementText")
            == curriculum_contracts[competency_id].get("text"),
            f"coverage requirement text differs from remediation ledger: {competency_id}",
        )

        if remediation.get("decision") == "covered":
            contract_id = remediation.get("evidenceContractId")
            _require_nonempty_string(contract_id, "evidenceContractId", competency_id)
            _require(
                entry.get("evidenceContractId") == contract_id,
                f"coverage evidence contract differs from remediation ledger: {competency_id}",
            )
            _require(
                contract_id in evidence_contracts,
                f"unknown evidence contract: {competency_id}",
            )
            contract = evidence_contracts[contract_id]
            _require(
                isinstance(contract, dict)
                and contract.get("competencyId") == competency_id,
                f"evidence contract has wrong competency: {competency_id}",
            )
            for field in ("requirementText", "learningAction", "productEvidence"):
                value = (
                    entry["requirementText"]
                    if field == "requirementText"
                    else contract.get(field)
                )
                _require_nonempty_string(value, field, competency_id)
                _require(
                    isinstance(entry.get("evidence"), str) and value in entry["evidence"],
                    f"coverage evidence lacks {field}: {competency_id}",
                )
                _require(
                    isinstance(entry.get("matchRationale"), str)
                    and value in entry["matchRationale"],
                    f"coverage rationale lacks {field}: {competency_id}",
                )
            referenced_contract_ids.append(contract_id)
        elif remediation.get("decision") == "remain-partial":
            _require(
                "evidenceContractId" not in entry,
                f"remain-partial record has evidenceContractId: {competency_id}",
            )
            residual_gap = remediation.get("residualGap")
            _require(isinstance(residual_gap, dict), f"invalid residual gap: {competency_id}")
            for field in ("reason", "risk", "followUp"):
                _require(
                    entry.get(field) == residual_gap.get(field),
                    f"coverage residual {field} differs from remediation ledger: {competency_id}",
                )
        else:
            raise IUM09ValidationError(
                f"invalid remediation decision: {competency_id}"
            )

    _require(
        len(referenced_contract_ids) == len(set(referenced_contract_ids)),
        "evidence contracts must be referenced exactly once",
    )
    _require(
        set(referenced_contract_ids) == set(evidence_contracts),
        "evidence contracts must be referenced by a covered ledger decision",
    )
    return set(coverage_entries)


def validate_ium09(
    module_payload,
    coverage_payload,
    remediation_payload,
    curriculum_contracts,
):
    """Validate the complete IUM09 chain and return both record maps."""
    evidence_contracts = validate_coverage_evidence(
        module_payload,
        curriculum_contracts,
    )
    remediation_entries = validate_remediation_ledger(
        remediation_payload,
        curriculum_contracts,
        evidence_contracts,
    )
    validate_remediated_coverage(
        coverage_payload,
        remediation_entries,
        evidence_contracts,
        curriculum_contracts,
    )
    return {
        "evidenceContracts": evidence_contracts,
        "remediationEntries": remediation_entries,
    }
