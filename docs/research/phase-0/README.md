# Forschungsarchitektur Phase 0

Dieses Verzeichnis ist der kanonische Forschungsbestand für Phase 0. Es hält Quellen, Claims, Rechercheaufträge, Rohberichte, kuratierte Berichte und die paketübergreifende Synthese getrennt.

## Bestand und Reihenfolge

1. Das Quellenregister wird vor dem Anlegen eines Claims gepflegt.
2. Claims im Ledger verweisen ausschließlich auf registrierte Quellen.
3. Recherchepakete liefern reproduzierbare Aufträge, Rohberichte und kuratierte Ergebnisse.
4. Die Synthese klärt Übereinstimmungen, Spannungen und Übertragungsgrenzen zwischen den Paketen.
5. Erst danach werden Forschungsbefunde in Designprinzipien und das Fachprofil überführt.

## Paketstatus

| Paket | Gegenstand | Status |
| --- | --- | --- |
| `informatikdidaktik` | Konzepte, Programmieren und typische Lernhürden | working |
| `medienbildung` | Medienanalyse, Produktion, Rechte und Teilhabe | working |
| `lernpsychologie` | Üben, Feedback, Scaffolding und Transfer | working |
| `digitale-lernendenumgebungen` | Gestaltungsmerkmale digitaler Lernumgebungen | working |
| `integration` | Zusammenführung und Konfliktanalyse | working |

Die Statuswerte folgen dem [Forschungsprotokoll](research-protocol.md). Ein Rohbericht ist keine geprüfte Synthese und eine Synthese ist keine automatische Projektentscheidung.

## Abschlussreview vom 29. Juli 2026

**Ergebnis:** Phase 0 ist als Forschungs-, Fachprofil-, Curriculum- und Roadmapgrundlage **reviewfähig mit offenen Lücken**. Der Review schließt weder die 60 semantischen `partial`-Einträge noch die Zeitlücken der Roadmap durch Behauptung. Er aktiviert keine Phase-1-Planung.

### Automatisierte Prüfung

| Gate | Ergebnis |
| --- | --- |
| vollständige Unit-Test-Suite | 101 Tests, `OK` |
| `scripts/validate_phase0.py` | Exit `0`, `phase 0 validation passed` |
| `git diff --check` | ohne Befund |
| Red-Flag-Suche | keine Treffer in `README.md`, `docs`, `curriculum`, `roadmap`, `scripts`, `tests` |
| Encoding | keine Treffer für `Ã`, `Â` oder `�` in 36 versionierten Textdateien |
| Coverage-Vertrag | 171 Records: 111 `covered`, 60 `partial`, 0 `deferred` |
| Match-Rationales | 171 von 171 eindeutig |

Der im Plan wörtlich formulierte rekursive Encoding-Scan erfasst auch ignorierte binäre Dateien unter `scripts/__pycache__` und `tests/__pycache__` und kann dort zufällige Bytefolgen als Zeichen melden. Diese Dateien wurden nicht gelöscht. Das belastbare Gate wurde deshalb auf die mit `git ls-files` ermittelten versionierten Textdateien begrenzt und schloss `__pycache__`, `.pytest_cache`, `.pyc` und `.pyo` ausdrücklich aus.

## Manueller Quellen- und Coverage-Audit

### Forschungsclaims

Je Forschungspaket wurden der erste, mittlere und letzte Claim in Ledger-Reihenfolge gegen Quellenregister, Kuration, Scope, Evidenzniveau und Limitationen geprüft.

| Paket | geprüfte Claims | Befund |
| --- | --- | --- |
| Informatikdidaktik | `CLAIM-INF-001`, `CLAIM-INF-006`, `CLAIM-INF-011` | Quellen registriert und `primary-checked`; K-8-, Hochschul- und Normativitätsgrenzen bleiben sichtbar |
| Medienbildung | `CLAIM-MED-001`, `CLAIM-MED-007`, `CLAIM-MED-013` | Quellen registriert und `primary-checked`; Wirksamkeit, Einzelfallschutz und Lizenzreichweite werden nicht überdehnt |
| Lernpsychologie und Unterricht | `CLAIM-LP-001`, `CLAIM-LP-007`, `CLAIM-LP-013` | Quellen registriert und `primary-checked`; Domänen-, Alters-, Kausalitäts- und Digitalitätsgrenzen sind explizit |
| Digitale Lernumgebungen und OER | `CLAIM-DLE-001`, `CLAIM-DLE-007`, `CLAIM-DLE-014` | Quellen registriert und `primary-checked`; Standardstatus, Browserabhängigkeit und fehlender Lernwirksamkeitsnachweis bleiben getrennt |

