# Phase 1: Plattformbetrieb

Dieses Handbuch beschreibt das implementierte Plattformfundament des IuM-Lernwerks. Es dokumentiert den technischen Betrieb, nicht die Freigabe realer Unterrichtsinhalte. Automatisierte Prüfungen und CI können den Status `implemented` belegen; `device-verified` erfordert reale Geräte- und Schulnetztests und bleibt bis dahin `not-run`.

## Buildvarianten und Start

Der Produktionsbuild ist bewusst **production-empty**: Er erzeugt Portal, Verträge und Laufzeit, enthält aber noch kein Lernmodul. Der Fixture-Build ergänzt ausschließlich das synthetische Referenzmodul aus `tests/fixtures/reference-module/`. Diese Trennung verhindert, dass Testinhalte als Unterrichtsmaterial erscheinen.

```powershell
npm ci
npm run build
npm run build:fixture
npm run preview:fixture
```

`npm run build` erzeugt die Produktionsvariante für `/`. `npm run build:fixture` erzeugt die lokale Referenzvariante für `/`. Mit `npm run build:fixture:subpath` wird dieselbe Referenzvariante für `/ium-lernwerk/` gebaut. Alle Laufzeitverweise bleiben innerhalb des konfigurierten Basispfads; ein Server muss die erzeugten statischen Dateien unter genau diesem Pfad ausliefern.

## Local-First-Datenvertrag

Die Plattform hat keine Konten, keine Serverdiagnostik und keine personenbezogene Telemetrie. Ein Modul kann zwei klar benannte Modi anbieten:

- **bestätigte Speicherung**: Der Browser speichert den Arbeitsstand erst nach bewusster Zustimmung lokal in IndexedDB.
- **flüchtige Sitzung**: Der Arbeitsstand bleibt nur im Arbeitsspeicher und endet mit Schließen oder Neuladen der Seite.

Der Export ist eine bewusst ausgelöste lokale JSON-Datei. Die Oberfläche kennzeichnet ihn als **sensiblen Export**, weil Lernprodukte oder Freitext enthalten sein können. Exportdateien dürfen nicht ungeprüft in öffentliche Repositories, Tickets oder Messenger gelangen. Der Import prüft Format und Schema, bevor er vorhandenen Zustand ersetzt.

„Daten global löschen“ löscht nach Bestätigung sämtliche vom Lernwerk gespeicherten Modulstände in diesem Browserprofil. Einzelne Modulstände können separat gelöscht werden. Browserdaten, die außerhalb des Lernwerks liegen, werden nicht berührt.

## Offline und kontrollierte Aktualisierung

Nach einem erfolgreichen Online-Aufruf werden Shell, lokale Assets, Offline-Hinweis und Fixture-Inhalte für den konfigurierten Pfad vorgehalten. Für den **ersten Offline-Aufruf** auf einem Gerät gilt: Ohne vorherigen Cache kann er nicht von der Anwendung beantwortet werden; dafür darf keine anwendungsseitige Fehlermeldung versprochen werden.

Ein neuer Service Worker aktiviert sich nicht ungefragt. Die Oberfläche meldet eine verfügbare Version und führt die **kontrollierte Aktualisierung** erst nach Zustimmung aus. Vor dem Wechsel fordert sie aktive Module zum Speichern beziehungsweise Flushen ihres Zustands auf. Schlägt Installation oder Aktivierung fehl, bleibt die bisherige funktionsfähige Version aktiv.

## Einbettung und Rückfall

Eine Einbettung in LMS oder andere Portale ist nur innerhalb der unterstützten Browser- und Sicherheitsrichtlinien vorgesehen. Blockiert eine Einbettung IndexedDB, Downloads, Service Worker oder Navigation, weist die Oberfläche auf die Einschränkung hin. Der fachlich gleichwertige Rückfall ist das Öffnen des Lernwerks in einem eigenen Tab; ein stiller Wechsel zu unsicherer Speicherung findet nicht statt.

## Lizenzen und externe Abhängigkeiten

Eigener Code steht unter MIT, eigene Inhalte unter CC BY-SA 4.0, sofern eine Datei nichts Abweichendes ausweist. `public/asset-licenses.json` dokumentiert die im Portal ausgelieferten Assets. `reports/phase1/dependency-sbom.cdx.json` und der Lizenzbericht werden bei der Qualitätsprüfung neu erzeugt und nicht versioniert. Der Kern lädt weder fremde Skripte noch Webfonts oder CDN-Ressourcen zur Laufzeit.

## Qualitätssicherung

Die vollständige, plattformunabhängige Prüfkette wird mit genau einem Befehl ausgeführt:

```powershell
npm run verify:phase1
```

Sie prüft nacheinander Verträge, Architekturgrenzen, Typen, Plattformtests, alle drei Builds, Build- und Lizenzqualität, Browserfluss in Chromium/Firefox/WebKit, Offlineverhalten, Barrierefreiheit, Python-Tests sowie die Validatoren von IUM11 bis Phase 0. Sie bricht beim ersten Fehler ab.

Für gezielte Entwicklung stehen zusätzlich diese Befehle bereit:

```powershell
npm run test:platform
npm run typecheck
npm run quality:build
npm run quality:licenses
npm run test:browser
npm run test:offline
npm run test:accessibility
npm run test:python
```

GitHub Actions teilt dieselben Gates in `legacy`, `contracts-build`, `browser` und `offline-quality`. Erfolgreiche CI bedeutet ausschließlich `implemented`. Sie ersetzt weder Prüfung auf einem verwalteten iPad noch Safari-, Schulnetz-, Filter-, MDM-, Web-Clip-, VoiceOver- oder LMS-Evidenz. Diese wird ausschließlich im [Geräteprotokoll](device-verification.md) dokumentiert.

## Temporärer HTTPS-Pfad für die Geräteprüfung

Der manuell gestartete Workflow `.github/workflows/device-fixture-pages.yml` veröffentlicht ausschließlich den synthetischen Fixture-Build unter `https://h4r7w16.github.io/ium-lernwerk/`. Er reagiert nicht auf normale Pushes und läuft nur auf `main`. Vor dem Upload prüft er Plattformverträge, Unterpfadbuild, Qualitätsbudgets und den vollständig injizierten Service Worker; Schreibrechte auf Pages und OIDC erhält ausschließlich der getrennte Deployjob.

Dieser Pfad ist ein technisches Prüfmittel für IUM14. Er enthält kein curriculares Lernmodul, keine realen Daten, keine Konten, keine Telemetrie und keine Drittanbieter-Laufzeitressourcen. Eine erfolgreiche Bereitstellung belegt nur einen erreichbaren HTTPS-Testkontext. `device-verified` bleibt bis zur dokumentierten realen iPad-, Policy-, Schulnetz- und LMS-Prüfung `not-run`.

## Statusgrenze

- Plattformfundament: `implemented`, sobald die vollständige automatisierte Prüfkette grün ist.
- Reale Geräteprüfung: `device-verified: not-run`, bis das Protokoll mit überprüfbarer Evidenz ausgefüllt wurde.
- Unterrichtliche Wirksamkeit und Pilotierung: nicht durch Phase 1 belegt.
