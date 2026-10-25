# Rover-Werkstatt · Durchführung ALG-2, ALG-5 und ALG-6

**Fassung 2.0 · Klasse 7 · 210 Minuten.** Mit ALG-1/3/4 weiterhin 405 Minuten innerhalb der 36-UE-Planung. Das Inhaltsmapping bleibt Grundlage. Fachliche Ziele sind erhalten; Dokumentation wird zusammengeführt. Keine Durchführung, gemessene Motivation oder reale Bearbeitungszeit behauptet.

## Vorbereiten und Zugang

Neue Lernwerk-Ansicht, deutsche Blöcke, vorbereitete XML, bekannte Notizmöglichkeit und schulischer Ablageort. Direkter Link lädt bereits. „Starten“ setzt den jeweiligen Flaggenstapel in Gang, lose Blöcke werden angeklickt. „Schrittmodus“/„Ein Schritt“ und „Datei speichern“/„Datei öffnen“ entsprechen der Oberfläche. „Mehr Werkzeuge“ erhält das Projekt. Vor dem Verwerfen eigener Änderungen sichern. Downloadablage auf dem Zielgerät prüfen.

ALG-3/4 müssen vor ALG-5 verstanden sein. Bei Lücken kurze Nachsicherung und veränderten Prüffall durchführen, Zeit aus dem gemeinsamen Unterstützungskonto buchen. Die 30 Minuten spätere Code-Wiederaufnahme sind kein zweites Förderkonto. Jede Person erklärt selbst; Lehrdateien sind öffentlich und kein gesicherter Prüfungsbereich. Sachliche Hilfe dokumentiert die Lehrperson knapp, ohne daraus automatische Kompetenz- oder Personeneinstufung abzuleiten.

## ALG-2 · Wert und Wirkung · 60 Minuten

| Phase | min | Schwerpunkt |
|---|---|---|
| Erklärung | 15 | Ausdruck liefert Wert; Anweisung bewirkt Bewegung. |
| Gelenkt | 15 | Drei Tabellenzeilen, Zahl/Text/Wahrheitswert. |
| Eigene Anwendung | 20 | Eingabe 7→9; eigene Rechnung für 12 und Zustand lesen. |
| Rückmeldung/Revision | 10 | Zeile präzisieren, Vergleich 8>8→9>8; Datei-Rückkehr. |

`5+7`: Eingaben 5 und 7, Rückgabe 12/Zahl. `gehe(5+7)`: erhält 12, verändert bei Richtung 90 den Ort; kein einsetzbarer Rückgabewert. `sage Ziel`: Eingabe „Ziel“/Zeichenkette, Wirkung Textanzeige, kein einsetzbarer Rückgabewert. `8>8`: falsch/Wahrheitswert; `9>8`: wahr. Inneres 7→9 ergibt 14, die lose Rechnung bleibt 12. Eigene passende Rechnungen sind etwa 3×4, 6+6, 15−3. `x-Position` zeigt nach Reset 0, nach eigener Zwölferbewegung 12; keine sichtbare Eingabe, Zustandszugriff.

**Beobachtung → Hilfe:** Ergebnisblase eines Ausdrucks von `sage` unterscheiden. Inneren und äußeren Block markieren; Eingabe des äußeren Blocks ist Ergebnis des inneren. Eine eigene Tabellenzeile und kurze Vorher-/Nachhernotiz genügen; keine parallele zweite Erklärungssammlung.

## ALG-5 · Eigene Steuerung und Gegenfall · 90 Minuten

| Phase | min | Schwerpunkt |
|---|---|---|
| Erklärung/Klärung | 15 | Ziel 60/80, Schritt 10/15, verständliche Meldungen wählen. |
| Gelenkt | 15 | Entscheidung am Mini-Fall 25/30/35, dann eigener grafischer Plan. |
| Eigene Anwendung | 40 | Bauen 20, drei Tests 15, Sichern 5; kurzer Blick nach 10. |
| Rückmeldung/Revision | 20 | Fremden Startwert prüfen, begründet verbessern, Datei-Rückkehr. |

