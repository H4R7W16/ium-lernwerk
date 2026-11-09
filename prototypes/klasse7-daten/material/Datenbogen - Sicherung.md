---
type: output
status: reviewed
area: Unterricht
project: IuM-Lernwerk
klassenstufe: 7
fassung: "1.1"
created: 2026-10-28
updated: 2026-11-07
tags:
  - output/sicherung
---

# Kommt deine Botschaft an? Unsere Sicherung

Diese Seite wird **nach der jeweiligen Besprechung** genutzt. Sie hält die gemeinsamen Ergebnisse fest. Deine eigenen Versuche, Rechnungen und Änderungen bleiben in deinen Werkstattnotizen.

## 1 · Eindeutig zurückübersetzen

Codieren ordnet Zeichen Codewörter zu. Decodieren übersetzt mithilfe derselben Vereinbarung zurück. Bei unserem eigenen Code sind die Codewörter gleich lang und für alle Zeichen verschieden. Vom vereinbarten Anfang aus kann man die Bitfolge deshalb eindeutig in Zweiergruppen zerlegen und jede Gruppe einem Zeichen zuordnen.

Verschiedene Codewörter allein genügen bei unterschiedlichen Längen nicht immer: Bei A → 0, M → 01 und O → 1 kann `01` sowohl M als auch AO bedeuten. Eine feste Länge mit verschiedenen Codewörtern ist eine mögliche Reparatur. Andere Längen sind nicht grundsätzlich verboten; dann müssen die Grenzen anders eindeutig bestimmbar sein.

Fremdes Decodieren prüft, ob eine Vereinbarung verständlich ausgeführt wurde. Zwei erfolgreiche Nachrichten beweisen noch nicht für alle Fälle Eindeutigkeit; dafür betrachten wir zusätzlich die Regel. Codierung allein schützt keine Geheimnisse.

## 2 · Gemeinsame Zeichenvereinbarung

ASCII ist ein 7-Bit-Zeichencode. In unserer Darstellung steht davor eine Null: So passt der Code in ein Byte mit acht Bits. Ein Textleerzeichen hat einen eigenen Code; die Abstände zwischen dargestellten Achtblöcken sind nur Lesehilfen. Groß- und Kleinbuchstaben haben unterschiedliche Codes.

Eigener Code und ASCII ordnen Zeichen Bitfolgen zu. Beim eigenen Code vereinbart das Team die Tabelle. Bei ASCII ist die Zuordnung festgelegt. Moderne Texte können andere Codierungen benutzen; deshalb gilt „ein Zeichen = ein Byte“ nicht allgemein. Ursprüngliches ASCII enthält zum Beispiel keine Umlaute oder Emoji.

## 3 · Bildvorlage, Raster und Bits

Beim Diskretisieren wird die Vorlage in endlich viele Felder überführt. In unserem Modell wird ein Feld schwarz, wenn sein Mittelpunkt auf der schwarzen Form liegt; ein Randpunkt zählt als schwarz. Eine andere Abtastregel kann zu anderen Pixeln führen. Unsere Regel ist ein einfaches Modell, keine vollständige Beschreibung einer Kamera.

Danach beschreiben wir das Raster durch Bits: 0 für weiß, 1 für schwarz, zeilenweise von links oben. **Breite, Höhe, Farbzuordnung und Leserichtung** gehören zur Bildvereinbarung. Die Herstellungsvorschrift erklärt den Weg von der Vorlage zum Raster. Zum Rückübersetzen der bereits festgelegten Bits reicht die Bildvereinbarung.

Eine fehlerfreie Rückübersetzung gewinnt das Raster zurück. Sie gewinnt nicht automatisch Details zurück, die beim Diskretisieren verloren gingen. Mehr Pixel können feinere Unterschiede erhalten. Die bloße Vergrößerung eines vorhandenen Pixelbildes fügt keine ursprünglichen Details hinzu.

## 4 · Datenmengen nachvollziehbar bestimmen

Die Datenmenge wird hier durch die Anzahl der Bits beschrieben. Ein Byte besteht aus acht Bits.

| Modell | Rechnung |
|---|---|
| ASCII-Text in unserer Byte-Darstellung | Zeichenzahl einschließlich Leerzeichen × 8 Bit |
| Unkomprimiertes Schwarzweißraster mit einem Bit pro Pixel | Breite × Höhe × 1 Bit |
| Bits in Byte | Bitzahl ÷ 8 |
| Byte in Bits | Bytezahl × 8 |

Alle Pixel zählen, auch weiße. Zwei 8×8-Bilder benötigen in diesem Modell jeweils 64 Bit = 8 Byte. Die Anzahl schwarzer Felder ändert daran nichts.

Bei den Dezimalpräfixen gilt: 1 kB = 1 000 Byte, 1 MB = 1 000 kB, 1 GB = 1 000 MB, 1 TB = 1 000 GB. Bei Vergleichen zuerst dieselbe Einheit verwenden. Die Rechnung betrifft den Nutzdatenanteil. Eine reale Datei kann zusätzliche Angaben enthalten und komprimiert sein; ihre Dateigröße ist deshalb nicht mit jeder Modellrechnung identisch.

## 5 · Datenmenge und Zweck zusammen betrachten

Eine passende Auflösung erhält die Informationen, die für den Zweck gebraucht werden. Bei gleicher Bits-pro-Pixel-Zahl hat ein 8×8-Bild viermal so viele Nutzdaten wie ein 4×4-Bild: 64 statt 16 Bit, also 8 statt 2 Byte. Der Faktor ergibt sich aus **beiden** Bildrichtungen.

Unter sonst gleichen Bedingungen müssen damit mehr Daten übertragen und gespeichert werden. Geräte, Netze und Speicher benötigen Energie; die Herstellung benötigt Rohstoffe. Aus der Bitzahl allein folgt aber kein fester Stromverbrauch und keine CO₂-Menge. Technik, Nutzung und Betrieb beeinflussen den Bedarf.

Im konstruierten Schlüsselpaar kann das gleiche 4×4-Raster zwei Vorlagen entsprechen. Vergrößern gewinnt den verlorenen Unterschied nicht zurück. Das 8×8-Raster erhält hier einen Unterschied, ist aber keine allgemeine Qualitätsgarantie.

Eine begründete Wahl nennt **Zweck, sichtbares Detail, Datenmenge und Aussagegrenze**. Eine kleine Datei, die den nötigen Unterschied nicht erkennen lässt, erfüllt den Auftrag nicht. Mehr Pixel allein garantieren ebenfalls keine ausreichende Darstellung.

## Später wieder aufgreifen

Mit Abstand bearbeitet ihr neue Code- und Datenfälle zuerst ohne diese Sicherung. Dafür sind im Jahrgang bereits 20 Minuten außerhalb der 270 Minuten dieses Bogens vorgesehen. Die Lehrperson legt den Termin fest und nutzt die Ergebnisse, um gezielt zu unterstützen.


## Zwei Rückwege unterscheiden · Fassung 1.1

Bei der vorhandenen Abnahme in DAT-3 erklärt jede Person an einer Zelle: Bits lassen sich mit der Bildvereinbarung eindeutig zum Raster zurücklesen. Der ursprüngliche Umriss lässt sich daraus nicht eindeutig zurückgewinnen. Bei Verwechslung nur eine Zelle gemeinsam prüfen; eine andere Zelle danach selbst erklären lassen. DAT-5 verwendet diese Grenze für das Zweckurteil. Keine zusätzliche Aufgabe; 75 Minuten in DAT-3 und 270 Minuten im Datenbogen bleiben erhalten.
