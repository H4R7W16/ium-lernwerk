# Klasse 6 ergänzend auf GitHub Pages

## Auftrag und Integrationspunkt
Veröffentlichung des geprüften M01–M07-Jahrgangs auf ausdrücklichen Nutzerauftrag vom 23.10.2026. Inhaltsstand `5e09c0d182076069e4af3d2acf824fdb2bde4fa7`; bisheriger Pages-Stand `90e875534ed275037b1b68dae50da08d2442fc4f`.

## Erhaltung und Ausgabe
`node prototypes/pages/build.cjs` führt den bisherigen Klasse5-/Recherche-Build mit den Klasse6-Ausgaben zusammen. Die 812 bisherigen Dateien einschließlich Wurzeleinstieg müssen mit `prototypes/pages/bestand-sha256.json` übereinstimmen. Abweichungen, zusätzliche alte Pfade, interne Dateien und unerreichbare lokale HTML-Verweise brechen den Build ab. Neue öffentliche Dateien liegen ausschließlich unter `klasse6/`.

Der bisherige gemeinsame Workflow `.github/workflows/klasse5-pages.yml` bleibt der einzige aktive Pages-Deployweg. Er prüft und veröffentlicht das gemeinsame Artefakt; dessen Verzeichnisname `dist/klasse5-pages` bleibt als technischer Vertrag erhalten. Die öffentliche Seite wird um `/klasse6/` mit 254 Dateien ergänzt. Alle 254 stimmen mit der Endausgabe des Jahrgangsreviews überein; insgesamt 1.066 öffentliche Dateien.

## Prüfung und Grenzen
Die drei neuen Veröffentlichungstests prüfen vollständigen Bestandsschutz, alle sieben Reihen samt Jahresplanung und die eigenen Manifest-/Speicher-/Offlinepfade. Der Workflow prüft zusätzlich die vorhandenen gemeinsamen Inhaltstests sowie die Netz- und Zeichenwerkzeuge. Der TypeScript-Workflowvertrag wird ebenfalls mitgeführt. Vor Integration sämtliche bisherigen Dateien öffentlich per HTTP/SHA256 vergleichen; nach Deployment das komplette Artefakt erneut öffentlich vergleichen und die tatsächlichen Zugänge im Browser prüfen.

Die bestehenden Inhaltsreviews bleiben gültig. Der Jahrgangsreview ist ein Selbstreview mit 22 Kriterien; die Publikation ergänzt keinen Nachweis realer Schulgeräte, verfügbarer 38 Jahres-UE oder Unterrichtserprobung. Veröffentlichungsergebnis und endgültiger Merge-/Deploy-Stand werden im Projekt-Handoff dokumentiert.
