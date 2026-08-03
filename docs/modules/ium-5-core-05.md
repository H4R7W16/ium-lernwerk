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
