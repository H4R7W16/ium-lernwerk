# Gemeinsame Pages-Ausgabe

`preparePages()` prüft und liefert die gebundenen Inhaltsausgaben der bisherigen Klassen 5/6/7. Historische SHA-Bindungen und Original-Snap-Dateien bleiben unverändert geprüft.

`preparePublishedPages()` ergänzt auf ausdrücklichen Nutzerauftrag vom 27.10.2026 die Klassenstufen-Auswahl der regulären Jahrgangsseiten. `build()` veröffentlicht ausschließlich diese vollständige Ausgabe. Die Auswahl führt über normale Links nach Klasse 5, 6 oder 7. Unterrichtsinhalte und bestehende Speicher-/Verlassen-Schutzmechanismen werden nicht verändert.

Die begrenzten Ausnahmen gegenüber dem gebundenen Ausgang sind:

- Kopfzeile und zwei lokale Menüreferenzen im HTML.
- Je eine CSS-/JS-Datei in den drei regulären Jahrgangswurzeln.
- Dateienliste und Version der beiden regulären Klasse-5/6-Offlinepakete.
- Herkunftsbindung der eigenen Snap!-Editorhülle: neuer Hüllenhash und zusätzliche Menü-Assetbindung; der Ausgangshash bleibt dokumentiert. Original-Engine und Projektdateien bleiben bytegleich.

Eingefrorene zusätzliche Recherche-Beispiele behalten ihren Referenzstand. Die Navigation speichert nichts und sendet keine Analysedaten. Ein Klassenwechsel verspricht keine Offline-Verfügbarkeit eines noch nicht vorbereiteten anderen Jahrgangs.

`grade-navigation.test.cjs` prüft die tatsächliche Ausgabe, relative Einstiege von allen Unterseiten, alle lokalen HTML-Verweise, den Erhalt sämtlicher Inhalte außerhalb des Headers, Offline-Assets und Herkunftsmanifeste. Bestehende Bestandstests laufen unverändert auf der gebundenen Ausgangsfassung weiter; die zusätzliche Ausgabestufe wird gesondert geprüft.
