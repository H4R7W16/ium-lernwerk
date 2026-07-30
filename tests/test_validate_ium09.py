import copy
import json
import unittest
from pathlib import Path

from scripts.validate_ium09 import (
    BASELINE_PARTIAL_IDS,
    BASELINE_MODULE_STRUCTURE_FINGERPRINT_SHA256,
    IUM09ValidationError,
    coverage_baseline_fingerprint,
    module_structure_fingerprint,
    validate_coverage_evidence,
    validate_ium09,
    validate_remediation_ledger,
    validate_remediated_coverage,
)


PRIVATE_BOUNDARY_TEXT = (
    "Das private lokale Artefakt wird nicht erhoben, übertragen, "
    "eingesammelt, gespeichert oder bewertet."
)

INTEGRATED_PRIVATE_PRODUCT = "integrierten privaten lokalen Reflexionsmatrix"
COMMON_CASE_PRODUCT = "gemeinsamen teilbaren fallbezogenen Wirkungskarte"
COMMON_CASE = "vollständig vorgegebenen gemeinsamen fiktiven Fall"
MG001_CRITERIA = (
    "Kriterienbasis: vollständig vorgegebener, im nichtpersonalen Auftrag "
    "enthaltener altersbezogener Kriterienkatalog."
)
CORE08_SHARED_DOSSIER = "desselben geteilten Evidenz- und Entscheidungsdossiers"
CORE08_COMMON_MATERIAL = (
    "dieselben kuratierten Dienst- und Falschmeldungsfälle, Akteursdaten, "
    "Belege, Gegenbelege, Kriterien und die gemeinsame Revision"
)
CORE08_FALSE_INFORMATION_CASE = (
    "vollständig vorgegebenen kuratierten manipulativen Falschmeldungsfall"
)
CORE03_LOCAL_PROJECT = (
    "desselben tatsächlichen lokalen Mini-Projekts zur gemeinsamen "
    "Überarbeitung des bereits vorhandenen Kommunikationsleitfadens"
)
CORE03_SHARED_PRODUCT = (
    "desselben gemeinsam revidierten Kommunikationsleitfadens mit "
    "integrierten Fallkarten"
)
CORE03_SAFE_CONTENT = "ausschließlich neutrale und fiktive Inhalte"
CORE03_DATA_BOUNDARY = (
    "Zugangsdaten, private Nachrichten, personenbezogene Inhalte und "
    "vollständige Kommunikationsprotokolle werden weder erhoben noch gespeichert"
)
CORE02_INTEGRATED_TRACE = (
    "integrierte Belegspur derselben belegten Antwort oder dokumentierten Revision"
)
CORE06_COMMON_PRODUCT = (
    "demselben adressatengerechten Informationsprodukt mit integrierter "
    "Gestaltungsbegründung und Vorher-Nachher-Revision"
)
CORE06_RIGHTS_PRIVACY_TRACE = "getrennte Rechte- und Datenschutzspur"
CORE06_TEXT_FORMAT_TRACE = "Baustein- und Formatierungsspur"
CORE06_IMAGE_TRACE = "Bildnutzungs- und Gestaltungsentscheidung"
CORE06_GIVEN_DESIGN_TRACE = (
    "kriterien- und beleggebundene Analyse- und Urteilsspur der "
    "vorgegebenen Gestaltung"
)
CORE6_CORE02_COMMON_MODEL = "desselben teilbaren Datenfluss- und Auswahlmodells"
CORE6_CORE02_CONDITIONS_LAYER = "klar beschrifteten Bedingungen-Matrix"
CORE6_CORE02_AD_PATH_LAYER = "klar beschrifteten Werbeauswahlpfaden"
CORE6_CORE02_CURATED_CASES = (
    "ausschließlich kuratierte fiktive oder neutralisierte "
    "Fall- und Bedingungsdaten"
)
CORE6_CORE02_PRIVACY_BOUNDARY = (
    "keine realen Konten, Profile, Werbeverläufe, Standort- oder "
    "Nutzungsdaten, Screenshots personalisierter Werbung oder "
    "personenbezogene Selbstauskünfte"
)
CORE7_CORE03_TRACE_PRODUCT = (
    "sechs synchron verknüpften Ansichten/Spalten desselben vorhandenen "
    "Code-, Ablauf- und Zustandstraceprodukts"
)
CORE7_CORE03_COMMON_TRACE = (
    "demselben Programmfall, denselben Ausführungspositionen, Eingaben, "
    "Werten, Ausgaben und derselben korrigierten Fassung"
)


EXPECTED_CAUSE_CLASS_BY_ID = {
    **dict.fromkeys(
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
        },
        "module-detail",
    ),
    **dict.fromkeys(
        {
            "BMB16-GYM-IK-GM-002", "BMB16-GYM-IK-KK-002",
            "BMB16-GYM-IK-KK-003", "BMB16-GYM-PK-HK-003",
            "BMB16-GYM-PK-SK-003", "INF7-16-GYM-PK-SV-001",
            "LH26-E-DA-015", "LH26-E-DP-001", "LH26-E-KS-001",
        },
        "school-context",
    ),
    **dict.fromkeys(
        {
            "BMB16-GYM-IK-MG-001", "BMB16-GYM-IK-MG-003",
            "BMB16-GYM-PK-RK-001", "BMB16-GYM-PK-RK-002",
            "BMB16-GYM-PK-RK-003", "LH26-E-DP-003", "LH26-E-DP-013",
            "LH26-E-DP-014",
        },
        "private-local",
    ),
    **dict.fromkeys(
        {
            "LH26-E-PROG-001", "LH26-E-PROG-002",
            "LH26-E-PROG-003", "LH26-E-PROG-004",
        },
        "roadmap-level",
    ),
}

AUDITED_DECISIONS = {
    "BMB16-GYM-IK-GM-001": ("IUM-5-CORE-01", "module-detail", "covered"),
    "BMB16-GYM-IK-GM-002": ("IUM-5-CORE-01", "school-context", "covered"),
    "BMB16-GYM-IK-GM-003": (
        "IUM-5-CORE-01", "module-detail", "remain-partial"
    ),
    "BMB16-GYM-PK-SK-003": ("IUM-5-CORE-01", "school-context", "covered"),
    "LH26-E-DA-004": ("IUM-5-CORE-01", "module-detail", "covered"),
    "LH26-E-DP-001": ("IUM-5-CORE-01", "school-context", "covered"),
    "LH26-E-PROG-001": ("IUM-5-CORE-01", "roadmap-level", "remain-partial"),
    "LH26-E-PROG-002": ("IUM-5-CORE-05", "roadmap-level", "remain-partial"),
    "LH26-E-PROG-003": ("IUM-7-CORE-08", "roadmap-level", "remain-partial"),
    "LH26-E-PROG-004": ("IUM-7-CORE-08", "roadmap-level", "remain-partial"),
    "BMB16-GYM-IK-MG-001": ("IUM-5-CORE-07", "private-local", "covered"),
    "BMB16-GYM-IK-MG-002": ("IUM-5-CORE-07", "module-detail", "covered"),
    "BMB16-GYM-IK-MG-003": ("IUM-5-CORE-07", "private-local", "covered"),
    "BMB16-GYM-PK-RK-001": ("IUM-5-CORE-07", "private-local", "covered"),
    "BMB16-GYM-PK-RK-002": ("IUM-5-CORE-07", "private-local", "covered"),
    "BMB16-GYM-PK-RK-003": (
        "IUM-5-CORE-07", "private-local", "remain-partial"
    ),
    "LH26-E-DP-003": ("IUM-5-CORE-07", "private-local", "remain-partial"),
    "INF7-16-GYM-IK-IGD-006": (
        "IUM-7-CORE-08", "module-detail", "covered"
    ),
    "INF7-16-GYM-PK-AB-005": (
        "IUM-7-CORE-08", "module-detail", "covered"
    ),
    "INF7-16-GYM-PK-AB-006": (
        "IUM-7-CORE-08", "module-detail", "covered"
    ),
    "INF7-16-GYM-PK-KK-006": (
        "IUM-7-CORE-08", "module-detail", "covered"
    ),
    "LH26-E-DP-013": ("IUM-7-CORE-08", "private-local", "covered"),
    "BMB16-GYM-IK-KK-002": (
        "IUM-5-CORE-03", "school-context", "covered"
    ),
    "BMB16-GYM-IK-KK-003": (
        "IUM-5-CORE-03", "school-context", "covered"
    ),
    "BMB16-GYM-PK-HK-003": (
        "IUM-5-CORE-03", "school-context", "covered"
    ),
    "BMB16-GYM-PK-RK-004": (
        "IUM-5-CORE-03", "module-detail", "covered"
    ),
    "LH26-E-KS-001": ("IUM-5-CORE-03", "school-context", "covered"),
    "LH26-E-KS-002": ("IUM-5-CORE-03", "module-detail", "covered"),
    "LH26-E-ALG-001": ("IUM-5-CORE-05", "module-detail", "covered"),
    "INF7-16-GYM-IK-ALG-003": (
        "IUM-7-CORE-03", "module-detail", "covered"
    ),
    "INF7-16-GYM-PK-MI-005": (
        "IUM-7-CORE-03", "module-detail", "covered"
    ),
    "INF7-16-GYM-PK-SV-003": (
        "IUM-7-CORE-03", "module-detail", "covered"
    ),
    "LH26-E-ALG-007": ("IUM-7-CORE-03", "module-detail", "covered"),
    "LH26-E-ALG-008": ("IUM-7-CORE-03", "module-detail", "covered"),
    "LH26-E-ALG-009": ("IUM-7-CORE-03", "module-detail", "covered"),
    "LH26-E-ID-009": ("IUM-5-CORE-02", "module-detail", "covered"),
    "BMB16-GYM-IK-PP-002": (
        "IUM-5-CORE-06", "module-detail", "covered"
    ),
    "LH26-E-DA-005": ("IUM-5-CORE-06", "module-detail", "covered"),
    "LH26-E-DA-006": ("IUM-5-CORE-06", "module-detail", "covered"),
    "LH26-E-DA-008": ("IUM-5-CORE-06", "module-detail", "covered"),
    "LH26-E-DP-004": ("IUM-6-CORE-02", "module-detail", "covered"),
    "LH26-E-DP-006": ("IUM-6-CORE-02", "module-detail", "covered"),
}


