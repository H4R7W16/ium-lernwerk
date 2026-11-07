# ALG-6 · Die Haltestelle ist verpasst!

**60 Minuten · Rover-Werkstatt.** Ein fremdes Programm fährt über die Haltestelle 50 hinaus. Finde die Ursache und zeige, dass deine Reparatur auch bei veränderten Werten funktioniert.

## 1 · Die Codekarte beginnen · 10 Minuten gemeinsam

Öffne das Startprojekt, **starte noch nicht**. Der Rover soll zunächst zweimal je `5 + 5` Schritte fahren, dann in Zehnerschritten bis an die Marke 50 oder darüber. Genau auf 50 soll „Ziel“ erscheinen, sonst „vorbei“.

```text
Start x = 0; Richtung 90°
wiederhole 2-mal
    gehe (5 + 5) Schritte
wiederhole bis x-Position > 50
    gehe 10 Schritte
falls x-Position = 50
    sage Ziel
sonst
    sage vorbei
```

Beginnt in der [Ablaufvorlage](../bilder/alg6-codekarte.svg) gemeinsam bei 0 und dem ersten festen Durchlauf. Ergänze Positionen und Notizen auf **einer Codekarte**: als Skizze oder auf dem Ausdruck. Eine zusätzliche Laufspurtabelle brauchst du nicht.

<img src="../bilder/alg6-codekarte.svg" alt="Ablaufvorlage mit Start, fester Wiederholung, vorangestellter Abbruchfrage, Bewegung mit Rücksprung und zwei Meldungszweigen. Ergänze Positionen, Durchlaufzahlen und Wahrheitswerte." class="codekarte">

## 2 · Untersuchen und reparieren · 35 Minuten

**Drei Prüffragen:** Wo steht der Rover? Was ergibt die nächste Bedingung? Welche Handlung folgt? Ergänze die Antworten an der passenden Stelle deiner Codekarte.

**Vorhersage:** Ergänze die Positionsfolge an beiden Schleifen bis zur Meldung. Beschrifte die Bedingungsausgänge mit wahr/falsch. Notiere auch die letzte Abbruchprüfung.

**Prüfen:** Nutze **Schrittmodus**, **Starten**, dann **Ein Schritt**. Vergleiche mit deiner ersten Spur. Markiere die erste Prüfung, deren Folge gegen den Auftrag verstößt. Formuliere dort die Fehlerursache und ändere nur die Abbruchbedingung. Prüfe denselben Fall erneut.

<details><summary>Hilfe: Wo beginnt der Fehler?</summary>

Suche die erste Bewegung, die nicht mehr erlaubt wäre. Welche Frage wurde unmittelbar davor geprüft? Was liefert sie an dieser Position?

</details>

<details><summary>Hilfe: Wie ändere ich die Abbruchfrage?</summary>

Soll bei wahr weitergefahren oder aufgehört werden? Formuliere „erreicht oder überschritten“ anders: „nicht mehr …“. Baue daraus einen Vergleich, bei Bedarf mit `nicht`. Erprobe den neuen Kurzfall danach selbst.

</details>

**Deine Variante:** Wähle für die bedingte Schleife Schrittweite **12 oder 15**. Welche Wahl trifft die Marke, welche überspringt sie? Sage Endposition und Meldung vorher voraus, führe aus und ergänze beides auf der Karte. Was erklärt die Veränderung?

**Nach der Reparatur: fachlich sichern.** Erkläre an deiner Karte Anweisung, feste Wiederholung, bedingte Wiederholung und Verzweigung. Zeichne nichts erneut.

**Randnotizen zum ursprünglichen Code:** Ergänze auf derselben Karte: Eingabe → Wert mit Werttyp oder Wirkung. Nenne einen Rechen-/Vergleichsoperator, wenn vorhanden. Stichwörter und Pfeile genügen.

<details><summary>Hilfe: Werttyp, Operator und kurze Notiz</summary>

Werttypen sind Zahl, Zeichenkette (Text) und Wahrheitswert (wahr/falsch). Beispiel an anderem Code: `3 * 4`: Eingaben 3 und 4 → 12 (Zahl); Operator `*` multipliziert. Operatoren rechnen oder vergleichen, etwa `*` oder `<`.

</details>

| Stelle | Deine kurze Notiz |
|---|---|
| `10` | … |
| `5 + 5` in `gehe … Schritte` | … |
| `x-Position` nach der festen Wiederholung | … |
| `x-Position > 50` bei x = 50 | … |
| `sage Ziel` | … |

Richtwert: 10 Minuten Spur, 18 Minuten Erprobung/Reparatur/Variante, 7 Minuten Randnotizen.

## 3 · Gegencheck und Kurzfall · 15 Minuten

Lasse einen kritischen Schritt erklären und verbessere deine Karte oder Reparatur. **Neuer Kurzfall:** Setze die bedingte Schrittweite auf 10 zurück und ändere die feste Wiederholung auf **3**. Sage die Zahl der Bewegungen beider Schleifen und die Meldung voraus, prüfe und begründe.

**Behalte:** deine Codekarte mit erster Spur, Randnotizen, Reparaturgrund und Varianten. Sichere die reparierte Fassung mit **2 Wiederholungen und Schrittweite 10** über **Datei speichern** als `ALG-6_Kennung.xml`. Prüfe sie über **Datei öffnen**.