**Vertrag:** Nur fahren, solange x vor dem Ziel liegt. Bei Erreichen oder Überschreiten nicht weiterfahren. Anschließend genau getroffen/vorbei unterscheiden, auch bei Start am oder hinter dem Ziel. Positive Schritte, Richtung 90; keine eigenen Variablen/Funktionen nötig. Beide Stationslinien sind im Hintergrund beschriftet.

Beispiel: `wiederhole bis nicht(x < Ziel)` mit Bewegung, danach `falls x = Ziel ... sonst ...`. Andere passende Kontrollstrukturen akzeptieren, wenn Wiederholung, Verzweigung und alle Startfälle verständlich nachgewiesen sind. Eine pauschale feste Anzahl genügt bei veränderten Starts nicht.

Normalfallwerte: Ziel 60/Schritt 10→60, 60/15→60, 80/10→80, 80/15→90. Am Ziel null Bewegungen. Der dritte Test ist selbst zu entwickeln: ein gültiger Start knapp vor dem Ziel, dessen Schrittfolge es überspringt. Zum Beispiel Ziel−1 oder Ziel−5 bei den vorgesehenen Schrittweiten. Begründung vor Ausführung verlangen; den Startwert nicht vorweg an alle verteilen. Ein solcher Gegenfall deckt den falschen Gleichheitsabbruch auf. Bei unerwarteten Bewegungen spätestens nach sechs stoppen; acht erwartete Schritte bei Ziel 80/Schritt 10 bleiben korrekt.

**Zwei Individualkriterien aus dem Mapping:** eigenes begrenztes Problem mit Anweisung, Verzweigung und passender Wiederholung implementieren; Normal-, Grenz- und Fehler-/Gegenfall begründet prüfen und überarbeiten. Grafischer Plan, eine Testliste und eine konkrete Revision tragen diese Kriterien. Der zusätzliche fremde Startwert ist der kurze neue Fall im bestehenden Rückmeldefenster, keine Zusatzstunde. Wenn der Code korrekt ist, begründete Klarstellung von Meldung/Plan akzeptieren; keinen Fehler erfinden lassen.

## ALG-6 · Eine Codekarte statt doppelter Dokumentation · 60 Minuten

| Phase | min | Schwerpunkt |
|---|---|---|
| Neue Erklärung | 0 | Voraussetzung aus ALG-1 bis ALG-5; bei Lücken vorher nachsichern. |
| Gelenkt | 10 | Vorlage erklären und nur Start/ersten festen Durchlauf anlegen. |
| Eigene Anwendung | 35 | Grafische Spur 10, kurze Randnotizen 7, Ausführen/Reparatur/Variante 18. |
| Rückmeldung/Revision | 15 | Kritischen Schritt erklären, fester Teil 3 statt 2, sichern/wieder öffnen. |

Die [Ablaufvorlage](../bilder/alg6-codekarte.svg) wird klein skizziert oder ausgedruckt und individuell ergänzt. Positionsfolgen, letzte Abbruchprüfung und wahr/falsch gehören direkt an die betreffenden Schleifen-/Zweigstellen. Die ergänzte grafische Karte ist gleichzeitig Laufspur und Ablaufdarstellung; keine zweite Volltabelle oder neu gestaltete Grafik verlangen. Alle vier Grundbausteine müssen am Ablauf erklärt werden. Bei Bedarf ist eine kurze mündliche Erläuterung mit Lehrpersonennotiz gleichwertig; die individuelle erste Spur bleibt erhalten.

**Erwartung:** Fehlerfassung: Start 0, fester Teil 10/20, bedingt 30/40/50/60, Abbruch bei 60, Meldung „vorbei“. Vier bedingte Bewegungen und letzte Prüfung 60>wahr. Bei 50 ist 50>50 falsch – entgegen dem Ziel „erreicht oder überschritten“. Korrektur `nicht(x < 50)` oder gleichwertig: drei bedingte Bewegungen, Ende 50/„Ziel“. Die Fehlerhypothese muss die Prüfung an 50 erklären.

