# IUM-5-CORE-05 – Modulspezifikation „Präzise Abläufe ausführbar machen“

**Status:** zur Schriftprüfung nach freigegebenem Gesamtdesign

**Datum:** 3. August 2026

**Scope:** fachlich-didaktisches, interaktives und technisches Design des ersten Phase-2-Goldstandardmoduls

**Ausgangsstand:** `main` auf Commit `a7e3868`

## 1. Entscheidung und Ziel

`IUM-5-CORE-05 – Präzise Abläufe ausführbar machen` wird als digitale **hybride Algorithmus-Werkstatt** für das Gymnasium in Klasse 5 umgesetzt. Ein schulbezogener Lieferroboter dient als stabiles Modell für die Ausführung eindeutiger Anweisungen. Er ist weder Spielfigur noch Belohnungssystem. Nach dem Aufbau des Algorithmusbegriffs wird der Kontext im Transfer bewusst verlassen.

Das Modul verbindet in einem durchgängigen Lernzyklus:

```text
Entwurf → Vorhersage → Ausführung → Vergleich → Reparaturhypothese → Revision → Sicherung
```

Die Lernenden erzeugen nicht bloß einen funktionierenden Ablauf. Sie machen ihr Verständnis durch Vorhersage, Laufspur, begründete Fehlerkorrektur und eine angemessene Entscheidung über eine Schleife sichtbar.

Diese Spezifikation ist implementierungsnah, startet aber noch keine Implementierung. Sie hält Gate B für Pilotierung, LMS-Einbindung und Produktrelease geschlossen.

## 2. Status- und Gategrenze

Für das Modul gilt während der gesamten hier spezifizierten Entwicklung:

- Modulstatus `working`;
- Gate A für Spezifikation, Implementierung mit synthetischen Daten und interne Qualitätssicherung ist offen;
- Gate B für Unterrichtspilotierung, reale Lernendendaten, LMS-Einbindung und Veröffentlichung als einsatzbereites Produkt bleibt geschlossen;
- `device-verified` bleibt `not-run`;
- automatisierte Tests, interne Reviews und öffentliche Quelltexte dürfen den Status nicht selbstständig auf `reviewed` oder `standard` anheben;
- jede Oberfläche und Dokumentation kennzeichnet den Arbeitsstand unmissverständlich.

Verbindliche Gategrundlage ist `docs/superpowers/specs/2026-08-03-ium-phase2-entwicklungs-und-einsatzgate-design.md`.

## 3. Bindende Grundlagen und Hierarchie

Das Modul folgt in dieser Reihenfolge:

1. der aktuellen Lesehilfe Informatik und Medienbildung für Gymnasium und Sekundarstufe I in Baden-Württemberg als curricularem Orientierungsbestand;
2. den normalisierten Curriculumrecords und dem Phase-0-Crosswalk des Repositories;
3. dem Fachprofil `docs/fachprofil/ium-gymnasium-5-7.md`;
4. dem freigegebenen Gesamtdesign und dem Phase-1-Plattformvertrag;
5. dem autoritativen Zeitvertrag in `roadmap/time-model.json`;
6. den didaktischen Arbeitsannahmen aus dem kuratierten Forschungsbestand, insbesondere `CLAIM-INF-003`, `CLAIM-INF-004`, `CLAIM-INF-006`, `CLAIM-INF-007`, `CLAIM-LP-001`, `CLAIM-LP-002`, `CLAIM-LP-010`, `CLAIM-LP-012` und `CLAIM-LP-013`.

Forschungsbefunde aus Hochschulkontexten werden dabei als begründete Designheuristik, nicht als gesicherter Wirksamkeitsnachweis für Klasse 5 behandelt. Die konkrete Altersangemessenheit bleibt später pilotierungspflichtig.

## 4. Curricularer Vertrag

| Feld | Festlegung |
|---|---|
| Modul-ID | `IUM-5-CORE-05` |
| Titel | Präzise Abläufe ausführbar machen |
| Schulart und Jahrgang | Gymnasium, Klasse 5 |
| Art | Kernmodul |
| Lernstrang | `STRAND-A` |
| Voraussetzung | `IUM-5-CORE-01` |
| Primäre Kompetenzrecords | `LH26-E-PROG-002`, `LH26-E-ALG-001`, `LH26-E-ALG-002`, `LH26-E-ALG-003`, `LH26-E-ALG-004` |
| Zeit | regulär/baseline 5 UE = 225 Minuten; erweitert 6 UE = 270 Minuten |
| Spätere Wiederaufnahme | `IUM-6-CORE-04` |
| Status | `working` |
| Pilotpflicht | `pilotRequired: true` |

Das Modul deckt folgende fachliche Handlungen ab:

- erste, niedrigschwellige Schritte im Umgang mit Algorithmen, ohne die für Klasse 7 vorgesehene Programmiertiefe vorwegzunehmen;
- digitale Systeme erkennen, deren Funktion wesentlich durch algorithmische Abläufe bestimmt ist;
- einen Algorithmus als präzise Folge ausführbarer Anweisungen beschreiben;
- einfache grafische Algorithmen erklären und ausführen;
- Anweisung und Schleife mit fester Wiederholungszahl als Grundbausteine verwenden.

Explizit ausgeschlossen bleiben Verzweigungen, bedingte Schleifen, Variablen, freie Programmierung und die in Klasse 7 vorgesehene vertiefte Kontrollflussanalyse.

## 5. Leitfrage, Lernziele und Erfolgskriterien

### 5.1 Leitfrage

> Wie genau muss eine Vorschrift sein, damit Mensch und digitales System denselben Ablauf ausführen?

### 5.2 Lernziele

Am Ende des regulären Pfads können Lernende:

