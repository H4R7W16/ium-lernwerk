from __future__ import annotations

import json
import hashlib
import re
from datetime import date as calendar_date
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse


CONTROL_FILES = (
    Path("roadmap/v2/status.json"),
    Path("roadmap/v2/archive/v1-baseline.json"),
    Path("roadmap/v2/requirements/requirements.json"),
    Path("roadmap/v2/foundations/curriculum/status.json"),
    Path("roadmap/v2/foundations/curriculum/source-basis.json"),
    Path("roadmap/v2/foundations/curriculum/gap-assessments.json"),
    Path("roadmap/v2/foundations/sources/status.json"),
    Path("roadmap/v2/foundations/sources/inventory.json"),
    Path("roadmap/v2/foundations/sources/traceability.json"),
    Path("roadmap/v2/foundations/sources/link-audit.json"),
    Path("roadmap/v2/foundations/sources/source-register.json"),
    Path("schemas/v2/source-inventory.schema.json"),
    Path("schemas/v2/source-traceability.schema.json"),
    Path("schemas/v2/source-link-audit.schema.json"),
    Path("roadmap/v2/foundations/learning-experience/legacy-audit.json"),
    Path("roadmap/v2/foundations/learning-experience/legacy-audit.md"),
    Path("schemas/v2/legacy-learning-audit.schema.json"),
    Path("roadmap/v2/foundations/learning-experience/evidence-register.json"),
    Path("roadmap/v2/foundations/learning-experience/evidence-synthesis.md"),
    Path("schemas/v2/learning-evidence.schema.json"),
    Path("roadmap/v2/foundations/learning-experience/learner-profile.json"),
    Path("roadmap/v2/foundations/learning-experience/learner-profile.md"),
    Path("schemas/v2/learner-profile.schema.json"),
    Path("roadmap/v2/foundations/learning-experience/learning-architecture.json"),
    Path("roadmap/v2/foundations/learning-experience/learning-architecture.md"),
    Path("schemas/v2/learning-design.schema.json"),
    Path("roadmap/v2/foundations/learning-experience/material-patterns.json"),
    Path("roadmap/v2/foundations/learning-experience/material-experience-guide.md"),
    Path("schemas/v2/material-patterns.schema.json"),
    Path("roadmap/v2/foundations/learning-experience/experience-gates.json"),
    Path("roadmap/v2/foundations/learning-experience/teacher-orchestration.md"),
    Path("roadmap/v2/foundations/learning-experience/review-form.md"),
    Path("schemas/v2/experience-gates.schema.json"),
)

EXPERIENCE_GATE_IDS = {
    "evidence-integrity", "goal-action-evidence-alignment", "cognitive-economy",
    "disciplinary-learning-action", "representation-coherence",
    "support-without-task-removal", "feedback-and-next-action",
    "orientation-and-recovery", "accessibility-and-equivalence",
    "teacher-orchestration", "privacy-and-emotional-safety", "pilot-boundary",
}
EXPERIENCE_OWNER_ROLES = {
    "source-reviewer", "subject-didactics-reviewer", "accessibility-reviewer",
    "teacher-reviewer", "privacy-reviewer", "integration-reviewer",
}
EXPERIENCE_SCOPE = {
    "grades": [5, 6, 7], "schoolType": "Gymnasium Baden-Württemberg", "level": "E",
    "maturity": "working", "contentProduction": "frozen", "productBinding": "product-neutral",
}
EXPERIENCE_REVIEW_BOUNDARY = {
    "definitionStatus": "working", "executionStatus": "not-run",
    "pilot": "not-started", "standardAllowed": False,
    "learningEffectClaimAllowed": False, "personalTelemetryAllowed": False,
}
EXPERIENCE_STATUS_EFFECT = {
    "onPass": "eligible-for-lxf07-review", "onFail": "block-foundation-review",
    "pilot": "not-started", "standardAllowed": False,
}
EXPERIENCE_GATE_SCHEMA_SHA256 = "579921A48DE0307FF970B5407FAA44B402DEB4D34DF7785195C821CE0DA5C0CE"

FULL_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
EXPECTED_REPOSITORY = "H4R7W16/ium-lernwerk"
EXPECTED_REMOTE = "https://github.com/H4R7W16/ium-lernwerk.git"
EXPECTED_MAIN_COMMIT = "dcaff3e4b6e96d8c1da3dd1d4dd56f6df6b35ef0"
EXPECTED_LXP05_REF = {
    "ref": "origin/feat/lxp05-ium5-experience",
    "commit": "645a1d4ea3c786b08e1320954b522edf86dc9f83",
    "role": "historical-unmerged-review-candidate",
}
UNVERIFIED_DASHBOARD_COMMIT = "07bc15e1e70d"
EXPECTED_STATEMENT_BOUNDARIES = (
    "V1-Artefakte sind Auditbestand und keine automatisch übernommenen V2-Standards.",
    "Technische Verifikation belegt weder didaktische Qualität noch Lernwirksamkeit.",
    "LXP05 bleibt ungemergt, eingefroren und außerhalb der wiederverwendbaren V2-Basis.",
    "Pilotierung, Veröffentlichung und Cutover sind nicht freigegeben.",
)
REQUIREMENT_DOMAINS = {
    "curriculum",
    "didactics",
    "sources",
    "platform",
    "privacy",
    "governance",
    "public-perception",
    "experience",
}
REQUIREMENT_BINDINGS = {
    "official",
    "project",
    "orientation",
    "candidate",
    "optional",
}
REQUIREMENT_SCOPES = {
    "module",
    "cross-cutting",
    "year",
    "cross-grade",
    "system",
}
REQUIREMENT_GRADES = {5, 6, 7}
FULFILLMENT_MODES = {"direct-module", "integrated", "cross-cutting"}
REQUIREMENT_COVERAGE = {
    "unassessed",
    "uncovered",
    "partial",
    "covered",
    "not-applicable",
}
EVIDENCE_KINDS = {"repo", "git", "vault", "url", "doi"}
REQUIREMENTS_TOP_LEVEL_FIELDS = {
    "schemaVersion",
    "projectId",
    "asOf",
    "requirements",
}
REQUIREMENT_FIELDS = {
    "id",
    "title",
    "statement",
    "domain",
    "origin",
    "binding",
    "scope",
    "grades",
    "fulfillmentModes",
    "coverage",
    "evidence",
    "dependencies",
    "risks",
    "gate",
}
EVIDENCE_FIELDS = {"kind", "target", "label", "required"}
REQUIREMENT_ID_PATTERN = re.compile(r"^V2-REQ-[A-Z0-9-]+$")
CURRICULUM_SOURCE_EXPECTATIONS = {
    "SRC-CUR-BMB-2016": {
        "title": "Gymnasium – Basiskurs Medienbildung (Bildungsplan 2016)",
        "binding": "official",
        "normativeStatus": "enacted",
        "repositoryPath": "curriculum/basiskurs-medienbildung/competencies.json",
        "datasetSha256": "2C39832CD6EE373C643994C69DB6F4411539669923704E6C0F45EF63C2112518",
        "sourceAssetSha256": "84609F1CAF3BDB5D3CFDD0BD6287C348F773F6BD5A2DD40F95D9711B1F338536",
        "recordCount": 59,
        "grades": [5],
        "directUrl": "https://www.bildungsplaene-bw.de/%2CLde/LS/BP2016BW/ALLG/GYM/BMB",
        "contentIdentity": "not-byte-compared",
    },
    "SRC-CUR-INF7-2016": {
        "title": "Gymnasium – Aufbaukurs Informatik (Klasse 7), Bildungsplan 2016",
        "binding": "official",
        "normativeStatus": "enacted",
        "repositoryPath": "curriculum/aufbaukurs-informatik/competencies.json",
        "datasetSha256": "DDE81984622A275C9FFEEDC8B601468F22021F19028DE6B162134C4050DBF0C5",
        "sourceAssetSha256": "57A535001B7371D949C761473DA72E05FB99AA01105B7C59AE34BF7DC47F20A9",
        "recordCount": 94,
        "grades": [7],
        "directUrl": "https://www.bildungsplaene-bw.de/%2CLde/LS/BP2016BW/ALLG/GYM/INF7",
        "contentIdentity": "not-byte-compared",
    },
    "SRC-CUR-LESEHILFE-2026-27": {
        "title": (
            "Lesehilfe Informatik und Medienbildung für die Klassen 5 bis 7 "
            "im Schuljahr 2026/2027"
        ),
        "binding": "orientation",
        "normativeStatus": "orientation",
        "repositoryPath": "curriculum/lesehilfe-2026-27/competencies.json",
        "datasetSha256": "4EAF2AB20BDD508D18B821B4D953EFDF6A6B7CAEA05EF8D904C101B3C4E342C8",
        "sourceAssetSha256": "1BC94255AD35D75782B819C1CA425D7C1F21CEDC6B2012378EC828BAC1451008",
        "recordCount": 125,
        "grades": [5, 6, 7],
        "directUrl": "https://km.baden-wuerttemberg.de/fileadmin/redaktion/m-km/intern/PDF/Dateien/Schulart%C3%BCbergreifend/MINT/2026_Lesehilfe_IuM_Gym_und_Sek_I_bf.pdf",
        "contentIdentity": "sha256-match",
    },
}
EXPECTED_CURRICULUM_GAPS = {
    "BMB16-GYM-IK-GM-003": {
        "sourceId": "SRC-CUR-BMB-2016",
        "sourceBinding": "official",
        "sourceDatasetPath": "curriculum/basiskurs-medienbildung/competencies.json",
        "normativeWeight": "enacted",
        "moduleIds": ["IUM-5-CORE-01"],
        "timeReviewId": "TR-BMB16-GYM-IK-GM-003",
        "proposedFulfillmentMode": "cross-cutting",
        "decisionState": "approved-direction",
    },
    "BMB16-GYM-PK-RK-003": {
        "sourceId": "SRC-CUR-BMB-2016",
        "sourceBinding": "official",
        "sourceDatasetPath": "curriculum/basiskurs-medienbildung/competencies.json",
        "normativeWeight": "enacted",
        "moduleIds": ["IUM-5-CORE-07"],
        "timeReviewId": "TR-BMB16-GYM-PK-RK-003",
        "proposedFulfillmentMode": "direct-module",
        "decisionState": "open",
    },
    "LH26-E-DP-003": {
        "sourceId": "SRC-CUR-LESEHILFE-2026-27",
        "sourceBinding": "orientation",
        "sourceDatasetPath": "curriculum/lesehilfe-2026-27/competencies.json",
        "normativeWeight": "orientation",
        "moduleIds": ["IUM-5-CORE-07"],
        "timeReviewId": "TR-LH26-E-DP-003",
        "proposedFulfillmentMode": "direct-module",
        "decisionState": "open",
    },
    "LH26-E-PROG-003": {
        "sourceId": "SRC-CUR-LESEHILFE-2026-27",
        "sourceBinding": "orientation",
        "sourceDatasetPath": "curriculum/lesehilfe-2026-27/competencies.json",
        "normativeWeight": "orientation",
        "moduleIds": ["IUM-7-CORE-08"],
        "timeReviewId": "TR-LH26-E-PROG-003",
        "proposedFulfillmentMode": "integrated",
        "decisionState": "open",
    },
    "LH26-E-PROG-004": {
        "sourceId": "SRC-CUR-LESEHILFE-2026-27",
        "sourceBinding": "orientation",
        "sourceDatasetPath": "curriculum/lesehilfe-2026-27/competencies.json",
        "normativeWeight": "orientation",
        "moduleIds": ["IUM-7-CORE-08"],
        "timeReviewId": "TR-LH26-E-PROG-004",
        "proposedFulfillmentMode": "integrated",
        "decisionState": "open",
    },
}
PHASE0_SOURCE_BASELINE_EXPECTATIONS = {
    "sourceRegister": {
        "path": "docs/research/phase-0/source-register.json",
        "sha256": "F4B52FB6B8B5C7E31FF3BA73DA63B9D4E46F47B55FC51DFEDAE3F809100D6AB1",
        "recordCount": 63,
        "collection": "sources",
    },
    "claimLedger": {
        "path": "docs/research/phase-0/claim-ledger.json",
        "sha256": "5D6D5518FD9896FF052F51E06C52B0758EC031AF7B27E0919498BA5D9982728C",
        "recordCount": 51,
        "collection": "claims",
    },
    "principleLedger": {
        "path": "docs/research/phase-0/design-principles.json",
        "sha256": "4F577237E1CC9386DB87D37F7291D1E0C08ACF87C7ED5C85A48E2A6162C87B7B",
        "recordCount": 15,
        "collection": "principles",
    },
}
EXPECTED_LXP01_SOURCES = {
    "SRC-LXP-SDT-2024": {
        "legacyId": "LXP-SRC-SDT-2024",
        "doi": "10.1016/j.lmot.2024.102015",
        "url": "https://doi.org/10.1016/j.lmot.2024.102015",
        "verificationStatus": "metadata-checked",
        "licenseStatus": "publisher-rights-no-open-license",
        "usageStatus": "citation-only",
    },
    "SRC-LXP-SEGMENT-2019": {
        "legacyId": "LXP-SRC-SEGMENT-2019",
        "doi": "10.1007/s10648-018-9456-4",
        "url": "https://doi.org/10.1007/s10648-018-9456-4",
        "verificationStatus": "metadata-checked",
        "licenseStatus": "publisher-rights-no-open-license",
        "usageStatus": "citation-only",
    },
    "SRC-LXP-SIGNAL-2016": {
        "legacyId": "LXP-SRC-SIGNAL-2016",
        "doi": "10.1016/j.edurev.2015.12.003",
        "url": "https://doi.org/10.1016/j.edurev.2015.12.003",
        "verificationStatus": "metadata-checked",
        "licenseStatus": "publisher-rights-no-open-license",
        "usageStatus": "citation-only",
    },
    "SRC-LXP-W3C-COGA-2021": {
        "legacyId": "LXP-SRC-W3C-COGA-2021",
        "doi": None,
        "url": "https://www.w3.org/WAI/WCAG2/supplemental/",
        "verificationStatus": "primary-checked",
        "licenseStatus": "permissive-with-notice",
        "usageStatus": "reuse-with-notice",
    },
    "SRC-LXP-UDL30-2024": {
        "legacyId": "LXP-SRC-UDL30-2024",
        "doi": None,
        "url": "https://udlguidelines.cast.org/",
        "verificationStatus": "primary-checked",
        "licenseStatus": "no-open-license-identified",
        "usageStatus": "citation-and-link-only",
    },
    "SRC-LXP-COS-2023": {
        "legacyId": "LXP-SRC-COS-2023",
        "doi": "10.1016/j.compedu.2023.104864",
        "url": "https://doi.org/10.1016/j.compedu.2023.104864",
        "verificationStatus": "metadata-checked",
        "licenseStatus": "publisher-rights-no-open-license",
        "usageStatus": "citation-only",
    },
}
SOURCE_INVENTORY_FIELDS = {
    "schemaVersion",
    "projectId",
    "asOf",
    "phase0Baseline",
    "locatorOverrides",
    "lxp01Additions",
    "totals",
}
LXP01_SOURCE_FIELDS = {
    "legacyId",
    "sourceId",
    "title",
    "authors",
    "year",
    "sourceKind",
    "url",
    "doi",
    "verificationStatus",
    "licenseStatus",
    "usageStatus",
    "accessed",
    "liveCheck",
    "migrationState",
    "claimMigration",
    "recheckTriggers",
}
EXPECTED_SOURCE_ENTITY_FLOW = [
    "source",
    "claim",
    "project-decision",
    "design-principle",
    "material-pattern",
    "verification-evidence",
]
EXPECTED_SOURCE_ENTITY_TYPES = [
    {
        "id": "source",
        "definition": "Externe oder lokale Fundstelle mit Identität, Prüf-, Lizenz- und Aktualitätsstatus.",
        "mayReference": [],
    },
    {
        "id": "claim",
        "definition": "Prüfbare Aussage mit Geltungsbereich, Grenzen und mindestens einer registrierten Quelle.",
        "mayReference": ["source"],
    },
    {
        "id": "project-decision",
        "definition": "Bewusste Projektfestlegung, die Claims bewertet, aber selbst kein Forschungsbefund ist.",
        "mayReference": ["claim"],
    },
    {
        "id": "design-principle",
        "definition": "Aus Claims und Projektentscheidungen abgeleitete, überprüfbare Gestaltungsregel.",
        "mayReference": ["claim", "project-decision"],
    },
    {
        "id": "material-pattern",
        "definition": "Konkretes wiederverwendbares Material- oder Interaktionsmuster zur Umsetzung eines Prinzips.",
        "mayReference": ["claim", "design-principle"],
    },
    {
        "id": "verification-evidence",
        "definition": "Datierter Prüfnachweis für Entscheidung, Prinzip oder Materialmuster ohne eigene Wirksamkeitsbehauptung.",
        "mayReference": ["project-decision", "design-principle", "material-pattern"],
    },
]
EXPECTED_SOURCE_MIGRATION_RULES = {
    "releaseRelevantStatementsRequireClaimIds": True,
    "claimsRequireRegisteredSourceIds": True,
    "claimsRequirePrimaryCheckedSources": True,
    "lxp01AdditionsCreateClaims": False,
    "pendingLxp01ClaimReview": None,
}
SOURCE_TRACEABILITY_FIELDS = {
    "schemaVersion",
    "projectId",
    "asOf",
    "entityFlow",
    "entityTypes",
    "sourceInventoryPath",
    "claimBaseline",
    "migrationRules",
    "requiredGaps",
    "optionalGaps",
}
SOURCE_GAP_FIELDS = {
    "id",
    "sourceId",
    "required",
    "issue",
    "resolutionStatus",
    "ownerGate",
    "acceptanceCriterion",
}
SOURCE_LINK_AUDIT_FIELDS = {
    "schemaVersion",
    "projectId",
    "generatedAt",
    "inventoryPath",
    "policy",
    "summary",
    "checks",
}
LEGACY_LEARNING_AUDIT_FIELDS = {
    "schemaVersion",
    "projectId",
    "asOf",
    "requirementIds",
    "records",
    "knownGaps",
    "lxp05FailureLayers",
    "handoff",
}
LEGACY_AUDIT_RECORD_FIELDS = {
    "artifactId",
    "artifactKind",
    "artifactRef",
    "decision",
    "rationale",
    "requirementIds",
    "evidence",
    "successorTaskId",
}
LEGACY_AUDIT_GAP_FIELDS = {
    "id",
    "category",
    "status",
    "finding",
    "consequence",
    "evidence",
}
LEGACY_AUDIT_FAILURE_LAYER_FIELDS = {
    "layer",
    "finding",
    "disposition",
    "evidence",
}
LEGACY_AUDIT_HANDOFF_FIELDS = {
    "nextTaskId",
    "contentProduction",
    "lxp05",
    "decisionBoundary",
}
EXPECTED_LP_CLAIMS = {f"CLAIM-LP-{number:03d}" for number in range(1, 14)}
EXPECTED_PRINCIPLES = {f"PRIN-{number:03d}" for number in range(1, 16)}
EXPECTED_LXP_SPECS = {"LXP01", "LXP02", "LXP03", "LXP04"}
EXPECTED_LEGACY_ARTIFACTS = (
    EXPECTED_LP_CLAIMS
    | EXPECTED_PRINCIPLES
    | EXPECTED_LXP_SPECS
    | {"FACH-IUM-5-7"}
)
LEGACY_DECISIONS = {"retain", "adapt", "replace", "reference-only", "drop"}
EXPECTED_LEGACY_GAPS = {
    "GAP-LXF01-SOURCE",
    "GAP-LXF01-PRINCIPLE-CONTRACT",
    "GAP-LXF01-QUALITY-CONFLATION",
    "GAP-LXF01-LXP04-SPECIFICITY",
    "GAP-LXF01-LEARNER-ASSUMPTIONS",
}
EXPECTED_LXP05_FAILURE_LAYERS = {
    "evidence",
    "translation",
    "implementation",
    "pilot",
}
V2_SOURCE_REGISTER_FIELDS = {"schemaVersion", "projectId", "asOf", "sources"}
V2_SOURCE_FIELDS = {
    "id",
    "title",
    "authors",
    "year",
    "sourceKind",
    "url",
    "doi",
    "accessed",
    "verificationStatus",
    "licenseStatus",
    "usageStatus",
    "relevance",
    "updateRisk",
}
V2_SOURCE_KINDS = {
    "meta-analysis",
    "research-synthesis",
    "theory-review",
    "theory-framework",
    "professional-guidance",
    "professional-standard",
}
V2_SOURCE_VERIFICATION_STATUSES = {"metadata-checked", "primary-checked"}
V2_SOURCE_UPDATE_RISKS = {"low", "medium", "high"}
EXPECTED_LXF02_ADDITIONAL_SOURCE_METADATA = {
    "SRC-V2-LXF-SDT-2024": {
        "doi": "10.1016/j.lmot.2024.102015",
        "url": "https://doi.org/10.1016/j.lmot.2024.102015",
        "sourceKind": "meta-analysis",
    },
    "SRC-V2-LXF-SEGMENT-2019": {
        "doi": "10.1007/s10648-018-9456-4",
        "url": "https://doi.org/10.1007/s10648-018-9456-4",
        "sourceKind": "meta-analysis",
    },
    "SRC-V2-LXF-SIGNAL-2016": {
        "doi": "10.1016/j.edurev.2015.12.003",
        "url": "https://doi.org/10.1016/j.edurev.2015.12.003",
        "sourceKind": "meta-analysis",
    },
    "SRC-V2-LXF-W3C-COGA-2021": {
        "doi": None,
        "url": "https://www.w3.org/WAI/WCAG2/supplemental/",
        "sourceKind": "professional-guidance",
    },
    "SRC-V2-LXF-UDL30-2024": {
        "doi": None,
        "url": "https://udlguidelines.cast.org/",
        "sourceKind": "professional-guidance",
    },
    "SRC-V2-LXF-COS-2023": {
        "doi": "10.1016/j.compedu.2023.104864",
        "url": "https://doi.org/10.1016/j.compedu.2023.104864",
        "sourceKind": "meta-analysis",
    },
    "SRC-V2-LXF-MAYER-2024": {
        "doi": "10.1007/s10648-023-09842-1",
        "url": "https://doi.org/10.1007/s10648-023-09842-1",
        "sourceKind": "theory-review",
    },
    "SRC-V2-LXF-ICAP-2014": {
        "doi": "10.1080/00461520.2014.965823",
        "url": "https://doi.org/10.1080/00461520.2014.965823",
        "sourceKind": "theory-framework",
    },
    "SRC-V2-LXF-EEF-META-2025": {
        "doi": None,
        "url": "https://educationendowmentfoundation.org.uk/education-evidence/guidance-reports/metacognition",
        "sourceKind": "professional-guidance",
    },
    "SRC-V2-LXF-WCAG22-2024": {
        "doi": None,
        "url": "https://www.w3.org/TR/wcag/",
        "sourceKind": "professional-standard",
    },
}
EXPECTED_LXF02_SOURCE_IDS = {
    "SRC-LP-IBBW-WU",
    "SRC-LP-PRIOR-2022",
    "SRC-LP-CLT-2020",
    "SRC-LP-WORKED-2023",
    "SRC-LP-SELFEXPLAIN-2018",
    "SRC-LP-SCAFFOLD-2017",
    "SRC-LP-QUIZZING-2021",
    "SRC-LP-SPACING-2025",
    "SRC-LP-TRANSFER-2018",
    "SRC-LP-FEEDBACK-2020",
    "SRC-LP-AUTONOMY-2025",
    "SRC-LP-PF-2021",
    "SRC-LP-SRL-2008",
    *EXPECTED_LXF02_ADDITIONAL_SOURCE_METADATA,
}
LEARNING_EVIDENCE_REGISTER_FIELDS = {"schemaVersion", "asOf", "claims"}
LEARNING_EVIDENCE_CLAIM_FIELDS = {
    "id",
    "statement",
    "mechanism",
    "scope",
    "learnerContext",
    "boundaryConditions",
    "sourceIds",
    "evidenceLevel",
    "status",
}
LEARNING_EVIDENCE_LEVELS = {"low", "medium", "high", "normative"}
LEARNING_EVIDENCE_STATUSES = {"draft", "working", "reviewed", "standard"}
PROFESSIONAL_SOURCE_KINDS = {"professional-guidance", "professional-standard"}
LEARNER_PROFILE_FIELDS = {
    "schemaVersion",
    "projectId",
    "asOf",
    "scope",
    "dimensions",
}
LEARNER_PROFILE_SCOPE_FIELDS = {
    "profileType",
    "grades",
    "schoolType",
    "level",
    "individualDiagnosis",
    "maturity",
    "statementBoundaries",
}
LEARNER_PROFILE_DIMENSION_FIELDS = {
    "id",
    "label",
    "evidenceSupportedAssumptions",
    "curriculumAndProjectExpectations",
    "openAgeSpecificQuestions",
    "pilotQuestions",
}
LEARNER_PROFILE_STATEMENT_FIELDS = {
    "id",
    "statement",
    "claimIds",
    "grades",
    "variability",
    "designConsequence",
    "status",
    "limitations",
}
LEARNER_PROFILE_CONSEQUENCE_FIELDS = {
    "learnerMaterial",
    "teacherOrchestration",
}
LEARNER_PROFILE_EXPECTATION_FIELDS = {
    "id",
    "basis",
    "statement",
    "grades",
    "referenceIds",
    "limitations",
}
LEARNER_PROFILE_QUESTION_FIELDS = {
    "id",
    "question",
    "grades",
    "decisionOwner",
    "implications",
}
LEARNER_PROFILE_PILOT_FIELDS = {
    "id",
    "question",
    "grades",
    "evidenceNeeded",
    "privacyBoundary",
}
LEARNER_PROFILE_DIMENSION_ORDER = (
    "prior-knowledge-and-conceptions",
    "reading-and-disciplinary-language",
    "attention-and-working-memory-load",
    "digital-operation-routines",
    "self-regulation-and-help-use",
    "motivation-and-perceived-purpose",
    "access-barriers-and-expression",
    "classroom-collaboration-and-orchestration",
)
EXPECTED_LEARNER_PROFILE_DIMENSIONS = set(LEARNER_PROFILE_DIMENSION_ORDER)
LEARNER_PROFILE_STATUSES = {"draft", "working", "reviewed", "standard"}
LEARNER_PROFILE_EXPECTATION_BASES = {
    "official-curriculum",
    "orientation",
    "project-decision",
}
LEARNER_PROFILE_DECISION_OWNER_PATTERN = re.compile(
    r"^(?:LXF0[4-7]|IUM-V2-R[5-7])$"
)
LEARNER_PROFILE_REFERENCE_PATTERN = re.compile(
    r"\b(?:CLAIM-[A-Z0-9-]+|BMB16-[A-Z0-9-]+|LH26-[A-Z0-9-]+|"
    r"INF7-16-[A-Z0-9-]+|V2-REQ-[A-Z0-9-]+)\b"
)
LEARNER_PROFILE_BEHAVIORAL_BOUNDARY = (
    "Einzelantworten, Klicks, Bearbeitungszeiten und Hilfenutzung werden nicht zu "
    "stabilen Personenmerkmalen oder Defizitlabels verdichtet."
)
LEARNER_PROFILE_HELP_USE_LABEL = "Selbstregulation und Hilfenutzung"
LEARNER_PROFILE_SCHEMA_SHA256 = (
    "7482F51AA45E11FC1AC8C487B0C2D15D18C1162EDD1ECA02F04479178FE1264A"
)
LEARNING_ARCHITECTURE_FIELDS = {
    "schemaVersion",
    "projectId",
    "asOf",
    "scope",
    "principleGroups",
    "learningFunctionGrammar",
    "taskTypes",
    "practiceTransferStages",
    "instructionModes",
}
LEARNING_ARCHITECTURE_SCOPE_FIELDS = {
    "grades",
    "schoolType",
    "level",
    "maturity",
    "contentProduction",
}
LEARNING_ARCHITECTURE_GROUP_FIELDS = {"id", "label", "principles"}
LEARNING_ARCHITECTURE_PRINCIPLE_FIELDS = {
    "id",
    "title",
    "decision",
    "claimIds",
    "decisionBasis",
    "obligation",
    "appliesTo",
    "positivePatterns",
    "antiPatterns",
    "observableCriteria",
    "verificationMethods",
    "status",
}
LEARNING_ARCHITECTURE_GROUP_ORDER = (
    "goal-and-purpose",
    "prior-knowledge-and-cognitive-load",
    "disciplinary-learning-action",
    "explanation-and-representation",
    "task-and-support",
    "feedback-practice-and-transfer",
    "orientation-and-access",
    "teacher-orchestration",
)
EXPECTED_LEARNING_ARCHITECTURE_GROUPS = set(LEARNING_ARCHITECTURE_GROUP_ORDER)
LEARNING_FUNCTION_ORDER = (
    "orient",
    "surface-prior-knowledge",
    "open-disciplinary-problem",
    "explain-or-model",
    "guided-action",
    "independent-application",
    "use-feedback",
    "secure-and-transfer",
)
EXPECTED_LEARNING_FUNCTIONS = set(LEARNING_FUNCTION_ORDER)
LEARNING_FUNCTION_GRAMMAR_FIELDS = {
    "universalOrder",
    "functions",
    "transitions",
    "sequenceVariants",
    "digitalInteractions",
}
LEARNING_FUNCTION_FIELDS = {
    "id",
    "label",
    "purpose",
    "observableOutput",
    "teacherRole",
    "boundaries",
}
LEARNING_TRANSITION_FIELDS = {
    "id",
    "from",
    "to",
    "pedagogicalRationale",
    "conditions",
}
LEARNING_SEQUENCE_VARIANT_FIELDS = {
    "id",
    "label",
    "transitionIds",
    "rationale",
    "conditions",
}
LEARNING_DIGITAL_INTERACTION_FIELDS = {
    "id",
    "label",
    "learningFunctionId",
    "purpose",
    "forbiddenUses",
    "observableCriteria",
    "verificationMethods",
}
LEARNING_TASK_TYPE_FIELDS = {
    "id",
    "purpose",
    "evidenceUse",
    "feedbackTiming",
    "boundaries",
}
LEARNING_PRACTICE_STAGE_FIELDS = {
    "id",
    "definition",
    "temporalPosition",
    "observableEvidence",
    "boundaries",
}
LEARNING_INSTRUCTION_MODE_FIELDS = {
    "id",
    "claimIds",
    "useWhen",
    "avoidWhen",
    "requiredBefore",
    "requiredAfter",
}
LEARNING_ARCHITECTURE_OBLIGATIONS = {
    "required",
    "conditional",
    "recommended",
    "avoid",
}
LEARNING_ARCHITECTURE_APPLIES_TO = {
    "learner-material",
    "learning-sequence",
    "task",
    "explanation",
    "digital-interaction",
    "assessment",
    "accessibility",
    "teacher-orchestration",
}
LEARNING_ARCHITECTURE_VERIFICATION_METHODS = {
    "source-review",
    "expert-review",
    "content-walkthrough",
    "automated-check",
    "accessibility-audit",
    "usability-test",
    "classroom-pilot",
}
LEARNING_ARCHITECTURE_STATUSES = {"draft", "working", "reviewed"}
EXPECTED_LEARNING_TASK_TYPES = {"learning-task", "performance-task"}
EXPECTED_LEARNING_PRACTICE_STAGES = {
    "immediate-application",
    "delayed-retrieval",
    "transfer",
}
EXPECTED_LEARNING_INSTRUCTION_MODES = {
    "supported-exploration",
    "explicit-explanation",
}
LEARNING_DESIGN_SCHEMA_SHA256 = (
    "28A985C02380CE0F4FE0163B5D99EDDEE3874E71ED07A884082BE8B543BA9CF6"
)
LEARNING_ARCHITECTURE_REFERENCE_PATTERN = re.compile(
    r"\b(?:V2-REQ-[A-Z0-9-]+|LXF03-S-[0-9]{3}|LXF03-E-[0-9]{3})\b"
)
MATERIAL_PATTERN_FIELDS = {
    "schemaVersion",
    "projectId",
    "asOf",
    "scope",
    "policies",
    "patterns",
    "walkthroughs",
}
MATERIAL_PATTERN_SCOPE_FIELDS = {
    "grades",
    "schoolType",
    "level",
    "maturity",
    "contentProduction",
    "productBinding",
}
MATERIAL_PATTERN_POLICY_FIELDS = {
    "universalPageTemplate",
    "universalElementLimit",
    "universalMinuteLimit",
    "decorativeGamificationDefault",
    "productComponentsAllowed",
    "learnerFacingContentAllowed",
}
MATERIAL_PATTERN_RECORD_FIELDS = {
    "id",
    "family",
    "title",
    "learnerPurpose",
    "teacherPurpose",
    "learningFunctionIds",
    "principleIds",
    "applicability",
    "requiredElements",
    "forbiddenElements",
    "observableChecks",
    "verificationMethods",
    "accessibilityConsiderations",
    "productDependencies",
    "quantifiedRules",
    "status",
}
MATERIAL_PATTERN_APPLICABILITY_FIELDS = {"useWhen", "doNotUseWhen"}
MATERIAL_PATTERN_QUANTIFIED_RULE_FIELDS = {"statement", "claimIds", "scope"}
MATERIAL_PATTERN_WALKTHROUGH_FIELDS = {
    "id",
    "label",
    "patternIds",
    "learnerQuestion",
    "requiredInformation",
    "action",
    "feedback",
    "teacherRole",
    "barrier",
    "verificationMethod",
}
MATERIAL_PATTERN_FAMILY_ORDER = (
    "entry-and-orientation",
    "worked-example-with-active-processing",
    "linked-representations-and-signaling",
    "prediction-execution-comparison",
    "guided-practice-and-help",
    "feedback-and-revision",
    "retrieval-and-return",
    "transfer",
    "progress-and-reentry",
    "accessible-alternative",
)
EXPECTED_MATERIAL_PATTERN_FAMILIES = set(MATERIAL_PATTERN_FAMILY_ORDER)
EXPECTED_MATERIAL_WALKTHROUGHS = {
    "entry",
    "central-learning-action",
    "securing-and-reentry",
}
MATERIAL_PATTERN_STATUSES = {"draft", "working", "reviewed"}
MATERIAL_PATTERN_QUANTIFIED_SCOPES = {"conditional", "context-bound", "universal"}
MATERIAL_PATTERN_NUMERIC_LIMIT_PATTERN = re.compile(
    r"\b(?:\d+|ein(?:e[rmns]?)?|eins|zwei|drei|vier|fünf|sechs|sieben|acht|neun|zehn|elf|zwölf|"
    r"dreizehn|vierzehn|fünfzehn|sechzehn|siebzehn|achtzehn|neunzehn|zwanzig)"
    r"(?:\s*[-‑–]\s*(?:seitig\w*|minütig\w*|jährig\w*)|"
    r"\s+(?:Seite(?:n)?|Min(?:\.|ute(?:n)?)?|Element(?:e|en)?|Jahr(?:e)?))\b|"
    r"\b(?:zwei|drei|vier|fünf|sechs|sieben|acht|neun|zehn|elf|zwölf|dreizehn|"
    r"vierzehn|fünfzehn|sechzehn|siebzehn|achtzehn|neunzehn|zwanzig)"
    r"(?:seitig\w*|minütig\w*|jährig\w*)\b",
    re.IGNORECASE,
)
MATERIAL_PATTERN_BOUNDED_COUNT_PATTERN = re.compile(
    r"\b(?:mindestens|höchstens|maximal|genau)\s+"
    r"(?:\d+|ein(?:e[rmns]?)?|eins|zwei|drei|vier|fünf|sechs|sieben|acht|neun|zehn|elf|zwölf|"
    r"dreizehn|vierzehn|fünfzehn|sechzehn|siebzehn|achtzehn|neunzehn|zwanzig)"
    r"(?:\s+[\w-]+){0,2}\s+"
    r"(?:Produktlage(?:n)?|Ansicht(?:en)?|Abschnitt(?:e)?|Schritt(?:e)?|Karte(?:n)?|Kachel(?:n)?|"
    r"Spalte(?:n)?|Zeile(?:n)?|Bildschirm(?:e)?)\b",
    re.IGNORECASE,
)
MATERIAL_PATTERN_PRODUCT_FEATURE_PATTERN = re.compile(
    r"\b(?:app[- ]?shell|pwa|react router|sidebar|navbar|routing|astro[- ]?komponente|"
    r"dashboard[- ]?karte|weiter[- ]?button|button|schaltfläche|navigationsleiste|"
    r"zurück[- ]?link|registerkarte|menü|akkordeon|dialogfenster|dropdown)\b",
    re.IGNORECASE,
)
MATERIAL_PATTERN_VISUAL_SPEC_PATTERN = re.compile(
    r"(?:\b\d+(?:[.,]\d+)?\s*(?:px|rem|em)\b|"
    r"\b(?:ein|zwei|drei|vier|fünf|sechs|sieben|acht|neun|zehn)[- ]?spaltig\w*\b|"
    r"\brund\w*\s+(?:Karte|Kachel)\w*\b|\bSchatten\w*\b|"
    r"\b(?:blau|rot|grün|gelb|orange|violett|lila|grau|schwarz|weiß)\w*\s+"
    r"(?:Karte|Kachel|Überschrift|Button|Schaltfläche|Hintergrund)\b)",
    re.IGNORECASE,
)
MATERIAL_PATTERN_LEARNER_UI_COPY_PATTERN = re.compile(
    r"\b(?:klicke|tippe|drücke|ziehe|wähle|öffne|beginne|starte|wechsle|navigiere|löse)\b"
    r"[^.!?]*\b(?:weiter|zurück|button|schaltfläche|karte|kachel|menü|link|registerkarte|aufgabe)\b",
    re.IGNORECASE,
)
MATERIAL_PATTERN_SCHEMA_SHA256 = (
    "09324B5AE1288DE5AC2204EBB97E012E3D72ACB6328374C47FB59120FA14831E"
)
ALLOWED_LEGACY_EXTERNAL_EVIDENCE = {
    (
        "git:origin/feat/lxp05-ium5-experience:"
        "docs/quality/ium-learning-experience-implementation-report.md"
    ),
    (
        "vault:Vault/40_Projekte/IuM-Lernwerk/"
        "2026-08-30 - Analyse - IUM5 Bestandsanalyse "
        "Lernenden- und Lehrkraftperspektive.md"
    ),
}
EXPECTED_LINK_AUDIT_POLICY = {
    "requiredFailure": "block-and-preserve-last-snapshot",
    "optionalFailure": "warn-and-write",
    "acceptedStatuses": ["resolved", "restricted"],
}


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_status(data: object) -> list[str]:
    if not isinstance(data, dict):
        return ["V2 status muss ein Objekt sein"]

    errors: list[str] = []
    unknown_fields = sorted(
        set(data)
        - {
            "schemaVersion",
            "projectId",
            "activeBaseline",
            "v2State",
            "contentProduction",
            "lxp05",
            "cutover",
        }
    )
    if unknown_fields:
        errors.append(
            "V2 status enthält unbekannte Felder: " + ", ".join(unknown_fields)
        )
    if data.get("schemaVersion") != 1:
        errors.append("V2 schemaVersion muss 1 sein")
    if data.get("projectId") != "ium-lernwerk":
        errors.append("V2 projectId muss ium-lernwerk sein")

    v2_state = data.get("v2State")
    if v2_state != "building":
        errors.append("v2State muss building sein")
    if data.get("activeBaseline") != "v1":
        if v2_state == "building":
            errors.append(
                "activeBaseline muss v1 sein, solange v2State building ist"
            )
        else:
            errors.append("activeBaseline muss v1 sein")
    if data.get("contentProduction") != "frozen":
        errors.append("contentProduction muss frozen sein")

    lxp05 = data.get("lxp05")
    if not isinstance(lxp05, dict) or lxp05 != {
        "state": "frozen",
        "integration": "unmerged",
    }:
        errors.append("LXP05 muss frozen und unmerged bleiben")

    cutover = data.get("cutover")
    if not isinstance(cutover, dict) or cutover != {"state": "not-approved"}:
        errors.append("cutover muss not-approved sein")
    return errors