**Kurze Randnotizen, fünf Codezeilen:** `10` ist Zahl und Ausdruck ohne Operator; `5+5` erhält 5/5, liefert 10/Zahl, Operator+; die äußere Bewegung erhält 10, verändert den Ort und gibt keinen einsetzbaren Wert zurück. `x-Position` nach festem Teil:20/Zahl, keine sichtbare Eingabe, kein Rechen-/Vergleichsoperator. `x>50` bei 50: falsch/Wahrheitswert, Vergleich>. `sage Ziel`: übergebene Zeichenkette, Textanzeige statt einsetzbarer Rückgabe. Nicht zu fünf langen Aufsätzen erweitern.

**Varianten:** Wählt ein Kind 12, ergibt die reparierte bedingte Folge 20→32→44→56/„vorbei“; bei 15:20→35→50/„Ziel“. Vorhersage und Beobachtung gegenüber dem Zehnerlauf erklären. Neuer Kurzfall mit festem Teil 3×10 und bedingt 10:30→40→50/„Ziel“, drei feste und zwei bedingte Bewegungen. Bei erster Reparaturhilfe diesen Kurzfall ohne eingeblendete Lösung erklären lassen. Exportierte Abschlussfassung wieder 2 feste Durchläufe und bedingt 10.

### Elf Kriterien bleiben in derselben Codekarte sichtbar

| Mappingkriterium | Fundstelle des Individualbelegs |
|---|---|
| 1 Anweisung beschreiben | Bewegung in Spur erläutern; Wirkung/Rückgabe in Randnotiz trennen. |
| 2 Feste Wiederholung beschreiben | Erste Positionsfolge und geänderte feste Durchlaufzahl. |
| 3 Bedingte Wiederholung/Abbruch beschreiben | Vorangestellte und letzte Prüfung, Grenzhypothese und Reparatur. |
| 4 Verzweigung beschreiben | wahr/falsch an zwei Ausgängen, gewählte Meldung erklären. |
| 5 Ausdrucksarten unterscheiden | Literal 10/Zustand, Rechnung 5+5, Vergleichx>50. |
| 6 Übergabe/Rückgabe identifizieren | Innere Rechnung, äußere Bewegung und sage-Zeile. |
| 7 Zahl, Zeichenkette, Wahrheitswert identifizieren | Randnotizen zu 10/5+5, Ziel, x>50. |
| 8 Schrittweise analysieren | Individuelle Positionsspur bis zur letzten Prüfung. |
| 9 Ablauf darstellen und Wirkung erklären | Ergänzte Grafik mit Rückwegen/Zweigen und Erklärung der Meldung. |
| 10 Übergebene Werte gezielt ändern | Selbst gewählte bedingte Schrittweite 12 oder 15 tatsächlich einsetzen. |
| 11 Vorhersagen, ausführen, vergleichen | Erwartung/Beobachtung der Variante, begründeter Vergleich zum Zehnerlauf. |

Nr 1–5 beziehen sich auf 3.2.3.1(1), Nr 6 auf(2), Nr 7 auf(3), Nr 8–9 auf(5), Nr 10–11 auf(6). Weniger doppelte Darstellung bedeutet keine Streichung dieser Ziele. Pro Kriterium knapp selbstständig/nach Hilfe/weiterer Bedarf/nicht beobachtet festhalten. Keine Gesamtnote aus Dateiabgabe oder Klicks.

## Sicherung, Zeit und Pilotierung

[Sicherung](sicherung.html) nach eigenem Versuch nutzen. Rückmeldung nennt eine konkrete Stelle und einen nächsten Schritt. Tatsächliche Zeit bei ALG-4/6 besonders erfassen;405 Minuten sind weiterhin eine zu prüfende Annahme. Größere Lücken transparent über Unterstützung/Puffer beziehungsweise eine neue Kapazitätsentscheidung bearbeiten. Nach Durchführung in den Jahrgangsbrief Minuten, Hilfe und nächsten Auftrag zurückmelden. Safari/Touch, Offline und Verbindungen bleiben getrennte Geräteprüfungen.
