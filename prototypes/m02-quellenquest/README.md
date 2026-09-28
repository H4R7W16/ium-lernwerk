# Quellenquest: Was wird aus unserer Pausenwiese?

Begrenzter Klasse-5-Prototyp zur Quellen- und Textarbeit. Umsetzung des angenommenen Quest-Konzepts vom 28.09.2026 innerhalb der vorhandenen statischen Lernwerk-Architektur.

## Lernweg

1. Eine erste Einschätzung und eine eigene Prüffrage zur Chatnachricht formulieren.
2. Einen Prüfvorgang am Fundbüro-Beispiel nachvollziehen; danach drei Dokumente nach Herkunft, Datum, Zweck und Frage untersuchen.
3. Zwei Kernfragen (plus zwei optionale Aussagen) beurteilen und Passagen direkt im Dokument auswählen. Gestuftes Feedback und Belegübersicht unterstützen die Erklärung.
4. Eine sachliche Antwort aus den eigenen Belegen formulieren, die erste Einschätzung wieder aufnehmen und einen Satz nach Begründungsvergleich überarbeiten.
5. Den Sporttag selbstständig prüfen. Ein alter Schulbrief wird durch eine nachvollziehbare Aktualisierung überholt; ein Kind gibt diese im Chat korrekt weiter. Eine Endzeit bleibt offen.

Keine Spielschlösser oder Punktelogik. Die fünf Etappen sind unmittelbar erreichbar; ein vorheriger Abschluss ist nicht erforderlich. Offene Antworten werden nicht automatisch fachlich bewertet. Mündliche und handschriftliche Antworten sind möglich.

## Dateien

- content.js: einzige redaktionelle Quelle für Dokumente, Lernschritte, Hilfen und Erwartungshorizonte.
- model.js: prüft Urteile zusammen mit Textbelegen und ordnet Quellen passend zur Frage zu.
- render.cjs: erzeugt Lernoberfläche, Wissen, Lehrpersonenbriefing, Gesamtmaterial und fünf vollständige Einzelmaterialien.
- app.js / style.css: Bedienung und responsive Darstellung.
- model.test.cjs: zehn gezielte Prüfungen.

Das HTML wird durch den vorhandenen Build in prototypes/m06-reinigungsfall/build.cjs erzeugt. Es wird kein zweiter Generator oder allgemeines Quest-System eingeführt.

## Vorschau und Prüfung

Node 22, keine zusätzlichen Abhängigkeiten nötig:

    node --test prototypes/m02-quellenquest/model.test.cjs prototypes/m06-reinigungsfall/pages-build.test.cjs
    node prototypes/m06-reinigungsfall/build.cjs <neues-lokales-ausgabeverzeichnis>

Den Ausgabeordner über einen lokalen HTTP-Server ausliefern; Einstieg /quellenquest/. Begleitseiten: wissen.html, lehrkraft.html, material.html und baustein-<etappe>.html. Materialien und Wissen funktionieren ohne JavaScript.

## Didaktische Einordnung

Teilbereich der aktiven G5-M02-Planung, keine vollständige Internetrecherche. Alle Personen und Quellen sind ausdrücklich erfunden. Für reale Quellen muss die Herkunft gesondert geprüft werden. Auch Autorität oder Aktualität allein garantieren keine Richtigkeit.

Zeitannahme rund 60 Minuten; reale Klasse-5-Erprobung steht aus. Zur Erprobung: Auftragverständnis, Hilfenutzung, eigene Begründungen, Revision, Transfer sowie unabhängige Übernahme durch die Lehrperson beobachten.

Quellcode unter der Repository-Lizenz, selbst erstellte Lerntexte entsprechend LICENSE-CONTENT.md. Keine übernommenen Bilder oder Drittmaterialien.


## Gemeinsamer Lernwerkrahmen

Der Pages-Build ersetzt die bisherigen Kopfbereiche durch `prototypes/shared/prototype-navigation.cjs` und das gemeinsame CSS. Ein natives Themenmenü verbindet die drei aktuellen Angebote. Lernweg/Stationssteuerung bleibt lokal. Auf den interaktiven Einstiegen öffnen Wissen und Unterrichtsmaterial ergänzend in einem neuen Tab.
