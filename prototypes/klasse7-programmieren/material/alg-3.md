# ALG-3 · Welches Depot ist zuständig?

**75 Minuten · Rover-Werkstatt.** Bei x = 40 verläuft die Depotgrenze. Vor ihr ist Depot A zuständig, an der Grenze und dahinter Depot B. Der Rover soll die passende Meldung zeigen und dabei stehen bleiben.

## 1 · Die Grenze entscheidet · 15 Minuten gemeinsam

Ein `falls … sonst …` prüft eine Bedingung: **wahr** führt in den ersten, **falsch** in den zweiten Zweig. Pro Aufruf wird genau ein Zweig ausgeführt.

Vergleiche vor dem Ausführen:

| Position | `x-Position < 40` | `nicht (x-Position > 40)` |
|---|---|---|
| 30 | … | … |
| 40 | … | … |
| 50 | … | … |

`nicht` kehrt wahr und falsch um. Wo unterscheiden sich die Bedingungen? Welche passt zu „Depot A“?

## 2 · Die Depotanzeige ergänzen · 15 Minuten gemeinsam

Öffne das Startprojekt. **Starten** stellt zunächst x = 40 her. Ergänze im losen `falls … sonst …` den fehlenden zweiten Meldungsblock und hänge die Verzweigung unten an den Startstapel.

Halte deine **Vorhersage für 40** fest und prüfe. Teste danach 30: Ändere nur die Startposition, nicht die Grenze 40.

## 3 · Deine Melderegel · 30 Minuten

Du entscheidest, welches Depot du zuerst abfragen willst: **„vor 40?“** oder **„an oder hinter 40?“**. Wähle verständliche Meldungen, plane die Bedingung und ordne beide Zweige passend zu. Baue deine Fassung ohne Bewegung.

Skizziere die Entscheidungsraute mit Frage, wahr/falsch und beiden Meldungen. Ergänze darin drei Tests: **39, 40 und 41**. Notiere jeweils deine erwartete Meldung vor dem Lauf und hake sie nach dem Prüfen mit einer kurzen Beobachtung ab.

## 4 · Regel wechseln · 15 Minuten

Lasse den Grenzfall erklären und überarbeite bei Bedarf. **Neuer Kurzfall:** Formuliere dieselbe Depotregel nun mit der jeweils anderen Frage. Sage für 39 und 40 voraus, welcher Zweig gewählt wird. Prüfe: Was muss außer der Bedingung geändert werden?

**Behalte:** deine Skizze mit den drei Tests und einem Satz zum Fragenwechsel. Sichere `ALG-3_Kennung.xml` über **Datei speichern**. Öffne sie über **Datei öffnen** und prüfe 40 erneut.

<details><summary>Hilfe und Bedienung</summary>

Frage zuerst, ob deine Bedingung genau bei 40 wahr ist. `nicht (x-Position < 40)` fragt „nicht mehr davor?“. Bei einer falschen Meldung prüfe getrennt Startposition, Bedingung und Zweig. Nutze bei Bedarf **Schrittmodus** und **Ein Schritt**; der grüne Link lädt das Startprojekt bereits.

</details>
