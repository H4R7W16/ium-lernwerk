# Klasse 6 M05 – Dein Muster. Dein Programm.

Stand 22.10.2026, Inhalt 1.0.0. Baseline `90e8755`, Branch `feat/klasse6-m05-algorithmen`. Lokale Produktion, keine Veröffentlichung.

## Lernbogen und Inhalt

Musterband für ein Klassenfest: Auftakt → vollständig erklärtes L-Modell → Quadratfehler untersuchen → eigenes Band mit Ablaufgrafik und Code → Rückmeldung und Revision → neuer Stiftzustand im Transfer → zwei spätere Abrufe. Sechs Schritte, sieben Wissensartikel, drei eigene SVGs, sechs druckbare Einzelmaterialien mit Hilfen/Lösungen und drei Blankorastern, Lehrhinweise, Reihenkommentar und Textbriefing.

135 Kernminuten, zusätzlich sieben Minuten M04-Abruf davor und je sieben M05-Abrufminuten vor M06/M07 aus dem bestehenden Jahreskonto. Ziele 3.1.3.1(1)–(6) der aktiven AHF-Projektplanung dee82ec. Vollständige Ziel-/Nachweismatrix im Vault: „2026-10-22 - Klasse 6 M05 Inhaltsbrief und Medienwahl“.

Ein wachsendes eigenes Produkt, getrenntes Modell, Hilfen am Arbeitsort und überprüfte Revision übertragen die Recherchekapitel-Erkenntnisse. Keine allgemeine Python-/Scratchkompetenz und keine empirisch nachgewiesene Lernwirkung behaupten.

## Technische Entscheidung

`prototypes/m05-zeichnen/`: kleine deterministische Sprache `vor`, `rechts`, `links`, `hoch`, `runter`, `wiederhole N [ ... ]`. Kein eval, keine Konten, keine neue Abhängigkeit. Begrenztes Raster, höchstens 200 Anweisungen, feste Schleifen 1–9. Einzelschritt und vollständige Ausführung; exakte aufgenommene Spuren werden zusammen mit Code und eigenen Erklärungen über den bestehenden Mantel gesichert. Bildschirmzustand ohne Protokollaufnahme wird bewusst nicht konserviert.

`class6-drawing.cjs` passt das digitale Codefeld und den Papierweg an. Papier bietet manuelle Ausführung mit Raster und Marker; eigene Geräteausführung bleibt nachzuholen. Änderung im gemeinsamen Autorenrenderer ist auf Klasse 6/drawing begrenzt.

## Verifikation

- 53 Tests bestanden: Interpreter/Gegenfälle, Integration, bestehende Inhalte und Mantel-Speicherwege. Vollständiger Build 639 Dateien, interne Links validiert.
- 377 bestehende Klasse-5-Ausgabedateien bytegleich, Inhaltsquellen M01–M04 unverändert.
- Tatsächlicher Browserdurchgang: eigene Bandfassungen, Einzelschritt, Quadratkorrektur, Stiftlücke, Syntaxfehler ohne alten Erfolg, Wissen/Rückweg, Export und Import in neuen leeren Tab. Desktop und 390-Pixel-Ansicht.
- Zwölf PDF-Prüfrender mit insgesamt 28 Seiten vollständig visuell gesichtet (13 Lernenden-, 15 Hilfen-/Lösungsseiten).
- Qualitätszyklus R1 → Nacharbeit → R2 → Nacharbeit → R3: **READY_FOR_REVIEW**, 17 Kriterien. Prüffassung `95600f2484781bb8671e810ab22a13db889e1499cc943e29c9dc9a4e81fe2569`.
- F01 Schleifenformulierung, F02 Papierweg und F03 Cursorposition behoben. F04 kleiner Layoutrest akzeptiert: Modellblatt mit kurzer zweiter Kriterienseite und einzelne locker gesetzte Lösungsseiten. Keine offenen wesentlichen Befunde.

Prüfbereich auf TIER: `C:/Users/Jan/AI-Workspace-Local/Work/ium-klasse6-m05-qa-20261022/` mit `run.json`, `report-final.md`, `check-final.json`, `review-final.md`, `tests-release.txt`, `preservation.txt`, `build-final2/`, Druck-PDFs und Sichtnachweisen. Formaler Pass bedeutet bereit zur Sichtung. Reale Lerngruppe/Zeit, Schulgeräte/Touch, vollständiger Screenreader und physischer Druck bleiben zu prüfen.

## Fortsetzung

M06 „Kommunikationsräume beurteilen“, 165 Kernminuten. Vorher sechs Minuten M03- und sieben Minuten M05-Abruf einplanen. Reale Kommunikation, Hilfeweg und privater Eigenbezug bleiben eigenständige Nachweise. M07 folgt anschließend. Vor Übernahme auf anderes Gerät Quellbranch und aktuellen main-Stand integrieren; dieses lokale Review ist keine Publikationsfreigabe.
