import argparse
import copy
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

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
PRIVACY_CONTRACT_FIELDS = {
    "id",
    "moduleId",
    "scope",
    "artifactOwner",
    "artifactCustody",
    "institutionalHandling",
    "status",
}
INSTITUTIONAL_HANDLING_FIELDS = {
    "access",
    "observation",
    "collection",
    "transfer",
    "storage",
    "assessment",
}
TIME_REVIEW_FIELDS = {
    "id",
    "competencyId",
    "moduleId",
    "sourceTimeImpactLevel",
    "decision",
    "rationale",
    "phaseIds",
    "additionalMinutes",
    "integrationContractIds",
    "sequenceEvidenceId",
    "pathAvailability",
    "coverageConsequence",
    "risk",
    "followUp",
    "status",
}
PRIVACY_DISPOSITION_FIELDS = {
    "contractId",
    "observableBasis",
    "evidenceContractId",
    "privateArtifactContribution",
    "privateActivityTimeTreatment",
}
PRIVATE_ARTIFACT_CONTRIBUTION_FIELDS = {
    "product",
    "evidence",
    "additionalTimeClaim",
}
OBSERVABLE_BASES = {
    "nonpersonal-follow-up",
    "nonpersonal-module-detail",
    "none",
}
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
GRADE_7_INTEGRATION_IDS = frozenset(
    {
        "INT-7-DATA-CODING",
        "INT-7-PROGRAMMING",
        "INT-7-NET-SECURITY",
        "INT-7-DATA-MEDIA-SOCIETY",
    }
)
GRADE_7_CORE_MODULE_IDS = frozenset(
    {
        "IUM-7-CORE-01",
        "IUM-7-CORE-02",
        "IUM-7-CORE-03",
        "IUM-7-CORE-04",
        "IUM-7-CORE-05",
        "IUM-7-CORE-06",
        "IUM-7-CORE-07",
        "IUM-7-CORE-08",
        "IUM-7-CORE-09",
        "IUM-7-CORE-10",
    }
)
GRADE_7_FLEX_RANGES = {
    "IUM-7-EXT-01": {"min": 3, "recommended": 4, "max": 5},
    "IUM-7-TRANSFER-01": {"min": 3, "recommended": 4, "max": 5},
    "IUM-7-PROJECT-01": {"min": 8, "recommended": 10, "max": 12},
}
GRADE_7_CORE_UNITS = {
    "IUM-7-CORE-01": {"optimized": 5, "robust": 5, "historical-minimum": 6},
    "IUM-7-CORE-02": {"optimized": 3, "robust": 4, "historical-minimum": 5},
    "IUM-7-CORE-03": {"optimized": 5, "robust": 5, "historical-minimum": 6},
    "IUM-7-CORE-04": {"optimized": 6, "robust": 6, "historical-minimum": 7},
    "IUM-7-CORE-05": {"optimized": 4, "robust": 4, "historical-minimum": 5},
    "IUM-7-CORE-06": {"optimized": 3, "robust": 3, "historical-minimum": 4},
    "IUM-7-CORE-07": {"optimized": 4, "robust": 4, "historical-minimum": 5},
    "IUM-7-CORE-08": {"optimized": 4, "robust": 6, "historical-minimum": 6},
    "IUM-7-CORE-09": {"optimized": 2, "robust": 3, "historical-minimum": 4},
    "IUM-7-CORE-10": {"optimized": 4, "robust": 6, "historical-minimum": 6},
}
GRADE_7_INTEGRATION_BOUNDS = {
    "INT-7-DATA-CODING": {
        "moduleIds": ["IUM-7-CORE-01", "IUM-7-CORE-02"],
        "pathIds": ["optimized", "robust"],
        "countedInModuleId": "IUM-7-CORE-02",
        "sharedMinutes": 90,
        "savingsMinutesByPath": {"optimized": 135, "robust": 90},
    },
    "INT-7-PROGRAMMING": {
        "moduleIds": ["IUM-7-CORE-03", "IUM-7-CORE-04"],
        "pathIds": ["optimized", "robust"],
        "countedInModuleId": "IUM-7-CORE-04",
        "sharedMinutes": 90,
        "savingsMinutesByPath": {"optimized": 90, "robust": 90},
    },
    "INT-7-NET-SECURITY": {
        "moduleIds": [
            "IUM-7-CORE-05",
            "IUM-7-CORE-06",
            "IUM-7-CORE-07",
        ],
        "pathIds": ["optimized", "robust"],
        "countedInModuleId": "IUM-7-CORE-07",
        "sharedMinutes": 135,
        "savingsMinutesByPath": {"optimized": 135, "robust": 135},
    },
    "INT-7-DATA-MEDIA-SOCIETY": {
        "moduleIds": [
            "IUM-7-CORE-08",
            "IUM-7-CORE-09",
            "IUM-7-CORE-10",
        ],
        "pathIds": ["optimized", "robust"],
        "countedInModuleId": "IUM-7-CORE-10",
        "sharedMinutes": 45,
        "savingsMinutesByPath": {"optimized": 270, "robust": 45},
    },
}
GRADE_7_VARIANT_TARGETS = {
    "GRADE-7-OPTIMIZED-DEMAND": ("optimized", 40),
    "GRADE-7-ROBUST-DEMAND": ("robust", 46),
    "GRADE-7-HISTORICAL-MINIMUM": ("historical-minimum", 54),
}
GRADE_7_VARIANT_INTEGRATIONS = {
    "GRADE-7-OPTIMIZED-DEMAND": GRADE_7_INTEGRATION_IDS,
    "GRADE-7-ROBUST-DEMAND": GRADE_7_INTEGRATION_IDS,
    "GRADE-7-HISTORICAL-MINIMUM": frozenset(),
}
GRADE_7_DECISION_OPTIONS = [
    "additional-school-time",
    "structural-integration-or-reclassification",
    "curricular-reprioritisation",
    "earlier-preparation",
    "explicitly-incomplete-path",
]
GRADE_7_UNIMPLEMENTED_OPTIONS_RATIONALE = (
    "Die drei vollständigen Kernbedarfsrechnungen liegen bei 40, 46 und 54 "
    "Unterrichtseinheiten. Selbst die unpilotierte optimierte Untergrenze "
    "überschreitet 30/34/38; daher existiert kein verfügbares "
    "Klasse-7-Angebot und das Zeiturteil bleibt red. Keine der fünf "
    "Folgeoptionen ist umgesetzt."
)
GRADE_6_INTEGRATION_BOUNDS = {
    "INT-6-ACTORS-SELECTION": {
        "moduleIds": ["IUM-6-CORE-01", "IUM-6-CORE-02"],
        "pathIds": ["baseline", "regular"],
        "countedInModuleId": "IUM-6-CORE-01",
        "sharedMinutes": 90,
        "savingsMinutesByPath": {"baseline": 90, "regular": 45},
    },
    "INT-6-CONFLICT-PRODUCTION": {
        "moduleIds": ["IUM-6-CORE-06", "IUM-6-CORE-07"],
        "pathIds": ["baseline", "regular"],
        "countedInModuleId": "IUM-6-CORE-07",
        "sharedMinutes": 90,
        "savingsMinutesByPath": {"baseline": 90, "regular": 0},
    },
    "INT-6-ALGORITHM-REVISIT": {
        "moduleIds": ["IUM-5-CORE-05", "IUM-6-CORE-04"],
        "pathIds": ["baseline", "regular"],
        "countedInModuleId": "IUM-6-CORE-04",
        "sharedMinutes": 45,
        "savingsMinutesByPath": {"baseline": 45, "regular": 0},
    },
}
GRADE_6_VARIANT_TARGETS = {
    "GRADE-6-BASELINE": ("baseline", 30),
    "GRADE-6-REGULAR": ("regular", 34),
    "GRADE-6-EXTENDED-REFERENCE": ("extended", 38),
    "GRADE-6-EXTENDED-TRANSFER": ("extended", 38),
    "GRADE-6-EXTENDED-CODING": ("extended", 38),
}
_GRADE_6_BASELINE_ALLOCATIONS = {
    "IUM-6-CORE-01": ("baseline", 5),
    "IUM-6-CORE-02": ("baseline", 4),
    "IUM-6-CORE-03": ("baseline", 4),
    "IUM-6-CORE-04": ("baseline", 4),
    "IUM-6-CORE-05": ("baseline", 4),
    "IUM-6-CORE-06": ("baseline", 4),
    "IUM-6-CORE-07": ("baseline", 5),
}
_GRADE_6_REGULAR_ALLOCATIONS = {
    "IUM-6-CORE-01": ("regular", 6),
    "IUM-6-CORE-02": ("regular", 5),
    "IUM-6-CORE-03": ("regular", 4),
    "IUM-6-CORE-04": ("regular", 5),
    "IUM-6-CORE-05": ("regular", 4),
    "IUM-6-CORE-06": ("regular", 4),
    "IUM-6-CORE-07": ("regular", 6),
}
GRADE_6_VARIANT_BOUNDS = {
    "GRADE-6-BASELINE": {
        "allocations": _GRADE_6_BASELINE_ALLOCATIONS,
        "integrationContractIds": GRADE_6_INTEGRATION_IDS,
    },
    "GRADE-6-REGULAR": {
        "allocations": _GRADE_6_REGULAR_ALLOCATIONS,
        "integrationContractIds": GRADE_6_INTEGRATION_IDS,
    },
    "GRADE-6-EXTENDED-REFERENCE": {
        "allocations": {
            **_GRADE_6_REGULAR_ALLOCATIONS,
            "IUM-6-EXT-01": ("standalone", 4),
        },
        "integrationContractIds": GRADE_6_INTEGRATION_IDS,
    },
    "GRADE-6-EXTENDED-TRANSFER": {
        "allocations": {
            **_GRADE_6_REGULAR_ALLOCATIONS,
            "IUM-6-TRANSFER-01": ("standalone", 4),
        },
        "integrationContractIds": GRADE_6_INTEGRATION_IDS,
    },
    "GRADE-6-EXTENDED-CODING": {
        "allocations": {
            **_GRADE_6_REGULAR_ALLOCATIONS,
            "IUM-6-CORE-04": ("targeted-extension", 6),
            "IUM-6-EXT-02": ("standalone", 3),
        },
        "integrationContractIds": frozenset(
            {
                "INT-6-ACTORS-SELECTION",
                "INT-6-CONFLICT-PRODUCTION",
            }
        ),
    },
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


def _has_grade_6_orchestration(time_model, module_payload=None):
    integration_contracts = time_model.get("integrationContracts", [])
    annual_variants = time_model.get("annualVariants", [])
    grade_judgements = time_model.get("gradeJudgements", [])
    modules = (
        module_payload.get("modules", [])
        if isinstance(module_payload, dict)
        else []
    )
    grade_6_module_ids = {
        module.get("id")
        for module in modules
        if isinstance(module, dict)
        and module.get("grade") == 6
        and isinstance(module.get("id"), str)
    }
    return (
        any(
            isinstance(contract, dict)
            and (
                contract.get("id") in GRADE_6_INTEGRATION_IDS
                or any(
                    module_id in grade_6_module_ids
                    for module_id in contract.get("moduleIds", [])
                    if isinstance(module_id, str)
                )
            )
            for contract in integration_contracts
        )
        or any(
            isinstance(variant, dict) and variant.get("grade") == 6
            for variant in annual_variants
        )
        or any(
            isinstance(judgement, dict) and judgement.get("grade") == 6
            for judgement in grade_judgements
        )
    )


def _has_grade_7_orchestration(time_model, module_payload=None):
    integration_contracts = time_model.get("integrationContracts", [])
    annual_variants = time_model.get("annualVariants", [])
    grade_judgements = time_model.get("gradeJudgements", [])
    modules = (
        module_payload.get("modules", [])
        if isinstance(module_payload, dict)
        else []
    )
    grade_7_module_ids = {
        module.get("id")
        for module in modules
        if isinstance(module, dict)
        and module.get("grade") == 7
        and isinstance(module.get("id"), str)
    }
    return (
        any(
            isinstance(contract, dict)
            and (
                contract.get("id") in GRADE_7_INTEGRATION_IDS
                or any(
                    module_id in grade_7_module_ids
                    for module_id in contract.get("moduleIds", [])
                    if isinstance(module_id, str)
                )
            )
            for contract in integration_contracts
        )
        or any(
            isinstance(variant, dict) and variant.get("grade") == 7
            for variant in annual_variants
        )
        or any(
            isinstance(judgement, dict) and judgement.get("grade") == 7
            for judgement in grade_judgements
        )
    )


def _validate_grade_6_judgement(
    time_model,
    module_contracts,
    integration_contracts,
    annual_variants,
):
    grade_judgements = time_model.get("gradeJudgements")
    _require(
        isinstance(module_contracts, dict)
        and isinstance(integration_contracts, dict)
        and isinstance(annual_variants, dict)
        and isinstance(grade_judgements, list),
        "validated grade 6 orchestration indices and judgements are required",
    )

    grade_6_module_contracts = {
        module_id: contract
        for module_id, contract in module_contracts.items()
        if contract.get("grade") == 6
    }
    grade_6_integrations = {
        integration_id: contract
        for integration_id, contract in integration_contracts.items()
        if (
            integration_id in GRADE_6_INTEGRATION_IDS
            or any(
                module_contracts.get(module_id, {}).get("grade") == 6
                for module_id in contract.get("moduleIds", [])
                if isinstance(module_id, str)
            )
        )
    }
    grade_6_variants = {
        variant_id: variant
        for variant_id, variant in annual_variants.items()
        if variant.get("grade") == 6
    }
    grade_6_judgements = [
        judgement
        for judgement in grade_judgements
        if isinstance(judgement, dict) and judgement.get("grade") == 6
    ]
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

    residuals = set()
    expected_grade_6_module_ids = GRADE_6_CORE_MODULE_IDS | {
        "IUM-6-EXT-01",
        "IUM-6-EXT-02",
        "IUM-6-TRANSFER-01",
        "IUM-6-PROJECT-01",
    }
    actual_grade_6_module_ids = set(grade_6_module_contracts)
    for module_id in expected_grade_6_module_ids - actual_grade_6_module_ids:
        residuals.add((module_id, "missing-record"))
    for module_id in actual_grade_6_module_ids - expected_grade_6_module_ids:
        residuals.add((module_id, "unexpected-record"))

    actual_grade_6_integration_ids = set(grade_6_integrations)
    expected_grade_6_integration_ids = set(GRADE_6_INTEGRATION_IDS)
    for integration_id in (
        expected_grade_6_integration_ids - actual_grade_6_integration_ids
    ):
        residuals.add((integration_id, "missing-record"))
    for integration_id in (
        actual_grade_6_integration_ids - expected_grade_6_integration_ids
    ):
        residuals.add((integration_id, "unexpected-record"))
    for integration_id, expected_bounds in GRADE_6_INTEGRATION_BOUNDS.items():
        integration = grade_6_integrations.get(integration_id)
        if not isinstance(integration, dict):
            continue
        actual_bounds = (
            {
                field: integration.get(field)
                for field in expected_bounds
            }
        )
        if actual_bounds != expected_bounds:
            residuals.add((integration_id, "contract-bounds-mismatch"))
        if integration.get("status") not in {"working", "reviewed"}:
            residuals.add((integration_id, "status-not-ready"))

    actual_grade_6_variant_ids = set(grade_6_variants)
    expected_grade_6_variant_ids = set(GRADE_6_VARIANT_TARGETS)
    for variant_id in expected_grade_6_variant_ids - actual_grade_6_variant_ids:
        residuals.add((variant_id, "missing-record"))
    for variant_id in actual_grade_6_variant_ids - expected_grade_6_variant_ids:
        residuals.add((variant_id, "unexpected-record"))
    for variant_id, (path_id, target_units) in GRADE_6_VARIANT_TARGETS.items():
        variant = grade_6_variants.get(variant_id)
        if not isinstance(variant, dict):
            continue
        expected_bounds = GRADE_6_VARIANT_BOUNDS[variant_id]
        actual_allocations = {
            allocation["moduleId"]: (
                allocation["budgetPathId"],
                allocation["units"],
            )
            for allocation in variant.get("allocations", [])
        }
        if (
            variant.get("pathId") != path_id
            or variant.get("targetUnits") != target_units
            or actual_allocations != expected_bounds["allocations"]
            or set(variant.get("integrationContractIds", []))
            != set(expected_bounds["integrationContractIds"])
        ):
            residuals.add((variant_id, "contract-bounds-mismatch"))
        if variant.get("available") is not True:
            residuals.add((variant_id, "unavailable"))
        if variant.get("status") not in {"working", "reviewed"}:
            residuals.add((variant_id, "status-not-ready"))

    ready_for_green = not residuals
    _require(
        (judgement["timeFeasibilityStatus"] == "green") == ready_for_green,
        "grade 6 green judgement requires exact 30/34/38 variants and passing integrations",
    )
    if not ready_for_green:
        residual_text = f"{judgement['rationale']} {judgement['risk']}"
        required_evidence = {
            f"{record_id} [{cause_code}]"
            for record_id, cause_code in residuals
        }
        _require(
            all(evidence in residual_text for evidence in required_evidence),
            "grade 6 amber judgement must name every residual record ID and cause",
        )


def _validate_grade_7_judgement(
    time_model,
    module_contracts,
    integration_contracts,
    annual_variants,
):
    grade_judgements = time_model.get("gradeJudgements")
    _require(
        isinstance(module_contracts, dict)
        and isinstance(integration_contracts, dict)
        and isinstance(annual_variants, dict)
        and isinstance(grade_judgements, list),
        "validated grade 7 orchestration indices and judgements are required",
    )

    grade_7_module_contracts = {
        module_id: contract
        for module_id, contract in module_contracts.items()
        if contract.get("grade") == 7
    }
    grade_7_integrations = {
        integration_id: contract
        for integration_id, contract in integration_contracts.items()
        if (
            integration_id in GRADE_7_INTEGRATION_IDS
            or any(
                module_contracts.get(module_id, {}).get("grade") == 7
                for module_id in contract.get("moduleIds", [])
                if isinstance(module_id, str)
            )
        )
    }
    grade_7_variants = {
        variant_id: variant
        for variant_id, variant in annual_variants.items()
        if (
            variant.get("grade") == 7
            or any(
                module_contracts.get(allocation.get("moduleId"), {}).get("grade")
                == 7
                for allocation in variant.get("allocations", [])
                if isinstance(allocation, dict)
            )
        )
    }
    grade_7_variant_ids = set(grade_7_variants)
    grade_7_judgements = [
        judgement
        for judgement in grade_judgements
        if (
            isinstance(judgement, dict)
            and (
                judgement.get("grade") == 7
                or bool(
                    set(judgement.get("annualVariantIds", []))
                    & grade_7_variant_ids
                )
            )
        )
    ]
    _require(
        len(grade_7_judgements) == 1,
        "grade 7 orchestration needs exactly one judgement",
    )
    judgement = grade_7_judgements[0]
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
        "grade 7 judgement fields differ from the IUM10 contract",
    )
    _require(
        judgement["grade"] == 7
        and judgement["semanticCoverageStatus"] == "partial"
        and judgement["timeFeasibilityStatus"] == "red"
        and judgement["sequenceEvidenceStatus"] == "partial"
        and judgement["pilotStatus"] == "not-started",
        "grade 7 status dimensions must remain partial/red/partial/not-started",
    )
    _require(
        judgement["annualVariantIds"] == list(GRADE_7_VARIANT_TARGETS),
        "grade 7 judgement must reference the exact demand scenarios",
    )
    _require(
        judgement["decisionOptions"] == GRADE_7_DECISION_OPTIONS,
        "grade 7 judgement must retain exactly five unimplemented options",
    )
    for field in ("rationale", "risk"):
        _require(
            isinstance(judgement[field], str) and judgement[field].strip(),
            f"grade 7 judgement {field} must be a nonempty string",
        )
    _require(
        judgement["rationale"] == GRADE_7_UNIMPLEMENTED_OPTIONS_RATIONALE,
        "grade 7 judgement must use the canonical unimplemented-options rationale",
    )

    expected_module_ids = GRADE_7_CORE_MODULE_IDS | set(GRADE_7_FLEX_RANGES)
    _require(
        set(grade_7_module_contracts) == expected_module_ids,
        "grade 7 needs exactly thirteen task 7 module contracts",
    )
    for module_id, expected_paths in GRADE_7_CORE_UNITS.items():
        contract = grade_7_module_contracts[module_id]
        actual_paths = {
            budget["pathId"]: budget["units"]
            for budget in contract.get("pathBudgets", [])
            if isinstance(budget, dict)
        }
        _require(
            contract.get("kind") == "core"
            and actual_paths == expected_paths
            and contract.get("status") in CONTRACT_STATUSES,
            f"grade 7 core matrix differs from the approved contract: {module_id}",
        )
    for module_id, expected_range in GRADE_7_FLEX_RANGES.items():
        contract = grade_7_module_contracts[module_id]
        budgets = contract.get("pathBudgets", [])
        _require(
            contract.get("kind") != "core"
            and contract.get("standaloneUnitRange") == expected_range
            and len(budgets) == 1
            and budgets[0].get("pathId") == "standalone"
            and budgets[0].get("units") == expected_range["recommended"]
            and contract.get("status") in CONTRACT_STATUSES,
            f"grade 7 flex range differs from the approved contract: {module_id}",
        )

    _require(
        set(grade_7_integrations) == set(GRADE_7_INTEGRATION_IDS),
        "grade 7 needs exactly four approved cluster integrations",
    )
    for integration_id, expected_bounds in GRADE_7_INTEGRATION_BOUNDS.items():
        integration = grade_7_integrations[integration_id]
        actual_bounds = {
            field: integration.get(field) for field in expected_bounds
        }
        _require(
            actual_bounds == expected_bounds
            and integration.get("status") in {"working", "reviewed"},
            f"grade 7 cluster bounds differ from the approved contract: {integration_id}",
        )

    _require(
        set(grade_7_variants) == set(GRADE_7_VARIANT_TARGETS),
        "grade 7 permits only the three approved demand scenarios",
    )
    for variant_id, (path_id, target_units) in GRADE_7_VARIANT_TARGETS.items():
        variant = grade_7_variants[variant_id]
        actual_allocations = {
            allocation["moduleId"]: (
                allocation["budgetPathId"],
                allocation["units"],
            )
            for allocation in variant.get("allocations", [])
            if isinstance(allocation, dict)
        }
        expected_allocations = {
            module_id: (path_id, path_units[path_id])
            for module_id, path_units in GRADE_7_CORE_UNITS.items()
        }
        _require(
            variant.get("grade") == 7
            and variant.get("kind") == "demand-scenario"
            and variant.get("pathId") == path_id
            and variant.get("targetUnits") == target_units
            and actual_allocations == expected_allocations
            and set(variant.get("integrationContractIds", []))
            == set(GRADE_7_VARIANT_INTEGRATIONS[variant_id])
            and variant.get("available") is False
            and variant.get("status") in {"working", "reviewed"},
            f"grade 7 demand scenario differs from the approved contract: {variant_id}",
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


def validate_privacy_contracts(privacy_contracts, module_contracts):
    """Validate privacy contracts and return them keyed by contract id."""
    _require(
        isinstance(privacy_contracts, list),
        "privacy contracts must be a list",
    )
    _require(
        isinstance(module_contracts, dict),
        "validated module contracts must be keyed by module id",
    )

    contracts_by_id = {}
    contracted_module_ids = set()
    for contract in privacy_contracts:
        _require(isinstance(contract, dict), "privacy contract must be an object")
        module_reference = contract.get("moduleId", "<missing moduleId>")
        missing_fields = sorted(PRIVACY_CONTRACT_FIELDS - set(contract))
        unexpected_fields = sorted(set(contract) - PRIVACY_CONTRACT_FIELDS)
        _require(
            not missing_fields and not unexpected_fields,
            "privacy contract "
            f"{module_reference} fields differ: "
            f"missing {missing_fields}; unexpected {unexpected_fields}",
        )
        module_id = contract["moduleId"]
        contract_id = contract["id"]
        _require(
            isinstance(module_id, str) and module_id in module_contracts,
            f"privacy contract references unknown module: {module_id}",
        )
        _require(
            contract_id == f"PC-{module_id}",
            f"invalid privacy contract id: {module_id}",
        )
        _require(
            contract_id not in contracts_by_id
            and module_id not in contracted_module_ids,
            f"privacy contract ids and module ids must be unique: {module_id}",
        )
        _require(
            contract["scope"] == "private-local-reflection",
            f"invalid privacy scope: {module_id}",
        )
        _require(
            contract["artifactOwner"] == "learner",
            f"invalid artifactOwner: {module_id}",
        )
        _require(
            contract["artifactCustody"] == "learner-controlled",
            f"invalid artifactCustody: {module_id}",
        )
        handling = contract["institutionalHandling"]
        _require(
            isinstance(handling, dict)
            and set(handling) == INSTITUTIONAL_HANDLING_FIELDS,
            f"invalid institutionalHandling fields: {module_id}",
        )
        for field in sorted(INSTITUTIONAL_HANDLING_FIELDS):
            _require(
                handling[field] == "prohibited",
                f"{module_id} institutional handling {field} must be prohibited",
            )
        _require(
            isinstance(contract["status"], str)
            and contract["status"] in CONTRACT_STATUSES,
            f"invalid privacy status: {module_id}",
        )
        contracts_by_id[contract_id] = contract
        contracted_module_ids.add(module_id)
    return contracts_by_id


def validate_time_model_draft(time_model, module_payload=None):
    """Validate the draft and its available module-time orchestration."""
    _require(isinstance(time_model, dict), "time model draft must be an object")
    schema_version = time_model.get("schemaVersion")
    _require(
        isinstance(schema_version, int)
        and not isinstance(schema_version, bool)
        and schema_version == 2,
        "schema version must be the integer 2",
    )
    has_grade_6_orchestration = _has_grade_6_orchestration(
        time_model,
        module_payload,
    )
    has_grade_7_orchestration = _has_grade_7_orchestration(
        time_model,
        module_payload,
    )
    grade_7_is_in_current_scope = (
        isinstance(module_payload, dict)
        and any(
            isinstance(module, dict) and module.get("grade") == 7
            for module in module_payload.get("modules", [])
        )
    )
    has_grade_7_orchestration = (
        has_grade_7_orchestration or grade_7_is_in_current_scope
    )
    if has_grade_6_orchestration or has_grade_7_orchestration:
        _require(
            isinstance(module_payload, dict)
            and isinstance(module_payload.get("modules"), list),
            "grade 6/7 draft validation requires the module graph payload",
        )
        module_contract_records = time_model.get("moduleContracts")
        _require(
            isinstance(module_contract_records, list),
            "module contracts must be a list",
        )
        contracted_grades = {
            contract.get("grade")
            for contract in module_contract_records
            if isinstance(contract, dict) and _positive_int(contract.get("grade"))
        }
        scoped_module_payload = {
            "modules": [
                module
                for module in module_payload["modules"]
                if isinstance(module, dict)
                and module.get("grade") in contracted_grades
            ]
        }
        validated_module_contracts = validate_module_contracts(
            module_contract_records,
            scoped_module_payload,
        )
        validate_privacy_contracts(
            time_model.get("privacyContracts"),
            validated_module_contracts,
        )
        validated_integration_contracts = validate_integration_contracts(
            time_model.get("integrationContracts"),
            validated_module_contracts,
        )
        validated_annual_variants = validate_annual_variants(
            time_model.get("annualVariants"),
            validated_module_contracts,
            validated_integration_contracts,
        )
        if has_grade_6_orchestration:
            _validate_grade_6_judgement(
                time_model,
                validated_module_contracts,
                validated_integration_contracts,
                validated_annual_variants,
            )
        if has_grade_7_orchestration:
            _validate_grade_7_judgement(
                time_model,
                validated_module_contracts,
                validated_integration_contracts,
                validated_annual_variants,
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
        expected_grade_7_bounds = GRADE_7_INTEGRATION_BOUNDS.get(contract_id)
        matches_approved_grade_7_bounds = (
            isinstance(expected_grade_7_bounds, dict)
            and all(
                contract.get(field) == expected_value
                for field, expected_value in expected_grade_7_bounds.items()
            )
            and contract.get("status") in {"working", "reviewed"}
        )
        _require(
            all(_nonnegative_int(minutes) for minutes in savings.values())
            and (
                all(minutes <= shared_minutes for minutes in savings.values())
                or matches_approved_grade_7_bounds
            ),
            "integration savings must stay within shared minutes unless the "
            f"complete approved grade 7 bounds match: {contract_id}",
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
        if contract_id in GRADE_6_INTEGRATION_IDS | GRADE_7_INTEGRATION_IDS:
            prerequisite_text = " ".join(contract["prerequisites"])
            for module_id in module_ids:
                participant_actions = [
                    action
                    for action in contract["preservedLearningActions"]
                    if action.startswith(f"{module_id} ")
                ]
                _require(
                    len(participant_actions) == 1,
                    "grade 6/7 integration needs exactly one explicit learning action "
                    f"for participant {module_id}: {contract_id}",
                )
                participant_evidence = [
                    evidence
                    for evidence in contract[
                        "preservedProductAndCurriculumEvidence"
                    ]
                    if evidence.startswith(f"{module_id}: ")
                ]
                competency_ids = module_contracts[module_id].get(
                    "competencyIds",
                    [],
                )
                _require(
                    len(participant_evidence) == 1
                    and "Kompetenznachweis" in participant_evidence[0]
                    and "Produktnachweis" in participant_evidence[0]
                    and any(
                        competency_id in participant_evidence[0]
                        for competency_id in competency_ids
                    ),
                    "grade 6/7 integration needs participant-specific competency "
                    f"and product evidence for {module_id}: {contract_id}",
                )
                _require(
                    module_id in prerequisite_text,
                    "grade 6/7 integration prerequisites must name every participant: "
                    f"{contract_id}/{module_id}",
                )
            for path_id in path_ids:
                _require(
                    f"{path_id}: +{savings[path_id]} Minuten"
                    in contract["fallback"],
                    "grade 6/7 integration fallback must name each path consequence: "
                    f"{contract_id}/{path_id}",
                )
                _require(
                    f"{path_id}:" in contract["risk"],
                    "grade 6/7 integration risk must distinguish each path: "
                    f"{contract_id}/{path_id}",
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
    actual_budget_path_overrides_by_variant = {}
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
        actual_budget_path_overrides = {
            module_id: budget_path_id
            for module_id, budget_path_id in selected_budget_path_ids.items()
            if budget_path_id != variant["pathId"]
        }
        registered_budget_path_overrides = (
            ANNUAL_VARIANT_BUDGET_PATH_OVERRIDES.get(variant_id, {})
        )
        _require(
            registered_budget_path_overrides == actual_budget_path_overrides,
            "annual variant path override differs from actual allocation deviations: "
            f"{variant_id}",
        )
        if actual_budget_path_overrides:
            actual_budget_path_overrides_by_variant[variant_id] = (
                actual_budget_path_overrides
            )
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

    if set(GRADE_6_VARIANT_TARGETS) <= set(variants_by_id):
        _require(
            ANNUAL_VARIANT_BUDGET_PATH_OVERRIDES
            == actual_budget_path_overrides_by_variant,
            "annual variant path override registry differs from actual allocation deviations",
        )

    return variants_by_id


def _validate_privacy_disposition(
    review,
    handoff,
    privacy_contracts_by_id,
    privacy_contract_by_module_id,
):
    competency_id = review["competencyId"]
    module_id = review["moduleId"]
    has_contract = module_id in privacy_contract_by_module_id
    cause_class = handoff["causeClass"]

    _require(
        cause_class != "private-local" or has_contract,
        f"private-local time review needs privacy contract: {competency_id}",
    )
    if not has_contract:
        _require(
            "privacyDisposition" not in review,
            f"orphan privacyDisposition: {competency_id}",
        )
        return

    _require(
        "privacyDisposition" in review,
        f"privacyDisposition missing: {competency_id}",
    )
    disposition = review["privacyDisposition"]
    _require(
        isinstance(disposition, dict)
        and set(disposition) == PRIVACY_DISPOSITION_FIELDS,
        f"privacyDisposition fields invalid: {competency_id}",
    )
    contract = privacy_contract_by_module_id[module_id]
    _require(
        disposition["contractId"] == contract["id"]
        and disposition["contractId"] in privacy_contracts_by_id,
        f"privacyDisposition contractId mismatch: {competency_id}",
    )
    basis = disposition["observableBasis"]
    _require(
        isinstance(basis, str) and basis in OBSERVABLE_BASES,
        f"invalid observableBasis: {competency_id}",
    )
    expected_evidence_id = handoff["evidenceContractId"]
    _require(
        disposition["evidenceContractId"] == expected_evidence_id,
        f"privacyDisposition evidenceContractId mismatch: {competency_id}",
    )
    if basis == "nonpersonal-follow-up":
        _require(
            cause_class == "private-local" and expected_evidence_id is not None,
            f"invalid nonpersonal-follow-up observableBasis: {competency_id}",
        )
    elif basis == "nonpersonal-module-detail":
        _require(
            cause_class == "module-detail" and expected_evidence_id is not None,
            f"invalid nonpersonal-module-detail observableBasis: {competency_id}",
        )
    else:
        _require(
            expected_evidence_id is None
            and review["decision"] == "unresolved"
            and review["additionalMinutes"] == 0
            and review["phaseIds"] == []
            and review["pathAvailability"] == []
            and review["integrationContractIds"] == []
            and review["sequenceEvidenceId"] is None,
            f"none privacy basis must remain unresolved and unallocated: {competency_id}",
        )

    contribution = disposition["privateArtifactContribution"]
    _require(
        isinstance(contribution, dict)
        and set(contribution) == PRIVATE_ARTIFACT_CONTRIBUTION_FIELDS,
        f"privateArtifactContribution fields invalid: {competency_id}",
    )
    for field in sorted(PRIVATE_ARTIFACT_CONTRIBUTION_FIELDS):
        _require(
            contribution[field] == "excluded",
            f"{competency_id} private artifact {field} must be excluded",
        )
    _require(
        disposition["privateActivityTimeTreatment"] == "module-budget-only",
        f"privateActivityTimeTreatment must be module-budget-only: {competency_id}",
    )


def validate_time_reviews(
    time_reviews,
    remediation_payload,
    module_contracts,
    integration_contracts,
    annual_variants,
    require_complete=False,
    *,
    privacy_contracts=None,
):
    """Validate time reviews and return them keyed by review id."""
    _require(
        isinstance(require_complete, bool),
        "require_complete must be a boolean",
    )
    _require(
        isinstance(module_contracts, dict),
        "validated module contracts must be keyed by module id",
    )
    _require(
        isinstance(integration_contracts, dict),
        "validated integration contracts must be keyed by contract id",
    )
    _require(
        isinstance(annual_variants, dict),
        "validated annual variants must be keyed by variant id",
    )
    if privacy_contracts is None:
        privacy_contracts = {}
    _require(
        isinstance(privacy_contracts, dict),
        "validated privacy contracts must be keyed by contract id",
    )
    privacy_contract_by_module_id = {
        contract["moduleId"]: contract
        for contract in privacy_contracts.values()
    }
    _require(
        len(privacy_contract_by_module_id) == len(privacy_contracts),
        "validated privacy contracts must use unique module ids",
    )

    handoff_entries = (
        remediation_payload.get("entries")
        if isinstance(remediation_payload, dict)
        else None
    )
    _require(
        isinstance(handoff_entries, list),
        "remediation payload must contain entries",
    )
    handoffs_by_id = {}
    for handoff in handoff_entries:
        _require(
            isinstance(handoff, dict),
            "time handoff must be an object",
        )
        competency_id = handoff.get("competencyId")
        before = handoff.get("before")
        time_impact = handoff.get("timeImpact")
        cause_class = handoff.get("causeClass")
        evidence_contract_id = handoff.get("evidenceContractId")
        _require(
            isinstance(competency_id, str)
            and competency_id.strip()
            and isinstance(before, dict)
            and isinstance(before.get("evidenceModuleId"), str)
            and before["evidenceModuleId"].strip()
            and isinstance(time_impact, dict)
            and time_impact.get("level")
            in {"review-required", "roadmap-dependent"}
            and isinstance(time_impact.get("rationale"), str)
            and time_impact["rationale"].strip(),
            "invalid IUM09 time handoff",
        )
        _require(
            isinstance(cause_class, str) and cause_class.strip(),
            f"time handoff causeClass missing: {competency_id}",
        )
        _require(
            evidence_contract_id is None
            or (
                isinstance(evidence_contract_id, str)
                and evidence_contract_id.strip()
            ),
            f"invalid time handoff evidenceContractId: {competency_id}",
        )
        _require(
            competency_id not in handoffs_by_id,
            "time handoff ids must be unique",
        )
        handoffs_by_id[competency_id] = handoff
    _require(
        len(handoffs_by_id) == len(handoff_entries) == 60,
        "time handoffs must be exactly 60 and unique",
    )
    _require(
        Counter(
            handoff["timeImpact"]["level"]
            for handoff in handoff_entries
        )
        == Counter({"review-required": 56, "roadmap-dependent": 4}),
        "time handoff level counts differ from immutable IUM09 baseline",
    )
    _require(
        {
            competency_id
            for competency_id, handoff in handoffs_by_id.items()
            if handoff["timeImpact"]["level"] == "roadmap-dependent"
        }
        == ROADMAP_DEPENDENT_IDS,
        "roadmap-dependent handoff ids differ from immutable IUM09 baseline",
    )
    _require(
        time_handoff_fingerprint(remediation_payload)
        == BASELINE_TIME_HANDOFF_SHA256,
        "time handoff fingerprint differs from immutable IUM09 baseline",
    )

    _require(isinstance(time_reviews, list), "time reviews must be a list")
    reviews_by_id = {}
    reviewed_competency_ids = set()
    claimed_minutes_by_phase = Counter()
    claimed_minutes_by_budget = Counter()
    for review in time_reviews:
        _require(isinstance(review, dict), "time review must be an object")
        _require(
            frozenset(review)
            in {
                frozenset(TIME_REVIEW_FIELDS),
                frozenset(TIME_REVIEW_FIELDS | {"privacyDisposition"}),
            },
            "time review fields differ from the IUM10 contract",
        )

        competency_id = review["competencyId"]
        _require(
            isinstance(competency_id, str)
            and competency_id in handoffs_by_id,
            f"unknown competency for time review: {competency_id}",
        )
        _require(
            competency_id not in reviewed_competency_ids,
            f"competency needs at most one time review: {competency_id}",
        )
        reviewed_competency_ids.add(competency_id)

        review_id = review["id"]
        _require(
            isinstance(review_id, str)
            and review_id == f"TR-{competency_id}",
            f"invalid time review id: {competency_id}",
        )
        _require(
            review_id not in reviews_by_id,
            "time review ids must be unique",
        )

        handoff = handoffs_by_id[competency_id]
        module_id = review["moduleId"]
        _require(
            module_id == handoff["before"]["evidenceModuleId"]
            and module_id in module_contracts,
            f"time review module differs from IUM09 handoff: {competency_id}",
        )
        _require(
            review["sourceTimeImpactLevel"]
            == handoff["timeImpact"]["level"],
            f"time review source level differs from IUM09 handoff: {competency_id}",
        )
        _require(
            review["decision"]
            in {"absorbed", "integrated", "additional-time", "unresolved"},
            f"invalid time review decision: {competency_id}",
        )
        for field in (
            "rationale",
            "risk",
            "followUp",
        ):
            _require(
                isinstance(review[field], str) and review[field].strip(),
                f"time review {field} must be a nonempty string: {competency_id}",
            )
        _require(
            review["coverageConsequence"] == "semantic-status-unchanged",
            "time review cannot preempt semantic coverage status: "
            f"{competency_id}",
        )
        _require(
            isinstance(review["status"], str)
            and review["status"] in CONTRACT_STATUSES,
            f"invalid time review status: {competency_id}",
        )
        _require(
            _nonnegative_int(review["additionalMinutes"]),
            f"additional minutes must be a non-negative integer: {competency_id}",
        )

        phase_ids = review["phaseIds"]
        _require(
            isinstance(phase_ids, list)
            and all(
                isinstance(phase_id, str) and phase_id.strip()
                for phase_id in phase_ids
            )
            and len(phase_ids) == len(set(phase_ids)),
            f"invalid time review phase ids: {competency_id}",
        )
        module_contract = module_contracts[module_id]
        _require(
            isinstance(module_contract, dict),
            f"invalid validated module contract: {module_id}",
        )
        module_phase_ids = {
            phase_budget.get("phaseId")
            for budget in module_contract.get("pathBudgets", [])
            if isinstance(budget, dict)
            for phase_budget in budget.get("phaseBudgets", [])
            if isinstance(phase_budget, dict)
        }
        _require(
            set(phase_ids) <= module_phase_ids,
            f"time review references unknown module phase: {competency_id}",
        )

        integration_ids = review["integrationContractIds"]
        _require(
            isinstance(integration_ids, list)
            and all(
                isinstance(integration_id, str) and integration_id.strip()
                for integration_id in integration_ids
            )
            and len(integration_ids) == len(set(integration_ids)),
            f"invalid time review integration ids: {competency_id}",
        )
        for integration_id in integration_ids:
            integration_contract = integration_contracts.get(integration_id)
            _require(
                isinstance(integration_contract, dict)
                and module_id
                in integration_contract.get("moduleIds", []),
                f"time review references unknown integration: {competency_id}",
            )
            _require(
                integration_contract.get("status") != "failed",
                f"time review references failed integration: {competency_id}",
            )

        path_availability = review["pathAvailability"]
        _require(
            isinstance(path_availability, list)
            and all(
                isinstance(variant_id, str) and variant_id.strip()
                for variant_id in path_availability
            )
            and len(path_availability) == len(set(path_availability)),
            f"invalid time review path availability: {competency_id}",
        )
        _require(
            set(path_availability) <= set(annual_variants),
            f"time review references unknown annual variant: {competency_id}",
        )
        decision = review["decision"]
        for variant_id in path_availability:
            annual_variant = annual_variants[variant_id]
            allocations = (
                annual_variant.get("allocations")
                if isinstance(annual_variant, dict)
                else None
            )
            _require(
                isinstance(allocations, list),
                f"invalid validated annual variant: {variant_id}",
            )
            module_allocations = [
                allocation
                for allocation in allocations
                if isinstance(allocation, dict)
                and allocation.get("moduleId") == module_id
            ]
            _require(
                len(module_allocations) <= 1,
                "time review path must allocate its module at most once: "
                f"{competency_id}/{variant_id}",
            )
            if module_allocations:
                budget_path_id = module_allocations[0].get("budgetPathId")
                matching_budgets = [
                    budget
                    for budget in module_contract.get("pathBudgets", [])
                    if isinstance(budget, dict)
                    and budget.get("pathId") == budget_path_id
                ]
                _require(
                    len(matching_budgets) == 1,
                    "time review path references an unknown module budget: "
                    f"{competency_id}/{variant_id}",
                )
            else:
                _require(
                    decision == "integrated" and bool(integration_ids),
                    "time review path must allocate its reviewed module unless "
                    "a cross-grade integration carries it: "
                    f"{competency_id}/{variant_id}",
                )

            declared_integration_ids = annual_variant.get(
                "integrationContractIds",
                [],
            )
            _require(
                isinstance(declared_integration_ids, list),
                f"invalid validated annual variant integrations: {variant_id}",
            )
            for integration_id in integration_ids:
                integration = integration_contracts[integration_id]
                _require(
                    integration_id in declared_integration_ids,
                    "time review integration is not used by its annual variant: "
                    f"{competency_id}/{variant_id}/{integration_id}",
                )
                participant_ids = set(integration.get("moduleIds", []))
                participant_allocations = [
                    allocation
                    for allocation in allocations
                    if isinstance(allocation, dict)
                    and allocation.get("moduleId") in participant_ids
                ]
                _require(
                    bool(participant_allocations),
                    "time review integration has no allocated participant: "
                    f"{competency_id}/{variant_id}/{integration_id}",
                )
                for allocation in participant_allocations:
                    participant_id = allocation["moduleId"]
                    participant_contract = module_contracts.get(participant_id)
                    selected_path_id = allocation.get("budgetPathId")
                    _require(
                        isinstance(participant_contract, dict)
                        and selected_path_id in integration.get("pathIds", [])
                        and any(
                            isinstance(budget, dict)
                            and budget.get("pathId") == selected_path_id
                            for budget in participant_contract.get(
                                "pathBudgets",
                                [],
                            )
                        ),
                        "time review integration is not applicable to a selected "
                        "participant budget: "
                        f"{competency_id}/{variant_id}/{integration_id}",
                    )
                counted_module_id = integration.get("countedInModuleId")
                counted_allocations = [
                    allocation
                    for allocation in participant_allocations
                    if allocation.get("moduleId") == counted_module_id
                ]
                _require(
                    len(counted_allocations) == 1,
                    "time review integration counted module is not allocated: "
                    f"{competency_id}/{variant_id}/{integration_id}",
                )
                counted_path_id = counted_allocations[0].get("budgetPathId")
                counted_contract = module_contracts[counted_module_id]
                counted_budgets = [
                    budget
                    for budget in counted_contract.get("pathBudgets", [])
                    if isinstance(budget, dict)
                    and budget.get("pathId") == counted_path_id
                ]
                _require(
                    len(counted_budgets) == 1
                    and any(
                        isinstance(allocation, dict)
                        and allocation.get("integrationContractId")
                        == integration_id
                        for allocation in counted_budgets[0].get(
                            "sharedAllocations",
                            [],
                        )
                    ),
                    "time review integration is declared but not selected in "
                    "the counted module budget: "
                    f"{competency_id}/{variant_id}/{integration_id}",
                )

        is_roadmap_dependent = (
            review["sourceTimeImpactLevel"] == "roadmap-dependent"
        )
        if is_roadmap_dependent:
            _require(
                phase_ids == [],
                "roadmap-dependent review cannot use single-phase evidence: "
                f"{competency_id}",
            )
            _require(
                review["sequenceEvidenceId"] == f"SE-{competency_id}",
                "roadmap-dependent review needs its sequence evidence id: "
                f"{competency_id}",
            )
        else:
            _require(
                review["sequenceEvidenceId"] is None,
                "review-required handoff cannot use sequence evidence: "
                f"{competency_id}",
            )

        additional_minutes = review["additionalMinutes"]
        if decision == "absorbed":
            _require(
                additional_minutes == 0
                and bool(phase_ids)
                and not integration_ids,
                "absorbed review needs an existing positive phase and no "
                f"additional or integration time: {competency_id}",
            )
            _require(
                isinstance(module_contract.get("centralLearningProduct"), str)
                and module_contract["centralLearningProduct"].strip(),
                f"absorbed review needs an existing module product: {competency_id}",
            )
        elif decision == "integrated":
            _require(
                additional_minutes > 0 or bool(integration_ids),
                "integrated review needs positive own or integration time: "
                f"{competency_id}",
            )
            _require(
                additional_minutes == 0 or bool(phase_ids),
                "integrated own time needs a positive phase binding: "
                f"{competency_id}",
            )
        elif decision == "additional-time":
            _require(
                additional_minutes > 0
                and bool(phase_ids)
                and not integration_ids,
                "additional-time review needs positive phase-bound minutes "
                f"without integration time: {competency_id}",
            )
        else:
            _require(
                additional_minutes == 0
                and phase_ids == []
                and not integration_ids
                and path_availability == [],
                "unresolved review cannot claim phases, time, integration, "
                f"or an available path: {competency_id}",
            )

        if decision != "unresolved":
            _require(
                bool(path_availability),
                f"resolved time review needs an available path: {competency_id}",
            )

        _validate_privacy_disposition(
            review,
            handoff,
            privacy_contracts,
            privacy_contract_by_module_id,
        )

        if additional_minutes > 0:
            budgets_by_path_id = {
                budget.get("pathId"): budget
                for budget in module_contract.get("pathBudgets", [])
                if isinstance(budget, dict)
                and isinstance(budget.get("pathId"), str)
            }
            for variant_id in path_availability:
                annual_variant = annual_variants[variant_id]
                allocations = (
                    annual_variant.get("allocations")
                    if isinstance(annual_variant, dict)
                    else None
                )
                _require(
                    isinstance(allocations, list),
                    f"invalid validated annual variant: {variant_id}",
                )
                module_allocations = [
                    allocation
                    for allocation in allocations
                    if isinstance(allocation, dict)
                    and allocation.get("moduleId") == module_id
                ]
                _require(
                    len(module_allocations) == 1,
                    "time review path must allocate its module exactly once: "
                    f"{competency_id}/{variant_id}",
                )
                budget_path_id = module_allocations[0].get("budgetPathId")
                _require(
                    budget_path_id in budgets_by_path_id,
                    "time review path references an unknown module budget: "
                    f"{competency_id}/{variant_id}",
                )
                budget = budgets_by_path_id[budget_path_id]
                included_phase_minutes = sum(
                    phase_budget.get("minutes", 0)
                    for phase_budget in budget.get("phaseBudgets", [])
                    if isinstance(phase_budget, dict)
                    and phase_budget.get("phaseId") in phase_ids
                    and _nonnegative_int(phase_budget.get("minutes"))
                )
                _require(
                    included_phase_minutes >= additional_minutes,
                    "additional minutes must already be included in the selected "
                    f"module budget: {competency_id}/{variant_id}",
                )
                phase_minutes_by_id = {
                    phase_budget.get("phaseId"): phase_budget.get("minutes")
                    for phase_budget in budget.get("phaseBudgets", [])
                    if isinstance(phase_budget, dict)
                    and isinstance(phase_budget.get("phaseId"), str)
                    and _nonnegative_int(phase_budget.get("minutes"))
                }
                budget_key = (module_id, variant_id, budget_path_id)
                claimed_minutes_by_budget[budget_key] += additional_minutes
                budget_minutes = budget.get("minutes")
                if not _nonnegative_int(budget_minutes):
                    budget_minutes = sum(phase_minutes_by_id.values())
                _require(
                    claimed_minutes_by_budget[budget_key] <= budget_minutes,
                    "cumulative additional minutes exceed the selected module "
                    f"budget: {competency_id}/{variant_id}",
                )
                for phase_id in phase_ids:
                    phase_key = (
                        module_id,
                        variant_id,
                        budget_path_id,
                        phase_id,
                    )
                    claimed_minutes_by_phase[phase_key] += additional_minutes
                    _require(
                        claimed_minutes_by_phase[phase_key]
                        <= phase_minutes_by_id[phase_id],
                        "cumulative additional minutes exceed the selected "
                        "phase budget: "
                        f"{competency_id}/{variant_id}/{phase_id}",
                    )

        reviews_by_id[review_id] = review

    if require_complete:
        _require(
            reviewed_competency_ids == set(handoffs_by_id),
            "complete time reviews must match all 60 baseline handoff ids",
        )
    else:
        _require(
            reviewed_competency_ids <= set(handoffs_by_id),
            "partial time reviews must be a subset of baseline handoff ids",
        )
    return reviews_by_id


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


def _load_repository_json(root, relative_path):
    with (root / relative_path).open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_ium10_repository(root):
    """Load and validate the composed IUM10 repository contract."""
    root = Path(root)
    module_payload = _load_repository_json(
        root,
        "roadmap/module-candidates.json",
    )
    coverage_payload = _load_repository_json(
        root,
        "roadmap/coverage-plan.json",
    )
    remediation_payload = _load_repository_json(
        root,
        "roadmap/coverage-remediation.json",
    )
    time_model = _load_repository_json(root, "roadmap/time-model.json")

    baseline = validate_ium10_baseline(
        module_payload,
        coverage_payload,
        remediation_payload,
    )
    validate_time_model_draft(time_model, module_payload)
    capacity_paths = validate_capacity_model(
        time_model["capacityModel"],
        time_model["unit"],
    )
    module_contracts = validate_module_contracts(
        time_model["moduleContracts"],
        module_payload,
    )
    integration_contracts = validate_integration_contracts(
        time_model["integrationContracts"],
        module_contracts,
    )
    annual_variants = validate_annual_variants(
        time_model["annualVariants"],
        module_contracts,
        integration_contracts,
    )
    privacy_contracts = validate_privacy_contracts(
        time_model["privacyContracts"],
        module_contracts,
    )
    time_reviews = validate_time_reviews(
        time_model["timeReviews"],
        remediation_payload,
        module_contracts,
        integration_contracts,
        annual_variants,
        require_complete=False,
        privacy_contracts=privacy_contracts,
    )
    return {
        "baseline": baseline,
        "capacityPaths": capacity_paths,
        "moduleContracts": module_contracts,
        "integrationContracts": integration_contracts,
        "annualVariants": annual_variants,
        "privacyContracts": privacy_contracts,
        "timeReviews": time_reviews,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate the composed IUM10 repository contract.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root containing roadmap JSON inputs.",
    )
    arguments = parser.parse_args(argv)
    try:
        result = validate_ium10_repository(arguments.root)
    except (IUM10ValidationError, OSError, json.JSONDecodeError) as error:
        print(f"IUM10 repository validation failed: {error}", file=sys.stderr)
        return 1
    print(
        "IUM10 repository validation passed: "
        f"{len(result['timeReviews'])} registered time reviews "
        "(partial baseline)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
