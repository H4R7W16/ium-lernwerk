# ALG-4 · Durchführungsplan für den ersten Unterrichtseinsatz

**75 Minuten · Lehrerimpulse, Hilfen und Anschlussdiagnose.** [Briefing als Vorlesetext](alg-4-briefing.html) · [Zur Lernaufgabe](../lernende/alg-4.html)

## Ziel und Rahmen

„Warum fährt der Rover immer weiter?“: Die Lernenden unterscheiden feste Wiederholungszahl und bedingten Abbruch. Sie verfolgen die **Prüfung vor der Bewegung**, reparieren die Abbruchbedingung und begründen auch null Bewegungen sowie ein erlaubtes Überschreiten der Marke. Das Modell gilt für **positive Schritte nach rechts, Richtung 90°**, ohne Hindernisse; es steuert keinen echten Roboter.

Grundlage sind die [Lernendenfassung 2.2](../lernende/alg-4.html), der [Reihenkommentar](durchfuehrung-134.html) und der [Jahrgangsbrief](jahrgang.html). **10 Minuten Entdecken + 15 Minuten Erklären + 35 Minuten Reparieren + 15 Minuten Gegencheck, Transfer und Sicherung = 75 Minuten**. Die Reihe bleibt bei **405 Programmierminuten innerhalb der 36 Jahres-UE**. Die bestehende Planung bezieht sich auf die dort dokumentierte Anhörungsfassung vom 21.09.2026; keine neue Aussage zum verbindlichen Planstatus oder zu einer Fachprofilfreigabe.

**Didaktische Änderung:** Der begrenzte Widerspruch zwischen den Starts 0 und 45 erzeugt die Frage, die anschließend explizit geklärt wird. Das ist kein ungestütztes Entdecken: Code, Zielregel und Stoppweg sind vorgegeben, die Erklärung folgt spätestens ab Minute 10. Die Wahl des ersten Reparaturtests ist fachlich begründet: 40 entlarvt einen strengen Größer-Vergleich, 45 den Gleichheitsabbruch. Beide Fälle bleiben Pflicht. Eine kürzere gemeinsame Phase schafft fünf zusätzliche Minuten für die eigene Reparatur.

ALG-1 liefert feste Wiederholung, ALG-3 Wahrheitswerte, Negation und Grenzfall. Vorher die tatsächliche ALG-3-Rückmeldung prüfen. Lerngruppe, Gerätezahl, tatsächliche Diagnose und Dateiroutine sind noch unbekannt; der Verlauf setzt startbereite Geräte voraus. Er ist eine Erprobungsplanung, keine gemessene Bearbeitungszeit.

**Ein vorhandenes Notizprodukt genügt:** eine kurze Vermutung/Positionsfolge aus dem Einstieg, eigene Abbruchfrage, vollständige Prüfspur der Reparatur für Start 0, erste Prüfung für 40 und 45 sowie der begründete neue Fall 35/12; dazu die eigene reparierte XML. Die Begründung der Testwahl kann mündlich erfolgen. Vorhersagen bleiben lesbar, Korrekturen werden ergänzt. Keine zusätzliche Ablaufgrafik, zweite Volltabelle oder neue Abgabe.

## Vorbereitung und Material

