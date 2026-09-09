# V2-M06 – technischer Integrationsreview

Stand: 9. September 2026. Gegenstand ist ausschließlich der lokale Entwicklungskandidat. Reale Zielgeräte, Schulnetz, LMS, Nutzung, Pilot und Veröffentlichung wurden nicht geprüft.

## Auditbefunde F01–F08

| Befund | Synthetischer Stand | Reale Grenze |
| --- | --- | --- |
| F01 Datenannahme | Load und Import verwenden denselben Modul-/Versions-/Payloadvertrag; Negativtests bestehen. | Zielprofil und reale Altstände nicht geprüft. |
| F02 Recovery | Unverändertes Original bleibt getrennt exportierbar; beschädigte Stände werden nicht aktiviert. | Downloadziel und Recoveryablage institutionell offen. |
| F03 Importtransaktion | Vorschau, Bestätigung, Abbruch und Löschung entwerten ausstehende Aktionen. | Browserdateidialoge auf Zielgeräten offen. |
| F04 Revision/Löschung | CAS und Löschgeneration verhindern stille Überschreibung und Wiederbelebung synthetisch. | Gemeinsame reale Browserprofile und Verantwortlichkeit offen. |
| F05 Speicher/Datenwege | Speicherwahl liegt vor Runtime; Export und Clipboard sind bewusste Handlungen. | Profilverwaltung, Quota, Sync und Löschfristen offen. |
| F06 Updates | Readback, flüchtiges Veto und Mehrclientkoordination sind synthetisch geprüft. | Reale Netz-/Policyunterbrechung offen. |
| F07 Modulbindung | Eigene V2-ID, Registry, Renderer, fünfteilige Schleife und Dossier sind gebunden. | Fachlich-didaktische Nutzerprüfung offen. |
| F08 Toolchain/Zielbrowser | CI und lokaler Abschlusslauf verwenden Node 22.23.2/npm 10.9.8. Chromium, Firefox und WebKit bestehen Workbench, Zustand, Accessibility und Offline. | Reale Browser-/Geräteprofile offen. |

## TECH-01–11

| ID | Ergebnis | Beleg / verbleibender Punkt |
| --- | --- | --- |
| TECH-01 | synthetisch behoben | V2-Registry, Modul-ID, Version 0.1.0, Materialrevision und 225 Minuten sind buildgebunden; V1-/Fixture-Isolation geprüft. |
| TECH-02 | synthetisch behoben | S0–S3-Fachkern und fünfteiliger S3-Körper sind in Plattform- und Browserprüfungen gebunden. |
| TECH-03 | synthetisch behoben | Leeres Programm scheitert; Referenzprogramm liefert zehn Spurzeilen mit Befehls-ID, Durchlauf und Zustandsübergang. |
| TECH-04 | synthetisch behoben | Versions-/Schemafehler werden abgewiesen; P3 wird nur aus einem laufgebundenen, geprüften Beleg übernommen und vollständig rehydriert. |
| TECH-05 | synthetisch behoben | Pending-Import wird bei Fehler, Abbruch und Löschung entwertet. |
| TECH-06 | synthetisch behoben | Zwei Seiten zeigen Konflikt; Löschung verhindert Wiederbelebung. Reale Profiltrennung offen. |
| TECH-07 | synthetisch behoben | P0/P4 bleiben flüchtig und fehlen im Dossiervertrag; gespeicherte P1–P3/P5/P6-Produkte bleiben getrennt erhalten. |
| TECH-08 | synthetisch behoben | Offlinecache, Updatevertrag und sichtbare Wiederaufnahme bestehen; WebKit-Windows öffnet Route und elf Materialien nach echtem Serverstopp. |
| TECH-09 | synthetisch behoben | Axe, Tastatur, Touch, Reflow und vollständiges 44-px-Zielinventar bestehen in Chromium, Firefox und WebKit; assistive Realprüfung bleibt offen. |
| TECH-10 | synthetisch ohne Drittressourcen | Build und Browserlauf laden keine Drittressourcen; Betreiber-, Hosting-, LMS- und Rechteentscheidung offen. |
| TECH-11 | synthetisch behoben | Rückkehrnotiz, Speicherstatus, Wiederaufnahme und bewusstes Abrufen vor dem Vergleich sind geprüft. |

