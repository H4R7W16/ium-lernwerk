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

# DAT-1 · Kommt wirklich dieselbe Nachricht an?

**60 Minuten · erst allein, dann zu zweit**

Dein Übertragungsgerät kennt nur zwei Zeichen: **0 und 1**. Du sollst eine kurze Nachricht so codieren, dass eine andere Person genau deinen Text zurückgewinnt. Ihr dürft dafür eine Tabelle vereinbaren.

Am Ende hast du eine eigene Codetabelle, zwei Übertragungsproben und einen erklärten Fehlerfall. Arbeite in deinen [[Datenbogen - Werkstattnotizen|Werkstattnotizen]].

## 1 · Eine Nachricht, zwei Lesarten · 10 Minuten

Die erste Tabelle lautet:

| Textzeichen | Codewort |
|---|---|
| A | 0 |
| M | 01 |
| O | 1 |

Angekommen ist **01**. Was könnte die Nachricht gewesen sein? Schreibe vor dem Austausch deine Lesart auf. Suche anschließend eine zweite. Zeige durch Striche, wie du die Bits aufteilst.

Die Lehrperson klärt mit euch: Ein **Bit** hat einen von zwei Werten, 0 oder 1. Eine **Bitfolge** besteht aus mehreren Bits. Eine **Codierung** ordnet Zeichen Codewörter zu. Beim **Decodieren** geht es zurück. Dafür müssen Tabelle und Grenzen der Codewörter klar sein. Erfolgreiches Raten genügt nicht.

## 2 · Eine verlässliche Vereinbarung · 15 Minuten

Wir brauchen genau vier Textzeichen: **A, M, O und das Leerzeichen**. In der Tabelle schreiben wir für das Leerzeichen „␣“. Es steht für eine Lücke im Text, nicht für den Buchstaben O oder eine Null.

Nutze die vier Codewörter **00, 01, 10, 11**. Verteile sie selbst auf die vier Zeichen; jedes Codewort darf nur einmal vorkommen.

| Textzeichen | Mein Codewort |
|---|---|
| A | … |
| M | … |
| O | … |
| Leerzeichen ␣ | … |

Codiert gemeinsam ein Beispiel mit einer anderen Zuordnung als deiner. Lest es in Zweiergruppen zurück. Erkläre dann an deiner Tabelle: Warum kann jede Zweiergruppe nur ein Zeichen bedeuten? Was muss die empfangende Person außer den Bits wissen?

<details><summary>Hilfe: Ich verliere die Grenze</summary>
<p>Beginne beim ersten Bit. Markiere immer genau zwei Bits, etwa <code>10 | 00 | 11</code>. Suche jede Gruppe in deiner Tabelle. Die Striche sind hier nur Lesehilfen. In eurer Übertragung sind die festen Zweiergruppen vereinbart.</p>
</details>

## 3 · Besteht dein Code den Fremdtest? · 25 Minuten

1. Erfinde **zwei verschiedene Texte mit je drei bis fünf Zeichen** aus A, M, O und Leerzeichen. Eine Folge wie „MOA“ ist erlaubt. Mindestens einer der beiden Texte enthält ein Leerzeichen. Halte die Originaltexte zunächst verdeckt.
2. Codiere beide Texte allein. Gib nur deine Tabelle und die beiden Bitfolgen weiter. Vereinbarung: vom ersten Bit an in Zweiergruppen lesen.
3. Decodiere selbst die beiden Nachrichten deiner Partnerperson. Notiere die Gruppen und den zurückgewonnenen Text. Vergleicht erst danach mit den Originalen. Sagt bei einer Abweichung, **an welcher Gruppe** sie beginnt. Korrigiert dort und lest erneut.
4. Erzeuge nun eine **absichtlich fehlerhafte zweite Tabelle** mit A, M und O. Finde dazu eine Bitfolge, die zwei verschiedene Texte ergeben kann. Nimm einen anderen Fall als das Einstiegsbeispiel. Notiere beide Rückübersetzungen. Verbessere die Tabelle oder die Vereinbarung, sodass dieser Fehler vermieden wird.

Beide Personen entwerfen und decodieren. Ein gemeinsames Blatt ersetzt deine eigenen Versuche nicht. Haltet nach den ersten acht Minuten kurz an: Sind Tabelle und erste Nachricht bereits vorhanden? Wenn nicht, nutzt die Hilfe.

<details><summary>Hilfe: Einen mehrdeutigen Fall bauen</summary>
<p>Prüfe zuerst, was passiert, wenn zwei Zeichen dasselbe Codewort bekommen. Oder lasse das Codewort eines Zeichens aus den Codewörtern zweier anderer Zeichen bestehen. Schreibe die zwei unterschiedlichen Texte dazu. Du musst keinen besonders komplizierten Code erfinden.</p>
</details>

## 4 · Prüfen, verbessern, erklären · 10 Minuten

Tauscht einen **neuen Text mit vier Zeichen** aus, der eure verbesserte Regel prüft. Danach beantwortest du allein:

- Was macht deinen Code eindeutig rückübersetzbar? Nenne Zuordnung **und** Codewortgrenzen.
- Was zeigen eure Versuche, und warum ist die Regelbegründung zusätzlich nötig?

Ein guter Nachweis zeigt Tabelle, tatsächliche Rückübersetzungen, den mehrdeutigen Gegenfall und eine begründete Reparatur. Falls die erste Tabelle schon eindeutig war, bleibt sie erhalten; verbessert wird dann die absichtlich fehlerhafte Tabelle.

**Festhalten:** Codierung macht einen Text darstellbar und übertragbar. Sie macht ihn nicht automatisch geheim. Wer eure Tabelle kennt, kann mitlesen. Die gemeinsame [[Datenbogen - Sicherung|Sicherung]] wird nach der Besprechung ergänzt.

Wenn du ohne Partnerperson arbeitest, prüft die Lehrperson eine deiner Nachrichten und gibt dir eine fremde zurück. Selbstlesen nach kurzer Pause ersetzt diesen Fremdtest nicht.
