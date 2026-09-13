# M06 Reinigungsfall: Sauber geplant

> Stand: 13.09.2026. Portable Lesefassung der gleichnamigen fachlichen Vault-Notiz. [Entscheidungsstand und nächste Schritte](README.md). Die Planungsdokumentation ist keine Einsatz- oder Produktfreigabe.

## Auftrag und Stand

Der Nutzer hat den Reinigungsroboter als M06-Anwendung gewählt und die konkrete Fortsetzung beauftragt. Dieser Entwurf spezifiziert den Lernfall einschließlich Grundrissen, Musterlösungen, Fehlern, Lernprodukten und einer lokalen interaktiven Vorschau. Die didaktische Ausgestaltung steht zum Review; eine Nutzerentscheidung über alle Details oder empirische Lernwirkung liegt noch nicht vor.

Der interaktive Konzeptprototyp liegt im Workspace unter `Shared/Prototypes/ium-v2-ux01/reinigungsfall.html` und ist dort auch über die lokale Vorschau erreichbar. Die Seite funktioniert auch direkt als Datei. Der bisherige Prüffahrt-Entwurf bleibt für den Vergleich erhalten. Der produktive M06-Fachkern und seine alten Dossier-/Zielverträge werden hier nicht ersetzt.

## Lernfrage und fachlicher Ertrag

**Wie planen und prüfen wir die Fahrt so, dass wirklich die ganze Bodenfläche gereinigt wird?**

Nach einer Bastelaktion liegen Papierkrümel auf einer freien Bodenfläche. Alle Lernenden bekommen dieselbe vereinfachte Raumsituation. Niemand muss einen Roboter besitzen oder seine Wohnung beschreiben. Die Aufgabenfläche liegt neben dem Basteltisch; Möbel stehen zunächst außerhalb. Das ist eine konstruierte Lernsituation, kein Herstellerauftrag oder tatsächlich durchgeführter Reinigungstest.

Lernende sollen Anweisung, Reihenfolge, Anfangszustand und feste Wiederholung erklären, eine Ablaufgrafik selbst ergänzen beziehungsweise erstellen, eigenen Code ausführen und eine Korrektur anhand einer Spur begründen. Sie unterscheiden **„entspricht meiner Absicht“**, **„läuft ohne Kollision“** und **„erfüllt den Reinigungsauftrag“**. Ein Roboter am Start ist noch kein Beleg für eine saubere Fläche.

Der Fall trägt damit eine fachliche Denkbewegung: vom Verstehen einzelner Zustandsänderungen über korrekte Gruppierung zu einem selbst gewählten vollständigen Ablauf. Die Oberfläche zeigt den fachlichen Zustand durch Blickpfeil, Krümel, Häkchen, Koordinaten und erreichte Kacheln.

## Reihen- und Bildungsplananschluss

Planungsanker ist `V2-G5-M06` mit **225 Minuten / fünf Einheiten à 45 Minuten**. Voraussetzung laut Jahrgangsroadmap ist M01; S0 überprüft die tatsächlich benötigten Bedien- und Darstellungsroutinen, statt sie als vorhanden anzunehmen. Es gibt noch keine konkret durchgeführte Lerngruppe, keine vorhandene Lerndiagnose und keinen festgelegten Stundenabstand. Dies ist Lehrwerksentwicklung, keine Anschlussstunde an vermeintlich schon durchgeführten Unterricht.

Das lokale allgemeine Unterrichtsplanungsmodul besitzt noch kein eigenes IuM-Fachprofil. Als begrenztes Arbeitsprofil gelten die vorhandene V2-Lernarchitektur, das M06-Referenzdesign und die Jahrgangsplanung: präzise Zustandsbegriffe, Darstellungswechsel, individueller Code, begründete Revision und Transfer. Daraus wird kein neuer allgemeiner Fachstandard abgeleitet.

