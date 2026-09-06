# IUM-V2-R6 – Review und Validierung

Stand: 2026-09-06. Ausgangscommit `5146310ae855636d3529e8d31b079b5ca265da6e`. R5 ist ausdrücklich abgenommen, R6-Nutzerabnahme steht aus. Prüfart: KI-Dokumentenselbstreview durch Codex; keine unabhängige Fachprüfung.

## Fachliche Gegenprüfung

1. **Echter Anschluss statt angenommener Kohorte:** R5-Planungsabnahme ist kein Lernnachweis. Sechs noch nicht durchgeführte Einstiegsklärungen besitzen Produkt, Kriterium, Reaktion und eigenen Zeitposten. Insbesondere für 2026/27 wird ein durchlaufenes V2-Vorjahr nicht vorausgesetzt.
2. **Vollständige Übergabe:** Alle 17 vereinbarten Erstzuordnungen sind im R6-Kern. 39 weitere Kompetenzen besitzen explizite Fortschrittsbeschreibungen gegenüber R5. Keine stille Verschiebung in Flex oder nach R7.
3. **Quellentreue:** Alle 85 einschlägigen Orientierungsrecords werden geführt; 60 Kompetenzen und 25 Auslegungskontexte getrennt. Amtliches BMB-Klasse-5-Curriculum wird nicht zu einem neuen Klasse-6-Pflichtkatalog.
4. **Nachweisgrenzen:** Vier orientierende Eigenbezüge bleiben offen, zwei amtliche BMB-Altfragen werden zusätzlich mitgeführt. Weder Fallarbeit noch private Nutzungserhebung wird zur vermeintlichen Lösung. Alle acht Projektanforderungen bleiben ebenfalls `unassessed`.
5. **Begrenzte Progression:** Netz-/Speichermodelle, Quellenwiderspruch, Dateninteressen und Codierungswahl erweitern die Nutzungsperspektive. Der Algorithmusblock vertieft Erklärung und Fehlerprüfung von Anweisungen/festen Wiederholungen; fortgeschrittene Klasse-7-Konstrukte werden nicht vorausgesetzt.
6. **Zeitrechnung:** 1215 Minuten Kern sind aus sieben neuen Lernhandlungen kalkuliert. Erklärung, angeleitete Übung, eigene Anwendung, Revision und Sicherung sind je Modul enthalten. 90 Minuten Einstiegsklärung und 0/45 Minuten zusätzliche Überbrückung werden getrennt addiert.
7. **Begrenztes Reparaturbudget:** Die knappe 32-Variante setzt tragfähigen Einstieg voraus. Breite Lücken oder Bedarf über 45 Minuten erfordern Neuplanung; Reserven werden nicht als beliebig ausreichend ausgegeben. Die 36-Variante ist eine unpilotierte Arbeitsannahme.
8. **Echte Integration:** M07 beschränkt das Produkt und verwendet bekannte Inhalte. Individueller Beitrag, aufgenommene Rückmeldung, Rechteprüfung und Revision sind geplant. Mehrere Recordverweise erzeugen keine zusätzlichen Unterrichtsminuten.
9. **Optionale Vertiefung:** Beide Flexmodule tragen keine exklusive Kompetenz. Bei zusätzlichem Förderbedarf ist Umplanung möglich; sie ändert den dokumentierten Kernanspruch nicht stillschweigend.
10. **Digitale Zielhandlungen und Fallback:** Modellskizzen können Netzverständnis belegen; offline simulierte Suche, Kanalnutzung oder Programmausführung ersetzen die praktische Zielhandlung nicht. Alle realen Zugänge sind noch zu prüfen.
11. **Lernarchitektur und Quellen:** Je Modul sind Ziel, Handlung, Produkt, Hilfen, Revision, digitale Funktion und Pilotfrage verbunden. LXF-Prinzipien und auditierte Übernahmeentscheidungen sind referenziert. Die Quellenprüfung aus R5 ist als übernommener Stand gekennzeichnet; keine neue Remoteprüfung behauptet.
12. **Eigenes Review und Übergang:** R6 bleibt im Nutzerreview. R7 erhält geplante Eingangsprodukte und muss Vorwissen erneut prüfen. Sechs R6-Gates und alle 16 Grundlagenfragen bleiben offen. Keine Reifeachse wird durch technische Tests auf Einsatz, Pilot oder Wirkung hochgestuft.

## Technische Ergebnisse

27 gezielte R6-Vertragstests wurden vor dem Validator angelegt; der erste Lauf scheiterte am noch fehlenden R6-Modul. Alle 27 Tests bestehen. Sie prüfen vollständige Quellmenge, R5-Anschluss, Pflicht-/Flextrennung, Privatheitsgrenzen, noch nicht beobachtetes Eingangswissen, Jahresrechnung, Referenzen, Gates, Abnahmecommit und Hashbindung.

Die vollständige Python-Suite besteht mit **931 Tests in 119,079 Sekunden**. Das integrierte V2-Gate und die vier JSON-Instanzen gegen AJV Draft 2020-12 bestehen ebenfalls. 29 Prüfeingänge werden gebunden; fünf lokale Markdownziele sind vorhanden. Nach Fertigstellung dieses Berichts werden seine Hashbindung und die unmittelbar betroffenen Prüfungen vor Commit nochmals kontrolliert.

Der erste Gesamtlauf hatte einen veralteten R6-Prüfstand gemeldet: Während dieses Laufs waren noch die Nachweisformulierung zu Akteursinteressen und der Prinzipienbezug zum verzögerten Abruf präzisiert worden. Der Hashschutz wies beide Änderungen korrekt zurück. Nach neuer Bindung wurde die vollständige Suite auf unverändertem Stand erfolgreich wiederholt. Kein technischer Restbefund im geprüften Umfang.

Die Integration verändert nur drei Aufrufe/Importe im zentralen Validator und sieben erwartete Fehlmeldungen im bestehenden Test. Versiegelte Vorgänger-, Grundlagen-, Audit- und Curriculumdateien bleiben unverändert; die R5-Abnahme ist additiv. Produktcode und Plattformkonfiguration sind nicht Teil von R6.

## Offene fachliche Grenzen

Reale Kohorte, Nettozeit, schulische Zugänge, konkrete Materialien/Tools und deren Zugänglichkeit sind noch unbekannt bzw. ungeprüft. Die sechs privaten Eigenbezüge benötigen eine spätere tragfähige Nachweisentscheidung. Zeitpassung, Nutzung der Lernangebote, Lernwirkung und Transfer sind nicht durch Dokumenten- oder Softwaretests belegt. Die Nutzerabnahme bestätigt eine Planung mit diesen Grenzen.