def _is_repository_relative(value: object) -> bool:
    if not isinstance(value, str) or not value.strip() or "\\" in value:
        return False
    if re.match(r"^[A-Za-z]:", value):
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def validate_archive(data: object) -> list[str]:
    if not isinstance(data, dict):
        return ["V1-Archiv muss ein Objekt sein"]

    errors: list[str] = []
    unknown_fields = sorted(
        set(data)
        - {
            "schemaVersion",
            "repository",
            "remote",
            "mainCommit",
            "candidateRefs",
            "artifactRoots",
            "capturedAt",
            "statementBoundaries",
            "limitations",
        }
    )
    if unknown_fields:
        errors.append(
            "V1-Archiv enthält unbekannte Felder: " + ", ".join(unknown_fields)
        )
    if data.get("schemaVersion") != 1:
        errors.append("V1 schemaVersion muss 1 sein")
    if data.get("repository") != EXPECTED_REPOSITORY:
        errors.append(f"V1 repository muss {EXPECTED_REPOSITORY} sein")
    if data.get("remote") != EXPECTED_REMOTE:
        errors.append("V1 remote muss das geprüfte GitHub-Remote sein")
    if not isinstance(data.get("mainCommit"), str) or not FULL_SHA_PATTERN.fullmatch(
        data["mainCommit"]
    ):
        errors.append("V1 mainCommit muss eine vollständige 40-stellige SHA sein")
    elif data["mainCommit"] != EXPECTED_MAIN_COMMIT:
        errors.append(
            "V1 mainCommit muss den verifizierten main-Stand "
            f"{EXPECTED_MAIN_COMMIT} referenzieren"
        )

    candidate_refs = data.get("candidateRefs")
    if not isinstance(candidate_refs, list):
        candidate_refs = []
    for candidate in candidate_refs:
        if not isinstance(candidate, dict):
            errors.append("V1 candidateRef muss ein Objekt sein")
            continue
        ref = candidate.get("ref")
        commit = candidate.get("commit")
        if not isinstance(commit, str) or not FULL_SHA_PATTERN.fullmatch(commit):
            errors.append(
                "V1 candidateRef commit muss eine vollständige 40-stellige SHA sein: "
                f"{ref if isinstance(ref, str) else '<unbekannt>'}"
            )
    if EXPECTED_LXP05_REF not in candidate_refs:
        errors.append(
            "V1-Archiv muss den verifizierten ungemergten LXP05-Kandidaten enthalten"
        )

    artifact_roots = data.get("artifactRoots")
    if not isinstance(artifact_roots, list) or not artifact_roots:
        errors.append("V1 artifactRoots dürfen nicht leer sein")
    else:
        for artifact_root in artifact_roots:
            if not _is_repository_relative(artifact_root):
                errors.append(
                    "V1 artifactRoot muss repository-relativ sein: "
                    f"{artifact_root}"
                )

    captured_at = data.get("capturedAt")
    if not isinstance(captured_at, str) or not DATE_PATTERN.fullmatch(captured_at):
        errors.append("V1 capturedAt muss YYYY-MM-DD sein")

    statement_boundaries = data.get("statementBoundaries")
    if statement_boundaries != list(EXPECTED_STATEMENT_BOUNDARIES):
        errors.append("V1-Archiv muss alle verbindlichen Aussagegrenzen enthalten")

    limitations = data.get("limitations")
    dashboard_limited = isinstance(limitations, list) and any(
        isinstance(item, dict)
        and item.get("reference") == UNVERIFIED_DASHBOARD_COMMIT
        and item.get("status") == "unverified-local"
        for item in limitations
    )
    if not dashboard_limited:
        errors.append(
            "V1-Archiv muss den Dashboard-Commit 07bc15e1e70d als "
            "unverified-local begrenzen"
        )
    return errors


def _nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_evidence_pointer(
    pointer: object,
    requirement_id: str,
    root: Path | None,
    warnings: list[str],
) -> list[str]:
    if not isinstance(pointer, dict):
        return [f"Evidenzreferenz muss ein Objekt sein in {requirement_id}"]

    errors: list[str] = []
    unknown_fields = sorted(set(pointer) - EVIDENCE_FIELDS)
    if unknown_fields:
        errors.append(
            f"Evidenzreferenz enthält unbekannte Felder in {requirement_id}: "
            + ", ".join(unknown_fields)
        )

    kind = pointer.get("kind")
    if not isinstance(kind, str) or kind not in EVIDENCE_KINDS:
        errors.append(f"unbekannter Evidenztyp {kind} in {requirement_id}")

    required = pointer.get("required")
    if not isinstance(required, bool):
        errors.append(
            f"Evidenzreferenz required muss boolesch sein in {requirement_id}"
        )

    target = pointer.get("target")
    if not _nonempty_string(target):
        if required is True:
            errors.append(f"Pflichtreferenz ohne Ziel in {requirement_id}")
        else:
            errors.append(f"optionale Referenz ohne Ziel in {requirement_id}")

    if not _nonempty_string(pointer.get("label")):
        errors.append(f"Evidenzreferenz ohne Label in {requirement_id}")

    if kind == "repo" and _nonempty_string(target):
        if not _is_repository_relative(target):
            errors.append(
                f"Repository-Referenz muss repository-relativ sein in "
                f"{requirement_id}: {target}"
            )
        elif root is not None and not (root / target).exists():
            if required is True:
                errors.append(
                    f"Pflichtreferenz im Repository fehlt in {requirement_id}: "
                    f"{target}"
                )
            elif required is False:
                warnings.append(
                    f"optionale Repository-Referenz fehlt in {requirement_id}: "
                    f"{target}"
                )
    elif kind == "vault" and _nonempty_string(target) and required is False:
        warnings.append(
            f"optionale Vault-Referenz lokal nicht auflösbar in {requirement_id}: "
            f"{target}"
        )
    elif (
        kind == "git"
        and _nonempty_string(target)
        and not FULL_SHA_PATTERN.fullmatch(target)
    ):
        errors.append(
            "Git-Referenz muss eine vollständige 40-stellige SHA sein in "
            f"{requirement_id}: {target}"
        )
    return errors


def _dependency_cycle(requirements_by_id: dict[str, dict]) -> list[str] | None:
    state: dict[str, int] = {}
    stack: list[str] = []

    def visit(requirement_id: str) -> list[str] | None:
        state[requirement_id] = 1
        stack.append(requirement_id)
        dependencies = requirements_by_id[requirement_id].get("dependencies", [])
        if isinstance(dependencies, list):
            for dependency in sorted(
                item for item in dependencies if isinstance(item, str)
            ):
                if dependency not in requirements_by_id:
                    continue
                if state.get(dependency, 0) == 1:
                    start = stack.index(dependency)
                    return stack[start:] + [dependency]
                if state.get(dependency, 0) == 0:
                    cycle = visit(dependency)
                    if cycle is not None:
                        return cycle
        stack.pop()
        state[requirement_id] = 2
        return None

    for requirement_id in sorted(requirements_by_id):
        if state.get(requirement_id, 0) == 0:
            cycle = visit(requirement_id)
            if cycle is not None:
                return cycle
    return None


def validate_requirements(
    data: object,
    root: Path | None = None,
    warnings: list[str] | None = None,
) -> list[str]:
    if not isinstance(data, dict):
        return ["V2-Anforderungsregister muss ein Objekt sein"]

    report_warnings = warnings if warnings is not None else []
    errors: list[str] = []
    unknown_fields = sorted(set(data) - REQUIREMENTS_TOP_LEVEL_FIELDS)
    if unknown_fields:
        errors.append(
            "V2-Anforderungsregister enthält unbekannte Felder: "
            + ", ".join(unknown_fields)
        )
    if data.get("schemaVersion") != 1:
        errors.append("V2-Anforderungsregister schemaVersion muss 1 sein")
    if data.get("projectId") != "ium-lernwerk":
        errors.append("V2-Anforderungsregister projectId muss ium-lernwerk sein")
    if not isinstance(data.get("asOf"), str) or not DATE_PATTERN.fullmatch(
        data["asOf"]
    ):
        errors.append("V2-Anforderungsregister asOf muss YYYY-MM-DD sein")

    requirements = data.get("requirements")
    if not isinstance(requirements, list) or not requirements:
        errors.append("V2 requirements dürfen nicht leer sein")
        return errors

    seen_ids: set[str] = set()
    requirements_by_id: dict[str, dict] = {}
    for index, requirement in enumerate(requirements):
        if not isinstance(requirement, dict):
            errors.append(f"V2-Anforderung an Position {index} muss ein Objekt sein")
            continue

        requirement_id_value = requirement.get("id")
        requirement_id = (
            requirement_id_value
            if _nonempty_string(requirement_id_value)
            else f"<Position {index}>"
        )
        unknown_requirement_fields = sorted(set(requirement) - REQUIREMENT_FIELDS)
        if unknown_requirement_fields:
            errors.append(
                f"V2-Anforderung enthält unbekannte Felder in {requirement_id}: "
                + ", ".join(unknown_requirement_fields)
            )

        if not _nonempty_string(requirement_id_value):
            errors.append(
                f"Pflichtfeld id fehlt oder ist leer in {requirement_id}"
            )
        elif not REQUIREMENT_ID_PATTERN.fullmatch(requirement_id_value):
            errors.append(f"ungültige Anforderungs-ID {requirement_id_value}")
        elif requirement_id_value in seen_ids:
            errors.append(f"doppelte Anforderungs-ID {requirement_id_value}")
        else:
            seen_ids.add(requirement_id_value)
            requirements_by_id[requirement_id_value] = requirement

        for field in ("title", "statement", "gate"):
            if not _nonempty_string(requirement.get(field)):
                errors.append(
                    f"Pflichtfeld {field} fehlt oder ist leer in {requirement_id}"
                )

        domain = requirement.get("domain")
        if not isinstance(domain, str) or domain not in REQUIREMENT_DOMAINS:
            errors.append(f"unbekannte Domäne {domain}")
        binding = requirement.get("binding")
        if not isinstance(binding, str) or binding not in REQUIREMENT_BINDINGS:
            errors.append(f"unbekannte Bindung {binding} in {requirement_id}")
        scope = requirement.get("scope")
        if not isinstance(scope, str) or scope not in REQUIREMENT_SCOPES:
            errors.append(f"unbekannter Scope {scope} in {requirement_id}")
        coverage = requirement.get("coverage")
        if not isinstance(coverage, str) or coverage not in REQUIREMENT_COVERAGE:
            errors.append(
                f"unbekannter Abdeckungsstatus {coverage} in {requirement_id}"
            )

        grades = requirement.get("grades")
        if not isinstance(grades, list) or not grades:
            errors.append(f"grades dürfen nicht leer sein in {requirement_id}")
        else:
            for grade in grades:
                if not isinstance(grade, int) or grade not in REQUIREMENT_GRADES:
                    errors.append(
                        f"unbekannte Klassenstufe {grade} in {requirement_id}"
                    )
            if len(grades) != len(set(str(grade) for grade in grades)):
                errors.append(f"doppelte Klassenstufe in {requirement_id}")

        modes = requirement.get("fulfillmentModes")
        if not isinstance(modes, list) or not modes:
            errors.append(
                f"fulfillmentModes dürfen nicht leer sein in {requirement_id}"
            )
        else:
            for mode in modes:
                if not isinstance(mode, str) or mode not in FULFILLMENT_MODES:
                    errors.append(
                        f"unbekannter Erfüllungsmodus {mode} in {requirement_id}"
                    )
            if len(modes) != len(set(str(mode) for mode in modes)):
                errors.append(f"doppelter Erfüllungsmodus in {requirement_id}")

        for pointer_field in ("origin", "evidence"):
            pointers = requirement.get(pointer_field)
            if not isinstance(pointers, list) or (
                pointer_field == "origin" and not pointers
            ):
                qualifier = "nicht leer" if pointer_field == "origin" else "eine Liste"
                errors.append(
                    f"{pointer_field} muss {qualifier} sein in {requirement_id}"
                )
                continue
            for pointer in pointers:
                errors.extend(
                    _validate_evidence_pointer(
                        pointer,
                        requirement_id,
                        root,
                        report_warnings,
                    )
                )

        evidence = requirement.get("evidence")
        if coverage == "covered" and (
            not isinstance(evidence, list) or not evidence
        ):
            errors.append(
                f"V2-Abdeckung covered benötigt Evidenz in {requirement_id}"
            )

        dependencies = requirement.get("dependencies")
        if not isinstance(dependencies, list):
            errors.append(f"dependencies muss eine Liste sein in {requirement_id}")
        elif not all(_nonempty_string(item) for item in dependencies):
            errors.append(
                f"dependencies enthält eine leere ID in {requirement_id}"
            )
        elif len(dependencies) != len(set(dependencies)):
            errors.append(f"doppelte Abhängigkeit in {requirement_id}")

        risks = requirement.get("risks")
        if not isinstance(risks, list) or not risks or not all(
            _nonempty_string(risk) for risk in risks
        ):
            errors.append(f"risks dürfen nicht leer sein in {requirement_id}")

    for requirement_id, requirement in sorted(requirements_by_id.items()):
        dependencies = requirement.get("dependencies", [])
        if not isinstance(dependencies, list):
            continue
        for dependency in dependencies:
            if _nonempty_string(dependency) and dependency not in requirements_by_id:
                errors.append(f"unbekannte Abhängigkeit {dependency}")

    cycle = _dependency_cycle(requirements_by_id)
    if cycle is not None:
        errors.append(
            "zyklische Anforderungsabhängigkeit " + " -> ".join(cycle)
        )
    return errors


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _is_https_url(value: object) -> bool:
    if not _nonempty_string(value):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def _is_http_url(value: object) -> bool:
    if not _nonempty_string(value):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _is_iso_date(value: object) -> bool:
    if not isinstance(value, str) or not DATE_PATTERN.fullmatch(value):
        return False
    try:
        calendar_date.fromisoformat(value)
    except ValueError:
        return False
    return True


def _is_plain_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _missing_fields(data: dict, required: set[str], label: str) -> list[str]:
    return [
        f"{label} benötigt Pflichtfeld {field}"
        for field in sorted(required - set(data))
    ]


def _unknown_fields(
    data: dict,
    allowed: set[str],
    label: str,
) -> list[str]:
    unknown = sorted(set(data) - allowed)
    if not unknown:
        return []
    return [f"{label} enthält unbekannte Felder: " + ", ".join(unknown)]


def _load_contract_json(
    root: Path,
    relative_path: str,
    label: str,
    errors: list[str],
) -> object | None:
    if not _is_repository_relative(relative_path):
        errors.append(f"{label} muss repository-relativ sein: {relative_path}")
        return None
    path = root / relative_path
    if not path.is_file():
        errors.append(f"{label} fehlt: {relative_path}")
        return None
    try:
        return load_json(path)
    except (OSError, UnicodeError, json.JSONDecodeError):
        errors.append(f"{label} ist kein gültiges JSON: {relative_path}")
        return None


def validate_curriculum_source_basis(data: object, root: Path) -> list[str]:
    if not isinstance(data, dict):
        return ["V2-Curriculumquellenbasis muss ein Objekt sein"]

    errors: list[str] = []
    errors.extend(
        _unknown_fields(
            data,
            {
                "schemaVersion",
                "projectId",
                "asOf",
                "baseline",
                "sources",
                "totals",
                "crosswalk",
                "coverageAudit",
                "decisionBasis",
                "statementBoundaries",
            },
            "V2-Curriculumquellenbasis",
        )
    )
    if data.get("schemaVersion") != 1:
        errors.append("V2-Curriculumquellenbasis schemaVersion muss 1 sein")
    if data.get("projectId") != "ium-lernwerk":
        errors.append("V2-Curriculumquellenbasis projectId muss ium-lernwerk sein")
    if not isinstance(data.get("asOf"), str) or not DATE_PATTERN.fullmatch(
        data["asOf"]
    ):
        errors.append("V2-Curriculumquellenbasis asOf muss YYYY-MM-DD sein")

    baseline = data.get("baseline")
    if not isinstance(baseline, dict):
        errors.append("V2-Curriculumbaseline muss ein Objekt sein")
    else:
        errors.extend(
            _unknown_fields(
                baseline,
                {"status", "commit", "immutablePaths"},
                "V2-Curriculumbaseline",
            )
        )
        if baseline.get("status") != "v1-audit-input":
            errors.append("V2-Curriculumbaseline muss v1-audit-input bleiben")
        if baseline.get("commit") != EXPECTED_MAIN_COMMIT:
            errors.append(
                "V2-Curriculumbaseline muss den versiegelten V1-Commit "
                f"{EXPECTED_MAIN_COMMIT} verwenden"
            )
        immutable_paths = baseline.get("immutablePaths")
        expected_paths = {
            expectation["repositoryPath"]
            for expectation in CURRICULUM_SOURCE_EXPECTATIONS.values()
        } | {"curriculum/crosswalk.json", "roadmap/coverage-plan.json"}
        if not isinstance(immutable_paths, list):
            errors.append(
                "V2-Curriculumbaseline muss alle fünf unveränderten V1-Pfade versiegeln"
            )
        elif not all(
            isinstance(path, str) and _is_repository_relative(path)
            for path in immutable_paths
        ):
            errors.append("V2-Curriculumbaseline enthält einen ungültigen Pfad")
        elif set(immutable_paths) != expected_paths:
            errors.append(
                "V2-Curriculumbaseline muss alle fünf unveränderten V1-Pfade versiegeln"
            )

    sources = data.get("sources")
    if not isinstance(sources, list):
        errors.append("V2-Curriculumquellen müssen eine Liste sein")
        sources = []
    source_ids = [
        source.get("sourceId")
        for source in sources
        if isinstance(source, dict) and _nonempty_string(source.get("sourceId"))
    ]
    if len(source_ids) != len(set(source_ids)):
        errors.append("V2-Curriculumquellen enthalten doppelte sourceIds")
    if set(source_ids) != set(CURRICULUM_SOURCE_EXPECTATIONS):
        errors.append("V2-Curriculumquellen müssen exakt die drei geprüften Quellen enthalten")

    all_record_ids: list[str] = []
    for source in sources:
        if not isinstance(source, dict):
            errors.append("V2-Curriculumquelle muss ein Objekt sein")
            continue
        source_id = source.get("sourceId")
        if not _nonempty_string(source_id):
            errors.append("V2-Curriculumquelle benötigt eine sourceId")
            continue
        expectation = CURRICULUM_SOURCE_EXPECTATIONS.get(source_id)
        if expectation is None:
            continue
        errors.extend(
            _unknown_fields(
                source,
                {
                    "sourceId",
                    "title",
                    "binding",
                    "normativeStatus",
                    "repositoryPath",
                    "datasetSha256",
                    "sourceAssetSha256",
                    "recordCount",
                    "grades",
                    "checkedAt",
                    "currentReview",
                },
                f"Curriculumquelle {source_id}",
            )
        )
        if source.get("binding") != expectation["binding"]:
            if source_id == "SRC-CUR-LESEHILFE-2026-27":
                errors.append(
                    "SRC-CUR-LESEHILFE-2026-27 muss als orientation gebunden bleiben"
                )
            else:
                errors.append(f"Curriculumquelle {source_id} muss official gebunden sein")
        for field in (
            "title",
            "normativeStatus",
            "repositoryPath",
            "datasetSha256",
            "sourceAssetSha256",
            "grades",
        ):
            if source.get(field) != expectation[field]:
                errors.append(
                    f"Curriculumquelle {source_id} hat einen abweichenden Wert in {field}"
                )
        if source.get("recordCount") != expectation["recordCount"]:
            errors.append(
                f"Curriculumquelle {source_id} erwartet {expectation['recordCount']} "
                f"Records, deklariert {source.get('recordCount')}"
            )
        if not isinstance(source.get("checkedAt"), str) or not DATE_PATTERN.fullmatch(
            source["checkedAt"]
        ):
            errors.append(f"Curriculumquelle {source_id} checkedAt muss YYYY-MM-DD sein")

        current_review = source.get("currentReview")
        if not isinstance(current_review, dict):
            errors.append(f"Curriculumquelle {source_id} benötigt currentReview")
        else:
            errors.extend(
                _unknown_fields(
                    current_review,
                    {
                        "checkedAt",
                        "status",
                        "landingPageUrl",
                        "directUrl",
                        "contentIdentity",
                        "remoteSha256",
                        "remoteByteLength",
                        "finding",
                    },
                    f"currentReview {source_id}",
                )
            )
            if current_review.get("checkedAt") != "2026-09-03":
                errors.append(f"currentReview {source_id} muss am 2026-09-03 geprüft sein")
            current_review_status = current_review.get("status")
            if not isinstance(current_review_status, str) or current_review_status not in {
                "transition-status-rechecked",
                "direct-source-rechecked",
            }:
                errors.append(f"currentReview {source_id} hat unbekannten Prüfstatus")
            for field in ("landingPageUrl", "directUrl"):
                if not _is_https_url(current_review.get(field)):
                    errors.append(f"currentReview {source_id} benötigt eine HTTPS-{field}")
            if current_review.get("directUrl") != expectation["directUrl"]:
                errors.append(f"currentReview {source_id} hat eine abweichende Direktfundstelle")
            if current_review.get("contentIdentity") != expectation[
                "contentIdentity"
            ]:
                errors.append(
                    f"currentReview {source_id} hat einen unbelegten Identitätsstatus"
                )
            if source_id == "SRC-CUR-LESEHILFE-2026-27":
                if current_review.get("remoteSha256") != expectation[
                    "sourceAssetSha256"
                ]:
                    errors.append(
                        "currentReview SRC-CUR-LESEHILFE-2026-27 muss den geprüften Remote-Hash ausweisen"
                    )
                if current_review.get("remoteByteLength") != 246597:
                    errors.append(
                        "currentReview SRC-CUR-LESEHILFE-2026-27 muss 246597 Remote-Bytes ausweisen"
                    )
            elif current_review.get("remoteSha256") is not None or current_review.get(
                "remoteByteLength"
            ) is not None:
                errors.append(
                    f"currentReview {source_id} darf ohne neuen Download keine Remote-Bytes behaupten"
                )
            if not _nonempty_string(current_review.get("finding")):
                errors.append(f"currentReview {source_id} benötigt einen Befund")

        relative_path = expectation["repositoryPath"]
        source_data = _load_contract_json(
            root,
            relative_path,
            f"Curriculumdatensatz {source_id}",
            errors,
        )
        if source_data is None:
            continue
        if _sha256(root / relative_path) != expectation["datasetSha256"]:
            errors.append(
                f"Curriculumdatensatz {source_id} weicht vom versiegelten V1-Hash ab"
            )
        if not isinstance(source_data, dict) or source_data.get("sourceId") != source_id:
            errors.append(f"Curriculumdatensatz {source_id} hat eine falsche sourceId")
            continue
        records = source_data.get("records")
        if not isinstance(records, list):
            errors.append(f"Curriculumdatensatz {source_id} benötigt Records")
            continue
        if len(records) != expectation["recordCount"]:
            errors.append(
                f"Curriculumdatensatz {source_id} enthält {len(records)} statt "
                f"{expectation['recordCount']} Records"
            )
        record_ids = [
            record.get("id")
            for record in records
            if isinstance(record, dict) and _nonempty_string(record.get("id"))
        ]
        if len(record_ids) != len(records) or len(record_ids) != len(set(record_ids)):
            errors.append(f"Curriculumdatensatz {source_id} enthält ungültige oder doppelte IDs")
        all_record_ids.extend(record_ids)
        metadata = source_data.get("metadata")
        if not isinstance(metadata, dict) or metadata.get("sha256") != expectation[
            "sourceAssetSha256"
        ]:
            errors.append(f"Curriculumdatensatz {source_id} hat einen abweichenden Quellasset-Hash")

    totals = data.get("totals")
    if isinstance(totals, dict):
        errors.extend(
            _unknown_fields(
                totals,
                {"recordCount", "uniqueRecordCount"},
                "V2-Curriculumgesamtzählung",
            )
        )
    if totals != {"recordCount": 278, "uniqueRecordCount": 278}:
        errors.append("V2-Curriculumquellenbasis muss 278 Records und 278 eindeutige IDs ausweisen")
    if len(all_record_ids) != 278 or len(set(all_record_ids)) != 278:
        errors.append("Die drei versiegelten Curriculumdatensätze müssen 278 eindeutige Records enthalten")

    crosswalk = data.get("crosswalk")
    if not isinstance(crosswalk, dict):
        errors.append("V2-Curriculumquellenbasis benötigt den V1-Crosswalk")
    else:
        errors.extend(
            _unknown_fields(
                crosswalk,
                {
                    "repositoryPath",
                    "datasetSha256",
                    "status",
                    "recordCount",
                    "relationCount",
                    "unmappedRecordCount",
                    "relationshipCounts",
                },
                "V2-Crosswalk",
            )
        )
        crosswalk_path = "curriculum/crosswalk.json"
        expected_hash = "8522C912C7747AF1D39D2822513A3E75EF410CB7BBE9BD98574BF9CF69AC0720"
        if crosswalk.get("repositoryPath") != crosswalk_path:
            errors.append("V2-Crosswalk muss curriculum/crosswalk.json referenzieren")
        if crosswalk.get("datasetSha256") != expected_hash:
            errors.append("V2-Crosswalk muss den versiegelten V1-Hash ausweisen")
        if crosswalk.get("status") != "v1-audit-input":
            errors.append("V2-Crosswalk muss v1-audit-input bleiben")
        actual_crosswalk = _load_contract_json(
            root, crosswalk_path, "V1-Crosswalk", errors
        )
        if actual_crosswalk is not None:
            if _sha256(root / crosswalk_path) != expected_hash:
                errors.append("V1-Crosswalk weicht vom versiegelten Hash ab")
            expected_counts = {
                "curriculumRecords": 278,
                "relations": 56,
                "unmappedRecords": 107,
                "relationshipCounts": {
                    "equivalent": 2,
                    "extends": 15,
                    "new": 3,
                    "not-comparable": 4,
                    "overlaps": 15,
                    "reframes": 17,
                },
            }
            if not isinstance(actual_crosswalk, dict) or actual_crosswalk.get(
                "counts"
            ) != expected_counts:
                errors.append("V1-Crosswalk-Zählungen weichen vom geprüften Stand ab")
            for field, expected_field in (
                ("recordCount", 278),
                ("relationCount", 56),
                ("unmappedRecordCount", 107),
            ):
                if crosswalk.get(field) != expected_field:
                    errors.append(f"V2-Crosswalk hat einen abweichenden Wert in {field}")
            if crosswalk.get("relationshipCounts") != expected_counts[
                "relationshipCounts"
            ]:
                errors.append("V2-Crosswalk hat abweichende Beziehungstyp-Zählungen")

    coverage_audit = data.get("coverageAudit")
    if not isinstance(coverage_audit, dict):
        errors.append("V2-Curriculumquellenbasis benötigt den V1-Coverage-Audit")
    else:
        errors.extend(
            _unknown_fields(
                coverage_audit,
                {
                    "repositoryPath",
                    "datasetSha256",
                    "status",
                    "entryCount",
                    "byBinding",
                },
                "V2-Coverage-Audit",
            )
        )
        coverage_path = "roadmap/coverage-plan.json"
        expected_hash = "4553BE524D7DBC0E02EA3362869A71EE2F4B28164A18AEC7557FDC2001990929"
        expected_by_binding = {
            "official": {"covered": 74, "partial": 2, "total": 76},
            "orientation": {"covered": 92, "partial": 3, "total": 95},
        }
        if coverage_audit.get("repositoryPath") != coverage_path:
            errors.append("V2-Coverage-Audit muss roadmap/coverage-plan.json referenzieren")
        if coverage_audit.get("datasetSha256") != expected_hash:
            errors.append("V2-Coverage-Audit muss den versiegelten V1-Hash ausweisen")
        if coverage_audit.get("status") != "v1-audit-input":
            errors.append("V2-Coverage-Audit muss v1-audit-input bleiben")
        if coverage_audit.get("entryCount") != 171:
            errors.append("V2-Coverage-Audit muss 171 V1-Einträge ausweisen")
        if coverage_audit.get("byBinding") != expected_by_binding:
            errors.append("V2-Coverage-Audit hat abweichende Bindungszählungen")
        coverage_data = _load_contract_json(
            root, coverage_path, "V1-Coverage-Audit", errors
        )
        if coverage_data is not None:
            if _sha256(root / coverage_path) != expected_hash:
                errors.append("V1-Coverage-Audit weicht vom versiegelten Hash ab")
            entries = coverage_data.get("entries") if isinstance(coverage_data, dict) else None
            if not isinstance(entries, list) or len(entries) != 171:
                errors.append("V1-Coverage-Audit muss 171 Einträge enthalten")
            else:
                actual_counts = {
                    "official": {"covered": 0, "partial": 0, "total": 0},
                    "orientation": {"covered": 0, "partial": 0, "total": 0},
                }
                for entry in entries:
                    if not isinstance(entry, dict):
                        continue
                    binding = (
                        "official"
                        if entry.get("normativeWeight") == "enacted"
                        else "orientation"
                    )
                    status = entry.get("coverageStatus")
                    if status in {"covered", "partial"}:
                        actual_counts[binding][status] += 1
                        actual_counts[binding]["total"] += 1
                if actual_counts != expected_by_binding:
                    errors.append("V1-Coverage-Audit-Zählungen weichen vom geprüften Stand ab")

    decision_basis = data.get("decisionBasis")
    if not isinstance(decision_basis, list) or not decision_basis:
        errors.append("V2-Curriculumquellenbasis benötigt eine Entscheidungsbasis")
    else:
        for pointer in decision_basis:
            errors.extend(
                _validate_evidence_pointer(
                    pointer,
                    "curriculum-source-basis",
                    root,
                    [],
                )
            )
    boundaries = data.get("statementBoundaries")
    if not isinstance(boundaries, list) or len(boundaries) < 2 or not all(
        _nonempty_string(boundary) for boundary in boundaries
    ):
        errors.append("V2-Curriculumquellenbasis benötigt Aussagegrenzen")
    return errors


