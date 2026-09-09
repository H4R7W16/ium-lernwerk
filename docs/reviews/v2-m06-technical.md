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
| F08 Toolchain/Zielbrowser | CI ist auf Node 22.23.2/npm 10.9.8 und drei Browserprojekte festgelegt. Chromium und WebKit führen den Kernpfad aus. | Firefox scheitert lokal vor der Seite im Runner; reale Browser-/Geräteprofile offen. |

## TECH-01–11

| ID | Ergebnis | Beleg / verbleibender Punkt |
| --- | --- | --- |
| TECH-01 | synthetisch behoben | V2-Registry, Modul-ID, Version 0.1.0, Materialrevision und 225 Minuten sind buildgebunden; V1-/Fixture-Isolation geprüft. |
| TECH-02 | synthetisch behoben | S0–S3-Fachkern und fünfteiliger S3-Körper sind in Plattform- und Browserprüfungen gebunden. |
| TECH-03 | synthetisch behoben | Leeres Programm scheitert; Referenzprogramm liefert zehn Spurzeilen mit Befehls-ID, Durchlauf und Zustandsübergang. |
| TECH-04 | teilweise synthetisch behoben | Versions-/Schemafehler werden abgewiesen; die globale Speicheraktion übernimmt eine nur im Formular eingetragene P3-Begründung nicht in das Dossier, und die UI-Hydration nach Wiederöffnung bleibt als `IMP08-F01` offen. |
| TECH-05 | synthetisch behoben | Pending-Import wird bei Fehler, Abbruch und Löschung entwertet. |
| TECH-06 | synthetisch behoben | Zwei Seiten zeigen Konflikt; Löschung verhindert Wiederbelebung. Reale Profiltrennung offen. |
| TECH-07 | teilweise synthetisch behoben | P0/P4 sind nicht Teil des Dossiervertrags. Der Browsergegencheck bleibt bis zur P3-Hydrationskorrektur offen. |
| TECH-08 | teilweise synthetisch behoben | Offlinecache und Updatevertrag bestehen; sichtbare Wiederaufnahme des P3-Felds scheitert an `IMP08-F01`. |
| TECH-09 | teilweise synthetisch behoben | Axe, Tastatur, Touch und Reflow bestehen in Chromium. Sechs `summary`-Ziele unterschreiten 44 px Höhe (`IMP08-F02`); assistive Realprüfung offen. |
| TECH-10 | synthetisch ohne Drittressourcen | Build und Browserlauf laden keine Drittressourcen; Betreiber-, Hosting-, LMS- und Rechteentscheidung offen. |
| TECH-11 | teilweise synthetisch behoben | Rückkehrnotiz und Speicherstatus sind vorhanden; sichtbarer P3-Wiedereinstieg bleibt mit `IMP08-F01` offen. |

## Offene reproduzierte Befunde

### IMP08-F01 – P3-Begründung ist nicht an globales Speichern und Wiederöffnung gebunden

Wenn die „Begründung der Prüffahrt“ ausgefüllt und anschließend nur die globale Speicheraktion ausgelöst wird, wird der neue Text nicht in das Dossier übernommen. Nach Reload bleibt das Feld leer. Betroffen sind direkter Wiedereinstieg, Exportbeleg, Offlinewiederaufnahme und die sichtbare Kontrolle eines geschützten Stands. Der angenommene IMP07-Produktcode wird in IMP08 nicht stillschweigend verändert.

### IMP08-F02 – sechs Details-Ziele unter 44 px

Die `summary`-Elemente für Beispiel, H1–H4 und Datenverwaltung messen im Chromium-Desktoplauf rund 24,8 px Höhe. Tastatur-, Touch- und Reflowpfad funktionieren, das festgelegte 44-px-Ziel ist dennoch nicht erfüllt.

### IMP08-F03 – Firefox-Runner öffnet keine Seite

Alle 18 Firefox-Fälle der M06-Matrix scheitern lokal vor Produktnavigation mit `browserContext.newPage: Cannot read properties of undefined (reading '_page')`. Chromium und WebKit bestehen die vier Kernfälle. Das ist als Runner-/Umgebungsbefund dokumentiert und kein Firefox-Produktpass.

### IMP08-F04 – bestehender Astro-Typbefund

`npm run check:astro` scheitert weiterhin in `apps/lernwerk-portal/src/sw.ts:94`, weil `message.values` optional typisiert ist. IMP08 ändert den bereits angenommenen Produktcode nicht. Reale Builds und TypeScript-Projektprüfung werden getrennt berichtet.

