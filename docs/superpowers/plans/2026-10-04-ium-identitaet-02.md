# IuM-Identität 02 im Lernwerk – Umsetzungsplan

**Ziel:** Die gewählte Wortmarke 02 und eine gemeinsame Gestaltung in der aktuellen Klasse-5-Oberfläche umsetzen.
**Basis:** 6cfd63e; lokale Arbeitskopie auf feat/ium-identitaet-02.
**Gestaltungsreferenz:** Nutzerentscheidung für 02-mittig-fuellend.svg vom 04.10.2026: IuM links, Lernwerk mit mittigem zweizeiligem Fachnamen, große blaue 5 rechts.
**Architektur:** Bestehenden statischen Mantelgenerator verwenden. Kleine, gemeinsame Gestaltungsdatei zuletzt laden. Fachliche Inhalte, Datenformat, Reihenfolge und Arbeitsstände weiterverwenden.

## Verbindliche Gestaltung

- Segoe UI für Wortmarke und Oberfläche; System-Fallback. Technischer Code behält Monospace.
- Anthrazit #222A2F, Blau #2D52EE, Hintergrund #F7F7F2, Text sekundär #5B656D.
- Vollständige Wortmarke auf großen Bildschirmen; passende kompakte Fassung bei schmalen Breiten.
- Klasse 5 ist der tatsächliche verfügbare Jahrgang. Keine erfundenen Jahrgangszugänge.
- Aufgaben, Wissen, Materialien, Lehrpersonen- und Sicherungsfunktionen bleiben erreichbar.
- Keine Veröffentlichung und kein Eingriff in die gleichzeitig genutzte Produktarbeitskopie.
- Selbstreview im bestehenden Chat nach Repository-Regel; keine Subagenten.

## Umsetzung und Prüfung

- [x] Wortmarken unter prototypes/shared/brand übernehmen, gemeinsame Kopfzeile und Asset-Auslieferung in mantel-render.cjs anpassen.
- [x] Gemeinsame Farbtokens in mantel.css, learning-ui.css und algorithmus.css einsetzen; Gestaltungsregeln in identity.css ergänzen.
- [x] Startseite mit großer, zweistufiger Überschrift, klarem Themeneinstieg und realen Zugängen zu Arbeit und Lehrpersonen gestalten.
- [x] Manifest, App-Symbol und Offlinepaket an die Identität anschließen.
- [x] Bestehende Node-Prüfungen und vollständigen statischen Build ausführen. Relative Links und Offline-Assetliste prüfen.
- [x] Desktop und Mobilansicht, Themenmenü, Fachseite und Arbeitsübersicht im Browser sichten; aktuellen Selbstreview dokumentieren.

## Prüffokus

Responsive Kopfzeile bis 320 px, vorhandene Themenbilder, lange deutsche Bezeichnungen, Sichtbarkeit des Tastaturfokus, Erreichbarkeit der Wissens-/Materialseiten, Offline-Logo, Druckansicht.

Die Änderung ist Gestaltung und Assetintegration. Keine Tests ergänzen, die lediglich CSS oder Logo-Markup nachbilden; bestehende Funktionsprüfungen und Browserprüfung verwenden. Git-Änderungen bleiben zunächst zur Sichtung auf dem eigenen Branch.