Alle zwölf Claim-IDs sind im jeweils passenden kuratierten Bericht enthalten. Im Quellenregister gibt es **keine** Quelle mit `verificationStatus: secondary-only`. Der einzige nicht primärgeprüfte Registereintrag, `SRC-LP-SIGNALING-2018` mit `metadata-checked`, trägt keinen retained Claim.

### Curriculumstichprobe

Geprüft wurden erster, mittlerer und letzter Record jeder durch `sourceLocator.section` ausgewiesenen Quellsektion. Bei Sektionen mit zwei Records wurden beide geprüft. Das ergibt 100 Recordprüfungen in 34 Sektionen. Kontrolliert wurden `sourceId`, Recordtyp, Status `verified`, `text`, `sourceText`, Seite und Abschnittslocator.

#### Lesehilfe 2026/2027 – `orientation`

| Quellsektion | Records | Stichprobe |
| --- | ---: | --- |
| Inhaltliche Ausrichtung in den Klassen 5 und 6 | 2 | `LH26-E-PROG-001`, `LH26-E-PROG-002` |
| Neuausrichtung in Klasse 7 | 2 | `LH26-E-PROG-003`, `LH26-E-PROG-004` |
| Klassen 5/6 – Digitalität und Partizipation: Bewusste Mediennutzung | 7 | `LH26-E-DP-001`, `LH26-E-DP-004`, `LH26-E-DP-006` |
| Klassen 5/6 – Digitalität und Partizipation: Von der Mediennutzung zur informationellen Selbstbestimmung | 4 | `LH26-E-DP-007`, `LH26-E-DP-EX-002`, `LH26-E-DP-009` |
| Klassen 5/6 – Information und Daten: Informationen suchen und prüfen | 6 | `LH26-E-ID-001`, `LH26-E-ID-002`, `LH26-E-ID-004` |
| Klassen 5/6 – Information und Daten: Informationen einordnen und codieren | 15 | `LH26-E-ID-005`, `LH26-E-ID-010`, `LH26-E-ID-015` |
| Klassen 5/6 – Algorithmen: Erste Schritte in der Programmierung | 9 | `LH26-E-ALG-EX-001`, `LH26-E-ALG-003`, `LH26-E-ALG-006` |
| Klassen 5/6 – Kommunikation und Sicherheit: Kommunikation im digitalen Raum | 8 | `LH26-E-KS-001`, `LH26-E-KS-003`, `LH26-E-KS-007` |
| Klassen 5/6 – Kommunikation und Sicherheit: Internet und soziale Medien | 12 | `LH26-E-KS-008`, `LH26-E-KS-011`, `LH26-E-KS-015` |
| Klassen 5/6 – Digitales Arbeiten: Bedienkonzepte in digitalen Werkzeugen | 13 | `LH26-E-DA-001`, `LH26-E-DA-005`, `LH26-E-DA-009` |
| Klassen 5/6 – Digitales Arbeiten: Gestaltung und Produktion digitaler Medien | 9 | `LH26-E-DA-EX-005`, `LH26-E-DA-EX-007`, `LH26-E-DA-015` |
| Klasse 7 – Digitalität und Partizipation: Gaming und Manipulation durch Medien | 13 | `LH26-E-DP-010`, `LH26-E-DP-014`, `LH26-E-DP-018` |
| Klasse 7 – Information und Daten: Grundlagen digitaler Daten | 7 | `LH26-E-ID-016`, `LH26-E-ID-019`, `LH26-E-ID-022` |
| Klasse 7 – Algorithmen: Algorithmische Grundbausteine | 8 | `LH26-E-ALG-007`, `LH26-E-ALG-EX-004`, `LH26-E-ALG-012` |
| Klasse 7 – Kommunikation und Sicherheit: Einfache kryptographische Verfahren | 7 | `LH26-E-KS-016`, `LH26-E-KS-019`, `LH26-E-KS-022` |
| Klasse 7 – Digitales Arbeiten: Manipulation von Medien | 3 | `LH26-E-DA-EX-008`, `LH26-E-DA-016`, `LH26-E-DA-017` |

