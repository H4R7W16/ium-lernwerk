# ALG-3 · Durchführungsplan für den ersten Unterrichtseinsatz

**75 Minuten · Lehrerimpulse, Hilfen und Anschlussdiagnose.** [Briefing als Vorlesetext](alg-3-briefing.html) · [Zur Lernaufgabe](../lernende/alg-3.html)

## Ziel und Rahmen

„Welches Depot ist zuständig?“: Vor x = 40 gilt Depot A, **an der Grenze und dahinter Depot B**. Die Lernenden sagen Wahrheitswerte und gewählte Zweige voraus, bauen eine eigene Melderegel und erklären, wie dieselbe Regel mit der jeweils anderen Frage dargestellt wird. Ein Aufruf von `falls … sonst …` führt genau einen Zweig aus.

Grundlage sind die [Lernendenfassung 2.0](../lernende/alg-3.html), der [Reihenkommentar](durchfuehrung-134.html) und der [Jahrgangsbrief](jahrgang.html). **15 + 15 + 30 + 15 = 75 Minuten**; weiterhin **405 Programmierminuten innerhalb der 36 Jahres-UE**. Aufgaben, Startprojekt und Lernwerk-Editor bleiben erhalten. Bildungsplananschluss: bestehende Projektplanung mit der dort dokumentierten Anhörungsfassung vom 21.09.2026; keine neue Aussage über deren verbindlichen Status und keine neue Fachprofilfreigabe.

ALG-2 liefert Zahl und Wahrheitswert sowie den x-Reporter als Voraussetzung. Vorher dessen tatsächliche Rückmeldung prüfen. Durchführung, individuelle Diagnose, Gerätezahl und Dauer der Dateiroutine sind noch unbekannt; die folgende Taktung setzt startbereite Geräte voraus. Geplante Aufgaben zählen nicht als bereits erhobene Diagnose.

**Ein gebündeltes Lernprodukt:** eigene Entscheidungsskizze mit Frage, wahr/falsch, zwei Meldungen und den drei Testeinträgen 39/40/41; dazu ein Satz zum Fragenwechsel und die XML-Datei. Die gemeinsame Einstiegstabelle bleibt Arbeitsnotiz. Kein zusätzliches Arbeitsblatt, zweites Testprotokoll oder neuer Upload.

## Vorbereitung und Material

