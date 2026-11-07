# M07-Pilot: Informationskarte verständlich überarbeiten

Stand: 07.11.2026. Isolierter Pilot auf Basis `2c3b556`, Branch `feat/ium-lernbogen-pilot-20261107`. Dieser Plan wurde vor der Inhaltsänderung festgehalten. Teilauftrag: gezielte redaktionelle Überarbeitung; kein neuer Lernbogen, kein Rendererumbau und keine Änderung des Zeitkontos. Reviewart: redaktioneller Selbstreview durch den mit M07 beauftragten Agenten, keine Unterrichtsbeobachtung.

## Lernbewegung vor der Änderung

Die Lernenden beginnen mit einer echten Erklärfrage: Warum nennen ältere Darstellungen neun, heutige acht Planeten? Am fremden Bibliotheksbeispiel unterscheiden sie auffällige Gestaltung, Verständlichkeit und belegte Richtigkeit. Eine kurze Bedienprobe macht Zeichen, Absatz und Objekt als verschiedene Eingriffsmöglichkeiten erfahrbar. Danach übersetzt das Zweierteam geprüfte Aussagen in eine eigene Karte; jede Person formuliert und gestaltet selbst. Eine andere Person liest ohne Voraberklärung, sodass die Differenz zwischen beabsichtigter und tatsächlicher Aussage sichtbar werden kann. Eine begründete Revision bearbeitet diese Verständnisstelle, während Rechteprüfung und Empfängerproben die reale Verwendbarkeit sichern. Der abschließende Transfer verändert Zielgruppe und Zugangsbedingungen; spätere Abrufe prüfen die Unterscheidungen erneut.

## Gelungene Verbindungen und konkrete Hürden

- Das Bibliotheksmodell zeigt einen vollständigen Denkweg an einem anderen Thema; das Pluto-Produkt bleibt eine eigene Gestaltungsleistung. Die Unterscheidung einer geänderten Einteilung von einem Verschwinden Plutos muss erhalten bleiben.
- `austausch/kanal` verlangt echtes Lesen ohne Voraberklärung. `revision/ueberarbeiten` knüpft daran eine eigene Änderung und erneutes Lesen. Diese Verbindung ist der Kern, nicht die Anzahl der ausgefüllten Felder.
- Die Hauptanweisung der Revision setzt zwar Verbesserung voraus, doch editierbare v2, PDF-Export und Wiederöffnen stehen nur im eingeklappten Arbeitsweg. Teilen und Abschluss benötigen diese Dateien anschließend. Die Ausgabe wird durch `class5-content.cjs` erzeugt: `action` ist direkt sichtbar, `routes` liegt digital in geschlossenen `details`.
- Die Bedienprobe fordert echte Operationen und zusätzlich Dateiname plus drei schriftlich beschriebene Änderungen. Planung und Erstfassungsnachweis verlangen teilweise dieselben Angaben erneut; Projektspur und Lernwerk können als doppelte Pflicht verstanden werden.
- Die Revision verlangt selbst bei korrekter Rechteleiste eine zusätzliche Präzisierung. Eine fachlich unbegründete kosmetische Änderung wäre ein schlechter Ersatz für die Prüfung der vorhandenen Angaben.

## Enges Änderungspaket und erwartete Bilanz

1. Dateifolge in der vorhandenen sichtbaren Hauptanweisung nennen, gleichlautende Speicheranweisungen im Klapptext kürzen. Auch die Erstfassung sichtbar als editierbare v1 sichern.
2. Projektspur und Lernwerk als alternative Orte für dieselben kurzen Nachweise benennen. Planungseintrag bei Fertigstellung ergänzen oder aktualisieren, nicht nochmals abschreiben. Tatsächliche Produktdateien bleiben separat.
3. Die drei Formatierungsarten direkt am Gerät zeigen und erklären. Die schriftliche Werkstattliste entfällt; die tatsächliche Bedienung und der individuelle Abschlussnachweis bleiben. Das Antwortfeld wird optional, nicht der Gerätenachweis.
4. Rechteangaben prüfen und bei Bedarf korrigieren; bereits korrekte Angaben an einem konkreten Element begründet bestätigen. Die fachliche oder gestalterische Revision nach echter Rückmeldung bleibt verpflichtend.
5. Betroffene Lehrhinweise und den M07-Reihenkommentar synchronisieren. Jahresplanung, Zeit, Schrittzahl, Quellen, Materialien, spätere Abrufe und gemeinsame Renderer bleiben gleich.