def core_module(**overrides):
    module = {
        "id": "IUM-5-CORE-01",
        "grade": 5,
        "kind": "core",
        "competencyIds": ["BMB16-GYM-IK-GM-001"],
        "prerequisiteModuleIds": [],
        "lessonRange": {"min": 5, "max": 7},
    }
    module.update(overrides)
    return module


def module_payload(*modules):
    return {"modules": list(modules)}


def curriculum_contracts():
    return {
        "BMB16-GYM-IK-GM-001": {"text": "Konkrete Kompetenz."},
        "BMB16-GYM-IK-GM-002": {"text": "Zweite Kompetenz."},
        "BMB16-GYM-IK-GM-003": {"text": "Dritte Kompetenz."},
        "BMB16-GYM-IK-KK-002": {
            "text": (
                "einen digitalen Kommunikationsweg (zum Beispiel E-Mail) "
                "in seinen Grundfunktionen anwenden"
            )
        },
        "BMB16-GYM-IK-KK-003": {
            "text": (
                "mindestens einen digitalen Kommunikationsweg zur Kooperation "
                "und zum Austausch innerhalb von Projekten nutzen"
            )
        },
        "BMB16-GYM-PK-HK-003": {
            "text": "Medien für Zusammenarbeit und Kooperation nutzen"
        },
        "BMB16-GYM-PK-RK-004": {
            "text": (
                "Übertretungen rechtlicher und moralischer Grenzen in der "
                "digitalen Welt erkennen und daraus Regeln für das eigene "
                "soziale Verhalten ableiten"
            )
        },
        "BMB16-GYM-IK-PP-002": {
            "text": (
                "bei der Erstellung eines digitalen Medienprodukts erste "
                "grundlegende Urheberrechts- und Datenschutzrichtlinien "
                "beachten"
            )
        },
        "BMB16-GYM-IK-MG-001": {
            "text": (
                "die persönliche Motivation bezüglich des eigenen "
                "Medienverhaltens beschreiben und die eigene Nutzung ihrem "
                "Alter entsprechend bewerten"
            )
        },
        "BMB16-GYM-IK-MG-002": {
            "text": (
                "die positiven Aspekte der Mediennutzung, aber auch die "
                "Risiken und Gefahren des (übermäßigen) Mediengebrauchs "
                "erläutern, bewerten und präventive Maßnahmen benennen"
            )
        },
        "BMB16-GYM-IK-MG-003": {
            "text": (
                "die Wirkung von Medien an Beispielen untersuchen, ihre "
                "Empfindungen dazu äußern und erste Gesetzmäßigkeiten ableiten"
            )
        },
        "BMB16-GYM-PK-RK-001": {
            "text": (
                "anknüpfend an ihre eigenen Erfahrungen das Nutzungsverhalten "
                "beschreiben und vergleichen"
            )
        },
        "BMB16-GYM-PK-RK-002": {
            "text": (
                "den Einfluss der digitalen Medien auf ihre Lebenswelt "
                "darstellen und Wirklichkeit mit Medienwirklichkeit in "
                "Beziehung setzen"
            )
        },
        "BMB16-GYM-PK-RK-003": {
            "text": (
                "Auswirkungen der medialen Selbstdarstellung abschätzen und "
                "in Grundzügen bewerten"
            )
        },
        "INF7-16-GYM-IK-IGD-006": {
            "text": (
                "den Sachverhalt der permanent anfallenden personenbezogenen "
                "Daten bei der Nutzung von Diensten und deren Speicherung an "
                "alltagsrelevanten Beispielen erläutern und dabei sowohl "
                "Nutzen als auch Risiken nennen"
            )
        },
        "INF7-16-GYM-PK-AB-005": {
            "text": (
                "Auswirkungen von Computersystemen auf Gesellschaft, "
                "Berufswelt und persönliches Lebensumfeld aus verschiedenen "
                "Perspektiven bewerten"
            )
        },
        "INF7-16-GYM-PK-AB-006": {
            "text": (
                "im Zusammenhang mit einer digitalisierten Gesellschaft einen "
                "eigenen Standpunkt zu ethischen Fragen in der Informatik "
                "einnehmen und ihn argumentativ vertreten"
            )
        },
        "INF7-16-GYM-PK-KK-006": {
            "text": (
                "Aspekte von Toleranz und Akzeptanz von Vielfalt im Kontext "
                "informatischer Fragestellungen diskutieren"
            )
        },
        "INF7-16-GYM-IK-ALG-003": {
            "text": "Variablen als änderbaren Wertespeicher erläutern"
        },
        "INF7-16-GYM-PK-MI-005": {
            "text": (
                "geeignete Programme und Hilfsmittel zur grafisch gestützten "
                "Modellierung einsetzen"
            )
        },
        "INF7-16-GYM-PK-SV-003": {
            "text": "Beziehungen zwischen Daten/Objekten erkennen und erläutern"
        },
        "LH26-E-ALG-007": {
            "text": (
                "algorithmische Grundbausteine beschreiben: • Anweisung • "
                "Schleife (Variante mit konstanter Anzahl von Durchläufen und "
                "Variante mit Bedingung) • Verzweigung • Ausdrücke ohne "
                "Operatoren, mit arithmetischen Operatoren und mit "
                "Vergleichsoperatoren"
            )
        },
        "LH26-E-ALG-008": {
            "text": (
                "Übergabe und Rückgabe von Werten bei gegebenen Anweisungen "
                "und Ausdrücken identifizieren"
            )
        },
        "LH26-E-ALG-009": {
            "text": (
                "den Datentyp (Zeichenkette, Zahl, Wahrheitswert) von Werten "
                "und Ausdrücken identifizieren"
            )
        },
        "LH26-E-DP-013": {
            "text": (
                "sich mit in manipulativer Absicht verbreiteten "
                "Falschmeldungen im digitalen Raum auseinandersetzen und den "
                "eigenen Umgang damit reflektieren"
            )
        },
        "LH26-E-ALG-001": {
            "text": (
                "digitale Systeme identifizieren, deren Funktionsweise "
                "wesentlich durch algorithmische Prozesse bestimmt ist"
            )
        },
        "LH26-E-KS-001": {
            "text": (
                "schulische Kommunikationskanäle und Möglichkeiten zur "
                "Kollaboration nutzen"
            )
        },
        "LH26-E-KS-002": {
            "text": (
                "Auswirkungen von Konflikten und Problemen bei der digitalen "
                "Kommunikation reflektieren und diskutieren"
            )
        },
        "LH26-E-ID-009": {
            "text": (
                "Strategien anwenden, um Informationen mit Vorwissen zu "
                "verknüpfen und für eine gegebene Fragestellung "
                "weiterzuverarbeiten"
            )
        },
        "LH26-E-DA-005": {
            "text": (
                "Bausteine eines Textes identifizieren und Möglichkeiten zu "
                "ihrer Formatierung nutzen"
            )
        },
        "LH26-E-DA-006": {
            "text": "eine Objektart zur visuellen Gestaltung nutzen"
        },
        "LH26-E-DA-008": {
            "text": (
                "die Wirkung einer vorgegebenen Gestaltung beurteilen und "
                "den Zusammenhang von Inhalt und Form analysieren"
            )
        },
        "LH26-E-DP-004": {
            "text": (
                "Nutzungs- und Rahmenbedingungen von Apps, Programmen und "
                "Onlinediensten exemplarisch herausarbeiten"
            )
        },
        "LH26-E-DP-006": {
            "text": (
                "Möglichkeiten nennen, wie die spezifische Auswahl der "
                "Werbebotschaft zustande kommt"
            )
        },
    }


def evidence_contract(**overrides):
    contract = {
        "id": "CE-IUM-5-CORE-01-BMB16-GYM-IK-GM-001",
        "competencyId": "BMB16-GYM-IK-GM-001",
        "mode": "module-detail",
        "learningAction": "Die Kompetenz fachlich ausführen.",
        "productEvidence": "Die fachliche Produktspur.",
        "productVisibility": "shared",
    }
    contract.update(overrides)
    return contract


def school_context_contract(**overrides):
    contract = evidence_contract(
        mode="school-context",
        executionType="actual-local-use",
        localConfigurationRequirement="Die lokale Schulumgebung wird verwendet.",
    )
    contract.update(overrides)
    return contract


def private_local_contract(**overrides):
    contract = evidence_contract(
        mode="private-local",
        productVisibility="private-local",
        privacyBoundary=PRIVATE_BOUNDARY_TEXT,
        nonPersonalFollowUp="Ein fiktiver Fall wird fachlich beurteilt.",
    )
    contract.update(overrides)
    return contract


class ValidateCoverageEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        cls.repository_payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(encoding="utf-8")
        )

    def validate(self, *contracts, module=None):
        payload = copy.deepcopy(self.repository_payload)
        module = payload["modules"][0] if module is None else module
        if module is not payload["modules"][0]:
            payload["modules"][0] = module
        module["coverageEvidence"] = list(contracts)
        return validate_coverage_evidence(
            payload, curriculum_contracts()
        )

    def test_accepts_all_valid_evidence_modes(self):
        second = school_context_contract(
            id="CE-IUM-5-CORE-01-BMB16-GYM-IK-GM-002",
            competencyId="BMB16-GYM-IK-GM-002",
        )
        private = private_local_contract(
            id="CE-IUM-5-CORE-01-BMB16-GYM-IK-GM-003",
            competencyId="BMB16-GYM-IK-GM-003",
        )
        result = self.validate(evidence_contract(), second, private)
        self.assertEqual(
            set(result),
            {
                "CE-IUM-5-CORE-01-BMB16-GYM-IK-GM-001",
                "CE-IUM-5-CORE-01-BMB16-GYM-IK-GM-002",
                "CE-IUM-5-CORE-01-BMB16-GYM-IK-GM-003",
                "CE-IUM-5-CORE-03-BMB16-GYM-IK-KK-002",
                "CE-IUM-5-CORE-03-BMB16-GYM-IK-KK-003",
                "CE-IUM-5-CORE-03-BMB16-GYM-PK-HK-003",
                "CE-IUM-5-CORE-03-BMB16-GYM-PK-RK-004",
                "CE-IUM-5-CORE-03-LH26-E-KS-001",
                "CE-IUM-5-CORE-03-LH26-E-KS-002",
                "CE-IUM-5-CORE-02-LH26-E-ID-009",
                "CE-IUM-5-CORE-07-BMB16-GYM-IK-MG-001",
                "CE-IUM-5-CORE-07-BMB16-GYM-IK-MG-002",
                "CE-IUM-5-CORE-07-BMB16-GYM-IK-MG-003",
                "CE-IUM-5-CORE-07-BMB16-GYM-PK-RK-001",
                "CE-IUM-5-CORE-07-BMB16-GYM-PK-RK-002",
                "CE-IUM-7-CORE-08-INF7-16-GYM-IK-IGD-006",
                "CE-IUM-7-CORE-08-INF7-16-GYM-PK-AB-005",
                "CE-IUM-7-CORE-08-INF7-16-GYM-PK-AB-006",
                "CE-IUM-7-CORE-08-INF7-16-GYM-PK-KK-006",
                "CE-IUM-7-CORE-08-LH26-E-DP-013",
                "CE-IUM-7-CORE-03-INF7-16-GYM-IK-ALG-003",
                "CE-IUM-7-CORE-03-INF7-16-GYM-PK-MI-005",
                "CE-IUM-7-CORE-03-INF7-16-GYM-PK-SV-003",
                "CE-IUM-7-CORE-03-LH26-E-ALG-007",
                "CE-IUM-7-CORE-03-LH26-E-ALG-008",
                "CE-IUM-7-CORE-03-LH26-E-ALG-009",
                "CE-IUM-5-CORE-05-LH26-E-ALG-001",
                "CE-IUM-5-CORE-06-BMB16-GYM-IK-PP-002",
                "CE-IUM-5-CORE-06-LH26-E-DA-005",
                "CE-IUM-5-CORE-06-LH26-E-DA-006",
                "CE-IUM-5-CORE-06-LH26-E-DA-008",
                "CE-IUM-6-CORE-02-LH26-E-DP-004",
                "CE-IUM-6-CORE-02-LH26-E-DP-006",
            },
        )
        self.assertEqual(result[private["id"]]["mode"], "private-local")

    def test_rejects_unknown_competency(self):
        contract = evidence_contract(competencyId="UNKNOWN")
        contract["id"] = "CE-IUM-5-CORE-01-UNKNOWN"
        with self.assertRaisesRegex(IUM09ValidationError, "unknown competency"):
            self.validate(contract)

    def test_rejects_contract_for_flexible_module(self):
        module = core_module(kind="extension")
        with self.assertRaisesRegex(IUM09ValidationError, "core module"):
            self.validate(evidence_contract(), module=module)

    def test_rejects_duplicate_contract_id(self):
        with self.assertRaisesRegex(IUM09ValidationError, "unique"):
            self.validate(evidence_contract(), evidence_contract())

    def test_rejects_id_that_does_not_encode_module_and_competency(self):
        contract = evidence_contract(id="CE-IUM-5-CORE-01-WRONG")
        with self.assertRaisesRegex(IUM09ValidationError, "id"):
            self.validate(contract)

    def test_rejects_invalid_evidence_mode(self):
        with self.assertRaisesRegex(IUM09ValidationError, "mode"):
            self.validate(evidence_contract(mode="roadmap-level"))

    def test_rejects_invalid_product_visibility(self):
        with self.assertRaisesRegex(IUM09ValidationError, "visibility"):
            self.validate(evidence_contract(productVisibility="public"))

    def test_rejects_private_local_visibility_for_module_detail(self):
        with self.assertRaisesRegex(IUM09ValidationError, "module-detail"):
            self.validate(evidence_contract(productVisibility="private-local"))

    def test_rejects_private_local_visibility_for_school_context(self):
        with self.assertRaisesRegex(IUM09ValidationError, "school-context"):
            self.validate(
                school_context_contract(productVisibility="private-local")
            )

    def test_rejects_empty_coverage_evidence_when_field_is_present(self):
        payload = copy.deepcopy(self.repository_payload)
        payload["modules"][0]["coverageEvidence"] = []
        with self.assertRaisesRegex(IUM09ValidationError, "nonempty"):
            validate_coverage_evidence(payload, curriculum_contracts())

    def test_requires_actual_local_use_for_school_context(self):
        with self.assertRaisesRegex(IUM09ValidationError, "actual-local-use"):
            self.validate(school_context_contract(executionType="simulation"))

    def test_requires_local_configuration_for_school_context(self):
        contract = school_context_contract()
        del contract["localConfigurationRequirement"]
        with self.assertRaisesRegex(IUM09ValidationError, "localConfigurationRequirement"):
            self.validate(contract)

    def test_rejects_private_local_contract_with_nonprivate_visibility(self):
        with self.assertRaisesRegex(IUM09ValidationError, "private-local"):
            self.validate(private_local_contract(productVisibility="shared"))

    def test_requires_exact_private_boundary(self):
        with self.assertRaisesRegex(IUM09ValidationError, "privacyBoundary"):
            self.validate(private_local_contract(privacyBoundary="Nicht speichern."))

    def test_requires_nonpersonal_follow_up_for_private_local(self):
        contract = private_local_contract()
        del contract["nonPersonalFollowUp"]
        with self.assertRaisesRegex(IUM09ValidationError, "nonPersonalFollowUp"):
            self.validate(contract)


class Core07RepositoryOrchestrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(encoding="utf-8")
        )
        module = next(
            module
            for module in payload["modules"]
            if module["id"] == "IUM-5-CORE-07"
        )
        cls.contracts = {
            contract["competencyId"]: contract
            for contract in module["coverageEvidence"]
        }

    def test_core_07_uses_one_private_matrix_and_one_nonpersonal_case_product(self):
        private_ids = {
            "BMB16-GYM-IK-MG-001",
            "BMB16-GYM-IK-MG-003",
            "BMB16-GYM-PK-RK-001",
            "BMB16-GYM-PK-RK-002",
        }
        self.assertEqual(
            set(self.contracts),
            private_ids | {"BMB16-GYM-IK-MG-002"},
        )

        for competency_id in private_ids:
            with self.subTest(competency_id=competency_id):
                contract = self.contracts[competency_id]
                self.assertIn(
                    INTEGRATED_PRIVATE_PRODUCT,
                    contract["productEvidence"],
                )
                self.assertIn(
                    COMMON_CASE_PRODUCT,
                    contract["nonPersonalFollowUp"],
                )
                self.assertIn(COMMON_CASE, contract["nonPersonalFollowUp"])

        shared_product_fields = [
            self.contracts[competency_id]["nonPersonalFollowUp"]
            for competency_id in private_ids
        ] + [self.contracts["BMB16-GYM-IK-MG-002"]["productEvidence"]]
        self.assertEqual(
            sum(
                field.count(COMMON_CASE_PRODUCT)
                for field in shared_product_fields
            ),
            5,
        )
        self.assertTrue(
            all(COMMON_CASE in field for field in shared_product_fields)
        )

        mg001 = self.contracts["BMB16-GYM-IK-MG-001"]
        for field in ("learningAction", "productEvidence", "nonPersonalFollowUp"):
            with self.subTest(mg001_field=field):
                self.assertIn(MG001_CRITERIA, mg001[field])