1. mehrdeutige und ausführbare Anweisungen anhand eines konkreten Zustands unterscheiden;
2. einen einfachen grafischen Algorithmus schrittweise vorhersagen, ausführen und anhand einer Laufspur erklären;
3. eine Abweichung am ersten verursachenden Schritt lokalisieren;
4. eine Reparaturhypothese formulieren, gezielt prüfen und den Algorithmus revidieren;
5. eine feste Wiederholung passend einsetzen oder begründet darauf verzichten;
6. an Beispielen, Nichtbeispielen und einem Grenzfall beurteilen, ob die Funktion eines digitalen Systems wesentlich algorithmisch bestimmt ist.

### 5.3 Transparente Qualitätskriterien

Ein gelungenes Lernprodukt ist:

- **präzise:** Jede Anweisung hat in der gegebenen Situation eine eindeutige Bedeutung;
- **ausführbar:** Der festgelegte Interpreter kann jeden zulässigen Schritt ausführen;
- **zielerreichend:** Der Lieferauftrag wird ohne ungültige Aktion abgeschlossen;
- **nachvollziehbar:** Vorhersage und relevante Laufspur lassen den Ablauf erkennen;
- **revidiert:** Die Reparatur bezieht sich auf die zuerst festgestellte Abweichung;
- **begründet:** Die Schleifenentscheidung passt zu einer konstanten Wiederholung.

Die kürzeste Route ist kein allgemeines Qualitätskriterium. Das Modul optimiert Verständnis und Präzision, nicht Geschwindigkeit oder Code-Golf.

## 6. Zentrales Lernprodukt

Der lokale Arbeitsbestand enthält genau die fachlich erforderlichen Produktspuren:

1. den ersten eigenständigen grafischen Algorithmus;
2. die strukturierte Vorhersage von Zielposition, Blickrichtung und Auftragserfolg;
3. die für die Begründung relevante Laufspur einschließlich erster Abweichung oder erfolgreichem Abschluss;
4. die gekennzeichnete Reparaturquelle: eigener Entwurf oder standardisierter Einzelfehlerfall;
5. eine kurze Reparaturhypothese;
6. die revidierte Fassung des reparierten Algorithmus;
7. eine kurze Begründung, warum eine feste Schleife verwendet oder nicht verwendet wurde;
8. die fallbezogene Einordnung algorithmisch bestimmter Systeme, einschließlich Begründung des Grenzfalls.

Die Laufspur ist nicht als lückenloses Verlaufsprofil aller Versuche gedacht. Für das Produkt wird nur die von der lernenden Person ausgewählte oder zuletzt bestätigte Belegspur gesichert. Ist der erste eigenständige Entwurf bereits fachlich korrekt, bearbeitet die lernende Person zusätzlich einen für alle gleichartigen, standardisierten Einzelfehlerfall. Damit bleibt die Reparatur eine verbindliche Lernhandlung, ohne im eigenen Entwurf künstlich einen Fehler zu erzeugen oder zufälliges Scheitern zu belohnen.

## 7. Geprüfte Designansätze

### 7.1 Gewählt: hybride Algorithmus-Werkstatt

Der Ansatz koppelt einen begrenzten grafischen Befehlseditor, ein sichtbares Zustandsmodell, verpflichtende Vorhersage, deterministische Ausführung, Laufspur und Revision. Er ermöglicht fachliche Ausführung und Fehlersuche ohne die zusätzliche Syntaxlast einer Programmiersprache.

### 7.2 Nicht gewählt: spielzentriertes Robotik-Abenteuer

Punkte, Level, Avatarfortschritt, Belohnungen und künstliche Zeitverknappung würden den Fokus von Präzision, Zustand und Begründung auf extrinsische Spielziele verschieben. Der Roboter bleibt daher Modellobjekt.

### 7.3 Nicht gewählt: freier Blockprogrammiereditor

Ein allgemeiner Editor würde Funktionen eröffnen, die curricular noch nicht erforderlich sind, und die Lernhandlung durch Werkzeug- und Suchlast verbreitern. Das Modul verwendet ausschließlich die benötigte Befehlssprache.

### 7.4 Nicht gewählt: rein analoge Boden- oder Kartenprogrammierung

Analoge Ausführung kann fachlich sinnvoll sein, ist hier aber nicht überlegen: Das digitale Medium koppelt identische Semantik, schrittweise Zustandsänderung, reproduzierbare Fehler, Laufspur und Revision unmittelbar. Eine parallele Papierstruktur hätte keine eigenständige Lernfunktion.

## 8. Kontext und Modellgrenze

Der wiederkehrende Kontext ist ein Lieferroboter in einem vereinfachten Schulgebäude. Er bewegt genau ein Transportgut von einem Startfeld zu einem gekennzeichneten Ziel. Karten, Hindernisse, Gut und Ablageziel sind synthetisch und enthalten keine realen Orts-, Personen- oder Schuldaten.

Der Kontext erfüllt drei Funktionen:

- Er gibt jeder Anweisung eine beobachtbare Zustandswirkung.
- Er macht Mehrdeutigkeit und falsche Reihenfolge sichtbar.
- Er erlaubt feste Wiederholungen ohne Einführung weiterer Kontrollstrukturen.

Die Modellgrenze wird ausdrücklich gesichert: Reale Roboter besitzen Sensoren, Unsicherheiten und komplexere Steuerungen. Das Lernmodell führt nur die hier definierte Befehlssprache auf einem diskreten Raster aus. Im Transfer wird daher nicht behauptet, jedes digitale System arbeite wie der Lieferroboter.

## 9. Befehlssprache und Zustandsmodell

### 9.1 Zulässige Befehle

