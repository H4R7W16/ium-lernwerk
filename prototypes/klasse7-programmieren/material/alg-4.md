# ALG-4 · Warum fährt der Rover immer weiter?

**75 Minuten · Rover-Werkstatt.** Die Haltestelle liegt bei 40. Der Rover soll fahren, solange er davor steht. Erreicht oder überschreitet er die Marke, ist Schluss. Dieser Entwurf schafft das nicht für jeden Start.

## 1 · Eine verdächtige Schleife · 15 Minuten gemeinsam

```text
Startposition setzen; Richtung 90°
wiederhole bis x-Position = 40
    gehe 10 Schritte
sage fertig
```

`wiederhole 4-mal` zählt vier Durchläufe. `wiederhole bis …` prüft dagegen **vor jeder Bewegung**, ob die Abbruchbedingung wahr ist. Dann endet die Schleife – auch ohne eine einzige Bewegung.

## 2 · Drei Starts, eine Frage · 15 Minuten gemeinsam

Sage für **0, 40 und 45** voraus: Welche Positionen folgen? Endet der Entwurf? Vergleiche mit vier festen Zehnerschritten ab derselben Position.

Öffne das Startprojekt. Teste 0 und 40 mit **Starten**. Für 45 aktiviere **Schrittmodus**, starte und nutze **Ein Schritt**. Stoppe spätestens nach vier Bewegungen mit **Stopp**. Warum können positive Zehnerschritte von 45 aus die 40 nie erreichen?

## 3 · Deine Reparatur · 30 Minuten

Ändere **nur die Abbruchbedingung**. Dein Vorschlag muss bei allen drei Starts an oder hinter 40 aufhören. Der Bewegungsblock bleibt bei 10. Wähle einen passenden Vergleich; `nicht` steht zur Verfügung.

Führe für den Start 0 eine kurze Prüfspur:

| x bei der Prüfung | Bedingung wahr/falsch | Nächste Handlung |
|---|---|---|
| 0 | … | … |
| weitere Prüfungen bis zum Ende | … | … |

Notiere auch die letzte Prüfung. Ergänze für Start 40 und 45 jeweils die erste Prüfung. Prüfe deine Vorhersagen im Programm. Begründe die Reparatur an einem dieser Fälle; eine neue Ablaufgrafik ist hier nicht nötig.

## 4 · Hält die Reparatur? · 15 Minuten

Lasse einen deiner Fälle gegenprüfen und verbessere bei Bedarf. **Neuer Kurzfall:** Start 35, Schrittweite 12. Sage Endposition und Zahl der Bewegungen voraus, prüfe und erkläre, warum Gleichheit allein nicht genügt.

**Behalte:** deine Prüfspur und den begründeten neuen Fall. Stelle Start 0 und Schrittweite 10 wieder her. Sichere `ALG-4_Kennung.xml` über **Datei speichern**, öffne sie über **Datei öffnen** und teste.

<details><summary>Hilfe</summary>

„Noch vor 40?“ ist eine Fortsetzungsfrage. Der `bis`-Block braucht die Abbruchfrage. Prüfe einen Vorschlag zuerst gedanklich bei 40 und 45. Das Modell gilt hier für positive Schritte nach rechts; es steuert keinen echten Roboter.

</details>