class Core03RepositoryOrchestrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(encoding="utf-8")
        )
        cls.module = next(
            module
            for module in payload["modules"]
            if module["id"] == "IUM-5-CORE-03"
        )
        cls.contracts = {
            contract["competencyId"]: contract
            for contract in cls.module.get("coverageEvidence", [])
        }

    def test_core_03_closes_six_records_in_one_safe_actual_local_project(self):
        school_context_ids = {
            "BMB16-GYM-IK-KK-002",
            "BMB16-GYM-IK-KK-003",
            "BMB16-GYM-PK-HK-003",
            "LH26-E-KS-001",
        }
        module_detail_ids = {
            "BMB16-GYM-PK-RK-004",
            "LH26-E-KS-002",
        }
        self.assertEqual(
            set(self.contracts),
            school_context_ids | module_detail_ids,
        )
        self.assertEqual(self.module["lessonRange"], {"min": 4, "max": 6})

        for competency_id, contract in self.contracts.items():
            with self.subTest(competency_id=competency_id):
                self.assertIn(
                    CORE03_LOCAL_PROJECT,
                    contract["learningAction"],
                )
                self.assertIn(
                    CORE03_SHARED_PRODUCT,
                    contract["productEvidence"],
                )
                self.assertIn(
                    CORE03_SAFE_CONTENT,
                    contract["productEvidence"],
                )
                self.assertIn(
                    CORE03_DATA_BOUNDARY,
                    contract["productEvidence"],
                )
        self.assertEqual(
            sum(
                contract["productEvidence"].count(CORE03_SHARED_PRODUCT)
                for contract in self.contracts.values()
            ),
            6,
        )

        for competency_id in school_context_ids:
            with self.subTest(school_context_id=competency_id):
                contract = self.contracts[competency_id]
                self.assertEqual(contract["mode"], "school-context")
                self.assertEqual(
                    contract["executionType"],
                    "actual-local-use",
                )
                self.assertIn("tatsächlich", contract["learningAction"])
                self.assertIn(
                    "vor Ort freigegeben",
                    contract["localConfigurationRequirement"],
                )
                for product_name in (
                    "Moodle", "Microsoft Teams", "Google Classroom", "IServ"
                ):
                    self.assertNotIn(
                        product_name,
                        contract["localConfigurationRequirement"],
                    )

        kk002 = self.contracts["BMB16-GYM-IK-KK-002"]["learningAction"]
        for term in (
            "digitalen Kommunikationsweg",
            "Grundfunktionen tatsächlich anwenden",
            "adressatengerecht verfassen",
            "senden oder teilen",
            "abrufen",
            "neutralen Testanhang",
            "entsprechende lokale Kernfunktion",
        ):
            self.assertIn(term, kk002)

        kk003 = self.contracts["BMB16-GYM-IK-KK-003"]["learningAction"]
        for term in (
            "mindestens einen digitalen Kommunikationsweg",
            "Kooperation",
            "Austausch",
            "innerhalb",
            "tatsächlich nutzen",
        ):
            self.assertIn(term, kk003)

        hk003 = self.contracts["BMB16-GYM-PK-HK-003"]["learningAction"]
        for term in (
            "Medien",
            "Zusammenarbeit",
            "Kooperation",
            "tatsächlich nutzen",
        ):
            self.assertIn(term, hk003)

        ks001 = self.contracts["LH26-E-KS-001"]
        for term in (
            "schulischen Kommunikationskanal",
            "Möglichkeiten zur Kollaboration",
            "tatsächlich nutzen",
        ):
            self.assertIn(term, ks001["learningAction"])
        for term in (
            "schulischen Kommunikationskanal",
            "Kollaborationsmöglichkeit",
            "technisch getrennt",
            "beide",
            "selben Projektlauf",
        ):
            self.assertIn(term, ks001["localConfigurationRequirement"])

        rk004 = self.contracts["BMB16-GYM-PK-RK-004"]["learningAction"]
        for term in (
            "rechtliche Grenzübertretungen",
            "moralische Grenzübertretungen",
            "getrennt erkennen",
            "begründete Regeln",
            "eigenes soziales Verhalten ableiten",
        ):
            self.assertIn(term, rk004)

        ks002 = self.contracts["LH26-E-KS-002"]["learningAction"]
        for term in (
            "Auswirkungen",
            "fiktiven digitalen Konflikts",
            "reflektieren",
            "diskutieren",
            "mehreren Perspektiven",
            "mehrere Folgen",
            "gemeinsame Revision",
        ):
            self.assertIn(term, ks002)


class Core02RepositoryOrchestrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(encoding="utf-8")
        )
        cls.module = next(
            module
            for module in payload["modules"]
            if module["id"] == "IUM-5-CORE-02"
        )
        cls.contracts = {
            contract["competencyId"]: contract
            for contract in cls.module.get("coverageEvidence", [])
        }

    def test_core_02_integrates_prior_knowledge_source_link_and_revision(self):
        self.assertEqual(set(self.contracts), {"LH26-E-ID-009"})
        self.assertEqual(
            self.module["prerequisiteModuleIds"],
            ["IUM-5-CORE-01"],
        )
        self.assertEqual(self.module["lessonRange"], {"min": 5, "max": 7})

        contract = self.contracts["LH26-E-ID-009"]
        self.assertEqual(contract["mode"], "module-detail")
        self.assertEqual(contract["productVisibility"], "teacher-observable")

        for term in (
            "Strategien Vorwissensanker, Quellenabgleich und Antwortrevision anwenden",
            "zur konkreten Suchfrage sachbezogenes Vorwissen",
            "im selben digitalen Quellendossier festhalten",
            "eine neue Quelleninformation ausdrücklich als Übereinstimmung, "
            "Ergänzung oder Widerspruch damit verknüpfen",
            "aus diesem Abgleich eine belegte Aussage oder dokumentierte "
            "Revision der Antwort ableiten",
        ):
            self.assertIn(term, contract["learningAction"])

        for term in (
            CORE02_INTEGRATED_TRACE,
            "gekennzeichnetem sachbezogenem Vorwissensanker",
            "neuer Quelleninformation",
            "Verknüpfung als Übereinstimmung, Ergänzung oder Widerspruch",
            "daraus abgeleiteter weiterverarbeiteter Aussage",
            "kein separates Zusatzprodukt",
        ):
            self.assertIn(term, contract["productEvidence"])


class Core06RepositoryOrchestrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(encoding="utf-8")
        )
        cls.module = next(
            module
            for module in payload["modules"]
            if module["id"] == "IUM-5-CORE-06"
        )
        cls.contracts = {
            contract["competencyId"]: contract
            for contract in cls.module.get("coverageEvidence", [])
        }

    def test_core_06_orchestrates_four_distinct_traces_in_one_product_revision(self):
        expected_traces = {
            "BMB16-GYM-IK-PP-002": CORE06_RIGHTS_PRIVACY_TRACE,
            "LH26-E-DA-005": CORE06_TEXT_FORMAT_TRACE,
            "LH26-E-DA-006": CORE06_IMAGE_TRACE,
            "LH26-E-DA-008": CORE06_GIVEN_DESIGN_TRACE,
        }
        self.assertEqual(set(self.contracts), set(expected_traces))
        self.assertEqual(
            self.module["prerequisiteModuleIds"],
            ["IUM-5-CORE-01", "IUM-5-CORE-02"],
        )
        self.assertEqual(self.module["lessonRange"], {"min": 5, "max": 7})

        for competency_id, trace in expected_traces.items():
            with self.subTest(competency_id=competency_id):
                contract = self.contracts[competency_id]
                self.assertEqual(contract["mode"], "module-detail")
                self.assertEqual(
                    contract["productVisibility"],
                    "teacher-observable",
                )
                self.assertIn(CORE06_COMMON_PRODUCT, contract["productEvidence"])
                self.assertIn(trace, contract["productEvidence"])
                for other_id, other_trace in expected_traces.items():
                    if other_id != competency_id:
                        self.assertNotIn(other_trace, contract["productEvidence"])

        self.assertEqual(
            len(
                {
                    contract["productEvidence"]
                    for contract in self.contracts.values()
                }
            ),
            4,
        )

    def test_pp002_separates_copyright_and_data_protection_without_private_evidence(self):
        contract = self.contracts["BMB16-GYM-IK-PP-002"]
        for term in (
            "für jedes verwendete Fremdmaterial",
            "Quelle, Lizenz und zulässige Nutzung",
            "getrennt davon",
            "datensparsame Inhalts- und Veröffentlichungsentscheidung",
            "fiktive oder sachbezogene Inhalte",
            "keine echten personenbezogenen Daten",
            "begrenzten Adressatenkreis",
        ):
            self.assertIn(term, contract["learningAction"])
        self.assertIn(
            "bei der erstellung",
            contract["learningAction"].casefold(),
        )
        for term in (
            CORE06_RIGHTS_PRIVACY_TRACE,
            "quellen- und lizenzbezogene Entscheidung pro Fremdmaterial",
            "Datenvermeidung",
            "keine echten personenbezogenen Daten",
            "begrenzter Adressatenkreis",
            "keine Einwilligungsdokumente",
            "keine private Offenlegung",
        ):
            self.assertIn(term, contract["productEvidence"])

    def test_da005_identifies_concrete_text_parts_and_uses_multiple_formats(self):
        contract = self.contracts["LH26-E-DA-005"]
        for term in (
            "in einer vorgegebenen konkreten Textfassung",
            "Überschrift",
            "Fließtext",
            "Bildunterschrift",
            "Listenbaustein",
            "identifizieren",
            "Formatvorlage oder Absatzformat",
            "Liste",
            "Hervorhebung",
            "tatsächlich und funktional nutzen",
        ):
            self.assertIn(term, contract["learningAction"])
        for term in (
            CORE06_TEXT_FORMAT_TRACE,
            "markierten Textbausteine",
            "Vorher-Nachher-Vergleich",
            "mehrere tatsächlich eingesetzte Formatierungen",
        ):
            self.assertIn(term, contract["productEvidence"])
        self.assertNotIn("Text gestalten", contract["learningAction"])

    def test_da006_requires_the_named_object_type_image_and_its_visible_function(self):
        contract = self.contracts["LH26-E-DA-006"]
        for term in (
            "ein Bild als verpflichtend nachzuweisende visuelle Objektart",
            "tatsächlich nutzen",
            "Position, Größe oder Ausschnitt",
            "visuelle Funktion",
            "weitere Gestaltungsobjekte bleiben optional",
        ):
            self.assertIn(term, contract["learningAction"])
        for term in (
            CORE06_IMAGE_TRACE,
            "das eingesetzte Bild",
            "sichtbare Entscheidung zu Position, Größe oder Ausschnitt",
            "begründete Funktion für die Aussage",
        ):
            self.assertIn(term, contract["productEvidence"])
        self.assertNotIn("visuelle Objekte nutzen", contract["learningAction"])

    def test_da008_analyses_and_judges_a_given_design_before_optional_transfer(self):
        contract = self.contracts["LH26-E-DA-008"]
        for term in (
            "eine vorgegebene Gestaltung",
            "Wirkung anhand vorgegebener Kriterien und konkreter Belege beurteilen",
            "Zusammenhang von Inhalt und Form analysieren",
            "erst anschließend",
            "eigene Überarbeitung übertragen",
            "ersetzt Analyse und Urteil nicht",
        ):
            self.assertIn(term, contract["learningAction"])
        for term in (
            CORE06_GIVEN_DESIGN_TRACE,
            "Gestaltungselement",
            "Inhalt",
            "Form",
            "Wirkung",
            "Beleg",
            "begründetes Gesamturteil",
            "optionale Transfermarkierung",
        ):
            self.assertIn(term, contract["productEvidence"])


