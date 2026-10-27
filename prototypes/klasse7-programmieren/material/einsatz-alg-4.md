# ALG-4 · Durchführungsplan für den ersten Unterrichtseinsatz

**75 Minuten · Lehrerimpulse, Hilfen und Anschlussdiagnose.** [Briefing als Vorlesetext](alg-4-briefing.html) · [Zur Lernaufgabe](../lernende/alg-4.html)

## Ziel und Rahmen

„Warum fährt der Rover immer weiter?“: Die Lernenden unterscheiden feste Wiederholungszahl und bedingten Abbruch. Sie verfolgen die **Prüfung vor der Bewegung**, reparieren die Abbruchbedingung und begründen auch null Bewegungen sowie ein erlaubtes Überschreiten der Marke. Das Modell gilt für **positive Schritte nach rechts, Richtung 90°**, ohne Hindernisse; es steuert keinen echten Roboter.

Grundlage sind die [Lernendenfassung 2.0](../lernende/alg-4.html), der [Reihenkommentar](durchfuehrung-134.html) und der [Jahrgangsbrief](jahrgang.html). **15 + 15 + 30 + 15 = 75 Minuten**, unverändert **405 Programmierminuten innerhalb der 36 Jahres-UE**. Die bestehende Planung bezieht sich auf die dort dokumentierte Anhörungsfassung vom 21.09.2026; keine neue Aussage zum verbindlichen Planstatus oder zu einer Fachprofilfreigabe.

ALG-1 liefert feste Wiederholung, ALG-3 Wahrheitswerte, Negation und Grenzfall. Vorher die tatsächliche ALG-3-Rückmeldung prüfen. Lerngruppe, Gerätezahl, tatsächliche Diagnose und Dateiroutine sind noch unbekannt; der Verlauf setzt startbereite Geräte voraus. Er ist eine Erprobungsplanung, keine gemessene Bearbeitungszeit.

**Ein vorhandenes Notizprodukt genügt:** vollständige Prüfspur der Reparatur für Start 0, erste Prüfung für 40 und 45 sowie der begründete neue Fall 35/12; dazu die eigene reparierte XML. Vorhersagen bleiben lesbar, Korrekturen werden ergänzt. Keine zusätzliche Ablaufgrafik, zweite Volltabelle oder neue Abgabe.

## Vorbereitung und Material