## Aufgelöste reproduzierte Befunde

### IMP08-F01 – P3-Begründung ist nicht an globales Speichern und Wiederöffnung gebunden

NA01–NA03 binden P3 an Laufkennung, Vorhersage, Programm und Spurstellen. Export, Import, Reload und Offlinewiederaufnahme bestehen in der Drei-Browser-Matrix.

### IMP08-F02 – sechs Details-Ziele unter 44 px

NA05 korrigiert die M06-lokalen Zielgrößen. Das vollständige Inventar in Ausgangs-, Hilfe-, Abruf-, Diagramm-, Spur- und Verwaltungszuständen besteht mit mindestens 44 × 44 CSS-Pixeln.

### IMP08-F03 – Firefox-Runner öffnet keine Seite

Der Windows-Inhaltsprozess startet mit `MOZ_DISABLE_CONTENT_SANDBOX=1`; Linux-CI behält die Standardkonfiguration. Alle vorgesehenen Firefoxfälle bestehen.

### IMP08-F04 – bestehender Astro-Typbefund

Die Antwortwerte des Service Workers werden unmittelbar mit `Array.isArray` eingegrenzt. Astro prüft 27 Dateien ohne Fehler, Warnungen oder Hinweise.

### IMP08-F05 – WebKit-Offlinewiederöffnung bricht im Runner ab

Der defekte Playwright-Offlinetoggle wird unter Windows nicht als Produktnachweis verwendet. Ein eigener Test beendet den statischen Server und öffnet anschließend Route, Dossier und alle elf Material-/Briefingrouten aus dem Service-Worker-Cache.

### IMP08-F06 – bestehender CI-Vertrag erwartet weiterhin vier Jobs

CI und Plattformvertrag führen fünf Jobs und Node 22.23.2. Der V2-Job bindet Commit, Laufkennung und Ergebnisartefakt eindeutig und führt den Orchestrator auch nach einem fehlgeschlagenen Browser-Installationsschritt aus.

### IMP08-F07 – V2-Auditdigest ist nach Runtime-Implementierung veraltet

Der historische AUD-Befund bleibt unverändert sichtbar: `AUD Review veraltet: packages/module-runtime/src/runtime.ts`. Der Orchestrator prüft den versiegelten Aktivierungsstand deshalb mit `verify:v2:activation:historical` und den heutigen Stand separat mit `verify:v2:implementation`.

### IMP08-F08 – lokale Lizenz-SBOM scheitert unter abweichender Toolchain

Unter Node 22.23.2/npm 10.9.8 werden 645 im Repository installierte Pakete gegen den vollständigen Lockfile-SBOM mit 766 Komponenten geprüft. Fremde Codex-Laufzeitpakete außerhalb des Repositorys werden nicht als Projektabhängigkeiten gezählt; es bleiben keine ungültigen Lizenzen.

### IMP08-F09 – ältere Implementierungsfixtures erwarten weiterhin nur IMP01

Validator- und Dashboardfixtures bilden IMP01–IMP08 ab und behalten ihre Manipulationsprüfungen. 1.028 Python-Tests und 41 Dashboardtests bestehen.

## Historisches NA06-Ergebnis des Orchestrators

`npm run verify:v2:m06` hat alle 20 Schritte ausgeführt und bestanden. Enthalten sind 229 Plattformtests, zweimal der vollständige Pythonbestand mit je 1.028 Tests, 111 M06-Browserfälle in Chromium/Firefox/WebKit, acht Runtime- und zwei Updatefälle, beide V2-Buildprofile, SBOM/Lizenzen und die vollständige V1-Verifikation mit 24/24 Schritten. Die Laufgrenzen bleiben synthetischer Entwicklungskandidat, reale Geräte `not-run`, Nutzung und Pilot `not-started`, Curriculum `unassessed`, Veröffentlichung `closed`.

