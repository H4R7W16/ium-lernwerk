# ALG-5: eigene Projekte in „Deine Arbeit“

Stand: 07.11.2026. Umsetzung abgeschlossen; die praktische Endprüfung ist auf ausdrückliche Nutzerentscheidung als Annahme akzeptiert. Diese Erweiterung ist noch nicht veröffentlicht.

Bisher merkte die Karte nur, wo eine separate XML-Datei liegt. Jetzt kann eine ALG-5-Karte eine bewusste Kopie des eigenen Snap-Projekts enthalten. Damit wird der letzte übernommene Stand über die Karte wieder geöffnet und zusammen mit der Übersicht transportiert.

## Ablauf für Lernende

1. ALG-5 als Arbeitsstelle merken und „Snap-Projekt hinzufügen“ wählen.
2. Eine eigene XML-Datei öffnen oder bewusst mit dem Startprojekt beginnen. Den Rover bearbeiten und „Projektstand übernehmen“ wählen. Die Karte zeigt Dateiname und Übernahmezeitpunkt.
3. „Übersicht mit Projekt herunterladen“ wählen und die tatsächlich heruntergeladene Datei am Ablageort prüfen. Auf einem anderen Gerät unter „Deine Arbeit“ die Übersichtsdatei laden, gewünschte Karte übernehmen und „Mein Projekt weiterbearbeiten“ wählen.

Weitere Editoränderungen benötigen eine erneute Übernahme. Heftnotizen, Bilder und andere externe Dateien werden weiterhin gesondert mitgenommen. Eine bloße Downloadanforderung wird nicht als bestätigte dauerhafte Ablage ausgegeben.

## Umsetzung und Schutz eigener Arbeit

- Das versionierte Übersichtspaket V2 kann ALG-5-Projektkopien enthalten; V1-Übersichten bleiben lesbar. Hinweisänderungen und Auswahlimporte erhalten die zugehörige Projektkopie. Andere Karten und Jahrgänge werden nicht in Snap-Projekte umgewandelt.
- Der zusätzliche ALG-5-Editor wird aus den bestehenden Snap-Quellen abgeleitet. Die bisher veröffentlichten Editor-Dateien werden nicht umgeschrieben. Herkunft und Ausgabe werden beim Build gebunden.
- XML-Strukturprüfung, 10 MiB pro Projekt und 32 MiB pro Paket begrenzen fehlerhafte Eingaben. Browserquota kann früher greifen; der offene Stand bleibt dann flüchtig verfügbar und muss exportiert werden.
- Übernahme berücksichtigt die tatsächlich erfasste Revision. Ungesicherte Änderungen, asynchroner Dateiaustausch und Ladefehler erhalten eigene Schutzwege; bei gescheiterter Wiederherstellung wird eine XML-Rettungskopie angeboten. Laden oder Übernehmen soll keine Programme unbeabsichtigt weiterlaufen lassen.

## Review und Prüfgrenze

Der Gegenreview fand sechs konkrete Befunde: Änderungen während verzögertem Dateilesen, erneutes Entsperren über den Startknopf, nicht erreichbare Rettungskopie, falsch positiver Downloadtext, durch Snap-Speicherereignisse gestartete Programme und Tastaturzugriff auf den verdeckten Editor. Die Korrekturen wurden mit zunächst roten und anschließend grünen Regressionen nachgeprüft. Der letzte gezielte Reviewlauf bestand aus 27 Tests (5 UI-Ereignistests mit DOM-Mock, 6 Sitzungstests, 16 Adapter-/Bridge-Tests).

Im tatsächlichen Browser wurde zusätzlich ein Layoutfehler durch einen vollständig versteckten iframe erkannt und korrigiert: Der Editor bleibt nun im Layout, ist zunächst abgedeckt und inert. Die abschließende reale XML-/Paket-Rücksicherung sowie schmale Tastaturbedienung und Druckmetadaten dieser Erweiterung sind nicht vollständig nachgewiesen. Die Computersteuerung brach die praktische Endprüfung aus Sicherheitsgründen ab; keine alternative Steuerung wurde zur Umgehung dieser Sperre eingesetzt.

Am 07.11.2026 erklärte der Nutzer: „wir gehen davon aus, dass es funktoniert.“ Der Abschluss übernimmt diese Annahme ausdrücklich, ohne einen bestandenen Browserdurchlauf, eine reale Lernendenerprobung oder einen vollständigen formalen Qualitätspass zu behaupten. Automatisierte Tests und statischer Review sind Funktionsnachweise mit den genannten Grenzen. Der Implementierungsplan hält diese Entscheidung ebenfalls fest.


## Abschließende technische Prüfung

Nach dem Fast-Forward-Abgleich auf main `2c3b5563ae6f0a0888811df314337853dcb041f4` bestand am 07.11.2026 die vollständige Pages-Prüfkette aus CONTRIBUTING.md mit **273/273 Tests**, ohne Fehler oder übersprungene Tests (103,4 Sekunden, Exit 0). Ein frischer Pages-Build erzeugte **1.397 Dateien**. Die fünf gegenüber dem vorherigen Prüfstand hinzugekommenen Tests stammen aus dem zwischenzeitlich aktualisierten Hauptzweig. Diese Prüfung umfasst den letzten Startknopf-/Dateileseschutz.

Die lokalen Belege liegen unter `AI-Workspace-Local/Work/ium7-alg5-projektstand-20261106-qa`: `final-pages-tests.log`, `final-pages-test-result.json`, `final-build.log` und der gesonderte Buildvergleich gegen main. Der statische Detailreview ist unter `review-final.md` dokumentiert. Archivierte Abschlussbelege und der Git-Handoff sind in der Workspace-Session „2026-11-07 - ALG-5 Projektstände Abschluss unter akzeptierter Prüfannahme“ verknüpft. Keine dieser technischen Prüfungen ersetzt die oben benannte praktische Prüfannahme.