#### Basiskurs Medienbildung 2016 – `enacted`

| Quellsektion | Records | Stichprobe |
| --- | ---: | --- |
| 2.1 Sachkompetenz | 3 | `BMB16-GYM-PK-SK-001`, `BMB16-GYM-PK-SK-002`, `BMB16-GYM-PK-SK-003` |
| 2.2 Handlungskompetenz | 3 | `BMB16-GYM-PK-HK-001`, `BMB16-GYM-PK-HK-002`, `BMB16-GYM-PK-HK-003` |
| 2.3 Reflexionskompetenz | 4 | `BMB16-GYM-PK-RK-001`, `BMB16-GYM-PK-RK-002`, `BMB16-GYM-PK-RK-004` |
| 3.1.1 Information und Wissen | 6 | `BMB16-GYM-IK-IW-001`, `BMB16-GYM-IK-IW-002`, `BMB16-GYM-IK-IW-003-EX-001` |
| 3.1.2 Produktion und Präsentation | 6 | `BMB16-GYM-IK-PP-001`, `BMB16-GYM-IK-PP-002`, `BMB16-GYM-IK-PP-003-EX-001` |
| 3.1.3 Kommunikation und Kooperation | 6 | `BMB16-GYM-IK-KK-001`, `BMB16-GYM-IK-KK-002`, `BMB16-GYM-IK-KK-003-EX-001` |
| 3.1.4 Mediengesellschaft | 6 | `BMB16-GYM-IK-MG-001`, `BMB16-GYM-IK-MG-002`, `BMB16-GYM-IK-MG-003-EX-001` |
| 3.1.5 Grundlagen digitaler Medienarbeit | 6 | `BMB16-GYM-IK-GM-001`, `BMB16-GYM-IK-GM-002`, `BMB16-GYM-IK-GM-003-EX-001` |
| 4. Operatoren | 19 | `BMB16-GYM-OP-001`, `BMB16-GYM-OP-010`, `BMB16-GYM-OP-019` |

#### Aufbaukurs Informatik Klasse 7 – `enacted`

| Quellsektion | Records | Stichprobe |
| --- | ---: | --- |
| 2.1 Strukturieren und Vernetzen | 8 | `INF7-16-GYM-PK-SV-001`, `INF7-16-GYM-PK-SV-002-EX-001`, `INF7-16-GYM-PK-SV-005` |
| 2.2 Modellieren und Implementieren | 11 | `INF7-16-GYM-PK-MI-001`, `INF7-16-GYM-PK-MI-006`, `INF7-16-GYM-PK-MI-010` |
| 2.3 Kommunizieren und Kooperieren | 7 | `INF7-16-GYM-PK-KK-001`, `INF7-16-GYM-PK-KK-004`, `INF7-16-GYM-PK-KK-006` |
| 2.4 Analysieren und Bewerten | 7 | `INF7-16-GYM-PK-AB-001`, `INF7-16-GYM-PK-AB-003`, `INF7-16-GYM-PK-AB-006` |
| 3.1.1 Daten und Codierung | 11 | `INF7-16-GYM-IK-DC-001`, `INF7-16-GYM-IK-DC-004`, `INF7-16-GYM-IK-DC-008-EX-001` |
| 3.1.2 Algorithmen | 10 | `INF7-16-GYM-IK-ALG-001`, `INF7-16-GYM-IK-ALG-004`, `INF7-16-GYM-IK-ALG-007` |
| 3.1.3 Rechner und Netze | 6 | `INF7-16-GYM-IK-RN-001`, `INF7-16-GYM-IK-RN-002-EX-001`, `INF7-16-GYM-IK-RN-003-EX-002` |
| 3.1.4 Informationsgesellschaft und Datensicherheit | 12 | `INF7-16-GYM-IK-IGD-001`, `INF7-16-GYM-IK-IGD-003-EX-001`, `INF7-16-GYM-IK-IGD-006-EX-001` |
| 4. Operatoren | 22 | `INF7-16-GYM-OP-001`, `INF7-16-GYM-OP-011`, `INF7-16-GYM-OP-022` |

