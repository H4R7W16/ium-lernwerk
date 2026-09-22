# Verifikation · Lernstudio · 23.09.2026

Geprüft durch Codex im bestehenden lokalen IuM-Worktree. Selbstprüfung, keine unabhängige Lernendenerprobung.

## Automatisiert

- 78/78 gezielte Tests: Material, vorhandene Lernfassung 3, Lernwerkstatt, neues Lernstudio und öffentliche Dateizuordnung.
- 10 Lernstudio-Tests: Checkabdeckung, Rückmeldung/Unterstützung, Invalidierung nach Änderungen, sichere Wiederherstellung, Endvorhersage, fachliche Vergleichsfälle, leerer Anfangszustand und atomare Ablehnung ungültiger Schleifenkörper.
- Fehlerfälle vor der Korrektur rot und anschließend grün: fehlendes Modell, leerer eigener Plan, unzulässiger Schleifenkörper.
- Vollständiger statischer Build mit Syntaxprüfung: 35 öffentliche Dateien. Die vier neuen Laufzeitdateien werden separat unter /lernstudio/ ausgeliefert.
- git diff --check ohne Fehler. Keine Import-/Exporttests, keine Gesamtsuite.

## Im tatsächlichen In-App-Browser bedient

| Prüfung | Ergebnis |
| --- | --- |
| 1024 × 768 | Beide Arbeitsflächen sichtbar; Unterkante der vollständigen Steuerung bei 754 CSS-Pixeln, keine horizontale Überbreite. Im geprüften Einstieg keine Schaltfläche unter 44 × 44 CSS-Pixeln. |
| 768 × 1024 | Programm und Simulation nebeneinander; Hinweise, Erklärung und Prüfstation nutzbar. Ein anfangs überbreiter Stationsaufbau korrigiert und erneut visuell geprüft. |
| 320 × 780 | Einspaltige Ersatzansicht ohne horizontale Seitenüberbreite. Kleine Kapitellabels sind keine Optimierung für den Haupteinsatz. |
| Elf Stationen | Alle über den Lernweg geöffnet; Startzustände und Schrittzahlen vorhanden; keine Browserfehler im frischen Prüflauf. |
| Vorhersage | Zielkachel und Blick eingegeben, drei Schritte ausgeführt, richtige gemeinsame Rückmeldung. Auswahl während der Fahrt eingefroren. |
| Schleife | Aktiver Körperbefehl synchron. Ein animierter Durchlauf endet nach vor → links bei Schritt 2/8; Wiedergabe pausiert dort. |
| Reparatur | Fehlerhaften Lauf beobachtet, links in den Körper aufgenommen, Folgeanweisung entfernt; vier Kacheln, Rückkehr und richtiger Blick anerkannt. |
| Eigener Plan | Vollständigen Reihenplan über den Codeeditor eingegeben und ausgeführt; zwölf Kacheln, kein Wandstopp und Schleife anerkannt. |
| Selbstcheck | Falsche Antwort mit spezifischer Erklärung; Korrektur erfolgreich, als erneuter/unterstützter Check kenntlich. |
| Transfer | Plan B stoppt beim zweiten Aufnehmen; Plan A bearbeitet automatisch alle drei Werkstücke. |
| Editor | Körper maximal fünf Befehle; danach Ergänzung gesperrt und Fokus auf Übernehmen. Escape schließt Dialog. |
| Speichern | Opt-in, Neustart, Wiederaufnahme des beobachteten Zustands; anschließend Speicherung über die UI ausgeschaltet. Nur selbst erzeugte lokale Testdaten verwendet. |
| Wissen | Vollständige Erklärung gezielt geöffnet; Rückkehr zum Experiment vorhanden. |

## Offen

- Reale Schul-iPads einschließlich Safari, Hoch-/Querformatwechsel und Bildschirmtastatur.
- Umfassende Prüfung mit Screenreader, echtem 200-%-Zoom und reduzierter Bewegung im Betriebssystem. CSS-Präferenz und semantische Bedienelemente sind implementiert; daraus folgt kein vollständiger Barrierefreiheitsnachweis.
- Lernendenerprobung: finden sie den Einstieg, bilden sie korrekte Vorhersagen, verstehen sie die Gruppierung, übertragen sie den Plan? Motivation, Belastung und Transfer getrennt erheben.
- Vergleich mit der bisherigen Lernwerkstatt und Lesefassung; keine empirische Überlegenheit behauptet.
