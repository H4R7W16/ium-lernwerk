# Rover-Werkstatt · Durchführung ALG-1, ALG-3 und ALG-4

**Fassung 2.0 · Klasse 7 · 195 Minuten.** Zusammen mit ALG-2/5/6 bleiben es 405 Minuten und 36 Jahres-UE. Zeiten sind Planungsannahmen; Lernzeit und Motivation sind noch nicht im Unterricht erprobt. Digitales Primärmaterial, kurze eigene Notizen auf Papier oder im bekannten Dokument. Kein zusätzliches Aufgabenheft erforderlich.

## Vorbereiten und steuern

Direkte Lernwerk-Links öffnen die bereits geladenen Startdateien. „Starten“ ist die grüne Flagge; ALG-1 verwendet lose Stapel. Beschriftete Aktionen „Schrittmodus“, „Ein Schritt“, „Stopp“, „Datei speichern“ und „Datei öffnen“ vorführen. In XML eingebettete SVG-Bühnen markieren die Stationen; sie erzeugen keine externen Abrufe. Die Pfeilfigur bleibt ein Bewegungsmodell, kein realer Roboter. Positive Schritte, Richtung 90°, x wächst nach rechts.

Lösungen erst nach eigenem Versuch besprechen; der öffentliche Lehrpersonenbereich ist kein Zugriffsschutz. Jede Person führt eine eigene knappe Werkstattnotiz. Bedienhilfe und Fachhilfe unterscheiden, ohne daraus eine Note zu berechnen. Bei fehlendem Vorwissen vor der abhängigen Aufgabe nachsichern; tatsächliche Zusatzzeit im vorhandenen Unterstützungskonto buchen. Keine zweite stille Pufferstunde.

## ALG-1 · Route zur Station 20 · 45 Minuten

| Phase | min | Lernhandlung / nächster Blick |
|---|---|---|
| Erklärung | 10 | Klammerreichweite, Start und Ziel; beide Endorte vorher vermuten. |
| Gelenkt | 10 | A ausführen und einzelne Positionen erklären. |
| Eigene Anwendung | 15 | B mit integrierter Ablaufskizze; eigene feste Route nach 20. |
| Rückmeldung/Revision | 10 | Skizze abgleichen, B-Variante mit drei Fünferschritten, Datei-Rückkehr. |

**Erwartung:** A 0→10→20→30, B 0→10→15→20; jeweils einmal „Ende“. Für eigenes A sind etwa 2×10, 4×5 oder 5×4 gültig. Nicht nur den Endort prüfen: Die feste Wiederholungszahl und einzelne Bewegung müssen erklärt werden. B-Variante: 0→10→15→20→25. Ein gleiches Ende beweist keinen gleichen Weg.

**Beobachtung → Hilfe:** Werden alle Zahlen miteinander multipliziert, Klammer markieren und den Rumpf ausschreiben lassen. Stimmt nur der Endwert, eine Zwischenposition erläutern lassen. Bei sicherem Einstieg eigene Route früher entwickeln lassen; gemeinsamer Gegencheck bleibt.

**Produkt:** eine Ablaufskizze mit Positionen, eigene Route, kurze Erklärung des neuen Falls und XML; keine separate zweite Volltabelle.

## ALG-3 · Depotentscheidung bei 40 · 75 Minuten

| Phase | min | Lernhandlung / nächster Blick |
|---|---|---|
| Erklärung | 15 | Zwei Bedingungen bei 30/40/50 vergleichen. |
| Gelenkt | 15 | Fehlenden Meldungszweig ergänzen, 40 und 30 prüfen. |
| Eigene Anwendung | 30 | Erste Frage selbst wählen, Zweige begründen, Plan mit Tests 39/40/41. |
| Rückmeldung/Revision | 15 | Frage umkehren, Zweige passend neu zuordnen; sichern und wieder öffnen. |

`x < 40` ergibt bei 30/40/50 wahr/falsch/falsch; `nicht (x > 40)` wahr/wahr/falsch. Letzteres bedeutet kleiner oder gleich und passt an der Grenze nicht zu „Depot A“. Ausgangsregel: 39→A, 40→B, 41→B. Wer zuerst „an oder hinter 40?“ fragt, kann `nicht (x < 40)` verwenden und muss im Wahrzweig B melden. Logisch gleichwertige Lösungen akzeptieren; keine Bewegung.

**Beobachtung → Hilfe:** Bei falscher Grenzmeldung zuerst den Wahrheitswert, danach den Zweig nennen lassen. Startposition und Regelgrenze getrennt markieren. Eine gezeichnete Entscheidungsraute kann gleichzeitig die drei Testeinträge tragen; kein zweites Ablaufprotokoll verlangen.

## ALG-4 · Haltestelle 40 reparieren · 75 Minuten

| Phase | min | Lernhandlung / nächster Blick |
|---|---|---|
| Erklärung | 15 | Feste Anzahl gegen vorangestellte Abbruchprüfung. |
| Gelenkt | 15 | Starts 0/40/45 vorhersagen, begrenzt ausführen. |
| Eigene Anwendung | 30 | Nur Abbruchbedingung reparieren; eine volle Prüfspur und zwei erste Prüfungen. |
| Rückmeldung/Revision | 15 | Fall 35/12 vorhersagen und prüfen; Ausgangsdatei sichern und wieder öffnen. |

Fehler `x = 40`: Start 0 endet nach vier Bewegungen bei 40; Start 40 braucht null. Start 45 erreicht mit positiven Zehnerschritten die 40 nie. Fehlerlauf nach spätestens vier Bewegungen stoppen. Feste vier Wiederholungen bewegen dagegen bei jedem Start viermal.

Korrektur beispielsweise `nicht (x < 40)`. Start 0: Prüfungen 0/falsch, 10/falsch, 20/falsch, 30/falsch, 40/wahr. Start 40 und 45: erste Prüfung wahr, keine Bewegung. Variante Start 35/Schritt 12: Ende 47, eine Bewegung, zwei Prüfungen. `x > 40` allein wäre am Start 40 noch falsch. „fertig“ folgt erst nach dem Schleifenende.

**Beobachtung → Hilfe:** Fortsetzungsfrage „noch davor?“ von Abbruchfrage trennen. Bei fehlender letzter Prüfung den Zeitpunkt der Meldung verfolgen. Neue Ablaufgrafik entfällt hier bewusst: Die Prüfspur trägt das Schleifenverständnis; eigenständiger grafischer Plan bleibt in ALG-5 und grafisch verfolgter fremder Ablauf in ALG-6 erhalten.

## Sicherung und Rückfluss

Für die Besprechung stehen die [Sicherungskarten](sicherung.html) bereit. Nach Durchführung knapp festhalten: tatsächliche Minuten, belegte Erklärung, Hilfe, offener nächster Schritt. Nicht beobachtete Ausführung als offen lassen. Peer-Gegencheck hat ein konkretes Objekt; allein übernimmt die Lehrperson. Ein Projektimport oder eine kopierte Lösung ersetzt keine eigene Erklärung.
