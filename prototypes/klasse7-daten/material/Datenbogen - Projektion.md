---
type: output
status: reviewed
area: Unterricht
project: IuM-Lernwerk
klassenstufe: 7
fassung: "1.0"
created: 2026-10-28
updated: 2026-11-07
tags:
  - output/projektion
---

# Fünf Impulse für die gemeinsame Besprechung

Die Großansichten zeigen jeweils nur den aktuellen Denkauftrag. Erwartungen und Moderation stehen im Durchführungsplan. Die vollständige Arbeitsseite wird nicht als Folie verkleinert.

## P1 · Eine Bitfolge – zwei Texte?

| Zeichen | Code |
|---|---|
| A | 0 |
| M | 01 |
| O | 1 |

> Angekommen: **01**

Welche Texte könnten gemeint sein? Zeige, wo du trennst.

## P2 · Welcher Text kommt an?

> Gewollt: **AM**
>
> Gesendet: **01000001 01101101**

Welche Tabellenzeile entscheidet? Prüfe den zweiten Block.

## P3 · Was erhält die Übertragung?

![Vorlage, Raster mit Mittelpunkten und Pixelbild](../../../../../Assets/IuM-Lernwerk/Daten/2026-10-28-Fassung-1.0/material/dreieck-weg.svg)

Das Raster kommt fehlerfrei an. Kommt damit auch die ursprüngliche Kante genau zurück?

## P4 · Ein Paket mit 20 Byte Platz

> **AM TOR** und ein **8×8-Bild**

Text: acht Bits pro Zeichen. Bild: ein Bit pro Pixel. Nur Nutzdaten zählen.

Passt das? Zeige Rechnung und Rest in Byte.

## P5 · Wann genügt die kleinere Variante?

![Schlüssel in zwei Rasterauflösungen](../../../../../Assets/IuM-Lernwerk/Daten/2026-10-28-Fassung-1.0/material/schluessel-vergleich.svg)

Erst: ein Zeichen für die Schlüsselausleihe.

<section class="key-transfer" id="zweckwechsel"><h3>Neuer Zweck: zwei Schlüssel unterscheiden</h3><p>Jetzt sollen die Bilder helfen, Schlüssel I und II an ihren Zähnen auseinanderzuhalten.</p><figure><img src="material/schluesselpaar-4.svg" alt="Schlüssel I und II mit jeweils 4 mal 4 Pixeln. Vergleiche die Raster; dieselben Werte findest du in den Tabellen."/><figcaption>I links · II rechts · gleiche Anzeigegröße · <a href="material/schluesselpaar-4.svg">Bild größer öffnen</a></figcaption></figure><p><strong>Zuerst selbst:</strong> Findest du in diesen 4×4-Bildern einen Unterschied? Reichen sie für den neuen Zweck? Halte dein erstes Urteil kurz in derselben Notiz fest.</p><details><summary>Rasterwerte 4 × 4 lesen</summary><p>0 = weiß, 1 = schwarz. Die Spalten stehen oben, die Zeilen links; gezählt wird ab links oben.</p><table><caption>Schlüssel I · 4 × 4</caption><thead><tr><th scope="col">Zeile</th><th scope="col">1</th><th scope="col">2</th><th scope="col">3</th><th scope="col">4</th></tr></thead><tbody><tr><th scope="row">1</th><td>1</td><td>1</td><td>0</td><td>0</td></tr><tr><th scope="row">2</th><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><th scope="row">3</th><td>0</td><td>0</td><td>1</td><td>1</td></tr><tr><th scope="row">4</th><td>0</td><td>0</td><td>0</td><td>0</td></tr></tbody></table><table><caption>Schlüssel II · 4 × 4</caption><thead><tr><th scope="col">Zeile</th><th scope="col">1</th><th scope="col">2</th><th scope="col">3</th><th scope="col">4</th></tr></thead><tbody><tr><th scope="row">1</th><td>1</td><td>1</td><td>0</td><td>0</td></tr><tr><th scope="row">2</th><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><th scope="row">3</th><td>0</td><td>0</td><td>1</td><td>1</td></tr><tr><th scope="row">4</th><td>0</td><td>0</td><td>0</td><td>0</td></tr></tbody></table></details><details id="vergleich-8"><summary>Danach: mit 8×8 Pixeln prüfen</summary><figure><img src="material/schluesselpaar-8.svg" alt="Schlüssel I und II mit jeweils 8 mal 8 Pixeln. Vergleiche die Raster; dieselben Werte findest du in den Tabellen."/><figcaption>I links · II rechts · gleiche Anzeigegröße · <a href="material/schluesselpaar-8.svg">Bild größer öffnen</a></figcaption></figure><p>Prüfe dein Urteil erneut. Zeige ein entscheidendes Feld mit Zeile und Spalte. Welche Auflösung würdest du für diese beiden Modelle wählen? Begründe auch, was du damit noch nicht über echte Schlüssel weißt.</p><details><summary>Rasterwerte 8 × 8 lesen</summary><p>0 = weiß, 1 = schwarz. Die Spalten stehen oben, die Zeilen links; gezählt wird ab links oben.</p><table><caption>Schlüssel I · 8 × 8</caption><thead><tr><th scope="col">Zeile</th><th scope="col">1</th><th scope="col">2</th><th scope="col">3</th><th scope="col">4</th><th scope="col">5</th><th scope="col">6</th><th scope="col">7</th><th scope="col">8</th></tr></thead><tbody><tr><th scope="row">1</th><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><th scope="row">2</th><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><th scope="row">3</th><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><th scope="row">4</th><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><th scope="row">5</th><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td></tr><tr><th scope="row">6</th><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td></tr><tr><th scope="row">7</th><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><th scope="row">8</th><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr></tbody></table><table><caption>Schlüssel II · 8 × 8</caption><thead><tr><th scope="col">Zeile</th><th scope="col">1</th><th scope="col">2</th><th scope="col">3</th><th scope="col">4</th><th scope="col">5</th><th scope="col">6</th><th scope="col">7</th><th scope="col">8</th></tr></thead><tbody><tr><th scope="row">1</th><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><th scope="row">2</th><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><th scope="row">3</th><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><th scope="row">4</th><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><th scope="row">5</th><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td></tr><tr><th scope="row">6</th><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td></tr><tr><th scope="row">7</th><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><th scope="row">8</th><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr></tbody></table></details></details><details id="gegenpruefung"><summary>Erst nach deinem Urteil: Vorlagen und Gegenprüfung</summary><figure><img src="material/schluesselpaar-vorlagen.svg" alt="Die beiden geometrischen Schlüsselvorlagen zur Gegenprüfung."/><figcaption>Eigene Modellvorlagen · nach derselben Mittelpunktregel gerastert · <a href="material/schluesselpaar-vorlagen.svg">Bild größer öffnen</a></figcaption></figure><p>Die 4×4-Raster sind gleich. Im 8×8-Raster ist Zeile 6, Spalte 8 bei I weiß und bei II schwarz. Der rechte Zahn ist in der zweiten Vorlage länger. Größeres Anzeigen der 4×4-Bilder gewinnt dieses Detail nicht zurück.</p><p>Die feinere Variante unterscheidet diesen Modellfall. Ob Fotos echter Schlüssel alle nötigen Unterschiede zeigen, ist damit nicht geprüft. Je Bild bleiben es 16 oder 64 Bit Nutzdaten; ein Paar benötigt jeweils doppelt so viele. Die SVG-Dateigröße ist nicht diese Modellrechnung.</p></details></section>