Die Stichprobe ergab keinen neuen Korrekturbedarf. Beispiele bleiben als `example`, Operatoren als `operator`, Prozesskompetenzen als `process-competency`; die Lesehilfe bleibt `orientation`.

### Alle 60 `partial`-Einträge

Jeder `partial`-Eintrag wurde einzeln gegen exakten Anforderungstext, Evidenz-Kernkandidat, zentrale Lernhandlung, Produkt, `matchRationale`, Grund, Risiko und Folgeaktion gelesen. Alle 60 Gründe, Risiken und Folgeaktionen sind recordgenau und eindeutig. Die vier Progressionsrecords verlangen zu Recht einen jahrgangsweiten Sequenznachweis statt eines zusätzlichen Einzelprodukts.

| Evidenz-Kernkandidat | Anzahl | einzeln geprüfte Records |
| --- | ---: | --- |
| `IUM-5-CORE-01` | 7 | `BMB16-GYM-IK-GM-001`, `BMB16-GYM-IK-GM-002`, `BMB16-GYM-IK-GM-003`, `BMB16-GYM-PK-SK-003`, `LH26-E-DA-004`, `LH26-E-DP-001`, `LH26-E-PROG-001` |
| `IUM-5-CORE-02` | 1 | `LH26-E-ID-009` |
| `IUM-5-CORE-03` | 6 | `BMB16-GYM-IK-KK-002`, `BMB16-GYM-IK-KK-003`, `BMB16-GYM-PK-HK-003`, `BMB16-GYM-PK-RK-004`, `LH26-E-KS-001`, `LH26-E-KS-002` |
| `IUM-5-CORE-05` | 2 | `LH26-E-ALG-001`, `LH26-E-PROG-002` |
| `IUM-5-CORE-06` | 4 | `BMB16-GYM-IK-PP-002`, `LH26-E-DA-005`, `LH26-E-DA-006`, `LH26-E-DA-008` |
| `IUM-5-CORE-07` | 7 | `BMB16-GYM-IK-MG-001`, `BMB16-GYM-IK-MG-002`, `BMB16-GYM-IK-MG-003`, `BMB16-GYM-PK-RK-001`, `BMB16-GYM-PK-RK-002`, `BMB16-GYM-PK-RK-003`, `LH26-E-DP-003` |
| `IUM-6-CORE-02` | 2 | `LH26-E-DP-004`, `LH26-E-DP-006` |
| `IUM-6-CORE-06` | 2 | `LH26-E-KS-014`, `LH26-E-KS-015` |
| `IUM-6-CORE-07` | 4 | `LH26-E-DA-009`, `LH26-E-DA-010`, `LH26-E-DA-012`, `LH26-E-DA-015` |
| `IUM-7-CORE-01` | 5 | `INF7-16-GYM-IK-DC-001`, `INF7-16-GYM-IK-DC-004`, `INF7-16-GYM-IK-DC-005`, `LH26-E-ID-020`, `LH26-E-ID-021` |
| `IUM-7-CORE-03` | 6 | `INF7-16-GYM-IK-ALG-003`, `INF7-16-GYM-PK-MI-005`, `INF7-16-GYM-PK-SV-003`, `LH26-E-ALG-007`, `LH26-E-ALG-008`, `LH26-E-ALG-009` |
| `IUM-7-CORE-04` | 3 | `INF7-16-GYM-PK-KK-002`, `INF7-16-GYM-PK-MI-003`, `INF7-16-GYM-PK-SV-002` |
| `IUM-7-CORE-05` | 3 | `INF7-16-GYM-IK-IGD-004`, `INF7-16-GYM-PK-AB-002`, `INF7-16-GYM-PK-SV-001` |
| `IUM-7-CORE-08` | 7 | `INF7-16-GYM-IK-IGD-006`, `INF7-16-GYM-PK-AB-005`, `INF7-16-GYM-PK-AB-006`, `INF7-16-GYM-PK-KK-006`, `LH26-E-DP-013`, `LH26-E-PROG-003`, `LH26-E-PROG-004` |
| `IUM-7-CORE-10` | 1 | `LH26-E-DP-014` |