class Core6Core02RepositoryOrchestrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(encoding="utf-8")
        )
        cls.module = next(
            module
            for module in payload["modules"]
            if module["id"] == "IUM-6-CORE-02"
        )
        cls.contracts = {
            contract["competencyId"]: contract
            for contract in cls.module.get("coverageEvidence", [])
        }

    def test_two_distinct_layers_share_one_safe_model_without_private_evidence(self):
        expected = {"LH26-E-DP-004", "LH26-E-DP-006"}
        self.assertEqual(set(self.contracts), expected)
        self.assertEqual(
            self.module["prerequisiteModuleIds"],
            ["IUM-5-CORE-07", "IUM-6-CORE-01"],
        )
        self.assertEqual(self.module["lessonRange"], {"min": 5, "max": 7})

        for competency_id in expected:
            with self.subTest(competency_id=competency_id):
                contract = self.contracts[competency_id]
                self.assertEqual(contract["mode"], "module-detail")
                self.assertEqual(
                    contract["productVisibility"],
                    "teacher-observable",
                )
                self.assertIn(
                    CORE6_CORE02_COMMON_MODEL,
                    contract["productEvidence"],
                )
                self.assertIn(
                    CORE6_CORE02_CURATED_CASES,
                    contract["productEvidence"],
                )
                self.assertIn(
                    CORE6_CORE02_PRIVACY_BOUNDARY,
                    contract["productEvidence"],
                )
                self.assertNotIn(
                    "private Reflexionsnotiz",
                    contract["productEvidence"],
                )
                self.assertNotIn(
                    "eigene Mediennutzung",
                    contract["productEvidence"],
                )
                self.assertIn(
                    "kein unverbundenes Zusatzprodukt",
                    contract["productEvidence"],
                )

    def test_dp004_extracts_both_condition_types_from_multiple_examples_with_evidence(self):
        self.assertIn("LH26-E-DP-004", self.contracts)
        contract = self.contracts["LH26-E-DP-004"]
        for term in (
            "Nutzungs- und Rahmenbedingungen",
            "mindestens zwei unterschiedlichen Dienst- oder Softwarebeispielen",
            "Apps, Programmen oder Onlinediensten",
            "konkreten kuratierten fiktiven oder neutralisierten "
            "Bedingungen-Auszügen",
            "herausarbeiten",
            "Fundstelle belegen",
            "Auswirkung auf die Nutzung und die Schutzentscheidung",
            "keine Anmeldung",
        ):
            self.assertIn(term, contract["learningAction"])

        for term in (
            CORE6_CORE02_CONDITIONS_LAYER,
            "mindestens zwei unterschiedliche Dienst- oder Softwarebeispiele",
            "Zugang, Alter oder Kosten",
            "Daten oder Berechtigungen",
            "Werbung oder Finanzierung",
            "Nutzungsrechte oder Kündigung",
            "Bedingungen-Auszug",
            "Fundstelle oder Beleg",
            "Auswirkung auf Nutzung und Schutzentscheidung",
        ):
            self.assertIn(term, contract["productEvidence"])

    def test_dp006_names_multiple_specific_ad_selection_paths_with_model_limits(self):
        self.assertIn("LH26-E-DP-006", self.contracts)
        contract = self.contracts["LH26-E-DP-006"]
        for term in (
            "Möglichkeiten nennen",
            "spezifische Auswahl einer Werbebotschaft",
            "mindestens drei unterscheidbare modellierte Auswahlwege",
            "aktueller Inhalts- oder Suchkontext",
            "fiktives Profilmerkmal",
            "fiktives Nutzungsverhaltenssignal",
            "Signal oder Datenmerkmal",
            "Auswahlregel oder Auswahlmodell",
            "konkrete Werbebotschaft",
            "keine technische Gewissheit über einen konkreten Dienst",
        ):
            self.assertIn(term, contract["learningAction"])

        for term in (
            CORE6_CORE02_AD_PATH_LAYER,
            "mindestens drei synthetische Fälle",
            "Kontextpfad",
            "Profilpfad",
            "Verhaltenspfad",
            "Signal oder Datenmerkmal",
            "Auswahlregel oder Auswahlmodell",
            "konkret ausgewählte Werbebotschaft",
            "nicht bloß allgemeine Auswahlhypothesen",
            "Modellgrenze",
        ):
            self.assertIn(term, contract["productEvidence"])


class Core05RepositoryOrchestrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        module_payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(encoding="utf-8")
        )
        cls.module = next(
            module
            for module in module_payload["modules"]
            if module["id"] == "IUM-5-CORE-05"
        )
        cls.contracts = {
            contract["competencyId"]: contract
            for contract in cls.module.get("coverageEvidence", [])
        }

        remediation_payload = json.loads(
            (root / "roadmap/coverage-remediation.json").read_text(
                encoding="utf-8"
            )
        )
        cls.remediation = {
            entry["competencyId"]: entry
            for entry in remediation_payload["entries"]
            if entry["competencyId"] in {"LH26-E-ALG-001", "LH26-E-PROG-002"}
        }

        coverage_payload = json.loads(
            (root / "roadmap/coverage-plan.json").read_text(encoding="utf-8")
        )
        cls.coverage = {
            entry["competencyId"]: entry
            for entry in coverage_payload["entries"]
            if entry["competencyId"] in {"LH26-E-ALG-001", "LH26-E-PROG-002"}
        }

    def test_alg001_identifies_and_justifies_mixed_cases_in_the_algorithm_product(self):
        self.assertEqual(
            AUDITED_DECISIONS["LH26-E-ALG-001"],
            ("IUM-5-CORE-05", "module-detail", "covered"),
        )
        self.assertEqual(set(self.contracts), {"LH26-E-ALG-001"})
        self.assertEqual(
            self.module["prerequisiteModuleIds"],
            ["IUM-5-CORE-01"],
        )
        self.assertEqual(self.module["lessonRange"], {"min": 5, "max": 7})

        contract = self.contracts["LH26-E-ALG-001"]
        self.assertEqual(contract["mode"], "module-detail")
        self.assertEqual(contract["productVisibility"], "teacher-observable")

        for term in (
            "aus einem gemischten Satz",
            "digitale Systeme, Nichtbeispiele und Grenzbeispiele",
            "digitale Systeme identifizieren",
            "deren Funktionsweise wesentlich durch algorithmische Prozesse "
            "bestimmt ist",
            "für jeden Fall",
            "am konkreten algorithmischen Prozess",
            "begründen",
        ):
            self.assertIn(term, contract["learningAction"])

        for term in (
            "derselben Produktansicht",
            "ausführbaren grafischen Algorithmus",
            "Laufprotokoll",
            "integrierte Klassifikations- und Begründungsspur",
            "alle vorgegebenen Fälle",
            "konkreten algorithmischen Prozess",
            "fallbezogene Begründung",
            "kein unverbundenes Zusatzprodukt",
        ):
            self.assertIn(term, contract["productEvidence"])

    def test_prog002_stays_roadmap_dependent_without_an_evidence_contract(self):
        self.assertEqual(
            AUDITED_DECISIONS["LH26-E-PROG-002"],
            ("IUM-5-CORE-05", "roadmap-level", "remain-partial"),
        )
        self.assertNotIn("LH26-E-PROG-002", self.contracts)

        entry = self.remediation["LH26-E-PROG-002"]
        coverage = self.coverage["LH26-E-PROG-002"]
        residual_reason = (
            "Ein Einzelmodul belegt noch nicht die übergreifend "
            "niederschwellige Abgrenzung zur fachlichen Tiefe des Aufbaukurses."
        )
        self.assertEqual(entry["decision"], "remain-partial")
        self.assertIsNone(entry["evidenceContractId"])
        self.assertEqual(
            entry["after"],
            {
                "coverageStatus": "partial",
                "semanticAudit": "documented-gap",
            },
        )
        self.assertEqual(entry["timeImpact"]["level"], "roadmap-dependent")
        self.assertEqual(entry["graphImpact"]["level"], "none")
        self.assertEqual(entry["residualGap"]["reason"], residual_reason)
        self.assertEqual(coverage["reason"], residual_reason)
        self.assertEqual(entry["residualGap"]["risk"], coverage["risk"])
        self.assertEqual(entry["residualGap"]["followUp"], coverage["followUp"])
        for field in ("changeRationale",):
            for term in (
                "jahrgangsübergreifend",
                "altersangemessene",
                "niederschwellige",
                "fachlichen Tiefe in Klasse 7",
                "kein Einzelmodulvertrag",
            ):
                self.assertIn(term, entry[field])
        self.assertIn(
            "jahrgangsübergreifenden Sequenznachweis",
            entry["residualGap"]["risk"],
        )
        self.assertIn(
            "jahrgangsweiten Sequenznachweis",
            entry["residualGap"]["followUp"],
        )
        self.assertIn(
            "jahrgangsübergreifend",
            entry["residualGap"]["followUp"],
        )
        for field in ("risk", "followUp"):
            for term in (
                "altersangemessene",
                "niederschwellige",
                "fachlichen Tiefe in Klasse 7",
            ):
                self.assertIn(term, entry["residualGap"][field])


