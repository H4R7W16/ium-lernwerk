# B17 · Führungsrevision R01–R03

09.11.2026 · Ausgang d4a5108557d29742d50e3e49c6c71624ff3bcc82 · feat/ium-lernbogen-pilot-20261107.
Ausdrücklich beauftragte Umsetzung des vorliegenden Reviews, Inline-Selbstreview. Klasse6, etwa11–12Jahre. Vorhandene Unterrichts-/Stufenprofile und Jahresplanung weiter gültig.

## Lernbewegung und Grenzen

Erkennen15 → Wirkung15 → Daten20 → Modell20 → B42-Datenfluss25 → eigene Werbekarte25 → Revision30 → neutraler/privater Bezug30 → Transfer/Sicherung30 =210Kernminuten. Vorab8M02-Minuten und später6+6 getrennt. Eigene Vorhersage → Start prüfen → genau einen früheren Besuch ändern → neue Vorhersage → prüfen → erklären/Grenze. Zettel/Liste oder Bildschirmhilfe, keine zweite Pflichtausführung. B42 und eigentliche Gestaltung bleiben selbstständige neue Produkte. Version2.0.0/Feldbestand unverändert.

## Konkrete Ausführung

R01: aktueller kurzer Phasenimpuls und Startknopf vor den Stationen; zweite Prüftaste direkt bei der Besuchswahl. Drei Stationen bleiben räumlich getrennt. Regeln kurz, vollständige Regel vor der Aufgabe direkt verlinkt.

R02: reine comparison(state)-Funktion liefert geprüften Start und erst nach CHECK_CHANGE den geprüften Eingriff. Eine Tabelle ersetzt beide Textkästen: K, V, für V gezählte Besuche; Spalten Start/nach Eingriff. Nachher-Spalte bis Endvergleich verborgen. Keine vorweggenommene Ursachenbegründung.

R03: Links zur vorhandenen Versuchsspur vor Bedienung und nach Vergleich, ein Rücklink nach dem vorhandenen Feld. Rückweg öffnet Hilfe und fokussiert phasengerecht Start, Besuchswahl, zweite Prüfung oder Ergebnis. Nach zweiter Prüfung Fokus auf Ergebnisüberschrift, Reset nachgeordnet. Kein neues Antwortfeld, keine Bestätigung als Kompetenznachweis. Mündlich/Heft weiter möglich. Modellreset verändert Antworten nicht.

Technisch kleine Änderungen in b17-model.js/css/render.cjs, begrenzter Rücklink in class5-content.cjs, bestehende B17-Tests ergänzen. Lehrhinweise/Briefing/Reihenkommentar mitführen. Neue additive Revisionsbindung für exakt geänderte Ausgaben; neue Quelldateien vor Hashbildung LF, Gitobjekt-Regel beachten. Kein neuer Medienasset oder Runtimebedarf.

## Umsetzung und Prüfung

- [x] Neue Tests rot: Ergebnissperre/alle Zweige, frühe Orientierung, eindeutige Rückwege/ein Antwortfeld/Papier unverändert.
- [x] UI, kompakter Vergleich und Fokus/Rückwege implementieren; Lehrhinweise synchron.
- [x] Gezielt/größer testen, frischer Gesamtbuild und Vorher-Nachher-Abgleich samt geschütztem Bestand.
- [x] Tatsächliche1280/390px-/Tastaturprobe, beide Zweige, Vorhersagewege/Notizschutz/Reset/B42; Wortmenge und Wege messen.
- [x] Ganzen Lernbogen selbst prüfen, Gewinne/Verluste und Grenzen dokumentieren, Fassungsreview/check/report, Fetch/Pull und lokaler Commit; Vorschau zeigen.