Verteilung: 31 `partial` aus den beiden `enacted` Bildungsplänen und 29 aus der Lesehilfe mit Gewicht `orientation`; 15 BMB-, 16 INF7- und 29 Lesehilfe-Records. Die Einträge bleiben offen. Eine spätere Änderung zu `covered` erfordert den jeweils dokumentierten operator- und produktgenauen Re-Audit.

### Abhängigkeiten des Kernpfads

Alle 31 Kanten des Kernpfads wurden einzeln auf fachliche Voraussetzung, Jahrgangsrichtung und Kernstatus geprüft. Die folgende kompakte Darstellung enthält jede Kante:

| Zielmodul | geprüfte unmittelbare Voraussetzungen |
| --- | --- |
| `IUM-5-CORE-01` | keine |
| `IUM-5-CORE-02` | `IUM-5-CORE-01` |
| `IUM-5-CORE-03` | `IUM-5-CORE-01` |
| `IUM-5-CORE-04` | `IUM-5-CORE-01` |
| `IUM-5-CORE-05` | `IUM-5-CORE-01` |
| `IUM-5-CORE-06` | `IUM-5-CORE-01`, `IUM-5-CORE-02` |
| `IUM-5-CORE-07` | `IUM-5-CORE-02` |
| `IUM-6-CORE-01` | `IUM-5-CORE-02` |
| `IUM-6-CORE-02` | `IUM-5-CORE-07`, `IUM-6-CORE-01` |
| `IUM-6-CORE-03` | `IUM-5-CORE-05` |
| `IUM-6-CORE-04` | `IUM-5-CORE-05` |
| `IUM-6-CORE-05` | `IUM-5-CORE-04` |
| `IUM-6-CORE-06` | `IUM-5-CORE-03`, `IUM-5-CORE-07` |
| `IUM-6-CORE-07` | `IUM-5-CORE-06`, `IUM-6-CORE-01` |
| `IUM-7-CORE-01` | `IUM-6-CORE-03` |
| `IUM-7-CORE-02` | `IUM-7-CORE-01` |
| `IUM-7-CORE-03` | `IUM-6-CORE-04` |
| `IUM-7-CORE-04` | `IUM-7-CORE-03` |
| `IUM-7-CORE-05` | `IUM-6-CORE-05` |
| `IUM-7-CORE-06` | `IUM-7-CORE-01`, `IUM-7-CORE-05` |
| `IUM-7-CORE-07` | `IUM-7-CORE-06` |
| `IUM-7-CORE-08` | `IUM-6-CORE-01`, `IUM-6-CORE-02` |
| `IUM-7-CORE-09` | `IUM-6-CORE-02`, `IUM-7-CORE-08` |
| `IUM-7-CORE-10` | `IUM-6-CORE-07`, `IUM-7-CORE-08` |

Der Graph ist azyklisch; keine Kante führt in einen früheren Jahrgang und kein Kernmodul hängt von einem flexiblen Modul ab. Die sieben flexiblen Kandidaten docken ausschließlich an Kernmodule an und sind keine verdeckten Kernvoraussetzungen.

### `reviewed` Designprinzipien

| Prinzip | Claim- und Quellenprüfung | Profilbezug | Befund |
| --- | --- | --- | --- |
| `PRIN-011` Datenminimierung und fehlertolerante lokale Arbeit | `CLAIM-DLE-004` bis `-006`; alle tragenden Quellen `primary-checked` | nicht personenbezogene Diagnose; Quellen/Lizenz/Aktualität/Accessibility | `reviewed` ist für die belegte Rechts-/Standardbasis plausibel; konkrete Datenflüsse und Rechtsprüfung bleiben Phase-1-Gates |
| `PRIN-012` WCAG-Baseline durch reale Nutzeraufgaben ergänzen | `CLAIM-DLE-001` bis `-003`; alle tragenden Quellen `primary-checked` | Material-/Repräsentationsstandards; Accessibility | technische Baseline, schulische Bedienbarkeit und Lernwirksamkeit bleiben korrekt getrennt |
| `PRIN-014` OER als bearbeitbare Rechte- und Quellenkette ausliefern | `CLAIM-MED-013`, `CLAIM-DLE-009` bis `-011`; alle tragenden Quellen `primary-checked` | Medienproduktion; Quellen/Lizenz/Aktualität/Accessibility | Lizenzreichweite, Drittmaterial und gerichtete Kompatibilität bleiben als Risiken sichtbar |

