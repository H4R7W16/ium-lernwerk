import copy
import json
import hashlib
from pathlib import Path
import tempfile
import unittest

import scripts.validate_v2_rebaseline as v2_validator
from scripts.validate_v2_rebaseline import (
    validate_repository,
    validate_repository_report,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MISSING_CURRICULUM_CONTRACTS = [
    "roadmap/v2/foundations/curriculum/status.json fehlt",
    "roadmap/v2/foundations/curriculum/source-basis.json fehlt",
    "roadmap/v2/foundations/curriculum/gap-assessments.json fehlt",
]
MISSING_SOURCE_CONTRACTS = [
    "roadmap/v2/foundations/sources/status.json fehlt",
    "roadmap/v2/foundations/sources/inventory.json fehlt",
    "roadmap/v2/foundations/sources/traceability.json fehlt",
    "roadmap/v2/foundations/sources/link-audit.json fehlt",
    "roadmap/v2/foundations/sources/source-register.json fehlt",
    "schemas/v2/source-inventory.schema.json fehlt",
    "schemas/v2/source-traceability.schema.json fehlt",
    "schemas/v2/source-link-audit.schema.json fehlt",
]
MISSING_LEARNING_EXPERIENCE_CONTRACTS = [
    "roadmap/v2/foundations/learning-experience/legacy-audit.json fehlt",
    "roadmap/v2/foundations/learning-experience/legacy-audit.md fehlt",
    "schemas/v2/legacy-learning-audit.schema.json fehlt",
    "roadmap/v2/foundations/learning-experience/evidence-register.json fehlt",
    "roadmap/v2/foundations/learning-experience/evidence-synthesis.md fehlt",
    "schemas/v2/learning-evidence.schema.json fehlt",
    "roadmap/v2/foundations/learning-experience/learner-profile.json fehlt",
    "roadmap/v2/foundations/learning-experience/learner-profile.md fehlt",
    "schemas/v2/learner-profile.schema.json fehlt",
    "roadmap/v2/foundations/learning-experience/learning-architecture.json fehlt",
    "roadmap/v2/foundations/learning-experience/learning-architecture.md fehlt",
    "schemas/v2/learning-design.schema.json fehlt",
    "roadmap/v2/foundations/learning-experience/material-patterns.json fehlt",
    "roadmap/v2/foundations/learning-experience/material-experience-guide.md fehlt",
    "schemas/v2/material-patterns.schema.json fehlt",
    "roadmap/v2/foundations/learning-experience/experience-gates.json fehlt",
    "roadmap/v2/foundations/learning-experience/teacher-orchestration.md fehlt",
    "roadmap/v2/foundations/learning-experience/review-form.md fehlt",
    "schemas/v2/experience-gates.schema.json fehlt",
    "roadmap/v2/foundations/learning-experience/status.json fehlt",
    "roadmap/v2/foundations/learning-experience/validation-report.md fehlt",
]
MISSING_GOVERNANCE_CONTRACTS = [
    "roadmap/v2/foundations/governance/governance-contract.json fehlt",
    "roadmap/v2/foundations/governance/status.json fehlt",
    "roadmap/v2/foundations/governance/README.md fehlt",
    "roadmap/v2/foundations/governance/inventory.md fehlt",
    "roadmap/v2/foundations/governance/validation-report.md fehlt",
    "schemas/v2/governance.schema.json fehlt",
]
MISSING_FOUNDATION_CONTRACTS = (
    MISSING_CURRICULUM_CONTRACTS
    + MISSING_SOURCE_CONTRACTS
    + MISSING_LEARNING_EXPERIENCE_CONTRACTS
    + MISSING_GOVERNANCE_CONTRACTS
)

EXPECTED_LP_CLAIMS = {f"CLAIM-LP-{number:03d}" for number in range(1, 14)}
EXPECTED_PRINCIPLES = {f"PRIN-{number:03d}" for number in range(1, 16)}
EXPECTED_LXP_SPECS = {"LXP01", "LXP02", "LXP03", "LXP04"}
LEGACY_DECISIONS = {"retain", "adapt", "replace", "reference-only", "drop"}
EXPECTED_LXF02_ADDITIONAL_SOURCES = {
    "SRC-V2-LXF-SDT-2024",
    "SRC-V2-LXF-SEGMENT-2019",
    "SRC-V2-LXF-SIGNAL-2016",
    "SRC-V2-LXF-W3C-COGA-2021",
    "SRC-V2-LXF-UDL30-2024",
    "SRC-V2-LXF-COS-2023",
    "SRC-V2-LXF-MAYER-2024",
    "SRC-V2-LXF-ICAP-2014",
    "SRC-V2-LXF-EEF-META-2025",
    "SRC-V2-LXF-WCAG22-2024",
}

VALID_LXF02_SOURCE_REGISTER = {
    "schemaVersion": 1,
    "projectId": "ium-lernwerk",
    "asOf": "2026-09-03",
    "sources": [
        {
            "id": "SRC-TEST-META",
            "title": "Geprüfte Meta-Analyse",
            "authors": ["Test Author"],
            "year": 2024,
            "sourceKind": "meta-analysis",
            "url": "https://doi.org/10.1000/test",
            "doi": "10.1000/test",
            "accessed": "2026-09-03",
            "verificationStatus": "primary-checked",
            "licenseStatus": "publisher-rights-no-open-license",
            "usageStatus": "citation-only",
            "relevance": ["test"],
            "updateRisk": "low",
        },
        {
            "id": "SRC-TEST-STANDARD",
            "title": "Professionelle Leitlinie",
            "authors": ["Test Organisation"],
            "year": 2024,
            "sourceKind": "professional-standard",
            "url": "https://example.org/standard",
            "doi": None,
            "accessed": "2026-09-03",
            "verificationStatus": "primary-checked",
            "licenseStatus": "use-status-documented",
            "usageStatus": "citation-and-link-only",
            "relevance": ["test"],
            "updateRisk": "medium",
        },
    ],
}

VALID_LXF02_EVIDENCE_REGISTER = {
    "schemaVersion": 1,
    "asOf": "2026-09-03",
    "claims": [
        {
            "id": "CLAIM-TEST-001",
            "statement": "Ein begrenzter Testclaim wird geprüft.",
            "mechanism": "Der angenommene Mechanismus ist explizit benannt.",
            "scope": "Testumfang ohne Verallgemeinerung.",
            "learnerContext": "Lernende in einem dokumentierten Testkontext.",
            "boundaryConditions": ["Keine Übertragung außerhalb des Testkontexts."],
            "sourceIds": ["SRC-TEST-META"],
            "evidenceLevel": "medium",
            "status": "reviewed",
        }
    ],
}

EXPECTED_LXF03_DIMENSIONS = {
    "prior-knowledge-and-conceptions",
    "reading-and-disciplinary-language",
    "attention-and-working-memory-load",
    "digital-operation-routines",
    "self-regulation-and-help-use",
    "motivation-and-perceived-purpose",
    "access-barriers-and-expression",
    "classroom-collaboration-and-orchestration",
}


def make_valid_lxf03_dimension(dimension_id: str, number: int) -> dict:
    return {
        "id": dimension_id,
        "label": f"Testdimension {number}",
        "evidenceSupportedAssumptions": [
            {
                "id": f"LXF03-S-{number:03d}",
                "statement": "Eine aktuelle, aufgabenbezogene Annahme wird geprüft.",
                "claimIds": ["CLAIM-TEST-001"],
                "grades": [5, 6, 7],
                "variability": (
                    "Vorwissen, Erfahrung und Unterstützungsbedarf können innerhalb "
                    "jedes Jahrgangs variieren."
                ),
                "designConsequence": {
                    "learnerMaterial": (
                        "Das Material bietet einen sichtbaren Zugang zur Aufgabe."
                    ),
                    "teacherOrchestration": (
                        "Die Lehrkraft prüft das aktuelle Produkt und passt Hilfen an."
                    ),
                },
                "status": "working",
                "limitations": [
                    "Die Aussage beschreibt keine stabile Eigenschaft einer Person."
                ],
            }
        ],
        "curriculumAndProjectExpectations": [
            {
                "id": f"LXF03-E-{number:03d}",
                "basis": "project-decision",
                "statement": "Der Lernprozess bleibt fachlich und prüfbar ausgerichtet.",
                "grades": [5, 6, 7],
                "referenceIds": ["V2-REQ-LXF-001"],
                "limitations": [
                    "Die Projektentscheidung ist kein empirischer Wirkungsnachweis."
                ],
            }
        ],
        "openAgeSpecificQuestions": [
            {
                "id": f"LXF03-Q-{number:03d}",
                "question": "Welche Unterstützung ist im jeweiligen Jahrgang nötig?",
                "grades": [5, 6, 7],
                "decisionOwner": "LXF07",
                "implications": (
                    "Die Ausgestaltung bleibt bis zu Review und Pilotierung veränderbar."
                ),
            }
        ],
        "pilotQuestions": [
            {
                "id": f"LXF03-P-{number:03d}",
                "question": "Ist die Aufgabe ohne vermeidbare Barriere bearbeitbar?",
                "grades": [5, 6, 7],
                "evidenceNeeded": (
                    "Nicht personenbezogene Beobachtung von Produkten, Rückfragen und "
                    "der Inanspruchnahme von Hilfen."
                ),
                "privacyBoundary": "non-personal-observation-only",
            }
        ],
    }


VALID_LXF03_PROFILE = {
    "schemaVersion": 1,
    "projectId": "ium-lernwerk",
    "asOf": "2026-09-03",
    "scope": {
        "profileType": "planning-profile",
        "grades": [5, 6, 7],
        "schoolType": "Gymnasium Baden-Württemberg",
        "level": "E",
        "individualDiagnosis": "prohibited",
        "maturity": "working",
        "statementBoundaries": [
            "Das Profil beschreibt planungsrelevante Varianz, keine Durchschnittsperson.",
            (
                "Einzelantworten, Klicks, Bearbeitungszeiten und Hilfenutzung werden "
                "nicht zu stabilen Personenmerkmalen oder Defizitlabels verdichtet."
            ),
        ],
    },
    "dimensions": [
        make_valid_lxf03_dimension("prior-knowledge-and-conceptions", 1),
        make_valid_lxf03_dimension("reading-and-disciplinary-language", 2),
        make_valid_lxf03_dimension("attention-and-working-memory-load", 3),
        make_valid_lxf03_dimension("digital-operation-routines", 4),
        make_valid_lxf03_dimension("self-regulation-and-help-use", 5),
        make_valid_lxf03_dimension("motivation-and-perceived-purpose", 6),
        make_valid_lxf03_dimension("access-barriers-and-expression", 7),
        make_valid_lxf03_dimension(
            "classroom-collaboration-and-orchestration", 8
        ),
    ],
}

EXPECTED_LXF04_GROUPS = {
    "goal-and-purpose",
    "prior-knowledge-and-cognitive-load",
    "disciplinary-learning-action",
    "explanation-and-representation",
    "task-and-support",
    "feedback-practice-and-transfer",
    "orientation-and-access",
    "teacher-orchestration",
}
EXPECTED_LXF04_FUNCTIONS = {
    "orient",
    "surface-prior-knowledge",
    "open-disciplinary-problem",
    "explain-or-model",
    "guided-action",
    "independent-application",
    "use-feedback",
    "secure-and-transfer",
}


def make_valid_lxf04_principle(number: int) -> dict:
    return {
        "id": f"LXF04-PR-{number:03d}",
        "title": f"Testprinzip {number}",
        "decision": "Die Lernhandlung und ihr Nachweis werden zusammen geplant.",
        "claimIds": ["CLAIM-TEST-001"],
        "decisionBasis": "V2-REQ-001; LXF03-S-001; LXF03-E-001",
        "obligation": "required",
        "appliesTo": ["learner-material", "teacher-orchestration"],
        "positivePatterns": [
            "Eine fachliche Handlung führt zu einem prüfbaren Lernprodukt."
        ],
        "antiPatterns": [
            "Eine sichtbare Aktivität wird ohne fachlichen Nachweis als Lernen gewertet."
        ],
        "observableCriteria": [
            "Ziel, Handlung und Lernprodukt benennen dieselbe fachliche Beziehung."
        ],
        "verificationMethods": ["content-walkthrough"],
        "status": "reviewed",
    }


def make_valid_lxf04_function(function_id: str, number: int) -> dict:
    return {
        "id": function_id,
        "label": f"Testfunktion {number}",
        "purpose": "Eine klar begrenzte Funktion im Lernprozess erfüllen.",
        "observableOutput": "Ein aufgabenbezogenes Zwischen- oder Lernprodukt.",
        "teacherRole": "Die Lehrkraft prüft Produkt und Übergangsbedingung.",
        "boundaries": [
            "Die Funktion erzwingt weder eine eigene Seite noch eine feste Dauer."
        ],
    }


VALID_LXF04_ARCHITECTURE = {
    "schemaVersion": 1,
    "projectId": "ium-lernwerk",
    "asOf": "2026-09-03",
    "scope": {
        "grades": [5, 6, 7],
        "schoolType": "Gymnasium Baden-Württemberg",
        "level": "E",
        "maturity": "working",
        "contentProduction": "frozen",
    },
    "principleGroups": [
        {
            "id": group_id,
            "label": f"Testgruppe {number}",
            "principles": [make_valid_lxf04_principle(number)],
        }
        for number, group_id in enumerate(
            (
                "goal-and-purpose",
                "prior-knowledge-and-cognitive-load",
                "disciplinary-learning-action",
                "explanation-and-representation",
                "task-and-support",
                "feedback-practice-and-transfer",
                "orientation-and-access",
                "teacher-orchestration",
            ),
            start=1,
        )
    ],
    "learningFunctionGrammar": {
        "universalOrder": False,
        "functions": [
            make_valid_lxf04_function(function_id, number)
            for number, function_id in enumerate(
                (
                    "orient",
                    "surface-prior-knowledge",
                    "open-disciplinary-problem",
                    "explain-or-model",
                    "guided-action",
                    "independent-application",
                    "use-feedback",
                    "secure-and-transfer",
                ),
                start=1,
            )
        ],
        "transitions": [
            {
                "id": "LXF04-T-001",
                "from": "orient",
                "to": "surface-prior-knowledge",
                "pedagogicalRationale": (
                    "Zielklarheit richtet die anschließende Aktivierung aus."
                ),
                "conditions": ["Die Aufgabe benötigt anschlussfähiges Vorwissen."],
            },
            {
                "id": "LXF04-T-002",
                "from": "surface-prior-knowledge",
                "to": "open-disciplinary-problem",
                "pedagogicalRationale": (
                    "Sichtbares Vorwissen begrenzt den sinnvollen Problemraum."
                ),
                "conditions": ["Die Exploration kann relevantes Vorläuferwissen erzeugen."],
            },
            {
                "id": "LXF04-T-003",
                "from": "open-disciplinary-problem",
                "to": "explain-or-model",
                "pedagogicalRationale": (
                    "Die Erklärung greift erzeugte Lösungen, Fragen und Fehlwege auf."
                ),
                "conditions": ["Die Problemphase hat ein auswertbares Produkt erzeugt."],
            },
            {
                "id": "LXF04-T-004",
                "from": "explain-or-model",
                "to": "guided-action",
                "pedagogicalRationale": (
                    "Angeleitetes Handeln verarbeitet die neue Beziehung aktiv."
                ),
                "conditions": ["Die Erklärung benennt Zielwissen und Modellierung."],
            },
            {
                "id": "LXF04-T-005",
                "from": "guided-action",
                "to": "independent-application",
                "pedagogicalRationale": (
                    "Eigenständige Anwendung prüft, ob Unterstützung reduziert werden kann."
                ),
                "conditions": ["Mindestens ein angeleiteter Schritt ist nachvollziehbar."],
            },
            {
                "id": "LXF04-T-006",
                "from": "independent-application",
                "to": "use-feedback",
                "pedagogicalRationale": (
                    "Rückmeldung wird an einem eigenen Produkt handlungswirksam."
                ),
                "conditions": ["Ein revidierbares Produkt liegt vor."],
            },
            {
                "id": "LXF04-T-007",
                "from": "use-feedback",
                "to": "secure-and-transfer",
                "pedagogicalRationale": (
                    "Revision und Sicherung trennen Korrektur von späterer Übertragung."
                ),
                "conditions": ["Die Rückmeldung hat eine nächste Handlung ausgelöst."],
            },
            {
                "id": "LXF04-T-008",
                "from": "surface-prior-knowledge",
                "to": "explain-or-model",
                "pedagogicalRationale": (
                    "Bei fehlendem Vorwissen oder prozeduralem Ziel folgt frühe Erklärung."
                ),
                "conditions": ["Offene Exploration wäre nicht tragfähig."],
            },
            {
                "id": "LXF04-T-009",
                "from": "orient",
                "to": "independent-application",
                "pedagogicalRationale": (
                    "Ein Rückkehrpfad kann mit einem angekündigten Abruf beginnen."
                ),
                "conditions": ["Zielwissen wurde zuvor gesichert."],
            },
        ],
        "sequenceVariants": [
            {
                "id": "LXF04-V-001",
                "label": "Unterstützte Problemöffnung",
                "transitionIds": [
                    "LXF04-T-001",
                    "LXF04-T-002",
                    "LXF04-T-003",
                    "LXF04-T-004",
                    "LXF04-T-005",
                    "LXF04-T-006",
                    "LXF04-T-007",
                ],
                "rationale": "Konzeptuelles Zielwissen wird durch Vorläuferwissen vorbereitet.",
                "conditions": ["Vorwissen und Problemraum sind hinreichend begrenzt."],
            },
            {
                "id": "LXF04-V-002",
                "label": "Frühe explizite Erklärung",
                "transitionIds": [
                    "LXF04-T-001",
                    "LXF04-T-008",
                    "LXF04-T-004",
                    "LXF04-T-005",
                    "LXF04-T-006",
                    "LXF04-T-007",
                ],
                "rationale": "Fehlendes Vorwissen oder ein prozedurales Ziel verlangt Führung.",
                "conditions": ["Exploration würde keine nutzbare Vorstruktur erzeugen."],
            },
            {
                "id": "LXF04-V-003",
                "label": "Verzögerte Wiederaufnahme",
                "transitionIds": [
                    "LXF04-T-009",
                    "LXF04-T-006",
                    "LXF04-T-007",
                ],
                "rationale": "Ein später Abruf macht Behalten und erneute Anwendung sichtbar.",
                "conditions": ["Eine frühere Sicherung liegt vor."],
            },
        ],
        "digitalInteractions": [
            {
                "id": "LXF04-DI-001",
                "label": "Bearbeitbare Fachhandlung",
                "learningFunctionId": "guided-action",
                "purpose": "Eine fachlich relevante Handlung ausführbar und revidierbar machen.",
                "forbiddenUses": [
                    "Interaktivität ohne fachliche Funktion als Lernnachweis behandeln."
                ],
                "observableCriteria": [
                    "Die Eingabe verändert ein fachlich interpretierbares Produkt."
                ],
                "verificationMethods": ["content-walkthrough", "usability-test"],
            }
        ],
    },
    "taskTypes": [
        {
            "id": "learning-task",
            "purpose": "Den Aufbau, die Prüfung oder Revision von Verständnis ermöglichen.",
            "evidenceUse": "formative",
            "feedbackTiming": "during-learning",
            "boundaries": ["Fehler und Hilfen dürfen die Bewertung nicht verdeckt verschärfen."],
        },
        {
            "id": "performance-task",
            "purpose": "Eine zuvor aufgebaute Kompetenz unter geklärten Bedingungen zeigen.",
            "evidenceUse": "summative-or-gate",
            "feedbackTiming": "after-performance",
            "boundaries": ["Neue Unterstützung darf die geprüfte Leistung nicht verändern."],
        },
    ],
    "practiceTransferStages": [
        {
            "id": "immediate-application",
            "definition": "Zeitnahe Anwendung der gerade erklärten oder modellierten Beziehung.",
            "temporalPosition": "immediate",
            "observableEvidence": "Eine eigenständige Anwendung am nahen Fall.",
            "boundaries": ["Unmittelbarer Erfolg belegt kein verzögertes Behalten."],
        },
        {
            "id": "delayed-retrieval",
            "definition": "Spätere Wiederaufnahme ohne bloße Wiederexposition.",
            "temporalPosition": "delayed",
            "observableEvidence": "Relevante Beziehung wird erneut abgerufen und genutzt.",
            "boundaries": ["Ein optimaler Abstand ist nicht pauschal festgelegt."],
        },
        {
            "id": "transfer",
            "definition": "Anwendung relevanter Beziehungen in einer substanziell neuen Aufgabe.",
            "temporalPosition": "novel-context",
            "observableEvidence": "Begründete Übertragung auf veränderte Bedingungen.",
            "boundaries": ["Oberflächenvariation allein gilt nicht als Transfer."],
        },
    ],
    "instructionModes": [
        {
            "id": "supported-exploration",
            "claimIds": ["CLAIM-TEST-001"],
            "useWhen": ["Konzeptuelles Zielwissen und anschlussfähiges Vorwissen vorliegen."],
            "avoidWhen": ["Der Problemraum unklar oder überwiegend prozedural ist."],
            "requiredBefore": ["Zielwissen, Vorwissen und möglicher Lösungsraum sind analysiert."],
            "requiredAfter": ["Eine Erklärung greift Produkte, Fragen und Fehlwege explizit auf."],
        },
        {
            "id": "explicit-explanation",
            "claimIds": ["CLAIM-TEST-001"],
            "useWhen": ["Neues Verfahren oder fehlendes Anschlusswissen Führung verlangt."],
            "avoidWhen": ["Die Erklärung eigenes fachliches Denken vollständig ersetzt."],
            "requiredBefore": ["Zielwissen und erwartete Lernhürde sind bestimmt."],
            "requiredAfter": ["Aktive Verarbeitung und eigenständige Anwendung folgen."],
        },
    ],
}


EXPECTED_LXF05_FAMILIES = {
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
}


def make_valid_lxf05_pattern(family: str, number: int) -> dict:
    return {
        "id": f"LXF05-PT-{number:03d}",
        "family": family,
        "title": f"Testmuster {number}",
        "learnerPurpose": "Eine fachliche Beziehung sichtbar bearbeiten und prüfen.",
        "teacherPurpose": "Produkt und Unterstützungsbedarf fachlich interpretieren.",
        "learningFunctionIds": ["guided-action"],
        "principleIds": ["LXF04-PR-001"],
        "applicability": {
            "useWhen": ["Die fachliche Kernhandlung und ihr Produkt bestimmt sind."],
            "doNotUseWhen": ["Die Form nur Oberfläche oder Ablage organisieren würde."],
        },
        "requiredElements": ["Sichtbare fachliche Kernhandlung"],
        "forbiddenElements": ["Erledigungsanzeige als alleiniger Lernnachweis"],
        "observableChecks": ["Das resultierende Produkt ist fachlich interpretierbar."],
        "verificationMethods": ["content-walkthrough"],
        "accessibilityConsiderations": [
            "Die Kernhandlung besitzt einen gleichwertigen Tastatur- und Textpfad."
        ],
        "productDependencies": [],
        "quantifiedRules": [],
        "status": "working",
    }


VALID_LXF05_MATERIAL_PATTERNS = {
    "schemaVersion": 1,
    "projectId": "ium-lernwerk",
    "asOf": "2026-09-03",
    "scope": {
        "grades": [5, 6, 7],
        "schoolType": "Gymnasium Baden-Württemberg",
        "level": "E",
        "maturity": "working",
        "contentProduction": "frozen",
        "productBinding": "product-neutral",
    },
    "policies": {
        "universalPageTemplate": False,
        "universalElementLimit": False,
        "universalMinuteLimit": False,
        "decorativeGamificationDefault": False,
        "productComponentsAllowed": False,
        "learnerFacingContentAllowed": False,
    },
    "patterns": [
        make_valid_lxf05_pattern(family, number)
        for number, family in enumerate(
            (
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
            ),
            start=1,
        )
    ],
    "walkthroughs": [
        {
            "id": "entry",
            "label": "Einstieg und Orientierung",
            "patternIds": ["LXF05-PT-001"],
            "learnerQuestion": "Was ist das Ziel und womit beginne ich?",
            "requiredInformation": "Ziel, Zweck, Ausgangslage und nächster Schritt.",
            "action": "Ein aufgabenbezogenes Vorprodukt erzeugen.",
            "feedback": "Rückmeldung macht die nächste fachliche Handlung sichtbar.",
            "teacherRole": "Ausgangslagen lesen und den Übergang entscheiden.",
            "barrier": "Orientierung darf nicht von Navigationserfahrung abhängen.",
            "verificationMethod": "content-walkthrough",
        },
        {
            "id": "central-learning-action",
            "label": "Zentrale Lernhandlung",
            "patternIds": [
                "LXF05-PT-002",
                "LXF05-PT-003",
                "LXF05-PT-004",
                "LXF05-PT-005",
                "LXF05-PT-006",
                "LXF05-PT-010",
            ],
            "learnerQuestion": "Welche Beziehung soll ich bearbeiten und prüfen?",
            "requiredInformation": "Auftrag, Material, Kriterien und verfügbare Hilfe.",
            "action": "Eine fachliche Beziehung ausführen, erklären oder revidieren.",
            "feedback": "Kriterium, Produktstelle und nächster Schritt werden verbunden.",
            "teacherRole": "Beobachten, gezielt stützen und Anspruch erhalten.",
            "barrier": "Bedienung und Sprache dürfen die Kernhandlung nicht verdecken.",
            "verificationMethod": "expert-review",
        },
        {
            "id": "securing-and-reentry",
            "label": "Sicherung und Wiedereinstieg",
            "patternIds": [
                "LXF05-PT-007",
                "LXF05-PT-008",
                "LXF05-PT-009",
                "LXF05-PT-010",
            ],
            "learnerQuestion": "Was ist gesichert und wie arbeite ich später weiter?",
            "requiredInformation": "Gesicherte Beziehung, offener Stand und Rückkehrpunkt.",
            "action": "Abrufen, übertragen oder den nächsten Schritt aufnehmen.",
            "feedback": "Stand und offene Handlung bleiben ohne Wertung nachvollziehbar.",
            "teacherRole": "Sicherung prüfen und Rückkehr oder Transfer rahmen.",
            "barrier": "Fortschritt darf weder Persondiagnose noch Lernnachweis vortäuschen.",
            "verificationMethod": "usability-test",
        },
    ],
}


VALID_STATUS = {
    "schemaVersion": 1,
    "projectId": "ium-lernwerk",
    "activeBaseline": "v1",
    "v2State": "building",
    "contentProduction": "frozen",
    "lxp05": {"state": "frozen", "integration": "unmerged"},
    "cutover": {"state": "not-approved"},
}

VALID_ARCHIVE = {
    "schemaVersion": 1,
    "repository": "H4R7W16/ium-lernwerk",
    "remote": "https://github.com/H4R7W16/ium-lernwerk.git",
    "mainCommit": "dcaff3e4b6e96d8c1da3dd1d4dd56f6df6b35ef0",
    "candidateRefs": [
        {
            "ref": "origin/feat/lxp05-ium5-experience",
            "commit": "645a1d4ea3c786b08e1320954b522edf86dc9f83",
            "role": "historical-unmerged-review-candidate",
        }
    ],
    "artifactRoots": [
        "docs/research/phase-0",
        "curriculum",
        "roadmap",
        "modules",
        "packages",
        "apps",
        "pilot",
    ],
    "capturedAt": "2026-09-03",
    "statementBoundaries": [
        "V1-Artefakte sind Auditbestand und keine automatisch übernommenen V2-Standards.",
        "Technische Verifikation belegt weder didaktische Qualität noch Lernwirksamkeit.",
        "LXP05 bleibt ungemergt, eingefroren und außerhalb der wiederverwendbaren V2-Basis.",
        "Pilotierung, Veröffentlichung und Cutover sind nicht freigegeben.",
    ],
    "limitations": [
        {
            "id": "dashboard-local-commit",
            "status": "unverified-local",
            "reference": "07bc15e1e70d",
            "statement": (
                "Der im Vault dokumentierte Dashboard-Commit ist nicht als "
                "lokales oder entferntes Git-Objekt reproduzierbar."
            ),
        }
    ],
}

VALID_REQUIREMENT = {
    "id": "V2-REQ-001",
    "title": "V1 und V2 trennen",
    "statement": "V1 bleibt bis zum ausdrücklichen Cutover die aktive Baseline.",
    "domain": "governance",
    "origin": [
        {
            "kind": "vault",
            "target": (
                "2026-09-03 - Entscheidung - Kontrollierte Re-Baseline V2 "
                "und Lern-Experience-Fundament"
            ),
            "label": "Freigegebene Re-Baseline-Entscheidung",
            "required": True,
        }
    ],
    "binding": "project",
    "scope": "system",
    "grades": [5, 6, 7],
    "fulfillmentModes": ["cross-cutting"],
    "coverage": "unassessed",
    "evidence": [],
    "dependencies": [],
    "risks": ["Ein vorzeitiger Cutover vermischt V1- und V2-Aussagen."],
    "gate": "IUM-V2-CUT",
}

VALID_REQUIREMENTS = {
    "schemaVersion": 1,
    "projectId": "ium-lernwerk",
    "asOf": "2026-09-03",
    "requirements": [VALID_REQUIREMENT],
}


def write_json(root: Path, relative_path: str, payload: object) -> None:
    target = root / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_control_files(
    root: Path,
    *,
    status: object = VALID_STATUS,
    archive: object = VALID_ARCHIVE,
    requirements: object | None = None,
    include_requirements: bool = True,
) -> None:
    write_json(root, "roadmap/v2/status.json", status)
    write_json(root, "roadmap/v2/archive/v1-baseline.json", archive)
    if include_requirements:
        write_json(
            root,
            "roadmap/v2/requirements/requirements.json",
            {} if requirements is None else requirements,
        )


def load_repo_json(relative_path: str) -> object:
    return json.loads((PROJECT_ROOT / relative_path).read_text(encoding="utf-8"))


class ValidateV2RebaselineTests(unittest.TestCase):
    def test_missing_control_files_fail_closed(self) -> None:
        """Catches a validator that silently accepts an absent V2 control plane."""
        with tempfile.TemporaryDirectory() as directory:
            errors = validate_repository(Path(directory))

        self.assertIn("roadmap/v2/status.json fehlt", errors)
        self.assertIn("roadmap/v2/archive/v1-baseline.json fehlt", errors)
        self.assertIn("roadmap/v2/requirements/requirements.json fehlt", errors)
        self.assertIn(
            "roadmap/v2/foundations/curriculum/status.json fehlt",
            errors,
        )
        self.assertIn(
            "roadmap/v2/foundations/curriculum/source-basis.json fehlt",
            errors,
        )
        self.assertIn(
            "roadmap/v2/foundations/curriculum/gap-assessments.json fehlt",
            errors,
        )
        for expected_error in MISSING_SOURCE_CONTRACTS:
            self.assertIn(expected_error, errors)
        for expected_error in MISSING_LEARNING_EXPERIENCE_CONTRACTS:
            self.assertIn(expected_error, errors)

    def test_legacy_learning_audit_covers_every_required_input_once(self) -> None:
        """Catches legacy evidence being silently omitted from the V2 handoff."""
        audit = load_repo_json(
            "roadmap/v2/foundations/learning-experience/legacy-audit.json"
        )

        errors = v2_validator.validate_legacy_learning_audit(audit, PROJECT_ROOT)

        self.assertEqual([], errors)
        self.assertEqual(
            [], v2_validator.validate_legacy_learning_audit_schema(PROJECT_ROOT)
        )
        records = audit["records"]
        self.assertEqual(
            EXPECTED_LP_CLAIMS,
            {
                record["artifactId"]
                for record in records
                if record["artifactKind"] == "claim"
            },
        )
        self.assertEqual(
            EXPECTED_PRINCIPLES,
            {
                record["artifactId"]
                for record in records
                if record["artifactKind"] == "principle"
            },
        )
        self.assertEqual(
            EXPECTED_LXP_SPECS,
            {
                record["artifactId"]
                for record in records
                if record["artifactKind"] == "lxp-spec"
            },
        )
        self.assertEqual(
            {"FACH-IUM-5-7"},
            {
                record["artifactId"]
                for record in records
                if record["artifactKind"] == "fachprofil"
            },
        )
        self.assertTrue(
            {record["decision"] for record in records}.issubset(LEGACY_DECISIONS)
        )

    def test_legacy_learning_audit_rejects_missing_duplicate_and_unknown_ids(
        self,
    ) -> None:
        """Catches incomplete, duplicated, or invented legacy audit inputs."""
        audit = load_repo_json(
            "roadmap/v2/foundations/learning-experience/legacy-audit.json"
        )

        missing = copy.deepcopy(audit)
        missing["records"] = [
            record
            for record in missing["records"]
            if record["artifactId"] != "CLAIM-LP-013"
        ]
        duplicate = copy.deepcopy(audit)
        duplicate["records"].append(copy.deepcopy(duplicate["records"][0]))
        unknown = copy.deepcopy(audit)
        unknown["records"][0]["artifactId"] = "CLAIM-LP-999"

        self.assertIn(
            "LXF01-Audit fehlt Pflichtartefakt: CLAIM-LP-013",
            v2_validator.validate_legacy_learning_audit(missing, PROJECT_ROOT),
        )
        self.assertIn(
            f"LXF01-Audit enthält doppelte artifactId: {audit['records'][0]['artifactId']}",
            v2_validator.validate_legacy_learning_audit(duplicate, PROJECT_ROOT),
        )
        self.assertIn(
            "LXF01-Audit enthält unbekanntes Pflichtartefakt: CLAIM-LP-999",
            v2_validator.validate_legacy_learning_audit(unknown, PROJECT_ROOT),
        )

    def test_legacy_learning_audit_enforces_decision_contract(self) -> None:
        """Catches decisions without rationale, evidence, or a valid successor."""
        audit = load_repo_json(
            "roadmap/v2/foundations/learning-experience/legacy-audit.json"
        )
        unknown = copy.deepcopy(audit)
        unknown["records"][0]["decision"] = "keep"
        no_rationale = copy.deepcopy(audit)
        no_rationale["records"][0]["rationale"] = ""
        retained_without_evidence = copy.deepcopy(audit)
        retained_without_evidence["records"][0]["decision"] = "retain"
        retained_without_evidence["records"][0]["successorTaskId"] = None
        retained_without_evidence["records"][0]["evidence"] = []
        adapt_without_successor = copy.deepcopy(audit)
        adapt_without_successor["records"][0]["decision"] = "adapt"
        adapt_without_successor["records"][0]["successorTaskId"] = None
        terminal_with_successor = copy.deepcopy(audit)
        terminal_with_successor["records"][0]["decision"] = "reference-only"
        terminal_with_successor["records"][0]["successorTaskId"] = "LXF02"
        adapt_without_evidence = copy.deepcopy(audit)
        adapt_without_evidence["records"][0]["evidence"] = []
        invalid_external_evidence = copy.deepcopy(audit)
        invalid_external_evidence["records"][-1]["evidence"] = [
            "git:does-not-exist"
        ]

        cases = [
            (unknown, "hat unbekannte Entscheidung: keep"),
            (no_rationale, "benötigt eine Begründung"),
            (retained_without_evidence, "retain benötigt mindestens einen Beleg"),
            (adapt_without_successor, "adapt benötigt einen successorTaskId"),
            (
                terminal_with_successor,
                "reference-only benötigt successorTaskId null",
            ),
            (adapt_without_evidence, "evidence benötigt mindestens einen Beleg"),
            (invalid_external_evidence, "enthält unzulässigen externen Beleg"),
        ]
        for mutated, expected in cases:
            with self.subTest(expected=expected):
                errors = v2_validator.validate_legacy_learning_audit(
                    mutated, PROJECT_ROOT
                )
                self.assertTrue(
                    any(expected in error for error in errors),
                    msg=errors,
                )

    def test_legacy_learning_audit_preserves_known_gap_and_failure_layers(
        self,
    ) -> None:
        """Catches the audit hiding known evidence, translation, or pilot gaps."""
        audit = load_repo_json(
            "roadmap/v2/foundations/learning-experience/legacy-audit.json"
        )

        self.assertEqual(
            {
                "GAP-LXF01-SOURCE",
                "GAP-LXF01-PRINCIPLE-CONTRACT",
                "GAP-LXF01-QUALITY-CONFLATION",
                "GAP-LXF01-LXP04-SPECIFICITY",
                "GAP-LXF01-LEARNER-ASSUMPTIONS",
            },
            {finding["id"] for finding in audit["knownGaps"]},
        )
        self.assertEqual(
            {"evidence", "translation", "implementation", "pilot"},
            {layer["layer"] for layer in audit["lxp05FailureLayers"]},
        )

        missing_gap = copy.deepcopy(audit)
        missing_gap["knownGaps"] = missing_gap["knownGaps"][1:]
        errors = v2_validator.validate_legacy_learning_audit(
            missing_gap, PROJECT_ROOT
        )
        self.assertIn(
            "LXF01-Audit fehlt bekannte Lücke: GAP-LXF01-SOURCE", errors
        )

        empty_gap_evidence = copy.deepcopy(audit)
        empty_gap_evidence["knownGaps"][0]["evidence"] = []
        empty_layer_evidence = copy.deepcopy(audit)
        empty_layer_evidence["lxp05FailureLayers"][0]["evidence"] = []
        self.assertTrue(
            any(
                "LXF01-Lücke 1 evidence benötigt mindestens einen Beleg" in error
                for error in v2_validator.validate_legacy_learning_audit(
                    empty_gap_evidence, PROJECT_ROOT
                )
            )
        )
        self.assertTrue(
            any(
                "LXF01-Fehlerebene 1 evidence benötigt mindestens einen Beleg"
                in error
                for error in v2_validator.validate_legacy_learning_audit(
                    empty_layer_evidence, PROJECT_ROOT
                )
            )
        )

    def test_legacy_learning_audit_schema_is_fail_closed_and_sealed(self) -> None:
        """Catches a schema edit making contract fields optional or extensible."""
        schema = load_repo_json("schemas/v2/legacy-learning-audit.schema.json")
        schema["additionalProperties"] = True
        schema["required"].remove("knownGaps")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_json(root, "schemas/v2/legacy-learning-audit.schema.json", schema)
            errors = v2_validator.validate_legacy_learning_audit_schema(root)

        self.assertIn(
            "LXF01-Schema weicht von der versiegelten Definition ab", errors
        )
        self.assertIn("LXF01-Schema muss top-level fail-closed sein", errors)
        self.assertIn("LXF01-Schema hat abweichende Pflichtfelder", errors)

    def test_learning_evidence_claim_requires_mechanism(self) -> None:
        """Catches claims that jump from a source straight to a design slogan."""
        register = copy.deepcopy(VALID_LXF02_EVIDENCE_REGISTER)
        del register["claims"][0]["mechanism"]

        errors = v2_validator.validate_learning_evidence_register(
            register, VALID_LXF02_SOURCE_REGISTER
        )

        self.assertIn("LXF02-Claim CLAIM-TEST-001 benötigt mechanism", errors)

    def test_learning_evidence_claim_requires_boundary_conditions(self) -> None:
        """Catches an evidence claim without explicit transfer limits."""
        register = copy.deepcopy(VALID_LXF02_EVIDENCE_REGISTER)
        register["claims"][0]["boundaryConditions"] = []

        errors = v2_validator.validate_learning_evidence_register(
            register, VALID_LXF02_SOURCE_REGISTER
        )

        self.assertIn(
            "LXF02-Claim CLAIM-TEST-001 boundaryConditions benötigt mindestens einen Eintrag",
            errors,
        )

    def test_learning_evidence_claim_rejects_unknown_source_id(self) -> None:
        """Catches a dangling source-to-claim reference."""
        register = copy.deepcopy(VALID_LXF02_EVIDENCE_REGISTER)
        register["claims"][0]["sourceIds"] = ["SRC-UNKNOWN"]

        errors = v2_validator.validate_learning_evidence_register(
            register, VALID_LXF02_SOURCE_REGISTER
        )

        self.assertIn(
            "LXF02-Claim CLAIM-TEST-001 referenziert unbekannte Quelle SRC-UNKNOWN",
            errors,
        )

    def test_learning_evidence_fails_closed_on_malformed_source_collection(
        self,
    ) -> None:
        """Catches valid JSON with a non-list sources value crashing integration."""
        errors = v2_validator.validate_learning_evidence_register(
            VALID_LXF02_EVIDENCE_REGISTER,
            {"sources": 1},
        )

        self.assertIn(
            "LXF02-Evidenzregister benötigt eine Quellenliste",
            errors,
        )

    def test_reviewed_claim_requires_primary_checked_sources(self) -> None:
        """Catches reviewed claims resting only on metadata inspection."""
        sources = copy.deepcopy(VALID_LXF02_SOURCE_REGISTER)
        sources["sources"][0]["verificationStatus"] = "metadata-checked"

        errors = v2_validator.validate_learning_evidence_register(
            VALID_LXF02_EVIDENCE_REGISTER, sources
        )

        self.assertIn(
            "LXF02-Claim CLAIM-TEST-001 darf mit nicht primär geprüfter Quelle SRC-TEST-META nicht reviewed sein",
            errors,
        )

    def test_professional_standard_cannot_be_high_causal_learning_evidence(
        self,
    ) -> None:
        """Catches a professional standard being promoted to causal evidence."""
        register = copy.deepcopy(VALID_LXF02_EVIDENCE_REGISTER)
        claim = register["claims"][0]
        claim["sourceIds"] = ["SRC-TEST-STANDARD"]
        claim["evidenceLevel"] = "high"

        errors = v2_validator.validate_learning_evidence_register(
            register, VALID_LXF02_SOURCE_REGISTER
        )

        self.assertIn(
            "LXF02-Claim CLAIM-TEST-001 darf professionelle Standards nicht als hohe kausale Lerneffekt-Evidenz führen",
            errors,
        )

    def test_learning_evidence_rejects_premature_standard_status(self) -> None:
        """Catches LXF02 evidence being promoted before the later standards gate."""
        register = copy.deepcopy(VALID_LXF02_EVIDENCE_REGISTER)
        register["claims"][0]["status"] = "standard"

        errors = v2_validator.validate_learning_evidence_register(
            register, VALID_LXF02_SOURCE_REGISTER
        )

        self.assertIn(
            "LXF02-Claim CLAIM-TEST-001 darf vor LXF07 nicht standard sein",
            errors,
        )

    def test_lxf02_source_register_rejects_invalid_date_and_source_kind(self) -> None:
        """Catches plausible-looking but invalid source normalization metadata."""
        sources = copy.deepcopy(VALID_LXF02_SOURCE_REGISTER)
        sources["sources"][0]["accessed"] = "2026-02-30"
        sources["sources"][0]["sourceKind"] = "blog-summary"

        errors = v2_validator.validate_v2_source_register(sources)

        self.assertIn(
            "LXF02-Quelle SRC-TEST-META accessed muss ein echtes Kalenderdatum sein",
            errors,
        )
        self.assertIn(
            "LXF02-Quelle SRC-TEST-META hat unbekannten sourceKind: blog-summary",
            errors,
        )

    def test_learning_evidence_contract_is_wired_into_repository_gate(self) -> None:
        """Catches LXF02 files being created without fail-closed gate integration."""
        with tempfile.TemporaryDirectory() as directory:
            errors = validate_repository(Path(directory))

        for expected_error in (
            "roadmap/v2/foundations/sources/source-register.json fehlt",
            "roadmap/v2/foundations/learning-experience/evidence-register.json fehlt",
            "roadmap/v2/foundations/learning-experience/evidence-synthesis.md fehlt",
            "schemas/v2/learning-evidence.schema.json fehlt",
        ):
            self.assertIn(expected_error, errors)

    def test_real_learning_evidence_contract_is_complete_and_traceable(self) -> None:
        """Catches missing migrated claims, gap sources, or orphaned source records."""
        sources = load_repo_json(
            "roadmap/v2/foundations/sources/source-register.json"
        )
        register = load_repo_json(
            "roadmap/v2/foundations/learning-experience/evidence-register.json"
        )

        self.assertEqual([], v2_validator.validate_v2_source_register(sources))
        self.assertEqual(
            [], v2_validator.validate_learning_evidence_register(register, sources)
        )
        source_ids = {source["id"] for source in sources["sources"]}
        claim_ids = {claim["id"] for claim in register["claims"]}
        referenced_source_ids = {
            source_id
            for claim in register["claims"]
            for source_id in claim["sourceIds"]
        }
        self.assertTrue(EXPECTED_LXF02_ADDITIONAL_SOURCES.issubset(source_ids))
        self.assertTrue(EXPECTED_LP_CLAIMS.issubset(claim_ids))
        self.assertEqual(source_ids, referenced_source_ids)
        self.assertNotIn("standard", {claim["status"] for claim in register["claims"]})

    def test_learning_evidence_schema_seals_the_exact_claim_contract(self) -> None:
        """Catches optional mechanisms, open-ended claim fields, or premature standards."""
        schema = load_repo_json("schemas/v2/learning-evidence.schema.json")
        claim_schema = schema["$defs"]["claim"]
        expected_fields = {
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

        self.assertFalse(schema["additionalProperties"])
        self.assertEqual({"schemaVersion", "asOf", "claims"}, set(schema["required"]))
        self.assertFalse(claim_schema["additionalProperties"])
        self.assertEqual(expected_fields, set(claim_schema["required"]))
        self.assertEqual(expected_fields, set(claim_schema["properties"]))
        self.assertEqual(
            ["draft", "working", "reviewed", "standard"],
            claim_schema["properties"]["status"]["enum"],
        )

    def test_learning_evidence_schema_rejects_weakened_semantics(self) -> None:
        """Catches semantic schema rules being removed while field names stay intact."""
        schema = load_repo_json("schemas/v2/learning-evidence.schema.json")
        mutations = {
            "as-of-format": lambda candidate: candidate["properties"]["asOf"].pop(
                "format"
            ),
            "claim-items": lambda candidate: candidate["properties"]["claims"].pop(
                "items"
            ),
            "mechanism-min-length": lambda candidate: candidate["$defs"]["claim"][
                "properties"
            ]["mechanism"].pop("minLength"),
            "source-id-uniqueness": lambda candidate: candidate["$defs"]["claim"][
                "properties"
            ]["sourceIds"].pop("uniqueItems"),
        }

        for label, mutate in mutations.items():
            with self.subTest(mutation=label), tempfile.TemporaryDirectory() as directory:
                weakened = copy.deepcopy(schema)
                mutate(weakened)
                root = Path(directory)
                write_json(root, "schemas/v2/learning-evidence.schema.json", weakened)

                errors = v2_validator.validate_learning_evidence_schema(root)

                self.assertIn(
                    "LXF02-Schema weicht von der versiegelten Definition ab",
                    errors,
                )

    def test_learning_evidence_schema_type_errors_fail_closed_without_crashing(
        self,
    ) -> None:
        """Catches malformed schema containers crashing the schema self-check."""
        schema = load_repo_json("schemas/v2/learning-evidence.schema.json")
        mutations = {
            "required": lambda candidate: candidate.__setitem__("required", 1),
            "definitions": lambda candidate: candidate.__setitem__("$defs", 1),
            "status-schema": lambda candidate: candidate["$defs"]["claim"][
                "properties"
            ].__setitem__("status", 1),
        }

        for label, mutate in mutations.items():
            with self.subTest(mutation=label), tempfile.TemporaryDirectory() as directory:
                malformed = copy.deepcopy(schema)
                mutate(malformed)
                root = Path(directory)
                write_json(root, "schemas/v2/learning-evidence.schema.json", malformed)

                errors = v2_validator.validate_learning_evidence_schema(root)

                self.assertIn(
                    "LXF02-Schema weicht von der versiegelten Definition ab",
                    errors,
                )

    def test_learning_evidence_synthesis_covers_all_required_families(self) -> None:
        """Catches a machine-valid register without the agreed fachlich readable synthesis."""
        path = (
            PROJECT_ROOT
            / "roadmap/v2/foundations/learning-experience/evidence-synthesis.md"
        )
        text = path.read_text(encoding="utf-8")
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
        self.assertTrue(all(position >= 0 for position in positions))
        self.assertEqual(sorted(positions), positions)

    def test_learning_evidence_synthesis_rejects_empty_family_sections(self) -> None:
        """Catches an outline masquerading as a completed evidence synthesis."""
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
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = (
                root
                / "roadmap/v2/foundations/learning-experience/evidence-synthesis.md"
            )
            path.parent.mkdir(parents=True)
            path.write_text("\n\n".join(headings) + "\n", encoding="utf-8")

            errors = v2_validator.validate_learning_evidence_synthesis(root)

        self.assertIn(
            "LXF02-Evidenzsynthese Abschnitt ohne substantiellen Inhalt: ## Lernarchitektur",
            errors,
        )

    def test_learner_profile_contract_is_wired_into_repository_gate(self) -> None:
        """Catches LXF03 artifacts being optional in the repository gate."""
        with tempfile.TemporaryDirectory() as directory:
            errors = validate_repository(Path(directory))

        for expected_error in (
            "roadmap/v2/foundations/learning-experience/learner-profile.json fehlt",
            "roadmap/v2/foundations/learning-experience/learner-profile.md fehlt",
            "schemas/v2/learner-profile.schema.json fehlt",
        ):
            self.assertIn(expected_error, errors)

    def test_learner_profile_requires_traceable_bounded_statements(self) -> None:
        """Catches profile claims without evidence, grade scope, or safe consequences."""
        validator = getattr(v2_validator, "validate_learner_profile", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        expected_errors = {
            "claimIds": "benötigt claimIds",
            "grades": "benötigt grades",
            "variability": "benötigt variability",
            "designConsequence": "benötigt designConsequence",
            "status": "benötigt status",
            "limitations": "benötigt limitations",
        }

        for field, expected_error in expected_errors.items():
            with self.subTest(field=field):
                profile = copy.deepcopy(VALID_LXF03_PROFILE)
                del profile["dimensions"][0]["evidenceSupportedAssumptions"][0][
                    field
                ]
                errors = validator(
                    profile, VALID_LXF02_EVIDENCE_REGISTER, PROJECT_ROOT
                )
                self.assertTrue(
                    any(expected_error in error for error in errors), errors
                )

    def test_learner_profile_rejects_unknown_claims_and_invalid_grades(self) -> None:
        """Catches dangling evidence and age assertions outside the approved scope."""
        validator = getattr(v2_validator, "validate_learner_profile", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        profile = copy.deepcopy(VALID_LXF03_PROFILE)
        statement = profile["dimensions"][0]["evidenceSupportedAssumptions"][0]
        statement["claimIds"] = ["CLAIM-UNKNOWN"]
        statement["grades"] = [5, 8]

        errors = validator(profile, VALID_LXF02_EVIDENCE_REGISTER, PROJECT_ROOT)

        self.assertTrue(
            any("referenziert unbekannten Claim CLAIM-UNKNOWN" in error for error in errors)
        )
        self.assertTrue(
            any("grades enthält unzulässige Jahrgangsstufe 8" in error for error in errors)
        )

    def test_learner_profile_rejects_average_learner_and_harmful_inferences(
        self,
    ) -> None:
        """Catches stereotyping, click-time diagnosis, and an average-learner shortcut."""
        validator = getattr(v2_validator, "validate_learner_profile", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        average = copy.deepcopy(VALID_LXF03_PROFILE)
        average["averageLearner"] = {"grade": 6}
        stable_label = copy.deepcopy(VALID_LXF03_PROFILE)
        stable_label["dimensions"][0]["evidenceSupportedAssumptions"][0][
            "statement"
        ] = "Lernende in Klasse 5 sind digital unfähig."
        click_inference = copy.deepcopy(VALID_LXF03_PROFILE)
        click_inference["dimensions"][0]["evidenceSupportedAssumptions"][0][
            "statement"
        ] = "Eine lange Klickzeit beweist geringe Selbstregulation."

        average_errors = validator(
            average, VALID_LXF02_EVIDENCE_REGISTER, PROJECT_ROOT
        )
        label_errors = validator(
            stable_label, VALID_LXF02_EVIDENCE_REGISTER, PROJECT_ROOT
        )
        click_errors = validator(
            click_inference, VALID_LXF02_EVIDENCE_REGISTER, PROJECT_ROOT
        )

        self.assertIn(
            "LXF03-Profil darf keinen undifferenzierten averageLearner enthalten",
            average_errors,
        )
        self.assertTrue(
            any("enthält unzulässiges stabiles Defizitlabel" in error for error in label_errors)
        )
        self.assertTrue(
            any("enthält unzulässige Klickzeit-Inferenz" in error for error in click_errors)
        )

    def test_learner_profile_rejects_less_obvious_labels_and_click_inferences(
        self,
    ) -> None:
        """Catches deficit nouns and inferential click-time wording, not just adjectives."""
        profile_with_deficit = copy.deepcopy(VALID_LXF03_PROFILE)
        profile_with_deficit["dimensions"][0]["evidenceSupportedAssumptions"][0][
            "statement"
        ] = "Lernende der Klasse 5 haben ein digitales Defizit."
        profile_with_click_inference = copy.deepcopy(VALID_LXF03_PROFILE)
        profile_with_click_inference["dimensions"][0][
            "evidenceSupportedAssumptions"
        ][0][
            "statement"
        ] = "Eine lange Klickdauer lässt auf geringe Selbstregulation schließen."

        deficit_errors = v2_validator.validate_learner_profile(
            profile_with_deficit, VALID_LXF02_EVIDENCE_REGISTER, PROJECT_ROOT
        )
        click_errors = v2_validator.validate_learner_profile(
            profile_with_click_inference,
            VALID_LXF02_EVIDENCE_REGISTER,
            PROJECT_ROOT,
        )

        self.assertTrue(
            any(
                "enthält unzulässiges stabiles Defizitlabel" in error
                for error in deficit_errors
            )
        )
        self.assertTrue(
            any(
                "enthält unzulässige Klickzeit-Inferenz" in error
                for error in click_errors
            )
        )

    def test_learner_profile_guards_all_profiling_text_and_both_inference_directions(
        self,
    ) -> None:
        """Catches harmful profiling moved out of the primary statement field."""
        mutations = (
            (
                "variability",
                lambda statement: statement.__setitem__(
                    "variability", "Lernende der Klasse 5 sind digital unfähig."
                ),
                "stabiles Defizitlabel",
            ),
            (
                "teacher consequence",
                lambda statement: statement["designConsequence"].__setitem__(
                    "teacherOrchestration",
                    "Eine lange Klickzeit beweist geringe Selbstregulation.",
                ),
                "Klickzeit-Inferenz",
            ),
            (
                "inverse click inference",
                lambda statement: statement.__setitem__(
                    "statement",
                    "Geringe Selbstregulation lässt sich aus einer langen Klickzeit ableiten.",
                ),
                "Klickzeit-Inferenz",
            ),
            (
                "expectation limitation",
                lambda statement: statement.__setitem__(
                    "_expectation_limitation", "Lernende besitzen ein digitales Defizit."
                ),
                "stabiles Defizitlabel",
            ),
            (
                "unrelated negation after stable label",
                lambda statement: statement.__setitem__(
                    "statement",
                    (
                        "Lernende in Klasse 5 sind digital unfähig, aber nicht alle "
                        "benötigen dieselbe Hilfe."
                    ),
                ),
                "stabiles Defizitlabel",
            ),
            (
                "unrelated negation after click inference",
                lambda statement: statement.__setitem__(
                    "statement",
                    (
                        "Eine lange Klickzeit beweist geringe Selbstregulation, ohne "
                        "dass die Lehrkraft eingreift."
                    ),
                ),
                "Klickzeit-Inferenz",
            ),
            (
                "coordinated stable label after unrelated negation",
                lambda statement: statement.__setitem__(
                    "statement",
                    (
                        "Nicht alle benötigen dieselbe Hilfe und Lernende sind digital "
                        "unfähig."
                    ),
                ),
                "stabiles Defizitlabel",
            ),
            (
                "coordinated click inference after unrelated negation",
                lambda statement: statement.__setitem__(
                    "statement",
                    (
                        "Ohne Unterstützung bleibt die Aufgabe schwierig und eine lange "
                        "Klickzeit beweist geringe Selbstregulation."
                    ),
                ),
                "Klickzeit-Inferenz",
            ),
            (
                "unrelated collection boundary before click inference",
                lambda statement: statement.__setitem__(
                    "statement",
                    (
                        "Eine lange Klickzeit wird ohne Personenbezug erfasst und "
                        "beweist geringe Selbstregulation."
                    ),
                ),
                "Klickzeit-Inferenz",
            ),
            (
                "plural click times",
                lambda statement: statement.__setitem__(
                    "statement",
                    "Aus Klickzeiten lässt sich geringe Selbstregulation ableiten.",
                ),
                "Klickzeit-Inferenz",
            ),
            (
                "plural click durations",
                lambda statement: statement.__setitem__(
                    "statement", "Klickdauern beweisen geringe Selbstregulation."
                ),
                "Klickzeit-Inferenz",
            ),
            (
                "plural click rates",
                lambda statement: statement.__setitem__(
                    "statement", "Klickraten zeigen geringe Motivation."
                ),
                "Klickzeit-Inferenz",
            ),
            (
                "without doubt is not negation",
                lambda statement: statement.__setitem__(
                    "statement",
                    "Eine lange Klickzeit beweist ohne Zweifel geringe Selbstregulation.",
                ),
                "Klickzeit-Inferenz",
            ),
            (
                "indicates",
                lambda statement: statement.__setitem__(
                    "statement", "Viele Klicks deuten auf geringe Selbstregulation hin."
                ),
                "Klickzeit-Inferenz",
            ),
            (
                "permits conclusions",
                lambda statement: statement.__setitem__(
                    "statement",
                    "Klickzeiten erlauben Rückschlüsse auf geringe Selbstregulation.",
                ),
                "Klickzeit-Inferenz",
            ),
            (
                "speaks for",
                lambda statement: statement.__setitem__(
                    "statement", "Klickraten sprechen für geringe Motivation."
                ),
                "Klickzeit-Inferenz",
            ),
            (
                "recognizable",
                lambda statement: statement.__setitem__(
                    "statement",
                    "An Klickzahlen ist geringe Selbstregulation erkennbar.",
                ),
                "Klickzeit-Inferenz",
            ),
            (
                "can be concluded",
                lambda statement: statement.__setitem__(
                    "statement",
                    "Aus Klickdaten kann auf geringe Fähigkeit geschlossen werden.",
                ),
                "Klickzeit-Inferenz",
            ),
        )

        for label, mutate, expected_error in mutations:
            with self.subTest(field=label):
                profile = copy.deepcopy(VALID_LXF03_PROFILE)
                dimension = profile["dimensions"][0]
                statement = dimension["evidenceSupportedAssumptions"][0]
                mutate(statement)
                if "_expectation_limitation" in statement:
                    dimension["curriculumAndProjectExpectations"][0]["limitations"] = [
                        statement.pop("_expectation_limitation")
                    ]

                errors = v2_validator.validate_learner_profile(
                    profile, VALID_LXF02_EVIDENCE_REGISTER, PROJECT_ROOT
                )

                self.assertTrue(
                    any(expected_error in error for error in errors), errors
                )

    def test_learner_profile_allows_explicit_anti_diagnostic_boundaries(self) -> None:
        """Keeps negated safeguards from becoming false positive gate failures."""
        safe_statements = (
            "Lernende haben kein digitales Defizit.",
        )

        for statement_text in safe_statements:
            with self.subTest(statement=statement_text):
                profile = copy.deepcopy(VALID_LXF03_PROFILE)
                profile["dimensions"][0]["evidenceSupportedAssumptions"][0][
                    "statement"
                ] = statement_text

                errors = v2_validator.validate_learner_profile(
                    profile, VALID_LXF02_EVIDENCE_REGISTER, PROJECT_ROOT
                )

                self.assertFalse(
                    any(
                        "stabiles Defizitlabel" in error
                        or "Klickzeit-Inferenz" in error
                        for error in errors
                    ),
                    errors,
                )

    def test_learner_profile_reserves_click_telemetry_for_the_scope_boundary(
        self,
    ) -> None:
        """Makes arbitrary click-based profile prose fail closed."""
        valid_profile = copy.deepcopy(VALID_LXF03_PROFILE)
        allowed_interface_phrase = copy.deepcopy(VALID_LXF03_PROFILE)
        allowed_interface_phrase["dimensions"][0][
            "evidenceSupportedAssumptions"
        ][0]["statement"] = (
            "Fachliche Segmentierung ist nicht mit mehr Klickschritten gleichzusetzen."
        )

        valid_errors = v2_validator.validate_learner_profile(
            valid_profile, VALID_LXF02_EVIDENCE_REGISTER, PROJECT_ROOT
        )
        interface_errors = v2_validator.validate_learner_profile(
            allowed_interface_phrase, VALID_LXF02_EVIDENCE_REGISTER, PROJECT_ROOT
        )

        self.assertFalse(
            any("Klickzeit-Inferenz" in error for error in valid_errors), valid_errors
        )
        self.assertFalse(
            any("Klickzeit-Inferenz" in error for error in interface_errors),
            interface_errors,
        )

        forbidden_texts = (
            (
                "Einzelantworten, Klicks, Bearbeitungszeiten und Hilfenutzung werden "
                "nicht zu stabilen Personenmerkmalen oder Defizitlabels verdichtet."
            ),
            "Klickmetriken werden ausgewertet.",
            "Klickmuster werden ausgewertet.",
            "Mausklickmuster werden ausgewertet.",
            "Personenbezogene Telemetrie wird ausgewertet.",
            "Interaktionstelemetrie wird ausgewertet.",
            "Bearbeitungszeiten werden ausgewertet.",
            "Aufgabenbearbeitungszeiten werden ausgewertet.",
            "Hilfenutzung wird ausgewertet.",
            "Personenbezogene Systemdaten werden ausgewertet.",
            "Aktivitätsmessung wird zur Profilbildung verwendet.",
        )
        for text in forbidden_texts:
            with self.subTest(text=text):
                profile = copy.deepcopy(VALID_LXF03_PROFILE)
                profile["dimensions"][0]["evidenceSupportedAssumptions"][0][
                    "statement"
                ] = text
                errors = v2_validator.validate_learner_profile(
                    profile, VALID_LXF02_EVIDENCE_REGISTER, PROJECT_ROOT
                )
                self.assertTrue(
                    any("Klickzeit-Inferenz" in error for error in errors), errors
                )

    def test_learner_profile_rejects_unroutable_decision_owner(self) -> None:
        """Catches a hand validator that is weaker than the sealed schema."""
        profile = copy.deepcopy(VALID_LXF03_PROFILE)
        profile["dimensions"][0]["openAgeSpecificQuestions"][0][
            "decisionOwner"
        ] = "nobody"

        errors = v2_validator.validate_learner_profile(
            profile, VALID_LXF02_EVIDENCE_REGISTER, PROJECT_ROOT
        )

        self.assertTrue(
            any("hat ungültigen decisionOwner: nobody" in error for error in errors),
            errors,
        )

    def test_learner_profile_rejects_invalid_record_ids(self) -> None:
        """Catches records that cannot be stably referenced by later LXF gates."""
        profile = copy.deepcopy(VALID_LXF03_PROFILE)
        dimension = profile["dimensions"][0]
        dimension["evidenceSupportedAssumptions"][0]["id"] = "statement-one"
        dimension["curriculumAndProjectExpectations"][0]["id"] = "expectation-one"
        dimension["openAgeSpecificQuestions"][0]["id"] = "question-one"
        dimension["pilotQuestions"][0]["id"] = "pilot-one"

        errors = v2_validator.validate_learner_profile(
            profile, VALID_LXF02_EVIDENCE_REGISTER, PROJECT_ROOT
        )

        for expected_error in (
            "LXF03-Profilstatement statement-one hat eine ungültige ID",
            "LXF03-Erwartung expectation-one hat eine ungültige ID",
            "LXF03-Altersfrage question-one hat eine ungültige ID",
            "LXF03-Pilotfrage pilot-one hat eine ungültige ID",
        ):
            self.assertIn(expected_error, errors)

    def test_learner_profile_requires_exact_dimensions_and_split_consequences(
        self,
    ) -> None:
        """Catches a missing profile domain or merged learner/teacher consequence."""
        validator = getattr(v2_validator, "validate_learner_profile", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        profile = copy.deepcopy(VALID_LXF03_PROFILE)
        profile["dimensions"] = [
            dimension
            for dimension in profile["dimensions"]
            if dimension["id"] != "access-barriers-and-expression"
        ]
        del profile["dimensions"][0]["evidenceSupportedAssumptions"][0][
            "designConsequence"
        ]["teacherOrchestration"]

        errors = validator(profile, VALID_LXF02_EVIDENCE_REGISTER, PROJECT_ROOT)

        self.assertIn(
            "LXF03-Profil fehlt Dimension: access-barriers-and-expression", errors
        )
        self.assertTrue(
            any(
                "designConsequence benötigt teacherOrchestration" in error
                for error in errors
            )
        )

    def test_learner_profile_separates_curriculum_orientation_and_decisions(
        self,
    ) -> None:
        """Catches an orienting record being presented as enacted curriculum."""
        validator = getattr(v2_validator, "validate_learner_profile", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        profile = copy.deepcopy(VALID_LXF03_PROFILE)
        expectation = profile["dimensions"][0][
            "curriculumAndProjectExpectations"
        ][0]
        expectation["basis"] = "official-curriculum"
        expectation["referenceIds"] = ["LH26-E-PROG-001"]

        errors = validator(profile, VALID_LXF02_EVIDENCE_REGISTER, PROJECT_ROOT)

        self.assertTrue(
            any(
                "führt Orientierungsrecord LH26-E-PROG-001 als amtlich bindend"
                in error
                for error in errors
            )
        )

    def test_real_learner_profile_is_complete_and_traceable(self) -> None:
        """Catches incomplete real data even if a small fixture remains valid."""
        validator = getattr(v2_validator, "validate_learner_profile", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        profile = load_repo_json(
            "roadmap/v2/foundations/learning-experience/learner-profile.json"
        )
        evidence = load_repo_json(
            "roadmap/v2/foundations/learning-experience/evidence-register.json"
        )

        self.assertEqual([], validator(profile, evidence, PROJECT_ROOT))
        self.assertEqual(
            EXPECTED_LXF03_DIMENSIONS,
            {dimension["id"] for dimension in profile["dimensions"]},
        )

    def test_learner_profile_schema_is_fail_closed_and_sealed(self) -> None:
        """Catches optional profile fields or weakened anti-diagnostic semantics."""
        validator = getattr(v2_validator, "validate_learner_profile_schema", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        schema = load_repo_json("schemas/v2/learner-profile.schema.json")
        weakened = copy.deepcopy(schema)
        weakened["$defs"]["profileStatement"]["required"].remove("claimIds")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_json(root, "schemas/v2/learner-profile.schema.json", weakened)
            errors = validator(root)

        self.assertIn(
            "LXF03-Schema weicht von der versiegelten Definition ab", errors
        )

    def test_learner_profile_schema_requires_the_behavioral_boundary(self) -> None:
        """Keeps the anti-telemetry boundary in schema and hand validation alike."""
        schema = load_repo_json("schemas/v2/learner-profile.schema.json")
        boundary_schema = schema["$defs"]["scope"]["properties"][
            "statementBoundaries"
        ]

        self.assertEqual(
            {
                "const": (
                    "Einzelantworten, Klicks, Bearbeitungszeiten und Hilfenutzung "
                    "werden nicht zu stabilen Personenmerkmalen oder Defizitlabels "
                    "verdichtet."
                )
            },
            boundary_schema.get("contains"),
        )
        self.assertEqual(1, boundary_schema.get("minContains"))

    def test_learner_profile_markdown_covers_every_dimension_and_view(self) -> None:
        """Catches machine data without the agreed human review structure."""
        validator = getattr(v2_validator, "validate_learner_profile_markdown", None)
        self.assertIsNotNone(validator)
        assert validator is not None

        self.assertEqual([], validator(PROJECT_ROOT))

    def test_learner_profile_markdown_must_match_json_scope_status_and_references(
        self,
    ) -> None:
        """Catches a readable synthesis drifting away from its structured source."""
        validator = v2_validator.validate_learner_profile_markdown
        source_markdown = (
            PROJECT_ROOT
            / "roadmap/v2/foundations/learning-experience/learner-profile.md"
        ).read_text(encoding="utf-8")
        mutations = (
            ("status", source_markdown.replace("**Status:** `working`", "**Status:** `reviewed`")),
            (
                "scope",
                source_markdown.replace(
                    "Gymnasium Baden-Württemberg, Niveau E, Klassen 5–7",
                    "Gymnasium Baden-Württemberg, Niveau E, Klassen 5–6",
                ),
            ),
            ("missing reference", source_markdown.replace("CLAIM-LP-002", "CLAIM-TEST-001")),
            ("invented reference", source_markdown.replace("CLAIM-LP-002", "CLAIM-INVENTED-999")),
        )

        for label, markdown in mutations:
            with self.subTest(mutation=label), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                write_json(
                    root,
                    "roadmap/v2/foundations/learning-experience/learner-profile.json",
                    load_repo_json(
                        "roadmap/v2/foundations/learning-experience/learner-profile.json"
                    ),
                )
                target = (
                    root
                    / "roadmap/v2/foundations/learning-experience/learner-profile.md"
                )
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(markdown, encoding="utf-8")

                errors = validator(root)

                self.assertTrue(errors, label)

    def test_learner_profile_markdown_rejects_hidden_header_conflicts_and_moved_refs(
        self,
    ) -> None:
        """Catches globally present metadata or references in the wrong context."""
        validator = v2_validator.validate_learner_profile_markdown
        source_markdown = (
            PROJECT_ROOT
            / "roadmap/v2/foundations/learning-experience/learner-profile.md"
        ).read_text(encoding="utf-8")
        hidden_header_conflict = (
            source_markdown.replace("**Status:** `working`", "**Status:** `reviewed`")
            + "\n**Status:** `working`\n"
        )
        moved_reference = source_markdown.replace(
            "CLAIM-LP-002; CLAIM-LP-012", "CLAIM-LP-012"
        ).replace(
            "CLAIM-V2-LXF-COGA-001; CLAIM-V2-LXF-UDL-001",
            "CLAIM-LP-002; CLAIM-V2-LXF-COGA-001; CLAIM-V2-LXF-UDL-001",
            1,
        )

        for label, markdown in (
            ("hidden header conflict", hidden_header_conflict),
            ("moved reference", moved_reference),
        ):
            with self.subTest(mutation=label), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                write_json(
                    root,
                    "roadmap/v2/foundations/learning-experience/learner-profile.json",
                    load_repo_json(
                        "roadmap/v2/foundations/learning-experience/learner-profile.json"
                    ),
                )
                target = (
                    root
                    / "roadmap/v2/foundations/learning-experience/learner-profile.md"
                )
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(markdown, encoding="utf-8")

                errors = validator(root)

                self.assertTrue(errors, label)

    def test_learning_architecture_contract_is_wired_into_repository_gate(self) -> None:
        """Catches LXF04 artifacts being optional in the repository gate."""
        with tempfile.TemporaryDirectory() as directory:
            errors = validate_repository(Path(directory))

        for expected_error in (
            "roadmap/v2/foundations/learning-experience/learning-architecture.json fehlt",
            "roadmap/v2/foundations/learning-experience/learning-architecture.md fehlt",
            "schemas/v2/learning-design.schema.json fehlt",
        ):
            self.assertIn(expected_error, errors)

    def test_learning_architecture_principle_requires_the_complete_design_contract(
        self,
    ) -> None:
        """Catches principles that cannot be traced, applied, or reviewed."""
        validator = getattr(v2_validator, "validate_learning_architecture", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        required_fields = (
            "claimIds",
            "decisionBasis",
            "obligation",
            "positivePatterns",
            "antiPatterns",
            "observableCriteria",
            "verificationMethods",
        )

        for field in required_fields:
            with self.subTest(field=field):
                architecture = copy.deepcopy(VALID_LXF04_ARCHITECTURE)
                del architecture["principleGroups"][0]["principles"][0][field]

                errors = validator(
                    architecture,
                    VALID_LXF02_EVIDENCE_REGISTER,
                    VALID_LXF03_PROFILE,
                    VALID_REQUIREMENTS,
                )

                self.assertTrue(
                    any(f"benötigt {field}" in error for error in errors), errors
                )

    def test_learning_architecture_rejects_automation_as_the_only_review_method(
        self,
    ) -> None:
        """Catches a didactic principle being approved only by a technical check."""
        validator = getattr(v2_validator, "validate_learning_architecture", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        architecture = copy.deepcopy(VALID_LXF04_ARCHITECTURE)
        architecture["principleGroups"][0]["principles"][0][
            "verificationMethods"
        ] = ["automated-check"]

        errors = validator(
            architecture,
            VALID_LXF02_EVIDENCE_REGISTER,
            VALID_LXF03_PROFILE,
            VALID_REQUIREMENTS,
        )

        self.assertTrue(
            any("darf nicht nur automatisiert geprüft werden" in error for error in errors),
            errors,
        )

    def test_learning_architecture_fails_closed_on_malformed_enum_types(
        self,
    ) -> None:
        """Catches valid JSON containers crashing LXF04 enum membership checks."""
        validator = getattr(v2_validator, "validate_learning_architecture", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        architecture = copy.deepcopy(VALID_LXF04_ARCHITECTURE)
        principle = architecture["principleGroups"][0]["principles"][0]
        principle["obligation"] = []
        principle["status"] = {}
        architecture["learningFunctionGrammar"]["transitions"][0]["from"] = []
        architecture["learningFunctionGrammar"]["digitalInteractions"][0][
            "learningFunctionId"
        ] = {}

        errors = validator(
            architecture,
            VALID_LXF02_EVIDENCE_REGISTER,
            VALID_LXF03_PROFILE,
            VALID_REQUIREMENTS,
        )

        self.assertTrue(errors)
        self.assertTrue(any("unbekannte obligation" in error for error in errors))
        self.assertTrue(any("unbekannten status" in error for error in errors))
        self.assertTrue(
            any("referenziert unbekannte Lernfunktion" in error for error in errors)
        )

    def test_learning_architecture_dependency_indexes_fail_closed_on_scalars(
        self,
    ) -> None:
        """Catches scalar dependency collections crashing LXF04 reference indexing."""
        validator = getattr(v2_validator, "validate_learning_architecture", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        cases = (
            ("claims", "evidence", lambda value: value.__setitem__("claims", 7)),
            (
                "requirements",
                "requirements",
                lambda value: value.__setitem__("requirements", 7),
            ),
            (
                "dimensions",
                "profile",
                lambda value: value.__setitem__("dimensions", 7),
            ),
            (
                "assumptions",
                "profile",
                lambda value: value["dimensions"][0].__setitem__(
                    "evidenceSupportedAssumptions", 7
                ),
            ),
            (
                "expectations",
                "profile",
                lambda value: value["dimensions"][0].__setitem__(
                    "curriculumAndProjectExpectations", 7
                ),
            ),
        )
        for name, target, mutate in cases:
            with self.subTest(name=name):
                evidence = copy.deepcopy(VALID_LXF02_EVIDENCE_REGISTER)
                profile = copy.deepcopy(VALID_LXF03_PROFILE)
                requirements = copy.deepcopy(VALID_REQUIREMENTS)
                selected = {
                    "evidence": evidence,
                    "profile": profile,
                    "requirements": requirements,
                }[target]
                mutate(selected)

                errors = validator(
                    copy.deepcopy(VALID_LXF04_ARCHITECTURE),
                    evidence,
                    profile,
                    requirements,
                )

                self.assertTrue(errors)

    def test_learning_architecture_instruction_claims_fail_closed_on_scalar(
        self,
    ) -> None:
        """Catches a scalar instruction-mode claim collection crashing LXF04."""
        validator = getattr(v2_validator, "validate_learning_architecture", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        architecture = copy.deepcopy(VALID_LXF04_ARCHITECTURE)
        architecture["instructionModes"][0]["claimIds"] = 7

        errors = validator(
            architecture,
            VALID_LXF02_EVIDENCE_REGISTER,
            VALID_LXF03_PROFILE,
            VALID_REQUIREMENTS,
        )

        self.assertTrue(any("benötigt claimIds" in error for error in errors), errors)

    def test_learning_architecture_rejects_invalid_digital_interaction_id(
        self,
    ) -> None:
        """Keeps the hand validator aligned with the sealed interaction ID schema."""
        validator = getattr(v2_validator, "validate_learning_architecture", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        architecture = copy.deepcopy(VALID_LXF04_ARCHITECTURE)
        architecture["learningFunctionGrammar"]["digitalInteractions"][0][
            "id"
        ] = "not-a-contract-id"

        errors = validator(
            architecture,
            VALID_LXF02_EVIDENCE_REGISTER,
            VALID_LXF03_PROFILE,
            VALID_REQUIREMENTS,
        )

        self.assertTrue(any("hat eine ungültige ID" in error for error in errors), errors)

    def test_learning_architecture_requires_all_groups_and_a_required_principle(
        self,
    ) -> None:
        """Catches a missing quality dimension or an entirely optional group."""
        validator = getattr(v2_validator, "validate_learning_architecture", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        architecture = copy.deepcopy(VALID_LXF04_ARCHITECTURE)
        architecture["principleGroups"] = architecture["principleGroups"][:-1]
        architecture["principleGroups"][0]["principles"][0][
            "obligation"
        ] = "recommended"

        errors = validator(
            architecture,
            VALID_LXF02_EVIDENCE_REGISTER,
            VALID_LXF03_PROFILE,
            VALID_REQUIREMENTS,
        )

        self.assertIn(
            "LXF04-Architektur fehlt Prinzipgruppe: teacher-orchestration", errors
        )
        self.assertTrue(
            any("goal-and-purpose benötigt mindestens ein Pflichtprinzip" in error for error in errors),
            errors,
        )

    def test_learning_architecture_rejects_dangling_claim_and_decision_references(
        self,
    ) -> None:
        """Catches a design decision that no longer consumes LXF02, LXF03, and V2."""
        validator = getattr(v2_validator, "validate_learning_architecture", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        architecture = copy.deepcopy(VALID_LXF04_ARCHITECTURE)
        principle = architecture["principleGroups"][0]["principles"][0]
        principle["claimIds"] = ["CLAIM-MISSING"]
        principle["decisionBasis"] = "V2-REQ-MISSING; LXF03-S-999; LXF03-E-999"

        errors = validator(
            architecture,
            VALID_LXF02_EVIDENCE_REGISTER,
            VALID_LXF03_PROFILE,
            VALID_REQUIREMENTS,
        )

        for expected in (
            "referenziert unbekannten Claim CLAIM-MISSING",
            "referenziert unbekannte V2-Anforderung V2-REQ-MISSING",
            "referenziert unbekanntes LXF03-Statement LXF03-S-999",
            "referenziert unbekannte LXF03-Erwartung LXF03-E-999",
        ):
            self.assertTrue(any(expected in error for error in errors), errors)

    def test_learning_architecture_rejects_an_unconsumed_lxf02_claim(self) -> None:
        """Catches reviewed evidence silently disappearing during design translation."""
        validator = getattr(v2_validator, "validate_learning_architecture", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        evidence = copy.deepcopy(VALID_LXF02_EVIDENCE_REGISTER)
        extra_claim = copy.deepcopy(evidence["claims"][0])
        extra_claim["id"] = "CLAIM-TEST-UNUSED"
        evidence["claims"].append(extra_claim)

        errors = validator(
            copy.deepcopy(VALID_LXF04_ARCHITECTURE),
            evidence,
            VALID_LXF03_PROFILE,
            VALID_REQUIREMENTS,
        )

        self.assertIn(
            "LXF04-Architektur lässt LXF02-Claim ohne Designbezug: CLAIM-TEST-UNUSED",
            errors,
        )

    def test_learning_function_grammar_is_flexible_but_fail_closed(self) -> None:
        """Catches a universal page order, missing function, or unreasoned transition."""
        validator = getattr(v2_validator, "validate_learning_architecture", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        architecture = copy.deepcopy(VALID_LXF04_ARCHITECTURE)
        grammar = architecture["learningFunctionGrammar"]
        grammar["universalOrder"] = True
        grammar["functions"] = grammar["functions"][:-1]
        grammar["transitions"][0]["pedagogicalRationale"] = ""
        grammar["digitalInteractions"][0]["learningFunctionId"] = "click-through"

        errors = validator(
            architecture,
            VALID_LXF02_EVIDENCE_REGISTER,
            VALID_LXF03_PROFILE,
            VALID_REQUIREMENTS,
        )

        self.assertIn(
            "LXF04-Lernfunktionsgrammatik darf keine universelle Reihenfolge setzen",
            errors,
        )
        self.assertIn(
            "LXF04-Lernfunktionsgrammatik fehlt Funktion: secure-and-transfer",
            errors,
        )
        self.assertTrue(
            any("LXF04-T-001 benötigt pedagogicalRationale" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any("referenziert unbekannte Lernfunktion click-through" in error for error in errors),
            errors,
        )

    def test_learning_function_variants_must_form_connected_transition_paths(
        self,
    ) -> None:
        """Catches a named sequence whose transition chain cannot actually be followed."""
        validator = getattr(v2_validator, "validate_learning_architecture", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        architecture = copy.deepcopy(VALID_LXF04_ARCHITECTURE)
        architecture["learningFunctionGrammar"]["sequenceVariants"][0][
            "transitionIds"
        ][1] = "LXF04-T-008"

        errors = validator(
            architecture,
            VALID_LXF02_EVIDENCE_REGISTER,
            VALID_LXF03_PROFILE,
            VALID_REQUIREMENTS,
        )

        self.assertTrue(
            any("bildet keinen zusammenhängenden Übergangspfad" in error for error in errors),
            errors,
        )

    def test_learning_architecture_keeps_task_mode_and_transfer_distinctions(
        self,
    ) -> None:
        """Catches collapsed task types, practice stages, or instruction conditions."""
        validator = getattr(v2_validator, "validate_learning_architecture", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        architecture = copy.deepcopy(VALID_LXF04_ARCHITECTURE)
        architecture["taskTypes"] = architecture["taskTypes"][:1]
        architecture["practiceTransferStages"] = architecture[
            "practiceTransferStages"
        ][:2]
        architecture["instructionModes"][0]["requiredAfter"] = []

        errors = validator(
            architecture,
            VALID_LXF02_EVIDENCE_REGISTER,
            VALID_LXF03_PROFILE,
            VALID_REQUIREMENTS,
        )

        self.assertIn("LXF04-Architektur fehlt Aufgabentyp: performance-task", errors)
        self.assertIn("LXF04-Architektur fehlt Übungsstufe: transfer", errors)
        self.assertTrue(
            any("supported-exploration benötigt requiredAfter" in error for error in errors),
            errors,
        )

    def test_real_learning_architecture_is_complete_and_traceable(self) -> None:
        """Catches an incomplete real LXF04 contract behind a permissive fixture."""
        validator = getattr(v2_validator, "validate_learning_architecture", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        architecture_path = (
            PROJECT_ROOT
            / "roadmap/v2/foundations/learning-experience/learning-architecture.json"
        )
        self.assertTrue(architecture_path.is_file())
        architecture = load_repo_json(
            "roadmap/v2/foundations/learning-experience/learning-architecture.json"
        )
        evidence = load_repo_json(
            "roadmap/v2/foundations/learning-experience/evidence-register.json"
        )
        profile = load_repo_json(
            "roadmap/v2/foundations/learning-experience/learner-profile.json"
        )
        requirements = load_repo_json("roadmap/v2/requirements/requirements.json")

        self.assertEqual(
            [],
            validator(
                architecture, evidence, profile, requirements
            ),
        )
        self.assertEqual(
            EXPECTED_LXF04_GROUPS,
            {group["id"] for group in architecture["principleGroups"]},
        )
        self.assertEqual(
            EXPECTED_LXF04_FUNCTIONS,
            {
                function["id"]
                for function in architecture["learningFunctionGrammar"]["functions"]
            },
        )
        self.assertEqual(
            18,
            sum(len(group["principles"]) for group in architecture["principleGroups"]),
        )

    def test_learning_design_schema_is_fail_closed_and_sealed(self) -> None:
        """Catches optional principle fields or an extensible LXF04 schema."""
        validator = getattr(v2_validator, "validate_learning_design_schema", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        schema = load_repo_json("schemas/v2/learning-design.schema.json")
        weakened = copy.deepcopy(schema)
        weakened["$defs"]["principle"]["required"].remove("claimIds")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_json(root, "schemas/v2/learning-design.schema.json", weakened)
            errors = validator(root)

        self.assertIn(
            "LXF04-Schema weicht von der versiegelten Definition ab", errors
        )

    def test_learning_architecture_markdown_covers_contract_and_variants(self) -> None:
        """Catches machine data without the agreed human review guide."""
        validator = getattr(
            v2_validator, "validate_learning_architecture_markdown", None
        )
        self.assertIsNotNone(validator)
        assert validator is not None

        self.assertEqual([], validator(PROJECT_ROOT))

    def test_material_pattern_contract_is_wired_into_repository_gate(self) -> None:
        """Catches LXF05 artifacts being optional in the repository gate."""
        with tempfile.TemporaryDirectory() as directory:
            errors = validate_repository(Path(directory))

        for expected_error in (
            "roadmap/v2/foundations/learning-experience/material-patterns.json fehlt",
            "roadmap/v2/foundations/learning-experience/material-experience-guide.md fehlt",
            "schemas/v2/material-patterns.schema.json fehlt",
        ):
            self.assertIn(expected_error, errors)

    def test_material_pattern_requires_complete_traceable_contract(self) -> None:
        """Catches a pattern without purpose, use boundary, evidence, or access contract."""
        validator = getattr(v2_validator, "validate_material_patterns", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        required_fields = (
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
        )

        for field in required_fields:
            with self.subTest(field=field):
                contract = copy.deepcopy(VALID_LXF05_MATERIAL_PATTERNS)
                del contract["patterns"][0][field]

                errors = validator(
                    contract,
                    VALID_LXF04_ARCHITECTURE,
                    VALID_LXF02_EVIDENCE_REGISTER,
                )

                self.assertTrue(
                    any(f"benötigt {field}" in error for error in errors), errors
                )

    def test_material_patterns_require_every_family_and_unique_ids(self) -> None:
        """Catches a partial grammar or duplicate pattern identity."""
        validator = getattr(v2_validator, "validate_material_patterns", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        contract = copy.deepcopy(VALID_LXF05_MATERIAL_PATTERNS)
        contract["patterns"] = contract["patterns"][:-1]
        contract["patterns"][1]["id"] = contract["patterns"][0]["id"]

        errors = validator(
            contract,
            VALID_LXF04_ARCHITECTURE,
            VALID_LXF02_EVIDENCE_REGISTER,
        )

        self.assertIn(
            "LXF05-Materialgrammatik fehlt Patternfamilie: accessible-alternative",
            errors,
        )
        self.assertTrue(any("doppelte Pattern-ID" in error for error in errors), errors)

    def test_material_patterns_consume_reviewed_principles_and_known_functions(
        self,
    ) -> None:
        """Catches patterns resting on unreviewed design or an unknown learning function."""
        validator = getattr(v2_validator, "validate_material_patterns", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        architecture = copy.deepcopy(VALID_LXF04_ARCHITECTURE)
        architecture["principleGroups"][0]["principles"][0]["status"] = "working"
        contract = copy.deepcopy(VALID_LXF05_MATERIAL_PATTERNS)
        contract["patterns"][0]["learningFunctionIds"] = ["app-shell-navigation"]

        errors = validator(
            contract,
            architecture,
            VALID_LXF02_EVIDENCE_REGISTER,
        )

        self.assertTrue(any("ist nicht reviewed" in error for error in errors), errors)
        self.assertTrue(
            any("unbekannte Lernfunktion app-shell-navigation" in error for error in errors),
            errors,
        )

    def test_material_patterns_reject_product_shell_dependencies(self) -> None:
        """Catches an app-shell feature being smuggled in as a learning pattern."""
        validator = getattr(v2_validator, "validate_material_patterns", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        contract = copy.deepcopy(VALID_LXF05_MATERIAL_PATTERNS)
        contract["patterns"][0]["productDependencies"] = ["app-shell-navigation"]

        errors = validator(
            contract,
            VALID_LXF04_ARCHITECTURE,
            VALID_LXF02_EVIDENCE_REGISTER,
        )

        self.assertTrue(
            any("darf keine Produktabhängigkeit" in error for error in errors), errors
        )

    def test_material_patterns_reject_unreferenced_page_or_minute_rules(self) -> None:
        """Catches invented universal page and time limits without claim support."""
        validator = getattr(v2_validator, "validate_material_patterns", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        contract = copy.deepcopy(VALID_LXF05_MATERIAL_PATTERNS)
        contract["patterns"][0]["quantifiedRules"] = [
            {
                "statement": "Jedes Material hat höchstens 3 Seiten.",
                "claimIds": [],
                "scope": "universal",
            }
        ]

        errors = validator(
            contract,
            VALID_LXF04_ARCHITECTURE,
            VALID_LXF02_EVIDENCE_REGISTER,
        )

        self.assertTrue(
            any("Seiten- oder Minutenregel benötigt claimIds" in error for error in errors),
            errors,
        )

    def test_material_patterns_route_all_numeric_layout_time_and_age_rules(
        self,
    ) -> None:
        """Catches invented numeric universals hidden in ordinary pattern prose."""
        validator = getattr(v2_validator, "validate_material_patterns", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        cases = (
            "Jedes Material hat höchstens 3 Seiten.",
            "Eine Phase dauert immer 10 Minuten.",
            "Jede Ansicht enthält maximal 7 Elemente.",
            "Das Muster gilt für 12-Jährige.",
            "Jedes Material hat höchstens drei Seiten.",
            "Die Abfolge besteht aus 3-seitigen Einheiten.",
            "Eine Phase dauert immer 10 min.",
            "Jede Ansicht enthält höchstens drei Elemente.",
            "Für mindestens zwei unterscheidbare Produktlagen gilt eine Anschlussoption.",
            "Jedes Material hat höchstens fünfzehn Seiten.",
            "Eine Aktivierung ist stets 10-minütig.",
            "Jede Phase ist zehnminütig.",
            "Jeder Einstieg zeigt mindestens fünfzehn Schritte.",
        )

        for statement in cases:
            with self.subTest(statement=statement):
                contract = copy.deepcopy(VALID_LXF05_MATERIAL_PATTERNS)
                contract["patterns"][0]["requiredElements"] = [statement]

                errors = validator(
                    contract,
                    VALID_LXF04_ARCHITECTURE,
                    VALID_LXF02_EVIDENCE_REGISTER,
                )

                self.assertTrue(
                    any("außerhalb quantifiedRules" in error for error in errors),
                    errors,
                )

        contract = copy.deepcopy(VALID_LXF05_MATERIAL_PATTERNS)
        contract["walkthroughs"][0]["requiredInformation"] = (
            "Jeder Einstieg zeigt höchstens drei Elemente."
        )

        errors = validator(
            contract,
            VALID_LXF04_ARCHITECTURE,
            VALID_LXF02_EVIDENCE_REGISTER,
        )

        self.assertTrue(
            any("außerhalb quantifiedRules" in error for error in errors), errors
        )

        allowed_contract = copy.deepcopy(VALID_LXF05_MATERIAL_PATTERNS)
        allowed_contract["patterns"][0]["forbiddenElements"] = [
            "Keine feste Grenze von drei Seiten."
        ]
        allowed_contract["patterns"][0]["applicability"]["doNotUseWhen"] = [
            "Nicht verwenden, wenn höchstens drei Schritte erzwungen würden."
        ]
        allowed_contract["patterns"][0]["requiredElements"] = [
            "Eine einseitige Perspektive wird durch Kontrast sichtbar."
        ]

        allowed_errors = validator(
            allowed_contract,
            VALID_LXF04_ARCHITECTURE,
            VALID_LXF02_EVIDENCE_REGISTER,
        )

        self.assertFalse(
            any("außerhalb quantifiedRules" in error for error in allowed_errors),
            allowed_errors,
        )

    def test_material_patterns_reject_shell_features_hidden_as_required_elements(
        self,
    ) -> None:
        """Catches a concrete product shell encoded outside productDependencies."""
        validator = getattr(v2_validator, "validate_material_patterns", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        cases = (
            "Eine App-Shell-Navigation mit React Router und Sidebar.",
            "Eine Dashboard-Karte mit Weiter-Button.",
            "Eine blaue Karte mit 24px Überschrift.",
            "Klicke auf Weiter, um fortzufahren.",
            "Eine Navigationsleiste mit Zurücklink und Registerkarte.",
            "Ein zweispaltiges Layout mit runden Karten und Schatten.",
            "Öffne das Menü und beginne mit Aufgabe 1.",
            "Löse jetzt Aufgabe 1.",
            "Ein Akkordeon mit Dialogfenster und Dropdown.",
        )
        for statement in cases:
            with self.subTest(statement=statement):
                contract = copy.deepcopy(VALID_LXF05_MATERIAL_PATTERNS)
                contract["patterns"][0]["requiredElements"] = [statement]

                errors = validator(
                    contract,
                    VALID_LXF04_ARCHITECTURE,
                    VALID_LXF02_EVIDENCE_REGISTER,
                )

                self.assertTrue(
                    any(
                        "konkrete Produkt-, Darstellungs- oder Lernendentextvorgabe"
                        in error
                        for error in errors
                    ),
                    errors,
                )

        contract = copy.deepcopy(VALID_LXF05_MATERIAL_PATTERNS)
        contract["walkthroughs"][0]["action"] = (
            "Eine PWA-App-Shell mit Dashboard-Karte öffnen."
        )
        errors = validator(
            contract,
            VALID_LXF04_ARCHITECTURE,
            VALID_LXF02_EVIDENCE_REGISTER,
        )
        self.assertTrue(
            any(
                "konkrete Produkt-, Darstellungs- oder Lernendentextvorgabe" in error
                for error in errors
            ),
            errors,
        )

        allowed_contract = copy.deepcopy(VALID_LXF05_MATERIAL_PATTERNS)
        allowed_contract["patterns"][0]["forbiddenElements"] = [
            "Ein Weiter-Button als verpflichtende Navigation."
        ]
        allowed_contract["patterns"][0]["applicability"]["doNotUseWhen"] = [
            "Nicht verwenden, wenn eine Navigationsleiste fachlich bedeutungslose Wege vorgibt."
        ]
        allowed_errors = validator(
            allowed_contract,
            VALID_LXF04_ARCHITECTURE,
            VALID_LXF02_EVIDENCE_REGISTER,
        )
        self.assertFalse(
            any(
                "konkrete Produkt-, Darstellungs- oder Lernendentextvorgabe" in error
                for error in allowed_errors
            ),
            allowed_errors,
        )

    def test_material_patterns_require_human_semantic_review(self) -> None:
        """Makes semantic neutrality a human gate rather than a regex promise."""
        contract = copy.deepcopy(VALID_LXF05_MATERIAL_PATTERNS)
        contract["patterns"][0]["verificationMethods"] = ["usability-test"]

        errors = v2_validator.validate_material_patterns(
            contract,
            VALID_LXF04_ARCHITECTURE,
            VALID_LXF02_EVIDENCE_REGISTER,
        )

        self.assertTrue(
            any("benötigt fachlichen Neutralitätsreview" in error for error in errors),
            errors,
        )

    def test_material_walkthroughs_are_neutral_complete_and_traceable(self) -> None:
        """Catches a polished page shell replacing the three agreed neutral walkthroughs."""
        validator = getattr(v2_validator, "validate_material_patterns", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        contract = copy.deepcopy(VALID_LXF05_MATERIAL_PATTERNS)
        del contract["walkthroughs"][0]["barrier"]
        contract["walkthroughs"] = contract["walkthroughs"][:2]

        errors = validator(
            contract,
            VALID_LXF04_ARCHITECTURE,
            VALID_LXF02_EVIDENCE_REGISTER,
        )

        self.assertTrue(any("benötigt barrier" in error for error in errors), errors)
        self.assertIn(
            "LXF05-Materialgrammatik fehlt Walkthrough: securing-and-reentry",
            errors,
        )

    def test_real_material_pattern_contract_is_complete_and_product_neutral(self) -> None:
        """Catches an incomplete real LXF05 contract behind a permissive fixture."""
        validator = getattr(v2_validator, "validate_material_patterns", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        contract_path = (
            PROJECT_ROOT
            / "roadmap/v2/foundations/learning-experience/material-patterns.json"
        )
        self.assertTrue(contract_path.is_file())
        contract = load_repo_json(
            "roadmap/v2/foundations/learning-experience/material-patterns.json"
        )
        architecture = load_repo_json(
            "roadmap/v2/foundations/learning-experience/learning-architecture.json"
        )
        evidence = load_repo_json(
            "roadmap/v2/foundations/learning-experience/evidence-register.json"
        )

        self.assertEqual([], validator(contract, architecture, evidence))
        self.assertEqual(
            EXPECTED_LXF05_FAMILIES,
            {pattern["family"] for pattern in contract["patterns"]},
        )
        self.assertTrue(
            all(not pattern["productDependencies"] for pattern in contract["patterns"])
        )

    def test_material_pattern_schema_is_fail_closed_and_sealed(self) -> None:
        """Catches optional pattern fields or an extensible LXF05 schema."""
        validator = getattr(v2_validator, "validate_material_patterns_schema", None)
        self.assertIsNotNone(validator)
        assert validator is not None
        schema = load_repo_json("schemas/v2/material-patterns.schema.json")
        weakened = copy.deepcopy(schema)
        weakened["$defs"]["pattern"]["required"].remove("principleIds")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_json(root, "schemas/v2/material-patterns.schema.json", weakened)
            errors = validator(root)

        self.assertIn(
            "LXF05-Schema weicht von der versiegelten Definition ab", errors
        )

    def test_material_pattern_schema_matches_manual_whitespace_and_review_rules(
        self,
    ) -> None:
        """Catches schema acceptance of values rejected by the hand validator."""
        schema = load_repo_json("schemas/v2/material-patterns.schema.json")

        self.assertEqual(r".*\S.*", schema["$defs"]["nonEmptyString"]["pattern"])
        self.assertEqual(
            {"const": "automated-check"},
            schema["$defs"]["walkthrough"]["properties"]["verificationMethod"][
                "not"
            ],
        )

    def test_material_pattern_schema_declares_semantic_review_boundary(self) -> None:
        """Prevents the structural schema from claiming to prove prose neutrality."""
        schema = load_repo_json("schemas/v2/material-patterns.schema.json")

        self.assertEqual(
            {
                "structuralValidator": "json-schema",
                "semanticLint": "scripts/validate_v2_rebaseline.py",
                "authoritativeGate": "expert-review-or-content-walkthrough",
                "automatedSemanticProof": False,
            },
            schema["x-iumSemanticValidation"],
        )

    def test_material_experience_guide_covers_patterns_and_walkthroughs(self) -> None:
        """Catches machine data without the agreed human review guide."""
        validator = getattr(v2_validator, "validate_material_experience_guide", None)
        self.assertIsNotNone(validator)
        assert validator is not None

        self.assertEqual([], validator(PROJECT_ROOT))

    def test_material_experience_guide_requires_three_complete_review_tables(
        self,
    ) -> None:
        """Catches walkthrough headings surviving after a required table field is lost."""
        validator = v2_validator.validate_material_experience_guide
        source = (
            PROJECT_ROOT
            / "roadmap/v2/foundations/learning-experience/material-experience-guide.md"
        ).read_text(encoding="utf-8")
        mutations = (
            source.replace("| Lernendenfrage |", "| Entfernt |", 1),
            source.replace("| Prüffeld | Abstrakte Ausprägung |", "Prüffelder fehlen", 1),
            source.replace(
                "| Lernendenfrage | Was ist das fachliche Ziel, wofür wird mein Produkt gebraucht und womit beginne ich? |",
                "| Lernendenfrage | |",
                1,
            ),
            source.replace(
                "| Lernendenfrage | Was ist das fachliche Ziel, wofür wird mein Produkt gebraucht und womit beginne ich? |",
                "| Zusatzfeld | zusätzlicher Inhalt |\n| Lernendenfrage | Was ist das fachliche Ziel, wofür wird mein Produkt gebraucht und womit beginne ich? |",
                1,
            ),
            source.replace(
                "| Prüffeld | Abstrakte Ausprägung |\n|---|---|",
                "| Prüffeld | Abstrakte Ausprägung |\nEin Trennsatz.\n|---|---|",
                1,
            ),
        )

        for mutation_index, markdown in enumerate(mutations):
            with self.subTest(mutation_index=mutation_index), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                target = (
                    root
                    / "roadmap/v2/foundations/learning-experience/material-experience-guide.md"
                )
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(markdown, encoding="utf-8")

                errors = validator(root)

                self.assertTrue(
                    any("unvollständige Walkthrough-Tabelle" in error for error in errors),
                    errors,
                )

    def test_source_inventory_requires_an_object(self) -> None:
        """Catches malformed top-level JSON bypassing source-foundation checks."""
        errors = v2_validator.validate_source_inventory([], PROJECT_ROOT)

        self.assertEqual(["V2-Quelleninventar muss ein Objekt sein"], errors)

    def test_source_inventory_preserves_phase0_and_registers_exact_lxp01_set(self) -> None:
        """Catches silent Phase-0 drift or an incomplete LXP01 migration path."""
        inventory = load_repo_json("roadmap/v2/foundations/sources/inventory.json")

        errors = v2_validator.validate_source_inventory(inventory, PROJECT_ROOT)

        self.assertEqual([], errors)

    def test_source_inventory_rejects_baseline_hash_drift(self) -> None:
        """Catches an inventory that no longer identifies the audited V1 input."""
        inventory = copy.deepcopy(
            load_repo_json("roadmap/v2/foundations/sources/inventory.json")
        )
        inventory["phase0Baseline"]["sourceRegister"]["sha256"] = "0" * 64

        errors = v2_validator.validate_source_inventory(inventory, PROJECT_ROOT)

        self.assertIn(
            "V2-Quelleninventar sourceRegister sha256 stimmt nicht mit der Datei überein",
            errors,
        )

    def test_source_inventory_rejects_missing_or_promoted_lxp01_source(self) -> None:
        """Catches losing an addition or treating an unreviewed source as a V2 claim."""
        inventory = copy.deepcopy(
            load_repo_json("roadmap/v2/foundations/sources/inventory.json")
        )
        inventory["lxp01Additions"].pop()
        inventory["lxp01Additions"][0]["claimMigration"] = "approved"

        errors = v2_validator.validate_source_inventory(inventory, PROJECT_ROOT)

        self.assertIn(
            "V2-Quelleninventar muss exakt die sechs LXP01-Ergänzungen enthalten",
            errors,
        )
        self.assertIn(
            "LXP01-Quelle SRC-LXP-SDT-2024 muss bis LXF02 ohne V2-Claim bleiben",
            errors,
        )

    def test_source_inventory_requires_resolved_lesehilfe_locator_override(self) -> None:
        """Catches carrying the one locator-less V1 source into V2 unresolved."""
        inventory = copy.deepcopy(
            load_repo_json("roadmap/v2/foundations/sources/inventory.json")
        )
        inventory["locatorOverrides"] = []

        errors = v2_validator.validate_source_inventory(inventory, PROJECT_ROOT)

        self.assertIn(
            "V2-Quelleninventar benötigt den aufgelösten Locator für SRC-CUR-LESEHILFE-2026-27",
            errors,
        )

    def test_source_contract_enums_fail_closed_for_non_scalar_json_values(self) -> None:
        """Catches unhashable JSON arrays or objects crashing new enum checks."""
        inventory_fields = (
            ("sourceKind",),
            ("verificationStatus",),
            ("licenseStatus",),
            ("usageStatus",),
            ("liveCheck", "status"),
        )
        for field_path in inventory_fields:
            for malformed in ([], {}, None, True):
                with self.subTest(contract="inventory", field=field_path, value=malformed):
                    inventory = copy.deepcopy(
                        load_repo_json("roadmap/v2/foundations/sources/inventory.json")
                    )
                    target = inventory["lxp01Additions"][0]
                    if len(field_path) == 1:
                        target[field_path[0]] = malformed
                    else:
                        target[field_path[0]][field_path[1]] = malformed
                    errors = v2_validator.validate_source_inventory(
                        inventory,
                        PROJECT_ROOT,
                    )
                    self.assertTrue(errors)

        for malformed in ([], {}, None, True):
            with self.subTest(contract="link-audit", value=malformed):
                audit = copy.deepcopy(
                    load_repo_json("roadmap/v2/foundations/sources/link-audit.json")
                )
                audit["checks"][0]["status"] = malformed
                errors = v2_validator.validate_source_link_audit(
                    audit,
                    PROJECT_ROOT,
                    [],
                )
                self.assertTrue(errors)

    def test_source_inventory_rejects_incomplete_records_and_invalid_ranges(self) -> None:
        """Catches divergence between required schema fields and manual validation."""
        inventory = copy.deepcopy(
            load_repo_json("roadmap/v2/foundations/sources/inventory.json")
        )
        inventory["locatorOverrides"].append({"sourceId": "SRC-INCOMPLETE"})
        source = inventory["lxp01Additions"][0]
        source["year"] = 1899
        source["liveCheck"]["httpStatus"] = 999
        source["accessed"] = "2026-02-31"

        errors = v2_validator.validate_source_inventory(inventory, PROJECT_ROOT)

        self.assertIn("V2-Locator-Override SRC-INCOMPLETE benötigt url", errors)
        self.assertIn("LXP01-Quelle SRC-LXP-SDT-2024 hat ein ungültiges Jahr", errors)
        self.assertIn(
            "LXP01-Quelle SRC-LXP-SDT-2024 liveCheck hat ungültigen httpStatus",
            errors,
        )
        self.assertIn(
            "LXP01-Quelle SRC-LXP-SDT-2024 accessed muss ein echtes Kalenderdatum sein",
            errors,
        )

    def test_source_link_audit_requires_terminal_transport_evidence(self) -> None:
        """Catches resolved checks without the terminal HTTP evidence required by schema."""
        audit = copy.deepcopy(
            load_repo_json("roadmap/v2/foundations/sources/link-audit.json")
        )
        first = audit["checks"][0]
        first.pop("httpStatus")
        first.pop("finalUrl")

        errors = v2_validator.validate_source_link_audit(audit, PROJECT_ROOT, [])

        self.assertIn(
            f"V2-Linkprüfung {first['sourceId']} benötigt Pflichtfeld httpStatus",
            errors,
        )
        self.assertIn(
            f"V2-Linkprüfung {first['sourceId']} benötigt Pflichtfeld finalUrl",
            errors,
        )
        self.assertIn(
            f"V2-Linkprüfung {first['sourceId']} benötigt terminale HTTP-Evidenz für resolved",
            errors,
        )

    def test_source_schema_files_are_loaded_and_match_manual_contracts(self) -> None:
        """Catches orphaned JSON Schemas that drift from the enforced data contract."""
        errors = v2_validator.validate_source_schemas(PROJECT_ROOT)

        self.assertEqual([], errors)

    def test_source_schema_validation_fails_closed_for_missing_and_weakened_schemas(self) -> None:
        """Catches direct schema validation silently accepting absent or weakened files."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            errors = v2_validator.validate_source_schemas(root)

            self.assertEqual(3, len(errors))
            self.assertTrue(
                all("V2-Quellenschema fehlt:" in error for error in errors)
            )

            schema_paths = (
                "schemas/v2/source-inventory.schema.json",
                "schemas/v2/source-traceability.schema.json",
                "schemas/v2/source-link-audit.schema.json",
            )
            for relative_path in schema_paths:
                write_json(root, relative_path, load_repo_json(relative_path))
            link_schema = load_repo_json(
                "schemas/v2/source-link-audit.schema.json"
            )
            link_schema["$defs"]["check"]["allOf"] = []
            write_json(
                root,
                "schemas/v2/source-link-audit.schema.json",
                link_schema,
            )

            errors = v2_validator.validate_source_schemas(root)

            self.assertIn(
                "V2-Quellenschema Linkstatus-Semantik ist abgeschwächt: "
                "schemas/v2/source-link-audit.schema.json",
                errors,
            )

            inventory_schema = load_repo_json(
                "schemas/v2/source-inventory.schema.json"
            )
            inventory_schema["$defs"]["source"]["properties"][
                "claimMigration"
            ]["const"] = "approved"
            write_json(
                root,
                "schemas/v2/source-inventory.schema.json",
                inventory_schema,
            )

            errors = v2_validator.validate_source_schemas(root)

            self.assertIn(
                "V2-Quellenschema fachliche Semantik ist abgeschwächt: "
                "schemas/v2/source-inventory.schema.json",
                errors,
            )

    def test_repository_gate_reports_missing_source_schemas_via_control_files(self) -> None:
        """Catches repository validation losing the fail-closed schema file gate."""
        with tempfile.TemporaryDirectory() as directory:
            errors, _warnings = validate_repository_report(Path(directory))

        for relative_path in (
            "schemas/v2/source-inventory.schema.json",
            "schemas/v2/source-traceability.schema.json",
            "schemas/v2/source-link-audit.schema.json",
        ):
            self.assertIn(f"{relative_path} fehlt", errors)

    def test_source_schema_versions_reject_booleans(self) -> None:
        """Catches Python treating true as the integer schema version one."""
        inventory = copy.deepcopy(
            load_repo_json("roadmap/v2/foundations/sources/inventory.json")
        )
        traceability = copy.deepcopy(
            load_repo_json("roadmap/v2/foundations/sources/traceability.json")
        )
        audit = copy.deepcopy(
            load_repo_json("roadmap/v2/foundations/sources/link-audit.json")
        )
        inventory["schemaVersion"] = True
        traceability["schemaVersion"] = True
        audit["schemaVersion"] = True

        self.assertIn(
            "V2-Quelleninventar schemaVersion muss 1 sein",
            v2_validator.validate_source_inventory(inventory, PROJECT_ROOT),
        )
        self.assertIn(
            "V2-Quellenrückverfolgung schemaVersion muss 1 sein",
            v2_validator.validate_source_traceability(
                traceability,
                PROJECT_ROOT,
                [],
            ),
        )
        self.assertIn(
            "V2-Quellenlinkaudit schemaVersion muss 1 sein",
            v2_validator.validate_source_link_audit(audit, PROJECT_ROOT, []),
        )

    def test_source_inventory_live_check_binds_status_to_terminal_http(self) -> None:
        """Catches a live-check status that contradicts its terminal response."""
        inventory = copy.deepcopy(
            load_repo_json("roadmap/v2/foundations/sources/inventory.json")
        )
        source = inventory["lxp01Additions"][0]
        source["liveCheck"]["status"] = "resolved"
        source["liveCheck"]["httpStatus"] = 404

        errors = v2_validator.validate_source_inventory(inventory, PROJECT_ROOT)

        self.assertIn(
            "LXP01-Quelle SRC-LXP-SDT-2024 resolved benötigt terminalen 2xx-Status",
            errors,
        )

        source["liveCheck"]["status"] = "restricted"
        source["liveCheck"]["httpStatus"] = 200

        errors = v2_validator.validate_source_inventory(inventory, PROJECT_ROOT)

        self.assertIn(
            "LXP01-Quelle SRC-LXP-SDT-2024 restricted benötigt HTTP 401 oder 403",
            errors,
        )

    def test_source_traceability_verifies_claims_and_closes_optional_lxf02_gap(self) -> None:
        """Catches an obsolete pre-LXF02 warning surviving the documented source decision."""
        traceability = load_repo_json(
            "roadmap/v2/foundations/sources/traceability.json"
        )
        warnings: list[str] = []

        errors = v2_validator.validate_source_traceability(
            traceability,
            PROJECT_ROOT,
            warnings,
        )

        self.assertEqual([], errors)
        self.assertEqual([], warnings)
        self.assertEqual(
            "resolved-not-migrated",
            traceability["optionalGaps"][0]["resolutionStatus"],
        )
        self.assertIsNone(
            traceability["migrationRules"]["pendingLxp01ClaimReview"]
        )
        self.assertFalse(
            traceability["migrationRules"]["lxp01AdditionsCreateClaims"]
        )
        self.assertEqual(6, len(traceability["entityTypes"]))

    def test_source_readme_maps_all_lxp01_ids_to_registered_lxf02_ids(self) -> None:
        """Catches documentation links to source IDs that do not exist."""
        readme = (
            PROJECT_ROOT / "roadmap/v2/foundations/sources/README.md"
        ).read_text(encoding="utf-8")
        expected_mappings = {
            "SRC-LXP-SDT-2024": "SRC-V2-LXF-SDT-2024",
            "SRC-LXP-SEGMENT-2019": "SRC-V2-LXF-SEGMENT-2019",
            "SRC-LXP-SIGNAL-2016": "SRC-V2-LXF-SIGNAL-2016",
            "SRC-LXP-W3C-COGA-2021": "SRC-V2-LXF-W3C-COGA-2021",
            "SRC-LXP-UDL30-2024": "SRC-V2-LXF-UDL30-2024",
            "SRC-LXP-COS-2023": "SRC-V2-LXF-COS-2023",
        }

        for historical_id, registered_id in expected_mappings.items():
            with self.subTest(source=historical_id):
                self.assertIn(
                    f"| `{historical_id}` | `{registered_id}` |",
                    readme,
                )

    def test_source_traceability_rejects_illegal_reference_direction(self) -> None:
        """Catches a source entity being allowed to masquerade as a claim."""
        traceability = copy.deepcopy(
            load_repo_json("roadmap/v2/foundations/sources/traceability.json")
        )
        traceability["entityTypes"][0]["mayReference"] = ["claim"]

        errors = v2_validator.validate_source_traceability(
            traceability,
            PROJECT_ROOT,
            [],
        )

        self.assertIn(
            "V2-Quellenrückverfolgung enthält unerlaubte Entitätsreferenzrichtungen",
            errors,
        )

    def test_source_traceability_rejects_entity_collapse_and_required_gaps(self) -> None:
        """Catches merging evidence entities or passing a gate with a required gap."""
        traceability = copy.deepcopy(
            load_repo_json("roadmap/v2/foundations/sources/traceability.json")
        )
        traceability["entityFlow"].remove("project-decision")
        traceability["requiredGaps"] = [
            {
                "id": "SRC-GAP-REQUIRED",
                "sourceId": "SRC-MISSING",
                "required": True,
                "issue": "Pflichtquelle fehlt.",
                "resolutionStatus": "unresolved",
                "ownerGate": "IUM-V2-SRC",
                "acceptanceCriterion": "Quelle registrieren und primär prüfen.",
            }
        ]

        errors = v2_validator.validate_source_traceability(
            traceability,
            PROJECT_ROOT,
            [],
        )

        self.assertIn(
            "V2-Quellenrückverfolgung muss alle sechs Entitätstypen getrennt halten",
            errors,
        )
        self.assertIn(
            "V2-Quellenrückverfolgung darf keine offene Pflichtquellenlücke enthalten",
            errors,
        )

    def test_source_link_audit_accepts_current_complete_snapshot(self) -> None:
        """Catches an incomplete or internally inconsistent 69-source snapshot."""
        audit = load_repo_json("roadmap/v2/foundations/sources/link-audit.json")
        warnings: list[str] = []

        errors = v2_validator.validate_source_link_audit(
            audit,
            PROJECT_ROOT,
            warnings,
        )

        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_source_link_audit_blocks_required_failure_but_warns_for_optional(self) -> None:
        """Catches treating required and optional locator failures as equivalent."""
        audit = copy.deepcopy(
            load_repo_json("roadmap/v2/foundations/sources/link-audit.json")
        )
        required = next(check for check in audit["checks"] if check["required"])
        required["status"] = "missing"
        required["httpStatus"] = 404
        audit["summary"]["resolved"] -= 1
        audit["summary"]["missing"] += 1
        errors = v2_validator.validate_source_link_audit(audit, PROJECT_ROOT, [])
        self.assertIn(
            f"V2-Linkaudit enthält nicht auflösbare Pflichtquelle {required['sourceId']}",
            errors,
        )

        audit = copy.deepcopy(
            load_repo_json("roadmap/v2/foundations/sources/link-audit.json")
        )
        optional = next(check for check in audit["checks"] if not check["required"])
        optional["status"] = "missing"
        optional["httpStatus"] = 404
        audit["summary"]["resolved"] -= 1
        audit["summary"]["missing"] += 1
        audit["summary"]["warnings"] = 1
        warnings = []
        errors = v2_validator.validate_source_link_audit(
            audit,
            PROJECT_ROOT,
            warnings,
        )
        self.assertEqual([], errors)
        self.assertEqual(
            [
                f"optionale Quelle {optional['sourceId']} ist im V2-Linkaudit nicht auflösbar"
            ],
            warnings,
        )

    def test_source_link_audit_does_not_crash_on_malformed_nested_inventory(self) -> None:
        """Catches valid JSON with wrong nested types escaping fail-closed reporting."""
        inventory = copy.deepcopy(
            load_repo_json("roadmap/v2/foundations/sources/inventory.json")
        )
        inventory["locatorOverrides"] = 0
        inventory["lxp01Additions"] = 0
        audit = load_repo_json("roadmap/v2/foundations/sources/link-audit.json")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative_path in (
                "docs/research/phase-0/source-register.json",
                "docs/research/phase-0/claim-ledger.json",
                "docs/research/phase-0/design-principles.json",
            ):
                target = root / relative_path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((PROJECT_ROOT / relative_path).read_bytes())
            write_json(
                root,
                "roadmap/v2/foundations/sources/inventory.json",
                inventory,
            )

            errors = v2_validator.validate_source_link_audit(audit, root, [])

        self.assertIn(
            "V2-Quelleninventar locatorOverrides muss eine Liste sein",
            errors,
        )
        self.assertIn(
            "V2-Quelleninventar lxp01Additions muss eine Liste sein",
            errors,
        )

    def test_source_foundation_accepts_documented_user_approval(self) -> None:
        """Catches losing the explicit source-to-LXF01 approval transition."""
        status = copy.deepcopy(
            load_repo_json("roadmap/v2/foundations/sources/status.json")
        )
        status["workStatus"] = "done"
        status["maturity"]["foundationConcept"] = "reviewed"
        status["maturity"]["subjectReview"] = "passed"
        status["nextGate"] = "LXF01"

        errors = v2_validator.validate_foundation_status(
            status,
            "sources",
            {"V2-REQ-SRC-001"},
            PROJECT_ROOT,
            [],
        )

        self.assertEqual([], errors)

    def test_repository_report_integrates_all_source_contracts(self) -> None:
        """Catches source or evidence contracts not being wired into the release gate."""
        errors, warnings = validate_repository_report(PROJECT_ROOT)

        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_building_v2_keeps_v1_as_active_baseline(self) -> None:
        """Catches activating V2 before the explicit cutover decision."""
        status = copy.deepcopy(VALID_STATUS)
        status["activeBaseline"] = "v2"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, status=status)
            errors = validate_repository(root)

        self.assertIn(
            "activeBaseline muss v1 sein, solange v2State building ist",
            errors,
        )

    def test_content_production_remains_frozen(self) -> None:
        """Catches opening learner-content work during the re-baseline."""
        status = copy.deepcopy(VALID_STATUS)
        status["contentProduction"] = "open"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, status=status)
            errors = validate_repository(root)

        self.assertIn("contentProduction muss frozen sein", errors)

    def test_lxp05_remains_frozen_and_unmerged(self) -> None:
        """Catches treating the rejected LXP05 candidate as active product work."""
        status = copy.deepcopy(VALID_STATUS)
        status["lxp05"] = {"state": "active", "integration": "merged"}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, status=status)
            errors = validate_repository(root)

        self.assertIn("LXP05 muss frozen und unmerged bleiben", errors)

    def test_status_rejects_wrong_fixed_contract_values(self) -> None:
        """Catches weakening any fixed IUM-V2-00 control-state boundary."""
        cases = (
            ("schemaVersion", 2, "V2 schemaVersion muss 1 sein"),
            ("projectId", "other", "V2 projectId muss ium-lernwerk sein"),
            ("v2State", "active", "v2State muss building sein"),
            (
                "cutover",
                {"state": "approved"},
                "cutover muss not-approved sein",
            ),
        )
        for field, value, expected in cases:
            with self.subTest(field=field):
                status = copy.deepcopy(VALID_STATUS)
                status[field] = value
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write_control_files(root, status=status)
                    errors = validate_repository(root)
                self.assertIn(expected, errors)

    def test_main_commit_requires_a_full_sha(self) -> None:
        """Catches an archive that cannot identify the immutable V1 commit."""
        archive = copy.deepcopy(VALID_ARCHIVE)
        archive["mainCommit"] = "dcaff3e"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, archive=archive)
            errors = validate_repository(root)

        self.assertIn(
            "V1 mainCommit muss eine vollständige 40-stellige SHA sein",
            errors,
        )

    def test_main_commit_must_match_the_verified_v1_baseline(self) -> None:
        """Catches replacing V1 with a different but syntactically valid commit."""
        archive = copy.deepcopy(VALID_ARCHIVE)
        archive["mainCommit"] = "a" * 40
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, archive=archive)
            errors = validate_repository(root)

        self.assertIn(
            "V1 mainCommit muss den verifizierten main-Stand "
            "dcaff3e4b6e96d8c1da3dd1d4dd56f6df6b35ef0 referenzieren",
            errors,
        )

    def test_candidate_commit_requires_a_full_sha(self) -> None:
        """Catches an ambiguous candidate reference in the V1 archive."""
        archive = copy.deepcopy(VALID_ARCHIVE)
        archive["candidateRefs"][0]["commit"] = "645a1d4"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, archive=archive)
            errors = validate_repository(root)

        self.assertIn(
            "V1 candidateRef commit muss eine vollständige 40-stellige SHA sein: "
            "origin/feat/lxp05-ium5-experience",
            errors,
        )

    def test_archive_rejects_wrong_fixed_contract_values(self) -> None:
        """Catches changing the identity or provenance of the V1 baseline."""
        cases = (
            ("schemaVersion", 2, "V1 schemaVersion muss 1 sein"),
            (
                "repository",
                "other/repository",
                "V1 repository muss H4R7W16/ium-lernwerk sein",
            ),
            (
                "remote",
                "https://example.invalid/repository.git",
                "V1 remote muss das geprüfte GitHub-Remote sein",
            ),
            ("capturedAt", "03.09.2026", "V1 capturedAt muss YYYY-MM-DD sein"),
        )
        for field, value, expected in cases:
            with self.subTest(field=field):
                archive = copy.deepcopy(VALID_ARCHIVE)
                archive[field] = value
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write_control_files(root, archive=archive)
                    errors = validate_repository(root)
                self.assertIn(expected, errors)

    def test_archive_requires_the_verified_lxp05_candidate(self) -> None:
        """Catches dropping the known unmerged candidate from V1 history."""
        archive = copy.deepcopy(VALID_ARCHIVE)
        archive["candidateRefs"] = []
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, archive=archive)
            errors = validate_repository(root)

        self.assertIn(
            "V1-Archiv muss den verifizierten ungemergten LXP05-Kandidaten enthalten",
            errors,
        )

    def test_unknown_top_level_fields_fail_closed(self) -> None:
        """Catches bypassing either contract with an ungoverned status field."""
        status = copy.deepcopy(VALID_STATUS)
        status["progressPercent"] = 80
        archive = copy.deepcopy(VALID_ARCHIVE)
        archive["githubDashboardUrl"] = "https://example.invalid/07bc15e1e70d"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, status=status, archive=archive)
            errors = validate_repository(root)

        self.assertIn(
            "V2 status enthält unbekannte Felder: progressPercent",
            errors,
        )
        self.assertIn(
            "V1-Archiv enthält unbekannte Felder: githubDashboardUrl",
            errors,
        )

    def test_archive_requires_all_statement_boundaries(self) -> None:
        """Catches an archive that preserves files but loses their claim limits."""
        archive = copy.deepcopy(VALID_ARCHIVE)
        archive["statementBoundaries"].pop()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, archive=archive)
            errors = validate_repository(root)

        self.assertIn(
            "V1-Archiv muss alle verbindlichen Aussagegrenzen enthalten",
            errors,
        )

    def test_artifact_roots_must_be_repository_relative(self) -> None:
        """Catches leaking a local absolute path into the portable archive."""
        archive = copy.deepcopy(VALID_ARCHIVE)
        archive["artifactRoots"][0] = "C:/Users/Jan/IuM"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, archive=archive)
            errors = validate_repository(root)

        self.assertIn(
            "V1 artifactRoot muss repository-relativ sein: C:/Users/Jan/IuM",
            errors,
        )

    def test_dashboard_commit_stays_an_unverified_limitation(self) -> None:
        """Catches promoting the unavailable dashboard commit to Git evidence."""
        archive = copy.deepcopy(VALID_ARCHIVE)
        archive["limitations"] = []
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, archive=archive)
            errors = validate_repository(root)

        self.assertIn(
            "V1-Archiv muss den Dashboard-Commit 07bc15e1e70d als unverified-local begrenzen",
            errors,
        )

    def test_invalid_json_fails_closed(self) -> None:
        """Catches a malformed control file being treated like a valid state."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root)
            (root / "roadmap/v2/status.json").write_text("{", encoding="utf-8")
            errors = validate_repository(root)

        self.assertIn("roadmap/v2/status.json ist kein gültiges JSON", errors)

    def test_valid_archive_waits_only_for_the_requirements_gate(self) -> None:
        """Catches false archive errors once IUM-V2-00 is complete."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, include_requirements=False)
            errors = validate_repository(root)

        self.assertEqual(
            ["roadmap/v2/requirements/requirements.json fehlt"]
            + MISSING_FOUNDATION_CONTRACTS,
            errors,
        )

    def test_duplicate_requirement_ids_fail_closed(self) -> None:
        """Catches ambiguous evidence and dependencies caused by duplicate IDs."""
        requirements = copy.deepcopy(VALID_REQUIREMENTS)
        requirements["requirements"].append(copy.deepcopy(VALID_REQUIREMENT))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, requirements=requirements)
            errors = validate_repository(root)

        self.assertIn("doppelte Anforderungs-ID V2-REQ-001", errors)

    def test_unknown_requirement_domain_fails_closed(self) -> None:
        """Catches an ungoverned domain bypassing the eight-domain contract."""
        requirements = copy.deepcopy(VALID_REQUIREMENTS)
        requirements["requirements"][0]["domain"] = "ui-decoration"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, requirements=requirements)
            errors = validate_repository(root)

        self.assertIn("unbekannte Domäne ui-decoration", errors)

    def test_malformed_enum_type_fails_closed_without_crashing(self) -> None:
        """Catches non-scalar JSON values crashing enum validation."""
        requirements = copy.deepcopy(VALID_REQUIREMENTS)
        requirements["requirements"][0]["domain"] = []
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, requirements=requirements)
            errors = validate_repository(root)

        self.assertIn("unbekannte Domäne []", errors)

    def test_unknown_requirement_enum_values_fail_closed(self) -> None:
        """Catches invalid bindings, scopes, modes, coverage, grades, and evidence kinds."""
        cases = (
            ("binding", "accidental", "unbekannte Bindung accidental in V2-REQ-001"),
            ("scope", "page", "unbekannter Scope page in V2-REQ-001"),
            (
                "fulfillmentModes",
                ["decorative"],
                "unbekannter Erfüllungsmodus decorative in V2-REQ-001",
            ),
            (
                "coverage",
                "complete",
                "unbekannter Abdeckungsstatus complete in V2-REQ-001",
            ),
            ("grades", [8], "unbekannte Klassenstufe 8 in V2-REQ-001"),
        )
        for field, value, expected in cases:
            with self.subTest(field=field):
                requirements = copy.deepcopy(VALID_REQUIREMENTS)
                requirements["requirements"][0][field] = value
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write_control_files(root, requirements=requirements)
                    errors = validate_repository(root)
                self.assertIn(expected, errors)

        requirements = copy.deepcopy(VALID_REQUIREMENTS)
        requirements["requirements"][0]["origin"][0]["kind"] = "file"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, requirements=requirements)
            errors = validate_repository(root)
        self.assertIn("unbekannter Evidenztyp file in V2-REQ-001", errors)

    def test_required_evidence_pointer_needs_a_target(self) -> None:
        """Catches a mandatory source that cannot be followed or reviewed."""
        requirements = copy.deepcopy(VALID_REQUIREMENTS)
        requirements["requirements"][0]["origin"][0]["target"] = ""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, requirements=requirements)
            errors = validate_repository(root)

        self.assertIn("Pflichtreferenz ohne Ziel in V2-REQ-001", errors)

    def test_required_repository_reference_must_resolve(self) -> None:
        """Catches a required repository source that does not exist."""
        requirements = copy.deepcopy(VALID_REQUIREMENTS)
        requirements["requirements"][0]["origin"][0] = {
            "kind": "repo",
            "target": "docs/does-not-exist.md",
            "label": "Fehlende Pflichtquelle",
            "required": True,
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, requirements=requirements)
            errors = validate_repository(root)

        self.assertIn(
            "Pflichtreferenz im Repository fehlt in V2-REQ-001: "
            "docs/does-not-exist.md",
            errors,
        )

    def test_optional_missing_repository_reference_is_only_a_warning(self) -> None:
        """Catches historical source gaps incorrectly blocking the V2 gate."""
        requirements = copy.deepcopy(VALID_REQUIREMENTS)
        requirements["requirements"][0]["origin"][0] = {
            "kind": "repo",
            "target": "docs/historical-source-not-recovered.md",
            "label": "Nicht wiedergefundene historische Quelle",
            "required": False,
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, requirements=requirements)
            errors, warnings = validate_repository_report(root)

        self.assertEqual(MISSING_FOUNDATION_CONTRACTS, errors)
        self.assertIn(
            "optionale Repository-Referenz fehlt in V2-REQ-001: "
            "docs/historical-source-not-recovered.md",
            warnings,
        )

    def test_optional_vault_reference_is_reported_as_unresolved_warning(self) -> None:
        """Catches an unverifiable historical Vault link being silently accepted."""
        requirements = copy.deepcopy(VALID_REQUIREMENTS)
        requirements["requirements"][0]["origin"][0]["required"] = False
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, requirements=requirements)
            errors, warnings = validate_repository_report(root)

        self.assertEqual(MISSING_FOUNDATION_CONTRACTS, errors)
        self.assertIn(
            "optionale Vault-Referenz lokal nicht auflösbar in V2-REQ-001: "
            "2026-09-03 - Entscheidung - Kontrollierte Re-Baseline V2 und "
            "Lern-Experience-Fundament",
            warnings,
        )

    def test_git_evidence_requires_a_full_commit_sha(self) -> None:
        """Catches ambiguous Git proof that is not bound to an immutable commit."""
        requirements = copy.deepcopy(VALID_REQUIREMENTS)
        requirements["requirements"][0]["origin"][0] = {
            "kind": "git",
            "target": "dcaff3e",
            "label": "Zu kurzer Commit",
            "required": True,
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, requirements=requirements)
            errors = validate_repository(root)

        self.assertIn(
            "Git-Referenz muss eine vollständige 40-stellige SHA sein in "
            "V2-REQ-001: dcaff3e",
            errors,
        )

    def test_unknown_requirement_dependency_fails_closed(self) -> None:
        """Catches a sequencing rule that points to no registered requirement."""
        requirements = copy.deepcopy(VALID_REQUIREMENTS)
        requirements["requirements"][0]["dependencies"] = ["V2-REQ-999"]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, requirements=requirements)
            errors = validate_repository(root)

        self.assertIn("unbekannte Abhängigkeit V2-REQ-999", errors)

    def test_cyclic_requirement_dependency_fails_closed(self) -> None:
        """Catches an impossible gate order in the requirements graph."""
        first = copy.deepcopy(VALID_REQUIREMENT)
        first["dependencies"] = ["V2-REQ-002"]
        second = copy.deepcopy(VALID_REQUIREMENT)
        second["id"] = "V2-REQ-002"
        second["dependencies"] = ["V2-REQ-001"]
        requirements = copy.deepcopy(VALID_REQUIREMENTS)
        requirements["requirements"] = [first, second]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, requirements=requirements)
            errors = validate_repository(root)

        self.assertIn(
            "zyklische Anforderungsabhängigkeit V2-REQ-001 -> V2-REQ-002 -> "
            "V2-REQ-001",
            errors,
        )

    def test_covered_requirement_requires_v2_evidence(self) -> None:
        """Catches automatic V2 coverage inferred from the existence of V1 work."""
        requirements = copy.deepcopy(VALID_REQUIREMENTS)
        requirements["requirements"][0]["coverage"] = "covered"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, requirements=requirements)
            errors = validate_repository(root)

        self.assertIn(
            "V2-Abdeckung covered benötigt Evidenz in V2-REQ-001",
            errors,
        )

    def test_missing_required_requirement_field_fails_closed(self) -> None:
        """Catches an incomplete requirement entering the control register."""
        requirements = copy.deepcopy(VALID_REQUIREMENTS)
        del requirements["requirements"][0]["title"]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, requirements=requirements)
            errors = validate_repository(root)

        self.assertIn(
            "Pflichtfeld title fehlt oder ist leer in V2-REQ-001",
            errors,
        )

    def test_real_curriculum_foundation_contracts_are_consistent(self) -> None:
        """Catches drift between the V2 curriculum contract and immutable V1 facts."""
        requirements = json.loads(
            (PROJECT_ROOT / "roadmap/v2/requirements/requirements.json").read_text(
                encoding="utf-8"
            )
        )
        source_basis = json.loads(
            (
                PROJECT_ROOT
                / "roadmap/v2/foundations/curriculum/source-basis.json"
            ).read_text(encoding="utf-8")
        )
        gaps = json.loads(
            (
                PROJECT_ROOT
                / "roadmap/v2/foundations/curriculum/gap-assessments.json"
            ).read_text(encoding="utf-8")
        )
        status = json.loads(
            (
                PROJECT_ROOT / "roadmap/v2/foundations/curriculum/status.json"
            ).read_text(encoding="utf-8")
        )
        requirement_ids = {
            requirement["id"] for requirement in requirements["requirements"]
        }

        errors = []
        errors.extend(
            v2_validator.validate_curriculum_source_basis(
                source_basis,
                PROJECT_ROOT,
            )
        )
        errors.extend(
            v2_validator.validate_curriculum_gap_assessments(
                gaps,
                PROJECT_ROOT,
            )
        )
        errors.extend(
            v2_validator.validate_foundation_status(
                status,
                "curriculum",
                requirement_ids,
                PROJECT_ROOT,
            )
        )

        self.assertEqual([], errors)

    def test_lesehilfe_cannot_be_promoted_to_official_binding(self) -> None:
        """Catches treating the orienting Lesehilfe like an enacted curriculum."""
        source_basis = json.loads(
            (
                PROJECT_ROOT
                / "roadmap/v2/foundations/curriculum/source-basis.json"
            ).read_text(encoding="utf-8")
        )
        source_basis["sources"][2]["binding"] = "official"

        errors = v2_validator.validate_curriculum_source_basis(
            source_basis,
            PROJECT_ROOT,
        )

        self.assertIn(
            "SRC-CUR-LESEHILFE-2026-27 muss als orientation gebunden bleiben",
            errors,
        )

    def test_source_record_count_must_match_the_v1_dataset(self) -> None:
        """Catches a declared seal that no longer describes the source dataset."""
        source_basis = json.loads(
            (
                PROJECT_ROOT
                / "roadmap/v2/foundations/curriculum/source-basis.json"
            ).read_text(encoding="utf-8")
        )
        source_basis["sources"][0]["recordCount"] = 58

        errors = v2_validator.validate_curriculum_source_basis(
            source_basis,
            PROJECT_ROOT,
        )

        self.assertIn(
            "Curriculumquelle SRC-CUR-BMB-2016 erwartet 59 Records, deklariert 58",
            errors,
        )

    def test_gap_register_must_equal_the_current_five_v1_partial_records(self) -> None:
        """Catches silently losing or inventing an unresolved curriculum record."""
        gaps = json.loads(
            (
                PROJECT_ROOT
                / "roadmap/v2/foundations/curriculum/gap-assessments.json"
            ).read_text(encoding="utf-8")
        )
        gaps["assessments"].pop()

        errors = v2_validator.validate_curriculum_gap_assessments(
            gaps,
            PROJECT_ROOT,
        )

        self.assertIn(
            "V2-Curriculumlücken müssen exakt die fünf aktuellen V1-partial-Records enthalten",
            errors,
        )

    def test_v1_partial_record_cannot_auto_promote_to_v2_coverage(self) -> None:
        """Catches V1 module work being reused as unreviewed V2 fulfillment proof."""
        gaps = json.loads(
            (
                PROJECT_ROOT
                / "roadmap/v2/foundations/curriculum/gap-assessments.json"
            ).read_text(encoding="utf-8")
        )
        gaps["assessments"][0]["v2Coverage"]["status"] = "covered"

        errors = v2_validator.validate_curriculum_gap_assessments(
            gaps,
            PROJECT_ROOT,
        )

        self.assertIn(
            "V2-Curriculumlücke BMB16-GYM-IK-GM-003 darf ohne neue V2-Evidenz nicht covered sein",
            errors,
        )

    def test_tool_use_is_cross_cutting_without_extra_time_or_task(self) -> None:
        """Catches reintroducing a synthetic module or time block for routine tool use."""
        gaps = json.loads(
            (
                PROJECT_ROOT
                / "roadmap/v2/foundations/curriculum/gap-assessments.json"
            ).read_text(encoding="utf-8")
        )
        tool_use = gaps["assessments"][0]
        tool_use["v2Coverage"]["proposedFulfillmentMode"] = "direct-module"
        tool_use["time"]["additionalMinutes"] = 20
        tool_use["followUp"]["newLearningTask"] = "required"

        errors = v2_validator.validate_curriculum_gap_assessments(
            gaps,
            PROJECT_ROOT,
        )

        self.assertIn(
            "BMB16-GYM-IK-GM-003 muss als cross-cutting geführt werden",
            errors,
        )
        self.assertIn(
            "BMB16-GYM-IK-GM-003 darf keine zusätzlichen Minuten erzeugen",
            errors,
        )
        self.assertIn(
            "BMB16-GYM-IK-GM-003 darf keine künstliche Zusatzaufgabe erzeugen",
            errors,
        )

    def test_curriculum_foundation_cannot_claim_content_implementation(self) -> None:
        """Catches confusing a reviewed planning contract with learner content."""
        requirements = json.loads(
            (PROJECT_ROOT / "roadmap/v2/requirements/requirements.json").read_text(
                encoding="utf-8"
            )
        )
        status = json.loads(
            (
                PROJECT_ROOT / "roadmap/v2/foundations/curriculum/status.json"
            ).read_text(encoding="utf-8")
        )
        status["maturity"]["contentImplementation"] = "implemented"

        errors = v2_validator.validate_foundation_status(
            status,
            "curriculum",
            {requirement["id"] for requirement in requirements["requirements"]},
            PROJECT_ROOT,
        )

        self.assertIn(
            "Curriculumfundament darf bei eingefrorener Inhaltsproduktion keine Implementierung beanspruchen",
            errors,
        )

    def test_curriculum_foundation_accepts_documented_user_approval(self) -> None:
        """Catches the repository control state lagging behind an approved review gate."""
        status = json.loads(
            (
                PROJECT_ROOT / "roadmap/v2/foundations/curriculum/status.json"
            ).read_text(encoding="utf-8")
        )
        status["workStatus"] = "done"
        status["maturity"]["foundationConcept"] = "reviewed"
        status["maturity"]["subjectReview"] = "passed"
        status["nextGate"] = "IUM-V2-SRC"

        errors = v2_validator.validate_foundation_status(
            status,
            "curriculum",
            {"V2-REQ-CUR-001", "V2-REQ-CUR-002"},
            PROJECT_ROOT,
        )

        self.assertEqual([], errors)

    def test_curriculum_contracts_fail_closed_on_nested_object_ids(self) -> None:
        """Catches malformed JSON arrays crashing set-based cross-file checks."""
        source_basis = json.loads(
            (
                PROJECT_ROOT
                / "roadmap/v2/foundations/curriculum/source-basis.json"
            ).read_text(encoding="utf-8")
        )
        source_basis["baseline"]["immutablePaths"][0] = {"path": "curriculum"}
        status = json.loads(
            (
                PROJECT_ROOT / "roadmap/v2/foundations/curriculum/status.json"
            ).read_text(encoding="utf-8")
        )
        status["requirementIds"][0] = {"id": "V2-REQ-CUR-001"}

        source_errors = v2_validator.validate_curriculum_source_basis(
            source_basis,
            PROJECT_ROOT,
        )
        status_errors = v2_validator.validate_foundation_status(
            status,
            "curriculum",
            {"V2-REQ-CUR-001", "V2-REQ-CUR-002"},
            PROJECT_ROOT,
        )

        self.assertIn(
            "V2-Curriculumbaseline enthält einen ungültigen Pfad",
            source_errors,
        )
        self.assertIn(
            "V2-Fundamentstatus curriculum enthält eine ungültige requirementId",
            status_errors,
        )

    def test_curriculum_contracts_reject_unknown_nested_status_fields(self) -> None:
        """Catches hidden aggregate progress or evidence shortcuts in nested objects."""
        source_basis = json.loads(
            (
                PROJECT_ROOT
                / "roadmap/v2/foundations/curriculum/source-basis.json"
            ).read_text(encoding="utf-8")
        )
        source_basis["crosswalk"]["progressPercent"] = 80
        gaps = json.loads(
            (
                PROJECT_ROOT
                / "roadmap/v2/foundations/curriculum/gap-assessments.json"
            ).read_text(encoding="utf-8")
        )
        gaps["assessments"][0]["v2Coverage"]["v1EvidenceAccepted"] = True

        source_errors = v2_validator.validate_curriculum_source_basis(
            source_basis,
            PROJECT_ROOT,
        )
        gap_errors = v2_validator.validate_curriculum_gap_assessments(
            gaps,
            PROJECT_ROOT,
        )

        self.assertIn(
            "V2-Crosswalk enthält unbekannte Felder: progressPercent",
            source_errors,
        )
        self.assertIn(
            "V2-Abdeckung BMB16-GYM-IK-GM-003 enthält unbekannte Felder: v1EvidenceAccepted",
            gap_errors,
        )

    def test_curriculum_contracts_fail_closed_on_malformed_enum_types(self) -> None:
        """Catches syntactically valid JSON objects crashing enum membership checks."""
        source_basis = json.loads(
            (
                PROJECT_ROOT
                / "roadmap/v2/foundations/curriculum/source-basis.json"
            ).read_text(encoding="utf-8")
        )
        status = json.loads(
            (
                PROJECT_ROOT / "roadmap/v2/foundations/curriculum/status.json"
            ).read_text(encoding="utf-8")
        )
        gaps = json.loads(
            (
                PROJECT_ROOT
                / "roadmap/v2/foundations/curriculum/gap-assessments.json"
            ).read_text(encoding="utf-8")
        )

        malformed_cases = [
            (
                "source review status",
                source_basis,
                lambda contract: contract["sources"][0]["currentReview"].__setitem__(
                    "status", {}
                ),
                lambda contract: v2_validator.validate_curriculum_source_basis(
                    contract, PROJECT_ROOT
                ),
                "currentReview SRC-CUR-BMB-2016 hat unbekannten Prüfstatus",
            ),
            (
                "foundation work status",
                status,
                lambda contract: contract.__setitem__("workStatus", {}),
                lambda contract: v2_validator.validate_foundation_status(
                    contract,
                    "curriculum",
                    {"V2-REQ-CUR-001", "V2-REQ-CUR-002"},
                    PROJECT_ROOT,
                ),
                "V2-Fundamentstatus curriculum hat unbekannten workStatus",
            ),
            (
                "foundation maturity",
                status,
                lambda contract: contract["maturity"].__setitem__(
                    "foundationConcept", {}
                ),
                lambda contract: v2_validator.validate_foundation_status(
                    contract,
                    "curriculum",
                    {"V2-REQ-CUR-001", "V2-REQ-CUR-002"},
                    PROJECT_ROOT,
                ),
                "Reifeachse foundationConcept ist ungültig in curriculum",
            ),
            (
                "open question disposition",
                status,
                lambda contract: contract["openQuestions"][0].__setitem__(
                    "disposition", {}
                ),
                lambda contract: v2_validator.validate_foundation_status(
                    contract,
                    "curriculum",
                    {"V2-REQ-CUR-001", "V2-REQ-CUR-002"},
                    PROJECT_ROOT,
                ),
                "Offene Frage CUR-Q-002 hat ungültige disposition",
            ),
            (
                "coverage decision state",
                gaps,
                lambda contract: contract["assessments"][0]["v2Coverage"].__setitem__(
                    "decisionState", {}
                ),
                lambda contract: v2_validator.validate_curriculum_gap_assessments(
                    contract, PROJECT_ROOT
                ),
                "V2-Curriculumlücke BMB16-GYM-IK-GM-003 hat ungültigen decisionState",
            ),
        ]

        for label, original, mutate, validate, expected_error in malformed_cases:
            with self.subTest(label=label):
                contract = copy.deepcopy(original)
                mutate(contract)
                self.assertIn(expected_error, validate(contract))

    def test_gap_validator_enforces_schema_time_and_follow_up_fields(self) -> None:
        """Catches the hand-written validator accepting values rejected by the schema."""
        gaps = json.loads(
            (
                PROJECT_ROOT
                / "roadmap/v2/foundations/curriculum/gap-assessments.json"
            ).read_text(encoding="utf-8")
        )
        assessment = gaps["assessments"][1]
        assessment["time"]["status"] = "invented"
        assessment["time"]["additionalMinutes"] = -1
        del assessment["time"]["rationale"]
        assessment["followUp"]["kind"] = "invented"
        assessment["followUp"]["newLearningTask"] = {}

        errors = v2_validator.validate_curriculum_gap_assessments(
            gaps,
            PROJECT_ROOT,
        )

        competency_id = "BMB16-GYM-PK-RK-003"
        self.assertIn(
            f"V2-Zeitstatus {competency_id} hat unbekannten Status",
            errors,
        )
        self.assertIn(
            f"V2-Zeitstatus {competency_id} hat ungültige additionalMinutes",
            errors,
        )
        self.assertIn(
            f"V2-Zeitstatus {competency_id} benötigt eine Begründung",
            errors,
        )
        self.assertIn(
            f"V2-Folgeprüfung {competency_id} hat unbekannte Art",
            errors,
        )
        self.assertIn(
            f"V2-Folgeprüfung {competency_id} hat ungültigen newLearningTask",
            errors,
        )

    def test_gap_decision_states_remain_sealed_until_subject_review(self) -> None:
        """Catches an unresolved gap being silently promoted to an approved direction."""
        gaps = json.loads(
            (
                PROJECT_ROOT
                / "roadmap/v2/foundations/curriculum/gap-assessments.json"
            ).read_text(encoding="utf-8")
        )

        for assessment in gaps["assessments"]:
            competency_id = assessment["competencyId"]
            mutated = copy.deepcopy(gaps)
            candidate = next(
                item
                for item in mutated["assessments"]
                if item["competencyId"] == competency_id
            )
            expected_state = (
                "approved-direction"
                if competency_id == "BMB16-GYM-IK-GM-003"
                else "open"
            )
            candidate["v2Coverage"]["decisionState"] = (
                "open" if expected_state == "approved-direction" else "approved-direction"
            )

            with self.subTest(competency_id=competency_id):
                errors = v2_validator.validate_curriculum_gap_assessments(
                    mutated,
                    PROJECT_ROOT,
                )
                self.assertIn(
                    f"V2-Curriculumlücke {competency_id} muss bis zur fachlichen Entscheidung {expected_state} bleiben",
                    errors,
                )


LXF06_FILES = [
    "roadmap/v2/foundations/learning-experience/experience-gates.json",
    "roadmap/v2/foundations/learning-experience/teacher-orchestration.md",
    "roadmap/v2/foundations/learning-experience/review-form.md",
    "schemas/v2/experience-gates.schema.json",
]
LXF06_GATE_IDS = [
    "evidence-integrity", "goal-action-evidence-alignment", "cognitive-economy",
    "disciplinary-learning-action", "representation-coherence",
    "support-without-task-removal", "feedback-and-next-action",
    "orientation-and-recovery", "accessibility-and-equivalence",
    "teacher-orchestration", "privacy-and-emotional-safety", "pilot-boundary",
]


class ExperienceGateTests(unittest.TestCase):
    """Protect the boundary between a review definition and actual review evidence."""

    def setUp(self):
        base = PROJECT_ROOT / "roadmap/v2/foundations/learning-experience"
        self.architecture = json.loads((base / "learning-architecture.json").read_text(encoding="utf-8"))
        self.patterns = json.loads((base / "material-patterns.json").read_text(encoding="utf-8"))
        self.contract = {
            "schemaVersion": 1, "projectId": "ium-lernwerk", "asOf": "2026-09-05",
            "scope": copy.deepcopy(self.patterns["scope"]),
            "reviewBoundary": {
                "definitionStatus": "working", "executionStatus": "not-run",
                "pilot": "not-started", "standardAllowed": False,
                "learningEffectClaimAllowed": False, "personalTelemetryAllowed": False,
            },
            "gates": [],
            "walkthroughBindings": [
                {"walkthroughId": name, "gateIds": list(LXF06_GATE_IDS)}
                for name in ("entry", "central-learning-action", "securing-and-reentry")
            ],
        }
        for gate_id in LXF06_GATE_IDS:
            self.contract["gates"].append({
                "id": gate_id, "title": "Begrenzter Testvertrag",
                "question": "Ist das fachliche Produkt prüfbar?",
                "evidenceRequired": ["Ein aufgabenbezogenes Produkt mit Fundstelle."],
                "method": ["expert-review", "source-review", "accessibility-audit"],
                "principleIds": ["LXF04-PR-001"], "patternIds": ["LXF05-PT-001"],
                "passCondition": "Die fachliche Beziehung ist am Produkt erkennbar.",
                "failAction": "Die Pflichtlücke vor Freigabe schließen und erneut prüfen.",
                "ownerRole": "subject-didactics-reviewer",
                "statusEffect": {
                    "onPass": "eligible-for-lxf07-review", "onFail": "block-foundation-review",
                    "pilot": "not-started", "standardAllowed": False,
                },
            })

    def check(self, data=...):
        validate = getattr(v2_validator, "validate_experience_gates", None)
        self.assertTrue(callable(validate), "LXF06 gate validation is not implemented")
        return validate(self.contract if data is ... else data, self.architecture, self.patterns)

    def test_missing_lxf06_artifacts_block_repository_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            errors = validate_repository(Path(directory))
        for path in LXF06_FILES:
            self.assertIn(path + " fehlt", errors)

    def test_complete_review_definition_is_accepted_without_claiming_execution(self):
        self.assertEqual([], self.check())

    def test_each_gate_requires_the_full_method_and_responsibility_contract(self):
        for field in ("question", "evidenceRequired", "method", "passCondition", "failAction", "ownerRole", "statusEffect", "principleIds", "patternIds"):
            with self.subTest(field=field):
                data = copy.deepcopy(self.contract)
                del data["gates"][0][field]
                self.assertTrue(self.check(data))

    def test_whitespace_is_not_evidence_or_a_pass_condition(self):
        for field, value in (("question", "  "), ("evidenceRequired", ["\t"]), ("passCondition", "\n"), ("failAction", "")):
            with self.subTest(field=field):
                data = copy.deepcopy(self.contract)
                data["gates"][0][field] = value
                self.assertTrue(self.check(data))

    def test_automated_or_future_usage_methods_cannot_replace_didactic_review(self):
        for methods in (["automated-check"], ["usability-test"], ["classroom-pilot"], ["source-review"]):
            with self.subTest(methods=methods):
                data = copy.deepcopy(self.contract)
                data["gates"][1]["method"] = methods
                self.assertTrue(self.check(data))

    def test_source_and_accessibility_gates_require_their_specific_methods(self):
        for position in (0, 8):
            with self.subTest(position=position):
                data = copy.deepcopy(self.contract)
                data["gates"][position]["method"] = ["expert-review"]
                self.assertTrue(self.check(data))

    def test_automation_may_supplement_a_suitable_human_review(self):
        self.contract["gates"][1]["method"] = ["automated-check", "content-walkthrough"]
        self.assertEqual([], self.check())

    def test_status_effect_cannot_approve_pilot_standard_or_foundation(self):
        for field, value in (("onPass", "reviewed"), ("onFail", "accept-without-evidence"), ("pilot", "completed"), ("standardAllowed", True), ("standardAllowed", 0)):
            with self.subTest(field=field, value=value):
                data = copy.deepcopy(self.contract)
                data["gates"][0]["statusEffect"][field] = value
                self.assertTrue(self.check(data))

    def test_definition_cannot_pretend_review_or_real_use_has_occurred(self):
        for field, value in (("executionStatus", "passed"), ("pilot", "in-progress"), ("standardAllowed", True), ("learningEffectClaimAllowed", True), ("personalTelemetryAllowed", True)):
            with self.subTest(field=field):
                data = copy.deepcopy(self.contract)
                data["reviewBoundary"][field] = value
                self.assertTrue(self.check(data))

    def test_missing_duplicate_and_unknown_gates_are_rejected(self):
        for mutation in (lambda d: d["gates"].pop(), lambda d: d["gates"].append(copy.deepcopy(d["gates"][0])), lambda d: d["gates"][0].update(id="invented")):
            data = copy.deepcopy(self.contract)
            mutation(data)
            self.assertTrue(self.check(data))

    def test_unknown_or_unreviewed_principles_and_patterns_are_rejected(self):
        for field in ("principleIds", "patternIds"):
            data = copy.deepcopy(self.contract)
            data["gates"][0][field] = ["missing"]
            self.assertTrue(self.check(data))
        self.patterns["patterns"][0]["status"] = "working"
        self.assertTrue(self.check())
        self.patterns["patterns"][0]["status"] = "reviewed"
        self.architecture["principleGroups"][0]["principles"][0]["status"] = "draft"
        self.assertTrue(self.check())

    def test_walkthroughs_require_known_unique_complete_bindings(self):
        for mutation in (
            lambda d: d["walkthroughBindings"].pop(),
            lambda d: d["walkthroughBindings"][0].update(walkthroughId="invented"),
            lambda d: d["walkthroughBindings"][0].update(gateIds=["missing"]),
            lambda d: d["walkthroughBindings"][0].update(gateIds=[]),
            lambda d: d["walkthroughBindings"].append(copy.deepcopy(d["walkthroughBindings"][0])),
        ):
            data = copy.deepcopy(self.contract)
            mutation(data)
            self.assertTrue(self.check(data))

    def test_malformed_values_fail_closed_instead_of_crashing(self):
        for value in (None, [], 1, "invalid"):
            self.assertTrue(self.check(value))
        for field in ("gates", "scope", "reviewBoundary", "walkthroughBindings"):
            for value in (None, True, "invalid", [{}]):
                data = copy.deepcopy(self.contract)
                data[field] = value
                self.assertTrue(self.check(data))
        for field in ("id", "ownerRole", "method", "statusEffect", "principleIds", "patternIds"):
            for value in ({}, [None], 1, False):
                data = copy.deepcopy(self.contract)
                data["gates"][0][field] = value
                self.assertTrue(self.check(data))

    def test_unknown_fields_and_duplicate_references_are_rejected(self):
        for mutate in (
            lambda d: d.update(pilot="completed"),
            lambda d: d["gates"][0].update(result="passed"),
            lambda d: d["gates"][0]["statusEffect"].update(release=True),
            lambda d: d["gates"][0].update(principleIds=["LXF04-PR-001", "LXF04-PR-001"]),
            lambda d: d["gates"][0].update(method=["expert-review", "expert-review"]),
        ):
            data = copy.deepcopy(self.contract)
            mutate(data)
            self.assertTrue(self.check(data))

    def test_real_gate_contract_is_consumed_by_repository_validation(self):
        path = PROJECT_ROOT / LXF06_FILES[0]
        self.assertTrue(path.is_file(), "LXF06 experience-gates.json is missing")
        self.assertEqual([], self.check(json.loads(path.read_text(encoding="utf-8"))))
        self.assertEqual([], validate_repository(PROJECT_ROOT))



class LearningExperienceReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.base = "roadmap/v2/foundations/learning-experience/"
        inputs = [p for p in v2_validator.CONTROL_FILES
                  if p.name not in {"validation-report.md"} and p.as_posix() != self.base + "status.json"]
        inputs.append(Path("docs/superpowers/specs/2026-09-03-ium-v2-controlled-rebaseline-design.md"))
        for relative in inputs:
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((PROJECT_ROOT / relative).read_bytes())
        report = Path(self.base + "validation-report.md")
        (self.root / report).write_text("# Review\n## Beleg\nKonkreter Testbeleg.\n", encoding="utf-8")
        inputs.append(report)
        definitions = json.loads((self.root / (self.base + "experience-gates.json")).read_text(encoding="utf-8"))
        evidence = [{"path": report.as_posix(), "locator": "## Beleg", "observation": "Der Gegenfall führt zur dokumentierten Umsteuerung."}]
        self.data = {
            "schemaVersion": 1, "projectId": "ium-lernwerk", "id": "learning-experience",
            "asOf": "2026-09-05", "workStatus": "done", "concept": "reviewed",
            "pilot": "not-started", "standardization": "not-eligible",
            "contentProduction": "frozen", "release": "closed",
            "nextGate": "IUM-V2-GOV", "nextGateCondition": "explicit-lxf07-user-approval",
            "review": {
                "type": "ai-assisted-document-review", "reviewer": "Codex", "independence": "self-review",
                "baseCommit": "beaba6d3382d60ef31b1171368e4580b2e1432b3",
                "inputDigests": {p.as_posix(): self.digest(p) for p in inputs},
                "gateResults": [{"id": g["id"], "result": "pass", "methods": [m for m in g["method"] if m != "automated-check"],
                                 "ownerRole": g["ownerRole"], "evidence": copy.deepcopy(evidence),
                                 "limitation": "Prüfung am Dokument, keine reale Durchführung."} for g in definitions["gates"]],
                "walkthroughResults": [{"id": n, "result": "pass", "perspectives": ["learner", "teacher"],
                                        "evidence": copy.deepcopy(evidence)}
                                       for n in ("entry", "central-learning-action", "securing-and-reentry")],
                "openQuestions": [{"id": "PILOT-001", "question": "Wie trägt der Entwurf im Unterricht?", "owner": "teacher-reviewer",
                                   "trigger": "Gesondert freigegebener Unterrichtspilot", "risk": "Reale Nutzung ist noch unbekannt.",
                                   "disposition": "deferred-to-later-gate"}],
            },
        }

    def digest(self, relative):
        return hashlib.sha256((self.root / relative).read_bytes().replace(b"\r\n", b"\n")).hexdigest()

    def check(self, data=None, prior=()):
        fn = getattr(v2_validator, "validate_learning_experience_release", None)
        self.assertTrue(callable(fn), "LXF07 Releasevalidator fehlt")
        return fn(self.data if data is None else data, self.root, prior)

    def test_complete_document_review_can_reach_reviewed(self):
        self.assertEqual(self.check(), [])

    def test_automation_alone_cannot_release_any_gate(self):
        for i in range(12):
            with self.subTest(gate=i):
                d=copy.deepcopy(self.data); d["review"]["gateResults"][i]["methods"]=["automated-check"]
                self.assertTrue(self.check(d))

    def test_missing_failed_duplicate_and_unknown_gate_block_promotion(self):
        for mode in ("missing", "failed", "not-run", "duplicate", "unknown"):
            with self.subTest(mode=mode):
                d=copy.deepcopy(self.data); gates=d["review"]["gateResults"]
                if mode=="missing": gates.pop()
                elif mode in {"failed","not-run"}: gates[0]["result"]="fail" if mode=="failed" else mode
                elif mode=="duplicate": gates[-1]=copy.deepcopy(gates[0])
                else: gates[0]["id"]="unknown"
                self.assertTrue(self.check(d))

    def test_evidence_must_exist_match_locator_and_include_observation(self):
        for field,value in (("path","../outside.md"),("path","absent.md"),("locator","missing heading"),("observation"," ")):
            with self.subTest(field=field,value=value):
                d=copy.deepcopy(self.data); d["review"]["gateResults"][0]["evidence"][0][field]=value
                self.assertTrue(self.check(d))
        d=copy.deepcopy(self.data); d["review"]["gateResults"][0]["evidence"]=[]
        self.assertTrue(self.check(d))

    def test_each_required_input_and_report_must_be_present_and_unchanged(self):
        for relative in self.data["review"]["inputDigests"]:
            with self.subTest(path=relative):
                p=self.root/relative; before=p.read_bytes()
                p.write_bytes(before+b"\nUnreviewed edit\n")
                self.assertTrue(self.check())
                p.write_bytes(before)
        p=self.root/(self.base+"validation-report.md"); p.rename(p.with_suffix(".missing"))
        self.assertTrue(self.check())

    def test_digest_manifest_cannot_drop_or_add_targets(self):
        d=copy.deepcopy(self.data); d["review"]["inputDigests"].pop(next(iter(d["review"]["inputDigests"])))
        self.assertTrue(self.check(d))
        d=copy.deepcopy(self.data); d["review"]["inputDigests"]["../outside.md"]="0"*64
        self.assertTrue(self.check(d))

    def test_pending_prerequisite_errors_block_promotion(self):
        for reason in ("Quelle fehlt", "Claim ist draft", "Prinzipreferenz unbekannt", "Pilotstatus unzulässig"):
            with self.subTest(reason=reason): self.assertTrue(self.check(prior=[reason]))

    def test_no_standard_pilot_release_or_production_promotion(self):
        for field,value in (("concept","standard"),("pilot","completed"),("standardization","eligible"),("release","released"),("contentProduction","open"),("nextGateCondition","automatic")):
            with self.subTest(field=field):
                d=copy.deepcopy(self.data);d[field]=value;self.assertTrue(self.check(d))

    def test_status_axes_cannot_disagree(self):
        for work,concept in (("done","working"),("review","reviewed")):
            d=copy.deepcopy(self.data);d.update(workStatus=work,concept=concept);self.assertTrue(self.check(d))

    def test_explicit_lower_status_can_record_failed_gate(self):
        d=copy.deepcopy(self.data);d.update(workStatus="blocked",concept="working")
        d["review"]["gateResults"][0]["result"]="fail"
        self.assertEqual(self.check(d,prior=["Offener fachlicher Befund"]),[])

    def test_both_perspectives_and_all_three_walkthroughs_required(self):
        d=copy.deepcopy(self.data);d["review"]["walkthroughResults"].pop();self.assertTrue(self.check(d))
        d=copy.deepcopy(self.data);d["review"]["walkthroughResults"][0]["perspectives"]=["learner"];self.assertTrue(self.check(d))

    def test_commit_role_and_review_identity_are_explicit(self):
        for field,value in (("baseCommit","short"),("reviewer"," "),("type","automated-check"),("independence","independent")):
            d=copy.deepcopy(self.data);d["review"][field]=value;self.assertTrue(self.check(d))
        d=copy.deepcopy(self.data);d["review"]["gateResults"][0]["ownerRole"]="teacher-reviewer";self.assertTrue(self.check(d))

    def test_open_questions_need_owner_trigger_and_risk(self):
        for field in ("owner","trigger","risk"):
            d=copy.deepcopy(self.data);del d["review"]["openQuestions"][0][field];self.assertTrue(self.check(d))

    def test_malformed_and_unknown_fields_fail_closed(self):
        for key,value in (("review",[]),("schemaVersion",True),("asOf","2026-02-30"),("unexpected",True)):
            with self.subTest(key=key):
                d=copy.deepcopy(self.data);d[key]=value;self.assertTrue(self.check(d))
        for field in ("inputDigests","gateResults","walkthroughResults","openQuestions"):
            for value in (None,True,42,"wrong",[None]):
                with self.subTest(field=field,value=value):
                    d=copy.deepcopy(self.data);d["review"][field]=value;self.assertTrue(self.check(d))

    def test_draft_claim_principle_or_pattern_blocks_even_with_refreshed_digest(self):
        for filename, chain in (("evidence-register", ["claims", 0]),
                                ("learning-architecture", ["principleGroups", 0, "principles", 0]),
                                ("material-patterns", ["patterns", 0])):
            for status in ("draft", "working", "standard"):
                with self.subTest(filename=filename,status=status):
                    relative=Path(self.base+filename+".json")
                    path=self.root/relative; original=path.read_bytes()
                    data=json.loads(original); item=data
                    for part in chain: item=item[part]
                    item["status"]=status
                    path.write_text(json.dumps(data),encoding="utf-8")
                    d=copy.deepcopy(self.data)
                    d["review"]["inputDigests"][relative.as_posix()]=self.digest(relative)
                    self.assertTrue(self.check(d))
                    path.write_bytes(original)

    def test_specific_source_and_accessibility_methods_remain_required(self):
        for name in ("evidence-integrity", "accessibility-and-equivalence"):
            d=copy.deepcopy(self.data)
            next(g for g in d["review"]["gateResults"] if g["id"]==name)["methods"]=["expert-review"]
            self.assertTrue(self.check(d))

    def test_git_line_ending_conversion_preserves_evidence(self):
        for relative in self.data["review"]["inputDigests"]:
            p=self.root/relative
            p.write_bytes(p.read_bytes().replace(b"\r\n",b"\n").replace(b"\n",b"\r\n"))
        self.assertEqual(self.check(),[])

    def test_repository_consumes_release_record(self):
        path=self.root/(self.base+"status.json")
        d=copy.deepcopy(self.data);d["review"]["gateResults"][0]["evidence"]=[]
        path.write_text(json.dumps(d),encoding="utf-8")
        self.assertTrue(any("LXF07" in e for e in validate_repository(self.root)))


if __name__ == "__main__":
    unittest.main()
