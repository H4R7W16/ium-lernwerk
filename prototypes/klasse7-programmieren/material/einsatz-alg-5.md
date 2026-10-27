# ALG-5 · Durchführungsplan für den ersten Unterrichtseinsatz

**90 Minuten · Lehrerimpulse, Hilfen und Anschlussdiagnose.** [Briefing als Vorlesetext](alg-5-briefing.html) · [Zur Lernaufgabe](../lernende/alg-5.html)

## Ziel und Rahmen

„Dein Rover, dein Härtetest“: Die Lernenden planen und bauen eine eigene begrenzte Steuerung mit Bewegung, passender Wiederholung und Meldungsverzweigung. Sie prüfen Normalfall, Grenzfall und einen **selbst gewählten Überschreitungsfall**, reagieren auf einen fremden Start und verbessern eine konkrete Stelle begründet.

Grundlage sind die [Lernendenfassung 2.0](../lernende/alg-5.html), der [Reihenkommentar](durchfuehrung-256.html) und der [Jahrgangsbrief](jahrgang.html). **15 + 15 + 40 + 20 = 90 Minuten**; weiterhin **405 Programmierminuten innerhalb der 36 Jahres-UE**. Eigene Wahl zwischen Station 60/80, Schrittweite 10/15 und zwei klaren Meldungen bleibt erhalten. Die Zahlen dürfen direkt im Code stehen; eigene Variablen oder Funktionen werden nicht verlangt.

ALG-3/4 liefern Wahrheitswerte, Verzweigung, vorangestellte Abbruchprüfung und null Bewegungen. Deren tatsächliche Rückmeldung vorher prüfen. Diagnose, Geräteverteilung und reale Bearbeitungszeit sind noch unbekannt; der Ablauf setzt startbereite, ausreichend bedienbare Geräte voraus. Er ist eine Erprobungsplanung. Bildungsplanbezug: vorhandene Projektgrundlage mit der dokumentierten Anhörungsfassung vom 21.09.2026, keine neue Aussage zum verbindlichen Planstatus oder zu einer Fachprofilfreigabe.

**Gebündeltes Lernprodukt:** zwei Sätze zu den eigenen Regeln, eigener grafischer Ablaufplan, eine Testliste mit drei eigenen Fällen, kurzer fremder Test sowie eine Zeile „Änderung – Grund – neuer Test“ und eigene XML. Alles kann auf derselben Werkstattnotiz stehen. Kein zusätzliches Aufgabenheft, Spielprojekt, Video oder neues Abgabeformular.

## Vorbereitung und Material