## Spezifikationsabdeckung

Die Matrix ordnet die für Phase 0 relevanten Anforderungen aus den Abschnitten 3, 4, 5, 8, 9 und 13 sowie aus der Phase-0-Definition des Gesamtdesigns konkreten Artefakten zu. Ein Gedankenstrich in der Curriculumspalte bedeutet, dass die Anforderung eine Projekt- oder Technikregel und keine Curriculumvorgabe ist.

| Gesamtdesign-Anforderung | Forschungsartefakt | Profilregel | Curriculumanker | Roadmap/Coverage | Ergebnis oder echte Lücke |
| --- | --- | --- | --- | --- | --- |
| §3: Lesehilfe nur als Orientierung; BMB/INF7 weiter geltend | `source-register.json`, `research-protocol.md` | §2 Quellenbasis und Geltung | drei `competencies.json`, `crosswalk.json` | `normativeWeight` in `coverage-plan.json` | erfüllt; 95 `orientation`, 76 `enacted` |
| §3: Niveau E und fünf Lesehilfe-Bereiche | `synthesis.md` | §§4–7 | `LH26-E-*` | Kernkandidaten der Klassen 5–7 | erfüllt; konkrete 5/6-Verteilung bleibt `working` |
| §3: Prozesse und Operatoren gemeinsam auswerten | Claim-Ledger zu fachlichen Praktiken | §§3, 9, 10 | `operators.json` mit 78 Einträgen | Lernhandlungen und Produkte je Kandidat | erfüllt; keine universelle Operatorenhierarchie behauptet |
| §3: Abdeckung nur durch Mapping belegen | `data-contract.md` | §2 und §3 | `crosswalk.json` | 171 recordgenaue Coverage-Einträge | strukturell erfüllt; 60 Records bleiben semantisch `partial` |
| §3: neue amtliche Vorgaben überwachen | `research-protocol.md` | §19 Recheck-Trigger | `source-status.md` | Quellenstand als Roadmaprisiko | offen bis zur tatsächlichen Veröffentlichung eines neuen Fachplans |
| §4: Problem, Frage oder Gestaltungsauftrag statt Buchkapitel | `synthesis.md`, `PRIN-001` | §§3 und 8 | repräsentative Fachrecords je Modul | `centralQuestion`, `centralLearningAction`, `centralLearningProduct` | auf Kandidatenebene erfüllt |
| §4.1–4.7: sieben funktionale Modulphasen | `PRIN-001`, `PRIN-003` bis `-008` | §§8, 12 und 13 | BMB-/INF7-Prozesskompetenzen | alle 24 Kernkandidaten besitzen die vollständige `moduleGrammar` | Kandidatenvertrag erfüllt; konkrete Modulausgestaltung und Erprobung offen |
| §4.2 und §4.6: keine zentrale personenbezogene Speicherung | `CLAIM-LP-002`, `-010`, `PRIN-009`, `PRIN-011` | §15 | Reflexions- und Analysekompetenzen | private Reflexion nicht erhoben; keine Profile in Kandidaten | erfüllt auf Planungs- und Kandidatenebene |
| §4.5–4.6: fachliches Produkt, Prüfung und Revision | `PRIN-005`, `PRIN-008`, `PRIN-015` | §§9, 10, 12 und 17 | produkt- und prozessbezogene Records | Produkt und Revision je Kandidat; recordgenaue Coverage | 60 konkrete Operator-Produkt-Lücken bleiben offen |
| §4.7: gemeinsame Sicherung | `CLAIM-LP-001`, `-012` | §§12 und 13 | fachliche Begriffe und Prozessrecords | `shared-consolidation` in allen Kernkandidaten | Kandidatenvertrag erfüllt; Handbuch und Unterrichtserprobung offen |
| §5.1: Klasse 5 handlungsfähig machen | Informatik-, Medien- und Lernpsychologie-Synthese | §7 Progression | BMB plus Lesehilfe 5/6 | sieben Klasse-5-Kernkandidaten | fachlich plausibel; 31–44 Einheiten, Status `amber` |
| §5.2: Klasse 6 Mechanismen und Wirkungen | Medien-/Informatiksynthese | §§5–7 | Lesehilfe 5/6 | sieben Klasse-6-Kernkandidaten | fachlich plausibel; 35–50 Einheiten, Status `red` |
| §5.3: Klasse 7 Systeme analysieren und gestalten | Informatik-/Mediensynthese | §§4–7, 9 und 10 | INF7 plus Lesehilfe 7 | zehn Klasse-7-Kernkandidaten | fachlich plausibel; 54–78 Einheiten, Status `red` |
| §5.4: Perspektiven nur fachlich begründet verbinden | `synthesis.md`, `PRIN-008` | §6 Integration | `LH26-E-PROG-003`, `-004` und Crosswalk-Brücken | integrierte Kandidaten und Abhängigkeitsketten | Einzelmodule plausibel; jahrgangsweite Perspektivenbalance bleibt bei beiden Progressionsrecords `partial` |
| §8: Beurteilungsinstrumentarium vollständig, reduzierbar und datensparsam | `PRIN-015` | §17 | Produkt- und Prozesskompetenzen | `assessmentWorkingNotes` in allen Kandidaten | als `working` vorhanden; Umfang und Validität brauchen Nutzerreview und spätere Erprobung |
| §9.1: Informatikdidaktik | Prompt, Raw- und Curated-Paket 01 | §§4, 9, 11 | Algorithmen-, Daten-, Netz- und Prozessrecords | Informatikpfade und Coverage | erfüllt mit sichtbaren Alters-/Domänengrenzen |
| §9.2: Medienbildungsdidaktik | Prompt, Raw- und Curated-Paket 02 | §§5 und 10 | Medienbildungs- und Gesellschaftsrecords | Medienanalyse-/Produktionspfade | erfüllt mit Schutz- und Wirkungsgrenzen |
| §9.3: Lernpsychologie und Unterricht | Prompt, Raw- und Curated-Paket 03 | §§8, 11–13 | fachliche Prozessrecords als Anwendungskontext | Modulgrammatik und Unterstützung | erfüllt; konkrete IuM-Übertragungen bleiben `working` |
| §9.4: digitale Lernumgebungen und OER | Prompt, Raw- und Curated-Paket 04 | §§14–16 | Rechte-, Datenschutz- und Produktionsrecords, soweit curricular | Medienbegründung, Analogmaterial, erhöhte Prüffälle | Forschungsgrundlage erfüllt; technische Umsetzung gehört nicht zu Phase 0 |
| §9.5: Evidenz-, Curriculum- und Projektstatus trennen | `research-protocol.md`, Claim-Ledger, Designprinzipien | §2 Regelhierarchie | Quellenstatus und Recordstatus | Roadmap und Coverage `working` | erfüllt; kein Artefakt wird automatisch `standard` |
| §13.1: didaktische Gates | Synthese und 15 Designprinzipien | §§3, 8–18 | Crosswalk und Operatorenmodell | Kandidatengraph, Coverage und Roadmapreview | auf Phase-0-Artefakte angewandt; Modul- und Handbuchprüfung offen |
| §13.2: technische Gates | DLE-Claims, `PRIN-011`, `-012`, `-014` | §§14–16 | – | nur Anforderungen und Pilotkriterien dokumentiert | bewusst offen: keine Plattform-, Offline-, Speicher-, Browser- oder Performanceimplementierung in Phase 0 |
| §13.3: Review und Erprobung | Forschungsprotokoll und Recheck-Logik | §19 | Curriculumstatus | taskbezogene Reviews dokumentiert | unabhängige Taskreviews erfolgt; Nutzerreview, Goldstandard-Pilot und Unterrichtserprobung offen |
| Phase 0: vier Researchpakete und quellenkritische Kuration | vier Prompt-/Raw-/Curated-Pakete, Ledger, Register, Synthese | Forschungsregeln im gesamten Profil | – | Designprinzipien tragen die Roadmap | erfüllt |
| Phase 0: Fachprofil | Synthese und Designprinzipien | kanonisches 19-teiliges Fachprofil | fünf registrierte Curriculumanker | Profilzuordnungen in 15 von 15 Prinzipien | erfüllt, Status `working` |
| Phase 0: vollständiges Mapping | Forschungs- und Datenvertrag | Abdeckungsgate in §2/§3 | 278 Records vollständig im Crosswalk aufgelöst | 171 Anforderungsrecords zugeordnet | strukturell erfüllt; keine semantische Vollabdeckung behauptet |
| Phase 0: erster Roadmapentwurf | Designprinzipien und Profil | Progressions- und Modulregeln | 171 Anforderungsrecords | 31 Kandidaten, azyklischer Graph, Zeitmodell | Entwurf erfüllt; 60 `partial` und zwei rote Jahrgänge verhindern Vollfreigabe |

