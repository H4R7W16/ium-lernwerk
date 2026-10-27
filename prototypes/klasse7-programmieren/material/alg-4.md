# ALG-4 · Warum fährt der Rover immer weiter?

**75 Minuten · Rover-Werkstatt.** Von 0 aus klappt die Fahrt. Auch von 45? Repariere den Rover: Vor 40 soll er fahren. **An oder hinter 40 darf keine weitere Bewegung folgen.** Überschreiten ist erlaubt.

## 1 · Funktioniert doch! Oder? · 10 Minuten

Vermute: Was passiert bei Start **0**, was bei **45**? Öffne das Startprojekt und teste 0 mit **Starten**.

```text
Startposition setzen; Richtung 90°
wiederhole bis x-Position = 40
    gehe 10 Schritte
sage fertig
```

Ändere nur die Startposition auf 45. Untersucht diesen Lauf gemeinsam: **Schrittmodus einschalten → Starten → Ein Schritt**. Beobachtet die x-Position nach zwei Bewegungen. Spätestens nach vier Bewegungen **Stopp**, erst danach den Schrittmodus beenden.

**Passt die Beobachtung zu deiner Vermutung?** Notiere eine Positionsfolge. Zählt Positionsänderungen; eine alte „fertig“-Blase beweist kein Ende.

## 2 · Was fragt die Schleife? · 15 Minuten

Der `bis`-Block prüft **vor der Bewegung**: Ist die Abbruchbedingung wahr? **Wahr → Schleife verlassen. Falsch → Bewegung, dann erneut prüfen.**

Start **40**: Fährt der Rover überhaupt? Begründe vor dem Test am Code. Erklärt auch, warum er von 45 mit positiven Zehnerschritten die 40 nie erreicht.

Vergleicht mündlich: Wo enden vier feste Zehnerschritte ab **0, 40 und 45**? Warum erfüllt `wiederhole 4-mal` unsere Regel nicht?

## 3 · Reparieren und testen · 35 Minuten

Formuliere deine Abbruchfrage in eigenen Worten. Ändere **nur die Abbruchbedingung**; `gehe 10 Schritte` bleibt. Wähle einen Vergleich, bei Bedarf mit `nicht`.

**Teste zuerst 40 oder 45 – du entscheidest.** Was willst du damit an deinem Vorschlag prüfen? Sage das Ergebnis vorher, teste im Schrittmodus. **Bei einer Abweichung:** Finde die erste Prüfung, die eine falsche Handlung auslöst. Kläre dort wahr/falsch, ändere gezielt und teste denselben Start erneut. Spätestens nach vier unerwarteten Bewegungen stoppen.

Prüfe mit der endgültigen Bedingung alle drei Starts. Führe für **0** die volle Prüfspur; für **40 und 45** genügt jeweils die erste Prüfung:

| x bei der Prüfung | Bedingung wahr/falsch | Nächste Handlung |
|---|---|---|
| 0 | … | … |
| weitere Prüfungen bis zum Ende | … | … |

**Die letzte Prüfung gehört dazu.** Zeige im Code, was nach ihr folgt. Eine Notiz für Vermutung, Reparatur und Spur genügt.

<details><summary>Hilfe: Er stoppt sofort oder fährt zu lange</summary>

Setze den aktuellen Ort gedanklich in deine Frage ein. Bei wahr wird gestoppt, bei falsch gefahren. Passt das zur Zielregel? „Noch vor 40?“ wäre eine Fortsetzungsfrage.

</details>

<details><summary>Hilfe: Mein Vergleich scheitert an der Grenze</summary>

Prüfe genau 40: Reicht „größer als 40“? `nicht` kehrt einen Wahrheitswert um. Grenze und Schrittweite bleiben gleich.

</details>

## 4 · Hält die Reparatur? · 15 Minuten

**Gegencheck:** Eine andere Person prüft einen deiner Fälle und fragt: „Welche Prüfung beendet den Lauf?“ Erkläre selbst und verbessere eine unklare Stelle. Allein übernimmt die Lehrperson den Gegencheck.

**Neuer Fall – erst allein, ohne Lauf:** Start 35, Schrittweite 12. Sage Endposition, Zahl der Bewegungen und der Prüfungen voraus. Teste deine Reparatur und erkläre, warum Gleichheit allein nicht genügt.

**Sichern:** Behalte Prüfspur und begründeten neuen Fall. Stelle Start 0 und Schrittweite 10 wieder her; behalte deine reparierte Bedingung. Sichere `ALG-4_Kennung.xml` über **Datei speichern**, öffne sie über **Datei öffnen** und teste erneut.

Das Modell gilt für positive Schritte nach rechts, Richtung 90°. Es steuert keinen echten Roboter.
