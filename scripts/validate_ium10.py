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


class IUM10ValidationError(ValueError):
    pass


def _require(condition, message):
    if not condition:
        raise IUM10ValidationError(message)


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
