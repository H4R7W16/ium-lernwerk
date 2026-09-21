# IuM-Lernwerk

Neue zusätzliche Referenzstrecke: **[Mit Schleifen planen – eigenständig lernen](https://h4r7w16.github.io/ium-lernwerk/selbstlernen/)** · **[Lesefassung](https://h4r7w16.github.io/ium-lernwerk/selbstlernen/read.html)** · [Quellcode und Anleitung](prototypes/m06-selbstlernen/README.md). Stand 21.09.2026 nach UX11-Nacharbeit, als Prüffassung zugänglich; keine Schülererprobung oder Unterrichtsfreigabe. Die bisherige Startadresse und die folgenden älteren Fassungen bleiben erhalten.

Ein digitales Lernwerk für Informatik und Medienbildung am Gymnasium in Baden-Württemberg, Klassen 5 bis 7. Ziel sind verständliche, relevante Aufgaben, an denen Lernende informatische Zusammenhänge selbst untersuchen und erklären können. Das Lehrwerk befindet sich in Entwicklung.

## Beispielinhalt ausprobieren: Sauber geplant

**[Aktuelle Lernfassung 2 im Browser öffnen](https://h4r7w16.github.io/ium-lernwerk/reinigungsfall-v2/)** – ohne Installation oder Anmeldung.

Der Beispielinhalt zeigt M06 für Klasse 5: Nach dem Basteln soll ein Modellroboter die Bodenfläche reinigen. Neun frei anwählbare Lernschritte führen von Bewegung und Drehung über Vorhersagen, Wiederholungen und Fehlerkorrektur zum eigenen Plan. Transfer und eine selbst aufgebaute Abschlussfolge sichern die fachlichen Zusammenhänge. Die Schritte sind keine neun Unterrichtsstunden.

Der Stand ist für den informellen Austausch in einem kleinen Kreis gedacht. Eindrücke und Probleme **direkt an Jan** zurückmelden; ein Formular, GitHub-Konto oder festes Prüfprogramm ist nicht nötig.

### Was lässt sich ausprobieren?

- Einzelne Aktionen oder ganze Wiederholungskörper verfolgen; aktueller Körperbefehl, Durchlauf, Ort und Blickrichtung sind sichtbar.
- Eine Endkachel und Blickrichtung vorhersagen, neue Aufgaben ergänzen und eigene Programme ausführen.
- Randrunde und vollständige Reinigung unterscheiden; beim Überarbeiten bleibt der Grundriss sichtbar.
- Eigene Erklärungen mit konkreten Beispielen vergleichen und ausgewählte Läufe festhalten.
- Eine neue Befehlsfolge selbst aufbauen und korrigieren.
- Den Arbeitsstand als Datei sichern und öffnen oder freiwillig im Browser behalten.

**Ohne gewählte Sicherung bleiben Eingaben nur im geöffneten Tab.** Browserspeicherung ist an das Gerät, den Browser und die Adresse gebunden; für einen Wechsel eine Datei mitnehmen. Ablaufgrafiken entstehen weiterhin auf Papier.

Dies ist ein ausführbarer Beispielinhalt, noch nicht das gesamte Lehrwerk 5–7. Die Vorschau besitzt feste Bewegungsbefehle, keine Sensorsteuerung. Automatisierte Prüfungen bewerten weder freie Erklärungen noch tatsächliche Lernwirksamkeit. Reale Unterrichtserprobung und umfassende Zugänglichkeitsprüfung bleiben offen.

### Quellcode, Anleitung und Vergleich

| Gesucht | Einstieg |
| --- | --- |
| Aktueller Beispielinhalt und Quellcode | [prototypes/m06-reinigungsfall-v2](prototypes/m06-reinigungsfall-v2/) |
| Lernweg, Speicherung und lokale Nutzung | [Anleitung zur Lernfassung 2](prototypes/m06-reinigungsfall-v2/README.md) |
| Dokumentierte lokale Vorprüfung | [QA der Lernfassung 2](prototypes/m06-reinigungsfall-v2/QA.md) |
| Erste Reinigungsfassung zum Vergleich | [Im Browser öffnen](https://h4r7w16.github.io/ium-lernwerk/reinigungsfall.html) · [Quellcode](prototypes/m06-reinigungsfall/) |
| Fachliche Ausgangsplanung und Musterlösungen | [Ausarbeitung M06](https://github.com/H4R7W16/ium-lernwerk/blob/4abbe6c2225e608f9bc10c9ae9a4028477235864/docs/planning/ium-5-7/m06-reinigungsfall.md) |
| Roter Faden 5–7 und externe Lernangebote | [Planungsübersicht](https://github.com/H4R7W16/ium-lernwerk/blob/4abbe6c2225e608f9bc10c9ae9a4028477235864/docs/planning/ium-5-7/README.md) |

Die verlinkte Ausgangsplanung liegt auf einem festgehaltenen Entwicklungsstand. Die zusätzliche Fassung setzt die nachfolgende Lernendenanalyse um; ihre aktuelle Lernfolge ist in der Anleitung dokumentiert. Weitergehende Planungen sind nicht automatisch Funktionen der Vorschau.

Der manuelle [Workflow „Selbstlernstrecke Pages“](https://github.com/H4R7W16/ium-lernwerk/actions/workflows/selbstlernen-pages.yml) prüft ausschließlich Material und Veröffentlichungsdateien und veröffentlicht alle drei Fassungen gemeinsam. Import-/Exporttests und Gesamtsuiten gehören nicht zu diesem Workflow. Der bestehende Workflow „Reinigungsfall Pages“ bleibt für seinen bisherigen Prüfumfang erhalten. Die [Projektstartseite](https://h4r7w16.github.io/ium-lernwerk/) führt zur aktuellen Lernfassung; die ältere direkte Adresse bleibt erhalten.

## Hintergrund: bisherige Entwicklungsstände

Die folgenden Abschnitte dokumentieren frühere Module und technische Grundlagen. Bezeichnungen wie `IUM-5-CORE-05`, „Gate B“ und „Pages-Fixture“ gehören zu diesen Entwicklungsständen. Für die aktuelle Reinigungsroboter-Vorschau gelten die Beschreibung und Links oben.

## Phase 2: erstes Lernmodul im Arbeitsstand

`IUM-5-CORE-05 – Präzise Abläufe ausführbar machen` ist als erstes vollständiges digitales Lernmodul lokal implementiert und bleibt ein **interner Arbeitsstand**. Es verbindet einen geschlossenen grafischen Algorithmuseditor mit Vorhersage, deterministischer Ausführung, Laufspur, begründeter Reparatur, fester Wiederholung, Transfer und Selbstcheck. Sein Status ist ausdrücklich `working`: Es ist **nicht für Unterrichtseinsatz** freigegeben, nicht im derzeitigen öffentlichen Pages-Fixture enthalten und noch nicht durch die reale Gate-B-Prüfung pilotiert. Reale Geräte- und Schulnetzprüfung bleibt `device-verified: not-run`.

- [Freigegebene Modulspezifikation](docs/superpowers/specs/2026-08-03-ium-5-core-05-moduldesign.md)
- [Testgetriebener Implementierungsplan](docs/superpowers/plans/2026-08-03-ium-5-core-05-implementation.md)
- [Modulbetrieb und Datengrenzen](docs/modules/ium-5-core-05.md)
- [Digitales Lehrkräftehandbuch](modules/IUM-5-CORE-05/handbuch/lehrkraeftehandbuch.md)

Die vollständige lokale Gate-A-Prüfkette startet mit `npm run verify:ium5`. Ein grüner Lauf schließt Gate B nicht und ersetzt weder Pilotierung noch reale Geräteprüfung.

### Implementiertes Gate-B-Paket - nicht ausgeführt

Das Repository enthält nun den technischen und fachlich-didaktischen Gate-B-Vertrag, geschlossene Evidenzschemas, sechs synthetische Beispiele, einen manuellen Previewworkflow, Leitfäden und einen begründeten analogen Beobachtungsbogen. Diese Implementierung ist **keine Ausführungsfreigabe**: Der Previewworkflow wurde nicht gestartet, reale technische Evidenz wurde nicht erhoben und keine Pilotierung oder LMS-Nutzung fand statt.

```powershell
python -B scripts/validate_ium5_gate_b.py protocol
python -B scripts/validate_ium5_gate_b.py synthetic
$env:IUM_BUILD_REVISION='1111111111111111111111111111111111111111'
$env:IUM_PREVIEW_ID='ium5-gate-b-test-0001'
npm run build:gate-b-preview
npm run verify:ium5:gate-b
Remove-Item Env:IUM_BUILD_REVISION
Remove-Item Env:IUM_PREVIEW_ID
```

Der lokale Previewbuild liegt unter `/ium-lernwerk/` und trägt auf jeder HTML-Seite `noindex`, SHA, Preview-ID, `working`, `not-run` und den dauerhaften Nichtfreigabebanner. Der separate Workflow `.github/workflows/ium5-gate-b-preview.yml` ist ausschließlich manuell, auf `main` und nach expliziter Nichtfreigabebestätigung startbar. Eine daraus entstehende Pages-URL wäre öffentlich; der Link ist keine Zugriffskontrolle. Dieser Implementierungsstand autorisiert keinen Workflowstart.

Reale Evidenzpakete und Rohbelege bleiben außerhalb von Git, GitHub-Artefakten und diesem öffentlichen Repository. Bei einer später gesondert autorisierten Rücknahme wird die Prüffassung deaktiviert; falls weiterhin ein HTTPS-Technikpfad benötigt wird, darf nur nach eigener Entscheidung wieder das synthetische `device-fixture-pages.yml` veröffentlicht werden.

- [Gate-B-Protokoll](pilot/ium5-gate-b/protocol.json)
- [Technisches Runbook](pilot/ium5-gate-b/docs/technical-runbook.md)
- [Pilotleitfaden](pilot/ium5-gate-b/docs/pilot-guide.md)
- [Reviewleitfaden](pilot/ium5-gate-b/docs/review-guide.md)
- [Analoger Beobachtungsbogen](pilot/ium5-gate-b/print/observation-sheet.html)

Spätere Entscheidungen bleiben getrennt: technischer Eintritt, explorativer Pilot, Bestätigung mit anderer Lerngruppe, reale LMS-Route und erst danach eine mögliche `working`-Freigabeprüfung. Keine davon ändert automatisch Modulstatus oder Gerätestatus.

## Phase 1: implementiertes Plattformfundament

Das freigegebene Plattformfundament ist als contract-first, Local-First und offline-fähige statische Webanwendung implementiert. Der frühere production-empty-Build war der Phase-1-Ausgangsstand; der strikt getrennte synthetische Fixture-Build macht die allgemeinen Daten-, Browser- und Offlineflüsse weiterhin prüfbar. Die automatisierte Aussagegrenze des Fundaments ist `implemented`. Reale Geräte- und Schulnetzprüfung bleibt `device-verified: not-run`.

- [Freigegebene Spezifikation](docs/superpowers/specs/2026-08-03-ium-phase1-plattformfundament-design.md)
- [Umsetzungsplan](docs/superpowers/plans/2026-08-03-ium-phase1-plattformfundament-implementation.md)
- [Plattformbetrieb und Local-First-Datengrenzen](docs/platform/README.md)
- [Geräte- und Schulnetzprotokoll](docs/platform/device-verification.md)

Die vollständige automatisierte Prüfung startet mit `npm run verify:phase1`. CI ersetzt die reale Geräteprüfung nicht.

## Phase 0: validierte Grundlage

Phase 0 umfasst Forschungsbasis, Curriculumdaten, Fachprofil, Modulverträge, Coverageaudit und das IUM10-Zeitmodell. Das davon getrennte technische Plattformfundament liegt in Phase 1.

Das IUM10-Zeitmodell hat den Status `working`. [roadmap/time-model.json](roadmap/time-model.json) ist die kanonische Quelle mit Schema 3; [roadmap/module-roadmap.md](roadmap/module-roadmap.md) ist die daraus abgeleitete Lesefassung. Die vollständigen Jahresvarianten und Referenzrechnungen sind daraus projiziert:

### Zeitmodell in Zahlen

| Klasse | Verfügbare Pfade (UE) | Bedarf ohne Angebot (UE) | Zeiturteil |
| --- | --- | --- | --- |
| 5 | 30/34/38 | — | green |
| 6 | 30/34/38/38/38 | — | green |
| 7 | — | 46/54 | amber |

Die drei 38-UE-Pfade der Klasse 6 bilden unterschiedliche Erweiterungen ab. Für Klasse 7 ist `GRADE-7-WORKING-40` ein `working`-Arbeitsziel mit `conditional`-Verfügbarkeit und `amber`-Zeitmachbarkeit; die 46- und 54-UE-Pfade sind `unavailable`/`red` und ausschließlich Referenzrechnungen, keine Ersatzangebote.

Status: **Auftraggeber-Zeitfreigabe ausstehend**. `working` ist der Status der 40-UE-Jahresvariante und bedeutet weder `available` noch `reviewed` oder zeitlich freigegeben. Die fünf Urteilachsen werden in dieser Reihenfolge ausgewiesen: Verfügbarkeit, Zeitmachbarkeit, Sequenznachweis, Pilotstatus, semantische Coverage.

- Klasse 5: available / green / covered / not-started / partial
- Klasse 6: available / green / covered / not-started / covered
- Klasse 7: conditional / amber / covered / not-started / partial

Klasse 7 bleibt nur unter dem Working-40-Vertrag bedingt: fünf Gates (`capacity`, `integration`, `technical`, `privacy`, `pilot`) sowie vier Integrationspiloten und ein Jahrespfadpilot sind noch nicht abgeschlossen. Ein gescheitertes erforderliches Gate führt fail-closed zu `unavailable`/`red`. Die additive Rückfallrechnung lautet `40 + 3 + 2 + 3 + 6 = 54`; 38 UE sind lediglich eine nichtnormative Vergleichsgrenze, keine Klasse-7-Jahresvariante.

Die 36 privacy-sicheren Pilotaufträge bleiben aggregiert: 31 Modulaufträge, vier Integrationsaufträge und ein Jahrespfadauftrag. Private Reflexion, persönliche Telemetrie und Schülerprodukte als Zeitnachweis sind ausgeschlossen; `handoffProductPresent` ist nur ein aggregierter Ja/Nein-Befund und allein kein positiver Zeitnachweis.

Die übrigen IUM10-Achsen bleiben ebenfalls getrennt beurteilt:

- aktuelle IUM10-Coverage: 166 `covered` / 5 `partial`;
- historische IUM09-Projektion: 164 `covered` / 7 `partial`;
- 60/60 Zeitreviews und 4/4 Sequenznachweise sind dokumentiert;
- Pilotaufträge bleiben auf Modul-, Integrations- oder Jahrespfadebene aggregiert und nichtpersonal, ohne persönliche Diagnostik oder Telemetrie.

In der historischen IUM09-Projektion gilt weiterhin: 164 sind auf Kandidatenebene `covered`, 7 bleiben `partial`. Von 60 Ausgangslücken wurden 53 geschlossen; 7 bleiben im Ledger offen. Trotz der verbesserten semantischen Coverage ist das Lernwerk weiterhin zeitlich nicht freigegeben.

Flexible Vertiefungs-, Transfer- und Projektmodule bleiben zusätzlich außerhalb der 40 UE sichtbar und ersetzen weder fehlende Kernzeit noch gescheiterte Kernintegrationen. Digital ist das selbstverständliche Unterrichtsmedium; analoge Materialien werden nur eingesetzt, wenn die Lernhandlung ihre Verwendung didaktisch begründet. Eine zwanghafte Doppelstruktur ist nicht vorgesehen.

## IUM11-Pilotinstrument

<!-- IUM11-PUBLICATION-CONTRACT:START -->
<!-- Generiert aus Pilotprotokoll und Zeitmodell; nicht manuell bearbeiten. -->
| Bereich | Verbindliche Fakten |
| --- | --- |
| Vertragsbindung | schemaVersion: 1; id: IUM11-PUBLICATION-CONTRACT; contractVersion: 1.0.0; protocolPath: pilot/pilot-protocol.json; timeModelPath: roadmap/time-model.json; protocolVersion: 1.0.0; toolVersion: 1.0.0; timeModelFingerprintAlgorithm: sha256-canonical-json-v1; timeModelFingerprint: 873774e52b6c9a20e08e5079c898a014493a39305be5efa35a601248ff36a2c1 |
| Kernpfad | variantId: GRADE-7-WORKING-40; targetUnits: 40; clusterCount: 4; moduleCount: 10; pilotStageCount: 5 |
| Clusterbudgets und Rückfälle | id: CLUSTER-7-DATA-CODING; order: 1; budgetUnits: 8; fallbackDeltaUnits: 3; id: CLUSTER-7-PROGRAMMING; order: 2; budgetUnits: 11; fallbackDeltaUnits: 2; id: CLUSTER-7-NET-SECURITY; order: 3; budgetUnits: 11; fallbackDeltaUnits: 3; id: CLUSTER-7-DATA-MEDIA-SOCIETY; order: 4; budgetUnits: 10; fallbackDeltaUnits: 6 |
| Privacygrenze | minimumLearnerResponses: 10; personalDataAllowed: false; realPackagesInRepositoryAllowed: false |
| Aktuelle Urteilachsen | status: working; availabilityStatus: conditional; timeFeasibilityStatus: amber; sequenceEvidenceStatus: covered; pilotStatus: not-started; semanticCoverageStatus: partial |
| Aussagegrenze | statementBoundary: documented-conditions-only |
| Zulässige Empfehlung | allowedRecommendation: eligible-for-working-availability-review |
| Gesperrte Reifegrade | forbiddenMaturityValues: reviewed; forbiddenMaturityValues: standard |
| Spätere Auftraggeberentscheidung | requiresCommissionerDecision: true; secondIndependentAnnualRunRequiredForMaturity: true; allowedChanges: availabilityStatus: available; allowedChanges: timeFeasibilityStatus: green; allowedChanges: pilotStatus: completed; unchangedAxes: status: working; unchangedAxes: semanticCoverageStatus: partial |
| Reale Pilotierung | realPilotCompleted: false; syntheticValidationOnly: true |
| Flexible Module | flexibleModulesOutsideCorePreserved: true; flexibleModuleSubstitution: forbidden; Flexible Vertiefungs-, Transfer- und Projektmodule bleiben sichtbar erhalten. |
<!-- IUM11-PUBLICATION-CONTRACT:END -->

IUM11 veröffentlicht ein lokales, privacy-sicheres Entwicklungsinstrument für den Klasse-7-Kernpfad. Die verbindlichen, automatisch erzeugten Fakten stehen im vorstehenden Faktenblock. Das Instrument und seine Beispiele sind synthetisch geprüft; dies ist keine reale Pilotierung und keine Statushochsetzung.

- [Pilotprotokoll](pilot/pilot-protocol.json)
- [Lokales Offline-Cockpit](pilot/cockpit/index.html)
- [Lehrkräfteanleitung](pilot/docs/teacher-guide.md)
- [Reviewanleitung](pilot/docs/review-guide.md)
- [IUM11-Validator](scripts/validate_ium11.py)

Das Cockpit wird direkt lokal geöffnet, verarbeitet nur Klassenaggregate im Arbeitsspeicher und speichert erst durch einen bewussten JSON-Download. Kleine Gruppen werden unterdrückt und exportieren keine Lernendenzählwerte. Reale Evidenz- und Entscheidungspakete bleiben außerhalb dieses öffentlichen Repositorys. Die verbindlichen Urteilachsen werden nicht durch das Instrument verändert.

<!-- IUM11-PUBLICATION-SCOPE:END -->

## Zentrale Einstiege

- [Validierte Modulroadmap](roadmap/module-roadmap.md)
- [Autoritatives IUM10-Zeitmodell](roadmap/time-model.json)
- [Recordgenauer Abdeckungsplan](roadmap/coverage-plan.json)
- [IUM10-Validator](scripts/validate_ium10.py)
- [IUM09-Validator](scripts/validate_ium09.py)
- [Gesamtvalidator Phase 0](scripts/validate_phase0.py)
- [Fachprofil Gymnasium 5–7](docs/fachprofil/ium-gymnasium-5-7.md)
- [Curriculum-Crosswalk](curriculum/crosswalk.json) und [begründete Progression](curriculum/progression.md)
- [Forschungsarchitektur](docs/research/phase-0/README.md) und [Forschungssynthese](docs/research/phase-0/synthesis.md)
- [Verbindliche Gesamtspezifikation](docs/superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md)

IUM10 ist nicht `reviewed`; eine Zeitfreigabe ist nicht erteilt. Die Implementierung des Phase-1-Plattformfundaments ändert diese inhaltliche und zeitliche Statusgrenze nicht.

## Validierung

```powershell
python -B -m unittest discover -s tests -p "test_*.py"
python -B scripts/build_ium11_cockpit.py --check
node --check pilot/cockpit/assets/app.js
python -B scripts/build_ium11_publication_contract.py --check
python -B scripts/validate_ium11.py
python -B scripts/validate_ium10.py
python -B scripts/validate_ium09.py
python -B scripts/validate_phase0.py
```

## Lizenzen

Eigener Validierungscode steht unter der [MIT-Lizenz](LICENSE). Eigene inhaltliche Repository-Beiträge stehen unter [CC BY-SA 4.0](LICENSE-CONTENT.md), sofern eine Datei nicht ausdrücklich etwas anderes festlegt. Material Dritter behält seine jeweils ausgewiesene Lizenz.