def _curriculum_record_index(root: Path, errors: list[str]) -> dict[str, dict]:
    index: dict[str, dict] = {}
    for expectation in CURRICULUM_SOURCE_EXPECTATIONS.values():
        path = expectation["repositoryPath"]
        data = _load_contract_json(root, path, "Curriculumdatensatz", errors)
        if not isinstance(data, dict):
            continue
        records = data.get("records")
        if not isinstance(records, list):
            continue
        for record in records:
            if isinstance(record, dict) and _nonempty_string(record.get("id")):
                index[record["id"]] = record
    return index


def validate_curriculum_gap_assessments(data: object, root: Path) -> list[str]:
    if not isinstance(data, dict):
        return ["V2-Curriculumlückenregister muss ein Objekt sein"]

    errors: list[str] = []
    errors.extend(
        _unknown_fields(
            data,
            {
                "schemaVersion",
                "projectId",
                "asOf",
                "baselineCoveragePath",
                "coverageBoundary",
                "assessments",
            },
            "V2-Curriculumlückenregister",
        )
    )
    if data.get("schemaVersion") != 1:
        errors.append("V2-Curriculumlückenregister schemaVersion muss 1 sein")
    if data.get("projectId") != "ium-lernwerk":
        errors.append("V2-Curriculumlückenregister projectId muss ium-lernwerk sein")
    if not isinstance(data.get("asOf"), str) or not DATE_PATTERN.fullmatch(
        data["asOf"]
    ):
        errors.append("V2-Curriculumlückenregister asOf muss YYYY-MM-DD sein")
    if data.get("baselineCoveragePath") != "roadmap/coverage-plan.json":
        errors.append("V2-Curriculumlückenregister muss den V1-Coverage-Audit referenzieren")
    if not _nonempty_string(data.get("coverageBoundary")):
        errors.append("V2-Curriculumlückenregister benötigt eine Abdeckungsgrenze")

    assessments = data.get("assessments")
    if not isinstance(assessments, list):
        errors.append("V2-Curriculumlücken assessments müssen eine Liste sein")
        assessments = []
    ids = [
        assessment.get("competencyId")
        for assessment in assessments
        if isinstance(assessment, dict)
        and _nonempty_string(assessment.get("competencyId"))
    ]
    if len(ids) != len(set(ids)):
        errors.append("V2-Curriculumlücken enthalten doppelte competencyIds")
    if set(ids) != set(EXPECTED_CURRICULUM_GAPS):
        errors.append(
            "V2-Curriculumlücken müssen exakt die fünf aktuellen V1-partial-Records enthalten"
        )

    coverage_data = _load_contract_json(
        root,
        "roadmap/coverage-plan.json",
        "V1-Coverage-Audit",
        errors,
    )
    coverage_entries: dict[str, dict] = {}
    if isinstance(coverage_data, dict) and isinstance(coverage_data.get("entries"), list):
        coverage_entries = {
            entry["competencyId"]: entry
            for entry in coverage_data["entries"]
            if isinstance(entry, dict) and _nonempty_string(entry.get("competencyId"))
        }
        actual_partial = {
            entry_id
            for entry_id, entry in coverage_entries.items()
            if entry.get("coverageStatus") == "partial"
        }
        if actual_partial != set(EXPECTED_CURRICULUM_GAPS):
            errors.append("Der aktuelle V1-Coverage-Audit enthält nicht die erwarteten fünf Restlücken")

    record_index = _curriculum_record_index(root, errors)
    allowed_assessment_fields = {
        "competencyId",
        "sourceId",
        "sourceBinding",
        "sourceDatasetPath",
        "requirementText",
        "v1Audit",
        "v2Coverage",
        "time",
        "followUp",
        "risk",
        "auditEvidence",
        "v2Evidence",
    }
    for assessment in assessments:
        if not isinstance(assessment, dict):
            errors.append("V2-Curriculumlücke muss ein Objekt sein")
            continue
        competency_id = assessment.get("competencyId")
        if not _nonempty_string(competency_id):
            errors.append("V2-Curriculumlücke benötigt eine competencyId")
            continue
        errors.extend(
            _unknown_fields(
                assessment,
                allowed_assessment_fields,
                f"V2-Curriculumlücke {competency_id}",
            )
        )
        expected = EXPECTED_CURRICULUM_GAPS.get(competency_id)
        if expected is None:
            continue
        for field in ("sourceId", "sourceBinding", "sourceDatasetPath"):
            if assessment.get(field) != expected[field]:
                errors.append(f"V2-Curriculumlücke {competency_id} hat falsches {field}")
        record = record_index.get(competency_id)
        if record is None:
            errors.append(f"Curriculumrecord {competency_id} fehlt im versiegelten Datensatz")
        elif assessment.get("requirementText") != record.get("sourceText"):
            errors.append(f"V2-Curriculumlücke {competency_id} verändert den Quellwortlaut")

        v1_audit = assessment.get("v1Audit")
        if not isinstance(v1_audit, dict):
            errors.append(f"V2-Curriculumlücke {competency_id} benötigt v1Audit")
        else:
            errors.extend(
                _unknown_fields(
                    v1_audit,
                    {"status", "normativeWeight", "moduleIds", "timeReviewId"},
                    f"V1-Audit {competency_id}",
                )
            )
            if v1_audit.get("status") != "partial":
                errors.append(f"V1-Auditstatus {competency_id} muss partial bleiben")
            for field in ("normativeWeight", "moduleIds", "timeReviewId"):
                if v1_audit.get(field) != expected[field]:
                    errors.append(f"V1-Audit {competency_id} hat falsches {field}")
            current_entry = coverage_entries.get(competency_id)
            if current_entry is not None:
                if current_entry.get("coverageStatus") != "partial":
                    errors.append(f"V1-Coverage {competency_id} ist nicht mehr partial")
                for current_field, expected_field in (
                    ("normativeWeight", "normativeWeight"),
                    ("moduleIds", "moduleIds"),
                    ("timeReviewId", "timeReviewId"),
                ):
                    if v1_audit.get(expected_field) != current_entry.get(current_field):
                        errors.append(
                            f"V1-Audit {competency_id} weicht im Feld {expected_field} vom Coverage-Plan ab"
                        )

        v2_coverage = assessment.get("v2Coverage")
        if not isinstance(v2_coverage, dict):
            errors.append(f"V2-Curriculumlücke {competency_id} benötigt v2Coverage")
        else:
            errors.extend(
                _unknown_fields(
                    v2_coverage,
                    {"status", "proposedFulfillmentMode", "decisionState", "rationale"},
                    f"V2-Abdeckung {competency_id}",
                )
            )
            coverage_status = v2_coverage.get("status")
            if coverage_status == "covered":
                errors.append(
                    f"V2-Curriculumlücke {competency_id} darf ohne neue V2-Evidenz nicht covered sein"
                )
            elif coverage_status != "unassessed":
                errors.append(
                    f"V2-Curriculumlücke {competency_id} muss bis zum V2-Design unassessed bleiben"
                )
            if v2_coverage.get("proposedFulfillmentMode") != expected[
                "proposedFulfillmentMode"
            ]:
                if competency_id == "BMB16-GYM-IK-GM-003":
                    errors.append(
                        "BMB16-GYM-IK-GM-003 muss als cross-cutting geführt werden"
                    )
                else:
                    errors.append(
                        f"V2-Curriculumlücke {competency_id} hat einen falschen vorgesehenen Erfüllungsmodus"
                    )
            decision_state = v2_coverage.get("decisionState")
            if not isinstance(decision_state, str) or decision_state not in {
                "approved-direction",
                "open",
            }:
                errors.append(f"V2-Curriculumlücke {competency_id} hat ungültigen decisionState")
            elif decision_state != expected["decisionState"]:
                errors.append(
                    f"V2-Curriculumlücke {competency_id} muss bis zur fachlichen "
                    f"Entscheidung {expected['decisionState']} bleiben"
                )
            if not _nonempty_string(v2_coverage.get("rationale")):
                errors.append(f"V2-Curriculumlücke {competency_id} benötigt eine V2-Begründung")

        time = assessment.get("time")
        if not isinstance(time, dict):
            errors.append(f"V2-Curriculumlücke {competency_id} benötigt einen Zeitstatus")
        else:
            errors.extend(
                _unknown_fields(
                    time,
                    {"status", "additionalMinutes", "rationale"},
                    f"V2-Zeitstatus {competency_id}",
                )
            )
            time_status = time.get("status")
            if not isinstance(time_status, str) or time_status not in {
                "no-additional-time",
                "unassessed",
                "not-claimable",
                "roadmap-dependent",
            }:
                errors.append(f"V2-Zeitstatus {competency_id} hat unbekannten Status")
            additional_minutes = time.get("additionalMinutes")
            if additional_minutes is not None and (
                not isinstance(additional_minutes, int)
                or isinstance(additional_minutes, bool)
                or additional_minutes < 0
            ):
                errors.append(
                    f"V2-Zeitstatus {competency_id} hat ungültige additionalMinutes"
                )
            if not _nonempty_string(time.get("rationale")):
                errors.append(f"V2-Zeitstatus {competency_id} benötigt eine Begründung")
            if competency_id == "BMB16-GYM-IK-GM-003":
                if time_status != "no-additional-time" or additional_minutes != 0:
                    errors.append(
                        "BMB16-GYM-IK-GM-003 darf keine zusätzlichen Minuten erzeugen"
                    )
            elif additional_minutes is not None:
                errors.append(
                    f"V2-Curriculumlücke {competency_id} darf vor der Roadmap keine Minuten festlegen"
                )

        follow_up = assessment.get("followUp")
        if not isinstance(follow_up, dict):
            errors.append(f"V2-Curriculumlücke {competency_id} benötigt followUp")
        else:
            errors.extend(
                _unknown_fields(
                    follow_up,
                    {"kind", "newLearningTask", "owner", "nextReview", "acceptanceCriterion"},
                    f"V2-Folgeprüfung {competency_id}",
                )
            )
            for field in ("kind", "newLearningTask", "owner", "nextReview", "acceptanceCriterion"):
                if field not in follow_up or (
                    field not in {"newLearningTask"}
                    and not _nonempty_string(follow_up.get(field))
                ):
                    errors.append(f"V2-Curriculumlücke {competency_id} benötigt followUp.{field}")
            follow_up_kind = follow_up.get("kind")
            if not isinstance(follow_up_kind, str) or follow_up_kind not in {
                "evidence-matrix",
                "module-design",
                "privacy-decision",
                "year-roadmap",
            }:
                errors.append(f"V2-Folgeprüfung {competency_id} hat unbekannte Art")
            new_learning_task = follow_up.get("newLearningTask")
            if not isinstance(new_learning_task, str) or new_learning_task not in {
                "not-required",
                "not-decided",
                "not-applicable",
                "required",
            }:
                errors.append(
                    f"V2-Folgeprüfung {competency_id} hat ungültigen newLearningTask"
                )
            if competency_id == "BMB16-GYM-IK-GM-003" and follow_up.get(
                "newLearningTask"
            ) != "not-required":
                errors.append(
                    "BMB16-GYM-IK-GM-003 darf keine künstliche Zusatzaufgabe erzeugen"
                )
        if not _nonempty_string(assessment.get("risk")):
            errors.append(f"V2-Curriculumlücke {competency_id} benötigt ein Risiko")

        audit_evidence = assessment.get("auditEvidence")
        if not isinstance(audit_evidence, list) or not audit_evidence:
            errors.append(f"V2-Curriculumlücke {competency_id} benötigt Audit-Evidenz")
        else:
            for pointer in audit_evidence:
                errors.extend(
                    _validate_evidence_pointer(pointer, competency_id, root, [])
                )
        v2_evidence = assessment.get("v2Evidence")
        if not isinstance(v2_evidence, list):
            errors.append(f"V2-Curriculumlücke {competency_id} v2Evidence muss eine Liste sein")
        elif v2_evidence:
            errors.append(
                f"V2-Curriculumlücke {competency_id} darf in diesem Fundament noch keine V2-Evidenz beanspruchen"
            )
    return errors


def validate_foundation_status(
    data: object,
    expected_id: str,
    requirement_ids: set[str],
    root: Path,
    warnings: list[str] | None = None,
) -> list[str]:
    if not isinstance(data, dict):
        return [f"V2-Fundamentstatus {expected_id} muss ein Objekt sein"]

    errors: list[str] = []
    report_warnings = warnings if warnings is not None else []
    errors.extend(
        _unknown_fields(
            data,
            {
                "schemaVersion",
                "projectId",
                "id",
                "asOf",
                "workStatus",
                "maturity",
                "requirementIds",
                "evidence",
                "openQuestions",
                "nextGate",
            },
            f"V2-Fundamentstatus {expected_id}",
        )
    )
    if data.get("schemaVersion") != 1:
        errors.append(f"V2-Fundamentstatus {expected_id} schemaVersion muss 1 sein")
    if data.get("projectId") != "ium-lernwerk":
        errors.append(f"V2-Fundamentstatus {expected_id} projectId muss ium-lernwerk sein")
    if data.get("id") != expected_id:
        errors.append(f"V2-Fundamentstatus muss die ID {expected_id} tragen")
    if not isinstance(data.get("asOf"), str) or not DATE_PATTERN.fullmatch(
        data["asOf"]
    ):
        errors.append(f"V2-Fundamentstatus {expected_id} asOf muss YYYY-MM-DD sein")
    work_status = data.get("workStatus")
    if not isinstance(work_status, str) or work_status not in {
        "planned",
        "in_progress",
        "blocked",
        "review",
        "done",
    }:
        errors.append(f"V2-Fundamentstatus {expected_id} hat unbekannten workStatus")

    maturity = data.get("maturity")
    maturity_fields = {
        "curriculumCoverage": {"unassessed", "uncovered", "partial", "covered", "not-applicable"},
        "foundationConcept": {"missing", "draft", "reviewed", "standard"},
        "dataVerification": {"not-run", "passed", "failed", "stale"},
        "contentImplementation": {"not-started", "working", "implemented"},
        "technicalVerification": {"not-run", "passed", "failed", "stale"},
        "subjectReview": {"not-started", "in-review", "passed", "changes-required"},
        "usageReview": {"not-started", "planned", "running", "passed", "failed", "not-applicable"},
        "classroomPilot": {"not-started", "planned", "running", "completed", "not-applicable"},
        "release": {"closed", "conditional", "released", "not-applicable"},
    }
    if not isinstance(maturity, dict):
        errors.append(f"V2-Fundamentstatus {expected_id} benötigt getrennte Reifeachsen")
    else:
        errors.extend(
            _unknown_fields(maturity, set(maturity_fields), f"Reifeachsen {expected_id}")
        )
        for field, allowed in maturity_fields.items():
            maturity_value = maturity.get(field)
            if not isinstance(maturity_value, str) or maturity_value not in allowed:
                errors.append(f"Reifeachse {field} ist ungültig in {expected_id}")

    status_requirement_ids = data.get("requirementIds")
    valid_status_requirement_ids: list[str] = []
    if not isinstance(status_requirement_ids, list) or not status_requirement_ids:
        errors.append(f"V2-Fundamentstatus {expected_id} benötigt requirementIds")
        status_requirement_ids = []
    else:
        valid_status_requirement_ids = [
            requirement_id
            for requirement_id in status_requirement_ids
            if _nonempty_string(requirement_id)
        ]
        if len(valid_status_requirement_ids) != len(status_requirement_ids):
            errors.append(
                f"V2-Fundamentstatus {expected_id} enthält eine ungültige requirementId"
            )
        if len(valid_status_requirement_ids) != len(set(valid_status_requirement_ids)):
            errors.append(f"V2-Fundamentstatus {expected_id} enthält doppelte requirementIds")
    for requirement_id in valid_status_requirement_ids:
        if requirement_id not in requirement_ids:
            errors.append(f"V2-Fundamentstatus {expected_id} referenziert unbekannte Anforderung {requirement_id}")

    evidence = data.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        errors.append(f"V2-Fundamentstatus {expected_id} benötigt Evidenz")
    else:
        for pointer in evidence:
            errors.extend(
                _validate_evidence_pointer(
                    pointer,
                    f"foundation-{expected_id}",
                    root,
                    report_warnings,
                )
            )

    open_questions = data.get("openQuestions")
    if not isinstance(open_questions, list):
        errors.append(f"V2-Fundamentstatus {expected_id} openQuestions muss eine Liste sein")
    else:
        seen_question_ids: set[str] = set()
        for question in open_questions:
            if not isinstance(question, dict):
                errors.append(f"Offene Frage in {expected_id} muss ein Objekt sein")
                continue
            errors.extend(
                _unknown_fields(
                    question,
                    {"id", "question", "owner", "risk", "disposition"},
                    f"Offene Frage in {expected_id}",
                )
            )
            question_id = question.get("id")
            if not _nonempty_string(question_id):
                errors.append(f"Offene Frage in {expected_id} benötigt eine ID")
            elif question_id in seen_question_ids:
                errors.append(f"Doppelte offene Frage {question_id} in {expected_id}")
            else:
                seen_question_ids.add(question_id)
            for field in ("question", "owner", "risk"):
                if not _nonempty_string(question.get(field)):
                    errors.append(f"Offene Frage {question_id} benötigt {field}")
            disposition = question.get("disposition")
            if not isinstance(disposition, str) or disposition not in {
                "open",
                "accepted",
                "resolved",
            }:
                errors.append(f"Offene Frage {question_id} hat ungültige disposition")
    if not _nonempty_string(data.get("nextGate")):
        errors.append(f"V2-Fundamentstatus {expected_id} benötigt nextGate")

    if expected_id == "curriculum":
        if data.get("workStatus") != "done":
            errors.append("Freigegebenes Curriculumfundament muss im Status done bleiben")
        if set(valid_status_requirement_ids) != {"V2-REQ-CUR-001", "V2-REQ-CUR-002"}:
            errors.append("Curriculumfundament muss beide CUR-Anforderungen referenzieren")
        if isinstance(maturity, dict):
            if maturity.get("curriculumCoverage") != "unassessed":
                errors.append("Curriculumfundament darf noch keine V2-Gesamtabdeckung behaupten")
            if maturity.get("dataVerification") != "passed":
                errors.append("Curriculumfundament muss die versiegelte Datenbasis verifizieren")
            if maturity.get("contentImplementation") != "not-started":
                errors.append(
                    "Curriculumfundament darf bei eingefrorener Inhaltsproduktion keine Implementierung beanspruchen"
                )
            if maturity.get("foundationConcept") != "reviewed":
                errors.append("Freigegebenes Curriculumfundament muss fachlich reviewed sein")
            if maturity.get("subjectReview") != "passed":
                errors.append("Freigegebenes Curriculumfundament muss den Fachreview bestanden haben")
            if maturity.get("release") != "closed":
                errors.append("Curriculumfundament darf keine Releasefreigabe beanspruchen")
        if data.get("nextGate") != "IUM-V2-SRC":
            errors.append("Freigegebenes Curriculumfundament muss IUM-V2-SRC als nächstes Gate führen")
    elif expected_id == "sources":
        if data.get("workStatus") != "done":
            errors.append("Freigegebenes Quellenfundament muss im Status done bleiben")
        if set(valid_status_requirement_ids) != {"V2-REQ-SRC-001"}:
            errors.append("Quellenfundament muss V2-REQ-SRC-001 referenzieren")
        if isinstance(maturity, dict):
            expected_maturity = {
                "curriculumCoverage": "not-applicable",
                "foundationConcept": "reviewed",
                "dataVerification": "passed",
                "contentImplementation": "not-started",
                "technicalVerification": "passed",
                "subjectReview": "passed",
                "usageReview": "not-applicable",
                "classroomPilot": "not-applicable",
                "release": "closed",
            }
            if maturity != expected_maturity:
                errors.append(
                    "Freigegebenes Quellenfundament muss die getrennten Reifeachsen konservativ ausweisen"
                )
        if data.get("nextGate") != "LXF01":
            errors.append("Freigegebenes Quellenfundament muss LXF01 als nächstes Gate führen")
    return errors


def validate_source_inventory(data: object, root: Path) -> list[str]:
    if not isinstance(data, dict):
        return ["V2-Quelleninventar muss ein Objekt sein"]

    errors: list[str] = []
    errors.extend(
        _unknown_fields(data, SOURCE_INVENTORY_FIELDS, "V2-Quelleninventar")
    )
    errors.extend(_missing_fields(data, SOURCE_INVENTORY_FIELDS, "V2-Quelleninventar"))
    if not _is_plain_int(data.get("schemaVersion")) or data.get("schemaVersion") != 1:
        errors.append("V2-Quelleninventar schemaVersion muss 1 sein")
    if data.get("projectId") != "ium-lernwerk":
        errors.append("V2-Quelleninventar projectId muss ium-lernwerk sein")
    if not _is_iso_date(data.get("asOf")):
        errors.append("V2-Quelleninventar asOf muss ein echtes Kalenderdatum sein")

    baseline = data.get("phase0Baseline")
    if not isinstance(baseline, dict):
        errors.append("V2-Quelleninventar benötigt eine Phase-0-Baseline")
    else:
        errors.extend(
            _unknown_fields(
                baseline,
                {"role", *PHASE0_SOURCE_BASELINE_EXPECTATIONS},
                "V2 Phase-0-Baseline",
            )
        )
        errors.extend(
            _missing_fields(
                baseline,
                {"role", *PHASE0_SOURCE_BASELINE_EXPECTATIONS},
                "V2 Phase-0-Baseline",
            )
        )
        if baseline.get("role") != "v1-audit-input":
            errors.append("V2 Phase-0-Baseline muss v1-audit-input bleiben")
        for label, expected in PHASE0_SOURCE_BASELINE_EXPECTATIONS.items():
            record = baseline.get(label)
            if not isinstance(record, dict):
                errors.append(f"V2-Quelleninventar benötigt {label}")
                continue
            errors.extend(
                _unknown_fields(
                    record,
                    {"path", "sha256", "recordCount"},
                    f"V2-Quelleninventar {label}",
                )
            )
            errors.extend(
                _missing_fields(
                    record,
                    {"path", "sha256", "recordCount"},
                    f"V2-Quelleninventar {label}",
                )
            )
            if record.get("path") != expected["path"]:
                errors.append(
                    f"V2-Quelleninventar {label} muss den versiegelten Pfad referenzieren"
                )
            if record.get("sha256") != expected["sha256"]:
                errors.append(
                    f"V2-Quelleninventar {label} muss den versiegelten Hash referenzieren"
                )
            if record.get("recordCount") != expected["recordCount"]:
                errors.append(
                    f"V2-Quelleninventar {label} muss {expected['recordCount']} Einträge ausweisen"
                )
            source_path = root / expected["path"]
            if not source_path.is_file():
                errors.append(
                    f"V2-Quelleninventar {label} Datei fehlt: {expected['path']}"
                )
                continue
            if _sha256(source_path) != record.get("sha256"):
                errors.append(
                    f"V2-Quelleninventar {label} sha256 stimmt nicht mit der Datei überein"
                )
            try:
                source_data = load_json(source_path)
            except (OSError, UnicodeError, json.JSONDecodeError):
                errors.append(
                    f"V2-Quelleninventar {label} Datei ist kein gültiges JSON"
                )
                continue
            collection = (
                source_data.get(expected["collection"])
                if isinstance(source_data, dict)
                else None
            )
            if not isinstance(collection, list) or len(collection) != record.get(
                "recordCount"
            ):
                errors.append(
                    f"V2-Quelleninventar {label} recordCount stimmt nicht mit der Datei überein"
                )

    overrides = data.get("locatorOverrides")
    lesehilfe_override: dict | None = None
    if not isinstance(overrides, list):
        errors.append("V2-Quelleninventar locatorOverrides muss eine Liste sein")
        overrides = []
    seen_override_ids: set[str] = set()
    override_fields = {"sourceId", "url", "checkedAt", "status", "reason", "evidencePath"}
    for override in overrides:
        if not isinstance(override, dict):
            errors.append("V2-Locator-Override muss ein Objekt sein")
            continue
        override_id = override.get("sourceId")
        override_label = (
            f"V2-Locator-Override {override_id}"
            if _nonempty_string(override_id)
            else "V2-Locator-Override"
        )
        errors.extend(_unknown_fields(override, override_fields, override_label))
        errors.extend(_missing_fields(override, override_fields, override_label))
        if not _nonempty_string(override_id):
            errors.append("V2-Locator-Override benötigt sourceId")
        elif override_id in seen_override_ids:
            errors.append(f"doppelter V2-Locator-Override {override_id}")
        else:
            seen_override_ids.add(override_id)
        if not _is_https_url(override.get("url")):
            errors.append(f"{override_label} benötigt url")
        if not _is_iso_date(override.get("checkedAt")):
            errors.append(f"{override_label} checkedAt muss ein echtes Kalenderdatum sein")
        if override.get("status") != "resolved":
            errors.append(f"{override_label} muss als resolved ausgewiesen sein")
        if not _nonempty_string(override.get("reason")):
            errors.append(f"{override_label} benötigt reason")
        evidence_path = override.get("evidencePath")
        if not _is_repository_relative(evidence_path) or not (
            root / evidence_path
        ).is_file():
            errors.append(f"{override_label} benötigt auflösbare Repository-Evidenz")
        if override.get("sourceId") == "SRC-CUR-LESEHILFE-2026-27":
            if lesehilfe_override is not None:
                errors.append("V2-Quelleninventar enthält den Lesehilfe-Locator doppelt")
            lesehilfe_override = override
    if lesehilfe_override is None:
        errors.append(
            "V2-Quelleninventar benötigt den aufgelösten Locator für SRC-CUR-LESEHILFE-2026-27"
        )
    else:
        expected_locator = CURRICULUM_SOURCE_EXPECTATIONS[
            "SRC-CUR-LESEHILFE-2026-27"
        ]["directUrl"]
        if lesehilfe_override.get("url") != expected_locator:
            errors.append("V2-Lesehilfe-Locator muss die geprüfte direkte Fundstelle tragen")
        if lesehilfe_override.get("status") != "resolved":
            errors.append("V2-Lesehilfe-Locator muss als resolved ausgewiesen sein")
    if seen_override_ids != {"SRC-CUR-LESEHILFE-2026-27"}:
        errors.append("V2-Quelleninventar darf nur den geprüften Lesehilfe-Locator überschreiben")

    additions = data.get("lxp01Additions")
    if not isinstance(additions, list):
        errors.append("V2-Quelleninventar lxp01Additions muss eine Liste sein")
        additions = []
    additions_by_id: dict[str, dict] = {}
    for index, addition in enumerate(additions):
        if not isinstance(addition, dict):
            errors.append(f"LXP01-Quelle an Position {index} muss ein Objekt sein")
            continue
        source_id = addition.get("sourceId")
        label = source_id if _nonempty_string(source_id) else f"<Position {index}>"
        errors.extend(
            _unknown_fields(addition, LXP01_SOURCE_FIELDS, f"LXP01-Quelle {label}")
        )
        errors.extend(
            _missing_fields(addition, LXP01_SOURCE_FIELDS, f"LXP01-Quelle {label}")
        )
        if not _nonempty_string(source_id):
            errors.append(f"LXP01-Quelle {label} benötigt sourceId")
        elif source_id in additions_by_id:
            errors.append(f"doppelte LXP01-Quellen-ID {source_id}")
        else:
            additions_by_id[source_id] = addition
        for field in ("legacyId", "title"):
            if not _nonempty_string(addition.get(field)):
                errors.append(f"LXP01-Quelle {label} benötigt {field}")
        authors = addition.get("authors")
        if not isinstance(authors, list) or not authors or not all(
            _nonempty_string(author) for author in authors
        ):
            errors.append(f"LXP01-Quelle {label} benötigt Autoren")
        source_year = addition.get("year")
        if not _is_plain_int(source_year) or not 1900 <= source_year <= 2026:
            errors.append(f"LXP01-Quelle {label} hat ein ungültiges Jahr")
        source_kind = addition.get("sourceKind")
        if not isinstance(source_kind, str) or source_kind not in {
            "meta-analysis",
            "professional-standard",
        }:
            errors.append(f"LXP01-Quelle {label} hat einen unbekannten Quellentyp")
        if not _is_https_url(addition.get("url")):
            errors.append(f"LXP01-Quelle {label} benötigt eine HTTPS-Fundstelle")
        doi = addition.get("doi")
        if doi is not None and (
            not _nonempty_string(doi) or not doi.lower().startswith("10.")
        ):
            errors.append(f"LXP01-Quelle {label} hat einen ungültigen DOI")
        verification_status = addition.get("verificationStatus")
        if not isinstance(verification_status, str) or verification_status not in {
            "metadata-checked",
            "primary-checked",
        }:
            errors.append(f"LXP01-Quelle {label} hat einen unbekannten Prüfstatus")
        license_status = addition.get("licenseStatus")
        if not isinstance(license_status, str) or license_status not in {
            "publisher-rights-no-open-license",
            "permissive-with-notice",
            "no-open-license-identified",
        }:
            errors.append(f"LXP01-Quelle {label} hat einen unbekannten Lizenzstatus")
        usage_status = addition.get("usageStatus")
        if not isinstance(usage_status, str) or usage_status not in {
            "citation-only",
            "reuse-with-notice",
            "citation-and-link-only",
        }:
            errors.append(f"LXP01-Quelle {label} hat einen unbekannten Nutzungsstatus")
        if not _is_iso_date(addition.get("accessed")):
            errors.append(
                f"LXP01-Quelle {label} accessed muss ein echtes Kalenderdatum sein"
            )
        live_check = addition.get("liveCheck")
        if not isinstance(live_check, dict):
            errors.append(f"LXP01-Quelle {label} benötigt liveCheck")
        else:
            errors.extend(
                _unknown_fields(
                    live_check,
                    {"checkedAt", "status", "httpStatus", "finalUrl"},
                    f"LXP01-liveCheck {label}",
                )
            )
            errors.extend(
                _missing_fields(
                    live_check,
                    {"checkedAt", "status", "httpStatus", "finalUrl"},
                    f"LXP01-liveCheck {label}",
                )
            )
            live_status = live_check.get("status")
            if not isinstance(live_status, str) or live_status not in {
                "resolved",
                "restricted",
            }:
                errors.append(f"LXP01-Quelle {label} ist nicht live auflösbar")
            http_status = live_check.get("httpStatus")
            if not _is_plain_int(http_status) or not 100 <= http_status <= 599:
                errors.append(
                    f"LXP01-Quelle {label} liveCheck hat ungültigen httpStatus"
                )
            if live_status == "resolved" and (
                not _is_plain_int(http_status) or not 200 <= http_status <= 299
            ):
                errors.append(
                    f"LXP01-Quelle {label} resolved benötigt terminalen 2xx-Status"
                )
            if live_status == "restricted" and (
                not _is_plain_int(http_status) or http_status not in {401, 403}
            ):
                errors.append(
                    f"LXP01-Quelle {label} restricted benötigt HTTP 401 oder 403"
                )
            if not _is_https_url(live_check.get("finalUrl")):
                errors.append(f"LXP01-Quelle {label} liveCheck benötigt finalUrl")
            if not _is_iso_date(live_check.get("checkedAt")):
                errors.append(
                    f"LXP01-Quelle {label} liveCheck checkedAt muss ein echtes Kalenderdatum sein"
                )
        if addition.get("migrationState") != "registered-v2":
            errors.append(f"LXP01-Quelle {label} muss registered-v2 sein")
        if addition.get("claimMigration") != "pending-lxf02-claim-review":
            errors.append(
                f"LXP01-Quelle {label} muss bis LXF02 ohne V2-Claim bleiben"
            )
        if addition.get("recheckTriggers") != [
            "before-claim-review",
            "before-publication",
            "locator-or-license-change",
        ]:
            errors.append(f"LXP01-Quelle {label} benötigt alle Recheck-Trigger")

    if set(additions_by_id) != set(EXPECTED_LXP01_SOURCES):
        errors.append(
            "V2-Quelleninventar muss exakt die sechs LXP01-Ergänzungen enthalten"
        )
    for source_id, expected in EXPECTED_LXP01_SOURCES.items():
        addition = additions_by_id.get(source_id)
        if addition is None:
            continue
        for field, expected_value in expected.items():
            if addition.get(field) != expected_value:
                errors.append(
                    f"LXP01-Quelle {source_id} hat einen unerwarteten Wert für {field}"
                )

    totals = data.get("totals")
    if totals != {"phase0": 63, "lxp01Additions": 6, "combined": 69}:
        errors.append("V2-Quelleninventar muss die Summen 63 + 6 = 69 ausweisen")
    return errors