Gewinn erwartet: früh erkennbare Dateivoraussetzungen und weniger doppelte Schriftarbeit bei erhaltener Diagnose. Möglicher Verlust: Die entfallende schriftliche Werkstattliste hinterlässt weniger dauerhaftes Kontrollmaterial. Deshalb muss die direkte Gerätevorführung beobachtbar bleiben; Selbstbehauptung oder bloßer Dateiname reichen nicht. Die Rechteprüfung darf nicht als Ausweg aus der tatsächlichen Produktrevision dienen.

## Prüfumfang vorab

Vollständige kanonische Folge einschließlich Brücke, Zwischenabruf, Austausch, Revision, Teilen, Abschluss und späterem Abruf erneut durchgehen. Gegenfälle: (a) missverständliche eigene Karte, (b) bereits richtige Rechteleiste bei erforderlicher Verständlichkeitsrevision, (c) nur ein gewählter Notizort, (d) ausgefüllte Felder ohne tatsächliche Gerätehandlung. Sichtbare Dateifolge im generierten HTML bei geschlossenen Arbeitswegen prüfen; Print-/Lehrabhängigkeiten abgleichen. Bestehende Tests, Build und abschließende Fassungsbindung integriert der Root-Agent; hier keine vorweggenommene Pass-Aussage. Echte Schulgeräte, Partnerreaktionen, Unterrichtszeit und Lernwirkung bleiben unerprobt.

## Nachprüfung der Endfassung

Die Umsetzung betrifft `prototypes/shared/inhalte/klasse6/medienprodukt.json`, den Reihenkommentar in `prototypes/shared/class6-media-project.cjs` und diesen Bericht. Nach ausdrücklicher Freigabe des Root-Agenten wurde zusätzlich genau `prototypes/shared/inhalte/assets/medienprodukt6/projektspur.txt` synchronisiert: Der bestehende Inhaltsvertrag verlangt denselben Text in Download und `printText`. Keine gemeinsamen Renderer, Kataloge, Versionskennungen, Quellen, Zeitkonten oder Git-Commits geändert.

### Durchgang durch den ganzen Lernweg

| Abschnitt | Vergleich vor / nach und Beurteilung |
|---|---|
| Brücke und Auftrag | Die sechs früheren Abrufe, Zeitzuordnung und fremde Bibliothekskarte bleiben unverändert. Das andere Thema liefert einen Denkweg, ohne das eigene Pluto-Produkt vorzugeben. |
| Werkstatt | Zeichen, Absatz, Objekt, Zwischenablage, Speichern und erneutes Öffnen bleiben echte Bedienhandlungen. Die Rückkehr fordert jetzt direkte Vorführung und Erklärung statt zusätzlicher schriftlicher Liste. Das optionale Notizfeld ist kein optionaler Gerätenachweis. |
| Entwurf und R12 | Belegter eigener Satz, Rollenwechsel, zehnminütige Zwischenkontrolle und erklärendes Objekt bleiben erhalten. Die Wahl Projektspur oder Lernwerk steht direkt im Planauftrag, weil `workNotice` in M07 ohne Abschlussblock nicht zuverlässig auf jeder Lernseite erscheint. Bei der Erstfassung wird dieser Eintrag ergänzt. Die sichtbare v1-Anweisung bereitet den späteren Vergleich vor. R12 und der Rückweg zum Entwurf bleiben gleich. |
| Austausch | Die andere reale Person öffnet die Karte und erklärt ohne Voraberklärung die unterschiedlichen Planetenzahlen. Rückmeldung, Rückfrage und Aushandlung bleiben unverändert. Es wird keine zusätzliche Lesetest-Dokumentation verlangt. |
| Revision | Die Verständlichkeitsänderung, die eigene Ausführung jeder Person und das erneute Lesen bleiben verbindlich. Korrekte Rechteangaben können begründet bestehen bleiben. v2, Export und Wiederöffnen stehen jetzt in der sichtbaren Hauptanweisung; im Klapptext entfällt dieselbe Speicheranweisung. |
| Teilen und Abschluss | Beide tatsächlichen Empfangsproben, der eigene Beitrag am Produkt und der Transfer für Klasse 3 ohne Internet bleiben unverändert. Die vorhandene Abschlussvorstellung kann auf die nun ausdrücklich herzustellende PDF zurückgreifen. Der Teilauftrag spricht von Produktdatei und Notizen, sodass die alternative Projektspur nicht durch eine spätere Lernwerk-Pflicht aufgehoben wird. |
| Spätere Abrufe | R13 fordert Verbesserungen einer fremden Karte, R14 Zugangskorrektur, anderen Teilweg und Revisionsnachweis. Beide beginnen ohne alte Notizen. Keiner benötigt die entfallene schriftliche Werkstattliste. v1/v2, echte Rückmeldung und begründete Änderung bleiben als Revisionsbelege erhalten. |

### Konkrete Gegenfälle, redaktionell durchgespielt

