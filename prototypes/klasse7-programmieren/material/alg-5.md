# ALG-5 · Dein Rover, dein Härtetest

**90 Minuten · Rover-Werkstatt.** Entwickle eine Steuerung, die auch bei ungewohntem Start funktioniert. Dein Testteam prüft sie an deinem Auftrag.

## 1 · Deine Regeln festlegen · 15 Minuten

Wähle Station **60 oder 80**, Schrittweite **10 oder 15** und zwei Meldungen. Normaler Start: 0, Richtung rechts.

Formuliere deinen **Einsatzauftrag**: „Mein Rover soll … . Station … und Schrittweite … passen, weil … . Ich nehme die Steuerung ab, wenn … .“ Begründe, ob dir im Normalfall ein genauer Treffer oder wenige Bewegungen wichtiger sind. Vergleiche beide Schrittweiten: Geht beides zugleich? Ergänze denselben Auftrag.

Deine Steuerung muss:

- vor der Station fahren, an oder hinter ihr keinen weiteren Schritt machen;
- „genau getroffen“ und „vorbei“ durch unterschiedliche Meldungen anzeigen;
- auch beim Start an oder hinter der Station richtig reagieren.

Weniger Bewegungen bedeutet im Modell nicht automatisch weniger Energie. Die Zahlen stehen direkt im Code; eigene Variablen sind nicht nötig. Beide möglichen Stationen sind eingezeichnet.

## 2 · Vom Auftrag zum Plan · 15 Minuten gelenkt

Klärt gemeinsam nur den Mini-Fall: Position 25, Marke 30 – fahren oder stoppen? Was ändert sich bei 30 und 35?

Markiere im Einsatzauftrag die Anforderungen an Fahrentscheidung und Meldung. Zeichne deinen **eigenen grafischen Ablaufplan** mit Fragen, Rückwegen und Ende: Wo wird vor der Bewegung geprüft? Wo verzweigen die Meldungen? Wähle eine Wiederholung, die auch bei verändertem Start passt.

## 3 · Bauen und selbst testen · 40 Minuten

Öffne das Startprojekt mit Start und Richtung. Baue selbst. Zeige nach etwa zehn Minuten Plan und ersten Code.

Plane ungefähr 20 Minuten fürs Bauen, 15 für Tests und 5 fürs Sichern. Ordne jeden Test einer Anforderung zu. Schreibe deine **Vorhersage vor dem Start** in diese Testliste:

| Fall | Deine Eingabe | Erwartete Position/Meldung | Beobachtung |
|---|---|---|---|
| Normalfall | Start 0 | … | … |
| Grenzfall | Start an der Station | … | … |
| Dein Gegenfall | Wähle und begründe einen Start, der die Marke überspringt. | … | … |

Fährt dein Rover weiter, obwohl er schon stoppen sollte? Drücke **Stopp**, spätestens nach sechs unerwarteten Bewegungen. Erwartete Schritte auf dem Weg zur Station zählen hier nicht mit.

<details><summary>Hilfe: Wo beginne ich?</summary>

Baue zuerst die Fahrentscheidung. `wiederhole bis …` endet bei wahr. Prüfe sie am Ziel, ergänze dann die Meldungsverzweigung. „Nicht mehr davor?“ und „genau getroffen?“ sind verschiedene Fragen. **Schrittmodus → Ein Schritt** hilft beim Verfolgen.

</details>

<details><summary>Hilfe: Wie finde ich einen Gegenfall?</summary>

Starte knapp vor dem Ziel. Führt ein ganzer Schritt darüber hinaus? Warum würde Gleichheit als Abbruchfrage hier scheitern?

</details>

## 4 · Fremder Test, eigene Verbesserung · 20 Minuten

Tauscht einen zusätzlichen Startwert **hinter der Station** aus. Sagt die Wirkung vorher; jede Person prüft am eigenen Programm. Allein übernimmt die Lehrperson den Gegencheck.

Überarbeite Code, Plan oder Meldung: **Änderung – Grund – neuer Test**. Prüfe gegen deinen Einsatzauftrag: Erfüllt der Normalfall deine Qualitätswahl? Halten Grenz- und Gegenfälle die Fahrregel ein? Ist alles richtig, begründe die Abnahme an einem kritischen Test. Keine Änderung ohne Zweck.

**Behalte:** Einsatzauftrag, Plan, Testliste und begründete Verbesserung oder Abnahme. Stelle Start 0 wieder her. Sichere `ALG-5_Kennung.xml` über **Datei speichern**, öffne sie über **Datei öffnen** und teste erneut.
