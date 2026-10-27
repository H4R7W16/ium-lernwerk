# Klassenstufen-Auswahl – Umsetzungsplan

> Umsetzung inline; Repositoryvorgabe: Selbstreview ohne zusätzliche Agenten.

**Ziel:** Klick auf die Klassenstufe im IuM-Titel öffnet die Auswahl Klasse 5, 6 und 7; ein Eintrag führt zum vorhandenen Jahrgangseinstieg.

**Ansatz:** Native HTML-details/summary-Auswahl im bestehenden Kopf. Klasse 5/6 behalten ihre Wortmarken; Klasse 7 bekommt die Stufe im anklickbaren Titel. Die aktuelle Stufe ist markiert. Normale Links erhalten vorhandene Speicher-/Verlassen-Schutzmechanismen. Escape und Klick außerhalb schließen die Auswahl. Keine neue Bibliothek, Telemetrie oder Speicherung.

**Bestandsschutz:** Eine eng begrenzte letzte Ausgabestufe ergänzt Header und lokale Menü-Assets nach der unveränderten gebundenen Inhaltsvorbereitung. `preparePages()` bleibt die geprüfte Ausgangsfassung; `preparePublishedPages()` wird die vollständige veröffentlichte Ausgabe. Neue Tests prüfen alle tatsächlichen Ausgabeseiten, gültige Ziele und bytegleiche Inhalte außerhalb des Headers. Historische Quellen, ursprüngliche Snap!-Engine und Unterrichtsinhalte bleiben geschützt. Das zusätzliche Herkunftsmanifest bindet die angepasste eigene Editorhülle samt Menü-Assets neu und bewahrt deren Ausgangshash. Klasse-5/6-Service-Worker erhalten die lokalen Menüdateien und eine neue Versionskennung. Zusätzliche eingefrorene Recherche-Beispiele behalten ihren Referenzstand.

## Dateien

- Neu: `prototypes/shared/grade-navigation.cjs`, `grade-navigation.css`, `grade-navigation.js`.
- Ergänzen: `prototypes/pages/build.cjs`; vorherige Bestandstests unverändert, neue Integrationstests unter `prototypes/pages/grade-navigation.test.cjs`.
- Dokumentieren: kurzer Pages-README-Eintrag, Session-/Veröffentlichungsnachweis im Vault.

## Schritte

- [x] Integrationstests für reale Jahrgangsseiten, relative Ziele, Artikelerhalt, unveränderte Laufzeit und Offline-Dateien schreiben; fehlende Auswahl als roten Test beobachten.
- [x] Header-Ergänzung und lokales Menüverhalten implementieren; Tests grün ausführen.
- [x] Vollständigen bisherigen Pages-Testbefehl einmal ausführen und frischen Build erzeugen. Den bestehenden expliziten Pages-Prüfpfad erhalten und `prototypes/pages/grade-navigation.test.cjs` ausdrücklich ergänzen.
- [x] Tatsächliche Ausgabe im Browser bedienen: Öffnen, aktuelle Stufe, Wechsel 5/6/7, Escape, Außenklick und Rückkehr mit einem synthetischen Arbeitsstand. Menü auf schmalem Gerät prüfen. Lokale Snap!-Ausführung bleibt außerhalb der Browserprobe; Original-Engine wird technisch unverändert geprüft.
- [ ] Diff im Selbstreview prüfen, Commit/PR integrieren, Pages-Deployment und öffentliche Menüs prüfen. Keine Schutzregeln übersteuern. Git-Stand und tatsächliche Prüfgrenzen dokumentieren.

## Kritische Fälle

- Unterseiten dürfen relative Links nicht in ihr eigenes Themenverzeichnis auflösen.
- Wechsel darf vorhandene Eingaben nicht durch neue Speicherlogik überschreiben.
- Popup muss auf schmaler Ansicht erreichbar bleiben und darf das Canvas nicht verdeckt unerreichbar machen.
- Offline-Caches müssen die neue Navigation mitnehmen; die Auswahl verspricht keinen offline verfügbaren anderen Jahrgang.
- Snap!-Originaldateien, Programmprojekte und externe Verbindungsregeln bleiben unverändert.

## Laufender Selbstreview

Rotlauf: drei fehlende Navigations-/Offline-Eigenschaften scheiterten, bestehende Verweise bestanden. Danach fünf Integrationstests erfolgreich. Erste Browserprobe: Wechsel 5→6→7, Enter, Escape und Außenklick erfolgreich. Zwei lokale UI-Befunde: Themen- und Klassenmenü gleichzeitig offen; mobile Wortmarke durch nebeneinander angeordnete Fachbezeichnung zu klein. Korrektur: Themenmenü beim Öffnen der Stufenauswahl schließen; Wortmarke mit Fachzeile im Grid erhalten. Nachprüfung am frischen zweiten Build erforderlich.

Endbuild release2: 144/144 Veröffentlichungsprüfungen erfolgreich, 1.154 Dateien. Browsernachprüfung: ein Kopfmenü offen; mobile Wortmarke wieder lesbar, Menü innerhalb375px Inhaltbreite, Tab/Enter/Escape/Außenklick funktionieren. Tatsächlicher Wechsel5→6→7 und zurück; synthetische Testantwort bleibt nach5→6→5 vorhanden. Safari-Hardwareprobe und unsicherer Snap-Verlassen-Fall nicht neu ausgeführt; bestehender Guard und originale Engine technisch erhalten.

Vor Auslieferung neue Textdateien auf LF normalisiert und die Versionssortierung plattformunabhängig gemacht, damit lokaler und GitHub-Build identische Asset-/Cachehashes erzeugen. Eng betroffene Integrationsprüfungen und Endbuild werden erneut ausgeführt.

CI-Nachprüfung: Der bestehende Workflow-Vertrag verlangt den wörtlichen bisherigen Pfad. Den ersetzenden Glob zurückgenommen und den neuen Test explizit daneben ergänzt; betroffenen Plattform-Vertrag gezielt nachprüfen. Keine Testanforderung gelockert.