- [Lernaufgabe ALG-5](../lernende/alg-5.html) und [zugehöriges Startprojekt](https://h4r7w16.github.io/ium-lernwerk/klasse7/programmieren/snap/lernwerk.html?aufgabe=alg-5) bereithalten. Das Projekt enthält nur grüne Flagge, Startort 0/0 und Richtung 90°. **Starten fährt zunächst nicht:** Die Steuerung muss selbst gebaut und angehängt werden. Beide Stationslinien sind bereits sichtbar; eine eigene Bühne ist nicht nötig.
- Arbeitsnotiz/Papier, Projektion von Mini-Fall und tatsächlichem Code bereithalten. Für Hilfen: Bewegung, Steuerung, Operatoren und Aussehen sind in der Lernwerk-Ansicht erreichbar. „Mehr Werkzeuge“ erhält das Projekt. Keine vollständige Beispiellösung vor dem eigenen Plan zeigen.
- Modell: positive Schritte nach rechts, Richtung 90°. Vor der Station weiterfahren, **an oder hinter ihr keine weitere Bewegung**. Erst danach passende Meldung zum aktuellen Endort wählen. Start-x, Zielzahl und Schrittweite getrennt zeigen; gleiche Zielzahl in den relevanten Prüfungen beibehalten. Den Endort am numerischen x-Wert unten ablesen, nicht allein an den nah beieinanderliegenden Stationslinien.
- **Nicht jeden Normalfall als Treffer erwarten:** Station 80/Schritt 15 endet von 0 bei **90/„vorbei“**. Bei Station 80/Schritt 10 sind **acht erwartete Bewegungen** richtig. Die Grenze von sechs gilt für **unerwartete** Bewegungen. Bei Abweichung möglichst sofort Stopp, spätestens nach sechs unerwarteten Bewegungen. Unklare neue Programme vor dem Start im Schrittmodus untersuchen; Bedienklicks sind nicht Bewegungen.
- **Datei speichern → Datei öffnen** auf dem vorgesehenen Safari-Schulgerät vorher erproben. Ablage und neutrale Kennung vereinbaren: `ALG-5_Kennung.xml`. Beim Ersetzen eines geänderten Projekts kann eine Rückfrage erscheinen; gewünschte aktuelle Arbeit vorher sichern. Ein Download allein ist noch keine erfolgreiche Rückkehr.
- Bei Partnergeräten beide an Plan und Code beteiligen, Bedienrollen wechseln und jede Person selbst vorhersagen und begründen lassen. Gemeinsame Datei allein belegt keine Einzelkompetenz. Fehlende eigene Bedien-/Dateihandlungen offen halten; die Zeitannahme ersetzt keine Geräteplanung.

## Verlauf · 90 Minuten

| Zeit | Lehrperson und konkreter Impuls | Lernhandlung und Beobachtung |
|---|---|---|
| **0–3** | „Dein Rover soll auch bei einem ungewohnten Start richtig reagieren. Welche Regel muss gelten, bevor er einen Schritt macht?“ | Auftrag in eigene Worte fassen. Start an oder hinter der Station nicht als Sonderfall ausblenden. |
| **3–10** | „Wähle 60 oder 80, Schritte von 10 oder 15 und zwei verständliche Meldungen. Woran erkennt dein Testteam genau getroffen oder vorbei?“ Noch keine fertige Codefassung vorgeben. | Eigene Entscheidungen in zwei Sätzen festhalten. Meldungen müssen fachlich unterscheidbar sein, nicht vorgegebenen Wortlaut kopieren. |
| **10–15** | Einige Regeln hören: „Passt deine Meldung auch, wenn ein Schritt über die Station führt? Was muss bei Start genau am Ziel passieren?“ | Erwartungen schärfen: null Bewegungen am/hinter dem Ziel. Die genaue Endposition der eigenen Normalfahrt bleibt zunächst eigene Vorhersage. |
| **15–20** | Gemeinsam nur den Mini-Fall klären: „Bei 25 und Marke 30: fahren oder stoppen? Und bei 30 oder 35? Welche Frage entscheidet danach die Meldung?“ | 25: weiter; 30/35: stoppen. Genau getroffen und vorbei getrennt beurteilen. Kein komplettes 60/80-Programm gemeinsam bauen. |
| **20–30** | „Zeichne deinen Ablauf. Wo liegt die Frage vor der Bewegung? Wohin führt der Rückweg? Wo verzweigen die Meldungen?“ Bei Bedarf leere Raute statt fertigem Plan anbieten. | Eigener grafischer Plan mit Fragen, bezeichneten Ausgängen, Rückweg und Ende. Passende Wiederholung selbst wählen; Plan muss zur eigenen Regel passen. |
| **30–40** | Startprojekt öffnen: „Baue zuerst den Teil, der über Fahren oder Stoppen entscheidet.“ Nach etwa zehn Minuten Plan und ersten Code kurz zeigen lassen. | Eigenen Plan in Code umsetzen. Bei Partnergeräten Bedienrolle wechseln. Lehrperson prüft nicht nur Zahl der Blöcke, sondern Ort der Prüfung und Rückweg. |
| **40–50** | Beim Rundgang: „Woher weiß das Programm, dass es stoppen darf? Wann wählt es die Meldung? Stimmen deine Zielzahlen zusammen?“ Gestufte Hilfe nur an konkreter Hürde geben. | Steuerung fertigstellen, Plan/Code abgleichen. Bewegung, passende Wiederholung und Verzweigung sind vorhanden; keine feste Bewegungszahl nur aus dem Normalfall ableiten. |
| **50–55** | „Sage zuerst Endort und Meldung für Start 0 voraus. Prüfe dann.“ Bei 80/15 ein korrektes „vorbei“ nicht als Fehler werten. | Erste Zeile der vorhandenen Testliste: eigene Erwartung vor dem Lauf, tatsächliche Beobachtung danach. Eine Abweichung erklären und gezielt neu prüfen. |
| **55–60** | „Teste genau an deiner Station. Darf sich der Ort ändern? Welche Meldung passt?“ | Zweite Testzeile: null Bewegungen, unveränderter Ort, Treffer-Meldung. Ein scheinbar richtiger Normalfall allein genügt nicht. |
| **60–65** | „Wähle selbst einen anderen Start vor deinem Ziel, bei dem die Schrittfolge darüber hinausführt. Begründe vor dem Lauf, warum er ein guter Gegenfall ist.“ Noch keine Startzahl an alle verteilen. | Dritte Zeile: eigener Start, begründete Erwartung, tatsächliche Beobachtung. Der Fall muss die Marke überspringen; Start am Ziel ersetzt ihn nicht. |
| **65–70** | „Sichere deinen jetzigen Stand und halte fest, welche Stelle noch offen ist.“ Kein neues Formular. | Zwischenstand als XML speichern, Notiz und Code erhalten. Dieser Download ersetzt nicht die abschließende Rückkehr zur verbesserten Datei. |
| **70–74** | Fremden zusätzlichen Startwert austauschen, Erwartung zunächst individuell. Wenn Start bereits hinter dem Ziel bisher nicht belegt ist, diesen Fall für den Fremdtest wählen lassen; der konkrete Wert bleibt frei. Allein stellt die Lehrperson den Gegenfall. | Auf den fremden Start am eigenen Programm reagieren. Kurzen Eintrag direkt unter die vorhandene Liste setzen, keine neue Volltabelle. |
| **74–80** | „Prüfe den fremden Start. Erkläre am Plan, warum die beobachtete Meldung passt. Was darf bei einem Start schon hinter der Station nicht geschehen?“ | Fremdtest ausführen und erklären. Hinter der Station: null Bewegungen, gleicher Ort, Vorbei-Meldung. Auch nicht bedienende Partnerperson befragen. |
| **80–85** | „Verbessere eine konkrete Stelle an Code, Plan oder Meldung. Was änderst du, warum und welcher Test prüft das?“ Korrektes Programm muss nicht absichtlich kaputtgemacht werden. | Eine begründete Revision samt erneutem passenden Test. Bei korrektem Code etwa eine präzisere Meldung oder einen unklaren Planpfeil verbessern. Zeile „Änderung – Grund – neuer Test“. |
| **85–90** | Kurz sichern: „Erst Fahrentscheidung, danach Meldungsentscheidung.“ **Nur Start auf 0 zurückstellen; eigene Station und Schrittweite behalten.** Verbesserte Datei speichern, wieder öffnen und Normalfall erneut prüfen. | Eigene Werte, Meldungen und Revision wiedererkennen; richtige Normalfallerwartung kontrollieren. Bei 80/15 bleibt 90/„vorbei“ richtig. Datei-Rückkehr und fehlende Realhandlungen getrennt dokumentieren. |

Die vierzig Minuten Eigenphase enthalten regulär ungefähr **20 Minuten Bauen, 15 Minuten Tests und 5 Minuten Zwischensichern**. Die letzten zwanzig Minuten sind bereits Teil der 90 Minuten, kein Zusatzblock.

## Lösungen, Kriterien und Sicherung

Eine mögliche Struktur: **wiederhole bis nicht (x-Position < eigene Zielzahl)** mit Bewegung; danach **falls x-Position = eigene Zielzahl**, Treffer-Meldung, sonst Vorbei-Meldung. Andere passende Kontrollstrukturen akzeptieren, wenn vor der Bewegung entschieden wird, die Meldung stimmt und die Startfälle nachvollziehbar erfüllt sind. Eine pauschale feste Anzahl von Bewegungen für Start 0 reicht bei verändertem Start nicht. Lösung erst nach eigenem Versuch besprechen.

| Eigene Station / Schritt | Normalfall ab 0 | Bewegungen | Meldungsbedeutung |
|---|---|---|---|
| 60 / 10 | 0 → 10 → … → 60 | 6 | genau getroffen |
| 60 / 15 | 0 → 15 → 30 → 45 → 60 | 4 | genau getroffen |
| 80 / 10 | 0 → 10 → … → 80 | 8 | genau getroffen |
| 80 / 15 | 0 → 15 → 30 → 45 → 60 → 75 → 90 | 6 | vorbei; trotzdem korrekt |

Start **am Ziel**: sofort stoppen, keine Bewegung, Treffer-Meldung. Start **bereits dahinter**: sofort stoppen, keine Bewegung, Vorbei-Meldung. Beim gewählten `bis`-Muster lautet die letzte Abbruchprüfung wahr; die anschließende Gleichheitsfrage entscheidet die Meldung. Das sind zwei verschiedene Aufgaben der Bedingungen.

**Eigener Gegenfall:** Ein Start knapp vor der eigenen Station, dessen nächste Schritte sie überspringen. Beispiel nur nach eigener Wahl oder als gezielte Hilfe: Station 60, Schritt 10, Start 55 → 65/„vorbei“; auch 59 wäre geeignet. Bei 80/15 etwa 79 → 94/„vorbei“. Nicht alle Lernenden auf dieselbe Beispielzahl festlegen. Ein falscher Gleichheitsabbruch würde von solchen Starts aus weiterlaufen. Das muss nicht ungebremst ausgeführt werden.

**Zentrale Sicherung auf Tafel/Projektion und vorhandener Notiz:** „Vor jeder Bewegung entscheiden, ob noch gefahren werden darf. An oder hinter der Station stoppen. Danach genau getroffen oder vorbei unterscheiden. Ein guter Test hat eine Erwartung vor dem Lauf, eine Beobachtung und eine Erklärung.“ Dazu ein selbst erarbeitetes Planbeispiel mit Rückweg und Meldungsverzweigung; eigene Pläne bleiben erhalten. Die [ALG-5-Sicherung](sicherung.html) erst nach den eigenen Versuchen zum Abgleich nutzen, nicht vorzeitig als Bauvorlage. Der öffentliche Lehrpersonenbereich ist kein geschützter Test.

## Hürden und nächste Hilfe

| Beobachtung | Passender nächster Impuls |
|---|---|
| Starten fährt im Startprojekt nicht. | „Welche Blöcke sind schon da, welche Steuerung musst du selbst ergänzen?“ Reset ist vorhanden, Fahr- und Meldeteil fehlen noch. |
| Plan zeigt Bewegung vor der ersten Frage. | Start genau am Ziel durch den Plan verfolgen. „Welche Bewegung wäre dort schon zu viel?“ Leere Prüfraute anbieten, keinen vollständigen Plan vorgeben. |
| x = Ziel als Abbruch scheint im Normalfall zu reichen. | „Welcher selbst gewählte Start überspringt deine Station?“ Erst den Gegenfall begründen; bei Bedarf Start knapp davor anregen. |
| Wahr/falsch bzw. Abbruch/Fortsetzen verwechselt. | „Bei bis heißt wahr: Ende. Welche Antwort brauchst du schon am Ziel?“ Mit dem Mini-Fall 30/30 klären, danach eigene Frage erneut anwenden. |
| Immer dieselbe Meldung oder Meldung vor dem Anhalten. | „Welche Frage unterscheidet genau getroffen und vorbei am aktuellen Endort?“ Ort der Meldungsentscheidung prüfen. |
| Normalfall 80/15 endet 90/„vorbei“. | „War der Rover bei 75 noch davor? Wo steht er nach einem weiteren erlaubten Schritt?“ Als korrekte Wahl anerkennen, nicht auf Schritt 10 zurücksetzen. |
| Programm bei insgesamt sechs Schritten gestoppt. | Erwartete und unerwartete Bewegungen trennen. 80/10 benötigt acht erwartete Schritte. Sobald die Beobachtung abweicht, stoppen und begründen. |
| Nur eine von zwei relevanten Zielzahlen wurde geändert. | „Beurteilen Fahr- und Meldungsfrage dieselbe Station?“ Werte mit dem eigenen Zwei-Satz-Vertrag abgleichen. |
| Schreiben oder Darstellung blockiert. | Leere Start-/Frage-/Endeformen, Pfeile oder eine leere Testzeile anbieten. Satzanfänge: „Mein Gegenfall ist geeignet, weil …“, „Ich ändere …, damit …; mein neuer Test ist …“. Mündliches Erklären zulassen. |

**Schrittmodus** bei unklarem Ablauf vor dem Start einschalten; tatsächliche x-Änderungen statt Klicks zählen. Bei Fehlerlauf Stopp vor Moduswechsel. Eine alte Sprechblase kann aus einem früheren Lauf stehen bleiben; allein daraus keinen aktuellen Testerfolg ableiten. Den numerischen Ort, den Codeweg und den beendeten Lauf zusammen betrachten.

Sichere Lernende können freiwillig einen zweiten begründeten Gegenfall oder eine andere gültige Steuerung vergleichen. Kein zusätzliches Spiel, keine Variablenpflicht und keine vierte eigene Pflicht-Testliste.

## Diagnose und Anschluss an ALG-6

Zwei individuelle Kriterien aus dem bestehenden Mapping: **eigene begrenzte Steuerung mit Anweisung, passender Wiederholung und Verzweigung umsetzen** sowie **Normal-, Grenz- und Gegenfall begründet prüfen und eine Verbesserung erneut testen**. Plan, Code, Testliste und Revisionszeile tragen diese Kriterien gemeinsam; kein zusätzlicher Kompetenzbogen nötig.

**Regulärer Anschluss:** Die Person erklärt vorangestellte Fahrprüfung und nachfolgende Meldungsentscheidung, begründet den eigenen Überschreitungsfall und den fremden Start, erkennt am/hinter dem Ziel null Bewegungen und belegt eine konkrete Revision samt Test. Kopierte Beispiellösung, Partnerdatei oder ein richtiger Normalfall allein genügen nicht. Individuelle Kurzfrage: „Welche Stelle würde versagen, wenn dein Rover schon hinter der Station startet?“

**Gezielte Nachsicherung:** Bei fehlender erster Prüfung zunächst einen Start am Ziel ohne Lauf verfolgen, bei unklarer Meldung dieselbe Endposition durch die Meldungsfrage führen. Danach mit einem veränderten Start selbst erklären lassen. Fehlen individuelle Belege oder gelang die eigene Umsetzung noch nicht, vor ALG-6 gezielt nachsichern; dessen fremde Codeanalyse setzt die Grundlagen voraus. Geräte-/Dateiprobleme getrennt von fachlichen Lücken notieren. Nicht beobachtete Bedienung bleibt offen, auch wenn das Teamprodukt korrekt ist.

## Zeitraster, Ausfall und Rückfluss

**Variante 45 + 45 Minuten:** 0–43 wie oben; 43–45 laufenden Versuch beenden und Zwischenstand speichern. Nach der Pause 45–48 öffnen, 48–55 fertigbauen, 55–67 die drei Tests, 67–70 Zwischensichern. 70–90 bleiben unverändert. Damit stehen weiterhin 20 Minuten fürs eigentliche Bauen zur Verfügung; Tests werden auf zwölf und spätes Zwischensichern auf drei Minuten verdichtet, weil die zusätzliche Datei-Rückkehr innerhalb der Eigenphase liegt. Eingeübte Dateiroutine ist Voraussetzung; kein offener Tab oder fortsetzbarer Programmlauf über die Pause wird vorausgesetzt. Die Variante ist noch nicht zeitlich erprobt.

Bei Verzögerung zuerst freiwillige Vertiefung und zusätzliche Plenumsbeiträge streichen. Eigene Steuerung, begründeter Gegenfall und tatsächliche Revision schützen. Unvollständige Datei-Rückkehr, fehlende Implementation oder Diagnose ausdrücklich offen halten und gezielt nachholen. Zusatzunterstützung nach [Jahrgangsbrief](jahrgang.html) im bestehenden Konto von **135 Unterstützungsminuten** buchen; keine heimliche Verlängerung von 90 auf 105 Minuten und keine Doppelbuchung. Bei Partnergeräten tatsächliche Bedienanteile und Zeitverlust berücksichtigen.

Bei Geräteausfall Regeln, grafischen Plan und Testvorhersagen auf Papier bearbeiten, gegebenenfalls Demonstrationslauf nutzen. Eigene Implementation und Datei-Rückkehr sind damit nicht nachgewiesen. Größerer Verlust verlangt neue Anschlussplanung anhand der tatsächlichen Lage.

**Kompakter WU-Check:** Eigene Parameter und begründete Gegenfälle aktivieren Denken (Band 1); konkrete Hürden steuern gestufte Hilfen (Band 3); eigene Lösung, Peer-Rückmeldung und erneuter Test erhalten den fachlichen Anspruch (Band 6). Redaktionelle Planungsprüfung, kein Wirksamkeitsnachweis. Nach Einsatz tatsächliche Minuten, belegte Einzelumsetzung, Test-/Revisionsbegründung, Hilfe und Datei-Rückkehr dokumentieren; nächsten Schritt vor ALG-6 entscheiden und Briefing bei Ablaufänderungen mitführen.