## Plan-Level-Akzeptanz

| Kriterium | Stand |
| --- | --- |
| vier Pakete mit Prompt, Raw und Curated | erfüllt |
| jeder retained Claim mit registrierter Quelle und Limitation | erfüllt |
| Fachprofil trennt persönliche Annahmen, Evidenz, Curriculum und Projektentscheidungen | erfüllt |
| drei Curriculumquellen mit Locators und Recordstatus extrahiert | erfüllt |
| Crosswalk berücksichtigt jeden Record | erfüllt: 278 aufgelöst, darunter 107 begründet separat geführte Beispiele/Operatoren |
| Progression trennt Norm und didaktische Sequenz | erfüllt |
| Modulkandidaten bilden einen azyklischen Graph | erfüllt |
| jeder enacted Anforderungsrecord ist `covered`, `partial` oder `deferred` | erfüllt: 45 `covered`, 31 `partial`, 0 `deferred` |
| progressiver Kern und flexible Architektur bleiben erhalten | erfüllt: 24 Kern-, 7 flexible Kandidaten |
| keine Phase-1-Implementierung in Phase 0 | erfüllt |
| automatisierte Tests und manueller Audit | erfüllt für den Phase-0-Bestand; offene Befunde bleiben dokumentiert |
| Repository- und Workspace-Handoff | nach Task-15-Commit und Nutzerreview-Gates vollständig vorbereitet |