def validate_source_traceability(
    data: object,
    root: Path,
    warnings: list[str] | None = None,
) -> list[str]:
    if not isinstance(data, dict):
        return ["V2-Quellenrückverfolgung muss ein Objekt sein"]

    report_warnings = warnings if warnings is not None else []
    errors: list[str] = []
    errors.extend(
        _unknown_fields(
            data,
            SOURCE_TRACEABILITY_FIELDS,
            "V2-Quellenrückverfolgung",
        )
    )
    if not _is_plain_int(data.get("schemaVersion")) or data.get("schemaVersion") != 1:
        errors.append("V2-Quellenrückverfolgung schemaVersion muss 1 sein")
    if data.get("projectId") != "ium-lernwerk":
        errors.append("V2-Quellenrückverfolgung projectId muss ium-lernwerk sein")
    if not isinstance(data.get("asOf"), str) or not DATE_PATTERN.fullmatch(
        data["asOf"]
    ):
        errors.append("V2-Quellenrückverfolgung asOf muss YYYY-MM-DD sein")
    if data.get("entityFlow") != EXPECTED_SOURCE_ENTITY_FLOW:
        errors.append(
            "V2-Quellenrückverfolgung muss alle sechs Entitätstypen getrennt halten"
        )
    if data.get("entityTypes") != EXPECTED_SOURCE_ENTITY_TYPES:
        errors.append(
            "V2-Quellenrückverfolgung enthält unerlaubte Entitätsreferenzrichtungen"
        )

    inventory_path = data.get("sourceInventoryPath")
    expected_inventory_path = "roadmap/v2/foundations/sources/inventory.json"
    if inventory_path != expected_inventory_path:
        errors.append("V2-Quellenrückverfolgung muss das V2-Quelleninventar referenzieren")
    inventory_data = _load_contract_json(
        root,
        expected_inventory_path,
        "V2-Quelleninventar",
        errors,
    )
    if inventory_data is not None:
        errors.extend(validate_source_inventory(inventory_data, root))

    claim_baseline = data.get("claimBaseline")
    expected_claim = PHASE0_SOURCE_BASELINE_EXPECTATIONS["claimLedger"]
    if not isinstance(claim_baseline, dict):
        errors.append("V2-Quellenrückverfolgung benötigt eine Claim-Baseline")
    else:
        errors.extend(
            _unknown_fields(
                claim_baseline,
                {
                    "path",
                    "sha256",
                    "claimCount",
                    "reviewedClaimCount",
                    "uniqueSourceCount",
                },
                "V2 Claim-Baseline",
            )
        )
        if claim_baseline.get("path") != expected_claim["path"]:
            errors.append("V2 Claim-Baseline muss das versiegelte Claim-Ledger referenzieren")
        if claim_baseline.get("sha256") != expected_claim["sha256"]:
            errors.append("V2 Claim-Baseline muss den versiegelten Hash referenzieren")
        expected_counts = {
            "claimCount": 51,
            "reviewedClaimCount": 51,
            "uniqueSourceCount": 57,
        }
        for field, expected_value in expected_counts.items():
            if claim_baseline.get(field) != expected_value:
                errors.append(
                    f"V2 Claim-Baseline {field} muss {expected_value} ausweisen"
                )

    if data.get("migrationRules") != EXPECTED_SOURCE_MIGRATION_RULES:
        errors.append("V2-Quellenrückverfolgung muss alle Migrationsregeln fail-closed halten")

    required_gaps = data.get("requiredGaps")
    if not isinstance(required_gaps, list):
        errors.append("V2-Quellenrückverfolgung requiredGaps muss eine Liste sein")
        required_gaps = []
    if required_gaps:
        errors.append(
            "V2-Quellenrückverfolgung darf keine offene Pflichtquellenlücke enthalten"
        )

    optional_gaps = data.get("optionalGaps")
    if not isinstance(optional_gaps, list):
        errors.append("V2-Quellenrückverfolgung optionalGaps muss eine Liste sein")
        optional_gaps = []

    for collection_name, gaps, expected_required in (
        ("Pflichtquellenlücke", required_gaps, True),
        ("optionale Quellenlücke", optional_gaps, False),
    ):
        seen_gap_ids: set[str] = set()
        for gap in gaps:
            if not isinstance(gap, dict):
                errors.append(f"{collection_name} muss ein Objekt sein")
                continue
            errors.extend(_unknown_fields(gap, SOURCE_GAP_FIELDS, collection_name))
            gap_id = gap.get("id")
            if not _nonempty_string(gap_id):
                errors.append(f"{collection_name} benötigt eine ID")
            elif gap_id in seen_gap_ids:
                errors.append(f"doppelte Quellenlücken-ID {gap_id}")
            else:
                seen_gap_ids.add(gap_id)
            for field in (
                "sourceId",
                "issue",
                "resolutionStatus",
                "ownerGate",
                "acceptanceCriterion",
            ):
                if not _nonempty_string(gap.get(field)):
                    errors.append(f"{collection_name} {gap_id} benötigt {field}")
            if gap.get("required") is not expected_required:
                errors.append(f"{collection_name} {gap_id} hat einen falschen required-Wert")

    expected_optional_gap = {
        "id": "SRC-GAP-LP-SIGNALING-2018",
        "sourceId": "SRC-LP-SIGNALING-2018",
        "required": False,
        "issue": (
            "Die Phase-0-Quelle ist nur metadatengeprüft und trägt keinen "
            "V2-Claim; LXF02 verwendet für den engeren Claim zu Text-Bild-"
            "Beziehungen stattdessen SRC-V2-LXF-SIGNAL-2016."
        ),
        "resolutionStatus": "resolved-not-migrated",
        "ownerGate": "LXF02",
        "acceptanceCriterion": (
            "SRC-LP-SIGNALING-2018 nicht in V2-Claims referenzieren und die "
            "primär geprüfte Alternative im LXF02-Quellenregister nachweisen."
        ),
    }
    if optional_gaps != [expected_optional_gap]:
        errors.append(
            "V2-Quellenrückverfolgung muss die eine optionale Phase-0-Prüflücke ausweisen"
        )

    source_register_path = root / PHASE0_SOURCE_BASELINE_EXPECTATIONS[
        "sourceRegister"
    ]["path"]
    claim_ledger_path = root / expected_claim["path"]
    if not source_register_path.is_file() or not claim_ledger_path.is_file():
        return errors
    try:
        source_register = load_json(source_register_path)
        claim_ledger = load_json(claim_ledger_path)
    except (OSError, UnicodeError, json.JSONDecodeError):
        errors.append("V2-Quellenrückverfolgung kann die Phase-0-Ledger nicht lesen")
        return errors

    phase0_sources = (
        source_register.get("sources") if isinstance(source_register, dict) else None
    )
    claims = claim_ledger.get("claims") if isinstance(claim_ledger, dict) else None
    if not isinstance(phase0_sources, list) or not isinstance(claims, list):
        errors.append("V2-Quellenrückverfolgung benötigt lesbare Phase-0-Collections")
        return errors

    sources_by_id: dict[str, dict] = {}
    for source in phase0_sources:
        if not isinstance(source, dict) or not _nonempty_string(source.get("id")):
            errors.append("Phase-0-Quelle ohne gültige ID")
            continue
        source_id = source["id"]
        if source_id in sources_by_id:
            errors.append(f"doppelte Phase-0-Quellen-ID {source_id}")
        sources_by_id[source_id] = source
    if isinstance(inventory_data, dict):
        additions = inventory_data.get("lxp01Additions")
        if isinstance(additions, list):
            for addition in additions:
                if isinstance(addition, dict) and _nonempty_string(
                    addition.get("sourceId")
                ):
                    source_id = addition["sourceId"]
                    if source_id in sources_by_id:
                        errors.append(f"V2-Quellen-ID kollidiert mit Phase 0: {source_id}")
                    sources_by_id[source_id] = addition

    reviewed_claim_count = 0
    referenced_source_ids: set[str] = set()
    seen_claim_ids: set[str] = set()
    for claim in claims:
        if not isinstance(claim, dict):
            errors.append("Phase-0-Claim muss ein Objekt sein")
            continue
        claim_id = claim.get("id")
        if not _nonempty_string(claim_id):
            errors.append("Phase-0-Claim benötigt eine ID")
            continue
        if claim_id in seen_claim_ids:
            errors.append(f"doppelte Phase-0-Claim-ID {claim_id}")
        seen_claim_ids.add(claim_id)
        if claim.get("status") != "reviewed":
            errors.append(f"Phase-0-Claim {claim_id} ist nicht reviewed")
            continue
        reviewed_claim_count += 1
        source_ids = claim.get("sourceIds")
        if not isinstance(source_ids, list) or not source_ids:
            errors.append(f"Phase-0-Claim {claim_id} benötigt registrierte Quellen")
            continue
        for source_id in source_ids:
            if not _nonempty_string(source_id) or source_id not in sources_by_id:
                errors.append(f"Phase-0-Claim {claim_id} referenziert unbekannte Quelle {source_id}")
                continue
            referenced_source_ids.add(source_id)
            if sources_by_id[source_id].get("verificationStatus") != "primary-checked":
                errors.append(
                    f"Phase-0-Claim {claim_id} referenziert nicht primär geprüfte Quelle {source_id}"
                )
    if reviewed_claim_count != 51 or len(referenced_source_ids) != 57:
        errors.append(
            "V2-Quellenrückverfolgung muss 51 reviewed Claims über 57 Quellen nachweisen"
        )
    if "SRC-LP-SIGNALING-2018" in referenced_source_ids:
        errors.append(
            "optionale Prüflücke SRC-LP-SIGNALING-2018 darf keinen reviewed Claim tragen"
        )
    return errors


def _expected_source_link_targets(
    root: Path,
    inventory: dict,
    errors: list[str],
) -> dict[str, dict[str, object]]:
    source_register = _load_contract_json(
        root,
        "docs/research/phase-0/source-register.json",
        "Phase-0-Quellenregister",
        errors,
    )
    claim_ledger = _load_contract_json(
        root,
        "docs/research/phase-0/claim-ledger.json",
        "Phase-0-Claim-Ledger",
        errors,
    )
    if not isinstance(source_register, dict) or not isinstance(claim_ledger, dict):
        return {}
    sources = source_register.get("sources")
    claims = claim_ledger.get("claims")
    if not isinstance(sources, list) or not isinstance(claims, list):
        errors.append("V2-Linkaudit benötigt lesbare Phase-0-Collections")
        return {}
    reviewed_source_ids = {
        source_id
        for claim in claims
        if isinstance(claim, dict) and claim.get("status") == "reviewed"
        for source_id in claim.get("sourceIds", [])
        if _nonempty_string(source_id)
    }
    raw_overrides = inventory.get("locatorOverrides")
    overrides_list = raw_overrides if isinstance(raw_overrides, list) else []
    overrides = {
        override.get("sourceId"): override.get("url")
        for override in overrides_list
        if isinstance(override, dict)
        and _nonempty_string(override.get("sourceId"))
        and _is_https_url(override.get("url"))
    }
    expected: dict[str, dict[str, object]] = {}
    for source in sources:
        if not isinstance(source, dict) or not _nonempty_string(source.get("id")):
            continue
        source_id = source["id"]
        if source.get("doi"):
            locator_type = "doi"
            url = f"https://doi.org/{source['doi']}"
        elif source.get("url"):
            locator_type = "url"
            url = source["url"]
        elif source_id in overrides:
            locator_type = "v2-override"
            url = overrides[source_id]
        else:
            locator_type = "missing"
            url = ""
        expected[source_id] = {
            "required": (
                source_id in reviewed_source_ids or source_id.startswith("SRC-CUR-")
            ),
            "locatorType": locator_type,
            "url": url,
        }
    additions = inventory.get("lxp01Additions")
    if isinstance(additions, list):
        for addition in additions:
            if not isinstance(addition, dict) or not _nonempty_string(
                addition.get("sourceId")
            ):
                continue
            source_id = addition["sourceId"]
            expected[source_id] = {
                "required": True,
                "locatorType": "doi" if addition.get("doi") else "url",
                "url": addition.get("url"),
            }
    return expected


def validate_source_link_audit(
    data: object,
    root: Path,
    warnings: list[str] | None = None,
) -> list[str]:
    if not isinstance(data, dict):
        return ["V2-Quellenlinkaudit muss ein Objekt sein"]

    report_warnings = warnings if warnings is not None else []
    errors: list[str] = []
    errors.extend(
        _unknown_fields(data, SOURCE_LINK_AUDIT_FIELDS, "V2-Quellenlinkaudit")
    )
    errors.extend(
        _missing_fields(data, SOURCE_LINK_AUDIT_FIELDS, "V2-Quellenlinkaudit")
    )
    if not _is_plain_int(data.get("schemaVersion")) or data.get("schemaVersion") != 1:
        errors.append("V2-Quellenlinkaudit schemaVersion muss 1 sein")
    if data.get("projectId") != "ium-lernwerk":
        errors.append("V2-Quellenlinkaudit projectId muss ium-lernwerk sein")
    generated_at = data.get("generatedAt")
    if not _is_iso_date(generated_at):
        errors.append(
            "V2-Quellenlinkaudit generatedAt muss ein echtes Kalenderdatum sein"
        )
    expected_inventory_path = "roadmap/v2/foundations/sources/inventory.json"
    if data.get("inventoryPath") != expected_inventory_path:
        errors.append("V2-Quellenlinkaudit muss das V2-Quelleninventar referenzieren")
    if data.get("policy") != EXPECTED_LINK_AUDIT_POLICY:
        errors.append("V2-Quellenlinkaudit muss die fail-closed Linkpolicy ausweisen")

    inventory = _load_contract_json(
        root,
        expected_inventory_path,
        "V2-Quelleninventar",
        errors,
    )
    if not isinstance(inventory, dict):
        return errors
    errors.extend(validate_source_inventory(inventory, root))
    expected_targets = _expected_source_link_targets(root, inventory, errors)

    checks = data.get("checks")
    if not isinstance(checks, list):
        errors.append("V2-Quellenlinkaudit checks muss eine Liste sein")
        return errors
    checks_by_id: dict[str, dict] = {}
    for index, check in enumerate(checks):
        if not isinstance(check, dict):
            errors.append(f"V2-Linkprüfung an Position {index} muss ein Objekt sein")
            continue
        source_id = check.get("sourceId")
        label = source_id if _nonempty_string(source_id) else f"<Position {index}>"
        errors.extend(
            _unknown_fields(
                check,
                {
                    "sourceId",
                    "required",
                    "locatorType",
                    "url",
                    "status",
                    "httpStatus",
                    "finalUrl",
                    "checkedAt",
                },
                f"V2-Linkprüfung {label}",
            )
        )
        check_fields = {
            "sourceId",
            "required",
            "locatorType",
            "url",
            "status",
            "httpStatus",
            "finalUrl",
            "checkedAt",
        }
        errors.extend(
            _missing_fields(check, check_fields, f"V2-Linkprüfung {label}")
        )
        if not _nonempty_string(source_id):
            errors.append(f"V2-Linkprüfung {label} benötigt sourceId")
            continue
        if source_id in checks_by_id:
            errors.append(f"doppelte V2-Linkprüfung {source_id}")
        checks_by_id[source_id] = check
        if not isinstance(check.get("required"), bool):
            errors.append(f"V2-Linkprüfung {source_id} required muss boolesch sein")
        expected = expected_targets.get(source_id)
        if expected is None:
            errors.append(f"V2-Linkaudit enthält unbekannte Quelle {source_id}")
        else:
            for field in ("required", "locatorType", "url"):
                if check.get(field) != expected[field]:
                    errors.append(
                        f"V2-Linkprüfung {source_id} hat einen unerwarteten Wert für {field}"
                    )
        status = check.get("status")
        if not isinstance(status, str) or status not in {
            "resolved",
            "restricted",
            "missing",
            "unresolved",
        }:
            errors.append(f"V2-Linkprüfung {source_id} hat unbekannten Status")
        if check.get("required") is True and (
            not isinstance(status, str) or status not in {"resolved", "restricted"}
        ):
            errors.append(
                f"V2-Linkaudit enthält nicht auflösbare Pflichtquelle {source_id}"
            )
        if check.get("required") is False and (
            not isinstance(status, str) or status not in {"resolved", "restricted"}
        ):
            report_warnings.append(
                f"optionale Quelle {source_id} ist im V2-Linkaudit nicht auflösbar"
            )
        http_status = check.get("httpStatus")
        if http_status is not None and (
            not _is_plain_int(http_status) or not 100 <= http_status <= 599
        ):
            errors.append(f"V2-Linkprüfung {source_id} hat ungültigen httpStatus")
        final_url = check.get("finalUrl")
        if final_url is not None and not _is_http_url(final_url):
            errors.append(f"V2-Linkprüfung {source_id} hat keine HTTP(S)-finalUrl")
        if isinstance(status, str) and status in {"resolved", "restricted"} and (
            not _is_plain_int(http_status)
            or not 100 <= http_status <= 599
            or not _is_http_url(final_url)
        ):
            errors.append(
                f"V2-Linkprüfung {source_id} benötigt terminale HTTP-Evidenz für {status}"
            )
        if status == "resolved" and (
            not _is_plain_int(http_status) or not 200 <= http_status <= 299
        ):
            errors.append(
                f"V2-Linkprüfung {source_id} resolved benötigt einen terminalen 2xx-Status"
            )
        if status == "restricted" and (
            not _is_plain_int(http_status) or http_status not in {401, 403}
        ):
            errors.append(
                f"V2-Linkprüfung {source_id} restricted benötigt HTTP 401 oder 403"
            )
        if status == "missing" and (
            not _is_plain_int(http_status) or http_status not in {404, 410}
        ):
            errors.append(
                f"V2-Linkprüfung {source_id} missing benötigt HTTP 404 oder 410"
            )
        if check.get("checkedAt") != generated_at:
            errors.append(f"V2-Linkprüfung {source_id} hat einen abweichenden Stichtag")

    if set(checks_by_id) != set(expected_targets):
        errors.append("V2-Quellenlinkaudit muss exakt alle 69 registrierten Quellen prüfen")

    summary = data.get("summary")
    expected_summary = {
        "total": len(checks),
        "required": sum(1 for check in checks if isinstance(check, dict) and check.get("required") is True),
        "optional": sum(1 for check in checks if isinstance(check, dict) and check.get("required") is False),
        "resolved": sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "resolved"),
        "restricted": sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "restricted"),
        "missing": sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "missing"),
        "unresolved": sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "unresolved"),
        "warnings": sum(
            1
            for check in checks
            if isinstance(check, dict)
            and check.get("required") is False
            and (
                not isinstance(check.get("status"), str)
                or check.get("status") not in {"resolved", "restricted"}
            )
        ),
    }
    if summary != expected_summary:
        errors.append("V2-Quellenlinkaudit summary stimmt nicht mit den Einzelprüfungen überein")
    if isinstance(summary, dict):
        for field in expected_summary:
            value = summary.get(field)
            if not _is_plain_int(value) or value < 0:
                errors.append(
                    f"V2-Quellenlinkaudit summary {field} muss eine nichtnegative Ganzzahl sein"
                )
    if expected_summary["total"] != 69 or expected_summary["required"] != 68 or expected_summary["optional"] != 1:
        errors.append("V2-Quellenlinkaudit muss 68 Pflicht- und eine optionale Quelle prüfen")
    return errors


def _legacy_artifact_kind(artifact_id: str) -> str | None:
    if artifact_id in EXPECTED_LP_CLAIMS:
        return "claim"
    if artifact_id in EXPECTED_PRINCIPLES:
        return "principle"
    if artifact_id in EXPECTED_LXP_SPECS:
        return "lxp-spec"
    if artifact_id == "FACH-IUM-5-7":
        return "fachprofil"
    return None


def _legacy_artifact_ref(artifact_id: str) -> str | None:
    if artifact_id in EXPECTED_LP_CLAIMS:
        return f"docs/research/phase-0/claim-ledger.json#{artifact_id}"
    if artifact_id in EXPECTED_PRINCIPLES:
        return f"docs/research/phase-0/design-principles.json#{artifact_id}"
    if artifact_id == "FACH-IUM-5-7":
        return "docs/fachprofil/ium-gymnasium-5-7.md"
    lxp_paths = {
        "LXP01": "docs/superpowers/specs/2026-08-04-ium-learning-experience-production-design.md",
        "LXP02": "docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md",
        "LXP03": "docs/superpowers/specs/2026-08-05-ium-learning-experience-reference-designs.md",
        "LXP04": "docs/superpowers/specs/2026-08-05-ium-learning-experience-design-system.md",
    }
    return lxp_paths.get(artifact_id)


def _validate_legacy_evidence_list(
    value: object,
    label: str,
    root: Path,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, list):
        return [f"{label} evidence muss eine Liste sein"]
    if not value:
        errors.append(f"{label} evidence benötigt mindestens einen Beleg")
    valid_values = [item for item in value if _nonempty_string(item)]
    if len(valid_values) != len(value):
        errors.append(f"{label} evidence enthält einen ungültigen Beleg")
    if len(set(valid_values)) != len(valid_values):
        errors.append(f"{label} evidence enthält doppelte Belege")
    for evidence in valid_values:
        if evidence.startswith(("git:", "vault:")):
            if evidence not in ALLOWED_LEGACY_EXTERNAL_EVIDENCE:
                errors.append(
                    f"{label} enthält unzulässigen externen Beleg: {evidence}"
                )
            continue
        repository_path = evidence.split("#", 1)[0]
        if not _is_repository_relative(repository_path):
            errors.append(f"{label} enthält keinen repository-relativen Beleg: {evidence}")
        elif not (root / repository_path).is_file():
            errors.append(f"{label} verweist auf fehlenden Beleg: {evidence}")
    return errors


def validate_legacy_learning_audit(data: object, root: Path) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["LXF01-Audit muss ein Objekt sein"]
    errors.extend(
        _missing_fields(data, LEGACY_LEARNING_AUDIT_FIELDS, "LXF01-Audit")
    )
    errors.extend(
        _unknown_fields(data, LEGACY_LEARNING_AUDIT_FIELDS, "LXF01-Audit")
    )
    if not _is_plain_int(data.get("schemaVersion")) or data.get("schemaVersion") != 1:
        errors.append("LXF01-Audit benötigt schemaVersion 1")
    if data.get("projectId") != "ium-lernwerk":
        errors.append("LXF01-Audit hat eine unerwartete projectId")
    if not _is_iso_date(data.get("asOf")):
        errors.append("LXF01-Audit benötigt einen ISO-Stichtag")
    if data.get("requirementIds") != ["V2-REQ-LXF-001"]:
        errors.append("LXF01-Audit muss exakt V2-REQ-LXF-001 zugeordnet sein")

    records = data.get("records")
    if not isinstance(records, list):
        errors.append("LXF01-Audit records muss eine Liste sein")
        records = []
    seen_ids: set[str] = set()
    for index, record in enumerate(records):
        label = f"LXF01-Auditdatensatz {index + 1}"
        if not isinstance(record, dict):
            errors.append(f"{label} muss ein Objekt sein")
            continue
        errors.extend(_missing_fields(record, LEGACY_AUDIT_RECORD_FIELDS, label))
        errors.extend(_unknown_fields(record, LEGACY_AUDIT_RECORD_FIELDS, label))
        artifact_id = record.get("artifactId")
        if not _nonempty_string(artifact_id):
            errors.append(f"{label} benötigt eine artifactId")
            continue
        if artifact_id in seen_ids:
            errors.append(f"LXF01-Audit enthält doppelte artifactId: {artifact_id}")
        seen_ids.add(artifact_id)
        expected_kind = _legacy_artifact_kind(artifact_id)
        if expected_kind is None:
            errors.append(f"LXF01-Audit enthält unbekanntes Pflichtartefakt: {artifact_id}")
        elif record.get("artifactKind") != expected_kind:
            errors.append(
                f"LXF01-Audit {artifact_id} hat unerwartete artifactKind"
            )
        expected_ref = _legacy_artifact_ref(artifact_id)
        if expected_ref is not None and record.get("artifactRef") != expected_ref:
            errors.append(f"LXF01-Audit {artifact_id} hat unerwartete artifactRef")
        if expected_ref is not None:
            ref_path = expected_ref.split("#", 1)[0]
            if not (root / ref_path).is_file():
                errors.append(f"LXF01-Audit {artifact_id} verweist auf fehlendes Artefakt")
        decision = record.get("decision")
        if not isinstance(decision, str) or decision not in LEGACY_DECISIONS:
            errors.append(
                f"LXF01-Audit {artifact_id} hat unbekannte Entscheidung: {decision}"
            )
        if not _nonempty_string(record.get("rationale")):
            errors.append(f"LXF01-Audit {artifact_id} benötigt eine Begründung")
        if record.get("requirementIds") != ["V2-REQ-LXF-001"]:
            errors.append(
                f"LXF01-Audit {artifact_id} muss exakt V2-REQ-LXF-001 zugeordnet sein"
            )
        evidence = record.get("evidence")
        errors.extend(
            _validate_legacy_evidence_list(
                evidence,
                f"LXF01-Audit {artifact_id}",
                root,
            )
        )
        if decision == "retain" and isinstance(evidence, list) and not evidence:
            errors.append(
                f"LXF01-Audit {artifact_id} retain benötigt mindestens einen Beleg"
            )
        successor = record.get("successorTaskId")
        if decision in {"adapt", "replace"}:
            if not isinstance(successor, str) or not re.fullmatch(r"LXF0[2-7]", successor):
                errors.append(
                    f"LXF01-Audit {artifact_id} {decision} benötigt einen successorTaskId"
                )
        elif isinstance(decision, str) and decision in LEGACY_DECISIONS and successor is not None:
            errors.append(
                f"LXF01-Audit {artifact_id} {decision} benötigt successorTaskId null"
            )
    for missing_id in sorted(EXPECTED_LEGACY_ARTIFACTS - seen_ids):
        errors.append(f"LXF01-Audit fehlt Pflichtartefakt: {missing_id}")
    if len(records) != len(EXPECTED_LEGACY_ARTIFACTS):
        errors.append("LXF01-Audit muss exakt 33 Pflichtartefakte klassifizieren")

    gaps = data.get("knownGaps")
    if not isinstance(gaps, list):
        errors.append("LXF01-Audit knownGaps muss eine Liste sein")
        gaps = []
    seen_gaps: set[str] = set()
    gap_categories = {
        "source-management",
        "evidence-contract",
        "quality-boundary",
        "implementation-specificity",
        "learner-context",
    }
    for index, gap in enumerate(gaps):
        label = f"LXF01-Lücke {index + 1}"
        if not isinstance(gap, dict):
            errors.append(f"{label} muss ein Objekt sein")
            continue
        errors.extend(_missing_fields(gap, LEGACY_AUDIT_GAP_FIELDS, label))
        errors.extend(_unknown_fields(gap, LEGACY_AUDIT_GAP_FIELDS, label))
        gap_id = gap.get("id")
        if not _nonempty_string(gap_id):
            errors.append(f"{label} benötigt eine id")
            continue
        if gap_id in seen_gaps:
            errors.append(f"LXF01-Audit enthält doppelte bekannte Lücke: {gap_id}")
        seen_gaps.add(gap_id)
        if gap_id not in EXPECTED_LEGACY_GAPS:
            errors.append(f"LXF01-Audit enthält unbekannte Lücke: {gap_id}")
        if not isinstance(gap.get("category"), str) or gap.get("category") not in gap_categories:
            errors.append(f"{label} hat eine unbekannte Kategorie")
        if not isinstance(gap.get("status"), str) or gap.get("status") not in {"open", "partially-closed"}:
            errors.append(f"{label} hat einen unbekannten Status")
        for field in ("finding", "consequence"):
            if not _nonempty_string(gap.get(field)):
                errors.append(f"{label} benötigt {field}")
        errors.extend(
            _validate_legacy_evidence_list(gap.get("evidence"), label, root)
        )
    for missing_gap in sorted(EXPECTED_LEGACY_GAPS - seen_gaps):
        errors.append(f"LXF01-Audit fehlt bekannte Lücke: {missing_gap}")
    if len(gaps) != len(EXPECTED_LEGACY_GAPS):
        errors.append("LXF01-Audit muss exakt fünf bekannte Lücken führen")

    layers = data.get("lxp05FailureLayers")
    if not isinstance(layers, list):
        errors.append("LXF01-Audit lxp05FailureLayers muss eine Liste sein")
        layers = []
    seen_layers: set[str] = set()
    for index, layer in enumerate(layers):
        label = f"LXF01-Fehlerebene {index + 1}"
        if not isinstance(layer, dict):
            errors.append(f"{label} muss ein Objekt sein")
            continue
        errors.extend(
            _missing_fields(layer, LEGACY_AUDIT_FAILURE_LAYER_FIELDS, label)
        )
        errors.extend(
            _unknown_fields(layer, LEGACY_AUDIT_FAILURE_LAYER_FIELDS, label)
        )
        layer_id = layer.get("layer")
        if not isinstance(layer_id, str) or layer_id not in EXPECTED_LXP05_FAILURE_LAYERS:
            errors.append(f"{label} hat eine unbekannte Ebene")
        elif layer_id in seen_layers:
            errors.append(f"LXF01-Audit enthält doppelte Fehlerebene: {layer_id}")
        else:
            seen_layers.add(layer_id)
        for field in ("finding", "disposition"):
            if not _nonempty_string(layer.get(field)):
                errors.append(f"{label} benötigt {field}")
        errors.extend(
            _validate_legacy_evidence_list(layer.get("evidence"), label, root)
        )
    for missing_layer in sorted(EXPECTED_LXP05_FAILURE_LAYERS - seen_layers):
        errors.append(f"LXF01-Audit fehlt Fehlerebene: {missing_layer}")
    if len(layers) != len(EXPECTED_LXP05_FAILURE_LAYERS):
        errors.append("LXF01-Audit muss exakt vier LXP05-Fehlerebenen führen")

    handoff = data.get("handoff")
    if not isinstance(handoff, dict):
        errors.append("LXF01-Audit handoff muss ein Objekt sein")
    else:
        errors.extend(
            _missing_fields(handoff, LEGACY_AUDIT_HANDOFF_FIELDS, "LXF01-Handoff")
        )
        errors.extend(
            _unknown_fields(handoff, LEGACY_AUDIT_HANDOFF_FIELDS, "LXF01-Handoff")
        )
        expected_handoff = {
            "nextTaskId": "LXF02",
            "contentProduction": "frozen",
            "lxp05": "historical-unmerged-review-candidate",
        }
        for field, expected_value in expected_handoff.items():
            if handoff.get(field) != expected_value:
                errors.append(f"LXF01-Handoff hat unerwarteten Wert für {field}")
        if not _nonempty_string(handoff.get("decisionBoundary")):
            errors.append("LXF01-Handoff benötigt eine Entscheidungsgrenze")
    return errors


