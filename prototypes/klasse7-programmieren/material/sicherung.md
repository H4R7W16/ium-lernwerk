# Rover-Werkstatt · Besprechung und Sicherung

**Fassung 2.0.** Karten erst nach dem eigenen Versuch gemeinsam nutzen. Die Seite ist öffentlich. Ein fremdes Lösungsprojekt belegt keine eigene Erklärung.

## ALG-1 · Gleicher Endort, anderer Weg

A endet 30, B endet 20. B:0→10→15→20. Eine eigene feste Route nach 20 kann 2×10 oder 4×5 sein. Die Klammer bestimmt den wiederholten Inhalt; „Ende“ steht danach und erscheint einmal. B mit drei Fünferschritten endet 25.

**Merksatz:** Die Zahl an der Schleife zählt Durchläufe, die Zahl in der Bewegung bestimmt die einzelne Strecke.

## ALG-2 · Wert und Wirkung

`5+7` erhält 5 und 7 und liefert 12/Zahl. `gehe(5+7)` erhält 12 und verändert den Ort; kein einsetzbarer Rückgabewert. `sage Ziel` erhält eine Zeichenkette und bewirkt eine Anzeige. `8>8` ist falsch, `9>8` wahr. `x-Position` liefert den aktuellen Zustand als Zahl, ohne sichtbare Eingabe.

**Merksatz:** Ein Wert kann Eingabe eines anderen Blocks werden. Eine beobachtete Wirkung ist keine Rückgabe.

## ALG-3 · Die Grenze gehört zu Depot B

`x<40`:30 wahr,40 falsch,50 falsch. `nicht(x>40)`:30 wahr,40 wahr,50 falsch. Die Bedingungen unterscheiden sich am Grenzwert. Bei „vor 40?“ ist der Wahrzweig A; bei „an oder hinter 40?“ ist der Wahrzweig B. Die Meldungen müssen zur Frage passen.

**Merksatz:** Ein Aufruf der Verzweigung führt genau einen der beiden Zweige aus.

[Beispiellösung ALG-3](ALG-3-Beispielloesung.xml)

## ALG-4 · Gleichheit kann übersprungen werden

Von 45 aus erreichen positive Zehnerschritte die 40 nie. `nicht(x<40)` bedeutet „an oder hinter 40“. Der bis-Block prüft vor der Bewegung. Bei Start 40 oder 45 endet die reparierte Fassung ohne Bewegung; bei 35/Schritt 12 endet sie 47.

**Merksatz:** Anzahl der Bewegungen und Anzahl der Bedingungsprüfungen unterscheiden. Die letzte Prüfung gehört zur Erklärung.

[Repariertes Beispiel ALG-4](ALG-4-Repariert.xml)

## ALG-5 · Ein guter Test unterscheidet Programme

Ein Normalfall allein genügt nicht. Der Start genau am Ziel prüft, ob eine unnötige Bewegung erfolgt. Ein selbst gewählter Start, der das Ziel überspringt, kann einen falschen Gleichheitsabbruch entlarven. Beispiel Ziel 60/Schritt 10/Start 55:55→65, dann Stopp und „vorbei“. Jede Person kann eine andere passende Testidee begründen.

**Merksatz:** Erwartung vor Ausführung notieren, Abweichung erklären, Verbesserung erneut prüfen. Ein grafischer Plan und der Code beschreiben denselben Ablauf.

[Eine mögliche Steuerung ALG-5](ALG-5-Beispielloesung.xml)

## ALG-6 · Warum die Haltestelle verpasst wird

Fehlerfassung: fester Teil bis 20, bedingt bis 60, „vorbei“. Bei 50 ist `x>50` noch falsch. Die reparierte Abbruchfrage lautet etwa `nicht(x<50)`; sie endet 50/„Ziel“. Bedingte Schrittweite 12 führt 56/„vorbei“,15 führt 50/„Ziel“. Fester Teil 3×10 und danach Schritt 10: drei feste, zwei bedingte Bewegungen bis 50.

Die beschriftete Codekarte verbindet Positionsspur, Abbruchfrage und Meldungsentscheidung. Literal 10 und `x-Position` enthalten keinen Rechen-/Vergleichsoperator; `5+5` rechnet; `x>50` vergleicht. Zahl, Text und Wahrheitswert an den konkreten Stellen benennen.

**Merksatz:** Eine gezielte Änderung wird durch Vorhersage, tatsächlichen Lauf und begründeten Vergleich verständlich.

[Repariertes Beispiel ALG-6](ALG-6-Repariert.xml)

## Nach einer Schwierigkeit

Wählt eine konkrete unklare Stelle und ein passendes Beispiel. Bei fehlender Ablaufvorstellung kurze Spur gemeinsam beginnen; danach einen veränderten Fall selbst erklären. Ein noch nicht beobachteter Lauf bleibt offen. Hilfe ist Teil des Lernens; fachliche Klärung und technische Bedienung getrennt betrachten.