1. **Missverständliche Karte:** Eine Erstfassung wie „Früher gab es neun Planeten, heute nur noch acht“ kann einen verschwundenen Planeten nahelegen. Eine mögliche Revision benennt stattdessen die geänderte Einteilung seit 2006 und beschriftet den Zeitvergleich mit „Pluto als Planet eingeordnet“ und „Pluto als Zwergplanet eingeordnet“. Das Beispiel ist eine redaktionelle Aufgabenbearbeitung, keine beobachtete Lernendenäußerung. Der Auftrag verlangt weiterhin den tatsächlichen Lesetest, bevor eine konkrete Rückmeldung als Beleg festgehalten wird.
2. **Rechte bereits korrekt:** Bei eigenen Formen und einer passenden Herkunfts-/Rechteleiste kann das Team diese Angaben am konkreten Element bestätigen. Eine echte Text-/Gestaltungsrevision bleibt durch `revision/ueberarbeiten.text`, den ersten Arbeitsweg und das erste Kriterium erforderlich; die Bestätigung ist kein Ersatz dafür.
3. **Nur Projektspur oder nur Lernwerk:** Eigener Satz und Beleg werden geplant, beim Entwurf ergänzt, Rückmeldung und Vorher–Nachher begründet festgehalten. Die Produktdateien bleiben gesondert. Dieselben inhaltlichen Nachweise sind an beiden Orten erreichbar; die spätere Wiederaufnahme verlangt ohnehin den ersten Versuch ohne Notizen.
4. **Felder ohne Handlung ausgefüllt:** Eine schriftliche Behauptung reicht weiterhin nicht: Werkstatt verlangt sichtbare Bedienung, Austausch das Öffnen durch eine reale Person, Teilen zwei Empfangsproben und Abschluss den eigenen Beitrag an konkreten Dateien. Der Umgehungsweg wird durch Beobachtung begrenzt, nicht technisch ausgeschlossen.

### Tatsächlich ausgeführte Prüfung

- Kanonische Quelle nach Änderung erneut durchgegangen; unveränderte Brücke, fachliche Sachinformationen, spätere Abrufe und Zeitangaben mit dem Diff abgeglichen. Lehrhinweise, Briefing und Reihenkommentar auf widersprechende Rechte- oder Notizpflichten geprüft.
- `A.validate(pack)`, `R.render(pack)` und `A.assets(pack)` ausgeführt: erfolgreich, 27 M07-Ausgabeseiten und vier Assets. Keine vollumfängliche Browser-/Drucksichtung in diesem Teillauf behauptet.
- Im erzeugten HTML sämtliche `details`-Inhalte für eine gezielte Strukturprüfung ausgeblendet: sichtbare editierbare v1 sowie v2 → PDF → erneutes Öffnen vorhanden. Direkte Gerätevorführung, alternative Notizorte, echte Leserprobe und verbindliche Revision ebenfalls geprüft. Papier-HTML enthält die neue Hauptanweisung und den Gerätenachweis.
- Download und Drucktext stimmen überein. Der erste Assetcheck meldete einen CRLF/LF-Unterschied nach dem lokalen Schreiben; LF korrigiert und denselben Check erneut erfolgreich ausgeführt.
- `git diff --check` für die eigenen Dateien ohne Befund. Bestehende Tests, integrierter Build, tatsächliche Ansichten und abschließende Fassungsbindung werden vom Root-Agenten geprüft; deren Ergebnis wird hier nicht vorweggenommen.

### Bilanz und bewusst verbleibende Grenzen

Die Revision klärt notwendige Voraussetzungen am Arbeitsort und entfernt doppelte Beschreibungen. Sie reduziert keine fachliche oder digitale Zielhandlung und führt weder einen neuen Pflichtschritt noch eine neue Dokumentationsform ein. Die 210 Kernminuten sowie 39 + 5 + 12 Abrufminuten bleiben gleich; eine Zeitersparnis ist plausibel, aber nicht gemessen.

Weniger schriftliche Werkstattspur bedeutet weniger nachträglich lesbares Kontrollmaterial. Die direkte Gerätevorführung und der bestehende individuelle Abschlussnachweis tragen diese Diagnose; Lehrende müssen beide tatsächlich beobachten. Das bereits vorhandene Weiterprüfen eines zunächst verständlichen Produkts mit anderer Darstellungsgröße oder Zielgruppe bleibt erhalten. Es kann bei sehr sicheren Teams Zeit beanspruchen; im engen Pilot wurde es nicht um eine neue Phase erweitert. Gesamtanforderung und Unterrichtszeit müssen im realen Einsatz erprobt werden. Die redaktionelle Prüfung bestätigt weder reale Zusammenarbeit noch Gerätezugang oder Lernwirkung.
