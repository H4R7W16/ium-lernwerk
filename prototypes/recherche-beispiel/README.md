# Zusätzliches Recherche-Beispiel

Veröffentlicht unter [beispiele/recherche/](https://h4r7w16.github.io/ium-lernwerk/beispiele/recherche/), zusätzlich zur unveränderten bisherigen [Klasse-5-Version](https://h4r7w16.github.io/ium-lernwerk/klasse5/). Der Einstieg führt direkt zum neuen Recherchekapitel mit Leas Film. Die zugehörige Beispielumgebung liegt im eigenen Unterpfad; alle Materialien und Navigationen bleiben dort verfügbar.

## Quelle und Build

Kapitel 1.7.0/RQ05-F1, Film 1.0 vom 13.10.2026. quelle/ enthält nur die bei der vorhandenen statischen Erzeugung tatsächlich benötigten Originalquellen und Medien. quellstand.json dokumentiert ihre SHA256-Werte. Es enthält keine gerenderten HTML-Builds, Runtimes, Git-Verwaltung, privaten Lernstände oder internen Reviewprotokolle.

Der additive Build verwendet die unveränderte bisherige Pages-Erzeugung und ergänzt ausschließlich beispiele/. Er verweigert Pfadkollisionen, prüft alle lokalen HTML-Verweise und vergleicht alle bisherigen Ausgabedateien per SHA256. Speicherkennung und Offlinecache der neuen Umgebung sind getrennt.

Build: node prototypes/recherche-beispiel/build.cjs. Prüfung: node --test prototypes/recherche-beispiel/pages.test.cjs. Der bestehende Klasse-5-Pages-Workflow liefert beide Angebote als ein Artefakt aus.

## Sichtungsstand

Der Film bleibt die bestehende Fassung 1.0. Zwei offene Bildbefunde: A13, Untertitel überdecken zeitweise die Herkunftszeile; A12/A14, Originaltext beim Wiederfinden klein. Qualitative Hörsichtung und reale Lernerprobung bleiben offen. Veröffentlichen schließt diese Befunde nicht. Für eine begleitete Nutzung Pausen bei 0:37 und 1:47 vorsehen.

## Weiterarbeiten

Die Quelle ist bewusst getrennt von der alten Version. Änderungen nur im Beispielstand durchführen und dessen Nachweise aktualisieren; eine Übernahme in die alte Fassung benötigt einen eigenen Auftrag. Die Herkunft und Nutzungsangaben stehen im Kapitel unter Quellen und in den Mediennachweisen.
