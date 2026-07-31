import copy
import hashlib
import json
import unittest
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
PRIOR_20_TIME_REVIEWS_SHA256 = (
    "48a289cdfee61288c31806064660a01f294820f99a74150ef87536496613945f"
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

CORE07_NONPERSONAL_PRODUCT_FUNCTION = (
    "Als beobachtbare Produkt-, Zeit- und Evidenzspur zählt ausschließlich "
    "die nichtpersonale gemeinsame Wirkungskarte; die private "
    "Reflexionsnotiz wird weder eingesehen noch angerechnet. Das zentrale "
    "Lernprodukt eigenständig erstellen: Teilbare fallbezogene Wirkungskarte "
    "mit Beobachtung, möglicher Erklärung, Gegenperspektive, Unsicherheit und "
    "revidierbarer Handlungsoption; die private Reflexionsnotiz verbleibt "
    "ausschließlich bei der lernenden Person."
)
CORE07_AUDIT_EXPECTATIONS = {
    "BMB16-GYM-IK-MG-001": {
        "decision": "additional-time",
        "additionalMinutes": 15,
        "phaseIds": ["independent-action-product"],
        "rationale": (
            "Die 15 Minuten sind ausschließlich dem nichtpersonalen "
            "Abschnitt „Altersbezogene Bewertung“ der gemeinsamen "
            "fallbezogenen Wirkungskarte zugeordnet: Die Lernenden bewerten "
            "den vollständig vorgegebenen fiktiven Fall mit dem vollständig "
            "vorgegebenen Kriterienkatalog und begründen angemessene oder "
            "problematische Merkmale. Inhalt, Bearbeitungsstand und "
            "Zeitbedarf der privaten Motivations- und Nutzungsbewertung "
            "werden weder beobachtet noch als Produkt- oder Evidenzspur "
            "angerechnet."
        ),
        "risk": (
            "Eine Einsicht, Abgabe, Lehrkraftbeobachtung oder Bewertung der "
            "privaten Reflexionsmatrix würde persönliche Nutzungsmotivation "
            "erheben und die Datenschutzgrenze verletzen; das sichtbare "
            "Fallurteil darf keine Rückschlüsse auf den privaten Inhalt "
            "verlangen."
        ),
        "followUp": (
            "Im Pilot ausschließlich aggregiert prüfen, ob das "
            "nichtpersonale fiktive Fallurteil innerhalb der 15 Minuten "
            "entsteht und ohne Einsicht in die private Matrix funktioniert; "
            "private Inhalte und Bearbeitungszeiten werden nicht erhoben, "
            "übertragen, eingesammelt, gespeichert oder bewertet."
        ),
    },
    "BMB16-GYM-IK-MG-002": {
        "decision": "additional-time",
        "additionalMinutes": 20,
        "phaseIds": [
            "guided-practice",
            "review-revise-transfer",
        ],
        "rationale": (
            "Das Erläutern eines positiven Nutzungsaspekts und eines Risikos "
            "oder einer Gefahr übermäßiger Nutzung, ihr kriterien- und "
            "beleggestütztes Bewerten sowie das Ableiten einer passenden "
            "Präventionsmaßnahme benötigen 20 Minuten angeleitete Fallanalyse "
            "und Revision im gemeinsamen Abschnitt „Nutzen, Risiken und "
            "Prävention“ derselben Wirkungskarte."
        ),
        "risk": (
            "Eine bloße Liste von Nutzen, Risiken oder Verboten würde "
            "Erläuterung, belegtes Kriterienurteil und passende Prävention "
            "nicht ausführen; persönliche Nutzungsdaten sind für den "
            "vollständig vorgegebenen fiktiven Fall weder nötig noch "
            "zulässig."
        ),
        "followUp": (
            "Im Pilot am nichtpersonalen Fallprodukt prüfen, ob positiver "
            "Aspekt, Risiko oder Gefahr, Kriterien und Belege, begründetes "
            "Urteil und passende Präventionsmaßnahme innerhalb der 20 "
            "Minuten vollständig sichtbar werden."
        ),
    },
    "BMB16-GYM-IK-MG-003": {
        "decision": "absorbed",
        "additionalMinutes": 0,
        "phaseIds": [
            "guided-practice",
            "independent-action-product",
            "review-revise-transfer",
        ],
        "rationale": (
            "Im nichtpersonalen Abschnitt „Wirkung und bedingte "
            "Gesetzmäßigkeit“ nutzen die Untersuchung derselben zwei "
            "kuratierten Medienbeispiele, der Vergleich vollständig "
            "vorgegebener fiktiver Reaktionsdaten sowie Ableitung und "
            "Revision einer bedingten Wirkungsaussage bereits dieselbe "
            "positive Wirkungs- und Revisionsspur der gemeinsamen "
            "Wirkungskarte. Private Empfindungen oder private Ableitungen "
            "sind weder Voraussetzung dieser Spur noch beobachtbares Produkt "
            "oder Evidenz und tragen keine zusätzlichen Minuten."
        ),
        "risk": (
            "Aus der nichtpersonalen Wirkungsaussage dürfen weder private "
            "Empfindungen abgeleitet noch Einsicht, Gespräch, Abgabe oder "
            "Bewertung der privaten Reflexionsmatrix verlangt werden."
        ),
        "followUp": (
            "Im Pilot ausschließlich die nichtpersonale Untersuchung der "
            "fiktiven Reaktionsdaten sowie die bedingte Wirkungsaussage und "
            "ihre Revision in der gemeinsamen Wirkungskarte prüfen; private "
            "Empfindungen und Ableitungen werden nicht erhoben, übertragen, "
            "eingesammelt, gespeichert oder bewertet."
        ),
    },
    "BMB16-GYM-PK-RK-001": {
        "decision": "additional-time",
        "additionalMinutes": 15,
        "phaseIds": ["guided-practice"],
        "rationale": (
            "Die 15 Minuten gelten ausschließlich dem nichtpersonalen "
            "Abschnitt „Nutzungsvergleich“ der gemeinsamen Wirkungskarte: "
            "Die zwei vollständig vorgegebenen Nutzungssituationen des "
            "fiktiven Falls werden mit dem vorgegebenen Kriterienkatalog "
            "beschrieben und verglichen; Gemeinsamkeiten und Unterschiede "
            "werden begründet festgehalten. Eigenes Nutzungsverhalten und "
            "die private Vergleichsmatrix bilden weder die beobachtbare "
            "Produktspur noch den Zeitnachweis."
        ),
        "risk": (
            "Eine Übernahme eigener Nutzungssituationen in die gemeinsame "
            "Wirkungskarte oder eine Lehrkraftkontrolle der privaten Matrix "
            "würde die nichtpersonale Anschlussaufgabe in eine verdeckte "
            "Erhebung persönlicher Mediennutzung verwandeln."
        ),
        "followUp": (
            "Im Pilot nur prüfen, ob der fiktive Nutzungsvergleich mit "
            "gemeinsamen Kriterien, Gemeinsamkeiten und Unterschieden "
            "innerhalb der 15 Minuten gelingt und ohne Angaben aus der "
            "privaten Matrix verständlich bleibt."
        ),
    },
    "BMB16-GYM-PK-RK-002": {
        "decision": "additional-time",
        "additionalMinutes": 15,
        "phaseIds": ["independent-action-product"],
        "rationale": (
            "Die 15 Minuten sind ausschließlich dem nichtpersonalen "
            "Abschnitt „Lebenswelt und Medienwirklichkeit“ der gemeinsamen "
            "Wirkungskarte zugeordnet: Am vollständig vorgegebenen fiktiven "
            "Fall werden der Einfluss digitaler Medien auf dessen Lebenswelt "
            "sowie begründete Entsprechungen und Unterschiede zwischen "
            "Wirklichkeit und denselben kuratierten Medienbeispielen "
            "dargestellt. Die private Lebensweltreflexion ist keine "
            "beobachtbare Produkt- oder Evidenzspur."
        ),
        "risk": (
            "Persönliche Lebensbereiche dürfen weder abgefragt noch aus dem "
            "nichtpersonalen Fallprodukt erschlossen werden; sonst würde die "
            "gemeinsame Wirkungskarte die private Datenschutzgrenze "
            "unterlaufen."
        ),
        "followUp": (
            "Im Pilot ausschließlich die fiktive Lebensweltdarstellung und "
            "die begründete Beziehung zwischen Wirklichkeit und "
            "Medienwirklichkeit im gemeinsamen Produkt prüfen; die private "
            "Matrix bleibt vollständig außerhalb von Erhebung und Feedback."
        ),
    },
    "BMB16-GYM-PK-RK-003": {
        "decision": "unresolved",
        "additionalMinutes": 0,
        "phaseIds": [],
        "rationale": (
            "Ohne die ausstehende Ursachenreklassifikation von "
            "`private-local` zu `module-detail` existiert kein gültiger "
            "Evidenzvertrag für das Abschätzen und kriteriengestützte "
            "Bewerten medialer Selbstdarstellung. Deshalb werden weder eine "
            "private Erstleistung noch ein redundanter sichtbarer "
            "Fallnachweis und auch keine Einzelphase oder Zeit behauptet; "
            "der Record bleibt semantisch partial."
        ),
        "risk": (
            "Eine vorzeitige Zeitzuweisung würde eine fachlich "
            "unbeobachtbare fiktive Privatleistung und denselben Operator "
            "noch einmal als sichtbare Fallaufgabe modellieren und damit die "
            "Fehlklassifikation verdecken."
        ),
        "followUp": (
            "Nach einer späteren Design- und Ursachenreklassifikation genau "
            "einen shared- oder teacher-observable Fallnachweis für "
            "Folgenabschätzung und Kriterienurteil entwerfen und erst dann "
            "seinen positiven Zeitbedarf auditieren."
        ),
    },
    "LH26-E-DP-003": {
        "decision": "unresolved",
        "additionalMinutes": 0,
        "phaseIds": [],
        "rationale": (
            "Der geforderte Diskussionsoperator bezieht sich ausdrücklich "
            "auf Faszination, Konflikte und Probleme der eigenen "
            "Mediennutzung. Eine private Beschreibung ist keine Diskussion; "
            "eine beobachtbare Diskussion würde persönliche Nutzung "
            "offenlegen, während eine ausschließlich fiktive Falldiskussion "
            "den eigenen Bezug nicht erfüllt. Deshalb werden keine Phase, "
            "keine Minuten und kein verfügbarer Pfad behauptet; der Record "
            "bleibt semantisch partial."
        ),
        "risk": (
            "Gespräch, Lehrkraftbeobachtung, Abgabe oder "
            "Teilnahmeprotokollierung könnten sensible persönliche "
            "Nutzungsinhalte direkt oder indirekt erheben; ein fiktiver Fall "
            "würde dagegen die curriculare Lücke nur verdecken."
        ),
        "followUp": (
            "Im Curriculum- und Datenschutzreview klären, ob eine "
            "freiwillige, nicht bewertete und ausdrücklich nicht als "
            "Abdeckungs- oder Zeitnachweis verwendete Gesprächsgelegenheit "
            "pädagogisch angeboten werden soll; bis dahin bleibt der Record "
            "ohne Evidenzvertrag und Zeitzuweisung partial."
        ),
    },
}
CORE07_PRIVATE_FOLLOW_UP_TRACES = {
    "BMB16-GYM-IK-MG-001": (
        "Altersbezogene Bewertung",
        "fiktiven Fall",
        "Kriterienkatalog",
    ),
    "BMB16-GYM-IK-MG-003": (
        "Wirkung und bedingte Gesetzmäßigkeit",
        "fiktiver Reaktionsdaten",
        "bedingte Wirkungsaussage",
    ),
    "BMB16-GYM-PK-RK-001": (
        "Nutzungsvergleich",
        "vorgegebenen Nutzungssituationen",
        "Gemeinsamkeiten und Unterschiede",
    ),
    "BMB16-GYM-PK-RK-002": (
        "Lebenswelt und Medienwirklichkeit",
        "fiktiven Fall",
        "Wirklichkeit und Medienwirklichkeit",
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

    def test_repository_draft_has_the_capacity_contract_and_unimplemented_lists_empty(self):
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
                "timeReviews",
                "sequenceEvidence",
                "gradeJudgements",
                "risks",
                "pilotAssignments",
            },
        )
        self.assertEqual(time_model["schemaVersion"], 1)
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
        self.assertEqual(time_model["sequenceEvidence"], [])
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
    ):
        return validate_time_reviews(
            reviews,
            (
                self.remediation_payload
                if remediation_payload is None
                else remediation_payload
            ),
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

        reviews = []
        for entry in self.remediation_payload["entries"]:
            decision = (
                "unresolved"
                if entry["timeImpact"]["level"] == "roadmap-dependent"
                else "absorbed"
            )
            reviews.append(self.review(entry["competencyId"], decision))

        result = self.validate_reviews(reviews, require_complete=True)

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
            for competency_id in CORE07_AUDIT_EXPECTATIONS
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
            with self.subTest(
                core07_nonpersonal_product_path=budget["pathId"]
            ):
                product_phase = next(
                    phase
                    for phase in budget["phaseBudgets"]
                    if phase["phaseId"] == "independent-action-product"
                )
                self.assertEqual(
                    product_phase["learningFunction"],
                    CORE07_NONPERSONAL_PRODUCT_FUNCTION,
                )

        expected_paths = [
            "GRADE-5-BASELINE",
            "GRADE-5-REGULAR",
            "GRADE-5-EXTENDED",
        ]
        for competency_id, expected in CORE07_AUDIT_EXPECTATIONS.items():
            with self.subTest(core07_competency_id=competency_id):
                review = reviews_by_competency_id[competency_id]
                self.assertEqual(
                    {
                        field: review[field]
                        for field in (
                            "decision",
                            "additionalMinutes",
                            "phaseIds",
                            "rationale",
                            "risk",
                            "followUp",
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
        for competency_id in CORE07_AUDIT_EXPECTATIONS:
            expected_status = (
                "partial"
                if competency_id in CORE07_PARTIAL_IDS
                else "covered"
            )
            with self.subTest(core07_semantic_status=competency_id):
                self.assertEqual(
                    coverage_by_id[competency_id]["coverageStatus"],
                    expected_status,
                )
                self.assertEqual(
                    remediation_by_id[competency_id]["after"][
                        "coverageStatus"
                    ],
                    expected_status,
                )

        core07_module = next(
            module
            for module in module_payload["modules"]
            if module["id"] == "IUM-5-CORE-07"
        )
        evidence_by_competency_id = {
            evidence["competencyId"]: evidence
            for evidence in core07_module["coverageEvidence"]
        }
        for competency_id, required_traces in (
            CORE07_PRIVATE_FOLLOW_UP_TRACES.items()
        ):
            with self.subTest(core07_private_follow_up=competency_id):
                evidence = evidence_by_competency_id[competency_id]
                review = reviews_by_competency_id[competency_id]
                self._assert_core07_private_time_boundary(
                    review,
                    evidence,
                    required_traces,
                )

        for competency_id in CORE07_PARTIAL_IDS:
            with self.subTest(core07_partial_boundary=competency_id):
                handoff = remediation_by_id[competency_id]
                review = reviews_by_competency_id[competency_id]
                self.assertIsNone(handoff["evidenceContractId"])
                self.assertEqual(review["decision"], "unresolved")
                self.assertEqual(review["additionalMinutes"], 0)
                self.assertEqual(review["phaseIds"], [])
                self.assertEqual(review["pathAvailability"], [])

    def _assert_core07_private_time_boundary(
        self,
        review,
        evidence,
        required_traces,
    ):
        self.assertEqual(evidence["mode"], "private-local")
        self.assertEqual(evidence["productVisibility"], "private-local")
        self.assertEqual(
            evidence["privacyBoundary"],
            PRIVATE_LOCAL_BOUNDARY,
        )
        self.assertTrue(evidence["nonPersonalFollowUp"].strip())

        review_text = " ".join(
            review[field]
            for field in ("rationale", "risk", "followUp")
        )
        for required_trace in required_traces:
            with self.subTest(core07_nonpersonal_trace=required_trace):
                self.assertIn(
                    required_trace,
                    evidence["nonPersonalFollowUp"],
                )
                self.assertIn(required_trace, review_text)
        self.assertIn("nichtpersonal", review_text.casefold())
        self.assertNotIn("teacher-observable", review_text.casefold())
        self.assertTrue(
            any(
                boundary_trace in review_text.casefold()
                for boundary_trace in (
                    "weder beobachtet",
                    "nicht erhoben",
                    "keine beobachtbare",
                    "weder die beobachtbare",
                    "außerhalb von erhebung",
                )
            )
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

    def test_repository_time_reviews_match_the_audited_decisions(self):
        prior_reviews = self.time_payload["timeReviews"][
            : len(PRIOR_20_TIME_REVIEW_IDS)
        ]
        self.assertEqual(
            tuple(review["id"] for review in prior_reviews),
            PRIOR_20_TIME_REVIEW_IDS,
        )
        canonical_prior_reviews = json.dumps(
            prior_reviews,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        self.assertEqual(
            hashlib.sha256(canonical_prior_reviews).hexdigest(),
            PRIOR_20_TIME_REVIEWS_SHA256,
        )

        result = validate_time_reviews(
            self.time_payload["timeReviews"],
            self.remediation_payload,
            self.repository_module_contracts,
            self.repository_integration_contracts,
            self.repository_annual_variants,
            require_complete=False,
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
                "sequenceEvidenceStatus": "partial",
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
                "sequenceEvidenceStatus": "partial",
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
