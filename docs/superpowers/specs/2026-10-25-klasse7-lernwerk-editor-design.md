# Lernwerk-Ansicht für Snap! · Klasse 7

## Auftrag und Entscheidungen

Jan möchte die Programmieroberfläche für das Lernwerk und Klasse 7 anpassen. Auf die Rückfrage nennt er alle drei Probleme: Funktionsfülle/Orientierung, kleine Bedienung und unpassende Gestaltung. Snap!, die 36 Jahres-UE und ALG-1 bis ALG-6 bleiben Grundlage. Die folgenden Details sind Umsetzungsvorschläge von Codex innerhalb dieses Auftrags, keine zusätzlich behaupteten Nutzerentscheidungen.

## Ansatz

Eine separate Lernwerk-Ansicht verwendet die unveränderte mitgelieferte Snap!-Laufzeit. Native Konfiguration übernimmt helles flaches Design, größere Blöcke und reduzierte Werkzeuge. Eine lokale HTML-Leiste ergänzt große beschriftete Aktionen, Kategorieauswahl und sichtbare echte Positionswerte. Die bisherige index.html bleibt bytegleich als technischer Rückweg.

Eine reine native Farb-/Größenkorrektur lässt kleine Menüaktionen und Orientierungsprobleme bestehen. Eine vollständige Neuprogrammierung des Blockeditors würde einen eigenen Editor samt Debugger und XML-Kompatibilität erfordern. Gewählt wird als begrenzte technische Umsetzung die zusätzliche Ansicht mit vorhandener Engine, ohne Abhängigkeiten oder geänderte Enginequellen.

## Verhalten

- Heller Lernwerk-Rahmen, Waldgrün, Systemschrift, native Blockfarben erhalten. Blöcke initial 145 Prozent, globaler Zoom 100 Prozent.
- Im Einstieg vier Kategorien: Bewegung, Aussehen, Steuerung und Operatoren. Alle zehn Projekte und insbesondere der Reparaturblock nicht bleiben abgedeckt. Mehr Werkzeuge öffnet die vollständige Palette und native Menüs ohne Reload oder Verlust des laufenden Projekts.
- Große HTML-Aktionen: Starten mit grüner Flagge, Pause/Fortsetzen, Stopp, Schrittmodus und Ein Schritt. Schrittmodus nutzt echte native Auswertung inklusive Unterausdrücken. Keine simulierte Schrittspur und keine Rückwärtsschritt-Behauptung. Lose Stapel aus ALG-1 werden weiterhin durch Antippen gestartet.
- Echte x-/y-Position und Richtung sichtbar. Keine Kompetenz-/Erledigtanzeige.
- Datei speichern als XML mit wählbarem Dateinamen und ehrlichem Hinweis Download angefordert. Lokales Öffnen validiert XML und fragt vor dem Verwerfen geänderter Arbeit. Vorhersagen oder Ergebnisse werden nicht automatisch gespeichert. Export bewahrt die ursprüngliche Palettensichtbarkeit; eigene Filter werden nicht im Projekt festgeschrieben.
- Aufgabenlinks öffnen die passende vorbereitete Datei; unbekannte/extern gerichtete Projektadressen werden abgelehnt. Originaldateien bleiben bytegleich.
- Bedienhilfe erklärt grüne Flagge versus Stapeltipp, Auswertungsschritte, Öffnen und Downloadkontrolle. Materialaufträge werden nicht gelöst oder umgeschrieben.

## Grenzen und Prüfung

Keine externe Schrift, Analyse, Cloudanmeldung oder zusätzliche Speicherung. Gleiche CSP mit connect-src self. Keine neue Fremdsoftware. Eigene Quelldateien und Herkunft lesbar veröffentlichen; bestehende AGPL-Lizenz und originale Provenienz unverändert.

Primär iPad im Querformat und Desktop. Unter 840 Pixeln bleibt die Programmierfläche in einem eigenen seitlich verschiebbaren Bereich; Rahmen/Dateiaktionen bleiben nutzbar. Canvas bleibt eine Grenze für Screenreader. Eine schmale HTML-Ansicht beweist keine echte Safari-Touchprobe.

Zuerst Verhaltenstests, Schutz des Altbestands und Build. Da die frühere lokale Snap!-Dateiprobe blockiert war, keine lokale Ersatz-Ausführung der Engine: tatsächliche Erprobung über die beauftragte GitHub Page als gekennzeichnete Testansicht. Der originale Einstieg bleibt dabei erhalten. Anschließend realen neuen Editor mit ALG-2/5/6, Schrittmodus, Datei-Rückkehr und schmaler Darstellung prüfen; Befunde bearbeiten, Grenzen als solche dokumentieren. Keine Behauptung vollständiger Safari-/Offlinefreigabe.
