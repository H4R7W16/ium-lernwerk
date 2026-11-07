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

<section class="key-transfer" id="zweckwechsel"><h3>Neuer Zweck: zwei Schlüssel unterscheiden</h3><p>Jetzt sollen die Bilder helfen, Schlüssel I und II an ihren Zähnen auseinanderzuhalten.</p><figure><img src="material/schluesselpaar-4.svg" alt="Schlüssel I und II mit jeweils 4 mal 4 Pixeln. Vergleiche die Raster; dieselben Werte findest du in den Tabellen."/><figcaption>I links · II rechts · gleiche Anzeigegröße · <a href="material/schluesselpaar-4.svg">Bild größer öffnen</a></figcaption></figure><p><strong>Zuerst selbst:</strong> Findest du in diesen 4×4-Bildern einen Unterschied? Reichen sie für den neuen Zweck? Halte dein erstes Urteil kurz in derselben Notiz fest.</p><details><summary>Rasterwerte 4 × 4 lesen</summary><p>0 = weiß, 1 = schwarz. Die Spalten stehen oben, die Zeilen links; gezählt wird ab links oben.</p><table><caption>Schlüssel I · 4 × 4</caption><thead><tr><th scope="col">Zeile</th><th scope="col">1</th><th scope="col">2</th><th scope="col">3</th><th scope="col">4</th></tr></thead><tbody><tr><th scope="row">1</th><td>1</td><td>1</td><td>0</td><td>0</td></tr><tr><th scope="row">2</th><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><th scope="row">3</th><td>0</td><td>0</td><td>1</td><td>1</td></tr><tr><th scope="row">4</th><td>0</td><td>0</td><td>0</td><td>0</td></tr></tbody></table><table><caption>Schlüssel II · 4 × 4</caption><thead><tr><th scope="col">Zeile</th><th scope="col">1</th><th scope="col">2</th><th scope="col">3</th><th scope="col">4</th></tr></thead><tbody><tr><th scope="row">1</th><td>1</td><td>1</td><td>0</td><td>0</td></tr><tr><th scope="row">2</th><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><th scope="row">3</th><td>0</td><td>0</td><td>1</td><td>1</td></tr><tr><th scope="row">4</th><td>0</td><td>0</td><td>0</td><td>0</td></tr></tbody></table></details><details id="vergleich-8"><summary>Danach: mit 8×8 Pixeln prüfen</summary><figure><img src="material/schluesselpaar-8.svg" alt="Schlüssel I und II mit jeweils 8 mal 8 Pixeln. Vergleiche die Raster; dieselben Werte findest du in den Tabellen."/><figcaption>I links · II rechts · gleiche Anzeigegröße · <a href="material/schluesselpaar-8.svg">Bild größer öffnen</a></figcaption></figure><p>Prüfe dein Urteil erneut. Zeige ein entscheidendes Feld mit Zeile und Spalte. Welche Auflösung würdest du für diese beiden Modelle wählen? Begründe auch, was du damit noch nicht über echte Schlüssel weißt.</p><details><summary>Rasterwerte 8 × 8 lesen</summary><p>0 = weiß, 1 = schwarz. Die Spalten stehen oben, die Zeilen links; gezählt wird ab links oben.</p><table><caption>Schlüssel I · 8 × 8</caption><thead><tr><th scope="col">Zeile</th><th scope="col">1</th><th scope="col">2</th><th scope="col">3</th><th scope="col">4</th><th scope="col">5</th><th scope="col">6</th><th scope="col">7</th><th scope="col">8</th></tr></thead><tbody><tr><th scope="row">1</th><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><th scope="row">2</th><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><th scope="row">3</th><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><th scope="row">4</th><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><th scope="row">5</th><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td></tr><tr><th scope="row">6</th><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td></tr><tr><th scope="row">7</th><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><th scope="row">8</th><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr></tbody></table><table><caption>Schlüssel II · 8 × 8</caption><thead><tr><th scope="col">Zeile</th><th scope="col">1</th><th scope="col">2</th><th scope="col">3</th><th scope="col">4</th><th scope="col">5</th><th scope="col">6</th><th scope="col">7</th><th scope="col">8</th></tr></thead><tbody><tr><th scope="row">1</th><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><th scope="row">2</th><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><th scope="row">3</th><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><th scope="row">4</th><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><th scope="row">5</th><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td></tr><tr><th scope="row">6</th><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td></tr><tr><th scope="row">7</th><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><th scope="row">8</th><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr></tbody></table></details></details><details id="gegenpruefung"><summary>Erst nach deinem Urteil: Vorlagen und Gegenprüfung</summary><figure><img src="material/schluesselpaar-vorlagen.svg" alt="Die beiden geometrischen Schlüsselvorlagen zur Gegenprüfung."/><figcaption>Eigene Modellvorlagen · nach derselben Mittelpunktregel gerastert · <a href="material/schluesselpaar-vorlagen.svg">Bild größer öffnen</a></figcaption></figure><p>Die 4×4-Raster sind gleich. Im 8×8-Raster ist Zeile 6, Spalte 8 bei I weiß und bei II schwarz. Der rechte Zahn ist in der zweiten Vorlage länger. Größeres Anzeigen der 4×4-Bilder gewinnt dieses Detail nicht zurück.</p><p>Die feinere Variante unterscheidet diesen Modellfall. Ob Fotos echter Schlüssel alle nötigen Unterschiede zeigen, ist damit nicht geprüft. Je Bild bleiben es 16 oder 64 Bit Nutzdaten; ein Paar benötigt jeweils doppelt so viele. Die SVG-Dateigröße ist nicht diese Modellrechnung.</p></details></section>

**Festhalten:** Eine kleine Datenmenge ist sinnvoll, wenn die benötigten Informationen erhalten bleiben. Mehr Pixel können Details erhalten; sie garantieren nicht für jeden Zweck ausreichende Qualität. Vergrößern allein gewinnt verlorene Details nicht zurück. Deine Entscheidung braucht Zweck, Beleg, Datenrechnung und eine Grenze ihrer Aussage. Die [[Datenbogen - Sicherung|gemeinsame Sicherung]] bündelt das Ergebnis.