| Vorhandener Record | Beitrag dieses Falls | Grenze |
| --- | --- | --- |
| BMB16-GYM-PK-SK-001 | Begriffe wie Anweisung, Körper, Durchlauf und Zustand an eigenen Produkten erklären. | Querschnittlicher Teilbeitrag; amtliche BMB-Quelle. |
| LH26-E-ALG-001 | Funktionsbeschreibungen von Zeitsteuerung/Wegberechnung untersuchen; Vorschrift, Ausführung und System unterscheiden. | Lesehilfe als Orientierung für 5/6, keine zusätzlich behauptete amtliche Norm. |
| LH26-E-ALG-002 / 003 | Präzisen Anfangszustand erklären, Ablaufgrafik ergänzen und selbst erstellen, Befehle ausführen. | Eine bloße Ortslinie genügt nicht als Ablaufgrafik. |
| LH26-E-ALG-004 / 005 / 006 | Feste Körper und Anzahl verstehen, eigenen Code programmieren und Spur analysieren. | Papier allein belegt keine praktische Programmierung. |

Die Record-Zuordnung stammt aus `roadmap/v2/grades/grade-5/curriculum-map.json`; Abdeckung bleibt `unassessed`. Der neue Flächenauftrag ersetzt die alten S3-Wegpunkte nicht stillschweigend. Vor einer Produktintegration müssen Lernprodukte, Prüfkriterien, Aufgabenfassungen und Belegversionen ausdrücklich auf den neuen Fall umgestellt werden.

## Modellregeln

1. Die gesamte rechteckige Fläche ist befahrbar. Kacheln sind eine Abstraktion gleich großer Bodenstücke, keine maßstabsgerechten Raummaße.
2. Koordinaten: Spalten von links nach rechts, Zeilen von oben nach unten. Der Startzustand nennt Ort und Blickrichtung.
3. `vor` fährt genau eine Kachel in Blickrichtung. `links` und `rechts` drehen am Ort um 90 Grad. Ein Drehen ist eine Aktion, aber keine weitere gereinigte Kachel.
4. Jede besuchte Kachel gilt im Modell als gereinigt; das Startfeld zählt von Beginn an. Mehrfaches Besuchen erhöht die Zahl verschiedener gereinigter Kacheln nicht. Während eines Laufs wird nichts wieder schmutzig.
5. `wiederhole n [ … ]` führt den gesamten Körper n-mal aus. Anzahl 2–9, Körper 1–5 Grundbefehle, keine Verschachtelung. Mehrere Wiederholungsblöcke nacheinander sind erlaubt. Nach 100 ausgeführten Aktionen wird gestoppt.
6. Ein Schritt über den Rand stoppt die Fahrt. Ort, Blick und gereinigte Felder ändern sich bei diesem fehlgeschlagenen Versuch nicht. Er wird als versuchte Aktion in der Spur sichtbar.
7. Reinigungserfolg bedeutet: reguläres Programmende, kein Randfehler/Schrittlimit und alle vereinbarten Felder erreicht. Für S3 kommt mindestens eine feste Wiederholung hinzu. Endort und Endblick sind frei. Die Rückkehr zur Station und kürzere Wege sind mögliche Zusatzkriterien.
8. Das Modell kennt keine Sensoren, Variablen, Bedingungen, Schmutzerkennung, Akkulaufzeit oder Reinigungsqualität. Es ist keine Simulation einer konkreten Roomba-Software. Ein neu aufgestellter Stuhl wird im Kern nicht heimlich als neue Simulationsfunktion eingeführt.

## Drei Grundrisse

Alle Punkte sind zu reinigende Kacheln; `R→` ist die bereits gereinigte Startkachel. Der Basteltisch liegt außerhalb der gezeigten Fläche.

```text
A · erste Befehle / Wiederholung     B · Klammer / Flächendeckung
      1    2                              1    2    3
  1   ·    ·                         1   ·    ·    ·
  2   R→   ·                         2   ·    ·    ·
                                     3   R→   ·    ·

C · eigener Entwurf
      1    2    3    4
  1   ·    ·    ·    ·
  2   ·    ·    ·    ·
  3   R→   ·    ·    ·
```

A hat 4 Kacheln, B 9, C 12. Das Vergrößern öffnet eine neue Planungsentscheidung, ohne neue Bewegungsregeln zu benötigen. Komplexe Möbellabyrinthe würden diese erste Lernfrage unnötig verlagern und sind hier nicht vorgesehen.

## Aufgaben und Lernprodukte

### S0 / P0 – Drei Befehle verstehen