| Anzeige | Semantik |
|---|---|
| `Gehe` | Bewege den Roboter genau ein Feld in aktueller Blickrichtung. |
| `Drehe links` | Ändere die Blickrichtung um 90 Grad gegen den Uhrzeigersinn; die Position bleibt gleich. |
| `Drehe rechts` | Ändere die Blickrichtung um 90 Grad im Uhrzeigersinn; die Position bleibt gleich. |
| `Nimm auf` | Nimm das Gut auf dem aktuellen Feld auf, falls der Roboter nichts trägt. |
| `Lege ab` | Lege das getragene Gut auf dem aktuellen Zielfeld ab. |
| `Wiederhole n-mal` | Führe die enthaltene Folge mit konstanter Anzahl `n` vollständig aus. |

Für `Wiederhole n-mal` gelten:

- `n` ist eine ganze Zahl von 2 bis 9;
- der Schleifenkörper enthält 1 bis 4 Grundbefehle;
- Schleifen dürfen nicht verschachtelt werden;
- Bedingungen, Abbruchbefehle und Variablen existieren nicht.

### 9.2 Raster und Zustand

- Ein Szenario verwendet höchstens ein Raster von 6 × 6 Feldern.
- Koordinaten werden textlich als Spalte und Zeile benannt, beispielsweise `C4`.
- Bewegungen sind nur orthogonal möglich.
- Ein vollständiger Zustand besteht aus Position, Blickrichtung, Tragezustand, Position des Guts, Zielzustand und aktuellem Ausführungsschritt.
- Ein Szenario definiert Startzustand, Hindernisse, Gut, Ablageziel und erwarteten Abschluss vollständig als geprüfte Daten.

### 9.3 Determinismus und Sicherheitsgrenze

Gleicher Startzustand und gleicher Algorithmus erzeugen immer dieselbe Laufspur. Weder Lerntext noch Importdatei kann ausführbaren JavaScript-Code, dynamische Komponenten oder externe Inhalte einspeisen.

Eine Ausführung endet:

- nach erfolgreichem Abarbeiten aller expandierten Grundbefehle;
- beim ersten fachlichen Fehler;
- spätestens nach 100 expandierten Grundbefehlen als technische Sicherheitsgrenze.

## 10. Fehlersemantik

Der Interpreter kennt genau folgende fachliche Fehler:

| Fehler | Auslöser | Zustandswirkung |
|---|---|---|
| Hindernis | `Gehe` würde auf ein blockiertes Feld führen. | Position bleibt unverändert; fehlgeschlagener Schritt wird protokolliert; Lauf stoppt. |
| Außerhalb | `Gehe` würde das Raster verlassen. | Position bleibt unverändert; fehlgeschlagener Schritt wird protokolliert; Lauf stoppt. |
| Gut fehlt | `Nimm auf` wird ohne verfügbares Gut am Feld oder mit bereits getragenem Gut ausgeführt. | Fachzustand bleibt unverändert; Lauf stoppt. |
| Ablage ungültig | `Lege ab` wird ohne getragenes Gut oder außerhalb des Zielfelds ausgeführt. | Fachzustand bleibt unverändert; Lauf stoppt. |
| Wiederholungszahl ungültig | Anzahl oder Schleifenkörper verletzt den Befehlsvertrag. | Algorithmus ist nicht startbar; der fehlerhafte Block wird benannt. |
| Schrittgrenze | Mehr als 100 Grundbefehle wären erforderlich. | Lauf stoppt vor dem nächsten Schritt; technische Grenze wird als solche, nicht als fachlicher Roboterfehler erklärt. |

Die Meldung benennt nie sofort die vollständige Lösung. Sie zeigt Ergebnis, verursachenden Schritt und Zustand und führt dann zum Vergleich mit Vorhersage und Laufspur.

## 11. Interaktionszyklus

### 11.1 Entwurf

Lernende fügen Befehle über beschriftete Schaltflächen ein, verschieben sie nach oben oder unten und löschen sie gezielt. Drag-and-drop darf ergänzend angeboten werden, ist aber niemals erforderlich. Für jeden Block sind Position und Zugehörigkeit zur Schleife textlich erkennbar.

### 11.2 Vorhersage

Vor der ersten Ausführung und nach einer inhaltlichen Revision wird eine kurze strukturierte Vorhersage verlangt:

- erwartete Endposition;
- erwartete Blickrichtung;
- erwarteter Auftragserfolg `ja`, `nein` oder `unsicher`.

Die Vorhersage wird nicht bewertet. Ihr Abschluss schaltet die Ausführung frei, damit der anschließende Vergleich eine echte Denkhandlung bleibt. Bei rein technischen Wiederholungen, etwa nach Wiederherstellung eines identischen Zustands, wird sie nicht künstlich erneut verlangt.

### 11.3 Ausführung

Die Standardbedienung ist schrittweise. Zusätzlich kann der vollständige Lauf abgespielt werden. Sichtbar und für assistive Technik verfügbar sind:

- aktueller Befehl;
- Position und Blickrichtung;
- Tragezustand;
- bei Schleifen aktuelle Iteration und Gesamtzahl;
- Ergebnis oder Fehlerzustand.

### 11.4 Vergleich und Reparatur

Nach Ende oder Fehler vergleicht die Oberfläche Vorhersage und beobachteten Zustand. Die Lernenden markieren die erste relevante Abweichung in der Laufspur und vervollständigen einen Satzstarter, zum Beispiel:

- „Ich vermute, der erste falsche Schritt ist …, weil …“
- „Wenn ich … ändere, dann sollte …“

Freie Kurzbegründungen sind auf 500 Unicode-Zeichen begrenzt. Es gibt keine Namensfelder.

### 11.5 Revision und Sicherung

Eine Revision erzeugt keine unbegrenzte Versuchshistorie. Für den reduzierbaren Arbeitsbestand bleiben die freigegebene Ausgangsfassung, die bestätigte Belegspur und die revidierte Fassung erhalten. Ist der eigene Entwurf beim ersten Lauf bereits korrekt, öffnet das Modul keinen personenbezogenen Adaptionspfad, sondern weist den im Aufgabenvertrag vorgesehenen standardisierten Einzelfehlerfall zu; dessen Ausgangsfassung, Belegspur und Reparatur bilden dann die Revisionsspur. Danach begründet die lernende Person ihre Schleifenentscheidung und bearbeitet den Systemtransfer.

