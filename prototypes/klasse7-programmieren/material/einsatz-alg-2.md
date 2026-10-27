# ALG-2 · Durchführungsplan für den ersten Unterrichtseinsatz

**60 Minuten · Lehrerimpulse, Hilfen und Anschlussdiagnose.** [Briefing als Vorlesetext](alg-2-briefing.html) · [Zur Lernaufgabe](../lernende/alg-2.html)

## Ziel und Rahmen

„Gleiche Zahl – gleiche Wirkung?“: Die Lernenden unterscheiden **einen Ausdruck, der einen Wert liefert**, von **einer Anweisung, die etwas bewirkt**. Sie verfolgen, wie das Ergebnis einer eigenen Rechnung zur Eingabe des Bewegungsblocks wird. Zahl, Zeichenkette und Wahrheitswert werden an konkreten Beispielen unterschieden.

Grundlage sind die Lernendenfassung 2.0, [Reihenkommentar und Lösungen](durchfuehrung-256.html) und der [Jahrgangsbrief](jahrgang.html). Station **x = 12**, Snap! in der Lernwerk-Ansicht, **15 + 15 + 20 + 10 Minuten**. Die Reihe bleibt bei **405 Programmierminuten innerhalb der 36 Jahres-UE**. Aufgaben und Startprojekt werden nicht verändert. Bildungsplanbezug: vorhandene Projektplanung auf Basis der dort dokumentierten Anhörungsfassung vom 21.09.2026; keine neue Aussage zum verbindlichen Planstatus.

ALG-1 liefert den Anschluss über Programmlesen und Vorhersagen. Vor dem Einsatz dessen tatsächliche Rückmeldung prüfen; bei fehlender Grundlage gezielt nachsichern. Lerngruppe, Geräteverteilung und Dateiroutine sind noch unbekannt. Der Verlauf setzt startbereite Geräte voraus; 60 Minuten und fünf Minuten Datei-Rückkehr sind Planwerte, keine gemessenen Unterrichtsergebnisse.

**Ein bestehendes Notizprodukt genügt:** vier Tabellenzeilen, eine knappe Vorher-nachher-Notiz und die eigene Berechnung im Projekt. Vorhersagen bleiben lesbar; Korrekturen werden ergänzt. Kein weiteres Arbeitsblatt, Protokoll oder zusätzlicher Upload. Die Lehrperson hört auch individuelle Erklärungen.

## Vorbereitung und Material