- [Lernaufgabe ALG-4](../lernende/alg-4.html) und [zugehöriges Startprojekt](../snap/lernwerk.html?aufgabe=alg-4) bereithalten. Die Datei heißt `ALG-4-Fehlersuche.xml`. **Starten führt hier den gesamten angehängten Stapel aus:** Startort setzen, Richtung setzen, `wiederhole bis x-Position = 40`, danach `sage fertig`. Keine lose Schleife zusätzlich anklicken.
- **Start-x**, **Schrittweite 10** und **Vergleichsgrenze 40** getrennt zeigen. Im Einstieg selbst nur Start-x ändern; in der Reparaturphase die Abbruchbedingung. Die Schrittweite bleibt bis zum neuen Kurzfall bei 10; y = 0 und Richtung 90° bleiben erhalten. x unten am Bühnenrand ablesen, nicht aus der Figurgröße schätzen. Das Startprojekt und eine Projektion vor Stundenbeginn bereitstellen; Geräteöffnung gehört in die ersten fünf Minuten, kein zusätzlicher Vorspann.
- Vor dem Fehlerstart 45 sichtbar **Schrittmodus einschalten**, dann Starten und **Ein Schritt** bedienen. Positionsänderungen zählen; spätestens nach vier Bewegungen **Stopp**. Erst nach dem Stopp den Schrittmodus beenden. Der Moduswechsel ersetzt Stopp nicht; **Fortsetzen** würde einen pausierten Fehlerlauf weiterführen. Diese Routine vorher auf dem eingesetzten Gerät prüfen.
- **Alte Anzeige beachten:** In der öffentlichen Probe blieb die vorherige „fertig“-Sprechblase während des neuen Fehlerlaufs stehen. Sie beweist deshalb kein Ende dieses Laufs. Bei „Wartet auf einen Schritt“ läuft die Untersuchung noch; ein erzwungener Stopp ist ebenfalls kein reguläres Schleifenende. Aktuelle Prüfspur und Codeweg entscheiden.
- Bestehende [ALG-4-Sicherung](sicherung.html) samt repariertem Beispiel erst nach dem eigenen Versuch nutzen. Projiziert werden Lernaufgabencode, reale Schritte und die gemeinsame Prüfspur. Eine weitere Präsentation oder Grafik ist nicht nötig.
- **Datei speichern → Datei öffnen** mit neutraler Kennung und vereinbartem Ablageort vorher in Safari auf dem Schulgerät erproben. Zielname `ALG-4_Kennung.xml`. Bei Partnergeräten zunächst Bedienung und Vorhersage verteilen, zur eigenen Reparatur wechseln. Beide führen die knappe Spur und erklären selbst; allein übernimmt die Lehrperson den Gegencheck.

## Verlauf · 75 Minuten