## 12. Oberflächenarchitektur

Gewählt ist die **zweigeteilte Fokuswerkstatt**:

- links beziehungsweise zuerst: Ausführungsraum mit Raster, Roboter, Gut, Ziel und Zustandsbeschreibung;
- rechts beziehungsweise danach: grafischer Algorithmuseditor;
- direkt darunter: Vorhersage, Laufspur, Abweichungsanalyse und Revision;
- darüber: aktueller Auftrag und Lernziel;
- am Ende: Sicherung und Transfer.

Auf schmalen Ansichten werden Ausführungsraum und Editor in derselben logischen Reihenfolge untereinander angeordnet. Es gibt keine horizontale Seitenbedingung. Die Oberfläche muss bei 320 CSS-Pixeln Breite und 200 Prozent Zoom vollständig bedienbar bleiben.

Jede Lernphase zeigt nur die gerade benötigten Werkzeuge. Navigation und Status bleiben stabil; dekorative Elemente dürfen die Befehls- und Zustandsrepräsentation nicht verdrängen.

## 13. Fünf Aufgabenfamilien

### 13.1 Präzisionskontraste

Lernende vergleichen kurze Alltags- und Roboteranweisungen, beispielsweise „Geh zur Tür“ mit einer zustandsbezogenen Schrittfolge. Sie benennen, welche Information fehlt, ohne schon eine formale Definition auswendig zu lernen.

### 13.2 Aktiv bearbeitete Beispiele

Ein vollständiges Beispiel wird nicht nur vorgespielt. Lernende sagen den nächsten Zustand voraus, ordnen Teilsequenzen, ergänzen eine Lücke oder vergleichen zwei fast gleiche Algorithmen. Danach werden Algorithmus, Anweisung, Ausführung, Zustand und Laufspur explizit erklärt.

### 13.3 Gezielte Fehlerfälle

Kurze Fälle isolieren jeweils einen Schwerpunkt:

- falsche Reihenfolge;
- falsche Drehung;
- fehlender Schritt;
- unpassende feste Wiederholungszahl.

Die Fälle verlangen Lokalisierung, Hypothese, gezielte Änderung und erneute Prüfung, nicht bloß „noch einmal probieren“.

### 13.4 Eigenständiger Lieferauftrag

Die Lernenden bearbeiten eine von drei fachlich gleichwertigen Karten. Jede Variante verlangt Aufnahme, Transport, Ablage, mindestens eine Richtungsänderung und eine sinnvolle Entscheidung über eine feste Wiederholung. Die Varianten unterscheiden sich nicht in der geforderten Kompetenz, sondern reduzieren bloßes Abschreiben.

### 13.5 Algorithmus-Lupe

Im Transfer ordnen Lernende kuratierte Fälle ein:

- deutlich algorithmisch bestimmte digitale Systeme, etwa Navigation, Suchdienst oder digitale Stundenplananzeige;
- Nichtbeispiele, etwa Papierkarte oder rein mechanischer Kurzzeitwecker;
- einen Grenzfall, etwa ein Fahrzeug, bei dem erst geklärt werden muss, ob eine Person es direkt fernsteuert oder ein gespeicherter Ablauf ausgeführt wird.

Die Aufgabe verlangt eine kurze fallbezogene Begründung. „Digital“ und „algorithmisch bestimmt“ werden ausdrücklich nicht gleichgesetzt.

## 14. Unterrichtssequenz im regulären Pfad

Der reguläre Pfad umfasst exakt 225 Minuten. Die Phasen des autoritativen Zeitvertrags werden folgendermaßen auf fünf Unterrichtseinheiten verteilt:

| UE | Minuten | Lernfunktion und Tätigkeit | Gesicherte Spur |
|---|---:|---|---|
| 1 | 15 Orientierung | Mehrdeutigen Lieferauftrag beobachten, widersprechende Ausführungen vergleichen, Leitfrage aufbauen. | gemeinsame Problemfrage |
| 1 | 20 Vorwissen | Alltagsschritte präzisieren, Vorhersagen begründen, Bezug zu bekannten digitalen Arbeitsabläufen herstellen. | flüchtige aufgabenbezogene Vorhersagen |
| 1 | 10 Konzept | Erste Merkmale einer ausführbaren Anweisung sammeln. | gemeinsame Merkmalliste |
| 2 | 25 Konzept | Begriffe Algorithmus, Anweisung, Ausführung, Zustand und Laufspur an einem aktiven Beispiel explizit aufbauen. | gemeinsame Begriffs- und Zustandsdarstellung |
| 2 | 20 angeleitet | Nächste Zustände vorhersagen, Befehle ordnen und eine Lücke ergänzen. | bearbeitetes Beispiel |
| 3 | 25 angeleitet | Fehlerfälle zu Reihenfolge, Drehung, fehlendem Schritt und Wiederholungszahl hypothesengeleitet bearbeiten. | kurze Fehlerbegründungen |
| 3 | 20 Produkt | Eigenständigen Lieferauftrag beginnen: Entwurf und erste strukturierte Vorhersage. | Ausgangsfassung und Vorhersage |
| 4 | 35 Produkt | Algorithmus ausführen, Laufspur prüfen, erste Abweichung lokalisieren, Reparatur testen. | Belegspur und revidierte Fassung |
| 4 | 10 Prüfen/Überarbeiten | Schleifenentscheidung und Reparatur knapp begründen. | begründete Revision |
| 5 | 25 Prüfen/Transfer | Algorithmus-Lupe mit Beispielen, Nichtbeispielen und Grenzfall; Produkt anhand der Kriterien überarbeiten. | Systemklassifikation und Endfassung |
| 5 | 20 Sicherung | Gemeinsame Erklärung der Leitfrage, Begriffe und Modellgrenze; reduzierbarer Selbstcheck. | gesicherte Kriterien und individuelle Endfassung |