class Core7Core03RepositoryOrchestrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(encoding="utf-8")
        )
        cls.module = next(
            module
            for module in payload["modules"]
            if module["id"] == "IUM-7-CORE-03"
        )
        cls.contracts = {
            contract["competencyId"]: contract
            for contract in cls.module.get("coverageEvidence", [])
        }

    def test_core_03_orchestrates_six_distinct_views_in_one_trace_product(self):
        expected_views = {
            "INF7-16-GYM-IK-ALG-003": "Wertespeicher- und Zustandsansicht",
            "INF7-16-GYM-PK-MI-005": (
                "grafische Ablauf- und Zustandsmodellierungsansicht"
            ),
            "INF7-16-GYM-PK-SV-003": (
                "Daten- und Objektbeziehungsansicht"
            ),
            "LH26-E-ALG-007": "Grundbaustein- und Ausdrucksansicht",
            "LH26-E-ALG-008": "Übergabe- und Rückgabeansicht",
            "LH26-E-ALG-009": "Datentypansicht",
        }
        self.assertEqual(set(self.contracts), set(expected_views))
        self.assertEqual(self.module["lessonRange"], {"min": 6, "max": 8})

        for competency_id, view_name in expected_views.items():
            with self.subTest(competency_id=competency_id):
                contract = self.contracts[competency_id]
                self.assertEqual(contract["mode"], "module-detail")
                self.assertIn(
                    CORE7_CORE03_TRACE_PRODUCT,
                    contract["productEvidence"],
                )
                self.assertIn(
                    CORE7_CORE03_COMMON_TRACE,
                    contract["productEvidence"],
                )
                self.assertIn(view_name, contract["productEvidence"])
                self.assertIn(
                    "keine zusätzlichen Einzelprodukte",
                    contract["productEvidence"],
                )

        variable = self.contracts["INF7-16-GYM-IK-ALG-003"]
        self.assertIn(
            "Variable ausdrücklich als änderbaren Wertespeicher erläutern",
            variable["learningAction"],
        )
        self.assertIn(
            "Zustandsänderung vom alten zum neuen Wert",
            variable["productEvidence"],
        )

        modelling = self.contracts["INF7-16-GYM-PK-MI-005"]
        for term in (
            "plattformneutrales grafisches Modellierungswerkzeug",
            "tatsächlich einsetzen",
            "erstellen, bearbeiten und korrigieren",
        ):
            self.assertIn(term, modelling["learningAction"])
        self.assertIn(
            "Werkzeugeinsatz mit bearbeiteter und korrigierter Modellfassung",
            modelling["productEvidence"],
        )

        building_blocks = self.contracts["LH26-E-ALG-007"]
        for term in (
            "Anweisung",
            "Schleife mit konstanter Durchlaufzahl",
            "Schleife mit Bedingung",
            "Verzweigung",
            "Ausdruck ohne Operator",
            "Ausdruck mit arithmetischem Operator",
            "Ausdruck mit Vergleichsoperator",
        ):
            self.assertIn(term, building_blocks["learningAction"])
            self.assertIn(term, building_blocks["productEvidence"])

        data_types = self.contracts["LH26-E-ALG-009"]
        for term in (
            "Zeichenkette",
            "Zahl",
            "Wahrheitswert",
            "Werten und Ausdrücken",
        ):
            self.assertIn(term, data_types["learningAction"])
            self.assertIn(term, data_types["productEvidence"])

    def test_sv003_requires_a_labelled_dependency_graph_not_a_linear_trace_chain(self):
        relationship = self.contracts["INF7-16-GYM-PK-SV-003"]
        for field in ("learningAction", "productEvidence"):
            with self.subTest(field=field):
                self.assertNotIn(
                    "Eingabe → Variable → Ausdrucksergebnis → Ausgabe",
                    relationship[field],
                )

        for term in (
            "gerichteten und beschrifteten Datenabhängigkeitsgraphen",
            "Eingabedatum",
            "Variablenzustand vor der Anweisung",
            "Variablenzustand nach der Anweisung",
            "Ausdrucksergebnis",
            "Ausgabeobjekt",
            "mindestens eine Abhängigkeit",
            "Änderungsfolge",
            "Beziehungen statt einer bloß zeitlichen Verarbeitung",
        ):
            self.assertIn(term, relationship["learningAction"])

        for edge_label in ("liest", "schreibt", "hängt ab von"):
            self.assertIn(edge_label, relationship["learningAction"])
            self.assertIn(edge_label, relationship["productEvidence"])
        self.assertIn("gerichtete Kanten", relationship["productEvidence"])
        self.assertIn(
            "Bedeutung der Abhängigkeit und Änderungsfolge",
            relationship["productEvidence"],
        )

    def test_alg008_distinguishes_expression_results_from_statements_without_returns(self):
        transfer = self.contracts["LH26-E-ALG-008"]
        for term in (
            "Übergabe und Rückgabe von Werten",
            "von seiner Quelle oder aus einem inneren Ausdruck",
            "konsumierenden Operanden, Parameter oder Ziel",
            "ausgewerteter Ausdruck liefert seinen Ergebniswert",
            "konsumierenden äußeren Ausdruck oder eine Anweisung",
            "Anweisung ohne definierten Ergebniswert liefert keinen Rückgabewert",
            "keine Funktionsrückgabe unterstellt",
        ):
            self.assertIn(term, transfer["learningAction"])

        for term in (
            "Quelle, konsumierenden Operand/Parameter/Ziel, ausgewertetes "
            "Ergebnis und Empfänger",
            "kein Rückgabewert",
            "Funktionsrückgabe wird nicht behauptet",
        ):
            self.assertIn(term, transfer["productEvidence"])

        self.assertNotIn(
            "Übergabe und Rückgabe von Werten identifizieren und jeweils "
            "Quelle, Ziel, Eingabe und Ergebnis eindeutig zuordnen",
            transfer["learningAction"],
        )
        self.assertNotIn(
            "Übergabe und Rückgabe sowie Quelle, Ziel, Eingabe und Ergebnis "
            "getrennt aus",
            transfer["productEvidence"],
        )


class Core08RepositoryOrchestrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(encoding="utf-8")
        )
        cls.module = next(
            module
            for module in payload["modules"]
            if module["id"] == "IUM-7-CORE-08"
        )
        cls.contracts = {
            contract["competencyId"]: contract
            for contract in cls.module.get("coverageEvidence", [])
        }

    def test_core_08_orchestrates_five_records_in_one_dossier(self):
        visible_ids = {
            "INF7-16-GYM-IK-IGD-006",
            "INF7-16-GYM-PK-AB-005",
            "INF7-16-GYM-PK-AB-006",
            "INF7-16-GYM-PK-KK-006",
        }
        private_id = "LH26-E-DP-013"
        self.assertEqual(set(self.contracts), visible_ids | {private_id})

        for competency_id in visible_ids:
            with self.subTest(competency_id=competency_id):
                product = self.contracts[competency_id]["productEvidence"]
                self.assertIn(CORE08_SHARED_DOSSIER, product)
                self.assertIn(CORE08_COMMON_MATERIAL, product)

        igd006 = self.contracts["INF7-16-GYM-IK-IGD-006"]
        for term in (
            "permanent anfallenden",
            "Speicherung",
            "alltagsrelevanten Dienstfall",
            "Nutzen",
            "Risiken",
        ):
            self.assertIn(term, igd006["learningAction"])

        ab005 = self.contracts["INF7-16-GYM-PK-AB-005"]
        for term in (
            "Gesellschaft",
            "Berufswelt",
            "persönliches Lebensumfeld",
            "betroffene Person",
            "Beschäftigte",
            "Dienstanbieter",
            "Öffentlichkeit",
        ):
            self.assertIn(term, ab005["learningAction"])

        ab006 = self.contracts["INF7-16-GYM-PK-AB-006"]
        for term in (
            "eigene Position",
            "ethischen Informatikfrage",
            "Kriterien",
            "Belegen",
            "Gegenargument",
            "argumentativ vertreten",
        ):
            self.assertIn(term, ab006["learningAction"])

        kk006 = self.contracts["INF7-16-GYM-PK-KK-006"]
        for term in (
            "Toleranz",
            "Akzeptanz",
            "Vielfalt",
            "informatischen Fragestellung",
            "mehreren benannten Perspektiven",
            "revidiertes Ergebnis",
        ):
            self.assertIn(term, kk006["learningAction"])

        private = self.contracts[private_id]
        self.assertEqual(private["productVisibility"], "private-local")
        self.assertEqual(private["privacyBoundary"], PRIVATE_BOUNDARY_TEXT)
        self.assertIn(
            CORE08_FALSE_INFORMATION_CASE,
            private["learningAction"],
        )
        self.assertIn("eigenen Umgang", private["learningAction"])
        self.assertIn("private lokale Reflexionsnotiz", private["productEvidence"])
        self.assertIn(CORE08_SHARED_DOSSIER, private["nonPersonalFollowUp"])
        self.assertIn(CORE08_COMMON_MATERIAL, private["nonPersonalFollowUp"])
        self.assertIn(
            CORE08_FALSE_INFORMATION_CASE,
            private["nonPersonalFollowUp"],
        )
        self.assertIn(
            "ohne Kenntnis der privaten Notiz",
            private["nonPersonalFollowUp"],
        )
        self.assertIn(
            "keine persönliche Handlungsoption",
            private["nonPersonalFollowUp"],
        )


class ModuleStructureFingerprintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        cls.repository_payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(encoding="utf-8")
        )

    def test_repository_payload_matches_immutable_structure_baseline(self):
        self.assertEqual(
            module_structure_fingerprint(self.repository_payload),
            BASELINE_MODULE_STRUCTURE_FINGERPRINT_SHA256,
        )

    def test_rejects_changed_immutable_module_fields(self):
        mutations = {
            "id": lambda module: module.__setitem__("id", "IUM-5-CORE-99"),
            "grade": lambda module: module.__setitem__("grade", 6),
            "kind": lambda module: module.__setitem__("kind", "extension"),
            "prerequisiteModuleIds": lambda module: module.__setitem__(
                "prerequisiteModuleIds", ["IUM-5-CORE-01"]
            ),
            "lessonRange": lambda module: module.__setitem__(
                "lessonRange", {"min": 6, "max": 8}
            ),
        }
        for field, mutate in mutations.items():
            with self.subTest(field=field):
                payload = copy.deepcopy(self.repository_payload)
                payload["modules"][0].pop("coverageEvidence", None)
                mutate(payload["modules"][0])
                with self.assertRaisesRegex(
                    IUM09ValidationError, "module structure fingerprint"
                ):
                    validate_coverage_evidence(payload, curriculum_contracts())

    def test_json_key_order_does_not_change_fingerprint(self):
        reordered_payload = json.loads(
            json.dumps(self.repository_payload, sort_keys=True, ensure_ascii=False)
        )
        self.assertEqual(
            module_structure_fingerprint(self.repository_payload),
            module_structure_fingerprint(reordered_payload),
        )


class CoverageBaselineFingerprintTests(unittest.TestCase):
    def test_hashes_only_sorted_immutable_before_records(self):
        entries = [
            {
                "competencyId": "B",
                "requirementText": "B text",
                "before": {
                    "coverageStatus": "partial",
                    "semanticAudit": "documented-gap",
                    "evidenceModuleId": "IUM-5-CORE-02",
                    "reason": "B reason",
                },
                "decision": "remain-partial",
            },
            {
                "competencyId": "A",
                "requirementText": "A text",
                "before": {
                    "coverageStatus": "partial",
                    "semanticAudit": "documented-gap",
                    "evidenceModuleId": "IUM-5-CORE-01",
                    "reason": "A reason",
                },
                "decision": "covered",
            },
        ]

        self.assertEqual(
            coverage_baseline_fingerprint(entries),
            "51af7b42e2d84adf0a3b0cef4548e0f4adc2bd9f275f537f4fa3abc8c65be01c",
        )


class RemediationLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        cls.coverage_payload = json.loads(
            (root / "roadmap/coverage-plan.json").read_text(encoding="utf-8")
        )
        cls.ledger_payload = json.loads(
            (root / "roadmap/coverage-remediation.json").read_text(encoding="utf-8")
        )
        cls.curriculum_contracts = {
            entry["competencyId"]: {"text": entry["requirementText"]}
            for entry in cls.coverage_payload["entries"]
        }
        cls.coverage_entries = {
            entry["competencyId"]: entry
            for entry in cls.coverage_payload["entries"]
        }
        module_payload = json.loads(
            (root / "roadmap/module-candidates.json").read_text(encoding="utf-8")
        )
        cls.repository_evidence_contracts = validate_coverage_evidence(
            module_payload, cls.curriculum_contracts
        )

    def validate(self, payload, evidence_contracts=None):
        contracts = dict(self.repository_evidence_contracts)
        if evidence_contracts is not None:
            contracts.update(evidence_contracts)
        return validate_remediation_ledger(
            payload, self.curriculum_contracts, contracts
        )

    def test_repository_ledger_has_immutable_baseline_metadata(self):
        self.assertEqual(
            set(self.ledger_payload),
            {"schemaVersion", "status", "baseline", "entries"},
        )
        self.assertEqual(self.ledger_payload["schemaVersion"], 1)
        self.assertEqual(self.ledger_payload["status"], "working")
        self.assertEqual(
            self.ledger_payload["baseline"],
            {
                "coverageCommit": "69c9d4f5504a297289615b4169fc4a9ea6d9b253",
                "partialCount": 60,
                "recordFingerprintSha256": (
                    "b7602352c67f61cdf075a65df167e12f7283b8f62867386545fea758b6e08892"
                ),
            },
        )

    def test_repository_ledger_has_each_baseline_id_in_its_specified_class(self):
        actual = {
            entry["competencyId"]: entry["causeClass"]
            for entry in self.ledger_payload["entries"]
        }
        self.assertEqual(actual, EXPECTED_CAUSE_CLASS_BY_ID)
        self.assertEqual(len(self.ledger_payload["entries"]), 60)

    def test_repository_ledger_fingerprint_matches_approved_before_records(self):
        self.assertEqual(
            coverage_baseline_fingerprint(self.ledger_payload["entries"]),
            "b7602352c67f61cdf075a65df167e12f7283b8f62867386545fea758b6e08892",
        )

    def test_repository_ledger_preserves_before_records_and_matches_audits(self):
        for entry in self.ledger_payload["entries"]:
            with self.subTest(competency_id=entry["competencyId"]):
                source = self.coverage_entries[entry["competencyId"]]
                self.assertEqual(entry["requirementText"], source["requirementText"])
                audit = AUDITED_DECISIONS.get(entry["competencyId"])
                if audit is None:
                    expected_module = entry["before"]["evidenceModuleId"]
                    expected_cause = entry["causeClass"]
                    expected_decision = "remain-partial"
                    self.assertEqual(
                        entry["before"],
                        {
                            "coverageStatus": source["coverageStatus"],
                            "semanticAudit": source["semanticAudit"],
                            "evidenceModuleId": source["evidenceModuleId"],
                            "reason": source["reason"],
                        },
                    )
                else:
                    expected_module, expected_cause, expected_decision = audit
                self.assertEqual(
                    entry["before"]["evidenceModuleId"], expected_module
                )
                self.assertEqual(entry["causeClass"], expected_cause)
                self.assertEqual(entry["decision"], expected_decision)
                if expected_decision == "covered":
                    self.assertIsNotNone(entry["evidenceContractId"])
                    self.assertEqual(
                        entry["after"],
                        {
                            "coverageStatus": "covered",
                            "semanticAudit": "operator-product-match",
                        },
                    )
                    self.assertIsNone(entry["residualGap"])
                else:
                    self.assertIsNone(entry["evidenceContractId"])
                    self.assertEqual(
                        entry["after"],
                        {
                            "coverageStatus": "partial",
                            "semanticAudit": "documented-gap",
                        },
                    )
                    self.assertEqual(
                        entry["residualGap"],
                        {
                            "reason": source["reason"],
                            "risk": source["risk"],
                            "followUp": source["followUp"],
                        },
                    )
                expected_graph = (
                    "review-required"
                    if entry["competencyId"]
                    in {
                        "BMB16-GYM-IK-GM-003",
                        "BMB16-GYM-PK-RK-003",
                    }
                    else "none"
                )
                self.assertEqual(entry["graphImpact"]["level"], expected_graph)
                expected_time = (
                    "roadmap-dependent"
                    if entry["causeClass"] == "roadmap-level"
                    else "review-required"
                )
                self.assertEqual(entry["timeImpact"]["level"], expected_time)

    def test_validator_accepts_repository_baseline_ledger(self):
        entries = self.validate(self.ledger_payload)
        self.assertEqual(set(entries), set(EXPECTED_CAUSE_CLASS_BY_ID))

    def test_validator_rejects_changed_baseline_requirement_text(self):
        payload = copy.deepcopy(self.ledger_payload)
        payload["entries"][0]["requirementText"] = "Unzulässige Änderung."
        with self.assertRaisesRegex(IUM09ValidationError, "fingerprint"):
            self.validate(payload)

    def test_validator_rejects_incomplete_residual_gap(self):
        payload = copy.deepcopy(self.ledger_payload)
        entry = next(
            entry
            for entry in payload["entries"]
            if entry["decision"] == "remain-partial"
        )
        del entry["residualGap"]["followUp"]
        with self.assertRaisesRegex(IUM09ValidationError, "residualGap"):
            self.validate(payload)

    def test_validator_rejects_covered_contract_from_a_different_baseline_module(self):
        payload = copy.deepcopy(self.ledger_payload)
        entry = payload["entries"][0]
        contract_id = "CE-IUM-7-CORE-01-BMB16-GYM-IK-GM-001"
        entry.update(
            {
                "decision": "covered",
                "evidenceContractId": contract_id,
                "after": {
                    "coverageStatus": "covered",
                    "semanticAudit": "operator-product-match",
                },
                "residualGap": None,
            }
        )
        with self.assertRaisesRegex(IUM09ValidationError, "baseline module"):
            self.validate(
                payload,
                {contract_id: {"competencyId": entry["competencyId"]}},
            )

    def test_validator_rejects_roadmap_level_departures(self):
        index = next(
            index
            for index, entry in enumerate(self.ledger_payload["entries"])
            if entry["causeClass"] == "roadmap-level"
        )
        mutations = {
            "decision": (
                lambda entry: entry.update(
                    {
                        "decision": "covered",
                        "evidenceContractId": "CE-IUM-5-CORE-01-LH26-E-PROG-001",
                        "after": {
                            "coverageStatus": "covered",
                            "semanticAudit": "operator-product-match",
                        },
                        "residualGap": None,
                    }
                ),
                {"CE-IUM-5-CORE-01-LH26-E-PROG-001": {"competencyId": "LH26-E-PROG-001"}},
                "roadmap-level",
            ),
            "contract": (
                lambda entry: entry.__setitem__(
                    "evidenceContractId", "CE-IUM-5-CORE-01-LH26-E-PROG-001"
                ),
                {},
                "remain-partial",
            ),
            "time": (
                lambda entry: entry["timeImpact"].__setitem__(
                    "level", "review-required"
                ),
                {},
                "roadmap-level",
            ),
            "graph": (
                lambda entry: entry["graphImpact"].__setitem__(
                    "level", "review-required"
                ),
                {},
                "roadmap-level",
            ),
        }
        for departure, (mutate, evidence_contracts, message) in mutations.items():
            with self.subTest(departure=departure):
                payload = copy.deepcopy(self.ledger_payload)
                mutate(payload["entries"][index])
                with self.assertRaisesRegex(IUM09ValidationError, message):
                    self.validate(payload, evidence_contracts)


