# Welche Prüfung stoppt den Rover?

**30 Minuten · mit Abstand nach ALG-6 · Papier oder bekanntes Dokument**

Hier liest du eine vereinfachte Darstellung von Snap-Blöcken. `x` bedeutet die x-Position, keine neue selbst angelegte Variable. Der Rover zeigt nach rechts; „gehe“ vergrößert x. Bei „wiederhole bis“ wird **vor jedem möglichen Durchlauf** geprüft. Eine wahre Bedingung beendet die Schleife. Du brauchst zunächst weder Editor noch alte Lösungen.

## 1 · Erst vorhersagen · 12 Minuten

```
Start: x = 0; Richtung rechts
wiederhole 2-mal:
    gehe (3 + 3) Schritte
wiederhole bis (x = 36):
    gehe 10 Schritte
sage „angekommen“
```

1. Welche Zahl liefert `(3 + 3)`? Welche Art von Wert liefert `(x = 36)`? Was ist anders am Block `sage „angekommen“`?
2. Notiere die Position nach der festen Wiederholung. Ergänze danach die ersten vier Positionen, die die bedingte Schleife erreicht. Wird 36 jemals getroffen? Erkläre die Regel der Positionsfolge; vier Versuche allein beweisen noch kein „nie“.
3. Das Ziel lautet jetzt ausdrücklich: **beim ersten Erreichen oder Überschreiten von 36 stoppen; bei einem Start ab 36 gar nicht mehr gehen.** Ersetze nur die Stoppbedingung. Zeichne dazu eine kleine Entscheidung mit Ja-/Nein-Pfeilen: stoppen oder gehen und erneut prüfen.

## 2 · Mit Gegenfällen prüfen · 7 Minuten

Prüft eure reparierte **bedingte Schleife allein, ohne die feste Wiederholung davor**, mit Start x = **12, 36 und 40**. Notiert Endposition und Anzahl der Bewegungen. Zählt für Start 12 auch die Bedingungsprüfungen. Erklärt euch die erste Stelle, an der ursprüngliche und reparierte Fassung unterschiedlich handeln.

Die Lehrperson klärt anschließend die entscheidende Grenze. Ein passender Stopp im Normalfall allein genügt nicht.

## 3 · Verbessern und verändern · 8 Minuten

Verbessere eine falsche Entscheidung oder begründe die Abnahme deiner Lösung. Neuer Fall: Die reparierte bedingte Schleife startet bei **x = 31** und geht jeweils **8 Schritte**. Sage Endposition und Zahl der Bewegungen voraus. Was zeigt dieser Fall über „angekommen“? Formuliere eine genauere Meldung für die vereinbarte Stoppregel.

Falls ihr den Editor zur Gegenprüfung nutzt: Vorhersage zuerst notieren, ursprünglichen Fehlerlauf spätestens nach vier Bewegungen stoppen. Keine zusätzliche Programmieraufgabe anschließen.

## 4 · Einen nächsten Test festhalten · 3 Minuten

Zeige die endgültige Bedingung, den Grenztest und deine neue Meldung. Die Lehrperson fragt bei Bedarf nach: **Wert, Prüfreihenfolge oder Grenze?** Benenne den passenden nächsten Test. Es ist eine Lernphase, keine benotete Prüfung.