**Lernendentext:** „Auf der freien Bodenfläche liegen Papierkrümel. Unser Modellroboter startet bei (1,2) und blickt nach rechts. Lies `vor; links; vor`. Welche Kacheln erreicht er? Wo steht er danach und wohin blickt er? Halte eine Vorhersage oder Unsicherheit fest. Prüfe Schritt für Schritt.“

Erwartung: Nach `vor` (2,2)/rechts; nach `links` gleicher Ort, Blick oben; nach dem zweiten `vor` (2,1)/oben. Drei von vier Kacheln erreicht, (1,1) bleibt offen. Der Einstieg verlangt ausdrücklich noch keine vollständige Reinigung. Die Lehrkraft modelliert bei Bedarf einen einzigen Zustandswechsel mit einer Spielfigur; die übrigen erklären Lernende.

Diagnose: Kann die Person Ort und Blick unterscheiden und eine Kachel benennen? Wenn nicht, vor der Wiederholung ein neues Zweibefehlsbeispiel mit Figur bearbeiten. P0 ist eine Diagnose, keine Note.

### S1 / P1 – Den ganzen Körper wiederholen

Auf Fläche A gilt `wiederhole 4 [vor; links]`. Nach zwei Aktionen steht der Roboter (2,2)/oben, nach vier Aktionen (2,1)/links. Nach acht Aktionen sind alle vier Felder besucht; Endzustand (1,2)/rechts. An den Stopps müssen Lernende den nächsten Befehl und den Zustand begründen.

**Eigenes Produkt:** Auf Papier die Ablaufgrafik `Start → wiederhole 4 [vor; …] → Ende` ergänzen, den ganzen Körper umrahmen, Anzahl 4 notieren und zwei aufeinanderfolgende Zustände erklären. Die Antwort `links` allein genügt nicht. Eine Spurzeichnung ergänzt die Ablaufgrafik; sie ersetzt deren Befehlsreihenfolge und Körpergrenze nicht.

Sicherung: Vier Durchläufe mit je zwei Aktionen ergeben acht Aktionen. Nur Bewegungen können weitere Kacheln erreichen. Anzahl der Codezeilen, Zahl ausgeführter Aktionen und Zahl verschiedener besuchter Kacheln sind unterschiedliche Größen.

### S2a / P2 – Eine falsche Gruppierung korrigieren

Absicht auf Fläche B: viermal denselben Körper ausführen, nämlich zwei Kacheln vorfahren und links drehen. Fehlercode:

```text
wiederhole 4 [vor; vor]
links
```

**Lernendentext:** „Vergleiche die Absicht mit dem Code. Sage seine Fahrt voraus. Prüfe ab Aktion 1, wann zuerst ein anderer Befehl ausgeführt wird als beabsichtigt. Verändere die Klammer und begründe deine Änderung an dieser Spurstelle.“

Handgeprüfter Erwartungshorizont: Aktion 1 erreicht (2,3), Aktion 2 (3,3), jeweils Blick rechts. In Aktion 3 versucht der tatsächliche Code erneut `vor` und stoppt am Rand. Beabsichtigt ist in Aktion 3 `links`, also (3,3)/oben. Es reicht nicht zu sagen „er fährt gegen die Wand“: Die Körpergrenze lässt das Drehen erst nach sämtlichen Wiederholungen folgen.

Korrektur: `wiederhole 4 [vor; vor; links]`. Diese Fassung beendet 12 Aktionen ohne Kollision bei (1,3)/rechts. Sie entspricht der Randfahrt, reinigt aber erst acht von neun Kacheln. Diese offene Frage führt zu S2b. Kein grünes Gesamturteil „Aufgabe gelöst“ vergeben.

### S2b / P2 – Die Absicht selbst verbessern

**Lernendentext:** „Der Roboter kommt wieder am Start an. Reicht das für unseren Reinigungsauftrag? Markiere die besuchten Kacheln. Prüfe deine Vermutung und ergänze einen Weg zu den ausgelassenen Kacheln. Zeige an einer Spurstelle, warum deine Änderung hilft.“

Fehlende Kachel: (2,2). Eine mögliche begrenzte Revision ergänzt hinter dem vorhandenen Randplan:

```text
vor
links
vor
```

Nach Aktion 13: (2,3)/rechts, weiterhin 8 Kacheln. Aktion 14: gleicher Ort, Blick oben, weiterhin 8. Aktion 15: (2,2)/oben, jetzt 9 Kacheln. Die Fahrt ist vollständig; Rückkehr zur Station wird nicht verlangt. Diese Lösung dient dem Erwartungshorizont und wird nicht vorab als Schülerlösung angezeigt.

P2 besteht aus einer vor dem jeweiligen Lauf erfassten Erwartung, Codefassung, relevanter Spurstelle, eigener Erklärung und Vergleich zur Revision. S2a begründet die Gruppierung, S2b die Abdeckung. Technischer Lauf und Lehrkrafturteil über die Erklärung bleiben getrennt. Eine spätere Codeänderung darf einen bereits ausgewählten Vorherbeleg nicht überschreiben.

### S3 / P3 – Eine eigene Fläche reinigen

**Lernendentext:** „Plane die Reinigung der Fläche C. Beginne bei (1,3), Blick rechts. Zeichne zuerst deine eigene Ablaufgrafik mit Befehlen, Wiederholungskörper und Anzahl. Schreibe unabhängig davon deinen Code. Nutze mindestens eine feste Wiederholung. Sage erreichte Felder und Endzustand voraus. Prüfe, verbessere bei Bedarf und belege zwei entscheidende Stellen.“

Erfolgskriterien: alle 12 Kacheln erreicht, reguläres Programmende ohne Kollision/Schrittlimit, feste Wiederholung vorhanden. Die Erklärung muss zeigen, warum zwischen Teilflächen richtig gewechselt wird und warum Grafik und Code dasselbe bedeuten. Unterschiedliche Endpositionen und Lösungen sind zulässig.

Eine mögliche Zeilenlösung (nur Erwartungshorizont):

```text
wiederhole 3 [vor]
links
vor
links
wiederhole 3 [vor]
rechts
vor
rechts
wiederhole 3 [vor]
```

Sie hat 15 Aktionen, erreicht 12 Kacheln und endet (4,1)/rechts. Wichtige Stellen: Aktion 3 erreicht (4,3); Aktion 5 wechselt nach (4,2); Aktion 10 dreht bei (1,2) nach oben; Aktion 11 erreicht (1,1). Erklärung: Beim Wechsel nach einer nach links durchfahrenen Zeile sind Rechtsdrehungen nötig. Einfach zweimal dieselbe Linkswende würde zurück in die vorige Zeile führen.

Eine zweite zulässige Lösung reinigt spaltenweise: `links; wiederhole 2 [vor]; rechts; vor; rechts; wiederhole 2 [vor]; links; vor; links; wiederhole 2 [vor]; rechts; vor; rechts; wiederhole 2 [vor]`. Sie hat 18 Aktionen und endet (4,3)/unten. Beide Lösungen wurden ausgeführt; keine ist als einzig richtige oder global kürzeste Lösung vorgegeben.

Zusatz bei sicherem Verständnis: Zwei funktionierende Pläne nach Zahl ausgeführter Aktionen und mehrfach besuchten Kacheln vergleichen. „Weniger Codezeilen“ bedeutet nicht automatisch „weniger gefahrene Kacheln“. Eine Rückkehrpflicht verändert den Auftrag und braucht eine neue Prüfung.

### P4 – Später abrufen und nach einer Pause fortsetzen

Zu Beginn eines späteren Termins wird der alte Code zunächst verdeckt. Lernende notieren einen Körper mit mindestens zwei verschiedenen Grundbefehlen, entfalten zwei Durchläufe, erklären einen Zustand und markieren Unsicherheit. Erst danach vergleichen sie. Ein heute geklickter Vergleich belegt kein Behalten über mehrere Tage; der tatsächliche Abstand wird bei Erprobung protokolliert.

Bei kurzer Unterbrechung genügt eine Rückkehrnotiz: offener Punkt und nächste Handlung. Ohne verfügbare Abrufdiagnose zeigt die Lehrkraft einen neuen Zweibefehlsfall und lässt Ort/Blick begründen, bevor eigenständig weitergearbeitet wird.

