# ALG-5 · Dein Rover, dein Härtetest

**90 Minuten · Rover-Werkstatt.** Entwickle eine Steuerung, die auch bei einem ungewohnten Start funktioniert. Dein Team soll sie anhand deiner Regeln testen können.

## 1 · Deine Regeln festlegen · 15 Minuten

Wähle die Station **60 oder 80**, die Schrittweite **10 oder 15** und zwei klare Meldungen. Der Rover startet normalerweise bei 0 und schaut nach rechts.

Dein Auftrag:

- Fahren, solange der Rover vor deiner Station steht; an oder hinter ihr keinen weiteren Schritt machen.
- Eine Meldung für „genau getroffen“, eine andere für „vorbei“ zeigen.
- Auch dann richtig reagieren, wenn der Rover bereits an oder hinter der Station startet.

Halte deine Wahl in zwei Sätzen fest. Die Zahlen stehen direkt im Code; eigene Variablen sind nicht nötig. Die beiden Linien auf der Bühne zeigen die möglichen Stationen.

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

## 4 · Fremder Test, eigene Verbesserung · 20 Minuten

Tauscht einen zusätzlichen Startwert aus und sagt die Wirkung vorher voraus. Jede Person prüft am eigenen Programm. Allein übernimmt die Lehrperson den Gegencheck.

Überarbeite eine konkrete Stelle an Code, Plan oder Meldung und teste erneut. Notiere kurz **Änderung – Grund – neuer Test**. Wenn alles passt, darf die Verbesserung auch eine verständlichere Meldung sein.

**Behalte:** Plan, Testliste und eine begründete Verbesserung. Stelle den Start auf 0, sichere `ALG-5_Kennung.xml` über **Datei speichern**, öffne sie über **Datei öffnen** und teste erneut.

<details><summary>Hilfe nach Bedarf</summary>

„Noch vor der Station?“ und „genau getroffen?“ sind zwei verschiedene Fragen. `wiederhole bis …` endet bei wahr. `nicht (x-Position < Zielzahl)` fragt „nicht mehr davor?“. Für deinen Gegenfall hilft ein Start knapp vor dem Ziel; prüfe, ob ein ganzer Schritt darüber hinausführt. Mit **Schrittmodus** und **Ein Schritt** kannst du den Weg verfolgen.

</details>
