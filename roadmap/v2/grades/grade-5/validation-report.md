# IUM-V2-R5 – Review und Validierung

Stand: 2026-09-06. Ausgangscommit `dc059cffcb2866c6e0d7df3c83dbc0410d14d680`. Prüfart: KI-Dokumentenselbstreview durch Codex. Die AUD-Nutzerabnahme liegt vor; R5-Nutzerabnahme steht aus. Keine unabhängige Prüfung behauptet.

## Fachliche Gegenprüfung

1. **Vollständiger Eingang:** Alle 144 einschlägigen Rohrecords sind einzeln geführt. 85 Kompetenzen werden von 59 Auslegungskontexten unterschieden. Keine unbemerkte Beschränkung auf alte Coverage-Einträge.
2. **Normative Geltung:** 25 amtliche BMB-Kompetenzen bleiben Klasse 5 zugeordnet; keine wird nach Klasse 6 verschoben. Die 60 orientierenden Kompetenzen haben den gemeinsamen Quellscope 5/6; die projektinterne Teilung ist ausdrücklich begründet.
3. **Ehrliche Privatheitslücke:** Die vollständige Prüfung zeigt sechs Eigenbezugsrecords, darunter zwei amtliche. Alle bleiben offen; die Roadmap meldet keine vollständige Basiskurserfüllung. Fiktive Fälle schließen diese Lücke nicht.
4. **Selbstdarstellung:** Der andere amtliche Record RK-003 verlangt Folgenabschätzung und Bewertung, aber keinen privaten Nutzungsbericht. Beide Denkhandlungen sind in M05 vorgesehen und bleiben als tatsächliche Evidenz ungeprüft.
5. **Neue Folge:** Arbeitsraum, Quellenarbeit, echte Kooperation, Medienprodukt, Urteil und algorithmische Grundbegriffe sind aus Voraussetzungen aufgebaut. Alte Modulfolge, Zeitmodell und LXP05-Oberfläche sind keine Produktionsvorlage.
6. **Zeit ohne Doppelzählung:** 1260 Minuten Kern ergeben 28 Einheiten. Jede Modulzeit enthält Übung, selbstständige Anwendung, Feedback und Sicherung. 32/36/40-Varianten addieren nur zusätzliche Wiederaufnahme, Organisation, Puffer und gegebenenfalls Flex.
7. **Flex bleibt optional:** Keine Pflichtkompetenz hängt ausschließlich an F01 oder F02. Bei knapper Zeit wird Vertiefung ausgelassen; bei zusätzlichem Förderbedarf wird sie durch Übung ersetzt. Unter 32 Einheiten ist Neuplanung nötig.
8. **Werkzeugmatrix:** Drei reguläre Arbeitskontexte tragen zunehmend selbstständige Werkzeugnutzung. Keine künstliche Zusatzaufgabe, kein Zusatzstundenblock und keine Abdeckung aus bloßen Klicks.
9. **Digitale/kooperative Nachweise:** Ein Schulnetzlogin, digitaler Kommunikationsweg und praktisches Programmieren können nicht durch einen Papierfallback belegt werden. Für M03 ist ein individueller Beitrag mit gemeinsamer Revision vorgesehen; reale Kanalfreigabe bleibt offen.
10. **Lernarchitektur und Feedback:** Lernziel, Handlung und Produkt sind pro Modul verbunden; begrenzte Unterstützung, konkrete Revision und zeitversetzte Wiederaufnahme sind vorgesehen. Die acht Qualitätsdimensionen aus LXF bleiben Vertragsgrundlage. Die WU-Perspektiven Angebotsnutzung und formatives Feedback wurden als Kontrollfragen verwendet, nicht als pauschaler Wirksamkeitsbeweis.
11. **Quellen und Anspruch:** Aktuelle amtliche Fachseite und Lesehilfe wurden geprüft; ihre Geltung bleibt unterschiedlich. Modulprinzipien verweisen auf vorhandene abgenommene Claims. Konkrete künftige Materialien/Assets und Lizenzentscheidungen brauchen später einen eigenen Check.
12. **R6 und Reifeachsen:** 17 orientierende Aufträge sind mit Begründung übergeben, R6 ist noch nicht begonnen. 16 Grundlagenfragen und vier R5-Eintrittsgates bleiben offen. Technische Vertragsprüfung, Curriculum-Coverage, Implementierung, Nutzung, Pilot und Freigabe werden nicht vermischt.

## Ergebnis

Der Planungsumfang ist zur Nutzerabnahme geeignet, mit sichtbarer Einschränkung: Es gibt keine tragfähige Nachweisentscheidung für sechs private Eigenbezüge, kein bestätigtes lokales Jahreskontingent und keine echte Geräte-/Nutzungserprobung. Diese Punkte verhindern eine uneingeschränkte Einsatz- oder Coveragefreigabe; sie werden durch die Planungsabnahme nicht geschlossen. Die neuen Module werden als Konzept geprüft, nicht als einsatzfertiges Material.

## Technische Verifikation

Frische Ergebnisse am 6. September 2026:

- 21 R5-Vertragstests bestanden. Die ursprünglichen Tests liefen vor Implementierung rot. Ein zusätzlicher Reviewbefund zu nicht auflösbaren Planungsabschnitten wurde mit eigenem zunächst fehlschlagendem Test geschlossen.
- Die fokussierte Regression mit den bisherigen V2-/GOV-/AUD-Tests bestand vor dieser Nachschärfung mit 228 Tests. Danach wurden alle 21 R5-Tests erneut ausgeführt.
- `npm run test:python`: **904 Tests bestanden** in 118,723 Sekunden, einschließlich der Nachschärfung. IUM11-Ablehnungen in der Ausgabe gehören zu erfolgreichen Negativtests.
- `npm run verify:v2`: integriertes Gate bestanden. Alle vier neuen JSON-Instanzen gegen Draft 2020-12 mit AJV geprüft.
- 24 R5-Prüfeingänge über SHA-256/UTF-8/LF gebunden; sechs lokale Markdownlinks geprüft. Die vollständige Recordmenge, Bindungsgrade, Elternbezüge, acht Projektanforderungen, Modul-/Prinzipienverweise, Voraussetzungen und Zeitsummen werden geprüft.
- Git-Diff und Scope geprüft: V1-Daten, zentrales Anforderungsregister und die bestehenden versiegelten Grundlagen-/AUD-Eingänge unverändert. Die AUD-Abnahme ist additiv.

Nach Eintrag dieses Berichts werden seine Dateibindung aktualisiert und die R5-Tests sowie das integrierte Gate erneut geprüft. Der finale Commit und der gesonderte Vault-Abgleich werden im Session-Handoff festgehalten. Keine Produkt- oder Abhängigkeitsdateien geändert; kein neuer Produktbuild, Realgeräte-, Nutzungs- oder Unterrichtstest ausgeführt oder behauptet.