### S4 / P5 – Transfer in ein anderes Zustandsmodell

Die Prüfstation beginnt **frei**. `aufnehmen`: frei → belegt; `prüfen`: belegt → geprüft; `ablegen`: geprüft → frei. Verglichen werden A: `3 × [aufnehmen; prüfen; ablegen]` und B: `3 × [aufnehmen]; 3 × [prüfen]; 3 × [ablegen]`.

Lernende führen drei Aktionen beider Fassungen von Hand aus und begründen die erste unmögliche Aktion. A ergibt belegt, geprüft, frei und kann weiterlaufen. B ergibt zunächst belegt; das zweite `aufnehmen` ist bereits unmöglich. Die Übertragung liegt im vollständigen Körper, nicht im Austauschen eines Robotersymbols. Kein Einbau von `wenn` oder Sensorbefehlen in die Robotersprache.

### S5 / P6 – Systemeinordnung und Modellgrenze

Vier Funktionsbriefe bleiben erhalten: Zeitsteuerung vergleicht Uhrzeit und Startzeit; Wegberechnung verarbeitet Start, Ziel und Verbindungen; Papier enthält eine Vorschrift; ein Standbild zeigt nur Roboter und Zahlen. Lernende benennen für die ersten beiden einen notwendigen Verarbeitungsschritt und begründen, warum Papier nicht selbst ausführt und das Standbild keine ausreichenden Aussagen zum Algorithmus erlaubt.

Zusätzlicher Ausblick: Ein Stuhl wird nach der Planung auf die Fläche gestellt. Unser festes Programm kennt diese Änderung nicht. Sensorinformationen und programmierte Bedingungen wären ein späterer Ansatz; das ist der Anschluss an G7-M03 und optional den LMZ-ComThink-Putzroboter. Der vollständige Hardwareaufbau ist nicht Teil der 225 Minuten.

## Zeit, Unterstützung und Diagnose

Die folgende Aufteilung erhält die fünf vorhandenen Zeitkomponenten exakt. Sie ist eine zu erprobende Planung, keine gemessene Bearbeitungszeit. Keine zusätzliche Pflichtzeit für eine Robotervorführung oder Hardware.

| Einheit | Orientierung/Erklärung | Angeleitet | Eigenständig | Feedback/Revision | Sicherung/Transfer | Schwerpunkt |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 20 | 20 | 0 | 0 | 5 | S0, erster Körper, Ort/Blick-Diagnose |
| 2 | 5 | 15 | 10 | 10 | 5 | Eigene P1-Grafikergänzung, S2a |
| 3 | 5 | 10 | 10 | 15 | 5 | P4 vor Wiederanzeige, S2b, Beginn eigener Planung |
| 4 | 5 | 5 | 30 | 5 | 0 | Eigene Grafik/Code für S3, gezielte Rückmeldung |
| 5 | 0 | 5 | 10 | 10 | 20 | S3 abschließen, S4-Transfer, S5-Systemeinordnung |
| **Summe** | **35** | **55** | **60** | **40** | **35** | **225 Minuten** |

Lehrkraft führt die erste Bewegung vor; bei Drehen nur den Blickpfeil ändern. Gestufte Hilfen behandeln zuerst Ort/Blick, dann den gesamten Körper, schließlich Teilflächen und einen Begründungssatz. Eine Lösung wird nicht durch einen grünen Haken vorweggenommen. Sprachliche Alternative: auf Felder und Befehle zeigen und mündlich erklären; die fachliche Erwartung bleibt dieselbe.

Nach 5–10 Minuten eigenständiger Arbeit prüft die Lehrkraft bei Bedarf ein Minimalprodukt: Anfangszustand und eine erklärte Spurstelle, später eine Teilflächenidee. Keine größere Expertengruppenstruktur erforderlich. Alle erstellen eigene P1/P3-Produkte. Ein kurzer Vergleich ist freiwillig ergänzend; daraus wird kein individueller Nachweis automatisch abgeleitet.

Bei Geräteausfall: Grundrisse und Befehle aus dieser Notiz ausdrucken, Spielfigur und Markierungen nutzen, Vorhersage/Spur manuell halten. Die praktische digitale Ausführung bleibt dann offen. Fehlende oder unsichere P0/P4-Diagnose führt zu einem kurzen neuen Zustandsbeispiel vor dem selbstständigen Entwurf.