## Toolchain und CI

CI und lokaler Abschlusslauf pinnen Node 22.23.2/npm 10.9.8. Der additive V2-M06-Job führt den gesamten Orchestrator aus, auch wenn die Browserinstallation zuvor fehlschlägt, und lädt V2-, Phase-1- und Fehlerartefakte immer unter einem Namen aus Run-ID, Run-Attempt und Commit-SHA hoch. Der lokale Lauf `na06-local-final` ist in `reports/v2-m06/summary.json` protokolliert; ein externer CI-Lauf ist nicht behauptet.

## NA08 – Korrektur der NA07-Befunde F01–F05

Die folgenden Änderungen sind durch den Nutzerauftrag vom 09.09.2026 autorisiert. Die F-Nummern dieses Abschnitts gehören zum NA07-Schlussreview, nicht zum älteren FU-TECH-Audit oben.

- F01: `v2-m06` trägt `if: always()` auf Jobebene bei weiterhin vorhandenem `needs: contracts-build`. Damit kann auch ein fehlgeschlagener Vorgänger den Prüflauf nicht implizit überspringen. Der lokale Workflowvertrag prüft genau diese Voraussetzung; ein ausgeführter GitHub-CI-Lauf bleibt ein gesonderter Nachweis.
- F02: Jeder Orchestratorlauf besitzt ein neues Verzeichnis unter `reports/v2-m06/runs/`. Browsergruppen erhalten getrennte JSON-Einzelergebnisse und Artefakte. Kurze eindeutige Arbeitsverzeichnisse unter `reports/pw/` verhindern den reproduzierten Windows-Downloadabbruch bei zu langen Pfaden; nach Ende des Browserprozesses werden die Artefakte zusätzlich in der Gruppe archiviert. CI lädt beide Bereiche hoch. Die Integration prüft absichtlichen frühen Browserfehler, anschließenden Erfolg und bytegleichen Erhalt des früheren Traces.
- F03: Jeder erzeugte Build wird unmittelbar nach Service-Worker-Finalisierung als Dateibaum und SHA-256-Manifest archiviert. Manifest und Browsergruppe nennen Revision, Profil, Basispfad, Prüfschritt und konkreten Build. Die Digests entstehen aus lexikalisch sortierten relativen Pfaden und Dateihashes (UTF-8, LF, kein Schluss-LF; `.vite-cache` ausgeschlossen). `latest.json` ist nur ein Zeiger; frühere Läufe bleiben erhalten. Der zusätzliche Artefakttest erweitert den Orchestrator auf 21 Schritte. Aktuelle Zahlen und Buildhashes stehen nach abgeschlossenem Lauf in `roadmap/v2/implementation/evidence.json`.
- F04: Der Autorenreview ist anhand des angenommenen M06-Designs recordgenau und anhand des Materialmanifests materialgenau berichtigt. Alle Curriculumrecords bleiben `unassessed`.
- F05: Einfügen und Ändern einer Wiederholung prüfen eine ganze Anzahl 2–9 vor der Dossiermutation und melden ungültige Werte am Feld. Der Controller weist zusätzlich strukturell ungültige Programme zurück. Regressionen prüfen leere Eingabe, 1, 10 und Dezimalzahl, Speicherung/Export gültiger Nachbararbeit sowie Grenzen 2/9 und Korrektur mit Reload.

Der NA07-Gesamtlauf bleibt historisch 19/20 mit separat bestandenem Root-Build-Retry. Keine nachträgliche Umdeutung dieses Ergebnisses und keine Wiederverwendung des dort beanstandeten alten Hashs als neuer Buildnachweis.
