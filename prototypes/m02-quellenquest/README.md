# Quellenquest: Was wird aus unserer Pausenwiese?

Begrenzter Klasse-5-Prototyp zur Quellen- und Textarbeit. Umsetzung des angenommenen Quest-Konzepts vom 28.09.2026 innerhalb der vorhandenen statischen Lernwerk-Architektur.

## Lernweg

1. Prüffrage zur Chatnachricht klären.
2. Chat, älteren AG-Vorschlag und aktuellen Beschluss nach Herkunft, Datum und Zweck untersuchen.
3. Aussagen als belegt, widerlegt oder offen beurteilen und konkrete Textstellen auswählen.
4. Eine sachliche Antwort mit Belegen formulieren, mit Kriterien/Beispiel vergleichen und verbessern.
5. Den Bibliotheksfall selbstständig prüfen. Dort ist die Chatnachricht neuer als die passende Originalmitteilung.

Keine Spielschlösser oder Punktelogik. Die fünf Etappen sind unmittelbar erreichbar; ein vorheriger Abschluss ist nicht erforderlich. Offene Antworten werden nicht automatisch fachlich bewertet. Mündliche und handschriftliche Antworten sind möglich.

## Dateien

- content.js: einzige redaktionelle Quelle für Dokumente, Lernschritte, Hilfen und Erwartungshorizonte.
- model.js: prüft Urteile zusammen mit Textbelegen und ordnet Quellen passend zur Frage zu.
- render.cjs: erzeugt Lernoberfläche, Wissen, Lehrpersonenbriefing, Gesamtmaterial und fünf vollständige Einzelmaterialien.
- app.js / style.css: Bedienung und responsive Darstellung.
- model.test.cjs: acht gezielte Prüfungen.

Das HTML wird durch den vorhandenen Build in prototypes/m06-reinigungsfall/build.cjs erzeugt. Es wird kein zweiter Generator oder allgemeines Quest-System eingeführt.

## Vorschau und Prüfung

Node 22, keine zusätzlichen Abhängigkeiten nötig:

    node --test prototypes/m02-quellenquest/model.test.cjs prototypes/m06-reinigungsfall/pages-build.test.cjs
    node prototypes/m06-reinigungsfall/build.cjs <neues-lokales-ausgabeverzeichnis>

Den Ausgabeordner über einen lokalen HTTP-Server ausliefern; Einstieg /quellenquest/. Begleitseiten: wissen.html, lehrkraft.html, material.html und baustein-<etappe>.html. Materialien und Wissen funktionieren ohne JavaScript.

## Didaktische Einordnung

Teilbereich der aktiven G5-M02-Planung, keine vollständige Internetrecherche. Alle Personen und Quellen sind ausdrücklich erfunden. Für reale Quellen muss die Herkunft gesondert geprüft werden. Auch Autorität oder Aktualität allein garantieren keine Richtigkeit.

Zeitannahme 55 Minuten; reale Klasse-5-Erprobung steht aus. Zur Erprobung: Auftragverständnis, Hilfenutzung, eigene Begründungen, Revision, Transfer sowie unabhängige Übernahme durch die Lehrperson beobachten.

Quellcode unter der Repository-Lizenz, selbst erstellte Lerntexte entsprechend LICENSE-CONTENT.md. Keine übernommenen Bilder oder Drittmaterialien.