| Zeit | Lehrperson und konkreter Impuls | Lernhandlung und Beobachtung |
|---|---|---|
| **0–5** | Zielregel nennen, dann „Gilt das bei Start 0 und auch bei 45?“ Keine Abbrucherklärung vorweggeben. Kurze Vermutung, Link öffnen, Start 0 ausführen lassen. | Früh selbst am laufenden Programm handeln. Endort 40 beobachten; kurze Vermutung zu 45 festhalten. Wer den Fehler schon erkennt, begründet seine Vorhersage, statt Überraschung vorspielen zu müssen. |
| **5–10** | Nur Start-x auf 45 ändern; gemeinsam im vorher eingeschalteten Schrittmodus untersuchen. „Was ändert sich tatsächlich? Passt das zu unserer Regel?“ Nach zwei beobachteten Bewegungen besprechen und stoppen, spätestens nach vier. | **45 → 55 → 65** beobachten, gegebenenfalls bis 85. Eine kurze Folge genügt. Alte „fertig“-Blase ist kein Endbeleg. Stopp, dann Modus beenden. Ursache als Vermutung sammeln; noch keine vollständige Reparatur zeigen. |
| **10–15** | Jetzt am gerade untersuchten Code erklären: „bis prüft vor der Bewegung. Wahr heißt Ende, falsch heißt Bewegung und erneute Prüfung.“ „Warum wird Gleichheit von 45 aus nicht wahr?“ | Erklärung an Beobachtung binden. Positive Zehnerschritte führen von 45 weiter weg; bloß länger warten hilft nicht. |
| **15–20** | „Nun Start 40: Was geschieht zuerst? Fährt er überhaupt?“ Jede Person erst vorhersagen und begründen lassen, dann gemeinsam prüfen. | Erste Prüfung wahr, null Bewegungen. Prüfung und Bewegung unterscheiden; Ergebnis am Code erklären. |
| **20–25** | Vier feste Zehnerschritte danebenstellen. „Welche Endorte ergeben sich ab 0, 40, 45? Welche Regel steuert jeweils die Anzahl?“ | Mündlich 40, 80, 85 vergleichen. Viermal endet immer nach vier Durchläufen, erfüllt aber nicht die Zielregel. Keine zusätzliche Vergleichstabelle verlangen. |
| **25–30** | „Welche Frage soll bei ja das Aufhören auslösen?“ Erst eigene Worte, dann Blockvorschlag. Hilfe nur bei beobachteter Hürde öffnen lassen. | Abbruchfrage formulieren; erste eigene Änderung spätestens in dieser Phase. Ziel: bei 0 falsch, bei 40/45 wahr. Keine Lösung als gemeinsames Abschreibmuster. |
| **30–40** | „Womit prüfst du deine Idee zuerst: 40 oder 45? Warum gerade damit?“ Nicht eine Wahl als einzig richtige werten. Bei unerwartetem Weiterfahren nach höchstens vier Bewegungen stoppen lassen. | Test auswählen und erwarten; bei Abweichung die erste regelwidrige Entscheidung lokalisieren, ihren Wahrheitswert erklären, genau dort verbessern und denselben Start erneut prüfen. Die Testwahl richtet sich nach dem eigenen Vorschlag; beide Fälle folgen noch. |
| **40–55** | „Verfolge die Reparatur von 0 vollständig, dazu die erste Prüfung bei 40 und 45.“ Bei Paaren Bedienrolle wechseln. | Spur **0, 10, 20, 30, 40** einschließlich letzter wahrer Prüfung; bei 40/45 sofort wahr, null Bewegungen. Alle drei Starts mit der endgültigen Bedingung tatsächlich prüfen. Frühere Erfolge mit einer verworfenen Bedingung gelten nicht für die Endfassung. |
| **55–60** | Kurzer individueller Blick: „Welche Zeile erklärt das Ende? Was ist bei 45 jetzt anders?“ Offene Reparatur gezielt unterstützen. | Erklärung und Code abgleichen. Dieses Fenster dient der Konsolidierung oder Nacharbeit innerhalb der 35 Minuten, keiner Zusatzaufgabe. |
| **60–63** | „Lasst einen eurer Fälle prüfen. Kann die andere Person die letzte Prüfung und den Übergang zu fertig erklären?“ | Peer-Feedback an Spur und Code; eine unklare Stelle verbessern. Richtiger Endort allein genügt nicht, beide Personen erklären selbst. |
| **63–69** | Neuer Kurzfall, erst individuell: „Start 35, Schrittweite 12. Wo endet die reparierte Fassung? Wie viele Bewegungen und Prüfungen gibt es? Warum reicht Gleichheit nicht?“ Danach gezielt testen. | **35/falsch → Bewegung nach 47; 47/wahr → Ende.** Eine Bewegung, zwei Prüfungen. 47 ist zulässig; keine Fahrt exakt nach 40 erfinden. Begründung knapp an der vorhandenen Notiz ergänzen. |
| **69–70** | Sicherung bündeln: „bis heißt: bei wahr stoppen. Auch der letzte Test und auch null Bewegungen gehören dazu.“ | Abbruchfrage und Bewegungsanzahl getrennt benennen. Prüfspur und neuer Fall bleiben sichtbar. |
| **70–75** | **Start 0 und Schrittweite 10 wiederherstellen, die reparierte Bedingung behalten.** Datei speichern und wieder öffnen. „Erkennst du deine Abbruchfrage? Prüfe von 0 erneut.“ | Eigene Reparatur nach der Datei-Rückkehr identifizieren; Ergebnis 40 mit nachvollziehbarem Ende. Ein Download allein genügt nicht. Nicht versehentlich die fehlerhafte Gleichheit wiederherstellen. |

## Lösungen und zentrale Sicherung

| Start | Fehlerentwurf mit `x = 40` | Vier feste Zehnerschritte | Reparatur mit `nicht (x < 40)` |
|---|---|---|---|
| 0 | 0 → 10 → 20 → 30 → 40; vier Bewegungen, fünf Prüfungen; fertig | Vier Bewegungen bis 40 | Vier Bewegungen bis 40; fünf Prüfungen |
| 40 | Erste Prüfung wahr, null Bewegungen; fertig | Vier Bewegungen bis 80 | Erste Prüfung wahr, null Bewegungen; fertig |
| 45 | 45 → 55 → 65 → 75 → 85 …; kein reguläres Ende im Modell. Versuch nach spätestens vier Bewegungen stoppen. | Vier Bewegungen bis 85 | Erste Prüfung wahr, null Bewegungen; bleibt 45, danach fertig |

Eine mögliche Abbruchbedingung ist **`nicht (x-Position < 40)`**, also „nicht mehr davor“. Logisch gleichwertige Bedingungen akzeptieren. **`x > 40` allein ist ungeeignet:** Bei 40 ist sie noch falsch und löst eine unnötige Bewegung aus. **`x < 40`** beantwortet die Fortsetzungsfrage und würde bei Start 0 sofort abbrechen. Zahlen oder Bewegungsblöcke zu verändern ersetzt die geforderte Reparatur der Bedingung nicht.

