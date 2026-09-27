# Ein Bild – zwei Geschichten

Zweiter Lernstudio-Prototyp für Klasse 5: Medienanalyse mit einem kleinen eigenen Text-Bild-Produkt. Öffentlicher Zielpfad: `/medienanalyse/`.

## Lernweg
Fünf unabhängig anwählbare Schritte: Entdecken, Untersuchen, Prüfen, Gestalten, Übertragen. Hauptfall Schulfest, Transfer Schulbibliothek. Beide Szenen und ihre Situationskarten sind als erfunden gekennzeichnet. Die Bilder wurden mit Imagegen erzeugt; Herkunft und vollständige Prompts stehen in [ASSETS.md](ASSETS.md).

Die Bilduntersuchung verändert zuerst nur den Ausschnitt, danach nur die Überschrift. Der eigene Beitrag kombiniert frei gewählten Ausschnitt, selbst formulierte Überschrift, Bildunterschrift und Begründung. Die Vorschau reagiert direkt. Geschlossene Belegfragen liefern materialbezogene Hinweise; offene Texte werden nicht automatisch als richtig bewertet. Nach einer Revision müssen die Selbstprüfkriterien erneut beurteilt werden.

## Selbstlernen und Unterricht
- Kurze Erklärungen, Merksätze, zwei Hilfestufen und kommentierte Beispiele.
- Alle Hash-Ziele sind direkt erreichbar: `#eindruck`, `#wirkung`, `#belege`, `#gestalten`, `#transfer`.
- `wissen.html`: vollständige Erklärungen und Beispiele.
- `lehrkraft.html`: Ziele, Zeitannahmen, Impulse, Fehlvorstellungen, Hilfen und fachliche Antworten.
- `material.html`: Bilder, Situationskarten und Arbeitsaufträge ohne Lösungen, mit Drucklayout. Auch ohne JavaScript lesbar.
- Lehrperson kann einen Inhalt übernehmen und beim nächsten Arbeitsauftrag in den digitalen Weg zurückführen.

## Dateien und Vorschau
`content.js` enthält die gemeinsame Unterrichtsgrundlage. `model.js` enthält reine Crop-/Rückmeldelogik. `app.js` steuert die Oberfläche. `guides.cjs` erzeugt statische Materialseiten beim vorhandenen Pages-Build. Keine neuen Bibliotheken oder externen Laufzeitdienste.

Node 22, vom Repository-Stamm:

    node --test prototypes/m05-medienanalyse/model.test.cjs prototypes/m06-reinigungsfall/pages-build.test.cjs
    node prototypes/m06-reinigungsfall/build.cjs <frisches-lokales-Ausgabeverzeichnis>

Das Ausgabeverzeichnis mit einem statischen Server bereitstellen und `/medienanalyse/` öffnen. Der Quellenordner allein enthält die generierten Materialseiten noch nicht.

## Umfang und Grenzen
Ausschnitt aus der Projektplanung G5-M04/G5-M05. Keine vollständige Abdeckung dieser Module oder umfassende Quellenkritik. Rund 90 Minuten sind eine unpilotierte Zeitannahme. Reale Erprobung mit Klasse 5, Schul-iPads und assistiven Technologien steht aus. Gezielte Nachweise: [QA.md](QA.md).
