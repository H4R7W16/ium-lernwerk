# Lehrkräftehandbuch: IUM-5-CORE-05

## Kompetenzbezug, Leitfrage und Zeitvertrag

Das Modul bindet `LH26-E-PROG-002` sowie `LH26-E-ALG-001` bis `LH26-E-ALG-004` aus der aktuellen Lesehilfe. Die Leitfrage lautet: „Wie werden Anweisungen so präzise, dass ein System sie eindeutig ausführen kann?“ Das zentrale Produkt ist ein ausführbarer grafischer Algorithmus mit Vorhersage, bestätigter Belegspur, Reparaturhypothese, revidierter Fassung und begründeter Entscheidung über eine feste Wiederholung.

Der reguläre Pfad umfasst 225 Minuten in fünf Unterrichtseinheiten. Der erweiterte Pfad umfasst 270 Minuten und ergänzt eine echte sechste Unterrichtseinheit. Beide Pfade entsprechen `TC-IUM-5-CORE-05`; `pilotRequired` bleibt wahr und der Status bleibt `working`.

## Fachlicher Hintergrund

Ein Algorithmus ist hier eine präzise, endliche Folge ausführbarer Anweisungen. Eine Anweisung bezeichnet einen einzelnen geschlossenen Befehl. Ausführung ist die Anwendung dieses Befehls auf einen Zustand. Der Zustand umfasst Position, Blickrichtung, Tragezustand, Gutposition und Lieferstatus. Eine Laufspur dokumentiert für jeden Schritt Quellbefehl, möglichen Schleifendurchlauf, Vorherzustand, Nachherzustand und Ergebnis.

Die feste Schleife wiederholt einen nichtleeren Körper mit ein bis vier Grundbefehlen genau zwei- bis neunmal. Sie ist nur dann fachlich passend, wenn dieselbe Befehlsfolge mit konstanter Anzahl wiederkehrt. Die Werkstatt begrenzt bewusst das Modell: Keine Verzweigung, bedingte Schleife, Variable, Ereignissteuerung oder freie Programmierung ist enthalten. Diese Abgrenzung schützt die altersangemessene Einführung und nimmt die für Klasse 7 vorgesehene Programmiertiefe nicht vorweg.

## Voraussetzungen

Vorausgesetzt werden die Arbeitsgrundlagen aus `IUM-5-CORE-01`: Browser öffnen, die Modulroute aufrufen, lokale Dateien gezielt auswählen und einen Export an einem vereinbarten Ort speichern. Fehlt diese Voraussetzung, demonstriert die Lehrkraft den Dateidialog und vereinbart einen lokalen Speicherort; die fachliche Algorithmusarbeit wird nicht durch ein separates Dateimanagementtraining ersetzt.

## Fünf Unterrichtseinheiten

### Unterrichtseinheit 1 – 45 Minuten

- 15 Minuten: mehrdeutigen Lieferauftrag öffnen und Leitfrage entwickeln;
- 20 Minuten: präzise Alltagsschritte vergleichen und Vorwissen aktivieren;
- 10 Minuten: Algorithmus und Anweisung am aktiven Beispiel explizieren.

### Unterrichtseinheit 2 – 45 Minuten

- 25 Minuten: Ausführung, Zustand und Laufspur begrifflich aufbauen;
- 20 Minuten: nächsten Zustand vorhersagen und schrittweise prüfen.

### Unterrichtseinheit 3 – 45 Minuten

- 25 Minuten: vier Fehlervarianten vergleichen und erste Abweichung lokalisieren;
- 20 Minuten: eigene Produktkarte wählen und Ausgangsfassung entwerfen.

### Unterrichtseinheit 4 – 45 Minuten

- 35 Minuten: eigenen Algorithmus vorhersagen, ausführen und Belegspur bestätigen;
- 10 Minuten: Reparaturhypothese formulieren und Revision prüfen.

### Unterrichtseinheit 5 – 45 Minuten

- 25 Minuten: Algorithmus-Lupe mit Positivfällen, Nichtbeispielen und Grenzfall;
- 20 Minuten: Selbstcheck, Schleifenentscheidung und gemeinsame Sicherung.

## Sechs Unterrichtseinheiten

Die zusätzliche sechste Unterrichtseinheit ist keine Wiederholung der Einführung. Lernende erhalten `extended-inherited`, einen vorhandenen Algorithmus mit genau einem geerbten Fehler zu einer neuen Karte. Sie sagen den Lauf voraus, führen schrittweise aus, lokalisieren die erste Abweichung, begründen eine gezielte Änderung und prüfen die revidierte Fassung. Die 45 Minuten bilden damit eine zusätzliche Ausführungs- und Reparaturleistung.

## Sozialform und Geräteverhältnis

In der Einzelarbeit bleibt jede Person für Vorhersage, Belegspur und Begründung verantwortlich. Partnererklärung dient dazu, einen konkreten Zustandswechsel oder eine Schleifenentscheidung fachsprachlich zu erläutern, nicht dazu, die Bedienung zu übernehmen. Bei einem Geräteverhältnis von 1:2 wechseln die Rollen nach jedem bestätigten Spurabschnitt: Eine Person bedient, die andere sagt den nächsten Zustand voraus und prüft die Textspur. Beide begründen nacheinander mindestens eine Entscheidung.

## Erwartbare Fehler

