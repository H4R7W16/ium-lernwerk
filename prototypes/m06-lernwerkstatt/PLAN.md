# Lernwerkstatt: Entwurf und Ausführung
Stand 22.09.2026. Auftrag: neue, eigenständige Referenz nach Ablehnung von V3. Primär Schul-iPads.
## Gestaltungsentscheidung
Kein Artikel mit angehängtem Simulator. Eine gemeinsame Arbeitsfläche verbindet antippbares Programm, große Bodenfläche, Vorhersage, Ausführung und konkrete Rückmeldung. Sekundäre Erklärungen sind pro Aufgabe in einem erreichbaren Lesebereich verfügbar. Vollständige bisherige Lesefassung bleibt erreichbar.
Verworfene Alternativen: weitere Etappen um V3 (erhält dessen Simulationsschwäche); bloßes V2-Reskin (behebt Erklärungslücken nicht).
## Lernarchitektur
Vorhersage von Bewegung/Drehung → ganzer Schleifenkörper und ausgeschriebene Folge → Befehl nach Schleife → falsche Gruppierung reparieren → Reihen planen → zweiter Reihenwechsel → eigener Flächenplan → Randrunde beurteilen → Transfer auf Prüfstation → Abruf mit neuem Start.
Beispiele, gestufte Hinweise und begründete Lösungen unmittelbar je Lernstation. Rückmeldungen unterscheiden ausführbar, Flächendeckung und Erklärung. Freie Lösungen nach Kriterien.
## Umsetzung
1. Eigenständiger Adapter über bestehendem geprüften Modell, Tests für Teilflächen, Schleifen und Stationstransfer.
2. Neue DOM-/SVG-Oberfläche: Codeblöcke, Einzelschritt, zurück, Animation/Pause, Ende, Verlauf; reduzierbare Bewegung.
3. Touch-Bausteine mit Bearbeiten/Einfügen/Umordnen, keine Drag-Pflicht. Notizen in Sitzung, ausdrücklich aktivierbare Gerätespeicherung.
4. Tablet-Quer-/Hochformat visuell prüfen; gerichtete Modell-/Pages-Checks; unabhängiger Abschlussreview.
5. Neue Pages-Route /lernwerkstatt/ plus Versionswahl. Historische Fassungen erhalten.
## Qualität
1024×768 und 768×1024, 390 schmal. Kein Hover als notwendige Bedienung; Kernaktionen mindestens 44 CSS-px; Fokus erhalten, Dialog-Rückkehr; Animation bei Navigation/Editieren stoppen; Ausführung bleibt an den geprüften Entwurf gebunden.
Tests allein belegen keine Motivation. Prüfung auf echtem iPad/Safari und mit Lernenden bleibt gesondert.
## Ledger
- Bestehenden isolierten Worktree wiederverwendet, eigener Branch feat/m06-lernwerkstatt auf aktuellem origin/main.
- Die pädagogische Begründung stützt sich auf vorhandene Module und lokale WU-Exzerpte 1, 9, 12; keine neuen empirischen Wirksamkeitsbehauptungen.
- Kein Import/Export und keine Gesamtsuite. Neue Oberfläche hat keinen Dateiimport/-export.
