# Klasse 7 – gemeinsame Jahreswege

Dieser Adapter ergänzt den Jahrgangseinstieg, den Jahresleitfaden, die Zielzuordnung und vier spätere Abruffälle. Die 22 Kernaufgaben bleiben in ihren bisherigen Quellen. `addYearRoutes` folgt den vier Unit-Adaptern und geht der Klassenstufenwahl voraus; die Snap-Arbeitsfläche wird ausgelassen. Der alte Jahrgangsbrief-Link bleibt als Wegweiser zum gemeinsamen Leitfaden erhalten.

## Quellen und Aktualisierung

Kanonische Texte: `Vault/40_Projekte/IuM-Lernwerk/Klasse 7/Jahreswege/` im AI-Workspace. Renderquelle: `Shared/Scripts/Build-IuM7-Jahreswege.mjs`; Aufruf mit Workspace-, Repo- und lokalem Marked-ESM-Pfad. `material/` enthält die synchronisierten Markdowntexte, `inhalt/` die HTML-Lesefassung und vier unverändert übernommene Diagnosedateien. `quelle-sha256.json` bindet die importierten Quellen und die daraus erzeugten Dateien. Änderungen zuerst an der kanonischen Quelle vornehmen, dann rendern und prüfen.

Die Pages-CI benötigt keine zusätzlichen Pakete; sie liest die gebundenen fertigen Quelldateien. Reviewprotokolle, Serverlogs und vollständige Vorschau-Builds gehören nicht in diesen Baustein.

## Prüfverantwortung

`jahrgang.test.cjs` prüft den Erhalt der fachlichen Hauptinhalte, die 22 Aufgaben, 29 Zielzeilen, die einheitliche Navigation und lokale Pfade. `pages/grade-navigation.test.cjs` prüft separat den Schritt von gemeinsamer Navigation zu Klassenwahl. `klasse7-programmieren/layout.test.cjs` prüft isoliert den bestehenden Reihenlayout-Adapter; Gesamtverhalten bleibt durch die Jahrgangs- und Einheitentests gebunden. Die privaten Reflexionswege, tatsächlichen Handlungen und 270/270/405/270 Minuten bleiben bestehen.