Vollständige reparierte Prüfspur von 0: **0/falsch → gehe 10; 10/falsch → gehe 10; 20/falsch → gehe 10; 30/falsch → gehe 10; 40/wahr → Schleife verlassen und fertig anzeigen.** Die letzte Zeile ist Teil der Erklärung: Im Code wird die Schleife verlassen, anschließend folgt die Meldung. Ein manuell erzwungener Stopp ersetzt diese Zeile nicht. Native Auswertungsschritte des Editors werden hier nicht als zusätzliche logische Bedingungsprüfungen gezählt.

Neuer Fall 35/12: **Endort 47, eine Bewegung, zwei Prüfungen**. Die Gleichheitsfassung würde 40 überspringen und mit positiven Zwölferschritten nicht zurückkehren. Das muss nicht ungebremst ausprobiert werden; die begründete Positionsfolge genügt für diese Fehleraussage.

**Zentrale Sicherung an Tafel/Projektion und im bestehenden Notizprodukt:** Prüfspur mit letzter wahrer Zeile; daneben „wahr → Ende, falsch → Bewegung → neue Prüfung“. Merksatz: „Der bis-Block prüft vor der Bewegung. An oder hinter der Marke kann die Schleife ohne Bewegung enden. Ein zulässiges Ende muss nicht exakt auf der Marke liegen.“ Die [öffentliche Sicherung](sicherung.html) erst nach dem eigenen Versuch zum Abgleich nutzen; sie ist kein geschützter Test.

## Hürden und nächste Hilfe

| Beobachtung | Passender nächster Impuls |
|---|---|
| Änderungen werden wahllos ausprobiert. | „Wo ist die erste Entscheidung, die unserer Regel widerspricht? Was liefert deine Frage dort?“ Erst diese Stelle erklären, dann einen begründeten Eingriff und denselben Test wiederholen. |
| „Wahr heißt weiterfahren.“ | „Lies das Wort bis. Ist der Abbruch schon erreicht?“ Die erste Prüfung bei Start 40 ohne Lauf beantworten lassen. |
| Jede Schleife müsse mindestens einmal fahren. | Prüfung vor dem Bewegungsblock zeigen. „Was würde bei Start 40 als Erstes ausgeführt?“ |
| Richtiger Endort, aber letzte Prüfung fehlt. | „Woher weiß das Programm nach der letzten Bewegung, dass es fertig ist?“ Letzte Zeile ergänzen und fünf Prüfungen von vier Bewegungen unterscheiden. |
| x > 40 scheint zu funktionieren. | Den noch ungeprüften Start genau bei 40 vorhersagen. Eine zusätzliche Bewegung dort widerlegt die Regel. |
| Vergleichsgrenze oder Bewegung wurde statt der Bedingung verändert. | Start-x, Grenze 40 und Schrittweite 10 getrennt zeigen. Nur den Prüfblock reparieren; alle drei Starts beibehalten. |
| Nach mehreren Klicks bewegt sich nichts. | „Ein Schritt ist ein Auswertungsschritt. Wird gerade die Frage berechnet?“ Auf nächste tatsächliche x-Änderung achten; keine feste Klickzahl versprechen. |
| „Es steht doch fertig, also ist er fertig.“ | Alte Sprechblase, aktuellen Wartestatus und mathematischen Codeweg vergleichen. Der manuelle Stopp ist kein vom Programm gefundenes Schleifenende. |
| Schreiben oder Begründen blockiert. | Eine leere Zeile mit Ort / wahr-falsch / nächste Handlung anbieten. Satzanfänge: „Bei 40 ist die Abbruchfrage …“, „Die letzte Prüfung ist nötig, weil …“. Mündliche Erklärung zulassen. |

Wer sicher arbeitet, kann freiwillig einen weiteren Start knapp vor 40 wählen und begründen, ob er die Marke trifft oder überspringt. Das ersetzt keinen noch fehlenden Kernfall und wird nicht zur Zusatzpflicht.

## Diagnose und Anschluss an ALG-5

**Regulärer Anschluss:** Die Person unterscheidet feste Wiederholungszahl von bedingtem Abbruch, erklärt die Reihenfolge Prüfung–Bewegung–Prüfung einschließlich letzter wahrer Prüfung und begründet null Bewegungen bei 40/45. Im neuen Fall nennt und erklärt sie 47, eine Bewegung und zwei Prüfungen. Eigene Bedingung und Spur stimmen überein. Testwahl kurz am eigenen Vorschlag begründen lassen. Bei einer Fehlreparatur muss die Person die erste regelwidrige Entscheidung benennen können; nicht die Zahl ausprobierter Blöcke bewerten. Ein kopiertes `nicht (x < 40)`, vier Bedienklicks oder die sichtbare Meldung allein belegen dies nicht. Öffentliche Sicherung und Partnerhilfe sind zugänglich; der eigene neue Fall bleibt der notwendige Gegencheck gegen scheinbaren Erfolg.

