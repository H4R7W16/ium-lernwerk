# Lernfassung 3: interaktiv planen

Eigenständige auswählbare Fassung der Selbstlernstrecke. Vier frei wählbare Etappen verbinden ein erklärtes 3×2-Beispiel, ausführbare 4×2-Lücken, den linken Reihenwechsel und einen freien 4×3-Plan.

## Quellen und Vorschau

Die vollständigen Fachinhalte und der Simulationskern kommen aus ../m06-selbstlernen. content.cjs ergänzt nur den Einstieg und die Planungsseite. journey-model.js bewertet die beiden Teilaufgaben; journey.js verbindet Eingaben, Fahrt und Etappen. Der bestehende Renderer akzeptiert eine optionale Seitenliste, die App einen optionalen Speicherschlüssel und einen Erweiterungsaufruf.

node prototypes/m06-reinigungsfall/build.cjs /absoluter/neuer/vorschauordner

Der Pages-Build stellt /lernfassung-3/ und /lernfassung-3/read.html bereit. node prototypes/m06-lernfassung3/render.cjs erzeugt bei Bedarf lokale HTML-Einstiege für die Quellvorschau; diese generierten Dateien werden nicht versioniert.

## Prüfung

node --test prototypes/m06-lernfassung3/journey.test.cjs prototypes/m06-selbstlernen/material.test.cjs prototypes/m06-reinigungsfall/pages-build.test.cjs

Gezielte Prüfungen, keine Import-/Exporttests oder Gesamtsuiten. Im Browser zusätzlich Etappen, Fehler/Korrekturen, Wissen-Rückkehr, alternative Programme, Tastatur, schmale Ansichten und Versionswechsel prüfen.

## Lernstände

Die Browsersicherung der dritten Fassung verwendet einen eigenen Schlüssel. Das vorhandene Sicherungsformat und die ausdrücklich importierbaren Daten bleiben unverändert. Eingaben in den Teilaufgaben und freie Begründungen bleiben im offenen Tab, wie auf der Lernseite erklärt; sie gehören nicht zur Sicherung. Der eigene 4×3-Code bleibt sicherbar. Alle Hilfen, Lösungen und Ablauftabellen sind ohne Lernstandsfreigabe zugänglich; read.html benötigt kein JavaScript.

Fachliche und technische Prüfung ersetzt keine Erprobung mit Lernenden.
