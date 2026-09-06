# IUM-V2-R7 – Review und Validierung

Stand: 2026-09-06. R6-Abnahme am Commit `c38ff9b0b037539b37d6964091c38dc3c323344a` liegt vor, R7-Nutzerabnahme steht aus. Prüfart: KI-Dokumentenselbstreview durch Codex. Keine unabhängige Fachprüfung, keine beobachtete Kohorte und keine Unterrichtspilotierung.

## Fachliche Gegenprüfung

1. **Vollständiger Eingang:** 94 amtliche Aufbaukursrecords und 40 Klasse-7-Orientierungsrecords ergeben 134 einzeln geführte Einträge. 51 amtliche und 31 orientierende Kompetenzen werden von 52 Kontexten getrennt.
2. **Amtlicher Kern:** Alle 51 amtlichen Kompetenzen besitzen im Kern Zielhandlung, geplante Evidenz und Modulzeit. Prozesskompetenzen wie Softwaremodellierung, Codeadaption aus verschiedenen Quellen, tatsächlicher Austausch, Test, Teamreflexion, Vielfalt und eigener ethischer Standpunkt werden nicht nur nominell erwähnt.
3. **Orientierungsumfang:** 20 orientierende Kompetenzen liegen im Kern, fünf zusätzliche in M06 und drei in M07. Je Jahrespfad bleiben ausgelassene Records ausdrücklich offen. Die Gewichtung ist Projektentscheidung; Quellenrollen werden nicht verändert.
4. **Neue Reflexionsfragen:** DP-013/014/018 bleiben offen. Fachliche Teilanalysen sind vorgesehen, eigener Reflexionsanteil nicht dadurch belegt. Datensparsame Unterrichtsreflexion könnte möglich sein, ist aber noch nicht als tragfähiger Nachweis ausgestaltet. Keine pauschale Unmöglichkeit und keine private Offenlegung behauptet.
5. **Vorgängergrenzen:** Sechs frühere Eigenbezugsfragen und alle 16 Grundlagenfragen bleiben erhalten. Amtliche Klasse-5-Altfragen werden nicht zu neuen Klasse-7-Vorgaben umgedeutet.
6. **Progression 5–7:** Sieben Stränge binden konkrete R5-/R6-Module, den Wortlaut des geplanten R6-Produkts, R7-Ziele und Einstiegsklärung. Die tatsächliche Klasse 7 hat die neue Folge nicht nachweislich durchlaufen; Vorwissen bleibt nicht beobachtet.
7. **Neuer Konzeptaufbau:** Binärzahlen, Datenmengen/Präfixe, ASCII, Pixelgrafik, eigene reversible Codes und Codewortzahlen werden explizit aufgebaut. Variablen, Bedingungen, Wertefluss und Datentypen werden nicht aus der festen Wiederholung in R6 vorausgesetzt. Codierung und Verschlüsselung bleiben fachlich getrennt.
8. **Kapazitätsehrlichkeit:** 1260 Minuten Kern plus 360 Minuten Jahresposten ergeben 36 UE. M06 erweitert auf 40 UE, M07 auf 43 UE. Die neun Checks gegen 32/36/40 Netto-UE-Szenarien zeigen Defizit und Restzeit; lokale Verfügbarkeit bleibt überall unbestätigt. 43 UE sind ausschließlich Bedarf.
9. **Historischer Vergleich:** Alte 40-/46-/54-UE-Pfade sind ausschließlich Auditinput. Neue Module, Zeitkomponenten und Pfadprojektionen wurden aus R7-Anforderungen kalkuliert; keine historische Verfügbarkeit übernommen.
10. **Integration und Flex:** Drei Integrationseinträge besitzen getrennt erkennbare Nachweise und weder Zusatzzeit noch Zeitgutschrift. Zwei optionale Flexangebote sind außerhalb aller Pfade; sie schließen keine Pflichtlücke. M06/M07 sind curriculare Erweiterungen mit konkreten offenen Zielen.
11. **Orchestrierung und Fallback:** M03 begrenzt Teamprodukt, Verantwortlichkeit, Zwischenkontrolle und individuelle Erklärung. Feedback führt zu Revision, Wiederaufnahme wird getrennt budgetiert. Papierersatz kann Modellverständnis bewahren, lässt reale digitale Zielhandlungen aber offen.
12. **Eigene Abnahme:** Acht R7-Gates bleiben offen; DASH und Cutover werden nicht aktiviert. Planung ist keine tatsächliche Coverage, Zeitpassung, Zugänglichkeit, Angebotsnutzung oder Lernwirkung. Aktuelle Quellenprüfung und nicht erneut geprüfte Byteidentität sind getrennt dokumentiert.

## Technische Prüfung

35 gezielte Vertragstests wurden vor bzw. während der Implementierung angelegt. Der erste Lauf scheiterte am fehlenden R7-Validator. Ein zusätzlicher Gegenfall reproduzierte eine zu schwache Progressionsreferenz: Eine gültige Strang-ID konnte auf einen unpassenden Lernbogen verweisen. Ursache war die reine ID-Mengenprüfung ohne Prüfung des verknüpften Zielmoduls. Die gezielte Ergänzung prüft jetzt auch diese Verbindung; der reproduzierte Gegenfall besteht.

Alle **35 R7-Vertragstests** und die vollständige Python-Regression mit **966 Tests in 123,891 Sekunden** bestehen. Das integrierte V2-Gate sowie alle fünf JSON-Instanzen gegen AJV Draft 2020-12 bestehen ebenfalls. 39 Prüfeingänge werden gebunden, sieben lokale Dokumentziele sind vorhanden. Die vollständige Suite lief auf unverändertem Stand; nach Abschluss dieses Berichts werden Hashbindung, Jahrgangstests, V2-Gate und Schema-Instanzen unmittelbar vor Commit erneut geprüft.

Die Integration ergänzt drei Imports/Aufrufe im zentralen Validator und acht erwartete Missing-File-Meldungen im bestehenden Test. Der separate R7-Validator prüft Mengen, Quellenrollen, die tatsächlichen Strang-/Modulverbindungen, Jahresrechnungen, Pfadprojektionen, Kapazitätsdefizite, historische Aussagegrenzen, offene Gates, Reifeachsen und den exakten R6-Abnahmecommit. Versiegelte R5-/R6-, Grundlagen-, Audit-, Curriculum- und historische Zeitdateien bleiben unverändert. Kein offener blockierender technischer Befund im geprüften Umfang.

## Offene Entscheidungen

Lokale Nettozeit und reale Eingangslage entscheiden später, welcher Pfad tragfähig ist. Die 36-/40-UE-Varianten lassen acht bzw. drei zusätzliche Orientierungsziele offen. Die drei neuen Reflexionsfragen bleiben selbst im 43-UE-Bedarf offen. Zusätzlich bestehen die sechs Vorgängerfragen. Vor Einsatz sind Werkzeuge, konkrete Materialien/Regeln, Zugänglichkeit und Erprobung separat zu prüfen. Diese offenen Punkte blockieren keine ehrliche Planungsdisposition, erlauben aber keine vollständige Erfüllungs- oder Einsatzbehauptung.
