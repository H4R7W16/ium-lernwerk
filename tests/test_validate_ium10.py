import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import nullcontext
from pathlib import Path

import scripts.validate_ium10 as ium10_validator
from scripts.validate_ium10 import (
    BASELINE_COVERAGE_PROJECTION_SHA256,
    BASELINE_MODULE_STRUCTURE_SHA256,
    BASELINE_TIME_HANDOFF_SHA256,
    IUM10_BASELINE_COMMIT,
    IUM10ValidationError,
    coverage_projection_fingerprint,
    time_handoff_fingerprint,
    validate_annual_variants,
    validate_capacity_model,
    validate_integration_contracts,
    validate_module_contracts,
    validate_privacy_contracts,
    validate_time_reviews,
    validate_time_model_draft,
    validate_ium10_baseline,
)


TIME_AUDIT_DECISIONS = {
    "BMB16-GYM-IK-GM-001": "additional-time",
    "BMB16-GYM-IK-GM-002": "additional-time",
    "BMB16-GYM-IK-GM-003": "additional-time",
    "BMB16-GYM-IK-KK-002": "additional-time",
    "BMB16-GYM-IK-KK-003": "absorbed",
    "BMB16-GYM-PK-SK-003": "absorbed",
    "BMB16-GYM-PK-HK-003": "absorbed",
    "BMB16-GYM-PK-RK-004": "additional-time",
    "LH26-E-DA-004": "additional-time",
    "LH26-E-DP-001": "additional-time",
    "LH26-E-ID-009": "absorbed",
    "LH26-E-ALG-001": "absorbed",
    "LH26-E-KS-001": "additional-time",
    "LH26-E-KS-002": "additional-time",
    "LH26-E-PROG-001": "unresolved",
    "LH26-E-PROG-002": "unresolved",
    "BMB16-GYM-IK-PP-002": "integrated",
    "LH26-E-DA-005": "additional-time",
    "LH26-E-DA-006": "additional-time",
    "LH26-E-DA-008": "additional-time",
    "BMB16-GYM-IK-MG-001": "additional-time",
    "BMB16-GYM-IK-MG-002": "additional-time",
    "BMB16-GYM-IK-MG-003": "absorbed",
    "BMB16-GYM-PK-RK-001": "additional-time",
    "BMB16-GYM-PK-RK-002": "additional-time",
    "BMB16-GYM-PK-RK-003": "unresolved",
    "LH26-E-DP-003": "unresolved",
    "LH26-E-DP-004": "integrated",
    "LH26-E-DP-006": "integrated",
    "LH26-E-KS-014": "additional-time",
    "LH26-E-KS-015": "additional-time",
    "LH26-E-DA-009": "additional-time",
    "LH26-E-DA-010": "additional-time",
    "LH26-E-DA-012": "absorbed",
    "LH26-E-DA-015": "additional-time",
    "INF7-16-GYM-IK-DC-001": "additional-time",
    "INF7-16-GYM-IK-DC-004": "additional-time",
    "INF7-16-GYM-IK-DC-005": "integrated",
    "LH26-E-ID-020": "absorbed",
    "LH26-E-ID-021": "additional-time",
    "INF7-16-GYM-IK-ALG-003": "integrated",
    "INF7-16-GYM-PK-MI-005": "additional-time",
    "INF7-16-GYM-PK-SV-003": "additional-time",
    "LH26-E-ALG-007": "integrated",
    "LH26-E-ALG-008": "additional-time",
    "LH26-E-ALG-009": "additional-time",
    "INF7-16-GYM-PK-KK-002": "additional-time",
    "INF7-16-GYM-PK-MI-003": "additional-time",
    "INF7-16-GYM-PK-SV-002": "additional-time",
    "INF7-16-GYM-IK-IGD-004": "integrated",
    "INF7-16-GYM-PK-AB-002": "additional-time",
    "INF7-16-GYM-PK-SV-001": "additional-time",
    "INF7-16-GYM-IK-IGD-006": "additional-time",
    "INF7-16-GYM-PK-AB-005": "integrated",
    "INF7-16-GYM-PK-AB-006": "additional-time",
    "INF7-16-GYM-PK-KK-006": "integrated",
    "LH26-E-DP-013": "additional-time",
    "LH26-E-PROG-003": "unresolved",
    "LH26-E-PROG-004": "unresolved",
    "LH26-E-DP-014": "additional-time",
}

PRIOR_20_TIME_REVIEW_IDS = (
    "TR-BMB16-GYM-IK-GM-001",
    "TR-BMB16-GYM-IK-GM-002",
    "TR-BMB16-GYM-IK-GM-003",
    "TR-BMB16-GYM-PK-SK-003",
    "TR-LH26-E-DA-004",
    "TR-LH26-E-DP-001",
    "TR-LH26-E-ID-009",
    "TR-BMB16-GYM-IK-KK-002",
    "TR-BMB16-GYM-IK-KK-003",
    "TR-BMB16-GYM-PK-HK-003",
    "TR-BMB16-GYM-PK-RK-004",
    "TR-LH26-E-KS-001",
    "TR-LH26-E-KS-002",
    "TR-LH26-E-ALG-001",
    "TR-LH26-E-PROG-001",
    "TR-LH26-E-PROG-002",
    "TR-BMB16-GYM-IK-PP-002",
    "TR-LH26-E-DA-005",
    "TR-LH26-E-DA-006",
    "TR-LH26-E-DA-008",
)
PRIOR_20_TIME_REVIEW_STRUCTURE_SHA256 = (
    "f4bc3b75f2d575ce24faf3dd6bc16ea9823eb7b44c37391744c0f14a47563908"
)
PRE_TASK15_TIME_REVIEW_COUNT = 27
PRE_TASK15_TIME_REVIEWS_SHA256 = (
    "804105f7587a0f267ee45fa19fc69a3e54aa40ed33c0913bfd051fb343d60123"
)
TASK15_AUDIT_EXPECTATIONS = {
    "LH26-E-DP-004": {
        "decision": "integrated",
        "additionalMinutes": 20,
        "phaseIds": [
            "guided-practice",
            "independent-action-product",
        ],
        "integrationContractIds": ["INT-6-ACTORS-SELECTION"],
        "evidenceContractId": "CE-IUM-6-CORE-02-LH26-E-DP-004",
        "productAnchors": (
            "mindestens zwei unterschiedliche Dienst- oder Softwarebeispiele",
            "Bedingungen-Matrix",
            "Zugang, Alter oder Kosten",
            "Daten oder Berechtigungen",
            "Werbung oder Finanzierung",
            "Nutzungsrechte oder Kündigung",
            "Fundstelle oder Beleg",
            "Auswirkung auf Nutzung und Schutzentscheidung",
        ),
        "ownReviewAnchors": (
            "Bedingungen-Auszüge",
            "Fundstellen",
            "Bedingungen-Matrix",
            "20 Minuten",
        ),
    },
    "LH26-E-DP-006": {
        "decision": "integrated",
        "additionalMinutes": 25,
        "phaseIds": [
            "independent-action-product",
            "review-revise-transfer",
        ],
        "integrationContractIds": ["INT-6-ACTORS-SELECTION"],
        "evidenceContractId": "CE-IUM-6-CORE-02-LH26-E-DP-006",
        "productAnchors": (
            "mindestens drei synthetische Fälle",
            "Kontextpfad",
            "Profilpfad",
            "Verhaltenspfad",
            "Signal oder Datenmerkmal",
            "Auswahlregel oder Auswahlmodell",
            "konkret ausgewählte Werbebotschaft",
            "Modellgrenze",
        ),
        "ownReviewAnchors": (
            "drei synthetischen Werbeauswahlpfaden",
            "Auswahlregel",
            "konkreter Werbebotschaft",
            "Modellgrenze",
            "25 Minuten",
        ),
    },
}
TASK15_PATH_AVAILABILITY = [
    "GRADE-6-BASELINE",
    "GRADE-6-REGULAR",
    "GRADE-6-EXTENDED-REFERENCE",
    "GRADE-6-EXTENDED-TRANSFER",
    "GRADE-6-EXTENDED-CODING",
]
TASK15_INTEGRATION_CONTRACT_FIELDS = (
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
)
TASK15_INTEGRATION_CONTRACT_SHA256 = (
    "6ca11792977d1f6f26dd5d3752bf935c067d5bf85e2f45bb70489670a670519f"
)
TASK15_REVIEW_EXCLUSION_SHA256 = {
    "LH26-E-DP-004": (
        "94bec0d9e9bf16f44fb717d950cc458046a3365c35912c1f101a3cd9895ac628"
    ),
    "LH26-E-DP-006": (
        "c4b8bdf6a73e789228f6dfdebc8df708921a85738d7bb6a85eddf76fafee3c76"
    ),
}
PRE_TASK16_TIME_REVIEW_COUNT = 29
PRE_TASK16_TIME_REVIEWS_SHA256 = (
    "ce391c2dd9175314bfcc2c18ef8a7a1cbed87bb85ce8d70e3589f2c7475a4a43"
)
TASK16_AUDIT_EXPECTATIONS = {
    "LH26-E-KS-014": {
        "decision": "additional-time",
        "additionalMinutes": 25,
        "phaseIds": [
            "guided-practice",
            "independent-action-product",
            "review-revise-transfer",
        ],
        "integrationContractIds": [],
        "evidenceContractId": "CE-IUM-6-CORE-06-LH26-E-KS-014",
        "productAnchors": (
            "wiederholte Abwertung",
            "Ausschluss",
            "Macht- oder Reichweitendynamik",
            "Situation → Merkmal → konkreter Fallbeleg",
            "Prävention, Hilfe und Melden",
            "begründete Eskalationsentscheidung",
        ),
        "reviewAnchors": (
            "Merkmal-und-Strategie-Spur",
            "konkrete Fallbelege",
            "25 Minuten",
        ),
    },
    "LH26-E-KS-015": {
        "decision": "additional-time",
        "additionalMinutes": 20,
        "phaseIds": [
            "build-concept",
            "independent-action-product",
        ],
        "integrationContractIds": [],
        "evidenceContractId": "CE-IUM-6-CORE-06-LH26-E-KS-015",
        "productAnchors": (
            "mehrere plausible digitale und soziale",
            "Ursachenhypothese",
            "begünstigender Faktor",
            "Unsicherheit",
            "Belegstelle",
            "kein Victim Blaming",
            "keine Ferndiagnose",
            "keine behauptete Täterabsicht",
        ),
        "reviewAnchors": (
            "Faktorenkarte",
            "Ursachenhypothese",
            "begünstigender Faktor",
            "Unsicherheitsmarkierung",
            "20 Minuten",
        ),
    },
}
GRADE6_PATH_AVAILABILITY = [
    "GRADE-6-BASELINE",
    "GRADE-6-REGULAR",
    "GRADE-6-EXTENDED-REFERENCE",
    "GRADE-6-EXTENDED-TRANSFER",
    "GRADE-6-EXTENDED-CODING",
]
TASK16_INTEGRATION_CONTRACT_SHA256 = (
    "6f324c8b4eebe4795b95eb994df048ef65a616cba409921ac78884c670345787"
)
TASK16_REVIEW_TEXT_PROJECTION_SHA256 = {
    "LH26-E-KS-014": (
        "f6f5fb23bac6e542d73ba142de46eddc5106fbde00c2ab3879a150c3589de488"
    ),
    "LH26-E-KS-015": (
        "a1a17a14a68f7026376053e93b91143de6760eac1cd338c3b877537550bdfb7b"
    ),
}
PRE_TASK17_TIME_REVIEW_COUNT = 31
PRE_TASK17_TIME_REVIEWS_SHA256 = (
    "c6fc0760057676ae4c905ccec312ae9d7e8065932eec8a120b251bd18088d514"
)
TASK17_AUDIT_EXPECTATIONS = {
    "LH26-E-DA-009": (
        "additional-time",
        30,
        (
            "build-concept",
            "independent-action-product",
            "review-revise-transfer",
        ),
        "module-detail",
        "module-detail",
        "shared",
    ),
    "LH26-E-DA-010": (
        "additional-time", 20, ("guided-practice",),
        "module-detail", "module-detail", "shared",
    ),
    "LH26-E-DA-012": (
        "absorbed", 0,
        ("independent-action-product", "review-revise-transfer"),
        "module-detail", "module-detail", "teacher-observable",
    ),
    "LH26-E-DA-015": (
        "additional-time", 20, ("guided-practice",),
        "school-context", "school-context", "teacher-observable",
    ),
}
TASK17_REQUIRED_TEXT = {
    "LH26-E-DA-009": (
        "Mikrogeschichte", "Gestaltungs- und Wirkungsziel", "Version 1",
        "sichtbarer Feedbackbefund", "Soll-Ist-Abgleich",
        "Textrevision von Version 1 zu Version 2", "Provenienz",
        "konkrete Lizenz oder Freigabe", "eigene Anteile",
    ),
    "LH26-E-DA-010": (
        "vorhandenen vorgegebenen kuratierten Analyseprodukts",
        "Zielgruppe", "intendierte Wirkung", "Inhalts- und Formbelege",
        "Befund und begründete Inferenz getrennt",
        "Transfer in das eigene Produkt ist optional",
        "ersetzt die Analyse nicht", "ohne nachgewiesene kompatible Freigabe",
        "weder in das offen nachnutzbare Produkt übernommen",
        "noch mit ihm weiterveröffentlicht", "strengeren offenen Rechtepfad",
    ),
    "LH26-E-DA-012": (
        "mindestens drei unterscheidbare Bedienkonzepte",
        "Operation → Produktänderung", "zugehörige sichtbare Revision",
        "Operation → sichtbare Produktänderung → zugehörige Revision",
        "tatsächlichen Produktions- und Revisionszeit",
        "keine Bildschirmaufzeichnung", "Interaktionsvollprotokoll",
    ),
    "LH26-E-DA-015": (
        "mindestens zwei verschiedene Teilwege tatsächlich nutzen", "Weg A",
        "Weg B", "bereitstellen oder teilen und abrufen oder öffnen",
        "neutralen, fiktiven oder personenbezugsfreien Produkts",
        "vor Ort verfügbare, schulisch freigegebene und datenschutzkonforme",
        "tatsächliche lokale Ausführung", "lokale Konfigurationsgate",
        "Ersatzroute", "ohne eine allgemeine Plattformvoraussetzung",
        "Zugangsdaten, private Links, Inhaltsprotokolle und öffentliche "
        "Schülerkonten dürfen weder Evidenz",
    ),
}
PRE_TASK18_TIME_REVIEW_COUNT = 35
PRE_TASK18_TIME_REVIEWS_SHA256 = (
    "957ec9dbbc6140834e4f97574e08103eec131979367a0838e81263bd4fea1dc6"
)
GRADE7_DEMAND_PATH_AVAILABILITY = [
    "GRADE-7-OPTIMIZED-DEMAND",
    "GRADE-7-ROBUST-DEMAND",
    "GRADE-7-HISTORICAL-MINIMUM",
]
GRADE7_INTEGRATED_DEMAND_PATH_AVAILABILITY = [
    "GRADE-7-OPTIMIZED-DEMAND",
    "GRADE-7-ROBUST-DEMAND",
]
TASK18_AUDIT_EXPECTATIONS = {
    "INF7-16-GYM-IK-DC-001": dict(
        decision="additional-time", additionalMinutes=15,
        phaseIds=["independent-action-product"], integrationContractIds=[],
        pathAvailability=GRADE7_DEMAND_PATH_AVAILABILITY,
    ),
    "INF7-16-GYM-IK-DC-004": dict(
        decision="additional-time", additionalMinutes=15,
        phaseIds=["build-concept", "shared-consolidation"],
        integrationContractIds=[], pathAvailability=GRADE7_DEMAND_PATH_AVAILABILITY,
    ),
    "INF7-16-GYM-IK-DC-005": dict(
        decision="integrated", additionalMinutes=30,
        phaseIds=["guided-practice", "independent-action-product", "review-revise-transfer"],
        integrationContractIds=["INT-7-DATA-CODING"],
        pathAvailability=GRADE7_INTEGRATED_DEMAND_PATH_AVAILABILITY,
    ),
    "LH26-E-ID-020": dict(
        decision="absorbed", additionalMinutes=0,
        phaseIds=["build-concept", "shared-consolidation"],
        integrationContractIds=[], pathAvailability=GRADE7_DEMAND_PATH_AVAILABILITY,
    ),
    "LH26-E-ID-021": dict(
        decision="additional-time", additionalMinutes=15,
        phaseIds=["build-concept", "independent-action-product"],
        integrationContractIds=[], pathAvailability=GRADE7_DEMAND_PATH_AVAILABILITY,
    ),
}
TASK18_REQUIRED_TEXT = {
    "INF7-16-GYM-IK-DC-001": (
        "mindestens vier", "Bedeutung", "Darstellung", "Verwendungszweck",
        "Codierung nicht mit Verschlüsselung gleichsetzen",
    ),
    "INF7-16-GYM-IK-DC-004": (
        "Länge einer Bitfolge", "0100000101000010", "16 Bit",
        "8 Bit = 1 Byte", "16 Bit = 2 Byte", "kB", "MB", "GB", "TB",
        "ausdrücklich dezimal",
    ),
    "INF7-16-GYM-IK-DC-005": (
        "Zahl → 8-Bit-Folge", "8-Bit-Folge → Zahl", "Stellenwertmethode",
        "2^7", "2^0", "Summe der Stellenwerte", "führende Nullen",
        "0 ↔ 00000000", "127 ↔ 01111111", "128 ↔ 10000000",
        "255 ↔ 11111111", "unbekannten Prüffall",
    ),
    "LH26-E-ID-020": (
        "Länge einer Bitfolge", "0100000101000010", "16 Bit",
        "8 Bit = 1 Byte", "16 Bit = 2 Byte", "ausschließlich",
    ),
    "LH26-E-ID-021": (
        "Kilo", "Mega", "Giga", "Tera", "10^3", "10^6", "10^9",
        "10^12", "kB", "MB", "GB", "TB", "2 kB = 2 × 10^3 Byte",
        "3 MB = 3 × 10^6 Byte", "4 GB = 4 × 10^9 Byte",
        "5 TB = 5 × 10^12 Byte",
    ),
}
TASK18_FORBIDDEN_TEXT = {
    "INF7-16-GYM-IK-DC-001": (
        "beispiele werden nur genannt", "codierung und verschlüsselung werden gleichgesetzt",
        "codierung wird mit verschlüsselung gleichgesetzt",
        "grade-7-optimized-demand ist verfügbar",
        "jahresurteil bleibt nicht red",
    ),
    "INF7-16-GYM-IK-DC-004": (
        "bitfolgenlänge ohne bit-byte-beziehung", "größere einheiten bleiben unklar",
        "größere einheiten werden binär ausgewiesen",
    ),
    "INF7-16-GYM-IK-DC-005": (
        "nur eine umwandlungsrichtung", "ohne stellenwerterklärung",
        "ohne führende nullen", "ohne grenzfälle", "ohne stellenwechselfälle",
        "ohne unbekannten prüffall", "nur die vorwärtsumwandlung",
        "nur die rückwärtsumwandlung",
    ),
    "LH26-E-ID-020": (
        "größere präfixe sind für diesen record pflicht",
        "kilo, mega, giga und tera werden vorausgesetzt",
        "kilo und mega sind für id-020 verpflichtend",
    ),
    "LH26-E-ID-021": (
        "präfixe werden nur genannt", "binärpräfixe werden vermischt",
        "kib", "mib", "gib", "tib", "ohne umrechnung nur aufgezählt",
    ),
}
TASK18_REVIEW_ANCHORS = {
    "INF7-16-GYM-IK-DC-005": (
        "ausschließlich", "bestehende geprüfte Bit- und Codespur",
        "bis IUM-7-CORE-02", "Stellenwertmethode",
        "Grenz- und Stellenwechselfälle", "unbekannte Prüffall",
    ),
    "LH26-E-ID-020": (
        "exakt derselbe Bit-und-Byte-Ausschnitt wie DC-004",
        "0100000101000010 → 16 Bit", "8 Bit = 1 Byte", "16 Bit = 2 Byte",
        "keine zweite Zeitbeanspruchung",
    ),
    "LH26-E-ID-021": (
        "über die bloße Dezimalkennzeichnung in DC-004 hinaus",
        "tatsächlich ausgeführten Umrechnungen", "nicht doppelt",
    ),
}
TASK18_REVIEW_TEXT_PROJECTION_SHA256 = {
    "INF7-16-GYM-IK-DC-001": (
        "6254abf3c0e4d9258277401942d231add017790316497cb8ec41817e775b7a9a"
    ),
    "INF7-16-GYM-IK-DC-004": (
        "3a8017b772f75928cdc586b5109579a661654f958b798a60d5557f01ebb805e2"
    ),
    "INF7-16-GYM-IK-DC-005": (
        "465033f5c6bb22e73eb31c08187a702d4f134b4f280926506bc1afc904afb355"
    ),
    "LH26-E-ID-020": (
        "a1e53e36c7480c1c920cfe369f0f12e11c67cc8c2dd084ab1d7f94296abbbd87"
    ),
    "LH26-E-ID-021": (
        "34b4c2cd951463a9c1832c3412f4204bf2fbef992189dab56918306bf920bd93"
    ),
}
TASK18_INTEGRATION_FORBIDDEN_TEXT = (
    "alltagscodierungs-landkarte", "stellenwertmethode", "grenzfallprüfung",
    "führende nullen", "dezimalpräfixumrechnung",
)
TASK18_INTEGRATION_CONTRACT_SHA256 = (
    "159dce0cbf75630d5ab14d2fc76cbc8a9e226b4297ab718d1fa3eb6ae4cec6f2"
)
TASK18_CORE01_STABLE_FIELDS_SHA256 = (
    "556c09ce1718903c73afa087de58dafc85db567f3d061ef89aa175e7cecea8ca"
)
TASK18_GRADE7_VARIANTS_SHA256 = (
    "445004380123fc9bccb245bfc33d6b43b466047e4cb70220386d426ec736dfdd"
)
TASK18_GRADE7_JUDGEMENT_SHA256 = (
    "0fb10a96a001e1f920d7f9197d87899c9523d96c1e8649cfc99cd11c14f3f128"
)
PRE_TASK19_TIME_REVIEW_COUNT = 40
PRE_TASK19_TIME_REVIEWS_SHA256 = (
    "2d0242bf62f92f561781a09183ddeafdf8638b296e850a60ad1dda1e5bf88138"
)
TASK19_AUDIT_EXPECTATIONS = {
    "INF7-16-GYM-IK-ALG-003": dict(
        decision="integrated", additionalMinutes=20,
        phaseIds=["guided-practice"],
        integrationContractIds=["INT-7-PROGRAMMING"],
        pathAvailability=GRADE7_INTEGRATED_DEMAND_PATH_AVAILABILITY,
    ),
    "INF7-16-GYM-PK-MI-005": dict(
        decision="additional-time", additionalMinutes=20,
        phaseIds=["independent-action-product", "review-revise-transfer"],
        integrationContractIds=[],
        pathAvailability=GRADE7_DEMAND_PATH_AVAILABILITY,
    ),
    "INF7-16-GYM-PK-SV-003": dict(
        decision="additional-time", additionalMinutes=20,
        phaseIds=["independent-action-product", "review-revise-transfer"],
        integrationContractIds=[],
        pathAvailability=GRADE7_DEMAND_PATH_AVAILABILITY,
    ),
    "LH26-E-ALG-007": dict(
        decision="integrated", additionalMinutes=25,
        phaseIds=["build-concept"],
        integrationContractIds=["INT-7-PROGRAMMING"],
        pathAvailability=GRADE7_INTEGRATED_DEMAND_PATH_AVAILABILITY,
    ),
    "LH26-E-ALG-008": dict(
        decision="additional-time", additionalMinutes=15,
        phaseIds=["guided-practice"],
        integrationContractIds=[],
        pathAvailability=GRADE7_DEMAND_PATH_AVAILABILITY,
    ),
    "LH26-E-ALG-009": dict(
        decision="additional-time", additionalMinutes=15,
        phaseIds=["independent-action-product"],
        integrationContractIds=[],
        pathAvailability=GRADE7_DEMAND_PATH_AVAILABILITY,
    ),
}
TASK19_REQUIRED_TEXT = {
    "INF7-16-GYM-IK-ALG-003": (
        "änderbaren Wertespeicher", "alten Wert", "neuen Wert",
        "auslösende Anweisung", "20 Minuten eigene",
    ),
    "INF7-16-GYM-PK-MI-005": (
        "plattformneutrales grafisches Modellierungswerkzeug",
        "tatsächlich einsetzen", "erstellt, bearbeitet und korrigiert",
        "Anzeige, Demo oder bloße Tracingoberfläche genügt nicht",
    ),
    "INF7-16-GYM-PK-SV-003": (
        "gerichteten", "beschrifteten Datenabhängigkeitsgraphen",
        "Eingabedatum", "Variablenzustand vor der Anweisung",
        "Variablenzustand nach der Anweisung", "Ausdrucksergebnis",
        "Ausgabeobjekt", "liest", "schreibt", "hängt ab von",
        "mindestens eine Abhängigkeit", "Änderungsfolge",
    ),
    "LH26-E-ALG-007": (
        "Anweisung", "Schleife mit konstanter Durchlaufzahl",
        "Schleife mit Bedingung", "Verzweigung",
        "Ausdruck ohne Operator", "Ausdruck mit arithmetischem Operator",
        "Ausdruck mit Vergleichsoperator", "25 Minuten eigene",
    ),
    "LH26-E-ALG-008": (
        "Quelle oder innerem Ausdruck", "konsumierenden Operanden",
        "Parameter oder Ziel", "Ausdrucksergebnis", "Empfänger",
        "keinen Rückgabewert", "keine Funktionsrückgabe unterstellt",
    ),
    "LH26-E-ALG-009": (
        "Zeichenkette", "Zahl", "Wahrheitswert", "Werten und Ausdrücken",
        "Eingabe", "Zwischenergebnis", "Bedingung", "Ausgabe",
        "begründet", "15 Minuten eigene Produktzeit",
    ),
}
TASK19_FORBIDDEN_TEXT = {
    "INF7-16-GYM-IK-ALG-003": (
        "variable wird nur als unveränderlicher wert bezeichnet",
        "variable ist konstant",
        "alte zustand ist entbehrlich",
        "zustandsänderung ohne alten wert",
        "zustandsänderung ohne neuen wert",
        "zustandsänderung ohne auslösende anweisung",
        "derselbe programmfall genügt zur absorption",
        "dieselbe traceansicht allein rechtfertigt integration",
    ),
    "INF7-16-GYM-PK-MI-005": (
        "eine bloße anzeige oder demo genügt",
        "nur anzeigen reicht aus",
        "erstellen, bearbeiten und korrigieren entfallen",
        "das werkzeug wird nur gezeigt",
        "derselbe programmfall genügt zur absorption",
        "dasselbe grafische werkzeug allein rechtfertigt integration",
    ),
    "INF7-16-GYM-PK-SV-003": (
        "zeitliche reihenfolge allein genügt",
        "weder gerichtete kanten noch labels",
        "ein graph ohne gerichtete datenabhängigkeit genügt",
        "derselbe programmfall genügt zur absorption",
        "dasselbe grafische werkzeug allein rechtfertigt integration",
    ),
    "LH26-E-ALG-007": (
        "nur eine schleifenvariante genügt",
        "ausdrucksformen werden nicht unterschieden",
        "ein demonstrierter trace genügt für die integration",
        "ein anderer programmfall genügt für die integration",
    ),
    "LH26-E-ALG-008": (
        "jede anweisung hat einen rückgabewert",
        "jede anweisung liefert immer ein ergebnis",
        "funktionsrückgabe wird ohne funktion unterstellt",
        "derselbe programmfall genügt zur absorption",
        "dieselbe traceansicht allein rechtfertigt integration",
    ),
    "LH26-E-ALG-009": (
        "nur zahlen werden typisiert",
        "typnamen ohne begründung genügen",
        "wert und datentyp werden gleichgesetzt",
        "derselbe programmfall genügt zur absorption",
    ),
}
TASK19_REVIEW_TEXT_PROJECTION_SHA256 = {
    "INF7-16-GYM-IK-ALG-003": (
        "9cfa7ecc46a24905c233707318cd4903c0c8b1994dc81a13c278269de87a80c8"
    ),
    "INF7-16-GYM-PK-MI-005": (
        "1dd9902c75088ebabdceb99cb1cc03b78475c10e38e20c76e0b36c00f93ab3d3"
    ),
    "INF7-16-GYM-PK-SV-003": (
        "4bb10e02783d9144d4b01ca1d3b20993e030abdcba7934dc7ad6d958c2552e48"
    ),
    "LH26-E-ALG-007": (
        "5953cd0365025b3b529ea60ec7810579e139a3aa7b8340fb4e568a92b87f4e94"
    ),
    "LH26-E-ALG-008": (
        "b8bd0aa5715ab8fdb539300aa26555accb9680e635d90c3845e3cb12ce7b4a89"
    ),
    "LH26-E-ALG-009": (
        "b51d775c810eca8a5d4604d2c317350efe7417f8f0b74973f9d5ebf9ade9cb80"
    ),
}
TASK19_INTEGRATION_FORBIDDEN_TEXT = (
    "ersetzt Implementierung", "ersetzt Codeausführung",
    "ersetzt Normal-, Grenz- und Gegenfalltests", "ersetzt Debugging",
    "trägt die Implementierung", "trägt die Tests", "trägt das Debugging",
    "gemeinsame Spur macht eine eigene Implementierung unnötig",
    "ein nur demonstrierter Trace genügt",
    "Vorführung des Ablaufs reicht für die Anrechnung",
    "ein anderer Programmfall genügt",
)
TASK19_MI005_FALLBACK_REQUIRED_TEXT = (
    "alternatives editierbares grafisches Modellierungswerkzeug oder Hilfsmittel",
    "Lernenden selbst ein Modell erstellen, bearbeiten und korrigieren",
    "statische, angezeigte oder vorbereitete Ersatzdarstellung genügt nicht",
    "ohne ein solches Fallback",
    "nicht als pilotiert oder zeitlich bestätigt",
)
TASK19_MI005_FALLBACK_FORBIDDEN_TEXT = (
    "vorbereitete Ersatzdarstellung nutzen",
    "bei Ausfall genügt eine statische Ersatzdarstellung",
)
TASK19_INTEGRATION_CONTRACT_SHA256 = (
    "693e68feee70291680a324372235ff2fb03d6eddab76941354a26bc47f13911c"
)
TASK19_CORE03_STABLE_FIELDS_SHA256 = (
    "a2f4d566b6b2721fc59228f9e4c49ff8dc4db93aed27c46353feaaf11ad8490a"
)
PRE_TASK20_TIME_REVIEW_COUNT = 46
PRE_TASK20_TIME_REVIEWS_SHA256 = (
    "8f6b0b7c43badfd9d7989ec78b75688de23d963adc0c2ea526e7faf51ae903f6"
)
TASK20_AUDIT_EXPECTATIONS = {
    "INF7-16-GYM-PK-KK-002": dict(
        decision="additional-time", additionalMinutes=25,
        phaseIds=["independent-action-product", "review-revise-transfer"],
        integrationContractIds=[],
        pathAvailability=GRADE7_DEMAND_PATH_AVAILABILITY,
    ),
    "INF7-16-GYM-PK-MI-003": dict(
        decision="additional-time", additionalMinutes=25,
        phaseIds=["guided-practice", "independent-action-product"],
        integrationContractIds=[],
        pathAvailability=GRADE7_DEMAND_PATH_AVAILABILITY,
    ),
    "INF7-16-GYM-PK-SV-002": dict(
        decision="additional-time", additionalMinutes=20,
        phaseIds=["independent-action-product", "review-revise-transfer"],
        integrationContractIds=[],
        pathAvailability=GRADE7_DEMAND_PATH_AVAILABILITY,
    ),
}
TASK20_REQUIRED_TEXT = {
    "INF7-16-GYM-PK-KK-002": (
        "konkret benannte andere Lerngruppe der Klasse 7 ohne Programmvorwissen",
        "Adressaten- und Vorwissensnotiz",
        "Anpassung von Erklärungstiefe oder Beispiel",
        "vier sichtbare Abschnitte", "Sachverhalt", "eigener Idee",
        "Lösungsweg", "Ergebnis", "fachlich korrektes Glossar",
        "Algorithmus", "Variable", "Verzweigung", "Schleife",
        "Testfall", "Fehlerhypothese", "programmbezogenes Beispiel",
        "jede lernende Person", "eigene zielgruppenbezogene Erklärung",
        "begründete Anpassungsentscheidung",
    ),
    "INF7-16-GYM-PK-MI-003": (
        "mindestens zwei konkrete Fälle oder Testeingaben",
        "eigene Invariante-/Variationsentscheidung", "invariante",
        "charakteristische", "verallgemeinerbare Bestandteile",
        "Variation oder Zufallsdetails", "verallgemeinertes Modell",
        "Teillösung", "beide Ausgangsfälle", "weiteren Prüffall",
        "Jede lernende Person",
    ),
    "INF7-16-GYM-PK-SV-002": (
        "mindestens zwei tatsächlich verwendete Projektdateien",
        "Rolle und Zweck", "mehrere tatsächlich verwendete Programmbezeichner",
        "Variablen", "Funktionen oder Blöcke", "dokumentierten Namenskonvention",
        "Vorher-Nachher-Tabelle", "alten und neuen Namen",
        "gespeicherter Projektbestand und Programm",
        "tatsächliche Umbenennung", "Jede lernende Person",
        "mindestens eine Datei- oder Programmbezeichner-Umbenennung",
    ),
}
TASK20_FORBIDDEN_TEXT = {
    "INF7-16-GYM-PK-KK-002": (
        "allgemein verständliche sprache genügt",
        "zielgruppe und vorwissen sind entbehrlich",
        "viererstruktur entfällt", "glossar oder beispiel entfallen",
        "präsentation des teamprodukts genügt",
        "ein teammitglied erledigt die erklärung für alle",
        "dasselbe teamprodukt begründet recordbezogene integration",
        "die 90 minuten werden für kk-002 erneut angerechnet",
    ),
    "INF7-16-GYM-PK-MI-003": (
        "details nur löschen genügt", "ein fall genügt",
        "invariante und variation müssen nicht getrennt werden",
        "rückanwendung entfällt",
        "ein teammitglied erledigt die abstraktion für alle",
        "derselbe fall begründet recordbezogene integration",
        "die 90 minuten werden für mi-003 erneut angerechnet",
    ),
    "INF7-16-GYM-PK-SV-002": (
        "clean-code-behauptung genügt",
        "namenstabelle ohne umbenennung genügt",
        "namenskonvention entfällt",
        "x, test1 und final_final sind aussagekräftig",
        "ein teammitglied benennt für alle um",
        "dasselbe programm begründet recordbezogene integration",
        "die 90 minuten werden für sv-002 erneut angerechnet",
    ),
}
TASK20_REVIEW_TEXT_PROJECTION_SHA256 = {
    "INF7-16-GYM-PK-KK-002": (
        "2c57a058d6e8d8756a63ee35ff337e4ce7e24c10351116f4c1ad804c87ed7e1f"
    ),
    "INF7-16-GYM-PK-MI-003": (
        "4af02921932096de8f1273cb903a3988e9ac34d09f903f43fd5809db6a5bc601"
    ),
    "INF7-16-GYM-PK-SV-002": (
        "b01eee857e465660c697dd8920a6ab47e1c7b6ada948bed5c382258c59780f1c"
    ),
}
TASK20_INTEGRATION_FORBIDDEN_TEXT = (
    "INF7-16-GYM-PK-KK-002", "INF7-16-GYM-PK-MI-003",
    "INF7-16-GYM-PK-SV-002", "Zielgruppenkommunikation",
    "Abstraktionshandlung", "Namensrefaktorierung",
    "gemeinsame Präsentation trägt die drei Zielrecords",
    "Teamarbeit ersetzt die individuelle Fachhandlung",
)
TASK20_INTEGRATION_CONTRACT_SHA256 = (
    "693e68feee70291680a324372235ff2fb03d6eddab76941354a26bc47f13911c"
)
TASK20_CORE04_STABLE_FIELDS_SHA256 = (
    "c814b012ffc480cf88881dc6d52247c1dd3115db5404f1114fa2c6c60777d82d"
)
PRE_TASK21_TIME_REVIEW_COUNT = 49
PRE_TASK21_TIME_REVIEWS_SHA256 = (
    "0c7e4b41925b9d268d299ee8ae9c36aeaaf66f585b85fd10d2452daff6b180ee"
)
TASK21_AUDIT_EXPECTATIONS = {
    "INF7-16-GYM-IK-IGD-004": dict(
        decision="integrated", additionalMinutes=30,
        phaseIds=["guided-practice"],
        integrationContractIds=["INT-7-NET-SECURITY"],
        pathAvailability=GRADE7_INTEGRATED_DEMAND_PATH_AVAILABILITY,
        evidenceMode="module-detail",
    ),
    "INF7-16-GYM-PK-AB-002": dict(
        decision="additional-time", additionalMinutes=30,
        phaseIds=["review-revise-transfer"], integrationContractIds=[],
        pathAvailability=GRADE7_DEMAND_PATH_AVAILABILITY,
        evidenceMode="module-detail",
    ),
    "INF7-16-GYM-PK-SV-001": dict(
        decision="additional-time", additionalMinutes=30,
        phaseIds=["independent-action-product"],
        integrationContractIds=[],
        pathAvailability=GRADE7_DEMAND_PATH_AVAILABILITY,
        causeClass="school-context", evidenceMode="school-context",
    ),
}
TASK21_REQUIRED_TEXT = {
    "INF7-16-GYM-IK-IGD-004": (
        "mehreren vollständig vorgegebenen fiktiven Bedrohungsfällen",
        "mobile Geräte und Datenträger", "mindestens vier Paaren",
        "Verlust, Diebstahl oder unbefugter Zugriff", "Displaysperre",
        "Geräte- oder Datenträgerverschlüsselung",
        "nicht vertrauenswürdige Wechseldatenträger oder Schadsoftware",
        "freigegebenen Datenträgern und Pfaden", "Updates",
        "Schadsoftwareprüfung", "unsichere Übertragung",
        "freigegebenem Übertragungsweg", "Sicht- und Zugriffsschutz",
        "Beschädigung oder Ausfall", "Backup", "geprüfter Wiederherstellung",
        "Risiko", "mögliche Maßnahme", "Schutzwirkung", "Grenze",
        "Zielkonflikt", "Persönliche Geräte werden nicht verändert",
        "Gerätekennungen nicht erhoben", "Jede lernende Person",
        "eigene vollständige Risiko–Maßnahme-Spur",
    ),
    "INF7-16-GYM-PK-AB-002": (
        "innerhalb der bestehenden CORE-05-Phase",
        "Modellelement", "Vorhersage", "Datenweg",
        "entsprechenden beobachteten realen Schritt",
        "sicheren, nichtpersonalen tatsächlichen oder kuratierten",
        "Client–Server- und Speicherworkflows", "Übereinstimmungen",
        "Abweichungen", "Auslassungen", "Modellgrenze",
        "begründete Modellrevision", "lokale Freigabegate",
        "Paketaufzeichnung", "private Protokolle", "Zugangsdaten",
        "Jede lernende Person", "eigene Modell–Realsituation-Tabelle",
    ),
    "INF7-16-GYM-PK-SV-001": (
        "innerhalb der bestehenden CORE-05-Phase",
        "tatsächliche lokale Schulnetznutzung", "Freigabe-",
        "Orientierungs- und technischer Anlaufzeit", "Jede lernende Person",
        "vor Ort freigegebenes, lokal verfügbares und datenschutzkonformes",
        "neutrales Arbeitsziel", "freigegebenen Speicherort oder Pfad",
        "neutrales, fiktives und personenfreies Testartefakt",
        "ruft es erneut ab", "öffnet es", "verifiziert das Aufgabenergebnis",
        "falls er lokal unterstützt ist", "ausschließlich Arbeitsziel",
        "Pfadbezeichnung oder Pfadkategorie", "ausgeführte Operationen",
        "Ergebnis der Abruf- und Öffnungsprüfung", "actual-local-use",
        "bleibt der Record partial", "Zeitentscheidung unbestätigt",
    ),
}
TASK21_FORBIDDEN_TEXT = {
    "INF7-16-GYM-IK-IGD-004": (
        "allgemeine sicherheitstipps genügen",
        "drei risiko–maßnahme-paare genügen",
        "schutzwirkung und grenze entfallen",
        "die maßnahmen bieten vollständigen schutz",
        "persönliche geräte werden verändert",
        "gerätekennungen werden erhoben",
        "ein teammitglied erstellt die risiko–maßnahme-spur für alle",
        "integration verkürzt die igd-004-schutzhandlung",
        "die 135 minuten werden in core-05 erneut gezählt",
    ),
    "INF7-16-GYM-PK-AB-002": (
        "das modell ist vereinfacht und das genügt",
        "ein modell-modell-vergleich genügt", "beobachtung entfällt",
        "abweichung und auslassung entfallen", "modellgrenze entfällt",
        "begründete revision entfällt", "paketmitschnitt ist zulässig",
        "private logs werden gespeichert", "zugangsdaten werden dokumentiert",
        "ein teammitglied erstellt tabelle und revision für alle",
        "dasselbe systemmodell absorbiert ab-002",
        "die 135 minuten werden von ab-002 abgezogen",
    ),
    "INF7-16-GYM-PK-SV-001": (
        "eine simulation schließt sv-001", "eine demonstration schließt sv-001",
        "eine screenshotspur schließt sv-001",
        "eine kuratierte ersatzspur schließt sv-001",
        "das vorab-freigabegate entfällt",
        "ohne lokale konfiguration gilt der record als geschlossen",
        "technische anlaufzeit entfällt", "zugangsdaten werden dokumentiert",
        "ip-adressen werden dokumentiert", "private dateien werden erhoben",
        "ein teammitglied führt die lokale nutzung für alle aus",
        "derselbe workflow integriert sv-001",
        "die 135 minuten werden von sv-001 abgezogen",
    ),
}
TASK21_REVIEW_TEXT_PROJECTION_SHA256 = {
    "INF7-16-GYM-IK-IGD-004": (
        "6f9abd219616f9cb046bc022c7fd7f8666b0f3fde40706c032891ce1b66f3edb"
    ),
    "INF7-16-GYM-PK-AB-002": (
        "650a123acca1c6bf9ff4da4927eda9f7de5e1a0c71d8b74581a4b2b3fce3a8d2"
    ),
    "INF7-16-GYM-PK-SV-001": (
        "233c77e6ac344ec055fad301c2cd5ff656a409586ce51f32e97b5152525fc231"
    ),
}
TASK21_INTEGRATION_FORBIDDEN_TEXT = (
    "INF7-16-GYM-PK-AB-002", "INF7-16-GYM-PK-SV-001",
    "Modell–Realsituation-Vergleich wird gemeinsam getragen",
    "tatsächliche lokale Schulnetznutzung wird gemeinsam getragen",
    "gemeinsames Modell ersetzt Beobachtung und Revision",
    "gemeinsamer Datenweg ersetzt die tatsächliche lokale Ausführung",
    "135 Minuten werden in IUM-7-CORE-05 erneut gezählt",
    "IGD-004-Schutzhandlung wird verkürzt",
)
TASK21_INTEGRATION_CONTRACT_SHA256 = (
    "db03def06edd105a8f992efb176ea4f654cc38cc53c9e968007197c45eb15c33"
)
TASK21_CORE05_STABLE_FIELDS_SHA256 = (
    "f8d91f833997fdedef5c642343794fccb9a898680d7f043f50e815490fe3c11c"
)
PRE_TASK22_TIME_REVIEW_COUNT = 52
PRE_TASK22_TIME_REVIEWS_SHA256 = (
    "eed12ea254379c0d9a319c6bdcca43364881bbf82d2c74c0f6b50c4c6c283327"
)
TASK22_AUDIT_EXPECTATIONS = {
    "INF7-16-GYM-IK-IGD-006": dict(
        decision="additional-time", additionalMinutes=20,
        phaseIds=["build-concept"], integrationContractIds=[],
        pathAvailability=GRADE7_DEMAND_PATH_AVAILABILITY,
        sourceTimeImpactLevel="review-required", sequenceEvidenceId=None,
    ),
    "INF7-16-GYM-PK-AB-005": dict(
        decision="integrated", additionalMinutes=25,
        phaseIds=["independent-action-product"],
        integrationContractIds=["INT-7-DATA-MEDIA-SOCIETY"],
        pathAvailability=GRADE7_INTEGRATED_DEMAND_PATH_AVAILABILITY,
        sourceTimeImpactLevel="review-required", sequenceEvidenceId=None,
    ),
    "INF7-16-GYM-PK-AB-006": dict(
        decision="additional-time", additionalMinutes=20,
        phaseIds=["review-revise-transfer"], integrationContractIds=[],
        pathAvailability=GRADE7_DEMAND_PATH_AVAILABILITY,
        sourceTimeImpactLevel="review-required", sequenceEvidenceId=None,
    ),
    "INF7-16-GYM-PK-KK-006": dict(
        decision="integrated", additionalMinutes=25,
        phaseIds=["guided-practice"],
        integrationContractIds=["INT-7-DATA-MEDIA-SOCIETY"],
        pathAvailability=GRADE7_INTEGRATED_DEMAND_PATH_AVAILABILITY,
        sourceTimeImpactLevel="review-required", sequenceEvidenceId=None,
    ),
    "LH26-E-DP-013": dict(
        decision="additional-time", additionalMinutes=15,
        phaseIds=["review-revise-transfer"], integrationContractIds=[],
        pathAvailability=GRADE7_DEMAND_PATH_AVAILABILITY,
        sourceTimeImpactLevel="review-required", sequenceEvidenceId=None,
        causeClass="private-local", evidenceMode="private-local",
        evidenceVisibility="private-local",
    ),
    "LH26-E-PROG-003": dict(
        decision="unresolved", additionalMinutes=0, phaseIds=[],
        integrationContractIds=[], pathAvailability=[],
        sourceTimeImpactLevel="roadmap-dependent",
        sequenceEvidenceId="SE-LH26-E-PROG-003",
        causeClass="roadmap-level", evidenceContractId=None,
    ),
    "LH26-E-PROG-004": dict(
        decision="unresolved", additionalMinutes=0, phaseIds=[],
        integrationContractIds=[], pathAvailability=[],
        sourceTimeImpactLevel="roadmap-dependent",
        sequenceEvidenceId="SE-LH26-E-PROG-004",
        causeClass="roadmap-level", evidenceContractId=None,
    ),
}
TASK22_PRIVACY_EXPECTATIONS = {
    "INF7-16-GYM-IK-IGD-006": ("nonpersonal-module-detail", "CE-IUM-7-CORE-08-INF7-16-GYM-IK-IGD-006"),
    "INF7-16-GYM-PK-AB-005": ("nonpersonal-module-detail", "CE-IUM-7-CORE-08-INF7-16-GYM-PK-AB-005"),
    "INF7-16-GYM-PK-AB-006": ("nonpersonal-module-detail", "CE-IUM-7-CORE-08-INF7-16-GYM-PK-AB-006"),
    "INF7-16-GYM-PK-KK-006": ("nonpersonal-module-detail", "CE-IUM-7-CORE-08-INF7-16-GYM-PK-KK-006"),
    "LH26-E-DP-013": ("nonpersonal-follow-up", "CE-IUM-7-CORE-08-LH26-E-DP-013"),
    "LH26-E-PROG-003": ("none", None),
    "LH26-E-PROG-004": ("none", None),
}
TASK22_PRIVACY_CONTRACT = {
    "id": "PC-IUM-7-CORE-08",
    "moduleId": "IUM-7-CORE-08",
    "scope": "private-local-reflection",
    "artifactOwner": "learner",
    "artifactCustody": "learner-controlled",
    "institutionalHandling": {
        "access": "prohibited",
        "observation": "prohibited",
        "collection": "prohibited",
        "transfer": "prohibited",
        "storage": "prohibited",
        "assessment": "prohibited",
    },
    "status": "working",
}
TASK22_REVIEW_TEXT_PROJECTION_SHA256 = {
    "INF7-16-GYM-IK-IGD-006": "5bdef373e12f9a8ea353d4379c1070a03c6d4b9d33de8acf353b0af64db37aa5",
    "INF7-16-GYM-PK-AB-005": "a344ff1e501340f81632dcb14ca308c79bcf2da6545431976cbe6b7ccd550593",
    "INF7-16-GYM-PK-AB-006": "316bebe9e78a3b2c801dd31e907100147e66d57eeb5119feaba8f058df00a273",
    "INF7-16-GYM-PK-KK-006": "48b63315c3757fe911b3dbceb72d127d22ec8d2c9f75ad8217a90a9ad23d9a73",
    "LH26-E-DP-013": "a752f95c866561f19c5178dae49c84586fca81b6677b1f40ef3fc1e68991a56b",
    "LH26-E-PROG-003": "35511c67e198cef3e87126a1078d25f34bc152f3b408501ff927b094123349d3",
    "LH26-E-PROG-004": "881ef00a2c0d3917251a0e1c587492a9b6ecedf6d6c75d19bb9046004e22fce4",
}
TASK22_REQUIRED_TEXT = {
    "INF7-16-GYM-IK-IGD-006": (
        "vollständig kuratierten alltagsrelevanten Dienstfall",
        "permanente Anfallen personenbezogener Daten",
        "während der Dienstnutzung", "Datenfolge",
        "Speicherung ausdrücklich als eigene Folge",
        "mindestens einen konkreten Nutzen", "konkrete Risiken",
        "dieselben kuratierten Akteursdaten", "Belege", "Gegenbelege",
        "Kriterien", "gemeinsame Revision", "Persönliche Live-Daten",
    ),
    "INF7-16-GYM-PK-AB-005": (
        "Gesellschaft", "Berufswelt", "persönliches Lebensumfeld",
        "betroffene Person", "Beschäftigte", "Dienstanbieter",
        "Öffentlichkeit", "kriterien- und beleggestützt", "Gegenbeleg",
        "Unsicherheit", "gemeinsames revidiertes Urteil",
        "analytischer Gegenstandsbereich", "keine Offenlegung",
        "CORE-09-Mechanismuskarte ersetzt", "vollständige CORE-08-Breite",
    ),
    "INF7-16-GYM-PK-AB-006": (
        "Jede lernende Person", "Darf ein digitaler Dienst personenbezogene "
        "Daten zur Auswahl und Reichweitensteuerung verwenden?",
        "eigene Position", "Kriterien", "Belegen",
        "mindestens ein Gegenargument", "argumentativ",
        "begründete Revision", "individuellen Abschnitt",
    ),
    "INF7-16-GYM-PK-KK-006": (
        "Wie berücksichtigen oder benachteiligen Datenerhebung, "
        "Kategorisierung und Ausspielung unterschiedliche Lebenslagen und "
        "Identitäten?",
        "Toleranz und Akzeptanz von Vielfalt", "mehreren benannten Perspektiven",
        "fachbezogene Argumente", "revidiertes Ergebnis",
        "keine Offenlegung eigener Identität", "persönlicher Betroffenheit",
    ),
    "LH26-E-DP-013": (
        "vollständig vorgegebenen kuratierten manipulativen Falschmeldungsfall",
        "Behauptung", "manipulative Absicht", "Akteursdaten", "Belege",
        "Gegenbelege", "Kriterien", "gemeinsame Revision",
        "private lokale Reflexionsnotiz", "eigenen Umgang", "Belegprüfung",
        "Unsicherheit", "möglicher privater Revision",
        "nicht erhoben, übertragen, eingesammelt, gespeichert oder bewertet",
        "ohne Kenntnis der Privatnotiz",
        "keine persönliche Handlungsoption als Abgabe",
        "ausschließlich auf den nichtpersonalen Anschluss",
        "weder Produkt, Evidenz noch zusätzlicher Record-Zeitclaim",
    ),
    "LH26-E-PROG-003": (
        "systematische jahrgangsweite Verbindung",
        "fortgeführter informatischer Inhalte", "stärkerer Medienbildung",
        "weder durch ein Einzelmodul noch durch das gemeinsame Dossier",
        "SE-LH26-E-PROG-003", "Task 24", "vollständige Module",
        "fachliche Tiefe", "Perspektivenbalance", "Zeitgewichtung",
    ),
    "LH26-E-PROG-004": (
        "geringere Informatikanteil", "größere Medienbildungsanteil",
        "technischer, anwendungsbezogener, gesellschaftlicher und "
        "medienbezogener Perspektiven", "jahrgangsweit und zeitgewichtet",
        "Ein zusätzliches Einzelprodukt", "SE-LH26-E-PROG-004", "Task 24",
    ),
}
TASK22_FORBIDDEN_TEXT = {
    "INF7-16-GYM-IK-IGD-006": (
        "eine einmalige dateneingabe genügt",
        "speicherung ohne datenanfall genügt",
        "pauschaler nutzen und risiken genügen",
        "persönliche live-daten werden genutzt",
        "das gemeinsame dossier absorbiert igd-006",
    ),
    "INF7-16-GYM-PK-AB-005": (
        "gesellschaft entfällt", "berufswelt entfällt",
        "persönliches lebensumfeld entfällt",
        "die perspektive betroffene person entfällt",
        "die perspektive beschäftigte entfällt",
        "die perspektive dienstanbieter entfällt",
        "die perspektive öffentlichkeit entfällt",
        "unbelegte bewertung genügt", "revision entfällt",
        "persönliche erfahrungen müssen offengelegt werden",
        "die core-09-mechanismuskarte ersetzt den core-08-abschnitt vollständig",
    ),
    "INF7-16-GYM-PK-AB-006": (
        "ein gruppenstandpunkt genügt", "bloße meinungsabfrage genügt",
        "die informatikfrage entfällt", "kriterien und belege entfallen",
        "gegenargument entfällt", "argumentative vertretung entfällt",
        "revision entfällt", "ein überzeugungsprofil wird angelegt",
        "das gemeinsame dossier integriert ab-006",
    ),
    "INF7-16-GYM-PK-KK-006": (
        "ein allgemeiner sozialappell genügt", "datenerhebung entfällt",
        "kategorisierung entfällt", "ausspielung entfällt",
        "perspektiven entfallen", "revision entfällt",
        "eigene identität wird offengelegt",
        "allgemeine vielfaltserwähnung genügt",
    ),
    "LH26-E-DP-013": (
        "die private notiz wird als abgabe eingesammelt",
        "private notiz ist produkt", "private notiz ist evidenz",
        "private notiz erhält zusätzlichen zeitclaim",
        "private notiz wird bewertet", "fertigstellung wird protokolliert",
        "teilnahme wird beobachtet",
        "der gemeinsame abschnitt benötigt kenntnis der privatnotiz",
        "persönliche handlungsoption ist abgabe",
        "das gemeinsame dossier integriert dp-013",
    ),
    "LH26-E-PROG-003": (
        "das dossier absorbiert prog-003", "coverage ist covered",
        "sequence-evidence-objekt wurde angelegt",
    ),
    "LH26-E-PROG-004": (
        "das dossier absorbiert prog-004", "coverage ist covered",
        "sequence-evidence-objekt wurde angelegt",
    ),
}
TASK22_INTEGRATION_FORBIDDEN_TEXT = (
    "INF7-16-GYM-IK-IGD-006", "INF7-16-GYM-PK-AB-006", "LH26-E-DP-013",
    "LH26-E-PROG-003", "LH26-E-PROG-004",
    "Datenfolge wird vollständig vom Dossier getragen",
    "ethische Position wird vollständig vom Dossier getragen",
    "private Reflexion wird gemeinsam getragen",
    "Mechanismuskarte ersetzt Auswirkungen und Perspektiven",
    "allgemeine Vielfaltserwähnung ersetzt die informatische Vielfaltsfrage",
)
TASK22_CORE08_STABLE_FIELDS_SHA256 = (
    "cd5b6abf1305692d5ab3b76f407cca690df5a4982c7dd346130ae6331f0929c7"
)
TASK22_INTEGRATION_CONTRACT_SHA256 = (
    "c54c7a46659d67cf3090c9ee5f142dbdf9e72cf896a59f7e38fba4cd89d980bf"
)
TASK24_SEQUENCE_EVIDENCE_SHA256 = (
    "162edbea8795bfa36d10eab2c49b789e471a865a8337577f3ef7f85f224f9304"
)
PRE_TASK22_CORE07_PRIVACY_CONTRACT_SHA256 = (
    "6e78f073474c34b7ac89ada55cd4ab22fa021f0279bed8619091335aa2a0ef41"
)
PRE_TASK23_TIME_REVIEW_COUNT = 59
PRE_TASK23_TIME_REVIEWS_SHA256 = (
    "fc6ed25e48da24103455091df92036a389cd309e98af52a9c67b145a73e93be8"
)
TASK23_AUDIT_EXPECTATIONS = {
    "LH26-E-DP-014": dict(
        decision="additional-time", additionalMinutes=20,
        phaseIds=["review-revise-transfer"], integrationContractIds=[],
        pathAvailability=GRADE7_DEMAND_PATH_AVAILABILITY,
        sourceTimeImpactLevel="review-required", sequenceEvidenceId=None,
        causeClass="private-local", evidenceMode="private-local",
        evidenceVisibility="private-local",
    ),
}
TASK23_PRIVACY_CONTRACT = {
    "id": "PC-IUM-7-CORE-10",
    "moduleId": "IUM-7-CORE-10",
    "scope": "private-local-reflection",
    "artifactOwner": "learner",
    "artifactCustody": "learner-controlled",
    "institutionalHandling": {
        "access": "prohibited",
        "observation": "prohibited",
        "collection": "prohibited",
        "transfer": "prohibited",
        "storage": "prohibited",
        "assessment": "prohibited",
    },
    "status": "working",
}
TASK23_REVIEW_TEXT_PROJECTION_SHA256 = (
    "1f00217998e28e5c3cef23dee0b010d381b95e4b9a0df9fbc0c14ea2f876dc31"
)
TASK23_CORE10_STABLE_FIELDS_SHA256 = (
    "b5537b9d3c2e704abcaf886af5cd1f8e86801f929033220d4bdb07293d0e6376"
)
TASK23_INTEGRATION_CONTRACT_SHA256 = TASK22_INTEGRATION_CONTRACT_SHA256
PRE_TASK23_PRIVACY_CONTRACTS_SHA256 = (
    "447a668d3427d583af9cfbfbe0a4ca51eadc1714cd5f738a443a3935982b3ccc"
)
TASK23_REQUIRED_TEXT = (
    "ausschließlich nichtpersonale Gegenperspektive",
    "20 Minuten",
    "bestehenden Vorher–Nachher-Medienprodukt",
    "vollständig vorgegebenen kuratierten Medienbeispielen",
    "Geschlechterrollen oder Schönheitsideale",
    "Gestaltungsmittel",
    "mögliche allgemeine Wirkung",
    "verändert das Medienprodukt nachvollziehbar",
    "ohne Kenntnis, Vorlage, Bestätigung oder Besprechung",
    "weder Nachweis noch Proxy",
    "Inhalt, Existenz, Fertigstellung oder Teilnahme",
    "eigene Erfahrung oder Selbstwahrnehmung",
    "fachliches Kriterium",
    "persönliche Handlungsoption",
    "mögliche ausschließlich private Revision",
    "ausschließlich im vorhandenen Modulbudget",
    "weder Produkt, Evidenz noch zusätzlicher Record-Zeitclaim",
    "weder integriert noch absorbiert",
    "45 bereits in IUM-7-CORE-10 gezählten gemeinsamen Minuten",
    "weder diesem Einzelrecord zugerechnet noch erneut gezählt",
    "270-Minuten-Einsparungsannahme ist kein zusätzlicher Zeitvorrat",
    "nicht verfügbare Bedarfsszenarien",
    "Jahresurteil bleibt red",
    "keine persönliche Offenlegung",
    "Personenprofil",
    "automatische Punkte",
    "automatisches Scoring",
)
TASK23_FORBIDDEN_TEXT = (
    "die privatnotiz ist produkt",
    "die privatnotiz ist evidenz",
    "die privatnotiz erhält zusätzlichen zeitclaim",
    "die privatnotiz wird eingesammelt",
    "die privatnotiz wird bewertet",
    "fertigstellung wird protokolliert",
    "teilnahme wird beobachtet",
    "der sichtbare anschluss benötigt kenntnis der privatnotiz",
    "persönliche offenlegung ist erforderlich",
    "int-7-data-media-society integriert dp-014",
    "die 45 gemeinsamen minuten werden dp-014 zugerechnet",
    "die 45 gemeinsamen minuten werden erneut gezählt",
    "die 270-minuten-einsparung ist zusätzlicher zeitvorrat",
    "ist ein verfügbarer 38-ue-pfad",
    "personenprofil wird angelegt",
    "automatische punkte werden vergeben",
    "automatisches scoring wird eingesetzt",
)
PRIVATE_LOCAL_BOUNDARY = (
    "Das private lokale Artefakt wird nicht erhoben, übertragen, "
    "eingesammelt, gespeichert oder bewertet."
)

EXPECTED_GM003_TIME_PLACEMENT_RATIONALE = (
    "Die 20 Minuten sind ausschließlich als Zeitanteil der bereits "
    "vorgesehenen eigenständigen Dateiordnungs- und Speicherhandlung in der "
    "Arbeitswegkarte verortet. Diese operative Zeitplatzierung erzeugt weder "
    "eine neue Mehrwerkzeug-Lernhandlung noch einen Produkt- oder "
    "Evidenznachweis für die weitgehend selbstständige Anwendung mehrerer "
    "Standardprogramme und Mediengeräte; der Record bleibt semantisch partial."
)
EXPECTED_GM003_PRODUCT_ONLY_FOLLOW_UP = (
    "Ausschließlich den noch fehlenden beobachtbaren semantischen "
    "Produktnachweis für eine zusammenhängende, weitgehend selbstständige "
    "Mehrwerkzeug-Handlung auditieren; die modulare Zeitplatzierung ist "
    "geklärt."
)
EXPECTED_DP001_RULE_RATIONALE = (
    "Die 15 Minuten sind ausschließlich für das Anwenden der lokalen "
    "Medienregeln, das Erläutern ihrer Zwecke und Folgen sowie die begründete "
    "Bearbeitung eines Regelkonflikts im kommentierten Regelabschnitt der "
    "Arbeitswegkarte vorgesehen. Zugangsdaten und private Inhalte bilden "
    "dabei nur eine operative Datengrenze; sie sind kein beobachtetes "
    "fachliches Lernergebnis und keine positive Produktspur."
)
EXPECTED_DP001_OPERATIONAL_BOUNDARY_RISK = (
    "Schulabhängige Regelwerke können unterschiedlich komplex sein; reale "
    "Zugangsdaten oder private Inhalte dürfen die operative Datengrenze nicht "
    "überschreiten, werden aber nicht als fachliches Lernergebnis bewertet."
)
EXPECTED_DP001_RULE_FOLLOW_UP = (
    "Im Pilot ausschließlich prüfen, ob Regelanwendung, Zweck- und "
    "Folgenerklärung sowie die begründete Konfliktlösung im Regelabschnitt "
    "erreicht werden und ob die operative Datengrenze eingehalten bleibt."
)
EXPECTED_ID009_EXECUTED_DOSSIER_RATIONALE = (
    "Vorwissensanker, ausdrücklicher Quellenabgleich und die daraus abgeleitete "
    "belegte Aussage oder Revision werden nicht als Kriterienliste ergänzt, "
    "sondern bereits als ausgeführte Recherche-, Beleg- und Urteilsarbeit im "
    "selben digitalen Quellendossier erstellt und revidiert; die drei "
    "positiven Phasen tragen damit dieselbe Produktspur ohne zusätzliche "
    "Minuten."
)
EXPECTED_ID009_INTEGRATION_BOUNDARY_RISK = (
    "Eine bloße Kriteriennennung oder ein abgehakter Quellencheck würde die "
    "verlangte Verknüpfung und Weiterverarbeitung unterschreiten; "
    "INT-5-RESEARCH-PRODUCTION trägt diese record-spezifische Vorwissens- und "
    "Urteilsspur nicht automatisch, solange sie im späteren Informationsprodukt "
    "nicht tatsächlich identisch fortgeführt wird."
)
EXPECTED_ID009_IDENTICAL_TRAIL_FOLLOW_UP = (
    "Im Pilot prüfen, ob Vorwissensanker, neue Quelleninformation, "
    "ausdrückliche Beziehung und daraus abgeleitete Aussage oder Revision in "
    "derselben Dossierspur beobachtbar erreicht werden; die Integration nur "
    "bei nachweislich identischer Quellen- und Belegspur nutzen."
)

CORE03_AUDIT_EXPECTATIONS = {
    "BMB16-GYM-IK-KK-002": {
        "decision": "additional-time",
        "additionalMinutes": 15,
        "phaseIds": ["guided-practice"],
        "rationale": (
            "Das tatsächliche lokale Verfassen, Senden oder Teilen, Abrufen "
            "und Ausführen eines neutralen Testanhangs beziehungsweise der "
            "lokalen Kernfunktion benötigt 15 Minuten angeleitete Praxis im "
            "freigegebenen schulischen Kommunikationskanal; eine Simulation "
            "der Grundfunktionen reicht nicht aus."
        ),
        "risk": (
            "Lokale Anmeldung, Kanaloberfläche, Anhangsfunktion oder "
            "Berechtigungen können technische Anlaufzeit verursachen; "
            "Zugangsdaten und Kommunikationsinhalte werden nicht dokumentiert."
        ),
        "followUp": (
            "Im Pilot die technische Anlaufzeit und die tatsächlich "
            "ausgeführten Grundfunktionen ausschließlich aggregiert prüfen "
            "und eine neutrale lokale Ersatzaufgabe bereithalten."
        ),
    },
    "BMB16-GYM-IK-KK-003": {
        "decision": "absorbed",
        "additionalMinutes": 0,
        "phaseIds": [
            "independent-action-product",
            "review-revise-transfer",
        ],
        "rationale": (
            "Teilen, Abrufen, Abstimmen und Übernehmen neutraler fiktiver "
            "Änderungsvorschläge sind dieselbe tatsächlich ausgeführte "
            "lokale Kooperationshandlung und dieselbe Revisionsspur des "
            "Kommunikationsleitfadens, deren Ausführungszeit bei "
            "LH26-E-KS-001 gezählt wird; es entsteht keine weitere "
            "Zeit- oder Produktspur."
        ),
        "risk": (
            "Eine bloß beschriebene, demonstrierte oder simulierte "
            "Projektkommunikation würde den Operator nutzen trotz vorhandener "
            "Leitfadenrevision unterschreiten."
        ),
        "followUp": (
            "Im Pilot bestätigen, dass alle vier Kooperationsschritte im "
            "lokalen Mini-Projekt tatsächlich ausgeführt werden und in "
            "derselben nichtpersonalen Revisionsspur sichtbar bleiben."
        ),
    },
    "BMB16-GYM-PK-HK-003": {
        "decision": "absorbed",
        "additionalMinutes": 0,
        "phaseIds": [
            "independent-action-product",
            "review-revise-transfer",
        ],
        "rationale": (
            "Gemeinsames Prüfen, Bearbeiten, Abstimmen und Revidieren der "
            "neutralen fiktiven Fallkarten und Regelvorschläge nutzt dieselbe "
            "tatsächliche lokale Medienkooperation und dieselbe Produktspur "
            "wie LH26-E-KS-001; dafür wird keine zweite Zeitspur angesetzt."
        ),
        "risk": (
            "Eine arbeitsteilige Sammlung ohne gemeinsame Bearbeitung, "
            "Abstimmung und Revision wäre keine ausgeführte Kooperation und "
            "dürfte nicht als absorbiert gelten."
        ),
        "followUp": (
            "Im Pilot die gemeinsame Bearbeitung und Revision als "
            "beobachtbare nichtpersonale Produktspur prüfen, ohne Nachrichten "
            "oder vollständige Kommunikationsprotokolle zu speichern."
        ),
    },
    "BMB16-GYM-PK-RK-004": {
        "decision": "additional-time",
        "additionalMinutes": 15,
        "phaseIds": ["build-concept"],
        "rationale": (
            "Rechtliche und moralische Grenzübertretungen müssen an "
            "fiktiven Fällen ausdrücklich getrennt erkannt und in begründete "
            "Regeln für das eigene soziale Verhalten überführt werden; diese "
            "Unterscheidungs- und Regelbildungsarbeit benötigt 15 Minuten "
            "eigene Begriffszeit im vorhandenen Leitfadenprodukt."
        ),
        "risk": (
            "Eine undifferenzierte Regel- oder Verbotsliste würde weder die "
            "rechtlich-moralische Trennung noch die begründete Ableitung für "
            "soziales Verhalten sichtbar machen."
        ),
        "followUp": (
            "Im Pilot prüfen, ob jede neutrale Fallkarte die getrennte "
            "Markierung und eine daraus begründete Regelrevision enthält."
        ),
    },
    "LH26-E-KS-001": {
        "decision": "additional-time",
        "additionalMinutes": 20,
        "phaseIds": ["independent-action-product"],
        "rationale": (
            "Der vor Ort freigegebene schulische Kommunikationskanal und die "
            "reale Kollaborationsmöglichkeit werden im selben Mini-Projekt "
            "tatsächlich zum Teilen, Abrufen, gemeinsamen Bearbeiten und "
            "Übernehmen neutraler Beiträge genutzt; dafür sind 20 Minuten "
            "eigenständige lokale Ausführungszeit enthalten, eine Simulation "
            "wird nicht angerechnet."
        ),
        "risk": (
            "Technisch getrennte Kommunikations- und "
            "Kollaborationswerkzeuge oder lokale Zugangsprobleme können die "
            "ausgewiesene Ausführungszeit verdrängen; Zugangsdaten bleiben "
            "undokumentiert."
        ),
        "followUp": (
            "Vor dem Pilot beide lokal freigegebenen Funktionen festlegen und "
            "aggregiert prüfen, ob Teilen, Abrufen, gemeinsames Bearbeiten "
            "und Übernehmen tatsächlich innerhalb der 20 Minuten gelingen."
        ),
    },
    "LH26-E-KS-002": {
        "decision": "additional-time",
        "additionalMinutes": 20,
        "phaseIds": ["review-revise-transfer"],
        "rationale": (
            "Die Auswirkungen eines fiktiven digitalen Konflikts werden aus "
            "mehreren Perspektiven auf mehrere Folgen reflektiert und "
            "gemeinsam diskutiert; Ergebnisse werden in der integrierten "
            "Fallkarte und den Regeln sichtbar revidiert. Diese Reflexions-, "
            "Diskussions- und Revisionsarbeit benötigt 20 Minuten."
        ),
        "risk": (
            "Eine kurze Meinungsabfrage ohne mehrere Perspektiven, mehrere "
            "Folgen, begründete Diskussion und sichtbare gemeinsame Revision "
            "würde die recordgenaue Konfliktanalyse unterschreiten."
        ),
        "followUp": (
            "Im Pilot an neutralen fiktiven Fällen prüfen, ob mehrere "
            "Perspektiven und Folgen, Ergebnisse der Reflexion und Diskussion "
            "sowie die daraus entstandene gemeinsame Revision sichtbar "
            "erreicht werden."
        ),
    },
}

EXPECTED_KS002_LEARNING_ACTION = (
    "Im Rahmen desselben tatsächlichen lokalen Mini-Projekts zur gemeinsamen "
    "Überarbeitung des bereits vorhandenen Kommunikationsleitfadens "
    "Auswirkungen eines fiktiven digitalen Konflikts aus mehreren "
    "Perspektiven auf mehrere Folgen reflektieren und diskutieren und die "
    "gemeinsame Revision der integrierten Fallkarte und der Regeln anhand der "
    "Ergebnisse sichtbar machen."
)
EXPECTED_KS002_PRODUCT_EVIDENCE = (
    "Im selben Produktteil desselben gemeinsam revidierten "
    "Kommunikationsleitfadens mit integrierten Fallkarten dokumentiert die "
    "überarbeitete fiktive Konfliktfallkarte mehrere Perspektiven, mehrere "
    "Folgen, Ergebnisse der Reflexion und Diskussion sowie die daraus "
    "hervorgegangene gemeinsame Revision; verwendet werden ausschließlich "
    "neutrale und fiktive Inhalte. Der Ausführungsnachweis hält ausschließlich "
    "die ausgeführten Schritte und die gemeinsame Revision fest; "
    "Kommunikationsinhalte werden nicht protokolliert; Zugangsdaten, private "
    "Nachrichten, personenbezogene Inhalte und vollständige "
    "Kommunikationsprotokolle werden weder erhoben noch gespeichert."
)

CORE03_REGULAR_PHASE_INCREMENTS = {
    "guided-practice": (
        15,
        "Fiktive Nachrichten und Konfliktfälle im lokalen Kanal angeleitet "
        "prüfen und überarbeiten.",
    ),
    "independent-action-product": (
        20,
        "Das zentrale Lernprodukt eigenständig erstellen: "
        "Kommunikationsleitfaden mit Fallkarten, begründeten Regeln, "
        "Beispielnachrichten und einem überarbeiteten Konfliktfall.",
    ),
    "review-revise-transfer": (
        10,
        "Leitfaden in kooperativer Anwendung prüfen, revidieren und "
        "übertragen.",
    ),
}
CORE03_REGULAR_DELTA_REVIEW_PROVENANCE = {
    "guided-practice": (15, "BMB16-GYM-IK-KK-002"),
    "independent-action-product": (20, "LH26-E-KS-001"),
    "review-revise-transfer": (10, "LH26-E-KS-002"),
}

CORE05_ALG001_AUDIT_EXPECTATION = {
    "decision": "absorbed",
    "additionalMinutes": 0,
    "phaseIds": [
        "guided-practice",
        "independent-action-product",
        "review-revise-transfer",
    ],
    "rationale": (
        "Die Klassifikation digitaler Systeme und die fallbezogene "
        "Begründung werden am selben grafischen Algorithmus tatsächlich "
        "erprobt: Die Lernenden führen ihn aus, erklären die Laufspur, "
        "korrigieren eine Abweichung und sichern Einstufung und Begründung "
        "im beobachtbaren Algorithmusprodukt. Die drei positiven Phasen "
        "tragen damit dieselbe Produktspur ohne zusätzliche Minuten; eine "
        "bloße Demonstration genügt nicht."
    ),
    "risk": (
        "Eine vorgeführte Algorithmusanimation oder bloße Kennzeichnung "
        "digitaler Systeme ohne eigene Ausführung, Erklärung der Laufspur, "
        "Fehlerkorrektur und sichtbare Klassifikations- und Begründungsspur "
        "würde den Identifikationsoperator unterschreiten."
    ),
    "followUp": (
        "Im Pilot prüfen, ob jede Einstufung mit der selbst ausgeführten "
        "Laufspur verknüpft ist und Erprobung, Erklärung, Reparatur sowie "
        "Klassifikations- und Begründungsspur im gemeinsamen Produkt "
        "beobachtbar erreicht werden."
    ),
}
CORE05_PROG002_AUDIT_EXPECTATION = {
    "decision": "unresolved",
    "additionalMinutes": 0,
    "phaseIds": [],
    "rationale": (
        "Die altersangemessene und niederschwellige "
        "Algorithmenprogression sowie ihre Abgrenzung zur Implementierungs- "
        "und Debuggingtiefe in Klasse 7 können weder einer Einzelphase noch "
        "dem Produkt von IUM-5-CORE-05 zugerechnet werden und bleiben bis "
        "zum jahrgangsübergreifenden Sequenzaudit unverortet."
    ),
    "risk": (
        "Ohne vollständigen Sequenznachweis würden die positive "
        "Klasse-5-Produktzeit und ihre Wiederaufnahme in Klasse 6 eine nicht "
        "belegte niederschwellige Progression und Abgrenzung zur fachlichen "
        "Tiefe in Klasse 7 suggerieren."
    ),
    "followUp": (
        "In Task 24 Algorithmenprodukt Klasse 5, aktive Wiederaufnahme "
        "Klasse 6, Implementierungs- und Debuggingtiefe Klasse 7, "
        "Zeitgewichtung und verfügbare Jahrespfade ausschließlich über "
        "SE-LH26-E-PROG-002 auditieren."
    ),
}
EXPECTED_CORE05_ALGORITHM_ACTION = (
    "Alltagshandlungen präzisieren, grafische Algorithmen ausführen, "
    "Abweichungen erklären und eine konstante Wiederholung als Grundbaustein "
    "modellieren."
)
EXPECTED_CORE05_ALGORITHM_PRODUCT = (
    "Ausführbarer grafischer Algorithmus mit Vorhersage, Laufprotokoll, "
    "reparierter Fassung und begründeter Schleifenentscheidung."
)

CORE06_AUDIT_EXPECTATIONS = {
    "BMB16-GYM-IK-PP-002": {
        "decision": "integrated",
        "additionalMinutes": 15,
        "phaseIds": [
            "independent-action-product",
            "review-revise-transfer",
        ],
        "integrationContractIds": ["INT-5-RESEARCH-PRODUCTION"],
        "rationale": (
            "Die 45 gemeinsamen Minuten von INT-5-RESEARCH-PRODUCTION tragen "
            "ausschließlich Identität und inhaltlichen Beleg derselben "
            "geprüften Quelle vom Quellendossier bis zum Quellenverzeichnis. "
            "Lizenz und zulässige Nutzung jedes Fremdmaterials sowie die "
            "getrennte Datenschutz- und Veröffentlichungsentscheidung mit "
            "fiktiven oder sachbezogenen Inhalten und begrenztem "
            "Adressatenkreis benötigen 15 Minuten eigene Produktions- und "
            "Revisionszeit; die Integration trägt weder diese Entscheidungen "
            "noch die Produktion."
        ),
        "risk": (
            "Bei abweichenden Quellen oder einer Ausweitung der gemeinsamen "
            "Spur auf Lizenz, Nutzung, Datenschutz, Adressatenwahl oder "
            "Produktion wäre die Integration eine Scheineinsparung; echte "
            "personenbezogene Daten dürfen nicht zur Produkt- oder "
            "Feedbackspur werden."
        ),
        "followUp": (
            "Im Pilot die identische Quellen- und Belegspur getrennt von den "
            "15 Minuten eigener Arbeit prüfen: für jedes Fremdmaterial Lizenz "
            "und zulässige Nutzung sowie separat Datenvermeidung, fiktive oder "
            "sachbezogene Inhalte und begrenzten Adressatenkreis im "
            "produzierten Informationsprodukt nachweisen."
        ),
    },
    "LH26-E-DA-005": {
        "decision": "additional-time",
        "additionalMinutes": 15,
        "phaseIds": [
            "guided-practice",
            "review-revise-transfer",
        ],
        "integrationContractIds": [],
        "rationale": (
            "Das Identifizieren von Überschrift, Fließtext, Bildunterschrift "
            "und Listenbaustein sowie die funktionale Nutzung mehrerer "
            "konkreter Formatierungen benötigen 15 Minuten angeleitete "
            "Gestaltungs- und Revisionszeit im selben Vorher-Nachher-Produkt. "
            "Der Erweiterungspfad vertieft diese Arbeit mit zusätzlich "
            "30 Minuten angeleiteter Praxis und 20 Minuten Revision."
        ),
        "risk": (
            "Eine vorbereitete Vorlage oder bloße Formatierungsdemonstration "
            "könnte Identifikation, eigene funktionale Nutzung und sichtbare "
            "Revision verdrängen; dann wäre die ausgewiesene Zeit keine "
            "recordgenaue Lernzeit."
        ),
        "followUp": (
            "Im Pilot prüfen, ob die Lernenden die vier Textbausteine selbst "
            "markieren, mehrere Formatierungen funktional einsetzen und ihre "
            "adressatengerechte Wirkung im Vorher-Nachher-Vergleich innerhalb "
            "der ausgewiesenen Zeit revidieren."
        ),
    },
    "LH26-E-DA-006": {
        "decision": "additional-time",
        "additionalMinutes": 25,
        "phaseIds": ["independent-action-product"],
        "integrationContractIds": [],
        "rationale": (
            "Auswahl und tatsächliche Nutzung eines rechtegeprüften Bildes, "
            "die Entscheidung zu Position, Größe oder Ausschnitt und die "
            "Begründung seiner Funktion für Aussage und Zielgruppe benötigen "
            "25 Minuten eigenständige Produktionszeit. Die zusätzlichen "
            "40 Produktminuten des Erweiterungspfads ermöglichen eine "
            "zweite Gestaltungsfassung, ihren Vergleich und eine dokumentierte "
            "Auswahl und Iteration innerhalb derselben Produktspur."
        ),
        "risk": (
            "Bildsuche, Import, lokale Werkzeugbedienung oder Rechteprüfung "
            "können die Gestaltungsentscheidung verdrängen; "
            "INT-5-RESEARCH-PRODUCTION darf nur bei tatsächlich identischer "
            "Dossierquelle genutzt werden und wird für diesen Record nicht "
            "pauschal angerechnet."
        ),
        "followUp": (
            "Im Pilot Produktions- und Unterstützungszeit aggregiert prüfen "
            "und sicherstellen, dass Bildnutzung, konkrete "
            "Gestaltungsentscheidung, Rechtebeleg und adressatengerechte "
            "Funktionsbegründung sichtbar erreicht werden."
        ),
    },
    "LH26-E-DA-008": {
        "decision": "additional-time",
        "additionalMinutes": 20,
        "phaseIds": ["guided-practice"],
        "integrationContractIds": [],
        "rationale": (
            "Die kriterien- und beleggebundene Analyse einer vorgegebenen "
            "Gestaltung, die Zuordnung von Inhalt, Form und Wirkung sowie das "
            "begründete Gesamturteil benötigen 20 Minuten eigene angeleitete "
            "Analysezeit vor der Produktrevision. Die zusätzlichen 30 "
            "Praxisminuten des Erweiterungspfads vertiefen diese Urteilsspur; "
            "ein Transfer in die eigene Revision ersetzt sie nicht."
        ),
        "risk": (
            "Wenn nur das eigene Produkt bewertet oder eine "
            "Gestaltungswirkung ohne konkreten Beleg behauptet wird, "
            "verschmelzen Analyse, Urteil und Revision zu einer nicht "
            "belastbaren Kurzreflexion."
        ),
        "followUp": (
            "Im Pilot prüfen, ob Inhalt, Form, Wirkung und Beleg der "
            "vorgegebenen Gestaltung sowie ein begründetes Gesamturteil "
            "innerhalb der Analysezeit vollständig vor einer optionalen "
            "Übertragung in die eigene Revision entstehen."
        ),
    },
}

CORE06_EXTENDED_PHASE_DELTAS = {
    "orientation-challenge": 0,
    "activate-prior-knowledge": 0,
    "build-concept": 0,
    "guided-practice": 30,
    "independent-action-product": 40,
    "review-revise-transfer": 20,
    "shared-consolidation": 0,
}
CORE06_POSITIVE_DELTA_REVIEW_PROVENANCE = {
    "guided-practice": ["LH26-E-DA-005", "LH26-E-DA-008"],
    "independent-action-product": [
        "BMB16-GYM-IK-PP-002",
        "LH26-E-DA-006",
    ],
    "review-revise-transfer": [
        "BMB16-GYM-IK-PP-002",
        "LH26-E-DA-005",
    ],
}
CORE06_EXTENDED_PRODUCT_FUNCTION = (
    "Zwei adressatengerechte Gestaltungsfassungen desselben "
    "Informationsprodukts erstellen; beide mit derselben getrennten Rechte- "
    "und Datenschutzspur, Baustein- und Formatierungsspur, Bildnutzungs- und "
    "Gestaltungsentscheidung sowie den aus der Analyse der vorgegebenen "
    "Gestaltung gewonnenen Kriterien vergleichen, eine Fassung begründet "
    "auswählen und sie sichtbar iterieren. Alternativenvergleich, "
    "Auswahlbegründung und zusätzliche Vorher–Nachher-Iteration bleiben im "
    "teacher-observable Produktdossier. Das zentrale Lernprodukt eigenständig "
    "erstellen: Adressatengerechtes Informationsprodukt mit "
    "Quellenverzeichnis, Gestaltungsbegründung, Kriterienfeedback, "
    "Vorher–Nachher-Revision, Präsentationsnotiz und kriteriengebundener "
    "Qualitätseinschätzung."
)
CORE06_INT5_SHARED_PHASE_OR_PRODUCT = (
    "Gemeinsame geprüfte Quellen- und Belegspur vom digitalen Quellendossier "
    "bis zum Quellenverzeichnis des Informationsprodukts; geteilt werden "
    "ausschließlich Quellenidentität und inhaltlicher Beleg."
)
CORE06_INT5_PRESERVED_LEARNING_ACTIONS = [
    (
        "IUM-5-CORE-02 zerlegt die Suchfrage, dokumentiert Suchwege, prüft "
        "Quellen und revidiert die belegte Antwort."
    ),
    (
        "IUM-5-CORE-06 übernimmt ausschließlich dieselbe geprüfte "
        "Quellenidentität und denselben inhaltlichen Beleg in das "
        "Quellenverzeichnis; Lizenz, Nutzung, Datenschutz, Adressatenwahl und "
        "Produktion bleiben eigenständige Lernhandlungen."
    ),
]
CORE06_INT5_PRESERVED_PRODUCT_EVIDENCE = [
    (
        "Das digitale Quellendossier behält Suchprotokoll, Kriterienvergleich, "
        "belegte Antwort und dokumentierte Revision."
    ),
    (
        "Das Informationsprodukt behält die nachvollziehbare Zuordnung "
        "derselben Quelle und desselben inhaltlichen Belegs zum "
        "Quellenverzeichnis."
    ),
    (
        "Die identische Quellenreferenz und der identische inhaltliche Beleg "
        "sind in beiden Produkten nachvollziehbar miteinander verknüpft; "
        "Rechte-, Datenschutz-, Adressaten- und Produktionsnachweise sind "
        "nicht geteilt."
    ),
]
CORE06_INT5_PREREQUISITES = [
    (
        "Recherchefrage und Informationsprodukt behandeln denselben "
        "fachlichen Gegenstand."
    ),
    (
        "Dieselbe im Quellendossier geprüfte Quellenreferenz und derselbe "
        "inhaltliche Beleg werden in das Informationsprodukt übernommen."
    ),
    (
        "Lizenz, zulässige Nutzung, Datenschutz, Adressatenwahl und "
        "Produktion erhalten unabhängig von der Integration eigene positive "
        "Modulzeit."
    ),
]
CORE06_INT5_RISK = (
    "Bei abweichendem Thema, nicht identischer Quellenreferenz oder nicht "
    "identischem inhaltlichem Beleg wäre die Zeitersparnis unzulässig. Eine "
    "Anrechnung von Lizenz, Nutzung, Datenschutz, Adressatenwahl oder "
    "Produktion wäre ebenfalls eine Scheinintegration."
)
CORE06_INT5_FALLBACK = (
    "Scheitert die identische Quellen- und Belegspur, erhalten Recherche und "
    "Medienprodukt wieder eigenständige Zeit für Quellenauswahl, "
    "Quellenprüfung und Belegzuordnung; die Baseline benötigt dann 45 Minuten "
    "zusätzlich und das Jahrgangsurteil wird neu berechnet. Die eigenständige "
    "Zeit für Lizenz, Nutzung, Datenschutz, Adressatenwahl und Produktion "
    "bleibt im Integrations- wie im Fallbackfall unverändert erhalten."
)

CORE07_REVIEW_CONTRACTS = {
    "BMB16-GYM-IK-MG-001": {
        "decision": "additional-time",
        "additionalMinutes": 15,
        "phaseIds": ["independent-action-product"],
    },
    "BMB16-GYM-IK-MG-002": {
        "decision": "additional-time",
        "additionalMinutes": 20,
        "phaseIds": [
            "guided-practice",
            "review-revise-transfer",
        ],
    },
    "BMB16-GYM-IK-MG-003": {
        "decision": "absorbed",
        "additionalMinutes": 0,
        "phaseIds": [
            "guided-practice",
            "independent-action-product",
            "review-revise-transfer",
        ],
    },
    "BMB16-GYM-PK-RK-001": {
        "decision": "additional-time",
        "additionalMinutes": 15,
        "phaseIds": ["guided-practice"],
    },
    "BMB16-GYM-PK-RK-002": {
        "decision": "additional-time",
        "additionalMinutes": 15,
        "phaseIds": ["independent-action-product"],
    },
    "BMB16-GYM-PK-RK-003": {
        "decision": "unresolved",
        "additionalMinutes": 0,
        "phaseIds": [],
    },
    "LH26-E-DP-003": {
        "decision": "unresolved",
        "additionalMinutes": 0,
        "phaseIds": [],
    },
}
CORE07_PRIVATE_CONCEPTS = {
    "BMB16-GYM-IK-MG-001": (
        "fictional-criteria-judgement",
        "nonpersonal-product",
    ),
    "BMB16-GYM-IK-MG-003": (
        "media-effect",
        "nonpersonal-product",
    ),
    "BMB16-GYM-PK-RK-001": (
        "fictional-use-comparison",
        "nonpersonal-product",
    ),
    "BMB16-GYM-PK-RK-002": (
        "fictional-media-reality",
        "nonpersonal-product",
    ),
}
CORE07_SEMANTIC_TRACE_GROUPS = {
    "media-effect": (
        ("wirkung",),
        ("fiktiv",),
        ("reaktionsdaten",),
        ("bedingt",),
        ("revid", "revision"),
    ),
    "fictional-criteria-judgement": (
        ("fiktiv",),
        ("kriter",),
        ("bewert", "urteil"),
        ("begründ",),
    ),
    "fictional-use-comparison": (
        ("fiktiv",),
        ("nutzungssituation",),
        ("vergleich",),
        ("gemeinsamkeit",),
        ("unterschied",),
    ),
    "fictional-media-reality": (
        ("fiktiv",),
        ("lebenswelt",),
        ("wirklichkeit",),
        ("medienwirklichkeit",),
    ),
    "shared-benefit-risk-prevention": (
        ("positiv", "nutzen"),
        ("risiko", "gefahr"),
        ("kriter",),
        ("beleg",),
        ("prävent",),
    ),
    "nonpersonal-product": (
        ("nichtpersonal", "fiktiv"),
        ("wirkungskarte",),
    ),
    "local-private-activity": (
        ("privat",),
        ("reflexionsnotiz", "reflexionsmatrix", "matrix"),
        (
            "verbleibt",
            "bleibt bei",
            "bearbeit",
            "beschreib",
            "untersuch",
            "darstell",
            "äußer",
            "anknüpf",
        ),
    ),
    "independence": (
        (
            "ohne einsicht",
            "ohne kenntnis",
            "keine angaben",
            "benötigt keine",
        ),
    ),
    "no-observation": (
        (
            "nicht eingesehen",
            "weder eingesehen",
            "nicht beobachtet",
            "weder beobachtet",
        ),
        (
            "nicht angerechnet",
            "nicht als nachweis angerechnet",
            "noch angerechnet",
        ),
    ),
}
CORE07_PARTIAL_IDS = {
    "BMB16-GYM-PK-RK-003",
    "LH26-E-DP-003",
}


EXPECTED_GRADE_5_UNITS = {
    "IUM-5-CORE-01": {"baseline": 5, "regular": 6, "extended": 6},
    "IUM-5-CORE-02": {"baseline": 4, "regular": 5, "extended": 5},
    "IUM-5-CORE-03": {"baseline": 4, "regular": 5, "extended": 5},
    "IUM-5-CORE-04": {"baseline": 3, "regular": 3, "extended": 3},
    "IUM-5-CORE-05": {"baseline": 5, "regular": 5, "extended": 6},
    "IUM-5-CORE-06": {"baseline": 5, "regular": 5, "extended": 7},
    "IUM-5-CORE-07": {"baseline": 4, "regular": 5, "extended": 6},
}

EXPECTED_GRADE_6_CORE_UNITS = {
    "IUM-6-CORE-01": {"baseline": 5, "regular": 6},
    "IUM-6-CORE-02": {"baseline": 4, "regular": 5},
    "IUM-6-CORE-03": {"baseline": 4, "regular": 4},
    "IUM-6-CORE-04": {
        "baseline": 4,
        "regular": 5,
        "targeted-extension": 6,
    },
    "IUM-6-CORE-05": {"baseline": 4, "regular": 4},
    "IUM-6-CORE-06": {"baseline": 4, "regular": 4},
    "IUM-6-CORE-07": {"baseline": 5, "regular": 6},
}

EXPECTED_GRADE_6_FLEX_CONTRACTS = {
    "IUM-6-EXT-01": {
        "standaloneUnitRange": {"min": 3, "recommended": 4, "max": 4},
        "prerequisiteModuleIds": ["IUM-6-CORE-01"],
    },
    "IUM-6-EXT-02": {
        "standaloneUnitRange": {"min": 2, "recommended": 3, "max": 3},
        "prerequisiteModuleIds": ["IUM-6-CORE-05"],
    },
    "IUM-6-TRANSFER-01": {
        "standaloneUnitRange": {"min": 2, "recommended": 4, "max": 4},
        "prerequisiteModuleIds": ["IUM-5-CORE-01", "IUM-6-CORE-05"],
    },
    "IUM-6-PROJECT-01": {
        "standaloneUnitRange": {"min": 8, "recommended": 10, "max": 12},
        "prerequisiteModuleIds": ["IUM-6-CORE-01", "IUM-6-CORE-07"],
    },
}

EXPECTED_GRADE_6_INTEGRATIONS = {
    "INT-6-ACTORS-SELECTION": {
        "moduleIds": ["IUM-6-CORE-01", "IUM-6-CORE-02"],
        "countedInModuleId": "IUM-6-CORE-01",
        "sharedMinutes": 90,
        "savingsMinutesByPath": {"baseline": 90, "regular": 45},
    },
    "INT-6-CONFLICT-PRODUCTION": {
        "moduleIds": ["IUM-6-CORE-06", "IUM-6-CORE-07"],
        "countedInModuleId": "IUM-6-CORE-07",
        "sharedMinutes": 90,
        "savingsMinutesByPath": {"baseline": 90, "regular": 0},
    },
    "INT-6-ALGORITHM-REVISIT": {
        "moduleIds": ["IUM-5-CORE-05", "IUM-6-CORE-04"],
        "countedInModuleId": "IUM-6-CORE-04",
        "sharedMinutes": 45,
        "savingsMinutesByPath": {"baseline": 45, "regular": 0},
    },
}

EXPECTED_GRADE_6_VARIANTS = {
    "GRADE-6-BASELINE": {
        "pathId": "baseline",
        "targetUnits": 30,
        "coreUnits": 30,
        "flexModuleId": None,
        "flexUnits": 0,
    },
    "GRADE-6-REGULAR": {
        "pathId": "regular",
        "targetUnits": 34,
        "coreUnits": 34,
        "flexModuleId": None,
        "flexUnits": 0,
    },
    "GRADE-6-EXTENDED-REFERENCE": {
        "pathId": "extended",
        "targetUnits": 38,
        "coreUnits": 34,
        "flexModuleId": "IUM-6-EXT-01",
        "flexUnits": 4,
    },
    "GRADE-6-EXTENDED-TRANSFER": {
        "pathId": "extended",
        "targetUnits": 38,
        "coreUnits": 34,
        "flexModuleId": "IUM-6-TRANSFER-01",
        "flexUnits": 4,
    },
    "GRADE-6-EXTENDED-CODING": {
        "pathId": "extended",
        "targetUnits": 38,
        "coreUnits": 35,
        "flexModuleId": "IUM-6-EXT-02",
        "flexUnits": 3,
    },
}

EXPECTED_GRADE_7_UNITS = {
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

EXPECTED_GRADE_7_FLEX_CONTRACTS = {
    "IUM-7-EXT-01": {
        "standaloneUnitRange": {"min": 3, "recommended": 4, "max": 5},
        "prerequisiteModuleIds": ["IUM-7-CORE-01"],
    },
    "IUM-7-TRANSFER-01": {
        "standaloneUnitRange": {"min": 3, "recommended": 4, "max": 5},
        "prerequisiteModuleIds": [
            "IUM-6-CORE-06",
            "IUM-7-CORE-05",
            "IUM-7-CORE-06",
        ],
    },
    "IUM-7-PROJECT-01": {
        "standaloneUnitRange": {"min": 8, "recommended": 10, "max": 12},
        "prerequisiteModuleIds": ["IUM-7-CORE-08", "IUM-7-CORE-10"],
    },
}

EXPECTED_GRADE_7_INTEGRATIONS = {
    "INT-7-DATA-CODING": {
        "moduleIds": ["IUM-7-CORE-01", "IUM-7-CORE-02"],
        "countedInModuleId": "IUM-7-CORE-02",
        "savingsMinutesByPath": {"optimized": 135, "robust": 90},
    },
    "INT-7-PROGRAMMING": {
        "moduleIds": ["IUM-7-CORE-03", "IUM-7-CORE-04"],
        "countedInModuleId": "IUM-7-CORE-04",
        "savingsMinutesByPath": {"optimized": 90, "robust": 90},
    },
    "INT-7-NET-SECURITY": {
        "moduleIds": [
            "IUM-7-CORE-05",
            "IUM-7-CORE-06",
            "IUM-7-CORE-07",
        ],
        "countedInModuleId": "IUM-7-CORE-07",
        "savingsMinutesByPath": {"optimized": 135, "robust": 135},
    },
    "INT-7-DATA-MEDIA-SOCIETY": {
        "moduleIds": [
            "IUM-7-CORE-08",
            "IUM-7-CORE-09",
            "IUM-7-CORE-10",
        ],
        "countedInModuleId": "IUM-7-CORE-10",
        "savingsMinutesByPath": {"optimized": 270, "robust": 45},
    },
}

EXPECTED_GRADE_7_VARIANTS = {
    "GRADE-7-OPTIMIZED-DEMAND": ("optimized", 40),
    "GRADE-7-ROBUST-DEMAND": ("robust", 46),
    "GRADE-7-HISTORICAL-MINIMUM": ("historical-minimum", 54),
}

EXPECTED_GRADE_7_DECISION_OPTIONS = [
    "additional-school-time",
    "structural-integration-or-reclassification",
    "curricular-reprioritisation",
    "earlier-preparation",
    "explicitly-incomplete-path",
]
EXPECTED_GRADE_7_UNIMPLEMENTED_OPTIONS_RATIONALE = (
    "Die drei vollständigen Kernbedarfsrechnungen liegen bei 40, 46 und 54 "
    "Unterrichtseinheiten. Selbst die unpilotierte optimierte Untergrenze "
    "überschreitet 30/34/38; daher existiert kein verfügbares "
    "Klasse-7-Angebot und das Zeiturteil bleibt red. Keine der fünf "
    "Folgeoptionen ist umgesetzt."
)


class IUM10BaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        cls.module_payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(encoding="utf-8")
        )
        cls.coverage_payload = json.loads(
            (root / "roadmap/coverage-plan.json").read_text(encoding="utf-8")
        )
        cls.remediation_payload = json.loads(
            (root / "roadmap/coverage-remediation.json").read_text(encoding="utf-8")
        )

    def validate_baseline(self, module_payload=None, coverage_payload=None, remediation_payload=None):
        return validate_ium10_baseline(
            self.module_payload if module_payload is None else module_payload,
            self.coverage_payload if coverage_payload is None else coverage_payload,
            self.remediation_payload if remediation_payload is None else remediation_payload,
        )

    def test_repository_baseline_has_immutable_module_coverage_and_handoff_contracts(self):
        result = self.validate_baseline()

        self.assertEqual(len(result["moduleIds"]), 31)
        self.assertEqual(len(result["coverageIds"]), 171)
        self.assertEqual(len(result["handoffIds"]), 60)
        self.assertEqual(
            coverage_projection_fingerprint(
                self.coverage_payload,
                self.remediation_payload,
            ),
            BASELINE_COVERAGE_PROJECTION_SHA256,
        )
        self.assertEqual(
            time_handoff_fingerprint(self.remediation_payload),
            BASELINE_TIME_HANDOFF_SHA256,
        )

    def test_rejects_mutated_module_id_grade_kind_prerequisite_or_lesson_range(self):
        mutations = (
            ("id", "IUM-5-CORE-01-MUTATED"),
            ("grade", 8),
            ("kind", "extension"),
            ("prerequisiteModuleIds", ["IUM-5-CORE-99"]),
            ("lessonRange", {"min": 99, "max": 100}),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                module_payload = copy.deepcopy(self.module_payload)
                module_payload["modules"][0][field] = value

                with self.assertRaises(IUM10ValidationError):
                    self.validate_baseline(module_payload=module_payload)

    def test_rejects_mutated_coverage_id_module_assignment_or_ium09_status(self):
        mutations = (
            ("competencyId", "MUTATED-COVERAGE-ID"),
            ("moduleIds", ["IUM-5-CORE-02"]),
            ("coverageStatus", "partial"),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                coverage_payload = copy.deepcopy(self.coverage_payload)
                coverage_payload["entries"][0][field] = value

                with self.assertRaises(IUM10ValidationError):
                    self.validate_baseline(coverage_payload=coverage_payload)

    def test_rejects_mutated_handoff_id_module_level_or_rationale(self):
        mutations = (
            ("competencyId", "MUTATED-HANDOFF-ID"),
            ("before.evidenceModuleId", "IUM-5-CORE-02"),
            ("timeImpact.level", "none-detected"),
            ("timeImpact.rationale", "Mutierte Übergabebegründung."),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                remediation_payload = copy.deepcopy(self.remediation_payload)
                target = remediation_payload["entries"][0]
                container, _, key = field.rpartition(".")
                if container:
                    target[container][key] = value
                else:
                    target[key] = value

                with self.assertRaises(IUM10ValidationError):
                    self.validate_baseline(remediation_payload=remediation_payload)


class IUM10RepositoryRunnerTests(unittest.TestCase):
    REPOSITORY_INPUTS = (
        "roadmap/module-candidates.json",
        "roadmap/coverage-plan.json",
        "roadmap/coverage-remediation.json",
        "roadmap/time-model.json",
    )

    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]

    def run_validator(self, *arguments):
        return subprocess.run(
            [
                sys.executable,
                "-B",
                "-m",
                "scripts.validate_ium10",
                *map(str, arguments),
            ],
            cwd=self.root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

    def copy_repository_inputs(self, target_root):
        for relative_path in self.REPOSITORY_INPUTS:
            source = self.root / relative_path
            target = target_root / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

    def test_module_command_validates_repository_and_reports_partial_review_count(self):
        result = self.run_validator()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout,
            "IUM10 repository validation passed: "
            "60 registered time reviews (partial baseline)\n",
        )
        self.assertEqual(result.stderr, "")

    def test_module_command_rejects_corrupted_structured_disposition(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            fixture_root = Path(temporary_directory)
            self.copy_repository_inputs(fixture_root)
            time_model_path = fixture_root / "roadmap/time-model.json"
            time_model = json.loads(time_model_path.read_text(encoding="utf-8"))
            review = next(
                review
                for review in time_model["timeReviews"]
                if review["competencyId"] == "BMB16-GYM-IK-MG-001"
            )
            review["privacyDisposition"]["privateArtifactContribution"][
                "product"
            ] = "included"
            time_model_path.write_text(
                json.dumps(time_model, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

            result = self.run_validator("--root", fixture_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn(
            "private artifact product must be excluded",
            result.stderr,
        )
        self.assertNotIn("validation passed", result.stderr)


class IUM10CapacityModelTests(unittest.TestCase):
    @staticmethod
    def unit_contract():
        return {"label": "Unterrichtseinheit", "minutes": 45}

    @staticmethod
    def capacity_model():
        return {
            "officialWeeklyUnits": 1,
            "officialStatus": "administrative-context",
            "calendarEstimate": {
                "schoolYear": "2026/2027",
                "status": "dated-project-calculation",
                "weekdayUnits": {
                    "monday": 40,
                    "tuesday": 40,
                    "wednesday": 39,
                    "thursday": 36,
                    "friday": 37,
                },
            },
            "capacityLevels": [
                "calendar-capacity",
                "local-capacity",
                "planning-capacity",
            ],
            "planningPaths": [
                {"id": "baseline", "units": 30, "status": "working"},
                {"id": "regular", "units": 34, "status": "working"},
                {"id": "extended", "units": 38, "status": "working"},
            ],
            "bufferRule": {
                "formula": "localCapacityUnits - selectedPathUnits",
                "minimumBufferUnits": 0,
                "protectedLearningFunctions": [
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
            },
            "status": "working",
        }

    def validate_capacity(self, capacity_model=None, unit_contract=None):
        return validate_capacity_model(
            self.capacity_model() if capacity_model is None else capacity_model,
            self.unit_contract() if unit_contract is None else unit_contract,
        )

    def test_returns_the_three_working_paths_for_the_45_minute_unit_and_dated_calendar(self):
        result = self.validate_capacity()

        self.assertEqual(
            result,
            {
                "baseline": {"id": "baseline", "units": 30, "status": "working"},
                "regular": {"id": "regular", "units": 34, "status": "working"},
                "extended": {"id": "extended", "units": 38, "status": "working"},
            },
        )

    def test_rejects_the_30_plus_6_heuristic_as_an_official_norm(self):
        capacity_model = self.capacity_model()
        capacity_model["officialStatus"] = "30+6 official norm"

        with self.assertRaisesRegex(IUM10ValidationError, "30\\+6"):
            self.validate_capacity(capacity_model=capacity_model)

    def test_rejects_a_negative_local_buffer(self):
        capacity_model = self.capacity_model()
        capacity_model["bufferRule"]["minimumBufferUnits"] = -1

        with self.assertRaisesRegex(IUM10ValidationError, "buffer"):
            self.validate_capacity(capacity_model=capacity_model)

    def test_rejects_a_missing_capacity_level(self):
        capacity_model = self.capacity_model()
        capacity_model["capacityLevels"].remove("local-capacity")

        with self.assertRaisesRegex(IUM10ValidationError, "capacity levels"):
            self.validate_capacity(capacity_model=capacity_model)

    def test_rejects_a_baseline_without_all_protected_learning_functions(self):
        capacity_model = self.capacity_model()
        capacity_model["bufferRule"]["protectedLearningFunctions"].remove("revision")

        with self.assertRaisesRegex(IUM10ValidationError, "protected learning functions"):
            self.validate_capacity(capacity_model=capacity_model)

    def test_rejects_boolean_values_where_integer_contract_values_are_required(self):
        mutations = (
            ("unit minutes", self.unit_contract(), ("minutes",), True),
            ("official units", self.capacity_model(), ("officialWeeklyUnits",), True),
            (
                "calendar weekday units",
                self.capacity_model(),
                ("calendarEstimate", "weekdayUnits", "monday"),
                True,
            ),
            ("path units", self.capacity_model(), ("planningPaths", 0, "units"), True),
            (
                "minimum buffer units",
                self.capacity_model(),
                ("bufferRule", "minimumBufferUnits"),
                True,
            ),
        )
        for label, payload, path, value in mutations:
            with self.subTest(label=label):
                target = payload
                for key in path[:-1]:
                    target = target[key]
                target[path[-1]] = value

                if label == "unit minutes":
                    with self.assertRaises(IUM10ValidationError):
                        self.validate_capacity(unit_contract=payload)
                else:
                    with self.assertRaises(IUM10ValidationError):
                        self.validate_capacity(capacity_model=payload)

    def test_rejects_boolean_schema_version_in_the_repository_draft(self):
        root = Path(__file__).resolve().parents[1]
        time_model = json.loads(
            (root / "roadmap/time-model.json").read_text(encoding="utf-8")
        )
        time_model["schemaVersion"] = True

        with self.assertRaisesRegex(IUM10ValidationError, "schema version"):
            validate_time_model_draft(time_model)

    def test_repository_draft_has_schema_two_and_the_migrated_private_local_contracts(self):
        root = Path(__file__).resolve().parents[1]
        time_model = json.loads(
            (root / "roadmap/time-model.json").read_text(encoding="utf-8")
        )
        module_payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(encoding="utf-8")
        )

        validate_time_model_draft(time_model, module_payload)

        self.assertEqual(time_model["schemaVersion"], 2)
        self.assertIn("privacyContracts", time_model)
        self.assertEqual(
            [contract["id"] for contract in time_model["privacyContracts"]],
            [
                "PC-IUM-5-CORE-07",
                "PC-IUM-7-CORE-08",
                "PC-IUM-7-CORE-10",
            ],
        )

    def test_repository_draft_has_capacity_contract_and_task24_sequence_records(self):
        root = Path(__file__).resolve().parents[1]
        time_model = json.loads(
            (root / "roadmap/time-model.json").read_text(encoding="utf-8")
        )
        module_payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(encoding="utf-8")
        )
        validate_time_model_draft(time_model, module_payload)

        self.assertEqual(
            set(time_model),
            {
                "schemaVersion",
                "status",
                "baseline",
                "unit",
                "capacityModel",
                "moduleContracts",
                "integrationContracts",
                "annualVariants",
                "privacyContracts",
                "timeReviews",
                "sequenceEvidence",
                "gradeJudgements",
                "risks",
                "pilotAssignments",
            },
        )
        self.assertEqual(time_model["schemaVersion"], 2)
        self.assertEqual(time_model["status"], "draft")
        self.assertEqual(
            time_model["baseline"],
            {
                "commit": IUM10_BASELINE_COMMIT,
                "moduleStructureSha256": BASELINE_MODULE_STRUCTURE_SHA256,
                "coverageProjectionSha256": BASELINE_COVERAGE_PROJECTION_SHA256,
                "timeHandoffSha256": BASELINE_TIME_HANDOFF_SHA256,
            },
        )
        self.assertEqual(
            {item["competencyId"] for item in time_model["sequenceEvidence"]},
            {
                "LH26-E-PROG-001",
                "LH26-E-PROG-002",
                "LH26-E-PROG-003",
                "LH26-E-PROG-004",
            },
        )
        self.assertEqual(time_model["risks"], [])
        self.assertEqual(time_model["pilotAssignments"], [])
        self.assertEqual(
            validate_capacity_model(time_model["capacityModel"], time_model["unit"]),
            {
                "baseline": {"id": "baseline", "units": 30, "status": "working"},
                "regular": {"id": "regular", "units": 34, "status": "working"},
                "extended": {"id": "extended", "units": 38, "status": "working"},
            },
        )


class IUM10ModuleContractTests(unittest.TestCase):
    @staticmethod
    def module_payload():
        return {
            "modules": [
                {
                    "id": "IUM-5-CORE-01",
                    "grade": 5,
                    "kind": "core",
                    "lessonRange": {"min": 5, "max": 7},
                    "competencyIds": ["COMP-CORE-01"],
                    "centralLearningAction": "Ein Modell fachlich anwenden.",
                    "centralLearningProduct": "Ein überprüfbares Modellprodukt.",
                    "prerequisiteModuleIds": [],
                    "moduleGrammar": [
                        "orientation-challenge",
                        "activate-prior-knowledge",
                        "build-concept",
                        "guided-practice",
                        "independent-action-product",
                        "review-revise-transfer",
                        "shared-consolidation",
                    ],
                },
                {
                    "id": "IUM-6-EXT-01",
                    "grade": 6,
                    "kind": "extension",
                    "lessonRange": {"min": 3, "max": 4},
                    "competencyIds": ["COMP-EXT-01"],
                    "centralLearningAction": "Eine Behauptung mit Belegen prüfen.",
                    "centralLearningProduct": "Eine begründete Prüfmatrix.",
                    "prerequisiteModuleIds": ["IUM-5-CORE-01"],
                    "moduleGrammar": [
                        "orientation-challenge",
                        "activate-prior-knowledge",
                        "guided-practice",
                        "independent-action-product",
                        "review-revise-transfer",
                        "shared-consolidation",
                    ],
                },
            ]
        }

    @staticmethod
    def phase_budgets(phase_ids):
        return [
            {
                "phaseId": phase_id,
                "minutes": 45,
                "learningFunction": f"{phase_id} fachlich durchführen.",
            }
            for phase_id in phase_ids
        ]

    @classmethod
    def core_contract(cls):
        phase_budgets = cls.phase_budgets(cls.module_payload()["modules"][0]["moduleGrammar"])
        minutes = sum(phase["minutes"] for phase in phase_budgets)
        return {
            "id": "TC-IUM-5-CORE-01",
            "moduleId": "IUM-5-CORE-01",
            "grade": 5,
            "kind": "core",
            "historicalLessonRange": {"min": 5, "max": 7},
            "competencyIds": ["COMP-CORE-01"],
            "centralLearningAction": "Ein Modell fachlich anwenden.",
            "centralLearningProduct": "Ein überprüfbares Modellprodukt.",
            "prerequisiteModuleIds": [],
            "revisitModuleIds": [],
            "pathBudgets": [
                {
                    "pathId": path_id,
                    "units": 7,
                    "minutes": minutes,
                    "directMinutes": minutes,
                    "countedSharedMinutes": 0,
                    "phaseBudgets": copy.deepcopy(phase_budgets),
                    "sharedAllocations": [],
                }
                for path_id in ("baseline", "regular", "extended")
            ],
            "standaloneUnitRange": None,
            "timeReviewIds": [],
            "integrationContractIds": [],
            "schoolDependentSteps": [],
            "risk": "Die verfügbare Schulzeit muss im Pilot geprüft werden.",
            "pilotRequired": True,
            "status": "working",
        }

    @classmethod
    def flexible_contract(cls):
        phase_budgets = cls.phase_budgets(cls.module_payload()["modules"][1]["moduleGrammar"])
        minutes = sum(phase["minutes"] for phase in phase_budgets)
        return {
            "id": "TC-IUM-6-EXT-01",
            "moduleId": "IUM-6-EXT-01",
            "grade": 6,
            "kind": "extension",
            "historicalLessonRange": {"min": 3, "max": 4},
            "competencyIds": ["COMP-EXT-01"],
            "centralLearningAction": "Eine Behauptung mit Belegen prüfen.",
            "centralLearningProduct": "Eine begründete Prüfmatrix.",
            "prerequisiteModuleIds": ["IUM-5-CORE-01"],
            "revisitModuleIds": ["IUM-5-CORE-01"],
            "pathBudgets": [
                {
                    "pathId": "standalone",
                    "units": 6,
                    "minutes": minutes,
                    "directMinutes": minutes,
                    "countedSharedMinutes": 0,
                    "phaseBudgets": phase_budgets,
                    "sharedAllocations": [],
                }
            ],
            "standaloneUnitRange": {"min": 3, "recommended": 4, "max": 6},
            "timeReviewIds": [],
            "integrationContractIds": [],
            "schoolDependentSteps": [],
            "risk": "Die zusätzliche Zeit wird nur bei lokaler Kapazität eingesetzt.",
            "pilotRequired": True,
            "status": "working",
        }

    @staticmethod
    def grade_six_core_04_module():
        return {
            "id": "IUM-6-CORE-04",
            "grade": 6,
            "kind": "core",
            "lessonRange": {"min": 5, "max": 7},
            "competencyIds": ["COMP-CORE-04"],
            "centralLearningAction": "Ein Programm schrittweise ausführen.",
            "centralLearningProduct": "Ein getestetes Programmprodukt.",
            "prerequisiteModuleIds": ["IUM-5-CORE-01"],
            "moduleGrammar": [
                "orientation-challenge",
                "activate-prior-knowledge",
                "build-concept",
                "guided-practice",
                "independent-action-product",
                "review-revise-transfer",
                "shared-consolidation",
            ],
        }

    @classmethod
    def grade_six_core_04_contract(cls, include_targeted_extension=False):
        contract = cls.core_contract()
        module = cls.grade_six_core_04_module()
        contract.update(
            {
                "id": "TC-IUM-6-CORE-04",
                "moduleId": module["id"],
                "grade": module["grade"],
                "kind": module["kind"],
                "historicalLessonRange": copy.deepcopy(module["lessonRange"]),
                "competencyIds": list(module["competencyIds"]),
                "centralLearningAction": module["centralLearningAction"],
                "centralLearningProduct": module["centralLearningProduct"],
                "prerequisiteModuleIds": list(module["prerequisiteModuleIds"]),
                "pathBudgets": contract["pathBudgets"][:2],
            }
        )
        if include_targeted_extension:
            targeted_extension = copy.deepcopy(contract["pathBudgets"][0])
            targeted_extension["pathId"] = "targeted-extension"
            contract["pathBudgets"].append(targeted_extension)
        return contract

    def contracts(self):
        return [self.core_contract(), self.flexible_contract()]

    def validate_contracts(self, contracts=None, module_payload=None):
        return validate_module_contracts(
            self.contracts() if contracts is None else contracts,
            self.module_payload() if module_payload is None else module_payload,
        )

    def test_returns_contracts_keyed_by_their_existing_module_ids(self):
        result = self.validate_contracts()

        self.assertEqual(set(result), {"IUM-5-CORE-01", "IUM-6-EXT-01"})
        self.assertEqual(result["IUM-5-CORE-01"]["id"], "TC-IUM-5-CORE-01")
        self.assertEqual(result["IUM-6-EXT-01"]["pathBudgets"][0]["pathId"], "standalone")

    def test_accepts_grade_six_core_04_with_standard_paths(self):
        contract = self.grade_six_core_04_contract()
        result = validate_module_contracts(
            [contract],
            {"modules": [self.grade_six_core_04_module()]},
        )

        self.assertEqual(result, {"IUM-6-CORE-04": contract})

    def test_accepts_grade_six_core_04_with_optional_targeted_extension(self):
        contract = self.grade_six_core_04_contract(include_targeted_extension=True)
        result = validate_module_contracts(
            [contract],
            {"modules": [self.grade_six_core_04_module()]},
        )

        self.assertEqual(
            {budget["pathId"] for budget in result["IUM-6-CORE-04"]["pathBudgets"]},
            {"baseline", "regular", "targeted-extension"},
        )

    def test_rejects_unknown_duplicate_or_malformed_contract_identity(self):
        mutations = (
            ("unknown module", "moduleId", "IUM-5-CORE-99"),
            ("wrong contract id", "id", "TC-IUM-5-CORE-99"),
        )
        for label, field, value in mutations:
            with self.subTest(label=label):
                contracts = self.contracts()
                contracts[0][field] = value
                with self.assertRaises(IUM10ValidationError):
                    self.validate_contracts(contracts=contracts)

        contracts = self.contracts()
        duplicate = copy.deepcopy(contracts[0])
        duplicate["moduleId"] = "IUM-6-EXT-01"
        duplicate["id"] = "TC-IUM-6-EXT-01"
        contracts.append(duplicate)
        with self.assertRaises(IUM10ValidationError):
            self.validate_contracts(contracts=contracts)

    def test_rejects_contract_metadata_that_diverges_from_its_module(self):
        mutations = (
            ("grade", 6),
            ("kind", "extension"),
            ("historicalLessonRange", {"min": 2, "max": 7}),
            ("competencyIds", ["COMP-OTHER"]),
            ("prerequisiteModuleIds", ["IUM-6-EXT-01"]),
            ("centralLearningAction", "Eine andere Lernhandlung."),
            ("centralLearningProduct", "Ein anderes Lernprodukt."),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                contracts = self.contracts()
                contracts[0][field] = value
                with self.assertRaises(IUM10ValidationError):
                    self.validate_contracts(contracts=contracts)

    def test_rejects_inconsistent_path_arithmetic(self):
        mutations = (
            ("unit minutes", "minutes", 314),
            ("phase total", "phaseBudgets.0.minutes", 44),
            ("direct and shared total", "directMinutes", 314),
        )
        for label, field, value in mutations:
            with self.subTest(label=label):
                contracts = self.contracts()
                budget = contracts[0]["pathBudgets"][0]
                target, _, key = field.rpartition(".")
                if target:
                    container, index = target.split(".")
                    budget[container][int(index)][key] = value
                else:
                    budget[key] = value
                with self.assertRaises(IUM10ValidationError):
                    self.validate_contracts(contracts=contracts)

        contracts = self.contracts()
        budget = contracts[0]["pathBudgets"][0]
        budget["directMinutes"] = 270
        budget["countedSharedMinutes"] = 45
        with self.assertRaises(IUM10ValidationError):
            self.validate_contracts(contracts=contracts)

    def test_rejects_missing_zero_or_unpermitted_phase_budgets(self):
        mutations = (
            ("missing core phase", "core", "phaseBudgets", lambda phases: phases[:-1]),
            ("zero core phase", "core", "phaseBudgets.0.minutes", 0),
            ("unpermitted flexible phase", "flexible", "phaseBudgets.0.phaseId", "build-concept"),
        )
        for label, contract_kind, field, value in mutations:
            with self.subTest(label=label):
                contracts = self.contracts()
                contract = contracts[0] if contract_kind == "core" else contracts[1]
                target, _, key = field.rpartition(".")
                if target == "":
                    budget = contract["pathBudgets"][0]
                    budget[key] = value(budget[key])
                else:
                    container, index = target.split(".")
                    contract["pathBudgets"][0][container][int(index)][key] = value
                with self.assertRaises(IUM10ValidationError):
                    self.validate_contracts(contracts=contracts)

    def test_rejects_missing_learning_function_non_core_paths_or_missing_pilot(self):
        mutations = (
            ("missing learning function", "learningFunction", ""),
            ("flexible core coverage", "pathId", "baseline"),
        )
        for label, field, value in mutations:
            with self.subTest(label=label):
                contracts = self.contracts()
                if field == "learningFunction":
                    contracts[0]["pathBudgets"][0]["phaseBudgets"][0][field] = value
                else:
                    contracts[1]["pathBudgets"][0][field] = value
                with self.assertRaises(IUM10ValidationError):
                    self.validate_contracts(contracts=contracts)

        contracts = self.contracts()
        contracts[0]["pilotRequired"] = False
        with self.assertRaises(IUM10ValidationError):
            self.validate_contracts(contracts=contracts)

    def test_rejects_boolean_values_in_integer_contract_fields(self):
        mutations = (
            ("standalone range minimum", "standaloneUnitRange.min", True),
            ("standalone range", "standaloneUnitRange.recommended", True),
            ("standalone range maximum", "standaloneUnitRange.max", True),
            ("path units", "pathBudgets.0.units", True),
            ("path minutes", "pathBudgets.0.minutes", True),
            ("direct minutes", "pathBudgets.0.directMinutes", True),
            ("shared minutes", "pathBudgets.0.countedSharedMinutes", True),
            ("phase minutes", "pathBudgets.0.phaseBudgets.0.minutes", True),
        )
        for label, field, value in mutations:
            with self.subTest(label=label):
                contracts = self.contracts()
                contract = contracts[1] if field.startswith("standalone") else contracts[0]
                current = contract
                for part in field.split(".")[:-1]:
                    current = current[int(part)] if part.isdigit() else current[part]
                current[field.split(".")[-1]] = value
                with self.assertRaises(IUM10ValidationError):
                    self.validate_contracts(contracts=contracts)

        contracts = self.contracts()
        budget = contracts[0]["pathBudgets"][0]
        budget["directMinutes"] = 270
        budget["countedSharedMinutes"] = 45
        budget["sharedAllocations"] = [
            {"integrationContractId": "INT-TEST", "minutes": True}
        ]
        with self.assertRaises(IUM10ValidationError):
            self.validate_contracts(contracts=contracts)

    def test_rejects_extra_path_time_without_more_practice_product_or_revision(self):
        contracts = self.contracts()
        regular = contracts[0]["pathBudgets"][1]
        regular["units"] += 1
        regular["minutes"] += 45
        regular["directMinutes"] += 45
        regular["phaseBudgets"][0]["minutes"] += 45

        with self.assertRaisesRegex(
            IUM10ValidationError,
            "practice, product, or revision",
        ):
            self.validate_contracts(contracts=contracts)

    def test_rejects_extended_focus_time_that_regresses_from_regular_path(self):
        contracts = self.contracts()
        regular = contracts[0]["pathBudgets"][1]
        regular["units"] = 8
        regular["minutes"] = 360
        regular["directMinutes"] = 360
        regular["phaseBudgets"][3]["minutes"] = 90

        extended = contracts[0]["pathBudgets"][2]
        extended["units"] = 9
        extended["minutes"] = 405
        extended["directMinutes"] = 405
        extended["phaseBudgets"][0]["minutes"] = 120
        extended["phaseBudgets"][3]["minutes"] = 60

        with self.assertRaisesRegex(
            IUM10ValidationError,
            "immediate predecessor",
        ):
            self.validate_contracts(contracts=contracts)

    def test_rejects_targeted_extension_focus_time_that_regresses_from_regular_path(self):
        contract = self.grade_six_core_04_contract(
            include_targeted_extension=True
        )
        regular = contract["pathBudgets"][1]
        regular["units"] = 8
        regular["minutes"] = 360
        regular["directMinutes"] = 360
        regular["phaseBudgets"][3]["minutes"] = 90

        targeted = contract["pathBudgets"][2]
        targeted["units"] = 9
        targeted["minutes"] = 405
        targeted["directMinutes"] = 405
        targeted["phaseBudgets"][0]["minutes"] = 120
        targeted["phaseBudgets"][3]["minutes"] = 60

        with self.assertRaisesRegex(
            IUM10ValidationError,
            "immediate predecessor",
        ):
            validate_module_contracts(
                [contract],
                {"modules": [self.grade_six_core_04_module()]},
            )


class IUM10IntegrationContractTests(unittest.TestCase):
    CONTRACT_ID = "INT-TEST-SHARED-EVIDENCE"

    @classmethod
    def module_contracts(cls):
        contracts = {}
        for module_id, counted in (("MODULE-A", False), ("MODULE-B", True)):
            path_budgets = []
            for path_id in ("baseline", "regular", "extended"):
                allocation = (
                    [{"integrationContractId": cls.CONTRACT_ID, "minutes": 45}]
                    if counted
                    else []
                )
                path_budgets.append(
                    {
                        "pathId": path_id,
                        "countedSharedMinutes": 45 if counted else 0,
                        "sharedAllocations": allocation,
                    }
                )
            contracts[module_id] = {
                "moduleId": module_id,
                "integrationContractIds": [cls.CONTRACT_ID],
                "pathBudgets": path_budgets,
            }
        return contracts

    @classmethod
    def integration_contract(cls):
        return {
            "id": cls.CONTRACT_ID,
            "moduleIds": ["MODULE-A", "MODULE-B"],
            "pathIds": ["baseline", "regular", "extended"],
            "sharedPhaseOrProduct": "Eine gemeinsame Quellen- und Belegspur.",
            "countedInModuleId": "MODULE-B",
            "sharedMinutes": 45,
            "savingsMinutesByPath": {
                "baseline": 45,
                "regular": 0,
                "extended": 0,
            },
            "preservedLearningActions": [
                "MODULE-A prüft Quellen.",
                "MODULE-B nutzt und belegt die Quellen.",
            ],
            "preservedProductAndCurriculumEvidence": [
                "Quellendossier und Produktquellenverzeichnis bleiben prüfbar.",
            ],
            "prerequisites": ["Die Produktspur nutzt dasselbe Rechercheergebnis."],
            "risk": "Getrennte Themen verhindern die gemeinsame Evidenzspur.",
            "fallback": "Beide Module erhalten eigenständige Recherche- und Produktionszeit.",
            "status": "working",
        }

    def validate_integrations(self, contracts=None, module_contracts=None):
        return validate_integration_contracts(
            [self.integration_contract()] if contracts is None else contracts,
            self.module_contracts() if module_contracts is None else module_contracts,
        )

    def test_returns_integration_contracts_keyed_by_unique_id(self):
        result = self.validate_integrations()

        self.assertEqual(result, {self.CONTRACT_ID: self.integration_contract()})

    def test_rejects_unknown_modules_paths_or_counted_module(self):
        mutations = (
            ("moduleIds", ["MODULE-A", "MODULE-MISSING"]),
            ("pathIds", ["baseline", "regular", "missing"]),
            ("countedInModuleId", "MODULE-MISSING"),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                contract = self.integration_contract()
                contract[field] = value
                with self.assertRaises(IUM10ValidationError):
                    self.validate_integrations(contracts=[contract])

    def test_rejects_missing_or_unexpected_fields_fail_closed(self):
        missing = self.integration_contract()
        missing.pop("countedInModuleId")
        unexpected = self.integration_contract()
        unexpected["note"] = "Nicht Teil des Vertrags."

        for contract in (missing, unexpected):
            with self.subTest(fields=set(contract)):
                with self.assertRaisesRegex(IUM10ValidationError, "fields"):
                    self.validate_integrations(contracts=[contract])

    def test_rejects_shared_minutes_counted_in_more_than_one_module(self):
        module_contracts = self.module_contracts()
        for budget in module_contracts["MODULE-A"]["pathBudgets"]:
            budget["countedSharedMinutes"] = 45
            budget["sharedAllocations"] = [
                {"integrationContractId": self.CONTRACT_ID, "minutes": 45}
            ]

        with self.assertRaisesRegex(IUM10ValidationError, "exactly once"):
            self.validate_integrations(module_contracts=module_contracts)

    def test_rejects_boolean_values_as_minutes(self):
        mutations = (
            ("sharedMinutes", True),
            ("savingsMinutesByPath.baseline", True),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                contract = self.integration_contract()
                current = contract
                parts = field.split(".")
                for part in parts[:-1]:
                    current = current[part]
                current[parts[-1]] = value
                with self.assertRaises(IUM10ValidationError):
                    self.validate_integrations(contracts=[contract])

        module_contracts = self.module_contracts()
        module_contracts["MODULE-B"]["pathBudgets"][0]["sharedAllocations"][0][
            "minutes"
        ] = True
        with self.assertRaises(IUM10ValidationError):
            self.validate_integrations(module_contracts=module_contracts)

    def test_rejects_unknown_module_integration_reference(self):
        module_contracts = self.module_contracts()
        module_contracts["MODULE-A"]["integrationContractIds"].append(
            "INT-UNKNOWN"
        )

        with self.assertRaisesRegex(IUM10ValidationError, "unknown integration reference"):
            self.validate_integrations(module_contracts=module_contracts)

    def test_rejects_unknown_shared_allocation_integration_id(self):
        module_contracts = self.module_contracts()
        budget = module_contracts["MODULE-A"]["pathBudgets"][0]
        budget["countedSharedMinutes"] = 45
        budget["sharedAllocations"].append(
            {"integrationContractId": "INT-UNKNOWN", "minutes": 45}
        )

        with self.assertRaisesRegex(IUM10ValidationError, "unknown shared allocation"):
            self.validate_integrations(module_contracts=module_contracts)


class IUM10AnnualVariantTests(unittest.TestCase):
    @staticmethod
    def module_contracts():
        return {
            "MODULE-A": {
                "moduleId": "MODULE-A",
                "grade": 5,
                "kind": "core",
                "pathBudgets": [
                    {"pathId": "baseline", "units": 2},
                    {"pathId": "regular", "units": 3},
                    {"pathId": "extended", "units": 3},
                ],
            },
            "MODULE-B": {
                "moduleId": "MODULE-B",
                "grade": 5,
                "kind": "core",
                "pathBudgets": [
                    {"pathId": "baseline", "units": 3},
                    {"pathId": "regular", "units": 3},
                    {"pathId": "extended", "units": 4},
                ],
            },
        }

    @staticmethod
    def annual_variant():
        return {
            "id": "GRADE-5-TEST",
            "grade": 5,
            "kind": "planning-path",
            "pathId": "baseline",
            "targetUnits": 5,
            "allocations": [
                {"moduleId": "MODULE-A", "budgetPathId": "baseline", "units": 2},
                {"moduleId": "MODULE-B", "budgetPathId": "baseline", "units": 3},
            ],
            "integrationContractIds": [],
            "available": True,
            "status": "working",
            "rationale": "Der Kernpfad passt rechnerisch in fünf Testeinheiten.",
            "risk": "Die Rechnung ist noch nicht pilotiert.",
        }

    def validate_variants(
        self,
        variants=None,
        module_contracts=None,
        integration_contracts=None,
    ):
        return validate_annual_variants(
            [self.annual_variant()] if variants is None else variants,
            self.module_contracts() if module_contracts is None else module_contracts,
            {} if integration_contracts is None else integration_contracts,
        )

    @staticmethod
    def integration_contract(status="working"):
        return {
            "id": "INT-TEST",
            "moduleIds": ["MODULE-A", "MODULE-B"],
            "pathIds": ["baseline"],
            "countedInModuleId": "MODULE-B",
            "status": status,
        }

    def integration_aware_inputs(self, *, integration_status="working"):
        module_contracts = self.module_contracts()
        module_contracts["MODULE-B"]["pathBudgets"][0]["sharedAllocations"] = [
            {"integrationContractId": "INT-TEST", "minutes": 45}
        ]
        integration = self.integration_contract(status=integration_status)
        return module_contracts, {"INT-TEST": integration}

    def override_variant(self):
        variant = self.annual_variant()
        variant.update(
            {
                "id": "GRADE-5-OVERRIDE-TEST",
                "pathId": "regular",
                "targetUnits": 6,
                "allocations": [
                    {
                        "moduleId": "MODULE-A",
                        "budgetPathId": "regular",
                        "units": 3,
                    },
                    {
                        "moduleId": "MODULE-B",
                        "budgetPathId": "baseline",
                        "units": 3,
                    },
                ],
                "integrationContractIds": ["INT-TEST"],
            }
        )
        return variant

    def validate_with_module_b_baseline_override(
        self,
        *,
        module_contracts,
        integration_contracts,
    ):
        variant = self.override_variant()
        overrides = ium10_validator.ANNUAL_VARIANT_BUDGET_PATH_OVERRIDES
        overrides[variant["id"]] = {"MODULE-B": "baseline"}
        try:
            return self.validate_variants(
                variants=[variant],
                module_contracts=module_contracts,
                integration_contracts=integration_contracts,
            )
        finally:
            del overrides[variant["id"]]

    def test_returns_annual_variants_keyed_by_unique_id(self):
        result = self.validate_variants()

        self.assertEqual(result, {"GRADE-5-TEST": self.annual_variant()})

    def test_rejects_unknown_modules_paths_allocation_units_or_target_sum(self):
        mutations = (
            ("allocations.0.moduleId", "MODULE-MISSING"),
            ("allocations.0.budgetPathId", "missing"),
            ("allocations.0.units", 3),
            ("targetUnits", 6),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                variant = self.annual_variant()
                current = variant
                for part in field.split(".")[:-1]:
                    current = current[int(part)] if part.isdigit() else current[part]
                current[field.split(".")[-1]] = value
                with self.assertRaises(IUM10ValidationError):
                    self.validate_variants(variants=[variant])

    def test_rejects_unknown_top_level_planning_path(self):
        variant = self.annual_variant()
        variant["pathId"] = "missing"

        with self.assertRaisesRegex(IUM10ValidationError, "planning path"):
            self.validate_variants(variants=[variant])

    def test_rejects_same_sized_foreign_budget_path_for_planning_variant(self):
        variant = self.annual_variant()
        variant["pathId"] = "regular"
        variant["targetUnits"] = 6
        variant["allocations"] = [
            {"moduleId": "MODULE-A", "budgetPathId": "extended", "units": 3},
            {"moduleId": "MODULE-B", "budgetPathId": "regular", "units": 3},
        ]

        with self.assertRaisesRegex(IUM10ValidationError, "variant path"):
            self.validate_variants(variants=[variant])

    def test_rejects_same_sized_optimized_budgets_for_robust_demand_scenario(self):
        module_contracts = {
            module_id: {
                "moduleId": module_id,
                "grade": 7,
                "kind": "core",
                "pathBudgets": [
                    {"pathId": "optimized", "units": units},
                    {"pathId": "robust", "units": units},
                ],
            }
            for module_id, units in (("MODULE-A", 2), ("MODULE-B", 3))
        }
        variant = {
            "id": "GRADE-7-ROBUST-TEST",
            "grade": 7,
            "kind": "demand-scenario",
            "pathId": "robust",
            "targetUnits": 5,
            "allocations": [
                {"moduleId": "MODULE-A", "budgetPathId": "optimized", "units": 2},
                {"moduleId": "MODULE-B", "budgetPathId": "optimized", "units": 3},
            ],
            "integrationContractIds": [],
            "available": False,
            "status": "working",
            "rationale": "Das robuste Testszenario weist fünf Einheiten aus.",
            "risk": "Das Testszenario ist kein verfügbarer Jahrespfad.",
        }

        with self.assertRaisesRegex(IUM10ValidationError, "variant path"):
            self.validate_variants(
                variants=[variant],
                module_contracts=module_contracts,
            )

    def test_rejects_missing_or_unexpected_fields_fail_closed(self):
        missing = self.annual_variant()
        missing.pop("available")
        unexpected = self.annual_variant()
        unexpected["note"] = "Nicht Teil des Vertrags."

        for variant in (missing, unexpected):
            with self.subTest(fields=set(variant)):
                with self.assertRaisesRegex(IUM10ValidationError, "fields"):
                    self.validate_variants(variants=[variant])

    def test_rejects_boolean_values_as_units_or_availability(self):
        mutations = (
            ("targetUnits", True),
            ("allocations.0.units", True),
            ("available", 1),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                variant = self.annual_variant()
                current = variant
                for part in field.split(".")[:-1]:
                    current = current[int(part)] if part.isdigit() else current[part]
                current[field.split(".")[-1]] = value
                with self.assertRaises(IUM10ValidationError):
                    self.validate_variants(variants=[variant])

    def test_rejects_omitted_integration_used_by_selected_budget(self):
        module_contracts, integrations = self.integration_aware_inputs()
        variant = self.annual_variant()

        with self.assertRaisesRegex(IUM10ValidationError, "required integrations"):
            self.validate_variants(
                variants=[variant],
                module_contracts=module_contracts,
                integration_contracts=integrations,
            )

    def test_rejects_failed_integration_while_variant_remains_available(self):
        module_contracts, integrations = self.integration_aware_inputs(
            integration_status="failed"
        )
        variant = self.annual_variant()
        variant["integrationContractIds"] = ["INT-TEST"]

        with self.assertRaisesRegex(IUM10ValidationError, "failed integration"):
            self.validate_variants(
                variants=[variant],
                module_contracts=module_contracts,
                integration_contracts=integrations,
            )

    def test_rejects_declared_integration_not_used_by_selected_budgets(self):
        integration = self.integration_contract()
        variant = self.annual_variant()
        variant["integrationContractIds"] = ["INT-TEST"]

        with self.assertRaisesRegex(IUM10ValidationError, "required integrations"):
            self.validate_variants(
                variants=[variant],
                integration_contracts={"INT-TEST": integration},
            )

    def test_rejects_override_when_participant_path_is_unsupported_by_integration(self):
        module_contracts, integrations = self.integration_aware_inputs()

        with self.assertRaisesRegex(
            IUM10ValidationError,
            "participant budget path",
        ):
            self.validate_with_module_b_baseline_override(
                module_contracts=module_contracts,
                integration_contracts=integrations,
            )

    def test_accepts_override_when_all_participant_paths_support_integration(self):
        module_contracts, integrations = self.integration_aware_inputs()
        integrations["INT-TEST"]["pathIds"] = ["baseline", "regular"]

        result = self.validate_with_module_b_baseline_override(
            module_contracts=module_contracts,
            integration_contracts=integrations,
        )

        self.assertEqual(set(result), {"GRADE-5-OVERRIDE-TEST"})


class IUM10PrivacyContractTests(unittest.TestCase):
    MODULE_ID = "IUM-5-CORE-07"
    CONTRACT_ID = "PC-IUM-5-CORE-07"

    @classmethod
    def module_contracts(cls):
        return {
            cls.MODULE_ID: {
                "moduleId": cls.MODULE_ID,
                "status": "working",
            }
        }

    @classmethod
    def privacy_contract(cls):
        return {
            "id": cls.CONTRACT_ID,
            "moduleId": cls.MODULE_ID,
            "scope": "private-local-reflection",
            "artifactOwner": "learner",
            "artifactCustody": "learner-controlled",
            "institutionalHandling": {
                "access": "prohibited",
                "observation": "prohibited",
                "collection": "prohibited",
                "transfer": "prohibited",
                "storage": "prohibited",
                "assessment": "prohibited",
            },
            "status": "working",
        }

    def test_accepts_the_exact_module_privacy_contract(self):
        result = validate_privacy_contracts(
            [self.privacy_contract()],
            self.module_contracts(),
        )

        self.assertEqual(set(result), {self.CONTRACT_ID})
        self.assertEqual(result[self.CONTRACT_ID]["moduleId"], self.MODULE_ID)

    def test_rejects_each_missing_or_extra_top_level_field(self):
        for field in tuple(self.privacy_contract()):
            with self.subTest(missing=field):
                contract = self.privacy_contract()
                del contract[field]
                module_reference = (
                    self.MODULE_ID
                    if field != "moduleId"
                    else "<missing moduleId>"
                )
                with self.assertRaisesRegex(
                    IUM10ValidationError,
                    f"{module_reference}.*missing.*{field}",
                ):
                    validate_privacy_contracts(
                        [contract],
                        self.module_contracts(),
                    )

        contract = self.privacy_contract()
        contract["note"] = "x"
        with self.assertRaisesRegex(
            IUM10ValidationError,
            f"{self.MODULE_ID}.*unexpected.*note",
        ):
            validate_privacy_contracts([contract], self.module_contracts())

    def test_rejects_each_invalid_or_empty_top_level_value(self):
        mutations = (
            ("wrong id", lambda c: c.__setitem__("id", "PC-WRONG"), "id"),
            ("wrong scope", lambda c: c.__setitem__("scope", "shared"), "scope"),
            ("wrong owner", lambda c: c.__setitem__("artifactOwner", "teacher"), "artifactOwner"),
            ("wrong custody", lambda c: c.__setitem__("artifactCustody", "institution"), "artifactCustody"),
            ("boolean status", lambda c: c.__setitem__("status", True), "status"),
            ("wrong status", lambda c: c.__setitem__("status", "accepted"), "status"),
        )
        for label, mutate, message in mutations:
            with self.subTest(label=label):
                contract = self.privacy_contract()
                mutate(contract)
                with self.assertRaisesRegex(IUM10ValidationError, message):
                    validate_privacy_contracts([contract], self.module_contracts())

        for field in (
            "id",
            "moduleId",
            "scope",
            "artifactOwner",
            "artifactCustody",
            "status",
        ):
            with self.subTest(empty=field):
                contract = self.privacy_contract()
                contract[field] = ""
                with self.assertRaises(IUM10ValidationError):
                    validate_privacy_contracts(
                        [contract],
                        self.module_contracts(),
                    )

    def test_rejects_every_nonprohibited_institutional_handling_value(self):
        for field in (
            "access",
            "observation",
            "collection",
            "transfer",
            "storage",
            "assessment",
        ):
            with self.subTest(field=field):
                contract = self.privacy_contract()
                contract["institutionalHandling"][field] = "allowed"
                with self.assertRaisesRegex(
                    IUM10ValidationError,
                    f"{self.MODULE_ID}.*{field}",
                ):
                    validate_privacy_contracts([contract], self.module_contracts())

    def test_rejects_each_missing_or_extra_handling_field(self):
        extra = self.privacy_contract()
        extra["institutionalHandling"]["profiling"] = "prohibited"
        with self.assertRaisesRegex(IUM10ValidationError, "institutionalHandling"):
            validate_privacy_contracts([extra], self.module_contracts())

        for field in tuple(
            self.privacy_contract()["institutionalHandling"]
        ):
            with self.subTest(missing=field):
                contract = self.privacy_contract()
                del contract["institutionalHandling"][field]
                with self.assertRaisesRegex(
                    IUM10ValidationError,
                    "institutionalHandling",
                ):
                    validate_privacy_contracts(
                        [contract],
                        self.module_contracts(),
                    )

    def test_rejects_duplicates_and_orphans(self):
        duplicate = copy.deepcopy(self.privacy_contract())
        orphan = self.privacy_contract()
        orphan["id"] = "PC-IUM-5-CORE-99"
        orphan["moduleId"] = "IUM-5-CORE-99"

        cases = (
            (
                "duplicate",
                [self.privacy_contract(), duplicate],
                self.module_contracts(),
                "unique",
            ),
            ("orphan", [orphan], self.module_contracts(), "unknown module"),
        )
        for label, contracts, modules, message in cases:
            with self.subTest(label=label):
                with self.assertRaisesRegex(IUM10ValidationError, message):
                    validate_privacy_contracts(contracts, modules)


class IUM10TimeReviewTests(unittest.TestCase):
    VARIANT_ID = "GRADE-TEST-BASELINE"
    INTEGRATION_ID = "INT-TEST-TIME-REVIEW"
    REVIEW_REQUIRED_IDS = (
        "BMB16-GYM-IK-GM-001",
        "BMB16-GYM-IK-GM-002",
        "BMB16-GYM-IK-GM-003",
        "BMB16-GYM-IK-KK-002",
    )

    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        cls.remediation_payload = json.loads(
            (root / "roadmap/coverage-remediation.json").read_text(
                encoding="utf-8"
            )
        )
        cls.module_payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(
                encoding="utf-8"
            )
        )
        cls.coverage_payload = json.loads(
            (root / "roadmap/coverage-plan.json").read_text(
                encoding="utf-8"
            )
        )
        cls.bmb_payload = json.loads(
            (
                root
                / "curriculum/basiskurs-medienbildung/competencies.json"
            ).read_text(encoding="utf-8")
        )
        cls.lesehilfe_payload = json.loads(
            (
                root
                / "curriculum/lesehilfe-2026-27/competencies.json"
            ).read_text(encoding="utf-8")
        )
        cls.time_payload = json.loads(
            (root / "roadmap/time-model.json").read_text(encoding="utf-8")
        )
        cls.handoffs_by_id = {
            entry["competencyId"]: entry
            for entry in cls.remediation_payload["entries"]
        }
        cls.repository_module_contracts = validate_module_contracts(
            cls.time_payload["moduleContracts"],
            cls.module_payload,
        )
        cls.repository_integration_contracts = validate_integration_contracts(
            cls.time_payload["integrationContracts"],
            cls.repository_module_contracts,
        )
        cls.repository_annual_variants = validate_annual_variants(
            cls.time_payload["annualVariants"],
            cls.repository_module_contracts,
            cls.repository_integration_contracts,
        )
        cls.repository_privacy_contracts = validate_privacy_contracts(
            cls.time_payload["privacyContracts"],
            cls.repository_module_contracts,
        )

    def test_repository_core07_private_local_dispositions_match_the_audited_matrix(self):
        expected = {
            "BMB16-GYM-IK-MG-001": (
                "nonpersonal-follow-up",
                "CE-IUM-5-CORE-07-BMB16-GYM-IK-MG-001",
            ),
            "BMB16-GYM-IK-MG-002": (
                "nonpersonal-module-detail",
                "CE-IUM-5-CORE-07-BMB16-GYM-IK-MG-002",
            ),
            "BMB16-GYM-IK-MG-003": (
                "nonpersonal-follow-up",
                "CE-IUM-5-CORE-07-BMB16-GYM-IK-MG-003",
            ),
            "BMB16-GYM-PK-RK-001": (
                "nonpersonal-follow-up",
                "CE-IUM-5-CORE-07-BMB16-GYM-PK-RK-001",
            ),
            "BMB16-GYM-PK-RK-002": (
                "nonpersonal-follow-up",
                "CE-IUM-5-CORE-07-BMB16-GYM-PK-RK-002",
            ),
            "BMB16-GYM-PK-RK-003": ("none", None),
            "LH26-E-DP-003": ("none", None),
        }
        reviews = [
            review
            for review in self.time_payload["timeReviews"]
            if review["moduleId"] == "IUM-5-CORE-07"
        ]
        self.assertEqual(len(reviews), 7)
        for review in reviews:
            with self.subTest(competency_id=review["competencyId"]):
                disposition = review["privacyDisposition"]
                self.assertEqual(
                    disposition["contractId"],
                    "PC-IUM-5-CORE-07",
                )
                self.assertEqual(
                    (
                        disposition["observableBasis"],
                        disposition["evidenceContractId"],
                    ),
                    expected[review["competencyId"]],
                )
                self.assertEqual(
                    set(
                        disposition[
                            "privateArtifactContribution"
                        ].values()
                    ),
                    {"excluded"},
                )
                self.assertEqual(
                    disposition["privateActivityTimeTreatment"],
                    "module-budget-only",
                )

    def test_repository_structured_dispositions_preserve_time_and_coverage_balance(self):
        reviews = [
            review
            for review in self.time_payload["timeReviews"]
            if review["moduleId"] == "IUM-5-CORE-07"
        ]
        self.assertEqual(len(reviews), 7)
        self.assertEqual(
            sum(
                review["additionalMinutes"]
                for review in reviews
                if review["additionalMinutes"] > 0
            ),
            65,
        )
        self.assertEqual(
            {
                review["competencyId"]
                for review in reviews
                if review["decision"] == "unresolved"
            },
            {"BMB16-GYM-PK-RK-003", "LH26-E-DP-003"},
        )
        self.assertEqual(
            {
                review["privacyDisposition"]["observableBasis"]
                for review in reviews
            },
            {
                "nonpersonal-follow-up",
                "nonpersonal-module-detail",
                "none",
            },
        )
        self.assertEqual(
            sum(
                review["privacyDisposition"]["observableBasis"]
                == "nonpersonal-follow-up"
                for review in reviews
            ),
            4,
        )
        self.assertEqual(
            sum(
                review["privacyDisposition"]["observableBasis"]
                == "nonpersonal-module-detail"
                for review in reviews
            ),
            1,
        )
        self.assertEqual(
            sum(
                review["privacyDisposition"]["observableBasis"] == "none"
                for review in reviews
            ),
            2,
        )

    def test_repository_core07_rejects_each_private_contribution_mutation(self):
        fields = ("product", "evidence", "additionalTimeClaim")
        for field in fields:
            with self.subTest(field=field):
                time_payload = copy.deepcopy(self.time_payload)
                review = next(
                    review
                    for review in time_payload["timeReviews"]
                    if review["competencyId"] == "BMB16-GYM-IK-MG-001"
                )
                review["privacyDisposition"]["privateArtifactContribution"][field] = (
                    "included"
                )
                privacy_contracts = validate_privacy_contracts(
                    time_payload["privacyContracts"],
                    self.repository_module_contracts,
                )
                with self.assertRaisesRegex(IUM10ValidationError, field):
                    validate_time_reviews(
                        time_payload["timeReviews"],
                        self.remediation_payload,
                        self.repository_module_contracts,
                        self.repository_integration_contracts,
                        self.repository_annual_variants,
                        privacy_contracts=privacy_contracts,
                    )

    @classmethod
    def module_contracts(cls):
        module_ids = {
            entry["before"]["evidenceModuleId"]
            for entry in cls.remediation_payload["entries"]
        }
        return {
            module_id: {
                "moduleId": module_id,
                "centralLearningProduct": (
                    f"Eine überprüfbare Produktspur für {module_id}."
                ),
                "pathBudgets": [
                    {
                        "pathId": "baseline",
                        "minutes": 90,
                        "sharedAllocations": (
                            [
                                {
                                    "integrationContractId": cls.INTEGRATION_ID,
                                    "minutes": 45,
                                }
                            ]
                            if module_id == "IUM-5-CORE-03"
                            else []
                        ),
                        "phaseBudgets": [
                            {
                                "phaseId": "guided-practice",
                                "minutes": 45,
                            },
                            {
                                "phaseId": "independent-action-product",
                                "minutes": 45,
                            },
                        ],
                    }
                ],
            }
            for module_id in module_ids
        }

    @classmethod
    def integration_contracts(cls):
        return {
            cls.INTEGRATION_ID: {
                "id": cls.INTEGRATION_ID,
                "moduleIds": ["IUM-5-CORE-01", "IUM-5-CORE-03"],
                "pathIds": ["baseline"],
                "countedInModuleId": "IUM-5-CORE-03",
                "sharedMinutes": 45,
                "status": "working",
            }
        }

    @classmethod
    def annual_variants(cls):
        return {
            cls.VARIANT_ID: {
                "id": cls.VARIANT_ID,
                "allocations": [
                    {
                        "moduleId": module_id,
                        "budgetPathId": "baseline",
                        "units": 1,
                    }
                    for module_id in sorted(cls.module_contracts())
                ],
                "available": True,
                "integrationContractIds": [cls.INTEGRATION_ID],
            }
        }

    @classmethod
    def review(cls, competency_id, decision):
        handoff = cls.handoffs_by_id[competency_id]
        review = {
            "id": f"TR-{competency_id}",
            "competencyId": competency_id,
            "moduleId": handoff["before"]["evidenceModuleId"],
            "sourceTimeImpactLevel": handoff["timeImpact"]["level"],
            "decision": decision,
            "rationale": "Die Zeitentscheidung ist an der Lernhandlung geprüft.",
            "phaseIds": ["guided-practice"],
            "additionalMinutes": 0,
            "integrationContractIds": [],
            "sequenceEvidenceId": None,
            "pathAvailability": [cls.VARIANT_ID],
            "coverageConsequence": "semantic-status-unchanged",
            "risk": "Die Zeitannahme muss im Modulbetrieb pilotiert werden.",
            "followUp": "Die tatsächlichen Modulminuten aggregiert prüfen.",
            "status": "working",
        }
        if decision == "integrated":
            review["integrationContractIds"] = [cls.INTEGRATION_ID]
        elif decision == "additional-time":
            review["additionalMinutes"] = 15
        elif decision == "unresolved":
            review["phaseIds"] = []
            review["pathAvailability"] = []
        if handoff["timeImpact"]["level"] == "roadmap-dependent":
            review["phaseIds"] = []
            review["additionalMinutes"] = 0
            review["integrationContractIds"] = []
            review["sequenceEvidenceId"] = f"SE-{competency_id}"
            review["pathAvailability"] = []
        return review

    def validate_reviews(
        self,
        reviews,
        *,
        remediation_payload=None,
        module_contracts=None,
        integration_contracts=None,
        annual_variants=None,
        require_complete=False,
        privacy_contracts=None,
    ):
        return validate_time_reviews(
            reviews,
            self.remediation_payload
            if remediation_payload is None
            else remediation_payload,
            self.module_contracts()
            if module_contracts is None
            else module_contracts,
            self.integration_contracts()
            if integration_contracts is None
            else integration_contracts,
            self.annual_variants()
            if annual_variants is None
            else annual_variants,
            require_complete,
            privacy_contracts=privacy_contracts,
        )

    @classmethod
    def core07_privacy_contracts(cls):
        return validate_privacy_contracts(
            [IUM10PrivacyContractTests.privacy_contract()],
            cls.module_contracts(),
        )

    @staticmethod
    def private_disposition(
        competency_id,
        observable_basis,
        module_id="IUM-5-CORE-07",
    ):
        return {
            "contractId": f"PC-{module_id}",
            "observableBasis": observable_basis,
            "evidenceContractId": (
                None
                if observable_basis == "none"
                else f"CE-{module_id}-{competency_id}"
            ),
            "privateArtifactContribution": {
                "product": "excluded",
                "evidence": "excluded",
                "additionalTimeClaim": "excluded",
            },
            "privateActivityTimeTreatment": "module-budget-only",
        }

    def test_accepts_private_local_review_with_nonpersonal_follow_up(self):
        competency_id = "BMB16-GYM-IK-MG-001"
        review = self.review(competency_id, "additional-time")
        review["privacyDisposition"] = self.private_disposition(
            competency_id,
            "nonpersonal-follow-up",
        )

        result = self.validate_reviews(
            [review],
            privacy_contracts=self.core07_privacy_contracts(),
        )

        self.assertEqual(set(result), {f"TR-{competency_id}"})

    def test_rejects_private_local_review_without_module_contract(self):
        review = self.review("BMB16-GYM-IK-MG-001", "additional-time")
        with self.assertRaisesRegex(IUM10ValidationError, "private-local.*privacy"):
            self.validate_reviews([review], privacy_contracts={})

    def test_rejects_protected_module_review_without_disposition(self):
        review = self.review("BMB16-GYM-IK-MG-001", "additional-time")
        with self.assertRaisesRegex(IUM10ValidationError, "privacyDisposition"):
            self.validate_reviews(
                [review],
                privacy_contracts=self.core07_privacy_contracts(),
            )

    def test_rejects_orphan_disposition_on_unprotected_module(self):
        review = self.review("BMB16-GYM-IK-GM-001", "additional-time")
        review["privacyDisposition"] = self.private_disposition(
            "BMB16-GYM-IK-GM-001",
            "nonpersonal-follow-up",
        )
        with self.assertRaisesRegex(IUM10ValidationError, "orphan"):
            self.validate_reviews([review], privacy_contracts={})

    def test_rejects_private_disposition_reference_and_basis_drift(self):
        competency_id = "BMB16-GYM-IK-MG-001"
        mutations = (
            ("contract", ("contractId",), "PC-WRONG", "contractId"),
            (
                "basis",
                ("observableBasis",),
                "nonpersonal-module-detail",
                "observableBasis",
            ),
            (
                "unknown basis",
                ("observableBasis",),
                "personal-artifact",
                "observableBasis",
            ),
            (
                "evidence",
                ("evidenceContractId",),
                "CE-WRONG",
                "evidenceContractId",
            ),
            (
                "time treatment",
                ("privateActivityTimeTreatment",),
                "record-minutes",
                "module-budget-only",
            ),
            (
                "product",
                ("privateArtifactContribution", "product"),
                "included",
                "product",
            ),
            (
                "evidence contribution",
                ("privateArtifactContribution", "evidence"),
                "included",
                "evidence",
            ),
            (
                "time contribution",
                ("privateArtifactContribution", "additionalTimeClaim"),
                "included",
                "additionalTimeClaim",
            ),
        )
        for label, path, value, message in mutations:
            with self.subTest(label=label):
                review = self.review(competency_id, "additional-time")
                disposition = self.private_disposition(
                    competency_id,
                    "nonpersonal-follow-up",
                )
                target = disposition
                for key in path[:-1]:
                    target = target[key]
                target[path[-1]] = value
                review["privacyDisposition"] = disposition
                with self.assertRaisesRegex(IUM10ValidationError, message):
                    self.validate_reviews(
                        [review],
                        privacy_contracts=self.core07_privacy_contracts(),
                    )

    def test_task22_accepts_none_basis_with_exact_roadmap_sequence_reference(self):
        competency_id = "LH26-E-PROG-003"
        review = self.review(competency_id, "unresolved")
        review["privacyDisposition"] = self.private_disposition(
            competency_id, "none", "IUM-7-CORE-08"
        )
        privacy_contracts = validate_privacy_contracts(
            [TASK22_PRIVACY_CONTRACT],
            self.module_contracts(),
        )

        result = self.validate_reviews(
            [review],
            privacy_contracts=privacy_contracts,
        )

        self.assertEqual(set(result), {f"TR-{competency_id}"})

    def test_task22_none_basis_keeps_nonroadmap_and_allocated_reviews_closed(self):
        competency_id = "LH26-E-PROG-003"
        privacy_contracts = validate_privacy_contracts(
            [TASK22_PRIVACY_CONTRACT],
            self.module_contracts(),
        )
        mutations = (
            ("non-roadmap level", "sourceTimeImpactLevel", "review-required"),
            ("positive minutes", "additionalMinutes", 15),
            ("phase", "phaseIds", ["guided-practice"]),
            ("path", "pathAvailability", [self.VARIANT_ID]),
            ("integration", "integrationContractIds", [self.INTEGRATION_ID]),
            ("wrong sequence", "sequenceEvidenceId", "SE-WRONG"),
            ("missing sequence", "sequenceEvidenceId", None),
        )
        for label, field, value in mutations:
            with self.subTest(label=label):
                review = self.review(competency_id, "unresolved")
                review["privacyDisposition"] = self.private_disposition(
                    competency_id, "none", "IUM-7-CORE-08"
                )
                review[field] = value
                with self.assertRaises(IUM10ValidationError):
                    self.validate_reviews(
                        [review],
                        privacy_contracts=privacy_contracts,
                    )

    def test_rejects_non_string_observable_basis_as_validation_error(self):
        competency_id = "BMB16-GYM-IK-MG-001"
        review = self.review(competency_id, "additional-time")
        review["privacyDisposition"] = self.private_disposition(
            competency_id,
            "nonpersonal-follow-up",
        )
        review["privacyDisposition"]["observableBasis"] = []

        with self.assertRaisesRegex(
            IUM10ValidationError,
            f"observableBasis.*{competency_id}",
        ):
            self.validate_reviews(
                [review],
                privacy_contracts=self.core07_privacy_contracts(),
            )

    def test_rejects_each_missing_or_extra_disposition_field(self):
        competency_id = "BMB16-GYM-IK-MG-001"
        disposition = self.private_disposition(
            competency_id,
            "nonpersonal-follow-up",
        )
        cases = []
        for field in tuple(disposition):
            mutated = copy.deepcopy(disposition)
            del mutated[field]
            cases.append((f"missing {field}", mutated, "privacyDisposition"))
        extra = copy.deepcopy(disposition)
        extra["note"] = "x"
        cases.append(("extra disposition", extra, "privacyDisposition"))

        for field in tuple(disposition["privateArtifactContribution"]):
            mutated = copy.deepcopy(disposition)
            del mutated["privateArtifactContribution"][field]
            cases.append(
                (f"missing contribution {field}", mutated, "privateArtifactContribution")
            )
        extra_contribution = copy.deepcopy(disposition)
        extra_contribution["privateArtifactContribution"]["note"] = "x"
        cases.append(
            (
                "extra contribution",
                extra_contribution,
                "privateArtifactContribution",
            )
        )

        for label, mutated, message in cases:
            with self.subTest(label=label):
                review = self.review(competency_id, "additional-time")
                review["privacyDisposition"] = mutated
                with self.assertRaisesRegex(IUM10ValidationError, message):
                    self.validate_reviews(
                        [review],
                        privacy_contracts=self.core07_privacy_contracts(),
                    )

    def test_rejects_cross_module_privacy_contract_reference(self):
        competency_id = "BMB16-GYM-IK-MG-001"
        core07 = IUM10PrivacyContractTests.privacy_contract()
        other = IUM10PrivacyContractTests.privacy_contract()
        other["id"] = "PC-IUM-5-CORE-01"
        other["moduleId"] = "IUM-5-CORE-01"
        privacy_contracts = validate_privacy_contracts(
            [core07, other],
            self.module_contracts(),
        )
        review = self.review(competency_id, "additional-time")
        review["privacyDisposition"] = self.private_disposition(
            competency_id,
            "nonpersonal-follow-up",
        )
        review["privacyDisposition"]["contractId"] = other["id"]

        with self.assertRaisesRegex(IUM10ValidationError, "contractId"):
            self.validate_reviews(
                [review],
                privacy_contracts=privacy_contracts,
            )

    def test_accepts_module_detail_and_unresolved_privacy_dispositions(self):
        module_detail_id = "BMB16-GYM-IK-MG-002"
        unresolved_id = "BMB16-GYM-PK-RK-003"
        module_detail = self.review(module_detail_id, "additional-time")
        module_detail["privacyDisposition"] = self.private_disposition(
            module_detail_id,
            "nonpersonal-module-detail",
        )
        unresolved = self.review(unresolved_id, "unresolved")
        unresolved["privacyDisposition"] = self.private_disposition(
            unresolved_id,
            "none",
        )

        result = self.validate_reviews(
            [module_detail, unresolved],
            privacy_contracts=self.core07_privacy_contracts(),
        )

        self.assertEqual(
            set(result),
            {f"TR-{module_detail_id}", f"TR-{unresolved_id}"},
        )

    def test_rejects_none_with_evidence_phase_path_integration_sequence_or_minutes(self):
        competency_id = "BMB16-GYM-PK-RK-003"
        mutations = (
            ("evidence", ("privacyDisposition", "evidenceContractId"), "CE-WRONG"),
            ("phase", ("phaseIds",), ["guided-practice"]),
            ("path", ("pathAvailability",), [self.VARIANT_ID]),
            ("integration", ("integrationContractIds",), [self.INTEGRATION_ID]),
            ("sequence", ("sequenceEvidenceId",), "SE-WRONG"),
            ("minutes", ("additionalMinutes",), 15),
        )
        for label, path, value in mutations:
            with self.subTest(label=label):
                review = self.review(competency_id, "unresolved")
                review["privacyDisposition"] = self.private_disposition(
                    competency_id,
                    "none",
                )
                target = review
                for key in path[:-1]:
                    target = target[key]
                target[path[-1]] = value
                with self.assertRaises(IUM10ValidationError):
                    self.validate_reviews(
                        [review],
                        privacy_contracts=self.core07_privacy_contracts(),
                    )

    def test_accepts_hand_built_absorbed_integrated_additional_and_unresolved_reviews(self):
        decisions = ("absorbed", "integrated", "additional-time", "unresolved")
        reviews = [
            self.review(competency_id, decision)
            for competency_id, decision in zip(
                self.REVIEW_REQUIRED_IDS,
                decisions,
            )
        ]

        result = self.validate_reviews(reviews)

        self.assertEqual(
            set(result),
            {f"TR-{competency_id}" for competency_id in self.REVIEW_REQUIRED_IDS},
        )
        self.assertEqual(
            result["TR-BMB16-GYM-IK-GM-003"]["additionalMinutes"],
            15,
        )
        self.assertEqual(
            result["TR-BMB16-GYM-IK-GM-002"]["integrationContractIds"],
            [self.INTEGRATION_ID],
        )

    def test_rejects_duplicate_review_id_wrong_module_or_wrong_source_level(self):
        first = self.review(self.REVIEW_REQUIRED_IDS[0], "absorbed")
        second = self.review(self.REVIEW_REQUIRED_IDS[1], "absorbed")
        second["id"] = first["id"]
        with self.assertRaises(IUM10ValidationError):
            self.validate_reviews([first, second])

        mutations = (
            ("moduleId", "IUM-5-CORE-99"),
            ("sourceTimeImpactLevel", "roadmap-dependent"),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                review = self.review(self.REVIEW_REQUIRED_IDS[0], "absorbed")
                review[field] = value
                with self.assertRaises(IUM10ValidationError):
                    self.validate_reviews([review])

    def test_rejects_unknown_phase_integration_or_annual_variant(self):
        mutations = (
            ("phaseIds", ["unknown-phase"]),
            ("integrationContractIds", ["INT-UNKNOWN"]),
            ("pathAvailability", ["GRADE-UNKNOWN"]),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                review = self.review(self.REVIEW_REQUIRED_IDS[0], "absorbed")
                review[field] = value
                with self.assertRaises(IUM10ValidationError):
                    self.validate_reviews([review])

    def test_enforces_each_decision_minute_path_risk_and_product_contract(self):
        mutations = (
            ("absorbed with additional time", "absorbed", "additionalMinutes", 1),
            (
                "integrated without time or integration",
                "integrated",
                "integrationContractIds",
                [],
            ),
            ("additional time with zero minutes", "additional-time", "additionalMinutes", 0),
            ("unresolved with an available path", "unresolved", "pathAvailability", [self.VARIANT_ID]),
            ("unresolved with empty risk", "unresolved", "risk", ""),
            ("unresolved with empty follow-up", "unresolved", "followUp", ""),
        )
        for label, decision, field, value in mutations:
            with self.subTest(label=label):
                review = self.review(self.REVIEW_REQUIRED_IDS[0], decision)
                review[field] = value
                with self.assertRaises(IUM10ValidationError):
                    self.validate_reviews([review])

        review = self.review(self.REVIEW_REQUIRED_IDS[0], "absorbed")
        module_contracts = self.module_contracts()
        module_contracts[review["moduleId"]]["centralLearningProduct"] = ""
        with self.assertRaises(IUM10ValidationError):
            self.validate_reviews(
                [review],
                module_contracts=module_contracts,
            )

    def test_roadmap_dependent_review_uses_sequence_evidence_not_a_single_phase(self):
        competency_id = "LH26-E-PROG-001"
        review = self.review(competency_id, "unresolved")

        result = self.validate_reviews([review])

        self.assertEqual(
            result[f"TR-{competency_id}"]["sequenceEvidenceId"],
            f"SE-{competency_id}",
        )
        self.assertEqual(result[f"TR-{competency_id}"]["phaseIds"], [])

        mutations = (
            ("single phase evidence", "phaseIds", ["guided-practice"]),
            ("missing sequence evidence", "sequenceEvidenceId", None),
            ("wrong sequence evidence", "sequenceEvidenceId", "SE-OTHER"),
        )
        for label, field, value in mutations:
            with self.subTest(label=label):
                invalid = self.review(competency_id, "unresolved")
                invalid[field] = value
                with self.assertRaises(IUM10ValidationError):
                    self.validate_reviews([invalid])

    def test_additional_minutes_must_be_in_each_available_module_budget(self):
        review = self.review(self.REVIEW_REQUIRED_IDS[0], "additional-time")
        review["additionalMinutes"] = 45
        self.validate_reviews([review])

        review["additionalMinutes"] = 46
        with self.assertRaises(IUM10ValidationError):
            self.validate_reviews([review])

        annual_variants = self.annual_variants()
        annual_variants[self.VARIANT_ID]["allocations"] = [
            allocation
            for allocation in annual_variants[self.VARIANT_ID]["allocations"]
            if allocation["moduleId"] != review["moduleId"]
        ]
        review["additionalMinutes"] = 15
        with self.assertRaises(IUM10ValidationError):
            self.validate_reviews(
                [review],
                annual_variants=annual_variants,
            )

    def test_rejects_cumulative_additional_minutes_above_one_phase_capacity(self):
        first = self.review("BMB16-GYM-IK-GM-001", "additional-time")
        second = self.review("BMB16-GYM-IK-GM-002", "additional-time")
        first["additionalMinutes"] = 45
        second["additionalMinutes"] = 45

        with self.assertRaises(IUM10ValidationError):
            self.validate_reviews([first, second])

    def test_accepts_cumulative_minutes_in_distinct_phase_capacities(self):
        guided = self.review("BMB16-GYM-IK-GM-001", "additional-time")
        product = self.review("BMB16-GYM-IK-GM-002", "additional-time")
        guided["additionalMinutes"] = 45
        product["additionalMinutes"] = 45
        product["phaseIds"] = ["independent-action-product"]

        result = self.validate_reviews([guided, product])

        self.assertEqual(result, {guided["id"]: guided, product["id"]: product})

    def test_aggregates_each_overlapping_path_availability_list(self):
        annual_variants = self.annual_variants()
        second_variant = copy.deepcopy(annual_variants[self.VARIANT_ID])
        second_variant["id"] = "GRADE-TEST-SECOND"
        annual_variants[second_variant["id"]] = second_variant
        first = self.review("BMB16-GYM-IK-GM-001", "additional-time")
        second = self.review("BMB16-GYM-IK-GM-002", "additional-time")
        first["additionalMinutes"] = 30
        second["additionalMinutes"] = 30
        first["pathAvailability"] = [self.VARIANT_ID, second_variant["id"]]
        second["pathAvailability"] = [second_variant["id"]]

        with self.assertRaises(IUM10ValidationError):
            self.validate_reviews(
                [first, second],
                annual_variants=annual_variants,
            )

    def test_coverage_consequence_cannot_preempt_semantic_status(self):
        review = self.review("BMB16-GYM-IK-GM-001", "absorbed")

        result = self.validate_reviews([review])

        self.assertEqual(
            result[review["id"]]["coverageConsequence"],
            "semantic-status-unchanged",
        )

        promoted = copy.deepcopy(review)
        promoted["coverageConsequence"] = "promote-to-covered"
        with self.assertRaises(IUM10ValidationError):
            self.validate_reviews([promoted])

    def test_rejects_unrelated_grade_six_variant_for_grade_five_review(self):
        review = self.review("BMB16-GYM-IK-GM-001", "absorbed")
        review["pathAvailability"] = ["GRADE-6-BASELINE"]

        with self.assertRaises(IUM10ValidationError):
            self.validate_reviews(
                [review],
                module_contracts=self.repository_module_contracts,
                integration_contracts=self.repository_integration_contracts,
                annual_variants=self.repository_annual_variants,
            )

    def test_accepts_cross_grade_integration_in_the_later_grade_variant(self):
        review = self.review("LH26-E-ALG-001", "integrated")
        review["phaseIds"] = []
        review["integrationContractIds"] = ["INT-6-ALGORITHM-REVISIT"]
        review["pathAvailability"] = ["GRADE-6-BASELINE"]

        result = self.validate_reviews(
            [review],
            module_contracts=self.repository_module_contracts,
            integration_contracts=self.repository_integration_contracts,
            annual_variants=self.repository_annual_variants,
        )

        self.assertEqual(result, {review["id"]: review})

    def test_rejects_integration_not_used_by_the_named_variant(self):
        review = self.review("LH26-E-ALG-001", "integrated")
        review["phaseIds"] = []
        review["integrationContractIds"] = ["INT-6-ALGORITHM-REVISIT"]
        review["pathAvailability"] = ["GRADE-5-BASELINE"]

        with self.assertRaises(IUM10ValidationError):
            self.validate_reviews(
                [review],
                module_contracts=self.repository_module_contracts,
                integration_contracts=self.repository_integration_contracts,
                annual_variants=self.repository_annual_variants,
            )

    def test_rejects_failed_integration_from_upstream_valid_indexes(self):
        time_payload = copy.deepcopy(self.time_payload)
        for integration in time_payload["integrationContracts"]:
            if integration["id"] == "INT-6-ALGORITHM-REVISIT":
                integration["status"] = "failed"
        module_contracts = validate_module_contracts(
            time_payload["moduleContracts"],
            self.module_payload,
        )
        integration_contracts = validate_integration_contracts(
            time_payload["integrationContracts"],
            module_contracts,
        )
        variant = copy.deepcopy(
            next(
                variant
                for variant in time_payload["annualVariants"]
                if variant["id"] == "GRADE-6-BASELINE"
            )
        )
        variant["available"] = False
        annual_variants = validate_annual_variants(
            [variant],
            module_contracts,
            integration_contracts,
        )
        review = self.review("LH26-E-ALG-001", "integrated")
        review["phaseIds"] = []
        review["integrationContractIds"] = ["INT-6-ALGORITHM-REVISIT"]
        review["pathAvailability"] = ["GRADE-6-BASELINE"]

        with self.assertRaises(IUM10ValidationError):
            self.validate_reviews(
                [review],
                module_contracts=module_contracts,
                integration_contracts=integration_contracts,
                annual_variants=annual_variants,
            )

    def test_rejects_boolean_minutes_and_non_exact_fields(self):
        review = self.review(self.REVIEW_REQUIRED_IDS[0], "additional-time")
        review["additionalMinutes"] = True
        with self.assertRaises(IUM10ValidationError):
            self.validate_reviews([review])

        missing = self.review(self.REVIEW_REQUIRED_IDS[0], "absorbed")
        missing.pop("coverageConsequence")
        unexpected = self.review(self.REVIEW_REQUIRED_IDS[0], "absorbed")
        unexpected["note"] = "Nicht Teil des Vertrags."
        for review in (missing, unexpected):
            with self.subTest(fields=set(review)):
                with self.assertRaises(IUM10ValidationError):
                    self.validate_reviews([review])

    def test_partial_mode_requires_a_unique_subset_of_the_exact_baseline(self):
        review = self.review(self.REVIEW_REQUIRED_IDS[0], "absorbed")
        self.assertEqual(
            self.validate_reviews([review]),
            {review["id"]: review},
        )

        incomplete_baseline = copy.deepcopy(self.remediation_payload)
        incomplete_baseline["entries"].pop()
        with self.assertRaises(IUM10ValidationError):
            self.validate_reviews(
                [review],
                remediation_payload=incomplete_baseline,
            )

        unknown = copy.deepcopy(review)
        unknown["id"] = "TR-COMP-UNKNOWN"
        unknown["competencyId"] = "COMP-UNKNOWN"
        with self.assertRaises(IUM10ValidationError):
            self.validate_reviews([unknown])

    def test_complete_mode_requires_exactly_all_sixty_baseline_ids(self):
        partial = self.review(self.REVIEW_REQUIRED_IDS[0], "absorbed")
        with self.assertRaises(IUM10ValidationError):
            self.validate_reviews([partial], require_complete=True)

        complete_baseline = copy.deepcopy(self.remediation_payload)
        repository_disposed_reviews = {
            review["competencyId"]: review
            for review in self.time_payload["timeReviews"]
            if "privacyDisposition" in review
        }
        reviews = []
        for entry in self.remediation_payload["entries"]:
            decision = (
                "unresolved"
                if entry["timeImpact"]["level"] == "roadmap-dependent"
                else "absorbed"
            )
            repository_disposed_review = repository_disposed_reviews.get(
                entry["competencyId"]
            )
            if (
                repository_disposed_review is not None
                and repository_disposed_review["privacyDisposition"][
                    "observableBasis"
                ]
                == "none"
            ):
                decision = "unresolved"
            review = self.review(entry["competencyId"], decision)
            if repository_disposed_review is not None:
                review["privacyDisposition"] = copy.deepcopy(
                    repository_disposed_review["privacyDisposition"]
                )
            reviews.append(review)

        result = self.validate_reviews(
            reviews,
            remediation_payload=complete_baseline,
            require_complete=True,
            privacy_contracts=self.repository_privacy_contracts,
        )

        self.assertEqual(len(result), 60)
        self.assertEqual(
            {review["competencyId"] for review in result.values()},
            set(self.handoffs_by_id),
        )

    def _assert_id009_repository_contract(
        self,
        reviews_by_competency_id,
        module_contracts,
    ):
        id009_review = reviews_by_competency_id["LH26-E-ID-009"]
        self.assertEqual(
            (
                id009_review["decision"],
                id009_review["additionalMinutes"],
                id009_review["phaseIds"],
                id009_review["integrationContractIds"],
                id009_review["pathAvailability"],
            ),
            (
                "absorbed",
                0,
                [
                    "activate-prior-knowledge",
                    "independent-action-product",
                    "review-revise-transfer",
                ],
                [],
                [
                    "GRADE-5-BASELINE",
                    "GRADE-5-REGULAR",
                    "GRADE-5-EXTENDED",
                ],
            ),
        )
        self.assertEqual(
            module_contracts["IUM-5-CORE-02"]["timeReviewIds"],
            ["TR-LH26-E-ID-009"],
        )
        self.assertEqual(
            id009_review["rationale"],
            EXPECTED_ID009_EXECUTED_DOSSIER_RATIONALE,
        )
        self.assertEqual(
            id009_review["risk"],
            EXPECTED_ID009_INTEGRATION_BOUNDARY_RISK,
        )
        self.assertEqual(
            id009_review["followUp"],
            EXPECTED_ID009_IDENTICAL_TRAIL_FOLLOW_UP,
        )

    def _assert_core03_repository_contract(
        self,
        reviews_by_competency_id,
        module_contracts,
    ):
        core03_contract = module_contracts["IUM-5-CORE-03"]
        self.assertEqual(
            core03_contract["timeReviewIds"],
            [
                f"TR-{competency_id}"
                for competency_id in CORE03_AUDIT_EXPECTATIONS
            ],
        )
        self.assertEqual(
            core03_contract["schoolDependentSteps"],
            ["actual-local-communication-and-collaboration"],
        )
        self.assertEqual(
            core03_contract["centralLearningAction"],
            "Analoge und digitale Situationen vergleichen, Nachrichten "
            "adressatengerecht verfassen, private Daten schützen und "
            "Konfliktfolgen an fiktiven Fällen abwägen.",
        )

        expected_paths = [
            "GRADE-5-BASELINE",
            "GRADE-5-REGULAR",
            "GRADE-5-EXTENDED",
        ]
        for competency_id, expected in CORE03_AUDIT_EXPECTATIONS.items():
            with self.subTest(core03_competency_id=competency_id):
                review = reviews_by_competency_id[competency_id]
                self.assertEqual(
                    {
                        "decision": review["decision"],
                        "additionalMinutes": review["additionalMinutes"],
                        "phaseIds": review["phaseIds"],
                        "rationale": review["rationale"],
                        "risk": review["risk"],
                        "followUp": review["followUp"],
                    },
                    expected,
                )
                self.assertEqual(review["moduleId"], "IUM-5-CORE-03")
                self.assertEqual(
                    review["sourceTimeImpactLevel"],
                    "review-required",
                )
                self.assertEqual(review["integrationContractIds"], [])
                self.assertIsNone(review["sequenceEvidenceId"])
                self.assertEqual(review["pathAvailability"], expected_paths)

        core03_module = next(
            module
            for module in self.module_payload["modules"]
            if module["id"] == "IUM-5-CORE-03"
        )
        evidence_by_competency_id = {
            evidence["competencyId"]: evidence
            for evidence in core03_module["coverageEvidence"]
        }
        self.assertEqual(
            {
                competency_id: (
                    evidence_by_competency_id[competency_id]["mode"],
                    evidence_by_competency_id[competency_id]["executionType"],
                    evidence_by_competency_id[competency_id][
                        "productVisibility"
                    ],
                )
                for competency_id in (
                    "BMB16-GYM-IK-KK-002",
                    "BMB16-GYM-IK-KK-003",
                    "BMB16-GYM-PK-HK-003",
                    "LH26-E-KS-001",
                )
            },
            {
                "BMB16-GYM-IK-KK-002": (
                    "school-context",
                    "actual-local-use",
                    "teacher-observable",
                ),
                "BMB16-GYM-IK-KK-003": (
                    "school-context",
                    "actual-local-use",
                    "teacher-observable",
                ),
                "BMB16-GYM-PK-HK-003": (
                    "school-context",
                    "actual-local-use",
                    "teacher-observable",
                ),
                "LH26-E-KS-001": (
                    "school-context",
                    "actual-local-use",
                    "teacher-observable",
                ),
            },
        )
        self._assert_core03_regular_delta_review_provenance(
            reviews_by_competency_id,
            core03_contract,
            evidence_by_competency_id,
        )
        self.assertEqual(
            evidence_by_competency_id["LH26-E-KS-002"],
            {
                "id": "CE-IUM-5-CORE-03-LH26-E-KS-002",
                "competencyId": "LH26-E-KS-002",
                "mode": "module-detail",
                "learningAction": EXPECTED_KS002_LEARNING_ACTION,
                "productEvidence": EXPECTED_KS002_PRODUCT_EVIDENCE,
                "productVisibility": "shared",
            },
        )
        ks002_review_text = " ".join(
            reviews_by_competency_id["LH26-E-KS-002"][field]
            for field in ("rationale", "risk", "followUp")
        ).casefold()
        self.assertNotIn("respekt", ks002_review_text)
        self.assertNotIn("hilfeweg", ks002_review_text)

    def _assert_core05_repository_contract(
        self,
        reviews_by_competency_id,
        module_contracts,
    ):
        core05_contract = module_contracts["IUM-5-CORE-05"]
        self.assertEqual(
            core05_contract["timeReviewIds"],
            [
                "TR-LH26-E-ALG-001",
                "TR-LH26-E-PROG-002",
            ],
        )

        expected_paths = [
            "GRADE-5-BASELINE",
            "GRADE-5-REGULAR",
            "GRADE-5-EXTENDED",
        ]
        alg001_review = reviews_by_competency_id["LH26-E-ALG-001"]
        self.assertEqual(
            {
                "decision": alg001_review["decision"],
                "additionalMinutes": alg001_review["additionalMinutes"],
                "phaseIds": alg001_review["phaseIds"],
                "rationale": alg001_review["rationale"],
                "risk": alg001_review["risk"],
                "followUp": alg001_review["followUp"],
            },
            CORE05_ALG001_AUDIT_EXPECTATION,
        )
        self.assertEqual(alg001_review["moduleId"], "IUM-5-CORE-05")
        self.assertEqual(
            alg001_review["sourceTimeImpactLevel"],
            "review-required",
        )
        self.assertEqual(alg001_review["integrationContractIds"], [])
        self.assertIsNone(alg001_review["sequenceEvidenceId"])
        self.assertEqual(alg001_review["pathAvailability"], expected_paths)

        prog002_review = reviews_by_competency_id["LH26-E-PROG-002"]
        self.assertEqual(
            {
                "decision": prog002_review["decision"],
                "additionalMinutes": prog002_review["additionalMinutes"],
                "phaseIds": prog002_review["phaseIds"],
                "rationale": prog002_review["rationale"],
                "risk": prog002_review["risk"],
                "followUp": prog002_review["followUp"],
            },
            CORE05_PROG002_AUDIT_EXPECTATION,
        )
        self.assertEqual(prog002_review["moduleId"], "IUM-5-CORE-05")
        self.assertEqual(
            prog002_review["sourceTimeImpactLevel"],
            "roadmap-dependent",
        )
        self.assertEqual(prog002_review["integrationContractIds"], [])
        self.assertEqual(
            prog002_review["sequenceEvidenceId"],
            "SE-LH26-E-PROG-002",
        )
        self.assertEqual(prog002_review["pathAvailability"], [])

        core05_module = next(
            module
            for module in self.module_payload["modules"]
            if module["id"] == "IUM-5-CORE-05"
        )
        self.assertEqual(
            core05_module["centralLearningAction"],
            EXPECTED_CORE05_ALGORITHM_ACTION,
        )
        self.assertEqual(
            core05_module["centralLearningProduct"],
            EXPECTED_CORE05_ALGORITHM_PRODUCT,
        )
        alg001_evidence = next(
            evidence
            for evidence in core05_module["coverageEvidence"]
            if evidence["competencyId"] == "LH26-E-ALG-001"
        )
        self.assertEqual(alg001_evidence["mode"], "module-detail")
        self.assertEqual(
            alg001_evidence["productVisibility"],
            "teacher-observable",
        )
        for required_trace in (
            "ausgeführten grafischen Algorithmus",
            "Laufprotokoll",
            "fallbezogene Begründung",
        ):
            with self.subTest(core05_required_trace=required_trace):
                self.assertIn(
                    required_trace,
                    " ".join(
                        (
                            alg001_evidence["learningAction"],
                            alg001_evidence["productEvidence"],
                        )
                    ),
                )

    def _assert_core06_repository_contract(
        self,
        reviews_by_competency_id,
        module_contracts,
        remediation_payload=None,
        module_payload=None,
        integration_contracts=None,
    ):
        if remediation_payload is None:
            remediation_payload = self.remediation_payload
        if module_payload is None:
            module_payload = self.module_payload
        if integration_contracts is None:
            integration_contracts = self.repository_integration_contracts
        core06_contract = module_contracts["IUM-5-CORE-06"]
        expected_review_ids = [
            f"TR-{competency_id}"
            for competency_id in CORE06_AUDIT_EXPECTATIONS
        ]
        self.assertEqual(core06_contract["timeReviewIds"], expected_review_ids)

        expected_paths = [
            "GRADE-5-BASELINE",
            "GRADE-5-REGULAR",
            "GRADE-5-EXTENDED",
        ]
        for competency_id, expected in CORE06_AUDIT_EXPECTATIONS.items():
            with self.subTest(core06_competency_id=competency_id):
                review = reviews_by_competency_id[competency_id]
                self.assertEqual(
                    {
                        field: review[field]
                        for field in (
                            "decision",
                            "additionalMinutes",
                            "phaseIds",
                            "integrationContractIds",
                            "rationale",
                            "risk",
                            "followUp",
                        )
                    },
                    expected,
                )
                self.assertEqual(review["moduleId"], "IUM-5-CORE-06")
                self.assertEqual(
                    review["sourceTimeImpactLevel"],
                    "review-required",
                )
                self.assertIsNone(review["sequenceEvidenceId"])
                self.assertEqual(review["pathAvailability"], expected_paths)

        self.assertEqual(
            {
                competency_id: review["integrationContractIds"]
                for competency_id, review in reviews_by_competency_id.items()
                if competency_id in CORE06_AUDIT_EXPECTATIONS
            },
            {
                "BMB16-GYM-IK-PP-002": [
                    "INT-5-RESEARCH-PRODUCTION"
                ],
                "LH26-E-DA-005": [],
                "LH26-E-DA-006": [],
                "LH26-E-DA-008": [],
            },
        )
        for required_product_trace in (
            "Adressatengerechtes Informationsprodukt",
            "Quellenverzeichnis",
            "Vorher–Nachher-Revision",
        ):
            with self.subTest(
                core06_required_product_trace=required_product_trace
            ):
                self.assertIn(
                    required_product_trace,
                    core06_contract["centralLearningProduct"],
                )

        budgets_by_path = {
            budget["pathId"]: budget
            for budget in core06_contract["pathBudgets"]
        }
        self.assertEqual(
            {
                path_id: budget["units"]
                for path_id, budget in budgets_by_path.items()
            },
            {"baseline": 5, "regular": 5, "extended": 7},
        )
        self.assertEqual(
            budgets_by_path["baseline"]["phaseBudgets"],
            budgets_by_path["regular"]["phaseBudgets"],
        )
        regular_phase_minutes = {
            phase["phaseId"]: phase["minutes"]
            for phase in budgets_by_path["regular"]["phaseBudgets"]
        }
        extended_phase_minutes = {
            phase["phaseId"]: phase["minutes"]
            for phase in budgets_by_path["extended"]["phaseBudgets"]
        }
        actual_phase_deltas = {
            phase_id: extended_phase_minutes[phase_id] - minutes
            for phase_id, minutes in regular_phase_minutes.items()
        }
        self.assertEqual(actual_phase_deltas, CORE06_EXTENDED_PHASE_DELTAS)
        self.assertEqual(sum(actual_phase_deltas.values()), 90)
        self.assertEqual(
            (
                actual_phase_deltas["independent-action-product"],
                actual_phase_deltas["review-revise-transfer"],
            ),
            (40, 20),
        )
        self._assert_core06_extended_product_depth(core06_contract)
        self._assert_core06_canonical_delta_provenance(
            reviews_by_competency_id,
            core06_contract,
            remediation_payload,
            module_payload,
        )
        self._assert_core06_integration_boundary(integration_contracts)

    def _assert_core07_repository_contract(
        self,
        reviews_by_competency_id,
        module_contracts,
        remediation_payload=None,
        module_payload=None,
        coverage_payload=None,
    ):
        if remediation_payload is None:
            remediation_payload = self.remediation_payload
        if module_payload is None:
            module_payload = self.module_payload
        if coverage_payload is None:
            coverage_payload = self.coverage_payload

        core07_contract = module_contracts["IUM-5-CORE-07"]
        expected_review_ids = [
            f"TR-{competency_id}"
            for competency_id in CORE07_REVIEW_CONTRACTS
        ]
        self.assertEqual(
            core07_contract["timeReviewIds"],
            expected_review_ids,
        )
        self.assertEqual(core07_contract["integrationContractIds"], [])
        self.assertEqual(
            core07_contract["schoolDependentSteps"],
            ["private-local-reflection-remains-uncollected"],
        )
        for budget in core07_contract["pathBudgets"]:
            product_phase = next(
                phase
                for phase in budget["phaseBudgets"]
                if phase["phaseId"] == "independent-action-product"
            )
            self._assert_core07_product_phase_boundary(
                product_phase["learningFunction"]
            )

        expected_paths = [
            "GRADE-5-BASELINE",
            "GRADE-5-REGULAR",
            "GRADE-5-EXTENDED",
        ]
        phase_ids_by_path = {
            budget["pathId"]: {
                phase["phaseId"] for phase in budget["phaseBudgets"]
            }
            for budget in core07_contract["pathBudgets"]
        }
        for competency_id, expected in CORE07_REVIEW_CONTRACTS.items():
            review = reviews_by_competency_id[competency_id]
            self.assertEqual(
                {
                    field: review[field]
                    for field in (
                        "decision",
                        "additionalMinutes",
                        "phaseIds",
                    )
                },
                expected,
            )
            self.assertEqual(review["moduleId"], "IUM-5-CORE-07")
            self.assertEqual(
                review["sourceTimeImpactLevel"],
                "review-required",
            )
            self.assertEqual(review["integrationContractIds"], [])
            self.assertIsNone(review["sequenceEvidenceId"])
            self.assertEqual(
                review["pathAvailability"],
                (
                    []
                    if expected["decision"] == "unresolved"
                    else expected_paths
                ),
            )
            self.assertEqual(
                review["coverageConsequence"],
                "semantic-status-unchanged",
            )
            for field in ("rationale", "risk", "followUp"):
                self.assertTrue(review[field].strip())
            for phase_id in review["phaseIds"]:
                self.assertTrue(
                    all(
                        phase_id in available_phase_ids
                        for available_phase_ids in (
                            phase_ids_by_path.values()
                        )
                    )
                )

        coverage_by_id = {
            entry["competencyId"]: entry
            for entry in coverage_payload["entries"]
        }
        remediation_by_id = {
            entry["competencyId"]: entry
            for entry in remediation_payload["entries"]
        }
        self.assertEqual(
            coverage_projection_fingerprint(
                coverage_payload,
                remediation_payload,
            ),
            BASELINE_COVERAGE_PROJECTION_SHA256,
        )
        core07_module = next(
            module
            for module in module_payload["modules"]
            if module["id"] == "IUM-5-CORE-07"
        )
        core07_evidence = core07_module["coverageEvidence"]
        for competency_id in CORE07_REVIEW_CONTRACTS:
            expected_status = (
                "partial"
                if competency_id in CORE07_PARTIAL_IDS
                else "covered"
            )
            coverage = coverage_by_id[competency_id]
            handoff = remediation_by_id[competency_id]
            review = reviews_by_competency_id[competency_id]
            self.assertEqual(coverage["coverageStatus"], expected_status)
            self.assertEqual(
                handoff["after"]["coverageStatus"],
                expected_status,
            )
            self.assertEqual(
                coverage["evidenceModuleId"],
                "IUM-5-CORE-07",
            )
            self.assertEqual(
                handoff["before"]["evidenceModuleId"],
                "IUM-5-CORE-07",
            )

            if competency_id in CORE07_PARTIAL_IDS:
                self.assertIsNone(handoff["evidenceContractId"])
                self.assertIsNone(coverage.get("evidenceContractId"))
                self.assertFalse(
                    any(
                        evidence["competencyId"] == competency_id
                        for evidence in core07_evidence
                    )
                )
                self.assertEqual(review["decision"], "unresolved")
                self.assertEqual(review["additionalMinutes"], 0)
                self.assertEqual(review["phaseIds"], [])
                self.assertEqual(review["pathAvailability"], [])
                self.assertIn(
                    "partial",
                    " ".join(
                        review[field]
                        for field in ("rationale", "risk", "followUp")
                    ).casefold(),
                )
                continue

            evidence_contract_id = handoff["evidenceContractId"]
            self.assertIsInstance(evidence_contract_id, str)
            self.assertTrue(evidence_contract_id)
            self.assertEqual(
                coverage.get("evidenceContractId"),
                evidence_contract_id,
            )
            matching_evidence = [
                evidence
                for evidence in core07_evidence
                if (
                    evidence["id"] == evidence_contract_id
                    and evidence["competencyId"] == competency_id
                )
            ]
            self.assertEqual(len(matching_evidence), 1)
            evidence = matching_evidence[0]
            if competency_id in CORE07_PRIVATE_CONCEPTS:
                self._assert_core07_private_time_boundary(
                    review,
                    evidence,
                    CORE07_PRIVATE_CONCEPTS[competency_id],
                )
            else:
                self.assertEqual(
                    competency_id,
                    "BMB16-GYM-IK-MG-002",
                )
                self._assert_core07_module_detail_boundary(
                    review,
                    evidence,
                )

    def _assert_core07_private_time_boundary(
        self,
        review,
        evidence,
        concept_names,
    ):
        self.assertEqual(evidence["mode"], "private-local")
        self.assertEqual(evidence["productVisibility"], "private-local")
        self.assertEqual(
            evidence["privacyBoundary"],
            PRIVATE_LOCAL_BOUNDARY,
        )
        self.assertTrue(evidence["nonPersonalFollowUp"].strip())

        local_activity_text = " ".join(
            evidence[field]
            for field in ("learningAction", "productEvidence")
        )
        self._assert_core07_trace_groups(
            local_activity_text,
            CORE07_SEMANTIC_TRACE_GROUPS["local-private-activity"],
        )
        review_text = ". ".join(
            review[field]
            for field in ("rationale", "risk", "followUp")
        )
        for concept_name in concept_names:
            trace_groups = CORE07_SEMANTIC_TRACE_GROUPS[concept_name]
            self._assert_core07_trace_groups(
                evidence["nonPersonalFollowUp"],
                trace_groups,
            )
            self._assert_core07_trace_groups(
                review_text,
                trace_groups,
            )
        self._assert_core07_trace_groups(
            evidence["nonPersonalFollowUp"],
            CORE07_SEMANTIC_TRACE_GROUPS["independence"],
        )
        self.assertIn("nichtpersonal", review_text.casefold())
        self.assertNotIn("teacher-observable", review_text.casefold())
        self._assert_core07_trace_groups(
            review_text,
            (
                (
                    "weder beobachtet",
                    "nicht erhoben",
                    "keine beobachtbare",
                    "weder die beobachtbare",
                    "außerhalb von erhebung",
                    "ohne angaben",
                ),
            ),
        )

    def _assert_core07_module_detail_boundary(self, review, evidence):
        self.assertEqual(evidence["mode"], "module-detail")
        self.assertEqual(evidence["productVisibility"], "shared")
        self.assertNotIn("privacyBoundary", evidence)
        self.assertNotIn("nonPersonalFollowUp", evidence)
        evidence_text = " ".join(
            evidence[field]
            for field in ("learningAction", "productEvidence")
        )
        review_text = ". ".join(
            review[field]
            for field in ("rationale", "risk", "followUp")
        )
        trace_groups = CORE07_SEMANTIC_TRACE_GROUPS[
            "shared-benefit-risk-prevention"
        ]
        self._assert_core07_trace_groups(evidence_text, trace_groups)
        self._assert_core07_trace_groups(review_text, trace_groups)
        self.assertIn("nichtpersonal", review_text.casefold())

    def _assert_core07_product_phase_boundary(self, learning_function):
        self._assert_core07_trace_groups(
            learning_function,
            CORE07_SEMANTIC_TRACE_GROUPS["nonpersonal-product"],
        )
        self._assert_core07_trace_groups(
            learning_function,
            CORE07_SEMANTIC_TRACE_GROUPS["local-private-activity"],
        )
        self._assert_core07_trace_groups(
            learning_function,
            CORE07_SEMANTIC_TRACE_GROUPS["no-observation"],
        )
        self._assert_core07_trace_groups(
            learning_function,
            (
                ("produkt",),
                ("zeit",),
                ("evidenz",),
                ("beobachtung",),
                ("erklärung",),
                ("gegenperspektive",),
                ("unsicherheit",),
                ("revidier",),
            ),
        )

    def _assert_core07_trace_groups(self, text, trace_groups):
        normalized_text = " ".join(text.casefold().split())
        for alternatives in trace_groups:
            self.assertTrue(
                any(
                    trace.casefold() in normalized_text
                    for trace in alternatives
                ),
                msg=(
                    "missing CORE07 semantic trace group "
                    f"{alternatives!r}"
                ),
            )

    def _assert_core06_extended_product_depth(self, core06_contract):
        budgets_by_path = {
            budget["pathId"]: budget
            for budget in core06_contract["pathBudgets"]
        }
        regular_product_function = next(
            phase["learningFunction"]
            for phase in budgets_by_path["regular"]["phaseBudgets"]
            if phase["phaseId"] == "independent-action-product"
        )
        extended_product_function = next(
            phase["learningFunction"]
            for phase in budgets_by_path["extended"]["phaseBudgets"]
            if phase["phaseId"] == "independent-action-product"
        )
        self.assertNotEqual(
            extended_product_function,
            regular_product_function,
        )
        self.assertEqual(
            extended_product_function,
            CORE06_EXTENDED_PRODUCT_FUNCTION,
        )

    def _assert_core06_canonical_delta_provenance(
        self,
        reviews_by_competency_id,
        core06_contract,
        remediation_payload,
        module_payload,
    ):
        handoffs_by_id = {
            entry["competencyId"]: entry
            for entry in remediation_payload["entries"]
        }
        core06_module = next(
            module
            for module in module_payload["modules"]
            if module["id"] == "IUM-5-CORE-06"
        )
        canonical_chains = {}
        for competency_id in CORE06_AUDIT_EXPECTATIONS:
            handoff = handoffs_by_id[competency_id]
            evidence_contract_id = handoff["evidenceContractId"]
            matching_evidence = [
                evidence
                for evidence in core06_module["coverageEvidence"]
                if evidence["id"] == evidence_contract_id
                and evidence["competencyId"] == competency_id
            ]
            self.assertEqual(len(matching_evidence), 1)
            self.assertEqual(
                reviews_by_competency_id[competency_id]["moduleId"],
                core06_module["id"],
            )
            canonical_chains[competency_id] = (
                handoff,
                matching_evidence[0],
                reviews_by_competency_id[competency_id],
            )

        budgets_by_path = {
            budget["pathId"]: budget
            for budget in core06_contract["pathBudgets"]
        }
        regular_phase_minutes = {
            phase["phaseId"]: phase["minutes"]
            for phase in budgets_by_path["regular"]["phaseBudgets"]
        }
        extended_phase_minutes = {
            phase["phaseId"]: phase["minutes"]
            for phase in budgets_by_path["extended"]["phaseBudgets"]
        }
        positive_deltas = {
            phase_id: extended_phase_minutes[phase_id] - regular_minutes
            for phase_id, regular_minutes in regular_phase_minutes.items()
            if extended_phase_minutes[phase_id] - regular_minutes > 0
        }
        self.assertEqual(
            set(positive_deltas),
            set(CORE06_POSITIVE_DELTA_REVIEW_PROVENANCE),
        )
        for phase_id, competency_ids in (
            CORE06_POSITIVE_DELTA_REVIEW_PROVENANCE.items()
        ):
            with self.subTest(core06_delta_phase=phase_id):
                for competency_id in competency_ids:
                    self.assertIn(competency_id, canonical_chains)
                    self.assertIn(
                        phase_id,
                        canonical_chains[competency_id][2]["phaseIds"],
                    )
                supported_minutes = sum(
                    canonical_chains[competency_id][2][
                        "additionalMinutes"
                    ]
                    for competency_id in competency_ids
                )
                self.assertGreaterEqual(
                    supported_minutes,
                    positive_deltas[phase_id],
                )

    def _assert_core06_integration_boundary(self, integration_contracts):
        integration = integration_contracts["INT-5-RESEARCH-PRODUCTION"]
        self.assertEqual(
            integration["sharedPhaseOrProduct"],
            CORE06_INT5_SHARED_PHASE_OR_PRODUCT,
        )
        self.assertEqual(
            integration["preservedLearningActions"],
            CORE06_INT5_PRESERVED_LEARNING_ACTIONS,
        )
        self.assertEqual(
            integration["preservedProductAndCurriculumEvidence"],
            CORE06_INT5_PRESERVED_PRODUCT_EVIDENCE,
        )
        self.assertEqual(
            integration["prerequisites"],
            CORE06_INT5_PREREQUISITES,
        )
        self.assertEqual(integration["risk"], CORE06_INT5_RISK)
        self.assertEqual(integration["fallback"], CORE06_INT5_FALLBACK)

    def _assert_core03_regular_delta_review_provenance(
        self,
        reviews_by_competency_id,
        core03_contract,
        evidence_by_competency_id,
    ):
        budgets_by_path = {
            budget["pathId"]: budget
            for budget in core03_contract["pathBudgets"]
        }
        baseline_phases = {
            phase["phaseId"]: phase
            for phase in budgets_by_path["baseline"]["phaseBudgets"]
        }
        regular_phases = {
            phase["phaseId"]: phase
            for phase in budgets_by_path["regular"]["phaseBudgets"]
        }
        actual_increments = {
            phase_id: (
                regular_phases[phase_id]["minutes"]
                - baseline_phases[phase_id]["minutes"],
                regular_phases[phase_id]["learningFunction"],
            )
            for phase_id in regular_phases
            if (
                regular_phases[phase_id]["minutes"]
                != baseline_phases[phase_id]["minutes"]
            )
        }
        self.assertEqual(
            actual_increments,
            CORE03_REGULAR_PHASE_INCREMENTS,
        )
        self.assertEqual(
            sum(
                increment
                for increment, _learning_function
                in actual_increments.values()
            ),
            45,
        )
        self.assertEqual(
            set(actual_increments),
            set(CORE03_REGULAR_DELTA_REVIEW_PROVENANCE),
        )
        for phase_id, (
            expected_increment,
            competency_id,
        ) in CORE03_REGULAR_DELTA_REVIEW_PROVENANCE.items():
            review = reviews_by_competency_id[competency_id]
            handoff = self.handoffs_by_id[competency_id]
            evidence = evidence_by_competency_id[competency_id]
            self.assertEqual(
                actual_increments[phase_id][0],
                expected_increment,
            )
            self.assertIn(phase_id, review["phaseIds"])
            self.assertGreaterEqual(
                review["additionalMinutes"],
                expected_increment,
            )
            self.assertEqual(
                handoff["evidenceContractId"],
                evidence["id"],
            )
            self.assertEqual(
                evidence["competencyId"],
                review["competencyId"],
            )

    def _assert_core03_ks002_review_contract(self, review):
        expected = CORE03_AUDIT_EXPECTATIONS["LH26-E-KS-002"]
        self.assertEqual(
            {
                "decision": review["decision"],
                "additionalMinutes": review["additionalMinutes"],
                "phaseIds": review["phaseIds"],
                "rationale": review["rationale"],
                "risk": review["risk"],
                "followUp": review["followUp"],
            },
            expected,
        )
        review_text = " ".join(
            review[field]
            for field in ("rationale", "risk", "followUp")
        ).casefold()
        self.assertNotIn("respekt", review_text)
        self.assertNotIn("hilfeweg", review_text)

    def test_core03_ks002_rejects_nonrecord_evidence(self):
        result = validate_time_reviews(
            self.time_payload["timeReviews"],
            self.remediation_payload,
            self.repository_module_contracts,
            self.repository_integration_contracts,
            self.repository_annual_variants,
            require_complete=False,
            privacy_contracts=self.repository_privacy_contracts,
        )
        reviews_by_competency_id = {
            review["competencyId"]: review for review in result.values()
        }

        for field, nonrecord_claim in (
            (
                "rationale",
                " Zusätzlich wird eine respektvolle Reaktion eingeübt.",
            ),
            (
                "risk",
                " Zusätzlich könnte ein Hilfeweg fehlen.",
            ),
            (
                "followUp",
                " Zusätzlich einen Hilfeweg beobachten.",
            ),
        ):
            with self.subTest(field=field):
                weakened_reviews = copy.deepcopy(reviews_by_competency_id)
                weakened_reviews["LH26-E-KS-002"][field] += nonrecord_claim
                with self.assertRaises(AssertionError):
                    self._assert_core03_ks002_review_contract(
                        weakened_reviews["LH26-E-KS-002"],
                    )

    def test_core03_regular_delta_rejects_unreviewed_consolidation(self):
        result = validate_time_reviews(
            self.time_payload["timeReviews"],
            self.remediation_payload,
            self.repository_module_contracts,
            self.repository_integration_contracts,
            self.repository_annual_variants,
            require_complete=False,
            privacy_contracts=self.repository_privacy_contracts,
        )
        reviews_by_competency_id = {
            review["competencyId"]: review for review in result.values()
        }
        weakened_contract = copy.deepcopy(
            self.repository_module_contracts["IUM-5-CORE-03"]
        )
        regular_budget = next(
            budget
            for budget in weakened_contract["pathBudgets"]
            if budget["pathId"] == "regular"
        )
        phases = {
            phase["phaseId"]: phase
            for phase in regular_budget["phaseBudgets"]
        }
        phases["review-revise-transfer"]["minutes"] -= 5
        phases["shared-consolidation"]["minutes"] += 5
        core03_module = next(
            module
            for module in self.module_payload["modules"]
            if module["id"] == "IUM-5-CORE-03"
        )
        evidence_by_competency_id = {
            evidence["competencyId"]: evidence
            for evidence in core03_module["coverageEvidence"]
        }

        with self.assertRaises(AssertionError):
            self._assert_core03_regular_delta_review_provenance(
                reviews_by_competency_id,
                weakened_contract,
                evidence_by_competency_id,
            )

    def test_core03_respect_and_help_keep_their_canonical_records(self):
        coverage_by_id = {
            entry["competencyId"]: entry
            for entry in self.coverage_payload["entries"]
        }
        bmb_by_id = {
            record["id"]: record for record in self.bmb_payload["records"]
        }
        lesehilfe_by_id = {
            record["id"]: record
            for record in self.lesehilfe_payload["records"]
        }

        self.assertEqual(
            (
                bmb_by_id["BMB16-GYM-IK-KK-001"]["sourceText"],
                coverage_by_id["BMB16-GYM-IK-KK-001"][
                    "evidenceModuleId"
                ],
                coverage_by_id["BMB16-GYM-IK-KK-001"][
                    "requirementText"
                ],
            ),
            (
                "wichtige Regeln zur Kommunikation im Netz herausarbeiten "
                "und sich angemessen verhalten: zum Beispiel respektvolle "
                "Kommunikation (Netiquette), Umgang mit privaten Daten, "
                "Unterscheidung zwischen privaten und öffentlichen Daten, "
                "Cybermobbing",
                "IUM-5-CORE-03",
                "wichtige Regeln zur Kommunikation im Netz herausarbeiten "
                "und sich angemessen verhalten",
            ),
        )
        self.assertEqual(
            (
                lesehilfe_by_id["LH26-E-KS-014"]["sourceText"],
                coverage_by_id["LH26-E-KS-014"]["evidenceModuleId"],
                coverage_by_id["LH26-E-KS-014"]["evidenceContractId"],
            ),
            (
                "Merkmale verletzenden oder ausgrenzenden Verhaltens in "
                "digitalen Kommunikationsräumen (zum Beispiel Cybermobbing, "
                "Hassrede) beschreiben und exemplarisch Handlungsstrategien "
                "im Hinblick auf Präventionsmaßnahmen, Hilfsangebote oder "
                "Meldemöglichkeiten nennen",
                "IUM-6-CORE-06",
                "CE-IUM-6-CORE-06-LH26-E-KS-014",
            ),
        )

    def test_id009_repository_contract_rejects_generic_audit_text(self):
        result = validate_time_reviews(
            self.time_payload["timeReviews"],
            self.remediation_payload,
            self.repository_module_contracts,
            self.repository_integration_contracts,
            self.repository_annual_variants,
            require_complete=False,
            privacy_contracts=self.repository_privacy_contracts,
        )
        reviews_by_competency_id = {
            review["competencyId"]: review for review in result.values()
        }

        for field in ("rationale", "risk", "followUp"):
            with self.subTest(field=field):
                weakened_reviews = copy.deepcopy(reviews_by_competency_id)
                weakened_reviews["LH26-E-ID-009"][field] = (
                    "Generischer nichtleerer Audittext."
                )
                with self.assertRaises(AssertionError):
                    self._assert_id009_repository_contract(
                        weakened_reviews,
                        self.repository_module_contracts,
                    )

    def test_core06_rejects_identical_or_generic_extended_product_depth(self):
        core06_contract = self.repository_module_contracts[
            "IUM-5-CORE-06"
        ]
        self._assert_core06_extended_product_depth(core06_contract)

        budgets_by_path = {
            budget["pathId"]: budget
            for budget in core06_contract["pathBudgets"]
        }
        regular_product_function = next(
            phase["learningFunction"]
            for phase in budgets_by_path["regular"]["phaseBudgets"]
            if phase["phaseId"] == "independent-action-product"
        )
        for label, weakened_function in (
            ("identical", regular_product_function),
            (
                "generic",
                "Das zentrale Lernprodukt mit mehr Zeit vertiefen.",
            ),
        ):
            with self.subTest(weakened_product_depth=label):
                weakened_contract = copy.deepcopy(core06_contract)
                extended_budget = next(
                    budget
                    for budget in weakened_contract["pathBudgets"]
                    if budget["pathId"] == "extended"
                )
                extended_product_phase = next(
                    phase
                    for phase in extended_budget["phaseBudgets"]
                    if phase["phaseId"] == "independent-action-product"
                )
                extended_product_phase["learningFunction"] = (
                    weakened_function
                )
                with self.assertRaises(AssertionError):
                    self._assert_core06_extended_product_depth(
                        weakened_contract
                    )

    def test_core06_rejects_broken_canonical_delta_provenance(self):
        result = validate_time_reviews(
            self.time_payload["timeReviews"],
            self.remediation_payload,
            self.repository_module_contracts,
            self.repository_integration_contracts,
            self.repository_annual_variants,
            require_complete=False,
            privacy_contracts=self.repository_privacy_contracts,
        )
        reviews_by_competency_id = {
            review["competencyId"]: review for review in result.values()
        }
        core06_contract = self.repository_module_contracts[
            "IUM-5-CORE-06"
        ]
        self._assert_core06_canonical_delta_provenance(
            reviews_by_competency_id,
            core06_contract,
            self.remediation_payload,
            self.module_payload,
        )

        broken_handoff = copy.deepcopy(self.remediation_payload)
        next(
            entry
            for entry in broken_handoff["entries"]
            if entry["competencyId"] == "BMB16-GYM-IK-PP-002"
        )["evidenceContractId"] = "CE-BROKEN-CANONICAL-CHAIN"
        with self.assertRaises(AssertionError):
            self._assert_core06_canonical_delta_provenance(
                reviews_by_competency_id,
                core06_contract,
                broken_handoff,
                self.module_payload,
            )

        unsupported_phase_contract = copy.deepcopy(core06_contract)
        extended_budget = next(
            budget
            for budget in unsupported_phase_contract["pathBudgets"]
            if budget["pathId"] == "extended"
        )
        phase_minutes = {
            phase["phaseId"]: phase
            for phase in extended_budget["phaseBudgets"]
        }
        phase_minutes["build-concept"]["minutes"] += 5
        phase_minutes["guided-practice"]["minutes"] -= 5
        with self.assertRaises(AssertionError):
            self._assert_core06_canonical_delta_provenance(
                reviews_by_competency_id,
                unsupported_phase_contract,
                self.remediation_payload,
                self.module_payload,
            )

    def test_core06_rejects_overbroad_int5_shared_trace(self):
        self._assert_core06_integration_boundary(
            self.repository_integration_contracts
        )

        overbroad_integrations = copy.deepcopy(
            self.repository_integration_contracts
        )
        overbroad_integrations["INT-5-RESEARCH-PRODUCTION"][
            "sharedPhaseOrProduct"
        ] = (
            "Gemeinsame Quellen-, Rechte-, Lizenz-, Datenschutz-, "
            "Adressaten- und Produktionsspur."
        )
        with self.assertRaises(AssertionError):
            self._assert_core06_integration_boundary(
                overbroad_integrations
            )

    def _repository_reviews_by_competency_id(self):
        result = validate_time_reviews(
            self.time_payload["timeReviews"],
            self.remediation_payload,
            self.repository_module_contracts,
            self.repository_integration_contracts,
            self.repository_annual_variants,
            require_complete=False,
            privacy_contracts=self.repository_privacy_contracts,
        )
        return {
            review["competencyId"]: review for review in result.values()
        }

    def _assert_prior20_repository_contract(self, prior_reviews):
        self.assertEqual(
            tuple(review["id"] for review in prior_reviews),
            PRIOR_20_TIME_REVIEW_IDS,
        )
        canonical_structure = json.dumps(
            self._prior20_structural_projection(prior_reviews),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        self.assertEqual(
            hashlib.sha256(canonical_structure).hexdigest(),
            PRIOR_20_TIME_REVIEW_STRUCTURE_SHA256,
        )

    def _prior20_structural_projection(self, prior_reviews):
        return [
            {
                "id": review["id"],
                "competencyId": review["competencyId"],
                "moduleId": review["moduleId"],
                "grade": self.repository_module_contracts[
                    review["moduleId"]
                ]["grade"],
                "timeImpactLevel": review["sourceTimeImpactLevel"],
                "decision": review["decision"],
                "phaseIds": review["phaseIds"],
                "additionalMinutes": review["additionalMinutes"],
                "integrationContractIds": review[
                    "integrationContractIds"
                ],
                "pathAvailability": review["pathAvailability"],
                "sequenceEvidenceId": review["sequenceEvidenceId"],
                "status": review["status"],
                "coverageConsequence": review[
                    "coverageConsequence"
                ],
            }
            for review in prior_reviews
        ]

    def _canonical_sha256(self, value):
        canonical = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(canonical).hexdigest()

    def _assert_audit_review_slice(
        self,
        reviews,
        *,
        start,
        expectations,
        prior_sha256,
    ):
        expected_ids = [
            f"TR-{competency_id}" for competency_id in expectations
        ]
        audit_reviews = reviews[start:start + len(expected_ids)]
        self.assertEqual(
            [review["id"] for review in audit_reviews],
            expected_ids,
        )
        for review_id in expected_ids:
            self.assertEqual(
                sum(review["id"] == review_id for review in reviews),
                1,
            )
        self.assertEqual(
            self._canonical_sha256(reviews[:start]),
            prior_sha256,
        )
        return expected_ids, audit_reviews

    def _assert_canonical_projection(
        self,
        value,
        *,
        fields,
        expected_sha256,
        exact_fields=False,
    ):
        if exact_fields:
            self.assertEqual(set(value), set(fields))
        projection = {field: value[field] for field in fields}
        self.assertEqual(
            self._canonical_sha256(projection),
            expected_sha256,
        )

    def _assert_authoritative_evidence_chain(
        self,
        competency_id,
        *,
        module_id,
        expected_evidence_id,
        expected_cause_class,
        expected_mode,
        expected_visibility,
        handoffs,
        coverage,
        evidence,
    ):
        handoff = handoffs[competency_id]
        coverage_entry = coverage[competency_id]
        evidence_entry = evidence[competency_id]
        self.assertEqual(
            (
                handoff["causeClass"],
                handoff["before"]["evidenceModuleId"],
                handoff["timeImpact"]["level"],
                handoff["evidenceContractId"],
                coverage_entry["evidenceModuleId"],
                coverage_entry["evidenceContractId"],
                evidence_entry["id"],
                evidence_entry["mode"],
                evidence_entry["productVisibility"],
            ),
            (
                expected_cause_class,
                module_id,
                "review-required",
                expected_evidence_id,
                module_id,
                expected_evidence_id,
                expected_evidence_id,
                expected_mode,
                expected_visibility,
            ),
        )
        return evidence_entry

    def _assert_audit_review_matrix(
        self,
        audit_reviews,
        *,
        expectations,
        module_id,
        handoffs,
        coverage,
        evidence,
        cause_class,
        evidence_mode,
        evidence_visibility,
    ):
        reviews_by_competency_id = {
            review["competencyId"]: review for review in audit_reviews
        }
        self.assertEqual(
            set(reviews_by_competency_id),
            set(expectations),
        )
        matrix_fields = (
            "decision",
            "additionalMinutes",
            "phaseIds",
            "integrationContractIds",
            "pathAvailability",
        )
        for competency_id, expected in expectations.items():
            review = reviews_by_competency_id[competency_id]
            self.assertEqual(
                review["id"],
                f"TR-{review['competencyId']}",
            )
            self.assertEqual(
                tuple(review[field] for field in matrix_fields),
                tuple(expected[field] for field in matrix_fields),
            )
            self.assertEqual(
                (
                    review["moduleId"],
                    review["sourceTimeImpactLevel"],
                    review["sequenceEvidenceId"],
                    review["coverageConsequence"],
                    review["status"],
                ),
                (
                    module_id,
                    expected.get("sourceTimeImpactLevel", "review-required"),
                    expected.get("sequenceEvidenceId"),
                    "semantic-status-unchanged",
                    "working",
                ),
            )
            expected_evidence_id = expected.get(
                "evidenceContractId", f"CE-{module_id}-{competency_id}"
            )
            if expected_evidence_id is None:
                self.assertEqual(
                    (
                        handoffs[competency_id]["causeClass"],
                        handoffs[competency_id]["before"]["evidenceModuleId"],
                        handoffs[competency_id]["timeImpact"]["level"],
                        handoffs[competency_id]["evidenceContractId"],
                        coverage[competency_id]["evidenceModuleId"],
                        coverage[competency_id].get("evidenceContractId"),
                        coverage[competency_id]["coverageStatus"],
                        coverage[competency_id]["semanticAudit"],
                        competency_id in evidence,
                    ),
                    (
                        expected["causeClass"], module_id,
                        expected["sourceTimeImpactLevel"], None,
                        module_id, None, "partial", "documented-gap", False,
                    ),
                )
            else:
                self._assert_authoritative_evidence_chain(
                    competency_id,
                    module_id=module_id,
                    expected_evidence_id=expected_evidence_id,
                    expected_cause_class=expected.get("causeClass", cause_class),
                    expected_mode=expected.get("evidenceMode", evidence_mode),
                    expected_visibility=expected.get(
                        "evidenceVisibility", evidence_visibility
                    ),
                    handoffs=handoffs,
                    coverage=coverage,
                    evidence=evidence,
                )
        return reviews_by_competency_id

    def _assert_audit_paths(
        self,
        path_availability,
        *,
        module_id,
        module_contract,
        annual_variants,
        integration_id=None,
        expected_available=True,
        expected_kind=None,
        expected_targets=None,
        expected_grade=None,
    ):
        phase_minutes_by_path = {
            budget["pathId"]: {
                phase["phaseId"]: phase["minutes"]
                for phase in budget["phaseBudgets"]
            }
            for budget in module_contract["pathBudgets"]
        }
        variants_by_id = {
            variant["id"]: variant for variant in annual_variants.values()
        }
        for variant_id in path_availability:
            variant = variants_by_id[variant_id]
            allocation = next(
                item
                for item in variant["allocations"]
                if item["moduleId"] == module_id
            )
            self.assertEqual(variant["available"], expected_available)
            if expected_kind is not None:
                self.assertEqual(variant["kind"], expected_kind)
            if expected_grade is not None:
                self.assertEqual(variant["grade"], expected_grade)
            if expected_targets is not None:
                self.assertEqual(
                    variant["targetUnits"],
                    expected_targets[variant_id],
                )
            self.assertIn(
                allocation["budgetPathId"],
                phase_minutes_by_path,
            )
            if integration_id is not None:
                self.assertIn(
                    integration_id,
                    variant["integrationContractIds"],
                )
        return phase_minutes_by_path

    def _assert_fully_counted_phase_claims(
        self,
        reviews,
        *,
        phase_minutes_by_path,
        expected_claims_by_phase,
    ):
        claims_by_phase = {}
        for review in reviews:
            for phase_id in review["phaseIds"]:
                self.assertTrue(
                    all(
                        phase_minutes[phase_id] > 0
                        for phase_minutes in phase_minutes_by_path.values()
                    )
                )
                claims_by_phase[phase_id] = (
                    claims_by_phase.get(phase_id, 0)
                    + review["additionalMinutes"]
                )
            self.assertLessEqual(
                review["additionalMinutes"],
                min(
                    sum(
                        phase_minutes[phase_id]
                        for phase_id in review["phaseIds"]
                    )
                    for phase_minutes in phase_minutes_by_path.values()
                ),
            )
        self.assertEqual(claims_by_phase, expected_claims_by_phase)
        for phase_minutes in phase_minutes_by_path.values():
            for phase_id, claimed_minutes in claims_by_phase.items():
                self.assertLessEqual(
                    claimed_minutes,
                    phase_minutes[phase_id],
                )

    def test_core07_rejects_broken_authoritative_evidence_chain(self):
        reviews_by_competency_id = (
            self._repository_reviews_by_competency_id()
        )

        for source_name in ("remediation", "coverage"):
            with self.subTest(broken_core07_chain=source_name):
                remediation_payload = copy.deepcopy(
                    self.remediation_payload
                )
                coverage_payload = copy.deepcopy(self.coverage_payload)
                payload = (
                    remediation_payload
                    if source_name == "remediation"
                    else coverage_payload
                )
                next(
                    entry
                    for entry in payload["entries"]
                    if entry["competencyId"]
                    == "BMB16-GYM-IK-MG-001"
                )["evidenceContractId"] = (
                    f"CE-BROKEN-CORE07-{source_name.upper()}"
                )

                with self.assertRaises(AssertionError):
                    self._assert_core07_repository_contract(
                        reviews_by_competency_id,
                        self.repository_module_contracts,
                        remediation_payload=remediation_payload,
                        coverage_payload=coverage_payload,
                    )

    def test_core07_accepts_semantically_equivalent_product_phase(self):
        reviews_by_competency_id = (
            self._repository_reviews_by_competency_id()
        )
        module_contracts = copy.deepcopy(
            self.repository_module_contracts
        )
        equivalent_learning_function = (
            "Nur die teilbare nichtpersonale Wirkungskarte bildet die "
            "beobachtbare Produkt-, Zeit- und Evidenzspur. Die lernende "
            "Person bearbeitet daneben eine private lokale "
            "Reflexionsnotiz; sie bleibt bei ihr, wird nicht eingesehen, "
            "nicht beobachtet und nicht als Nachweis angerechnet. Das "
            "zentrale Lernprodukt eigenständig erstellen: Teilbare "
            "fallbezogene Wirkungskarte mit Beobachtung, möglicher "
            "Erklärung, Gegenperspektive, Unsicherheit und revidierbarer "
            "Handlungsoption."
        )
        for budget in module_contracts["IUM-5-CORE-07"]["pathBudgets"]:
            product_phase = next(
                phase
                for phase in budget["phaseBudgets"]
                if phase["phaseId"] == "independent-action-product"
            )
            product_phase["learningFunction"] = (
                equivalent_learning_function
            )

        self._assert_core07_repository_contract(
            reviews_by_competency_id,
            module_contracts,
        )

    def test_core07_rejects_product_phase_without_private_local_activity(self):
        reviews_by_competency_id = (
            self._repository_reviews_by_competency_id()
        )
        module_contracts = copy.deepcopy(
            self.repository_module_contracts
        )
        without_private_activity = (
            "Nur die teilbare nichtpersonale Wirkungskarte bildet die "
            "beobachtbare Produkt-, Zeit- und Evidenzspur. Private Inhalte "
            "werden nicht erhoben, gespeichert oder bewertet. Das zentrale "
            "Lernprodukt eigenständig erstellen: Teilbare fallbezogene "
            "Wirkungskarte mit Beobachtung, möglicher Erklärung, "
            "Gegenperspektive, Unsicherheit und revidierbarer "
            "Handlungsoption."
        )
        for budget in module_contracts["IUM-5-CORE-07"]["pathBudgets"]:
            product_phase = next(
                phase
                for phase in budget["phaseBudgets"]
                if phase["phaseId"] == "independent-action-product"
            )
            product_phase["learningFunction"] = without_private_activity

        with self.assertRaises(AssertionError):
            self._assert_core07_repository_contract(
                reviews_by_competency_id,
                module_contracts,
            )

    def test_prior20_structural_guard_allows_equivalent_prose(self):
        prior_reviews = copy.deepcopy(
            self.time_payload["timeReviews"][
                : len(PRIOR_20_TIME_REVIEW_IDS)
            ]
        )
        original_projection = self._prior20_structural_projection(
            prior_reviews
        )
        prior_reviews[0]["rationale"] = (
            "Innerhalb der Gerätearbeit brauchen die Erkundung der Geräte "
            "und die beobachtete Zuordnung von Eingabe, Verarbeitung und "
            "Ausgabe eine eigene angeleitete Zeitspur. Die "
            "Gerätefunktionsmatrix bleibt Bestandteil der kommentierten "
            "System- und Arbeitswegkarte."
        )
        prior_reviews[0]["risk"] = (
            "Abweichende Mediengeräte oder fehlende Komponenten können die "
            "Erkundung und Beobachtung zeitlich verlängern."
        )
        prior_reviews[0]["followUp"] = (
            "Im Pilot aggregiert erfassen, ob Geräte verfügbar sind, wie "
            "viel Unterstützung nötig ist und ob die "
            "Gerätefunktionsmatrix erreicht wird."
        )

        self.assertEqual(
            self._prior20_structural_projection(prior_reviews),
            original_projection,
        )
        self._assert_prior20_repository_contract(prior_reviews)

    def test_prior20_structural_guard_rejects_structural_mutations(self):
        mutations = (
            ("decision", "absorbed"),
            ("additionalMinutes", 99),
            ("phaseIds", ["review-revise-transfer"]),
            ("id", "TR-BROKEN-PRIOR20-ID"),
        )
        for field, value in mutations:
            with self.subTest(prior20_structural_field=field):
                prior_reviews = copy.deepcopy(
                    self.time_payload["timeReviews"][
                        : len(PRIOR_20_TIME_REVIEW_IDS)
                    ]
                )
                prior_reviews[0][field] = value
                with self.assertRaises(AssertionError):
                    self._assert_prior20_repository_contract(
                        prior_reviews
                    )

    def _assert_core02_task15_audit_contract(
        self,
        reviews,
        module_contracts=None,
        integration_contracts=None,
        annual_variants=None,
        remediation_payload=None,
        coverage_payload=None,
        module_payload=None,
        use_subtests=True,
    ):
        if module_contracts is None:
            module_contracts = self.repository_module_contracts
        if integration_contracts is None:
            integration_contracts = self.repository_integration_contracts
        if annual_variants is None:
            annual_variants = self.repository_annual_variants
        if remediation_payload is None:
            remediation_payload = self.remediation_payload
        if coverage_payload is None:
            coverage_payload = self.coverage_payload
        if module_payload is None:
            module_payload = self.module_payload

        expected_review_ids, task15_reviews = (
            self._assert_audit_review_slice(
                reviews,
                start=PRE_TASK15_TIME_REVIEW_COUNT,
                expectations=TASK15_AUDIT_EXPECTATIONS,
                prior_sha256=PRE_TASK15_TIME_REVIEWS_SHA256,
            )
        )

        reviews_by_competency_id = {
            review["competencyId"]: review for review in task15_reviews
        }
        core02_contract = module_contracts["IUM-6-CORE-02"]
        self.assertEqual(
            core02_contract["timeReviewIds"],
            expected_review_ids,
        )
        self.assertEqual(
            set(reviews_by_competency_id),
            set(TASK15_AUDIT_EXPECTATIONS),
        )

        remediation_by_id = {
            entry["competencyId"]: entry
            for entry in remediation_payload["entries"]
        }
        coverage_by_id = {
            entry["competencyId"]: entry
            for entry in coverage_payload["entries"]
        }
        core02_module = next(
            module
            for module in module_payload["modules"]
            if module["id"] == "IUM-6-CORE-02"
        )
        evidence_by_id = {
            evidence["competencyId"]: evidence
            for evidence in core02_module["coverageEvidence"]
        }
        phase_minutes_by_path = self._assert_audit_paths(
            TASK15_PATH_AVAILABILITY,
            module_id="IUM-6-CORE-02",
            module_contract=core02_contract,
            annual_variants=annual_variants,
            integration_id="INT-6-ACTORS-SELECTION",
        )

        integration = integration_contracts["INT-6-ACTORS-SELECTION"]
        self._assert_canonical_projection(
            integration,
            fields=TASK15_INTEGRATION_CONTRACT_FIELDS,
            expected_sha256=TASK15_INTEGRATION_CONTRACT_SHA256,
            exact_fields=True,
        )
        self.assertEqual(
            integration["countedInModuleId"],
            "IUM-6-CORE-01",
        )
        shared_trace = integration["sharedPhaseOrProduct"]
        for shared_anchor in (
            "Akteurs-",
            "Interessen-",
            "Evidenzkarte",
        ):
            self.assertIn(shared_anchor, shared_trace)
        for record_specific_product in (
            "Bedingungen-Matrix",
            "Werbeauswahlpfade",
        ):
            self.assertNotIn(record_specific_product, shared_trace)

        forbidden_personal_evidence = (
            ("reale Konten", "realen Konten"),
            ("Profile",),
            ("Werbeverläufe",),
            ("Standort- oder Nutzungsdaten",),
            ("Screenshots personalisierter Werbung",),
            ("personenbezogene Selbstauskünfte",),
        )
        task15_matrix = {
            competency_id: {
                **expected,
                "pathAvailability": TASK15_PATH_AVAILABILITY,
            }
            for competency_id, expected in TASK15_AUDIT_EXPECTATIONS.items()
        }
        reviews_by_competency_id = self._assert_audit_review_matrix(
            task15_reviews,
            expectations=task15_matrix,
            module_id="IUM-6-CORE-02",
            handoffs=remediation_by_id,
            coverage=coverage_by_id,
            evidence=evidence_by_id,
            cause_class="module-detail",
            evidence_mode="module-detail",
            evidence_visibility="teacher-observable",
        )
        for competency_id, expected in TASK15_AUDIT_EXPECTATIONS.items():
            subtest = (
                self.subTest(task15_competency_id=competency_id)
                if use_subtests
                else nullcontext()
            )
            with subtest:
                review = reviews_by_competency_id[competency_id]
                evidence = evidence_by_id[competency_id]

                evidence_text = " ".join(
                    (
                        evidence["learningAction"],
                        evidence["productEvidence"],
                    )
                )
                review_text = " ".join(
                    review[field]
                    for field in ("rationale", "risk", "followUp")
                )
                self._assert_canonical_projection(
                    review,
                    fields=("risk", "followUp"),
                    expected_sha256=(
                        TASK15_REVIEW_EXCLUSION_SHA256[competency_id]
                    ),
                )
                for anchor in expected["productAnchors"]:
                    self.assertIn(anchor, evidence_text)
                for anchor in expected["ownReviewAnchors"]:
                    self.assertIn(anchor, review_text)
                self.assertIn(
                    "identische gemeinsame Akteurs-, Interessen- und "
                    "Evidenzkarte",
                    review_text,
                )
                for forbidden_trace_group in forbidden_personal_evidence:
                    self.assertTrue(
                        any(
                            forbidden_trace.casefold()
                            in evidence_text.casefold()
                            for forbidden_trace in forbidden_trace_group
                        )
                    )
                    self.assertTrue(
                        any(
                            forbidden_trace.casefold()
                            in review_text.casefold()
                            for forbidden_trace in forbidden_trace_group
                        )
                    )
                self.assertIn("private Selbstreflexion", review_text)
                self.assertIn(
                    "weder Produkt, Evidenz noch Zusatzminuten",
                    review_text,
                )

        self._assert_fully_counted_phase_claims(
            task15_reviews,
            phase_minutes_by_path=phase_minutes_by_path,
            expected_claims_by_phase={
                "guided-practice": 20,
                "independent-action-product": 45,
                "review-revise-transfer": 25,
            },
        )

    def test_repository_core02_task15_audit_contract(self):
        self._assert_core02_task15_audit_contract(
            self.time_payload["timeReviews"]
        )

    def test_core02_task15_contract_allows_later_review(self):
        reviews = copy.deepcopy(self.time_payload["timeReviews"])
        reviews.append(
            {
                "id": "TR-LATER-REVIEW",
                "competencyId": "LATER-REVIEW",
            }
        )

        self._assert_core02_task15_audit_contract(reviews)

    def test_core02_task15_contract_rejects_later_duplicate_task15_id(self):
        reviews = copy.deepcopy(self.time_payload["timeReviews"])
        reviews.append(copy.deepcopy(reviews[PRE_TASK15_TIME_REVIEW_COUNT]))

        with self.assertRaises(AssertionError):
            self._assert_core02_task15_audit_contract(reviews)

    def test_core02_task15_contract_rejects_overextended_shared_trace(self):
        integration_contracts = copy.deepcopy(
            self.repository_integration_contracts
        )
        integration_contracts["INT-6-ACTORS-SELECTION"][
            "sharedPhaseOrProduct"
        ] = (
            "Gemeinsame Akteurs-, Interessen- und Evidenzkarte; sie trägt "
            "zusätzlich Bedingungen-Auszüge und Fundstellen, Auswahlregeln, "
            "konkrete Werbebotschaft, Modellgrenze und Urteil."
        )

        with self.assertRaises(AssertionError):
            self._assert_core02_task15_audit_contract(
                self.time_payload["timeReviews"],
                integration_contracts=integration_contracts,
            )

    def test_core02_task15_contract_rejects_personal_evidence_claim(self):
        reviews = copy.deepcopy(self.time_payload["timeReviews"])
        review = next(
            review
            for review in reviews
            if review["id"] == "TR-LH26-E-DP-004"
        )
        review["risk"] = (
            "Reale Konten, Profile, Werbeverläufe, Standort- oder "
            "Nutzungsdaten, Screenshots personalisierter Werbung und "
            "personenbezogene Selbstauskünfte werden als Fallgrundlage sowie "
            "Produkt- und Evidenzspur verwendet."
        )

        with self.assertRaises(AssertionError):
            self._assert_core02_task15_audit_contract(
                reviews,
                use_subtests=False,
            )

    def _assert_core06_task16_audit_contract(
        self,
        reviews,
        integration_contracts=None,
    ):
        if integration_contracts is None:
            integration_contracts = self.repository_integration_contracts

        expected_ids, task16_reviews = self._assert_audit_review_slice(
            reviews,
            start=PRE_TASK16_TIME_REVIEW_COUNT,
            expectations=TASK16_AUDIT_EXPECTATIONS,
            prior_sha256=PRE_TASK16_TIME_REVIEWS_SHA256,
        )

        core06_contract = self.repository_module_contracts[
            "IUM-6-CORE-06"
        ]
        self.assertEqual(core06_contract["timeReviewIds"], expected_ids)
        integration = integration_contracts[
            "INT-6-CONFLICT-PRODUCTION"
        ]
        self._assert_canonical_projection(
            integration,
            fields=tuple(integration),
            expected_sha256=TASK16_INTEGRATION_CONTRACT_SHA256,
        )
        self.assertEqual(
            (
                integration["moduleIds"],
                integration["pathIds"],
                integration["countedInModuleId"],
            ),
            (
                ["IUM-6-CORE-06", "IUM-6-CORE-07"],
                ["baseline", "regular"],
                "IUM-6-CORE-07",
            ),
        )
        for own_trace in ("Merkmal-und-Strategie-Spur", "Faktorenkarte"):
            self.assertNotIn(
                own_trace,
                integration["sharedPhaseOrProduct"],
            )

        handoffs = {
            entry["competencyId"]: entry
            for entry in self.remediation_payload["entries"]
        }
        coverage = {
            entry["competencyId"]: entry
            for entry in self.coverage_payload["entries"]
        }
        core06_module = next(
            module
            for module in self.module_payload["modules"]
            if module["id"] == "IUM-6-CORE-06"
        )
        evidence = {
            item["competencyId"]: item
            for item in core06_module["coverageEvidence"]
        }
        phase_minutes_by_path = self._assert_audit_paths(
            GRADE6_PATH_AVAILABILITY,
            module_id="IUM-6-CORE-06",
            module_contract=core06_contract,
            annual_variants=self.repository_annual_variants,
            integration_id="INT-6-CONFLICT-PRODUCTION",
        )
        task16_matrix = {
            competency_id: {
                **expected,
                "pathAvailability": GRADE6_PATH_AVAILABILITY,
            }
            for competency_id, expected in TASK16_AUDIT_EXPECTATIONS.items()
        }
        reviews_by_id = self._assert_audit_review_matrix(
            task16_reviews,
            expectations=task16_matrix,
            module_id="IUM-6-CORE-06",
            handoffs=handoffs,
            coverage=coverage,
            evidence=evidence,
            cause_class="module-detail",
            evidence_mode="module-detail",
            evidence_visibility="teacher-observable",
        )
        for competency_id, review in reviews_by_id.items():
            expected = TASK16_AUDIT_EXPECTATIONS[competency_id]
            self.assertNotIn("privacyDisposition", review)
            evidence_entry = evidence[competency_id]
            product_text = " ".join(
                (
                    evidence_entry["learningAction"],
                    evidence_entry["productEvidence"],
                )
            )
            review_text = " ".join(
                review[field]
                for field in ("rationale", "risk", "followUp")
            )
            for anchor in expected["productAnchors"]:
                self.assertIn(anchor, product_text)
            for anchor in expected["reviewAnchors"]:
                self.assertIn(anchor, review_text)
            self.assertIn(
                "desselben kuratierten fiktiven Konfliktfalls",
                review_text,
            )
            self._assert_canonical_projection(
                review,
                fields=("rationale", "risk", "followUp"),
                expected_sha256=(
                    TASK16_REVIEW_TEXT_PROJECTION_SHA256[competency_id]
                ),
            )

        self._assert_fully_counted_phase_claims(
            task16_reviews,
            phase_minutes_by_path=phase_minutes_by_path,
            expected_claims_by_phase={
                "guided-practice": 25,
                "independent-action-product": 45,
                "review-revise-transfer": 25,
                "build-concept": 20,
            },
        )

    def test_repository_core06_task16_audit_contract(self):
        validate_time_reviews(
            self.time_payload["timeReviews"],
            self.remediation_payload,
            self.repository_module_contracts,
            self.repository_integration_contracts,
            self.repository_annual_variants,
            require_complete=False,
            privacy_contracts=self.repository_privacy_contracts,
        )
        self._assert_core06_task16_audit_contract(
            self.time_payload["timeReviews"]
        )

    def test_core06_task16_contract_allows_later_review(self):
        reviews = copy.deepcopy(self.time_payload["timeReviews"])
        reviews.append(
            {"id": "TR-LATER-TASK16", "competencyId": "LATER-TASK16"}
        )
        self._assert_core06_task16_audit_contract(reviews)

    def test_core06_task16_contract_rejects_duplicate_id(self):
        reviews = copy.deepcopy(self.time_payload["timeReviews"])
        reviews.append(copy.deepcopy(reviews[PRE_TASK16_TIME_REVIEW_COUNT]))
        with self.assertRaises(AssertionError):
            self._assert_core06_task16_audit_contract(reviews)

    def test_core06_task16_contract_rejects_integrated_disposition(self):
        for competency_id in TASK16_AUDIT_EXPECTATIONS:
            with self.subTest(competency_id=competency_id):
                reviews = copy.deepcopy(self.time_payload["timeReviews"])
                review = next(
                    review
                    for review in reviews
                    if review["competencyId"] == competency_id
                )
                review["decision"] = "integrated"
                review["integrationContractIds"] = [
                    "INT-6-CONFLICT-PRODUCTION"
                ]
                with self.assertRaises(AssertionError):
                    self._assert_core06_task16_audit_contract(reviews)

    def test_core06_task16_contract_rejects_overextended_integration(self):
        integrations = copy.deepcopy(self.repository_integration_contracts)
        integrations["INT-6-CONFLICT-PRODUCTION"][
            "sharedPhaseOrProduct"
        ] += " Sie trägt Merkmal-und-Strategie-Spur und Faktorenkarte."
        with self.assertRaises(AssertionError):
            self._assert_core06_task16_audit_contract(
                self.time_payload["timeReviews"],
                integration_contracts=integrations,
            )

    def _assert_core06_rationale_mutation_rejected(
        self,
        competency_id,
        mutation,
    ):
        reviews = copy.deepcopy(self.time_payload["timeReviews"])
        review = next(
            review
            for review in reviews
            if review["competencyId"] == competency_id
        )
        review["rationale"] += f" {mutation}"
        with self.assertRaises(AssertionError):
            self._assert_core06_task16_audit_contract(reviews)

    def test_core06_task16_contract_rejects_personal_evidence_in_rationale(
        self,
    ):
        self._assert_core06_rationale_mutation_rejected(
            "LH26-E-KS-014",
            "Reale persönliche Konfliktdaten werden als Evidenz verwendet.",
        )

    def test_core06_task16_contract_rejects_victim_blaming_in_rationale(
        self,
    ):
        self._assert_core06_rationale_mutation_rejected(
            "LH26-E-KS-015",
            "Victim Blaming wird als Ursachenhypothese verwendet.",
        )

    def test_core06_task16_contract_rejects_remote_diagnosis_in_rationale(
        self,
    ):
        self._assert_core06_rationale_mutation_rejected(
            "LH26-E-KS-015",
            "Eine Ferndiagnose wird als Ursachenhypothese verwendet.",
        )

    def test_core06_task16_contract_rejects_offender_intent_in_rationale(
        self,
    ):
        self._assert_core06_rationale_mutation_rejected(
            "LH26-E-KS-015",
            "Eine Täterabsicht wird als sicher behauptet.",
        )

    def test_core06_task16_contract_rejects_integration_overreach_in_rationale(
        self,
    ):
        self._assert_core06_rationale_mutation_rejected(
            "LH26-E-KS-015",
            "Die Integration trägt außerdem die Faktorenkarte.",
        )

    def _assert_core07_task17_semantic_boundaries(
        self,
        *,
        evidence_by_competency_id,
        reviews_by_competency_id,
        integration_contract,
    ):
        def audit_text(evidence, review, evidence_fields):
            return " ".join(
                [evidence[field] for field in evidence_fields]
                + [review[field] for field in ("rationale", "risk", "followUp")]
            )

        da012_evidence = evidence_by_competency_id["LH26-E-DA-012"]
        da012_text = audit_text(
            da012_evidence,
            reviews_by_competency_id["LH26-E-DA-012"],
            ("learningAction", "productEvidence"),
        )
        for required_execution in (
            "mindestens drei unterscheidbare Bedienkonzepte anwenden",
            "Operation → Produktänderung",
            "zugehörige sichtbare Revision",
        ):
            self.assertIn(required_execution, da012_text)
        da012_casefold = da012_text.casefold()
        for non_execution in (
            "nur aufgelistet",
            "bloß aufgelistet",
            "nur beschrieben",
            "bloß beschrieben",
            "nur simuliert",
            "bloß simuliert",
            "ohne tatsächliche produktänderung",
            "ohne zugehörige revision",
        ):
            self.assertNotIn(non_execution, da012_casefold)

        da015_evidence = evidence_by_competency_id["LH26-E-DA-015"]
        da015_review = reviews_by_competency_id["LH26-E-DA-015"]
        self.assertEqual(da015_evidence["executionType"], "actual-local-use")
        local_gate = da015_evidence["localConfigurationRequirement"]
        for local_gate_requirement in (
            "beide verschiedenen Teilwege A und B vor Ort verfügbar",
            "schulisch freigegeben und datenschutzkonform",
            "im Modul tatsächlich benutzt",
        ):
            self.assertIn(local_gate_requirement, local_gate)
        self.assertIn(
            "Ersatzroute",
            audit_text(da015_evidence, da015_review, ()),
        )
        self.assertIn(
            "keine Zugangsdaten, privaten Links, Inhaltsprotokolle oder "
            "öffentlichen Schülerkonten werden erfasst",
            da015_evidence["productEvidence"],
        )
        da015_text = audit_text(
            da015_evidence,
            da015_review,
            (
                "learningAction",
                "productEvidence",
                "localConfigurationRequirement",
            ),
        ).casefold()
        for unsafe_evidence in (
            "als nachweis gespeichert",
            "als evidenz gespeichert",
            "als nachweis erfasst",
            "als evidenz erfasst",
            "zugangsdaten werden gespeichert",
            "private links werden gespeichert",
            "inhaltsprotokolle werden gespeichert",
            "öffentliche schülerkonten werden gespeichert",
            "öffentliche schülerkonten werden vorausgesetzt",
            "öffentliche schülerkonten werden angelegt",
        ):
            self.assertNotIn(unsafe_evidence, da015_text)
        for generic_platform_duty in (
            "plattform ist für alle schulen verpflichtend",
            "plattform wird für alle schulen vorausgesetzt",
            "allgemeine plattformpflicht",
            "ist für beide wege verpflichtend",
        ):
            self.assertNotIn(generic_platform_duty, da015_text)

        for competency_id in TASK17_AUDIT_EXPECTATIONS:
            self.assertEqual(
                reviews_by_competency_id[competency_id]["integrationContractIds"],
                [],
            )
        integration_text = integration_contract["sharedPhaseOrProduct"].casefold()
        for record_specific_trace in (
            "mikrogeschichte",
            "analyse- und wirkungsabsichtsspur",
            "bedienkonzepte",
            "teilwegspuren a und b",
        ):
            self.assertNotIn(record_specific_trace, integration_text)

    def _assert_core07_task17_audit_contract(
        self,
        reviews,
        *,
        integration_contracts=None,
        module_payload=None,
    ):
        integration_contracts = (
            integration_contracts or self.repository_integration_contracts
        )
        module_payload = module_payload or self.module_payload
        expected_ids, task_reviews = self._assert_audit_review_slice(
            reviews,
            start=PRE_TASK17_TIME_REVIEW_COUNT,
            expectations=TASK17_AUDIT_EXPECTATIONS,
            prior_sha256=PRE_TASK17_TIME_REVIEWS_SHA256,
        )
        core_contract = self.repository_module_contracts["IUM-6-CORE-07"]
        self.assertEqual(core_contract["timeReviewIds"], expected_ids)

        integration = integration_contracts["INT-6-CONFLICT-PRODUCTION"]
        self._assert_canonical_projection(
            integration,
            fields=TASK15_INTEGRATION_CONTRACT_FIELDS,
            expected_sha256=TASK16_INTEGRATION_CONTRACT_SHA256,
            exact_fields=True,
        )
        phase_minutes = self._assert_audit_paths(
            GRADE6_PATH_AVAILABILITY,
            module_id="IUM-6-CORE-07",
            module_contract=core_contract,
            annual_variants=self.repository_annual_variants,
            integration_id="INT-6-CONFLICT-PRODUCTION",
        )
        budgets = {item["pathId"]: item for item in core_contract["pathBudgets"]}
        self.assertEqual(
            [(budgets[path]["units"], budgets[path]["minutes"])
             for path in ("baseline", "regular")],
            [(5, 225), (6, 270)],
        )
        regular_deltas = {
            phase_id: phase_minutes["regular"][phase_id] - minutes
            for phase_id, minutes in phase_minutes["baseline"].items()
            if phase_minutes["regular"][phase_id] != minutes
        }
        self.assertEqual(
            regular_deltas,
            {
                "guided-practice": 10,
                "independent-action-product": 15,
                "review-revise-transfer": 15,
                "shared-consolidation": 5,
            },
        )
        self.assertEqual(sum(regular_deltas.values()), 45)
        regular_depth = " ".join(
            phase["learningFunction"]
            for phase in budgets["regular"]["phaseBudgets"]
        )
        for anchor in (
            "Weitere Asset-, Lizenz- und Gestaltungsvarianten",
            "zusätzlichen Asset- und Wirkungsnachweisen",
            "vertieft revidieren",
            "erweitert sichern",
        ):
            self.assertIn(anchor, regular_depth)

        handoffs = {item["competencyId"]: item
                    for item in self.remediation_payload["entries"]}
        coverage = {item["competencyId"]: item
                    for item in self.coverage_payload["entries"]}
        module = next(
            item
            for item in module_payload["modules"]
            if item["id"] == "IUM-6-CORE-07"
        )
        evidence = {item["competencyId"]: item
                    for item in module["coverageEvidence"]}
        task17_matrix = {
            competency_id: dict(
                decision=expected[0], additionalMinutes=expected[1],
                phaseIds=list(expected[2]), integrationContractIds=[],
                pathAvailability=GRADE6_PATH_AVAILABILITY,
                causeClass=expected[3], evidenceMode=expected[4],
                evidenceVisibility=expected[5],
            )
            for competency_id, expected in TASK17_AUDIT_EXPECTATIONS.items()
        }
        reviews_by_id = self._assert_audit_review_matrix(
            task_reviews,
            expectations=task17_matrix,
            module_id="IUM-6-CORE-07",
            handoffs=handoffs,
            coverage=coverage,
            evidence=evidence,
            cause_class=None,
            evidence_mode=None,
            evidence_visibility=None,
        )
        for competency_id, review in reviews_by_id.items():
            evidence_entry = evidence[competency_id]
            audit_text = " ".join(
                (
                    evidence_entry["learningAction"],
                    evidence_entry["productEvidence"],
                    evidence_entry.get("localConfigurationRequirement", ""),
                    review["rationale"],
                    review["risk"],
                    review["followUp"],
                )
            )
            for anchor in TASK17_REQUIRED_TEXT[competency_id]:
                self.assertIn(anchor, audit_text)
            self.assertIn(
                "INT-6-CONFLICT-PRODUCTION wird nicht beansprucht",
                audit_text,
            )
            self.assertNotIn("werden als Evidenz verwendet", audit_text)

        self._assert_core07_task17_semantic_boundaries(
            evidence_by_competency_id=evidence,
            reviews_by_competency_id=reviews_by_id,
            integration_contract=integration,
        )

        for anchor in (
            "Gestaltungs- und Wirkungsziel",
            "Feedbackbefund",
            "Soll-Ist-Abgleich",
            "Textrevision von Version 1 zu Version 2",
        ):
            self.assertIn(
                anchor,
                evidence["LH26-E-DA-009"]["productEvidence"],
            )
        self.assertEqual(
            evidence["LH26-E-DA-015"]["executionType"],
            "actual-local-use",
        )
        self.assertNotIn(
            "Microsoft Teams muss",
            evidence["LH26-E-DA-015"]["localConfigurationRequirement"],
        )
        self._assert_fully_counted_phase_claims(
            task_reviews,
            phase_minutes_by_path=phase_minutes,
            expected_claims_by_phase={
                "build-concept": 30,
                "independent-action-product": 30,
                "review-revise-transfer": 30,
                "guided-practice": 40,
            },
        )

    def test_repository_core07_task17_audit_contract(self):
        validate_time_reviews(
            self.time_payload["timeReviews"],
            self.remediation_payload,
            self.repository_module_contracts,
            self.repository_integration_contracts,
            self.repository_annual_variants,
            require_complete=False,
            privacy_contracts=self.repository_privacy_contracts,
        )
        self._assert_core07_task17_audit_contract(
            self.time_payload["timeReviews"]
        )

    def test_core07_task17_contract_allows_later_review(self):
        reviews = copy.deepcopy(self.time_payload["timeReviews"])
        reviews.append(
            {"id": "TR-LATER-TASK17", "competencyId": "LATER-TASK17"}
        )
        self._assert_core07_task17_audit_contract(reviews)

    def test_core07_task17_contract_rejects_duplicate_id(self):
        reviews = copy.deepcopy(self.time_payload["timeReviews"])
        reviews.append(copy.deepcopy(reviews[PRE_TASK17_TIME_REVIEW_COUNT]))
        with self.assertRaises(AssertionError):
            self._assert_core07_task17_audit_contract(reviews)

    def _task17_semantic_probe_inputs(self):
        module_payload = copy.deepcopy(self.module_payload)
        core07 = next(
            item for item in module_payload["modules"]
            if item["id"] == "IUM-6-CORE-07"
        )
        return (
            module_payload,
            {item["competencyId"]: item for item in core07["coverageEvidence"]},
            {
                item["competencyId"]: copy.deepcopy(item)
                for item in self.time_payload["timeReviews"]
                if item["competencyId"] in TASK17_AUDIT_EXPECTATIONS
            },
            copy.deepcopy(
                self.repository_integration_contracts[
                    "INT-6-CONFLICT-PRODUCTION"
                ]
            ),
        )

    def test_core07_task17_semantics_rejects_boundary_overrides(
        self,
    ):
        mutations = (
            (
                "da012-list-only",
                ("evidence", "LH26-E-DA-012", "productEvidence"),
                " Tatsächlich werden die drei Bedienkonzepte nur aufgelistet.",
            ),
            (
                "da015-credentials-stored",
                ("evidence", "LH26-E-DA-015", "productEvidence"),
                " Zugangsdaten werden gespeichert.",
            ),
            (
                "da015-private-links-stored",
                ("evidence", "LH26-E-DA-015", "productEvidence"),
                " Private Links werden gespeichert.",
            ),
            (
                "da015-platform-duty",
                (
                    "evidence",
                    "LH26-E-DA-015",
                    "localConfigurationRequirement",
                ),
                " Eine digitale Plattform ist für alle Schulen verpflichtend.",
            ),
            (
                "da015-moodle-duty-for-both-routes",
                (
                    "evidence",
                    "LH26-E-DA-015",
                    "localConfigurationRequirement",
                ),
                " Moodle ist für beide Wege verpflichtend.",
            ),
            (
                "record-integration-overreach",
                ("integration", "sharedPhaseOrProduct"),
                " Sie trägt Mikrogeschichte, Analyse- und "
                "Wirkungsabsichtsspur, Bedienkonzepte und Teilwegspuren A und B.",
            ),
        )
        for label, path, suffix in mutations:
            with self.subTest(semantic_boundary=label):
                _, evidence, reviews, integration = (
                    self._task17_semantic_probe_inputs()
                )
                target = {
                    "evidence": evidence,
                    "integration": integration,
                }[path[0]]
                for key in path[1:-1]:
                    target = target[key]
                target[path[-1]] += suffix

                with self.assertRaises(AssertionError):
                    self._assert_core07_task17_semantic_boundaries(
                        evidence_by_competency_id=evidence,
                        reviews_by_competency_id=reviews,
                        integration_contract=integration,
                    )

    def test_core07_task17_audit_contract_invokes_semantic_boundaries(self):
        module_payload, evidence, _, _ = (
            self._task17_semantic_probe_inputs()
        )
        evidence["LH26-E-DA-012"]["productEvidence"] += (
            " Tatsächlich werden die drei Bedienkonzepte nur aufgelistet."
        )

        with self.assertRaises(AssertionError):
            self._assert_core07_task17_audit_contract(
                self.time_payload["timeReviews"],
                module_payload=module_payload,
            )

    def test_core07_task17_contract_rejects_review_mutations(self):
        mutations = [
            (competency_id, "decision", "integrated")
            for competency_id in TASK17_AUDIT_EXPECTATIONS
        ] + [(
            "LH26-E-DA-015",
            "risk",
            "Zugangsdaten, private Links, Inhaltsprotokolle und öffentliche "
            "Schülerkonten werden als Evidenz verwendet.",
        )]
        for competency_id, field, value in mutations:
            with self.subTest(competency_id=competency_id, field=field):
                reviews = copy.deepcopy(self.time_payload["timeReviews"])
                review = next(
                    item
                    for item in reviews
                    if item["competencyId"] == competency_id
                )
                review[field] = value
                if field == "decision":
                    review["integrationContractIds"] = [
                        "INT-6-CONFLICT-PRODUCTION"
                    ]
                with self.assertRaises(AssertionError):
                    self._assert_core07_task17_audit_contract(reviews)

    def test_core07_task17_contract_rejects_evidence_mutations(self):
        mutations = (
            ("LH26-E-DA-009", "productEvidence",
             "Gestaltungs- und Wirkungsziel", "entfallenes Ziel"),
            ("LH26-E-DA-009", "productEvidence",
             "Feedbackbefund", "allgemeine Rückmeldung"),
            ("LH26-E-DA-009", "productEvidence",
             "Soll-Ist-Abgleich", "unbegründete Änderung"),
            ("LH26-E-DA-009", "productEvidence",
             "Textrevision von Version 1 zu Version 2", "kosmetische Änderung"),
            ("LH26-E-DA-010", "productEvidence",
             "Transfer in das eigene Produkt ist optional und ersetzt die "
             "Analyse nicht.", "Transfer ersetzt die Analyse."),
            ("LH26-E-DA-012", "productEvidence",
             "Operation → Produktänderung", "bloße Bedienliste"),
            ("LH26-E-DA-015", "executionType",
             "actual-local-use", "simulated-local-use"),
            ("LH26-E-DA-015", "localConfigurationRequirement",
             "Als lokales Gate",
             "Microsoft Teams muss als allgemeine Plattformvoraussetzung"),
        )
        for competency_id, field, old, new in mutations:
            with self.subTest(
                competency_id=competency_id,
                field=field,
                replacement=new,
            ):
                modules = copy.deepcopy(self.module_payload)
                module = next(
                    item
                    for item in modules["modules"]
                    if item["id"] == "IUM-6-CORE-07"
                )
                evidence = next(
                    item
                    for item in module["coverageEvidence"]
                    if item["competencyId"] == competency_id
                )
                evidence[field] = evidence[field].replace(old, new)
                with self.assertRaises(AssertionError):
                    self._assert_core07_task17_audit_contract(
                        self.time_payload["timeReviews"],
                        module_payload=modules,
                    )

    def test_core07_task17_contract_rejects_integration_overreach(self):
        integrations = copy.deepcopy(self.repository_integration_contracts)
        integrations["INT-6-CONFLICT-PRODUCTION"][
            "sharedPhaseOrProduct"
        ] += (
            " Sie trägt Mikrogeschichte, Analyse- und Wirkungsabsichtsspur, "
            "Bedienkonzepte und Teilwegspuren A und B."
        )
        with self.assertRaises(AssertionError):
            self._assert_core07_task17_audit_contract(
                self.time_payload["timeReviews"],
                integration_contracts=integrations,
            )

    def _assert_grade7_demand_scenarios(
        self,
        annual_variants,
        core_contract,
        *,
        module_id,
        integration_id,
    ):
        phase_minutes = self._assert_audit_paths(
            GRADE7_DEMAND_PATH_AVAILABILITY,
            module_id=module_id,
            module_contract=core_contract,
            annual_variants=annual_variants,
            expected_available=False,
            expected_kind="demand-scenario",
            expected_grade=7,
            expected_targets={
                "GRADE-7-OPTIMIZED-DEMAND": 40,
                "GRADE-7-ROBUST-DEMAND": 46,
                "GRADE-7-HISTORICAL-MINIMUM": 54,
            },
        )
        variants = {item["id"]: item for item in annual_variants.values()}
        for variant_id in GRADE7_INTEGRATED_DEMAND_PATH_AVAILABILITY:
            self.assertIn(
                integration_id,
                variants[variant_id]["integrationContractIds"],
            )
        self.assertNotIn(
            integration_id,
            variants["GRADE-7-HISTORICAL-MINIMUM"][
                "integrationContractIds"
            ],
        )
        return phase_minutes

    def _assert_grade7_audit_context(
        self,
        *,
        expected_time_review_ids,
        module_id,
        integration_id,
        core_stable_sha256,
        integration_contract_sha256,
        annual_variants,
        integration_contracts,
        module_contracts=None,
    ):
        module_contracts = (
            self.repository_module_contracts
            if module_contracts is None
            else module_contracts
        )
        core_contract = module_contracts[module_id]
        self.assertEqual(
            core_contract["timeReviewIds"],
            expected_time_review_ids,
        )
        stable_fields = tuple(
            field for field in core_contract if field != "timeReviewIds"
        )
        self._assert_canonical_projection(
            core_contract,
            fields=stable_fields,
            expected_sha256=core_stable_sha256,
        )
        phase_minutes = self._assert_grade7_demand_scenarios(
            annual_variants,
            core_contract,
            module_id=module_id,
            integration_id=integration_id,
        )
        grade7_variants = [
            item for item in annual_variants.values() if item["grade"] == 7
        ]
        self.assertEqual(
            self._canonical_sha256(grade7_variants),
            TASK18_GRADE7_VARIANTS_SHA256,
        )
        grade7_judgement = next(
            item
            for item in self.time_payload["gradeJudgements"]
            if item["grade"] == 7
        )
        self.assertEqual(
            (
                grade7_judgement["timeFeasibilityStatus"],
                grade7_judgement["annualVariantIds"],
            ),
            ("red", GRADE7_DEMAND_PATH_AVAILABILITY),
        )
        self.assertEqual(
            self._canonical_sha256(grade7_judgement),
            TASK18_GRADE7_JUDGEMENT_SHA256,
        )
        integration = integration_contracts[integration_id]
        self._assert_canonical_projection(
            integration,
            fields=tuple(integration),
            expected_sha256=integration_contract_sha256,
            exact_fields=True,
        )
        return core_contract, phase_minutes, integration

    def _assert_grade7_task18_demand_scenarios(
        self,
        annual_variants,
        core_contract,
    ):
        return self._assert_grade7_demand_scenarios(
            annual_variants,
            core_contract,
            module_id="IUM-7-CORE-01",
            integration_id="INT-7-DATA-CODING",
        )

    def _assert_core01_task18_semantic_boundaries(
        self,
        *,
        evidence_by_competency_id,
        reviews_by_competency_id,
        integration_contract,
    ):
        audit_texts = {
            competency_id: " ".join(
                evidence_by_competency_id[competency_id][field]
                for field in ("learningAction", "productEvidence")
            ) + " " + " ".join(
                reviews_by_competency_id[competency_id][field]
                for field in ("rationale", "risk", "followUp")
            )
            for competency_id in TASK18_AUDIT_EXPECTATIONS
        }
        for competency_id, text in audit_texts.items():
            for anchor in TASK18_REQUIRED_TEXT[competency_id]:
                self.assertIn(anchor, text)
            for forbidden in TASK18_FORBIDDEN_TEXT[competency_id]:
                self.assertNotIn(forbidden.casefold(), text.casefold())
            for anchor in TASK18_REVIEW_ANCHORS.get(competency_id, ()):
                self.assertIn(
                    anchor,
                    reviews_by_competency_id[competency_id]["rationale"],
                )

        id020_review = reviews_by_competency_id["LH26-E-ID-020"]
        self.assertEqual(
            (
                id020_review["decision"],
                id020_review["additionalMinutes"],
                id020_review["integrationContractIds"],
            ),
            ("absorbed", 0, []),
        )
        shared_text = integration_contract["sharedPhaseOrProduct"].casefold()
        for forbidden in TASK18_INTEGRATION_FORBIDDEN_TEXT:
            self.assertNotIn(forbidden.casefold(), shared_text)

        for competency_id, review in reviews_by_competency_id.items():
            path_text = " ".join(
                review[field] for field in ("rationale", "risk", "followUp")
            )
            self.assertIn("nicht verfügbare Bedarfsszenarien", path_text)
            self.assertIn("Jahresurteil bleibt red", path_text)
            for false_release in (
                "verfügbarer Jahrespfad",
                "grüner Jahrespfad",
                "freigegebener Jahrespfad",
            ):
                self.assertNotIn(false_release, path_text.casefold())

    def _assert_core01_task18_audit_contract(
        self,
        reviews,
        *,
        integration_contracts=None,
        annual_variants=None,
        module_payload=None,
    ):
        integration_contracts = (
            integration_contracts or self.repository_integration_contracts
        )
        annual_variants = annual_variants or self.repository_annual_variants
        module_payload = module_payload or self.module_payload
        expected_ids, task_reviews = self._assert_audit_review_slice(
            reviews,
            start=PRE_TASK18_TIME_REVIEW_COUNT,
            expectations=TASK18_AUDIT_EXPECTATIONS,
            prior_sha256=PRE_TASK18_TIME_REVIEWS_SHA256,
        )
        core_contract, phase_minutes, integration = (
            self._assert_grade7_audit_context(
                expected_time_review_ids=expected_ids,
                module_id="IUM-7-CORE-01",
                integration_id="INT-7-DATA-CODING",
                core_stable_sha256=TASK18_CORE01_STABLE_FIELDS_SHA256,
                integration_contract_sha256=(
                    TASK18_INTEGRATION_CONTRACT_SHA256
                ),
                annual_variants=annual_variants,
                integration_contracts=integration_contracts,
            )
        )
        self.assertEqual(
            (
                integration["moduleIds"],
                integration["pathIds"],
                integration["countedInModuleId"],
            ),
            (
                ["IUM-7-CORE-01", "IUM-7-CORE-02"],
                ["optimized", "robust"],
                "IUM-7-CORE-02",
            ),
        )

        handoffs = {
            item["competencyId"]: item
            for item in self.remediation_payload["entries"]
        }
        coverage = {
            item["competencyId"]: item
            for item in self.coverage_payload["entries"]
        }
        module = next(
            item
            for item in module_payload["modules"]
            if item["id"] == "IUM-7-CORE-01"
        )
        evidence = {
            item["competencyId"]: item
            for item in module["coverageEvidence"]
        }
        reviews_by_competency_id = self._assert_audit_review_matrix(
            task_reviews,
            expectations=TASK18_AUDIT_EXPECTATIONS,
            module_id="IUM-7-CORE-01",
            handoffs=handoffs,
            coverage=coverage,
            evidence=evidence,
            cause_class="module-detail",
            evidence_mode="module-detail",
            evidence_visibility="teacher-observable",
        )
        for competency_id, expected_sha256 in (
            TASK18_REVIEW_TEXT_PROJECTION_SHA256.items()
        ):
            self._assert_canonical_projection(
                reviews_by_competency_id[competency_id],
                fields=("rationale", "risk", "followUp"),
                expected_sha256=expected_sha256,
            )

        self._assert_core01_task18_semantic_boundaries(
            evidence_by_competency_id=evidence,
            reviews_by_competency_id=reviews_by_competency_id,
            integration_contract=integration,
        )
        self._assert_fully_counted_phase_claims(
            task_reviews,
            phase_minutes_by_path=phase_minutes,
            expected_claims_by_phase={
                "independent-action-product": 60,
                "build-concept": 30,
                "shared-consolidation": 15,
                "guided-practice": 30,
                "review-revise-transfer": 30,
            },
        )

    def _task18_semantic_probe_inputs(self):
        module_payload = copy.deepcopy(self.module_payload)
        module = next(
            item
            for item in module_payload["modules"]
            if item["id"] == "IUM-7-CORE-01"
        )
        evidence = {
            item["competencyId"]: item
            for item in module["coverageEvidence"]
        }
        reviews = {
            item["competencyId"]: copy.deepcopy(item)
            for item in self.time_payload["timeReviews"]
            if item["competencyId"] in TASK18_AUDIT_EXPECTATIONS
        }
        integration = copy.deepcopy(
            self.repository_integration_contracts["INT-7-DATA-CODING"]
        )
        return evidence, reviews, integration

    def test_repository_core01_task18_audit_contract(self):
        validate_time_reviews(
            self.time_payload["timeReviews"],
            self.remediation_payload,
            self.repository_module_contracts,
            self.repository_integration_contracts,
            self.repository_annual_variants,
            require_complete=False,
            privacy_contracts=self.repository_privacy_contracts,
        )
        self._assert_core01_task18_audit_contract(
            self.time_payload["timeReviews"]
        )

    def test_core01_task18_rejects_original_review_contradictions(self):
        contradictions = (
            (
                "INF7-16-GYM-IK-DC-001",
                "GRADE-7-OPTIMIZED-DEMAND ist verfügbar und das "
                "Jahresurteil bleibt nicht red.",
            ),
            (
                "LH26-E-ID-020",
                "Kilo und Mega sind für ID-020 verpflichtend.",
            ),
            (
                "LH26-E-ID-021",
                "Die Präfixe werden ohne Umrechnung nur aufgezählt.",
            ),
            (
                "INF7-16-GYM-IK-DC-005",
                "Nur die Vorwärtsumwandlung genügt.",
            ),
        )
        for competency_id, contradiction in contradictions:
            with self.subTest(
                competency_id=competency_id,
                contradiction=contradiction,
            ):
                evidence, reviews, integration = (
                    self._task18_semantic_probe_inputs()
                )
                reviews[competency_id]["followUp"] += f" {contradiction}"
                with self.assertRaises(AssertionError):
                    self._assert_core01_task18_semantic_boundaries(
                        evidence_by_competency_id=evidence,
                        reviews_by_competency_id=reviews,
                        integration_contract=integration,
                    )

    def test_audit_review_matrix_rejects_id_competency_mismatch(self):
        task_reviews = copy.deepcopy(
            self.time_payload["timeReviews"][
                PRE_TASK18_TIME_REVIEW_COUNT:
                PRE_TASK18_TIME_REVIEW_COUNT + len(TASK18_AUDIT_EXPECTATIONS)
            ]
        )
        task_reviews[0]["id"], task_reviews[1]["id"] = (
            task_reviews[1]["id"],
            task_reviews[0]["id"],
        )
        handoffs = {
            item["competencyId"]: item
            for item in self.remediation_payload["entries"]
        }
        coverage = {
            item["competencyId"]: item
            for item in self.coverage_payload["entries"]
        }
        module = next(
            item for item in self.module_payload["modules"]
            if item["id"] == "IUM-7-CORE-01"
        )
        evidence = {
            item["competencyId"]: item
            for item in module["coverageEvidence"]
        }
        with self.assertRaises(AssertionError):
            self._assert_audit_review_matrix(
                task_reviews,
                expectations=TASK18_AUDIT_EXPECTATIONS,
                module_id="IUM-7-CORE-01",
                handoffs=handoffs,
                coverage=coverage,
                evidence=evidence,
                cause_class="module-detail",
                evidence_mode="module-detail",
                evidence_visibility="teacher-observable",
            )

    def test_core01_task18_rejects_noncanonical_review_text_projection(self):
        for competency_id in TASK18_AUDIT_EXPECTATIONS:
            with self.subTest(competency_id=competency_id):
                reviews = copy.deepcopy(self.time_payload["timeReviews"])
                review = next(
                    item for item in reviews
                    if item["competencyId"] == competency_id
                )
                review["risk"] += " Beliebige Ergänzung."
                with self.assertRaises(AssertionError):
                    self._assert_core01_task18_audit_contract(reviews)

    def test_core01_task18_contract_allows_later_review(self):
        reviews = copy.deepcopy(self.time_payload["timeReviews"])
        reviews.append(
            {"id": "TR-LATER-TASK18", "competencyId": "LATER-TASK18"}
        )
        self._assert_core01_task18_audit_contract(reviews)

    def test_core01_task18_contract_rejects_duplicate_id(self):
        reviews = copy.deepcopy(self.time_payload["timeReviews"])
        reviews.append(copy.deepcopy(reviews[PRE_TASK18_TIME_REVIEW_COUNT]))
        with self.assertRaises(AssertionError):
            self._assert_core01_task18_audit_contract(reviews)

    def test_core01_task18_rejects_semantic_and_matrix_mutations(self):
        evidence_suffixes = (
            ("INF7-16-GYM-IK-DC-001", "Beispiele werden nur genannt."),
            ("INF7-16-GYM-IK-DC-001", "Codierung und Verschlüsselung werden gleichgesetzt."),
            ("INF7-16-GYM-IK-DC-004", "Bitfolgenlänge ohne Bit-Byte-Beziehung genügt."),
            ("INF7-16-GYM-IK-DC-004", "Größere Einheiten bleiben unklar."),
            ("INF7-16-GYM-IK-DC-005", "Nur eine Umwandlungsrichtung wird bearbeitet."),
            ("INF7-16-GYM-IK-DC-005", "Nur die Rückwärtsumwandlung genügt."),
            ("INF7-16-GYM-IK-DC-005", "Ohne Stellenwerterklärung."),
            ("INF7-16-GYM-IK-DC-005", "Ohne führende Nullen."),
            ("INF7-16-GYM-IK-DC-005", "Ohne Grenzfälle."),
            ("INF7-16-GYM-IK-DC-005", "Ohne Stellenwechselfälle."),
            ("INF7-16-GYM-IK-DC-005", "Ohne unbekannten Prüffall."),
            ("LH26-E-ID-020", "Größere Präfixe sind für diesen Record Pflicht."),
            ("LH26-E-ID-021", "Präfixe werden nur genannt."),
            ("LH26-E-ID-021", "Binärpräfixe werden vermischt: KiB und MiB."),
        )
        for competency_id, suffix in evidence_suffixes:
            with self.subTest(evidence_shortcut=(competency_id, suffix)):
                evidence, reviews, integration = self._task18_semantic_probe_inputs()
                evidence[competency_id]["productEvidence"] += f" {suffix}"
                with self.assertRaises(AssertionError):
                    self._assert_core01_task18_semantic_boundaries(
                        evidence_by_competency_id=evidence,
                        reviews_by_competency_id=reviews,
                        integration_contract=integration,
                    )

        semantic_mutations = (
            ("LH26-E-ID-020", {"decision": "additional-time", "additionalMinutes": 15}),
            ("integration", "Alltagscodierungs-Landkarte, Stellenwertmethode, Grenzfallprüfung, führende Nullen und Dezimalpräfixumrechnung."),
        )
        for target, value in semantic_mutations:
            with self.subTest(semantic_boundary=target):
                evidence, reviews, integration = self._task18_semantic_probe_inputs()
                if target == "integration":
                    integration["sharedPhaseOrProduct"] += f" {value}"
                else:
                    reviews[target].update(value)
                with self.assertRaises(AssertionError):
                    self._assert_core01_task18_semantic_boundaries(
                        evidence_by_competency_id=evidence,
                        reviews_by_competency_id=reviews,
                        integration_contract=integration,
                    )

        review_mutations = (
            ("INF7-16-GYM-IK-DC-001", "decision", "absorbed"),
            ("INF7-16-GYM-IK-DC-004", "additionalMinutes", 0),
            ("INF7-16-GYM-IK-DC-005", "integrationContractIds", []),
            ("LH26-E-ID-020", "decision", "additional-time"),
            ("LH26-E-ID-021", "phaseIds", ["guided-practice"]),
            ("INF7-16-GYM-IK-DC-005", "pathAvailability", GRADE7_DEMAND_PATH_AVAILABILITY),
        )
        for competency_id, field, value in review_mutations:
            with self.subTest(review_matrix=(competency_id, field)):
                reviews = copy.deepcopy(self.time_payload["timeReviews"])
                next(
                    item for item in reviews
                    if item["competencyId"] == competency_id
                )[field] = value
                with self.assertRaises(AssertionError):
                    self._assert_core01_task18_audit_contract(reviews)

        variants = copy.deepcopy(self.repository_annual_variants)
        variants["GRADE-7-OPTIMIZED-DEMAND"]["available"] = True
        with self.assertRaises(AssertionError):
            self._assert_grade7_task18_demand_scenarios(
                variants,
                self.repository_module_contracts["IUM-7-CORE-01"],
            )

    def _assert_grade7_task19_demand_scenarios(
        self,
        annual_variants,
        core_contract,
    ):
        return self._assert_grade7_demand_scenarios(
            annual_variants,
            core_contract,
            module_id="IUM-7-CORE-03",
            integration_id="INT-7-PROGRAMMING",
        )

    def _assert_core03_task19_semantic_boundaries(
        self,
        *,
        evidence_by_competency_id,
        reviews_by_competency_id,
        integration_contract,
    ):
        audit_texts = {
            competency_id: " ".join(
                evidence_by_competency_id[competency_id][field]
                for field in ("learningAction", "productEvidence")
            ) + " " + " ".join(
                reviews_by_competency_id[competency_id][field]
                for field in ("rationale", "risk", "followUp")
            )
            for competency_id in TASK19_AUDIT_EXPECTATIONS
        }
        for competency_id, text in audit_texts.items():
            for anchor in TASK19_REQUIRED_TEXT[competency_id]:
                self.assertIn(anchor, text)
            for forbidden in TASK19_FORBIDDEN_TEXT[competency_id]:
                self.assertNotIn(forbidden.casefold(), text.casefold())

            review = reviews_by_competency_id[competency_id]
            path_text = " ".join(
                review[field] for field in ("rationale", "risk", "followUp")
            )
            self.assertIn("nicht verfügbare Bedarfsszenarien", path_text)
            self.assertIn("Jahresurteil bleibt red", path_text)
            for false_release in (
                "ist ein verfügbarer 38-ue-pfad",
                "ist ein grüner 38-ue-pfad",
                "ist ein freigegebener 38-ue-pfad",
                "der 38-ue-pfad ist freigegeben",
                "jahresurteil bleibt nicht red",
                "jahresurteil ist nicht red",
            ):
                self.assertNotIn(false_release, path_text.casefold())

        mi005_follow_up = reviews_by_competency_id[
            "INF7-16-GYM-PK-MI-005"
        ]["followUp"]
        for anchor in TASK19_MI005_FALLBACK_REQUIRED_TEXT:
            self.assertIn(anchor, mi005_follow_up)
        for forbidden in TASK19_MI005_FALLBACK_FORBIDDEN_TEXT:
            self.assertNotIn(forbidden.casefold(), mi005_follow_up.casefold())

        integrated_ids = {
            competency_id
            for competency_id, review in reviews_by_competency_id.items()
            if review["decision"] == "integrated"
        }
        self.assertEqual(
            integrated_ids,
            {"INF7-16-GYM-IK-ALG-003", "LH26-E-ALG-007"},
        )
        for competency_id, review in reviews_by_competency_id.items():
            if competency_id in integrated_ids:
                self.assertEqual(
                    review["integrationContractIds"],
                    ["INT-7-PROGRAMMING"],
                )
                self.assertEqual(
                    review["pathAvailability"],
                    GRADE7_INTEGRATED_DEMAND_PATH_AVAILABILITY,
                )
            else:
                self.assertNotEqual(review["decision"], "absorbed")
                self.assertEqual(review["integrationContractIds"], [])
                self.assertEqual(
                    review["pathAvailability"],
                    GRADE7_DEMAND_PATH_AVAILABILITY,
                )

        integration_text = " ".join(
            [integration_contract["sharedPhaseOrProduct"]]
            + integration_contract["preservedLearningActions"]
            + integration_contract["preservedProductAndCurriculumEvidence"]
            + integration_contract["prerequisites"]
            + [integration_contract["risk"]]
        )
        for anchor in (
            "INF7-16-GYM-IK-ALG-003",
            "LH26-E-ALG-007",
            "vollständigen, korrigierten Trace",
            "eigenständige Codeausführung, Tests, Debugging",
        ):
            self.assertIn(anchor, integration_text)
        for forbidden in TASK19_INTEGRATION_FORBIDDEN_TEXT:
            self.assertNotIn(forbidden.casefold(), integration_text.casefold())

    def _assert_core03_task19_audit_contract(
        self,
        reviews,
        *,
        integration_contracts=None,
        annual_variants=None,
        module_payload=None,
    ):
        integration_contracts = (
            integration_contracts or self.repository_integration_contracts
        )
        annual_variants = annual_variants or self.repository_annual_variants
        module_payload = module_payload or self.module_payload
        expected_ids, task_reviews = self._assert_audit_review_slice(
            reviews,
            start=PRE_TASK19_TIME_REVIEW_COUNT,
            expectations=TASK19_AUDIT_EXPECTATIONS,
            prior_sha256=PRE_TASK19_TIME_REVIEWS_SHA256,
        )
        core_contract, phase_minutes, integration = (
            self._assert_grade7_audit_context(
                expected_time_review_ids=expected_ids,
                module_id="IUM-7-CORE-03",
                integration_id="INT-7-PROGRAMMING",
                core_stable_sha256=TASK19_CORE03_STABLE_FIELDS_SHA256,
                integration_contract_sha256=(
                    TASK19_INTEGRATION_CONTRACT_SHA256
                ),
                annual_variants=annual_variants,
                integration_contracts=integration_contracts,
            )
        )
        self.assertEqual(
            (
                integration["moduleIds"],
                integration["pathIds"],
                integration["countedInModuleId"],
            ),
            (
                ["IUM-7-CORE-03", "IUM-7-CORE-04"],
                ["optimized", "robust"],
                "IUM-7-CORE-04",
            ),
        )

        handoffs = {
            item["competencyId"]: item
            for item in self.remediation_payload["entries"]
        }
        coverage = {
            item["competencyId"]: item
            for item in self.coverage_payload["entries"]
        }
        module = next(
            item
            for item in module_payload["modules"]
            if item["id"] == "IUM-7-CORE-03"
        )
        evidence = {
            item["competencyId"]: item
            for item in module["coverageEvidence"]
        }
        reviews_by_competency_id = self._assert_audit_review_matrix(
            task_reviews,
            expectations=TASK19_AUDIT_EXPECTATIONS,
            module_id="IUM-7-CORE-03",
            handoffs=handoffs,
            coverage=coverage,
            evidence=evidence,
            cause_class="module-detail",
            evidence_mode="module-detail",
            evidence_visibility="teacher-observable",
        )
        for competency_id, expected_sha256 in (
            TASK19_REVIEW_TEXT_PROJECTION_SHA256.items()
        ):
            self._assert_canonical_projection(
                reviews_by_competency_id[competency_id],
                fields=("rationale", "risk", "followUp"),
                expected_sha256=expected_sha256,
            )
        self._assert_core03_task19_semantic_boundaries(
            evidence_by_competency_id=evidence,
            reviews_by_competency_id=reviews_by_competency_id,
            integration_contract=integration,
        )
        self._assert_fully_counted_phase_claims(
            task_reviews,
            phase_minutes_by_path=phase_minutes,
            expected_claims_by_phase={
                "guided-practice": 35,
                "independent-action-product": 55,
                "review-revise-transfer": 40,
                "build-concept": 25,
            },
        )

    def _task19_semantic_probe_inputs(self):
        module = next(
            item
            for item in self.module_payload["modules"]
            if item["id"] == "IUM-7-CORE-03"
        )
        evidence = {
            item["competencyId"]: item
            for item in module["coverageEvidence"]
        }
        reviews = {
            item["competencyId"]: copy.deepcopy(item)
            for item in self.time_payload["timeReviews"]
            if item["competencyId"] in TASK19_AUDIT_EXPECTATIONS
        }
        integration = copy.deepcopy(
            self.repository_integration_contracts["INT-7-PROGRAMMING"]
        )
        return evidence, reviews, integration

    def test_repository_core03_task19_audit_contract(self):
        validate_time_reviews(
            self.time_payload["timeReviews"],
            self.remediation_payload,
            self.repository_module_contracts,
            self.repository_integration_contracts,
            self.repository_annual_variants,
            require_complete=False,
            privacy_contracts=self.repository_privacy_contracts,
        )
        self._assert_core03_task19_audit_contract(
            self.time_payload["timeReviews"]
        )

    def test_core03_task19_rejects_direct_semantic_contradictions(self):
        contradictions = (
            ("INF7-16-GYM-IK-ALG-003", "Variable wird nur als unveränderlicher Wert bezeichnet."),
            ("INF7-16-GYM-PK-MI-005", "Eine bloße Anzeige oder Demo genügt."),
            ("INF7-16-GYM-PK-SV-003", "Zeitliche Reihenfolge allein genügt."),
            ("LH26-E-ALG-007", "Nur eine Schleifenvariante genügt."),
            ("LH26-E-ALG-008", "Jede Anweisung hat einen Rückgabewert."),
            ("LH26-E-ALG-009", "Nur Zahlen werden typisiert."),
            ("INF7-16-GYM-PK-SV-003", "Derselbe Programmfall genügt zur Absorption."),
            ("INF7-16-GYM-PK-MI-005", "Dasselbe grafische Werkzeug allein rechtfertigt Integration."),
            (
                "INF7-16-GYM-IK-ALG-003",
                "GRADE-7-OPTIMIZED-DEMAND ist ein verfügbarer 38-UE-Pfad.",
            ),
            ("LH26-E-ALG-008", "Optimized ist ein grüner 38-UE-Pfad."),
            ("LH26-E-ALG-009", "Das Jahresurteil bleibt nicht red."),
        )
        for competency_id, contradiction in contradictions:
            with self.subTest(
                competency_id=competency_id,
                contradiction=contradiction,
            ):
                evidence, reviews, integration = (
                    self._task19_semantic_probe_inputs()
                )
                reviews[competency_id]["followUp"] += f" {contradiction}"
                with self.assertRaises(AssertionError):
                    self._assert_core03_task19_semantic_boundaries(
                        evidence_by_competency_id=evidence,
                        reviews_by_competency_id=reviews,
                        integration_contract=integration,
                    )

    def test_core03_task19_rejects_exact_reviewer_semantic_probes(self):
        reviewer_probes = (
            (
                "review",
                "INF7-16-GYM-IK-ALG-003",
                "Die Variable ist konstant und der alte Zustand ist entbehrlich.",
            ),
            (
                "review",
                "INF7-16-GYM-PK-MI-005",
                "Nur Anzeigen reicht aus; Erstellen, Bearbeiten und Korrigieren entfallen.",
            ),
            (
                "review",
                "INF7-16-GYM-PK-SV-003",
                "Der Graph muss weder gerichtete Kanten noch Labels enthalten.",
            ),
            (
                "review",
                "LH26-E-ALG-008",
                "Jede Anweisung liefert immer ein Ergebnis.",
            ),
            (
                "review",
                "LH26-E-ALG-009",
                "Der 38-UE-Pfad ist freigegeben.",
            ),
            (
                "integration",
                None,
                "Die gemeinsame Spur macht eine eigene Implementierung unnötig.",
            ),
            (
                "integration",
                None,
                "Die Vorführung des Ablaufs reicht für die Anrechnung.",
            ),
        )
        for target, competency_id, contradiction in reviewer_probes:
            with self.subTest(
                target=target,
                competency_id=competency_id,
                contradiction=contradiction,
            ):
                evidence, reviews, integration = (
                    self._task19_semantic_probe_inputs()
                )
                if target == "integration":
                    integration["sharedPhaseOrProduct"] += f" {contradiction}"
                else:
                    reviews[competency_id]["followUp"] += f" {contradiction}"
                with self.assertRaises(AssertionError):
                    self._assert_core03_task19_semantic_boundaries(
                        evidence_by_competency_id=evidence,
                        reviews_by_competency_id=reviews,
                        integration_contract=integration,
                    )

    def test_core03_task19_rejects_static_mi005_fallback(self):
        static_fallbacks = (
            "Bei Ausfall eine vorbereitete Ersatzdarstellung nutzen.",
            "Bei Ausfall genügt eine statische Ersatzdarstellung.",
        )
        for static_fallback in static_fallbacks:
            with self.subTest(static_fallback=static_fallback):
                evidence, reviews, integration = (
                    self._task19_semantic_probe_inputs()
                )
                reviews["INF7-16-GYM-PK-MI-005"]["followUp"] = static_fallback
                with self.assertRaises(AssertionError):
                    self._assert_core03_task19_semantic_boundaries(
                        evidence_by_competency_id=evidence,
                        reviews_by_competency_id=reviews,
                        integration_contract=integration,
                    )

    def test_core03_task19_rejects_integration_overreach(self):
        overreaches = (
            "Sie ersetzt Implementierung.",
            "Sie ersetzt Codeausführung.",
            "Sie ersetzt Normal-, Grenz- und Gegenfalltests.",
            "Sie ersetzt Debugging.",
            "Ein nur demonstrierter Trace genügt für die Integration.",
            "Ein anderer Programmfall genügt für die Integration.",
        )
        for overreach in overreaches:
            with self.subTest(overreach=overreach):
                evidence, reviews, integration = (
                    self._task19_semantic_probe_inputs()
                )
                integration["sharedPhaseOrProduct"] += f" {overreach}"
                with self.assertRaises(AssertionError):
                    self._assert_core03_task19_semantic_boundaries(
                        evidence_by_competency_id=evidence,
                        reviews_by_competency_id=reviews,
                        integration_contract=integration,
                    )

    def test_core03_task19_rejects_noncanonical_review_text_projection(self):
        for competency_id in TASK19_AUDIT_EXPECTATIONS:
            with self.subTest(competency_id=competency_id):
                reviews = copy.deepcopy(self.time_payload["timeReviews"])
                review = next(
                    item for item in reviews
                    if item["competencyId"] == competency_id
                )
                review["risk"] += " Beliebige Ergänzung."
                with self.assertRaises(AssertionError):
                    self._assert_core03_task19_audit_contract(reviews)

    def test_core03_task19_contract_allows_later_review(self):
        reviews = copy.deepcopy(self.time_payload["timeReviews"])
        reviews.append(
            {"id": "TR-LATER-TASK19", "competencyId": "LATER-TASK19"}
        )
        self._assert_core03_task19_audit_contract(reviews)

    def test_core03_task19_contract_rejects_duplicate_id(self):
        reviews = copy.deepcopy(self.time_payload["timeReviews"])
        reviews.append(copy.deepcopy(reviews[PRE_TASK19_TIME_REVIEW_COUNT]))
        with self.assertRaises(AssertionError):
            self._assert_core03_task19_audit_contract(reviews)

    def test_core03_task19_rejects_matrix_path_and_phase_mutations(self):
        review_mutations = (
            ("INF7-16-GYM-IK-ALG-003", "decision", "absorbed"),
            ("INF7-16-GYM-PK-MI-005", "additionalMinutes", 0),
            ("INF7-16-GYM-PK-SV-003", "integrationContractIds", ["INT-7-PROGRAMMING"]),
            ("LH26-E-ALG-007", "pathAvailability", GRADE7_DEMAND_PATH_AVAILABILITY),
            ("LH26-E-ALG-008", "phaseIds", ["build-concept"]),
            ("LH26-E-ALG-009", "decision", "absorbed"),
        )
        for competency_id, field, value in review_mutations:
            with self.subTest(review_matrix=(competency_id, field)):
                reviews = copy.deepcopy(self.time_payload["timeReviews"])
                next(
                    item for item in reviews
                    if item["competencyId"] == competency_id
                )[field] = value
                with self.assertRaises(AssertionError):
                    self._assert_core03_task19_audit_contract(reviews)

        variants = copy.deepcopy(self.repository_annual_variants)
        variants["GRADE-7-OPTIMIZED-DEMAND"]["available"] = True
        with self.assertRaises(AssertionError):
            self._assert_grade7_task19_demand_scenarios(
                variants,
                self.repository_module_contracts["IUM-7-CORE-03"],
            )

        task_reviews = copy.deepcopy(
            self.time_payload["timeReviews"][
                PRE_TASK19_TIME_REVIEW_COUNT:
                PRE_TASK19_TIME_REVIEW_COUNT + len(TASK19_AUDIT_EXPECTATIONS)
            ]
        )
        next(
            item for item in task_reviews
            if item["competencyId"] == "LH26-E-ALG-009"
        )["additionalMinutes"] = 20
        phase_minutes = self._assert_grade7_task19_demand_scenarios(
            self.repository_annual_variants,
            self.repository_module_contracts["IUM-7-CORE-03"],
        )
        with self.assertRaises(AssertionError):
            self._assert_fully_counted_phase_claims(
                task_reviews,
                phase_minutes_by_path=phase_minutes,
                expected_claims_by_phase={
                    "guided-practice": 35,
                    "independent-action-product": 55,
                    "review-revise-transfer": 40,
                    "build-concept": 25,
                },
            )

    def _assert_grade7_task20_demand_scenarios(
        self,
        annual_variants,
        core_contract,
    ):
        return self._assert_grade7_demand_scenarios(
            annual_variants,
            core_contract,
            module_id="IUM-7-CORE-04",
            integration_id="INT-7-PROGRAMMING",
        )

    def _assert_core04_task20_semantic_boundaries(
        self,
        *,
        evidence_by_competency_id,
        reviews_by_competency_id,
        integration_contract,
    ):
        audit_texts = {
            competency_id: " ".join(
                evidence_by_competency_id[competency_id][field]
                for field in ("learningAction", "productEvidence")
            ) + " " + " ".join(
                reviews_by_competency_id[competency_id][field]
                for field in ("rationale", "risk", "followUp")
            )
            for competency_id in TASK20_AUDIT_EXPECTATIONS
        }
        for competency_id, text in audit_texts.items():
            for anchor in TASK20_REQUIRED_TEXT[competency_id]:
                self.assertIn(anchor, text)
            for forbidden in TASK20_FORBIDDEN_TEXT[competency_id]:
                self.assertNotIn(forbidden.casefold(), text.casefold())

            review = reviews_by_competency_id[competency_id]
            review_text = " ".join(
                review[field] for field in ("rationale", "risk", "followUp")
            )
            self.assertIn("nicht verfügbare Bedarfsszenarien", review_text)
            self.assertIn("Jahresurteil bleibt red", review_text)
            self.assertIn("Personenprofil", review_text)
            self.assertIn("automatisches Scoring", review_text)
            for false_release in (
                "ist ein verfügbarer 38-ue-pfad",
                "ist ein grüner 38-ue-pfad",
                "ist ein freigegebener 38-ue-pfad",
                "der 38-ue-pfad ist freigegeben",
                "jahresurteil bleibt nicht red",
                "jahresurteil ist nicht red",
            ):
                self.assertNotIn(false_release, review_text.casefold())
            self.assertEqual(review["decision"], "additional-time")
            self.assertGreater(review["additionalMinutes"], 0)
            self.assertEqual(review["integrationContractIds"], [])
            self.assertEqual(
                review["pathAvailability"],
                GRADE7_DEMAND_PATH_AVAILABILITY,
            )

        individually_attributable = {
            "INF7-16-GYM-PK-KK-002": (
                "jede lernende Person",
                "eigene zielgruppenbezogene Erklärung oder begründete "
                "Anpassungsentscheidung",
                "eindeutig zuordnen",
            ),
            "INF7-16-GYM-PK-MI-003": (
                "Jede lernende Person",
                "eigene Invariante-/Variationsentscheidung",
                "eindeutig zurechenbar",
            ),
            "INF7-16-GYM-PK-SV-002": (
                "Jede lernende Person",
                "mindestens eine Datei- oder Programmbezeichner-Umbenennung",
                "tatsächlich aus",
                "begründet sie",
            ),
        }
        for competency_id, anchors in individually_attributable.items():
            review_text = " ".join(
                reviews_by_competency_id[competency_id][field]
                for field in ("rationale", "risk", "followUp")
            )
            for anchor in anchors:
                self.assertIn(anchor, review_text)

        integration_text = " ".join(
            [integration_contract["sharedPhaseOrProduct"]]
            + integration_contract["preservedLearningActions"]
            + integration_contract["preservedProductAndCurriculumEvidence"]
            + integration_contract["prerequisites"]
            + [integration_contract["risk"], integration_contract["fallback"]]
        )
        for anchor in (
            "LH26-E-ALG-010",
            "INF7-16-GYM-IK-ALG-005",
            "eigenständige Codeausführung, Tests, Debugging",
        ):
            self.assertIn(anchor, integration_text)
        self.assertEqual(integration_contract["sharedMinutes"], 90)
        self.assertEqual(
            integration_contract["countedInModuleId"],
            "IUM-7-CORE-04",
        )
        for forbidden in TASK20_INTEGRATION_FORBIDDEN_TEXT:
            self.assertNotIn(forbidden.casefold(), integration_text.casefold())

    def _assert_core04_task20_audit_contract(
        self,
        reviews,
        *,
        integration_contracts=None,
        annual_variants=None,
        module_payload=None,
    ):
        integration_contracts = (
            integration_contracts or self.repository_integration_contracts
        )
        annual_variants = annual_variants or self.repository_annual_variants
        module_payload = module_payload or self.module_payload
        expected_ids, task_reviews = self._assert_audit_review_slice(
            reviews,
            start=PRE_TASK20_TIME_REVIEW_COUNT,
            expectations=TASK20_AUDIT_EXPECTATIONS,
            prior_sha256=PRE_TASK20_TIME_REVIEWS_SHA256,
        )
        core_contract, phase_minutes, integration = (
            self._assert_grade7_audit_context(
                expected_time_review_ids=expected_ids,
                module_id="IUM-7-CORE-04",
                integration_id="INT-7-PROGRAMMING",
                core_stable_sha256=TASK20_CORE04_STABLE_FIELDS_SHA256,
                integration_contract_sha256=(
                    TASK20_INTEGRATION_CONTRACT_SHA256
                ),
                annual_variants=annual_variants,
                integration_contracts=integration_contracts,
            )
        )
        self.assertEqual(
            (
                integration["moduleIds"],
                integration["pathIds"],
                integration["countedInModuleId"],
            ),
            (
                ["IUM-7-CORE-03", "IUM-7-CORE-04"],
                ["optimized", "robust"],
                "IUM-7-CORE-04",
            ),
        )

        handoffs = {
            item["competencyId"]: item
            for item in self.remediation_payload["entries"]
        }
        coverage = {
            item["competencyId"]: item
            for item in self.coverage_payload["entries"]
        }
        module = next(
            item
            for item in module_payload["modules"]
            if item["id"] == "IUM-7-CORE-04"
        )
        evidence = {
            item["competencyId"]: item
            for item in module["coverageEvidence"]
        }
        reviews_by_competency_id = self._assert_audit_review_matrix(
            task_reviews,
            expectations=TASK20_AUDIT_EXPECTATIONS,
            module_id="IUM-7-CORE-04",
            handoffs=handoffs,
            coverage=coverage,
            evidence=evidence,
            cause_class="module-detail",
            evidence_mode="module-detail",
            evidence_visibility="shared",
        )
        for competency_id, expected_sha256 in (
            TASK20_REVIEW_TEXT_PROJECTION_SHA256.items()
        ):
            self._assert_canonical_projection(
                reviews_by_competency_id[competency_id],
                fields=("rationale", "risk", "followUp"),
                expected_sha256=expected_sha256,
            )
        self._assert_core04_task20_semantic_boundaries(
            evidence_by_competency_id=evidence,
            reviews_by_competency_id=reviews_by_competency_id,
            integration_contract=integration,
        )
        self._assert_fully_counted_phase_claims(
            task_reviews,
            phase_minutes_by_path=phase_minutes,
            expected_claims_by_phase={
                "independent-action-product": 70,
                "review-revise-transfer": 45,
                "guided-practice": 25,
            },
        )

    def _task20_semantic_probe_inputs(self):
        module = next(
            item
            for item in self.module_payload["modules"]
            if item["id"] == "IUM-7-CORE-04"
        )
        evidence = {
            item["competencyId"]: item
            for item in module["coverageEvidence"]
        }
        reviews = {
            item["competencyId"]: copy.deepcopy(item)
            for item in self.time_payload["timeReviews"]
            if item["competencyId"] in TASK20_AUDIT_EXPECTATIONS
        }
        integration = copy.deepcopy(
            self.repository_integration_contracts["INT-7-PROGRAMMING"]
        )
        return evidence, reviews, integration

    def test_repository_core04_task20_audit_contract(self):
        validate_time_reviews(
            self.time_payload["timeReviews"],
            self.remediation_payload,
            self.repository_module_contracts,
            self.repository_integration_contracts,
            self.repository_annual_variants,
            require_complete=False,
            privacy_contracts=self.repository_privacy_contracts,
        )
        self._assert_core04_task20_audit_contract(
            self.time_payload["timeReviews"]
        )

    def test_core04_task20_rejects_direct_semantic_contradictions(self):
        contradictions = (
            ("INF7-16-GYM-PK-KK-002", "Allgemein verständliche Sprache genügt."),
            ("INF7-16-GYM-PK-KK-002", "Zielgruppe und Vorwissen sind entbehrlich."),
            ("INF7-16-GYM-PK-KK-002", "Viererstruktur entfällt."),
            ("INF7-16-GYM-PK-KK-002", "Glossar oder Beispiel entfallen."),
            ("INF7-16-GYM-PK-KK-002", "Präsentation des Teamprodukts genügt."),
            ("INF7-16-GYM-PK-MI-003", "Details nur löschen genügt."),
            ("INF7-16-GYM-PK-MI-003", "Ein Fall genügt."),
            (
                "INF7-16-GYM-PK-MI-003",
                "Invariante und Variation müssen nicht getrennt werden.",
            ),
            ("INF7-16-GYM-PK-MI-003", "Rückanwendung entfällt."),
            ("INF7-16-GYM-PK-SV-002", "Clean-Code-Behauptung genügt."),
            (
                "INF7-16-GYM-PK-SV-002",
                "Namenstabelle ohne Umbenennung genügt.",
            ),
            ("INF7-16-GYM-PK-SV-002", "Namenskonvention entfällt."),
            (
                "INF7-16-GYM-PK-SV-002",
                "x, test1 und final_final sind aussagekräftig.",
            ),
            (
                "INF7-16-GYM-PK-KK-002",
                "Ein Teammitglied erledigt die Erklärung für alle.",
            ),
            (
                "INF7-16-GYM-PK-MI-003",
                "Ein Teammitglied erledigt die Abstraktion für alle.",
            ),
            (
                "INF7-16-GYM-PK-SV-002",
                "Ein Teammitglied benennt für alle um.",
            ),
            (
                "INF7-16-GYM-PK-KK-002",
                "Dasselbe Teamprodukt begründet recordbezogene Integration.",
            ),
            (
                "INF7-16-GYM-PK-MI-003",
                "Derselbe Fall begründet recordbezogene Integration.",
            ),
            (
                "INF7-16-GYM-PK-SV-002",
                "Dasselbe Programm begründet recordbezogene Integration.",
            ),
            (
                "INF7-16-GYM-PK-KK-002",
                "Die 90 Minuten werden für KK-002 erneut angerechnet.",
            ),
            (
                "INF7-16-GYM-PK-MI-003",
                "Die 90 Minuten werden für MI-003 erneut angerechnet.",
            ),
            (
                "INF7-16-GYM-PK-SV-002",
                "Die 90 Minuten werden für SV-002 erneut angerechnet.",
            ),
            (
                "INF7-16-GYM-PK-KK-002",
                "GRADE-7-OPTIMIZED-DEMAND ist ein verfügbarer 38-UE-Pfad.",
            ),
            (
                "INF7-16-GYM-PK-MI-003",
                "Das Jahresurteil bleibt nicht red.",
            ),
        )
        for competency_id, contradiction in contradictions:
            with self.subTest(
                competency_id=competency_id,
                contradiction=contradiction,
            ):
                evidence, reviews, integration = (
                    self._task20_semantic_probe_inputs()
                )
                reviews[competency_id]["followUp"] += f" {contradiction}"
                with self.assertRaises(AssertionError):
                    self._assert_core04_task20_semantic_boundaries(
                        evidence_by_competency_id=evidence,
                        reviews_by_competency_id=reviews,
                        integration_contract=integration,
                    )

    def test_core04_task20_rejects_integration_overreach_semantically(self):
        overreaches = (
            (
                "sharedPhaseOrProduct",
                " Zielgruppenkommunikation, Abstraktionshandlung und "
                "Namensrefaktorierung werden gemeinsam getragen.",
            ),
            (
                "sharedPhaseOrProduct",
                " Teamarbeit ersetzt die individuelle Fachhandlung.",
            ),
            (
                "preservedProductAndCurriculumEvidence",
                "Kompetenznachweis INF7-16-GYM-PK-KK-002, "
                "INF7-16-GYM-PK-MI-003 und INF7-16-GYM-PK-SV-002.",
            ),
        )
        for field, overreach in overreaches:
            with self.subTest(integration_field=field, overreach=overreach):
                evidence, reviews, integration = (
                    self._task20_semantic_probe_inputs()
                )
                if isinstance(integration[field], list):
                    integration[field].append(overreach)
                else:
                    integration[field] += overreach
                with self.assertRaises(AssertionError):
                    self._assert_core04_task20_semantic_boundaries(
                        evidence_by_competency_id=evidence,
                        reviews_by_competency_id=reviews,
                        integration_contract=integration,
                    )

    def test_core04_task20_rejects_noncanonical_review_text_projection(self):
        for competency_id in TASK20_AUDIT_EXPECTATIONS:
            with self.subTest(competency_id=competency_id):
                reviews = copy.deepcopy(self.time_payload["timeReviews"])
                review = next(
                    item
                    for item in reviews
                    if item["competencyId"] == competency_id
                )
                review["risk"] += " Beliebige Ergänzung."
                with self.assertRaises(AssertionError):
                    self._assert_core04_task20_audit_contract(reviews)

    def test_core04_task20_contract_allows_later_review(self):
        reviews = copy.deepcopy(self.time_payload["timeReviews"])
        reviews.append(
            {"id": "TR-LATER-TASK20", "competencyId": "LATER-TASK20"}
        )
        self._assert_core04_task20_audit_contract(reviews)

    def test_core04_task20_contract_rejects_duplicate_id(self):
        reviews = copy.deepcopy(self.time_payload["timeReviews"])
        reviews.append(copy.deepcopy(reviews[PRE_TASK20_TIME_REVIEW_COUNT]))
        with self.assertRaises(AssertionError):
            self._assert_core04_task20_audit_contract(reviews)

    def test_core04_task20_rejects_matrix_path_and_phase_mutations(self):
        review_mutations = (
            ("INF7-16-GYM-PK-KK-002", "decision", "absorbed"),
            ("INF7-16-GYM-PK-MI-003", "additionalMinutes", 0),
            (
                "INF7-16-GYM-PK-SV-002",
                "integrationContractIds",
                ["INT-7-PROGRAMMING"],
            ),
            (
                "INF7-16-GYM-PK-KK-002",
                "pathAvailability",
                GRADE7_INTEGRATED_DEMAND_PATH_AVAILABILITY,
            ),
            ("INF7-16-GYM-PK-MI-003", "phaseIds", ["build-concept"]),
            ("INF7-16-GYM-PK-SV-002", "decision", "integrated"),
        )
        for competency_id, field, value in review_mutations:
            with self.subTest(review_matrix=(competency_id, field)):
                reviews = copy.deepcopy(self.time_payload["timeReviews"])
                next(
                    item
                    for item in reviews
                    if item["competencyId"] == competency_id
                )[field] = value
                with self.assertRaises(AssertionError):
                    self._assert_core04_task20_audit_contract(reviews)

        for variant_id, field, value in (
            ("GRADE-7-OPTIMIZED-DEMAND", "available", True),
            ("GRADE-7-ROBUST-DEMAND", "targetUnits", 38),
        ):
            with self.subTest(variant=(variant_id, field)):
                variants = copy.deepcopy(self.repository_annual_variants)
                variants[variant_id][field] = value
                with self.assertRaises(AssertionError):
                    self._assert_grade7_task20_demand_scenarios(
                        variants,
                        self.repository_module_contracts["IUM-7-CORE-04"],
                    )

        task_reviews = copy.deepcopy(
            self.time_payload["timeReviews"][
                PRE_TASK20_TIME_REVIEW_COUNT:
                PRE_TASK20_TIME_REVIEW_COUNT + len(TASK20_AUDIT_EXPECTATIONS)
            ]
        )
        next(
            item
            for item in task_reviews
            if item["competencyId"] == "INF7-16-GYM-PK-SV-002"
        )["additionalMinutes"] = 30
        phase_minutes = self._assert_grade7_task20_demand_scenarios(
            self.repository_annual_variants,
            self.repository_module_contracts["IUM-7-CORE-04"],
        )
        with self.assertRaises(AssertionError):
            self._assert_fully_counted_phase_claims(
                task_reviews,
                phase_minutes_by_path=phase_minutes,
                expected_claims_by_phase={
                    "independent-action-product": 80,
                    "review-revise-transfer": 55,
                    "guided-practice": 25,
                },
            )

    def _assert_core05_task21_semantic_boundaries(
        self,
        *,
        evidence_by_competency_id,
        reviews_by_competency_id,
        integration_contract,
    ):
        audit_texts = {}
        for competency_id in TASK21_AUDIT_EXPECTATIONS:
            evidence = evidence_by_competency_id[competency_id]
            evidence_text = " ".join(
                str(evidence[field])
                for field in (
                    "learningAction",
                    "productEvidence",
                    "executionType",
                    "localConfigurationRequirement",
                )
                if field in evidence
            )
            review = reviews_by_competency_id[competency_id]
            review_text = " ".join(
                review[field] for field in ("rationale", "risk", "followUp")
            )
            audit_texts[competency_id] = f"{evidence_text} {review_text}"

            for anchor in TASK21_REQUIRED_TEXT[competency_id]:
                self.assertIn(anchor, audit_texts[competency_id])
            for forbidden in TASK21_FORBIDDEN_TEXT[competency_id]:
                self.assertNotIn(
                    forbidden.casefold(), audit_texts[competency_id].casefold()
                )
            for anchor in (
                "nicht verfügbare Bedarfsszenarien",
                "Jahresurteil bleibt red",
                "Personenprofil",
                "automatische Punkte",
                "automatisches Scoring",
            ):
                self.assertIn(anchor, review_text)
            for false_release in (
                "ist ein verfügbarer 38-ue-pfad",
                "ist ein grüner 38-ue-pfad",
                "ist ein freigegebener 38-ue-pfad",
                "jahresurteil bleibt nicht red",
                "personenprofil wird angelegt",
                "automatische punkte werden vergeben",
                "automatisches scoring wird eingesetzt",
            ):
                self.assertNotIn(false_release, review_text.casefold())

        individual_anchors = {
            "INF7-16-GYM-IK-IGD-004": (
                "Jede lernende Person",
                "eigene vollständige Risiko–Maßnahme-Spur",
                "lehrkraftbeobachtbar oder eindeutig zurechenbar",
            ),
            "INF7-16-GYM-PK-AB-002": (
                "Jede lernende Person", "eigene Modell–Realsituation-Tabelle",
                "lehrkraftbeobachtbar oder eindeutig zurechenbar",
            ),
            "INF7-16-GYM-PK-SV-001": (
                "Jede lernende Person", "tatsächliche Speicher- oder Upload-",
                "Abruf-, Öffnungs- und Prüfhandlung",
                "lehrkraftbeobachtbar oder eindeutig zurechenbar",
            ),
        }
        for competency_id, anchors in individual_anchors.items():
            review_text = " ".join(
                reviews_by_competency_id[competency_id][field]
                for field in ("rationale", "risk", "followUp")
            )
            for anchor in anchors:
                self.assertIn(anchor, review_text)

        sv_evidence = evidence_by_competency_id[
            "INF7-16-GYM-PK-SV-001"
        ]
        self.assertEqual(sv_evidence["executionType"], "actual-local-use")
        for anchor in (
            "Vor Freigabe benennt die Lehrkraft",
            "lokal verfügbares, schulisch freigegebenes und "
            "datenschutzkonformes Schulnetz",
            "neutrale Aufgabe",
            "bleibt der Record partial",
        ):
            self.assertIn(anchor, sv_evidence["localConfigurationRequirement"])

        integration_text = " ".join(
            [integration_contract["sharedPhaseOrProduct"]]
            + integration_contract["preservedLearningActions"]
            + integration_contract["preservedProductAndCurriculumEvidence"]
            + integration_contract["prerequisites"]
            + [integration_contract["risk"], integration_contract["fallback"]]
        )
        for anchor in (
            "INF7-16-GYM-IK-IGD-004",
            "Bedrohung und begründete Schutzmaßnahme",
        ):
            self.assertIn(anchor, integration_text)
        self.assertEqual(integration_contract["sharedMinutes"], 135)
        self.assertEqual(
            integration_contract["countedInModuleId"], "IUM-7-CORE-07"
        )
        for forbidden in TASK21_INTEGRATION_FORBIDDEN_TEXT:
            self.assertNotIn(forbidden.casefold(), integration_text.casefold())

    def _assert_core05_task21_audit_contract(
        self,
        reviews,
        *,
        integration_contracts=None,
        annual_variants=None,
        module_payload=None,
    ):
        integration_contracts = (
            integration_contracts or self.repository_integration_contracts
        )
        annual_variants = annual_variants or self.repository_annual_variants
        module_payload = module_payload or self.module_payload
        expected_ids, task_reviews = self._assert_audit_review_slice(
            reviews,
            start=PRE_TASK21_TIME_REVIEW_COUNT,
            expectations=TASK21_AUDIT_EXPECTATIONS,
            prior_sha256=PRE_TASK21_TIME_REVIEWS_SHA256,
        )
        core_contract, phase_minutes, integration = (
            self._assert_grade7_audit_context(
                expected_time_review_ids=expected_ids,
                module_id="IUM-7-CORE-05",
                integration_id="INT-7-NET-SECURITY",
                core_stable_sha256=TASK21_CORE05_STABLE_FIELDS_SHA256,
                integration_contract_sha256=(
                    TASK21_INTEGRATION_CONTRACT_SHA256
                ),
                annual_variants=annual_variants,
                integration_contracts=integration_contracts,
            )
        )
        self.assertEqual(
            (
                integration["moduleIds"],
                integration["pathIds"],
                integration["countedInModuleId"],
                integration["sharedMinutes"],
            ),
            (
                ["IUM-7-CORE-05", "IUM-7-CORE-06", "IUM-7-CORE-07"],
                ["optimized", "robust"],
                "IUM-7-CORE-07",
                135,
            ),
        )
        for budget in core_contract["pathBudgets"]:
            self.assertEqual(
                (budget["countedSharedMinutes"], budget["sharedAllocations"]),
                (0, []),
            )

        handoffs = {
            item["competencyId"]: item
            for item in self.remediation_payload["entries"]
        }
        coverage = {
            item["competencyId"]: item
            for item in self.coverage_payload["entries"]
        }
        module = next(
            item
            for item in module_payload["modules"]
            if item["id"] == "IUM-7-CORE-05"
        )
        evidence = {
            item["competencyId"]: item
            for item in module["coverageEvidence"]
        }
        reviews_by_competency_id = self._assert_audit_review_matrix(
            task_reviews,
            expectations=TASK21_AUDIT_EXPECTATIONS,
            module_id="IUM-7-CORE-05",
            handoffs=handoffs,
            coverage=coverage,
            evidence=evidence,
            cause_class="module-detail",
            evidence_mode="module-detail",
            evidence_visibility="teacher-observable",
        )
        for competency_id, expected_sha256 in (
            TASK21_REVIEW_TEXT_PROJECTION_SHA256.items()
        ):
            self._assert_canonical_projection(
                reviews_by_competency_id[competency_id],
                fields=("rationale", "risk", "followUp"),
                expected_sha256=expected_sha256,
            )
        self._assert_core05_task21_semantic_boundaries(
            evidence_by_competency_id=evidence,
            reviews_by_competency_id=reviews_by_competency_id,
            integration_contract=integration,
        )
        self._assert_fully_counted_phase_claims(
            task_reviews,
            phase_minutes_by_path=phase_minutes,
            expected_claims_by_phase={
                "guided-practice": 30,
                "review-revise-transfer": 30,
                "independent-action-product": 30,
            },
        )

    def test_repository_core05_task21_audit_contract(self):
        validate_time_reviews(
            self.time_payload["timeReviews"],
            self.remediation_payload,
            self.repository_module_contracts,
            self.repository_integration_contracts,
            self.repository_annual_variants,
            require_complete=False,
            privacy_contracts=self.repository_privacy_contracts,
        )
        self._assert_core05_task21_audit_contract(
            self.time_payload["timeReviews"]
        )

    def _task21_semantic_probe_inputs(self):
        module = next(
            item
            for item in self.module_payload["modules"]
            if item["id"] == "IUM-7-CORE-05"
        )
        evidence = {
            item["competencyId"]: copy.deepcopy(item)
            for item in module["coverageEvidence"]
            if item["competencyId"] in TASK21_AUDIT_EXPECTATIONS
        }
        reviews = {
            item["competencyId"]: copy.deepcopy(item)
            for item in self.time_payload["timeReviews"]
            if item["competencyId"] in TASK21_AUDIT_EXPECTATIONS
        }
        integration = copy.deepcopy(
            self.repository_integration_contracts["INT-7-NET-SECURITY"]
        )
        return evidence, reviews, integration

    def test_core05_task21_rejects_direct_semantic_contradictions(self):
        contradictions = {
            "INF7-16-GYM-IK-IGD-004": (
                "Allgemeine Sicherheitstipps genügen.",
                "Drei Risiko–Maßnahme-Paare genügen.",
                "Schutzwirkung und Grenze entfallen.",
                "Die Maßnahmen bieten vollständigen Schutz.",
                "Persönliche Geräte werden verändert.",
                "Gerätekennungen werden erhoben.",
                "Ein Teammitglied erstellt die Risiko–Maßnahme-Spur für alle.",
                "Integration verkürzt die IGD-004-Schutzhandlung.",
                "Die 135 Minuten werden in CORE-05 erneut gezählt.",
                "Personenprofil wird angelegt.",
            ),
            "INF7-16-GYM-PK-AB-002": (
                "Das Modell ist vereinfacht und das genügt.",
                "Ein Modell-Modell-Vergleich genügt.", "Beobachtung entfällt.",
                "Abweichung und Auslassung entfallen.", "Modellgrenze entfällt.",
                "Begründete Revision entfällt.", "Paketmitschnitt ist zulässig.",
                "Private Logs werden gespeichert.", "Zugangsdaten werden dokumentiert.",
                "Ein Teammitglied erstellt Tabelle und Revision für alle.",
                "Dasselbe Systemmodell absorbiert AB-002.",
                "Die 135 Minuten werden von AB-002 abgezogen.",
                "Das Jahresurteil bleibt nicht red.",
                "Automatische Punkte werden vergeben.",
            ),
            "INF7-16-GYM-PK-SV-001": (
                "Eine Simulation schließt SV-001.",
                "Eine Demonstration schließt SV-001.",
                "Eine Screenshotspur schließt SV-001.",
                "Eine kuratierte Ersatzspur schließt SV-001.",
                "Das Vorab-Freigabegate entfällt.",
                "Ohne lokale Konfiguration gilt der Record als geschlossen.",
                "Technische Anlaufzeit entfällt.", "IP-Adressen werden dokumentiert.",
                "Private Dateien werden erhoben.",
                "Ein Teammitglied führt die lokale Nutzung für alle aus.",
                "Derselbe Workflow integriert SV-001.",
                "Die 135 Minuten werden von SV-001 abgezogen.",
                "GRADE-7-OPTIMIZED-DEMAND ist ein verfügbarer 38-UE-Pfad.",
                "Automatisches Scoring wird eingesetzt.",
            ),
        }
        for competency_id, cases in contradictions.items():
            for contradiction in cases:
                self._assert_task21_semantic_contradiction(
                    competency_id, contradiction
                )

    def _assert_task21_semantic_contradiction(
        self, competency_id, contradiction
    ):
        with self.subTest(
            competency_id=competency_id,
            contradiction=contradiction,
        ):
            evidence, reviews, integration = (
                self._task21_semantic_probe_inputs()
            )
            reviews[competency_id]["followUp"] += f" {contradiction}"
            with self.assertRaises(AssertionError):
                self._assert_core05_task21_semantic_boundaries(
                    evidence_by_competency_id=evidence,
                    reviews_by_competency_id=reviews,
                    integration_contract=integration,
                )

    def test_core05_task21_rejects_local_execution_substitutes_semantically(self):
        mutations = (
            ("executionType", "actual-local-use", "simulated-local-use"),
            (
                "localConfigurationRequirement",
                "bleibt der Record partial",
                "gilt der Record als geschlossen",
            ),
        )
        for field, old, new in mutations:
            with self.subTest(field=field, replacement=new):
                evidence, reviews, integration = (
                    self._task21_semantic_probe_inputs()
                )
                sv_evidence = evidence["INF7-16-GYM-PK-SV-001"]
                sv_evidence[field] = sv_evidence[field].replace(old, new)
                with self.assertRaises(AssertionError):
                    self._assert_core05_task21_semantic_boundaries(
                        evidence_by_competency_id=evidence,
                        reviews_by_competency_id=reviews,
                        integration_contract=integration,
                    )

    def test_core05_task21_rejects_integration_overreach_semantically(self):
        overreaches = (
            (
                "sharedPhaseOrProduct",
                " Modell–Realsituation-Vergleich wird gemeinsam getragen.",
            ),
            (
                "sharedPhaseOrProduct",
                " Tatsächliche lokale Schulnetznutzung wird gemeinsam getragen.",
            ),
            (
                "preservedProductAndCurriculumEvidence",
                "Kompetenznachweise INF7-16-GYM-PK-AB-002 und "
                "INF7-16-GYM-PK-SV-001.",
            ),
            (
                "sharedPhaseOrProduct",
                " Gemeinsames Modell ersetzt Beobachtung und Revision.",
            ),
            (
                "sharedPhaseOrProduct",
                " Gemeinsamer Datenweg ersetzt die tatsächliche lokale "
                "Ausführung.",
            ),
        )
        for field, overreach in overreaches:
            with self.subTest(integration_field=field, overreach=overreach):
                evidence, reviews, integration = (
                    self._task21_semantic_probe_inputs()
                )
                if isinstance(integration[field], list):
                    integration[field].append(overreach)
                else:
                    integration[field] += overreach
                with self.assertRaises(AssertionError):
                    self._assert_core05_task21_semantic_boundaries(
                        evidence_by_competency_id=evidence,
                        reviews_by_competency_id=reviews,
                        integration_contract=integration,
                    )

        for field, value in (
            ("countedInModuleId", "IUM-7-CORE-05"),
            ("sharedMinutes", 270),
        ):
            with self.subTest(integration_field=field, value=value):
                evidence, reviews, integration = (
                    self._task21_semantic_probe_inputs()
                )
                integration[field] = value
                with self.assertRaises(AssertionError):
                    self._assert_core05_task21_semantic_boundaries(
                        evidence_by_competency_id=evidence,
                        reviews_by_competency_id=reviews,
                        integration_contract=integration,
                    )

        evidence, reviews, integration = self._task21_semantic_probe_inputs()
        integration["preservedLearningActions"][0] = integration[
            "preservedLearningActions"
        ][0].replace(
            "Bedrohung und begründete Schutzmaßnahme",
            "Bedrohung ohne eigene Schutzhandlung",
        )
        with self.assertRaises(AssertionError):
            self._assert_core05_task21_semantic_boundaries(
                evidence_by_competency_id=evidence,
                reviews_by_competency_id=reviews,
                integration_contract=integration,
            )

    def test_core05_task21_rejects_noncanonical_review_text_projection(self):
        self.assertEqual(len(TASK21_REVIEW_TEXT_PROJECTION_SHA256), 3)
        for competency_id in TASK21_AUDIT_EXPECTATIONS:
            with self.subTest(competency_id=competency_id):
                reviews = copy.deepcopy(self.time_payload["timeReviews"])
                next(
                    item
                    for item in reviews
                    if item["competencyId"] == competency_id
                )["risk"] += " Beliebige Ergänzung."
                with self.assertRaises(AssertionError):
                    self._assert_core05_task21_audit_contract(reviews)

    def test_core05_task21_contract_allows_later_review(self):
        reviews = copy.deepcopy(self.time_payload["timeReviews"])
        reviews.append(
            {"id": "TR-LATER-TASK21", "competencyId": "LATER-TASK21"}
        )
        self._assert_core05_task21_audit_contract(reviews)

    def test_core05_task21_contract_rejects_duplicate_id(self):
        reviews = copy.deepcopy(self.time_payload["timeReviews"])
        reviews.append(copy.deepcopy(reviews[PRE_TASK21_TIME_REVIEW_COUNT]))
        with self.assertRaises(AssertionError):
            self._assert_core05_task21_audit_contract(reviews)

    def test_core05_task21_rejects_matrix_path_and_phase_mutations(self):
        review_mutations = (
            ("INF7-16-GYM-IK-IGD-004", "decision", "additional-time"),
            (
                "INF7-16-GYM-IK-IGD-004",
                "pathAvailability",
                GRADE7_DEMAND_PATH_AVAILABILITY,
            ),
            (
                "INF7-16-GYM-PK-AB-002",
                "integrationContractIds",
                ["INT-7-NET-SECURITY"],
            ),
            ("INF7-16-GYM-PK-AB-002", "phaseIds", ["guided-practice"]),
            ("INF7-16-GYM-PK-SV-001", "additionalMinutes", 0),
            ("INF7-16-GYM-PK-SV-001", "decision", "integrated"),
        )
        for competency_id, field, value in review_mutations:
            with self.subTest(review_matrix=(competency_id, field)):
                reviews = copy.deepcopy(self.time_payload["timeReviews"])
                next(
                    item
                    for item in reviews
                    if item["competencyId"] == competency_id
                )[field] = value
                with self.assertRaises(AssertionError):
                    self._assert_core05_task21_audit_contract(reviews)

        for variant_id, field, value in (
            ("GRADE-7-OPTIMIZED-DEMAND", "available", True),
            ("GRADE-7-ROBUST-DEMAND", "targetUnits", 38),
        ):
            with self.subTest(variant=(variant_id, field)):
                variants = copy.deepcopy(self.repository_annual_variants)
                variants[variant_id][field] = value
                with self.assertRaises(AssertionError):
                    self._assert_core05_task21_audit_contract(
                        self.time_payload["timeReviews"],
                        annual_variants=variants,
                    )

        task_reviews = copy.deepcopy(
            self.time_payload["timeReviews"][PRE_TASK21_TIME_REVIEW_COUNT:52]
        )
        next(
            item
            for item in task_reviews
            if item["competencyId"] == "INF7-16-GYM-IK-IGD-004"
        )["additionalMinutes"] = 40
        core_contract = self.repository_module_contracts["IUM-7-CORE-05"]
        phase_minutes = self._assert_grade7_demand_scenarios(
            self.repository_annual_variants,
            core_contract,
            module_id="IUM-7-CORE-05",
            integration_id="INT-7-NET-SECURITY",
        )
        with self.assertRaises(AssertionError):
            self._assert_fully_counted_phase_claims(
                task_reviews,
                phase_minutes_by_path=phase_minutes,
                expected_claims_by_phase={
                    "guided-practice": 40,
                    "review-revise-transfer": 30,
                    "independent-action-product": 30,
                },
            )

    def _assert_core08_task22_semantic_boundaries(
        self,
        *,
        evidence_by_competency_id,
        reviews_by_competency_id,
        integration_contract,
        privacy_contract,
    ):
        for competency_id, review in reviews_by_competency_id.items():
            evidence = evidence_by_competency_id.get(competency_id, {})
            evidence_text = " ".join(
                str(evidence[field])
                for field in (
                    "learningAction",
                    "productEvidence",
                    "privacyBoundary",
                    "nonPersonalFollowUp",
                )
                if field in evidence
            )
            review_text = " ".join(
                review[field] for field in ("rationale", "risk", "followUp")
            )
            audit_text = f"{evidence_text} {review_text}"
            for anchor in TASK22_REQUIRED_TEXT[competency_id]:
                self.assertIn(anchor, audit_text)
            for forbidden in TASK22_FORBIDDEN_TEXT[competency_id]:
                self.assertNotIn(forbidden.casefold(), audit_text.casefold())
            for anchor in (
                "nicht verfügbare Bedarfsszenarien",
                "Jahresurteil",
                "red",
                "Personenprofil",
                "automatische Punkte",
                "automatisches Scoring",
            ):
                semantic_probe = (
                    "automatisch" if anchor == "automatische Punkte" else anchor
                )
                self.assertIn(semantic_probe.casefold(), review_text.casefold())
            for false_release in (
                "ist ein verfügbarer 38-ue-pfad",
                "ist ein grüner 38-ue-pfad",
                "ist ein freigegebener 38-ue-pfad",
                "jahresurteil bleibt nicht red",
                "personenprofil wird angelegt",
                "automatische punkte werden vergeben",
                "automatisches scoring wird eingesetzt",
            ):
                self.assertNotIn(false_release, review_text.casefold())

            disposition = review["privacyDisposition"]
            self.assertEqual(
                (
                    disposition["contractId"],
                    disposition["observableBasis"],
                    disposition["evidenceContractId"],
                    set(disposition["privateArtifactContribution"].values()),
                    disposition["privateActivityTimeTreatment"],
                ),
                (
                    "PC-IUM-7-CORE-08",
                    TASK22_PRIVACY_EXPECTATIONS[competency_id][0],
                    TASK22_PRIVACY_EXPECTATIONS[competency_id][1],
                    {"excluded"},
                    "module-budget-only",
                ),
            )

        dp_evidence = evidence_by_competency_id["LH26-E-DP-013"]
        self.assertEqual(dp_evidence["privacyBoundary"], PRIVATE_LOCAL_BOUNDARY)
        self.assertIn("ohne Kenntnis der privaten Notiz", dp_evidence["nonPersonalFollowUp"])
        self.assertIn(
            "keine persönliche Handlungsoption als Abgabe",
            dp_evidence["nonPersonalFollowUp"],
        )
        self.assertEqual(privacy_contract, TASK22_PRIVACY_CONTRACT)

        integration_text = " ".join(
            [integration_contract["sharedPhaseOrProduct"]]
            + integration_contract["preservedLearningActions"]
            + integration_contract["preservedProductAndCurriculumEvidence"]
            + integration_contract["prerequisites"]
            + [integration_contract["risk"], integration_contract["fallback"]]
        )
        for anchor in (
            "INF7-16-GYM-PK-AB-005",
            "INF7-16-GYM-PK-KK-006",
        ):
            self.assertIn(anchor, integration_text)
        for forbidden in TASK22_INTEGRATION_FORBIDDEN_TEXT:
            self.assertNotIn(forbidden.casefold(), integration_text.casefold())
        self.assertEqual(
            (
                integration_contract["countedInModuleId"],
                integration_contract["sharedMinutes"],
                integration_contract["savingsMinutesByPath"],
            ),
            ("IUM-7-CORE-10", 45, {"optimized": 270, "robust": 45}),
        )

    def _assert_core08_task22_audit_contract(
        self,
        reviews,
        *,
        integration_contracts=None,
        annual_variants=None,
        module_payload=None,
        coverage_payload=None,
        privacy_contracts=None,
        sequence_evidence=None,
    ):
        integration_contracts = (
            integration_contracts or self.repository_integration_contracts
        )
        annual_variants = annual_variants or self.repository_annual_variants
        module_payload = module_payload or self.module_payload
        coverage_payload = coverage_payload or self.coverage_payload
        privacy_contracts = privacy_contracts or self.repository_privacy_contracts
        sequence_evidence = (
            self.time_payload["sequenceEvidence"]
            if sequence_evidence is None
            else sequence_evidence
        )
        expected_ids, task_reviews = self._assert_audit_review_slice(
            reviews,
            start=PRE_TASK22_TIME_REVIEW_COUNT,
            expectations=TASK22_AUDIT_EXPECTATIONS,
            prior_sha256=PRE_TASK22_TIME_REVIEWS_SHA256,
        )
        core_contract, phase_minutes, integration = (
            self._assert_grade7_audit_context(
                expected_time_review_ids=expected_ids,
                module_id="IUM-7-CORE-08",
                integration_id="INT-7-DATA-MEDIA-SOCIETY",
                core_stable_sha256=TASK22_CORE08_STABLE_FIELDS_SHA256,
                integration_contract_sha256=TASK22_INTEGRATION_CONTRACT_SHA256,
                annual_variants=annual_variants,
                integration_contracts=integration_contracts,
            )
        )
        for budget in core_contract["pathBudgets"]:
            self.assertEqual(
                (budget["countedSharedMinutes"], budget["sharedAllocations"]),
                (0, []),
            )

        handoffs = {
            item["competencyId"]: item
            for item in self.remediation_payload["entries"]
        }
        coverage = {
            item["competencyId"]: item
            for item in coverage_payload["entries"]
        }
        module = next(
            item
            for item in module_payload["modules"]
            if item["id"] == "IUM-7-CORE-08"
        )
        evidence = {
            item["competencyId"]: item for item in module["coverageEvidence"]
        }
        reviews_by_competency_id = self._assert_audit_review_matrix(
            task_reviews,
            expectations=TASK22_AUDIT_EXPECTATIONS,
            module_id="IUM-7-CORE-08",
            handoffs=handoffs,
            coverage=coverage,
            evidence=evidence,
            cause_class="module-detail",
            evidence_mode="module-detail",
            evidence_visibility="shared",
        )

        self.assertEqual(set(privacy_contracts), {
            "PC-IUM-5-CORE-07",
            "PC-IUM-7-CORE-08",
            "PC-IUM-7-CORE-10",
        })
        self.assertEqual(
            self._canonical_sha256(privacy_contracts["PC-IUM-5-CORE-07"]),
            PRE_TASK22_CORE07_PRIVACY_CONTRACT_SHA256,
        )
        self.assertEqual(
            privacy_contracts["PC-IUM-7-CORE-08"],
            TASK22_PRIVACY_CONTRACT,
        )
        self.assertEqual(
            self._canonical_sha256(sequence_evidence),
            TASK24_SEQUENCE_EVIDENCE_SHA256,
        )
        self.assertEqual(len(TASK22_REVIEW_TEXT_PROJECTION_SHA256), 7)
        for competency_id, expected_sha256 in (
            TASK22_REVIEW_TEXT_PROJECTION_SHA256.items()
        ):
            self._assert_canonical_projection(
                reviews_by_competency_id[competency_id],
                fields=("rationale", "risk", "followUp"),
                expected_sha256=expected_sha256,
            )
        self._assert_core08_task22_semantic_boundaries(
            evidence_by_competency_id=evidence,
            reviews_by_competency_id=reviews_by_competency_id,
            integration_contract=integration,
            privacy_contract=privacy_contracts["PC-IUM-7-CORE-08"],
        )
        self._assert_fully_counted_phase_claims(
            task_reviews,
            phase_minutes_by_path=phase_minutes,
            expected_claims_by_phase={
                "build-concept": 20,
                "independent-action-product": 25,
                "review-revise-transfer": 35,
                "guided-practice": 25,
            },
        )

    def _validate_repository_time_reviews(
        self,
        reviews,
        *,
        privacy_contracts=None,
    ):
        return validate_time_reviews(
            reviews,
            self.remediation_payload,
            self.repository_module_contracts,
            self.repository_integration_contracts,
            self.repository_annual_variants,
            require_complete=False,
            privacy_contracts=(
                self.repository_privacy_contracts
                if privacy_contracts is None
                else privacy_contracts
            ),
        )

    def test_repository_core08_task22_audit_contract(self):
        self._validate_repository_time_reviews(self.time_payload["timeReviews"])
        self._assert_core08_task22_audit_contract(
            self.time_payload["timeReviews"]
        )

    def test_repository_core08_task22_privacy_contract_enables_dp013_review(self):
        competency_id = "LH26-E-DP-013"
        review = next(
            item for item in self.time_payload["timeReviews"]
            if item["competencyId"] == competency_id
        )
        result = self._validate_repository_time_reviews([review])

        self.assertEqual(set(result), {f"TR-{competency_id}"})

    def _task22_semantic_probe_inputs(self):
        module = next(
            item
            for item in self.module_payload["modules"]
            if item["id"] == "IUM-7-CORE-08"
        )
        evidence = {
            item["competencyId"]: copy.deepcopy(item)
            for item in module["coverageEvidence"]
            if item["competencyId"] in TASK22_AUDIT_EXPECTATIONS
        }
        reviews = {
            item["competencyId"]: copy.deepcopy(item)
            for item in self.time_payload["timeReviews"]
            if item["competencyId"] in TASK22_AUDIT_EXPECTATIONS
        }
        integration = copy.deepcopy(
            self.repository_integration_contracts[
                "INT-7-DATA-MEDIA-SOCIETY"
            ]
        )
        privacy = copy.deepcopy(
            self.repository_privacy_contracts["PC-IUM-7-CORE-08"]
        )
        return evidence, reviews, integration, privacy

    def _assert_task22_semantic_failure(
        self,
        evidence,
        reviews,
        integration,
        privacy,
    ):
        with self.assertRaises(AssertionError):
            self._assert_core08_task22_semantic_boundaries(
                evidence_by_competency_id=evidence,
                reviews_by_competency_id=reviews,
                integration_contract=integration,
                privacy_contract=privacy,
            )

    def _assert_task22_review_text_failure(self, competency_id, text):
        evidence, reviews, integration, privacy = (
            self._task22_semantic_probe_inputs()
        )
        reviews[competency_id]["followUp"] += f" {text}"
        self._assert_task22_semantic_failure(
            evidence, reviews, integration, privacy
        )

    def test_core08_task22_rejects_direct_semantic_contradictions(self):
        for competency_id, contradictions in TASK22_FORBIDDEN_TEXT.items():
            for contradiction in contradictions:
                with self.subTest(
                    competency_id=competency_id,
                    contradiction=contradiction,
                ):
                    self._assert_task22_review_text_failure(
                        competency_id, f"{contradiction.capitalize()}."
                    )

        common_contradictions = (
            (
                "INF7-16-GYM-IK-IGD-006",
                "GRADE-7-OPTIMIZED-DEMAND ist ein verfügbarer 38-UE-Pfad.",
            ),
            (
                "INF7-16-GYM-PK-AB-005",
                "GRADE-7-OPTIMIZED-DEMAND ist ein grüner 38-UE-Pfad.",
            ),
            (
                "LH26-E-PROG-003",
                "GRADE-7-OPTIMIZED-DEMAND ist ein freigegebener 38-UE-Pfad.",
            ),
            ("LH26-E-PROG-004", "Jahresurteil bleibt nicht red."),
        )
        for competency_id, contradiction in common_contradictions:
            with self.subTest(
                competency_id=competency_id,
                path_contradiction=contradiction,
            ):
                self._assert_task22_review_text_failure(
                    competency_id, contradiction
                )

    def test_core08_task22_rejects_integration_overreach_semantically(self):
        text_overreaches = (
            (
                "preservedProductAndCurriculumEvidence",
                "INF7-16-GYM-IK-IGD-006 wird vollständig bewahrt.",
            ),
            (
                "preservedProductAndCurriculumEvidence",
                "INF7-16-GYM-PK-AB-006 und LH26-E-DP-013 werden bewahrt.",
            ),
            (
                "preservedProductAndCurriculumEvidence",
                "LH26-E-PROG-003 und LH26-E-PROG-004 werden bewahrt.",
            ),
            (
                "sharedPhaseOrProduct",
                "Die Mechanismuskarte ersetzt Auswirkungen und Perspektiven.",
            ),
            (
                "sharedPhaseOrProduct",
                "Allgemeine Vielfaltserwähnung ersetzt die informatische "
                "Vielfaltsfrage.",
            ),
        )
        for field, overreach in text_overreaches:
            with self.subTest(field=field, overreach=overreach):
                evidence, reviews, integration, privacy = (
                    self._task22_semantic_probe_inputs()
                )
                if isinstance(integration[field], list):
                    integration[field].append(overreach)
                else:
                    integration[field] += f" {overreach}"
                self._assert_task22_semantic_failure(
                    evidence, reviews, integration, privacy
                )

        for field, value in (
            ("countedInModuleId", "IUM-7-CORE-08"),
            ("sharedMinutes", 270),
            ("savingsMinutesByPath", {"optimized": 45, "robust": 45}),
        ):
            with self.subTest(field=field, value=value):
                evidence, reviews, integration, privacy = (
                    self._task22_semantic_probe_inputs()
                )
                integration[field] = value
                self._assert_task22_semantic_failure(
                    evidence, reviews, integration, privacy
                )

    def test_core08_task22_privacy_mutations_fail_closed_in_validator(self):
        time_payload = copy.deepcopy(self.time_payload)
        without_core08 = [
            contract
            for contract in time_payload["privacyContracts"]
            if contract["id"] != "PC-IUM-7-CORE-08"
        ]
        privacy_contracts = validate_privacy_contracts(
            without_core08,
            self.repository_module_contracts,
        )
        with self.assertRaisesRegex(
            IUM10ValidationError,
            "private-local time review needs privacy contract",
        ):
            self._validate_repository_time_reviews(
                [next(
                    review for review in time_payload["timeReviews"]
                    if review["competencyId"] == "LH26-E-DP-013"
                )],
                privacy_contracts=privacy_contracts,
            )

        for handling in (
            "access", "observation", "collection", "transfer", "storage",
            "assessment",
        ):
            with self.subTest(institutional_handling=handling):
                contracts = copy.deepcopy(self.time_payload["privacyContracts"])
                next(
                    item for item in contracts
                    if item["id"] == "PC-IUM-7-CORE-08"
                )["institutionalHandling"][handling] = "allowed"
                with self.assertRaises(IUM10ValidationError):
                    validate_privacy_contracts(
                        contracts,
                        self.repository_module_contracts,
                    )

        disposition_mutations = (
            ("missing disposition", None, None),
            ("wrong contract", "contractId", "PC-WRONG"),
            ("wrong basis", "observableBasis", "nonpersonal-follow-up"),
            ("wrong evidence", "evidenceContractId", "CE-WRONG"),
            ("product included", "privateArtifactContribution.product", "included"),
            ("evidence included", "privateArtifactContribution.evidence", "included"),
            (
                "time included",
                "privateArtifactContribution.additionalTimeClaim",
                "included",
            ),
            ("other time treatment", "privateActivityTimeTreatment", "separate"),
        )
        for label, field, value in disposition_mutations:
            with self.subTest(disposition=label):
                payload = copy.deepcopy(self.time_payload)
                review = next(
                    item for item in payload["timeReviews"]
                    if item["competencyId"] == "INF7-16-GYM-IK-IGD-006"
                )
                if field is None:
                    del review["privacyDisposition"]
                elif field.startswith("privateArtifactContribution."):
                    nested = field.split(".", 1)[1]
                    review["privacyDisposition"][
                        "privateArtifactContribution"
                    ][nested] = value
                else:
                    review["privacyDisposition"][field] = value
                privacy_contracts = validate_privacy_contracts(
                    payload["privacyContracts"],
                    self.repository_module_contracts,
                )
                with self.assertRaises(IUM10ValidationError):
                    self._validate_repository_time_reviews(
                        payload["timeReviews"],
                        privacy_contracts=privacy_contracts,
                    )

    def test_core08_task22_rejects_matrix_progression_and_path_mutations(self):
        review_mutations = (
            ("INF7-16-GYM-IK-IGD-006", "decision", "integrated"),
            (
                "INF7-16-GYM-PK-AB-005", "pathAvailability",
                GRADE7_DEMAND_PATH_AVAILABILITY,
            ),
            (
                "INF7-16-GYM-PK-AB-006", "integrationContractIds",
                ["INT-7-DATA-MEDIA-SOCIETY"],
            ),
            ("INF7-16-GYM-PK-KK-006", "phaseIds", ["build-concept"]),
            ("LH26-E-DP-013", "additionalMinutes", 0),
            ("LH26-E-PROG-003", "phaseIds", ["build-concept"]),
            ("LH26-E-PROG-003", "additionalMinutes", 5),
            (
                "LH26-E-PROG-004", "pathAvailability",
                GRADE7_DEMAND_PATH_AVAILABILITY,
            ),
            (
                "LH26-E-PROG-004", "integrationContractIds",
                ["INT-7-DATA-MEDIA-SOCIETY"],
            ),
            ("LH26-E-PROG-004", "sequenceEvidenceId", "SE-WRONG"),
        )
        for competency_id, field, value in review_mutations:
            with self.subTest(competency_id=competency_id, field=field):
                reviews = copy.deepcopy(self.time_payload["timeReviews"])
                next(
                    item for item in reviews
                    if item["competencyId"] == competency_id
                )[field] = value
                with self.assertRaises(AssertionError):
                    self._assert_core08_task22_audit_contract(reviews)

        coverage_payload = copy.deepcopy(self.coverage_payload)
        next(
            item for item in coverage_payload["entries"]
            if item["competencyId"] == "LH26-E-PROG-003"
        )["coverageStatus"] = "covered"
        with self.assertRaises(AssertionError):
            self._assert_core08_task22_audit_contract(
                self.time_payload["timeReviews"],
                coverage_payload=coverage_payload,
            )

        sequence_evidence = [{
            "id": "SE-LH26-E-PROG-003",
            "competencyId": "LH26-E-PROG-003",
        }]
        with self.assertRaises(AssertionError):
            self._assert_core08_task22_audit_contract(
                self.time_payload["timeReviews"],
                sequence_evidence=sequence_evidence,
            )

        for variant_id, field, value in (
            ("GRADE-7-OPTIMIZED-DEMAND", "available", True),
            ("GRADE-7-ROBUST-DEMAND", "targetUnits", 38),
        ):
            with self.subTest(variant=variant_id, field=field):
                variants = copy.deepcopy(self.repository_annual_variants)
                variants[variant_id][field] = value
                with self.assertRaises(AssertionError):
                    self._assert_core08_task22_audit_contract(
                        self.time_payload["timeReviews"],
                        annual_variants=variants,
                    )

    def test_core08_task22_audit_contract_invokes_semantic_boundaries(self):
        module_payload = copy.deepcopy(self.module_payload)
        module = next(
            item for item in module_payload["modules"]
            if item["id"] == "IUM-7-CORE-08"
        )
        evidence = next(
            item for item in module["coverageEvidence"]
            if item["competencyId"] == "LH26-E-DP-013"
        )
        evidence["nonPersonalFollowUp"] += (
            " Der gemeinsame Abschnitt benötigt Kenntnis der Privatnotiz."
        )
        with self.assertRaises(AssertionError):
            self._assert_core08_task22_audit_contract(
                self.time_payload["timeReviews"],
                module_payload=module_payload,
            )

    def test_core08_task22_rejects_noncanonical_review_text_projection(self):
        self.assertEqual(len(TASK22_REVIEW_TEXT_PROJECTION_SHA256), 7)
        for competency_id in TASK22_AUDIT_EXPECTATIONS:
            with self.subTest(competency_id=competency_id):
                reviews = copy.deepcopy(self.time_payload["timeReviews"])
                next(
                    item for item in reviews
                    if item["competencyId"] == competency_id
                )["risk"] += " Beliebige Ergänzung."
                with self.assertRaises(AssertionError):
                    self._assert_core08_task22_audit_contract(reviews)

    def test_core08_task22_contract_allows_later_review_and_rejects_duplicate(self):
        reviews = copy.deepcopy(self.time_payload["timeReviews"])
        reviews.append({"id": "TR-LATER-TASK22", "competencyId": "LATER-TASK22"})
        self._assert_core08_task22_audit_contract(reviews)

        reviews = copy.deepcopy(self.time_payload["timeReviews"])
        reviews.append(copy.deepcopy(reviews[PRE_TASK22_TIME_REVIEW_COUNT]))
        with self.assertRaises(AssertionError):
            self._assert_core08_task22_audit_contract(reviews)

    def _assert_core10_task23_semantic_boundaries(
        self,
        *,
        evidence,
        review,
        integration_contract,
        privacy_contract,
    ):
        evidence_text = " ".join(
            str(evidence[field])
            for field in (
                "learningAction",
                "productEvidence",
                "privacyBoundary",
                "observationBoundary",
                "nonPersonalFollowUp",
            )
        )
        review_text = " ".join(
            review[field] for field in ("rationale", "risk", "followUp")
        )
        audit_text = f"{evidence_text} {review_text}"
        for anchor in TASK23_REQUIRED_TEXT:
            self.assertIn(anchor.casefold(), audit_text.casefold())
        for forbidden in TASK23_FORBIDDEN_TEXT:
            self.assertNotIn(forbidden, audit_text.casefold())

        self.assertEqual(evidence["privacyBoundary"], PRIVATE_LOCAL_BOUNDARY)
        self.assertEqual(
            evidence["observationBoundary"],
            "Die Privatnotiz wird weder geöffnet noch beobachtet, inhaltlich "
            "besprochen, vorgelegt oder in ihrer Erstellung bestätigt oder "
            "kontrolliert.",
        )
        self.assertIn(
            "Diese Anschlussaufgabe funktioniert ohne Kenntnis, Vorlage, "
            "Bestätigung oder Besprechung der privaten Reflexionsnotiz",
            evidence["nonPersonalFollowUp"],
        )
        self.assertIn(
            "ist kein Nachweis der Reflexion der eigenen Selbstwahrnehmung",
            evidence["nonPersonalFollowUp"],
        )

        disposition = review["privacyDisposition"]
        self.assertEqual(
            disposition,
            {
                "contractId": "PC-IUM-7-CORE-10",
                "observableBasis": "nonpersonal-follow-up",
                "evidenceContractId": "CE-IUM-7-CORE-10-LH26-E-DP-014",
                "privateArtifactContribution": {
                    "product": "excluded",
                    "evidence": "excluded",
                    "additionalTimeClaim": "excluded",
                },
                "privateActivityTimeTreatment": "module-budget-only",
            },
        )
        self.assertEqual(privacy_contract, TASK23_PRIVACY_CONTRACT)

        integration_text = " ".join(
            [integration_contract["sharedPhaseOrProduct"]]
            + integration_contract["preservedLearningActions"]
            + integration_contract["preservedProductAndCurriculumEvidence"]
            + integration_contract["prerequisites"]
            + [integration_contract["risk"], integration_contract["fallback"]]
        )
        self.assertNotIn("LH26-E-DP-014", integration_text)
        self.assertEqual(
            (
                integration_contract["countedInModuleId"],
                integration_contract["sharedMinutes"],
                integration_contract["savingsMinutesByPath"],
            ),
            ("IUM-7-CORE-10", 45, {"optimized": 270, "robust": 45}),
        )

    def _assert_core10_task23_audit_contract(
        self,
        reviews,
        *,
        annual_variants=None,
        integration_contracts=None,
        module_contracts=None,
        module_payload=None,
        coverage_payload=None,
        privacy_contracts=None,
        sequence_evidence=None,
    ):
        annual_variants = (
            self.repository_annual_variants
            if annual_variants is None
            else annual_variants
        )
        integration_contracts = (
            self.repository_integration_contracts
            if integration_contracts is None
            else integration_contracts
        )
        module_contracts = (
            self.repository_module_contracts
            if module_contracts is None
            else module_contracts
        )
        module_payload = self.module_payload if module_payload is None else module_payload
        coverage_payload = (
            self.coverage_payload
            if coverage_payload is None
            else coverage_payload
        )
        privacy_contracts = (
            self.repository_privacy_contracts
            if privacy_contracts is None
            else privacy_contracts
        )
        sequence_evidence = (
            self.time_payload["sequenceEvidence"]
            if sequence_evidence is None
            else sequence_evidence
        )

        expected_ids, task_reviews = self._assert_audit_review_slice(
            reviews,
            start=PRE_TASK23_TIME_REVIEW_COUNT,
            expectations=TASK23_AUDIT_EXPECTATIONS,
            prior_sha256=PRE_TASK23_TIME_REVIEWS_SHA256,
        )
        core_contract, phase_minutes, integration = (
            self._assert_grade7_audit_context(
                expected_time_review_ids=expected_ids,
                module_id="IUM-7-CORE-10",
                integration_id="INT-7-DATA-MEDIA-SOCIETY",
                core_stable_sha256=TASK23_CORE10_STABLE_FIELDS_SHA256,
                integration_contract_sha256=(
                    TASK23_INTEGRATION_CONTRACT_SHA256
                ),
                annual_variants=annual_variants,
                integration_contracts=integration_contracts,
                module_contracts=module_contracts,
            )
        )
        self.assertEqual(
            [
                (
                    budget["pathId"],
                    budget["minutes"],
                    budget["directMinutes"],
                    budget["countedSharedMinutes"],
                    budget["sharedAllocations"],
                )
                for budget in core_contract["pathBudgets"]
            ],
            [
                (
                    "optimized", 180, 135, 45,
                    [{
                        "integrationContractId":
                            "INT-7-DATA-MEDIA-SOCIETY",
                        "minutes": 45,
                    }],
                ),
                (
                    "robust", 270, 225, 45,
                    [{
                        "integrationContractId":
                            "INT-7-DATA-MEDIA-SOCIETY",
                        "minutes": 45,
                    }],
                ),
                ("historical-minimum", 270, 270, 0, []),
            ],
        )

        handoffs = {
            item["competencyId"]: item
            for item in self.remediation_payload["entries"]
        }
        coverage = {
            item["competencyId"]: item
            for item in coverage_payload["entries"]
        }
        module = next(
            item
            for item in module_payload["modules"]
            if item["id"] == "IUM-7-CORE-10"
        )
        evidence = {
            item["competencyId"]: item for item in module["coverageEvidence"]
        }
        reviews_by_competency_id = self._assert_audit_review_matrix(
            task_reviews,
            expectations=TASK23_AUDIT_EXPECTATIONS,
            module_id="IUM-7-CORE-10",
            handoffs=handoffs,
            coverage=coverage,
            evidence=evidence,
            cause_class="private-local",
            evidence_mode="private-local",
            evidence_visibility="private-local",
        )

        self.assertEqual(
            list(privacy_contracts),
            [
                "PC-IUM-5-CORE-07",
                "PC-IUM-7-CORE-08",
                "PC-IUM-7-CORE-10",
            ],
        )
        self.assertEqual(
            self._canonical_sha256(list(privacy_contracts.values())[:2]),
            PRE_TASK23_PRIVACY_CONTRACTS_SHA256,
        )
        self.assertEqual(
            privacy_contracts["PC-IUM-7-CORE-10"],
            TASK23_PRIVACY_CONTRACT,
        )
        self.assertEqual(
            self._canonical_sha256(sequence_evidence),
            TASK24_SEQUENCE_EVIDENCE_SHA256,
        )

        review = reviews_by_competency_id["LH26-E-DP-014"]
        self._assert_canonical_projection(
            review,
            fields=("rationale", "risk", "followUp"),
            expected_sha256=TASK23_REVIEW_TEXT_PROJECTION_SHA256,
        )
        self._assert_core10_task23_semantic_boundaries(
            evidence=evidence["LH26-E-DP-014"],
            review=review,
            integration_contract=integration,
            privacy_contract=privacy_contracts["PC-IUM-7-CORE-10"],
        )
        self._assert_fully_counted_phase_claims(
            task_reviews,
            phase_minutes_by_path=phase_minutes,
            expected_claims_by_phase={"review-revise-transfer": 20},
        )

    def test_repository_core10_task23_audit_contract(self):
        self._validate_repository_time_reviews(self.time_payload["timeReviews"])
        self._assert_core10_task23_audit_contract(
            self.time_payload["timeReviews"]
        )

    def test_repository_core10_task23_privacy_contract_enables_dp014_review(self):
        competency_id = "LH26-E-DP-014"
        review = next(
            item for item in self.time_payload["timeReviews"]
            if item["competencyId"] == competency_id
        )
        result = self._validate_repository_time_reviews([review])

        self.assertEqual(set(result), {f"TR-{competency_id}"})

    def _task23_semantic_probe_inputs(self):
        module = next(
            item
            for item in self.module_payload["modules"]
            if item["id"] == "IUM-7-CORE-10"
        )
        evidence = copy.deepcopy(next(
            item for item in module["coverageEvidence"]
            if item["competencyId"] == "LH26-E-DP-014"
        ))
        review = copy.deepcopy(next(
            item for item in self.time_payload["timeReviews"]
            if item["competencyId"] == "LH26-E-DP-014"
        ))
        integration = copy.deepcopy(
            self.repository_integration_contracts[
                "INT-7-DATA-MEDIA-SOCIETY"
            ]
        )
        privacy = copy.deepcopy(
            self.repository_privacy_contracts["PC-IUM-7-CORE-10"]
        )
        return evidence, review, integration, privacy

    def test_core10_task23_rejects_private_proxies_and_integration_overreach(self):
        contradictions = (
            "Die Privatnotiz ist Produkt.",
            "Fertigstellung wird protokolliert.",
            "Teilnahme wird beobachtet.",
            "Der sichtbare Anschluss benötigt Kenntnis der Privatnotiz.",
            "INT-7-DATA-MEDIA-SOCIETY integriert DP-014.",
            "Die 45 gemeinsamen Minuten werden erneut gezählt.",
            "Die 270-Minuten-Einsparung ist zusätzlicher Zeitvorrat.",
            "GRADE-7-OPTIMIZED-DEMAND ist ein verfügbarer 38-UE-Pfad.",
        )
        for contradiction in contradictions:
            with self.subTest(contradiction=contradiction):
                evidence, review, integration, privacy = (
                    self._task23_semantic_probe_inputs()
                )
                review["risk"] += f" {contradiction}"
                with self.assertRaises(AssertionError):
                    self._assert_core10_task23_semantic_boundaries(
                        evidence=evidence,
                        review=review,
                        integration_contract=integration,
                        privacy_contract=privacy,
                    )

        evidence, review, integration, privacy = (
            self._task23_semantic_probe_inputs()
        )
        evidence["nonPersonalFollowUp"] += (
            " Der sichtbare Anschluss benötigt Kenntnis der Privatnotiz."
        )
        with self.assertRaises(AssertionError):
            self._assert_core10_task23_semantic_boundaries(
                evidence=evidence,
                review=review,
                integration_contract=integration,
                privacy_contract=privacy,
            )

    def test_core10_task23_privacy_mutations_fail_closed_in_validator(self):
        without_core10 = [
            contract
            for contract in self.time_payload["privacyContracts"]
            if contract["id"] != "PC-IUM-7-CORE-10"
        ]
        privacy_contracts = validate_privacy_contracts(
            without_core10,
            self.repository_module_contracts,
        )
        review = next(
            item for item in self.time_payload["timeReviews"]
            if item["competencyId"] == "LH26-E-DP-014"
        )
        with self.assertRaisesRegex(
            IUM10ValidationError,
            "private-local time review needs privacy contract",
        ):
            self._validate_repository_time_reviews(
                [review],
                privacy_contracts=privacy_contracts,
            )

        for handling in (
            "access", "observation", "collection", "transfer", "storage",
            "assessment",
        ):
            with self.subTest(institutional_handling=handling):
                contracts = copy.deepcopy(self.time_payload["privacyContracts"])
                next(
                    item for item in contracts
                    if item["id"] == "PC-IUM-7-CORE-10"
                )["institutionalHandling"][handling] = "allowed"
                with self.assertRaises(IUM10ValidationError):
                    validate_privacy_contracts(
                        contracts,
                        self.repository_module_contracts,
                    )

        disposition_mutations = (
            ("missing disposition", None, None),
            ("wrong contract", "contractId", "PC-IUM-7-CORE-08"),
            ("wrong basis", "observableBasis", "nonpersonal-module-detail"),
            ("wrong evidence", "evidenceContractId", "CE-WRONG"),
            ("product included", "privateArtifactContribution.product", "included"),
            ("evidence included", "privateArtifactContribution.evidence", "included"),
            (
                "time included",
                "privateArtifactContribution.additionalTimeClaim",
                "included",
            ),
            ("other time treatment", "privateActivityTimeTreatment", "separate"),
        )
        for label, field, value in disposition_mutations:
            with self.subTest(disposition=label):
                mutated = copy.deepcopy(review)
                if field is None:
                    del mutated["privacyDisposition"]
                elif field.startswith("privateArtifactContribution."):
                    nested = field.split(".", 1)[1]
                    mutated["privacyDisposition"][
                        "privateArtifactContribution"
                    ][nested] = value
                else:
                    mutated["privacyDisposition"][field] = value
                with self.assertRaises(IUM10ValidationError):
                    self._validate_repository_time_reviews([mutated])

    def test_core10_task23_rejects_matrix_shared_time_and_path_mutations(self):
        review_mutations = (
            ("decision", "integrated"),
            ("additionalMinutes", 0),
            ("phaseIds", ["independent-action-product"]),
            ("integrationContractIds", ["INT-7-DATA-MEDIA-SOCIETY"]),
            ("pathAvailability", GRADE7_INTEGRATED_DEMAND_PATH_AVAILABILITY),
        )
        for field, value in review_mutations:
            with self.subTest(review_field=field):
                reviews = copy.deepcopy(self.time_payload["timeReviews"])
                next(
                    item for item in reviews
                    if item["competencyId"] == "LH26-E-DP-014"
                )[field] = value
                with self.assertRaises(AssertionError):
                    self._assert_core10_task23_audit_contract(reviews)

        for variant_id, field, value in (
            ("GRADE-7-OPTIMIZED-DEMAND", "available", True),
            ("GRADE-7-ROBUST-DEMAND", "targetUnits", 38),
        ):
            with self.subTest(variant=variant_id, field=field):
                variants = copy.deepcopy(self.repository_annual_variants)
                variants[variant_id][field] = value
                with self.assertRaises(AssertionError):
                    self._assert_core10_task23_audit_contract(
                        self.time_payload["timeReviews"],
                        annual_variants=variants,
                    )

        module_contracts = copy.deepcopy(self.repository_module_contracts)
        core10 = module_contracts["IUM-7-CORE-10"]
        core10["pathBudgets"][0]["countedSharedMinutes"] = 65
        core10["pathBudgets"][0]["sharedAllocations"][0]["minutes"] = 65
        with self.assertRaises(AssertionError):
            self._assert_core10_task23_audit_contract(
                self.time_payload["timeReviews"],
                module_contracts=module_contracts,
            )

        integrations = copy.deepcopy(self.repository_integration_contracts)
        integrations["INT-7-DATA-MEDIA-SOCIETY"][
            "preservedProductAndCurriculumEvidence"
        ].append("LH26-E-DP-014 wird durch den Verbund bewahrt.")
        with self.assertRaises(AssertionError):
            self._assert_core10_task23_audit_contract(
                self.time_payload["timeReviews"],
                integration_contracts=integrations,
            )

    def test_core10_task23_rejects_noncanonical_text_and_duplicate_review(self):
        reviews = copy.deepcopy(self.time_payload["timeReviews"])
        next(
            item for item in reviews
            if item["competencyId"] == "LH26-E-DP-014"
        )["risk"] += " Beliebige Ergänzung."
        with self.assertRaises(AssertionError):
            self._assert_core10_task23_audit_contract(reviews)

        reviews = copy.deepcopy(self.time_payload["timeReviews"])
        reviews.append(copy.deepcopy(reviews[PRE_TASK23_TIME_REVIEW_COUNT]))
        with self.assertRaises(AssertionError):
            self._assert_core10_task23_audit_contract(reviews)

    def test_repository_time_reviews_match_the_audited_decisions(self):
        prior_reviews = self.time_payload["timeReviews"][
            : len(PRIOR_20_TIME_REVIEW_IDS)
        ]
        self._assert_prior20_repository_contract(prior_reviews)

        result = validate_time_reviews(
            self.time_payload["timeReviews"],
            self.remediation_payload,
            self.repository_module_contracts,
            self.repository_integration_contracts,
            self.repository_annual_variants,
            require_complete=False,
            privacy_contracts=self.repository_privacy_contracts,
        )
        reviews_by_competency_id = {
            review["competencyId"]: review for review in result.values()
        }

        self.assertEqual(
            set(reviews_by_competency_id),
            set(TIME_AUDIT_DECISIONS),
        )
        for competency_id, expected_decision in TIME_AUDIT_DECISIONS.items():
            with self.subTest(competency_id=competency_id):
                review = reviews_by_competency_id[competency_id]
                self.assertEqual(review["decision"], expected_decision)
                self.assertEqual(
                    review["coverageConsequence"],
                    "semantic-status-unchanged",
                )

        gm003_review = reviews_by_competency_id["BMB16-GYM-IK-GM-003"]
        self.assertEqual(
            (
                gm003_review["decision"],
                gm003_review["additionalMinutes"],
                gm003_review["phaseIds"],
                gm003_review["pathAvailability"],
            ),
            (
                "additional-time",
                20,
                ["independent-action-product"],
                [
                    "GRADE-5-BASELINE",
                    "GRADE-5-REGULAR",
                    "GRADE-5-EXTENDED",
                ],
            ),
        )
        self.assertEqual(
            gm003_review["rationale"],
            EXPECTED_GM003_TIME_PLACEMENT_RATIONALE,
        )
        self.assertEqual(
            gm003_review["followUp"],
            EXPECTED_GM003_PRODUCT_ONLY_FOLLOW_UP,
        )

        dp001_review = reviews_by_competency_id["LH26-E-DP-001"]
        self.assertEqual(
            (
                dp001_review["decision"],
                dp001_review["additionalMinutes"],
                dp001_review["phaseIds"],
                dp001_review["pathAvailability"],
            ),
            (
                "additional-time",
                15,
                ["review-revise-transfer"],
                [
                    "GRADE-5-BASELINE",
                    "GRADE-5-REGULAR",
                    "GRADE-5-EXTENDED",
                ],
            ),
        )
        self.assertEqual(
            dp001_review["rationale"],
            EXPECTED_DP001_RULE_RATIONALE,
        )
        self.assertEqual(
            dp001_review["risk"],
            EXPECTED_DP001_OPERATIONAL_BOUNDARY_RISK,
        )
        self.assertEqual(
            dp001_review["followUp"],
            EXPECTED_DP001_RULE_FOLLOW_UP,
        )
        self.assertNotIn(
            "Datenschutz",
            " ".join(
                (
                    dp001_review["rationale"],
                    dp001_review["risk"],
                    dp001_review["followUp"],
                )
            ),
        )
        self._assert_id009_repository_contract(
            reviews_by_competency_id,
            self.repository_module_contracts,
        )
        self._assert_core03_repository_contract(
            reviews_by_competency_id,
            self.repository_module_contracts,
        )
        self._assert_core05_repository_contract(
            reviews_by_competency_id,
            self.repository_module_contracts,
        )
        self._assert_core06_repository_contract(
            reviews_by_competency_id,
            self.repository_module_contracts,
        )
        self._assert_core07_repository_contract(
            reviews_by_competency_id,
            self.repository_module_contracts,
        )
        progression_review = reviews_by_competency_id["LH26-E-PROG-001"]
        self.assertEqual(progression_review["phaseIds"], [])
        self.assertEqual(
            progression_review["sequenceEvidenceId"],
            "SE-LH26-E-PROG-001",
        )


class IUM10Grade5RepositoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        cls.time_model = json.loads(
            (root / "roadmap/time-model.json").read_text(encoding="utf-8")
        )
        module_payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(encoding="utf-8")
        )
        cls.grade_5_and_6_payload = {
            "modules": [
                module
                for module in module_payload["modules"]
                if module["grade"] in {5, 6}
            ]
        }
        cls.grade_5_payload = {
            "modules": [
                module for module in module_payload["modules"] if module["grade"] == 5
            ]
        }
        cls.grade_5_and_6_contracts = [
            contract
            for contract in cls.time_model["moduleContracts"]
            if contract["grade"] in {5, 6}
        ]
        cls.grade_5_contracts = [
            contract
            for contract in cls.time_model["moduleContracts"]
            if contract["grade"] == 5
        ]

    def test_repository_has_seven_complete_grade_5_time_contracts(self):
        contracts = validate_module_contracts(
            self.grade_5_contracts,
            self.grade_5_payload,
        )

        self.assertEqual(set(contracts), set(EXPECTED_GRADE_5_UNITS))
        for module_id, expected_paths in EXPECTED_GRADE_5_UNITS.items():
            with self.subTest(module_id=module_id):
                contract = contracts[module_id]
                budgets = {
                    budget["pathId"]: budget for budget in contract["pathBudgets"]
                }
                self.assertEqual(
                    {path_id: budget["units"] for path_id, budget in budgets.items()},
                    expected_paths,
                )
                for budget in budgets.values():
                    phases = {
                        phase["phaseId"]: phase for phase in budget["phaseBudgets"]
                    }
                    self.assertEqual(len(phases), 7)
                    self.assertTrue(
                        phases["orientation-challenge"]["learningFunction"].endswith(
                            contract["centralLearningAction"]
                        )
                    )
                    self.assertTrue(
                        phases["independent-action-product"]["learningFunction"].endswith(
                            contract["centralLearningProduct"]
                        )
                    )

    def test_repository_integration_counts_shared_evidence_only_in_core_06(self):
        all_contracts = validate_module_contracts(
            self.grade_5_and_6_contracts,
            self.grade_5_and_6_payload,
        )
        integrations = validate_integration_contracts(
            [
                integration
                for integration in self.time_model["integrationContracts"]
                if set(integration["moduleIds"]) <= set(all_contracts)
            ],
            all_contracts,
        )
        contracts = {
            module_id: contract
            for module_id, contract in all_contracts.items()
            if contract["grade"] == 5
        }

        self.assertEqual(
            set(integrations),
            {"INT-5-RESEARCH-PRODUCTION"} | set(EXPECTED_GRADE_6_INTEGRATIONS),
        )
        integration = integrations["INT-5-RESEARCH-PRODUCTION"]
        self.assertEqual(
            integration["moduleIds"],
            ["IUM-5-CORE-02", "IUM-5-CORE-06"],
        )
        self.assertEqual(integration["countedInModuleId"], "IUM-5-CORE-06")
        self.assertEqual(integration["sharedMinutes"], 45)
        self.assertEqual(
            integration["savingsMinutesByPath"],
            {"baseline": 45, "regular": 0, "extended": 0},
        )
        self.assertIn("Quellen", integration["sharedPhaseOrProduct"])
        self.assertIn("Beleg", integration["sharedPhaseOrProduct"])
        self.assertIn("eigenständig", integration["fallback"])
        self.assertEqual(
            {
                module_id: contract["integrationContractIds"]
                for module_id, contract in contracts.items()
            },
            {
                module_id: (
                    ["INT-5-RESEARCH-PRODUCTION"]
                    if module_id in {"IUM-5-CORE-02", "IUM-5-CORE-06"}
                    else ["INT-6-ALGORITHM-REVISIT"]
                    if module_id == "IUM-5-CORE-05"
                    else []
                )
                for module_id in EXPECTED_GRADE_5_UNITS
            },
        )

    def test_repository_has_available_core_only_30_34_38_variants(self):
        all_contracts = validate_module_contracts(
            self.grade_5_and_6_contracts,
            self.grade_5_and_6_payload,
        )
        integrations = validate_integration_contracts(
            [
                integration
                for integration in self.time_model["integrationContracts"]
                if set(integration["moduleIds"]) <= set(all_contracts)
            ],
            all_contracts,
        )
        all_variants = validate_annual_variants(
            [
                variant
                for variant in self.time_model["annualVariants"]
                if all(
                    allocation["moduleId"] in all_contracts
                    for allocation in variant["allocations"]
                )
            ],
            all_contracts,
            integrations,
        )
        contracts = {
            module_id: contract
            for module_id, contract in all_contracts.items()
            if contract["grade"] == 5
        }
        variants = {
            variant_id: variant
            for variant_id, variant in all_variants.items()
            if variant["grade"] == 5
        }

        expected_variants = {
            "GRADE-5-BASELINE": ("baseline", 30),
            "GRADE-5-REGULAR": ("regular", 34),
            "GRADE-5-EXTENDED": ("extended", 38),
        }
        self.assertEqual(set(variants), set(expected_variants))
        for variant_id, (path_id, target_units) in expected_variants.items():
            with self.subTest(variant_id=variant_id):
                variant = variants[variant_id]
                self.assertEqual(variant["pathId"], path_id)
                self.assertEqual(variant["targetUnits"], target_units)
                self.assertIs(variant["available"], True)
                self.assertEqual(
                    variant["integrationContractIds"],
                    ["INT-5-RESEARCH-PRODUCTION"],
                )
                self.assertEqual(
                    {allocation["moduleId"] for allocation in variant["allocations"]},
                    set(EXPECTED_GRADE_5_UNITS),
                )
                self.assertTrue(
                    all(
                        contracts[allocation["moduleId"]]["kind"] == "core"
                        for allocation in variant["allocations"]
                    )
                )

    def test_repository_grade_5_judgement_separates_status_dimensions(self):
        judgements = [
            judgement
            for judgement in self.time_model["gradeJudgements"]
            if judgement["grade"] == 5
        ]

        self.assertEqual(len(judgements), 1)
        judgement = judgements[0]
        self.assertEqual(
            {
                "semanticCoverageStatus": judgement["semanticCoverageStatus"],
                "timeFeasibilityStatus": judgement["timeFeasibilityStatus"],
                "sequenceEvidenceStatus": judgement["sequenceEvidenceStatus"],
                "pilotStatus": judgement["pilotStatus"],
            },
            {
                "semanticCoverageStatus": "partial",
                "timeFeasibilityStatus": "green",
                "sequenceEvidenceStatus": "covered",
                "pilotStatus": "not-started",
            },
        )
        self.assertEqual(
            judgement["annualVariantIds"],
            ["GRADE-5-BASELINE", "GRADE-5-REGULAR", "GRADE-5-EXTENDED"],
        )


class IUM10Grade6RepositoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        cls.time_model = json.loads(
            (root / "roadmap/time-model.json").read_text(encoding="utf-8")
        )
        module_payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(encoding="utf-8")
        )
        cls.full_module_payload = module_payload
        cls.grade_5_and_6_payload = {
            "modules": [
                module
                for module in module_payload["modules"]
                if module["grade"] in {5, 6}
            ]
        }
        cls.grade_6_payload = {
            "modules": [
                module for module in module_payload["modules"] if module["grade"] == 6
            ]
        }
        cls.grade_6_modules = {
            module["id"]: module for module in cls.grade_6_payload["modules"]
        }
        cls.grade_6_contracts = [
            contract
            for contract in cls.time_model["moduleContracts"]
            if contract["grade"] == 6
        ]
        cls.grade_5_and_6_contracts = [
            contract
            for contract in cls.time_model["moduleContracts"]
            if contract["grade"] in {5, 6}
        ]

    def validated_contracts(self):
        return validate_module_contracts(
            self.grade_6_contracts,
            self.grade_6_payload,
        )

    def validated_grade_5_and_6_contracts(self, contracts=None):
        return validate_module_contracts(
            (
                self.grade_5_and_6_contracts
                if contracts is None
                else contracts
            ),
            self.grade_5_and_6_payload,
        )

    def validated_orchestration(self, time_model=None):
        model = self.time_model if time_model is None else time_model
        contracts = validate_module_contracts(
            [
                contract
                for contract in model["moduleContracts"]
                if contract["grade"] in {5, 6}
            ],
            self.grade_5_and_6_payload,
        )
        integrations = validate_integration_contracts(
            [
                integration
                for integration in model["integrationContracts"]
                if set(integration["moduleIds"]) <= set(contracts)
            ],
            contracts,
        )
        variants = validate_annual_variants(
            [
                variant
                for variant in model["annualVariants"]
                if all(
                    allocation["moduleId"] in contracts
                    for allocation in variant["allocations"]
                )
            ],
            contracts,
            integrations,
        )
        return contracts, integrations, variants

    def grade_6_orchestration_findings(self, time_model):
        grade_6_module_ids = set(self.grade_6_modules)
        grade_6_integration_ids = [
            integration["id"]
            for integration in time_model["integrationContracts"]
            if set(integration["moduleIds"]) & grade_6_module_ids
        ]
        grade_6_variant_ids = [
            variant["id"]
            for variant in time_model["annualVariants"]
            if variant["grade"] == 6
            or any(
                allocation["moduleId"] in grade_6_module_ids
                for allocation in variant["allocations"]
            )
        ]
        grade_6_judgement_indexes = [
            index
            for index, judgement in enumerate(time_model["gradeJudgements"])
            if judgement["grade"] == 6
            or set(judgement["annualVariantIds"]) & set(grade_6_variant_ids)
        ]
        return {
            "integrationContractIds": grade_6_integration_ids,
            "annualVariantIds": grade_6_variant_ids,
            "gradeJudgementIndexes": grade_6_judgement_indexes,
        }

    def assert_grade_6_scope_matches_task_6_exactly(self, time_model):
        findings = self.grade_6_orchestration_findings(time_model)
        self.assertEqual(
            set(findings["integrationContractIds"]),
            set(EXPECTED_GRADE_6_INTEGRATIONS),
        )
        self.assertEqual(
            set(findings["annualVariantIds"]),
            set(EXPECTED_GRADE_6_VARIANTS),
        )
        self.assertEqual(len(findings["gradeJudgementIndexes"]), 1)

    def test_repository_grade_6_scope_matches_task_6_exactly(self):
        self.assert_grade_6_scope_matches_task_6_exactly(self.time_model)

    def test_scope_links_spoofed_grade_judgement_to_grade_6_variant(self):
        adversarial_time_model = copy.deepcopy(self.time_model)
        repository_findings = self.grade_6_orchestration_findings(
            self.time_model
        )
        adversarial_time_model["annualVariants"].append(
            {
                "id": "SPOOFED-ALLOCATION-VARIANT",
                "grade": 5,
                "kind": "planning-path",
                "pathId": "baseline",
                "targetUnits": 30,
                "allocations": [
                    {
                        "moduleId": module_id,
                        "budgetPathId": "baseline",
                        "units": units["baseline"],
                    }
                    for module_id, units in EXPECTED_GRADE_6_CORE_UNITS.items()
                ],
                "integrationContractIds": [],
                "available": True,
                "status": "working",
                "rationale": "Über Klasse-6-Allokationen semantisch verknüpft.",
                "risk": "Das grade-Feld ist absichtlich falsch gesetzt.",
            }
        )
        spoofed_judgement_index = len(
            adversarial_time_model["gradeJudgements"]
        )
        adversarial_time_model["gradeJudgements"].append(
            {
                "grade": 5,
                "semanticCoverageStatus": "partial",
                "timeFeasibilityStatus": "green",
                "sequenceEvidenceStatus": "partial",
                "pilotStatus": "not-started",
                "annualVariantIds": ["SPOOFED-ALLOCATION-VARIANT"],
                "rationale": "Über die Jahresvariante semantisch Klasse 6.",
                "risk": "Das grade-Feld ist absichtlich falsch gesetzt.",
                "decisionOptions": ["defer-to-task-6"],
            }
        )

        findings = self.grade_6_orchestration_findings(
            adversarial_time_model
        )

        self.assertEqual(
            set(findings["annualVariantIds"]),
            set(EXPECTED_GRADE_6_VARIANTS)
            | {"SPOOFED-ALLOCATION-VARIANT"},
        )
        self.assertEqual(
            findings["gradeJudgementIndexes"],
            repository_findings["gradeJudgementIndexes"]
            + [spoofed_judgement_index],
        )
        with self.assertRaises(AssertionError):
            self.assert_grade_6_scope_matches_task_6_exactly(
                adversarial_time_model
            )

    def test_repository_has_exactly_three_grade_6_integrations_with_exact_boundaries(self):
        contracts, integrations, _ = self.validated_orchestration()
        grade_6_integrations = {
            integration_id: integration
            for integration_id, integration in integrations.items()
            if integration_id in EXPECTED_GRADE_6_INTEGRATIONS
        }

        self.assertEqual(
            set(grade_6_integrations),
            set(EXPECTED_GRADE_6_INTEGRATIONS),
        )
        for integration_id, expected in EXPECTED_GRADE_6_INTEGRATIONS.items():
            with self.subTest(integration_id=integration_id):
                integration = grade_6_integrations[integration_id]
                self.assertEqual(integration["pathIds"], ["baseline", "regular"])
                for field, value in expected.items():
                    self.assertEqual(integration[field], value)
                self.assertGreaterEqual(
                    len(integration["preservedLearningActions"]),
                    2,
                )
                self.assertGreaterEqual(
                    len(integration["preservedProductAndCurriculumEvidence"]),
                    2,
                )
                prerequisite_text = " ".join(integration["prerequisites"])
                for module_id in integration["moduleIds"]:
                    with self.subTest(
                        integration_id=integration_id,
                        module_id=module_id,
                    ):
                        learning_actions = [
                            action
                            for action in integration[
                                "preservedLearningActions"
                            ]
                            if action.startswith(f"{module_id} ")
                        ]
                        evidence_records = [
                            evidence
                            for evidence in integration[
                                "preservedProductAndCurriculumEvidence"
                            ]
                            if evidence.startswith(f"{module_id}: ")
                        ]
                        self.assertEqual(len(learning_actions), 1)
                        self.assertEqual(len(evidence_records), 1)
                        self.assertIn(
                            "Kompetenznachweis",
                            evidence_records[0],
                        )
                        self.assertIn(
                            "Produktnachweis",
                            evidence_records[0],
                        )
                        self.assertTrue(
                            any(
                                competency_id in evidence_records[0]
                                for competency_id in contracts[module_id][
                                    "competencyIds"
                                ]
                            )
                        )
                        self.assertIn(module_id, prerequisite_text)
                for path_id, saved_minutes in expected[
                    "savingsMinutesByPath"
                ].items():
                    self.assertIn(
                        f"{path_id}: +{saved_minutes} Minuten",
                        integration["fallback"],
                    )
                    self.assertIn(
                        f"{path_id}:",
                        integration["risk"],
                    )
                self.assertIn(
                    f"{integration['sharedMinutes']} Minuten",
                    integration["fallback"],
                )
                self.assertIn("eigenständig", integration["fallback"].lower())

    def test_rejects_grade_6_integration_when_participant_or_path_evidence_is_removed(self):
        def remove_learning_action(integration):
            del integration["preservedLearningActions"][0]

        def remove_product_evidence(integration):
            del integration["preservedProductAndCurriculumEvidence"][0]

        def remove_concrete_prerequisites(integration):
            integration["prerequisites"] = [
                "Die Voraussetzungen werden vor der Integration allgemein geprüft."
            ]

        def remove_path_specific_fallback(integration):
            integration["fallback"] = (
                "Bei Problemen werden eigenständige Sequenzen bereitgestellt."
            )

        def remove_path_specific_risk(integration):
            integration["risk"] = (
                "Ein allgemeines Integrationsrisiko bleibt zu beobachten."
            )

        mutations = (
            ("participant learning action", remove_learning_action),
            ("participant product evidence", remove_product_evidence),
            ("concrete prerequisites", remove_concrete_prerequisites),
            ("path-specific fallback", remove_path_specific_fallback),
            ("path-specific risk", remove_path_specific_risk),
        )
        for integration_id in EXPECTED_GRADE_6_INTEGRATIONS:
            for label, mutate in mutations:
                with self.subTest(
                    integration_id=integration_id,
                    removed=label,
                ):
                    adversarial_time_model = copy.deepcopy(self.time_model)
                    integration = next(
                        contract
                        for contract in adversarial_time_model[
                            "integrationContracts"
                        ]
                        if contract["id"] == integration_id
                    )
                    mutate(integration)

                    with self.assertRaises(IUM10ValidationError):
                        validate_time_model_draft(
                            adversarial_time_model,
                            self.full_module_payload,
                        )

    def test_repository_counts_each_grade_6_shared_allocation_only_in_its_counted_module(self):
        contracts, integrations, _ = self.validated_orchestration()

        for integration_id, expected in EXPECTED_GRADE_6_INTEGRATIONS.items():
            locations = {
                (module_id, budget["pathId"], allocation["minutes"])
                for module_id, contract in contracts.items()
                for budget in contract["pathBudgets"]
                for allocation in budget["sharedAllocations"]
                if allocation["integrationContractId"] == integration_id
            }
            self.assertEqual(
                locations,
                {
                    (
                        expected["countedInModuleId"],
                        path_id,
                        expected["sharedMinutes"],
                    )
                    for path_id in ("baseline", "regular")
                },
            )

            adversarial_contracts = copy.deepcopy(contracts)
            uncounted_module_id = next(
                module_id
                for module_id in expected["moduleIds"]
                if module_id != expected["countedInModuleId"]
            )
            adversarial_contracts[uncounted_module_id]["pathBudgets"][0][
                "sharedAllocations"
            ].append(
                {
                    "integrationContractId": integration_id,
                    "minutes": expected["sharedMinutes"],
                }
            )
            with self.assertRaisesRegex(IUM10ValidationError, "exactly once"):
                validate_integration_contracts(
                    list(integrations.values()),
                    adversarial_contracts,
                )

    def test_rejects_cross_grade_integration_without_prerequisite_and_revisit_chain(self):
        contracts, integrations, _ = self.validated_orchestration()
        adversarial_contracts = copy.deepcopy(contracts)
        adversarial_contracts["IUM-5-CORE-05"]["revisitModuleIds"] = []

        with self.assertRaisesRegex(IUM10ValidationError, "cross-grade"):
            validate_integration_contracts(
                list(integrations.values()),
                adversarial_contracts,
            )

    def test_repository_has_exact_grade_6_30_34_and_three_38_variants(self):
        contracts, _, variants = self.validated_orchestration()
        grade_6_variants = {
            variant_id: variant
            for variant_id, variant in variants.items()
            if variant["grade"] == 6
        }
        core_module_ids = set(EXPECTED_GRADE_6_CORE_UNITS)

        self.assertEqual(set(grade_6_variants), set(EXPECTED_GRADE_6_VARIANTS))
        for variant_id, expected in EXPECTED_GRADE_6_VARIANTS.items():
            with self.subTest(variant_id=variant_id):
                variant = grade_6_variants[variant_id]
                allocations = {
                    allocation["moduleId"]: allocation
                    for allocation in variant["allocations"]
                }
                self.assertEqual(variant["pathId"], expected["pathId"])
                self.assertEqual(variant["targetUnits"], expected["targetUnits"])
                self.assertIs(variant["available"], True)
                self.assertEqual(variant["status"], "working")
                self.assertEqual(
                    core_module_ids & set(allocations),
                    core_module_ids,
                )
                self.assertEqual(
                    sum(
                        allocation["units"]
                        for module_id, allocation in allocations.items()
                        if module_id in core_module_ids
                    ),
                    expected["coreUnits"],
                )
                self.assertNotIn("IUM-6-PROJECT-01", allocations)

                flex_module_ids = {
                    module_id
                    for module_id in allocations
                    if contracts[module_id]["kind"] != "core"
                }
                expected_flex_ids = (
                    set()
                    if expected["flexModuleId"] is None
                    else {expected["flexModuleId"]}
                )
                self.assertEqual(flex_module_ids, expected_flex_ids)
                self.assertEqual(
                    sum(
                        allocations[module_id]["units"]
                        for module_id in flex_module_ids
                    ),
                    expected["flexUnits"],
                )

        coding_allocations = {
            allocation["moduleId"]: allocation
            for allocation in grade_6_variants[
                "GRADE-6-EXTENDED-CODING"
            ]["allocations"]
        }
        self.assertEqual(
            coding_allocations["IUM-6-CORE-04"],
            {
                "moduleId": "IUM-6-CORE-04",
                "budgetPathId": "targeted-extension",
                "units": 6,
            },
        )
        self.assertEqual(
            coding_allocations["IUM-6-EXT-02"],
            {
                "moduleId": "IUM-6-EXT-02",
                "budgetPathId": "standalone",
                "units": 3,
            },
        )

    def test_grade_6_extended_variants_use_explicit_budget_path_overrides(self):
        core_regular_overrides = {
            module_id: "regular" for module_id in EXPECTED_GRADE_6_CORE_UNITS
        }
        expected_overrides = {
            "GRADE-6-EXTENDED-REFERENCE": {
                **core_regular_overrides,
                "IUM-6-EXT-01": "standalone",
            },
            "GRADE-6-EXTENDED-TRANSFER": {
                **core_regular_overrides,
                "IUM-6-TRANSFER-01": "standalone",
            },
            "GRADE-6-EXTENDED-CODING": {
                **core_regular_overrides,
                "IUM-6-CORE-04": "targeted-extension",
                "IUM-6-EXT-02": "standalone",
            },
        }

        self.assertEqual(
            ium10_validator.ANNUAL_VARIANT_BUDGET_PATH_OVERRIDES,
            expected_overrides,
        )

    def test_rejects_stale_grade_6_variant_or_module_override_keys(self):
        contracts = self.validated_grade_5_and_6_contracts()
        integrations = validate_integration_contracts(
            [
                integration
                for integration in self.time_model["integrationContracts"]
                if set(integration["moduleIds"]) <= set(contracts)
            ],
            contracts,
        )
        overrides = ium10_validator.ANNUAL_VARIANT_BUDGET_PATH_OVERRIDES
        original_overrides = copy.deepcopy(overrides)

        def add_stale_variant_override():
            overrides["STALE-GRADE-6-OVERRIDE"] = {
                "IUM-6-CORE-01": "regular",
            }

        def add_stale_module_override():
            overrides["GRADE-6-EXTENDED-REFERENCE"][
                "IUM-6-EXT-02"
            ] = "standalone"

        mutations = (
            ("stale variant override", add_stale_variant_override),
            ("stale module override", add_stale_module_override),
        )
        try:
            for label, mutate in mutations:
                with self.subTest(label=label):
                    overrides.clear()
                    overrides.update(copy.deepcopy(original_overrides))
                    mutate()

                    with self.assertRaisesRegex(
                        IUM10ValidationError,
                        "variant path override",
                    ):
                        validate_annual_variants(
                            [
                                variant
                                for variant in self.time_model["annualVariants"]
                                if all(
                                    allocation["moduleId"] in contracts
                                    for allocation in variant["allocations"]
                                )
                            ],
                            contracts,
                            integrations,
                        )
        finally:
            overrides.clear()
            overrides.update(original_overrides)

    def test_rejects_grade_6_flex_replacement_and_project_in_normal_variants(self):
        contracts, integrations, variants = self.validated_orchestration()
        core_regular_overrides = {
            module_id: "regular" for module_id in EXPECTED_GRADE_6_CORE_UNITS
        }
        adversarial_variants = []

        flex_replacement = copy.deepcopy(variants["GRADE-6-BASELINE"])
        flex_replacement["id"] = "GRADE-6-FLEX-REPLACEMENT"
        flex_replacement["allocations"] = [
            (
                {
                    "moduleId": "IUM-6-EXT-01",
                    "budgetPathId": "standalone",
                    "units": 4,
                }
                if allocation["moduleId"] == "IUM-6-CORE-03"
                else allocation
            )
            for allocation in flex_replacement["allocations"]
        ]
        adversarial_variants.append(
            (
                flex_replacement,
                {"IUM-6-EXT-01": "standalone"},
                "all core modules",
            )
        )

        project_variant = copy.deepcopy(variants["GRADE-6-REGULAR"])
        project_variant.update(
            {
                "id": "GRADE-6-PROJECT-ADVERSARIAL",
                "pathId": "extended",
                "targetUnits": 44,
            }
        )
        project_variant["allocations"].append(
            {
                "moduleId": "IUM-6-PROJECT-01",
                "budgetPathId": "standalone",
                "units": 10,
            }
        )
        adversarial_variants.append(
            (
                project_variant,
                {
                    **core_regular_overrides,
                    "IUM-6-PROJECT-01": "standalone",
                },
                "project modules",
            )
        )

        for variant, overrides, message in adversarial_variants:
            with self.subTest(variant_id=variant["id"]):
                ium10_validator.ANNUAL_VARIANT_BUDGET_PATH_OVERRIDES[
                    variant["id"]
                ] = overrides
                try:
                    with self.assertRaisesRegex(IUM10ValidationError, message):
                        validate_annual_variants(
                            [variant],
                            contracts,
                            integrations,
                        )
                finally:
                    del ium10_validator.ANNUAL_VARIANT_BUDGET_PATH_OVERRIDES[
                        variant["id"]
                    ]

    def test_repository_grade_6_judgement_is_green_but_semantic_and_pilot_statuses_stay_separate(self):
        validate_time_model_draft(
            self.time_model,
            self.full_module_payload,
        )
        judgements = [
            judgement
            for judgement in self.time_model["gradeJudgements"]
            if judgement["grade"] == 6
        ]

        self.assertEqual(len(judgements), 1)
        judgement = judgements[0]
        self.assertEqual(
            {
                "semanticCoverageStatus": judgement["semanticCoverageStatus"],
                "timeFeasibilityStatus": judgement["timeFeasibilityStatus"],
                "sequenceEvidenceStatus": judgement["sequenceEvidenceStatus"],
                "pilotStatus": judgement["pilotStatus"],
            },
            {
                "semanticCoverageStatus": "partial",
                "timeFeasibilityStatus": "green",
                "sequenceEvidenceStatus": "covered",
                "pilotStatus": "not-started",
            },
        )
        self.assertEqual(
            set(judgement["annualVariantIds"]),
            set(EXPECTED_GRADE_6_VARIANTS),
        )
        self.assertIn("semant", judgement["rationale"].lower())
        self.assertIn("pilot", judgement["risk"].lower())

    def test_rejects_green_grade_6_judgement_when_variants_or_integrations_do_not_pass(self):
        mutations = (
            (
                "failed module contract",
                "moduleContracts",
                "TC-IUM-6-CORE-01",
                "status",
                "failed",
            ),
            (
                "wrong 30 path",
                "annualVariants",
                "GRADE-6-BASELINE",
                "targetUnits",
                31,
            ),
            (
                "failed integration",
                "integrationContracts",
                "INT-6-ACTORS-SELECTION",
                "status",
                "failed",
            ),
        )
        for label, collection, record_id, field, value in mutations:
            with self.subTest(label=label):
                adversarial_time_model = copy.deepcopy(self.time_model)
                records = adversarial_time_model[collection]
                record = next(record for record in records if record["id"] == record_id)
                record[field] = value
                with self.assertRaises(IUM10ValidationError):
                    validate_time_model_draft(
                        adversarial_time_model,
                        self.full_module_payload,
                    )

        unjustified_amber = copy.deepcopy(self.time_model)
        next(
            judgement
            for judgement in unjustified_amber["gradeJudgements"]
            if judgement["grade"] == 6
        )["timeFeasibilityStatus"] = "amber"
        with self.assertRaisesRegex(
            IUM10ValidationError,
            "grade 6 green judgement",
        ):
            validate_time_model_draft(
                unjustified_amber,
                self.full_module_payload,
            )

    def test_green_grade_6_judgement_runs_structural_and_exact_contract_validation(self):
        def mutate_counted_module(time_model):
            next(
                integration
                for integration in time_model["integrationContracts"]
                if integration["id"] == "INT-6-ACTORS-SELECTION"
            )["countedInModuleId"] = "IUM-6-CORE-03"

        def mutate_module_pair(time_model):
            next(
                integration
                for integration in time_model["integrationContracts"]
                if integration["id"] == "INT-6-CONFLICT-PRODUCTION"
            )["moduleIds"] = ["IUM-6-CORE-05", "IUM-6-CORE-07"]

        def mutate_savings(time_model):
            next(
                integration
                for integration in time_model["integrationContracts"]
                if integration["id"] == "INT-6-ALGORITHM-REVISIT"
            )["savingsMinutesByPath"]["baseline"] = 0

        def mutate_variant_budget_path(time_model):
            variant = next(
                variant
                for variant in time_model["annualVariants"]
                if variant["id"] == "GRADE-6-EXTENDED-REFERENCE"
            )
            allocation = next(
                allocation
                for allocation in variant["allocations"]
                if allocation["moduleId"] == "IUM-6-CORE-01"
            )
            allocation["budgetPathId"] = "baseline"

        mutations = (
            ("invalid counted module", mutate_counted_module),
            ("invalid module pair", mutate_module_pair),
            ("wrong exact savings", mutate_savings),
            ("invalid variant budget path", mutate_variant_budget_path),
        )
        for label, mutate in mutations:
            with self.subTest(label=label):
                adversarial_time_model = copy.deepcopy(self.time_model)
                mutate(adversarial_time_model)

                with self.assertRaises(IUM10ValidationError):
                    validate_time_model_draft(
                        adversarial_time_model,
                        self.full_module_payload,
                    )

    def grade_6_amber_with_algorithm_bounds_residual(self, residual_evidence):
        time_model = copy.deepcopy(self.time_model)
        integration = next(
            integration
            for integration in time_model["integrationContracts"]
            if integration["id"] == "INT-6-ALGORITHM-REVISIT"
        )
        integration["savingsMinutesByPath"]["baseline"] = 0
        integration["fallback"] = integration["fallback"].replace(
            "baseline: +45 Minuten",
            "baseline: +0 Minuten",
        )
        judgement = next(
            judgement
            for judgement in time_model["gradeJudgements"]
            if judgement["grade"] == 6
        )
        judgement["timeFeasibilityStatus"] = "amber"
        judgement["rationale"] = "Das Zeiturteil ist wegen eines Restbefunds amber."
        judgement["risk"] = residual_evidence
        return time_model

    def task_5_draft_with_grade_6_module_contracts_only(self):
        time_model = copy.deepcopy(self.time_model)
        time_model["moduleContracts"] = [
            contract
            for contract in time_model["moduleContracts"]
            if contract["grade"] in {5, 6}
        ]
        retained_module_ids = {
            contract["moduleId"] for contract in time_model["moduleContracts"]
        }
        time_model["privacyContracts"] = [
            contract for contract in time_model["privacyContracts"]
            if contract["moduleId"] in retained_module_ids
        ]
        time_model["integrationContracts"] = [
            integration
            for integration in time_model["integrationContracts"]
            if set(integration["moduleIds"]) <= retained_module_ids
        ]
        time_model["annualVariants"] = [
            variant
            for variant in time_model["annualVariants"]
            if all(
                allocation["moduleId"] in retained_module_ids
                for allocation in variant["allocations"]
            )
        ]
        time_model["gradeJudgements"] = [
            judgement
            for judgement in time_model["gradeJudgements"]
            if judgement["grade"] in {5, 6}
        ]
        known_grade_6_integration_ids = set(EXPECTED_GRADE_6_INTEGRATIONS)
        time_model["integrationContracts"] = [
            integration
            for integration in time_model["integrationContracts"]
            if integration["id"] not in known_grade_6_integration_ids
        ]
        time_model["annualVariants"] = [
            variant
            for variant in time_model["annualVariants"]
            if variant["grade"] != 6
        ]
        time_model["gradeJudgements"] = [
            judgement
            for judgement in time_model["gradeJudgements"]
            if judgement["grade"] != 6
        ]
        for contract in time_model["moduleContracts"]:
            contract["integrationContractIds"] = [
                integration_id
                for integration_id in contract["integrationContractIds"]
                if integration_id not in known_grade_6_integration_ids
            ]
            for budget in contract["pathBudgets"]:
                retained_allocations = [
                    allocation
                    for allocation in budget["sharedAllocations"]
                    if allocation["integrationContractId"]
                    not in known_grade_6_integration_ids
                ]
                removed_minutes = budget["countedSharedMinutes"] - sum(
                    allocation["minutes"]
                    for allocation in retained_allocations
                )
                budget["sharedAllocations"] = retained_allocations
                budget["countedSharedMinutes"] -= removed_minutes
                budget["directMinutes"] += removed_minutes
        return time_model

    @staticmethod
    def add_extra_grade_6_flex_project_integration(time_model):
        integration_id = "INT-6-EXTRA-FLEX-PROJECT"
        participant_ids = ("IUM-6-EXT-02", "IUM-6-PROJECT-01")
        contracts = {
            contract["moduleId"]: contract
            for contract in time_model["moduleContracts"]
        }
        for module_id in participant_ids:
            contracts[module_id]["integrationContractIds"].append(
                integration_id
            )
        counted_budget = contracts["IUM-6-PROJECT-01"]["pathBudgets"][0]
        counted_budget["directMinutes"] -= 45
        counted_budget["countedSharedMinutes"] += 45
        counted_budget["sharedAllocations"].append(
            {
                "integrationContractId": integration_id,
                "minutes": 45,
            }
        )
        time_model["integrationContracts"].append(
            {
                "id": integration_id,
                "moduleIds": list(participant_ids),
                "pathIds": ["standalone"],
                "sharedPhaseOrProduct": (
                    "Adversariale gemeinsame Flex-Projekt-Spur."
                ),
                "countedInModuleId": "IUM-6-PROJECT-01",
                "sharedMinutes": 45,
                "savingsMinutesByPath": {"standalone": 0},
                "preservedLearningActions": [
                    "Beide Module bearbeiten eine gemeinsame Spur."
                ],
                "preservedProductAndCurriculumEvidence": [
                    "Ein gemeinsames Produkt bleibt sichtbar."
                ],
                "prerequisites": [
                    "Beide Modulverträge liegen vor."
                ],
                "risk": "Die zusätzliche Integration ist nicht autorisiert.",
                "fallback": "Beide Module arbeiten eigenständig.",
                "status": "working",
            }
        )

    def test_amber_grade_6_judgement_rejects_generic_or_id_only_residual_text(self):
        invalid_residual_evidence = (
            "Eine Integration hat einen Restbefund.",
            "INT-6-ALGORITHM-REVISIT",
        )
        for residual_evidence in invalid_residual_evidence:
            with self.subTest(residual_evidence=residual_evidence):
                time_model = self.grade_6_amber_with_algorithm_bounds_residual(
                    residual_evidence
                )

                with self.assertRaises(IUM10ValidationError):
                    validate_time_model_draft(
                        time_model,
                        self.full_module_payload,
                    )

    def test_amber_grade_6_judgement_accepts_exact_record_and_cause_evidence(self):
        time_model = self.grade_6_amber_with_algorithm_bounds_residual(
            "INT-6-ALGORITHM-REVISIT [contract-bounds-mismatch]"
        )

        result = validate_time_model_draft(
            time_model,
            self.full_module_payload,
        )

        self.assertIs(result, time_model)

    def test_rejects_green_grade_6_judgement_with_duplicate_orchestration_records(self):
        duplicates = (
            ("moduleContracts", "TC-IUM-6-CORE-01"),
            ("integrationContracts", "INT-6-ACTORS-SELECTION"),
            ("annualVariants", "GRADE-6-BASELINE"),
        )
        for collection, record_id in duplicates:
            with self.subTest(collection=collection):
                adversarial_time_model = copy.deepcopy(self.time_model)
                record = next(
                    record
                    for record in adversarial_time_model[collection]
                    if record["id"] == record_id
                )
                adversarial_time_model[collection].append(copy.deepcopy(record))

                with self.assertRaises(IUM10ValidationError):
                    validate_time_model_draft(
                        adversarial_time_model,
                        self.full_module_payload,
                    )

    def test_rejects_green_grade_6_judgement_with_extra_flex_project_integration(self):
        adversarial_time_model = copy.deepcopy(self.time_model)
        self.add_extra_grade_6_flex_project_integration(
            adversarial_time_model
        )

        with self.assertRaisesRegex(
            IUM10ValidationError,
            "grade 6 green judgement",
        ):
            validate_time_model_draft(
                adversarial_time_model,
                self.full_module_payload,
            )

    def test_bootstrap_rejects_isolated_grade_6_flex_project_integration(self):
        adversarial_time_model = (
            self.task_5_draft_with_grade_6_module_contracts_only()
        )
        self.add_extra_grade_6_flex_project_integration(
            adversarial_time_model
        )
        grade_6_module_ids = set(self.grade_6_modules)
        grade_6_integration_ids = {
            integration["id"]
            for integration in adversarial_time_model[
                "integrationContracts"
            ]
            if set(integration["moduleIds"]) & grade_6_module_ids
        }
        self.assertEqual(
            grade_6_integration_ids,
            {"INT-6-EXTRA-FLEX-PROJECT"},
        )
        self.assertFalse(
            any(
                variant["grade"] == 6
                for variant in adversarial_time_model["annualVariants"]
            )
        )
        self.assertFalse(
            any(
                judgement["grade"] == 6
                for judgement in adversarial_time_model["gradeJudgements"]
            )
        )

        with self.assertRaisesRegex(
            IUM10ValidationError,
            "grade 6 orchestration needs exactly one judgement",
        ):
            validate_time_model_draft(
                adversarial_time_model,
                self.full_module_payload,
            )

    def test_grade_6_module_contracts_alone_do_not_bootstrap_orchestration(self):
        task_5_time_model = (
            self.task_5_draft_with_grade_6_module_contracts_only()
        )

        result = validate_time_model_draft(task_5_time_model)

        self.assertIs(result, task_5_time_model)

    def test_repository_has_exactly_eleven_complete_grade_6_time_contracts(self):
        expected_module_ids = set(EXPECTED_GRADE_6_CORE_UNITS) | set(
            EXPECTED_GRADE_6_FLEX_CONTRACTS
        )
        self.assertEqual(
            {contract["moduleId"] for contract in self.grade_6_contracts},
            expected_module_ids,
        )
        contracts = self.validated_contracts()
        self.assertEqual(set(contracts), expected_module_ids)
        self.assertEqual(len(contracts), 11)

    def test_repository_grade_6_core_paths_match_the_approved_matrix(self):
        contracts = self.validated_contracts()

        for module_id, expected_paths in EXPECTED_GRADE_6_CORE_UNITS.items():
            with self.subTest(module_id=module_id):
                budgets = {
                    budget["pathId"]: budget
                    for budget in contracts[module_id]["pathBudgets"]
                }
                self.assertEqual(
                    {
                        path_id: budget["units"]
                        for path_id, budget in budgets.items()
                    },
                    expected_paths,
                )

    def test_repository_grade_6_flex_ranges_and_prerequisites_match_the_graph(self):
        contracts = self.validated_contracts()

        for module_id, expected in EXPECTED_GRADE_6_FLEX_CONTRACTS.items():
            with self.subTest(module_id=module_id):
                contract = contracts[module_id]
                self.assertEqual(
                    contract["standaloneUnitRange"],
                    expected["standaloneUnitRange"],
                )
                self.assertEqual(
                    contract["prerequisiteModuleIds"],
                    expected["prerequisiteModuleIds"],
                )
                self.assertEqual(
                    contract["prerequisiteModuleIds"],
                    self.grade_6_modules[module_id]["prerequisiteModuleIds"],
                )
                self.assertEqual(
                    contract["pathBudgets"][0]["units"],
                    expected["standaloneUnitRange"]["recommended"],
                )

    def test_repository_grade_6_phase_budgets_are_positive_and_grammar_complete(self):
        contracts = self.validated_contracts()

        for module_id, contract in contracts.items():
            expected_phase_ids = set(
                self.grade_6_modules[module_id]["moduleGrammar"]
            )
            for budget in contract["pathBudgets"]:
                with self.subTest(module_id=module_id, path_id=budget["pathId"]):
                    phase_budgets = budget["phaseBudgets"]
                    self.assertEqual(
                        {phase["phaseId"] for phase in phase_budgets},
                        expected_phase_ids,
                    )
                    self.assertTrue(
                        all(
                            phase["minutes"] > 0
                            and phase["learningFunction"].strip()
                            for phase in phase_budgets
                        )
                    )
                    self.assertEqual(
                        sum(phase["minutes"] for phase in phase_budgets),
                        budget["units"] * 45,
                    )

    def test_repository_extra_grade_6_core_time_only_expands_allowed_functions(self):
        contracts = self.validated_contracts()
        allowed_growth_phases = {
            "activate-prior-knowledge",
            "build-concept",
            "guided-practice",
            "independent-action-product",
            "review-revise-transfer",
            "shared-consolidation",
        }

        for module_id in EXPECTED_GRADE_6_CORE_UNITS:
            budgets = {
                budget["pathId"]: budget
                for budget in contracts[module_id]["pathBudgets"]
            }
            ordered_path_ids = [
                path_id
                for path_id in ("baseline", "regular", "targeted-extension")
                if path_id in budgets
            ]
            for earlier_path_id, later_path_id in zip(
                ordered_path_ids,
                ordered_path_ids[1:],
            ):
                earlier = {
                    phase["phaseId"]: phase["minutes"]
                    for phase in budgets[earlier_path_id]["phaseBudgets"]
                }
                later = {
                    phase["phaseId"]: phase["minutes"]
                    for phase in budgets[later_path_id]["phaseBudgets"]
                }
                growth_phases = {
                    phase_id
                    for phase_id in earlier
                    if later[phase_id] > earlier[phase_id]
                }
                with self.subTest(
                    module_id=module_id,
                    earlier_path_id=earlier_path_id,
                    later_path_id=later_path_id,
                ):
                    self.assertTrue(growth_phases <= allowed_growth_phases)
                    if budgets[later_path_id]["units"] > budgets[earlier_path_id]["units"]:
                        self.assertTrue(growth_phases)

    def test_repository_project_requires_focus_time_outside_normal_year_paths(self):
        contracts = self.validated_contracts()
        project = contracts["IUM-6-PROJECT-01"]

        self.assertIn("zusätzliche", project["risk"].lower())
        self.assertIn("schwerpunktzeit", project["risk"].lower())
        self.assertIn("30/34/38", project["risk"])
        self.assertFalse(
            any(
                allocation["moduleId"] == project["moduleId"]
                for variant in self.time_model["annualVariants"]
                for allocation in variant["allocations"]
            )
        )


class IUM10Grade7RepositoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        cls.time_model = json.loads(
            (root / "roadmap/time-model.json").read_text(encoding="utf-8")
        )
        module_payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(encoding="utf-8")
        )
        cls.module_payload = module_payload
        cls.grade_7_payload = {
            "modules": [
                module for module in module_payload["modules"] if module["grade"] == 7
            ]
        }
        cls.grade_7_modules = {
            module["id"]: module for module in cls.grade_7_payload["modules"]
        }
        cls.grade_7_contracts = [
            contract
            for contract in cls.time_model["moduleContracts"]
            if contract["grade"] == 7
        ]

    def test_repository_has_exactly_thirteen_grade_7_time_contracts(self):
        expected_module_ids = set(EXPECTED_GRADE_7_UNITS) | set(
            EXPECTED_GRADE_7_FLEX_CONTRACTS
        )

        self.assertEqual(
            {contract["moduleId"] for contract in self.grade_7_contracts},
            expected_module_ids,
        )
        contracts = validate_module_contracts(
            self.grade_7_contracts,
            self.grade_7_payload,
        )
        self.assertEqual(set(contracts), expected_module_ids)
        self.assertEqual(len(contracts), 13)

    def test_repository_grade_7_core_paths_match_the_approved_matrix(self):
        contracts = {
            contract["moduleId"]: contract for contract in self.grade_7_contracts
        }
        self.assertEqual(set(contracts) & set(EXPECTED_GRADE_7_UNITS), set(EXPECTED_GRADE_7_UNITS))

        for module_id, expected_paths in EXPECTED_GRADE_7_UNITS.items():
            with self.subTest(module_id=module_id):
                budgets = {
                    budget["pathId"]: budget
                    for budget in contracts[module_id]["pathBudgets"]
                }
                self.assertEqual(
                    {
                        path_id: budget["units"]
                        for path_id, budget in budgets.items()
                    },
                    expected_paths,
                )

    def test_repository_grade_7_flex_ranges_match_the_approved_contracts(self):
        contracts = {
            contract["moduleId"]: contract for contract in self.grade_7_contracts
        }
        self.assertEqual(
            set(contracts) & set(EXPECTED_GRADE_7_FLEX_CONTRACTS),
            set(EXPECTED_GRADE_7_FLEX_CONTRACTS),
        )

        for module_id, expected in EXPECTED_GRADE_7_FLEX_CONTRACTS.items():
            with self.subTest(module_id=module_id):
                contract = contracts[module_id]
                self.assertEqual(
                    contract["standaloneUnitRange"],
                    expected["standaloneUnitRange"],
                )
                self.assertEqual(
                    contract["prerequisiteModuleIds"],
                    expected["prerequisiteModuleIds"],
                )
                self.assertEqual(
                    contract["pathBudgets"][0]["units"],
                    expected["standaloneUnitRange"]["recommended"],
                )
                self.assertFalse(
                    any(
                        allocation["moduleId"] == module_id
                        for variant in self.time_model["annualVariants"]
                        for allocation in variant["allocations"]
                    )
                )

    def test_repository_grade_7_phase_budgets_are_positive_and_grammar_complete(self):
        contracts = {
            contract["moduleId"]: contract for contract in self.grade_7_contracts
        }
        self.assertEqual(set(contracts), set(self.grade_7_modules))

        for module_id, contract in contracts.items():
            expected_phase_ids = set(
                self.grade_7_modules[module_id]["moduleGrammar"]
            )
            for budget in contract["pathBudgets"]:
                with self.subTest(module_id=module_id, path_id=budget["pathId"]):
                    phase_budgets = budget["phaseBudgets"]
                    self.assertEqual(
                        {phase["phaseId"] for phase in phase_budgets},
                        expected_phase_ids,
                    )
                    self.assertTrue(
                        all(
                            phase["minutes"] > 0
                            and phase["learningFunction"].strip()
                            for phase in phase_budgets
                        )
                    )
                    self.assertEqual(
                        sum(phase["minutes"] for phase in phase_budgets),
                        budget["units"] * 45,
                    )

    def test_repository_has_exactly_four_grade_7_cluster_integrations(self):
        grade_7_integrations = {
            integration["id"]: integration
            for integration in self.time_model["integrationContracts"]
            if integration["id"] in EXPECTED_GRADE_7_INTEGRATIONS
        }
        self.assertEqual(
            set(grade_7_integrations),
            set(EXPECTED_GRADE_7_INTEGRATIONS),
        )

        for integration_id, expected in EXPECTED_GRADE_7_INTEGRATIONS.items():
            with self.subTest(integration_id=integration_id):
                integration = grade_7_integrations[integration_id]
                self.assertEqual(integration["pathIds"], ["optimized", "robust"])
                for field, expected_value in expected.items():
                    self.assertEqual(integration[field], expected_value)

    def test_repository_has_only_the_three_unavailable_grade_7_demand_scenarios(self):
        grade_7_variants = {
            variant["id"]: variant
            for variant in self.time_model["annualVariants"]
            if variant["grade"] == 7
        }
        self.assertEqual(set(grade_7_variants), set(EXPECTED_GRADE_7_VARIANTS))

        for variant_id, (path_id, target_units) in EXPECTED_GRADE_7_VARIANTS.items():
            with self.subTest(variant_id=variant_id):
                variant = grade_7_variants[variant_id]
                allocations = {
                    allocation["moduleId"]: allocation
                    for allocation in variant["allocations"]
                }
                self.assertEqual(variant["kind"], "demand-scenario")
                self.assertEqual(variant["pathId"], path_id)
                self.assertEqual(variant["targetUnits"], target_units)
                self.assertIs(variant["available"], False)
                self.assertEqual(set(allocations), set(EXPECTED_GRADE_7_UNITS))
                self.assertTrue(
                    all(
                        allocation["budgetPathId"] == path_id
                        for allocation in allocations.values()
                    )
                )
                self.assertEqual(
                    sum(allocation["units"] for allocation in allocations.values()),
                    target_units,
                )

    def test_repository_grade_7_judgement_is_red_with_five_unimplemented_options(self):
        judgements = [
            judgement
            for judgement in self.time_model["gradeJudgements"]
            if judgement["grade"] == 7
        ]
        self.assertEqual(len(judgements), 1)
        judgement = judgements[0]
        self.assertEqual(
            {
                "semanticCoverageStatus": judgement["semanticCoverageStatus"],
                "timeFeasibilityStatus": judgement["timeFeasibilityStatus"],
                "sequenceEvidenceStatus": judgement["sequenceEvidenceStatus"],
                "pilotStatus": judgement["pilotStatus"],
            },
            {
                "semanticCoverageStatus": "partial",
                "timeFeasibilityStatus": "red",
                "sequenceEvidenceStatus": "partial",
                "pilotStatus": "not-started",
            },
        )
        self.assertEqual(
            judgement["annualVariantIds"],
            list(EXPECTED_GRADE_7_VARIANTS),
        )
        self.assertEqual(
            judgement["decisionOptions"],
            EXPECTED_GRADE_7_DECISION_OPTIONS,
        )
        self.assertEqual(
            judgement["rationale"],
            EXPECTED_GRADE_7_UNIMPLEMENTED_OPTIONS_RATIONALE,
        )

    def validate_grade_7_model(self, time_model=None):
        model = self.time_model if time_model is None else time_model
        return validate_time_model_draft(model, self.module_payload)

    def test_validator_accepts_the_exact_grade_7_orchestration(self):
        result = self.validate_grade_7_model()

        self.assertIs(result, self.time_model)

    def test_validator_rejects_complete_removal_of_grade_7_orchestration(self):
        adversarial = copy.deepcopy(self.time_model)
        adversarial["moduleContracts"] = [
            contract
            for contract in adversarial["moduleContracts"]
            if contract["grade"] != 7
        ]
        adversarial["integrationContracts"] = [
            integration
            for integration in adversarial["integrationContracts"]
            if integration["id"] not in EXPECTED_GRADE_7_INTEGRATIONS
        ]
        adversarial["annualVariants"] = [
            variant
            for variant in adversarial["annualVariants"]
            if variant["grade"] != 7
        ]
        adversarial["gradeJudgements"] = [
            judgement
            for judgement in adversarial["gradeJudgements"]
            if judgement["grade"] != 7
        ]

        with self.assertRaises(IUM10ValidationError):
            self.validate_grade_7_model(adversarial)

    def test_validator_allows_intermediate_scope_that_excludes_grade_7_modules(self):
        intermediate = copy.deepcopy(self.time_model)
        grade_7_module_ids = {
            contract["moduleId"]
            for contract in intermediate["moduleContracts"]
            if contract["grade"] == 7
        }
        intermediate["moduleContracts"] = [
            contract
            for contract in intermediate["moduleContracts"]
            if contract["grade"] != 7
        ]
        intermediate["integrationContracts"] = [
            integration
            for integration in intermediate["integrationContracts"]
            if integration["id"] not in EXPECTED_GRADE_7_INTEGRATIONS
        ]
        intermediate["annualVariants"] = [
            variant
            for variant in intermediate["annualVariants"]
            if variant["grade"] != 7
        ]
        intermediate["gradeJudgements"] = [
            judgement
            for judgement in intermediate["gradeJudgements"]
            if judgement["grade"] != 7
        ]
        intermediate["privacyContracts"] = [
            contract
            for contract in intermediate["privacyContracts"]
            if contract["moduleId"] not in grade_7_module_ids
        ]
        intermediate_module_payload = {
            "modules": [
                module
                for module in self.module_payload["modules"]
                if module["grade"] != 7
            ]
        }

        result = validate_time_model_draft(
            intermediate,
            intermediate_module_payload,
        )

        self.assertIs(result, intermediate)

    def test_validator_rejects_coupled_removal_of_grade_6_and_grade_7_scope(self):
        adversarial = copy.deepcopy(self.time_model)
        removed_integration_ids = set(EXPECTED_GRADE_6_INTEGRATIONS) | set(
            EXPECTED_GRADE_7_INTEGRATIONS
        )
        adversarial["moduleContracts"] = [
            contract
            for contract in adversarial["moduleContracts"]
            if contract["grade"] != 7
        ]
        for contract in adversarial["moduleContracts"]:
            contract["integrationContractIds"] = [
                integration_id
                for integration_id in contract["integrationContractIds"]
                if integration_id not in removed_integration_ids
            ]
            for budget in contract["pathBudgets"]:
                retained_allocations = [
                    allocation
                    for allocation in budget["sharedAllocations"]
                    if allocation["integrationContractId"]
                    not in removed_integration_ids
                ]
                removed_minutes = sum(
                    allocation["minutes"]
                    for allocation in budget["sharedAllocations"]
                    if allocation["integrationContractId"]
                    in removed_integration_ids
                )
                budget["sharedAllocations"] = retained_allocations
                budget["countedSharedMinutes"] -= removed_minutes
                budget["directMinutes"] += removed_minutes
        adversarial["integrationContracts"] = [
            integration
            for integration in adversarial["integrationContracts"]
            if integration["id"] not in removed_integration_ids
        ]
        adversarial["annualVariants"] = [
            variant
            for variant in adversarial["annualVariants"]
            if variant["grade"] not in {6, 7}
        ]
        adversarial["gradeJudgements"] = [
            judgement
            for judgement in adversarial["gradeJudgements"]
            if judgement["grade"] not in {6, 7}
        ]

        with self.assertRaises(IUM10ValidationError):
            self.validate_grade_7_model(adversarial)

    def test_validator_rejects_any_grade_7_core_matrix_change(self):
        adversarial = copy.deepcopy(self.time_model)
        contract = next(
            contract
            for contract in adversarial["moduleContracts"]
            if contract["moduleId"] == "IUM-7-CORE-01"
        )
        budget = next(
            budget
            for budget in contract["pathBudgets"]
            if budget["pathId"] == "optimized"
        )
        budget["units"] = 6
        budget["minutes"] += 45
        budget["directMinutes"] += 45
        next(
            phase
            for phase in budget["phaseBudgets"]
            if phase["phaseId"] == "guided-practice"
        )["minutes"] += 45
        variant = next(
            variant
            for variant in adversarial["annualVariants"]
            if variant["id"] == "GRADE-7-OPTIMIZED-DEMAND"
        )
        variant["targetUnits"] = 41
        next(
            allocation
            for allocation in variant["allocations"]
            if allocation["moduleId"] == "IUM-7-CORE-01"
        )["units"] = 6

        with self.assertRaises(IUM10ValidationError):
            self.validate_grade_7_model(adversarial)

    def test_validator_rejects_changed_grade_7_cluster_bounds_or_evidence(self):
        mutations = (
            (
                "savings",
                lambda integration: integration["savingsMinutesByPath"].__setitem__(
                    "robust",
                    89,
                ),
            ),
            (
                "participant evidence",
                lambda integration: integration[
                    "preservedProductAndCurriculumEvidence"
                ].pop(),
            ),
        )
        for label, mutate in mutations:
            with self.subTest(label=label):
                adversarial = copy.deepcopy(self.time_model)
                integration = next(
                    integration
                    for integration in adversarial["integrationContracts"]
                    if integration["id"] == "INT-7-DATA-CODING"
                )
                mutate(integration)

                with self.assertRaises(IUM10ValidationError):
                    self.validate_grade_7_model(adversarial)

    def test_public_integration_validator_rejects_arbitrary_grade_7_savings(self):
        contracts = validate_module_contracts(
            self.time_model["moduleContracts"],
            self.module_payload,
        )
        adversarial_integrations = copy.deepcopy(
            self.time_model["integrationContracts"]
        )
        integration = next(
            integration
            for integration in adversarial_integrations
            if integration["id"] == "INT-7-DATA-CODING"
        )
        integration["savingsMinutesByPath"]["optimized"] = 999
        integration["fallback"] = integration["fallback"].replace(
            "optimized: +135 Minuten",
            "optimized: +999 Minuten",
        )

        with self.assertRaises(IUM10ValidationError):
            validate_integration_contracts(
                adversarial_integrations,
                contracts,
            )

    def test_validator_rejects_available_or_normal_grade_7_offerings(self):
        available = copy.deepcopy(self.time_model)
        next(
            variant
            for variant in available["annualVariants"]
            if variant["id"] == "GRADE-7-OPTIMIZED-DEMAND"
        )["available"] = True
        with self.assertRaises(IUM10ValidationError):
            self.validate_grade_7_model(available)

        historical_units = {
            module_id: paths["historical-minimum"]
            for module_id, paths in EXPECTED_GRADE_7_UNITS.items()
        }
        selected_modules_by_target = {
            30: [1, 2, 3, 4, 8],
            34: [1, 2, 3, 4, 5, 7],
            38: [1, 2, 3, 4, 5, 6, 7],
        }
        for target_units, module_numbers in selected_modules_by_target.items():
            with self.subTest(target_units=target_units):
                adversarial = copy.deepcopy(self.time_model)
                module_ids = [
                    f"IUM-7-CORE-{module_number:02d}"
                    for module_number in module_numbers
                ]
                adversarial["annualVariants"].append(
                    {
                        "id": f"GRADE-7-ADVERSARIAL-{target_units}",
                        "grade": 7,
                        "kind": "demand-scenario",
                        "pathId": "historical-minimum",
                        "targetUnits": target_units,
                        "allocations": [
                            {
                                "moduleId": module_id,
                                "budgetPathId": "historical-minimum",
                                "units": historical_units[module_id],
                            }
                            for module_id in module_ids
                        ],
                        "integrationContractIds": [],
                        "available": True,
                        "status": "working",
                        "rationale": "Adversariales normales Klasse-7-Angebot.",
                        "risk": "Der Pfad lässt Kernmodule aus.",
                    }
                )

                with self.assertRaises(IUM10ValidationError):
                    self.validate_grade_7_model(adversarial)

    def test_validator_rejects_flex_as_grade_7_core_replacement(self):
        adversarial = copy.deepcopy(self.time_model)
        variant_id = "GRADE-7-FLEX-REPLACEMENT"
        historical_units = {
            module_id: paths["historical-minimum"]
            for module_id, paths in EXPECTED_GRADE_7_UNITS.items()
        }
        selected_core_ids = [
            "IUM-7-CORE-01",
            "IUM-7-CORE-02",
            "IUM-7-CORE-03",
            "IUM-7-CORE-05",
            "IUM-7-CORE-06",
        ]
        adversarial["annualVariants"].append(
            {
                "id": variant_id,
                "grade": 7,
                "kind": "demand-scenario",
                "pathId": "historical-minimum",
                "targetUnits": 30,
                "allocations": [
                    *[
                        {
                            "moduleId": module_id,
                            "budgetPathId": "historical-minimum",
                            "units": historical_units[module_id],
                        }
                        for module_id in selected_core_ids
                    ],
                    {
                        "moduleId": "IUM-7-EXT-01",
                        "budgetPathId": "standalone",
                        "units": 4,
                    },
                ],
                "integrationContractIds": [],
                "available": True,
                "status": "working",
                "rationale": "Adversarialer Flex-Ersatz für ausgelassene Kernmodule.",
                "risk": "Der flexible Vertrag ersetzt Kernabdeckung.",
            }
        )
        overrides = ium10_validator.ANNUAL_VARIANT_BUDGET_PATH_OVERRIDES
        overrides[variant_id] = {"IUM-7-EXT-01": "standalone"}
        try:
            with self.assertRaises(IUM10ValidationError):
                self.validate_grade_7_model(adversarial)
        finally:
            del overrides[variant_id]

    def test_validator_rejects_green_amber_or_changed_grade_7_options(self):
        for time_status in ("green", "amber"):
            with self.subTest(time_status=time_status):
                adversarial = copy.deepcopy(self.time_model)
                judgement = next(
                    judgement
                    for judgement in adversarial["gradeJudgements"]
                    if judgement["grade"] == 7
                )
                judgement["timeFeasibilityStatus"] = time_status
                with self.assertRaises(IUM10ValidationError):
                    self.validate_grade_7_model(adversarial)

        adversarial = copy.deepcopy(self.time_model)
        judgement = next(
            judgement
            for judgement in adversarial["gradeJudgements"]
            if judgement["grade"] == 7
        )
        judgement["decisionOptions"] = judgement["decisionOptions"][:-1]
        with self.assertRaises(IUM10ValidationError):
            self.validate_grade_7_model(adversarial)

    def test_validator_rejects_contradictory_grade_7_option_rationale(self):
        adversarial = copy.deepcopy(self.time_model)
        judgement = next(
            judgement
            for judgement in adversarial["gradeJudgements"]
            if judgement["grade"] == 7
        )
        judgement["rationale"] = (
            f"{EXPECTED_GRADE_7_UNIMPLEMENTED_OPTIONS_RATIONALE} "
            "Tatsächlich sind alle fünf Folgeoptionen umgesetzt."
        )

        with self.assertRaises(IUM10ValidationError):
            self.validate_grade_7_model(adversarial)

    def test_repository_counts_grade_7_shared_time_only_in_counted_modules(self):
        contracts = validate_module_contracts(
            self.time_model["moduleContracts"],
            self.module_payload,
        )
        integrations = validate_integration_contracts(
            self.time_model["integrationContracts"],
            contracts,
        )

        for integration_id, expected in EXPECTED_GRADE_7_INTEGRATIONS.items():
            integration = integrations[integration_id]
            locations = {
                (module_id, budget["pathId"], allocation["minutes"])
                for module_id, contract in contracts.items()
                for budget in contract["pathBudgets"]
                for allocation in budget["sharedAllocations"]
                if allocation["integrationContractId"] == integration_id
            }
            self.assertEqual(
                locations,
                {
                    (
                        expected["countedInModuleId"],
                        path_id,
                        integration["sharedMinutes"],
                    )
                    for path_id in ("optimized", "robust")
                },
            )


class IUM10SequenceEvidenceTests(unittest.TestCase):
    PRE_TASK24_TIME_REVIEWS_SHA256 = (
        "500eb6a77aea0f0bc5d1804665a3719ceb88b0b577cf9b707c25b4bad0a3f2aa"
    )
    PRE_TASK24_MODULE_CONTRACTS_SHA256 = (
        "187f5df570ea77b8c2168810e99506c9998db6ceadf9f592418cf53fdb720a7c"
    )
    PRE_TASK24_INTEGRATION_CONTRACTS_SHA256 = (
        "9c624435b24c07916993e43e6839c69835d1e3a8b5d69468b6503b6cf6d94b31"
    )
    PRE_TASK24_PRIVACY_CONTRACTS_SHA256 = (
        "80f7f31cc51165ba214202dd36c207217387b4831600eb7e852725bf00c4b23b"
    )
    PRE_TASK24_ANNUAL_VARIANTS_SHA256 = (
        "1c2c3c3b562a16108672175cf8f983bdb02608a2e5d0589abaabbd8a2b6af406"
    )
    PRE_TASK24_PROG34_COVERAGE_SHA256 = (
        "8377a5d1128ff8f8efc58f858ea77ed04cd4c13ca2e2f3876cbbed4da0ff7dbf"
    )
    PRE_TASK24_REMEDIATION_SHA256 = (
        "b0a7ab3aafc7820c8602536675ce98fad03bce924c86c411443ad528888242c5"
    )
    EXPECTED_DECISIONS = {
        "LH26-E-PROG-001": "covered",
        "LH26-E-PROG-002": "covered",
        "LH26-E-PROG-003": "remain-partial",
        "LH26-E-PROG-004": "remain-partial",
    }
    PROG001_ACTION = (
        "Gerätekomponenten, Betriebssystem, Verzeichnisse, Speicherorte und "
        "Zugangsschutz in einem realen Arbeitsauftrag nutzen, erklären und "
        "gegen Störfälle prüfen."
    )
    PROG001_PRODUCT = (
        "Kommentierte System- und Arbeitswegkarte mit eigener Verzeichnisstruktur, "
        "Schutzentscheidungen und Wiederanlauf-Checkliste."
    )
    PROG002_ACTION = (
        "Alltagshandlungen präzisieren, grafische Algorithmen ausführen, "
        "Abweichungen erklären und eine konstante Wiederholung als Grundbaustein "
        "modellieren."
    )
    PROG002_PRODUCT = (
        "Ausführbarer grafischer Algorithmus mit Vorhersage, Laufprotokoll, "
        "reparierter Fassung und begründeter Schleifenentscheidung."
    )

    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.root = root
        self.time_model = json.loads(
            (root / "roadmap/time-model.json").read_text(encoding="utf-8")
        )
        self.coverage_payload = json.loads(
            (root / "roadmap/coverage-plan.json").read_text(encoding="utf-8")
        )
        self.remediation_payload = json.loads(
            (root / "roadmap/coverage-remediation.json").read_text(
                encoding="utf-8"
            )
        )
        module_payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(encoding="utf-8")
        )
        module_contracts = validate_module_contracts(
            self.time_model["moduleContracts"],
            module_payload,
        )
        integration_contracts = validate_integration_contracts(
            self.time_model["integrationContracts"],
            module_contracts,
        )
        self.annual_variants = validate_annual_variants(
            self.time_model["annualVariants"],
            module_contracts,
            integration_contracts,
        )
        privacy_contracts = validate_privacy_contracts(
            self.time_model["privacyContracts"],
            module_contracts,
        )
        self.time_reviews = validate_time_reviews(
            self.time_model["timeReviews"],
            self.remediation_payload,
            module_contracts,
            integration_contracts,
            self.annual_variants,
            require_complete=False,
            privacy_contracts=privacy_contracts,
        )

    @staticmethod
    def _canonical_sha256(value):
        encoded = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def _sequence_records(self):
        records = copy.deepcopy(self.time_model["sequenceEvidence"])
        self.assertEqual(
            len(records),
            4,
            "Task 24 muss vor Mutationsprüfungen vier Sequenznachweise liefern",
        )
        return records

    def _validate(
        self,
        sequence_evidence=None,
        *,
        time_reviews=None,
        annual_variants=None,
        coverage_payload=None,
    ):
        validator = getattr(ium10_validator, "validate_sequence_evidence", None)
        self.assertIsNotNone(
            validator,
            "Task 24 muss die öffentliche validate_sequence_evidence-Schnittstelle bereitstellen",
        )
        return validator(
            self.time_model["sequenceEvidence"]
            if sequence_evidence is None
            else sequence_evidence,
            self.time_reviews if time_reviews is None else time_reviews,
            self.annual_variants
            if annual_variants is None
            else annual_variants,
            self.coverage_payload
            if coverage_payload is None
            else coverage_payload,
        )

    def test_public_sequence_validator_accepts_exact_repository_contract(self):
        result = self._validate()

        self.assertEqual(set(result), set(self.EXPECTED_DECISIONS))
        for competency_id, decision in self.EXPECTED_DECISIONS.items():
            with self.subTest(competency_id=competency_id):
                evidence = result[competency_id]
                self.assertEqual(evidence["id"], f"SE-{competency_id}")
                self.assertEqual(
                    evidence["timeReviewId"],
                    f"TR-{competency_id}",
                )
                self.assertEqual(evidence["fachAuditStatus"], "passed")
                self.assertEqual(evidence["coverageDecision"], decision)
                self.assertEqual(evidence["status"], "working")

    def test_repository_sequence_scopes_and_time_weights_are_exact(self):
        result = self._validate()
        grade_5_core = {f"IUM-5-CORE-{number:02d}" for number in range(1, 8)}
        grade_6_core = {f"IUM-6-CORE-{number:02d}" for number in range(1, 8)}
        grade_7_core = {f"IUM-7-CORE-{number:02d}" for number in range(1, 11)}

        self.assertEqual(result["LH26-E-PROG-001"]["grades"], [5, 6])
        self.assertEqual(
            set(result["LH26-E-PROG-001"]["moduleIds"]),
            grade_5_core | grade_6_core,
        )
        self.assertEqual(result["LH26-E-PROG-002"]["grades"], [5, 6, 7])
        self.assertEqual(
            result["LH26-E-PROG-002"]["moduleIds"],
            [
                "IUM-5-CORE-05",
                "IUM-6-CORE-04",
                "IUM-7-CORE-03",
                "IUM-7-CORE-04",
            ],
        )
        for competency_id in ("LH26-E-PROG-003", "LH26-E-PROG-004"):
            with self.subTest(competency_id=competency_id):
                evidence = result[competency_id]
                self.assertEqual(evidence["grades"], [7])
                self.assertEqual(set(evidence["moduleIds"]), grade_7_core)
                weights = {
                    item["variantId"]: {
                        group["id"]: group["units"]
                        for group in item["weightGroups"]
                    }
                    for item in evidence["timeEvidence"]
                }
                self.assertEqual(
                    weights,
                    {
                        "GRADE-7-OPTIMIZED-DEMAND": {
                            "core-01-07": 30,
                            "core-08-10": 10,
                        },
                        "GRADE-7-ROBUST-DEMAND": {
                            "core-01-07": 31,
                            "core-08-10": 15,
                        },
                        "GRADE-7-HISTORICAL-MINIMUM": {
                            "core-01-07": 38,
                            "core-08-10": 16,
                        },
                    },
                )

    def test_sequence_validator_rejects_identity_scope_and_depth_mutations(self):
        mutations = (
            ("duplicate id", lambda records: records.append(copy.deepcopy(records[0]))),
            (
                "unknown record",
                lambda records: records[0].__setitem__(
                    "competencyId", "LH26-E-PROG-999"
                ),
            ),
            (
                "wrong review binding",
                lambda records: records[0].__setitem__(
                    "timeReviewId", "TR-LH26-E-PROG-002"
                ),
            ),
            ("missing grade", lambda records: records[0]["grades"].pop()),
            ("missing module", lambda records: records[0]["moduleIds"].pop()),
            (
                "empty progression",
                lambda records: records[0]["progression"][0].__setitem__(
                    "learningDepth", ""
                ),
            ),
            (
                "empty product depth",
                lambda records: records[1]["operatorProductDepth"][0].__setitem__(
                    "productDepth", ""
                ),
            ),
            (
                "single perspective proxy",
                lambda records: records[2].__setitem__(
                    "perspectiveWeighting",
                    records[2]["perspectiveWeighting"][:1],
                ),
            ),
            (
                "private evidence included",
                lambda records: records[2]["evidenceBoundary"].__setitem__(
                    "privateEvidence", "included"
                ),
            ),
            (
                "single module proxy included",
                lambda records: records[3]["evidenceBoundary"].__setitem__(
                    "singleModuleProxy", "included"
                ),
            ),
            (
                "automatic personal assessment included",
                lambda records: records[3]["evidenceBoundary"].__setitem__(
                    "automatedPersonalAssessment", "included"
                ),
            ),
        )
        for label, mutate in mutations:
            with self.subTest(mutation=label):
                records = self._sequence_records()
                mutate(records)
                with self.assertRaises(IUM10ValidationError):
                    self._validate(records)

    def test_sequence_validator_rejects_nonzero_or_allocated_roadmap_review(self):
        mutations = (
            ("decision", "covered"),
            ("additionalMinutes", 5),
            ("phaseIds", ["build-concept"]),
            ("integrationContractIds", ["INT-7-PROGRAMMING"]),
            ("pathAvailability", ["GRADE-5-BASELINE"]),
            ("sequenceEvidenceId", "SE-WRONG"),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                reviews = copy.deepcopy(self.time_reviews)
                reviews["TR-LH26-E-PROG-001"][field] = value
                with self.assertRaises(IUM10ValidationError):
                    self._validate(time_reviews=reviews)

    def test_sequence_validator_derives_availability_and_units_from_variants(self):
        mutations = (
            (
                "unknown variant",
                lambda item: item.__setitem__("variantId", "GRADE-5-UNKNOWN"),
            ),
            (
                "wrong availability",
                lambda item: item.__setitem__("available", False),
            ),
            (
                "wrong target units",
                lambda item: item.__setitem__("targetUnits", 31),
            ),
            (
                "wrong scoped units",
                lambda item: item.__setitem__("scopeUnits", 29),
            ),
            (
                "wrong scoped modules",
                lambda item: item["scopeModuleIds"].pop(),
            ),
        )
        for label, mutate in mutations:
            with self.subTest(mutation=label):
                records = self._sequence_records()
                mutate(records[0]["timeEvidence"][0])
                with self.assertRaises(IUM10ValidationError):
                    self._validate(records)

        records = self._sequence_records()
        records[2]["timeEvidence"][0]["weightGroups"][0]["units"] = 29
        with self.assertRaises(IUM10ValidationError):
            self._validate(records)

    def test_covered_requires_passed_audit_and_a_genuinely_available_path(self):
        records = self._sequence_records()
        records[0]["fachAuditStatus"] = "failed"
        with self.assertRaises(IUM10ValidationError):
            self._validate(records)

        records = self._sequence_records()
        variants = copy.deepcopy(self.annual_variants)
        for item in records[0]["timeEvidence"]:
            item["available"] = False
            variants[item["variantId"]]["available"] = False
        with self.assertRaises(IUM10ValidationError):
            self._validate(records, annual_variants=variants)

    def test_prog003_and_prog004_cannot_be_covered_by_unavailable_grade7_scenarios(self):
        for competency_id in ("LH26-E-PROG-003", "LH26-E-PROG-004"):
            with self.subTest(competency_id=competency_id):
                records = self._sequence_records()
                evidence = next(
                    item for item in records
                    if item["competencyId"] == competency_id
                )
                evidence["coverageDecision"] = "covered"
                evidence["coverageConsequence"] = {
                    "coverageStatus": "covered",
                    "semanticAudit": "operator-product-match",
                    "rationale": "Die roten Bedarfsszenarien genügen angeblich.",
                }
                coverage = copy.deepcopy(self.coverage_payload)
                entry = next(
                    item for item in coverage["entries"]
                    if item["competencyId"] == competency_id
                )
                entry["coverageStatus"] = "covered"
                entry["semanticAudit"] = "operator-product-match"
                with self.assertRaises(IUM10ValidationError):
                    self._validate(records, coverage_payload=coverage)

    def test_coverage_decision_and_original_strings_are_fail_closed(self):
        coverage = copy.deepcopy(self.coverage_payload)
        entry = next(
            item for item in coverage["entries"]
            if item["competencyId"] == "LH26-E-PROG-001"
        )
        entry["coverageStatus"] = "partial"
        entry["semanticAudit"] = "documented-gap"
        with self.assertRaises(IUM10ValidationError):
            self._validate(coverage_payload=coverage)

        anchors = {
            "LH26-E-PROG-001": (self.PROG001_ACTION, self.PROG001_PRODUCT),
            "LH26-E-PROG-002": (self.PROG002_ACTION, self.PROG002_PRODUCT),
        }
        for competency_id, (action, product) in anchors.items():
            for field, anchor in (("evidence", action), ("matchRationale", product)):
                with self.subTest(competency_id=competency_id, field=field):
                    coverage = copy.deepcopy(self.coverage_payload)
                    entry = next(
                        item for item in coverage["entries"]
                        if item["competencyId"] == competency_id
                    )
                    entry[field] = entry[field].replace(anchor, "entfernt")
                    with self.assertRaises(IUM10ValidationError):
                        self._validate(coverage_payload=coverage)

    def test_task24_preserves_time_model_and_prog003_prog004_inputs(self):
        self.assertEqual(len(self.time_model["timeReviews"]), 60)
        self.assertEqual(
            self._canonical_sha256(self.time_model["timeReviews"]),
            self.PRE_TASK24_TIME_REVIEWS_SHA256,
        )
        for field, expected in (
            ("moduleContracts", self.PRE_TASK24_MODULE_CONTRACTS_SHA256),
            (
                "integrationContracts",
                self.PRE_TASK24_INTEGRATION_CONTRACTS_SHA256,
            ),
            ("privacyContracts", self.PRE_TASK24_PRIVACY_CONTRACTS_SHA256),
            ("annualVariants", self.PRE_TASK24_ANNUAL_VARIANTS_SHA256),
        ):
            with self.subTest(field=field):
                self.assertEqual(
                    self._canonical_sha256(self.time_model[field]),
                    expected,
                )
        prog34 = [
            entry for entry in self.coverage_payload["entries"]
            if entry["competencyId"]
            in {"LH26-E-PROG-003", "LH26-E-PROG-004"}
        ]
        self.assertEqual(
            self._canonical_sha256(prog34),
            self.PRE_TASK24_PROG34_COVERAGE_SHA256,
        )
        self.assertEqual(
            self._canonical_sha256(self.remediation_payload),
            self.PRE_TASK24_REMEDIATION_SHA256,
        )

    def test_grade_sequence_statuses_follow_the_four_sequence_decisions(self):
        judgements = {
            item["grade"]: item for item in self.time_model["gradeJudgements"]
        }
        self.assertEqual(
            {
                grade: judgement["sequenceEvidenceStatus"]
                for grade, judgement in judgements.items()
            },
            {5: "covered", 6: "covered", 7: "partial"},
        )
        self.assertEqual(
            {
                grade: judgement["timeFeasibilityStatus"]
                for grade, judgement in judgements.items()
            },
            {5: "green", 6: "green", 7: "red"},
        )

    def test_task24_does_not_add_task25_cross_artifact_references(self):
        for entry in self.coverage_payload["entries"]:
            if entry["competencyId"] in self.EXPECTED_DECISIONS:
                self.assertNotIn("timeReviewId", entry)
                self.assertNotIn("sequenceEvidenceId", entry)
        for entry in self.remediation_payload["entries"]:
            self.assertNotIn("timeReviewId", entry)
            self.assertNotIn("sequenceEvidenceId", entry)