- [Lernaufgabe ALG-4](../lernende/alg-4.html) und [zugehöriges Startprojekt](https://h4r7w16.github.io/ium-lernwerk/klasse7/programmieren/snap/lernwerk.html?aufgabe=alg-4) bereithalten. Die Datei heißt `ALG-4-Fehlersuche.xml`. **Starten führt hier den gesamten angehängten Stapel aus:** Startort setzen, Richtung setzen, `wiederhole bis x-Position = 40`, danach `sage fertig`. Keine lose Schleife zusätzlich anklicken.
- **Start-x**, **Schrittweite 10** und **Vergleichsgrenze 40** getrennt zeigen. In der Reparaturphase nur die Abbruchbedingung ändern. Die Schrittweite bleibt bis zum neuen Kurzfall bei 10; y = 0 und Richtung 90° bleiben erhalten. x unten am Bühnenrand ablesen, nicht aus der Figurgröße schätzen.
- Vor dem Fehlerstart 45 sichtbar **Schrittmodus einschalten**, dann Starten und **Ein Schritt** bedienen. Positionsänderungen zählen; spätestens nach vier Bewegungen **Stopp**. Erst nach dem Stopp den Schrittmodus beenden. Der Moduswechsel ersetzt Stopp nicht; **Fortsetzen** würde einen pausierten Fehlerlauf weiterführen. Diese Routine vorher auf dem eingesetzten Gerät prüfen.
- **Alte Anzeige beachten:** In der öffentlichen Probe blieb die vorherige „fertig“-Sprechblase während des neuen Fehlerlaufs stehen. Sie beweist deshalb kein Ende dieses Laufs. Bei „Wartet auf einen Schritt“ läuft die Untersuchung noch; ein erzwungener Stopp ist ebenfalls kein reguläres Schleifenende. Aktuelle Prüfspur und Codeweg entscheiden.
- Bestehende [ALG-4-Sicherung](sicherung.html) samt repariertem Beispiel erst nach dem eigenen Versuch nutzen. Projiziert werden Lernaufgabencode, reale Schritte und die gemeinsame Prüfspur. Eine weitere Präsentation oder Grafik ist nicht nötig.
- **Datei speichern → Datei öffnen** mit neutraler Kennung und vereinbartem Ablageort vorher in Safari auf dem Schulgerät erproben. Zielname `ALG-4_Kennung.xml`. Bei Partnergeräten zunächst Bedienung und Vorhersage verteilen, zur eigenen Reparatur wechseln. Beide führen die knappe Spur und erklären selbst; allein übernimmt die Lehrperson den Gegencheck.

## Verlauf · 75 Minuten

| Zeit | Lehrperson und konkreter Impuls | Lernhandlung und Beobachtung |
|---|---|---|
| **0–3** | „Die Haltestelle liegt bei 40. Solange der Rover davor ist, soll er fahren. An oder hinter 40 soll er keinen weiteren Schritt machen.“ Anschluss: ALG-3 prüfte einmal, jetzt kehrt die Prüfung zurück. | Auftrag erfassen: Überschreiten ist erlaubt, Weiterfahren danach nicht. Noch keinen Fehlerlauf starten. |
| **3–8** | Vier feste Zehnerschritte neben den `bis`-Code stellen. „Was entscheidet jeweils, ob noch eine Bewegung kommt?“ | Feste Anzahl von Bedingungsprüfung unterscheiden. Zahl 4 und Vergleich 40 sind verschiedene Steuerungen. |
| **8–12** | „Was bedeutet wahr beim bis-Block? Was geschieht, wenn die Bedingung schon am Anfang wahr ist?“ Die Prüfung vor dem Rumpf markieren. | Wahr → Schleife endet; falsch → Bewegung und erneute Prüfung. Null Durchläufe sind möglich. |
| **12–15** | „Vermute für 0, 40 und 45: Welche Orte folgen, endet der Entwurf? Was würden dagegen vier feste Zehnerschritte tun?“ | Individuelle kurze Vorhersagen auf der vorhandenen Notiz, danach Austausch. Keine drei ausführlichen Zusatzprotokolle verlangen. |
| **15–21** | Start 0 und danach 40 gemeinsam prüfen. Jeweils nur Start-x ändern. „Warum fährt er bei 40 gar nicht? Wo liegt fertig im Code?“ | Fehlerentwurf endet von 0 bei 40 nach vier Bewegungen, von 40 ohne Bewegung. Zwischenpositionen am Code erklären; bei Bedarf kurz steppen. Beide Fälle allein beweisen noch keine brauchbare Steuerung. |
| **21–27** | Start 45 im aktivierten Schrittmodus verfolgen. „Welche Position hat sich wirklich verändert? Ist Gleichheit jetzt wahr?“ Spätestens bei vier Bewegungen stoppen; alte „fertig“-Anzeige ausdrücklich vom aktuellen Lauf trennen. | **45 → 55 → 65 → 75 → 85** beobachten; Gleichheit bleibt falsch. Bedienklicks und Bewegungen getrennt zählen. Stopp dokumentiert den Abbruch des Versuchs, keine erfolgreiche Programmlösung. |
| **27–30** | „Warum kann er von 45 mit positiven Zehnerschritten die 40 nie erreichen? Warum wäre ein festes Viermal trotzdem keine Reparatur unserer Regel?“ | Bewegung führt weiter von 40 weg. Viermal endet zwar nach vier Bewegungen, stoppt aber am Start 40 nicht sofort; die gewünschte Regel ist bedingt. |
| **30–38** | „Ändere nur die Abbruchfrage. Welche Antwort muss sie bei 0, bei 40 und bei 45 liefern?“ Nach etwa fünf Minuten eine Begründung hören. Eine Formel erst als gezielte Hilfe anbieten. | Eigenen Vorschlag formulieren: bei 0 falsch, bei 40/45 wahr. Vergleich und gegebenenfalls nicht selbst wählen. Unklare Vorschläge zunächst gedanklich bzw. begrenzt im Schrittmodus prüfen; bei unerwartetem Weiterfahren stoppen. |
| **38–50** | „Verfolge deine reparierte Fassung von 0. Schreibe bei jeder Prüfung Ort, wahr/falsch und nächste Handlung auf. Welche Prüfung beendet den Lauf?“ Bei Paaren Bedienrolle wechseln. | Vollständige Spur mit **0, 10, 20, 30, 40**. Vier Bewegungen, fünf logische Prüfungen einschließlich der letzten wahren Prüfung. Betroffenen Fall nach einer Korrektur erneut prüfen. |
| **50–60** | „Prüfe die Starts 40 und 45. Welche erste Prüfung genügt jeweils? Was bleibt gegenüber dem alten Entwurf anders?“ Gezielter Blick auf eigene Bedingung und tatsächlichen Lauf. | Je eine erste wahre Prüfung, null Bewegungen, anschließend fertig. 45 bleibt bei 45; er soll nicht zurück nach 40 fahren. Nur diese ersten Prüfungen zur vorhandenen Spur ergänzen und einen Fall begründen. |
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

Vollständige reparierte Prüfspur von 0: **0/falsch → gehe 10; 10/falsch → gehe 10; 20/falsch → gehe 10; 30/falsch → gehe 10; 40/wahr → Schleife verlassen und fertig anzeigen.** Die letzte Zeile ist Teil der Erklärung. Native Auswertungsschritte des Editors werden hier nicht als zusätzliche logische Bedingungsprüfungen gezählt.

Neuer Fall 35/12: **Endort 47, eine Bewegung, zwei Prüfungen**. Die Gleichheitsfassung würde 40 überspringen und mit positiven Zwölferschritten nicht zurückkehren. Das muss nicht ungebremst ausprobiert werden; die begründete Positionsfolge genügt für diese Fehleraussage.

**Zentrale Sicherung an Tafel/Projektion und im bestehenden Notizprodukt:** Prüfspur mit letzter wahrer Zeile; daneben „wahr → Ende, falsch → Bewegung → neue Prüfung“. Merksatz: „Der bis-Block prüft vor der Bewegung. An oder hinter der Marke kann die Schleife ohne Bewegung enden. Ein zulässiges Ende muss nicht exakt auf der Marke liegen.“ Die [öffentliche Sicherung](sicherung.html) erst nach dem eigenen Versuch zum Abgleich nutzen; sie ist kein geschützter Test.

## Hürden und nächste Hilfe

| Beobachtung | Passender nächster Impuls |
|---|---|
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

**Regulärer Anschluss:** Die Person erklärt die Reihenfolge Prüfung–Bewegung–Prüfung, einschließlich letzter wahrer Prüfung, und begründet null Bewegungen bei 40/45. Im neuen Fall nennt und erklärt sie 47, eine Bewegung und zwei Prüfungen. Eigene Bedingung und Spur stimmen überein. Ein kopiertes `nicht (x < 40)`, vier Bedienklicks oder die sichtbare Meldung allein belegen dies nicht.

**Gezielte Nachsicherung:** Bei vertauschter Fortsetzungs-/Abbruchfrage zuerst die Frage in Alltagssprache für 40 beantworten, dann einen veränderten Start ohne Lauf prüfen. Fehlt die letzte Prüfung, die letzte Bewegung und die nachfolgende Entscheidung getrennt zeigen und an einem anderen kurzen Fall erneut erklären lassen. Ruhigere Partnerperson einbeziehen. Fehlen individuelle Antworten, beginnt ALG-5 mit einer Ersatzdiagnose statt mit ungeprüft vorausgesetztem Verständnis. Geräteprobleme getrennt von fachlichen Lücken notieren.

ALG-5 erweitert das auf eigene Station, Schrittweite, Meldungsverzweigung und selbst gewählten Gegenfall. Dessen vollständige Steuerung wird hier nicht vorweggenommen.

## Zeitraster, Ausfall und Rückfluss

**Variante 45 + 30 Minuten:** 0–43 wie oben; 43–45 den laufenden Versuch beenden, eigene Fassung speichern und offenen Prüfschritt auf der Notiz markieren. Nach der Pause 45–48 öffnen; 48–60 gegebenenfalls offenen Bauschritt beenden, die Prüfspur ab Start 0 abgleichen und 40/45 prüfen. 60–75 bleiben unverändert. Das XML sichert den Code, keinen an genau derselben Stelle fortsetzbaren Lauf. Dateiaktionen liegen innerhalb der dreißigminütigen Eigenphase; ein offener Tab über die Pause wird nicht vorausgesetzt. Eingeübte Dateiroutine ist Voraussetzung, die Zeitvariante noch nicht im Unterricht erprobt.

Bei Verzögerung zuerst freiwillige Vertiefung und weitere Plenumsbeiträge weglassen. Eigene Reparatur, letzte Prüfung und neuer Kurzfall bleiben erhalten. Fehlende Datei-Rückkehr oder Diagnose ausdrücklich offen halten und nachholen. Nötige Zusatzunterstützung im bestehenden Jahreskonto von **135 Unterstützungsminuten** konkret buchen; keine heimliche Verlängerung der 75 Minuten und keine Doppelbuchung.

Bei Geräteausfall lassen sich Code, Vorhersagen, Reparatur und Prüfspur auf Papier bearbeiten; ein Demonstrationslauf unterstützt den Abgleich. Eigene Programmbedienung und Datei-Rückkehr sind damit nicht nachgewiesen. Falls der Schrittmodus am vorgesehenen Gerät nicht verlässlich funktioniert, Fehlerfall 45 nur am Code verfolgen und die digitale Ausführung offen dokumentieren. Bei größerem Verlust den Anschluss anhand der tatsächlichen Lage neu planen.

**Kompakter WU-Check:** Gegenfall und letzte Prüfung aktivieren begründetes Denken (Band 1); gestufte Hilfen reagieren auf konkrete Verwechslungen (Band 3); eigene Bedingung, Rückmeldung und neuer Fall erhalten den fachlichen Anspruch (Band 6). Das ist eine redaktionelle Planungsprüfung, kein Wirksamkeitsnachweis. Nach Einsatz tatsächliche Minuten, individuelle Abbrucherklärung, benötigte Hilfe, Datei-Rückkehr und nächsten Schritt vor ALG-5 dokumentieren; Briefing bei Ablaufänderungen mitführen.
