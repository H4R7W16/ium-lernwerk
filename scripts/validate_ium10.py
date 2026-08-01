import argparse
import copy
import hashlib
import json
import sys
from collections import Counter
from functools import wraps
from pathlib import Path

if __package__:
    from .validate_ium09 import (
        BASELINE_PARTIAL_IDS,
        module_structure_fingerprint,
    )
else:
    from validate_ium09 import (
        BASELINE_PARTIAL_IDS,
        module_structure_fingerprint,
    )


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
CURRENT_COVERAGE_SHA256 = (
    "f39df261d7fab3733deafe9c1f4da4d15ca2778440d6d38828a088614e835776"
)
TIME_MODEL_BASELINE_FIELDS = {
    "commit",
    "moduleStructureSha256",
    "coverageProjectionSha256",
    "timeHandoffSha256",
}
ROADMAP_DEPENDENT_IDS = frozenset(
    {
        "LH26-E-PROG-001",
        "LH26-E-PROG-002",
        "LH26-E-PROG-003",
        "LH26-E-PROG-004",
    }
)
COVERED_SEQUENCE_IDS = frozenset(
    {"LH26-E-PROG-001", "LH26-E-PROG-002"}
)
GRADE_7_BALANCE_SEQUENCE_IDS = frozenset(
    {"LH26-E-PROG-003", "LH26-E-PROG-004"}
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
AVAILABILITY_STATUSES = {"conditional", "available", "unavailable"}
AVAILABILITY_CONTRACT_FIELDS = {
    "id",
    "variantId",
    "requiredCapacityUnits",
    "comparisonBoundaryUnits",
    "gates",
    "fallbackDeltaUnitsByIntegrationContractId",
    "maximumFallbackUnits",
    "forbiddenCompensations",
    "failureMode",
    "status",
    "risk",
}
AVAILABILITY_GATE_FIELDS = {"status", "requirement"}
AVAILABILITY_GATE_STATUSES = {"not-started", "passed", "failed"}
GRADE_7_AVAILABILITY_CONTRACT_ID = "AVAIL-GRADE-7-WORKING-40"
GRADE_7_AVAILABILITY_GATE_IDS = {
    "capacity",
    "integration",
    "technical",
    "privacy",
    "pilot",
}
GRADE_7_FALLBACK_DELTAS = {
    "INT-7-DATA-CODING": 3,
    "INT-7-PROGRAMMING": 2,
    "INT-7-NET-SECURITY": 3,
    "INT-7-DATA-MEDIA-SOCIETY": 6,
}
GRADE_7_FORBIDDEN_COMPENSATIONS = [
    "core-module-removal",
    "required-learning-action-removal",
    "operator-mention-only",
    "demonstration-instead-of-independent-application",
    "homework-shift",
    "unsupervised-self-study-as-guaranteed-time",
    "private-reflection-as-evidence",
    "flexible-module-substitution",
    "comparison-boundary-as-grade-7-path",
]
GRADE_7_AVAILABILITY_CONTRACT_RISK = (
    "Fehlende, widersprüchliche oder gescheiterte Evidenz darf keinen positiven "
    "Verfügbarkeits- oder Zeitstatus erzeugen."
)
TIME_MODEL_FIELDS = {
    "schemaVersion",
    "status",
    "baseline",
    "unit",
    "capacityModel",
    "moduleContracts",
    "integrationContracts",
    "annualVariants",
    "availabilityContracts",
    "privacyContracts",
    "timeReviews",
    "sequenceEvidence",
    "gradeJudgements",
    "risks",
    "pilotAssignments",
}
RISK_FIELDS = {"id", "scope", "risk", "impact", "mitigation", "status"}
RISK_SCOPES = {
    "RISK-IUM10-UNPILOTED-TIME": "all-module-contracts",
    "RISK-IUM10-TECHNICAL-STARTUP": "school-dependent-steps",
    "RISK-IUM10-INTEGRATION-FALLBACK": "integration-contracts",
    "RISK-IUM10-GRADE7-CAPACITY": "grade-7",
    "RISK-IUM10-PRIVATE-LEARNING-ACTIONS": "private-local-reflection",
}
APPROVED_RISK_REGISTER_SHA256 = (
    "8da9e7b197a8dc4a7dcbecb277b07a3e121681cb27f91e26b75fcbc9a0e3a894"
)
PILOT_ASSIGNMENT_FIELDS = {
    "id",
    "scopeType",
    "scopeIds",
    "contractIds",
    "aggregationLevel",
    "measures",
    "personalData",
    "personalTelemetry",
    "privateReflectionEvidence",
    "excludedUses",
    "status",
    "fallback",
}
PILOT_SCOPE_TYPES = {"module", "integration", "annual-variant"}
PILOT_STATUSES = {"not-started", "in-progress", "completed"}
PILOT_MEASURES = [
    "plannedTeachingUnits",
    "actualTeachingUnits",
    "handoffProductPresent",
    "fallbackActivated",
    "aggregatedTechnicalStartupMinutes",
    "aggregatedSupportDemand",
    "requiredLearningPhasesCompleted",
    "gateOutcome",
]
PILOT_EXCLUDED_USES = [
    "grades",
    "competence-profiles",
    "individual-diagnostics",
    "learner-identifiers",
    "personal-learning-paths",
    "private-reflection-content",
    "student-products-as-time-evidence",
    "automated-personal-assessment",
]
GRADE_7_REQUIRED_PILOT_IDS = frozenset(
    {
        "PILOT-INT-7-DATA-CODING",
        "PILOT-INT-7-PROGRAMMING",
        "PILOT-INT-7-NET-SECURITY",
        "PILOT-INT-7-DATA-MEDIA-SOCIETY",
        "PILOT-GRADE-7-WORKING-40",
    }
)
GRADE_7_WORKING_40_REVIEW_IDS = frozenset(
    {
        "TR-INF7-16-GYM-IK-DC-001",
        "TR-INF7-16-GYM-IK-DC-004",
        "TR-INF7-16-GYM-IK-DC-005",
        "TR-INF7-16-GYM-IK-ALG-003",
        "TR-INF7-16-GYM-IK-IGD-004",
        "TR-INF7-16-GYM-IK-IGD-006",
        "TR-INF7-16-GYM-PK-AB-002",
        "TR-INF7-16-GYM-PK-AB-005",
        "TR-INF7-16-GYM-PK-AB-006",
        "TR-INF7-16-GYM-PK-KK-002",
        "TR-INF7-16-GYM-PK-KK-006",
        "TR-INF7-16-GYM-PK-MI-003",
        "TR-INF7-16-GYM-PK-MI-005",
        "TR-INF7-16-GYM-PK-SV-001",
        "TR-INF7-16-GYM-PK-SV-002",
        "TR-INF7-16-GYM-PK-SV-003",
        "TR-LH26-E-ALG-007",
        "TR-LH26-E-ALG-008",
        "TR-LH26-E-ALG-009",
        "TR-LH26-E-DP-013",
        "TR-LH26-E-DP-014",
        "TR-LH26-E-ID-020",
        "TR-LH26-E-ID-021",
    }
)
AUTHORITATIVE_TIME_BOUNDARY = (
    "lessonRange ist die historische, eigenständige Kandidatenschätzung. "
    "roadmap/time-model.json ist für Jahreszuweisung, Pfadstatus und "
    "Zeitfreigabe autoritativ."
)


def derive_grade_7_operational_state(availability_contract, pilot_assignments):
    _require(
        isinstance(availability_contract, dict)
        and isinstance(availability_contract.get("gates"), dict)
        and set(availability_contract["gates"]) == GRADE_7_AVAILABILITY_GATE_IDS,
        "grade 7 operational state requires the five availability gates",
    )
    _require(
        isinstance(pilot_assignments, dict)
        and GRADE_7_REQUIRED_PILOT_IDS <= set(pilot_assignments),
        "grade 7 operational state requires all five required pilots",
    )
    _require(
        all(
            isinstance(gate, dict)
            and gate.get("status") in AVAILABILITY_GATE_STATUSES
            for gate in availability_contract["gates"].values()
        ),
        "grade 7 operational state has invalid gate statuses",
    )
    required_pilots = {
        pilot_id: pilot_assignments[pilot_id]
        for pilot_id in GRADE_7_REQUIRED_PILOT_IDS
    }
    _require(
        all(
            isinstance(pilot, dict)
            and pilot.get("id") == pilot_id
            and pilot.get("status") in PILOT_STATUSES
            for pilot_id, pilot in required_pilots.items()
        ),
        "grade 7 operational state has invalid required pilots",
    )
    gate_statuses = {
        gate["status"] for gate in availability_contract["gates"].values()
    }
    pilot_statuses = {pilot["status"] for pilot in required_pilots.values()}
    if pilot_statuses == {"not-started"}:
        pilot_status = "not-started"
    elif pilot_statuses == {"completed"}:
        pilot_status = "completed"
    else:
        pilot_status = "in-progress"

    if "failed" in gate_statuses:
        availability_status, time_status = "unavailable", "red"
    elif gate_statuses == {"passed"} and pilot_status == "completed":
        availability_status, time_status = "available", "green"
    else:
        availability_status, time_status = "conditional", "amber"

    return {
        "availabilityStatus": availability_status,
        "timeFeasibilityStatus": time_status,
        "pilotStatus": pilot_status,
    }
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
    7: {"working-40", "robust", "historical-minimum"},
}
CORE_PATH_ORDER = {
    5: ("baseline", "regular", "extended"),
    6: ("baseline", "regular", "targeted-extension"),
    7: ("working-40", "robust", "historical-minimum"),
}
ANNUAL_PATH_IDS_BY_KIND = {
    "planning-path": {"baseline", "regular", "extended"},
    "working-target": {"working-40"},
    "demand-scenario": {"robust", "historical-minimum"},
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
GRADE_5_CORE_MODULE_IDS = frozenset(
    f"IUM-5-CORE-{number:02d}" for number in range(1, 8)
)
SEQUENCE_EVIDENCE_FIELDS = {
    "id",
    "competencyId",
    "timeReviewId",
    "moduleIds",
    "grades",
    "progression",
    "operatorProductDepth",
    "perspectiveWeighting",
    "timeEvidence",
    "remainingBoundary",
    "fachAuditStatus",
    "coverageDecision",
    "coverageConsequence",
    "evidenceBoundary",
    "status",
}
SEQUENCE_PROGRESSION_FIELDS = {"grade", "moduleIds", "learningDepth"}
SEQUENCE_DEPTH_FIELDS = {"grade", "operatorDepth", "productDepth"}
SEQUENCE_PERSPECTIVE_FIELDS = {"perspective", "moduleIds", "rationale"}
SEQUENCE_TIME_EVIDENCE_FIELDS = {
    "variantId",
    "availabilityStatus",
    "targetUnits",
    "scopeModuleIds",
    "scopeUnits",
    "weightGroups",
    "rationale",
}
SEQUENCE_WEIGHT_GROUP_FIELDS = {"id", "moduleIds", "units"}
SEQUENCE_COVERAGE_CONSEQUENCE_FIELDS = {
    "coverageStatus",
    "semanticAudit",
    "rationale",
}
SEQUENCE_EVIDENCE_BOUNDARY_FIELDS = {
    "privateEvidence",
    "singleModuleProxy",
    "automatedPersonalAssessment",
    "rationale",
}
SEQUENCE_SCOPES = {
    "LH26-E-PROG-001": {
        "grades": [5, 6],
        "moduleIds": sorted(GRADE_5_CORE_MODULE_IDS)
        + sorted(GRADE_6_CORE_MODULE_IDS),
        "variantModuleIds": {
            "GRADE-5-BASELINE": sorted(GRADE_5_CORE_MODULE_IDS),
            "GRADE-6-BASELINE": sorted(GRADE_6_CORE_MODULE_IDS),
        },
        "coverageDecision": "covered",
    },
    "LH26-E-PROG-002": {
        "grades": [5, 6, 7],
        "moduleIds": [
            "IUM-5-CORE-05",
            "IUM-6-CORE-04",
            "IUM-7-CORE-03",
            "IUM-7-CORE-04",
        ],
        "variantModuleIds": {
            "GRADE-5-BASELINE": ["IUM-5-CORE-05"],
            "GRADE-6-BASELINE": ["IUM-6-CORE-04"],
            "GRADE-7-WORKING-40": [
                "IUM-7-CORE-03",
                "IUM-7-CORE-04",
            ],
        },
        "coverageDecision": "covered",
    },
    "LH26-E-PROG-003": {
        "grades": [7],
        "moduleIds": sorted(GRADE_7_CORE_MODULE_IDS),
        "variantModuleIds": {
            variant_id: sorted(GRADE_7_CORE_MODULE_IDS)
            for variant_id in (
                "GRADE-7-WORKING-40",
                "GRADE-7-ROBUST-DEMAND",
                "GRADE-7-HISTORICAL-MINIMUM",
            )
        },
        "coverageDecision": "remain-partial",
    },
    "LH26-E-PROG-004": {
        "grades": [7],
        "moduleIds": sorted(GRADE_7_CORE_MODULE_IDS),
        "variantModuleIds": {
            variant_id: sorted(GRADE_7_CORE_MODULE_IDS)
            for variant_id in (
                "GRADE-7-WORKING-40",
                "GRADE-7-ROBUST-DEMAND",
                "GRADE-7-HISTORICAL-MINIMUM",
            )
        },
        "coverageDecision": "remain-partial",
    },
}
SEQUENCE_GRADE_7_WEIGHT_GROUPS = {
    "core-01-07": [f"IUM-7-CORE-{number:02d}" for number in range(1, 8)],
    "core-08-10": [f"IUM-7-CORE-{number:02d}" for number in range(8, 11)],
}
SEQUENCE_COVERAGE_ANCHORS = {
    "LH26-E-PROG-001": (
        "In den Klassen 5 und 6 knüpft die Lesehilfe im Wesentlichen an die "
        "Themen und Zielsetzungen des „Basiskurs Medienbildung“ an. Im Mittelpunkt "
        "stehen der sichere, verantwortungsvolle und reflektierte Umgang mit "
        "digitalen Medien, Informationen, Daten, Kommunikationsangeboten und "
        "digitalen Arbeitsmitteln.",
        "Gerätekomponenten, Betriebssystem, Verzeichnisse, Speicherorte und "
        "Zugangsschutz in einem realen Arbeitsauftrag nutzen, erklären und gegen "
        "Störfälle prüfen.",
        "Kommentierte System- und Arbeitswegkarte mit eigener Verzeichnisstruktur, "
        "Schutzentscheidungen und Wiederanlauf-Checkliste.",
    ),
    "LH26-E-PROG-002": (
        "Ergänzend wird mit dem Bereich „Erste Schritte mit Algorithmen“ bereits "
        "ein grundlegendes Element der Informatik aufgenommen. Die Schülerinnen "
        "und Schüler begegnen dabei ersten algorithmischen Denk- und Vorgehensweisen "
        "in einer altersangemessenen und niederschwelligen Form. Die Behandlung ist "
        "bewusst grundlegend angelegt und erreicht noch nicht die fachliche Tiefe "
        "des bisherigen Aufbaukurses Informatik in Klasse 7.",
        "Alltagshandlungen präzisieren, grafische Algorithmen ausführen, "
        "Abweichungen erklären und eine konstante Wiederholung als Grundbaustein "
        "modellieren.",
        "Ausführbarer grafischer Algorithmus mit Vorhersage, Laufprotokoll, "
        "reparierter Fassung und begründeter Schleifenentscheidung.",
    ),
}
GRADE_7_FLEX_RANGES = {
    "IUM-7-EXT-01": {"min": 3, "recommended": 4, "max": 5},
    "IUM-7-TRANSFER-01": {"min": 3, "recommended": 4, "max": 5},
    "IUM-7-PROJECT-01": {"min": 8, "recommended": 10, "max": 12},
}
GRADE_7_CORE_UNITS = {
    "IUM-7-CORE-01": {"working-40": 5, "robust": 5, "historical-minimum": 6},
    "IUM-7-CORE-02": {"working-40": 3, "robust": 4, "historical-minimum": 5},
    "IUM-7-CORE-03": {"working-40": 5, "robust": 5, "historical-minimum": 6},
    "IUM-7-CORE-04": {"working-40": 6, "robust": 6, "historical-minimum": 7},
    "IUM-7-CORE-05": {"working-40": 4, "robust": 4, "historical-minimum": 5},
    "IUM-7-CORE-06": {"working-40": 3, "robust": 3, "historical-minimum": 4},
    "IUM-7-CORE-07": {"working-40": 4, "robust": 4, "historical-minimum": 5},
    "IUM-7-CORE-08": {"working-40": 4, "robust": 6, "historical-minimum": 6},
    "IUM-7-CORE-09": {"working-40": 2, "robust": 3, "historical-minimum": 4},
    "IUM-7-CORE-10": {"working-40": 4, "robust": 6, "historical-minimum": 6},
}
GRADE_7_INTEGRATION_BOUNDS = {
    "INT-7-DATA-CODING": {
        "moduleIds": ["IUM-7-CORE-01", "IUM-7-CORE-02"],
        "pathIds": ["working-40", "robust"],
        "countedInModuleId": "IUM-7-CORE-02",
        "sharedMinutes": 90,
        "savingsMinutesByPath": {"working-40": 135, "robust": 90},
    },
    "INT-7-PROGRAMMING": {
        "moduleIds": ["IUM-7-CORE-03", "IUM-7-CORE-04"],
        "pathIds": ["working-40", "robust"],
        "countedInModuleId": "IUM-7-CORE-04",
        "sharedMinutes": 90,
        "savingsMinutesByPath": {"working-40": 90, "robust": 90},
    },
    "INT-7-NET-SECURITY": {
        "moduleIds": [
            "IUM-7-CORE-05",
            "IUM-7-CORE-06",
            "IUM-7-CORE-07",
        ],
        "pathIds": ["working-40", "robust"],
        "countedInModuleId": "IUM-7-CORE-07",
        "sharedMinutes": 135,
        "savingsMinutesByPath": {"working-40": 135, "robust": 135},
    },
    "INT-7-DATA-MEDIA-SOCIETY": {
        "moduleIds": [
            "IUM-7-CORE-08",
            "IUM-7-CORE-09",
            "IUM-7-CORE-10",
        ],
        "pathIds": ["working-40", "robust"],
        "countedInModuleId": "IUM-7-CORE-10",
        "sharedMinutes": 45,
        "savingsMinutesByPath": {"working-40": 270, "robust": 45},
    },
}
GRADE_7_VARIANT_TARGETS = {
    "GRADE-7-WORKING-40": ("working-40", 40),
    "GRADE-7-ROBUST-DEMAND": ("robust", 46),
    "GRADE-7-HISTORICAL-MINIMUM": ("historical-minimum", 54),
}
GRADE_7_VARIANT_INTEGRATIONS = {
    "GRADE-7-WORKING-40": GRADE_7_INTEGRATION_IDS,
    "GRADE-7-ROBUST-DEMAND": GRADE_7_INTEGRATION_IDS,
    "GRADE-7-HISTORICAL-MINIMUM": frozenset(),
}
GRADE_7_DECISION_OPTIONS = [
    "pilot-grade-7-clusters",
    "pilot-grade-7-end-to-end",
    "fall-back-on-failed-required-gate",
]
GRADE_7_UNIMPLEMENTED_OPTIONS_RATIONALE = (
    "Das vollständige 40-UE-Arbeitsziel der Klasse 7 bleibt bis zur "
    "Pilotierung conditional und amber. Die 46- und 54-UE-Referenzrechnungen "
    "bleiben unavailable; der Sequenznachweis ist covered, die semantische "
    "Coverage partial und der Pilotstatus not-started."
)
GRADE_7_INITIAL_RISK = (
    "Ohne neues Auftraggebergate dürfen weder Kernmodule entfernt noch flexible "
    "Module als Ersatz verwendet werden. Die drei Pilot- und Rückfalloptionen "
    "bleiben bis zu ihren eigenen Gates offen."
)
GRADE_5_JUDGEMENT_RATIONALE = (
    "Die verfügbaren Kernvarianten sind rechnerisch mit 30, 34 und 38 "
    "Unterrichtseinheiten zeitlich grün. Die drei verbleibenden semantischen "
    "Lücken der Klasse 5 bleiben davon getrennt partial; die beiden "
    "Sequenznachweise PROG-001/002 sind covered."
)
GRADE_6_JUDGEMENT_RATIONALE = (
    "Die verfügbaren vollständigen Kernpfade ergeben exakt 30 und 34 "
    "Unterrichtseinheiten; alle drei Erweiterungsvarianten ergeben exakt 38 "
    "Unterrichtseinheiten und alle drei Integrationsverträge sind working. "
    "Semantische Coverage und Sequenznachweise sind covered; Zeitmachbarkeit "
    "und Pilotstatus bleiben davon getrennt green beziehungsweise not-started."
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

# Recordgenaue, in Tasks 9-23 fachlich auditierte Registrierung. Sie ist
# absichtlich unabhängig von den JSON-Daten, damit ein formal plausibler
# Tausch von Entscheidung oder Minuten nicht unbemerkt bleibt.
APPROVED_TIME_AUDIT = {
    "BMB16-GYM-IK-GM-001": ("IUM-5-CORE-01", "review-required", "additional-time", 15),
    "BMB16-GYM-IK-GM-002": ("IUM-5-CORE-01", "review-required", "additional-time", 15),
    "BMB16-GYM-IK-GM-003": ("IUM-5-CORE-01", "review-required", "additional-time", 20),
    "BMB16-GYM-PK-SK-003": ("IUM-5-CORE-01", "review-required", "absorbed", 0),
    "LH26-E-DA-004": ("IUM-5-CORE-01", "review-required", "additional-time", 15),
    "LH26-E-DP-001": ("IUM-5-CORE-01", "review-required", "additional-time", 15),
    "LH26-E-ID-009": ("IUM-5-CORE-02", "review-required", "absorbed", 0),
    "BMB16-GYM-IK-KK-002": ("IUM-5-CORE-03", "review-required", "additional-time", 15),
    "BMB16-GYM-IK-KK-003": ("IUM-5-CORE-03", "review-required", "absorbed", 0),
    "BMB16-GYM-PK-HK-003": ("IUM-5-CORE-03", "review-required", "absorbed", 0),
    "BMB16-GYM-PK-RK-004": ("IUM-5-CORE-03", "review-required", "additional-time", 15),
    "LH26-E-KS-001": ("IUM-5-CORE-03", "review-required", "additional-time", 20),
    "LH26-E-KS-002": ("IUM-5-CORE-03", "review-required", "additional-time", 20),
    "LH26-E-ALG-001": ("IUM-5-CORE-05", "review-required", "absorbed", 0),
    "LH26-E-PROG-001": ("IUM-5-CORE-01", "roadmap-dependent", "unresolved", 0),
    "LH26-E-PROG-002": ("IUM-5-CORE-05", "roadmap-dependent", "unresolved", 0),
    "BMB16-GYM-IK-PP-002": ("IUM-5-CORE-06", "review-required", "integrated", 15),
    "LH26-E-DA-005": ("IUM-5-CORE-06", "review-required", "additional-time", 15),
    "LH26-E-DA-006": ("IUM-5-CORE-06", "review-required", "additional-time", 25),
    "LH26-E-DA-008": ("IUM-5-CORE-06", "review-required", "additional-time", 20),
    "BMB16-GYM-IK-MG-001": ("IUM-5-CORE-07", "review-required", "additional-time", 15),
    "BMB16-GYM-IK-MG-002": ("IUM-5-CORE-07", "review-required", "additional-time", 20),
    "BMB16-GYM-IK-MG-003": ("IUM-5-CORE-07", "review-required", "absorbed", 0),
    "BMB16-GYM-PK-RK-001": ("IUM-5-CORE-07", "review-required", "additional-time", 15),
    "BMB16-GYM-PK-RK-002": ("IUM-5-CORE-07", "review-required", "additional-time", 15),
    "BMB16-GYM-PK-RK-003": ("IUM-5-CORE-07", "review-required", "unresolved", 0),
    "LH26-E-DP-003": ("IUM-5-CORE-07", "review-required", "unresolved", 0),
    "LH26-E-DP-004": ("IUM-6-CORE-02", "review-required", "integrated", 20),
    "LH26-E-DP-006": ("IUM-6-CORE-02", "review-required", "integrated", 25),
    "LH26-E-KS-014": ("IUM-6-CORE-06", "review-required", "additional-time", 25),
    "LH26-E-KS-015": ("IUM-6-CORE-06", "review-required", "additional-time", 20),
    "LH26-E-DA-009": ("IUM-6-CORE-07", "review-required", "additional-time", 30),
    "LH26-E-DA-010": ("IUM-6-CORE-07", "review-required", "additional-time", 20),
    "LH26-E-DA-012": ("IUM-6-CORE-07", "review-required", "absorbed", 0),
    "LH26-E-DA-015": ("IUM-6-CORE-07", "review-required", "additional-time", 20),
    "INF7-16-GYM-IK-DC-001": ("IUM-7-CORE-01", "review-required", "additional-time", 15),
    "INF7-16-GYM-IK-DC-004": ("IUM-7-CORE-01", "review-required", "additional-time", 15),
    "INF7-16-GYM-IK-DC-005": ("IUM-7-CORE-01", "review-required", "integrated", 30),
    "LH26-E-ID-020": ("IUM-7-CORE-01", "review-required", "absorbed", 0),
    "LH26-E-ID-021": ("IUM-7-CORE-01", "review-required", "additional-time", 15),
    "INF7-16-GYM-IK-ALG-003": ("IUM-7-CORE-03", "review-required", "integrated", 20),
    "INF7-16-GYM-PK-MI-005": ("IUM-7-CORE-03", "review-required", "additional-time", 20),
    "INF7-16-GYM-PK-SV-003": ("IUM-7-CORE-03", "review-required", "additional-time", 20),
    "LH26-E-ALG-007": ("IUM-7-CORE-03", "review-required", "integrated", 25),
    "LH26-E-ALG-008": ("IUM-7-CORE-03", "review-required", "additional-time", 15),
    "LH26-E-ALG-009": ("IUM-7-CORE-03", "review-required", "additional-time", 15),
    "INF7-16-GYM-PK-KK-002": ("IUM-7-CORE-04", "review-required", "additional-time", 25),
    "INF7-16-GYM-PK-MI-003": ("IUM-7-CORE-04", "review-required", "additional-time", 25),
    "INF7-16-GYM-PK-SV-002": ("IUM-7-CORE-04", "review-required", "additional-time", 20),
    "INF7-16-GYM-IK-IGD-004": ("IUM-7-CORE-05", "review-required", "integrated", 30),
    "INF7-16-GYM-PK-AB-002": ("IUM-7-CORE-05", "review-required", "additional-time", 30),
    "INF7-16-GYM-PK-SV-001": ("IUM-7-CORE-05", "review-required", "additional-time", 30),
    "INF7-16-GYM-IK-IGD-006": ("IUM-7-CORE-08", "review-required", "additional-time", 20),
    "INF7-16-GYM-PK-AB-005": ("IUM-7-CORE-08", "review-required", "integrated", 25),
    "INF7-16-GYM-PK-AB-006": ("IUM-7-CORE-08", "review-required", "additional-time", 20),
    "INF7-16-GYM-PK-KK-006": ("IUM-7-CORE-08", "review-required", "integrated", 25),
    "LH26-E-DP-013": ("IUM-7-CORE-08", "review-required", "additional-time", 15),
    "LH26-E-PROG-003": ("IUM-7-CORE-08", "roadmap-dependent", "unresolved", 0),
    "LH26-E-PROG-004": ("IUM-7-CORE-08", "roadmap-dependent", "unresolved", 0),
    "LH26-E-DP-014": ("IUM-7-CORE-10", "review-required", "additional-time", 20),
}


class IUM10ValidationError(ValueError):
    pass


def _require(condition, message):
    if not condition:
        raise IUM10ValidationError(message)


def _validation_boundary(label):
    """Convert malformed public JSON-like inputs into the domain error."""
    def decorate(function):
        @wraps(function)
        def guarded(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except IUM10ValidationError:
                raise
            except (AttributeError, IndexError, KeyError, TypeError, ValueError) as error:
                raise IUM10ValidationError(
                    f"{label} has an invalid structure: {error}"
                ) from None

        return guarded

    return decorate


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


def _current_coverage_fingerprint(coverage_payload):
    """Fingerprint the complete IUM10 source before making a deep projection."""
    _require(
        isinstance(coverage_payload, dict),
        "coverage payload must be an object",
    )
    entries = coverage_payload.get("entries")
    _require(
        isinstance(entries, list) and len(entries) == 171,
        "coverage payload must contain exactly 171 records",
    )
    canonical_entries = []
    coverage_ids = set()
    for entry in entries:
        _require(
            isinstance(entry, dict),
            "coverage record must be an object",
        )
        competency_id = entry.get("competencyId")
        _require(
            isinstance(competency_id, str)
            and competency_id.strip()
            and competency_id not in coverage_ids,
            f"duplicate or invalid coverage id: {competency_id}",
        )
        coverage_ids.add(competency_id)
        canonical_entries.append(entry)
    _require(
        len(coverage_ids) == len(canonical_entries) == 171,
        "current coverage fingerprint must contain exactly 171 records",
    )
    canonical_scope = {
        field: value
        for field, value in coverage_payload.items()
        if field != "entries"
    }
    canonical_scope["entries"] = sorted(
        canonical_entries,
        key=lambda entry: entry["competencyId"],
    )
    return _canonical_sha256(canonical_scope)


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
        "availabilityStatus",
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
        if variant.get("availabilityStatus") != "available":
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
    availability_contracts,
):
    grade_judgements = time_model.get("gradeJudgements")
    _require(
        isinstance(module_contracts, dict)
        and isinstance(integration_contracts, dict)
        and isinstance(annual_variants, dict)
        and isinstance(availability_contracts, dict)
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
        "availabilityStatus",
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
        judgement["grade"] == 7,
        "grade 7 judgement must have grade 7",
    )
    _require(
        judgement["semanticCoverageStatus"] == "partial",
        "grade 7 semantic coverage status must remain partial",
    )
    _require(
        judgement["sequenceEvidenceStatus"] == "covered",
        "grade 7 sequence evidence status must remain covered",
    )
    _require(
        isinstance(judgement["availabilityStatus"], str)
        and isinstance(judgement["timeFeasibilityStatus"], str)
        and isinstance(judgement["pilotStatus"], str),
        "grade 7 operational status fields are invalid",
    )
    _require(
        judgement["annualVariantIds"] == list(GRADE_7_VARIANT_TARGETS),
        "grade 7 judgement must reference the exact demand scenarios",
    )
    _require(
        judgement["decisionOptions"] == GRADE_7_DECISION_OPTIONS,
        "grade 7 judgement must retain exactly three approved decision options",
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
    _require(
        judgement["risk"] == GRADE_7_INITIAL_RISK,
        "grade 7 judgement must use the canonical initial risk",
    )
    _require(
        set(availability_contracts) == {GRADE_7_AVAILABILITY_CONTRACT_ID}
        and availability_contracts[GRADE_7_AVAILABILITY_CONTRACT_ID]["variantId"]
        == "GRADE-7-WORKING-40",
        "grade 7 needs exactly the working-40 availability contract",
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
            and variant.get("kind")
            == ("working-target" if variant_id == "GRADE-7-WORKING-40" else "demand-scenario")
            and variant.get("pathId") == path_id
            and variant.get("targetUnits") == target_units
            and actual_allocations == expected_allocations
            and set(variant.get("integrationContractIds", []))
            == set(GRADE_7_VARIANT_INTEGRATIONS[variant_id])
            and variant.get("availabilityStatus")
            == ("conditional" if variant_id == "GRADE-7-WORKING-40" else "unavailable")
            and variant.get("availabilityContractId")
            == (
                GRADE_7_AVAILABILITY_CONTRACT_ID
                if variant_id == "GRADE-7-WORKING-40"
                else None
            )
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


def validate_availability_contracts(
    availability_contracts,
    annual_variants,
    integration_contracts,
):
    """Validate the single fail-closed Grade-7 availability contract."""
    _require(
        isinstance(availability_contracts, list)
        and len(availability_contracts) == 1,
        "availability contracts need exactly one contract",
    )
    _require(
        isinstance(annual_variants, dict),
        "validated annual variants must be keyed by variant id",
    )
    _require(
        isinstance(integration_contracts, dict),
        "validated integration contracts must be keyed by contract id",
    )

    contract = availability_contracts[0]
    _require(
        isinstance(contract, dict) and set(contract) == AVAILABILITY_CONTRACT_FIELDS,
        "availability contract fields differ from the IUM10 contract",
    )
    _require(
        contract["id"] == GRADE_7_AVAILABILITY_CONTRACT_ID,
        "availability contract id must be AVAIL-GRADE-7-WORKING-40",
    )
    _require(
        contract["variantId"] == "GRADE-7-WORKING-40",
        "availability contract must reference GRADE-7-WORKING-40",
    )
    _require(
        contract["variantId"] in annual_variants,
        "availability contract references an unknown annual variant",
    )
    _require(
        _positive_int(contract["requiredCapacityUnits"])
        and contract["requiredCapacityUnits"] == 40,
        "availability contract required capacity units must be 40",
    )
    _require(
        _positive_int(contract["comparisonBoundaryUnits"])
        and contract["comparisonBoundaryUnits"] == 38,
        "availability contract comparison boundary units must be 38",
    )

    gates = contract["gates"]
    _require(
        isinstance(gates, dict) and set(gates) == GRADE_7_AVAILABILITY_GATE_IDS,
        "availability contract gate ids differ from the IUM10 contract",
    )
    for gate_id, gate in gates.items():
        _require(
            isinstance(gate, dict) and set(gate) == AVAILABILITY_GATE_FIELDS,
            f"availability contract gate fields differ: {gate_id}",
        )
        _require(
            gate["status"] in AVAILABILITY_GATE_STATUSES,
            f"availability contract gate status is invalid: {gate_id}",
        )
        _require(
            isinstance(gate["requirement"], str) and gate["requirement"].strip(),
            f"availability contract gate requirement must be nonempty: {gate_id}",
        )

    fallback_deltas = contract["fallbackDeltaUnitsByIntegrationContractId"]
    _require(
        isinstance(fallback_deltas, dict)
        and set(fallback_deltas) == set(GRADE_7_FALLBACK_DELTAS),
        "availability contract fallback integration ids differ",
    )
    _require(
        all(
            _positive_int(delta)
            and delta == GRADE_7_FALLBACK_DELTAS[integration_id]
            for integration_id, delta in fallback_deltas.items()
        ),
        "availability contract fallback deltas differ",
    )
    _require(
        set(fallback_deltas) <= set(integration_contracts),
        "availability contract references an unknown integration contract",
    )
    _require(
        _positive_int(contract["maximumFallbackUnits"])
        and contract["maximumFallbackUnits"] == 54
        and contract["maximumFallbackUnits"]
        == contract["requiredCapacityUnits"] + sum(fallback_deltas.values()),
        "availability contract maximum fallback units must be 54",
    )
    _require(
        isinstance(contract["forbiddenCompensations"], list)
        and contract["forbiddenCompensations"] == GRADE_7_FORBIDDEN_COMPENSATIONS,
        "availability contract forbidden compensations differ",
    )
    _require(
        contract["failureMode"] == "fail-closed",
        "availability contract failure mode must be fail-closed",
    )
    _require(
        contract["status"] == "working" and isinstance(contract["status"], str),
        "availability contract status must be working",
    )
    _require(
        contract["risk"] == GRADE_7_AVAILABILITY_CONTRACT_RISK,
        "availability contract risk differs from the canonical contract",
    )
    return {contract["id"]: contract}


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
        and schema_version == 3,
        "schema version must be the integer 3",
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
            validated_availability_contracts = validate_availability_contracts(
                time_model.get("availabilityContracts"),
                validated_annual_variants,
                validated_integration_contracts,
            )
            _validate_grade_7_judgement(
                time_model,
                validated_module_contracts,
                validated_integration_contracts,
                validated_annual_variants,
                validated_availability_contracts,
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
            "projectAssumption",
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
        "official status must be administrative-context; the project assumption is non-normative",
    )

    project_assumption = capacity_model["projectAssumption"]
    _require(
        isinstance(project_assumption, dict),
        "project assumption must be an object",
    )
    _require(
        set(project_assumption)
        == {"nominalUnits", "coreUnits", "bufferUnits", "status"},
        "project assumption fields differ from the IUM10 contract",
    )
    for field in ("nominalUnits", "coreUnits", "bufferUnits"):
        _require(
            isinstance(project_assumption[field], int)
            and not isinstance(project_assumption[field], bool),
            f"project assumption {field} must be an integer",
        )
    _require(
        project_assumption["coreUnits"] == 30
        and project_assumption["bufferUnits"] == 6
        and project_assumption["nominalUnits"]
        == project_assumption["coreUnits"]
        + project_assumption["bufferUnits"],
        "project assumption must remain the non-normative 30 plus 6 model",
    )
    _require(
        project_assumption["status"] == "non-normative-project-assumption",
        "project assumption status must remain non-normative",
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
        "availabilityStatus",
        "availabilityContractId",
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
            variant["kind"] in ANNUAL_PATH_IDS_BY_KIND,
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
            variant["availabilityStatus"] in AVAILABILITY_STATUSES
            and (
                variant["availabilityContractId"] is None
                or isinstance(variant["availabilityContractId"], str)
                and variant["availabilityContractId"].strip()
            ),
            f"annual variant availability status is invalid: {variant_id}",
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
            variant["availabilityStatus"] != "available"
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
        sequence_evidence_id = review["sequenceEvidenceId"]
        sequence_reference_is_allowed = (
            review["sourceTimeImpactLevel"] == "roadmap-dependent"
            and sequence_evidence_id == f"SE-{competency_id}"
        )
        _require(
            expected_evidence_id is None
            and review["decision"] == "unresolved"
            and review["additionalMinutes"] == 0
            and review["phaseIds"] == []
            and review["pathAvailability"] == []
            and review["integrationContractIds"] == []
            and (
                sequence_evidence_id is None
                or sequence_reference_is_allowed
            ),
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


def validate_sequence_evidence(
    sequence_evidence,
    time_reviews,
    annual_variants,
    coverage_payload,
):
    """Validate the four roadmap-wide sequence records by competency id."""
    _require(
        isinstance(sequence_evidence, list) and len(sequence_evidence) == 4,
        "sequence evidence must contain exactly four records",
    )
    _require(
        isinstance(time_reviews, dict),
        "validated time reviews must be keyed by review id",
    )
    _require(
        isinstance(annual_variants, dict),
        "validated annual variants must be keyed by variant id",
    )
    coverage_entries = (
        coverage_payload.get("entries")
        if isinstance(coverage_payload, dict)
        else None
    )
    _require(
        isinstance(coverage_entries, list),
        "coverage payload must contain entries",
    )
    coverage_by_id = {}
    for entry in coverage_entries:
        _require(
            isinstance(entry, dict)
            and isinstance(entry.get("competencyId"), str),
            "coverage entry must have a competency id",
        )
        competency_id = entry["competencyId"]
        _require(
            competency_id not in coverage_by_id,
            f"duplicate coverage competency id: {competency_id}",
        )
        coverage_by_id[competency_id] = entry

    validated = {}
    sequence_ids = set()
    for evidence in sequence_evidence:
        _require(
            isinstance(evidence, dict)
            and set(evidence) == SEQUENCE_EVIDENCE_FIELDS,
            "sequence evidence fields differ from the IUM10 contract",
        )
        competency_id = evidence["competencyId"]
        _require(
            competency_id in SEQUENCE_SCOPES,
            f"unknown sequence competency id: {competency_id}",
        )
        _require(
            competency_id not in validated,
            f"duplicate sequence competency id: {competency_id}",
        )
        sequence_id = evidence["id"]
        _require(
            sequence_id == f"SE-{competency_id}"
            and sequence_id not in sequence_ids,
            f"sequence id mismatch or duplicate: {competency_id}",
        )
        sequence_ids.add(sequence_id)

        expected_scope = SEQUENCE_SCOPES[competency_id]
        _require(
            isinstance(evidence["grades"], list)
            and all(_positive_int(grade) for grade in evidence["grades"])
            and evidence["grades"] == expected_scope["grades"],
            f"sequence grades differ from the approved scope: {competency_id}",
        )
        _require(
            evidence["moduleIds"] == expected_scope["moduleIds"],
            f"sequence modules differ from the approved scope: {competency_id}",
        )

        review_id = f"TR-{competency_id}"
        review = time_reviews.get(review_id)
        _require(
            evidence["timeReviewId"] == review_id
            and isinstance(review, dict)
            and review.get("id") == review_id
            and review.get("competencyId") == competency_id,
            f"sequence review binding is invalid: {competency_id}",
        )
        _require(
            review.get("sourceTimeImpactLevel") == "roadmap-dependent"
            and review.get("decision") == "unresolved"
            and _nonnegative_int(review.get("additionalMinutes"))
            and review.get("additionalMinutes") == 0
            and review.get("phaseIds") == []
            and review.get("integrationContractIds") == []
            and review.get("pathAvailability") == []
            and review.get("sequenceEvidenceId") == sequence_id,
            f"sequence review must remain unresolved and unallocated: {competency_id}",
        )

        expected_modules_by_grade = {
            grade: [
                module_id
                for module_id in expected_scope["moduleIds"]
                if module_id.startswith(f"IUM-{grade}-")
            ]
            for grade in expected_scope["grades"]
        }
        progression = evidence["progression"]
        _require(
            isinstance(progression, list)
            and len(progression) == len(expected_modules_by_grade),
            f"sequence progression must cover every grade: {competency_id}",
        )
        progression_by_grade = {}
        for step in progression:
            _require(
                isinstance(step, dict)
                and set(step) == SEQUENCE_PROGRESSION_FIELDS,
                f"sequence progression fields are invalid: {competency_id}",
            )
            grade = step["grade"]
            _require(
                _positive_int(grade)
                and grade in expected_modules_by_grade
                and grade not in progression_by_grade
                and step["moduleIds"] == expected_modules_by_grade[grade]
                and isinstance(step["learningDepth"], str)
                and step["learningDepth"].strip(),
                f"sequence progression is incomplete: {competency_id}/{grade}",
            )
            progression_by_grade[grade] = step
        _require(
            set(progression_by_grade) == set(expected_modules_by_grade),
            f"sequence progression grades are incomplete: {competency_id}",
        )

        depth_records = evidence["operatorProductDepth"]
        _require(
            isinstance(depth_records, list)
            and len(depth_records) == len(expected_modules_by_grade),
            f"operator/product depth must cover every grade: {competency_id}",
        )
        depth_by_grade = {}
        for depth in depth_records:
            _require(
                isinstance(depth, dict)
                and set(depth) == SEQUENCE_DEPTH_FIELDS,
                f"operator/product depth fields are invalid: {competency_id}",
            )
            grade = depth["grade"]
            _require(
                _positive_int(grade)
                and grade in expected_modules_by_grade
                and grade not in depth_by_grade
                and isinstance(depth["operatorDepth"], str)
                and depth["operatorDepth"].strip()
                and isinstance(depth["productDepth"], str)
                and depth["productDepth"].strip(),
                f"operator/product depth is incomplete: {competency_id}/{grade}",
            )
            depth_by_grade[grade] = depth
        _require(
            set(depth_by_grade) == set(expected_modules_by_grade),
            f"operator/product depth grades are incomplete: {competency_id}",
        )

        perspectives = evidence["perspectiveWeighting"]
        _require(
            isinstance(perspectives, list) and bool(perspectives),
            f"perspective weighting must be nonempty: {competency_id}",
        )
        perspective_ids = set()
        perspective_module_ids = set()
        for perspective in perspectives:
            _require(
                isinstance(perspective, dict)
                and set(perspective) == SEQUENCE_PERSPECTIVE_FIELDS,
                f"perspective weighting fields are invalid: {competency_id}",
            )
            perspective_id = perspective["perspective"]
            module_ids = perspective["moduleIds"]
            _require(
                isinstance(perspective_id, str)
                and perspective_id.strip()
                and perspective_id not in perspective_ids
                and _nonempty_string_list(module_ids)
                and bool(module_ids)
                and set(module_ids) <= set(expected_scope["moduleIds"])
                and isinstance(perspective["rationale"], str)
                and perspective["rationale"].strip(),
                f"perspective weighting is incomplete: {competency_id}",
            )
            perspective_ids.add(perspective_id)
            perspective_module_ids.update(module_ids)
        _require(
            perspective_module_ids == set(expected_scope["moduleIds"]),
            f"perspective weighting must cover the complete sequence: {competency_id}",
        )
        if competency_id in GRADE_7_BALANCE_SEQUENCE_IDS:
            _require(
                perspective_ids
                == {"technical", "application", "societal", "media"},
                f"grade 7 sequence needs all four perspectives: {competency_id}",
            )
            media_modules = next(
                item["moduleIds"]
                for item in perspectives
                if item["perspective"] == "media"
            )
            _require(
                set(media_modules)
                == {"IUM-7-CORE-08", "IUM-7-CORE-09", "IUM-7-CORE-10"},
                f"grade 7 media perspective cannot use a CORE-08 proxy: {competency_id}",
            )

        time_evidence = evidence["timeEvidence"]
        expected_variant_modules = expected_scope["variantModuleIds"]
        _require(
            isinstance(time_evidence, list)
            and len(time_evidence) == len(expected_variant_modules),
            f"sequence time evidence has the wrong size: {competency_id}",
        )
        time_evidence_by_variant = {}
        for time_record in time_evidence:
            _require(
                isinstance(time_record, dict)
                and set(time_record) == SEQUENCE_TIME_EVIDENCE_FIELDS,
                f"sequence time evidence fields are invalid: {competency_id}",
            )
            variant_id = time_record["variantId"]
            variant = annual_variants.get(variant_id)
            _require(
                variant_id in expected_variant_modules
                and variant_id not in time_evidence_by_variant
                and isinstance(variant, dict),
                f"unknown or duplicate sequence variant: {competency_id}/{variant_id}",
            )
            scope_module_ids = expected_variant_modules[variant_id]
            expected_variant_grades = {
                int(module_id.split("-")[1]) for module_id in scope_module_ids
            }
            _require(
                len(expected_variant_grades) == 1,
                f"sequence variant scope spans multiple grades: {competency_id}/{variant_id}",
            )
            expected_variant_grade = next(iter(expected_variant_grades))
            expected_variant_kind = (
                "working-target"
                if variant_id == "GRADE-7-WORKING-40"
                else "demand-scenario"
                if expected_variant_grade == 7
                else "planning-path"
            )
            _require(
                variant.get("id") == variant_id
                and _positive_int(variant.get("grade"))
                and variant["grade"] == expected_variant_grade
                and variant.get("kind") == expected_variant_kind
                and variant.get("availabilityStatus") in AVAILABILITY_STATUSES,
                f"sequence variant identity is invalid: {competency_id}/{variant_id}",
            )
            allocations = variant.get("allocations")
            _require(
                isinstance(allocations, list),
                f"sequence variant allocations are invalid: {variant_id}",
            )
            allocation_units = {}
            for allocation in allocations:
                _require(
                    isinstance(allocation, dict)
                    and isinstance(allocation.get("moduleId"), str)
                    and allocation["moduleId"] not in allocation_units
                    and _positive_int(allocation.get("units")),
                    f"sequence variant allocation is invalid: {variant_id}",
                )
                allocation_units[allocation["moduleId"]] = allocation["units"]
            _require(
                time_record["scopeModuleIds"] == scope_module_ids
                and set(scope_module_ids) <= set(allocation_units),
                f"sequence time scope differs from variant allocations: {competency_id}/{variant_id}",
            )
            derived_scope_units = sum(
                allocation_units[module_id] for module_id in scope_module_ids
            )
            _require(
                time_record["availabilityStatus"] == variant["availabilityStatus"],
                f"sequence time evidence availability differs: {competency_id}",
            )
            _require(
                _positive_int(variant.get("targetUnits"))
                and _positive_int(time_record["targetUnits"])
                and time_record["targetUnits"] == variant["targetUnits"]
                and _positive_int(time_record["scopeUnits"])
                and time_record["scopeUnits"] == derived_scope_units
                and isinstance(time_record["rationale"], str)
                and time_record["rationale"].strip(),
                f"sequence time facts are not derived from the variant: {competency_id}/{variant_id}",
            )
            weight_groups = time_record["weightGroups"]
            if competency_id in GRADE_7_BALANCE_SEQUENCE_IDS:
                _require(
                    isinstance(weight_groups, list)
                    and len(weight_groups) == len(SEQUENCE_GRADE_7_WEIGHT_GROUPS),
                    f"grade 7 sequence needs both time weight groups: {competency_id}/{variant_id}",
                )
                groups_by_id = {}
                for group in weight_groups:
                    _require(
                        isinstance(group, dict)
                        and set(group) == SEQUENCE_WEIGHT_GROUP_FIELDS,
                        f"sequence time weight fields are invalid: {competency_id}/{variant_id}",
                    )
                    group_id = group["id"]
                    expected_group_modules = SEQUENCE_GRADE_7_WEIGHT_GROUPS.get(
                        group_id
                    )
                    _require(
                        isinstance(expected_group_modules, list)
                        and group_id not in groups_by_id
                        and group["moduleIds"] == expected_group_modules
                        and _positive_int(group["units"])
                        and group["units"] == sum(
                            allocation_units[module_id]
                            for module_id in expected_group_modules
                        ),
                        f"sequence time weight is not allocation-derived: {competency_id}/{variant_id}/{group_id}",
                    )
                    groups_by_id[group_id] = group
                _require(
                    set(groups_by_id) == set(SEQUENCE_GRADE_7_WEIGHT_GROUPS),
                    f"grade 7 time weight groups are incomplete: {competency_id}/{variant_id}",
                )
            else:
                _require(
                    weight_groups == [],
                    f"only grade 7 balance records use weight groups: {competency_id}/{variant_id}",
                )
            time_evidence_by_variant[variant_id] = time_record
        _require(
            set(time_evidence_by_variant) == set(expected_variant_modules),
            f"sequence variants differ from the approved scope: {competency_id}",
        )

        _require(
            isinstance(evidence["remainingBoundary"], str)
            and evidence["remainingBoundary"].strip(),
            f"sequence remaining boundary must be nonempty: {competency_id}",
        )
        _require(
            evidence["fachAuditStatus"] == "passed",
            f"sequence fach audit must be passed: {competency_id}",
        )
        decision = evidence["coverageDecision"]
        _require(
            decision == expected_scope["coverageDecision"],
            f"sequence coverage decision differs from the fach audit: {competency_id}",
        )
        if decision == "covered":
            _require(
                any(item["availabilityStatus"] == "available" for item in time_evidence),
                f"covered sequence needs a genuinely available annual path: {competency_id}",
            )
            expected_coverage_status = "covered"
            expected_semantic_audit = "operator-product-match"
        else:
            expected_coverage_status = "partial"
            expected_semantic_audit = "documented-gap"

        consequence = evidence["coverageConsequence"]
        _require(
            isinstance(consequence, dict)
            and set(consequence) == SEQUENCE_COVERAGE_CONSEQUENCE_FIELDS
            and consequence["coverageStatus"] == expected_coverage_status
            and consequence["semanticAudit"] == expected_semantic_audit
            and isinstance(consequence["rationale"], str)
            and consequence["rationale"].strip(),
            f"sequence coverage consequence is invalid: {competency_id}",
        )
        coverage_entry = coverage_by_id.get(competency_id)
        _require(
            isinstance(coverage_entry, dict)
            and coverage_entry.get("coverageStatus") == expected_coverage_status
            and coverage_entry.get("semanticAudit") == expected_semantic_audit,
            f"sequence decision differs from coverage plan: {competency_id}",
        )
        if decision == "covered":
            _require(
                "reason" not in coverage_entry,
                f"covered sequence cannot retain a contradictory gap reason: {competency_id}",
            )
            for anchor in SEQUENCE_COVERAGE_ANCHORS[competency_id]:
                _require(
                    coverage_entry.get("requirementText")
                    == SEQUENCE_COVERAGE_ANCHORS[competency_id][0]
                    and isinstance(coverage_entry.get("evidence"), str)
                    and anchor in coverage_entry["evidence"]
                    and isinstance(coverage_entry.get("matchRationale"), str)
                    and anchor in coverage_entry["matchRationale"],
                    f"coverage sequence lacks an immutable source/action/product string: {competency_id}",
                )

        boundary = evidence["evidenceBoundary"]
        _require(
            isinstance(boundary, dict)
            and set(boundary) == SEQUENCE_EVIDENCE_BOUNDARY_FIELDS
            and boundary["privateEvidence"] == "excluded"
            and boundary["singleModuleProxy"] == "excluded"
            and boundary["automatedPersonalAssessment"] == "excluded"
            and isinstance(boundary["rationale"], str)
            and boundary["rationale"].strip(),
            f"sequence evidence boundary is invalid: {competency_id}",
        )
        _require(
            evidence["status"] == "working",
            f"sequence evidence status must be working: {competency_id}",
        )
        validated[competency_id] = evidence

    _require(
        set(validated) == ROADMAP_DEPENDENT_IDS,
        "sequence evidence ids differ from the four roadmap-dependent records",
    )
    return validated


def _validate_sequence_judgement_statuses(grade_judgements, sequence_evidence):
    _require(
        isinstance(grade_judgements, list)
        and len(grade_judgements) == 3
        and all(isinstance(judgement, dict) for judgement in grade_judgements)
        and [judgement.get("grade") for judgement in grade_judgements]
        == [5, 6, 7]
        and all(
            _positive_int(judgement["grade"])
            for judgement in grade_judgements
        )
        and isinstance(sequence_evidence, dict)
        and set(sequence_evidence) == ROADMAP_DEPENDENT_IDS,
        "sequence judgements require exact grade 5, 6, and 7 objects",
    )
    judgements_by_grade = {}
    for judgement in grade_judgements:
        if (
            not isinstance(judgement, dict)
            or not _positive_int(judgement.get("grade"))
            or judgement.get("grade") not in {5, 6, 7}
        ):
            continue
        grade = judgement["grade"]
        _require(
            grade not in judgements_by_grade,
            f"duplicate grade judgement: {grade}",
        )
        judgements_by_grade[grade] = judgement
    _require(
        set(judgements_by_grade) == {5, 6, 7},
        "sequence evidence needs grade 5, 6, and 7 judgements",
    )
    expected_statuses = {5: "covered", 6: "covered", 7: "covered"}
    for grade, expected_status in expected_statuses.items():
        _require(
            judgements_by_grade[grade].get("sequenceEvidenceStatus")
            == expected_status,
            f"grade {grade} sequence evidence status must be {expected_status}",
        )
    return judgements_by_grade


def validate_risks(risks):
    """Validate the small, non-numeric IUM10 risk register."""
    _require(
        isinstance(risks, list) and len(risks) == len(RISK_SCOPES),
        "risk register must contain exactly five records",
    )
    validated = {}
    for risk in risks:
        _require(
            isinstance(risk, dict) and set(risk) == RISK_FIELDS,
            "risk fields differ from the IUM10 contract",
        )
        risk_id = risk["id"]
        _require(
            isinstance(risk_id, str)
            and risk_id in RISK_SCOPES
            and risk_id not in validated,
            f"unknown or duplicate risk id: {risk_id}",
        )
        _require(
            risk["scope"] == RISK_SCOPES[risk_id],
            f"risk scope differs from the approved register: {risk_id}",
        )
        for field in ("risk", "impact", "mitigation"):
            _require(
                isinstance(risk[field], str) and risk[field].strip(),
                f"risk {field} must be a nonempty string: {risk_id}",
            )
        _require(
            risk["status"] == "working"
            and isinstance(risk["status"], str),
            f"risk status must remain working: {risk_id}",
        )
        validated[risk_id] = risk
    _require(
        set(validated) == set(RISK_SCOPES),
        "risk ids differ from the approved register",
    )
    _require(
        _canonical_sha256(
            sorted(validated.values(), key=lambda risk: risk["id"])
        )
        == APPROVED_RISK_REGISTER_SHA256,
        "risk register differs from the approved canonical facts",
    )
    return validated


def validate_pilot_assignments(
    pilot_assignments,
    module_contracts,
    integration_contracts,
    annual_variants,
    availability_contracts,
):
    """Validate all privacy-safe pilots against their approved scope contracts."""
    _require(
        isinstance(module_contracts, dict) and len(module_contracts) == 31,
        "pilot assignments require exactly 31 validated module contracts",
    )
    _require(
        isinstance(integration_contracts, dict)
        and set(GRADE_7_INTEGRATION_IDS) <= set(integration_contracts),
        "pilot assignments require all four validated grade 7 integrations",
    )
    _require(
        isinstance(annual_variants, dict)
        and "GRADE-7-WORKING-40" in annual_variants,
        "pilot assignments require the grade 7 working annual variant",
    )
    _require(
        isinstance(availability_contracts, dict)
        and GRADE_7_AVAILABILITY_CONTRACT_ID in availability_contracts,
        "pilot assignments require the grade 7 availability contract",
    )
    expected = {}
    for module_id, contract in module_contracts.items():
        expected[f"PILOT-{module_id}"] = {
            "scopeType": "module",
            "scopeIds": [module_id],
            "contractIds": [contract["id"]],
            "aggregationLevel": "module",
            "fallback": "nonpersonal-module-replanning",
        }
    for integration_id in sorted(GRADE_7_INTEGRATION_IDS):
        expected[f"PILOT-{integration_id}"] = {
            "scopeType": "integration",
            "scopeIds": [integration_id],
            "contractIds": [integration_id],
            "aggregationLevel": "integration",
            "fallback": "standalone-module-time",
        }
    expected["PILOT-GRADE-7-WORKING-40"] = {
        "scopeType": "annual-variant",
        "scopeIds": ["GRADE-7-WORKING-40"],
        "contractIds": [GRADE_7_AVAILABILITY_CONTRACT_ID],
        "aggregationLevel": "annual-variant",
        "fallback": "nonpersonal-annual-replanning",
    }
    _require(
        isinstance(pilot_assignments, list) and len(pilot_assignments) == 36,
        "pilot assignments must contain exactly 36 typed records",
    )
    validated = {}
    for pilot in pilot_assignments:
        _require(
            isinstance(pilot, dict)
            and set(pilot) == PILOT_ASSIGNMENT_FIELDS,
            "pilot assignment fields differ from the IUM10 contract",
        )
        pilot_id = pilot["id"]
        _require(
            isinstance(pilot_id, str)
            and pilot_id in expected
            and pilot_id not in validated,
            f"unknown or duplicate pilot id: {pilot_id}",
        )
        contract = expected[pilot_id]
        _require(
            pilot["scopeType"] in PILOT_SCOPE_TYPES
            and all(pilot[field] == value for field, value in contract.items()),
            f"pilot scope contract differs from the approved assignment: {pilot_id}",
        )
        _require(
            pilot["measures"] == PILOT_MEASURES,
            f"pilot measures differ from the approved aggregate: {pilot_id}",
        )
        _require(
            pilot["personalData"] == "prohibited"
            and pilot["personalTelemetry"] == "prohibited"
            and pilot["privateReflectionEvidence"] == "prohibited",
            f"pilot privacy evidence must be prohibited: {pilot_id}",
        )
        _require(
            pilot["excludedUses"] == PILOT_EXCLUDED_USES,
            f"pilot excluded uses differ from the approved aggregate: {pilot_id}",
        )
        _require(
            pilot["status"] in PILOT_STATUSES,
            f"pilot status is invalid: {pilot_id}",
        )
        validated[pilot_id] = pilot
    _require(
        set(validated) == set(expected),
        "pilot ids differ from the 36 approved assignments",
    )
    return validated


def _validate_final_grade_judgements(
    grade_judgements,
    sequence_evidence,
    annual_variants,
    coverage_payload,
    time_reviews,
    module_contracts,
    availability_contracts,
    pilot_assignments,
):
    judgements = _validate_sequence_judgement_statuses(
        grade_judgements,
        sequence_evidence,
    )
    fields = {
        "grade",
        "availabilityStatus",
        "semanticCoverageStatus",
        "timeFeasibilityStatus",
        "sequenceEvidenceStatus",
        "pilotStatus",
        "annualVariantIds",
        "rationale",
        "risk",
        "decisionOptions",
    }
    expected = {
        5: {
            "availability": "available",
            "semantic": "partial",
            "time": "green",
            "sequence": "covered",
            "variants": [
                "GRADE-5-BASELINE",
                "GRADE-5-REGULAR",
                "GRADE-5-EXTENDED",
            ],
            "options": [
                "pilot-grade-5-time-model",
                "retain-semantic-gaps",
            ],
            "rationale": GRADE_5_JUDGEMENT_RATIONALE,
        },
        6: {
            "availability": "available",
            "semantic": "covered",
            "time": "green",
            "sequence": "covered",
            "variants": [
                "GRADE-6-BASELINE",
                "GRADE-6-REGULAR",
                "GRADE-6-EXTENDED-REFERENCE",
                "GRADE-6-EXTENDED-TRANSFER",
                "GRADE-6-EXTENDED-CODING",
            ],
            "options": [
                "pilot-grade-6-time-model",
                "fall-back-to-standalone-integration-time",
            ],
            "rationale": GRADE_6_JUDGEMENT_RATIONALE,
        },
        7: {
            "availability": "conditional",
            "semantic": "partial",
            "time": "amber",
            "sequence": "covered",
            "variants": [
                "GRADE-7-WORKING-40",
                "GRADE-7-ROBUST-DEMAND",
                "GRADE-7-HISTORICAL-MINIMUM",
            ],
            "options": GRADE_7_DECISION_OPTIONS,
            "rationale": GRADE_7_UNIMPLEMENTED_OPTIONS_RATIONALE,
        },
    }

    derived_semantic = {grade: "covered" for grade in expected}
    coverage_entries = coverage_payload.get("entries", [])
    _require(
        isinstance(coverage_entries, list),
        "coverage entries are required for final grade judgements",
    )
    for entry in coverage_entries:
        if not isinstance(entry, dict) or entry.get("coverageStatus") != "partial":
            continue
        review = time_reviews.get(entry.get("timeReviewId"))
        _require(
            isinstance(review, dict),
            "every current partial coverage entry needs a validated time review",
        )
        contract = module_contracts.get(review.get("moduleId"))
        _require(
            isinstance(contract, dict) and contract.get("grade") in expected,
            "every current partial coverage entry needs a validated module grade",
        )
        derived_semantic[contract["grade"]] = "partial"

    operational_state = derive_grade_7_operational_state(
        availability_contracts[GRADE_7_AVAILABILITY_CONTRACT_ID],
        pilot_assignments,
    )
    pilot_gate_status = availability_contracts[
        GRADE_7_AVAILABILITY_CONTRACT_ID
    ]["gates"]["pilot"]["status"]
    _require(
        pilot_gate_status != "passed"
        or all(
            pilot_assignments[pilot_id]["status"] == "completed"
            for pilot_id in GRADE_7_REQUIRED_PILOT_IDS
        ),
        "grade 7 pilot gate cannot pass without all required pilots completed",
    )

    for grade, judgement in judgements.items():
        contract = expected[grade]
        grade_7_state = operational_state if grade == 7 else None
        _require(
            set(judgement) == fields
            and judgement["availabilityStatus"]
            == (grade_7_state["availabilityStatus"] if grade_7_state else contract["availability"])
            and judgement["semanticCoverageStatus"] == contract["semantic"]
            and judgement["semanticCoverageStatus"] == derived_semantic[grade]
            and judgement["timeFeasibilityStatus"]
            == (grade_7_state["timeFeasibilityStatus"] if grade_7_state else contract["time"])
            and judgement["sequenceEvidenceStatus"] == contract["sequence"]
            and judgement["pilotStatus"]
            == (grade_7_state["pilotStatus"] if grade_7_state else "not-started")
            and judgement["annualVariantIds"] == contract["variants"]
            and judgement["decisionOptions"] == contract["options"]
            and all(
                variant_id in annual_variants
                for variant_id in judgement["annualVariantIds"]
            )
            and judgement["rationale"] == contract["rationale"]
            and isinstance(judgement["risk"], str)
            and judgement["risk"].strip(),
            f"grade {grade} judgement differs from the approved final contract",
        )
    return judgements


@_validation_boundary("IUM09 coverage projection")
def ium09_coverage_projection(
    coverage_payload,
    remediation_payload,
    sequence_evidence,
):
    """Return a deep-copied coverage payload restored to IUM09 after-status."""
    _require(
        _current_coverage_fingerprint(coverage_payload)
        == CURRENT_COVERAGE_SHA256,
        "current coverage records differ from the approved IUM10 source",
    )
    _require(
        isinstance(sequence_evidence, list) and len(sequence_evidence) == 4,
        "IUM09 projection requires exactly four sequence decisions",
    )
    sequence_by_id = {}
    expected_decisions = {
        "LH26-E-PROG-001": "covered",
        "LH26-E-PROG-002": "covered",
        "LH26-E-PROG-003": "remain-partial",
        "LH26-E-PROG-004": "remain-partial",
    }
    for evidence in sequence_evidence:
        _require(
            isinstance(evidence, dict),
            "sequence decision must be an object",
        )
        competency_id = evidence.get("competencyId")
        _require(
            isinstance(competency_id, str)
            and competency_id in expected_decisions
            and competency_id not in sequence_by_id
            and evidence.get("id") == f"SE-{competency_id}"
            and evidence.get("timeReviewId") == f"TR-{competency_id}",
            f"unknown, duplicate, or mismatched sequence decision: {competency_id}",
        )
        decision = expected_decisions[competency_id]
        expected_status = "covered" if decision == "covered" else "partial"
        expected_audit = (
            "operator-product-match"
            if decision == "covered"
            else "documented-gap"
        )
        consequence = evidence.get("coverageConsequence")
        _require(
            evidence.get("coverageDecision") == decision
            and isinstance(consequence, dict)
            and consequence.get("coverageStatus") == expected_status
            and consequence.get("semanticAudit") == expected_audit,
            f"contradictory sequence decision: {competency_id}",
        )
        sequence_by_id[competency_id] = evidence
    _require(
        set(sequence_by_id) == ROADMAP_DEPENDENT_IDS,
        "sequence decisions differ from the four roadmap records",
    )

    remediation_entries = (
        remediation_payload.get("entries")
        if isinstance(remediation_payload, dict)
        else None
    )
    _require(
        isinstance(remediation_entries, list)
        and len(remediation_entries) == 60,
        "IUM09 projection requires all 60 remediation records",
    )
    remediation_by_id = {}
    for remediation in remediation_entries:
        _require(
            isinstance(remediation, dict)
            and isinstance(remediation.get("competencyId"), str)
            and remediation["competencyId"] not in remediation_by_id,
            "remediation ids for IUM09 projection must be unique",
        )
        remediation_by_id[remediation["competencyId"]] = remediation
    _require(
        set(remediation_by_id) == BASELINE_PARTIAL_IDS,
        "IUM09 projection remediation ids differ from the baseline",
    )

    projection = copy.deepcopy(coverage_payload)
    entries = projection.get("entries") if isinstance(projection, dict) else None
    _require(
        isinstance(entries, list) and len(entries) == 171,
        "IUM09 projection requires exactly 171 coverage records",
    )
    coverage_ids = set()
    for entry in entries:
        _require(
            isinstance(entry, dict)
            and isinstance(entry.get("competencyId"), str)
            and entry["competencyId"] not in coverage_ids,
            "coverage ids for IUM09 projection must be unique",
        )
        coverage_ids.add(entry["competencyId"])
        competency_id = entry["competencyId"]
        if competency_id in expected_decisions:
            decision = expected_decisions[competency_id]
            expected_status = "covered" if decision == "covered" else "partial"
            expected_audit = (
                "operator-product-match"
                if decision == "covered"
                else "documented-gap"
            )
            _require(
                entry.get("coverageStatus") == expected_status
                and entry.get("semanticAudit") == expected_audit,
                f"coverage contradicts sequence decision: {competency_id}",
            )
        if competency_id not in COVERED_SEQUENCE_IDS:
            continue
        remediation = remediation_by_id[competency_id]
        after = remediation.get("after")
        residual_gap = remediation.get("residualGap")
        _require(
            remediation.get("decision") == "remain-partial"
            and after
            == {
                "coverageStatus": "partial",
                "semanticAudit": "documented-gap",
            }
            and isinstance(residual_gap, dict)
            and set(residual_gap) == {"reason", "risk", "followUp"}
            and all(
                isinstance(residual_gap[field], str)
                and residual_gap[field].strip()
                for field in ("reason", "risk", "followUp")
            )
            and entry.get("coverageStatus") == "covered"
            and entry.get("semanticAudit") == "operator-product-match",
            f"invalid IUM09 projection source: {competency_id}",
        )
        entry.update(after)
        entry.update(residual_gap)
    _require(
        len(coverage_ids) == 171,
        "IUM09 projection coverage ids must be unique",
    )
    return projection


@_validation_boundary("IUM10 time references")
def validate_time_references(
    module_payload,
    coverage_payload,
    remediation_payload,
    validated_time_model,
):
    """Validate all cross-artifact IUM10 references."""
    _require(
        isinstance(validated_time_model, dict),
        "validated time model must be an indexed mapping",
    )
    module_contracts = validated_time_model.get("moduleContracts")
    time_reviews = validated_time_model.get("timeReviews")
    sequence_evidence = validated_time_model.get("sequenceEvidence")
    annual_variants = validated_time_model.get("annualVariants")
    availability_contracts = validated_time_model.get("availabilityContracts")
    pilot_assignments = validated_time_model.get("pilotAssignments")
    _require(
        isinstance(module_contracts, dict) and len(module_contracts) == 31,
        "validated time model must contain 31 module contracts",
    )
    _require(
        isinstance(time_reviews, dict) and len(time_reviews) == 60,
        "validated time model must contain 60 time reviews",
    )
    _require(
        isinstance(sequence_evidence, dict) and len(sequence_evidence) == 4,
        "validated time model must contain four sequence records",
    )
    _require(
        isinstance(annual_variants, dict)
        and set(GRADE_7_VARIANT_TARGETS) <= set(annual_variants),
        "validated time model must contain the grade 7 annual variants",
    )
    _require(
        isinstance(availability_contracts, dict)
        and set(availability_contracts) == {GRADE_7_AVAILABILITY_CONTRACT_ID}
        and availability_contracts[GRADE_7_AVAILABILITY_CONTRACT_ID].get("variantId")
        == "GRADE-7-WORKING-40",
        "validated time model must contain the grade 7 availability contract",
    )
    _require(
        isinstance(pilot_assignments, dict)
        and GRADE_7_REQUIRED_PILOT_IDS <= set(pilot_assignments),
        "validated time model must contain all required grade 7 pilots",
    )
    _require(
        set(APPROVED_TIME_AUDIT) == set(BASELINE_PARTIAL_IDS)
        and len(APPROVED_TIME_AUDIT) == 60,
        "approved time audit registry must contain the 60 baseline handoffs",
    )

    modules = module_payload.get("modules") if isinstance(module_payload, dict) else None
    model_notes = (
        module_payload.get("modelNotes")
        if isinstance(module_payload, dict)
        else None
    )
    _require(
        isinstance(model_notes, dict)
        and model_notes.get("timeBoundary") == AUTHORITATIVE_TIME_BOUNDARY,
        "module modelNotes.timeBoundary differs from the authoritative time boundary",
    )
    _require(
        isinstance(modules, list) and len(modules) == 31,
        "module references require exactly 31 modules",
    )
    time_contract_ids = set()
    for module in modules:
        _require(isinstance(module, dict), "module reference must be an object")
        module_id = module.get("id")
        contract_id = module.get("timeContractId")
        contract = (
            module_contracts.get(module_id)
            if isinstance(module_id, str)
            else None
        )
        _require(
            isinstance(module_id, str)
            and isinstance(contract_id, str)
            and contract_id == f"TC-{module_id}"
            and contract_id not in time_contract_ids
            and isinstance(contract, dict)
            and contract.get("id") == contract_id
            and contract.get("moduleId") == module_id
            and contract.get("historicalLessonRange") == module.get("lessonRange"),
            f"invalid module time reference: {module_id}",
        )
        time_contract_ids.add(contract_id)
    _require(
        time_contract_ids == {contract["id"] for contract in module_contracts.values()},
        "module time references differ from the 31 contracts",
    )

    remediation_entries = remediation_payload.get("entries") if isinstance(remediation_payload, dict) else None
    _require(
        isinstance(remediation_entries, list) and len(remediation_entries) == 60,
        "remediation references require exactly 60 records",
    )
    remediation_by_id = {}
    time_review_ids = set()
    for entry in remediation_entries:
        _require(isinstance(entry, dict), "remediation reference must be an object")
        competency_id = entry.get("competencyId")
        review_id = entry.get("timeReviewId")
        review = (
            time_reviews.get(review_id)
            if isinstance(review_id, str)
            else None
        )
        _require(
            isinstance(competency_id, str)
            and competency_id not in remediation_by_id
            and review_id == f"TR-{competency_id}"
            and review_id not in time_review_ids
            and isinstance(review, dict),
            f"invalid remediation time reference: {competency_id}",
        )
        approved = APPROVED_TIME_AUDIT.get(competency_id)
        _require(
            approved
            == (
                review.get("moduleId"),
                review.get("sourceTimeImpactLevel"),
                review.get("decision"),
                review.get("additionalMinutes"),
            )
            and review.get("id") == review_id
            and review.get("competencyId") == competency_id
            and _nonnegative_int(review.get("additionalMinutes"))
            and isinstance(entry.get("before"), dict)
            and review.get("moduleId") == entry["before"].get("evidenceModuleId")
            and review.get("sourceTimeImpactLevel") == entry.get("timeImpact", {}).get("level"),
            f"time review differs from its approved registration: {competency_id}",
        )
        _require(
            "sequenceEvidenceId" not in entry,
            f"remediation cannot carry a sequence evidence reference: {competency_id}",
        )
        remediation_by_id[competency_id] = entry
        time_review_ids.add(review_id)
    _require(
        set(remediation_by_id) == set(BASELINE_PARTIAL_IDS)
        and time_review_ids == set(time_reviews),
        "remediation time references differ from the 60 reviews",
    )

    coverage_entries = coverage_payload.get("entries") if isinstance(coverage_payload, dict) else None
    _require(
        isinstance(coverage_entries, list) and len(coverage_entries) == 171,
        "coverage references require exactly 171 records",
    )
    coverage_ids = set()
    coverage_time_review_ids = set()
    coverage_sequence_ids = set()
    for entry in coverage_entries:
        _require(isinstance(entry, dict), "coverage reference must be an object")
        competency_id = entry.get("competencyId")
        _require(
            isinstance(competency_id, str) and competency_id not in coverage_ids,
            f"duplicate or invalid coverage reference id: {competency_id}",
        )
        coverage_ids.add(competency_id)
        if competency_id in remediation_by_id:
            expected_review_id = f"TR-{competency_id}"
            _require(
                entry.get("timeReviewId") == expected_review_id
                and expected_review_id not in coverage_time_review_ids,
                f"invalid coverage time reference: {competency_id}",
            )
            coverage_time_review_ids.add(expected_review_id)
        else:
            _require(
                "timeReviewId" not in entry,
                f"legacy coverage record cannot carry a time review: {competency_id}",
            )
        if competency_id in ROADMAP_DEPENDENT_IDS:
            expected_sequence_id = f"SE-{competency_id}"
            _require(
                entry.get("sequenceEvidenceId") == expected_sequence_id
                and expected_sequence_id not in coverage_sequence_ids
                and competency_id in sequence_evidence,
                f"invalid coverage sequence reference: {competency_id}",
            )
            coverage_sequence_ids.add(expected_sequence_id)
        else:
            _require(
                "sequenceEvidenceId" not in entry,
                f"non-roadmap coverage record cannot carry sequence evidence: {competency_id}",
            )
    _require(
        coverage_time_review_ids == time_review_ids,
        "coverage time references differ from the 60 reviews",
    )
    _require(
        coverage_sequence_ids == {f"SE-{competency_id}" for competency_id in ROADMAP_DEPENDENT_IDS},
        "coverage sequence references differ from the four records",
    )
    working_40_review_ids = set()
    for review_id, review in time_reviews.items():
        path_availability = review.get("pathAvailability") if isinstance(review, dict) else None
        _require(
            isinstance(path_availability, list)
            and len(path_availability) == len(set(path_availability))
            and all(
                isinstance(variant_id, str) and variant_id in annual_variants
                for variant_id in path_availability
            ),
            f"validated time review has invalid path availability: {review_id}",
        )
        if "GRADE-7-WORKING-40" in path_availability:
            working_40_review_ids.add(review_id)
    _require(
        working_40_review_ids == GRADE_7_WORKING_40_REVIEW_IDS,
        "working-40 path availability references differ from the approved contract",
    )
    return {
        "timeContractIds": time_contract_ids,
        "timeReviewIds": time_review_ids,
        "sequenceEvidenceIds": coverage_sequence_ids,
        "availabilityContractIds": set(availability_contracts),
        "requiredGrade7PilotIds": set(GRADE_7_REQUIRED_PILOT_IDS),
        "working40PathAvailabilityReviewIds": working_40_review_ids,
    }


@_validation_boundary("IUM10 baseline")
def validate_ium10_baseline(module_payload, coverage_payload, remediation_payload):
    """Validate the immutable IUM09 baseline consumed by IUM10."""
    modules = module_payload.get("modules") if isinstance(module_payload, dict) else None
    _require(isinstance(modules, list), "module payload must contain modules")
    _require(
        all(
            isinstance(module, dict)
            and isinstance(module.get("id"), str)
            and module["id"].strip()
            for module in modules
        ),
        "module records must have string ids",
    )
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
    _require(
        all(
            isinstance(entry, dict)
            and isinstance(entry.get("competencyId"), str)
            and entry["competencyId"].strip()
            for entry in coverage_entries
        ),
        "coverage records must have string competency ids",
    )
    coverage_ids = {entry["competencyId"] for entry in coverage_entries}
    _require(len(coverage_ids) == len(coverage_entries) == 171, "coverage ids must be exactly 171 and unique")
    historical_coverage_statuses = []
    for entry in coverage_entries:
        competency_id = entry["competencyId"]
        if competency_id in COVERED_SEQUENCE_IDS:
            _require(
                entry.get("coverageStatus") == "covered"
                and entry.get("semanticAudit") == "operator-product-match",
                f"task 24 sequence upgrade is missing: {competency_id}",
            )
            historical_coverage_statuses.append("partial")
        else:
            historical_coverage_statuses.append(entry["coverageStatus"])
    _require(
        Counter(historical_coverage_statuses)
        == Counter({"covered": 164, "partial": 7}),
        "coverage status counts differ from immutable IUM09 baseline",
    )
    _require(
        coverage_projection_fingerprint(coverage_payload, remediation_payload)
        == BASELINE_COVERAGE_PROJECTION_SHA256,
        "coverage projection fingerprint differs from immutable IUM09 baseline",
    )
    _require(
        _current_coverage_fingerprint(coverage_payload)
        == CURRENT_COVERAGE_SHA256,
        "current coverage records differ from the approved IUM10 source",
    )

    handoff_entries = (
        remediation_payload.get("entries")
        if isinstance(remediation_payload, dict)
        else None
    )
    _require(isinstance(handoff_entries, list), "remediation payload must contain entries")
    _require(
        all(
            isinstance(entry, dict)
            and isinstance(entry.get("competencyId"), str)
            and entry["competencyId"].strip()
            for entry in handoff_entries
        ),
        "handoff records must have string competency ids",
    )
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
        "moduleStructureSha256": BASELINE_MODULE_STRUCTURE_SHA256,
        "coverageProjectionSha256": BASELINE_COVERAGE_PROJECTION_SHA256,
        "timeHandoffSha256": BASELINE_TIME_HANDOFF_SHA256,
    }


def _validate_time_model_baseline(
    stored_baseline,
    module_payload,
    coverage_payload,
    remediation_payload,
):
    _require(
        isinstance(stored_baseline, dict)
        and set(stored_baseline) == TIME_MODEL_BASELINE_FIELDS,
        "time model baseline fields differ from the immutable contract",
    )
    computed = {
        "moduleStructureSha256": module_structure_fingerprint(module_payload),
        "coverageProjectionSha256": coverage_projection_fingerprint(
            coverage_payload,
            remediation_payload,
        ),
        "timeHandoffSha256": time_handoff_fingerprint(remediation_payload),
    }
    expected = {
        "commit": IUM10_BASELINE_COMMIT,
        "moduleStructureSha256": BASELINE_MODULE_STRUCTURE_SHA256,
        "coverageProjectionSha256": BASELINE_COVERAGE_PROJECTION_SHA256,
        "timeHandoffSha256": BASELINE_TIME_HANDOFF_SHA256,
    }
    _require(
        all(
            isinstance(stored_baseline[field], str)
            and stored_baseline[field] == expected[field]
            for field in TIME_MODEL_BASELINE_FIELDS
        ),
        "stored time model baseline differs from authoritative constants",
    )
    _require(
        all(
            stored_baseline[field] == computed[field]
            for field in computed
        ),
        "stored time model fingerprints differ from the current baseline artifacts",
    )


@_validation_boundary("IUM10 validation")
def validate_ium10(
    time_payload,
    module_payload,
    coverage_payload,
    remediation_payload,
):
    """Validate the complete IUM10 chain and return indexed contracts."""
    _require(
        isinstance(time_payload, dict) and set(time_payload) == TIME_MODEL_FIELDS,
        "time model top-level fields differ from the IUM10 contract",
    )
    _require(
        time_payload.get("status") == "working"
        and isinstance(time_payload.get("status"), str),
        "complete IUM10 time model status must be working",
    )
    baseline = validate_ium10_baseline(
        module_payload,
        coverage_payload,
        remediation_payload,
    )
    _validate_time_model_baseline(
        time_payload["baseline"],
        module_payload,
        coverage_payload,
        remediation_payload,
    )
    _require(
        isinstance(time_payload.get("schemaVersion"), int)
        and not isinstance(time_payload["schemaVersion"], bool)
        and time_payload["schemaVersion"] == 3,
        "schema version must be the integer 3",
    )
    capacity_paths = validate_capacity_model(
        time_payload["capacityModel"],
        time_payload["unit"],
    )
    module_contracts = validate_module_contracts(
        time_payload["moduleContracts"],
        module_payload,
    )
    integration_contracts = validate_integration_contracts(
        time_payload["integrationContracts"],
        module_contracts,
    )
    annual_variants = validate_annual_variants(
        time_payload["annualVariants"],
        module_contracts,
        integration_contracts,
    )
    availability_contracts = validate_availability_contracts(
        time_payload["availabilityContracts"],
        annual_variants,
        integration_contracts,
    )
    _validate_grade_6_judgement(
        time_payload,
        module_contracts,
        integration_contracts,
        annual_variants,
    )
    _validate_grade_7_judgement(
        time_payload,
        module_contracts,
        integration_contracts,
        annual_variants,
        availability_contracts,
    )
    privacy_contracts = validate_privacy_contracts(
        time_payload["privacyContracts"],
        module_contracts,
    )
    time_reviews = validate_time_reviews(
        time_payload["timeReviews"],
        remediation_payload,
        module_contracts,
        integration_contracts,
        annual_variants,
        require_complete=True,
        privacy_contracts=privacy_contracts,
    )
    sequence_evidence = validate_sequence_evidence(
        time_payload["sequenceEvidence"],
        time_reviews,
        annual_variants,
        coverage_payload,
    )
    risks = validate_risks(time_payload["risks"])
    pilot_assignments = validate_pilot_assignments(
        time_payload["pilotAssignments"],
        module_contracts,
        integration_contracts,
        annual_variants,
        availability_contracts,
    )
    grade_judgements = _validate_final_grade_judgements(
        time_payload["gradeJudgements"],
        sequence_evidence,
        annual_variants,
        coverage_payload,
        time_reviews,
        module_contracts,
        availability_contracts,
        pilot_assignments,
    )
    result = {
        "baseline": baseline,
        "capacityPaths": capacity_paths,
        "moduleContracts": module_contracts,
        "integrationContracts": integration_contracts,
        "annualVariants": annual_variants,
        "availabilityContracts": availability_contracts,
        "privacyContracts": privacy_contracts,
        "timeReviews": time_reviews,
        "sequenceEvidence": sequence_evidence,
        "gradeJudgements": grade_judgements,
        "risks": risks,
        "pilotAssignments": pilot_assignments,
    }
    result["timeReferences"] = validate_time_references(
        module_payload,
        coverage_payload,
        remediation_payload,
        result,
    )
    result["ium09CoverageProjection"] = ium09_coverage_projection(
        coverage_payload,
        remediation_payload,
        time_payload["sequenceEvidence"],
    )
    return result


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

    return validate_ium10(
        time_model,
        module_payload,
        coverage_payload,
        remediation_payload,
    )


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
        f"{len(result['moduleContracts'])} module contracts, "
        f"{len(result['timeReviews'])} time reviews, and "
        f"{len(result['sequenceEvidence'])} sequence records"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