Summen über alle UE:

| Vertragsphase | Minuten |
|---|---:|
| Orientierung und Herausforderung | 15 |
| Vorwissen aktivieren | 20 |
| Begriffe und Konzept aufbauen | 35 |
| Angeleitet üben | 45 |
| Eigenständiges Lernprodukt | 55 |
| Prüfen, überarbeiten und transferieren | 35 |
| Gemeinsam sichern | 20 |
| **Gesamt** | **225** |

## 15. Erweiterungspfad mit sechs UE

Der Erweiterungspfad umfasst exakt 270 Minuten und ergänzt reale Ausführungs- und Fehlerkorrekturzeit:

- angeleitet üben: plus 15 Minuten;
- eigenständiges Lernprodukt: plus 20 Minuten;
- prüfen, überarbeiten und transferieren: plus 5 Minuten;
- gemeinsam sichern: plus 5 Minuten.

Die zusätzliche sechste UE verwendet einen bereits vorhandenen, fehlerhaften Algorithmus zu einer neuen, gleichartigen Karte. Lernende müssen:

1. den Endzustand vorhersagen;
2. den Ablauf tatsächlich ausführen;
3. die erste Abweichung lokalisieren;
4. eine Reparaturhypothese formulieren;
5. gezielt revidieren und erneut ausführen;
6. die neue Lösung mit dem eigenen Produkt vergleichen.

Die Erweiterung führt keine neue Kompetenz, keinen neuen Befehl und kein zusätzliches Bewertungsprodukt ein. Mehr Demonstration allein erfüllt den Erweiterungsvertrag nicht.

## 16. Unterstützung und Differenzierung

Hilfen sind aufgabenbezogen, transparent und ohne automatische Personenzuschreibung verfügbar:

- textliche Szenenbeschreibung mit Koordinaten;
- vollständiges bearbeitetes Beispiel;
- teilweise vorgegebener Algorithmus;
- Drehhilfe mit Blickrichtungswechsel;
- ausgeschriebene Darstellung einer Schleife;
- Laufspurtabelle;
- Fragen zum ersten Abweichungspunkt;
- Satzstarter für Reparatur und Begründung.

Lernende oder Lehrkraft wählen Hilfen bewusst. Es gibt kein automatisches Fading anhand von Zeit, Klickzahl, Fehlversuchen oder vermuteter Kompetenz. Hilfenutzung wird weder gespeichert noch exportiert.

Die drei Karten des eigenständigen Lieferauftrags sind gleichwertige Varianten, keine verdeckten Niveaustufen. Eine spätere Differenzierung nach Niveaustufen benötigt einen eigenen Designauftrag.

## 17. Rückmeldung

Rückmeldung folgt einer festen fachlichen Staffelung:

1. Ergebnis benennen: Auftrag erfüllt oder noch nicht erfüllt;
2. verursachenden Schritt und Zustand sichtbar machen;
3. zum Vergleich von Vorhersage und Laufspur auffordern;
4. auf Wunsch einen strategischen Hinweis anbieten;
5. erst auf ausdrückliche Anforderung ein vollständiges Beispiel öffnen.

Rückmeldungen bewerten keine Person. Sie verwenden keine Punkte, Sterne, Ranglisten, Kompetenzampeln oder Lobserien für bloße Interaktion. Fehler werden als erwartbarer Teil von Modellierung und Problemlösen gerahmt.

## 18. Rolle der Lehrkraft und Sozialform

Das Modul ist kein vollständig selbstgesteuerter Onlinekurs. Die Lehrkraft orchestriert:

- den gemeinsamen Präzisionskontrast;
- die explizite Einführung der Fachbegriffe;
- den ersten gemeinsamen Vergleich von Vorhersage und Lauf;
- einen anonymisierten Fehlerfall;
- die gemeinsame Sicherung zu Schleife, Debugging, algorithmisch bestimmten Systemen und Modellgrenze.

Standard ist Einzelarbeit mit kurzen Partnererklärungen. Bei Geräteverhältnis 1:2 werden die Rollen **steuern** und **vorhersagen/prüfen** vergeben und nach jeder Aufgabe gewechselt. Beide Rollen verlangen eine sichtbare fachliche Denkhandlung; eine Person darf nicht dauerhaft nur bedienen.

Wenn ein Produkt oder Selbstcheck fehlt, zieht die Lehrkraft keine Diagnose aus Klick- oder Zeitdaten. Sie gibt einen frischen, kurzen Fall und bittet um Vorhersage, Laufspur und Erklärung des ersten Abweichungspunkts.

## 19. Voraussetzung und Fallback

`IUM-5-CORE-01` wird vorausgesetzt. Das Handbuch benennt die konkret benötigten Routinen, insbesondere sichere Grundbedienung, lokale Arbeitsstände und elementare Navigation in der Lernwerkoberfläche.

Fehlen einzelne Bedienroutinen, bietet das Modul eine kurze Schnittstellenhilfe, ohne Inhalte von `IUM-5-CORE-01` erneut zu unterrichten. Fehlt die fachliche Voraussetzung in einer Lerngruppe breiter, entscheidet die Lehrkraft vor Modulstart über Wiederaufnahme des vorausgesetzten Moduls; das aktuelle Modul kompensiert dies nicht durch zusätzliche verdeckte Unterrichtszeit.

Technische Fallbacks:

- Tastatur- und Schaltflächenbedienung statt Drag-and-drop;
- Textdarstellung von Karte, Zustand und Laufspur statt rein grafischer Darstellung;
- flüchtiger Arbeitsmodus mit Exporthinweis, falls persistente Speicherung nicht verfügbar ist;
- Wiederaufnahme über den vorhandenen Importvertrag;
- bei nicht ausführbarer Kernfunktion kein analoger Ersatz mit behaupteter Gleichwertigkeit, sondern dokumentierter technischer Abbruch und spätere Wiederaufnahme.

