# IuM Lernwerkstatt
Eigenständige neue Prüffassung nach dem Feedback zu Lernfassung 3. Schwerpunkt: Schul-iPads; Route /lernwerkstatt/. Vorherige Versionen bleiben erhalten.

## Aufbau
- index.html, workshop.css, workshop.js: eigenständige Oberfläche ohne externe Bibliotheken oder Schriftabrufe.
- workshop-model.js: elf Stationen mit Auftrag, Erklärungen, gestuften Hilfen und Lösungen; Adapter über dem bestehenden Selbstlernmodell.
- Gemeinsame Simulationsgrundlage: ../m06-selbstlernen/model.js und cleaning-core.js.
- Die vollständige bestehende Lesefassung bleibt aus jeder Station erreichbar.
- Lernprodukte bleiben beim Stationswechsel in der Seite. Lokale Speicherung ist ausdrücklich optional und standardmäßig aus. Kein Dateiimport/-export in dieser Fassung.

## Gezielte Prüfung
node --test prototypes/m06-lernwerkstatt/workshop.test.cjs

Die manuelle Pages-Workflow-Prüfung umfasst zusätzlich nur die bisherigen Material-, Journey- und Pages-Tests. Keine Import-/Exporttests und keine Gesamtsuite ausführen.

## Abgrenzung
Diese Prüffassung ersetzt weder die Re-Baseline noch UX11/UX12-Freigaben. Browser- und Modellprüfung beweisen keine Lernwirkung. Reale Schul-iPad-/Safari-Erprobung und Nutzerabnahme stehen separat.