def validate_legacy_learning_audit_schema(root: Path) -> list[str]:
    relative_path = Path("schemas/v2/legacy-learning-audit.schema.json")
    path = root / relative_path
    if not path.is_file():
        return [f"LXF01-Schema fehlt: {relative_path.as_posix()}"]
    try:
        schema = load_json(path)
    except (OSError, UnicodeError, json.JSONDecodeError):
        return [f"LXF01-Schema ist kein gültiges JSON: {relative_path.as_posix()}"]
    if not isinstance(schema, dict):
        return ["LXF01-Schema muss ein Objekt sein"]
    errors: list[str] = []
    canonical_schema = json.dumps(
        schema,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    if hashlib.sha256(canonical_schema).hexdigest().upper() != (
        "57D344DE15E1E19E925BDA220D08030DB43099CCCD29A98652D02ACF7704F13F"
    ):
        errors.append("LXF01-Schema weicht von der versiegelten Definition ab")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append("LXF01-Schema benötigt Draft 2020-12")
    if schema.get("$id") != (
        "https://github.com/H4R7W16/ium-lernwerk/"
        "schemas/v2/legacy-learning-audit.schema.json"
    ):
        errors.append("LXF01-Schema hat eine unerwartete $id")
    if schema.get("type") != "object" or schema.get("additionalProperties") is not False:
        errors.append("LXF01-Schema muss top-level fail-closed sein")
    if set(schema.get("required", [])) != LEGACY_LEARNING_AUDIT_FIELDS:
        errors.append("LXF01-Schema hat abweichende Pflichtfelder")
    properties = schema.get("properties")
    if not isinstance(properties, dict) or set(properties) != LEGACY_LEARNING_AUDIT_FIELDS:
        errors.append("LXF01-Schema hat abweichende Properties")
    definitions = schema.get("$defs")
    expected_definitions = {
        "auditRecord": LEGACY_AUDIT_RECORD_FIELDS,
        "knownGap": LEGACY_AUDIT_GAP_FIELDS,
        "failureLayer": LEGACY_AUDIT_FAILURE_LAYER_FIELDS,
        "handoff": LEGACY_AUDIT_HANDOFF_FIELDS,
    }
    if not isinstance(definitions, dict):
        errors.append("LXF01-Schema benötigt $defs")
        return errors
    for name, fields in expected_definitions.items():
        definition = definitions.get(name)
        if not isinstance(definition, dict):
            errors.append(f"LXF01-Schema benötigt Definition {name}")
            continue
        if definition.get("type") != "object" or definition.get("additionalProperties") is not False:
            errors.append(f"LXF01-Schema Definition {name} muss fail-closed sein")
        if set(definition.get("required", [])) != fields:
            errors.append(f"LXF01-Schema Definition {name} hat abweichende Pflichtfelder")
        definition_properties = definition.get("properties")
        if not isinstance(definition_properties, dict) or set(definition_properties) != fields:
            errors.append(f"LXF01-Schema Definition {name} hat abweichende Properties")
    return errors


def validate_legacy_learning_audit_markdown(root: Path) -> list[str]:
    path = root / "roadmap/v2/foundations/learning-experience/legacy-audit.md"
    if not path.is_file():
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return ["LXF01-Auditsynthese ist nicht als UTF-8 lesbar"]
    expected_headings = [
        "# LXF01 Bestandsaudit",
        "## Tragfähiger Bestand",
        "## Anpassungsbedürftiger Bestand",
        "## Zu ersetzende Annahmen",
        "## Nur historische Referenz",
        "## Entfallende Regeln",
        "## Querschnittliche Ursachen des LXP05-Fehlschlags",
        "## Übergabe an LXF02",
    ]
    positions = [text.find(heading) for heading in expected_headings]
    errors: list[str] = []
    for heading, position in zip(expected_headings, positions):
        if position < 0:
            errors.append(f"LXF01-Auditsynthese fehlt Überschrift: {heading}")
    present_positions = [position for position in positions if position >= 0]
    if present_positions != sorted(present_positions):
        errors.append("LXF01-Auditsynthese hat eine unerwartete Abschnittsreihenfolge")
    return errors


def validate_v2_source_register(
    data: object,
    root: Path | None = None,
) -> list[str]:
    if not isinstance(data, dict):
        return ["LXF02-Quellenregister muss ein Objekt sein"]

    errors: list[str] = []
    errors.extend(
        _unknown_fields(data, V2_SOURCE_REGISTER_FIELDS, "LXF02-Quellenregister")
    )
    errors.extend(
        _missing_fields(data, V2_SOURCE_REGISTER_FIELDS, "LXF02-Quellenregister")
    )
    if not _is_plain_int(data.get("schemaVersion")) or data.get("schemaVersion") != 1:
        errors.append("LXF02-Quellenregister schemaVersion muss 1 sein")
    if data.get("projectId") != "ium-lernwerk":
        errors.append("LXF02-Quellenregister projectId muss ium-lernwerk sein")
    if not _is_iso_date(data.get("asOf")):
        errors.append("LXF02-Quellenregister asOf muss ein echtes Kalenderdatum sein")

    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append("LXF02-Quellenregister sources dürfen nicht leer sein")
        return errors

    sources_by_id: dict[str, dict] = {}
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            errors.append(f"LXF02-Quelle an Position {index} muss ein Objekt sein")
            continue
        source_id_value = source.get("id")
        source_id = (
            source_id_value
            if _nonempty_string(source_id_value)
            else f"<Position {index}>"
        )
        label = f"LXF02-Quelle {source_id}"
        errors.extend(_unknown_fields(source, V2_SOURCE_FIELDS, label))
        errors.extend(_missing_fields(source, V2_SOURCE_FIELDS, label))
        if not _nonempty_string(source_id_value):
            errors.append(f"{label} benötigt id")
        elif not source_id_value.startswith("SRC-"):
            errors.append(f"{label} hat eine ungültige ID")
        elif source_id_value in sources_by_id:
            errors.append(f"LXF02-Quellenregister enthält doppelte ID {source_id_value}")
        else:
            sources_by_id[source_id_value] = source

        if not _nonempty_string(source.get("title")):
            errors.append(f"{label} benötigt title")
        authors = source.get("authors")
        if not isinstance(authors, list) or not authors or not all(
            _nonempty_string(author) for author in authors
        ):
            errors.append(f"{label} authors dürfen nicht leer sein")
        elif len(authors) != len(set(authors)):
            errors.append(f"{label} authors dürfen keine Duplikate enthalten")
        year = source.get("year")
        if not _is_plain_int(year) or not 1900 <= year <= 2026:
            errors.append(f"{label} year muss zwischen 1900 und 2026 liegen")
        source_kind = source.get("sourceKind")
        if not isinstance(source_kind, str) or source_kind not in V2_SOURCE_KINDS:
            errors.append(f"{label} hat unbekannten sourceKind: {source_kind}")
        url = source.get("url")
        if not _is_https_url(url):
            errors.append(f"{label} benötigt eine HTTPS-url")
        doi = source.get("doi")
        if doi is not None and (
            not _nonempty_string(doi) or not str(doi).startswith("10.")
        ):
            errors.append(f"{label} doi muss null oder eine DOI sein")
        if _nonempty_string(doi) and url != f"https://doi.org/{doi}":
            errors.append(f"{label} DOI und url stimmen nicht überein")
        if not _is_iso_date(source.get("accessed")):
            errors.append(f"{label} accessed muss ein echtes Kalenderdatum sein")
        verification = source.get("verificationStatus")
        if (
            not isinstance(verification, str)
            or verification not in V2_SOURCE_VERIFICATION_STATUSES
        ):
            errors.append(
                f"{label} hat unbekannten verificationStatus: {verification}"
            )
        for field in ("licenseStatus", "usageStatus"):
            if not _nonempty_string(source.get(field)):
                errors.append(f"{label} benötigt {field}")
        relevance = source.get("relevance")
        if not isinstance(relevance, list) or not relevance or not all(
            _nonempty_string(item) for item in relevance
        ):
            errors.append(f"{label} relevance darf nicht leer sein")
        elif len(relevance) != len(set(relevance)):
            errors.append(f"{label} relevance darf keine Duplikate enthalten")
        update_risk = source.get("updateRisk")
        if not isinstance(update_risk, str) or update_risk not in V2_SOURCE_UPDATE_RISKS:
            errors.append(f"{label} hat unbekanntes updateRisk: {update_risk}")

    if set(sources_by_id) != EXPECTED_LXF02_SOURCE_IDS:
        missing = sorted(EXPECTED_LXF02_SOURCE_IDS - set(sources_by_id))
        unexpected = sorted(set(sources_by_id) - EXPECTED_LXF02_SOURCE_IDS)
        if missing:
            errors.append(
                "LXF02-Quellenregister fehlt erwartete Quelle: " + ", ".join(missing)
            )
        if unexpected:
            errors.append(
                "LXF02-Quellenregister enthält unerwartete Quelle: "
                + ", ".join(unexpected)
            )

    for source_id, expected in EXPECTED_LXF02_ADDITIONAL_SOURCE_METADATA.items():
        source = sources_by_id.get(source_id)
        if source is None:
            continue
        for field, expected_value in expected.items():
            if source.get(field) != expected_value:
                errors.append(
                    f"LXF02-Quelle {source_id} hat einen unerwarteten Wert für {field}"
                )

    if root is not None:
        phase0_path = root / "docs/research/phase-0/source-register.json"
        if not phase0_path.is_file():
            errors.append("LXF02-Quellenregister kann Phase-0-Quellen nicht abgleichen")
        else:
            try:
                phase0 = load_json(phase0_path)
            except (OSError, UnicodeError, json.JSONDecodeError):
                errors.append("LXF02-Quellenregister kann Phase-0-Quellen nicht lesen")
            else:
                phase0_sources = (
                    phase0.get("sources") if isinstance(phase0, dict) else None
                )
                phase0_by_id = {
                    item["id"]: item
                    for item in phase0_sources or []
                    if isinstance(item, dict) and _nonempty_string(item.get("id"))
                }
                legacy_source_ids = EXPECTED_LXF02_SOURCE_IDS - set(
                    EXPECTED_LXF02_ADDITIONAL_SOURCE_METADATA
                )
                for source_id in sorted(legacy_source_ids):
                    normalized = sources_by_id.get(source_id)
                    original = phase0_by_id.get(source_id)
                    if normalized is None or original is None:
                        errors.append(
                            f"LXF02-Quellenregister kann {source_id} nicht auf Phase 0 zurückführen"
                        )
                        continue
                    for field in (
                        "title",
                        "authors",
                        "year",
                        "sourceKind",
                        "url",
                        "doi",
                        "verificationStatus",
                    ):
                        if normalized.get(field) != original.get(field):
                            errors.append(
                                f"LXF02-Quelle {source_id} weicht in {field} von Phase 0 ab"
                            )
    return errors


def validate_learning_evidence_register(
    data: object,
    source_register: object,
) -> list[str]:
    if not isinstance(data, dict):
        return ["LXF02-Evidenzregister muss ein Objekt sein"]

    errors: list[str] = []
    errors.extend(
        _unknown_fields(
            data, LEARNING_EVIDENCE_REGISTER_FIELDS, "LXF02-Evidenzregister"
        )
    )
    errors.extend(
        _missing_fields(
            data, LEARNING_EVIDENCE_REGISTER_FIELDS, "LXF02-Evidenzregister"
        )
    )
    if not _is_plain_int(data.get("schemaVersion")) or data.get("schemaVersion") != 1:
        errors.append("LXF02-Evidenzregister schemaVersion muss 1 sein")
    if not _is_iso_date(data.get("asOf")):
        errors.append("LXF02-Evidenzregister asOf muss ein echtes Kalenderdatum sein")

    raw_sources = (
        source_register.get("sources")
        if isinstance(source_register, dict)
        else None
    )
    if not isinstance(raw_sources, list):
        errors.append("LXF02-Evidenzregister benötigt eine Quellenliste")
        raw_sources = []
    sources_by_id = {
        source["id"]: source
        for source in raw_sources
        if isinstance(source, dict) and _nonempty_string(source.get("id"))
    }
    if not sources_by_id:
        errors.append("LXF02-Evidenzregister benötigt ein lesbares Quellenregister")

    claims = data.get("claims")
    if not isinstance(claims, list) or not claims:
        errors.append("LXF02-Evidenzregister claims dürfen nicht leer sein")
        return errors

    claims_by_id: dict[str, dict] = {}
    referenced_source_ids: set[str] = set()
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            errors.append(f"LXF02-Claim an Position {index} muss ein Objekt sein")
            continue
        claim_id_value = claim.get("id")
        claim_id = (
            claim_id_value
            if _nonempty_string(claim_id_value)
            else f"<Position {index}>"
        )
        label = f"LXF02-Claim {claim_id}"
        errors.extend(_unknown_fields(claim, LEARNING_EVIDENCE_CLAIM_FIELDS, label))
        errors.extend(_missing_fields(claim, LEARNING_EVIDENCE_CLAIM_FIELDS, label))
        if not _nonempty_string(claim_id_value):
            errors.append(f"{label} benötigt id")
        elif not re.fullmatch(r"CLAIM-[A-Z0-9-]+", claim_id_value):
            errors.append(f"{label} hat eine ungültige ID")
        elif claim_id_value in claims_by_id:
            errors.append(f"LXF02-Evidenzregister enthält doppelte ID {claim_id_value}")
        else:
            claims_by_id[claim_id_value] = claim

        for field in ("statement", "mechanism", "scope", "learnerContext"):
            if not _nonempty_string(claim.get(field)):
                errors.append(f"{label} benötigt {field}")

        boundaries = claim.get("boundaryConditions")
        if not isinstance(boundaries, list) or not boundaries:
            errors.append(
                f"{label} boundaryConditions benötigt mindestens einen Eintrag"
            )
        elif not all(_nonempty_string(boundary) for boundary in boundaries):
            errors.append(f"{label} boundaryConditions enthält einen leeren Eintrag")
        elif len(boundaries) != len(set(boundaries)):
            errors.append(f"{label} boundaryConditions enthält Duplikate")

        source_ids = claim.get("sourceIds")
        if not isinstance(source_ids, list) or not source_ids:
            errors.append(f"{label} sourceIds benötigt mindestens einen Eintrag")
            source_ids = []
        elif not all(_nonempty_string(source_id) for source_id in source_ids):
            errors.append(f"{label} sourceIds enthält eine leere ID")
        elif len(source_ids) != len(set(source_ids)):
            errors.append(f"{label} sourceIds enthält Duplikate")

        source_kinds: set[str] = set()
        for source_id in source_ids:
            if not _nonempty_string(source_id):
                continue
            source = sources_by_id.get(source_id)
            if source is None:
                errors.append(f"{label} referenziert unbekannte Quelle {source_id}")
                continue
            referenced_source_ids.add(source_id)
            source_kind = source.get("sourceKind")
            if isinstance(source_kind, str):
                source_kinds.add(source_kind)
            if (
                claim.get("status") == "reviewed"
                and source.get("verificationStatus") != "primary-checked"
            ):
                errors.append(
                    f"{label} darf mit nicht primär geprüfter Quelle {source_id} nicht reviewed sein"
                )

        evidence_level = claim.get("evidenceLevel")
        if (
            not isinstance(evidence_level, str)
            or evidence_level not in LEARNING_EVIDENCE_LEVELS
        ):
            errors.append(f"{label} hat unbekanntes evidenceLevel: {evidence_level}")
        if evidence_level == "high" and source_kinds & PROFESSIONAL_SOURCE_KINDS:
            errors.append(
                f"{label} darf professionelle Standards nicht als hohe kausale Lerneffekt-Evidenz führen"
            )
        if evidence_level == "normative" and "professional-standard" not in source_kinds:
            errors.append(
                f"{label} benötigt für evidenceLevel normative einen professionellen Standard"
            )

        status = claim.get("status")
        if not isinstance(status, str) or status not in LEARNING_EVIDENCE_STATUSES:
            errors.append(f"{label} hat unbekannten status: {status}")
        elif status == "standard":
            errors.append(f"{label} darf vor LXF07 nicht standard sein")

    if set(sources_by_id) == EXPECTED_LXF02_SOURCE_IDS:
        missing_legacy_claims = sorted(EXPECTED_LP_CLAIMS - set(claims_by_id))
        for claim_id in missing_legacy_claims:
            errors.append(f"LXF02-Evidenzregister fehlt adaptierter Claim {claim_id}")
        unreferenced = sorted(set(sources_by_id) - referenced_source_ids)
        if unreferenced:
            errors.append(
                "LXF02-Evidenzregister lässt registrierte Quellen ohne Claim: "
                + ", ".join(unreferenced)
            )
    return errors


def validate_learning_evidence_schema(root: Path) -> list[str]:
    relative_path = Path("schemas/v2/learning-evidence.schema.json")
    path = root / relative_path
    if not path.is_file():
        return [f"LXF02-Schema fehlt: {relative_path.as_posix()}"]
    try:
        schema = load_json(path)
    except (OSError, UnicodeError, json.JSONDecodeError):
        return [f"LXF02-Schema ist kein gültiges JSON: {relative_path.as_posix()}"]
    if not isinstance(schema, dict):
        return ["LXF02-Schema muss ein Objekt sein"]

    errors: list[str] = []
    canonical_schema = json.dumps(
        schema,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    if hashlib.sha256(canonical_schema).hexdigest().upper() != (
        "86B91090C4598C09C1D51F1D865E37111F0818CCD0A9E42927F673F1DF6F05C3"
    ):
        return ["LXF02-Schema weicht von der versiegelten Definition ab"]
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append("LXF02-Schema benötigt Draft 2020-12")
    if schema.get("$id") != (
        "https://github.com/H4R7W16/ium-lernwerk/"
        "schemas/v2/learning-evidence.schema.json"
    ):
        errors.append("LXF02-Schema hat eine unerwartete $id")
    if schema.get("type") != "object" or schema.get("additionalProperties") is not False:
        errors.append("LXF02-Schema muss top-level fail-closed sein")
    if set(schema.get("required", [])) != LEARNING_EVIDENCE_REGISTER_FIELDS:
        errors.append("LXF02-Schema hat abweichende Pflichtfelder")
    properties = schema.get("properties")
    if not isinstance(properties, dict) or set(properties) != LEARNING_EVIDENCE_REGISTER_FIELDS:
        errors.append("LXF02-Schema hat abweichende Properties")
    claim = schema.get("$defs", {}).get("claim")
    if not isinstance(claim, dict):
        errors.append("LXF02-Schema benötigt Definition claim")
        return errors
    if claim.get("type") != "object" or claim.get("additionalProperties") is not False:
        errors.append("LXF02-Schema Claim muss fail-closed sein")
    if set(claim.get("required", [])) != LEARNING_EVIDENCE_CLAIM_FIELDS:
        errors.append("LXF02-Schema Claim hat abweichende Pflichtfelder")
    claim_properties = claim.get("properties")
    if not isinstance(claim_properties, dict) or set(claim_properties) != LEARNING_EVIDENCE_CLAIM_FIELDS:
        errors.append("LXF02-Schema Claim hat abweichende Properties")
        return errors
    if claim_properties.get("status", {}).get("enum") != [
        "draft",
        "working",
        "reviewed",
        "standard",
    ]:
        errors.append("LXF02-Schema Claim hat abweichende Statuswerte")
    if claim_properties.get("evidenceLevel", {}).get("enum") != [
        "low",
        "medium",
        "high",
        "normative",
    ]:
        errors.append("LXF02-Schema Claim hat abweichende Evidenzstufen")
    for field in ("boundaryConditions", "sourceIds"):
        if claim_properties.get(field, {}).get("minItems") != 1:
            errors.append(f"LXF02-Schema Claim {field} muss nicht leer sein")
    return errors


def validate_learning_evidence_synthesis(root: Path) -> list[str]:
    path = root / "roadmap/v2/foundations/learning-experience/evidence-synthesis.md"
    if not path.is_file():
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return ["LXF02-Evidenzsynthese ist nicht als UTF-8 lesbar"]
    headings = [
        "# LXF02 Evidenzsynthese",
        "## Lernarchitektur",
        "## Kognitive Belastung und Multimedia",
        "## Aktivierung und Aufgabenqualität",
        "## Unterstützung und Erklärung",
        "## Übung und Transfer",
        "## Feedback und Metakognition",
        "## Motivation und Agency",
        "## Inklusion und Accessibility",
        "## Digitale Interaktion",
        "## Orchestrierung",
        "## Fachspezifische Grenzen",
    ]
    positions = [text.find(heading) for heading in headings]
    errors: list[str] = []
    for heading, position in zip(headings, positions):
        if position < 0:
            errors.append(f"LXF02-Evidenzsynthese fehlt Überschrift: {heading}")
    present = [position for position in positions if position >= 0]
    if present != sorted(present):
        errors.append("LXF02-Evidenzsynthese hat eine unerwartete Abschnittsreihenfolge")
    for heading, position in zip(headings[1:], positions[1:]):
        if position < 0:
            continue
        content_start = position + len(heading)
        next_heading = re.search(r"(?m)^## ", text[content_start:])
        content_end = (
            content_start + next_heading.start()
            if next_heading is not None
            else len(text)
        )
        content = text[content_start:content_end]
        if len(re.findall(r"\b[\wÄÖÜäöüß-]+\b", content)) < 20:
            errors.append(
                "LXF02-Evidenzsynthese Abschnitt ohne substantiellen Inhalt: "
                f"{heading}"
            )
    return errors


def _validate_lxf03_grades(value: object, label: str) -> tuple[list[str], list[int]]:
    errors: list[str] = []
    if not isinstance(value, list) or not value:
        return [f"{label} benötigt grades"], []
    valid: list[int] = []
    for grade in value:
        if not _is_plain_int(grade) or grade not in REQUIREMENT_GRADES:
            errors.append(f"{label} grades enthält unzulässige Jahrgangsstufe {grade}")
        else:
            valid.append(grade)
    if len(valid) != len(set(valid)):
        errors.append(f"{label} grades enthält Duplikate")
    return errors, valid


def _validate_lxf03_string_list(
    value: object,
    label: str,
    field: str,
) -> tuple[list[str], list[str]]:
    if not isinstance(value, list) or not value:
        return [f"{label} benötigt {field}"], []
    valid = [item for item in value if _nonempty_string(item)]
    errors: list[str] = []
    if len(valid) != len(value):
        errors.append(f"{label} {field} enthält einen leeren Eintrag")
    if len(valid) != len(set(valid)):
        errors.append(f"{label} {field} enthält Duplikate")
    return errors, valid


def _validate_lxf03_profile_text(
    value: object,
    label: str,
    *,
    allow_behavioral_boundary: bool = False,
    allow_help_use_label: bool = False,
) -> list[str]:
    if not _nonempty_string(value):
        return []

    errors: list[str] = []
    sentences = re.split(r"(?<=[.!?])\s+|[\r\n]+", value.casefold())
    stable_patterns = (
        re.compile(
            r"\b(?:ist|sind|bleibt|bleiben|gelten als)\b[^.!?]{0,80}"
            r"\b(?:defizitär\w*|unfähig\w*|unmotiviert\w*|lernschwach\w*)\b"
        ),
        re.compile(
            r"\b(?:hat|haben|besitzt|besitzen)\b[^.!?]{0,80}\bdefizit\w*\b"
        ),
        re.compile(
            r"\b(?:defizitär\w*|unfähig\w*|unmotiviert\w*|lernschwach\w*)\b"
            r"[^.!?]{0,40}\b(?:lernende|schüler\w*)\b"
        ),
        re.compile(
            r"\b(?:durchschnittslern\w*|averagelearner|digital natives?|lernertyp\w*)\b"
        ),
    )
    telemetry_pattern = re.compile(
        r"\b(?:(?!klickschritt\w*\b)[\w-]*(?:klick|click)[\w-]*|"
        r"[\w-]*(?:telemetrie|bearbeitungs(?:zeit|dauer)|hilfenutzung|"
        r"systemdaten|aktivitätsmess|nutzungsdaten|tracking)[\w-]*)\b"
    )
    negation_pattern = re.compile(
        r"\b(?:nicht|nie|niemals|keineswegs|kein|keine|keinen|keinem|keiner)\b"
    )
    clause_boundary_pattern = re.compile(
        r"[,;:]|\b(?:aber|doch|während|hingegen|sondern|und)\b"
    )

    def clause_bounds(sentence: str, start: int, end: int) -> tuple[int, int]:
        before = [
            match
            for match in clause_boundary_pattern.finditer(sentence)
            if match.end() <= start
        ]
        after = [
            match
            for match in clause_boundary_pattern.finditer(sentence)
            if match.start() >= end
        ]
        clause_start = before[-1].end() if before else 0
        clause_end = after[0].start() if after else len(sentence)
        return clause_start, clause_end

    def clause_context(sentence: str, start: int, end: int) -> str:
        clause_start, clause_end = clause_bounds(sentence, start, end)
        return sentence[clause_start:clause_end]

    def is_locally_negated(context: str) -> bool:
        without_non_negating_phrases = re.sub(
            r"\bnicht\s+(?:nur|alle)\b", "", context
        )
        return bool(negation_pattern.search(without_non_negating_phrases))

    for sentence in sentences:
        if not sentence.strip():
            continue
        stable_label_found = False
        for pattern in stable_patterns:
            for match in pattern.finditer(sentence):
                local_context = clause_context(sentence, match.start(), match.end())
                if not is_locally_negated(local_context):
                    errors.append(
                        f"{label} enthält unzulässiges stabiles Defizitlabel"
                    )
                    stable_label_found = True
                    break
            if stable_label_found:
                break

        if telemetry_pattern.search(sentence):
            allowed_boundary = (
                allow_behavioral_boundary
                and value.strip() == LEARNER_PROFILE_BEHAVIORAL_BOUNDARY
            )
            allowed_label = (
                allow_help_use_label
                and value.strip() == LEARNER_PROFILE_HELP_USE_LABEL
            )
            if not allowed_boundary and not allowed_label:
                errors.append(
                    f"{label} enthält unzulässige Klickzeit-Inferenz oder "
                    "Telemetrieformulierung"
                )
                break
    return errors


def _learner_profile_reference_indexes(
    root: Path,
    errors: list[str],
) -> tuple[dict[str, dict], set[str]]:
    curriculum = _curriculum_record_index(root, errors)
    requirements_path = root / "roadmap/v2/requirements/requirements.json"
    requirement_ids: set[str] = set()
    if not requirements_path.is_file():
        errors.append("LXF03-Profil kann V2-Anforderungen nicht abgleichen")
        return curriculum, requirement_ids
    try:
        requirements = load_json(requirements_path)
    except (OSError, UnicodeError, json.JSONDecodeError):
        errors.append("LXF03-Profil kann V2-Anforderungen nicht lesen")
        return curriculum, requirement_ids
    raw_requirements = (
        requirements.get("requirements") if isinstance(requirements, dict) else None
    )
    if not isinstance(raw_requirements, list):
        errors.append("LXF03-Profil benötigt ein lesbares V2-Anforderungsregister")
        return curriculum, requirement_ids
    requirement_ids = {
        requirement["id"]
        for requirement in raw_requirements
        if isinstance(requirement, dict)
        and _nonempty_string(requirement.get("id"))
    }
    return curriculum, requirement_ids


def validate_learner_profile(
    data: object,
    evidence_register: object,
    root: Path,
) -> list[str]:
    if not isinstance(data, dict):
        return ["LXF03-Profil muss ein Objekt sein"]

    errors: list[str] = []
    if "averageLearner" in data:
        errors.append(
            "LXF03-Profil darf keinen undifferenzierten averageLearner enthalten"
        )
    errors.extend(_unknown_fields(data, LEARNER_PROFILE_FIELDS, "LXF03-Profil"))
    errors.extend(_missing_fields(data, LEARNER_PROFILE_FIELDS, "LXF03-Profil"))
    if not _is_plain_int(data.get("schemaVersion")) or data.get("schemaVersion") != 1:
        errors.append("LXF03-Profil schemaVersion muss 1 sein")
    if data.get("projectId") != "ium-lernwerk":
        errors.append("LXF03-Profil projectId muss ium-lernwerk sein")
    if not _is_iso_date(data.get("asOf")):
        errors.append("LXF03-Profil asOf muss ein echtes Kalenderdatum sein")

    scope = data.get("scope")
    if not isinstance(scope, dict):
        errors.append("LXF03-Profil benötigt scope")
    else:
        errors.extend(_unknown_fields(scope, LEARNER_PROFILE_SCOPE_FIELDS, "LXF03-Scope"))
        errors.extend(_missing_fields(scope, LEARNER_PROFILE_SCOPE_FIELDS, "LXF03-Scope"))
        scope_errors, scope_grades = _validate_lxf03_grades(
            scope.get("grades"), "LXF03-Scope"
        )
        errors.extend(scope_errors)
        if set(scope_grades) != REQUIREMENT_GRADES:
            errors.append("LXF03-Scope muss genau die Klassen 5, 6 und 7 umfassen")
        fixed_scope = {
            "profileType": "planning-profile",
            "schoolType": "Gymnasium Baden-Württemberg",
            "level": "E",
            "individualDiagnosis": "prohibited",
            "maturity": "working",
        }
        for field, expected in fixed_scope.items():
            if scope.get(field) != expected:
                errors.append(f"LXF03-Scope {field} muss {expected} sein")
        boundary_errors, boundaries = _validate_lxf03_string_list(
            scope.get("statementBoundaries"),
            "LXF03-Scope",
            "statementBoundaries",
        )
        errors.extend(boundary_errors)
        if boundaries and len(boundaries) < 2:
            errors.append("LXF03-Scope benötigt mindestens zwei Aussagegrenzen")
        if LEARNER_PROFILE_BEHAVIORAL_BOUNDARY not in boundaries:
            errors.append(
                "LXF03-Scope benötigt die versiegelte Anti-Telemetrie-Grenze"
            )
        for index, boundary in enumerate(boundaries):
            errors.extend(
                _validate_lxf03_profile_text(
                    boundary,
                    f"LXF03-Scope Aussagegrenze {index + 1}",
                    allow_behavioral_boundary=True,
                )
            )

    raw_claims = (
        evidence_register.get("claims")
        if isinstance(evidence_register, dict)
        else None
    )
    if not isinstance(raw_claims, list):
        errors.append("LXF03-Profil benötigt ein lesbares Evidenzregister")
        raw_claims = []
    known_claim_ids = {
        claim["id"]
        for claim in raw_claims
        if isinstance(claim, dict) and _nonempty_string(claim.get("id"))
    }
    curriculum_records, requirement_ids = _learner_profile_reference_indexes(
        root, errors
    )

    dimensions = data.get("dimensions")
    if not isinstance(dimensions, list) or not dimensions:
        errors.append("LXF03-Profil dimensions dürfen nicht leer sein")
        return errors

    dimensions_by_id: dict[str, dict] = {}
    record_ids: set[str] = set()
    for position, dimension in enumerate(dimensions):
        if not isinstance(dimension, dict):
            errors.append(f"LXF03-Dimension an Position {position} muss ein Objekt sein")
            continue
        dimension_id_value = dimension.get("id")
        dimension_id = (
            dimension_id_value
            if _nonempty_string(dimension_id_value)
            else f"<Position {position}>"
        )
        label = f"LXF03-Dimension {dimension_id}"
        errors.extend(_unknown_fields(dimension, LEARNER_PROFILE_DIMENSION_FIELDS, label))
        errors.extend(_missing_fields(dimension, LEARNER_PROFILE_DIMENSION_FIELDS, label))
        if not _nonempty_string(dimension_id_value):
            errors.append(f"{label} benötigt id")
        elif dimension_id_value in dimensions_by_id:
            errors.append(f"LXF03-Profil enthält doppelte Dimension {dimension_id_value}")
        else:
            dimensions_by_id[dimension_id_value] = dimension
        if not _nonempty_string(dimension.get("label")):
            errors.append(f"{label} benötigt label")
        else:
            errors.extend(
                _validate_lxf03_profile_text(
                    dimension.get("label"),
                    f"{label} label",
                    allow_help_use_label=True,
                )
            )

        assumptions = dimension.get("evidenceSupportedAssumptions")
        if not isinstance(assumptions, list) or not assumptions:
            errors.append(f"{label} benötigt evidenceSupportedAssumptions")
            assumptions = []
        for index, statement in enumerate(assumptions):
            if not isinstance(statement, dict):
                errors.append(f"{label} Profilstatement {index} muss ein Objekt sein")
                continue
            statement_id_value = statement.get("id")
            statement_id = (
                statement_id_value
                if _nonempty_string(statement_id_value)
                else f"<Position {index}>"
            )
            statement_label = f"LXF03-Profilstatement {statement_id}"
            errors.extend(
                _unknown_fields(
                    statement, LEARNER_PROFILE_STATEMENT_FIELDS, statement_label
                )
            )
            for field in sorted(LEARNER_PROFILE_STATEMENT_FIELDS - set(statement)):
                errors.append(f"{statement_label} benötigt {field}")
            if not _nonempty_string(statement_id_value):
                errors.append(f"{statement_label} benötigt id")
            elif not re.fullmatch(r"LXF03-S-[0-9]{3}", statement_id_value):
                errors.append(f"{statement_label} hat eine ungültige ID")
            elif statement_id_value in record_ids:
                errors.append(f"LXF03-Profil enthält doppelte ID {statement_id_value}")
            else:
                record_ids.add(statement_id_value)
            statement_text = statement.get("statement")
            if not _nonempty_string(statement_text):
                errors.append(f"{statement_label} benötigt statement")
            else:
                errors.extend(
                    _validate_lxf03_profile_text(statement_text, statement_label)
                )
            claim_errors, claim_ids = _validate_lxf03_string_list(
                statement.get("claimIds"), statement_label, "claimIds"
            )
            errors.extend(claim_errors)
            for claim_id in claim_ids:
                if claim_id not in known_claim_ids:
                    errors.append(
                        f"{statement_label} referenziert unbekannten Claim {claim_id}"
                    )
            grade_errors, _grades = _validate_lxf03_grades(
                statement.get("grades"), statement_label
            )
            errors.extend(grade_errors)
            if not _nonempty_string(statement.get("variability")):
                errors.append(f"{statement_label} benötigt variability")
            else:
                errors.extend(
                    _validate_lxf03_profile_text(
                        statement.get("variability"),
                        f"{statement_label} variability",
                    )
                )
            consequence = statement.get("designConsequence")
            if not isinstance(consequence, dict):
                errors.append(f"{statement_label} benötigt designConsequence")
            else:
                errors.extend(
                    _unknown_fields(
                        consequence,
                        LEARNER_PROFILE_CONSEQUENCE_FIELDS,
                        f"{statement_label} designConsequence",
                    )
                )
                for field in sorted(
                    LEARNER_PROFILE_CONSEQUENCE_FIELDS - set(consequence)
                ):
                    errors.append(
                        f"{statement_label} designConsequence benötigt {field}"
                    )
                for field in LEARNER_PROFILE_CONSEQUENCE_FIELDS:
                    if field in consequence and not _nonempty_string(
                        consequence.get(field)
                    ):
                        errors.append(
                            f"{statement_label} designConsequence {field} darf nicht leer sein"
                        )
                    elif field in consequence:
                        errors.extend(
                            _validate_lxf03_profile_text(
                                consequence.get(field),
                                f"{statement_label} designConsequence {field}",
                            )
                        )
            status = statement.get("status")
            if not isinstance(status, str) or status not in LEARNER_PROFILE_STATUSES:
                errors.append(f"{statement_label} hat unbekannten status: {status}")
            elif status == "standard":
                errors.append(f"{statement_label} darf vor LXF07 nicht standard sein")
            limitation_errors, _limitations = _validate_lxf03_string_list(
                statement.get("limitations"), statement_label, "limitations"
            )
            errors.extend(limitation_errors)
            for limitation in _limitations:
                errors.extend(
                    _validate_lxf03_profile_text(
                        limitation, f"{statement_label} limitation"
                    )
                )

        expectations = dimension.get("curriculumAndProjectExpectations")
        if not isinstance(expectations, list) or not expectations:
            errors.append(f"{label} benötigt curriculumAndProjectExpectations")
            expectations = []
        for index, expectation in enumerate(expectations):
            if not isinstance(expectation, dict):
                errors.append(f"{label} Erwartung {index} muss ein Objekt sein")
                continue
            expectation_id_value = expectation.get("id")
            expectation_id = (
                expectation_id_value
                if _nonempty_string(expectation_id_value)
                else f"<Position {index}>"
            )
            expectation_label = f"LXF03-Erwartung {expectation_id}"
            errors.extend(
                _unknown_fields(
                    expectation, LEARNER_PROFILE_EXPECTATION_FIELDS, expectation_label
                )
            )
            for field in sorted(LEARNER_PROFILE_EXPECTATION_FIELDS - set(expectation)):
                errors.append(f"{expectation_label} benötigt {field}")
            if not _nonempty_string(expectation_id_value):
                errors.append(f"{expectation_label} benötigt id")
            elif not re.fullmatch(r"LXF03-E-[0-9]{3}", expectation_id_value):
                errors.append(f"{expectation_label} hat eine ungültige ID")
            elif expectation_id_value in record_ids:
                errors.append(f"LXF03-Profil enthält doppelte ID {expectation_id_value}")
            else:
                record_ids.add(expectation_id_value)
            if not _nonempty_string(expectation.get("statement")):
                errors.append(f"{expectation_label} benötigt statement")
            else:
                errors.extend(
                    _validate_lxf03_profile_text(
                        expectation.get("statement"), expectation_label
                    )
                )
            basis = expectation.get("basis")
            if not isinstance(basis, str) or basis not in LEARNER_PROFILE_EXPECTATION_BASES:
                errors.append(f"{expectation_label} hat unbekannte basis: {basis}")
            grade_errors, expectation_grades = _validate_lxf03_grades(
                expectation.get("grades"), expectation_label
            )
            errors.extend(grade_errors)
            reference_errors, reference_ids = _validate_lxf03_string_list(
                expectation.get("referenceIds"), expectation_label, "referenceIds"
            )
            errors.extend(reference_errors)
            for reference_id in reference_ids:
                if basis == "project-decision":
                    if reference_id not in requirement_ids:
                        errors.append(
                            f"{expectation_label} referenziert unbekannte V2-Anforderung {reference_id}"
                        )
                    continue
                record = curriculum_records.get(reference_id)
                if record is None:
                    errors.append(
                        f"{expectation_label} referenziert unbekannten Curriculumrecord {reference_id}"
                    )
                    continue
                source_id = record.get("sourceId")
                if basis == "official-curriculum" and source_id == "SRC-CUR-LESEHILFE-2026-27":
                    errors.append(
                        f"{expectation_label} führt Orientierungsrecord {reference_id} als amtlich bindend"
                    )
                if basis == "orientation" and source_id != "SRC-CUR-LESEHILFE-2026-27":
                    errors.append(
                        f"{expectation_label} führt amtlichen Record {reference_id} nur als Orientierung"
                    )
                record_grades = record.get("grades")
                if isinstance(record_grades, list) and not set(expectation_grades).issubset(
                    {grade for grade in record_grades if _is_plain_int(grade)}
                ):
                    errors.append(
                        f"{expectation_label} überschreitet den Jahrgangsscope von {reference_id}"
                    )
            limitation_errors, _limitations = _validate_lxf03_string_list(
                expectation.get("limitations"), expectation_label, "limitations"
            )
            errors.extend(limitation_errors)
            for limitation in _limitations:
                errors.extend(
                    _validate_lxf03_profile_text(
                        limitation, f"{expectation_label} limitation"
                    )
                )

        questions = dimension.get("openAgeSpecificQuestions")
        if not isinstance(questions, list) or not questions:
            errors.append(f"{label} benötigt openAgeSpecificQuestions")
            questions = []
        for index, question in enumerate(questions):
            if not isinstance(question, dict):
                errors.append(f"{label} offene Frage {index} muss ein Objekt sein")
                continue
            question_id = question.get("id")
            question_label = f"LXF03-Altersfrage {question_id or index}"
            errors.extend(
                _unknown_fields(question, LEARNER_PROFILE_QUESTION_FIELDS, question_label)
            )
            for field in sorted(LEARNER_PROFILE_QUESTION_FIELDS - set(question)):
                errors.append(f"{question_label} benötigt {field}")
            if not _nonempty_string(question_id):
                errors.append(f"{question_label} benötigt id")
            elif not re.fullmatch(r"LXF03-Q-[0-9]{3}", question_id):
                errors.append(f"{question_label} hat eine ungültige ID")
            elif question_id in record_ids:
                errors.append(f"LXF03-Profil enthält doppelte ID {question_id}")
            else:
                record_ids.add(question_id)
            for field in ("question", "decisionOwner", "implications"):
                if not _nonempty_string(question.get(field)):
                    errors.append(f"{question_label} benötigt {field}")
            decision_owner = question.get("decisionOwner")
            if _nonempty_string(decision_owner) and not (
                LEARNER_PROFILE_DECISION_OWNER_PATTERN.fullmatch(decision_owner)
            ):
                errors.append(
                    f"{question_label} hat ungültigen decisionOwner: {decision_owner}"
                )
            for field in ("question", "implications"):
                if _nonempty_string(question.get(field)):
                    errors.extend(
                        _validate_lxf03_profile_text(
                            question.get(field), f"{question_label} {field}"
                        )
                    )
            grade_errors, _grades = _validate_lxf03_grades(
                question.get("grades"), question_label
            )
            errors.extend(grade_errors)

        pilot_questions = dimension.get("pilotQuestions")
        if not isinstance(pilot_questions, list) or not pilot_questions:
            errors.append(f"{label} benötigt pilotQuestions")
            pilot_questions = []
        for index, pilot in enumerate(pilot_questions):
            if not isinstance(pilot, dict):
                errors.append(f"{label} Pilotfrage {index} muss ein Objekt sein")
                continue
            pilot_id = pilot.get("id")
            pilot_label = f"LXF03-Pilotfrage {pilot_id or index}"
            errors.extend(_unknown_fields(pilot, LEARNER_PROFILE_PILOT_FIELDS, pilot_label))
            for field in sorted(LEARNER_PROFILE_PILOT_FIELDS - set(pilot)):
                errors.append(f"{pilot_label} benötigt {field}")
            if not _nonempty_string(pilot_id):
                errors.append(f"{pilot_label} benötigt id")
            elif not re.fullmatch(r"LXF03-P-[0-9]{3}", pilot_id):
                errors.append(f"{pilot_label} hat eine ungültige ID")
            elif pilot_id in record_ids:
                errors.append(f"LXF03-Profil enthält doppelte ID {pilot_id}")
            else:
                record_ids.add(pilot_id)
            for field in ("question", "evidenceNeeded"):
                if not _nonempty_string(pilot.get(field)):
                    errors.append(f"{pilot_label} benötigt {field}")
                else:
                    errors.extend(
                        _validate_lxf03_profile_text(
                            pilot.get(field), f"{pilot_label} {field}"
                        )
                    )
            if pilot.get("privacyBoundary") != "non-personal-observation-only":
                errors.append(
                    f"{pilot_label} privacyBoundary muss non-personal-observation-only sein"
                )
            grade_errors, _grades = _validate_lxf03_grades(
                pilot.get("grades"), pilot_label
            )
            errors.extend(grade_errors)

    actual_dimensions = set(dimensions_by_id)
    for missing in sorted(EXPECTED_LEARNER_PROFILE_DIMENSIONS - actual_dimensions):
        errors.append(f"LXF03-Profil fehlt Dimension: {missing}")
    for unexpected in sorted(actual_dimensions - EXPECTED_LEARNER_PROFILE_DIMENSIONS):
        errors.append(f"LXF03-Profil enthält unerwartete Dimension: {unexpected}")
    return errors


def validate_learner_profile_schema(root: Path) -> list[str]:
    relative_path = Path("schemas/v2/learner-profile.schema.json")
    path = root / relative_path
    if not path.is_file():
        return [f"LXF03-Schema fehlt: {relative_path.as_posix()}"]
    try:
        schema = load_json(path)
    except (OSError, UnicodeError, json.JSONDecodeError):
        return [f"LXF03-Schema ist kein gültiges JSON: {relative_path.as_posix()}"]
    if not isinstance(schema, dict):
        return ["LXF03-Schema muss ein Objekt sein"]
    canonical_schema = json.dumps(
        schema,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    if hashlib.sha256(canonical_schema).hexdigest().upper() != (
        LEARNER_PROFILE_SCHEMA_SHA256
    ):
        return ["LXF03-Schema weicht von der versiegelten Definition ab"]
    return []


def validate_learner_profile_markdown(root: Path) -> list[str]:
    path = root / "roadmap/v2/foundations/learning-experience/learner-profile.md"
    if not path.is_file():
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return ["LXF03-Fachprofil ist nicht als UTF-8 lesbar"]
    profile_path = (
        root / "roadmap/v2/foundations/learning-experience/learner-profile.json"
    )
    try:
        profile = load_json(profile_path)
    except (OSError, UnicodeError, json.JSONDecodeError):
        return ["LXF03-Fachprofil kann nicht mit dem strukturierten Profil abgeglichen werden"]
    if not isinstance(profile, dict):
        return ["LXF03-Fachprofil benötigt ein strukturiertes Profilobjekt"]
    title = "# LXF03 Fach- und Stufenprofil IuM 5–7"
    dimension_headings = [
        "## 1. Vorwissen und Vorstellungen",
        "## 2. Lesen und Fachsprache",
        "## 3. Aufmerksamkeit und Arbeitsgedächtnisbelastung",
        "## 4. Digitale Bedienroutinen",
        "## 5. Selbstregulation und Hilfenutzung",
        "## 6. Motivation und wahrgenommener Sinn",
        "## 7. Zugangsbarrieren und Ausdruckswege",
        "## 8. Zusammenarbeit und Lehrkraftorchestrierung",
    ]
    view_headings = [
        "### Evidenzgestützte Annahmen",
        "### Curriculare oder projektdefinierte Erwartungen",
        "### Offene altersspezifische Fragen",
        "### Folgen für Lernendenmaterial",
        "### Folgen für Lehrkraftorchestrierung",
        "### Pilotfragen",
    ]
    errors: list[str] = []
    if not text.startswith(f"{title}\n"):
        errors.append(f"LXF03-Fachprofil fehlt Überschrift: {title}")
    positions = [text.find(heading) for heading in dimension_headings]
    present = [position for position in positions if position >= 0]
    preamble = text[: min(present)] if present else text
    scope = profile.get("scope")
    if isinstance(scope, dict):
        status_values = re.findall(
            r"(?m)^\*\*Status:\*\*\s*`([^`\r\n]+)`\s*$", preamble
        )
        if status_values != [scope.get("maturity")]:
            errors.append("LXF03-Fachprofil Status weicht vom strukturierten Profil ab")
        grades = scope.get("grades")
        grade_label = (
            f"{min(grades)}–{max(grades)}"
            if isinstance(grades, list)
            and grades
            and all(_is_plain_int(grade) for grade in grades)
            else "<ungültig>"
        )
        expected_scope = (
            f"{scope.get('schoolType')}, Niveau {scope.get('level')}, "
            f"Klassen {grade_label}"
        )
        scope_values = [
            value.strip()
            for value in re.findall(
                r"(?m)^\*\*Geltungsbereich:\*\*\s*(.+?)\s*$", preamble
            )
        ]
        if scope_values != [expected_scope]:
            errors.append("LXF03-Fachprofil Geltungsbereich weicht vom JSON ab")
    as_of = profile.get("asOf")
    if _is_iso_date(as_of):
        year, month, day = (int(part) for part in as_of.split("-"))
        month_names = (
            "",
            "Januar",
            "Februar",
            "März",
            "April",
            "Mai",
            "Juni",
            "Juli",
            "August",
            "September",
            "Oktober",
            "November",
            "Dezember",
        )
        expected_date = f"{day}. {month_names[month]} {year}"
        date_values = [
            value.strip()
            for value in re.findall(
                r"(?m)^\*\*Stichtag:\*\*\s*(.+?)\s*$", preamble
            )
        ]
        if date_values != [expected_date]:
            errors.append("LXF03-Fachprofil Stichtag weicht vom JSON ab")

    dimensions = profile.get("dimensions")
    dimensions_by_id: dict[str, dict] = {}
    if isinstance(dimensions, list):
        for dimension in dimensions:
            if isinstance(dimension, dict) and _nonempty_string(dimension.get("id")):
                dimensions_by_id[dimension["id"]] = dimension
    for heading, position in zip(dimension_headings, positions):
        if position < 0:
            errors.append(f"LXF03-Fachprofil fehlt Überschrift: {heading}")
    if present != sorted(present):
        errors.append("LXF03-Fachprofil hat eine unerwartete Abschnittsreihenfolge")
    for index, (dimension_id, heading, position) in enumerate(
        zip(LEARNER_PROFILE_DIMENSION_ORDER, dimension_headings, positions)
    ):
        if position < 0:
            continue
        end = (
            positions[index + 1]
            if index + 1 < len(positions) and positions[index + 1] >= 0
            else len(text)
        )
        block = text[position:end]
        expected_references: set[str] = set()
        dimension = dimensions_by_id.get(dimension_id, {})
        assumptions = dimension.get("evidenceSupportedAssumptions")
        if isinstance(assumptions, list):
            for statement in assumptions:
                if isinstance(statement, dict) and isinstance(
                    statement.get("claimIds"), list
                ):
                    expected_references.update(
                        claim_id
                        for claim_id in statement["claimIds"]
                        if _nonempty_string(claim_id)
                    )
        expectations = dimension.get("curriculumAndProjectExpectations")
        if isinstance(expectations, list):
            for expectation in expectations:
                if isinstance(expectation, dict) and isinstance(
                    expectation.get("referenceIds"), list
                ):
                    expected_references.update(
                        reference_id
                        for reference_id in expectation["referenceIds"]
                        if _nonempty_string(reference_id)
                    )
        cited_references = set(LEARNER_PROFILE_REFERENCE_PATTERN.findall(block))
        for missing_reference in sorted(expected_references - cited_references):
            errors.append(
                f"LXF03-Fachprofil {heading} fehlt Referenz: {missing_reference}"
            )
        for unknown_reference in sorted(cited_references - expected_references):
            errors.append(
                f"LXF03-Fachprofil {heading} enthält unerwartete Referenz: "
                f"{unknown_reference}"
            )
        subpositions = [block.find(view) for view in view_headings]
        for view, subposition in zip(view_headings, subpositions):
            if subposition < 0:
                errors.append(f"LXF03-Fachprofil {heading} fehlt Ansicht: {view}")
        present_subpositions = [value for value in subpositions if value >= 0]
        if present_subpositions != sorted(present_subpositions):
            errors.append(f"LXF03-Fachprofil {heading} hat falsche Ansichtsreihenfolge")
        for subindex, (view, subposition) in enumerate(
            zip(view_headings, subpositions)
        ):
            if subposition < 0:
                continue
            content_start = subposition + len(view)
            later = [
                value
                for value in subpositions[subindex + 1 :]
                if value >= 0
            ]
            content_end = min(later) if later else len(block)
            content = block[content_start:content_end]
            if len(re.findall(r"\b[\wÄÖÜäöüß-]+\b", content)) < 12:
                errors.append(
                    f"LXF03-Fachprofil {heading} hat leere oder zu knappe Ansicht: {view}"
                )
    return errors


def _validate_lxf04_string_list(
    value: object,
    label: str,
    field: str,
    *,
    allow_duplicates: bool = False,
) -> tuple[list[str], list[str]]:
    if not isinstance(value, list) or not value:
        return [f"{label} benötigt {field}"], []
    valid = [item for item in value if _nonempty_string(item)]
    errors: list[str] = []
    if len(valid) != len(value):
        errors.append(f"{label} {field} enthält einen leeren Eintrag")
    if not allow_duplicates and len(valid) != len(set(valid)):
        errors.append(f"{label} {field} enthält Duplikate")
    return errors, valid


def _lxf04_reference_indexes(
    evidence_register: object,
    learner_profile: object,
    requirements: object,
) -> tuple[set[str], set[str], set[str], set[str]]:
    raw_claims = (
        evidence_register.get("claims")
        if isinstance(evidence_register, dict)
        else None
    )
    if not isinstance(raw_claims, list):
        raw_claims = []
    claim_ids = {
        claim["id"]
        for claim in raw_claims
        if isinstance(claim, dict) and _nonempty_string(claim.get("id"))
    }

    statement_ids: set[str] = set()
    expectation_ids: set[str] = set()
    dimensions = (
        learner_profile.get("dimensions")
        if isinstance(learner_profile, dict)
        else None
    )
    if not isinstance(dimensions, list):
        dimensions = []
    for dimension in dimensions:
        if not isinstance(dimension, dict):
            continue
        assumptions = dimension.get("evidenceSupportedAssumptions")
        if not isinstance(assumptions, list):
            assumptions = []
        for statement in assumptions:
            if isinstance(statement, dict) and _nonempty_string(statement.get("id")):
                statement_ids.add(statement["id"])
        expectations = dimension.get("curriculumAndProjectExpectations")
        if not isinstance(expectations, list):
            expectations = []
        for expectation in expectations:
            if isinstance(expectation, dict) and _nonempty_string(
                expectation.get("id")
            ):
                expectation_ids.add(expectation["id"])

    raw_requirements = (
        requirements.get("requirements")
        if isinstance(requirements, dict)
        else None
    )
    if not isinstance(raw_requirements, list):
        raw_requirements = []
    requirement_ids = {
        requirement["id"]
        for requirement in raw_requirements
        if isinstance(requirement, dict)
        and _nonempty_string(requirement.get("id"))
    }
    return claim_ids, statement_ids, expectation_ids, requirement_ids


def validate_learning_architecture(
    data: object,
    evidence_register: object,
    learner_profile: object,
    requirements: object,
) -> list[str]:
    if not isinstance(data, dict):
        return ["LXF04-Architektur muss ein Objekt sein"]

    errors: list[str] = []
    errors.extend(
        _unknown_fields(data, LEARNING_ARCHITECTURE_FIELDS, "LXF04-Architektur")
    )
    errors.extend(
        _missing_fields(data, LEARNING_ARCHITECTURE_FIELDS, "LXF04-Architektur")
    )
    if not _is_plain_int(data.get("schemaVersion")) or data.get("schemaVersion") != 1:
        errors.append("LXF04-Architektur schemaVersion muss 1 sein")
    if data.get("projectId") != "ium-lernwerk":
        errors.append("LXF04-Architektur projectId muss ium-lernwerk sein")
    if not _is_iso_date(data.get("asOf")):
        errors.append("LXF04-Architektur asOf muss ein echtes Kalenderdatum sein")

    scope = data.get("scope")
    if not isinstance(scope, dict):
        errors.append("LXF04-Architektur benötigt scope")
    else:
        errors.extend(
            _unknown_fields(scope, LEARNING_ARCHITECTURE_SCOPE_FIELDS, "LXF04-Scope")
        )
        errors.extend(
            _missing_fields(scope, LEARNING_ARCHITECTURE_SCOPE_FIELDS, "LXF04-Scope")
        )
        grade_errors, grades = _validate_lxf03_grades(scope.get("grades"), "LXF04-Scope")
        errors.extend(grade_errors)
        if set(grades) != REQUIREMENT_GRADES:
            errors.append("LXF04-Scope muss genau die Klassen 5, 6 und 7 umfassen")
        expected_scope = {
            "schoolType": "Gymnasium Baden-Württemberg",
            "level": "E",
            "maturity": "working",
            "contentProduction": "frozen",
        }
        for field, expected in expected_scope.items():
            if scope.get(field) != expected:
                errors.append(f"LXF04-Scope {field} muss {expected} sein")

    known_claims, known_statements, known_expectations, known_requirements = (
        _lxf04_reference_indexes(evidence_register, learner_profile, requirements)
    )
    if not known_claims:
        errors.append("LXF04-Architektur benötigt ein lesbares LXF02-Evidenzregister")
    if not known_statements or not known_expectations:
        errors.append("LXF04-Architektur benötigt ein lesbares LXF03-Profil")
    if not known_requirements:
        errors.append("LXF04-Architektur benötigt ein lesbares V2-Anforderungsregister")

    groups = data.get("principleGroups")
    groups_by_id: dict[str, dict] = {}
    principle_ids: set[str] = set()
    referenced_claim_ids: set[str] = set()
    if not isinstance(groups, list) or not groups:
        errors.append("LXF04-Architektur principleGroups dürfen nicht leer sein")
        groups = []
    for position, group in enumerate(groups):
        if not isinstance(group, dict):
            errors.append(f"LXF04-Prinzipgruppe an Position {position} muss ein Objekt sein")
            continue
        group_id_value = group.get("id")
        group_id = (
            group_id_value
            if _nonempty_string(group_id_value)
            else f"<Position {position}>"
        )
        label = f"LXF04-Prinzipgruppe {group_id}"
        errors.extend(_unknown_fields(group, LEARNING_ARCHITECTURE_GROUP_FIELDS, label))
        errors.extend(_missing_fields(group, LEARNING_ARCHITECTURE_GROUP_FIELDS, label))
        if not _nonempty_string(group_id_value):
            errors.append(f"{label} benötigt id")
        elif group_id_value in groups_by_id:
            errors.append(f"LXF04-Architektur enthält doppelte Prinzipgruppe {group_id_value}")
        else:
            groups_by_id[group_id_value] = group
        if not _nonempty_string(group.get("label")):
            errors.append(f"{label} benötigt label")
        principles = group.get("principles")
        if not isinstance(principles, list) or not principles:
            errors.append(f"{group_id} benötigt mindestens ein Pflichtprinzip")
            principles = []
        has_required = False
        for principle_position, principle in enumerate(principles):
            if not isinstance(principle, dict):
                errors.append(
                    f"{label} Prinzip an Position {principle_position} muss ein Objekt sein"
                )
                continue
            principle_id_value = principle.get("id")
            principle_id = (
                principle_id_value
                if _nonempty_string(principle_id_value)
                else f"<Position {principle_position}>"
            )
            principle_label = f"LXF04-Prinzip {principle_id}"
            errors.extend(
                _unknown_fields(
                    principle,
                    LEARNING_ARCHITECTURE_PRINCIPLE_FIELDS,
                    principle_label,
                )
            )
            for field in sorted(LEARNING_ARCHITECTURE_PRINCIPLE_FIELDS - set(principle)):
                errors.append(f"{principle_label} benötigt {field}")
            if not _nonempty_string(principle_id_value):
                errors.append(f"{principle_label} benötigt id")
            elif not re.fullmatch(r"LXF04-PR-[0-9]{3}", principle_id_value):
                errors.append(f"{principle_label} hat eine ungültige ID")
            elif principle_id_value in principle_ids:
                errors.append(f"LXF04-Architektur enthält doppelte Prinzip-ID {principle_id_value}")
            else:
                principle_ids.add(principle_id_value)
            for field in ("title", "decision", "decisionBasis"):
                if not _nonempty_string(principle.get(field)):
                    errors.append(f"{principle_label} benötigt {field}")

            claim_errors, claim_ids = _validate_lxf04_string_list(
                principle.get("claimIds"), principle_label, "claimIds"
            )
            errors.extend(claim_errors)
            for claim_id in claim_ids:
                referenced_claim_ids.add(claim_id)
                if claim_id not in known_claims:
                    errors.append(f"{principle_label} referenziert unbekannten Claim {claim_id}")

            decision_basis = principle.get("decisionBasis")
            basis_refs = (
                set(LEARNING_ARCHITECTURE_REFERENCE_PATTERN.findall(decision_basis))
                if _nonempty_string(decision_basis)
                else set()
            )
            basis_requirements = {ref for ref in basis_refs if ref.startswith("V2-REQ-")}
            basis_statements = {ref for ref in basis_refs if ref.startswith("LXF03-S-")}
            basis_expectations = {ref for ref in basis_refs if ref.startswith("LXF03-E-")}
            if not basis_requirements:
                errors.append(f"{principle_label} decisionBasis benötigt eine V2-Anforderung")
            if not basis_statements:
                errors.append(f"{principle_label} decisionBasis benötigt ein LXF03-Statement")
            if not basis_expectations:
                errors.append(f"{principle_label} decisionBasis benötigt eine LXF03-Erwartung")
            for reference in sorted(basis_requirements - known_requirements):
                errors.append(
                    f"{principle_label} referenziert unbekannte V2-Anforderung {reference}"
                )
            for reference in sorted(basis_statements - known_statements):
                errors.append(
                    f"{principle_label} referenziert unbekanntes LXF03-Statement {reference}"
                )
            for reference in sorted(basis_expectations - known_expectations):
                errors.append(
                    f"{principle_label} referenziert unbekannte LXF03-Erwartung {reference}"
                )

            obligation = principle.get("obligation")
            if (
                not isinstance(obligation, str)
                or obligation not in LEARNING_ARCHITECTURE_OBLIGATIONS
            ):
                errors.append(f"{principle_label} hat unbekannte obligation: {obligation}")
            if obligation == "required":
                has_required = True
            applies_errors, applies_to = _validate_lxf04_string_list(
                principle.get("appliesTo"), principle_label, "appliesTo"
            )
            errors.extend(applies_errors)
            for target in applies_to:
                if target not in LEARNING_ARCHITECTURE_APPLIES_TO:
                    errors.append(f"{principle_label} hat unbekannten Geltungsbereich: {target}")
            for field in ("positivePatterns", "antiPatterns", "observableCriteria"):
                field_errors, _values = _validate_lxf04_string_list(
                    principle.get(field), principle_label, field
                )
                errors.extend(field_errors)
            method_errors, methods = _validate_lxf04_string_list(
                principle.get("verificationMethods"),
                principle_label,
                "verificationMethods",
            )
            errors.extend(method_errors)
            for method in methods:
                if method not in LEARNING_ARCHITECTURE_VERIFICATION_METHODS:
                    errors.append(f"{principle_label} hat unbekannte Prüfmethode: {method}")
            if methods == ["automated-check"]:
                errors.append(f"{principle_label} darf nicht nur automatisiert geprüft werden")
            status = principle.get("status")
            if (
                not isinstance(status, str)
                or status not in LEARNING_ARCHITECTURE_STATUSES
            ):
                errors.append(f"{principle_label} hat unbekannten status: {status}")
        if not has_required:
            errors.append(f"{group_id} benötigt mindestens ein Pflichtprinzip")

    actual_groups = set(groups_by_id)
    for missing in sorted(EXPECTED_LEARNING_ARCHITECTURE_GROUPS - actual_groups):
        errors.append(f"LXF04-Architektur fehlt Prinzipgruppe: {missing}")
    for unexpected in sorted(actual_groups - EXPECTED_LEARNING_ARCHITECTURE_GROUPS):
        errors.append(f"LXF04-Architektur enthält unerwartete Prinzipgruppe: {unexpected}")

    grammar = data.get("learningFunctionGrammar")
    if not isinstance(grammar, dict):
        errors.append("LXF04-Architektur benötigt learningFunctionGrammar")
        grammar = {}
    else:
        errors.extend(
            _unknown_fields(grammar, LEARNING_FUNCTION_GRAMMAR_FIELDS, "LXF04-Lernfunktionsgrammatik")
        )
        errors.extend(
            _missing_fields(grammar, LEARNING_FUNCTION_GRAMMAR_FIELDS, "LXF04-Lernfunktionsgrammatik")
        )
    if grammar.get("universalOrder") is not False:
        errors.append("LXF04-Lernfunktionsgrammatik darf keine universelle Reihenfolge setzen")

    functions = grammar.get("functions")
    functions_by_id: dict[str, dict] = {}
    if not isinstance(functions, list) or not functions:
        errors.append("LXF04-Lernfunktionsgrammatik benötigt functions")
        functions = []
    for position, function in enumerate(functions):
        if not isinstance(function, dict):
            errors.append(f"LXF04-Lernfunktion an Position {position} muss ein Objekt sein")
            continue
        function_id_value = function.get("id")
        function_id = (
            function_id_value
            if _nonempty_string(function_id_value)
            else f"<Position {position}>"
        )
        label = f"LXF04-Lernfunktion {function_id}"
        errors.extend(_unknown_fields(function, LEARNING_FUNCTION_FIELDS, label))
        errors.extend(_missing_fields(function, LEARNING_FUNCTION_FIELDS, label))
        if not _nonempty_string(function_id_value):
            errors.append(f"{label} benötigt id")
        elif function_id_value in functions_by_id:
            errors.append(f"LXF04-Lernfunktionsgrammatik enthält doppelte Funktion {function_id_value}")
        else:
            functions_by_id[function_id_value] = function
        for field in ("label", "purpose", "observableOutput", "teacherRole"):
            if not _nonempty_string(function.get(field)):
                errors.append(f"{label} benötigt {field}")
        boundary_errors, _boundaries = _validate_lxf04_string_list(
            function.get("boundaries"), label, "boundaries"
        )
        errors.extend(boundary_errors)
    for missing in sorted(EXPECTED_LEARNING_FUNCTIONS - set(functions_by_id)):
        errors.append(f"LXF04-Lernfunktionsgrammatik fehlt Funktion: {missing}")
    for unexpected in sorted(set(functions_by_id) - EXPECTED_LEARNING_FUNCTIONS):
        errors.append(f"LXF04-Lernfunktionsgrammatik enthält unbekannte Funktion: {unexpected}")

    transitions = grammar.get("transitions")
    transitions_by_id: dict[str, dict] = {}
    if not isinstance(transitions, list) or not transitions:
        errors.append("LXF04-Lernfunktionsgrammatik benötigt transitions")
        transitions = []
    for position, transition in enumerate(transitions):
        if not isinstance(transition, dict):
            errors.append(f"LXF04-Übergang an Position {position} muss ein Objekt sein")
            continue
        transition_id_value = transition.get("id")
        transition_id = (
            transition_id_value
            if _nonempty_string(transition_id_value)
            else f"<Position {position}>"
        )
        label = transition_id if _nonempty_string(transition_id_value) else f"LXF04-Übergang {transition_id}"
        errors.extend(_unknown_fields(transition, LEARNING_TRANSITION_FIELDS, label))
        errors.extend(_missing_fields(transition, LEARNING_TRANSITION_FIELDS, label))
        if not _nonempty_string(transition_id_value):
            errors.append(f"{label} benötigt id")
        elif not re.fullmatch(r"LXF04-T-[0-9]{3}", transition_id_value):
            errors.append(f"{label} hat eine ungültige ID")
        elif transition_id_value in transitions_by_id:
            errors.append(f"LXF04-Lernfunktionsgrammatik enthält doppelten Übergang {transition_id_value}")
        else:
            transitions_by_id[transition_id_value] = transition
        if not _nonempty_string(transition.get("pedagogicalRationale")):
            errors.append(f"{label} benötigt pedagogicalRationale")
        condition_errors, _conditions = _validate_lxf04_string_list(
            transition.get("conditions"), label, "conditions"
        )
        errors.extend(condition_errors)
        source = transition.get("from")
        target = transition.get("to")
        for endpoint, field in ((source, "from"), (target, "to")):
            if (
                not isinstance(endpoint, str)
                or endpoint not in EXPECTED_LEARNING_FUNCTIONS
            ):
                errors.append(f"{label} {field} referenziert unbekannte Lernfunktion {endpoint}")
        if (
            isinstance(source, str)
            and source == target
            and source in EXPECTED_LEARNING_FUNCTIONS
        ):
            errors.append(f"{label} darf keine Selbstschleife bilden")

    variants = grammar.get("sequenceVariants")
    variant_ids: set[str] = set()
    if not isinstance(variants, list) or len(variants) < 2:
        errors.append("LXF04-Lernfunktionsgrammatik benötigt mindestens zwei Reihenfolgevarianten")
        variants = variants if isinstance(variants, list) else []
    for position, variant in enumerate(variants):
        if not isinstance(variant, dict):
            errors.append(f"LXF04-Variante an Position {position} muss ein Objekt sein")
            continue
        variant_id_value = variant.get("id")
        variant_id = variant_id_value if _nonempty_string(variant_id_value) else f"<Position {position}>"
        label = f"LXF04-Variante {variant_id}"
        errors.extend(_unknown_fields(variant, LEARNING_SEQUENCE_VARIANT_FIELDS, label))
        errors.extend(_missing_fields(variant, LEARNING_SEQUENCE_VARIANT_FIELDS, label))
        if not _nonempty_string(variant_id_value):
            errors.append(f"{label} benötigt id")
        elif not re.fullmatch(r"LXF04-V-[0-9]{3}", variant_id_value):
            errors.append(f"{label} hat eine ungültige ID")
        elif variant_id_value in variant_ids:
            errors.append(f"LXF04-Lernfunktionsgrammatik enthält doppelte Variante {variant_id_value}")
        else:
            variant_ids.add(variant_id_value)
        for field in ("label", "rationale"):
            if not _nonempty_string(variant.get(field)):
                errors.append(f"{label} benötigt {field}")
        condition_errors, _conditions = _validate_lxf04_string_list(
            variant.get("conditions"), label, "conditions"
        )
        errors.extend(condition_errors)
        transition_errors, transition_ids = _validate_lxf04_string_list(
            variant.get("transitionIds"),
            label,
            "transitionIds",
            allow_duplicates=True,
        )
        errors.extend(transition_errors)
        path: list[dict] = []
        for transition_id in transition_ids:
            transition = transitions_by_id.get(transition_id)
            if transition is None:
                errors.append(f"{label} referenziert unbekannten Übergang {transition_id}")
            else:
                path.append(transition)
        if len(path) == len(transition_ids) and any(
            current.get("to") != following.get("from")
            for current, following in zip(path, path[1:])
        ):
            errors.append(f"{label} bildet keinen zusammenhängenden Übergangspfad")

    interactions = grammar.get("digitalInteractions")
    interaction_ids: set[str] = set()
    if not isinstance(interactions, list) or not interactions:
        errors.append("LXF04-Lernfunktionsgrammatik benötigt digitalInteractions")
        interactions = []
    for position, interaction in enumerate(interactions):
        if not isinstance(interaction, dict):
            errors.append(f"LXF04-Digitalinteraktion an Position {position} muss ein Objekt sein")
            continue
        interaction_id_value = interaction.get("id")
        interaction_id = interaction_id_value if _nonempty_string(interaction_id_value) else f"<Position {position}>"
        label = f"LXF04-Digitalinteraktion {interaction_id}"
        errors.extend(_unknown_fields(interaction, LEARNING_DIGITAL_INTERACTION_FIELDS, label))
        errors.extend(_missing_fields(interaction, LEARNING_DIGITAL_INTERACTION_FIELDS, label))
        if not _nonempty_string(interaction_id_value):
            errors.append(f"{label} benötigt id")
        elif not re.fullmatch(r"LXF04-DI-[0-9]{3}", interaction_id_value):
            errors.append(f"{label} hat eine ungültige ID")
        elif interaction_id_value in interaction_ids:
            errors.append(f"LXF04-Lernfunktionsgrammatik enthält doppelte Digitalinteraktion {interaction_id_value}")
        else:
            interaction_ids.add(interaction_id_value)
        for field in ("label", "purpose"):
            if not _nonempty_string(interaction.get(field)):
                errors.append(f"{label} benötigt {field}")
        learning_function_id = interaction.get("learningFunctionId")
        if (
            not isinstance(learning_function_id, str)
            or learning_function_id not in EXPECTED_LEARNING_FUNCTIONS
        ):
            errors.append(f"{label} referenziert unbekannte Lernfunktion {learning_function_id}")
        for field in ("forbiddenUses", "observableCriteria"):
            field_errors, _values = _validate_lxf04_string_list(
                interaction.get(field), label, field
            )
            errors.extend(field_errors)
        method_errors, methods = _validate_lxf04_string_list(
            interaction.get("verificationMethods"), label, "verificationMethods"
        )
        errors.extend(method_errors)
        for method in methods:
            if method not in LEARNING_ARCHITECTURE_VERIFICATION_METHODS:
                errors.append(f"{label} hat unbekannte Prüfmethode: {method}")
        if methods == ["automated-check"]:
            errors.append(f"{label} darf nicht nur automatisiert geprüft werden")

    def validate_named_records(
        value: object,
        collection_label: str,
        expected_ids: set[str],
        required_fields: set[str],
        string_fields: tuple[str, ...],
        list_fields: tuple[str, ...],
    ) -> dict[str, dict]:
        records_by_id: dict[str, dict] = {}
        if not isinstance(value, list) or not value:
            errors.append(f"LXF04-Architektur benötigt {collection_label}")
            value = []
        for position, record in enumerate(value):
            if not isinstance(record, dict):
                errors.append(f"LXF04-{collection_label} an Position {position} muss ein Objekt sein")
                continue
            record_id_value = record.get("id")
            record_id = record_id_value if _nonempty_string(record_id_value) else f"<Position {position}>"
            label = f"LXF04-{collection_label} {record_id}"
            errors.extend(_unknown_fields(record, required_fields, label))
            errors.extend(_missing_fields(record, required_fields, label))
            if not _nonempty_string(record_id_value):
                errors.append(f"{label} benötigt id")
            elif record_id_value in records_by_id:
                errors.append(f"LXF04-{collection_label} enthält doppelte ID {record_id_value}")
            else:
                records_by_id[record_id_value] = record
            for field in string_fields:
                if not _nonempty_string(record.get(field)):
                    errors.append(f"{label} benötigt {field}")
            for field in list_fields:
                field_errors, _values = _validate_lxf04_string_list(
                    record.get(field), label, field
                )
                errors.extend(field_errors)
        for missing in sorted(expected_ids - set(records_by_id)):
            noun = {
                "Aufgabentyp": "Aufgabentyp",
                "Übungsstufe": "Übungsstufe",
                "Instruktionsmodus": "Instruktionsmodus",
            }[collection_label]
            errors.append(f"LXF04-Architektur fehlt {noun}: {missing}")
        for unexpected in sorted(set(records_by_id) - expected_ids):
            errors.append(f"LXF04-Architektur enthält unerwartete {collection_label}-ID: {unexpected}")
        return records_by_id

    task_types = validate_named_records(
        data.get("taskTypes"),
        "Aufgabentyp",
        EXPECTED_LEARNING_TASK_TYPES,
        LEARNING_TASK_TYPE_FIELDS,
        ("purpose", "evidenceUse", "feedbackTiming"),
        ("boundaries",),
    )
    task_semantics = {
        "learning-task": ("formative", "during-learning"),
        "performance-task": ("summative-or-gate", "after-performance"),
    }
    for task_id, (evidence_use, feedback_timing) in task_semantics.items():
        task = task_types.get(task_id)
        if task is not None and (
            task.get("evidenceUse") != evidence_use
            or task.get("feedbackTiming") != feedback_timing
        ):
            errors.append(f"LXF04-Aufgabentyp {task_id} hat widersprüchliche Nachweissemantik")

    stages = validate_named_records(
        data.get("practiceTransferStages"),
        "Übungsstufe",
        EXPECTED_LEARNING_PRACTICE_STAGES,
        LEARNING_PRACTICE_STAGE_FIELDS,
        ("definition", "temporalPosition", "observableEvidence"),
        ("boundaries",),
    )
    stage_positions = {
        "immediate-application": "immediate",
        "delayed-retrieval": "delayed",
        "transfer": "novel-context",
    }
    for stage_id, temporal_position in stage_positions.items():
        stage = stages.get(stage_id)
        if stage is not None and stage.get("temporalPosition") != temporal_position:
            errors.append(f"LXF04-Übungsstufe {stage_id} hat falsche temporalPosition")

    modes = validate_named_records(
        data.get("instructionModes"),
        "Instruktionsmodus",
        EXPECTED_LEARNING_INSTRUCTION_MODES,
        LEARNING_INSTRUCTION_MODE_FIELDS,
        (),
        ("claimIds", "useWhen", "avoidWhen", "requiredBefore", "requiredAfter"),
    )
    for mode_id, mode in modes.items():
        raw_mode_claim_ids = mode.get("claimIds")
        mode_claim_ids = (
            raw_mode_claim_ids if isinstance(raw_mode_claim_ids, list) else []
        )
        for claim_id in mode_claim_ids:
            if _nonempty_string(claim_id):
                referenced_claim_ids.add(claim_id)
                if claim_id not in known_claims:
                    errors.append(f"LXF04-Instruktionsmodus {mode_id} referenziert unbekannten Claim {claim_id}")
    unreferenced_claims = sorted(known_claims - referenced_claim_ids)
    if unreferenced_claims:
        errors.append(
            "LXF04-Architektur lässt LXF02-Claim ohne Designbezug: "
            + ", ".join(unreferenced_claims)
        )
    return errors


def validate_learning_design_schema(root: Path) -> list[str]:
    relative_path = Path("schemas/v2/learning-design.schema.json")
    path = root / relative_path
    if not path.is_file():
        return [f"LXF04-Schema fehlt: {relative_path.as_posix()}"]
    try:
        schema = load_json(path)
    except (OSError, UnicodeError, json.JSONDecodeError):
        return [f"LXF04-Schema ist kein gültiges JSON: {relative_path.as_posix()}"]
    if not isinstance(schema, dict):
        return ["LXF04-Schema muss ein Objekt sein"]
    canonical_schema = json.dumps(
        schema,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    if hashlib.sha256(canonical_schema).hexdigest().upper() != (
        LEARNING_DESIGN_SCHEMA_SHA256
    ):
        return ["LXF04-Schema weicht von der versiegelten Definition ab"]
    return []


def validate_learning_architecture_markdown(root: Path) -> list[str]:
    path = root / "roadmap/v2/foundations/learning-experience/learning-architecture.md"
    if not path.is_file():
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return ["LXF04-Lernarchitektur ist nicht als UTF-8 lesbar"]
    headings = [
        "# LXF04 Lernarchitektur-Vertrag",
        "## Vertragsgrenzen",
        "## Acht Qualitätsdimensionen",
        "## Lernfunktionsgrammatik",
        "## Gültige Reihenfolgevarianten",
        "## Lern- und Leistungsaufgaben",
        "## Exploration und explizite Erklärung",
        "## Anwendung, verzögerter Abruf und Transfer",
        "## Digitale Interaktion",
        "## WU-Abgleich",
        "## Übergabegrenze",
    ]
    errors: list[str] = []
    positions = [text.find(heading) for heading in headings]
    for heading, position in zip(headings, positions):
        if position < 0:
            errors.append(f"LXF04-Lernarchitektur fehlt Überschrift: {heading}")
    present = [position for position in positions if position >= 0]
    if present != sorted(present):
        errors.append("LXF04-Lernarchitektur hat eine unerwartete Abschnittsreihenfolge")
    required_terms = [
        *LEARNING_FUNCTION_ORDER,
        "learning-task",
        "performance-task",
        "immediate-application",
        "delayed-retrieval",
        "transfer",
        "supported-exploration",
        "explicit-explanation",
    ]
    for term in required_terms:
        if term not in text:
            errors.append(f"LXF04-Lernarchitektur fehlt Vertragsbegriff: {term}")
    for variant_number in range(1, 6):
        variant_id = f"LXF04-V-{variant_number:03d}"
        if variant_id not in text:
            errors.append(f"LXF04-Lernarchitektur fehlt Reihenfolgevariante: {variant_id}")
    dimension_headings = [
        "### 1. Ziel und Sinn",
        "### 2. Vorwissen und kognitive Belastung",
        "### 3. Fachliche Lernhandlung",
        "### 4. Erklärung und Repräsentation",
        "### 5. Aufgabe und Unterstützung",
        "### 6. Feedback, Übung und Transfer",
        "### 7. Orientierung und Zugänglichkeit",
        "### 8. Lehrkraftorchestrierung",
    ]
    dimension_positions = [text.find(heading) for heading in dimension_headings]
    for heading, position in zip(dimension_headings, dimension_positions):
        if position < 0:
            errors.append(f"LXF04-Lernarchitektur fehlt Dimension: {heading}")
    if [p for p in dimension_positions if p >= 0] != sorted(
        p for p in dimension_positions if p >= 0
    ):
        errors.append("LXF04-Lernarchitektur hat eine unerwartete Dimensionsreihenfolge")
    if "keine universelle" not in text.casefold() and "keine abschließende" not in text.casefold():
        errors.append("LXF04-Lernarchitektur muss die nicht-universelle Reihenfolge erklären")
    return errors


def validate_material_patterns(
    data: object,
    learning_architecture: object,
    evidence_register: object,
) -> list[str]:
    if not isinstance(data, dict):
        return ["LXF05-Materialgrammatik muss ein Objekt sein"]

    errors: list[str] = []

    def nested_strings(value: object) -> list[str]:
        if isinstance(value, str):
            return [value]
        if isinstance(value, list):
            return [text for item in value for text in nested_strings(item)]
        if isinstance(value, dict):
            return [text for item in value.values() for text in nested_strings(item)]
        return []

    def has_concrete_product_or_copy(text: str) -> bool:
        return any(
            pattern.search(text)
            for pattern in (
                MATERIAL_PATTERN_PRODUCT_FEATURE_PATTERN,
                MATERIAL_PATTERN_VISUAL_SPEC_PATTERN,
                MATERIAL_PATTERN_LEARNER_UI_COPY_PATTERN,
            )
        )
    errors.extend(
        _unknown_fields(data, MATERIAL_PATTERN_FIELDS, "LXF05-Materialgrammatik")
    )
    errors.extend(
        _missing_fields(data, MATERIAL_PATTERN_FIELDS, "LXF05-Materialgrammatik")
    )
    if not _is_plain_int(data.get("schemaVersion")) or data.get("schemaVersion") != 1:
        errors.append("LXF05-Materialgrammatik schemaVersion muss 1 sein")
    if data.get("projectId") != "ium-lernwerk":
        errors.append("LXF05-Materialgrammatik projectId muss ium-lernwerk sein")
    if not _is_iso_date(data.get("asOf")):
        errors.append("LXF05-Materialgrammatik asOf muss ein echtes Kalenderdatum sein")

    scope = data.get("scope")
    if not isinstance(scope, dict):
        errors.append("LXF05-Materialgrammatik benötigt scope")
    else:
        errors.extend(_unknown_fields(scope, MATERIAL_PATTERN_SCOPE_FIELDS, "LXF05-Scope"))
        errors.extend(_missing_fields(scope, MATERIAL_PATTERN_SCOPE_FIELDS, "LXF05-Scope"))
        grade_errors, grades = _validate_lxf03_grades(scope.get("grades"), "LXF05-Scope")
        errors.extend(grade_errors)
        if set(grades) != REQUIREMENT_GRADES:
            errors.append("LXF05-Scope muss genau die Klassen 5, 6 und 7 umfassen")
        expected_scope = {
            "schoolType": "Gymnasium Baden-Württemberg",
            "level": "E",
            "maturity": "working",
            "contentProduction": "frozen",
            "productBinding": "product-neutral",
        }
        for field, expected in expected_scope.items():
            if scope.get(field) != expected:
                errors.append(f"LXF05-Scope {field} muss {expected} sein")

    policies = data.get("policies")
    if not isinstance(policies, dict):
        errors.append("LXF05-Materialgrammatik benötigt policies")
    else:
        errors.extend(
            _unknown_fields(policies, MATERIAL_PATTERN_POLICY_FIELDS, "LXF05-Policies")
        )
        errors.extend(
            _missing_fields(policies, MATERIAL_PATTERN_POLICY_FIELDS, "LXF05-Policies")
        )
        for field in sorted(MATERIAL_PATTERN_POLICY_FIELDS):
            if policies.get(field) is not False:
                errors.append(f"LXF05-Policy {field} muss false bleiben")

    principles_by_id: dict[str, dict] = {}
    functions_by_id: dict[str, dict] = {}
    if isinstance(learning_architecture, dict):
        groups = learning_architecture.get("principleGroups")
        if isinstance(groups, list):
            for group in groups:
                principles = group.get("principles") if isinstance(group, dict) else None
                if not isinstance(principles, list):
                    continue
                for principle in principles:
                    if isinstance(principle, dict) and _nonempty_string(principle.get("id")):
                        principles_by_id[principle["id"]] = principle
        grammar = learning_architecture.get("learningFunctionGrammar")
        functions = grammar.get("functions") if isinstance(grammar, dict) else None
        if isinstance(functions, list):
            functions_by_id = {
                function["id"]: function
                for function in functions
                if isinstance(function, dict) and _nonempty_string(function.get("id"))
            }
    if not principles_by_id or not functions_by_id:
        errors.append("LXF05-Materialgrammatik benötigt eine lesbare LXF04-Architektur")

    raw_claims = evidence_register.get("claims") if isinstance(evidence_register, dict) else None
    claims = raw_claims if isinstance(raw_claims, list) else []
    known_claim_ids = {
        claim["id"]
        for claim in claims
        if isinstance(claim, dict) and _nonempty_string(claim.get("id"))
    }
    if not known_claim_ids:
        errors.append("LXF05-Materialgrammatik benötigt ein lesbares LXF02-Evidenzregister")

    patterns = data.get("patterns")
    patterns_by_id: dict[str, dict] = {}
    families: set[str] = set()
    if not isinstance(patterns, list) or not patterns:
        errors.append("LXF05-Materialgrammatik benötigt patterns")
        patterns = []
    for position, pattern in enumerate(patterns):
        if not isinstance(pattern, dict):
            errors.append(f"LXF05-Pattern an Position {position} muss ein Objekt sein")
            continue
        pattern_id_value = pattern.get("id")
        pattern_id = pattern_id_value if _nonempty_string(pattern_id_value) else f"<Position {position}>"
        label = f"LXF05-Pattern {pattern_id}"
        errors.extend(_unknown_fields(pattern, MATERIAL_PATTERN_RECORD_FIELDS, label))
        for field in sorted(MATERIAL_PATTERN_RECORD_FIELDS - set(pattern)):
            errors.append(f"{label} benötigt {field}")
        if not _nonempty_string(pattern_id_value):
            errors.append(f"{label} benötigt id")
        elif not re.fullmatch(r"LXF05-PT-[0-9]{3}", pattern_id_value):
            errors.append(f"{label} hat eine ungültige ID")
        elif pattern_id_value in patterns_by_id:
            errors.append(f"LXF05-Materialgrammatik enthält doppelte Pattern-ID {pattern_id_value}")
        else:
            patterns_by_id[pattern_id_value] = pattern

        family = pattern.get("family")
        if not isinstance(family, str) or family not in EXPECTED_MATERIAL_PATTERN_FAMILIES:
            errors.append(f"{label} hat unbekannte Patternfamilie: {family}")
        elif family in families:
            errors.append(f"LXF05-Materialgrammatik enthält doppelte Patternfamilie: {family}")
        else:
            families.add(family)

        for field in ("title", "learnerPurpose", "teacherPurpose"):
            if not _nonempty_string(pattern.get(field)):
                errors.append(f"{label} benötigt {field}")

        function_errors, function_ids = _validate_lxf04_string_list(
            pattern.get("learningFunctionIds"), label, "learningFunctionIds"
        )
        errors.extend(function_errors)
        for function_id in function_ids:
            if function_id not in functions_by_id:
                errors.append(f"{label} referenziert unbekannte Lernfunktion {function_id}")

        principle_errors, principle_ids = _validate_lxf04_string_list(
            pattern.get("principleIds"), label, "principleIds"
        )
        errors.extend(principle_errors)
        for principle_id in principle_ids:
            principle = principles_by_id.get(principle_id)
            if principle is None:
                errors.append(f"{label} referenziert unbekanntes LXF04-Prinzip {principle_id}")
            elif principle.get("status") != "reviewed":
                errors.append(f"{label} referenziert LXF04-Prinzip {principle_id}; es ist nicht reviewed")

        applicability = pattern.get("applicability")
        if not isinstance(applicability, dict):
            errors.append(f"{label} benötigt applicability")
        else:
            errors.extend(
                _unknown_fields(
                    applicability,
                    MATERIAL_PATTERN_APPLICABILITY_FIELDS,
                    f"{label} applicability",
                )
            )
            for field in ("useWhen", "doNotUseWhen"):
                field_errors, _values = _validate_lxf04_string_list(
                    applicability.get(field), label, f"applicability.{field}"
                )
                errors.extend(field_errors)

        for field in (
            "requiredElements",
            "forbiddenElements",
            "observableChecks",
            "verificationMethods",
            "accessibilityConsiderations",
        ):
            field_errors, values = _validate_lxf04_string_list(
                pattern.get(field), label, field
            )
            errors.extend(field_errors)
            if field == "verificationMethods":
                for method in values:
                    if method not in LEARNING_ARCHITECTURE_VERIFICATION_METHODS:
                        errors.append(f"{label} hat unbekannte Prüfmethode: {method}")
                if values == ["automated-check"]:
                    errors.append(f"{label} darf nicht nur automatisiert geprüft werden")
                if not {"expert-review", "content-walkthrough"}.intersection(values):
                    errors.append(
                        f"{label} benötigt fachlichen Neutralitätsreview durch expert-review oder content-walkthrough"
                    )

        quantified_rules = pattern.get("quantifiedRules")
        narrative = [
            text
            for field in (
                "title",
                "learnerPurpose",
                "teacherPurpose",
                "requiredElements",
                "observableChecks",
                "accessibilityConsiderations",
            )
            for text in nested_strings(pattern.get(field))
            if _nonempty_string(text)
        ]
        if isinstance(applicability, dict):
            narrative.extend(
                text
                for text in nested_strings(applicability.get("useWhen"))
                if _nonempty_string(text)
            )
        if any(
            MATERIAL_PATTERN_NUMERIC_LIMIT_PATTERN.search(value)
            or MATERIAL_PATTERN_BOUNDED_COUNT_PATTERN.search(value)
            for value in narrative
        ):
            errors.append(
                f"{label} enthält eine numerische Seiten-, Element-, Minuten- oder Altersregel außerhalb quantifiedRules"
            )
        quantified_narrative = [
            rule.get("statement")
            for rule in quantified_rules
            if isinstance(rule, dict) and _nonempty_string(rule.get("statement"))
        ] if isinstance(quantified_rules, list) else []
        if any(has_concrete_product_or_copy(value) for value in narrative + quantified_narrative):
            errors.append(
                f"{label} kodiert eine konkrete Produkt-, Darstellungs- oder Lernendentextvorgabe"
            )

        product_dependencies = pattern.get("productDependencies")
        if not isinstance(product_dependencies, list):
            errors.append(f"{label} benötigt productDependencies")
        elif product_dependencies:
            errors.append(f"{label} darf keine Produktabhängigkeit enthalten")

        quantified_rules = pattern.get("quantifiedRules")
        if not isinstance(quantified_rules, list):
            errors.append(f"{label} benötigt quantifiedRules")
            quantified_rules = []
        for rule_position, rule in enumerate(quantified_rules):
            rule_label = f"{label} Mengenregel {rule_position + 1}"
            if not isinstance(rule, dict):
                errors.append(f"{rule_label} muss ein Objekt sein")
                continue
            errors.extend(
                _unknown_fields(rule, MATERIAL_PATTERN_QUANTIFIED_RULE_FIELDS, rule_label)
            )
            errors.extend(
                _missing_fields(rule, MATERIAL_PATTERN_QUANTIFIED_RULE_FIELDS, rule_label)
            )
            statement = rule.get("statement")
            if not _nonempty_string(statement):
                errors.append(f"{rule_label} benötigt statement")
            claim_errors, claim_ids = _validate_lxf04_string_list(
                rule.get("claimIds"), rule_label, "claimIds"
            )
            errors.extend(claim_errors)
            if (
                _nonempty_string(statement)
                and MATERIAL_PATTERN_NUMERIC_LIMIT_PATTERN.search(statement)
                and not claim_ids
            ):
                errors.append(f"{rule_label} als Seiten- oder Minutenregel benötigt claimIds")
            for claim_id in claim_ids:
                if claim_id not in known_claim_ids:
                    errors.append(f"{rule_label} referenziert unbekannten Claim {claim_id}")
            scope_value = rule.get("scope")
            if (
                not isinstance(scope_value, str)
                or scope_value not in MATERIAL_PATTERN_QUANTIFIED_SCOPES
            ):
                errors.append(f"{rule_label} hat unbekannten scope: {scope_value}")

        status = pattern.get("status")
        if not isinstance(status, str) or status not in MATERIAL_PATTERN_STATUSES:
            errors.append(f"{label} hat unbekannten status: {status}")

    for family in sorted(EXPECTED_MATERIAL_PATTERN_FAMILIES - families):
        errors.append(f"LXF05-Materialgrammatik fehlt Patternfamilie: {family}")
    for family in sorted(families - EXPECTED_MATERIAL_PATTERN_FAMILIES):
        errors.append(f"LXF05-Materialgrammatik enthält unerwartete Patternfamilie: {family}")

    walkthroughs = data.get("walkthroughs")
    walkthrough_ids: set[str] = set()
    referenced_pattern_ids: set[str] = set()
    if not isinstance(walkthroughs, list) or not walkthroughs:
        errors.append("LXF05-Materialgrammatik benötigt walkthroughs")
        walkthroughs = []
    for position, walkthrough in enumerate(walkthroughs):
        if not isinstance(walkthrough, dict):
            errors.append(f"LXF05-Walkthrough an Position {position} muss ein Objekt sein")
            continue
        walkthrough_id_value = walkthrough.get("id")
        walkthrough_id = walkthrough_id_value if _nonempty_string(walkthrough_id_value) else f"<Position {position}>"
        label = f"LXF05-Walkthrough {walkthrough_id}"
        errors.extend(_unknown_fields(walkthrough, MATERIAL_PATTERN_WALKTHROUGH_FIELDS, label))
        for field in sorted(MATERIAL_PATTERN_WALKTHROUGH_FIELDS - set(walkthrough)):
            errors.append(f"{label} benötigt {field}")
        if (
            not isinstance(walkthrough_id_value, str)
            or walkthrough_id_value not in EXPECTED_MATERIAL_WALKTHROUGHS
        ):
            errors.append(f"{label} hat eine unbekannte ID")
        elif walkthrough_id_value in walkthrough_ids:
            errors.append(f"LXF05-Materialgrammatik enthält doppelten Walkthrough {walkthrough_id_value}")
        else:
            walkthrough_ids.add(walkthrough_id_value)
        for field in (
            "label",
            "learnerQuestion",
            "requiredInformation",
            "action",
            "feedback",
            "teacherRole",
            "barrier",
        ):
            if not _nonempty_string(walkthrough.get(field)):
                errors.append(f"{label} benötigt {field}")
        pattern_errors, pattern_ids = _validate_lxf04_string_list(
            walkthrough.get("patternIds"), label, "patternIds"
        )
        errors.extend(pattern_errors)
        for pattern_id in pattern_ids:
            referenced_pattern_ids.add(pattern_id)
            if pattern_id not in patterns_by_id:
                errors.append(f"{label} referenziert unbekanntes Pattern {pattern_id}")
        method = walkthrough.get("verificationMethod")
        if (
            not isinstance(method, str)
            or method not in LEARNING_ARCHITECTURE_VERIFICATION_METHODS
        ):
            errors.append(f"{label} hat unbekannte verificationMethod: {method}")
        elif method == "automated-check":
            errors.append(f"{label} darf nicht nur automatisiert geprüft werden")
        walkthrough_narrative = [
            text
            for field in (
                "label",
                "learnerQuestion",
                "requiredInformation",
                "action",
                "feedback",
                "teacherRole",
                "barrier",
            )
            for text in nested_strings(walkthrough.get(field))
            if _nonempty_string(text)
        ]
        if any(
            MATERIAL_PATTERN_NUMERIC_LIMIT_PATTERN.search(value)
            or MATERIAL_PATTERN_BOUNDED_COUNT_PATTERN.search(value)
            for value in walkthrough_narrative
        ):
            errors.append(
                f"{label} enthält eine numerische Seiten-, Element-, Minuten- oder Altersregel außerhalb quantifiedRules"
            )
        if any(has_concrete_product_or_copy(value) for value in walkthrough_narrative):
            errors.append(
                f"{label} kodiert eine konkrete Produkt-, Darstellungs- oder Lernendentextvorgabe"
            )
    for walkthrough_id in sorted(EXPECTED_MATERIAL_WALKTHROUGHS - walkthrough_ids):
        errors.append(f"LXF05-Materialgrammatik fehlt Walkthrough: {walkthrough_id}")
    unreviewed_patterns = sorted(set(patterns_by_id) - referenced_pattern_ids)
    if unreviewed_patterns:
        errors.append(
            "LXF05-Materialgrammatik lässt Pattern ohne neutralen Walkthrough: "
            + ", ".join(unreviewed_patterns)
        )
    return errors


def validate_experience_gates(data: object, architecture: object, patterns: object) -> list[str]:
    """Validate review definitions only; never award didactic or pilot approval."""
    errors: list[str] = []
    label = "LXF06"
    fields = {"schemaVersion", "projectId", "asOf", "scope", "reviewBoundary", "gates", "walkthroughBindings"}
    if not isinstance(data, dict):
        return ["LXF06-Gatevertrag muss ein Objekt sein"]
    errors.extend(_unknown_fields(data, fields, label))
    errors.extend(_missing_fields(data, fields, label))
    if type(data.get("schemaVersion")) is not int or data.get("schemaVersion") != 1:
        errors.append("LXF06 benötigt schemaVersion 1")
    if data.get("projectId") != "ium-lernwerk":
        errors.append("LXF06 hat unbekannte projectId")
    as_of = data.get("asOf")
    try:
        if not isinstance(as_of, str) or not DATE_PATTERN.fullmatch(as_of):
            raise ValueError
        calendar_date.fromisoformat(as_of)
    except ValueError:
        errors.append("LXF06 benötigt ein gültiges asOf-Datum")
    # JSON equality distinguishes false from zero, unlike Python dict equality.
    for field, expected in (("scope", EXPERIENCE_SCOPE), ("reviewBoundary", EXPERIENCE_REVIEW_BOUNDARY)):
        if json.dumps(data.get(field), sort_keys=True) != json.dumps(expected, sort_keys=True):
            errors.append(f"LXF06 {field} verletzt die Vorproduktionsgrenze")

    principles_by_id: dict[str, dict] = {}
    groups = architecture.get("principleGroups") if isinstance(architecture, dict) else None
    for group in groups if isinstance(groups, list) else []:
        items = group.get("principles") if isinstance(group, dict) else None
        for item in items if isinstance(items, list) else []:
            if isinstance(item, dict) and isinstance(item.get("id"), str):
                principles_by_id[item["id"]] = item
    patterns_by_id: dict[str, dict] = {}
    items = patterns.get("patterns") if isinstance(patterns, dict) else None
    for item in items if isinstance(items, list) else []:
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            patterns_by_id[item["id"]] = item
            if item.get("status") != "reviewed":
                errors.append(f"LXF06 benötigt freigegebenes Pattern {item['id']}")
    if not principles_by_id or not patterns_by_id:
        errors.append("LXF06 benötigt LXF04- und LXF05-Voraussetzungen")

    gates = data.get("gates")
    if not isinstance(gates, list):
        errors.append("LXF06 gates muss eine Liste sein")
        gates = []
    if len(gates) != len(EXPERIENCE_GATE_IDS):
        errors.append("LXF06 benötigt genau zwölf Pflichtgates")
    seen: set[str] = set()
    gate_fields = {
        "id", "title", "question", "evidenceRequired", "method", "principleIds",
        "patternIds", "passCondition", "failAction", "ownerRole", "statusEffect",
    }
    for position, gate in enumerate(gates):
        if not isinstance(gate, dict):
            errors.append(f"LXF06 Gate {position} muss ein Objekt sein")
            continue
        gate_id = gate.get("id")
        gate_label = f"LXF06 Gate {gate_id}" if isinstance(gate_id, str) else f"LXF06 Gate {position}"
        errors.extend(_unknown_fields(gate, gate_fields, gate_label))
        errors.extend(_missing_fields(gate, gate_fields, gate_label))
        if not isinstance(gate_id, str) or gate_id not in EXPERIENCE_GATE_IDS:
            errors.append(f"{gate_label} hat unbekannte id")
        elif gate_id in seen:
            errors.append(f"{gate_label} ist doppelt")
        else:
            seen.add(gate_id)
        for field in ("title", "question", "passCondition", "failAction"):
            if not _nonempty_string(gate.get(field)):
                errors.append(f"{gate_label} benötigt {field}")
        lists = {}
        for field in ("evidenceRequired", "method", "principleIds", "patternIds"):
            field_errors, values = _validate_lxf04_string_list(gate.get(field), gate_label, field)
            errors.extend(field_errors)
            lists[field] = values
        methods = set(lists["method"])
        if not methods <= LEARNING_ARCHITECTURE_VERIFICATION_METHODS:
            errors.append(f"{gate_label} hat unbekannte Prüfmethode")
        if gate_id == "evidence-integrity":
            if "source-review" not in methods:
                errors.append(f"{gate_label} benötigt source-review")
        elif not methods.intersection({"expert-review", "content-walkthrough"}):
            errors.append(f"{gate_label} benötigt fachlichen Review; Automation oder spätere Nutzung allein reicht nicht")
        if gate_id == "accessibility-and-equivalence" and "accessibility-audit" not in methods:
            errors.append(f"{gate_label} benötigt accessibility-audit und fachlichen Äquivalenzreview")
        for field, targets in (("principleIds", principles_by_id), ("patternIds", patterns_by_id)):
            for reference in lists[field]:
                target = targets.get(reference)
                if target is None or target.get("status") != "reviewed":
                    errors.append(f"{gate_label} benötigt bekannte, reviewed {field}: {reference}")
        role = gate.get("ownerRole")
        if not isinstance(role, str) or role not in EXPERIENCE_OWNER_ROLES:
            errors.append(f"{gate_label} benötigt bekannte ownerRole")
        if json.dumps(gate.get("statusEffect"), sort_keys=True) != json.dumps(EXPERIENCE_STATUS_EFFECT, sort_keys=True):
            errors.append(f"{gate_label} statusEffect darf weder Pilot, Standard noch Fundament freigeben")
    if seen != EXPERIENCE_GATE_IDS:
        errors.append("LXF06 Pflichtgates sind unvollständig")

    expected_walkthroughs = {"entry", "central-learning-action", "securing-and-reentry"}
    actual_walkthroughs = set()
    source_walkthroughs = patterns.get("walkthroughs") if isinstance(patterns, dict) else None
    for item in source_walkthroughs if isinstance(source_walkthroughs, list) else []:
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            actual_walkthroughs.add(item["id"])
    if not expected_walkthroughs <= actual_walkthroughs:
        errors.append("LXF06 benötigt die drei LXF05-Walkthroughs")
    bindings = data.get("walkthroughBindings")
    if not isinstance(bindings, list):
        errors.append("LXF06 walkthroughBindings muss eine Liste sein")
        bindings = []
    if len(bindings) != 3:
        errors.append("LXF06 benötigt drei Walkthrough-Zuordnungen")
    bound_walkthroughs: set[str] = set()
    bound_gates: set[str] = set()
    for binding in bindings:
        if not isinstance(binding, dict):
            errors.append("LXF06 Walkthrough-Zuordnung muss ein Objekt sein")
            continue
        fields = {"walkthroughId", "gateIds"}
        errors.extend(_unknown_fields(binding, fields, "LXF06 Walkthrough"))
        errors.extend(_missing_fields(binding, fields, "LXF06 Walkthrough"))
        name = binding.get("walkthroughId")
        if not isinstance(name, str) or name not in expected_walkthroughs or name in bound_walkthroughs:
            errors.append("LXF06 Walkthrough-ID ist unbekannt oder doppelt")
        else:
            bound_walkthroughs.add(name)
        list_errors, ids = _validate_lxf04_string_list(binding.get("gateIds"), "LXF06 Walkthrough", "gateIds")
        errors.extend(list_errors)
        for gate_id in ids:
            if gate_id not in seen:
                errors.append(f"LXF06 Walkthrough referenziert unbekanntes Gate {gate_id}")
            else:
                bound_gates.add(gate_id)
    if bound_walkthroughs != expected_walkthroughs or bound_gates != EXPERIENCE_GATE_IDS:
        errors.append("LXF06 Walkthrough-Zuordnungen lassen Pflichtgates ungeprüft")
    return errors


def validate_experience_gate_artifacts(root: Path) -> list[str]:
    """Check readable required artifacts and protect the independent schema contract."""
    errors = []
    for relative in (
        "roadmap/v2/foundations/learning-experience/teacher-orchestration.md",
        "roadmap/v2/foundations/learning-experience/review-form.md",
    ):
        path = root / relative
        if not path.is_file():
            continue  # Missing files are reported once via CONTROL_FILES.
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            errors.append(f"LXF06 {relative} ist nicht als UTF-8 lesbar")
        else:
            if not text.strip():
                errors.append(f"LXF06 {relative} ist leer")
    schema_path = root / "schemas/v2/experience-gates.schema.json"
    if schema_path.is_file():
        try:
            schema = load_json(schema_path)
        except (OSError, UnicodeError, json.JSONDecodeError):
            errors.append("LXF06-Schema ist kein gültiges JSON")
        else:
            canonical = json.dumps(schema, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
            if hashlib.sha256(canonical).hexdigest().upper() != EXPERIENCE_GATE_SCHEMA_SHA256:
                errors.append("LXF06-Schema weicht von der versiegelten Definition ab")
    return errors


def validate_material_patterns_schema(root: Path) -> list[str]:
    relative_path = Path("schemas/v2/material-patterns.schema.json")
    path = root / relative_path
    if not path.is_file():
        return [f"LXF05-Schema fehlt: {relative_path.as_posix()}"]
    try:
        schema = load_json(path)
    except (OSError, UnicodeError, json.JSONDecodeError):
        return [f"LXF05-Schema ist kein gültiges JSON: {relative_path.as_posix()}"]
    if not isinstance(schema, dict):
        return ["LXF05-Schema muss ein Objekt sein"]
    canonical_schema = json.dumps(
        schema,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    if hashlib.sha256(canonical_schema).hexdigest().upper() != MATERIAL_PATTERN_SCHEMA_SHA256:
        return ["LXF05-Schema weicht von der versiegelten Definition ab"]
    return []


def validate_material_experience_guide(root: Path) -> list[str]:
    path = root / "roadmap/v2/foundations/learning-experience/material-experience-guide.md"
    if not path.is_file():
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return ["LXF05-Materialleitfaden ist nicht als UTF-8 lesbar"]
    headings = [
        "# LXF05 Material- und Experience-Grammatik",
        "## Vertragsgrenzen",
        "## Globale Gestaltungsregeln",
        "## Zehn Patternfamilien",
        "## Neutrale Walkthroughs",
        "### Walkthrough 1: Einstieg und Orientierung",
        "### Walkthrough 2: Zentrale Lernhandlung",
        "### Walkthrough 3: Sicherung und Wiedereinstieg",
        "## Lehrkraftvarianten",
        "## Prüf- und Statuslogik",
        "## WU-Abgleich",
        "## Übergabegrenze",
    ]
    errors: list[str] = []
    positions = [text.find(heading) for heading in headings]
    for heading, position in zip(headings, positions):
        if position < 0:
            errors.append(f"LXF05-Materialleitfaden fehlt Überschrift: {heading}")
    present = [position for position in positions if position >= 0]
    if present != sorted(present):
        errors.append("LXF05-Materialleitfaden hat eine unerwartete Abschnittsreihenfolge")
    for family in MATERIAL_PATTERN_FAMILY_ORDER:
        if family not in text:
            errors.append(f"LXF05-Materialleitfaden fehlt Patternfamilie: {family}")
    for pattern_number in range(1, 11):
        pattern_id = f"LXF05-PT-{pattern_number:03d}"
        if pattern_id not in text:
            errors.append(f"LXF05-Materialleitfaden fehlt Pattern: {pattern_id}")
    required_terms = (
        "Kohärenz",
        "Informationshierarchie",
        "Signaling",
        "räumlich",
        "zeitlich",
        "Segmentierung",
        "progressive Offenlegung",
        "Sprache",
        "Lesbarkeit",
        "Hilfe",
        "Wahl",
        "Gamification",
        "Mediensemantik",
        "Feedbackhierarchie",
        "Status",
        "Fehlerbehebung",
        "Wiedereinstieg",
        "Print",
        "Nicht-JavaScript",
        "schmale",
        "breite",
    )
    for term in required_terms:
        if term.casefold() not in text.casefold():
            errors.append(f"LXF05-Materialleitfaden fehlt Gestaltungsbegriff: {term}")
    walkthrough_headings = (
        "### Walkthrough 1: Einstieg und Orientierung",
        "### Walkthrough 2: Zentrale Lernhandlung",
        "### Walkthrough 3: Sicherung und Wiedereinstieg",
    )
    walkthrough_ends = (
        walkthrough_headings[1],
        walkthrough_headings[2],
        "## Lehrkraftvarianten",
    )
    required_rows = (
        "Lernendenfrage",
        "Erforderliche Information",
        "Handlung",
        "Rückmeldung",
        "Lehrkraftrolle",
        "Barriere",
        "Prüfmethode",
    )
    for heading, end_heading in zip(walkthrough_headings, walkthrough_ends):
        start = text.find(heading)
        end = text.find(end_heading, start + len(heading)) if start >= 0 else -1
        if start < 0 or end < 0:
            continue
        block = text[start:end]
        lines = block.splitlines()
        header_indexes = [
            index
            for index, line in enumerate(lines)
            if line.strip() == "| Prüffeld | Abstrakte Ausprägung |"
        ]
        table_complete = len(header_indexes) == 1
        table_rows: list[list[str]] = []
        if table_complete:
            header_index = header_indexes[0]
            separator_index = header_index + 1
            table_complete = (
                separator_index < len(lines)
                and lines[separator_index].strip() == "|---|---|"
            )
            row_index = separator_index + 1
            while table_complete and row_index < len(lines):
                row = lines[row_index].strip()
                if not row.startswith("|"):
                    break
                cells = [cell.strip() for cell in row.strip("|").split("|")]
                table_rows.append(cells)
                row_index += 1
            table_complete = (
                len(table_rows) == len(required_rows)
                and all(
                    len(cells) == 2
                    and cells[0] == required_row
                    and bool(cells[1])
                    for cells, required_row in zip(table_rows, required_rows)
                )
            )
        if not table_complete:
            errors.append(
                f"LXF05-Materialleitfaden hat eine unvollständige Walkthrough-Tabelle: {heading}"
            )
    return errors


def validate_source_schemas(root: Path) -> list[str]:
    resolved_semantics = [
        {
            "if": {"properties": {"status": {"const": "resolved"}}, "required": ["status"]},
            "then": {
                "properties": {
                    "httpStatus": {"type": "integer", "minimum": 200, "maximum": 299},
                    "finalUrl": {"type": "string", "format": "uri"},
                }
            },
        },
        {
            "if": {"properties": {"status": {"const": "restricted"}}, "required": ["status"]},
            "then": {
                "properties": {
                    "httpStatus": {"enum": [401, 403]},
                    "finalUrl": {"type": "string", "format": "uri"},
                }
            },
        },
    ]
    audit_semantics = resolved_semantics + [
        {
            "if": {"properties": {"status": {"const": "missing"}}, "required": ["status"]},
            "then": {
                "properties": {
                    "httpStatus": {"enum": [404, 410]},
                    "finalUrl": {"type": "string", "format": "uri"},
                }
            },
        }
    ]
    expectations = {
        "schemas/v2/source-inventory.schema.json": {
            "id": "https://github.com/H4R7W16/ium-lernwerk/schemas/v2/source-inventory.schema.json",
            "digest": "7F7B8685A59ADF0D020FD2A2EE788BC500C3B40D7899D66E13F79945C8E46B25",
            "top": SOURCE_INVENTORY_FIELDS,
            "defs": {
                "sealedLedger": {"path", "sha256", "recordCount"},
                "locatorOverride": {
                    "sourceId",
                    "url",
                    "checkedAt",
                    "status",
                    "reason",
                    "evidencePath",
                },
                "liveCheck": {"checkedAt", "status", "httpStatus", "finalUrl"},
                "source": LXP01_SOURCE_FIELDS,
            },
            "semantics": {
                ("properties", "schemaVersion", "const"): 1,
                ("properties", "projectId", "const"): "ium-lernwerk",
                ("properties", "asOf", "format"): "date",
                ("properties", "phase0Baseline", "properties", "role", "const"): "v1-audit-input",
                ("properties", "locatorOverrides", "minItems"): 1,
                ("properties", "locatorOverrides", "maxItems"): 1,
                ("properties", "locatorOverrides", "items", "$ref"): "#/$defs/locatorOverride",
                ("properties", "lxp01Additions", "minItems"): 6,
                ("properties", "lxp01Additions", "maxItems"): 6,
                ("properties", "lxp01Additions", "items", "$ref"): "#/$defs/source",
                ("properties", "totals", "properties", "phase0", "const"): 63,
                ("properties", "totals", "properties", "lxp01Additions", "const"): 6,
                ("properties", "totals", "properties", "combined", "const"): 69,
                ("$defs", "sealedLedger", "properties", "sha256", "pattern"): "^[0-9A-F]{64}$",
                ("$defs", "sealedLedger", "properties", "recordCount", "type"): "integer",
                ("$defs", "sealedLedger", "properties", "recordCount", "minimum"): 0,
                ("$defs", "locatorOverride", "properties", "url", "format"): "uri",
                ("$defs", "locatorOverride", "properties", "checkedAt", "format"): "date",
                ("$defs", "locatorOverride", "properties", "status", "const"): "resolved",
                ("$defs", "liveCheck", "properties", "status", "enum"): ["resolved", "restricted"],
                ("$defs", "liveCheck", "properties", "httpStatus", "minimum"): 100,
                ("$defs", "liveCheck", "properties", "httpStatus", "maximum"): 599,
                ("$defs", "liveCheck", "properties", "checkedAt", "format"): "date",
                ("$defs", "liveCheck", "properties", "finalUrl", "format"): "uri",
                ("$defs", "liveCheck", "allOf"): resolved_semantics,
                ("$defs", "source", "properties", "year", "minimum"): 1900,
                ("$defs", "source", "properties", "year", "maximum"): 2026,
                ("$defs", "source", "properties", "sourceKind", "enum"): ["meta-analysis", "professional-standard"],
                ("$defs", "source", "properties", "url", "format"): "uri",
                ("$defs", "source", "properties", "verificationStatus", "enum"): ["metadata-checked", "primary-checked"],
                ("$defs", "source", "properties", "licenseStatus", "enum"): ["publisher-rights-no-open-license", "permissive-with-notice", "no-open-license-identified"],
                ("$defs", "source", "properties", "usageStatus", "enum"): ["citation-only", "reuse-with-notice", "citation-and-link-only"],
                ("$defs", "source", "properties", "accessed", "format"): "date",
                ("$defs", "source", "properties", "liveCheck", "$ref"): "#/$defs/liveCheck",
                ("$defs", "source", "properties", "migrationState", "const"): "registered-v2",
                ("$defs", "source", "properties", "claimMigration", "const"): "pending-lxf02-claim-review",
                ("$defs", "source", "properties", "recheckTriggers", "prefixItems"): [
                    {"const": "before-claim-review"},
                    {"const": "before-publication"},
                    {"const": "locator-or-license-change"},
                ],
                ("$defs", "source", "properties", "recheckTriggers", "items"): False,
            },
        },
        "schemas/v2/source-traceability.schema.json": {
            "id": "https://github.com/H4R7W16/ium-lernwerk/schemas/v2/source-traceability.schema.json",
            "digest": "D12F0CF9E067DC75ADBC3A074685290D7C90363E2A32226E14DC516C2E4F6296",
            "top": SOURCE_TRACEABILITY_FIELDS,
            "defs": {
                "entityType": {"id", "definition", "mayReference"},
                "gap": SOURCE_GAP_FIELDS,
            },
            "semantics": {
                ("properties", "schemaVersion", "const"): 1,
                ("properties", "projectId", "const"): "ium-lernwerk",
                ("properties", "asOf", "format"): "date",
                ("properties", "entityFlow", "prefixItems"): [
                    {"const": entity_type} for entity_type in EXPECTED_SOURCE_ENTITY_FLOW
                ],
                ("properties", "entityFlow", "items"): False,
                ("properties", "entityTypes", "minItems"): 6,
                ("properties", "entityTypes", "maxItems"): 6,
                ("properties", "entityTypes", "items", "$ref"): "#/$defs/entityType",
                ("properties", "sourceInventoryPath", "const"): "roadmap/v2/foundations/sources/inventory.json",
                ("properties", "claimBaseline", "properties", "path", "const"): "docs/research/phase-0/claim-ledger.json",
                ("properties", "claimBaseline", "properties", "sha256", "pattern"): "^[0-9A-F]{64}$",
                ("properties", "claimBaseline", "properties", "claimCount", "const"): 51,
                ("properties", "claimBaseline", "properties", "reviewedClaimCount", "const"): 51,
                ("properties", "claimBaseline", "properties", "uniqueSourceCount", "const"): 57,
                ("properties", "migrationRules", "properties", "releaseRelevantStatementsRequireClaimIds", "const"): True,
                ("properties", "migrationRules", "properties", "claimsRequireRegisteredSourceIds", "const"): True,
                ("properties", "migrationRules", "properties", "claimsRequirePrimaryCheckedSources", "const"): True,
                ("properties", "migrationRules", "properties", "lxp01AdditionsCreateClaims", "const"): False,
                ("properties", "migrationRules", "properties", "pendingLxp01ClaimReview", "const"): None,
                ("properties", "requiredGaps", "maxItems"): 0,
                ("properties", "optionalGaps", "minItems"): 1,
                ("properties", "optionalGaps", "maxItems"): 1,
                ("properties", "optionalGaps", "items", "$ref"): "#/$defs/gap",
                ("$defs", "entityType", "properties", "id", "enum"): list(EXPECTED_SOURCE_ENTITY_FLOW),
                ("$defs", "entityType", "properties", "mayReference", "items", "enum"): list(EXPECTED_SOURCE_ENTITY_FLOW),
                ("$defs", "entityType", "properties", "mayReference", "uniqueItems"): True,
                ("$defs", "gap", "properties", "required", "type"): "boolean",
            },
        },
        "schemas/v2/source-link-audit.schema.json": {
            "id": "https://github.com/H4R7W16/ium-lernwerk/schemas/v2/source-link-audit.schema.json",
            "digest": "91379A3E2D5675AF0540DE487F1E4BDBF4AC813586CD9EBAE0DB9AD28A7044A4",
            "top": SOURCE_LINK_AUDIT_FIELDS,
            "defs": {
                "check": {
                    "sourceId",
                    "required",
                    "locatorType",
                    "url",
                    "status",
                    "httpStatus",
                    "finalUrl",
                    "checkedAt",
                },
            },
            "semantics": {
                ("properties", "schemaVersion", "const"): 1,
                ("properties", "projectId", "const"): "ium-lernwerk",
                ("properties", "generatedAt", "format"): "date",
                ("properties", "inventoryPath", "const"): "roadmap/v2/foundations/sources/inventory.json",
                ("properties", "policy", "properties", "requiredFailure", "const"): "block-and-preserve-last-snapshot",
                ("properties", "policy", "properties", "optionalFailure", "const"): "warn-and-write",
                ("properties", "policy", "properties", "acceptedStatuses", "prefixItems"): [
                    {"const": "resolved"},
                    {"const": "restricted"},
                ],
                ("properties", "policy", "properties", "acceptedStatuses", "items"): False,
                ("properties", "summary", "properties", "total", "const"): 69,
                ("properties", "summary", "properties", "required", "const"): 68,
                ("properties", "summary", "properties", "optional", "const"): 1,
                ("properties", "checks", "minItems"): 69,
                ("properties", "checks", "maxItems"): 69,
                ("properties", "checks", "items", "$ref"): "#/$defs/check",
                ("$defs", "check", "properties", "sourceId", "pattern"): "^SRC-",
                ("$defs", "check", "properties", "required", "type"): "boolean",
                ("$defs", "check", "properties", "locatorType", "enum"): ["doi", "url", "v2-override"],
                ("$defs", "check", "properties", "url", "format"): "uri",
                ("$defs", "check", "properties", "status", "enum"): ["resolved", "restricted", "missing", "unresolved"],
                ("$defs", "check", "properties", "httpStatus", "minimum"): 100,
                ("$defs", "check", "properties", "httpStatus", "maximum"): 599,
                ("$defs", "check", "properties", "finalUrl", "format"): "uri",
                ("$defs", "check", "properties", "checkedAt", "format"): "date",
                ("$defs", "check", "allOf"): audit_semantics,
            },
        },
    }
    errors: list[str] = []
    for relative_path, expected in expectations.items():
        path = root / relative_path
        if not path.is_file():
            errors.append(f"V2-Quellenschema fehlt: {relative_path}")
            continue
        try:
            schema = load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError):
            errors.append(f"V2-Quellenschema ist kein gültiges JSON: {relative_path}")
            continue
        if not isinstance(schema, dict):
            errors.append(f"V2-Quellenschema muss ein Objekt sein: {relative_path}")
            continue
        canonical_schema = json.dumps(
            schema,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        if hashlib.sha256(canonical_schema).hexdigest().upper() != expected["digest"]:
            errors.append(
                f"V2-Quellenschema weicht von der versiegelten Definition ab: {relative_path}"
            )
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"V2-Quellenschema benötigt Draft 2020-12: {relative_path}")
        if schema.get("$id") != expected["id"]:
            errors.append(f"V2-Quellenschema hat eine unerwartete $id: {relative_path}")
        if schema.get("type") != "object" or schema.get("additionalProperties") is not False:
            errors.append(f"V2-Quellenschema muss top-level fail-closed sein: {relative_path}")
        if set(schema.get("required", [])) != expected["top"]:
            errors.append(f"V2-Quellenschema hat abweichende Pflichtfelder: {relative_path}")
        properties = schema.get("properties")
        if not isinstance(properties, dict) or set(properties) != expected["top"]:
            errors.append(f"V2-Quellenschema hat abweichende Properties: {relative_path}")
        definitions = schema.get("$defs")
        if not isinstance(definitions, dict):
            errors.append(f"V2-Quellenschema benötigt $defs: {relative_path}")
            continue
        for definition_name, required_fields in expected["defs"].items():
            definition = definitions.get(definition_name)
            if not isinstance(definition, dict):
                errors.append(
                    f"V2-Quellenschema benötigt Definition {definition_name}: {relative_path}"
                )
                continue
            if definition.get("type") != "object" or definition.get(
                "additionalProperties"
            ) is not False:
                errors.append(
                    f"V2-Quellenschema Definition {definition_name} muss fail-closed sein: {relative_path}"
                )
            if set(definition.get("required", [])) != required_fields:
                errors.append(
                    f"V2-Quellenschema Definition {definition_name} hat abweichende Pflichtfelder: {relative_path}"
                )
            definition_properties = definition.get("properties")
            if not isinstance(definition_properties, dict) or set(
                definition_properties
            ) != required_fields:
                errors.append(
                    f"V2-Quellenschema Definition {definition_name} hat abweichende Properties: {relative_path}"
                )
        for key_path, expected_value in expected["semantics"].items():
            actual_value: object = schema
            for key in key_path:
                if not isinstance(actual_value, dict) or key not in actual_value:
                    actual_value = None
                    break
                actual_value = actual_value[key]
            if actual_value != expected_value:
                label = (
                    "Linkstatus-Semantik"
                    if key_path[-1] == "allOf"
                    else "fachliche Semantik"
                )
                errors.append(
                    f"V2-Quellenschema {label} ist abgeschwächt: {relative_path}"
                )
    return errors


def validate_repository_report(root: Path) -> tuple[list[str], list[str]]:
    warnings: list[str] = []
    errors = [
        f"{path.as_posix()} fehlt"
        for path in CONTROL_FILES
        if not (root / path).is_file()
    ]
    validators = (
        (Path("roadmap/v2/status.json"), validate_status),
        (Path("roadmap/v2/archive/v1-baseline.json"), validate_archive),
    )
    for relative_path, validator in validators:
        path = root / relative_path
        if not path.is_file():
            continue
        try:
            data = load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError):
            errors.append(f"{relative_path.as_posix()} ist kein gültiges JSON")
            continue
        errors.extend(validator(data))

    requirements_path = Path("roadmap/v2/requirements/requirements.json")
    path = root / requirements_path
    requirement_ids: set[str] = set()
    requirements_register: object = {}
    if path.is_file():
        try:
            data = load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError):
            errors.append(f"{requirements_path.as_posix()} ist kein gültiges JSON")
        else:
            requirements_register = data
            errors.extend(validate_requirements(data, root, warnings))
            if isinstance(data, dict) and isinstance(data.get("requirements"), list):
                requirement_ids = {
                    requirement["id"]
                    for requirement in data["requirements"]
                    if isinstance(requirement, dict)
                    and _nonempty_string(requirement.get("id"))
                }

    curriculum_contracts = (
        (
            Path("roadmap/v2/foundations/curriculum/source-basis.json"),
            lambda payload: validate_curriculum_source_basis(payload, root),
        ),
        (
            Path("roadmap/v2/foundations/curriculum/gap-assessments.json"),
            lambda payload: validate_curriculum_gap_assessments(payload, root),
        ),
        (
            Path("roadmap/v2/foundations/curriculum/status.json"),
            lambda payload: validate_foundation_status(
                payload,
                "curriculum",
                requirement_ids,
                root,
                warnings,
            ),
        ),
    )
    for relative_path, validator in curriculum_contracts:
        path = root / relative_path
        if not path.is_file():
            continue
        try:
            data = load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError):
            errors.append(f"{relative_path.as_posix()} ist kein gültiges JSON")
            continue
        errors.extend(validator(data))

    source_contracts = (
        (
            Path("roadmap/v2/foundations/sources/inventory.json"),
            lambda payload: validate_source_inventory(payload, root),
        ),
        (
            Path("roadmap/v2/foundations/sources/traceability.json"),
            lambda payload: validate_source_traceability(payload, root, warnings),
        ),
        (
            Path("roadmap/v2/foundations/sources/link-audit.json"),
            lambda payload: validate_source_link_audit(payload, root, warnings),
        ),
        (
            Path("roadmap/v2/foundations/sources/source-register.json"),
            lambda payload: validate_v2_source_register(payload, root),
        ),
        (
            Path("roadmap/v2/foundations/sources/status.json"),
            lambda payload: validate_foundation_status(
                payload,
                "sources",
                requirement_ids,
                root,
                warnings,
            ),
        ),
    )
    for relative_path, validator in source_contracts:
        path = root / relative_path
        if not path.is_file():
            continue
        try:
            data = load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError):
            errors.append(f"{relative_path.as_posix()} ist kein gültiges JSON")
            continue
        errors.extend(validator(data))
    errors.extend(
        error
        for error in validate_source_schemas(root)
        if not error.startswith("V2-Quellenschema fehlt:")
    )

    legacy_audit_path = Path(
        "roadmap/v2/foundations/learning-experience/legacy-audit.json"
    )
    path = root / legacy_audit_path
    if path.is_file():
        try:
            data = load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError):
            errors.append(f"{legacy_audit_path.as_posix()} ist kein gültiges JSON")
        else:
            errors.extend(validate_legacy_learning_audit(data, root))
    errors.extend(
        error
        for error in validate_legacy_learning_audit_schema(root)
        if not error.startswith("LXF01-Schema fehlt:")
    )
    errors.extend(validate_legacy_learning_audit_markdown(root))

    v2_source_register: object = {}
    v2_source_path = Path("roadmap/v2/foundations/sources/source-register.json")
    path = root / v2_source_path
    if path.is_file():
        try:
            v2_source_register = load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError):
            v2_source_register = {}

    learning_evidence_register: object = {}
    evidence_register_path = Path(
        "roadmap/v2/foundations/learning-experience/evidence-register.json"
    )
    path = root / evidence_register_path
    if path.is_file():
        try:
            data = load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError):
            errors.append(f"{evidence_register_path.as_posix()} ist kein gültiges JSON")
        else:
            learning_evidence_register = data
            errors.extend(
                validate_learning_evidence_register(data, v2_source_register)
            )
    errors.extend(
        error
        for error in validate_learning_evidence_schema(root)
        if not error.startswith("LXF02-Schema fehlt:")
    )
    errors.extend(validate_learning_evidence_synthesis(root))

    learner_profile: object = {}
    learner_profile_path = Path(
        "roadmap/v2/foundations/learning-experience/learner-profile.json"
    )
    path = root / learner_profile_path
    if path.is_file():
        try:
            data = load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError):
            errors.append(f"{learner_profile_path.as_posix()} ist kein gültiges JSON")
        else:
            learner_profile = data
            errors.extend(
                validate_learner_profile(data, learning_evidence_register, root)
            )
    errors.extend(
        error
        for error in validate_learner_profile_schema(root)
        if not error.startswith("LXF03-Schema fehlt:")
    )
    errors.extend(validate_learner_profile_markdown(root))

    learning_architecture_path = Path(
        "roadmap/v2/foundations/learning-experience/learning-architecture.json"
    )
    learning_architecture: object = {}
    path = root / learning_architecture_path
    if path.is_file():
        try:
            data = load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError):
            errors.append(
                f"{learning_architecture_path.as_posix()} ist kein gültiges JSON"
            )
        else:
            learning_architecture = data
            errors.extend(
                validate_learning_architecture(
                    data,
                    learning_evidence_register,
                    learner_profile,
                    requirements_register,
                )
            )
    errors.extend(
        error
        for error in validate_learning_design_schema(root)
        if not error.startswith("LXF04-Schema fehlt:")
    )
    errors.extend(validate_learning_architecture_markdown(root))

    material_patterns_path = Path(
        "roadmap/v2/foundations/learning-experience/material-patterns.json"
    )
    material_patterns: object = {}
    path = root / material_patterns_path
    if path.is_file():
        try:
            data = load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError):
            errors.append(f"{material_patterns_path.as_posix()} ist kein gültiges JSON")
        else:
            material_patterns = data
            errors.extend(
                validate_material_patterns(
                    data,
                    learning_architecture,
                    learning_evidence_register,
                )
            )
    errors.extend(
        error
        for error in validate_material_patterns_schema(root)
        if not error.startswith("LXF05-Schema fehlt:")
    )
    errors.extend(validate_material_experience_guide(root))
    experience_gates_path = root / "roadmap/v2/foundations/learning-experience/experience-gates.json"
    if experience_gates_path.is_file():
        try:
            data = load_json(experience_gates_path)
        except (OSError, UnicodeError, json.JSONDecodeError):
            errors.append("LXF06 experience-gates.json ist kein gültiges JSON")
        else:
            errors.extend(validate_experience_gates(data, learning_architecture, material_patterns))
    errors.extend(validate_experience_gate_artifacts(root))
    return errors, warnings


def validate_repository(root: Path) -> list[str]:
    errors, _warnings = validate_repository_report(root)
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors, warnings = validate_repository_report(root)
    for warning in warnings:
        print(f"WARNUNG: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print("V2 re-baseline validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