## 20. Lokaler Daten- und Exportvertrag

### 20.1 Grundsatz

Alle Daten bleiben im vorhandenen lokalen Plattformvertrag. Das Modul verlangt oder erzeugt keine Namen, Konten, E-Mail-Adressen, Klassenkennungen, Gerätekennungen, Netzwerkkennungen oder personenbezogenen Diagnosedaten. Es gibt kein Backend, keine Telemetrie und keine Drittanbieterrequests.

### 20.2 Persistenter Modulpayload

Der Payload ist versioniert und enthält ausschließlich:

- aktuelle Lernphase und Szenario-ID;
- bestätigte Ausgangsfassung des eigenständigen Algorithmus;
- strukturierte Vorhersage;
- ausgewählte Belegspur;
- Reparaturquelle `eigener Entwurf` oder `standardisierter Einzelfehlerfall`;
- kurze Reparaturhypothese;
- revidierte Algorithmusfassung;
- kurze Schleifenbegründung;
- fallbezogene Systemklassifikationen mit Kurzbegründung;
- Abschlussstände des reduzierbaren Selbstchecks.

Nicht persistent und nicht exportierbar sind:

- Zeitbedarf;
- Anzahl oder Folge fehlgeschlagener Versuche;
- Klick-, Scroll-, Fokus- oder Navigationsdaten;
- Hilfenutzung;
- Wiedergabegeschwindigkeit;
- automatisch abgeleitete Leistungs-, Fähigkeits- oder Personenmerkmale;
- unbestätigte Zwischenläufe und vollständige Bearbeitungshistorien.

### 20.3 Schema und Migration

Der Modulpayload erhält eine eigene ganzzahlige Schemaversion innerhalb des bestehenden `LearningStateEnvelope`. Importdaten werden vor Anzeige und Verwendung vollständig validiert. Migrationen arbeiten auf Kopien, sind deterministisch und testen mindestens:

- Import der aktuellen Version;
- Migration jeder unterstützten Vorgängerversion;
- Ablehnung zukünftiger oder strukturell ungültiger Versionen;
- Erhalt von Ausgangsfassung, Vorhersage, Belegspur, Revision und Begründungen;
- keine Ausführung von Daten als Code.

## 21. Lernnachweis ohne integrierte Diagnostik

Das Modul integriert ausdrücklich keine Diagnostik. Es stellt einen reduzierbaren, aufgabenbezogenen Arbeitsbestand bereit, den Lernende und Lehrkraft im Unterricht fachlich besprechen können.

Der Selbstcheck umfasst genau vier Fragen:

1. Ist jede Anweisung in dieser Situation eindeutig?
2. Passt die Laufspur zu meiner Vorhersage?
3. Bezieht sich meine Reparatur auf die gefundene Abweichung und kann ich sie begründen?
4. Ist meine feste Wiederholung passend – oder ist hier keine Schleife sinnvoll?

Antworten sind `ja`, `noch prüfen` oder `nicht zutreffend`, soweit fachlich möglich. Daraus entstehen keine Punkte, Niveaustufen, automatischen Empfehlungen oder dauerhaften Profile.

## 22. Barrierefreiheit und responsive Nutzung

Die zentrale Lernhandlung muss ohne Maus, Drag-and-drop, Farberkennung, Animation oder visuelles Raster möglich sein.

Verbindlich sind:

- semantische Überschriften, Regionen, Listen, Formulare und Schaltflächen;
- konsistente Fokusreihenfolge und sichtbarer Tastaturfokus;
- vollständige Bedienung per Tastatur und Touch;
- beschriftete Einfüge-, Verschiebe- und Löschaktionen für jeden Algorithmusblock;
- Textäquivalent für Raster, Roboterposition, Blickrichtung, Gut, Ziel und Hindernisse;
- textuelle Laufspur mit Schritt, Befehl, Vorherzustand, Nachherzustand und Ergebnis;
- sichtbare und angemessen angekündigte Änderung des aktuellen Befehls und Ergebniszustands;
- keine Information ausschließlich durch Farbe, Position, Ton oder Bewegung;
- schrittweise Ausführung als Standard und respektierte reduzierte Bewegung;
- Reflow bei 320 CSS-Pixeln und Bedienbarkeit bei 200 Prozent Zoom;
- ausreichend große Touchziele und keine zeitkritische Eingabe.

Das visuelle Raster und die textliche Zustandsdarstellung verwenden dieselbe semantische Quelle. Sie dürfen fachlich nicht auseinanderlaufen.

## 23. Digital-analog-Entscheidung

Für die erste Fassung sind keine analogen Lernendenmaterialien vorgesehen. Das digitale Medium besitzt hier eine eigenständige fachliche Funktion: Es führt eine exakt definierte Semantik aus und koppelt Anweisung, Zustand, Wiederholung, Laufspur und reproduzierbare Revision.

Das Lehrkräftehandbuch ist digital und mediengerecht aufgebaut. Eine Browser-Druckfunktion kann technisch funktionieren, begründet aber keine zweite analoge Materialstruktur. Spätere analoge Materialien benötigen eine eigene, dokumentierte Lernfunktion und einen eigenen Scopeentscheid.

## 24. Technische Architekturgrenze

Das Modul nutzt die bestehende Phase-1-Plattform und ergänzt sie nur um modulspezifische Fachlogik:

