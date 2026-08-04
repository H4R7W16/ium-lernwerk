---
moduleId: IUM-5-CORE-05
status: working
gateB: closed
device-verified: not-run
reviews:
  - path: ../reviews/ium-5-core-05-fach-didaktik.md
    verdict: APPROVED
    reviewedCommit: 4c26698590869b51e8d272cb4ddaf4920455d180
  - path: ../reviews/ium-5-core-05-engineering-accessibility-privacy.md
    verdict: APPROVED
    reviewedCommit: 4c26698590869b51e8d272cb4ddaf4920455d180
verification:
  command: npm run verify:ium5
  verifiedAt: 2026-08-03
  successfulSteps: 24
  totalSteps: 24
---

# IUM-5-CORE-05: Betrieb des Arbeitsstands

`IUM-5-CORE-05 – Präzise Abläufe ausführbar machen` ist das erste vollständig implementierte Lernmodul des Lernwerks. Der Stand ist `working` und **nicht für Unterrichtseinsatz** freigegeben. Die automatisierte Gate-A-Prüfung belegt technische und vertragliche Eigenschaften; Gate B bleibt bis zu den vorgesehenen unabhängigen Reviews, Realgeräteprüfungen und Pilotbefunden geschlossen.

## Lokal starten

```powershell
npm ci
npm run build
npm run preview:ium5
```

Der Previewserver stellt den Produktionsbuild lokal unter `http://localhost:4322/module/ium-5-core-05/` bereit. Er ist kein Deployment. Der öffentliche Pages-Workflow bleibt ausschließlich dem synthetischen Fixture vorbehalten.

## Lernpfade

Der reguläre Pfad umfasst fünf Unterrichtseinheiten: präzise Anweisungen klären, einen Algorithmus aufbauen und vorhersagen, kontrolliert ausführen und per Laufspur belegen, eine Abweichung diagnostizieren und reparieren sowie den Algorithmusbegriff auf andere Systeme übertragen. Die optionale sechste Unterrichtseinheit vertieft feste Wiederholungen und deren Modellgrenzen. Sie ersetzt keinen Bestandteil des Kernpfads.

Die Werkstatt nutzt geschlossene Befehlsblöcke, einen deterministischen Interpreter und zehn geprüfte Szenarien. Lernende erstellen als zusammenhängendes Produkt einen ausführbaren Algorithmus mit Vorhersage, Belegspur, reparierter Fassung, begründeter Schleifenentscheidung, Transferklassifikationen und Selbstcheck.

## Lokaler Arbeitsstand und Datenschutzgrenze

Erst die bestätigte lokale Speicherung legt einen Arbeitsstand im Browserprofil ab. Der persistente Payload enthält exakt:

- `phaseId`, `scenarioId`, `initialAlgorithm` und `prediction`;
- `evidenceTrace`, `repairSource`, `repairHypothesis` und `revisedAlgorithm`;
- `loopDecision`, `systemClassifications` und `selfCheck`.

Ausführungs-Cursor, Klicks, Versuchszahlen, Zeiten, Hilfenutzung, Fokus, Navigation und sonstige Sitzungsdaten bleiben flüchtige Nichtdaten. Es gibt kein Konto, keine Serverdiagnostik und keine personenbezogene Telemetrie.

„Arbeitsstand exportieren“ erzeugt nach bewusster Aktion eine lokale JSON-Datei. Sie kann Freitext und Lernprodukte enthalten und ist deshalb als sensibel zu behandeln. Ein Import wird zunächst formal und modulspezifisch geprüft und erst nach Bestätigung übernommen. „Arbeitsstand löschen“ entfernt den Zustand dieses Moduls nach Rückfrage aus dem aktiven Browserprofil. Die globale Plattformlöschung bleibt zusätzlich verfügbar.

## Offline und Aktualisierung

Nach einem vollständigen Online-Aufruf ist der Kernpfad einschließlich Roboterasset offline nutzbar. Ein erster Aufruf ohne vorherige Installation kann nicht offline funktionieren. Neue Versionen aktivieren sich erst nach „Speichern und aktualisieren“; davor wird der aktive Modulzustand geflusht. Fehlt einem Kandidaten ein Precache-Asset, wird er verworfen und die bisherige funktionsfähige Version bleibt aktiv.

## Barrierearme Bedienung

Alle Kernhandlungen sind ohne Drag-and-drop per Tastatur und beschrifteten Schaltflächen erreichbar. Szene und Laufspur besitzen textuelle Alternativen; Fehlermeldungen, Phasenwechsel und Arbeitsstandsaktionen führen den Fokus gezielt. Reflow bei 320 CSS-Pixeln, 200 Prozent Zoom, grobe Zeigereingabe und reduzierte Bewegung sind automatisiert abgesichert. Eine bestandene Automation ersetzt keine reale Prüfung mit VoiceOver, verwaltetem iPad oder schulischen Richtlinien; `device-verified: not-run` bleibt unverändert.

## Lizenzen

Eigene Lerninhalte und das geometrisch gezeichnete Roboter-SVG stehen unter CC BY-SA 4.0. Der modulspezifische Code steht unter MIT. Die Provenienz liegt in `modules/IUM-5-CORE-05/assets/licenses.json`; der Build führt das Asset zusätzlich in `asset-licenses.json`. Es werden keine externen Laufzeitressourcen geladen.

