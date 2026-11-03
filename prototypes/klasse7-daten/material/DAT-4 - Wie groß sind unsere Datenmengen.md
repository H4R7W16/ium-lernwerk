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

# DAT-4 · Wie viel muss übertragen werden?

**60 Minuten · eigene Rechnungen, gemeinsamer Vergleich**

Ein Bild kann nur wenige schwarze Felder haben und trotzdem viele Bits benötigen. Berechne, wie viele Daten in unseren Text- und Bildpaketen stecken. Nutze deine Ergebnisse aus DAT-2 und DAT-3.

## 1 · Was zählen wir? · 15 Minuten

Zwei 8×8-Bilder: eines vollständig weiß, eines mit vielen schwarzen Feldern. Braucht das weiße Bild in unserem Modell weniger Bits? Vermute zuerst und begründe anschließend.

**Unser Rechenmodell:** Jedes Schwarzweißpixel wird mit genau **einem Bit** gespeichert, auch ein weißes. Jedes ASCII-Zeichen belegt in unserer Byte-Darstellung **acht Bits**, auch ein Leerzeichen. Wir zählen nur diese unkomprimierten **Nutzdaten**. Angaben wie Breite, Höhe und Codierung sind zusätzlich nötig, werden in diesen Rechnungen aber nicht mitgezählt.

Eine echte PNG-, SVG- oder Textdatei kann deshalb eine andere Größe haben. Dateiformat, zusätzliche Angaben und Kompression spielen dabei eine Rolle. Die auf dieser Seite angezeigte SVG-Datei ist **nicht** das Ein-Bit-pro-Pixel-Modell. Ihre Dateieigenschaften sind kein Gegenbeweis gegen unsere Rechnung.

| Beziehung | Beispiel |
|---|---|
| 1 Byte = 8 Bit | 24 Bit ÷ 8 = 3 Byte |
| 1 Kilobyte (kB) = 1 000 Byte | 3 kB = 3 000 Byte |
| 1 Megabyte (MB) = 1 000 kB | 2 MB = 2 000 kB |
| 1 Gigabyte (GB) = 1 000 MB | 4 GB = 4 000 MB |
| 1 Terabyte (TB) = 1 000 GB | 1 TB = 1 000 GB |

Wir verwenden hier die **Dezimalpräfixe**, also immer den Faktor 1 000 zwischen benachbarten Zeilen ab kB. Das Zeichen B steht für Byte. Bit und Byte sind verschiedene Einheiten.

## 2 · Den Rechenweg sichtbar machen · 15 Minuten

**Muster:** „OK!“ hat drei Zeichen. `3 Zeichen × 8 Bit je Zeichen = 24 Bit = 3 Byte`.

Ein 4×4-Schwarzweißbild: `4 × 4 Pixel × 1 Bit je Pixel = 16 Bit = 2 Byte`.

Bearbeite gemeinsam zwei Änderungen: Wie verändert sich die Rechnung bei „O K!“ mit einem Leerzeichen? Wie viele Bits sind 5 Byte? Erklärt dabei, warum ihr multipliziert oder dividiert.

<details><summary>Hilfe: Erst die Einheit, dann die Zahl</summary>
<p>Vom Bild zu Bits: Breite mal Höhe mal Bits je Pixel. Von Bits zu Byte: in Achtergruppen bündeln, also durch acht teilen. Von Byte zu Bits: mit acht multiplizieren. Schreibe die Einheiten an jeden Rechenschritt.</p>
</details>

## 3 · Ein kleines Datenbudget · 20 Minuten

Notiere Ansatz, Ergebnis und Einheit. Ein Taschenrechner ist nach dem eigenen Ansatz erlaubt.

1. Berechne die Nutzdatenmenge von **AM TOR** aus DAT-2 und von **deinem eigenen Raster** aus DAT-3 – jeweils in Bit und Byte. Falls dein Raster noch fehlt, nutze ein 8×8-Raster und kennzeichne den Ersatz.
2. Vergleiche die beiden 8×8-Bilder vom Einstieg. Erkläre, warum „mehr Schwarz“ in unserem Modell nicht „mehr Daten“ bedeutet.
3. Ordne diese **erfundenen Größenkarten** von klein nach groß. Zeige für mindestens zwei Vergleiche die Umrechnung: **900 kB, 2 MB, 1 500 MB, 3 GB, 1 TB**. Nenne außerdem, wie viele Byte 900 kB und wie viele GB 1 TB sind.
4. Für ein Paket stehen **genau 20 Byte Nutzdatenplatz** zur Verfügung. Es soll **AM TOR** und ein **8×8-Schwarzweißbild** enthalten. Passt das? Zeige die Rechnung und den Rest. Würde stattdessen ein 16×16-Bild passen?

<details><summary>Hilfe: Eine große Zahl macht noch keine große Datenmenge</summary>
<p>Vergleiche erst nach einer passenden Umrechnung. 1 500 MB lassen sich beispielsweise mit 3 GB vergleichen, wenn du beide Angaben in MB schreibst. Für 1 TB brauchst du nicht alle Nullen auszuschreiben: Der nächste Schritt nach unten führt zu GB.</p>
</details>

## 4 · Fehler erklären und erneut rechnen · 10 Minuten

Vergleicht eure Rechenwege. Ein Ergebnis ohne Einheit wird vervollständigt; bei einem Faktorfehler korrigiert ihr den betreffenden Schritt.

**Neuer Fall, zuerst allein:** Ein anderes Paket enthält **zehn ASCII-Zeichen in unserer Byte-Darstellung** und ein **16×8-Schwarzweißbild**. Hat es höchstens 30 Byte Nutzdaten? Notiere eine Rechnung und begründe deine Entscheidung.

Die gemeinsame [[Datenbogen - Sicherung|Sicherung]] hält Rechenregeln und Modellgrenze fest. Deine eigenen Rechnungen bleiben daneben sichtbar. DAT-5 braucht besonders den Zusammenhang: mehr Pixel bedeuten bei unverändertem Bitbedarf pro Pixel mehr Nutzdaten.