- fachliche Quellen und Manifest liegen im regulären Modulbereich;
- der Modulpfad erhält eine statische, explizite Zuordnung zum Renderer `algorithm-workbench`;
- es gibt kein dynamisches Pluginladen und keine Auswahl ausführbaren Codes aus Manifest, Payload oder URL;
- der Interpreter ist eine begrenzte, deterministische Fachfunktion mit geprüften Daten;
- Szenarien, Befehle, Ziele und erwartete Zustände sind statische, validierte Modulressourcen;
- `TEST-PLATFORM-REFERENCE` und sonstige Fixtures bleiben vollständig isoliert;
- eine modulspezifische Komponente wird erst nach einem zweiten realen fachlichen Einsatz als gemeinsamer Plattformbaustein erwogen;
- Änderungen am Plattformvertrag erfordern einen nachgewiesenen, separat getesteten Lernbedarf.

Der Kernpfad funktioniert offline und ohne externe Laufzeit-, Schrift-, Analyse- oder Medienabhängigkeiten.

## 25. Lehrkräftehandbuch

Das Handbuch liefert mindestens:

1. Kompetenzbezug, Leitfrage, Lernziele und Zeitvertrag;
2. fachlichen Hintergrund zu Algorithmus, Anweisung, Ausführung, Zustand, Laufspur, fester Schleife und Modellgrenze;
3. Abgrenzung zu Verzweigung, bedingter Schleife, Variable und freier Programmierung;
4. Voraussetzungen aus `IUM-5-CORE-01` und Schnittstellenfallback;
5. minutierte Fünf-UE-Sequenz und echte Sechs-UE-Erweiterung;
6. Hinweise für Einzelarbeit, Partnererklärung und Geräteverhältnis 1:2;
7. erwartbare Fehler und fachlich geeignete Rückfragen;
8. Erklärungspunkte und gemeinsame Sicherung;
9. Hilfen, Beobachtungskriterien und frische Kurzfälle bei fehlender Evidenz;
10. Bedienungs-, Accessibility-, Speicher-, Offline- und Gerätefallbacks;
11. Datenschutz-, Export-, Lizenz- und Statusgrenzen;
12. klare Aussage, dass keine automatische Diagnose, Punktzahl oder Freigabeentscheidung erzeugt wird.

## 26. OER-, Asset- und Quellenvertrag

- Eigener Programmcode steht unter MIT.
- Eigene Lerntexte, Aufgaben, Szenarien und Grafiken stehen unter CC BY-SA 4.0.
- Alle Assets erhalten maschinenprüfbare Provenienz, Lizenz, Urheberangabe und Änderungsvermerk.
- Externe Assets werden nur verwendet, wenn Lizenz und Offline-Nutzung eindeutig kompatibel sind; für dieses Modul werden eigene einfache Grafiken bevorzugt.
- Der Lieferroboter wird als sachliche, nicht verniedlichende Vektorgrafik ohne Marken- oder Produktähnlichkeit gestaltet.
- Curriculum- und Forschungsbezüge werden aus den vorhandenen Repository-Beständen referenziert; nicht belegte Quellen oder Wirkungsbehauptungen sind unzulässig.

## 27. Qualitätssicherung

### 27.1 Vertrags- und Inhaltsprüfungen

- Manifest entspricht dem Schema und bindet exakt `IUM-5-CORE-05`.
- Die fünf Curriculumrecords, Voraussetzung, `STRAND-A`, `working`, `pilotRequired: true` und der 5/6-UE-Zeitvertrag sind vollständig referenziert.
- Jede Aufgabenfamilie, Lernphase und Produktspur ist vorhanden.
- Keine verbotene Kontrollstruktur oder freie Codeausführung ist erreichbar.
- Keine analoge Doppelstruktur wird ausgeliefert.

### 27.2 Interpreterprüfungen

- jeder Grundbefehl in gültigem Zustand;
- jede Drehung aus allen vier Blickrichtungen;
- feste Wiederholung an Anfang, Mitte und Ende eines Algorithmus;
- minimale und maximale gültige Wiederholungszahl;
- Ablehnung von Verschachtelung, ungültiger Anzahl und leerem Schleifenkörper;
- alle sechs Fehlerzustände;
- identische Laufspur für identische Eingaben;
- Stopp am ersten Fehler und an der Schrittgrenze;
- keine Mutation von Szenariodaten oder Ausgangsalgorithmus.

### 27.3 Lernzyklus- und Datenprüfungen

- Ausführung erst nach strukturierter Vorhersage;
- Schritt- und Gesamtlauf erzeugen semantisch dieselbe Endspur;
- erste Abweichung ist identifizierbar;
- Ausgangsfassung und Revision bleiben unterscheidbar;
- bei einem im ersten Lauf korrekten eigenen Entwurf entsteht die Revisionsspur am standardisierten Einzelfehlerfall;
- nur bestätigte Belegspur wird persistent;
- Hilfenutzung, Zeit und Versuchshistorie erscheinen weder in Zustand noch Export;
- Speichern, Neuladen, Export, Import, Migration und Löschen erhalten beziehungsweise entfernen den vereinbarten Arbeitsbestand verlustfrei;
- ungültige Importdaten verändern den aktiven Stand nicht.

### 27.4 Accessibility-, Browser- und Offlineprüfungen

- vollständiger Kernpfad nur mit Tastatur;
- vollständiger Kernpfad nur mit Touch und ohne Drag;
- Screenreaderpfad für Editor, Zustandsbeschreibung, aktuellen Befehl, Laufspur und Fehler;
- 320 CSS-Pixel, 200 Prozent Zoom, Hoch- und Querformat;
- reduzierte Bewegung und schrittweise Ausführung;
- Offline-Start und vollständiger Kernpfad ohne Netzwerk;
- keine Drittanbieterrequests, Telemetrie, externen Schriften oder Laufzeitimporte;
- kontrolliertes Update ohne Verlust eines gültigen Arbeitsstands.

### 27.5 Reviewgrenzen

Vor Implementierungsabschluss erfolgen getrennte fachliche, didaktische, technische, Accessibility-, Datenschutz- und Lizenzreviews. Diese Reviews belegen interne Qualität, öffnen aber Gate B nicht.