## Verifikation und Aussagegrenze

```powershell
npm run verify:ium5
```

Die fail-fast Kette prüft Verträge, Architekturgrenzen, Typen, Astro, Plattform, Builds und Lizenzen, Browser in Chromium/Firefox/WebKit, Zustand, Offlineverhalten, Accessibility sowie alle vorhandenen Legacy-Validatoren. Ein grüner Lauf belegt den reproduzierbaren `working`-Stand. Er ist weder eine Unterrichtsfreigabe noch ein Wirksamkeitsnachweis und schließt Gate B nicht.

## Gate-B-Paket und lokale Prüfung

Der Gate-B-Vertrag ist implementiert, aber nicht real ausgeführt. Protokoll und ausschließlich synthetische Beispiele lassen sich ohne Evidenzerhebung prüfen:

```powershell
python -B scripts/validate_ium5_gate_b.py protocol
python -B scripts/validate_ium5_gate_b.py synthetic
$env:IUM_BUILD_REVISION='1111111111111111111111111111111111111111'
$env:IUM_PREVIEW_ID='ium5-gate-b-test-0001'
npm run verify:ium5:gate-b
Remove-Item Env:IUM_BUILD_REVISION
Remove-Item Env:IUM_PREVIEW_ID
```

Der lokale Buildbefehl `npm run build:gate-b-preview` erzeugt die Produktionsvariante für `/ium-lernwerk/` mit Nichtfreigabebanner, `noindex`, vollständigem SHA, Preview-ID, `working` und `device-verified: not-run`. Ohne SHA und Preview-ID bricht er vor dem Build ab. Er fügt weder Telemetrie noch Gate-B-Speicherung hinzu und enthält nicht das synthetische Fixture-Modul.

## Publikations- und Evidenzgrenze

`.github/workflows/ium5-gate-b-preview.yml` beschreibt einen manuellen, bestätigungspflichtigen Pages-Pfad. Der Workflow wurde in diesem Implementierungsauftrag nicht gestartet. Eine spätere Pages-URL wäre öffentlich und keine Zugriffskontrolle; Kennzeichnung und `robots.txt` mindern Auffindbarkeit, ersetzen aber keine Autorisierung.

Reale technische und Pilot-Evidenz bleibt außerhalb des Repositories und außerhalb von GitHub-Artefakten. Im Repository liegen nur geschlossene Schemas und synthetische Pakete. Papieraggregate werden nach geprüfter Übertragung vernichtet; reale digitale Pakete sind spätestens 30 Tage nach der Entscheidung einschließlich temporärer Kopien zu löschen.

Falls eine später autorisierte Prüffassung zurückgenommen werden muss, wird sie deaktiviert oder durch einen ausdrücklich akzeptierten Stand ersetzt. Der vorhandene `device-fixture-pages.yml` bleibt semantisch unverändert und darf nur nach einer eigenen Entscheidung wieder den ausschließlich synthetischen Technikpfad bereitstellen.

## Getrennte nächste Entscheidungen

1. Technischer Eintritt anhand der realen Sechs-Zeilen-Matrix.
2. Explorative Pilotentscheidung für `regular-225`.
3. Bestätigungsentscheidung für `extended-270` mit anderer Lerngruppe.
4. Eigenständige Entscheidung über die reale LMS-Route.
5. Erst danach menschliche Entscheidung, ob der unveränderte Arbeitsstand einer `working`-Freigabeprüfung vorgelegt werden darf.

Kein Validator, Review oder Workflow setzt `status: working` oder `device-verified: not-run` automatisch hoch. Die einzige positive Gate-B-Empfehlung `eligible-for-working-release-review` ist keine Freigabe.

## Interne Reviewevidenz

| Review | Geprüfter Commit | Urteil |
| --- | --- | --- |
| [Fachlich-didaktischer Review](../reviews/ium-5-core-05-fach-didaktik.md) | `4c26698590869b51e8d272cb4ddaf4920455d180` | `APPROVED` |
| [Engineering, Accessibility, Privacy und Lizenzen](../reviews/ium-5-core-05-engineering-accessibility-privacy.md) | `4c26698590869b51e8d272cb4ddaf4920455d180` | `APPROVED` |

Letzter vollständiger Lauf auf dem geprüften Commit: `npm run verify:ium5`, 2026-08-03, 24/24 Schritte erfolgreich. Die Reviews geben den internen Gate-A-Handoff frei; sie verändern weder `working` noch `device-verified: not-run` und öffnen Gate B nicht.

### Gate-B-Implementierungsreviews

| Review | Geprüfter Commit | Urteil |
| --- | --- | --- |
| [Fachlich-didaktischer Gate-B-Review](../reviews/ium5-gate-b-fach-didaktik.md) | `2b4353d5d1a786d4d1ceddba71e3a7b2bdfe28d9` | `APPROVED AFTER FIXES` |
| [Engineering, Accessibility und Privacy](../reviews/ium5-gate-b-engineering-accessibility-privacy.md) | `2b4353d5d1a786d4d1ceddba71e3a7b2bdfe28d9` | `APPROVED AFTER FIXES` |

Die Urteile bestätigen ausschließlich die Implementierungsqualität des Gate-B-Pakets. Es wurde weder ein Preview veröffentlicht noch eine reale Geräteprüfung oder Pilotierung durchgeführt; `working` und `device-verified: not-run` bleiben unverändert.