## Echte offene Punkte

1. **Semantische Abdeckung:** 60 Records sind `partial`; eine Vollabdeckungsbehauptung ist unzulässig.
2. **Zeit:** Klasse 5 liegt bei 31–44 Einheiten knapp über dem 30er-Kern und bleibt `amber`; Klasse 6 mit 35–50 und Klasse 7 mit 54–78 sind `red`.
3. **Klassen 5/6:** Die jahrgangsgenaue Aufteilung des gemeinsamen Lesehilfebands ist eine revidierbare Projektentscheidung.
4. **Quellenstand:** Die Lesehilfe ist `orientation`; der angekündigte Fachplan und dynamische Rechts-/Technikstände benötigen Rechecks.
5. **Beurteilungsinstrumentarium:** Der Bestand ist ausdrücklich reduzierbar und noch nicht durch Nutzerreview oder Unterrichtserprobung validiert.
6. **Technik und Erprobung:** Plattform-, Offline-, Speicher-, Browser-, Accessibility-, Performance- und Handbuchabnahmen sowie der Goldstandard-Pilot liegen außerhalb von Phase 0.

## Vier Nutzerreview-Gates

Phase 1 darf erst spezifiziert werden, wenn die folgenden vier Entscheidungen getrennt angenommen oder bewusst revidiert wurden:

1. **Forschungssynthese:** Sind Claim-Auswahl, Evidenzgrenzen, Spannungen und die zwölf `working` gegenüber drei `reviewed` Designprinzipien als Grundlage akzeptiert?
2. **Fachprofil:** Sind Fachkern, getrennte Lernstränge, Integrationskriterien, Orchestrierung, Analog-/Digitalentscheidung und reduzierbares Beurteilungsinstrumentarium akzeptiert?
3. **Curriculare Vollständigkeit:** Werden Quellenstatus, Crosswalk, Operatorenmodell, offene 5/6-Verteilung und die 60 recordgenauen `partial`-Lücken akzeptiert oder zur Nacharbeit zurückgegeben?
4. **Modulroadmap:** Werden Kandidatengraph, Hybridmodell, Abhängigkeiten, `amber`/`red`-Zeiturteile und der nur empfohlene Goldstandard-Pilot akzeptiert oder revidiert?

Eine Zustimmung zu einem Gate ersetzt nicht die Entscheidung über die anderen drei. Insbesondere darf die Roadmap nicht als zeitlich freigegeben gelten, solange die roten Jahrgänge und die 60 `partial`-Lücken bestehen.