- falsche Reihenfolge: „An welcher Spurzeile befindet sich das Gut zum ersten Mal nicht mehr dort, wo du es erwartest?“
- falsche Drehung: „Was verändert eine Drehung – und was bleibt gleich?“
- fehlender Schritt: „Welche Koordinate fehlt zwischen der letzten passenden und der ersten abweichenden Zeile?“
- falsche Wiederholungszahl: „Wie viele einzelne Bewegungen zeigt die ausgeschriebene Schleife?“
- Aufnahme am falschen Ort: „Welche drei Bedingungen müssen vor `aufnehmen` sichtbar sein?“
- Ablage am falschen Ort: „Was unterscheidet Zielkoordinate und aktuelle Roboterkoordinate?“

Die Rückfragen beziehen sich auf beobachtbare Zustände und Befehle. Sie schreiben weder die Lösung vor noch ordnen Lernende einem Niveau zu.

## Erklärungspunkte und gemeinsame Sicherung

Verbindliche Erklärungspunkte sind der Unterschied zwischen Algorithmus und einzelner Anweisung, die Unveränderlichkeit der Position beim Drehen, die Bedeutung eines Vorher-/Nachherzustands, die erste Abweichung als Reparaturbeleg und die Bedingung einer konstanten Wiederholung. In der Sicherung werden je ein gelungenes Beispiel, ein Nichtbeispiel und ein Grenzfall mit denselben Kriterien besprochen.

## Hilfen, Beobachtungskriterien und frische Evidenzfälle

Hilfen werden von Lernenden selbst gewählt und nicht adaptiv zugeteilt: Szenenbeschreibung, Drehhilfe, ausgeschriebene Schleife, Laufspurtabelle, Satzstarter und Fragen zur ersten Abweichung. Beobachtet werden Präzision der Vorhersage, Bezug der Hypothese zur Belegspur, Sparsamkeit der Revision und Begründung der Schleifenentscheidung.

Fehlt eine belastbare Erklärung, nutzt die Lehrkraft einen frischen Kurzfall statt gespeicherter Verlaufsdaten: Start B3 mit Blick nach Osten und ein einzelner Drehbefehl; eine Zweischrittfolge mit vertauschter Aufnahme; sowie drei gleiche Bewegungen einmal ausgeschrieben und einmal als feste Wiederholung. Diese Fälle werden mündlich oder an der gemeinsamen Anzeige bearbeitet und nicht persistiert.

## Accessibility

Die zentrale Handlung ist ohne Maus, Drag-and-drop, Farberkennung oder Animation möglich. Jeder Block besitzt beschriftete Einfüge-, Verschiebe- und Löschaktionen. Raster und Laufspur haben vollständige Textäquivalente; Änderung von aktuellem Befehl und Ergebnis wird sichtbar und höflich angekündigt. Für Reflow bei 320 CSS-Pixeln und 200 Prozent Zoom werden Listen untereinander dargestellt. Bei Screenreadern beginnt die Orientierung mit Szenenbeschreibung und Algorithmusliste, anschließend folgen Vorhersage, Ausführung und Laufspur.

## Technische Fallbacks, Offline und Geräte

Der Kernpfad benötigt keine externe Verbindung. Vor Unterrichtsbeginn wird die Modulroute einmal online installiert und danach im Offlinebetrieb geprüft. Bei ausbleibender grafischer Darstellung bleibt die textuelle Szenenbeschreibung fachlich maßgeblich. Bei Geräteausfall arbeitet das Paar am verbleibenden Gerät mit dem geregelten Rollenwechsel. Ist kein Gerät verfügbar, wird die Stunde nicht mit einer ungleichwertigen Kopie der Werkstatt ersetzt; die Lehrkraft nutzt einen kurzen gemeinsamen Zustandsvergleich und verschiebt die individuelle Ausführung.

## Datenschutz und Export

Es gibt keine integrierte Diagnostik und keine personenbezogene Übertragung. Lokal gespeichert werden ausschließlich Phase, Szenario, Ausgangsalgorithmus, Vorhersage, bestätigte Belegspur, Reparaturquelle, Reparaturhypothese, revidierter Algorithmus, Schleifenentscheidung, Systemklassifikationen und Selbstcheck. Hilfenutzung, Bearbeitungszeit, Versuchshistorie, Name, Kennung und Geräteprofil gehören nicht zum Zustand. Export und Import verarbeiten nur diesen Arbeitsbestand; Löschen entfernt ihn lokal.

## Lizenz und Quellen

Programmcode steht unter MIT. Lerntexte, Aufgaben, Szenarien und die projektintern gezeichnete Robotergrafik stehen unter CC BY-SA 4.0. Die Assetprovenienz liegt maschinenlesbar in `assets/licenses.json`. Curriculare Aussagen referenzieren die Repositoryquelle `curriculum/lesehilfe-2026-27/competencies.json`; Zeitannahmen referenzieren `roadmap/time-model.json`.

## Status- und Einsatzgrenze

Der Modulstand ist `working`, nicht `reviewed`, `standard` oder einsatzfreigegeben. `device-verified` bleibt `not-run`. Das interne Gate A kann technische und fachliche Prüfbarkeit feststellen; es öffnet nicht Gate B. Pilotierung, reale Lernendendaten, LMS-Integration, Benotung, Kompetenzprofile und automatische Freigabeentscheidungen sind nicht Bestandteil dieses Stands. Die Werkstatt erzeugt ausdrücklich keine automatische Diagnose, Punktzahl oder Einsatzfreigabe.