class RemediatedCoverageTests(unittest.TestCase):
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
            (root / "roadmap/coverage-remediation.json").read_text(
                encoding="utf-8"
            )
        )
        cls.curriculum_contracts = {
            entry["competencyId"]: {"text": entry["requirementText"]}
            for entry in cls.coverage_payload["entries"]
        }
        cls.repository_evidence_contracts = validate_coverage_evidence(
            cls.module_payload, cls.curriculum_contracts
        )

    def validated_ledger_entries(self):
        return validate_remediation_ledger(
            self.remediation_payload,
            self.curriculum_contracts,
            self.repository_evidence_contracts,
        )

    def covered_chain_payloads(self):
        module_payload = copy.deepcopy(self.module_payload)
        contract = evidence_contract()
        evidence = module_payload["modules"][0]["coverageEvidence"]
        evidence[:] = [
            contract
            if item["competencyId"] == contract["competencyId"]
            else item
            for item in evidence
        ]
        coverage_payload = copy.deepcopy(self.coverage_payload)
        coverage_entry = next(
            entry
            for entry in coverage_payload["entries"]
            if entry["competencyId"] == contract["competencyId"]
        )
        coverage_entry.update(
            {
                "coverageStatus": "covered",
                "semanticAudit": "operator-product-match",
                "evidenceContractId": contract["id"],
            }
        )
        for field in ("requirementText", "learningAction", "productEvidence"):
            value = (
                coverage_entry["requirementText"]
                if field == "requirementText"
                else contract[field]
            )
            coverage_entry["evidence"] += f" {value}"
            coverage_entry["matchRationale"] += f" {value}"
        remediation_payload = copy.deepcopy(self.remediation_payload)
        remediation_entry = next(
            entry
            for entry in remediation_payload["entries"]
            if entry["competencyId"] == contract["competencyId"]
        )
        remediation_entry.update(
            {
                "decision": "covered",
                "evidenceContractId": contract["id"],
                "after": {
                    "coverageStatus": "covered",
                    "semanticAudit": "operator-product-match",
                },
                "residualGap": None,
            }
        )
        return module_payload, coverage_payload, remediation_payload, contract

    def test_accepts_repository_remediation_chain(self):
        result = validate_remediated_coverage(
            self.coverage_payload,
            self.validated_ledger_entries(),
            self.repository_evidence_contracts,
            self.curriculum_contracts,
        )
        self.assertEqual(
            result,
            {entry["competencyId"] for entry in self.coverage_payload["entries"]},
        )

    def test_rejects_each_nonempty_residual_gap_mutation(self):
        for field in ("reason", "risk", "followUp"):
            with self.subTest(field=field):
                coverage_payload = copy.deepcopy(self.coverage_payload)
                partial_entry = next(
                    entry
                    for entry in coverage_payload["entries"]
                    if entry["coverageStatus"] == "partial"
                )
                partial_entry[field] += " Abweichung."
                with self.assertRaisesRegex(IUM09ValidationError, "residual"):
                    validate_remediated_coverage(
                        coverage_payload,
                        self.validated_ledger_entries(),
                        self.repository_evidence_contracts,
                        self.curriculum_contracts,
                    )

    def test_rejects_status_change_without_matching_ledger_decision(self):
        coverage_payload = copy.deepcopy(self.coverage_payload)
        partial_entry = next(
            entry
            for entry in coverage_payload["entries"]
            if entry["coverageStatus"] == "partial"
        )
        partial_entry.update(
            {
                "coverageStatus": "covered",
                "semanticAudit": "operator-product-match",
                "evidenceContractId": (
                    f"CE-{partial_entry['evidenceModuleId']}-"
                    f"{partial_entry['competencyId']}"
                ),
            }
        )
        with self.assertRaisesRegex(IUM09ValidationError, "coverage status"):
            validate_remediated_coverage(
                coverage_payload,
                self.validated_ledger_entries(),
                self.repository_evidence_contracts,
                self.curriculum_contracts,
            )

    def test_rejects_evidence_contract_id_on_legacy_covered_record(self):
        coverage_payload = copy.deepcopy(self.coverage_payload)
        legacy_covered = next(
            entry
            for entry in coverage_payload["entries"]
            if entry["competencyId"] not in EXPECTED_CAUSE_CLASS_BY_ID
        )
        legacy_covered["evidenceContractId"] = "CE-legacy-record"
        with self.assertRaisesRegex(IUM09ValidationError, "legacy covered"):
            validate_remediated_coverage(
                coverage_payload,
                self.validated_ledger_entries(),
                self.repository_evidence_contracts,
                self.curriculum_contracts,
            )

    def test_rejects_coverage_chain_truncated_to_baseline_partial_ids(self):
        coverage_payload = copy.deepcopy(self.coverage_payload)
        coverage_payload["entries"] = [
            entry
            for entry in coverage_payload["entries"]
            if entry["competencyId"] in BASELINE_PARTIAL_IDS
        ]
        curriculum_contracts = {
            competency_id: self.curriculum_contracts[competency_id]
            for competency_id in BASELINE_PARTIAL_IDS
        }
        with self.assertRaisesRegex(IUM09ValidationError, "exactly 171"):
            validate_remediated_coverage(
                coverage_payload,
                self.validated_ledger_entries(),
                self.repository_evidence_contracts,
                curriculum_contracts,
            )

    def test_rejects_remediation_mapping_with_legacy_covered_record(self):
        remediation_entries = dict(self.validated_ledger_entries())
        coverage_payload = copy.deepcopy(self.coverage_payload)
        legacy_covered = next(
            entry
            for entry in coverage_payload["entries"]
            if entry["competencyId"] not in BASELINE_PARTIAL_IDS
        )
        legacy_covered.update(
            {
                "coverageStatus": "partial",
                "semanticAudit": "documented-gap",
                "reason": "Unzulässige zusätzliche Restrisikoentscheidung.",
            }
        )
        remediation_entries[legacy_covered["competencyId"]] = {
            "competencyId": legacy_covered["competencyId"],
            "requirementText": legacy_covered["requirementText"],
            "decision": "remain-partial",
            "evidenceContractId": None,
            "after": {
                "coverageStatus": "partial",
                "semanticAudit": "documented-gap",
            },
            "residualGap": {
                "reason": legacy_covered["reason"],
                "risk": legacy_covered["risk"],
                "followUp": legacy_covered["followUp"],
            },
        }
        with self.assertRaisesRegex(IUM09ValidationError, "baseline partial ids"):
            validate_remediated_coverage(
                coverage_payload,
                remediation_entries,
                self.repository_evidence_contracts,
                self.curriculum_contracts,
            )

    def test_covered_record_requires_every_contract_text_in_evidence_and_rationale(self):
        for container in ("evidence", "matchRationale"):
            for field in ("requirementText", "learningAction", "productEvidence"):
                with self.subTest(container=container, field=field):
                    module_payload, coverage_payload, remediation_payload, contract = (
                        self.covered_chain_payloads()
                    )
                    coverage_entry = next(
                        entry
                        for entry in coverage_payload["entries"]
                        if entry["competencyId"] == contract["competencyId"]
                    )
                    value = (
                        coverage_entry["requirementText"]
                        if field == "requirementText"
                        else contract[field]
                    )
                    coverage_entry[container] = coverage_entry[container].replace(
                        value,
                        "",
                    )
                    evidence_contracts = validate_coverage_evidence(
                        module_payload,
                        self.curriculum_contracts,
                    )
                    remediation_entries = validate_remediation_ledger(
                        remediation_payload,
                        self.curriculum_contracts,
                        evidence_contracts,
                    )
                    message = "evidence" if container == "evidence" else "rationale"
                    with self.assertRaisesRegex(IUM09ValidationError, message):
                        validate_remediated_coverage(
                            coverage_payload,
                            remediation_entries,
                            evidence_contracts,
                            self.curriculum_contracts,
                        )

    def test_rejects_evidence_contract_without_a_covered_ledger_decision(self):
        evidence_contracts = dict(self.repository_evidence_contracts)
        evidence_contracts["CE-orphan"] = {
            "competencyId": "BMB16-GYM-IK-GM-001"
        }
        with self.assertRaisesRegex(IUM09ValidationError, "referenced"):
            validate_remediated_coverage(
                self.coverage_payload,
                self.validated_ledger_entries(),
                evidence_contracts,
                self.curriculum_contracts,
            )

    def test_orchestrator_rejects_module_structure_mutation(self):
        module_payload = copy.deepcopy(self.module_payload)
        module_payload["modules"][0]["grade"] = 6
        with self.assertRaisesRegex(IUM09ValidationError, "module structure fingerprint"):
            validate_ium09(
                module_payload,
                self.coverage_payload,
                self.remediation_payload,
                self.curriculum_contracts,
            )


if __name__ == "__main__":
    unittest.main()