## Material und Quellen

Die Grundrisse, Codes, Aufgaben und Illustration sind eigens erstellte didaktische Modelle. Ein Foto oder Herstellervideo ist keine Voraussetzung für den Kernweg. Die vorhandene [iRobot-Beschreibung des Roomba 205](https://answers.irobot.com/en-GB/knowledge/20501) dient nur als freiwilliger Realitätsanker. Der erneute Textabruf am 13.09. lieferte keinen Seitenkörper; hier werden daraus keine zusätzlichen technischen Gerätebehauptungen abgeleitet. Frühere Quellensichtung steht in der Kontextnotiz.

Fachlicher Abgleich: `packages/v2-g5-m06/src/model.ts`, `validation.ts`, `interpreter.ts`, M06-Referenzspezifikation und Jahrgangsroadmap im Repo. Didaktische Orientierung: „Unterrichtsplanung - Manifest“ (interne Vault-Referenz), „Jan - Pädagogisches Profil“ (interne Vault-Referenz), „IBBW WU Band 1 - Grundlagen wirksamer Unterricht“ (interne Vault-Referenz), „IBBW WU Band 6 - Aufgaben im Fachunterricht“ (interne Vault-Referenz), „IBBW WU Band 3 - Konstruktive Unterstuetzung“ (interne Vault-Referenz). Die lokalen Exzerpte wurden gelesen; keine erneute Volllektüre aller PDFs behauptet.

## Prüf-Gates und WU-Check

- Planungsanker: bestehendes M06, Zeit und Sprachgrenzen gesichert; konkrete Lerngruppe und Stundenabstand noch offen.
- Kognitive Aktivierung: eigener Zustandsvergleich, falsche Gruppierung, unvollständige Flächendeckung, eigener Entwurf und neuer Transferzustand.
- Unterstützung/Zugänglichkeit: kurze Regeln sichtbar; Ort/Blick getrennt; stufenweise Hilfe, Textalternative zur Farbcodierung, Papiergrafik und mündliche Erklärung.
- Aufgabenqualität: Reinigung verändert das Erfolgskriterium. Mehrere Lösungen sind möglich, ein kürzester Weg ist keine versteckte Pflicht.
- Feedback/Diagnose: technische Folgen von eigenem Code werden sichtbar; Erklärungen benötigen fachliches Urteil. P0/P4 und ihr Fallback steuern die nächste Unterstützung.
- Klassenführung: bekannte freie Fläche, feste Regeln und kleine Entscheidungen; Lehrkraft kann Phasen gemeinsam führen, Navigation bleibt offen.
- Ausspielkanal: lokale interaktive HTML-Vorschau, weil Ausführung und Spur die Lernhandlung unterstützen; LearningView wird hier nicht produktiv angelegt.
- Quellen/Modell: Eigenkonstruktion transparent, kein ungesicherter Herstelleralgorithmus. Curriculumzuordnung bleibt ein geplanter Beitrag.
- Wichtigste Erprobungsfrage: Verstehen Lernende den Unterschied zwischen korrekter Randfahrt und erfülltem Reinigungsauftrag und nutzen sie dieses Verständnis bei einer neuen Fläche?

## Umsetzung und nächste Entscheidung

Der lokale Prototyp zeigt alle Lernschritte, prüft freie Eingaben in der begrenzten Sprache und hält Vergleichsbelege im Arbeitsspeicher. Die Ablaufgrafik bleibt ein eigenes Papierprodukt; ein digitaler Grafikeditor, dauerhaftes Speichern, Wiederherstellung und produktive Belegmigration sind nicht Teil dieser Vorschau. Historische UX01-Belege beziehen sich weiterhin auf den damaligen Stand.

Vor einer Produktumsetzung den Lernfall fachlich sichten, die Eingabeverlässlichkeit aus U0 mitberücksichtigen und den neuen Flächen-/Belegvertrag konkret beschließen. Anschließend produktive Umsetzung und echte Lernerprobung separat planen. Die normale Fakefinder-Version und optionalen ComThink-Anwendungen bleiben unverändert im übergeordneten Plan.