- [Lernaufgabe ALG-2](../lernende/alg-2.html) öffnen und den dortigen Projektlink nutzen. [Startprojekt in Snap!](https://h4r7w16.github.io/ium-lernwerk/klasse7/programmieren/snap/lernwerk.html?aufgabe=alg-2) vorab auf einem Schulgerät prüfen. **Starten** setzt hier x und y auf 0 sowie die Richtung auf 90°. Es führt die losen Rechen- und Bewegungsblöcke nicht aus. Nach dem Zurücksetzen erst den gewünschten losen Block anklicken.
- Vor jeder Bewegung zurücksetzen. Die Stationsgrafik allein unterscheidet x = 12 und x = 14 kaum; den numerischen x-Wert unten am Bühnenrand ablesen. Einen ruhenden Block am Namen/Operator erkennen, nicht an einer festen Bildschirmposition.
- Im Startprojekt liegen **zwei getrennte „5 + 7“**: eine Rechnung im Bewegungsblock und eine lose Rechnung. Außerdem ist **„3 × 4“ bereits vorbereitet**. Das bei Hilfen und Bewertung berücksichtigen.
- Die bestehende [ALG-2-Sicherung](sicherung.html) für den späteren Abgleich bereithalten. Projiziert werden Lernaufgabe, tatsächlicher Code und anschließend die kurze Sicherung; eine zusätzliche Präsentation ist nicht nötig.
- **Datei speichern → Datei öffnen** vorher in Safari auf dem eingesetzten Gerät erproben; Ablage und neutrale Kennung vereinbaren. Zielname: `ALG-2_Kennung.xml`. Keine Anmeldung und keine Veröffentlichung von Schülerprojekten nötig.
- Bei Partnergeräten übernimmt zunächst eine Person die Bedienung, die andere prüft die Vorhersage. Zur eigenen Rechnung wechseln. Beide halten die vier Zeilen und die neue Vorhersage selbst fest und erklären selbst.

## Verlauf · 60 Minuten

| Zeit | Lehrperson und konkreter Impuls | Lernhandlung und Beobachtung |
|---|---|---|
| **0–3** | Station 12 zeigen. „Heute geht es um eine Zahl und darum, was das Programm mit ihr macht.“ Starten, x = 0 und Richtung 90° prüfen. | Ziel verstehen; lose Rechnung und Bewegungsblock finden. Keine erste Bewegung ohne geklärten Ausgangsort. |
| **3–7** | „Was passiert bei einem Klick auf die lose Rechnung 5 + 7? Und was beim Bewegungsblock? Vermute für beide, was sichtbar wird und wo der Rover steht.“ Noch nicht ausführen. | Jede Person notiert zwei kurze Vorhersagen. Auch „beides ist 12“ als Ausgangsvermutung zulassen und nach der Bedeutung fragen. |
| **7–12** | Erst die lose Rechnung anklicken: „Wo erscheint 12? Hat sich x verändert?“ Danach zurücksetzen und den blauen Bewegungsblock anklicken: „Was macht dieser mit der 12?“ | Rückgabewert 12 bei unverändertem x = 0 mit Wirkung x = 12 vergleichen. Am Rand ablesen, statt nur auf die Figur zu schauen. |
| **12–15** | „Die Rechnung liefert einen Wert. Die Bewegung verwendet diesen Wert als Eingabe und ändert den Ort.“ Inneren und äußeren Block zeigen lassen. | Begriffe Ausdruck, Anweisung, Eingabe und Rückgabewert am Beispiel klären. Eine unpassende Vorhersage mit Begründung korrigieren. |
| **15–22** | Erste zwei Tabellenzeilen gemeinsam füllen: „Welche Eingaben erhält die Rechnung? Welche Zahl erhält die Bewegung von ihr?“ Vor jeder Bewegung zurücksetzen. | `5 + 7`: Eingaben 5 und 7, Wert 12, Typ Zahl. Bewegung: Eingabe 12, Wirkung x: 0 → 12. Der innere Ausdruck bleibt im Programm stehen. |
| **22–26** | „Bearbeite sage Ziel als dritte Zeile selbst. Was erhält der Block? Liefert er einen einsetzbaren Wert oder zeigt er etwas an?“ Danach kurz vergleichen. | „Ziel“ als Zeichenkette und sichtbare Sprechblase als Wirkung unterscheiden. Keine Zeichenkette als Rückgabewert des ganzen sage-Blocks erfinden. |
| **26–30** | „Ist 8 größer als 8? Sag das Ergebnis vor dem Klick voraus.“ Auswerten und „Wahrheitswert“ benennen. | Ergebnis **falsch** erklären: gleich ist nicht größer. Nicht alle Werte sind Zahlen. Die feste Vergleichsaufgabe verlangt keine fünfte Tabellenzeile. |
| **30–36** | „Ändere nur die 7 innerhalb des Bewegungsblocks in 9. Was bleibt gleich, was ändert sich?“ Zuerst Vorhersage, dann Reset und Bewegung. | Summe und Endort 14; Typ Zahl und Blockart bleiben gleich. Die lose Rechnung 5 + 7 ergibt weiterhin 12. Knapp an der vorhandenen Zeile ergänzen. |
| **36–43** | „Wähle oder baue eine eigene Rechnung für 12 und setze sie in die Bewegung ein. Erkläre den Weg der Zahl.“ Bei Paaren Bedienrolle wechseln. Nach etwa vier Minuten: „Zeig mir, welche Eingabe der äußere Block erhält.“ | Eigene Wahl testen und vierte Zeile ergänzen. Die bereitliegende 3 × 4 darf bewusst verwendet werden; das bloße Anklicken beweist die Verknüpfung noch nicht. |
| **43–50** | „Klicke x-Position nach Starten an, dann nach deiner Fahrt. Der Block hat keine sichtbare Zahleneingabe. Woher kommt sein Wert?“ | x-Reporter liefert zuerst 0, nach der eigenen Zwölferfahrt 12. Er liest den aktuellen Zustand und bewegt den Rover nicht. Die Beobachtung passt als Randnotiz zur eigenen Zeile. |
| **50–52** | „Zeigt euch eure eigene Zeile. Kann die andere Person Rechnung → Zahl → Bewegung → neuer Ort erklären? Verbessert eine unklare Stelle.“ | Kurzes Peer-Feedback, bei Bedarf von der Lehrperson. Beide erklären; gemeinsame Datei allein ist kein individueller Nachweis. |
| **52–55** | Neuer Fall zunächst ohne Lauf: „Aus 8 > 8 wird 9 > 8. Was ist das Ergebnis? Ändert sich auch der Typ?“ | Jede Person sagt **wahr** voraus, prüft und ergänzt: Ergebnis geändert, Typ Wahrheitswert geblieben. Lehrperson hört/liest die Begründung. |
| **55–60** | Sicherung aus den Antworten bündeln. Eigene Datei speichern und wieder öffnen. „Woran erkennst du deine Rechnung? Setze zurück und prüfe deine Bewegung erneut.“ | Vier Zeilen und Vorher-nachher-Notiz behalten. Eigene Eingaben nach dem Öffnen identifizieren und erneut x = 12 erreichen. Ein Download allein genügt nicht als Datei-Rückkehr. |

## Lösungen und knappe Sicherung

| Beispiel | Eingabe | Wert und Typ oder Wirkung |
|---|---|---|
| Lose `5 + 7` | 5 und 7 | Rückgabewert 12, Typ **Zahl**; keine Bewegung. |
| `gehe (5 + 7) Schritte` | Äußerer Block erhält die berechnete 12. | Wirkung x: 0 → 12 bei Richtung 90°; kein in eine Rechnung einsetzbarer Rückgabewert des Bewegungsblocks. |
| `sage Ziel` | „Ziel“, Typ **Zeichenkette** | Sichtbare Textausgabe als Wirkung; kein einsetzbarer Rückgabewert des sage-Blocks. |
| Eigene Rechnung in Bewegung | Beispielsweise 6 + 6, 3 × 4 oder 15 − 3 ergibt 12. | Zahl 12 wird Bewegungseingabe; nach Reset x = 12. Verschiedene Rechnungen sind gleichberechtigt. |
| Nur innere 7 → 9 | 5 und 9 | Ergebnis 14, Typ weiterhin Zahl; Bewegung von 0 nach 14. Lose 5 + 7 unverändert. |
| `8 > 8` → `9 > 8` | Erst 8 und 8, dann 9 und 8 | **falsch → wahr**, beide vom Typ **Wahrheitswert**. |
| `x-Position` | Keine sichtbare Eingabe; liest Bühnenzustand. | Zahl: nach Reset 0, nach eigener Fahrt 12. Kein Befehl und keine feste Konstante. |

**An Tafel/Projektion und im vorhandenen Notizprodukt bündeln:** „Der innere Ausdruck liefert einen Wert. Der äußere Block verwendet ihn als Eingabe. Eine Anweisung bewirkt etwas. Werte haben Typen: Zahl, Zeichenkette, Wahrheitswert. x-Position liest den aktuellen Ort.“ Dazu den Pfeil **Rechnung → 12 → Bewegung → x = 12**. Die [öffentliche Sicherung](sicherung.html) erst nach dem eigenen Versuch für den Abgleich nutzen; sie ist kein geschützter Test.

## Hürden und nächste Hilfe

| Beobachtung | Passender nächster Impuls |
|---|---|
| „Starten fährt nicht los.“ | „Hier setzt Starten den Ort zurück. Welchen losen Block musst du für die Fahrt anklicken?“ Nicht wiederholt neu laden. |
| x ist 24 oder 26 statt 12/14. | Ausgangsort prüfen. „Die neue Fahrt beginnt an deinem jetzigen Ort. Was bewirkt Starten?“ Zurücksetzen und erneut vorhersagen. |
| Die Änderung scheint nichts zu bewirken. | Beide getrennten Summen zeigen lassen. „Welche 7 steckt in der Bewegung?“ Nur dort ändern; Ergebnis an x ablesen. |
| Wertblase und Sprechblase werden gleichgesetzt. | „Welche Anzeige gehört zur Rechnung? Welchen Wert kann ein anderer Block verwenden?“ Dann sage-Block vergleichen; sichtbare Ausgabe nicht als „keine Ausgabe“ bezeichnen. |
| „14 ist ein neuer Typ“ / „wahr ist eine Zahl“. | Wert und Typ getrennt benennen lassen. „Was kann dieser Block grundsätzlich liefern: eine Zahl oder eine Ja-Nein-Entscheidung?“ |
| Eigene Rechnung oder Sprache überfordert. | Erst Zielzahl 12 in Teilzahlen zerlegen lassen, bei Bedarf vorbereitete 3 × 4 anbieten. Satzanfänge: „Der innere Block liefert …“, „Der äußere erhält …“, „Der Ort ändert sich, weil …“. Mündliches Erklären zulassen. |

**Schrittmodus** nur bei Bedarf zur verlangsamten Beobachtung einsetzen: Ein Schritt ist ein Auswertungsschritt, nicht zwingend eine Bewegung. Den Reset vollständig beenden, bevor ein loser Block gestartet wird. Keine feste Klickzahl versprechen; Modus anschließend beenden, wenn er nicht mehr hilft. Form und Bedeutung der Blöcke mitbetrachten, nicht allein ihre Farbe.

Wer sicher arbeitet, kann freiwillig eine zweite Rechnung für 12 erklären oder vorhersagen, wo eine zweite Fahrt ohne Reset endet. Das ersetzt keine noch fehlende Kernhandlung und wird nicht zur Zusatzpflicht.

## Diagnose und Anschluss an ALG-3

**Bereit für den regulären Anschluss:** Die Person unterscheidet Rückgabewert und Wirkung, erklärt die eigene Verschachtelung und begründet im neuen Vergleich wahr bei unverändertem Typ Wahrheitswert. ALG-3 kann Bedingungen daran anschließen. Eine richtige 12, eine kopierte Tabelle oder ein fertiges Partnerprojekt allein reichen für dieses Urteil nicht.

**Gezielte Nachsicherung:** Bei unklarer Verschachtelung den inneren Wert mit einem Pfeil zur äußeren Eingabe verfolgen lassen und mit einer anderen Rechnung erneut fragen. Bei unsicherem Wahrheitswert vor ALG-3 einen weiteren strikten Vergleich zunächst ohne Lauf begründen lassen. Hilfen danach abbauen. Auch die ruhigere Person am Partnergerät einbeziehen. Wenn individuelle Antworten fehlen, Diagnose offen halten und zu Beginn von ALG-3 kurz einzeln nachfragen. Bedien-/Dateiprobleme getrennt von fachlichen Lücken notieren.

## Zeitraster, Ausfall und Rückfluss

Bei **45-Minuten-Stunden** bleibt es bei insgesamt 60 Minuten: 0–43 wie oben; 43–45 Zwischenstand speichern, innerhalb der zwanzig Minuten Eigenarbeit. Nach der Pause 45–50 Datei öffnen und die x-Position-Probe durchführen; 50–60 unverändert. Kein über die Pause offener Tab wird vorausgesetzt. Der Variantenwechsel beansprucht Zeit der Eigenphase und setzt eine eingeübte Dateiroutine voraus.

Bei Verzögerungen zuerst freiwillige Vertiefung und weitere Plenumsbeiträge streichen. Eigene Wertverknüpfung und individueller neuer Fall bleiben erhalten. Scheitert die Datei-Rückkehr oder fehlt Diagnosezeit, den offenen Schritt ausdrücklich dokumentieren und gezielt nachholen. Notwendige zusätzliche Unterstützung nach Jahrgangsbrief im vorhandenen Jahreskonto von **135 Unterstützungsminuten** buchen; keine heimliche Verlängerung der 60 Minuten, keine Doppelbuchung. Bei größerem Verlust den Anschluss anhand der tatsächlichen Diagnose neu planen.

Bei Geräteausfall können Vorhersage, Wertpfeile und Vergleich auf Papier erarbeitet werden; ein Demonstrationslauf unterstützt den Abgleich. Individuelle Programmbedienung und Datei-Rückkehr sind damit nicht nachgewiesen.

**Kompakter WU-Check:** Vorhersage und neuer Fall aktivieren Denken (Band 1); gestufte Hilfen reagieren auf konkrete Beobachtungen (Band 3); eigene Rechnung, Rückmeldung und Diagnose erhalten den fachlichen Anspruch (Band 6). Das ist eine Planungsprüfung, kein Wirksamkeitsnachweis. Nach dem realen Einsatz nur vier Punkte zurückmelden: Welche Unterscheidung gelang selbstständig? Wo war Hilfe nötig? Gelang die Datei-Rückkehr? Welche tatsächliche Zeit und nächste Unterstützung folgen daraus? Briefing bei Ablaufänderungen mitführen.
