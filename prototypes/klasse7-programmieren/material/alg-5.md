# ALG-5 · Dein Rover, dein Härtetest

**90 Minuten · Rover-Werkstatt.** Entwickle eine Steuerung, die auch bei einem ungewohnten Start funktioniert. Dein Team soll sie anhand deiner Regeln testen können.

## 1 · Deine Regeln festlegen · 15 Minuten

Wähle die Station **60 oder 80**, die Schrittweite **10 oder 15** und zwei klare Meldungen. Der Rover startet normalerweise bei 0 und schaut nach rechts.

Dein Auftrag:

- Fahren, solange der Rover vor deiner Station steht; an oder hinter ihr keinen weiteren Schritt machen.
- Eine Meldung für „genau getroffen“, eine andere für „vorbei“ zeigen.
- Auch dann richtig reagieren, wenn der Rover bereits an oder hinter der Station startet.

Wähle bewusst: Soll der Normalfall **genau treffen** oder mit **wenigen Bewegungen** enden? Vergleiche dafür beide Schrittweiten an deiner Station. Geht beides zugleich? Halte Wahl und Grund in zwei Sätzen fest. Weniger Bewegungen bedeutet im Modell nicht automatisch weniger Energie. Die Zahlen stehen direkt im Code; eigene Variablen sind nicht nötig. Die beiden Linien auf der Bühne zeigen die möglichen Stationen.

## 2 · Vom Auftrag zum Plan · 15 Minuten gelenkt

Klärt gemeinsam nur den Mini-Fall: Position 25, Marke 30 – fahren oder stoppen? Was ändert sich bei 30 und 35?

Zeichne dann deinen **eigenen grafischen Ablaufplan**: Wo wird vor der Bewegung geprüft? Wo verzweigen die Meldungen? Mache Fragen, Rückwege und Ende sichtbar. Entscheide, welche Wiederholung deine Regel auch bei verändertem Start erfüllt.

## 3 · Bauen und selbst testen · 40 Minuten

Öffne das Startprojekt. Es enthält nur Start und Richtung. Baue deine Steuerung selbst. Zeige nach etwa zehn Minuten kurz Plan und ersten Code.

Plane ungefähr 20 Minuten fürs Bauen, 15 für Tests und 5 fürs Sichern. Führe diese kleine Testliste; schreibe die Erwartung **vor** dem Start auf:

| Fall | Deine Eingabe | Erwartete Position/Meldung | Beobachtung |
|---|---|---|---|
| Normalfall | Start 0 | … | … |
| Grenzfall | Start an deiner Station | … | … |
| Dein Gegenfall | Wähle selbst einen Start, bei dem die Marke übersprungen wird. Begründe deine Wahl. | … | … |

Wenn der Rover unerwartet weiterfährt, nutze **Stopp**. Ein kurzer Fehlweg genügt zum Untersuchen; stoppe spätestens nach sechs unerwarteten Bewegungen.

<details><summary>Hilfe: Wo beginne ich mit dem Programm?</summary>

Baue zuerst die Fahrentscheidung. `wiederhole bis …` endet bei wahr. Prüfe sie am Ziel, bevor du die Meldungsverzweigung ergänzt. „Nicht mehr davor?“ und „genau getroffen?“ sind verschiedene Fragen. **Schrittmodus** und **Ein Schritt** helfen beim Verfolgen.

</details>

<details><summary>Hilfe: Wie finde ich einen Gegenfall?</summary>

Wähle einen Start knapp vor dem Ziel. Führt ein ganzer Schritt darüber hinaus? Erkläre, warum ein Programm mit Gleichheitsabbruch hier versagen würde.

</details>

## 4 · Fremder Test, eigene Verbesserung · 20 Minuten

Tauscht einen zusätzlichen Startwert **hinter der gewählten Station** aus und sagt die Wirkung vorher voraus. Jede Person prüft am eigenen Programm. Allein übernimmt die Lehrperson den Gegencheck.

Überarbeite nach dem Test gezielt Code, Plan oder Meldung und prüfe erneut: **Änderung – Grund – neuer Test**. Ist alles klar und richtig, begründe deine Abnahme an einem kritischen Test. Einen fehlenden Test darfst du ergänzen. Keine Änderung ohne Zweck.

**Behalte:** Plan, Testliste und deine begründete Verbesserung oder Abnahme. Stelle den Start auf 0, sichere `ALG-5_Kennung.xml` über **Datei speichern**, öffne sie über **Datei öffnen** und teste erneut.