### IMP08-F05 – WebKit-Offlinewiederöffnung bricht im Runner ab

Der WebKit-Fall zur persistenten Offlinewiederöffnung erreicht beim Reload einen internen Browserfehler (`page.reload: WebKit encountered an internal error`). Die übrigen beiden WebKit-Offlinefälle bestehen. Der Befund wird getrennt von `IMP08-F01` geführt, weil der Runner vor der fachlichen Wiedereinstiegsassertion abbricht.

### IMP08-F06 – bestehender CI-Vertrag erwartet weiterhin vier Jobs

Der vollständige Plattformlauf zählt 207 bestandene und einen fehlgeschlagenen Test. `tests/platform/documentation.test.ts` erwartet weiterhin exakt die vier bisherigen CI-Jobs und Node 22.20.0; der angenommene IMP08-Plan ergänzt dagegen den fünften Job `v2-m06` und pinnt Node 22.23.2. Die Testdatei gehört nicht zum autorisierten IMP08-Dateisatz und wird daher nicht außerhalb des Plans angepasst.

### IMP08-F07 – V2-Auditdigest ist nach Runtime-Implementierung veraltet

`npm run verify:v2` meldet `AUD Review veraltet: packages/module-runtime/src/runtime.ts`. Der Entwicklungsvalidator akzeptiert dagegen IMP01–IMP08 und bestätigt die geschlossenen Grenzen. Das historische Audit wurde nach den angenommenen Runtime-Änderungen nicht neu versiegelt und gehört nicht zum IMP08-Dateisatz.

### IMP08-F08 – lokale Lizenz-SBOM scheitert unter abweichender Toolchain

`npm run quality:licenses` scheitert lokal unter Node 24.11.0/npm 11.6.1 mit `ESBOMPROBLEMS`, weil optionale `@emnapi`-Pakete im installierten Baum fehlen. Der neue CI-Job pinnt Node 22.23.2/npm 10.9.8; ein erfolgreicher Lauf dieser Zieltoolchain liegt lokal nicht vor und darf erst durch CI belegt werden.

### IMP08-F09 – ältere Implementierungsfixtures erwarten weiterhin nur IMP01

Der vollständige Pythonlauf besteht 1021 von 1028 Tests. Vier der sieben roten Fälle liegen in `tests/test_validate_v2_implementation.py`: Die Test-Fixtures erwarten nur IMP01 als autorisiertes Paket beziehungsweise verändern den inzwischen abgenommenen Kandidaten ohne passende Abnahme. Drei weitere Fälle sind dieselbe Ursache wie `IMP08-F07`. Der nachgelagerte Dashboardlauf besteht 40 von 41 Tests; auch dort erwartet eine Snapshot-Fixture nur IMP01. Beide Alt-Testdateien gehören nicht zum autorisierten IMP08-Dateisatz.

## Gesamtergebnis des Orchestrators

`npm run verify:v2:m06` hat alle 18 Schritte ausgeführt und 8 bestanden sowie 10 mit Exitcode 1 protokolliert. Bestanden sind Vertragsgenerierung, Workspace-Grenzen, TypeScript, Entwicklungsvalidator, V2-Registry, Materialvertrag und beide V2-Buildprofile. Rot sind Astro, Plattform, Python, V2-Baseline, die vier Browsergruppen, Lizenz-SBOM und die wegen Astro früh abbrechende V1-Integration. Der Browser-Entrypoint startet und stoppt den Root-Preview selbstständig; der Kontrolllauf endet ohne hängenden Server mit 8 bestandenen Chromium-/WebKit-Kernfällen und 4 Firefox-Runnerfehlern.

## Toolchain und CI

CI pinnt Node 22.23.2 und npm 10.9.8, gibt beide Versionen aus und behält die bestehenden Jobs. Ein additiver V2-M06-Job führt V2-Baseline, Entwicklungsvalidator, Root-/Subpath-Build, Chromium/Firefox/WebKit und den Orchestrator aus. Vorprüfungen zeichnen ihren Status mit `continue-on-error` auf; der abschließende Orchestrator bestimmt den Jobstatus und der Evidenz-Upload läuft immer. Der lokale Lauf verwendet Node 24.11.0/npm 11.6.1 und ist deshalb kein Nachweis für den gepinnten CI-Runner.