## 28. Definition of Done für Gate A

Die Modulimplementierung darf später nur dann als Gate-A-intern abgeschlossen gelten, wenn:

- regulärer und erweiterter Lernpfad vollständig umgesetzt sind;
- Lernendenmodul und Lehrkräftehandbuch denselben Fach-, Zeit- und Datenvertrag verwenden;
- alle vorgesehenen automatisierten Prüfungen grün sind;
- interne Reviews ohne offene blockierende Befunde abgeschlossen sind;
- Curriculum-, Quellen-, Asset- und Lizenzmapping vollständig sind;
- der öffentliche Arbeitsstand eindeutig `working` ausweist;
- weder Produktkatalog noch LMS noch einsatzbereites Deployment das Modul freigeben;
- `device-verified` weiterhin wahrheitsgemäß `not-run` bleibt.

## 29. Nicht-Ziele

Nicht Bestandteil dieses Auftrags sind:

- Niveaustufendifferenzierung;
- automatische Diagnostik oder Beurteilung;
- Konten, Klassenverwaltung, Lehrkräftedashboard oder Cloudspeicherung;
- Gamification, Punkte, Badges, Ranglisten oder adaptive Personalisierung;
- freie Block- oder Textprogrammierung;
- Verzweigungen, bedingte Schleifen, Variablen oder verschachtelte Schleifen;
- reale Robotik-Hardware;
- analoge Parallelmaterialien;
- Pilotierung, LMS-Integration, produktives Deployment oder Statushochsetzung.

## 30. Implementierungsreihenfolge als Designabhängigkeit

Ein späterer testgetriebener Implementierungsplan muss folgende Abhängigkeit respektieren:

```text
Manifest und modulspezifischer Zustandsvertrag
→ reiner Interpreter und Szenariovalidierung
→ Algorithmuseditor und barrierefreies Zustandsmodell
→ Vorhersage, Ausführung und Laufspur
→ Reparatur, Revision und Produktpersistenz
→ Aufgabenfolge und Systemtransfer
→ Lehrkräftehandbuch, Lizenzen und vollständige QA
```

Dies ist noch kein Ausführungsplan. Dateien, Testfälle, Commitgrenzen und konkrete Implementierungsschritte werden erst nach schriftlicher Freigabe dieser Spezifikation mit `superpowers:writing-plans` festgelegt.

## 31. Bekannte Risiken und Gegenmaßnahmen

| Risiko | Gegenmaßnahme |
|---|---|
| Roboterkontext wird als Spiel statt als Modell gelesen. | Keine Belohnungsmechanik; Fachbegriffe, Zustand und Modellgrenze sichtbar halten; im Transfer Kontext verlassen. |
| Trial-and-error ersetzt Vorhersage und Erklärung. | Vorhersage vor Ausführung, erste Abweichung markieren, Reparaturhypothese vor Revision. |
| Oberfläche überlastet Lernende in Klasse 5. | Begrenzte Befehlssprache, phasenweise Werkzeuge, aktive Beispiele, explizite Erklärung und gemeinsame Sicherung. |
| Drag-and-drop oder Raster schließen Lernende aus. | Gleichwertige Schaltflächen-, Tastatur- und Textpfade aus derselben semantischen Quelle. |
| Arbeitsstand wird zur verdeckten Diagnose. | Nur Produktspuren speichern; keine Zeit-, Versuch-, Klick- oder Hilfedaten; kein Scoring oder Profil. |
| Erweiterungs-UE wird bloße Demonstration. | Verbindliche zusätzliche Vorhersage, reale Ausführung, Fehlerlokalisierung, Reparatur und Vergleich. |
| Klasse-7-Inhalte werden vorweggenommen. | Nur Sequenz und feste Wiederholung; keine Bedingung, Variable, Verschachtelung oder freie Programmierung. |
| Ein grüner Build wird als Einsatzfreigabe missverstanden. | Status `working`, Gate-B-Sperre und `device-verified: not-run` in Manifest, Dokumentation und Oberfläche. |

## 32. Akzeptanzkriterien dieser Spezifikation

- Curricularer Vertrag, Zeitvertrag und Grenzen zu Klasse 7 sind eindeutig.
- Der Fünf-UE-Pfad summiert sich exakt auf 225 Minuten und bildet alle Vertragsphasen ab.
- Die sechste UE enthält zusätzliche Ausführung und Fehlerkorrektur, aber keine neue Kompetenz.
- Lernprodukt, Interaktionszyklus, Aufgabenfamilien und Qualitätskriterien sind vollständig definiert.
- Befehlssprache, Zustand, Fehlersemantik, Persistenz und Migration sind implementierbar beschrieben.
- Lehrkraftrolle, Hilfen, Feedback und gemeinsame Sicherung sind festgelegt.
- Keine integrierte Diagnostik, Telemetrie, Personalisierung oder analoge Doppelstruktur entsteht.
- Tastatur-, Touch-, Screenreader-, Text-, Reflow- und Offlinepfad sind gleichwertige Anforderungen.
- OER-, Lizenz-, Fixture- und statische Architekturgrenzen sind eindeutig.
- Gate B bleibt geschlossen und der Modulstatus bleibt `working`.

## 33. Schriftliches Freigabegate

Mit der schriftlichen Freigabe werden fachlich-didaktischer Lernpfad, Interaktionsmodell, Unterrichtszeit, Produkt- und Datenvertrag, technische Grenzen und Qualitätssicherung für `IUM-5-CORE-05` verbindlich.

Die Freigabe erlaubt als nächsten Schritt ausschließlich die Erstellung eines testgetriebenen Implementierungsplans. Sie erlaubt noch keine reale Pilotierung, LMS-Einbindung, Produktveröffentlichung oder Hochstufung des Modulstatus.