**Gezielte Nachsicherung:** Bei vertauschter Fortsetzungs-/Abbruchfrage zuerst die Frage in Alltagssprache für 40 beantworten, dann einen veränderten Start ohne Lauf prüfen. Fehlt die letzte Prüfung, die letzte Bewegung und die nachfolgende Entscheidung getrennt zeigen und an einem anderen kurzen Fall erneut erklären lassen. Ruhigere Partnerperson einbeziehen. Fehlen individuelle Antworten, beginnt ALG-5 mit einer Ersatzdiagnose statt mit ungeprüft vorausgesetztem Verständnis. Geräteprobleme getrennt von fachlichen Lücken notieren.

ALG-5 erweitert das auf eigene Station, Schrittweite, Meldungsverzweigung und selbst gewählten Gegenfall. Dessen vollständige Steuerung wird hier nicht vorweggenommen.

## Zeitraster, Ausfall und Rückfluss

**Variante 45 + 30 Minuten:** 0–43 wie oben; 43–45 den laufenden Versuch beenden, eigene Fassung speichern und offenen Prüfschritt auf der Notiz markieren. Nach der Pause 45–48 öffnen; 48–60 offene Prüfspur und 40/45 vervollständigen und erklären. Das Konsolidierungsfenster 55–60 geht darin auf. 60–75 bleiben unverändert. Das XML sichert den Code, keinen an genau derselben Stelle fortsetzbaren Lauf. Dateiaktionen liegen innerhalb der 35-minütigen Eigenphase; ein offener Tab über die Pause wird nicht vorausgesetzt. Eingeübte Dateiroutine ist Voraussetzung, die Zeitvariante noch nicht im Unterricht erprobt.

**Zeitgrenzen aktiv steuern:** Einstieg bei Minute 10 beenden, nötigenfalls nur eine gemeinsame Demonstration statt weiterer Einzelversuche. Erklärung und Nullfall bis Minute 25 klären. Ab Minute 55 zuerst offene Kernschritte unterstützen; keine zusätzliche Challenge eröffnen. Die letzten fünf Minuten bleiben für die Datei-Rückkehr. Bei Verzögerung freiwillige Vertiefung und weitere Plenumsbeiträge weglassen. Eigene Reparatur, letzte Prüfung und neuer Kurzfall bleiben erhalten. Fehlende Datei-Rückkehr oder Diagnose ausdrücklich offen halten und nachholen. Nötige Zusatzunterstützung im bestehenden Jahreskonto von **135 Unterstützungsminuten** konkret buchen; keine heimliche Verlängerung der 75 Minuten und keine Doppelbuchung.

Bei Geräteausfall lassen sich Code, Vorhersagen, Reparatur und Prüfspur auf Papier bearbeiten; ein Demonstrationslauf unterstützt den Abgleich. Eigene Programmbedienung und Datei-Rückkehr sind damit nicht nachgewiesen. Falls der Schrittmodus am vorgesehenen Gerät nicht verlässlich funktioniert, Fehlerfall 45 nur am Code verfolgen und die digitale Ausführung offen dokumentieren. Bei größerem Verlust den Anschluss anhand der tatsächlichen Lage neu planen.

**Kompakter WU-Check:** Widerspruch, begründete Testwahl und letzte Prüfung verlangen Erklärungen (Band 1); zwei Hilfen reagieren auf Fortsetzungsfrage und Grenzfehler (Band 3); eigene Bedingung, Rückmeldung und neuer Fall erhalten den Anspruch (Band 6). Das ist eine redaktionelle Planungsprüfung, kein Wirksamkeitsnachweis. Nach Einsatz festhalten: erste eigene Codeänderung erreicht, tatsächliche Minuten, individuelle Abbrucherklärung, benötigte Fach-/Bedienhilfe, Datei-Rückkehr und nächster Schritt vor ALG-5. Eine höhere Klickzahl oder sichtbare Begeisterung allein belegt kein besseres Verständnis.
