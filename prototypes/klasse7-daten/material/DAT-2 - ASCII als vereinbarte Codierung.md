---
type: output
status: reviewed
area: Unterricht
project: IuM-Lernwerk
klassenstufe: 7
fassung: "1.0"
created: 2026-10-28
updated: 2026-10-28
tags:
  - output/lernmaterial
---

# DAT-2 · Eine Tabelle, die beide kennen

**45 Minuten · eigene Arbeit mit gemeinsamer Klärung**

Eure eigenen Codes funktionieren nur, wenn beide Seiten dieselbe Vereinbarung kennen. Für den nächsten Auftrag gilt eine verbreitete Vereinbarung: **ASCII**, gesprochen ungefähr „Äski“. Du codierst eine Nachricht und liest eine andere zurück.

## 1 · Gleiche Bits, andere Tabelle? · 10 Minuten

Zwei Teams verwenden für A unterschiedliche Codewörter. Können sie ihre Tabellen einfach weglassen? Begründe kurz mit DAT-1.

**ASCII** ordnet Buchstaben, Ziffern, Satz- und Steuerzeichen festgelegte Codes zu. ASCII ist ein **7-Bit-Code**. In dieser Werkstatt schreiben und speichern wir jeden ASCII-Code in einem **Byte mit acht Bits**: Vor die sieben Bits kommt eine Null. Ein Byte besteht aus acht Bits.

Unsere Tabelle zeigt nur einen Ausschnitt. Umlaute und Emoji gehören nicht zum ursprünglichen ASCII-Zeichenvorrat. Eine fehlende Tabellenzeile beweist aber nicht automatisch, dass ein Zeichen in ASCII fehlt: Unser Ausschnitt ist kleiner als die vollständige Tabelle.

## 2 · Nachschlagen statt Binärrechnen · 10 Minuten

| Zeichen | Darstellung in einem Byte | Zeichen | Darstellung in einem Byte |
|---|---|---|---|
| Leerzeichen ␣ | `00100000` | A | `01000001` |
| E | `01000101` | I | `01001001` |
| K | `01001011` | M | `01001101` |
| O | `01001111` | R | `01010010` |
| T | `01010100` | U | `01010101` |
| a | `01100001` | m | `01101101` |
| ! | `00100001` | ? | `00111111` |

**Gemeinsames Beispiel:** „OK“ wird zu `01001111 01001011`. Jeder Achtblock steht für ein Zeichen. Die Lücke zwischen den Blöcken dient nur der Lesbarkeit; ein echtes Leerzeichen im Text braucht seinen eigenen Code `00100000`.

Suche jetzt selbst den Code für **A!**. Decke den Text ab und lese deine beiden Blöcke zurück. Die Tabelle bleibt offen; einen automatischen Konverter brauchst du nicht.

<details><summary>Hilfe: Den Achtblock finden</summary>
<p>Beim Codieren suchst du links das Zeichen und übernimmst die acht Bits. Beim Decodieren suchst du den ganzen Achtblock in einer Bitspalte und liest das zugehörige Zeichen. Vergleiche Groß- und Kleinbuchstaben sorgfältig.</p>
</details>

## 3 · Zwei verschiedene Richtungen · 15 Minuten

Bearbeite in deinen Notizen:

1. Codiere **AM TOR**. Das Leerzeichen zwischen M und T gehört dazu. Notiere einen Achtblock pro Zeichen.
2. Decodiere diese neue Nachricht: `01001011 01001111 01001101 01001101`. Notiere den Text und markiere eine Zuordnung in der Tabelle.
3. Jemand codiert „AM“ als `01000001 01101101`. Prüfe den Text, der damit tatsächlich ankommt. Falls nötig, repariere genau den falschen Block.
4. Erkläre in zwei Sätzen: Was haben dein eigener Code und ASCII gemeinsam? Was ist an der Vereinbarung anders?

**Qualitätsmaßstab:** richtige Zeichen, richtige Blockgrenzen, ein mitcodiertes Leerzeichen und eine Erklärung der gemeinsamen Vereinbarung. Die Zahl der ausgefüllten Blöcke allein genügt nicht.

## 4 · Rückmeldung und neuer Fall · 10 Minuten

Vergleicht eure Ergebnisse mit der Lehrperson. Suche bei einer Abweichung zuerst das betreffende Zeichen, dann dessen Block. Erhalte den ersten Versuch lesbar und notiere die Korrektur.

Danach ohne die vorherige Lösung: Codiere **A?** und decodiere **`01010100 01001111 01010010`**. Die Tabelle darfst du benutzen. Erkläre abschließend, warum „acht Bits pro Zeichen“ für unser vereinbartes Modell passt, aber keine Regel für sämtliche Texte und Zeichencodierungen ist.

**Festhalten:** Eine Bitfolge lässt sich nur mit der passenden Codierungsvereinbarung deuten. ASCII ist kein Geheimcode. Die [[Datenbogen - Sicherung|Sicherung]] enthält nach der Besprechung das gemeinsame Ergebnis.

Tabellendaten: ASCII nach [RFC 20](https://www.rfc-editor.org/rfc/rfc20.html), eigener verkürzter Ausschnitt mit führender Null. Keine Umrechnung zwischen Dezimal- und Binärzahlen verlangt.