- [Lernaufgabe ALG-3](../lernende/alg-3.html) und [zugehöriges Startprojekt](https://h4r7w16.github.io/ium-lernwerk/klasse7/programmieren/snap/lernwerk.html?aufgabe=alg-3) bereithalten. **Starten** setzt hier x = 40, y = 0 und Richtung 90°. Die zunächst lose Verzweigung wird dadurch noch nicht ausgeführt. Sie muss unter den Startstapel einrasten.
- Im Startprojekt prüft die Verzweigung bereits `x-Position < 40`; im ersten Zweig steht `sage Bereich A`, der sonst-Zweig ist leer. Unter **Bausteine → Aussehen** liegt `sage Hallo!`. Text ändern und in den **sonst-Zweig** einsetzen; nicht versehentlich eine zweite Meldung im ersten Zweig anfügen. „Bereich A/B“ und „Depot A/B“ sind bei eindeutiger Zuordnung fachlich gleichwertig.
- **Startposition und Regelgrenze unterscheiden:** Für Tests die x-Zahl im blauen Startblock ändern. Die 40 im Vergleich bleibt die feste Depotgrenze. Nach jeder Änderung erneut Starten drücken. Danach bleibt der Ort gleich; das Programm meldet nur das Depot. Die Setzung des Testorts am Anfang ist keine zusätzliche Fahrt durch die Verzweigung.
- Bestehende [ALG-3-Sicherung](sicherung.html) samt Beispiel nur für den späteren Abgleich bereithalten. Projiziert werden Einstiegstabelle aus der Lernaufgabe, tatsächlicher Code und die gemeinsame Entscheidungsskizze. Keine zusätzliche Präsentation nötig.
- Auf einem vorgesehenen Safari-Schulgerät vorher **Datei speichern → Datei öffnen** mit neutraler Kennung und vereinbartem Ablageort erproben. Zielname `ALG-3_Kennung.xml`; keine Anmeldung oder Veröffentlichung von Schülerprojekten erforderlich.
- Bei Partnergeräten: eine Person bedient, die andere sagt Bedingungswert und Zweig voraus. Zur eigenen Fassung wechseln. Beide skizzieren und erklären selbst. Bei Einzelgeräten genügt der kurze spätere Partnerabgleich; fehlenden Austausch übernimmt die Lehrperson.

## Verlauf · 75 Minuten

| Zeit | Lehrperson und konkreter Impuls | Lernhandlung und Beobachtung |
|---|---|---|
| **0–3** | Depotgrenze zeigen: „Bis vor 40 ist A zuständig. Genau 40 gehört schon B. Der Rover soll nur die richtige Meldung zeigen.“ | Regel in eigenen Worten wiedergeben. Das Grenzschild ist eine Entscheidungslinie, kein Fahrziel. |
| **3–8** | „Prüfe für 30, 40 und 50 beide Bedingungen. Noch nicht ausführen. Ist nicht größer dasselbe wie kleiner?“ | Jede Person trägt wahr/falsch in die vorhandene Einstiegstabelle ein. Erste Überlegung sichtbar lassen. |
| **8–12** | Ergebnisse vergleichen: „Bei welcher Position unterscheiden sich die beiden Fragen? Erkläre erst den inneren Vergleich, dann nicht.“ | `x < 40`: wahr/falsch/falsch. `nicht (x > 40)`: wahr/wahr/falsch. Unterschied bei 40 begründen; zweiter Ausdruck schließt die Grenze ein. |
| **12–15** | Auf die vorbereitete Verzweigung übertragen: „Wenn die Frage wahr ist, welcher Zweig läuft? Was passiert bei falsch?“ | Wahrzweig und sonst-Zweig am Code zeigen. Nicht zwei aufeinanderfolgende Prüfungen oder Dauerüberwachung hineinlesen. |
| **15–19** | Starten vorführen, x = 40 ablesen: „Warum sehen wir noch keine Depotmeldung? Was fehlt und welcher Stapel ist noch lose?“ | Startstapel und Verzweigung erkennen. Fehlende sonst-Meldung benennen, nicht die Bedingung ändern. |
| **19–25** | Meldungsblock gemeinsam in den sonst-Zweig einsetzen und ganze Verzweigung unten an den Startstapel hängen. „Bei 40: Wert der Bedingung, gewählter Zweig, erwartete Meldung?“ Erst danach starten. | **falsch → sonst → B** vorhersagen und prüfen; x bleibt nach der Testort-Setzung 40. Sitzen Block und Zweig am richtigen Ort? |
| **25–30** | „Teste 30. Welche Zahl ist dein Testort, welche unsere Regelgrenze?“ Nur Start-x ändern, erneut starten. | **wahr → erster Zweig → A**. Regelgrenze bleibt 40, Meldung und numerischer x-Wert werden verglichen. |
| **30–37** | „Welche Frage möchtest du zuerst stellen: vor 40 oder an beziehungsweise hinter 40? Wie sollen deine Meldungen heißen?“ Nach etwa fünf Minuten kurz nachfragen: „Was ist deine Frage genau bei 40?“ | Eigene Frage wählen und als Raute skizzieren; wahr/falsch mit passenden Meldungen verbinden. Jede Person muss den Grenzfall erklären können. |
| **37–45** | „Baue deine Fassung. Dein Programm soll melden und stehen bleiben.“ Bei Partnergeräten Bedienrolle wechseln. Bei Hilfebedarf die Frage sprachlich klären, bevor eine Formel angeboten wird. | Bedingung, beide Meldungszweige und Skizze in Übereinstimmung bringen. Keine Bewegungs- oder Wiederholungsblöcke ergänzen. |
| **45–53** | „Prüfe 39, 40 und 41. Sage jeweils zuerst deine Meldung voraus und zeige den gewählten Zweig.“ Start-x ändern, Grenze 40 erhalten. | Drei Tests direkt an der Skizze: Erwartung vor dem Lauf, tatsächliche Meldung und kurze Beobachtung danach. x bleibt jeweils am gesetzten Testort. |
| **53–60** | „Was belegt dein Grenztest? Passen Frage, Pfeile, Code und Meldungen zusammen?“ Gezielter Zwischenblick auf Skizze und einen tatsächlichen Lauf. | Eine Abweichung erklären und verbessern; betroffenen Fall erneut prüfen. Bei fehlerfreier Fassung die Begründung für 40 schärfen. Keine Pflicht, künstlich einen Fehler zu erzeugen. |
| **60–63** | „Erklärt euch 40 am Diagramm. Welche Frage habt ihr gewählt, welcher Pfeil führt zu B?“ Bei Bedarf selbst kurz zuhören. | Konkretes Peer-Feedback und eine unklare Stelle nachbessern. Beide Personen erklären selbst. |
| **63–69** | Neuer Kurzfall, zuerst individuell: „Stelle nun die jeweils andere Frage. Sage für 39 und 40 den Zweig voraus. Was muss außer der Bedingung angepasst werden, damit dieselben Depots zuständig bleiben?“ | Neue Frage mit neuer Zweigzuordnung planen, prüfen und am eigenen Diagramm ergänzen. Ein Satz erklärt, warum dieselben Meldungen erhalten bleiben. |
| **69–70** | Antworten bündeln: „wahr gehört zur Frage, nicht immer zu Depot A. Die Grenze gehört B.“ Gemeinsamen Merksatz sichtbar lassen. | Bedingung und Zuordnung getrennt benennen; Skizze und kurzer Satz dienen als Sicherung. |
| **70–75** | Eigene Datei speichern und wieder öffnen. „Erkennst du deine Frage und Meldungen wieder? Stelle Start-x auf 40 und prüfe erneut.“ | Eigene Fassung identifizieren; 40 liefert B, ohne Bewegung nach der Testort-Setzung. Download allein genügt nicht als erfolgreiche Datei-Rückkehr. |

## Lösungen und zentrale Sicherung

| Bedingung bzw. erste Frage | 30 | 40 | 50 | Zuordnung |
|---|---|---|---|---|
| `x-Position < 40` · vor 40? | wahr | falsch | falsch | wahr → A, falsch → B |
| `nicht (x-Position > 40)` · nicht größer als 40? | wahr | wahr | falsch | Als A-Frage ungeeignet: ordnet 40 fälschlich A zu. |
| `nicht (x-Position < 40)` · an oder hinter 40? | falsch | wahr | wahr | wahr → B, falsch → A |

Für **39/40/41** sind die Meldungen immer **A/B/B**. Bei der Frage „vor 40?“ lauten die Zweigwerte wahr/falsch/falsch; bei „an oder hinter 40?“ falsch/wahr/wahr. Verschiedene klare Meldungstexte und logisch gleichwertige Bedingungen akzeptieren. Entscheidend sind die ursprüngliche Grenze und die begründete Zuordnung, nicht das Nachbauen einer Musterlösung.

Beim Wechsel zwischen diesen beiden Fragen kehren sich die Wahrheitswerte um. **Die beiden Meldungen müssen deshalb den jeweils anderen Zweigen zugeordnet werden.** Nur die Bedingung zu ändern vertauscht sonst die Depotmeldungen. Erwartung erst vorhersagen lassen, diese Lösung nicht vor dem eigenen Kurzfall projizieren.

**Zentrale Sicherung an Tafel/Projektion und in der vorhandenen Skizze:** Raute mit gewählter Frage; ausgehende Pfeile wahr/falsch; Meldungen A/B. Dazu „Ein Aufruf prüft die Bedingung und führt genau einen Zweig aus. Dieselbe Depotregel kann mit einer anderen Frage und passender Zweigzuordnung beschrieben werden. Genau 40 gehört B.“ Drei Testeinträge bleiben an der Skizze, der Satz zum Fragenwechsel direkt daneben. Die [öffentliche Sicherung](sicherung.html) erst nach dem eigenen Versuch zum Abgleich nutzen; sie ist kein geschützter Test.

## Hürden und passende nächste Hilfe

| Beobachtung | Nächster Impuls bzw. Hilfe |
|---|---|
| Starten setzt x, zeigt aber keine neue Meldung. | „Hängt die Verzweigung wirklich am Startstapel? Ist im gewählten Zweig ein Meldungsblock?“ Danach nur den vollständigen Startstapel ausführen. |
| Zwei Meldungen stehen im ersten Zweig, sonst ist leer. | Beide C-förmigen Innenräume zeigen. Meldungsblock in den unteren Innenraum ziehen; der Inhalt muss dort sichtbar eingerastet sein. |
| Für einen Test wurde die Grenze verändert. | Start-x und Vergleichs-40 getrennt zeigen lassen: „Wo steht der Rover? Nach welcher unveränderten Regel entscheiden wir?“ Grenze wiederherstellen und denselben Test wiederholen. |
| „Nicht größer“ wird als „kleiner“ gelesen. | Zuerst `40 > 40` beantworten, danach dessen Wert umkehren. Gleichheit an der Grenze ausdrücklich besprechen. |
| Wahr wird automatisch A zugeordnet. | „Was fragt deine Raute? Was bedeutet Ja genau bei 40?“ Frage in Alltagssprache beantworten, dann die zugehörige Meldung wählen. |
| Nach Fragenwechsel sind die Meldungen vertauscht. | Einen Fall vom Fragewert über den Pfeil bis zur Meldung verfolgen lassen. Erst danach den zweiten Zweig anpassen und neu prüfen. |
| Skizze oder Sprache blockiert. | Raute mit zwei leeren Pfeilen anbieten; Frage und Meldungen selbst eintragen lassen. Satzanfänge: „Bei 40 ist meine Bedingung …, deshalb …“, „Die Frage ändert sich, die Depotregel bleibt …“. Mündliches Erklären zulassen. |

**Schrittmodus** optional zur verlangsamten Verfolgung nutzen. Ein Schritt ist ein Auswertungsschritt, nicht garantiert ein ganzer Zweig oder eine neue Bedingungsprüfung. Bis zur gewählten Meldung verfolgen, dann wieder normal arbeiten. Die Verzweigung prüft pro Aufruf einmal; eine nachträgliche Testortänderung löst ohne neuen Start keinen neuen Aufruf aus.

Sichere Lernende können freiwillig prüfen, ob ihre Regel auch an einem Zwischenwert wie 39,5 stimmt. `x > 39` würde die drei ganzzahligen Tests bestehen, aber die ursprüngliche Grenze verändern. Drei erfolgreiche Tests sind daher kein vollständiger Beweis für jede eingegebene Zahl. Das ist eine mögliche Vertiefung oder gezielte Hilfe, keine vierte Pflichtabgabe.

## Diagnose und Anschluss an ALG-4

**Regulärer Anschluss:** Die Person erklärt bei 40 Bedingungswert, gewählten Zweig und B-Meldung, bringt eigene Skizze und Code in Übereinstimmung und begründet den Fragenwechsel mit angepassten Zweigen. Eine richtige B-Anzeige oder kopierte Musterzeichnung allein genügt nicht. ALG-4 kann daran die wiederholte Prüfung einer Abbruchbedingung anschließen; die einmalige Verzweigung aus ALG-3 bleibt davon zu unterscheiden.

**Nachsicherung nach Befund:** Bei Grenzverwechslung zunächst 40 und einen Nachbarwert ohne Lauf begründen lassen. Bei unklarer Zweigwahl eine andere Frage am selben Ort verfolgen und erneut erklären lassen. Im Partnergerät auch die nicht bedienende Person ansprechen. Fehlen individuelle Antworten, beginnt ALG-4 mit einer kurzen Ersatzdiagnose statt ungeprüft vorausgesetztem Verständnis. Geräte-/Dateiprobleme getrennt von fachlichen Lücken dokumentieren.

## Zeitraster, Ausfall und Rückfluss

**Variante 45 + 30 Minuten:** 0–43 wie oben; 43–45 die gegebenenfalls noch unvollständige eigene Fassung speichern und den offenen Schritt an der Skizze markieren. Nach der Pause 45–48 wieder öffnen; 48–60 Tests und Abgleich fortsetzen. 60–75 bleiben unverändert. Speichern und Rückkehr liegen innerhalb der dreißigminütigen Eigenphase; kein geöffneter Tab über die Pause wird vorausgesetzt. Die Variante setzt eingeübte Dateiroutine voraus und ist noch nicht zeitlich erprobt.

Bei Verzögerung zuerst freiwillige Vertiefung und weitere Plenumsbeiträge weglassen. Eigene Melderegel, Grenztest und Erklärung zum Fragenwechsel schützen. Unvollständige Datei-Rückkehr oder fehlende Diagnose ausdrücklich offen halten und nachholen. Nötige Zusatzunterstützung nach [Jahrgangsbrief](jahrgang.html) im vorhandenen Jahreskonto von **135 Unterstützungsminuten** konkret buchen; keine heimliche Verlängerung der 75 Minuten oder Doppelbuchung.

Bei Geräteausfall Bedingungen, Diagramm und Vorhersagen auf Papier bearbeiten, gegebenenfalls Demonstrationslauf nutzen. Eigene Programmbedienung und Datei-Rückkehr sind damit nicht nachgewiesen. Bei größerem Zeitverlust den Anschluss anhand der tatsächlichen Lage neu planen.

**Kompakter WU-Check:** Grenzvergleich und Fragenwechsel fordern begründetes Denken (Band 1); Hilfen knüpfen an beobachtete Verwechslungen an (Band 3); eigene Frage, passende Rückmeldung und individueller neuer Fall erhalten den fachlichen Anspruch (Band 6). Das ist eine redaktionelle Planungsprüfung, kein Wirksamkeitsnachweis. Nach dem Einsatz festhalten: tatsächliche Minuten, individuelle Grenz-/Zweigerklärung, benötigte Hilfe, Datei-Rückkehr und nächster Schritt vor ALG-4. Bei Änderungen Briefing mitführen.
