---
type: output
status: reviewed
area: Unterricht
project: IuM-Lernwerk
klassenstufe: 7
fassung: "1.0"
created: 2026-10-28
updated: 2026-11-05
tags:
  - output/lernmaterial
---

# DAT-5 · So klein wie sinnvoll?

**30 Minuten · eigene Entscheidung mit Gegenprüfung**

Für einen **fiktiven schulischen Leihplan** soll ein kleines Schlüsselzeichen übertragen werden. Der Plan zeigt damit: Hier kannst du einen Schlüssel ausleihen. Entscheide, welche Bilddaten für diesen Zweck ausreichen.

## 1 · Erst den Zweck klären · 5 Minuten

![Schlüsselzeichen in 4×4 und 8×8 Pixeln, gleich groß dargestellt](../../../../../Assets/IuM-Lernwerk/Daten/2026-10-28-Fassung-1.0/material/schluessel-vergleich.svg)

A hat **4×4 Pixel**, B hat **8×8 Pixel**. Beide verwenden ein Bit je Pixel. Es sind nach derselben Mittelpunktregel erzeugte Versionen derselben Vorlage, hier vergrößert dargestellt. Das ist ein Modell, keine gemessene Lesbarkeitsstudie.

<details id="schluesselraster"><summary>Beide Bilder als Raster mit Zeilen und Spalten lesen</summary>
<p>0 steht für ein weißes Feld, 1 für ein schwarzes. Zeile 1 ist oben, Spalte 1 links. Vergleiche benachbarte Felder: Wo schließt sich eine Form, wo bleibt eine Lücke?</p>
<table><caption>A · 4 × 4 Pixel</caption><thead><tr><th scope="col">Zeile</th><th scope="col">Spalte 1</th><th scope="col">Spalte 2</th><th scope="col">Spalte 3</th><th scope="col">Spalte 4</th></tr></thead><tbody><tr><th scope="row">1</th><td>1</td><td>1</td><td>0</td><td>0</td></tr><tr><th scope="row">2</th><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><th scope="row">3</th><td>0</td><td>0</td><td>1</td><td>1</td></tr><tr><th scope="row">4</th><td>0</td><td>0</td><td>0</td><td>0</td></tr></tbody></table>
<table><caption>B · 8 × 8 Pixel</caption><thead><tr><th scope="col">Zeile</th><th scope="col">Spalte 1</th><th scope="col">Spalte 2</th><th scope="col">Spalte 3</th><th scope="col">Spalte 4</th><th scope="col">Spalte 5</th><th scope="col">Spalte 6</th><th scope="col">Spalte 7</th><th scope="col">Spalte 8</th></tr></thead><tbody><tr><th scope="row">1</th><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><th scope="row">2</th><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><th scope="row">3</th><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><th scope="row">4</th><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><th scope="row">5</th><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td></tr><tr><th scope="row">6</th><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td></tr><tr><th scope="row">7</th><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><th scope="row">8</th><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr></tbody></table>
</details>

Welches Detail hilft dir zu erkennen, dass es ein Schlüssel sein soll? Prüfe es in beiden Bildern oder in den beiden Tabellen. Zeile und Spalte können als Beleg dienen.

## 2 · Daten haben einen Weg · 5 Minuten

![Qualitatives Modell: Bilddaten speichern, übertragen und anzeigen](../../../../../Assets/IuM-Lernwerk/Daten/2026-10-28-Fassung-1.0/material/datenweg.svg)

**Unser Modell:** Bei gleichem Format, gleicher Zahl von Kopien und gleicher Nutzung bedeuten mehr Bits mehr zu speichernde und zu übertragende Daten. Geräte, Netze und Speicher benötigen Energie; ihre Herstellung benötigt Rohstoffe. Der tatsächliche Energiebedarf hängt aber auch von Technik, Betrieb und Nutzung ab. Viermal so viele Nutzdaten bedeuten deshalb **nicht automatisch viermal so viel Strom**.

Rechnet gemeinsam A in Bits und Byte um. Sagt, was sich beim Wechsel zu B in der Rechnung ändert. Eine CO₂-Zahl könnt ihr aus diesen Angaben nicht bestimmen.

## 3 · Deine Entscheidung für den Leihplan · 10 Minuten

Formuliere eine Empfehlung in **drei bis fünf Sätzen**, mit Rechnung oder kurzen Stichpunkten daneben:

1. Wähle A oder B. Nenne ein Detail aus dem Bild oder dem Raster als Beleg dafür, ob das Bild seinen Zweck erfüllt. Wenn du keine Variante ausreichend findest, begründe eine Änderung.
2. Berechne die Nutzdatenmenge beider Bilder in Bit und Byte. Vergleiche sie als Verhältnis.
3. Verbinde deine Wahl mit Übertragung **und** Speicherung. Benenne, was du über den Ressourcenbedarf sagen kannst und was du ohne weitere Angaben nicht weißt.

<details><summary>Hilfe: Eine Abwägung formulieren</summary>
<p>„Für … wähle ich … . An … erkenne ich … . Gegenüber … müssen … Bits übertragen und gespeichert werden. Das ist sinnvoll, weil … . Den genauen Strombedarf kann ich daraus nicht … .“ Mehrere Entscheidungen sind möglich, wenn Zweck, Bildbeleg und Rechnung zusammenpassen.</p>
</details>

## 4 · Gegenprobe und Revision · 10 Minuten

Eine andere Person prüft deine Empfehlung: **Lässt sich das Detail im Bild oder an den genannten Rasterfeldern wiederfinden? Stimmen Menge und Zweck zusammen?** Sie stellt eine konkrete Rückfrage. Du ergänzt oder korrigierst deine Begründung. Falls ihr nicht übereinstimmt, bleibt der strittige Punkt sichtbar; die Lehrperson hilft bei der Klärung.

**Neuer Zweck – allein entscheiden:** Nun soll ein Bild helfen, **zwei sehr ähnliche Schlüssel an kleinen Unterschieden ihrer Zähne auseinanderzuhalten**. Reicht die gerade gewählte Variante dafür? Begründe, was du genauer sehen oder prüfen müsstest. Du darfst zu dem Schluss kommen, dass keine der beiden Modellvarianten den neuen Zweck zuverlässig erfüllt.

**Festhalten:** Eine kleine Datenmenge ist sinnvoll, wenn die benötigten Informationen erhalten bleiben. Mehr Pixel können Details erhalten; sie garantieren nicht für jeden Zweck ausreichende Qualität. Vergrößern allein gewinnt verlorene Details nicht zurück. Deine Entscheidung braucht Zweck, Beleg, Datenrechnung und eine Grenze ihrer Aussage. Die [[Datenbogen - Sicherung|gemeinsame Sicherung]] bündelt das Ergebnis.
